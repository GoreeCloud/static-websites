#!/usr/bin/env python3
"""Read-only production-source parity and HTTP smoke test for GoreeCloud.com.

No third-party dependencies, credentials, persistence, telemetry or collected user data.
Run against the exact source revision expected to be serving production.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
HOST = "https://www.goreecloud.com"
APEX = "https://goreecloud.com/"
FILES = (
    ("index.html", "/"),
    ("404.html", "/404.html"),
    ("robots.txt", "/robots.txt"),
    ("sitemap.xml", "/sitemap.xml"),
    ("assets/logo.svg", "/assets/logo.svg"),
    ("assets/favicon.svg", "/assets/favicon.svg"),
    ("assets/connected-world.svg", "/assets/connected-world.svg"),
    ("assets/site.css", "/assets/site.css"),
)
REMOVED_ROUTES = (
    "/suite/",
    "/android/",
    "/platform-systems/",
    "/office-suite/",
    "/firefox/",
    "/github/",
    "/privacy/",
    "/security/",
    "/design/",
)
MAX_RESPONSE_BYTES = 1024 * 1024


class SameSiteRedirects(urllib.request.HTTPRedirectHandler):
    """Never follow a redirect outside GoreeCloud's HTTPS website."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlsplit(newurl)
        if parsed.scheme != "https" or parsed.hostname not in (
            "www.goreecloud.com", "goreecloud.com"
        ) or parsed.port not in (None, 443):
            raise ValueError("unexpected redirect origin")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENER = urllib.request.build_opener(SameSiteRedirects())
UA = {"User-Agent": "GoreeCloud-production-integrity-check/1.0"}


def fetch(url: str):
    """Return (status, final URL, response headers, capped bytes)."""
    request = urllib.request.Request(url, headers=UA)
    for attempt in range(3):
        try:
            response = OPENER.open(request, timeout=12)
        except urllib.error.HTTPError as exc:
            response = exc
        except (OSError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(attempt + 1)
            continue
        try:
            if response.status in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(attempt + 1)
                continue
            return (
                response.status,
                response.geturl(),
                response.headers,
                response.read(MAX_RESPONSE_BYTES + 1),
            )
        finally:
            response.close()
    raise RuntimeError("request retry budget exhausted")


def validate_headers(headers, path: str) -> None:
    csp = headers.get("Content-Security-Policy", "")
    for directive in ("default-src 'self'", "script-src 'none'", "object-src 'none'",
                      "frame-ancestors 'none'", "connect-src 'none'"):
        if directive not in csp:
            raise AssertionError(f"{path}: missing CSP directive {directive!r}")
    required = {
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "no-referrer",
        "X-Frame-Options": "DENY",
    }
    for key, value in required.items():
        if headers.get(key, "").lower() != value.lower():
            raise AssertionError(f"{path}: missing or incorrect {key}")


def check() -> None:
    for filename, path in FILES:
        status, final, headers, body = fetch(HOST + path)
        expected_url = HOST + ("/404" if path == "/404.html" else path)
        if status != 200 or final != expected_url:
            raise AssertionError(f"{path}: unexpected status/redirect: {status}")
        validate_headers(headers, path)
        expected = (ROOT / filename).read_bytes()
        if len(body) > MAX_RESPONSE_BYTES or body != expected:
            raise AssertionError(
                f"{path}: source hash mismatch (local {hashlib.sha256(expected).hexdigest()[:12]}, "
                f"served {hashlib.sha256(body).hexdigest()[:12]})"
            )
        print(f"PASS source parity {path}", flush=True)

    for path in REMOVED_ROUTES:
        status, final, headers, _ = fetch(HOST + path)
        if status != 404 or final != HOST + path:
            raise AssertionError(f"{path}: obsolete page returned {status}")
        validate_headers(headers, path)
        print(f"PASS obsolete route 404 {path}", flush=True)

    status, final, headers, _ = fetch(APEX)
    if status != 200 or final != HOST + "/":
        raise AssertionError("apex redirect did not reach canonical homepage")
    validate_headers(headers, "/")
    print("PASS HTTPS apex canonical redirect", flush=True)


if __name__ == "__main__":
    try:
        check()
    except (AssertionError, urllib.error.URLError, OSError, ValueError) as exc:
        print(f"FAIL production integrity: {exc}", file=sys.stderr)
        raise SystemExit(1) from None
    print("PASS production matches committed homepage source", flush=True)
