#!/usr/bin/env python3
"""Strict first-party product-mark and identity-status audit for preview only."""
from __future__ import annotations

from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,sys

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
PRODUCTS=SITE/'products/index.html'
PINS={
    'browser-family.svg':'d99784423ac237a01b520153953842cbfecf1a838f2d2fcfaa9a0d2eff704769',
    'search.svg':'74db42cf6b20c9527614471b6cc6cea004c39c28f385ad7c499f374161406dc0',
    'drive-existing-consumer.svg':'c04f6525f08ba351163b62450acab28731bb85f0eb1aa42fd42defadf3ce2bdc',
}
EXPECTED={
    'GoreeCloud UI':('candidate','/assets/gc-ui/app-icon.svg'),
    'GoreeShield':('missing',None),
    'Wardveil':('missing',None),
    'GoreeCloud Mesh':('missing',None),
    'GoreeCloud Browser':('official','/assets/product-icons/browser-family.svg'),
    'Browser Mobile':('official','/assets/product-icons/browser-family.svg'),
    'GoreeCloud Maps':('missing',None),
    'GoreeCloud Search':('verified-consumer','/assets/product-icons/search.svg'),
    'GoreeCloud Drive':('existing-consumer','/assets/product-icons/drive-existing-consumer.svg'),
    'GoreeCloud Projects':('missing',None),
    'GoreeCloud Analytics':('missing',None),
    'GoreeCloud Gateway':('missing',None),
}

class Cards(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.cards=[]
        self.current=None
        self.heading=False

    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if tag=='article' and 'data-product-card' in d:
            if self.current is not None:raise ValueError('Nested catalog article')
            self.current={'name':'','status':None,'icons':[],'pending':False}
        if self.current is None:return
        if tag=='h3':self.heading=True
        if tag=='div' and d.get('data-identity-status'):
            if self.current['status']:raise ValueError('Duplicate identity slot')
            self.current['status']=d['data-identity-status']
        if tag=='img' and d.get('class')=='product-identity-mark':
            self.current['icons'].append((d.get('src'),d.get('alt')))
        if tag=='span' and d.get('class')=='product-identity-pending':
            self.current['pending']=True
    def handle_data(self, value):
        if self.current is not None and self.heading:self.current['name']+=value
    def handle_endtag(self, tag):
        if tag=='h3':self.heading=False
        if tag=='article' and self.current is not None:
            self.cards.append(self.current)
            self.current=None

def audit():
    problems=[]
    for name,expected in PINS.items():
        p=SITE/'assets/product-icons'/name
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
            problems.append('source icon changed: '+name)
        elif any(word in p.read_bytes().lower() for word in (b'<script',b'<foreignobject',b'<image',b'xlink:href',b'href="http:',b'href="https:')):
            problems.append('unsafe SVG content: '+name)
    obj=json.loads((ROOT/'PRODUCT-ICON-SOURCES.json').read_text())
    paths={'browser-family':'browser-family.svg','search':'search.svg','drive-existing-consumer':'drive-existing-consumer.svg'}
    for key,name in paths.items():
        if obj[key]['sha256']!=PINS[name]:problems.append('central provenance manifest mismatch: '+name)
    parser=Cards();parser.feed((SITE/'products/index.html').read_text())
    if len(parser.cards)!=12:problems.append(f'expected 12 cards, got {len(parser.cards)}')
    found=set()
    for card in parser.cards:
        name=card['name'].strip()
        if name not in EXPECTED:problems.append('Unexpected product '+name);continue
        if name in found:problems.append('Duplicate '+name)
        found.add(name)
        status,target=EXPECTED[name]
        if status!=card['status']:problems.append(f'{name}: status {card["status"]!r}, expected {status}')
        if target:
            if card['icons']!=[(target,'')]:problems.append(name+': wrong product icon / missing decorative alt')
            if card['pending']:problems.append(name+': wrongly marked missing')
        else:
            if card['icons'] or not card['pending']:problems.append(name+': unapproved official icon inferred')
    if found!=set(EXPECTED):problems.append('Missing identities: '+repr(set(EXPECTED)-found))
    return problems

if __name__=='__main__':
    problems=audit()
    if problems:
        print('FAIL product identity audit:',*problems,sep='\n - ')
        sys.exit(1)
    print('PASS product identity: 12 catalog entries, 2 approved Browser uses, recovered Search, existing consumer Drive, proposed GC UI, 7 honest gaps, SHA-256 pins')
