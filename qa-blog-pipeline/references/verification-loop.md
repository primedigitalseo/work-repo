# Stage 6: Verification loop

Every published Q&A post gets polled **5 times across 30 days**. The output is a
citation **rate**, never a boolean.

## Why a single check is not a measurement

Identical repeated queries return matching cited domains only **40 to 46%** of
the time, and the same recommended business only **~7%** of the time. Google's
local pack, by comparison, returns the same result roughly **90%** of the time.

So a single SERP check that comes back cited is roughly a coin flip, and a
single check that comes back not-cited is not evidence of anything. Reporting
either one as a fact is reporting noise as a result, and it will reverse itself
in front of the client next month.

## Schedule

Standard poll days after publish: **3, 7, 14, 21, 30.**

Front-loaded because the first-crawl window is where a new URL either enters the
grounding set or does not, and stretched to 30 so a late entry still gets caught.

Poll the head term always. Poll the variants where budget allows: the variants
are the ones that show cluster capture rather than single-keyword luck.

## What to log, per poll

| Field | Notes |
|---|---|
| Poll date | Actual date run, not the scheduled date |
| Poll number | 1 to 5 |
| Keyword | Head term or variant |
| AIO present | Was `ai_overview` in `item_types` at all |
| Client cited | Client domain present in the AI Overview `references[]` |
| Cited domains | The full list this poll returned |
| Post URL | The URL under test |

`AIO present` matters separately from `Client cited`. If the AI Overview stopped
appearing for that keyword, the post did not lose a citation, the SERP changed
shape. Those are different findings and they get different responses.

## The math

```
AIO citation rate = polls where client cited / polls actually run
```

Report as `3/5 polls (60%)`. Always state the denominator. If only 3 of 5 polls
have come due, report `2/3 polls (67%), 3 of 5 polls complete`, and do not
annualize, project, or round a partial series into a headline number.

A post with fewer than 5 completed polls is **not yet reportable** as a rate in
a client report. It can appear as in-progress.

## Tracking the cited-domain list over time

The `Cited domains` column is not bookkeeping. Watch it for:

- **A competitor entering.** That cluster becomes a displacement target again
  and the post needs a depth pass, not a new post.
- **The client entering and leaving across polls.** Normal. That is what the
  40-46% figure predicts. It is not a regression and it does not need a fix.
- **The whole reference set churning.** Grounding behavior shifted. If this
  shows up across several clients at once, the quarterly spec re-validation
  moves up.

## Weekly sweep

Once a week, run every poll that has come due across all clients in one pass,
then update each client's log. Posts drop out of the sweep after poll 5.

A post that is not in the verification log does not get measured, and an
unmeasured post cannot be reported. Registering the URL is part of publishing,
not a follow-up task.
