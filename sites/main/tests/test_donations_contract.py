#!/usr/bin/env python3
"""Donation page safety and route regression tests for the retained static site."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
PAGE = ROOT / "donations" / "index.html"
CANONICAL = "https://www.goreecloud.com/donations/"


class PageLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs = []
        self.forms = []
        self.inputs = []
        self.frames = []
        self.scripts = []
        self.links = []
        self.headings = []
        self.images_without_alt = []

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        if tag == "a":
            self.links.append(props)
        if tag == "form":
            self.forms.append(props)
        if tag in ("input", "textarea", "select"):
            self.inputs.append((tag, props))
        if tag in ("iframe", "object", "embed"):
            self.frames.append((tag, props))
        if tag == "script":
            self.scripts.append(props)
        if tag.startswith("h") and len(tag) == 2 and tag[1].isdigit():
            self.headings.append(tag)
        if tag == "img" and "alt" not in props:
            self.images_without_alt.append(props.get("src"))
        for key in ("href", "src"):
            if props.get(key):
                self.refs.append(props[key])


class DonationsContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.parser = PageLinks()
        cls.parser.feed(cls.html)

    def test_canonical_route_sitemap_and_build_are_synced(self):
        registry = json.loads((REPOSITORY / "sites/url-namespace.json").read_text(encoding="utf-8"))
        entries = [item for item in registry["canonical_paths"] if item["id"] == "donations"]
        self.assertEqual(entries, [{
            "id": "donations",
            "path": "/donations/",
            "source": "sites/main/donations/index.html",
        }])
        self.assertIn(CANONICAL, (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        self.assertIn('"donations/index.html"', (ROOT / "scripts/build_public_site.py").read_text(encoding="utf-8"))
        self.assertIn('"/donations/"', (ROOT / "scripts/browser_artifact_smoke.py").read_text(encoding="utf-8"))

    def test_payment_is_explicitly_unavailable(self):
        self.assertIn("Financial donations are not yet enabled.", self.html)
        self.assertIn("No payment method is currently connected", self.html)
        self.assertIn("GoreeCloud is not accepting financial donations", self.html)
        self.assertEqual(self.parser.forms, [])
        self.assertEqual(self.parser.inputs, [])
        self.assertEqual(self.parser.frames, [])
        self.assertNotRegex(self.html, r"(?i)tax[- ]deductible|registered charity|501[(]c[)]")

    def test_only_approved_link_schemes_and_public_destinations(self):
        allowed_external = {CANONICAL, "https://github.com/GoreeCloud"}
        allowed_mailto = "mailto:support@goreecloud.com"
        for address in self.parser.refs:
            parsed = urlparse(address)
            if not parsed.scheme:
                self.assertTrue(
                    address.startswith("/") or address.startswith("#"),
                    f"noncanonical local reference: {address}",
                )
            elif parsed.scheme == "mailto":
                self.assertTrue(address.startswith(allowed_mailto))
            elif parsed.scheme == "https":
                self.assertIn(address, allowed_external)
            else:
                self.fail(f"unapproved URL scheme: {address}")
        self.assertFalse(any(
            marker in self.html.lower()
            for marker in ("stripe.com/", "paypal.com/", "paypal.me/", "ko-fi.com/", "opencollective.com/", "github.com/sponsors/", "crypto:")
        ))

    def test_csp_friendly_accessible_shell(self):
        self.assertEqual(self.parser.headings.count("h1"), 1)
        self.assertEqual(self.parser.images_without_alt, [])
        self.assertEqual(self.parser.scripts, [
            {"src": "/js/theme-init-v8.js"},
            {"src": "/js/site-v8.js", "defer": None},
        ])
        self.assertNotRegex(self.html, r"(?i)\son(?:click|load|error)\s*=")
        for expected in (
            'data-glaze-version="1.7.0"',
            'data-glaze-consumer-state="source-adopted-unaccepted"',
            'rel="canonical" href="' + CANONICAL + '"',
            'class="skip-link" href="#main"',
            'id="main"',
            'id="primary-navigation"',
            'data-nav-toggle',
            'data-theme-toggle',
        ):
            self.assertIn(expected, self.html)

    def test_footer_discovery_and_homepage_cta(self):
        registry = json.loads((REPOSITORY / "sites/url-namespace.json").read_text(encoding="utf-8"))
        for route in registry["canonical_paths"]:
            source = REPOSITORY / route["source"]
            with self.subTest(route=route["path"]):
                self.assertIn('href="/donations/"', source.read_text(encoding="utf-8"))
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("Explore ways to support", homepage)


if __name__ == "__main__":
    unittest.main()
