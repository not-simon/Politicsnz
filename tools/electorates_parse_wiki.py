#!/usr/bin/env python3
"""Parse Wikipedia wikitext: 2026 candidates by electorate and 2023 results (electorate + party vote by electorate).
Writes raw/electorates/parsed_wiki.json. Run with python3 -I."""
import re, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
def strip_refs(s):
    s = re.sub(r'<ref[^>]*/>', '', s); return re.sub(r'<ref[^>]*>.*?</ref>', '', s, flags=re.S)
def delink(s):
    s = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', s or '')
    s = re.sub(r'\{\{NZ electorate link\|([^}|]*)[^}]*\}\}', r'\1', s)
    s = re.sub(r"'''?", '', s)
    return s.strip()
def fields(block):
    out = {}
    for m in re.finditer(r'\|\s*([a-z\-]+)\s*=\s*(.*?)(?=\n\s*\||\n?\}\}\s*$)', block, re.S):
        out[m.group(1)] = m.group(2).strip()
    return out
# --- 2026 candidates
t = strip_refs((ROOT / 'raw/elections/Candidates_in_the_2026_New_Zealand_general_election_by_electorate.wikitext').read_text())
cands = {}
for sec in re.split(r'\n===\s*', t)[1:]:
    name = sec.split('===')[0].strip()
    body = sec.split('===', 1)[1] if '===' in sec else ''
    withdrawn_part = ''
    if 'Retiring incumbents and withdrawn' in body:
        body, withdrawn_part = body.split('Retiring incumbents and withdrawn', 1)
    lst = []
    for part, wd in ((body, False), (withdrawn_part, True)):
        for m in re.finditer(r'\{\{NZ election box (candidate list|candidate|incumbent|independent|incumbent list)\b(.*?)\n\}\}', part, re.S):
            f = fields(m.group(2))
            lst.append({'name': delink(f.get('candidate', '')), 'party': delink(f.get('party', '')) or 'Independent',
                        'list': f.get('list', '').strip() or None, 'notes': delink(f.get('notes', '')),
                        'incumbent': 'incumbent' in m.group(1), 'box': m.group(1), 'withdrawn': wd})
    cands[name] = lst
# --- 2023 results
r = strip_refs((ROOT / 'raw/electorates/Results_of_the_2023_New_Zealand_general_election.wikitext').read_text())
res = {}
for m in re.finditer(r'\{\{NZ electorate result (hold|change)(.*?)\n\}\}', r, re.S):
    f = fields(m.group(2)); e = delink(f.get('electorate'))
    win = delink(f.get('winner')) or delink(f.get('incumbent')); wp = delink(f.get('winner-party')) or delink(f.get('incumbent-party'))
    res[e] = {'kind': m.group(1), 'incumbent': delink(f.get('incumbent')), 'incumbent_party': delink(f.get('incumbent-party')),
              'winner': win, 'winner_party': wp, 'majority': int(f.get('majority', '0').replace(',', '') or 0),
              'runner_up': delink(f.get('second')), 'runner_up_party': delink(f.get('second-party')),
              'third': delink(f.get('third')), 'third_party': delink(f.get('third-party'))}
# party vote by electorate
sec = r[r.index('===By electorate==='):r.index('== Electorate results ==')]
heads = ['National', 'Labour', 'Green', 'ACT', 'NZ First', 'Te Pāti Māori', 'TOP', 'NZ Loyal']
pv = {}
for row in sec.split('\n|-')[1:]:
    lines = [l for l in row.strip().split('\n') if l.startswith('|')]
    if not lines or 'text-align:left' not in lines[0]: continue
    e = delink(lines[0].split('|', 2)[-1] if lines[0].count('|') >= 2 else lines[0])
    e = re.sub(r'^style="[^"]*"\s*\|\s*', '', e).strip()
    vals = []
    for l in lines[1:]:
        v = l.split('|')[-1].strip()
        try: vals.append(float(v))
        except ValueError: vals.append(None)
    if len(vals) >= 8: pv[e] = dict(zip(heads, vals[:8]))
json.dump({'candidates_2026': cands, 'results_2023': res, 'party_vote_2023': pv}, open(ROOT / 'raw/electorates/parsed_wiki.json', 'w'), ensure_ascii=False, indent=1)
print(len(cands), len(res), len(pv))
