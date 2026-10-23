#!/usr/bin/env python3
"""Compute every number used in REPORT.md from the archive's JSON, so the report stays consistent with the data.

Usage:
    python3 tools/report_stats.py            # print all generated blocks to stdout
    python3 tools/report_stats.py --write    # rewrite the <!-- GENERATED:report-<name> START/END --> blocks in REPORT.md
    python3 tools/report_stats.py --write some/other/file.md   # same, for another copy of the report

Inputs (read-only): data/polls-2026.json, data/elections/*.json, data/parliaments/54.json, data/promises/*.json,
data/elections/2026.json, parties/*/policies/policies.json, data/guide/parties.json.

Method notes (also stated in REPORT.md):
- Poll average = simple unweighted mean of every published party-vote poll whose fieldwork ended in the 30 days up to
  the snapshot date (the same window and method data/guide/parties.json uses).
- Seat projections use the Sainte-Laguë divisors 1, 3, 5, ... over 120 seats, as the Electoral Act does. Only parties at
  or above 5% of the party vote, or assumed to win an electorate, share the seats. If a party wins more electorates than
  its entitlement it keeps them and the House grows (overhang). These are illustrations, not forecasts.
- Promise statistics: "resolved" = kept + partially kept + broken + abandoned. In-progress and not-yet-due items are
  left out of every percentage. Delivery index = (kept + 0.5 x partially kept) / resolved, the formula the ACT and NZ First
  track-record pages already use, applied here to every party.
"""
import json, glob, math, re, sys, collections, datetime, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPSHOT = datetime.date(2026, 10, 23)
SEATS = 120
MAIN7 = ['national', 'labour', 'green', 'act', 'nz-first', 'te-pati-maori', 'opportunity']
NAMES = {'national': 'National', 'labour': 'Labour', 'green': 'Green', 'act': 'ACT', 'nz-first': 'NZ First',
         'te-pati-maori': 'Te Pāti Māori', 'opportunity': 'TOP (Opportunity)', 'united-future': 'United Future',
         'mana': 'Mana', 'conservative': 'Conservative', 'nz-loyal': 'NZ Loyal', 'legalise-cannabis': 'Legalise Cannabis',
         'nz-outdoors-freedom': 'NZ Outdoors & Freedom', 'vision-nz': 'Vision NZ', 'animal-justice': 'Animal Justice',
         'womens-rights': "Women's Rights", 'alliance': 'Alliance', 'free-palestine': 'Free Palestine',
         'te-tai-tokerau-party': 'Te Tai Tokerau Party'}


def load(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return json.load(f)


def fmt(x, nd=1):
    return '–' if x is None else f'{x:.{nd}f}'


# ---------------------------------------------------------------- polls
POLLS = load('data/polls-2026.json')['polls']


def polls_in_window(days=30):
    start = SNAPSHOT - datetime.timedelta(days=days)
    out = []
    for p in POLLS:
        if p.get('is_election_result'):
            continue
        d = datetime.date.fromisoformat(p['end_date'])
        if start <= d <= SNAPSHOT:
            out.append(p)
    return out


def poll_average(polls):
    avg = {}
    for party in MAIN7:
        vals = [p['results'].get(party) for p in polls if p['results'].get(party) is not None]
        avg[party] = {'mean': sum(vals) / len(vals) if vals else None, 'min': min(vals) if vals else None,
                      'max': max(vals) if vals else None, 'n': len(vals)}
    return avg


def sainte_lague(votes, seats=SEATS):
    """votes: {party: share}. Returns {party: seats}."""
    quot = []
    for party, v in votes.items():
        for k in range(seats):
            quot.append((v / (2 * k + 1), party))
    quot.sort(reverse=True)
    alloc = collections.Counter(p for _, p in quot[:seats])
    return {p: alloc.get(p, 0) for p in votes}


def project(shares, electorates=None, threshold=5.0):
    """shares: {party: pct}; electorates: {party: electorate seats assumed won}. Returns (seats, house size, wasted %)."""
    electorates = electorates or {}
    qual = {p: v for p, v in shares.items() if v is not None and (v >= threshold or electorates.get(p, 0) > 0)}
    alloc = sainte_lague(qual)
    seats = {}
    for p, s in alloc.items():
        seats[p] = max(s, electorates.get(p, 0))
    for p, e in electorates.items():  # electorate-only winners with no party vote in the poll
        if p not in seats and e:
            seats[p] = e
    house = SEATS + sum(max(0, electorates.get(p, 0) - alloc.get(p, 0)) for p in seats)
    total = sum(v for v in shares.values() if v is not None)
    wasted = 100 - sum(v for p, v in shares.items() if p in qual)  # incl. 'others' implicitly
    return seats, house, wasted, total


# Scenario definitions (all use the 30-day poll average)
TPM_HELD = 4  # electorates Te Pāti Māori held at dissolution (Hauraki-Waikato, Tāmaki Makaurau, Te Tai Hauāuru, Waiariki)
SCENARIOS = [
    ('A', 'Threshold only: six parties ≥5% (incl. TOP); no electorate-only winners', {}, None),
    ('B', f'As A, plus Te Pāti Māori wins the {TPM_HELD} Māori seats it held at dissolution', {'te-pati-maori': TPM_HELD}, None),
    ('C', 'As B, plus Te Tai Tokerau Party (Kapa-Kingi) holds Te Tai Tokerau', {'te-pati-maori': TPM_HELD, 'te-tai-tokerau-party': 1}, None),
    ('D', 'As B, but TOP falls below 5% and wins no electorate', {'te-pati-maori': TPM_HELD}, 'opportunity'),
]
RIGHT = ['national', 'act', 'nz-first']
LEFT = ['labour', 'green', 'te-pati-maori']


def block_polls():
    w = polls_in_window()
    avg = poll_average(w)
    e23 = {p['party']: p['party_vote_pct'] for p in load('data/elections/2023.json')['parties']}
    pollsters = sorted(set(p['pollster'] for p in w))
    rows = ['| Party | 2023 result % | 30-day poll average % | Range in window | Change since 2023 (pp) |',
            '|---|---:|---:|---|---:|']
    for p in MAIN7:
        a = avg[p]
        ch = a['mean'] - e23[p] if a['mean'] is not None else None
        rows.append(f"| {NAMES[p]} | {e23[p]:.2f} | **{fmt(a['mean'])}** | {fmt(a['min'])}–{fmt(a['max'])} | "
                    f"{'+' if ch and ch > 0 else ''}{fmt(ch)} |")
    r = sum(avg[p]['mean'] for p in RIGHT)
    l = sum(avg[p]['mean'] for p in LEFT)
    rows.append(f"| *National + ACT + NZ First* | {sum(e23[p] for p in RIGHT):.2f} | **{r:.1f}** | | {r - sum(e23[p] for p in RIGHT):+.1f} |")
    rows.append(f"| *Labour + Green + Te Pāti Māori* | {sum(e23[p] for p in LEFT):.2f} | **{l:.1f}** | | {l - sum(e23[p] for p in LEFT):+.1f} |")
    rows.append('')
    rows.append(f"Window: {len(w)} polls with fieldwork ending {min(p['end_date'] for p in w)} to {max(p['end_date'] for p in w)} "
                f"({', '.join(pollsters)}). Simple unweighted mean; each poll counts once. Source rows: "
                f"[`data/polls-2026.json`](data/polls-2026.json) (from [Wikipedia's poll table](https://en.wikipedia.org/wiki/Opinion_polling_for_the_2026_New_Zealand_general_election), each row linked to the pollster's release).")
    return '\n'.join(rows), avg, w


def block_seats(avg, window):
    shares = {p: avg[p]['mean'] for p in MAIN7}
    order = MAIN7 + ['te-tai-tokerau-party']
    hdr = '| Scenario | ' + ' | '.join(NAMES[p] for p in order) + ' | House | Majority needs | Nat+ACT+NZF | Lab+Grn+TPM | Lab+Grn+TPM+TOP | Wasted vote % |'
    rows = [hdr, '|' + '---|' * (len(order) + 7)]
    for code, desc, elec, drop in SCENARIOS:
        # scenario D: the dropped party's votes stay in the denominator but win no seats
        s_use = {k: (0.0 if k == drop else v) for k, v in shares.items()}
        seats, house, _, _ = project(s_use, elec)
        maj = house // 2 + 1
        right = sum(seats.get(p, 0) for p in RIGHT)
        left = sum(seats.get(p, 0) for p in LEFT)
        lefttop = left + seats.get('opportunity', 0)
        cells = ' | '.join(str(seats.get(p, 0)) for p in order)
        wasted_pct = 100 - sum(v for p, v in s_use.items() if p in seats and v)
        rows.append(f"| **{code}** | {cells} | {house} | {maj} | {right}{' ✔' if right >= maj else ''} | {left}{' ✔' if left >= maj else ''} | "
                    f"{lefttop}{' ✔' if lefttop >= maj else ''} | {wasted_pct:.1f} |")
    rows.append('')
    for code, desc, elec, drop in SCENARIOS:
        rows.append(f"- **{code}**: {desc}.")
    rows.append('- ✔ = reaches a majority of the House on its own. "Wasted vote" = poll share of parties that win no seats '
                '(including "others", so it is 100 minus the qualifying parties\' combined share).')
    # Sensitivity: each poll in the window, scenario B
    tally = collections.Counter()
    detail = []
    for p in sorted(window, key=lambda x: x['end_date']):
        s = {k: p['results'].get(k) for k in MAIN7}
        seats, house, _, _ = project(s, {'te-pati-maori': TPM_HELD})
        maj = house // 2 + 1
        right = sum(seats.get(k, 0) for k in RIGHT)
        left = sum(seats.get(k, 0) for k in LEFT)
        top = seats.get('opportunity', 0)
        if right >= maj:
            res = 'Nat+ACT+NZF majority'
        elif left >= maj:
            res = 'Lab+Grn+TPM majority'
        elif top and right + top >= maj and left + top >= maj:
            res = 'TOP decides (either side + TOP)'
        elif top and left + top >= maj:
            res = 'Lab+Grn+TPM+TOP only'
        elif top and right + top >= maj:
            res = 'Nat+ACT+NZF+TOP only'
        else:
            res = 'no bloc majority'
        tally[res] += 1
        detail.append(f"| {p['date']} | [{p['pollster']}]({p['source_url']}) | {right} | {left} | {top} | {house} | {res} |")
    rows.append('')
    rows.append('**Sensitivity – every poll in the window, scenario B assumptions:**')
    rows.append('')
    rows.append('| Fieldwork | Pollster | Nat+ACT+NZF | Lab+Grn+TPM | TOP | House | Outcome |')
    rows.append('|---|---|---:|---:|---:|---:|---|')
    rows += detail
    rows.append('')
    rows.append('Tally: ' + '; '.join(f'{k}: {v}' for k, v in tally.most_common()) + '.')
    return '\n'.join(rows)


def block_quarters():
    q = collections.defaultdict(list)
    for p in POLLS:
        if p.get('is_election_result'):
            continue
        d = datetime.date.fromisoformat(p['end_date'])
        q[f'{d.year} Q{(d.month - 1) // 3 + 1}'].append(p)
    keys = sorted(q)
    means = {k: poll_average(q[k]) for k in keys}
    e23 = {p['party']: p['party_vote_pct'] for p in load('data/elections/2023.json')['parties']}
    rows = ['| Party | 2023 election | Highest quarter | Lowest quarter | Latest quarter (' + keys[-1] + ') | Swing election → latest quarter (pp) |',
            '|---|---:|---|---|---:|---:|']
    for p in MAIN7:
        series = [(k, means[k][p]['mean']) for k in keys if means[k][p]['mean'] is not None]
        hi = max(series, key=lambda x: x[1]); lo = min(series, key=lambda x: x[1])
        last = series[-1][1]
        rows.append(f"| {NAMES[p]} | {e23[p]:.1f} | {hi[1]:.1f} ({hi[0]}) | {lo[1]:.1f} ({lo[0]}) | {last:.1f} | {last - e23[p]:+.1f} |")
    lead = []
    for k in keys:
        n, l = means[k]['national']['mean'], means[k]['labour']['mean']
        lead.append(f"{k}: {'National' if n > l else 'Labour'} +{abs(n - l):.1f}")
    rows.append('')
    rows.append('Largest party by quarterly mean: ' + ' · '.join(lead) + '.')
    rows.append(f'Total polls since the 2023 election: {sum(len(v) for v in q.values())}. Quarterly means are simple averages of polls whose fieldwork ended in that quarter.')
    return '\n'.join(rows)


# ---------------------------------------------------------------- elections
YEARS = [2008, 2011, 2014, 2017, 2020, 2023]


def block_system():
    rows = ['| Election | Turnout % (of enrolled) | Parties on party-vote ballot | Parties winning seats | Effective no. of parties (votes) | Effective no. of parties (seats) | Gallagher disproportionality | "Wasted" party vote % | Overhang | Nat+Lab share % |',
            '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for y in YEARS:
        d = load(f'data/elections/{y}.json')
        ps = [p for p in d['parties'] if p.get('party_vote_pct') is not None]
        v = [p['party_vote_pct'] / 100 for p in ps]
        enp_v = 1 / sum(x * x for x in v)
        tot = sum(p.get('total_seats') or 0 for p in d['parties'])
        s = [(p.get('total_seats') or 0) / tot for p in d['parties']]
        enp_s = 1 / sum(x * x for x in s if x)
        seatmap = {p['party']: (p.get('total_seats') or 0) / tot * 100 for p in d['parties']}
        gall = math.sqrt(0.5 * sum((p['party_vote_pct'] - seatmap.get(p['party'], 0)) ** 2 for p in ps))
        winners = sum(1 for p in d['parties'] if (p.get('total_seats') or 0) > 0)
        nl = sum(p['party_vote_pct'] for p in ps if p['party'] in ('national', 'labour'))
        wasted = d.get('wasted_party_vote_pct')
        if wasted is None:
            wasted = sum(p['party_vote_pct'] for p in ps if not (p.get('total_seats') or 0))
        rows.append(f"| {y} | {d['turnout_pct']} | {len(ps)} | {winners} | {enp_v:.2f} | {enp_s:.2f} | {gall:.2f} | {wasted:.2f} | {d.get('overhang')} | {nl:.1f} |")
    rows.append('')
    rows.append('Effective number of parties = 1 / Σ(share²) (Laakso–Taagepera). Gallagher index = √(½ Σ(vote% − seat%)²); lower is more proportional. '
                'Seat shares use final seat totals in `data/elections/<year>.json` (2023 includes the Port Waikato by-election seat). '
                'Computed by `tools/report_stats.py` from [`data/elections/`](data/elections/).')
    return '\n'.join(rows)


def block_votes():
    avg = poll_average(polls_in_window())
    cols = YEARS
    rows = ['| Party | ' + ' | '.join(map(str, cols)) + ' | Oct 2026 polls |', '|---|' + '---:|' * (len(cols) + 1)]
    data = {y: {p['party']: p for p in load(f'data/elections/{y}.json')['parties']} for y in cols}
    for party in MAIN7:
        cells = []
        for y in cols:
            p = data[y].get(party)
            cells.append('–' if not p else f"{p['party_vote_pct']:.1f} ({p.get('total_seats') or 0})")
        rows.append(f"| {NAMES[party]} | " + ' | '.join(cells) + f" | {fmt(avg[party]['mean'])} |")
    rows.append('')
    rows.append('Party-vote % (total seats in brackets). Source: [`data/elections/`](data/elections/); Oct 2026 = 30-day poll average (no seats).')
    return '\n'.join(rows)


def block_maori():
    rows = ['| Election | Labour | Māori Party / Te Pāti Māori | Mana | TPM party vote % |', '|---|---:|---:|---:|---:|']
    for y in YEARS:
        d = load(f'data/elections/{y}.json')
        c = collections.Counter(e['party'] for e in d['electorates'] if e.get('type') == 'maori')
        tpm = next((p['party_vote_pct'] for p in d['parties'] if p['party'] == 'te-pati-maori'), None)
        rows.append(f"| {y} | {c.get('labour', 0)} | {c.get('te-pati-maori', 0)} | {c.get('mana', 0)} | {fmt(tpm, 2)} |")
    rows.append('')
    rows.append('Winners of the seven Māori electorates (from `data/elections/<year>.json`). At dissolution (Oct 2026) the seven were held by Te Pāti Māori 4, Labour 1, '
                'Te Tai Tokerau Party 1 and an independent 1 ([`data/parliaments/54.json`](data/parliaments/54.json); [electorates/README.md](electorates/README.md)).')
    return '\n'.join(rows)


def block_parliament():
    p = load('data/parliaments/54.json')
    a, b = p['composition_start'], p['composition_now_or_end']
    keys = ['national', 'labour', 'green', 'act', 'nz-first', 'te-pati-maori', 'independent']
    rows = ['| Party | Start (Dec 2023) | Dissolution (1 Oct 2026) |', '|---|---:|---:|']
    for k in keys:
        rows.append(f"| {NAMES.get(k, k.title())} | {a.get(k, 0)} | {b.get(k, 0)} |")
    rows.append(f"| **Total** | {p['total_start']} | {p['total_now_or_end']} |")
    gov_a = sum(a.get(k, 0) for k in RIGHT); gov_b = sum(b.get(k, 0) for k in RIGHT)
    rows.append('')
    rows.append(f"Government (National+ACT+NZ First): {gov_a} of {p['total_start']} at the start, {gov_b} of {p['total_now_or_end']} at dissolution "
                f"(Papakura vacant after Judith Collins resigned on 14 May 2026). Source: [`data/parliaments/54.json`](data/parliaments/54.json).")
    return '\n'.join(rows)


# ---------------------------------------------------------------- promises
PROMISE_PARTIES = ['national', 'labour', 'green', 'act', 'nz-first', 'te-pati-maori', 'united-future', 'mana']
STATUSES = ['kept', 'partially-kept', 'broken', 'abandoned', 'in-progress', 'not-yet-due']
TERMS = ['2008–11', '2011–14', '2014–17', '2017–20', '2020–23', '2023–26']
# Role of each party in each term: G = led government / coalition partner, S = support partner (C&S or cooperation),
# O = opposition, X = outside Parliament. Sources: party READMEs and data/elections/<year>.json 'government'.
ROLE = {
    'national':      dict(zip(TERMS, 'G G G O O G'.split())),
    'labour':        dict(zip(TERMS, 'O O O G G O'.split())),
    'green':         dict(zip(TERMS, 'O O O S S O'.split())),
    'act':           dict(zip(TERMS, 'S S S O O G'.split())),
    'nz-first':      dict(zip(TERMS, 'X O O G X G'.split())),
    'te-pati-maori': dict(zip(TERMS, 'S S S X O O'.split())),
    'united-future': dict(zip(TERMS, 'S S S X X X'.split())),
    'mana':          dict(zip(TERMS, 'X O X X X X'.split())),
}


def term_of(entry, party):
    made = entry.get('made', '')
    if party == 'labour' and entry.get('term'):
        t = entry['term']
        if t.startswith('2017-2020'):
            return '2017–20'
        if t.startswith('2020-2023'):
            return '2020–23'
        if t.startswith('2026'):
            return '2026'
        if 'Opposition 2023' in t:
            return '2023–26'
    if made.lower().startswith(('long-standing', 'standing')):
        return 'long-standing'
    years = [int(y) for y in re.findall(r'(20\d\d)', made) if int(y) >= 2008]
    if not years:
        return 'long-standing'
    y = years[0]
    if y >= 2026:
        return '2026'
    for t in TERMS:
        a = int(t[:4])
        if a <= y < a + 3:
            return t
    return 'long-standing'


def promises():
    out = {}
    for p in PROMISE_PARTIES:
        out[p] = load(f'data/promises/{p}.json')
    return out


def counts(entries):
    c = collections.Counter(e['status'] for e in entries)
    res = sum(c[s] for s in ['kept', 'partially-kept', 'broken', 'abandoned'])
    idx = (c['kept'] + 0.5 * c['partially-kept']) / res if res else None
    kp = (c['kept'] + c['partially-kept']) / res if res else None
    return c, res, idx, kp


def pct(x):
    return '–' if x is None else f'{100 * x:.0f}%'


def block_promises_overall():
    P = promises()
    rows = ['| Party | Entries | Kept | Partly kept | Broken | Abandoned | In progress | Not yet due (2026) | Resolved | Kept % | Kept or partly % | Delivery index |',
            '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in PROMISE_PARTIES:
        c, res, idx, kp = counts(P[p])
        rows.append(f"| [{NAMES[p]}](parties/{p}/track-record.md) | {len(P[p])} | {c['kept']} | {c['partially-kept']} | {c['broken']} | {c['abandoned']} | "
                    f"{c['in-progress']} | {c['not-yet-due']} | {res} | {pct(c['kept'] / res if res else None)} | {pct(kp)} | {pct(idx)} |")
    rows.append('')
    rows.append('All entries in [`data/promises/`](data/promises/). Percentages are of *resolved* entries (kept + partly + broken + abandoned). '
                'Delivery index = (kept + ½ partly kept) ÷ resolved. Includes promises from campaigns a party lost, which are mostly "abandoned" – see the next table.')
    return '\n'.join(rows)


def block_promises_role():
    P = promises()
    rows = ['| Party | In office (govt or coalition): resolved / index | As support partner: resolved / index | Opposition or out of Parliament: resolved / index | Long-standing / undated: resolved |',
            '|---|---|---|---|---|']
    for p in PROMISE_PARTIES:
        buckets = collections.defaultdict(list)
        for e in P[p]:
            t = term_of(e, p)
            if t == '2026':
                continue
            if t == 'long-standing':
                buckets['L'].append(e); continue
            r = ROLE[p].get(t, 'O')
            buckets['O' if r in ('O', 'X') else r].append(e)
        cell = []
        for k in ['G', 'S', 'O']:
            c, res, idx, kp = counts(buckets[k])
            if res:
                cell.append(f"{res} / **{pct(idx)}** ({c['kept']}✅ {c['partially-kept']}🟡 {c['broken']}❌ {c['abandoned']}⛔)")
            else:
                cell.append('–')
        cL = counts(buckets['L'])[1]
        rows.append(f"| {NAMES[p]} | " + ' | '.join(cell) + f" | {cL or '–'} |")
    rows.append('')
    rows.append('Each entry is assigned to the parliamentary term following the election or agreement at which the promise was made (from its `made` field; Labour\'s file also has a `term` field, used where present). '
                'Roles: National led governments 2008–17 and 2023–26; Labour 2017–23; ACT and the Māori Party were National\'s support partners 2008–17 and ACT a coalition partner from 2023; '
                'United Future a support partner 2008–17; the Greens a support partner 2017–23 (confidence & supply, then a cooperation agreement); NZ First a coalition partner 2017–20 and 2023–26. '
                'Sources: party READMEs and `government` in [`data/elections/`](data/elections/).')
    return '\n'.join(rows)


def block_promises_terms():
    P = promises()
    hdr = '| Party | ' + ' | '.join(TERMS) + ' | 2026 (not yet due) |'
    rows = [hdr, '|---|' + '---|' * (len(TERMS) + 1)]
    for p in PROMISE_PARTIES:
        by = collections.defaultdict(list)
        for e in P[p]:
            by[term_of(e, p)].append(e)
        cells = []
        for t in TERMS:
            c, res, idx, kp = counts(by[t])
            role = ROLE[p][t]
            tag = {'G': 'govt', 'S': 'support', 'O': 'opp', 'X': 'out'}[role]
            if res or c['in-progress']:
                cells.append(f"{c['kept']}/{c['partially-kept']}/{c['broken']}/{c['abandoned']}" + (f" +{c['in-progress']}⏳" if c['in-progress'] else '') + f" *({tag})*")
            else:
                cells.append(f"· *({tag})*")
        nyd = sum(1 for e in P[p] if e['status'] == 'not-yet-due')
        cells.append(str(nyd) if nyd else '–')
        rows.append(f"| {NAMES[p]} | " + ' | '.join(cells) + ' |')
    rows.append('')
    rows.append('Cells: kept / partly kept / broken / abandoned (+ in progress ⏳); role in that term in italics. "·" = no tracked promises for that term. '
                'The last column counts every entry with status not-yet-due (including a few 2023 promises carried into 2026 platforms). A few entries without a datable election (e.g. "long-standing policy") are omitted from this table but counted above.')
    return '\n'.join(rows)


def block_policies():
    gp = load('data/guide/parties.json')['parties']
    rows = ['| Party | 2026 policies in archive | Most common topics | Policy list |', '|---|---:|---|---|']
    total = 0
    for p in gp:
        slug = p['slug']
        path = os.path.join(ROOT, f'parties/{slug}/policies/policies.json')
        d = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else []
        total += len(d)
        c = collections.Counter(t for x in d for t in (x.get('topics') or []))
        top = ', '.join(t for t, _ in c.most_common(3))
        rows.append(f"| {NAMES.get(slug, p['short_name'])} | {len(d)} | {top} | [policies](parties/{slug}/policies/README.md) |")
    rows.append('')
    rows.append(f'{total} policies across the 17 registered parties (electorate-only groups hold the rest of the archive\'s 1,435). Topic labels are policy.nz\'s where available. '
                'Counts reflect how parties publish (the Greens itemise their whole manifesto and 40 policy papers), not how much they plan to do.')
    return '\n'.join(rows)


def block_quiz():
    q = load('data/guide/quiz.json')
    sym = {2: '**++**', 1: '+', 0: '0', -1: '−', -2: '**−−**', None: '·'}
    short = {'national': 'Nat', 'labour': 'Lab', 'green': 'Grn', 'act': 'ACT', 'nz-first': 'NZF', 'te-pati-maori': 'TPM', 'opportunity': 'TOP'}
    rows = ['| # | Statement | ' + ' | '.join(short[p] for p in MAIN7) + ' |', '|---|---|' + ':---:|' * len(MAIN7)]
    for st in q['statements']:
        cells = [sym[(st['positions'].get(p) or {}).get('position')] for p in MAIN7]
        if all(c == '·' for c in cells):
            continue
        rows.append(f"| {st['id']} | {st['text']} | " + ' | '.join(cells) + ' |')
    rows.append('')
    rows.append('++ strongly agree · + agree · 0 neutral/mixed · − disagree · −− strongly disagree · "·" no public position found (never guessed). '
                'Every cell has a quoted piece of evidence and a source URL in [`data/guide/quiz.json`](data/guide/quiz.json); coding rules in [guide/quiz-method.md](guide/quiz-method.md). '
                'Statements on which none of the seven has a recorded position are omitted.')
    return '\n'.join(rows)


BLOCKS = {
    'quiz': block_quiz,
    'polls': None, 'seats': None, 'quarters': block_quarters, 'system': block_system, 'votes': block_votes,
    'maori': block_maori, 'parliament': block_parliament, 'promises-overall': block_promises_overall,
    'promises-role': block_promises_role, 'promises-terms': block_promises_terms, 'policies': block_policies,
}


def build_all():
    out = {}
    polls_md, avg, window = block_polls()
    out['polls'] = polls_md
    out['seats'] = block_seats(avg, window)
    for k, f in BLOCKS.items():
        if f:
            out[k] = f()
    return out


def write(blocks, path=None):
    path = path or os.path.join(ROOT, 'REPORT.md')
    txt = open(path, encoding='utf-8').read()
    for k, v in blocks.items():
        pat = re.compile(rf'(<!-- GENERATED:report-{re.escape(k)} START -->\n).*?(<!-- GENERATED:report-{re.escape(k)} END -->)', re.S)
        if pat.search(txt):
            txt = pat.sub(lambda m: m.group(1) + v + '\n' + m.group(2), txt)
        else:
            print(f'warning: no marker for {k}', file=sys.stderr)
    open(path, 'w', encoding='utf-8').write(txt)


if __name__ == '__main__':
    b = build_all()
    if '--write' in sys.argv:
        i = sys.argv.index('--write')
        target = sys.argv[i + 1] if len(sys.argv) > i + 1 else None
        write(b, target)
        print((target or 'REPORT.md') + ' generated blocks updated:', ', '.join(b))
    else:
        for k, v in b.items():
            print(f'\n===== {k}\n{v}')
