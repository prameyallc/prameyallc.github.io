# Prameya LLC company site

This repository is the public company site. Edit **sources in `src/`**, then run:

```
python3 src/build_site.py
python3 -m unittest tests.test_site -v
```

Do not hand-edit generated HTML. The next build will overwrite it.

## Marketing rules

1. No outcome claims (“saves you $X”, “improves health”, “faster approval”).
2. No professional-role claims (“diagnoses”, “advises”, “represents you”, “certified”) unless they appear only as a negation, and never as a blanket OmniDent “does not diagnose” line.
3. No fabricated numbers (users, ratings, market sizes).
4. Honest availability. An app is “In development” until it is submitted, “Submitted to App Review” once a submission has gone to Apple, and “On the App Store” only when `store_url` is a real App Store URL (see the status protocol). Never “Download now.” Never an Apple badge CDN. Site-wide copy must stay true for every app: availability sentences are computed from `src/apps.json`, never typed as “all eleven are in development”.

Copy source of truth for capabilities is the landing-card text in `src/apps.json`, which was taken from the previous `index.html`. Do **not** import privacy-hub taglines (“dental photo analysis and coaching”, “legal AI for professionals”).

Privacy-policy facts that constrain marketing:

- OmniDent (24 August 2026) withdrew a blanket “does not diagnose” claim because on-device chat is unfiltered. The OmniDent page must not restore that sentence.
- Hugging Face model-file downloads: quote the privacy hub's sentence, “Some apps can download an optional AI model file from Hugging Face, and only after you choose to; each app's own policy says whether it does and when.” Do not list which apps download on site-wide pages; the hub stopped listing them on 2026-09-15 because the list was not verified. An app's own page may state its own download, as OmniMathematics does from `model_download` in `src/apps.json`. Do not paraphrase the hub stronger or weaker.
- OmniDerm’s shipping build does not assess a skin photograph. Journal JPEGs stay on device and are not analysed. Its Ask output is not filtered and its free library says when to see a dermatologist, so scope “never names a mark” to the journal and do not say the app never tells you whether to see a clinician.
- OmniRx’s shipping build does not take photographs. Its published policy discloses an optional Hugging Face Ask model download (offered only where Apple Intelligence cannot answer), so do not say OmniRx downloads no model.
- No app requires an account, but OmniDent offers an optional Sign in with Apple (Keychain only, no server; its policy section 5). Never write a blanket “No account”; say “No app requires an account” and keep the exception named on `/privacy-model/`.
- OmniCadence (formerly OmniOps; slug `omniops`) is a public portfolio app (operator journal). It does not certify, audit, or total avoided cost.

## Four principles

Runs on your device. Every claim has a source. The knowledge layer is free. It won’t pretend to be your professional.

Name exceptions on `/privacy-model/`. Do not quietly rewrite a principle to hide a network connection.

## Privacy split

Do not create a `privacy/` directory here. That URL is the separate `prameyallc/privacy` project. Link it absolutely: `https://prameyallc.github.io/privacy/`.

Support facts live at `/privacy/support/`: person-monitored inbox `admin@prameya.legal`, 45-day aim, no mailing list, do not send skin photos / medical records / medication lists.

## Availability CTAs

Mailto, not a list. Prefill `mailto:admin@prameya.legal?subject=…`. Do not promise a launch notification.

## Status protocol

`status` in `src/apps.json` takes one of three values. The footer, home page, FAQ, About, Pricing and one-pager availability sentences are computed from it, so change the catalog, not the prose.

- `"in_development"` — not submitted. Badge “In development”; the app page keeps the screenshot placeholder and marks its prices as planned.
- `"in_review"` — submitted to App Review and not on sale; `store_url` stays `null`. Badge “Submitted to App Review”; no screenshot placeholder, no “planned” note. The site cannot see Apple's review state, so the badge says only what stays true through a review, a rejection and a reply. Before publishing a change to `in_review`, read `asc versions list --app <Apple ID>` and confirm the version has been submitted (for example `WAITING_FOR_REVIEW`, `IN_REVIEW` or `REJECTED` after a submission). OmniMathematics has been `in_review` since its first submission in September 2026. OmniAvia has been `in_review` since its iOS 1.0 submission of 26 September 2026 (`asc review history --app 6815145487`: submitted, then rejected under 2.1 Information Needed; the submission stays, so the badge stays true). The other nine have been `in_review` since their iOS 1.0 submissions (`asc versions list`, 27 September 2026: `WAITING_FOR_REVIEW`).
- `"available"` — on sale:
  1. `"status": "available"`
  2. `"store_url": "https://apps.apple.com/…"` (real URL only)
  3. Rebuild. Badge becomes “On the App Store”; a text App Store link appears.

If a submission is withdrawn, set the app back to `"in_development"`.

OmniCadence (slug `omniops`) is in the public catalog (`src/apps.json` group `operator`). Do not remove it to “match an older ten-app landing.”

## Names and slugs

`name` and `legal_name` are the App Store names. Slugs never change, because the page URLs and the privacy URLs are built on them: OmniCadence stays at `/apps/omniops/` and OmniMathematics at `/apps/omnimath/`.

## Design tokens

`--bg #0B0B0E`, `--bg2 #131318`, `--card #17171D`, `--line #26262F`, `--ink #F2F3F6`, `--dim #9A9CA8`, `--brand #4DA3F0`. App accents are in `src/apps.json` (OHBrand from the old landing cards, not privacy-hub dots). System fonts only. No third-party scripts, fonts, or analytics.

## Tone

Calm, precise, anti-hype. Better client, not a substitute. Expertise translation, not replacement.
