#!/usr/bin/env python3
"""For each National MP (raw/people/national/mps.json) + extra titles, fetch Wikipedia wikitext, URL and lead image
(pageimages) in batches of 40, then Commons/enwiki imageinfo (extmetadata, 400px thumb) in batches.
Saves raw/people/national/wiki/<slug>.json (wikitext + plain text made with mwparserfromhell).
Usage: python3 -I tools/people_national_fetch_mps.py [extra "Wiki Title" ...]"""
import json, os, sys, re, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people_national_wiki import api
import mwparserfromhell
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw', 'people', 'national')
os.makedirs(os.path.join(D, 'wiki'), exist_ok=True)
SKIP = {'Kanwaljit Singh Bakshi', 'Christopher Finlayson', 'Chris Bishop (politician)'}
def slugify(name):
    s = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    s = re.sub(r'\([^)]*\)', '', s).lower().replace("'", '')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')
def plain(wt):
    wt = re.sub(r'<ref[^>/]*/>', '', wt); wt = re.sub(r'<ref.*?</ref>', '', wt, flags=re.S)
    return re.sub(r'\n{3,}', '\n\n', mwparserfromhell.parse(wt).strip_code())
mps = json.load(open(os.path.join(D, 'mps.json')))
titles = [t for t in mps if t not in SKIP] + sys.argv[1:]
todo = [t for t in titles if not os.path.exists(os.path.join(D, 'wiki', slugify(t) + '.json'))]
for i in range(0, len(todo), 40):
    batch = todo[i:i + 40]
    q = api({'action': 'query', 'titles': '|'.join(batch), 'redirects': 1, 'prop': 'pageimages|info|revisions',
             'piprop': 'name', 'inprop': 'url', 'rvprop': 'content|timestamp', 'rvslots': 'main'})
    norm = {x['from']: x['to'] for x in q['query'].get('normalized', [])}
    redir = {x['from']: x['to'] for x in q['query'].get('redirects', [])}
    pages = {p['title']: p for p in q['query']['pages'].values()}
    recs = []
    for t in batch:
        tt = norm.get(t, t); tt = redir.get(tt, tt); page = pages.get(tt, {})
        wt = page.get('revisions', [{}])[0].get('slots', {}).get('main', {}).get('*', '')
        recs.append({'query_title': t, 'title': page.get('title'), 'url': page.get('fullurl'), 'slug': slugify(t),
                     'pageimage': page.get('pageimage'), 'wikitext': wt, 'text': plain(wt),
                     'revision_timestamp': page.get('revisions', [{}])[0].get('timestamp')})
    files = sorted({r['pageimage'] for r in recs if r['pageimage']})
    info = {}
    for host in ('commons.wikimedia.org', 'en.wikipedia.org'):
        need = [f for f in files if f not in info]
        for j in range(0, len(need), 40):
            ii = api({'action': 'query', 'titles': '|'.join('File:' + f for f in need[j:j + 40]), 'prop': 'imageinfo',
                      'iiprop': 'url|extmetadata|size', 'iiurlwidth': 400}, host=host)
            nm = {x['to']: x['from'] for x in ii['query'].get('normalized', [])}
            for p in ii['query']['pages'].values():
                if p.get('imageinfo'):
                    f = p['title'].split(':', 1)[1].replace(' ', '_')
                    info[f] = dict(p['imageinfo'][0], host=host)
    for r in recs:
        if r['pageimage']: r['imageinfo'] = info.get(r['pageimage'])
        json.dump(r, open(os.path.join(D, 'wiki', r['slug'] + '.json'), 'w'), ensure_ascii=False, indent=1)
        print(r['slug'], r['title'], len(r['text']), r['pageimage'], bool(r.get('imageinfo')), flush=True)
