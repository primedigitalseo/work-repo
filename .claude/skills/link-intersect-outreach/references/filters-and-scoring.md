# Filters and Scoring

## Why each threshold exists

**Dofollow ≥ 1.** Straightforward on the value side. Note the tension: a site
that nofollows a competitor still *proved editorial link-out behavior*, and its
next link might be dofollow. If a vertical is prospect-poor, relaxing this is
the first filter to loosen — it typically adds 15–25% more emailable domains.

**DR floor to ~80 ceiling.** The floor is the client's own DR or 20, whichever
is higher — below that the link is not worth an email. The ceiling matters more
than people expect: above ~80 you are almost entirely in platforms
(blogspot, weebly, wix), aggregators (yellowpages, superpages, BBB), and
scrapers. Those are not outreach targets.

**Organic traffic ≥ 2,000/mo.** This is the single highest-value filter and the
one most often skipped. DR is gameable — a link-spam vendor domain can sit at
DR 69 with literally zero organic traffic. Traffic is much harder to fake.
When DR and traffic disagree, believe traffic.

**Spam score < 15.** DataForSEO's own metric. Useful but not sufficient on its
own; it misses expired-domain and parasite plays that the traffic floor catches.

**Recency: `first_seen` within 24 months OR `last_seen` within 90 days.**
Recency alone is the common mistake. It finds active linkers but deletes
evergreen resource pages that have linked for five years and still get updated
every season — often the best prospects in the set, since the page is
maintained and the maintainer is reachable. The OR keeps both populations.

**One contact per domain.** Two people at the same publication receiving the
same pitch in the same week reads as spam. It costs the outlet permanently for
a marginal second shot.

## Junk pattern exclusion list

Drop on domain match. This list is the accumulated residue of local-vertical
intersects and saves a lot of manual review:

```
# Business directories / aggregators
yellowpages superpages dexknows yp.com chamberofcommerce ezlocal citysquares
cityfos golocal247 uscity yellow.place tupalo find-open kudzu 2findlocal
showmelocal local.com mylocalservices bizbangboom yellowpagecity cylex
ibegin find-us-here bestprosintown allbiz freelistingusa ebusinesspages
bizhwy hoovers dnb.com dandb.com neustarlocaleze topratedlocal citysquares

# SEO tool scrapers / stat sites
woorank siteprice sitelike similarsites ispionage webwiki rankva
rankyour.website rank-your.site rank-top techdirectory siteprice

# Link-spam vendors (any of these appearing in a competitor's profile
# is itself a signal that competitor bought links)
buybacklinks backlinker linkrankpro rankxlinks ranklinkerpro seorankflow
buyseobacklinks *.shop-with-seo-words

# Free-site platforms / UGC
blogspot weebly wix homestead geocities.ws soup.io anonym.to livepositively
stagram appbrain

# Press release syndication
abnewswire ein-presswire prnewswire-syndicated openpr
```

Treat this as a living list. When a manual review turns up a new junk pattern,
add it here rather than filtering it by hand next month.

## Ahrefs `where` syntax

The MCP passes a JSON filter object. Working example against
`site-explorer-referring-domains`:

```json
{"and":[
  {"field":"domain_rating","is":["gte",25]},
  {"field":"domain_rating","is":["lte",80]},
  {"field":"traffic_domain","is":["gte",2000]},
  {"field":"dofollow_links","is":["gte",1]},
  {"field":"first_seen","is":["gte","2024-08-01"]}
]}
```

Useful `select` set:
`domain,domain_rating,links_to_target,dofollow_links,first_seen,traffic_domain`

Order by `traffic_domain:desc` rather than `domain_rating:desc` — it surfaces
real publishers first instead of high-DR directories.

## API unit budget

Ahrefs Lite is 100,000 units/month. Referring-domains rows cost ~15 units each
with the full select set, so budget accordingly:

| Step | Rows | Approx units |
|---|---|---|
| Gate 0 client triage (DR, stats, anchors, history) | ~60 | ~500 |
| Gate 1 viability test (1 competitor, 75 rows) | 75 | ~1,100 |
| Full intersect (5 targets × 100 rows) | 500 | ~7,500 |
| Monthly delta (5 targets, recency-filtered) | ~100 | ~1,500 |

A full new-client run is roughly 9,000 units; a monthly delta about 1,500.
That supports ~8 active clients on a Lite plan. Check
`subscription-info-limits-and-usage` (free, no units) before large pulls.

## Scoring for send priority

When the list is larger than the sending capacity, rank by:

```
score = log10(traffic_domain) * 2
      + (dofollow_links > 0 ? 1 : 0)
      + (has_byline ? 2 : 0)
      + (email_verified_valid ? 3 : 0)
      + archetype_weight
```

`archetype_weight`: 3 for archetypes that have converted for this vertical
before, 1 for untested, 0 for archetypes that have gone 0-for-50. Update these
weights from actual reply data each month — after two or three cycles this is
the most accurate targeting signal you have, and it is client-independent
within a vertical.
