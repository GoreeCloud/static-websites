"""Offline regressions for the preview-only internal-link and asset checker."""
from __future__ import annotations
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_site_links import SITE, audit  # noqa: E402


class SiteAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="goreecloud-audit-")
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name) / "site"
        shutil.copytree(SITE, self.site)

    def mutate_home(self, addition: str):
        target = self.site / "index.html"
        value = target.read_text(encoding="utf-8")
        self.assertIn("</main>", value)
        target.write_text(value.replace("</main>", addition + "</main>", 1), encoding="utf-8")

    def test_unmodified_site_passes(self):
        self.assertEqual(audit(self.site), [])

    def test_missing_static_image_fails(self):
        self.mutate_home('<img src="/assets/nonexistent-asset.png" alt="fake">')
        self.assertTrue(any("missing local img target" in x for x in audit(self.site)))

    def test_broken_fragment_fails(self):
        self.mutate_home('<a href="/ecosystem/#no-such-section">Broken fragment</a>')
        self.assertTrue(any("broken fragment" in x for x in audit(self.site)))

    def test_duplicate_id_fails(self):
        self.mutate_home('<span id="main">Duplicate</span>')
        self.assertTrue(any("duplicate id" in x for x in audit(self.site)))

    def test_external_script_fails(self):
        self.mutate_home('<script src="https://external.invalid/track.js"></script>')
        self.assertTrue(any("external script asset prohibited" in x for x in audit(self.site)))

    def test_inline_script_fails(self):
        self.mutate_home('<script>alert("not-allowed")</script>')
        self.assertTrue(any("inline script violates site CSP" in x for x in audit(self.site)))

    def test_unsafe_javascript_link_fails(self):
        self.mutate_home('<a href="javascript:alert(1)">Unsafe</a>')
        self.assertTrue(any("JavaScript reference" in x for x in audit(self.site)))

    def test_external_new_tab_without_rel_fails(self):
        self.mutate_home('<a href="https://example.com/" target="_blank">Missing rel</a>')
        self.assertTrue(any("lacks noopener/noreferrer" in x for x in audit(self.site)))

    def test_missing_preview_noindex_fails(self):
        target = self.site / "privacy/index.html"
        source = target.read_text(encoding="utf-8")
        self.assertIn('name="robots"', source)
        target.write_text(source.replace('name="robots"', 'name="not-robots"', 1))
        self.assertTrue(any("lacks noindex" in x for x in audit(self.site)))


if __name__ == "__main__":
    unittest.main()
