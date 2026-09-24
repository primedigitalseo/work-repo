"""Home Service Base API v1 client.

Read-only. Enforces the account limits documented at
https://homeservicebase.com/api (1 in-flight request, 60 req/60s, 1000 rows
per request, 30s query timeout) so a caller cannot trip them by accident.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://homeservicebase.com/api/v1"
ENV_KEY = "HSB_API_KEY"

MAX_ROWS_PER_REQUEST = 1000
# 60 requests per 60 seconds, and only one may be in flight. Serialising with a
# small margin keeps us under both without needing a token bucket.
MIN_REQUEST_INTERVAL = 1.05
MAX_RETRIES = 4


def encode_params(params):
    """Repeatable params are sent once per value; flags take 1."""
    pairs = []
    for key, value in (params or {}).items():
        if value is None or value == "":
            continue
        if isinstance(value, bool):
            if value:
                pairs.append((key, "1"))
            continue
        if isinstance(value, (list, tuple, set)):
            for item in value:
                if item is not None and item != "":
                    pairs.append((key, str(item)))
            continue
        pairs.append((key, str(value)))
    return urllib.parse.urlencode(pairs)


def build_url(path, params=None, base_url=BASE_URL):
    """The URL a call would use. No key, no request, no units."""
    query = encode_params(params)
    url = "%s/%s" % (base_url.rstrip("/"), path.lstrip("/"))
    return "%s?%s" % (url, query) if query else url


class HsbError(RuntimeError):
    """An API call failed in a way the caller needs to handle."""

    def __init__(self, message, status=None, payload=None):
        super().__init__(message)
        self.status = status
        self.payload = payload or {}


class MissingKey(HsbError):
    pass


def _redact(text):
    """Strip anything that looks like a key out of text we might print."""
    out = []
    for token in str(text).split():
        out.append("hsb_<redacted>" if token.startswith("hsb_") else token)
    return " ".join(out)


class Client:
    def __init__(self, api_key=None, base_url=BASE_URL, verbose=False):
        self.api_key = api_key or os.environ.get(ENV_KEY)
        if not self.api_key:
            raise MissingKey(
                "No API key. Set %s in the environment (cloud environment menu "
                "-> Edit -> API credentials). Never paste the key into chat." % ENV_KEY
            )
        self.base_url = base_url.rstrip("/")
        self.verbose = verbose
        self._last_request_at = 0.0
        self.units_remaining = None
        self.units_charged_total = 0

    # ---------------------------------------------------------------- internals

    def _throttle(self):
        wait = MIN_REQUEST_INTERVAL - (time.monotonic() - self._last_request_at)
        if wait > 0:
            time.sleep(wait)

    def _log(self, message):
        if self.verbose:
            print("[hsb] %s" % _redact(message), file=sys.stderr)

    def request(self, path, params=None):
        url = build_url(path, params, self.base_url)

        for attempt in range(MAX_RETRIES + 1):
            self._throttle()
            req = urllib.request.Request(
                url,
                headers={
                    "Authorization": "Bearer %s" % self.api_key,
                    "Accept": "application/json",
                    "User-Agent": "prime-digital-hsb/1.0",
                },
                method="GET",
            )
            self._log("GET %s" % url)
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    self._last_request_at = time.monotonic()
                    body = json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                self._last_request_at = time.monotonic()
                raw = exc.read().decode("utf-8", "replace")
                try:
                    payload = json.loads(raw)
                except ValueError:
                    payload = {"error": raw[:400]}
                message = payload.get("error", raw[:400])

                if exc.code == 429 and attempt < MAX_RETRIES:
                    # Either a rate limit or another request already running.
                    delay = float(exc.headers.get("Retry-After") or 5)
                    self._log("429 - waiting %.0fs (%s)" % (delay, message))
                    time.sleep(delay)
                    continue
                if exc.code == 503 and attempt < MAX_RETRIES:
                    # Query exceeded the 30s budget. Backing off rarely helps on
                    # its own, but a single retry costs nothing (errors are free).
                    self._log("503 - query too slow, retrying once")
                    time.sleep(2 * (attempt + 1))
                    continue

                raise HsbError(self._explain(exc.code, message), exc.code, payload)
            except urllib.error.URLError as exc:
                self._last_request_at = time.monotonic()
                raise HsbError(
                    "Could not reach %s (%s). If this is a CONNECT 403, the "
                    "environment's network policy is denying the host - add "
                    "homeservicebase.com to the allowed domains."
                    % (self.base_url, exc.reason)
                )

            charged = body.get("unitsCharged") or 0
            self.units_charged_total += charged
            if "unitsRemaining" in body:
                self.units_remaining = body["unitsRemaining"]
            return body

        raise HsbError("Gave up after %d retries" % MAX_RETRIES)

    @staticmethod
    def _explain(status, message):
        hints = {
            400: "Malformed parameter. Check filter names against the API reference.",
            401: "Key missing, invalid or revoked. Re-issue it in Settings -> API.",
            403: "No API access on this plan, monthly units exhausted, or the signal is paused.",
            404: "Signal not found, or it belongs to another account.",
            429: "Over a request limit, or a request is already running.",
            503: "Query ran past 30s. Narrow it with a category or location filter.",
        }
        hint = hints.get(status, "")
        return "HTTP %d: %s%s" % (status, message, (" - " + hint) if hint else "")

    # ------------------------------------------------------------------ paging

    def paginate(self, path, params, key, limit=None, page_size=MAX_ROWS_PER_REQUEST):
        """Yield rows across pages, stopping on a short page or at `limit`.

        Every row costs a unit, so this never over-fetches: the last page is
        trimmed to exactly what the caller asked for.
        """
        params = dict(params or {})
        offset = int(params.pop("offset", 0) or 0)
        page_size = max(1, min(int(page_size), MAX_ROWS_PER_REQUEST))
        yielded = 0

        while True:
            want = page_size
            if limit is not None:
                remaining = limit - yielded
                if remaining <= 0:
                    return
                want = min(want, remaining)

            page = dict(params)
            page["limit"] = want
            page["offset"] = offset
            body = self.request(path, page)
            rows = body.get(key) or []

            for row in rows:
                yield row
                yielded += 1
                if limit is not None and yielded >= limit:
                    return

            if len(rows) < want:
                return
            offset += len(rows)

    # ---------------------------------------------------------------- endpoints

    def websites(self, filters=None, limit=None):
        return self.paginate("websites", filters, "websites", limit=limit)

    def profiles(self, filters=None, limit=None):
        return self.paginate("profiles", filters, "profiles", limit=limit)

    def signal(self, signal_id, result_type=None, limit=None):
        filters = {}
        if result_type:
            filters["type"] = result_type
        return self.paginate("signals/%s" % signal_id, filters, "results", limit=limit)

    def usage(self):
        """Read the unit balance without spending anything.

        A query that matches nothing returns zero rows, and empty pages are free.
        """
        body = self.request("websites", {"domain": "__hsb_usage_probe__", "limit": 1})
        return {
            "unitsRemaining": body.get("unitsRemaining"),
            "unitsCharged": body.get("unitsCharged", 0),
        }
