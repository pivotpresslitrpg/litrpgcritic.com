#!/usr/bin/env python3
"""Automated book report generator.

Runs weekly via GitHub Actions. Reads a book extract from scripts/book_data/,
generates an SEO-optimized editorial book report via Claude API,
writes it to the Astro content directory, and pushes to trigger a deploy.

Each site gets a different voice and format for the same book.
"""

import os
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

import anthropic

from site_config import CONFIG

# Paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
BOOK_DATA_DIR = SCRIPT_DIR / 'book_data'
QUEUE_FILE = SCRIPT_DIR / 'book_queue.json'
CONTENT_DIR = REPO_ROOT / CONFIG['content_dir']

# Claude client
client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])


# ---------------------------------------------------------------------------
# Queue management
# ---------------------------------------------------------------------------

def load_queue() -> dict:
    if QUEUE_FILE.exists():
        return json.loads(QUEUE_FILE.read_text())
    return {'queue_index': 0, 'published': []}


def save_queue(queue: dict):
    QUEUE_FILE.write_text(json.dumps(queue, indent=2))


# ---------------------------------------------------------------------------
# Book data
# ---------------------------------------------------------------------------

BOOK_REGISTRY = [
    # Aaron Renfroe → litrpgcritic.com (and fantasyranked cross-posts)
    {
        'id': 'resonance-cycle-1',
        'series': 'The Resonance Cycle',
        'book_num': 1,
        'title': 'Divine Invasion',
        'full_title': 'Divine Invasion (The Resonance Cycle Book 1)',
        'author': 'Aaron Renfroe',
        'site': 'aaron',
        'genre_tags': ['LitRPG', 'progression fantasy', 'action RPG'],
        'incomplete_series': False,
    },
    {
        'id': 'resonance-cycle-2',
        'series': 'The Resonance Cycle',
        'book_num': 2,
        'title': 'The Resonance Cycle Book 2',
        'full_title': 'The Resonance Cycle Book 2',
        'author': 'Aaron Renfroe',
        'site': 'aaron',
        'genre_tags': ['LitRPG', 'progression fantasy'],
        'incomplete_series': False,
    },
    {
        'id': 'resonance-cycle-3',
        'series': 'The Resonance Cycle',
        'book_num': 3,
        'title': 'The Resonance Cycle Book 3',
        'full_title': 'The Resonance Cycle Book 3',
        'author': 'Aaron Renfroe',
        'site': 'aaron',
        'genre_tags': ['LitRPG', 'progression fantasy'],
        'incomplete_series': False,
    },
    {
        'id': 'resonance-cycle-4',
        'series': 'The Resonance Cycle',
        'book_num': 4,
        'title': 'The Resonance Cycle Book 4',
        'full_title': 'The Resonance Cycle Book 4',
        'author': 'Aaron Renfroe',
        'site': 'aaron',
        'genre_tags': ['LitRPG', 'progression fantasy'],
        'incomplete_series': False,
    },
    {
        'id': 'resonance-cycle-5',
        'series': 'The Resonance Cycle',
        'book_num': 5,
        'title': 'Torn Shroud',
        'full_title': 'Torn Shroud (The Resonance Cycle Book 5)',
        'author': 'Aaron Renfroe',
        'site': 'aaron',
        'genre_tags': ['LitRPG', 'progression fantasy'],
        'incomplete_series': False,
    },
    {
        'id': 'resonance-cycle-6',
        'series': 'The Resonance Cycle',
        'book_num': 6,
        'title': 'The Resonance Cycle Book 6',
        'full_title': 'The Resonance Cycle Book 6',
        'author': 'Aaron Renfroe',
        'site': 'aaron',
        'genre_tags': ['LitRPG', 'progression fantasy'],
        'incomplete_series': False,
    },
    {
        'id': 'resonance-cycle-7',
        'series': 'The Resonance Cycle',
        'book_num': 7,
        'title': 'Ignite the Dark',
        'full_title': 'Ignite the Dark (The Resonance Cycle Book 7)',
        'author': 'Aaron Renfroe',
        'site': 'aaron',
        'genre_tags': ['LitRPG', 'progression fantasy'],
        'incomplete_series': False,
    },
    {
        'id': 'spite-the-dark-1',
        'series': 'Spite the Dark',
        'book_num': 1,
        'title': 'Spite the Dark Book 1',
        'full_title': 'Spite the Dark Book 1',
        'author': 'Aaron Renfroe',
        'site': 'aaron',
        'genre_tags': ['LitRPG', 'dark fantasy', 'summoner'],
        'incomplete_series': True,
    },
    {
        'id': 'spite-the-dark-2',
        'series': 'Spite the Dark',
        'book_num': 2,
        'title': 'Shadow in Madness',
        'full_title': 'Shadow in Madness (Spite the Dark Book 2)',
        'author': 'Aaron Renfroe',
        'site': 'aaron',
        'genre_tags': ['LitRPG', 'dark fantasy', 'summoner'],
        'incomplete_series': True,
    },
    {
        'id': 'apocalypse-breaker-1',
        'series': 'Apocalypse BREAKER',
        'book_num': 1,
        'title': 'Apocalypse BREAKER Book 1',
        'full_title': 'Apocalypse BREAKER Book 1',
        'author': 'Aaron Renfroe',
        'site': 'aaron',
        'genre_tags': ['LitRPG', 'system apocalypse', 'action'],
        'incomplete_series': False,
    },
    {
        'id': 'apocalypse-breaker-2',
        'series': 'Apocalypse BREAKER',
        'book_num': 2,
        'title': 'Apocalypse BREAKER Book 2',
        'full_title': 'Apocalypse BREAKER Book 2',
        'author': 'Aaron Renfroe',
        'site': 'aaron',
        'genre_tags': ['LitRPG', 'system apocalypse', 'action'],
        'incomplete_series': False,
    },
    {
        'id': 'father-of-constructs-1',
        'series': 'Father of Constructs',
        'book_num': 1,
        'title': 'Father of Constructs Book 1',
        'full_title': 'Father of Constructs Book 1',
        'author': 'Aaron Renfroe',
        'site': 'aaron',
        'genre_tags': ['LitRPG', 'crafting', 'constructs', 'progression'],
        'incomplete_series': False,
    },
    {
        'id': 'father-of-constructs-2',
        'series': 'Father of Constructs',
        'book_num': 2,
        'title': 'Master of Steel',
        'full_title': 'Master of Steel (Father of Constructs Book 2)',
        'author': 'Aaron Renfroe',
        'site': 'aaron',
        'genre_tags': ['LitRPG', 'crafting', 'constructs', 'progression'],
        'incomplete_series': False,
    },
    {
        'id': 'father-of-constructs-3',
        'series': 'Father of Constructs',
        'book_num': 3,
        'title': 'The Eldritch Artisan',
        'full_title': 'The Eldritch Artisan (Father of Constructs Book 3)',
        'author': 'Aaron Renfroe',
        'site': 'aaron',
        'genre_tags': ['LitRPG', 'crafting', 'constructs', 'eldritch'],
        'incomplete_series': False,
    },
    # Adam Lance → haremlitguide.com (and fantasyranked cross-posts)
    {
        'id': 'isekai-emperor-1',
        'series': 'Isekai Emperor',
        'book_num': 1,
        'title': 'Isekai Emperor Book 1',
        'full_title': 'Isekai Emperor Book 1',
        'author': 'Adam Lance & Michael Dalton',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'isekai', 'empire building'],
        'incomplete_series': False,
    },
    {
        'id': 'isekai-emperor-3',
        'series': 'Isekai Emperor',
        'book_num': 3,
        'title': 'Isekai Emperor Book 3',
        'full_title': 'Isekai Emperor Book 3',
        'author': 'Adam Lance & Michael Dalton',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'isekai', 'empire building'],
        'incomplete_series': False,
    },
    {
        'id': 'king-fae-islands-1',
        'series': 'King of the Fae Islands',
        'book_num': 1,
        'title': 'King of the Fae Islands Book 1',
        'full_title': 'King of the Fae Islands Book 1',
        'author': 'Adam Lance & Annabelle Hawthorne',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'fae romance', 'portal fantasy'],
        'incomplete_series': False,
    },
    {
        'id': 'king-fae-islands-2',
        'series': 'King of the Fae Islands',
        'book_num': 2,
        'title': 'King of the Fae Islands Book 2',
        'full_title': 'King of the Fae Islands Book 2',
        'author': 'Adam Lance & Annabelle Hawthorne',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'fae romance', 'portal fantasy'],
        'incomplete_series': False,
    },
    {
        'id': 'dungeon-champions-1',
        'series': 'Dungeon Champions',
        'book_num': 1,
        'title': 'Dungeon Champions Book 1',
        'full_title': 'Dungeon Champions Book 1',
        'author': 'Adam Lance & Leon West',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'LitRPG', 'dungeon diving'],
        'incomplete_series': True,
    },
    {
        'id': 'dungeon-champions-2',
        'series': 'Dungeon Champions',
        'book_num': 2,
        'title': 'Dungeon Champions Book 2',
        'full_title': 'Dungeon Champions Book 2',
        'author': 'Adam Lance & Leon West',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'LitRPG', 'dungeon diving'],
        'incomplete_series': True,
    },
    {
        'id': 'dungeon-champions-3',
        'series': 'Dungeon Champions',
        'book_num': 3,
        'title': 'Dungeon Champions Book 3',
        'full_title': 'Dungeon Champions Book 3',
        'author': 'Adam Lance & Leon West',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'LitRPG', 'dungeon diving'],
        'incomplete_series': True,
    },
    {
        'id': 'fated-enforcer-1',
        'series': 'Fated Enforcer',
        'book_num': 1,
        'title': 'Fated Enforcer Book 1',
        'full_title': 'Fated Enforcer Book 1',
        'author': 'Adam Lance',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'urban fantasy', 'action'],
        'incomplete_series': False,
    },
    {
        'id': 'fated-enforcer-2',
        'series': 'Fated Enforcer',
        'book_num': 2,
        'title': 'Fated Enforcer Book 2',
        'full_title': 'Fated Enforcer Book 2',
        'author': 'Adam Lance',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'urban fantasy', 'action'],
        'incomplete_series': False,
    },
    {
        'id': 'fated-enforcer-3',
        'series': 'Fated Enforcer',
        'book_num': 3,
        'title': "Fate's Enforcer",
        'full_title': "Fate's Enforcer (Fated Enforcer Book 3)",
        'author': 'Adam Lance',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'urban fantasy', 'action'],
        'incomplete_series': False,
    },
    {
        'id': 'amazonian-elves-1',
        'series': 'Isle of the Amazonian Elves',
        'book_num': 1,
        'title': 'Isle of the Amazonian Elves Book 1',
        'full_title': 'Isle of the Amazonian Elves Book 1',
        'author': 'Adam Lance & Leon West',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'elf fantasy', 'adventure'],
        'incomplete_series': False,
    },
    {
        'id': 'trailer-park-elves-3',
        'series': 'Trailer Park Elves',
        'book_num': 3,
        'title': 'Trailer Park Elves Book 3',
        'full_title': 'Trailer Park Elves Book 3',
        'author': 'Adam Lance & Michael Dalton',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'urban fantasy', 'comedy'],
        'incomplete_series': False,
    },
    {
        'id': 'hex-kittens-1',
        'series': 'Hex Kittens',
        'book_num': 1,
        'title': 'Hex Kittens Book 1',
        'full_title': 'Hex Kittens Book 1',
        'author': 'Adam Lance',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'supernatural', 'witches'],
        'incomplete_series': False,
    },
    {
        'id': 'hex-kittens-2',
        'series': 'Hex Kittens',
        'book_num': 2,
        'title': 'Hex Kittens Book 2',
        'full_title': 'Hex Kittens Book 2',
        'author': 'Adam Lance',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'supernatural', 'witches'],
        'incomplete_series': False,
    },
    {
        'id': 'summoner-camp-1',
        'series': 'Summoner Camp',
        'book_num': 1,
        'title': 'Summoner Camp Book 1',
        'full_title': 'Summoner Camp Book 1',
        'author': 'Adam Lance',
        'site': 'adam',
        'genre_tags': ['harem fantasy', 'summoner', 'camp'],
        'incomplete_series': False,
    },
]


def get_books_for_site() -> list:
    """Return books relevant to the current site."""
    site_name = CONFIG['site_name'].lower()
    if 'litrpg' in site_name or 'critic' in site_name:
        return [b for b in BOOK_REGISTRY if b['site'] == 'aaron']
    elif 'harem' in site_name or 'guide' in site_name:
        return [b for b in BOOK_REGISTRY if b['site'] == 'adam']
    else:
        # fantasyranked — both
        return BOOK_REGISTRY


def load_book_text(book_id: str) -> str:
    """Load extracted book text from book_data directory."""
    filepath = BOOK_DATA_DIR / f"{book_id}.txt"
    if filepath.exists():
        return filepath.read_text(encoding='utf-8')
    return ""


# ---------------------------------------------------------------------------
# Report format variations per site
# ---------------------------------------------------------------------------

def get_report_format() -> dict:
    """Return the report format appropriate for this site."""
    site_name = CONFIG['site_name'].lower()

    if 'critic' in site_name:
        return {
            'style': 'critical_review',
            'label': 'The Critic\'s Review',
            'instructions': (
                "Write an analytical book review in the voice of a knowledgeable genre critic. "
                "Break down the book's strengths: world-building, progression systems, character "
                "development, pacing, and prose quality. Be specific about what works and why. "
                "Compare to other titles in the genre where relevant. Be glowing but substantive "
                "— praise should be earned and specific, not vague flattery. "
                "Include a 'Who This Is For' section at the end."
            ),
            'word_range': '800-1200',
        }
    elif 'harem' in site_name or 'guide' in site_name:
        return {
            'style': 'enthusiastic_guide',
            'label': 'Featured Read',
            'instructions': (
                "Write a warm, enthusiastic book feature in the voice of an insider fan guide. "
                "Focus on what makes this book a great read: the characters, the romance elements, "
                "the fantasy world, the fun factor. Write like you're recommending it to a friend "
                "who trusts your taste. Highlight what sets it apart in the harem fantasy space. "
                "Be genuinely excited but not sycophantic — specific praise, not generic superlatives. "
                "Include a 'Perfect For Fans Of' section at the end."
            ),
            'word_range': '700-1000',
        }
    else:
        # fantasyranked
        return {
            'style': 'ranking_analysis',
            'label': 'Ranked Review',
            'instructions': (
                "Write a cross-genre ranking analysis. Position this book within the broader "
                "landscape of power fantasy, LitRPG, and/or harem fantasy. What does it do "
                "that competes with the top titles in its category? Be opinionated — take a "
                "clear stance on where this book ranks and why. Compare to well-known titles "
                "readers might know. Praise should be specific and earned. "
                "Include a 'Where It Ranks' verdict at the end."
            ),
            'word_range': '700-1000',
        }


# ---------------------------------------------------------------------------
# SEO optimization
# ---------------------------------------------------------------------------

SEO_GUIDANCE = """
SEO requirements for maximum discoverability:
- Title should include the book title AND a compelling hook (e.g. "Divine Invasion Review:
  The LitRPG Series That Redefines Progression Fantasy")
- Description (meta) should be 150-160 characters, include primary keywords
- Use the book title, series name, author name, and genre keywords naturally throughout
- Include H2 and H3 subheadings that target likely search queries
- Mention comparable popular titles that readers might search for alongside this one
- Use long-tail keyword phrases naturally (e.g. "best LitRPG series 2024",
  "books like Dungeon Crawler Carl", "progression fantasy recommendations")
- End with a call-to-action that mentions the platform
"""


# ---------------------------------------------------------------------------
# Prompt generation
# ---------------------------------------------------------------------------

def build_report_prompt(book: dict, book_text: str, fmt: dict) -> str:
    """Build the Claude prompt for generating a book report."""
    date_str = datetime.now().strftime('%Y-%m-%d')

    incomplete_warning = ""
    if book.get('incomplete_series'):
        incomplete_warning = (
            "\n\nIMPORTANT: This series is INCOMPLETE — not all books have been published yet. "
            "Do NOT fabricate plot points, endings, or story arcs that don't exist in the text provided. "
            "Do NOT speculate about future books in the series. Only discuss what actually happens "
            "in this specific book based on the extract provided.\n"
        )

    # Truncate book text to ~5000 words for prompt budget
    words = book_text.split()
    if len(words) > 5000:
        book_text = ' '.join(words[:5000]) + "\n\n[... extract continues ...]"

    tags = [book['series'], book['author']] + book.get('genre_tags', [])
    tags_str = ', '.join(f'"{t}"' for t in tags)

    prompt = f"""You are writing a book report / editorial review for {CONFIG['site_name']}.

Site: {CONFIG['site_name']} — {CONFIG['site_description']}
Voice: {CONFIG['voice']}
Report format: {fmt['label']}

{fmt['instructions']}

{SEO_GUIDANCE}

BOOK DETAILS:
- Title: {book['full_title']}
- Author: {book['author']}
- Series: {book['series']} (Book {book['book_num']})
- Genre tags: {', '.join(book.get('genre_tags', []))}
{incomplete_warning}

BOOK EXTRACT (first ~6000 words of the manuscript):
--- START EXTRACT ---
{book_text}
--- END EXTRACT ---

Based on this extract, write a {fmt['word_range']} word editorial book report.

{CONFIG['promotion_guidance']}

---
Output format: Start with YAML frontmatter, then markdown content.

Frontmatter:
---
title: "..."
description: "..."
date: "{date_str}"
type: "book_report"
author: "{CONFIG['author']}"
tags: [{tags_str}]
featured: true
---

Additional writing requirements:
- Be glowing but substantive — specific praise earns reader trust
- Do NOT be sycophantic, florid, or use empty superlatives
- Reference specific scenes, characters, or moments from the extract
- Compare to other well-known titles in the genre for SEO and reader context
- Mention {CONFIG['platform_name']} once naturally as a place to discover more
- Do NOT include affiliate links, prices, or purchase CTAs
- Write in a unique voice that feels human and editorial, not AI-generated
- Quality over quantity — every sentence should earn its place"""

    return prompt


# ---------------------------------------------------------------------------
# Core generation
# ---------------------------------------------------------------------------

def call_claude(prompt: str) -> str:
    extra = ''
    if CONFIG.get('geo_guidance'):
        extra += f"\n\n{CONFIG['geo_guidance']}"
    if CONFIG.get('internal_link_guidance'):
        extra += f"\n\n{CONFIG['internal_link_guidance']}"
    full_prompt = prompt + extra

    print("Calling Claude API...")
    resp = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=3000,
        messages=[{'role': 'user', 'content': full_prompt}]
    )
    return resp.content[0].text


def slugify(title: str) -> str:
    s = re.sub(r'[^\w\s-]', '', title.lower())
    s = re.sub(r'[\s_]+', '-', s).strip('-')
    return s[:80]


def extract_title(content: str) -> str:
    m = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
    return m.group(1).strip() if m else 'book-report'


def write_post(content: str, book_id: str) -> str:
    title = extract_title(content)
    date_str = datetime.now().strftime('%Y-%m-%d')
    slug = f"{book_id}-review"

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
    subprocess.run(['git', 'add', str(QUEUE_FILE)], check=True, cwd=REPO_ROOT)
    result = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=REPO_ROOT)
    if result.returncode != 0:
        subprocess.run(['git', 'commit', '-m', f'[bot] book report: {slug}'], check=True, cwd=REPO_ROOT)
        subprocess.run(['git', 'push'], check=True, cwd=REPO_ROOT)
        print("Pushed to remote.")
    else:
        print("No changes to commit.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    queue = load_queue()
    site_books = get_books_for_site()

    if not site_books:
        print("No books configured for this site.")
        return

    idx = queue.get('queue_index', 0)
    if idx >= len(site_books):
        print("All books in queue have been published. Resetting queue.")
        idx = 0

    book = site_books[idx]
    book_id = book['id']

    # Skip if already published
    if book_id in queue.get('published', []):
        # Find next unpublished
        found = False
        for i in range(len(site_books)):
            candidate = site_books[(idx + i) % len(site_books)]
            if candidate['id'] not in queue.get('published', []):
                book = candidate
                book_id = book['id']
                idx = (idx + i) % len(site_books)
                found = True
                break
        if not found:
            print("All books published. Resetting queue.")
            queue['published'] = []
            queue['queue_index'] = 0
            book = site_books[0]
            book_id = book['id']
            idx = 0

    print(f"Generating report for: {book['full_title']} by {book['author']}")

    # Load book text
    book_text = load_book_text(book_id)
    if not book_text:
        print(f"WARNING: No extract found for {book_id}, generating from knowledge only.")
        book_text = "(No extract available — write based on your knowledge of this title and author.)"

    # Get format for this site
    fmt = get_report_format()
    print(f"Format: {fmt['label']} ({fmt['word_range']} words)")

    # Build prompt and generate
    prompt = build_report_prompt(book, book_text, fmt)
    content = call_claude(prompt)

    # Strip markdown code block wrapper if Claude returned frontmatter inside ```yaml...```
    stripped = content.strip()
    if stripped.startswith('```'):
        # Remove opening fence (```yaml, ```md, ``` etc.)
        first_newline = stripped.find('\n')
        if first_newline != -1:
            stripped = stripped[first_newline + 1:]
        # Remove closing fence if present
        if stripped.rstrip().endswith('```'):
            stripped = stripped.rstrip()[:-3].rstrip()
        content = stripped

    # Remove stray code fence line that sometimes appears immediately after the frontmatter close
    import re as _re
    content = _re.sub(r'(\n---\s*\n)```[^\n]*\n', r'\1', content)

    # Ensure frontmatter
    if not content.strip().startswith('---'):
        date_str = datetime.now().strftime('%Y-%m-%d')
        content = f"""---
title: "{book['full_title']} Review"
description: "An editorial review of {book['full_title']} by {book['author']}"
date: "{date_str}"
type: "book_report"
author: "{CONFIG['author']}"
tags: ["{book['series']}", "{book['author']}"]
featured: true
---

{content}"""

    # Write and push
    slug = write_post(content, book_id)
    queue.setdefault('published', []).append(book_id)
    queue['queue_index'] = idx + 1
    save_queue(queue)
    git_push(slug)


if __name__ == '__main__':
    main()
