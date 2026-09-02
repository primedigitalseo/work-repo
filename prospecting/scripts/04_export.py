#!/usr/bin/env python3
"""Export ranked, enriched contacts to sequencer CSVs.

Produces two files:
  exports/email_<campaign>.csv      -> Instantly / Smartlead / Apollo sequences
  exports/linkedin_<campaign>.csv   -> daily-capped connection queue

Every row carries a `signal_line` — the specific reason this person is being
contacted today. Sequences reference it as a merge variable so no two emails
open the same way.

  python scripts/04_export.py --campaign roofing-q4 --tier A --daily-linkedin 20
"""
import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import db   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EXPORTS = ROOT / "exports"

# Opening line by strongest signal. Falls back to a market-fact opener.
SIGNAL_LINES = {
    "new_mktg_leader": "saw you stepped into the marketing seat at {company}",
    "acquisition":     "saw {company} added a location recently",
    "hiring_field":    "noticed {company} is hiring field staff in {state}",
    "new_market":      "saw {company} moving into a new market",
    "headcount_growth": "{company} looks like it's been growing headcount",
}
DEFAULT_LINE = "we have unsold {service} lead volume in {state}"

ROWS = """
SELECT ct.id, ct.first_name, ct.last_name, ct.title, ct.email, ct.email_status,
       ct.linkedin_url, ct.phone AS direct_phone,
       c.id AS company_id, c.name AS company, c.domain, c.vertical, c.city, c.state,
       c.employees, c.num_locations, c.phone AS company_phone,
       s.total, s.tier, s.rationale,
       (SELECT kind FROM signals g WHERE g.company_id = c.id
         ORDER BY g.weight DESC, g.detected_at DESC LIMIT 1) AS top_signal
  FROM contacts ct
  JOIN companies c ON c.id = ct.company_id
  JOIN scores    s ON s.company_id = c.id
 WHERE s.tier IN ({tiers})
   AND ({email_clause})
 ORDER BY s.total DESC, ct.title_tier ASC
"""


def signal_line(row):
    tpl = SIGNAL_LINES.get(row["top_signal"] or "", DEFAULT_LINE)
    return tpl.format(company=row["company"], state=row["state"] or "your markets",
                      service=row["vertical"])


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--tier", default="A,B")
    ap.add_argument("--daily-linkedin", type=int, default=20,
                    help="connection requests per day; keep this conservative")
    ap.add_argument("--linkedin-days", type=int, default=10)
    args = ap.parse_args()

    conn = db.connect()
    tiers = [t.strip() for t in args.tier.split(",")]

    # ---- email ----
    q = ROWS.format(tiers=",".join("?" * len(tiers)),
                    email_clause="ct.email IS NOT NULL AND ct.email_status != 'bounced'")
    email_rows = []
    for r in conn.execute(q, tiers):
        if db.is_suppressed(conn, email=r["email"], domain=r["domain"]):
            continue
        email_rows.append({
            "email": r["email"], "first_name": r["first_name"], "last_name": r["last_name"],
            "company": r["company"], "title": r["title"], "website": r["domain"],
            "city": r["city"], "state": r["state"], "service": r["vertical"],
            "employees": r["employees"], "locations": r["num_locations"],
            "phone": r["direct_phone"] or r["company_phone"],
            "signal_line": signal_line(r), "why": r["rationale"],
            "score": r["total"], "tier": r["tier"], "linkedin_url": r["linkedin_url"],
        })

    n_email = write_csv(EXPORTS / f"email_{args.campaign}.csv", email_rows, [
        "email", "first_name", "last_name", "company", "title", "website", "city",
        "state", "service", "employees", "locations", "phone", "signal_line", "why",
        "score", "tier", "linkedin_url"])

    # ---- linkedin ----
    q = ROWS.format(tiers=",".join("?" * len(tiers)),
                    email_clause="ct.linkedin_url IS NOT NULL")
    li_rows, cap = [], args.daily_linkedin * args.linkedin_days
    for i, r in enumerate(conn.execute(q, tiers)):
        if i >= cap:
            break
        li_rows.append({
            "linkedin_url": r["linkedin_url"], "first_name": r["first_name"],
            "company": r["company"], "title": r["title"], "state": r["state"],
            "service": r["vertical"], "signal_line": signal_line(r),
            "send_day": (i // args.daily_linkedin) + 1,
            "score": r["total"], "tier": r["tier"],
        })

    n_li = write_csv(EXPORTS / f"linkedin_{args.campaign}.csv", li_rows, [
        "send_day", "linkedin_url", "first_name", "company", "title", "state",
        "service", "signal_line", "score", "tier"])

    for r in email_rows:
        conn.execute("""INSERT OR IGNORE INTO outreach (contact_id,channel,campaign,exported_at)
                        SELECT id,'email',?,datetime('now') FROM contacts WHERE email=?""",
                     (args.campaign, r["email"]))
    conn.commit()

    print(f"email:    {n_email:5} rows -> exports/email_{args.campaign}.csv")
    print(f"linkedin: {n_li:5} rows -> exports/linkedin_{args.campaign}.csv "
          f"({args.daily_linkedin}/day over {args.linkedin_days} days)")


if __name__ == "__main__":
    main()
