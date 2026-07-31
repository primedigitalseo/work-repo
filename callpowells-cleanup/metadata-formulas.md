# On-Page Metadata & Alt-Text Standards (Tier 2)

Apply these formulas across the site to clear the audit's title/meta/H1 flags (18 meta
descriptions too long, 7 missing, 10 titles too long, 6 missing H1, 5 multiple-H1, 10 page/SERP
title mismatches) and to standardize new pages.

> The exact per-URL rewrite list (current title/meta pulled from the crawl) is a separate CSV I'll
> generate once Ahrefs API units reset — they're rate-limited right now. These formulas define
> what those rewrites will follow.

## Title tag (≤ 60 chars)

| Page type | Formula | Example |
|---|---|---|
| Service page | `[Service] in [City], [ST] \| Powell's` | `Water Heater Services in Norfolk, VA \| Powell's` |
| Category hub | `[Category] in [City], [ST] \| Powell's` | `Plumbing in Wilmington, NC \| Powell's` |
| City page | `Plumbing, Heating & Air in [City], [ST] \| Powell's` | `Plumbing, Heating & Air in Winchester, VA \| Powell's` |
| Homepage | `Powell's \| Plumbing, Heating & Air in VA & NC` | — |
| Blog post | `[Post Title] \| Powell's` | — |

Rules: brand at the end, city + state in every service/city title, keep under 60 chars (trim the
long ones flagged in the audit), no duplicate titles across pages.

## Meta description (≤ 155 chars, include phone)

`[Service] in [City], [ST] from Powell's — [benefit/《licensed, same-day》]. Call [PHONE].`

Example: `Water heater repair, installation & tankless service in Norfolk, VA. Licensed
plumbers, same-day service. Call [NORFOLK-PHONE].`

Rules: unique per page, one sentence + CTA, include the city's CallRail tracking number, trim the
18 flagged over-length descriptions, write the 7 missing ones.

## H1 (exactly one per page)

- **Service pages:** geo-free is acceptable but geo-included is stronger for local → `[Service] in [City]`.
- **City / category / homepage:** MUST include the city → `Plumbing, Heating & Air in [City], [ST]`.
- Fix the 5 multiple-H1 pages (demote extra H1s to H2/H3) and add H1s to the 6 missing.
- Resolve the 10 page/SERP-title mismatches by aligning the title tag with the actual page topic.

## Image alt text (174 images flagged)

Convention: `[subject] — [service] in [city]`, natural language, no keyword stuffing.
- Good: `Powell's technician installing a tankless water heater in Norfolk, VA`
- Good: `Furnace tune-up service in Winchester`
- Avoid: `plumber norfolk plumber norfolk water heater` (stuffed)
Decorative images get empty `alt=""`. Prioritize service/city page hero and body images.

## Canonicals

Every page must have a self-referencing canonical. Verify none of the consolidated/redirected
slugs are still emitting canonicals to themselves.

## IndexNow

After the redirects + metadata updates go live, submit the ~84 changed URLs (audit: "Pages to
submit to IndexNow") so Bing/Yandex re-crawl quickly. If the site runs Rank Math/Yoast + a
compatible IndexNow plugin, this can be automated; otherwise submit via the IndexNow API.

## Per-page publish checklist

- [ ] Title matches formula, ≤ 60 chars, unique
- [ ] Meta description matches formula, ≤ 155 chars, includes phone
- [ ] Exactly one H1, city-inclusive where required
- [ ] Self-referencing canonical
- [ ] FAQPage JSON-LD if the page has an FAQ
- [ ] All meaningful images have descriptive alt text
- [ ] Internal links to service + city pages present
- [ ] No links to redirected/404 slugs
