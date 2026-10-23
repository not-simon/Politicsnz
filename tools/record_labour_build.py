#!/usr/bin/env python3
"""Build data/promises/labour.json (Labour Party promise tracker) and print the
reliability scorecard used in parties/labour/track-record.md.

Each entry follows docs/SCHEMA.md (promise, made, category, status, detail, sources)
plus three optional helper fields:
  id      short stable identifier
  term    which period the promise is judged against
  scored  True if the promise was testable in office (Labour in government) and is
          counted in the reliability scorecard. Opposition-era promises (2011, 2014,
          2023 after defeat) and 2026 promises are recorded but not scored.
Research notes: compiled 23 Oct 2026 from independent news coverage, official
documents and Wikipedia (for legislative dates). See sources on each entry.
"""
import json, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
T1 = "2017-2020 (Labour-NZ First coalition, Green confidence & supply)"
T2 = "2020-2023 (Labour majority, Green cooperation agreement)"
OPP1 = "Opposition 2008-2017 (not in government)"
OPP2 = "Opposition 2023-2026 (lost office)"
NEXT = "2026 election platform"

P = []
def add(id, promise, made, category, status, detail, sources, term, scored=True):
    P.append({"id": id, "promise": promise, "made": made, "category": category,
              "status": status, "detail": detail, "sources": sources,
              "term": term, "scored": scored})

# ---------------- Opposition era 2011 / 2014 (not testable in office) ----------------
add("2011-cgt", "Introduce a capital gains tax (excluding the family home)", "2011 election (Goff)", "tax",
    "abandoned",
    "Labour campaigned on a CGT in 2011 and again in 2014 but lost both elections. Andrew Little's leadership dropped it "
    "(confirmed at the 2015 conference); Ardern revived it via the Tax Working Group in 2017-19 then ruled it out (2019); "
    "Hipkins ruled it out in 2023, then Labour adopted a narrower property CGT for 2026.",
    ["https://www.interest.co.nz/news/54387/election-2011-party-policies-tax",
     "https://www.odt.co.nz/node/362358"], OPP1, False)
add("2011-super67", "Raise the NZ Superannuation eligibility age from 65 to 67 (phased 2020-2033)", "2011 and 2014 elections", "retirement",
    "abandoned",
    "A signature 'responsible' policy under Goff and Cunliffe. Little dropped it after taking over in 2014 and said in 2017 the age would not rise "
    "'while I'm leader'. Labour in government (2017-23) kept the age at 65 and resumed Super Fund contributions.",
    ["https://www.interest.co.nz/news/54392/election-2011-party-policies-tax-kiwisaver",
     "https://www.odt.co.nz/node/362358",
     "https://www.newshub.co.nz/home/politics/2017/03/labour-probably-won-t-raise-taxes-andrew-little.html"], OPP1, False)
add("2011-gst-fv", "Remove GST from fresh fruit and vegetables", "2011 election (Goff)", "tax",
    "abandoned",
    "Dropped under David Cunliffe (along with the $5,000 tax-free threshold) before 2014. The same idea was revived by Hipkins in 2023 (see 2023 entry).",
    ["https://www.odt.co.nz/node/288951"], OPP1, False)
add("2011-kiwisaver", "Make KiwiSaver compulsory, with employer contributions rising to 7%", "2011 election (Goff)", "retirement",
    "abandoned",
    "Not carried into the 2017 platform or enacted 2017-23. In 2026 Labour again proposes compulsory employer contributions and a higher minimum contribution (see 2026 entries).",
    ["https://www.interest.co.nz/news/54392/election-2011-party-policies-tax-kiwisaver"], OPP1, False)
add("2014-nzpower", "Create 'NZ Power', a single buyer of wholesale electricity (joint Labour-Green policy)", "2014 election (Cunliffe)", "energy",
    "abandoned", "Shelved by Andrew Little after the 2014 defeat; never revived.",
    ["https://www.interest.co.nz/news/78527/labour-says-wont-introduce-capital-gains-tax-first-term-shelves-nz-power-plan-twyford"], OPP1, False)
add("2014-kiwiassure", "Set up KiwiAssure, a state-owned general insurer alongside Kiwibank", "2014 election (announced late 2013)", "economy",
    "abandoned", "Put under review by Little in 2015; not in the 2017 platform and never established.",
    ["https://www.interest.co.nz/news/71102/election-2014-party-policies-insurance",
     "https://www.interest.co.nz/news/73751/little-re-consider-labours-plan-establish-new-state-owned-insurer-kiwiassure"], OPP1, False)
add("2014-36pc", "Raise the top income tax rate to 36 cents for income over $150,000", "2014 election (Cunliffe)", "tax",
    "abandoned", "Dropped after 2014; Little said in 2017 Labour had no plans to raise income taxes. Labour later introduced a 39% rate on income over $180,000 in 2021 (see 2020 entry).",
    ["https://www.odt.co.nz/news/politics/labour-surplus-bid-relies-tax-rises",
     "https://www.newshub.co.nz/home/politics/2017/03/labour-probably-won-t-raise-taxes-andrew-little.html"], OPP1, False)

# ---------------- 2017 election, 100-day plan and coalition agreements ----------------
add("2017-100day", "Deliver the 100-day plan (fees-free year, Healthy Homes, foreign-buyer ban, Families Package, stop state-house sales, child poverty bill, mental health inquiry, Tax Working Group, Pike River agency, etc.)",
    "2017 election", "general", "kept",
    "RNZ's and 1News' tracking concluded the list was largely ticked off by early February 2018. Several items were 'delivered' by introducing a bill or starting an inquiry rather than finishing it (e.g. the child poverty bill, the employment-law changes). One item was swapped after coalition talks.",
    ["https://www.newshub.co.nz/home/election/2017/09/labour-announces-top-priorities-if-elected.html",
     "https://www.newshub.co.nz/home/election/2017/10/jacinda-ardern-commits-to-100-day-plan-with-one-exception.html",
     "https://www.1news.co.nz/2017/12/12/halfway-point-in-governments-100-day-plan-sees-pm-pleased-with-progress/",
     "https://newstalkzb.co.nz/news/politics/govt-100-day-plan-whats-left-on-the-to-do-list"], T1)
add("2017-feesfree1", "First year of tertiary study or training fees-free from 1 January 2018", "2017 election (100-day plan)", "education",
    "kept",
    "Delivered on time. An AUT study using Stats NZ data on 250,000+ school leavers found no clear increase in tertiary participation after allowing for prior trends. The coalition government converted it to final-year fees-free from 2025.",
    ["https://en.wikipedia.org/wiki/Sixth_Labour_Government_of_New_Zealand",
     "https://www.aut.ac.nz/news/stories/did-fees-free-help-widen-access-to-uni"], T1)
add("2017-feesfree3", "Extend fees-free tertiary education to three years by 2024", "2017 election", "education",
    "abandoned",
    "In September 2020 Chris Hipkins (Education Minister) announced Labour would not extend fees-free beyond the first year, redirecting money to free apprenticeships/targeted vocational training. Students' associations called it a broken promise.",
    ["https://www.timeshighereducation.com/cn/news/no-extension-new-zealands-fee-free-scheme",
     "https://newshub.co.nz/home/politics/2020/10/nz-election-2020-jacinda-ardern-gets-hero-s-welcome-from-students-but-disappointment-over-broken-fees-free-promise.html"], T1)
add("2017-allowance", "Raise student allowances and living-cost loans by $50 a week", "2017 election (100-day plan)", "education",
    "kept", "Took effect 1 January 2018.",
    ["https://en.wikipedia.org/wiki/Sixth_Labour_Government_of_New_Zealand"], T1)
add("2017-healthyhomes", "Pass the Healthy Homes Guarantee Bill so all rentals are warm and dry", "2017 election (100-day plan)", "housing",
    "kept",
    "Healthy Homes Guarantee Act passed December 2017; standards set 2019. Compliance deadlines were later pushed out (private landlords: from 1 July 2024 to 1 July 2025; Kāinga Ora from 2023 to 2024) by Labour itself in 2022.",
    ["https://en.wikipedia.org/wiki/Healthy_Homes_Guarantee_Act_2017",
     "https://www.hud.govt.nz/news/changes-to-the-healthy-homes-standards-compliance-timeframes",
     "https://www.1news.co.nz/2022/11/22/govt-confirms-extension-to-healthy-homes-standards-deadline"], T1)
add("2017-foreignbuyers", "Ban overseas speculators from buying existing homes", "2017 election (100-day plan)", "housing",
    "kept",
    "Overseas Investment Amendment Act passed 15 August 2018 (65-57), in force 22 October 2018. Australians and Singaporeans exempt because of trade agreements. The 2023-26 coalition kept the ban but in 2025 created an exemption for Active Investor Plus visa holders buying homes worth $5m+.",
    ["https://www.lawsociety.org.nz/news/newsroom/ban-on-most-foreign-buyers-of-existing-homes-passed/",
     "https://www.aljazeera.com/amp/economy/2018/8/15/new-zealand-rolls-out-ban-on-foreign-national-property-purchases",
     "https://www.oneroof.co.nz/news/nzs-top-agents-surprised-as-foreign-buyer-ban-quietly-reversed-48757"], T1)
add("2017-statehouses", "Stop the sale of state houses and build more public housing (1,000+ state houses a year)", "2016-17 (Little/Ardern)", "housing",
    "kept",
    "State-house sales stopped. Labour reported a net increase of 10,037 public homes Oct 2017-June 2022 (8,240 new builds) and claimed 13,000+ by 2023, 'the most since the 1950s'. Critics (National; Newshub explainer) note many 'places' were purchases/leases and a ~5,000-home pipeline was inherited; AAP FactCheck found both parties can claim some credit.",
    ["https://www.newshub.co.nz/home/new-zealand/2016/07/labour-promises-1000-state-houses-a-year-until-demand-met.html",
     "https://newshub.co.nz/home/politics/2021/07/explainer-is-labour-fudging-state-house-numbers.html",
     "https://www.aap.com.au/factcheck/labour-and-national-both-claim-credit-for-nz-public-housing-rise/"], T1)
add("2017-kiwibuild", "KiwiBuild: build 100,000 affordable homes over 10 years", "2017 election", "housing",
    "broken",
    "Interim targets missed badly (1,000 homes by June 2019 was cut to 300; ~258 built by mid-2019; 452 by June 2020). In the September 2019 'reset' Megan Woods scrapped the 100,000 target altogether. Kāinga Ora reported 2,335 KiwiBuild homes completed between July 2018 and 29 February 2024, plus 1,238 contracted.",
    ["https://thespinoff.co.nz/politics/04-09-2019/cheat-sheet-megan-woods-hits-reset-on-the-beleaguered-kiwibuild-programme/",
     "https://www.newsroom.co.nz/2019/09/04/789917/government-introduces-major-kiwibuild-overhaul",
     "https://www.kaingaora.govt.nz/assets/Publications/OIAs-Official-Information-Requests/April-2024/9-April-2024-Breakdown-of-KiwiBuild-homes-by-Region-and-Price1.pdf",
     "https://www.wgtn.ac.nz/igps/commentaries/1769734-broken-kiwibuild-promises-deserve-an-election-loss"], T1)
add("2017-kiwibuild-yr1", "KiwiBuild: 1,000 homes in the first year (to June 2019)", "2017-18 (KiwiBuild targets)", "housing",
    "broken", "Target cut to 300 in January 2019, then all interim targets dropped by May 2019. 2019 had been branded the 'Year of Delivery'.",
    ["https://www.newsroom.co.nz/2019/01/29/419945/kiwibuild-under-microscope-after-target-shortfall",
     "https://newshub.co.nz/home/politics/2019/05/kiwibuild-s-final-target-has-been-dropped.html",
     "https://www.newshub.co.nz/home/politics/2019/07/year-of-delivery-political-party-leaders-judge-the-government-s-progress.html"], T1)
add("2017-lightrail", "Light rail from Auckland CBD to Mt Roskill within four years and to the airport within ten", "2017 election", "transport",
    "broken",
    "No track was laid. The process switched between NZTA, an unsolicited NZ Infra (NZ Super Fund/CDPQ) bid and a light-metro option; NZ First blocked a decision in 2020. In January 2022 Labour (now governing alone) endorsed a $14.6b tunnelled line; the National-led government cancelled it in January 2024, citing $228m spent (figure disputed by Labour's Michael Wood).",
    ["https://www.newshub.co.nz/home/election/2017/08/labour-promises-light-rail-to-auckland-airport-within-a-decade.html",
     "https://en.wikipedia.org/wiki/City_Centre%E2%80%93M%C4%81ngere_Line",
     "https://www.1news.co.nz/2024/01/14/government-officially-cancels-auckland-light-rail/",
     "https://www.newstalkzb.co.nz/news/national/former-transport-minister-michael-wood-lashes-out-at-national-for-scrapping-auckland-light-rail/"], T1)
add("2017-migration", "Reduce net migration by 20,000-30,000 a year", "2017 election", "immigration",
    "broken",
    "No cut was made before COVID: net migration reached a record ~91,700 gain in the year to early 2020. The later drop was caused by COVID border closures, not the 2017 policy. By 2022 ministers declined to restate the numerical goal.",
    ["https://www.newsroom.co.nz/2017/10/19/54611/big-policy-changes-ahead-for-labour-led-government",
     "https://newshub.co.nz/home/politics/2022/05/kris-faafoi-skirts-around-answering-whether-government-is-still-planning-to-cut-migration-as-promised-by-former-labour-leader.html",
     "https://en.wikipedia.org/wiki/Sixth_Labour_Government_of_New_Zealand"], T1)
add("2017-families", "Families Package: Best Start payment, Winter Energy Payment, higher Working for Families and Accommodation Supplement (funded by cancelling National's tax cuts)", "2017 election (100-day plan)", "welfare",
    "kept", "Legislated December 2017, in force 1 July 2018; projected to lift 88,000 children out of poverty by 2020/21.",
    ["https://www.beehive.govt.nz/sites/default/files/2017-12/Families%20Package%20Factsheet.pdf",
     "https://www.newshub.co.nz/home/politics/2017/12/labour-introduces-major-5b-plan-to-halve-child-poverty.html"], T1)
add("2017-ppl", "Extend paid parental leave to 26 weeks by 2020", "2017 election (100-day plan)", "welfare",
    "kept", "22 weeks from 1 July 2018 and 26 weeks from 1 July 2020, as scheduled.",
    ["https://www.hawkerbritton.com/wp-content/uploads/2017/11/NZ-Labour-announce-26-weeks-paid-parental-leave.pdf",
     "https://www.msd.govt.nz/documents/about-msd-and-our-work/publications-resources/evaluation/families-package-reports/the-families-package-and-2020-2022-income-support-reforms.pdf"], T1)
add("2017-childpoverty", "Legislate child poverty reduction targets and (Ardern) halve child poverty within 10 years", "2017 election", "welfare",
    "partially-kept",
    "Child Poverty Reduction Act 2018 passed with near-unanimous support. Of the first three-year targets (2020/21) two of three were met (after-housing-costs low income and material hardship); the before-housing-costs target was missed. Material hardship then rose from 10.5% (2021/22) to 12.5% (2022/23) amid high inflation, and the Auditor-General reported none of the 2023/24 targets were met. 10-year targets (2027/28) remain unmet on current Treasury modelling.",
    ["https://msd.govt.nz/about-msd-and-our-work/child-wellbeing-and-poverty-reduction/progress-targets.html",
     "https://2023.budget.govt.nz/budget/2023/wellbeing/child-poverty-report/poverty-reduced.htm",
     "https://www.oag.parliament.nz/2025/child-poverty/part1.htm"], T1)
add("2017-mentalhealth", "Hold a mental health inquiry and act on it (Budget 2019 $1.9b mental wellbeing package)", "2017 election (100-day plan); Budget 2019", "health",
    "partially-kept",
    "Inquiry (He Ara Oranga) held 2018; $1.9b committed 2019-2023; Mental Health Commission re-established. Primary-care services (Access and Choice) expanded, but a 2021 government mid-term review found weak accountability and the Ministry of Health did not see itself as leading the programme; in 2022 advocates said little had changed for many people and specialist services were unchanged in five years.",
    ["https://www.dpmc.govt.nz/sites/default/files/2021-09/report-mid-term-review-2019-mental-health-sep21.pdf",
     "https://newshub.co.nz/home/politics/2021/09/andrew-little-admits-ministry-of-health-struggled-to-deliver-on-mental-health-as-review-finds-lack-of-accountability.html",
     "https://1news.co.nz/2022/04/19/mental-health-advocate-not-much-improvement-despite-19b"], T1)
add("2017-notax", "No new taxes before the 2020 election (Tax Working Group changes only from 2021) other than those specified", "2017 election (Ardern's 14 Sept 2017 reversal)", "tax",
    "kept",
    "After National's 'tax' attacks Ardern announced a week before the election that any Tax Working Group changes would not take effect until after 2020. No new broad taxes were introduced 2017-20; specified measures (regional fuel tax, fuel excise rises, bright-line extension to 5 years) went ahead.",
    ["https://www.newsroom.co.nz/2017/09/14/47849/labour-hits-pause-at-2359-on-doomsday-clock",
     "https://www.newshub.co.nz/home/election/2017/09/poll-voters-think-jacinda-ardern-right-to-hold-off-on-taxes.html",
     "https://www.newsroom.co.nz/2018/09/10/230505/capital-gains-tax-looks-less-likely"], T1)
add("2017-twg-cgt", "Use the Tax Working Group to make the system 'fairer', including a possible capital gains tax", "2017 election", "tax",
    "abandoned",
    "The TWG (chaired by Sir Michael Cullen) recommended a broad CGT in February 2019. On 17 April 2019 Ardern ruled it out, citing no consensus in the coalition (NZ First opposed) and no mandate, and said she would not revisit it as leader - while saying she still believed in it.",
    ["https://www.newshub.co.nz/home/politics/2019/04/government-rules-out-capital-gains-tax.html",
     "https://www.newshub.co.nz/home/politics/2019/06/jacinda-ardern-still-wants-a-capital-gains-tax-despite-ruling-it-out-forever.html",
     "https://en.wikipedia.org/wiki/Tax_Working_Group"], T1)
add("2017-watertax", "Charge commercial users (including irrigators) a royalty for water", "2017 election", "environment",
    "abandoned", "Dropped in coalition talks with NZ First in October 2017 - Ardern said it was the one concession Labour made. A narrower bottled-water export royalty was put in the agreement.",
    ["https://newshub.co.nz/home/politics/2017/10/nz-first-made-us-can-the-water-tax-jacinda-ardern.html"], T1)
add("2017-minwage", "Raise the minimum wage to $20 an hour by 2021", "2017 election and coalition agreement; reaffirmed 2020", "work",
    "kept", "$16.50 (2018), $17.70 (2019), $18.90 (2020), $20.00 from 1 April 2021. Hipkins later lifted it to $22.70 (April 2023).",
    ["https://newshub.co.nz/home/politics/2020/12/government-confirms-2021-minimum-wage-hike.html",
     "https://www.mbie.govt.nz/assets/minimum-wage-2021-cabinet-paper-redacted.pdf"], T1)
add("2017-90day", "Abolish 90-day trial periods", "2017 election", "work",
    "partially-kept", "Compromise with NZ First: trials kept for firms with fewer than 20 employees and removed for larger firms.",
    ["https://en.wikipedia.org/wiki/Sixth_Labour_Government_of_New_Zealand"], T1)
add("2017-pike", "Re-enter the Pike River mine drift and recover remains/evidence where practicable", "2017 election (Andrew Little; 100-day plan agency)", "justice",
    "partially-kept",
    "Pike River Recovery Agency re-entered and explored the 2.2-2.4km drift; work was completed and the drift sealed in December 2021, with the agency disestablished July 2022. No remains were recovered and the mine workings were not entered; costs roughly doubled to over $50m. Winston Peters later alleged the government broke its word; Little said it delivered what was promised.",
    ["https://mbie.govt.nz/dmsdocument/25361-pike-river-recovery-agency-final-annual-report-2022",
     "https://www.odt.co.nz/regions/west-coast/pike-river-mine-tunnel-re-entry-cost-doubles-over-50m",
     "https://newshub.co.nz/home/shows/2021/08/winston-peters-alleges-govt-broke-its-word-on-pike-re-entry-is-taking-fight-to-court.html"], T1)
add("2017-police1800", "Add 1,800 new police officers over three years (NZ First coalition agreement)", "2017 coalition agreement", "justice",
    "partially-kept",
    "Government declared the target met in November 2019 (1,825 graduates deployed since October 2017) after redefining it as 1,800 graduates rather than 1,800 over attrition; the net increase in police staff was about 1,000.",
    ["https://www.1news.co.nz/2019/11/21/government-celebrates-hitting-target-of-1800-new-cops-but-not-all-are-convinced/",
     "https://www.newshub.co.nz/home/politics/2019/10/confusion-over-government-s-1800-new-police-target.html"], T1)
add("2017-trees", "Plant one billion trees over ten years (NZ First coalition agreement)", "2017 coalition agreement", "environment",
    "partially-kept",
    "The count includes commercial replanting; an MPI Cabinet paper estimated the programme itself would contribute less than a third. The dedicated One Billion Trees Fund closed in June 2021 having directly funded ~48 million trees. The NZ Conservation Authority warned in 2020 natives were ~12% of plantings against a two-thirds Cabinet target. No independent, audited tally of progress toward the billion was found.",
    ["https://mpi.govt.nz/dmsdocument/49315/direct",
     "https://www.doc.govt.nz/about-us/statutory-and-advisory-bodies/nz-conservation-authority/advice-to-the-minister-and-or-director-general/advice-on-the-one-billion-trees-programme/",
     "https://en.wikipedia.org/wiki/One_billion_trees_planting_program"], T1)
add("2017-pgf", "$1 billion a year Provincial Growth Fund (NZ First coalition agreement)", "2017 coalition agreement", "economy",
    "kept",
    "Around $3b allocated over the term. Job-creation claims were contested (1News 2019 analysis; the Auditor-General questioned job calculations in 2020); a later review credited ~8,400 jobs.",
    ["https://www.1news.co.nz/2019/05/08/jobs-created-by-provincial-growth-fund-may-not-be-quite-what-they-seem",
     "https://www.newstalkzb.co.nz/on-air/heather-du-plessis-allan-drive/audio/john-ryan-and-shane-jones-on-auditor-general-report-into-pgf"], T1)
add("2017-zerocarbon", "Pass a Zero Carbon Act with an independent Climate Change Commission (Green C&S agreement)", "2017 election / Green agreement", "environment",
    "kept", "Passed 7 November 2019 with National's support at third reading; Climate Change Commission established.",
    ["https://newshub.co.nz/home/politics/2019/11/jacinda-ardern-praises-government-s-united-front-in-passionate-speech-after-zero-carbon-bill-passes.html",
     "https://en.wikipedia.org/wiki/Climate_Change_Response_(Zero_Carbon)_Amendment_Act_2019"], T1)
add("2017-oilgas", "No new offshore oil and gas exploration permits", "Announced April 2018 (in government)", "environment",
    "kept",
    "Not a 2017 manifesto line; announced in April 2018 and legislated (Crown Minerals (Petroleum) Amendment Act 2018). Existing permits unaffected. Reversed by the National-led government's Crown Minerals Amendment Act 2025 (in force August 2025).",
    ["https://www.iea.org/policies/19185-crown-minerals-petroleum-amendment-act-2018",
     "https://en.wikipedia.org/wiki/Crown_Minerals_Amendment_Act_2025"], T1)
add("2017-rivers", "Make rivers and lakes swimmable within a generation", "2017 election", "environment",
    "partially-kept",
    "Essential Freshwater package (2020) set new national standards, but the swimmability goal had no statutory deadline and a 2020 Herald assessment graded it D for ambition. Parts were later wound back by the 2023-26 government.",
    ["https://www.sciencemediacentre.co.nz/wp-content/upload/2017/09/SMC-Election-2017-QA.pdf",
     "https://www.pressreader.com/new-zealand/the-new-zealand-herald/20200602/281947430068439"], T1)
add("2017-gp", "Cheaper doctors' visits; free GP visits for under-14s", "2017 election", "health",
    "kept", "Free under-14 visits and lower fees for Community Services Card holders from December 2018.",
    ["https://en.wikipedia.org/wiki/Sixth_Labour_Government_of_New_Zealand"], T1)
add("2017-schools", "Scrap National Standards and charter schools", "2017 election", "education",
    "kept", "National Standards scrapped December 2017; charter school law repealed 2018 with existing schools converted to state 'special character' schools.",
    ["https://en.wikipedia.org/wiki/Sixth_Labour_Government_of_New_Zealand"], T1)
add("2017-superfund", "Resume contributions to the NZ Super Fund and keep the pension age at 65", "2017 election", "retirement",
    "kept", "Contributions resumed; age kept at 65.",
    ["https://en.wikipedia.org/wiki/Sixth_Labour_Government_of_New_Zealand"], T1)
add("2017-refugees", "Raise the refugee quota to 1,500", "2017 election", "immigration",
    "kept", "Quota raised (to 1,500 from July 2020; resettlement disrupted by COVID).",
    ["https://en.wikipedia.org/wiki/Sixth_Labour_Government_of_New_Zealand"], T1)
add("2017-abuse-rc", "Royal Commission into abuse in state care", "2017 election", "justice",
    "kept", "Established 2018; final report delivered 2024.",
    ["https://en.wikipedia.org/wiki/Royal_Commission_of_Inquiry_into_Abuse_in_Care"], T1)
add("2017-abortion", "Take abortion out of the Crimes Act", "2017 election (Ardern)", "social",
    "kept", "Abortion Legislation Act 2020 passed (conscience vote) in March 2020.",
    ["https://en.wikipedia.org/wiki/Abortion_Legislation_Act_2020"], T1)
add("2017-cannabis", "Hold a binding referendum on recreational cannabis by 2020 (Green C&S agreement)", "2017 Green agreement", "justice",
    "kept",
    "Held with the 2020 election; 'No' won 50.7% to 48.4%. Labour took no party position; Ardern revealed only after the vote that she had voted yes - some experts said her silence may have been decisive.",
    ["https://newshub.co.nz/home/politics/2020/10/jacinda-ardern-reveals-she-voted-in-favour-of-cannabis-legalisation-as-new-zealand-votes-no.html",
     "https://newshub.co.nz/home/politics/2021/03/jacinda-ardern-s-refusal-to-take-sides-may-have-been-a-decisive-factor-in-cannabis-referendum-experts.html",
     "https://en.wikipedia.org/wiki/2020_New_Zealand_cannabis_referendum"], T1)
add("2017-threestrikes", "Repeal the 'three strikes' sentencing law", "2018 (Justice Minister Andrew Little)", "justice",
    "kept",
    "Abandoned in June 2018 when NZ First refused support; repealed in 2022 once Labour governed alone (Three Strikes Legislation Repeal Act 2022). Reinstated by the National-led government in 2024.",
    ["https://www.1news.co.nz/2018/06/11/amateur-hour-stuff-simon-bridges-wastes-no-time-ridiculing-governments-backdown-on-three-strikes-law-repeal",
     "https://newshub.co.nz/home/politics/2021/11/with-nz-first-out-of-the-picture-labour-finally-moves-on-three-strikes-law-repeal.html",
     "https://en.wikipedia.org/wiki/Three_Strikes_Legislation_Repeal_Act_2022"], T2)
add("2019-ihumatao", "Ihumātao: no building on the land while talks continue, and a negotiated solution (Ardern, July 2019)", "July 2019 (in government)", "māori",
    "kept",
    "Development halted in 2019; in December 2020 the Crown agreed to buy the land from Fletcher Building for $29.9m (outside the Treaty settlement process) under the Land for Housing Programme, with a Kīngitanga/Crown/Auckland Council MoU. Critics raised precedent concerns for full and final settlements.",
    ["https://newshub.co.nz/home/politics/2020/12/ih-m-tao-deal-reached-government-to-purchase-south-auckland-land-from-fletcher-building-for-30-million.html",
     "https://www.teaonews.co.nz/2020/12/17/ihumatao-finally-settled/"], T1)
add("2019-tepukenga", "Merge the 16 polytechnics and industry training organisations into one national institute (Te Pūkenga) to make vocational education financially sustainable", "Announced February 2019 (in government)", "education",
    "partially-kept",
    "Not a 2017 manifesto commitment; went further than the options consulted on. Merger took effect 2020-2023, but Te Pūkenga ran large deficits (forecast up to $110m in 2022), suffered leadership turnover and missed transition milestones. The coalition government is breaking it up; standalone polytechnics resumed from 2026 with Te Pūkenga disestablished at the end of 2026.",
    ["https://en.wikipedia.org/wiki/Te_P%C5%ABkenga",
     "https://thespinoff.co.nz/the-bulletin/04-08-2022/all-polytechs-to-cut-costs-to-shrink-mega-polytechs-deficit",
     "https://www.1news.co.nz/2023/12/14/te-pukenga-minister-sets-targets-for-scrapping-super-institute/"], T1)

# ---------------- COVID-19 (in government) ----------------
add("2020-elimination", "COVID-19 elimination strategy ('go hard and go early')", "March 2020 (in government)", "health",
    "partially-kept",
    "Elimination achieved in 2020 and most of 2021, with among the lowest death rates in the OECD and negative excess mortality to early 2023 (Royal Commission phase 1, Nov 2024). The strategy was abandoned in October 2021 after Delta; the Commission's phase 2 (March 2026) found the response 'broadly effective but flawed', criticising lockdown length, mandates' social-cohesion costs and the slow exit.",
    ["https://www.1news.co.nz/2024/11/28/first-phase-of-royal-commission-of-inquiry-into-covid-19-released/",
     "https://thespinoff.co.nz/politics/10-03-2026/covid-19-inquiry-makes-final-findings-on-spending-mandates-and-lockdowns",
     "https://www.odt.co.nz/news/national/covid-response-broadly-effective-some-flaws-inquiry-finds"], T1)
add("2020-wagesubsidy", "COVID wage subsidy to keep workers attached to employers", "March 2020 (in government)", "economy",
    "kept",
    "More than $13b paid March-December 2020 (about $19b by end of 2021). The Auditor-General found 'much to commend' but weak post-payment verification and urged recovery/prosecution of misuse.",
    ["https://oag.parliament.nz/2021/wage-subsidy/overview.htm",
     "https://www.newsroom.co.nz/verdict-on-19b-wage-subsidy-lands-a-year-late"], T1)

# ---------------- 2020 election (Labour majority) ----------------
add("2020-39pc", "New 39% top tax rate on income over $180,000 (affecting ~2% of earners)", "2020 election", "tax",
    "kept", "Legislated December 2020, in force 1 April 2021.",
    ["https://www.taxpolicy.ird.govt.nz/news/2020/2020-12-02-introduction-taxation-income-tax-rate-other-amendments-bill",
     "https://www.newshub.co.nz/home/money/2020/10/labour-s-top-tax-rate-here-s-how-it-will-affect-you.html"], T2)
add("2020-nootertax", "No other tax changes beyond the 39% rate - specifically no extension of the bright-line test (Grant Robertson)", "2020 election", "tax",
    "broken",
    "In March 2021 the government extended the bright-line test from 5 to 10 years for existing homes and began phasing out interest deductibility for residential landlords. Robertson admitted he had been 'too definitive' in ruling out a bright-line extension during the campaign; he argued the bright-line test is not a new tax. (The coalition restored interest deductibility from 2025; Labour said in Sept 2026 it would not change it again.)",
    ["https://taxpolicy.ird.govt.nz/news/2021/2021-03-23-government-property-announcements",
     "https://newshub.co.nz/home/politics/2021/03/finance-minister-grant-robertson-admits-being-too-definitive-in-ruling-out-bright-line-extension-during-election.html",
     "https://www.interest.co.nz/news/108145/robertson-says-labour-wouldnt-be-breaking-its-pre-election-promises-tax-if-it-extended",
     "https://www.1news.co.nz/2026/09/21/labour-rules-out-interest-deductibility-changes-for-landlords/"], T2)
add("2020-wealthtax", "No wealth tax ('I won't allow it to happen as Prime Minister' - Ardern)", "2020 election", "tax",
    "kept", "No wealth tax introduced 2020-23 despite Green pressure; David Parker's later work on one was shut down by Hipkins in 2023.",
    ["https://newshub.co.nz/home/politics/2020/10/nz-election-2020-jacinda-ardern-rubbishes-desperate-wealth-tax-attacks-i-won-t-allow-it-to-happen-as-prime-minister.html",
     "https://thespinoff.co.nz/the-bulletin/13-07-2023/the-pms-damned-captains-call-can-new-tax-policy-steady-the-ship"], T2)
add("2020-sickleave", "Double minimum sick leave from 5 to 10 days", "2020 election", "work",
    "kept", "Legislation introduced December 2020; 10 days in force from July 2021.",
    ["https://www.1news.co.nz/2020/09/18/labour-promises-to-double-sick-leave-to-10-days/",
     "https://en.wikipedia.org/wiki/Sixth_Labour_Government_of_New_Zealand"], T2)
add("2020-matariki", "New Matariki public holiday from 2022", "2020 election", "māori",
    "kept", "First observed 24 June 2022 (Te Kāhui o Matariki Public Holiday Act 2022).",
    ["https://en.wikipedia.org/wiki/Matariki"], T2)
add("2020-conversion", "Ban conversion therapy", "2020 election", "social",
    "kept", "Conversion Practices Prohibition Legislation Act passed February 2022 (strong cross-party support).",
    ["https://en.wikipedia.org/wiki/Conversion_Practices_Prohibition_Legislation_Act_2022"], T2)
add("2020-fpa", "Introduce Fair Pay Agreements (sector-wide bargaining)", "2017 and 2020 elections", "work",
    "kept",
    "Delayed in the first term (NZ First opposed); Fair Pay Agreements Act passed October 2022. No FPA was concluded before the coalition repealed the Act under urgency in December 2023.",
    ["https://en.wikipedia.org/wiki/Fair_Pay_Agreements_Act_2022",
     "https://mbie.govt.nz/about/news/repeal-of-fair-pay-agreements-legislation",
     "https://thespinoff.co.nz/politics/22-12-2023/the-hard-won-and-swiftly-lost-dream-of-fair-pay-agreements"], T2)
add("2020-apprentice", "Free trades training and apprenticeships (TTAF) and Apprenticeship Boost", "2020 election / COVID recovery", "education",
    "kept", "Apprenticeship fees removed from 1 July 2020 (TTAF ran to end of 2022); Apprenticeship Boost subsidy for employers.",
    ["https://en.wikipedia.org/wiki/Sixth_Labour_Government_of_New_Zealand"], T2)
add("2020-publichousing", "8,000 more public and transitional homes (Budget 2020, campaigned on in 2020)", "Budget 2020 / 2020 election", "housing",
    "kept",
    "Public housing additions continued at the highest rate in decades (Labour: 13,000+ public homes and 4,000+ transitional places 2017-23). No independent final audit of the specific 8,000 package was found, and new-build share is disputed.",
    ["https://www.hud.govt.nz/news/housing-and-budget-2020",
     "https://www.aap.com.au/factcheck/labour-and-national-both-claim-credit-for-nz-public-housing-rise/",
     "https://waateanews.com/2023/09/25/labour-promises-6000-new-state-homes/"], T2)
add("2020-lightrail", "Progress Auckland light rail now NZ First is gone", "2020 election", "transport",
    "broken", "A $14.6b tunnelled scheme was endorsed in 2022 and a delivery company set up, but no construction began before the 2023 election; the project was cancelled in January 2024.",
    ["https://newshub.co.nz/home/politics/2020/10/phil-twyford-on-how-labour-can-progress-auckland-light-rail-without-new-zealand-first.html",
     "https://newshub.co.nz/home/politics/2023/02/auckland-light-rail-survives-policy-purge-but-completed-plans-still-two-years-away.html",
     "https://www.1news.co.nz/2024/01/14/government-officially-cancels-auckland-light-rail/"], T2)
add("2021-threewaters-optin", "Three Waters reform would be voluntary (councils could opt out)", "2020-21 (government statements)", "local government",
    "broken",
    "The government initially said participation was optional, then in mid/late 2021 made the transfer of water assets to new entities mandatory. Ardern denied misleading councils.",
    ["https://en.wikipedia.org/wiki/Three_Waters_reform_programme"], T2)
add("2021-threewaters", "Reform drinking, waste and storm water into large publicly owned entities (Three Waters)", "2021 (in government)", "local government",
    "partially-kept",
    "Water Services Entities Act 2022 passed in December 2022 with Labour votes only (including a controversial, later-removed entrenchment clause). Hipkins' April 2023 reset replaced 4 entities with 10 and delayed the start to 2026. Whether there was an electoral mandate was contested. Fully repealed by the coalition in February 2024 ('Local Water Done Well').",
    ["https://1news.co.nz/2023/04/13/three-waters-reset-mega-entities-scrapped-as-new-model-proposed/",
     "https://thespinoff.co.nz/politics/14-04-2023/three-waters-gets-put-out-of-its-misery",
     "https://en.wikipedia.org/wiki/Water_Services_Entities_Act_2022",
     "https://www.1news.co.nz/2024/02/12/three-waters-repeal-to-go-ahead-replacement-due-by-mid-2025"], T2)
add("2021-healthnz", "Replace the 20 district health boards with Health NZ (Te Whatu Ora) and a Māori Health Authority (Te Aka Whai Ora)", "Announced April 2021 (in government)", "health",
    "kept",
    "Pae Ora (Healthy Futures) Act 2022; new entities from 1 July 2022. Outcomes contested: Health NZ overspent (a $722m deficit for 2023/24), and in July 2024 the coalition replaced its board with a commissioner, blaming an over-centralised model; Labour called this 'political spin' and pointed to inflation and pay settlements. Te Aka Whai Ora was abolished in June 2024.",
    ["https://en.wikipedia.org/wiki/Pae_Ora_(Healthy_Futures)_Act_2022",
     "https://interest.co.nz/public-policy/128842/health-nz-unable-stay-within-its-budget-after-period-high-inflation-and-fast",
     "https://www.1news.co.nz/2024/07/22/turnaround-job-health-nz-board-sacked-commissioner-appointed/",
     "https://www.teaonews.co.nz/2024/02/28/parliament-passes-bill-to-disestablish-te-aka-whai-ora/"], T2)
add("2021-smokefree", "Smokefree generation: ban tobacco sales to anyone born after 1 Jan 2009, cut retailers and nicotine", "2021 (Smokefree 2025 action plan, in government)", "health",
    "kept", "Law passed December 2022; the three main measures were repealed by the coalition in early 2024 before taking effect.",
    ["https://en.wikipedia.org/wiki/Smokefree_Environments_and_Regulated_Products_(Smoked_Tobacco)_Amendment_Act_2022"], T2)
add("2021-cleancar", "Clean Car Discount (feebate) and clean car import standard", "2020-21 (in government)", "environment",
    "kept", "Discount operated 2021-2023 and the import standard was legislated; the discount was ended by the incoming government at the end of 2023. Hipkins had already dropped the related Clean Car Upgrade scheme.",
    ["https://en.wikipedia.org/wiki/New_Zealand_Labour_Party",
     "https://www.1news.co.nz/2023/12/22/the-year-that-began-and-ended-with-labour-policy-bonfires/"], T2)
add("2023-merger", "Merge RNZ and TVNZ into a new public media entity", "2021-22 (in government)", "media",
    "abandoned", "Scrapped in Hipkins' February 2023 'policy bonfire' after about $23m had been spent.",
    ["https://newstalkzb.co.nz/news/politics/pm-chris-hipkins-bonfire-of-the-policies-refocus-sees-rnztvnz-merger-gone-income-insurance-scheme-to-change",
     "https://www.1news.co.nz/2023/02/08/what-you-need-to-know-about-todays-government-announcements"], T2)
add("2023-incomeins", "Social unemployment insurance scheme (with business and unions)", "2022 (in government)", "work",
    "abandoned", "Shelved in February 2023 'until the economy improves'; not revived.",
    ["https://newstalkzb.co.nz/news/politics/pm-chris-hipkins-bonfire-of-the-policies-refocus-sees-rnztvnz-merger-gone-income-insurance-scheme-to-change"], T2)
add("2023-biofuel", "Biofuels mandate for transport fuel", "2021-22 (in government)", "environment",
    "abandoned", "Dropped February 2023 because it would raise fuel prices.",
    ["https://newstalkzb.co.nz/news/politics/pm-chris-hipkins-bonfire-of-the-policies-refocus-sees-rnztvnz-merger-gone-income-insurance-scheme-to-change"], T2)
add("2023-hatespeech", "Hate speech law reform (post-Christchurch Royal Commission)", "2021 (in government)", "justice",
    "abandoned", "Withdrawn and referred to the Law Commission in February 2023.",
    ["https://thespinoff.co.nz/politics/24-04-2023/purged-punted-and-pruned-the-chris-hipkins-reprioritisation-in-full"], T2)
add("2023-vote16", "Lower the voting age to 16 for local elections", "2022 (in government, after Supreme Court ruling)", "democracy",
    "abandoned", "Dropped in Hipkins' 2023 reprioritisation. Labour's 2026 platform again supports 16- and 17-year-olds voting in local elections.",
    ["https://en.wikipedia.org/wiki/New_Zealand_Labour_Party",
     "https://www.scoop.co.nz/stories/PO2610/S00007/make-it-16-welcomes-labours-support-for-16-and-17-year-olds-voting-at-local-elections.htm"], T2)
add("2023-prescriptions", "Remove the $5 prescription co-payment", "Budget 2023 (in government)", "health",
    "kept", "Took effect 1 July 2023; reinstated by the coalition from July 2024 for most adults. Labour promises to remove it again in 2026.",
    ["https://www.1news.co.nz/2024/05/30/budget-2024-5-prescription-fee-back-in-weeks-with-some-exceptions/"], T2)
add("2023-ptfares", "Free public transport for 5-12 year-olds and half-price fares for under-25s", "Budget 2023 (in government)", "transport",
    "kept", "In place from July 2023; central funding withdrawn by the coalition and the concessions ended 30 April 2024.",
    ["https://at.govt.nz/about-us/news-events/media-centre/2024-media-releases/public-transport-fares-are-changing-for-under-25-year-olds-from-wednesday-01-may",
     "https://www.1news.co.nz/2024/03/26/many-bus-and-train-youth-discounts-to-stop-in-auckland-wellington"], T2)

# ---------------- 2023 election (Labour lost; not testable) ----------------
add("2023-nocgt", "'Under a government I lead there will be no wealth or capital gains tax' (Hipkins, July 2023)", "2023 election", "tax",
    "abandoned",
    "After the defeat Hipkins said tax was 'back on the table' (Nov 2023). In October 2025 Labour adopted a 28% capital gains tax on residential and commercial property (excluding the family home and farms) from July 2027, to fund free GP visits - with Hipkins still leader.",
    ["https://www.1news.co.nz/2023/07/12/end-of-story-hipkins-rules-out-wealth-and-capital-gains-taxes",
     "https://www.1news.co.nz/2023/11/07/capital-gains-wealth-taxes-back-on-the-table-hipkins/",
     "https://www.rnz.co.nz/news/political/577021/labour-to-campaign-on-narrow-capital-gains-tax-no-wealth-tax"], OPP2, False)
add("2023-gstfv", "Remove GST from fresh and frozen fruit and vegetables from 1 April 2024", "2023 election (pledge card)", "tax",
    "abandoned",
    "Not implemented (Labour lost). It does not appear among Labour's 2026 policies as listed by policy.nz (October 2026); we did not find a formal statement dropping it, so treat 'abandoned' as 'not carried forward'. Robertson reportedly opposed it in 2023.",
    ["https://www.odt.co.nz/news/national/labour-no-gst-fruit-and-veg-boost-working-families",
     "https://newstalkzb.co.nz/news/politics/labour-tax-policy-pm-chris-hipkins-reveals-removal-of-gst-from-fruit-and-vegetables-national-leader-christopher-luxon-responds",
     "https://policy.nz/2026/party-vote/parties/labour-party"], OPP2, False)
add("2023-dental", "Free basic dental care for under-30s (18-23 from July 2025; 18-29 from July 2026)", "2023 election (campaign launch)", "health",
    "abandoned",
    "Not implemented (Labour lost). Not among Labour's 2026 policies as listed by policy.nz; 2026 health offer instead centres on free GP visits ('Medicard') and free prescriptions.",
    ["https://www.1news.co.nz/2023/09/02/labour-pledges-free-dental-for-under-30s-if-elected/",
     "https://policy.nz/2026/party-vote/parties/labour-party"], OPP2, False)
add("2023-statehouses", "6,000 more public homes by 2027", "2023 election", "housing",
    "not-yet-due", "Not implemented (Labour lost). Carried forward in 2026 as 'at least 6,000 more social housing places over the next 4 years'.",
    ["https://www.newstalkzb.co.nz/news/politics/election-2023-labour-promises-6000-more-state-houses",
     "https://www.rnz.co.nz/news/politics_election-2026/1552827/labour-pledges-4-billion-for-state-houses-school-repairs-and-hospitals"], OPP2, False)
add("2023-pledgecard", "Rest of the 2023 nine-point pledge card (20 hours free ECE for 2-year-olds, Working for Families boost, 300 more police, partner paid leave, financial literacy, India trade mission, permanent Apprenticeship Boost)", "2023 election (pledge card)", "general",
    "not-yet-due",
    "Untested because Labour lost. Some items reappear in 2026 (Apprenticeship Boost restored and expanded); others are not in the 2026 platform.",
    ["https://www.1news.co.nz/2023/09/10/chris-hipkins-reveals-labours-nine-point-pledge-to-voters",
     "https://www.rnz.co.nz/news/politics/633845/election-26-labour-proposes-apprenticeship-boost-expansion"], OPP2, False)

# ---------------- 2026 platform (not yet due) ----------------
N = "2026 election"
add("2026-cgt", "28% capital gains tax on residential and commercial property (excluding the family home and farms) from July 2027, not retrospective", N, "tax", "not-yet-due",
    "Labour's revenue base for its health offer; a reversal of Hipkins' 2023 pledge.", ["https://www.rnz.co.nz/news/political/577021/labour-to-campaign-on-narrow-capital-gains-tax-no-wealth-tax",
    "https://www.1news.co.nz/2026/10/18/labours-capital-gains-tax-explained-what-is-it-and-who-will-pay/"], NEXT, False)
add("2026-gp", "Up to three free GP visits a year for everyone (Medicard), free maternity scans, free cervical screening 25-69", N, "health", "not-yet-due", "",
    ["https://www.rnz.co.nz/news/political/598331/labour-promises-free-maternity-scans-if-elected", "https://policy.nz/2026/party-vote/parties/labour-party"], NEXT, False)
add("2026-prescriptions", "Remove the $5 prescription charge (again)", N, "health", "not-yet-due", "", ["https://www.labour.org.nz/prescriptions"], NEXT, False)
add("2026-futurefund", "NZ Future Fund to invest in infrastructure and NZ businesses (Temasek-style)", N, "economy", "not-yet-due",
    "Labour said in May 2026 it would not release the fund's costing or which state assets would be included until after the election.",
    ["https://www.1news.co.nz/2025/10/20/nz-future-fund-labour-reveals-first-major-policy-for-next-election/",
     "https://www.nzherald.co.nz/nz/politics/labour-admits-it-will-not-release-cornerstone-policy-costing-and-job-modelling-until-after-the-election-blames-treaty-of-waitangi-concerns/QNGXJK4SHZFOJB52WFCVHPLR4E/"], NEXT, False)
add("2026-farecap", "$20 weekly public transport fare cap in Auckland, Wellington and Christchurch ($10 elsewhere) from July 2027", N, "transport", "not-yet-due",
    "Labour costed it at $65m a year; economists Sam Warburton and Brad Olsen estimated $91-112m.",
    ["https://www.stuff.co.nz/politics/360990643/labour-reveals-public-transport-fare-cap-long-awaited-election-policy",
     "https://www.rnz.co.nz/news/politics/598268/material-miscalculation-economists-identify-apparent-errors-in-labour-s-transport-policy"], NEXT, False)
add("2026-fiscal", "Return to surplus by 2029/30 and cut net debt to around 20% of GDP; independent Parliamentary Budget Office; restore wellbeing reporting and the Reserve Bank's dual mandate", N, "economy", "not-yet-due", "",
    ["https://www.rnz.co.nz/news/politics_election-2026/1081146/labour-releases-fiscal-strategy-promises-to-slash-debt"], NEXT, False)
add("2026-nogst", "Rule out raising GST in 2027; oppose fuel excise increases; no change to landlord interest deductibility", N, "tax", "not-yet-due", "",
    ["https://www.labour.org.nz/news/release-national-refuses-to-rule-out-gst-hike/",
     "https://www.1news.co.nz/2026/09/21/labour-rules-out-interest-deductibility-changes-for-landlords/"], NEXT, False)
add("2026-housing", "$4b over four years for at least 6,000 more social housing places, school and hospital repairs", N, "housing", "not-yet-due", "",
    ["https://www.rnz.co.nz/news/politics_election-2026/1552827/labour-pledges-4-billion-for-state-houses-school-repairs-and-hospitals"], NEXT, False)
add("2026-studentloan", "Write off 10% of eligible graduates' student loans ($583.4m over four years)", N, "education", "not-yet-due", "",
    ["https://www.nzherald.co.nz/nz/politics/labour-kicks-off-campaign-after-national-hammers-home-tax-attack/JJ6SXVR3HJH2RB7BF4567UTSDI/"], NEXT, False)
add("2026-payequity", "Restore the pay equity regime and give 65,000 care and support workers a pay rise ($2.5b over four years)", N, "work", "not-yet-due", "",
    ["https://www.rnz.co.nz/news/politics_election-2026/1718141/labour-releases-its-fiscal-plan-promises-pay-rise-for-care-and-support-workers"], NEXT, False)
add("2026-kiwisaver", "Make employer KiwiSaver contributions compulsory and raise the minimum contribution to 6%", N, "retirement", "not-yet-due", "",
    ["https://www.rnz.co.nz/news/politics_election-2026/1356180/labour-to-make-employer-contributions-to-kiwisaver-compulsory-if-elected"], NEXT, False)
add("2026-supermarkets", "Force Foodstuffs and Woolworths to separate wholesale from retail; ban excessive pricing ('price gouging')", N, "economy", "not-yet-due", "",
    ["https://www.rnz.co.nz/news/politics_election-2026/1478631/labour-proposes-splitting-foodstuffs-and-woolworths-from-their-wholesale-arms",
     "https://www.rnz.co.nz/news/politics_election-2026/1410372/labour-pledges-to-ban-big-companies-from-charging-excessive-prices"], NEXT, False)
add("2026-rsa", "Repeal the Regulatory Standards Act within the first 100 days", N, "governance", "not-yet-due", "",
    ["https://www.rnz.co.nz/news/political/578793/controversial-regulatory-standards-bill-passes-third-reading"], NEXT, False)
add("2026-socialmedia", "Send an under-16 social media ban bill to select committee within 100 days", N, "digital", "not-yet-due", "",
    ["https://www.rnz.co.nz/news/politics_election-2026/2015458/labour-pledges-social-media-ban-for-under-16s"], NEXT, False)
add("2026-education", "Pause the coalition's NCEA replacement and curriculum overhaul; restore school boards' Treaty obligations; 1,000 more teacher aides; locally made school lunches", N, "education", "not-yet-due", "",
    ["https://www.rnz.co.nz/news/politics_election-2026/1438233/labour-to-pause-government-s-school-curriculum-overhaul-ncea-changes-if-elected",
     "https://newsroom.co.nz/2026/04/28/labour-vows-to-reinstate-school-boards-treaty-obligations/",
     "https://www.rnz.co.nz/news/politics_election-2026/2074975/labour-promises-to-hire-1000-more-teacher-aides"], NEXT, False)
add("2026-justice", "Scrap youth offender boot camps; create a corporate homicide offence", N, "justice", "not-yet-due", "",
    ["https://www.stuff.co.nz/politics/361034862/failed-experiment-labour-vows-scrap-youth-offender-boot-camps",
     "https://www.rnz.co.nz/news/politics/1446374/labour-s-proposed-corporate-homicide-charges-welcomed-by-pike-river-mine-families"], NEXT, False)
add("2026-foreign", "Recognise Palestine, sanction Israel, stay out of AUKUS, lift aid towards 0.7% of GDP", N, "foreign affairs", "not-yet-due", "",
    ["https://www.rnz.co.nz/news/politics/1528401/labour-sums-up-its-foreign-policy-approach-as-independent-principled-and-unafraid",
     "https://en.wikipedia.org/wiki/New_Zealand_Labour_Party"], NEXT, False)
add("2026-nurses", "Guarantee a job for every NZ-trained graduate nurse", N, "health", "not-yet-due", "",
    ["https://www.rnz.co.nz/news/politics_election-2026/1197296/labour-promises-every-graduate-nurse-will-get-a-job"], NEXT, False)
add("2026-minwage", "Increase the minimum wage every year", N, "work", "not-yet-due", "",
    ["https://www.labour.org.nz/news/release-a-vote-for-national-means-three-years-of-frozen-wages/"], NEXT, False)

def main():
    out = ROOT / "data/promises/labour.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(P, ensure_ascii=False, indent=1) + "\n")
    ids = [p["id"] for p in P]; assert len(ids) == len(set(ids)), "duplicate ids"
    print("total entries", len(P))
    print("by status (all):", dict(collections.Counter(p["status"] for p in P)))
    sc = [p for p in P if p["scored"]]
    print("scored (testable in office):", len(sc))
    for term in (T1, T2):
        c = collections.Counter(p["status"] for p in sc if p["term"] == term)
        n = sum(c.values()); print(term, n, dict(c))
    c = collections.Counter(p["status"] for p in sc); n = len(sc)
    print("ALL SCORED", {k: f"{v} ({100*v/n:.0f}%)" for k, v in c.items()})
    for term in (OPP1, OPP2, NEXT):
        print(term, dict(collections.Counter(p["status"] for p in P if p["term"] == term)))

if __name__ == "__main__":
    main()
