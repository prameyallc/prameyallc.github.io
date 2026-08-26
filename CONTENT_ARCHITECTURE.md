# Content Architecture & Knowledge Integration

**How to build the knowledge layer into the Prameya apps**

This document outlines the technical architecture for integrating open educational content into on-device applications while maintaining the "knowledge layer is free" principle.

---

## Core Principles

1. **On-device first**: Knowledge base ships with the app
2. **Cited always**: Every claim has a source
3. **Offline capable**: Full functionality without network
4. **Free tier complete**: Reference library not paywalled
5. **Update pathway**: New knowledge via app updates or optional downloads

---

## Content Database Schema

### **Universal Knowledge Record**

Every piece of content (article, concept, procedure) follows this structure:

```json
{
  "id": "uuid-v4",
  "type": "concept|procedure|reference|case_study",
  "app": "omnisalub|omnident|...",
  "title": "Understanding Blood Pressure Readings",
  "slug": "blood-pressure-readings",
  "summary": "One-sentence summary for search results",
  "tier": "free|paid|pro",

  "content": {
    "sections": [
      {
        "heading": "What the numbers mean",
        "body_markdown": "Markdown content with citations[^1]",
        "media": [
          {
            "type": "image|video|interactive",
            "asset_id": "bp-diagram-001",
            "caption": "Normal blood pressure ranges by age",
            "alt_text": "Chart showing systolic and diastolic ranges"
          }
        ]
      }
    ]
  },

  "sources": [
    {
      "id": 1,
      "citation": "NIH NHLBI. Understanding Blood Pressure Readings. Updated 2025-03-15.",
      "url": "https://www.nhlbi.nih.gov/health/high-blood-pressure/diagnosis",
      "license": "Public Domain",
      "accessed": "2026-08-01"
    }
  ],

  "metadata": {
    "reading_level": 8.5,
    "word_count": 450,
    "last_reviewed": "2026-08-15",
    "review_frequency": "quarterly",
    "keywords": ["blood pressure", "hypertension", "vitals"],
    "related_concepts": ["hypertension-basics", "medication-effects-bp"]
  },

  "version": 2,
  "created": "2026-01-10T00:00:00Z",
  "updated": "2026-08-15T00:00:00Z"
}
```

### **Citation Management**

```json
{
  "source_id": "nih-nhlbi-bp-2025",
  "authority": "National Heart, Lung, and Blood Institute",
  "title": "Understanding Blood Pressure Readings",
  "url": "https://www.nhlbi.nih.gov/health/high-blood-pressure/diagnosis",
  "published": "2025-03-15",
  "accessed": "2026-08-01",
  "license": "Public Domain - US Government Work",
  "reliability_score": 5.0,
  "update_frequency": "annually",
  "next_check": "2027-03-15"
}
```

### **Concept Graph**

```json
{
  "concept_id": "hypertension-basics",
  "parent_concepts": ["cardiovascular-health"],
  "child_concepts": ["white-coat-hypertension", "secondary-hypertension"],
  "related_concepts": ["blood-pressure-readings", "lifestyle-modifications"],
  "prerequisites": ["blood-pressure-readings"],
  "difficulty_level": "intermediate",
  "apps": ["omnisalub"]
}
```

---

## Content Tiers & Access Control

### **Free Tier (Knowledge Layer)**
- Complete reference library
- Core concepts (500+ per app)
- Plain-language explanations
- All citations visible
- Basic calculators
- Educational content

**What's included FREE per app:**
- OmniSalub: Vital sign reference, common conditions, visit prep guide
- OmniDent: Oral health encyclopedia, technique guides, preventive care
- OmniDerm: Skin health basics, journaling guide, when-to-see-doctor
- OmniRx: Drug class library, how-to-take guides, medication safety
- OmniLex: Legal code reference, plain-language layer, form templates
- OmniBuild: Code summaries, OSHA/ADA/EPA guides, permit navigator
- OmniWealth: Finance concepts A-Z, basic calculators, cited sources
- OmniMath: First 5 chapters, concept codex, sample problems
- OmniAero: ACS overview, basic 14 CFR, sample lessons
- OmniPhysics: Core simulations, basic concept map, sample problems

### **Paid Tier (Personal Features)**
Unlocks tracking/journaling but NO additional knowledge gating:
- Unlimited personal data storage
- Advanced calculators (user-input based)
- Offline model downloads (where applicable)
- Export capabilities

### **Pro Tier (Convenience)**
Advanced features, NOT knowledge:
- Cloud backup
- Advanced analytics
- Priority support
- Additional export formats

**Critical**: Knowledge content NEVER moves from free → paid. New knowledge updates are added to free tier.

---

## Content Acquisition Pipeline

### **Phase 1: Source Identification**
```
Input: Knowledge gap (e.g., "hypertension management basics")
↓
Search: Government sources, OER, CC-licensed content
↓
Evaluate: Reliability, recency, license compatibility
↓
Select: Best source(s) for topic
↓
Output: Source record with metadata
```

### **Phase 2: Content Extraction**
```
Input: Source document (PDF, webpage, etc.)
↓
Extract: Text, structure, citations
↓
Clean: Remove formatting artifacts, normalize
↓
Validate: Accuracy check against source
↓
Output: Raw content + citation
```

### **Phase 3: Plain-Language Translation**
```
Input: Technical source content
↓
Analyze: Identify jargon, complex sentences
↓
Translate: Plain language (reading level 8-10)
↓
Preserve: Technical terms where necessary
↓
Validate: Accuracy maintained
↓
Output: Plain-language version WITH citation to original
```

**Example:**
- **Original (FDA label)**: "This medication is a selective serotonin reuptake inhibitor (SSRI) indicated for the treatment of major depressive disorder (MDD)."
- **Plain language**: "This medication is a type of antidepressant called an SSRI. It works by increasing serotonin in your brain. Doctors prescribe it for clinical depression.[^1]"
- **Citation**: [1] FDA. [Drug Name] Prescribing Information. [Date].

### **Phase 4: Enrichment**
```
Input: Plain-language content
↓
Add: Diagrams, charts, examples
↓
Create: Interactive elements (where applicable)
↓
Link: Related concepts, prerequisites
↓
Tag: Keywords, difficulty, categories
↓
Output: Enriched content record
```

### **Phase 5: Review & Validation**
```
Input: Enriched content
↓
SME Review: Subject matter expert validation
↓
Legal Review: License compliance check
↓
Accessibility: Screen reader, alt text, readability
↓
QA: Broken links, missing citations, formatting
↓
Approve: Ready for integration
↓
Output: Production-ready content
```

### **Phase 6: Integration**
```
Input: Approved content
↓
Database: Insert into content DB
↓
Index: Update search index
↓
Graph: Link to concept graph
↓
Assets: Bundle images/media
↓
Test: App integration smoke test
↓
Output: Deployed content (app update or download)
```

---

## Content Management System Requirements

### **Must-Have Features**

1. **Version Control**
   - Git-like versioning for all content
   - Rollback capability
   - Audit trail (who changed what, when)

2. **Workflow Management**
   - Draft → Review → Approved → Published
   - Role-based permissions (writer, reviewer, approver)
   - Automated checks (broken links, missing citations)

3. **Citation Tracking**
   - Source database
   - Citation validator
   - Update reminders (when sources need re-checking)
   - Broken link detector

4. **Search & Discovery**
   - Full-text search across all content
   - Filter by app, tier, type, difficulty
   - Related content suggestions
   - Gap analysis (what's missing)

5. **Quality Metrics**
   - Reading level scoring (Flesch-Kincaid)
   - Citation density
   - Review currency
   - User feedback integration

6. **Localization Ready**
   - Multi-language support (future)
   - Translation workflow
   - Cultural adaptation notes

### **Tech Stack Recommendation**

**Option A: Custom (Full Control)**
- PostgreSQL (content DB)
- Elasticsearch (search)
- Git (version control)
- Django/FastAPI (CMS backend)
- React (CMS frontend)

**Option B: Headless CMS (Faster)**
- Strapi (open source, self-hosted)
- Directus (open source, self-hosted)
- Sanity.io (hosted, generous free tier)
- Contentful (hosted, paid)

**Option C: Static Site Generator (Simplest)**
- Markdown files in Git
- Hugo/Jekyll for preview
- Custom build scripts for app integration
- Works for v1.0, doesn't scale well

**Recommendation**: Start with Option C (Markdown + Git), migrate to Option B (headless CMS) at scale.

---

## On-Device Storage Strategy

### **Embedded Database**
- SQLite for iOS/Mac
- Core Data (Apple's ORM) or direct SQLite
- Full-text search (FTS5)
- ~50MB knowledge base per app (compressed)

### **Asset Bundling**
- Images: WebP format (smaller than PNG/JPEG)
- Diagrams: SVG (scalable, small)
- Videos: HEVC (H.265) for size
- Bundle with app or optional download (Free tier = bundled)

### **Update Strategy**
- **App updates** (iOS paradigm):
  - Major content additions → app version bump
  - Users get updates via App Store

- **In-app downloads** (optional, advanced):
  - Pro users can download "knowledge packs"
  - E.g., "Advanced Calculus" for OmniMath
  - Still respects free tier (core 21 chapters remain)

### **Compression**
- Zstandard (zstd) for content compression
- ~60-70% size reduction on text
- Decompress on-device (fast, low battery impact)

---

## Content Update Workflow

### **Quarterly Update Cycle**

**Month 1: Source Review**
- Check all sources for updates
- Identify broken links
- Flag outdated content
- Discover new OER materials

**Month 2: Content Refresh**
- Update changed content
- Add new topics (priority: user requests)
- Remove deprecated information
- Expand thin areas

**Month 3: QA & Release**
- SME review of changes
- Legal license review
- App integration testing
- Bundle with next app update

### **Emergency Updates**
- Critical corrections (medical/legal errors)
- Security issues (e.g., vulnerable advice)
- Regulatory changes (law updates)
- → Expedited review → immediate app update

---

## Quality Control Checklist

Before ANY content goes live:

### **Accuracy**
- [ ] Every claim has a source citation
- [ ] Source is authoritative (govt, peer-reviewed, established OER)
- [ ] Source is current (within update frequency window)
- [ ] Plain-language version matches source meaning
- [ ] No medical/legal advice (only education/reference)

### **Legal**
- [ ] License permits commercial use
- [ ] Attribution provided (if required)
- [ ] No copyright infringement
- [ ] Derivative work compliance (CC licenses)
- [ ] Terms of use respected

### **Accessibility**
- [ ] Reading level 8-10 (or explicitly advanced)
- [ ] Alt text for all images
- [ ] Screen reader tested
- [ ] Color contrast meets WCAG AA
- [ ] Keyboard navigable

### **Technical**
- [ ] Links work (automated check)
- [ ] Images load and display correctly
- [ ] Search index updated
- [ ] Related concepts linked
- [ ] Database constraints validated

---

## App-Specific Content Priorities

### **Launch Blockers (Must have for v1.0)**

**OmniSalub**
- [ ] 20 common conditions (hypertension, diabetes, etc.)
- [ ] Vital sign reference ranges
- [ ] When-to-seek-care guidelines
- [ ] 50 FAQ

**OmniDent**
- [ ] Oral health encyclopedia (50 topics)
- [ ] Brushing/flossing technique guides
- [ ] Age-based care guides (infant → senior)
- [ ] When-to-see-dentist decision tree

**OmniDerm**
- [ ] Skin health basics (anatomy, sun safety)
- [ ] How to keep a skin journal
- [ ] ABCDE self-awareness (not diagnosis)
- [ ] When-to-see-dermatologist guide

**OmniRx**
- [ ] 100 drug classes explained
- [ ] How-to-take guides (timing, food, etc.)
- [ ] Medication safety basics
- [ ] Pharmacy communication guide

**OmniLex**
- [ ] USC structure explained
- [ ] How to read a law
- [ ] Court systems overview
- [ ] 50 common legal forms with instructions

**OmniBuild**
- [ ] Permit process by jurisdiction (top 50 cities)
- [ ] OSHA construction standards (plain language)
- [ ] ADA compliance guide
- [ ] When-you-need-a-licensed-professional guide

**OmniWealth**
- [ ] 100 financial concepts (A-Z)
- [ ] 20 basic calculators
- [ ] Retirement planning guide
- [ ] Investment basics (no recommendations)

**OmniMath**
- [ ] Chapters 1-5 complete (foundation)
- [ ] Concept codex (300 terms)
- [ ] 500 worked problems
- [ ] Interactive proof viewer

**OmniAero**
- [ ] Private Pilot ACS complete
- [ ] Part 61 & 91 plain-language
- [ ] Weather theory & METAR/TAF decoder
- [ ] Flight planning guide

**OmniPhysics**
- [ ] Mechanics simulations (10 core)
- [ ] E&M simulations (10 core)
- [ ] 200 concepts explained
- [ ] 300 worked problems

---

## Content Team Structure

### **Roles Needed**

**Content Strategist** (1)
- Identify knowledge gaps
- Prioritize topics
- Source selection
- Quality standards

**Content Writers** (3-5 per app)
- Plain-language translation
- Original explanatory content
- Diagram creation
- Citation management

**Subject Matter Experts** (as needed)
- Accuracy review
- Technical validation
- Consulted, not full-time

**Legal Reviewer** (1)
- License compliance
- Avoid advice language
- Risk mitigation

**Content Engineer** (1-2)
- CMS development
- Database design
- App integration
- Automation tools

### **In-House vs Outsource**

**Keep in-house:**
- Content strategy
- Legal review
- App integration
- Final approval

**Can outsource:**
- Plain-language writing (with review)
- Diagram creation
- Citation extraction
- Initial drafts

**Never outsource:**
- Medical/legal judgment calls
- What crosses the "hard line"
- License decisions

---

## Automation Opportunities

### **Content Extraction**
- OCR for PDF sources → markdown
- Web scraping for public domain content
- Citation extraction with NLP
- Auto-categorization with ML

### **Quality Checks**
- Broken link checker (scheduled)
- Reading level calculator
- Citation validator
- Plagiarism detection

### **Generation (Use with caution)**
- LLM-assisted plain-language translation
  - ⚠️ Always SME-reviewed
  - Never published without human validation
  - Useful for first drafts only

- Diagram generation from descriptions
- Example problem creation (math/physics)
- FAQ generation from common questions

### **User Feedback Loop**
- In-app "Report issue" button
- User-submitted questions (FAQ candidates)
- Content rating (helpful/not helpful)
- Analytics: Which content is most viewed

---

## Launch Readiness: Content Edition

An app is **content-ready for launch** when:

1. ✅ Free tier has 80%+ of core knowledge
2. ✅ Every piece of content has citations
3. ✅ All sources are properly licensed
4. ✅ Reading level targets met
5. ✅ Search and navigation functional
6. ✅ Related concepts linked
7. ✅ Accuracy validated by SME
8. ✅ Legal review passed
9. ✅ User testing completed
10. ✅ Update pathway established

**Current status: 0/10 apps are content-ready.**

This is the critical path to launch. The website is done; the knowledge layer needs to be built.

---

## Next Actions

1. **Pick one pilot app** (Recommendation: OmniMath or OmniPhysics - clear sources)
2. **Build content pipeline** (Markdown → DB → App)
3. **Create 10 pieces of content** end-to-end (validate workflow)
4. **User test** with beta testers (validate usefulness)
5. **Scale** to 100 pieces
6. **Launch** pilot app with Free tier
7. **Iterate** based on user feedback
8. **Expand** to remaining apps

**Estimated effort: 6-12 months for one app at quality standards.**

---

*Last updated: 2026-08-26*
*Focus: How to build the knowledge layer, not just what to include*
