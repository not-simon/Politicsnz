#!/usr/bin/env python3
"""Hand-coded party answers to the compass items ("the party takes the test").

Each cell is C(position, evidence, source_url, confidence):
  position   -2 strongly disagree / very negative .. +2 strongly agree / very positive, relative to the item TEXT
             (the direction key is applied later by compass_build.py; never pre-flip here).
  evidence   short quote or close paraphrase from the cited source, dated where the source is older than 2025.
  source_url the document, Hansard-based record (via Wikipedia vote tallies), survey answer or news report.
  confidence 'high'  = explicit policy, vote or leader statement on the substance of the item;
             'medium'= clear position that requires a small inferential step (e.g. a budget rule -> fiscal responsibility);
             'low'   = indirect or dated evidence, or a position that mixes signals.
Absence = no public evidence found; written as null and NOT counted (never guessed).

Rules: coded from (1) 2026 policy documents archived under parties/<slug>/policies/, (2) recorded votes
(conscience votes attributed to a party only when the whole caucus or a clear majority voted one way),
(3) on-record statements by the leader or MPs. Items of pure private morality (premarital sex, defying
authority) are left null for every party because no party takes a public stance on them.
Build with:  python3 -I tools/compass_build.py
"""

def C(position, evidence, source_url, confidence='medium'):
    return {'position': position, 'evidence': evidence, 'source_url': source_url, 'confidence': confidence}

# ---- frequently cited sources ----------------------------------------------
NAT_LUXON_JUNE = 'https://www.national.org.nz/news/20260621-rthonchristopherluxon'
NAT_LUXON_SEPT = 'https://www.national.org.nz/news/260927-christopherluxon'
NAT_UPSTON = 'https://www.national.org.nz/news/261008-louiseupston'
NAT_GROCERY = 'https://assets.national.org.nz/web/prod/More%20Grocery%20Competition.pdf?v=1789522994'
NAT_HUNTING = 'https://assets.national.org.nz/web/prod/National%27s%20Plan%20for%20Hunting%20and%20Fishing.pdf?v=1785105126'
NAT_WELFARE = 'https://assets.national.org.nz/web/prod/A%20firm,%20fair%20and%20affordable%20welfare%20system.pdf?v=1791407915'
NAT_ECON = 'https://assets.national.org.nz/web/prod/National%27s%20Economic%20Plan.pdf?v=1790557287'
NAT_WILLIS_SURPLUS = 'https://www.national.org.nz/news/20260809-honnicolawillis'
NAT_PENK_DEFENCE = 'https://newswire.co.nz/2026/05/chris-penk-defence-spending-2-percent-gdp-2033/'
NAT_INVESTOR = 'https://assets.national.org.nz/web/prod/National%27s%20Economic%20Plan.pdf?v=1790557287'

ACT_FISCAL = 'https://balancethebooks.nz/'
ACT_FISCAL_PDF = 'https://assets.nationbuilder.com/actnz/pages/38747/attachments/original/1791599898/ACT_2026_Fiscal_Plan.pdf?1791599898'
ACT_AFFORDABLE_GOVT = 'https://www.act.org.nz/affordable-government'
ACT_ONE_LAW_PDF = 'https://assets.nationbuilder.com/actnz/pages/36437/attachments/original/1787277161/One_Law_for_All_policy_06.pdf?1787277161'
ACT_ONE_LAW = 'https://www.act.org.nz/one-law-for-all'
ACT_WELFARE = 'https://www.act.org.nz/news/act-announces-policy-to-make-benefits-a-hand-up-not-a-way-of-life'
ACT_FARMING = 'https://www.act.org.nz/news/act-will-make-farming-fun-again'
ACT_SUPERMARKET = 'https://www.act.org.nz/news/act%E2%80%99s-plan-to-increase-supermarket-competition'
ACT_BURGLARY = 'https://www.act.org.nz/burglary'
ACT_DEPORT = 'https://www.act.org.nz/deport'
ACT_IMMIGRATION_SCOOP = 'https://www.scoop.co.nz/stories/PA2609/S00003/acts-new-immigration-policy-to-put-reside-back-in-resident.htm'
ACT_POWER = 'https://assets.nationbuilder.com/actnz/pages/37361/attachments/original/1789601230/Stability__investment__affordability.pdf?1789601230'
ACT_PUBLIC_SERVICE = 'https://assets.nationbuilder.com/actnz/mailings/59226/attachments/original/PublicService_policy_03.pdf?1786679526'

LAB_FISCAL = 'https://www.labour.org.nz/fiscal-strategy'
LAB_FUTUREFUND = 'https://www.labour.org.nz/futurefund'
LAB_FUTUREFUND_PDF = 'https://www.labour.org.nz/media/vbyf0pxe/the-new-zealand-future-fund.pdf'
LAB_TRUST = 'https://www.labour.org.nz/government-you-can-trust'
LAB_GOUGING = 'https://www.labour.org.nz/banning-price-gouging'
LAB_RAINBOW = 'https://www.labour.org.nz/news/release-labour-to-deliver-stronger-healthcare-and-protections-for-rainbow-communities/'
LAB_CGT = 'https://www.labour.org.nz/capitalgainstax'
LAB_SMALLBIZ = 'https://www.labour.org.nz/small-business-first'
LAB_IMMIGRATION = 'https://www.labour.org.nz/immigration'
LAB_BOOTCAMPS = 'https://www.labour.org.nz/news/'
LAB_AUKUS = 'https://www.labour.org.nz/news/release-a-labour-government-will-not-join-aukus/'
LAB_HIPKINS_DEFENCE = 'https://www.1news.co.nz/2026/06/02/hipkins-says-new-policy-coming-soon-labour-still-working-through-budget/'

GRN_INCOME = 'https://www.greens.org.nz/manifesto_2026_income'
GRN_WEALTH = 'https://www.greens.org.nz/manifesto_2026_tax'
GRN_PUBLIC = 'https://www.greens.org.nz/manifesto_2026_public_services'
GRN_FOOD = 'https://assets.nationbuilder.com/beachheroes/pages/89620/attachments/original/1788650611/AFFORDABLE_FOOD_FOR_ALL_OF_US_POLICY_FINAL.pdf?1788650611'
GRN_ECON_POLICY = 'https://assets.nationbuilder.com/beachheroes/pages/64724/attachments/original/1778624605/Policy-Greens_Government_Economy_Policy_2024-2026.pdf'
GRN_JUSTICE = 'https://www.greens.org.nz/manifesto_2026_justice_and_community_safety'
GRN_JUSTICE_POLICY = 'https://assets.nationbuilder.com/beachheroes/pages/64794/attachments/original/1781652265/Policy-Greens_Justice_Policy_2025-2026.pdf?1781652265'
GRN_WOMEN = 'https://assets.nationbuilder.com/beachheroes/pages/65060/attachments/original/1779238542/Policy-Greens_Womens_Policy_2025-2026.pdf?1779238542'
GRN_BUSINESS = 'https://assets.nationbuilder.com/beachheroes/pages/64528/attachments/original/1781650904/Policy-Greens_Business_Policy_2025-2026.pdf?1781650904'
GRN_RAINBOW = 'https://www.greens.org.nz/manifesto_2026_rainbow_communities'
GRN_IMMIGRATION = 'https://www.greens.org.nz/manifesto_2026_immigration_and_refugees'
GRN_DEMOCRACY = 'https://www.greens.org.nz/manifesto_2026_democracy'
GRN_SECURITY = 'https://assets.nationbuilder.com/beachheroes/pages/64948/attachments/original/1778624615/Policy-Greens_Security_Defence_Policy_2011-2026.pdf'
GRN_CORPTAX = 'https://www.greens.org.nz/manifesto_2026_tax'
GRN_LOBBY = 'https://www.greens.org.nz/manifesto_2026_democracy'

NZF_SOTN = 'https://www.scoop.co.nz/stories/PA2603/S00137/winston-peters-state-of-the-nation-2026-power-to-the-people.htm'
NZF_DEEDS = 'https://www.scoop.co.nz/stories/PA2605/S00140/winston-peters-speech-by-their-deeds-you-will-know-them.htm'
NZF_ANIMAL_FARM = 'https://www.scoop.co.nz/stories/PA2608/S00133/winston-peters-speech-the-labour-green-maori-opportunity-antipodean-animal-farm.htm'
NZF_HOPE = 'https://www.scoop.co.nz/stories/PA2606/S00103/winston-peters-speech-keep-hope-alive.htm'
NZF_TOMORROW = 'https://www.scoop.co.nz/stories/PA2607/S00134/hope-and-a-better-tomorrow.htm'
NZF_REFERENDUM = 'https://www.scoop.co.nz/stories/PA2602/S00071/new-zealand-first-to-campaign-for-referendum-on-maori-seats.htm'
NZF_ELEVENTH = 'https://www.scoop.co.nz/stories/PA2608/S00010/winston-peters-speech-new-zealand-in-its-eleventh-hour.htm'
NZF_SUPERMARKET = 'https://www.nzfirst.nz/break_up_the_supermarket_duopoly'
NZF_SENTENCING = 'https://www.nzfirst.nz/'
NZF_IMMIGRATION = 'https://www.nzfirst.nz/nz_first_announces_immigration_reform_policies'
NZF_SMALLBIZ = 'https://www.nzfirst.nz/'
WIKI_NZF = 'https://en.wikipedia.org/wiki/New_Zealand_First'

TPM_TAX = 'https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf'
TPM_PRISONS = 'https://www.scoop.co.nz/stories/PA2601/S00112/if-youre-not-trying-to-abolish-prisons-in-aotearoa-what-are-you-doing-in-parliament-rawiri-waititi.htm'
TPM_SEATS = 'https://www.scoop.co.nz/stories/PA2602/S00082/maori-seats-are-constitutional-not-conditional.htm'
TPM_TAKATAPUI = 'https://drive.google.com/file/d/1qyqzCxGrLF067Q2S5ZafwQ1F_UDOpPj0/view'
TPM_MP_PAY = 'https://www.scoop.co.nz/stories/PA2604/S00015/te-pati-maori-calls-for-freeze-on-mp-pay-rises.htm'
TPM_WATER = 'https://drive.google.com/file/d/1LPTzVr2sdxSNdfLF2DFLikHqr2zaeuBP/view'
TPM_PEACE = 'https://www.scoop.co.nz/stories/PA2603/S00004/te-pati-maori-statement-aotearoa-must-stand-for-peace.htm'
TPM_MILITARY = 'https://www.maoriparty.org.nz/military_neutrality'
TPM_SANCTIONS = 'https://scoop.co.nz/stories/PA202410/S00184.htm'
TPM_KAI = 'https://www.maoriparty.org.nz/kai_sovereignt'

OPP_TAX = 'https://cdn.opportunity.org.nz/documents/policy/Opportunity%20Policy%20-%20Tax%20Reset.pdf'
OPP_LEFTRIGHT = 'https://www.opportunity.org.nz/_left_right_politics_is_failing_new_zealand'
OPP_CLEAN = 'https://cdn.opportunity.org.nz/documents/policy/Opportunity%20Policy%20-%20Clean%20Up%20Politics.pdf'
OPP_VOICE = 'https://cdn.opportunity.org.nz/documents/policy/citizens-voice-policy.pdf'
OPP_INFRA = 'https://cdn.opportunity.org.nz/documents/policy/Opportunity%20Policy%20-%20Intergenerational%20Infrastructure.pdf'
OPP_SOTN = 'https://www.opportunity.org.nz/the-state-of-the-nation'
OPP_ECONOMY = 'https://cdn.opportunity.org.nz/documents/policy/breakthrough-economy-policy-overview.pdf'
OPP_CRIME = 'https://cdn.opportunity.org.nz/documents/policy/Opportunity%20Policy%20-%20Smart%20on%20Crime.pdf'
OPP_COMPETITION = 'https://www.opportunity.org.nz/'

ALL_STAND = 'https://allianceparty.nz/what-we-stand-for/'
ALL_JUSTICE = 'https://allianceparty.nz/wp-content/uploads/2026/09/alliance-justice-policy-2026.pdf'
ALL_DEMOCRACY = 'https://allianceparty.nz/wp-content/uploads/2026/09/alliance-te-tiriti-democracy-constitutional-policy-2026.pdf'
ALL_FOREIGN = 'https://allianceparty.nz/wp-content/uploads/2026/10/alliance-foreign-affairs-defence-international-relations-policy-2026.pdf'
ALL_WOMEN = 'https://allianceparty.nz/wp-content/uploads/2026/09/alliance-women-gender-equality-economic-security-policy-2026.pdf'
ALL_HOUSING = 'https://allianceparty.nz/wp-content/uploads/2026/09/alliance-housing-policy-2026.pdf'
ALL_TAXCOST = 'https://allianceparty.nz/wp-content/uploads/2026/09/alliance-tax-policy-costings-2026.pdf'
ALL_CHILD = 'https://allianceparty.nz/wp-content/uploads/2026/09/alliance-universal-child-benefit-and-child-poverty-policy-2026.pdf'
ALL_ENERGY = 'https://allianceparty.nz/wp-content/uploads/2026/09/alliance-environment-climate-sustainable-economy-policy-2026.pdf'
ALL_SMALLBIZ = 'https://allianceparty.nz/wp-content/uploads/2026/09/alliance-small-business-local-enterprise-cooperative-policy-2026.pdf'

CON_OVERVIEW = 'https://conservatives.org.nz/policies/overview/'
CON_PRINCIPLES = 'https://www.conservatives.nz/principles'
CON_POLICY = 'https://www.conservatives.nz/policy'
CON_AG = 'https://conservatives.org.nz/policies/agriculture/'
CON_ECON = 'https://conservatives.org.nz/policies/economy-1/'
CON_NEWPOL = 'https://www.conservatives.nz/news/new-policies-announcement'
CON_IMMIG = 'https://conservatives.org.nz/policies/immigration/'
CON_STAND = 'https://www.conservatives.nz/we-stand-for'
CON_LIFE = 'https://conservatives.org.nz/policies/right-to-life/'
CON_BUREAU = 'https://conservatives.org.nz/policies/bureaucracy/'
WIKI_CON = 'https://en.wikipedia.org/wiki/Conservative_Party_of_New_Zealand'

VIS = 'https://www.vision.org.nz/visionpolicies'
WIKI_VIS = 'https://en.wikipedia.org/wiki/Vision_NZ'
OFP_DD = 'https://freedom.kiwi/direct-democracy'
OFP_FISH = 'https://freedom.kiwi/nzofp-fisheries-policy'
OFP_CONDUCT = 'https://freedom.kiwi/anti-bullying-policy'
OFP_ACC = 'https://freedom.kiwi/the-acc-justice-accountability-policy-statement'
OFP_CANNABIS = 'https://freedom.kiwi/cannabis-policy'
LOYAL_RNZ = 'https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election'
WIKI_LOYAL = 'https://en.wikipedia.org/wiki/New_Zealand_Loyal'
WRP_FULL = 'https://womensrightsparty.nz/wp-content/uploads/2025/11/POLICY-Womens-Rights-Party-2025-041125.docx'
WRP_POLICY = 'https://womensrightsparty.nz/policy/'
WRP_PRIORITIES = 'https://womensrightsparty.nz/our-priorities/'
TTP = 'https://tetaitokerauparty.org.nz/our-policies/'
AJP_PEOPLE = 'https://animaljustice.org.nz/policies/ajp-people-policies-pack/'
ALCP = 'https://www.alcp.org.nz/policy'
FPP = 'https://palfree.nz/'

WIKI_ABORTION = 'https://en.wikipedia.org/wiki/Abortion_Legislation_Act_2020'
WIKI_MARRIAGE = 'https://en.wikipedia.org/wiki/Marriage_(Definition_of_Marriage)_Amendment_Act_2013'
WIKI_CONVERSION = 'https://en.wikipedia.org/wiki/Conversion_Practices_Prohibition_Legislation_Act_2022'
WIKI_THREESTRIKES = 'https://en.wikipedia.org/wiki/Sentencing_(Reinstating_Three_Strikes)_Amendment_Act_2024'
WIKI_TPB = 'https://en.wikipedia.org/wiki/Treaty_Principles_Bill'
WIKI_NATIONAL = 'https://en.wikipedia.org/wiki/New_Zealand_National_Party'
WIKI_SIXTH_LABOUR = 'https://en.wikipedia.org/wiki/Sixth_Labour_Government_of_New_Zealand'

CODING = {}

def S(item_id, **cells):
    CODING[item_id] = cells

# ================================================================= ECONOMIC
S('econ_wvs_incomes',
  green=C(2, 'A wealth tax on net wealth over $10m "can reduce income inequality and ensure everyone has enough to live"; "multi-millionaires pay $9 in tax for every $100 ... teachers pay $22".', GRN_WEALTH, 'high'),
  te_pati_maori=C(2, '"wealth inequality is currently extremely high. Tax reform is required to address wealth inequality" (1.5-2.5% net wealth tax).', TPM_TAX, 'high'),
  alliance=C(2, '"We want to create a more equal, fair, and democratic society"; "make the wealthy who earn their income from assets pay their fair share".', ALL_STAND, 'high'),
  labour=C(1, 'Future Fund paper: "Our system has been designed to justify inequalities of wealth and income"; CGT so "those profiting from property pay their fair share".', LAB_FUTUREFUND_PDF, 'medium'),
  opportunity=C(1, 'Cites "widening inequality"; land tax plus Citizens\' Income would "significantly decrease poverty", while rejecting the "socialist redistribution" label.', OPP_TAX, 'medium'),
  womens_rights=C(1, '"social and economic inequality and poverty, are of particular concern"; "benefits need to be increased so that all people have living incomes".', WRP_POLICY, 'medium'),
  te_tai_tokerau_party=C(1, 'Universal Whānau Allowance, amnesty on whānau debt to MSD/IRD; describes "persistent economic extraction" from the North.', TTP, 'medium'),
  animal_justice=C(1, 'Policies address "economic inequality that traps people in exploitative industries".', AJP_PEOPLE, 'low'),
  act=C(-1, 'Fiscal plan aims at "much lower, flatter taxes"; no capital gains tax; opposes wealth taxes.', ACT_FISCAL, 'medium'),
  national=C(-1, '"Reward for achievement" is a stated party value; "No new taxes, including no capital gains tax".', NAT_ECON, 'medium'),
  nz_first=C(0, 'Peters lists "Egalitarianism" among NZ First\'s values, but attacks Opportunity\'s "redistribution of wealth and bludging tax policy".', NZF_SOTN, 'low'),
  conservative=C(-1, 'Calls for a flat tax rate: "The New Zealand citizen can spend their money far better than the government can."', CON_ECON, 'low'),
)
S('econ_wvs_ownership',
  alliance=C(-2, '"returning to public ownership and control of key national and local assets"; a "reverse privatisation" programme for electricity, ports, water, telecommunications, Air NZ.', ALL_STAND, 'high'),
  green=C(-2, 'Public services and SOEs "continue to be owned by the government"; a publicly owned KiwiMart and "Kiwipower".', GRN_PUBLIC, 'high'),
  nz_first=C(-2, '"we own our country\'s assets"; "No government with New Zealand First will be selling our assets"; buy back BNZ.', NZF_SOTN, 'high'),
  labour=C(-1, 'Future Fund: seeded assets "cannot be sold and will remain in public ownership for generations"; "Instead of selling off our assets ...".', LAB_FUTUREFUND, 'high'),
  te_pati_maori=C(-1, '"Reject privatisation and trading of water rights"; increase Māori and community ownership of energy.', TPM_WATER, 'medium'),
  nz_loyal=C(-2, 'Platform includes nationalisation of key infrastructure (communications, transport, water, energy grid).', WIKI_LOYAL, 'medium'),
  nz_outdoors_freedom=C(-1, 'Says the Quota Management System "privatised the once public fishery"; keep fisheries in public ownership (but also wants smaller government).', OFP_FISH, 'low'),
  te_tai_tokerau_party=C(-1, 'Māori-governed land buy-back fund; community-owned food hubs.', TTP, 'low'),
  act=C(1, 'Open power transmission to private investment; opposes break-ups and state-run alternatives; public-private partnerships for cancer centres.', ACT_POWER, 'medium'),
)
S('econ_wvs_responsibility',
  green=C(2, '"Everyone deserves support through hard times, not blame and punishment"; increase benefits to liveable rates.', GRN_INCOME, 'high'),
  alliance=C(2, 'A Universal Benefit and "a strong and comprehensive welfare state".', ALL_CHILD, 'high'),
  te_pati_maori=C(2, '"ensure everybody is paid enough to live with dignity, whether they are in employment or not" (Oct 2024).', TPM_SANCTIONS, 'high'),
  opportunity=C(2, 'Universal Citizens\' Income: "Give every adult the basics to live well".', OPP_TAX, 'high'),
  te_tai_tokerau_party=C(2, 'Replace the benefit system with a non-taxable Universal Whānau Allowance.', TTP, 'medium'),
  labour=C(1, 'Free GP visits (Medicard), 6,000 more social housing places, fare caps: an expanded state role in provision.', LAB_GOUGING, 'medium'),
  womens_rights=C(1, '"Minimum wages and benefits need to be increased so that all people have living incomes."', WRP_POLICY, 'medium'),
  act=C(-2, '"Welfare should unlock potential, not trap it"; restore "personal responsibility, and the value of work"; five-year benefit stand-down for new residents.', ACT_WELFARE, 'high'),
  national=C(-1, '"those who can work should work ... Our welfare system provides a safety net when people need it, but it must be fair and affordable"; "Personal responsibility" is a party value.', NAT_UPSTON, 'high'),
  conservative=C(-2, 'Government "should strengthen families rather than create long-term dependency"; "Encourage self-reliance".', CON_OVERVIEW, 'high'),
  vision_nz=C(-1, '"dismantle state dependency, strip away government over-reach", but also a universal payment for families with a child under one.', VIS, 'medium'),
  nz_first=C(0, 'Mixed: "targeted government intervention ... a hand up in times of need" versus calling a universal basic income "communism" and listing "personal responsibility" as a kiwi value.', NZF_SOTN, 'medium'),
  nz_outdoors_freedom=C(-1, 'Swiss-style subsidiarity: "dismantle" the "bloated bureaucracy in Wellington"; smaller central government.', OFP_DD, 'low'),
)
S('econ_wvs_competition',
  act=C(2, '"More competition and ..." is ACT\'s standard remedy; one-stop consenting body to approve competing supermarkets.', ACT_SUPERMARKET, 'high'),
  national=C(2, '"Competitive enterprise" is a party value; "Strong competition is one of the most effective ways to reduce prices, increase innovation, lift productivity".', NAT_GROCERY, 'high'),
  opportunity=C(2, 'Commerce Commission powers "to investigate, intervene and force structural separation of anti-competitive businesses".', OPP_COMPETITION, 'high'),
  labour=C(1, 'Competition scrutiny of fuel, airports and groceries, alongside a price-gouging ban.', LAB_GOUGING, 'medium'),
  nz_first=C(1, 'Break up the supermarket duopoly: "Creating more competition will drive prices down" - but also calls NZ "the victim of a totally unfettered free market".', NZF_SUPERMARKET, 'medium'),
  conservative=C(1, 'Principle: people "free to pursue their legitimate self-interest within a competitive economy".', CON_PRINCIPLES, 'medium'),
  green=C(0, 'Breaks up the duopoly for competition but would re-impose a legal ban on "unreasonably high prices" removed by 1980s deregulation.', GRN_FOOD, 'medium'),
  alliance=C(-1, 'Rejects "the zero-sum assumptions of competition and imperial capital"; natural monopolies in public ownership; supports stronger competition law for small firms.', ALL_FOREIGN, 'low'),
)
S('econ_cses_reduce_differences',
  green=C(2, 'Wealth tax over $10m to "reduce income inequality"; corporate tax to 33% for the largest 0.7% of companies.', GRN_WEALTH, 'high'),
  te_pati_maori=C(2, 'Net wealth tax and 33% company tax to "address wealth inequality ... and fund public services".', TPM_TAX, 'high'),
  alliance=C(2, 'Progressive tax scale to 47% over $250,000, wealth and financial-transactions taxes, to fund free services.', ALL_TAXCOST, 'high'),
  labour=C(1, '28% capital gains tax on investment property with "every dollar raised" going to health.', LAB_CGT, 'medium'),
  opportunity=C(1, 'Land value tax funding a Citizens\' Income that lifts incomes for 70% of households.', OPP_TAX, 'medium'),
  womens_rights=C(1, 'CPAG-style Working for Families reform to "lift the poorest families out of poverty".', WRP_FULL, 'medium'),
  te_tai_tokerau_party=C(1, 'Universal Whānau Allowance and whānau debt amnesty.', TTP, 'medium'),
  animal_justice=C(1, 'Government procurement to require fair wages; concern about "economic inequality".', AJP_PEOPLE, 'low'),
  act=C(-2, 'No capital gains tax; "much lower, flatter taxes, paid for by spending control".', ACT_FISCAL, 'medium'),
  national=C(-1, '"No new taxes, including no capital gains tax."', NAT_ECON, 'medium'),
  nz_first=C(0, '"Egalitarianism" claimed as a value; Opportunity\'s land-tax-funded income called "robbing Peter to pay Paul" and "communism".', NZF_ANIMAL_FARM, 'low'),
  conservative=C(-1, 'Flat tax rate for individuals and companies.', CON_NEWPOL, 'medium'),
)
S('econ_nzes_privatisation',
  alliance=C(2, '"Stop all further privatisation and return ports, water, telecommunications and Air New Zealand to full public ownership."', ALL_ENERGY, 'high'),
  nz_first=C(2, '"Labour and National, went on to sell our assets, privatise our country ... an abject failure and purveyor of misery".', NZF_SOTN, 'high'),
  nz_loyal=C(2, 'Nationalisation of communications, transport, water and energy infrastructure.', WIKI_LOYAL, 'medium'),
  green=C(1, '"restoring public ownership of energy projects would make power more affordable"; keep SOEs in public ownership.', GRN_PUBLIC, 'medium'),
  labour=C(1, 'Future Fund locks assets in public ownership "instead of selling off our assets and opening the gates to foreign investors".', LAB_FUTUREFUND_PDF, 'medium'),
  te_pati_maori=C(1, 'Rejects privatisation and trading of water rights; "Energy that belongs here. Generation we control."', TPM_WATER, 'low'),
  nz_outdoors_freedom=C(1, 'QMS "privatised the once public fishery".', OFP_FISH, 'low'),
  act=C(-1, 'Favours private investment in transmission and public-private partnerships; no concern expressed about past privatisation.', ACT_POWER, 'medium'),
  national=C(-1, 'Carried out the 2011-14 mixed-ownership share floats despite a referendum against them (dated evidence; no 2026 asset-sales policy found).', WIKI_NATIONAL, 'low'),
)
S('econ_nzes_big_business',
  green=C(2, 'Supermarkets "making $1 million a day in excessive profits"; large corporations "profiting from the public without contributing back".', GRN_FOOD, 'high'),
  te_pati_maori=C(2, '"breaking the stranglehold that monopolies have on food supply"; company tax back to 33%.', TPM_KAI, 'high'),
  alliance=C(2, 'Media "captured by big business interests"; "Political power must not be concentrated in the hands of ... multinational corporations, wealthy individuals".', ALL_DEMOCRACY, 'high'),
  te_tai_tokerau_party=C(2, 'Food supply "controlled by an anti-competitive corporate supermarket duopoly" that "extract[s] millions from our local economy".', TTP, 'medium'),
  labour=C(1, '"crack down on big companies who charge excessive prices"; "the big companies can\'t rip you off".', LAB_GOUGING, 'medium'),
  nz_first=C(1, 'Power system "designed to make maximum profits for power companies"; break up the supermarket duopoly; Australian-owned banks.', NZF_SOTN, 'medium'),
  opportunity=C(1, 'Consumers "paying too much because of a lack of market competition in sectors such as the supermarkets and banking".', OPP_COMPETITION, 'medium'),
  animal_justice=C(1, '"democratic deficits that allow wealthy interests to block necessary reforms"; address the supermarket duopoly.', AJP_PEOPLE, 'low'),
  nz_loyal=C(1, 'Opposition to "globalist" institutions including banks (policy.nz description quoted in party README).', LOYAL_RNZ, 'low'),
  nz_outdoors_freedom=C(1, '"Holding Big Pharma Accountable"; strengthen anti-monopoly law.', OFP_ACC, 'low'),
  national=C(0, 'Says "supermarket competition is still too weak" yet "businesses create wealth, not governments".', NAT_GROCERY, 'medium'),
  act=C(-1, 'Criticises "political leadership blame[ing] companies for their prices", which "creates greater bureaucracy".', ACT_SUPERMARKET, 'medium'),
)
S('econ_secs_limited_government',
  act=C(2, '"smaller, more efficient government"; halve the number of ministries; cut non-frontline spending to 2017 levels.', ACT_AFFORDABLE_GOVT, 'high'),
  national=C(2, 'Luxon lists "Limited government" among National\'s founding values (June 2026).', NAT_LUXON_JUNE, 'high'),
  conservative=C(2, '"Reduce the size of government"; policies "built on ... limited government".', CON_AG, 'high'),
  nz_outdoors_freedom=C(2, '"Decentralisation & Smaller Government"; dismantle the "bloated bureaucracy in Wellington".', OFP_DD, 'high'),
  vision_nz=C(1, '"Less Government, More Community"; "cutting the size of government".', VIS, 'medium'),
  nz_loyal=C(1, '"We reject government overreach"; "Decentralise government and return power to the people" (but also nationalisation).', LOYAL_RNZ, 'low'),
  green=C(-2, 'Public Finance Act reform "Avoiding arbitrary limits on government debt and expenditure"; a Ministry for Green Works; state-owned supermarket and power company.', GRN_ECON_POLICY, 'high'),
  alliance=C(-2, '"major state-led intervention"; a new Ministry of Works; public ownership of utilities.', ALL_HOUSING, 'high'),
  te_pati_maori=C(-1, 'Large new state programmes ($2.8b Kai Credit, wealth tax) alongside devolution to iwi and hapū.', TPM_KAI, 'medium'),
  labour=C(-1, 'Future Fund, Medicard and fare caps expand the state\'s role, while promising "not a new layer of bureaucracy".', LAB_FUTUREFUND, 'low'),
  opportunity=C(0, 'Would cut welfare bureaucracy and consenting red tape but add a Citizens\' Income and borrow 15% of GDP for infrastructure.', OPP_INFRA, 'low'),
  nz_first=C(0, '"targeted government intervention" and economic nationalism, alongside attacks on "bureaucracy gone mad".', NZF_SOTN, 'low'),
)
S('econ_secs_welfare_benefits',
  green=C(2, '"Increase benefits to liveable rates, individualise benefit entitlements and abolish benefit sanctions."', GRN_INCOME, 'high'),
  alliance=C(2, 'Universal Benefit; "abolish benefit sanctions, stand-downs and beneficiary debt".', ALL_CHILD, 'high'),
  te_pati_maori=C(2, '"We will scrap benefit sanctions and ensure everybody is paid enough to live with dignity" (Oct 2024).', TPM_SANCTIONS, 'high'),
  womens_rights=C(2, 'Remove "discrimination against beneficiary families"; benefits "need to be increased".', WRP_FULL, 'medium'),
  te_tai_tokerau_party=C(2, 'Replace the "complex, punitive benefit system" with a Universal Whānau Allowance.', TTP, 'medium'),
  opportunity=C(1, 'Replaces most benefits with a Citizens\' Income because the "welfare system traps people in poverty with punitive rules".', OPP_TAX, 'medium'),
  labour=C(1, 'In office: benefit increases and wage indexation (2018-23); opposes National\'s 2026 benefit cuts.', WIKI_SIXTH_LABOUR, 'low'),
  act=C(-2, 'Benefits "a hand-up, not a way of life"; money-management cards after four months; tighter medical certification.', ACT_WELFARE, 'high'),
  national=C(-2, 'Reduce Jobseeker payments after two years; random drug testing; five-year stand-down for new residents.', NAT_WELFARE, 'high'),
  conservative=C(-2, '"Fifty years of expanding welfare has undermined our families and created an underclass."', CON_POLICY, 'high'),
  vision_nz=C(-1, '"Slash state dependency"; but abolish income tax on benefits.', VIS, 'medium'),
  nz_first=C(-1, 'Ten-year benefit stand-down for migrants; UBI called "communism"; defends superannuation.', NZF_IMMIGRATION, 'medium'),
)
S('econ_secs_business',
  act=C(2, '"Small businesses shouldn\'t need a lawyer just to have a difficult conversation"; growth policies built around business.', ACT_FISCAL, 'high'),
  national=C(2, '"businesses create wealth, not governments"; "Competitive enterprise" value.', NAT_GROCERY, 'high'),
  conservative=C(2, 'Lower company tax; "Retention of capital will encourage entrepreneurs".', CON_ECON, 'high'),
  labour=C(1, '"Small Business First" package; "leveling the playing field for Kiwi businesses and innovation".', LAB_SMALLBIZ, 'medium'),
  opportunity=C(1, '25% technology tax credit for SMEs; "Impact Company" structure.', OPP_ECONOMY, 'medium'),
  nz_first=C(1, 'Company tax cut to 20% for firms under $30m turnover; hostile to power companies and Australian banks.', NZF_SOTN, 'medium'),
  te_tai_tokerau_party=C(1, 'Five-year corporate tax exemption for new regional employers.', TTP, 'low'),
  green=C(0, 'Keeps 28% rate for SMEs but 33% for the largest corporates and would "Regulate businesses ... to be socially and environmentally responsible".', GRN_BUSINESS, 'medium'),
  te_pati_maori=C(0, 'Company tax to 33% and a $1b tax-avoidance crackdown, but a quarter of government contracts for Māori businesses.', TPM_TAX, 'medium'),
  alliance=C(0, 'Supports small business and co-operatives with a public development bank, while bringing utilities into public ownership.', ALL_SMALLBIZ, 'low'),
)
S('econ_secs_fiscal_responsibility',
  act=C(2, '"Government has to do its part by living within its means"; surplus in 2028/29 and $12.4b less debt by 2031.', ACT_FISCAL, 'high'),
  national=C(2, 'Return to surplus by 2028/29; keep debt below 40% of GDP; "Economic productivity and fiscal discipline ... are national security".', NAT_WILLIS_SURPLUS, 'high'),
  labour=C(2, '"Labour will balance the books, return to surplus by 2029/30, reduce net debt to 20% of GDP".', LAB_FISCAL, 'high'),
  conservative=C(1, '"careful management of public money"; "tackle public debt".', CON_OVERVIEW, 'medium'),
  nz_first=C(1, 'Attacks the previous government\'s "massive overborrowing"; Labour "will tax more, spend more, and borrow more".', NZF_SOTN, 'medium'),
  opportunity=C(0, 'Would issue "up to an additional 15% of GDP in special infrastructure" bonds, arguing NZ "can borrow carefully".', OPP_INFRA, 'medium'),
  alliance=C(0, 'Tax package "runs a surplus in both periods" but funds a large state-led spending programme.', ALL_TAXCOST, 'low'),
  green=C(-1, '"Enabling greater government borrowing for investing in infrastructure; Avoiding arbitrary limits on government debt and expenditure".', GRN_ECON_POLICY, 'medium'),
)
S('econ_secs_gun_ownership',
  act=C(2, '"restored common sense to firearms laws"; policies to back hunters and make disrupting lawful hunters an offence.', ACT_FARMING, 'high'),
  national=C(1, 'Increase public access to shooting ranges and hunter training; supported the 2019 semi-automatic ban.', NAT_HUNTING, 'medium'),
  green=C(-2, '"continuing to oppose possession of military-style semi-automatic firearms"; robust licensing and registration.', GRN_JUSTICE, 'high'),
  labour=C(-1, 'Led the 2019 semi-automatic firearms ban and registry.', WIKI_SIXTH_LABOUR, 'medium'),
  nz_first=C(-1, 'Supported the 2019 firearms ban in government.', WIKI_NZF, 'low'),
)

# ================================================================= SOCIAL
S('soc_vsa_defy_authority')   # no party takes a public position; all null
S('soc_vsa_discipline',
  nz_outdoors_freedom=C(-2, 'Politicians "will no longer hold the supreme power"; citizens can veto laws.', OFP_DD, 'medium'),
  alliance=C(-1, '"a radically democratic party"; participatory democracy with recall of representatives.', ALL_DEMOCRACY, 'low'),
  opportunity=C(-1, 'Citizens\' assemblies because "Parliament has become gridlocked"; distrust of leader-driven politics.', OPP_VOICE, 'low'),
  nz_loyal=C(-1, '"We reject government overreach ... return power to the people."', LOYAL_RNZ, 'low'),
  vision_nz=C(1, 'Core principle "One Nation, One People, One Vote, One Government, One Flag, Under One God"; schools to "rebuild a shared national identity".', VIS, 'low'),
)
S('soc_vsa_gods_laws',
  vision_nz=C(2, '"Under One God"; "protect the unborn"; "Protect the nuclear family"; remove gender theory and RSE from schools.', VIS, 'high'),
  conservative=C(1, '"We stand by Judeo-Christian Western cultural traditions"; unborn-child personhood; opposed abortion decriminalisation.', CON_POLICY, 'medium'),
  nz_loyal=C(1, 'Teach children "objective morality"; end "corrupt sex and gender education".', WIKI_LOYAL, 'low'),
  green=C(-2, 'Reproductive rights, rainbow and drug-law reform; opposes any religious basis for law.', GRN_WOMEN, 'high'),
  alliance=C(-2, '"Reproductive healthcare is a fundamental health right and must not be treated as a criminal matter."', ALL_WOMEN, 'high'),
  act=C(-2, 'Voted for abortion decriminalisation at every stage (2020) and sponsored the End of Life Choice Act.', WIKI_ABORTION, 'high'),
  labour=C(-1, 'Took abortion out of the Crimes Act in government (2020); Rainbow Pae Ora strategy.', WIKI_ABORTION, 'medium'),
  te_pati_maori=C(-1, 'Calls for "a stop to political, legislative, and religious developments that deny and marginalise Takatāpui".', TPM_TAKATAPUI, 'medium'),
  nz_first=C(0, 'Self-described "only socially conservative party" that voted against same-sex marriage, yet Peters says "the government has no place in the nation\'s bedrooms".', NZF_HOPE, 'low'),
  national=C(0, 'Conscience votes: MPs mostly opposed the Abortion Legislation Act 2020 and split on same-sex marriage.', WIKI_NATIONAL, 'low'),
  womens_rights=C(0, 'Defends "reproductive autonomy" but opposes pornography involving violence and would adopt the Nordic model on prostitution.', WRP_PRIORITIES, 'low'),
)
S('soc_vsa_premarital')       # no party takes a public position; all null
S('soc_vsa_not_tougher',
  green=C(2, 'Prioritise rehabilitation; voted against reinstating three strikes; repeal the Misuse of Drugs Act.', GRN_JUSTICE, 'high'),
  te_pati_maori=C(2, '"Abolish prisons by 2040"; repeal three strikes, gang and bail laws.', TPM_PRISONS, 'high'),
  alliance=C(2, 'High imprisonment "cannot be addressed simply by building more prisons or imposing harsher sentences".', ALL_JUSTICE, 'high'),
  te_tai_tokerau_party=C(2, '"Prison Sinking Lid"; "punitive policing entrench[es] institutional inequity".', TTP, 'medium'),
  labour=C(1, 'Voted against reinstating three strikes; would end youth boot camps; but would "crack down" on price gouging.', WIKI_THREESTRIKES, 'medium'),
  opportunity=C(1, '"Smart on Crime": prevention, rehabilitation; decriminalise drug possession.', OPP_CRIME, 'medium'),
  nz_outdoors_freedom=C(1, 'Citizens\' veto to "kill" unpopular laws; rights that cannot be "voted away by politicians".', OFP_DD, 'low'),
  nz_loyal=C(1, '"We reject government overreach."', LOYAL_RNZ, 'low'),
  legalise_cannabis=C(0, '"Education not incarceration" for cannabis, but claims "the strongest law and order policy" against serious crime.', ALCP, 'low'),
  womens_rights=C(0, 'Would criminalise sex buyers and ban the "rough sex" defence, but opposes new hate-crime categories.', WRP_FULL, 'low'),
  act=C(-2, 'Mandatory minimum three years for a third burglary; voted to reinstate three strikes.', ACT_BURGLARY, 'high'),
  national=C(-2, 'Reinstated three strikes, banned gang patches, boot camps; "fixing the basics in law and order".', WIKI_THREESTRIKES, 'high'),
  nz_first=C(-2, 'More mandatory minimum sentences, tougher parole, caps on sentence discounts.', NZF_SENTENCING, 'high'),
  conservative=C(-1, '"Punishment that will deter crime"; longer sentences for repeat child-sex offenders; also "individual freedom".', CON_PRINCIPLES, 'medium'),
  vision_nz=C(-1, '"restore order"; deputise Community Support Officers; "hold individuals accountable".', VIS, 'low'),
)
S('soc_vsa_crack_down',
  act=C(2, 'Three strikes for burglary; deport non-citizen serious offenders; licensed security guards with powers to remove people.', ACT_BURGLARY, 'high'),
  national=C(2, '"37,000 fewer victims of crime, no more gang patches, ram raids are down 85%"; add 240 prison beds.', NAT_LUXON_SEPT, 'high'),
  nz_first=C(2, 'Mandatory minimums for violent and sexual offenders; attacks Labour\'s "ridiculous view on law and order".', NZF_ANIMAL_FARM, 'high'),
  conservative=C(1, '"Removal of criminals from society, to protect others"; "Safe neighbourhoods and streets".', CON_PRINCIPLES, 'medium'),
  vision_nz=C(1, '"restoring safety to our streets ... restore order".', VIS, 'medium'),
  green=C(-2, 'Rehabilitation over punishment; end military-style academies; raise the age of criminal responsibility.', GRN_JUSTICE, 'high'),
  te_pati_maori=C(-2, '"Prisons don\'t work because they do nothing to address the root causes of crime".', TPM_PRISONS, 'high'),
  alliance=C(-2, 'Justice "based on prevention, rehabilitation, restorative justice".', ALL_JUSTICE, 'high'),
  te_tai_tokerau_party=C(-2, 'Divert offenders into hapū-run rehabilitation; iwi-governed youth justice.', TTP, 'medium'),
  labour=C(-1, 'Opposed reinstating three strikes and permanent boot camps.', WIKI_THREESTRIKES, 'medium'),
  opportunity=C(-1, '"Prevention – Rehabilitation – Victim focused – Reintegration".', OPP_CRIME, 'medium'),
  legalise_cannabis=C(0, 'Wants "law and order and respect for rule of law" restored by ending prohibition, not by harsher enforcement.', ALCP, 'low'),
)
S('soc_secs_abortion',
  green=C(2, '"Uphold women\'s reproductive rights ... equitable access ... to contraception, abortion"; voted for the 2020 Act at all stages.', GRN_WOMEN, 'high'),
  alliance=C(2, '"ensure free, safe, and accessible abortion services throughout Aotearoa".', ALL_WOMEN, 'high'),
  act=C(1, 'Voted for the Abortion Legislation Act 2020 at all three readings.', WIKI_ABORTION, 'medium'),
  labour=C(1, 'Government bill that decriminalised abortion (2020); most Labour MPs voted for it on a conscience vote.', WIKI_ABORTION, 'medium'),
  womens_rights=C(1, '"the right to have control of our own bodies, including reproductive autonomy".', WRP_PRIORITIES, 'medium'),
  conservative=C(-2, 'Unborn Child (Legal Personhood and Rights) Act from the third trimester.', CON_LIFE, 'high'),
  vision_nz=C(-2, '"a compassionate society must protect its most vulnerable, beginning in the womb"; review laws that "endanger the unborn".', VIS, 'high'),
  nz_first=C(-1, 'Seven of nine NZ First MPs voted against the 2020 Act at its third reading after Peters demanded a referendum.', WIKI_NZF, 'medium'),
  national=C(-1, 'National MPs "mostly opposed the Abortion Legislation Act 2020" (conscience vote).', WIKI_NATIONAL, 'low'),
)
S('soc_secs_religion',
  vision_nz=C(2, 'Led by Destiny Church co-leader Hannah Tamaki; "Under One God" principle.', VIS, 'high'),
  conservative=C(1, '"We stand by Judeo-Christian Western cultural traditions".', CON_POLICY, 'medium'),
  act=C(-1, 'Exclude "purely spiritual and religious effects" from planning law; no karakia or prayers in public-service work time.', ACT_PUBLIC_SERVICE, 'low'),
  te_pati_maori=C(-1, 'Colonial systems including "religion" have "failed to recognise, protect, or serve Takatāpui".', TPM_TAKATAPUI, 'low'),
)
S('soc_secs_traditional_marriage',
  vision_nz=C(2, '"Protect the nuclear family"; tax credits for marriage milestones at 7, 15 and 20 years.', VIS, 'high'),
  conservative=C(1, 'Campaigns on "conservative family values"; "a man is a man, and a woman is a woman".', CON_POLICY, 'medium'),
  nz_first=C(1, 'All seven NZ First MPs voted against same-sex marriage in 2013; "the only socially conservative party".', WIKI_NZF, 'medium'),
  green=C(-2, 'Voted for marriage equality (2013); rainbow policy.', WIKI_MARRIAGE, 'high'),
  labour=C(-1, 'Marriage equality was Labour MP Louisa Wall\'s bill (2013), supported by most Labour MPs.', WIKI_MARRIAGE, 'medium'),
  act=C(-1, 'ACT\'s MP voted for marriage equality (2013); liberal on personal choice.', WIKI_MARRIAGE, 'low'),
  te_pati_maori=C(-1, 'Māori Party MPs voted for marriage equality (2013); takatāpui commission.', WIKI_MARRIAGE, 'low'),
  alliance=C(-1, 'Policy names lesbian and trans women among groups whose barriers it will address.', ALL_WOMEN, 'low'),
  national=C(0, 'MPs split on same-sex marriage (2013 conscience vote).', WIKI_NATIONAL, 'low'),
)
S('soc_secs_traditional_values',
  vision_nz=C(2, '"restoration will ... come from inside the home"; "balanced history and strong civic values".', VIS, 'high'),
  conservative=C(2, '"Conserving the good for a better New Zealand"; conservative family values.', CON_OVERVIEW, 'high'),
  nz_first=C(2, '"We are the only socially conservative party"; "proud traditional kiwi values".', NZF_SOTN, 'high'),
  nz_loyal=C(1, 'Teach children "objective morality".', WIKI_LOYAL, 'low'),
  national=C(1, '"Strong families and caring communities"; a socially conservative wing (conscience votes).', NAT_LUXON_SEPT, 'low'),
  green=C(-1, 'Progressive agenda: drug-law reform, rainbow rights, Te Tiriti co-governance.', GRN_RAINBOW, 'low'),
  alliance=C(-1, 'Progressive gender, reproductive and justice policies.', ALL_WOMEN, 'low'),
  act=C(-1, 'Classical-liberal: End of Life Choice, abortion decriminalisation, secular public service.', WIKI_ABORTION, 'low'),
)
S('soc_secs_family_unit',
  vision_nz=C(2, '"the family is the ultimate cornerstone of society and the primary incubator for our nation\'s morals".', VIS, 'high'),
  conservative=C(2, '"Strong families are the foundation of a healthy society."', CON_OVERVIEW, 'high'),
  national=C(1, '"Strong families and caring communities" is a founding value; 30 weeks paid parental leave.', NAT_LUXON_SEPT, 'medium'),
  nz_first=C(1, '$5,000 grant for new parents; socially conservative self-description.', NZF_SOTN, 'low'),
)
S('soc_secs_patriotism',
  nz_first=C(2, '"We are the only patriotic party ... We stand proud to be patriots of New Zealand"; "nationalist with a capital N".', NZF_SOTN, 'high'),
  vision_nz=C(2, '"One Nation, One People ... One Flag"; schools to "rebuild a shared national identity".', VIS, 'high'),
  nz_loyal=C(2, '"We take our country back from foreign interests"; leave the UN, WEF and WHO.', LOYAL_RNZ, 'medium'),
  conservative=C(1, '"National sovereignty" among its principles; "Policies that put New Zealanders first".', CON_STAND, 'medium'),
  national=C(1, 'Party constitution: "loyalty to country and Sovereign".', WIKI_NATIONAL, 'low'),
)
S('soc_secs_military',
  national=C(2, '"National security" is a founding value; "Boosting defence spending"; Defence Capability Plan to 2% of GDP by 2032/33.', NAT_PENK_DEFENCE, 'high'),
  act=C(1, 'Fiscal plan protects spending growth in "core frontline services such as health, education, defence".', ACT_FISCAL_PDF, 'medium'),
  nz_first=C(1, '"energy security is national security"; praises Ron Mark\'s defence procurement record; coalition partner in the 2025 Defence Capability Plan.', NZF_ELEVENTH, 'medium'),
  labour=C(0, 'Hipkins rejected US calls to lift spending to a set level: "no other country should dictate New Zealand\'s military spend"; would not join AUKUS.', LAB_HIPKINS_DEFENCE, 'low'),
  conservative=C(0, '"Taking a neutral stance rather than being dragged into war"; keep the Australian alliance; a support-and-reconstruction military.', CON_NEWPOL, 'low'),
  green=C(-2, 'Withdraw from Five Eyes; Defence Force to "focus on climate change, humanitarian responses".', GRN_SECURITY, 'high'),
  te_pati_maori=C(-2, 'Declare NZ "militarily neutral"; "War has never delivered enduring safety for ordinary people".', TPM_MILITARY, 'high'),
  alliance=C(-2, 'Non-aligned; "remove offensive capabilities"; close foreign military and intelligence facilities.', ALL_FOREIGN, 'high'),
  free_palestine=C(-2, 'Withdraw from "any formal security alliances with the U.S."; against "military interventionism".', FPP, 'medium'),
)
S('soc_ess_gay_free',
  green=C(2, 'Rainbow communities manifesto; increase resourcing for rainbow organisations.', GRN_RAINBOW, 'high'),
  labour=C(2, 'Rainbow Pae Ora health strategy; passed the conversion-practices ban (2022).', LAB_RAINBOW, 'high'),
  te_pati_maori=C(2, '$200m and an independent Takatāpui-governed Commission; "homophobia and transphobia are no longer acceptable".', TPM_TAKATAPUI, 'high'),
  alliance=C(2, 'Names lesbian and trans women among groups whose rights it will advance.', ALL_WOMEN, 'medium'),
  act=C(1, 'Voted for marriage equality (2013) and the conversion-practices ban (2022).', WIKI_CONVERSION, 'medium'),
  national=C(1, '25 of 33 National MPs voted for the conversion-practices ban (2022); "National with Pride" wing.', WIKI_CONVERSION, 'low'),
  opportunity=C(1, 'Criticises NZ First for telling voters "transgender Kiwis ... are the problem".', OPP_SOTN, 'low'),
  nz_outdoors_freedom=C(1, 'Code of conduct: "We welcome and support people of all backgrounds and identities ... any sexual orientation".', OFP_CONDUCT, 'low'),
  womens_rights=C(1, '"committed to the rights of lesbians to organise and socialise separately".', WRP_FULL, 'low'),
  nz_first=C(0, '"the government has no place in the nation\'s bedrooms – may a thousand blossoms bloom", but derides "rainbow-wars" and voted against same-sex marriage.', NZF_HOPE, 'medium'),
  vision_nz=C(-1, 'Positions "have included opposition to abortion, homosexuality" (Wikipedia); 2026 policies define sex in law and protect the "nuclear family".', WIKI_VIS, 'low'),
)
S('soc_cses_immigrants_economy',
  green=C(2, 'New residency pathways; refugee quota to 5,000; migrant workers "contribute to Business success".', GRN_IMMIGRATION, 'high'),
  labour=C(1, '"Migrants bring much-needed energy and skills"; immigration "planned around what New Zealand needs".', LAB_IMMIGRATION, 'medium'),
  opportunity=C(1, '"Immigration can bring expertise, energy and capital to the New Zealand economy."', OPP_ECONOMY, 'medium'),
  act=C(1, 'Skills categories kept open where demand is shown; "why are we paying people to stay at home who could be doing jobs we are currently filling with migrants?"', ACT_WELFARE, 'low'),
  national=C(1, 'Encourage Active Investor Plus visa holders to stay: "NZ needs partners on the world stage to help businesses get ahead".', NAT_INVESTOR, 'low'),
  alliance=C(1, '"review and reduce unnecessary barriers to migration from neighbouring Pacific Island countries".', ALL_FOREIGN, 'low'),
  nz_first=C(-1, 'Opening "our borders to mass immigration" part of an "abject failure"; visas tied to genuine shortages.', NZF_SOTN, 'medium'),
  conservative=C(-1, '"population growing faster than social goods makes everyone poorer"; cap unskilled migration.', CON_IMMIG, 'medium'),
  vision_nz=C(-2, '"Pause mass immigration immediately".', VIS, 'high'),
  nz_loyal=C(-2, 'Immigration moratorium.', WIKI_LOYAL, 'medium'),
)
S('soc_cses_culture_harmed',
  vision_nz=C(2, 'English the official language; 10-year citizenship wait; a country "where the rights and culture of Kiwi citizens are put first".', VIS, 'high'),
  nz_first=C(1, 'Governments "open[ed] our society to every wild-west simpleton ideology"; "one people, one country, one flag, one law".', NZF_SOTN, 'medium'),
  conservative=C(1, '"Newcomers should follow our way of life."', CON_POLICY, 'medium'),
  nz_loyal=C(1, 'Immigration moratorium; "take our country back from foreign interests".', LOYAL_RNZ, 'low'),
  green=C(-2, 'Communities of Colour policy; "Welcoming, safe and fair pathways to make Aotearoa home".', GRN_IMMIGRATION, 'high'),
  labour=C(-1, 'Immigration policy "aims to treat migrants with decency".', LAB_IMMIGRATION, 'medium'),
  opportunity=C(-1, 'Condemns parties that say "immigrants ... are the problem".', OPP_SOTN, 'low'),
  alliance=C(-1, 'Migrant and refugee women explicitly included in equality policy.', ALL_WOMEN, 'low'),
)

# ================================================================= POPULISM
S('pop_cses_compromise',
  nz_loyal=C(2, '"No compromise. No apologies."', LOYAL_RNZ, 'high'),
  nz_outdoors_freedom=C(1, 'Politicians "go through the motions of the Select Committee process ... and push ahead with their pre-determined agendas anyway".', OFP_DD, 'low'),
  nz_first=C(0, 'Says leaders must "say the things people are thinking without fear or favour", yet has governed with both National and Labour and "reluctantly supported" ACT\'s Regulatory Standards Act.', WIKI_NZF, 'medium'),
  opportunity=C(-1, 'Citizens\' assemblies "consistently find common ground on hard issues".', OPP_VOICE, 'medium'),
)
S('pop_cses_dont_care',
  nz_outdoors_freedom=C(2, '"They hear us, but they refuse to listen"; "politicians ram through deeply unpopular laws".', OFP_DD, 'high'),
  vision_nz=C(2, '"career politicians insulated inside a Wellington bubble".', VIS, 'high'),
  nz_loyal=C(2, '"We reject government overreach"; "Expose and eradicate propaganda from our news media".', LOYAL_RNZ, 'medium'),
  nz_first=C(1, '"Those out of touch, bureaucratic, left elitists"; "Ordinary kiwis have had enough."', NZF_DEEDS, 'medium'),
  te_pati_maori=C(1, '"politicians lining their own pockets while whānau go without"; "Wellington definitely does not work for Māori".', TPM_MP_PAY, 'medium'),
  opportunity=C(1, '"Left-right politics is failing New Zealand"; "trust in government is under pressure".', OPP_LEFTRIGHT, 'medium'),
  alliance=C(1, '"Political power must not be concentrated in the hands of governments ... or distant bureaucracies."', ALL_DEMOCRACY, 'low'),
  te_tai_tokerau_party=C(1, 'Seeks "political and economic independence" from a Wellington that "extracts" from the North.', TTP, 'low'),
)
S('pop_cses_trustworthy',
  nz_loyal=C(-2, 'Anti-establishment platform: expose media "propaganda"; leave the UN, WEF, WHO.', LOYAL_RNZ, 'medium'),
  nz_outdoors_freedom=C(-2, '"the fake listening stops"; politicians hide "behind toothless" consultation.', OFP_DD, 'medium'),
  vision_nz=C(-1, 'Drug testing for MPs; replace "career politicians" with "dedicated public servants".', VIS, 'medium'),
  opportunity=C(-1, 'A political corruption watchdog and policy-costing unit "if trust is to be rebuilt".', OPP_CLEAN, 'low'),
  nz_first=C(-1, 'Attacks "elitist" opponents and "Wellington" as out of touch.', NZF_DEEDS, 'low'),
)
S('pop_cses_main_problem',
  nz_loyal=C(2, '"We take our country back"; scrap the tax system, leave international bodies.', LOYAL_RNZ, 'medium'),
  nz_outdoors_freedom=C(1, 'Direct democracy because politicians "ram through deeply unpopular laws".', OFP_DD, 'medium'),
  vision_nz=C(1, '"MMP Fatigue and Democracy Reset": eliminate "unelected List MPs".', VIS, 'low'),
)
S('pop_cses_strong_leader',
  act=C(-2, 'Add to the Constitution Act that "the rule of law is fundamental" and "Everyone, including the Government, should be bound by the law".', ACT_ONE_LAW_PDF, 'high'),
  alliance=C(-2, '"Parliament must be an effective check on executive power"; an entrenched Bill of Rights.', ALL_DEMOCRACY, 'high'),
  labour=C(-1, 'Limit urgency "to genuine emergencies" and send rushed laws back to select committee.', LAB_TRUST, 'medium'),
  opportunity=C(-1, 'Concern at "increasingly centralised executive power"; corruption watchdog.', OPP_CLEAN, 'medium'),
  nz_outdoors_freedom=C(-1, 'Fundamental rights "will no longer be able to be voted away by politicians".', OFP_DD, 'medium'),
  green=C(-1, 'Lobbying register, donation caps, "uphold the international rule of law".', GRN_LOBBY, 'low'),
  nz_first=C(0, '"New Zealand needs strong leadership who are not afraid to be strong", while naming "the rule of law" a core Western value.', NZF_ANIMAL_FARM, 'medium'),
)
S('pop_cses_people_decide',
  nz_outdoors_freedom=C(2, 'Swiss-style binding citizens\' referendums: a citizens\' veto and citizen-initiated laws.', OFP_DD, 'high'),
  nz_first=C(2, 'Binding referendum on the Māori seats; long-standing advocacy of "binding citizen initiated referenda".', NZF_REFERENDUM, 'high'),
  act=C(1, 'Campaigned for a binding referendum on Treaty principles; restored binding local referendums on Māori wards.', ACT_ONE_LAW, 'medium'),
  conservative=C(1, 'Party policy has included "Binding citizens-initiated referendums".', WIKI_CON, 'low'),
  nz_loyal=C(1, '"Decentralise government and return power to the people."', LOYAL_RNZ, 'medium'),
  opportunity=C(1, 'Randomly selected citizens\' assemblies, mirroring the number of MPs, to advise on major issues ("Direct democracy").', OPP_VOICE, 'medium'),
  alliance=C(1, 'Citizens\' Initiatives and recall, but "Direct democracy should complement representative democracy rather than replace it".', ALL_DEMOCRACY, 'low'),
  animal_justice=C(1, '"Establish citizens\' assemblies for major policy decisions currently deadlocked".', AJP_PEOPLE, 'low'),
  vision_nz=C(1, 'Place "power firmly back into the hands of local voters"; abolish party lists.', VIS, 'low'),
  green=C(0, 'Citizens\' assemblies for local decisions, but entrench the Māori seats beyond referendums.', GRN_DEMOCRACY, 'low'),
  te_pati_maori=C(-1, 'Entrench the Māori seats "beyond the reach of referendums"; "constitutional, not conditional".', TPM_SEATS, 'medium'),
)
S('pop_cses_rich_powerful',
  nz_loyal=C(2, 'Opposition to "globalist" institutions "such as the United Nations, Banks, and the World Economic Forum".', LOYAL_RNZ, 'medium'),
  alliance=C(1, 'Media should hold "the wealthy and the politicians\' feet to the fire"; "We don\'t receive large donations from big business".', ALL_STAND, 'low'),
  te_pati_maori=C(1, 'Tax system "rewarding wealth accumulation and property speculation"; MPs "lining their own pockets".', TPM_MP_PAY, 'low'),
  nz_outdoors_freedom=C(1, 'Government "acts as Pfizer\'s unpaid insurance company".', OFP_ACC, 'low'),
  green=C(1, 'Lobbying and donation reform so "big money and professional lobbying can have less influence over politics".', GRN_LOBBY, 'low'),
  opportunity=C(1, '"growing private and foreign influence in politics, expanding political lobbying".', OPP_CLEAN, 'low'),
  nz_first=C(1, 'Fonterra "gone from a propped-up nationalist company, to a sell-out globalist company"; attacks "elitists".', NZF_SOTN, 'low'),
)
S('pop_cses_majority',
  nz_first=C(2, 'Binding referendum on the Māori seats; "forcing government to accept the will of the people".', NZF_REFERENDUM, 'high'),
  act=C(1, 'Treaty principles must not "go beyond what Parliament intend[ed]" "to protect democratic majority rule"; but "every New Zealander is equal before the law".', ACT_ONE_LAW_PDF, 'medium'),
  nz_loyal=C(1, '"Scrap all race-based policies."', LOYAL_RNZ, 'low'),
  vision_nz=C(1, '"One Vote"; "End all race-based politics".', VIS, 'low'),
  conservative=C(1, '"One people under one law"; "equal treatment".', CON_OVERVIEW, 'low'),
  national=C(0, 'Voted down the Treaty Principles Bill (2025) but restored local referendums on Māori wards (2024).', WIKI_TPB, 'medium'),
  nz_outdoors_freedom=C(0, 'Binding referendums on laws, yet fundamental rights "belong to the people anyway" and cannot be voted away.', OFP_DD, 'medium'),
  labour=C(-1, 'Opposed the Treaty Principles Bill; opposed Māori-ward referendums.', WIKI_TPB, 'low'),
  te_pati_maori=C(-2, 'Māori seats "guaranteed under Te Tiriti"; entrench them "beyond the reach of referendums".', TPM_SEATS, 'high'),
  green=C(-2, 'Entrench the Māori seats; councils as Te Tiriti partners with Māori wards.', GRN_DEMOCRACY, 'high'),
  alliance=C(-2, 'Any direct-democracy system must include "protection of minority and individual rights".', ALL_DEMOCRACY, 'high'),
  te_tai_tokerau_party=C(-2, 'Constitutional protection for He Whakaputanga and Te Tiriti; iwi-governed institutions.', TTP, 'medium'),
)

PARTY_KEYS = {
    'national': 'national', 'labour': 'labour', 'green': 'green', 'act': 'act', 'nz_first': 'nz-first',
    'te_pati_maori': 'te-pati-maori', 'opportunity': 'opportunity', 'nz_loyal': 'nz-loyal',
    'nz_outdoors_freedom': 'nz-outdoors-freedom', 'legalise_cannabis': 'legalise-cannabis',
    'animal_justice': 'animal-justice', 'alliance': 'alliance', 'conservative': 'conservative',
    'womens_rights': 'womens-rights', 'vision_nz': 'vision-nz', 'free_palestine': 'free-palestine',
    'te_tai_tokerau_party': 'te-tai-tokerau-party',
}
PARTY_NAMES = {
    'national': 'National', 'labour': 'Labour', 'green': 'Green', 'act': 'ACT', 'nz-first': 'NZ First',
    'te-pati-maori': 'Te Pāti Māori', 'opportunity': 'Opportunity (TOP)', 'nz-loyal': 'NZ Loyal',
    'nz-outdoors-freedom': 'NZ Outdoors & Freedom', 'legalise-cannabis': 'Legalise Cannabis',
    'animal-justice': 'Animal Justice', 'alliance': 'Alliance', 'conservative': 'Conservative',
    'womens-rights': "Women's Rights", 'vision-nz': 'Vision NZ', 'free-palestine': 'Free Palestine',
    'te-tai-tokerau-party': 'Te Tai Tokerau Party',
}
