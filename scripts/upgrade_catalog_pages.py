#!/usr/bin/env python3
"""Idempotent, preview-only catalog controls; existing public copy is untouched."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "products/index.html": ('data-results-count>12 projects shown</p>', 'products'),
    "github/index.html": ('data-repo-count>55 repositories shown</p>', 'github'),
    "suite/index.html": ('data-suite-count>45 names shown across 9 groups</p>', 'suite'),
}
CONTROLS = """<div class="catalog-tools" data-catalog-actions="{name}" role="group" aria-label="Directory sharing and filter actions">
  <button type="button" class="catalog-tool" data-catalog-share>Copy filtered link</button>
  <button type="button" class="catalog-tool" data-catalog-reset>Reset filters</button>
  <span class="catalog-tool-status" data-catalog-status role="status" aria-live="polite" aria-atomic="true"></span>
  <output class="catalog-tool-link" data-catalog-link hidden aria-label="Shareable directory link"></output>
</div>"""
for relative, (marker, name) in PAGES.items():
    p = ROOT / "site" / relative
    body = p.read_text(encoding="utf-8")
    if 'data-catalog-actions=' in body:
        raise SystemExit(f"Already modified: {relative}")
    assert body.count(marker) == 1, (relative, "missing result-count marker")
    assert body.count('<script src="/assets/site.js" defer></script>') == 1
    replacement = marker + CONTROLS.format(name=name)
    body = body.replace(marker, replacement, 1)
    body = body.replace('<script src="/assets/site.js" defer></script>',
        '<script src="/assets/site.js" defer></script>\n'
        '  <script src="/assets/catalog-tools.js" defer></script>', 1)
    p.write_text(body, encoding="utf-8")
    print(f"Expanded catalog {relative}: share/reset and accessible live feedback")

css_path = ROOT / "site/assets/site.css"
css = css_path.read_text(encoding="utf-8")
if "/* Catalog action controls — nontracking shareable views */" in css:
    raise SystemExit("Catalog styles already present")
css += """

/* Catalog action controls — nontracking shareable views */
.catalog-tools { display:flex; flex-wrap:wrap; align-items:center; gap:10px; margin: 12px 0 24px; }
.catalog-tool { min-height:44px; min-width:120px; padding:10px 17px; font-size:14px;
  border:1px solid var(--gc-outline); border-radius:var(--radius-md);
  background:var(--gc-surface); color:var(--gc-text); font-weight:650; }
.catalog-tool:hover { background:var(--gc-surface-tonal); }
.catalog-tool:focus-visible { outline:3px solid var(--gc-focus); outline-offset:3px; }
.catalog-tool-status { color:var(--gc-text-soft); font-size:14px; line-height:1.6; }
.catalog-tool-link { flex-basis:100%; display:block; font-size:14px; line-height:1.6;
  overflow-wrap:anywhere; padding:13px 16px; border:1px solid var(--gc-divider);
  border-radius:var(--radius-md); background:var(--gc-surface); user-select:text; }
.catalog-tool-link[hidden] { display:none; }
@media (max-width:480px) {
  .catalog-tool { flex:1; }
  .catalog-tool-status { flex-basis:100%; }
}
"""
css_path.write_text(css, encoding="utf-8")
