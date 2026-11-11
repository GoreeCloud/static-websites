#!/usr/bin/env python3
"""One-time, deterministic enhancement of the preview static site.

Run from the recovery branch baseline before the site is modified. This
does not call any APIs, write Cloudflare, or modify production.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/"site"
ASSETS=SITE/"assets/gc-ui"

def read(name):
    return (SITE/name).read_text(encoding="utf-8")
def write(name,value):
    (SITE/name).write_text(value,encoding="utf-8")

def balanced_div_replace(body, prefix, new_html):
    at=body.find(prefix)
    if at<0:raise ValueError("Source not found: "+prefix)
    tokens=re.finditer(r"<div\b[^>]*>|</div\s*>",body[at:],re.I|re.S)
    level=0
    for m in tokens:
        if m.group().lower().startswith("</div"):
            level-=1
            if level==0:
                return body[:at]+new_html+body[at+m.end():]
        else:level+=1
    raise ValueError("Unclosed source div: "+prefix)

# Audit official, local-only, product-scoped assets; do not recolor source SVGs.
names=["app-icon.svg","symbol.svg","logo-light.svg","logo-dark.svg","favicon.ico","interface-constellation.svg"]
if any(not (ASSETS/name).is_file() for name in names):
    raise SystemExit("Required pinned local GC UI asset missing")

home=read("index.html")
if '<div class="feature-wall"' not in home or "pillar-04" not in home:
    raise SystemExit("Unexpected home baseline")
original=home
home=balanced_div_replace(home,'<div class="feature-wall"',
'''<figure class="gcui-feature-panel">
  <div class="gcui-feature-head"><span class="gcui-feature-overline">THE DESIGN LANGUAGE · GOREeCLOUD UI</span><span class="gcui-feature-status">FIRST-PARTY ARTWORK</span></div>
  <img class="gcui-feature-art" src="/assets/gc-ui/interface-constellation.svg" alt="Original illustration of layered interface surfaces representing Cloud Canvas, Surface, and Lens" width="1440" height="980" loading="lazy" decoding="async">
  <figcaption class="gcui-feature-caption"><span class="gcui-wordmark-pair">
    <img class="gcui-wordmark-for-light" src="/assets/gc-ui/logo-light.svg" alt="GoreeCloud UI Aperture Weave official wordmark" width="710" height="180" loading="lazy">
    <img class="gcui-wordmark-for-dark" src="/assets/gc-ui/logo-dark.svg" alt="GoreeCloud UI Aperture Weave official wordmark" width="710" height="180" loading="lazy">
  </span><span class="gcui-feature-caption-copy">Canvas, Surface, Lens. A shared language for calm, capable software—not a claim of shipped features.</span></figcaption>
</figure>''')
home,n=re.subn(r'(<article class="card pillar-04">.*?<div class="symbol">).*?(</div><h3>GoreeCloud UI</h3>)',
                  r'\1<img src="/assets/gc-ui/symbol.svg" alt="" width="32" height="32" loading="lazy">\2',home,count=1,flags=re.S)
if n!=1:raise SystemExit("Could not replace GC UI pillar generic icon")
if len(home)==len(original):raise SystemExit("Home unchanged")
write("index.html",home)

design=read("design/index.html")
if '<div class="story-orbit"' not in design:
    raise SystemExit("Unexpected design page baseline")
design=design.replace('<link rel="stylesheet" href="/assets/site.css">',
'''<link rel="icon" type="image/svg+xml" href="/assets/gc-ui/app-icon.svg">
  <link rel="icon" type="image/x-icon" href="/assets/gc-ui/favicon.ico" sizes="any">
  <link rel="stylesheet" href="/assets/site.css">''',1)
design=design.replace('<div class="story-copy"><span class="eyebrow">GoreeCloud UI · GC UI</span>',
'''<div class="story-copy">
  <div class="gcui-brand-heading" aria-label="Approved GoreeCloud UI Aperture Weave identity">
    <img class="gcui-wordmark-for-light" src="/assets/gc-ui/logo-light.svg" alt="GoreeCloud UI Aperture Weave" width="710" height="180">
    <img class="gcui-wordmark-for-dark" src="/assets/gc-ui/logo-dark.svg" alt="GoreeCloud UI Aperture Weave" width="710" height="180">
  </div><span class="eyebrow">GoreeCloud UI · Official design identity</span>''',1)
design=balanced_div_replace(design,'<div class="story-orbit"',
'''<figure class="gcui-hero-art">
  <img src="/assets/gc-ui/interface-constellation.svg" alt="Official GC UI artwork showing three layered, floating interface surfaces in an abstract composition" width="1440" height="980" decoding="async">
  <figcaption>Original Aperture Weave interface artwork · Canvas / Surface / Lens</figcaption>
</figure>''')
write("design/index.html",design)

products=read("products/index.html")
patt='<h3>GoreeCloud UI</h3>'
if products.count(patt)!=1:raise SystemExit("Unexpected products entry count")
products=products.replace(patt,'<img class="gcui-product-mark" src="/assets/gc-ui/app-icon.svg" alt="" width="58" height="58" loading="lazy">'+patt)
write("products/index.html",products)

ecosystem=read("ecosystem/index.html")
if '<h2>GoreeCloud UI</h2>' in ecosystem:
    ecosystem=ecosystem.replace('<h2>GoreeCloud UI</h2>','<img class="gcui-ecosystem-mark" src="/assets/gc-ui/symbol.svg" alt="" width="56" height="56" loading="lazy"><h2>GoreeCloud UI</h2>',1)
    write("ecosystem/index.html",ecosystem)

css=read("assets/site.css")
if "/* GC UI branded polish, verified art assets" in css:raise SystemExit("Already improved")
css+='''

/* GC UI branded polish, verified art assets; no new UI semantic palette. */
body { font-size:17px; }
.eyebrow { font-size:12px; letter-spacing:.15em; }
.micro-note,.footer-bottom { font-size:13px; line-height:1.6; }
.card p,.product-card p { font-size:16px; line-height:1.7; }
.card { min-height:272px; }
.section { padding:84px 0; }
.section-tight { padding:52px 0; }
.hero { padding:clamp(62px,7vw,108px) 0 82px; }
h1 { font-size:clamp(3.7rem,6.4vw,6.7rem); }
h2 { font-size:clamp(2.5rem,4.1vw,4rem); }
.hero .lead { max-width:600px; }
.section-head p { font-size:18px; }
.footer { margin-top:65px; }
.footer nav a,.footer p { font-size:15px; }
.card .symbol img { width:32px;height:32px;display:block;object-fit:contain; }
.gcui-product-mark { display:block; width:58px;height:58px; margin:0 0 20px;border-radius:16px; }
.gcui-ecosystem-mark { width:54px;height:54px;display:block;margin:0 0 18px;object-fit:contain; }
.gcui-feature-panel { margin:0;position:relative;min-width:0; border:1px solid var(--gc-divider);border-radius:var(--radius-xl);background:var(--gc-surface);overflow:hidden;box-shadow:var(--gc-shadow); }
.gcui-feature-head { padding:20px 24px;display:flex;gap:8px;flex-wrap:wrap;justify-content:space-between;align-items:center;color:var(--gc-text-soft);font-size:11px;font-weight:750;letter-spacing:.1em; }
.gcui-feature-overline {text-transform:uppercase;}
.gcui-feature-status {font-size:11px;letter-spacing:.04em;opacity:.85;}
.gcui-feature-art {width:100%;aspect-ratio:1440/880;object-fit:cover;display:block;background:#10182f; }
.gcui-feature-caption {padding:19px 24px 24px;display:grid;gap:7px;background:var(--gc-surface);}
.gcui-wordmark-pair {display:block;max-width:265px;}
.gcui-wordmark-pair img,.gcui-brand-heading img {display:block;width:100%;height:auto;object-fit:contain;}
.gcui-wordmark-for-light {display:none!important;}
:root[data-theme="light"] .gcui-wordmark-for-light {display:block!important;}
:root[data-theme="light"] .gcui-wordmark-for-dark {display:none!important;}
.gcui-feature-caption-copy {font-size:15px;color:var(--gc-text-soft);line-height:1.6;max-width:55ch;}
.gcui-brand-heading {max-width:340px;min-width:0;margin-bottom:26px;}
.gcui-hero-art {margin:0;border:1px solid var(--gc-divider);border-radius:var(--radius-xl);overflow:hidden;background:#10182f;box-shadow:var(--gc-shadow);min-width:0;}
.gcui-hero-art img {width:100%;height:auto;aspect-ratio:1440/980;display:block;}
.gcui-hero-art figcaption {padding:13px 20px;font-size:13px;line-height:1.5;color:#e3e9ff;background:#151d39;}
.story-hero .story-grid:has(.gcui-hero-art) {grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(28px,4vw,64px);}
.story-hero .story-grid:has(.gcui-hero-art) h1 {font-size:clamp(3.3rem,5vw,5.3rem);}
@media(max-width:860px){
  .story-hero .story-grid:has(.gcui-hero-art){grid-template-columns:1fr;}
  .gcui-hero-art{max-width:760px;}
}
@media(max-width:640px){
  body {font-size:16px;}
  .section {padding:61px 0;}
  .hero {padding:54px 0 58px;}
  .card {min-height:0;}
  .micro-note,.footer-bottom {font-size:13px;}
  .eyebrow {font-size:11px;}
  .mobile-nav a {font-size:11px;}
  .gcui-feature-head {padding:15px;}
  .gcui-feature-caption {padding:14px 17px 19px;}
  .gcui-feature-caption-copy {font-size:14px;}
  .gcui-brand-heading {max-width:275px;}
}
@media(prefers-contrast:more){
  .gcui-feature-panel,.gcui-hero-art {box-shadow:none;border-width:2px;}
}
@media(forced-colors:active){
  .gcui-feature-panel,.gcui-hero-art {border:2px solid CanvasText;}
}
'''
write("assets/site.css",css)
print("Improved homepage, GC UI design, products, ecosystem, shared stylesheet.")
