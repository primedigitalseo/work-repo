---
name: link-intersect-outreach
description: Build and run competitor link-intersect outreach campaigns for Prime Digital SEO clients — find every site linking to competitors but not to the client, drill down to the specific linking page and anchor, scrape the byline, waterfall-enrich the author's email, verify it, and push to Instantly with per-lead personalization variables. Use this whenever someone asks to run link prospecting, link intersect, link gap analysis, competitor backlink outreach, blogger/editor outreach, or cold link building for a client — including phrases like "run the link intersect for [client]", "who links to our competitors", "build a link prospect list", "link gap for [domain]", "find outreach targets for [client]", "cold outreach for links", "who should we email for links", or "run the delta" for a monthly refresh. Also trigger when scoping or pricing a link building offer, deciding whether a client's vertical can support editorial outreach at all, or when someone proposes buying links instead. This skill governs ALL editorial link outreach at Prime Digital SEO and is the gate that decides whether a client should be in an outreach campaign in the first place. It does NOT cover Semantic Links / LinkLab orders (see semantic-links-order) or disavow work (see disavow-file-builder).
---

# Link Intersect Outreach

Find people who have already proven they link out to content in your client's
category, reach them with a specific page and a specific reason, and repeat
monthly against the delta.

The whole edge here is relevance, not automation. Anyone can send 400 emails.
The reason this converts is that every recipient has demonstrably linked to a
competitor's page, and you are showing up referencing that exact link. Protect
that edge at every step — the moment the list stops being "people who provably
link out about this topic," you are just spamming, and the reply rate collapses
to zero while the domain reputation damage stays.

## Two gates before you prospect anything

Most of the money this skill saves is in *not* running campaigns that were
never going to work. Run both gates before promising a client anything.

### Gate 0 — Is the client's own link profile healthy?

Building new links onto a poisoned profile is pouring water into a leaky
bucket, and worse, it hides the real problem behind six months of "we're
building links." Pull these four numbers for the client domain first:

| Signal | Healthy | Investigate |
|---|---|---|
| Links ÷ referring domains | under ~20 | over 50 — sitewide or spam blasts |
| Refdomain growth curve | smooth | step-function jumps in a single month |
| Anchor profile | branded + URL dominant | foreign-language, gambling, adult, or SEO-service-pitch anchors |
| DR vs organic keywords | roughly proportional | DR 25+ with a handful of keywords means the DR is fake |

Any two of those firing means stop. Hand off to `disavow-file-builder`,
clean the profile, and re-run this gate after Google has re-crawled. Say this
to the client plainly — "we are not going to build on top of this" is a much
better conversation than one six months from now about why nothing moved.

The failure signature to recognize: a burst of tens of thousands of links from
a handful of unrelated foreign domains, all first-seen within one week, with
anchors in another language or anchors that are literally advertisements for
link-selling services. That is a negative SEO attack or a burned vendor, not a
link profile.

### Gate 1 — Does this vertical support editorial outreach at all?

This pipeline works because some categories have people who write about the
topic and link out. Many categories do not. Local home services mostly do not:
run an intersect on five local competitors in a trade vertical and what comes
back is directories, scrapers, and link-spam vendors — sites with no author, no
editorial decision, and nobody to email.

Test it in ten minutes and about 1,500 Ahrefs units before you sell anything:

1. Pull the top ~75 referring domains by DR for the single strongest local
   competitor.
2. Count how many are *emailable* — a real site, with articles, with bylines,
   that chose to link.

Under 5% emailable means the local intersect is dead. Do not force it. Go to
the vertical-level variant below, and if that is also dry, tell the client this
budget belongs in Semantic Links / LinkLab geo and niche placements instead.
Recommending the cheaper existing channel when it is the right answer is worth
more than a campaign that quietly fails.

## Choosing intersect targets

The original form of this tactic says "your top 5 competitors." For local
clients that is usually wrong, because your local competitors' backlinks are
citations, not editorial links.

**Local intersect** (`targets` = 5 direct local competitors): use when Gate 1
passed — competitive metros, categories with real trade press, or clients big
enough that regional media covers them.

**Vertical intersect** (`targets` = the national content sites that own the
category): use when the local intersect is dry. The prospects that come back
are national or regional publishers who link to category content, which buys
topical authority — the axis local clients are usually thin on. Geo relevance
you keep buying through Semantic Links; this buys the other one.

One trap worth knowing about when picking vertical targets: **a site's backlink
profile reflects why it is famous, not what it is about.** Some category leaders
are famous for their marketing rather than their subject — intersect against
them and you inherit marketing bloggers citing them as a case study, not
publishers who cover the topic. Sanity-check any target by scanning its top
refdomains for topical fit before committing units to it. If more than half the
links are from agency and SEO-tool blogs, pick a different target.

Whichever you choose, `exclude_targets` is always the client domain, so
everything returned is a genuine gap.

## Treat the output as archetypes, not a finished list

The intersect rarely hands you 400 clean prospects. What it reliably hands you
is a **taxonomy of who links to this category**, which is far more durable.

Read the surviving domains and name the patterns — real estate blogs writing
"does this add home value," materials and equipment manufacturers with dealer
pages, regional lifestyle magazines, trade publications, adjacent-service
contractors, local event and tourism sites. Then go find more of each archetype
inside the client's geography, which the intersect can't see because those
sites never linked to a national competitor.

The intersect is your discovery mechanism. The archetype list is the asset. It
carries across every client in the vertical and it is what makes the second
client in a niche cheaper than the first.

## Filters

Apply on the way out of the intersect. Read
`references/filters-and-scoring.md` for the reasoning behind each threshold and
the exact Ahrefs `where` syntax — the short version:

- Dofollow, at least one
- DR between the client's floor and ~80 (above that is platforms and directories)
- Referring domain organic traffic ≥ 2,000/mo — this catches what DR misses,
  because DR is gameable and traffic mostly isn't
- Spam score under 15
- `first_seen` within 24 months **OR** `last_seen` within 90 days — you want
  *alive*, not *new*. Straight recency alone deletes evergreen resource pages
  that have linked for five years and still get edited.
- One contact per domain, hard cap. Two people at the same publication getting
  the same pitch reads as spam and costs you the outlet.
- Drop anything matching the junk patterns list in the reference file
  (directories, scrapers, link vendors, free-site platforms).

Expect roughly 4,000 rows to become 300–450. If it becomes 40, you are in a
Gate 1 situation you talked yourself past — go back.

## From domain to a reason to email

This is the step almost nobody does, and it is the entire difference between
"loved your article" and an email that gets a reply. For each surviving domain,
hit the backlinks endpoint to get:

- the exact **page that links out**
- the **anchor text** used
- the **specific competitor URL** it points at
- the **page title** and topic

Then scrape the linking page for the byline — author name, author page, and
often an email sitting in the footer or on the about page. Use the `crawl4ai`
skill for this; it handles the JS-heavy cases and batches cleanly.

Store all of it. Every one of those fields becomes an Instantly variable.

## Enrichment waterfall

One provider gets 40–60%. Chaining gets past 85%. Order matters — cheapest and
highest-hit-rate first, stop at the first verified hit:

**Findymail → Prospeo → People Data Labs → Apollo (floor)**

Then verify everything through MillionVerifier before it touches a sender.
Catch-alls go in their own bucket and never send from a primary domain — route
them to a secondary or drop them. A 3% bounce rate is the difference between a
warm domain and a burned one.

If you don't want to run the chain, BetterContact or LeadMagic will do it for a
few cents an email. That is genuinely fine until volume makes it not fine —
somewhere north of ~5,000 lookups/month, build the chain.

## The suppression layer

This is the part that separates an agency process from a solo tactic, and it is
the one thing you cannot retrofit later. **Build the suppression table before
the first campaign, not after the first collision.**

Verticals overlap across clients. Without a central record you will pitch the
same editor for three different clients in one quarter, and that editor will
never open an email from you again.

One table, agency-wide: contact email, domain, client pitched for, date sent,
outcome. Check every new list against it before push. Rules:

- 90-day cooldown per contact across **all** clients
- Permanent exclusion on a negative reply or unsubscribe
- Never two clients to the same domain inside one quarter
- Exclude anyone already linking to the client

See `references/suppression-and-infrastructure.md` for the schema and the
sending infrastructure rules (domain separation, per-client sender identity,
volume ramps, CAN-SPAM requirements).

## Sending

Push to Instantly with every variable attached: linking page URL, page title,
competitor URL, anchor text, author name, topic.

**Personalize the variable, not the email.** One LLM call per lead writes a
single opening line off what is actually on their page. The body stays static.
This costs under a penny a lead, and 400 emails with one genuinely specific
line each reads more human than 400 fully generated ones — because fully
generated bodies drift into the same four adjectives and recipients notice.

Guard the generated line: **require it to contain a verbatim substring from the
scraped page.** If it doesn't validate, fall back to a template that uses the
page title directly. One hallucinated reference — a post they didn't write, a
topic that isn't theirs — costs a domain's reputation and any chance at the
relationship. Rejection rate runs around 10%, and those were your worst emails
anyway.

Templates and the line-generation prompt are in
`references/outreach-templates.md`.

## The monthly delta

Re-run the intersect every 30 days. The delta — every new link the competitors
picked up since last run — is the new target list.

This is the most valuable part of the whole system and it is easy to
under-sell. A one-time link gap audit is a project fee. A monthly delta is a
retainer with a visible artifact every single month: "here are the 23 sites
that linked to your competitors last month and not to you, and we've already
contacted 23 of them." Report it that way.

## What to tell clients about cost

Be straight about this internally so nobody oversells it. Marginal cost per
400-lead campaign lands around $50–100 all-in. Sending infrastructure amortizes
across clients.

But this does not make links free. At a 1–3% positive reply rate you get 4–12
conversations, and a real share of those come back with "sure, we charge $200."
Add reply handling, negotiation, and producing whatever asset you promised, and
all-in lands in the same $150–400/link range as Semantic Links.

**The case is not cost — it is that these are links you cannot buy from a
vendor:** topically relevant editorial placements on sites that already cover
the category, plus a repeatable monthly deliverable. Price and pitch it on that.

## Output

Deliver two things per run:

1. **Prospect sheet** (xlsx) — one row per contact: domain, DR, traffic,
   archetype, linking page URL, page title, anchor, competitor URL, author,
   email, verification status, suppression check result.
2. **Campaign brief** (1 page) — archetype breakdown, list size after each
   filter stage, sender identity used, volume ramp, and the delta vs. last month.

Use the `xlsx` skill for the sheet and `brand-kit` styling if the client sees it.
