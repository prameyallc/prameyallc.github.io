# Launch Checklist for Prameya LLC Site

## ✅ Completed

### Pricing Infrastructure
- [x] Added three-tier pricing model to all 10 apps in `src/apps.json`
- [x] Created `/pricing/` page explaining the pricing philosophy
- [x] Added "Pricing" to main navigation
- [x] Integrated pricing tables into all app pages
- [x] Styled pricing components matching the design system
- [x] All tests passing (15/15)
- [x] Site rebuilt successfully (22 pages)
- [x] Updated CLAUDE.md documentation

### Pricing Model Summary

**Free Tier**
- Full access to knowledge layer (reference libraries, guides, sources)
- Respects "knowledge layer is free" principle
- No account, no time limit

**Paid App** (One-time purchase)
- Health apps: $2.99-$4.99
- Professional apps: $7.99-$14.99
- Learning apps: $6.99-$19.99
- Unlocks: unlimited usage, complete history, offline models, all platforms

**Pro Subscription** (Optional IAP)
- $1.99-$7.99/month (annual options save 40-50%)
- Adds: export, analytics, cloud backup, priority support

---

## ❌ Still Needed for Full Launch

### 1. **Build the Actual Apps**
The website is just marketing. You need to:
- [ ] Develop the iOS/Mac apps for all 10 products
- [ ] Implement the three-tier pricing in App Store Connect
- [ ] Configure in-app purchases for Pro subscriptions
- [ ] Submit apps for App Store review

### 2. **Add Real Content to Website**
- [ ] **Screenshots**: Replace placeholder "Screenshots will appear here" with real app screenshots
- [ ] **App Store links**: Get actual URLs from App Store Connect
- [ ] Update `src/apps.json` when apps ship:
  ```json
  "status": "available",
  "store_url": "https://apps.apple.com/..."
  ```

### 3. **Optional Enhancements**
- [ ] Add app demo videos
- [ ] Create press kit/media assets
- [ ] Set up analytics (if desired, respecting privacy principles)
- [ ] Domain cutover to `prameya.legal` (see CLAUDE.md)
- [ ] Add testimonials/reviews (only real ones, per marketing rules)

---

## 🚀 When an App Ships

```bash
# 1. Edit src/apps.json
# Change status to "available" and add real store_url

# 2. Rebuild site
python3 src/build_site.py

# 3. Run tests
python3 -m unittest tests.test_site -v

# 4. Commit and push
git add .
git commit -m "Launch OmniSalub on the App Store"
git push origin main

# GitHub Pages will automatically deploy
```

---

## 📊 Current Site Status

**Pages**: 22 total
- Homepage
- /apps/ (portfolio index)
- /apps/{slug}/ (10 app pages)
- /pricing/ ✨ NEW
- /standard/
- /about/
- /privacy-model/
- /contact/
- /resources/ (+ 4 sub-pages)

**Tests**: 15/15 passing ✅
**Marketing constraints**: All enforced via test suite
**Privacy split**: Correctly maintained (no /privacy/ in this repo)
**Design system**: Fully styled, mobile responsive

---

## 🎯 What Makes You Launch-Ready

✅ **Website is production-ready**
- Clean, professional design
- Pricing clearly explained
- Marketing constraints enforced
- Mobile responsive
- Zero third-party tracking
- Fast static site

❌ **Apps themselves need to be built**
- This repo is just the marketing site
- The actual iOS/Mac apps don't exist yet
- App development is the critical path to launch

---

## 💡 Next Steps

**Immediate priority**: Build the apps
1. Start with one app (recommend OmniMath or OmniPhysics - simpler scope)
2. Implement the free/paid/pro tier structure
3. Submit to App Store
4. Update website when approved
5. Repeat for remaining 9 apps

**Website is ready to support the launch whenever you ship.**

---

*Last updated: 2026-08-26*
