#!/usr/bin/env python3
"""Re-create the small JSON extracts in raw/compass/ from the downloaded source files.

  python3 -I tools/compass_extract.py

Sources (all downloaded 23 Oct 2026; see guide/compass-method.md for citations and licences):
  raw/compass/gps_by_party_v2_1.dta            Global Party Survey 2019 party-level file (Harvard Dataverse, CC0)
  /home/user/vdeminstitute/vdemdata/data/vparty.RData   V-Party v2 (clone of github.com/vdeminstitute/vdemdata); optional
  raw/compass/cses5_csv/cses5.csv               CSES Module 5 full release (285 MB, not committed; re-download from cses.org)
  raw/compass/nzes2023_sectionsBCD_freq.pdf     NZES 2023 weighted frequency tables (jackvowles.com), via pdftotext -layout
  raw/compass/nzes2020_sectionsBC_freq.pdf      NZES 2020 weighted frequency tables
Each step is skipped with a message if its input is missing, so the committed extracts are not clobbered.
"""
import json, math, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'raw', 'compass')

def gps():
    src = os.path.join(RAW, 'gps_by_party_v2_1.dta')
    if not os.path.exists(src):
        return print('skip GPS (no .dta)')
    import pandas as pd
    d = pd.read_stata(src, convert_categoricals=False)
    nz = d[d['ISO'] == 'NZL']
    cols = ['Partyname', 'Partyabb', 'Experts', 'Elec_year', 'PartyPerVote'] + [f'V{i}' for i in range(1, 4)] + \
           ['V4_Scale', 'V5', 'V6_Scale', 'V7', 'V8_Scale'] + [f'V{i}' for i in range(9, 22)] + \
           ['PG_left_right', 'PG_state_market', 'PG_liberty_authority', 'WVS_LR_PartyVoter', 'WVS_LibCon_PartyVoter',
            'WVS_Polmistrust_PartyVoter', 'WVS_LR_MedianVoter', 'ID_ParlGov', 'ID_CMP']
    out = nz[cols].round(3).to_dict(orient='records')
    json.dump(out, open(os.path.join(RAW, 'gps2019_nz_extract.json'), 'w'), indent=1, default=str)
    print('GPS rows', len(out))

def vparty():
    src = '/home/user/vdeminstitute/vdemdata/data/vparty.RData'
    if not os.path.exists(src):
        return print('skip V-Party (no vparty.RData)')
    import pyreadr
    r = pyreadr.read_r(src); d = r[list(r.keys())[0]]
    nz = d[d['country_name'] == 'New Zealand']
    cols = ['v2paenname', 'v2pashname', 'year', 'pf_party_id', 'v2pavote', 'v2paseatshare', 'v2pariglef', 'v2pariglef_osp',
            'v2pawelf', 'v2pawelf_osp', 'v2paculsup', 'v2paculsup_osp', 'v2paanteli', 'v2paanteli_osp', 'v2papeople', 'v2papeople_osp',
            'v2paplur', 'v2paplur_osp', 'v2paimmig', 'v2paimmig_osp', 'v2palgbt', 'v2palgbt_osp', 'v2parelig', 'v2parelig_osp',
            'v2pawomlab', 'v2pawomlab_osp', 'v2paminor', 'v2paminor_osp', 'v2paopresp', 'v2paopresp_osp', 'v2xpa_popul',
            'v2xpa_illiberal', 'v2xpa_antiplural', 'ep_v8_popul', 'ep_antielite_salience', 'ep_people_vs_elite', 'ep_galtan',
            'ep_lrecon', 'ep_v6_lib_cons', 'ep_v4_lr']
    cols = [c for c in cols if c in d.columns]
    out = nz[cols].to_dict(orient='records')
    json.dump(out, open(os.path.join(RAW, 'vparty_v2_nz_extract.json'), 'w'), indent=1, default=str)
    print('V-Party rows', len(out))

def cses():
    src = os.path.join(RAW, 'cses5_csv', 'cses5.csv')
    if not os.path.exists(src):
        return print('skip CSES (no cses5.csv; download https://cses.org/wp-content/uploads/2023/07/cses5_csv.zip)')
    import pandas as pd
    cols = ['E1004', 'E1006_NAM'] + [f'E5018_{c}' for c in 'ABCDEFGHI'] + [f'E3019_{c}' for c in 'ABCDEFGHI']
    parts = [ch[ch['E1006_NAM'].astype(str).str.contains('New Zealand', case=False, na=False)]
             for ch in pd.read_csv(src, usecols=cols, chunksize=200000)]
    nz = pd.concat(parts)
    out = {}
    for el, g in nz.groupby('E1004'):
        exp = {c: float(g[f'E5018_{c}'].iloc[0]) for c in 'ABCDEFGHI'}
        resp = {}
        for c in 'ABCDEFGHI':
            v = g[f'E3019_{c}']; v = v[(v >= 0) & (v <= 10)]
            if len(v):
                resp[c] = {'mean': round(float(v.mean()), 2), 'n': int(len(v))}
        out[str(el)] = {'expert_E5018': exp, 'respondent_E3019_unweighted': resp, 'n_respondents': int(len(g))}
    json.dump(out, open(os.path.join(RAW, 'cses5_nz_party_placements.json'), 'w'), indent=1)
    print('CSES elections', list(out))

def nzes_table(text, key):
    """Parse one Stata-style weighted frequency table (codes 0-10 + DK) that follows '-> tabulation of <key>'."""
    m = re.search(r'-> tabulation of %s\n' % re.escape(key), text)
    if not m:
        return None
    seg = text[m.end():]
    nxt = seg.find('-> tabulation of')
    seg = seg[:nxt] if nxt > 0 else seg
    vals = {}
    for line in seg.split('\n'):
        mm = re.match(r'^\s*(\d+)\.?(?:\s+\d+)?\s*(?:Left|Right|Centre)?\s*\|\s*([\d.,]+)\s+([\d.]+)', line)
        if mm and int(mm.group(1)) <= 10:
            vals[int(mm.group(1))] = float(mm.group(2).replace(',', ''))
    dk = re.search(r'(?:Don.t know|DK)\s*\|\s*([\d.,]+)\s+([\d.]+)', seg)
    if len(vals) != 11:
        raise ValueError(f'{key}: parsed {len(vals)} categories')
    n = sum(vals.values()); mean = sum(k * v for k, v in vals.items()) / n
    sd = math.sqrt(sum(v * (k - mean) ** 2 for k, v in vals.items()) / n)
    return {'mean': round(mean, 2), 'sd': round(sd, 2), 'weighted_n_placing': round(n, 1),
            'dont_know_pct': float(dk.group(2)) if dk else None, 'distribution': {str(k): round(v, 1) for k, v in vals.items()}}

def nzes():
    out = {}
    for pdf, key, tables in (
        ('nzes2023_sectionsBCD_freq.pdf', 'nzes2023', {'B5a': 'labour', 'B5b': 'national', 'B5c': 'green', 'B5d': 'act', 'B5e': 'nz-first', 'B5f': 'te-pati-maori', 'B5g': 'opportunity'}),
        ('nzes2020_sectionsBC_freq.pdf', 'nzes2020', {'B7_1': 'labour', 'B7_2': 'national', 'B7_3': 'green', 'B7_4': 'nz-first', 'B7_5': 'act', 'B7_6': 'te-pati-maori', 'B7_7': 'new-conservative', 'B7_8': 'opportunity'}),
    ):
        src = os.path.join(RAW, pdf)
        if not os.path.exists(src):
            print('skip', pdf); continue
        txt = subprocess.run(['pdftotext', '-layout', src, '-'], capture_output=True, text=True).stdout
        out[key] = {slug: nzes_table(txt, k) for k, slug in tables.items()}
    if out:
        json.dump(out, open(os.path.join(RAW, 'nzes_party_placements.json'), 'w'), indent=1)
        for k, v in out.items():
            print(k, {s: (t['mean'], t['dont_know_pct']) for s, t in v.items()})

if __name__ == '__main__':
    gps(); vparty(); cses(); nzes()
