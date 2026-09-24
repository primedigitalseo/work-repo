#!/usr/bin/env python3
"""Weekly drop watch for every client metro in tools/metro_watch.json.

    python3 tools/metro_watch.py              # all markets
    python3 tools/metro_watch.py dsh redefined
    python3 tools/metro_watch.py --dry-run    # print URLs, spend nothing

For each market it pulls the unregistered domains in the metro's counties,
limited to home-improvement categories minus the client's own niche, and diffs
them against the snapshot in watch-state/<market>.json. Domains seen for the
first time are written to watch-reports/<date>.csv - those are the fresh drops
to DR-screen before the link-selling networks reach them.

Snapshots live in a tracked directory, not .hsb-state/, because cloud
containers are ephemeral: the diff only works if the last snapshot is committed.

Cost: one unit per row pulled, roughly 3,400 per full run.
"""

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hsb.client import Client, HsbError, build_url  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(ROOT, "tools", "metro_watch.json")
STATE_DIR = os.path.join(ROOT, "watch-state")
REPORT_DIR = os.path.join(ROOT, "watch-reports")

REPORT_COLUMNS = [
    "market", "client", "domain", "name", "primaryCategory", "city", "state",
    "rating", "reviewsCount", "mapsUrl",
]


def market_filters(config, market):
    spec = config["markets"][market]
    exclude = re.compile(spec["exclude"], re.I)
    return {
        "domainUnregistered": "1",
        "geoKind": "county",
        "geoId": spec["counties"],
        "primaryCategory": [c for c in config["categories"] if not exclude.search(c)],
    }


def load_snapshot(market):
    path = os.path.join(STATE_DIR, "%s.json" % market)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh).get("domains", {})


def save_snapshot(market, domains, now):
    os.makedirs(STATE_DIR, exist_ok=True)
    path = os.path.join(STATE_DIR, "%s.json" % market)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"name": market, "updatedAt": now, "domains": domains}, fh,
                  indent=1, sort_keys=True)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("markets", nargs="*", help="Market keys. Default: all.")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    with open(CONFIG, "r", encoding="utf-8") as fh:
        config = json.load(fh)
    markets = args.markets or list(config["markets"])
    unknown = [m for m in markets if m not in config["markets"]]
    if unknown:
        raise SystemExit("Unknown market(s): %s" % ", ".join(unknown))

    if args.dry_run:
        for m in markets:
            print(m, build_url("profiles", market_filters(config, m)))
        return 0

    client = Client()
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    fresh_rows = []

    for m in markets:
        previous = load_snapshot(m)
        try:
            rows = list(client.profiles(market_filters(config, m)))
        except HsbError as exc:
            print("[watch] %s: %s - snapshot left unchanged" % (m, exc), file=sys.stderr)
            continue

        current, fresh = {}, {}
        for row in rows:
            domain = (row.get("websiteDomain") or "").lower()
            if not domain or domain in current:
                continue
            if domain in previous:
                current[domain] = previous[domain]
            else:
                current[domain] = now
                fresh[domain] = row

        save_snapshot(m, current, now)
        client_name = config["markets"][m]["client"]
        for domain, row in fresh.items():
            fresh_rows.append({
                "market": m, "client": client_name, "domain": domain,
                "name": row.get("name") or "", "primaryCategory": row.get("primaryCategory") or "",
                "city": row.get("city") or "", "state": row.get("state") or "",
                "rating": row.get("rating") if row.get("rating") is not None else "",
                "reviewsCount": row.get("reviewsCount") if row.get("reviewsCount") is not None else "",
                "mapsUrl": row.get("mapsUrl") or "",
            })

        label = "baseline" if not previous else "%d new" % len(fresh)
        print("[watch] %s: %d tracked, %s, %d no longer listed"
              % (m, len(current), label, len(set(previous) - set(current))), file=sys.stderr)

    os.makedirs(REPORT_DIR, exist_ok=True)
    report = os.path.join(REPORT_DIR, "%s.csv" % now[:10])
    with open(report, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=REPORT_COLUMNS)
        writer.writeheader()
        writer.writerows(fresh_rows)

    print("[watch] %d fresh drops -> %s" % (len(fresh_rows), os.path.relpath(report, ROOT)),
          file=sys.stderr)
    print("[watch] %d units charged, %s remaining"
          % (client.units_charged_total, client.units_remaining), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
