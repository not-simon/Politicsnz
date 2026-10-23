#!/usr/bin/env python3
"""Build parties/national/policies/policies.json and README.md.
Inputs: raw/policy.nz/parties/national-party.json, raw/party-docs/national/doc_index.json (from
tools/policies_national_build_docs.py) and the documents/ folder.
Run: python3 -I tools/policies_national_build.py
"""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from policies_national_fetch import orig

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POL = os.path.join(ROOT, 'parties', 'national', 'policies')
DOCS = os.path.join(POL, 'documents')
RETRIEVED = '2026-10-23'
idx = json.load(open(os.path.join(ROOT, 'raw/party-docs/national/doc_index.json')))
pnz = json.load(open(os.path.join(ROOT, 'raw/policy.nz/parties/national-party.json')))

GROUPS = [
    ('economy', 'Economy'), ('incomes-and-employment', 'Incomes & employment'), ('health', 'Health'),
    ('education', 'Education'), ('housing', 'Housing'), ('transport-and-infrastructure', 'Transport & infrastructure'),
    ('environment', 'Environment'), ('law-justice-and-government', 'Law, justice & government'),
    ('community-and-inclusion', 'Community & inclusion'), ('te-ao-maori', 'Te ao Māori'), ('migration', 'Migration'),
    ('defence-and-foreign-affairs', 'Defence & foreign affairs'), ('media-culture-and-recreation', 'Media, culture & recreation'),
]
GROUP_KEYS = [g for g, _ in GROUPS]


def title_of(doc):
    p = os.path.join(POL, doc)
    m = re.search(r'^title: (".*")$', open(p).read(), re.M)
    return json.loads(m.group(1)) if m else doc


def src_url_of(doc):
    m = re.search(r'^source_url: (".*")$', open(os.path.join(POL, doc)).read(), re.M)
    return json.loads(m.group(1)) if m else ''


# Additional documents relevant to the same policy as a cited document (National's own policy-hub page,
# the policy PDF, or the announcement release). Keys/values are document slugs.
RELATED = {
    'news-261007-cameronbrewer': ['policy-47-point-plan-small-businesses'],
    'pdf-nationals-47-point-plan-to-support-small-businesses': ['policy-47-point-plan-small-businesses'],
    'news-261008-louiseupston': ['policy-walfare'],
    'news-261010-toddmcclay': ['policy-fisheries'],
    'news-260923-markmitchell': ['policy-fix-fire-and-emergency', 'pdf-backing-our-firefighters'],
    'news-260913-markmitchell': ['policy-police-auckland-transport', 'pdf-auckland-transport-police-teams'],
    'news-261001-national-to-trial-seamless-trans-tasman': ['policy-trans-tasman-travel', 'pdf-making-trans-tasman-travel-seamless'],
    'pdf-growing-more-to-feed-the-world': ['policy-double-exports'],
    'news-261009-toddmcclay-1': ['policy-securing-water-and-fertiliser', 'pdf-water-security-policy'],
    'news-260916-nicolawillis': ['policy-grocery-competition'],
    'policy-international-visitor-levy': ['pdf-international-visitor-levy-reset'],
    'pdf-nationals-economic-plan': ['policy-nationals-eco-plan'],
    'pdf-nationals-plan-for-hunting-and-fishing': ['policy-hunting-and-fishing', 'pdf-delivering-hunting-and-fishing', 'pdf-plan-for-hunting-and-fishing'],
    'pdf-nationals-south-island-plan': ['policy-hunters-and-anglers'],
    'pdf-electrify-nz-2-0': ['policy-electrify-nz-2'],
    'news-20261018-paulgoldsmith': ['policy-remove-rights-to-silence'],
    'news-260823-no-new-taxes-under-national': ['policy-no-new-taxes'],
    'news-261011-ericastanford': ['policy-education-teaching-the-basics-brilliantly', 'pdf-nationals-education-manifesto', 'policy-kiwi-kids'],
    'news-260920-screen-use-to-end-in-ece-and-limits-set': ['policy-education-teaching-the-basics-brilliantly', 'pdf-ece-set-up-for-success', 'pdf-nationals-education-manifesto', 'policy-kiwi-kids'],
    'policy-kiwisaver': ['pdf-national-kiwisaver-policy-document', 'news-260621-national-to-further-boost-kiwis-financia'],
    'policy-paid-parental-leave': ['pdf-paid-parental-leave'],
    'policy-responsibility-rules': ['pdf-nationals-budget-responsibility-rules'],
    'news-261013-nicolawillis': ['policy-welcome-kiwis-home'],
    'policy-solar': ['pdf-national-electrify-nz-home-energy-fund-policy-document', 'news-20260625-brownbishopwatts'],
    'news-20260817-honsimeonbrown': ['news-261015-simeonbrown-1'],
    'rnz-national-promises-to-fund-800-million-christchurch-northern-motorway-extension': ['news-261005-chrisbishop', 'policy-pegasus-woodend-bypass', 'pdf-building-the-future-belfast-to-pegasus-and-woodend-bypass'],
    'news-20260705-hontoddmcclay': ['pdf-building-the-future-new-zealands-next-billion-customers'],
    'pdf-more-medicines-and-earlier-care': ['news-261006-simeonbrown'],
    'news-260824-christopherluxon': ['pdf-online-safety-bill-fact-sheet'],
    'news-260918-tamapotaka': ['pdf-18-september-2026-retirement-village-exit-repayment-changes-media-fact-sheet'],
    'news-260608-national-backs-farmers-and-conservation': ['news-260608-national-backs-farmers-qeii-national-t'],
    'policy-build-the-future': ['news-20260715-honchrispenk'],
    'policy-consent-laws': ['news-20260719-honpaulgoldsmith'],
    'pdf-nationals-fiscal-plan': ['policy-nationals-fiscal-plan', 'news-261012-nicolawillis'],
    'news-261014-simonwatts': ['policy-backing-auckland'],
}
# Per-policy extra related docs (policy.nz id -> doc slugs)
RELATED_BY_ID = {
    'POL55177': ['pdf-national-backs-the-waikato', 'policy-backing-waikato'],
    'POL54734': ['pdf-national-kiwisaver-policy-document', 'news-260621-national-to-further-boost-kiwis-financia', 'policy-young-adults'],
    'POL55211': ['policy-retirement'],
    'POL54815': ['policy-kiwi-kids'],
}

D = lambda s: f'documents/{s}.md'

# ----------------------------------------------------------------------------------------------
# Policies found on National's own policy hub / documents that policy.nz does not list separately.
# Each was checked against every policy.nz Why/How text (not just the statement) to avoid duplicates.
# Summaries are this archive's own neutral paraphrase; full verbatim text is in the linked documents.
EXTRAS = [
    # --- Transport & infrastructure
    dict(statement='Fund construction of Mill Road Stage One (Manukau to Alfriston) in South Auckland',
         topics=['transport-and-infrastructure', 'cars-and-roads', 'infrastructure-funding-and-planning'],
         why='National says South Auckland roads have not kept up with growth around Drury, Papakura and Manukau, and that Stage One is ranked highly in the Government’s Major Transport Project Pipeline.',
         how='National would commit $1.75 billion of Crown capital in Budget 2028, held in tagged contingency, to build the four-lane Stage One corridor; any extra costs would come from the National Land Transport Fund.',
         costing='$1.75 billion Crown capital (Budget 2028), per National’s Mill Road document and Fiscal Plan.',
         docs=['policy-mill-road', 'pdf-building-the-future-mill-road', 'news-261004-chrisbishop', 'pdf-nationals-fiscal-plan']),
    dict(statement='Fund route protection for Mill Road Stages Two and Three (Alfriston to Drury)',
         topics=['transport-and-infrastructure', 'cars-and-roads', 'infrastructure-funding-and-planning'],
         why='National says landowners along the route face uncertainty and that route protection gives landowners, developers and Auckland Council certainty to plan.',
         how='National would allocate $100 million to NZTA to progress route protection and work with Auckland Council on timing of the later stages in Auckland’s 30-year transport plan.',
         costing='$100 million Crown capital (Budget 2027 in the Fiscal Plan capital table).',
         docs=['policy-mill-road', 'pdf-building-the-future-mill-road', 'pdf-nationals-fiscal-plan']),
    dict(statement='Progress Hamilton Southern Links and explore staged delivery',
         topics=['transport-and-infrastructure', 'cars-and-roads', 'regional-development'],
         why='National describes Southern Links as a major future connection linking the Waikato Expressway with western Hamilton, new housing, businesses and Hamilton Airport.',
         how='National says it would continue to progress the project and explore options for staged delivery so some benefits arrive sooner. No new funding figure is stated.',
         docs=['policy-backing-waikato', 'pdf-national-backs-the-waikato', 'news-20261019-chrisbishop']),
    dict(statement='Deliver the Auckland Deal, including a coordinated 30-year Auckland transport strategy',
         topics=['transport-and-infrastructure', 'infrastructure-funding-and-planning', 'local-government'],
         why='National says Auckland needs to plan ahead rather than constantly play catch-up.',
         how='National would deliver the Auckland Regional Deal, including a joint 30-year transport strategy/plan developed with Auckland Council through the new Auckland Regional Transport Committee.',
         docs=['policy-backing-auckland', 'pdf-building-the-future-backing-auckland-to-succeed', 'pdf-building-the-future-mill-road']),
    dict(statement='Complete and implement the replacement of the Resource Management Act',
         topics=['environment', 'urban-planning-and-resource-management', 'economy'],
         why='National says the new planning system will roughly halve the number of consents needed and give more certainty, including for farmers and renewable energy projects.',
         how='National would finish implementing the RMA replacement with consistent national rules, fewer unnecessary consents, more enabling rules for renewables, and transition support.',
         docs=['pdf-nationals-47-point-plan-to-support-small-businesses', 'pdf-nationals-economic-plan', 'pdf-electrify-nz-2-0', 'pdf-nationals-south-island-plan']),
    dict(statement='Deliver 19 national standards for everyday farm activities under the new planning system',
         topics=['environment', 'agriculture', 'urban-planning-and-resource-management'],
         why='National says rules for everyday farm jobs differ from council to council and that consents are costly (citing a Federated Farmers survey average of nearly $45,000 per new consent).',
         how='National would set 19 national standards (for example farm plans) for routine farm work, developed with farmers, growers and the sector, so many everyday activities would not need resource consent.',
         docs=['pdf-growing-more-to-feed-the-world', 'policy-double-exports']),
    dict(statement='Legislate requirements for asset management plans and long-term capital plans',
         topics=['transport-and-infrastructure', 'infrastructure-funding-and-planning'],
         why='Listed in National’s Economic Plan under building infrastructure for the future.',
         how='National would legislate requirements for asset management plans and long-term capital plans (the plan gives no further detail).',
         docs=['pdf-nationals-economic-plan', 'policy-nationals-eco-plan']),
    # --- Health
    dict(statement='Deliver the Waikato Medical School, with 120 extra medical training places a year from 2028',
         topics=['health', 'health-funding-and-workforce', 'regional-development'],
         why='National says it will build a stronger pipeline of doctors for rural and regional New Zealand.',
         how='National would complete the New Zealand Graduate School of Medicine at the University of Waikato (backed by $82.85 million of government funding plus university/philanthropic funding) with students training across regional and rural Waikato.',
         docs=['policy-backing-waikato', 'pdf-national-backs-the-waikato', 'pdf-growing-more-to-feed-the-world']),
    # --- Housing / seniors
    dict(statement='Ring-fence at least 20 per cent of Housing Flexible Fund places for seniors’ housing',
         topics=['housing', 'housing-affordability', 'seniors'],
         why='Part of National’s plan for retirement, aimed at boosting housing for older New Zealanders.',
         how='At least 20 per cent of all future Housing Flexible Fund places would be reserved for seniors’ housing, such as affordable rentals (e.g. Abbeyfield), social homes or other models.',
         docs=['policy-retirement', 'pdf-nationals-plan-for-retirement', 'news-20261022-retirement']),
    dict(statement='Expand granny flat rules so more can be built faster and cheaper',
         topics=['housing', 'housing-affordability', 'seniors'],
         why='National says granny flats support inter-generational living and that its earlier consent exemption for units up to 70m² can go further.',
         how='National would allow an attached garage of up to 40m² in addition to a 70m² granny flat, require PIMs for standalone dwellings within five working days with cost-recovery fees, remove the need for a primary dwelling, explore a new builder licensing class, and let tiny homes on wheels use the rules.',
         docs=['policy-retirement', 'pdf-nationals-plan-for-retirement']),
    # --- Community
    dict(statement='Review Enduring Powers of Attorney law to protect seniors from elder abuse and financial exploitation',
         topics=['community-and-inclusion', 'seniors', 'law-justice-and-government'],
         why='National says protections against elder abuse and financial exploitation should be strengthened.',
         how='National would review the Enduring Powers of Attorney framework and consider further measures, including law changes, to better protect seniors from economic harm.',
         docs=['policy-retirement', 'pdf-nationals-plan-for-retirement']),
    dict(statement='Establish a free 0800-SENIORS helpline for government services',
         topics=['community-and-inclusion', 'seniors', 'benefits'],
         why='National says seniors need one place to get help navigating government services and the support they are entitled to.',
         how='A single free helpline covering any issue, sitting within the Ministry of Social Development and funded within existing baselines.',
         costing='Within existing MSD baselines (per National).',
         docs=['policy-retirement', 'pdf-nationals-plan-for-retirement']),
    # --- Education
    dict(statement='Expand the Year 7–10 Maths Acceleration Programme by 40,000 students',
         topics=['education', 'schools'],
         why='Part of National’s plan to keep “teaching the basics brilliantly”.',
         how='The programme would be expanded by an additional 40,000 students to reach 128,000 students across three years.',
         docs=['policy-kiwi-kids', 'pdf-nationals-plan-for-kiwi-kids', 'news-20261021-christopherluxon']),
    dict(statement='Provide Learning Support Coordinators in all schools with Year 1–8 students and more teacher-aide hours',
         topics=['education', 'schools', 'disability'],
         why='National describes this as the largest boost to learning support in a generation.',
         how='Learning Support Coordinators for all schools with Year 1–8 students from 2028, and additional teacher-aide hours building to two million extra hours a year from 2028 (much of this was funded by the current Government and is listed by National as a 2026 policy for Kiwi kids).',
         docs=['policy-kiwi-kids', 'pdf-nationals-plan-for-kiwi-kids', 'pdf-nationals-education-manifesto']),
    dict(statement='Make classrooms warmer and quieter with acoustic panels, ceiling insulation and carpet',
         topics=['education', 'schools'],
         why='National says it wants “more warm, dry classrooms”.',
         how='Installing acoustic panels, ceiling insulation bales and carpet with built-in underlay across schools nationwide to improve warmth and reduce noise.',
         docs=['policy-kiwi-kids', 'pdf-nationals-plan-for-kiwi-kids']),
    dict(statement='Keep the cellphone ban in schools',
         topics=['education', 'schools'],
         why='Listed by National as one of its 2026 election policies for Kiwi kids (the ban was introduced this term).',
         how='Retain the existing ban on cellphones during the school day.',
         docs=['policy-kiwi-kids', 'pdf-nationals-plan-for-kiwi-kids']),
    dict(statement='Keep the requirement for one hour a day each of reading, writing and maths',
         topics=['education', 'schools'],
         why='National says the current focus on the basics is starting to lift achievement and should continue.',
         how='Retain the requirement for an hour a day of reading, writing and maths in primary and intermediate schools, alongside structured literacy and maths.',
         docs=['policy-kiwi-kids', 'pdf-nationals-plan-for-kiwi-kids', 'pdf-nationals-education-manifesto']),
    dict(statement='Extend the school lunch programme to 2029',
         topics=['education', 'schools', 'public-health'],
         why='Included as a spending commitment in National’s Fiscal Plan.',
         how='Funding for another two years of the school lunch programme. The Fiscal Plan does not describe changes to how the programme works.',
         costing='$451.8 million operating over 2027/28–2029/30 (Fiscal Plan table).',
         docs=['pdf-nationals-fiscal-plan', 'policy-nationals-fiscal-plan']),
    dict(statement='Expand Youth Guarantee by 1,000 places a year',
         topics=['education', 'trades-and-vocational-education', 'young-people'],
         why='National says this gives more young people early, practical pathways into work, including food and fibre.',
         how='Youth Guarantee places would grow by 1,000 a year, alongside doubling Trades Academy places to 20,000 by 2030.',
         docs=['pdf-growing-more-to-feed-the-world', 'policy-double-exports']),
    # --- Economy / business
    dict(statement='Keep Investment Boost',
         topics=['economy', 'business-support', 'government-revenue-and-finance'],
         why='National says Investment Boost rewards businesses that invest and contrasts this with Labour, which it says would not keep it.',
         how='Retain the immediate 20 per cent deduction for eligible new productive assets of any value, for businesses of every size.',
         docs=['pdf-nationals-47-point-plan-to-support-small-businesses', 'pdf-nationals-economic-plan']),
    dict(statement='Reduce tax compliance, including dropping detailed FBT logbooks for work vehicles',
         topics=['economy', 'business-support', 'government-revenue-and-finance'],
         why='Listed under National’s plan to grow the economy and reduce costs for business.',
         how='Employers would no longer need detailed fringe benefit tax log books for work vehicles, and innovative firms would get R&D tax credits during the year rather than after it.',
         docs=['pdf-nationals-economic-plan', 'policy-nationals-eco-plan']),
    dict(statement='Support businesses through the transition to the new Employment Leave Act',
         topics=['incomes-and-employment', 'business-support', 'wages-and-working-conditions'],
         why='The Employment Leave Act replaces the Holidays Act from August 2028, requiring payroll changes.',
         how='National would provide early guidance, worked payroll examples and coordinated implementation support for employers and payroll providers (point 4 of the 47-point plan).',
         docs=['pdf-nationals-47-point-plan-to-support-small-businesses', 'policy-47-point-plan-small-businesses']),
    dict(statement='Progress motor-vehicle repair-information reform for independent workshops',
         topics=['economy', 'business-support', 'prices'],
         why='Part of National’s small-business plan to lower costs and improve competition.',
         how='Progress Dan Bidois’ reform to give independent workshops better access to manufacturers’ repair information (point 31 of the 47-point plan).',
         docs=['pdf-nationals-47-point-plan-to-support-small-businesses']),
    dict(statement='Deliver capital-market reforms and use Invest New Zealand to connect businesses with investment',
         topics=['economy', 'business-support', 'foreign-investment'],
         why='National says growing businesses need easier access to capital, skills and partners.',
         how='Deliver capital-market reforms making it easier for growing businesses to raise equity and debt, and use Invest New Zealand to connect productive businesses with international investment, skills and commercial partners (points 39–40 of the 47-point plan).',
         docs=['pdf-nationals-47-point-plan-to-support-small-businesses']),
    # --- Trade
    dict(statement='Remove a further $1 billion of non-tariff trade barriers by 2030',
         topics=['economy', 'trade-and-exports'],
         why='National says it removed $733 million of non-tariff barriers this term and wants to cut more red tape for exporters.',
         how='Target removal of another $1 billion of non-tariff barriers by 2030, prioritising barriers identified with exporters, with a focus on paperless trade and digital customs, including through the FIT Partnership.',
         docs=['pdf-nationals-47-point-plan-to-support-small-businesses', 'pdf-building-the-future-new-zealands-next-billion-customers', 'pdf-nationals-economic-plan']),
    dict(statement='Negotiate essential-supplies agreements with like-minded partners',
         topics=['defence-and-foreign-affairs', 'trade-and-exports', 'international-relations'],
         why='National says such agreements protect access to critical goods (food, medicines, critical inputs) during global disruption.',
         how='Use the NZ–Singapore Agreement on Trade in Essential Supplies (AOTES) as a template for agreements with other partners and extend the model across the FIT Partnership with shared early-warning systems.',
         docs=['pdf-building-the-future-new-zealands-next-billion-customers', 'pdf-nationals-47-point-plan-to-support-small-businesses']),
    dict(statement='Grow services exports to 35 per cent of exports by 2030 and modernise existing free trade agreements',
         topics=['economy', 'trade-and-exports'],
         why='National says services exports have grown from about 23% to 27% of total exports and that existing agreements can deliver more value.',
         how='Drive services exports towards 35% of total export value by 2030; modernise existing FTAs starting with China (a “negative list” approach to services); grow the Digital Economy Partnership Agreement; pursue a CPTPP–EU digital trade agreement; expand CPTPP and RCEP membership.',
         docs=['pdf-building-the-future-new-zealands-next-billion-customers', 'policy-new-trade']),
    dict(statement='Give NZTE a sharper “lead and follow” mandate and run at least 23 trade missions next term',
         topics=['economy', 'trade-and-exports', 'business-support'],
         why='National says NZTE should actively lead companies to new markets rather than only follow them.',
         how='NZTE would proactively identify exporters who could benefit from new FTAs and build sector opportunity maps; NZTE, Investment New Zealand and Education New Zealand would work under one coordinated strategy; at least 23 trade missions would be completed with a sector focus.',
         docs=['pdf-building-the-future-new-zealands-next-billion-customers']),
    # --- Agriculture / environment
    dict(statement='Invest $16 million from the International Visitor Levy to control wild deer, feral goats and other pests',
         topics=['environment', 'conservation', 'agriculture'],
         why='National says damaging wild animal populations harm productive land and conservation gains.',
         how='$16 million over four years from the IVL for coordinated control across public, Māori and private land, starting in the Central North Island and Southern Westland, and finalising a National Introduced Wild Animal Management Framework.',
         costing='$16 million over four years from the International Visitor Levy.',
         docs=['pdf-growing-more-to-feed-the-world']),
    dict(statement='Update agricultural vehicle weight rules so modern tractors and harvesters do not need routine overweight permits',
         topics=['transport-and-infrastructure', 'agriculture', 'cars-and-roads'],
         why='National says modern farm machinery routinely needs overweight permits.',
         how='Update the rules while protecting vulnerable roads and bridges; in the meantime NZTA would be directed to improve the permit system.',
         docs=['pdf-growing-more-to-feed-the-world']),
    dict(statement='Create regional wildfire readiness plans',
         topics=['environment', 'agriculture', 'climate-adaptation'],
         why='National says wildfire risk is rising and crews often arrive without the information they need.',
         how='Plans would be developed with forest owners, farmers, Fire and Emergency New Zealand and councils so firefighters can act fast with the right information.',
         docs=['pdf-growing-more-to-feed-the-world']),
    # --- Fiscal / government
    dict(statement='Reduce foreign aid spending outside the Pacific (by 10 per cent) to help fund medicines',
         topics=['defence-and-foreign-affairs', 'aid-development-and-institutions', 'government-revenue-and-finance'],
         why='National says this savings helps pay for its $604 million Pharmac uplift.',
         how='Reduce foreign aid and associated administration costs by 10 per cent while “fully protecting aid to the Pacific” (per the 6 October 2026 release). Policy.nz records the Pharmac funding under POL55205.',
         costing='Saving of $431.2 million over 2027/28–2030/31 (Fiscal Plan: “Reduce the foreign aid budget”).',
         docs=['news-261006-simeonbrown', 'pdf-more-medicines-and-earlier-care', 'pdf-nationals-fiscal-plan']),
    dict(statement='Establish an election policy costings unit',
         topics=['law-justice-and-government', 'government-revenue-and-finance'],
         why='Listed as a commitment in National’s Fiscal Plan.',
         how='Funding for an election policy costings unit in the year of the next general election. The Fiscal Plan gives no further design detail.',
         costing='$1.2 million (Fiscal Plan table).',
         docs=['pdf-nationals-fiscal-plan']),
]


def doc_ok(d):
    return os.path.exists(os.path.join(POL, d))


def topics_clean(ts):
    out = []
    for t in ts:
        if t not in out:
            out.append(t)
    return out


def costing_from(how):
    m = re.search(r'(This party estimates that this policy would[^.]*\.)', how or '')
    return m.group(1) if m else None


def build_entries():
    entries = []
    for p in pnz['policies']:
        attrs = {a['name'].lower(): re.sub(r'\s+', ' ', a['value']).strip() for a in p['attributes']}
        srcs, seen = [], set()
        for c in p['citations']:
            u = orig(c['url'])
            d = idx[u]['doc']
            if d in seen:
                continue
            seen.add(d)
            srcs.append({'title': c['title'], 'url': u, 'document': d, 'cited_by': 'policy.nz'})
        rel = []
        for s in list(srcs):
            slug = s['document'][len('documents/'):-3]
            rel += RELATED.get(slug, [])
        rel += RELATED_BY_ID.get(p['reference'], [])
        for r in rel:
            d = D(r)
            if d not in seen and doc_ok(d):
                seen.add(d)
                srcs.append({'title': title_of(d), 'url': src_url_of(d), 'document': d, 'cited_by': 'archive (related National document)'})
        tps = topics_clean(p['topics'])
        e = {'id': p['reference'], 'statement': p['statement'].strip().replace('  ', ' '), 'topics': tps,
             'primary_topic': next((t for t in tps if t in GROUP_KEYS), tps[0]),
             'key_policy': any(t.startswith('key-policies-') for t in tps),
             'summary': {'why': attrs.get('why', ''), 'how': attrs.get('how', '')}, 'summary_source': 'policy.nz',
             'costing': costing_from(attrs.get('how')),
             'sources': srcs}
        entries.append(e)
    for i, x in enumerate(EXTRAS, 1):
        srcs = []
        for s in x['docs']:
            d = D(s)
            assert doc_ok(d), d
            srcs.append({'title': title_of(d), 'url': src_url_of(d), 'document': d, 'cited_by': 'archive'})
        tps = topics_clean(x['topics'])
        entries.append({'id': f'NAT-ARC-{i:02d}', 'statement': x['statement'], 'topics': tps,
                        'primary_topic': next((t for t in tps if t in GROUP_KEYS), tps[0]), 'key_policy': False,
                        'summary': {'why': x['why'], 'how': x['how']}, 'summary_source': 'archive',
                        'costing': x.get('costing'), 'sources': srcs})
    return entries


def fiscal_table():
    t = open(os.path.join(DOCS, 'pdf-nationals-fiscal-plan.md')).read()
    lay = t.split('## Full text (page-layout rendering)')[1]
    a = lay.index('OPERATING'); b = lay.index('Sources:')
    block = lay[a:b].rstrip()
    block = '\n'.join(l.rstrip() for l in block.splitlines() if l.strip())
    return block


def anchor(s):
    s = s.lower()
    s = re.sub(r'[^\w\- ]', '', s)
    return s.replace(' ', '-')


def render_policy(e):
    L = [f"#### {e['statement']}", '',
         f"`{e['id']}` · topics: {', '.join(e['topics'])} · summary: {'policy.nz' if e['summary_source']=='policy.nz' else 'this archive'}", '']
    if e['summary']['why']:
        L.append(f"- **Why:** {e['summary']['why']}")
    if e['summary']['how']:
        L.append(f"- **How:** {e['summary']['how']}")
    if e.get('costing'):
        L.append(f"- **Costing:** {e['costing']}")
    kind = lambda d: ('PDF' if '/pdf-' in d else 'policy page' if '/policy-' in d or '/web-' in d else 'press release' if '/news-' in d else 'external')
    docs = ' · '.join(f"[{title_of(s['document'])}]({s['document']}) ({kind(s['document'])})" for s in e['sources'])
    L.append(f"- **Full text:** {docs}")
    L.append('')
    return L


def main():
    entries = build_entries()
    json.dump(entries, open(os.path.join(POL, 'policies.json'), 'w'), indent=1, ensure_ascii=False)

    docs = sorted(f for f in os.listdir(DOCS) if f.endswith('.md'))
    used = {s['document'] for e in entries for s in e['sources']}
    n_pnz = sum(1 for e in entries if e['summary_source'] == 'policy.nz')
    n_arc = len(entries) - n_pnz
    by = collections.OrderedDict((g, []) for g in GROUP_KEYS)
    for e in entries:
        by.setdefault(e['primary_topic'], []).append(e)
    also = collections.defaultdict(list)
    for e in entries:
        for t in e['topics']:
            if t in GROUP_KEYS and t != e['primary_topic']:
                also[t].append(e)
    gname = dict(GROUPS)

    L = ['# National Party — 2026 election policies', '',
         f"Every 2026 general-election policy of the New Zealand National Party (Te Rōpū Nāhinara) that this archive could find, "
         f"with a short summary of each and links to the **full verbatim text** of National's own policy documents, web pages and press releases.", '',
         f"- **{len(entries)} policies**: {n_pnz} from [policy.nz](https://policy.nz) (the Why/How summaries are policy.nz's neutral summaries) "
         f"plus {n_arc} further commitments found in National's own documents that policy.nz does not list separately (summaries written by this archive, marked `NAT-ARC-xx`).",
         f"- **{len(docs)} source documents** in [`documents/`](documents/): {sum(1 for d in docs if d.startswith('pdf-'))} PDF policy documents, "
         f"{sum(1 for d in docs if d.startswith('policy-') or d.startswith('web-'))} policy pages from national.org.nz, "
         f"{sum(1 for d in docs if d.startswith('news-'))} National Party press releases/speeches, and "
         f"{sum(1 for d in docs if d.startswith(('beehive-', 'rnz-')))} third-party pages cited by policy.nz (Beehive, RNZ).",
         f"- Retrieved **{RETRIEVED}** directly from national.org.nz / assets.national.org.nz (policy hub: <https://www.national.org.nz/policies>), "
         "beehive.govt.nz and rnz.co.nz. Original PDFs and HTML are kept in `raw/party-docs/national/`. Scripts: `tools/policies_national_*.py`.",
         "- Policy statements, Why/How summaries and topics for `POL…` entries come from policy.nz (`raw/policy.nz/parties/national-party.json`). "
         "Costings are shown only where National or policy.nz states one.",
         "- National is the senior party in the current (2023–2026) coalition Government, so some documents mix new election promises with "
         "descriptions of what the Government has already done. Entries here are the forward-looking commitments.", '',
         '## Contents', '', '- [Key commitments / headline policies](#key-commitments--headline-policies)',
         '- [Costings & fiscal plan](#costings--fiscal-plan)', '- Policies by topic:']
    for g in by:
        if by[g]:
            L.append(f"  - [{gname.get(g, g)}](#{anchor(gname.get(g, g))}) ({len(by[g])})")
    L += ['- [All source documents](#all-source-documents)', '']

    # Key commitments
    L += ['## Key commitments / headline policies', '',
          "National's campaign slogan is “Fixing the Basics. Building the Future.” Its central promises, as set out on its policy hub, “Our Plan” page and campaign launch, are:", '']
    head = [
        ('No new taxes in the next term (including no capital gains tax), and keep Investment Boost', ['POL54733', 'NAT-ARC-20']),
        ('Return to surplus in 2028/29, keep net core Crown debt below 40% of GDP, spending towards 30% of GDP (Budget Responsibility Rules)', ['POL54725', 'POL54726', 'POL54727']),
        ('Make KiwiSaver compulsory from 1 July 2028 (combined contributions rising to 12% by 2032), $1,500 “Baby Boost” and auto-enrolment at birth, KiwiSaver top-up during paid parental leave, employer contributions for over-65s', ['POL54734']),
        ('Extend paid parental leave from 26 to 30 weeks by 2029', ['POL54715']),
        ('Widen 5% deposit First Home Loans (income cap raised to $300,000)', ['POL54918']),
        ('Cut the student loan repayment rate from 12% to 10% and get tougher on overseas defaulters', ['POL54813', 'POL54814']),
        ('A further $604m for Pharmac, bowel screening from age 50, breast screening to 74, free cervical screening 25–69', ['POL55205', 'POL55208', 'POL55209', 'POL55211']),
        ('Pursue structural separation of Foodstuffs into two competing nationwide grocery groups (subject to Commerce Commission assessment)', ['POL55014']),
        ('Cap council rate rises (2–4%)', ['POL54817']),
        ('Firmer welfare: work support for 30,000 jobseekers, lower rate after two years, drug testing, five-year residency rule', ['POL55226', 'POL55227', 'POL55228', 'POL55230']),
        ('Replace NCEA; keep students at school until end of Year 11; no screens in ECE; ban under-16s from social media', ['POL55174', 'POL55259', 'POL55050', 'POL54815']),
        ('Big transport builds: Belfast–Pegasus/Woodend Bypass ($800m), Mill Road Stage One ($1.75b), next Roads of National Significance', ['POL55201', 'NAT-ARC-01', 'POL55177']),
        ('Energy: Home Energy Fund loans for solar/batteries, consent-free rooftop solar, Electrify NZ 2.0 market changes', ['POL54922', 'POL54923', 'POL55183']),
        ('Double exports by 2034 and pursue trade deals with “the next billion customers”', ['POL54712', 'POL54711']),
        ('Law and order: dedicated Auckland transport police, remove right to silence where a child is murdered, “yes means yes” consent law, end good-character discounts for sexual offending', ['POL54978', 'POL55322', 'POL54925', 'POL54926']),
    ]
    byid = {e['id']: e for e in entries}
    for text, ids in head:
        links = ', '.join(f"[{i}](#{anchor(byid[i]['statement'])})" for i in ids)
        L.append(f"- {text} — {links}")
    keyp = [e for e in entries if e['key_policy']]
    L += ['', f"policy.nz flags {len(keyp)} of the policies below as National's *key policies* in particular topics: " +
          '; '.join(f"[{e['statement']}](#{anchor(e['statement'])})" for e in keyp) + '.', '',
          "National's own policy hub groups its campaign documents as: " +
          ', '.join(f"[{title_of(D(s))}]({D(s)})" for s in ['policy-nationals-fiscal-plan', 'policy-nationals-eco-plan', 'policy-no-new-taxes',
                     'policy-kiwisaver', 'policy-welcome-kiwis-home', 'policy-kiwi-kids', 'policy-young-adults', 'policy-retirement',
                     'policy-education-teaching-the-basics-brilliantly', 'policy-more-medicines-and-earlier-care', 'policy-walfare',
                     'policy-47-point-plan-small-businesses', 'policy-double-exports', 'policy-electrify-nz-2', 'policy-backing-auckland',
                     'policy-backing-waikato', 'policy-hunters-and-anglers']) +
          f" — full list: [{title_of(D('policy-index'))}]({D('policy-index')}).", '']

    # Fiscal
    L += ['## Costings & fiscal plan', '',
          "National published a **Fiscal Plan** ([full text](documents/pdf-nationals-fiscal-plan.md); [web page](documents/policy-nationals-fiscal-plan.md)) "
          "and **Budget Responsibility Rules** ([full text](documents/pdf-nationals-budget-responsibility-rules.md)). In summary (all figures are National's own):", '',
          "- Operating allowances of $2.4 billion per Budget; capital allowances of $3.5 billion for Budgets 2027 and 2028 and $5 billion thereafter.",
          "- Election commitments total $16,450.7 million operating over 2026/27–2030/31, leaving $7,549.3 million of operating allowance unallocated; "
          "National says health makes up 88 per cent of its spending commitments.",
          "- Savings counted: reducing the foreign aid budget (−$431.2m) and stronger welfare expectations/case management (−$583.0m).",
          "- Capital commitments of $1,093.5 million (Budget 2027) and $1,750 million (Budget 2028, Mill Road Stage One).",
          "- A re-elected National Government would not impose new taxes, return to surplus in 2028/29 and keep debt below 40 per cent of GDP; "
          "National says it would consider tax relief only once the books are back in surplus.", '',
          "The Fiscal Plan's commitments table, reproduced verbatim from the PDF's text layer (layout preserved; $ million):", '',
          '```text', fiscal_table(), '```', '',
          "Policy-specific costings published by National are given under each policy below (e.g. Mill Road, water storage loans, IVL reset, KiwiSaver package).", '']

    for g, es in by.items():
        if not es:
            continue
        L += [f"## {gname.get(g, g)}", '']
        for e in es:
            L += render_policy(e)
        if also.get(g):
            L += [f"*Also relevant to {gname.get(g, g)} (listed under another topic):* " +
                  '; '.join(f"[{e['statement']}](#{anchor(e['statement'])})" for e in also[g]), '']

    L += ['## All source documents', '',
          'Each file contains front matter (title, source URL, retrieval date, format, fetch method) and the complete verbatim text.', '',
          '| Document | Source | Used by policies |', '|---|---|---|']
    cnt = collections.Counter(s['document'] for e in entries for s in e['sources'])
    for d in docs:
        dd = 'documents/' + d
        L.append(f"| [{title_of(dd).replace('|', '/')}]({dd}) | <{src_url_of(dd)}> | {cnt.get(dd, 0)} |")
    L += ['', "Documents with 0 policies are campaign speeches, overview pages or supporting fact sheets kept for completeness.", '',
          '---', f"Built by `tools/policies_national_build.py` on {RETRIEVED}. Source data: policy.nz and national.org.nz. "
          "If you spot an error, the verbatim documents are the authority."]
    open(os.path.join(POL, 'README.md'), 'w').write('\n'.join(L) + '\n')
    print(len(entries), 'policies', n_pnz, 'policy.nz', n_arc, 'archive;', len(docs), 'docs;', len(set(used)), 'docs used')


if __name__ == '__main__':
    main()
