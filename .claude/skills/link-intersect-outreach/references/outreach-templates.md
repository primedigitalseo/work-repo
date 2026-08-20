# Outreach Templates

## The principle

The body is static and reviewed by a human once. Only the opening line is
generated per lead. This keeps quality controllable at 400 sends and keeps
cost under a penny a lead — and it reads more human than full generation,
because fully generated bodies converge on the same handful of adjectives and
recipients have learned to spot that.

## Opening-line generation

One call per lead. Prompt:

```
You are writing ONE sentence — the opening line of a cold email to the author
of this page.

PAGE TITLE: {page_title}
PAGE URL: {linking_page_url}
THEY LINKED TO: {competitor_url}
ANCHOR TEXT USED: {anchor}
PAGE EXCERPT: {first_500_words}

Write one sentence that shows you actually read this specific page. Reference
the link they included or a concrete detail from the page. No compliments, no
"great article," no "I loved your piece." Do not pitch anything — the next
line of the email does that.

Return only the sentence, and it must quote at least four consecutive words
that appear verbatim in the page title or excerpt.
```

**Validate before sending.** Check that the returned line contains a ≥4-word
verbatim substring from `page_title` or `first_500_words`. On failure, fall
back to:

```
Saw you linked to {competitor_domain} in "{page_title}".
```

That fallback is still specific and true. Around 10% will fail validation, and
those were the emails most likely to embarrass you.

## Body — Template A: the data/asset offer

Best for archetypes that publish cost, comparison, or how-much content.

```
{generated_opening_line}

I work with {client_name}, a {client_descriptor} in {client_metro}. We have
{specific_asset} — {asset_detail} — that would slot into that piece as a
regional data point.

Happy to send it over as a table you can drop in, no strings. If it's useful
and you want to credit us, great; if not, keep it anyway.

{sender_name}
{sender_title}, {client_name}
{physical_address}
{unsubscribe_link}
```

`specific_asset` must be real and must exist before the campaign sends. Real
options: actual project cost data across N builds, permit/timeline data for a
region, original photography, a materials comparison from real jobs. If the
client has none of these, build one first — the campaign is worth roughly
nothing without it.

## Body — Template B: the resource addition

For roundups, resource pages, and "best of" lists.

```
{generated_opening_line}

Quick one — that list doesn't have anyone covering {geo_or_niche_gap}.
{client_name} has been doing {service} in {metro} since {year}
({credibility_marker}).

Worth a look for the list? Either way, {genuine_useful_note_about_their_page}.

{sender_name}
{sender_title}, {client_name}
{physical_address}
{unsubscribe_link}
```

`genuine_useful_note_about_their_page` — a broken link, an outdated figure, a
company on the list that closed. Find it during the byline scrape. It is the
single highest-converting element in either template because it costs you
something and gives them something.

## Follow-up

One follow-up, four business days later, threaded. Never more than one — a
second follow-up on cold outreach converts near zero and materially raises
spam complaints.

```
Bumping this once in case it got buried — no worries at all if it's not a fit.

{one_line_restating_the_specific_offer}
```

## Subject lines

Specific and lowercase-plain beats clever. Rotate across a campaign:

- `your {topic} piece`
- `{competitor_domain} link in your {topic} post`
- `regional data for your {topic} guide`
- `small fix on {page_title_short}`

Never use fake-reply prefixes (`Re:`, `Fwd:`), fake urgency, or the recipient's
first name alone as the subject. All of them raise open rate slightly and reply
rate not at all, while training people to distrust the sender.

## Reply handling

Route replies to a monitored human inbox, not an automation. Buckets:

- **Interested / send it** — send the asset within 24 hours. Speed matters more
  than polish here.
- **"We charge $X"** — a real outcome, not a failure. Log the price in the
  suppression table notes. Compare against Semantic Links pricing before
  accepting; many are worth it at $150–250 and not at $400+.
- **Not a fit** — mark `negative`, permanent suppression, reply thanking them.
- **Angry / unsubscribe** — suppress permanently, do not reply beyond
  confirming removal.
