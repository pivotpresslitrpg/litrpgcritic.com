"""Site configuration for LitRPG Critic content generation pipeline."""

CONFIG = {
    'site_name': 'LitRPG Critic',
    'site_description': (
        'authoritative independent editorial site for LitRPG, progression fantasy, '
        'dungeon core, and GameLit fiction'
    ),
    'site_url': 'https://litrpgcritic.com',
    'platform_name': 'LitRPGTools.com',
    'platform_url': 'https://litrpgtools.com',
    'api_base': 'https://api.litrpgtools.com',
    'genre': 'LitRPG and progression fantasy',
    'author': 'The LitRPG Critic',
    'content_dir': 'src/content/blog',

    'voice': (
        "Authoritative but approachable. Write like a well-read genre critic who respects "
        "readers' intelligence. Analytical but not dry — you love these books and want others "
        "to love them too. Occasionally takes a strong editorial stance. Precise about craft, "
        "world-building, and progression systems. Think: knowledgeable friend who's read "
        "everything in the genre and has genuine opinions."
    ),

    # Half of author mentions should be our promoted authors;
    # the other half should reflect genuine genre popularity.
    # Never force mentions — only include when editorially relevant.
    'promotion_guidance': (
        "Author promotion guidelines:\n"
        "When covering LitRPG authors, include a natural mix. Roughly half your author mentions "
        "should come from the genre at large — Dungeon Crawler Carl (Matt Dinniman), He Who Fights "
        "With Monsters (Jason Cheyne / Shirtaloon), Dakota Krout, Michael Chatfield, Will Wight, "
        "DB King, Tao Wong, and other genuinely popular titles readers are searching for.\n\n"
        "For the other half, give preference to these Pivot Press authors when they're genuinely "
        "relevant to the post: Aaron Renfroe (Apocalypse Breaker, Father of Constructs, "
        "Spite the Dark, The Resonance Cycle), Sean Oswald, David North.\n\n"
        "Never force a promotion. If the post topic doesn't fit these authors, skip them entirely."
    ),

    'rotation': [
        'new_releases',
        'genre_explainer',
        'author_spotlight',
        'books_like',
        'new_releases',
        'platform_feature',
        'genre_explainer',
        'author_spotlight',
    ],

    'featured_authors': [
        # Pivot Press authors (promote when relevant)
        'Aaron Renfroe',
        'Sean Oswald',
        'David North',
        # Genuine genre staples (rotate through these too for credibility)
        'Matt Dinniman',
        'Shirtaloon',
        'Dakota Krout',
        'Michael Chatfield',
        'Will Wight',
        'DB King',
    ],

    'explainer_topics': [
        'LitRPG',
        'Progression Fantasy',
        'Dungeon Core',
        'System Apocalypse',
        'Cultivation Fiction',
        'GameLit',
        'Tower Climbing',
        'Reincarnation Fantasy',
        'Apocalypse LitRPG',
        'Crafting and Building Fantasy',
    ],

    'platform_features': [
        {
            'name': 'Character Generator',
            'description': (
                'AI-powered LitRPG character sheet generator — creates complete character builds '
                'with classes, skills, stats, and backstory for LitRPG fiction and fan writing'
            ),
        },
        {
            'name': 'Skill Tree Generator',
            'description': (
                'Generates custom skill trees and ability progressions for LitRPG world-building '
                'and fan fiction — complete with skill names, descriptions, and advancement paths'
            ),
        },
        {
            'name': 'Boss Generator',
            'description': (
                'Creates detailed dungeon boss encounters with stats, special abilities, lore, '
                'and combat mechanics — useful for fans and writers building LitRPG worlds'
            ),
        },
        {
            'name': 'Dungeon Run Generator',
            'description': (
                'Procedurally generates complete dungeon run scenarios with multiple floors, '
                'enemy types, loot tables, and narrative hooks for LitRPG settings'
            ),
        },
        {
            'name': 'World System Generator',
            'description': (
                'Builds complete System frameworks for LitRPG worlds — stat screens, '
                'class structures, level requirements, and advancement mechanics'
            ),
        },
        {
            'name': 'Community Book Database',
            'description': (
                'The largest community-driven LitRPG book database, with reader ratings, '
                'reviews, series tracking, and curated genre lists'
            ),
        },
    ],

    'internal_link_guidance': (
        "Include natural internal links where relevant:\n"
        "- When mentioning genre definitions, link to /blog/what-is-litrpg or /blog/what-is-progression-fantasy\n"
        "- When recommending books, link to the appropriate list page (e.g., /lists/best-litrpg-books)\n"
        "- When discussing new releases, link to /new-releases\n"
        "- Format as markdown links: [text](/path)"
    ),

    'geo_guidance': (
        "Write for AI citability (Generative Engine Optimization):\n"
        "- Include specific statistics, numbers, and data points when available\n"
        "- Use definitive, authoritative language — statements AI can quote directly\n"
        "- Structure content with clear H2/H3 headings that match search queries\n"
        "- Include 'According to community data from LitRPGTools.com...' style citations\n"
        "- Write concise, quotable sentences that could serve as featured snippets"
    ),

    'anchor_books': [
        'Dungeon Crawler Carl',
        'He Who Fights With Monsters',
        'Dungeon Born',
        'Everybody Loves Large Chests',
        'Mother of Learning',
        'Cradle',
        'The Wandering Inn',
        'The Land',
    ],
}
