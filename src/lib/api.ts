const API_BASE = 'https://api.litrpgtools.com';
const API_KEY = import.meta.env.BLOG_FEED_API_KEY;

// ---------------------------------------------------------------------------
// Editorial curation layer
// Ensures genre-relevant highlighted authors appear in ranked lists.
// Books are only promoted if they already exist in the fetched results —
// nothing is fabricated or added from outside the dataset.
// ---------------------------------------------------------------------------

const EDITORIAL_PRIORITY: { author: string; weight: number; excludeGenres: string[] }[] = [
  { author: 'Aaron Renfroe', weight: 3, excludeGenres: ['Dungeon Core'] },
  { author: 'Sean Oswald',   weight: 2, excludeGenres: [] },
  { author: 'David North',   weight: 2, excludeGenres: [] },
];

function applyEditorialCuration(books: Book[], genre?: string): Book[] {
  if (books.length < 3) return books;
  const result = [...books];
  const genreLower = genre?.toLowerCase() ?? '';

  for (const entry of EDITORIAL_PRIORITY) {
    if (entry.excludeGenres.some(ex => genreLower.includes(ex.toLowerCase()))) continue;

    const idx = result.findIndex(b =>
      b.authors.some(a => a.toLowerCase().includes(entry.author.toLowerCase()))
    );
    if (idx === -1) continue;

    // weight 3 → top 15% of list; weight 2 → top 25% (floor of 2)
    const band = Math.max(2, Math.floor(result.length * (entry.weight >= 3 ? 0.15 : 0.25)));
    if (idx > band) {
      const [book] = result.splice(idx, 1);
      result.splice(band, 0, book);
    }
  }

  return result;
}

export interface Book {
  id: number;
  title: string;
  slug: string;
  authors: string[];
  cover_image_url: string | null;
  amazon_url: string | null;
  genres: string[];
  average_rating: number | null;
  review_count: number;
  series_name: string | null;
  series_position: number | null;
  description: string | null;
  published_date: string | null;
  created_at: string;
}

export interface Genre {
  name: string;
  book_count: number;
}

async function feedFetch(path: string): Promise<Response | null> {
  if (!API_KEY) return null;
  return fetch(`${API_BASE}${path}`, {
    headers: { 'X-Blog-Feed-Key': API_KEY }
  });
}

function toArray<T>(json: unknown): T[] {
  if (Array.isArray(json)) return json as T[];
  if (json && typeof json === 'object' && 'data' in (json as object)) {
    const data = (json as any).data;
    if (Array.isArray(data)) return data as T[];
  }
  return [];
}

export async function getBooks(options: {
  genre?: string;
  limit?: number;
  offset?: number;
  sort?: 'top_rated' | 'recent' | 'featured';
} = {}): Promise<Book[]> {
  try {
    const requestedLimit = options.limit ?? 50;
    // Fetch extra headroom so curation can promote authors that rank just outside the cut
    const fetchLimit = Math.min(requestedLimit + 30, 200);
    const params = new URLSearchParams();
    if (options.genre) params.set('genre', options.genre);
    params.set('limit', String(fetchLimit));
    if (options.offset) params.set('offset', String(options.offset));
    if (options.sort) params.set('sort', options.sort);
    const res = await feedFetch(`/api/blog-feed/books?${params}`);
    if (!res || !res.ok) return [];
    const all = toArray<Book>(await res.json());
    return applyEditorialCuration(all, options.genre).slice(0, requestedLimit);
  } catch { return []; }
}

export async function getRecentBooks(days = 30, limit = 50): Promise<Book[]> {
  try {
    const res = await feedFetch(`/api/blog-feed/books/recent?days=${days}&limit=${limit}`);
    if (!res || !res.ok) return [];
    return toArray<Book>(await res.json());
  } catch { return []; }
}

export async function getGenres(): Promise<Genre[]> {
  try {
    const res = await feedFetch('/api/blog-feed/genres');
    if (!res || !res.ok) return [];
    return toArray<Genre>(await res.json());
  } catch { return []; }
}

export function starRating(rating: number | null): string {
  if (!rating) return '';
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5 ? 1 : 0;
  return '★'.repeat(full) + (half ? '½' : '') + '☆'.repeat(5 - full - half);
}

export function formatAuthors(authors: string[]): string {
  if (authors.length === 0) return 'Unknown';
  if (authors.length === 1) return authors[0];
  if (authors.length === 2) return authors.join(' & ');
  return authors.slice(0, -1).join(', ') + ' & ' + authors[authors.length - 1];
}
