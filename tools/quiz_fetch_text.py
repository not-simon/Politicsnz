#!/usr/bin/env python3
"""Fetch a URL with curl (via proxy), cache raw HTML in raw/quiz/pages/, print readable text (optionally grep).
Usage: python3 -I tools/quiz_fetch_text.py <url> [regex] [context_chars]"""
import sys, os, re, subprocess, hashlib
from bs4 import BeautifulSoup
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'raw/quiz/pages'); os.makedirs(D, exist_ok=True)
url = sys.argv[1]
name = re.sub(r'[^A-Za-z0-9]+', '_', url.split('//', 1)[-1])[:120] + '_' + hashlib.md5(url.encode()).hexdigest()[:6] + '.html'
p = os.path.join(D, name)
if not os.path.exists(p) or os.path.getsize(p) < 500:
    subprocess.run(['curl', '-sS', '-L', '--max-time', '40', '-A',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141 Safari/537.36',
                    '-o', p, url])
html = open(p, encoding='utf-8', errors='replace').read()
s = BeautifulSoup(html, 'html.parser')
for t in s(['script', 'style', 'noscript', 'svg', 'nav', 'footer', 'header']): t.decompose()
txt = re.sub(r'\s*\n\s*', '\n', s.get_text('\n'))
if len(sys.argv) > 2:
    ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    last = -1
    for m in re.finditer(sys.argv[2], txt, re.I):
        if m.start() < last: continue
        last = m.end() + ctx
        print('...', txt[max(0, m.start()-ctx):m.end()+ctx].replace('\n', ' '), '...\n')
else:
    print(txt[:8000])
