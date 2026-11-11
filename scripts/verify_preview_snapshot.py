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
    if len(actual) != 26:
        fail("Expected exactly 26 reviewed iteration assets")
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
        "app-icon.svg": "a1bf6370761f247a56666c0d61ba615dce3e5789c6e7845c630caecf6d9de418",
        "symbol.svg": "78794bc48907ddd822b42d96cd0be0061bd1b1b4fe168384e5a3818afef50078",
        "logo-light.svg": "4e40c93337c84de16560b26d701a3334d3b448bc7e04a2efe189944eac680682",
        "logo-dark.svg": "dcdd57b18d94673973f1771f91752ece56d93737679b56bed4b8339719d1eb66",
        "favicon.ico": "874fe939d8ce7a3958d11b7d1655daa22389beeb6a903c87eb17590e57a94313",
        "interface-constellation.svg": "50661cf8d84818240ac7ac5e273123e041f9471ef4aa953d2be05019e4aef6aa",
    }
    for name,digest in pins.items():
        candidate = SITE / "assets/gc-ui" / name
        if not candidate.is_file() or hashlib.sha256(candidate.read_bytes()).hexdigest() != digest:
            fail("Official asset pin mismatch: "+name)
    gcui_page = (SITE / "design/index.html").read_text("utf-8")
    for marker in ('/assets/gc-ui/app-icon.svg', '/assets/gc-ui/favicon.ico',
                   '/assets/gc-ui/logo-light.svg','/assets/gc-ui/logo-dark.svg',
                   '/assets/gc-ui/interface-constellation.svg'):
        if marker not in gcui_page:
            fail("GoreeCloud UI page missing official identity: "+marker)
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
