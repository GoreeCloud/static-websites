#!/usr/bin/env python3
"""Validate the one-website GoreeCloud public URL namespace."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "sites" / "url-namespace.json"
EXPECTED_PATHS = {
    "home": "/",
    "platform-systems": "/platform-systems/",
    "suite": "/suite/",
    "android": "/android/",
    "office-suite": "/office-suite/",
    "firefox": "/firefox/",
    "github": "/github/",
    "contact": "/contact/",
    "design": "/design/",
    "security": "/security/",
    "privacy": "/privacy/",
}


def fail(message: str) -> None:
    raise SystemExit(f"URL namespace validation failed: {message}")


def main() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("schema_version") != "2.0":
        fail("schema_version must be 2.0")
    if data.get("repository") != "GoreeCloud/static-websites":
        fail("repository authority is incorrect")
    if data.get("canonical_origin") != "https://www.goreecloud.com":
        fail("canonical_origin must be https://www.goreecloud.com")
    if data.get("state") != "single-retained-website":
        fail("state must be single-retained-website")

    website = data.get("website")
    if not isinstance(website, dict):
        fail("website object is missing")
    if website.get("id") != "main" or website.get("current_public_host") != "www.goreecloud.com":
        fail("www.goreecloud.com must be the one retained website")
    if website.get("source_path") != "sites/main":
        fail("retained website source_path must be sites/main")
    if website.get("build_command") != ["python", "sites/main/scripts/build_public_site.py"]:
        fail("retained website build command drifted")

    paths = data.get("canonical_paths")
    if not isinstance(paths, list):
        fail("canonical_paths must be a list")
    found = {entry.get("id"): entry.get("path") for entry in paths}
    if found != EXPECTED_PATHS:
        fail(f"canonical path inventory drifted: {found!r}")

    seen: set[str] = set()
    for entry in paths:
        path = entry["path"]
        source = entry.get("source")
        if path in seen:
            fail(f"duplicate canonical path: {path}")
        seen.add(path)
        if path != "/" and (not path.startswith("/") or not path.endswith("/")):
            fail(f"canonical path is not normalized: {path}")
        if not isinstance(source, str) or not source.startswith("sites/main/"):
            fail(f"invalid source for {entry.get('id')}: {source!r}")
        source_file = ROOT / source
        if not source_file.is_file() or source_file.is_symlink():
            fail(f"canonical source missing or unsafe: {source}")

    compatibility = data.get("compatibility_paths")
    if not isinstance(compatibility, list):
        fail("compatibility_paths must be a list")
    redirect_text = (ROOT / "sites/main/_redirects").read_text(encoding="utf-8")
    for entry in compatibility:
        old = entry.get("from")
        new = entry.get("to")
        if not isinstance(old, str) or not isinstance(new, str):
            fail("compatibility route requires from/to strings")
        if f"{old} {new} 301" not in redirect_text:
            fail(f"compatibility route is not implemented in _redirects: {old} -> {new}")

    boundary = data.get("historical_boundary", "")
    if "not current website inventory" not in boundary:
        fail("historical multi-site source must be explicitly non-current")

    print("URL namespace valid: one retained website with eleven canonical path-based destinations.")


if __name__ == "__main__":
    main()
