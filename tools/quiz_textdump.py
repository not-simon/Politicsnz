#!/usr/bin/env python3
"""Dump readable text from raw party HTML/PDF downloads (minor parties) for quiz position research.
Usage: python3 -I tools/quiz_textdump.py <party-docs-subdir> <outdir>"""
import sys, os, subprocess, glob
from bs4 import BeautifulSoup
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
for f in sorted(glob.glob(os.path.join(src, '**', '*'), recursive=True)):
    if os.path.isdir(f): continue
    name = os.path.relpath(f, src).replace('/', '_')
    if f.endswith('.html'):
        s = BeautifulSoup(open(f, encoding='utf-8', errors='replace').read(), 'html.parser')
        for t in s(['script', 'style', 'noscript', 'svg']): t.decompose()
        txt = '\n'.join(l.strip() for l in s.get_text('\n').splitlines() if l.strip())
    elif f.endswith('.pdf'):
        txt = subprocess.run(['pdftotext', '-layout', f, '-'], capture_output=True, text=True).stdout
    else:
        continue
    open(os.path.join(out, name + '.txt'), 'w').write(txt)
    print(name, len(txt))
