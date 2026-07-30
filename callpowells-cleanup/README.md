# Callpowells.com — Site Cleanup (Ahrefs Site Audit)

**Source:** Ahrefs Site Audit project *Callpowells* (ID 9339278)
**Crawl date:** 2026-07-28 · **Health score:** 67/100 · **Pages crawled:** 852 · **URLs with errors:** 277

## What this fixes

The site is carrying **104 broken (404) pages** that are still internally linked (25–52 links
each) and, in 15 cases, still hold earned backlinks. This wastes crawl budget, leaks internal
PageRank into dead ends, and dumps external authority into 404s. Consolidating it back into the
live pages is the fastest structural win for map-pack relevance.

## Redirect targets are grounded in each city's MAIN NAV

Every target was chosen by reading the **main navigation menu of each city site**
(`/norfolk/`, `/winchester/`, `/wilmington/`) — the nav is the source of truth for which
services each city actually offers:

- **Norfolk nav lists no AC or Heating child pages** (only the AC and Heating hubs). So every
  Norfolk AC/Heating 404 → its hub. The 13 backlink-bearing Norfolk HVAC pages preserve their
  links via the 301 into the hub.
- **Winchester nav** lists `gas-oil-furnaces-repair` ("Furnaces"), `water-heater-services`, and
  `boiler-and-radiator-services` — not the separate `furnace-repair`, `tankless-water-heaters`,
  or `boiler-repair` pages. So those 404s map to the nav survivors.
- **Wilmington nav** points "Water Heater Repair" at `/wilmington/heating/water-heater-repair/`,
  which **404s** — the live page is `/wilmington/plumbing/water-heater-repair/`. The nav link
  itself needs repointing (flagged below).

Rule applied to every row: **if the service appears in that city's nav → 301 to the live nav
page; if it does not → 301 to the category hub (Plumbing / AC / Heating / Septic).**

## Files

| File | Use |
|---|---|
| **`callpowells-redirects-import.csv`** | **Give this to Viktor.** 2-column `source,target` (relative paths), ready to import into the **Redirection** plugin. 100 rows. |
| **`callpowells-redirect-map.csv`** | Review copy — full URLs + `backlinks`, `internal_links`, and a `notes` column explaining each target. |

## Three nav links to repoint (not just redirect)

These are broken links inside the menus themselves — fix the menu item in addition to the 301:

1. Norfolk **"Services"** → `/norfolk/?page_id=71` (404). Repoint or remove the menu item.
2. Wilmington **"Water Heater Repair"** → `/wilmington/heating/water-heater-repair/` (404).
   Repoint to `/wilmington/plumbing/water-heater-repair/`.
3. Any city menu item still pointing at a redirected slug should be updated to the live target
   so the nav stops firing 301s on every page load.

## After redirects: remove the dead internal links

The Norfolk/Winchester HVAC and septic 404s each have 25–33 internal links (they're built into
the silo/footer link modules). Once redirects are live, strip those links so the site stops
referencing 404s, then re-crawl in Ahrefs to confirm the 404 count drops and health recovers.

---

## Your question: water-heater-services hub vs. individual water-heater pages

**Current state (from each city's nav):**

| City | Water-heater pages in nav |
|---|---|
| Norfolk | Water Heater Services (hub), Tankless Water Heaters, Water Heater Installation |
| Winchester | Water Heater Services (hub) only |
| Wilmington | Water Heater Services (hub), Tankless, Repair, Installation, Replacement (5 pages) |

**Recommendation (Benner lean-site framework):** **Keep ONE `water-heater-services` hub per
city. Fold Installation / Repair / Replacement / Tankless into it as H3 sections**, and 301 the
individual slugs into the hub.

Why:
- They're all the **same Google entity** ("water heater service") — separate pages target the
  same category and split internal link equity instead of concentrating it.
- None of the individual water-heater pages show organic traffic in the audit; they're thin
  near-duplicates. Under the helpful-content site-quality multiplier, 5 overlapping pages per
  city drag the whole silo down.
- Backlinks are preserved through the 301 (e.g., Winchester's `tankless-water-heaters` with 119
  backlinks → `water-heater-services`).
- Benner rule: start a sub-service as an H3 on the parent; only promote it back to a standalone
  page if ranking data later shows the hub can't rank for that term alone. Right now there's no
  such data, so consolidate.

**Net:** Winchester is already correct (hub only). Standardize Norfolk and Wilmington down to
the single hub. This is a separate change from the 404 cleanup (it removes *live* nav pages), so
those consolidation redirects are **not** in the import file yet — say the word and I'll add the
water-heater consolidation rows and write the merged hub content.

---

## Implementation (WordPress / Elementor + Redirection plugin)

1. Import `callpowells-redirects-import.csv` into **Redirection** (Tools → Import, map
   `source`→`target`, 301).
2. Repoint the 3 broken nav items above.
3. Remove dead internal links pointing at the old 404 slugs.
4. Re-crawl in Ahrefs to confirm 404s cleared and health score recovered.

## Other issues in the same audit (not in this file)

- 141 pages with broken/redirected JavaScript + 141 with redirected images (likely one
  site-wide theme/plugin asset — one fix clears ~140 URLs).
- 174 images missing alt text (add service + city terms).
- 17 noindex pages and 5 orphan pages to review.
- On-page: 18 meta descriptions too long, 10 titles too long, 6 missing H1s.
