#!/usr/bin/env python3
"""Print a downloaded Wikipedia article as plain text with each citation shown inline as [url] (for research)."""
import json, os, re, sys
import mwparserfromhell as mw
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'people', 'national', 'wiki')
for slug in sys.argv[1:]:
    w = json.load(open(os.path.join(D, slug + '.json')))['wikitext']
    named = {}
    for m in re.finditer(r'<ref name="?([^">/]+)"?\s*>(.*?)</ref>', w, flags=re.S):
        u = re.search(r'url\s*=\s*([^\s|}]+)', m.group(2)) or re.search(r'\[(https?://\S+)', m.group(2))
        if u: named[m.group(1).strip()] = u.group(1)
    def rep(m):
        u = re.search(r'url\s*=\s*([^\s|}]+)', m.group(0)) or re.search(r'\[(https?://\S+)', m.group(0))
        return f' ⟨{u.group(1)}⟩' if u else ''
    w = re.sub(r'<ref[^>/]*>.*?</ref>', rep, w, flags=re.S)
    w = re.sub(r'<ref name="?([^">/]+)"?\s*/>', lambda m: f' ⟨{named.get(m.group(1).strip(), "")}⟩' if named.get(m.group(1).strip()) else '', w)
    w = re.sub(r'\{\{[Ii]nfobox.*?\n\}\}', '', w, count=1, flags=re.S)
    t = mw.parse(w).strip_code()
    t = re.sub(r'\n{3,}', '\n\n', t)
    t = t[:t.find('\nReferences\n')] if '\nReferences\n' in t else t
    print(f'===== {slug}\n{t}')
