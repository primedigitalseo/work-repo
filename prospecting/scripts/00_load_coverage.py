#!/usr/bin/env python3
"""Load your lead inventory. Run this FIRST — coverage is 40% of every score.

CSV columns: state,metro,postal_code,service,monthly_volume,fill_rate
  monthly_volume : exclusive leads you can deliver per month in that ZIP
  fill_rate      : 0.0-1.0, share already sold. Unsold = volume * (1 - fill_rate)

  python scripts/00_load_coverage.py config/coverage.csv
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import db   # noqa: E402


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    if not path.exists():
        sys.exit(f"not found: {path}")

    conn = db.connect()
    db.init(conn)
    n = 0
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            conn.execute(
                """INSERT INTO coverage (state,metro,postal_code,service,monthly_volume,fill_rate)
                   VALUES (?,?,?,?,?,?)
                   ON CONFLICT(postal_code,service) DO UPDATE SET
                     monthly_volume=excluded.monthly_volume, fill_rate=excluded.fill_rate""",
                (row["state"].strip().upper(), row.get("metro", "").strip(),
                 row["postal_code"].strip(), row["service"].strip().lower(),
                 int(row["monthly_volume"]), float(row["fill_rate"])))
            n += 1
    conn.commit()

    print(f"loaded {n} coverage rows")
    for r in conn.execute(
        """SELECT service, state, SUM(monthly_volume*(1.0-fill_rate)) AS open_vol
             FROM coverage GROUP BY service, state ORDER BY open_vol DESC"""):
        print(f"  {r['service']:12} {r['state']:3}  {int(r['open_vol']):5} unsold leads/mo")


if __name__ == "__main__":
    main()
