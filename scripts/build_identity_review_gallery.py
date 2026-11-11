#!/usr/bin/env python3
"""Source-pinned, accessible static gallery for unapproved product identities.

Only modifies an isolated website review branch. Source images come from
GoreeCloud/brand-assets candidate PR #25 and are not altered or published
as approved product marks. No design generation or external network usage.
"""
from __future__ import annotations
import hashlib, html, json, os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
SOURCE_COMMIT='c48ebf7e9a098184e879445e6fe4aec9171fa7c3'
if not os.getenv('GOREECLOUD_BRAND_ASSETS_DIR'):
    raise SystemExit('Set GOREECLOUD_BRAND_ASSETS_DIR to exact checked-out candidate source')
SOURCE=Path(os.environ['GOREECLOUD_BRAND_ASSETS_DIR'])
PRODUCTS=[
 ('goreeshield','GoreeShield','PRIVACY','Privacy choices and consent. Layered protection surrounding an explicit choice control.'),
 ('wardveil','Wardveil','CYBERSECURITY','Threat defense and monitoring. A watch shield carrying a protective signal.'),
 ('mesh','GoreeCloud Mesh','INTEGRATION','Bounded system connectivity. Four independent endpoints connected through an intentional hub.'),
 ('maps','GoreeCloud Maps','MAPS & LOCATION','Navigable terrain and destination. Folded map surfaces with a clear location pin.'),
 ('projects','GoreeCloud Projects','PLANNING','Organized independent work. A segmented three-lane project board.'),
 ('analytics','GoreeCloud Analytics','ANALYTICS','Thoughtful measurement. Distinct chart bars and a simplified trend trace.'),
 ('gateway','GoreeCloud Gateway','NETWORK EDGE','Managed network entry. Two isolated networks linked by a deliberate gateway.')
]
IMAGES=['app-icon.svg','symbol.svg','logo.svg','logo-dark.svg','artwork.svg','raster/icon-16.png','raster/icon-32.png']
OUT=SITE/'assets/identity-review'
if OUT.exists():raise SystemExit('Gallery assets already present; repeat by clean checkout, not overwrite')
OUT.mkdir(parents=True)

entrylist=[]
for slug,name,role,meaning in PRODUCTS:
    source=SOURCE/'products'/slug/'candidates/foundation-v1'
    review=OUT/slug
    review.mkdir()
    original=json.loads((source/'manifest.json').read_text())
    raster=json.loads((source/'raster/asset-index.json').read_text())
    if original['status']!='unapproved original candidate; NOT an official brand master':
        raise SystemExit('Status mismatch: '+slug)
    for asset in IMAGES:
        data=(source/asset).read_bytes()
        if asset.endswith('.svg'):
            if hashlib.sha256(data).hexdigest()!=original['files'][asset]:
                raise SystemExit('Source vector mismatch: '+slug+'/'+asset)
        elif hashlib.sha256(data).hexdigest()!=raster['files'][asset.split('/')[-1]]['sha256']:
            raise SystemExit('Source raster mismatch: '+slug+'/'+asset)
        dest=review/Path(asset).name
        dest.write_bytes(data)
        entrylist.append({
          'web':'assets/identity-review/'+slug+'/'+dest.name,
          'source':'products/'+slug+'/candidates/foundation-v1/'+asset,
          'sha256':hashlib.sha256(data).hexdigest(),
          'status':'candidate-only'})
manifest={'schema_version':1,'source_repo':'GoreeCloud/brand-assets',
          'source_commit':SOURCE_COMMIT,
          'status':'unapproved preview-only candidates, not official product marks',
          'products':[x[0] for x in PRODUCTS],'files':entrylist}
(ROOT/'IDENTITY-REVIEW-SOURCES.json').write_text(json.dumps(manifest,indent=2)+'\n')

products=SITE/'products/index.html'
source=products.read_text()
head,tail=source.split('<main id="main">',1)
_,foot=tail.split('</main>',1)
head=head.replace('<title>Products and open development — GoreeCloud</title>',
                  '<title>Brand identity review — GoreeCloud</title>')
head=head.replace('content="Explore', 'content="Review unapproved GoreeCloud product identities. Explore',1)
cards=[]
for slug,name,role,meaning in PRODUCTS:
    escape=html.escape
    prefix='/assets/identity-review/'+slug+'/'
    srcbase='https://github.com/GoreeCloud/brand-assets/blob/'+SOURCE_COMMIT+'/products/'+slug+'/candidates/foundation-v1/'
    # Icon illustrations are decorative because the adjacent text states the identity.
    card=f'''<article class="identity-review-card" data-review-product="{slug}" data-review-status="candidate">
  <div class="identity-review-art">
    <img src="{prefix}artwork.svg" alt="Conceptual {escape(name)} Foundation v1 artwork, not an application screenshot" width="1280" height="720" loading="lazy" decoding="async">
  </div>
  <div class="identity-review-copy">
    <div class="identity-review-heading">
      <img src="{prefix}app-icon.svg" alt="" width="58" height="58" loading="lazy" decoding="async">
      <div><span class="identity-review-role">{escape(role)}</span><h2>{escape(name)}</h2></div>
    </div>
    <p>{escape(meaning)}</p>
    <div class="identity-review-wordmark">
      <img class="review-wordmark-for-light" src="{prefix}logo.svg" alt="Proposed {escape(name)} light-background wordmark" width="1100" height="170" loading="lazy" decoding="async">
      <img class="review-wordmark-for-dark" src="{prefix}logo-dark.svg" alt="Proposed {escape(name)} dark-background wordmark" width="1100" height="170" loading="lazy" decoding="async">
    </div>
    <div class="identity-review-size-row" role="group" aria-label="{escape(name)} pixel-size identity examples">
      <span>True size</span>
      <img src="{prefix}icon-16.png" alt="{escape(name)} icon at 16 pixels" width="16" height="16" loading="lazy" decoding="async">
      <img src="{prefix}icon-32.png" alt="{escape(name)} icon at 32 pixels" width="32" height="32" loading="lazy" decoding="async">
      <img src="{prefix}symbol.svg" alt="{escape(name)} standalone concept mark" width="42" height="42" loading="lazy" decoding="async">
      <span>16 / 32 / symbol</span>
    </div>
    <div class="identity-review-source">
      <span class="identity-review-state">Proposed · not approved</span>
      <a class="text-link" href="{srcbase}app-icon.svg" target="_blank" rel="noopener noreferrer">View source SVG <span aria-hidden="true">↗</span></a>
    </div>
  </div>
</article>'''
    cards.append(card)
main='''<main id="main">
<section class="page-hero identity-review-intro">
  <div class="container"><span class="eyebrow">First-party brand exploration / source-controlled</span>
    <h1>Distinct roles.<br><span class="gradient-text">Distinct identities.</span></h1>
    <p class="lead">Seven product-specific design candidates with original vector geometry. Review their clarity at real icon sizes and their light/dark wordmarks before any official selection or deployment.</p>
    <p class="identity-review-warning"><strong>Review only.</strong> These designs have not been approved as official brands. They do not replace GoreeCloud's permanent blue G, the current official marks, or any deployed application assets. Illustrations are conceptual, not functional screenshots.</p>
    <p><a class="text-link" href="https://github.com/GoreeCloud/brand-assets/pull/25" target="_blank" rel="noopener noreferrer">Open the complete review PR <span aria-hidden="true">↗</span></a></p>
  </div>
</section>
<section class="section-tight">
  <div class="container">
    <div class="identity-review-grid">
'''+ '\n'.join(cards) +'''
    </div>
    <div class="identity-review-next">
      <h2>Approval comes before adoption.</h2>
      <p>These icons remain proposals until their distinction, small-size legibility, rights, accessibility, platform packaging and visual direction are reviewed. GoreeShield manages privacy, Wardveil manages cybersecurity, and Mesh manages integration; the icons do not imply that a service is deployed.</p>
      <a class="button secondary" href="/products/">Return to the product catalog <span class="arrow" aria-hidden="true">↗</span></a>
    </div>
  </div>
</section>
</main>'''
page=SITE/'identity-review/index.html'
page.parent.mkdir(exist_ok=True)
page.write_text(head+main+foot)
# Add an explicit review link to pending status disclosure on the Products page.
marker='the new GoreeCloud UI concept and Drive’s existing consumer icon still require central identity approval.</p>'
assert source.count(marker)==1
products.write_text(source.replace(marker,marker.replace('</p>',
  ' <a class="text-link" href="/identity-review/">View the seven proposed identity designs</a>.</p>'),1))

style=SITE/'assets/site.css'
css=style.read_text()
css+='''

/* Original GoreeCloud Foundation v1 image review — unapproved identity sandbox. */
.identity-review-intro {padding-bottom:26px;}
.identity-review-intro h1 {max-width:940px;}
.identity-review-warning {max-width:840px;padding:18px 22px;margin:24px 0 15px;
  background:var(--gc-surface-tonal);border:1px solid var(--gc-outline);border-radius:var(--radius-md);
  color:var(--gc-text-soft);font-size:15px;line-height:1.65;}
.identity-review-grid {display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;}
.identity-review-card {min-width:0;background:var(--gc-surface);border:1px solid var(--gc-divider);
  border-radius:var(--radius-lg);overflow:hidden;display:flex;flex-direction:column;}
.identity-review-art {background:#e6eaf6;overflow:hidden;}
.identity-review-art img {display:block;width:100%;height:auto;aspect-ratio:1280/720;object-fit:cover;}
.identity-review-copy {padding:24px;display:grid;gap:16px;}
.identity-review-heading {display:flex;align-items:center;gap:16px;}
.identity-review-heading>img {width:58px;height:58px;object-fit:contain;border-radius:15px;flex:none;}
.identity-review-heading h2 {font-size:clamp(20px,2.1vw,30px);margin:3px 0;}
.identity-review-role {display:block;color:var(--gc-text-faint);font-size:11px;letter-spacing:.12em;font-weight:760;}
.identity-review-copy>p {font-size:15px;color:var(--gc-text-soft);line-height:1.55;margin:0;}
.identity-review-wordmark {background:#fff;border:1px solid var(--gc-divider);border-radius:14px;
  min-height:76px;display:grid;align-items:center;padding:13px 16px;}
.identity-review-wordmark img {width:100%;height:auto;max-height:58px;object-fit:contain;object-position:left;}
.review-wordmark-for-dark {display:none!important;}
:root[data-theme="dark"] .identity-review-wordmark {background:#15203b;}
:root[data-theme="dark"] .review-wordmark-for-light {display:none!important;}
:root[data-theme="dark"] .review-wordmark-for-dark {display:block!important;}
.identity-review-size-row {display:flex;align-items:center;flex-wrap:wrap;gap:13px;
  padding:12px 0;border-top:1px solid var(--gc-divider);border-bottom:1px solid var(--gc-divider);}
.identity-review-size-row span {font-size:12px;color:var(--gc-text-faint);}
.identity-review-size-row img {flex:none;object-fit:contain;}
.identity-review-size-row img[width="16"] {width:16px;height:16px;}
.identity-review-size-row img[width="32"] {width:32px;height:32px;}
.identity-review-size-row img[width="42"] {width:42px;height:42px;}
.identity-review-source {display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;}
.identity-review-source .text-link {font-size:13px;}
.identity-review-state {font-size:12px;color:var(--gc-text-soft);}
.identity-review-next {margin-top:32px;padding:clamp(24px,4vw,46px);border-radius:var(--radius-xl);
  background:var(--gc-surface-tonal);border:1px solid var(--gc-divider);}
.identity-review-next h2 {font-size:clamp(24px,3.4vw,43px);}
.identity-review-next p {max-width:75ch;color:var(--gc-text-soft);}
@media(max-width:840px){.identity-review-grid{grid-template-columns:1fr;gap:16px;}}
@media(max-width:520px){.identity-review-copy{padding:18px;gap:13px;}
  .identity-review-heading>img{width:52px;height:52px;}
  .identity-review-size-row{gap:9px;}
  .identity-review-warning{padding:15px;}
}
@media(prefers-contrast:more){.identity-review-card,.identity-review-wordmark {border-width:2px;}}
@media(forced-colors:active){.identity-review-card,.identity-review-wordmark,.identity-review-warning{border:2px solid CanvasText;}}
'''
style.write_text(css)
print('Review gallery generated:',len(PRODUCTS),'unapproved cards;',len(entrylist),'byte-identical pinned candidate assets')
