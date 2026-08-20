# Pre-ship QA checklist

Blocking. Every item is a failure mode already paid for in a client account.
Run it before the Doc goes into the client's `New Q&A blogs` folder.

## Selection

- [ ] **Question came off the qualified backlog.** Not a client suggestion, not
      a gap someone noticed, not an idea from a call.
- [ ] **Cluster has 4 or more variants.** Fewer, it goes back to the backlog.
- [ ] **All variants are covered in this one post.** Nothing split to a second
      URL. Bedrock's 10-keyword post exists because nothing was split off it.
- [ ] **No existing post covers this cluster.** If one does, extend that URL.
- [ ] **Gate evidence is fresh.** Head-term volume >= 150 and no `images` in
      `item_types`, re-checked if the cluster was qualified over 90 days ago.

## Structure

- [ ] **Direct answer complete in the first 40 to 60 words.**
- [ ] **Nothing above that answer.** No brand copy, no CTA, no scene-setting, no
      restating the question.
- [ ] **The opening block survives being lifted out.** Read it alone. If it needs
      the paragraph after it to make sense, rewrite it.
- [ ] **One H2 per fan-out phrasing, worded as extracted.** No smoothing, no
      merging, no invented headings.
- [ ] **Cost or timeline H2 present**, even on a symptom post.
- [ ] **Each H2 answers itself in its first sentence.**

## Compliance

- [ ] **Exactly one schema type.** FAQPage or Article. Never both. Check what the
      SEO plugin already emits before adding.
- [ ] **Schema not deployed through OTTO.**
- [ ] **Zero em dashes.** Search for the character. Google Docs inserts them on
      its own from a double hyphen.
- [ ] **No geo modifier** in the title, slug, or any H1/H2.

## Handoff

- [ ] **Doc filename is exactly the head question**, interrogative. No client
      name, no "Blog -" prefix, no date. This filename becomes the WordPress
      title and the slug.
- [ ] **Doc is in the client's `New Q&A blogs` folder.**
- [ ] **Previously posted Docs have been moved out of that folder.** The Make
      scenario has no archive step and reposts anything it still finds.

## Post-publish

- [ ] **URL registered in the verification log** with its five poll dates
      (day 3, 7, 14, 21, 30).
