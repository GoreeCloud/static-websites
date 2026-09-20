#!/usr/bin/env python3
"""Fail-closed Glaze UI V1.6 target validation for the website migration candidate."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "glaze.lock.json"
PAGES = (
    ROOT / "index.html",
    ROOT / "platform-systems/index.html",
    ROOT / "suite/index.html",
    ROOT / "office-suite/index.html",
    ROOT / "firefox/index.html",
    ROOT / "github/index.html",
)
EXPECTED = {
    "version": "1.6.0",
    "lifecycle": "Stable",
    "repository": "GoreeCloud/glaze-ui",
    "stable_commit": "081527eff1c5fe5001b6b9598d60439c8fb3c5e3",
    "accepted_release_source": "a7180679ea851389e0f3004515f9a25f420e716d",
    "entrypoint": "js/glaze-v1.6.0.mjs",
    "entrypoint_blob": "7dfc863d6c39def97c263de80b21b73efe54db1e",
    "consumer_state": "migration-candidate-unaccepted",
}


def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\x00"
    return hashlib.sha1(header + data, usedforsecurity=False).hexdigest()


def main() -> int:
    errors: list[str] = []
    try:
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Glaze UI validation failed: {exc}")
        return 1

    for key, value in EXPECTED.items():
        if lock.get(key) != value:
            errors.append(f"glaze.lock.json {key} must be {value!r}; found {lock.get(key)!r}")

    source_root = os.environ.get("GLAZE_UI_SOURCE")
    if source_root:
        source = Path(source_root)
        version = source / "VERSION"
        entrypoint = source / EXPECTED["entrypoint"]
        if not version.is_file() or version.read_text(encoding="utf-8").strip() != EXPECTED["version"]:
            errors.append("pinned Glaze source VERSION is not 1.6.0")
        if not entrypoint.is_file():
            errors.append("pinned Glaze V1.6.0 runtime entrypoint is missing")
        elif git_blob_sha(entrypoint.read_bytes()) != EXPECTED["entrypoint_blob"]:
            errors.append("pinned Glaze V1.6.0 runtime entrypoint bytes do not match the accepted blob")

    for page in PAGES:
        if not page.is_file():
            errors.append(f"missing V1.6 consumer page: {page.relative_to(ROOT)}")
            continue
        text = page.read_text(encoding="utf-8")
        for marker in (
            'data-glaze-version="1.6.0"',
            'name="goreecloud-glaze-ui" content="1.6.0"',
            'name="goreecloud-glaze-consumer-state" content="migration-candidate-unaccepted"',
        ):
            if marker not in text:
                errors.append(f"{page.relative_to(ROOT)} missing V1.6 target marker: {marker}")
        for forbidden in ("consumer-state\" content=\"accepted", "production-eligible", "Glaze UI conformant"):
            if forbidden in text:
                errors.append(f"{page.relative_to(ROOT)} overclaims downstream Glaze acceptance: {forbidden}")

    css = (ROOT / "css/site-v8.css").read_text(encoding="utf-8")
    for marker in (
        ":focus-visible",
        "prefers-reduced-motion",
        "prefers-reduced-transparency",
        "prefers-contrast:more",
        "forced-colors:active",
        "min-height:48px",
    ):
        if marker not in css:
            errors.append(f"website V1.6 migration CSS missing accessibility/adaptive marker: {marker}")

    if errors:
        print("Glaze UI V1.6 target validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Glaze UI V1.6 target validation passed. Consumer state remains migration-candidate-unaccepted; this is not downstream acceptance.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
