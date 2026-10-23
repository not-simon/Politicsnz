#!/usr/bin/env python3
"""Build parties/labour/policies/policies.json and README.md.

Inputs: raw/policy.nz/parties/labour-party.json (76 policy.nz statements), raw/party-docs/labour/fetch_index.json,
parties/labour/policies/documents/*.md (made by policies_labour_extract.py), and the ARCHIVE list below (policies
published by Labour that policy.nz does not list; summaries written for this archive, neutral, from the cited text).
Usage: python3 -I tools/policies_labour_build.py
"""
import json, os, re, importlib.util, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, 'parties', 'labour', 'policies')
DOCS = os.path.join(OUTDIR, 'documents')
spec = importlib.util.spec_from_file_location('f', os.path.join(ROOT, 'tools', 'policies_labour_fetch.py'))
F = importlib.util.module_from_spec(spec); spec.loader.exec_module(F)
LO = 'https://www.labour.org.nz/'
N = LO + 'news/'
SC = 'https://img.scoop.co.nz/media/pdfs/2610/Factsheet__School_Costs.pdf'

GROUPS = collections.OrderedDict([
    ('health', 'Health'), ('education', 'Education'), ('housing', 'Housing'), ('environment', 'Environment'),
    ('transport-and-infrastructure', 'Transport & infrastructure'), ('economy', 'Economy'),
    ('incomes-and-employment', 'Incomes & employment'), ('law-justice-and-government', 'Law, justice & government'),
    ('community-and-inclusion', 'Community & inclusion'), ('te-ao-maori', 'Te ao Māori'),
    ('defence-and-foreign-affairs', 'Defence & foreign affairs'), ('media-culture-and-recreation', 'Media, culture & recreation')])
PRIMARY_OVERRIDE = {'POL54670': 'economy', 'POL54687': 'economy', 'POL55151': 'housing', 'POL54753': 'media-culture-and-recreation',
                    'POL55043': 'incomes-and-employment', 'POL55092': 'economy', 'POL54768': 'transport-and-infrastructure',
                    'POL55312': 'media-culture-and-recreation', 'POL55313': 'media-culture-and-recreation',
                    'POL54899': 'economy', 'POL54916': 'economy', 'POL54945': 'incomes-and-employment', 'POL55306': 'te-ao-maori',
                    'POL54819': 'te-ao-maori', 'POL55147': 'te-ao-maori', 'POL55180': 'incomes-and-employment',
                    'POL55203': 'transport-and-infrastructure', 'POL55204': 'transport-and-infrastructure',
                    'POL55231': 'transport-and-infrastructure', 'POL55232': 'transport-and-infrastructure',
                    'POL55235': 'economy', 'POL55236': 'economy', 'POL55237': 'economy', 'POL55215': 'defence-and-foreign-affairs',
                    'POL54969': 'community-and-inclusion', 'POL54970': 'community-and-inclusion', 'POL54971': 'community-and-inclusion',
                    'POL54972': 'community-and-inclusion', 'POL55045': 'community-and-inclusion', 'POL55216': 'community-and-inclusion',
                    'POL54985': 'incomes-and-employment', 'POL55158': 'education', 'POL54716': 'education', 'POL55130': 'defence-and-foreign-affairs',
                    'POL55134': 'defence-and-foreign-affairs', 'POL54898': 'environment', 'POL54717': 'environment',
                    'POL55152': 'education', 'POL55153': 'health', 'POL55167': 'incomes-and-employment', 'POL55214': 'incomes-and-employment'}

# Extra Labour pages that set out the same policy in more detail (added to the policy.nz citations).
EXTRA = {
    'POL54665': [LO + 'affordable-healthcare'],
    'POL54669': [LO + 'affordable-healthcare', LO + 'ed-recovery-plan', LO + 'media/vtbneplb/labour-free-doctors-visits.pdf'],
    'POL54670': [N + 'release-targeted-tax-to-grow-the-economy-and-fund-free-doctor-s-visits/', LO + 'media/pfvguai5/labour-cgt.pdf'],
    'POL54685': [N + 'release-faster-cheaper-auckland-train-trips-under-labour/', LO + 'cost-of-living-plan'],
    'POL54686': [N + 'release-labour-to-make-maternity-scans-free/'],
    'POL54687': [N + 'release-labour-launches-new-zealand-future-fund/', LO + 'media/vbyf0pxe/the-new-zealand-future-fund.pdf'],
    'POL54689': [N + 'release-labour-will-make-cervical-screening-free/', LO + 'media/prhel1zq/cervical-screening-factsheet.pdf'],
    'POL54692': [N + 'release-labour-backs-family-doctors/', LO + 'media/dbskvb1y/backinglocaldoctors.pdf'],
    'POL54716': [N + 'release-labour-to-expand-apprenticeship-boost/', LO + 'good-jobs'],
    'POL54717': [N + 'release-labour-to-make-power-bills-more-affordable-with-solarsaver/'],
    'POL54718': [N + 'release-labour-is-backing-small-business-to-grow/', N + 'release-labour-s-plan-to-grow-the-economy-from-the-grassroots-up/'],
    'POL54719': [N + 'release-labour-to-open-up-govt-contracts-to-small-businesses/'],
    'POL54720': [N + 'release-labour-is-backing-small-business-to-grow/'],
    'POL54721': [N + 'release-labour-is-backing-small-business-to-grow/'],
    'POL54747': [LO + 'fiscal-plan', N + 'release-labour-will-back-kiwis-with-a-responsible-fiscal-plan/'],
    'POL54748': [LO + 'fiscal-plan', N + 'release-labour-will-back-kiwis-with-a-responsible-fiscal-plan/'],
    'POL54749': [LO + 'policy'], 'POL54750': [LO + 'policy', N + 'release-labour-s-plan-to-grow-the-economy-from-the-grassroots-up/'],
    'POL54751': [LO + 'policy'], 'POL54752': [LO + 'policy'],
    'POL54753': [LO + 'safer-online'],
    'POL54768': [LO + 'fuel-tax-freeze', N + 'release-no-increase-in-fuel-taxes-under-labour/'],
    'POL54819': [N + 'release-labour-is-backing-maori-into-skilled-work/'],
    'POL54820': [LO + 'graduate-nurse-job-guarantee'],
    'POL54822': [N + 'release-labour-will-scrap-national-s-boot-camps/'],
    'POL54898': [LO + 'fixing-the-ets'],
    'POL54969': [LO + 'immigration'], 'POL54970': [LO + 'immigration'], 'POL54971': [LO + 'immigration'], 'POL54972': [LO + 'immigration'],
    'POL54985': [LO + 'strengthening-kiwisaver'],
    'POL55043': [LO + 'fair-go-for-drivers'],
    'POL55044': [LO + 'fairer-workplaces'],
    'POL55045': [LO + 'community-housing-and-retirement-villages', N + 'release-labour-to-reform-retirement-village-repayments/'],
    'POL55092': [LO + 'fairer-grocery-prices'],
    'POL55129': [LO + 'foreign-affairs'], 'POL55130': [LO + 'foreign-affairs'], 'POL55131': [LO + 'foreign-affairs'],
    'POL55133': [LO + 'foreign-affairs'], 'POL55134': [LO + 'foreign-affairs', LO + 'fixing-the-ets'],
    'POL55151': [LO + 'start-work-now'], 'POL55152': [LO + 'start-work-now'], 'POL55153': [LO + 'start-work-now'],
    'POL55158': [LO + 'cutting-student-debt'],
    'POL55167': [LO + 'pay-equity', LO + 'fairer-workplaces'], 'POL55214': [LO + 'pay-equity'],
    'POL55180': [LO + 'fair-go-for-families'],
    'POL55189': [LO + 'government-you-can-trust', N + 'speech-trust-in-government-chris-hipkins/'],
    'POL55190': [LO + 'government-you-can-trust', N + 'speech-trust-in-government-chris-hipkins/', N + 'release-christopher-luxon-is-making-it-harder-to-vote/'],
    'POL55203': [LO + 'fair-go-for-drivers'], 'POL55204': [LO + 'fair-go-for-drivers'],
    'POL55215': [LO + 'immigration', LO + 'foreign-affairs'],
    'POL55216': [LO + 'disability', N + 'release-national-turns-flawed-disability-bill-into-law/'],
    'POL55231': [LO + 'better-deal-when-you-fly'], 'POL55232': [LO + 'better-deal-when-you-fly'],
    'POL55235': [N + 'release-labour-will-get-kiwis-a-better-deal-from-banks/'],
    'POL55236': [N + 'release-labour-will-get-kiwis-a-better-deal-from-banks/'],
    'POL55237': [N + 'release-labour-will-get-kiwis-a-better-deal-from-banks/'],
    'POL55255': [LO + 'cutting-back-to-school-costs'],
    'POL55282': [LO + 'cutting-back-to-school-costs', N + 'release-labour-will-cut-the-cost-of-getting-kids-back-to-school/', SC],
    'POL55284': [N + 'release-labour-will-cut-the-cost-of-getting-kids-back-to-school/', SC],
    'POL55285': [N + 'release-labour-will-cut-the-cost-of-getting-kids-back-to-school/', SC],
    'POL55306': [LO + 'backing-maori-businesses'],
}

NOTES = {
    'POL54747': 'Timing differs between sources: policy.nz (citing Labour\'s fiscal strategy page, archived 24 Aug 2026) says an OBEGAL surplus in 2029/30; Labour\'s later Fiscal Plan (labour.org.nz/fiscal-plan, released 4 Oct 2026) says an OBEGAL surplus in 2028/29.',
    'POL54748': 'Wording differs slightly: the Fiscal Plan page says "Net debt down towards 20% of GDP over time" in its key facts and "below 20% of GDP over time" in its body text.',
    'POL55129': 'policy.nz says 0.7% of GDP; Labour\'s Foreign Affairs page says "towards 0.7% of GNI as fiscal conditions allow".',
    'POL55238': 'Sourced by policy.nz to the 1News Leaders Debate (video, no transcript available) and a Labour release; the release text is reproduced in documents/.',
}

# Labour policies found on labour.org.nz that policy.nz does not list as separate statements.
# (id, statement, primary group, topics, summary, [source urls], costing or None, note or None)
ARCHIVE = [
 ('LAB-A01', 'Free up more than 4.5 million GP appointments a year', 'health', ['health', 'health-services'],
  'Labour says it would free up more than 4.5 million GP appointments a year through phone triage, better information for patients and technology that reduces paperwork (including AI scribes), backed by a new Digital Innovation Fund. It is part of the Medicard and ED Recovery Plan packages.',
  [LO + 'medicard', LO + 'ed-recovery-plan'], 'Medicard costing table (NZ$m): "AI scribe technology / Digital Innovation Fund" 4.3, 5, 5, 5 over four years.', None),
 ('LAB-A02', 'Create an Independent Pricing Authority to set GP funding', 'health', ['health', 'health-funding-and-workforce'],
  'An Independent Pricing Authority, modelled on Australia\'s Independent Health and Aged Care Pricing Authority, would set an evidence-based national funding rate for general practice by July 2028; Health NZ would have to fund any increase the following year, and money now collected as co-payments would be added to practice funding.',
  [LO + 'medicard'], 'Medicard costing table (NZ$m): Independent Pricing Authority 6 a year.', None),
 ('LAB-A03', 'ED Recovery Plan: ministerial direction on emergency departments and end the health hiring freeze', 'health', ['health', 'health-services'],
  'At a Labour Minister\'s first meeting with the Director-General of Health, Labour says it would direct an independent report on deaths linked to long ED waits, a nationwide stocktake of closed and unopened beds, restarted winter planning and stronger reporting, and end the current hiring freeze.',
  [LO + 'ed-recovery-plan', N + 'release-labour-will-get-emergency-departments-moving/'], None, None),
 ('LAB-A04', 'More emergency care outside hospital (paramedics, telehealth, pharmacists, early discharge teams)', 'health', ['health', 'health-services'],
  'Part of the ED Recovery Plan: more extended-care paramedics, a clinical telehealth service, longer emergency medicine supplies from pharmacists, and early supported discharge teams in every region.',
  [LO + 'ed-recovery-plan', N + 'release-labour-will-get-emergency-departments-moving/'], None, None),
 ('LAB-A05', 'Build Dunedin Hospital as originally committed', 'health', ['health', 'infrastructure-funding-and-planning'],
  'Labour said it would build Dunedin Hospital as it had committed to before the 2023 election, and accused the current Government of downgrading the project.',
  [N + 'release-labour-will-build-dunedin-hospital/'], None, 'The release is dated 1 December 2024 on labour.org.nz; it is included as a standing commitment, not a 2026 campaign announcement.'),
 ('LAB-A06', 'Fund 1,000 extra teacher aides', 'education', ['education', 'schools'],
  'Labour would fund 1,000 additional teacher aides, simplify learning-support funding to give schools more certainty and teacher aides more job security, and build on the 2022 Highest Needs Review to identify gaps in learning support.',
  [N + 'release-labour-to-provide-more-help-in-the-classroom/'], '$80 million over four years (Labour release, 22 Oct 2026).', None),
 ('LAB-A07', 'Establish an Independent Council for Curriculum and Assessment', 'education', ['education', 'schools'],
  'An Independent Council for Curriculum and Assessment would be set up in law to lead curriculum and assessment design, with an interim expert group in Labour\'s first three months. Curriculum changes not yet implemented would be paused for a year (maths and English work continues) and NCEA would stay unchanged until 2029.',
  [N + 'release-labour-to-give-parents-confidence-in-their-children-s-education/'], 'About $500,000 a year, from reprioritised baseline education funding.', None),
 ('LAB-A08', 'Restore the Te Tiriti o Waitangi obligation on school boards', 'education', ['education', 'schools', 'te-ao-maori', 'te-tiriti-o-waitangi-and-governance'],
  'Labour would reinstate the legal obligation for school boards to give effect to Te Tiriti o Waitangi; Willow-Jean Prime lodged a member\'s bill, the Education and Training (Upholding Te Tiriti o Waitangi) Amendment Bill, as a first step.',
  [N + 'release-labour-will-restore-te-tiriti-commitment-in-schools/'], None, None),
 ('LAB-A09', 'Partner with Māori in education', 'education', ['education', 'te-ao-maori', 'te-tiriti-o-waitangi-and-governance'],
  'Responding to a Waitangi Tribunal report on curriculum changes, Labour committed to working in partnership with Māori to enable greater Māori leadership over Māori education.',
  [N + 'release-labour-will-partner-with-maori-in-education/'], None, None),
 ('LAB-A10', 'Early childhood education: affirm Te Whāriki and restore ECE\'s purpose as education', 'education', ['education', 'early-childhood-education'],
  'Labour would affirm the Te Whāriki curriculum, continue the Early Learning Action Plan, restore the purpose of ECE as education and refresh the 10-year strategic plan; all communities, including Pacific language nests, Puna Reo and Te Kōhanga Reo, are to benefit.',
  [LO + 'early-childhood-education'], None, None),
 ('LAB-A11', 'ECE teacher pay parity, better ratios and smaller groups', 'education', ['education', 'early-childhood-education', 'wages-and-working-conditions'],
  'Labour says it is committed to working towards pay parity for ECE teachers with other teachers, would bring in stronger teacher-child ratios and smaller group sizes, and would remove barriers for qualified teachers (including English-language test exemptions for Pacific and other centres not teaching in English).',
  [LO + 'early-childhood-education'], None, None),
 ('LAB-A12', 'Stronger ECE oversight and restored network planning', 'education', ['education', 'early-childhood-education'],
  'Unannounced checks, clearer financial reporting and a better complaints process for ECE providers; restored network planning that supports community-based, smaller and parent-led providers; and better information about providers for parents.',
  [LO + 'early-childhood-education'], None, None),
 ('LAB-A13', 'Living Wage across the public service', 'incomes-and-employment', ['incomes-and-employment', 'wages-and-working-conditions', 'public-sector'],
  'Labour would require the Living Wage for all directly employed workers of government departments and departmental agencies, pay at least the Living Wage across the public service and publicly owned organisations, protect procurement standards, and work towards extending it across the wider public sector, starting with schools and hospitals.',
  [LO + 'fairer-workplaces'], None, None),
 ('LAB-A14', 'Introduce Fair Pay Agreements legislation in the first 100 days', 'incomes-and-employment', ['incomes-and-employment', 'wages-and-working-conditions'],
  'Labour would introduce legislation to bring back Fair Pay Agreements (sector-wide bargaining) within its first 100 days.',
  [LO + 'fairer-workplaces', LO + 'policy'], None, None),
 ('LAB-A15', 'Make collective agreements the default and review the Employment Relations Act', 'incomes-and-employment', ['incomes-and-employment', 'wages-and-working-conditions'],
  'Collective agreements would become the default (with the choice of an individual agreement), and Labour would review the Employment Relations Act, including minimum redundancy compensation and letting workers bargain with whoever actually controls their work.',
  [LO + 'fairer-workplaces'], None, None),
 ('LAB-A16', 'Ban most non-compete clauses and protect conditions when a business is sold', 'incomes-and-employment', ['incomes-and-employment', 'wages-and-working-conditions'],
  'Labour would ban most non-compete clauses in employment agreements and protect workers\' existing terms and conditions when a business is sold or a contract changes hands.',
  [LO + 'fairer-workplaces'], None, None),
 ('LAB-A17', 'Reinstate leave entitlements removed by Holidays Act changes', 'incomes-and-employment', ['incomes-and-employment', 'wages-and-working-conditions'],
  'Labour would roll back the current Government\'s employment changes and reinstate leave entitlements removed by changes to the Holidays Act.',
  [LO + 'fairer-workplaces'], None, None),
 ('LAB-A18', 'Stronger protections for gig and platform workers', 'incomes-and-employment', ['incomes-and-employment', 'wages-and-working-conditions'],
  'Labour would reject the "gateway test", work on greater protections for gig and platform workers and work towards ratifying ILO Convention 193.',
  [LO + 'fairer-workplaces'], None, None),
 ('LAB-A19', 'Reverse health and safety law changes and ratify ILO Convention 190', 'incomes-and-employment', ['incomes-and-employment', 'wages-and-working-conditions'],
  'Labour would reverse the current Government\'s changes to health and safety law and ratify ILO Convention 190 on violence and harassment at work (alongside the separate corporate homicide offence).',
  [LO + 'fairer-workplaces'], None, None),
 ('LAB-A20', 'Require employers to publish pay gaps (pay transparency)', 'incomes-and-employment', ['incomes-and-employment', 'wages-and-working-conditions', 'women'],
  'Labour would require employers to publish pay gaps between different groups of staff. Carmel Sepuloni\'s Pay Transparency Bill (announced Oct 2025) would require employers with more than 150 staff to report gender and ethnic pay differences and include pay ranges in job advertisements.',
  [LO + 'fairer-workplaces', N + 'release-mandatory-pay-reporting-to-help-close-pay-gaps/'], None, None),
 ('LAB-A21', 'Independent review of Fire and Emergency NZ', 'law-justice-and-government', ['law-justice-and-government', 'public-sector'],
  'A Labour Government would start an independent review of Fire and Emergency New Zealand\'s funding and operations.',
  [N + 'release-labour-will-launch-independent-review-into-fenz/'], None, None),
 ('LAB-A22', 'Extend presumptive cancer cover and ACC cover for firefighters', 'law-justice-and-government', ['law-justice-and-government', 'wages-and-working-conditions'],
  'Labour would extend presumptive occupational cancer cover for firefighters (no need to prove the cancer came from firefighting) and make Kieran McAnulty\'s member\'s bill extending ACC cover to volunteer firefighters government policy.',
  [N + 'release-labour-will-launch-independent-review-into-fenz/', N + 'release-labour-to-back-volunteer-firefighters-and-lower-power-bills-for-businesses/'], None, None),
 ('LAB-A23', 'Redirect up to $50m a year into Elevate to back innovative Kiwi companies', 'economy', ['economy', 'business-support', 'economic-development-and-industry'],
  'Labour would redirect up to $50 million a year of the Government\'s contribution to the NZ Super Fund into Elevate so more innovative businesses can expand in New Zealand.',
  [N + 'release-labour-s-plan-to-grow-the-economy-from-the-grassroots-up/'], 'Up to $50 million a year, redirected from NZ Super Fund contributions.', None),
 ('LAB-A24', 'Expand the Game Development Sector Rebate', 'economy', ['economy', 'business-support', 'arts-culture-and-heritage'],
  'Labour would lift the rebate rate to 25%, lower the minimum annual spend threshold to $200,000 so smaller studios qualify, and raise the maximum annual rebate from $3 million to $4.5 million, within the existing $40 million a year.',
  [N + 'release-labour-backs-kiwi-game-developers-to-grow/'], 'Within the existing $40 million a year rebate budget.', 'Announced 22 October 2025.'),
 ('LAB-A25', 'Require a small-business impact check before new laws and rules', 'economy', ['economy', 'business-support', 'public-sector'],
  'Under Small Business First, ministers and agencies would have to consider the impact on small businesses before new laws, regulations and procurement rules are approved.',
  [LO + 'small-business-first'], None, None),
 ('LAB-A26', 'Keep the operating allowance at $2.4b and fund commitments within existing allowances', 'economy', ['economy', 'government-revenue-and-finance'],
  'Labour\'s Fiscal Plan keeps the operating allowance at the $2.4 billion per Budget set at Budget 2026 and fits its announced capital commitments (about $4.1 billion) within $12 billion of future capital allowances; Labour says the plan was independently reviewed by accounting firm Hall Chadwick.',
  [LO + 'fiscal-plan', N + 'release-labour-will-back-kiwis-with-a-responsible-fiscal-plan/'], 'See Fiscal Plan section above.', None),
 ('LAB-A27', 'Reverse planned public service cuts', 'economy', ['economy', 'public-sector', 'government-revenue-and-finance'],
  'Labour would reverse half of the additional cuts planned for the next Budget and fully reverse cuts planned for future Budgets, while expecting agencies to spend carefully.',
  [LO + 'fiscal-plan'], 'Funded within the Fiscal Plan (no separate figure published on the page).', None),
 ('LAB-A28', 'Support the NZ-India free trade agreement (with conditions)', 'economy', ['economy', 'trade-and-exports'],
  'Labour said it would support the NZ-India FTA while warning businesses about its investment-target clawback, and said it had secured Government commitments on more labour inspectors, faster visa variations and progress on the Modern Slavery Bill.',
  [N + 'release-labour-to-support-india-free-trade-agreement/'], None, 'Position announced 23 April 2026.'),
 ('LAB-A29', 'Repeal the Regulatory Standards Act in the first 100 days', 'law-justice-and-government', ['law-justice-and-government', 'parliament-and-democracy'],
  'Labour has committed to repeal the Regulatory Standards Act within its first 100 days; Duncan Webb also lodged a member\'s bill to repeal it.',
  [N + 'release-labour-to-repeal-regulatory-standards-act-winston-are-you-in/'], None, 'Announced 25 November 2025.'),
 ('LAB-A30', 'Lobbying register, code of conduct and stand-down period for ex-ministers', 'law-justice-and-government', ['law-justice-and-government', 'parliament-and-democracy'],
  'Labour would introduce a mandatory code of conduct and a public register of paid lobbyists (showing who pays them) and a stand-down period so former ministers cannot move straight into lobbying.',
  [LO + 'government-you-can-trust', N + 'speech-trust-in-government-chris-hipkins/'], None, None),
 ('LAB-A31', 'Modernise the Official Information Act', 'law-justice-and-government', ['law-justice-and-government', 'parliament-and-democracy'],
  'Labour would modernise the OIA, codify proactive releases (including ministers\' diaries) and create a penalties regime for breaches.',
  [LO + 'government-you-can-trust', N + 'speech-trust-in-government-chris-hipkins/'], None, None),
 ('LAB-A32', 'Limit parliamentary urgency', 'law-justice-and-government', ['law-justice-and-government', 'parliament-and-democracy'],
  'Urgency would be restricted to genuine emergencies, fixing urgent errors, Budgets and a 100-day plan signposted before the election, and rushed laws would be sent back to select committee.',
  [LO + 'government-you-can-trust', N + 'speech-trust-in-government-chris-hipkins/'], None, None),
 ('LAB-A33', 'One person, one vote in local elections', 'law-justice-and-government', ['law-justice-and-government', 'parliament-and-democracy', 'local-government'],
  'Labour would end the rule that allows some people to vote in more than one council area.',
  [N + 'speech-trust-in-government-chris-hipkins/'], None, None),
 ('LAB-A34', 'Donation disclosure for third-party campaigners', 'law-justice-and-government', ['law-justice-and-government', 'parliament-and-democracy'],
  'Third-party campaigners in local and national elections would have to disclose donations on the same terms as political parties.',
  [N + 'speech-trust-in-government-chris-hipkins/'], None, None),
 ('LAB-A35', 'Reform the UN Charter and back the WHO', 'defence-and-foreign-affairs', ['defence-and-foreign-affairs', 'international-relations', 'aid-development-and-institutions'],
  'Labour would support reviewing and "maturing" the UN Charter, support the World Health Organization and adopt the updated WHO health regulations.',
  [LO + 'foreign-affairs'], None, None),
 ('LAB-A36', 'Push for a ban on lethal autonomous weapons and parliamentary scrutiny of military deployments', 'defence-and-foreign-affairs', ['defence-and-foreign-affairs', 'defence-and-veterans', 'international-relations'],
  'Labour would seek an ICJ advisory opinion on the legality of lethal fully autonomous weapons and support international efforts to ban them, establish clear parliamentary scrutiny if New Zealand joins armed conflicts, and strengthen oversight of payloads launched from New Zealand.',
  [LO + 'foreign-affairs'], None, None),
 ('LAB-A37', 'Human rights defenders programme and recognition of gender apartheid', 'defence-and-foreign-affairs', ['defence-and-foreign-affairs', 'international-relations', 'women'],
  'Labour would set up a programme (including safe haven) for human rights defenders, strengthen advocacy for democracy and human rights including in Myanmar, and advocate for gender apartheid to be recognised in the Crimes Against Humanity Treaty.',
  [LO + 'foreign-affairs'], None, None),
 ('LAB-A38', 'Re-engage in climate diplomacy and back the global transition away from fossil fuels', 'defence-and-foreign-affairs', ['defence-and-foreign-affairs', 'environment', 'emissions-reduction'],
  'Labour says it would re-engage strongly in international climate diplomacy and support the global transition away from fossil fuels.',
  [LO + 'foreign-affairs'], None, None),
 ('LAB-A39', 'Not join AUKUS', 'defence-and-foreign-affairs', ['defence-and-foreign-affairs', 'defence-and-veterans', 'international-relations'],
  'A Labour Government would not join pillar one (nuclear-powered submarines) or pillar two of the AUKUS security pact.',
  [N + 'release-a-labour-government-will-not-join-aukus/'], None, 'The release is dated 1 December 2024 on labour.org.nz.'),
 ('LAB-A40', 'End annual benefit renewals for people with permanent disabilities', 'community-and-inclusion', ['community-and-inclusion', 'disability', 'benefits'],
  'Labour would end annual benefit renewals for people with verified permanent disabilities and work towards systemic change so disabled people can move into open employment.',
  [LO + 'disability'], None, None),
 ('LAB-A41', 'At least 25% of new Kāinga Ora homes to be accessible', 'housing', ['housing', 'social-and-public-housing', 'disability'],
  'Labour would require at least a quarter of new Kāinga Ora builds to be accessible.',
  [LO + 'disability'], None, None),
 ('LAB-A42', 'Strengthen disability rights in law', 'community-and-inclusion', ['community-and-inclusion', 'disability'],
  'Labour would require agencies to produce Enabling Good Lives impact assessments, targets and actions; amend the Human Rights Act to define reasonable accommodation and treat denying it as discrimination; progress incorporating the UN Convention on the Rights of Persons with Disabilities into law; and build disabled leadership capacity.',
  [LO + 'disability'], None, None),
 ('LAB-A43', '$950m Crown guarantee for the Community Housing Funding Agency', 'housing', ['housing', 'social-and-public-housing'],
  'From Labour\'s first Budget in 2027, a $950 million Crown guarantee for CHFA social bonds would let community housing providers borrow more cheaply; Labour cites a CHFA estimate that for every 11 homes built the saving could pay for a twelfth.',
  [LO + 'community-housing-and-retirement-villages', N + 'release-labour-backs-community-housing-to-build-more-homes/'], 'A contingent guarantee: only called on in the event of a default (Labour).', None),
 ('LAB-A44', 'Independent disputes service for retirement village residents', 'community-and-inclusion', ['community-and-inclusion', 'seniors'],
  'Alongside the three-month repayment rule, Labour would set up an independent disputes resolution service for retirement village residents and protect genuinely vulnerable small, rural and charitable villages without creating a loophole for larger operators.',
  [LO + 'community-housing-and-retirement-villages', N + 'release-labour-to-reform-retirement-village-repayments/'], None, None),
 ('LAB-A45', 'Landlords to provide curtains or window coverings (member\'s bill)', 'housing', ['housing', 'renting', 'housing-quality'],
  'Helen White\'s member\'s bill would extend the healthy homes standards so landlords must provide insulated curtains or window coverings in rentals.',
  [N + 'release-labour-bill-helps-renters-save-on-energy-costs/'], None, 'A Labour MP\'s member\'s bill (drawn 21 May 2026), not listed on Labour\'s policy hub.'),
 ('LAB-A46', 'Energy performance standards for office buildings (member\'s bill)', 'environment', ['environment', 'energy', 'emissions-reduction'],
  'Rachel Brooking\'s Building (Energy Efficient Office Buildings) Amendment Bill would require office buildings to meet energy performance standards.',
  [N + 'release-labour-to-back-volunteer-firefighters-and-lower-power-bills-for-businesses/'], None, 'A Labour MP\'s member\'s bill (drawn 23 July 2026), not listed on Labour\'s policy hub.'),
 ('LAB-A47', 'SolarSaver: $30m community battery fund and free EECA advice', 'environment', ['environment', 'energy'],
  'Alongside the SolarSaver loans and subsidies, Labour would create a $30 million community battery fund so neighbourhoods share the benefits, have EECA act as a free one-stop shop for advice, quotes and finance matching, and ensure fair time-of-use rates for power exported to the grid.',
  [LO + 'solarsaver'], 'Part of SolarSaver\'s $160 million over four years (funded by repurposing the Gas Security fund).', None),
 ('LAB-A48', 'Ban secret car-finance commissions and allow 14 days to cancel car-yard insurance', 'transport-and-infrastructure', ['transport-and-infrastructure', 'cars-and-roads', 'prices'],
  'As part of A Fair Go For Drivers and the Fair Go Law, Labour would ban secret car finance commissions and give buyers 14 days to cancel add-on insurance bought at the car yard without penalty.',
  [LO + 'fair-go-for-drivers', LO + 'fair-go-for-families'], None, None),
 ('LAB-A49', 'Advertised ticket prices to include all mandatory fees', 'incomes-and-employment', ['incomes-and-employment', 'prices'],
  'Under the Fair Go Law the advertised price of tickets (and other goods) would have to include all mandatory fees, with no surprise checkout charges, and introductory-offer pricing would have to be clear.',
  [LO + 'fair-go-for-families', N + 'release-a-fair-go-for-families/'], None, None),
 ('LAB-A50', 'Require disclosure of international money transfer fees (member\'s bill)', 'incomes-and-employment', ['incomes-and-employment', 'prices'],
  'Arena Williams\'s member\'s bill would amend the Financial Markets Conduct Act 2013 to require full disclosure of fees, commissions and exchange rates before an international money transfer is made; it passed its first reading in April 2026.',
  [N + 'release-labour-bill-ending-hidden-transfer-fees-passes-first-reading/'], None, 'A Labour MP\'s member\'s bill.'),
]

OVERVIEW = [LO + 'policy', LO + 'cost-of-living-plan', LO + 'affordable-healthcare', LO + 'good-jobs', LO + 'laboursaver',
            LO + 'costofliving', LO + 'healthcare', LO + 'homes', LO + 'jobs',
            N + 'speech-labour-party-campaign-launch-2026-chris-hipkins/', N + 'speech-trust-in-government-chris-hipkins/']


def load_docs():
    idx = json.load(open(os.path.join(ROOT, 'raw', 'party-docs', 'labour', 'fetch_index.json')))
    m = {}
    for u, r in idx.items():
        path = os.path.join(DOCS, r['slug'] + '.md')
        if not os.path.exists(path):
            continue
        fm = {}
        txt = open(path).read()
        for line in txt.split('---')[1].strip().split('\n'):
            k, v = line.split(':', 1)
            fm[k.strip()] = json.loads(v.strip())
        body = txt.split('---', 2)[2]
        rec = {'document': 'documents/%s.md' % r['slug'], 'title': fm.get('title', ''), 'published': fm.get('published'),
               'ok': r.get('status') == '200' and len(body.strip()) > 200}
        m[u.rstrip('/')] = rec
    return m


def doc_for(docs, url):
    return docs.get(F.original_url(url).rstrip('/'))


def costing_from(how):
    sents = re.split(r'(?<=[.!?])\s+', how or '')
    c = [s.strip() for s in sents if re.search(r'\bcost', s, re.I) and re.search(r'\$|costed', s)]
    return ' '.join(c) or None


def primary_group(pid, topics):
    if pid in PRIMARY_OVERRIDE:
        return PRIMARY_OVERRIDE[pid]
    for g in GROUPS:
        if 'key-policies-' + g in topics:
            return g
    for g in GROUPS:
        if g in topics:
            return g
    return 'economy'


def main():
    docs = load_docs()
    pj = json.load(open(os.path.join(ROOT, 'raw', 'policy.nz', 'parties', 'labour-party.json')))
    out, problems = [], []
    used_docs = set()
    for p in pj['policies']:
        pid = p['reference']
        topics = list(dict.fromkeys(t for t in p['topics']))
        attrs = {a['name'].lower(): re.sub(r'\s+', ' ', a['value']).strip() for a in p.get('attributes', [])}
        sources, seen = [], set()
        for c in p.get('citations', []):
            orig = F.original_url(c['url'])
            d = doc_for(docs, orig)
            key = orig.rstrip('/')
            if key in seen:
                continue
            seen.add(key)
            s = {'title': c.get('title', ''), 'url': orig, 'cited_by_policy_nz_as': c['url'], 'document': d['document'] if d else None}
            if not d:
                s['note'] = 'not retrievable'
            sources.append(s)
        for u in EXTRA.get(pid, []):
            key = u.rstrip('/')
            if key in seen:
                continue
            seen.add(key)
            d = doc_for(docs, u)
            sources.append({'title': d['title'] if d else '', 'url': u, 'added_by_archive': True, 'document': d['document'] if d else None})
        e = {'id': pid, 'statement': p['statement'].strip(), 'topics': topics, 'primary_group': primary_group(pid, topics),
             'summary': {'why': attrs.get('why', ''), 'how': attrs.get('how', '')}, 'summary_source': 'policy.nz',
             'costing': costing_from(attrs.get('how')), 'sources': sources}
        if pid in NOTES:
            e['notes'] = NOTES[pid]
        out.append(e)
    for (aid, st, grp, topics, summ, urls, cost, note) in ARCHIVE:
        sources = []
        for u in urls:
            d = doc_for(docs, u)
            sources.append({'title': d['title'] if d else '', 'url': u, 'document': d['document'] if d else None})
        e = {'id': aid, 'statement': st, 'topics': topics, 'primary_group': grp, 'summary': {'why': None, 'how': summ},
             'summary_source': 'archive', 'costing': cost, 'sources': sources}
        if note:
            e['notes'] = note
        out.append(e)
    for e in out:
        ok = [s for s in e['sources'] if s.get('document')]
        if not ok:
            problems.append('NO DOCUMENT: %s %s' % (e['id'], e['statement']))
        for s in e['sources']:
            if s.get('document'):
                used_docs.add(s['document'])
            else:
                problems.append('missing doc for source %s in %s' % (s['url'], e['id']))
    json.dump(out, open(os.path.join(OUTDIR, 'policies.json'), 'w'), indent=1, ensure_ascii=False)
    write_readme(out, docs, used_docs)
    alldocs = {'documents/' + f for f in os.listdir(DOCS)}
    orphan = alldocs - used_docs - {doc_for(docs, u)['document'] for u in OVERVIEW if doc_for(docs, u)}
    for p in problems:
        print(p)
    print('policies', len(out), 'policy.nz', len(pj['policies']), 'archive', len(ARCHIVE), 'docs', len(alldocs), 'orphans', sorted(orphan))


def body_of(doc):
    t = open(os.path.join(OUTDIR, doc)).read()
    return t.split('---', 2)[2]


def section(doc, start, stop_re=r'^#{2,4} '):
    """Return verbatim lines from a document between a line equal to `start` and the next heading."""
    lines, on = [], False
    for l in body_of(doc).split('\n'):
        if l.strip() == start:
            on = True
            continue
        if on and re.match(stop_re, l):
            break
        if on:
            lines.append(l)
    return '\n'.join(lines).strip()


def write_readme(out, docs, used):
    groups = collections.OrderedDict((g, []) for g in GROUPS)
    for e in out:
        groups[e['primary_group']].append(e)
    n_pnz = sum(1 for e in out if e['summary_source'] == 'policy.nz')
    n_arc = len(out) - n_pnz
    ndocs = len(os.listdir(DOCS))
    L = []
    A = L.append
    A('# Labour Party: 2026 election policies')
    A('')
    A('Every 2026 election policy of the New Zealand Labour Party that this archive could find, with summaries and links to the **full verbatim text** of every source page.')
    A('')
    A('- **%d policies** in total: **%d** listed by [policy.nz](https://policy.nz) (summaries by policy.nz, marked *policy.nz*) and **%d** more found on labour.org.nz that policy.nz does not list separately (summaries written for this archive, marked *archive*).' % (len(out), n_pnz, n_arc))
    A('- **%d full-text source documents** in [`documents/`](documents/): Labour\'s policy pages, PDFs, press releases and speeches on labour.org.nz, plus Scoop, RNZ and TVNZ pages that policy.nz cited. All were fetched from the original URLs (web.archive.org links in policy.nz were mapped back to the original pages) on **23 October 2026**. Text is verbatim; only the markup was turned into Markdown. Six policy PDFs (factsheets and policy documents linked from Labour pages) are also included as extracted text, and the PDFs themselves are kept in `raw/party-docs/labour/pdf/`.' % ndocs)
    A('- Structured data: [`policies.json`](policies.json). Scripts: `tools/policies_labour_fetch.py`, `tools/policies_labour_extract.py`, `tools/policies_labour_build.py`.')
    A('- How completeness was checked: every policy card on Labour\'s policy hub ([labour.org.nz/policy](https://www.labour.org.nz/policy)) and every page linked from it was captured. labour.org.nz has no sitemap.xml (it returns 404), so the list of all ~820 news items in the site\'s news menu was used instead: the ~300 most recent titles (roughly August 2025 to 22 October 2026) were read one by one and older ones were searched by keyword, and every release that announced a commitment was captured. Releases that only attack other parties, or report member\'s bills that have already passed, are not counted as policies.')
    A('- Each *archive* summary is a neutral restatement of what the linked Labour text says. Costings are Labour\'s own figures; none are independent estimates. Where sources disagree, this is noted.')
    A('')
    A('## Headline commitments')
    A('')
    A('These are the policy cards on Labour\'s [policy hub](https://www.labour.org.nz/policy), in Labour\'s order. Each description is Labour\'s own text (full page: [documents/policy.md](documents/policy.md)).')
    A('')
    hub = body_of('documents/policy.md').split('\n')
    i = 0
    while i < len(hub):
        l = hub[i]
        if l.startswith('### ') and 'Frequently asked' not in l:
            j = i + 1
            while j < len(hub) and not hub[j].strip():
                j += 1
            A('- **%s**: %s' % (l[4:].strip(), hub[j].strip()))
        if 'Frequently asked' in l:
            break
        i += 1
    A('')
    A('## Fiscal plan and costings')
    A('')
    A('Labour published its Fiscal Plan on 4 October 2026 ([labour.org.nz/fiscal-plan](https://www.labour.org.nz/fiscal-plan), full text: [documents/fiscal-plan.md](documents/fiscal-plan.md)). Its earlier fiscal strategy page is at [documents/fiscal-strategy.md](documents/fiscal-strategy.md). The key facts as Labour states them:')
    A('')
    A(section('documents/fiscal-plan.md', 'Key facts', r'^(#{2,4} |Hard work)'))
    A('')
    A('Capital commitments (from the Fiscal Plan page):')
    A('')
    A(section('documents/fiscal-plan.md', '### Capital commitments'))
    A('')
    A('Costings listed on Labour\'s policy hub FAQ ("How are Labour\'s policies being funded?"), verbatim:')
    A('')
    faq = body_of('documents/policy.md')
    m = re.search(r'Costings include:\n\n(.*?)\n\nWhen will', faq, re.S)
    if m:
        A(m.group(1).strip())
    A('')
    A('> Note on timing: policy.nz (citing Labour\'s August fiscal strategy page) gives the OBEGAL surplus year as 2029/30. Labour\'s Fiscal Plan of 4 October 2026 says 2028/29.')
    A('')
    A('## Contents by topic')
    A('')
    for g, items in groups.items():
        if items:
            A('- [%s](#%s) (%d)' % (GROUPS[g], anchor(GROUPS[g]), len(items)))
    A('- [Overview and plan documents](#overview-and-plan-documents)')
    A('')
    for g, items in groups.items():
        if not items:
            continue
        A('## %s' % GROUPS[g])
        A('')
        for e in items:
            A('### %s' % e['statement'])
            A('')
            other = [GROUPS[t] for t in GROUPS if t in e['topics'] and t != g]
            A('`%s` · summary: *%s*%s' % (e['id'], e['summary_source'], (' · also: ' + ', '.join(other)) if other else ''))
            A('')
            if e['summary'].get('why'):
                A('**Why:** ' + e['summary']['why'])
                A('')
            if e['summary'].get('how'):
                A(('**How:** ' if e['summary_source'] == 'policy.nz' else '**Summary:** ') + e['summary']['how'])
                A('')
            if e.get('costing'):
                A('**Costing (as stated):** ' + e['costing'])
                A('')
            if e.get('notes'):
                A('**Note:** ' + e['notes'])
                A('')
            A('**Full text:** ' + '; '.join(src_link(s) for s in e['sources']))
            A('')
    A('## Overview and plan documents')
    A('')
    A('Labour pages that group several policies together (also kept in full):')
    A('')
    for u in OVERVIEW:
        d = doc_for(docs, u)
        if d:
            A('- [%s](%s) ([original](%s))' % (d['title'] or u, d['document'], u))
    A('')
    open(os.path.join(OUTDIR, 'README.md'), 'w').write('\n'.join(L) + '\n')


def anchor(t):
    return re.sub(r'[^\w\- ]', '', t.lower()).replace(' ', '-')


def src_link(s):
    t = s.get('title') or s['url']
    t = t.replace('[', '(').replace(']', ')')
    if s.get('document'):
        return '[%s](%s) ([original](%s))' % (t, s['document'], s['url'])
    return '%s (%s), not retrievable' % (t, s['url'])


if __name__ == '__main__':
    main()
