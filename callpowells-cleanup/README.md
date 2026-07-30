# Callpowells.com — Site Cleanup (Ahrefs Site Audit)

**Source:** Ahrefs Site Audit project *Callpowells* (ID 9339278)
**Crawl date:** 2026-07-28 · **Health score:** 67/100
**Pages crawled:** 852 · **URLs with errors:** 277

## Why this cleanup matters for local map-pack ranking

The site is carrying **104 broken (404) service/city pages** that are still internally
linked (25–52 internal links each) and, in ~15 cases, still hold earned backlinks.
This wastes crawl budget, leaks internal PageRank into dead ends, and — for the
backlink-bearing pages — dumps external authority into a 404 instead of into a page
that could rank. Consolidating this authority back into the live location and service
pages is the fastest structural win for map-pack relevance.

## Files

- **`callpowells-redirect-map.csv`** — 301 redirect plan for the broken pages.
  Columns: `source_url_404`, `target_url_301`, `silo`, `backlinks`,
  `internal_links`, `action`, `notes`.

## How to read the `action` column

| action | meaning |
|---|---|
| `redirect` | Straightforward 301 to the closest live page. Just implement. |
| `rebuild-or-redirect` | Page has real backlinks (see `backlinks`). **Decide:** if Powell's still services that trade in that city, *rebuild the page* to recover the ranking + links; otherwise 301 to the listed hub. |

## Priority order

1. **Rebuild-or-redirect rows first (15 pages).** These carry the backlinks — highest
   value. Top targets: `winchester/plumbing/boiler-repair/` (128 backlinks),
   `winchester/plumbing/tankless-water-heaters/` (119), and 13 Norfolk HVAC pages (40–104).
2. **Bulk `redirect` rows (85 pages).** Mostly the 59 Wilmington
   `sewer-line-repair/{city}/` sub-pages → consolidate all to the live parent
   `/wilmington/plumbing/sewer-line-repair/`.
3. **Remove the internal links** pointing at the dead URLs (menus, silo/footer link
   modules) so the site stops referencing 404s after redirects go in.

> Note: The audit reports 104 total 4XX URLs; this map covers 100. Any additional
> `/wilmington/plumbing/sewer-line-repair/{city}/` URLs not listed follow the same
> rule — 301 to the live parent `/wilmington/plumbing/sewer-line-repair/`.

## Implementation (WordPress / Elementor)

The site runs WordPress (Hello Elementor theme). Easiest path:
- Import `callpowells-redirect-map.csv` into the **Redirection** plugin (or Rank Math
  → Redirections), mapping `source_url_404` → `target_url_301` as 301s.
- After redirects are live, re-crawl in Ahrefs to confirm the 404 count drops and the
  health score recovers.

## Other issues flagged in the same audit (not in this file)

- 141 pages with broken/redirected JavaScript + 141 with redirected images
  (likely one site-wide theme/plugin asset — one fix clears ~140 URLs).
- 174 images missing alt text (add service + city terms).
- 17 noindex pages and 5 orphan pages to review.
- On-page: 18 meta descriptions too long, 10 titles too long, 6 missing H1s.
