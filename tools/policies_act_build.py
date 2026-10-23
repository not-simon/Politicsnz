#!/usr/bin/env python3
"""Build parties/act/policies/{policies.json,README.md,documents/*.md} (run with python3 -I).

Requires tools/policies_act_fetch.py to have been run first (raw/party-docs/act/fetched.json).
- 91 policy.nz statements (summary_source "policy.nz") + archive-only entries for policies found
  on act.org.nz that policy.nz does not list (summary_source "archive", written neutrally from the
  linked ACT page; see ARCHIVE below).
- One documents/<slug>.md per unique source (PDFs de-duplicated by extracted-text hash).
"""
import collections, hashlib, json, os, re, subprocess, sys, urllib.parse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW = os.path.join(ROOT, 'raw', 'party-docs', 'act')
OUT = os.path.join(ROOT, 'parties', 'act', 'policies')
DOCS = os.path.join(OUT, 'documents')
os.makedirs(DOCS, exist_ok=True)

store = json.load(open(os.path.join(RAW, 'fetched.json')))
pnz = json.load(open(os.path.join(ROOT, 'raw', 'policy.nz', 'parties', 'act-party.json')))
GROUPS = json.load(open(os.path.join(ROOT, 'raw', 'policy.nz', 'party-vote-election.json')))['topicsList']
GROUP_NAMES = {
    'community-and-inclusion': 'Community & inclusion', 'defence-and-foreign-affairs': 'Defence & foreign affairs',
    'economy': 'Economy', 'education': 'Education', 'environment': 'Environment', 'health': 'Health',
    'housing': 'Housing', 'incomes-and-employment': 'Incomes & employment',
    'law-justice-and-government': 'Law, justice & government', 'media-culture-and-recreation': 'Media, culture & recreation',
    'migration': 'Migration', 'te-ao-maori': 'Te ao Māori', 'transport-and-infrastructure': 'Transport & infrastructure'}
# sub-topic -> policy.nz topic group (most frequent co-occurring group across all parties' policy.nz data)
SUB2GROUP = {
    'agriculture': 'economy', 'aid-development-and-institutions': 'defence-and-foreign-affairs',
    'animal-welfare': 'community-and-inclusion', 'benefits': 'incomes-and-employment', 'business-support': 'economy',
    'cars-and-roads': 'transport-and-infrastructure', 'civil-justice': 'law-justice-and-government',
    'climate-adaptation': 'environment', 'conservation': 'environment', 'criminal-justice': 'law-justice-and-government',
    'economic-development-and-industry': 'economy', 'emissions-reduction': 'environment',
    'energy': 'transport-and-infrastructure', 'family-justice-and-safety': 'law-justice-and-government',
    'firearms': 'media-culture-and-recreation', 'fisheries': 'economy', 'free-expression-and-hate-speech': 'community-and-inclusion',
    'fresh-water-and-pollution': 'environment', 'government-revenue-and-finance': 'economy',
    'health-funding-and-workforce': 'health', 'health-services': 'health', 'housing-affordability': 'housing',
    'infrastructure-funding-and-planning': 'transport-and-infrastructure', 'international-relations': 'defence-and-foreign-affairs',
    'internet-and-digital-technologies': 'economy', 'jobs-and-employment': 'incomes-and-employment',
    'land-and-resources': 'te-ao-maori', 'local-government': 'law-justice-and-government', 'medicines': 'health',
    'oceans': 'environment', 'oil-gas-and-mining': 'economy', 'parliament-and-democracy': 'law-justice-and-government',
    'pasifika': 'community-and-inclusion', 'policing': 'law-justice-and-government', 'prices': 'incomes-and-employment',
    'public-health': 'health', 'public-sector': 'law-justice-and-government',
    'public-transport-cycling-and-walking': 'transport-and-infrastructure', 'regional-development': 'economy',
    'schools': 'education', 'sports-and-recreation': 'media-culture-and-recreation',
    'superannuation-and-savings': 'incomes-and-employment', 'tax-and-income-support': 'incomes-and-employment',
    'te-reo-maori-and-culture': 'te-ao-maori', 'te-tiriti-o-waitangi-and-governance': 'te-ao-maori',
    'tertiary-education-and-research': 'education', 'tertiary-fees-and-student-support': 'education',
    'tourism': 'economy', 'urban-planning-and-resource-management': 'transport-and-infrastructure',
    'wages-and-working-conditions': 'incomes-and-employment', 'waste-management': 'environment',
    'women': 'community-and-inclusion', 'young-people': 'community-and-inclusion'}

# act.org.nz policy pages (by fetched slug) that set out each policy.nz statement (index in policy.nz order).
RELATED = {
    0: ['let-pharmacies-do-more'], 1: ['let-pharmacies-do-more'], 2: ['burglary'], 3: ['closing-medicines-gap'],
    4: ['open-the-backcountry'], 5: ['equal-treatment-at-universities'], 6: ['stopping-coercion'], 7: ['paris'], 8: ['paris'],
    9: ['protect-lawful-hunting'], 10: ['public-safety'], 11: ['game-management'], 12: ['game-management'],
    13: ['affordable-uniforms'], 14: ['let-the-kid-on-the-bus'], 15: ['back-the-volunteers'], 16: ['local-tourism-dividend'],
    17: ['unlocking-new-zealands-digital-economy'], 18: ['unlocking-new-zealands-digital-economy'],
    19: ['put-reside-back-in-resident'], 20: ['student-services-fee'], 21: ['one-law-for-all'],
    22: ['equal-service'], 23: ['equal-service'], 24: ['equal-service'], 25: ['affordable-government'],
    26: ['welfare'], 27: ['welfare'], 28: ['keeping-children-safe'], 29: ['a-starship-for-cancer'],
    31: ['innovation-trials'], 32: ['fair-contribution', 'deport'], 33: ['deport'], 34: ['deport'],
    35: ['disrupt-the-class-leave-the-class'], 36: ['deport'], 37: ['scrap-net-zero-cut-the-carbon-tax'],
    38: ['scrap-net-zero-cut-the-carbon-tax'], 39: ['deport'], 40: ['deport'], 41: ['rural-crime'],
    42: ['professional-free-speech'], 43: ['wind-up-the-waitangi-tribunal'],
    44: ['keep-new-zealand-moving'], 45: ['keep-new-zealand-moving'], 46: ['keep-new-zealand-moving'], 47: ['keep-new-zealand-moving'],
    48: ['backing-small-business'], 49: ['backing-small-business'],
    50: ['backing-small-business', 'an-easier-end-to-dead-end-employment'], 51: ['backing-small-business'],
    52: ['backing-small-business'], 53: ['scrap-net-zero-cut-the-carbon-tax', 'make-farming-fun-again'],
    54: ['scrap-net-zero-cut-the-carbon-tax'], 55: ['scrap-net-zero-cut-the-carbon-tax', 'make-farming-fun-again'],
    56: ['make-farming-fun-again'], 57: ['crack-down-on-noisy-vehicles'], 58: ['open-the-door-to-supermarket-competition'],
    59: ['strengthening-end-of-life-choice'], 60: ['abundant-and-affordable-electricity'],
    61: ['abundant-and-affordable-electricity'], 62: ['abundant-and-affordable-electricity'],
    63: ['abundant-and-affordable-electricity'], 66: ['leave-spirituality-out-of-infrastructure'],
    67: ['leave-spirituality-out-of-infrastructure'], 68: ['leave-spirituality-out-of-infrastructure'],
    69: ['no-tax-on-kiwisaver-earnings'], 70: ['unlocking-mineral-wealth'], 71: ['unlocking-mineral-wealth'],
    72: ['unlocking-mineral-wealth'], 73: ['unlocking-mineral-wealth'], 74: ['unlocking-mineral-wealth'],
    76: ['make-farming-fun-again'], 78: ['fiscalplan'], 79: ['fiscalplan'], 80: ['fiscalplan'],
    81: ['fiscalplan', 'fair-funding-for-independent-schools'], 82: ['fiscalplan'], 83: ['abolish-labours-rental-tax'],
    84: ['plenty-is-possible'], 85: ['plenty-is-possible'], 86: ['plenty-is-possible'], 87: ['plenty-is-possible'],
    88: ['plenty-is-possible'], 89: ['tougher-penalties-for-rubbish-dumping'], 90: ['shorter-waits-for-your-gp'],
}

# Policies on act.org.nz that policy.nz (as downloaded) does not list. Summaries are neutral paraphrases
# of the linked ACT page; the documents hold the verbatim text.
ARCHIVE = [
    ('ACT-A01', 'Expand charter schools to 10,000 enrolments by the end of 2029', ['education', 'schools'],
     'ACT says charter schools give families more choice and educators more freedom, with accountability for results, and that more than 2,000 students are already enrolled.',
     'Protect charter schools from closure, set a target of 10,000 enrolments by end-2029 with annual reporting, remove barriers to state and state-integrated schools converting, encourage new charter schools where there is demand (aiming for an option in every major town), fund growth from existing education budgets and keep performance standards.',
     ['expanding-charter-schools']),
    ('ACT-A02', 'Create a national pathway into the trades from school', ['education', 'schools', 'jobs-and-employment', 'young-people'],
     'ACT says too many young people are pushed towards university without a proper chance to try a trade, and wants trades on an equal footing with university.',
     'Remove funding caps on approved trades subjects at school (with funding following students who learn off-site), create Industry Awards alongside University Entrance, and give employers a stronger say in subjects through Industry Skills Boards.',
     ['a-real-pathway-to-a-trade']),
    ('ACT-A03', 'Remove voting rights from unelected council appointees, including the Independent Māori Statutory Board', ['law-justice-and-government', 'local-government', 'te-ao-maori'],
     'ACT says ratepayers should be able to vote out everyone who votes at the council table.',
     'Amend the Local Government Act so unelected members of council committees and subcommittees cannot vote or count toward quorum, change Auckland Council law so Independent Māori Statutory Board members cannot vote on committees, and apply the rule to every kind of appointee.',
     ['no-votes-for-unelected-reps', 'news-act-time-to-end-voting-rights-for-unelected-council-appointees']),
    ('ACT-A04', 'Abolish the Climate Change Commission', ['environment', 'emissions-reduction', 'public-sector', 'government-revenue-and-finance'],
     'ACT says the Commission costs $14–15 million a year, duplicates work done elsewhere in government and recommends policies ACT considers harmful.',
     'Abolish the Commission as an independent Crown entity and transfer emissions-target monitoring and reporting to the Ministry for Cities, Environment, Regions and Transport, alongside the greenhouse gas inventory and the ETS.',
     ['scrap-the-climate-change-commission', 'make-farming-fun-again']),
    ('ACT-A05', 'Allow grazing licences on conservation land to control wilding pines and fire risk', ['environment', 'conservation', 'agriculture'],
     'ACT says targeted grazing could control invasive vegetation and wildfire fuel loads on suitable DOC land more cheaply than aerial spraying.',
     'Amend the Conservation Act 1987 to direct DOC to issue grazing licences for specified areas, set an ecological framework for where grazing is appropriate, set practical licence conditions and recognise virtual fencing as compliant stock exclusion.',
     ['grazing', 'make-farming-fun-again']),
    ('ACT-A06', 'Create a three-year Rural Workforce Visa for farm work', ['migration', 'agriculture', 'jobs-and-employment'],
     'ACT says farms need a reliable year-round supply of workers that current visas do not provide.',
     'A standalone three-year visa for dairy, sheep and beef and general farm work, tied to accredited rural employers rather than a region, reissued for three more years if no New Zealander is available, with a residence pathway after six years; it would be exempt from ACT\'s proposed infrastructure levy.',
     ['rural-visa', 'make-farming-fun-again']),
    ('ACT-A07', 'Cut non-frontline government spending back to 2017 levels per person', ['economy', 'government-revenue-and-finance', 'public-sector'],
     'ACT says public service staffing and spending grew sharply from 2017 to 2023 without better services.',
     'Return non-welfare spending outside protected frontline services (health, education, defence, police, children\'s services) to its 2017 level per person adjusted for inflation and wage growth, phased in over three years; ACT\'s fiscal plan says this cuts $9.5 billion a year once fully implemented.',
     ['fiscalplan']),
    ('ACT-A08', 'Keep contributions to the NZ Superannuation Fund suspended', ['economy', 'government-revenue-and-finance', 'superannuation-and-savings'],
     'ACT says borrowing to invest in markets adds risk to the Crown balance sheet while taxpayers already pay interest on debt.',
     'Maintain the current suspension of Crown contributions to the New Zealand Superannuation Fund (listed in ACT\'s Fiscal Plan as a non-operating change).',
     ['fiscalplan']),
    ('ACT-A09', 'Make councils compensate landowners for overlays such as Significant Natural Areas', ['environment', 'land-and-resources', 'agriculture', 'urban-planning-and-resource-management'],
     'Part of ACT\'s Make Farming Fun Again plan; ACT says landowners should not bear the cost of restrictions imposed for public benefit.',
     'Require councils to pay fair compensation when they restrict private land through overlays such as Significant Natural Areas or Outstanding Natural Landscapes, and protect farmers from a return to Labour-style SNA rules.',
     ['make-farming-fun-again']),
    ('ACT-A10', 'Recognise trusted overseas approvals for agricultural chemicals and veterinary medicines', ['agriculture', 'economy', 'business-support'],
     'Part of ACT\'s Make Farming Fun Again plan, aimed at lowering farm costs and improving access to competing products.',
     'Speed up access to proven agricultural chemicals and veterinary medicines by recognising trusted overseas approvals.',
     ['make-farming-fun-again']),
    ('ACT-A11', 'Let routine farm work proceed without resource consent where it meets national standards', ['agriculture', 'urban-planning-and-resource-management', 'environment'],
     'Part of ACT\'s Make Farming Fun Again plan; ACT says consent costs for routine work add cost without environmental benefit.',
     'Introduce at least ten new permitted-activity standards (e.g. farm plans, vegetable growing, on-farm water storage, gravel extraction, drain maintenance, effluent, fertiliser, farm quarries, wetland restoration, small/medium solar) and let farmers change land use without consent where consistent with National Standards.',
     ['make-farming-fun-again']),
    ('ACT-A12', 'Ease restrictions on agricultural drones and farm technology', ['agriculture', 'internet-and-digital-technologies', 'business-support'],
     'Part of ACT\'s Make Farming Fun Again plan, aimed at productivity and lower operating costs.',
     'Remove unnecessary restrictions on agricultural drones and other technology that can improve productivity and reduce operating costs.',
     ['make-farming-fun-again']),
    ('ACT-A13', 'Cut red tape on homekill and direct farm-to-consumer sales', ['agriculture', 'business-support', 'prices'],
     'Part of ACT\'s Make Farming Fun Again plan.',
     'Cut red tape around homekill and make it easier for farmers to sell their products directly to consumers.',
     ['make-farming-fun-again']),
    ('ACT-A14', 'Review the Sharemilking Agreements Act', ['agriculture', 'jobs-and-employment'],
     'Part of ACT\'s Make Farming Fun Again plan; ACT says the Act should reflect how farming businesses operate today.',
     'Review the Sharemilking Agreements Act.',
     ['make-farming-fun-again']),
    ('ACT-A15', 'Long-term funding to eradicate wilding pines, with DOC coordinating pest control', ['environment', 'conservation', 'agriculture'],
     'Part of ACT\'s Make Farming Fun Again plan; ACT says this reduces the burden on individual farmers.',
     'Commit to long-term wilding pine eradication funding, direct DOC to coordinate pest control across public and private land, make permanent forest owners carry long-term costs and risks including pest control, and keep catchment-group funding at $13.5 million by redirecting $4.5 million a year within MPI.',
     ['make-farming-fun-again', 'scrap-net-zero-cut-the-carbon-tax']),
    ('ACT-A16', 'Accept food labels that meet UK, EU or US requirements by default', ['economy', 'prices', 'business-support'],
     'Part of ACT\'s supermarket competition policy; ACT says NZ-specific labelling adds cost and is a barrier to new entrants.',
     'Recognise food labels from trusted overseas systems by default, alongside faster alcohol licensing and removing inconsistent local requirements for new stores.',
     ['open-the-door-to-supermarket-competition']),
    ('ACT-A17', 'Legalise plug-in solar and implement the Solar Regulatory Review', ['energy', 'prices', 'emissions-reduction'],
     'Part of ACT\'s electricity policy; ACT says red tape is limiting household solar.',
     'Implement the recommendations of the Ministry for Regulation\'s Solar Regulatory Review, including legalising plug-in solar, and lift unnecessary limits on households exporting solar power.',
     ['abundant-and-affordable-electricity']),
    ('ACT-A18', 'Oppose forced break-ups of the big electricity generator-retailers', ['energy', 'economy', 'prices'],
     'Part of ACT\'s electricity policy; ACT says forced break-ups would deter investment in new generation.',
     'Oppose forced break-ups of the major generator-retailers while strengthening enforcement against misuse of market power to shut out competitors.',
     ['abundant-and-affordable-electricity']),
    ('ACT-A19', 'Renegotiate New Zealand\'s Paris Agreement commitment, and leave if a fair deal is not possible', ['international-relations', 'emissions-reduction', 'environment', 'agriculture'],
     'ACT says current targets ignore the different warming effects of methane and carbon dioxide and penalise efficient farmers.',
     'Issue a New Zealand-designed NDC on a split-gas basis and renegotiate the Paris commitment; if a fairer arrangement cannot be reached, New Zealand should be prepared to leave.',
     ['paris', 'scrap-net-zero-cut-the-carbon-tax']),
]

# ---------------------------------------------------------------- helpers
by_slug = collections.defaultdict(list)
for u, r in store.items():
    by_slug[r['slug']].append(r)


def html_rec(slug):
    for r in by_slug.get(slug, []):
        if r.get('kind') == 'html':
            return r
    raise KeyError(slug)


def clean(t):
    return t.replace('⁠', '').replace(' ', ' ').replace('​', '')


def slugify(s):
    s = urllib.parse.unquote(s).lower().replace('’', '').replace("'", '')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:90]


def norm_url(u):
    return re.sub(r'^(https?://web\.archive\.org)?/web/\d+[a-z_]*/', '', u.strip())


# ---- documents: group records into unique docs
docs = {}          # doc_slug -> info
url2doc = {}
pdf_hash2doc = {}
cite_titles = {}
for p in pnz['policies']:
    for c in p.get('citations', []):
        cite_titles.setdefault(norm_url(c['url']), c['title'].strip())

for u, r in store.items():
    if not r.get('ok'):
        continue
    if r['kind'] == 'pdf':
        h = hashlib.md5(re.sub(r'\s+', '', r['text']).encode()).hexdigest()
        if h in pdf_hash2doc:
            d = docs[pdf_hash2doc[h]]
            d['aliases'].append(u)
            if r.get('cited_by_policynz'):
                d['cited'] = True; d['cite_title'] = d.get('cite_title') or cite_titles.get(u)
            url2doc[u] = d['slug']
            continue
        base = os.path.basename(urllib.parse.urlparse(r['final_url']).path)
        slug = 'pdf-' + slugify(re.sub(r'\.pdf$', '', base, flags=re.I))
        pdf_hash2doc[h] = slug
        docs[slug] = {'slug': slug, 'rec': r, 'kind': 'pdf', 'source_url': r['final_url'], 'aliases': [u],
                      'cited': bool(r.get('cited_by_policynz')), 'cite_title': cite_titles.get(u)}
        url2doc[u] = slug
    else:
        slug = r['slug']
        docs[slug] = {'slug': slug, 'rec': r, 'kind': 'html', 'source_url': r['final_url'], 'aliases': [u],
                      'cited': bool(r.get('cited_by_policynz')), 'cite_title': cite_titles.get(u)}
        url2doc[u] = slug

# PDF titles: first page heading lines (skipping the date line)
TITLE_OVERRIDE = {'pdf-smallergovt-2': 'ACT’s plan for a consolidated bureaucracy',
                  'pdf-act-2026-fiscal-plan': 'ACT Fiscal Plan 2026',
                  'pdf-acts-plan-to-make-farming-fun-again': 'ACT’s Plan to Make Farming Fun Again',
                  'pdf-local-gov-letter-on-bill': 'Letter to the Minister of Local Government on unelected committee members (8 September 2025)',
                  'pdf-local-government-restoring-democratic-integrity-v1-9': 'Local Government (Restoring Democratic Integrity) Amendment Bill (Member’s Bill, draft for consultation)'}


def pdf_title(d):
    if d['slug'] in TITLE_OVERRIDE:
        return TITLE_OVERRIDE[d['slug']]
    if d.get('cite_title'):
        m = re.match(r"^'(.+?)'\s*\(PDF\)", d['cite_title'])
        if m:
            return m.group(1).strip()
    first = d['rec']['text'].split('\f')[0]
    lines = [l.strip() for l in first.splitlines() if l.strip()]
    out = []
    for l in lines:
        if re.fullmatch(r'[\d .]+', l) or l.upper() == 'DRAFT FOR CONSULTATION':
            continue
        if len(l) > 45 or (out and l[0].islower() is False and l in ("Member's Bill", 'Member’s Bill')):
            break
        out.append(l)
        if len(out) >= 4:
            break
    t = ' '.join(out)
    return re.sub(r'\s+', ' ', t).strip() or os.path.basename(d['source_url'])


HTML_TITLE_OVERRIDE = {'fiscal-plan': 'balancethebooks.nz — “ACT will pay down debt faster” (ACT fiscal plan microsite)'}


def html_title(d):
    if d['slug'] in HTML_TITLE_OVERRIDE:
        return HTML_TITLE_OVERRIDE[d['slug']]
    r = d['rec']
    t = clean(r.get('h1') or '').strip()
    if not t:
        t = r.get('page_title', d['slug'])
    return t


def html_date(r):
    for b in r['blocks'][:4]:
        m = re.fullmatch(r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), (\d{1,2} \w+ \d{4})', b.strip())
        if m:
            return m.group(2)
    return None


BULLET = re.compile(r'^\s*([•●▪◦‣]|–\s|\d+\.\s|[a-z]\)\s|\(\w{1,3}\)\s)')


def pdf_to_md(rec):
    pdf_path = os.path.join(ROOT, rec['raw_file']) if rec.get('raw_file') else None
    # reading-order extraction (default pdftotext mode handles the two-column layout correctly)
    text = subprocess.run(['pdftotext', pdf_path, '-'], capture_output=True, text=True).stdout if pdf_path else rec['text']
    pages = clean(text).split('\f')
    out = []
    for i, pg in enumerate(pages, 1):
        if not pg.strip():
            continue
        out.append(f'<!-- page {i} -->')
        if len(re.findall(r'\(\d+\.\d{3}\)', pg)) >= 10 and pdf_path:
            lay = subprocess.run(['pdftotext', '-layout', '-f', str(i), '-l', str(i), pdf_path, '-'],
                                 capture_output=True, text=True).stdout
            out.append('```text\n' + clean(lay).rstrip() + '\n```')
            continue
        for block in re.split(r'\n\s*\n', pg):
            lines = [l.strip() for l in block.splitlines() if l.strip()]
            if not lines:
                continue
            para = []
            for l in lines:
                if para and not BULLET.match(l):
                    if para[-1].endswith('-') and not para[-1].endswith(' -'):
                        para[-1] = para[-1] + l
                    else:
                        para[-1] = para[-1] + ' ' + l
                else:
                    para.append(l)
            for p in para:
                p = re.sub(r'^[•●▪◦‣]\s*', '- ', p)
                p = re.sub(r'^([#>+*|])', r'\\\1', p)
                p = re.sub(r'^(\d+)\.(\s)', r'\1\\.\2', p) if not BULLET.match(p) else p
                out.append(p)
    return '\n\n'.join(out)


def html_to_md(rec):
    out = []
    for b in rec['blocks']:
        b = clean(b)
        m = re.match(r'^(#+) (.*)$', b)
        if m:
            lvl = min(len(m.group(1)), 6)
            out.append('#' * max(lvl, 2) + ' ' + m.group(2))
        elif b.startswith('- '):
            out.append(b)
        else:
            b = re.sub(r'^([>+*|])', r'\\\1', b)
            out.append(b)
    # keep consecutive list items together
    txt = ''
    for i, line in enumerate(out):
        if i and line.startswith('- ') and out[i - 1].startswith('- '):
            txt += '\n' + line
        else:
            txt += ('\n\n' if i else '') + line
    if rec.get('links'):
        seen, links = set(), []
        for a in rec['links']:
            if a['href'] in seen or 'action.act.org.nz/r?' in a['href']:
                continue
            seen.add(a['href']); links.append(a)
        if links:
            txt += '\n\n---\n\n**Links in the original text:**\n\n' + '\n'.join(
                f"- {clean(a['text']) or '(link)'} → <{a['href']}>" for a in links)
    return txt


for slug, d in docs.items():
    r = d['rec']
    d['title'] = pdf_title(d) if d['kind'] == 'pdf' else html_title(d)
    d['date'] = html_date(r) if d['kind'] == 'html' else None
    if d['kind'] == 'html':
        d['doc_type'] = 'press release' if '/news/' in d['source_url'] else (
            'policy index page' if '/policies' in d['source_url'] else 'policy page')
        if 'scoop.co.nz' in d['source_url']:
            d['doc_type'] = 'press release (Scoop mirror)'
        if 'balancethebooks.nz' in d['source_url']:
            d['doc_type'] = 'fiscal plan microsite'
    else:
        d['doc_type'] = 'policy document (PDF)'

# full-policy PDF links from each html page -> doc slugs
page_pdfs = {}
for u, r in store.items():
    if r.get('kind') == 'html' and r.get('ok'):
        page_pdfs[r['slug']] = [url2doc[x] for x in r.get('full_policy_links', []) if x in url2doc]


def write_doc(d):
    r = d['rec']
    fm = ['---', f'title: {json.dumps(d["title"], ensure_ascii=False)}', 'party: act',
          f'source_url: {d["source_url"]}']
    others = sorted(set(a for a in d['aliases'] if a != d['source_url']))
    if others:
        fm.append('also_published_at:')
        fm += [f'  - {a}' for a in others]
    fm += [f'retrieved: {r["retrieved"]}', f'format: {d["kind"]}',
           'fetch_method: ' + ('curl (direct from origin), text extracted with pdftotext (reading order; tables kept with -layout)'
                               if d['kind'] == 'pdf' else
                               'curl (direct from origin), main content extracted with BeautifulSoup (tools/policies_act_fetch.py)'),
           f'document_type: {d["doc_type"]}']
    if d.get('date'):
        fm.append(f'published: {json.dumps(d["date"])}')
    if d['kind'] == 'pdf':
        fm.append(f'pages: {r.get("pages")}')
        fm.append(f'raw_file: {r.get("raw_file") or "(not kept: >10MB)"}')
    else:
        fm.append(f'raw_file: {r.get("raw_file")}.gz')
    fm.append(f'cited_by_policy_nz: {"true" if d["cited"] else "false"}')
    fm.append('---')
    body = pdf_to_md(r) if d['kind'] == 'pdf' else html_to_md(r)
    if 'scoop.co.nz' in d['source_url']:
        body = body.replace(' Advertisement - scroll to continue reading', '')
    head = [f'# {d["title"]}', '',
            f'*ACT New Zealand {d["doc_type"]}' + (f', {d["date"]}' if d.get('date') else '') +
            f'. Source: <{d["source_url"]}> (retrieved {r["retrieved"]}).*', '',
            '## Full text', '',
            '> Verbatim text as published; only whitespace and markup have been normalised.'
            + (' PDF page breaks are marked with HTML comments; tables are reproduced with their original layout.' if d['kind'] == 'pdf' else '')
            + (f" Extraction: {r['extraction']}." if r.get('extraction') else ''),
            '']
    pdfs = page_pdfs.get(d['slug']) if d['kind'] == 'html' else None
    txt = '\n'.join(fm) + '\n\n' + '\n'.join(head) + '\n' + body.strip() + '\n'
    if pdfs:
        txt += '\n---\n\n**Full policy document linked from this page:** ' + ', '.join(
            f'[{docs[p]["title"]}]({p}.md)' for p in dict.fromkeys(pdfs)) + '\n'
    open(os.path.join(DOCS, d['slug'] + '.md'), 'w').write(txt)


for d in docs.values():
    write_doc(d)


# ---------------------------------------------------------------- policies
GENERIC_SUBTOPICS = {'prices', 'business-support', 'economic-development-and-industry', 'government-revenue-and-finance', 'young-people'}


def primary_group(topics):
    for t in topics:
        if t.startswith('key-policies-'):
            return t[len('key-policies-'):]
    present = [t for t in topics if t in GROUPS]
    score = collections.Counter()
    for t in topics:
        if t in SUB2GROUP and SUB2GROUP[t] in present:
            score[SUB2GROUP[t]] += 0.5 if t in GENERIC_SUBTOPICS else 1
    if score:
        best = max(score.values())
        return sorted(g for g, n in score.items() if n == best)[0]
    if present:
        return present[0]
    score = collections.Counter(SUB2GROUP[t] for t in topics if t in SUB2GROUP)
    return score.most_common(1)[0][0]


def src_entry(slug, title=None, url=None):
    d = docs[slug]
    return {'title': title or d['title'], 'url': url or d['source_url'], 'document': f'documents/{slug}.md'}


def doc_sources(slugs, seen=None):
    """Sources for the given page slugs, followed (recursively) by the full-policy documents they link to."""
    out, seen = [], (set() if seen is None else seen)
    queue = list(slugs)
    while queue:
        s = queue.pop(0)
        if s in seen or s not in docs:
            continue
        seen.add(s); out.append(src_entry(s))
        queue[0:0] = page_pdfs.get(s, [])
    return out


policies = []
for i, p in enumerate(pnz['policies']):
    attrs = {a['name']: a['value'].strip() for a in p.get('attributes', [])}
    topics = list(dict.fromkeys(p['topics']))
    cited, seen = [], set()
    for c in p.get('citations', []):
        o = norm_url(c['url'])
        s = url2doc.get(o)
        if s and s not in seen:
            seen.add(s)
            cited.append({'title': c['title'].strip(), 'url': o, 'document': f'documents/{s}.md',
                          'policy_nz_citation': c['url'].strip()})
            cited += doc_sources(page_pdfs.get(s, []), seen)
        elif not s:
            cited.append({'title': c['title'].strip(), 'url': o, 'document': None,
                          'policy_nz_citation': c['url'].strip(), 'note': 'could not be fetched'})
    related = [x for x in doc_sources(RELATED.get(i, [])) if x['document'] not in {c['document'] for c in cited}]
    policies.append({
        'id': p['reference'], 'statement': re.sub(r'\s+', ' ', p['statement']).strip(), 'topics': topics,
        'topic_group': primary_group(topics), 'key_policy': any(t.startswith('key-policies-') for t in topics),
        'summary': {'why': attrs.get('Why'), 'how': attrs.get('How')}, 'summary_source': 'policy.nz',
        'sources': cited + [dict(x, relation='related ACT policy page/document') for x in related]})

for aid, stmt, topics, why, how, slugs in ARCHIVE:
    for s in slugs:
        assert s in docs, s
    policies.append({'id': aid, 'statement': stmt, 'topics': topics, 'topic_group': primary_group(topics),
                     'key_policy': False, 'summary': {'why': why, 'how': how}, 'summary_source': 'archive',
                     'sources': doc_sources(slugs)})

json.dump(policies, open(os.path.join(OUT, 'policies.json'), 'w'), indent=1, ensure_ascii=False)
print('policies', len(policies), 'docs', len(docs), file=sys.stderr)
json.dump({s: {'title': d['title'], 'kind': d['kind'], 'type': d['doc_type'], 'url': d['source_url'], 'date': d.get('date'),
               'cited': d['cited']} for s, d in docs.items()},
          open(os.path.join(RAW, 'docs_index.json'), 'w'), indent=1, ensure_ascii=False)


# ---------------------------------------------------------------- README
def md_link(src):
    if src.get('document'):
        return f"[{src['title']}]({src['document']}) ([original]({src['url']}))"
    return f"{src['title']} — <{src['url']}> (*not retrievable: {src.get('note', '')}*)"


def anchor(text):
    a = text.lower().strip()
    a = re.sub(r'[^\w\- ]', '', a, flags=re.U)
    return a.replace(' ', '-')


n_pnz = sum(1 for p in policies if p['summary_source'] == 'policy.nz')
n_arc = len(policies) - n_pnz
types = collections.Counter(d['doc_type'] for d in docs.values())
ret = sorted({d['rec']['retrieved'] for d in docs.values()})
acc = sorted({m for p in pnz['policies'] for c in p.get('citations', [])
              for m in re.findall(r'accessed (\d{2} \w+ 2026)', c['title'])}, key=lambda x: __import__('datetime').datetime.strptime(x, '%d %B %Y'))
fiscal = 'documents/pdf-act-2026-fiscal-plan.md'

L = []
L.append('# ACT New Zealand — 2026 election policies\n')
L.append(f'Every 2026 general-election (7 November 2026) policy of ACT New Zealand that this archive could find: '
         f'**{len(policies)} policies** — {n_pnz} from [policy.nz](https://policy.nz/parties/act-party) and {n_arc} additional policies found only on '
         f'[act.org.nz](https://www.act.org.nz/policies) — backed by **{len(docs)} full-text source documents** '
         f'({", ".join(f"{v} {k}" for k, v in types.most_common())}).\n')
L.append('**How this was built** ([`tools/policies_act_fetch.py`](../../../tools/policies_act_fetch.py), '
         '[`tools/policies_act_build.py`](../../../tools/policies_act_build.py)):\n')
L.append(f'- Starting point: the policy.nz dataset for ACT (`raw/policy.nz/parties/act-party.json`, {n_pnz} statements; policy.nz citations were accessed between {acc[0]} and {acc[-1]}). '
         'The **Why / How** text for those entries is policy.nz\'s neutral summary ("This party says …"), reproduced unchanged.')
L.append('- Every cited source was fetched again directly from its origin (policy.nz cites Wayback Machine snapshots; the archived original URL was fetched instead) '
         f'on {", ".join(ret)}. HTML pages were reduced to their main content; PDFs were converted with `pdftotext` '
         '(designed multi-column PDFs can interleave sidebars with body text in reading order; the original PDFs are kept in `raw/party-docs/act/pdf/`).')
L.append('- The full act.org.nz sitemap was crawled for policy pages (`/policies/*` index pages plus every policy landing page, excluding people, news archive and '
         '"ACT\'s Record" pages, which describe past actions rather than 2026 commitments). Every "Read the full policy" PDF linked from those pages was downloaded too.')
L.append(f'- Policies on act.org.nz that policy.nz does not list were added with `summary_source: "archive"` (IDs `ACT-A01`…`ACT-A{n_arc:02d}`); '
         'their Why/How summaries were written for this archive from the linked ACT page and should be checked against the full text.')
L.append('- Each policy links to the full verbatim text of its sources in [`documents/`](documents/). Duplicate PDFs (same file at several URLs) are stored once, with all URLs listed in the front matter.')
L.append('- Structured data: [`policies.json`](policies.json).\n')
L.append('> Summaries describe what ACT says it would do; they are not endorsements or fact-checks. ACT\'s own claims (costs, statistics) are reported as ACT\'s claims.\n')

# headline
L.append('## Headline commitments\n')
L.append('policy.nz flags these as ACT\'s **key policies**:\n')
for p in policies:
    if p['key_policy']:
        L.append(f"- [{p['statement']}](#{anchor(p['statement'] + ' ' + p['id'])}) — {GROUP_NAMES.get(p['topic_group'], p['topic_group'])}")
L.append('\nACT\'s own [Fiscal Plan page](documents/fiscalplan.md) summarises its programme as (verbatim):\n')
fp = html_rec('fiscalplan')['blocks']
i0 = fp.index('### ACT will:')
for b in fp[i0 + 1:]:
    if not b.startswith('- '):
        break
    L.append(clean(b))
L.append('')

# fiscal plan
L.append('## Fiscal plan / alternative budget\n')
L.append(f'ACT released its **[ACT Fiscal Plan 2026]({fiscal})** (12-page PDF, 11 October 2026; '
         '[original](https://assets.nationbuilder.com/actnz/pages/38747/attachments/original/1791599898/ACT_2026_Fiscal_Plan.pdf?1791599898)), '
         'with a landing page ([fiscalplan](documents/fiscalplan.md)) and an interactive debt microsite ([balancethebooks.nz](documents/fiscal-plan.md)). '
         'Key figures as stated in the PDF (all figures are ACT\'s; $ nominal):\n')
L += [
    '- **Debt:** net core Crown debt (excluding NZ Super Fund) of $217 billion by June 2031, which ACT says is $12.4 billion lower than current Treasury forecasts '
    '(the PDF\'s "Headline Figures" page also describes it as "$12 billion lower than forecast in the Pre-election Fiscal Update"; the costing table shows 217.336 vs 229.769).',
    '- **Operating balance:** OBEGAL surplus of $13.6 billion in 2030/31 (vs $8.9 billion under current Government plans); OBEGALx $16.4 billion (vs $11.7 billion); '
    'OBEGALx in small surplus in 2027/28, a year earlier than current plans; OBEGAL returns to a $5.1 billion surplus in 2028/29.',
    '- **No new taxes; no broad-based tax cuts in this plan** — "several strategic tax cuts" instead: no tax on KiwiSaver earnings ($1.065bn in 2027/28 rising to $1.437bn in 2030/31), '
    'a Carbon Tax Refund (est. ~$100 per household), an uncapped donation tax credit, reformed crypto tax treatment, and $264m of targeted tax relief "to be announced".',
    '- **New operating spending (outside the operating allowance), $445m in 2027/28 rising to $551m:** expanded pharmacy minor-ailments scheme, Local Tourism Dividend, '
    'Young Investors Fund (~$35m/yr, $500 for Year 11 students), Overstayers Investigation Unit ($60m/yr), rural crime funding, electronic money management for long-term Jobseeker recipients, '
    'Three Strikes for Burglary, Working with Children Check, independent school subsidy indexation, and a $100m/yr initiative "to be announced".',
    '- **Savings:** future operating allowances cut from $2.4bn to $2bn a year (+$0.4bn in 2027/28 rising to +$1.6bn in 2030/31); non-welfare, non-frontline spending returned to 2017 '
    'levels per person (headline reductions $1.5bn in 2027/28, $2.8bn, $3.2bn, $2.4bn in 2030/31 — including abolishing demographic ministries ~$187m/yr and cutting foreign aid to 2017 levels '
    'excluding Ukraine ~$283m/yr); NZ Super age rising by three months a year to 67 by 2035 ($0.46bn rising to $1.89bn, less compassionate early access); five-year benefit stand-down for '
    'residence-class visa holders; tighter medical certification for health/disability benefits; replacing the KiwiSaver Government Contribution ($0.52–0.59bn/yr); lower financing costs ($452m by 2030/31).',
    '- **Capital/non-operating:** $2m for anti-social noise cameras; $2bn contingency for a National Cancer Centre; $150m contingency for a new Epsom secondary school; '
    'maintain the suspension of NZ Super Fund contributions.',
    '- The landing page states ACT would "Cut $9.5 billion a year from spending outside welfare and protected frontline services once fully implemented" and '
    '"Make government smaller and more accountable, with 19 departments and 18 ministers".',
    f'- The full costing table is reproduced (layout preserved) at the end of the [Fiscal Plan document]({fiscal}).\n']

# ACT site structure
L.append('## How act.org.nz groups its policies\n')
L.append('ACT\'s [policy index](documents/policies.md) has these sections (each links to its own document): ' + ', '.join(
    f"[{docs[s]['title']}](documents/{s}.md)" for s in docs if s.startswith('policies-')) + '. '
    '(The Housing, Environment, Seniors and Welfare section pages contained no policy links when crawled.)\n')

# TOC
grouped = collections.OrderedDict((g, []) for g in GROUPS)
for p in policies:
    grouped.setdefault(p['topic_group'], []).append(p)
L.append('## Contents (by policy.nz topic group)\n')
for g, ps in grouped.items():
    if ps:
        L.append(f'- [{GROUP_NAMES.get(g, g)}](#{anchor(GROUP_NAMES.get(g, g))}) ({len(ps)})')
L.append('- [All source documents](#all-source-documents)\n')
L.append('Each policy appears once, under its main topic group (policy.nz "key policy" group where flagged, otherwise the group most of its sub-topics belong to); all its topics are listed with it.\n')

for g, ps in grouped.items():
    if not ps:
        continue
    L.append(f'## {GROUP_NAMES.get(g, g)}\n')
    for p in ps:
        L.append(f"### {p['statement']} ({p['id']})\n")
        meta = [f"Topics: {', '.join(p['topics'])}"]
        if p['key_policy']:
            meta.insert(0, '**Key policy** (policy.nz)')
        meta.append('Summary: ' + ('policy.nz' if p['summary_source'] == 'policy.nz' else 'this archive (not on policy.nz)'))
        L.append('*' + ' · '.join(meta) + '*\n')
        L.append(f"**Statement:** {p['statement']}\n")
        L.append(f"**Why:** {(p['summary']['why'] or '').strip()}\n")
        L.append(f"**How:** {(p['summary']['how'] or '').strip()}\n")
        L.append('**Full text:**\n')
        for s_ in p['sources']:
            L.append('- ' + md_link(s_) + (' *(related)*' if s_.get('relation') else ''))
        L.append('')

L.append('## All source documents\n')
L.append('| Document | Type | Date | Cited by policy.nz |')
L.append('|---|---|---|---|')
for s_, d in sorted(docs.items(), key=lambda kv: (kv[1]['doc_type'], kv[1]['title'].lower())):
    L.append(f"| [{d['title']}](documents/{s_}.md) | {d['doc_type']} | {d.get('date') or ''} | {'yes' if d['cited'] else ''} |")
L.append('')
L.append('### Not captured\n')
L.append('- Links in ACT pages that go through ACT\'s email click-tracking redirector (`action.act.org.nz/r?...`) could not be followed; where these pointed to a policy PDF, '
         'the same PDF was captured from its direct URL (e.g. the One Law for All policy).')
L.append('- "ACT\'s Record" pages, people pages and the ~3,000-item news archive were not captured except where a news item is a policy source.')
L.append('- The KiwiSaver calculator and the overseas-voting page are interactive/informational and were not captured.\n')
open(os.path.join(OUT, 'README.md'), 'w').write('\n'.join(L))
print('README written', file=sys.stderr)
