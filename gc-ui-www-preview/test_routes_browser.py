#!/usr/bin/env python3
"""Chromium/Firefox localhost smoke for all eleven non-deployed GC UI routes."""
from __future__ import annotations
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import json

from playwright.sync_api import sync_playwright
from build_routes import OUT, PATHS
from test_routes import verify


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def smoke():
    verify(OUT)
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(OUT)))
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    base = f"http://127.0.0.1:{server.server_port}"
    results = []
    try:
        with sync_playwright() as pw:
            for browser_name in ("chromium", "firefox"):
                browser = getattr(pw, browser_name).launch(headless=True)
                context = browser.new_context(
                    viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
                page = context.new_page()
                resources, errors = [], []
                page.on("request", lambda request: resources.append(request.url))
                page.on("pageerror", lambda error: errors.append(str(error)))
                try:
                    for route in PATHS.values():
                        response = page.goto(base + route, wait_until="networkidle")
                        assert response and response.status == 200, (browser_name, route, "not served")
                        assert page.get_by_role("main").count() == 1
                        assert page.get_by_role("heading", level=1).count() == 1
                        assert page.get_by_role("navigation", name="Retained website routes").count() == 1
                        assert page.locator('nav[aria-label="Retained website routes"] a').count() == 11
                        assert page.locator('nav[aria-label="Retained website routes"] a[aria-current="page"]').count() == 1
                        assert page.locator('meta[name="robots"]').get_attribute("content").startswith("noindex")
                        assert page.locator("html").get_attribute("data-gc-candidate") == "not-deployed"
                        assert "Not deployed" in page.locator("main").inner_text()
                        for width in (320, 375, 768, 1280):
                            page.set_viewport_size({"width": width, "height": 900})
                            overflow = page.evaluate("document.documentElement.scrollWidth - innerWidth")
                            assert overflow <= 1, (browser_name, route, width, "overflow", overflow)
                        if route == "/suite/":
                            search = page.get_by_role("searchbox", name="Search Suite products")
                            assert search.count() == 1
                            cards = page.locator("#source-content .candidate-content-card:visible")
                            baseline = cards.count()
                            assert baseline >= 40, (browser_name, "missing Suite inventory")
                            search.fill("Memos")
                            assert 0 < cards.count() < baseline
                            assert "Memos" in cards.first.inner_text()
                            search.fill("unmatched-product-identifier")
                            assert cards.count() == 0
                            assert "0 of " in page.locator("#suite-filter-status").inner_text()
                            search.fill("")
                            assert cards.count() == baseline
                        if route == "/android/":
                            lifecycle = page.get_by_role("navigation", name="Android lifecycle sections")
                            assert lifecycle.locator("a").count() == 4
                            assert page.locator("#planned .candidate-content-card").count() == 4
                            assert page.locator("#active-development .candidate-content-card").count() == 16
                            assert page.locator("#release-candidate .candidate-content-card").count() == 1
                            assert page.locator("#stable .candidate-content-card").count() == 1
                            lifecycle.get_by_role("link", name="Active development").click()
                            assert page.url.endswith("/android/#active-development")
                        if route == "/github/":
                            assert page.locator("#github-live-results .github-repo-card").count() == 0
                            filter_label = page.locator("label[for=github-repo-filter]")
                            assert filter_label.is_hidden()
                            page.evaluate("""() => {
                                window.previewGithubCalls = [];
                                window.fetch = async (url, options) => {
                                    window.previewGithubCalls.push({url, options});
                                    if (!url.startsWith("https://api.github.com/users/GoreeCloud/repos?type=owner")) throw new Error("incorrect GitHub account endpoint");
                                    return new Response(JSON.stringify([
                                      {name:"Memos", full_name:"GoreeCloud/Memos",
                                       owner:{login:"GoreeCloud"}, private:false,
                                       description:"Public repository", language:"Python",
                                       default_branch:"main", archived:false},
                                      {name:"Hidden", full_name:"GoreeCloud/Hidden",
                                       owner:{login:"GoreeCloud"}, private:true}
                                    ]), {status:200, headers:{"Content-Type":"application/json"}});
                                };
                            }""")
                            assert page.evaluate("window.previewGithubCalls.length") == 0
                            page.get_by_role("button", name="Load public repositories").click()
                            cards = page.locator("#github-live-results .github-repo-card")
                            cards.first.wait_for()
                            assert cards.count() == 1
                            assert filter_label.is_visible()
                            assert page.evaluate("window.previewGithubCalls.length") == 1
                            assert cards.first.locator("a").get_attribute("href") == "https://github.com/GoreeCloud/Memos"
                            search = page.get_by_role("searchbox", name="Filter loaded repositories")
                            search.fill("missing")
                            assert cards.count() == 0
                            search.fill("")
                            assert cards.count() == 1
                            page.reload(wait_until="networkidle")
                            page.evaluate("""() => {
                                window.previewGithubCalls = [];
                                window.fetch = async url => {
                                    window.previewGithubCalls.push(url);
                                    if (!url.startsWith("https://api.github.com/users/GoreeCloud/repos?type=owner")) throw new Error("incorrect GitHub account endpoint");
                                    return new Response("{}", {status:429});
                                };
                            }""")
                            retry = page.locator("[data-gc-load-repos]")
                            retry.click()
                            page.wait_for_function("document.getElementById('github-live-status').textContent.includes('limited')")
                            assert retry.is_enabled()
                            assert filter_label.is_hidden()
                            assert page.evaluate("window.previewGithubCalls.length") == 1
                            page.evaluate("""() => {
                                window.previewGithubCalls = [];
                                window.fetch = async url => {
                                    window.previewGithubCalls.push(url);
                                    if (!url.startsWith("https://api.github.com/users/GoreeCloud/repos?type=owner")) throw new Error("incorrect GitHub account endpoint");
                                    const number = new URL(url).searchParams.get('page');
                                    const record = name => ({
                                      name, full_name: "GoreeCloud/" + name,
                                      owner:{login:"GoreeCloud"}, private:false,
                                      description:"Public", language:"Python",
                                      default_branch:"main", archived:false
                                    });
                                    const rows = number === "1"
                                      ? Array.from({length:100}, (_, i) => record("Repo-" + i))
                                      : [record("Memos"), record("Repo-0")];
                                    return new Response(JSON.stringify(rows), {status:200});
                                };
                            }""")
                            retry.click()
                            page.wait_for_function("document.querySelectorAll('#github-live-results .github-repo-card').length === 101")
                            assert page.evaluate("window.previewGithubCalls.length") == 2
                            assert not retry.is_enabled()
                        page.set_viewport_size({"width": 375, "height": 900})
                        page.evaluate("document.documentElement.style.fontSize='200%'")
                        overflow = page.evaluate("document.documentElement.scrollWidth - innerWidth")
                        assert overflow <= 1, (browser_name, route, "200% text overflow", overflow)
                        page.evaluate("document.documentElement.style.removeProperty('font-size')")
                    page.goto(base + "/", wait_until="networkidle")
                    page.get_by_role("button", name="Dark").click()
                    assert page.locator("html").get_attribute("data-gc-mode") == "dark"
                    page.goto(base + "/privacy/", wait_until="networkidle")
                    assert page.locator("html").get_attribute("data-gc-mode") == "dark"
                    page.emulate_media(forced_colors="active", reduced_motion="reduce")
                    assert page.get_by_role("main").count() == 1
                    assert not errors, (browser_name, errors)
                    assert all(url.startswith(base + "/") for url in resources), (browser_name, "unexpected resource origin")
                    results.append({"browser": browser_name, "routes": 11,
                                    "viewportWidths": [320, 375, 768, 1280],
                                    "textScale": 200, "deployed": False, "accepted": False})
                finally:
                    context.close()
                    browser.close()
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=3)
    return results


if __name__ == "__main__":
    print(json.dumps(smoke(), sort_keys=True))
