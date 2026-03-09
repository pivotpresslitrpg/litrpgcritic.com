#!/usr/bin/env python3
"""One-shot pillar page generator for SEO-optimized 'What is...' content.

Run manually: python scripts/generate_pillar.py
Requires ANTHROPIC_API_KEY environment variable.
"""

import os
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

import anthropic

from site_config import CONFIG

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
CONTENT_DIR = REPO_ROOT / CONFIG['content_dir']

client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

PILLAR_TOPICS = [
    {
        'title': 'What is LitRPG? The Complete Guide to LitRPG Fiction',
        'slug': 'what-is-litrpg',
        'description': 'What is LitRPG? A complete guide to the LitRPG genre — its origins, defining features, best books to start with, and why millions of readers love it.',
        'word_count': '3000-3500',
        'focus': 'LitRPG',
        'internal_links': [
            {'url': '/lists/best-litrpg-books', 'text': 'Best LitRPG Books of All Time'},
            {'url': '/lists/best-dungeon-core', 'text': 'Best Dungeon Core Books'},
            {'url': '/lists/best-completed-litrpg', 'text': 'Best Completed LitRPG Series'},
            {'url': '/lists/best-litrpg-audiobooks', 'text': 'Best LitRPG Audiobooks'},
        ],
        'faq_topics': [
            'What does LitRPG stand for?',
            'What is the difference between LitRPG and GameLit?',
            'Where did LitRPG originate?',
            'What is the best LitRPG book for beginners?',
            'Is LitRPG the same as progression fantasy?',
            'Can LitRPG books be read without playing video games?',
        ],
    },
    {
        'title': 'What is Progression Fantasy? The Definitive Guide',
        'slug': 'what-is-progression-fantasy',
        'description': 'What is progression fantasy? A definitive guide to the genre — what makes it different from LitRPG, the best books, and why readers love power scaling stories.',
        'word_count': '2500-3000',
        'focus': 'Progression Fantasy',
        'internal_links': [
            {'url': '/lists/best-progression-fantasy', 'text': 'Best Progression Fantasy Series'},
            {'url': '/lists/best-litrpg-books', 'text': 'Best LitRPG Books'},
            {'url': '/blog', 'text': 'Latest Articles'},
        ],
        'faq_topics': [
            'What is the difference between progression fantasy and LitRPG?',
            'What are the best progression fantasy books?',
            'Is Cradle a progression fantasy?',
            'Does progression fantasy always have a magic system?',
            'Where can I find progression fantasy recommendations?',
        ],
    },
    {
        'title': 'What is Dungeon Core? The Complete Guide to Dungeon Core Fiction',
        'slug': 'what-is-dungeon-core',
        'description': 'What is dungeon core fiction? A complete guide to the subgenre where you ARE the dungeon — origins, key mechanics, best books, and why readers love building trap-filled labyrinths.',
        'word_count': '2000-2500',
        'focus': 'Dungeon Core',
        'internal_links': [
            {'url': '/lists/best-dungeon-core', 'text': 'Best Dungeon Core Books'},
            {'url': '/lists/best-litrpg-books', 'text': 'Best LitRPG Books'},
            {'url': '/blog/what-is-litrpg', 'text': 'What is LitRPG?'},
        ],
        'faq_topics': [
            'What is dungeon core fiction?',
            'What is the difference between dungeon core and dungeon crawler?',
            'What are the best dungeon core books?',
            'Is Dungeon Born the first dungeon core novel?',
            'Where can I find dungeon core recommendations?',
        ],
    },
    {
        'title': 'What is GameLit? How It Differs From LitRPG',
        'slug': 'what-is-gamelit',
        'description': 'What is GameLit? A guide to game-influenced fiction — how it differs from LitRPG, the best GameLit books, and why the distinction matters for readers.',
        'word_count': '2000-2500',
        'focus': 'GameLit',
        'internal_links': [
            {'url': '/lists/best-gamelit', 'text': 'Best GameLit Books'},
            {'url': '/lists/best-litrpg-books', 'text': 'Best LitRPG Books'},
            {'url': '/blog/what-is-litrpg', 'text': 'What is LitRPG?'},
        ],
        'faq_topics': [
            'What is the difference between GameLit and LitRPG?',
            'What are the best GameLit books?',
            'Is Ready Player One a GameLit book?',
            'Does GameLit always have stat screens?',
            'Where can I find GameLit recommendations?',
        ],
    },
]


def generate_pillar(topic: dict) -> str:
    """Generate a pillar page using Claude API."""
    links_text = '\n'.join(
        f"- [{l['text']}]({l['url']})" for l in topic['internal_links']
    )
    faq_text = '\n'.join(f"- {q}" for q in topic['faq_topics'])

    prompt = f"""Write a comprehensive, SEO-optimized pillar page titled "{topic['title']}".

REQUIREMENTS:
- Word count: {topic['word_count']} words
- Genre focus: {topic['focus']}
- Site: {CONFIG['site_name']} ({CONFIG['site_url']})
- Voice: {CONFIG['voice']}

STRUCTURE:
1. Opening paragraph (40-60 words): Write a clear, direct definition optimized for Google's featured snippet. Start with "{topic['focus']} is..." — no preamble.

2. Main sections (use ## H2 headings):
   - Defining Characteristics / Core Elements
   - History and Origins
   - Key Subgenres (if applicable)
   - How It Differs From Related Genres
   - Why Readers Love It
   - 10 Best Books to Start With (numbered list with brief descriptions)
   - Where to Discover More

3. FAQ section: Generate Q&A pairs for these questions:
{faq_text}
Write the FAQ section using ## FAQ heading, then ### for each question with the answer below it.

INTERNAL LINKS — naturally weave these into the content:
{links_text}

IMPORTANT GUIDELINES:
- Include specific statistics and data where possible (e.g., "the LitRPG subreddit has over 100,000 members")
- Use authoritative, definitive language — this is THE guide
- In the "10 Best Books" section, include a mix of undisputed genre classics and Pivot Press titles when relevant
- {CONFIG['promotion_guidance']}
- End the "Where to Discover More" section with a natural mention of {CONFIG['platform_name']} ({CONFIG['platform_url']}) as the go-to resource
- Do NOT include frontmatter — I will add that separately
- Do NOT use the exact title as an H1 — start directly with the opening paragraph
- Write in Markdown format
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=5000,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def extract_faq(content: str) -> list:
    """Extract FAQ Q&A pairs from the generated content."""
    faq = []
    faq_section = re.split(r'##\s+FAQ', content, flags=re.IGNORECASE)
    if len(faq_section) < 2:
        return faq

    faq_text = faq_section[1]
    questions = re.split(r'###\s+', faq_text)
    for q_block in questions[1:]:  # skip text before first ###
        lines = q_block.strip().split('\n', 1)
        if len(lines) == 2:
            question = lines[0].strip().rstrip('?') + '?'
            answer = lines[1].strip()
            # Clean up markdown formatting from answer
            answer = re.sub(r'\n+', ' ', answer).strip()
            if question and answer:
                faq.append({'q': question, 'a': answer})
    return faq


def write_pillar(topic: dict, content: str):
    """Write the pillar page as a markdown file with frontmatter."""
    today = datetime.now().strftime('%Y-%m-%d')
    faq = extract_faq(content)

    frontmatter = {
        'title': topic['title'],
        'description': topic['description'],
        'date': today,
        'type': 'pillar',
        'author': CONFIG['author'],
        'tags': [topic['focus'].lower().replace(' ', '-'), 'guide', 'genre-explainer'],
        'featured': True,
    }
    if faq:
        frontmatter['faq'] = faq

    # Build frontmatter YAML manually for clean output
    fm_lines = ['---']
    fm_lines.append(f'title: "{frontmatter["title"]}"')
    fm_lines.append(f'description: "{frontmatter["description"]}"')
    fm_lines.append(f'date: "{frontmatter["date"]}"')
    fm_lines.append(f'type: "{frontmatter["type"]}"')
    fm_lines.append(f'author: "{frontmatter["author"]}"')
    fm_lines.append(f'tags: {json.dumps(frontmatter["tags"])}')
    fm_lines.append(f'featured: {str(frontmatter["featured"]).lower()}')
    if faq:
        fm_lines.append('faq:')
        for item in faq:
            q_escaped = item['q'].replace('"', '\\"')
            a_escaped = item['a'].replace('"', '\\"')
            fm_lines.append(f'  - q: "{q_escaped}"')
            fm_lines.append(f'    a: "{a_escaped}"')
    fm_lines.append('---')
    fm_lines.append('')

    full_content = '\n'.join(fm_lines) + content

    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = CONTENT_DIR / f"{topic['slug']}.md"
    filepath.write_text(full_content, encoding='utf-8')
    print(f"  Written: {filepath}")
    return filepath


def git_commit_and_push(files: list):
    """Commit and push the generated pillar pages."""
    for f in files:
        subprocess.run(['git', 'add', str(f)], cwd=REPO_ROOT, check=True)

    msg = f"Add pillar pages: {', '.join(t['slug'] for t in PILLAR_TOPICS)}"
    subprocess.run(['git', 'commit', '-m', msg], cwd=REPO_ROOT, check=True)
    subprocess.run(['git', 'push'], cwd=REPO_ROOT, check=True)
    print("Pushed to remote.")


def main():
    print(f"Generating pillar pages for {CONFIG['site_name']}...")
    generated_files = []

    for topic in PILLAR_TOPICS:
        filepath = CONTENT_DIR / f"{topic['slug']}.md"
        if filepath.exists():
            print(f"  Skipping {topic['slug']} (already exists)")
            continue

        print(f"  Generating: {topic['title']}...")
        content = generate_pillar(topic)
        f = write_pillar(topic, content)
        generated_files.append(f)

    if generated_files:
        git_commit_and_push(generated_files)
        print(f"Done! Generated {len(generated_files)} pillar pages.")
    else:
        print("No new pillar pages to generate.")


if __name__ == '__main__':
    main()
