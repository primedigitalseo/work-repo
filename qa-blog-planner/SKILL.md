---
name: qa-blog-planner
description: "Plan a prioritized Q&A blog content calendar of up to 12 posts for a local SEO client, clustered by topic and sequenced by combined search/AI volume and buyer intent, built for LLM/GEO citation. Use when someone wants to plan blogs (not write them yet): 'plan the blogs for [client]', 'build a content calendar', 'give me 12 blog topics', 'blog planner for [client]', 'topical map for [client]', 'what should [client] blog about', or 'scope a quarter of Q&A posts'. This is the UPSTREAM planning step that feeds qa-blog-automation (which writes each post). It outputs a calendar (Google Sheet), it does not write the posts."
---

# Q&A Blog Planner

Produce a prioritized content calendar of **up to 12** Q&A blog titles for one client:
clustered by topic, sequenced by combined volume and buyer intent, and built to get cited
by AI answers (ChatGPT, Perplexity, Google AI Overviews). The planner decides *what to
write and in what order*. The **`qa-blog-automation`** skill then writes each post; the
**`seo-geo-content`** skill governs the prose and voice. This skill stops at the plan.

The gold-standard output is the Bedrock "Water Damage Q&A Blog Content Calendar (LLM /
GEO)" sheet: a ranked table of 12 titles plus a query bank and a reusable GEO checklist.
Match that shape.

## When to run it

- "Plan the Q&A blogs for [client]" or "build [client] a content calendar" -> run once,
  produce one planner of up to 12 rows.
- Default to **12**. Do fewer only if asked, or if research does not surface 12 distinct,
  non-overlapping topics worth writing (say so rather than padding).

If the client is not in `qa-blog-automation/references/roster.md`, ask which market and
service to plan for rather than guessing.

## Constants

- **Roster (market, service, Q&A folder, CMS):** `qa-blog-automation/references/roster.md`
- **DataForSEO research method (auth + endpoints):** `qa-blog-automation/references/dataforseo.md`
- **Prime Digital Clients root folder:** `16LupA37Zy9ZTH3rEtC9BGYvEar_OKUKN`
- Save the planner in the client's **Content › Content Workflow** area (the parent of their
  "[Client] New Q&A Blogs" Q&A folder). If you cannot resolve that parent, save it into the
  Q&A folder itself and say so.

## The flow

### 1. Confirm client, market, service
Look up the client in the roster for market, service, and Q&A folder ID. Note the CMS.

### 2. Dedup against what exists
List the client's Q&A folder (`search_files` with `parentId = '<folder id>'`). Every
existing doc title is a covered topic. If a prior planner sheet exists, read it too. The
new plan must not repeat topics already written or already planned.

### 3. Research (DataForSEO)
Full method in `dataforseo.md`. For a planner you run a **wider** pass than for a single
post:
- **People Also Ask** across 5 to 8 seed queries spanning the whole service (cost,
  insurance, emergency, hiring, repair, definitions). Each PAA question is a candidate
  target query.
- **Search volume** on every candidate query, in one batched call (keep each keyword to 10
  words or fewer). This is your sizing metric. Where the account has **AI keyword volume**
  (ChatGPT/Gemini/Perplexity monthly), prefer it and label the column "mo. AI vol"; use
  Google Ads search volume as the proxy otherwise. Be explicit about which you used.
- **LLM Responses** (optional, high value): run 2 to 4 buyer prompts and note which
  competitor domains get cited and where the client is absent. Topics with an AI-visibility
  gap (competitors cited, client not) get a priority bump.
- **Filter out** commercial/navigational head terms ("[service] near me", "[service]
  [city]", bare product names). Those are service-page work, not Q&A.

### 4. Cluster, select, and sequence
- **Cluster** the surviving queries into 5 to 8 content clusters (e.g. Cost, Insurance,
  Emergency/How-to, Hiring, Decision, Education, Repair how-to).
- **Select up to 12 titles.** Roughly **5 pillars** (the highest combined-volume, strongest
  buyer-intent clusters) and the rest **support** posts. One title owns one cluster or a
  tight query group; titles must not overlap each other.
- Each title carries its **target queries** (its future H2s) and their volumes. The
  **combined monthly volume** is the sum across that title's queries.
- **Title rule:** the title is the highest-volume *question* in its group, phrased as the
  question. Keep titles geo-neutral or lightly localized. City-level AI volume is ~0
  (people don't ask AI "water damage restoration Minneapolis"), so localization belongs
  *inside* the posts, not in standalone city titles.
- **Sequence** by priority = combined volume x buyer intent. Pillars first (Seq 1 to 5),
  then support by descending value. Map to a 2-posts-per-month cadence (12 posts = 6
  months) unless told otherwise.
- **Priority tier** each row: HIGHEST / HIGH / MEDIUM-HIGH / MEDIUM.

### 5. Voice on titles and notes
Apply the `seo-geo-content` kill-list and punctuation rules to every title and note:
**no em dashes, no en dashes in ranges** (write "8 to 12"), and never "delve",
"comprehensive", "landscape", "in today's world". Titles should read like a real question a
buyer types.

### 6. Build the calendar (Google Sheet)
Create it as a Google Sheet by uploading CSV (`create_file`, `contentMimeType:
"text/csv"`, `textContent` = the CSV; the connector converts CSV to a Sheet). Title it
"[Client] - [Service] Q&A Blog Content Calendar (LLM / GEO)". `parentId` = the client's
Content Workflow folder (or Q&A folder as fallback). Verify by reading it back.

**Columns (match the gold standard):**
`Seq | Month | Type | Blog Title | Primary Cluster | Funnel Stage | Target Queries (avg mo. vol) | Combined mo. vol | Priority | Notes / Angle`

Then add three helper blocks below the table:
1. **TOTAL addressable volume/mo** (sum of the Combined column).
2. **HOW TO USE THIS CALENDAR** — build pillars first; give every target sub-question its
   own H2 with a 2 to 3 sentence direct answer up top; add FAQPage schema to every post;
   interlink support -> pillar -> service/contact; localize inside the posts.
3. **LOCAL GEO SIGNALS TO INCLUDE IN EVERY POST** — service-area mentions in the intro and
   an FAQ, state-specific facts, local price ranges, LocalBusiness + FAQPage schema,
   consistent NAP, one local proof point, an internal link to the localized service page.
4. Optionally a **TOP QUERIES** bank: the full ranked query list with cluster and volume,
   so the writer has the raw material when drafting.

### 7. Hand off to writing
The planner is the input to `qa-blog-automation`. Once approved, run that skill per row to
write and save each post (exactly how the Bedrock 12-post batch was produced from its
sheet). Optionally drop the planner link in the client's channel or `#client-qa-blogs` for
sign-off before writing begins. Do not write the posts inside this skill.

## Legal / regulated clients
For law, medical, or financial clients, keep planned topics to well-established facts
(statutes, regulations, agency rules) and flag in the Notes column that a licensed
professional must review each post before publishing.

## Scheduling note
Run this quarterly (or when a client's Q&A backlog runs low) to refill the pipeline, then
let `qa-blog-automation` work down the list weekly.
