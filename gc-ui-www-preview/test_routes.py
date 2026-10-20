"""Fail-closed tests for the undeployed 11-route GC UI candidate."""
from __future__ import annotations

from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json
import shutil
import tempfile
import unittest

from build_routes import OUT, PATHS, FILES, build


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.styles = []
        self.scripts = []
        self.current = 0
        self.mains = 0
        self.ids = set()
        self.noindex = False
        self.skip = False
        self.modes = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            if a["id"] in self.ids:
                raise ValueError("duplicate page id")
            self.ids.add(a["id"])
        if tag == "main":
            self.mains += 1
        if tag == "meta" and a.get("name") == "robots":
            self.noindex = "noindex" in a.get("content", "")
        if tag == "link" and "stylesheet" in a.get("rel", ""):
            self.styles.append(a.get("href"))
        if tag == "script":
            self.scripts.append(a.get("src"))
        if tag == "a":
            self.links.append(a)
            if a.get("aria-current") == "page":
                self.current += 1
            if a.get("href") == "#main":
                self.skip = True
        if tag == "button" and a.get("data-mode"):
            self.modes[a["data-mode"]] = a.get("aria-pressed")


def verify(folder: Path):
    evidence = json.loads((folder / "SHA256SUMS.json").read_text())
    if evidence["schema"] != "gc-ui-www-routes-isolated-candidate.v1":
        raise ValueError("unexpected candidate schema")
    if any(evidence.get(k) is not False for k in
           ("publicSiteChanged", "deployed", "productionAccepted", "contentParityAccepted", "a11yBrowserAccepted")):
        raise ValueError("unearned acceptance or deployment claim")
    if evidence["routes"] != list(PATHS.values()):
        raise ValueError("unapproved candidate URL route set")
    files = {}
    for path in folder.rglob("*"):
        if path.is_symlink():
            raise ValueError("symlink in artifact")
        if path.is_file() and path.name != "SHA256SUMS.json":
            files[path.relative_to(folder).as_posix()] = sha256(path.read_bytes()).hexdigest()
    if files != evidence["files"]:
        raise ValueError("artifact missing, changed or contains unexpected files")
    source = json.loads((folder / "SHA256SUMS.json").read_text()).get("sourceSha256")
    expected = {entry["source"]: sha256((OUT.parent / entry["source"]).read_bytes()).hexdigest()
                for entry in __import__("build_routes")._namespace()}
    if source != expected:
        raise ValueError("source provenance digest mismatch")
    for ident, route in PATHS.items():
        file = folder / ("index.html" if route == "/" else ident + "/index.html")
        value = file.read_text(encoding="utf-8")
        if "glaze" in value.lower() or "<style" in value or "<script>" in value:
            raise ValueError("unsafe predecessor or inline content")
        content_cards = value.count("candidate-content-card")
        if content_cards < (40 if ident == "suite" else 9 if ident == "platform-systems" else 3):
            raise ValueError("unreviewed source-content coverage " + route)
        page = Page()
        page.feed(value)
        prefix = "assets/" if route == "/" else "../assets/"
        if (page.mains != 1 or not page.skip or not page.noindex or page.current != 1
                or page.styles != [prefix + "gc-ui-foundations.css", prefix + "site.css", prefix + "routes.css"]
                or page.scripts != [prefix + "site.js"]
                or page.modes != {"system": "true", "light": "false", "dark": "false"}
                or not {"main", "overview", "source"} <= page.ids):
            raise ValueError("broken route semantics or source boundary " + route)
        internal = {a.get("href") for a in page.links if (a.get("href") or "").startswith("/")
                    and not a.get("href", "").startswith("//")}
        if not set(PATHS.values()) <= internal:
            raise ValueError("incomplete preserved navigation " + route)
    if set(files) != {"assets/" + x for x in FILES} | {
            "index.html", *(k + "/index.html" for k in PATHS if k != "home")}:
        raise ValueError("output allowlist mismatch")
    return len(PATHS)


class GCUIRouteCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build()

    def test_all_retained_routes_have_safe_preview(self):
        self.assertEqual(verify(OUT), 11)

    def test_tampered_route_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "artifact"
            shutil.copytree(OUT, copy)
            (copy / "privacy" / "index.html").write_text("<html>tampered</html>")
            with self.assertRaisesRegex(ValueError, "artifact missing, changed"):
                verify(copy)

    def test_unapproved_extra_asset_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "artifact"
            shutil.copytree(OUT, copy)
            (copy / "retired.html").write_text("Not an approved route")
            with self.assertRaisesRegex(ValueError, "artifact missing, changed"):
                verify(copy)


if __name__ == "__main__":
    unittest.main()
