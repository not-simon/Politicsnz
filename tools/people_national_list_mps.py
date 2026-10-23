#!/usr/bin/env python3
"""Extract National Party MPs from raw Wikipedia wikitext of the 50th-54th Parliament articles.
Writes raw/people/national/mps.json: {wiki_title: {name, parliaments:[..]}}"""
import re, json, os, collections
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'people', 'national')
out = collections.OrderedDict()
for n in range(50, 55):
    w = open(os.path.join(D, 'parliaments', f'{n}.wikitext')).read()
    for row in re.split(r'\n\|-', w):
        m = re.search(r'(party color cell\|\s*(New Zealand )?National|bgcolor=\{\{party color\|New Zealand National Party\}\})', row)
        if not m: continue
        rest = re.sub(r'\[\[File:[^\]]*\]\]', '', row[m.end():])
        rest = re.sub(r'\{\{font colou?r\|[^|}]*\|([^}]*)\}\}', r'\1', rest)
        l = None
        for l in re.finditer(r'\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]', rest):
            if not re.search(r'electorate|Minister|Speaker|Party|Parliament|Leader|Whip|List|list|Committee|Ministry|Government|Prime|Attorney|Commission', l.group(1)): break
        else: l = None
        if not l: continue
        title = l.group(1).strip(); name = (l.group(2) or title).strip()
        e = out.setdefault(title, {'name': name, 'parliaments': []})
        if n not in e['parliaments']: e['parliaments'].append(n)
json.dump(out, open(os.path.join(D, 'mps.json'), 'w'), indent=1, ensure_ascii=False)
for t, e in out.items(): print(t, '|', e['name'], e['parliaments'])
print(len(out))
