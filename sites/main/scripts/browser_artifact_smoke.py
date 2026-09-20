#!/usr/bin/env python3
"""Exercise the exact built GoreeCloud artifact in headless Chrome."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from build_public_site import DIST

DRIVER_HOST = "127.0.0.1"
DRIVER_PORT = 9517
DRIVER_BASE = f"http://{DRIVER_HOST}:{DRIVER_PORT}"
WEB_HOST = "127.0.0.1"
WEB_PORT = 8770
WEB_BASE = f"http://{WEB_HOST}:{WEB_PORT}"
PAGES = ("/", "/platform-systems/", "/suite/", "/office-suite/", "/firefox/", "/github/")
VIEWPORTS = ((1180, 900), (768, 900), (390, 844), (320, 844))


class BrowserError(RuntimeError):
    pass


def request(method: str, path: str, payload: dict[str, Any] | None = None, timeout: int = 20) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = Request(
        f"{DRIVER_BASE}{path}",
        data=data,
        method=method,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urlopen(req, timeout=timeout) as response:
            raw = response.read()
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise BrowserError(f"WebDriver HTTP {exc.code}: {detail}") from exc
    except (URLError, TimeoutError) as exc:
        raise BrowserError(f"WebDriver request failed: {exc}") from exc
    if not raw:
        return None
    value = json.loads(raw.decode("utf-8")).get("value")
    if isinstance(value, dict) and value.get("error"):
        raise BrowserError(f"{value.get('error')}: {value.get('message', '')}")
    return value


def driver_binary() -> str:
    for candidate in (shutil.which("chromedriver"), "/usr/local/share/chromedriver-linux64/chromedriver"):
        if candidate and Path(candidate).is_file():
            return str(candidate)
    raise BrowserError("chromedriver unavailable")


def wait_for_driver() -> None:
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        try:
            status = request("GET", "/status")
            if isinstance(status, dict) and status.get("ready"):
                return
        except Exception:
            pass
        time.sleep(0.2)
    raise BrowserError("chromedriver did not become ready")


def create_session() -> str:
    value = request("POST", "/session", {
        "capabilities": {"alwaysMatch": {
            "browserName": "chrome",
            "goog:chromeOptions": {"args": [
                "--headless=new", "--no-sandbox", "--disable-dev-shm-usage",
                "--disable-background-networking", "--disable-component-update",
                "--disable-default-apps", "--disable-extensions", "--disable-sync",
                "--no-first-run", "--window-size=1180,900",
            ]},
        }}
    })
    if not isinstance(value, dict) or not value.get("sessionId"):
        raise BrowserError(f"unexpected session response: {value!r}")
    return value["sessionId"]


def execute(session: str, script: str) -> Any:
    return request("POST", f"/session/{session}/execute/sync", {"script": script, "args": []})


def set_viewport(session: str, width: int, height: int) -> None:
    request("POST", f"/session/{session}/goog/cdp/execute", {
        "cmd": "Emulation.setDeviceMetricsOverride",
        "params": {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": False},
    })


def validate_page(session: str, path: str, width: int, height: int) -> None:
    request("POST", f"/session/{session}/url", {"url": WEB_BASE + path})
    set_viewport(session, width, height)
    state = execute(session, """
      const h1=document.querySelector('h1');
      const header=document.querySelector('.site-header');
      const nav=document.querySelector('[data-nav]');
      return {
        ready:document.readyState,
        width:window.innerWidth,
        height:window.innerHeight,
        scrollWidth:document.documentElement.scrollWidth,
        h1Count:document.querySelectorAll('h1').length,
        h1Text:(h1?.textContent||'').trim(),
        headerHeight:header?.getBoundingClientRect().height||0,
        navDisplay:nav?getComputedStyle(nav).display:'',
        bodyText:(document.body?.innerText||'').trim().length,
      };
    """)
    if not isinstance(state, dict):
        raise BrowserError(f"could not read state for {path}")
    if state.get("ready") != "complete":
        raise BrowserError(f"{path} did not finish loading")
    if abs(int(state.get("width", 0)) - width) > 1 or abs(int(state.get("height", 0)) - height) > 1:
        raise BrowserError(f"{path} viewport mismatch: {state}")
    if int(state.get("scrollWidth", width + 2)) > width + 1:
        raise BrowserError(f"{path} overflows horizontally at {width}px: {state}")
    if int(state.get("h1Count", 0)) != 1 or not state.get("h1Text"):
        raise BrowserError(f"{path} must render exactly one visible h1: {state}")
    if int(state.get("bodyText", 0)) < 80:
        raise BrowserError(f"{path} rendered unexpectedly little content: {state}")

    if width <= 900:
        nav_state = execute(session, """
          const button=document.querySelector('[data-nav-toggle]');
          const nav=document.querySelector('[data-nav]');
          if(button && button.getAttribute('aria-expanded')!=='true') button.click();
          const r=nav?.getBoundingClientRect();
          const links=[...document.querySelectorAll('[data-nav] a')].map(a=>a.getBoundingClientRect()).filter(r=>r.width&&r.height);
          return {
            expanded:button?.getAttribute('aria-expanded'),
            display:nav?getComputedStyle(nav).display:'',
            left:r?.left||0,right:r?.right||0,
            minHeight:links.length?Math.min(...links.map(r=>r.height)):0,
          };
        """)
        if nav_state.get("expanded") != "true" or nav_state.get("display") == "none":
            raise BrowserError(f"{path} mobile navigation did not open: {nav_state}")
        if float(nav_state.get("left", -2)) < -1 or float(nav_state.get("right", width + 2)) > width + 1:
            raise BrowserError(f"{path} mobile navigation overflows viewport: {nav_state}")
        if float(nav_state.get("minHeight", 0)) < 43.5:
            raise BrowserError(f"{path} mobile navigation target below 44px: {nav_state}")


def main() -> int:
    if not DIST.is_dir() or not (DIST / "index.html").is_file():
        print("Browser smoke failed: build artifact missing; run build_public_site.py first.")
        return 1

    web: subprocess.Popen[bytes] | None = None
    driver: subprocess.Popen[bytes] | None = None
    session: str | None = None
    log_path: Path | None = None
    try:
        web = subprocess.Popen(
            ["python3", "-m", "http.server", str(WEB_PORT), "--bind", WEB_HOST, "--directory", str(DIST)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            try:
                with urlopen(WEB_BASE + "/", timeout=1) as response:
                    if response.status == 200:
                        break
            except Exception:
                time.sleep(0.1)
        else:
            raise BrowserError("local artifact server did not become ready")

        with tempfile.NamedTemporaryFile(prefix="goreecloud-browser-", suffix=".log", delete=False) as log:
            log_path = Path(log.name)
            driver = subprocess.Popen(
                [driver_binary(), f"--port={DRIVER_PORT}", "--allowed-ips=127.0.0.1"],
                stdout=log, stderr=subprocess.STDOUT,
            )
        wait_for_driver()
        session = create_session()
        request("POST", f"/session/{session}/timeouts", {"implicit": 0, "pageLoad": 15000, "script": 10000})

        for width, height in VIEWPORTS:
            for path in PAGES:
                validate_page(session, path, width, height)

        print("Browser smoke passed for all six canonical pages at desktop, tablet, and mobile viewports.")
        return 0
    except Exception as exc:
        print(f"Browser smoke failed: {exc}")
        if log_path and log_path.is_file():
            log = log_path.read_text(encoding="utf-8", errors="replace")
            if log:
                print(log[-5000:])
        return 1
    finally:
        if session:
            try:
                request("DELETE", f"/session/{session}")
            except Exception:
                pass
        for proc in (driver, web):
            if proc:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)
        if log_path:
            try:
                log_path.unlink()
            except OSError:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
