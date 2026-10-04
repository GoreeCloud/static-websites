#!/usr/bin/env python3
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_public_site import PUBLIC_FILES  # noqa: E402

TEMPLATE = ROOT / "docs" / "release-evidence-template.md"


class ReleaseEvidenceTemplateTests(unittest.TestCase):
    def setUp(self):
        self.text = TEMPLATE.read_text(encoding="utf-8")
        self.lower = self.text.lower()

    def test_template_is_repository_only_and_candidate_bound(self):
        self.assertTrue(TEMPLATE.is_file())
        self.assertNotIn("docs/release-evidence-template.md", PUBLIC_FILES)
        for marker in (
            "one exact GoreeCloud Website release candidate",
            "Exact candidate commit (40-character SHA)",
            "Evidence from one candidate must not be silently reused",
            "Central Time (`America/Chicago`)",
            "12-hour time format",
            "must remain outside the website `dist/` artifact",
            "does not itself authorize a merge",
            "Historical evidence must remain distinguishable from current state",
        ):
            self.assertIn(marker.lower(), self.lower)

    def test_template_covers_current_release_domains(self):
        for section in (
            "## 1. Candidate identity",
            "## 2. Automated validation evidence",
            "## 3. Human visual and interaction acceptance",
            "## 4. Accessibility acceptance",
            "## 5. Progressive enhancement, resilience, privacy, and origin boundary",
            "## 6. Publication and creative-rights boundary",
            "## 7. Isolated artifact and deployment boundary",
            "## 8. Glaze consumer evidence",
            "## 9. Release authorization",
            "## 10. Post-release production verification",
            "## 11. Final reconciliation",
        ):
            self.assertIn(section, self.text)
        self.assertIn("eleven canonical routes", self.lower)
        self.assertIn("glaze v1.7", self.lower)

    def test_template_starts_fail_closed(self):
        self.assertNotIn("[x]", self.lower)
        for disposition in ("ACCEPTED", "BLOCKED", "REJECTED", "SUPERSEDED"):
            self.assertIn(f"- [ ] {disposition}", self.text)
        self.assertIn("Select exactly one final candidate disposition", self.text)

    def test_template_prohibits_sensitive_evidence_material(self):
        for marker in (
            "Do not place credentials",
            "private keys",
            "private IP addresses",
            "private hostnames",
            "Do not paste raw logs",
            "appropriate protected system",
        ):
            self.assertIn(marker.lower(), self.lower)

    def test_integrity_evidence_is_scoped(self):
        self.assertIn("checksum", self.lower)
        self.assertIn("git blob id", self.lower)
        self.assertIn("evidence for the specific property it validates", self.lower)
        self.assertIn("not proof of unrelated security", self.lower)


if __name__ == "__main__":
    unittest.main()
