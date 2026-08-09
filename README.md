# Prameya LLC — Landing Page

**Expert knowledge for everyone.**

This is a clean, modern, single-file landing page ready for your GitHub Pages site:
https://github.com/prameyallc/prameyallc.github.io

## How to upload

### Option 1 — GitHub Web UI (easiest)
1. Go to https://github.com/prameyallc/prameyallc.github.io
2. Click on `index.html`
3. Click the pencil icon (Edit)
4. Delete all existing content
5. Paste the entire contents of this `index.html`
6. Scroll down → Commit changes
7. Wait 30–60 seconds, then visit https://prameyallc.github.io

### Option 2 — Git push
```bash
git clone https://github.com/prameyallc/prameyallc.github.io.git
cd prameyallc.github.io
# replace index.html with the one from this folder
git add index.html
git commit -m "Add Prameya landing page"
git push
```

## How to add more apps (scale to 100)

Open `index.html` and find any `<article class="app-card" ...>` block.

Copy the entire block, paste it again, then change:
- `data-name="..."` (used for search)
- the emoji
- the `<h3>` title
- the `<p>` description
- the button text / link

The search bar and responsive grid will automatically handle dozens or hundreds of cards.

## Customization tips
- Change the accent color by editing the `--accent` CSS variable
- Replace “Coming soon” buttons with real links when apps go live
- Add categories later by adding data-category attributes + filter buttons if needed

---

© 2026 Prameya LLC
