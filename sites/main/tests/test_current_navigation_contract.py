#!/usr/bin/env python3
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "css" / "site-v9.css").read_text(encoding="utf-8")
JS = (ROOT / "js" / "site-v8.js").read_text(encoding="utf-8")


class CurrentNavigationContractTests(unittest.TestCase):
    def test_current_controls_keep_interaction_floor(self):
        for marker in (
            ".brand{display:inline-flex;align-items:center;gap:.62rem;min-height:48px",
            ".nav a,.nav button{display:inline-flex;align-items:center;justify-content:center;min-height:48px",
            ".theme-toggle,.nav-toggle{min-width:48px;min-height:48px",
            ".footer-links a{min-height:48px",
        ):
            self.assertIn(marker, CSS)

    def test_mobile_navigation_is_bounded_and_stateful(self):
        self.assertIn('.nav-actions .nav-toggle{display:inline-grid;place-items:center}', CSS)
        self.assertIn('.nav[data-open="true"]{display:flex}', CSS)
        self.assertIn('navButton.setAttribute("aria-label", open ? "Close navigation" : "Open navigation")', JS)
        self.assertIn('if (event.key === "Escape" && nav.dataset.open === "true")', JS)
        self.assertIn('navButton.focus()', JS)

    def test_accessibility_preferences_have_fallbacks(self):
        self.assertIn("@media (prefers-reduced-motion:reduce)", CSS)
        self.assertIn("@media (prefers-reduced-transparency:reduce)", CSS)
        self.assertIn("@media (forced-colors:active)", CSS)


if __name__ == "__main__":
    unittest.main()
