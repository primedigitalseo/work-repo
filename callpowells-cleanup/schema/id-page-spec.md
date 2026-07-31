# ID Page Spec (Entity Hub) — Tier 4

An **ID page** is a cloud-hosted static page (S3, Cloudflare Pages, or equivalent) referenced in
the LocalBusiness schema `@id`. It consolidates every external citation, profile, and branded
asset for one location into a single canonical hub, so bots have one place that validates the
brand-location entity. Build **one per location** (Winchester, Norfolk, Wilmington).

## Each ID page must contain

- Business name, full address, phone, website (exact NAP — must match GBP and on-site schema)
- Google Maps embed for that location
- A brief description reinforcing the semantic triple: **Powell's + [services] + [city]**
- Links to ALL verified external assets for the location:
  - GBP listing URL
  - Social profiles (Facebook, Instagram, YouTube, LinkedIn, Nextdoor)
  - Directories (Yelp, BBB, Angi, HomeAdvisor, industry/trade)
  - Chamber of commerce listing
  - Any press releases / cloud assets with accurate NAP
  - (These are the same URLs that go in the schema `sameAs` — the worksheet feeds both.)

## Wiring it up

1. Host the page (e.g. `https://[[host]]/powells-winchester`).
2. Put that URL in the location's schema `@id` (`...#business`).
3. Put every asset URL from `sameas-citation-worksheet.csv` into both the ID page body AND the
   schema `sameAs` array — the two reinforce the same entity from opposite directions.
4. Keep it current: every new citation/asset created gets added to the ID page.

## Status (fill during build)

| Location | ID page exists? | Referenced in @id? | Citations complete? | Action |
|---|---|---|---|---|
| Winchester | No (assumed) | — | — | Create |
| Norfolk | No (assumed) | — | — | Create |
| Wilmington | No (assumed) | — | — | Create |

> Confirm existing state before creating — if an ID page already exists for any location, update
> it rather than duplicating.
