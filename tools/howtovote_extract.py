#!/usr/bin/env python3
"""Dump the main text of fetched Commission pages (raw/howtovote/*.html) to raw/howtovote/txt/<name>.txt for checking.
Run with: python3 -I tools/howtovote_extract.py [name ...]"""
import sys, os, re
from bs4 import BeautifulSoup
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'howtovote')
os.makedirs(os.path.join(base, 'txt'), exist_ok=True)
names = sys.argv[1:] or [f[:-5] for f in sorted(os.listdir(base)) if f.endswith('.html')]
for n in names:
    p = os.path.join(base, n + '.html')
    if not os.path.exists(p):
        print('missing', n); continue
    s = BeautifulSoup(open(p, encoding='utf-8', errors='replace').read(), 'html.parser')
    for t in s(['script', 'style', 'noscript', 'svg']): t.decompose()
    main = s.find('main') or s.find(id='content') or s.body or s
    for nav in main.find_all(['nav', 'header', 'footer']): nav.decompose()
    lines = []
    for el in main.find_all(['h1','h2','h3','h4','p','li','td','th','summary','dt','dd']):
        t = el.get_text(' ', strip=True)
        if not t: continue
        if el.name.startswith('h'): t = '#'*int(el.name[1]) + ' ' + t
        elif el.name == 'li': t = '- ' + t
        for a in el.find_all('a', href=True):
            h = a['href']
            if h.startswith('/'): h = 'https://vote.nz' + h if 'vote' in n or n.startswith(('eligible','enrol','maori','key','ge-','what','need','cant','find','overseas','easyvote','glossary','accessible','communications','free','contact','unpublished','other','telephone')) else 'https://elections.nz' + h
            t += f' [{a.get_text(" ", strip=True)[:40]} -> {h}]'
        lines.append(t)
    out = '\n'.join(dict.fromkeys(lines))
    open(os.path.join(base, 'txt', n + '.txt'), 'w').write(out)
    print(n, len(out))
