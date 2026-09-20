#!/usr/bin/env python3
"""Build the allowlisted artifact for GoreeCloud's one retained public website."""

from __future__ import annotations

from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

PUBLIC_FILES = (
    ".well-known/security.txt",
    "404.html",
    "_headers",
    "_redirects",
    "assets/goreecloud-logo.svg",
    "assets/social-preview.png",
    "css/site-v8.css",
    "firefox/index.html",
    "github/index.html",
    "googlea0a636fd5dafd9e0.html",
    "index.html",
    "js/site-v8.js",
    "js/theme-init-v8.js",
    "office-suite/index.html",
    "platform-systems/index.html",
    "privacy.html",
    "repositories.html",
    "robots.txt",
    "security.html",
    "site.webmanifest",
    "sitemap.xml",
    "suite/index.html",
)


def fail(message: str) -> int:
    print(f"Public-site build failed: {message}")
    return 1


def main() -> int:
    if len(PUBLIC_FILES) != len(set(PUBLIC_FILES)):
        return fail("public allowlist contains duplicate paths")

    try:
        for relative in PUBLIC_FILES:
            source = ROOT / relative
            if not source.is_file():
                return fail(f"required public source is missing: {relative}")
            if source.is_symlink():
                return fail(f"public source must not be a symlink: {relative}")

        if DIST.exists():
            if DIST.is_symlink():
                return fail("dist must not be a symlink")
            shutil.rmtree(DIST)
        DIST.mkdir()

        for relative in PUBLIC_FILES:
            source = ROOT / relative
            destination = DIST / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

        for path in DIST.rglob("*"):
            if path.is_symlink():
                return fail(f"artifact contains a symlink: {path.relative_to(DIST)}")

    except OSError as exc:
        return fail(str(exc))

    file_count = sum(path.is_file() for path in DIST.rglob("*"))
    total_bytes = sum(path.stat().st_size for path in DIST.rglob("*") if path.is_file())
    print(f"Built GoreeCloud retained-site artifact: {file_count} files, {total_bytes} bytes -> dist/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
