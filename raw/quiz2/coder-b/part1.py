# Coder B data, part 1: statements + National, Labour, Green
def c(pos, ev, url, tier, conf):
    return {"position": pos, "evidence": ev, "source_url": url, "tier": tier, "confidence": conf}

STATEMENTS = [
 ("E1","The government should take active steps to reduce the gap between high and low incomes, even if that means higher taxes for some people.","+A"),
 ("E2","Lower taxes do more good for New Zealand than more government spending, even if it means fewer public services.","+B"),
 ("E3","Gains people make from rising property and asset values should be taxed in the same way as income from work.","+A"),
 ("E4","Services like electricity, housing and transport are delivered better by private businesses competing than by government ownership.","+B"),
 ("E5","People receiving benefits should face firm obligations and penalties for not meeting them, even if some households end up with less.","+B"),
 ("E6","Workers' pay and conditions are best protected by unions bargaining for whole industries, even if that raises costs for employers.","+A"),
 ("E7","Keeping government debt low should take priority over spending more on health and education right now.","+B"),
 ("S1","People who commit serious crimes should be given longer prison sentences, even if it means more people in prison for longer at public expense.","+B"),
 ("S2","Police should have more power to stop, search and move people on in public places, even if that limits some civil liberties.","+B"),
 ("S3","Adults should be free to make their own choices about things like drug use, even if others consider those choices harmful or wrong.","+A"),
 ("S4","Schools and public institutions should reflect changing social attitudes about gender, sexuality and family, even if some parents and communities object.","+A"),
 ("S5","People should be free to say what they think in public and online, even if others find it offensive or harmful.","+A"),
 ("S6","Young people who offend should face tougher consequences rather than mainly being supported through welfare and youth services.","+B"),
 ("T1","Te Tiriti o Waitangi should continue to shape our laws and how public services are run, even if that means some decisions are made differently for Māori.","+A"),
 ("T2","Government should treat everyone the same regardless of ancestry, so there should be no seats, wards or services set aside specifically for Māori.","+B"),
 ("T3","Māori should share decision-making with the Crown over natural resources such as land and water, even if that makes some decisions slower.","+A"),
 ("T4","Parliament, rather than the courts or the Waitangi Tribunal, should decide what the Treaty means in law.","+B"),
 ("T5","Te reo Māori and tikanga should have a bigger place in public life, such as in schools, government agencies and official names, even if some New Zealanders do not want this.","+A"),
 ("T6","The Treaty settlement process has gone far enough and should be brought to a close.","+B"),
 ("V1","We should do more to protect the environment, even if that means less economic growth.","+A"),
 ("V2","Farmers and industry should pay for the greenhouse gases they emit, even if that raises food and fuel prices.","+A"),
 ("V3","Big infrastructure, mining and energy projects should be able to go ahead faster, even if environmental checks are reduced.","+B"),
 ("V4","New Zealand should keep its international climate commitments even if other countries do less and it costs New Zealand economically.","+A"),
 ("V5","Extracting more minerals, oil and gas from New Zealand's land and waters is a good way to pay for public services.","+B"),
 ("O1","New Zealand should let in fewer immigrants, even if some businesses cannot find the workers they need.","+B"),
 ("O2","New migrants should wait several years before they can receive benefits and other public support.","+B"),
 ("O3","New Zealand should keep an independent foreign policy rather than tying itself more closely to traditional military allies, even if that means less protection.","+A"),
 ("D1","Major national decisions should be put to the public in binding referendums rather than decided by Parliament, even if that slows things down.","+A"),
 ("D2","Only individual voters on the electoral roll should be allowed to donate to political parties, even if parties then have less money to campaign.","+A"),
 ("D3","Local councils should be free to make their own decisions, even if rates and rules then differ from place to place, rather than central government overriding them.","+A"),
]

# shared vote sources
TPB = "https://en.wikipedia.org/wiki/Treaty_Principles_Bill"
WARDS = "https://en.wikipedia.org/wiki/Local_Government_(Electoral_Legislation_and_M%C4%81ori_Wards_and_M%C4%81ori_Constituencies)_Amendment_Act_2024"
FTA = "https://en.wikipedia.org/wiki/Fast-track_Approvals_Act_2024"
GANGS = "https://en.wikipedia.org/wiki/Gangs_Act_2024"
THREE = "https://en.wikipedia.org/wiki/Sentencing_(Reinstating_Three_Strikes)_Amendment_Act_2024"
CMA = "https://en.wikipedia.org/wiki/Crown_Minerals_Amendment_Act_2025"
MOVEON = "https://www.1news.co.nz/2026/09/18/controversial-move-on-legislation-passes-final-reading-in-parliament/"
BOOT = "https://www.odt.co.nz/news/national/bootcamps-bill-kicked-over-line-tsi466l0"
SSAB = "https://www.nzdoctor.co.nz/article/undoctored/social-security-amendment-bill-passes-law"
ENGBILL = "https://en.wikipedia.org/wiki/English_Language_Bill"
PUBERTY = "https://www.nbcnews.com/world/asia/new-zealand-halts-new-puberty-blockers-young-transgender-people-rcna244925"
GP = "https://www.greenpeace.org/aotearoa/action-hub/election-2026-environment-scorecards/"
CTU = "https://union.org.nz/election-scorecards-26/"
GREYPOWER = "https://www.greypower.co.nz/election-2026"

NAT_FISCAL = "https://assets.national.org.nz/web/prod/National%27s%20Fiscal%20Plan.pdf?v=1791759269"
NAT_NONEWTAX = "https://www.national.org.nz/news/260823-no-new-taxes-under-national"
NAT_WELFARE = "https://assets.national.org.nz/web/prod/A%20firm,%20fair%20and%20affordable%20welfare%20system.pdf?v=1791407915"
NAT_SMB = "https://assets.national.org.nz/web/prod/National%E2%80%99s%2047-point%20plan%20to%20support%20Small%20Businesses.pdf?v=1791324870"
NAT_RATES = "https://www.national.org.nz/policies/rates-capping"
NAT_FARM = "https://assets.national.org.nz/web/prod/Growing%20More%20to%20Feed%20the%20World.pdf?v=1792108210"
NAT_LAUNCH = "https://www.national.org.nz/news/260927-christopherluxon"
NAT_CONF = "https://www.national.org.nz/news/20260621-rthonchristopherluxon"
NAT_BISHOP = "https://www.national.org.nz/news/20260814-honchrisbishop-honsimonwatts"
NAT_BRR = "https://www.national.org.nz/news/20260809-honnicolawillis"

national = {
 "E1": c(-1, "No 2026 text on narrowing the income gap; National's fiscal plan rules out 'new taxes' and attacks Labour/Greens/TPM 'nine new taxes' as punishing 'Kiwis who do the right thing and save and invest' (Fiscal Plan, Oct 2026). Inference from explicit general principle (no higher taxes) -> disagree; recorded as inference.", NAT_FISCAL, 1, "low"),
 "E2": c(1, "Fiscal Plan (Oct 2026): 'not impose new taxes', 'show ongoing restraint so that overall government expenditure comes down towards 30% of GDP', 'right-sizing government'; but also pledges to 'continue investing in health, schools, law and order' - so a qualified preference for lower tax/smaller state.", NAT_FISCAL, 1, "medium"),
 "E3": c(-2, "'No new taxes, including no capital gains tax' (Fiscal Plan, Oct 2026); Luxon 21 Jun 2026: 'not smashing ambition with a Capital Gains Tax'; 'New Zealand's lack of a capital gains tax is a real competitive advantage' (23 Aug 2026).", NAT_NONEWTAX, 1, "high"),
 "E4": c(1, "Luxon (2025) said National is open to asset sales/'asset recycling' after the 2026 election and ruled out only state-house sales; prison redevelopment via public-private partnership (South Island Plan 2026); electricity policy opens transmission to competition. No general manifesto statement that private delivery is better, so qualified agree.", "https://www.interest.co.nz/public-policy/137617/battle-lines-drawn-asset-sales-parties-set-out-starkly-different-views", 4, "medium"),
 "E5": c(2, "'A firm, fair and affordable welfare system' (Oct 2026): lower Jobseeker rate after 2 of 3 years on benefit, drug testing with sanctions for non-compliance, 26-week stand-down for repeated voluntary unemployment; expanded Traffic Light sanctions in government (Social Security Amendment Act 2025).", NAT_WELFARE, 1, "high"),
 "E6": c(-2, "Repealed Fair Pay Agreements Act Dec 2023 (all National MPs voted for repeal; NZCTU scorecard Oct 2026 records National 'No' to restoring FPAs); 2026 small-business plan would require minimum employee support before collective bargaining can start.", NAT_SMB, 1, "high"),
 "E7": c(1, "Budget Responsibility Rules (9 Aug 2026): 'prioritising a return to surplus in 2028/29', 'bending debt down below 40% of GDP'; 'books in surplus so we don't saddle our kids with more debt'. Also commits to continuing health/education investment, so qualified agree.", NAT_BRR, 1, "medium"),
 "S1": c(2, "Voted for Sentencing (Reinstating Three Strikes) Amendment Act (3rd reading 13 Dec 2024) and sentencing-discount caps; campaign launch 27 Sep 2026: 'locking offenders up for longer to keep our community safe'; 240 extra prison beds at Christchurch Men's Prison.", NAT_LAUNCH, 2, "high"),
 "S2": c(2, "Government bill creating police move-on orders passed final reading 18 Sep 2026 (Justice Minister Goldsmith); Gangs Act 2024 (patch ban, dispersal notices) passed 68-55 with National support.", MOVEON, 2, "high"),
 "S3": c(-1, "Luxon (7 Oct 2022): National 'won't decriminalise cannabis'; 2026 welfare policy introduces drug testing of beneficiaries with sanctions. No newer general statement found; older statement used as nothing newer exists.", "https://www.1news.co.nz/2022/10/07/national-wont-decriminalise-cannabis-if-elected-luxon/", 4, "medium"),
 "S4": c(-1, "Health Minister Simeon Brown (National) halted new puberty-blocker prescriptions from 19 Dec 2025 (announced 19 Nov 2025); Education Minister Stanford's 2025 relationships and sexuality framework emphasises parental consultation/opt-out. Government actions attributable to National ministers; flagged.", PUBERTY, 5, "medium"),
 "S5": c(1, "In government National passed the Education and Training Amendment Act 2025 requiring universities to protect free speech and dropped Labour's hate-speech law work (ACT coalition commitments); but Luxon's 2026 policy bans under-16s from social media. Coalition-driven, qualified agree, flagged.", "https://www.national.org.nz/news/260824-christopherluxon", 5, "low"),
 "S6": c(2, "Oranga Tamariki (Responding to Serious Youth Offending) Amendment Bill creating Young Serious Offender declarations and military-style academies passed under urgency with National's votes; National's 2026 law-and-order material claims 'youth offending down 26%' and ram raids down 85% as results of tougher approach.", BOOT, 2, "high"),
 "T1": c(-1, "Campaign launch 27 Sep 2026: health minister 'with the guts to end Labour's obsession with co-governance'; coalition policy of targeting services 'by need not race'; Treaty clauses review (coalition commitment). National voted against the Treaty Principles Bill (10 Apr 2025), so not strongly disagree.", NAT_LAUNCH, 4, "medium"),
 "T2": c(0, "Mixed: supported 2024 law restoring binding polls on Māori wards and ended the Māori Health Authority ('need not race'), but Luxon has repeatedly ruled out abolishing or holding a referendum on the Māori seats (rejected NZ First's Feb 2026 referendum call). Both sides emphasised -> argued neutral.", WARDS, 2, "medium"),
 "T3": c(-2, "Repealed Three Waters co-governance (Water Services Acts Repeal Act, Feb 2024); voted to remove Te Mana o te Wai hierarchy from consenting (RM (Freshwater and Other Matters) Amendment Act 2024); Luxon 27 Sep 2026 attacks 'co-governance'.", NAT_LAUNCH, 2, "high"),
 "T4": c(0, "Voted against the Treaty Principles Bill at second reading (10 Apr 2025), saying principles developed by courts/Tribunal should stand; but committed in coalition to a review of Treaty clauses in legislation, i.e. Parliament re-specifying them. Documented contradiction -> 0.", TPB, 2, "medium"),
 "T5": c(-1, "National MP Rima Nakhle voted for and spoke in support of NZ First's English Language Bill (passed 3rd reading Jul 2026) under the coalition agreement; coalition requires departments to use English names first. Coalition-driven, flagged.", ENGBILL, 5, "medium"),
 "T6": None,
 "V1": c(-1, "Bishop/Watts 14 Aug 2026: 'A key part of this Government's plan... is to say yes to growth more often. That's why we are overhauling planning rules... and removing unnecessary red tape'; fast-track regime. Fisheries policy says 'strike the balance'. Qualified disagree.", NAT_BISHOP, 4, "medium"),
 "V2": c(-2, "'There will be no tax on agricultural emissions under a National government... back innovation over taxation' (Growing More to Feed the World, Oct 2026); maintain agriculture outside the ETS.", NAT_FARM, 1, "high"),
 "V3": c(2, "Passed the Fast-track Approvals Act 2024 (3rd reading 17 Dec 2024); 2026 policy to add a mining/extraction policy statement under the Fast-track Act and to replace the RMA; 'say yes to growth more often'.", FTA, 1, "high"),
 "V4": c(1, "'We will meet our commitments, keep New Zealand in Paris' (farming policy Oct 2026), while weakening the methane target and refusing agricultural pricing; qualified agree.", NAT_FARM, 1, "medium"),
 "V5": c(2, "Voted for Crown Minerals Amendment Act 2025 repealing the offshore oil and gas exploration ban; 2026 policy statement for mining under Fast-track; coalition Minerals Strategy to double mineral exports. Fiscal plan treats resource growth as revenue.", CMA, 2, "high"),
 "O1": c(0, "Economic Plan 2026: 'Changed immigration settings to ensure New Zealand is attracting the skills we need'; Luxon called 118,800 net migration 'unsustainable' (2023) but 2026 policy emphasises attracting skilled migrants and investors. Addressed only vaguely -> argued neutral.", "https://assets.national.org.nz/web/prod/National%27s%20Economic%20Plan.pdf?v=1790557287", 1, "low"),
 "O2": c(2, "Welfare policy (Oct 2026): extend the wait before new residents can access main benefits from 2 years to 5 years, 'in line with Australia and the UK'.", NAT_WELFARE, 1, "high"),
 "O3": c(-1, "Luxon conference speech 21 Jun 2026: 'Boosting defence spending and investing in the cutting-edge capability we need to protect our region'; Luxon wants NZ to be a 'force multiplier' for Australia and is scoping AUKUS Pillar 2. National still describes its foreign policy as independent, so qualified disagree.", NAT_CONF, 4, "medium"),
 "D1": None,
 "D2": None,
 "D3": c(-2, "Rates Capping Bill: councils' annual rate rises held to a 2-4% target range with an independent regulator (policy page, 2026); Government also required binding polls on Māori wards (2024).", NAT_RATES, 1, "high"),
}

LAB_CGT = "https://www.labour.org.nz/capitalgainstax"
LAB_WORK = "https://www.labour.org.nz/fairer-workplaces"
LAB_FISCAL = "https://www.labour.org.nz/fiscal-strategy"
LAB_FF = "https://www.labour.org.nz/futurefund"
LAB_IMM = "https://www.labour.org.nz/immigration"
LAB_AUKUS = "https://www.labour.org.nz/news/release-a-labour-government-will-not-join-aukus/"
LAB_MOVE = "https://www.labour.org.nz/news/release-move-on-bill-still-punishes-the-homeless/"
LAB_TRUST = "https://www.labour.org.nz/news/speech-trust-in-government-chris-hipkins/"

labour = {
 "E1": c(1, "2026 CGT (28% on property gains) ring-fenced for health, pay-equity restoration and Living Wage across the public service; Labour frames CGT as fairness between work and property income. No explicit 'reduce the gap' pledge or broad higher taxes (rules out wealth tax).", LAB_CGT, 1, "medium"),
 "E2": c(-1, "Fiscal Strategy 2026: 'balance the books without shrinking the economy'; funds Medicard, free prescriptions and public-service restoration partly through a new CGT; attacks National's tax cuts 'to those at the top'. Prefers services over tax cuts, qualified.", LAB_FISCAL, 1, "medium"),
 "E3": c(1, "28% capital gains tax on residential investment and commercial property from 1 Jul 2027; family home, farms, shares, KiwiSaver and businesses exempt - a partial version of taxing asset gains like income.", LAB_CGT, 1, "high"),
 "E4": c(-1, "NZ Future Fund: seeded state assets 'cannot be sold and will remain in public ownership for generations'; retain NZ ownership of Kiwibank; Hipkins on asset sales: 'there won't be anything left to sell'. Opposes privatisation; not an explicit claim that state delivery is better.", LAB_FF, 1, "medium"),
 "E5": c(-1, "Labour opposed the coalition's expansion of benefit sanctions (Social Security Amendment Act 2025, Traffic Light sanctions) and National's Oct 2026 welfare package; Labour did keep obligations/sanctions when in government. Coder could not retrieve the division record - verify.", SSAB, 2, "low"),
 "E6": c(2, "'Fair Pay Agreements legislation introduced in the first 100 days'; 'Collective agreements the default' (Fairer Workplaces, 2026); NZCTU scorecard: Labour 'Yes' to restoring FPAs.", LAB_WORK, 1, "high"),
 "E7": c(-1, "Fiscal Strategy: surplus by 2029/30 and net debt 'around 20% of GDP over time', but 'You can't cut your way to growth'; prioritises Medicard, hospital repairs and school upgrades now. Qualified disagree.", LAB_FISCAL, 1, "medium"),
 "S1": c(-1, "Voted against Sentencing (Reinstating Three Strikes) Amendment Act (Dec 2024; Duncan Webb: minimum-sentence laws 'did little to reduce serious crime'); no 2026 pledge to repeal.", THREE, 2, "medium"),
 "S2": c(0, "Voted against the Gangs Act 2024 but later said it would not repeal the patch ban; on the 2026 move-on orders bill Labour sought amendments to protect rough sleepers rather than opposing the power outright (3 Sep 2026 release). Both sides emphasised -> argued neutral.", LAB_MOVE, 2, "medium"),
 "S3": None,
 "S4": c(1, "Labour rainbow spokesperson Shanan Halbert called the Nov 2025 puberty-blocker ban 'one of the most damaging and ideological moves'; 2026 policy for a rainbow health strategy. No explicit position on the 2025 RSE framework found.", "https://gayexpress.co.nz/2025/11/exclusive-not-healthcare-but-politics-labours-shanan-halbert-slams-ban-on-trans-youth-treatment/", 4, "medium"),
 "S5": c(-1, "2026 'Safer Online' policy: Digital Duty of Care requiring platforms to protect people from 'harmful content', independent online regulator with fining powers, under-16 social media ban. (Hate-speech law work was dropped in 2023.) Qualified disagree.", "https://www.labour.org.nz/safer-online", 1, "medium"),
 "S6": c(-2, "'Stop running youth offender boot camps' / 'National must scrap its failed boot camps' (2026); voted against military-style academies legislation.", "https://www.labour.org.nz/news/release-national-must-scrap-its-failed-boot-camps/", 1, "high"),
 "T1": c(2, "Will restore the Te Tiriti obligation on school boards (21 May 2026), restore Mana Whakahono a Rohe iwi participation agreements, partner with Māori in education after Tribunal findings (17 Sep 2026); Greenpeace Q21 'Yes' to Treaty clauses in environmental law.", "https://www.labour.org.nz/news/release-labour-will-restore-te-tiriti-commitment-in-schools/", 1, "high"),
 "T2": c(-2, "Voted against the 2024 Māori wards referendum law (Hipkins: coalition 'embarrassing' NZ); defended Māori Health Authority; opposes NZ First's Māori seats referendum; 2026 pledge to partner with Māori in education.", WARDS, 2, "high"),
 "T3": c(1, "Will restore Mana Whakahono a Rohe iwi participation agreements in resource management and reinsert Treaty clauses in Planning/Natural Environment Bills (Greenpeace Q21); Greenpeace Q14: supports Te Mana o te Wai but did not commit to reinstating it in 100 days.", "https://www.labour.org.nz/news/release-labour-will-restore-mana-whakahono-a-rohe-agreements/", 1, "medium"),
 "T4": c(-2, "Voted against the Treaty Principles Bill (second reading 10 Apr 2025) and will repeal the Regulatory Standards Act in the first 100 days; relies on courts/Tribunal interpretation.", TPB, 2, "high"),
 "T5": c(1, "Campaign launch 2026 mocks coalition 'arguing... about te Reo on government letterheads'; restoring Te Tiriti in schools release criticises 'cutting support for teachers learning te reo Māori'; opposed English Language Bill as 'unnecessary and divisive' (McAnulty). No positive expansion pledge found.", ENGBILL, 2, "medium"),
 "T6": None,
 "V1": c(1, "Greenpeace Q23 'Yes': fix fast-track so 'environmental protections are not overridden'; 'no new mines on conservation land' (12 Oct 2026); but 2026 economic plan prioritises growth. Qualified agree.", GP, 3, "medium"),
 "V2": c(0, "Greenpeace Q17 (ag into ETS): no commitment - 'the ETS is broken... Labour will urgently review the ETS'. Topic addressed only vaguely -> argued neutral.", GP, 3, "medium"),
 "V3": c(-1, "Voted against the Fast-track Approvals Act (Dec 2024); Greenpeace Q23: 'Labour will fix the Fast-track Approvals Act so that environmental protections are not overridden' - retains a fast-track with safeguards, so qualified disagree.", GP, 3, "high"),
 "V4": c(2, "'We are committed to the Paris Agreement' (foreign policy speech 2026); Greenpeace Q16 'Yes' to reinstating offshore oil and gas ban; policy to 're-engage in climate diplomacy'.", "https://www.labour.org.nz/news/speech-new-zealand-an-independent-voice-in-the-world/", 1, "high"),
 "V5": c(-2, "Greenpeace 2026: 'Yes' to reinstating the offshore oil and gas exploration ban and 'Yes' to banning seabed mining; 'No new mines on conservation land' (12 Oct 2026); voted against Crown Minerals Amendment Act 2025.", GP, 3, "high"),
 "O1": c(0, "Immigration policy (11 Sep 2026): 'plan immigration around what New Zealand's workforce, housing and infrastructure can support' with an immigration statement; no commitment to reduce numbers, also expands Pacific access. Argued neutral.", LAB_IMM, 1, "medium"),
 "O2": c(0, "Extends the wait for permanent residence from two to four years (Immigration policy 2026) but has no policy to lengthen the benefit stand-down (currently 2 years) and opposes National's 5-year wait. Mixed -> argued neutral.", LAB_IMM, 1, "low"),
 "O3": c(1, "'A Labour Government will not join AUKUS' pillar one or two (1 Dec 2024, restated 2026); 'restoring our independent foreign policy'. Also wants to 'strengthen and revitalise relationships with traditional partners', so qualified.", LAB_AUKUS, 1, "medium"),
 "D1": None,
 "D2": c(0, "Greenpeace Q24 (voters-only donations): 'Labour believes in transparent and fair rules for political party donations' - no commitment; 2026 policy only extends disclosure to third-party campaigners. Vague -> argued neutral.", GP, 3, "low"),
 "D3": c(1, "Voted against the 2024 law overriding council decisions on Māori wards by forcing binding polls (Hipkins: coalition 'embarrassing' NZ). No stated 2026 position on the rates cap found in sources checked; +1 inferred from that vote only, flagged.", WARDS, 2, "low"),
}

GRN_INC = "https://www.greens.org.nz/manifesto_2026_income"
GRN_JUST = "https://www.greens.org.nz/manifesto_2026_justice_and_community_safety"
GRN_TIRITI = "https://www.greens.org.nz/manifesto_2026_te_tiriti_o_waitangi"
GRN_DEM = "https://www.greens.org.nz/manifesto_2026_democracy"
GRN_LG = "https://www.greens.org.nz/manifesto_2026_local_government"
GRN_TAX = "https://assets.nationbuilder.com/beachheroes/pages/71965/attachments/original/1782084525/GreensTaxPolicy2026.pdf?1782084525"
GRN_GOV = "https://www.greens.org.nz/government_in_the_economy_policy"
GRN_POWER = "https://assets.nationbuilder.com/beachheroes/pages/74612/attachments/original/1784510079/The_Greens'_Full_Power_Policy.pdf?1784510079"

green = {
 "E1": c(2, "Tax policy 2026 'A tax system for all of us': 2.5% tax on net assets over $10m, capital acquisitions tax, higher corporate tax and new top income rate 'to address inequality' and cut income tax for 96%.", GRN_TAX, 1, "high"),
 "E2": c(-2, "Greens fund free ECE, dental, fees-free and public housing by taxing 'the super-rich and large corporates'; manifesto: 'fund public services adequately'; Green Budget 2025 raises revenue and borrowing rather than cutting.", GRN_TAX, 1, "high"),
 "E3": c(2, "Standing economic policy: 'expanding the progressive tax system to equitably tax wealth and all forms of income, such as through capital gains, land, wealth, and inheritance taxes'; 2026 wealth tax and capital acquisitions tax; criticised Labour's CGT as too limited.", GRN_GOV, 1, "high"),
 "E4": c(-2, "Kiwipower publicly owned electricity firm ('Public ownership'), KiwiMart public supermarket, 'tens of thousands of new public homes', replace Public Transport Operating Model so services are 'provided publicly instead of for profit'; public services and SOEs to 'remain in public hands'.", GRN_POWER, 1, "high"),
 "E5": c(-2, "Manifesto 2026: 'Increase benefits to liveable rates, individualise benefit entitlements and abolish benefit sanctions'; high-trust model at Work and Income; voted against Social Security Amendment Act 2025.", GRN_INC, 1, "high"),
 "E6": c(2, "Default union membership for new workers, expanded right to strike, reverse pay-equity and Fair Pay Agreement changes (manifesto 2026); NZCTU scorecard 'Yes' to restoring FPAs.", "https://www.greens.org.nz/manifesto_2026_workforce_rights", 1, "high"),
 "E7": c(-2, "Standing policy: 'Enabling greater government borrowing for investing in infrastructure'; manifesto reforms public finance to 'support long-term resilience... health and well-being'; Green Budget 2025 funded by taxes on wealth, not spending restraint.", GRN_GOV, 1, "high"),
 "S1": c(-2, "Manifesto 2026: 'Enable judicial discretion in sentencing, including by abolishing mandatory minimum sentences, life sentences, preventive detention, limits on sentence discounts, three strikes'; voted against Three Strikes 2024.", GRN_JUST, 1, "high"),
 "S2": c(-2, "Voted against Gangs Act 2024 (dispersal and non-consorting powers 'would increase racism and the incarceration of Māori'); opposed the 2026 move-on orders bill entirely; manifesto: body cameras, stronger IPCA.", GANGS, 2, "high"),
 "S3": c(2, "Manifesto 2026: 'Repeal and replace the Misuse of Drugs Act... treats drug use as a health issue and provides for regulated access to cannabis for personal use'; psychedelic licensing; Good Samaritan laws.", "https://www.greens.org.nz/manifesto_2026_drug_law_reform", 1, "high"),
 "S4": c(2, "Manifesto 2026: 'Restore relationship and sexuality teaching guidelines - including education on... diverse identities and sexualities... in all schools'; reverse the puberty-blocker ban; amend Human Rights Act for gender identity.", "https://www.greens.org.nz/manifesto_2026_violence_prevention", 1, "high"),
 "S5": c(-2, "Manifesto 2026: 'Extend hate speech laws to cover religion, gender, disability and rainbow communities'; Digital Duty of Care regulating harmful online content.", GRN_JUST, 1, "high"),
 "S6": c(-2, "Manifesto 2026: 'End military-style academies, raise the age of criminal responsibility'; expand Rangatahi Courts and rehabilitation; voted against the bootcamps bill.", GRN_JUST, 1, "high"),
 "T1": c(2, "Manifesto 2026: 'Implement genuine Te Tiriti-based decision-making models across government and resource iwi and hapū to participate as partners'; Te Tiriti clauses in environment law (Greenpeace Q21 'Yes').", GRN_TIRITI, 1, "high"),
 "T2": c(-2, "Manifesto 2026: 'Entrench the Māori electoral seats'; reinstate councils' ability to keep Māori wards; by-Māori-for-Māori health clinics; voted against 2024 Māori wards referendum law.", GRN_DEM, 1, "high"),
 "T3": c(2, "Manifesto 2026: 'affirm the role of tangata whenua as shared decision-makers and kaitiaki in the new resource management system'; reinstate Te Mana o te Wai; Tiriti-based Public-Commons Partnerships.", "https://www.greens.org.nz/manifesto_2026_environmental_protection", 1, "high"),
 "T4": c(-2, "Voted against Treaty Principles Bill (Apr 2025); manifesto gives the Waitangi Tribunal 'the power to make binding recommendations' and recognises Te Tiriti as the authoritative text; repeal Regulatory Standards Act.", GRN_TIRITI, 1, "high"),
 "T5": c(2, "$200m for te reo Māori; 'Expand the learning, speaking and promotion of te reo Māori in both formal and informal settings'; Te Tiriti and te reo training for all public servants; opposed English Language Bill.", "https://www.greens.org.nz/manifesto_2026_maori_centred", 1, "high"),
 "T6": c(-2, "Manifesto 2026: remove 'Full and Final settlement' clauses, end 'large natural grouping' approach, Tribunal power to order return of Crown and private land, return of wrongfully alienated whenua outside settlements.", GRN_TIRITI, 1, "high"),
 "V1": c(2, "Manifesto 2026 environmental chapters: repeal Fast-track Act and revoke mining consents, ban new mining on conservation land, 30% ocean protection, phase out synthetic nitrogen and reduce stocking rates - nature prioritised over extraction-led growth.", "https://www.greens.org.nz/manifesto_2026_environmental_protection", 1, "high"),
 "V2": c(2, "Manifesto 2026: 'Introduce a price on agricultural emissions'; reform ETS to remove free allocation and forestry offsetting; Greenpeace Q17 'We will bring agricultural emissions into the ETS'.", "https://www.greens.org.nz/manifesto_2020_climate_action_emissions_reduction", 1, "high"),
 "V3": c(-2, "Manifesto 2026: 'Repeal the Fast-track Approvals Act and revoke consents for fast-track approvals for new coal, gold and seabed mining projects'; voted against the Act.", "https://www.greens.org.nz/manifesto_2026_environmental_protection", 1, "high"),
 "V4": c(2, "Manifesto 2026: 'Ensure Aotearoa meets our Paris Agreement commitments through strong domestic action'; strengthen Zero Carbon Act to 1.5 degrees; include NDC cost in financial statements.", "https://www.greens.org.nz/manifesto_2020_climate_action_emissions_reduction", 1, "high"),
 "V5": c(-2, "Manifesto 2026: 'Ban new fossil fuel extraction, end subsidies for fossil fuels and cancel the LNG terminal'; ban seabed mining; ban new mining on conservation land; voted against Crown Minerals Amendment Act 2025.", "https://www.greens.org.nz/manifesto_2026_energy", 1, "high"),
 "O1": c(-1, "Manifesto 2026 expands migration: residence pathways for overstayers, refugee quota to 5,000 by 2029, open work rights for Pacific workers, abolish health requirements; no statement on overall numbers, so qualified disagree.", "https://www.greens.org.nz/manifesto_2026_immigration_and_refugees", 1, "medium"),
 "O2": None,
 "O3": c(2, "Manifesto 2026: 'Decouple military and security frameworks from the United States, including declining to participate in AUKUS and withdrawing from Five Eyes'; 'Restore an independent foreign policy'.", "https://www.greens.org.nz/manifesto_2026_global_affairs_and_trade", 1, "high"),
 "D1": c(0, "Favours citizens' assemblies and community decision-making (local government chapter) and voted for referendum-based decisions only on local matters (casino licences); opposed referendums on Treaty principles and Māori seats. Topic addressed only indirectly -> argued neutral.", GRN_LG, 1, "low"),
 "D2": c(2, "Manifesto 2026: 'Reform electoral funding by limiting donations to registered voters, increasing public financing of campaigns and capping a donor's donations'; Greenpeace Q24 'Yes'.", GRN_DEM, 1, "high"),
 "D3": c(2, "Manifesto 2026: 'Reject the proposed rates cap and enable a range of new funding and financing tools'; 'empower councils by devolving further responsibilities'; reinstate councils' ability to keep Māori wards.", GRN_LG, 1, "high"),
}
