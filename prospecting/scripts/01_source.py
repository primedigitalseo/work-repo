#!/usr/bin/env python3
"""Source companies + contacts from Apollo into the local DB.

Spends NO enrichment credits. Search only. Records whether an email exists
(has_email) so scoring can prioritize before you pay to reveal anything.

  python scripts/01_source.py --vertical roofing
  python scripts/01_source.py --all --limit-per-band 2000
"""
import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import db                     # noqa: E402
from src.apollo import Apollo          # noqa: E402
from src.score import band_for, estimate_revenue   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CFG = yaml.safe_load((ROOT / "config" / "icp.yaml").read_text())


def org_from_row(row, vertical):
    """Apollo splits results into `organizations` (net-new) and `accounts` (saved).
    The organization id lives in a different field for each."""
    oid = row.get("organization_id") or row.get("id")
    domain = row.get("primary_domain") or row.get("domain")
    emp = row.get("estimated_num_employees")
    band = band_for(emp)
    if not band:
        return None
    return {
        "id": oid,
        "name": row.get("name"),
        "domain": domain,
        "linkedin_url": row.get("linkedin_url"),
        "phone": (row.get("primary_phone") or {}).get("number"),
        "vertical": vertical,
        "size_band": band,
        "employees": emp,
        "revenue_apollo": row.get("annual_revenue"),
        "revenue_est": estimate_revenue(emp),
        "city": row.get("city"),
        "state": row.get("state"),
        "postal_code": row.get("postal_code"),
        "metro": None,
        "founded_year": row.get("founded_year"),
        "num_locations": 1,
        "active_job_count": row.get("num_active_job_postings") or 0,
        "source": "apollo",
    }


def person_from_row(row, company_id, tier):
    org = row.get("organization") or {}
    return {
        "id": row.get("id"),
        "company_id": company_id or org.get("id"),
        "first_name": row.get("first_name"),
        "last_name": row.get("last_name") or row.get("last_name_obfuscated"),
        "title": row.get("title"),
        "title_tier": tier,
        "seniority": row.get("seniority"),
        "email": None,                       # not revealed by search
        "email_status": row.get("email_status"),
        "has_email": 1 if row.get("has_email") else 0,
        "linkedin_url": row.get("linkedin_url"),
        "phone": None,
        "city": row.get("city"),
        "state": row.get("state"),
    }


def source_vertical(conn, api, vertical, vcfg, limit_per_band):
    geo = CFG["geo"]
    locations = geo["states"] or [geo["country"]]
    since = (date.today() - timedelta(days=CFG["capacity_signals"]["window_days"])).isoformat()
    total_c = total_p = 0

    for band, bcfg in CFG["size_bands"].items():
        ranges = [bcfg["range"]]
        print(f"  [{vertical}/{band}] employees {bcfg['range']} ({bcfg['est_revenue']})")

        # --- companies ---
        got = 0
        for row in api.paginate(api.search_companies,
                                keywords=vcfg["keywords"],
                                employee_ranges=ranges,
                                locations=locations):
            c = org_from_row(row, vertical)
            if not c or not c["id"]:
                continue
            if c["domain"] and db.is_suppressed(conn, domain=c["domain"]):
                continue
            db.upsert_company(conn, c)
            if c["active_job_count"] >= 3:
                db.add_signal(conn, c["id"], "hiring_field",
                              f"{c['active_job_count']} open roles")
            got += 1
            if got >= limit_per_band:
                break
        conn.commit()
        total_c += got
        print(f"      companies: {got}")

        # --- contacts, by title tier ---
        for group in CFG["title_ladder"][band]:
            cap = CFG["contacts_per_company"][band] * limit_per_band
            n = 0
            for row in api.paginate(api.search_people,
                                    titles=group["titles"],
                                    employee_ranges=ranges,
                                    keywords=vcfg["keywords"],
                                    person_locations=[geo["country"]],
                                    org_locations=locations):
                org = row.get("organization") or {}
                oid = org.get("id")
                if not oid:
                    continue
                exists = conn.execute("SELECT 1 FROM companies WHERE id=?", (oid,)).fetchone()
                if not exists:
                    continue           # keep the graph closed to sourced companies
                db.upsert_contact(conn, person_from_row(row, oid, group["tier"]))
                n += 1
                if n >= cap:
                    break
            conn.commit()
            total_p += n
            print(f"      contacts t{group['tier']} {group['titles'][0]!r}: {n}")

        # --- capacity signal: field hiring in the last N days ---
        n = 0
        for row in api.paginate(api.search_companies,
                                keywords=vcfg["keywords"],
                                employee_ranges=ranges,
                                locations=locations,
                                job_titles=CFG["capacity_signals"]["job_titles"],
                                job_posted_after=since):
            oid = row.get("organization_id") or row.get("id")
            if conn.execute("SELECT 1 FROM companies WHERE id=?", (oid,)).fetchone():
                db.add_signal(conn, oid, "hiring_field",
                              "actively hiring field staff", weight=1.5)
                n += 1
            if n >= limit_per_band:
                break
        conn.commit()
        print(f"      hiring signals: {n}")

    return total_c, total_p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vertical")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--limit-per-band", type=int, default=1000)
    args = ap.parse_args()

    load_dotenv(ROOT / ".env")
    conn = db.connect()
    db.init(conn)
    api = Apollo()

    verticals = CFG["verticals"]
    targets = verticals.keys() if args.all else [args.vertical]
    if not args.all and not args.vertical:
        ap.error("pass --vertical NAME or --all")

    tc = tp = 0
    for v in targets:
        if v not in verticals:
            sys.exit(f"unknown vertical {v!r}; options: {list(verticals)}")
        print(f"\n== {v} ==")
        c, p = source_vertical(conn, api, v, verticals[v], args.limit_per_band)
        tc += c
        tp += p

    print(f"\ncompanies: {tc}  contacts: {tp}  enrichment credits spent: {api.credits_spent}")


if __name__ == "__main__":
    main()
