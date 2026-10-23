#!/usr/bin/env python3
"""Fetch plain-text extract of an English Wikipedia article via the API (cached in raw/quiz/wiki/) and grep it.
Usage: python3 -I tools/quiz_wiki.py "<Title>" [regex] [ctx]"""
import sys, os, re, json, urllib.parse, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'raw/quiz/wiki'); os.makedirs(D, exist_ok=True)
title = sys.argv[1]
p = os.path.join(D, re.sub(r'[^A-Za-z0-9]+', '_', title) + '.txt')
if not os.path.exists(p):
    u = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&redirects=1&format=json&titles=' + urllib.parse.quote(title)
    r = subprocess.run(['curl', '-sS', '-A', 'PoliticsNZResearch/1.0 (personal research)', u], capture_output=True, text=True).stdout
    pages = json.loads(r)['query']['pages']
    txt = next(iter(pages.values())).get('extract', '')
    open(p, 'w').write('SOURCE: https://en.wikipedia.org/wiki/' + title.replace(' ', '_') + '\n' + txt)
txt = open(p).read()
if len(sys.argv) > 2:
    ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 250; last = -1
    for m in re.finditer(sys.argv[2], txt, re.I):
        if m.start() < last: continue
        last = m.end() + ctx
        print('...', txt[max(0, m.start()-ctx):m.end()+ctx].replace('\n', ' '), '...\n')
else:
    print(txt[:6000])
