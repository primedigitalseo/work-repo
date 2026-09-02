"""Apollo API client.

Cost model that shapes this whole pipeline:
  - people/company SEARCH is cheap and returns has_email as a boolean flag
  - people BULK_MATCH (enrichment) costs 1 credit per revealed email

So: search wide, score, then spend credits only on the top of the ranked list.
Never enrich before scoring.
"""
import os
import time
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

BASE = "https://api.apollo.io/api/v1"
PAGE_MAX = 100
DISPLAY_LIMIT = 50_000  # Apollo caps any single search at 500 pages


class ApolloError(RuntimeError):
    pass


class Apollo:
    def __init__(self, api_key=None, sleep=0.35):
        self.key = api_key or os.environ.get("APOLLO_API_KEY")
        if not self.key:
            raise ApolloError("APOLLO_API_KEY not set (see .env.example)")
        self.sleep = sleep
        self.s = requests.Session()
        self.s.headers.update({
            "x-api-key": self.key,
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "accept": "application/json",
        })
        self.credits_spent = 0

    @retry(stop=stop_after_attempt(5),
           wait=wait_exponential(multiplier=2, min=2, max=30),
           retry=retry_if_exception_type(requests.RequestException))
    def _post(self, path, payload):
        r = self.s.post(f"{BASE}/{path}", json=payload, timeout=60)
        if r.status_code == 429:
            time.sleep(20)
            raise requests.RequestException("rate limited")
        if r.status_code >= 400:
            raise ApolloError(f"{path} -> {r.status_code}: {r.text[:400]}")
        time.sleep(self.sleep)
        return r.json()

    # ---------- search (cheap) ----------

    def search_companies(self, *, keywords=None, naics=None, employee_ranges=None,
                         locations=None, job_titles=None, job_posted_after=None,
                         page=1, per_page=PAGE_MAX):
        payload = {"page": page, "per_page": per_page}
        if keywords:
            payload["q_organization_keyword_tags"] = keywords
        if naics:
            payload["organization_naics_codes"] = naics
        if employee_ranges:
            payload["organization_num_employees_ranges"] = employee_ranges
        if locations:
            payload["organization_locations"] = locations
        if job_titles:
            payload["q_organization_job_titles"] = job_titles
        if job_posted_after:
            payload["organization_job_posted_at_range"] = {"min": job_posted_after}
        return self._post("mixed_companies/search", payload)

    def search_people(self, *, titles=None, employee_ranges=None, org_ids=None,
                      person_locations=None, org_locations=None, keywords=None,
                      seniorities=None, days_in_title_max=None,
                      page=1, per_page=PAGE_MAX):
        payload = {"page": page, "per_page": per_page}
        if titles:
            payload["person_titles"] = titles
        if employee_ranges:
            payload["organization_num_employees_ranges"] = employee_ranges
        if org_ids:
            payload["organization_ids"] = org_ids
        if person_locations:
            payload["person_locations"] = person_locations
        if org_locations:
            payload["organization_locations"] = org_locations
        if keywords:
            payload["q_organization_keyword_tags"] = keywords
        if seniorities:
            payload["person_seniorities"] = seniorities
        if days_in_title_max:
            # New in seat = highest-conversion window for a new vendor.
            payload["person_days_in_current_title_range"] = {"max": days_in_title_max}
        return self._post("mixed_people/search", payload)

    def paginate(self, fn, **kw):
        """Yield every record across pages, respecting Apollo's 50k display cap."""
        page, seen = 1, 0
        while True:
            data = fn(page=page, **kw)
            rows = data.get("people") or data.get("organizations") or []
            rows += data.get("accounts") or []
            if not rows:
                return
            for r in rows:
                yield r
            seen += len(rows)
            total = data.get("total_entries", 0)
            if seen >= min(total, DISPLAY_LIMIT) or page >= 500:
                return
            page += 1

    # ---------- enrichment (costs credits) ----------

    def bulk_match(self, people, reveal_personal_emails=False, reveal_phone=False):
        """people: list of dicts with at least {'id': apollo_person_id}. Max 10 per call.

        Each successfully revealed email costs 1 credit. Call this only on a
        scored, prioritized slice.
        """
        if len(people) > 10:
            raise ApolloError("bulk_match accepts max 10 records per call")
        payload = {
            "details": people,
            "reveal_personal_emails": reveal_personal_emails,
            "reveal_phone_number": reveal_phone,
        }
        out = self._post("people/bulk_match", payload)
        matched = [m for m in out.get("matches", []) if m and m.get("email")]
        self.credits_spent += len(matched)
        return out.get("matches", [])
