#!/usr/bin/env python3
"""Reconcile the two blind codings of the quiz2 party-position matrix.

Inputs : data/guide/quiz2-coder-a.json, data/guide/quiz2-coder-b.json
Outputs: data/guide/quiz2.json, raw/quiz2/RECONCILIATION.md (decision log)
The method page (guide/quiz-method.md) is written by tools/quiz2_method_page.py from quiz2.json.

Rules applied (guide/quiz-research.md section 4 and the reconciler brief):
- both coded, identical: adopt; merge evidence; tier = min; confidence = max if the two sources differ,
  else the lower of the two.
- both coded, differ by one: adopt the better-evidenced value; if equally evidenced, the lower tier;
  if still tied, the value nearer 0. Every such decision is recorded.
- one null, one coded: adopt only if the evidence meets section 4 (explicit position, or an explicit general
  principle whose scope plainly covers the statement -> +/-1 low); otherwise null.
- any cell whose evidence is an inference from general ideology (not an explicit principle) -> null.
- an argued 0 must fit one of the three EUvox cases (vague; both sides emphasised; party split) or be a
  documented vote/statement contradiction; otherwise re-coded or nulled.
"""
import json, re, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = json.load(open(ROOT / "data/guide/quiz2-coder-a.json"))
B = json.load(open(ROOT / "data/guide/quiz2-coder-b.json"))
SA = {s["id"]: s for s in A["statements"]}
SB = {s["id"]: s for s in B["statements"]}
STATEMENT_IDS = list(SA)
PARTIES = list(SA["E1"]["positions"])

DIMENSIONS = {
    "E": "State and market",
    "S": "Social order and personal freedom",
    "T": "Te Tiriti and biculturalism",
    "V": "Environment and development",
    "O": "Openness",
    "D": "Democracy and power",
}
POLES = {
    "E": ("active, redistributive state", "lower taxes, markets, individual responsibility"),
    "S": ("personal freedom, social liberalism", "order, tradition, tougher justice"),
    "T": ("partnership, Māori-specific arrangements", "one law for all, uniform treatment"),
    "V": ("protect environment, pay for emissions", "growth, extraction, faster approvals"),
    "O": ("open, pluralist, independent", "fewer migrants, assimilation, traditional alliances"),
    "D": ("direct democracy, limits on money, local autonomy", "representative decision-making, central control"),
}
PARTY_NAMES = {
    "national": "National", "labour": "Labour", "green": "Green", "act": "ACT", "nz-first": "NZ First",
    "te-pati-maori": "Te Pāti Māori", "opportunity": "Opportunity (TOP)", "nz-loyal": "NZ Loyal",
    "nz-outdoors-freedom": "NZ Outdoors & Freedom", "legalise-cannabis": "Legalise Cannabis",
    "animal-justice": "Animal Justice", "alliance": "Alliance", "conservative": "Conservative",
    "womens-rights": "Women's Rights", "vision-nz": "Vision NZ", "free-palestine": "Free Palestine",
    "te-tai-tokerau-party": "Te Tai Tokerau Party",
}
CONF_RANK = {"low": 0, "medium": 1, "high": 2}

# ----------------------------------------------------------------------------------------------------
# Decisions. key = (statement, party). Fields:
#   pos   : adopted position (None = null)
#   pick  : which coder's evidence text/URL is primary ("A", "B", or "merge" for both)
#   conf  : confidence to record (optional override)
#   tier  : tier to record (optional override)
#   url   : source URL override (optional)
#   note  : the reconciler's written reason (published)
# Cells not listed here: identical codings are merged automatically.
# ----------------------------------------------------------------------------------------------------
D = {}
def dec(stmt, party, pos, pick, note, conf=None, tier=None, url=None, extra=None):
    D[(stmt, party)] = dict(pos=pos, pick=pick, note=note, conf=conf, tier=tier, url=url, extra=extra)

# ---- cells where the coders differed by one point (40) and by two (1) ----
dec("E1", "national", -1, "merge", "Both coders derive the value from the same 'no new taxes' pledge; neither found any 2026 text on narrowing the income gap. That is the permitted inference from an explicit general principle, which section 4.1(3) caps at +/-1 with low confidence. A's -2 (high) is reduced accordingly.", conf="low")
dec("E1", "nz-first", 0, "merge", "A (-1) and B (0) document the same two facts: NZ First proposes redistribution (In-Work Tax Credit rise, minimum-wage indexation, state bank) and simultaneously rejects higher taxes (SME tax cut; wealth taxes called 'communism', 13 Sep 2026). The statement is a trade-off and the party emphasises both sides without choosing: EUvox argued-neutral case 2. Consistent with its E2 and E7 codings.", conf="medium")
dec("E1", "conservative", -1, "merge", "Flat tax and lower taxes are explicit and emphasised, but the party says nothing about the income gap itself; the value is an inference from an explicit tax principle, so -1 under section 4.1(3). Confidence medium because the flat-tax commitment is a direct rejection of progressive taxation.", conf="medium")
dec("E3", "nz-first", -1, "merge", "Peters' derision of Labour's CGT (Oct 2025) and of wealth/land taxes (Sep 2026) is explicit opposition, but there is no 2026 policy document and KPMG's tracker records 'not stated'. -2 requires an emphasised, unconditional position; -1 fits.", conf="medium")
dec("E3", "te-pati-maori", 1, "merge", "The Kiwi Tax Plan (Aug 2026) taxes net wealth, vacant houses, land-banking and residential sales (stamp duty) but contains no capital gains tax: the archived plan never mentions capital gains. The statement is about taxing gains like income; taxing asset holdings is a partial match, so +1 (B's reading).", conf="medium")
dec("E4", "te-pati-maori", -1, "merge", "Explicit rejection of privatising water rights and a Māori energy-ownership fund, but no general position on private versus public delivery across electricity, housing and transport. Equal evidence and tier; nearer-zero rule gives -1.", conf="medium")
dec("E4", "opportunity", 0, "B", "Abundant Energy keeps Crown stakes in the gentailers and restructures the market for competition; housing policy backs both Kāinga Ora and community providers. Both sides stated by design: argued neutral (B, medium).")
dec("S1", "conservative", 1, "merge", "The only explicit 'longer sentences' commitment is for repeat child sexual offenders; the principles ('punishment that will deter crime', 'removal of criminals from society') point the same way but do not say longer. Equal tier; nearer-zero rule gives +1.", conf="medium")
dec("S2", "nz-first", 2, "B", "B cites two recorded votes directly enacting move-on and dispersal powers (Gangs Act 2024; Move-on Orders Bill 2026) plus NZ First's own Oct 2026 law-and-order package. Tier 2 beats A's tier-5 coalition inference. Confidence medium rather than high because stop-and-search specifically is not in NZ First's own policy text.", conf="medium")
dec("S3", "act", None, "merge", "DOWNGRADED TO NULL. A's 0 rests on Seymour's 2020 personal referendum vote and 'not a priority' remark (pre-2023, and a statement of no position rather than an argued neutral); B's -1 rests on ACT welcoming drug testing of beneficiaries and a drug-driving law, neither of which is a principle whose scope plainly covers adult freedom to use drugs. Neither coding meets section 4.")
dec("S5", "nz-first", 2, "A", "A cites the party's own Protection of Freedom of Expression member's bill (Nov 2025), long-standing opposition to hate-speech law and a 2026 free-speech plank: tier 1, explicit and emphasised. B's qualification (a 'misinformation posture') is not documented as a proposal to restrict speech.")
dec("S5", "conservative", 2, "B", "B's sources add the specific principle that laws 'must not be weaponised to target people with particular views', which covers the statement's 'even if offensive' clause; 'defend freedom of speech and assembly' appears in every policy summary. Emphasised and unconditional. Confidence medium because online harms are not addressed.", conf="medium")
dec("S6", "labour", -1, "merge", "Labour's material addresses one instrument (scrap boot camps / military-style academies) and does not set out the broader principle of support over tougher consequences; that is 'only part of the proposal', so -1.", conf="medium")
dec("S6", "opportunity", -2, "B", "Smart on Crime explicitly chooses the alternative the statement rejects: redirect boot-camp funding to prevention, whānau-centred interventions and rehabilitation for persistent young offenders. Clear, emphasised, no qualification: -2 (B).")
dec("S6", "alliance", -2, "B", "Justice policy proposes habilitation centres 'particularly for young people', Community Care Orders and iwi-run rehabilitation instead of imprisonment, and frames youth offending as a social-environment problem. The support-based alternative is stated explicitly: -2.", conf="medium")
dec("T1", "labour", 1, "A", "Labour restores Te Tiriti obligations in schools and iwi participation agreements and opposes the Treaty-clauses review, but A documents restrictions: no re-establishment of the Māori Health Authority and a deliberate de-emphasis in the 2026 campaign. Qualified support: +1.")
dec("T1", "nz-loyal", -1, "merge", "Both coders infer from 'scrap all race-based policies' (RNZ, 12 Oct 2026, verified). An inference from a general principle is capped at +/-1 low by section 4.1(3).", conf="low")
dec("T1", "womens-rights", 0, "A", "The only text is 'we acknowledge Te Tiriti o Waitangi as Aotearoa New Zealand's founding document' with nothing on law or services. Addressed only vaguely: EUvox argued-neutral case 1 (A). Low confidence.", conf="low")
dec("T2", "national", 1, "A", "National legislated binding polls on Māori wards (tier 2 vote, 30 Jul 2024), disestablished the Māori Health Authority and issued the 'need not race' circular: concrete action against set-aside wards and services. It has no policy to abolish the Māori seats, which is a restriction, not an opposing emphasis, so +1 rather than 0. Neither coder's claim that Luxon formally ruled out NZ First's Feb 2026 seats referendum could be verified; it is not relied on.", conf="medium")
dec("T3", "vision-nz", -1, "merge", "'End He Puapua-driven policies' targets the co-governance roadmap by name, but it is still a general principle rather than a statement on resource co-management: +/-1 low under section 4.1(3).", conf="low")
dec("T4", "opportunity", -2, "B", "B cites the party's formal submission calling the Treaty Principles Bill 'constitutionally inappropriate, historically flawed and procedurally illegitimate', an explicit and emphatic rejection of Parliament defining the Treaty's meaning; A's policy paper points the same way. Consistent with Labour and Green, coded -2 from the same bill.", conf="medium")
dec("T4", "alliance", -1, "merge", "Strengthening the Tribunal and committing to act on its recommendations favours the Tribunal's authority, but the policy does not say who should determine the Treaty's meaning. Partial fit: -1.", conf="medium")
dec("T6", "green", -2, "B", "B's manifesto citations (remove 'full and final' clauses, end the large-natural-grouping approach, Tribunal power to order return of land) are specific proposals to re-open and extend the process, the direct opposite of closure. Emphasised: -2.")
dec("T6", "alliance", -1, "merge", "'Grievances must be redressed' and a stronger Tribunal oppose closure in direction but do not address the settlement process specifically. -1 medium.", conf="medium")
dec("V1", "nz-outdoors-freedom", 0, "merge", "The party rejects climate policy (exit Paris) while backing poison-free conservation, ecological agriculture and fisheries restoration. Both sides emphasised: argued neutral (case 2). Equal tier and confidence; nearer-zero rule.", conf="low")
dec("V2", "national", -1, "A", "'No tax on agricultural emissions' is explicit, but National keeps industry inside the ETS. The statement covers farmers and industry; rejecting one half is partial opposition: -1 (A's reasoning), high confidence.")
dec("V3", "opportunity", -1, "B", "Greenpeace answer 'Yes' to restoring enforceable protections in consenting, but the Affordable Housing policy seeks faster consenting: qualified disagree (B).")
dec("V3", "alliance", -1, "merge", "Mining bans, restoration bonds and a Conservation Minister veto all add checks, but the party has no statement on fast-track approvals themselves. Equal tier; nearer-zero rule: -1.", conf="medium")
dec("V4", "te-pati-maori", 1, "merge", "Strong domestic climate measures and 'advocate internationally for climate justice' support the direction, but neither coder found a statement on keeping international commitments at economic cost. +1 (B's reading), medium.", conf="medium")
dec("V5", "animal-justice", -2, "B", "B's quotation verified in the archived policy: 'End government underwriting and tax incentives for fossil fuel exploration, particularly ... offshore oil and gas'; restrict seabed mining; mining 'destroys underground habitats'. Explicit and directly contrary: -2 (A had only an inference).", conf="medium")
dec("O1", "national", 0, "merge", "National's 2026 measures target investors and skilled migrants and say nothing about overall numbers; Luxon's 2023 'unsustainable' remark cuts the other way. Addressed without a direction on numbers: argued neutral. Equal tier and confidence; nearer-zero rule.", conf="low")
dec("O1", "labour", 0, "B", "Labour's Sep 2026 policy plans immigration 'around what the workforce, housing and infrastructure can support' (verified on labour.org.nz/immigration) with no target for fewer or more. Argued neutral (B, medium).")
dec("O1", "green", -1, "merge", "Every Green proposal expands migration pathways, but the manifesto contains no statement on overall numbers; -2 requires an emphasised unconditional position. -1 medium.", conf="medium")
dec("O3", "nz-first", -1, "B", "Peters as Foreign Minister said independence 'never meant non-aligned', pursued AUKUS Pillar 2 exploration and deepened US/Australia ties. A's counterweight ('sovereignty' rhetoric) concerns foreign influence and the UN, not military alliances, so it does not make an argued neutral. -1 low.", conf="low")
dec("D1", "green", -1, "A", "The Greens oppose every national referendum proposed this term (Treaty principles, Māori seats; would entrench the seats against referendums) and have no direct-democracy policy; their only referendum proposal is local (casino licences). A pattern of explicit opposition to the proposed instruments: -1, low confidence because no general statement exists.", conf="low")
dec("D1", "act", 0, "A", "ACT campaigned for a binding referendum on its Treaty Principles Bill (2023-25) and backed binding Māori-ward polls, but opposed Luxon's electoral-system referendum (Reuters, 5-6 Aug 2026, verified) and asserts parliamentary supremacy. Both sides on the record: argued neutral (A).", conf="low")
dec("D1", "te-pati-maori", -1, "merge", "Explicit opposition to referendums on the Māori seats ('beyond the reach of referendums') and Treaty principles, preferring a Matike Mai constitutional process. Specific to those questions, so -1 rather than -2; medium.", conf="medium")
dec("D1", "opportunity", 0, "B", "Citizens' Voice proposes citizens' assemblies for major decisions while stating 'this isn't about replacing elections or Parliament', and the leader rejected a Treaty referendum. Direct participation deliberately short of binding referendums: argued neutral (B, medium).")
dec("D2", "animal-justice", 2, "B", "B's quotation verified in the archived People Policies pack: 'Permit only New Zealand citizens or permanent residents registered to vote to make political donations, removing corporate/industry entity donations', with a $1,500 disclosure threshold. Exactly the statement: +2.")
dec("D3", "labour", 0, "A", "Labour is 'open to the idea of a rates cap in principle' (Aug 2026, centralising) after Hipkins called caps counter-productive (Jul 2025), and opposed the Māori-ward override (devolving). B's +1 rests on the single 2024 vote. Documented both-ways record: argued neutral (A).", conf="low")
dec("D3", "act", -2, "A", "Two-point disagreement. ACT's programme constrains councils at every turn: rates cap, binding Māori-ward polls, removing votes from unelected appointees by statute, mandated compensation rules, and opposition to councils' own bed tax. B's devolving item (a Local Tourism Dividend) is a funding transfer, not autonomy. A's evidence is directly on point: -2, medium.", conf="medium")

# ---- cells coded by one coder only (51) ----
dec("E1", "animal-justice", 1, "B", "Explicit commitment to reduce economic inequality through employment law and transition support; no tax measure. Partial: +1 low.")
dec("E1", "womens-rights", 1, "B", "Explicit: raise minimum wages and benefits 'so that all people have living incomes' and target Working for Families at the poorest. Direction explicit, tax side unaddressed: +1 low.")
dec("E1", "te-tai-tokerau-party", 1, "B", "Universal Whānau Allowance, debt amnesty and mana whenua equity stakes are explicit redistribution; no tax measure: +1 low.")
dec("E2", "nz-first", 0, "A", "Tax cuts (20% SME rate) and very large new spending ($100bn Future Fund, Kiwi Kids Grant) proposed together with no stated preference: both sides emphasised, argued neutral. Consistent with E1 and E7.")
dec("E2", "nz-loyal", None, "B", "DOWNGRADED TO NULL. 'Scrap the current tax system' states no direction on the level of tax and 'reject government overreach' is general ideology; neither plainly covers a tax-versus-services trade-off.")
dec("E2", "nz-outdoors-freedom", 1, "B", "'Smaller, leaner central government', shrink ministries and 'end bureaucratic waste' is an explicit general principle whose scope plainly covers preferring a smaller state to more services: +1 low.")
dec("E3", "conservative", None, "B", "DOWNGRADED TO NULL. A flat income-tax preference says nothing about whether capital gains should be taxed (a flat tax can include or exclude them); no capital-gains text exists in any archived Conservative document.")
dec("E5", "conservative", 1, "B", "'Welfare: reform is needed. Fifty years of expanding welfare has undermined our families and created an underclass' and 'less dependency' (verified) is an explicit general welfare-reform principle whose scope covers firmer obligations; no sanctions detail: +1 low.")
dec("E5", "vision-nz", None, "B", "DOWNGRADED TO NULL. 'Dismantle state dependency' and 'no-strings-attached' family payments are adjacent to, not about, obligations and penalties on beneficiaries; a 0 must rest on the statement's own topic being addressed.")
dec("E6", "animal-justice", 1, "B", "'Strong unions and worker rights provide the foundation for reducing inequality' and rights 'through collective organisation' is an explicit principle covering union bargaining; no industry-wide bargaining specifics: +1, medium as coded.")
dec("S1", "legalise-cannabis", None, "B", "DOWNGRADED TO NULL. The policy redirects enforcement money 'to fight serious crime' (if anything, the opposite direction) and has no sentencing position; B's own note calls it a weak inference.")
dec("S1", "womens-rights", 1, "B", "Explicit call for 'standalone, sex-based laws with higher penalties' for violence against women and children: longer sentences for one class of serious crime, +1 low.")
dec("S2", "nz-outdoors-freedom", -1, "A", "Entrenching the Bill of Rights as supreme law so freedom of movement and assembly 'cannot be overridden' is an explicit principle whose scope plainly covers expanded move-on and search powers: -1 low.")
dec("S3", "nz-first", None, "B", "DOWNGRADED TO NULL. B's cited speech (State of the Nation, Mar 2026) contains no reference to cannabis, drugs or drug law (fetched and checked); the remaining basis is a 2020 referendum stance, and A found nothing in two searches.")
dec("S4", "act", -1, "B", "Verified: ACT children's spokesperson Karen Chhour welcomed the suspension of puberty-blocker prescriptions as putting 'child safety' first (20 Nov 2025 release). That is an explicit position on a public institution's approach to gender, but it concerns health, not schools, and the RSE-guideline removal was a NZ First coalition demand, not ACT's. Reduced from -2 to -1, medium, tier 4.", conf="medium", tier=4, url="https://www.act.org.nz/news/puberty-blockers-chhour-backs-moves-to-prioritise-child-safety")
dec("S4", "opportunity", 1, "B", "State of the Nation 2026 explicitly defends transgender New Zealanders against NZ First's 'policies of fear and division'; a general principle covering public institutions and gender: +1 low.")
dec("S5", "labour", -1, "B", "'Safer Online' (2026): a Digital Duty of Care requiring platforms to protect people from 'harmful content' and a regulator with fining powers is an explicit limit on online speech that others find harmful: -1 medium.")
dec("S5", "te-pati-maori", -1, "B", "Mana Takatāpui (Sep 2026) seeks 'protection from violence and hate'; the party supported hate-speech criminalisation in 2021 (older evidence used because nothing newer exists; date recorded). -1 low.")
dec("S5", "opportunity", None, "B", "DOWNGRADED TO NULL. A ban on materially false statements in electoral advertising is a truth-in-advertising rule, not a position on offensive or harmful speech; support for an under-16 social media bill is not a speech position.")
dec("S5", "nz-loyal", None, "A", "DOWNGRADED TO NULL. 'We restore our freedoms' is general ideology and 'expose and eradicate propaganda from our news media' is about the media, not about what people may say; the statement's topic is not addressed, so there is no argued neutral.")
dec("S5", "animal-justice", None, "B", "DOWNGRADED TO NULL. Whistleblower protection and support for peaceful protest do not cover offensive or harmful speech.")
dec("T1", "legalise-cannabis", 1, "B", "Standing policy: 'Full inclusion of Treaty of Waitangi principles' as a founding principle and support for 'partnership' under the Treaty: an explicit general principle covering the Treaty shaping law. Founding text dates from 1996 but remains the current policy page. +1 low.")
dec("T2", "animal-justice", -1, "A", "'Prioritising Māori leadership in land-use decision-making' is an explicit principle in favour of Māori-specific roles, which plainly contradicts 'no arrangements set aside for Māori': -1 low.")
dec("T3", "nz-loyal", -1, "A", "'Scrap all race-based policies' (verified) plainly covers Māori co-management of resources: -1 low.")
dec("T3", "animal-justice", 1, "A", "'Prioritising Māori leadership in land-use decision-making' and self-determined food and land systems directly supports shared decision-making over land: +1 medium.")
dec("T4", "conservative", 1, "A", "Verified: 'Bureaucrats, elements of the Judiciary, and unelected advisors ... have increasingly chosen to usurp the democratic mandate of elected representatives', with 'one law for all'. An explicit principle of elected-over-judicial authority whose scope covers Parliament versus the courts and Tribunal on the Treaty: +1 low.")
dec("T5", "alliance", 2, "A", "Verified: 'Māoritanga and Te Reo promoted as the first culture and language of Aotearoa New Zealand'. Explicit and emphatic: +2 high. (B missed this line.)")
dec("T5", "conservative", None, "B", "DOWNGRADED TO NULL. 'Newcomers should follow our way of life' is about immigrants, not te reo or tikanga in public life; 'Judeo-Christian traditions' is general ideology.")
dec("T6", "national", 0, "A", "Goldsmith (Jun 2026) is 'focused on progressing settlements' with no proposal to curtail the process and no claim it has gone too far; National addresses settlements but takes neither the closure nor the expansion side. Argued neutral, low confidence; B coded null and A notes null is also defensible.")
dec("V1", "nz-loyal", -1, "A", "'Save our farmers from restrictive regulations' and 'end climate accords based on faulty science' (verified) are explicit principles against environmental regulation at economic cost: -1 low.")
dec("V2", "nz-loyal", -1, "A", "'End climate accords based on faulty science' and 'save our farmers from restrictive regulations' plainly cover emissions pricing on farmers, but the value is an inference from general principles, so reduced from -2 to -1 low under section 4.1(3).", conf="low")
dec("V2", "nz-outdoors-freedom", -2, "A", "Verified in the archived agriculture policy: exit Paris because it is 'far more expensive to stay and pay their taxes'; 'farm animals cannot release more carbon than they eat'; 'we should celebrate carbon, not fear it'. Explicit rejection of farm emissions liability: -2, medium (industry not addressed separately).", conf="medium")
dec("V2", "vision-nz", -1, "A", "'Leave ... the Paris Accord' to 'restore absolute national sovereignty' (verified) is an explicit rejection of climate obligations whose scope plainly covers making farmers and industry pay for emissions: -1 low.")
dec("V3", "nz-outdoors-freedom", -1, "A", "Precautionary principle with full liability and an independent Health-Environment Protection Agency: explicit principles for more, not fewer, checks: -1 low.")
dec("V3", "animal-justice", -1, "A", "Mandatory wildlife impact assessments in planning and road design is an explicit proposal for more environmental checks on projects: -1 low.")
dec("V3", "conservative", 1, "B", "'Remove excessive red tape to speed up project approvals while maintaining environmental protections': supports faster approvals but not reduced checks, the weaker version of the statement: +1 low.")
dec("V3", "te-tai-tokerau-party", -1, "A", "Kaitiaki Guardians empowered to issue protection notices against environmental harm, and repeal of the Regulatory Standards Act: more enforcement, not less: -1 low.")
dec("O1", "legalise-cannabis", None, "A", "DOWNGRADED TO NULL. The party says it has 'no other immigration position beyond inclusiveness and tolerance': a declared absence of policy is null under section 4.2, not an argued neutral.")
dec("O1", "alliance", -1, "B", "'Review and reduce unnecessary barriers to migration from neighbouring Pacific Island countries' moves toward more migrants for one region; partial: -1 low.")
dec("O2", "labour", None, "B", "DOWNGRADED TO NULL. labour.org.nz/immigration (fetched) says nothing about benefits or stand-downs; the two-to-four-year change concerns permanent residence, not benefit access, and the claimed opposition to a five-year benefit wait could not be sourced. No position found.")
dec("O2", "green", None, "A", "DOWNGRADED TO NULL. 'Remove barriers for migrants' is general, and 'reciprocal welfare arrangements' concerns bilateral reciprocity, not a stand-down; neither plainly covers how long new migrants should wait for benefits. A labelled it a low-confidence inference.")
dec("O2", "alliance", -1, "B", "Welfare policy abolishes 'unnecessary stand-down periods' and makes income support a universal entitlement based on dignity: an explicit principle whose scope plainly covers migrant stand-downs: -1 low.")
dec("O3", "act", -1, "B", "ACT's 2026 minerals policy frames development as providing 'strategic resources to our allies' (verified), and ACT campaigns for defence spending of 2% of GDP arguing New Zealand must pay to keep its Australian alliance credible (act.org.nz, 'God defend New Zealand'). Direction toward allies, no explicit alliance doctrine: -1 low.")
dec("D1", "national", -1, "A", "Luxon refused a Treaty referendum ('it's a no from me', Jan 2025) and said an election, not a referendum, is the mandate for asset sales; he is 'open to' an electoral-system referendum (Reuters, Aug 2026, verified), the one domain where referendums are conventional. Pattern of preferring parliamentary decision, with a qualification: -1 low.")
dec("D1", "labour", -1, "A", "Verified: Labour opposed Luxon's proposed electoral-system referendum (Reuters, 5 Aug 2026) and NZ First's Māori-seats referendum (McAnulty, 12 Feb 2026: 'it is Māori that should decide'); no direct-democracy policy. -1 low.")
dec("D1", "animal-justice", None, "B", "DOWNGRADED TO NULL. Praise for citizens' assemblies is not a position on binding referendums versus Parliament; B's own note says 'not binding referendums per se'.")
dec("D1", "conservative", None, "B", "DOWNGRADED TO NULL. 'Give power back to the people' aimed at bureaucrats and judges does not address referendums; a 0 requires the statement's topic to be addressed.")
dec("D1", "vision-nz", None, "B", "DOWNGRADED TO NULL. Abolishing party lists, cutting MP numbers and term limits are reforms of representation, not a position on referendums; B called it a weak inference.")
dec("D2", "national", None, "A", "DOWNGRADED TO NULL. Greenpeace records that National has no policy on voter-only donations ('no policy' is null under section 4.2); raising the disclosure threshold concerns disclosure, not who may donate.")
dec("D3", "conservative", 1, "B", "Verified principle: 'Decision-making should be as local as possible through a principle known as localism ... higher levels of government should serve to empower and support lower levels of authority, rather than control or replace them'. Explicit: +1 medium.")
dec("D3", "te-tai-tokerau-party", None, "B", "DOWNGRADED TO NULL. Rohe-based devolution to hapū and iwi and freeing food trade 'from council licensing' is not a position on council autonomy versus central government; B's own note concedes councils are not addressed.")

# ---- identical cells that still need a change (inference caps, tier/confidence fixes) ----
dec("S3", "national", -1, "merge", "Identical codings. Luxon's 2022 'won't decriminalise cannabis' is the only general statement (pre-2023, used because nothing newer exists; date recorded) and the 2026 drug-testing of Jobseekers is narrow in scope. Confidence held at low.", conf="low")

# ----------------------------------------------------------------------------------------------------
def merge_text(a, b):
    """Combine two coders' evidence into one audit text."""
    if a and b:
        if a["source_url"] == b["source_url"]:
            longer = a if len(a["evidence"]) >= len(b["evidence"]) else b
            return longer["evidence"]
        return f"Coder A: {a['evidence']} Coder B: {b['evidence']}"
    return (a or b)["evidence"]

def build_cell(stmt, party):
    a = SA[stmt]["positions"].get(party)
    b = SB[stmt]["positions"].get(party)
    av = a["position"] if a else None
    bv = b["position"] if b else None
    key = (stmt, party)
    log = None
    if key in D:
        d = D[key]
        pos = d["pos"]
        if pos is None:
            log = dict(statement=stmt, party=party, A=av, B=bv, adopted=None, reason=d["note"])
            return None, log, av, bv
        pick = d["pick"]
        prim = a if pick == "A" else b if pick == "B" else (a if (a and (not b or a["tier"] <= b["tier"])) else b)
        other = b if prim is a else a
        evidence = merge_text(a, b) if pick == "merge" else prim["evidence"]
        if pick != "merge" and other and other["source_url"] != prim["source_url"]:
            evidence += f" Other coder: {other['evidence']}"
        tier = d["tier"] or min(x["tier"] for x in (a, b) if x)
        conf = d["conf"] or prim["confidence"]
        url = d["url"] or prim["source_url"]
        cell = dict(position=pos, evidence=evidence + f" Reconciler: {d['note']}", source_url=url, tier=tier,
                    confidence=conf, coders_agreed=(av == bv and av is not None),
                    reconciled_from={"A": av, "B": bv})
        if other and other["source_url"] != url:
            cell["source_url_2"] = other["source_url"]
        log = dict(statement=stmt, party=party, A=av, B=bv, adopted=pos, reason=d["note"])
        return cell, log, av, bv
    # automatic merge of identical codings
    if a is None and b is None:
        return None, None, av, bv
    assert a and b and av == bv, (stmt, party, av, bv)
    prim = a if a["tier"] <= b["tier"] else b
    other = b if prim is a else a
    if a["source_url"] != b["source_url"]:
        conf = max((a["confidence"], b["confidence"]), key=lambda c: CONF_RANK[c])
    else:
        conf = min((a["confidence"], b["confidence"]), key=lambda c: CONF_RANK[c])
    cell = dict(position=av, evidence=merge_text(a, b), source_url=prim["source_url"], tier=min(a["tier"], b["tier"]),
                confidence=conf, coders_agreed=True, reconciled_from={"A": av, "B": bv})
    if other["source_url"] != prim["source_url"]:
        cell["source_url_2"] = other["source_url"]
    return cell, None, av, bv

# ----------------------------------------------------------------------------------------------------
statements, logs = [], []
stats = dict(cells_both_coded=0, identical=0, within1=0, opposite_sign=0, single_coder_cells=0,
             adopted_from_single_coder=0, single_coder_downgraded_to_null=0, disagreements_resolved=0,
             both_coded_downgraded_to_null=0, inference_cells_reduced_to_pm1=0)
for sid in STATEMENT_IDS:
    s = SA[sid]
    positions = {}
    for p in PARTIES:
        cell, log, av, bv = build_cell(sid, p)
        if av is not None and bv is not None:
            stats["cells_both_coded"] += 1
            if av == bv: stats["identical"] += 1
            if abs(av - bv) <= 1: stats["within1"] += 1
            if av * bv < 0: stats["opposite_sign"] += 1
            if av != bv:
                stats["disagreements_resolved"] += 1
                if cell is None: stats["both_coded_downgraded_to_null"] += 1
        elif av is not None or bv is not None:
            stats["single_coder_cells"] += 1
            if cell is None: stats["single_coder_downgraded_to_null"] += 1
            else: stats["adopted_from_single_coder"] += 1
        if log:
            logs.append(log)
            if "section 4.1(3)" in log["reason"] and log["adopted"] is not None and \
               (abs(av or 0) == 2 or abs(bv or 0) == 2):
                stats["inference_cells_reduced_to_pm1"] += 1
        positions[p] = cell
    dim = sid[0]
    statements.append(dict(id=sid, dimension=dim, dimension_label=DIMENSIONS[dim],
                           pole_a=POLES[dim][0], pole_b=POLES[dim][1],
                           text=s["text"], polarity=s["polarity"],
                           polarity_sign=1 if s["polarity"] == "+A" else -1,
                           positions=positions))

stats["exact_pct"] = round(100 * stats["identical"] / stats["cells_both_coded"], 1)
stats["within1_pct"] = round(100 * stats["within1"] / stats["cells_both_coded"], 1)
stats["downgraded_to_null"] = stats["single_coder_downgraded_to_null"] + stats["both_coded_downgraded_to_null"]
# Krippendorff-style simple summary: per-value distribution of differences
diffs = {}
for sid in STATEMENT_IDS:
    for p in PARTIES:
        a = SA[sid]["positions"].get(p); b = SB[sid]["positions"].get(p)
        if a and b:
            d_ = abs(a["position"] - b["position"]); diffs[d_] = diffs.get(d_, 0) + 1
stats["difference_distribution"] = {str(k): v for k, v in sorted(diffs.items())}

parties = {}
for p in PARTIES:
    n = sum(1 for s in statements if s["positions"][p] is not None)
    low = sum(1 for s in statements if s["positions"][p] and s["positions"][p]["confidence"] == "low")
    zeros = sum(1 for s in statements if s["positions"][p] and s["positions"][p]["position"] == 0)
    tiers = {}
    for s in statements:
        c = s["positions"][p]
        if c: tiers[str(c["tier"])] = tiers.get(str(c["tier"]), 0) + 1
    parties[p] = dict(name=PARTY_NAMES[p], positions_recorded=n, low_confidence_cells=low, argued_neutral_cells=zeros,
                      tier_counts=dict(sorted(tiers.items())),
                      in_default_ranking=n >= 15,
                      coverage_note=None if n >= 15 else "fewer than 15 of 30 positions: shown with a 'limited information' badge and excluded from the default ranking")

# blind check: no party, leader, Act or scheme names in statement text
BLIND = re.compile(r"\b(National|Labour|Greens?|ACT|NZ First|New Zealand First|Te P[āa]ti M[āa]ori|TOP|Opportunit(y|ies) Party|Luxon|Hipkins|Seymour|Peters|Swarbrick|Davidson|Waititi|Ngarewa-Packer|Manji|Treaty Principles Bill|Fast-?track Approvals|Three Strikes|Regulatory Standards|Gangs? Act|Māori Health Authority|Te Aka Whai Ora|ETS|Emissions Trading Scheme|Paris Agreement|AUKUS|Five Eyes|Kāinga Ora|Pharmac|KiwiSaver|Working for Families|Fair Pay Agreements?|He Puapua|Matike Mai|Three Waters|Act\s+\d{4}|\w+ Act\b|\w+ Bill\b|\d)")
for s in statements:
    m = BLIND.search(s["text"])
    assert not m, f"blind check failed on {s['id']}: {m.group(0)!r}"
    if " not " in f" {s['text']} " or "n't" in s["text"]:
        print(f"note: '{s['id']}' contains a negation word inside a clause (checked by hand: not a negated proposal)")
    assert len(s["text"].split()) <= 40, s["id"]

SCORING = {
    "scale": {"-2": "Strongly disagree", "-1": "Disagree", "0": "Neutral", "1": "Agree", "2": "Strongly agree",
              "skip": "No opinion / skip (excluded from the match)"},
    "party_scale": "-2..+2 as coded; 0 = argued neutral (counts as a position); null = no position found (excluded, never shown as neutral)",
    "importance_weights": {"less": 0.5, "normal": 1.0, "very": 2.0},
    "agreement": "a_ij = 1 - |u_i - p_ij| / 4   (city-block, in [0,1]) over S_j = statements the user answered and party j has a non-null position",
    "raw_match": "raw_j = sum_{i in S_j} w_i * a_ij / sum_{i in S_j} w_i",
    "shrinkage": {"formula": "match_j = (sum_{i in S_j} w_i * a_ij + k * 0.5) / (sum_{i in S_j} w_i + k)", "k": 4,
                  "note": "shrinks toward the uninformative value 0.5 by k phantom neutral statements"},
    "coverage_rule": {"default_ranking_if": "|S_j| >= max(10, 0.5 * M), where M = number of statements the user answered",
                      "otherwise": "listed separately with the badge 'based on only N of your M answers' and the shrunk score",
                      "party_level_badge": "parties with fewer than 15 of 30 coded positions carry a 'limited information' badge and are excluded from the default ranking"},
    "dimension_agreement": "A_jd = sum_{i in d and S_j} w_i a_ij / sum_{i in d and S_j} w_i, reported as agreement on N of the dimension's statements",
    "dimension_map": {"formula": "x_d = mean_i(s_i * v_i) / 2 in [-1, +1], over the dimension's statements with a value; s_i = polarity_sign (+1 for '+A' items, -1 for '+B' items); v_i = user answer or party position",
                      "meaning": "+1 = pole A, -1 = pole B; agreeing with a '+B' statement moves toward pole B",
                      "status": "secondary illustration; the ranking uses all statements, never the map"},
    "uncertainty_band": "recompute match_j (a) with every low-confidence party cell set to null and (b) with every +/-1 party cell moved one step toward and away from the user; show min-max as a thin band; show the count of low-confidence cells",
    "display": ["ranked list with visible gaps", "whole percentages only", "ties within 2 points shown as ties",
                "'based on N of your M answers' on every party", "per-dimension agreement with evidence links",
                "unweighted result beside the weighted one", "freeze date and method link", "no 'advice' or 'recommendation' wording",
                "statement order randomised per session, no topic headers while answering", "party positions revealed only after all answers"],
    "unit_tests": ["identical answers -> 100", "opposite extremes -> 0 before shrinkage", "skipped, no-opinion and null cells excluded",
                   "weights applied", "k shrinkage: 30 cells at raw 0.70 -> 0.676"],
}

out = {
    "version": "2026-10-v2",
    "generated": datetime.date(2026, 10, 23).isoformat(),
    "freeze_date": "2026-10-23",
    "about": "Party positions on 30 statements, coded independently by two coders from published sources (manifesto first, then votes, questionnaire answers, dated statements, coalition actions) and reconciled by a third reviewer. Evidence, URL, tier and confidence are published for every cell. See guide/quiz-method.md and raw/quiz2/RECONCILIATION.md.",
    "dimensions": {k: {"label": v, "pole_a": POLES[k][0], "pole_b": POLES[k][1]} for k, v in DIMENSIONS.items()},
    "evidence_tiers": {"1": "party's 2026 manifesto / policy document / policy page", "2": "recorded party vote in the 54th Parliament on legislation enacting or repealing the proposal",
                       "3": "party's own written answer to a third-party questionnaire (Greenpeace, NZCTU, Grey Power, KPMG tracker)", "4": "dated statement by the leader or portfolio spokesperson",
                       "5": "coalition agreement commitment or government action attributable to the party (flagged)"},
    "statements": statements,
    "parties": parties,
    "agreement": {k: stats[k] for k in ["cells_both_coded", "exact_pct", "within1_pct", "opposite_sign", "difference_distribution",
                                         "single_coder_cells", "adopted_from_single_coder", "downgraded_to_null",
                                         "single_coder_downgraded_to_null", "both_coded_downgraded_to_null", "disagreements_resolved",
                                         "inference_cells_reduced_to_pm1"]},
    "scoring": SCORING,
    "blind_check": "no party, leader, Act or scheme names in statement text (asserted by regex at build time; also no negations and no statement over 40 words)",
    "reconciliation_log": logs,
    "sources": {"coder_a": "data/guide/quiz2-coder-a.json", "coder_b": "data/guide/quiz2-coder-b.json",
                "notes": ["raw/quiz2/coder-a/NOTES.md", "raw/quiz2/coder-b/NOTES.md", "raw/quiz2/RECONCILIATION.md"]},
}
json.dump(out, open(ROOT / "data/guide/quiz2.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(out["agreement"], indent=1))
for p, v in parties.items():
    print(f"{v['name']:24s} {v['positions_recorded']:2d}  low={v['low_confidence_cells']:2d} zeros={v['argued_neutral_cells']}")
print("non-null cells:", sum(v["positions_recorded"] for v in parties.values()))
