#!/usr/bin/env python3
"""Contract tests for the Prameya company site.

The built HTML in the repo root is what GitHub Pages serves. These tests
read that HTML plus src/apps.json so a status or copy drift fails locally
before it is published.
"""

from __future__ import annotations

import json
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
    "omnimath",
    "omniaero",
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
    def test_catalog_lists_exactly_the_ten_public_apps(self) -> None:
        data = load_apps()
        slugs = [app["slug"] for app in data["apps"]]
        self.assertEqual(slugs, EXPECTED_SLUGS)
        self.assertTrue(all(app["status"] == "in_development" for app in data["apps"]))
        self.assertTrue(all(not app.get("store_url") for app in data["apps"]))
        self.assertNotIn("omniops", slugs)

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
            self.assertIn("In development", text, msg=app["slug"])
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

    def test_privacy_model_links_the_existing_hub_and_names_model_downloads(self) -> None:
        text = (ROOT / "privacy-model" / "index.html").read_text(encoding="utf-8")
        self.assertIn("https://prameyallc.github.io/privacy/", text)
        self.assertIn("OmniLex", text)
        self.assertIn("OmniDent", text)
        self.assertIn("OmniSalub", text)
        self.assertIn("Hugging Face", text)

    def test_no_omniops_product_page(self) -> None:
        self.assertFalse((ROOT / "apps" / "omniops").exists())

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
