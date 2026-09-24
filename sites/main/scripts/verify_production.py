#!/usr/bin/env python3
"""Verify the exact retained GoreeCloud website artifact on the production hostname."""

from __future__ import annotations

import hashlib
import os
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen

from build_public_site import DIST

ORIGIN = "https://www.goreecloud.com"
ROUTES = {
    "/": "index.html",
    "/android/": "android/index.html",
    "/design/": "design/index.html",
    "/security/": "security/index.html",
    "/privacy/": "privacy/index.html",
}
REDIRECTS = {
    "/privacy.html": "/privacy/",
    "/security.html": "/security/",
}
ATTEMPTS = 6
SLEEP_SECONDS = 10
MAX_BYTES = 2_000_000
REQUIRED_HEADER_VALUES = {
    "Strict-Transport-Security": "max-age=31536000",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
}
REQUIRED_CSP_PARTS = (
    "default-src 'self'",
    "object-src 'none'",
    "frame-ancestors 'none'",
    "script-src 'self'",
    "style-src 'self'",
    "connect-src 'self' https://api.github.com",
)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def request_for(url: str) -> Request:
    return Request(
        url,
        headers={
            "User-Agent": "GoreeCloud-Production-Verification/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )


def bounded_read(response) -> bytes:
    body = response.read(MAX_BYTES + 1)
    if len(body) > MAX_BYTES:
        raise RuntimeError("response exceeded bounded response size")
    return body


def validate_headers(route: str, headers, *, require_indexable: bool) -> list[str]:
    failures: list[str] = []
    for name, expected in REQUIRED_HEADER_VALUES.items():
        actual = headers.get(name, "")
        if actual != expected:
            failures.append(f"{route}: {name} mismatch: {actual!r}")
    csp = headers.get("Content-Security-Policy", "")
    if not csp:
        failures.append(f"{route}: Content-Security-Policy header is missing")
    else:
        for part in REQUIRED_CSP_PARTS:
            if part not in csp:
                failures.append(f"{route}: Content-Security-Policy missing directive: {part}")
    if require_indexable and "noindex" in headers.get("X-Robots-Tag", "").lower():
        failures.append(f"{route}: production route is marked noindex by X-Robots-Tag")
    return failures


def fetch_exact(route: str, marker: str):
    query = urlencode({"goreecloud_verify": marker})
    with urlopen(request_for(f"{ORIGIN}{route}?{query}"), timeout=20) as response:
        final_url = response.geturl()
        split = urlsplit(final_url)
        if split.scheme != "https" or split.netloc != "www.goreecloud.com":
            raise RuntimeError(f"{route} escaped canonical production origin: {final_url}")
        if split.path != route:
            raise RuntimeError(f"{route} resolved to unexpected path: {split.path}")
        if response.status != 200:
            raise RuntimeError(f"{route} returned HTTP {response.status}")
        return bounded_read(response), final_url, response.headers


def verify_redirect(source: str, target: str, marker: str) -> list[str]:
    failures: list[str] = []
    query = urlencode({"goreecloud_verify": marker})
    opener = build_opener(NoRedirect())
    request = request_for(f"{ORIGIN}{source}?{query}")
    try:
        response = opener.open(request, timeout=20)
        status = response.status
        headers = response.headers
        response.close()
    except HTTPError as exc:
        status = exc.code
        headers = exc.headers
        exc.close()
    except (URLError, TimeoutError) as exc:
        return [f"{source}: redirect request failed: {exc}"]

    if status != 301:
        failures.append(f"{source}: expected HTTP 301; got {status}")
    location = headers.get("Location", "")
    if not location:
        failures.append(f"{source}: redirect Location header is missing")
    else:
        resolved = urlsplit(urljoin(ORIGIN, location))
        if resolved.scheme != "https" or resolved.netloc != "www.goreecloud.com" or resolved.path != target:
            failures.append(f"{source}: redirect target mismatch: {location!r}")
    return failures


def verify_404(expected_revision: str) -> list[str]:
    route = f"/__goreecloud-production-verification-404__-{expected_revision[:12]}"
    opener = build_opener(NoRedirect())
    request = request_for(ORIGIN + route)
    try:
        response = opener.open(request, timeout=20)
        status = response.status
        headers = response.headers
        body = bounded_read(response)
        response.close()
    except HTTPError as exc:
        status = exc.code
        headers = exc.headers
        body = bounded_read(exc)
        exc.close()
    except (URLError, TimeoutError, RuntimeError) as exc:
        return [f"{route}: 404 request failed: {exc}"]

    failures: list[str] = []
    if status != 404:
        failures.append(f"{route}: expected HTTP 404; got {status}")
        return failures
    expected = (DIST / "404.html").read_bytes()
    if body != expected:
        failures.append(
            f"{route}: 404 body mismatch expected_sha256={digest(expected)} "
            f"actual_sha256={digest(body)}"
        )
    failures.extend(validate_headers(route, headers, require_indexable=False))
    return failures


def verify_once(expected_revision: str) -> list[str]:
    failures: list[str] = []
    marker = expected_revision[:12]

    for route, relative in ROUTES.items():
        expected_path = DIST / relative
        if not expected_path.is_file():
            failures.append(f"{route}: expected artifact file missing: {relative}")
            continue
        expected = expected_path.read_bytes()
        try:
            actual, final_url, headers = fetch_exact(route, marker)
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
        failures.extend(validate_headers(route, headers, require_indexable=True))

    for source, target in REDIRECTS.items():
        failures.extend(verify_redirect(source, target, marker))

    failures.extend(verify_404(expected_revision))
    return failures


def main() -> int:
    if not DIST.is_dir():
        print("Production verification failed: isolated artifact is missing.")
        return 1
    if not (DIST / "404.html").is_file():
        print("Production verification failed: isolated 404 artifact is missing.")
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
                "Production verification passed: Home, Android, Design, Security, and Privacy match "
                f"the exact isolated artifact for {expected_revision}; required security/indexing "
                "headers, Privacy/Security legacy redirects, and exact 404 behavior are verified."
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
