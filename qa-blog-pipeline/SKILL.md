---
name: qa-blog-pipeline
description: >-
  Run the weekly Q&A blog content process for Prime Digital SEO clients under
  the AIO Content Pipeline Spec v1.0. Use whenever someone asks to write, draft,
  commission, or queue a weekly Q&A blog post for any client, picks the next
  question to write, builds or refills a client's Q&A question backlog, or asks
  things like "write this week's Q&A blog for [client]", "what question are we
  writing for [client]", "run the Q&A blogs", "qualify these keywords", "which
  questions passed the gate", "check if we got cited", or "why isn't [client]
  showing up in AI Overviews". Also trigger on AIO qualification, citation-gap
  extraction, question clustering, the verification polling loop, or reporting
  AI search results for the Q&A channel. This skill governs ALL question
  selection and Q&A blog writing decisions and replaces PAA-sourced question
  selection everywhere it appears in `seo-geo-content`.
---

# Weekly Q&A Blog Pipeline (AIO)

The operating procedure for the weekly Q&A blog program. It targets **Google AI
Overviews and Gemini**. It is not a ChatGPT visibility play.

Source of record: `references/aio-pipeline-spec.md` (Spec v1.0, Aug 2026, owner
Mike Amatulli). This skill is that spec turned into the week-to-week process.
When the two disagree, the spec wins and this skill gets fixed.

## What changed, and why it matters

The old process picked questions from People Also Ask and wrote them up. Three
things were wrong with that:

1. **PAA is the wrong source.** Gemini's fan-out queries overlap Google PAA
   phrasing only 12.7% on average, and 80% of fan-out queries score below 0.2
   similarity. Sourcing from PAA misses most of what the engine actually
   searches. Stage 3 replaces it with the AI Overview `references[]` array.
2. **Format alone does not work.** EverClear runs this exact pipeline and holds
   2 AIO keywords. Same format, no topic demand. Stage 2 is now a blocking gate,
   not a suggestion.
3. **A single SERP check is a sample, not a measurement.** Identical repeated
   queries return matching cited domains only ~40-46% of the time. Stage 6 logs
   a rate across 5 polls, never a boolean.

This skill overrides `seo-geo-content` wherever that skill says to source H2s or
research from PAA. Its voice and quality rules still apply.

## Never do these

- **Never scope this work to a client as "AI visibility" without naming the
  engine.** It is Google AI Overviews and Gemini. ChatGPT visibility is a
  separate workstream (vertical communities and vertical directories) and this
  pipeline does not move it. Cited-domain overlap between the two engines is 8%.
- **Never write a question that did not come off the qualified backlog.** No
  ad-hoc topics, no client suggestions straight to draft, no "this seems useful."
  Everything passes Stage 2 first.
- **Never commission a post for a cluster with fewer than 4 variants.** Hold it
  in the backlog. A thin post spends the URL for nothing.
- **Never split a cluster's variants across two posts.** One URL per cluster.
  Not splitting is what let one Bedrock post hold 10 keywords.
- **Never report AIO citation as yes/no.** Rate, with the poll count stated.
- **Never deploy the post's schema through OTTO.** No OTTO projects is a
  standing constraint. Schema goes in through the site's own setup.
- **Never use em dashes in client-facing copy.**

## The cadence

The spec reads as one pipeline. In practice it runs on three clocks. Do not try
to run a blocking DataForSEO gate inline against a Monday deadline.

| Clock | Work | Stages |
|---|---|---|
| Quarterly, per client | Build and refill the qualified cluster backlog | 1-4 |
| Weekly, per client | Commission, write, QA, ship one post | 5 |
| Weekly, all clients | Run the polls that came due | 6 |
| Monthly, per client | Report the channel | Section 3 |

The weekly writing job draws from a backlog that was already qualified. If the
backlog is empty, the answer is to run Stages 1-4, not to invent a question.

## Backlog build (quarterly, per client)

Full procedure and the exact DataForSEO call: `references/qualification-gate.md`.

**Stage 1: Discovery.** Keywords Everywhere `related` + `pasf` endpoints per
service line. Search volume only. No CPC, no competition data.

**Stage 2: AIO qualification gate (blocking).** For every candidate, call
DataForSEO `serp/google/organic/live/advanced` and read `item_types`. Rejects are
evaluated first and beat a qualify:

```
REJECT    if 'images' in item_types        # Conner failure mode
REJECT    if volume < 150 on the head term # EverClear failure mode
QUALIFY   if 'ai_overview' in item_types
```

Then classify by phrasing.

- **Accept:** Symptom ("why does my X", "what causes X", "is it normal for X"),
  Duration ("how long does X take"), Cost ("how much does X cost", "X cost
  per"), Procedure ("do I need to X before Y", "can you reuse X").
- **Reject:** definition and spec phrasing ("what is X", "X dimensions", "X
  chart"). These lose to image packs.

**Stage 3: Citation-gap extraction.** Pull `references[]` off the AI Overview
block for every qualified keyword and build two lists per cluster:

- **Currently-cited domains.** Who owns the answer today. If a direct competitor
  appears, the keyword is a displacement target and moves up the queue.
- **Fan-out phrasings.** The queries the AI Overview actually resolved. These
  become the H2s. This is the PAA replacement.

**Stage 4: Clustering.** Group by head question. Minimum 4 variants to
commission. One URL per cluster. Below 4 variants it stays in the backlog.

Backlog output per cluster: head question, variant list, head-term volume,
currently-cited domains, fan-out phrasings, displacement flag.

The backlog lives on the client's Q&A Content Calendar (LLM/GEO) sheet, which
today carries volume but no gate evidence. The columns to add, and a worked
audit of the current Care Roofing calendar against this spec, are in
`references/content-calendar.md`.

## The weekly write (per client)

### 1. Take the next cluster
Highest-priority cluster off the client's backlog. Displacement targets (a
direct competitor is currently cited) outrank the rest. Never pick by feel, and
never write a cluster already covered by an existing post: check the client's
published Q&A set first and extend the existing URL instead if one covers it.

### 2. Pre-flight
If the cluster was qualified more than 90 days ago, re-run the Stage 2 gate on
the head term before writing. Grounding behavior shifts as the index changes,
and an `images` pack can arrive on a SERP that did not have one. Re-validate the
whole spec quarterly.

### 3. Write to the Stage 5 constraints
Paste-ready prompt: `references/writer-prompt.md`. The binding constraints:

- **Slug = head question verbatim, interrogative, hyphenated. No geo modifier.**
- **Opening block = the direct answer in the first 40-60 words**, ahead of any
  brand copy, CTA, or scene-setting.
- **One H2 per variant phrasing** from the cluster, using the Stage 3 fan-out
  wording, not invented paraphrases.
- **At least one H2 covering cost or timeline**, even on a symptom post.
  Commercial-intent AIO placements convert to buyers: Care Roofing runs 9/18
  commercial against Bedrock's 4/31.
- **Schema: FAQPage** where the cluster is genuinely multi-question, **Article**
  otherwise. **Never both.** Check what the site's SEO plugin already emits for
  posts before adding anything, so the post does not end up carrying both.
- **No em dashes.** Google Docs autocorrects a double hyphen into one, so this
  needs an actual check, not an intention.

### 4. QA gate (blocking)
Every line is a failure mode we have already paid for. See
`references/qa-checklist.md` for the full version.

- [ ] Question came off the qualified backlog
- [ ] Cluster has 4+ variants, all covered in this one post
- [ ] Head term volume >= 150, no `images` in `item_types`
- [ ] Direct answer complete within the first 40-60 words
- [ ] No brand copy, CTA, or scene-setting above that answer
- [ ] One H2 per fan-out phrasing
- [ ] Cost or timeline H2 present
- [ ] Exactly one schema type, FAQPage or Article
- [ ] Zero em dashes
- [ ] No geo modifier in the slug or H1

### 5. Ship it
Save the draft into the client's Q&A blog Drive folder and update its row on the
client's **Q&A Content Calendar (LLM/GEO)** sheet. Approval runs through the
client's Slack channel and then the client's recurring ClickUp approval task.
Calendar structure and the gate columns it needs: `references/content-calendar.md`.

**The slug rule binds wherever the handoff happens.** Whatever carries the draft
into WordPress, the published title is the head question verbatim and the slug
matches it: interrogative, hyphenated, no geo modifier, no "(2026 Price Guide)"
style suffix. Where the handoff reads a Google Doc filename, the filename
becomes the title and therefore the slug, so name the Doc the head question and
nothing else.

**Legacy note.** The per-client "[Client] Q&A Blogs to Wordpress" Make scenarios
are not the current path. Five of seven are deactivated; the two still flagged
active (EverClear, Rembrandt) have not been edited since Dec 2025 and carry no
execution history, and none of the Tier 1 or Tier 2 rollout clients has one. If
one is ever revived: it posts the Drive filename as the WordPress title and has
no move-or-archive step, so any Doc left in the folder reposts on the next run.

### 6. Register it for verification
On publish, add the URL to the client's verification log with its five poll
dates. A post that is not in the log does not get measured, and an unmeasured
post cannot be reported.

## Verification loop (weekly sweep, all clients)

Re-poll DataForSEO SERP for each target keyword **5 times across 30 days**
post-publish. Standard schedule: **day 3, 7, 14, 21, 30**.

Log per poll: date, keyword, whether the client domain appears in the AI
Overview `references[]`, and which domains did. Report as a rate over polls run
("3/5 polls, 60%"), never as cited yes/no. Identical repeated queries return
matching cited domains only ~40-46% of the time, and the same recommended
business ~7% of the time, against ~90% for Google's local pack. One check is a
sample.

Details and the log shape: `references/verification-loop.md`.

## Reporting

Full rules and the client-expectation language: `references/reporting.md`.

The AI search channel in the v4 HTML report must carry:

- AIO citation rate across 5 or more polls, **with the poll count stated**
- Keyword count on AIO-eligible SERPs (eligibility) **alongside** citation count
  (conversion). Two different numbers, both shown.
- Gemini/AIO and ChatGPT as **separate lines**, never merged into one "AI
  visibility" figure

Do not report review velocity as an AI visibility driver. AI-recommended
businesses average 4.75 stars against a 4.84 plain-search baseline, and citation
frequency correlates with rating at 0.013. Review work stays justified on Map
Pack and conversion grounds only.

Set in writing with the client: roughly **12% of AI results are clickable on
desktop and 28% on mobile**. AIO citation is brand exposure with weak click
attribution. Say this before the first report, not after a client asks where the
traffic is.

## Rollout order

Work the queue in this order. Tier 1 is restructuring pages that already sit on
the right SERPs, which is the highest ROI available and needs no new content.

**Tier 1: restructure what exists.**
- Powell's Plumbing: 19 AIO-eligible keywords, 4 citations
- Conner: 40 AIO-eligible keywords, 4 citations (30 lost to the image pack)

Fix the opening-block structure on these before commissioning anything new.

**Tier 2: extend the winners.**
- Bedrock Plumbers: add the commercial layer (cost guides, material comparisons)
- Care Roofing: extend the symptom set

**Tier 3: zero-presence clients.**
- Long Island Custom Blinds, Exteriors Plus MN, Redefined Restoration, Praiano

## Known limits, state them when asked

Do not oversell this internally or to clients.

- The internal sample is **n=4 client domains**, with no control for domain
  authority or publishing volume.
- Care Roofing's 100% novelty rate may partly reflect Google expanding AIO
  coverage in roofing generally. Validate with Ahrefs
  `site-explorer-ai-responses-count` against 3 non-client roofing competitors
  before treating the effect size as ours.
- The Citation Ledger covers the 50 largest US metros, primarily one engine, one
  point in time. Several of our clients are suburban or rural, outside that frame.
- Grounding behavior shifts as the index changes. **Re-validate this spec
  quarterly.**

## Standing constraints carried forward

No OTTO projects. No em dashes in client-facing copy. Service page H1s carry no
geographic modifier. GBP name verified in Google, categories verified via Pleper.
PR topics checked in Ahrefs, no repeats within 6 months. Review velocity via
Windsor `google_my_business` for owned GBPs and Viktor in client Slack for
competitors: the DataForSEO review-velocity Make scenario does not work, do not
use it.
