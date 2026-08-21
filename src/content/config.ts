import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.string(),
    // Optional ISO date for a substantive refresh. Drives schema dateModified
    // and the visible "Updated" line; omit for posts that have not changed.
    updated: z.string().optional(),
    type: z.string(),
    author: z.string().default('The LitRPG Critic'),
    tags: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    faq: z.array(z.object({ q: z.string(), a: z.string() })).optional(),
  }),
});

export const collections = { blog };
