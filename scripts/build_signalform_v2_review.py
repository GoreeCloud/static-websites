#!/usr/bin/env python3
"""Build an isolated static before/after identity review from pinned first-party source.

No image service or network requests; never replaces an existing approved
master or current public Products icons. Fail closed on unexpected source.
"""
from __future__ import annotations

from pathlib import Path
import html
import hashlib
import json
import os

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
SOURCE_DIR=os.environ.get('GOREECLOUD_BRAND_ASSETS_DIR')
if not SOURCE_DIR:
    raise SystemExit('Set GOREECLOUD_BRAND_ASSETS_DIR to a verified local source checkout')
SOURCE=Path(SOURCE_DIR)
SOURCE_SHA='0807d8719b13858394ba62637629c85d314bdf7a'
PRODUCTS=[
 ('goreeshield','GoreeShield','PRIVACY','Quiet Aperture','Consent and privacy shutters, not a security shield.'),
 ('wardveil','Wardveil','CYBERSECURITY','Sentinel Sweep','Radar and detection trace, not a privacy control.'),
 ('mesh','GoreeCloud Mesh','INTEGRATION','Interlock','Deliberately crossing pathways, not an unrestricted hub.'),
 ('maps','GoreeCloud Maps','WAYFINDING','Wayfinding Loop','Route and compass destination, not a generic folded map.'),
 ('projects','GoreeCloud Projects','PLANNING','Milestone Ladder','Independent progress stages, not a dashboard screenshot.'),
 ('analytics','GoreeCloud Analytics','INSIGHTS','Insight Horizon','A sampled insight trajectory, not a generic bar chart.'),
 ('gateway','GoreeCloud Gateway','NETWORK EDGE','One-Way Passage','A clear routed passage rather than conflicting inward arrows.')
]
FLAT=['app-icon.svg','symbol.svg','logo.svg','logo-dark.svg','artwork.svg','raster/icon-16.png','raster/icon-32.png']
OUT=SITE/'assets/identity-signalform-v2'
if OUT.exists():
    raise SystemExit('Refusing to overwrite any existing reviewed identity assets')
OUT.mkdir(parents=True)
filelist=[]
for slug,name,role,concept,note in PRODUCTS:
    folder=SOURCE/'products'/slug/'candidates/signalform-v2'
    source_manifest=json.loads((folder/'manifest.json').read_text())
    raster_manifest=json.loads((folder/'raster/asset-index.json').read_text())
    assert source_manifest['approved'] is False
    assert source_manifest['family']=='signalform-v2'
    assert source_manifest['product']==slug
    assert raster_manifest['status'].startswith('unapproved')
    dst=OUT/slug
    dst.mkdir()
    for source in FLAT:
        content=(folder/source).read_bytes()
        expected=(source_manifest['files'][source] if source.endswith('.svg') else raster_manifest['files'][source.split('/')[-1]]['sha256'])
        actual=hashlib.sha256(content).hexdigest()
        if actual!=expected:raise SystemExit('V2 SHA-256 source mismatch: '+slug+'/'+source)
        dest=dst/Path(source).name
        dest.write_bytes(content)
        filelist.append({'path':'assets/identity-signalform-v2/'+slug+'/'+dest.name,
                         'sha256':actual, 'source':'products/'+slug+'/candidates/signalform-v2/'+source,
                         'status':'unapproved-candidate'})
manifest={'schema_version':1,'brand_repo':'GoreeCloud/brand-assets',
          'source_commit':SOURCE_SHA,
          'status':'review-only, unapproved, not official',
          'products':[x[0] for x in PRODUCTS], 'files':filelist}
(ROOT/'SIGNALFORM-V2-SOURCES.json').write_text(json.dumps(manifest,indent=2)+'\n')

# Reuse the exact existing noindex/CSP nav shell, but not its controls/script.
old=(SITE/'identity-review/index.html').read_text()
assert old.count('<main id="main">')==1
head,rest=old.split('<main id="main">',1)
_,tail=rest.split('</main>',1)
head=head.replace('  <script src="/assets/identity-workbench.js" defer></script>\n','')
head=head.replace('Brand identity review — GoreeCloud','Signalform v2 identity comparison — GoreeCloud')
head=head.replace('Review unapproved GoreeCloud product identities.',
                  'Compare seven original GoreeCloud v1 and Signalform v2 identity proposals.')
columns=[]
for slug,name,role,concept,note in PRODUCTS:
    a=html.escape
    oldbase='/assets/identity-review/'+slug+'/'
    newbase='/assets/identity-signalform-v2/'+slug+'/'
    source='https://github.com/GoreeCloud/brand-assets/blob/'+SOURCE_SHA+'/products/'+slug+'/candidates/signalform-v2/app-icon.svg'
    columns.append(f'''<article class="sf-product" id="compare-{slug}" data-signalform-identity="{slug}" data-approval="pending">
      <div class="sf-product-head">
       <div><span class="eyebrow">{a(role)} / UNAPPROVED REDESIGN</span><h2>{a(name)}</h2>
          <p>{a(concept)} — {a(note)}</p></div>
       <a class="text-link" href="{source}" target="_blank" rel="noopener noreferrer">Inspect V2 SVG source <span aria-hidden="true">↗</span></a>
      </div>
      <div class="sf-comparison">
        <div class="sf-version">
         <h3>Before <span>Foundation v1 · preserved</span></h3>
         <div class="sf-icon-frame"><img src="{oldbase}app-icon.svg" width="512" height="512" alt="{a(name)} original Foundation v1 proposal" loading="lazy" decoding="async"></div>
         <div class="sf-size-line"><span>Actual pixel sizes</span><img src="{oldbase}icon-16.png" width="16" height="16" alt="{a(name)} V1 at 16 pixels"><img src="{oldbase}icon-32.png" width="32" height="32" alt="{a(name)} V1 at 32 pixels"></div>
        </div>
        <div class="sf-version">
         <h3>Redesigned <span>Signalform v2 · pending approval</span></h3>
         <div class="sf-icon-frame"><img src="{newbase}app-icon.svg" width="512" height="512" alt="{a(name)} redesigned Signalform v2 proposal" loading="lazy" decoding="async"></div>
         <div class="sf-size-line"><span>Actual pixel sizes</span><img src="{newbase}icon-16.png" width="16" height="16" alt="{a(name)} V2 at 16 pixels"><img src="{newbase}icon-32.png" width="32" height="32" alt="{a(name)} V2 at 32 pixels"></div>
        </div>
      </div>
      <div class="sf-wordmarks">
       <div class="sf-wordmark-light"><span>V2 light wordmark</span><img src="{newbase}logo.svg" width="1120" height="170" alt="{a(name)} v2 light-background wordmark" loading="lazy" decoding="async"></div>
       <div class="sf-wordmark-dark"><span>V2 dark wordmark</span><img src="{newbase}logo-dark.svg" width="1120" height="170" alt="{a(name)} v2 dark-background wordmark" loading="lazy" decoding="async"></div>
      </div>
      <details class="sf-more">
       <summary>Inspect standalone symbol and conceptual artwork</summary>
       <div class="sf-more-content">
        <img class="sf-symbol" src="{newbase}symbol.svg" width="512" height="512" alt="{a(name)} original proposed standalone symbol" loading="lazy" decoding="async">
        <img class="sf-art" src="{newbase}artwork.svg" width="1280" height="760" alt="{a(name)} proposed conceptual brand artwork; not a product screenshot" loading="lazy" decoding="async">
       </div>
      </details>
     </article>''')
page='''<main id="main">
<section class="page-hero sf-intro"><div class="container">
 <span class="eyebrow">Original product identity study / November 2026</span>
 <h1>More distinctive.<br><span class="gradient-text">Still GoreeCloud.</span></h1>
 <p class="lead">Before-and-after comparisons of seven independent product identities. The previous concepts are retained, while Signalform v2 explores open forms, intentional connection, clearer routing and stronger product-specific silhouettes.</p>
 <p class="sf-warning"><strong>All seven designs are proposals.</strong> The original permanent GoreeCloud G, approved product marks, and production website remain unchanged. The designs below are not official, do not indicate implemented services, and none has founder approval.</p>
 <p><a class="text-link" href="https://github.com/GoreeCloud/brand-assets/pull/27" target="_blank" rel="noopener noreferrer">Review the source proposal and test evidence <span aria-hidden="true">↗</span></a></p>
</div></section>
<section class="section-tight"><div class="container">
 <nav class="sf-section-nav" aria-label="Jump to product comparison">'''+''.join(f'<a href="#compare-{slug}">{html.escape(name)}</a>' for slug,name,_,_,_ in PRODUCTS)+'''</nav>
 <div class="sf-product-list">'''+ '\n'.join(columns)+'''</div>
 <p class="sf-final">No approvals are recorded by this page. The preferred designs must pass deliberate founder review, manual small-size/accessibility checks, canonical-source promotion and downstream consumer verification. <a class="text-link" href="/identity-review/">Return to the original identity workbench</a>.</p>
</div></section>
</main>'''
out=SITE/'identity-review-v2/index.html'
out.parent.mkdir(exist_ok=True)
out.write_text(head+page+tail)
css=SITE/'assets/site.css'
txt=css.read_text()
assert '/* Signalform v2 review comparison' not in txt
txt+='''

/* Signalform v2 review comparison — never canonical product branding. */
.sf-intro {padding-bottom:23px;}
.sf-intro h1 {max-width:950px;}
.sf-warning {max-width:82ch;background:var(--gc-surface-tonal);border:1px solid var(--gc-outline);
 border-radius:var(--radius-md);padding:16px 20px;line-height:1.65;color:var(--gc-text-soft);font-size:15px;}
.sf-section-nav {display:flex;gap:8px;flex-wrap:wrap;margin:0 0 25px;}
.sf-section-nav a {padding:10px 14px;min-height:44px;display:flex;align-items:center;
 border:1px solid var(--gc-divider);border-radius:999px;color:var(--gc-text);background:var(--gc-surface);font-size:13px;font-weight:670;text-decoration:none;}
.sf-section-nav a:focus-visible {outline:3px solid var(--gc-focus);outline-offset:3px;}
.sf-product-list {display:grid;gap:26px;}
.sf-product {padding:clamp(16px,2.8vw,32px);background:var(--gc-surface);border:1px solid var(--gc-divider);
 border-radius:var(--radius-xl);scroll-margin-top:90px;min-width:0;}
.sf-product-head {display:flex;justify-content:space-between;align-items:start;gap:18px;margin-bottom:19px;}
.sf-product-head h2 {font-size:clamp(24px,3vw,43px);margin:10px 0 8px;}
.sf-product-head p {max-width:66ch;line-height:1.6;color:var(--gc-text-soft);}
.sf-product-head .text-link {flex:none;font-size:13px;}
.sf-comparison {display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;}
.sf-version {min-width:0;border:1px solid var(--gc-divider);border-radius:var(--radius-lg);overflow:hidden;}
.sf-version h3 {padding:15px 17px;margin:0;font-size:17px;display:flex;align-items:start;gap:5px;flex-direction:column;}
.sf-version h3 span {font-size:12px;color:var(--gc-text-soft);font-weight:530;}
.sf-icon-frame {min-height:0;background:#e5eaf6;display:flex;align-items:center;justify-content:center;padding:23px;}
.sf-icon-frame img {display:block;width:min(100%,230px);height:auto;aspect-ratio:1;object-fit:contain;}
.sf-size-line {min-height:56px;padding:10px 16px;display:flex;align-items:center;gap:15px;}
.sf-size-line span {font-size:12px;color:var(--gc-text-soft);}
.sf-size-line img {object-fit:contain;flex:none;image-rendering:auto;}
.sf-wordmarks {display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:15px;}
.sf-wordmarks>div {padding:16px;min-width:0;border-radius:var(--radius-md);border:1px solid var(--gc-divider);}
.sf-wordmarks span {font-size:12px;font-weight:710;display:block;margin-bottom:10px;}
.sf-wordmarks img {width:100%;height:auto;max-height:90px;object-fit:contain;object-position:left;}
.sf-wordmark-light {background:#fff;color:#273857;}
.sf-wordmark-dark {background:#14213d;color:#f3f6ff;}
.sf-more {border-top:1px solid var(--gc-divider);margin-top:20px;padding-top:13px;}
.sf-more summary {cursor:pointer;min-height:44px;font-weight:660;display:flex;align-items:center;color:var(--gc-text);}
.sf-more summary:focus-visible {outline:3px solid var(--gc-focus);}
.sf-more-content {display:grid;grid-template-columns:1fr 2fr;gap:18px;align-items:center;}
.sf-more-content img {max-width:100%;height:auto;object-fit:contain;}
.sf-more-content .sf-symbol {max-height:240px;object-fit:contain;}
.sf-final {margin:34px 0 0;max-width:80ch;color:var(--gc-text-soft);line-height:1.7;}
@media(max-width:760px){
 .sf-product-head {display:block;}
 .sf-comparison {gap:9px;}
 .sf-icon-frame {padding:13px;}
 .sf-version h3 {padding:12px;font-size:15px;}
 .sf-size-line {padding:10px;gap:9px;flex-wrap:wrap;}
 .sf-wordmarks {grid-template-columns:1fr;}
 .sf-more-content {grid-template-columns:1fr;}
}
@media(max-width:390px){
 .sf-product {padding:12px;}
 .sf-comparison {grid-template-columns:1fr;}
 .sf-icon-frame img {width:min(100%,168px);}
}
@media(forced-colors:active){
 .sf-product,.sf-version,.sf-wordmarks>div,.sf-warning {border:2px solid CanvasText;}
}
'''
css.write_text(txt)
# Add an optional review-only comparison entry point to v1, without changing its status.
p=SITE/'identity-review/index.html'
t=p.read_text()
needle='The Flowframe v2 graphics'
# Fall back to a reliable nonintrusive link right after the review main heading.
insert='<p><a class="text-link" href="/identity-review-v2/">Compare the redesigned Signalform v2 identity candidates <span aria-hidden="true">↗</span></a></p>\n'
marker='    <p class="identity-review-warning">'
if marker not in t:
    marker='<p class="identity-review-warning">'
assert marker in t
t=t.replace(marker,insert+marker,1)
p.write_text(t)
print('Generated static V1/V2 comparison:',len(PRODUCTS),'products,',len(filelist),'source-pinned V2 files')
