#!/usr/bin/env python3
"""Build data/electorates/2026.json, electorates/<slug>.md and electorates/README.md.

Inputs (all already downloaded; run tools/electorates_wiki_fetch.py and tools/electorates_parse_wiki.py first):
  raw/policy.nz/electorates/*.json            policy.nz electorate descriptions + candidate lists
  raw/electorates/parsed_wiki.json            Wikipedia 2026 candidates-by-electorate (incumbent flags, notes)
  raw/electorates/parsed_wiki_pages.json      Wikipedia electorate articles: official 2023 results boxes
  raw/electorates/ec/electorate_maps.html     Electoral Commission 2025 boundary maps page
  data/elections/2023.json                    (cross-check only)
Run: python3 -I tools/electorates_build.py
"""
import json, re, glob, pathlib, sys, unicodedata, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from partymap import PNZ_TO_REPO
from electorates_meta import SRC, REGION, CHANGES, ABOLISHED, SITTING_OVERRIDE, NOT_STANDING, NOTES, BATTLEGROUNDS
from bs4 import BeautifulSoup

TODAY = '2026-10-23'
def norm(s):
    return re.sub(r'[^a-z]', '', unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower())
def slugify(s):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower())).strip('-')
def src(keys):
    return [SRC.get(k, k) for k in keys]

PARTY_NAMES = {'national': 'National', 'labour': 'Labour', 'green': 'Green', 'act': 'ACT', 'nz-first': 'NZ First',
               'te-pati-maori': 'Te Pāti Māori', 'opportunity': 'Opportunity (TOP)', 'nz-loyal': 'NZ Loyal',
               'nz-outdoors-freedom': 'NZ Outdoors & Freedom', 'legalise-cannabis': 'Legalise Cannabis',
               'animal-justice': 'Animal Justice', 'alliance': 'Alliance', 'conservative': 'Conservative',
               'womens-rights': "Women's Rights", 'vision-nz': 'Vision NZ', 'free-palestine': 'Free Palestine',
               'te-tai-tokerau-party': 'Te Tai Tokerau Party', 'independent': 'Independent'}
def wiki_party(name):
    n = (name or '').lower()
    for k, v in [('national', 'national'), ('labour', 'labour'), ('green', 'green'), ('act new zealand', 'act'),
                 ('new zealand first', 'nz-first'), ('nz first', 'nz-first'), ('tai tokerau party', 'te-tai-tokerau-party'),
                 ('māori', 'te-pati-maori'), ('opportunit', 'opportunity'), ('loyal', 'nz-loyal'),
                 ('outdoors', 'nz-outdoors-freedom'), ('cannabis', 'legalise-cannabis'), ('animal justice', 'animal-justice'),
                 ('alliance', 'alliance'), ('new conservative', 'new-conservative'), ('conservative', 'conservative'),
                 ("women's rights", 'womens-rights'), ('vision', 'vision-nz'), ('free palestine', 'free-palestine'),
                 ('newzeal', 'newzeal'), ('freedoms', 'freedoms-nz'), ('democracynz', 'democracynz'),
                 ('leighton baker', 'leighton-baker'), ('independent', 'independent')]:
        if k in n: return v
    return slugify(name) if name else 'independent'
def pname(p): return PARTY_NAMES.get(p, p.replace('-', ' ').title())

def clean_name(first, last):
    def fix(tok):
        if len(tok) > 1 and tok.isupper():
            t = tok.capitalize()
            t = re.sub(r'^(Mc)([a-z])', lambda m: 'Mc' + m.group(2).upper(), t)
            t = re.sub(r"-([a-z])", lambda m: '-' + m.group(1).upper(), t)
            return t
        if re.match(r'^Mc[A-Z]{2,}', tok): return 'Mc' + tok[2:].capitalize()
        return tok
    return ' '.join(fix(t) for t in f'{first} {last}'.split())

# ---------- inputs
W = json.load(open(ROOT / 'raw/electorates/parsed_wiki.json'))
WC = W['candidates_2026']; WCN = {norm(k): k for k in WC}
PAGES = json.load(open(ROOT / 'raw/electorates/parsed_wiki_pages.json'))
PAGE_BY_SEAT = {re.sub(r' \(.*\)$', '', v['title']): v for v in PAGES.values()}
PAGE_BY_SEAT.update({'Mt Albert': PAGE_BY_SEAT.get('Mount Albert'), 'Mt Roskill': PAGE_BY_SEAT.get('Mount Roskill')})
E23 = {e['name']: e for e in json.load(open(ROOT / 'data/elections/2023.json'))['electorates']}
maps = {}
mh = ROOT / 'raw/electorates/ec/electorate_maps.html'
if mh.exists():
    for a in BeautifulSoup(mh.read_text(), 'html.parser').find_all('a', href=True):
        if '/Boundary-Review/2025/Maps/' in a['href']:
            maps[norm(a.get_text().split('(')[0])] = 'https://elections.nz' + a['href']
MAPS_PAGE = SRC['ec_maps']; INTERACTIVE = 'https://elections.nz/maps/boundary-review-2025'

def find_folder(party, slug):
    p = ROOT / 'parties' / party / 'people' / slug
    if p.exists(): return f'parties/{party}/people/{slug}'
    hits = sorted(glob.glob(str(ROOT / 'parties' / '*' / 'people' / slug)))
    return str(pathlib.Path(hits[0]).relative_to(ROOT)) if hits else None

SKIP_KINDS = ('party only', 'majority', 'informal', 'total', 'turnout', 'swing', 'gain', 'hold', 'rejected', 'disallowed')
def result_from_page(seat):
    pg = PAGE_BY_SEAT.get(seat)
    if not pg: return None, None
    key = 'by2023' if seat == 'Port Waikato' else 'ge2023'
    rows = pg.get(key) or []
    cands = sorted([r for r in rows if r['votes'] is not None and r['candidate'] and not r['kind'].startswith(SKIP_KINDS)], key=lambda r: -r['votes'])
    pv = {}
    for r in pg.get('ge2023') or []:
        if r.get('party_pct') is not None and r['party']:
            sl = wiki_party(r['party'])
            pv[sl] = round(pv.get(sl, 0) + r['party_pct'], 2)
    if len(cands) < 2: return None, pg['url']
    w, ru = cands[0], cands[1]
    total = sum(c['votes'] for c in cands)
    res = {'seat': seat, 'contest': '2023 Port Waikato by-election (25 Nov 2023)' if key == 'by2023' else '2023 general election (14 Oct 2023)',
           'winner': w['candidate'], 'party': wiki_party(w['party']), 'winner_votes': w['votes'], 'winner_pct': w['pct'],
           'majority': w['votes'] - ru['votes'], 'runner_up': ru['candidate'], 'runner_up_party': wiki_party(ru['party']),
           'runner_up_votes': ru['votes'],
           'candidates': [{'name': c['candidate'], 'party': wiki_party(c['party']), 'votes': c['votes'], 'pct': c['pct']} for c in cands]}
    main = ['national', 'labour', 'green', 'act', 'nz-first', 'te-pati-maori', 'opportunity', 'nz-loyal']
    if pv:
        res['party_vote_winner'] = max(pv, key=pv.get)
        res['party_vote_pct'] = {k: pv[k] for k in main if k in pv}
        res['party_vote_basis'] = '2023 general election party vote (official count)'
    mj = [r for r in rows if r['kind'].startswith('majority')]
    if mj and mj[0]['votes'] != res['majority']:
        res['note'] = f"Wikipedia's majority row says {mj[0]['votes']}; computed from candidate votes: {res['majority']}."
    return res, pg['url']

# ---------- build
out = []
for f in sorted(glob.glob(str(ROOT / 'raw/policy.nz/electorates/*-electorate.json'))):
    el = json.load(open(f))['election']
    slug = el['slug'].replace('-electorate', '')
    name = el['title'].replace(' electorate', '')
    etype = 'maori' if any(t['slug'] == 'roll:maori' for t in el['tags']) else 'general'
    ch = CHANGES.get(slug)
    wname = WCN.get(norm(name)) or WCN.get(norm(name.replace('Mt ', 'Mount ')))
    wl = [x for x in WC.get(wname, []) if not x['withdrawn']]
    result_seat = ch['result_seat'] if ch else (wname if wname in PAGE_BY_SEAT else name)
    if result_seat not in PAGE_BY_SEAT: result_seat = result_seat.replace('Mt ', 'Mount ')
    res, res_url = result_from_page(result_seat)
    sources = [f'https://policy.nz/2026/{el["slug"]}', SRC['wcands'], SRC['ec_maps']]
    if res_url: sources.append(res_url)
    # cross-check with data/elections/2023.json
    xchk = None
    e23 = E23.get(result_seat) or E23.get(result_seat.replace('Mount ', 'Mt '))
    if res and e23 and e23.get('majority') not in (None, res['majority']) and result_seat != 'Port Waikato':
        xchk = f"data/elections/2023.json gives a majority of {e23['majority']:,}; the official count shown in the Wikipedia electorate article gives {res['majority']:,} (the summary table there appears to use preliminary figures)."
    # candidates
    cands = []
    for c in el.get('candidates') or []:
        per = c['person']; ps = (per.get('party') or {}).get('slug') or 'independent'
        party = PNZ_TO_REPO.get(ps, ps)
        pa = per.get('partyAffiliation') or {}
        rank = pa.get('listRank'); rank = int(rank) if rank and str(rank).strip().isdigit() else None
        nm = clean_name(per['firstName'], per['lastName'])
        match = None
        for x in wl:
            xp = wiki_party(x['party'])
            same_party = xp == party or (xp == 'independent' and party in ('independent',)) or (party not in PARTY_NAMES)
            xn = re.sub(r'\{\{.*', '', x['name']).strip()
            if norm(xn) == norm(nm) or (same_party and (norm(xn.split()[-1]) == norm(nm.split()[-1]) or norm(xn.split()[0]) == norm(nm.split()[0]))):
                match = dict(x, name=xn); break
        if match and rank is None and (match.get('list') or '').isdigit(): rank = int(match['list'])
        cands.append({'name': match['name'] if match else nm, 'slug': per['slug'], 'party': party,
                      'party_name': (per.get('party') or {}).get('name') or 'Independent',
                      'list_rank_2026': rank, 'folder': find_folder(party, per['slug']),
                      'wikipedia_note': (match or {}).get('notes') or None,
                      'incumbent': bool(match and match['incumbent'])})
    order = ['national', 'labour', 'green', 'act', 'nz-first', 'te-pati-maori', 'opportunity']
    cands.sort(key=lambda c: (order.index(c['party']) if c['party'] in order else 99, c['name']))
    # sitting MP
    ov = SITTING_OVERRIDE.get(slug, {})
    sitting, sitting_note = None, ov.get('note')
    if ov.get('vacant'):
        sitting = None
    elif ov.get('mp'):
        n, p, s = ov['mp']; sitting = {'name': n, 'party': p, 'slug': s}
    elif res:
        win_c = next((c for c in cands if norm(c['name']) == norm(res['winner']) or c['incumbent']), None)
        sitting = {'name': res['winner'], 'party': res['party'], 'slug': win_c['slug'] if win_c else slugify(res['winner'])}
    if sitting:
        sitting['folder'] = find_folder(sitting['party'], sitting['slug'])
        if ch: sitting['seat_held'] = ch['result_seat']
    standing = bool(sitting and any(norm(c['name']) == norm(sitting['name']) or c['slug'] == sitting['slug'] for c in cands))
    for c in cands:
        c['sitting_mp'] = bool(sitting and (c['slug'] == sitting['slug'] or norm(c['name']) == norm(sitting['name'])))
        c.pop('incumbent')
    # predecessor MPs for new seats
    pred_mps = []
    if ch:
        for ps in ch['predecessors']:
            r2, _ = result_from_page(ps)
            if r2:
                pred_mps.append({'seat': ps, 'mp_2023': r2['winner'], 'party': r2['party'], 'majority_2023': r2['majority'],
                                 'standing_here': any(norm(c['name']) == norm(r2['winner']) for c in cands)})
    maj = res['majority'] if res else None
    bg = next((b for b in BATTLEGROUNDS if b[0] == slug), None)
    marginal = bool((maj is not None and maj < 2000) or bg)
    basis = []
    if maj is not None and maj < 2000: basis.append(f'2023 majority {maj:,} (<2,000)' + (f' in predecessor {result_seat}' if ch else ''))
    if bg: basis.append('identified as a seat to watch by media analysis: ' + bg[1])
    if slug == 'tamaki-makaurau': basis.append('2025 by-election majority was 3,519')
    # contest notes
    if slug in NOTES:
        note, nsrc = NOTES[slug]; nsrc = src(nsrc)
    elif res:
        pv_note = ''
        if res.get('party_vote_winner') and res['party_vote_winner'] != res['party']:
            pv_note = f" {pname(res['party_vote_winner'])} won the party vote."
        who = sitting['name'] if sitting else 'The sitting MP'
        note = (f"{pname(res['party'])} won {'the predecessor seat of ' + result_seat if ch else 'here'} by {res['majority']:,} votes in 2023 "
                f"over {pname(res['runner_up_party'])}'s {res['runner_up']}.{pv_note} "
                + (f"{who} is standing again." if standing else f"{who} is not standing here."))
        nsrc = [res_url, SRC['wcands']]
    else:
        note, nsrc = '', []
    if slug in NOT_STANDING and NOT_STANDING[slug] not in note:
        note = (note + ' ' + NOT_STANDING[slug]).strip()
        nsrc = nsrc + [SRC['w2026']]
    sources += [s for s in nsrc if s and s not in sources]
    if ch: sources += [s for s in src(ch['src']) if s not in sources]
    if ov: sources += [s for s in src(ov.get('src', [])) if s not in sources]
    # policy.nz description fact-check
    desc = el['description'].strip()
    checks = []
    if res:
        for m in re.finditer(r'margin of (\d[\d,]*\d|\d)(%?)', desc):
            v = int(m.group(1).replace(',', ''))
            sent = desc[max(desc.rfind('.', 0, m.start()), 0):m.start()]
            if 'party vote' in sent: continue
            if m.group(2) == '%':
                checks.append(f'"margin of {m.group(1)}%" — the official 2023 majority was {res["majority"]:,} votes.')
            elif v != res['majority']:
                extra = ' (that figure is the winner’s vote total)' if v == res['winner_votes'] else ''
                checks.append(f'"margin of {m.group(1)}"{extra} — the official 2023 majority was {res["majority"]:,} votes over {res["runner_up"]}.')
    MANUAL_CHECK = {
        'hauraki-waikato': 'The description refers to the 2020 result: Nanaia Mahuta (Labour) lost the seat in 2023 to Hana-Rawhiti Maipi-Clarke (Te Pāti Māori), the current MP.',
        'papakura': 'Judith Collins resigned from Parliament on 14 May 2026; the seat is vacant until the election.',
        'wellington-bays': 'Julie Anne Genter won Rongotai at the 2023 (not 2026) election.',
        'northcote': '"margin of 43" in the party vote should be read as 43% (National’s party-vote share).',
        'waitakere': 'Paulo Garcia was the MP for New Lynn (a predecessor seat), not Waitākere.',
        'kenepuru': 'Ōhāriu is the correct spelling of the predecessor seat.',
        'te-tai-tonga': 'The claim that Rino Tirikatene has joined NZ First has not been independently verified here.',
    }
    if slug in MANUAL_CHECK: checks.append(MANUAL_CHECK[slug])
    entry = {
        'slug': slug, 'name': name, 'type': etype, 'region': REGION.get(slug),
        'description': desc, 'description_source': f'policy.nz (https://policy.nz/2026/{el["slug"]}), retrieved Oct 2026; quoted verbatim',
        'description_fact_check': checks,
        'boundary_status': ch['status'] if ch else 'continuing (same name; boundaries may have been adjusted in the 2025 review)',
        'boundary_note': ch['note'] if ch else None,
        'predecessor_seats': ch['predecessors'] if ch else [name if not name.startswith('Mt ') else name],
        'predecessor_mps': pred_mps or None,
        'map_pdf': maps.get(norm(name)) or maps.get(norm(name.replace('Mount ', 'Mt '))),
        'map_page': MAPS_PAGE,
        'sitting_mp': sitting, 'sitting_mp_note': sitting_note,
        'mp_standing_again': standing,
        'mp_not_standing_note': NOT_STANDING.get(slug),
        'result_2023': ({**res, 'for_predecessor_seat': result_seat if ch else None,
                          'source': res_url, 'cross_check': xchk} if res else None),
        'candidates': cands, 'candidates_count': len(cands),
        'marginal': marginal, 'marginal_basis': basis,
        'contest_notes': note, 'contest_notes_sources': nsrc,
        'sources': sources,
    }
    out.append(entry)

out.sort(key=lambda e: (e['type'] != 'general', norm(e['name'])))
(ROOT / 'data/electorates').mkdir(parents=True, exist_ok=True)
json.dump(out, open(ROOT / 'data/electorates/2026.json', 'w'), ensure_ascii=False, indent=1)

# ---------- markdown
D = ROOT / 'electorates'; D.mkdir(exist_ok=True)
def fmt(n): return f'{n:,}' if isinstance(n, int) else ('—' if n is None else str(n))
def plink(c, prefix='../'):
    return f"[{c['name']}]({prefix}{c['folder']}/)" if c.get('folder') else c['name']
for e in out:
    L = [f"# {e['name']} electorate ({'Māori' if e['type'] == 'maori' else 'general'})", '',
         f"**Region:** {e['region']}  ", f"**Election day:** Saturday 7 November 2026  ",
         f"**Boundary status:** {e['boundary_status']}" + (f" — predecessor seat(s): {', '.join(e['predecessor_seats'])}" if e['boundary_note'] else ''), '']
    if e['boundary_note']: L += [f"> {e['boundary_note']}", '']
    L += ['## About this electorate', '', e['description'], '', f"_Description quoted from [policy.nz](https://policy.nz/2026/{e['slug']}-electorate)._", '']
    if e['description_fact_check']:
        L += ['**Fact-check notes on the description above** (checked against official 2023 results):', '']
        L += [f'- {x}' for x in e['description_fact_check']] + ['']
    L += ['## Map', '']
    if e['map_pdf']: L.append(f"- [Official 2025 boundary map (PDF, Electoral Commission)]({e['map_pdf']})")
    L += [f"- [All electorate maps — Electoral Commission]({e['map_page']})", f"- [Interactive map comparing 2020 and 2025 boundaries]({INTERACTIVE})", '']
    L += ['## Sitting MP', '']
    s = e['sitting_mp']
    if s:
        L.append(f"**{plink(s) if s.get('folder') else s['name']}** ({pname(s['party'])})" + (f" — elected for {s['seat_held']} in 2023" if s.get('seat_held') else '') + '  ')
        L.append(f"Standing again here in 2026: **{'yes' if e['mp_standing_again'] else 'no'}**")
    else:
        L.append('**Vacant**')
    if e['sitting_mp_note']: L += ['', e['sitting_mp_note']]
    if e['mp_not_standing_note']: L += ['', e['mp_not_standing_note']]
    if e['predecessor_mps']:
        L += ['', '| Predecessor seat | MP elected 2023 | Party | 2023 majority | Standing here? |', '|---|---|---|---|---|']
        for p in e['predecessor_mps']:
            L.append(f"| {p['seat']} | {p['mp_2023']} | {pname(p['party'])} | {fmt(p['majority_2023'])} | {'yes' if p['standing_here'] else 'no'} |")
    L.append('')
    r = e['result_2023']
    L += ['## 2023 result' + (f" (predecessor seat: {r['for_predecessor_seat']})" if r and r.get('for_predecessor_seat') else ''), '']
    if r:
        L += [f"_{r['contest']}. Winner **{r['winner']}** ({pname(r['party'])}), majority **{fmt(r['majority'])}**._", '',
              '| Candidate | Party | Votes | % |', '|---|---|---:|---:|']
        for c in r['candidates'][:6]:
            L.append(f"| {c['name']} | {pname(c['party'])} | {fmt(c['votes'])} | {c['pct'] if c['pct'] is not None else '—'} |")
        if len(r['candidates']) > 6: L.append(f"| _{len(r['candidates']) - 6} others_ | | | |")
        if r.get('party_vote_pct'):
            L += ['', '**Party vote 2023 (%):** ' + ', '.join(f"{pname(k)} {v}" for k, v in sorted(r['party_vote_pct'].items(), key=lambda kv: -kv[1]))]
            if r['seat'] == 'Port Waikato': L.append('_Party vote is from the 14 October 2023 general election (the party vote was not cancelled)._')
        if r.get('cross_check'): L += ['', f"_Note: {r['cross_check']}_"]
        L += ['', f"_Source: [Wikipedia — {r['seat']}]({r['source']}), citing the Electoral Commission official result._"]
    else:
        L.append('No 2023 result available.')
    L += ['', f"## 2026 candidates ({e['candidates_count']})", '', '| Candidate | Party | List rank | Notes |', '|---|---|---:|---|']
    for c in e['candidates']:
        note = ('**Sitting MP.** ' if c['sitting_mp'] else '') + (c['wikipedia_note'] or '')
        L.append(f"| {plink(c)} | {c['party_name']} | {c['list_rank_2026'] or '—'} | {note.strip()} |")
    L += ['', '_Candidate list from policy.nz (Electoral Commission final list, released 9 Oct 2026); notes from Wikipedia._', '']
    L += ['## What to watch', '']
    L.append(f"- {e['contest_notes']}" if e['contest_notes'] else '- —')
    if e['marginal']: L.append(f"- **Marginal / battleground:** {'; '.join(e['marginal_basis'])}.")
    L += ['', '## Sources', ''] + [f'- {u}' for u in e['sources']] + ['', f'_Compiled {TODAY} by tools/electorates_build.py._', '']
    (D / f"{e['slug']}.md").write_text('\n'.join(L))

# README
R = ['# 2026 electorates — voter guide', '',
     'New Zealand votes on **Saturday 7 November 2026**. You get two votes: a **party vote** (decides how many seats each party gets) and an **electorate vote** for your local MP. '
     'There are **71 electorates** in 2026 — 64 general (48 North Island, 16 South Island) and 7 Māori — one fewer than in 2023 after the 2025 boundary review.', '',
     'Find your electorate: [Electoral Commission electorate maps](%s) · [interactive map](%s). Data: [`data/electorates/2026.json`](../data/electorates/2026.json).' % (MAPS_PAGE, INTERACTIVE), '',
     '## What changed in the 2025 boundary review', '',
     'The Representation Commission finalised boundaries on 8 August 2025: 19 electorates were unchanged and the boundaries of 49 general and three Māori electorates were adjusted, mainly in Auckland, Bay of Plenty, Christchurch and the lower North Island, where one North Island general seat was removed ([Electoral Commission](%s); [Wikipedia](%s)).' % (SRC['ec_final'], SRC['w2026']), '',
     '| New / renamed 2026 seat | Status | Predecessor seat(s) |', '|---|---|---|']
for e in out:
    if e['boundary_note']: R.append(f"| [{e['name']}]({e['slug']}.md) | {e['boundary_status']} | {', '.join(e['predecessor_seats'])} |")
R += ['', '**Abolished or renamed 2023 seats:** ' + '; '.join(f'{a} ({b})' for a, b in ABOLISHED) + '.', '']
R += ['## Battleground seats to watch in 2026', '',
      'Drawn from published media analyses (pollster David Farrar and commentators in [interest.co.nz/RNZ, 19 Aug 2026](%s); [Stuff, 19 Oct 2026](%s); commentator Michael Swanson, [The Periodical, 18 Oct 2026](%s); [RNZ, 14 Oct 2026](%s); [NZ Herald, 20 Oct 2026](%s)). Farrar said at least 12 National-held general seats, all three Green-held seats and ACT-held Tāmaki could be competitive, and that every Māori seat except Ikaroa-Rāwhiti is potentially in play.' % (SRC['interest'], SRC['stuff8'], SRC['swanson'], SRC['rnz_ttt'], SRC['herald_diary']), '',
      '| Seat | Held by (2023) | 2023 majority | Why it matters | Sources |', '|---|---|---:|---|---|']
byslug = {e['slug']: e for e in out}
for s, why, ks in BATTLEGROUNDS:
    e = byslug[s]; r = e['result_2023'] or {}
    R.append(f"| [{e['name']}]({s}.md) | {pname(r.get('party', ''))} | {fmt(r.get('majority'))} | {why} | " + ' '.join(f'[{i+1}]({u})' for i, u in enumerate(src(ks))) + ' |')
close = sorted([e for e in out if e['result_2023'] and e['result_2023']['majority'] < 2000], key=lambda e: e['result_2023']['majority'])
R += ['', '**Closest 2023 results (majority under 2,000, including predecessor seats):** ' + ', '.join(
    f"[{e['name']}]({e['slug']}.md) {e['result_2023']['majority']:,}" + (f" ({e['result_2023']['for_predecessor_seat']})" if e['result_2023'].get('for_predecessor_seat') else '') for e in close) + '. Ōhāriu (abolished) was also won by 1,260.']
R += ['', '**Split-voting campaigns:** Te Pāti Māori is urging supporters to give it their electorate vote and their party vote to Labour or the Greens; National’s leadership has urged voters not to split votes, while ACT and NZ First defended the practice ([Wikipedia](%s)). No formal electorate deals have been announced; in Epsom, National’s Paul Goldsmith is openly contesting ACT leader David Seymour’s seat ([Stuff](%s)).' % (SRC['w2026'], SRC['stuff8']), '']
R += ['## All electorates', '', '“Majority” is the 2023 winning margin (for new/renamed seats, of the main predecessor seat, shown in brackets). ⚠️ = marginal (majority under 2,000) or named as a battleground by media.', '',
      '| Electorate | Type | Region | Sitting MP | Standing again? | 2023 majority | Candidates | Marginal |', '|---|---|---|---|---|---:|---:|:---:|']
for e in out:
    s = e['sitting_mp']; r = e['result_2023'] or {}
    mp = f"{s['name']} ({pname(s['party'])})" if s else 'Vacant'
    mj = fmt(r.get('majority')) + (f" ({r['for_predecessor_seat']})" if r.get('for_predecessor_seat') else '') + (' (2023 by-election)' if 'by-election' in r.get('contest', '') else '')
    R.append(f"| [{e['name']}]({e['slug']}.md) | {'Māori' if e['type'] == 'maori' else 'General'} | {e['region']} | {mp} | {'yes' if e['mp_standing_again'] else ('—' if not s else 'no')} | {mj} | {e['candidates_count']} | {'⚠️' if e['marginal'] else ''} |")
R += ['', '## About the data', '',
      '- **Descriptions** are quoted verbatim from policy.nz with attribution. Several contain numerical errors (often the winner’s vote total is described as the “margin”); each electorate page lists fact-check notes against official results.',
      '- **2023 results** are the official counts as reproduced in each Wikipedia electorate article (which cite the Electoral Commission; electionresults.govt.nz itself is blocked from this environment). Where `data/elections/2023.json` (built from the Wikipedia summary table, which uses some preliminary-count figures) differs, the page says so.',
      '- **Candidates** are the final list published by policy.nz; list ranks from policy.nz or Wikipedia. Each links to the candidate’s folder under `parties/`.',
      f'- Compiled {TODAY} by `tools/electorates_build.py` (inputs fetched by `tools/electorates_wiki_fetch.py`, parsed by `tools/electorates_parse_wiki.py`).', '']
(D / 'README.md').write_text('\n'.join(R))
print('electorates:', len(out), 'general', sum(e['type'] == 'general' for e in out), 'maori', sum(e['type'] == 'maori' for e in out))
print('marginal', sum(e['marginal'] for e in out), 'no folder', sum(1 for e in out for c in e['candidates'] if not c['folder']))
