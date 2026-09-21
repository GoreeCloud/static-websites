#!/usr/bin/env python3
"""Build the allowlisted artifact for GoreeCloud's one retained public website."""

from __future__ import annotations

from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

PUBLIC_FILES = (
    ".well-known/security.txt",
    "404.html",
    "_headers",
    "_redirects",
    "assets/social-preview.png",
    "assets/social/instagram.ico",
    "assets/social/threads.ico",
    "assets/social/tiktok.ico",
    "assets/social/x.ico",
    "assets/social/reddit.ico",
    "assets/social/pinterest.ico",
    "css/site-v9.css",
    "contact/index.html",
    "firefox/index.html",
    "github/index.html",
    "googlea0a636fd5dafd9e0.html",
    "index.html",
    "js/site-v8.js",
    "js/theme-init-v8.js",
    "office-suite/index.html",
    "platform-systems/index.html",
    "privacy.html",
    "repositories.html",
    "robots.txt",
    "security.html",
    "site.webmanifest",
    "sitemap.xml",
    "suite/index.html",
    "assets/brand/goreecloud-logo.svg",
    "assets/brand/goreecloud-wordmark.svg",
    "assets/firefox/advanced-tab-manager.svg",
    "assets/firefox/redirector.svg",
    "assets/firefox/source-resync.svg",
    "assets/firefox/webspaces.svg",
    "assets/products/ai.svg",
    "assets/products/app-store.svg",
    "assets/products/backup.svg",
    "assets/products/bookmarks.svg",
    "assets/products/browser.svg",
    "assets/products/calendar.svg",
    "assets/products/changelogs.svg",
    "assets/products/code.svg",
    "assets/products/contacts.svg",
    "assets/products/dns.svg",
    "assets/products/documents.svg",
    "assets/products/download-manager-extension.svg",
    "assets/products/drive.svg",
    "assets/products/feed.svg",
    "assets/products/file-manager.svg",
    "assets/products/forms.svg",
    "assets/products/gallery.svg",
    "assets/products/gateway.svg",
    "assets/products/health.svg",
    "assets/products/home.svg",
    "assets/products/home-security.svg",
    "assets/products/identity.svg",
    "assets/products/index.svg",
    "assets/products/keyboard.svg",
    "assets/products/launcher.svg",
    "assets/products/location.svg",
    "assets/products/mail.svg",
    "assets/products/manager.svg",
    "assets/products/maps.svg",
    "assets/products/memos.svg",
    "assets/products/messenger.svg",
    "assets/products/monitor.svg",
    "assets/products/music.svg",
    "assets/products/network.svg",
    "assets/products/notes.svg",
    "assets/products/notify.svg",
    "assets/products/office.svg",
    "assets/products/photos.svg",
    "assets/products/presentations.svg",
    "assets/products/reader.svg",
    "assets/products/router-os.svg",
    "assets/products/search.svg",
    "assets/products/social.svg",
    "assets/products/spreadsheet.svg",
    "assets/products/sync.svg",
    "assets/products/tasks.svg",
    "assets/products/terminal.svg",
    "assets/products/vault.svg",
    "assets/products/video.svg",
    "assets/products/website.svg",
    "assets/products/writer.svg",
    "assets/systems/everkeep.svg",
    "assets/systems/glaze-ui.svg",
    "assets/systems/mesh.svg",
    "assets/systems/observability.svg",
    "assets/systems/policy.svg",
    "assets/systems/privacy-shield.svg",
    "assets/systems/wardveil-security.svg",
    "assets/wallpapers/graphite.svg",
    "assets/wallpapers/living-glaze.svg",
    "assets/wallpapers/mesh.svg",
    "assets/wallpapers/pearl.svg",
)


def fail(message: str) -> int:
    print(f"Public-site build failed: {message}")
    return 1


def main() -> int:
    if len(PUBLIC_FILES) != len(set(PUBLIC_FILES)):
        return fail("public allowlist contains duplicate paths")

    try:
        for relative in PUBLIC_FILES:
            source = ROOT / relative
            if not source.is_file():
                return fail(f"required public source is missing: {relative}")
            if source.is_symlink():
                return fail(f"public source must not be a symlink: {relative}")

        if DIST.exists():
            if DIST.is_symlink():
                return fail("dist must not be a symlink")
            shutil.rmtree(DIST)
        DIST.mkdir()

        for relative in PUBLIC_FILES:
            source = ROOT / relative
            destination = DIST / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

        for path in DIST.rglob("*"):
            if path.is_symlink():
                return fail(f"artifact contains a symlink: {path.relative_to(DIST)}")

    except OSError as exc:
        return fail(str(exc))

    file_count = sum(path.is_file() for path in DIST.rglob("*"))
    total_bytes = sum(path.stat().st_size for path in DIST.rglob("*") if path.is_file())
    print(f"Built GoreeCloud retained-site artifact: {file_count} files, {total_bytes} bytes -> dist/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
