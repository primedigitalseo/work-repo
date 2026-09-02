#!/usr/bin/env python3
"""Reveal emails for the top of the ranked list. THIS SPENDS APOLLO CREDITS.

One credit per revealed email. Defaults are deliberately small — raise --budget
only once you've reviewed what scripts/02_score.py ranked.

  python scripts/03_enrich.py --budget 250 --tier A --dry-run
  python scripts/03_enrich.py --budget 250 --tier A
"""
import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import db                # noqa: E402
from src.apollo import Apollo     # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

QUERY = """
SELECT ct.id, ct.first_name, ct.title, ct.title_tier, c.name AS company, s.total, s.tier
  FROM contacts ct
  JOIN companies c ON c.id = ct.company_id
  JOIN scores    s ON s.company_id = c.id
 WHERE ct.enriched_at IS NULL
   AND ct.has_email = 1
   AND s.tier IN ({tiers})
 ORDER BY s.total DESC, ct.title_tier ASC
 LIMIT ?
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=100, help="max credits to spend")
    ap.add_argument("--tier", default="A", help="comma list, e.g. A,B")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    load_dotenv(ROOT / ".env")
    conn = db.connect()
    tiers = [t.strip() for t in args.tier.split(",")]
    rows = conn.execute(
        QUERY.format(tiers=",".join("?" * len(tiers))), (*tiers, args.budget)
    ).fetchall()

    if not rows:
        sys.exit("nothing to enrich — run 01_source and 02_score first")

    print(f"{len(rows)} contacts queued, up to {len(rows)} credits")
    for r in rows[:10]:
        print(f"  {r['total']:5.1f} {r['tier']}  {r['first_name']} — {r['title']} @ {r['company']}")
    if len(rows) > 10:
        print(f"  ... and {len(rows)-10} more")

    if args.dry_run:
        print("\ndry run — no credits spent")
        return

    api = Apollo()
    revealed = 0
    for i in range(0, len(rows), 10):
        batch = rows[i:i + 10]
        matches = api.bulk_match([{"id": r["id"]} for r in batch])
        for m in matches:
            if not m or not m.get("id"):
                continue
            email = m.get("email")
            if email and db.is_suppressed(conn, email=email):
                continue
            conn.execute(
                """UPDATE contacts SET email=?, email_status=?, phone=?,
                          linkedin_url=COALESCE(?, linkedin_url),
                          last_name=COALESCE(?, last_name),
                          enriched_at=datetime('now')
                    WHERE id=?""",
                (email, m.get("email_status"),
                 (m.get("phone_numbers") or [{}])[0].get("sanitized_number"),
                 m.get("linkedin_url"), m.get("last_name"), m["id"]))
            if email:
                revealed += 1
        conn.commit()
        print(f"  {min(i+10, len(rows))}/{len(rows)} — {revealed} emails revealed")

    print(f"\nrevealed {revealed} emails, {api.credits_spent} credits spent")


if __name__ == "__main__":
    main()
