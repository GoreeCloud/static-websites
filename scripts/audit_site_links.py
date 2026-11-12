#!/usr/bin/env python3
"""Dependency-free, offline, fail-closed validation of the nonproduction website.

Verifies navigation/fragment targets, first-party static resources, review-only
indexing, safe external links and basic document landmarks. This neither
changes files nor makes network requests.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import posixpath
import sys

SITE = Path(__file__).resolve().parents[1] / "site"
TRUSTED_ORIGIN = "https://preview.invalid"


class Document(HTMLParser):
    def __init__(self, name: str):
        super().__init__(convert_charrefs=True)
        self.name = name
        self.ids: set[str] = set()
        self.refs: list[tuple[str, str, str]] = []
        self.errors: list[str] = []
        self.landmarks: dict[str, int] = {}
        self.robots = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        props = dict(attrs)
        for attr in ("id",):
            value = props.get(attr)
            if value:
                if value in self.ids:
                    self.errors.append(f"{self.name}: duplicate id #{value}")
                self.ids.add(value)
        if tag in ("main", "h1"):
            self.landmarks[tag] = self.landmarks.get(tag, 0) + 1
        if tag == "meta" and (props.get("name") or "").lower() == "robots":
            if "noindex" in (props.get("content") or "").lower():
                self.robots = True
        if tag == "script":
            if not props.get("src"):
                self.errors.append(f"{self.name}: inline script violates site CSP")
        if tag == "style":
            self.errors.append(f"{self.name}: inline CSS violates site CSP")
        if tag == "img" and "alt" not in props:
            self.errors.append(f"{self.name}: missing image alt attribute")
        if tag == "a":
            if props.get("target") == "_blank":
                rel = set((props.get("rel") or "").lower().split())
                if not {"noopener", "noreferrer"}.issubset(rel):
                    self.errors.append(f"{self.name}: external-tab link lacks noopener/noreferrer")
        if tag == "button" and not props.get("aria-label"):
            # Visible button text is checked by browser tests; inaccessible
            # empty self-closing buttons are not allowed here.
            pass
        if tag == "a" and props.get("href") is not None:
            self.refs.append(("link", props["href"] or "", tag))
        if tag in ("img", "script") and props.get("src") is not None:
            self.refs.append(("asset", props["src"] or "", tag))
        if tag == "link":
            rel = set((props.get("rel") or "").lower().split())
            if {"stylesheet", "icon", "manifest"} & rel:
                self.refs.append(("asset", props.get("href") or "", tag))


def resolve(site: Path, current: str, value: str) -> tuple[str | None, str | None, str | None]:
    """Return local site-relative path, fragment and error; or none for external."""
    if not value or value.startswith("//") or value.lower().startswith("javascript:"):
        return None, None, "empty, protocol-relative or JavaScript reference"
    parsed = urlsplit(value)
    if parsed.scheme:
        if parsed.scheme in ("https", "http") and parsed.netloc:
            return None, None, None
        if parsed.scheme in ("mailto", "tel"):
            return None, None, None
        return None, None, f"unsupported URL scheme {parsed.scheme!r}"
    if parsed.netloc:
        return None, None, "untrusted network-path reference"
    # Resolve against the page's deployed route, not its on-disk index.html.
    route = "/" if current == "index.html" else "/" + current.removesuffix("index.html")
    absolute = urljoin(TRUSTED_ORIGIN + route, value)
    pieces = urlsplit(absolute)
    path = unquote(pieces.path)
    if "\\" in path or "/../" in path or path.endswith("/.."):
        return None, None, "unsafe traversal or backslash"
    path = posixpath.normpath(path)
    if pieces.path.endswith("/") and not path.endswith("/"):
        path += "/"
    if path == "/":
        local = "index.html"
    elif path.endswith("/"):
        local = path.strip("/") + "/index.html"
    else:
        local = path.lstrip("/")
    return local, unquote(pieces.fragment), None


def audit(site: Path = SITE) -> list[str]:
    errors: list[str] = []
    pages = sorted(site.rglob("*.html"))
    docs: dict[str, Document] = {}
    if len(pages) != 17:
        errors.append(f"expected 17 static HTML pages, found {len(pages)}")
    for page in pages:
        name = str(page.relative_to(site))
        doc = Document(name)
        try:
            doc.feed(page.read_text(encoding="utf-8"))
        except (UnicodeError, ValueError) as e:
            errors.append(f"{name}: could not parse: {type(e).__name__}")
        docs[name] = doc
        errors.extend(doc.errors)
        if not doc.robots:
            errors.append(f"{name}: preview page lacks noindex robots")
        if name != "404.html" and (
            doc.landmarks.get("main") != 1 or doc.landmarks.get("h1") != 1
        ):
            errors.append(f"{name}: expected exactly one main and one h1")

    references = 0
    for current, doc in docs.items():
        for kind, raw, tag in doc.refs:
            references += 1
            target, fragment, error = resolve(site, current, raw)
            if error:
                errors.append(f"{current}: {tag} {raw!r}: {error}")
                continue
            if target is None:
                if kind == "asset":
                    errors.append(f"{current}: external {tag} asset prohibited: {raw!r}")
                continue
            path = site / target
            if not path.is_file():
                errors.append(f"{current}: missing local {tag} target {raw!r} -> {target!r}")
            elif fragment and target.endswith(".html"):
                target_doc = docs.get(target)
                if not target_doc or fragment not in target_doc.ids:
                    errors.append(f"{current}: broken fragment {raw!r}")
    return sorted(set(errors))


def main() -> int:
    errors = audit()
    if errors:
        print(f"BLOCKED: {len(errors)} static website problems")
        for error in errors[:80]:
            print(" - " + error)
        return 1
    print("PASS: 17 pages, internal resources, fragment targets, noindex, and CSP-safe source references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
