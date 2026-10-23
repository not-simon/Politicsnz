"""Hand-written catalogue of 2026 policies for the minor parties / electorate-only groups (and TOP extras).

Every entry's statement/why/how is a neutral summary written for this archive (summary_source "archive") from the
party's own document(s) listed in `docs` (document slugs under parties/<party>/policies/documents/). "why" records
the party's own stated reason (attributed), "how" what it says it would do. Nothing here is the party's verbatim text.
Consumed by tools/policies_minor_build.py.
"""


def P(id, statement, topics, why, how, docs, key=False):
    return {"id": id, "statement": statement, "topics": topics, "why": why, "how": how, "docs": docs, "key": key}


CATALOG = {}
META = {}

# ------------------------------------------------------------------------------------------------ Te Tai Tokerau Party
TTP = ["ttp-pataka-policy"]
META["te-tai-tokerau-party"] = {
    "name": "Te Tai Tokerau Party", "website": "https://tetaitokerauparty.org.nz/",
    "registered": "5 August 2026 (Electoral Commission register)",
    "intro": "The Te Tai Tokerau Party was launched by Te Tai Tokerau MP Mariameno Kapa-Kingi in May 2026 after her split "
             "from Te Pāti Māori. Its whole platform is published on one page, \"TTP Pātaka Policy\", organised in five "
             "pillars (Whānau, Whare, Whenua, Tino Rangatiratanga, Ōhanga Ā-Rohe). Each named policy on that page is listed "
             "below. The page does not give costings except where noted.",
    "gaps": "The \"Tai Tokerau Fund\" policy is marked by the party as \"in development\". No separate PDFs, press releases or costings were found on the site.",
}
CATALOG["te-tai-tokerau-party"] = [
    P("TTP-01", "Pass Te Ture Mokopuna (the Mokopuna Act) requiring government decisions to consider current and future generations of mokopuna",
      ["community-and-inclusion", "young-people", "law-justice-and-government", "parliament-and-democracy"],
      "The party calls this its flagship policy, modelled on Wales's Well-being of Future Generations Act 2015 and grounded in mātauranga Māori and Te Tiriti.",
      "Public bodies would be bound by a 'Mokopuna Principle', report annually against mokopuna wellbeing goals, carry out Mokopuna Impact Assessments on significant laws, Budgets and projects, and be monitored by an independent Commissioner for Mokopuna using co-designed national indicators.",
      TTP, key=True),
    P("TTP-02", "Create a Crown–Iwi Investment Fund and give mana whenua a 25% equity stake in major regional infrastructure",
      ["te-ao-maori", "land-and-resources", "economy", "economic-development-and-industry"],
      "The party says the state should co-invest in iwi- and hapū-owned assets so whānau become owners in the value chain rather than low-wage labour.",
      "A Crown–Iwi Investment Fund for 'transition infrastructure' (renewable energy, green hydrogen, digital); major regional projects such as wind farms would have to offer at least 25% equity to local mana whenua, funded by low-interest government loans.",
      TTP),
    P("TTP-03", "Wipe low-income whānau debt to MSD and IRD and replace the benefit system with a Universal Whānau Allowance",
      ["incomes-and-employment", "benefits", "tax-and-income-support"],
      "The party says whānau cannot retrain or innovate while being penalised by MSD, and that the current system creates a poverty trap.",
      "An immediate amnesty on about $2 billion of debt owed by low-income whānau to MSD and IRD; a simplified, non-taxable Universal Whānau Allowance for people in training or caregiving; and an end to 'relationship status' policing in the benefit system.",
      TTP, key=True),
    P("TTP-04", "Adopt a 'prison sinking lid' that diverts non-violent offenders with addiction or mental-health needs into hapū-run rehabilitation",
      ["law-justice-and-government", "criminal-justice", "health", "mental-health"],
      "The party says each prisoner costs over $150,000 a year while reoffending stays high, and that rural communities lack preventative resources.",
      "Corrections savings from each bed vacated through health-focused diversion would be legally transferred to local hapū-led rehabilitation trusts running secure, alcohol- and drug-free 'healing sanctuaries', with mandatory restorative work programmes for those diverted.",
      TTP),
    P("TTP-05", "Establish Te Aka Motuhake, a fully iwi-governed Māori health commissioning authority, plus a bonded iwi health scholarship scheme",
      ["health", "health-services", "health-funding-and-workforce", "te-ao-maori"],
      "The party rejects the mainstreaming of indigenous health structures and wants to fix the Māori health workforce shortage.",
      "An autonomous, state-funded but iwi-governed health authority controlling clinical design, regional funding and provider licensing; an uncapped scholarship bonding graduates to Māori, iwi or rural providers for at least four years; and more diagnostic, preventative and dental services delivered from tribal hubs.",
      TTP),
    P("TTP-06", "Fund 'Backyard Sovereignty Kits' (garden beds, chickens, rain tanks) and deregulate small-scale local food trade",
      ["incomes-and-employment", "prices", "economy", "agriculture"],
      "The party says supermarket prices are crippling for Northland whānau and that home food production should be treated as regional infrastructure.",
      "Funded flat-pack kits with raised beds, soil, seeds, a predator-proof coop and laying hens; rain-water catchment and irrigation; mobile gardening mentors; and an exemption of hyper-local household food barter and sales from council licensing and transaction taxes.",
      TTP),
    P("TTP-07", "Provide free solar power, home-delivered kai and paid cultural roles for kaumātua",
      ["community-and-inclusion", "superannuation-and-savings", "energy"],
      "The party says many kaumātua live in energy poverty and are cut off from whānau and tribal roles.",
      "Prioritise elder-occupied homes for fully funded solar and batteries on community grids with zero-cost baseline electricity; monthly fresh-food prescription vouchers delivered to homes; paid mentorship roles for kaumātua and kuia; and paid, trained in-home carers drawn from local whānau ('Ringa Manaaki Dividend').",
      TTP),
    P("TTP-08", "Train local rangatahi to build hempcrete homes on papakāinga through a Rohe Construction Academy",
      ["housing", "housing-quality", "construction", "education", "trades-and-vocational-education"],
      "The party links overcrowded, damp housing to high rates of rheumatic fever and respiratory illness and says imported materials make building expensive.",
      "A funded trade academy in Te Tai Tokerau paying trainees a living wage; regional plants turning local hemp hurd and lime into certified building panels; and homes built on ancestral land and papakāinga, allocated first to overcrowded families and bypassing commercial developers.",
      TTP),
    P("TTP-09", "Set up a $150m-a-year Kaitiaki Guardians Network with statutory environmental enforcement powers",
      ["environment", "conservation", "te-ao-maori", "land-and-resources"],
      "The party wants Māori to move from being 'consulted' on the environment to being its legal 'eyes and ears'.",
      "A $150 million annual Crown appropriation for iwi- and hapū-led guardian teams with statutory power to monitor and enforce environmental rules in their rohe, including issuing protection notices for urupā, marae and biodiversity hotspots.",
      TTP),
    P("TTP-10", "Create a Whenua Climate Restoration Fund giving iwi first right of refusal to buy back low-lying and coastal land, and a Māori Biodiversity Credit System",
      ["environment", "climate-adaptation", "te-ao-maori", "land-and-resources"],
      "The party says climate adaptation needs space and that iwi should control ecosystems that buffer against sea-level rise and food insecurity.",
      "A fund backing a compulsory first right of refusal for iwi to buy ecologically significant low-lying and coastal land, and Crown payments to whānau and iwi for carbon sequestration and ecosystem services from restored forests and wetlands.",
      TTP),
    P("TTP-11", "Make marae official off-grid Civil Defence hubs with funded energy, water, stockpiles and training",
      ["environment", "climate-adaptation", "community-and-inclusion", "te-ao-maori"],
      "The party says marae already open their doors in emergencies long before state agencies arrive.",
      "Fund solar, batteries, rainwater collection and filtration at designated marae; stock emergency supplies and satellite communications; and legally designate marae as co-equal Civil Defence hubs under NEMA with funded emergency training for whānau.",
      TTP),
    P("TTP-12", "Replace marine law with a Moana Ora Act protecting 30% of territorial waters through iwi/hapū-managed areas",
      ["environment", "oceans", "fisheries", "te-ao-maori"],
      "The party says current marine management is fragmented and ignores customary rights.",
      "Repeal and replace marine legislation with an act mandating Indigenous Protected and Conserved Areas, a binding 30% protection target co-designed and managed by iwi/hapū (including seasonal rāhui), an end to destructive bottom trawling and secured customary fishing rights.",
      TTP),
    P("TTP-13", "Constitutionally protect He Whakaputanga and Te Tiriti, and repeal the Regulatory Standards Act 2025 and the Treaty Clauses Review",
      ["te-ao-maori", "te-tiriti-o-waitangi-and-governance", "law-justice-and-government"],
      "The party notes that both founding documents were signed in Te Tai Tokerau and wants protection against legislative harm to them.",
      "Advance a Tiriti-centred constitution led by community voices, and, as a priority, vote to repeal the Regulatory Standards Act 2025 and the Treaty Clauses Review.",
      TTP, key=True),
    P("TTP-14", "Increase and entrench Waitangi Tribunal funding and make its findings binding on the Crown beyond specific land types",
      ["te-ao-maori", "te-tiriti-o-waitangi-and-governance"],
      "The party sees the Tribunal as a forum for justice relied on by whānau.",
      "Raise and entrench funding (amount to be set after talks with the Tribunal and whānau) and extend the Tribunal's binding jurisdiction over the Crown.",
      TTP),
    P("TTP-15", "Fund tangata whenua-led Te Tiriti education in the curriculum, the public service and for all MPs",
      ["te-ao-maori", "education", "schools", "te-tiriti-o-waitangi-and-governance"],
      None,
      "More funding for Te Tiriti education led by tangata whenua, embedded in the NZ Curriculum and in public-service professional development, including for all sitting MPs.",
      TTP),
    P("TTP-16", "Redirect 20% of Crown revenue from conservation and public land into a Māori-governed land-buyback fund",
      ["te-ao-maori", "land-and-resources", "te-tiriti-o-waitangi-and-governance"],
      "The party wants to replace lengthy land-return negotiations with automatic, revenue-backed mechanisms.",
      "Legislate a mandatory 20% redirection of Crown revenues from conservation and public lands into a Māori-governed Land Acquisition Fund, remove LINZ's disposal authority and automatically return unused public-works land to its original owners, with a right of first refusal to buy back private land.",
      TTP),
    P("TTP-17", "Create Te Whare Tohu Tātai, an independent Māori data and Crown-compliance commission",
      ["te-ao-maori", "te-tiriti-o-waitangi-and-governance", "public-sector"],
      None,
      "A statutory commission to monitor Crown compliance with all historical settlements, with ownership and control of all state data about Māori whānau and enforcement powers.",
      TTP),
    P("TTP-18", "Pass a Māori Justice & Autonomous Policing Act transferring youth-justice funding to iwi-governed authorities",
      ["law-justice-and-government", "criminal-justice", "policing", "te-ao-maori"],
      "The party says state-controlled corrections and punitive policing entrench institutional inequity.",
      "Transfer regional youth-justice budgets to iwi-governed, marae-anchored authorities and fund iwi-administered community safety services under tribal jurisdiction, with restorative justice replacing incarceration.",
      TTP),
    P("TTP-19", "Build Local Business Incubators in Whangārei, Kaikohe and Kaitaia with a five-year 100% tax holiday for start-ups",
      ["economy", "regional-development", "business-support"],
      "The party says young people leave the North because it lacks high-spec commercial infrastructure.",
      "Funded co-working spaces with fibre, fabrication labs and studios; businesses based in the incubators would pay no 'regional corporate income tax' for five years if local payroll and staffing targets are met; plus mentoring and seed grants.",
      TTP),
    P("TTP-20", "Require government agencies to buy 10% (rising to 15% by 2030) of goods and services from Māori-owned and local businesses",
      ["economy", "regional-development", "te-ao-maori", "jobs-and-employment"],
      "The party says state money spent in the regions should stay there.",
      "A 'Social & Indigenous Procurement Mandate' for schools, hospitals and construction, a 35% local Māori employment and 50% youth/apprenticeship target on regional projects, and 'Farm to School' purchasing of Māori-grown food.",
      TTP),
    P("TTP-21", "Fund community-owned Kai Sovereignty food hubs and require Northland supermarkets to give 30% of shelf space to local produce",
      ["incomes-and-employment", "prices", "economy", "agriculture"],
      "The party says the supermarket duopoly trucks northern produce to Auckland and back with large markups.",
      "Fund regional processing hubs (kitchens, cold storage, butchery, packing), support direct-to-consumer networks, and require supermarkets in Te Tai Tokerau to allocate at least 30% of shelf space to locally grown unprocessed food bought from regional suppliers.",
      TTP),
    P("TTP-22", "Create a Tai Tokerau Fund modelled on the Provincial Growth Fund, specific to iwi (details in development)",
      ["economy", "regional-development", "te-ao-maori"],
      None,
      "The party lists a regional, iwi-specific fund modelled on the Provincial Growth Fund; its page says full detail is still in development.",
      TTP),
]

# ------------------------------------------------------------------------------------------------ Opportunity (TOP)
_tax = ["pdf-tax-reset", "pdf-tax-reset-transition-plan", "release-2026-05-tax-reset"]
_en = ["pdf-abundant-energy", "pdf-abundant-energy-paper"]
_oc = ["pdf-healthy-oceans", "release-2026-04-healthy-oceans-dunedin"]
_pol = ["pdf-clean-up-politics", "web-bottom-lines"]
_inf = ["pdf-intergenerational-infrastructure", "release-2026-08-intergenerational-infrastructure"]
_cl = ["pdf-climate-action"]
_ed = ["pdf-future-fit-education"]
_be = ["pdf-breakthrough-economy", "release-2026-07-breakthrough-economy"]
OPP_RELATED = {
    "POL54777": _tax, "POL54816": _tax, "POL54818": _tax,
    "POL54770": _en, "POL54806": _en, "POL54807": _en, "POL55049": _en,
    "POL54776": _oc + ["web-bottom-lines"], "POL54825": _oc, "POL54826": _oc, "POL54827": _oc,
    "POL54778": _pol, "POL54808": _pol, "POL54809": _pol, "POL54784": ["pdf-citizens-voice"],
    "POL54779": _be + ["pdf-digital-future"], "POL54824": _be + ["web-bottom-lines"], "POL54852": _be,
    "POL54785": _inf, "POL54874": _inf, "POL54875": _inf, "POL54811": _inf,
    "POL54786": ["release-2026-04-free-public-transport"],
    "POL54853": ["pdf-affordable-housing"], "POL54873": ["pdf-affordable-housing"],
    "POL54854": ["pdf-smart-on-crime"], "POL54855": ["pdf-smart-on-crime"],
    "POL54810": _cl, "POL54782": _cl + ["web-bottom-lines"], "POL55169": _cl + ["web-bottom-lines"], "POL55175": _cl,
    "POL54791": _cl, "POL54876": _cl, "POL54900": _cl + ["web-industry-energy-resilience-fund"],
    "POL54823": ["web-healthy-people", "web-bottom-lines"], "POL54871": ["web-healthy-people", "web-bottom-lines"],
    "POL54885": ["web-healthy-people"],
    "POL54860": _ed, "POL54861": _ed, "POL54862": _ed, "POL54869": _ed,
    "POL54828": _ed + ["pdf-honouring-te-tiriti"], "POL54829": ["pdf-honouring-te-tiriti"],
}
META["opportunity"] = {
    "name": "Opportunity (The Opportunity Party, TOP)", "website": "https://www.opportunity.org.nz/",
    "registered": "6 March 2017 (Electoral Commission register)",
    "intro": "Opportunity (leader Qiulae Wong) publishes its platform as 15 policy pages (priority policies: Abundant Energy, "
             "Breakthrough Economy, Clean Up Politics, Healthy Oceans, Tax Reset; plus Citizens' Voice, Future-fit Education, "
             "Healthy People, Honouring Te Tiriti, Smart on Crime, Affordable Housing, Digital Future, Inter-Generational "
             "Infrastructure, Climate Action, Healthy Land & Water), most with a downloadable PDF policy paper, plus statements "
             "and five election \"bottom lines\". The list below starts from policy.nz's 56 statements for the party (with "
             "policy.nz's own Why/How text) and adds policies from TOP's documents that policy.nz does not list (IDs OPP-A..).\n\n"
             "**How the text was obtained.** www.opportunity.org.nz is behind a Cloudflare bot challenge (HTTP 403 to curl and "
             "headless Chromium) and web.archive.org is unreachable from this environment, so web pages were recovered from "
             "**Common Crawl** WARC captures (crawls CC-MAIN-2026-30/34/39/43; capture date in each document's front matter) via "
             "[`tools/policies_minor_cc.py`](../../../tools/policies_minor_cc.py). The 15 policy PDFs were downloaded directly from "
             "cdn.opportunity.org.nz (not blocked). Press releases are also taken from their scoop.co.nz mirrors.",
    "gaps": "Three pages cited by policy.nz have no Common Crawl capture and could not be retrieved: /healthy_land "
            "(Healthy Land & Water policy — water quality, gene technology context), /disability_statement and "
            "/arts_and_culture_statement; their documents say so explicitly, and the policy.nz summaries are kept. Common "
            "Crawl captures date from July–October 2026 and may predate later edits. Note that the Citizens' Voice PDF is dated "
            "June 2025. The NZ Herald reported (Oct 2026) that tax reform is not among TOP's five bottom lines; the Tax Reset "
            "remains on its policy page. Web search capacity ran out during research, so further Scoop mirrors were not sought.",
}
CATALOG["opportunity"] = [
    P("OPP-A01", "Five 'bottom lines' for supporting any government: Commerce Commission break-up powers, lobbying and donation reform, a 10-year health plan, ending bottom trawling, and Paris/Climate Commission commitments",
      ["law-justice-and-government", "parliament-and-democracy"],
      "Opportunity says no party can achieve its whole platform under MMP, so it names five non-negotiable policies any governing partner must accept.",
      "(1) empower the Commerce Commission to investigate, intervene and force structural separation; (2) a mandatory lobbyist register and code of conduct and a per-donor cap with donations from registered voters only; (3) a 10-year cross-party health plan; (4) an immediate end to bottom trawling in the most damaged inshore areas such as the Hauraki Gulf, then a staged phase-out; (5) recommit to Paris obligations and protect the Climate Change Commission. It adds that honouring Te Tiriti is an approach it will bring to negotiations.",
      ["web-bottom-lines"], key=True),
    P("OPP-A02", "Realign income tax to three rates: 28% up to $50,000, 34% to $200,000 and 39% above", ["incomes-and-employment", "tax-and-income-support"],
      "Part of the Tax Reset, which Opportunity says simplifies tax and removes secondary tax rates.", "New brackets alongside the Citizen's Income, Land Value Tax and KiwiSaver 2.0.", ["pdf-tax-reset"]),
    P("OPP-A03", "Replace Working for Families and most benefits with tax-free Child Support Incomes and fixed top-ups", ["incomes-and-employment", "benefits"],
      "Opportunity says the benefit system traps people in poverty with effective marginal tax rates of up to 90%.",
      "Per-child payments starting at $18,250 for a first child in the first year and falling to $7,750 for ages 4–18, plus a $9,500 sole-parent allowance, a $6,000 disability allowance, superannuitant top-ups and regional Housing Support Income payments.",
      ["pdf-tax-reset"]),
    P("OPP-A04", "Phase in the Tax Reset over about a decade, starting with 18–29-year-olds and a 0.5% urban-only land tax", ["incomes-and-employment", "tax-and-income-support", "economy"],
      "Opportunity says changes of this scale must be introduced carefully to avoid inflation and disruption.",
      "Two years of planning first; Citizen's Income rolled out in age tranches of about 25% of the population; Land Value Tax starting at 0.5% on urban land and rising to 1.75%/0.5% rural by year 6; KiwiSaver 2.0 contributions rising 1% a year over six years.",
      ["pdf-tax-reset-transition-plan"]),
    P("OPP-A05", "Allow only registered voters to donate to parties, cut the disclosure threshold to $1,000 and cap spending across the whole electoral cycle", ["law-justice-and-government", "parliament-and-democracy"],
      "Opportunity says it wants to 'sever the link' between donations and political influence.",
      "Ban donations from companies, trusts and other entities and from non-voters; require audited annual party statements; apply advertising spending limits over the full three-year cycle with quarterly Electoral Commission summaries.",
      ["pdf-clean-up-politics"]),
    P("OPP-A06", "Impose a one-year cooling-off period before ministers, senior staff and officials can become lobbyists", ["law-justice-and-government", "parliament-and-democracy", "public-sector"],
      None, "Part of its lobbying regulation, alongside a statutory code of conduct, a ban on contingency fees and foreign-lobbying disclosure.", ["pdf-clean-up-politics"]),
    P("OPP-A07", "Strengthen the Official Information Act, MPs' pecuniary-interest rules and whistleblower protections, and create an independent policy costing unit", ["law-justice-and-government", "parliament-and-democracy", "public-sector"],
      "Opportunity says good rules mean little without institutions that enforce them.",
      "Narrower OIA withholding grounds, lower pecuniary-interest thresholds, broader whistleblower coverage, a better-funded Electoral Commission and a costing unit available to all registered parties.",
      ["pdf-clean-up-politics"]),
    P("OPP-A08", "Require Opportunity MPs to rent from unrelated parties rather than use allowances on property they own, and seek a full review of MP entitlements", ["law-justice-and-government", "parliament-and-democracy"],
      "Opportunity says public money should not build MPs' private property wealth or flow back to parties or donors.",
      "Its MPs would only claim actual, reasonable accommodation costs paid to an unrelated third party and would not lease property linked to the MP, party or major donors; it would seek a review of allowances including those for former MPs and spouses.",
      ["web-opportunity-accommodation-allowance-policy", "release-2026-06-mp-allowances"]),
    P("OPP-A09", "Require AI data centres to fund their own clean energy, pay full grid-connection costs and report energy and water use", ["economy", "internet-and-digital-technologies", "energy"],
      "Part of Digital Future, which Opportunity says sets guardrails to protect people, data and the environment.", None, ["web-digital-future", "pdf-digital-future"]),
    P("OPP-A10", "Require New Zealanders' critical data to be hosted onshore and favour local and open-source suppliers in government tech purchasing", ["economy", "internet-and-digital-technologies", "public-sector"],
      None, "Also: a public register of government technology projects, recognition of Māori Data Sovereignty Principles in public-sector AI procurement, more cyber-security funding and a review of rights in an AI world (algorithmic bias, copyright).",
      ["web-digital-future", "pdf-digital-future"]),
    P("OPP-A11", "Introduce a 25% tax credit for small businesses adopting new technology and a cross-party national AI framework", ["economy", "business-support", "internet-and-digital-technologies"],
      None, "A tax credit to help SMEs adopt cutting-edge tools and a national framework on data rights, IP and investment 'shaped by the New Zealand public directly'.", ["web-digital-future", "pdf-breakthrough-economy"]),
    P("OPP-A12", "Restore polytechnic baseline funding and give polytechs a mandate to lead regional productivity", ["education", "trades-and-vocational-education", "economy"],
      "Opportunity says polytechnics can anchor regional, job-focused training and help local businesses.", "Restore funding cut by the current government and bulk-fund polytechnics and public research organisations for technology transfer.", ["pdf-breakthrough-economy"]),
    P("OPP-A13", "Double government funding for start-up incubators, accelerators, deep-tech programmes and Young Enterprise", ["economy", "business-support"], None, "As stated in the Breakthrough Economy policy.", ["pdf-breakthrough-economy"]),
    P("OPP-A14", "Agree a population policy for stable long-term immigration", ["migration"],
      "Opportunity says immigration brings skills and capital but has not been matched by infrastructure and planning.", "A population policy linking immigration to investment in infrastructure, planning and social programmes.", ["pdf-breakthrough-economy"]),
    P("OPP-A15", "Create an 'Impact Company' legal structure and expand support for small businesses", ["economy", "business-support"], None,
      "Amend the Companies Act for a for-profit entity with social purpose; fund FinCap and financial-capability services; review ACC levies toward risk-weighting; reverse the ban on merchant surcharges; speed up R&D tax credit processing; and create a Consumer Advocacy Fund.", ["pdf-breakthrough-economy"]),
    P("OPP-A16", "Restore pre-2025 customary marine title settings and review recent changes to statutory Treaty clauses", ["te-ao-maori", "te-tiriti-o-waitangi-and-governance"],
      None, "Honour existing settlements and complete outstanding ones; restore pre-2025 Marine and Coastal Area settings; review Treaty provisions statute by statute; support a national constitutional conversation using deliberative processes with Māori as Treaty partner.", ["pdf-honouring-te-tiriti", "web-honouring-te-tiriti"]),
    P("OPP-A17", "Adopt a presumption in favour of devolving services to Māori organisations where it improves outcomes, and improve Māori access to capital", ["te-ao-maori", "public-sector"],
      None, "Match Māori decision-making authority to the issue, give devolved bodies operational autonomy and longer-term funding, evaluate and expand what works, and support financing models for Māori assets.", ["pdf-honouring-te-tiriti"]),
    P("OPP-A18", "Restore an independent Teaching Council and raise entry standards for teacher training", ["education", "schools"],
      None, "Higher initial teacher-education entry requirements, funded professional development and induction, a restored independent Teaching Council with elected members, and an empowered Curriculum and Assessment Council.", ["pdf-future-fit-education"]),
    P("OPP-A19", "Set minimum child-to-teacher ratios in early childhood education (1:3 under twos) and move to quality-based contracting", ["education", "early-childhood-education"],
      None, "Ratios of 1:3 for under-twos, 1:5 for 2–3 year-olds and 1:8 for older children, maximum group sizes, 80% qualified staff in teacher-led services, and more core funding for community-owned services.", ["pdf-future-fit-education"]),
    P("OPP-A20", "Reinstate the Smokefree 2025 legislation", ["health", "public-health"], None, "Listed on the Healthy People policy page.", ["web-healthy-people"]),
    P("OPP-A21", "Reverse the Government's plan for an LNG import terminal in Taranaki", ["transport-and-infrastructure", "energy"],
      "Opportunity says tying the grid to volatile imported gas would not serve communities or businesses.", "Calls on the Government to reverse the decision and points to its Abundant Energy plan.", ["web-call-for-government-reversal-on-lng-terminal"]),
]

# ------------------------------------------------------------------------------------------------ Vision NZ
VIS = ["vision-policies"]
META["vision-nz"] = {
    "name": "Vision NZ (Vision New Zealand)", "website": "https://www.vision.org.nz/",
    "registered": "4 December 2019 (Electoral Commission register)",
    "intro": "Vision NZ, led by Hannah Tamaki, publishes its platform on a single \"Our Policies\" page in nine sections, each "
             "with a list of \"Policy Commitments\" followed by a policy overview. Every listed commitment is entered below "
             "as a separate policy (the \"Why\" lines paraphrase the section overview).",
    "gaps": "No costings, PDFs or fuller policy documents were found on vision.org.nz. The page gives no amounts for the "
            "weekly 'Family Empowerment Grant 2' or the newborn birth payment.",
}
_why_fam = "Vision NZ says the family is the cornerstone of society and that state agencies and regulation have eroded parents' confidence and authority."
_why_col = "Vision NZ says middle-class families are being pushed to the brink by the cost of living, including the price of locally grown food."
_why_edu = "Vision NZ says education standards have declined because schools shifted from core academics to 'social engineering'."
_why_law = "Vision NZ says the system relies too heavily on distant agencies and wants community-led action to make neighbourhoods safe."
_why_inf = "Vision NZ says central-government transport planning ignores daily life and that fast-growing areas are left behind."
_why_id = "Vision NZ says it stands for one unified country free of 'global overreach' and race-based politics."
_why_sex = "Vision NZ says biological sex should be upheld in law to protect women's privacy, safety and rights, and to protect children."
_why_hlth = "Vision NZ says the health system is strained by waitlists and GP shortages while money goes to administration and race-based spending."
_why_dem = "Vision NZ says MMP list MPs are unelected and wants a smaller, more accountable Parliament."
CATALOG["vision-nz"] = [
    P("VIS-01", "Create a Ministry for Families", ["community-and-inclusion", "public-sector"], _why_fam,
      "A dedicated ministry to act as a watchdog against state over-reach and promote solutions for households.", VIS, key=True),
    P("VIS-02", "Reverse policies that override parents' rights, responsibilities, knowledge or consent", ["community-and-inclusion", "family-justice-and-safety"], _why_fam,
      "Protect the 'nuclear family' by reversing such policies (the page does not list which).", VIS),
    P("VIS-03", "Give every child a $5,000 'Family Empowerment Grant 1' at birth", ["incomes-and-employment", "tax-and-income-support"], _why_fam,
      "A $5,000 'wealth and wellbeing investment' per newborn to start asset growth.", VIS),
    P("VIS-04", "Pay families with a child under one a weekly no-strings 'Family Empowerment Grant 2'", ["incomes-and-employment", "benefits"], _why_fam,
      "A weekly payment for families with children under the age of one (amount not stated).", VIS),
    P("VIS-05", "Replace the minimum wage with an annually adjusted Living Wage set in law", ["incomes-and-employment", "wages-and-working-conditions"], _why_fam,
      "Legislate a transition from the minimum wage to a Living Wage adjusted every year for inflation.", VIS),
    P("VIS-06", "Remove benefit and tax rules that discourage marriage or reward parental separation", ["incomes-and-employment", "benefits"], _why_fam,
      "Eliminate financial rules the party says disincentivise marriage or reward separation.", VIS),
    P("VIS-07", "Introduce tax credits for 7, 15 and 20 years of marriage and interest-free packages for first-home buyers", ["incomes-and-employment", "tax-and-income-support", "housing", "housing-affordability"], _why_fam,
      "Marriage-milestone tax credits at 7, 15 and 20 years plus interest-free first-home packages.", VIS),
    P("VIS-08", "Set up a free 0800 helpline and put hapū liaison staff in every Oranga Tamariki office", ["community-and-inclusion", "family-justice-and-safety", "te-ao-maori"], _why_fam,
      "Aimed at stopping 'forced state interventions' in families.", VIS),
    P("VIS-09", "Open government land for affordable housing, allow dual home builds under the RMA, and give $50,000 start-up grants to hapū family enterprises", ["housing", "housing-affordability", "urban-planning-and-resource-management", "economy"], _why_fam,
      "Unlock Crown land for affordable housing initiatives, reform the RMA to allow two homes on a site, and fund $50,000 start-up grants for hapū family businesses.", VIS),
    P("VIS-10", "Make the first $25,000 of personal income tax-free", ["incomes-and-employment", "tax-and-income-support"], _why_col,
      "A tax-free threshold of $25,000 on personal income.", VIS, key=True),
    P("VIS-11", "Abolish income tax on superannuation, student loans and welfare benefits", ["incomes-and-employment", "tax-and-income-support", "superannuation-and-savings"], _why_col,
      "Remove income tax from NZ Super, student loans and benefits.", VIS),
    P("VIS-12", "Introduce 'Farm Gate Prices' so New Zealanders get priority and fair prices on home-grown meat and dairy", ["incomes-and-employment", "prices", "agriculture"], _why_col,
      "A farm-gate pricing model giving New Zealanders first priority and fair pricing for local meat and dairy.", VIS),
    P("VIS-13", "Require foreign-owned companies to employ a baseline percentage of New Zealand citizens, with higher tax for those that don't", ["incomes-and-employment", "jobs-and-employment", "economy"], _why_col,
      "Mandate a minimum share of NZ-citizen staff in foreign-owned firms and apply a higher tax rate to foreign traders and businesses below the baseline.", VIS),
    P("VIS-14", "Introduce a newborn birth payment", ["incomes-and-employment", "benefits"], _why_col,
      "A dedicated payment on the birth of a child to 'incentivise childbirth' (amount not stated).", VIS),
    P("VIS-15", "Remove gender theory, Relationships and Sexuality Education and 'political propaganda' from the curriculum", ["education", "schools"], _why_edu,
      "Remove these from the national curriculum after an independent review for political bias.", VIS, key=True),
    P("VIS-16", "Refocus schools on a knowledge-rich curriculum of literacy, numeracy, science and 'balanced history'", ["education", "schools"], _why_edu,
      "Centre the curriculum 'strictly' on those subjects.", VIS),
    P("VIS-17", "Invest heavily in early childhood education focused on language, literacy and social skills", ["education", "early-childhood-education"], _why_edu,
      "High-quality ECE investment, and keep ECE free of 'inappropriate ideological, foreign religious, or overt cultural content'.", VIS),
    P("VIS-18", "Raise teacher salaries and cut their administrative workload", ["education", "schools", "wages-and-working-conditions"], _why_edu,
      "To attract and keep teachers.", VIS),
    P("VIS-19", "Strengthen civics education on New Zealand's democratic institutions", ["education", "schools"], _why_edu,
      "A strengthened civic education programme.", VIS),
    P("VIS-20", "Deputise Community Support Officers to support Police", ["law-justice-and-government", "policing"], _why_law,
      "Community Support Officers would help Police maintain public safety.", VIS),
    P("VIS-21", "Fund grassroots organisations to deliver 24/7 wrap-around family services on truancy, addiction, debt and housing", ["law-justice-and-government", "criminal-justice", "community-and-inclusion"], _why_law,
      "Fund organisations with proven records, combined with local accountability, strict enforcement and prevention.", VIS),
    P("VIS-22", "Match infrastructure and transport spending to local growth, with fast-growing regions getting their fair share", ["transport-and-infrastructure", "infrastructure-funding-and-planning", "cars-and-roads"], _why_inf,
      "Prioritise roads, schools and services where communities are growing, and productive investment over bureaucracy.", VIS),
    P("VIS-23", "Adopt 'One Nation, One People, One Vote, One Government, One Flag, Under One God' as a unifying principle", ["community-and-inclusion", "law-justice-and-government"], _why_id,
      "Stated as the party's core principle.", VIS),
    P("VIS-24", "Pause mass immigration immediately while visa policy is reviewed", ["migration"], _why_id,
      "An immediate pause to relieve pressure on infrastructure and communities.", VIS, key=True),
    P("VIS-25", "Leave the United Nations and the Paris Agreement", ["defence-and-foreign-affairs", "international-relations", "environment"], _why_id,
      "To 'restore absolute national sovereignty'.", VIS),
    P("VIS-26", "Require 10 years' residency for citizenship and end dual citizenship for new applicants", ["migration"], _why_id,
      "Extend the residency requirement for citizenship to 10 years; no dual citizenship for new applicants.", VIS),
    P("VIS-27", "Declare English the official language of New Zealand", ["community-and-inclusion", "te-ao-maori"], _why_id, "Make English the official language.", VIS),
    P("VIS-28", "End race-based policies and 'He Puapua-driven' policies across government", ["te-ao-maori", "te-tiriti-o-waitangi-and-governance"], _why_id,
      "Remove such policies across government, including all race-based targeting in health.", VIS),
    P("VIS-29", "Define sex in law strictly as male and female and designate single-sex spaces and women's sport by biological sex", ["community-and-inclusion", "women", "sports-and-recreation"], _why_sex,
      "Legal definition of biological sex; toilets, changing rooms, refuges and prisons designated by sex; sport categories restricted by biological sex; review the Births, Deaths, Marriages and Relationships Registration Act 2021.", VIS),
    P("VIS-30", "Ban gender-transition medical treatment for minors and pass a Parental Rights Bill covering children up to 16", ["health", "young-people", "community-and-inclusion"], _why_sex,
      "Prohibit all medical gender-transition interventions for under-18s and restore parental authority over children's health decisions up to age 16.", VIS),
    P("VIS-31", "Prioritise primary care and GP access and raise health-worker pay", ["health", "health-services", "health-funding-and-workforce"], _why_hlth,
      "Redirect budgets to the frontline, cut specialist waitlists, increase salary budgets, and boost funding and incentives for domestic students in health degrees.", VIS),
    P("VIS-32", "Fully fund Plunket and increase pre- and post-natal support", ["health", "public-health"], _why_hlth,
      "Full, stable Plunket funding and more financial support for maternal and infant care.", VIS),
    P("VIS-33", "Review and reform laws that 'endanger the lives of unborn children'", ["health", "community-and-inclusion"], "Vision NZ says a compassionate society must protect the vulnerable 'beginning in the womb'.",
      "Review existing legislation (the party does not name specific changes).", VIS),
    P("VIS-34", "Abolish MMP party lists so only electorate winners sit in Parliament, and cut the number of MPs", ["law-justice-and-government", "parliament-and-democracy"], _why_dem,
      "Overhaul MMP to eliminate list seats and reduce the size of Parliament.", VIS, key=True),
    P("VIS-35", "Introduce term limits and regular drug testing for MPs, ban taxpayer-funded alcohol at MP functions, and reject digital ID", ["law-justice-and-government", "parliament-and-democracy"], _why_dem,
      "Term limits for politicians, mandatory drug testing of sitting MPs, no taxpayer-funded alcohol, and opposition to digital IDs.", VIS),
]

# ------------------------------------------------------------------------------------------------ Aotearoa Legalise Cannabis Party
ALCP = ["full-spectrum-policy"]
META["legalise-cannabis"] = {
    "name": "Aotearoa Legalise Cannabis Party (ALCP)", "website": "https://www.alcp.org.nz/",
    "registered": "30 May 1996 (Electoral Commission register)",
    "intro": "The ALCP's policy page (\"Full Spectrum Policy\") is a single document, credited as developed in 2005 by Irinka "
             "Britnell, Paula Lambert and Kevin O'Connell, with a 'Policy Minimum Programme', eleven numbered portfolio "
             "sections and a 2020 addendum of ideas 'under discussion' prepared for the cannabis referendum bill. The party "
             "presents this page as its current policy; each distinct commitment is listed below.",
    "gaps": "The policy text is largely from 2005 with a 2020 addendum; no 2026-specific manifesto, costings or press releases "
            "were captured (the site's News page was not mined, and web search capacity ran out during this research). "
            "The 2020 items are described by the party as 'under discussion and in progress'.",
}
_why_alcp = "The ALCP says cannabis prohibition is unworkable and discriminatory, wastes public money and fuels the black market."
CATALOG["legalise-cannabis"] = [
    P("ALCP-01", "Make possession, cultivation and use of cannabis free from prosecution", ["law-justice-and-government", "criminal-justice", "health"],
      _why_alcp, "Part of the party's 'Policy Minimum Programme': no prosecution for possessing, growing or using cannabis and cannabis/hemp products.", ALCP, key=True),
    P("ALCP-02", "Create regulated R18 cannabis commerce like alcohol and tobacco, but with no promotion", ["health", "public-health", "economy"],
      _why_alcp, "Legal adult-only sales with no advertising or promotional aspects, with details fine-tuned by a policy council.", ALCP, key=True),
    P("ALCP-03", "Provide for medicinal cannabis, including home-grown medicine and prescribed preparations", ["health", "medicines"],
      "The party says legal access would promote safer modes of use such as vaporisation and mouth sprays.",
      "Establish therapeutic applications of cannabis, allowing both home-grown medicinal cannabis and prescribed preparations.", ALCP),
    P("ALCP-04", "Enable full-scale hemp production, prioritising local low-cost biofuel, fibre and hurd", ["economy", "agriculture", "environment", "energy"],
      "The party says hemp would create jobs (especially in depressed regions), cut emissions and pollution, save forests and improve soils.",
      "Allow full-scale cannabis-hemp farming and use, with priority for localised biofuel production and fibre and hurd for building materials, paper, plastics and textiles; hemp seed as food.", ALCP),
    P("ALCP-05", "Expunge all cannabis convictions and apologise for prohibition", ["law-justice-and-government", "criminal-justice"],
      "The party says up to 20,000 people a year are convicted of cannabis offences and that Māori are four to five times more likely to be convicted.",
      "Wipe all cannabis convictions; the 2020 addendum adds that apologies must be made for the injustices of prohibition.", ALCP, key=True),
    P("ALCP-06", "Hold a prohibition 'truth and reconciliation' commission", ["law-justice-and-government", "criminal-justice"],
      "The party says Parliament has a duty to challenge injustice and break down prejudice.", "A full commission on prohibition 'in the interests of accountability'.", ALCP),
    P("ALCP-07", "Set up a tobacco, alcohol and cannabis authority (Drugs Policy Council) to regulate recreational substances", ["health", "public-health", "alcohol-and-drugs"],
      "The party says credible, harm-reduction drug education is impossible under current 'double standards'.",
      "A single regulator to develop the regulatory framework for recreational substances, with 'adults only' enforcement and honest drug education in schools funded from prohibition savings.", ALCP),
    P("ALCP-08", "Redirect prohibition enforcement money to health, education, community and serious crime", ["law-justice-and-government", "policing", "government-revenue-and-finance"],
      "The party says police would be freed up for 'real crime' and public trust in the law would improve.",
      "Shift funds currently spent enforcing cannabis laws into health, education, community and employment, and more police and court resources for serious crime.", ALCP),
    P("ALCP-09", "Stop overseas cannabis offences being a barrier to immigrating to New Zealand", ["migration"],
      "The party says it has no other immigration position beyond inclusiveness and tolerance.", "Cannabis offences in other jurisdictions should not bar migrants.", ALCP),
    P("ALCP-10", "Reallocate drug-war resources to border security and civil defence", ["defence-and-foreign-affairs"],
      "The party says the international war on drugs aids organised crime and terrorism.", "Resources freed by ending the cannabis 'drug war' would strengthen border security and civil defence.", ALCP),
    P("ALCP-11", "Allow at least five cannabis plants per household and affordable micro-licences for small growers", ["economy", "business-support", "law-justice-and-government"],
      "Part of the party's 2020 'cottage industry' ideas, which it says are still under discussion.",
      "A 'bare minimum' five-plant home-grow allowance, affordable micro-licences for existing growers, Kiwi seed strains, safe edibles, quality-controlled retail products and protection against racially loaded enforcement; an age limit more consistent with alcohol and tobacco.", ALCP),
]

# ------------------------------------------------------------------------------------------------ Free Palestine
FP = ["palfree-home-objectives-principles", "constitution-june-2026", "release-2026-08-newest-political-party"]
META["free-palestine"] = {
    "name": "Free Palestine (Palestine Free from the River to the Sea Party)", "website": "https://palfree.nz/",
    "registered": "5 August 2026 as \"Free Palestine\" (Electoral Commission register)",
    "intro": "Free Palestine is a single-issue party registered in August 2026 (its website calls it the 'Palestine Free from "
             "the River to the Sea Party'). Its platform consists of three objectives and six founding principles on its "
             "one-page website, the same principles in its June 2026 constitution lodged with the Electoral Commission, and a "
             "six-point list in its August 2026 registration press release. Each principle/objective is listed below.",
    "gaps": "The party has no published policies on domestic issues. Wording differs slightly between sources: the website "
            "refers to dismantling 'the Zionist structure of the state of Israel', the constitution to 'the apartheid structure'. "
            "Media reports of a separate 2026 foreign-affairs policy could not be checked against a party document (web search "
            "capacity ran out). The website's membership, enrolment and donation sections are omitted from the captured text.",
}
CATALOG["free-palestine"] = [
    P("FPP-01", "Support the right of return of Palestinian refugees and the dismantling of Israel's current state structure, rejecting a two-state solution",
      ["defence-and-foreign-affairs", "international-relations"],
      "The party says a just peace depends on refugees' return and that further partition would bring more injustice.",
      "Founding principle 1 (website) / constitution clause 2.", FP, key=True),
    P("FPP-02", "Establish a single secular, democratic, bi-national state in all of historic Palestine with equal citizenship",
      ["defence-and-foreign-affairs", "international-relations"], None,
      "Founding principle 4: one state with full and equal citizenship and ethnic and religious rights protected in a democratic constitution.", FP, key=True),
    P("FPP-03", "Press the New Zealand government to uphold international law and UN resolutions on Palestine and support war-crimes and genocide prosecutions",
      ["defence-and-foreign-affairs", "international-relations"],
      "The party says its aim is to change public opinion and put sustained parliamentary pressure on the government.",
      "Accept the primacy of international law and UN resolutions; call Israel to account under the Universal Declaration of Human Rights; have New Zealand support prosecutions and use its independent voice internationally.", FP),
    P("FPP-04", "Give 'unconditional and complete solidarity' to Palestinian resistance 'in all forms accordant with International Humanitarian Law'",
      ["defence-and-foreign-affairs", "international-relations"], None,
      "Founding principle 5 (the press release lists 'unconditional support for all forms of Palestine resistance' without the IHL qualifier).", FP),
    P("FPP-05", "Adopt an independent foreign policy and withdraw from formal military and security alliances with the United States",
      ["defence-and-foreign-affairs", "international-relations"], None,
      "Founding principle 6: leave any formal US security alliances and distance foreign policy from 'Anglo-U.S. economic hegemony and military interventionism'.", FP, key=True),
    P("FPP-06", "Build a mass democratic movement and global solidarity links for Palestinian liberation",
      ["defence-and-foreign-affairs", "community-and-inclusion"], None,
      "The party's stated objectives: a broad party uniting Palestine supporters from all traditions, and links with others resisting inequality and injustice; it also seeks to persuade other parties to adopt stronger pro-Palestine policies.", FP),
]

# ------------------------------------------------------------------------------------------------ NZ Loyal
NZL = ["rnz-quote-of-party-website", "nzloyal-com-not-retrievable"]
META["nz-loyal"] = {
    "name": "New Zealand Loyal (NZ Loyal)", "website": "https://nzloyal.com/",
    "registered": "5 August 2026 (re-registered; Electoral Commission register)",
    "intro": "NZ Loyal (leader Kelvyn Alp) was re-registered in August 2026. **Its own policy pages could not be captured**: "
             "nzloyal.com is behind a Cloudflare bot challenge that blocked both curl and a headless browser. The only "
             "verbatim party wording available to this archive is a ten-point list RNZ quoted from the party's website on "
             "12 October 2026; each point is listed below with that RNZ article as the source.",
    "gaps": "Full policy text NOT retrievable (nzloyal.com HTTP 403 Cloudflare; web.archive.org unreachable from this "
            "environment; newzealandloyal.com is a parked domain). Detail behind each headline (mechanisms, costs) is "
            "unknown. A separate group calling itself the 'Real NZ Loyal' disputes Alp's leadership (reported by The Press "
            "and Wikipedia); this archive lists the registered party's stated policies only.",
}
_nzl = "Listed on the party's website as quoted by RNZ; no further detail could be retrieved."
CATALOG["nz-loyal"] = [
    P("NZL-01", "End New Zealand's participation in the UN, WEF and WHO", ["defence-and-foreign-affairs", "international-relations"],
      "The party's stated aim is to 'take our country back from foreign interests'.", _nzl, NZL, key=True),
    P("NZL-02", "End climate accords the party says are 'based on faulty science'", ["environment", "emissions-reduction"], None, _nzl, NZL),
    P("NZL-03", "Establish energy independence, including oil and gas", ["transport-and-infrastructure", "energy", "oil-gas-and-mining"], None, _nzl, NZL),
    P("NZL-04", "Free farmers from 'restrictive regulations'", ["economy", "agriculture"], None, _nzl, NZL),
    P("NZL-05", "Scrap the current tax system", ["incomes-and-employment", "tax-and-income-support"], None, _nzl + " The replacement system is not described.", NZL, key=True),
    P("NZL-06", "Scrap all race-based policies", ["te-ao-maori", "te-tiriti-o-waitangi-and-governance"], None, _nzl, NZL),
    P("NZL-07", "Establish a New Zealand constitution", ["law-justice-and-government", "parliament-and-democracy"], None, _nzl, NZL),
    P("NZL-08", "'Expose and eradicate propaganda' from news media", ["media-culture-and-recreation"], None, _nzl, NZL),
    P("NZL-09", "Protect children from what the party calls 'corrupt sex and gender education'", ["education", "schools"], None, _nzl, NZL),
    P("NZL-10", "Decentralise government and 'return power to the people'", ["law-justice-and-government", "local-government"], None, _nzl, NZL),
]

# ------------------------------------------------------------------------------------------------ NAP (Not A Party)
META["nap"] = {
    "name": "NAP (Not A Party)", "website": "https://nap.org.nz/",
    "registered": "Not a registered party; contests electorates only (Kenepuru: Bob Wessex; Kāpiti: Richard Goode — per policy.nz)",
    "intro": "\"Not A Party\" describes itself as 'the forerunner of a new breed of post-democratic political party' that "
             "advocates 'a peaceful transition to a society based on voluntary cooperation'. Rather than a policy programme "
             "it published a 7 October 2026 media release proposing a national conversation about governance without "
             "parties, plus a list of principles. Those positions are listed below.",
    "gaps": "The site's 'Policies' menu item (nap.org.nz/?page_id=21) returned HTTP 404 on 2026-10-23; no policy list exists beyond the items below.",
}
NAP = ["media-release-2026-10-07-exit-politics", "principles", "beyond-democracy"]
CATALOG["nap"] = [
    P("NAP-01", "Start a national conversation about governing without political parties ('Exit politics')", ["law-justice-and-government", "parliament-and-democracy"],
      "NAP says parties force voters into 'package deals' and the system is 'better at producing political careers than producing good decisions'.",
      "Experiment with citizens' assemblies, deliberative democracy, local decision-making, participatory budgeting, digital consultation and rotating civic representation, with New Zealand as 'a laboratory for innovation in governance'.",
      ["media-release-2026-10-07-exit-politics"], key=True),
    P("NAP-02", "Move peacefully to a society based on voluntary cooperation, guided by principles of self-sovereignty and self-government", ["law-justice-and-government", "community-and-inclusion"],
      None, "Its listed principles: self-sovereignty, self-government, self-ownership, self-reliance, self-defence, self-control, self-respect, self-help, solidarity and 'safer communities together'.",
      ["principles", "beyond-democracy"]),
]

# ------------------------------------------------------------------------------------------------ Socialist Equality Group
SEG = ["election-statement-2026-10-13"]
META["socialist-equality-group"] = {
    "name": "Socialist Equality Group (SEG)", "website": "https://www.wsws.org/",
    "registered": "Not a registered party; one electorate candidate (Tom Petterson, Hutt South)",
    "intro": "The Trotskyist Socialist Equality Group is standing Tom Petterson in Hutt South. Its programme is its election "
             "statement published on the World Socialist Web Site on 13 October 2026, which says the campaign 'is not a bid "
             "for office' but an intervention for socialist leadership of the working class. The statement's explicit "
             "demands are listed below.",
    "gaps": "The statement is the only programme document; it gives no costings.",
}
_seg_war = "The SEG says a third world war is developing and that both Labour and National back US war plans and higher military spending."
CATALOG["socialist-equality-group"] = [
    P("SEG-01", "End all military spending and redirect it to schools, hospitals and ending poverty", ["defence-and-foreign-affairs", "government-revenue-and-finance"], _seg_war, "Part of its 'No money for war!' demands.", SEG, key=True),
    P("SEG-02", "Leave Five Eyes, close the Waihopai spy base and abolish the intelligence agencies", ["defence-and-foreign-affairs", "international-relations"], _seg_war, "As stated.", SEG),
    P("SEG-03", "Abolish ANZUS, end all military alliances (US, Australia, NATO) and withdraw all troops deployed overseas", ["defence-and-foreign-affairs", "international-relations"], _seg_war, "As stated.", SEG),
    P("SEG-04", "Raise all wages by 20% immediately, raise benefits, and index wages and benefits monthly to the cost of living", ["incomes-and-employment", "wages-and-working-conditions", "benefits"],
      "The SEG says real wages have fallen 6.4% since 2021 while billionaire wealth has grown.", "An immediate 20 percent pay rise for all workers plus automatic monthly cost-of-living adjustments.", SEG, key=True),
    P("SEG-05", "Guarantee a permanent full-time job for all who want one and a living income for those who cannot work", ["incomes-and-employment", "jobs-and-employment", "benefits"], None, "As stated.", SEG),
    P("SEG-06", "Cancel student debt and restore free tertiary education", ["education", "tertiary-fees-and-student-support"], None, "As stated.", SEG),
    P("SEG-07", "Provide free universal healthcare and reverse cuts to health, education and public-service jobs and pay", ["health", "health-services", "public-sector"], None, "As stated.", SEG),
    P("SEG-08", "Build rank-and-file workers' committees independent of the unions", ["incomes-and-employment", "wages-and-working-conditions"],
      "The SEG says the trade union bureaucracy acts as 'an industrial police force for the state and big business'.",
      "Committees linked internationally through the International Workers' Alliance of Rank-and-File Committees.", SEG),
    P("SEG-09", "Give full citizenship rights to all immigrants and end deportations", ["migration"], None, "Repeal all 'anti-immigrant measures'.", SEG),
    P("SEG-10", "Nationalise the banks and major corporations under workers' democratic control and seize billionaires' wealth", ["economy", "government-revenue-and-finance"],
      "The SEG says $129 billion is held by 150 families and that the wealth was created by the working class.",
      "Establish a 'workers' government' after the working class takes political power.", SEG, key=True),
]

# ------------------------------------------------------------------------------------------------ Progressive Aotearoa NZ
PR = ["policies"]
META["progressive-aotearoa-new-zealand"] = {
    "name": "Progressive Aotearoa New Zealand (Progressive Party, PPANZ)", "website": "https://www.progressiveparty.co.nz/",
    "registered": "Not a registered party; electorate candidates only (Nelson: Bruce Dyer; West Coast-Tasman: Kevin Rooke; Kāpiti: Michael Walker — per policy.nz)",
    "intro": "The Progressive Party (PPANZ) publishes a 'Policies' page with sections on health, housing, education, justice, "
             "Māori policy, animals and plants, agriculture, climate change, industry, taxation and social boards, each "
             "beginning 'The Progressive Party advocates…', plus a longer 'PPANZ Manifesto' (marked as a work in progress, "
             "including a Covid-19 strategy white paper). The main advocated positions are listed below.",
    "gaps": "Undated pages; no costings. The manifesto is captured in full but its points largely repeat the Policies page.",
}
_pr = "The Progressive Party says economic and political power should serve people rather than concentrated wealth (its stated philosophy draws on economic democracy and 'neohumanism')."
CATALOG["progressive-aotearoa-new-zealand"] = [
    P("PPA-01", "Guarantee access to food, clothing, housing, education and healthcare", ["community-and-inclusion", "incomes-and-employment"], _pr, "Listed in the health, housing and education sections as guarantees for everyone.", PR, key=True),
    P("PPA-02", "Create an independent National Health Board outside the Health Ministry to oversee Te Whatu Ora", ["health", "health-services"], "The party says this would counterbalance political influence on health priorities.", "A board of health experts with elected and appointed members, plus co-operative primary and residential care, Māori-for-Māori services and higher taxes on harmful products ring-fenced for health.", PR),
    P("PPA-03", "Legalise cannabis as a health issue and support the End-of-Life Choice Act", ["health", "alcohol-and-drugs"], None, "Tax revenue from cannabis would go to health, with research on benefits and harms; the party also lists voluntary vaccination and a review of Covid-era measures for future pandemics.", PR),
    P("PPA-04", "Offer state-funded mortgages, a state-owned house-building enterprise and limit home ownership to NZ residents", ["housing", "housing-affordability"], "The party says leaving housing to the market 'amounts to a dereliction of duty'.", "Also long-term leasing, co-operative housing and co-housing options, and a capital gains tax to curb speculation.", PR, key=True),
    P("PPA-05", "Make te reo Māori compulsory in primary and secondary schools, aiming for a bilingual Aotearoa", ["te-ao-maori", "te-reo-maori-and-culture", "education"], None, "Language parity with English, plus full teaching of New Zealand history and the constitutional documents (Te Tiriti and He Whakaputanga).", PR),
    P("PPA-06", "Entrench the Māori seats in Parliament", ["te-ao-maori", "parliament-and-democracy"], None, "Give the Māori seats the same entrenched protection as general seats.", PR),
    P("PPA-07", "Move schooling from national standards to child-centred, experiential learning including meditation and mindfulness", ["education", "schools"], None, "Learning based on each child's needs, parents as active partners, restorative behaviour management and a Hauora (holistic wellbeing) approach.", PR),
    P("PPA-08", "Focus prisons on rehabilitation, education and restorative justice, and end for-profit prisons", ["law-justice-and-government", "criminal-justice"], "The party views crime as rooted in social and economic conditions.", "Skills training and tikanga Māori in prisons, mental-health services, restorative justice, community reintegration support, and terminating private prison arrangements.", PR),
    P("PPA-09", "Establish a Ministry for Animal and Plant Welfare and extend legal advocacy to nature", ["environment", "conservation", "community-and-inclusion"], None, "Building on Te Urewera's legal personhood and animals' legal recognition as sentient.", PR),
    P("PPA-10", "Shift farming to co-operatives and plant-based protein", ["economy", "agriculture"], None, "Incentivise farmers to move to plant protein (including lab-grown meat) and regenerative, ethical farming models; co-operatives at all levels of agriculture.", PR),
    P("PPA-11", "Build a government-backed renewables industry and prepare to move infrastructure 10 metres above sea level", ["environment", "emissions-reduction", "climate-adaptation", "energy"], None, "Electrify transport, convert sewage and organic waste to biogas and biodiesel, raise eco-housing standards, phase out gas appliances, and redirect foreign aid toward emissions cuts in the Pacific.", PR),
    P("PPA-12", "Run businesses with more than nine employees as worker co-operatives and state-manage monopolistic key industries", ["economy", "economic-development-and-industry"], None, "A Minister, Ministry and Centre for Cooperative Studies; railways, power and mining state-managed; a nationwide co-operative supermarket to cut living costs.", PR, key=True),
    P("PPA-13", "Phase out income tax in favour of taxes on production, remove GST from fresh produce and introduce a capital gains tax", ["incomes-and-employment", "tax-and-income-support"], None, "Income tax would become a mechanism capping salaries at a maximum linked to the minimum wage, set by a Wages and Salary Commission.", PR),
    P("PPA-14", "Create Social Boards of respected community members to advise local and national government", ["law-justice-and-government", "parliament-and-democracy"], "The party says they would moderate lobby groups' influence.", None, PR),
]

# ------------------------------------------------------------------------------------------------ electorate-only groups with no published policy
_none = ("No party website, policy page or published platform could be found for this group (checked policy.nz candidate "
         "data, which lists no policies or profile text, and web search before search capacity ran out on 2026-10-23). If the "
         "group publishes policies, they should be added here.")
for slug, name, who in [
    ("balance-new-zealand", "Balance New Zealand", "Whanganui: Juan Charles Coffey"),
    ("build-the-nation", "Build the Nation", "Northland: Richard McIntosh"),
    ("jobseeker-party", "Jobseeker Party", "Henderson: Kelso Papali'i"),
    ("money-free-party", "Money Free Party", "West Coast-Tasman: Richard Francis Osmaston; Wellington Bays: Liam Anderson; Whangārei: Luke Beharrell"),
    ("new-world-order-mccann-party", "New World Order McCann Party", "Hamilton West: Nathan Lee Couper"),
    ("nz-economic-euthenics-party", "NZ Economic Euthenics Party", "Christchurch Central: Tubby Hansen"),
    ("peoples-party-new-zealand", "People's Party New Zealand", "Māngere: Alani Fisher Taione; Ōtāhuhu: Eseta Haunga"),
    ("te-pati-hira", "Te Pāti Hira", "Wairarapa: Jared Warren Gardner"),
    ("your-pic-party", "Your PIC Party", "Te Tai Tokerau: Karl Barkley"),
    ("independent-taranaki", "Independent Taranaki", "New Plymouth: Rusty Kane"),
]:
    META[slug] = {"name": name, "website": None,
                  "registered": f"Not a registered party; electorate candidate(s) only ({who} — per policy.nz)",
                  "intro": f"{name} is an electorate-only label used by candidate(s) in the 2026 election. It is not on the "
                           "Electoral Commission's register of parties and does not contest the party vote.",
                  "gaps": _none}
    CATALOG[slug] = []
META["money-free-party"]["gaps"] = _none + (" Background: the Money Free movement (led by Richard Osmaston) has long argued "
    "that money itself drives problems such as climate change and homelessness (Wikipedia, 'Money Free movement'); no 2026 "
    "policy document was found.")
META["balance-new-zealand"]["gaps"] = _none + (" A Facebook-page mirror (govserv.org) shows posts describing the group as "
    "centrist and discussing permanent residents' voting rights and MPs' entitlements, but this could not be verified "
    "against a party policy document, so nothing is listed.")

# ------------------------------------------------------------------------------------------------ NZ Outdoors & Freedom Party
META["nz-outdoors-freedom"] = {
    "name": "NZ Outdoors & Freedom Party ('freedom')", "website": "https://freedom.kiwi/ (registered as www.nzofp.co.nz, which serves the same site)",
    "registered": "11 August 2017 (Electoral Commission register)",
    "intro": "The NZ Outdoors & Freedom Party (leader Sue Grey) now brands itself 'freedom'. Its Policies page links ten "
             "policy pages: Direct Democracy (its 'new core pillar'), Agriculture, Housing, Open Source First, Cannabis, "
             "Anti-Bullying, the ACC Justice & Accountability statement, Education, Fisheries, and Outdoors Recreation & "
             "Wildlife. Each distinct commitment on those pages is listed below.",
    "gaps": "The home page renders almost no text without JavaScript (captured as-is). Pages are undated; costings appear "
            "only in the ACC statement. Positions on 1080, fluoride and 5G described in media coverage were not found on "
            "the current policy pages, so are not listed.",
}
DD, AG, HO, OS, CA, AB, ACC, ED, FI, RW = (["direct-democracy"], ["agriculture-policy"], ["housing-policy"], ["open-source-policy"],
    ["cannabis-policy"], ["anti-bullying-policy"], ["the-acc-justice-accountability-policy-statement"], ["education-policy"],
    ["nzofp-fisheries-policy"], ["outdoors-recreation-and-wildlife-policy"])
_dd = "The party says Covid-era measures showed fundamental rights could be overridden by a simple parliamentary majority and that select-committee consultation is 'a toothless illusion'."
CATALOG["nz-outdoors-freedom"] = [
    P("OFP-01", "Entrench the NZ Bill of Rights Act as supreme law", ["law-justice-and-government", "parliament-and-democracy"], _dd,
      "Make the Bill of Rights the constitutional bedrock so no government or emergency declaration can override rights such as free speech, movement, assembly and the right to refuse medical treatment.", DD, key=True),
    P("OFP-02", "Introduce Swiss-style binding citizens' referendums: a citizens' veto on laws and citizen-initiated laws", ["law-justice-and-government", "parliament-and-democracy"], _dd,
      "Citizens could gather signatures to force a binding nationwide vote to strike down a law, or to put their own draft law on the ballot, with a lower signature threshold than the current 10% for non-binding referendums.", DD, key=True),
    P("OFP-03", "Decentralise government under a 'subsidiarity' principle and let regions keep part of the GST and tax raised locally", ["law-justice-and-government", "local-government", "regional-development"], _dd,
      "Return decisions on local infrastructure, land management and regional development to communities, shrink central ministries and give regions financial autonomy.", DD),
    P("OFP-04", "Withdraw from the Paris Agreement and focus on flood management and carbon-rich soils", ["environment", "emissions-reduction", "agriculture"],
      "The party says farm animals cannot release more carbon than they eat and that extreme weather is 'nature, not climate change'.",
      "Exit Paris (it says staying would cost more than leaving), maintain river flows and channels to reduce flood risk, and support ecological agriculture with minimal synthetic inputs.", AG, key=True),
    P("OFP-05", "Replace the EPA with an independent Health-Environment Protection Agency and apply the precautionary principle to new technology", ["environment", "public-health", "agriculture"], None,
      "New technologies and products only with full liability for the business introducing them; independent biosecurity at every entry point.", AG),
    P("OFP-06", "Leave the CPTPP (TPPA) and RCEP and pursue 'fair trade' bilateral deals", ["defence-and-foreign-affairs", "international-relations", "economy"], None,
      "Withdraw from agreements that limit New Zealand's ability to legislate, increase Pacific trade, strengthen anti-monopoly law and place a moratorium on sales of farmland, forestry, housing and infrastructure to non-tax-residents.", AG),
    P("OFP-07", "Free up land and revise the RMA to speed house building, with a mix of public and private housing", ["housing", "housing-affordability", "urban-planning-and-resource-management"],
      "The party says every citizen should have access to an affordable, warm, dry home.", "Identify land for subdivision, sequence servicing and construction, and have the Ministry of Housing take a hands-on role.", HO),
    P("OFP-08", "Require high standards for new homes (R5 insulation, rainwater and greywater systems, energy efficiency) and fund hempcrete building", ["housing", "housing-quality", "construction"], None,
      "Also solar or micro-generation, green space for gardens, recycling of building materials, lower consent costs for sustainable materials, and a funding scheme for hempcrete homes.", HO),
    P("OFP-09", "Fully fund night shelters and low-cost living spaces for homeless people", ["housing", "community-and-inclusion"], None, "Shelters would provide two nutritious meals a day and supplements; the party also wants to restore New Zealand's leadership in social housing.", HO),
    P("OFP-10", "Adopt an 'Open Source First' rule for government software procurement", ["economy", "internet-and-digital-technologies", "public-sector"],
      "The party says dependence on multinational software vendors is a hidden import cost and a resilience risk.", "Agencies must check for a suitable open-source option before buying proprietary software, compare whole-of-life costs, and use New Zealand providers for support.", OS),
    P("OFP-11", "Decriminalise personal cannabis use and cultivation and support medicinal cannabis and hemp", ["health", "alcohol-and-drugs", "law-justice-and-government"], None,
      "No criminal offence for personal possession or growing; support home-grown medicinal cannabis and small NZ suppliers over 'Big Pharma', with lower licensing barriers; update law to support hemp products.", CA),
    P("OFP-12", "Create a nationwide anti-bullying strategy treating bullying as a public-health issue", ["health", "mental-health", "education"], None,
      "Awareness programmes in schools and communities, leadership training for teachers and managers, bullying questions in routine health screening, and treatment of psychological effects.", AB),
    P("OFP-13", "Make one doctor's injury diagnosis final for ACC and abolish ACC's review and dispute machinery", ["health", "health-services", "public-sector"],
      "The party says ACC 'expert shopping' is used to decline claims.", "Disestablish ACC review specialists and investigators, cancel contracts with FairWay and ICRA, stop paying external consultants to contest diagnoses; it claims $61.5m a year savings to redirect to surgery, rehabilitation and disability support.", ACC),
    P("OFP-14", "Pursue Pfizer for breach of contract over Covid-19 vaccines and recover ACC vaccine-injury costs", ["health", "law-justice-and-government"], None,
      "Release the full NZ Pfizer contract, bring a Crown claim to recover the $16.8m ACC has paid for vaccine injuries, guarantee ACC compensation for long-term vaccine harm, give ACC a statutory right of recourse against manufacturers, and review ACC law to cover distress and loss of enjoyment of life.", ACC),
    P("OFP-15", "Make early childhood centres and primary schools Wi-Fi free, using wired connections", ["education", "schools", "public-health"], None, "Minimise Wi-Fi in high schools too and work with Chorus on wired fibre connections.", ED),
    P("OFP-16", "Invest heavily in education with an outdoors- and community-focused curriculum, implementing the Tomorrow's Schools Review", ["education", "schools"], None, None, ED),
    P("OFP-17", "Replace the fisheries Quota Management System with a LegaSea-style system keeping fisheries in public ownership", ["economy", "fisheries", "environment"],
      "The party says the QMS has depleted fish stocks, privatised a public resource and priced locals out.",
      "Tendered commercial permits with no private sale of fishing rights, catches landed and processed in NZ, only NZ-owned operators, fleet separation in the territorial sea, and more recreational and customary inshore access.", FI),
    P("OFP-18", "Replace DOC with a Department of Outdoors – Wildlife, Recreation & Nature (DOWRN)", ["environment", "conservation", "sports-and-recreation"],
      "The party says governments have undervalued New Zealanders' outdoors culture and access.", "A department promoting access to all public land, coasts and rivers, poison-free conservation (trapping rather than poisons), food gathering on public land, and early public engagement on access decisions.", RW, key=True),
]

# ------------------------------------------------------------------------------------------------ Conservative Party NZ
META["conservative"] = {
    "name": "Conservative Party NZ (Conservatives NZ)", "website": "https://www.conservatives.nz/ (2026 campaign site: https://conservatives.org.nz/)",
    "registered": "6 October 2011 (Electoral Commission register)",
    "intro": "The Conservative Party NZ (called the New Conservatives in 2020–2023; leader Helen Houghton) has two websites: the "
             "party site conservatives.nz (policy summary, principles, and policy press releases from 2025–26) and a separate "
             "2026 campaign site conservatives.org.nz, linked from the main site, with 14 policy pages (Overview, Health, Economy, "
             "Bureaucracy, Environment, Immigration, Policing, Climate, Agriculture, Child Protection, Tax Relief, Right to Life, "
             "Natural Resources, Energy). Both are captured; policies are listed below with the campaign page as the main source.",
    "gaps": "Wix blog posts on conservatives.nz are rendered client-side; their text was recovered from the page's embedded "
            "data. The campaign Energy page's layout table extracted poorly (text is present but jumbled). Tax wording differs: "
            "the economy page says 'lower tax rate', a 2025 press release says 'flat tax rate'.",
}
C = lambda *x: ["campaign-" + i for i in x]
CATALOG["conservative"] = [
    P("CON-01", "Cut personal and company tax, align the company rate with the top personal rate, and lower GST to 12.5%", ["incomes-and-employment", "tax-and-income-support", "economy"],
      "The party says lower taxes improve compliance and investment and that New Zealand's rates should be no higher than Australia's.", "Also tackle public debt; a 2025 release calls for a 'flat tax rate' for individuals and companies.", C("economy-1") + ["news-new-policies-announcement"], key=True),
    P("CON-02", "Stop taxing NZ Super (including for over-65s still working) and boarders' income in private homes", ["incomes-and-employment", "superannuation-and-savings", "tax-and-income-support"], None,
      "Remove NZ Super from taxable income, and exempt genuine home-sharing/boarder income with safeguards against commercial use.", C("superannuation"), key=True),
    P("CON-03", "Let mayors become full-time council CEOs and give ministers power to appoint and sack senior public servants", ["law-justice-and-government", "public-sector", "local-government"],
      "The party says unelected bureaucrats and advisers usurp the mandate of elected representatives.", "Elected representatives at local and national level would get wide powers to dismiss obstructive or incompetent staff; legislate to curtail 'unconstitutional bureaucratic power'.", C("bureaucracy") + ["news-has-new-zealand-lost-control-of-its-own-government"]),
    P("CON-04", "Make cutting hospital waiting times the top health priority, funded from bureaucracy, procurement and productivity savings", ["health", "health-services", "health-funding-and-workforce"],
      "The party says the key issue is whether patients are treated in time, not how much is spent.", "Measure waits for elective surgery, specialists, diagnostics, cancer and ED; buy private capacity where it is quicker and competitive; grow the domestic workforce; link any extra funding to measurable results.", C("health")),
    P("CON-05", "Tighten immigration toward skilled migrants and cap other net migration by the supply of housing, doctors and school places", ["migration"],
      "The party says population growing faster than 'social goods' makes everyone poorer.", "A stable points system; end 'golden' investor visas; NZ licence tests for foreign truck drivers; tougher document checks and audits; report GDP per capita.", C("immigration"), key=True),
    P("CON-06", "Hold a Royal Commission of Inquiry into police under-performance and corruption", ["law-justice-and-government", "policing"],
      "The party cites fabricated drink-drive tests and lost public trust.", "Also: refer prima facie criminal allegations against police and all deaths caused by police action to the courts; protect identities of police witnesses in international drug cases; review drone laws.", C("policing") + ["news-police-policy-announcement"]),
    P("CON-07", "Strengthen the IPCA: double its staff, quadruple its budget, and let it prosecute and name officers", ["law-justice-and-government", "policing"], None, "As set out in its 'Sharpening the Teeth of the IPCA' statement.", ["news-sharpening-the-teeth-of-the-ipca"]),
    P("CON-08", "Improve access to justice for self-represented litigants", ["law-justice-and-government", "civil-justice"], None,
      "Procedural changes, support services, legal aid reform, tax deductions and cost awards for pro bono work, and wider Family Dispute Resolution.", ["news-press-release-improving-access-to-justice-for-self-represented-litigan"]),
    P("CON-09", "Leave the Paris Agreement, scrap the ETS and repeal all 'climate'-based taxes, laws and agencies", ["environment", "emissions-reduction"],
      "The party says there is no climate emergency and that climate policies raise food and energy costs and hurt the poor most.", "Remove fossil-fuel taxes and restrictions, abolish climate units in government, end energy subsidies of any kind, and stop public funding of methane research such as AgriZero.", C("climate", "agriculture"), key=True),
    P("CON-10", "Oppose converting farmland to carbon forestry and oppose the Gene Technology Bill", ["economy", "agriculture"], None,
      "No incentives for permanent carbon forestry on productive land; keep restrictions on GMO field trials and release; revisit the Planning and Natural Environment Bills to make them workable and protect property rights.", C("agriculture") + ["news-policy-clarification-on-rural-environmental-and-agricultural-issues"]),
    P("CON-11", "Encourage oil and gas exploration with a Norway-style resource joint venture and sovereign investment fund", ["economy", "oil-gas-and-mining"],
      "The party says New Zealand has failed to secure a fair share of its resources.", "Public-private resource partnerships, royalties shared with local communities, environmental bonds, returns held in a New Zealand Investment Fund.", C("natural-resources"), key=True),
    P("CON-12", "Buy a fleet of oil tankers and build new oil refineries for fuel security", ["transport-and-infrastructure", "energy", "oil-gas-and-mining"], None,
      "Tankers would guarantee supply and floating storage until refineries able to process local and Pacific crude are built; also bring back manufacturing.", C("natural-resources", "agriculture")),
    P("CON-13", "Ensure 'cheap, reliable and abundant' energy without relying solely on solar and wind", ["transport-and-infrastructure", "energy"], None, "Renewables have a role but cannot be relied on alone because of variability.", C("energy")),
    P("CON-14", "Create a Kermadec Ocean Sanctuary and overhaul fisheries management with cameras on all commercial vessels", ["environment", "oceans", "fisheries"],
      "The party says the sustainable fisheries regime is widely abused.", "Promote the Kermadec Ocean Sanctuary Bill and reinstall surveillance cameras on commercial vessels.", C("environment") + ["news-has-new-zealand-failed-its-oceans"]),
    P("CON-15", "Increase penalties for child sexual offending and online exploitation", ["law-justice-and-government", "criminal-justice", "family-justice-and-safety"], None,
      "Longer sentences for serious and repeat offenders, review of sentence reductions, better monitoring after release, more online-exploitation investigation resources and victim support.", C("child-protection")),
    P("CON-16", "Restrict irreversible gender-related medical procedures for minors and require parental involvement", ["health", "young-people", "community-and-inclusion"], None,
      "Independent assessment before significant intervention, evidence-based practice, parental involvement subject to safeguards, and independent review mechanisms.", C("child-protection")),
    P("CON-17", "Recognise an unborn child as a legal person from the third trimester", ["health", "community-and-inclusion", "law-justice-and-government"],
      "The party says every human life has inherent dignity.", "An Unborn Child (Legal Personhood and Rights) Act with a protected right to life, without criminalising pregnant women, plus a Pregnancy and Family Support Programme (support payment, housing security, support services, adoption options).", C("right-to-life"), key=True),
    P("CON-18", "Review all trade agreements and pursue a neutral foreign policy with a support- and reconstruction-focused military", ["defence-and-foreign-affairs", "international-relations"], None,
      "Seek a balance between free trade and protectionism ('Trade before War'); avoid being drawn into conflicts that do not threaten NZ territory.", ["news-new-policies-announcement"]),
    P("CON-19", "Employment and services based on merit, 'one law for all', and 'a man is a man, and a woman is a woman'", ["community-and-inclusion", "te-ao-maori"],
      "The party opposes policies that divide people by race, ancestry, sex or identity.", "Listed among its 'policies that work' alongside limiting unskilled immigration and defending free speech and Judeo-Christian traditions.", ["site-policy", "campaign-overview"]),
]

# ------------------------------------------------------------------------------------------------ Women's Rights Party
META["womens-rights"] = {
    "name": "Women's Rights Party", "website": "https://womensrightsparty.nz/",
    "registered": "28 August 2023 (Electoral Commission register)",
    "intro": "The Women's Rights Party, a sex-based-rights feminist party, publishes 13 'policy proposal' pages (each with a "
             "Proposal and Rationale), an 'Our Priorities' page and a downloadable full policy document (Word file dated "
             "4 Nov 2025, which also contains members' policy-amendment proposals). Each distinct policy is listed below.",
    "gaps": "The full policy document is a Word file converted with pandoc; its proposal forms are tables, kept as HTML "
            "tables. No 2026-specific manifesto or costings were found; the web policy pages are undated.",
}
W = lambda x: ["proposal-" + x]
FULL = ["full-policy-docx-2025"]
_wr = "The party says women's rights must be based on biological sex rather than gender identity."
CATALOG["womens-rights"] = [
    P("WRP-01", "Ban puberty blockers and cross-sex hormones for under-18s with 'sex-related distress' and restrict funded gender surgery to over-25s", ["health", "young-people"], _wr,
      "Also an inquiry into Health NZ's contracting of PATHA to write gender-affirming care guidelines, which it notes scored poorly in the Cass Report assessment.", W("puberty-blockers-hormones-and-surgery") + FULL, key=True),
    P("WRP-02", "Record biological sex on birth certificates and repeal sex self-identification", ["community-and-inclusion", "law-justice-and-government"], _wr,
      "Amend the Births, Deaths, Marriages and Relationships Registration Act 2021 to remove 'nominated sex'; sex could be corrected only if originally recorded wrongly (e.g. undetected DSD).", FULL, key=True),
    P("WRP-03", "Oppose adding 'gender identity and gender expression' to the Human Rights Act", ["community-and-inclusion", "law-justice-and-government"],
      "The party says it could undermine sex-based exceptions.", None, W("human-rights-act") + FULL),
    P("WRP-04", "Remove 'gender, gender identity and gender expression' from the Conversion Practices Prohibition Act", ["community-and-inclusion", "law-justice-and-government"],
      "It supports protecting lesbian, gay and bisexual people from conversion practices but says 'gender' is not a clear concept for law.", None, W("conversion-practices") + FULL),
    P("WRP-05", "Replace the Prostitution Reform Act with the 'Nordic' Equality Model criminalising buyers and brothel owners", ["law-justice-and-government", "criminal-justice", "women"], None,
      "Decriminalise the prostituted person, criminalise exploiters, fund exit services; meanwhile keep section 19 (barring temporary-visa holders from sex work) to deter trafficking.", W("prostitution") + FULL, key=True),
    P("WRP-06", "Ban the 'rough sex' defence in murder and serious-harm cases", ["law-justice-and-government", "criminal-justice", "family-justice-and-safety"], "The party opposes pornography involving strangulation and violence.", None, W("rough-sex-murder-defence") + FULL),
    P("WRP-07", "Keep commercial surrogacy illegal, ban international surrogacy by New Zealanders and lengthen the birth mother's decision period", ["community-and-inclusion", "women", "law-justice-and-government"],
      "The party says surrogacy cannot be free of exploitation and having a baby by surrogacy is not a human right.", "Keep the birth mother as first legal parent with longer than seven days to decide; children should be able to learn their origins.", FULL),
    P("WRP-08", "Add 'sex' to the Sentencing Act's aggravating factors instead of creating new hate-crime laws", ["law-justice-and-government", "criminal-justice"], None,
      "Amend section 9(1)(h) to include sex, oppose 'gender identity' as an aggravating factor and oppose new hate-crime offences.", FULL),
    P("WRP-09", "Protect single-sex spaces and keep biological males out of women's prisons", ["community-and-inclusion", "women", "criminal-justice"], _wr,
      "Single-sex toilets, changing rooms, refuges, wards, sports and women-only groups (including online); school privacy from the opposite sex; supportive conditions for pregnant prisoners and mothers.", W("exit-services-for-women-leaving-gangs-religious-cults-and-se") + FULL),
    P("WRP-10", "Fund women-only refuges, exit services for women leaving gangs or cults, and support for detransitioners", ["community-and-inclusion", "family-justice-and-safety", "women"], None,
      "More resources to leave domestic violence and accessible, affordable, enforced protection orders.", W("exit-services-for-women-leaving-gangs-religious-cults-and-se")),
    P("WRP-11", "Require parents to be told what is taught in sexuality education and stop schools supporting 'social transition'", ["education", "schools"],
      "The party broadly supports the new RSE Framework because it recognises biological sex.", "Full disclosure to parents, no outside agencies such as InsideOut, teach that under-16s cannot consent, refer distressed children to professionals with parents involved.", W("educating-our-young-people") + FULL),
    P("WRP-12", "Extend paid parental leave from six to 12 months, reform Working for Families and fund continuity of midwifery care", ["incomes-and-employment", "benefits", "health"],
      "The party says mothering and caring is work that contributes to society.", "Partner leave in addition to the mother's, CPAG-style WFF reform removing discrimination against beneficiary families, wrap-around support for vulnerable mothers, free or affordable childcare and a review of for-profit ECE.", W("working-for-families-reform") + FULL, key=True),
    P("WRP-13", "Deliver pay equity in the public and private sectors and reinstate Fair Pay Agreements", ["incomes-and-employment", "wages-and-working-conditions", "women"],
      "The party says about 150,000 women's pay-equity claims were extinguished by the 2025 law change.", "A strong onus on employers and publication of average hourly pay by occupation, sex and ethnicity.", W("pay-equity") + FULL),
    P("WRP-14", "Raise minimum wages and benefits and provide free financial advice to secure older women's incomes", ["incomes-and-employment", "superannuation-and-savings", "women"],
      "The party says older women are the fastest-growing group in poverty globally.", "Living incomes, affordable housing and work with the Office for Seniors on solutions to the retirement savings gap.", W("financial-stability-for-women-in-older-age") + FULL),
    P("WRP-15", "Add a principle of the right to a clean and safe natural environment", ["environment"], None, None, W("environmental")),
    P("WRP-16", "Stand with women denied education, work and safety worldwide", ["defence-and-foreign-affairs", "international-relations", "women"], None, "Its international policy statement.", W("international")),
    P("WRP-17", "Use language in law, health and education that defines women as adult human females and motherhood as exclusively female", ["community-and-inclusion", "women"], _wr,
      "Keep words such as 'mother', 'woman' and 'breastfeeding' in maternity services.", ["our-priorities"] + FULL + W("advocating-for-women")),
]
