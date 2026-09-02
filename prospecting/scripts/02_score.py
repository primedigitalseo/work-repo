#!/usr/bin/env python3
"""Score every sourced company. Run after 01_source and after any coverage update."""
import sys
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import db                # noqa: E402
from src.score import score_company   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CFG = yaml.safe_load((ROOT / "config" / "icp.yaml").read_text())

MARKETING_WORDS = ("marketing", "growth", "demand", "brand", "digital")


def main():
    conn = db.connect()
    db.init(conn)

    companies = conn.execute("SELECT * FROM companies").fetchall()
    if not companies:
        sys.exit("no companies in db — run scripts/01_source.py first")

    counts = {"A": 0, "B": 0, "C": 0, "hold": 0}
    for c in companies:
        titles = [r["title"] or "" for r in conn.execute(
            "SELECT title FROM contacts WHERE company_id=?", (c["id"],))]
        has_mktg = any(w in t.lower() for t in titles for w in MARKETING_WORDS)
        s = score_company(conn, c, CFG["verticals"].get(c["vertical"]), has_mktg)
        conn.execute(
            """INSERT INTO scores (company_id,fit_score,coverage_score,signal_score,
                                   total,tier,rationale,computed_at)
               VALUES (:company_id,:fit_score,:coverage_score,:signal_score,
                       :total,:tier,:rationale,datetime('now'))
               ON CONFLICT(company_id) DO UPDATE SET
                 fit_score=excluded.fit_score, coverage_score=excluded.coverage_score,
                 signal_score=excluded.signal_score, total=excluded.total,
                 tier=excluded.tier, rationale=excluded.rationale,
                 computed_at=datetime('now')""", s)
        counts[s["tier"]] += 1
    conn.commit()

    print(f"scored {len(companies)} companies")
    for t in ("A", "B", "C", "hold"):
        print(f"  tier {t}: {counts[t]}")

    print("\ntop 15:")
    for r in conn.execute(
        """SELECT c.name, c.vertical, c.state, c.employees, s.total, s.tier, s.rationale
             FROM scores s JOIN companies c ON c.id = s.company_id
            ORDER BY s.total DESC LIMIT 15"""):
        print(f"  {r['total']:5.1f} {r['tier']}  {r['name'][:34]:34} "
              f"{r['vertical']:12} {r['state'] or '--':4} {r['employees'] or 0:4}emp  {r['rationale'][:70]}")


if __name__ == "__main__":
    main()
