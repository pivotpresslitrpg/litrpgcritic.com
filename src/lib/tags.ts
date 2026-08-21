// ---------------------------------------------------------------------------
// Tag hubs.
//
// The corpus carries a rich tag vocabulary that previously had no landing
// pages, so topically related posts were only reachable through a dated index.
// Hubs turn that vocabulary into internal links and give each recurring topic
// a rankable page.
//
// MIN_POSTS keeps one-off tags from generating thin pages: a hub with a single
// post is crawl budget spent on nothing. Tags below the threshold still appear
// in frontmatter, they just do not get a page or a chip.
// ---------------------------------------------------------------------------

export const MIN_POSTS = 3;

export interface TagEntry {
  /** Display form, exactly as authored in frontmatter. */
  name: string;
  slug: string;
  count: number;
}

export function tagSlug(tag: string): string {
  return tag
    .toLowerCase()
    .replace(/&/g, ' and ')
    .replace(/['’.]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

interface TaggedPost {
  data: { tags?: string[]; date: string };
}

/** Tags that qualify for a hub page, most-used first. */
export function buildTagIndex<T extends TaggedPost>(posts: T[]): TagEntry[] {
  const bySlug = new Map<string, { name: string; count: number }>();

  for (const post of posts) {
    for (const raw of post.data.tags ?? []) {
      const name = raw.trim();
      if (!name) continue;
      const slug = tagSlug(name);
      if (!slug) continue;
      const existing = bySlug.get(slug);
      if (existing) existing.count += 1;
      else bySlug.set(slug, { name, count: 1 });
    }
  }

  return [...bySlug.entries()]
    .filter(([, v]) => v.count >= MIN_POSTS)
    .map(([slug, v]) => ({ slug, name: v.name, count: v.count }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));
}

/** Posts carrying a given tag slug, newest first. */
export function postsForTag<T extends TaggedPost>(posts: T[], slug: string): T[] {
  return posts
    .filter((p) => (p.data.tags ?? []).some((t) => tagSlug(t) === slug))
    .sort((a, b) => b.data.date.localeCompare(a.data.date));
}
