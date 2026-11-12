#!/usr/bin/env python3
"""Offline, strict source-boundary checks for unapproved Signalform v2 comparison."""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
META=ROOT/'SIGNALFORM-V2-SOURCES.json'
SLUGS=['goreeshield','wardveil','mesh','maps','projects','analytics','gateway']
FILES=['app-icon.svg','symbol.svg','logo.svg','logo-dark.svg','artwork.svg','icon-16.png','icon-32.png']
COMMIT='0807d8719b13858394ba62637629c85d314bdf7a'

def audit():
    errors=[]
    data=json.loads(META.read_text())
    if data.get('source_commit')!=COMMIT:errors.append('Unexpected candidate source commit')
    if data.get('products')!=SLUGS:errors.append('Product coverage drift')
    if 'unapproved' not in data.get('status','') or 'not official' not in data.get('status',''):
        errors.append('Candidate status disclosure missing')
    expected={f'assets/identity-signalform-v2/{s}/{name}' for s in SLUGS for name in FILES}
    actual={v['path'] for v in data.get('files',[])}
    if expected!=actual or len(data.get('files',[]))!=49:errors.append('Missing, duplicate, or unexpected candidate file')
    sixteen=set()
    for f in data.get('files',[]):
        rel=f.get('path','')
        target=SITE/rel
        if f.get('status')!='unapproved-candidate':
            errors.append(rel+': illicit approval status promotion')
        if target.is_symlink() or not target.is_file():
            errors.append(rel+': missing or symlink asset')
            continue
        binary=target.read_bytes()
        if hashlib.sha256(binary).hexdigest()!=f.get('sha256'):
            errors.append(rel+': source SHA mismatch')
        if rel.endswith('.svg'):
            if re.search(rb'<script|<foreignObject|<image\b|xlink:href|href\s*=\s*[\x22\x27]https?:|url\(\s*https?:',binary,re.I):
                errors.append(rel+': risky SVG features')
            try:
                doc=ET.fromstring(binary)
                if doc.tag!='{http://www.w3.org/2000/svg}svg':
                    errors.append(rel+': invalid SVG namespace')
                if doc.find('{http://www.w3.org/2000/svg}title') is None or doc.find('{http://www.w3.org/2000/svg}desc') is None:
                    errors.append(rel+': missing accessible SVG metadata')
            except ET.ParseError:
                errors.append(rel+': malformed source SVG')
        elif rel.endswith('.png'):
            if binary[:8]!=b'\x89PNG\r\n\x1a\n' or len(binary)<24:
                errors.append(rel+': invalid PNG signature')
            else:
                w,h=struct.unpack('>II',binary[16:24])
                wanted=16 if rel.endswith('icon-16.png') else 32
                if (w,h)!=(wanted,wanted):errors.append(rel+': wrong actual pixel size')
            if rel.endswith('icon-16.png'):sixteen.add(hashlib.sha256(binary).hexdigest())
    if len(sixteen)!=7:errors.append('Seven redesigned 16px icons are not distinct')
    p=SITE/'identity-review-v2/index.html'
    if not p.is_file():errors.append('Missing review route')
    else:
        page=p.read_text()
        for marker in ('All seven designs are proposals.','permanent GoreeCloud G','not official','Before','Redesigned','/identity-review/'):
            if marker not in page:errors.append('Review-only disclosure absent: '+marker)
        for s in SLUGS:
            if page.count('data-signalform-identity="'+s+'"')!=1:errors.append('Missing/duplicated product comparison: '+s)
            if page.count('id="compare-'+s+'"')!=1:errors.append('Missing product comparison anchor: '+s)
            if page.count('data-approval="pending"')!=7:errors.append('Candidate approval state changed')
            if f'/assets/identity-review/{s}/app-icon.svg' not in page:
                errors.append('Foundation v1 comparison no longer visible: '+s)
            for name in FILES:
                if f'/assets/identity-signalform-v2/{s}/{name}' not in page:
                    errors.append('New V2 asset omitted from comparison: '+s+'/'+name)
    if '/identity-review-v2/' not in (SITE/'identity-review/index.html').read_text():
        errors.append('Missing opt-in route from original gallery')
    if '/identity-review-v2/' in (SITE/'products/index.html').read_text():
        errors.append('Official Products catalog was repurposed for unapproved visual review')
    return errors

if __name__=='__main__':
    issues=audit()
    if issues:
        print('FAIL Signalform V2 preview',*issues,sep='\n - ')
        sys.exit(1)
    print('PASS Signalform v2: 49 exact imported source assets, 7 side-by-side v1/v2 proposals and unchanged official catalog')
