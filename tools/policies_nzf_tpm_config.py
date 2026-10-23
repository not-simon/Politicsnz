"""Configuration for tools/policies_nzf_tpm_build.py: NZ First and Te Pāti Māori 2026 policy archive.

SCOOP: Scoop story codes (raw/party-docs/<party>/scoop/<code>.html) used as full-text documents.
PDFS: party PDFs downloaded into raw/party-docs/<party>/ with their published URLs.
MAP: policy.nz policy id -> (group, [document keys that hold the party's own text on the policy], note)
EXTRA: policies found in party publications that policy.nz does not list (summary_source "archive").
Document keys: "scoop:<code>" or "pdf:<file>".
"""

RETRIEVED = "2026-10-23"

# --------------------------------------------------------------------------------------------- NZ FIRST
NZF_SCOOP = [
    "PA2511-S00018", "PA2512-S00181", "PA2602-S00071", "PA2602-S00102", "PA2602-S00178", "PA2603-S00062",
    "PA2603-S00137", "PA2603-S00183", "PA2603-S00187", "PA2603-S00188", "PA2604-S00094", "PA2605-S00060",
    "PA2605-S00140", "PA2605-S00199", "PA2606-S00103", "PA2606-S00132", "PA2606-S00192", "PA2606-S00202",
    "PA2607-S00038", "PA2607-S00039", "PA2607-S00044", "PA2607-S00069", "PA2607-S00134", "PA2608-S00008",
    "PA2608-S00010", "PA2608-S00133", "PA2608-S00184", "PA2608-S00205", "PA2608-S00222", "PA2608-S00261", "PA2609-S00058",
    "PA2609-S00059", "PA2609-S00118", "PA2609-S00134", "PA2609-S00193", "PA2609-S00205", "PA2609-S00261",
    "PA2609-S00276", "PA2609-S00277", "PA2610-S00076", "PA2610-S00084", "PA2610-S00087", "PA2610-S00110",
    "PA2610-S00112", "PA2610-S00133", "PA2610-S00135", "PA2610-S00145", "PA2610-S00155", "PA2610-S00162",
    "PA2610-S00174", "PA2610-S00200", "PA2610-S00209", "PO2608-S00121",
]
NZF_PDFS = {
    "Financial_Markets_Conduct_Preventing_Payment_Scamv1.5.pdf": (
        "Financial Markets Conduct (Preventing Payment Scams) Amendment Bill (draft v1.5, NZ First member's bill)",
        "https://img.scoop.co.nz/media/pdfs/2602/Financial_Markets_Conduct_Preventing_Payment_Scamv1.5.pdf",
        "Attached by NZ First to its 27 Feb 2026 press release (Scoop PA2602/S00178)."),
    "Accessibility_Standards_Billv1.4.pdf": (
        "Accessibility Standards Bill (draft v1.4, NZ First member's bill)",
        "https://img.scoop.co.nz/media/pdfs/2607/Accessibility_Standards_Billv1.4.pdf",
        "Attached by NZ First to its 8 Jul 2026 press release (Scoop PA2607/S00069)."),
}
NZF_MAP = {
    "POL54656": ("Cost of living, competition & banking", ["scoop:PA2603-S00137"], ""),
    "POL54657": ("Cost of living, competition & banking", ["scoop:PA2603-S00137"],
                 "policy.nz also cites a Labour Party release ('Labour will make price gouging illegal'); that is another party's page and is not an NZ First source."),
    "POL54658": ("Cost of living, competition & banking", ["scoop:PA2604-S00094"], ""),
    "POL54659": ("Cost of living, competition & banking", ["scoop:PA2604-S00094"], ""),
    "POL54660": ("Cost of living, competition & banking", ["scoop:PA2604-S00094"], ""),
    "POL54661": ("Mining, energy & resources", ["scoop:PA2603-S00188", "scoop:PA2603-S00187"], ""),
    "POL54662": ("Mining, energy & resources", ["scoop:PA2603-S00188", "scoop:PA2603-S00187"], ""),
    "POL54663": ("Cost of living, competition & banking", ["scoop:PA2605-S00140", "scoop:PA2605-S00199"], ""),
    "POL54664": ("Families, incomes, savings & super", ["scoop:PA2605-S00140"], ""),
    "POL54668": ("Democracy, the Treaty & Māori affairs", ["scoop:PA2606-S00132"], ""),
    "POL54746": ("Families, incomes, savings & super", ["scoop:PA2608-S00008", "scoop:PA2608-S00010"], ""),
    "POL54754": ("Economy, tax & business", ["scoop:PA2608-S00184", "scoop:PA2608-S00205"], ""),
    "POL54755": ("Economy, tax & business", ["scoop:PA2605-S00199"], ""),
    "POL54756": ("Community, culture, safety & recreation", ["scoop:PA2603-S00183"],
                 "policy.nz's second citation is the same release on community.scoop.co.nz."),
    "POL54757": ("Democracy, the Treaty & Māori affairs", ["scoop:PA2602-S00071", "scoop:PA2602-S00102"], ""),
    "POL54759": ("Democracy, the Treaty & Māori affairs", ["scoop:PA2607-S00039", "scoop:PA2609-S00118"], ""),
    "POL54961": ("Families, incomes, savings & super", ["scoop:PA2609-S00059", "scoop:PA2609-S00058", "scoop:PA2609-S00118"], ""),
    "POL54962": ("Immigration & citizenship", ["scoop:PA2609-S00118", "scoop:PA2609-S00134"], ""),
    "POL54963": ("Immigration & citizenship", ["scoop:PA2609-S00118"], ""),
    "POL54964": ("Immigration & citizenship", ["scoop:PA2609-S00118"], ""),
    "POL54965": ("Immigration & citizenship", ["scoop:PA2609-S00118"], ""),
    "POL54966": ("Immigration & citizenship", ["scoop:PA2609-S00118"], ""),
    "POL54967": ("Immigration & citizenship", ["scoop:PA2609-S00118"], ""),
    "POL55057": ("Health", ["scoop:PA2609-S00205"], ""),
    "POL55073": ("Health", ["scoop:PA2609-S00205"], ""),
    "POL55076": ("Health", ["scoop:PA2609-S00205"], ""),
    "POL55077": ("Health", ["scoop:PA2609-S00205", "scoop:PO2608-S00121"],
                 "policy.nz cites NZ First's Mill Road release (PO2608/S00121) for this item, which does not mention nutrition; the dietary-guidelines review appears in the 'Make NZ Healthy' release (PA2609/S00205, point 6)."),
    "POL55078": ("Health", ["scoop:PA2609-S00205"], ""),
    "POL55155": ("Economy, tax & business", ["scoop:PA2609-S00261"], ""),
    "POL55157": ("Democracy, the Treaty & Māori affairs", ["scoop:PA2609-S00277", "scoop:PA2609-S00276"], ""),
    "POL55234": ("Community, culture, safety & recreation", ["scoop:PA2610-S00076", "scoop:PA2511-S00018"], ""),
    "POL55257": ("Families, incomes, savings & super", ["scoop:PA2610-S00084"], ""),
    "POL55258": ("Families, incomes, savings & super", ["scoop:PA2610-S00084"], ""),
    "POL55262": ("Immigration & citizenship", ["scoop:PA2610-S00087"], ""),
    "POL55304": ("Community, culture, safety & recreation", ["scoop:PA2610-S00135"], ""),
    "POL55305": ("Housing, infrastructure & transport", ["scoop:PA2610-S00112"], ""),
    "POL55308": ("Economy, tax & business", ["scoop:PA2610-S00145", "scoop:PA2610-S00110"], ""),
    "POL55309": ("Community, culture, safety & recreation", ["scoop:PA2610-S00133"], ""),
    "POL55310": ("Housing, infrastructure & transport", ["scoop:PA2610-S00155"], ""),
}

def _x(id_, group, statement, topics, why, how, docs, note=""):
    return {"id": id_, "group": group, "statement": statement, "topics": topics,
            "why": why, "how": how, "docs": docs, "note": note}

NZF_EXTRA = [
    _x("NZF-A01", "Economy, tax & business", "Establish a $100 billion NZ Future Fund to finance a 30-year infrastructure plan",
       ["economy", "infrastructure-funding-and-planning"],
       "The party says New Zealand needs a long-term, non-political way to pay for infrastructure instead of an 'on-off approach'.",
       "This party would set up a $100 billion 'Future Fund', run at arm's length from politicians on a model similar to Singapore's Temasek, to invest in a thirty-year infrastructure plan. The party says it would fund projects it has promised (for example the Hope Bypass). The party's releases seen for this archive do not set out how the fund's $100 billion would be raised.",
       ["scoop:PA2607-S00134", "scoop:PA2608-S00133", "scoop:PA2608-S00261", "scoop:PA2610-S00209"],
       "The original announcement release was not found on Scoop; the policy is described in the leader's speeches listed."),
    _x("NZF-A02", "Mining, energy & resources", "Invest $1 billion in a 'National Subsurface Development Survey' to find and develop oil, gas, geothermal and CO2-storage resources",
       ["energy", "land-and-resources", "economy"],
       "The party says New Zealand should identify and use its own energy reserves for fuel security, citing disruption in the Strait of Hormuz.",
       "This party would invest an initial $1 billion over the term of government in a national survey creating one dataset across energy, geothermal and CO2 storage sites, plus a framework to develop those sites and extract the resources. Announced at the party's July 2026 campaign launch.",
       ["scoop:PA2607-S00134", "scoop:PA2608-S00010", "scoop:PA2608-S00261"]),
    _x("NZF-A03", "Environment, climate & farming rules", "Withdraw New Zealand from the Paris Agreement",
       ["environment", "emissions-reduction", "international-relations"],
       "The party says meeting Paris commitments could send up to $22 billion of taxpayers' money offshore while New Zealand produces about 0.17% of global emissions.",
       "This party would take New Zealand out of the Paris Agreement and says it will campaign on this at the election.",
       ["scoop:PA2606-S00103", "scoop:PA2606-S00202", "scoop:PA2607-S00038"]),
    _x("NZF-A04", "Mining, energy & resources", "Create a National Energy Strategy and stop power companies holding back supply to raise prices",
       ["energy", "prices"],
       "The party says power companies control both supply and price, driving up costs for households and industry.",
       "Alongside splitting the 'gentailers', this party would deliver a National Energy Strategy and replace the current system so that companies cannot hold back supply to drive prices higher.",
       ["scoop:PA2603-S00137"]),
    _x("NZF-A05", "Mining, energy & resources", "Set mining zones, longer permits, reopen the School of Mines and refocus the Department of Conservation",
       ["land-and-resources", "economy", "conservation", "education"],
       "The party says mining rules are duplicated, slow and inconsistent and are stopping investment and jobs.",
       "As part of its mining package this party would identify mining zones with clearer rules, lengthen mining permits to cover the life of a mine including rehabilitation, reopen the School of Mines and fund trades training, fund Mines Rescue, invest in R&D for onshore value-add, refocus DOC on areas of high conservation value, review stewardship land, remove duplication including in the Wildlife Act, and make consultation time-bound.",
       ["scoop:PA2603-S00188", "scoop:PA2603-S00187"]),
    _x("NZF-A06", "Economy, tax & business", "Allow 50% first-year depreciation on new plant and machinery for manufacturers and export sectors",
       ["economy", "business-support", "government-revenue-and-finance"],
       "The party says weak productivity and low business investment hold New Zealand back, and that front-loaded depreciation lifts investment and GDP.",
       "This party would introduce a targeted 50% first-year depreciation rate for new plant, machinery and equipment in manufacturing and targeted export sectors (such as mining, aquaculture, forestry, farming and fishing). It says this is separate from the existing 20% Investment Boost.",
       ["scoop:PA2610-S00209"]),
    _x("NZF-A07", "Economy, tax & business", "Expand the Game Development Sector Rebate and baseline funding for the Centre of Digital Excellence (CODE)",
       ["economy", "business-support", "arts-culture-and-heritage"],
       "The party says the video-game industry is growing fast but local talent is being lost to Australia because of limits on the current rebate.",
       "This party would raise the rebate rate from 20% to 40%, raise the per-studio cap from $3 million to $10 million, lift the annual appropriation from $40 million to $45 million by 2028, lower the claim threshold from $250,000 to $150,000, baseline CODE's $5 million budget and grow it to $7 million by 2028.",
       ["scoop:PA2610-S00174"]),
    _x("NZF-A08", "Law & order", "'Life means life': degrees of murder, whole-of-life sentences for first-degree murder and child rape",
       ["criminal-justice", "law-justice-and-government"],
       "The party says the justice system too often fails to hold offenders to account and victims should come before offenders.",
       "This party would create a formal 'degrees of murder' regime (1st degree: life without parole; 2nd degree: minimum non-parole period of 30 years; 3rd degree: minimum 10 years), increase sentences for attempted murder and wounding with intent from 14 to 25 years, and introduce life imprisonment for rape of children.",
       ["scoop:PA2610-S00200"]),
    _x("NZF-A09", "Law & order", "More mandatory minimum sentences, tougher parole and limits on sentence discounts",
       ["criminal-justice"],
       "The party says sentencing has not delivered justice for victims.",
       "This party would increase the use of mandatory minimum sentences for serious violent and sexual offenders, cap non-guilty-plea discounts at 10% (guilty-plea discounts stay at 25%), raise parole eligibility to 75% of the sentence for long-term offenders, require murderers to be assessed as low risk before release, set an 8-year minimum non-parole period for 'coward punch' killings, treat home burglary like aggravated burglary, and oppose any extension of the Clean Slate law.",
       ["scoop:PA2610-S00200"]),
    _x("NZF-A10", "Law & order", "Create a dedicated organised-crime agency and fold the Serious Fraud Office into Police",
       ["criminal-justice", "public-sector"],
       "The party says transnational organised crime is growing and needs to be dismantled.",
       "This party would establish a dedicated agency, with a responsible minister, to dismantle transnational criminal networks, ensure Police have the resources they need, and abolish the SFO, replacing it with a specialised division inside NZ Police.",
       ["scoop:PA2610-S00200"]),
    _x("NZF-A11", "Law & order", "Strengthen self-defence protections, including investigating 'Castle Doctrine' laws",
       ["criminal-justice", "family-justice-and-safety"],
       "The party says people should be able to defend themselves and their property in their home or business.",
       "This party would investigate 'Castle Doctrine' and 'Stand Your Ground' laws (no duty to retreat), change Police and Solicitor-General prosecution guidelines so people who 'excessively defend' themselves at home or work are treated as victims unless there is overwhelming contrary evidence, and require the Solicitor-General to review any such prosecution.",
       ["scoop:PA2610-S00200"]),
    _x("NZF-A12", "Law & order", "State-funded immediate reparation for victims, faster publication of sentencing notes, less name suppression",
       ["criminal-justice", "civil-justice"],
       "The party says victims should come first and the courts should be more open.",
       "This party would have the state pay immediate reparation to victims and then recover it from offenders, require District Courts to publish sentencing notes within 72 hours, limit final name suppression to extreme cases, and review traffic penalty regimes for consistency.",
       ["scoop:PA2610-S00200"]),
    _x("NZF-A13", "Immigration & citizenship", "Grant automatic citizenship at birth only to children of citizens",
       ["migration"],
       "The party says permanent residence is easy to get and children of non-citizens currently become citizens automatically.",
       "This party would change birthright citizenship so that only the children of New Zealand citizens are automatically citizens at birth (currently a parent with indefinite residence also qualifies).",
       ["scoop:PA2609-S00118"]),
    _x("NZF-A14", "Immigration & citizenship", "Make refugee/protected-person status temporary and tighten asylum rules",
       ["migration", "international-relations"],
       "The party says asylum claims have risen and the system cannot distinguish genuine claims from people using it as another immigration pathway.",
       "This party would give refugees and protected persons a renewable 24-month residence permit reviewed against conditions in their home country (modelled on Denmark), bar asylum claims from people in New Zealand on a 'working-class visa', and stop temporary work rights during assessment being used as a stepping-stone to another visa.",
       ["scoop:PA2609-S00118"]),
    _x("NZF-A15", "Immigration & citizenship", "Hold a referendum on a legislated cap of 20,000 resident visas a year",
       ["migration", "infrastructure-funding-and-planning", "parliament-and-democracy"],
       "The party says population growth must not outpace infrastructure and New Zealanders should decide the size of the country.",
       "This party would hold a referendum on a legislated annual cap of 20,000 resident visas, linked to infrastructure capacity and a 30-year Population Plan.",
       ["scoop:PA2609-S00118"]),
    _x("NZF-A16", "Immigration & citizenship", "Require student visa holders to leave New Zealand before applying for a different visa",
       ["migration", "education"],
       "The party says export education is being used as a route to work and residence.",
       "This party would require student visa holders who want to switch to another visa to leave and reapply from abroad.",
       ["scoop:PA2609-S00118"]),
    _x("NZF-A17", "Health", "Other 'Make NZ Healthy' commitments: informed consent, metabolic health, recognising nurses, vitamin D review, research on agricultural sprays",
       ["health", "public-health", "agriculture"],
       "The party says the health system spends almost all its money treating illness rather than preventing it.",
       "In its 15-point 'Make NZ Healthy' plan this party also commits to put prevention 'back at the heart of healthcare', focus on metabolic health, make informed consent a core part of care, recognise consumer choice, find better ways to acknowledge nurses, fund a review of vitamin D levels, fund hospital trials of intravenous vitamin C, and invest in agricultural innovation including alternatives to potentially harmful sprays.",
       ["scoop:PA2609-S00205"]),
    _x("NZF-A18", "Health", "Hold a select committee inquiry into COVID-19 vaccine injuries",
       ["health", "parliament-and-democracy"],
       "The party says the recent COVID-19 inquiry report did not go far enough on vaccine safety and who was affected.",
       "This party would establish a select committee inquiry into injuries the vaccine 'may have caused', so that those affected can give evidence publicly and decision-makers can be held to account.",
       ["scoop:PA2603-S00062"]),
    _x("NZF-A19", "Families, incomes, savings & super", "Keep NZ Super universal at 65 with no means testing, and no asset sales",
       ["seniors", "benefits", "economy"],
       "The party presents itself as the defender of superannuitants and opposes privatisation.",
       "The party states: 'No government with New Zealand First will be selling our assets. No government with New Zealand First will touch our seniors’ superannuation – no means testing, no eligibility age increase, no indexing.'",
       ["scoop:PA2605-S00140"]),
    _x("NZF-A20", "Families, incomes, savings & super", "Reform retirement village law without retrospective three-month buy-backs",
       ["seniors", "housing"],
       "The party says retirement villages are an important housing option for seniors but residents need more protection and choice.",
       "The party backs the Retirement Villages Amendment Bill announced for introduction next term, says it will deliver reform that protects residents and keeps the sector sustainable, and opposes proposals for retrospective three-month buy-backs.",
       ["scoop:PA2609-S00193"]),
    _x("NZF-A21", "Housing, infrastructure & transport", "Bring back the Southerner passenger train and make the Mainlander more frequent",
       ["public-transport-cycling-and-walking", "transport-and-infrastructure"],
       "The party says South Island cities and towns should be reconnected by rail.",
       "This party would work with the operators of the Mainlander service to secure a commercially sound agreement that runs more trains between Christchurch, Dunedin and Invercargill.",
       ["scoop:PA2610-S00155"]),
    _x("NZF-A22", "Housing, infrastructure & transport", "Make the Mill Road extension in South Auckland a priority",
       ["transport-and-infrastructure", "infrastructure-funding-and-planning"],
       "The party says South Auckland has grown without the roads it needs.",
       "The party leader announced at its campaign launch in Manukau that extending and completing Mill Road (Manukau–Takanini–Papakura–Drury) would be a priority for a future NZ First-led government.",
       ["scoop:PO2608-S00121"]),
    _x("NZF-A23", "Housing, infrastructure & transport", "Regional infrastructure: new Matakana Island wharf and support for Sun Air's Bay of Plenty services",
       ["transport-and-infrastructure", "economic-development-and-industry"],
       "The party describes a 'Regional Infrastructure Plan' to back the provinces.",
       "The party leader announced the party would help Sun Air maintain its Bay of Plenty services and build a new wharf at Matakana Island.",
       ["scoop:PA2609-S00276"]),
    _x("NZF-A24", "Environment, climate & farming rules", "Introduce a nationwide container return scheme",
       ["environment", "fresh-water-and-pollution", "local-government"],
       "The party says billions of beverage containers end up as litter and ratepayers carry the cost.",
       "This party has introduced a member's bill for a scheme that puts a small refundable deposit on beverage containers, with operational details set by regulation.",
       ["scoop:PA2605-S00060"]),
    _x("NZF-A25", "Environment, climate & farming rules", "Pause Waikato Regional Council's Plan Change 1 farm rules",
       ["agriculture", "fresh-water-and-pollution", "local-government"],
       "The party says Plan Change 1 would force thousands of Waikato and Waipā farms into costly consents under a planning system that is being replaced.",
       "This party calls for PC1 implementation to be paused until the replacement RMA system is in place, existing lawful farming is protected, and future freshwater rules pass a 'primary production viability test'.",
       ["scoop:PA2607-S00044"]),
    _x("NZF-A26", "Environment, climate & farming rules", "Oppose liberalising genetic engineering without adequate safeguards",
       ["agriculture", "environment", "trade-and-exports"],
       "The party says New Zealand's export reputation is built on its GE-free label.",
       "The party says it will not support the government's gene technology legislation as it stands and is against liberalisation without adequate safeguards.",
       ["scoop:PA2606-S00103"]),
    _x("NZF-A27", "Economy, tax & business", "Make banks liable for preventable payment scams (Preventing Payment Scams bill)",
       ["economy", "business-support", "criminal-justice"],
       "The party says the banks' own code on scams is 'by banks for banks' and too weak.",
       "This party's member's bill would impose a duty on both sending and receiving banks to protect consumers, require confirmation of payee, know-your-customer checks, urgent account freezing and information sharing, and make the default that losses are not borne by the consumer when a bank fails that duty.",
       ["scoop:PA2602-S00178", "pdf:Financial_Markets_Conduct_Preventing_Payment_Scamv1.5.pdf"]),
    _x("NZF-A28", "Community, culture, safety & recreation", "Set national accessibility standards (Accessibility Standards Bill)",
       ["disability", "community-and-inclusion"],
       "The party says about 17% of New Zealanders are disabled and face avoidable barriers.",
       "This party's member's bill would create a framework for practical accessibility standards, especially for new public buildings, transport, housing and digital services.",
       ["scoop:PA2607-S00069", "pdf:Accessibility_Standards_Billv1.4.pdf"]),
    _x("NZF-A29", "Community, culture, safety & recreation", "Oppose a social media ban for under-16s",
       ["internet-and-digital-technologies", "young-people"],
       "The party says such a ban cannot work without banning VPNs or requiring digital ID, which would erode privacy, freedoms and parental rights.",
       "The party will not support legislation (National's or Labour's) to ban social media for under-16s.",
       ["scoop:PA2608-S00222", "scoop:PA2610-S00162"]),
    _x("NZF-A30", "Economy, tax & business", "Oppose the New Zealand–India free trade agreement",
       ["trade-and-exports", "migration", "international-relations"],
       "The party says the deal includes immigration and Paris Agreement clauses and investment commitments that are bad for New Zealand.",
       "The party opposes the India FTA as signed and has used 'agree to disagree' provisions in government on it.",
       ["scoop:PA2512-S00181", "scoop:PA2606-S00192"]),
]

NZF_HEADLINE = [
    ("Ruled out Labour", "“And just quietly, for the umpteenth time. New Zealand First will not be going with Labour.”", "scoop:PA2606-S00202"),
    ("No asset sales; NZ Super untouched", "“No government with New Zealand First will be selling our assets. No government with New Zealand First will touch our seniors’ superannuation – no means testing, no eligibility age increase, no indexing.”", "scoop:PA2605-S00140"),
    ("Immigration portfolio", "“It is imperative that a New Zealand First Minister holds the Immigration portfolio when part of the next coalition government to ensure the oversight, control and reform of the immigration system.”", "scoop:PA2609-S00118"),
    ("First 100 days", "Legislation to abolish the Waitangi Tribunal and replace it with a Treaty of Waitangi Completion Commission, and the fireworks ban bill, “will be tabled … within the first hundred days”.", ["scoop:PA2609-S00277", "scoop:PA2610-S00076"]),
]
NZF_SIGNATURE = ["POL54656", "POL54658", "POL54663", "POL54661", "POL54664", "NZF-A01", "NZF-A03", "POL54759",
                 "POL54961", "POL54757", "POL55157", "NZF-A02", "POL54746", "POL55155"]

# ------------------------------------------------------------------------------------------ TE PĀTI MĀORI
TPM_SCOOP = [
    "PA2502-S00022", "PA2601-S00112", "PA2601-S00115", "PA2602-S00040", "PA2602-S00082", "PA2602-S00141",
    "PA2603-S00004", "PA2603-S00110", "PA2604-S00015", "PA2604-S00042", "PA2604-S00046", "PA2605-S00134",
    "PA2606-S00066", "PA2608-S00006", "PA2608-S00044", "PA2608-S00238", "PA2609-S00008", "PA2609-S00161",
    "PA2609-S00211", "PA2609-S00245", "PA2610-S00026", "PA2610-S00052", "PA2610-S00101",
]
TPM_PDFS = {
    "A_Kiwi_Tax_Plan.pdf": ("A Kiwi Tax Plan — Te Pāti Māori Policy Manifesto 2026: Tax",
                            "https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf",
                            "Attached by Te Pāti Māori to its 26 Aug 2026 press release (Scoop PA2608/S00238)."),
    "TIRITI_ENTRENCHMENT_POLICY.pdf": ("Te Tiriti Entrenchment Policy 2026",
                                       "https://img.scoop.co.nz/media/pdfs/2609/TIRITI_ENTRENCHMENT_POLICY.pdf",
                                       "Attached by Te Pāti Māori to its 1 Sep 2026 press release (Scoop PA2609/S00008)."),
    "Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf": ("Energy Sovereignty Policy 2026",
                                                         "https://img.scoop.co.nz/media/pdfs/2609/Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf",
                                                         "Attached by Te Pāti Māori to its 16 Sep 2026 press release (Scoop PA2609/S00161)."),
    "KAI_SOVEREIGNTY_POLICY_2026.pdf": ("Kai Sovereignty Policy 2026",
                                        "https://img.scoop.co.nz/media/pdfs/2609/KAI_SOVEREIGNTY_POLICY_2026.pdf",
                                        "Attached by Te Pāti Māori to its 21 Sep 2026 press release (Scoop PA2609/S00211)."),
    "justice-drive-1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx.pdf": ("Justice — Te Pāti Māori Policy Manifesto 2026",
                                        "https://drive.google.com/file/d/1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx/view",
                                        "Google Drive file 'Justice.pdf' linked from maoriparty.org.nz (cited by policy.nz); downloaded directly from Google Drive (PDF created 18 May 2026)."),
    "mana-motuhake-drive-1Y9GTi2VGAYIJygAmaQ5e-WVCLYlCOYTL.pdf": ("Mana Motuhake Policy (2023 document — NOT confirmed as 2026 policy)",
                                        "https://drive.google.com/file/d/1Y9GTi2VGAYIJygAmaQ5e-WVCLYlCOYTL/view",
                                        "Google Drive file cited on Wikipedia as Te Pāti Māori's 'Mana Motuhake Policy'. The PDF metadata shows it was created on 29 Aug 2023, i.e. for the 2023 election. It is included only for reference because the party's 2026 'Mana Motuhake' page could not be retrieved; do not treat it as the 2026 text."),
}
TPM_MAP = {
    "POL54647": ("Health, disability & whānau", [], ""),
    "POL54649": ("Kai, cost of living & economy", ["pdf:KAI_SOVEREIGNTY_POLICY_2026.pdf", "scoop:PA2609-S00211"],
                 "policy.nz cites the party's June 2026 'Kai Sovereignty' web page (blocked); the September 2026 Kai Sovereignty Policy PDF is the party's later full policy."),
    "POL54650": ("Kai, cost of living & economy", ["pdf:KAI_SOVEREIGNTY_POLICY_2026.pdf", "scoop:PA2609-S00211"], ""),
    "POL54679": ("Education & te reo Māori", ["scoop:PA2608-S00006"], ""),
    "POL54680": ("Environment, climate & energy", ["scoop:PA2602-S00040"], ""),
    "POL54681": ("Environment, climate & energy", [], ""),
    "POL54682": ("Environment, climate & energy", [], ""),
    "POL54683": ("Foreign affairs & defence", [], ""),
    "POL54684": ("Foreign affairs & defence", [], ""),
    "POL54688": ("Foreign affairs & defence", ["scoop:PA2603-S00004"], ""),
    "POL54690": ("Foreign affairs & defence", [], ""),
    "POL54795": ("Te Tiriti, constitution & democracy", ["scoop:PA2608-S00044", "pdf:TIRITI_ENTRENCHMENT_POLICY.pdf"], ""),
    "POL54802": ("Te Tiriti, constitution & democracy", ["scoop:PA2502-S00022"],
                 "This commitment dates from February 2025; the September 2026 Entrenchment Policy proposes an independent Te Tiriti Commission (see POL54917)."),
    "POL54812": ("Tax", ["pdf:A_Kiwi_Tax_Plan.pdf", "scoop:PA2608-S00238"], ""),
    "POL54917": ("Te Tiriti, constitution & democracy", ["pdf:TIRITI_ENTRENCHMENT_POLICY.pdf", "scoop:PA2609-S00008", "scoop:PA2605-S00134"], ""),
    "POL54919": ("Te Tiriti, constitution & democracy", ["pdf:TIRITI_ENTRENCHMENT_POLICY.pdf", "scoop:PA2609-S00008"], ""),
    "POL54921": ("Te Tiriti, constitution & democracy", ["pdf:TIRITI_ENTRENCHMENT_POLICY.pdf", "scoop:PA2609-S00008"],
                 "A 2023 Te Pāti Māori 'Mana Motuhake Policy' PDF is archived for reference (documents/pdf-mana-motuhake-1y9gti2vgayijygamaq5e-wvclylcoytl.md); it predates 2026 and is not cited as 2026 policy."),
    "POL54938": ("Tax", ["pdf:A_Kiwi_Tax_Plan.pdf", "scoop:PA2608-S00238", "pdf:KAI_SOVEREIGNTY_POLICY_2026.pdf"], ""),
    "POL54939": ("Tax", ["pdf:A_Kiwi_Tax_Plan.pdf", "scoop:PA2608-S00238"], ""),
    "POL54940": ("Tax", ["pdf:A_Kiwi_Tax_Plan.pdf"], ""),
    "POL54941": ("Tax", ["pdf:A_Kiwi_Tax_Plan.pdf"], ""),
    "POL54942": ("Tax", ["pdf:A_Kiwi_Tax_Plan.pdf"], ""),
    "POL54943": ("Tax", ["pdf:A_Kiwi_Tax_Plan.pdf"], ""),
    "POL54968": ("Tax", ["pdf:A_Kiwi_Tax_Plan.pdf"], ""),
    "POL55000": ("Health, disability & whānau", [], ""),
    "POL55001": ("Health, disability & whānau", [], ""),
    "POL55058": ("Environment, climate & energy", ["pdf:Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf", "scoop:PA2609-S00161"], ""),
    "POL55059": ("Environment, climate & energy", ["pdf:Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf", "scoop:PA2609-S00161"], ""),
    "POL55060": ("Environment, climate & energy", ["pdf:Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf", "scoop:PA2609-S00161", "scoop:PA2604-S00042", "scoop:PA2606-S00066"], ""),
    "POL55061": ("Environment, climate & energy", ["pdf:Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf"], ""),
    "POL55062": ("Environment, climate & energy", ["pdf:Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf", "scoop:PA2609-S00161"], ""),
    "POL55063": ("Environment, climate & energy", ["pdf:Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf"], ""),
    "POL55064": ("Environment, climate & energy", ["pdf:Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf"], ""),
    "POL55065": ("Education & te reo Māori", [], ""),
    "POL55066": ("Health, disability & whānau", [], ""),
    "POL55067": ("Health, disability & whānau", [], ""),
    "POL55068": ("Arts, culture, sport & takatāpui", [], ""),
    "POL55070": ("Justice", ["pdf:justice-drive-1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx.pdf"],
                 "policy.nz cites the party's 'Justice' web page (blocked); the Justice chapter of the party's 2026 manifesto (Google Drive PDF) was retrieved."),
    "POL55071": ("Housing", ["scoop:PA2601-S00115"], ""),
    "POL55072": ("Arts, culture, sport & takatāpui", ["scoop:PA2610-S00101"], ""),
    "POL55085": ("Environment, climate & energy", [], ""),
    "POL55086": ("Arts, culture, sport & takatāpui", ["scoop:PA2609-S00245"], ""),
    "POL55087": ("Kai, cost of living & economy", [], ""),
    "POL55088": ("Kai, cost of living & economy", [], ""),
    "POL55283": ("Justice", ["pdf:justice-drive-1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx.pdf", "scoop:PA2601-S00112"], ""),
}
TPM_EXTRA = [
    _x("TPM-A01", "Tax", "Introduce a 2% Vacant House Tax",
       ["housing", "government-revenue-and-finance"],
       "The party says 111,700 homes across Aotearoa are empty while whānau need housing.",
       "This party would implement a Vacant House Tax of 2% as part of its Kiwi Tax Plan.",
       ["pdf:A_Kiwi_Tax_Plan.pdf", "scoop:PA2608-S00238"]),
    _x("TPM-A02", "Tax", "Invest $1 billion in Inland Revenue, the SFO, the FMA and the Financial Intelligence Unit to fight tax evasion",
       ["government-revenue-and-finance", "criminal-justice"],
       "The party says aggressive tax avoidance must be eliminated so everyone pays their fair share.",
       "This party would increase investment by $1 billion across IRD, the Serious Fraud Office, the Financial Markets Authority and the NZ Financial Intelligence Unit.",
       ["pdf:A_Kiwi_Tax_Plan.pdf"]),
    _x("TPM-A03", "Te Tiriti, constitution & democracy", "Establish a $220 million Mātike Mai Fund and set 2040 as the target for constitutional transformation",
       ["te-tiriti-o-waitangi-and-governance", "parliament-and-democracy"],
       "The party says Māori-led constitutional work (Mātike Mai Aotearoa) has been done but lacks resources and enforceable accountability.",
       "This party would fund a $220 million Mātike Mai Fund over four years to independently resource iwi, hapū and Māori to lead constitutional transformation, with 2040 as the target. It says it will not itself determine the constitutional destination.",
       ["pdf:TIRITI_ENTRENCHMENT_POLICY.pdf", "scoop:PA2609-S00008"]),
    _x("TPM-A04", "Te Tiriti, constitution & democracy", "Require a Te Tiriti Impact Statement for every Bill",
       ["te-tiriti-o-waitangi-and-governance", "parliament-and-democracy"],
       "The party says governments can ignore the Waitangi Tribunal and weaken Te Tiriti protections.",
       "This party would require every Bill before Parliament to include a Te Tiriti Impact Statement.",
       ["scoop:PA2608-S00044"]),
    _x("TPM-A05", "Te Tiriti, constitution & democracy", "Entrench the Māori electorates in the constitution",
       ["parliament-and-democracy", "te-ao-maori"],
       "The party says the Māori seats are guaranteed under Te Tiriti and should not be removable by referendum (responding to NZ First's referendum proposal).",
       "The party says that when it forms the next government it will 'entrench the Māori seats in the constitution beyond the reach of referendums'.",
       ["scoop:PA2602-S00082"]),
    _x("TPM-A06", "Kai, cost of living & economy", "$100 million Community Kai Fund and $100 million for regenerative Māori agriculture (Mātai Ahuwhenua)",
       ["agriculture", "community-and-inclusion", "te-ao-maori"],
       "The party says whānau should be able to grow their own kai rather than depend on food parcels and the supermarket duopoly.",
       "This party would set up a $100 million Community Kai Fund for home gardens, marae māra kai and community food farms, invest an extra $100 million in Mātai Ahuwhenua for regenerative and diversified Māori land-based production, and protect Māori seed, mātauranga and Indigenous plant whakapapa including through WAI 262 protections.",
       ["pdf:KAI_SOVEREIGNTY_POLICY_2026.pdf", "scoop:PA2609-S00211"]),
    _x("TPM-A07", "Environment, climate & energy", "Give the Commerce Commission and Electricity Authority stronger powers over power prices and profits",
       ["energy", "prices"],
       "The party says energy is essential infrastructure that must serve people before profit.",
       "This party would strengthen regulators' powers to investigate excessive pricing and profits, with structural intervention, pricing tools and enforceable remedies if regulation fails, and remove barriers to whānau and communities generating and trading energy. It sets 2035 as the target for 'Energy Sovereignty'.",
       ["pdf:Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf", "scoop:PA2609-S00161"]),
    _x("TPM-A08", "Education & te reo Māori", "Te Kōhanga Reo Act, secure baseline funding and 20 new kōhanga reo",
       ["early-childhood-education", "te-reo-maori-and-culture"],
       "The party says kōhanga reo are the heartbeat of te reo Māori revitalisation and need long-term certainty.",
       "This party would pass a Te Kōhanga Reo Act, lock in annual baseline funding, create a $20 million-a-year capital fund, invest $50 million to clear the backlog of around 80 kōhanga needing new builds or refurbishment, and fund 20 new kōhanga reo over three years.",
       ["scoop:PA2610-S00052"]),
    _x("TPM-A09", "Education & te reo Māori", "$1.25 billion for kura Māori property and restore Te Ahu o Te Reo Māori",
       ["schools", "te-reo-maori-and-culture"],
       "The party says kura need fit-for-purpose buildings and the education workforce needs te reo capability.",
       "This party would commit $1.25 billion over five years ($250 million a year) through a ring-fenced kura Māori property plan, and restore Te Ahu o Te Reo Māori with $30 million a year.",
       ["scoop:PA2610-S00052"]),
    _x("TPM-A10", "Education & te reo Māori", "Expand school lunches, free public transport for students, free school counselling, te reo Māori core to Year 10",
       ["schools", "education", "public-transport-cycling-and-walking"],
       "The party says Māori learners thrive when whānau are central and identity is upheld.",
       "Alongside the Māori Education Authority, the party's education policy includes expanding school lunches, free public transport for all students, free school counselling, making te reo Māori a core curriculum subject through Year 10, more student support and a stronger education workforce.",
       ["scoop:PA2608-S00006"]),
    _x("TPM-A11", "Arts, culture, sport & takatāpui", "Independent Toi Māori Authority and an income programme for 1,000 Māori artists",
       ["arts-culture-and-heritage", "te-ao-maori"],
       "The party says colonisation targeted Māori artists and knowledge-holders and decisions on Toi Māori should be in Māori hands.",
       "This party would create a Toi Māori Authority independent of Creative New Zealand, funded at parity with it and governed by tohunga toi, and a rotating programme paying 1,000 artists at a time for 30 hours a week over two years.",
       ["scoop:PA2610-S00101"]),
    _x("TPM-A12", "Arts, culture, sport & takatāpui", "$200 million over three years and an independent Takatāpui-governed Commission",
       ["community-and-inclusion", "health", "housing"],
       "The party says decisions about takatāpui have been made without takatāpui.",
       "This party would commit $200 million over three years (reported as reprioritised from health, social development, housing and Māori development) and create an independent Takatāpui-governed Commission with authority over ring-fenced funding for gender-affirming kaupapa Māori healthcare, mental health and suicide prevention, safe housing, protection from violence and hate, culture and education.",
       ["scoop:PA2609-S00245"],
       "The funding breakdown by portfolio comes from news coverage (RNZ reports co-leader Rawiri Waititi gave it: $100m Health, $50m Social Development, $40m Housing, $10m Vote Māori), not from the party release archived here."),
    _x("TPM-A13", "Justice", "Create an independent Māori Justice Authority funded from half of the Corrections, Police and Courts budgets",
       ["criminal-justice", "te-ao-maori"],
       "The party says the justice system was imposed on Māori, breaches Te Tiriti and over-incarcerates Māori.",
       "This party would establish a tikanga-led Independent Māori Justice Authority with real decision-making power, funded by reallocating 50% of Vote Corrections, 50% of Vote Police and 50% of Vote Courts, and invest in kaupapa Māori legal aid and community law services.",
       ["pdf:justice-drive-1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx.pdf"]),
    _x("TPM-A14", "Justice", "Repeal three strikes, gang and bail laws; raise the age of criminal responsibility to 16",
       ["criminal-justice", "young-people"],
       "The party says these laws discriminate against Māori and criminalise rangatahi early.",
       "This party would repeal three-strikes legislation, gangs legislation, the Sentencing (Reform) Amendment Act and the Bail Amendment Act, raise the age of criminal responsibility from 10 to 16, extend the Clean Slate Act to custodial sentences, require police body cameras, replace the IPCA with a Māori-grounded oversight body and reinstate funding for cultural (s27) reports.",
       ["pdf:justice-drive-1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx.pdf"]),
    _x("TPM-A15", "Justice", "Decriminalise drug use and close military-style bootcamps and youth justice residences",
       ["criminal-justice", "health", "young-people"],
       "The party says drug use is a health issue and youth residences harm rangatahi.",
       "This party would overhaul the Misuse of Drugs Act to treat drug use as a health issue and wipe convictions for use and possession, close military-style bootcamps immediately and youth justice residences by 2030, end solitary confinement as punishment, and (under 'electoral justice') restore voting rights for all people in Corrections facilities and lower the voting age to 16.",
       ["pdf:justice-drive-1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx.pdf"]),
    _x("TPM-A16", "Housing", "Universal rent control and an end to no-cause evictions",
       ["housing", "housing-affordability"],
       "The party says renters need security amid a housing crisis.",
       "The party's housing policy includes supporting renters through universal rent control and repealing no-cause evictions, and taxing property investors.",
       ["scoop:PA2601-S00115"]),
    _x("TPM-A17", "Housing", "Build 2,000 papakāinga homes and allocate half of new social housing to whānau Māori",
       ["housing", "social-and-public-housing", "te-ao-maori"],
       "The party says Māori make up half of the social housing waitlist and homelessness is a Te Tiriti breach.",
       "The party's housing policy includes building 2,000 houses on papakāinga, radically increasing public housing investment, and allocating 50% of new social housing builds to whānau Māori; its Tāmaki Makaurau MP has a member's bill to prevent youth homelessness.",
       ["scoop:PA2601-S00115", "scoop:PA2602-S00141"]),
    _x("TPM-A18", "Housing", "Stop all sales of freehold land to offshore foreign interests",
       ["housing", "foreign-investment", "land-and-resources"],
       "The party says land should not be sold to overseas buyers.",
       "The party's housing policy includes stopping all sales of freehold land to offshore foreign interests.",
       ["scoop:PA2601-S00115"]),
    _x("TPM-A19", "Health, disability & whānau", "Fund a Marae Resilience Package so marae can act as civil-defence hubs",
       ["climate-adaptation", "community-and-inclusion", "te-ao-maori"],
       "The party says marae act as frontline shelters in emergencies without formal support or funding.",
       "The party has called for formal recognition of marae as emergency response hubs, upfront funding for emergency supplies and infrastructure, generators, water storage and communications, and long-term investment.",
       ["scoop:PA2604-S00046"],
       "Made as a call on the current government (April 2026) rather than as a manifesto document."),
    _x("TPM-A20", "Kai, cost of living & economy", "Freeze MPs' pay rises and suspend fuel excise tax (cost-of-living calls)",
       ["prices", "parliament-and-democracy"],
       "The party says politicians should not get pay rises while whānau struggle, and fuel excise adds about $35 to a 50-litre fill.",
       "The party has called for an immediate freeze on pay rises for MPs, Ministers and the Prime Minister (with a deeper cut for Ministers and the PM), and for the immediate suspension of fuel excise tax.",
       ["scoop:PA2604-S00015", "scoop:PA2603-S00110"],
       "Made as calls on the current government in March/April 2026."),
]
TPM_HEADLINE = [
    ("Electoral strategy", "“Candidate vote Te Pāti Māori. Party vote Green or Labour, you choose.” The party list has one candidate (General Secretary Lance Norman) beyond its seven Māori electorate candidates.", "scoop:PA2610-S00026"),
    ("Goal", "“Our strategy is clear. We want more Māori in Parliament, a one-term Government, and an independent Māori voice that is accountable to our people.”", "scoop:PA2610-S00026"),
    ("Constitutional reform", "“Te Tiriti is the constitutional foundation of Aotearoa. Its mana does not rise and fall depending on who forms the Government.” — Entrenchment policy: binding Waitangi Tribunal recommendations, a Te Tiriti Commission with compliance-order powers, a $220m Mātike Mai Fund, UNDRIP action plan within 100 days.", "scoop:PA2609-S00008"),
    ("Tax", "Kiwi Tax Plan: first $30,000 tax-free, top rate 48% over $300,000, wealth tax from 1.5% above $2m net wealth, company tax back to 33%. (NZ First's leader said Te Pāti Māori called its tax policy a “bottom line”; this archive could not retrieve a Te Pāti Māori statement using that phrase.)", "pdf:A_Kiwi_Tax_Plan.pdf"),
]
TPM_SIGNATURE = ["POL54812", "POL54939", "POL54938", "POL54917", "POL54795", "TPM-A03", "POL54679", "POL55059",
                 "POL55283", "TPM-A13", "POL54684", "POL54680", "TPM-A12", "TPM-A08"]

# extra non-party links (news coverage) for archive items, shown as "Coverage" links
EXTRA_LINKS = {
    "TPM-A12": [("NZ Herald: Te Pāti Māori announces $200m fund to create Takatāpui commission",
                 "https://www.nzherald.co.nz/nz/politics/election-2026-te-pati-maori-announces-200m-fund-to-create-takatapui-commission/6V6TE7RCBJCFVIUVRTE53VHJTQ/"),
                ("RNZ: Te Pāti Māori promises $200 million to change 'who holds power' for decisions about takatāpui",
                 "https://www.rnz.co.nz/news/politics_election-2026/1530281/te-pati-maori-promises-200-million-to-change-who-holds-power-for-decisions-about-takatapui")],
    "NZF-A01": [],
}

# ============================================================================ COMMON CRAWL ROUND (23 Oct 2026)
# Pages captured by Common Crawl (raw/party-docs/<party>/cc_html/, see tools/policies_nzf_tpm_cc_*.py) archived as
# documents in addition to every policy.nz-cited page that has a capture.
NZF_CC = [
    "policy", "breaking_up_the_gentailers", "break_up_the_supermarket_duopoly", "returning_50_of_mining_royalties_to_the_regions",
    "establishing_a_kiwisaver_generation", "backing_a_new_zealand_owned_bank", "disestablish_auckland_s_independent_maori_statutory_board",
    "referendum_on_maori_seats", "establishing_a_special_economic_zone_at_marsden_point", "complete_the_christchurch_cathedral",
    "citizens_only_voting", "future_proofing_our_fuel_security", "the_kiwi_kids_grant", "use_it_or_lose_it_dairy_policy",
    "withdraw_from_paris_accord", "the_100bn_new_zealand_future_fund", "nz_super_for_citizens_only", "immigration_reform_policies",
    "the_plan_to_make_nz_healthy", "20_tax_rate_for_smes", "ending_the_waitangi_makework_industry",
    "our-members-bills", "maori_seats_referendum_bill", "the_fireworks_prohibition_legislation_bill", "the_container_return_scheme_bill",
    "local_government_auckland_council_disestablishment_of_imsb_amendment_bill", "preventing_payment_scams_bill",
    "the_accessibility_standards_bill", "prostate_cancer_screening_bill", "nz_first_introduces_bill_to_protect_against_digital_id_overreach",
    "nzf_bill_legislating_nzs_name", "cash_transactions_protection_bill", "definitions-woman-man-bill", "repeal-of-dei-requirements-bill",
    "english-language-bill-passes-first-reading", "conscience-referendums-bill", "fluoridation-referendum-bill",
    "display_of_flags_government_premises_bill", "nz_first_lodges_differing_view_on_the_gene_tech_bill",
    "the_kiwisaver_generation_and_bnz_buy_back", "nzf_pillars",
]
TPM_CC = [
    "policy", "energy_sovereignty", "te_tiriti_entrenchment", "tax", "takat_pui", "kai_sovereignt", "mokopuna_m_ori", "disabilities",
    "housing", "education_training", "toi_maori", "te_reo_maori", "health", "mana_motuhake", "justice", "economic_development",
    "cost_of_living", "military_neutrality", "freshwater_policy", "climate", "maori_sports", "mana_hau_policy",
    "we_want_cheaper_power_and_we_want_our_people_to_own_it",
]
CC_TOOL = {"te-pati-maori": "what-matters-to-you"}   # page whose embedded manifesto data is archived specially

NZF_PDFS.update({
    "Fireworks_Prohibition_Legislation_Bill.pdf": ("Fireworks Prohibition Legislation Bill (NZ First member's bill)",
        "https://assets.nationbuilder.com/nzfirst/pages/8447/attachments/original/1762913986/Fireworks_Prohibition_Legislation_Bill.pdf?1762913986",
        "Linked from nzfirst.nz/the_fireworks_prohibition_legislation_bill; downloaded directly from assets.nationbuilder.com."),
    "Container_Return_Scheme_Bill-v1.5_1.pdf": ("Container Return Scheme Bill (draft v1.5, NZ First member's bill)",
        "https://assets.nationbuilder.com/nzfirst/pages/9701/attachments/original/1778203177/Container_Return_Scheme_Bill-v1.5_%281%29.pdf?1778203177",
        "Linked from nzfirst.nz/the_container_return_scheme_bill; downloaded directly from assets.nationbuilder.com."),
})
_D = "Te Pāti Māori Policy Manifesto 2026 chapter, Google Drive file linked ('Click here' / full policy) from the party's policy page"
def _drv(i): return f"https://drive.google.com/file/d/{i}/view"
TPM_PDFS.update({
    "drive/11dbbk3BTNigHUb4xANPnTKxb2TC9dAgg.pdf": ("Tax — Te Pāti Māori Policy Manifesto 2026 (Drive edition)", _drv("11dbbk3BTNigHUb4xANPnTKxb2TC9dAgg"), _D + " maoriparty.org.nz/tax. Same policy as the Scoop-hosted A Kiwi Tax Plan PDF; extraction differs slightly."),
    "drive/1esXEFN0eAOtJFcdIYwYOzaVkyFtEx5vE.pdf": ("Te Tiriti Entrenchment — Te Pāti Māori Policy Manifesto 2026 (Drive edition)", _drv("1esXEFN0eAOtJFcdIYwYOzaVkyFtEx5vE"), _D + " maoriparty.org.nz/te_tiriti_entrenchment (PDF created 2 Sep 2026)."),
    "drive/1CPy0C0flCQ71RKuSmtaD3CNsoShG7QAc.pdf": ("Energy Sovereignty — Te Pāti Māori Policy Manifesto 2026 (Drive edition)", _drv("1CPy0C0flCQ71RKuSmtaD3CNsoShG7QAc"), _D + " maoriparty.org.nz/energy_sovereignty (PDF created 21 Sep 2026)."),
    "drive/12XBSiuPt6KrpmxoHovpWOhfrB5ngTYkY.pdf": ("Mana Motuhake — Te Pāti Māori Policy Manifesto 2026", _drv("12XBSiuPt6KrpmxoHovpWOhfrB5ngTYkY"), _D + " maoriparty.org.nz/mana_motuhake (PDF created 18 May 2026)."),
    "drive/1CCbBwB6mcxNgPTDnycPkcgvVrUDY5ZmL.pdf": ("Military Neutrality — Te Pāti Māori Policy Manifesto 2026", _drv("1CCbBwB6mcxNgPTDnycPkcgvVrUDY5ZmL"), _D + " maoriparty.org.nz/military_neutrality (PDF created 18 May 2026)."),
    "drive/1FzavJoSYNEzsVWhnS9sBMI3XENAb9-Dr.pdf": ("Climate — Te Pāti Māori Policy Manifesto 2026", _drv("1FzavJoSYNEzsVWhnS9sBMI3XENAb9-Dr"), _D + " maoriparty.org.nz/climate (PDF created 18 May 2026)."),
    "drive/1Jc9cFUmV5YgkPg7tlKpojeiOSvXzJX1N.pdf": ("Toi Māori — Te Pāti Māori Policy Manifesto 2026", _drv("1Jc9cFUmV5YgkPg7tlKpojeiOSvXzJX1N"), _D + " maoriparty.org.nz/toi_maori (PDF created 18 May 2026)."),
    "drive/1LPTzVr2sdxSNdfLF2DFLikHqr2zaeuBP.pdf": ("Freshwater — Te Pāti Māori Policy Manifesto 2026", _drv("1LPTzVr2sdxSNdfLF2DFLikHqr2zaeuBP"), _D + " maoriparty.org.nz/freshwater_policy (PDF created 18 May 2026)."),
    "drive/1T8WiwxG9nIDnDEjyVujLZKvoNWp7i0Oh.pdf": ("Housing — Te Pāti Māori Policy Manifesto 2026", _drv("1T8WiwxG9nIDnDEjyVujLZKvoNWp7i0Oh"), _D + " maoriparty.org.nz/housing (PDF created 5 Oct 2026)."),
    "drive/1dIy46mwnEg7G0oG-2r8xC5b0Be2Poegs.pdf": ("Mokopuna Māori — Te Pāti Māori Policy Manifesto 2026", _drv("1dIy46mwnEg7G0oG-2r8xC5b0Be2Poegs"), _D + " maoriparty.org.nz/mokopuna_m_ori (PDF created 18 May 2026)."),
    "drive/1m8zZo4j-pzDqeQdFj_OcVTPjq6VgEHCh.pdf": ("Te Reo Māori — Te Pāti Māori Policy Manifesto 2026", _drv("1m8zZo4j-pzDqeQdFj_OcVTPjq6VgEHCh"), _D + " maoriparty.org.nz/te_reo_maori (PDF created 18 May 2026)."),
    "drive/1qyqzCxGrLF067Q2S5ZafwQ1F_UDOpPj0.pdf": ("Mana Takatāpui — Te Pāti Māori Policy Manifesto 2026", _drv("1qyqzCxGrLF067Q2S5ZafwQ1F_UDOpPj0"), _D + " maoriparty.org.nz/takat_pui (PDF created 21 Sep 2026)."),
    "drive/1IeJ-WmT2cwdeo6noqVaSRFk55dhQGpNl.pdf": ("Whānau Pakari – Sport and Wellbeing Policy (2020 document — NOT confirmed as 2026 policy)", _drv("1IeJ-WmT2cwdeo6noqVaSRFk55dhQGpNl"), "Google Drive file 'MP Sport Policy.pdf' linked from maoriparty.org.nz/maori_sports (page captured March 2026). PDF metadata: created 30 Aug 2020 — an earlier election's policy, included for reference only."),
    "drive/1V1fVe2hhe5eNDVBuJYmxu3_07igGSiyo.pdf": ("Mana Hauā (Disability) Policy (2023 document — NOT confirmed as 2026 policy)", _drv("1V1fVe2hhe5eNDVBuJYmxu3_07igGSiyo"), "Google Drive file linked from maoriparty.org.nz/mana_hau_policy (page captured April 2026). PDF metadata: created 25 Aug 2023 — the 2023 policy, included for reference only; the 2026 'Disabilities' page and the 2026 'What matters to you?' tool are the current texts."),
    "drive/1N9MFecQz4zJngdvZhP6HtqC6IjiP5bIz.pdf": ("Mokopuna Māori Policy (2023 document — superseded)", _drv("1N9MFecQz4zJngdvZhP6HtqC6IjiP5bIz"), "Google Drive file linked from a 2023 maoriparty.org.nz news page. PDF metadata: created 1 Aug 2023. Superseded by the 2026 Mokopuna Māori manifesto chapter; included for reference only."),
})

TOOL = "tool:what-matters-to-you"
def _add(M, k, docs, note=None):
    g, d, n = M[k]
    M[k] = (g, d + [x for x in docs if x not in d], n if note is None else note)
P_TAX, P_ENT, P_EN = "pdf:drive/11dbbk3BTNigHUb4xANPnTKxb2TC9dAgg.pdf", "pdf:drive/1esXEFN0eAOtJFcdIYwYOzaVkyFtEx5vE.pdf", "pdf:drive/1CPy0C0flCQ71RKuSmtaD3CNsoShG7QAc.pdf"
P_MM, P_MIL, P_CLI = "pdf:drive/12XBSiuPt6KrpmxoHovpWOhfrB5ngTYkY.pdf", "pdf:drive/1CCbBwB6mcxNgPTDnycPkcgvVrUDY5ZmL.pdf", "pdf:drive/1FzavJoSYNEzsVWhnS9sBMI3XENAb9-Dr.pdf"
P_TOI, P_FW, P_HOU = "pdf:drive/1Jc9cFUmV5YgkPg7tlKpojeiOSvXzJX1N.pdf", "pdf:drive/1LPTzVr2sdxSNdfLF2DFLikHqr2zaeuBP.pdf", "pdf:drive/1T8WiwxG9nIDnDEjyVujLZKvoNWp7i0Oh.pdf"
P_MOK, P_REO, P_TAK = "pdf:drive/1dIy46mwnEg7G0oG-2r8xC5b0Be2Poegs.pdf", "pdf:drive/1m8zZo4j-pzDqeQdFj_OcVTPjq6VgEHCh.pdf", "pdf:drive/1qyqzCxGrLF067Q2S5ZafwQ1F_UDOpPj0.pdf"
P_SPORT, P_HAUA = "pdf:drive/1IeJ-WmT2cwdeo6noqVaSRFk55dhQGpNl.pdf", "pdf:drive/1V1fVe2hhe5eNDVBuJYmxu3_07igGSiyo.pdf"
for k in ["POL54812", "POL54938", "POL54939", "POL54940", "POL54941", "POL54942", "POL54943", "POL54968"]: _add(TPM_MAP, k, [P_TAX, "cc:tax"])
for k in ["POL54917", "POL54919", "POL54795"]: _add(TPM_MAP, k, [P_ENT, "cc:te_tiriti_entrenchment"])
for k in ["POL55058", "POL55059", "POL55060", "POL55061", "POL55062", "POL55063", "POL55064"]: _add(TPM_MAP, k, [P_EN, "cc:energy_sovereignty"])
_add(TPM_MAP, "POL54921", [P_MM]); _add(TPM_MAP, "POL54647", [TOOL]); _add(TPM_MAP, "POL55001", [TOOL])
for k in ["POL54680", "POL54681", "POL54682"]: _add(TPM_MAP, k, [P_CLI, TOOL])
for k in ["POL54683", "POL54684", "POL54688", "POL54690"]: _add(TPM_MAP, k, [P_MIL])
for k in ["POL55000", "POL55067"]: _add(TPM_MAP, k, [P_MOK, TOOL])
_add(TPM_MAP, "POL55065", [P_REO, TOOL]); _add(TPM_MAP, "POL55066", [TOOL]); _add(TPM_MAP, "POL54679", ["cc:education_training", TOOL])
_add(TPM_MAP, "POL55068", ["cc:policy", "cc:maori_sports", TOOL],
     "policy.nz cites maoriparty.org.nz/sports, which Common Crawl did not capture; the party's policy index page (captured 8 Oct 2026) carries the same 'Sports' summary, and the party's 'What matters to you?' tool lists the Whānau Pakari sport fund.")
_add(TPM_MAP, "POL55070", [TOOL]); _add(TPM_MAP, "POL55071", [P_HOU, TOOL]); _add(TPM_MAP, "POL55072", [P_TOI, TOOL])
_add(TPM_MAP, "POL55085", [P_FW, TOOL]); _add(TPM_MAP, "POL55086", [P_TAK, TOOL]); _add(TPM_MAP, "POL55087", [TOOL]); _add(TPM_MAP, "POL55088", [TOOL])
_add(TPM_MAP, "POL54649", [TOOL]); _add(TPM_MAP, "POL54650", [TOOL])
for x in TPM_EXTRA:
    if x["id"] in ("TPM-A01",): x["docs"] += [P_TAX, P_HOU, TOOL]
    if x["id"] in ("TPM-A02",): x["docs"] += [P_TAX]
    if x["id"] in ("TPM-A03",): x["docs"] += [P_ENT]
    if x["id"] in ("TPM-A04",): x["docs"] += [P_MM]
    if x["id"] == "TPM-A05":
        x["docs"] += [P_MM, TOOL]
        x["statement"] = "Entrench the Māori electorates and require Māori wards in every council"
        x["how"] += " The 2026 Mana Motuhake chapter and the party's policy tool also commit to requiring Māori wards and mana whenua representation in all councils."
    if x["id"] == "TPM-A06":
        x["docs"] += [P_CLI, TOOL]
        x["how"] += " The Climate chapter separately commits $300 million to Mātai Ahuwhenua and a five-year phase-out of synthetic fertilisers; the party's policy tool states '$400 million to help Māori farmers move to regenerative farming'."
    if x["id"] in ("TPM-A08", "TPM-A09", "TPM-A10"): x["docs"] += [TOOL]
    if x["id"] == "TPM-A11":
        x["docs"] += [P_TOI, TOOL]
        x["how"] += " The Toi Māori chapter also commits $19 million baseline funding for Te Matatini, $10 million for community, hapū and iwi kapa haka, a $10 million Toi Māori research fund, and a living wage for employed and contracted artists."
    if x["id"] == "TPM-A12":
        x["docs"] += [P_TAK, TOOL]
        x["how"] += " The chapter also commits to updating the Human Rights Act for people of diverse genders, sexualities and sex characteristics."
    if x["id"] in ("TPM-A13", "TPM-A14", "TPM-A15"): x["docs"] += [TOOL]
    if x["id"] == "TPM-A16":
        x["docs"] += [P_HOU, TOOL]
        x["statement"] = "Freeze rents (then cap rises at inflation) and repeal no-cause evictions in the first 100 days"
        x["how"] = "The 2026 Housing chapter says the party would freeze all rents, then allow increases only by the rate of inflation each year unless the owner makes significant improvements, and repeal no-cause evictions within its first 100 days in government. Earlier releases described this as 'universal rent control'."
    if x["id"] == "TPM-A17":
        x["docs"] += [P_HOU, TOOL]
        x["how"] += " The 2026 Housing chapter sets the 2,000 papakāinga homes within four years and commits to stopping the discounted sale of state houses to private investors and increasing funding for Sustaining Tenancies."
    if x["id"] == "TPM-A18": x["docs"] += [P_HOU, P_MM]
    if x["id"] == "TPM-A19":
        x["docs"] += [P_CLI, TOOL]
        x["how"] += " The 2026 Climate chapter commits $100m to a 'Māori National Service Defence framework' giving hapū, iwi and urban Māori organisations the same access and resources as local government after natural disasters, and a $100m Māori Taiao relief fund to rebuild marae, urupā and papakāinga."
        x["note"] = "First made as a call on the government (April 2026); now part of the 2026 Climate chapter."

def _t(id_, group, statement, topics, why, how, docs, note=""):
    return _x(id_, group, statement, topics, why, how, docs, note)
TPM_EXTRA += [
    _t("TPM-A21", "Kai, cost of living & economy", "Lift the minimum wage to the living wage ($28.95 an hour) and end youth rates", ["wages-and-working-conditions", "incomes-and-employment"],
       "The party says no one should be paid less than what it costs to live.",
       "The party's policy tool (from its 2026 manifesto) says the minimum wage would go 'straight up to the living wage', $28.95 an hour, and that youth and starting-out rates would end.", [TOOL]),
    _t("TPM-A22", "Kai, cost of living & economy", "Double baseline benefits, remove sanctions and work-test obligations, cancel benefit debt", ["benefits", "tax-and-income-support"],
       "The party says welfare should not punish whānau for being poor.",
       "The party's policy tool lists doubling baseline benefits, removing sanctions and work-test obligations, cancelling benefit debt owed to the Crown, hardship grants that do not need to be repaid, and Special Needs Grants that cover cultural costs such as tangihanga and unveilings.", [TOOL, "cc:cost_of_living"]),
    _t("TPM-A23", "Kai, cost of living & economy", "Free public transport for tamariki, students and Community Services Card holders, then for everyone within five years", ["public-transport-cycling-and-walking", "prices"],
       "The party says transport costs are a major part of the cost of living.",
       "The party's policy tool says public transport would be free immediately for tamariki, students (including tertiary) and Community Services Card holders, half price for everyone else, and free for everyone within five years.", [TOOL, "cc:cost_of_living"]),
    _t("TPM-A24", "Housing", "Repeal interest deductibility for landlords and use the money for social housing and papakāinga", ["housing", "government-revenue-and-finance"],
       "The party says restoring interest deductibility gave landlords a $3 billion tax break and pushes home ownership out of reach.",
       "The 2026 Housing chapter says the party would repeal interest deductibility and redistribute the $3 billion to help fund its social housing and papakāinga policies.", [P_HOU]),
    _t("TPM-A25", "Housing", "Create 'Rangatahi Ora' and a legal duty on government to end youth homelessness", ["housing", "young-people", "social-and-public-housing"],
       "The party says half of homeless people are under 25 and agencies have no duty to prevent it.",
       "The 2026 Housing chapter would set up a new agency, Rangatahi Ora, with functions, duties and powers to prevent youth homelessness, and a legal 'duty to assist' requiring agencies to end or stabilise a young person's homelessness (building on Oriini Kaipara's member's bill).", [P_HOU, TOOL, "scoop:PA2602-S00141"]),
    _t("TPM-A26", "Health, disability & whānau", "End state care of mokopuna Māori and create a Mokopuna Māori Authority funded with ~70% of Oranga Tamariki's budget", ["family-justice-and-safety", "te-ao-maori", "community-and-inclusion"],
       "The party says state care removes Māori children from their whakapapa and causes harm.",
       "The 2026 Mokopuna Māori chapter commits to ending state care for mokopuna Māori, a Mokopuna Māori Act creating an independent authority, a three-year transition away from Oranga Tamariki with 70% of its budget (about $1 billion a year) reallocated, reinstating section 7AA, ending uplifts without whānau, hapū and iwi consent, closing youth care and protection residences, and implementing all 138 recommendations of the Royal Commission into Abuse in Care (Whanaketia).", [P_MOK, TOOL]),
    _t("TPM-A27", "Education & te reo Māori", "Write off the living-cost part of student loans and pay every student a doubled student allowance", ["tertiary-education", "education"],
       "The party says cost barriers block whānau from education and training.",
       "The party's policy tool says the living-cost component of every student loan would be written off (working towards full write-offs for people who live and work here for five years), and every student would get a student allowance at double the rate, with the parental income test scrapped and allowances restored for postgraduate, part-time and long-course students.", [TOOL]),
    _t("TPM-A28", "Education & te reo Māori", "Teachers' pay rises that keep up with inflation", ["schools", "wages-and-working-conditions"],
       "The party says the education workforce needs support on pay and workload.",
       "The party's policy tool lists pay rises for teachers that keep up with inflation, support for Māori teachers, kaiako and support staff, and action on pay inequity and workload; it also lists second-chance and adult education and kai-sovereignty scholarships and trades apprenticeships.", [TOOL]),
    _t("TPM-A29", "Health, disability & whānau", "Free GP visits and free dental care for all whānau", ["health-services", "health"],
       "The party says Māori die seven years earlier than non-Māori.",
       "The party's policy tool lists free primary healthcare and free dental care for all whānau, clinics on marae, mobile health units and free delivery of medication, protecting rongoā Māori and funding more medicines through Pharmac.", [TOOL, "cc:health"]),
    _t("TPM-A30", "Health, disability & whānau", "$500 million a year for kaupapa Māori mental health", ["mental-health", "health"],
       "The party says mental health services must be culturally safe and accountable to Māori.",
       "The party's policy tool lists $500 million a year for kaupapa Māori mental health, free community mental health services, and treating addiction as a health issue with double the funding for prevention, harm reduction and treatment.", [TOOL]),
    _t("TPM-A31", "Health, disability & whānau", "Start bowel screening at 45 for everyone and 35 for Māori and Pacific peoples", ["public-health", "health-services"],
       "The party says screening ages should reflect earlier onset among Māori and Pacific peoples.",
       "The party's policy tool lists earlier bowel screening: from age 45 for everyone and from 35 for Māori and Pacific peoples.", [TOOL]),
    _t("TPM-A32", "Health, disability & whānau", "Move a quarter of all health and ACC funding to Māori-led systems", ["health-funding-and-workforce", "te-ao-maori"],
       "The party says a health system that does not understand Māori will keep failing Māori.",
       "The party's policy tool states 'A quarter of all health and ACC funding moved to systems led by Māori.'", [TOOL, "cc:health"]),
    _t("TPM-A33", "Health, disability & whānau", "Establish a Māori-led Mana Hauā Authority for disabled whānau and recognise unpaid care as work", ["disability", "te-ao-maori"],
       "The party says disabled Māori should not have to fight a degrading system for support.",
       "The party's policy tool lists a Mana Hauā Authority led by Māori, support that keeps Tangata Hauā with their whānau, recognising unpaid care as real work, and aligning disability support with income so no one is forced into poverty. (The party's 2023 Mana Hauā policy, archived for reference, set out a fuller list.)", [TOOL, "cc:disabilities", "cc:mana_hau_policy", P_HAUA]),
    _t("TPM-A34", "Environment, climate & energy", "End new oil and gas exploration and withdraw existing permits within five years", ["emissions-reduction", "energy", "oceans"],
       "The party says whenua and moana must be protected from extractive industries.",
       "The 2026 Climate chapter commits to ending new oil and gas exploration, withdrawing existing on- and offshore permits within five years and decommissioning sites within ten, with planning and support for workers through a just transition.", [P_CLI, TOOL]),
    _t("TPM-A35", "Environment, climate & energy", "Repeal the Fast-track Approvals Act and end mining on conservation land", ["conservation", "land-and-resources", "urban-planning-and-resource-management"],
       "The party says fast-track consenting overrides mana whenua and the environment.",
       "The 2026 Climate chapter commits to repealing the Fast-track Approvals Act and retrospectively revoking all fast-tracked mining consents, and ending mining on conservation land including reserves and Significant Natural Areas.", [P_CLI, TOOL]),
    _t("TPM-A36", "Environment, climate & energy", "$1 billion Pūngao Auaha Fund for solar and insulation on marae, kura, papakāinga and homes", ["energy", "climate-adaptation", "housing"],
       "The party says Māori communities should benefit from the energy transition.",
       "The 2026 Climate chapter establishes a $1 billion Pūngao Auaha Fund to retrofit marae, kura, papakāinga and housing with solar and insulation, support Māori-led community energy and move Māori-owned businesses off coal and gas. (It is separate in the Climate chapter from the $1 billion Energy Sovereignty Fund in the Energy chapter; the documents do not say whether these overlap.)", [P_CLI, TOOL]),
    _t("TPM-A37", "Environment, climate & energy", "Guarantee safe, affordable drinking water and ban the trading of water rights", ["fresh-water-and-pollution", "infrastructure-funding-and-planning"],
       "The party says water is a taonga, not a market asset.",
       "The 2026 Freshwater chapter commits to safe, affordable drinking water for all whānau, investment in water infrastructure, rejecting privatisation and trading of water rights, enforceable limits to restore waterways, and funding iwi, hapū and marae water initiatives.", [P_FW, TOOL]),
    _t("TPM-A38", "Education & te reo Māori", "Make te reo Māori compulsory in education and require public agencies to work bilingually", ["te-reo-maori-and-culture", "schools", "public-sector"],
       "The party says te reo should be part of everyday life, not something you have to ask for.",
       "The 2026 Te Reo Māori chapter commits to compulsory te reo Māori in the education system with age-appropriate progression, bilingual public institutions, funding whānau-, marae-, hapū- and iwi-led reo initiatives, stronger Māori media and broadcasting, and protections against rollback of te reo commitments.", [P_REO, TOOL]),
    _t("TPM-A39", "Arts, culture, sport & takatāpui", "A $100 million Whānau Pakari sport fund and Māori teams competing as Aotearoa Māori", ["sports-and-recreation", "young-people", "te-ao-maori"],
       "The party says sport builds belonging, wellbeing and pathways for rangatahi.",
       "The party's 2026 policy tool lists 'A $100 million Whānau Pakari fund for sport' (Māori sports academies, scholarships, funding for Pā Wars) and 'Māori teams competing overseas as Aotearoa Māori'. The fuller Whānau Pakari policy document the site links to dates from 2020.", [TOOL, "cc:maori_sports", P_SPORT]),
    _t("TPM-A40", "Te Tiriti, constitution & democracy", "Land back: return the foreshore and seabed, conservation land and Crown and council land to mana whenua", ["land-and-resources", "te-tiriti-o-waitangi-and-governance"],
       "The party says mana motuhake requires the return of land and authority.",
       "The 2026 Mana Motuhake chapter commits to returning the foreshore and seabed, all conservation land and all central and local government land to mana whenua, a first right of refusal for mana whenua on all private land sales, ending perpetual leases, and ending foreign freehold land sales (leasehold only).", [P_MM, TOOL, "cc:mana_motuhake"]),
    _t("TPM-A41", "Te Tiriti, constitution & democracy", "Establish a Māori Parliament", ["parliament-and-democracy", "te-ao-maori"],
       "The party says Māori political authority must be restored.",
       "The 2026 Mana Motuhake chapter (Stage 3) commits to establishing a Māori Parliament holding authority over Māori programmes, funding streams and governance structures accountable to Māori.", [P_MM]),
    _t("TPM-A42", "Te Tiriti, constitution & democracy", "Remove the British monarch as head of state and make Aotearoa the official name", ["parliament-and-democracy", "te-reo-maori-and-culture"],
       "The party frames these as part of Te Tiriti-based constitutional transformation.",
       "The 2026 Mana Motuhake chapter (Stage 3) lists removing the British Royal Family as Head of State and recognising Aotearoa as the country's official name.", [P_MM]),
    _t("TPM-A43", "Te Tiriti, constitution & democracy", "Reform Treaty settlements: end 'full and final' and 'large natural groupings' policies, add relativity clauses", ["te-tiriti-o-waitangi-and-governance"],
       "The party says the settlement framework must be durable, just and recognise hapū-level authority.",
       "The 2026 Mana Motuhake chapter commits to abolishing 'full and final' and 'large natural groupings' settlement policies and inserting retrospective relativity clauses into all Te Tiriti settlements.", [P_MM]),
    _t("TPM-A44", "Kai, cost of living & economy", "A quarter of government contracts for Māori businesses and a $4.5 billion Oranga Whenua Oranga Tangata Fund", ["economic-development-and-industry", "business-support", "te-ao-maori"],
       "The party says Māori prosperity needs Māori-led institutions and funds.",
       "The party's policy tool says a quarter of all government spending on contracts would go to businesses fully owned and governed by Māori, plus a $4.5 billion Oranga Whenua Oranga Tangata Fund for Māori land, marae and business.", [TOOL, "cc:economic_development"]),
    _t("TPM-A45", "Te Tiriti, constitution & democracy", "Lower the voting age to 16 and allow switching between Māori and general rolls at any time", ["parliament-and-democracy"],
       "The party says electoral law should not exclude Māori and young people.",
       "The party's policy tool and Justice chapter list lowering the voting age to 16, enrolment at any time, switching between the Māori and general rolls at any time, and restoring voting rights to people in prison.", [TOOL, "pdf:justice-drive-1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx.pdf"]),
    _t("TPM-A46", "Kai, cost of living & economy", "Protect the right to sell homegrown and homekill kai locally", ["agriculture", "prices"],
       "The party says communities should be able to feed each other.",
       "The party's policy tool lists 'The right to sell homegrown and homekill kai locally', including roadside kai, 'without interference or tax', and more land set aside for rural and urban food farms.", [TOOL, "cc:kai_sovereignt"]),
]
for k in ["POL54684"]:
    _add(TPM_MAP, k, [TOOL])

# ---- NZ First: CC policy pages for existing items, and members' bills listed on nzfirst.nz
for k, d in {"POL54664": ["cc:the_kiwisaver_generation_and_bnz_buy_back"], "POL54663": ["cc:the_kiwisaver_generation_and_bnz_buy_back"],
             "POL54757": ["cc:maori_seats_referendum_bill"], "POL54668": ["cc:local_government_auckland_council_disestablishment_of_imsb_amendment_bill"],
             "POL55234": ["cc:the_fireworks_prohibition_legislation_bill", "pdf:Fireworks_Prohibition_Legislation_Bill.pdf"],
             "POL54754": ["cc:use_it_or_lose_it_dairy_policy"], "POL54961": ["cc:nz_super_for_citizens_only"],
             "POL55157": ["cc:ending_the_waitangi_makework_industry"]}.items():
    _add(NZF_MAP, k, d)
for k in ["POL54962", "POL54963", "POL54964", "POL54965", "POL54966", "POL54967"]: _add(NZF_MAP, k, ["cc:immigration_reform_policies"])
for k in ["POL55057", "POL55073", "POL55076", "POL55077", "POL55078"]: _add(NZF_MAP, k, ["cc:the_plan_to_make_nz_healthy"])
for x in NZF_EXTRA:
    if x["id"] == "NZF-A01":
        x["docs"] = ["cc:the_100bn_new_zealand_future_fund"] + x["docs"]
        x["note"] = "The party's policy page for the Future Fund was retrieved via Common Crawl (captured 7 Sep 2026)."
        x["how"] = ("This party would establish a 'New Zealand Future Fund' of up to $100 billion to invest solely in a multi-decade infrastructure build, ring-fenced from politicians, on a model similar to Singapore's Temasek. "
                    "Its policy page says the fund would be built by attracting international investment through 'taxation incentivisation'. The party says it would fund promised projects (for example the Hope Bypass).")
    if x["id"] == "NZF-A02": x["docs"] = ["cc:future_proofing_our_fuel_security"] + x["docs"]
    if x["id"] == "NZF-A03": x["docs"] = ["cc:withdraw_from_paris_accord"] + x["docs"]
    if x["id"] == "NZF-A24": x["docs"] += ["cc:the_container_return_scheme_bill", "pdf:Container_Return_Scheme_Bill-v1.5_1.pdf"]
    if x["id"] == "NZF-A26": x["docs"] += ["cc:nz_first_lodges_differing_view_on_the_gene_tech_bill"]
    if x["id"] == "NZF-A27": x["docs"] += ["cc:preventing_payment_scams_bill"]
    if x["id"] == "NZF-A28": x["docs"] += ["cc:the_accessibility_standards_bill"]
_MB = "Members' bills on the party's books"
NZF_EXTRA += [
    _x("NZF-A31", _MB, "Free, structured prostate cancer screening for at-risk men (member's bill)", ["health", "public-health"],
       "The party lists this among its current members' bills.",
       "The Health (Prostate Cancer Screening Services) Amendment Bill (Sept 2025) 'will provide free, structured screening for at-risk men, using PSA testing, MRI scans, and targeted biopsies where needed.'", ["cc:prostate_cancer_screening_bill", "cc:our-members-bills"]),
    _x("NZF-A32", _MB, "Require organisations to accept physical ID, not only digital ID (member's bill)", ["internet-and-digital-technologies", "civil-justice"],
       "The party says physical identification must remain a valid and equal alternative to digital ID.",
       "The Identification (Protection of Physical Identification Methods) Bill (Sept 2025) would require organisations to accept passports, driver licences, 18+ cards, school IDs and other prescribed physical documents whenever proof of age or identity is required.", ["cc:nz_first_introduces_bill_to_protect_against_digital_id_overreach", "cc:our-members-bills"]),
    _x("NZF-A33", _MB, "Legislate 'New Zealand' as the country's official name (member's bill)", ["parliament-and-democracy", "arts-culture-and-heritage"],
       "The party says officials have been changing the country's name 'by stealth'.",
       "The New Zealand (Name of State) Bill (Aug 2025) would state in law that 'New Zealand' is the official geographic name of the country.", ["cc:nzf_bill_legislating_nzs_name", "cc:our-members-bills"],
       "Contrast: Te Pāti Māori's Mana Motuhake chapter proposes recognising 'Aotearoa' as the official name."),
    _x("NZF-A34", _MB, "Protect the right to pay with cash (member's bill)", ["economy", "prices"],
       "The party says cash must remain a private, accessible and reliable way to pay.",
       "The Cash Transactions Protection Bill (July 2025) would provide for the enduring use of cash as a method of payment.", ["cc:cash_transactions_protection_bill", "cc:our-members-bills"]),
    _x("NZF-A35", _MB, "Define 'woman' and 'man' biologically in law (member's bill)", ["civil-justice", "community-and-inclusion"],
       "The party says the law needs clarity and consistency.",
       "The Legislation (Definitions of Woman and Man) Amendment Bill (April 2025) would define 'woman' as 'an adult human biological female' and 'man' as 'an adult human biological male' in the Legislation Act 2019.", ["cc:definitions-woman-man-bill"]),
    _x("NZF-A36", _MB, "Repeal diversity and inclusion requirements in the public service (member's bill)", ["public-sector"],
       "The party says public service employment should be based on merit, not DEI targets.",
       "The Public Service (Repeal of Diversity and Inclusiveness Requirements) Amendment Bill (March 2025) would remove those requirements from the Public Service Act.", ["cc:repeal-of-dei-requirements-bill"]),
    _x("NZF-A37", _MB, "Make English an official language of New Zealand (member's bill)", ["arts-culture-and-heritage", "parliament-and-democracy"],
       "The party says the law should be clear about the official status of English.",
       "NZ First's English Language Bill, which would make English an official language, passed its first reading in March 2026.", ["cc:english-language-bill-passes-first-reading"]),
    _x("NZF-A38", _MB, "Require national referendums before conscience-vote issues become law (member's bill)", ["parliament-and-democracy"],
       "The party says conscience issues should be decided by the people, not MPs' conscience votes.",
       "The Conscience Acts Referendums Bill (March 2025) would require a mandatory national referendum before any conscience issue is passed into law.", ["cc:conscience-referendums-bill"]),
    _x("NZF-A39", _MB, "Return fluoridation decisions to local communities by referendum (member's bill)", ["public-health", "local-government"],
       "The party says fluoridation decisions were centralised without community say.",
       "The Fluoridation (Referendum) Legislation Bill (Feb 2025) would repeal the Health (Fluoridation of Drinking Water) Amendment Act 2021 and restore local decision-making through referendums.", ["cc:fluoridation-referendum-bill"]),
    _x("NZF-A40", _MB, "Only the official New Zealand flag on government buildings (member's bill)", ["public-sector", "arts-culture-and-heritage"],
       "The party says government premises should display only the national flag.",
       "The Display of Flags (Government Premises) Bill (July 2025) would make it law that government buildings can only display the official flag of New Zealand.", ["cc:display_of_flags_government_premises_bill"]),
]
