#!/usr/bin/env python3
"""Election-night results: read the Electoral Commission's public XML media feed and write data/results-2026.json.

Feed (documented in the Commission's 2026 media kit, p. 11): https://media.election.net.nz/xml/
  election.xml      national statistics + per-party votes and seats (party_seats = list, candidate_seats = electorate)
  parties.xml       p_no -> party name;  electorates.xml  e_no -> name;  candidates.xml  c_no -> "SURNAME, First", electorate, party
  eNN/eNN.xml       one file per electorate: statistics, party votes, candidate votes; final="true" when complete
Finished elections live at https://archive.electionresults.govt.nz/electionresults_<year>/xml/ with the same layout
(used as the test fixture: `--year 2023` must reproduce the official 2023 result in data/elections/2023.json).

Safety: nothing is written while the feed has no votes (before 7pm on 7 Nov the feed serves the full ballot with zeros),
so the site cannot show a "live count" of zeros, and the GitHub workflow that runs this only starts after 7pm NZDT.
Each run makes 75 small requests (max-age 30s on the server); the workflow runs every five minutes.

Usage:  python3 tools/results_feed.py                 # live 2026 feed -> data/results-2026.json
        python3 tools/results_feed.py --year 2023 --out /tmp/r2023.json --check   # fixture test against the archive
"""
import argparse, json, os, re, sys, time, unicodedata, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE = 'https://media.election.net.nz/xml/'
ARCHIVE = 'https://archive.electionresults.govt.nz/electionresults_{year}/xml/'
UA = 'BallotBookNZ/1.0 (+https://github.com/not-simon/Politicsnz; results reader)'
MAORI = {'hauraki-waikato', 'ikaroa-rawhiti', 'tamaki-makaurau', 'te-tai-hauauru', 'te-tai-tokerau', 'te-tai-tonga', 'waiariki'}

# Electoral Commission party names -> this archive's slugs. Anything not listed is matched on a normalised name,
# and failing that gets a slug made from its name (and is flagged in `unmapped_parties`).
PARTY_MAP = {
    'act new zealand': 'act', 'act': 'act',
    'new zealand first party': 'nz-first', 'new zealand first': 'nz-first', 'nz first': 'nz-first',
    'green party of aotearoa new zealand': 'green', 'green party': 'green',
    'new zealand labour party': 'labour', 'labour party': 'labour',
    'new zealand national party': 'national', 'national party': 'national',
    'te pati maori': 'te-pati-maori', 'maori party': 'te-pati-maori',
    'the opportunities party': 'opportunity', 'the opportunity party': 'opportunity', 'opportunities party (top)': 'opportunity', 'top': 'opportunity',
    'aotearoa legalise cannabis party': 'legalise-cannabis', 'animal justice party': 'animal-justice',
    'new conservatives': 'conservative', 'new conservative party': 'conservative', 'conservative party': 'conservative', 'newzeal': 'newzeal',
    'vision new zealand': 'vision-nz', 'vision nz': 'vision-nz', "women's rights party": 'womens-rights', 'womens rights party': 'womens-rights',
    'nz loyal': 'nz-loyal', 'new zealand loyal': 'nz-loyal', 'nz outdoors & freedom party': 'nz-outdoors-freedom', 'new zealand outdoors & freedom party': 'nz-outdoors-freedom',
    'outdoors & freedom': 'nz-outdoors-freedom', 'alliance': 'alliance', 'free palestine': 'free-palestine', 'free palestine party': 'free-palestine',
    'te tai tokerau party': 'te-tai-tokerau-party', 'freedoms new zealand': 'freedoms-nz', 'democracynz': 'democracy-nz', 'new zealand democracy': 'democracy-nz',
    'leighton baker party': 'leighton-baker', 'newzealand loyal': 'nz-loyal', 'new nation party': 'new-nation', 'the new zealand sovereignty party': 'nz-sovereignty',
    'new zealand people\'s party': 'nz-peoples', 'mana movement': 'mana', 'internet mana': 'internet-mana', 'united future': 'united-future', 'independent': 'independent',
}

def norm(s): return re.sub(r'\s+', ' ', unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower().replace('’', "'").strip())
def slugify(s): return re.sub(r'[^a-z0-9]+', '-', norm(s)).strip('-')

def fetch(url, cache_dir=None, retries=3):
    if cache_dir:
        p = Path(cache_dir) / re.sub(r'[^A-Za-z0-9._-]+', '_', url.split('/xml/')[-1] or 'index')
        if p.exists(): return p.read_bytes()
    last = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA, 'Cache-Control': 'no-cache'}), timeout=30) as r:
                data = r.read()
            if cache_dir: p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
            return data
        except Exception as e:  # noqa
            last = e; time.sleep(1.5 * (i + 1))
    raise last

def text(el, tag, default=None):
    x = el.find(tag)
    return (x.text or '').strip() if x is not None and x.text is not None else default
def num(el, tag):
    t = text(el, tag, '')
    try: return float(t) if '.' in t else int(t)
    except ValueError: return 0

def person_name(ec):  # "SWARBRICK, Chlöe" -> "Chlöe Swarbrick"
    if ',' in ec:
        sur, first = [x.strip() for x in ec.split(',', 1)]
        return f"{first} {sur.title() if sur.isupper() else sur}".strip()
    return ec.strip()

def load_slugs():
    e = json.load(open(ROOT / 'data' / 'electorates' / '2026.json'))
    E = e['electorates'] if isinstance(e, dict) else e
    by = {norm(x['name']): x['slug'] for x in E}
    g = json.load(open(ROOT / 'data' / 'guide' / 'parties.json')); G = g['parties'] if isinstance(g, dict) else g
    pm = json.load(open(ROOT / 'data' / 'parties-meta.json'))['parties']
    names = {}
    for p in G: names[norm(p['name'])] = p['slug']; names[norm(p.get('short_name') or '')] = p['slug']
    for s, m in pm.items(): names[norm(m.get('name') or '')] = s; names[norm(m.get('short') or '')] = s
    names.pop('', None)
    return by, names

def party_slug(name, names, unmapped):
    n = norm(name)
    if n in PARTY_MAP: return PARTY_MAP[n]
    if n in names: return names[n]
    n2 = re.sub(r'\b(the|party|of|aotearoa|new zealand|nz)\b', ' ', n); n2 = re.sub(r'\s+', ' ', n2).strip()
    for k, v in PARTY_MAP.items():
        if n2 and n2 == re.sub(r'\s+', ' ', re.sub(r'\b(the|party|of|aotearoa|new zealand|nz)\b', ' ', k)).strip(): return v
    s = slugify(name) or 'unknown'; unmapped.add(name); return s

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--year', type=int, default=2026)
    ap.add_argument('--base', default=None, help='feed base URL (default: live feed for 2026, archive otherwise)')
    ap.add_argument('--out', default=None)
    ap.add_argument('--cache', default=None, help='directory to cache/replay the raw XML')
    ap.add_argument('--check', action='store_true', help='compare party totals with data/elections/<year>.json')
    ap.add_argument('--force', action='store_true', help='write even when the feed has no votes yet')
    a = ap.parse_args()
    base = a.base or (LIVE if a.year == 2026 else ARCHIVE.format(year=a.year))
    out = Path(a.out) if a.out else ROOT / 'data' / f'results-{a.year}.json'
    slugs_by_name, party_names = load_slugs(); unmapped = set()

    parties = {p.get('p_no'): {'name': text(p, 'party_name'), 'short': text(p, 'short_name'), 'abbrev': text(p, 'abbrev'), 'registered': text(p, 'registered') == 'yes'}
               for p in ET.fromstring(fetch(base + 'parties.xml', a.cache)).findall('party')}
    for p in parties.values(): p['slug'] = party_slug(p['name'], party_names, unmapped)
    electorates = {e.get('e_no'): text(e, 'electorate_name') for e in ET.fromstring(fetch(base + 'electorates.xml', a.cache)).findall('electorate')}
    cands = {c.get('c_no'): {'name': person_name(text(c, 'candidate_name', '')), 'e_no': text(c, 'electorate'), 'p_no': text(c, 'party'), 'list_no': text(c, 'list_no')}
             for c in ET.fromstring(fetch(base + 'candidates.xml', a.cache)).findall('candidate')}
    el = ET.fromstring(fetch(base + 'election.xml', a.cache)); st = el.find('statistics')
    votes_cast = num(st, 'total_votes_cast')
    if votes_cast == 0 and not a.force:
        print(f'feed has no votes yet (updated {el.get("updated")}); nothing written'); return 0

    party_rows = []
    for p in el.find('partystatus').findall('party'):
        meta = parties.get(p.get('p_no'), {'name': 'Party ' + p.get('p_no'), 'slug': 'unknown-' + p.get('p_no'), 'registered': False})
        party_rows.append({'party': meta['slug'], 'name': meta['name'], 'registered': meta.get('registered', False), 'party_votes': num(p, 'votes'),
                           'party_vote_pct': float(num(p, 'percent_votes')), 'electorate_seats': num(p, 'candidate_seats'), 'list_seats': num(p, 'party_seats'), 'total_seats': num(p, 'total_seats')})
    party_rows.sort(key=lambda r: (-r['party_votes'], r['name']))

    e_rows = []
    for e_no in sorted(electorates, key=int):
        try: ex = ET.fromstring(fetch(f'{base}e{int(e_no):02d}/e{int(e_no):02d}.xml', a.cache))
        except Exception as err:  # keep going; one electorate file missing must not kill the run
            print('electorate', e_no, 'unavailable:', err, file=sys.stderr); continue
        es = ex.find('statistics'); name = electorates[e_no]; slug = slugs_by_name.get(norm(name), slugify(name))
        cv = []
        for c in (ex.find('candidatevotes') if ex.find('candidatevotes') is not None else []):
            meta = cands.get(c.get('c_no'), {'name': 'Candidate ' + c.get('c_no'), 'p_no': None})
            pm = parties.get(meta.get('p_no'), {'slug': 'independent'})
            cv.append({'name': meta['name'], 'party': pm['slug'], 'votes': num(c, 'votes')})
        cv.sort(key=lambda c: -c['votes'])
        pv = {}
        for p in (ex.find('partyvotes') if ex.find('partyvotes') is not None else []):
            pm = parties.get(p.get('p_no'));
            if pm: pv[pm['slug']] = pv.get(pm['slug'], 0) + num(p, 'votes')
        counted = float(num(es, 'percent_voting_places_counted')); final = ex.get('final') == 'true' and counted >= 100
        lead = cv[0] if cv and cv[0]['votes'] > 0 else None; second = cv[1] if len(cv) > 1 else None
        e_rows.append({'name': name, 'slug': slug, 'type': 'maori' if slug in MAORI else 'general', 'counted_pct': counted, 'final': final,
                       'votes_cast': num(es, 'total_votes_cast'), 'winner': lead['name'] if lead and final else None, 'party': lead['party'] if lead and final else None,
                       'leader': lead['name'] if lead else None, 'leader_party': lead['party'] if lead else None,
                       'majority': (lead['votes'] - second['votes']) if lead and second else None, 'runner_up': second['name'] if second and lead else None,
                       'runner_up_party': second['party'] if second and lead else None, 'winner_votes': lead['votes'] if lead else None,
                       'runner_up_votes': second['votes'] if second else None, 'candidates': cv, 'party_votes': pv})
        time.sleep(0.15)

    total_seats = sum(r['total_seats'] for r in party_rows)
    result = {'year': a.year, 'date': {2026: '2026-11-07', 2023: '2023-10-14', 2020: '2020-10-17', 2017: '2017-09-23'}.get(a.year), 'parliament': {2026: 55, 2023: 54, 2020: 53, 2017: 52}.get(a.year),
              'official': num(st, 'percent_electorates_final') >= 100 and a.year != 2026, 'preliminary': a.year == 2026,
              'updated': el.get('updated'), 'fetched': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              'counted_pct': float(num(st, 'percent_voting_places_counted')), 'counted_basis': 'percentage of voting places whose results have been entered (the Commission\'s measure), not percentage of votes',
              'voting_places_counted': num(st, 'total_voting_places_counted'), 'votes_cast': votes_cast, 'turnout_pct': float(num(st, 'percent_votes_cast')),
              'electorates_final': num(st, 'total_electorates_final'), 'total_seats': total_seats, 'majority': total_seats // 2 + 1 if total_seats else None,
              'source_url': 'https://www.electionresults.govt.nz' if a.year == 2026 else f'https://archive.electionresults.govt.nz/electionresults_{a.year}/',
              'feed_url': base, 'licence': 'Electoral Commission results data (Crown copyright); republished as factual information with attribution.',
              'parties': party_rows, 'electorates': e_rows, 'unmapped_parties': sorted(unmapped)}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n')
    print(f'{out}: {votes_cast:,} votes, {result["counted_pct"]}% of voting places, {len(e_rows)} electorates, {len(party_rows)} parties'
          + (f'; UNMAPPED party names: {sorted(unmapped)}' if unmapped else ''))

    if a.check:
        ref = json.load(open(ROOT / 'data' / 'elections' / f'{a.year}.json'))
        refp = {p['party']: p for p in ref['parties'] if isinstance(p, dict) and p.get('party_vote_pct') is not None}
        bad = 0
        for r in party_rows:
            if r['party'] in refp:
                q = refp[r['party']]
                for k in ('party_vote_pct', 'electorate_seats', 'list_seats', 'total_seats'):
                    if k in q and q[k] is not None and abs(float(q[k]) - float(r[k])) > (0.06 if k == 'party_vote_pct' else 0):
                        print(f'  MISMATCH {r["party"]} {k}: feed {r[k]} vs archive {q[k]}' + (f' ({q.get("note", "")[:80]})' if q.get('note') else '')); bad += 1
        refe = {norm(e['name']): e for e in ref.get('electorates', [])}
        for e in e_rows:
            q = refe.get(norm(e['name']))
            if q and e['winner'] and norm(q.get('winner', '')) != norm(e['winner']): print(f'  MISMATCH winner {e["name"]}: feed {e["winner"]} vs archive {q.get("winner")}'); bad += 1
        print('check:', 'OK' if not bad else f'{bad} differences')
    return 0

if __name__ == '__main__':
    sys.exit(main())
