#!/usr/bin/env python3
"""Dependency-free, fail-closed validation of a preview-only static snapshot.

No network calls, secret access or deployment. Git and Cloudflare are not touched.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
MANIFEST = ROOT / "SITE-MANIFEST.sha256"
REQUIRED = [
    "/", "/platform-systems/", "/suite/", "/android/", "/office-suite/",
    "/firefox/", "/github/", "/contact/", "/design/", "/security/",
    "/privacy/", "/ecosystem/", "/products/", "/principles/"
]
PROBLEMS: list[str] = []


def fail(message: str) -> None:
    PROBLEMS.append(message)


def main() -> int:
    if not MANIFEST.is_file():
        fail("Missing immutable manifest")
        lines = []
    else:
        lines = MANIFEST.read_text("utf-8").splitlines()
    checked: set[str] = set()
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  (site/[\w./-]+)", line)
        if not match:
            fail("Malformed manifest row")
            continue
        digest, relative = match.groups()
        if relative in checked or ".." in Path(relative).parts:
            fail("Duplicate or unsafe manifest path")
            continue
        checked.add(relative)
        p = ROOT / relative
        if not p.is_file() or p.is_symlink():
            fail("Missing or linked asset: " + relative)
            continue
        if hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            fail("Changed asset: " + relative)
    actual = {"site/" + str(p.relative_to(SITE)) for p in SITE.rglob("*") if p.is_file()}
    if actual != checked:
        fail("Manifest does not exactly cover all site files")
    if len(actual) != 33:
        fail("Expected exactly 33 reviewed iteration assets")
    headers = (SITE / "_headers").read_text("utf-8")
    robots = (SITE / "robots.txt").read_text("utf-8")
    redirects = (SITE / "_redirects").read_text("utf-8")
    for required in ["X-Robots-Tag: noindex, nofollow",
                     "X-Frame-Options: DENY", "X-Content-Type-Options: nosniff",
                     "Content-Security-Policy:", "script-src 'self'",
                     "object-src 'none'", "frame-ancestors 'none'"]:
        if required not in headers:
            fail("Missing protective _headers directive: " + required)
    for forbidden in ["'unsafe-inline'", "'unsafe-eval'", "script-src *"]:
        if forbidden in headers:
            fail("Unsafe CSP: " + forbidden)
    if "Disallow: /" not in robots:
        fail("Preview robots.txt must disallow crawling")
    if redirects.strip().splitlines()[-1:] != ["/social/ /contact/ 302"]:
        fail("Unexpected non-preview redirect")
    for route in REQUIRED:
        p = SITE / route.strip("/") / "index.html"
        if not p.is_file():
            fail("Missing route: " + route)
            continue
        html = p.read_text("utf-8")
        if 'name="robots"' not in html or "noindex" not in html:
            fail("Indexable candidate route: " + route)
        if "http-equiv=\"refresh\"" in html.lower():
            fail("Unapproved refresh redirect: " + route)
        if '<script src="/assets/site.js" defer></script>' not in html:
            fail("Missing expected first-party script: " + route)
    pins = {
        'app-icon.svg': '0b16beadbb8a9aa27baf912bfc5c6b40f30cf22c00b156e35c748e909a50a1a8',
        'symbol.svg': 'b4eb6b2e7185cd5a0ecb7d06513f3e5731ae0e3dd950d23fc4fabb8ba8eb9acd',
        'logo-light.svg': '8364d2d74a2a0874f109c2c015193e524104ba3be0a6998bb3f1e41b7442aecb',
        'logo-dark.svg': 'b3f7823cb6cce5fcaa68198a917d8c72e11db32901071f5afee2ad221a111906',
        'favicon.ico': '574ff31eeaa9fe6e155c2e555430a80a87748574dcc590fc9958318a044c1a08',
        'interface-constellation.svg': '695391d4c4b3360abb5979e73593ca2ed50794dca2ad3ee8b66f12ff4eba4ae2',
    }
    for name,digest in pins.items():
        candidate = SITE / "assets/gc-ui" / name
        if not candidate.is_file() or hashlib.sha256(candidate.read_bytes()).hexdigest() != digest:
            fail("Official asset pin mismatch: "+name)
    permanent = SITE / "assets/goreecloud"
    for name,digest in {
        "official-profile-logo-1024.png": "ac5c76fda60abbf5fc65957b18a3b4053dccb4b3cb42687dcd0bb428709c69e8",
        "logo.svg": '544e1e83ea4d8c67314286d7cc637b5cfc7c78d122c9595eba259c7075f654c6',
        "favicon.ico": 'e038e993e53a274b52abf246a649e21f6066553b51e89bb777126ea47325fcc3'
    }.items():
        if not (permanent/name).is_file() or hashlib.sha256((permanent/name).read_bytes()).hexdigest()!=digest:
            fail("GoreeCloud umbrella master pin mismatch: "+name)
    for html in SITE.rglob("*.html"):
        body=html.read_text("utf-8")
        if '/assets/goreecloud/favicon.ico' not in body or '/assets/goreecloud/logo.svg' not in body:
            fail("Missing umbrella site favicon: "+str(html))
        if 'brand-glyph' in body:
            fail("Unapproved generic umbrella identity survives: "+str(html))
    if 'Flowframe v2 concept · Under review' not in (SITE/"design/index.html").read_text("utf-8"):
        fail("New GC UI candidate missing approval boundary")
    gcui_page = (SITE / "design/index.html").read_text("utf-8")
    for marker in ('/assets/gc-ui/logo-light.svg','/assets/gc-ui/logo-dark.svg',
                   '/assets/gc-ui/interface-constellation.svg'):
        if marker not in gcui_page:
            fail("GoreeCloud UI review page missing candidate artwork: "+marker)
    for page in ("products/index.html", "github/index.html", "suite/index.html"):
        html = (SITE / page).read_text("utf-8")
        for element in ('/assets/catalog-tools.js', 'data-catalog-actions=',
                        'data-catalog-share', 'data-catalog-reset',
                        'data-catalog-status', 'data-catalog-link'):
            if element not in html:
                fail(f"Catalog controls missing {element} on {page}")
    if not (SITE / "assets/catalog-tools.js").is_file():
        fail("Missing first-party catalog enhancement script")
    if not (SITE / "404.html").is_file():
        fail("Missing 404 asset")
    if "<" in redirects.splitlines()[-1]:
        fail("Malformed redirects file")
    if PROBLEMS:
        print("BLOCKED preview snapshot:\n" + "\n".join("- " + s for s in PROBLEMS))
        return 1
    print(f"PASS preview-only snapshot: {len(actual)} SHA-256 files, {len(REQUIRED)} routes, noindex and CSP")
    return 0


if __name__ == "__main__":
    sys.exit(main())
