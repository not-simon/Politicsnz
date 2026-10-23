#!/usr/bin/env python3
"""Official 2026 National list ranks (Electoral Commission, vote.nz party lists, 9 Oct 2026, cross-checked with
Wikipedia 'Party lists in the 2026 New Zealand general election'). Writes raw/people/national/ec/national-list-2026.json"""
import re, os, json, unicodedata
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'people', 'national')
w = open(os.path.join(D, 'context', 'Party_lists_in_the_2026_New_Zealand_general_election.wikitext')).read()
sec = w[w.find('===National Party==='):w.find('===New Zealand First===')]
folders = set(os.listdir(os.path.join(D, '..', '..', '..', 'parties', 'national', 'people')))
out = {}
for m in re.finditer(r'rank = (\d+) \| lastname = [^|]*\| fullname = ([^|}]*(?:\|[^|}\]]*\]\])?)', sec):
    full = m.group(2); full = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', full).strip()
    s = unicodedata.normalize('NFKD', full).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    s = {'robin-atwal': 'robin-atwall'}.get(s, s)
    if s not in folders: print('no folder', s)
    out[s] = int(m.group(1))
json.dump(out, open(os.path.join(D, 'ec', 'national-list-2026.json'), 'w'), indent=1)
print(len(out))
