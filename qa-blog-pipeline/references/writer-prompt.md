# Stage 5: The writer prompt

Paste-ready. Fill the bracketed fields from the cluster's backlog record. Voice
and quality rules from `seo-geo-content` still apply, except that its
PAA-sourced research and H2 instructions are replaced by the fan-out phrasings
below.

## Fill these first

| Field | Source |
|---|---|
| `[CLIENT]`, `[SERVICE]` | Client record |
| `[HEAD QUESTION]` | Backlog: head question |
| `[FAN-OUT PHRASINGS]` | Backlog: Stage 3 fan-out list, verbatim |
| `[CITED DOMAINS]` | Backlog: currently-cited domains |
| `[SCHEMA TYPE]` | FAQPage if genuinely multi-question, else Article |

## The prompt

```
Write a Q&A blog post for [CLIENT], a [SERVICE] company.

HEAD QUESTION: [HEAD QUESTION]

This post targets Google AI Overviews. It will be judged on whether the AI
Overview cites it, so the structure below is not stylistic preference. Follow
it exactly.

OPENING BLOCK (hard requirement)
Open with the direct, complete answer to the head question in the first 40 to
60 words. Nothing precedes it: no brand introduction, no "if you have ever
noticed", no CTA, no scene-setting, no restating the question. A reader who
stops after two sentences has their answer. Write it so it can be lifted out
and quoted on its own without any surrounding context.

BODY STRUCTURE
Write one H2 for each of these phrasings, using the wording exactly as given:
[FAN-OUT PHRASINGS]

These are the queries the AI Overview actually resolved. Do not rewrite them
into smoother headings, do not merge two into one, and do not add H2s that are
not on this list, with the single exception below.

COST OR TIMELINE (hard requirement)
Include at least one H2 covering what it costs or how long it takes, even if
this is a symptom post and none of the phrasings above ask for it. Give real
ranges and name what moves the number. Commercial-intent placements are the
ones that convert to buyers.

Under each H2, lead with the answer to that heading in the first sentence, then
support it. Same rule as the opening block, applied per section.

WHAT WE ARE COMPETING WITH
These domains currently own this answer: [CITED DOMAINS]
Be more specific than they are. Concrete numbers, real ranges, actual failure
causes, the thing a technician would say. Generic advice does not displace an
incumbent citation.

VOICE
Write like the most experienced [SERVICE] tech in the shop explaining it to a
homeowner who is worried about the bill. Plain words. No hedging, no filler, no
"in today's world". Do not pad to hit a length.

HARD CONSTRAINTS
- No em dashes anywhere. Not one. Use commas, colons, or separate sentences.
- No geographic modifier in the title or headings.
- Do not open with the brand name.
- One CTA, at the very end, after the content has done its job.
- Schema: [SCHEMA TYPE] only. Never both FAQPage and Article on one post.

OUTPUT
Title: [HEAD QUESTION] exactly as written, interrogative, no geo modifier.
Then the body with H2s.
```

## After generation

**Filename and title.** Save the Google Doc named exactly the head question.
Where the handoff into WordPress reads a Doc filename, that filename becomes the
post title and WordPress derives the slug from it, so the filename is the slug.
No client name, no "Blog -" prefix, no date, no geo modifier, no "(2026 Price
Guide)" style suffix. A trailing question mark is fine, WordPress drops it from
the slug.

**Em dash sweep.** Google Docs autocorrects a double hyphen into an em dash as
you type, so a prompt instruction alone does not hold. Search the doc for the
character before it goes in the folder.

**Schema.** Confirm what the site's SEO plugin already outputs for posts before
adding anything. Most of these sites run Yoast, which emits post schema on its
own, and adding FAQPage on top is how a post ends up carrying both. Never deploy
this through OTTO.
