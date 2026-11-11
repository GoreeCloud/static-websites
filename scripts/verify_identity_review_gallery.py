#!/usr/bin/env python3
"""Offline review-only source/identity safety and exact imported asset checks."""
from __future__ import annotations
from pathlib import Path
import hashlib,json,re,struct,sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
MANIFEST=ROOT/'IDENTITY-REVIEW-SOURCES.json'
SLUGS=['goreeshield','wardveil','mesh','maps','projects','analytics','gateway']
NAMES=['app-icon.svg','symbol.svg','logo.svg','logo-dark.svg','artwork.svg','icon-16.png','icon-32.png']

def audit():
    problems=[]
    data=json.loads(MANIFEST.read_text())
    if data['products']!=SLUGS:problems.append('Product list/source order changed')
    if data['source_commit']!='c48ebf7e9a098184e879445e6fe4aec9171fa7c3':
        problems.append('Unreviewed source commit')
    if 'not official' not in data['status']:problems.append('Review status incorrectly official')
    expected={f'assets/identity-review/{slug}/{name}' for slug in SLUGS for name in NAMES}
    recorded={entry['web'] for entry in data['files']}
    if recorded!=expected or len(data['files'])!=49:
        problems.append('Missing or extra imported identity files')
    digest_list=set()
    for entry in data['files']:
        local=SITE/entry['web']
        if entry['status']!='candidate-only':
            problems.append('Image promoted to official without review: '+entry['web'])
        if local.is_symlink() or not local.is_file():
            problems.append('File missing, symlinked or unsafe: '+entry['web'])
            continue
        bytes_=local.read_bytes()
        if hashlib.sha256(bytes_).hexdigest()!=entry['sha256']:
            problems.append('Byte mismatch: '+entry['web'])
        if entry['web'].endswith('.svg'):
            if re.search(rb'<script|<foreignObject|<image\b|xlink:href|href\s*=\s*[\x22\x27]https?:|url\(\s*https?:',bytes_,re.I):
                problems.append('Untrusted SVG feature: '+entry['web'])
            try:
                root=ET.fromstring(bytes_)
                if root.tag!='{http://www.w3.org/2000/svg}svg':
                    problems.append('Non-SVG vector root: '+entry['web'])
                if not root.find('{http://www.w3.org/2000/svg}title') is not None:
                    problems.append('Missing accessible title: '+entry['web'])
            except ET.ParseError:
                problems.append('SVG parse failure: '+entry['web'])
        elif entry['web'].endswith('.png'):
            if bytes_[:8]!=b'\x89PNG\r\n\x1a\n':
                problems.append('PNG signature invalid: '+entry['web'])
            elif len(bytes_)>=24:
                width,height=struct.unpack('>II',bytes_[16:24])
                n=16 if entry['web'].endswith('icon-16.png') else 32
                if (width,height)!=(n,n):
                    problems.append('PNG size mismatch: '+entry['web'])
            if entry['web'].endswith('icon-16.png'):
                digest_list.add(hashlib.sha256(bytes_).hexdigest())
    if len(digest_list)!=7:problems.append('Small app marks are not distinct')
    page=(SITE/'identity-review/index.html').read_text()
    if page.count('data-review-status="candidate"')!=7:
        problems.append('Review page has wrong candidate count/status')
    for slug in SLUGS:
        if page.count('data-review-product="'+slug+'"')!=1:
            problems.append('Missing or duplicate gallery card: '+slug)
        for name in NAMES:
            if '/assets/identity-review/'+slug+'/'+name not in page:
                problems.append('Asset is not referenced by gallery: '+slug+'/'+name)
    for marker in ['name="robots" content="noindex','not been approved as official',
                   'GoreeCloud\'s permanent blue G','View source SVG']:
        if marker not in page:problems.append('Review-only disclosure missing: '+marker)
    if '/identity-review/' not in (SITE/'products/index.html').read_text():
        problems.append('No controlled entry point from Products')
    return problems

if __name__=='__main__':
    errors=audit()
    if errors:
        print('BLOCKED review gallery:',*errors,sep='\n - ')
        sys.exit(1)
    print('PASS seven unapproved candidate gallery cards, 49 source-pinned local assets, valid PNG/SVG and review-only controls')
