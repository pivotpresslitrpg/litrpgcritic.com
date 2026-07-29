#!/usr/bin/env python3
"""Automated blog post generator.

Runs on a schedule via GitHub Actions. Reads site_config.py for site-specific
settings, loads topics.json for rotation state, generates a post via Claude API,
writes it to the Astro content directory, and pushes to trigger a deploy.
"""

import os
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

import anthropic
import requests

from content_guard import retry_guidance, validate_generated_content
from site_config import CONFIG

# Paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
TOPICS_FILE = SCRIPT_DIR / 'topics.json'
CONTENT_DIR = REPO_ROOT / CONFIG['content_dir']

# Claude client is initialized lazily so helper tests do not require a live key.
client = None


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def load_state() -> dict:
    if TOPICS_FILE.exists():
        return json.loads(TOPICS_FILE.read_text())
    return {
        'rotation_index': 0,
        'published_slugs': [],
        'author_queue_index': 0,
        'anchor_queue_index': 0,
        'feature_queue_index': 0,
        'explainer_queue_index': 0,
    }


def save_state(state: dict):
    TOPICS_FILE.write_text(json.dumps(state, indent=2))


def _published_entries() -> list[tuple[str, str]]:
    entries = []
    for path in CONTENT_DIR.glob('*.md'):
        text = path.read_text(encoding='utf-8')
        title_match = re.search(r'^title:\s*["\']?([^"\'\n]+)', text, re.MULTILINE)
        type_match = re.search(r'^type:\s*["\']?([^"\'\n]+)', text, re.MULTILINE)
        if title_match and type_match:
            entries.append((title_match.group(1), type_match.group(1)))
    return entries


def _title_tokens(value: str) -> set[str]:
    tokens = re.findall(r'[a-z0-9]+', value.lower())
    return {token[:-1] if len(token) > 4 and token.endswith('s') else token for token in tokens}


def pick_unpublished_item(items: list, state: dict, index_key: str, content_type: str):
    if not items:
        raise RuntimeError(f"No configured items for {content_type}.")

    entries = _published_entries()
    start = state.get(index_key, 0)
    for offset in range(len(items)):
        item = items[(start + offset) % len(items)]
        label = item['name'] if isinstance(item, dict) else item
        marker = _title_tokens(label)
        already_used = any(
            existing_type == content_type and marker.issubset(_title_tokens(title))
            for title, existing_type in entries
        )
        if not already_used:
            state[index_key] = start + offset + 1
            return item

    raise RuntimeError(
        f"All configured {content_type} subjects have already been published. "
        "Add new queue items before the next run."
    )


# ---------------------------------------------------------------------------
# Book data helpers
# ---------------------------------------------------------------------------

def fetch_books(sort='top_rated', genre=None, limit=20) -> list:
    api_key = os.environ.get('BLOG_FEED_API_KEY', '')
    if not api_key:
        return []
    params = {'limit': str(limit), 'sort': sort}
    if genre:
        params['genre'] = genre
    try:
        resp = requests.get(
            f"{CONFIG['api_base']}/api/blog-feed/books",
            headers={'X-Blog-Feed-Key': api_key},
            params=params,
            timeout=15
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            return data
        return data.get('items', data.get('data', []))
    except Exception as e:
        print(f"Warning: failed to fetch books: {e}")
        return []


def fetch_recent_books(days=30, limit=20) -> list:
    api_key = os.environ.get('BLOG_FEED_API_KEY', '')
    if not api_key:
        return []
    try:
        resp = requests.get(
            f"{CONFIG['api_base']}/api/blog-feed/books/recent",
            headers={'X-Blog-Feed-Key': api_key},
            params={'days': str(days), 'limit': str(limit)},
            timeout=15
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            return data
        return data.get('items', data.get('data', []))
    except Exception as e:
        print(f"Warning: failed to fetch recent books: {e}")
        return []


def format_book_list(books: list, max_books=15) -> str:
    if not books:
        return "(no verified book data available)"
    lines = []
    for b in books[:max_books]:
        title = b.get('title', 'Unknown')
        authors = b.get('authors', [])
        author_str = ', '.join(authors) if authors else 'Unknown'
        rating = b.get('average_rating') or b.get('amazon_rating')
        review_count = b.get('review_count')
        series = b.get('series_name', '')
        genres = b.get('genres') or []
        published_date = b.get('published_date')
        description = re.sub(r'\s+', ' ', b.get('description') or '').strip()
        line = f"- {title} by {author_str}"
        if series:
            line += f" ({series})"
        if rating:
            line += f"; rating: {float(rating):.1f}/5"
            if review_count:
                line += f" from {int(review_count)} reviews"
        if genres:
            line += f"; genres: {', '.join(genres)}"
        if published_date:
            line += f"; published: {published_date}"
        if description:
            line += f"\n  Description: {description[:500]}"
        lines.append(line)
    return '\n'.join(lines)


SOURCE_RULES = """
SOURCE RULES:
- The VERIFIED SOURCE PACKET below is the only evidence for named books, authors,
  series, characters, plots, dates, genres, ratings, rankings, and comparisons.
- Recommend or describe only titles present in that packet.
- Never fill gaps from memory. If the packet does not support a detail, omit it.
- Editorial opinions are allowed only when clearly framed as opinions and grounded
  in a supplied description, genre, or rating.
- These rules override promotion guidance: do not insert a promoted author or
  title unless that exact author-title relationship appears in the packet.
"""


def pick_supported_author(items: list, state: dict, books: list) -> tuple[str, list]:
    entries = _published_entries()
    start = state.get('author_queue_index', 0)

    for offset in range(len(items)):
        author = items[(start + offset) % len(items)]
        marker = _title_tokens(author)
        already_used = any(
            existing_type == 'author_spotlight' and marker.issubset(_title_tokens(title))
            for title, existing_type in entries
        )
        author_key = re.sub(r'[^a-z0-9]+', '', author.lower())
        author_books = [
            book for book in books
            if any(
                re.sub(r'[^a-z0-9]+', '', candidate.lower()) == author_key
                for candidate in book.get('authors', [])
            )
        ]
        if not already_used and author_books:
            state['author_queue_index'] = start + offset + 1
            return author, author_books

    raise RuntimeError(
        "No unpublished author spotlight has verified books in the feed. "
        "Refresh the author queue or feed before publishing."
    )


# ---------------------------------------------------------------------------
# Post type generators
# Each returns a dict with 'prompt' and 'type' keys.
# Generators that advance queue indexes update state in-place and return it.
# ---------------------------------------------------------------------------

def gen_new_releases(state: dict) -> dict:
    books = fetch_recent_books(days=30, limit=20)
    if not books:
        books = fetch_books(sort='recent', limit=20)
    if not books:
        raise RuntimeError("Verified recent-book data is unavailable; refusing to publish.")
    book_data = format_book_list(books)

    prompt = f"""You are writing an editorial blog post for {CONFIG['site_name']}.

Site description: {CONFIG['site_description']}
Voice: {CONFIG['voice']}

POST TYPE: New Releases Roundup
Cover notable recent releases in {CONFIG['genre']}.

VERIFIED SOURCE PACKET — recent books from the community database:
{book_data}

{SOURCE_RULES}
{CONFIG['promotion_guidance']}

---
Output a complete blog post. Start with YAML frontmatter, then markdown content.

Frontmatter format (fill in the values):
---
title: "..."
description: "..."
date: "{datetime.now().strftime('%Y-%m-%d')}"
type: "new_releases"
author: "{CONFIG['author']}"
tags: [...]
featured: false
---

Writing requirements:
- 500-750 words
- Cover 4-6 specific books from the source packet; summarize only supplied details
- Natural editorial prose — not a listicle
- Mention {CONFIG['platform_name']} once, naturally, as a resource for finding more
- End with an invitation to explore
- Do NOT include affiliate links or price information"""
    return {'prompt': prompt, 'type': 'new_releases'}


def gen_author_spotlight(state: dict) -> dict:
    authors = CONFIG['featured_authors']
    books = fetch_books(sort='top_rated', limit=100)
    if not books:
        raise RuntimeError("Verified book data is unavailable; refusing to publish.")
    author, author_books = pick_supported_author(authors, state, books)
    book_data = format_book_list(author_books)

    prompt = f"""You are writing an editorial blog post for {CONFIG['site_name']}.

Site description: {CONFIG['site_description']}
Voice: {CONFIG['voice']}

POST TYPE: Author Spotlight
Subject author: {author}

VERIFIED SOURCE PACKET — their books in our community database:
{book_data}

{SOURCE_RULES}
{CONFIG['promotion_guidance']}

---
Output a complete blog post. Start with YAML frontmatter, then markdown content.

Frontmatter format:
---
title: "..."
description: "..."
date: "{datetime.now().strftime('%Y-%m-%d')}"
type: "author_spotlight"
author: "{CONFIG['author']}"
tags: ["{author}", ...]
featured: false
---

Writing requirements:
- 600-900 words
- Build a catalog guide from the supplied descriptions, genres, series, and dates
- Recommend an entry point only when the packet supports that recommendation
- Mention only series and titles present in the source packet
- Mention {CONFIG['platform_name']} as a place to discover more of their work
- Warm, enthusiastic editorial tone — like a recommendation from a well-read friend"""
    return {'prompt': prompt, 'type': 'author_spotlight', 'state': state}


def gen_genre_explainer(state: dict) -> dict:
    topics = CONFIG['explainer_topics']
    topic = pick_unpublished_item(topics, state, 'explainer_queue_index', 'genre_explainer')

    books = fetch_books(sort='top_rated', genre=topic, limit=20)
    if not books:
        raise RuntimeError(
            f"No verified book data is available for {topic!r}; refusing to publish."
        )
    book_data = format_book_list(books)

    prompt = f"""You are writing an editorial blog post for {CONFIG['site_name']}.

Site description: {CONFIG['site_description']}
Voice: {CONFIG['voice']}

POST TYPE: Genre / Sub-genre Explainer
Topic: {topic}

VERIFIED SOURCE PACKET — books tagged for this topic in our database:
{book_data}

{SOURCE_RULES}
{CONFIG['promotion_guidance']}

---
Output a complete blog post. Start with YAML frontmatter, then markdown content.

Frontmatter format:
---
title: "..."
description: "..."
date: "{datetime.now().strftime('%Y-%m-%d')}"
type: "genre_explainer"
author: "{CONFIG['author']}"
tags: ["{topic}", ...]
featured: false
---

Writing requirements:
- 700-1000 words
- Define the sub-genre clearly for someone new to it
- Explain what makes it appealing and who it's for
- Recommend 5-8 gateway books only when their supplied genres and descriptions fit
- Use general knowledge only for the high-level definition, never for named-title facts
- Include one natural mention of {CONFIG['platform_name']}"""
    return {'prompt': prompt, 'type': 'genre_explainer', 'state': state}


def gen_platform_feature(state: dict) -> dict:
    features = CONFIG['platform_features']
    feature = pick_unpublished_item(features, state, 'feature_queue_index', 'platform_feature')

    prompt = f"""You are writing an editorial blog post for {CONFIG['site_name']}.

Site description: {CONFIG['site_description']}
Voice: {CONFIG['voice']}

POST TYPE: Platform Feature Discovery
Platform: {CONFIG['platform_name']} ({CONFIG['platform_url']})
Feature: {feature['name']}
Feature description: {feature['description']}

{CONFIG['promotion_guidance']}

---
Output a complete blog post. Start with YAML frontmatter, then markdown content.

Frontmatter format:
---
title: "..."
description: "..."
date: "{datetime.now().strftime('%Y-%m-%d')}"
type: "platform_feature"
author: "{CONFIG['author']}"
tags: [...]
featured: false
---

Writing requirements:
- 500-700 words
- Write as an editorial discovery piece, not marketing copy
- Explain what the feature does and why readers in this genre will find it useful
- Include the platform URL ({CONFIG['platform_url']}) at least once, naturally
- Authentic, enthusiastic editorial tone
- No hype language — let the feature speak for itself"""
    return {'prompt': prompt, 'type': 'platform_feature', 'state': state}


def gen_books_like(state: dict) -> dict:
    anchor_books = CONFIG.get('anchor_books', [])
    anchor = pick_unpublished_item(
        anchor_books,
        state,
        'anchor_queue_index',
        'books_like',
    ) if anchor_books else None

    books = fetch_books(sort='top_rated', limit=25)
    if not books:
        raise RuntimeError("Verified recommendation data is unavailable; refusing to publish.")
    book_data = format_book_list(books)

    anchor_line = f"Anchor title: {anchor}" if anchor else "Choose a well-known anchor title in the genre."

    prompt = f"""You are writing an editorial blog post for {CONFIG['site_name']}.

Site description: {CONFIG['site_description']}
Voice: {CONFIG['voice']}

POST TYPE: "Books Like X" Recommendation Guide
{anchor_line}

VERIFIED SOURCE PACKET — candidate books in our database:
{book_data}

{SOURCE_RULES}
{CONFIG['promotion_guidance']}

---
Output a complete blog post. Start with YAML frontmatter, then markdown content.

Frontmatter format:
---
title: "If You Liked [X], Read These Next"
description: "..."
date: "{datetime.now().strftime('%Y-%m-%d')}"
type: "books_like"
author: "{CONFIG['author']}"
tags: [...]
featured: false
---

Writing requirements:
- 500-700 words
- Recommend 5-8 books from the source packet that are demonstrably similar
- For each recommendation, use only supplied genres and descriptions to explain the match
- Include a mention of {CONFIG['platform_name']} for finding similar reads
- Conversational, enthusiastic tone"""
    return {'prompt': prompt, 'type': 'books_like'}


def gen_fateforged(state: dict) -> dict:
    """HaremLit Guide only — Fateforged universe editorial pieces."""
    FATEFORGED_CONTEXT = """
The Fateforged Shared Universe is a connected harem fantasy series with multiple authors
and an interlocking timeline. Key series:

- Isekai Emperor (Adam Lance & Michael Dalton) — modern man isekai'd to a fantasy empire
- Trailer Park Elves (Adam Lance & Michael Dalton) — elves living in modern rural America
- King of the Fae Islands (Adam Lance & Annabelle Hawthorne) — fae realm harem fantasy
- Isle of the Amazonian Elves (Adam Lance & Leon West) — stranded on an amazon elf island
- Dungeon Champions (Adam Lance & Leon West) — dungeon diving with a companion harem

Adam Lance is the shared pen name of Aaron Renfroe, founder of Harem-Lit.com.
The universe has crossover characters, shared lore, and a grand connected timeline across all series.

IMPORTANT: Do NOT mention "Pivot Press" anywhere in generated content. Refer to the shared
world as "Fateforged" and authors by name only.
"""
    angles = [
        "a complete reading order guide for the Fateforged universe",
        "why the Fateforged universe has become a fan favorite in the harem fantasy community",
        "the best entry points into Fateforged for readers new to the universe",
        "the collaborative writing approach behind the Fateforged series",
        "the world-building and lore connecting all Fateforged series",
    ]
    idx = state.get('author_queue_index', 0)
    angle = angles[idx % len(angles)]

    books = fetch_books(sort='top_rated', limit=60)
    fateforged_authors = ['adam lance', 'annabelle hawthorne', 'leon west', 'michael dalton']
    fateforged_books = [
        b for b in books
        if any(fa in a.lower() for fa in fateforged_authors for a in b.get('authors', []))
    ]
    book_data = format_book_list(fateforged_books) if fateforged_books else "(use context above)"

    prompt = f"""You are writing an editorial blog post for {CONFIG['site_name']}.

Site description: {CONFIG['site_description']}
Voice: {CONFIG['voice']}

POST TYPE: Fateforged Universe Feature
Angle: {angle}

Fateforged universe background:
{FATEFORGED_CONTEXT}

Fateforged books in our database:
{book_data}

{CONFIG['promotion_guidance']}

---
Output a complete blog post. Start with YAML frontmatter, then markdown content.

Frontmatter format:
---
title: "..."
description: "..."
date: "{datetime.now().strftime('%Y-%m-%d')}"
type: "fateforged"
author: "{CONFIG['author']}"
tags: ["Fateforged", "Adam Lance", ...]
featured: false
---

Writing requirements:
- 700-1000 words
- Enthusiastic insider tone — write like a fan who's also an editor
- Mention Harem-Lit.com as the community home for Fateforged discussion
- Cover all relevant series, not just one
- Focus on what makes the universe special for harem fantasy fans
- This should feel like genuine editorial enthusiasm, not a press release"""
    return {'prompt': prompt, 'type': 'fateforged'}


def gen_cross_genre(state: dict) -> dict:
    """Fantasy Ranked only — cross-genre comparison pieces."""
    books_litrpg = fetch_books(sort='top_rated', limit=12)
    books_harem = fetch_books(sort='top_rated', limit=12)

    prompt = f"""You are writing an editorial blog post for {CONFIG['site_name']}.

Site description: {CONFIG['site_description']}
Voice: {CONFIG['voice']}

POST TYPE: Cross-Genre Comparison
Compare and connect LitRPG / progression fantasy with harem fantasy / men's romance fantasy
for readers who enjoy elements of both.

Books from our LitRPG database:
{format_book_list(books_litrpg)}

Books from our harem fantasy database:
{format_book_list(books_harem)}

{CONFIG['promotion_guidance']}

---
Output a complete blog post. Start with YAML frontmatter, then markdown content.

Frontmatter format:
---
title: "..."
description: "..."
date: "{datetime.now().strftime('%Y-%m-%d')}"
type: "cross_genre"
author: "{CONFIG['author']}"
tags: [...]
featured: false
---

Writing requirements:
- 600-800 words
- Compare the appeal of both genres to overlapping fan bases
- Identify crossover titles that fans of one genre would enjoy
- Use your own genre knowledge plus the database lists
- Mention both LitRPGTools.com and Harem-Lit.com naturally as community resources
- Confident, cross-genre authority voice"""
    return {'prompt': prompt, 'type': 'cross_genre'}


def gen_platform_bridge(state: dict) -> dict:
    """Fantasy Ranked only — platform discovery piece."""
    platforms = [
        {
            'name': 'LitRPGTools.com',
            'url': 'https://litrpgtools.com',
            'description': 'LitRPG book database, AI-powered generators (character builds, skill trees, dungeon runs, boss encounters, world systems), community ratings and reviews, gamification system',
        },
        {
            'name': 'Harem-Lit.com',
            'url': 'https://harem-lit.com',
            'description': 'Men\'s romance and harem fantasy book database, Allure gacha card collector game (character cards from harem novels, daily pulls, rarities, card battles), community ratings, author profiles',
        },
    ]
    idx = state.get('feature_queue_index', 0)
    platform = platforms[idx % len(platforms)]
    state['feature_queue_index'] = idx + 1

    prompt = f"""You are writing an editorial blog post for {CONFIG['site_name']}.

Site description: {CONFIG['site_description']}
Voice: {CONFIG['voice']}

POST TYPE: Platform Discovery Feature
Platform: {platform['name']} ({platform['url']})
What it offers: {platform['description']}

{CONFIG['promotion_guidance']}

---
Output a complete blog post. Start with YAML frontmatter, then markdown content.

Frontmatter format:
---
title: "..."
description: "..."
date: "{datetime.now().strftime('%Y-%m-%d')}"
type: "platform_bridge"
author: "{CONFIG['author']}"
tags: [...]
featured: false
---

Writing requirements:
- 500-700 words
- Editorial discovery piece — write as if introducing readers to something genuinely useful
- Focus on what readers can discover and do on the platform
- Include the platform URL ({platform['url']}) at least once, naturally
- No hype language — authentic editorial voice"""
    return {'prompt': prompt, 'type': 'platform_bridge', 'state': state}


# ---------------------------------------------------------------------------
# Generator registry
# ---------------------------------------------------------------------------

GENERATORS = {
    'new_releases': gen_new_releases,
    'author_spotlight': gen_author_spotlight,
    'genre_explainer': gen_genre_explainer,
    'platform_feature': gen_platform_feature,
    'books_like': gen_books_like,
    'fateforged': gen_fateforged,
    'cross_genre': gen_cross_genre,
    'platform_bridge': gen_platform_bridge,
}


# ---------------------------------------------------------------------------
# Rotation
# ---------------------------------------------------------------------------

def pick_post_type(state: dict) -> str:
    rotation = CONFIG['rotation']
    idx = state.get('rotation_index', 0)
    post_type = rotation[idx % len(rotation)]
    state['rotation_index'] = idx + 1
    return post_type


# ---------------------------------------------------------------------------
# Post writing
# ---------------------------------------------------------------------------

def slugify(title: str) -> str:
    s = re.sub(r'[^\w\s-]', '', title.lower())
    s = re.sub(r'[\s_]+', '-', s).strip('-')
    return s[:80]


def clean_response(text: str) -> str:
    """Strip code fences and duplicate H1 from Claude's response."""
    # Remove code-fence-wrapped frontmatter: ```yaml\n---\n...\n---\n```
    text = re.sub(r'```(?:yaml|yml)?\s*\n(---\n.*?\n---)\s*\n```', r'\1', text, count=1, flags=re.DOTALL)
    # Remove any leading H1 that duplicates the frontmatter title
    m = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', text)
    if m:
        title = m.group(1).strip()
        # Strip leading "# Title" line after frontmatter closing ---
        text = re.sub(
            r'(---\s*\n)\s*#\s+' + re.escape(title) + r'\s*\n',
            r'\1\n',
            text,
            count=1,
        )
    return text


def call_claude(prompt: str, *, inject_guidance: bool = True) -> str:
    global client
    if client is None:
        client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

    # Inject editorial and formatting guidance into generation prompts.
    extra = ''
    if inject_guidance:
        if CONFIG.get('geo_guidance'):
            extra += f"\n\n{CONFIG['geo_guidance']}"
        if CONFIG.get('internal_link_guidance'):
            extra += f"\n\n{CONFIG['internal_link_guidance']}"
        extra += (
            "\n\nCRITICAL FORMATTING RULES:\n"
            "- Output raw markdown ONLY. Do NOT wrap anything in code fences (no ``` blocks).\n"
            "- Do NOT include an H1 heading (# Title) in the body. The title comes from frontmatter only.\n"
            "- Start body content directly with the opening paragraph after the closing ---."
        )
    full_prompt = prompt + extra

    print("Calling Claude API...")
    resp = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=2200,
        messages=[{'role': 'user', 'content': full_prompt}]
    )
    return clean_response(resp.content[0].text)


def audit_draft_against_sources(source_prompt: str, content: str) -> str | None:
    if 'VERIFIED SOURCE PACKET' not in source_prompt:
        return None

    audit = call_claude(f"""Act as a strict pre-publication fact checker.

The ORIGINAL BRIEF contains a section labeled VERIFIED SOURCE PACKET. For named
books, authors, series, characters, plots, dates, genres, ratings, rankings, and
comparisons, only that packet is evidence. Instructions, model memory, and
general familiarity are not evidence.

Check the DRAFT for:
- a title attributed to the wrong author or series
- a character, premise, reading order, genre label, rating, or comparison not
  explicitly supported by the packet
- a recommendation whose title is absent from the packet
- confident biographical or catalog claims not supported by the packet

General genre definitions and clearly labeled editorial opinions may pass.

Return exactly PASS if every named factual claim is supported. Otherwise return
FAIL followed by concise bullets describing every unsupported or contradictory
claim so the writer can remove or correct them.

ORIGINAL BRIEF:
{source_prompt}

DRAFT:
{content}
""", inject_guidance=False)
    if audit.strip().upper() == 'PASS':
        return None
    return f"source-grounding audit failed: {audit.strip()[:1200]}"


def generate_validated_content(prompt: str, post_type: str) -> str:
    retry_suffix = ''
    expected_date = datetime.now().strftime('%Y-%m-%d')

    for attempt in range(1, 4):
        content = call_claude(prompt + retry_suffix)

        stripped = content.strip()
        if stripped.startswith('```'):
            first_newline = stripped.find('\n')
            if first_newline != -1:
                stripped = stripped[first_newline + 1:]
            if stripped.rstrip().endswith('```'):
                stripped = stripped.rstrip()[:-3].rstrip()
            content = stripped

        if not content.strip().startswith('---'):
            content = f"""---
title: "Post"
description: "Generated post"
date: "{expected_date}"
type: "{post_type}"
author: "{CONFIG['author']}"
tags: []
featured: false
---

{content}"""

        issues = validate_generated_content(
            content,
            content_dir=CONTENT_DIR,
            expected_date=expected_date,
            expected_type=post_type,
            platform_url=CONFIG['platform_url'],
            allowed_internal_links=CONFIG['allowed_internal_links'],
        )
        if not issues:
            source_issue = audit_draft_against_sources(prompt, content)
            if source_issue:
                issues.append(source_issue)

        if not issues:
            print(f"Content quality gate passed on attempt {attempt}.")
            return content

        print(f"Content quality gate failed on attempt {attempt}:")
        for issue in issues:
            print(f"- {issue}")
        retry_suffix = retry_guidance(issues)

    raise RuntimeError("Generated content failed the quality gate after 3 attempts.")


def extract_title(content: str) -> str:
    m = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
    return m.group(1).strip() if m else 'post'


def write_post(content: str, published_slugs: list) -> str:
    title = extract_title(content)
    date_str = datetime.now().strftime('%Y-%m-%d')
    slug = slugify(title)

    # Unique slug check
    base = slug
    counter = 1
    while f"{date_str}-{slug}" in published_slugs:
        slug = f"{base}-{counter}"
        counter += 1

    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{date_str}-{slug}.md"
    filepath = CONTENT_DIR / filename
    filepath.write_text(content, encoding='utf-8')
    print(f"Written: {filepath}")
    return f"{date_str}-{slug}"


def git_push(slug: str):
    subprocess.run(['git', 'config', 'user.email', 'bot@litrpgcritic.com'], check=True, cwd=REPO_ROOT)
    subprocess.run(['git', 'config', 'user.name', 'LitRPG Critic Bot'], check=True, cwd=REPO_ROOT)
    subprocess.run(['git', 'add', str(CONTENT_DIR)], check=True, cwd=REPO_ROOT)
    subprocess.run(['git', 'add', str(TOPICS_FILE)], check=True, cwd=REPO_ROOT)
    result = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=REPO_ROOT)
    if result.returncode != 0:
        subprocess.run(['git', 'commit', '-m', f'[bot] {slug}'], check=True, cwd=REPO_ROOT)
        subprocess.run(['git', 'push'], check=True, cwd=REPO_ROOT)
        print("Pushed to remote.")
    else:
        print("No changes to commit.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    state = load_state()
    post_type = pick_post_type(state)
    print(f"Post type: {post_type}")

    gen_fn = GENERATORS.get(post_type)
    if not gen_fn:
        print(f"Unknown post type: {post_type}, skipping.")
        return

    result = gen_fn(state)
    if 'state' in result:
        state.update(result['state'])

    content = generate_validated_content(result['prompt'], post_type)

    slug = write_post(content, state.get('published_slugs', []))
    state.setdefault('published_slugs', []).append(slug)
    save_state(state)
    git_push(slug)


if __name__ == '__main__':
    main()
