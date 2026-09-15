# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Test Commands

```bash
# Generate HTML from sources
python3 src/build_site.py

# Run all tests
python3 -m unittest tests.test_site -v
```

**Critical workflow:** This is a static site generator. Sources live in `src/`, generated HTML is committed to the repo root, and GitHub Pages serves the generated files directly from `main`. Never hand-edit generated HTML — the next build will overwrite it.

## Architecture

### The Generator Pattern

`src/build_site.py` is a stdlib-only Python generator that:
1. Reads `src/apps.json` (the canonical catalog of all eleven apps)
2. Reads page fragments from `src/pages/*.html`
3. Writes complete HTML files to the repo root
4. Outputs `sitemap.xml`, `robots.txt`, and `.nojekyll`

The builder uses **depth-relative paths** — each page knows how many `../` it needs to reach the root. Navigation, footer, and all internal links are computed from depth.

### The Data Model

`src/apps.json` is the single source of truth for:
- App metadata (slug, name, legal_name, icon, accent color)
- Status and availability (`status`, `store_url`)
- Marketing copy (audience, summary, detail, features, platforms)
- The "hard line" each app does not cross
- Privacy policy URLs
- **Pricing structure** (free_tier, pro_subscription with monthly / yearly / lifetime)

Apps are grouped into four categories (health, professional, operator, learning). The eleven public apps are listed in `EXPECTED_SLUGS` in the test file. OmniOps is in the catalog.

### Pricing Model

Each app has a two-layer pricing structure in `apps.json`:

1. **Free tier** — Full access to the knowledge layer (reference libraries, guides, sources) plus the user's own records and raw export. Respects the "knowledge layer is free" principle.
2. **Pro** — Optional IAP: monthly, annual, and lifetime of the same tools (formatted export, history depth, domain tools). No cloud backup SKU. No separate one-time "Full App."

The `pricing_table()` function in `build_site.py` generates pricing cards for each app page. The `/pricing/` page explains the overall model.

### Page Fragment System

Files in `src/pages/*.html` use template variables like `{{prefix}}`, `{{apps}}`, `{{email}}`, `{{app_mailtos}}`, etc. The `load_fragment()` function replaces these at build time. Fragments are pure HTML with no logic — all structure and conditionals live in the Python generator.

### Design Tokens

Hardcoded in `src/build_site.py`:
- `BASE_URL`: Currently `https://prameyallc.github.io`, will become `https://prameya.legal` on domain cutover
- `PRIVACY_HUB`: Separate site at `/privacy/` (different repo)
- `EMAIL`: `admin@prameya.legal`
- `HF_APPS`: The three apps whose page carries the generic Hugging Face install sentence (omnisalub, omnident, omnilex). OmniMathematics states its optional Ask-model download in its own words through `model_download` in `apps.json`

Each app has its own accent color from the OHBrand design system, stored in `apps.json` and applied via CSS custom properties.

## Marketing and Legal Constraints

The test suite enforces **four non-negotiable rules** that gate all copy:

1. **No outcome claims** — Never "saves you $X", "improves health", "faster approval"
2. **No professional-role claims** — Never "diagnoses", "advises", "represents you" unless explicitly negated
3. **No fabricated numbers** — No user counts, ratings, market sizes
4. **Honest availability** — An app is `in_development` until submitted, `in_review` while App Review has it (OmniMathematics), and `available` only with a real App Store `store_url`; site-wide availability sentences are computed from these statuses

### OmniDent Special Case

OmniDent's privacy policy (24 August 2026) **withdrew the blanket "does not diagnose" claim** because on-device chat is unfiltered. The test suite enforces that the OmniDent page must not restore that sentence. Use the nuanced language from `apps.json` instead: "has no FDA authorization", "do not act on chat or photo-note text", "ask a dentist".

### Privacy Policy Split

This repo must **never create a `privacy/` directory**. Privacy policies are served by the separate `prameyallc/privacy` project. Always link them absolutely: `https://prameyallc.github.io/privacy/`.

## Test-Driven Copy

The test suite (`tests/test_site.py`) is a contract test that reads both the source (`src/apps.json`) and the generated HTML to catch drift before publish. Tests verify:
- The ten expected apps are present and OmniOps is absent
- Each app page includes its hard line, status, and privacy URL
- No forbidden marketing phrases appear anywhere
- External URLs stay inside the allowlist (GitHub, X, mailto, Apple, privacy hub, schema.org)
- No third-party fonts, scripts, or analytics (zero network requests at runtime)
- Unique titles and canonical URLs for every page

If a test fails, the build is broken and must not be pushed.

## Changing App Status

When an app is submitted to App Review, set `"status": "in_review"` (keep `store_url` null) and rebuild. When an app ships:
1. Set `"status": "available"` in `src/apps.json`
2. Set `"store_url"` to the real `https://apps.apple.com/…` URL
3. Run `python3 src/build_site.py`
4. Run tests to verify
5. Commit the updated `apps.json` and generated HTML

The badge changes from "In development" to "On the App Store" and a CTA button appears.

## Domain Cutover Notes

The site will eventually move from `https://prameyallc.github.io/` to `https://prameya.legal/`. When that happens:
1. Add a `CNAME` file with `prameya.legal`
2. Configure custom domain in GitHub Pages settings
3. Update `BASE_URL` in `src/build_site.py` to `https://prameya.legal`
4. Rebuild and commit

The privacy hub will remain at `https://prameyallc.github.io/privacy/` unless separately mapped. Keep policy links absolute until then.

## Tone and Voice

Calm, precise, anti-hype. The tagline is "Expert knowledge for everyone" — the mission is translation of professional knowledge, not replacement of professionals. The portfolio concept is "better client, not a substitute". Copy should be confident but never make promises these apps do not keep.
