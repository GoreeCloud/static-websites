#!/usr/bin/env python3
"""Compatibility wrapper for building GoreeCloud's one retained public website.

The former multi-site namespace builder is retired. This wrapper delegates to
sites/main/scripts/build_public_site.py and mirrors that reviewed artifact to
repository-root dist/ only for tooling that still invokes the historical entrypoint.
"""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MAIN_DIST = ROOT / "sites/main/dist"
OUTPUT = ROOT / "dist"


def main() -> int:
    validate = subprocess.run(
        [sys.executable, "scripts/validate_url_namespace.py"],
        cwd=ROOT,
        check=False,
    )
    if validate.returncode:
        return validate.returncode

    build = subprocess.run(
        [sys.executable, "sites/main/scripts/build_public_site.py"],
        cwd=ROOT,
        check=False,
    )
    if build.returncode:
        return build.returncode

    if not MAIN_DIST.is_dir() or MAIN_DIST.is_symlink():
        print("Unified build failed: retained-site artifact is missing or unsafe.")
        return 1

    if OUTPUT.exists():
        if OUTPUT.is_symlink():
            print("Unified build failed: root dist must not be a symlink.")
            return 1
        shutil.rmtree(OUTPUT)
    shutil.copytree(MAIN_DIST, OUTPUT)

    count = sum(path.is_file() for path in OUTPUT.rglob("*"))
    print(f"Built one retained www artifact through compatibility entrypoint: {count} files -> dist/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
