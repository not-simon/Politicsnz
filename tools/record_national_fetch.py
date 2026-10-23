#!/usr/bin/env python3
"""Fetch Wikipedia plaintext extracts + wikitext for National Party track-record research.
Usage: python3 -I tools/record_national_fetch.py "Title 1" "Title 2" ...
Saves to raw/record/national/<Title>.txt (plaintext extract) and .wikitext"""
import sys, json, urllib.request, urllib.parse, os, time
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'record', 'national')
UA = {'User-Agent': 'PoliticsNZResearch/1.0 (personal research)'}
def get(params):
    url = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode(params)
    for i in range(6):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60)); time.sleep(2); return r
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(10 * (i + 1))
    raise SystemExit('rate limited')
for t in sys.argv[1:]:
    if os.path.exists(os.path.join(OUT, t.replace(' ', '_').replace('/', '_') + '.wikitext')): continue
    fn = t.replace(' ', '_').replace('/', '_')
    d = get({'action': 'query', 'prop': 'extracts', 'explaintext': 1, 'titles': t, 'format': 'json', 'redirects': 1})
    page = next(iter(d['query']['pages'].values()))
    open(os.path.join(OUT, fn + '.txt'), 'w').write(page.get('extract', '') or '')
    d = get({'action': 'parse', 'page': t, 'prop': 'wikitext', 'format': 'json', 'redirects': 1})
    open(os.path.join(OUT, fn + '.wikitext'), 'w').write(d.get('parse', {}).get('wikitext', {}).get('*', ''))
    print(t, len(page.get('extract', '') or ''))
