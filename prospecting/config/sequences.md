# Outreach copy

One rule: the first line must name something true and specific about *them*.
`{{signal_line}}` is populated per-contact by `04_export.py` from their strongest
detected signal, so no two sends open the same way.

Merge variables available in every export row:
`first_name` `company` `title` `city` `state` `service` `employees` `locations`
`signal_line` `why` `phone` `website`

---

## Email — sequence A (marketing title)

**1 — day 0.** Subject: `{{service}} leads in {{state}}`

> {{first_name}} — {{signal_line}}.
>
> We sell exclusive inbound homeowner leads by service and ZIP. Not shared, not
> resold — the homeowner called about {{service}}, and the call routes to one company.
>
> We have unsold volume in a few of your markets right now. Worth a look at the ZIPs
> and what the CAC would run you?

**2 — day 3.** Subject: `re: {{service}} leads in {{state}}`

> Following up with specifics: I can show you exact ZIPs, monthly volume, and price
> per lead before you commit to anything.
>
> Most groups start with two ZIPs for 30 days, measure booked-job rate, then decide.
> Want the numbers for {{city}}?

**3 — day 7.** Subject: `last one`

> Closing the loop, {{first_name}}. If lead volume isn't the constraint at {{company}}
> right now, that's a fine answer — happy to check back next quarter.
>
> If capacity is the constraint instead, that's usually the better conversation anyway.

**4 — day 14, breakup.** Subject: `{{company}} — closing this out`

> Taking you off my list. If exclusive {{service}} volume in {{state}} becomes useful,
> reply to this and I'll pull current availability.

---

## Email — sequence B (owner / GM, under ~50 employees)

**1 — day 0.** Subject: `{{service}} calls in {{city}}`

> {{first_name}} — {{signal_line}}.
>
> I sell exclusive {{service}} calls by ZIP. One company per lead, no sharing.
> You control which ZIPs and how many per month, and you can turn it off any time.
>
> Want me to send what's available around {{city}} and what each call costs?

**2 — day 4.**

> Quick numbers for {{city}}: I can hold a block of ZIPs for you and start at a
> volume that fits your crew. Most owners start small to check the booked-job rate
> before scaling.
>
> Worth 10 minutes?

**3 — day 10, breakup.** Same as sequence A.

---

## LinkedIn

Connection note (300 char limit, no pitch):

> {{first_name}} — {{signal_line}}. I work with {{service}} companies on exclusive
> inbound lead volume by ZIP. Thought it was worth connecting.

Message, 2 days after they accept:

> Thanks for connecting, {{first_name}}. Straight to it: we sell exclusive inbound
> homeowner leads by service and ZIP — one company per lead. We have unsold
> {{service}} volume in {{state}} right now.
>
> Want me to send the ZIP list and pricing? No call needed to look at it.

Follow-up, 5 days later, only if no reply:

> No worries if the timing's off. If it helps, I can send current {{state}}
> availability as a one-pager — takes you 30 seconds to see whether it's relevant.

---

## What to avoid

- "Lead generation agency" — puts you in the bucket with everyone they've fired
- "Quick question" subject lines — filtered by pattern at this point
- Any claim about their current CPL you can't source
- Sending before you can actually fill the ZIPs you name
