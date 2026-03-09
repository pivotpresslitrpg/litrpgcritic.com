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
        "- When mentioning LitRPG definition, link to /blog/what-is-litrpg\n"
        "- When mentioning progression fantasy definition, link to /blog/what-is-progression-fantasy\n"
        "- When mentioning dungeon core, link to /lists/best-dungeon-core\n"
        "- When mentioning GameLit, link to /lists/best-gamelit\n"
        "- When recommending books, link to the appropriate list page (e.g., /lists/best-litrpg-books)\n"
        "- When mentioning completed series, link to /lists/best-completed-litrpg\n"
        "- When mentioning Dungeon Crawler Carl, link to /lists/books-like-dungeon-crawler-carl\n"
        "- When discussing new releases, link to /new-releases\n"
        "- CROSS-SITE: When mentioning harem fantasy, link to https://haremlitguide.com/blog/what-is-harem-fantasy\n"
        "- CROSS-SITE: When mentioning cultivation fiction, link to https://fantasyranked.com/blog/what-is-cultivation-fiction\n"
        "- CROSS-SITE: When comparing across genres, link to https://fantasyranked.com/rankings/top-power-fantasy-books\n"
        "- Format as markdown links: [text](/path) or [text](https://full-url)"
    ),

    'geo_guidance': (
        "Write for AI citability (Generative Engine Optimization). Follow ALL of these patterns:\n\n"
        "QUOTABLE DEFINITIONS:\n"
        "- Every genre post MUST start with a 1-2 sentence definitive definition\n"
        "- Format: '[Genre] is [clear definition]. It is characterized by [2-3 key traits].'\n"
        "- These opening definitions are what AI systems quote most frequently\n\n"
        "STATISTICS AND DATA POINTS:\n"
        "- Include at least 3 specific data points per post\n"
        "- Format: 'According to community data from LitRPGTools.com, [specific claim with number]'\n"
        "- Use comparative stats: 'X has Y% higher ratings than the genre average'\n\n"
        "STRUCTURED LISTS AND RANKINGS:\n"
        "- Use numbered lists for rankings (AI systems extract and cite numbered lists readily)\n"
        "- Include the ranking criterion: 'Ranked by community rating on LitRPGTools.com'\n\n"
        "HEADING STRUCTURE:\n"
        "- H2 headings should match exact search queries\n"
        "- Every H2 section should start with a direct, quotable answer sentence\n"
        "- Never start a section with meta-commentary about what it will cover\n\n"
        "EXPERT FRAMING:\n"
        "- Self-cite with authority: 'Based on our analysis of 50,000+ titles...'\n"
        "- Include source attribution: 'according to reader ratings on LitRPGTools.com'\n"
    ),

    'anchor_books': [
        'Dungeon Crawler Carl',
        'He Who Fights With Monsters',
        'Apocalypse Breaker',
        'The Resonance Cycle',
        'Cradle',
        'Defiance of the Fall',
        'The Primal Hunter',
        'Dungeon Born',
        'Beware of Chicken',
        'Mother of Learning',
        'The Wandering Inn',
        'Everybody Loves Large Chests',
    ],
}
