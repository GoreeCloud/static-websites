#!/usr/bin/env python3
"""Isolated preview-only compact-layout and known-source product identities.

This script never designs marks or claims that unreviewed logos are official.
It copies existing first-party assets and validates current provenance.
"""
from pathlib import Path
import hashlib, json, os, re

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
if not os.environ.get('GOREECLOUD_BRAND_ASSETS_DIR'):
    raise SystemExit('Supply GOREECLOUD_BRAND_ASSETS_DIR pointing at the verified central brand-assets checkout')
ASSET_ROOT=Path(os.environ['GOREECLOUD_BRAND_ASSETS_DIR'])
ICON_DIR=SITE/'assets/product-icons'
ICON_DIR.mkdir(exist_ok=True)
SOURCES={
    'browser-family': ('central-approved', ASSET_ROOT/'products/browser-mobile/app-icon.svg',
      'GoreeCloud Browser and Browser Mobile share founder-approved Prism Tabs v5'),
    'search': ('central-existing',ASSET_ROOT/'products/search/app-icon.svg',
      'Recovered first-party Search favicon; central source and existing consumer match'),
}
for key,(status,p,note) in SOURCES.items():
    if not p.is_file():raise SystemExit('Missing existing official master: '+str(p))
    raw=p.read_bytes()
    if any(fragment in raw.lower() for fragment in (b'<script',b'<foreignobject',b'<image',b'xlink:href',b'href="https:',b'href="http:',b'url(https:')):
        raise SystemExit('Untrusted SVG master needs source review: '+str(p))
    (ICON_DIR/(key+'.svg')).write_bytes(raw)
# Consumer-in-use custom-branded Drive theme icon (not a centrally accepted master).
# Retrieved from GoreeCloud/drive in the authorized clone API read, not a third-party OpenCloud logo.
DRIVE_SVG=ICON_DIR/'drive-existing-consumer.svg'
if not DRIVE_SVG.exists():
    raise SystemExit('Need the separately verified Drive themed SVG source before proceeding')

products=SITE/'products/index.html'
t=products.read_text()
if 'data-identity-status=' in t:
    raise SystemExit('Site already modified')
entries={
    'GoreeCloud UI':('/assets/gc-ui/app-icon.svg','candidate','Flowframe v2 design proposed, not approved'),
    'GoreeCloud Browser':('/assets/product-icons/browser-family.svg','official','Founder-approved Prism Tabs v5'),
    'Browser Mobile':('/assets/product-icons/browser-family.svg','official','Founder-approved shared Prism Tabs v5'),
    'GoreeCloud Search':('/assets/product-icons/search.svg','verified-consumer','Current official Search icon source'),
    'GoreeCloud Drive':('/assets/product-icons/drive-existing-consumer.svg','existing-consumer','First-party Drive theme icon; not yet centrally approved'),
}
needed=['GoreeShield','Wardveil','GoreeCloud Mesh','GoreeCloud Maps','GoreeCloud Projects','GoreeCloud Analytics','GoreeCloud Gateway']

def replace_card(m):
    card=m.group(0)
    name_match=re.search(r'<h3>([^<]+)</h3>',card)
    if not name_match:raise ValueError('Product card without simple title')
    name=name_match.group(1)
    if name in entries:
        src,state,note=entries[name]
        # Existing GCUI icon should be replaced with a single common identity slot.
        card=re.sub(r'<img class="gcui-product-mark"[^>]*>', '',card)
        icon=(f'<img class="product-identity-mark" src="{src}" alt="" '
              f'width="52" height="52" loading="lazy" decoding="async">')
    elif name in needed:
        state,note='missing','No centrally accepted official icon recovered'
        icon='<span class="product-identity-pending" role="note" title="Official product artwork still pending" aria-label="Official product icon pending"><span aria-hidden="true">·</span></span>'
    else:
        raise ValueError('Unreviewed product '+name)
    card=card.replace('<h3>',f'<div class="product-identity" data-identity-status="{state}">{icon}</div><h3>',1)
    return card

t,count=re.subn(r'<article class="product-card"[^>]*>.*?</article>',replace_card,t,flags=re.S)
if count!=12:raise SystemExit(f'Expected 12 product cards, found {count}')
products.write_text(t)

css_path=SITE/'assets/site.css'
css=css_path.read_text()
css+="""

/* Spacing refinement — preserves GC UI semantic tokens and 44px controls.
   Reduces oversized blank surfaces without hiding content. */
:root { --gc-section-compact: 65px; }
@media(min-width:641px){
  .hero { padding:clamp(56px,6vw,85px) 0 60px; }
  .visual-stage { min-height:430px; }
  .stage-core { max-width:272px; }
  .section { padding:var(--gc-section-compact) 0; }
  .section-tight { padding:41px 0; }
  .section-head { margin-bottom:30px; }
  .card { min-height:232px; padding:22px; }
  .card .symbol { margin:18px 0 19px; width:50px; height:50px; }
  .split { gap:clamp(28px,4vw,66px); }
  .editorial-article { min-height:250px; padding:30px; }
  .cta { padding:clamp(34px,4vw,54px); }
  .page-hero { padding:76px 0 44px; }
  .pillar-detail { padding:32px 0; gap:25px; }
  .pillar-detail .scope { margin-bottom:14px; }
  .product-card { min-height:218px; padding:23px; }
  .product-card h3 { margin:12px 0 8px; }
  .footer { margin-top:50px; padding:44px 0 26px; }
  .footer-bottom { margin-top:38px; padding-top:19px; }
  h2 { font-size:clamp(2.35rem,3.8vw,3.65rem); }
  .page-hero h1 { font-size:clamp(3.25rem,5.4vw,5.4rem); }
}
.gcui-feature-art { aspect-ratio:1440/900; object-fit:contain; }
.gcui-feature-head { padding:14px 18px; }
.gcui-feature-caption { padding:12px 18px 17px; }
.gcui-feature-caption-copy { line-height:1.55; }
.gcui-wordmark-pair { max-width:235px; }
.gcui-hero-art img { aspect-ratio:1440/900; object-fit:contain; }
.product-identity { margin:13px 0 2px; width:52px; height:52px; flex:none; }
.product-identity-mark { display:block; width:52px; height:52px; border-radius:15px; object-fit:contain; }
.product-identity-pending { width:52px; height:52px; display:grid; place-items:center;
  border:1px dashed var(--gc-outline); border-radius:15px; color:var(--gc-text-faint);
  background:var(--gc-surface-tonal); font-size:24px; font-weight:500; }
.product-identity[data-identity-status="missing"] { opacity:.62; }
@media(max-width:640px){
  .hero { padding:40px 0 44px; }
  .visual-stage { min-height:315px; }
  .stage-core { max-width:235px; }
  .section { padding:47px 0; }
  .section-tight { padding:34px 0; }
  .section-head { margin-bottom:24px; }
  .page-hero { padding:54px 0 33px; }
  .pillar-detail { padding:25px 0; gap:12px; }
  .cta { padding:29px 23px; }
  .editorial-article { min-height:220px; padding:25px; }
  .product-card { min-height:0; padding:21px; }
  .product-card h3 { margin:9px 0; }
  .footer { margin-top:32px; padding:38px 0 20px; }
  .footer-bottom { margin-top:25px; padding-top:16px; }
  .card { padding:22px; }
}
@media(prefers-reduced-motion:reduce) {
 .card:hover, .button:hover, .icon-button:hover { transform:none; }
}
@media(forced-colors:active) {
 .product-identity-pending { border:1px dashed CanvasText; }
}
"""
css_path.write_text(css)
report={}
for key,(status,p,note) in SOURCES.items():
    report[key]={"status":status,"source":str(p.relative_to(ASSET_ROOT)),
                 "sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"notes":note}
report['drive-existing-consumer']={
    'status':'existing-consumer-not-centrally-approved',
    'source':'GoreeCloud/drive/services/web/assets/themes/goreecloud/assets/icon.svg',
    'sha256':hashlib.sha256(DRIVE_SVG.read_bytes()).hexdigest(),
    'notes':'GoreeCloud-specific first-party theme; NOT the OpenCloud upstream logo; official central review pending'
}
(ROOT/'PRODUCT-ICON-SOURCES.json').write_text(json.dumps(report,indent=2)+'\n')
print('Compact layout applied; official/recovered assets sourced; 12 cards: 5 icon surfaces and 7 explicit pending identities.')
