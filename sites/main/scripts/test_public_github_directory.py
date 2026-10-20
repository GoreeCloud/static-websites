#!/usr/bin/env python3
"""Verify the existing site's opt-in public repository directory without GitHub credentials."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
URL = "https://api.github.com/users/GoreeCloud/repos"
RETIRED = "https://api.github.com/orgs/GoreeCloud/repos"


def violations(script, page):
    problems = []
    if URL not in script or RETIRED in script:
        problems.append("incorrect public GitHub API identity")
    if "?type=owner&" not in script:
        problems.append("missing owned-repository query")
    if 'credentials: "omit"' not in script:
        problems.append("cross-origin credentials are not explicitly disabled")
    if 'redirect: "error"' not in script:
        problems.append("unexpected API redirects are not rejected")
    click = script.find('load.addEventListener("click", async () => {')
    fetch = script.find('await fetch(')
    if click < 0 or fetch < click:
        problems.append("repository data requested before explicit visitor action")
    for text in ("data-load-github", "data-github-status", "data-github-list"):
        if text not in page:
            problems.append("missing " + text)
    if "public organization endpoint" in page or "GitHub organization" in page:
        problems.append("outdated GitHub organization claim")
    if "does not publish private repository names" not in page:
        problems.append("lost public-only privacy disclosure")
    return problems


class DirectoryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = (ROOT / "js" / "site-v8.js").read_text(encoding="utf-8")
        cls.page = (ROOT / "github" / "index.html").read_text(encoding="utf-8")

    def test_current_public_account_directory(self):
        self.assertEqual(violations(self.script, self.page), [])

    def test_wrong_org_api_rejected(self):
        value = self.script.replace(URL, RETIRED)
        self.assertIn("incorrect public GitHub API identity", violations(value, self.page))

    def test_credential_regression_rejected(self):
        value = self.script.replace('credentials: "omit"', 'credentials: "include"')
        self.assertIn("cross-origin credentials are not explicitly disabled",
                      violations(value, self.page))

    def test_hidden_automatic_load_rejected(self):
        value = self.script.replace('load.addEventListener("click", async () => {',
                                    'document.addEventListener("load", async () => {')
        self.assertIn("repository data requested before explicit visitor action",
                      violations(value, self.page))


if __name__ == "__main__":
    unittest.main()
