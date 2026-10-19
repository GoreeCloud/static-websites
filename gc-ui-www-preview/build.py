#!/usr/bin/env python3
"""Build an isolated GC UI design-authority preview, never the public website."""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
import json
import shutil
import sys

SOURCE = Path(__file__).resolve().parent
REPOSITORY = SOURCE.parent
OUT = REPOSITORY / "dist-gc-ui-www-preview"
ASSETS = ("index.html", "site.css", "site.js", "gc-ui-foundations.css")


def build():
    if SOURCE.is_symlink() or not SOURCE.is_dir():
        raise ValueError("unsafe preview source")
    if OUT.is_symlink():
        raise ValueError("unsafe preview output")
    if OUT.exists():
        if not OUT.is_dir():
            raise ValueError("preview output must be a directory")
        shutil.rmtree(OUT)
    OUT.mkdir()
    digests = {}
    for name in ASSETS:
        origin = SOURCE / name
        if not origin.is_file() or origin.is_symlink():
            raise ValueError("missing or unsafe source file " + name)
        value = origin.read_bytes()
        if not value or len(value) > 1000000 or b"\x00" in value:
            raise ValueError("invalid source file " + name)
        (OUT / name).write_bytes(value)
        digests[name] = sha256(value).hexdigest()
    evidence = {
        "schema": "gc-ui-www-isolated-preview.v1",
        "scope": "single-design-route-source-preview-not-deployed",
        "canonicalWebsiteUnchanged": True,
        "deployed": False,
        "gcUiConsumerAccepted": False,
        "gcUiPlatformCutoverComplete": False,
        "files": dict(sorted(digests.items())),
    }
    (OUT / "SHA256SUMS.json").write_text(
        json.dumps(evidence, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return evidence


if __name__ == "__main__":
    try:
        print(json.dumps(build(), sort_keys=True))
    except (OSError, ValueError) as exc:
        print("GC UI preview build refused: " + str(exc), file=sys.stderr)
        sys.exit(1)
