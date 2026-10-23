#!/usr/bin/env python3 -I
"""ps.py PARTY REGEX [--docs] [--ctx N]  : search policies.json (and documents) of a party."""
import json, re, sys, os, glob
party = sys.argv[1]; rx = re.compile(sys.argv[2], re.I)
docs = '--docs' in sys.argv
ctx = 220
for i,a in enumerate(sys.argv):
    if a == '--ctx': ctx = int(sys.argv[i+1])
base = f'/home/user/Politicsnz/parties/{party}/policies'
pol = json.load(open(f'{base}/policies.json'))
n=0
for p in pol:
    s = json.dumps(p, ensure_ascii=False)
    if rx.search(s):
        n+=1
        print(f"## {p.get('id')} | {p.get('statement')}  [{','.join(p.get('topics',[]))}]")
        sm = p.get('summary') or {}
        for k in ('why','how'):
            if sm.get(k): print(f"   {k}: {sm[k]}")
        for src in p.get('sources',[])[:3]:
            print(f"   src: {src.get('url')}  doc={src.get('document')}")
print(f"-- {n} policies matched")
if docs:
    for f in sorted(glob.glob(f'{base}/documents/*.md')):
        t = open(f, errors='replace').read()
        hits = list(rx.finditer(t))
        if hits:
            print(f"\n=== {os.path.basename(f)} ({len(hits)} hits)")
            shown=0
            last=-1
            for m in hits:
                if m.start() < last: continue
                a=max(0,m.start()-ctx); b=min(len(t), m.end()+ctx)
                print('   …'+re.sub(r'\s+',' ',t[a:b])+'…')
                last=b; shown+=1
                if shown>=6: break
