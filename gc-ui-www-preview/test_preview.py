"""Source-only negative tests for the undeployed GC UI /design/ preview."""
from __future__ import annotations
from pathlib import Path
import shutil
import tempfile
import unittest

from build import ASSETS, SOURCE
from validate import validate


class GCUIRetainedWebsitePreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name)
        for name in ASSETS:
            shutil.copyfile(SOURCE / name, self.path / name)

    def tearDown(self):
        self.temp.cleanup()

    def test_original_source_is_valid_but_not_a_migration(self):
        result = validate(self.path)
        self.assertFalse(result["deployed"])
        self.assertFalse(result["productionDesignMigrated"])

    def test_unknown_legacy_import_is_rejected(self):
        path = self.path / "index.html"
        path.write_text(path.read_text() + '<script src="./glaze-runtime.js"></script>')
        with self.assertRaisesRegex(ValueError, "retired design"):
            validate(self.path)

    def test_broken_navigation_fails(self):
        path = self.path / "index.html"
        path.write_text(path.read_text().replace('href="#foundation"', 'href="#unknown-anchor"'))
        with self.assertRaisesRegex(ValueError, "broken in-page anchor"):
            validate(self.path)

    def test_unreviewed_foundations_bytes_fails(self):
        path = self.path / "gc-ui-foundations.css"
        path.write_text(path.read_text() + "\n/* added without source review */\n")
        with self.assertRaisesRegex(ValueError, "edited Foundations"):
            validate(self.path)

    def test_external_runtime_source_fails(self):
        path = self.path / "index.html"
        path.write_text(path.read_text().replace('./site.js', 'https://example.invalid/site.js'))
        with self.assertRaisesRegex(ValueError, "local preview JS"):
            validate(self.path)

    def test_aria_state_must_be_truthful(self):
        path = self.path / "index.html"
        path.write_text(path.read_text().replace('data-mode="system" aria-pressed="true"',
                                                'data-mode="system" aria-pressed="false"'))
        with self.assertRaisesRegex(ValueError, "accessible state"):
            validate(self.path)

    def test_source_symlinks_are_rejected(self):
        path = self.path / "site.css"
        path.unlink()
        path.symlink_to(SOURCE / "site.css")
        with self.assertRaisesRegex(ValueError, "unsafe preview asset"):
            validate(self.path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
