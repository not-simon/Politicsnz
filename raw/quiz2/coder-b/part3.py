# Coder B data, part 3: ten small parties
RNZ = "https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election"

nz_loyal = {
 "S4": c(-2, "Website platform as quoted by RNZ (12 Oct 2026): 'Protect our children from corrupt sex and gender education'. Party site not retrievable.", RNZ, 1, "high"),
 "T1": c(-1, "'Scrap all race-based policies' (website via RNZ, Oct 2026) - explicit general principle whose scope covers Treaty-based differentiated decisions; inference, low.", RNZ, 1, "low"),
 "T2": c(2, "'Scrap all race-based policies' (website via RNZ, Oct 2026) - directly covers seats, wards and services set aside for Māori.", RNZ, 1, "medium"),
 "V4": c(-2, "'End climate accords based on faulty science' (website via RNZ, Oct 2026).", RNZ, 1, "high"),
 "V5": c(1, "'Establish energy independence, including oil and gas'; 'Save our farmers from restrictive regulations' (website via RNZ) - supports extraction but says nothing about paying for services; qualified.", RNZ, 1, "medium"),
 "D3": c(1, "'Decentralise government and return power to the people' (website via RNZ, Oct 2026) - general principle covering council autonomy; inference, low.", RNZ, 1, "low"),
 "E2": c(1, "'Scrap the current tax system' and 'reject government overreach' (website via RNZ); replacement not described. Weak inference toward smaller state, low.", RNZ, 1, "low"),
}

alcp = {
 "S3": c(2, "Full Spectrum Policy: 'possession, cultivation and use of pure cannabis... be free from prosecution', regulated R18 commerce, expunge convictions; principle of 'upholding of individual and civic rights where these do not unreasonably impinge on others'.", "https://www.alcp.org.nz/policy", 1, "high"),
 "T1": c(1, "Policy section 9: 'supports principles of partnership, tolerance and co-operation underpinning the treaty'; 'Full inclusion of Treaty of Waitangi principles' as a founding principle (1996). General principle, qualified agree.", "https://www.alcp.org.nz/policy", 1, "low"),
 "S1": c(-1, "Policy redirects enforcement money 'to fight serious crime' but argues 'criminalisation is self-perpetuating' and seeks a prohibition truth-and-reconciliation commission; no sentencing-length position. Weak inference, low.", "https://www.alcp.org.nz/policy", 1, "low"),
}

VIS = "https://www.vision.org.nz/visionpolicies"
vision = {
 "S4": c(-2, "'Completely remove ideologically driven gender theory, Relationship and Sexuality Education (RSE), and political propaganda from the national curriculum'; ban gender-transition interventions for minors; Parental Rights Bill (Our Policies, 2026).", VIS, 1, "high"),
 "T1": c(-2, "'End all race-based politics and He Puapua-driven policies across government'; 'One Nation, One People, One Vote, One Government, One Flag, Under One God'.", VIS, 1, "high"),
 "T2": c(2, "'End all race-based politics and He Puapua-driven policies across government'; 'Completely remove all race-based targeted policies and spending within the healthcare sector'; 'One Vote'.", VIS, 1, "high"),
 "T3": c(-1, "Ending 'He Puapua-driven policies' (the co-governance roadmap) and 'divisive race-based politics' - explicit principle covering shared decision-making; inference, low.", VIS, 1, "low"),
 "T5": c(-2, "'Declare English as the official language of New Zealand'; early childhood centres 'free from... overt cultural content'.", VIS, 1, "high"),
 "V4": c(-2, "'Restore absolute national sovereignty by leaving the United Nations and the Paris Accord'.", VIS, 1, "high"),
 "O1": c(2, "'Pause mass immigration immediately to review visa policies and relieve pressure on local infrastructure and communities'; 10-year residency for citizenship; end dual citizenship for new applicants.", VIS, 1, "high"),
 "E5": c(0, "'Dismantle state dependency' and 'eliminate financial rules that disincentivise marriage' alongside 'no-strings-attached' family payments and abolishing tax on benefits. Both sides -> argued neutral, low.", VIS, 1, "low"),
 "D1": c(-1, "Democracy Reset: abolish MMP party lists, cut MP numbers, term limits - reforms of representative democracy, not referendums; 'Reject the introduction of digital IDs'. No referendum policy; weak inference, low.", VIS, 1, "low"),
}

FPP = "https://palfree.nz/"
free_palestine = {
 "O3": c(2, "Founding principle 6: 'New Zealand commit to an independent foreign policy by withdrawing itself from any formal security alliances with the U.S. and by distancing our foreign policy from the orbit of Anglo-U.S. economic hegemony and military interventionism'.", FPP, 1, "high"),
}

TTP = "https://tetaitokerauparty.org.nz/our-policies/"
ttp = {
 "E5": c(-2, "Ōranga Whānau: replace 'the complex, punitive benefit system' with a non-taxable Universal Whānau Allowance, wipe $2b of MSD/IRD debt, 'Remove all relationship status policing'.", TTP, 1, "high"),
 "E1": c(1, "Universal Whānau Allowance, debt amnesty, 25% mana whenua equity in regional infrastructure, living-wage trade academy - redistribution without a stated tax measure; qualified, low.", TTP, 1, "low"),
 "S1": c(-2, "Te Hokinga Mai: 'Prison Sinking Lid Policy' diverting non-violent offenders into hapū-run rehabilitation; prisons 'perpetuate multi-generational trauma'.", TTP, 1, "high"),
 "S6": c(-2, "Māori Justice & Autonomous Policing Act: transfer youth-justice budgets to iwi-governed authorities, 'restorative justice networks' replacing 'punitive policing and incarceration'.", TTP, 1, "high"),
 "T1": c(2, "Pillar Four: Tiriti-centred constitution, repeal Regulatory Standards Act and the Treaty Clauses Review, Te Ture Mokopuna upholding Te Tiriti obligations, Māori-governed health authority.", TTP, 1, "high"),
 "T2": c(-2, "Te Aka Motuhake iwi-governed health authority, Māori Justice Authority, Māori-governed land fund and data commission - services set aside specifically for Māori.", TTP, 1, "high"),
 "T3": c(2, "Mana Kaitiaki: iwi/hapū guardians with 'statutory authority to monitor, manage, and enforce environmental regulations within their rohe'; Moana Ora Act with 30% of waters co-designed and managed by iwi/hapū; land-back for climate buffers.", TTP, 1, "high"),
 "T4": c(-2, "Increase and entrench Waitangi Tribunal funding and 'extend its binding jurisdiction on the Crown'; constitutional protection against legislative harm to Te Tiriti and He Whakaputanga.", TTP, 1, "high"),
 "T5": c(1, "Te Tiriti re-education 'embedded in the NZ Curriculum and in public service professional development, including for all sitting MPs'; 'Strong Whakapapa - mokopuna have strong, secure connections to culture and language'.", TTP, 1, "medium"),
 "T6": c(-2, "Waitangi Tribunal powers and funding expanded; Hoki Whenua Mai statutory land-return engine funded by 20% of Crown revenue from public land, replacing 'lengthy negotiations'.", TTP, 1, "high"),
 "V1": c(1, "Mokopuna wellbeing goal 'Resilient Whenua - a resilient, biodiverse, healthy natural environment'; Moana Ora Act protects 30% of territorial waters and ends bottom trawling. No explicit growth trade-off; qualified.", TTP, 1, "medium"),
 "D3": c(1, "Decentralised, rohe-based delivery of health, justice and civil defence; deregulation of hyper-local food trade 'free of council licensing'. Supports local autonomy generally though not councils specifically; inference, low.", TTP, 1, "low"),
}

WRP = "https://womensrightsparty.nz/wp-content/uploads/2025/11/POLICY-Womens-Rights-Party-2025-041125.docx"
wrp = {
 "S4": c(-2, "Full policy (4 Nov 2025): stop schools supporting 'social transition', full disclosure to parents of sexuality education, sex-based rights 'given precedence over any proposed provisions based on concepts of gender'; ban puberty blockers for under-18s.", WRP, 1, "high"),
 "S5": c(1, "Hate Crimes proposal: 'The Women's Rights Party does not support the creation of new hate crime laws'; concern that such laws 'could lead to a crackdown' on women's-rights advocacy. Opposes new speech crimes; qualified agree.", WRP, 1, "medium"),
 "E6": c(2, "'reinstatement of legislative support for Fair Pay Agreements' and pay equity in private and public sectors (full policy 2025).", "https://womensrightsparty.nz/policy-proposal/pay-equity/", 1, "high"),
 "E1": c(1, "'Minimum wages and benefits need to be increased so that all people have living incomes'; CPAG-style Working for Families reform for 'the poorest families'. No tax measure; qualified, low.", WRP, 1, "low"),
 "T1": c(1, "'We acknowledge Te Tiriti o Waitangi as Aotearoa New Zealand's founding document' (full policy 2025) - brief general acknowledgement only; qualified, low.", WRP, 1, "low"),
 "V1": c(1, "Environmental policy: principle of 'the right to a clean and safe natural environment'; lists climate, environment and conservation among concerns. No growth trade-off stated; low.", "https://womensrightsparty.nz/policy-proposal/environmental/", 1, "low"),
 "S1": c(1, "Supports 'standalone, sex-based laws with higher penalties' for violence against women and children, banning the rough-sex defence, keeping biological males out of women's prisons. Partial - longer sentences only for this class of crime; low.", WRP, 1, "low"),
}

CON_CLIM = "https://conservatives.org.nz/policies/climate/"
CON_OVER = "https://conservatives.org.nz/policies/overview/"
CON_SMALL = "https://www.conservatives.nz/small-government"
CON_ECON = "https://conservatives.org.nz/policies/economy-1/"
CON_NEW = "https://www.conservatives.nz/news/new-policies-announcement"
CON_RES = "https://conservatives.org.nz/policies/natural-resources/"
CON_IMM = "https://conservatives.org.nz/policies/immigration/"
CON_PRIN = "https://www.conservatives.nz/principles"
conservative = {
 "E1": c(-1, "Finance policy: 'press for a flat tax rate for individuals and for companies'; principles: New Zealanders 'free to enjoy the fruits of their labour to the greatest possible extent'. Explicit principle against redistributive taxation; qualified.", CON_NEW, 1, "medium"),
 "E2": c(2, "Small Government page: 'over-governed, over-regulated, and over-taxed'; 'Government spending and borrowing... must be slashed'; cut personal and company tax, GST to 12.5%; 'shrink government so that it focuses on its core business'.", CON_SMALL, 1, "high"),
 "E3": c(-1, "'Flat tax rate for individuals and for companies' and lower taxes generally; no explicit CGT statement found. Inference from explicit tax principle, low.", CON_NEW, 1, "low"),
 "E4": c(0, "Mixed: 'the private sector prevailing over State control' and buying private hospital capacity, but also a state oil-tanker fleet, new state-backed refineries and a Norway-style public resource venture. Both sides -> argued neutral.", CON_RES, 1, "low"),
 "E5": c(1, "Policy index: 'Welfare: Reform is needed. Fifty years of expanding welfare has undermined our families and created an underclass'; 'Less dependency'. No specific sanctions policy; qualified.", "https://www.conservatives.nz/policy", 1, "low"),
 "E7": c(1, "'debt levels are a crisis which needs to be addressed now'; 'urgently tackling the massive debt'; but spending to be redirected to infrastructure and hospital waiting lists. Qualified agree.", CON_SMALL, 1, "medium"),
 "S1": c(2, "Principles: 'Punishment that will deter crime. Removal of criminals from society'; child-protection policy: 'repeat child sexual offenders face significantly longer prison sentences', review sentence reductions; overview: 'meaningful consequences for serious and repeat offending'.", CON_PRIN, 1, "high"),
 "S4": c(-2, "'Protecting children from radical gender ideology'; 'A man is a man, and a woman is a woman'; restrict gender-related medical procedures for minors with parental involvement.", "https://www.conservatives.nz/we-stand-for", 1, "high"),
 "S5": c(2, "'Freedom of speech and assembly' (What We Stand For); 'Defend freedom of speech and assembly' (policies); overview: free to 'express their views, practise their beliefs'; laws 'must not be weaponised to target people with particular views'.", "https://www.conservatives.nz/we-stand-for", 1, "high"),
 "T1": c(-2, "'One people under one law... We oppose policies that divide people according to race, ancestry, sex or identity'; 'Attempts to divide us by race are to be resisted'; 'end the gravy train for... tribal elites'.", CON_OVER, 1, "high"),
 "T2": c(2, "'Employment, promotion, and access to services based purely on merit'; 'Every New Zealander should have the same rights... under the law'; 'One Nation: New Zealanders are one people'.", CON_OVER, 1, "high"),
 "T3": c(-1, "'One people under one law' and opposition to race-based differentiation - explicit principle covering shared Māori-Crown decision-making; inference, low.", CON_OVER, 1, "low"),
 "T5": c(-1, "'Newcomers should follow our way of life'; 'Judeo-Christian Western cultural traditions'; resist division by race. No explicit te reo policy; inference, low.", "https://www.conservatives.nz/policy", 1, "low"),
 "V1": c(-1, "Climate policy: 'no climate emergency', 'Ending climate change alarmism'; make use of fossil fuels and minerals; yet 'committed to conserving and enhancing our natural environment' and a Kermadec sanctuary. Qualified disagree.", CON_CLIM, 1, "medium"),
 "V2": c(-2, "'All taxes and restrictions on fossil fuels which are based on climate ideology should be scrapped'; scrap the ETS; end public funding of methane research.", CON_CLIM, 1, "high"),
 "V3": c(1, "Agriculture policy: 'revisit the Planning and Natural Environment Bills to make them workable and protect property rights'; 'Fewer and less burdensome regulations'; 'Remove excessive red tape to speed up project approvals while maintaining environmental protections'. Qualified.", CON_RES, 1, "low"),
 "V4": c(-2, "'New Zealand should leave the Paris Agreement (and any other international agreements relating to climate)'.", CON_CLIM, 1, "high"),
 "V5": c(2, "Natural Resources: 'Actively encourage commercial oil and gas exploration', Norway-style joint venture, 'Hold the returns in a New Zealand Investment Fund... for future generations'; royalties shared with communities.", CON_RES, 1, "high"),
 "O1": c(2, "Immigration: net immigration of non-skilled migrants 'capped based on a broad measure of social goods... If our social goods are not increasing, net immigration... should be zero'; end golden visas.", CON_IMM, 1, "high"),
 "O2": None,
 "O3": c(1, "'Trade before War should be New Zealand's axiom. Taking a neutral stance rather than being dragged into war confrontations... should be a priority'; defence focused on support and reconstruction; but 'New Zealand must retain close' defence ties (text truncated). Qualified agree.", CON_NEW, 1, "medium"),
 "D3": c(1, "Principles: 'Decision-making should be as local as possible... localism'; 'Local decision making'; mayors may become full-time council CEOs; ministers to appoint and sack senior officials. Qualified agree.", CON_PRIN, 1, "medium"),
 "D1": c(0, "'Honest democratic process' and 'give power back to the people' with reforms aimed at bureaucrats and judiciary rather than referendums; no referendum policy. Vague -> argued neutral, low.", "https://www.conservatives.nz/policy", 1, "low"),
}

OFP_DD = "https://freedom.kiwi/direct-democracy"
ofp = {
 "D1": c(2, "Direct Democracy: Swiss-style binding citizens' veto and citizen-initiated laws with low signature thresholds; 'the power of veto shifts entirely to you'; demand a binding referendum on direct democracy as a coalition condition.", OFP_DD, 1, "high"),
 "D3": c(2, "'Subsidiarity': decisions on local infrastructure, land management and regional development 'returned entirely to local communities'; regions retain a portion of GST and tax raised locally.", OFP_DD, 1, "high"),
 "S3": c(2, "Cannabis policy: no criminal offence for personal possession or growing; Direct Democracy page lists 'bodily autonomy' and 'the right to refuse medical treatment' among sacred rights.", "https://freedom.kiwi/cannabis-policy", 1, "high"),
 "S5": c(2, "Enshrine NZBORA as supreme law so 'freedom of speech, movement, thought and conscience' can never be 'voted away by politicians' (Sue Grey).", OFP_DD, 1, "high"),
 "V4": c(-2, "Agriculture policy: withdraw from the Paris Agreement; 'That's nature, not climate change'; staying 'would cost more than leaving'.", "https://freedom.kiwi/agriculture-policy", 1, "high"),
 "V1": c(1, "Outdoors origins 'protecting our environment'; poison-free conservation, ecological agriculture 'with minimal synthetic inputs', fisheries QMS replaced to restore stocks; but local communities to decide conservation rules. Qualified agree, low.", "https://freedom.kiwi/outdoors-recreation-and-wildlife-policy", 1, "low"),
 "E4": c(-1, "Fisheries policy keeps fisheries 'in public ownership' with no private sale of rights; housing policy: Ministry of Housing 'hands-on role' and restore 'leadership in social housing'. Partial, low.", "https://freedom.kiwi/nzofp-fisheries-policy", 1, "low"),
 "T1": c(0, "Direct Democracy page reinterprets Article 2 tino rangatiratanga as 'self-determination... for all New Zealanders' via decentralisation; neither supports nor rejects Māori-specific arrangements. Vague -> argued neutral, low.", OFP_DD, 1, "low"),
 "E2": c(1, "'Smaller, leaner central government', 'Ending Bureaucratic Waste', shrink central ministries; no tax-cut pledge. Qualified, low.", OFP_DD, 1, "low"),
}

AJP_PEOPLE = "https://animaljustice.org.nz/policies/ajp-people-policies-pack/"
AJP_ENV = "https://animaljustice.org.nz/policies/ajp-environmental-and-economic-policies/"
AJP_SUM = "https://animaljustice.org.nz/policies/policy-summary/"
ajp = {
 "D2": c(2, "People policies: 'Permit only New Zealand citizens or permanent residents registered to vote to make political donations, removing corporate/industry entity donations'; $30,000 cap per cycle; disclosure threshold $1,500.", AJP_PEOPLE, 1, "high"),
 "V1": c(2, "Economic sufficiency 'within planetary boundaries'; shrink animal agriculture to cut emissions; protect and restore habitats; ban bottom trawling and restrict seabed mining.", AJP_SUM, 1, "high"),
 "V2": c(1, "Habitat policy: 'Redirect funds away from animal agriculture, through taxes and regulations'; 'internalising environmental and social costs' for polluters; no explicit emissions-pricing scheme. Qualified agree.", AJP_ENV, 1, "medium"),
 "V5": c(-2, "Environmental policies: 'End government underwriting and tax incentives for fossil fuel exploration, particularly... offshore oil and gas exploration'; mining 'destroy[s] underground habitats'; restrict seabed mining.", AJP_ENV, 1, "high"),
 "V4": c(1, "Environmental policies: 'Set legally binding targets for 100% renewable electricity'; 'urgently addressing climate change' by shrinking animal agriculture. No explicit international-commitment statement; inferred from explicit climate targets, low.", AJP_ENV, 1, "low"),
 "T1": c(1, "Te Tiriti policy: 'protecting the rights of animals requires genuine partnership with Māori'; 'Treaty-based approach to economic transition'.", "https://animaljustice.org.nz/policies/te-tiriti-o-waitangi/", 1, "medium"),
 "E6": c(1, "People policies: 'Strong unions and worker rights provide the foundation for reducing inequality'; worker rights 'through collective organisation'. No FPA/industry-bargaining specifics; qualified.", AJP_PEOPLE, 1, "medium"),
 "E1": c(1, "People policies address 'economic inequality' and reducing inequality through employment law and transition support; no tax policy stated. Qualified, low.", AJP_PEOPLE, 1, "low"),
 "D1": c(1, "People policies praise deliberative democracy (Irish citizens' assembly leading to a referendum) and propose citizens' assemblies; not binding referendums per se. Qualified, low.", AJP_PEOPLE, 1, "low"),
 "S5": c(1, "Policy summary: 'whistleblower protection and support for peaceful protest' - protects dissent but not offensive speech generally; low.", AJP_SUM, 1, "low"),
}

ALL_TAX = "https://allianceparty.nz/wp-content/uploads/2026/09/alliance-tax-justice-cost-of-living-policy-2026.pdf"
ALL_OWN = "https://allianceparty.nz/wp-content/uploads/2026/10/alliance-public-ownership-economic-democracy-policy-2026.pdf"
ALL_WELF = "https://allianceparty.nz/wp-content/uploads/2026/09/alliance-welfare-family-social-security-policy-2026.pdf"
ALL_WORK = "https://allianceparty.nz/wp-content/uploads/2026/09/alliance-workers-rights-employment-policy-2026.pdf"
ALL_JUST = "https://allianceparty.nz/wp-content/uploads/2026/09/alliance-justice-policy-2026.pdf"
ALL_TIRITI = "https://allianceparty.nz/wp-content/uploads/2026/09/alliance-te-tiriti-democracy-constitutional-policy-2026.pdf"
ALL_ENV = "https://allianceparty.nz/wp-content/uploads/2026/09/alliance-environment-climate-sustainable-economy-policy-2026.pdf"
ALL_FOR = "https://allianceparty.nz/wp-content/uploads/2026/10/alliance-foreign-affairs-defence-international-relations-policy-2026.pdf"
alliance = {
 "E1": c(2, "Tax Justice policy (Sep 2026): first $20,000 tax-free funded by a 2.5% wealth tax over $2m, 47% top rate above $250,000; 'income is taxed from the first dollar... while wealth is lightly taxed'.", ALL_TAX, 1, "high"),
 "E2": c(-2, "Free GP, dental, optical and audiology care, universal child benefit, free public transport, funded by wealth, CGT and transaction taxes; 'reverse privatisation'. Public services over tax cuts.", ALL_TAX, 1, "high"),
 "E3": c(2, "'33% capital gains tax on realised gains, excluding the family home', covering investment property, shares and business assets, plus annual wealth tax (Tax Justice 2026).", ALL_TAX, 1, "high"),
 "E4": c(-2, "Public Ownership policy (Oct 2026): 're-integrate electricity generation, transmission, distribution, and retail under public ownership'; return ports, water, telecoms and Air NZ to full public ownership; 100% publicly owned transport system; state-house rebuilding.", ALL_OWN, 1, "high"),
 "E5": c(-2, "Welfare policy: 'abolish benefit sanctions', abolish stand-downs, end welfare debt recovery, Universal Benefit.", ALL_WELF, 1, "high"),
 "E6": c(2, "Workers' Rights policy: 'Restore national collective bargaining', broad right to strike, Work Councils; NZCTU scorecard Oct 2026: Alliance 'Yes' to restoring Fair Pay Agreements.", ALL_WORK, 1, "high"),
 "E7": c(-2, "Platform of universal free health care, child benefit, 52 weeks' parental leave and public job creation funded by new taxes; 'full employment' and public investment as central goals; no debt-reduction target.", ALL_WORK, 1, "medium"),
 "S1": c(-2, "Justice policy: 'Our high imprisonment rate cannot be addressed simply by building more prisons or imposing harsher sentences'; 'reduce unnecessary imprisonment', 'three strikes and into treatment'.", ALL_JUST, 1, "high"),
 "S4": c(1, "Women and Gender Equality policy: 'support for informed-consent gender-affirming care', Gender Audit framework; no schools/RSE statement. Qualified agree.", "https://allianceparty.nz/wp-content/uploads/2026/09/alliance-women-gender-equality-economic-security-policy-2026.pdf", 1, "medium"),
 "S6": c(-2, "Justice policy: habilitation centres 'particularly for young people', Community Care Orders, iwi-run rehabilitation for young offenders instead of imprisonment.", ALL_JUST, 1, "high"),
 "T1": c(2, "Te Tiriti policy: 'Honouring Te Tiriti o Waitangi is not simply a matter of consultation. It must be reflected in the structure and operation of the state'; constitution grounded in Te Tiriti; act on Tribunal recommendations.", ALL_TIRITI, 1, "high"),
 "T2": c(-1, "Te Tiriti reflected in 'the structure and operation of the state', Māori role in appointing Tribunal members, Matike Mai considered; no explicit Māori seats/wards position. Inference from explicit principle, low.", ALL_TIRITI, 1, "low"),
 "T3": c(1, "Constitutional review to consider Matike Mai; 'Māori must have a meaningful role'; Māori consent on trade agreements affecting Māori interests. Partnership direction without a specific resource co-governance commitment; qualified.", ALL_TIRITI, 1, "medium"),
 "T4": c(-2, "'strengthen the Waitangi Tribunal... resources and independence necessary to perform its constitutional role'; 'commit to acting upon the recommendations of the Waitangi Tribunal'.", ALL_TIRITI, 1, "high"),
 "T6": c(-2, "Strengthening the Tribunal and acting on its findings on Treaty breaches; constitutional status of Te Tiriti to be reviewed - process expanded, not closed.", ALL_TIRITI, 1, "medium"),
 "V1": c(2, "Environment policy: 'polluter pays', Genuine Progress Index alongside GDP, mining banned in national parks, conservation land and the Coromandel, 'some environments are simply too important to risk permanent damage'.", ALL_ENV, 1, "high"),
 "V2": c(2, "'Replace the Emissions Trading Scheme with a carbon tax' with a transparent price; 'strict polluter-pays principle'; support farmers to 'reduce agricultural emissions'.", ALL_ENV, 1, "high"),
 "V3": c(-1, "Environment policy: restoration bonds and 'stringent' conditions for permitted mining, Conservation Minister veto; trade release criticises the Government 'fast-tracking legislation'. No explicit Fast-track Act position; qualified disagree.", ALL_ENV, 1, "medium"),
 "V4": c(1, "'Climate change represents one of the greatest threats... fundamental transition away from dependence on fossil fuels'; carbon tax. No explicit Paris statement found; inferred from explicit climate principle, low.", ALL_ENV, 1, "low"),
 "V5": c(-2, "Ban mining in national parks, conservation land and the Coromandel; 'transition away from dependence on fossil fuels'; electricity to be renewable and public.", ALL_ENV, 1, "high"),
 "O1": c(-1, "Foreign policy: 'review and reduce unnecessary barriers to migration from neighbouring Pacific Island countries'; no overall numbers position. Qualified disagree, low.", ALL_FOR, 1, "low"),
 "O2": c(-1, "Welfare policy abolishes 'unnecessary stand-down periods' and makes benefits a universal entitlement based on 'dignity' - scope plainly covers migrant stand-downs though migrants are not named; inference, low.", ALL_WELF, 1, "low"),
 "O3": c(2, "'independent, non-aligned, and peaceful nation'; 'We reject the idea that security is achieved through military alliances'; withdraw from inconsistent alliances, review foreign military and intelligence facilities.", ALL_FOR, 1, "high"),
 "D1": c(1, "Constitutional review to 'examine the establishment of Citizens' Initiatives, allowing citizens to propose legislation'; referendum on the monarchy; 'Any constitutional change should be determined democratically by the people'. Qualified agree.", ALL_TIRITI, 1, "medium"),
 "D2": c(1, "'strict transparency requirements for political donations... consider appropriate limits on political donations to prevent wealthy individuals, corporations, and other organisations from acquiring disproportionate political influence'; not an individuals-only rule. Qualified.", ALL_TIRITI, 1, "medium"),
 "D3": c(1, "Constitutional review to consider 'the role of local government'; end requirement for councils to put water into arms-length entities; repeal procurement rules forcing councils into corporatised public transport. Qualified agree.", ALL_ENV, 1, "medium"),
}
