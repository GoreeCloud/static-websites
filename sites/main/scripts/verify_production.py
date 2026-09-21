#!/usr/bin/env python3
"""Verify the exact retained GoreeCloud website artifact on the production hostname."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

from build_public_site import DIST

ORIGIN = "https://www.goreecloud.com"
ROUTES = {
    "/": "index.html",
    "/design/": "design/index.html",
    "/security/": "security/index.html",
    "/privacy/": "privacy/index.html",
}
ATTEMPTS = 6
SLEEP_SECONDS = 10
MAX_BYTES = 2_000_000


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(route: str, marker: str) -> tuple[bytes, str, object]:
    query = urlencode({"goreecloud_verify": marker})
    request = Request(
        f"{ORIGIN}{route}?{query}",
        headers={
            "User-Agent": "GoreeCloud-Production-Verification/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urlopen(request, timeout=20) as response:
        final_url = response.geturl()
        split = urlsplit(final_url)
        if split.scheme != "https" or split.netloc != "www.goreecloud.com":
            raise RuntimeError(f"{route} escaped canonical production origin: {final_url}")
        if response.status != 200:
            raise RuntimeError(f"{route} returned HTTP {response.status}")
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise RuntimeError(f"{route} exceeded bounded response size")
        return body, final_url, response.headers


def verify_once(expected_revision: str) -> list[str]:
    failures: list[str] = []
    for route, relative in ROUTES.items():
        expected_path = DIST / relative
        if not expected_path.is_file():
            failures.append(f"{route}: expected artifact file missing: {relative}")
            continue
        expected = expected_path.read_bytes()
        try:
            actual, final_url, headers = fetch(route, expected_revision[:12])
        except (HTTPError, URLError, TimeoutError, RuntimeError) as exc:
            failures.append(f"{route}: request failed: {exc}")
            continue
        if actual != expected:
            failures.append(
                f"{route}: byte mismatch expected_sha256={digest(expected)} "
                f"actual_sha256={digest(actual)} expected_bytes={len(expected)} "
                f"actual_bytes={len(actual)} final_url={final_url}"
            )
            continue
        if not headers.get("Strict-Transport-Security", ""):
            failures.append(f"{route}: exact bytes matched but HSTS header is missing")
    return failures


def main() -> int:
    if not DIST.is_dir():
        print("Production verification failed: isolated artifact is missing.")
        return 1

    expected_revision = os.environ.get("EXPECTED_REVISION", "").strip()
    if len(expected_revision) != 40:
        print("Production verification failed: EXPECTED_REVISION must be an exact 40-character Git SHA.")
        return 1

    failures: list[str] = []
    for attempt in range(1, ATTEMPTS + 1):
        failures = verify_once(expected_revision)
        if not failures:
            print(
                "Production verification passed: Home, Design, Security, and Privacy "
                f"match the exact isolated artifact for {expected_revision}."
            )
            return 0
        print(f"Production verification attempt {attempt}/{ATTEMPTS} did not match:")
        for failure in failures:
            print(f"  - {failure}")
        if attempt < ATTEMPTS:
            time.sleep(SLEEP_SECONDS)

    print("Production verification failed after bounded retries.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
