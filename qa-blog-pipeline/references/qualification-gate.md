# Stages 1-4: Building the qualified backlog

Run this per client, per service line, quarterly. Output is a ranked cluster
backlog that the weekly writing job draws from. Nothing gets written that did
not come through here.

## Stage 1: Discovery

Keywords Everywhere `related` and `pasf` endpoints, one pass per service line.

Return **search volume only**. Do not pull CPC or competition data: it is not
used by any downstream gate and it invites picking topics on commercial gut feel
instead of on the gate.

Output: a candidate universe per service line.

## Stage 2: AIO qualification gate (blocking)

For every candidate, call DataForSEO:

```
POST https://api.dataforseo.com/v3/serp/google/organic/live/advanced
[{
  "keyword":       "<candidate>",
  "location_code": <client market>,
  "language_code": "en",
  "device":        "desktop"
}]
```

Read `tasks[].result[].item_types`. Evaluate rejects first: a reject beats a
qualify, so a SERP carrying both `ai_overview` and `images` is rejected.

```
REJECT    if 'images' in item_types          # Conner failure mode
REJECT    if volume < 150 on the head term   # EverClear failure mode
QUALIFY   if 'ai_overview' in item_types
```

The volume floor applies to the **head term of the cluster**, not to every
variant. Long-tail variants under 150 are fine and expected; they are why the
cluster is worth a URL. What is not fine is a cluster whose head term cannot
clear 150.

### Why each reject exists

| Reject | Evidence |
|---|---|
| `images` in `item_types` | Conner: 40 AIO-eligible keywords off one page, 30 won as image, only 4 as `ai_overview`. The image pack cannibalizes the AIO slot on spec queries. |
| volume < 150 on head term | EverClear runs this identical pipeline and holds 2 AIO keywords. The format was never the problem. Topic demand was. |

### Phrasing classifier

Applied to everything that survives the reject rules.

| Verdict | Class | Patterns |
|---|---|---|
| Accept | Symptom | "why does my X", "what causes X", "is it normal for X" |
| Accept | Duration | "how long does X take" |
| Accept | Cost | "how much does X cost", "X cost per" |
| Accept | Procedure | "do I need to X before Y", "can you reuse X" |
| Reject | Definition | "what is X" |
| Reject | Spec | "X dimensions", "X chart", "X sizes" |

Definition and spec phrasing loses to image packs. It reads like useful content
and it is the exact shape that produced Conner's 30-to-4 result.

## Stage 3: Citation-gap extraction

This replaces PAA as the question source. It is the most valuable step in the
build, and the easiest to skip because it takes another parse pass.

The AI Overview block in the DataForSEO response carries a `references[]` array.
Pull it for every qualified keyword and build two lists per cluster.

**Currently-cited domains.** Who owns the answer today, from the `domain`/`url`
on each reference. If a direct competitor appears, flag the keyword as a
**displacement target**: it outranks everything else in the weekly queue,
because a citation there comes out of a competitor's share rather than out of
open space.

**Fan-out phrasings.** The queries the AI Overview actually resolved. These
become the post's H2s verbatim. Do not paraphrase them into house style: the
overlap between Gemini fan-out phrasing and Google PAA phrasing is 12.7% on
average, with 80% of fan-out queries below 0.2 similarity, so a paraphrase is
very likely to land back on the PAA wording the engine is not using.

## Stage 4: Clustering

Group qualified keywords by head question.

- **Minimum 4 variants to commission a post.** Below 4, the cluster stays in the
  backlog until discovery finds more. Do not publish thin.
- **One URL per cluster.** Never split variants across posts. One Bedrock post
  (`/why-does-my-garbage-disposal-smell-like-sewage.../`) holds 10 keywords, and
  it holds them because nothing was split off it.

## Backlog record

Per cluster, carry forward:

| Field | Use |
|---|---|
| Head question | Becomes the slug, the H1, and the Doc filename |
| Variants | One H2 each |
| Head-term volume | Gate evidence, re-checked at 90 days |
| `item_types` seen | Gate evidence, re-checked at 90 days |
| Currently-cited domains | Displacement flag, and the bar the copy has to beat |
| Fan-out phrasings | The H2 set |
| Qualified-on date | Triggers the 90-day re-check |
| Displacement flag | Queue priority |

## Re-checking

A cluster qualified more than 90 days ago gets its head term re-run through
Stage 2 before it is written. Grounding behavior shifts as the underlying index
changes, and an image pack can arrive on a SERP that did not have one when the
backlog was built.
