#!/usr/bin/env python3
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
NAMESPACE = json.loads((REPO_ROOT / "sites" / "url-namespace.json").read_text(encoding="utf-8"))
EXPECTED_PATHS = [
    "/", "/platform-systems/", "/suite/", "/android/", "/office-suite/", "/firefox/",
    "/github/", "/contact/", "/donations/", "/design/", "/security/", "/privacy/",
]


class CurrentSiteContractTests(unittest.TestCase):
    def test_namespace_is_one_retained_site_with_twelve_routes(self):
        self.assertEqual(NAMESPACE["repository"], "GoreeCloud/static-websites")
        self.assertEqual(NAMESPACE["state"], "single-retained-website")
        self.assertEqual(NAMESPACE["canonical_origin"], "https://www.goreecloud.com")
        self.assertEqual([entry["path"] for entry in NAMESPACE["canonical_paths"]], EXPECTED_PATHS)

    def test_every_canonical_page_is_glaze_v17_and_accessible_by_structure(self):
        for entry in NAMESPACE["canonical_paths"]:
            source = REPO_ROOT / entry["source"]
            text = source.read_text(encoding="utf-8")
            with self.subTest(path=entry["path"]):
                self.assertIn('data-glaze-version="1.7.0"', text)
                self.assertIn('data-glaze-consumer-state="source-adopted-unaccepted"', text)
                self.assertIn('<a class="skip-link" href="#main">Skip to content</a>', text)
                self.assertIn('id="primary-navigation"', text)
                self.assertIn('data-nav-toggle', text)
                self.assertIn('aria-controls="primary-navigation"', text)
                self.assertIn('aria-label="Open navigation"', text)
                self.assertIn('data-theme-toggle', text)
                self.assertEqual(text.count("<h1"), 1)

    def test_current_pages_do_not_recreate_retired_satellite_topology(self):
        retired = (
            "https://suite.goreecloud.com/",
            "https://design.goreecloud.com/",
            "https://privacy.goreecloud.com/",
            "https://security.goreecloud.com/",
            "https://projects.goreecloud.com/",
        )
        for entry in NAMESPACE["canonical_paths"]:
            text = (REPO_ROOT / entry["source"]).read_text(encoding="utf-8")
            for marker in retired:
                with self.subTest(path=entry["path"], marker=marker):
                    self.assertNotIn(marker, text)

    def test_homepage_links_current_path_based_authority_surfaces(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        for href in ("/design/", "/security/", "/privacy/", "/contact/", "/donations/"):
            self.assertIn(f'href="{href}"', home)

    def test_compatibility_routes_are_bounded(self):
        redirects = {entry["from"]: entry["to"] for entry in NAMESPACE["compatibility_paths"]}
        self.assertEqual(redirects["/repositories.html"], "/github/")
        self.assertEqual(redirects["/privacy.html"], "/privacy/")
        self.assertEqual(redirects["/security.html"], "/security/")
        self.assertEqual(redirects["/firefox-extensions"], "/firefox/")


if __name__ == "__main__":
    unittest.main()
