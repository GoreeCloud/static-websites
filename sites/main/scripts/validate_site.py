#!/usr/bin/env python3
"""Validate current public truth and semantic requirements for GoreeCloud Main."""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
import ipaddress
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = {
    "index.html": "https://www.goreecloud.com/",
    "platform-systems/index.html": "https://www.goreecloud.com/platform-systems/",
    "suite/index.html": "https://www.goreecloud.com/suite/",
    "office-suite/index.html": "https://www.goreecloud.com/office-suite/",
    "firefox/index.html": "https://www.goreecloud.com/firefox/",
    "github/index.html": "https://www.goreecloud.com/github/",
}
COMPATIBILITY = ("privacy.html", "security.html", "repositories.html")
STALE_MARKERS = (
    "Seven systems. Seven distinct responsibilities.",
    "seven Integral Platform Systems",
    "Fourteen official surfaces",
    "14 official public website",
    "GLAZE UI V1.3",
    "GLAZE UI V1.4 / 1.4",
    "Current Official Stable · 1.4",
    "suite.goreecloud.com",
    "firefox.goreecloud.com",
    "projects.goreecloud.com",
    "design.goreecloud.com",
    "privacy.goreecloud.com",
    "security.goreecloud.com",
    "roadmap.goreecloud.com",
    "blog.goreecloud.com",
    "archive.goreecloud.com",
    "This replaces the older multi-website model.",
    "This rebuild targets the current Official Stable Glaze UI contract.",
    "Migration candidate — acceptance pending",
)
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
CGNAT = ipaddress.ip_network("100.64.0.0/10")


def contains_private_address(text: str) -> bool:
    for token in IP_RE.findall(text):
        try:
            address = ipaddress.ip_address(token)
        except ValueError:
            continue
        if address.is_private or address in CGNAT:
            return True
    return False


class Audit(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: Counter[str] = Counter()
        self.h1 = 0
        self.canonical: str | None = None
        self.robots = ""
        self.inline_scripts = 0
        self.inline_styles = 0
        self.missing_alt: list[str] = []
        self.classes: Counter[str] = Counter()

    def handle_starttag(self, tag, attrs_list):
        attrs = {k: v or "" for k, v in attrs_list}
        identifier = attrs.get("id")
        if identifier:
            self.ids[identifier] += 1
        if tag == "h1":
            self.h1 += 1
        for cls in attrs.get("class", "").split():
            self.classes[cls] += 1
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonical = attrs.get("href")
        if tag == "meta" and attrs.get("name", "").lower() == "robots":
            self.robots = attrs.get("content", "")
        if tag == "script" and not attrs.get("src"):
            self.inline_scripts += 1
        if tag == "style":
            self.inline_styles += 1
        if tag == "img" and "alt" not in attrs:
            self.missing_alt.append(attrs.get("src", ""))


def audit_page(relative: str, expected_canonical: str | None, errors: list[str]) -> tuple[str, Audit] | None:
    path = ROOT / relative
    if not path.is_file():
        errors.append(f"missing public page: {relative}")
        return None
    text = path.read_text(encoding="utf-8")
    audit = Audit()
    audit.feed(text)

    if audit.h1 != 1:
        errors.append(f"{relative} must contain exactly one h1; found {audit.h1}")
    if audit.inline_scripts or audit.inline_styles:
        errors.append(f"{relative} contains inline script/style blocked by the site CSP")
    if audit.missing_alt:
        errors.append(f"{relative} has image(s) without alt attributes")
    for identifier, count in audit.ids.items():
        if count > 1:
            errors.append(f"{relative} contains duplicate id: {identifier}")
    if expected_canonical and audit.canonical != expected_canonical:
        errors.append(f"{relative} canonical mismatch: {audit.canonical!r}")
    if expected_canonical and "noindex" in audit.robots.lower():
        errors.append(f"{relative} is canonical but marked noindex")
    for stale in STALE_MARKERS:
        if stale in text:
            errors.append(f"{relative} contains stale current-state text: {stale}")
    if contains_private_address(text):
        errors.append(f"{relative} exposes private-range address material")
    for marker in (
        'data-glaze-version="1.6.0"',
        'name="goreecloud-glaze-ui" content="1.6.0"',
        'name="goreecloud-glaze-consumer-state" content="migration-candidate-unaccepted"',
    ):
        if marker not in text:
            errors.append(f"{relative} missing current Glaze migration marker: {marker}")
    if expected_canonical:
        for marker in (
            'id="primary-navigation"',
            'aria-controls="primary-navigation"',
            'aria-expanded="false"',
            'class="skip-link" href="#main"',
            'id="main"',
        ):
            if marker not in text:
                errors.append(f"{relative} missing required navigation/accessibility marker: {marker}")
    return text, audit


def main() -> int:
    errors: list[str] = []
    audited: dict[str, tuple[str, Audit]] = {}
    for relative, canonical in CANONICAL.items():
        result = audit_page(relative, canonical, errors)
        if result:
            audited[relative] = result

    for relative in COMPATIBILITY:
        result = audit_page(relative, None, errors)
        if result:
            _, audit = result
            if "noindex" not in audit.robots.lower():
                errors.append(f"{relative} must be noindex compatibility content")
            audited[relative] = result

    result = audit_page("404.html", None, errors)
    if result:
        _, audit = result
        if "noindex" not in audit.robots.lower():
            errors.append("404.html must be noindex")
        if audit.canonical:
            errors.append("404.html must not publish a canonical URL")

    home = audited.get("index.html", ("", Audit()))[0]
    for marker in (
        "One public website",
        "45 verified product surfaces",
        "Nine cross-cutting authorities",
        "Current Stable design system: V1.6.0",
        "/platform-systems/",
        "/suite/",
        "/office-suite/",
        "/firefox/",
        "/github/",
    ):
        if marker not in home:
            errors.append(f"homepage missing current-state marker: {marker}")

    platform = audited.get("platform-systems/index.html", ("", Audit()))
    if platform[1].classes["system-card"] != 9:
        errors.append(f"platform-systems must contain nine system cards; found {platform[1].classes['system-card']}")
    for name in (
        "GoreeCloud Manager", "Privacy Shield", "Wardveil Security", "Everkeep", "Glaze UI",
        "GoreeCloud Mesh", "GoreeCloud Identity", "GoreeCloud Policy", "GoreeCloud Observability",
    ):
        if name not in platform[0]:
            errors.append(f"platform-systems missing: {name}")
    if "not a tenth Integral Platform System" not in platform[0]:
        errors.append("platform-systems must preserve GoreeCloud Sync's separate-governance boundary")

    suite = audited.get("suite/index.html", ("", Audit()))
    if suite[1].classes["product-group"] != 9:
        errors.append(f"suite must contain nine product groups; found {suite[1].classes['product-group']}")
    if suite[1].classes["product"] != 45:
        errors.append(f"suite must contain 45 current products; found {suite[1].classes['product']}")

    office = audited.get("office-suite/index.html", ("", Audit()))[0]
    for marker in ("not yet implemented", "Rust", "Writer", ".gcwriter", ".gcsheet", ".gcpresent", "ODF 1.4", "not backup"):
        if marker not in office:
            errors.append(f"office-suite missing implementation/planning boundary marker: {marker}")

    firefox = audited.get("firefox/index.html", ("", Audit()))
    if firefox[1].classes["extension-card"] != 7:
        errors.append(f"firefox page must contain seven verified extension/client cards; found {firefox[1].classes['extension-card']}")
    for marker in (
        "Advanced Tab Manager", "Webspaces", "Privacy Shield", "Redirector",
        "Source Resync", "Download Manager Extension", "Bookmarks Firefox Client",
    ):
        if marker not in firefox[0]:
            errors.append(f"firefox page missing current source: {marker}")

    github = audited.get("github/index.html", ("", Audit()))[0]
    for marker in (
        "Load current public repositories",
        "does not publish private repository names",
        "Fresh metadata without publishing private inventory.",
        "Ready when you are",
        'role="status"',
        'aria-live="polite"',
        'aria-controls="github-repository-list"',
        'id="github-repository-list"',
    ):
        if marker not in github:
            errors.append(f"github page missing privacy/currentness marker: {marker}")
    if re.search(r"\b\d+\s+(?:total|public)\s+repositories\b", github, re.IGNORECASE):
        errors.append("github page must not hard-code a repository total")

    github_js = (ROOT / "js/site-v8.js").read_text(encoding="utf-8")
    if "https://api.github.com/orgs/GoreeCloud/repos" not in github_js:
        errors.append("GitHub catalog must use the public GoreeCloud organization API")
    if "data-load-github" not in github or "addEventListener(\"click\"" not in github_js:
        errors.append("GitHub public catalog must remain visitor-triggered rather than automatic")

    headers = (ROOT / "_headers").read_text(encoding="utf-8")
    if "posthog.com" in headers:
        errors.append("retired PostHog endpoint remains in current public CSP")
    if "connect-src 'self' https://api.github.com" not in headers:
        errors.append("GitHub on-demand catalog endpoint is not narrowly allowed by CSP")

    redirects = (ROOT / "_redirects").read_text(encoding="utf-8")
    for marker in (
        "/repositories.html /github/ 301",
        "/privacy.html /platform-systems/ 301",
        "/security.html /platform-systems/ 301",
        "/firefox-extensions /firefox/ 301",
    ):
        if marker not in redirects:
            errors.append(f"compatibility redirect missing: {marker}")

    if errors:
        print("Website validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Website validation passed: one current website, six canonical public pages, nine platform systems, and 45 Suite products.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
