#!/usr/bin/env python3
"""List citation URLs in a downloaded Wikipedia article whose URL matches a regex (research helper).
Usage: python3 -I tools/people_national_refs.py <slug> <regex>"""
import json, os, re, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'people', 'national', 'wiki')
w = json.load(open(os.path.join(D, sys.argv[1] + '.json')))['wikitext']
seen = []
for u in re.findall(r'url\s*=\s*([^\s|}]+)', w) + re.findall(r'\[(https?://[^\s\]]+)', w):
    if 'archive.org' in u: continue
    if re.search(sys.argv[2], u, re.I) and u not in seen: seen.append(u)
print('\n'.join(seen))
