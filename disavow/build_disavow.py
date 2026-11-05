"""Build Google disavow files for Prime Digital clients from Ahrefs spam pulls.

Input:  disavow/raw/ahrefs_spam.json  ({client_domain: {ref_domain: {domain_rating, dofollow_links, ...}}})
Output: disavow/<date>/<client-slug>-disavow-<date>.txt, review CSV, summary markdown.
"""
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TODAY = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
OUT = ROOT / TODAY
OUT.mkdir(parents=True, exist_ok=True)

CLIENTS = [
    ("Mikita Door & Window", "mikitadoorandwindow.com"),
    ("Everclear Pools & Spas", "everclearpoolsnj.com"),
    ("Exteriors Plus Roofing Siding & Windows", "exteriorsplusmn.com"),
    ("Bedrock Restoration", "bedrockrestoration.com"),
    ("Care Roofing Inc", "careroofingsolutions.com"),
    ("Bedrock Plumbing", "bedrockplumbers.com"),
    ("Somers Plumbers", "somersplumbers.com"),
    ("Winkler Kurtz LLP", "winklerkurtz.com"),
    ("Redefined Restoration", "redefinedresto.com"),
    ("Conner Roofing", "connerroofing.com"),
    ("Artisan Homes", "artisanhomesnd.com"),
    ("Blue Peaks Roofing", "bluepeaksroofing.com"),
    ("Rembrandt Roofing", "rembrandtroofing.com"),
    ("Pedestals Florist", "pedestalsflorist.com"),
    ("Nationwide Contracting", "nationwidecontractingllc.com"),
    ("Meigel Home Improvements", "meigelhomeimprovements.com"),
    ("Suburban Plumbing Experts", "suburbanplumbingexperts.com"),
    ("DSH Homes and Pools", "dshbuild.com"),
    ("GKontos Roofing", "gkontosinc.com"),
    ("Dream Design & Build", "ddandbllc.com"),
    ("Praiano Kitchen & Bathroom Remodeling", "praianohomes.com"),
    ("Long Island Custom Blinds", "longislandcustomblinds.com"),
    ("Christie & Co Salon", "christiesalon.com"),
]
CLIENT_DOMAINS = {d for _, d in CLIENTS}
MASTER_SOURCE = "connerroofing.com"
TURKISH_SOURCES = {"nationwidecontractingllc.com", "meigelhomeimprovements.com", "dshbuild.com"}

# Rows from the first all-time Conner pull whose links were lost before the Nov 2025 window,
# plus shared hosting/platform roots that must never be disavowed wholesale.
DROP = {"pages.dev", "za.com", "hi-ho.ne.jp", "az.pl", "printwhatyoulike.com", "clicktohigh.com"}

# --- Whitelist (never disavow) ---
WHITELIST_EXACT = {
    "bbb.org", "yelp.com", "homeadvisor.com", "angi.com", "angieslist.com", "thumbtack.com",
    "houzz.com", "nextdoor.com", "mapquest.com", "citysearch.com", "superpages.com",
    "yellowpages.com", "manta.com", "groupon.com", "magicpin.com", "ezlocal.com",
    "intensedebate.com", "prnewswire.com", "businesswire.com", "globenewswire.com", "pr.com",
    "einpresswire.com", "abnewswire.com",
}
WHITELIST_PATTERNS = [r"newswire", r"presswire", r"chamber"]

# Link exchange network, approved to keep (2026-11-05). Never disavow.
LINK_EXCHANGE_KEEP = {
    "campanelloconstruction.com", "northarundelconstruction.com", "nataliegoldsteindds.com",
    "drshadidds.com", "mwberglaw.com", "woodard1law.com", "promedimagining.com",
    "livingstonelandscaping.com", "acacialandscapeservices.com", "pearlstreetautomotive.com",
    "hcdsurgical.com", "massercontractors.com", "villasofestancia.com", "sunwaterweb.com",
    "mixoncci.com", "c4web.net", "garycutler.info", "productivepractice.net", "whosmypro.com",
    "thebestnewsplace.com", "netforumondemand.com", "holzconstruction.com", "handymaxphoenix.com",
    "dunlopelectrical.com", "assurehomehealth.org", "ckframing.com", "expresskitchendesigns.com",
    "brightstaryouth.org", "annikabansal.com", "operation-infinitejustice.org", "find-us-here.com",
}

# --- Flag for Mike's review: real-business-looking domains with dofollow links that recur
# across many clients (possible vendor/partner network or hacked SMB sites), plus
# niche directories that may be citations. ---
REVIEW_EXACT = {
    "campanelloconstruction.com", "northarundelconstruction.com", "nataliegoldsteindds.com",
    "drshadidds.com", "mwberglaw.com", "woodard1law.com", "promedimagining.com",
    "livingstonelandscaping.com", "acacialandscapeservices.com", "pearlstreetautomotive.com",
    "hcdsurgical.com", "massercontractors.com", "villasofestancia.com", "sunwaterweb.com",
    "mixoncci.com", "c4web.net", "garycutler.info", "productivepractice.net", "whosmypro.com",
    "thebestnewsplace.com", "netforumondemand.com", "holzconstruction.com", "handymaxphoenix.com",
    "dunlopelectrical.com", "assurehomehealth.org", "ckframing.com", "expresskitchendesigns.com",
    "brightstaryouth.org", "annikabansal.com", "operation-infinitejustice.org", "trustfeed.com",
    "viesearch.com", "officialsite.com", "apsense.com", "downtobid.com", "allstarpros.com",
    "plumbersbyzip.com", "plumberdirectory.info", "rooferssearch.com", "rooflists.com",
    "roof.info", "roofs.wiki", "roofs.fyi", "septic.fyi", "needseptic.com", "acebizlistings.com",
    "homeservicelookup.com", "ratingsnearme.com", "nearmelisting.com", "localbizindex.com",
    "chicago-directory.com", "lantern.llc", "developmentmi.com", "waterrestoring.com",
    "sunnydayconcrete.com", "beforeattorney.com", "ailegalcounsel.org", "golocalezservices.com",
    "nassaupros.com", "woowholocal.com", "igolocal.app", "profixdirectory.com",
    "servicefinderamerica.com", "stlouistoprated.com", "saintlouispros.com", "united-local.com",
    "contractornearyou.com", "find-us-here.com", "linkcentre.com", "rocklandcounty.info",
    "abetterroofer.com", "a-1roofingnow.com", "iknowaroofer.com", "provenroofer.com",
    "rooferbutler.com", "standrewsbuilders.net", "propanespecialty.com", "repairhomeexperts.com",
    "moldguide.com", "abatelocal.com", "basementlocal.com", "fixhubs.net", "getgrizz.com",
    "afterhourbooking.com", "vendorroster.com", "innovatedblindsconcepts.com",
}
# Review decisions (2026-11-05).
# Keep: real small-business sites (likely more link-exchange partners) and legit platforms.
REVIEWED_KEEP = {
    "allstarpros.com", "downtobid.com", "trustfeed.com", "viesearch.com",
    "innovatedblindsconcepts.com", "jaybirdphotography.com", "lynleephoto.com",
    "thachphotography.com", "msmklawfirm.com", "sunnydayconcrete.com", "standrewsbuilders.net",
    "propanespecialty.com", "doctorsathome.com", "njinspectors.com", "beforeattorney.com",
    "ailegalcounsel.org",
}
# Disavow: auto-generated "nationwide"/city lookalike directories, sitewide-link spam,
# and unrelated foreign sites. No citation or referral value.
REVIEWED_DISAVOW = {
    "a-1roofingnow.com", "abetterroofer.com", "abatelocal.com", "acebizlistings.com",
    "afterhourbooking.com", "asphaltroofingnationwide.com", "basementlocal.com",
    "chicago-directory.com", "contractornearyou.com", "electriciansdaily.news", "fixhubs.net",
    "getgrizz.com", "guttercleaningnationwide.com", "homeservicelookup.com", "igolocal.app",
    "iknowaroofer.com", "localbizindex.com", "moldguide.com", "nassaupros.com",
    "nearmelisting.com", "needseptic.com", "officialsite.com", "plumberdirectory.info",
    "plumbersbyzip.com", "profixdirectory.com", "provenroofer.com", "ratingsnearme.com",
    "repairhomeexperts.com", "rocklandcounty.info", "roof.info", "rooferbutler.com",
    "rooferssearch.com", "rooflists.com", "roofreplacementnationwide.com", "roofs.fyi",
    "roofs.wiki", "saintlouispros.com", "septic.fyi", "servicefinderamerica.com",
    "sidingcontractorbenchmark.com", "stlouistoprated.com", "united-local.com",
    "usametalroofingcontractors.com", "usaresidentialroofingcompanies.com",
    "usaroofleakrepaircontractors.com", "vendorroster.com", "woowholocal.com",
    "golocalezservices.com", "linkcentre.com", "apsense.com", "sitgespoolparty.com",
    "jazminsbeautysalon.be", "jomtien-realty.com", "constructionconsultant.co.za",
    "lawyerinjeddah.com", "waterrestoring.com", "diyprojectsforhome.com", "developmentmi.com",
    "lantern.llc",
}
TRADE_RX = re.compile(
    r"(roof|plumb|septic|construct|contract|builder|law|attorney|legal|dds|dental|landscap|"
    r"electric|restor|blinds|salon|florist|photo|automotive|hvac|siding|window|door|remodel|"
    r"kitchen|bath|pool|spa|gutter|concrete|mold|basement|handyman|inspector|realty|homes?\b)"
)

SPAMMY_TLDS = (".xyz", ".win", ".club", ".top", ".buzz", ".site", ".space", ".icu", ".monster",
               ".shop", ".store", ".online", ".website", ".click", ".fun", ".link")
FOREIGN_RX = re.compile(r"(\.tr$|\.ru$|\.рф$|\.cn$|\.ir$|\.jp$|\.ua$|haber|gundem|psikoloji|ajansportal)")
ADULT_RX = re.compile(r"(porn|sex-|escort|xxx|hdporn|casino|slot|poker|erythromycin|tabs\b|pharma)")
NETWORK_RX = re.compile(
    r"(seoexpress|link-baron|outrank-hq|rank-forge|^\d{6,}\.xyz$|-wiki\.win$|^wiki-[a-z]+\.win$|"
    r"checker|backlink|dapa|serp|rank|seo|index|crawl|anchor|authority|linkpro|seohub|seolink|"
    r"boosthub|ranklab|daily[a-z]+uknews|signalnews)"
)


def dr(row):
    try:
        return float(row.get("domain_rating") or 0)
    except ValueError:
        return 0.0


def whitelisted(d):
    if d in LINK_EXCHANGE_KEEP:
        return "approved link exchange (keep)"
    if d in REVIEWED_KEEP:
        return "reviewed 2026-11-05: real business or legit platform, keep"
    if d in WHITELIST_EXACT or d in CLIENT_DOMAINS:
        return "client domain" if d in CLIENT_DOMAINS else "whitelisted directory/platform"
    for p in WHITELIST_PATTERNS:
        if re.search(p, d):
            return f"whitelist pattern '{p}'"
    return None


def needs_review(d):
    if d in REVIEWED_DISAVOW:
        return None
    if d in REVIEW_EXACT:
        return "recurring real-business / niche-directory domain with dofollow links"
    if TRADE_RX.search(d) and not d.endswith(SPAMMY_TLDS) and not NETWORK_RX.search(d):
        return "trade/business keyword in domain; could be legit citation, partner or hacked SMB site"
    return None


def category(d, row):
    if FOREIGN_RX.search(d) or ADULT_RX.search(d):
        return "foreign"
    if d.endswith(SPAMMY_TLDS) and dr(row) < 50:
        return "tld"
    r = dr(row)
    if r >= 50:
        return "high"
    if r >= 10:
        return "mid"
    return "low"


HEADERS = {
    "high": "High-DR Spam (DR 50+, Ahrefs spam-flagged)",
    "mid": "Mid-DR Spam (DR 10-49, Ahrefs spam-flagged)",
    "low": "Low-DR Spam (DR <10, Ahrefs spam-flagged)",
    "tld": "Wiki Farms / Spammy TLDs",
    "foreign": "Foreign Language / Adult / Pharma Spam",
    "network": "Shared Portfolio Spam Network (from master list, not verified on this domain)",
}


def slug(name):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower().replace("&", "and"))).strip("-")


data = json.load(open(ROOT / "raw" / "ahrefs_spam.json"))
for k in list(data):
    for d in list(data[k]):
        if d in DROP:
            del data[k][d]

master_network = {d for d in data.get(MASTER_SOURCE, {}) if NETWORK_RX.search(d)}
turkish = set()
for src in TURKISH_SOURCES:
    turkish |= {d for d in data.get(src, {}) if FOREIGN_RX.search(d)}

summary_rows, review_rows, excluded_rows = [], [], []
for name, dom in CLIENTS:
    own = data.get(dom, {})
    cats = {k: [] for k in HEADERS}
    excluded, flagged = [], []
    for d, row in own.items():
        w = whitelisted(d)
        if w:
            excluded.append((d, w))
            continue
        rv = needs_review(d)
        if rv:
            flagged.append((d, row, rv))
            continue
        cats[category(d, row)].append(d)
    verified = {d for c in cats.values() for d in c}
    extra = set()
    if dom in TURKISH_SOURCES:
        extra_tr = turkish - verified
        cats["foreign"].extend(sorted(extra_tr))
        verified |= extra_tr
    if dom != MASTER_SOURCE:
        extra = {d for d in master_network - verified if not whitelisted(d) and not needs_review(d)}
        cats["network"] = sorted(extra)

    total = sum(len(v) for v in cats.values())
    fname = OUT / f"{slug(name)}-disavow-{TODAY}.txt"
    lines = [
        "# Google Disavow File",
        f"# Client: {name}",
        f"# Domain: {dom}",
        f"# Generated: {TODAY}",
        "# Source: Ahrefs MCP via Claude",
        f"# Total domains disavowed: {total}",
    ]
    for k, title in HEADERS.items():
        if not cats[k]:
            continue
        lines += ["", f"# --- {title} ---"]
        lines += [f"domain:{d.encode('idna').decode()}" for d in sorted(set(cats[k]))]
    fname.write_text("\n".join(lines) + "\n", encoding="utf-8")

    for d, row, why in flagged:
        review_rows.append([name, dom, d, row.get("domain_rating"), row.get("dofollow_links"), why])
    for d, why in excluded:
        excluded_rows.append([name, dom, d, why])
    summary_rows.append({
        "client": name, "domain": dom, "file": fname.name, "total": total,
        **{k: len(set(v)) for k, v in cats.items()},
        "excluded": len(excluded), "flagged": len(flagged), "pulled": len(own),
    })

with open(OUT / f"flagged-for-review-{TODAY}.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["client", "client_domain", "referring_domain", "domain_rating", "dofollow_links", "reason"])
    w.writerows(sorted(review_rows, key=lambda r: (r[2], r[0])))
with open(OUT / f"excluded-whitelist-{TODAY}.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["client", "client_domain", "referring_domain", "reason"])
    w.writerows(excluded_rows)
with open(OUT / f"summary-{TODAY}.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
    w.writeheader()
    w.writerows(summary_rows)

print(f"master network domains: {len(master_network)}; turkish network domains: {len(turkish)}")
for r in summary_rows:
    print(f"{r['client'][:34]:34} total={r['total']:5} high={r['high']:3} mid={r['mid']:4} low={r['low']:4} "
          f"tld={r['tld']:4} foreign={r['foreign']:4} network={r['network']:4} excl={r['excluded']:2} flag={r['flagged']:3}")
