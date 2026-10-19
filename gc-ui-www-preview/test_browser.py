#!/usr/bin/env python3
"""Real-browser, localhost-only GC UI www /design/ preview smoke, never production."""
from __future__ import annotations
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import json

from playwright.sync_api import sync_playwright
from build import OUT
from validate import validate


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def smoke() -> list[dict]:
    validate(OUT, built=True)
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(OUT)))
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    address = f"http://127.0.0.1:{server.server_port}"
    result = []
    try:
        with sync_playwright() as pw:
            for browser_name in ("chromium", "firefox"):
                browser = getattr(pw, browser_name).launch(headless=True)
                context = browser.new_context(
                    viewport={"width": 1280, "height": 900},
                    reduced_motion="reduce")
                page = context.new_page()
                visited = []
                page.on("request", lambda request: visited.append(request.url))
                try:
                    response = page.goto(address + "/index.html", wait_until="networkidle")
                    assert response and response.status == 200, browser_name + ": no home"
                    assert "GoreeCloud UI" in page.title()
                    assert page.locator('meta[name="robots"]').get_attribute("content").startswith("noindex")
                    assert page.get_by_role("main").count() == 1
                    assert page.get_by_role("navigation", name="Preview navigation").count() == 1
                    assert page.get_by_role("heading", level=1).count() == 1
                    assert page.locator("[data-mode]").count() == 3
                    assert page.locator("html").get_attribute("data-gc-preview") == "www-design-undeployed"
                    assert "Integral Platform System 05 / 09" in page.locator("body").inner_text()

                    page.keyboard.press("Tab")
                    assert page.evaluate("document.activeElement.classList.contains('skip')"), browser_name + ": skip"
                    page.keyboard.press("Enter")
                    assert page.evaluate("document.activeElement.id") == "main", browser_name + ": skip target"

                    page.get_by_role("button", name="Dark").click()
                    assert page.locator("html").get_attribute("data-gc-mode") == "dark"
                    assert page.get_by_role("button", name="Dark").get_attribute("aria-pressed") == "true"
                    page.reload(wait_until="networkidle")
                    assert page.locator("html").get_attribute("data-gc-mode") == "dark", browser_name + ": mode persistence"
                    page.get_by_role("button", name="Light").click()
                    assert page.locator("html").get_attribute("data-gc-mode") == "light"
                    page.emulate_media(color_scheme="dark")
                    page.get_by_role("button", name="System").click()
                    assert page.locator("html").get_attribute("data-gc-mode") == "dark", browser_name + ": system dark"

                    # Selected semantic pairs only: not full accessibility certification.
                    ratios = []
                    for mode in ("Light", "Dark"):
                        page.get_by_role("button", name=mode).click()
                        checks = page.evaluate("""() => {
                            const root = getComputedStyle(document.documentElement);
                            const linear = v => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4;
                            const value = name => {
                                const raw = root.getPropertyValue(name).trim();
                                const hex = /^#[0-9a-f]{3}$/i.test(raw) ?
                                    '#' + [...raw.slice(1)].map(c => c + c).join('') : raw;
                                if (!/^#[0-9a-f]{6}$/i.test(hex)) throw Error('invalid semantic role ' + name + '=' + raw);
                                const rgb = [1,3,5].map(i => linear(parseInt(hex.slice(i,i+2),16)/255));
                                return .2126 * rgb[0] + .7152 * rgb[1] + .0722 * rgb[2];
                            };
                            const pair = (fg,bg) => {
                                const a=value(fg),b=value(bg);
                                return (Math.max(a,b)+.05)/(Math.min(a,b)+.05);
                            };
                            return {
                              canvas:pair('--gc-v1-color-on-canvas','--gc-v1-color-canvas'),
                              primary:pair('--gc-v1-color-on-primary','--gc-v1-color-primary'),
                              muted:pair('--gc-v1-color-on-surface-muted','--gc-v1-color-surface-raised')
                            };
                        }""")
                        assert all(v >= 4.5 for v in checks.values()), (browser_name, mode, checks)
                        ratios.extend(checks.values())

                    # Full document reflow at narrow viewport, plus text-size stress.
                    for width in (320, 375, 768, 1280):
                        page.set_viewport_size({"width": width, "height": 900})
                        overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                        assert overflow <= 1, f"{browser_name}: {width}px viewport overflow {overflow}"
                    for scale, width in ((2, 375), (4, 320)):
                        page.set_viewport_size({"width": width, "height": 900})
                        page.evaluate("(s) => document.documentElement.style.fontSize = s", f"{scale*100}%")
                        overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                        if overflow > 1:
                            nodes = page.evaluate("""() => [...document.querySelectorAll('body *')]
                                .map(e => {let r=e.getBoundingClientRect();
                                    return {tag:e.tagName,cls:String(e.className).slice(0,70),
                                        right:Math.round(r.right),scroll:e.scrollWidth,client:e.clientWidth};})
                                .filter(e => e.right > innerWidth+1 || e.scroll > e.client+1)
                                .sort((a,b) => b.right-a.right).slice(0,8)""")
                            raise AssertionError(
                                f"{browser_name}: {scale*100}% text at {width}px overflow {overflow}px: {nodes}")
                        page.evaluate("document.documentElement.style.removeProperty('font-size')")
                    page.emulate_media(forced_colors="active", reduced_motion="reduce")
                    assert page.locator("main").count() == 1
                    assert all(url.startswith(address+"/") for url in visited), browser_name + ": external runtime request"
                    result.append({"browser": browser_name, "minimumSelectedContrast": round(min(ratios),2),
                                   "viewports": [320,375,768,1280], "textSizeProbes": [200,400],
                                   "deployed": False, "accepted": False})
                finally:
                    context.close()
                    browser.close()
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=3)
    return result


if __name__ == "__main__":
    print(json.dumps(smoke(), sort_keys=True))
