"""Fit + coverage + timing scoring.

Coverage is weighted heaviest on purpose. A perfect-profile prospect in a market
where you have no unsold inventory is a pitch you cannot fill, and a burned
relationship costs more than a skipped one.
"""

BAND_POINTS = {"sweet_spot": 18, "core": 14, "platform": 11, "emerging": 7}
TICKET_POINTS = {"high": 10, "medium": 7, "low": 4}

SIGNAL_POINTS = {
    "new_mktg_leader": 8,    # 0-6 months in seat, hired to change something
    "hiring_field": 6,       # techs coming online need demand to bill against
    "acquisition": 6,        # new branch, no lead flow under the new brand
    "new_market": 5,         # licensed or registered somewhere they have no brand
    "headcount_growth": 3,
    "hiring_marketing": 3,
}

TIERS = [(65, "A"), (45, "B"), (30, "C")]


def estimate_revenue(employees):
    """Home services runs roughly $150-250k revenue per employee. Use the midpoint."""
    if not employees:
        return None
    return int(employees * 200_000)


def band_for(employees):
    if employees is None:
        return None
    if employees < 11:
        return None          # below $3M, out of scope
    if employees <= 20:
        return "emerging"
    if employees <= 50:
        return "core"
    if employees <= 200:
        return "sweet_spot"
    if employees <= 500:
        return "platform"
    return "platform"


def fit_score(company, has_marketing_contact, vertical_cfg):
    pts, why = 0.0, []

    band = company["size_band"]
    pts += BAND_POINTS.get(band, 0)
    if band in ("sweet_spot", "core"):
        why.append(f"{company['employees']} employees (~${estimate_revenue(company['employees'])//1_000_000}M)")

    ticket = (vertical_cfg or {}).get("ticket", "medium")
    pts += TICKET_POINTS.get(ticket, 5)

    if has_marketing_contact:
        pts += 8
        why.append("has a dedicated marketing function")
    elif band in ("emerging", "core"):
        pts += 4       # owner-led sale is slower to find but faster to close
        why.append("owner-led marketing decision")

    locs = company["num_locations"] or 1
    if locs >= 5:
        pts += 4
        why.append(f"{locs} locations")
    elif locs >= 2:
        pts += 2

    return min(pts, 40.0), why


def coverage_score(conn, company, vertical):
    """Unsold inventory in this company's state, for the service they sell."""
    row = conn.execute(
        """SELECT COALESCE(SUM(monthly_volume * (1.0 - COALESCE(fill_rate,0))),0) AS open_vol,
                  COUNT(*) AS zips
             FROM coverage
            WHERE service = ? AND state = ?""",
        (vertical, company["state"]),
    ).fetchone()

    open_vol, zips = row["open_vol"] or 0, row["zips"] or 0
    if zips == 0:
        return 0.0, ["no coverage data for this market"]
    if open_vol <= 0:
        return 5.0, ["market covered but currently fully sold"]

    # 40 pts at 200+ unsold leads/month in their state, scaled linearly below that.
    pts = min(40.0, 8.0 + (open_vol / 200.0) * 32.0)
    return pts, [f"~{int(open_vol)} unsold {vertical} leads/mo in {company['state']}"]


def signal_score(conn, company_id):
    rows = conn.execute(
        "SELECT kind, detail FROM signals WHERE company_id=?", (company_id,)
    ).fetchall()
    pts, why = 0.0, []
    seen = set()
    for r in rows:
        if r["kind"] in seen:
            continue
        seen.add(r["kind"])
        p = SIGNAL_POINTS.get(r["kind"], 0)
        pts += p
        if p >= 5 and r["detail"]:
            why.append(r["detail"])
    return min(pts, 20.0), why


def tier_for(total):
    for threshold, name in TIERS:
        if total >= threshold:
            return name
    return "hold"


def score_company(conn, company, vertical_cfg, has_marketing_contact):
    f, why_f = fit_score(company, has_marketing_contact, vertical_cfg)
    c, why_c = coverage_score(conn, company, company["vertical"])
    s, why_s = signal_score(conn, company["id"])
    total = f + c + s
    rationale = "; ".join(why_s + why_c + why_f) or "profile match only"
    return {
        "company_id": company["id"],
        "fit_score": round(f, 1),
        "coverage_score": round(c, 1),
        "signal_score": round(s, 1),
        "total": round(total, 1),
        "tier": tier_for(total),
        "rationale": rationale,
    }
