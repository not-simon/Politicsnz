#!/usr/bin/env python3
"""Fetch Wikipedia plaintext extracts + wikitext for Green / Te Pati Maori track-record research.
Usage: python3 -I tools/record_green_tpm_fetch.py "Title 1" "Title 2" ...
Writes raw/record/green-tpm/<slug>.txt (extract) and .wiki (wikitext)."""
import sys, json, re, urllib.request, urllib.parse, os, time, urllib.error
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'record', 'green-tpm')
UA = {'User-Agent': 'PoliticsNZResearch/1.0 (personal research)'}
def get(params):
    url = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode(params)
    for i in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(5 * (i + 1))
    raise RuntimeError('rate limited: ' + url)
for t in sys.argv[1:]:
  try:
    slug = re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
    d = get({'action': 'query', 'prop': 'extracts', 'explaintext': 1, 'titles': t, 'format': 'json', 'redirects': 1})
    page = next(iter(d['query']['pages'].values()))
    txt = page.get('extract', '')
    w = get({'action': 'parse', 'page': t, 'prop': 'wikitext', 'format': 'json', 'redirects': 1})
    wt = w.get('parse', {}).get('wikitext', {}).get('*', '')
    open(os.path.join(OUT, slug + '.txt'), 'w').write(txt)
    open(os.path.join(OUT, slug + '.wiki'), 'w').write(wt)
    print(t, len(txt), len(wt), flush=True)
    time.sleep(2)
  except Exception as e:
    print('FAIL', t, e, flush=True)
