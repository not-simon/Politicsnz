#!/usr/bin/env python3
"""Published (expert / manifesto / voter-survey) placements of New Zealand parties, assembled from the
raw downloads in raw/compass/ into the structure used by data/guide/compass-parties.json.

Original scales are kept exactly as published. A transparent rescaling to the app's -10..+10 axes is
proposed for each source in RESCALE (formula strings + a Python implementation); nothing is converted
silently - both the original value and the rescaled value are written out.
Run via compass_build.py.
"""
import csv, json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'raw', 'compass')

def load(name):
    with open(os.path.join(RAW, name), encoding='utf-8') as f:
        return json.load(f)

# ---------------------------------------------------------------- Global Party Survey 2019
GPS_PARTIES = {'ACTNZ': 'act', 'Greens': 'green', 'NZFirst': 'nz-first', 'Labour': 'labour', 'Nats': 'national'}

def gps():
    rows = load('gps2019_nz_extract.json')
    out = []
    for r in rows:
        slug = GPS_PARTIES[r['Partyabb']]
        out.append({
            'party': slug,
            'experts': int(r['Experts']),
            'V4_Scale_economic_left_right': r['V4_Scale'],
            'V6_Scale_social_liberal_conservative': r['V6_Scale'],
            'V8_Scale_populist_rhetoric': r['V8_Scale'],
            'V9_populist_saliency': r['V9'],
            'V10_immigration_liberal_restrictive': r['V10'],
            'V11_spending_vs_tax_cuts': r['V11'],
            'V12_environment': r['V12'],
            'V13_nationalism_vs_multilateralism': r['V13'],
            'V16_liberal_democracy_respect_undermine': r['V16'],
            'WVS_LR_PartyVoter_mean_self_placement_1_10': r['WVS_LR_PartyVoter'],
            'rescaled': {
                'economic': rescale_0_10(r['V4_Scale']),
                'social': rescale_0_10(r['V6_Scale']),
                'populism': rescale_0_10(r['V8_Scale']),
            },
        })
    return {
        'id': 'gps2019',
        'name': 'Global Party Survey 2019 (expert survey)',
        'citation': 'Norris, Pippa (2020). Global Party Survey, 2019, V2.1 (party-level file, April 2020). Harvard Dataverse, doi:10.7910/DVN/WMGTNS.',
        'url': 'https://doi.org/10.7910/DVN/WMGTNS',
        'licence': 'CC0 1.0 (Dataverse licence field)',
        'year': 2019,
        'reference_election': 2017,
        'coverage_note': 'Five NZ parties were rated (12 experts each). The Māori Party and TOP were not included.',
        'scales': {
            'V4_Scale': '0 = extreme economic left ... 10 = extreme economic right (government role in economy: privatisation, taxes, regulation, spending, welfare)',
            'V6_Scale': '0 = very liberal ... 10 = very conservative social values (personal freedoms, abortion, same-sex marriage, democratic participation vs order, tradition, stability)',
            'V8_Scale': '0 = strongly favours pluralist rhetoric ... 10 = strongly favours populist rhetoric',
            'V9': '0 = no importance ... 10 = great importance of populist rhetoric',
            'V10': '0 = liberal immigration policies ... 10 = restrictive',
            'V11': '0 = favours increased public spending ... 10 = favours reduced taxation',
            'V12': '0 = favours environmental protection ... 10 = opposes',
            'V13': '0 = strongly favours nationalism ... 10 = strongly favours multilateralism',
            'V16': '0 = strongly respects liberal-democratic norms ... 10 = strongly undermines them',
            'WVS_LR_PartyVoter': 'mean 1-10 left-right self-placement of the party\'s own voters in the World Values Survey (GPS auxiliary variable)',
        },
        'rescale_formula': {'economic': 'V4_Scale -> (x - 5) * 2', 'social': 'V6_Scale -> (x - 5) * 2', 'populism': 'V8_Scale -> (x - 5) * 2'},
        'archived_copy': 'raw/compass/gps_by_party_v2_1.dta; extract raw/compass/gps2019_nz_extract.json; codebook raw/compass/gps_codebook.pdf',
        'parties': out,
    }

# ---------------------------------------------------------------- V-Party v2 (V-Dem)
VPARTY_SLUGS = {'New Zealand First Party': 'nz-first', 'Labour Party': 'labour', 'Green Party': 'green',
                'National Party': 'national', 'ACT New Zealand': 'act'}

def vparty():
    rows = load('vparty_v2_nz_extract.json')
    out = []
    for r in rows:
        if r['v2paenname'] not in VPARTY_SLUGS:
            continue
        yr = int(float(r['year']))
        if yr < 2002:
            continue
        def f(k):
            v = r.get(k)
            try:
                v = float(v)
                return None if math.isnan(v) else round(v, 3)
            except (TypeError, ValueError):
                return None
        out.append({
            'party': VPARTY_SLUGS[r['v2paenname']], 'election_year': yr,
            'v2pariglef_economic_left_right_interval': f('v2pariglef'),
            'v2pariglef_osp_0_6': f('v2pariglef_osp'),
            'v2pawelf_welfare_osp_0_4': f('v2pawelf_osp'),
            'v2paculsup_cultural_superiority_osp_0_4': f('v2paculsup_osp'),
            'v2paanteli_anti_elitism_osp_0_4': f('v2paanteli_osp'),
            'v2papeople_people_centrism_osp_0_4': f('v2papeople_osp'),
            'v2paplur_political_pluralism_osp_0_4': f('v2paplur_osp'),
            'v2paimmig_immigration_osp_0_4': f('v2paimmig_osp'),
            'v2palgbt_lgbt_equality_osp_0_4': f('v2palgbt_osp'),
            'v2parelig_religious_principles_osp_0_4': f('v2parelig_osp'),
            'v2xpa_popul_populism_index_0_1': f('v2xpa_popul'),
            'v2xpa_antiplural_antipluralism_index_0_1': f('v2xpa_antiplural'),
            'rescaled': {
                'economic': None if f('v2pariglef_osp') is None else round((f('v2pariglef_osp') - 3) * (10 / 3), 2),
                'populism': None if f('v2xpa_popul') is None else round((f('v2xpa_popul') - 0.5) * 20, 2),
            },
        })
    out.sort(key=lambda d: (d['party'], d['election_year']))
    return {
        'id': 'vparty_v2',
        'name': 'V-Party dataset v2 (Varieties of Democracy Institute, expert coding)',
        'citation': 'Lindberg, Staffan I., Nils Düpont, Masaaki Higashijima, Yaman Berker Kavasoglu, Kyle L. Marquardt, Michael Bernhard, Holger Döring, Allen Hicken, Melis Laebens, Juraj Medzihorsky, Anja Neundorf, Ora John Reuter, Saskia Ruth-Lovell, Keith R. Weghorst, Nina Wiesehomeier, Joseph Wright, Nazifa Alizada, Paul Bederke, Lisa Gastaldi, Sandra Grahn, Garry Hindle, Nina Ilchenko, Johannes von Römer, Steven Wilson, Daniel Pemstein, Brigitte Seim (2022). Varieties of Party Identity and Organization (V-Party) Dataset V2. Varieties of Democracy (V-Dem) Project.',
        'url': 'https://doi.org/10.23696/vpartydsv2',
        'licence': 'Free for research use with the suggested citation (V-Dem Institute terms; no Creative Commons licence is stated in the v2 codebook). Obtained from the V-Dem Institute\'s vdemdata R-package repository (github.com/vdeminstitute/vdemdata, data/vparty.RData).',
        'year': 2022,
        'coverage_note': 'NZ is coded for elections up to 2017 only; ACT is coded only to 2002, and the Māori Party, TOP, Mana and later minor parties are not coded. Values for 2014 and 2017 are shown (earlier years are in the raw extract).',
        'scales': {
            'v2pariglef': 'Economic left-right, measurement-model interval scale (lower = left). The _osp version is the ordinal original scale: 0 far-left ... 3 centre ... 6 far-right.',
            'v2pawelf_osp': 'Welfare: 0 strongly opposes ... 4 strongly supports welfare-state policies',
            'v2paculsup_osp': 'Cultural superiority: 0 strongly promotes superiority of a group/nation ... 4 strongly opposes',
            'v2paanteli_osp': 'Anti-elitism: 0 none ... 4 strongly anti-elite rhetoric',
            'v2papeople_osp': 'People-centrism: 0 none ... 4 strongly people-centric rhetoric',
            'v2paplur_osp': 'Political pluralism: 0 rejects ... 4 strongly embraces pluralism (respects opponents and institutions)',
            'v2paimmig_osp': 'Immigration: 0 strongly opposes ... 4 strongly supports',
            'v2palgbt_osp': 'LGBT social equality: 0 strongly opposes ... 4 strongly supports',
            'v2parelig_osp': 'Religious principles: 0 strongly promotes religious principles in politics ... 4 strongly opposes',
            'v2xpa_popul': 'Populism index 0-1 (combines anti-elitism and people-centrism)',
            'v2xpa_antiplural': 'Anti-pluralism index 0-1',
        },
        'rescale_formula': {'economic': 'v2pariglef_osp (0..6) -> (x - 3) * 10/3', 'populism': 'v2xpa_popul (0..1) -> (x - 0.5) * 20',
                            'social': 'not rescaled: V-Party has no single GAL-TAN scale; the LGBT, religion, immigration and cultural-superiority items are shown separately'},
        'archived_copy': 'raw/compass/vparty_v2_nz_extract.json (from vparty.RData); codebook raw/compass/vparty_codebook_v2.pdf',
        'parties': out,
    }

# ---------------------------------------------------------------- CSES Module 5 (expert + respondent)
CSES_LETTERS = {
    'NZL_2017': {'A': 'national', 'B': 'labour', 'C': 'nz-first', 'D': 'green', 'E': 'opportunity', 'F': 'te-pati-maori', 'G': 'act', 'H': 'mana'},
    'NZL_2020': {'A': 'labour', 'B': 'national', 'C': 'green', 'D': 'act', 'E': 'nz-first', 'F': 'opportunity', 'G': 'new-conservative', 'H': 'te-pati-maori'},
}

def cses():
    d = load('cses5_nz_party_placements.json')
    out = []
    for el, letters in CSES_LETTERS.items():
        yr = int(el[-4:])
        for letter, slug in letters.items():
            ex = d[el]['expert_E5018'].get(letter)
            resp = d[el]['respondent_E3019_unweighted'].get(letter)
            if ex is None or ex > 10:
                continue
            out.append({
                'party': slug, 'election_year': yr,
                'E5018_expert_left_right_0_10': ex,
                'E3019_respondent_mean_left_right_0_10_unweighted': resp['mean'] if resp else None,
                'E3019_n_respondents_placing': resp['n'] if resp else None,
                'rescaled': {'general_left_right_expert': rescale_0_10(ex),
                             'general_left_right_voters': rescale_0_10(resp['mean']) if resp else None},
            })
    return {
        'id': 'cses5',
        'name': 'CSES Module 5: collaborator (expert) left-right placements and respondent placements, New Zealand 2017 and 2020',
        'citation': 'The Comparative Study of Electoral Systems (www.cses.org). CSES MODULE 5 FULL RELEASE [dataset and documentation]. July 7, 2023 version. doi:10.7804/cses.module5.2023-07-07. New Zealand studies: NZES 2017 and NZES 2020 (collaborators Jack Vowles et al.).',
        'url': 'https://cses.org/data-download/cses-module-5-2016-2021/',
        'licence': 'Free for research use with citation (CSES data-download terms). Expert placement E5018 is the single judgment of the national collaborator team, not a multi-expert survey.',
        'year': 2023,
        'scales': {'E5018': '00 = Left ... 10 = Right, in the expert judgment of the CSES collaborator', 'E3019': 'respondents\' placement of each party, 0 = Left ... 10 = Right (means here are unweighted)'},
        'rescale_formula': {'general_left_right': '(x - 5) * 2; this is a GENERAL left-right scale, not the economic axis, and is plotted on the economic axis only as a labelled approximation'},
        'archived_copy': 'raw/compass/cses5_nz_party_placements.json (computed from raw/compass/cses5_csv/cses5.csv); codebook raw/compass/cses5_codebook_part3_parties_and_leaders.txt',
        'parties': out,
    }

# ---------------------------------------------------------------- NZES 2020 / 2023 voter placements
def nzes():
    d = load('nzes_party_placements.json')
    out = []
    for key, yr, item in (('nzes2023', 2023, 'B5'), ('nzes2020', 2020, 'B7')):
        for slug, v in d[key].items():
            out.append({
                'party': slug, 'election_year': yr, 'item': item,
                'mean_left_right_0_10_weighted': v['mean'], 'sd': v['sd'],
                'weighted_n_placing': v['weighted_n_placing'], 'dont_know_pct': v['dont_know_pct'],
                'distribution_weighted_freq': v['distribution'],
                'rescaled': {'general_left_right_voters': rescale_0_10(v['mean'])},
            })
    return {
        'id': 'nzes_voters',
        'name': 'New Zealand Election Study 2020 and 2023: voters\' mean placement of parties on a 0-10 left-right scale',
        'citation': 'Vowles, J. et al. New Zealand Election Study 2020 and 2023, weighted frequency tables (Sections B/C), hosted at jackvowles.com; question B5 (2023) / B7 (2020): "Where would you place these political parties on a scale from 0 to 10, where 0 means the most left and 10 means the most right?"',
        'url': 'https://www.nzes.net/home-2/the-2023-election/',
        'licence': 'Public frequency tables; means and SDs computed here from the published weighted frequencies (excluding Don\'t know). Unit-record NZES data are subject to the NZES Data Usage Terms and were not used.',
        'year': 2024,
        'scales': {'mean_left_right_0_10': '0 = most left ... 5 = centre ... 10 = most right'},
        'rescale_formula': {'general_left_right': '(mean - 5) * 2; a GENERAL left-right scale as perceived by voters, shown alongside (not as) the economic axis'},
        'archived_copy': 'raw/compass/nzes_party_placements.json; source PDFs raw/compass/nzes2023_sectionsBCD_freq.pdf and raw/compass/nzes2020_sectionsBC_freq.pdf',
        'parties': out,
    }

# ---------------------------------------------------------------- ParlGov (party-level, time-invariant)
PARLGOV_SLUGS = {'ACT': 'act', 'Greens': 'green', 'LP': 'labour', 'NP': 'national', 'NZFP': 'nz-first', 'TOP': 'opportunity',
                 'NC': 'new-conservative', 'MP': 'te-pati-maori', 'A': 'alliance', 'CP': 'conservative', 'ALCP': 'legalise-cannabis'}

def parlgov():
    out = []
    with open(os.path.join(RAW, 'parlgov_party.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r['country_name_short'] != 'NZL' or r['party_name_short'] not in PARLGOV_SLUGS:
                continue
            def num(k):
                return float(r[k]) if r[k] not in ('', None) else None
            expert_based = any(r[k] not in ('', None) for k in ('castles_mair', 'huber_inglehart', 'ray', 'benoit_laver', 'chess'))
            out.append({
                'party': PARLGOV_SLUGS[r['party_name_short']], 'parlgov_party_id': int(r['party_id']), 'family': r['family_name'],
                'left_right_0_10': num('left_right'), 'state_market_0_10': num('state_market'), 'liberty_authority_0_10': num('liberty_authority'),
                'based_on_expert_surveys': expert_based,
                'expert_survey_ids': {k: r[k] for k in ('castles_mair', 'huber_inglehart', 'benoit_laver') if r[k]},
                'rescaled': {
                    'economic': rescale_0_10(num('state_market')) if num('state_market') is not None else None,
                    'social': rescale_0_10(num('liberty_authority')) if num('liberty_authority') is not None else None,
                    'general_left_right': rescale_0_10(num('left_right')) if num('left_right') is not None else None,
                },
            })
    return {
        'id': 'parlgov',
        'name': 'ParlGov party table (development version, 2026 snapshot)',
        'citation': 'Döring, Holger and Philip Manow. Parliaments and governments database (ParlGov): Information on parties, elections and cabinets in established democracies. view_party.csv (development version, retrieved 23 Oct 2026).',
        'url': 'https://www.parlgov.org/data/parlgov-development_csv-utf-8/view_party.csv',
        'licence': 'ParlGov releases are published on Harvard Dataverse under CC0 1.0 (2024 release, doi:10.7910/DVN/2VZ5ZC).',
        'year': 2026,
        'coverage_note': 'left_right / state_market / liberty_authority are ParlGov composites of the Castles-Mair (1984), Huber-Inglehart (1995) and Benoit-Laver (2006) expert surveys where a party was rated; parties with no expert rating (e.g. TOP, Conservative, New Conservative) carry the mean of their party family and are flagged based_on_expert_surveys=false. The most recent expert input is 2003-04 (Benoit-Laver), so these are historical.',
        'scales': {'left_right': '0 left ... 10 right', 'state_market': '0 state ... 10 market', 'liberty_authority': '0 libertarian ... 10 authoritarian'},
        'rescale_formula': {'economic': 'state_market -> (x - 5) * 2', 'social': 'liberty_authority -> (x - 5) * 2', 'general_left_right': 'left_right -> (x - 5) * 2'},
        'archived_copy': 'raw/compass/parlgov_party.csv',
        'parties': out,
    }

def not_retrieved():
    return [
        {
            'id': 'marpor',
            'name': 'Manifesto Project (MARPOR / CMP) RILE scores for NZ manifestos',
            'url': 'https://manifesto-project.wzb.eu/',
            'status': 'not retrieved',
            'reason': 'The Manifesto Project Main Dataset (MPDS2024a) and its API require a free registered account and API key; the download could not be completed from this research environment and no published table of NZ RILE scores for 2017-2023 was found. The dataset covers NZ parties (CMP ids 64110 Green, 64320 Labour, 64420 ACT, 64620 National, 64621 NZ First, 64901 Māori Party per the CSES Module 5 codebook). RILE = share of right-coded quasi-sentences minus share of left-coded ones (-100..+100).',
            'proposed_rescale': 'economic approximation: RILE / 10 (so -100..+100 -> -10..+10); note RILE mixes economic and social categories.',
        },
        {
            'id': 'vote_compass_nz',
            'name': 'Vote Compass New Zealand 2023 / 2026 (Vox Pop Labs for 1News/TVNZ) party positions',
            'url': 'https://www.1news.co.nz/vote-compass/',
            'status': 'not retrieved',
            'reason': 'Vote Compass places parties on a two-dimensional (economic x social) chart inside the application, from party answers to 30 propositions calibrated by the Vox Pop Labs team with NZ political scientists; the party coordinates are shown to users but are not published as numbers in 1News articles or in a dataset. 1News articles on 10 Oct 2023 and 22 Oct 2026 publish electorate-level scores only.',
        },
        {
            'id': 'ches',
            'name': 'Chapel Hill Expert Survey',
            'status': 'not applicable',
            'reason': 'CHES covers European parties only; New Zealand is not included in any CHES wave.',
        },
    ]

def rescale_0_10(x):
    return None if x is None else round((float(x) - 5) * 2, 2)

def build_published():
    return {
        'sources': [gps(), vparty(), cses(), nzes(), parlgov()],
        'not_retrieved': not_retrieved(),
    }

if __name__ == '__main__':
    print(json.dumps(build_published(), indent=1, ensure_ascii=False)[:4000])
