#!/usr/bin/env python3
"""Build data/guide/quiz.json from tools/quiz_data.py, validate it, and refresh the coverage table in
guide/quiz-method.md (between <!-- GENERATED:quiz-coverage START/END --> markers).
Usage: python3 -I tools/quiz_build.py"""
import json, os, re, glob, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import quiz_data as Q

PARTIES = ['national', 'labour', 'green', 'act', 'nz-first', 'te-pati-maori', 'opportunity', 'nz-loyal',
           'nz-outdoors-freedom', 'legalise-cannabis', 'animal-justice', 'alliance', 'conservative',
           'womens-rights', 'vision-nz', 'free-palestine', 'te-tai-tokerau-party']
NAMES = {'national': 'National', 'labour': 'Labour', 'green': 'Green', 'act': 'ACT', 'nz-first': 'NZ First',
         'te-pati-maori': 'Te Pāti Māori', 'opportunity': 'Opportunity (TOP)', 'nz-loyal': 'NZ Loyal',
         'nz-outdoors-freedom': 'NZ Outdoors & Freedom', 'legalise-cannabis': 'Legalise Cannabis',
         'animal-justice': 'Animal Justice', 'alliance': 'Alliance', 'conservative': 'Conservative',
         'womens-rights': "Women's Rights", 'vision-nz': 'Vision NZ', 'free-palestine': 'Free Palestine',
         'te-tai-tokerau-party': 'Te Tai Tokerau Party'}
POLICYNZ_FILE = {'national': 'national-party', 'labour': 'labour-party', 'green': 'green-party', 'act': 'act-party',
                 'nz-first': 'nz-first', 'te-pati-maori': 'te-pati-maori', 'opportunity': 'opportunity-party'}

def deweb(u):
    m = re.search(r'/web/\d+[a-z_]*/(https?://.*)', u or '')
    return m.group(1) if m else u

# policy.nz index: id -> (party slug, statement, first citation url)
POL = {}
for slug, fn in POLICYNZ_FILE.items():
    d = json.load(open(os.path.join(ROOT, 'raw/policy.nz/parties', fn + '.json')))
    for p in d['policies']:
        cit = [deweb(c.get('url')) for c in p.get('citations', []) if c.get('url')]
        POL[p['reference']] = (slug, p['statement'].strip(), cit[0] if cit else None)

def doc_url(ref):
    path = os.path.join(ROOT, 'parties', ref.split('/')[0], 'policies/documents', ref.split('/', 1)[1])
    if not os.path.exists(path):
        raise SystemExit(f'missing document {path}')
    m = re.search(r'^source_url:\s*"?([^"\n]+)"?', open(path, encoding='utf-8').read(), re.M)
    if not m:
        raise SystemExit(f'no source_url in {path}')
    return m.group(1).strip()

import re
from quiz_blind_text import BLIND
# Terms that would tell the voter which party a statement belongs to. Statement text and
# explainers must not contain any of these; party positions/evidence (shown only after answering) may.
BANNED_NAMES = re.compile(r"\b(National|Labour|Greens?|ACT|NZ First|New Zealand First|Te P[āa]ti M[āa]ori|M[āa]ori Party|TOP|Opportunities|Alliance|Conservatives?|Vision NZ|NZ Loyal|"
    r"Luxon|Hipkins|Seymour|Peters|Swarbrick|Davidson|Waititi|Ngarewa-Packer|Willis|van Velden)\b")  # case-sensitive: 'national income', 'greenhouse', 'Crimes Act' are fine
BANNED_TERMS = re.compile(r"coalition|government did|the government has|the government dropped|the current government|the previous government|Treaty Principles Bill|Regulatory Standards|"
    r"Fast-track Approvals|Ka Ora|Medicard|KiwiMart|Kiwipower|Future Fund|FamilyBoost|Roads of National Significance|Te Aka Whai Ora|three strikes|Fair Pay Agreement|Gene Technology Bill|Online Safety bill", re.I)

errors = []
out = []
ids = set()
for st in Q.STATEMENTS:
    if st['id'] in ids: errors.append(f"duplicate id {st['id']}")
    ids.add(st['id'])
    if st['id'] not in BLIND: errors.append(f"{st['id']}: no party-blind wording in quiz_blind_text.py")
    else: st['text'], st['explainer'] = BLIND[st['id']]
    for field in ('text', 'explainer'):
        m = BANNED_NAMES.search(st[field]) or BANNED_TERMS.search(st[field])
        if m: errors.append(f"{st['id']}: {field} names a party or branded policy: '{m.group(0)}'")
    positions = {}
    for party in st['positions']:
        if party not in PARTIES: errors.append(f"{st['id']}: unknown party {party}")
    for party in PARTIES:
        c = st['positions'].get(party)
        if c is None:
            positions[party] = None; continue
        c = dict(c)
        if c['position'] not in (-2, -1, 0, 1, 2): errors.append(f"{st['id']}/{party}: bad position")
        if not c['evidence'].strip(): errors.append(f"{st['id']}/{party}: no evidence")
        pid = c.get('policy_id')
        if pid:
            if pid not in POL: errors.append(f"{st['id']}/{party}: unknown policy_id {pid}")
            elif POL[pid][0] != party: errors.append(f"{st['id']}/{party}: policy_id {pid} belongs to {POL[pid][0]}")
        src = c.get('source_url')
        if src and src.startswith('doc:'):
            src = doc_url(src[4:])
        if not src and pid in POL:
            src = POL[pid][2]
        if not src: errors.append(f"{st['id']}/{party}: no source")
        cell = {'position': c['position'], 'evidence': c['evidence'], 'source_url': src}
        if pid: cell['policy_id'] = pid
        positions[party] = cell
    out.append({'id': st['id'], 'issue': st['issue'], 'text': st['text'], 'explainer': st['explainer'],
                'positions': positions})

if errors:
    print('\n'.join(errors)); raise SystemExit(1)

n = len(out)
coverage = {p: sum(1 for s in out if s['positions'][p] is not None) for p in PARTIES}
doc = {
    'version': '2026-10',
    'generated': '2026-10-23',
    'scale': '-2 = strongly disagree, -1 = disagree, 0 = neutral/mixed, +1 = agree, +2 = strongly agree; '
             'null = the party has no public position we could find (never guessed). Positions are the party\'s, '
             'relative to the statement text.',
    'blind': 'Statement text and explainers are written without party names or branded policy names (enforced by quiz_build.py), '
             'so voters answer on the substance. Party positions and evidence are shown only after answering.',
    'scoring': {
        'method': 'For each statement both the user and the party answered: agreement = 1 - |user - party| / 4. '
                  'Weighted average over those statements using user importance weights (default 1; suggest 0.5/1/2). '
                  'Report coverage = statements the party has a position on, out of statements the user answered; '
                  'flag matches with coverage below 10 statements, and blend toward 0.5 (neutral) by '
                  'adjusted = (sum_w*agree + k*0.5) / (sum_w + k) with k = 3 so thin records are not over-rewarded.',
        'see': 'guide/quiz-method.md'},
    'parties': {p: {'name': NAMES[p], 'positions_recorded': coverage[p]} for p in PARTIES},
    'statements': out,
}
os.makedirs(os.path.join(ROOT, 'data/guide'), exist_ok=True)
json.dump(doc, open(os.path.join(ROOT, 'data/guide/quiz.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---- coverage table for guide/quiz-method.md
issues = []
for s in out:
    if s['issue'] not in issues: issues.append(s['issue'])
lines = [f'Statements: **{n}**. Cells filled: **{sum(coverage.values())}** of {n * len(PARTIES)}.', '',
         '| Party | Positions recorded | Coverage | Agree (+1/+2) | Neutral (0) | Disagree (−1/−2) | via policy.nz id |',
         '|---|---:|---:|---:|---:|---:|---:|']
for p in sorted(PARTIES, key=lambda x: -coverage[x]):
    cells = [s['positions'][p] for s in out if s['positions'][p]]
    lines.append(f"| {NAMES[p]} | {coverage[p]} | {round(100 * coverage[p] / n)}% | "
                 f"{sum(1 for c in cells if c['position'] > 0)} | {sum(1 for c in cells if c['position'] == 0)} | "
                 f"{sum(1 for c in cells if c['position'] < 0)} | {sum(1 for c in cells if c.get('policy_id'))} |")
lines += ['', '| # | Issue | Statement | Parties with a position |', '|---|---|---|---:|']
for s in out:
    k = sum(1 for p in PARTIES if s['positions'][p] is not None)
    lines.append(f"| {s['id']} | {s['issue']} | {s['text']} | {k} |")
table = '\n'.join(lines)
mp = os.path.join(ROOT, 'guide/quiz-method.md')
if os.path.exists(mp):
    md = open(mp, encoding='utf-8').read()
    md = re.sub(r'(<!-- GENERATED:quiz-coverage START -->).*?(<!-- GENERATED:quiz-coverage END -->)',
                lambda m: m.group(1) + '\n' + table + '\n' + m.group(2), md, flags=re.S)
    open(mp, 'w', encoding='utf-8').write(md)
print(f'OK: {n} statements; coverage', coverage)
