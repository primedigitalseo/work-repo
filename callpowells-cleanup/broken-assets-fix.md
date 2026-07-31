# Broken JavaScript & Redirected Images — Diagnosis & Fix

**Audit issues addressed:** "Page has broken JavaScript" (141 pages), "JavaScript broken"
(3 resources), "Page has redirected image" (141 pages), "Image redirects" (2 resources).

## Root cause (identified from the site's own homepage HTML across all 3 cities)

A **third-party ad-retargeting / data-broker pixel stack** is injected site-wide. The offenders:

- **3 scripts from `s.ksrndkehqnwntyxlhgto.com`** — `154310.js`, `154061.js`, `154311.js`.
  This matches the audit's "JavaScript broken = 3 resources" exactly. The domain is a random,
  unbranded string (typical of retargeting/data-broker pixels) and is loading on every page.
- **A `cnv.event.prod.bidr.io/log/cnv` tracking pixel** (bidr.io = Beeswax/BidR ad exchange)
  loaded as an `<img>` that returns a redirect — matches the "redirected image" flag.

Because these load on the shared header/footer template, they fire on ~141 pages, which is why
one root cause shows up as a site-wide issue count.

> **Confirm before removing:** Ahrefs API units were exhausted at the time of writing, so the
> exact broken-resource URLs should be re-verified in the Site Audit (Issues → "JavaScript
> broken" / "Image redirects") once units reset. The list below is derived from the live
> homepage HTML and is high-confidence, but confirm the client isn't running an active paid
> retargeting campaign through this vendor before pulling it.

## Action for Viktor

1. **Locate the injection.** These snippets are almost certainly added via one of:
   - A tracking/header-footer plugin (e.g., "Insert Headers and Footers", GTM container, or the
     `seo-automated-link-building` plugin also present on the site), **or**
   - Google Tag Manager (`googletagmanager.com/gtag/js` is loaded 24×) firing the pixel as a tag.
   Check GTM first, then header/footer injection plugins, then theme header.
2. **Remove the `ksrndkehqnwntyxlhgto.com` scripts and the `bidr.io` conversion pixel** unless
   the client confirms an active campaign using them. If it's an active campaign, replace the
   broken/redirecting versions with the vendor's current snippet instead of deleting.
3. **Optional hardening:** the CDN-hosted jQuery 3.4.1 and Materialize 1.0.0 can be served
   locally (or jQuery dropped in favor of WP core) to remove external render dependencies.
4. **Re-crawl in Ahrefs** to confirm the "broken JavaScript" and "redirected image" counts drop
   toward zero.

See **`broken-assets-fix.csv`** for the row-by-row list.

## Why it matters for ranking

Broken/blocked scripts and redirecting assets on every page add render errors and latency that
feed the site-quality signal. Clearing one injected vendor stack resolves ~140 page-level flags
at once — the highest issue-count-per-effort fix in the audit after the 404 cleanup.
