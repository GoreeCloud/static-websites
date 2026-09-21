#!/usr/bin/env python3
"""Validate links, canonical metadata, sitemap, and current public surface."""

from __future__ import annotations

from collections import Counter
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "index.html",
    "platform-systems/index.html",
    "suite/index.html",
    "office-suite/index.html",
    "firefox/index.html",
    "github/index.html",
    "stable/index.html",
    "contact/index.html",
    "privacy.html",
    "security.html",
    "repositories.html",
    "404.html",
)
CANONICAL = {
    "index.html": "https://www.goreecloud.com/",
    "platform-systems/index.html": "https://www.goreecloud.com/platform-systems/",
    "suite/index.html": "https://www.goreecloud.com/suite/",
    "office-suite/index.html": "https://www.goreecloud.com/office-suite/",
    "firefox/index.html": "https://www.goreecloud.com/firefox/",
    "github/index.html": "https://www.goreecloud.com/github/",
    "stable/index.html": "https://www.goreecloud.com/stable/",
    "contact/index.html": "https://www.goreecloud.com/contact/",
}


class Audit(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: Counter[str] = Counter()
        self.refs: list[str] = []
        self.canonical: str | None = None
        self.robots = ""

    def handle_starttag(self, tag, attrs_list):
        attrs = {k: v or "" for k, v in attrs_list}
        if attrs.get("id"):
            self.ids[attrs["id"]] += 1
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonical = attrs.get("href")
        if tag == "meta" and attrs.get("name", "").lower() == "robots":
            self.robots = attrs.get("content", "")
        for key in ("href", "src"):
            if attrs.get(key):
                self.refs.append(attrs[key])


def source_target(source_relative: str, raw_ref: str) -> tuple[Path, str]:
    parsed = urlparse(raw_ref)
    fragment = unquote(parsed.fragment)
    raw_path = unquote(parsed.path)
    if raw_path in ("", "."):
        return ROOT / source_relative, fragment
    if raw_path == "/":
        return ROOT / "index.html", fragment

    if raw_path.startswith("/"):
        candidate = ROOT / raw_path.lstrip("/")
    else:
        candidate = ROOT / Path(source_relative).parent / raw_path

    if raw_path.endswith("/"):
        candidate = candidate / "index.html"
    candidate = candidate.resolve()
    candidate.relative_to(ROOT.resolve())
    return candidate, fragment


def main() -> int:
    errors: list[str] = []
    audits: dict[Path, Audit] = {}

    for relative in PAGES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing public page: {relative}")
            continue
        audit = Audit()
        audit.feed(path.read_text(encoding="utf-8"))
        audits[path.resolve()] = audit

        expected = CANONICAL.get(relative)
        if expected and audit.canonical != expected:
            errors.append(f"{relative} canonical mismatch: {audit.canonical!r}")
        if expected and "noindex" in audit.robots.lower():
            errors.append(f"{relative} is canonical but noindex")
        if relative in {"privacy.html", "security.html", "repositories.html", "404.html"} and "noindex" not in audit.robots.lower():
            errors.append(f"{relative} must be noindex")

    for source_path, audit in audits.items():
        source_relative = str(source_path.relative_to(ROOT.resolve()))
        for ref in audit.refs:
            parsed = urlparse(ref)
            if parsed.scheme or parsed.netloc or ref.startswith("//"):
                continue
            if ref.startswith("#"):
                if parsed.fragment and unquote(parsed.fragment) not in audit.ids:
                    errors.append(f"{source_relative} references missing fragment: {ref}")
                continue
            try:
                target, fragment = source_target(source_relative, ref)
            except ValueError:
                errors.append(f"{source_relative} reference escapes site root: {ref}")
                continue
            if not target.exists():
                errors.append(f"{source_relative} references missing local target: {ref}")
                continue
            if fragment and target.suffix == ".html":
                target_audit = audits.get(target.resolve())
                if target_audit is None:
                    target_audit = Audit()
                    target_audit.feed(target.read_text(encoding="utf-8"))
                    audits[target.resolve()] = target_audit
                if fragment not in target_audit.ids:
                    errors.append(f"{source_relative} references missing fragment in {target.relative_to(ROOT)}: #{fragment}")

    sitemap = ROOT / "sitemap.xml"
    expected_urls = set(CANONICAL.values())
    if not sitemap.is_file():
        errors.append("sitemap.xml missing")
    else:
        try:
            root = ElementTree.fromstring(sitemap.read_text(encoding="utf-8"))
            ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
            urls: set[str] = set()
            for entry in root.findall(f"{ns}url"):
                loc = entry.find(f"{ns}loc")
                lastmod = entry.find(f"{ns}lastmod")
                if loc is None or not (loc.text or "").strip():
                    errors.append("sitemap contains an empty URL")
                    continue
                url = (loc.text or "").strip()
                urls.add(url)
                if lastmod is None:
                    errors.append(f"sitemap entry missing lastmod: {url}")
                else:
                    try:
                        if date.fromisoformat((lastmod.text or "").strip()) > date.today():
                            errors.append(f"sitemap entry has future lastmod: {url}")
                    except ValueError:
                        errors.append(f"sitemap entry has invalid lastmod: {url}")
            if urls != expected_urls:
                errors.append(f"sitemap must contain exactly the eight canonical pages; found {sorted(urls)}")
        except ElementTree.ParseError as exc:
            errors.append(f"invalid sitemap XML: {exc}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap: https://www.goreecloud.com/sitemap.xml" not in robots:
        errors.append("robots.txt missing canonical sitemap URL")

    if errors:
        print("Public surface validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Public surface validation passed: eight canonical pages and compatibility routes are internally coherent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
