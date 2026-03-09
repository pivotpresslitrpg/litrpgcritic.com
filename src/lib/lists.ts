export interface FAQ {
  q: string;
  a: string;
}

export interface ListConfig {
  title: string;
  description: string;
  intro: string;
  genre?: string;
  sort: 'top_rated' | 'featured';
  limit: number;
  faq?: FAQ[];
}

export const listConfig: Record<string, ListConfig> = {
  'best-litrpg-books': {
    title: 'The 60 Best LitRPG Books of All Time',
    description: 'Our definitive ranked list of the greatest LitRPG series and standalone novels, ranked by community ratings and editorial review.',
    intro: `LitRPG started as a niche corner of Russian web fiction in the early 2010s, then exploded into one of the fastest-growing categories on Amazon and Audible. The genre's core appeal is deceptively simple: characters in worlds where the rules of video games — stats, levels, skills, and experience points — are literal, physical reality. But the best LitRPG is never just about numbers going up.

The series that define the genre use their game systems as a lens for exploring power, identity, strategy, and the oldest kind of storytelling: a protagonist becoming something more than they were. The stats are the scaffolding. The story is what the scaffolding holds up.

This list covers the full breadth of LitRPG and progression fantasy — from genre-defining classics that established the conventions every new author works against, to modern series that have pushed what the genre can be. The genre's current flagships: Dungeon Crawler Carl (Matt Dinniman), He Who Fights With Monsters (Jason Cheyne), Defiance of the Fall (J.F. Brink), The Primal Hunter (Zogarth), and Cradle (Will Wight) for pure progression fantasy. Aaron Renfroe's Apocalypse Breaker and The Resonance Cycle represent the genre's more character-driven side. Rankings draw on community ratings from LitRPGTools.com, where thousands of readers have rated and reviewed these titles, combined with editorial judgment about craft, influence, and long-term staying power. A book that the community has returned to for five years beats a buzzy new release every time.`,
    genre: 'LitRPG',
    sort: 'top_rated',
    limit: 60,
    faq: [
      {
        q: 'What is LitRPG?',
        a: 'LitRPG (Literary Role-Playing Game) is a fiction genre in which characters inhabit worlds governed by game-like systems — experience points, skill trees, character stats, and level-ups that are physically real within the story. It originated in Russian web fiction, grew through platforms like Royal Road and Wattpad, and has become one of the strongest-selling categories on Amazon and Audible.',
      },
      {
        q: 'What is the best LitRPG book to start with?',
        a: 'Dungeon Crawler Carl by Matt Dinniman is the genre\'s most accessible entry point for new readers — darkly funny, relentlessly paced, and structurally inventive. For epic scope, the Cradle series (Will Wight) or He Who Fights With Monsters (Jason Cheyne) are excellent. For system apocalypse with strong character work, Apocalypse Breaker by Aaron Renfroe is a fast, punchy starting point. Defiance of the Fall (J.F. Brink) and The Primal Hunter (Zogarth) are go-tos for readers who want long, immersive series with high reread value.',
      },
      {
        q: 'What is the difference between LitRPG and progression fantasy?',
        a: 'LitRPG uses explicit game mechanics — visible stat screens, level-up notifications, experience point totals displayed in the text. Progression fantasy uses the same underlying structure (a character grows systematically stronger) but may not show game-style text boxes. The Cradle series by Will Wight is the canonical example of progression fantasy that omits explicit stats while keeping all the structural appeal.',
      },
      {
        q: 'Are most LitRPG books part of ongoing series?',
        a: 'Yes — most LitRPG titles are multi-book series, some running to a dozen or more entries. If you prefer binge-reading complete stories without waiting for the next installment, see our list of Best Completed LitRPG Series.',
      },
    ],
  },

  'best-dungeon-core': {
    title: 'The Best Dungeon Core Books (Ranked)',
    description: 'The top dungeon core and dungeon builder LitRPG novels, ranked by our community of readers.',
    intro: `Dungeon core is the sub-genre where you become the dungeon. You're not the hero fighting through traps — you're the intelligence designing them, managing monsters, and evolving your labyrinth to survive the adventurers who keep coming to loot you. It's a power-fantasy subgenre with a peculiar twist: you root for the thing that would normally be the obstacle.

The appeal cuts several ways. There's the city-builder satisfaction of designing increasingly elaborate systems. There's the arms-race tension of reading what the adventurers do and rethinking your defenses. And there's an unusual narrative empathy — these books make you genuinely care about a dungeon's survival in a way that feels stranger and more satisfying than it has any right to.

The sub-genre was largely pioneered by Dungeon Born (Dakota Krout) and has developed distinct conventions: core crystals, experience from kills, floor themes, boss monsters, and a dungeon's gradual awakening into something with goals and personality. The best entries build on those conventions and then push past them.`,
    genre: 'Dungeon Core',
    sort: 'top_rated',
    limit: 30,
    faq: [
      {
        q: 'What is a dungeon core book?',
        a: 'A dungeon core novel tells the story from the perspective of a dungeon — usually a magical core or crystal intelligence that grows by designing traps, cultivating monsters, and consuming the adventurers who explore it. The genre inverts traditional fantasy: you play as the boss, not the hero.',
      },
      {
        q: 'Which dungeon core book should I read first?',
        a: 'Dungeon Born by Dakota Krout is where the modern sub-genre began and where most readers start. It established the conventions — core crystals, floor design, experience from kills — that nearly every dungeon core book since has used as its foundation.',
      },
      {
        q: 'Is dungeon core a sub-genre of LitRPG?',
        a: 'Yes. Dungeon core books typically use LitRPG game mechanics — the dungeon has stats, levels, and abilities it upgrades over time. They are a distinct sub-genre with their own community and conventions, but firmly part of the broader LitRPG and GameLit ecosystem.',
      },
      {
        q: 'Are dungeon core books suitable for readers new to LitRPG?',
        a: 'Dungeon core is actually an excellent entry point for readers new to LitRPG, because the perspective is unusual and doesn\'t require prior familiarity with game mechanics. The dungeon "learning the rules" as it wakes up often serves as natural explanation for how the system works.',
      },
    ],
  },

  'best-progression-fantasy': {
    title: 'The Best Progression Fantasy Series',
    description: 'From Cradle to He Who Fights With Monsters — the definitive ranked list of progression fantasy.',
    intro: `Progression fantasy is LitRPG's literary cousin — a genre built around a character's systematic growth toward power, but without necessarily displaying the game-style stat screens and notifications of core LitRPG. Where LitRPG leans into the video game metaphor explicitly, progression fantasy takes the underlying appeal — the steady arc of getting stronger, mastering systems, climbing hierarchies of power — and lets it breathe as pure story.

The genre's defining text is Will Wight's Cradle series, which stripped the GameLit aesthetic back to its narrative bones and produced something that reads as much like epic fantasy as anything gamified. He Who Fights With Monsters (Jason Cheyne) brought the genre to a massive mainstream audience. The genre has since expanded in every direction.

What the best progression fantasy does that lesser entries don't: it makes the progression feel earned. A character whose numbers go up isn't interesting. A character who develops genuine mastery — who understands why they were weak and exactly how they've become strong — is. The series on this list are the ones that get that distinction right.`,
    genre: 'Progression Fantasy',
    sort: 'top_rated',
    limit: 40,
    faq: [
      {
        q: 'What is progression fantasy?',
        a: 'Progression fantasy is a genre in which a character systematically grows in power — developing skills, mastering systems, and climbing hierarchies — over the course of a series. It shares DNA with LitRPG but may omit explicit game-style notifications and stat screens. The Cradle series by Will Wight is the genre\'s defining example.',
      },
      {
        q: 'What is the best place to start with progression fantasy?',
        a: 'Unsouled (Cradle Book 1) by Will Wight is the standard starting point — the series is complete, has an enormous following, and the early books are short enough to read in an afternoon. He Who Fights With Monsters has broader mainstream appeal for readers coming from epic fantasy. Defiance of the Fall (J.F. Brink) and The Primal Hunter (Zogarth) are excellent for readers who want long-running, high-stakes multiverse progression. For something character-driven with a faster pace, Aaron Renfroe\'s The Resonance Cycle is a strong pick.',
      },
      {
        q: 'How does progression fantasy differ from LitRPG?',
        a: 'LitRPG uses explicit game mechanics — visible stat screens, level-up notifications, experience points as displayed numbers. Progression fantasy uses the same structural arc (a character gets systematically stronger) without necessarily showing game UI. In practice, many popular series blend both approaches.',
      },
      {
        q: 'Are there completed progression fantasy series worth reading?',
        a: 'Yes — the Cradle series (Will Wight) is complete at 12 books and widely considered the genre\'s best finished run. Lots of progression fantasy series are still ongoing, so see our Best Completed LitRPG Series list if you prefer to binge without waits.',
      },
    ],
  },

  'best-completed-litrpg': {
    title: 'Best Completed LitRPG Series (No Waiting)',
    description: 'Fully finished LitRPG series you can binge start-to-finish, right now.',
    intro: `One of the underrated joys of LitRPG and progression fantasy is that these genres reward long-haul commitment. The best series pay off properly — arcs that seemed disconnected in book two resolve in book eight, the character growth compounds across hundreds of hours of reading, and endings actually land. But all of that requires the author to finish the thing.

This list is for readers who've been burned too many times. No waiting for the next installment. No series abandoned mid-arc. No "the author hasn't updated in two years." Every series here is complete — you can pick it up today and read start-to-finish without a single cliffhanger into an unwritten sequel.

We've limited this list to multi-book series that reached a genuine narrative conclusion. Not "no new book in three years" — finished stories with confirmed endings. LitRPG readers have been burned by abandoned series enough that this distinction is worth being precise about.`,
    genre: 'LitRPG',
    sort: 'top_rated',
    limit: 25,
    faq: [
      {
        q: 'What counts as a "completed" series on this list?',
        a: 'Every series here has reached a narrative conclusion — the author finished the story with a final book that resolves the main arc. We do not include series that simply went quiet or have had no new entry in several years without an explicit conclusion.',
      },
      {
        q: 'What is the best completed LitRPG series to binge?',
        a: 'The Cradle series (Will Wight, 12 books) is consistently ranked as the genre\'s gold standard and is fully complete. Dungeon Crawler Carl (Matt Dinniman) is also complete and may be the most purely entertaining binge read in the genre — start with Book 1 and plan to lose a week. He Who Fights With Monsters (Jason Cheyne) is complete at 12 books with a massive following. Tao Wong\'s The System Apocalypse (12 books) is the definitive completed system apocalypse series.',
      },
      {
        q: 'How many books are typically in a completed LitRPG series?',
        a: 'LitRPG series vary widely — from trilogies to twelve-book runs. Most well-regarded complete series fall between 4 and 12 books. We note series length for each entry on this list.',
      },
    ],
  },

  'best-litrpg-audiobooks': {
    title: 'The Best LitRPG Audiobooks',
    description: 'Top LitRPG titles on Audible, selected for both story quality and narration.',
    intro: `LitRPG and audiobooks are a natural fit. The genre's in-head narration — status screen popups, internal tactical thinking, the cadence of a level-up — translates exceptionally well to audio. The best LitRPG audiobooks use their narrators the way great film composers use a score: the right voice makes the stats feel dramatic, the combat feel visceral, and the moments of leveling-up genuinely satisfying.

Audible has become one of the primary markets for the genre, and the production budgets reflect it — many of the top LitRPG series now feature professional narrator and production combinations that rival anything in traditional audiobook publishing. Jeff Hays reading Dungeon Crawler Carl is a benchmark not just for LitRPG audio but for the medium.

This list selects for both story quality and narration quality. A great LitRPG with a flat narrator doesn't make the cut. A mediocre story with an extraordinary narrator doesn't make it either. These are the titles genuinely worth your Audible credits.`,
    genre: 'LitRPG',
    sort: 'top_rated',
    limit: 30,
    faq: [
      {
        q: 'What makes a great LitRPG audiobook?',
        a: 'Great LitRPG audiobooks balance story quality with narration — the right narrator makes system notifications feel dramatic rather than mechanical, and maintains energy through long leveling sequences. The Dungeon Crawler Carl audiobooks (read by Jeff Hays) are the gold standard for what this can sound like at its best.',
      },
      {
        q: 'Who are the best LitRPG audiobook narrators?',
        a: 'Jeff Hays (Dungeon Crawler Carl), Travis Baldree (The Wandering Inn), and Andrea Parsneau are consistently praised across the community. For progression fantasy, Nick Podehl (Cradle) is widely considered the genre\'s best narrator. Highlight your preferred narrator in your audiobook platform\'s search to find more of their work.',
      },
      {
        q: 'Are all the books on this list available on Audible?',
        a: 'Every title on this list has an Audible edition. Some popular LitRPG series also have editions through Libro.fm or other audiobook platforms. All Amazon affiliate links will route to the listing that includes the Audible edition where available.',
      },
    ],
  },

  'best-gamelit': {
    title: 'The Best GameLit Books',
    description: 'The best GameLit novels — game mechanics and stats without necessarily being inside a game.',
    intro: `GameLit is the broader category that contains LitRPG, and the distinction matters. LitRPG is defined by explicit, foregrounded game mechanics — you see the stat screen, the experience notification, the level-up pop-up as text on the page. GameLit encompasses all fiction where game-like mechanics are a meaningful part of the world, including books where the systems operate more in the background, where stats are real but not always displayed, or where game logic shapes the world without being constantly announced.

The best GameLit tends to be the fiction where the mechanics genuinely serve the story rather than existing as the point. Skill descriptions are interesting when they reveal character or create tactical stakes. They're padding when they're just padding.

This list captures the best GameLit across its range — books that use game mechanics creatively, in ways that feel integrated rather than bolted on, whether those mechanics are explicit LitRPG or something more subtle.`,
    genre: 'GameLit',
    sort: 'top_rated',
    limit: 25,
    faq: [
      {
        q: 'What is GameLit?',
        a: 'GameLit is fiction that incorporates game mechanics — levels, skills, stats, inventory systems — as a meaningful element of the story world. LitRPG is a sub-genre of GameLit in which those mechanics are highly explicit, displayed to the reader as they are to the character. GameLit is the broader umbrella.',
      },
      {
        q: 'Is LitRPG a sub-genre of GameLit?',
        a: 'Yes. All LitRPG is GameLit, but not all GameLit is LitRPG. LitRPG requires explicit, visible game mechanics — stat screens, level notifications, experience points in the text. If you removed those displays and the genre still worked, it\'s probably GameLit rather than LitRPG proper.',
      },
      {
        q: 'What is the best GameLit book for someone new to the genre?',
        a: 'He Who Fights With Monsters (Jason Cheyne) is an ideal entry point — it has fully explicit LitRPG game mechanics with visible stats, but its broader epic fantasy scope and accessible prose make it welcoming to readers outside the core LitRPG community.',
      },
    ],
  },

  'books-like-dungeon-crawler-carl': {
    title: 'Best Books Like Dungeon Crawler Carl',
    description: "If you loved Dungeon Crawler Carl, these LitRPG books share its humor, grit, and relentless forward momentum.",
    intro: `Dungeon Crawler Carl — Matt Dinniman's series about a man, his princess-named cat, and the most lethal televised death sport in galactic history — has become the defining "why is this so good" moment in LitRPG. It's darkly funny, brutally difficult, structurally inventive, and emotionally honest in ways that catch readers completely off guard. The books are long and they are still the most talked-about series in the genre.

If you've finished what's available and you're looking for what to read next, you're probably looking for some combination of: a sarcastic or deeply human protagonist, a system that wants to kill you rather than accommodate you, humor that doesn't undercut genuine stakes, and forward momentum that never stops. Possibly also a scene that makes you unexpectedly emotional about a cat.

Nothing on this list is exactly like Dungeon Crawler Carl. These are the books most likely to scratch a similar itch — each for a different reason. Top picks: He Who Fights With Monsters (Jason Cheyne) for the culture-clash humor and momentum; Defiance of the Fall (J.F. Brink) for relentless multiverse survival; The Primal Hunter (Zogarth) for immersive office-worker-turned-powerhouse progression; and Apocalypse Breaker by Aaron Renfroe for fast-paced system apocalypse with real character stakes.`,
    genre: 'LitRPG',
    sort: 'top_rated',
    limit: 20,
    faq: [
      {
        q: 'What makes Dungeon Crawler Carl different from other LitRPG?',
        a: 'DCC\'s combination of sharp dark humor, satirical commentary (the dungeon is literally a televised galactic death sport), genuine emotional depth, and Dinniman\'s inventive system design sets it apart from most of the genre. Most LitRPG takes its premise more seriously. DCC takes its stakes seriously while being extremely funny about the setting.',
      },
      {
        q: 'Is Dungeon Crawler Carl a complete series?',
        a: 'The series is ongoing — Matt Dinniman continues to release new books. Given the length of individual volumes and the author\'s publication pace, there is always another entry to anticipate.',
      },
      {
        q: 'Where do I start with Dungeon Crawler Carl?',
        a: 'Book 1: Dungeon Crawler Carl. The series must be read in order — each book builds directly and substantially on the previous one. Do not start mid-series.',
      },
      {
        q: 'Is there LitRPG with similar humor to Dungeon Crawler Carl?',
        a: 'Apocalypse Breaker by Aaron Renfroe and the He Who Fights With Monsters series both have humor as a core element alongside serious stakes. For pure comedic LitRPG, Dungeon Crawler Carl remains the high-water mark — but these are the closest neighbors.',
      },
    ],
  },

  'best-litrpg-romance': {
    title: 'Best LitRPG Books with Romance',
    description: 'LitRPG stories where the romance subplot is more than a footnote.',
    intro: `LitRPG has a reputation as a genre primarily interested in combat optimization and power scaling. That reputation is partially deserved and mostly reductive. A significant portion of the genre's readership — and a growing one — wants the stats and the relationship dynamics: the tension of a will-they-won't-they playing out across three hundred dungeon floors, the satisfaction of a relationship that develops naturally alongside a character's growing strength.

LitRPG with romance is not a compromise or a dilution of either genre. The game mechanics actually create interesting romantic dynamics that straight romance fiction can't access: competing for party spots, power imbalances that shift as characters level, and the particular intimacy of fighting alongside someone in genuine danger, with life and death measured in hit points.

This list collects the best LitRPG and progression fantasy where the romantic subplot is developed, satisfying, and earns its place in the story — without becoming so dominant that readers primarily here for the LitRPG content feel shortchanged.`,
    genre: 'LitRPG',
    sort: 'top_rated',
    limit: 20,
    faq: [
      {
        q: 'Is LitRPG romance a separate sub-genre?',
        a: 'Not formally, but there is a substantial readership for LitRPG fiction with significant romance content. Some books on this list are primarily LitRPG with strong romance elements; others lean harder toward romance with game mechanics as the setting. We\'ve noted the balance in each description.',
      },
      {
        q: 'Do LitRPG romance books have guaranteed happy endings?',
        a: 'Most LitRPG romance has positive relationship arcs, but the genre does not follow the same structural conventions as traditional romance novels — which require a happily-ever-after or happy-for-now ending. In ongoing series, romantic arcs may still be developing.',
      },
      {
        q: 'Is there LitRPG with harem elements?',
        a: 'Yes — some LitRPG titles incorporate harem elements, particularly in men\'s adventure fiction. For that specific sub-niche, see also our companion site HaremLitGuide.com, which covers harem fantasy and men\'s romance LitRPG in depth.',
      },
    ],
  },
};
