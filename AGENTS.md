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
4. Honest availability. All eleven public apps are in development until `store_url` is a real App Store URL. Never “Download now.” Never an Apple badge CDN.

Copy source of truth for capabilities is the landing-card text in `src/apps.json`, which was taken from the previous `index.html`. Do **not** import privacy-hub taglines (“dental photo analysis and coaching”, “legal AI for professionals”).

Privacy-policy facts that constrain marketing:

- OmniDent (24 August 2026) withdrew a blanket “does not diagnose” claim because on-device chat is unfiltered. The OmniDent page must not restore that sentence.
- Hugging Face model-file downloads in the shipping story are OmniLex, OmniDent, and OmniSalub only. Quote the privacy hub; do not paraphrase it stronger or weaker.
- OmniDerm’s shipping build does not assess a skin photograph. Journal JPEGs stay on device and are not analysed.
- OmniRx’s shipping build does not download a model and does not take photographs.
- OmniOps is a public portfolio app (operator journal). It does not certify, audit, or total avoided cost.

## Four principles

Runs on your device. Every claim has a source. The knowledge layer is free. It won’t pretend to be your professional.

Name exceptions on `/privacy-model/`. Do not quietly rewrite a principle to hide a network connection.

## Privacy split

Do not create a `privacy/` directory here. That URL is the separate `prameyallc/privacy` project. Link it absolutely: `https://prameyallc.github.io/privacy/`.

Support facts live at `/privacy/support/`: person-monitored inbox `admin@prameya.legal`, 45-day aim, no mailing list, do not send skin photos / medical records / medication lists.

## Availability CTAs

Mailto, not a list. Prefill `mailto:admin@prameya.legal?subject=…`. Do not promise a launch notification.

## Status protocol

In `src/apps.json`:

1. `"status": "available"`
2. `"store_url": "https://apps.apple.com/…"` (real URL only)
3. Rebuild. Badge becomes “On the App Store”; a text App Store link appears.

OmniOps is in the public catalog (`src/apps.json` group `operator`). Do not remove it to “match an older ten-app landing.”

## Design tokens

`--bg #0B0B0E`, `--bg2 #131318`, `--card #17171D`, `--line #26262F`, `--ink #F2F3F6`, `--dim #9A9CA8`, `--brand #4DA3F0`. App accents are in `src/apps.json` (OHBrand from the old landing cards, not privacy-hub dots). System fonts only. No third-party scripts, fonts, or analytics.

## Tone

Calm, precise, anti-hype. Better client, not a substitute. Expertise translation, not replacement.
