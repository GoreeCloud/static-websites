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
