#!/usr/bin/env python3
"""Fill the computed fields of data/guide/parties.json in place.

* polling_avg_2026  - simple mean of every published poll in data/polls-2026.json whose
                      fieldwork/sort date falls in the 30 days up to the guide's as_of date.
                      Minor parties are not reported separately by public pollsters, so for
                      them we record policy.nz's own '2026 polling average' figure instead.
* track_record_line - one sentence built from data/promises/<slug>.json status counts
                      (the same data behind parties/<slug>/track-record.md) plus the
                      hand-written track_record_context.

Run:  python3 tools/guide_enrich.py   (idempotent; re-run whenever polls or promises change)
"""
import json, pathlib, datetime, statistics, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTIES = ROOT / 'data' / 'guide' / 'parties.json'
POLLS = ROOT / 'data' / 'polls-2026.json'
PROMISES = ROOT / 'data' / 'promises'
POLICYNZ = ROOT / 'raw' / 'policy.nz' / 'parties'
WINDOW_DAYS = 30

# archive slug -> policy.nz file slug
PNZ = {
    'national': 'national-party', 'labour': 'labour-party', 'green': 'green-party', 'act': 'act-party',
    'nz-first': 'nz-first', 'te-pati-maori': 'te-pati-maori', 'opportunity': 'opportunity-party',
    'nz-loyal': 'new-zealand-loyal', 'nz-outdoors-freedom': 'nz-outdoors--freedom-party',
    'legalise-cannabis': 'aotearoa-legalise-cannabis-party', 'animal-justice': 'animal-justice-party',
    'alliance': 'alliance-party', 'conservative': 'conservative-party-nz', 'womens-rights': 'womens-rights-party',
    'vision-nz': 'vision-nz', 'free-palestine': 'free-palestine', 'te-tai-tokerau-party': 'te-tai-tokerau-party',
}


def fmt(x):
    return ('%.1f' % x).rstrip('0').rstrip('.') if x is not None else None


def polling(guide):
    data = json.loads(POLLS.read_text())
    asof = datetime.date.fromisoformat(guide['as_of'])
    start = asof - datetime.timedelta(days=WINDOW_DAYS)
    rows = [p for p in data['polls'] if not p.get('is_election_result')
            and start <= datetime.date.fromisoformat(p['end_date']) <= asof]
    rows.sort(key=lambda p: p['end_date'])
    polled = set(data['parties'].values())
    out = {}
    for party in guide['parties']:
        slug = party['slug']
        if slug in polled:
            vals = [p['results'][slug] for p in rows if p['results'].get(slug) is not None]
            if not vals:
                continue
            out[slug] = {
                'average_pct': round(statistics.mean(vals), 1),
                'min_pct': min(vals), 'max_pct': max(vals),
                'polls': len(vals),
                'window': f"{start.isoformat()} to {asof.isoformat()}",
                'latest_poll': {'pollster': rows[-1]['pollster'], 'end_date': rows[-1]['end_date'],
                                'pct': rows[-1]['results'].get(slug), 'source': rows[-1]['source_url']},
                'method': f'Simple mean of all {len(vals)} published party-vote polls with fieldwork ending in the '
                          f'{WINDOW_DAYS} days to {asof.isoformat()} (no weighting).',
                'pollsters': sorted({p['pollster'] for p in rows}),
                'sources': ['data/polls-2026.json', data['source']] + [p['source_url'] for p in rows if p.get('source_url')],
            }
        else:
            f = POLICYNZ / (PNZ[slug] + '.json')
            attrs = {a['name']: a['value'] for a in json.loads(f.read_text())['party'].get('attributes', [])}
            val = attrs.get('2026 polling average')
            out[slug] = {
                'average_pct': None,
                'policy_nz_figure': val,
                'method': ('Not reported separately in the main public polls (pollsters group it under "other"). '
                           + (f"policy.nz lists its 2026 polling average as {val}." if val else
                              'policy.nz gives no polling figure for it.')),
                'sources': [f"https://policy.nz/2026/party-vote/parties/{PNZ[slug]}", 'raw/policy.nz/parties/' + f.name],
                'retrieved': '2026-10-23',
            }
    return out


LABEL = [('kept', 'kept'), ('partially-kept', 'partly kept'), ('broken', 'broken'),
         ('abandoned', 'abandoned'), ('in-progress', 'still in progress')]


def track_line(party):
    ctx = party.get('track_record_context', '').strip()
    f = PROMISES / (party['slug'] + '.json')
    if not f.exists():
        return ctx + (' This archive has no promise tracker for it.' if party.get('current_seats', {}).get('seats') else '')
    d = json.loads(f.read_text())
    if isinstance(d, dict):
        d = d.get('promises', d.get('entries', []))
    c = collections.Counter(x.get('status') for x in d)
    past = sum(v for k, v in c.items() if k != 'not-yet-due')
    bits = [f"{c[k]} {lab}" for k, lab in LABEL if c.get(k)]
    line = (f"{ctx} Of {past} past promises checked in this archive's tracker: " + ', '.join(bits) + '.')
    if c.get('not-yet-due'):
        line += f" ({c['not-yet-due']} 2026 promises are tracked but not yet due.)"
    return line.strip()


def main():
    guide = json.loads(PARTIES.read_text())
    polls = polling(guide)
    for party in guide['parties']:
        party['polling_avg_2026'] = polls.get(party['slug'])
        party['track_record_line'] = track_line(party)
        tf = party.get('track_record_file')
        if tf and not (ROOT / tf).exists():
            party['track_record_file_status'] = 'not yet written'
        else:
            party.pop('track_record_file_status', None)
    guide['enriched'] = datetime.date.today().isoformat()
    PARTIES.write_text(json.dumps(guide, ensure_ascii=False, indent=2) + '\n')
    for p in guide['parties']:
        pa = p['polling_avg_2026'] or {}
        print(f"{p['slug']:22} poll={pa.get('average_pct')!s:6} n={pa.get('polls','-')!s:3} | {p['track_record_line'][:110]}")


if __name__ == '__main__':
    main()
