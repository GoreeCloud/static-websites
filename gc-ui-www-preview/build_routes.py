#!/usr/bin/env python3
"""Build an isolated GC UI candidate for all 11 retained public URL paths.

This builder NEVER reads or writes the production sites/main/dist tree.
It is not a deployment mechanism or production-parity certification.
"""
from __future__ import annotations

from hashlib import sha256
from html import escape
from pathlib import Path
import json
import shutil
import sys

from build import SOURCE, REPOSITORY
from source_cards import extract, render
from public_links import render_links
from validate import validate as validate_foundations

NAMESPACE = REPOSITORY / "sites/url-namespace.json"
OUT = REPOSITORY / "dist-gc-ui-routes-preview"
FILES = ("gc-ui-foundations.css", "site.css", "site.js", "routes.css", "github-catalog.js")
PAGES = {
    "home": ("GoreeCloud", "Software and systems under your control.",
             "GoreeCloud develops privacy-first, self-hosted software for people who want control of their digital lives."),
    "platform-systems": ("Integral Platform Systems", "Nine shared systems. Nine distinct authorities.",
             "Manager, Privacy Shield, Wardveil Security, Everkeep, GoreeCloud UI, Mesh, Identity, Policy and Observability each retain their designated role."),
    "suite": ("GoreeCloud Suite", "Focused products. One connected ecosystem.",
             "The Suite connects independently governed GoreeCloud applications without turning an interface into a source of permissions."),
    "android": ("GoreeCloud Android", "GoreeCloud applications for Android.",
             "Android clients and platform work follow their individual development, verification, and release lifecycles."),
    "office-suite": ("GoreeCloud Office Suite", "A cohesive family of office tools.",
             "The Office Suite brings together document and productivity experiences with transparent feature and release boundaries."),
    "firefox": ("Firefox", "Browser tools with clear boundaries.",
             "GoreeCloud's browser integrations retain independent permission, privacy, compatibility, and release requirements."),
    "github": ("GitHub repositories", "Source you can review.",
             "GoreeCloud maintains publicly visible repositories and provider-native project records under its GitHub user account."),
    "contact": ("Contact GoreeCloud", "Get in touch through verified channels.",
             "The official GoreeCloud repository and existing published contact information remain the authoritative routes for project communication."),
    "design": ("GoreeCloud UI", "One coherent experience, distinct platform authorities.",
             "GC UI is Integral Platform System five of nine. Foundations 1.0.1 has narrowly scoped stable support; broader consumer migration is not accepted."),
    "security": ("Wardveil Security", "Security with visible authority and evidence.",
             "Wardveil owns the security domain; the shared design system supplies presentation and interaction, not security decisions."),
    "privacy": ("Privacy Shield", "Privacy authority stays with the operation.",
             "Privacy Shield owns consent and privacy-control boundaries. An interface alone cannot grant or infer authorization."),
}
PATHS = {
    "home": "/", "platform-systems": "/platform-systems/", "suite": "/suite/",
    "android": "/android/", "office-suite": "/office-suite/", "firefox": "/firefox/",
    "github": "/github/", "contact": "/contact/", "design": "/design/",
    "security": "/security/", "privacy": "/privacy/"
}


def _namespace() -> list[dict]:
    payload = json.loads(NAMESPACE.read_text(encoding="utf-8"))
    if (payload.get("canonical_origin") != "https://www.goreecloud.com"
            or payload.get("state") != "single-retained-website"
            or payload.get("website", {}).get("source_path") != "sites/main"):
        raise ValueError("current single-website authority changed")
    entries = payload.get("canonical_paths")
    if not isinstance(entries, list) or len(entries) != len(PATHS):
        raise ValueError("unexpected canonical route count")
    found = {}
    for entry in entries:
        ident, path, src = entry.get("id"), entry.get("path"), entry.get("source")
        if ident not in PATHS or path != PATHS[ident] or ident in found:
            raise ValueError("unknown or duplicated public URL path")
        if src != ("sites/main/index.html" if ident == "home" else "sites/main/" + ident + "/index.html"):
            raise ValueError("changed authoritative route source")
        origin = REPOSITORY / src
        if origin.is_symlink() or not origin.is_file():
            raise ValueError("missing retained source for " + ident)
        found[ident] = entry
    if set(found) != set(PATHS):
        raise ValueError("missing canonical route")
    return [found[ident] for ident in PATHS]


def _html(ident: str, path: str) -> str:
    title, heading, summary = PAGES[ident]
    source = REPOSITORY / ("sites/main/index.html" if ident == "home" else "sites/main/" + ident + "/index.html")
    public_cards = extract(source, ident)
    if len(public_cards) < 3:
        raise ValueError("missing reviewed public-source cards")
    public_section = render(public_cards) + render_links(source)
    suite_filter = ('''<div class="shell suite-search" role="search">
      <label for="suite-filter">Search Suite products</label>
      <input id="suite-filter" type="search" data-suite-filter
             aria-controls="source-content" autocomplete="off">
      <output id="suite-filter-status" role="status" aria-live="polite"></output>
    </div>''' if ident == "suite" else "")
    github_catalog = ('''<section class="section" id="github-catalog" aria-labelledby="github-catalog-title">
      <h2 id="github-catalog-title">Public GitHub repositories on demand</h2>
      <p class="section-lead">Privacy notice: loading this directory contacts GitHub directly
        from your browser. No GitHub request is sent until you activate the button.</p>
      <button class="primary-action" type="button" data-gc-load-repos
        aria-controls="github-live-results" aria-describedby="github-live-status">Load public repositories</button>
      <p id="github-live-status" role="status" aria-live="polite">Not loaded. Choose the button to connect to GitHub.</p>
      <label class="gc-repo-filter-label" for="github-repo-filter" hidden>Filter loaded repositories</label>
      <input id="github-repo-filter" type="search" data-gc-repo-filter hidden aria-describedby="github-live-status"
             placeholder="Filter by name, description or language">
      <div id="github-live-results" class="route-grid" aria-live="off"></div>
      <p><a href="https://github.com/GoreeCloud">View the GoreeCloud GitHub organization</a></p>
    </section>''' if ident == "github" else "")
    asset = "assets/" if path == "/" else "../assets/"
    navigation = "\n".join(
        '<a href="' + href + '"' + (' aria-current="page"' if key == ident else '') + '>'
        + escape(PAGES[key][0]) + "</a>"
        for key, href in PATHS.items()
    )
    return f'''<!doctype html>
<html lang="en" data-gc-mode="light" data-gc-candidate="not-deployed">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="noindex,nofollow,noarchive">
  <meta name="referrer" content="no-referrer">
  <meta name="color-scheme" content="light dark">
  <meta name="description" content="Isolated GC UI candidate for GoreeCloud's {escape(title, quote=True)} section. Not deployed or accepted.">
  <title>{escape(title)} — GC UI isolated candidate</title>
  <link rel="stylesheet" href="{asset}gc-ui-foundations.css">
  <link rel="stylesheet" href="{asset}site.css">
  <link rel="stylesheet" href="{asset}routes.css">
  <script defer src="{asset}site.js"></script>
  {'<script defer src="' + asset + 'github-catalog.js"></script>' if ident == "github" else ""}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="header">
  <div class="shell header-content candidate-header">
    <a class="candidate-brand" href="/" aria-label="GoreeCloud candidate home">GoreeCloud <span>UI candidate</span></a>
    <fieldset class="appearance"><legend>Appearance</legend>
      <button type="button" data-mode="system" aria-pressed="true">System</button>
      <button type="button" data-mode="light" aria-pressed="false">Light</button>
      <button type="button" data-mode="dark" aria-pressed="false">Dark</button>
    </fieldset>
  </div>
  <nav class="shell candidate-nav" aria-label="Retained website routes">
    {navigation}
  </nav>
</header>
<main class="shell" id="main" tabindex="-1">
  <section class="hero" aria-labelledby="page-title">
    <p class="eyebrow">GoreeCloud / Original GC UI candidate / {escape(path)}</p>
    <h1 id="page-title">{escape(heading)}</h1>
    <p class="intro">{escape(summary)}</p>
    <p class="notice"><strong>Not deployed.</strong> This is a structure and design preview for an existing public URL, not a replacement of the current site. Feature parity, security, accessibility, and rollback acceptance remain pending.</p>
    <p><a class="primary-action" href="#overview">Explore this section</a></p>
  </section>
  <section class="section" id="overview" aria-labelledby="overview-title">
    <p class="eyebrow">One current website / eleven preserved routes</p>
    <h2 id="overview-title">{escape(title)}</h2>
    <div class="route-grid">
      <article class="panel"><h3>Scope</h3><p>{escape(summary)}</p></article>
      <article class="panel"><h3>Design authority</h3><p>Original GoreeCloud UI components and semantic Foundations 1.0.1 tokens. No predecessor design-system dependency is included.</p></article>
      <article class="panel"><h3>Release boundary</h3><p>All existing URLs are retained in the candidate. Live content parity, browser accessibility, and production cutover still require independent review.</p></article>
    </div>
  </section>
  {suite_filter}
  {github_catalog}
  {public_section}
  <section class="section" id="source" aria-labelledby="source-title">
    <p class="eyebrow">Transparent provenance</p>
    <h2 id="source-title">Track source and migration</h2>
    <p class="section-lead">GC UI is Integral Platform System 5 of 9. Source maturity does not imply accepted deployments or production runtime behavior.</p>
    <p><a href="https://github.com/GoreeCloud/gc-ui">GoreeCloud UI source</a> ·
       <a href="https://github.com/GoreeCloud/static-websites/issues/144">Website migration issue</a> ·
       <a href="https://www.goreecloud.com{path}">Current public page (separate production site)</a></p>
  </section>
</main>
<footer class="footer"><div class="shell footer-content">
  <span>GC UI original design candidate · Not deployed</span>
  <a href="/">Candidate home</a>
  <a href="https://www.goreecloud.com/">Current public website</a>
</div></footer>
</body></html>
'''


def build():
    validate_foundations(SOURCE)
    entries = _namespace()
    if OUT.is_symlink() or OUT.resolve() != REPOSITORY.joinpath("dist-gc-ui-routes-preview").resolve():
        raise ValueError("unsafe candidate output")
    if OUT.exists():
        if not OUT.is_dir():
            raise ValueError("candidate output is not a directory")
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "assets").mkdir()
    digests = {}
    source_digests = {}
    for entry in entries:
        page = REPOSITORY / entry["source"]
        source_digests[entry["source"]] = sha256(page.read_bytes()).hexdigest()
    for name in FILES:
        origin = SOURCE / name
        if origin.is_symlink() or not origin.is_file():
            raise ValueError("missing or unsafe reviewed asset: " + name)
        raw = origin.read_bytes()
        if not raw or len(raw) > 1000000 or b"\x00" in raw:
            raise ValueError("invalid candidate asset: " + name)
        if name != "gc-ui-foundations.css" and b"glaze" in raw.lower():
            raise ValueError("retired design dependency")
        destination = OUT / "assets" / name
        destination.write_bytes(raw)
        digests[destination.relative_to(OUT).as_posix()] = sha256(raw).hexdigest()
    for entry in entries:
        relative = Path("index.html") if entry["path"] == "/" else Path(entry["id"]) / "index.html"
        destination = OUT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        raw = _html(entry["id"], entry["path"]).encode("utf-8")
        if b"glaze" in raw.lower():
            raise ValueError("retired design name found")
        destination.write_bytes(raw)
        digests[relative.as_posix()] = sha256(raw).hexdigest()
    report = {
        "schema": "gc-ui-www-routes-isolated-candidate.v1",
        "canonicalWebsite": "https://www.goreecloud.com",
        "publicSiteChanged": False,
        "deployed": False,
        "productionAccepted": False,
        "contentParityAccepted": False,
        "a11yBrowserAccepted": False,
        "routes": [entry["path"] for entry in entries],
        "files": dict(sorted(digests.items())),
        "sourceSha256": dict(sorted(source_digests.items())),
    }
    (OUT / "SHA256SUMS.json").write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    try:
        print(json.dumps(build(), sort_keys=True))
    except (ValueError, OSError, KeyError, UnicodeError) as error:
        print("GC UI route candidate build refused: " + str(error), file=sys.stderr)
        sys.exit(1)
