# Disavow Batch — 2026-11-05

Source: Ahrefs API (Lite plan), `site-explorer-referring-domains` + `site-explorer-refdomains-history`.
Rebuild: `python3 build_disavow.py 2026-11-05` (reads `raw/ahrefs_spam.json`).

## Spike finding

All 23 clients show the same referring-domain curve: a ramp starting May 2026 and a jump of
~1.5–2× between Aug 1 and Sep 1, 2026. Identical timing across unrelated sites points to
portfolio-wide spam networks:

| Network | Pattern | Clients hit | Link type |
|---|---|---|---|
| `.store` / `.shop` SEO-spam farm | `*seoexpress*`, `*link-baron*`, `*outrank-hq*`, `*rank-forge*`, `*boosthub/ranklab/seohub*.shop` | All | Mostly nofollow (0 dofollow) |
| Numeric `.xyz` farm | `11763xxx.xyz`, `37486xxx.xyz`, `54232xxx.xyz` | All sampled | Nofollow |
| Wiki farm | `*-wiki.win`, `wiki-*.win` | Nearly all | Dofollow (2–37 per domain) |
| DA/PA "checker" sites | `*checker*.site/.website/.online/.space` | All | Dofollow (1 each) |
| Turkish "haber" news network | `haber*.com.tr`, `gundem*` | Nationwide, Meigel, DSH | Dofollow, 3k–13k sitewide links per domain |
| Foreign/adult sitewide | `frine.org`, `ratheil.info`, `ecunationedirne.com`, `porno365.cv` | Mikita, Care Roofing, Bedrock Plumbing, DD&B | Dofollow, 10k–88k links |

## Method (budget-constrained)

20k Ahrefs units remained until the Nov 19 reset, so:

1. **Conner Roofing**: full spam-flagged list pulled (1,588 domains, links seen since 2025-11-01).
2. **Other 22 clients**: top 100 spam-flagged domains with dofollow links, sorted by link count.
   Nationwide, Meigel and DSH got a second page (Turkish network).
3. **Master network section**: 1,043 Conner domains matching the shared network patterns are added
   to every other client's file under a separate header. Exact-domain overlap measured on a
   Mikita sample was 42%; non-linking entries are no-ops in Google.
4. Turkish network (216 domains) is merged across Nationwide, Meigel and DSH.

## Gaps

- No client except Conner has its full spam list; nofollow-only spam beyond the master list is not covered.
- The Turkish network has more than 216 domains; further pages need units after Nov 19.
- The PBN-pattern query (step 2 of the SOP, zero-traffic dofollow non-spam) was skipped: `traffic_domain` costs 10 units/row.

## Files

- `2026-11-05/*-disavow-2026-11-05.txt` — one per client, GSC-ready
- `2026-11-05/flagged-for-review-2026-11-05.csv` — 366 rows held back for Mike
- `2026-11-05/excluded-whitelist-2026-11-05.csv` — whitelisted domains removed
- `2026-11-05/summary-2026-11-05.csv` — per-client counts

## Before uploading

Review the flagged CSV first. A cluster of real-business domains (law firms, dentists,
contractors, landscapers) sends dofollow links to 5–16 clients each, e.g. `find-us-here.com`,
`annikabansal.com`, `nataliegoldsteindds.com`, `woodard1law.com`, `campanelloconstruction.com`.
That pattern looks like a link exchange or vendor network. Confirm whether Prime Digital or a
vendor placed these before disavowing them.

Upload at https://search.google.com/search-console/disavow-links for both `https://` and
`https://www.` properties, then log date, count and file link in ClickUp.
