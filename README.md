# prameyallc.github.io

The Prameya LLC company site — <https://prameyallc.github.io/>

**Expert knowledge for everyone.**

## What's here

| Path | What it is |
|---|---|
| `src/apps.json` | Canonical catalog: copy, accents, status, privacy URLs. |
| `src/pages/` | Unique page bodies. |
| `src/build_site.py` | Stdlib generator. Writes HTML at the repo root. |
| `assets/css/site.css` | Design system. |
| `assets/icons/` | App icons, 256 px, from each app's `OHBrand` accent. |
| `AGENTS.md` | Marketing rules, privacy split, status protocol. |
| `SITE.md` | Sitemap, domain cutover, how to add an app. |

Served by GitHub Pages from `main` at the repository root. Pushing to `main` publishes. Generated HTML is committed; GitHub does not run the builder.

```
python3 src/build_site.py
python3 -m unittest tests.test_site -v
```

Do not hand-edit generated HTML.

## The eleven apps

**Health & the body** — OmniSalub · OmniDent · OmniDerm · OmniRx  
**Professional knowledge** — OmniLex · OmniBuild · OmniWealth  
**Operating discipline** — OmniOps  
**Learning** — OmniMath · OmniAero · OmniPhysics

## Rules this site is written under

1. **No outcome claims.** Never "saves you $X", "improves your health", "faster approval". Behaviour and capability only.
2. **No professional-role claims.** No "certified", "diagnoses", "advises", "represents you" as a positive claim. Each app page states the line it does not cross. OmniDent must not use a blanket "does not diagnose" sentence — its published policy withdrew that wording on 24 August 2026.
3. **No fabricated numbers.** No user counts, no market sizes, no ratings — nothing that isn't verifiable.
4. **Availability stated honestly.** Each app's `status` in `src/apps.json` is `in_development`, `in_review` (submitted to App Review, not on sale) or `available` (with a real `store_url`); see the status protocol in `AGENTS.md`. Site-wide availability sentences are computed from it. Rebuild after changing it.

Contact is `admin@prameya.legal`. That inbox is not a mailing list.

## Design

No fonts, scripts, or assets are fetched from third parties, so a visit does not leak an IP to anyone but GitHub (and destinations the visitor chooses to open). Colours are each app's real accent from the portfolio design tokens (`OHBrand`).

Privacy policies are a **separate** site: <https://prameyallc.github.io/privacy/>. This repo must not publish a `privacy/` directory.
