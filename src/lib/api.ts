const API_BASE = 'https://api.litrpgtools.com';
const API_KEY = import.meta.env.BLOG_FEED_API_KEY;

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

export async function getBooks(options: {
  genre?: string;
  limit?: number;
  offset?: number;
  sort?: 'top_rated' | 'recent' | 'featured';
} = {}): Promise<Book[]> {
  const params = new URLSearchParams();
  if (options.genre) params.set('genre', options.genre);
  if (options.limit) params.set('limit', String(options.limit));
  if (options.offset) params.set('offset', String(options.offset));
  if (options.sort) params.set('sort', options.sort);
  const res = await feedFetch(`/api/blog-feed/books?${params}`);
  if (!res || !res.ok) return [];
  return res.json();
}

export async function getRecentBooks(days = 30, limit = 50): Promise<Book[]> {
  const res = await feedFetch(`/api/blog-feed/books/recent?days=${days}&limit=${limit}`);
  if (!res || !res.ok) return [];
  return res.json();
}

export async function getGenres(): Promise<Genre[]> {
  const res = await feedFetch('/api/blog-feed/genres');
  if (!res || !res.ok) return [];
  return res.json();
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
