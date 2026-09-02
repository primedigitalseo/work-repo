# Local Avenue prospecting system

Builds and ranks a list of residential home-service companies ($3M+) and the people
inside them who buy leads, then exports ready-to-send email and LinkedIn campaigns.

## Why it's built this way

Apollo already covers this ICP well — roofing alone returns ~8,500 contacts at
21-200 employees with marketing/GM/owner titles, ~90% with emails on file. Scraping
licensing boards or directories to *find* these people would be wasted effort.

What Apollo doesn't tell you is **who to contact this week and why**. That's what
this adds: coverage matching against your actual lead inventory, plus timing signals
pulled from the same API calls.

Two cost facts shape the pipeline:

- Apollo **search** is cheap and reports whether an email exists (`has_email`)
- Apollo **enrichment** costs 1 credit per revealed email

So the order is fixed: source wide, score, then spend credits only on the top of the
ranked list. Revealing 50k emails would cost more than the campaign is worth.

## Pipeline

```
00_load_coverage.py  your lead inventory by ZIP × service     <- run first
01_source.py         Apollo search -> companies + contacts     (no credits)
02_score.py          fit + coverage + timing -> A/B/C tiers    (no credits)
03_enrich.py         reveal emails, top of list only           (spends credits)
04_export.py         sequencer CSV + LinkedIn queue
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env          # add APOLLO_API_KEY
cp config/coverage.example.csv config/coverage.csv   # then fill in real inventory
python scripts/00_load_coverage.py config/coverage.csv
python scripts/01_source.py --all --limit-per-band 1000
python scripts/02_score.py
python scripts/03_enrich.py --budget 250 --tier A --dry-run
python scripts/03_enrich.py --budget 250 --tier A
python scripts/04_export.py --campaign roofing-q4 --tier A,B
```

## Coverage is 40% of the score

`config/coverage.csv` — one row per ZIP × service:

```
state,metro,postal_code,service,monthly_volume,fill_rate
TX,Dallas-Fort Worth,75201,roofing,140,0.35
```

`fill_rate` is the share already sold, so unsold volume is `monthly_volume × (1 - fill_rate)`.
A company in a state with no coverage row drops to `hold` regardless of how good the
profile looks — pitching a market you can't fill costs more than skipping it.

Without this file the system still ranks by fit and timing, but every email opens with
a generic line instead of "we have 167 unsold roofing leads a month in your state."
That sentence is the entire differentiator against every other vendor in their inbox.

## Sizing logic

Private home-service revenue isn't published; headcount is. At roughly $150-250k
revenue per employee:

| Employees | Est. revenue | Who buys | Priority |
|---|---|---|---|
| 11-20 | $2-5M | owner / president | 3 |
| 21-50 | $5-12M | GM, ops manager, first marketing hire | 1 |
| 51-200 | $12-50M | director of marketing | **0 — best fit** |
| 201-500 | $50-125M | VP / CMO, longer cycle | 2 |

`config/icp.yaml` holds the title ladder per band. Below ~50 employees there usually
is no marketing director and the owner decides; the ladder handles that switch, and
pulls 1-4 contacts per company depending on size.

## Signals

Detected from the same Apollo calls, no extra tooling:

| Signal | Points | Why it matters |
|---|---|---|
| New marketing leader (<6 mo in seat) | 8 | Hired to change something; highest vendor-conversion window |
| Hiring field staff | 6 | Techs coming online need demand to bill against |
| Acquisition / new location | 6 | New branch has capacity and no lead flow |
| New market entry | 5 | No brand, no organic volume |
| Headcount growth | 3 | |

## Email infrastructure

The list is the easy half. Deliverability decides whether any of it lands:

- Send from **secondary domains**, never your primary. Two or three lookalikes
  (`golocalavenue.com`, `localavenue.co`), 2-3 mailboxes each
- SPF, DKIM, and DMARC on every sending domain before the first send
- **14-21 days of warmup** per mailbox before real volume
- Cap at **30-40 sends per mailbox per day**. Ten mailboxes is 300-400/day
- Verify every address before it enters a sequence (MillionVerifier, ~$0.0004 each).
  Bounce rate over 3% burns the domain
- Pause a mailbox the moment its bounce rate climbs, and re-verify the segment

## LinkedIn — read this before automating

LinkedIn's User Agreement prohibits automated access and messaging. Accounts running
automation get restricted or permanently banned, and this is not theoretical: LinkedIn
won a $500k breach-of-contract judgment against hiQ Labs in December 2022 on exactly
that contract theory, after losing the CFAA argument.

`04_export.py` writes a **queue**, not an autopilot: rows are ordered and stamped with
a `send_day` so you can work them manually or feed a tool you've chosen with the risk
understood. Defaults are 20 connection requests a day, which is under the threshold
where accounts typically get flagged.

If you do automate, use a separate account from your primary, keep daily caps low, and
expect to lose the account eventually. That's a business decision, not a technical one.

## Compliance

- **CAN-SPAM** — every email needs a real physical address, a working unsubscribe, and
  a subject line that doesn't misrepresent the message. Honor opt-outs within 10 days
- **CCPA/CPRA** — California's B2B exemption sunset January 1, 2023. Work emails and
  job titles of California residents are protected personal information now. You need a
  notice at collection and a working deletion path. At scale this can trigger data-broker
  registration
- The `suppression` table holds unsubscribes and bad domains. Every export filters
  against it. Load opt-outs the same day you receive them

## Extending sources

Apollo misses some companies entirely — typically owner-operated shops under 25 employees
that never built a LinkedIn presence. When you want that tail:

- **State contractor license boards** — the authoritative roster of who's licensed and
  active, by trade and state. No emails, so pair with domain discovery
- **Manufacturer certified-contractor directories** — GAF, Owens Corning, Carrier,
  Trane. Certification correlates with size and these are clean, paginated HTML
- **Trade associations** — NRCA (roofing), PHCC (plumbing), ACCA (HVAC), NPMA (pest)

Insert them as `companies` rows with `source` set accordingly; scoring and export work
unchanged. Do this only after Apollo's coverage is exhausted for a vertical.
