#!/usr/bin/env python3
"""Add an opt-in, no-network review workbench to the static candidate gallery.

Does not promote candidates to official, edit source assets or change product
catalog statuses. Generated markup remains ordinary HTML and needs no server.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/'site/identity-review/index.html'
CSS=ROOT/'site/assets/site.css'
html=PAGE.read_text()
assert html.count('<div class="identity-review-grid">')==1
assert 'data-review-filter' not in html
assert html.count('data-review-status="candidate"')==7
controls='''<div class="identity-workbench" role="group" aria-label="Identity candidate review controls" data-review-workbench>
  <label class="identity-review-filter-label" for="identity-review-filter">Filter candidate designs
    <select id="identity-review-filter" data-review-filter>
      <option value="all">All seven designs</option>
      <option value="pillars">Privacy, cybersecurity and integration</option>
      <option value="applications">Applications: Maps, Projects and Analytics</option>
      <option value="infrastructure">Infrastructure: Gateway</option>
    </select>
  </label>
  <button class="catalog-tool" type="button" data-review-compare aria-pressed="false">Compare light and dark wordmarks</button>
  <button class="catalog-tool" type="button" data-review-reset>Reset review</button>
  <span class="identity-review-count" data-review-count role="status" aria-live="polite" aria-atomic="true">Showing all 7 proposed designs.</span>
</div>
<div class="identity-review-grid" data-review-grid>'''
html=html.replace('<div class="identity-review-grid">',controls,1)
categories={'goreeshield':'pillars','wardveil':'pillars','mesh':'pillars','maps':'applications',
    'projects':'applications','analytics':'applications','gateway':'infrastructure'}
for slug,cat in categories.items():
    needle='data-review-product="'+slug+'"'
    assert html.count(needle)==1
    html=html.replace(needle,needle+' data-review-category="'+cat+'" id="identity-'+slug+'"',1)
    # Fragment permalink is explicit rather than constructing external/share URLs.
    block_start=html.index('id="identity-'+slug+'"')
    next_source=html.index('<div class="identity-review-source">',block_start)
    html=html[:next_source]+html[next_source:].replace(
      '<div class="identity-review-source">',
      '<div class="identity-review-source">\n      <a class="text-link" href="#identity-'+slug+'">Link to this design</a>',1)
html=html.replace('  <script src="/assets/catalog-tools.js" defer></script>\n',
                  '  <script src="/assets/identity-workbench.js" defer></script>\n',1)
PAGE.write_text(html)
css=CSS.read_text()
assert '/* Identity candidate review workbench' not in css
css+='''

/* Identity candidate review workbench (nontracking, release-isolated). */
.identity-workbench {display:flex;gap:12px 16px;flex-wrap:wrap;align-items:end;
 padding:19px 22px;margin:0 0 24px;background:var(--gc-surface);
 border:1px solid var(--gc-divider);border-radius:var(--radius-lg);}
.identity-review-filter-label {display:flex;flex-direction:column;gap:8px;font-size:13px;font-weight:720;
 color:var(--gc-text-soft);min-width:min(100%,280px);flex:1;}
.identity-review-filter-label select {appearance:auto;min-height:44px;padding:10px 14px;
 border:1px solid var(--gc-outline);border-radius:var(--radius-md);
 background:var(--gc-surface);color:var(--gc-text);font:inherit;}
.identity-review-filter-label select:focus-visible,.identity-workbench button:focus-visible {
 outline:3px solid var(--gc-focus);outline-offset:3px;}
.identity-review-count {font-size:13px;color:var(--gc-text-soft);flex-basis:100%;line-height:1.5;}
.identity-review-card[hidden] {display:none!important;}
.identity-review-card {scroll-margin-top:90px;}
.identity-review-grid[data-review-compare="true"] .identity-review-wordmark {
 display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;padding:0;
 background:transparent!important;border:0;}
.identity-review-grid[data-review-compare="true"] .identity-review-wordmark img {
 display:block!important;width:100%;height:auto;max-height:none;min-height:64px;
 padding:8px;border:1px solid var(--gc-divider);border-radius:12px;object-fit:contain;}
.identity-review-grid[data-review-compare="true"] .review-wordmark-for-light {background:#fff;}
.identity-review-grid[data-review-compare="true"] .review-wordmark-for-dark {background:#15203b;}
@media(max-width:520px){
 .identity-workbench{padding:16px;}
 .identity-workbench button{flex:1;}
 .identity-review-grid[data-review-compare="true"] .identity-review-wordmark {grid-template-columns:1fr;}
}
'''
CSS.write_text(css)
print('Upgraded seven static candidate cards with filter, compare, reset and source permalinks')
