# DataForSEO — Research Reference

DataForSEO is called over **direct HTTPS with curl**, not an MCP connector. Credentials
are environment variables, so they carry into scheduled/headless runs as long as the
environment provides them.

## Auth

```bash
AUTH=$(printf '%s:%s' "$DATAFORSEO_LOGIN" "$DATAFORSEO_PASSWORD" | base64 | tr -d '\n')
# then: -H "Authorization: Basic $AUTH"
```

Sanity-check access + balance with `GET https://api.dataforseo.com/v3/appendix/user_data`
(look at `result[0].money.balance` and `llm_mentions_subscription_expiry_date`).

## 1. People Also Ask (→ your H2s)

`POST https://api.dataforseo.com/v3/serp/google/organic/live/advanced`

```json
[{"keyword":"how much do custom blinds cost","location_name":"New York,New York,United States","language_code":"en","depth":10}]
```

- **One task per request.** The live endpoint rejects multiple tasks in the array
  ("You can set only one task at a time"). Loop over seeds, one call each.
- Localize with `location_name` (nearest city) or bake the geo into the keyword.
- Parse: walk `tasks[0].result[0].items`; for `type == "people_also_ask"`, each
  `items[].title` is a question. Also grab `type == "related_searches"` for more angles.
- Cost is ~$0.002 per call.

## 2. Search volume (→ pick the title)

`POST https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live`

```json
[{"location_code":2840,"language_code":"en","keywords":["how much do custom blinds cost","are motorized blinds worth it","blinds vs shades"]}]
```

- `location_code` 2840 = United States. Use national volume for informational queries.
- **Max 10 words per keyword.** One over-length keyword fails the WHOLE task with a 40501
  error, so keep every phrase to 10 words or fewer.
- Parse: `tasks[0].result[]` → each row has `keyword`, `search_volume`, `competition`,
  `cpc`. Null `search_volume` means no measurable volume — drop it.
- Cost is ~$0.09 for a batch.
- **Pick the highest-volume _question_ query as the title.** Explicitly discard
  commercial/navigational head terms ("[service] near me", "[service] [city]", bare
  product names) — those are service-page work, not Q&A, and the client usually already
  ranks/gets cited for them.

## 3. LLM Responses (AI-visibility gap, optional but valuable)

`POST https://api.dataforseo.com/v3/ai_optimization/chat_gpt/llm_responses/live`

```json
[{"user_prompt":"Who is the best roofing company in Springboro, OH?","model_name":"gpt-5.1","web_search":true,"max_output_tokens":2000}]
```

- Use a current model with web search (e.g. `gpt-5.1`) so it mirrors what a real buyer
  sees. Confirm valid models at `.../ai_optimization/chat_gpt/llm_responses/models`.
- Parse: `tasks[0].result[0]`:
  - `items[]` where `type == "message"` → `sections[].text` is the answer,
    `sections[].annotations[]` are the cited pages (`title`, `url`).
  - `fan_out_queries[]` = the sub-queries the model actually searched (great topic seeds).
- The gap you're mining: questions/fan-out queries where **competitor domains appear in
  the citations but the client's does not**. Those are the highest-leverage Q&A topics.
- Cost is ~$0.03–0.04 per call.

## Cost expectation

A full research pass for one post is roughly **$0.10** (PAA + volume + one LLM check). At
25 posts/week that's a few dollars — negligible relative to account balance. Still, don't
run redundant calls: batch volume keywords, and reuse PAA across related seeds.
