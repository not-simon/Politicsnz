#!/usr/bin/env python3 -I
"""dg.py PARTY REGEX [N snippets per doc=2] [CTX=200] : grep party documents, print url + snippets."""
import re, sys, os, glob
party = sys.argv[1]; rx = re.compile(sys.argv[2], re.I)
n = int(sys.argv[3]) if len(sys.argv) > 3 else 2
ctx = int(sys.argv[4]) if len(sys.argv) > 4 else 200
base = f'/home/user/Politicsnz/parties/{party}/policies/documents'
for f in sorted(glob.glob(f'{base}/*.md')):
    t = open(f, errors='replace').read()
    hits = list(rx.finditer(t))
    if not hits: continue
    m = re.search(r'^source_url:\s*(.*)$', t, re.M); url = m.group(1).strip() if m else '?'
    m = re.search(r'^title:\s*(.*)$', t, re.M); title = m.group(1).strip() if m else ''
    m = re.search(r'^retrieved:\s*(.*)$', t, re.M); ret = m.group(1).strip() if m else ''
    print(f"\n=== {os.path.basename(f)} | {title} | {url} | {len(hits)} hits")
    last=-1; shown=0
    for h in hits:
        if h.start() < last: continue
        a=max(0,h.start()-ctx); b=min(len(t),h.end()+ctx)
        print('   …'+re.sub(r'\s+',' ',t[a:b])+'…'); last=b; shown+=1
        if shown>=n: break
