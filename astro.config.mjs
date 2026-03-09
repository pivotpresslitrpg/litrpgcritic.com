// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://litrpgcritic.com',
  vite: {
    plugins: [tailwindcss()]
  },
  integrations: [
    sitemap({
      serialize(item) {
        if (item.url === 'https://litrpgcritic.com/') {
          item.priority = 1.0;
          item.changefreq = 'daily';
        } else if (item.url.includes('/lists/') || item.url.includes('/reviews/')) {
          item.priority = 0.9;
          item.changefreq = 'weekly';
        } else if (item.url.includes('/blog/')) {
          item.priority = 0.8;
          item.changefreq = 'monthly';
        } else if (item.url.includes('/new-releases')) {
          item.priority = 0.9;
          item.changefreq = 'daily';
        } else {
          item.priority = 0.3;
          item.changefreq = 'yearly';
        }
        return item;
      }
    })
  ]
});
