#!/usr/bin/env python3
"""Build data/promises/national.json (National Party promise tracker) and print a scorecard.

Every entry follows docs/SCHEMA.md: promise, made, category, status, detail, sources.
Assessments were researched on 2026-10-23 (see parties/national/track-record.md for method).
Run: python3 -I tools/record_national_build.py
"""
import json, os, collections

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# --- shared sources -------------------------------------------------------
W_NAT = "https://en.wikipedia.org/wiki/New_Zealand_National_Party"
W_5 = "https://en.wikipedia.org/wiki/Fifth_National_Government_of_New_Zealand"
W_6 = "https://en.wikipedia.org/wiki/Sixth_National_Government_of_New_Zealand"
PLEDGE = "https://www.1news.co.nz/2023/09/03/christopher-luxon-reveals-eight-point-pledge-to-voters/"
COAL = "https://www.1news.co.nz/2023/11/25/nationals-coalition-deals-which-policies-made-the-cut/"
RNZ100 = "https://www.rnz.co.nz/news/political/511135/100-day-plan-report-card-15-items-completion-up-for-debate"
BEE100 = "https://www.beehive.govt.nz/release/coalition-government-completes-100-day-plan"
TAX24 = "https://www.1news.co.nz/2024/05/30/budget-2024-tax-cuts-wont-cause-borrowing-or-inflation-willis/"
T_RNZ26 = "https://www.rnz.co.nz/news/politics/613970/pm-christopher-luxon-s-public-sector-targets-the-hits-and-misses-in-latest-update"
T_RNZ25 = "https://www.rnz.co.nz/news/politics/580654/how-many-of-the-government-s-9-key-targets-has-it-achieved"
T_DPMC = "https://www.dpmc.govt.nz/publications/government-targets-quarterly-reports-june-2026"
PREFU_RNZ = "https://www.rnz.co.nz/news/politics_election-2026/1647005/treasury-gives-willis-pre-election-boost-as-surplus-forecast-improves"
PREFU = "https://www.treasury.govt.nz/publications/efu/pre-election-economic-and-fiscal-update-2026"
COMMIT26 = "https://www.national.org.nz/news/260927-christopherluxon-1"
POLICIES = "parties/national/policies/README.md"

P = []
def add(promise, made, category, status, detail, sources):
    P.append({"promise": promise, "made": made, "category": category, "status": status,
              "detail": detail, "sources": sources})

# ===================== 2008 campaign (judged over 2008-11 and beyond) =====================
add("Not raise GST (\"National is not going to be raising GST\" - John Key, 2008 campaign)",
    "2008 election", "tax", "broken",
    "GST was raised from 12.5% to 15% on 1 October 2010 as part of a 'tax switch' that also cut income tax (top rate 38% -> 33%). Key argued he had been asked about raising GST to cover deficits and that the switch was revenue-neutral overall; Labour and commentators called it a broken promise. Verdict: broken on its plain wording, with the mitigating context that it was paired with income-tax cuts.",
    ["https://www.odt.co.nz/news/politics/key-ruled-out-gst-increase-2008",
     "https://scoop.co.nz/stories/PO1002/S00145/national-not-going-raise-gst-yeah-right.htm", W_5])
add("Keep the NZ Super eligibility age at 65 (Key: would resign rather than raise it)",
    "2008 election (reaffirmed 2011, 2014)", "superannuation", "kept",
    "The age stayed at 65 throughout Key's premiership (2008-2016). His successor Bill English explicitly declined to repeat the pledge in December 2016 and in March 2017 announced a plan to lift the age to 67 from 2040 (see 2017 entry). Kept for the terms in which it was made.",
    ["https://www.newshub.co.nz/home/politics/2016/12/bill-english-wont-stick-to-john-keys-super-pledge.html",
     "https://interest.co.nz/news/71071/governments-retirement-age-policy-65-more-issue-trust-now-rather-policy-english-says"])
add("Extend 90-day employment trial periods (first to small firms, then all employers)",
    "2008 election", "employment", "kept",
    "Employment Relations Amendment Act 2008 allowed firms with fewer than 20 staff to use 90-day trials; extended to all employers in 2010. (Labour later restricted it; National restored it for all employers in December 2023 - see 2023 entry.)",
    [W_5])

# ===================== 2011 campaign (judged 2011-14) =====================
add("Return the Crown accounts to an operating (OBEGAL) surplus in 2014/15",
    "2011 election", "fiscal", "kept",
    "Treasury's audited 2014/15 accounts (released 14 October 2015) showed an OBEGAL surplus of $414 million (0.2% of GDP) - narrowly, and better than the May 2015 Budget forecast of a deficit. Often remembered as missed because forecasts through 2015 showed a deficit, but the final result was a small surplus.",
    ["https://www.treasury.govt.nz/publications/year-end/financial-statements-government-new-zealand-year-ended-30-june-2015",
     "https://www.interest.co.nz/bonds/78132/treasury-reports-obegal-surplus-nz414-million-year-june-30-2015-first-budget-surplus-7"])
add("Partially sell state energy companies and Air NZ under a 'mixed ownership model' (sell up to 49% of Mighty River Power, Meridian, Genesis, Solid Energy; reduce Air NZ to 51%), raising $5-7 billion",
    "2011 election", "assets", "partially-kept",
    "Minority stakes in Mighty River Power (now Mercury), Meridian and Genesis were floated in 2013-14 and the Air NZ stake was reduced; Solid Energy was dropped because of its financial position. Proceeds were about $4.7 billion - below the $5-7 billion signalled. A citizens-initiated referendum in 2013 returned 67.3% opposed (45.1% turnout), which the government did not act on. The policy was clearly signalled before the 2011 election.",
    [W_NAT, "https://en.wikipedia.org/wiki/Mixed-ownership_model",
     "https://www.investsmart.com.au/investment-news/nz-asset-sales-raise-nz47bn/130446",
     "https://odt.co.nz/node/161143"])
add("170,000 new jobs by 2015 (Budget 2011 Treasury forecast that National campaigned on)",
    "2011 election", "economy", "partially-kept",
    "Progress lagged early (ODT reported 27,000 against a 92,000 forecast at one point). By November 2014 Economic Development Minister Steven Joyce told Parliament 159,000 jobs had been created since Budget 2011, 'around 12,000 to go'. No independent final tally for June 2015 was found, so this is graded partially kept on the government's own figures.",
    ["https://odt.co.nz/node/256834", "https://scoop.co.nz/stories/PA1411/S00375/pq-2-job-creation-progress.htm"])
add("Lead the rebuild of Christchurch after the 2010-11 earthquakes (CERA; 2012 Central City Recovery Plan with 17 anchor projects)",
    "2011 election", "infrastructure", "partially-kept",
    "Major Crown investment and several anchor projects delivered (bus interchange 2015, Tūranga library, justice & emergency precinct). Others ran years late and over budget: the Metro Sports Facility (Parakiore) targeted for Q1 2016 opened in December 2025 at roughly double its $246m budget; the stadium and Te Pae convention centre also faced years of delays (some delays fell under later governments).",
    ["https://oag.parliament.nz/2015/christchurch-projects/part2.htm",
     "https://www.odt.co.nz/star-news/star-christchurch/parakiore-set-open-after-decade-costly-delays", W_5])
add("Welfare reform: consolidate benefits and add work obligations",
    "2011 election", "welfare", "kept",
    "Seven main benefits were consolidated into three (Jobseeker Support, Sole Parent Support, Supported Living) with stronger work tests, implemented 2013.",
    [W_5])

# ===================== 2014 campaign (judged 2014-17) =====================
add("Hold a referendum on changing the New Zealand flag",
    "2014 election", "constitutional", "kept",
    "Two postal referendums were held (Nov-Dec 2015 and March 2016). Voters kept the existing flag 56.6% to 43.2%. The process cost about NZ$26 million. Key personally backed change; the promise (a vote) was kept, though the outcome he sought was rejected.",
    ["https://www.aljazeera.com/news/2016/3/24/new-zealand-rejects-alternate-flag-design-in-referendum",
     "https://www.csmonitor.com/World/Global-News/2016/0324/Why-New-Zealand-spent-17-million-to-change-its-flag-then-didn-t", W_5])
add("Free GP visits and prescriptions for children under 13",
    "2014 election", "health", "kept",
    "Implemented from July 2015.", [W_5, W_NAT])
add("Extend paid parental leave (to 16 then 18 weeks)",
    "2014 election (Budget 2014)", "family", "kept",
    "Paid parental leave was extended from 14 to 16 weeks (2015) and 18 weeks (2016). National later opposed Labour's faster extension to 26 weeks.",
    [W_NAT, W_5])
add("Modest personal income tax cuts later in the term 'if fiscal conditions allow'",
    "2014 election", "tax", "partially-kept",
    "Budget 2017's Family Incomes Package lifted the two lowest tax thresholds from 1 April 2018 and changed Working for Families. It was legislated but never took effect: the incoming Labour-led government repealed the threshold changes in December 2017. Graded partially kept - delivered in law, late in the term, but never paid.",
    ["https://www.interest.co.nz/news/88479/english-dangles-tax-cuts-front-party-faithful-while-trying-work-through-barclay-affair",
     "https://www.nzlii.org/nz/legis/repealed_act/tmfipa2017431/index.html"])
add("Auckland Housing Accord: 39,000 consented homes/sections in three years (2013-16)",
    "2013 accord (campaigned on in 2014)", "housing", "partially-kept",
    "Year 1 and 2 targets were met but year 3 fell short; the three-year total was about 37,500 (missed by 1,462, ~96% of target). Critics noted the accord measured consents, not affordability, which worsened sharply over the period.",
    ["https://amp.rnz.co.nz/article/bd934b98-9df0-4177-ac94-da764d13135a",
     "https://www.greaterauckland.org.nz/2017/05/09/auckland-housing-accord-sham-shalvation/"])

# ===================== 2017 campaign (National lost office) =====================
add("Raise the NZ Super age to 67, phased in from 2037 to 2040",
    "2017 election", "superannuation", "abandoned",
    "Announced by Bill English in March 2017. National won the most seats but lost office to a Labour-NZ First-Green arrangement, so the policy was never implemented. National re-proposed a later start (2044) in 2023, but dropped it in coalition talks with NZ First (see 2023 entry). Not a broken promise in government - untested.",
    ["https://www.newshub.co.nz/home/politics/2017/03/proposed-super-changes-reasonable-and-not-drastic-bill-english.html",
     "https://www.newshub.co.nz/home/politics/2019/08/national-s-superannuation-proposal-could-rule-out-winston-peters-as-a-coalition-partner.html"])
add("Ten new Roads of National Significance",
    "2017 election", "transport", "abandoned",
    "Never implemented because National lost office in 2017; revived in a different form as 17 Roads of National Significance in 2023-24 (see 2023 entry).",
    ["https://www.taxpayers.org.nz/bill_english_big_spending"])

# ===================== 2020 campaign (National lost office) =====================
add("Temporary income-tax cuts for 16 months as COVID-19 relief",
    "2020 election", "tax", "abandoned",
    "A late campaign addition (Collins had said in August 2020 there would be no tax cuts). National lost the election heavily (25.6%). Its next tax package (2023) was different and permanent.",
    ["https://www.1news.co.nz/2020/08/04/national-wont-put-taxes-up-but-it-also-wont-offer-tax-relief-judith-collins",
     "https://www.1news.co.nz/2020/09/22/tvnz-leaders-debate-judith-collins-and-jacinda-ardern-battle-on-wages-tax-and-poverty"])
add("$31 billion, 10-year infrastructure programme including a second Auckland harbour crossing",
    "2020 election", "infrastructure", "abandoned",
    "Untested - National lost the 2020 election. Elements (four-lane highways, RoNS) reappeared in the 2023 platform.",
    ["https://www.1news.co.nz/2020/07/16/judith-collins-says-its-time-for-boldness-as-she-pledges-31b-infrastructure-spend-including-second-auckland-harbour-crossing"])
add("Scrap the first-year fees-free tertiary policy",
    "2019-2020 (opposition)", "education", "abandoned",
    "National promised in 2019 to scrap Labour's first-year fees-free, and Collins said in 2020 'National will not have the fees free farce'. In 2023 National reversed this and promised to KEEP fees-free (see 2023 entry) - a notable U-turn.",
    ["https://www.1news.co.nz/2019/11/12/national-promises-to-bring-back-partnership-schools-scrap-first-year-fees-free-tertiary-model",
     "https://www.taxpayers.org.nz/national_s_u_turn"])

# ===================== 2023 campaign: pledge card (judged 2023-26) =====================
add("Pledge card: 'Lower inflation and grow the economy'",
    "2023 election (pledge card)", "economy", "partially-kept",
    "Annual CPI inflation fell from 5.6% (Sept 2023 quarter) to 2.2% by the September 2024 quarter - back inside the RBNZ 1-3% band for the first time since 2021 - but rose again to 4.1% and then 3.7% in the year to September 2026 (National attributes ~0.7 points to the 2026 Middle East oil shock). The economy was in recession through much of 2024; GDP grew 2.6% in the year to June 2026, and Treasury forecast unemployment to peak at 5.6% in 2026. Much of the disinflation was driven by RBNZ monetary policy and global factors.",
    [PLEDGE, "https://www.scoop.co.nz/stories/BU2410/S00287.htm", "https://www.national.org.nz/news/20261022-nicolawillis",
     "https://www.westpaciq.com.au/economics/2026/09/first-impressions-nz-gdp-jun-quarter-2026", PREFU_RNZ])
add("Pledge card: 'Let people keep more of what you earn' - personal income tax relief (raise thresholds, IETC, in-work tax credit), from 2024",
    "2023 election (pledge card; 'Back Pocket Boost')", "tax", "kept",
    "Budget 2024 delivered tax relief from 31 July 2024 averaging $3.7 billion a year, reaching ~3.5 million people (83%). Willis said the design 'aligns with the National Party tax plan with some adjustments to reflect coalition agreements'. Average-income households got up to $102 a fortnight.",
    [PLEDGE, TAX24])
add("'Up to $250 a fortnight' for an average-income family with children",
    "2023 election", "tax", "partially-kept",
    "The headline figure was a maximum. During the campaign National accepted that only about 3,000 households would get the full amount; the CTU later estimated fewer than 50 (closer to 30) did once the coalition package was finalised. Most households received far less (households with children averaged $78 a fortnight). Technically delivered as a maximum, but the framing overstated typical gains.",
    ["https://newshub.co.nz/home/politics/2023/10/election-2023-national-admits-only-3000-households-would-get-top-tax-relief-but-dismisses-claim-of-scam.html",
     "https://www.odt.co.nz/news/national/fewer-50-families-get-nationals-full-tax-package-says-ctu", TAX24])
add("Fund the tax package partly with a 15% tax on foreign buyers of homes over $2 million (repealing part of the foreign buyer ban), estimated at ~$740m a year",
    "2023 election", "tax", "abandoned",
    "Dropped in the National-NZ First coalition agreement (November 2023); NZ First and ACT both opposed it. Replaced by more IRD audit funding, the fees-free change, public service savings and other measures. In September 2025 the government instead proposed letting investor-visa holders buy homes worth $5m+.",
    [COAL, TAX24, W_6])
add("Tax relief 'fully funded' - no extra borrowing to pay for it",
    "2023 election / Budget 2024", "fiscal", "partially-kept",
    "Willis said the package was funded by savings and revenue measures and required no additional borrowing. Critics and analysts (Newshub's Jenna Lynch, Labour, the CTU, economists quoted by 1News) pointed out that Budget 2024 still increased overall borrowing by about $12 billion, so in aggregate the cuts were deficit-financed in the sense that money is fungible. Contested: the specific offsets were real, but the books remained in deficit.",
    [TAX24, "https://newshub.co.nz/home/politics/2024/05/budget-2024-jenna-lynch-analysis-the-as-advertised-budget-brings-tax-cuts-for-most-but-who-s-left-behind.html",
     "https://www.1news.co.nz/2024/04/11/the-maths-is-pretty-simple-scrutiny-on-govt-tax-cut-and-borrowing-plans"])
add("FamilyBoost: childcare tax credit of 25% of ECE fees, up to $75 a week, for families earning up to $180,000",
    "2023 election", "family", "partially-kept",
    "Introduced from 1 July 2024 as promised, but uptake was far below forecast: $50.5m reached 60,300 households in year one against a $131m budget, and only 153 families received the maximum in all four quarters. The government blamed IRD eligibility estimates and in July 2025 raised it to 40% of fees, up to $120 a week, with an income cap of $229,000. Willis maintained every eligible applicant got what was advertised.",
    ["https://www.ird.govt.nz/about-us/publications/annual-corporate-reports/annual-report/annual-report-2025/implementing-the-governments-priorities/implementing-budget-2024-initiatives/budget-2024-major-spending-decisions",
     "https://www.newstalkzb.co.nz/news/politics/familyboost-just-153-families-getting-maximum-75-weekly-childcare-tax-credit",
     "https://www.1news.co.nz/2025/07/07/boost-to-govts-flagship-childcare-rebates-after-uptake-issues"])
add("Return the books to surplus in 2026/27",
    "2023 election (fiscal plan)", "fiscal", "broken",
    "National's 2023 fiscal plan, based on PREFU 2023, aimed for an OBEGAL surplus in 2026/27. Successive Treasury updates pushed it out (to 2029/30 in HYEFU 2024 and to 2030 on OBEGAL in December 2025); the government adopted a new 'OBEGALx' measure (excluding ACC) and now targets a 2028/29 OBEGALx surplus. PREFU 2026 forecasts an OBEGALx deficit of $6.8b in 2026/27. Weak growth and revenue were major causes, but the target date was missed.",
    ["https://www.1news.co.nz/2025/12/16/govt-pushes-out-surplus-expectations-again/",
     "https://thespinoff.co.nz/business/18-12-2024/the-very-long-road-to-fiscal-recovery", PREFU_RNZ, PREFU])
add("Pledge card: 'Build infrastructure' - including Roads of National Significance",
    "2023 election (pledge card)", "infrastructure", "in-progress",
    "The 2024 National Land Transport Programme committed $32.9b including 17 RoNS. By July 2026 four RoNS were under construction (e.g. Hawke's Bay Expressway from November 2025) and six were expected by early 2027, but five were moved to a 'slow lane' with no construction timeline (incl. East West Link, Mill Road, Petone-Grenada). Also: National Infrastructure Agency created; a National Infrastructure Plan published February 2026.",
    [PLEDGE, W_6, "https://www.1news.co.nz/2026/07/09/govt-pulls-flagship-roading-projects-into-the-slow-lane/",
     "https://www.national.org.nz/news/20260709-honchrisbishop"])
add("Pledge card: 'Restore law and order'",
    "2023 election (pledge card)", "justice", "kept",
    "Gang-patch ban, consorting/dispersal powers, three strikes, Youth Serious Offender category and military-style academies all legislated. The government targets for victims of violent crime and serious youth offending were both met ahead of their 2030 deadlines (officials warn the victims survey is volatile). Note ram raids peaked in 2022 and were already falling before the change of government.",
    [PLEDGE, T_RNZ26, T_RNZ25,
     "https://newshub.co.nz/home/new-zealand/2023/11/ram-raids-down-from-2022-peak-still-averaging-over-one-per-day-new-data.html"])
add("Pledge card: 'Lift school achievement' (government target: 80% of Year 8 students at or above curriculum level by 2030)",
    "2023 election (pledge card)", "education", "in-progress",
    "Policy inputs delivered (an hour a day of reading, writing and maths; structured literacy from 2025; phone ban; maths action plan). But the achievement target was rated 'at risk' in the June 2026 report, with reading slipping slightly; the attendance target (80% present >90% of the time) was at 68% in Term 1 2026, rated 'probable'. National cites improved PAT maths data.",
    [PLEDGE, T_RNZ26, "https://www.national.org.nz/news/20261021-christopherluxon"])
add("Pledge card: 'Cut health waiting times' (targets: 95% of ED patients within 6 hours; 95% of elective patients treated within 4 months)",
    "2023 election (pledge card)", "health", "in-progress",
    "As at the June 2026 report, 74.2% of ED patients were seen within six hours and 64.5% of elective patients within four months - well short of 95% but rated 'feasible' by 2030. Elective performance improved from 57.3% in mid-2025. Officials had warned the ED target might not be achievable in the short term.",
    [PLEDGE, T_RNZ26, T_RNZ25])
add("Pledge card: 'Support seniors' - keep universal super and index it",
    "2023 election (pledge card)", "superannuation", "kept",
    "NZ Super remained universal and was uprated each year; National says couples are $180 a fortnight better off and the full rates rebate was extended to SuperGold card holders. (National's separate plan to raise the age - below - was dropped.)",
    [PLEDGE, "https://www.national.org.nz/news/20261022-retirement"])
add("Pledge card: 'Deliver Net Zero Carbon by 2050'",
    "2023 election (pledge card)", "climate", "in-progress",
    "The 2050 net-zero target for long-lived gases was kept and the first two emissions budgets (2022-25 and 2026-30) were reported on track in 2026. But the government cut the 2050 biogenic methane target from 24-47% to 14-24% below 2017 levels (October 2025), kept agriculture out of the ETS, reversed the offshore oil and gas exploration ban and passed a law blocking climate tort suits - which critics argue weakens the long-run path.",
    [PLEDGE, T_RNZ26, "https://www.1news.co.nz/2025/10/12/govt-to-lower-methane-reduction-target-rules-out-methane-taxes", W_6])

# ===================== 2023 campaign: specific policies =====================
add("100-day plan: 49 actions within the first 100 days",
    "2023 coalition (announced 29 Nov 2023)", "governance", "kept",
    "The government declared all 49 actions complete on 8 March 2024. RNZ's analysis judged 15 completions 'up for debate' (21 items only promised to 'begin work'; some bills were merely introduced), while four laws were passed under urgency with no public input. Substantively delivered on its own terms; the wording was generous.",
    [BEE100, RNZ100])
add("Repeal Fair Pay Agreements by Christmas 2023",
    "2023 election", "employment", "kept",
    "Fair Pay Agreements Act 2022 repealed under urgency on 14 December 2023.", [W_6, COAL])
add("Restore 90-day trial periods for all employers",
    "2023 election", "employment", "kept", "Passed 21 December 2023.", [W_6])
add("Return the Reserve Bank to a single inflation mandate",
    "2023 election", "economy", "kept", "Passed 13 December 2023.", [W_6])
add("Repeal Three Waters and replace it with locally controlled 'Local Water Done Well'",
    "2023 election", "local government", "kept",
    "Water Services Entities Act repealed under urgency on 14 February 2024; Local Water Done Well laws passed August 2024 and August 2025. The 2024 law also removed the requirement for the water regulator to consider Te Mana o te Wai when setting wastewater standards.",
    [W_6])
add("Repeal and replace the RMA (repeal Labour's Natural and Built Environment and Spatial Planning Acts by Christmas 2023, then new laws)",
    "2023 election", "environment & planning", "kept",
    "Also promised by Judith Collins in 2020 (Environmental Standards Act + Urban Planning Act; National lost that election). Labour's replacement Acts repealed 20 December 2023. Planning Act 2026 and Natural Environment Act 2026 passed 22 September 2026 (Labour supported the first readings). The new system is not expected to be fully in effect until about 2029.",
    [W_6])
add("Fast-track consenting for regionally and nationally significant projects",
    "2023 election", "environment & planning", "kept",
    "Fast-track Approvals Act passed 17 December 2024 after controversy over ministerial power (later amended so a panel decides). Projects approved from 2025, including Takitimu North Link Stage 2. Amended in 2025 to help new supermarket entrants.",
    [W_6, "https://www.1news.co.nz/2026/07/09/govt-pulls-flagship-roading-projects-into-the-slow-lane/"])
add("Restore mortgage-interest deductibility for residential landlords (National: phased over three years)",
    "2023 election", "housing/tax", "kept",
    "Accelerated in coalition at ACT's request: 80% from 1 April 2024 and 100% from 1 April 2025 (allocation increased from $2.1b to $2.9b).",
    [W_6, COAL])
add("Cut the bright-line test for residential property back to two years",
    "2023 election", "housing/tax", "kept", "Legislated March 2024, effective 1 July 2024.", [W_6])
add("Ban gang patches in public, give police dispersal and non-consorting powers, make gang membership an aggravating factor in sentencing",
    "2023 election", "justice", "kept",
    "Gangs Act 2024 passed 19 September 2024; the public-insignia ban took effect 21 November 2024 (up to six months' jail or a $5,000 fine). RNZ's 100-day check had noted the bill was then only at select committee.",
    ["https://www.1news.co.nz/2024/09/19/gang-patch-legislation-passed-into-law/",
     "https://www.1news.co.nz/2024/11/21/nzs-new-gang-laws-come-into-force-what-you-need-to-know/"])
add("Youth Serious Offender category and military-style academies for the worst young offenders",
    "2023 election", "justice", "kept",
    "A pilot boot camp ran from July 2024; legislation enabling the Youth Court to send offenders to Military Style Academies passed 17 September 2026. Serious/persistent youth offending fell below the government's 900 target (829 by June 2026).",
    [W_6, T_RNZ26])
add("End taxpayer funding for 'section 27' cultural reports at sentencing",
    "2023 election", "justice", "kept", "Passed under urgency on 6 March 2024.", [W_6])
add("Cancel Auckland light rail",
    "2023 election", "transport", "kept",
    "Confirmed 14 January 2024 (projected cost $29.2b; $228m already spent).", [W_6])
add("Scrap the Auckland Regional Fuel Tax",
    "2023 election", "transport", "kept",
    "Included in the 100-day plan; the tax ended on 30 June 2024.", [W_6, RNZ100])
add("Repeal the Clean Car Discount ('ute tax')",
    "2023 election", "transport", "kept", "Repealed under urgency 14 December 2023.", [W_6])
add("Reverse blanket speed-limit reductions",
    "2023 election", "transport", "kept",
    "Setting of Speed Limits rule replaced; in January 2025 limits were reversed on 38 state-highway sections with consultation on 49 more.", [W_6])
add("Reverse the ban on offshore oil and gas exploration",
    "2023 election", "energy", "kept",
    "Crown Minerals Amendment Act passed 31 July 2025; first new exploration permit granted 29 July 2026.", [W_6])
add("Keep agriculture out of the ETS and price farm emissions at farm level by 2030",
    "2023 election", "climate/agriculture", "partially-kept",
    "Agriculture formally excluded from the ETS (June 2024). (The farm-level-pricing-by-2030 wording is National's 2023 agriculture policy as recalled from campaign coverage; this archive did not re-fetch the original document.) Rather than pricing farm emissions, the government in October 2025 ruled out any methane tax/pricing and lowered the 2050 methane target - more farmer-friendly than the 2023 pledge to price at farm level by 2030.",
    [W_6, "https://www.1news.co.nz/2025/10/12/govt-to-lower-methane-reduction-target-rules-out-methane-taxes"])
add("Replace 'one-in, two-out' farm regulation rule (cut two farming regulations for every new one)",
    "2023 election", "agriculture", "abandoned",
    "Replaced in the coalition agreements by a broader commitment to cut farm regulation and a cross-government regulatory review.", [COAL])
add("Raise the NZ Super eligibility age from 65 to 67, starting in 2044",
    "2023 election", "superannuation", "abandoned",
    "Dropped in coalition: NZ First's agreement keeps the age at 65. National's 2026 retirement plan (22 Oct 2026) does not mention raising the age, though Luxon said in November 2025 it remained 'on the cards'.",
    [COAL, "https://thespinoff.co.nz/politics/24-11-2025/fixing-the-basics-sticking-with-luxon-the-national-partys-2026-plan",
     "https://www.national.org.nz/news/20261022-retirement"])
add("Keep the fees-free tertiary scheme (first year free) and not means-test it",
    "2023 election", "education", "broken",
    "National reversed its 2020 position and promised to keep fees-free. The coalition agreement with NZ First shifted it to the final year from 2025 (savings used for tax relief), and Budget 2026 scrapped final-year fees-free entirely (confirmed 8 May 2026).",
    ["https://newshub.co.nz/home/politics/2023/08/election-2023-national-would-keep-fees-free-policy-wouldn-t-means-test-despite-reckons-from-candidate.html",
     COAL, W_6])
add("Fund 13 additional cancer treatments (≈$280m over four years), paid for by reinstating the $5 prescription fee",
    "2023 election", "health", "kept",
    "Budget 2024 reinstated the $5 co-payment (from July 2024, with exemptions for under-14s, over-65s and Community Services Card holders) but contained no money for the cancer drugs - the government blamed a $1.77b Pharmac 'fiscal cliff'. After weeks of backlash it announced $604m over four years on 24 June 2024 for 54 medicines including 26 cancer treatments, and said the 13-drug promise would be met. Kept, but late and only after a public row; National now claims 33 extra cancer medicines funded.",
    ["https://www.1news.co.nz/2024/05/30/budget-2024-5-prescription-fee-back-in-weeks-with-some-exceptions/",
     "https://www.1news.co.nz/2024/06/04/luxon-promises-cancer-drug-announcement-before-christmas",
     "https://nzdoctor.co.nz/node/32100", W_6])
add("Extend free breast screening from 69 to 74",
    "2023 election", "health", "in-progress",
    "Budget 2024 provided $31.2m. Pilot in Nelson Marlborough from late 2024; national roll-out began 1 October 2025, widening each October so that all women up to 74 are covered by the end of 2029 - later than first signalled.",
    ["https://www.tewhatuora.govt.nz/health-services-and-programmes/breastscreen-aotearoa/extending-the-age-for-free-breast-screening",
     "https://newshub.co.nz/home/new-zealand/2024/06/government-s-age-extension-of-free-breast-cancer-screening-delayed.html"])
add("Build a third medical school at the University of Waikato (National: $280m Crown funding, opening 2027 with 120 places)",
    "2023 election", "health", "in-progress",
    "ACT's coalition deal required a full cost-benefit analysis first. Cabinet approved it on 21 July 2025 with Crown funding of $82.85m (the university and philanthropists provide >$150m); ground was broken December 2025; first 120 students expected in 2028 - a year later than promised and with a much smaller Crown contribution.",
    [COAL, "https://www.1news.co.nz/2025/07/21/govt-gives-green-light-and-83m-for-waikato-medical-school",
     "https://www.national.org.nz/news/20251205-hon-simeon-brown-ground-broken-on-waikato-medical-school"])
add("Dunedin Hospital: reverse Labour's cuts to the new build (restore 23 inpatient beds, two operating theatres, a PET scanner)",
    "2023 election", "health", "broken",
    "In September 2024 ministers said rising costs (~$3b) meant the project would be scaled back or the old hospital redeveloped; Luxon then committed to building it for $1.9 billion. Construction of the inpatient building later resumed. Nurses and local campaigners called it a betrayal; the government says it is still building 'a great hospital'. The specific 2023 pledge to restore the cut capacity was not honoured as made.",
    ["https://www.odt.co.nz/news/dunedin/national-pledges-dunedin-hospital-budget-boost",
     "https://kaitiaki.org.nz/article/liar-liar-pants-on-fire-nurses-confront-prime-minister-over-dunedin-hospital-betrayal/",
     "https://www.newstalkzb.co.nz/news/politics/dunedin-hospital-construction-resumes-on-project-mired-by-delays-cost-blowouts-and-protests"])
add("Disestablish Te Aka Whai Ora (the Māori Health Authority)",
    "2023 election", "health", "kept", "Legislation passed under urgency on 28 February 2024.", [W_6])
add("'Back to basics' in schools: an hour a day each of reading, writing and maths",
    "2023 election", "education", "kept", "Required in schools from 2024 (coalition agreement; Wikipedia's policy summary).", [COAL, W_6])
add("Ban cellphones in schools",
    "2023 election", "education", "kept", "In force from 29 April 2024 (100-day plan item).", [W_6])
add("Structured literacy and a new knowledge-rich curriculum",
    "2023 election", "education", "kept",
    "Structured literacy required in all state schools from Term 1 2025; Reading Recovery ended; new maths curriculum from 2025. Unions warned about pace of change.", [W_6])
add("Disestablish Te Pūkenga and restore regional polytechnics",
    "2023 election", "education", "in-progress",
    "Ten polytechnics regained autonomy from 1 January 2026; Te Pūkenga to be dissolved by late 2026 with five polytechnics' futures decided in 2026.", [W_6])
add("Cut public service back-office spending and consultants without touching the frontline",
    "2023 election", "public service", "partially-kept",
    "Agencies were told to find 6.5-7.5% savings in 2024. Public Service Commission data: FTEs fell from a peak of 65,699 (Dec 2023) to 62,654 (June 2025, -4.6%) and then rose again to 63,912 (June 2026) as funding went to frontline roles. Consultant/contractor spending fell. Critics and the PSA say cuts reached services (e.g. disability support, some health roles). In May 2026 the government announced a further 8,700-FTE reduction by mid-2029.",
    ["https://www.publicservice.govt.nz/data/workforce-data/public-sector-composition/workforce-size",
     "https://newstalkzb.co.nz/news/politics/prime-minister-christopher-luxon-defends-public-sector-job-cuts-govt-wants-more-medical-doctors-not-spin-doctors",
     "https://www.1news.co.nz/2026/05/19/union-says-govt-cuts-cruel-and-deep-election-year-clash-over-job-losses/"])
add("Nine public-sector 'Government Targets' to 2030 (announced April 2024)",
    "2024 (in government)", "governance", "in-progress",
    "June 2026 report: met early - emergency housing (471 households vs 800 target), victims of violent crime, serious youth offending; on track - emissions budgets; probable - school attendance; feasible but well short - ED and elective waits; at risk - Jobseeker numbers (215,200 vs 140,000) and student achievement. Deadline 2030.",
    ["https://www.beehive.govt.nz/release/prime-minister-launches-government-targets", T_DPMC, T_RNZ26])
add("Halve child poverty (material hardship to 6%) by 2028 - Luxon recommitted during the 2023 campaign",
    "2023 election", "social", "in-progress",
    "Off track. Interim 2026/27 material-hardship target was loosened to 11% in June 2024 (minister rejected officials' advice on what it would take). Stats NZ figures for the year to June 2025 showed 14.3% of children (≈169,300) in material hardship, up from 10.6% in 2022; the Children's Commissioner and CPAG say the 2028 target will not be met. Deadline not yet passed.",
    ["https://www.cpag.org.nz/media-releases/cpag-pm-luxon-on-track-to-break-election-promise-on-child-poverty",
     "https://rnz.co.nz/news/political/523167/minister-defends-lowered-child-poverty-targets-as-achievable",
     "https://www.1news.co.nz/2026/02/26/unacceptable-childrens-commissioner-says-child-poverty-progress-has-stalled"])
add("Reduce the number of households in emergency (motel) housing",
    "2023 election", "housing", "kept",
    "Government target of a 75% cut (to 800 or fewer) by 2030 was met early: 471 households in the June 2026 report. Eligibility was also tightened from August 2024.", [T_RNZ26, W_6])
add("Train 500 new frontline police within two years (by 27 November 2025)",
    "2023 coalition agreement (NZ First policy adopted by the government)", "justice", "broken",
    "Deadline missed: by mid-2025 only a small net increase had occurred; the date was pushed to June, then August, then September 2026. The government says it will still deliver the 500 'this term'.",
    ["https://www.1news.co.nz/2025/05/13/govt-concedes-itll-likely-miss-november-target-for-500-new-police",
     "https://www.1news.co.nz/2025/11/18/govts-target-for-500-new-police-officers-bumped-out-again/"])
add("Support ACT's Treaty Principles Bill only to select committee (not into law)",
    "2023 coalition agreement", "Treaty/constitutional", "kept",
    "National voted for the first reading (14 November 2024) and against the second reading, where the bill was defeated 112-11 on 10 April 2025.",
    ["https://en.wikipedia.org/wiki/Treaty_Principles_Bill", W_6])
add("Restore local referendums on Māori wards",
    "2023 coalition agreement", "local government", "kept",
    "Law passed 30 July 2024; referendums held with the October 2025 local elections (24 councils voted to remove wards, 18 to keep them).", [W_6])
add("Hold a referendum on a four-year parliamentary term at the 2026 election",
    "2023 coalition agreement / 2024 announcement", "constitutional", "abandoned",
    "Cabinet had set aside $25m (August 2025), but on 18 February 2026 the government dropped the referendum; the bill will not progress this term.", [W_6])
add("Reverse the ban on live animal exports by sea",
    "2023 coalition agreement (National & ACT pledge)", "agriculture", "abandoned",
    "On 10 March 2026 Associate Agriculture Minister Andrew Hoggard said it would not progress this term because there was no Cabinet consensus.", [W_6])
add("Find a cheaper replacement for the Interislander ferries after declining KiwiRail's $1.47b funding request (iReX cancelled December 2023)",
    "December 2023 (in government)", "infrastructure", "in-progress",
    "Cancelling iReX cost $671m in total ($222m to Hyundai Mipo, settled in August 2025 for less than the $300m provisioned). Ferry Holdings Ltd procured two new rail-enabled ferries due in service around 2029; the government puts total cost (ferries + port works) at about US$1.1b. Supporters say it avoided a ~$4b blowout; critics point to sunk costs and years of delay for new ships.",
    ["https://www.1news.co.nz/2025/08/15/how-much-it-cost-to-cancel-irex-ferry-contract-671-million/",
     "https://maritime-executive.com/corporate/interislander-signs-up-for-a-new-era-of-cook-strait-ferries", W_6])

# ===================== 2026 campaign (not yet due) =====================
for pr, cat, src in [
    ("No new taxes in the next term (including no capital gains tax)", "tax", [COMMIT26, POLICIES]),
    ("Return to an OBEGALx surplus in 2028/29, keep net core Crown debt below 40% of GDP and spending towards 30% of GDP", "fiscal", [POLICIES, PREFU_RNZ]),
    ("Make KiwiSaver compulsory (from 1 July 2028), lift contributions toward 12% by 2032 and pay a $1,500 'Baby Boost' at birth", "superannuation & savings", [COMMIT26, "https://www.national.org.nz/news/20261023-young-adults", POLICIES]),
    ("Extend paid parental leave from 26 to 30 weeks (by 2029)", "family", [COMMIT26, POLICIES]),
    ("Replace NCEA with new qualifications; keep students in school to the end of Year 11", "education", [COMMIT26, "https://www.national.org.nz/news/20261021-christopherluxon"]),
    ("Ban under-16s from social media", "education/online safety", ["https://www.national.org.nz/news/20261021-christopherluxon", W_6]),
    ("Cut the student loan repayment rate (12% to 10%) for borrowers living in NZ", "education", ["https://www.national.org.nz/news/20261023-young-adults", POLICIES]),
    ("Widen 5%-deposit First Home Loans", "housing", ["https://www.national.org.nz/news/20261023-young-adults", POLICIES]),
    ("A better deal at the supermarket: pursue structural separation of Foodstuffs", "economy", [COMMIT26, POLICIES]),
    ("Faster healthcare and more medicines (a further $604m for Pharmac; breast screening to 74 and bowel screening from 50 by 2029)", "health", [COMMIT26, POLICIES]),
    ("Seniors: ring-fence 20% of the Housing Flexible Fund for seniors' housing, 0800 Seniors helpline, employer KiwiSaver contributions for over-65s from 1 July 2027", "seniors", ["https://www.national.org.nz/news/20261022-retirement"]),
]:
    add(pr, "2026 election", cat, "not-yet-due", "Election is on 7 November 2026; commitment is for the 2026-29 term. See the 2026 policies page for full text.", src)

out = os.path.join(ROOT, 'data', 'promises', 'national.json')
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(P, open(out, 'w'), indent=2, ensure_ascii=False)

# ---------------- scorecard ----------------
def term(m):
    for k in ('2026',):
        if m.startswith(k): return '2026 (not yet due)'
    for k, v in [('2008', '2008-11 (Key, govt)'), ('2011', '2011-14 (Key, govt)'), ('2013', '2014-17 (Key/English, govt)'),
                 ('2014', '2014-17 (Key/English, govt)'), ('2017', '2017 (lost office)'), ('2019', '2017-23 (opposition)'),
                 ('2020', '2020 (opposition)')]:
        if m.startswith(k): return v
    return '2023-26 (Luxon, govt)'
c = collections.Counter(p['status'] for p in P)
print(len(P), 'promises', dict(c))
bt = collections.defaultdict(collections.Counter)
for p in P: bt[term(p['made'])][p['status']] += 1
for t in sorted(bt): print(t, dict(bt[t]), sum(bt[t].values()))
