"""Dependency-free source acceptance checks for the single-page GoreeCloud site."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.images = []
        self.h1_count = 0
        self.has_lang = False
        self.scripts = 0

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "html":
            self.has_lang = attrs.get("lang") == "en"
        if tag == "a":
            self.links.append(attrs)
        if tag == "img":
            self.images.append(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag == "script":
            self.scripts += 1


class HomepageAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "assets/site.css").read_text(encoding="utf-8")
        cls.markup = Markup()
        cls.markup.feed(cls.html)

    def test_only_one_public_content_page(self):
        self.assertEqual({p.name for p in ROOT.glob("*.html")}, {"index.html", "404.html"})
        self.assertIn('name="robots" content="noindex"', (ROOT / "404.html").read_text())
        self.assertIn("GoreeCloud", self.html)
        self.assertNotIn('data-glaze-version=', self.html)

    def test_semantics_and_single_heading(self):
        self.assertTrue(self.markup.has_lang)
        self.assertEqual(self.markup.h1_count, 1)
        self.assertEqual(self.markup.scripts, 0)
        self.assertEqual(len(self.markup.ids), len(set(self.markup.ids)))
        self.assertIn('href="#content"', self.html)

    def test_all_navigation_targets(self):
        self.assertGreaterEqual(len(self.markup.links), 7)
        for anchor in self.markup.links:
            dest = anchor.get("href", "")
            if dest.startswith("#"):
                self.assertIn(dest[1:], self.markup.ids, dest)
            else:
                self.assertEqual(dest, "https://github.com/GoreeCloud")
                self.assertEqual(anchor.get("target"), "_blank")
                rel = set(anchor.get("rel", "").split())
                self.assertTrue({"noopener", "noreferrer"} <= rel)

    def test_all_assets_local_and_safe(self):
        for img in self.markup.images:
            self.assertIn("alt", img)
            source = img["src"]
            self.assertTrue(source.startswith("/assets/"))
            self.assertTrue((ROOT / source.lstrip("/")).is_file(), source)
        self.assertNotIn("@import", self.css)
        self.assertNotIn("url(", self.css)
        self.assertNotIn("https://", self.css)
        self.assertNotIn("http://", self.css)
        for svg in (ROOT / "assets").glob("*.svg"):
            markup = svg.read_text(encoding="utf-8")
            self.assertTrue(ET.fromstring(markup).tag.endswith("svg"))
            markup = markup.replace("http://www.w3.org/2000/svg", "").lower()
            for dangerous in ("<script", "<foreignobject", "javascript:", "https://", "http://",
                              " onload=", " onerror=", "<animate", "<set"):
                self.assertNotIn(dangerous, markup, svg.name)

    def test_single_url_sitemap(self):
        urls = ET.parse(ROOT / "sitemap.xml").findall(".//{*}loc")
        self.assertEqual([url.text for url in urls], ["https://www.goreecloud.com/"])
        robots = (ROOT / "robots.txt").read_text()
        self.assertIn("Sitemap: https://www.goreecloud.com/sitemap.xml", robots)

    def test_hardened_static_headers(self):
        headers = (ROOT / "_headers").read_text()
        for rule in ("default-src 'self'", "script-src 'none'", "object-src 'none'",
                     "frame-ancestors 'none'", "connect-src 'none'",
                     "X-Content-Type-Options: nosniff", "Referrer-Policy: no-referrer"):
            self.assertIn(rule, headers)
        self.assertNotIn("'unsafe-inline'", headers)

    def test_pillar_boundaries_and_no_fake_release_claim(self):
        for label in ("GoreeShield", "Wardveil", "GoreeCloud Mesh", "GoreeCloud UI",
                      "GoreeCloud Identity", "Public source does not imply"):
            self.assertIn(label, self.html)

    def test_mobile_glow_cannot_force_rightward_scroll(self):
        section = re.search(r"\.ambient-b\s*\{([^}]+)\}", self.css)
        self.assertIsNotNone(section)
        self.assertRegex(section.group(1), r"\bright:\s*0\s*;")
        self.assertNotRegex(section.group(1), r"right:\s*-")
        self.assertIn(".orbit-one { width: 80%; }", self.css)
        self.assertIn("prefers-reduced-motion", self.css)
        self.assertIn("forced-colors", self.css)
        self.assertIn(".footer-links a { display: inline-flex; align-items: center; min-height: 44px; }", self.css)
        self.assertIn("@media (max-width: 360px)", self.css)


    def test_container_delivery_is_scoped_and_hardened(self):
        dockerfile = (ROOT / "Dockerfile").read_text()
        compose = (ROOT / "compose.yaml").read_text()
        nginx = (ROOT / "docker/site.conf").read_text()
        self.assertIn("nginx-unprivileged@sha256:", dockerfile)
        self.assertIn("USER 101:101", dockerfile)
        self.assertIn("COPY assets/", dockerfile)
        self.assertNotIn("COPY . ", dockerfile)
        for text in ("127.0.0.1:18080:8080", "user: \"101:101\"", "read_only: true",
                     "cap_drop:", "no-new-privileges:true", "tmpfs:"):
            self.assertIn(text, compose)
        self.assertIn("try_files $uri =404;", nginx)
        self.assertIn("error_page 404 /404.html;", nginx)
        self.assertIn("script-src 'none'", nginx)
        # HTTP loopback must not instruct browsers to upgrade CSS/image requests to HTTPS.
        self.assertNotIn("upgrade-insecure-requests", nginx)


if __name__ == "__main__":
    unittest.main()
