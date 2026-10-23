#!/usr/bin/env python3
"""Grep minor-party policy texts (parties/<p>/policies/documents + raw/quiz/<p>) for a regex, printing file + snippet.
Usage: python3 -I tools/quiz_minor_grep.py <regex> [party ...]"""
import sys, os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MINOR = ['nz-loyal','nz-outdoors-freedom','legalise-cannabis','animal-justice','alliance','conservative','womens-rights','vision-nz','free-palestine','te-tai-tokerau-party']
pat = re.compile(sys.argv[1], re.I); parties = sys.argv[2:] or MINOR
for p in parties:
    files = glob.glob(f'{ROOT}/parties/{p}/policies/documents/*.md') + glob.glob(f'{ROOT}/raw/quiz/{p}/*.txt')
    for f in sorted(files):
        t = re.sub(r'\s+', ' ', open(f, errors='replace').read()); last = -1
        for m in pat.finditer(t):
            if m.start() < last: continue
            last = m.end() + 200
            print(f'[{p}] {os.path.basename(f)}: ...{t[max(0,m.start()-200):m.end()+200]}...')
