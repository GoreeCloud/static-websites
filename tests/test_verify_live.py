"""Offline tests for the read-only HTTPS integrity checker."""
import unittest
import urllib.request

from scripts import verify_live


class LiveCheckerContract(unittest.TestCase):
    def test_fixed_targets(self):
        self.assertEqual(verify_live.HOST, "https://www.goreecloud.com")
        self.assertEqual(verify_live.APEX, "https://goreecloud.com/")
        self.assertEqual(len(verify_live.FILES), 9)
        self.assertEqual(len(verify_live.REMOVED_ROUTES), 9)
        self.assertEqual(len(set(path for _, path in verify_live.FILES)), 9)
        self.assertEqual(len(set(verify_live.REMOVED_ROUTES)), 9)
        self.assertNotIn("/", verify_live.REMOVED_ROUTES)

    def test_security_headers_mandatory(self):
        headers = {
            "Content-Security-Policy": "default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none'; connect-src 'none'",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "no-referrer",
            "X-Frame-Options": "DENY",
        }
        verify_live.validate_headers(headers, "/")
        headers["Content-Security-Policy"] = "default-src 'self'"
        with self.assertRaises(AssertionError):
            verify_live.validate_headers(headers, "/")

    def test_off_domain_redirect_is_rejected(self):
        handler = verify_live.SameSiteRedirects()
        request = urllib.request.Request(verify_live.APEX)
        with self.assertRaises(ValueError):
            handler.redirect_request(request, None, 302, "Found", {}, "https://example.com/")
        with self.assertRaises(ValueError):
            handler.redirect_request(request, None, 302, "Found", {}, "http://www.goreecloud.com/")
        allowed = handler.redirect_request(
            request, None, 301, "Moved", {}, "https://www.goreecloud.com/"
        )
        self.assertEqual(allowed.full_url, "https://www.goreecloud.com/")


if __name__ == "__main__":
    unittest.main()
