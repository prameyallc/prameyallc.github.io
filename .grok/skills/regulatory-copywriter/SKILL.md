---
name: regulatory-copywriter
description: Enforce Prameya marketing rules on company-site copy. Use when writing or editing app pages, headlines, CTAs, FAQs, one-pagers, or AGENTS.md, or when the user runs /regulatory-copywriter.
---

Read `AGENTS.md` before changing copy. That file is the source of truth.

Checklist for every sentence you add:

- Capability and behaviour only. No outcomes.
- No professional role as a positive claim.
- OmniDent: do not write “does not diagnose”. Follow the 24 August 2026 privacy policy.
- No users, ratings, market sizes, or other unverifiable numbers.
- Availability is “In development” unless `store_url` in `src/apps.json` is a real App Store URL.
- CTAs: Explore, Write to us, Read the privacy model. Never a shipping download button, never a waitlist.
- Do not import privacy-hub taglines into marketing cards.

After edits, run `python3 src/build_site.py` and `python3 -m unittest tests.test_site -v`.
