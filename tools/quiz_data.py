#!/usr/bin/env python3
"""Hand-curated data for the 'Find your match' quiz (data/guide/quiz.json).

Each position is P(position, evidence, source, policy_id=None).
  position: -2 strongly disagree .. +2 strongly agree with the statement.
  source:   a URL, or 'doc:<party>/<file>.md' (resolved by quiz_build.py to that document's source_url),
            or None when policy_id is given (resolved to the first policy.nz citation, de-archived).
A party with no public position on a statement is simply absent (written as null in the JSON).
Never guess: every non-null cell must quote or closely paraphrase the cited source.
Build with:  python3 -I tools/quiz_build.py
"""

def P(position, evidence, source=None, policy_id=None):
    return {'position': position, 'evidence': evidence, 'source_url': source, 'policy_id': policy_id}

# ---- shared sources -------------------------------------------------------
KPMG = 'https://assets.kpmg.com/content/dam/kpmgsites/nz/pdf/2026/09/2026-election-policy-tracker-v4.pdf'
GPEACE = 'https://www.greenpeace.org/static/planet4-aotearoa-stateless/2026/10/8f5b71d1-election-2026-scorecard-ranking-methodology.pdf'
CTU = 'https://union.org.nz/wp-content/uploads/2026/10/NZCTU-Scorecards-2.pdf'
GREY = 'https://www.greypower.co.nz/assets/default/documents/{}-Response-Grey-Power-Election-Policy-2026.pdf'
SALIENT = 'https://salient.org.nz/post/which-party-should-i-vote-for-your-guide-to-the-2026-election'
RNZ_SMALL = 'https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election'
RNZ_SUPER = 'https://www.rnz.co.nz/news/politics_election-2026/1865995/national-adamant-its-superannuation-stance-has-not-changed'
NAT_ECON = 'https://assets.national.org.nz/web/prod/National%27s%20Economic%20Plan.pdf?v=1790557287'
TPB = 'https://en.wikipedia.org/wiki/Treaty_Principles_Bill'
RSB = 'https://en.wikipedia.org/wiki/Regulatory_Standards_Bill'
FASTTRACK = 'https://en.wikipedia.org/wiki/Fast-track_Approvals_Act_2024'
THREESTRIKES = 'https://en.wikipedia.org/wiki/Sentencing_(Reinstating_Three_Strikes)_Amendment_Act_2024'
ALLIANCE_TAX = 'https://allianceparty.nz/wp-content/uploads/2026/09/alliance-tax-justice-cost-of-living-policy-2026.pdf'
ALLIANCE = 'https://allianceparty.nz/{}/'
VISION = 'https://www.vision.org.nz/visionpolicies'
WRP = 'https://womensrightsparty.nz/policy/'
TTT = 'https://tetaitokerauparty.org.nz/our-policies/'
ALCP = 'https://www.alcp.org.nz/policy'
PALFREE = 'https://palfree.nz/'
CONS = 'https://conservatives.org.nz/policies/{}/'
NZOFP = 'https://freedom.kiwi/{}'
SOCIAL_MEDIA = 'https://www.1news.co.nz/2026/08/24/luxon-moves-to-ban-under-16s-from-social-media-but-act-nz-first-say-no/'
SOCIAL_MEDIA_LAB = 'https://www.1news.co.nz/2026/08/25/labour-backs-under-16s-social-media-ban-handing-luxon-lifeline/'
PALESTINE_2025 = 'https://www.1news.co.nz/2025/09/27/nz-will-not-yet-recognise-palestinian-statehood-peters-says-in-un-speech'
PUBERTY = 'https://www.1news.co.nz/2025/11/19/govt-halts-puberty-blockers-for-new-gender-dysphoria-patients'
GENETECH_NZF = 'https://www.odt.co.nz/news/national/nz-first-withhold-support-gene-tech-bill-unless-major-changes-made-rnz'
GENETECH_AG = 'https://agscience.org.nz/?p=16163'
GENTAILERS = 'https://www.odt.co.nz/news/national/govt-stops-short-major-energy-reform-rnz'

STATEMENTS = []

def S(id, issue, text, explainer, positions):
    STATEMENTS.append({'id': id, 'issue': issue, 'text': text, 'explainer': explainer, 'positions': positions})

# =========================================================================== TAX
S('q01', 'tax', 'New Zealand should introduce a capital gains tax (for example on investment and commercial property).',
  'New Zealand has no general capital gains tax; Labour is campaigning on a 28% tax on gains from investment and commercial property (family homes, farms, shares and KiwiSaver excluded).', {
  'labour': P(2, 'Create a 28% capital gains tax on commercial and residential property, excluding the family home, from 1 July 2027.', None, 'POL54670'),
  'national': P(-2, '"No new taxes, including no capital gains tax."', NAT_ECON),
  'act': P(-2, 'KPMG 2026 tax tracker lists ACT: "No capital gains tax" (plus a crypto capital-gains exemption).', KPMG),
  'green': P(1, 'Prefers wider wealth taxes; Green MP Teanau Tuiono called Labour\'s CGT "quite narrow" and said the Greens\' wealth tax would be more effective. Greens also propose a 33% capital acquisitions (inheritance/gift) tax.', 'https://pmn.co.nz/read/political/greens-criticise-labour-s-limited-capital-gains-tax-plan'),
  'alliance': P(2, '"The Alliance will introduce a broad-based capital gains tax, covering investment property, shares..." (33%, excluding the family home).', ALLIANCE_TAX),
})

S('q02', 'tax', 'There should be an annual wealth tax on people with very large fortunes (for example net wealth over $2–10 million).',
  'Greens propose 2.5% on net wealth over $10m; Te Pāti Māori a tiered tax from $2m; Labour has ruled a wealth tax out.', {
  'green': P(2, 'Introduce a 2.5% tax on net wealth over $10 million (family homes exempt).', None, 'POL55135'),
  'te-pati-maori': P(2, 'Implement a targeted wealth tax: 1.5% on net assets $2–5m, 2% on $5–10m, 2.5% over $10m ("A Kiwi Tax Plan").', None, 'POL54939'),
  'labour': P(-2, 'KPMG tracker: "Chris Hipkins has ruled out a wealth/inheritance tax."', KPMG),
  'national': P(-2, 'National\'s Economic Plan lists the Greens/Te Pāti Māori "Asset Tax" among "nine new taxes" it opposes; promises "no new taxes".', NAT_ECON),
  'act': P(-2, 'KPMG tracker lists ACT: "No wealth tax/inheritance tax."', KPMG),
  'nz-first': P(-1, 'KPMG tracker: NZ First position "Not stated, has previously opposed such taxes."', KPMG),
  'alliance': P(2, '"2.5% Wealth Tax: An annual tax on individual net wealth above $2 million."', ALLIANCE.format('alliance-tax-plan-first-20000-income-tax-free')),
})

S('q03', 'cost-of-living', 'GST should be removed from food such as fresh fruit and vegetables.',
  'GST is charged at 15% on almost all food. Removing it from some food was debated in 2023; in 2026 Te Pāti Māori offers a "No GST on Kai" credit instead.', {
  'te-pati-maori': P(1, '"Remove GST costs from kai" — delivered as an income-tax "Kai Credit" worth about eight weeks of groceries for people earning under $60,000, rather than a GST exemption at the till.', None, 'POL54938'),
  'animal-justice': P(2, '"Remove GST from fruits, vegetables, legumes, nuts and other core plant-based foods."', 'doc:animal-justice/policy-policy-summary.md'),
  'conservative': P(-1, 'Favours a lower overall GST rate (12.5%) rather than food exemptions: "A lower rate of GST -12.5% is favoured."', CONS.format('economy-1')),
})

S('q04', 'tax', 'The first slice of everyone\'s income (e.g. the first $10,000 or more) should be tax-free.',
  'NZ taxes income from the first dollar (10.5% up to $15,600). Several parties propose a tax-free threshold paid for by other taxes.', {
  'green': P(2, 'Make the first $10,000 people earn tax-free.', None, 'POL54735'),
  'te-pati-maori': P(2, 'Make the first $30,000 earned tax-free.', None, 'POL54812'),
  'nz-first': P(2, 'KPMG tracker: NZ First would "make the lowest tax bracket (currently $14,000 pa) of income tax-free no later than 1 April 2027."', KPMG),
  'alliance': P(2, '"Make the first $20,000 of every person\'s income completely tax-free."', ALLIANCE.format('alliance-tax-plan-first-20000-income-tax-free')),
  'vision-nz': P(2, '"Make the first $25,000 of personal income completely tax-free."', VISION),
})

# =========================================================================== COST OF LIVING / WORK
S('q05', 'cost-of-living', 'The government should force the big supermarket chains to be broken up or restructured to increase competition.',
  'Two groups (Foodstuffs and Woolworths) dominate groceries. Proposals range from splitting Foodstuffs to a state-owned supermarket, versus easing entry for new competitors.', {
  'green': P(2, 'Break up the supermarket duopoly and use part of it to create a government-owned supermarket.', None, 'POL55032'),
  'labour': P(2, 'Separate wholesale food businesses from the retail supermarket sector.', None, 'POL55092'),
  'national': P(1, 'Separate the Foodstuffs business into two nationwide cooperatives (a targeted restructure rather than a full break-up).', None, 'POL55014'),
  'nz-first': P(2, 'Separate the Foodstuffs supermarket chain into two national cooperatives and give the Grocery Commissioner more powers.', None, 'POL54658'),
  'act': P(-2, '"While other parties destroy investor confidence by proposing break-ups, price controls, or state-run alternatives, ACT will focus on the barriers that make it hard for new competitors to enter."', 'doc:act/news-acts-plan-to-increase-supermarket-competition.md', 'POL55160'),
  'opportunity': P(1, 'Give the Commerce Commission greater powers and more market support to small businesses (no specific break-up).', None, 'POL54824'),
})

S('q06', 'work', 'The minimum wage should rise every year by at least the rate of inflation.',
  'Minimum-wage rises since 2023 have been below inflation. ACT proposes a three-year freeze.', {
  'labour': P(2, 'Increase the minimum wage every year; answered "Yes" to NZCTU: set the minimum wage above inflation for the next 3 years.', None, 'POL55238'),
  'nz-first': P(2, 'Increase the minimum wage in line with inflation; answered "Yes" to the NZCTU scorecard question.', None, 'POL55258'),
  'act': P(-2, 'Freeze the minimum wage for three years.', None, 'POL54990'),
  'green': P(2, 'NZCTU scorecard: "Yes" to setting the minimum wage above inflation for the next three years.', CTU),
  'te-pati-maori': P(2, 'NZCTU scorecard: "Yes" to setting the minimum wage above inflation for the next three years.', CTU),
  'alliance': P(2, 'NZCTU scorecard: "Yes" to setting the minimum wage above inflation for the next three years.', CTU),
  'vision-nz': P(2, '"Legislate the transition from the minimum wage to an annually adjusted Living Wage to protect working families from inflation."', VISION),
  'womens-rights': P(1, '"Minimum wages and benefits need to be increased so that all people have living incomes."', WRP),
})

S('q07', 'work', 'Fair Pay Agreements (industry-wide minimum pay and conditions negotiated by unions and employers) should be brought back.',
  'Labour introduced Fair Pay Agreements in 2022; the National-led government repealed them in December 2023.', {
  'labour': P(2, 'NZCTU scorecard: "Yes" to restoring Fair Pay Agreements in the first 100 days.', CTU),
  'green': P(2, 'Reverse changes to pay equity and fair pay agreements; NZCTU scorecard "Yes".', None, 'POL55104'),
  'te-pati-maori': P(2, 'NZCTU scorecard: "Yes" to restoring Fair Pay Agreements in the first 100 days.', CTU),
  'alliance': P(2, 'NZCTU scorecard: "Yes" to restoring Fair Pay Agreements in the first 100 days.', CTU),
  'national': P(-2, 'Repealed the Fair Pay Agreements Act in December 2023 (all National MPs voted for repeal); NZCTU scorecard "No".', 'https://union.org.nz/election-scorecards-26/'),
  'act': P(-2, 'Supported the 2023 repeal; NZCTU scorecard "No".', 'https://union.org.nz/election-scorecards-26/'),
  'nz-first': P(-2, 'NZCTU scorecard: "No" to restoring Fair Pay Agreements.', CTU),
  'opportunity': P(-1, 'NZCTU scorecard: "No" to restoring Fair Pay Agreements in the first 100 days.', CTU),
  'womens-rights': P(2, 'Advocates "reinstatement of legislative support for Fair Pay Agreements."', WRP),
})

# =========================================================================== HOUSING
S('q08', 'housing', 'Annual rent increases should be capped by law.',
  'There is currently no cap on how much rent can rise (only one increase per 12 months). The Greens propose a 2% annual cap.', {
  'green': P(2, 'Limit annual rent increases to 2 percent.', None, 'POL55082'),
  'labour': P(-1, 'In 2023 Chris Hipkins ruled out the Greens\' rent cap, saying it was not under consideration "and would not be in the future"; Labour\'s 2026 rent pledge covers only state/social housing tenants.', 'https://www.teaonews.co.nz/2023/07/04/pm-rules-out-greens-rental-cap/'),
  'national': P(-1, 'Focuses on building more homes "rather than controlling rents" (Salient 2026 guide); points to rent increases at a 25-year low.', SALIENT),
  'act': P(-2, 'Favours increasing supply through deregulation and property rights "rather than measures such as rent controls" (Salient 2026 guide).', SALIENT),
  'alliance': P(1, 'Caps social-housing rent at 25% of income (state-owned housing only).', ALLIANCE.format('the-right-to-a-roof-alliance-housing-policy')),
})

S('q09', 'housing', 'The government should build a lot more state and public housing.',
  'Kāinga Ora\'s building programme was scaled back after 2023; the government has focused on community housing providers and private supply.', {
  'green': P(2, 'Increase public housing supply and housing support.', None, 'POL55081'),
  'labour': P(2, 'Add at least 6,000 more social housing places over the next four years.', None, 'POL55151'),
  'te-pati-maori': P(2, 'Increase the supply of housing in both the public and private sector; wants more public and affordable housing.', None, 'POL55071'),
  'alliance': P(2, '"A five-year housing plan: a massive public building programme led by Kāinga Ora, alongside a newly established Ministry of Works."', ALLIANCE.format('the-right-to-a-roof-alliance-housing-policy')),
  'national': P(-1, '"Focused primarily on building more homes rather than controlling rents... free up land, streamline planning and consenting" — supply-led, not a state building programme (Salient guide).', SALIENT),
  'act': P(-1, 'Favours "increasing supply through deregulation, stronger property rights and easier consenting" and "greater faith in private investment... than in direct government provision".', SALIENT),
  'te-tai-tokerau-party': P(1, 'Mana Taumaru local build policy: hemp-panel homes built by local trainees on papakāinga, allocated to families in overcrowded or substandard housing.', TTT),
})

S('q10', 'housing', 'Councils should have to allow more and denser housing, such as townhouses and apartments, in our cities.',
  'Zoning rules decide how many homes can be built. Recent reforms (MDRS, "Going for Housing Growth") push councils to allow more density.', {
  'opportunity': P(2, 'Revamp zoning to reduce house prices.', None, 'POL54853'),
  'national': P(2, 'Wants to "free up land, streamline planning and consenting, and finance the infrastructure needed for development" (Salient guide); removing the ban on minimum car-parking is the only partial exception.', SALIENT),
  'act': P(2, 'Favours increasing supply through deregulation and easier consenting (Salient guide).', SALIENT),
  'green': P(1, 'Encourage mixed-use areas and walkability in new housing developments.', None, 'POL55084'),
  'nz-first': P(-1, 'Add infrastructure and service-capacity requirements to residential fast-track permissions (growth only where infrastructure keeps up).', None, 'POL55305'),
})

# =========================================================================== HEALTH
S('q11', 'health', 'Some GP visits each year should be free for everyone.',
  'Most adults pay $20–$80+ per GP visit. Labour proposes a "Medicard" with three free visits a year, funded by its capital gains tax.', {
  'labour': P(2, 'Make up to three GP visits a year free with a Medicard.', None, 'POL54669'),
  'green': P(2, 'Increase free public health services.', None, 'POL55118'),
  'alliance': P(2, '"Elimination of costs for GP visits, dental, optical, and audiology services."', ALLIANCE.format('alliance-health-policy-free-gp-dental-optical-audiology')),
  'national': P(-1, 'Says Labour\'s "free" promises (including the Medicard) total $18 billion and would need "nine new taxes"; offers rural doctor funding and pharmacist access instead.', NAT_ECON),
})

S('q12', 'health', 'The $5 prescription charge should be scrapped.',
  'The previous government removed the $5 prescription co-payment in 2023; the current government reinstated it for most adults in 2024.', {
  'labour': P(2, 'Remove the $5 charge for prescriptions (restore universal free prescriptions).', None, 'POL54665'),
  'national': P(-1, 'Keeps the $5 charge it reinstated in 2024 for most adults, with "targeted free prescriptions to seniors" instead of universal free prescriptions.', 'doc:national/news-20261022-retirement.md'),
})

# =========================================================================== EDUCATION
S('q13', 'education', 'Free school lunches should be expanded and made more generous, even if it costs more.',
  'Ka Ora, Ka Ako school lunches were kept but cut to roughly $3 a meal in 2024 under a model designed by ACT\'s David Seymour.', {
  'green': P(2, 'Keep and expand the free school lunches programme.', None, 'POL54722'),
  'labour': P(2, 'Pay for school lunches that cost $5 per meal and ensure schools provide locally made lunches.', None, 'POL55284'),
  'opportunity': P(2, 'Rebuild the school lunch programme.', None, 'POL54887'),
})

S('q14', 'education', 'Charter (partnership) schools should be allowed to continue.',
  'Charter schools are state-funded but privately run. They were reintroduced in 2025 by the National-ACT-NZ First government.', {
  'act': P(2, 'ACT campaigns on expanding charter schools.', 'doc:act/expanding-charter-schools.md'),
  'labour': P(-2, 'Labour vowed in 2024 to "get rid of" charter schools if returned to government.', 'https://www.1news.co.nz/2024/08/12/labour-vows-to-get-rid-of-charter-schools-if-it-regains-power/'),
  'green': P(-2, 'Green alternative Budget 2025 includes "Abolition of Charter Schools Agency".', 'doc:green/green-budget-2025.md'),
})

S('q15', 'education', 'University and polytechnic study should be fees-free.',
  'Fees-free first-year study (2018) was replaced in 2025 by a smaller final-year scheme.', {
  'green': P(2, 'Introduce fees-free tertiary education, universal student allowances and paid placements.', None, 'POL55035'),
  'alliance': P(2, 'Platform promises "free education and healthcare" (RNZ summary of the Alliance).', RNZ_SMALL),
  'labour': P(-1, 'Labour\'s 2026 student offer is a 10% student-loan cut for graduates who did not get Fees Free, not a return to fees-free study.', 'doc:labour/cutting-student-debt.md'),
  'national': P(-1, 'National\'s student policy is lowering the student-loan repayment rate to 10%, not fees-free study.', None, 'POL54813'),
})

# =========================================================================== CRIME & JUSTICE
S('q16', 'crime-justice', 'Repeat serious offenders should face mandatory longer sentences under a "three strikes" law.',
  'Labour repealed three strikes in 2022; the current government reinstated a version in December 2024.', {
  'national': P(2, 'Voted for the Sentencing (Reinstating Three Strikes) Amendment Act 2024 at every reading.', THREESTRIKES),
  'act': P(2, 'Voted for reinstating three strikes; 2026 policy adds a minimum three-year sentence for a third burglary conviction.', THREESTRIKES, 'POL54644'),
  'nz-first': P(2, 'Voted for the Reinstating Three Strikes Amendment Act 2024.', THREESTRIKES),
  'labour': P(-2, 'Voted against reinstatement; justice spokesperson Duncan Webb said three-strikes regimes did little to reduce serious crime.', THREESTRIKES),
  'green': P(-2, 'Voted against; Tamatha Paul said it would disproportionately target Māori and increase incarceration.', THREESTRIKES),
  'te-pati-maori': P(-2, 'Voted against the Reinstating Three Strikes Bill.', THREESTRIKES),
  'alliance': P(-1, 'Justice policy reframes it as "Three strikes and into treatment" — prevention and rehabilitation rather than longer sentences.', ALLIANCE.format('alliance-justice-policy-three-strikes-into-treatment')),
  'conservative': P(1, 'Wants "meaningful consequences for serious and repeat offending" and longer sentences for repeat child sex offenders.', CONS.format('overview')),
})

S('q17', 'crime-justice', 'We should send fewer people to prison and put more into rehabilitation and community alternatives.',
  'NZ has one of the higher imprisonment rates in the OECD, and the prison population has been rising.', {
  'green': P(2, 'Prioritise rehabilitation for convicted offenders; reduce restrictions on judges\' decisions.', None, 'POL55138'),
  'te-pati-maori': P(2, 'Abolish prisons by 2040 and move towards restorative justice.', None, 'POL55283'),
  'opportunity': P(2, 'Boost court and rehabilitation funding to reduce reoffending.', None, 'POL54854'),
  'te-tai-tokerau-party': P(2, '"Prison Sinking Lid Policy" — shift non-violent offenders with addiction and mental-health needs out of prison into localised rehabilitation.', TTT),
  'alliance': P(2, '"Three strikes and into treatment. Prevent harm, rehabilitate, support victims."', ALLIANCE.format('alliance-justice-policy-three-strikes-into-treatment')),
  'legalise-cannabis': P(1, '"Education not incarceration" — redirect money from prohibition enforcement to health and education.', ALCP),
  'national': P(-1, 'Add 240 beds to Christchurch Men\'s Prison; backs tougher sentencing (three strikes).', None, 'POL54705'),
  'act': P(-1, 'Tougher sentencing, including a mandatory minimum for a third burglary conviction.', None, 'POL54644'),
})

# =========================================================================== CLIMATE
S('q18', 'climate', 'Farmers should pay for their greenhouse gas emissions, for example by bringing agriculture into the Emissions Trading Scheme.',
  'Agriculture produces about half of NZ\'s emissions but is not priced. The government dropped plans to price farm emissions before 2030.', {
  'green': P(2, '"We will bring agricultural emissions into the ETS" (answer to Greenpeace 2026 survey).', GPEACE, 'POL54834'),
  'te-pati-maori': P(2, 'Answered "Yes" to bringing agriculture into the ETS by mid-2027 (Greenpeace 2026 survey).', GPEACE),
  'opportunity': P(1, 'Strengthen the ETS and include agriculture; told Greenpeace it "will explore a cap-and-trade market or novel levy structure" for biogenic methane.', None, 'POL54810'),
  'labour': P(-1, 'Made no commitment to price farm emissions: "in government Labour will urgently review the ETS" (Greenpeace survey answer).', GPEACE),
  'national': P(-2, 'Maintain the current position of agricultural emissions not being priced or offset through the ETS.', None, 'POL55319'),
  'act': P(-2, 'Ensure agriculture is not part of the emissions trading scheme.', None, 'POL54666'),
  'nz-first': P(-2, '"No, NZ First does not support emissions pricing in any form unless adopted by key trading partners" (Greenpeace survey).', GPEACE),
  'conservative': P(-2, '"There is no climate emergency... Laws/agreements like the Paris Accord, Zero Carbon Act, and Emissions Trading Scheme impose significant costs."', CONS.format('agriculture')),
  'animal-justice': P(1, 'Wants to "redirect funds away from animal agriculture, through taxes" and transition farmers to plant-based agriculture.', 'doc:animal-justice/policy-ajp-animal-policies.md'),
  'alliance': P(1, 'Replace the ETS with a carbon tax on a polluter-pays principle (no specific farm carve-out stated).', ALLIANCE.format('alliance-environment-climate-sustainable-economy-policy')),
})

S('q19', 'climate', 'New Zealand should keep its legal net-zero 2050 target and stay in the Paris Agreement.',
  'The Zero Carbon Act (2019, passed almost unanimously) sets a net-zero target for 2050; NZ is a party to the 2015 Paris Agreement.', {
  'labour': P(2, '"Labour is fully committed to the Paris Agreement and will put New Zealand on course to meet its targets."', 'doc:labour/fixing-the-ets.md'),
  'green': P(2, 'Enforce timely implementation of climate legislation and increase Zero Carbon Act reporting and transparency.', None, 'POL54859'),
  'opportunity': P(2, 'Retain the Climate Change Commission and ensure NZ\'s emissions goals align with the Paris Agreement.', None, 'POL55169'),
  'act': P(-2, 'Repeal the Zero Carbon Act and NZ\'s net-zero goal.', None, 'POL55046'),
  'nz-first': P(-2, 'Says it would withdraw New Zealand from the Paris Agreement (Salient guide; KPMG tracker: "Campaigned to leave the Paris Accord").', SALIENT),
  'conservative': P(-2, '"New Zealand should leave the Paris Agreement"; all climate legislation "should be repealed or withdrawn".', CONS.format('climate')),
  'vision-nz': P(-2, '"Restore absolute national sovereignty by leaving the United Nations and the Paris Accord."', VISION),
  'nz-loyal': P(-2, '"End climate accords based on faulty science" (party website as quoted by RNZ).', RNZ_SMALL),
  'nz-outdoors-freedom': P(-2, '"Let\'s get out of Paris accord and work for solutions to mitigate weather risks."', NZOFP.format('agriculture-policy')),
})

# =========================================================================== ENVIRONMENT
S('q20', 'environment', 'Ministers should be able to fast-track big infrastructure, mining and development projects past the normal consent process.',
  'The Fast-track Approvals Act 2024 lets listed projects skip the usual Resource Management Act process, with expert panels making the decisions.', {
  'national': P(2, 'Passed the Fast-track Approvals Act 2024 (supported at every reading) and proposes a fast-track policy statement for mining.', FASTTRACK, 'POL54701'),
  'act': P(2, 'Supported the Fast-track Approvals Act at every reading.', FASTTRACK),
  'nz-first': P(2, 'The Act was part of NZ First\'s coalition agreement; supported at every reading.', FASTTRACK),
  'labour': P(-1, 'Voted against the Act; "Labour will fix the Fast-track Approvals Act so that environmental protections are not overridden, there is public participation" (keeps a fast-track, but changed).', GPEACE),
  'green': P(-2, 'Repeal the Fast-track Approvals Act.', None, 'POL55095'),
  'te-pati-maori': P(-2, 'Voted against the Fast-track Approvals Act at all three readings.', FASTTRACK),
  'opportunity': P(-1, 'Answered "Yes" to restoring strong environmental protections and public participation in all resource consenting (Greenpeace survey).', GPEACE),
  'alliance': P(-1, 'Criticises the government for "fast-tracking legislation and using urgency for policies that harm Aotearoa New Zealand".', ALLIANCE.format('open-not-owned-alliance-trade-policy')),
})

S('q21', 'environment', 'Seabed mining should be banned in New Zealand waters.',
  'Trans-Tasman Resources\' South Taranaki iron-sands project has applied through fast-track; several parties want a permanent ban.', {
  'labour': P(2, 'Answered "Yes" to banning seabed mining (Greenpeace 2026 survey).', GPEACE),
  'green': P(2, 'Answered "Yes" to banning seabed mining (Greenpeace 2026 survey).', GPEACE),
  'te-pati-maori': P(2, 'Ban seabed mining.', None, 'POL54680'),
  'opportunity': P(2, 'Permanently ban seabed mining in NZ waters.', None, 'POL54827'),
  'national': P(-2, 'Voted against members\' bills to ban seabed mining (2023) and created the fast-track pathway used by seabed miners (Greenpeace assessment).', GPEACE),
  'act': P(-2, 'Voted against seabed-mining ban bills (2023); vocal pro-mining stance (Greenpeace assessment).', GPEACE),
  'nz-first': P(-2, '"No, NZ First does not support a ban; instead, we advocate for higher government levies on minerals extracted from coastal seabed iron sands."', GPEACE),
  'animal-justice': P(1, 'Key objective: "Restrict seabed mining" (restriction rather than outright ban).', 'doc:animal-justice/policy-ajp-animal-policies.md'),
})

S('q22', 'energy', 'The ban on new offshore oil and gas exploration should be brought back.',
  'Labour banned new offshore oil and gas permits in 2018; the Crown Minerals Amendment Act 2025 reversed the ban.', {
  'labour': P(2, 'Answered "Yes" to bringing back the ban (Greenpeace survey); Hipkins has said Labour would reinstate it while honouring existing permits.', GPEACE),
  'green': P(2, '"Yes. The Green Party wants to see new fossil fuel extraction ended in Aotearoa."', GPEACE),
  'te-pati-maori': P(2, 'Answered "Yes" to reinstating the ban (Greenpeace survey).', GPEACE),
  'opportunity': P(0, 'Would "not oppose a reinstatement" but considers it "probably unnecessary" and would not progress it itself.', GPEACE),
  'national': P(-2, 'Voted to repeal the ban (Crown Minerals Amendment Act 2025).', GPEACE),
  'act': P(-2, 'Voted to repeal the ban (Crown Minerals Amendment Act 2025).', GPEACE),
  'nz-first': P(-2, '"No. NZ First does not support reinstating a blanket ban on oil and gas exploration."', GPEACE),
  'conservative': P(-2, '"Actively encourage commercial oil and gas exploration."', CONS.format('natural-resources')),
  'nz-loyal': P(-2, '"Establish energy independence, including oil and gas" (party website as quoted by RNZ).', RNZ_SMALL),
  'animal-justice': P(2, '"Reverse the lifting of the offshore exploration ban and reinstate the moratorium on new fossil fuel permits."', 'doc:animal-justice/policy-ajp-environmental-and-economic-policies.md'),
})

S('q23', 'energy', 'The government should take a bigger direct role in electricity, such as a new state-owned power company or splitting up the big power companies.',
  'Four "gentailers" (Meridian, Mercury, Genesis, Contact) both generate and retail most power. A 2025 government review rejected structural separation.', {
  'green': P(2, 'Establish a publicly owned Crown entity ("Kiwipower") to invest in renewable generation.', None, 'POL54766'),
  'nz-first': P(2, 'Divide the "generation" and "retail" arms of power companies.', None, 'POL54656'),
  'opportunity': P(1, 'Restructure the electricity market to bring prices down; use the Crown\'s gentailer stakes to fund renewables.', None, 'POL54806'),
  'alliance': P(2, '"100 percent public ownership of electricity generation, transmission, distribution, and retail."', ALLIANCE.format('alliance-environment-climate-sustainable-economy-policy')),
  'national': P(-1, 'The National-led government\'s 2025 electricity review response did not include structural separation; Nicola Willis argued splitting the gentailers risked "massive instability".', GENTAILERS),
  'act': P(-2, 'Open power transmission to private investment; opposes break-ups and state-run alternatives.', None, 'POL55163'),
})

# =========================================================================== TE TIRITI / CO-GOVERNANCE
S('q24', 'te-tiriti', 'Parliament should define the principles of the Treaty of Waitangi in law, as ACT\'s Treaty Principles Bill proposed.',
  'The Treaty Principles Bill was voted down 112–11 at its second reading in April 2025; only ACT voted for it.', {
  'act': P(2, 'Sponsored the Treaty Principles Bill; its 11 MPs were the only votes in favour at the second reading (10 April 2025).', TPB),
  'national': P(-2, 'Voted against the Bill at its second reading after supporting it only to select committee; Luxon pledged to refuse a Treaty referendum.', TPB),
  'nz-first': P(-1, 'Voted against at the second reading, but its own policy is to remove references to "the principles of the Treaty" from legislation.', TPB),
  'labour': P(-2, 'Voted against at both readings; said the Bill\'s principles "did not match the principles of the Treaty".', TPB),
  'green': P(-2, 'Voted against at both readings.', TPB),
  'te-pati-maori': P(-2, 'Voted against at both readings; MPs led the haka protest at the first reading.', TPB),
})

S('q25', 'te-tiriti', 'The Waitangi Tribunal should be abolished or replaced once historical claims are settled.',
  'The Waitangi Tribunal (1975) investigates Crown breaches of the Treaty and makes mostly non-binding recommendations.', {
  'act': P(2, 'Abolish the Waitangi Tribunal once historical claims are resolved.', None, 'POL54960'),
  'nz-first': P(2, 'Replace the Waitangi Tribunal with a Treaty of Waitangi Completion Commission.', None, 'POL55157'),
  'te-pati-maori': P(-2, 'Make Waitangi Tribunal recommendations binding.', None, 'POL54795'),
  'green': P(-2, 'Implement Waitangi Tribunal recommendations; uphold te Tiriti across government decision-making.', None, 'POL54902'),
  'te-tai-tokerau-party': P(-2, 'Increase and entrench Waitangi Tribunal funding and extend its binding jurisdiction on the Crown.', TTT),
})

S('q26', 'te-tiriti', 'The Māori electorates should be abolished, or their future put to a referendum.',
  'Seven Māori electorates are elected by voters on the Māori roll. Abolishing or entrenching them is a recurring debate.', {
  'nz-first': P(2, 'Introduce a binding referendum on the Māori seats.', None, 'POL54757'),
  'green': P(-2, 'Entrench the Māori electoral seats.', None, 'POL54982'),
})

S('q27', 'te-tiriti', 'Government services should be allocated by need alone, without Māori- or ethnicity-specific programmes.',
  'Since 2023 the government has removed some ethnicity-based targeting (e.g. disestablishing Te Aka Whai Ora, the Māori Health Authority).', {
  'act': P(2, 'Remove ethnicity-based criteria for delivering public services.', None, 'POL54839'),
  'nz-first': P(1, 'Disestablish the Independent Māori Statutory Board from Auckland Council; policy is to remove "principles of the Treaty" references from environmental laws.', None, 'POL54668'),
  'vision-nz': P(2, '"Completely remove all race-based targeted policies and spending within the healthcare sector"; "End all race-based politics."', VISION),
  'conservative': P(2, '"Employment, promotion and access to public services should be based on individual need, ability and merit."', CONS.format('overview')),
  'nz-loyal': P(2, '"Scrap all race-based policies" (party website as quoted by RNZ).', RNZ_SMALL),
  'green': P(-2, 'Simplify funding for Hauora Māori providers; create a Māori Education Authority.', None, 'POL55119'),
  'te-pati-maori': P(-2, 'Invest in Māori health outcomes; Māori-led health, education, disability and justice systems.', None, 'POL55066'),
  'te-tai-tokerau-party': P(-2, '"Te Aka Motuhake" — an autonomous, state-funded, iwi-governed Māori health authority.', TTT),
  'labour': P(-1, 'Introduce a Māori-led job training programme and fund; allocate 5% of government procurement to Māori businesses.', None, 'POL54819'),
  'alliance': P(-1, 'Māori health providers keep the option to remain independent with full funding; constitutional change with Te Tiriti at the centre.', ALLIANCE.format('alliance-health-policy-free-gp-dental-optical-audiology')),
})

# =========================================================================== GOVERNANCE / DEMOCRACY
S('q28', 'democracy', 'The Regulatory Standards Act 2025 should be repealed.',
  'ACT\'s Regulatory Standards Act sets "principles of responsible regulation" that new laws are checked against. It passed 68–55 in November 2025.', {
  'labour': P(2, 'Lodged a member\'s bill to repeal it (Nov 2025); "Yes" to repealing it in the Greenpeace survey.', GPEACE),
  'green': P(2, '"Yes" to repealing the Regulatory Standards Act (Greenpeace survey).', GPEACE),
  'te-pati-maori': P(2, '"Yes" to repealing the Regulatory Standards Act (Greenpeace survey).', GPEACE),
  'opportunity': P(2, '"Yes" to repealing the Regulatory Standards Act (Greenpeace survey).', GPEACE),
  'te-tai-tokerau-party': P(2, '"As a matter of priority, vote to repeal both the Regulatory Standards Act 2025 and the Treaty Clauses Review."', TTT),
  'act': P(-2, 'Wrote and sponsored the Act (David Seymour, Minister for Regulation).', RSB),
  'national': P(-2, 'Voted for the Bill at all three readings; did not answer Greenpeace\'s repeal question.', RSB),
  'nz-first': P(0, 'Mixed: voted for it in 2025, Winston Peters then said NZ First would repeal it, but its 2026 Greenpeace survey answer did not commit to repeal.', GPEACE),
})

S('q29', 'democracy', 'Political donations should be capped, with only New Zealand voters allowed to donate.',
  'There is no cap on how much a person can donate to a party; companies, trusts and unions can donate.', {
  'opportunity': P(2, 'Cap donations at $30,000 per donor per election and ban donations from companies and trusts.', None, 'POL54809'),
  'green': P(2, '"Yes"; also "capping a donor\'s donations at a level that does not risk donor influence over policy."', GPEACE),
  'te-pati-maori': P(2, '"Yes" to limiting donations to registered voters (Greenpeace survey).', GPEACE),
  'animal-justice': P(1, 'Committed to "getting money out of politics" (no specific cap stated).', 'doc:animal-justice/election-2026-manifesto.md'),
  'labour': P(0, 'No commitment: "Labour believes in transparent and fair rules for political party donations" (Greenpeace survey).', GPEACE),
  'nz-first': P(0, 'Supports "electoral integrity and transparency" but has no policy restricting donations to voters (Greenpeace survey).', GPEACE),
})

S('q30', 'local-government', 'Central government should cap how much councils can raise rates each year.',
  'National proposes keeping annual rates rises within 2–4%; councils argue they need more funding tools for infrastructure.', {
  'national': P(2, 'Instruct councils to keep annual rate increases between 2 and 4 percent.', None, 'POL54817'),
  'green': P(-2, 'Reject the proposed rates cap and allow councils to use more funding tools.', None, 'POL55056'),
  'opportunity': P(-1, 'Give councils more tools to invest in infrastructure (rather than limiting revenue).', None, 'POL54811'),
})

# =========================================================================== IMMIGRATION
S('q31', 'immigration', 'Overall immigration to New Zealand should be reduced.',
  'Net migration hit records in 2023 and then fell sharply as more New Zealanders left for Australia.', {
  'nz-first': P(2, 'Replace the Accredited Employer Work Visa with a shortage-led skilled visa; remove automatic student-visa work rights; tie immigration to genuine labour shortages.', None, 'POL55262'),
  'vision-nz': P(2, '"Pause mass immigration immediately to review visa policies and relieve pressure on local infrastructure."', VISION),
  'conservative': P(1, 'Cap net immigration of unskilled and semi-skilled workers (zero if social goods are not increasing), while welcoming skilled migrants.', CONS.format('immigration')),
  'green': P(-1, 'Increase the refugee quota and support migrant workers to residency.', None, 'POL55127'),
})

S('q32', 'immigration', 'New residents should have to wait longer (five years or more) before they can get most benefits.',
  'Most benefits currently need two years\' residence. National proposes five; NZ First ten.', {
  'national': P(2, 'Change entitlements for benefits for new NZ residents to five years.', None, 'POL55230'),
  'nz-first': P(2, 'A benefit stand-down period of ten years for migrants, and longer residency for citizenship.', None, 'POL54965'),
  'act': P(2, '"ACT will introduce a five-year welfare stand-down for residence class visa holders" (2026 Fiscal Plan).', 'doc:act/pdf-act-2026-fiscal-plan.md', 'POL54881'),
})

# =========================================================================== SUPERANNUATION
S('q33', 'superannuation', 'The age of eligibility for NZ Superannuation should stay at 65.',
  'NZ Super is paid to everyone 65+ regardless of income. ACT proposes 67 by 2035; National supports raising it eventually but its 2026 policy is cross-party talks.', {
  'labour': P(2, '"Labour has been clear that it will not means test New Zealand superannuation or increase the age of eligibility."', GREY.format('Labour')),
  'green': P(2, '"Yes. We will retain NZ Superannuation as a universal entitlement from age 65."', GREY.format('Green')),
  'nz-first': P(2, '"New Zealand First will not support changes to the entitlement or eligibility of New Zealand Superannuation."', GREY.format('NZ-First')),
  'opportunity': P(2, 'Answered "Yes" to retaining the eligibility age at 65 (Grey Power survey).', GREY.format('Opportunity')),
  'alliance': P(2, '"Keeps the age of entitlement for Super at 65."', ALLIANCE.format('alliance-retirement-aged-care-kiwisaver-policy')),
  'act': P(-2, 'Raise the retirement age to 67 by 2035 (three months a year).', None, 'POL55275'),
  'national': P(-1, 'Would "have liked to make change" and has long backed 67 from a future date, but its 2026 election policy is only to hold cross-party accord talks on the retirement system.', RNZ_SUPER),
})

# =========================================================================== WELFARE
S('q34', 'welfare', 'Main benefits should be substantially increased.',
  'Benefits were indexed to wages from 2023, then changed back to inflation indexation by the current government.', {
  'green': P(2, 'Increase benefit payments and improve standards for beneficiaries.', None, 'POL55132'),
  'alliance': P(2, 'Proposes a Universal Benefit, individual entitlements, universal child payments and an end to benefit sanctions.', ALLIANCE.format('alliance-plan-to-rebuild-universal-social-security')),
  'womens-rights': P(2, '"Minimum wages and benefits need to be increased so that all people have living incomes."', WRP),
  'te-tai-tokerau-party': P(2, 'Replace the "complex, punitive benefit system" with a non-taxable Universal Whānau Allowance and wipe MSD/IRD debt for low-income whānau.', TTT),
  'opportunity': P(1, 'A universal Citizens\' Income of up to $370 a week, replacing many main benefits.', None, 'POL54816'),
  'act': P(-1, 'ACT\'s 2026 Fiscal Plan has no benefit increases; it tightens eligibility (independent medical certification for health and disability benefits, a five-year stand-down for new residents).', 'doc:act/pdf-act-2026-fiscal-plan.md', 'POL54864'),
  'national': P(-1, 'Reduce benefit payments for people receiving support for more than two years.', None, 'POL55227'),
})

S('q35', 'welfare', 'Beneficiaries should face tougher obligations and sanctions, such as drug tests or payment cuts.',
  'The government introduced a traffic-light sanctions system in 2025. National proposes drug testing and cuts after two years on a benefit.', {
  'national': P(2, 'Introduce drug testing for people receiving benefits; reduce payments after two years on a benefit; longer stand-downs.', None, 'POL55228'),
  'act': P(2, 'Restrict medical certification for health-related benefits and monitor spending of long-term jobseekers.', None, 'POL54866'),
  'green': P(-2, 'Increase benefit payments and improve standards for beneficiaries; refuse to use AI for welfare decisions.', None, 'POL55132'),
  'alliance': P(-2, '"An end to benefit sanctions."', ALLIANCE.format('alliance-plan-to-rebuild-universal-social-security')),
  'te-tai-tokerau-party': P(-2, 'Replace the "punitive benefit system" and end "relationship status" policing.', TTT),
  'vision-nz': P(1, '"Dismantle state dependency"; "Slash state dependency by eliminating financial rules that disincentivise marriage."', VISION),
  'conservative': P(1, '"Welfare: Reform is needed. Fifty years of expanding welfare has undermined our families and created an underclass."', 'https://www.conservatives.nz/policy'),
})

# =========================================================================== TRANSPORT / INFRASTRUCTURE
S('q36', 'transport', 'Transport money should go mainly to public transport and rail rather than new highways.',
  'The government\'s priority is "Roads of National Significance"; others favour rapid transit, rail and cheaper fares.', {
  'green': P(2, 'Build mass rapid transit in three major cities and invest in better rail and bus links; free or $2 fares.', None, 'POL55030'),
  'opportunity': P(2, 'Make public transport free.', None, 'POL54786'),
  'alliance': P(2, 'Publicly owned rail and coastal shipping as "twin backbones" of freight, more public-transport funding.', ALLIANCE.format('alliance-national-transport-strategy')),
  'labour': P(1, 'Introduce a $20 weekly public-transport fare cap in the main cities ($10 elsewhere).', None, 'POL54685'),
  'nz-first': P(1, 'Establish a 12-month trial of commuter rail in Canterbury and further south.', None, 'POL55310'),
  'national': P(-2, 'Complete construction of the next set of Roads of National Significance; fund the $800m Christchurch Northern Motorway extension.', None, 'POL55177'),
  'act': P(-2, 'Focus the National Land Transport Fund on road infrastructure only.', None, 'POL54974'),
})

# =========================================================================== AGRICULTURE
S('q37', 'agriculture', 'Rules limiting farm pollution of rivers (such as nitrogen limits) should be strengthened rather than loosened.',
  'The government has loosened some freshwater rules (e.g. Te Mana o te Wai, intensification limits) and is rewriting the RMA.', {
  'green': P(2, 'Impose nitrogen caps on all agricultural practices; phase out synthetic nitrogen fertiliser.', None, 'POL54906'),
  'te-pati-maori': P(2, 'Answered "Yes" to immediately lowering the synthetic nitrogen fertiliser cap and banning new dairy conversions (Greenpeace survey).', GPEACE),
  'opportunity': P(1, 'Tighten rules on water quality and reinstate Te Mana o te Wai, but did not back a lower fertiliser cap.', None, 'POL54797'),
  'labour': P(1, 'Says "freshwater limits should be national bottom lines" and wants councils able to implement the 2020 freshwater policy, but would not commit to lowering the nitrogen cap.', GPEACE),
  'national': P(-2, 'Supported blocking regional freshwater plans and let restrictions on intensification lapse (Greenpeace assessment).', GPEACE),
  'act': P(-2, 'Replace Te Mana o te Wai with measurable freshwater outcomes.', None, 'POL55193'),
  'nz-first': P(-2, '"No. Our approach is for practical, science-based freshwater management that balances environmental outcomes with productive land use."', GPEACE),
  'animal-justice': P(1, 'Links intensive dairying to "degradation of waterways"; seeks to transition away from animal agriculture.', 'doc:animal-justice/policy-ajp-animal-policies.md'),
})

S('q38', 'agriculture', 'Rules on gene technology (genetic modification) should be relaxed.',
  'The Gene Technology Bill would end the effective ban on GM outside the lab; it stalled in 2025–26 after NZ First withheld support.', {
  'national': P(2, 'Introduced the Gene Technology Bill and remains in favour.', GENETECH_AG),
  'act': P(2, 'Supports the Gene Technology Bill (with objections to its Māori advisory committee).', GENETECH_AG),
  'opportunity': P(2, 'Rewrite gene technology regulations to enable modern gene technologies.', None, 'POL54842'),
  'nz-first': P(-1, 'Would not support the Bill into law without major changes, calling it "far too liberal" and lacking safeguards.', GENETECH_NZF),
  'labour': P(-1, 'Withheld support at select committee citing limited consultation and lack of regulatory independence.', GENETECH_AG),
  'green': P(-2, 'Withheld support for the Gene Technology Bill at select committee.', GENETECH_AG),
  'te-pati-maori': P(-2, 'Withheld support for the Gene Technology Bill at select committee.', GENETECH_AG),
  'conservative': P(-2, '"We oppose the current government\'s move to end the long-standing restrictions placed on field trials and the release of genetically modified organisms."', CONS.format('agriculture')),
})

# =========================================================================== FOREIGN POLICY / DEFENCE
S('q39', 'foreign-policy', 'New Zealand should formally recognise the State of Palestine now.',
  'In September 2025 the government decided not to recognise Palestine "yet", unlike the UK, Canada and Australia.', {
  'labour': P(2, '"Labour will recognise the State of Palestine" and place economic sanctions on Israel.', 'doc:labour/foreign-affairs.md', 'POL55131'),
  'green': P(2, 'Recognise Palestine as a state and sanction Israel.', None, 'POL55113'),
  'free-palestine': P(2, 'Party exists to press NZ to "uphold its obligations under international law with respect to Palestine"; seeks a single democratic state.', PALFREE),
  'alliance': P(2, '"We must demand self-determination for Palestinians and the right to return to their homeland."', ALLIANCE.format('alliance-foreign-affairs-defence-international-relations-policy')),
  'national': P(-1, 'Government (PM Luxon, Foreign Minister Peters) decided in Sept 2025 not to recognise Palestine "yet", calling recognition inevitable but premature while Hamas remains.', PALESTINE_2025),
  'nz-first': P(-1, 'Winston Peters announced at the UN in Sept 2025: "we do not think that time is now."', PALESTINE_2025),
})

S('q40', 'defence', 'Defence spending should rise substantially, towards 2% of GDP.',
  'The 2025 Defence Capability Plan aims to lift defence spending from about 1% to 2% of GDP by the early 2030s.', {
  'national': P(2, 'National-led government\'s Defence Capability Plan targets 2% of GDP by 2032/33; Defence Minister Chris Penk reaffirmed "a smooth and steady upward trajectory to 2 percent" in May 2026.', 'https://newswire.co.nz/2026/05/chris-penk-defence-spending-2-percent-gdp-2033/'),
  'act': P(2, 'ACT\'s fiscal plan protects all spending growth in defence while cutting elsewhere, and ACT has called for a "real" pathway to 2% of GDP.', 'https://www.act.org.nz/real_change_to_take_defence_seriously'),
  'te-pati-maori': P(-2, 'Declare NZ a "military neutral" country and focus the Defence Force on protection, disaster response and the Pacific.', None, 'POL54684'),
  'green': P(-1, 'Security policy prioritises peacekeeping and "prevention over military force" and would withdraw NZ from the Five Eyes network; no increase in military spending proposed.', 'doc:green/security-defence-policy-2011-2026.md', 'POL55114'),
  'alliance': P(-2, 'A "peace-focused defence force", non-alignment and an end to intelligence sharing with the US.', ALLIANCE.format('alliance-foreign-affairs-defence-international-relations-policy')),
  'free-palestine': P(-1, 'NZ should withdraw "from any formal security alliances with the U.S." and distance itself from "military interventionism".', PALFREE),
})

S('q41', 'foreign-policy', 'New Zealand should increase its overseas aid budget.',
  'NZ spends about 0.25–0.3% of national income on aid; the UN target is 0.7%.', {
  'labour': P(2, 'Increase foreign aid to 0.7 percent of GDP.', None, 'POL55129'),
  'green': P(2, 'Increase climate aid funding to the Pacific.', None, 'POL55034'),
  'act': P(-2, 'Reduce NZ\'s foreign aid to 2017 levels.', None, 'POL55266'),
  'alliance': P(1, 'Developed nations should cancel Global South debts "as a form of reparation".', ALLIANCE.format('alliance-foreign-affairs-defence-international-relations-policy')),
})

# =========================================================================== DRUGS
S('q42', 'drugs', 'Cannabis should be legalised or decriminalised for personal use.',
  'A 2020 referendum on legal cannabis narrowly failed (48.4% yes). Medicinal cannabis is legal on prescription.', {
  'green': P(2, 'Decriminalise cannabis for personal use; long-term policy is a legal, regulated cannabis market.', None, 'POL55117'),
  'opportunity': P(2, 'Decriminalise drug possession (but not supply).', None, 'POL54855'),
  'legalise-cannabis': P(2, '"That the possession, cultivation and use of pure cannabis... be free from prosecution" and a regulated R18 cannabis market.', ALCP),
  'nz-outdoors-freedom': P(1, 'Supports medicinal use of cannabis for humans, pets and livestock (full legalisation not stated).', NZOFP.format('cannabis-policy')),
})

# =========================================================================== SOCIAL ISSUES
S('q43', 'social-issues', 'Children under 16 should be banned from social media.',
  'National\'s Online Safety bill would make platforms take reasonable steps to keep under-16s off; ACT and NZ First oppose it.', {
  'national': P(2, 'Ban under-16 year olds from social media (Online Safety (Minimum Age...) Bill).', None, 'POL54815'),
  'labour': P(1, 'Backed the bill to pass its first reading and go to select committee, wanting it "substantially improved".', SOCIAL_MEDIA_LAB, 'POL54753'),
  'opportunity': P(1, 'Support the online safety bill on an under-16 ban going to select committee.', None, 'POL54783'),
  'act': P(-2, 'Will vote against: "The ban they propose won\'t work, and the side effects will leave us worse off" (David Seymour).', SOCIAL_MEDIA),
  'nz-first': P(-2, 'Winston Peters said NZ First would "never support this", citing a slippery slope.', SOCIAL_MEDIA),
})

S('q44', 'social-issues', 'Puberty blockers and other medical gender-transition treatments should not be available to under-18s.',
  'In December 2025 the government stopped new prescriptions of puberty blockers for gender dysphoria, following the UK.', {
  'national': P(2, 'Health Minister Simeon Brown halted new puberty-blocker prescriptions for gender dysphoria from 19 Dec 2025 as a "precautionary approach".', PUBERTY),
  'nz-first': P(2, 'Campaigned for the ban and announced it ahead of the Ministry; Peters: "we never stopped fighting to make this happen."', PUBERTY),
  'womens-rights': P(2, 'Supports the puberty-blocker ban and would extend it to cross-sex hormones for under-18s and surgery for under-25s.', WRP),
  'vision-nz': P(2, '"Prohibit all medical interventions for gender transition in minors."', VISION),
  'conservative': P(1, 'Restrict irreversible procedures to alter a child\'s sex characteristics "where there is no clear medical necessity" and require independent assessment.', CONS.format('child-protection')),
  'green': P(-2, 'Free access to gender-affirming health care "including reversal of the ban on puberty blockers".', 'doc:green/web-manifesto-2026-rainbow-communities.md', 'POL55010'),
})

S('q45', 'social-issues', 'Abortion law should be made more restrictive.',
  'Abortion was decriminalised in 2020 (conscience vote). Most parties treat it as a conscience issue and have no party position.', {
  'conservative': P(2, 'Introduce an Unborn Child (Legal Personhood and Rights) Act recognising an unborn child as a legal person from the third trimester (28 weeks).', CONS.format('right-to-life')),
  'vision-nz': P(1, 'Healthcare policy commits to "protecting the sanctity of human life" (no specific abortion law change stated).', VISION),
  'womens-rights': P(-2, 'Lists "the right to have control of our own bodies, including reproductive autonomy" among the rights it exists to protect.', 'https://womensrightsparty.nz/our-priorities/'),
})
