export interface ListConfig {
  title: string;
  description: string;
  intro: string;
  genre?: string;
  sort: 'top_rated' | 'featured';
  limit: number;
}

export const listConfig: Record<string, ListConfig> = {
  'best-litrpg-books': {
    title: 'The 60 Best LitRPG Books of All Time',
    description: 'Our definitive ranked list of the greatest LitRPG series and standalone novels, ranked by community ratings and editorial review.',
    intro: 'LitRPG has grown from a niche web fiction genre to one of the most active publishing categories on Amazon. These are the books that define it — from genre-founding classics to modern masterworks.',
    genre: 'LitRPG',
    sort: 'top_rated',
    limit: 60,
  },
  'best-dungeon-core': {
    title: 'The Best Dungeon Core Books (Ranked)',
    description: 'The top dungeon core and dungeon builder LitRPG novels, ranked by our community of readers.',
    intro: 'Dungeon core books put you in the mind of the dungeon itself — building traps, managing monsters, and fending off adventurers. These are the best the sub-genre has to offer.',
    genre: 'Dungeon Core',
    sort: 'top_rated',
    limit: 30,
  },
  'best-progression-fantasy': {
    title: 'The Best Progression Fantasy Series',
    description: 'From Cradle to He Who Fights With Monsters — the definitive ranked list of progression fantasy.',
    intro: 'Progression fantasy strips LitRPG to its core: a character grows stronger, develops abilities, and climbs toward mastery. These are the series readers return to again and again.',
    genre: 'Progression Fantasy',
    sort: 'top_rated',
    limit: 40,
  },
  'best-completed-litrpg': {
    title: 'Best Completed LitRPG Series (No Waiting)',
    description: 'Fully finished LitRPG series you can binge start-to-finish, right now.',
    intro: "One of the best feelings in LitRPG: picking up a complete series and reading straight through. No cliffhangers, no multi-year waits. Here are the best completed runs in the genre.",
    genre: 'LitRPG',
    sort: 'top_rated',
    limit: 25,
  },
  'best-litrpg-audiobooks': {
    title: 'The Best LitRPG Audiobooks',
    description: 'Top LitRPG titles on Audible, selected for both story quality and narration.',
    intro: "LitRPG is one of the best-performing genres on Audible. The right narrator can make a system screen genuinely thrilling. These are the titles worth your Audible credits.",
    genre: 'LitRPG',
    sort: 'top_rated',
    limit: 30,
  },
  'best-gamelit': {
    title: 'The Best GameLit Books',
    description: 'The best GameLit novels — game mechanics and stats without necessarily being inside a game.',
    intro: "GameLit is LitRPG's close cousin: game-like mechanics (stats, levels, skills) in any setting. These are the standout titles that use those elements to great effect.",
    genre: 'GameLit',
    sort: 'top_rated',
    limit: 25,
  },
  'books-like-dungeon-crawler-carl': {
    title: 'Best Books Like Dungeon Crawler Carl',
    description: "If you loved Dungeon Crawler Carl, these LitRPG books share its humor, grit, and relentless forward momentum.",
    intro: "Matt Dinniman's Dungeon Crawler Carl is one of the most beloved series in LitRPG — darkly funny, brutally difficult, and impossible to put down. Here are the books most likely to scratch the same itch.",
    genre: 'LitRPG',
    sort: 'top_rated',
    limit: 20,
  },
  'best-litrpg-romance': {
    title: 'Best LitRPG Books with Romance',
    description: 'LitRPG stories where the romance subplot is more than a footnote.',
    intro: "Not every LitRPG reader wants pure grind — some want the stats AND the love story. These books deliver both without sacrificing either.",
    genre: 'LitRPG',
    sort: 'top_rated',
    limit: 20,
  },
};
