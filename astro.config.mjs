// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://litrpgcritic.com',
  trailingSlash: 'always',
  vite: {
    plugins: [tailwindcss()]
  },
  integrations: [
    sitemap({
      serialize(item) {
        const buildDate = new Date().toISOString();
        // Try to extract date from blog URL pattern (e.g. /blog/2025-01-15-some-title/)
        const dateMatch = item.url.match(/\/blog\/(\d{4}-\d{2}-\d{2})-/);

        if (item.url === 'https://litrpgcritic.com/') {
          item.priority = 1.0;
          item.changefreq = 'daily';
          item.lastmod = buildDate;
        } else if (item.url.includes('/lists/')) {
          item.priority = 0.9;
          item.changefreq = 'weekly';
          item.lastmod = buildDate;
        } else if (item.url.includes('/blog/what-is-')) {
          item.priority = 0.95;
          item.changefreq = 'monthly';
          item.lastmod = dateMatch ? new Date(dateMatch[1]).toISOString() : buildDate;
        } else if (item.url.includes('/blog/')) {
          item.priority = 0.8;
          item.changefreq = 'monthly';
          item.lastmod = dateMatch ? new Date(dateMatch[1]).toISOString() : buildDate;
        } else if (item.url.includes('/new-releases')) {
          item.priority = 0.9;
          item.changefreq = 'daily';
          item.lastmod = buildDate;
        } else {
          item.priority = 0.3;
          item.changefreq = 'yearly';
          item.lastmod = buildDate;
        }
        return item;
      }
    })
  ]
});
