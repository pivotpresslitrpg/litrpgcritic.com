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

from site_config import CONFIG

# Paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
TOPICS_FILE = SCRIPT_DIR / 'topics.json'
CONTENT_DIR = REPO_ROOT / CONFIG['content_dir']

# Claude client
client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])


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
        'feature_queue_index': 0,
        'explainer_queue_index': 0,
    }


def save_state(state: dict):
    TOPICS_FILE.write_text(json.dumps(state, indent=2))


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
        return "(no book data available — use your knowledge of the genre)"
    lines = []
    for b in books[:max_books]:
        title = b.get('title', 'Unknown')
        authors = b.get('authors', [])
        author_str = ', '.join(authors) if authors else 'Unknown'
        rating = b.get('average_rating') or b.get('amazon_rating')
        series = b.get('series_name', '')
        line = f"- {title} by {author_str}"
        if series:
            line += f" ({series})"
        if rating:
            line += f" — {float(rating):.1f}★"
        lines.append(line)
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Post type generators
# Each returns a dict with 'prompt' and 'type' keys.
# Generators that advance queue indexes update state in-place and return it.
# ---------------------------------------------------------------------------

def gen_new_releases(state: dict) -> dict:
    books = fetch_recent_books(days=30, limit=20)
    if not books:
        books = fetch_books(sort='recent', limit=20)
    book_data = format_book_list(books)

    prompt = f"""You are writing an editorial blog post for {CONFIG['site_name']}.

Site description: {CONFIG['site_description']}
Voice: {CONFIG['voice']}

POST TYPE: New Releases Roundup
Cover notable recent releases in {CONFIG['genre']}.

Recent books from the community database:
{book_data}

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
- Cover 4-6 specific books; briefly say why each is worth attention
- Natural editorial prose — not a listicle
- Mention {CONFIG['platform_name']} once, naturally, as a resource for finding more
- End with an invitation to explore
- Do NOT include affiliate links or price information"""
    return {'prompt': prompt, 'type': 'new_releases'}


def gen_author_spotlight(state: dict) -> dict:
    idx = state.get('author_queue_index', 0)
    authors = CONFIG['featured_authors']
    author = authors[idx % len(authors)]
    state['author_queue_index'] = idx + 1

    books = fetch_books(sort='top_rated', limit=60)
    author_books = [
        b for b in books
        if any(author.lower() in a.lower() for a in b.get('authors', []))
    ]
    book_data = format_book_list(author_books) if author_books else "(use your knowledge of this author's work)"

    prompt = f"""You are writing an editorial blog post for {CONFIG['site_name']}.

Site description: {CONFIG['site_description']}
Voice: {CONFIG['voice']}

POST TYPE: Author Spotlight
Subject author: {author}

Their books in our community database:
{book_data}

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
- Cover this author's writing style, recurring themes, and what makes their work distinctive
- Recommend a reading order or entry point for new readers
- Mention series by name where relevant
- Mention {CONFIG['platform_name']} as a place to discover more of their work
- Warm, enthusiastic editorial tone — like a recommendation from a well-read friend"""
    return {'prompt': prompt, 'type': 'author_spotlight', 'state': state}


def gen_genre_explainer(state: dict) -> dict:
    idx = state.get('explainer_queue_index', 0)
    topics = CONFIG['explainer_topics']
    topic = topics[idx % len(topics)]
    state['explainer_queue_index'] = idx + 1

    books = fetch_books(sort='top_rated', limit=20)
    book_data = format_book_list(books)

    prompt = f"""You are writing an editorial blog post for {CONFIG['site_name']}.

Site description: {CONFIG['site_description']}
Voice: {CONFIG['voice']}

POST TYPE: Genre / Sub-genre Explainer
Topic: {topic}

Top rated books from our database (may or may not be directly relevant):
{book_data}

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
- Recommend 5-8 gateway books with brief descriptions of each
- Draw on your own knowledge of the genre, not just the database list
- Include one natural mention of {CONFIG['platform_name']}"""
    return {'prompt': prompt, 'type': 'genre_explainer', 'state': state}


def gen_platform_feature(state: dict) -> dict:
    idx = state.get('feature_queue_index', 0)
    features = CONFIG['platform_features']
    feature = features[idx % len(features)]
    state['feature_queue_index'] = idx + 1

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
    idx = state.get('author_queue_index', 0)
    anchor = anchor_books[idx % len(anchor_books)] if anchor_books else None

    books = fetch_books(sort='top_rated', limit=25)
    book_data = format_book_list(books)

    anchor_line = f"Anchor title: {anchor}" if anchor else "Choose a well-known anchor title in the genre."

    prompt = f"""You are writing an editorial blog post for {CONFIG['site_name']}.

Site description: {CONFIG['site_description']}
Voice: {CONFIG['voice']}

POST TYPE: "Books Like X" Recommendation Guide
{anchor_line}

Top rated books in our database:
{book_data}

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
- Recommend 5-8 books similar to the anchor title
- For each recommendation, give 1-2 sentences explaining why fans of the anchor will enjoy it
- Draw on both the database list AND your knowledge of the genre
- Include a mention of {CONFIG['platform_name']} for finding similar reads
- Conversational, enthusiastic tone"""
    return {'prompt': prompt, 'type': 'books_like'}


def gen_fateforged(state: dict) -> dict:
    """HaremLit Guide only — Fateforged universe editorial pieces."""
    FATEFORGED_CONTEXT = """
The Fateforged Shared Universe is a connected harem fantasy series from Pivot Press,
with multiple authors and an interlocking timeline. Key series:

- Isekai Emperor (Adam Lance & Michael Dalton) — modern man isekai'd to a fantasy empire
- Trailer Park Elves (Adam Lance & Michael Dalton) — elves living in modern rural America
- King of the Fae Islands (Adam Lance & Annabelle Hawthorne) — fae realm harem fantasy
- Isle of the Amazonian Elves (Adam Lance & Leon West) — stranded on an amazon elf island
- Dungeon Champions (Adam Lance & Leon West) — dungeon diving with a companion harem

Adam Lance is the shared pen name of Aaron Renfroe, founder of Pivot Press and Harem-Lit.com.
The universe has crossover characters, shared lore, and a grand connected timeline across all series.
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


def call_claude(prompt: str) -> str:
    # Inject GEO and internal link guidance into every prompt
    extra = ''
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
    subprocess.run(['git', 'config', 'user.email', 'bot@pivotpress.com'], check=True, cwd=REPO_ROOT)
    subprocess.run(['git', 'config', 'user.name', 'Pivot Press Bot'], check=True, cwd=REPO_ROOT)
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

    content = call_claude(result['prompt'])

    # Ensure output starts with frontmatter
    if not content.strip().startswith('---'):
        date_str = datetime.now().strftime('%Y-%m-%d')
        content = f"""---
title: "Post"
description: "Generated post"
date: "{date_str}"
type: "{post_type}"
author: "{CONFIG['author']}"
tags: []
featured: false
---

{content}"""

    slug = write_post(content, state.get('published_slugs', []))
    state.setdefault('published_slugs', []).append(slug)
    save_state(state)
    git_push(slug)


if __name__ == '__main__':
    main()
