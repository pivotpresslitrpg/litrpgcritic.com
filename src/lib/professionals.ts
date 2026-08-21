// ---------------------------------------------------------------------------
// Industry-professional program — facts and calls to action.
//
// Every factual claim here is sourced from the live application flow on the
// platform. Do not add numbers that the platform does not publish itself.
//
// Voice note: this site is the LitRPG Critic — analytical, plain, willing to
// state a problem before offering the mechanism that solves it. The CTA copy
// below is written in that register and is deliberately NOT shared with the
// sister sites, which address the same program in their own voices.
// ---------------------------------------------------------------------------

import { PLATFORM_BASE, PLATFORM_NAME, withUtm } from './api';

export { PLATFORM_NAME };

const PATHS = {
  directory: '/industry-professionals',
  hub: '/join',
  apply: '/apply/industry-professional',
  guide: '/guides/industry-professionals',
} as const;

export type ProfessionalPath = keyof typeof PATHS;

/** Attributed deep link into the platform's professional surfaces. */
export function professionalUrl(path: ProfessionalPath, content: string): string {
  return withUtm(`${PLATFORM_BASE}${PATHS[path]}`, content);
}

// --- Roles -----------------------------------------------------------------

export interface ProfessionalRole {
  name: string;
  /** What this person is hired to do, in the author's terms. */
  work: string;
  /** The concrete entry requirement, or null when the portfolio is the bar. */
  requirement: string | null;
  applyContent: string;
}

export const ROLES: ProfessionalRole[] = [
  {
    name: 'Editor',
    work: 'Developmental, line, copy, or proof passes on manuscripts where prose, progression, and a stat system all have to hold at once.',
    requirement: null,
    applyContent: 'role-editor',
  },
  {
    name: 'Narrator',
    work: 'ACX and Findaway audiobook work, quoted per finished hour, with demo reels and LitRPG pronunciation comfort on file.',
    requirement: null,
    applyContent: 'role-narrator',
  },
  {
    name: 'Visual artist',
    work: 'Cover design, illustration, character art, maps, and typography — priced per tier, always including a commercial publishing license.',
    requirement: 'A hosted gallery of 5–10 images, an AI-use classification on every image, and a recorded rights attestation.',
    applyContent: 'role-artist',
  },
  {
    name: 'Alpha / beta reader',
    work: 'Structured pre-publication feedback per 50,000 words, with declared turnaround and delivery format. Alpha reading is an opt-in extra.',
    requirement: 'Confirmation that you have read at least 25 LitRPG or progression fantasy books.',
    applyContent: 'role-reader',
  },
  {
    name: 'Other specialist',
    work: 'Formatters, cartographers, publicists, sensitivity readers, and audio engineers working in the genre.',
    requirement: null,
    applyContent: 'role-other',
  },
];

/** Rate guidance the platform publishes to its own applicants. */
export const BETA_RATE_NOTE =
  'Beta readers set their own rates. The platform’s applicant guidance cites an industry norm of roughly $250–500 USD per 50,000 words for a full pass, with rush turnaround typically 1.5–2× standard.';

export const REVIEW_NOTE =
  'Applications are free, save as you go, and are reviewed by a human in about 5–7 days. Profiles are public only after approval.';

// --- Homepage band -----------------------------------------------------------
// Separate copy from CTA.community on purpose: the homepage speaks to a mixed
// audience arriving cold, not to a reader who just finished a related article.
export const BAND = {
  eyebrow: 'Industry professionals',
  heading: 'LitRPG is made by people you can now actually find',
  body:
    'Editors who understand progression systems, narrators who can carry a 300,000-word cast, artists who know what a dungeon core cover has to promise, and beta readers who have read 25+ books in the genre — listed publicly with rates and availability.',
  roleLabel: 'Apply as',
};

// --- Calls to action -------------------------------------------------------

export type CtaMode = 'hire' | 'earn' | 'create' | 'community';

export interface CtaAction {
  label: string;
  path: ProfessionalPath;
  content: string;
}

export interface CtaVariant {
  eyebrow: string;
  heading: string;
  body: string;
  primary: CtaAction;
  secondary: CtaAction;
}

export const CTA: Record<CtaMode, CtaVariant> = {
  hire: {
    eyebrow: 'For authors',
    heading: 'Hiring for a LitRPG book is its own problem',
    body:
      'An editor who can hold prose, pacing, and a progression system in their head simultaneously is not a general-purpose editor. The professional directory on ' +
      PLATFORM_NAME +
      ' lists people who chose this genre on purpose, filterable by role, current availability, and subgenre.',
    primary: { label: 'Search the directory', path: 'directory', content: 'cta-hire-directory' },
    secondary: { label: 'How vetting works', path: 'guide', content: 'cta-hire-guide' },
  },

  earn: {
    eyebrow: 'For readers',
    heading: 'The genre will pay for expertise you built for free',
    body:
      'Beta reading is the paid version of what serious genre readers already do in comment threads: catch the broken power curve, the contradicted stat block, the arc that quietly disappears. The qualifying bar is 25 books read in LitRPG or progression fantasy.',
    primary: { label: 'Apply as an alpha or beta reader', path: 'apply', content: 'cta-earn-apply' },
    secondary: { label: 'See who is already listed', path: 'directory', content: 'cta-earn-directory' },
  },

  create: {
    eyebrow: 'For visual artists',
    heading: 'Commissions from people who actually read the genre',
    body:
      'Every portfolio image carries an AI-use classification and a recorded rights attestation, and listed prices must include a commercial publishing license. In a market saturated with generated images, that disclosure is what makes verified human craft legible — and chargeable.',
    primary: { label: 'Apply as a visual artist', path: 'apply', content: 'cta-create-apply' },
    secondary: { label: 'Browse the artist roster', path: 'directory', content: 'cta-create-directory' },
  },

  community: {
    eyebrow: 'Industry professionals',
    heading: 'The people who make these books are findable now',
    body:
      'Editors, narrators, visual artists, and alpha/beta readers who work in LitRPG list themselves publicly, with rates, availability, and genre comfort on the profile. Authors search it for free. Professionals apply for free.',
    primary: { label: 'Explore the directory', path: 'directory', content: 'cta-community-directory' },
    secondary: { label: 'Apply to be listed', path: 'hub', content: 'cta-community-apply' },
  },
};

const ARTIST_HINTS = ['cover artist', 'visual artist', 'book cover', 'cover commission', 'artist opportunities', 'fantasy art job'];
const READER_HINTS = ['get paid to read', 'reader opportunities', 'alpha reader', 'paid reading'];
const AUTHOR_HINTS = ['beta reader', 'industry professional', 'writing advice', 'author resources', 'editors', 'narrators'];

function matches(haystack: string, hints: string[]): boolean {
  return hints.some((h) => haystack.includes(h));
}

/**
 * Pick the CTA register that fits a post. Artist and reader intents are checked
 * before the broader author intent because artist/reader posts also carry the
 * generic publishing tags.
 */
export function ctaModeFor(tags: string[] = [], title = ''): CtaMode {
  const hay = [...tags, title].join(' ').toLowerCase();
  if (matches(hay, ARTIST_HINTS)) return 'create';
  if (matches(hay, READER_HINTS)) return 'earn';
  if (matches(hay, AUTHOR_HINTS)) return 'hire';
  return 'community';
}
