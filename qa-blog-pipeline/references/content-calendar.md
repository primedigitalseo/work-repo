# The Q&A Content Calendar (LLM/GEO)

The per-client Google Sheet is where the backlog actually lives. Stages 1-4 fill
it; the weekly write draws from it. This file covers what it carries today, what
the gate requires it to carry, and a worked audit of the current Care Roofing
calendar.

## Columns today

`Seq | Month | Type | Blog Title | Primary Cluster | Funnel Stage | Target
Queries (avg mo. search vol) | Combined mo. vol | Priority | Notes / Angle`

Plus a HOW TO USE block, a LOCAL GEO SIGNALS checklist, and a METHOD note.

## What it already gets right

Keep these. They are not in the spec and they should be.

- **Commercial head terms filtered out** as service-page work, not Q&A. Correct
  boundary, and it keeps the pipeline from competing with its own money pages.
- **Pillar and support typing with explicit interlinking.** Support links up to
  its pillar, pillar links to the service page.
- **Localizing inside the post while the title stays geo-neutral.** This is the
  right reading of the no-geo-modifier rule, and the calendar states it.
- **Heavy cost and timeline coverage.** Six of twelve rows are cost or timeline,
  which is the commercial-intent bias the spec asks for.

## Columns the gate requires

`Combined mo. vol` is not the gate. The gate runs on the **head term**, on
`item_types`, and on phrasing. Add:

| Column | Fills at | Holds |
|---|---|---|
| Head term | Stage 2 | The one term the volume floor is tested against |
| Head-term vol | Stage 2 | Must be >= 150 |
| `item_types` | Stage 2 | Raw list from DataForSEO |
| Gate verdict | Stage 2 | QUALIFY / REJECT-images / REJECT-volume / REJECT-phrasing |
| Phrasing class | Stage 2 | Symptom / Duration / Cost / Procedure, or the reject reason |
| Cited domains | Stage 3 | Who owns the AI Overview today |
| Displacement | Stage 3 | Yes if a direct competitor is cited |
| Fan-out phrasings | Stage 3 | The H2 set, verbatim. Replaces the (PAA) entries |
| Variant count | Stage 4 | Must be >= 4 to commission |
| Qualified on | Stage 4 | Triggers the 90-day re-check |
| Published URL | Stage 5 | |
| Poll 1-5 | Stage 6 | Cited yes/no per poll, then the rate |

`Combined mo. vol` stays as a sizing number. It is not a gate and a row must
never qualify on it: a cluster of four 10/mo terms sums to 40 and is exactly the
EverClear failure mode.

## Two lines to change in the HOW TO USE block

**"Add FAQPage schema to every post."** Spec Stage 5: FAQPage where the cluster
is genuinely multi-question, Article otherwise, **never both**. "Every post"
guarantees FAQPage on single-question posts, and stacking it on top of what the
site's SEO plugin already emits is the exact double-schema failure the rule
exists to prevent. Change to: FAQPage only where the cluster is genuinely
multi-question, checked against existing plugin output.

**"the biggest single lever for citation in ChatGPT, Perplexity, and AI
Overviews."** Spec §0: this pipeline targets AI Overviews and Gemini and does
not move ChatGPT. Cited-domain overlap between the engines is 8%, and ChatGPT
cites the business's own site 15.9% of the time against Gemini's 59.9%,
favoring forums (41.7%) and directories (34.6%). Promising ChatGPT lift from
on-site Q&A sets up a miss. Change to: AI Overviews and Gemini, and scope
ChatGPT separately.

## Worked audit: Care Roofing calendar (2026-08-20)

Twelve rows, sent for approval. No row carries gate evidence: the METHOD note
records volume pulled via DataForSEO but no `item_types` check, so Stage 2 has
not run on any of them. Verdicts below are what the gate would return on the
listed data. They are not a re-scoping of the calendar, which is a good piece of
work, but the rows need the gate before they are commissioned.

| Seq | Title | Would flag |
|---|---|---|
| 1 | How Long Does a Roof Last in the Desert? | Geo modifier in title. 3 variants. Volume strong (12,100). |
| 2 | How Much Does a New Roof Cost in Palm Desert? (2026 Price Guide) | Geo modifier plus a non-interrogative suffix; slug will not be the head question. 2 variants. |
| 3 | How Much Does a Tile Roof Cost (and Is It Worth It)? | Only row with 4 variants. But the cost head terms are 70 and 50, under the floor; it clears only if "how long does a tile roof last" (1,000) is declared the head, which makes it a lifespan post, not a cost post. Declare the head term. |
| 4 | Tile Roof vs. Shingle Roof: Which Is Better for the Desert? | Comparison phrasing is not an accepted class. Geo modifier. High image-pack risk: materials comparisons are where Conner lost 30 of 40. |
| 5 | What Is a Cool Roof, and Is It Worth It in the Desert? | "What is X" is the explicit reject class. Geo modifier. Volume (480) does not rescue phrasing. |
| 6 | How Much Does a Flat Roof Cost to Replace? | Clean Cost phrasing, 1,000 head. 3 variants. |
| 7 | How Much Does a Metal Roof Cost? | Clean Cost phrasing, 3,600 head. 1 variant. |
| 8 | How Long Does It Take to Replace a Roof? | Clean Duration phrasing, 1,600 head. 1 variant. |
| 9 | Do You Need a Permit to Replace a Roof in California? | Clean Procedure phrasing. Geo modifier (California). 1 variant. |
| 10 | Signs You Need a New Roof | Not interrogative, so the slug cannot be a head question. Listicle shape carries image-pack risk. 2 variants. |
| 11 | Is Foam Roofing Worth It? | **Hard reject on volume.** All three terms are 10/mo, 30 combined, against a 150 floor. This is the EverClear failure mode exactly: real topical authority, no demand. |
| 12 | How Much Does a Roof Inspection Cost? | Clean Cost phrasing, 260 head. 1 variant. |

### Summary

- **Gate evidence missing on all 12.** No `item_types` pull, so no row is
  qualified yet.
- **11 of 12 are under the 4-variant minimum as listed.** This is the least
  alarming finding: the calendar lists target queries, not the Stage 3 fan-out
  set. Running citation-gap extraction is what lifts these over the line, and it
  is the step that has not run.
- **4 rows still source variants from PAA** (marked "(PAA)" on Seq 1, 3, 10, 11).
  Stage 3 replaces those entries with fan-out phrasings.
- **5 rows carry a geo modifier in the title** (1, 2, 4, 5, 9), against the
  calendar's own instruction to keep titles geo-neutral.
- **3 rows fail the phrasing classifier** (4 comparison, 5 definition, 10
  listicle).
- **1 hard volume reject** (11).

### Suggested order of operations

1. Run Stage 2 on the 12 head terms. One DataForSEO pass, fills four columns.
2. Drop Seq 11. Re-phrase or drop 4, 5, 10.
3. Run Stage 3 on what survives; replace the (PAA) entries with fan-out
   phrasings and record cited domains.
4. Re-check variant counts against the 4-minimum; hold anything short.
5. Strip geo modifiers and suffixes from the titles. Localize in the body, which
   the calendar already calls for.
6. Fix the two HOW TO USE lines above.
