// ---------------------------------------------------------------------------
// Network identity.
//
// The five public properties plus the parent publisher form one entity cluster.
// Every property must describe that cluster IDENTICALLY: search and answer
// engines treat `sameAs` as a merge instruction, and conflicting or partial
// declarations lower their confidence that the properties are one operator.
// If you edit this table, mirror the edit in the other two blog repos.
// ---------------------------------------------------------------------------

export interface NetworkProperty {
  name: string;
  url: string;
  kind: 'editorial' | 'platform' | 'publisher';
  /** Footer-length summary. Keep factual — this is disclosure copy, not sales copy. */
  blurb: string;
}

export const PUBLISHER: NetworkProperty = {
  name: 'Pivot Press Publishing',
  url: 'https://pivotpresspublishing.com',
  kind: 'publisher',
  blurb: 'Parent publisher of the editorial sites and reader platforms below.',
};

export const NETWORK: NetworkProperty[] = [
  {
    name: 'LitRPG Critic',
    url: 'https://litrpgcritic.com',
    kind: 'editorial',
    blurb: 'Reviews and ranked lists for LitRPG and progression fantasy.',
  },
  {
    name: 'Fantasy Ranked',
    url: 'https://fantasyranked.com',
    kind: 'editorial',
    blurb: 'Cross-genre power fantasy rankings and comparisons.',
  },
  {
    name: 'HaremLit Guide',
    url: 'https://haremlitguide.com',
    kind: 'editorial',
    blurb: 'Reader guides for harem fantasy and men’s romance.',
  },
  {
    name: 'LitRPGTools.com',
    url: 'https://litrpgtools.com',
    kind: 'platform',
    blurb: 'Book database, tracking, and the LitRPG industry-professional directory.',
  },
  {
    name: 'Harem-Lit.com',
    url: 'https://harem-lit.com',
    kind: 'platform',
    blurb: 'Book database, tracking, and the HaremLit industry-professional directory.',
  },
];

/** This site's canonical URL — used to filter itself out of sister listings. */
export const SELF_URL = 'https://litrpgcritic.com';

/** Sister editorial blogs (never includes this site). */
export const SISTER_SITES = NETWORK.filter(
  (p) => p.kind === 'editorial' && p.url !== SELF_URL,
);

/** Reader platforms in the network. */
export const PLATFORMS = NETWORK.filter((p) => p.kind === 'platform');

/**
 * Every other property in the cluster, for schema.org `sameAs`.
 * Identical set on all five properties (each minus itself) by design.
 */
export const SAME_AS: string[] = [
  ...NETWORK.filter((p) => p.url !== SELF_URL).map((p) => p.url),
  PUBLISHER.url,
];

export const PUBLISHER_ORG = {
  '@type': 'Organization',
  name: PUBLISHER.name,
  url: PUBLISHER.url,
} as const;

/**
 * The shared Organization node. Emit this once per page (homepage and the
 * evergreen hubs) so every property asserts the same cluster membership.
 */
export function organizationSchema(opts: {
  name: string;
  description: string;
  knowsAbout: string[];
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: opts.name,
    url: SELF_URL,
    description: opts.description,
    parentOrganization: PUBLISHER_ORG,
    sameAs: SAME_AS,
    knowsAbout: opts.knowsAbout,
  };
}
