#!/usr/bin/env python3
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CurrentDocumentationContractTests(unittest.TestCase):
    def test_version_and_glaze_lock_are_current(self):
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "5.25.1")
        lock = json.loads((ROOT / "glaze.lock.json").read_text(encoding="utf-8"))
        self.assertEqual(lock["version"], "1.7.0")
        self.assertEqual(lock["lifecycle"], "Stable")
        self.assertEqual(lock["repository"], "GoreeCloud/glaze")
        self.assertEqual(lock["stable_commit"], "1a5756daed2294155be2e9972b24f580f6222b7b")
        self.assertEqual(lock["consumer_state"], "source-adopted-unaccepted")

    def test_stability_baseline_preserves_exact_acceptance_boundary(self):
        text = (ROOT / "docs" / "stability-baseline.md").read_text(encoding="utf-8")
        for marker in (
            "eleven",
            "Glaze V1.7 / 1.7.0 Stable",
            "17303b6c7381faaa0e89ce6175ce24048fb56a12",
            "human visual review",
            "keyboard-only review",
            "assistive-technology review",
            "explicit GoreeCloud project-owner acceptance",
        ):
            self.assertIn(marker, text)

    def test_foundation_contract_uses_current_paths_and_identity(self):
        text = (ROOT / "docs" / "homepage-foundations-integration.md").read_text(encoding="utf-8")
        self.assertIn("**Glaze**", text)
        self.assertIn("https://www.goreecloud.com/design/", text)
        self.assertIn("https://www.goreecloud.com/privacy/", text)
        self.assertIn("https://www.goreecloud.com/security/", text)
        self.assertNotIn("https://design.goreecloud.com/", text)
        self.assertNotIn("https://privacy.goreecloud.com/", text)
        self.assertNotIn("https://security.goreecloud.com/", text)


if __name__ == "__main__":
    unittest.main()
