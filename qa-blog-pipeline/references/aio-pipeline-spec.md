# AIO Content Pipeline Spec - Prime Digital SEO

**Version 1.0 · Aug 2026 · Owner: Mike Amatulli**

Operating spec for the Claude Code Q&A blog pipeline (Keywords Everywhere +
DataForSEO). Replaces PAA-sourced question selection.

This file is the source of record. `../SKILL.md` is this spec turned into the
week-to-week process. Where the two disagree, this file wins and the skill gets
fixed.

## 0. Scope and target surface

This pipeline targets Google AI Overviews and Gemini. It is not a ChatGPT
visibility play.

**Evidence:** Gemini cites the business's own website 59.9% of the time; ChatGPT
does so 15.9%, favoring social/community forums (41.7%) and general directories
(34.6%). Cited-domain overlap between the two engines is 8%; same top business
named, 4.2%. (Steady Demand Citation Ledger, Aug 2026, n=14,472 citations /
1,487 queries / 50 metros.)

**Consequence:** ChatGPT visibility requires a separate workstream, vertical
community presence and vertical-specific directories. Do not scope Q&A content
as an "AI visibility" deliverable without naming the engine.

## 1. What the internal sample established

Ahrefs site-explorer-organic-keywords, `best_position_kind = ai_overview`, Aug
2026 vs Feb 2026 delta. n=4 client domains.

| Finding | Evidence |
|---|---|
| Content program causes AIO lift | Care Roofing: 18/18 AIO placements `status: left`, `best_position_kind_prev: null`. Zero six months prior. |
| AIO citation does not require top-3 organic | Bedrock: 5 keywords promoted from organic #8-#19 into AIO #1. |
| One post can capture a full variant cluster | Bedrock `/why-does-my-garbage-disposal-smell-like-sewage.../` holds 10 keywords. |
| Format alone is insufficient | EverClear runs the same Q&A pipeline, holds 2 AIO keywords. Topic demand failed. |
| Image packs cannibalize AIO on spec queries | Conner: 40 AIO-eligible keywords from one page, 30 won as image, only 4 as `ai_overview`. |

## 2. Pipeline stages

### Stage 1 - Discovery (existing)

Keywords Everywhere `related` + `pasf` endpoints to a candidate universe per
service line. Return search volume only. No CPC, no competition data.

### Stage 2 - AIO qualification gate (NEW, blocking)

For every candidate, call DataForSEO `serp/google/organic/live/advanced` and
evaluate `item_types`:

```
QUALIFY   if 'ai_overview' in item_types
REJECT    if 'images' in item_types        # Conner failure mode
REJECT    if volume < 150 on head term     # EverClear failure mode
```

Then classify by phrasing. Accept:

- **Symptom** - "why does my X...", "what causes X...", "is it normal for X..."
- **Duration** - "how long does X take"
- **Cost** - "how much does X cost", "X cost per..."
- **Procedure** - "do I need to X before Y", "can you reuse X"

Reject definition and spec phrasing ("what is X", "X dimensions", "X chart").
These lose to image packs.

### Stage 3 - Citation-gap extraction (NEW)

The AI Overview block in the DataForSEO response carries a `references[]` array.
Pull it for every qualified keyword and build two lists:

- **Currently-cited domains** - who owns the answer today. If a direct competitor
  appears, the keyword is a displacement target and gets priority.
- **Fan-out phrasings** - the actual queries the AI Overview resolved.

This replaces PAA as the question source. Gemini's own fan-out queries overlap
Google PAA phrasing only 12.7% on average, with 80% of fan-out queries scoring
below 0.2 similarity. Sourcing questions from PAA misses most of what the engine
actually searches.

### Stage 4 - Clustering

Group qualified keywords by head question. Minimum 4 variants to commission a
post. Below 4, hold the keyword in a backlog rather than publishing a thin post.

One URL per cluster. Never split variants across posts: that is what produced
Bedrock's 10-for-1 result.

### Stage 5 - Writer constraints

Pass to the generation prompt:

- Slug = head question verbatim, interrogative, hyphenated. No geo modifier.
- Opening block = direct answer in the first 40-60 words, ahead of any brand
  copy, CTA, or scene-setting.
- H2 per variant phrasing from the cluster.
- One H2 minimum covering cost or timeline, even on symptom posts.
  Commercial-intent AIO placements convert to buyers; Care Roofing runs 9/18
  commercial versus Bedrock's 4/31.
- Schema: FAQPage where the cluster is genuinely multi-question, Article
  otherwise. Never both.
- No em dashes in client-facing copy.

### Stage 6 - Verification loop (NEW)

Re-poll DataForSEO SERP for each target keyword 5 times across 30 days
post-publish. Log AIO citation as a rate, never as a boolean.

**Rationale:** identical repeated queries return matching cited domains only
~40-46% of the time, and the same recommended business ~7% of the time, against
~90% for Google's local pack. A single check is a sample, not a measurement.

## 3. Reporting rules (v4 HTML reports)

The AI search channel must report:

- AIO citation rate across >= 5 polls, with the poll count stated
- Keyword count on AIO-eligible SERPs (eligibility) alongside citation count
  (conversion)
- Gemini/AIO and ChatGPT as separate lines, never merged into one "AI
  visibility" figure

Do not report review velocity as an AI visibility driver. AI-recommended
businesses average 4.75 stars against a 4.84 plain-search baseline, and citation
frequency correlates with rating at 0.013. Review work remains justified on Map
Pack and conversion grounds only.

**Client expectation to set in writing:** roughly 12% of AI results are clickable
on desktop and 28% on mobile (Shotland / Nozzle, 15.2M local searches). AIO
citation is brand exposure with weak click attribution.

## 4. Onboarding addition - vertical source audit

Source mixes are vertical-specific, not universal. Documented patterns:

| Vertical | Dominant non-owned sources |
|---|---|
| Home trades (plumbing, HVAC, electrical, pest) | Even spread: own site, general directories, some social |
| Auto repair | Most Reddit-dependent vertical measured |
| Personal injury law | Legal ranking directories (Best Law Firms, Super Lawyers, Justia). Minimal social. |
| Dentistry | Zocdoc, Healthgrades, DeltaDental |

Reddit alone takes 13.7% of citations against 10.3% for the entire local-service
directory category (Angi, Thumbtack, HomeAdvisor combined), with bootstrap
intervals that don't cross zero.

**New onboarding deliverable:** per-client cited-source audit before citation or
directory work is scoped. National directories are table stakes and
differentiate nothing: only 2.0% of businesses appeared in more than one metro,
and those were national franchises.

Community presence is a genuine channel. It is not an astroturfing instruction;
fabricated discussion carries real platform and client risk.

## 5. Rollout order

**Tier 1** - restructure existing pages (highest ROI, no new content)

- Powell's: 19 AIO-eligible keywords, 4 citations
- Conner: 40 AIO-eligible keywords, 4 AIO citations (30 lost to image pack)

Both already appear on the right SERPs. Fix the opening-block structure before
commissioning anything new.

**Tier 2** - extend the winners

- Bedrock Plumbers: add the commercial layer (cost guides, material comparisons)
- Care Roofing: extend the symptom set

**Tier 3** - zero-presence clients

- Long Island Custom Blinds, Exteriors Plus MN, Redefined Restoration, Praiano

## 6. Known limits

- Internal sample is n=4 with no control for domain authority or publishing
  volume.
- Care Roofing's 100% novelty rate may partly reflect Google expanding AIO
  coverage in roofing generally. Validate with
  `site-explorer-ai-responses-count` against 3 non-client roofing competitors
  before treating the effect size as ours.
- The Citation Ledger covers the 50 largest US metros, primarily one engine, one
  point in time. Our clients include suburban and rural markets outside that
  frame.
- Grounding behavior shifts as the underlying index changes. Re-validate this
  spec quarterly.

## 7. Standing constraints carried forward

- No OTTO projects
- No em dashes in client-facing copy
- Service page H1s carry no geographic modifier
- GBP name verified in Google, categories verified via Pleper
- PR topics checked in Ahrefs, no repeats within 6 months
- Review velocity: Windsor `google_my_business` for owned GBPs; Viktor in client
  Slack for competitors. The DataForSEO review-velocity Make scenario does not
  work, do not use it.

## Sources

Ben Fisher, "What AI Actually Cites: 14,000+ Local AI Gemini and ChatGPT Search
Citations Analyzed," Steady Demand, Aug 6 2026 -
https://www.steadydemand.com/ai-citation-ledger/

Internal: Ahrefs Site Explorer AIO segment, Aug 19 2026 vs Feb 19 2026, n=4
client domains.
