# Tankless Water Heater Service Page: Bedrock Plumbing & Drain Cleaning

**Client:** Bedrock Plumbing & Drain Cleaning (St. Louis Park, MN GBP)
**Page type:** Service page (Prime Digital service-page wireframe, 12 sections)
**Service area:** Twin Cities metro
**Recommended URL:** `/tankless-water-heater-installation/`
**Prepared:** September 2026

---

## 0. RESEARCH LIMITATIONS (read this first)

This session's network policy blocked direct page fetching. `bedrockplumbers.com` and every competitor domain returned `EGRESS_BLOCKED` / 403 through both WebFetch and curl.

**What the research below IS built on:** Ahrefs API (keyword volumes, difficulty, SERP features, SERP overview, crawled-page inventory, organic keywords, top pages for bedrockplumbers.com), live web search results and snippets, DataForSEO business data, and published cost/code/water-quality sources.

**What could NOT be verified directly:** competitor on-page word counts, heading structures, and schema markup. Competitor coverage below is inferred from titles, snippets, and ranking keywords. Word count target is a vertical benchmark, not a measured median. If you want measured competitor word counts, run this from a session with open egress or paste the competitor HTML in.

**Client data flagged `[VERIFY]`** came from directory listings, not from the GBP via Zapier or DataForSEO. Confirm before publish.

---

## 1. STRATEGY RECOMMENDATION

### Build one page, not three

Repairs, replacements, and installs belong on a single tankless page. Three separate pages would split link equity across keywords that have almost no standalone geo volume, and they would compete with each other in a metro where Bedrock is already ranking on proximity rather than page authority.

### Reclaim the existing URL

Ahrefs crawl data shows `bedrockplumbers.com/tankless-water-heater-installation/` currently returns a **301**, and beneath it sits an abandoned city silo:

```
/tankless-water-heater-installation/bloomington-mn      404
/tankless-water-heater-installation/chanhassen-mn       404
/tankless-water-heater-installation/deephaven-mn        404
/tankless-water-heater-installation/eden-prairie-mn     404
/tankless-water-heater-installation/edina-mn            301
/tankless-water-heater-installation/minneapolis-mn      404
/tankless-water-heater-installation/minnetonka-mn       404
... 25+ more, nearly all 404
```

**Action for JM:** check where `/tankless-water-heater-installation/` currently redirects. If it points at the homepage or a generic services page, publish the new page at that exact URL so it inherits the existing link history and any residual crawl signal. Leave the city subfolder 404s alone. They should not come back. City-level tankless demand does not exist in this metro (see keyword table).

### Keyword targeting

Geo-modified tankless keywords are nearly empty in this metro. The volume sits in "near me" queries that Google resolves by proximity, and in informational cost and comparison queries.

| Keyword | US volume | KD | CPC | SERP features | Notes |
|---|---|---|---|---|---|
| tankless water heater cost | 23,000 | 1 | $0.35 | AI Overview, PAA, shopping | Informational, AI Overview eats the click |
| tankless water heater installation near me | 14,000 | 0 | $4.50 | **Local Pack**, PAA, paid | The money term. Proximity + relevance decides it |
| tankless water heater repair near me | 4,100 | 0 | **$14.00** | **Local Pack**, PAA | Highest commercial value on the list |
| tankless vs tank water heater | 3,100 | 1 | $0.03 | AI Overview, PAA | Capture on-page, not as a separate post |
| tankless water heater installation cost | 2,000 | 0 | $2.00 | AI Overview, PAA | On-page pricing section target |
| tankless water heater flush | 1,200 | 2 | $0.50 | AI Overview, PAA | Maintenance angle, ties to hard water |
| water heater repair minneapolis | 450 | 0 | **$30.00** | Local Pack, PAA | Parent category, Local Pack driven |
| tankless water heater installation minneapolis | 70 | n/a | n/a | none | Thin. Do not build around it |
| tankless water heater minneapolis | 10 | n/a | n/a | none | Thin |
| tankless water heater repair minneapolis | 0 | n/a | n/a | none | No standalone demand |

**Implication:** the page wins on Local Pack association plus topical depth, not on an exact-match geo headline. Put "Twin Cities" in the H1 for relevance and user clarity, then earn the "near me" impressions through GBP proximity, service-page relevance, and internal links from the eleven existing city pages.

### Where Bedrock stands today

| Metric | Value |
|---|---|
| Organic keywords (US) | 69 |
| Organic traffic | 283/mo |
| Keywords in top 3 | 18 |
| Traffic value | ~$984/mo |
| Water heater service page | **None exists** |

Every water-heater keyword Bedrock ranks for lands on a blog post. There is no commercial page collecting that intent. That is the gap this page fills.

---

## 2. SERP ANALYSIS BRIEF

**Seed keywords:** tankless water heater installation near me · tankless water heater repair near me · water heater repair minneapolis

### Local Pack (water heater repair minneapolis, Ahrefs SERP overview)

1. Water Heaters Now!
2. O'Boys Plumbing, Furnace & AC Repair
3. Paul Bunyan Plumbing & Drains

Bedrock is not in this pack. The pack is dominated by water-heater specialists and high-review-count generalists.

### Organic landscape for the same query

| Pos | URL | DR | Page traffic | Notes |
|---|---|---|---|---|
| 2 | reddit.com r/Minneapolis thread | 100 | 99 | "Best companies for replacing a water heater" |
| 4 | rotorooter.com | 74 | 7,768 | National brand, city-templated |
| 5 | centerpointenergy.com | 77 | 103 | Utility page |
| 6 | callhero.com/Services | 28 | 52 | Thin services page |
| 7 | yelp.com | 94 | 85,075 | Directory |
| 8 | sedgwickheating.com | 16 | 28 | Thin services page |
| 9 | thumbtack.com | 90 | 83 | Directory |
| 10 | paulbunyanplumbing.com | 14 | 48 | Local |

**Read:** positions 6, 8, and 10 are held by pages with DR 14 to 28 and near-zero page-level authority. This SERP is not gated by backlinks. A genuinely better page from a DR-low local domain can rank here.

### Twin Cities tankless competitor set

| Competitor | Tankless URL | Observed positioning |
|---|---|---|
| Genz-Ryan | `/plumbing/tankless-water-heaters/` | "Since 1950," heavy brand trust, broad HVAC site |
| Paul Bunyan Plumbing | `/water-heaters/tankless-water-heater-installation/` | Install and repair, Minneapolis and St. Paul |
| 4Front Energy | `/plumbing/tankless-water-heaters/` | Publishes Minneapolis permit content, code-aware |
| Twin Cities Premier Plumbing | `/tankless-water-heaters/` | Names suburbs including St. Louis Park, same-day angle |
| MN Plumbing & Home Services | `/st-louis-park-mn-55426/` | ZIP-targeted city page, tankless as a line item |
| Northern One Hour / Ben Franklin | `/water-heaters/.../tankless-water-heaters/` | Franchise template |

### Coverage read (inferred from titles, snippets, and ranking keywords)

| Topic | Genz-Ryan | Paul Bunyan | 4Front | TC Premier | MN Plumbing |
|---|---|---|---|---|---|
| Install + repair both covered | yes | yes | yes | yes | partial |
| Named suburb coverage | yes | partial | partial | yes | yes |
| Transparent starting prices | no | no | no | no | no |
| Tankless-specific symptom list | no | no | no | no | no |
| Minnesota winter sizing math | no | no | no | no | no |
| Local water hardness and descaling cadence | no | no | no | no | no |
| Permit and MN Rules 4714 detail | no | no | partial (blog) | no | no |
| Gas line and venting reality | no | no | no | no | no |
| FAQ with schema | partial | partial | partial | no | no |
| Service-tagged reviews on page | no | no | no | no | no |

### Gaps worth taking

**Mandatory inclusions** (two or more competitors cover these, so the page cannot skip them):
- Install, replacement, and repair in one place
- Named Twin Cities suburb coverage
- Brand names serviced
- Same-day and emergency availability
- Process from call to cleanup

**Differentiation opportunities** (nobody in this metro covers these well):
1. **Winter sizing math.** Twin Cities groundwater enters homes at 35°F to 42°F in January. Reaching a 110°F tap means a roughly 70°F rise, and a unit rated at its box number loses roughly 25 to 30 percent of that flow on a January morning. Every competitor sells "endless hot water" without saying this. It is the single most useful thing a Minnesota homeowner can learn before buying.
2. **Hard water descaling cadence tied to actual local numbers.** St. Louis Park water runs about 18 grains per gallon from limestone and sandstone aquifer wells. Minneapolis surface water runs roughly 5.5 to 7 gpg after lime softening. Same unit, very different maintenance schedules. Bedrock already has a `/water-softener/` page to link into.
3. **Pricing transparency.** No Twin Cities tankless page publishes starting prices. Three tiers with honest starting numbers is an immediate differentiator.
4. **Tankless-specific symptoms.** Everyone lists tank symptoms (rusty water, puddle under the tank). Nobody lists cold water sandwich, error codes, or flow drop when two fixtures run.
5. **Permit reality.** Minnesota Rules 4714 requires a permit and a licensed contractor for water heater replacement, including like-for-like swaps. Inspectors check the T&P valve, venting, and expansion tank. Saying this plainly separates a licensed shop from a handyman.

**Strongest competitor to beat:** Genz-Ryan (site authority, 75-year brand, broad coverage).
**Their weak spot:** generic national-template tankless copy with no Minnesota-specific engineering content and no prices.

**Wedge strategy:** own the Minnesota physics of tankless. Winter groundwater temperature, gas line and venting reality, and local water hardness maintenance, with published starting prices. Be the page a homeowner sends to their spouse before spending $4,000.

**Length target:** 1,100 to 1,400 words of body copy. Competitor pages in this vertical typically run 800 to 1,500. Do not pad past 1,400.

---

## 3. TOKEN BLOCK

### Auto-filled from Ahrefs crawl and site data (verified)

```
{{SERVICE_AREA}}          = Twin Cities metro
{{SERVICE_SLUG}}          = /tankless-water-heater-installation/
{{PRIMARY_CITY}}          = St. Louis Park
{{SERVICE_CATEGORY}}      = Plumbing
City pages (11 live):
  /plumbing-company-st-louis-park-mn/   /plumbing-company-minneapolis-mn/
  /plumbing-company-edina-mn/           /plumbing-company-minnetonka-mn/
  /plumbing-company-hopkins-mn/         /plumbing-company-plymouth-mn/
  /plumbing-company-eden-prairie-mn/    /plumbing-company-chanhassen-mn/
  /plumbing-company-deephaven-mn/       /plumbing-company-wayzata-mn/
  /plumbing-company-blaine-mn/
Related service pages (live):
  /drain-cleaning/  /sewer-line-repair-replacement/
  /boiler-repair-and-replacement/  /water-softener/  /emergency-plumbing-repair/
Tankless blog cluster (live, link these into the page):
  /how-much-does-it-cost-to-install-a-tankless-water-heater-complete-2025-guide/
  /how-to-choose-the-right-size-tankless-water-heater-for-your-home/
  /how-long-does-a-tankless-water-heater-installation-usually-take-expert-insights/
  /how-long-does-a-tankless-water-heater-last-compared-to-traditional-models/
  /comprehensive-maintenance-guide-for-tankless-water-heater-replacement/
  /tankless-water-heater-installation-maintenance-tips-for-optimal-performance/
  /tankless-water-heater-installation-environmental-benefits-for-eco-friendly-homes/
```

### From directories, needs verification before publish `[VERIFY]`

```
{{BUSINESS_NAME}}     = Bedrock Plumbing & Drain Cleaning   [VERIFY exact GBP name]
{{PHONE}}             = (952) 256-9074   [VERIFY: a second number, (952) 260-8584, also appears in listings]
{{ADDRESS}}           = 7000 Oxford St, St. Louis Park, MN 55426   [VERIFY ZIP against GBP]
{{LICENSE_NUMBER}}    = PC999936   [VERIFY against the actual MN license]
{{STAR_RATING}}       = 4.9   [VERIFY via DataForSEO GBP pull]
{{REVIEW_COUNT}}      = 378   [VERIFY via DataForSEO GBP pull]
{{YEARS_IN_BUSINESS}} = 3 (founded 2023)   [VERIFY founding year with client]
{{FAMILY_OWNED}}      = listed as family-owned   [VERIFY before using the phrase]
```

### Local facts used in the copy (sourced, safe to publish)

```
Winter groundwater inlet temp, Twin Cities:  35°F to 42°F in January
Temperature rise needed for a 110°F tap:     ~70°F
Winter flow derate vs rated GPM:             25% to 30%
St. Louis Park water hardness:               ~18 grains per gallon
Minneapolis water hardness:                  ~5.5 to 7 gpg (lime-softened river water)
Permit rule:                                 MN Rules 4714, permit + licensed contractor,
                                             like-for-like swaps included
Inspector checks:                            T&P valve, venting, expansion tank
Gas demand:                                  tankless 150,000 to 199,000 BTU vs ~40,000 BTU tank
Typical gas line result:                     most homes need a 3/4 inch line
Venting:                                     sidewall, terminated above expected snow line,
                                             intake separated from exhaust to prevent frost
Condensate:                                  neutralizer, never routed through unheated space
Minneapolis tankless market pricing:         avg ~$3,823, typical range $1,919 to $6,072,
                                             whole-house up to ~$9,000
```

### Client must confirm `[CONFIRM WITH CLIENT]`

1. `{{RESPONSE_TIME}}`: the promise, not a fact. Same-day? 24/7 emergency dispatch?
2. Three tier starting prices (proposals below)
3. `{{MANUFACTURER_BRANDS}}`: which tankless brands they install and are factory-certified on
4. `{{WORKMANSHIP_WARRANTY}}`: exact length and what it covers
5. `{{FINANCING_TERMS}}`: current terms, or drop the financing tile
6. `{{CURRENT_OFFER}}`: this month's offer
7. Whether they stock descaling kits and offer an annual flush plan
8. Hours (page currently assumes Mon to Fri 7a to 7p, Sat 8a to 4p, 24/7 emergency)

### Proposed price tiers (market-derived, client confirms before publish)

| Tier | Proposed starting price | Basis |
|---|---|---|
| Tankless Service & Descaling | $189 | Diagnostic plus flush, typical metro service call range |
| Tankless Replacement (like-for-like) | $3,900 | Below the $3,823 metro average is not credible for a licensed permit-pulled job, so this sits just above it |
| Tank-to-Tankless Conversion | $5,400 | Adds gas line, venting, condensate, permit. Metro range tops out near $9,000 |

These are proposals from published market data, not Bedrock's numbers. The page copy below carries `[CONFIRM]` placeholders. Swap in real numbers before publish.

---

## 4. PAGE COPY

Wireframe sections labeled for JM. No markdown headings inside copy blocks. Relative links only.

---

### === SECTION 1: HERO ===

**Breadcrumb:** Home › Plumbing › Tankless Water Heaters

**Location tag:** St. Louis Park • Twin Cities metro

**H1:** Tankless Water Heater Installation and Repair in the Twin Cities

**Subheadline:**
Same-day service, a written price before we start, and units sized for 38 degree Minnesota groundwater. Service starting at $[CONFIRM].

**Trust pills:**
Licensed & Insured · Upfront Pricing · Permits Pulled · 4.9/5 (378) `[VERIFY]`

**Primary CTA:** Get Free Estimate →
**Secondary CTA:** Call (952) 256-9074

**Inline quote form fields:** Full Name · Phone · Address or ZIP · Describe your issue
**Form submit:** Get My Free Quote →
**Form subhead:** in 60 seconds

---

### === SECTION 2: SYMPTOMS ===

**Eyebrow:** SYMPTOMS

**H2:** Signs your tankless water heater needs service

**Intro:**
Tankless units fail differently than tanks. No puddle on the floor, just hot water that quits behaving. Most of these we can diagnose in one visit.

**Symptom bullets:**
- Hot water goes cold mid-shower, then comes back
- An error code is flashing on the unit's display
- Water takes noticeably longer to get hot than last year
- Flow drops when the dishwasher and shower run together
- Rumbling, whining, or clicking when hot water runs
- White crusty buildup near the vent or condensate line
- The unit shuts down during long showers and restarts
- It has been more than a year since the last flush

**Closing line:**
If any of these sound familiar, call (952) 256-9074. We can usually diagnose in one visit.

---

### === SECTION 3: WHY US ===

**Eyebrow:** WHY CHOOSE US

**H2:** Why Bedrock Plumbing & Drain Cleaning for tankless water heaters

**Card 1: Sized for Minnesota Winters**
Twin Cities groundwater hits 38 degrees in January. We size for that, not the box.

**Card 2: Permits Pulled and Inspected**
Minnesota Rules 4714 requires a permit on every swap. We pull it and meet the inspector.

**Card 3: Gas and Venting Handled**
Most conversions need a 3/4 inch gas line and new sidewall venting. Both are in the quote.

**Card 4: Descaling on a Local Schedule**
St. Louis Park water runs 18 grains hard. We set your flush interval to match.

**Brand logo row caption:** Brands We Install & Service `[CONFIRM WITH CLIENT: list 3 to 5 brands]`

---

### === SECTION 4: PROCESS ===

**Eyebrow:** OUR PROCESS

**H2:** From call to clean-up

**1. Call or Book Online**
Tell us what the unit is doing. We book a window that works and confirm by text.

**2. On-Site Diagnosis**
We pull the error history, check gas pressure and venting, and test actual flow at the tap.

**3. Written Quote Before Tools Come Out**
You see repair and replacement side by side, with permit and disposal included in the number.

**4. Install, Test, and Walk Through**
We commission the unit, verify temperature rise, hand you the manual, and clean up.

**Closing CTA:** Schedule Your Free Estimate →

---

### === SECTION 5: PRICING ===

**Eyebrow:** PRICING

**H2:** What does a tankless water heater cost in the Twin Cities?

**Intro:**
Price moves with three things: whether your gas line can feed a 199,000 BTU unit, where the vent has to terminate, and whether you are replacing a tankless or converting from a tank. Here is what most jobs look like.

**Tier 1: Tankless Service & Descaling**
Starting at $[CONFIRM]
- Full diagnostic with error code history
- Descaling flush with commercial solution
- Inlet filter clean and flow test
- Written report on remaining unit life

**Tier 2: Tankless Replacement · MOST POPULAR**
Starting at $[CONFIRM]
- New condensing unit sized to your winter demand
- Old unit removed and recycled
- City permit pulled and inspection met
- Workmanship warranty in writing `[CONFIRM length]`

**Tier 3: Tank to Tankless Conversion**
Starting at $[CONFIRM]
- Gas line upsized to feed the new unit
- New sidewall venting terminated above the snow line
- Condensate drain and neutralizer installed
- Permit, inspection, and full commissioning

**Each tier CTA:** Get Exact Quote →

**Closing note:** Every job gets a free written estimate before we start. No surprises.

---

### === SECTION 6: THE MINNESOTA SECTION (added to the standard wireframe) ===

> **Note for JM:** this section is not in the standard service-page wireframe. It is the wedge from the SERP brief and the reason this page beats Genz-Ryan and Paul Bunyan. Place it between Pricing and Recent Jobs. Two short blocks with a small table.

**Eyebrow:** SIZED FOR MINNESOTA

**H2:** Why tankless sizing is different here

**Block 1:**
A tankless heater does not store hot water. It raises the temperature of whatever water walks in the door, and in January that water enters Twin Cities homes between 35 and 42 degrees. Getting a 110 degree shower means a 70 degree rise. The same unit that delivers its full rated flow in Texas gives up 25 to 30 percent of it on a Minnesota winter morning. That is why an undersized unit feels fine in August and runs out of hot water in February. We size on the January number.

**Block 2:**
Hard water is the other Minnesota factor. St. Louis Park draws from limestone and sandstone wells and tests around 18 grains per gallon, roughly three times what Minneapolis river water runs after lime softening. Scale coats the heat exchanger, the unit works harder for the same output, and the warranty gets shaky. Hard-water homes need a flush about once a year. Softened homes can usually stretch to two. If you are not sure which you have, we test it on the first visit. See also /water-softener/.

**Small table: what a 199,000 BTU unit actually delivers here**

| Month | Incoming water | Rise to 110°F | Realistic flow |
|---|---|---|---|
| July | ~65°F | 45°F | Two showers plus a sink |
| January | ~38°F | 72°F | One shower plus one fixture |

Caption: Flow figures are typical for a residential condensing unit. We calculate yours from your actual fixture count.

---

### === SECTION 7: RECENT JOBS ===

**Eyebrow:** RECENT WORK

**H2:** Recent tankless water heater jobs

Six placeholder cards for JM:
- Tankless Water Heater Installation in [CITY] · [MONTH] [YEAR]
- Tank to Tankless Conversion in [CITY] · [MONTH] [YEAR]
- Tankless Descaling in [CITY] · [MONTH] [YEAR]
- Tankless Water Heater Repair in [CITY] · [MONTH] [YEAR]
- Tankless Replacement in [CITY] · [MONTH] [YEAR]
- Gas Line Upgrade for Tankless in [CITY] · [MONTH] [YEAR]

**Right-side link:** View full gallery →

---

### === SECTION 8: REVIEWS ===

**Eyebrow:** REVIEWS

**H2:** Tankless customers, in their own words

**Right-side stat:** 4.9 from 378 reviews `[VERIFY via DataForSEO]`

- [First name], [City] · Tagged: Tankless Water Heater · "[PULL REVIEW FROM DATAFORSEO: customer mentions tankless specifically]"
- [First name], [City] · Tagged: Tankless Water Heater · "[PULL REVIEW FROM DATAFORSEO: customer mentions tankless specifically]"
- [First name], [City] · Tagged: Tankless Water Heater · "[PULL REVIEW FROM DATAFORSEO: customer mentions tankless specifically]"

**Bottom link:** Read all 378 reviews →

---

### === SECTION 9: FAQ ===

**Eyebrow:** FAQ

**H2:** Common questions about tankless water heaters

**1. How much does a tankless water heater cost in the Twin Cities?**
Replacing an existing tankless unit starts at $[CONFIRM]. Converting from a tank starts at $[CONFIRM], because that job usually adds a gas line upsize and new venting. Across the Minneapolis market, most whole-house tankless projects land between roughly $1,900 and $6,100 depending on unit size and what the gas and vent work requires. Every job gets a free written estimate first.

**2. How long does the installation take?**
A like-for-like tankless replacement is usually a single day. A tank-to-tankless conversion runs one to two days, because we are also upsizing gas, running new sidewall venting, and adding a condensate drain. We give you the realistic window in the written quote, not an optimistic one.

**3. Do tankless water heaters actually work in Minnesota winters?**
Yes, when they are sized for it. Groundwater enters Twin Cities homes at 35 to 42 degrees in January, so the unit has to raise it about 70 degrees to reach a comfortable shower. Expect a properly sized condensing unit to give up 25 to 30 percent of its rated flow at that temperature rise. We size on your January demand, which is why we ask how many fixtures run at once.

**4. How often does a tankless unit need to be flushed here?**
Once a year in hard-water homes, which includes most of St. Louis Park at roughly 18 grains per gallon. Homes on softened water or Minneapolis city water can often go two years. Skipping the flush scales the heat exchanger, cuts efficiency, and can void the manufacturer warranty. We can put you on an annual reminder `[CONFIRM plan details]`.

**5. Do I need a permit, and do you pull it?**
Yes, and yes. Minnesota Rules 4714 requires a permit and a licensed contractor for water heater replacement, including an identical like-for-like swap. Bedrock Plumbing & Drain Cleaning pulls the permit with your city and meets the inspector on site. The inspector checks the T&P valve, venting, and expansion tank. Permit cost is included in the quoted price.

**6. Will my gas line and venting work with a tankless unit?**
Often they need changes. A tank heater burns around 40,000 BTU. A whole-house tankless burns 150,000 to 199,000, so most homes need the gas line upsized, commonly to three quarter inch. Venting moves to a sealed sidewall termination set above the expected snow line, with the intake separated so it does not frost over. We check both before quoting, so the number you see is the number you pay.

**7. Should I repair my tankless unit or replace it?**
Under ten years old with a clean maintenance history, repair almost always wins, especially if the fault is a flow sensor, igniter, or scale. Past twelve years, or with a cracked heat exchanger, replacement is the honest answer. We show you both numbers side by side on the same estimate and let you decide.

**8. Are your technicians licensed and insured, and do you offer financing?**
Bedrock Plumbing & Drain Cleaning works under Minnesota plumbing license #PC999936 `[VERIFY]`, and every technician is licensed and insured. We bring proof to the job. Financing terms: `[CONFIRM WITH CLIENT]`.

**Closing box:** Don't see your question? Call us, we answer every call. → (952) 256-9074

---

### === FAQPage JSON-LD (paste into page head via Yoast or Insert Headers & Footers) ===

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How much does a tankless water heater cost in the Twin Cities?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Replacing an existing tankless unit starts at $[CONFIRM]. Converting from a tank starts at $[CONFIRM], because that job usually adds a gas line upsize and new venting. Across the Minneapolis market, most whole-house tankless projects land between roughly $1,900 and $6,100 depending on unit size and what the gas and vent work requires. Every job gets a free written estimate first."
      }
    },
    {
      "@type": "Question",
      "name": "How long does the installation take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A like-for-like tankless replacement is usually a single day. A tank-to-tankless conversion runs one to two days, because we are also upsizing gas, running new sidewall venting, and adding a condensate drain. We give you the realistic window in the written quote, not an optimistic one."
      }
    },
    {
      "@type": "Question",
      "name": "Do tankless water heaters actually work in Minnesota winters?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, when they are sized for it. Groundwater enters Twin Cities homes at 35 to 42 degrees in January, so the unit has to raise it about 70 degrees to reach a comfortable shower. Expect a properly sized condensing unit to give up 25 to 30 percent of its rated flow at that temperature rise. We size on your January demand, which is why we ask how many fixtures run at once."
      }
    },
    {
      "@type": "Question",
      "name": "How often does a tankless unit need to be flushed here?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Once a year in hard-water homes, which includes most of St. Louis Park at roughly 18 grains per gallon. Homes on softened water or Minneapolis city water can often go two years. Skipping the flush scales the heat exchanger, cuts efficiency, and can void the manufacturer warranty. We can put you on an annual reminder [CONFIRM plan details]."
      }
    },
    {
      "@type": "Question",
      "name": "Do I need a permit, and do you pull it?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, and yes. Minnesota Rules 4714 requires a permit and a licensed contractor for water heater replacement, including an identical like-for-like swap. Bedrock Plumbing & Drain Cleaning pulls the permit with your city and meets the inspector on site. The inspector checks the T&P valve, venting, and expansion tank. Permit cost is included in the quoted price."
      }
    },
    {
      "@type": "Question",
      "name": "Will my gas line and venting work with a tankless unit?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Often they need changes. A tank heater burns around 40,000 BTU. A whole-house tankless burns 150,000 to 199,000, so most homes need the gas line upsized, commonly to three quarter inch. Venting moves to a sealed sidewall termination set above the expected snow line, with the intake separated so it does not frost over. We check both before quoting, so the number you see is the number you pay."
      }
    },
    {
      "@type": "Question",
      "name": "Should I repair my tankless unit or replace it?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Under ten years old with a clean maintenance history, repair almost always wins, especially if the fault is a flow sensor, igniter, or scale. Past twelve years, or with a cracked heat exchanger, replacement is the honest answer. We show you both numbers side by side on the same estimate and let you decide."
      }
    },
    {
      "@type": "Question",
      "name": "Are your technicians licensed and insured, and do you offer financing?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Bedrock Plumbing & Drain Cleaning works under Minnesota plumbing license #PC999936, and every technician is licensed and insured. We bring proof to the job. Financing terms: [CONFIRM WITH CLIENT]."
      }
    }
  ]
}
</script>
```

---

### === SECTION 10: SERVICE AREAS ===

**Eyebrow:** WHERE WE WORK

**H3:** Tankless water heater service available in:

**Intro:** Tap your city for local pricing, recent jobs, and same-day availability.

| City | Link |
|---|---|
| St. Louis Park | /plumbing-company-st-louis-park-mn/ |
| Minneapolis | /plumbing-company-minneapolis-mn/ |
| Edina | /plumbing-company-edina-mn/ |
| Hopkins | /plumbing-company-hopkins-mn/ |
| Minnetonka | /plumbing-company-minnetonka-mn/ |
| Plymouth | /plumbing-company-plymouth-mn/ |
| Eden Prairie | /plumbing-company-eden-prairie-mn/ |
| Chanhassen | /plumbing-company-chanhassen-mn/ |
| Deephaven | /plumbing-company-deephaven-mn/ |
| Wayzata | /plumbing-company-wayzata-mn/ |
| Blaine | /plumbing-company-blaine-mn/ |
| Golden Valley | no page yet, render as plain text until one exists |

**Map caption:** GBP MAP EMBED: VERIFY CORRECT LOCATION

---

### === SECTION 11: FINANCING / GUARANTEE BAR ===

**Financing tile:** `[CONFIRM WITH CLIENT]` + subtext "Qualified buyers · 60-second app"
**Warranty tile:** `[CONFIRM WITH CLIENT]` workmanship warranty + subtext "In writing on every job"
**CTA:** Get Pre-Qualified →

> If financing terms are not current, remove this bar rather than publishing a vague claim.

---

### === SECTION 12: FINAL CTA ===

**H2:** Ready to get your tankless water heater done right?

**Subhead:** Same-day service, free written estimate, and a unit sized for February. Starting at $[CONFIRM].

**Primary CTA:** 📞 Call (952) 256-9074
**Secondary CTA:** Get Free Estimate ↑

**Trust strip:** ★ 4.9 (378) · Licensed & Insured · Permits Pulled · Same-Day Service `[VERIFY rating and count]`

---

### === FOOTER ===

Bedrock Plumbing & Drain Cleaning
7000 Oxford St, St. Louis Park, MN 55426 `[VERIFY]`
(952) 256-9074
Mon–Fri 7a–7p · Sat 8a–4p · 24/7 Emergency `[CONFIRM hours]`

**Plumbing Services:** Drain Cleaning · Sewer Line Repair & Replacement · Boiler Repair & Replacement · Water Softener · 24/7 Emergency Plumbing Repair

**Service Areas:** St. Louis Park · Minneapolis · Edina · Hopkins · Minnetonka

License #PC999936 `[VERIFY]` · Fully Insured · © 2026 Bedrock Plumbing & Drain Cleaning

---

## 5. INTERNAL LINKING PLAN

**Into the page (build these links):**
- All 11 city pages: add a tankless line to the services list, linking to `/tankless-water-heater-installation/`
- All 7 live tankless blog posts: add a contextual link in the first 200 words
- `/water-softener/`: link from the hard-water passage
- `/emergency-plumbing-repair/`: link where no-hot-water emergencies are mentioned
- Main services nav

**Out of the page:**
- `/water-softener/` from the hardness block
- `/emergency-plumbing-repair/` from the symptoms closer
- 3 of the tankless blog posts from the FAQ answers (cost guide, sizing guide, install duration)
- The 11 city pages from the service area chips

This turns an orphaned blog cluster into a supported commercial page. That cluster is currently Bedrock's only tankless asset and it points nowhere.

---

## 6. SITE ISSUES FOUND WHILE RESEARCHING

Not in scope for this page, but worth a ticket.

1. **Four competing city URL patterns.** `/plumbing-company-{city}-mn/`, `/plumbers/{city}-mn/`, `/service-areas/{city}-mn/`, and the dead `/tankless-water-heater-installation/{city}-mn/`. That is textbook page bloat and dilutes the city signal.
2. **Templated content bug.** `/service-areas/chanhassen-mn/` and `/service-areas/minnetonka-mn/` both carry the title "Plumbing Services in St. Louis Park, MN." Wrong city in the title tag is a doorway-page signal under current spam guidance. Fix or consolidate.
3. **Thirty-plus 404s under the old tankless silo**, plus 404s across several water-heater Q&A posts that presumably once had links.
4. **No tank water heater service page.** Bedrock ranks for water-heater blog terms with no commercial page to collect them. "water heater repair minneapolis" carries a $30 CPC. Recommend a companion `/water-heater-repair/` page after this one ships.
5. **Date-archive pages are crawlable** (`/2023/07/` through `/2026/09/`). Noindex them.

---

## 7. QA CHECKLIST BEFORE HANDOFF

- [ ] No em dashes anywhere
- [ ] No banned AI phrases
- [ ] Phone number in one format throughout
- [ ] License number in FAQ 8 and footer
- [ ] Exactly 8 symptoms, 4 why-us cards, 4 process steps, 3 tiers, 8 FAQs, 12 city chips
- [ ] Middle pricing tier carries the Most Popular badge
- [ ] Three review placeholders, none invented
- [ ] FAQPage JSON-LD pasted and validated at search.google.com/test/rich-results
- [ ] Schema Q&A text matches on-page text exactly after prices are filled in
- [ ] All `[CONFIRM]` and `[VERIFY]` tokens resolved
- [ ] GBP rating and review count pulled fresh from DataForSEO
- [ ] Published at the reclaimed `/tankless-water-heater-installation/` URL
- [ ] Internal links from the 11 city pages and 7 blog posts are live
