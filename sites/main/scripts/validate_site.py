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
    "contact/index.html": "https://www.goreecloud.com/contact/",
    "design/index.html": "https://www.goreecloud.com/design/",
    "security/index.html": "https://www.goreecloud.com/security/",
    "privacy/index.html": "https://www.goreecloud.com/privacy/",
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
PROHIBITED_PLACEHOLDER_MARKERS = (
    'product-card no-icon',
    'class="app-symbol"',
    'extension-art generic',
    '<div class="symbol">',
    '<span class="initials">',
    '<span>PL</span>',
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
    for placeholder in PROHIBITED_PLACEHOLDER_MARKERS:
        if placeholder in text:
            errors.append(f"{relative} contains prohibited placeholder visual treatment: {placeholder}")
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
        "45",
        "Nine cross-cutting authorities.",
        "Glaze UI V1.6",
        "/platform-systems/",
        "/suite/",
        "/office-suite/",
        "/firefox/",
        "/github/",
        "/contact/",
        "/privacy/",
        "/security/",
        "/design/",
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
    for identifier in ('id="privacy-shield"', 'id="wardveil-security"', 'id="glaze-ui"'):
        if identifier not in platform[0]:
            errors.append(f"platform-systems missing direct system anchor: {identifier}")

    suite = audited.get("suite/index.html", ("", Audit()))
    if suite[1].classes["product-section"] != 9:
        errors.append(f"suite must contain nine product groups; found {suite[1].classes['product-section']}")
    if suite[1].classes["product-card"] != 45:
        errors.append(f"suite must contain 45 current products; found {suite[1].classes['product-card']}")


    visual_requirements = {
        "index.html": ("hero-visual", "feature-card", "aura-panel", "/assets/brand/goreecloud-logo.svg", "/assets/products/drive.svg"),
        "platform-systems/index.html": ("system-map", "system-card", "/assets/systems/privacy-shield.svg", "/assets/systems/wardveil-security.svg", "/assets/systems/policy.svg", "/assets/systems/observability.svg"),
        "suite/index.html": ("hero-visual", "product-card", "/assets/products/notes.svg", "/assets/products/photos.svg", "/assets/products/sync.svg", "/assets/products/reader.svg", "/assets/products/social.svg", "/assets/products/keyboard.svg", "/assets/products/health.svg", "/assets/products/home.svg", "/assets/products/home-security.svg", "/assets/products/router-os.svg", "/assets/products/website.svg"),
        "office-suite/index.html": ("office-stage", "office-family", "arch-card", "/assets/products/office.svg", "/assets/products/writer.svg", "/assets/products/spreadsheet.svg", "/assets/products/presentations.svg", "/assets/products/forms.svg"),
        "firefox/index.html": ("browser-stage", "extension-card", "/assets/firefox/advanced-tab-manager.svg", "/assets/firefox/webspaces.svg", "/assets/firefox/redirector.svg"),
        "github/index.html": ("code-stage", "story-card", "/assets/brand/goreecloud-logo.svg"),
        "contact/index.html": ("contact-stage", "social-card", "/assets/social/instagram.ico", "support@goreecloud.com", "security@goreecloud.com"),
        "design/index.html": ("identity-stage", "design-lab", "material-grid", "/assets/systems/glaze-ui.svg", "Official Stable"),
        "security/index.html": ("identity-stage", "authority-flow", "showcase-card", "/assets/systems/wardveil-security.svg", "scope-specific evidence"),
        "privacy/index.html": ("identity-stage", "authority-flow", "showcase-card", "/assets/systems/privacy-shield.svg", "Privacy Shield remains in Development"),
    }
    for relative, markers in visual_requirements.items():
        text_value = audited.get(relative, ("", Audit()))[0]
        for marker in markers:
            if marker not in text_value:
                errors.append(f"{relative} missing required Glaze visual identity marker: {marker}")

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

    contact = audited.get("contact/index.html", ("", Audit()))[0]
    for marker in (
        "Instagram", "@goreecloud", "Threads", "TikTok", "@GoreeCloud",
        "Reddit", "u/goreecloud", "Pinterest", "support@goreecloud.com", "security@goreecloud.com",
        "personal phone numbers", "private email accounts", "residential or mailing addresses",
    ):
        if marker not in contact:
            errors.append(f"contact page missing verified public-contact/privacy marker: {marker}")
    if "334-" in contact or "slickkredd@" in contact or "goreeboy@" in contact:
        errors.append("contact page must not publish private owner contact records")

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
        "/privacy.html /privacy/ 301",
        "/security.html /security/ 301",
        "/firefox-extensions /firefox/ 301",
    ):
        if marker not in redirects:
            errors.append(f"compatibility redirect missing: {marker}")

    if errors:
        print("Website validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Website validation passed: one current website, ten canonical public pages, nine platform systems, and 45 Suite products.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
