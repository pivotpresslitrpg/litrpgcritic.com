import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = (await getCollection('blog'))
    .sort((a, b) => b.data.date.localeCompare(a.data.date));

  return rss({
    title: 'LitRPG Critic',
    description: 'Reviews, ranked lists, and new release coverage for LitRPG and progression fantasy.',
    site: context.site!,
    xmlns: { atom: 'http://www.w3.org/2005/Atom' },
    items: posts.map(post => ({
      title: post.data.title,
      pubDate: new Date(post.data.date + 'T12:00:00'),
      description: post.data.description,
      link: `/blog/${post.id}/`,
    })),
    customData: `<language>en-us</language>
<atom:link href="https://haremlitguide.com/rss.xml" rel="related" type="application/rss+xml" title="HaremLit Guide"/>
<atom:link href="https://fantasyranked.com/rss.xml" rel="related" type="application/rss+xml" title="Fantasy Ranked"/>`,
  });
}
