#!/usr/bin/env python3
"""Contract tests for the Prameya company site.

The built HTML in the repo root is what GitHub Pages serves. These tests
read that HTML plus src/apps.json so a status or copy drift fails locally
before it is published.
"""

from __future__ import annotations

import json
import html
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
APPS_JSON = ROOT / "src" / "apps.json"
BASE_HOST = "prameyallc.github.io"

EXPECTED_SLUGS = [
    "omnisalub",
    "omnident",
    "omniderm",
    "omnirx",
    "omnilex",
    "omnibuild",
    "omniwealth",
    "omniops",
    "omnimath",
    "omniavia",
    "omniphysics",
]

EXPECTED_PAGES = [
    ROOT / "index.html",
    ROOT / "apps" / "index.html",
    ROOT / "standard" / "index.html",
    ROOT / "about" / "index.html",
    ROOT / "privacy-model" / "index.html",
    ROOT / "contact" / "index.html",
    ROOT / "resources" / "index.html",
    ROOT / "resources" / "brand" / "index.html",
    ROOT / "resources" / "faq" / "index.html",
    ROOT / "resources" / "one-pagers" / "company" / "index.html",
    ROOT / "resources" / "one-pagers" / "portfolio" / "index.html",
]

ALLOWED_EXTERNAL_HOSTS = {
    "github.com",
    "www.github.com",
    "x.com",
    "twitter.com",
    "prameyallc.github.io",
    "schema.org",
    "www.schema.org",
}

FORBIDDEN_PHRASES = [
    "download now",
    "notify me when",
    "saves you",
    "improves your",
    "faster approval",
]

# Capability claims that must not appear as positive verbs.
FORBIDDEN_ROLE_CLAIMS = [
    r"\bdiagnoses\b",
    r"\badvises\b",
    r"\brepresents you\b",
]


STORE_NAMES = {
    "omnisalub": "OmniSalub",
    "omnident": "OmniDent",
    "omniderm": "OmniDerm",
    "omnirx": "OmniRx",
    "omnilex": "OmniLex",
    "omnibuild": "OmniBuild",
    "omniwealth": "OmniWealth",
    "omniops": "OmniCadence",
    "omnimath": "OmniMathematics",
    "omniavia": "OmniAvia",
    "omniphysics": "OmniPhysics",
}


HUB_MODEL_SENTENCE = ("Some apps can download an optional AI model file from Hugging Face, and only after you choose to; "
                      "each app's own policy says whether it does and when.")


class HrefCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == "a" and attr.get("href"):
            self.hrefs.append(attr["href"])
        if tag == "link" and attr.get("href"):
            self.hrefs.append(attr["href"])
        if tag == "script" and attr.get("src"):
            self.hrefs.append(attr["src"])
        if tag == "img" and attr.get("src"):
            self.hrefs.append(attr["src"])


def load_apps() -> dict:
    return json.loads(APPS_JSON.read_text(encoding="utf-8"))


def html_files() -> list[Path]:
    skip = {".git", "src", "tests", ".grok", "assets"}
    found = []
    for path in ROOT.rglob("*.html"):
        if any(part in skip for part in path.relative_to(ROOT).parts):
            continue
        found.append(path)
    return found


class CatalogTests(unittest.TestCase):
    def test_catalog_lists_exactly_the_eleven_public_apps(self) -> None:
        data = load_apps()
        slugs = [app["slug"] for app in data["apps"]]
        self.assertEqual(slugs, EXPECTED_SLUGS)
        statuses = {app["slug"]: app["status"] for app in data["apps"]}
        # Every iOS 1.0 has been submitted to App Review: OmniMathematics (September 2026), OmniAvia (26 September
        # 2026), and the other nine read WAITING_FOR_REVIEW on `asc versions list` (27 September 2026).
        # Nothing is on sale yet.
        self.assertTrue(all(status == "in_review" for status in statuses.values()), statuses)
        self.assertTrue(all(not app.get("store_url") for app in data["apps"]))
        self.assertIn("omniops", slugs)

    def test_display_names_are_the_app_store_names_and_slugs_stay(self) -> None:
        """OmniOps became OmniCadence (2026-09-06/07) and OmniMath is OmniMathematics on the store.
        The slugs, and the privacy URLs built on them, stay so existing links keep working."""
        data = {app["slug"]: app for app in load_apps()["apps"]}
        for slug, name in STORE_NAMES.items():
            self.assertEqual(data[slug]["name"], name, msg=slug)
            self.assertEqual(data[slug]["legal_name"], name, msg=slug)
            self.assertEqual(data[slug]["privacy_url"], f"https://prameyallc.github.io/privacy/{slug}/", msg=slug)

    def test_pricing_is_free_plus_pro_not_full_app(self) -> None:
        data = load_apps()
        for app in data["apps"]:
            pricing = app["pricing"]
            self.assertNotIn("paid_app", pricing, msg=app["slug"])
            pro = pricing["pro_subscription"]
            self.assertIn("price_monthly_usd", pro, msg=app["slug"])
            self.assertIn("price_yearly_usd", pro, msg=app["slug"])
            self.assertIn("price_lifetime_usd", pro, msg=app["slug"])
            self.assertTrue(pricing["free_tier"]["includes"], msg=app["slug"])

    def test_every_app_has_a_hard_line_and_privacy_url(self) -> None:
        data = load_apps()
        for app in data["apps"]:
            self.assertTrue(app["hard_line"].strip(), msg=app["slug"])
            self.assertTrue(app["summary"].strip(), msg=app["slug"])
            self.assertTrue(app["privacy_url"].startswith("https://prameyallc.github.io/privacy/"))
            icon = ROOT / "assets" / "icons" / app["icon"]
            self.assertTrue(icon.is_file(), msg=app["icon"])


class BuiltSiteTests(unittest.TestCase):
    def test_required_pages_exist(self) -> None:
        missing = [str(p.relative_to(ROOT)) for p in EXPECTED_PAGES if not p.is_file()]
        for slug in EXPECTED_SLUGS:
            path = ROOT / "apps" / slug / "index.html"
            if not path.is_file():
                missing.append(str(path.relative_to(ROOT)))
        self.assertEqual(missing, [])

    def test_this_repo_does_not_publish_a_privacy_directory(self) -> None:
        self.assertFalse((ROOT / "privacy").exists())

    def test_app_pages_restate_the_hard_line_and_status(self) -> None:
        data = load_apps()
        for app in data["apps"]:
            text = (ROOT / "apps" / app["slug"] / "index.html").read_text(encoding="utf-8")
            self.assertIn(app["hard_line"], text, msg=app["slug"])
            badge = re.search(r'<header class="page-hero">.*?<span class="status[^"]*">([^<]+)</span>', text, re.S)
            self.assertIsNotNone(badge, msg=app["slug"])
            expected = {"in_review": "Submitted to App Review", "available": "On the App Store"}.get(app["status"], "In development")
            self.assertNotIn(">In App Review<", text, msg=f"{app['slug']}: the site cannot see Apple's review state")
            self.assertEqual(badge.group(1), expected, msg=app["slug"])
            if app["status"] == "in_development":
                self.assertIn("Planned pricing; it can change before release.", text, msg=app["slug"])
            else:
                self.assertNotIn("Planned pricing", text, msg=app["slug"])
                self.assertNotIn("Screenshots will appear here", text, msg=app["slug"])
            self.assertIn(app["privacy_url"], text, msg=app["slug"])
            self.assertIn("Write to us about", text, msg=app["slug"])
            self.assertIn("mailto:admin@prameya.legal", text, msg=app["slug"])
            self.assertNotIn("Download now", text)
            if app.get("health_data_url"):
                self.assertIn(app["health_data_url"], text, msg=app["slug"])

    def test_home_keeps_the_hero_and_four_rules(self) -> None:
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("Expert knowledge,", text)
        self.assertIn("for everyone", text)
        self.assertIn("Runs on your device", text)
        self.assertIn("Every claim has a source", text)
        self.assertIn("The knowledge layer is free", text)
        self.assertIn("It won't pretend to be your professional", text)
        self.assertIn("better client, not a substitute", text)

    def test_contact_does_not_operate_a_mailing_list(self) -> None:
        text = (ROOT / "contact" / "index.html").read_text(encoding="utf-8")
        self.assertIn("admin@prameya.legal", text)
        self.assertIn("do not add you to a mailing list", text.lower())
        self.assertIn("Do not send photographs of your skin", text)

    def test_privacy_model_links_the_existing_hub_and_quotes_its_model_download_sentence(self) -> None:
        """The hub stopped naming apps (2026-09-15): the list was unverified. Quote the hub; name no app in that sentence."""
        text = (ROOT / "privacy-model" / "index.html").read_text(encoding="utf-8")
        self.assertIn("https://prameyallc.github.io/privacy/", text)
        self.assertIn("Hugging Face", text)
        self.assertIn(HUB_MODEL_SENTENCE, html.unescape(text))
        self.assertNotIn("do not download weights in the shipping build", text)
        quote = re.search(r"<blockquote>(.*?)</blockquote>", text, re.S)
        self.assertIsNotNone(quote)
        self.assertNotRegex(quote.group(1), r"Omni[A-Z]", msg="the quoted hub paragraph must not list apps")
        for stale in ("OmniLex, OmniDent and OmniSalub", "OmniMathematics when you choose to download its optional Ask model"):
            self.assertNotIn(stale, text, msg=stale)

    def test_omniops_has_a_product_page(self) -> None:
        """OmniCadence keeps the /apps/omniops/ URL it had as OmniOps."""
        path = ROOT / "apps" / "omniops" / "index.html"
        self.assertTrue(path.is_file())
        self.assertIn("<h1>OmniCadence</h1>", path.read_text(encoding="utf-8"))

    def test_built_html_uses_the_app_store_names(self) -> None:
        """No page shows the old names. File names in src attributes (assets/icons/OmniOps.png) are not shown."""
        for path in html_files():
            text = re.sub(r'\ssrc="[^"]*"', "", path.read_text(encoding="utf-8"))
            self.assertNotRegex(text, r"\bOmniOps\b", msg=str(path))
            self.assertNotRegex(text, r"\bOmniMath\b", msg=str(path))

    def test_built_html_does_not_sell_full_app_or_cloud_backup(self) -> None:
        for path in html_files():
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("Full App", text, msg=str(path))
            self.assertNotIn("Cloud backup", text, msg=str(path))
            self.assertNotIn("First 5 chapters", text, msg=str(path))

    def test_omnident_does_not_make_a_blanket_no_diagnose_claim(self) -> None:
        """Privacy policy 24 Aug 2026 withdrew blanket 'does not diagnose' for OmniDent."""
        text = (ROOT / "apps" / "omnident" / "index.html").read_text(encoding="utf-8").lower()
        self.assertNotIn("does not diagnose", text)
        self.assertIn("no fda authorization", text)
        self.assertIn("ask a dentist", text)

    def test_built_html_has_no_forbidden_marketing_phrases(self) -> None:
        for path in html_files():
            text = path.read_text(encoding="utf-8").lower()
            for phrase in FORBIDDEN_PHRASES:
                self.assertNotIn(phrase, text, msg=f"{path}: {phrase}")
            for pattern in FORBIDDEN_ROLE_CLAIMS:
                for match in re.finditer(pattern, text):
                    start = max(0, match.start() - 40)
                    window = text[start:match.end() + 10]
                    self.assertRegex(
                        window,
                        r"does not|don't|do not|never|won't|will not|none of",
                        msg=f"{path}: role claim not negated: {window!r}",
                    )

    def test_external_urls_stay_inside_the_allowlist(self) -> None:
        for path in html_files():
            parser = HrefCollector()
            parser.feed(path.read_text(encoding="utf-8"))
            for href in parser.hrefs:
                if href.startswith(("mailto:", "#", "/")):
                    continue
                if not href.startswith("http"):
                    continue
                host = urlparse(href).hostname or ""
                if host.endswith("apple.com"):
                    continue
                self.assertIn(host, ALLOWED_EXTERNAL_HOSTS, msg=f"{path}: {href}")

    def test_pages_have_unique_titles_and_canonicals(self) -> None:
        titles = []
        canonicals = []
        for path in html_files():
            text = path.read_text(encoding="utf-8")
            title = re.search(r"<title>([^<]+)</title>", text)
            canon = re.search(r'rel="canonical" href="([^"]+)"', text)
            self.assertIsNotNone(title, msg=path)
            self.assertIsNotNone(canon, msg=path)
            titles.append(title.group(1))
            canonicals.append(canon.group(1))
            self.assertIn(BASE_HOST, canon.group(1))
            self.assertIn('name="description"', text)
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(canonicals), len(set(canonicals)))

    def test_omnimath_page_says_only_what_the_submitted_app_does(self) -> None:
        """OmniMathematics 1.0 (24): 20 chapters in 6 parts, not a course, Pro is the study report only."""
        text = (ROOT / "apps" / "omnimath" / "index.html").read_text(encoding="utf-8")
        lower = text.lower()
        for stale in ("21 chapters", "twenty-one", "is a course", "extra drills", "lab interactives",
                      "export of your work", "screenshots will appear here", "in development.",
                      '"creativeworkstatus": "incomplete"',
                      # build 24 (2026-09-15): the Ask model is a per-device catalog and the Codex is Concepts
                      "350 mb", "qwen", "codex"):
            self.assertNotIn(stale, lower, msg=stale)
        for fact in ("20 chapters in 6 parts", "All 20 story-tour chapters", "Export my marks, as a raw file",
                     "Hugging Face", "MiniCPM5 2B", "openbmb/MiniCPM5-2B-MLX", "about 1.4 GB",
                     "Gemma 4 E2B", "mlx-community/gemma-4-E2B-it-qat-4bit", "about 4.4 GB",
                     "8 GB", "12 GB or more", "6 GB or less", "On-device Ask model", "Concepts",
                     "7-day free trial for eligible new subscribers",
                     "OmniMathematics is not a course, a credential or a tutor"):
            self.assertIn(fact, html.unescape(text), msg=fact)
        pro = re.search(r'<div class="tier featured">.*?<ul class="tier-features">(.*?)</ul>', text, re.S)
        self.assertIsNotNone(pro)
        self.assertEqual(re.findall(r"<li>([^<]+)</li>", pro.group(1)), ["A formatted study report of your marks"])

    def test_omniavia_page_says_only_what_the_submitted_app_does(self) -> None:
        """OmniAvia 1.0: ground study and reference. Never a go/no-go, and not "In development" once submitted."""
        text = html.unescape((ROOT / "apps" / "omniavia" / "index.html").read_text(encoding="utf-8"))
        for stale in ("Go / no-go reasoning", "go/no-go reasoning", "Planned pricing", "Screenshots will appear here",
                      "In development."):
            self.assertNotIn(stale, text, msg=stale)
        # The badge is this app's; the related-app cards further down carry their own.
        hero = re.search(r'<header class="page-hero">.*?</header>', text, re.S)
        self.assertIsNotNone(hero)
        self.assertIn('<span class="status">Submitted to App Review</span>', hero.group(0))
        self.assertNotIn("In development", hero.group(0))
        for fact in ("A source under every item", "iPhone", "Apple Watch",
                     "it never makes a go/no-go, airworthiness or fitness-to-fly decision",
                     "Formatted study PDF"):
            self.assertIn(fact, text, msg=fact)
        chips = [item for block in re.findall(r'<ul class="chips">(.*?)</ul>', text, re.S)
                 for item in re.findall(r"<li>([^<]+)</li>", block)]
        self.assertIn("A source under every item", chips)
        self.assertFalse([c for c in chips if "no-go" in c.lower()], chips)

    def test_pro_lists_sell_only_what_the_submitted_builds_sell(self) -> None:
        """2026-09-27 audit against each app's paywall and Pro gates. These lines named things the
        submitted builds do not sell (no checklists, no pharmacist PDF, no reminder tier, no
        refill-date field, a vault that is uncapped on Free, a PDF disclaimer the export dropped)."""
        withdrawn = {
            "omnibuild": ["Inspection checklist packs", "Unlimited projects"],
            "omnirx": ["Reminder depth", "Pharmacist conversation PDF", "Refill date", "refill dates"],
            "omnilex": ["Unlimited vault", "disclaimer on every page"],
            "omniderm": ["compare overlay"],
        }
        for slug, stale in withdrawn.items():
            text = html.unescape((ROOT / "apps" / slug / "index.html").read_text(encoding="utf-8"))
            for line in stale:
                self.assertNotIn(line, text, msg=f"{slug}: {line}")
        pro = {app["slug"]: app["pricing"]["pro_subscription"]["includes"] for app in load_apps()["apps"]}
        self.assertEqual(pro["omnirx"], ["Multi-medication schedule"])
        self.assertEqual(pro["omnilex"], ["Search what you imported", "Formatted PDF report, generated on your device"])
        self.assertEqual(pro["omnibuild"], ["More than two projects", "Permit-counter PDF"])

    def test_every_app_claim_matches_what_main_ships(self) -> None:
        """2026-09-27 audit of chips, summary, detail, hard line, meta description and free list against
        each app's main and published policy. These lines named things main does not do: an imaging
        journal with no UI, a Mac build not submitted, a hygienist endorsement the app withdrew (D-05),
        consumer consultation framing the OmniLex listing bans, a project-mapping OmniBuild does not
        do, a Physics concept map that does not exist, Math Ask text from before D-1/D-2, and
        "never"/"does not" lines that the apps' own content contradicts."""
        withdrawn = {
            "omnisalub": ["Imaging history", "The record a clinic keeps about you", "the history you already know",
                          "Raw export of your record<"],
            "omnident": ["hygienist"],
            "omniderm": ["does not tell you whether to see a clinician", "It never tells you what a mark is",
                         "OmniDerm never tells you what a mark is", "The app records what you noticed"],
            "omnirx": ["a class of medicine"],
            "omnilex": ["consultation", "preparation for a conversation with a lawyer", "every passage cited"],
            "omnibuild": ["maps what applies to your project", "a map of procedure", "Where a licence is required",
                          "OmniBuild maps permits", "Federal and state public standards"],
            "omniwealth": ["numbers you type"],
            "omniops": ["without buying a consultant"],
            "omnimath": ["can rephrase an answer", "Ask answers from Concepts and the topic packs",
                         "The button names the model", "is a discrete-math learning app"],
            "omniavia": ["The regulation itself is always one tap away", "14 CFR one tap away"],
            "omniphysics": ["Concept map", "concept map", "step by step"],
        }
        for slug, stale in withdrawn.items():
            text = html.unescape((ROOT / "apps" / slug / "index.html").read_text(encoding="utf-8"))
            # This app's own copy, meta description included; the related-app cards below carry other apps'.
            own, sep, _ = text.partition('<div class="kicker">Also in')
            self.assertTrue(sep, msg=slug)
            for line in stale:
                self.assertNotIn(line, own, msg=f"{slug}: {line}")
        # Chips and list items are matched whole, so a reworded item cannot hide a withdrawn one.
        data = {app["slug"]: app for app in load_apps()["apps"]}
        self.assertNotIn("Mac", data["omnisalub"]["platforms"], "OmniSalub's Mac 1.0 has not been submitted")
        self.assertNotIn("Imaging history", data["omnisalub"]["features"])
        self.assertNotIn("Concept map", data["omniphysics"]["features"])
        self.assertNotIn("Concept map", data["omniphysics"]["pricing"]["free_tier"]["includes"])
        self.assertNotIn("Permits & utilities", data["omnibuild"]["features"])
        self.assertNotIn("14 CFR in plain language", data["omniavia"]["features"])
        self.assertNotIn("14 CFR in plain language", data["omniavia"]["pricing"]["free_tier"]["includes"])
        self.assertNotIn("Daily check", data["omnirx"]["pricing"]["free_tier"]["includes"],
                         "Free stops saving after 30 logs for one medicine")
        # Site-wide pages that speak for an app.
        privacy = html.unescape((ROOT / "privacy-model" / "index.html").read_text(encoding="utf-8"))
        self.assertNotIn("does not download a model", privacy, "OmniRx's policy discloses an optional model download")
        self.assertNotIn("the app never tells you what a mark is", privacy)
        self.assertIn("sync preferences or records through your own iCloud account", privacy)
        standard = (ROOT / "standard" / "index.html").read_text(encoding="utf-8")
        self.assertNotRegex(standard, r"sync preferences\s+through your own iCloud")
        pricing = html.unescape((ROOT / "pricing" / "index.html").read_text(encoding="utf-8"))
        for stale in ("read and raw-export everything you entered", "can be read and raw-exported even if Pro lapses",
                      "Raw export of what you recorded"):
            self.assertNotIn(stale, pricing, msg=stale)
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertRegex(home, r"optional model-file downloads in some apps, sync\s+through your own iCloud account in some")

    def test_account_claim_is_true_and_omnident_sign_in_is_named(self) -> None:
        """OmniDent offers an optional Sign in with Apple (Keychain only, no server; its policy section 5),
        so "No account" as a blanket is false. No app requires one; name the exception on /privacy-model/."""
        for path in html_files():
            text = path.read_text(encoding="utf-8")
            for stale in ("No account, no server", "No accounts. No servers."):
                self.assertNotIn(stale, text, msg=f"{path}: {stale}")
        for page in ("index.html", "standard/index.html", "privacy-model/index.html"):
            text = (ROOT / page).read_text(encoding="utf-8")
            self.assertIn("No app requires an account.", text, msg=page)
            self.assertIn("OmniDent", text, msg=page)
            self.assertIn("optional Sign in with Apple", text, msg=page)
        privacy = html.unescape((ROOT / "privacy-model" / "index.html").read_text(encoding="utf-8"))
        for fact in ("no feature needs it, and it does not change what syncs", "in the Keychain on that device",
                     "None of it is sent to Prameya", "Delete Account & All Data"):
            self.assertIn(fact, privacy, msg=fact)

    def test_planning_documents_say_they_do_not_describe_the_shipped_apps(self) -> None:
        """These August 2026 plans are publicly fetchable and name withdrawn features and old app names."""
        for name in ("KNOWLEDGE_SOURCES.md", "CONTENT_ARCHITECTURE.md", "LAUNCH_CHECKLIST.md"):
            head = (ROOT / name).read_text(encoding="utf-8")[:600]
            self.assertTrue(head.startswith("> **Historical planning document, August 2026.**"), msg=name)
            self.assertIn("does not\n> describe the shipped apps", head, msg=name)
            self.assertIn("https://prameyallc.github.io/apps/", head, msg=name)
            self.assertIn("https://prameyallc.github.io/privacy/", head, msg=name)

    def test_site_wide_availability_copy_is_true_for_every_app(self) -> None:
        sentence = "All eleven apps have been submitted to App Review."
        for path in html_files():
            text = path.read_text(encoding="utf-8")
            for stale in ("in active development", "All eleven apps are", "not yet available on the App Store",
                          "No App Store links yet", "currently in development", "All ten are", "Ten apps",
                          "all in development", "All in development"):
                self.assertNotIn(stale, text, msg=f"{path}: {stale}")
            self.assertIn("links to the App Store once that app is available there", text, msg=str(path))
        for page in ("index.html", "pricing/index.html", "about/index.html", "resources/faq/index.html",
                     "resources/one-pagers/company/index.html", "resources/one-pagers/portfolio/index.html"):
            self.assertIn(sentence, (ROOT / page).read_text(encoding="utf-8"), msg=page)
        faq = html.unescape((ROOT / "resources" / "faq" / "index.html").read_text(encoding="utf-8"))
        self.assertIn(HUB_MODEL_SENTENCE, faq)
        self.assertNotIn("OmniLex, OmniDent and OmniSalub can download", faq)

    def test_pricing_page_is_true_of_omnimathematics_and_marks_planned_prices(self) -> None:
        text = (ROOT / "pricing" / "index.html").read_text(encoding="utf-8")
        for stale in ("Domain tools (visit pack, drills, sandbox, cadence)", "Formatted PDF / CSV export",
                      "Unlimited history and project depth", "Your own logs, photos, and documents",
                      "one-time app purchase"):
            self.assertNotIn(stale, text, msg=stale)
        self.assertIn("OmniMathematics: one feature, the formatted study report of your marks", text)
        self.assertIn("7-day free trial for eligible new subscribers", text)
        # The planned-price caveat is computed: it shows only while some app has not been submitted.
        if any(app["status"] == "in_development" for app in load_apps()["apps"]):
            self.assertIn("planned and can change before it is submitted", text)
        else:
            self.assertNotIn("planned and can change", text)
        self.assertIn("OmniAvia and OmniCadence: <strong>$5.99 / $39.99 / $99.99</strong>", text)

    def test_no_page_tells_a_subscriber_to_cancel_in_the_apps_own_settings(self) -> None:
        """"Cancel in Settings." reads as the app's Settings tab, which cannot cancel; the binary names the iOS path."""
        for path in html_files():
            text = html.unescape(path.read_text(encoding="utf-8"))
            self.assertNotIn("Cancel in Settings.", text, msg=str(path))
        omnimath = html.unescape((ROOT / "apps" / "omnimath" / "index.html").read_text(encoding="utf-8"))
        self.assertIn("Cancel in iOS Settings ▸ your name ▸ Subscriptions at least 24 hours before the period ends.", omnimath)
        self.assertIn("Study offline", omnimath)
        self.assertNotIn("Works offline", omnimath)

    def test_nojekyll_is_present(self) -> None:
        self.assertTrue((ROOT / ".nojekyll").is_file())

    def test_shared_stylesheet_and_no_third_party_stylesheets(self) -> None:
        css = ROOT / "assets" / "css" / "site.css"
        self.assertTrue(css.is_file())
        for path in html_files():
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(
                text,
                r"fonts\.googleapis|googletagmanager|google-analytics|cdn\.jsdelivr|unpkg\.com",
            )
            self.assertIn("assets/css/site.css", text)


if __name__ == "__main__":
    unittest.main()
