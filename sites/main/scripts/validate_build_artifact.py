#!/usr/bin/env python3
"""Validate the exact GoreeCloud retained-site build artifact."""

from __future__ import annotations

import ipaddress
from pathlib import Path
import re
import sys

from build_public_site import DIST, PUBLIC_FILES, ROOT

CANONICAL_PAGES = (
    "index.html",
    "platform-systems/index.html",
    "suite/index.html",
    "office-suite/index.html",
    "firefox/index.html",
    "github/index.html",
)
COMPATIBILITY_PAGES = ("privacy.html", "security.html", "repositories.html", "404.html")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
CGNAT = ipaddress.ip_network("100.64.0.0/10")
STALE_CURRENT_MARKERS = (
    "Seven systems. Seven distinct responsibilities.",
    "seven Integral Platform Systems",
    "Fourteen official surfaces",
    "14 official public website",
    "GLAZE UI V1.3",
    "GLAZE UI V1.4 / 1.4",
    "suite.goreecloud.com",
    "firefox.goreecloud.com",
    "design.goreecloud.com",
    "privacy.goreecloud.com",
    "security.goreecloud.com",
)


def contains_private_address(text: str) -> bool:
    for token in IP_RE.findall(text):
        try:
            address = ipaddress.ip_address(token)
        except ValueError:
            continue
        if address.is_private or address in CGNAT:
            return True
    return False


def main() -> int:
    errors: list[str] = []
    if not DIST.is_dir() or DIST.is_symlink():
        print("Build artifact validation failed: dist/ is missing or unsafe.")
        return 1

    expected = {Path(item) for item in PUBLIC_FILES}
    actual = {path.relative_to(DIST) for path in DIST.rglob("*") if path.is_file()}

    for path in sorted(expected - actual):
        errors.append(f"expected file missing from dist: {path}")
    for path in sorted(actual - expected):
        errors.append(f"unexpected file present in dist: {path}")

    for path in DIST.rglob("*"):
        if path.is_symlink():
            errors.append(f"artifact contains symlink: {path.relative_to(DIST)}")

    for relative in sorted(expected & actual):
        source = ROOT / relative
        built = DIST / relative
        if source.read_bytes() != built.read_bytes():
            errors.append(f"built bytes differ from reviewed source: {relative}")

    for page in CANONICAL_PAGES + COMPATIBILITY_PAGES:
        path = DIST / page
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in (
            'data-glaze-version="1.6.0"',
            'name="goreecloud-glaze-ui" content="1.6.0"',
            'name="goreecloud-glaze-consumer-state" content="migration-candidate-unaccepted"',
            "/css/site-v8.css",
            "/js/theme-init-v8.js",
            "/js/site-v8.js",
        ):
            if marker not in text:
                errors.append(f"{page} missing current V1.6 migration marker: {marker}")
        for stale in STALE_CURRENT_MARKERS:
            if stale in text:
                errors.append(f"{page} contains stale current-state marker: {stale}")
        if contains_private_address(text):
            errors.append(f"{page} contains private-range address material")

    headers = (DIST / "_headers").read_text(encoding="utf-8") if (DIST / "_headers").is_file() else ""
    for marker in (
        "Content-Security-Policy:",
        "Referrer-Policy: no-referrer",
        "X-Content-Type-Options: nosniff",
        "https://api.github.com",
    ):
        if marker not in headers:
            errors.append(f"_headers missing required marker: {marker}")
    for stale in ("posthog.com", "us-assets.i.posthog.com"):
        if stale in headers:
            errors.append(f"_headers still permits retired analytics dependency: {stale}")

    if errors:
        print("Build artifact validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    total_bytes = sum((DIST / path).stat().st_size for path in actual)
    print(f"Build artifact validation passed: {len(actual)} files, {total_bytes} bytes, one retained website.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
