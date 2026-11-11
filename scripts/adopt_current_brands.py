#!/usr/bin/env python3
"""Apply review-only umbrella and GC UI v2 image references to the static preview."""
from pathlib import Path
import hashlib,re

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/"site"
pages=sorted(SITE.rglob('*.html'))
assert len(pages)==15
replaced=0
for page in pages:
    s=page.read_text()
    old='<span class="brand-glyph" aria-hidden="true"></span>'
    count=s.count(old)
    s=s.replace(old,'<img class="brand-icon" src="/assets/goreecloud/official-profile-logo-1024.png" alt="" width="28" height="28" decoding="async">')
    replaced+=count
    before='  <link rel="stylesheet" href="/assets/site.css">'
    assert before in s,str(page)
    # Restore true umbrella site favicon across all routes, not an unapproved GC UI candidate.
    s=re.sub(r'^  <link rel="icon"[^\n]*\n','',s,flags=re.M)
    fav='''  <link rel="icon" type="image/svg+xml" href="/assets/goreecloud/logo.svg">
  <link rel="icon" type="image/x-icon" href="/assets/goreecloud/favicon.ico" sizes="any">
'''
    s=s.replace(before,fav+before,1)
    if page.parent.name=="design":
        s=s.replace('Approved GoreeCloud UI Aperture Weave identity','Flowframe v2 proposed GoreeCloud UI identity')
        s=s.replace('GoreeCloud UI Aperture Weave','GoreeCloud UI Flowframe v2 candidate')
        s=s.replace('GoreeCloud UI · Official design identity','GoreeCloud UI · Flowframe v2 concept · Under review')
        s=s.replace('Original Aperture Weave interface artwork','Original Flowframe v2 concept artwork')
        s=s.replace('width="710" height="180"','width="870" height="190"')
        s=s.replace('width="1440" height="980"','width="1440" height="900"')
        original='the retired Glaze system.</p>'
        assert original in s
        s=s.replace(original,'''the retired Glaze system.</p>
        <p class="gcui-review-note">The Flowframe v2 graphics shown here are a new visual identity proposal, not yet the official GoreeCloud UI mark.
        <a href="https://github.com/GoreeCloud/brand-assets/pull/22" target="_blank" rel="noopener noreferrer">View the source proposal and verification</a>.</p>''')
    if page==SITE/"index.html":
        assert '<div class="stage-core"><strong>G</strong></div>' in s
        s=s.replace('<div class="stage-core"><strong>G</strong></div>',
                    '<div class="stage-core"><img src="/assets/goreecloud/official-profile-logo-1024.png" alt="" width="310" height="310" decoding="async"></div>',1)
        s=s.replace('GoreeCloud UI Aperture Weave official wordmark','GoreeCloud UI Flowframe v2 candidate wordmark')
        s=s.replace('width="710" height="180"','width="870" height="190"')
        s=s.replace('FIRST-PARTY ARTWORK','NEW DESIGN CONCEPT')
        s=s.replace('Canvas, Surface, Lens. A shared language',
                    'Flowframe v2 identity proposal. Canvas, Surface, Lens. A shared language')
        s=s.replace('width="1440" height="980"','width="1440" height="900"')
    page.write_text(s)
assert replaced>=25,replaced
css=SITE/"assets/site.css"
s=css.read_text()
assert '/* Permanent umbrella G and experimental Flowframe review */' not in s
s+='''

/* Permanent umbrella G and experimental Flowframe review */
.brand-icon { width:28px;height:28px;flex:none;display:block;object-fit:contain;border-radius:8px; }
.stage-core { border:none;background:none;backdrop-filter:none;box-shadow:0 22px 80px rgba(59,130,246,.2);border-radius:33%;transform:none; }
.stage-core::before,.stage-core::after {content:none;}
.stage-core img { width:100%;height:100%;display:block;object-fit:contain;border-radius:33%; }
.gcui-review-note { max-width:65ch;color:var(--gc-text-soft);font-size:15px;line-height:1.65;margin-top:18px; }
.gcui-review-note a { text-decoration:underline;text-underline-offset:3px; }
.gcui-review-note a:focus-visible {outline:3px solid var(--gc-focus);outline-offset:3px;}
@media(max-width:640px){.brand-icon{width:25px;height:25px;}}
'''
css.write_text(s)
print('Prepared',len(pages),'HTML routes and',replaced,'brand placements')
