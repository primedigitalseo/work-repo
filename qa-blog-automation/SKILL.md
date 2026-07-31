---
name: qa-blog-automation
description: >-
  Prime Digital's weekly SEO+GEO Q&A blog process for local SEO clients. Use this
  whenever someone wants to research, write, or publish a Q&A blog post for a Prime
  Digital client — one client on demand or the full weekly roster. Triggers include
  "write a Q&A blog for [client]", "run the weekly Q&A blogs", "draft a question post
  for [client]", "add posts to [client]'s Q&A folder", "find blog topics for [client]",
  "do the Monday Q&A blogs", or any request to create question-style blog posts that
  answer a real search query, get saved as a Google Doc in a client's Q&A blog folder,
  and handed off to the Search Atlas app in Slack for WordPress drafting. Also use when
  scoping topics via DataForSEO (People Also Ask, search volume, or LLM/AI-visibility
  gaps) for a client blog. This skill is the single source of truth for the Q&A blog
  run — prefer it over ad-hoc blog writing so voice, structure, dedup, and the Slack
  handoff stay consistent across every client and every week.
---

# Q&A Blog Automation

Produce one question-style blog post per client that answers a real search query, is
built to rank in Google **and** get cited by AI answers (ChatGPT, Perplexity, Google AI
Overviews), then hand it off for publishing. The question **is** the title. The whole
point is to own the answer to questions buyers actually ask, in the client's local market.

This skill covers the *orchestration*. For the writing craft itself, also load the
**`seo-geo-content`** skill — this skill tells you what to research, where to save it,
and how to hand it off; that skill sharpens how the prose reads.

## When to run it

- **Single client, on demand:** "write a Q&A blog for Rembrandt" → run the flow once for
  that client. Default to one new post unless the user asks for several.
- **Full weekly roster:** "run the Monday Q&A blogs" → run the flow once per client in
  `references/roster.md`, then post all of them under one dated Slack thread.

If the client isn't in the roster, ask which client folder to use rather than guessing.

## Constants

- **Prime Digital Clients root folder:** `16LupA37Zy9ZTH3rEtC9BGYvEar_OKUKN`
- **Slack channel `#client-qa-blogs`:** `C0BG7G2PLEA`
- **Search Atlas Coworker app (tag to trigger WordPress drafting):** `<@U0BCP3ZGWSV>`
- **Gold-standard example (read it before writing your first post):** Google Doc
  `1WUam2Ge7R738WbRfeo3ppmjbr79a1d6KqYk6pzPHHhI` ("Bedrock Q&A Blog Example")
- **Roster + per-client Q&A folder IDs and CMS notes:** `references/roster.md`
- **DataForSEO endpoints, auth, and gotchas:** `references/dataforseo.md`

## The flow (per client)

### 1. Confirm the client and folder
Look up the client in `references/roster.md` to get the market, service, and Q&A folder
ID. Note any CMS exception (see Squarespace, below).

### 2. Dedup — read what's already covered
List the existing Google Docs in the client's Q&A folder
(`search_files` with `parentId = '<folder id>'`). **Every existing doc title is a covered
topic.** Pick a new topic that isn't already there. If a "Q&A Topics Log" doc exists,
read it too. This is what keeps the weekly run from repeating itself.

### 3. Research with DataForSEO
Full details in `references/dataforseo.md`. The method:
- Pull **People Also Ask** for a few question seeds in the client's niche + market. These
  become your H2s.
- Pull **Google Ads search volume** for the candidate queries.
- Optionally run an **LLM Responses** check (AI-visibility) to see which competitors get
  cited for a buyer prompt and where the client is absent.
- **Filter out commercial/navigational head terms** ("[service] near me", "[service]
  [city]", bare product names). Those are service-page work, not Q&A. Keep the
  *question* queries.
- **Title = the highest-volume question query**, localized (append "in [City/State]" or
  "for [City] Homes" the way the gold-standard example does). Prefer topics where there's
  an AI-visibility gap (competitors cited, client not).

### 4. Write the post (SEO+GEO framework)
Match the Bedrock gold-standard example. Load `seo-geo-content` for the prose. Structure:
- **H1 = the exact search query** (the question, with local modifier).
- **Cite-ready lead, 40 to 60 words:** a direct, quotable answer with a clear position
  and one qualifier. Written so an AI can lift it verbatim and attribute it to the client.
- **PAA-driven H2s:** each section header is a real People-Also-Ask question.
- **Answer-first + definitive:** state the answer, then support it. Avoid "it depends"
  without a concrete range right after.
- **Real local entities:** actual city names, neighborhoods, roads, landmarks, hospitals,
  utilities for the client's market. This is the moat national content can't copy.
- **Sourced statistics only when real and attributable** (e.g., U.S. Department of Energy,
  a state DMV, CPSC). Never invent a cited stat. Ranges may be given as typical estimates,
  clearly framed as estimates.
- **FAQ section (4 Q&As)** for FAQPage schema. The schema JSON-LD is applied at the
  WordPress step, so it does not need to live in the doc body (match the gold standard).
- **Internal-link lines** at the end (Related services / More from the blog) as plain
  text; real URLs get wired at the WordPress step.

### 5. Voice rules (non-negotiable)
- **Never use em dashes (—) in content.** Also avoid en dashes (–) in ranges; write "10
  to 15" and "$30 to $120" instead. Hyphens in compound words (faux-wood, no-fault) are
  fine.
- **Kill-list — never use:** delve, comprehensive, landscape, "in today's world."
- Use specific numbers and real examples. Pass the "would I say this out loud to a smart
  friend" test.
- After saving, **read the doc back and confirm there are no em dashes** before handing
  off. This is the rule most likely to slip through, so verify it every time.

### 6. Save as a Google Doc
Create the doc with `create_file`, `contentMimeType: "text/html"`, `textContent` = the
HTML body (h1/h2/h3, lists, bold). Title it with the question. `parentId` = the client's
Q&A folder ID. The `fileSize:1` in the response is a harmless creation-time quirk; verify
by reading the doc back.

Append the topic to the client's Q&A Topics Log if one is being maintained. Note: the
Google Drive connector is often **create-only** (no in-place edit). If you can't append,
rely on step 2's folder listing as the dedup source of truth and say so.

### 7. Slack handoff
All of a run's posts go under **one dated parent message**, with each client as a
threaded reply.
- **Parent message:** `*Mon M/D Client Q&A Blogs*` using the date of the run's Monday
  (America/New_York). Reuse the same thread for every client in the run (set `thread_ts`
  to the parent's `ts`).
- **Per-client reply (WordPress clients):** tag the app and give the client + doc link:
  ```
  <@U0BCP3ZGWSV> ready to draft into WordPress:

  • *Client Name* — Post Title
     https://docs.google.com/document/d/<doc id>/edit
  ```
- The app tag is what triggers Search Atlas to draft the post into the client's WordPress
  as a **draft** (not published).

## CMS exceptions

Some clients are not on WordPress, so the app can't auto-draft for them. Check the CMS
column in `references/roster.md`.

- **Squarespace (Winkler Kurtz):** the Squarespace API only exposes Commerce operations,
  so there's no way to auto-draft a blog post. Do everything else normally (research →
  write → save Doc), but in Slack **do not tag the app** for this client. Post the line
  flagged for manual paste instead:
  ```
  ⚠️ *Squarespace client — manual paste, no WordPress draft* (not tagging the app)

  • *Winkler Kurtz LLP* — Post Title
     https://docs.google.com/document/d/<doc id>/edit
  ```
  A human copies the Google Doc into the Squarespace blog editor.

## Legal / regulated clients

For law firms, medical, or financial clients, stick to well-established facts (statutes,
regulations, agency rules) stated plainly, and add a short "general information, not
[legal/medical/financial] advice" line at the end. Flag that a licensed professional at
the client should review before publishing.

## Scheduling note

This skill is the recipe. To run it automatically every Monday 8:00 AM America/New_York,
point a **Claude Code Remote trigger** (create_trigger, fresh session per fire) at it with
a thin prompt like: "Load the qa-blog-automation skill and run the full roster." Grant the
fired session the **Google Drive**, **Slack**, and **Search Atlas MCP** connectors, and
make sure `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` are present. Do not use local cron.
