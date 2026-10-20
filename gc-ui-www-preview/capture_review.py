#!/usr/bin/env python3
"""Private CI-only visual review package for the isolated eleven-route GC UI candidate."""
from functools import partial
from hashlib import sha256
from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json
import os

from playwright.sync_api import sync_playwright
from build_routes import OUT, PATHS
from test_routes import verify
from audit_source import audit as audit_content_gaps

REVIEW = OUT.parent / "dist-gc-ui-review"
WIDTHS = (("desktop", 1280), ("mobile", 375))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def capture():
    verify(OUT)
    if REVIEW.is_symlink():
        raise ValueError("unsafe review output")
    REVIEW.mkdir(exist_ok=True)
    images = REVIEW / "screenshots"
    if images.is_symlink():
        raise ValueError("unsafe screenshot output")
    images.mkdir(exist_ok=True)
    for prior in images.glob("*.png"):
        prior.unlink()
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(OUT)))
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    base = f"http://127.0.0.1:{server.server_port}"
    records = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                context = browser.new_context(reduced_motion="reduce", color_scheme="light")
                page = context.new_page()
                external = []
                page.on("request", lambda request:
                        external.append(request.url)
                        if not request.url.startswith(base + "/") else None)
                for ident, route in PATHS.items():
                    for screen, width in WIDTHS:
                        page.set_viewport_size({"width": width, "height": 900})
                        response = page.goto(base + route, wait_until="networkidle")
                        if not response or response.status != 200:
                            raise RuntimeError("preview route not served: " + route)
                        if page.locator('html[data-gc-candidate="not-deployed"]').count() != 1:
                            raise RuntimeError("missing undeployed banner on " + route)
                        if page.evaluate("document.documentElement.scrollWidth > innerWidth + 1"):
                            raise RuntimeError("horizontal overflow: " + route)
                        filename = f"{ident}-{screen}.png"
                        output = images / filename
                        page.screenshot(path=str(output), full_page=True,
                                        animations="disabled")
                        records.append({"route": route, "width": width,
                                        "image": "screenshots/" + filename,
                                        "sha256": sha256(output.read_bytes()).hexdigest()})
                        if ident == "design":
                            page.get_by_role("button", name="Dark", exact=True).click()
                            assert page.locator("html").get_attribute("data-gc-mode") == "dark"
                            dark_name = f"{ident}-{screen}-dark.png"
                            dark_output = images / dark_name
                            page.screenshot(path=str(dark_output), full_page=True,
                                            animations="disabled")
                            records.append({"route": route, "width": width,
                                            "mode": "dark", "image": "screenshots/" + dark_name,
                                            "sha256": sha256(dark_output.read_bytes()).hexdigest()})
                            page.get_by_role("button", name="Light", exact=True).click()
                if external:
                    raise RuntimeError("review unexpectedly requested an external origin")
                context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=3)
    head = os.environ.get("SOURCE_SHA", "local-checkout")
    manifest = {"schema": "gc-ui-www-visual-review.v1", "sourceHead": head,
                "deployed": False, "consumerAccepted": False,
                "noExternalRequests": True, "captures": records}
    (REVIEW / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (REVIEW / "content-seo-gap-audit.json").write_text(
        json.dumps(audit_content_gaps(), indent=2) + "\n", encoding="utf-8")
    sections = "".join(
        '<article><h2>' + escape(row["route"]) + " — " +
        ("Desktop" if row["width"] == 1280 else "Mobile") + (" — Dark" if row.get("mode") == "dark" else " — Light") +
        '</h2><img loading="lazy" src="' + escape(row["image"], quote=True) +
        '" alt="Isolated, undeployed GC UI route at ' + str(row["width"]) +
        ' pixels"></article>' for row in records)
    gallery = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
               '<meta name="viewport" content="width=device-width,initial-scale=1">'
               '<meta name="robots" content="noindex,nofollow"><title>GC UI visual review</title>'
               '<style>body{font:16px system-ui;max-width:1250px;margin:auto;padding:20px}'
               'article{padding:16px 0;border-bottom:1px solid #777}'
               'img{display:block;width:100%;height:auto;border:1px solid #aaa}'
               'h1,h2{line-height:1.2}</style></head><body>'
               '<h1>GoreeCloud GC UI — isolated review only</h1>'
               '<p><strong>Not deployed.</strong> Images of all eleven routes at '
               '1280px and 375px. These are visual references, not proof of '
               'content parity, accessibility or publication.</p>'
               + sections + '</body></html>')
    (REVIEW / "index.html").write_text(gallery)
    (REVIEW / "README.txt").write_text(
        "GC UI isolated visual review — NOT DEPLOYED OR ACCEPTED\n"
        "Open index.html locally for the 24 screenshots.\n"
        "The separate dist-gc-ui-routes-preview/ folder contains the HTML.\n"
        "To browse that site locally, from its parent directory run:\n"
        "  python3 -m http.server 4173 --directory dist-gc-ui-routes-preview\n"
        "Then visit http://127.0.0.1:4173/ . Never point it at production.\n"
        "Manifest: manifest.json. Content/SEO gaps: content-seo-gap-audit.json.\n")
    return manifest


if __name__ == "__main__":
    info = capture()
    print(json.dumps({"sourceHead": info["sourceHead"],
                      "screenCaptures": len(info["captures"]),
                      "deployed": False}, sort_keys=True))
