# LocalBusiness Schema — Templates (Tier 4)

One schema block per location page (the `/norfolk/`, `/winchester/`, `/wilmington/` home of each
silo). Fill every `[[PLACEHOLDER]]` with the location's real, verified NAP before deploying.
Validate at validator.schema.org and Google's Rich Results Test after inserting.

**Rules applied (Benner entity framework):**
- `@type` as an array — `["LocalBusiness","Plumber","HVACBusiness"]` (add `"SepticTankService"` where offered).
- Unique `@id` per location, pointing at that location's **ID page** (see `id-page-spec.md`).
- `sameAs` populated with ALL verified external profiles/citations (see `sameas-citation-worksheet.csv`).
- WebPage schema on each location page references the LocalBusiness `@id`.
- Self-referencing; one connected block per page, nothing orphaned.

---

## Winchester, VA (original / anchor location — Powell's Plumbing)

```json
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "Plumber", "HVACBusiness"],
  "@id": "[[WINCHESTER_ID_PAGE_URL]]#business",
  "name": "Powell's Plumbing, Heating & Air",
  "url": "https://callpowells.com/winchester/",
  "telephone": "[[WINCHESTER_PHONE]]",
  "priceRange": "$$",
  "image": "[[WINCHESTER_PRIMARY_PHOTO_URL]]",
  "logo": "https://callpowells.com/[[LOGO_PATH]]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[[WINCHESTER_STREET]]",
    "addressLocality": "Winchester",
    "addressRegion": "VA",
    "postalCode": "[[WINCHESTER_ZIP]]",
    "addressCountry": "US"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": "[[LAT]]", "longitude": "[[LNG]]" },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "[[OPEN]]", "closes": "[[CLOSE]]" }
  ],
  "areaServed": [
    { "@type": "City", "name": "Winchester" },
    { "@type": "City", "name": "[[NEARBY_CITY_1]]" },
    { "@type": "City", "name": "[[NEARBY_CITY_2]]" }
  ],
  "hasMap": "[[GOOGLE_MAPS_URL]]",
  "sameAs": [
    "[[GBP_URL]]",
    "https://www.bbb.org/us/va/winchester/profile/plumber/powells-plumbing-0241-15139",
    "[[FACEBOOK_URL]]",
    "[[INSTAGRAM_URL]]",
    "[[YELP_URL]]",
    "[[ANGI_URL]]",
    "[[OTHER_CITATION_URLS]]"
  ]
}
```

## Norfolk, VA

```json
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "Plumber", "HVACBusiness"],
  "@id": "[[NORFOLK_ID_PAGE_URL]]#business",
  "name": "Powell's Plumbing, Heating & Air — Norfolk",
  "url": "https://callpowells.com/norfolk/",
  "telephone": "[[NORFOLK_PHONE]]",
  "priceRange": "$$",
  "image": "[[NORFOLK_PRIMARY_PHOTO_URL]]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[[NORFOLK_STREET]]",
    "addressLocality": "Norfolk",
    "addressRegion": "VA",
    "postalCode": "[[NORFOLK_ZIP]]",
    "addressCountry": "US"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": "[[LAT]]", "longitude": "[[LNG]]" },
  "areaServed": [ { "@type": "City", "name": "Norfolk" } ],
  "hasMap": "[[GOOGLE_MAPS_URL]]",
  "sameAs": [ "[[GBP_URL]]", "[[ALL_NORFOLK_CITATION_URLS]]" ]
}
```

## Wilmington, NC

```json
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "Plumber", "HVACBusiness"],
  "@id": "[[WILMINGTON_ID_PAGE_URL]]#business",
  "name": "Powell's Plumbing, Heating & Air — Wilmington",
  "url": "https://callpowells.com/wilmington/",
  "telephone": "[[WILMINGTON_PHONE]]",
  "priceRange": "$$",
  "image": "[[WILMINGTON_PRIMARY_PHOTO_URL]]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[[WILMINGTON_STREET]]",
    "addressLocality": "Wilmington",
    "addressRegion": "NC",
    "postalCode": "[[WILMINGTON_ZIP]]",
    "addressCountry": "US"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": "[[LAT]]", "longitude": "[[LNG]]" },
  "areaServed": [ { "@type": "City", "name": "Wilmington" } ],
  "hasMap": "[[GOOGLE_MAPS_URL]]",
  "sameAs": [ "[[GBP_URL]]", "[[ALL_WILMINGTON_CITATION_URLS]]" ]
}
```

---

## Service-page schema (optional, high value)

On each service page, add a `Service` block that ties the service to the location's business
`@id`, so Google connects service → entity → location:

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "[[SERVICE NAME e.g. Water Heater Services]]",
  "provider": { "@id": "[[LOCATION_ID_PAGE_URL]]#business" },
  "areaServed": { "@type": "City", "name": "[[CITY]]" }
}
```

## FAQPage schema

Every page with an FAQ section (the water-heater hubs already have 10 FAQs) should output
`FAQPage` JSON-LD mirroring the visible Q&As. This is a rich-result eligibility win.

## Deploy checklist per location

- [ ] `@type` is an array including Plumber + HVACBusiness (+ SepticTankService where offered)
- [ ] `@id` points at the location's ID page and is identical everywhere that page is referenced
- [ ] NAP exactly matches the GBP and the ID page (character-for-character)
- [ ] `sameAs` includes every verified citation/profile from the worksheet
- [ ] WebPage schema on the page references the LocalBusiness `@id`
- [ ] Validated in Rich Results Test with zero errors
