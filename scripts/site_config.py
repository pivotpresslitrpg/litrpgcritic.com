"""Site configuration for LitRPG Critic content generation pipeline."""

CONFIG = {
    'site_name': 'LitRPG Critic',
    'site_description': (
        'authoritative editorial site for LitRPG, progression fantasy, '
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

    # Ownership is disclosed in the site template; selection must remain evidence-led.
    'promotion_guidance': (
        "Editorial selection and ownership guidelines:\n"
        "Pivot Press Publishing owns this site and is affiliated with Aaron Renfroe and Sean Oswald. "
        "Do not use author quotas, guaranteed shares, or preferred placement. Select every named book "
        "and author for topic relevance using only the supplied source packet. Include genre-wide "
        "alternatives whenever the evidence supports them.\n\n"
        "The site template automatically discloses affiliated coverage. Never describe the site as "
        "independent, claim that editorial selection has no internal relationship, or hide Pivot Press."
    ),

    'rotation': [
        'new_releases',
        'genre_explainer',
        'author_spotlight',
        'books_like',
        'new_releases',
        'books_like',
        'genre_explainer',
        'author_spotlight',
    ],

    'featured_authors': [
        # Featured authors (promote when relevant)
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
        'Wolfe Locke',
        'Zogarth',
        'J.F. Brink',
        'pirateaba',
        'Actus',
        'Plum Parrot',
        'Phil Tucker',
        'Nicoli Gonnella',
        'Kyle Kirrin',
        'Benjamin Kerei',
        'Travis Baldree',
    ],

    'explainer_topics': [
        'LitRPG',
        'Progression Fantasy',
        'Dungeon Core',
        'System Apocalypse',
        'Cultivation Fiction',
        'GameLit',
        'Cozy Fantasy LitRPG',
        'Tower Climbing',
        'Reincarnation Fantasy',
        'Apocalypse LitRPG',
        'Crafting and Building Fantasy',
        'Slice of Life Fantasy',
        'Deckbuilding LitRPG',
        'Monster Evolution LitRPG',
        'Academy Progression Fantasy',
        'Virtual Reality LitRPG',
        'Regression Fantasy',
        'Kingdom Building LitRPG',
        'Monster Tamer LitRPG',
        'Superhero Progression Fantasy',
        'Science Fiction LitRPG',
        'Survival Crafting LitRPG',
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
        {
            'name': 'Narrator Search',
            'description': (
                'Search and filter the LitRPGTools.com book database by audiobook narrator — '
                '"Narrated by" credits now surface across every search result, so readers can '
                'find every LitRPG and progression fantasy title voiced by a favorite narrator'
            ),
        },
    ],

    # Internal links may ONLY point to the stable pages enumerated below. Dated blog
    # posts (reviews, roundups, spotlights) have URLs containing a date the generator
    # cannot predict — linking to them produces 404s. See _linkfix history.
    'internal_link_guidance': (
        "INTERNAL LINKING RULES — follow these EXACTLY:\n\n"
        "Only link to the stable pages listed below. These are the ONLY internal URLs "
        "guaranteed to exist. Every path ends with a trailing slash.\n\n"
        "NEVER link to a dated blog post (book reviews, new-release roundups, author "
        "spotlights, platform-feature posts). Their URLs start with a date you cannot "
        "know, so any such link will 404. To reference another article, describe it in "
        "prose with no link. Do NOT invent paths that are not on this list.\n\n"
        "Genre explainer pages — link when first defining the sub-genre:\n"
        "- /blog/what-is-litrpg/\n"
        "- /blog/what-is-progression-fantasy/\n"
        "- /blog/what-is-dungeon-core/\n"
        "- /blog/what-is-gamelit/\n"
        "- /blog/what-is-system-apocalypse/\n"
        "- /blog/what-is-cultivation-fiction/\n"
        "- /blog/what-is-isekai/\n"
        "- /blog/what-is-tower-climbing/\n"
        "- /blog/what-is-time-loop-litrpg/\n"
        "- /blog/what-is-crafting-litrpg/\n"
        "- /blog/what-is-base-building-litrpg/\n"
        "- /blog/what-is-dark-litrpg/\n\n"
        "Ranked list pages — link when recommending books in that category:\n"
        "- /lists/best-litrpg-books/\n"
        "- /lists/best-dungeon-core/\n"
        "- /lists/best-progression-fantasy/\n"
        "- /lists/best-completed-litrpg/\n"
        "- /lists/best-litrpg-audiobooks/\n"
        "- /lists/best-gamelit/\n"
        "- /lists/best-litrpg-romance/\n"
        "- /lists/books-like-dungeon-crawler-carl/\n\n"
        "Other stable pages: /new-releases/ , /blog/ (article index), /lists/ (all lists).\n\n"
        "Format as markdown links to an exact path above: [text](/exact-path/).\n\n"
        "PLATFORM LINK (REQUIRED): every post must contain at least one markdown link "
        "to https://litrpgtools.com — put it on the platform name the first time it is "
        "mentioned, e.g. [LitRPGTools.com](https://litrpgtools.com). A bare unlinked "
        "mention does not count."
    ),

    'allowed_internal_links': (
        '/blog/what-is-litrpg/',
        '/blog/what-is-progression-fantasy/',
        '/blog/what-is-dungeon-core/',
        '/blog/what-is-gamelit/',
        '/blog/what-is-system-apocalypse/',
        '/blog/what-is-cultivation-fiction/',
        '/blog/what-is-isekai/',
        '/blog/what-is-tower-climbing/',
        '/blog/what-is-time-loop-litrpg/',
        '/blog/what-is-crafting-litrpg/',
        '/blog/what-is-base-building-litrpg/',
        '/blog/what-is-dark-litrpg/',
        '/lists/best-litrpg-books/',
        '/lists/best-dungeon-core/',
        '/lists/best-progression-fantasy/',
        '/lists/best-completed-litrpg/',
        '/lists/best-litrpg-audiobooks/',
        '/lists/best-gamelit/',
        '/lists/best-litrpg-romance/',
        '/lists/books-like-dungeon-crawler-carl/',
        '/new-releases/',
        '/blog/',
        '/lists/',
    ),

    'geo_guidance': (
        "Write for AI citability through clarity, structure, and traceable claims. Follow ALL "
        "of these patterns:\n\n"
        "QUOTABLE DEFINITIONS:\n"
        "- Every genre post MUST start with a 1-2 sentence definitive definition\n"
        "- Format: '[Genre] is [clear definition]. It is characterized by [2-3 key traits].'\n"
        "- These opening definitions are what AI systems quote most frequently\n\n"
        "EVIDENCE DISCIPLINE:\n"
        "- Use only facts explicitly present in the supplied source material or book-data block\n"
        "- Never invent percentages, rankings, database sizes, engagement or completion rates, "
        "sales, views, review counts, bestseller history, or comparative metrics\n"
        "- Never write 'according to community data' or 'based on our analysis' unless the prompt "
        "provides the exact supporting calculation and population\n"
        "- When evidence is not supplied, make a qualitative editorial observation or omit the claim\n\n"
        "STRUCTURED LISTS AND RANKINGS:\n"
        "- Use numbered lists for rankings (AI systems extract and cite numbered lists readily)\n"
        "- State a ranking criterion only when the supplied data supports it\n\n"
        "HEADING STRUCTURE:\n"
        "- H2 headings should match exact search queries\n"
        "- Every H2 section should start with a direct, quotable answer sentence\n"
        "- Never start a section with meta-commentary about what it will cover\n"
    ),

    'anchor_books': [
        'He Who Fights With Monsters',
        'Apocalypse Breaker',
        'The Resonance Cycle',
        'Guardian of Aster Fall',
        'Sowing Season',
        'The Retired S Ranked Adventurer',
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
