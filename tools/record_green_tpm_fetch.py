#!/usr/bin/env python3
"""Fetch Wikipedia wikitext (via /wiki/<title>?action=raw, which avoided API rate limits) for the
Green / Te Pati Maori track-record research. Usage: python3 -I tools/record_green_tpm_fetch.py "Title" ...
Writes raw/record/green-tpm/<slug>.wiki. Wikipedia is used as a finding aid: claims are cited to the
underlying independent sources listed in each article's references where possible."""
import sys, re, urllib.request, urllib.parse, os, time, urllib.error
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'record', 'green-tpm')
UA = {'User-Agent': 'PoliticsNZResearch/1.0 (personal research)'}
for t in sys.argv[1:]:
    slug = re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
    url = 'https://en.wikipedia.org/wiki/' + urllib.parse.quote(t.replace(' ', '_')) + '?action=raw'
    for i in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                wt = r.read().decode('utf-8')
            m = re.match(r'#REDIRECT\s*\[\[([^\]]+)\]\]', wt, re.I)
            if m:
                url = 'https://en.wikipedia.org/wiki/' + urllib.parse.quote(m.group(1).split('#')[0].replace(' ', '_')) + '?action=raw'
                continue
            open(os.path.join(OUT, slug + '.wiki'), 'w').write(wt)
            print(t, len(wt), flush=True)
            break
        except urllib.error.HTTPError as e:
            print('ERR', t, e.code, flush=True)
            if e.code == 404: break
            time.sleep(4 * (i + 1))
    time.sleep(1)
