# Home Service Base API client

Read-only client for the [Home Service Base](https://homeservicebase.com) API v1,
built to feed the expired-domain screen without repeating the mistakes of the
first three runs.

## Setup

Two things are needed before any live call works.

**1. API key.** Create one at Settings → API (Business plan and above) and store
it in the environment as `HSB_API_KEY`. In a Claude Code cloud session that is
the environment menu in the title bar → Edit → API credentials, or as a plain
environment variable. A new session picks it up. The key is shown once and looks
like `hsb_…`; never paste it into a chat or commit it.

**2. Network access.** `homeservicebase.com` must be in the environment's allowed
domains, otherwise the egress proxy answers `403` to the CONNECT and every call
fails before it leaves the container. Same menu → Edit → Network access.

Verify both:

```bash
python3 tools/hsb.py units          # free, prints the unit balance
```

## Commands

```bash
# Unregistered domains in Minnesota, plumbers and roofers, 5+ reviews
python3 tools/hsb.py expired --state 24 --category Plumber --category Roofer \
    --min-reviews 5 --limit 200 > candidates.csv

# Same query, printed not sent — costs nothing and needs no key
python3 tools/hsb.py expired --state 24 --category Plumber --dry-run

# Raw search with any filter from the API reference
python3 tools/hsb.py websites -f primaryCategory=Roofer -f minProfiles=5 --limit 100
python3 tools/hsb.py profiles -f stateId=24 -f runsLsa=1 --format json

# Signal results
python3 tools/hsb.py signal <uuid> --type new_websites --limit 100
```

Repeat `-f` to repeat a key: `-f stateId=6 -f stateId=48`.

### `watch` — the one that matters

The API has no drop-date filter, so domain freshness has to be derived. `watch`
snapshots the unregistered set for a query and prints only what is new since the
last run.

```bash
python3 tools/hsb.py watch mn-trades --state 24 --limit 1000
```

First run writes a baseline to `.hsb-state/mn-trades.json` and prints nothing.
Every run after that emits the domains that entered the set since — domains that
dropped recently.

This is the fix for the finding that ended run 003: across 86 screened domains,
the link-selling networks had already occupied nearly every candidate, with
their links first seen between March and September 2026. Buying from a static
export means arriving after them. A weekly `watch` puts you in the window before
the blast lands.

### `metro_watch.py` — weekly drops for every client metro

`watch` keyed to the client markets in `tools/metro_watch.json`: each market is
a set of county GEOIDs, pulled with `geoKind=county`, limited to
home-improvement categories minus the client's own niche (no roofers for a
roofing client, no pool builders for a pool client).

```bash
python3 tools/metro_watch.py              # all markets, ~3,400 units
python3 tools/metro_watch.py dsh          # one market
python3 tools/metro_watch.py --dry-run    # URLs only, free
```

Snapshots are written to `watch-state/` and new domains to
`watch-reports/<date>.csv`. Both are committed: a cloud container does not
survive between weekly runs, and a lost snapshot turns the next run into a new
baseline instead of a diff. The baseline was seeded from the 2026-09-24 pull.

Screen the new domains with Ahrefs' free `public-domain-rating-free` first (up
to 1,000 per call, 0 units), then pull referring domains only for DR 7+,
capped at 5 per market.

## Guardrails

The client enforces the account limits so a caller cannot trip them: one request
in flight, requests spaced at least 1.05s apart (60/60s), 1000 rows per page,
`Retry-After` honoured on `429`, one retry on a `503` query timeout.

Two guards are specific to expired-domain work:

- **`expired` forces `domainUnregistered=1`.** It cannot be turned off. Run 001
  was exported with the establishment-date filter instead of domain status and
  shipped 50 live businesses — care.com among them, running 2,000 Google Ads.
- **`expired` refuses `established` / `establishedFrom` / `establishedTo`.** An
  unregistered domain has no WHOIS record and therefore no registration date, so
  combining them silently returns the wrong set. If any returned row carries a
  registration date anyway, the command warns loudly before you spend Ahrefs
  units on it.

## Units

One unit per row returned. Errors and empty pages are free. `--limit` is exact —
the last page is trimmed to what you asked for, so no over-fetch. Monthly
allowance is 25,000 on Business, and it is shared by every key on the account.

`--dry-run` builds the URL locally: no key, no request, no units.

## Feeding the screen

`expired` emits the column order the
[Expired Domain Screen](https://claude.ai/artifact/XCV9SHMkp9crRgqjpsiuPj)
expects, so the CSV drops straight into the Ahrefs batch-analysis step:

```
domain, name, primaryCategory, city, state, rating, reviewsCount, phone, mapsUrl, profileUuid
```

`--endpoint websites` switches to the grouped-by-domain view when profile counts
matter more than location.

## Layout

```
tools/hsb.py           entry point
tools/hsb/client.py    HTTP, rate limiting, paging, unit accounting
tools/hsb/cli.py       commands and output formatting
tools/metro_watch.py   weekly drop watch across client metros
tools/metro_watch.json client markets, county GEOIDs, category list
watch-state/           metro_watch snapshots (committed)
watch-reports/         metro_watch new-drop CSVs (committed)
.hsb-state/            watch snapshots (gitignored)
```
