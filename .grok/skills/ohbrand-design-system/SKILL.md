---
name: ohbrand-design-system
description: Keep Prameya company-site colour, type, spacing, and components aligned with the existing dark OHBrand system. Use when editing CSS, templates, or app accents, or when the user runs /ohbrand-design-system.
---

Read `AGENTS.md` (tokens) and `assets/css/site.css` (components). App accents live only in `src/apps.json`.

Do:

- Reuse `.btn`, `.status`, `.app`, `.p`, `.kicker`, `.eyebrow`.
- Keep system fonts. Do not add a webfont.
- Use each app's catalog accent via `--a`. Do not restyle from privacy-hub dots.
- Mobile nav is CSS `<details>`, not JavaScript.

Do not invent a new logo or replace `assets/icons/`.
