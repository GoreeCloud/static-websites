#!/usr/bin/env python3
import json
from pathlib import Path
import sys
import unittest
from email.message import Message

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import verify_production as verifier  # noqa: E402


class ProductionVerifierTests(unittest.TestCase):
    def test_verifier_tracks_authoritative_namespace(self):
        namespace = json.loads((ROOT.parent / "url-namespace.json").read_text(encoding="utf-8"))
        self.assertEqual(list(verifier.ROUTES), [entry["path"] for entry in namespace["canonical_paths"]])
        self.assertEqual(verifier.REDIRECTS, {entry["from"]: entry["to"] for entry in namespace["compatibility_paths"]})

    def test_required_headers_accept_current_contract(self):
        headers = Message()
        for name, value in verifier.REQUIRED_HEADER_VALUES.items():
            headers[name] = value
        headers["Content-Security-Policy"] = "; ".join(verifier.REQUIRED_CSP_PARTS)
        self.assertEqual(verifier.validate_headers("/", headers, require_indexable=True), [])

    def test_noindex_and_missing_csp_fail_closed(self):
        headers = Message()
        for name, value in verifier.REQUIRED_HEADER_VALUES.items():
            headers[name] = value
        headers["X-Robots-Tag"] = "noindex"
        failures = verifier.validate_headers("/", headers, require_indexable=True)
        self.assertTrue(any("Content-Security-Policy header is missing" in failure for failure in failures))
        self.assertTrue(any("production route is marked noindex" in failure for failure in failures))

    def test_request_for_disables_intermediary_cache(self):
        request = verifier.request_for("https://www.goreecloud.com/")
        self.assertEqual(request.get_header("Cache-control"), "no-cache")
        self.assertEqual(request.get_header("Pragma"), "no-cache")


if __name__ == "__main__":
    unittest.main()
