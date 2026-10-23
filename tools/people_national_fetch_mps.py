#!/usr/bin/env python3
"""For each National MP (raw/people/national/mps.json) fetch Wikipedia plaintext extract, wikitext,
lead image (pageimages) and Commons/enwiki imageinfo extmetadata. Saves raw/people/national/wiki/<slug>.json
Usage: python3 -I tools/people_national_fetch_mps.py [extra "Wiki Title" ...]"""
import json, os, sys, re, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people_national_wiki import api
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'people', 'national')
os.makedirs(os.path.join(D, 'wiki'), exist_ok=True)
SKIP = {'Kanwaljit Singh Bakshi', 'Christopher Finlayson', 'Chris Bishop (politician)'}
def slugify(name):
    s = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    s = re.sub(r'\([^)]*\)', '', s).lower().replace("'", '')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')
mps = json.load(open(os.path.join(D, 'mps.json')))
titles = [t for t in mps if t not in SKIP] + sys.argv[1:]
for t in titles:
    slug = slugify(t)
    fn = os.path.join(D, 'wiki', slug + '.json')
    if os.path.exists(fn): continue
    q = api({'action': 'query', 'titles': t, 'redirects': 1, 'prop': 'extracts|pageimages|info|revisions',
             'explaintext': 1, 'piprop': 'name|original', 'inprop': 'url', 'rvprop': 'content|timestamp', 'rvslots': 'main'})
    page = next(iter(q['query']['pages'].values()))
    rec = {'query_title': t, 'title': page.get('title'), 'url': page.get('fullurl'), 'slug': slug,
           'extract': page.get('extract', ''), 'pageimage': page.get('pageimage'),
           'wikitext': page.get('revisions', [{}])[0].get('slots', {}).get('main', {}).get('*', ''),
           'revision_timestamp': page.get('revisions', [{}])[0].get('timestamp')}
    if rec['pageimage']:
        for host in ('commons.wikimedia.org', 'en.wikipedia.org'):
            ii = api({'action': 'query', 'titles': 'File:' + rec['pageimage'], 'prop': 'imageinfo',
                      'iiprop': 'url|extmetadata|size', 'iiurlwidth': 400}, host=host)
            p = next(iter(ii['query']['pages'].values()))
            if p.get('imageinfo'):
                rec['imageinfo'] = p['imageinfo'][0]; rec['imageinfo_host'] = host; break
    json.dump(rec, open(fn, 'w'), ensure_ascii=False, indent=1)
    print(slug, len(rec['extract']), rec['pageimage'], flush=True)
