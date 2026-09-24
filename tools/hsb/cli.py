"""Command line front end for the Home Service Base API.

    python3 tools/hsb.py units
    python3 tools/hsb.py expired --state 24 --category Plumber --limit 200
    python3 tools/hsb.py watch mn-trades --state 24 --limit 1000
    python3 tools/hsb.py websites -f primaryCategory=Roofer -f minProfiles=5

Expects HSB_API_KEY in the environment.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys

from .client import Client, HsbError, MissingKey, build_url

STATE_DIR = os.environ.get("HSB_STATE_DIR", ".hsb-state")

# Column order the expired-domain screen expects, so a run drops straight into
# the Ahrefs batch-analysis step without reshaping.
SCREEN_COLUMNS = [
    "domain", "name", "primaryCategory", "city", "state",
    "rating", "reviewsCount", "phone", "mapsUrl", "profileUuid",
]

WEBSITE_COLUMNS = [
    "domain", "profileCount", "totalReviewsCount", "topCategories",
    "establishedAt", "googleAdsCount", "advertisesLsa", "websiteId",
]


def _parse_filters(pairs):
    """Turn repeated -f key=value into a filter dict, collecting repeats."""
    filters = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise SystemExit("Bad filter %r - expected key=value" % pair)
        key, value = pair.split("=", 1)
        key, value = key.strip(), value.strip()
        if key in filters:
            existing = filters[key]
            if isinstance(existing, list):
                existing.append(value)
            else:
                filters[key] = [existing, value]
        else:
            filters[key] = value
    return filters


def _flatten_profile(row):
    return {
        "domain": row.get("websiteDomain") or "",
        "name": row.get("name") or "",
        "primaryCategory": row.get("primaryCategory") or "",
        "city": row.get("city") or "",
        "state": row.get("state") or "",
        "rating": row.get("rating") if row.get("rating") is not None else "",
        "reviewsCount": row.get("reviewsCount") if row.get("reviewsCount") is not None else "",
        "phone": row.get("phone") or "",
        "mapsUrl": row.get("mapsUrl") or "",
        "profileUuid": row.get("uuid") or "",
    }


def _flatten_website(row):
    cats = row.get("topCategories") or []
    return {
        "domain": row.get("domain") or "",
        "profileCount": row.get("profileCount") if row.get("profileCount") is not None else "",
        "totalReviewsCount": row.get("totalReviewsCount") if row.get("totalReviewsCount") is not None else "",
        "topCategories": "; ".join(
            "%s (%s)" % (c.get("name"), c.get("count")) for c in cats if c.get("name")
        ),
        "establishedAt": (row.get("establishedAt") or "")[:10],
        "googleAdsCount": row.get("googleAdsCount") if row.get("googleAdsCount") is not None else "",
        "advertisesLsa": row.get("advertisesLsa"),
        "websiteId": row.get("id") or "",
    }


def _emit(rows, columns, fmt, stream=None):
    stream = stream or sys.stdout
    if fmt == "json":
        json.dump(rows, stream, indent=2)
        stream.write("\n")
        return
    writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)


def _client(args):
    return Client(verbose=getattr(args, "verbose", False))


def _report_units(client):
    if client.units_charged_total:
        left = client.units_remaining
        print(
            "[hsb] %d units charged, %s remaining"
            % (client.units_charged_total, "unlimited" if left is None else left),
            file=sys.stderr,
        )


# --------------------------------------------------------------------- commands


def cmd_units(args):
    client = _client(args)
    usage = client.usage()
    left = usage["unitsRemaining"]
    print("Units remaining: %s" % ("unlimited" if left is None else left))
    print("This probe cost: %d" % usage["unitsCharged"])
    return 0


def cmd_search(args, path):
    filters = _parse_filters(args.filter)
    if args.dry_run:
        print(build_url(path, filters))
        return 0
    client = _client(args)
    rows = list(getattr(client, path)(filters, limit=args.limit))
    flatten = _flatten_website if path == "websites" else _flatten_profile
    columns = WEBSITE_COLUMNS if path == "websites" else SCREEN_COLUMNS
    out = rows if args.format == "json" else [flatten(r) for r in rows]
    _emit(out, columns, args.format)
    _report_units(client)
    return 0


def cmd_expired(args):
    """Unregistered domains only.

    domainUnregistered is forced on rather than passed through, because the
    failure that wasted run 001 was an export filtered by establishment date
    instead of domain status - fifty live businesses, one of them running two
    thousand Google Ads.
    """
    filters = _parse_filters(args.filter)

    for banned in ("established", "establishedFrom", "establishedTo"):
        if banned in filters:
            raise SystemExit(
                "%s cannot combine with unregistered domains - they have no "
                "registration date. Drop it." % banned
            )

    filters["domainUnregistered"] = "1"
    if args.state:
        filters["stateId"] = args.state
    if args.city:
        filters["cityId"] = args.city
    if args.category:
        filters["primaryCategory"] = args.category
    if args.min_reviews is not None:
        filters["minReviews" if args.endpoint == "profiles" else "minTotalReviews"] = args.min_reviews

    if args.dry_run:
        print(build_url(args.endpoint, filters))
        return 0

    client = _client(args)
    rows = list(getattr(client, args.endpoint)(filters, limit=args.limit))

    # An unregistered domain has no WHOIS record, so it cannot carry a
    # registration date. Anything that does means the filter did not apply.
    date_field = "websiteEstablishedAt" if args.endpoint == "profiles" else "establishedAt"
    dated = [r for r in rows if r.get(date_field)]
    if dated:
        print(
            "[hsb] WARNING: %d of %d rows carry a registration date. The "
            "unregistered filter did not apply - do not spend Ahrefs units on "
            "this list." % (len(dated), len(rows)),
            file=sys.stderr,
        )

    flatten = _flatten_profile if args.endpoint == "profiles" else _flatten_website
    columns = SCREEN_COLUMNS if args.endpoint == "profiles" else WEBSITE_COLUMNS
    out = rows if args.format == "json" else [flatten(r) for r in rows]
    _emit(out, columns, args.format)
    print("[hsb] %d unregistered domains" % len(rows), file=sys.stderr)
    _report_units(client)
    return 0


def cmd_watch(args):
    """Snapshot the unregistered set and report what is new since last run.

    The API has no drop-date filter, so freshness has to be derived. Domains
    appearing for the first time between two snapshots dropped recently - which
    is the window worth buying in, before the link-selling networks arrive.
    """
    filters = _parse_filters(args.filter)
    filters["domainUnregistered"] = "1"
    if args.state:
        filters["stateId"] = args.state
    if args.city:
        filters["cityId"] = args.city
    if args.category:
        filters["primaryCategory"] = args.category

    if args.dry_run:
        print(build_url("profiles", filters))
        return 0

    client = _client(args)
    os.makedirs(STATE_DIR, exist_ok=True)
    path = os.path.join(STATE_DIR, "%s.json" % args.name)

    previous = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            previous = json.load(fh).get("domains", {})

    rows = list(client.profiles(filters, limit=args.limit))
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

    current, fresh = {}, []
    for row in rows:
        domain = row.get("websiteDomain")
        if not domain:
            continue
        if domain in previous:
            current[domain] = previous[domain]
        else:
            current[domain] = now
            fresh.append(row)

    gone = sorted(set(previous) - set(current))

    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"name": args.name, "updatedAt": now, "domains": current}, fh, indent=2)

    if not previous:
        print(
            "[hsb] Baseline written: %d domains. Run again later to see new drops."
            % len(current),
            file=sys.stderr,
        )
    else:
        print(
            "[hsb] %d tracked, %d new since last run, %d no longer listed"
            % (len(current), len(fresh), len(gone)),
            file=sys.stderr,
        )

    out = fresh if args.format == "json" else [_flatten_profile(r) for r in fresh]
    _emit(out, SCREEN_COLUMNS, args.format)
    _report_units(client)
    return 0


def cmd_signal(args):
    client = _client(args)
    rows = list(client.signal(args.signal_id, args.type, limit=args.limit))
    json.dump(rows, sys.stdout, indent=2)
    sys.stdout.write("\n")
    _report_units(client)
    return 0


# ------------------------------------------------------------------------ main


def build_parser():
    p = argparse.ArgumentParser(
        prog="hsb",
        description="Home Service Base API client (read-only).",
    )
    p.add_argument("-v", "--verbose", action="store_true", help="Log each request to stderr.")
    sub = p.add_subparsers(dest="command", required=True)

    def add_common(sp, with_limit=True):
        sp.add_argument("-f", "--filter", action="append", metavar="KEY=VALUE",
                        help="Raw API filter. Repeat for multiple, or to repeat one key.")
        if with_limit:
            sp.add_argument("--limit", type=int, default=None,
                            help="Stop after N rows. Each row costs 1 unit.")
        sp.add_argument("--format", choices=["csv", "json"], default="csv")
        sp.add_argument("--dry-run", action="store_true",
                        help="Print the request URL without calling or spending units.")

    sp = sub.add_parser("units", help="Report the unit balance (free).")
    sp.set_defaults(func=cmd_units)

    sp = sub.add_parser("websites", help="Search the websites database.")
    add_common(sp)
    sp.set_defaults(func=lambda a: cmd_search(a, "websites"))

    sp = sub.add_parser("profiles", help="Search the business profiles database.")
    add_common(sp)
    sp.set_defaults(func=lambda a: cmd_search(a, "profiles"))

    sp = sub.add_parser("expired", help="Unregistered domains, filter forced on.")
    add_common(sp)
    sp.add_argument("--endpoint", choices=["profiles", "websites"], default="profiles",
                    help="profiles carries city/state and is better for local screening.")
    sp.add_argument("--state", action="append", help="stateId. Repeatable.")
    sp.add_argument("--city", action="append", help="cityId. Repeatable.")
    sp.add_argument("--category", action="append", help="Google category name. Repeatable.")
    sp.add_argument("--min-reviews", type=int, default=None)
    sp.set_defaults(func=cmd_expired)

    sp = sub.add_parser("watch", help="Diff the unregistered set against the last snapshot.")
    sp.add_argument("name", help="Snapshot name, e.g. mn-trades.")
    add_common(sp)
    sp.add_argument("--state", action="append")
    sp.add_argument("--city", action="append")
    sp.add_argument("--category", action="append")
    sp.set_defaults(func=cmd_watch)

    sp = sub.add_parser("signal", help="Fetch new results from one of your signals.")
    sp.add_argument("signal_id")
    sp.add_argument("--type", choices=["new_adopters", "new_profiles", "new_software",
                                       "new_videos", "new_websites", "new_companies"])
    sp.add_argument("--limit", type=int, default=None)
    sp.add_argument("--verbose", action="store_true")
    sp.set_defaults(func=cmd_signal)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except MissingKey as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    except HsbError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130
