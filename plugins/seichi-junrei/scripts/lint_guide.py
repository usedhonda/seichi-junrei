#!/usr/bin/env python3
"""Basic automatic gate for self-contained mobile guide and input selection."""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images=[]
        self.links=[]
        self.inputs=[]
        self.ids=set()
        self.script_count=0
    def handle_starttag(self, tag, attributes):
        a=dict(attributes)
        if a.get('id'): self.ids.add(a['id'])
        if tag=='img': self.images.append(a)
        if tag=='a': self.links.append(a)
        if tag=='input': self.inputs.append(a)
        if tag=='script': self.script_count+=1

def lint(html_text, guide=None):
    issues=[]
    parser=Inspector()
    parser.feed(html_text)
    for key in ('name="viewport"', '<meta name="robots"', 'STORY PILGRIMAGE', 'home-episodes', 'data-bookmark', 'data-scene', 'data-day-panel', 'data-mission'):
        if key not in html_text: issues.append("Missing content: "+key)
    if not parser.images: issues.append('No images')
    for i in parser.images:
        if i.get('id') == 'full-art-img': continue
        if not i.get('src','').startswith('data:image/'): issues.append('Image is not embedded as data URI')
        if not i.get('alt'): issues.append('Missing alt text')
    for a in parser.links:
        href=a.get('href','')
        if not (href.startswith('#') or href.startswith('https://')): issues.append('Disallowed link: '+href[:50])
    if any(r in html_text for r in ('@@TITLE@@','@@HERO@@','@@SOURCES@@')): issues.append('Unreplaced template token')
    visible = re.sub(r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+', '', html_text)
    for pattern in [r'(?i)\b(?:PNR|booking reference|reservation number|予約番号|確認番号)\s*[:：#]?\s*[A-Z0-9-]{4,}',
                    r'(?i)(?:sk-[a-zA-Z0-9]{12,}|\b\w+@[a-zA-Z0-9.-]+\.[a-z]{2,})']:
        if re.search(pattern,visible): issues.append('Possible sensitive data in HTML')
    if guide:
        from render_guide import validate
        try: validate(guide)
        except ValueError as err: issues.append('Guide gate: '+str(err))
        for st in guide.get('stages',[]):
            if 'stage-'+st.get('id','') not in parser.ids: issues.append('Stage missing: '+st.get('id',''))
        if len(parser.images) < 2: issues.append('Image count is low; insert more original/cleared art')
    return issues,parser

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('html_file',type=Path)
    p.add_argument('--guide',type=Path)
    a=p.parse_args()
    text=a.html_file.read_text(encoding='utf-8')
    guide=json.loads(a.guide.read_text(encoding='utf-8')) if a.guide else None
    issues,parser=lint(text,guide)
    print('images:',len(parser.images),'links:',len(parser.links),'inputs:',len(parser.inputs),'scripts:',parser.script_count)
    if issues:
        print('\n'.join('FAIL: '+x for x in issues));sys.exit(1)
    print('PASS: structural, media, selection and privacy heuristic checks')

if __name__=='__main__':main()
