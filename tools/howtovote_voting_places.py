#!/usr/bin/env python3
"""Normalise the Electoral Commission's 2026 voting-place data (as loaded by the official finder at map.vote.nz)
into data/guide/voting-places-2026.json.

Input : raw/howtovote/voting-places-2026.json  (copy of https://map.vote.nz/assets/map-data/locations-<hash>.json,
        captured 23 Oct 2026 with tools/howtovote_map_probe.js)
Output: data/guide/voting-places-2026.json
Run   : python3 -I tools/howtovote_voting_places.py
"""
import json, os, sys, datetime, collections

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = os.path.join(ROOT, 'raw', 'howtovote', 'voting-places-2026.json')
OUT = os.path.join(ROOT, 'data', 'guide', 'voting-places-2026.json')
SOURCE_URL = 'https://map.vote.nz/assets/map-data/locations-092ace171546d5fc.json'
FINDER_URL = 'https://map.vote.nz/voting-places'
ELECTION_DAY = '2026-11-07'

d = json.load(open(SRC, encoding='utf-8'))
E = {int(k): v for k, v in d['electorates'].items()}
ACC = {int(k): v['code'] for k, v in d['accessibility'].items()}  # 1 NONE, 2 PARTIAL, 3 FULL

def hhmm(t):
    return t[:5]

places = []
for l in d['locations']:
    lon, lat = l['coordinates']
    adv, eday = [], None
    for date, o, c in sorted(l['hours']):
        if date == ELECTION_DAY:
            eday = {'open': hhmm(o), 'close': hhmm(c)}
        else:
            adv.append({'date': date, 'open': hhmm(o), 'close': hhmm(c)})
    home = [E[e]['name'] for e in l['electorates'] if E[e]['vpType'] == 'Home']
    shared = [E[e]['name'] for e in l['electorates'] if E[e]['vpType'] == 'Shared']
    places.append({
        'id': l['id'],
        'name': l['name'],
        'address': ', '.join(x for x in [l['address'], l['suburb']] if x),
        'suburb': l['suburb'],
        'lat': round(lat, 6),
        'lon': round(lon, 6),
        'electorates': home + shared,
        'home_electorates': home,
        'advance_hours': adv,
        'election_day': eday,
        'accessible': ACC.get(l['accessibility']) == 'FULL',
        'accessibility': ACC.get(l['accessibility'], 'UNKNOWN').lower(),
        'whare_poti_maori': bool(l['whare']),
        'reo_rua_bilingual': bool(l['maori']),
        'source': FINDER_URL,
    })

places.sort(key=lambda p: (p['name'], p['id']))
dates = collections.Counter(h['date'] for p in places for h in p['advance_hours'])
out = {
    '_about': ('Voting places for the 2026 New Zealand General Election, normalised from the data file the Electoral '
               'Commission\'s official voting-place finder (map.vote.nz) loads. Field meanings are inferred from the file and '
               'checked against the Commission\'s 7 October 2026 media release; the Commission does not publish a data dictionary. '
               '"whare_poti_maori" = flagged "whare" in the source (Whare Pōti Māori voting places: marae, kura, wānanga and other '
               'spaces chosen for their significance to Māori voters); "reo_rua_bilingual" = flagged "maori" in the source (we read '
               'this as the bilingual/reo rua places where voting can be done in te reo Māori or English; 63 are flagged vs 67 '
               'announced, so treat as indicative). "accessible" is true only for places the Commission codes FULL; PARTIAL and NONE '
               'are in "accessibility". Hours are local NZ time. Always check the official finder before travelling: hours can change.'),
    'as_of': datetime.date.today().isoformat(),
    'election_day': ELECTION_DAY,
    'source': SOURCE_URL,
    'source_captured': '2026-10-23',
    'official_finder': FINDER_URL,
    'official_finder_notes': ('The finder is a client-side map: it loads the whole dataset and filters in the browser. It accepts no '
                              'documented address or electorate query parameters (tested ?electorate=... on 23 Oct 2026: page loads the '
                              'default view). Deep-link to https://map.vote.nz (or vote.nz/2026-general-election/voting-in-the-election/'
                              'find-a-voting-place for the list-by-electorate view) and let the voter type their address, or use this '
                              'file to compute nearest places client-side.'),
    'licence': ('Not stated on the data file or the finder page. vote.nz content is published by the Electoral Commission (Crown '
                'entity); no Creative Commons or other open licence statement was found on vote.nz, map.vote.nz or elections.nz on '
                '23 Oct 2026. Treat as Commission copyright: factual voting-place details are reproduced here for voter information '
                'with attribution; confirm terms with the Commission (enquiries@elections.govt.nz) before any other reuse.'),
    'counts': {
        'places': len(places),
        'open_election_day': sum(1 for p in places if p['election_day']),
        'open_during_advance_voting': sum(1 for p in places if p['advance_hours']),
        'open_26_october': dates.get('2026-10-26', 0),
        'fully_accessible': sum(1 for p in places if p['accessible']),
        'whare_poti_maori': sum(1 for p in places if p['whare_poti_maori']),
        'reo_rua_bilingual_flag': sum(1 for p in places if p['reo_rua_bilingual']),
        'electorates': len({n for p in places for n in p['electorates']}),
    },
    'cross_check': [
        {'claim': 'More than 2,300 voting places open on election day; 207 open on Monday 26 October; 1,679 fully accessible; '
                  'more than 220 Whare Pōti Māori places incl. 67 bilingual (reo rua)',
         'source': 'https://elections.nz/media-and-news/2026/voting-places-announced-for-2026-election (7 Oct 2026) and '
                   'https://elections.nz/media-and-news/2026/voting-starts-on-monday (22 Oct 2026)',
         'in_this_file': 'see counts; small differences reflect updates to the finder data since the releases'},
    ],
    'places': places,
}
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(out['counts'], indent=1), '->', OUT)
