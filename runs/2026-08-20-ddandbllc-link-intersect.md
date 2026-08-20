# Link Intersect Run — ddandbllc.com

**Client:** DD&B Custom Home & Pool Builders (Dream Design & Build LLC)
**Market:** Gulf Shores / Orange Beach / Baldwin County, AL
**Services:** Custom homes, gunite + fiberglass pool construction, pool
remodeling, pool design, home remodeling
**Run date:** 2026-08-20
**Data source:** Ahrefs API v3
**Outcome: STOPPED AT GATE 0 — do not run outreach**

---

## Gate 0 — Client link profile triage: FAILED

| Signal | Value | Threshold | Result |
|---|---|---|---|
| Live backlinks | 102,468 | — | — |
| Live referring domains | 825 | — | — |
| Links per refdomain | **124** | under 20 | FAIL |
| Domain Rating | 25 | — | — |
| Organic keywords (US) | **2** | proportional to DR | FAIL |
| Organic traffic (US) | 31/mo | — | — |
| Anchor profile | gambling / adult / SEO-pitch | branded + URL | FAIL |
| Refdomain curve | step-function bursts | smooth | FAIL |

Four of four fired. This is a negative SEO attack layered on top of a
previously purchased link profile.

### The attack

Top referring domains by link volume, all first seen 2026-06-07 → 2026-06-12:

| Domain | DR | Links | First seen |
|---|---|---|---|
| frine.org | 16 | 88,344 | 2026-06-07 |
| ecunationedirne.com | 6 | 63,936 | 2026-06-11 |
| shipvite.com | 41 | 52,391 | 2026-06-07 |
| rajeshdaikojokes.com | 11 | 12,900 | 2026-06-09 |
| fillopack.com | 12 | 11,271 | 2026-06-08 |
| sex-studentski.com | 8 | 6,159 | 2026-06-07 |
| sex-studentki.eu | 8 | 3,852 | 2026-06-07 |
| porno365.cv | 13 | 496 | 2026-06-07 |

Roughly 240,000 links appeared in a six-day window from Turkish-language,
gambling, and adult domains.

### The anchors

| Anchor | Refdomains | Links |
|---|---|---|
| `galabet giriş` (Turkish gambling) | 208 | **254,211** |
| `DD&B Custom Home & Pool Builders` | 225 | 411 |
| Fake testimonial naming "SEOExpress.org" | 219 | 230 |
| `https://ddandbllc.com/` | 208 | 331 |
| "Boost ddandbllc.com using high-quality backlinks..." | 43 | 43 |
| "High Quality Dofollow Backlinks DA 50 PA 40 Premium PBN..." | 7 | 7 |

A quarter-million links pointing at the client's domain with Turkish gambling
anchor text. Several anchors are literally advertisements for link-selling
services.

### The timeline

Referring domains by month:

```
2025-01    9
2025-06   33     DR 3.7
2025-08   54     DR 18
2025-11  145     DR 28
2025-12  362  <- +217 in one month (purchased link blast)
2026-03  288     DR 28  (plateau, no ranking gain)
2026-05  489     DR 27  <- attack begins
2026-06  656     DR 26
2026-07  737     DR 26
2026-08  824     DR 25  <- DR now declining
```

Two separate events. **December 2025:** a +217 refdomain blast — a bought link
package. It moved DR from 3.7 to 28 in six months and produced two ranking
keywords, which tells you the links were junk. **May–August 2026:** the spam
attack, ongoing, now actively dragging DR down as Ahrefs discounts it.

### Read

The site ranks for exactly two terms — `pool remodeling orange beach` (#2) and
`pool renovations orange beach` (#9) — both on `/pool-remodeling/`. A genuine
DR 28 local site would rank for dozens of local terms. The DR is not real.

The one piece of good news: the attack looks like it has not yet produced a
manual action or a visible ranking collapse, because there was very little
ranking to collapse. Cleaning this up now is cheap. In six months it will not be.

---

## Gate 1 — Vertical viability: FAILED (local variant)

Tested the local intersect against the strongest direct competitor,
`coxpoolsse.com` (established 1955, the dominant local player). Pulled the top
75 referring domains by DR and classified them.

| Category | Count | Emailable? |
|---|---|---|
| Business directories / citation aggregators | 27 | No |
| SEO tool scrapers and stat sites | 10 | No |
| Link-spam vendor domains | 8 | No |
| Free-site platforms (blogspot, weebly, homestead) | 6 | No |
| Corporate / data (D&B, hoovers, procore, crunchbase) | 5 | No |
| **Genuinely emailable editorial** | **~4** | Yes |

**Emailable rate: ~5%.** Under the 5% floor. Cross-checked against
`southernpoolscapes.com` — same distribution, plus press-release syndication
(abnewswire) and fake market-research sites.

The only real prospects in 125 rows of competitor backlinks:

- `lyonfinancial.net` — pool financing company, 14 dofollow links out, clearly
  links to builders it works with. Strong, obvious, and reachable.
- `citylifestyle.com` — regional lifestyle magazine network
- `hangoutmusicfest.com` — Gulf Shores music festival, local sponsorship angle
- `guildquality.com` — contractor review platform

Notable: eight link-spam vendor domains (`buybacklinks.agency`,
`backlinker.shop`, `rankxlinks.shop`, `seorankflow.shop`,
`buyseobacklinks.shop`, `linkrankpro.shop`, `ranklinkerpro.shop`,
`rank-top.click`) appear in Cox Pools' profile too. **The whole local market is
buying links from the same vendors.** That is a competitive read worth having:
nobody in this market has earned links, so the bar to actually earn a few is low.

---

## Vertical intersect — tested, partial

Ran the vertical variant against `riverpoolsandspas.com` (the largest pool
content site in the US) with full quality filters applied: DR 25–80, traffic
≥2,000/mo, dofollow ≥1, first seen since 2024-08.

60 rows returned. Roughly 10 were topically relevant.

**Why the yield was low — worth recording as a lesson.** River Pools is famous
for *content marketing* (Marcus Sheridan / "They Ask You Answer"), not for
pools. Its backlink profile is therefore dominated by marketing agency and
SEO-tool blogs citing it as a case study: `hookagency.com`, `leanlabs.com`,
`huble.com`, `inblog.ai`, `xgrowth.com.au`, `amraandelma.com`, `wordtracker.com`,
`sortlist.co.uk`, `elementor.cloud`, `markezine.jp`.

A site's backlink profile reflects why it is famous, not what it is about.
Next run, pick vertical targets that are topically famous — Latham, Pool &
Spa News, regional outdoor-living publishers — and sanity-check the profile
before spending units.

### The archetypes it did surface

Even at low yield, the run named the patterns worth chasing — and these are the
durable asset, reusable for every pool client:

| Archetype | Examples found | Local equivalent to hunt |
|---|---|---|
| **Real estate / home value blogs** | raleighrealty.com, ibuyer.com, brittany.com.ph | Gulf Coast realtors, Baldwin County brokerages, vacation-rental managers writing "does a pool add value" |
| **Materials & equipment manufacturers** | belgard.com, whytile.com, endlesspools.com | Dealer/installer pages — DD&B almost certainly already buys from several |
| **Trade publications** | lawnandlandscape.com | Pool & Spa News, PHTA, AQUA Magazine |
| **Custom home builder networks** | alairhomes.com | Regional builder associations, Baldwin County HBA |
| **Regional lifestyle / tourism** | calabogie.com, citylifestyle.com | Gulf Shores tourism, Southern Living regional, coastal living blogs |

The real-estate archetype is the strongest fit for DD&B and the intersect would
never have found the local ones — those sites never linked to a national pool
brand. This is the archetype-discovery pattern working as intended.

---

## Recommendation

**Do not run outreach for this client yet.** Sequence:

1. **Disavow now.** Hand to `disavow-file-builder`. All eight attack domains,
   the full `galabet giriş` anchor cluster, and the December 2025 purchased
   batch. This is urgent and cheap today.
2. **Have the vendor conversation.** Someone sold DD&B links in late 2025. Find
   out who, and make sure that contract is dead before building anything.
3. **Fix the ranking base.** Two keywords on one page for a
   custom-home-plus-pool builder across Baldwin County is a site problem, not a
   link problem. Run `benner-site-audit`, then `gbp-coverage-planner` for the
   city/service page build.
4. **Build the asset.** Real cost data across their gunite builds, or Gulf
   Coast–specific construction data (salt air, water table, hurricane code).
   No editorial outreach is worth running without it.
5. **Re-run this skill in ~90 days**, post-disavow, using the archetype list
   above seeded regionally rather than a national intersect.

Meanwhile, geo and niche placements through Semantic Links are the right
channel for this client — with the caveat that anchor text needs to stay
branded and URL-based until the spam anchor ratio comes down.

## Cost of this run

~4,400 Ahrefs units. Workspace usage after run: ~24,500 / 100,000, resets
2026-09-19.
