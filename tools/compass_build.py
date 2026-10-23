#!/usr/bin/env python3
"""Build data/guide/compass.json and data/guide/compass-parties.json.

  python3 -I tools/compass_build.py

Inputs: tools/compass_items.py (item bank + licences), tools/compass_party_coding.py (hand-coded party
answers), tools/compass_published.py (expert / manifesto / voter-survey placements from raw/compass/).
"""
import json, math, os, sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compass_items import ITEMS, AXES  # noqa: E402
from compass_party_coding import CODING, PARTY_KEYS, PARTY_NAMES  # noqa: E402
from compass_published import build_published  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, 'data', 'guide')
TODAY = '2026-10-23'
SLUG_ALIASES = {'new-conservative': 'conservative'}  # New Conservative (2017-2026) is the same registered party, renamed Conservative Party NZ in 2026

SCORING = {
    'response_values': {'likert5': '-2 strongly disagree, -1 disagree, 0 neither, +1 agree, +2 strongly agree; a skipped item is null',
                        'feeling5': '-2 very negative, -1 negative, 0 neutral, +1 positive, +2 very positive; a skipped item is null'},
    'keyed_score': 'keyed_i = direction_i * response_i   (so +2 always means the right / TAN-authoritarian / populist pole)',
    'axis_score': 'axis = 5 * mean(keyed_i over answered items on that axis), giving -10 (left / GAL-libertarian / pluralist) .. +10 (right / TAN-authoritarian / populist)',
    'min_items': {a: AXES[a]['min_items'] for a in AXES},
    'min_items_rule': 'If fewer than min_items on an axis were answered, do not show a point on that axis; show "not enough answers" instead.',
    'uncertainty': {
        'method': 'half-width = max(1.0, 1.96 * 5 * sd(keyed_i) / sqrt(n))  where sd is the sample standard deviation of the keyed item scores on that axis and n the number answered. The floor of 1.0 reflects that even a complete, perfectly consistent set of 5-point answers cannot locate a person more finely than about one unit on a 20-unit axis.',
        'display': 'Show the point with an error bar (or shaded band) of +/- half-width, and the text "based on n of N items". With all items answered and sd = 0 the band is +/-1.0.',
        'n_total': {a: sum(1 for i in ITEMS if i['axis'] == a) for a in AXES},
    },
    'subscales': 'Each item carries a "subscale" tag (SECS economic, SECS social, VSA authoritarianism, CSES populism, WVS economic values, CSES out-group, ESS, NZES). A subscale score is 5 * mean(keyed_i) over the answered items with that tag; show it only when at least half of the subscale\'s items were answered. SECS subscale scores can also be shown on Everett\'s original 0-100 metric: secs_0_100 = 50 + 12.5 * mean(keyed_i) (equivalent to mapping -2..+2 onto 25..75; a fully "very positive" conservative answer set scores 75, not 100, because the 5-point version compresses the thermometer).',
    'acquiescence': 'Within each axis roughly half the items are reverse-keyed (economic 6/6, social 10 TAN-keyed / 6 GAL-keyed, populism 7/1). A respondent who agrees with everything therefore lands near 0 on the economic axis; on the populism axis the CSES battery is mostly protrait, so the app should treat a populism score as indicative only and show it as a secondary axis.',
    'party_comparison': 'Parties are scored with the same formula from their coded answers (data/guide/compass-parties.json: coded.axes). Distance between a user and a party on the two main axes is the Euclidean distance in the -10..+10 plane, shown only for axes where both have enough items.',
}

def party_slug(k):
    return PARTY_KEYS[k]

def item_index():
    return {i['id']: i for i in ITEMS}

def score_axes(answers_by_item, items=ITEMS):
    """answers_by_item: {item_id: response(-2..2)}; returns per-axis dict."""
    idx = item_index()
    by_axis = defaultdict(list)
    for iid, resp in answers_by_item.items():
        if resp is None:
            continue
        it = idx[iid]
        by_axis[it['axis']].append(it['direction'] * resp)
    out = {}
    for axis, cfg in AXES.items():
        ks = by_axis.get(axis, [])
        n = len(ks); n_total = sum(1 for i in items if i['axis'] == axis)
        if n == 0:
            out[axis] = {'score': None, 'n_items': 0, 'n_total': n_total, 'enough': False, 'half_width': None}
            continue
        mean = sum(ks) / n
        sd = math.sqrt(sum((k - mean) ** 2 for k in ks) / (n - 1)) if n > 1 else 0.0
        hw = max(1.0, 1.96 * 5 * sd / math.sqrt(n))
        out[axis] = {'score': round(5 * mean, 2), 'n_items': n, 'n_total': n_total, 'enough': n >= cfg['min_items'],
                     'half_width': round(hw, 2), 'keyed_mean': round(mean, 3), 'keyed_sd': round(sd, 3)}
    return out

def score_subscales(answers_by_item):
    idx = item_index()
    tags = defaultdict(list); totals = Counter(i['subscale'] for i in ITEMS)
    for iid, resp in answers_by_item.items():
        if resp is None:
            continue
        it = idx[iid]
        tags[it['subscale']].append(it['direction'] * resp)
    out = {}
    for tag, total in totals.items():
        ks = tags.get(tag, [])
        if not ks:
            out[tag] = {'score': None, 'n_items': 0, 'n_total': total}
            continue
        mean = sum(ks) / len(ks)
        d = {'score': round(5 * mean, 2), 'n_items': len(ks), 'n_total': total, 'shown': len(ks) * 2 >= total}
        if tag.startswith('secs'):
            d['secs_0_100'] = round(50 + 12.5 * mean, 1)
        out[tag] = d
    return out

def build_compass():
    items = []
    for it in ITEMS:
        items.append({
            'id': it['id'], 'axis': it['axis'], 'direction': it['direction'], 'text': it['text'],
            'scale': it['scale'], 'subscale': it['subscale'], 'item_ref': it['item_ref'], 'note': it['note'],
            'source': it['source'],
        })
    balance = {}
    for a in AXES:
        pos = sum(1 for i in ITEMS if i['axis'] == a and i['direction'] == 1)
        neg = sum(1 for i in ITEMS if i['axis'] == a and i['direction'] == -1)
        balance[a] = {'keyed_plus': pos, 'keyed_minus': neg, 'total': pos + neg}
    return {
        'version': '2026-10',
        'generated': TODAY,
        'about': 'A general political-values test ("compass"): 36 items from openly licensed or public survey instruments, scored onto an economic left-right axis, a GAL-TAN social axis and a secondary populism axis. Items are deliberately NOT about New Zealand election issues (see data/guide/quiz.json for that); parties are placed on the same axes from published expert data and from our own coding of their documents (data/guide/compass-parties.json).',
        'method_page': 'guide/compass-method.md',
        'axes': AXES,
        'direction_key': '+1 = agreeing (or feeling positive) moves the respondent toward the right / TAN-authoritarian / populist pole; -1 = reverse-keyed item.',
        'balance': balance,
        'scoring': SCORING,
        'instruments': sorted({i['source']['instrument'] for i in ITEMS}),
        'items': items,
    }

def build_parties(published):
    idx = item_index()
    parties = {}
    for k, slug in PARTY_KEYS.items():
        answers = {}; cells = {}
        for iid in idx:
            cell = CODING.get(iid, {}).get(k)
            cells[iid] = cell
            answers[iid] = cell['position'] if cell else None
        axes = score_axes(answers)
        subs = score_subscales(answers)
        conf = Counter(c['confidence'] for c in cells.values() if c)
        parties[slug] = {
            'name': PARTY_NAMES[slug],
            'coded': {
                'items': cells,
                'n_coded': sum(1 for c in cells.values() if c),
                'n_items': len(idx),
                'confidence_counts': dict(conf),
                'axes': axes,
                'subscales': subs,
            },
            'published': defaultdict(list),
        }
    # attach published placements per party
    for src in published['sources']:
        for row in src['parties']:
            slug = SLUG_ALIASES.get(row['party'], row['party'])
            if slug not in parties:
                parties.setdefault(slug, {'name': slug, 'coded': None, 'published': defaultdict(list)})
            entry = dict(row); entry.pop('party', None)
            if row['party'] in SLUG_ALIASES:
                entry['party_name_in_source'] = row['party']
            parties[slug]['published'][src['id']].append(entry)
    # comparison: our economic/social vs GPS (the only multi-expert 2D source) and vs ParlGov expert composites
    for slug, p in parties.items():
        p['published'] = dict(p['published'])
        if not p.get('coded'):
            continue
        comp = {}
        gps_rows = p['published'].get('gps2019', [])
        if gps_rows:
            g = gps_rows[0]['rescaled']
            for a in ('economic', 'social', 'populism'):
                ours = p['coded']['axes'][a]['score']
                comp[f'gps2019_{a}'] = {'ours': ours, 'published': g[a], 'difference_ours_minus_published': None if ours is None else round(ours - g[a], 2)}
        pg = [r for r in p['published'].get('parlgov', []) if r['based_on_expert_surveys']]
        if pg:
            for a in ('economic', 'social'):
                ours = p['coded']['axes'][a]['score']; pub = pg[0]['rescaled'][a]
                comp[f'parlgov_{a}'] = {'ours': ours, 'published': pub, 'difference_ours_minus_published': None if ours is None or pub is None else round(ours - pub, 2)}
        vp = [r for r in p['published'].get('vparty_v2', []) if r['election_year'] == 2017]
        if vp:
            ours = p['coded']['axes']['economic']['score']; pub = vp[0]['rescaled']['economic']
            comp['vparty2017_economic'] = {'ours': ours, 'published': pub, 'difference_ours_minus_published': None if ours is None or pub is None else round(ours - pub, 2)}
            ours_p = p['coded']['axes']['populism']['score']; pub_p = vp[0]['rescaled']['populism']
            comp['vparty2017_populism'] = {'ours': ours_p, 'published': pub_p, 'difference_ours_minus_published': None if ours_p is None or pub_p is None else round(ours_p - pub_p, 2)}
        nz = [r for r in p['published'].get('nzes_voters', []) if r['election_year'] == 2023]
        if nz:
            comp['nzes2023_voters_general_left_right'] = {'ours_economic': p['coded']['axes']['economic']['score'], 'published_general_left_right': nz[0]['rescaled']['general_left_right_voters'],
                                                          'note': 'voters\' general left-right placement, not an economic-only scale'}
        p['comparison'] = comp
    return parties

def render_method(compass, parties):
    body = open(os.path.join(ROOT, 'tools', 'compass_method_body.md'), encoding='utf-8').read()
    lines = [body.rstrip(), '', '## Appendix A. Per-item table', '',
             'Direction: +1 = agreeing (or feeling positive) scores toward the right / TAN-authoritarian / populist pole; -1 = reverse-keyed. Scale: L = 5-point agree/disagree, T = 5-point feeling thermometer (SECS). Coded = number of the 17 parties with a non-null coded answer.', '',
             '| # | Axis | Id | Item text | Dir | Scale | Instrument / item ref | Licence | Coded |', '|---|---|---|---|---|---|---|---|---|']
    for n, it in enumerate(compass['items'], 1):
        coded = sum(1 for p in parties.values() if p.get('coded') and p['coded']['items'].get(it['id']))
        sc = 'T' if it['scale']['type'] == 'feeling5' else 'L'
        lic = it['source']['licence'].split('(')[0].split(';')[0].strip()
        lines.append(f"| {n} | {it['axis']} | `{it['id']}` | {it['text']} | {it['direction']:+d} | {sc} | {it['source']['instrument'].split(',')[0]}: {it['item_ref']} | {lic} | {coded} |")
    lines += ['', '## Appendix B. Party coding coverage and axis scores (our coding)', '',
              'Scores use the same formula as the user test; "-" means fewer items than the minimum for that axis (economic 6, social 8, populism 4). Band = +/- half-width.', '',
              '| Party | Items coded (of 36) | high / medium / low | Economic (n) | Social (n) | Populism (n) |', '|---|---|---|---|---|---|']
    def fmt(ax):
        if not ax['enough']:
            return f"- ({ax['n_items']})"
        return f"{ax['score']:+.1f} ± {ax['half_width']:.1f} ({ax['n_items']})"
    for slug, p in parties.items():
        c = p.get('coded')
        if not c:
            continue
        cc = c['confidence_counts']
        ax = c['axes']
        lines.append(f"| {p['name']} | {c['n_coded']} | {cc.get('high',0)} / {cc.get('medium',0)} / {cc.get('low',0)} | {fmt(ax['economic'])} | {fmt(ax['social'])} | {fmt(ax['populism'])} |")
    lines += ['', '## Appendix C. Published placements rescaled to -10..+10, next to our coding', '',
              'GPS = Global Party Survey 2019 (12 experts, 2017 parties); V-Party = V-Party v2 coding of the 2017 election; ParlGov = expert-survey composite (expert-based rows only); NZES = voters\' mean general left-right placement, 2023 (B5) and 2020 (B7); CSES = NZES collaborator\'s expert general left-right placement, 2020 and 2017. General left-right values are shown in the economic column in italics because they are not economic-only scales.', '',
              '| Party | Ours econ / social / populism | GPS econ / social / populism | V-Party 2017 econ / populism | ParlGov state-market / liberty-authority | NZES voters 2023 (2020) | CSES expert 2020 (2017) |', '|---|---|---|---|---|---|---|']
    def sc(v):
        return '-' if v is None else f"{v:+.1f}"
    for slug, p in parties.items():
        c = p.get('coded'); pub = p.get('published', {})
        ours = '-' if not c else ' / '.join(sc(c['axes'][a]['score']) if c['axes'][a]['enough'] else '-' for a in ('economic', 'social', 'populism'))
        g = pub.get('gps2019'); gs = '-' if not g else ' / '.join(sc(g[0]['rescaled'][a]) for a in ('economic', 'social', 'populism'))
        v = [r for r in pub.get('vparty_v2', []) if r['election_year'] == 2017]; vs = '-' if not v else f"{sc(v[0]['rescaled']['economic'])} / {sc(v[0]['rescaled']['populism'])}"
        pg = [r for r in pub.get('parlgov', []) if r['based_on_expert_surveys']]; ps = '-' if not pg else f"{sc(pg[0]['rescaled']['economic'])} / {sc(pg[0]['rescaled']['social'])}"
        nz23 = [r for r in pub.get('nzes_voters', []) if r['election_year'] == 2023]; nz20 = [r for r in pub.get('nzes_voters', []) if r['election_year'] == 2020]
        ns = ('*' + sc(nz23[0]['rescaled']['general_left_right_voters']) + '*' if nz23 else '-') + (f" (*{sc(nz20[0]['rescaled']['general_left_right_voters'])}*)" if nz20 else '')
        c20 = [r for r in pub.get('cses5', []) if r['election_year'] == 2020]; c17 = [r for r in pub.get('cses5', []) if r['election_year'] == 2017]
        cs = ('*' + sc(c20[0]['rescaled']['general_left_right_expert']) + '*' if c20 else '-') + (f" (*{sc(c17[0]['rescaled']['general_left_right_expert'])}*)" if c17 else '')
        if ours == '-' and gs == '-' and vs == '-' and ps == '-' and ns == '-' and cs == '-':
            continue
        lines.append(f"| {p['name']} | {ours} | {gs} | {vs} | {ps} | {ns} | {cs} |")
    lines += ['', f'*Generated by `tools/compass_build.py` on {TODAY}; the prose above is maintained in `tools/compass_method_body.md`.*', '']
    with open(os.path.join(ROOT, 'guide', 'compass-method.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def main():
    compass = build_compass()
    published = build_published()
    parties = build_parties(published)
    out_parties = {
        'version': '2026-10', 'generated': TODAY,
        'about': 'NZ party placements on the compass axes from (a) published expert/manifesto/voter-survey data, each kept on its original scale with a stated rescaling to -10..+10, and (b) our own coding of each party\'s answers to the 36 compass items from its 2026 policy documents, recorded votes and leader statements (null = no evidence, never guessed). Scores in coded.axes use the same formula as the user test (data/guide/compass.json scoring). See guide/compass-method.md.',
        'method_page': 'guide/compass-method.md',
        'axes_scale': '-10..+10 on every axis; economic: left (-) to right (+); social: GAL/libertarian (-) to TAN/authoritarian (+); populism: pluralist (-) to populist (+). "general_left_right" values are voters\' or experts\' overall left-right placements and are NOT the economic axis.',
        'coding_scale': '-2 strongly disagree / very negative .. +2 strongly agree / very positive relative to the item text; confidence high | medium | low; null = no public evidence found.',
        'published_sources': [{k: v for k, v in s.items() if k != 'parties'} for s in published['sources']],
        'not_retrieved': published['not_retrieved'],
        'parties': parties,
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, 'compass.json'), 'w', encoding='utf-8') as f:
        json.dump(compass, f, indent=1, ensure_ascii=False)
    with open(os.path.join(OUT_DIR, 'compass-parties.json'), 'w', encoding='utf-8') as f:
        json.dump(out_parties, f, indent=1, ensure_ascii=False)
    render_method(compass, parties)
    # report
    print('items:', len(ITEMS), compass['balance'])
    print(f"{'party':22} {'coded':>5} {'econ':>7} {'n':>3} {'social':>7} {'n':>3} {'popul':>7} {'n':>3}  gps(e,s,p)")
    for slug, p in parties.items():
        if not p.get('coded'):
            continue
        ax = p['coded']['axes']
        g = p['published'].get('gps2019')
        gs = f"{g[0]['rescaled']['economic']},{g[0]['rescaled']['social']},{g[0]['rescaled']['populism']}" if g else ''
        print(f"{slug:22} {p['coded']['n_coded']:>5} {str(ax['economic']['score']):>7} {ax['economic']['n_items']:>3} {str(ax['social']['score']):>7} {ax['social']['n_items']:>3} {str(ax['populism']['score']):>7} {ax['populism']['n_items']:>3}  {gs}")

if __name__ == '__main__':
    main()
