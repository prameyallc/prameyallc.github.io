# Site map and operations

Public host today: `https://prameyallc.github.io/`  
Sources: `src/` · Generated HTML is committed for GitHub Pages.

## Sitemap

| URL | Page |
|---|---|
| `/` | Home |
| `/apps/` | Portfolio |
| `/apps/<slug>/` | App page (ten public apps) |
| `/standard/` | Four rules |
| `/about/` | Company |
| `/privacy-model/` | Architecture + links to the privacy hub |
| `/contact/` | Email and support facts |
| `/resources/` | Index |
| `/resources/brand/` | Tokens, accents, icons, copy rules |
| `/resources/faq/` | FAQ |
| `/resources/one-pagers/company/` | Printable company sheet |
| `/resources/one-pagers/portfolio/` | Printable portfolio sheet |
| `/sitemap.xml` | This host only |
| `/robots.txt` | Points at the sitemap |

**Not in this repo:** `/privacy/` — served by `prameyallc/privacy`.

**Not a product page:** OmniOps.

## Add an app

1. Add a 256 px icon to `assets/icons/`.
2. Add a record to `src/apps.json` (group slug list + app object).
3. `python3 src/build_site.py`
4. `python3 -m unittest tests.test_site -v`

## Change status when an app ships

1. Set `status` to `available` and `store_url` to the real App Store URL.
2. Rebuild. Do not change the hard line, features, or summaries unless the shipping app actually changed — and then check the privacy policy first.

## Custom domain `prameya.legal`

The domain is verified to the GitHub org. To point it at **this** repo later:

1. Add a `CNAME` file containing `prameya.legal`.
2. GitHub → repo → Pages → custom domain, enforce HTTPS.
3. Set `BASE_URL` in `src/build_site.py` to `https://prameya.legal` and rebuild.

This repo then becomes `https://prameya.legal/`. The privacy **project** site remains `https://prameyallc.github.io/privacy/` unless a separate mapping is created. Keep policy links absolute until that changes.

Do not add the CNAME until that cutover is intended: it will redirect the org site.

## Accessibility and performance

- Target WCAG 2.2 AA. Skip link, visible focus, CSS-only mobile menu, `prefers-reduced-motion`.
- `--dim` is used for small status type instead of the old `--faint` grey.
- Zero third-party requests at runtime. The only outbound links are GitHub, X, mailto, Apple (when `store_url` exists), and the privacy hub.
- No webfonts. Icons are local PNGs.

## Builder

Stdlib Python only. Same idea as the privacy site: generate HTML on the author’s machine, commit the output, GitHub Pages serves files.
