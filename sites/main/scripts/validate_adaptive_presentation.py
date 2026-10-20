#!/usr/bin/env python3
"""Validate adaptive presentation of the retained website without retired upstream dependencies.

This is a *transition* guard, not a claim of full GC UI consumer acceptance.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "css/site-v9.css"
CANONICAL = (
    "index.html", "platform-systems/index.html", "suite/index.html",
    "android/index.html", "office-suite/index.html", "firefox/index.html",
    "github/index.html", "contact/index.html", "design/index.html",
    "security/index.html", "privacy/index.html",
)
REQUIRED_ADAPTIVE_CSS = (
    ":focus-visible",
    "prefers-reduced-motion",
    "prefers-reduced-transparency",
    "prefers-contrast:more",
    "forced-colors:active",
    "min-height:48px",
)


def main() -> int:
    errors: list[str] = []
    if CSS.is_symlink() or not CSS.is_file():
        errors.append("reviewed current-site CSS is absent or unsafe")
        css = ""
    else:
        css = CSS.read_text(encoding="utf-8")
    for marker in REQUIRED_ADAPTIVE_CSS:
        if marker not in css:
            errors.append(f"current-site adaptive CSS missing {marker}")
    for relative in CANONICAL:
        path = ROOT / relative
        if path.is_symlink() or not path.is_file():
            errors.append(f"retained route missing or unsafe: {relative}")
            continue
        content = path.read_text(encoding="utf-8")
        if "<main" not in content or "<h1" not in content or 'lang="en"' not in content:
            errors.append(f"retained route missing basic semantic structure: {relative}")
    if errors:
        print("Website adaptive presentation transition validation failed:")
        for problem in errors:
            print("  - " + problem)
        return 1
    print("Retained website adaptive CSS and 11 page structures verified. GC UI consumer cutover remains unaccepted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
