export const PIVOT_PRESS_NAME = 'Pivot Press Publishing';
export const PIVOT_PRESS_BASE = 'https://pivotpresspublishing.com';

const UTM_SOURCE = 'litrpgcritic';

const PIVOT_PRESS_AUTHORS = [
  'Aaron Renfroe',
  'Sean Oswald',
] as const;

const PIVOT_PRESS_SERIES = [
  'Apocalypse Breaker',
  'Father of Constructs',
  'The Resonance Cycle',
  'Spite the Dark',
] as const;

const AFFILIATION_TERMS = [...PIVOT_PRESS_AUTHORS, ...PIVOT_PRESS_SERIES];

function normalize(value: string): string {
  return ` ${value.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim()} `;
}

export function pivotPressUrl(content: string): string {
  const params = new URLSearchParams({
    utm_source: UTM_SOURCE,
    utm_medium: 'referral',
    utm_campaign: 'publisher-discovery',
    utm_content: content,
  });
  return `${PIVOT_PRESS_BASE}/?${params}`;
}

export function findPivotPressAffiliations(
  values: readonly (string | null | undefined)[],
): string[] {
  const haystack = normalize(values.filter(Boolean).join(' '));
  return AFFILIATION_TERMS.filter((term) => haystack.includes(normalize(term)))
    .map(String);
}

export function hasPivotPressAffiliatedAuthor(authors: readonly string[]): boolean {
  const normalizedAuthors = authors.map(normalize);
  return PIVOT_PRESS_AUTHORS.some((name) => normalizedAuthors.includes(normalize(name)));
}

export function isPivotPressAffiliatedAuthorName(name: string): boolean {
  return hasPivotPressAffiliatedAuthor([name]);
}
