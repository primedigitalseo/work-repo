# Suppression and Sending Infrastructure

## Suppression table

One table, agency-wide, checked before every push. This exists because the same
editor is a prospect for every client in a vertical, and they only get pitched
once.

```sql
CREATE TABLE outreach_contacts (
  email             TEXT PRIMARY KEY,
  domain            TEXT NOT NULL,
  author_name       TEXT,
  client_pitched    TEXT NOT NULL,
  campaign_id       TEXT,
  sent_at           DATE NOT NULL,
  outcome           TEXT,   -- no_reply | positive | negative | paid_quote | unsubscribe | bounce
  archetype         TEXT,
  notes             TEXT
);
CREATE INDEX idx_domain ON outreach_contacts(domain);
CREATE INDEX idx_sent_at ON outreach_contacts(sent_at);
```

Pre-push checks, in order:

1. **Email seen in last 90 days, any client** → drop
2. **Outcome ever `negative` / `unsubscribe` / `bounce`** → drop permanently
3. **Domain pitched for a different client this quarter** → drop
4. **Domain already links to this client** → drop (the intersect should have
   caught it, but profiles change between pulls)

The 90-day cooldown is per-contact and crosses clients deliberately. From the
recipient's side there is one agency emailing them, not four campaigns.

## Sending infrastructure

**Never send from the agency primary domain.** Client link outreach never
leaves `primedigitalseo.com`. One bad month there poisons every inbox the
agency depends on — sales, client comms, everything.

**One secondary domain per client**, branded to the client, not the agency:

- `getdd-b.com`, `dd-b-team.com` — not `primedigital-dd-b.com`
- 2–3 mailboxes per domain
- Warm for 3–4 weeks before the first real send
- Cap 30–40 sends per mailbox per day, ramping from 10

**Sender identity is a client decision, made at onboarding, not per campaign.**
Sending as the client converts meaningfully better. Sending as "the agency on
behalf of" reads like an agency and gets filed accordingly. Go client-branded,
and get sign-off on what goes out under their name during onboarding so it is
never a per-campaign conversation.

**Catch-all bucket.** Catch-all domains never go out on a primary. Route to a
dedicated secondary or drop. Watch bounce rate hard — above 3% pause the
campaign and re-verify the whole list.

## Volume math

At 400 sends/client/month across 6 clients that is 2,400/month, which needs
roughly 12–18 warm mailboxes across 6 domains. Plan infrastructure before
selling the sixth client, not after.

## Compliance

**CAN-SPAM** applies to every send:

- A real physical postal address in the footer
- A functioning opt-out that is honored within 10 business days
- No deceptive subject lines or From headers — the sender must be a real
  person who exists at the client or agency
- Opt-outs go into the suppression table as `unsubscribe`, permanently

**GDPR/UK-GDPR:** either filter EU/UK TLDs and known-EU domains out of the list,
or make a deliberate, documented decision to accept the exposure. Do not let it
happen by default because nobody looked.

Log the address and opt-out link used per campaign in the campaign brief so
there is a record.
