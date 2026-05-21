---
title: "LitRPGTools.com Now Lets Authors Build Their Own Reading Orders — and Shows Them the Data"
description: "Two LitRPGTools.com features shipped that change how readers find canonical reading orders and how authors understand their catalog performance. Here's what the new author Reading Order Builder and dashboard analytics actually do, and what it means for readers."
date: "2026-05-02"
type: "platform_feature"
author: "The LitRPG Critic"
tags: ["LitRPGTools.com", "platform features", "reading order", "author tools", "catalog analytics", "LitRPG", "progression fantasy"]
featured: false
---

The hardest practical problem in [LitRPG](/blog/what-is-litrpg/) isn't finding a series to read — it's figuring out what order to read it in. The genre is full of sprawling, multi-arc projects where the canonical path is non-obvious: side novellas, prequel arcs, anthology contributions, parallel series in the same universe. Reading-order guides have always been a job that mostly fell to fans, then to critics, then eventually filtered into community wikis that may or may not be current.

[LitRPGTools.com](https://litrpgtools.com) just shipped two features that move that responsibility back to where it belongs: with the authors themselves. The new **author Reading Order Builder** lets authors define and maintain canonical reading paths — including for shared universes with multiple parallel arcs. The companion **dashboard analytics** give authors actual catalog traffic data to inform those decisions. Together, they're a meaningful shift in how the platform treats author-side curation.

## Why a Built-in Reading Order Builder Matters

Until recently, reading orders on most book platforms were either implicit (just publication order, which is wrong almost as often as it's right) or maintained by external curators with no live link to the author. That's a fragile system. New books drop, side projects launch, and the reading order goes stale within months.

The new Reading Order Builder solves this by giving each author a tool inside their dashboard that:

1. **Defines the canonical path through their work** — the author decides what order their stuff should be read in, full stop. This is especially important for authors with multi-series universes where the right path depends on intent (story-chronology vs. publication-order vs. accessibility).
2. **Supports lanes for shared universes** — for projects where multiple parallel series tell different threads of the same world, the builder lets authors define each thread as its own lane. Readers can pick which lane to follow first or weave them as they go. That's the natural representation of how readers actually consume a sprawling universe.
3. **Stays live** — the admin layer supports live editing, so when a new book drops, the reading order updates without anyone needing to touch a wiki, refile a fan-maintained spreadsheet, or wait for a content team to notice.
4. **Exposes a public API** — the reading-order data is available through a public endpoint, which means external sites and reading guides can stay in sync with the author-defined source of truth rather than drifting apart.

That last point is the quiet structural win. The historic problem with reading-order guides isn't that they're wrong on day one — it's that they go wrong on day ninety, and there's no automated way to catch the drift. A platform-native, author-maintained, API-exposed canonical order is the first system we've seen in this genre that actually solves the staleness problem.

## What the Author Dashboard Analytics Add

Reading orders are downstream of an even more important question: **what are readers actually doing on your catalog?** The companion feature on the dashboard gives authors a much clearer picture: traffic insights at the catalog level, click patterns by book, and the kind of audience-engagement signals that have historically been opaque to indie LitRPG authors operating outside Amazon's KDP dashboard.

What this looks like in practice for authors:

- **Catalog-level traffic insights** — which books in your bibliography are pulling the most reader attention right now, broken down by entry rather than aggregated.
- **Card-driven click attribution** — for the gamification layer the platform has been building out, authors now see which surfaces are actually driving discovery vs. which are decorative.
- **Audible / format breakdowns** — visibility into which formats readers are converting to. For LitRPG specifically, audiobook conversion is a meaningful tier of revenue and discovery, and authors finally have a clean read on it from the dashboard.

For readers, this is invisible infrastructure. But it's the kind of invisible infrastructure that produces visibly better author decisions over the next year — better-curated reading orders, smarter sequencing of side projects, faster correction of confusing bibliographies. The signal feeds the curation feeds the experience.

## What Changes for Readers Right Now

Three concrete things, in order of how soon you'll feel them:

1. **Author profile pages now surface canonical reading orders.** When you land on an author profile, the path through their work is right there — defined by them, kept current by them. No more digging through sub-Reddits or hoping the wiki was updated this quarter.
2. **Sprawling universes finally have honest representation.** Universes like Aaron Renfroe's [Resonance Cycle](/blog/2026-03-11-resonance-cycle-1-review/) shared world or any other multi-arc project on the platform can present their reading paths the way they actually exist — with parallel lanes, optional side arcs, and recommended-but-not-required ordering — instead of forcing readers into a fake-linear sequence.
3. **External reading-order guides can stay synced.** Because the reading-order data is exposed via public API, sites like the [LitRPG Critic](/) can keep our own [reading order guides](/blog/2026-03-25-dungeon-crawler-carl-reading-order/) tied to the author's source of truth. When the author updates the canonical order, the platform reflects it, and downstream guides can pick it up. The historical problem of reading-order drift gets meaningfully smaller.

## The Bigger Pattern

LitRPGTools.com has been on a steady cadence of platform features that quietly shift the labor of curation from external fans back to the platform itself — the [narrator registry](/blog/2026-04-25-litrpgtools-narrator-registry-search-filter-litrpg-books-by-narrator/) put audiobook search in one place, the [Patreon integration](/blog/2026-04-17-litrpgtools-patreon-integration-link-your-account-unlock-patron-benefits/) tied paid serialization to the public catalog, the [skill tree generator](/blog/2026-04-13-litrpgtools-skill-tree-generator-build-custom-ability-progressions-for-your-worl/) gave worldbuilders a first-party tool, and now the Reading Order Builder + analytics give authors direct curation power over their own catalog presentation.

There's a pattern here worth naming. The platform is steadily reducing the amount of work readers have to do to find the right entry point into a [progression fantasy](/blog/what-is-progression-fantasy) catalog, and steadily reducing the amount of work authors have to do to keep their bibliography readable. Both halves of the user base are getting tools that used to be the responsibility of nobody in particular, which historically meant the tools didn't exist.

That's not a flashy feature drop. It's structural maintenance of the kind of platform LitRPG actually needs.

## Where to Use This Right Now

For readers:

- Visit your favorite author's profile on [LitRPGTools.com](https://litrpgtools.com) and check whether they've published a canonical reading order yet. The early adopters are already there.
- For shared universes with multiple authors, the lane support means you can pick a lane to follow first. Worth experimenting with — different lanes give different first impressions of the same world.

For authors with a presence on the platform:

- Open the dashboard and find the new Reading Order Builder CTA — discoverability is meaningfully better than the previous version. Define the path you'd want a brand-new reader to take through your work.
- Pull up the catalog traffic insights and see which books are actually getting attention right now. The data is there, it costs you nothing to look, and it'll inform every sequencing decision you make for the next year.

Browse the full LitRPG catalog, search by [narrator](/blog/2026-04-25-litrpgtools-narrator-registry-search-filter-litrpg-books-by-narrator/), or explore reading orders from your favorite authors on [LitRPGTools.com](https://litrpgtools.com). And when you've found your next reading-order anchor, our editorial guides are here to help — start with the [Dungeon Crawler Carl reading order](/blog/2026-03-25-dungeon-crawler-carl-reading-order/) or the [Cradle reading order](/blog/2026-04-07-cradle-reading-order-the-complete-guide-to-will-wights-series/) for two of the genre's most-asked-about paths.
