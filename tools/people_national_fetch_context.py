#!/usr/bin/env python3
"""Fetch wikitext of context articles (2026 election, candidate lists, cabinet) into raw/people/national/context/."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people_national_wiki import api
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'people', 'national', 'context')
for t in sys.argv[1:]:
    fn = os.path.join(D, t.replace(' ', '_').replace('/', '_') + '.wikitext')
    if os.path.exists(fn): continue
    d = api({'action': 'parse', 'page': t, 'prop': 'wikitext', 'redirects': 1})
    if 'parse' not in d: print('FAIL', t, d.get('error')); continue
    open(fn, 'w').write(d['parse']['wikitext']['*']); print(t, len(d['parse']['wikitext']['*']))
