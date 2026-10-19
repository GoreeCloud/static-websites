#!/usr/bin/env python3
"""Fail-closed source and built-output checks; no production approval implied."""
from __future__ import annotations
from hashlib import sha1, sha256
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys

from build import SOURCE, OUT, ASSETS

RELEASE_SOURCE_COMMIT = "7e0b61ee70af2edb87aa736cca483425f0aacaf4"
FOUNDATIONS_GIT_BLOB = "c0e32a40f0bba280c9a4e9e01f31e1114d60f26c"
PUBLISHED_FOUNDATIONS_TARBALL_SHA256 = "275d7e6dc9503b2e74b3190bcecf176d73d2345860e8a20fa5faa3b326cd2298"
LEGACY_ACTIVE = re.compile(r"glaze|data-glz|--glz", re.I)


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids: set[str] = set()
        self.targets: list[str] = []
        self.styles: list[str] = []
        self.scripts: list[str] = []
        self.theme: list[tuple[str, str | None]] = []
        self.skip = False
        self.main = 0
        self.lang = 0
        self.indexing = False
        self.inline_code = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang += int(a.get("lang") == "en")
        if a.get("id"):
            if a["id"] in self.ids:
                raise ValueError("duplicate preview anchor")
            self.ids.add(a["id"])
        if tag == "main":
            self.main += 1
        if tag == "meta" and a.get("name") == "robots":
            self.indexing = "noindex" in a.get("content", "")
        if "style" in a:
            self.inline_code = True
        if tag == "style":
            self.inline_code = True
        if tag == "script":
            if not a.get("src"):
                self.inline_code = True
            self.scripts.append(a.get("src", ""))
        if tag == "link" and "stylesheet" in a.get("rel", "").split():
            self.styles.append(a.get("href", ""))
        if tag == "a":
            href = a.get("href", "")
            if href.startswith("#"):
                self.targets.append(href[1:])
                if "skip" in a.get("class", "").split() and href == "#main":
                    self.skip = True
        if tag == "button" and a.get("data-mode"):
            self.theme.append((a["data-mode"], a.get("aria-pressed")))


def validate(folder: Path, built: bool = False) -> dict[str, object]:
    if not folder.is_dir() or folder.is_symlink():
        raise ValueError("missing or symlinked preview source")
    files = {name: folder / name for name in ASSETS}
    data: dict[str, bytes] = {}
    for name, path in files.items():
        if not path.is_file() or path.is_symlink():
            raise ValueError("missing or unsafe preview asset: " + name)
        blob = path.read_bytes()
        if not blob or len(blob) > 1000000 or b"\x00" in blob:
            raise ValueError("invalid preview bytes: " + name)
        blob.decode("utf-8", "strict")
        data[name] = blob
    # The published scoped Foundations release includes this file unchanged
    # from the reviewed commit. This tests exact Git source identity, not
    # independently downloaded npm-format archive identity.
    css = data["gc-ui-foundations.css"]
    source_object = b"blob " + str(len(css)).encode("ascii") + bytes([0]) + css
    if sha1(source_object).hexdigest() != FOUNDATIONS_GIT_BLOB:
        raise ValueError("unsupported or edited Foundations source")
    for name in ("index.html", "site.css", "site.js"):
        content = data[name].decode()
        if LEGACY_ACTIVE.search(content):
            raise ValueError("active retired design import/identity in " + name)
        if name.endswith(".css") and "@import" in content:
            raise ValueError("unapproved CSS imports")
    if "@import" in css.decode():
        raise ValueError("Foundations CSS import not reviewed")

    page = Document()
    page.feed(data["index.html"].decode())
    if page.lang != 1 or page.main != 1 or not page.skip or not page.indexing:
        raise ValueError("missing semantic language, main, skip link or noindex")
    if page.inline_code or any(t not in page.ids for t in page.targets):
        raise ValueError("inline content or broken in-page anchor")
    if page.styles != ["./gc-ui-foundations.css", "./site.css"]:
        raise ValueError("only the reviewed local CSS files may load")
    if page.scripts != ["./site.js"]:
        raise ValueError("only the local preview JS may load")
    if sorted(page.theme) != sorted([
        ("system", "true"), ("light", "false"), ("dark", "false")
    ]):
        raise ValueError("appearance control does not expose accessible state")
    if not {"main", "foundation", "boundaries", "status"} <= page.ids:
        raise ValueError("missing required preview sections")

    authored_css = data["site.css"].decode()
    for role in ("--gc-v1-foundation-target-touch",
                 "--gc-v1-foundation-typography-family-ui",
                 "--gc-v1-component-focus-width",
                 "--gc-v1-color-primary", "prefers-reduced-motion",
                 "forced-colors", "focus-visible", "max-width:650px"):
        if role not in authored_css:
            raise ValueError("missing scoped design/accessibility role " + role)

    script = data["site.js"].decode()
    for token in ("localStorage", "try", "catch", "aria-pressed", "data-gc-mode",
                  "prefers-color-scheme", "data-mode"):
        if token not in script:
            raise ValueError("missing accessible appearance logic: " + token)
    if re.search(r"\b(fetch|XMLHttpRequest|sendBeacon|WebSocket|eval)\s*\(", script):
        raise ValueError("preview must not fetch external resources or evaluate code")

    if built:
        permitted = set(ASSETS) | {"SHA256SUMS.json"}
        present = set(p.name for p in folder.iterdir())
        if permitted != present:
            raise ValueError("unexpected build output")
        metadata = json.loads((folder / "SHA256SUMS.json").read_text("utf-8"))
        if metadata.get("schema") != "gc-ui-www-isolated-preview.v1":
            raise ValueError("wrong preview artifact schema")
        for key in ("deployed", "gcUiConsumerAccepted", "gcUiPlatformCutoverComplete"):
            if metadata.get(key) is not False:
                raise ValueError("preview cannot claim completed product gate: " + key)
        if metadata.get("files") != {name: sha256(blob).hexdigest() for name, blob in data.items()}:
            raise ValueError("preview file digest mismatch")

    return {
        "status": "isolated-source-valid-no-deployment",
        "gcUiPublishedSource": RELEASE_SOURCE_COMMIT,
        "foundationsGitBlob": FOUNDATIONS_GIT_BLOB,
        "filesVerified": len(ASSETS),
        "deployed": False, "productionDesignMigrated": False
    }


if __name__ == "__main__":
    try:
        dist = "--dist" in sys.argv
        print(json.dumps(validate(OUT if dist else SOURCE, built=dist), sort_keys=True))
    except (OSError, UnicodeError, ValueError, KeyError) as error:
        print("GC UI retained-web preview invalid: " + str(error), file=sys.stderr)
        sys.exit(1)
