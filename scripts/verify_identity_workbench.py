#!/usr/bin/env python3
"""Offline contract for nontracking, candidate-only interactive review controls."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
GROUPS={
 'goreeshield':'pillars','wardveil':'pillars','mesh':'pillars',
 'maps':'applications','projects':'applications','analytics':'applications',
 'gateway':'infrastructure'
}

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards=[]
        self.links=[]
        self.controls={}
        self.has_script=False
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='article' and d.get('data-review-product'):
            self.cards.append(d)
        if tag=='a' and (d.get('href')or'').startswith('#identity-'):
            self.links.append(d.get('href'))
        if tag in ('button','select','span') and 'data-review' in ' '.join(d):
            for key in ('data-review-filter','data-review-compare','data-review-reset','data-review-count'):
                if key in d:self.controls[key]=d
        if tag=='script' and d.get('src')=='/assets/identity-workbench.js':self.has_script=True

def audit():
    issues=[]
    document=Page()
    document.feed((SITE/'identity-review/index.html').read_text(encoding='utf8'))
    by_slug={c.get('data-review-product'):c for c in document.cards}
    if len(document.cards)!=7 or set(by_slug)!=set(GROUPS):
        issues.append('Wrong count or unknown candidate cards')
    for slug,category in GROUPS.items():
        c=by_slug.get(slug,{})
        if c.get('data-review-category')!=category:issues.append(slug+': wrong semantic filter grouping')
        if c.get('id')!='identity-'+slug:issues.append(slug+': invalid deep-link target')
        if c.get('data-review-status')!='candidate':issues.append(slug+': silently promoted beyond candidate')
        if document.links.count('#identity-'+slug)!=1:issues.append(slug+': missing or duplicate permalink')
    if set(document.controls)!={'data-review-filter','data-review-compare','data-review-reset','data-review-count'}:
        issues.append('Missing accessible workbench controls')
    if document.controls.get('data-review-compare',{}).get('aria-pressed')!='false':
        issues.append('Compare button missing truthful default pressed state')
    if document.controls.get('data-review-count',{}).get('aria-live')!='polite':
        issues.append('Filter result count missing accessible announcement')
    if not document.has_script:issues.append('Local review-only enhancement script missing')
    script=SITE/'assets/identity-workbench.js'
    if not script.is_file():issues.append('Local script file missing')
    else:
        contents=script.read_text(encoding='utf8')
        for prohibited in ('fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage', 'sessionStorage',
                           'document.cookie', 'eval(', 'new Function(', 'navigator.clipboard'):
            if prohibited in contents:issues.append('Unexpected data/network capability: '+prohibited)
        if 'data-review-status="candidate"' not in contents:
            issues.append('Script does not explicitly restrict to unapproved candidate cards')
    return issues

if __name__=='__main__':
    errors=audit()
    if errors:
        print('FAIL review workbench',*errors,sep='\n - ')
        sys.exit(1)
    print('PASS seven original candidate groups, comparison control, accessible count, local-only enhancement and deep links')
