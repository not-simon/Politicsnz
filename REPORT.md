# Ballot Book NZ: the 2026 election report

**New Zealand general election: Saturday 7 November 2026.** Snapshot taken **23 October 2026**. Advance voting opens on Monday 26 October,
and the last day to enrol is Sunday 25 October. There is no election-day enrolment this year
([elections/2026.md](elections/2026.md); [Electoral Commission factsheet](https://elections.nz/assets/2026-General-Election/2026-Factsheet-Make-Sure-Youre-Enrolled-for-the-2026-General-Election-v2.pdf)).

This report pulls together the whole archive: results since 2008, 129 polls taken since the 2023 election, about 1,400 policy
statements for 2026, and promise-by-promise track records for eight parties. It describes the parties and their records. It
**does not recommend any party**. Each factual sentence links to an outside source or to the archive file it comes from, and
those files carry their own sources. Tables marked `GENERATED` are built from the JSON by
[`tools/report_stats.py`](tools/report_stats.py), so the numbers match the data. Run `python3 tools/report_stats.py --write`
to rebuild them.

**Contents:** [1. Summary](#1-summary-for-busy-voters) · [2. The parties](#2-the-2026-choice-party-by-party) ·
[3. Head-to-head](#3-head-to-head-on-the-big-issues) · [4. Promise-keeping](#4-reliability-and-promise-keeping) ·
[5. Performance in government](#5-performance-in-government-200826) · [6. Trends](#6-trends-20112026) ·
[7. Who's who](#7-whos-who) · [8. Data quality](#8-data-quality-and-limitations) · [9. Using the archive](#9-how-to-use-this-archive)

---

## 1. Summary for busy voters

**The state of play.** The 2023 election produced New Zealand's first three-party coalition under MMP: National, ACT and NZ
First, led by Christopher Luxon. It started with 68 of 123 seats ([data/elections/2023.json](data/elections/2023.json);
[data/parliaments/54.json](data/parliaments/54.json)). Over the term National's vote has slid from 38% to the high 20s, NZ First and TOP
have risen, and the Greens have reached record poll levels. The polls now show a race too close to call
([elections/2026.md](elections/2026.md#polling)).

<!-- GENERATED:report-polls START -->
| Party | 2023 result % | 30-day poll average % | Range in window | Change since 2023 (pp) |
|---|---:|---:|---|---:|
| National | 38.08 | **28.7** | 25.9–32.0 | -9.4 |
| Labour | 26.92 | **27.9** | 23.5–30.8 | +1.0 |
| Green | 11.61 | **15.2** | 13.3–16.0 | +3.5 |
| ACT | 8.64 | **9.8** | 9.0–11.0 | +1.2 |
| NZ First | 6.09 | **10.2** | 8.0–12.0 | +4.1 |
| Te Pāti Māori | 3.08 | **1.4** | 0.4–2.0 | -1.7 |
| TOP (Opportunity) | 2.22 | **6.2** | 4.8–8.0 | +4.0 |
| *National + ACT + NZ First* | 52.81 | **48.6** | | -4.2 |
| *Labour + Green + Te Pāti Māori* | 41.61 | **44.4** | | +2.8 |

Window: 9 polls with fieldwork ending 2026-09-27 to 2026-10-19 (1 News–Verian, Anacta, RNZ–Reid Research, Roy Morgan, Taxpayers' Union–Curia, The Post/Freshwater Strategy). Simple unweighted mean; each poll counts once. Source rows: [`data/polls-2026.json`](data/polls-2026.json) (from [Wikipedia's poll table](https://en.wikipedia.org/wiki/Opinion_polling_for_the_2026_New_Zealand_general_election), each row linked to the pollster's release).
<!-- GENERATED:report-polls END -->

**What those numbers could mean in seats.** The table below applies the Sainte-Laguë formula to the 30-day poll average. It uses
the same seat rules as the Electoral Act: a party needs 5% of the party vote or one electorate seat, and the House can grow if a
party wins overhang seats ([trends §3](elections/trends.md#3-turnout-overhang-and-the-wasted-vote)). It is an illustration, not a
forecast. Polls carry sampling error of roughly ±3 points for a party near 30%, and TOP is close enough to 5% that small movements
change the result.

<!-- GENERATED:report-seats START -->
| Scenario | National | Labour | Green | ACT | NZ First | Te Pāti Māori | TOP (Opportunity) | Te Tai Tokerau Party | House | Majority needs | Nat+ACT+NZF | Lab+Grn+TPM | Lab+Grn+TPM+TOP | Wasted vote % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 35 | 34 | 19 | 12 | 12 | 0 | 8 | 0 | 120 | 61 | 59 | 53 | 61 ✔ | 2.1 |
| **B** | 35 | 34 | 18 | 12 | 12 | 4 | 7 | 0 | 122 | 62 | 59 | 56 | 63 ✔ | 0.8 |
| **C** | 35 | 34 | 18 | 12 | 12 | 4 | 7 | 1 | 123 | 62 | 59 | 56 | 63 ✔ | 0.8 |
| **D** | 37 | 36 | 19 | 13 | 13 | 4 | 0 | 0 | 122 | 62 | 63 ✔ | 59 | 59 | 7.0 |

- **A**: Threshold only: six parties ≥5% (incl. TOP); no electorate-only winners.
- **B**: As A, plus Te Pāti Māori wins the 4 Māori seats it held at dissolution.
- **C**: As B, plus Te Tai Tokerau Party (Kapa-Kingi) holds Te Tai Tokerau.
- **D**: As B, but TOP falls below 5% and wins no electorate.
- ✔ = reaches a majority of the House on its own. "Wasted vote" = poll share of parties that win no seats (including "others", so it is 100 minus the qualifying parties' combined share).

**Sensitivity – every poll in the window, scenario B assumptions:**

| Fieldwork | Pollster | Nat+ACT+NZF | Lab+Grn+TPM | TOP | House | Outcome |
|---|---|---:|---:|---:|---:|---|
| 23–27 Sep 2026 | [1 News–Verian](https://www.1news.co.nz/2026/09/28/poll-greens-surge-to-best-result-ever-as-national-labour-slide-further/) | 58 | 58 | 7 | 123 | TOP decides (either side + TOP) |
| 31 Aug – 27 Sep 2026 | [Roy Morgan](https://www.roymorgan.com/findings/10351-nz-national-voting-intention-september-2026) | 63 | 51 | 8 | 122 | Nat+ACT+NZF majority |
| 24 Sep – 1 Oct 2026 | [RNZ–Reid Research](https://www.rnz.co.nz/news/politics_election-2026/1749693/rnz-reid-research-poll-national-crashes-greens-surge-opportunity-kingmaker) | 56 | 59 | 7 | 122 | TOP decides (either side + TOP) |
| 1–5 Oct 2026 | [Taxpayers' Union–Curia](https://www.taxpayers.org.nz/oct2026_nztucurpolljjhhfas) | 65 | 57 | 0 | 122 | Nat+ACT+NZF majority |
| 1–5 Oct 2026 | [1 News–Verian](https://www.1news.co.nz/2026/10/06/poll-opportunity-still-in-kingmaker-seat-as-greens-hold-strong/) | 58 | 57 | 8 | 123 | TOP decides (either side + TOP) |
| 6–10 Oct 2026 | [Anacta](https://www.thepost.co.nz/nz-news/361100468/labour-and-national-below-30-labours-pollster-tells-corporate-clients) | 57 | 58 | 7 | 122 | TOP decides (either side + TOP) |
| 8–12 Oct 2026 | [1 News–Verian](https://www.1news.co.nz/2026/10/13/poll-hipkins-and-luxon-now-neck-and-neck-opportunity-on-track-for-10-mps/) | 58 | 56 | 10 | 124 | TOP decides (either side + TOP) |
| 15–19 Oct 2026 | [1 News–Verian](https://www.1news.co.nz/2026/10/20/poll-national-jumps-leaving-labours-position-perilous/) | 60 | 55 | 8 | 123 | TOP decides (either side + TOP) |
| 9–19 Oct 2026 | [The Post/Freshwater Strategy](https://www.thepost.co.nz/politics/361101225/postfreshwater-strategy-poll-fraction-point-could-decide-who-governs) | 59 | 56 | 7 | 122 | TOP decides (either side + TOP) |

Tally: TOP decides (either side + TOP): 7; Nat+ACT+NZF majority: 2.
<!-- GENERATED:report-seats END -->

**What the arithmetic means politically.** On these numbers neither declared bloc wins a majority on its own **unless TOP falls
below 5%**. If TOP misses the threshold, its votes are wasted and the current coalition gets a majority (scenario D). Whether TOP
can be part of a government depends on who will work with it:

| Party | Will work with | Rules out | Source |
|---|---|---|---|
| National | ACT, NZ First | Labour ("grand coalition"), TOP (from 27 Jul 2026) | [RNZ](https://www.rnz.co.nz/news/politics/809555/national-rules-out-working-with-opportunity-party), [Bloomberg](https://www.bloomberg.com/news/articles/2026-05-11/new-zealand-pm-luxon-rules-out-grand-coalition-with-labour) |
| Labour | Greens; "door open" to TOP; could work with Te Pāti Māori, but senior roles "unlikely" | NZ First, ACT | [NZ Herald](https://www.nzherald.co.nz/nz/politics/labours-door-open-to-opportunity-senior-roles-for-te-pati-maori-unlikely-as-chris-hipkins-clarifies-vague-remarks/UBE55KHGCFGDHGYSRLQ3PUQN7Q/), [NZ Herald](https://www.nzherald.co.nz/nz/politics/its-clearly-not-going-to-happen-chris-hipkins-definitively-rules-out-nz-first/YGB36A3QYFF5RDBP6N7HGYV32Q/) |
| Green | Labour (joint Waitangi announcement, Feb 2026) | No formal statement found | [RNZ](https://www.rnz.co.nz/news/alert-top/585809/watch-live-labour-and-greens-speak-from-waitangi-treaty-grounds) |
| ACT | National, NZ First; a four-party deal with TOP "would be a good outcome" | Labour | [RNZ](https://www.rnz.co.nz/news/politics_election-2026/1932454/four-headed-beast-act-leader-david-seymour-hints-at-potential-for-coalition-with-opportunity) |
| NZ First | National, ACT | Labour; Peters said "No, I can't" to sitting at a Cabinet table with TOP's leader | [1News](https://www.1news.co.nz/2026/10/22/analysis-the-real-roadblock-to-opportunity-isnt-luxon-its-peters/) |
| Te Pāti Māori | Asks its voters to give their party vote to Labour or the Greens | The current government parties | [RNZ](https://www.rnz.co.nz/news/politics_election-2026/1011909/te-pati-maori-reveals-election-strategy-as-campaign-launches-in-gisborne) |
| TOP | Will talk to either side, starting with the largest party; "not here to prop up the current coalition government" | Any government with Winston Peters as Foreign Minister; also has five bottom lines | [1News](https://www.1news.co.nz/2026/10/21/opportunity-would-have-walked-away-from-current-coalition/) |

Full stances: [data/guide/parties.json](data/guide/parties.json) (`coalition_stance_2026`).

**What voters say matters.** In the Ipsos Issues Monitor (May 2026), the top concerns were:

- cost of living and inflation, 61%;
- healthcare, 39%;
- the economy, 33%;
- petrol prices, 26%;
- housing, 21%;
- unemployment, 19%.

Source: [elections/2026.md](elections/2026.md#campaign-issues); [RNZ](https://www.rnz.co.nz/news/political/596305/fuel-prices-become-fourth-biggest-issue-for-new-zealanders-poll-finds).

The latest economic figures:

- Annual inflation was **3.7%** in the September 2026 quarter, with petrol up 19.1%
  ([Stats NZ](https://www.stats.govt.nz/information-releases/consumers-price-index-september-2026-quarter/);
  [interest.co.nz](https://www.interest.co.nz/economy/140742/annual-inflation-hits-37-september-quarter-petrol-continuing-lead-way-followed)).
- Unemployment was **5.6%**, an 11-year high ([1News](https://www.1news.co.nz/2026/08/05/nzs-unemployment-rate-hits-11-year-high-in-june-quarter/)).

**The seven parties polling at or above 1%, in one line each** (from [data/guide/parties.json](data/guide/parties.json); details in §2):

| Party | One-line offer | Oct poll avg |
|---|---|---:|
| [National](parties/national/README.md) | No new taxes and a surplus by 2028/29; compulsory KiwiSaver; split Foodstuffs; 30 weeks' paid parental leave; replace NCEA | 28.7% |
| [Labour](parties/labour/README.md) | A 28% capital gains tax on property (not the family home) to fund three free GP visits a year; restore pay equity; force supermarkets to split wholesale from retail; $20/week fare cap | 27.9% |
| [Green](parties/green/README.md) | A 2.5% wealth tax above $10m and the first $10,000 of income tax-free; 2% cap on rent rises; a state supermarket ("KiwiMart"); "Kiwipower" | 15.2% |
| [NZ First](parties/nz-first/README.md) | Split the power companies and Foodstuffs; buy back BNZ; voting and NZ Super for citizens only; a referendum on the Māori seats | 10.2% |
| [ACT](parties/act/README.md) | Merge 43 departments into 19; raise the super age to 67 by 2035; repeal the Zero Carbon Act; three-year minimum-wage freeze | 9.8% |
| [TOP](parties/opportunity/README.md) | A Citizen's Income of up to $370 a week, funded by a land value tax; donation cap and lobbying register; ban bottom trawling | 6.2% |
| [Te Pāti Māori](parties/te-pati-maori/README.md) | First $30,000 tax-free and a wealth tax; an independent Te Tiriti Commission; abolish prisons by 2040; asks for electorate votes, with party votes to Labour or the Greens | 1.4% |

Ten other registered parties are standing. policy.nz lists each below 0.5%, or gives no figure
([§2.8](#28-the-other-ten-registered-parties)). If you want to match your own views against party positions, try the
45-statement quiz in [`site/`](site/index.html) ([method](guide/quiz-method.md)).

---

## 2. The 2026 choice, party by party

There are **17 registered parties** on the party-vote ballot ([data/elections/2026.json](data/elections/2026.json);
[RNZ explainer](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election)).
Each profile below uses the same template:

- **Left–right label:** as given in the party's Wikipedia infobox, quoted rather than judged by us ([position method](data/guide/parties.json)).
- **Party's own framing ("they say")** and **attributed criticism ("critics say")**: neither is the archive's view.
- **Costings:** what the party has published.
- **Track-record line:** computed from [data/promises/](data/promises/) (method in §4).

<!-- GENERATED:report-policies START -->
| Party | 2026 policies in archive | Most common topics | Policy list |
|---|---:|---|---|
| National | 159 | economy, transport-and-infrastructure, environment | [policies](parties/national/policies/README.md) |
| Labour | 126 | incomes-and-employment, economy, education | [policies](parties/labour/policies/README.md) |
| Green | 564 | environment, economy, community-and-inclusion | [policies](parties/green/policies/README.md) |
| ACT | 110 | economy, incomes-and-employment, environment | [policies](parties/act/policies/README.md) |
| NZ First | 79 | economy, incomes-and-employment, migration | [policies](parties/nz-first/policies/README.md) |
| Te Pāti Māori | 91 | te-ao-maori, te-tiriti-o-waitangi-and-governance, te-reo-maori-and-culture | [policies](parties/te-pati-maori/policies/README.md) |
| TOP (Opportunity) | 77 | economy, incomes-and-employment, environment | [policies](parties/opportunity/policies/README.md) |
| NZ Loyal | 10 | law-justice-and-government, defence-and-foreign-affairs, international-relations | [policies](parties/nz-loyal/policies/README.md) |
| NZ Outdoors & Freedom | 18 | law-justice-and-government, environment, health | [policies](parties/nz-outdoors-freedom/policies/README.md) |
| Legalise Cannabis | 11 | law-justice-and-government, health, criminal-justice | [policies](parties/legalise-cannabis/policies/README.md) |
| Animal Justice | 38 | community-and-inclusion, economy, agriculture | [policies](parties/animal-justice/policies/README.md) |
| Alliance | 27 | incomes-and-employment, economy, wages-and-working-conditions | [policies](parties/alliance/policies/README.md) |
| Conservative | 19 | law-justice-and-government, economy, health | [policies](parties/conservative/policies/README.md) |
| Women's Rights | 17 | women, community-and-inclusion, law-justice-and-government | [policies](parties/womens-rights/policies/README.md) |
| Vision NZ | 35 | incomes-and-employment, community-and-inclusion, education | [policies](parties/vision-nz/policies/README.md) |
| Free Palestine | 6 | defence-and-foreign-affairs, international-relations, community-and-inclusion | [policies](parties/free-palestine/policies/README.md) |
| Te Tai Tokerau Party | 22 | te-ao-maori, economy, te-tiriti-o-waitangi-and-governance | [policies](parties/te-tai-tokerau-party/policies/README.md) |

1409 policies across the 17 registered parties (electorate-only groups hold the rest of the archive's 1,435). Topic labels are policy.nz's where available. Counts reflect how parties publish (the Greens itemise their whole manifesto and 40 policy papers), not how much they plan to do.
<!-- GENERATED:report-policies END -->

### 2.1 National (centre-right) – leader Christopher Luxon

- **Stands for:** National leads the current government. It wants taxes kept where they are, spending held tight and the books
  back in surplus ([guide card](data/guide/parties.json); [Wikipedia label](https://en.wikipedia.org/wiki/New_Zealand_National_Party)).
- **Headline 2026 policies:** the "ten commitments" launched on 27 September 2026 ([National](https://www.national.org.nz/news/260927-christopherluxon-1)):
  - no new taxes;
  - compulsory KiwiSaver, with a $1,500 "Baby Boost";
  - paid parental leave extended from 26 to 30 weeks;
  - replace NCEA;
  - wider 5%-deposit First Home Loans;
  - structural separation of Foodstuffs;
  - $604m more for Pharmac and free bowel screening from 50, part-funded by cutting non-Pacific aid;
  - drug-testing of some beneficiaries;
  - no "good character" discounts in sentencing for sex offending;
  - referendums on MMP and on a four-year term.

  Sources: [README](parties/national/README.md#the-2026-campaign-pitch-and-headline-promises); [all 159 policies](parties/national/policies/README.md).
- **Costings:** its fiscal plan (12 Oct 2026) keeps new spending to $2.4b a year and leaves $7.5b unallocated over four years
  ([fiscal plan PDF](https://assets.national.org.nz/web/prod/National's%20Fiscal%20Plan.pdf)). It targets an OBEGALx surplus in 2028/29
  and debt below 40% of GDP ([README](parties/national/README.md)).
- **They say:** "Fixing the Basics, Building the Future"; it will "not impose new taxes". **Critics say:** Labour says "unemployment is
  higher, growth is weaker, debt has continued to rise" ([Labour fiscal plan](https://www.labour.org.nz/fiscal-plan)).
- **Coalition:** wants to continue with ACT and NZ First; rules out Labour and TOP (see §1).
- **Track record:** 61 resolved promises, delivery index 66% (§4). It was very reliable on repeal and legislation promises and
  weaker on outcome targets: the surplus date, 500 police, fees-free and the Dunedin Hospital
  ([track-record.md](parties/national/track-record.md#summary)).

### 2.2 Labour (centre-left) – leader Chris Hipkins

- **Stands for:** Labour is the main opposition and governed from 2017 to 2023. It is campaigning on health costs paid for by a new
  property tax, and on taking on big companies over prices ([guide card](data/guide/parties.json)).
- **Headline 2026 policies** ("Better Starts Now") ([README](parties/labour/README.md#2026-pitch-and-headline-promises); [126 policies](parties/labour/policies/README.md)):
  - a 28% capital gains tax on residential and commercial property (excluding the family home and farms) to fund up to three free
    GP visits a year;
  - free prescriptions, free cervical screening and free maternity scans;
  - restore the old pay-equity law, with a $4/hour pay rise for 65,000 care workers;
  - make price gouging illegal and force supermarkets to separate wholesale from retail;
  - $20/week public transport fare caps in the three biggest cities;
  - a 10% student-loan write-off;
  - at least 6,000 social homes;
  - a "NZ Future Fund";
  - repeal the Regulatory Standards Act within 100 days.
- **Costings:** its fiscal plan (Oct 2026) was reviewed by Hall Chadwick. It keeps the $2.4b operating allowance, forecasts a surplus
  in 2028/29 and targets net debt below 20% of GDP ([Labour](https://www.labour.org.nz/fiscal-plan)). National's Nicola Willis says
  restoring pay equity alone would cost $11b on Treasury estimates ([RNZ](https://www.rnz.co.nz/news/politics_election-2026/1733687/labour-s-fiscal-plan-national-s-claims-and-how-labour-is-defending-it)).
  Economists have queried the fare-cap costing: Labour says $65m, their estimates are $91–112m ([RNZ](https://www.rnz.co.nz/news/politics/598268/material-miscalculation-economists-identify-apparent-errors-in-labour-s-transport-policy)).
  Labour will not publish Future Fund costings before the election ([NZ Herald](https://www.nzherald.co.nz/nz/politics/labour-admits-it-will-not-release-cornerstone-policy-costing-and-job-modelling-until-after-the-election-blames-treaty-of-waitangi-concerns/QNGXJK4SHZFOJB52WFCVHPLR4E/)).
- **Coalition:** will govern with the Greens and is open to TOP and (with limits) Te Pāti Māori. It rules out NZ First and ACT.
  Hipkins has ruled out giving the Greens or Te Pāti Māori the police or corrections portfolios
  ([NZ Herald](https://www.nzherald.co.nz/nz/politics/election-2026-labours-chris-hipkins-rules-out-greens-te-pati-maori-from-major-ministerial-roles-in-herald-debate/3GBPYMI6TJBKHLVNOSPGY6WTKA/)).
- **Track record:** 61 scored promises from 2017–23, delivery index 67%. It reliably delivered laws and money transfers (about 71%
  kept outright) but kept only 2 of 13 big build or outcome targets outright (KiwiBuild, light rail, the migration cut)
  ([track-record.md](parties/labour/track-record.md#6-reliability-scorecard)). If Labour wins, the CGT will be its key test: the
  party has promised and then dropped a CGT four times since 2011 ([track-record §9](parties/labour/track-record.md#9-what-the-record-suggests-for-2026-promises)).

### 2.3 Green Party (centre-left to left-wing) – co-leaders Marama Davidson and Chlöe Swarbrick

- **Stands for:** strong climate and nature action, and a higher income floor paid for by taxing the very wealthy
  ([guide card](data/guide/parties.json); [Charter](parties/green/README.md#3-values-the-charter)).
- **Headline 2026 policies** ("For All of Us") ([README §10](parties/green/README.md#10-2026-pitch-and-headline-promises); [564 itemised policies](parties/green/policies/README.md)):
  - tax:
    - a 2.5% wealth tax on net wealth over $10m;
    - an inheritance and gift tax;
    - a 33% rate for the biggest companies;
    - a new top bracket above $160,000;
    - the first $10,000 of income tax-free;
  - housing: a 2% cap on rent rises and many more public homes;
  - "KiwiMart", a state supermarket chain made up of 120 stores the big two would have to sell;
  - "Kiwipower", a public renewable-energy company;
  - $2 public transport fares;
  - repeal the Fast-track Approvals Act and revoke the mining consents granted under it;
  - restore pay equity and free school lunches.
- **Costings:** its fiscal plan (23 Oct 2026) had its direct effects reviewed by Infometrics. It raises about $28.75b over four years
  from new taxes, delays surplus to 2029/30 and has net core Crown debt at 44% of GDP by 2030/31
  ([Newstalk ZB](https://www.newstalkzb.co.nz/news/politics/election-2026-green-party-s-plan-to-transform-nz-s-finances-with-more-tax-spending-debt/);
  [B2B News](https://b2bnews.co.nz/news/greens-fiscal-plan-adds-26-point-6bn-in-debt-by-2030-31/)). The plan document itself could
  not be retrieved ([policies README](parties/green/policies/README.md)). National says it contains "nine new taxes" (same source).
- **Coalition:** will support only a Labour-led government. It has not formally ruled any party in or out
  ([README §11](parties/green/README.md#11-coalition-stance)).
- **Track record:** the Greens have never been in Cabinet. They were a support partner from 2017 to 2023. Delivery index 59% overall,
  67% as a support partner. Delivery was best in 2017–20, when Labour needed their votes. Two breaches of the party's own stated
  principles are recorded: the 2018 waka-jumping vote and the 2020 Green School grant
  ([track-record.md](parties/green/track-record.md#1-scorecard)).

### 2.4 ACT (right-wing) – leader David Seymour

- **Stands for:** a smaller state, lower spending, deregulation, and "one law for all" regardless of race
  ([README](parties/act/README.md); [Wikipedia](https://en.wikipedia.org/wiki/ACT_New_Zealand)).
- **Headline 2026 policies** ([110 policies](parties/act/policies/README.md); [guide card](data/guide/parties.json)):
  - merge 43 departments into 19 and abolish population-group ministries;
  - raise the super age gradually to 67 by 2035;
  - repeal the Zero Carbon Act and abolish the Climate Change Commission;
  - a three-year minimum-wage freeze and a training wage;
  - three strikes for burglary;
  - deport serious non-citizen offenders;
  - close the Waitangi Tribunal once historical claims are settled;
  - opposes breaking up the supermarkets.
- **Costings:** its fiscal plan (11 Oct 2026) promises lower debt and spending, including $653m less on disability benefits
  ([ACT fiscal plan PDF](https://assets.nationbuilder.com/actnz/pages/38747/attachments/original/1791599898/ACT_2026_Fiscal_Plan.pdf?1791599898)).
  RNZ noted two unexplained items, one of about $100m a year and one of $264–303m a year of tax relief
  ([RNZ](https://www.rnz.co.nz/news/politics_election-2026/1835030/election-2026-as-it-happened-11-oct-greens-label-act-fiscal-plan-welfare-for-the-wealthiest-opportunity-seeks-answers-over-assumptions)).
  The Greens call the plan "welfare for the wealthiest" (same source).
- **Coalition:** wants to "lock Labour out" and is open to a four-party deal that includes TOP
  ([RNZ](https://www.rnz.co.nz/news/politics_election-2026/1932454/four-headed-beast-act-leader-david-seymour-hints-at-potential-for-coalition-with-opportunity)).
- **Track record:** delivery index 61% overall and 64% for 2023–26. Its track record calls ACT "highly reliable at delivering what it
  negotiates, but negotiated away a good part of what it campaigned on". Examples it traded away: the Treaty referendum, its own tax
  plan, and repeal of the Zero Carbon Act ([track-record.md](parties/act/track-record.md#reliability-scorecard)).

### 2.5 NZ First (Wikipedia gives no infobox label; its opening sentence says "right-wing populist") – leader Winston Peters

- **Stands for:** citizens-first policy, seniors and the regions, opposition to co-governance, and economic interventionism such as
  breaking up big companies ([README](parties/nz-first/README.md); [Wikipedia](https://en.wikipedia.org/wiki/New_Zealand_First)).
- **Headline 2026 policies** ([79 policies](parties/nz-first/policies/README.md)):
  - split the "gentailer" power companies;
  - split Foodstuffs into two cooperatives;
  - buy back BNZ and merge it with Kiwibank;
  - only citizens could vote or receive NZ Super;
  - a $5,000-a-year "Kiwi Kids Grant";
  - a 20% company tax rate for small and medium businesses;
  - binding referendums on the Māori seats and on capping resident visas;
  - repeal the Regulatory Standards Act it voted for.
- **Costings:** no full fiscal plan. The NZ Herald calls it the largest party in Parliament not to publish one
  ([NZ Herald](https://www.nzherald.co.nz/nz/politics/nz-firsts-policies-could-cost-72b-and-that-doesnt-include-buying-back-the-bnz/premium/SMEMEEW25JE7DC4IQPTINQGFYA/)).
  A Green analysis puts its policies at about $71.6b over four years, which NZ First rejects. Estimates of the cost of buying BNZ
  range from $7.5b to $24b (same source).
- **Coalition:** National and ACT only; rules out Labour and will not sit in Cabinet with TOP's leader (see §1).
- **Track record:** delivery index 56% overall. The pattern: what gets into a coalition agreement is usually delivered (the PGF, the
  RIF, keeping super at 65), while the most divisive campaign promises are often traded away and then revived at the next election
  ([track-record.md](parties/nz-first/track-record.md#reliability-scorecard)).

### 2.6 The Opportunity Party (TOP) (centre) – leader Qiulae Wong

- **Stands for:** what it calls "evidence-based" radical centrism. TOP has never been in Parliament
  ([README](parties/opportunity/README.md); [Wikipedia](https://en.wikipedia.org/wiki/Opportunity_Party_(New_Zealand))).
- **Headline 2026 policies** ([77 policies](parties/opportunity/policies/README.md)):
  - a means-tested Citizen's Income of up to $370 a week for most adults, replacing most benefits and NZ Super, funded by a land value tax;
  - a $30,000 donation cap, a lobbying register and an anti-corruption watchdog;
  - a 10-year health plan, with health funding at 9% of GDP;
  - a ban on inshore bottom trawling by 2030;
  - stronger Commerce Commission powers;
  - farming brought into the ETS.

  Its five "non-negotiables" were set out on 30 September ([README](parties/opportunity/README.md#2026-campaign-summary)).
- **Costings:** no full fiscal plan. Its "Tax Reset" says the land tax pays for the Citizen's Income with about $4b a year to spare
  ([TOP PDF](https://cdn.opportunity.org.nz/documents/policy/Opportunity%20Policy%20-%20Tax%20Reset.pdf)). The commentator Grant Duncan argues that
  surplus is largely offset by new borrowing costs ([Substack](https://grantduncanphd.substack.com/p/opportunity-what-does-top-really)).
- **Coalition:** open to either side, but not to a government with Peters as Foreign Minister (see §1).
- **Track record:** none in Parliament. Its best result was 2.44% in 2017 ([MINOR_PARTIES.md](parties/MINOR_PARTIES.md)).

### 2.7 Te Pāti Māori (left-wing) – co-leaders Debbie Ngarewa-Packer and Rawiri Waititi

- **Stands for:** Māori self-determination grounded in Te Tiriti o Waitangi ([README](parties/te-pati-maori/README.md#1-summary)).
- **Strategy:** in 2026 it is asking Māori-roll voters for their electorate vote and telling supporters to give their party vote to
  Labour or the Greens ("one plan, two votes") ([RNZ](https://www.rnz.co.nz/news/politics_election-2026/1011909/te-pati-maori-reveals-election-strategy-as-campaign-launches-in-gisborne)).
- **Headline 2026 policies** ([91 policies](parties/te-pati-maori/policies/README.md)):
  - the "Kiwi Tax Plan": first $30,000 of income tax-free, a 48% rate over $300,000, a wealth tax, and a 33% company rate;
  - GST off kai (food);
  - an independent Te Tiriti Commission and binding Waitangi Tribunal recommendations;
  - a Matike Mai constitution;
  - abolish prisons by 2040;
  - a $1b fund for Māori and community renewable energy.

  Source for the tax plan: [Kiwi Tax Plan PDF](https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf).
- **Costings:** no overall costing found (same PDF).
- **Coalition:** the left bloc only. Its MPs fell from six to four over the term after two expulsions; the High Court found one of
  them unlawful ([README §6](parties/te-pati-maori/README.md#6-the-202526-internal-crisis)).
- **Track record:** delivery index 63% overall and 78% as National's support partner in 2008–17 (Whānau Ora, the UNDRIP endorsement,
  the Māori Language Act). Since 2020 it has been in opposition, and its track record rates its handling of its own internal process
  as "poor" ([track-record.md](parties/te-pati-maori/track-record.md#4-did-it-stick-to-its-word)).

### 2.8 The other ten registered parties

None of these parties is reported separately by the main pollsters. policy.nz lists each at below 0.5%, or gives no figure
([data/guide/parties.json](data/guide/parties.json)). Wikipedia's left–right labels are quoted where it gives one.

| Party (leader) | Wikipedia label / description | Headline 2026 ideas | 2023 party vote | Costed plan? |
|---|---|---|---|---|
| [NZ Loyal](parties/nz-loyal/README.md) (Kelvyn Alp) | far-right | Leave the UN, WHO and WEF; end climate agreements; scrap the tax system; a written constitution | 1.21% | No |
| [NZ Outdoors & Freedom](parties/nz-outdoors-freedom/README.md) (Sue Grey) | "environmentalism with anti-government conspiracy theories" | Make the Bill of Rights supreme law; binding citizens' votes; replace DOC with a "Department of Outdoors"; no 1080 | in Freedoms NZ, 0.34% | No |
| [Legalise Cannabis](parties/legalise-cannabis/README.md) (Maki Herbert, Michael Appleby) | single-issue | Legal regulated R18 cannabis; expunge past convictions; hemp industry | 0.46% | No |
| [Animal Justice](parties/animal-justice/README.md) (Rob McNeil, Danette Wereta) | animal rights | End factory farming; a Commissioner for Animals; "no-kill" pounds | 0.17–0.18%* | No |
| [Alliance](parties/alliance/README.md) (Victor Billot) | left-wing | First $20,000 tax-free funded by a wealth tax, a CGT and a transactions levy; bring power, rail and ports back into public ownership | did not stand | Tax package only |
| [Conservative Party NZ](parties/conservative/README.md) (Helen Houghton) | right-wing | Lower taxes and 12.5% GST; leave the Paris Agreement; personhood for the unborn from the last trimester | 0.15–0.16%* | No |
| [Women's Rights](parties/womens-rights/README.md) (Jill Ovens, Dawn Trenberth) | gender-critical feminism (per Wikipedia's 2026 election article) | Single-sex spaces; extend the puberty-blocker ban to cross-sex hormones for under-18s | 0.08–0.09%* | No |
| [Vision NZ](parties/vision-nz/README.md) (Hannah Tamaki) | far-right | A Ministry for Families; pause mass immigration; first $25,000 tax-free; abolish list MPs | in Freedoms NZ | No |
| [Free Palestine](parties/free-palestine/README.md) (Paul Hopkinson) | single-issue (new in 2026) | One secular democratic state in Palestine; leave military alliances with the US | new | No |
| [Te Tai Tokerau Party](parties/te-tai-tokerau-party/README.md) (Mariameno Kapa-Kingi, sitting MP) | tino rangatiratanga (new in 2026) | A "Mokopuna Act"; write off about $2b of MSD and IRD debt owed by low-income whānau; iwi stakes in regional infrastructure | new | No |

\*Sources differ in the second decimal place (see §8). Party records and cards: [data/guide/parties.json](data/guide/parties.json);
history: [parties/MINOR_PARTIES.md](parties/MINOR_PARTIES.md).

- **Te Tai Tokerau Party:** Kapa-Kingi says she will rule no one out and would take a call from Luxon
  ([1News](https://www.1news.co.nz/2026/05/12/kapa-kingi-talks-plan-for-new-party-after-te-pati-maori-split/)).
- **The other nine:** no statement on post-election partners was found.

---

## 3. Head-to-head on the big issues

**Positions in brief.** These are plain summaries of each party's published 2026 policy. They come from
[data/guide/issues.json](data/guide/issues.json), where each position links to policy ids in `parties/<party>/policies/policies.json`.
The long version, with key facts for every issue, is [guide/issues.md](guide/issues.md). "—" means no 2026 position was found.

| Issue | National | Labour | Green | ACT | NZ First | Te Pāti Māori | TOP |
|---|---|---|---|---|---|---|---|
| **Cost of living** | Split Foodstuffs; hold fuel tax and RUC to 2028; rates rises capped at 2–4% | Outlaw price gouging; supermarkets split wholesale and retail; $20/wk fare cap; freeze fuel tax | KiwiMart; $2 fares; first $10k tax-free | Against supermarket break-up; one-stop consents for new entrants | Split Foodstuffs; +$70/wk Working for Families | GST off food; back Māori food businesses | Stronger Commerce Commission; Citizen's Income |
| **Tax** | No new taxes; further cuts delayed | 28% property CGT (not the family home); no GST rise | Wealth, inheritance and big-company taxes; new top rate; $10k tax-free | No tax on KiwiSaver earnings; landlords can offset losses | 20% company tax for SMEs | $30k tax-free; 48% top rate; wealth tax | Land value tax funding a Citizen's Income |
| **Health** | +$604m Pharmac; wider screening | 3 free GP visits; free prescriptions; ED plan | +$3b a year; free mental health services | Pharmacists treat more; Pharmac >10% of the health budget; PPP cancer centres | GP autonomy; health coaches | Māori health investment | 10-year plan; 9% of GDP |
| **Housing** | 5% deposit loans; faster consents; granny flats | 6,000+ social homes | 2% rent cap; rental WOF; public homes; reverse interest deductibility | Landlords offset losses | Citizens first for social housing | Public homes; 5% stamp duty; vacant-house tax | Zoning reform; land tax against land-banking |
| **Economy & jobs** | Tight spending; double exports by 2034; Investment Boost | NZ Future Fund; $4b build programme; yearly minimum wage rises | Youth job guarantee; default union membership | Cut spending; 3-year minimum-wage freeze; training wage | 20% SME company tax; Marsden Point zone | Māori economy; $1b energy fund | Science funding 2% of GDP |
| **Energy** | Solar and battery loans; dry-year backup | Solar loans and subsidies | Kiwipower; plug-in solar | Against gentailer break-up | Split gentailers; oil and gas exploration | $1b community energy fund | Restructure the electricity market |
| **Welfare** | Drug tests; cuts after 2 years on a benefit; 26-week stand-down | End annual renewals for permanent disability | Raise benefits; universal Best Start | Tighter medical certificates; 5-year wait for new residents | Kiwi Kids Grant; 10-year migrant stand-down | $30k tax-free; GST off food | Citizen's Income replaces benefits |
| **Law & order** | No "good character" discounts for sex offending; affirmative consent; more prison beds | Corporate manslaughter offence; end boot camps | Rehabilitation; coercive control offence; decriminalise cannabis | Three strikes for burglary; deport offenders | Wider deportation grounds; ban public fireworks sales | Abolish prisons by 2040 | More for courts and rehabilitation; decriminalise possession |
| **Climate** | Farm emissions out of the ETS; 50% ocean protection by 2040 | Review the ETS; stay in Paris | Cut gross emissions incl. farming; repeal fast-track | Repeal Zero Carbon; abolish the Climate Commission | More mining, incl. conservation land | Ban seabed mining | Farming into the ETS; $5b resilience fund |
| **Education** | Replace NCEA; compulsory to Year 11; lunches to 2029 | Pause NCEA scrapping; 1,000 teacher aides | Expand lunches; free ECE; fees-free tertiary | Expand charter schools | — | Māori Education Authority | 10-year plan; rebuild lunches |
| **Te Tiriti** | Voted against the Treaty Principles Bill; Luxon open to a Māori-seats referendum | Restore Treaty clauses and iwi participation | Entrench the Māori seats; $200m for te reo | Scale back Treaty principles; close the Tribunal | Māori-seats referendum; replace the Tribunal | Te Tiriti Commission; binding Tribunal | Not support a Treaty Principles bill |
| **Immigration** | Partner visa fast-track; 5-year wait for benefits | Citizenship for children born here; 4-year path to residence | Residency path for migrant workers; higher refugee quota | Visa surcharge; presence test | Shortage-led visas; overstayer amnesty-to-leave | — | — |
| **Retirement** | Compulsory KiwiSaver; Baby Boost | Compulsory employer contributions | 10-year residency for Super | Super age 67 by 2035 | Super for citizens only | — | Compulsory KiwiSaver at 6% |
| **Democracy** | MMP and 4-year-term referendums; costings unit | Same-day enrolment; repeal the RSA; lobbying register | $30k donation cap; no corporate donations | Merge departments; fewer ministers | Citizens-only voting | Te Tiriti Commissioner | Citizens' assemblies; donation cap |

**Where parties agree and disagree, statement by statement.** The quiz in the archive codes each party's public record on 45
neutral statements, from −2 to +2. Every cell has quoted evidence behind it.

<!-- GENERATED:report-quiz START -->
| # | Statement | Nat | Lab | Grn | ACT | NZF | TPM | TOP |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| q01 | New Zealand should introduce a capital gains tax (for example on investment and commercial property). | **−−** | **++** | + | **−−** | · | · | · |
| q02 | There should be an annual wealth tax on people with very large fortunes (for example net wealth over $2–10 million). | **−−** | **−−** | **++** | **−−** | − | **++** | · |
| q03 | GST should be removed from food such as fresh fruit and vegetables. | · | · | · | · | · | + | · |
| q04 | The first slice of everyone's income (e.g. the first $10,000 or more) should be tax-free. | · | · | **++** | · | **++** | **++** | · |
| q05 | The government should force the big supermarket chains to be broken up or restructured to increase competition. | + | **++** | **++** | **−−** | **++** | · | + |
| q06 | The minimum wage should rise every year by at least the rate of inflation. | · | **++** | **++** | **−−** | **++** | **++** | · |
| q07 | Fair Pay Agreements (industry-wide minimum pay and conditions negotiated by unions and employers) should be brought back. | **−−** | **++** | **++** | **−−** | **−−** | **++** | − |
| q08 | Annual rent increases should be capped by law. | − | − | **++** | **−−** | · | · | · |
| q09 | The government should build a lot more state and public housing. | − | **++** | **++** | − | · | **++** | · |
| q10 | Councils should have to allow more and denser housing, such as townhouses and apartments, in our cities. | **++** | · | + | **++** | · | · | **++** |
| q11 | Some GP visits each year should be free for everyone. | − | **++** | **++** | · | · | · | · |
| q12 | The $5 prescription charge should be scrapped. | − | **++** | · | · | · | · | · |
| q13 | Free school lunches should be expanded and made more generous, even if it costs more. | · | **++** | **++** | · | · | · | **++** |
| q14 | Charter (partnership) schools should be allowed to continue. | · | **−−** | **−−** | **++** | · | · | · |
| q15 | University and polytechnic study should be fees-free. | − | − | **++** | · | · | · | · |
| q16 | Repeat serious offenders should face mandatory longer sentences under a "three strikes" law. | **++** | **−−** | **−−** | **++** | **++** | **−−** | · |
| q17 | We should send fewer people to prison and put more into rehabilitation and community alternatives. | − | · | **++** | − | · | **++** | **++** |
| q18 | Farmers should pay for their greenhouse gas emissions, for example by bringing agriculture into the Emissions Trading Scheme. | **−−** | − | **++** | **−−** | **−−** | **++** | + |
| q19 | New Zealand should keep its legal net-zero 2050 target and stay in the Paris Agreement. | · | **++** | **++** | **−−** | **−−** | · | **++** |
| q20 | Ministers should be able to fast-track big infrastructure, mining and development projects past the normal consent process. | **++** | − | **−−** | **++** | **++** | **−−** | − |
| q21 | Seabed mining should be banned in New Zealand waters. | **−−** | **++** | **++** | **−−** | **−−** | **++** | **++** |
| q22 | The ban on new offshore oil and gas exploration should be brought back. | **−−** | **++** | **++** | **−−** | **−−** | **++** | 0 |
| q23 | The government should take a bigger direct role in electricity, such as a new state-owned power company or splitting up the big power companies. | − | · | **++** | **−−** | **++** | · | + |
| q24 | Parliament should define the principles of the Treaty of Waitangi in law, as ACT's Treaty Principles Bill proposed. | **−−** | **−−** | **−−** | **++** | − | **−−** | · |
| q25 | The Waitangi Tribunal should be abolished or replaced once historical claims are settled. | · | · | **−−** | **++** | **++** | **−−** | · |
| q26 | The Māori electorates should be abolished, or their future put to a referendum. | · | · | **−−** | · | **++** | · | · |
| q27 | Government services should be allocated by need alone, without Māori- or ethnicity-specific programmes. | · | − | **−−** | **++** | + | **−−** | · |
| q28 | The Regulatory Standards Act 2025 should be repealed. | **−−** | **++** | **++** | **−−** | 0 | **++** | **++** |
| q29 | Political donations should be capped, with only New Zealand voters allowed to donate. | · | 0 | **++** | · | 0 | **++** | **++** |
| q30 | Central government should cap how much councils can raise rates each year. | **++** | 0 | **−−** | · | · | · | − |
| q31 | Overall immigration to New Zealand should be reduced. | · | · | − | · | **++** | · | · |
| q32 | New residents should have to wait longer (five years or more) before they can get most benefits. | **++** | · | · | **++** | **++** | · | · |
| q33 | The age of eligibility for NZ Superannuation should stay at 65. | − | **++** | **++** | **−−** | **++** | **++** | **++** |
| q34 | Main benefits should be substantially increased. | − | · | **++** | − | · | + | + |
| q35 | Beneficiaries should face tougher obligations and sanctions, such as drug tests or payment cuts. | **++** | · | **−−** | **++** | · | **−−** | **−−** |
| q36 | Transport money should go mainly to public transport and rail rather than new highways. | **−−** | + | **++** | **−−** | + | · | **++** |
| q37 | Rules limiting farm pollution of rivers (such as nitrogen limits) should be strengthened rather than loosened. | **−−** | + | **++** | **−−** | **−−** | **++** | + |
| q38 | Rules on gene technology (genetic modification) should be relaxed. | **++** | − | **−−** | **++** | − | **−−** | **++** |
| q39 | New Zealand should formally recognise the State of Palestine now. | − | **++** | **++** | · | − | · | · |
| q40 | Defence spending should rise substantially, towards 2% of GDP. | **++** | · | − | + | · | **−−** | · |
| q41 | New Zealand should increase its overseas aid budget. | · | **++** | **++** | **−−** | · | · | · |
| q42 | Cannabis should be legalised or decriminalised for personal use. | · | · | **++** | · | · | · | **++** |
| q43 | Children under 16 should be banned from social media. | **++** | + | · | **−−** | **−−** | · | + |
| q44 | Puberty blockers and other medical gender-transition treatments should not be available to under-18s. | **++** | · | **−−** | · | **++** | · | · |

++ strongly agree · + agree · 0 neutral/mixed · − disagree · −− strongly disagree · "·" no public position found (never guessed). Every cell has a quoted piece of evidence and a source URL in [`data/guide/quiz.json`](data/guide/quiz.json); coding rules in [guide/quiz-method.md](guide/quiz-method.md). Statements on which none of the seven has a recorded position are omitted.
<!-- GENERATED:report-quiz END -->

Points that stand out in that table:

- **Some agreement crosses the bloc line.**
  - Supermarket restructuring (q05): National, Labour, the Greens, NZ First and TOP all support some form of it.
  - Denser housing (q10): National, ACT, TOP and the Greens support it.
  - A capital gains tax (q01): Labour and the Greens support one; National and ACT strongly oppose it.
- **The sharpest splits** are on the Treaty Principles Bill (q24: only ACT supports it), three strikes (q16), fast-track (q20), farm
  emissions pricing (q18), the RSA repeal (q28) and the super age (q33: only ACT and National are against keeping 65).
- **Coverage is uneven.** The seven parties have between 22 and 40 positions recorded each, and the smaller parties have far fewer
  ([quiz-method.md §4](guide/quiz-method.md#4-limitations)).

---

## 4. Reliability and promise-keeping

### 4.1 Method: one standard for every party

The archive tracks **329 promises across eight parties** in [data/promises/](data/promises/). Each one has a verdict: *kept*,
*partially kept*, *broken*, *abandoned*, *in progress* or *not yet due*. Every entry carries sources and a `detail` field explaining
the verdict. This report recomputes every party's figures from those files using the same rules:

1. **Only resolved promises are scored.** Resolved means kept + partly kept + broken + abandoned. In-progress items (mostly from the
   current term) and 2026 pledges are left out of every percentage.
2. **Delivery index = (kept + ½ × partly kept) ÷ resolved.** This is the formula the ACT and NZ First pages already used
   ([ACT](parties/act/track-record.md#reliability-scorecard)); here it is applied to everyone. The kept % and the kept-or-partly % are
   shown alongside it.
3. **Role matters.** Each promise is assigned to the term it was meant for. That term is classed as *in office* (leading or in
   coalition), *support partner* (confidence and supply, or a cooperation agreement), or *opposition / out of Parliament*.
   - A party cannot deliver from opposition. Promises from lost campaigns are therefore nearly all "abandoned": their only test is
     whether the party kept advocating them.
   - The fairest comparison of reliability is the **in-office and support-partner columns** of the second table.

<!-- GENERATED:report-promises-overall START -->
| Party | Entries | Kept | Partly kept | Broken | Abandoned | In progress | Not yet due (2026) | Resolved | Kept % | Kept or partly % | Delivery index |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| [National](parties/national/track-record.md) | 82 | 35 | 11 | 5 | 10 | 10 | 11 | 61 | 57% | 75% | 66% |
| [Labour](parties/labour/track-record.md) | 92 | 36 | 10 | 7 | 18 | 0 | 21 | 71 | 51% | 65% | 58% |
| [Green](parties/green/track-record.md) | 32 | 11 | 4 | 6 | 1 | 0 | 10 | 22 | 50% | 68% | 59% |
| [ACT](parties/act/track-record.md) | 38 | 18 | 4 | 5 | 6 | 0 | 5 | 33 | 55% | 67% | 61% |
| [NZ First](parties/nz-first/track-record.md) | 50 | 21 | 3 | 7 | 9 | 3 | 7 | 40 | 52% | 60% | 56% |
| [Te Pāti Māori](parties/te-pati-maori/track-record.md) | 21 | 8 | 3 | 3 | 1 | 0 | 6 | 15 | 53% | 73% | 63% |
| [United Future](parties/united-future/track-record.md) | 10 | 9 | 1 | 0 | 0 | 0 | 0 | 10 | 90% | 100% | 95% |
| [Mana](parties/mana/track-record.md) | 4 | 2 | 0 | 1 | 1 | 0 | 0 | 4 | 50% | 50% | 50% |

All entries in [`data/promises/`](data/promises/). Percentages are of *resolved* entries (kept + partly + broken + abandoned). Delivery index = (kept + ½ partly kept) ÷ resolved. Includes promises from campaigns a party lost, which are mostly "abandoned" – see the next table.
<!-- GENERATED:report-promises-overall END -->

<!-- GENERATED:report-promises-role START -->
| Party | In office (govt or coalition): resolved / index | As support partner: resolved / index | Opposition or out of Parliament: resolved / index | Long-standing / undated: resolved |
|---|---|---|---|---|
| National | 56 / **72%** (35✅ 11🟡 5❌ 5⛔) | – | 5 / **0%** (0✅ 0🟡 0❌ 5⛔) | – |
| Labour | 61 / **67%** (36✅ 10🟡 7❌ 8⛔) | – | 10 / **0%** (0✅ 0🟡 0❌ 10⛔) | – |
| Green | – | 15 / **67%** (8✅ 4🟡 3❌ 0⛔) | 3 / **33%** (1✅ 0🟡 1❌ 1⛔) | 4 |
| ACT | 22 / **64%** (12✅ 4🟡 3❌ 3⛔) | 5 / **60%** (3✅ 0🟡 1❌ 1⛔) | 5 / **40%** (2✅ 0🟡 1❌ 2⛔) | 1 |
| NZ First | 38 / **59%** (21✅ 3🟡 6❌ 8⛔) | – | 2 / **0%** (0✅ 0🟡 1❌ 1⛔) | – |
| Te Pāti Māori | – | 9 / **78%** (6✅ 2🟡 1❌ 0⛔) | 5 / **30%** (1✅ 1🟡 2❌ 1⛔) | – |
| United Future | – | 10 / **95%** (9✅ 1🟡 0❌ 0⛔) | – | – |
| Mana | – | – | 4 / **50%** (2✅ 0🟡 1❌ 1⛔) | – |

Each entry is assigned to the parliamentary term following the election or agreement at which the promise was made (from its `made` field; Labour's file also has a `term` field, used where present). Roles: National led governments 2008–17 and 2023–26; Labour 2017–23; ACT and the Māori Party were National's support partners 2008–17 and ACT a coalition partner from 2023; United Future a support partner 2008–17; the Greens a support partner 2017–23 (confidence & supply, then a cooperation agreement); NZ First a coalition partner 2017–20 and 2023–26. Sources: party READMEs and `government` in [`data/elections/`](data/elections/).
<!-- GENERATED:report-promises-role END -->

<!-- GENERATED:report-promises-terms START -->
| Party | 2008–11 | 2011–14 | 2014–17 | 2017–20 | 2020–23 | 2023–26 | 2026 (not yet due) |
|---|---|---|---|---|---|---|---|
| National | 2/0/1/0 *(govt)* | 2/4/0/0 *(govt)* | 3/1/0/0 *(govt)* | 0/0/0/3 *(opp)* | 0/0/0/2 *(opp)* | 28/6/4/5 +10⏳ *(govt)* | 11 |
| Labour | · *(opp)* | 0/0/0/4 *(opp)* | 0/0/0/3 *(opp)* | 22/9/4/3 *(govt)* | 14/1/3/5 *(govt)* | 0/0/0/3 *(opp)* | 21 |
| Green | · *(opp)* | · *(opp)* | · *(opp)* | 6/4/2/0 *(support)* | 2/0/1/0 *(support)* | 1/0/1/1 *(opp)* | 10 |
| ACT | · *(support)* | 1/0/0/1 *(support)* | 2/0/1/0 *(support)* | 1/0/0/0 *(opp)* | 1/0/1/2 *(opp)* | 12/4/3/3 *(govt)* | 5 |
| NZ First | · *(out)* | 0/0/0/1 *(opp)* | 0/0/1/0 *(opp)* | 8/2/5/3 +1⏳ *(govt)* | · *(out)* | 13/1/1/5 +2⏳ *(govt)* | 7 |
| Te Pāti Māori | 4/2/0/0 *(support)* | · *(support)* | 2/0/1/0 *(support)* | 0/0/1/0 *(out)* | 1/1/1/0 *(opp)* | 0/0/0/1 *(opp)* | 6 |
| United Future | 3/0/0/0 *(support)* | 5/1/0/0 *(support)* | 1/0/0/0 *(support)* | · *(out)* | · *(out)* | · *(out)* | – |
| Mana | · *(out)* | 0/0/1/1 *(opp)* | 1/0/0/0 *(out)* | 1/0/0/0 *(out)* | · *(out)* | · *(out)* | – |

Cells: kept / partly kept / broken / abandoned (+ in progress ⏳); role in that term in italics. "·" = no tracked promises for that term. The last column counts every entry with status not-yet-due (including a few 2023 promises carried into 2026 platforms). A few entries without a datable election (e.g. "long-standing policy") are omitted from this table but counted above.
<!-- GENERATED:report-promises-terms END -->

### 4.2 Caveats: read before comparing the numbers

- **Different sample sizes.** National (82 entries) and Labour (92) have far more tracked promises than Te Pāti Māori (21), the
  Greens (32) or Mana (4). United Future's 95% rests on ten negotiated items and nothing else. Small samples swing on one or two
  verdicts.
- **Selection.** Each file tracks the high-profile, checkable promises: pledge cards, flagship policies, 100-day plans and coalition
  agreements. None covers every manifesto line. The National file notes that adding the many small, low-profile promises would raise
  "kept" shares ([National caveats](parties/national/track-record.md#how-to-read-the-verdicts)). Labour's file says counts "would shift
  somewhat with a different selection" ([Labour method](parties/labour/track-record.md#10-method-and-caveats)).
- **Easy and hard promises.** Promises to repeal, legislate or pay out can almost always be delivered by a government with a majority.
  Promises about outcomes, such as surpluses, waiting times, homes built or child poverty, depend on the economy and on delivery
  capacity. Both major-party files find the same split:
  - Labour kept about 71% of its law and transfer promises outright, but only 2 of 13 build or outcome targets
    ([Labour §6](parties/labour/track-record.md#by-type-of-promise)).
  - About half of National's 2023–26 "kept" verdicts are repeals, while its misses are mostly outcomes
    ([National summary](parties/national/track-record.md#summary)).
  - So a government that mostly promises repeals will tend to score higher.
- **Government vs opposition vs support role.** Support partners such as the Greens, ACT 2008–17, the Māori Party and United Future
  promise less, and they bargain for specific items that can be written into an agreement. Their high rates partly reflect that.
- **Coalition constraints.**
  - Under MMP every government since 1996 has needed partners ([trends](elections/trends.md)).
  - NZ First blocked or diluted at least six Labour policies in 2017–20, including the CGT, the three-strikes repeal and light rail
    ([NZ First alignment](parties/nz-first/track-record.md#alignment-actions-vs-stated-policies-and-the-kingmaker-role)).
  - National lost its foreign-buyer tax and its super-age change to NZ First in 2023
    ([National README](parties/national/README.md#periods-in-government-and-arrangements)).
  - The National and Labour files mark promises lost in coalition talks as *abandoned*, not *broken*, and name the partner involved.
- **The files define "broken" slightly differently.**
  - National and Labour count a promise as broken only if it was missed "while in a position to deliver".
  - The ACT, NZ First, Green and Te Pāti Māori files count any non-delivery as broken, "whatever the reason", and explain the reason in
    `detail` ([Green how-to-read](parties/green/track-record.md#how-to-read-this)).
  - The effect is to make the smaller parties' broken counts slightly harsher. The kept and delivery-index figures are not affected.
- **External shocks.** Several records were hit by events outside the government's control:
  - the 2008–09 global financial crisis and the Canterbury earthquakes (Key);
  - COVID-19, then 7.3% inflation in 2022 (Ardern and Hipkins)
    ([Labour §3](parties/labour/track-record.md#3-covid-19-response));
  - the 2024 recession and the 2026 Middle East oil shock (Luxon) ([National caveats](parties/national/track-record.md#how-to-read-the-verdicts)).
- **Durability is a separate question.** At least 15 promises Labour kept were reversed by the 2023–26 coalition
  ([Labour durability](parties/labour/track-record.md#durability-what-survived-the-change-of-government)). ACT's charter schools and
  three strikes had been reversed by Labour in the past ([ACT trends](parties/act/track-record.md#trends-2011--2026)). A reversal does
  not change a "kept" verdict.
- **Other trackers differ.** The volunteer NZ Politics Promise Tracker lists 45 National promises: 23 kept, 18 in progress and 1
  broken. This archive finds more broken and partial verdicts, because it scores outcome promises
  ([National summary](parties/national/track-record.md#summary); [tracker](https://www.nzpoliticspromisetracker.nz/parties)).

**What the numbers do and don't show.** Measured in office or as a support partner, the six current parliamentary parties' delivery
indices fall in a fairly narrow band, about 59–78%. United Future, on ten items, is higher. That gap is small compared with the
uncertainty from selection and sample size. The clearer differences are in *what kind* of promise each party misses, set out below.

### 4.3 Where actions diverged from stated values: U-turns by party

Every party has some. The lists below are summaries of the "alignment" and "U-turn" sections of each track record, which give a
source for every item.

**National** ([full table](parties/national/track-record.md#notable-u-turns-and-changed-positions))
- GST: "not going to be raising GST" (2008), then raised it to 15% (2010)
  ([ODT](https://www.odt.co.nz/news/politics/key-ruled-out-gst-increase-2008)).
- Fees-free: promised to scrap it (2019–20), then to keep it (2023), then moved it to the final year in coalition, then abolished it
  in Budget 2026.
- KiwiSaver: halved the government contribution (2025), said it would "remain voluntary" (Nov 2025), then promised **compulsory**
  KiwiSaver (2026).
- Super age: Key said it would never rise; English proposed 67 (2017); National proposed 67 again (2023); dropped in coalition.
- Fiscal prudence versus outcomes: promised a surplus in 2026/27; it is now forecast for 2028/29, on a new OBEGALx measure. Net debt
  is forecast to peak at 43.9% of GDP, above National's own 40% ceiling
  ([RNZ](https://www.rnz.co.nz/news/politics_election-2026/1647005/treasury-gives-willis-pre-election-boost-as-surplus-forecast-improves)).
- Major changes passed under urgency without a campaign mandate: the smokefree repeal and the Equal Pay Amendment Act 2025, which
  cancelled 33 pay-equity claims ([Wikipedia](https://en.wikipedia.org/wiki/Equal_Pay_Amendment_Act_2025)).

**Labour** ([full list](parties/labour/track-record.md#notable-u-turns))
- Capital gains tax:
  - promised in 2011 and 2014, then dropped (2015);
  - ruled out in 2019 and in 2023 ("end of story"), against its own working group's or minister's advice;
  - promised again in 2025 ([1News](https://www.1news.co.nz/2023/07/12/end-of-story-hipkins-rules-out-wealth-and-capital-gains-taxes)).
- Bright-line test: ruled out an extension in the 2020 campaign, then extended it five months later
  ([Newshub](https://newshub.co.nz/home/politics/2021/03/finance-minister-grant-robertson-admits-being-too-definitive-in-ruling-out-bright-line-extension-during-election.html)).
- KiwiBuild: the 100,000-home target was scrapped in 2019 ([Spinoff](https://thespinoff.co.nz/politics/04-09-2019/cheat-sheet-megan-woods-hits-reset-on-the-beleaguered-kiwibuild-programme/)).
- Three Waters: presented as optional, then made mandatory (2021).
- The 2023 "policy bonfire" of its own programme ([Spinoff](https://thespinoff.co.nz/politics/24-04-2023/purged-punted-and-pruned-the-chris-hipkins-reprioritisation-in-full)).
- Interest deductibility: removed it, then opposed its restoration, then ruled out changing it again (Sept 2026)
  ([1News](https://www.1news.co.nz/2026/09/21/labour-rules-out-interest-deductibility-changes-for-landlords/)).

**Green** ([actions vs values](parties/green/track-record.md#5-actions-vs-values))
- Waka-jumping: voted for the waka-jumping law (2018) under the support agreement, voted to repeal it (2020–21), then used it to expel
  Darleen Tana (2024).
- Green School: an $11.7m grant to a private school (2020), against the party's policy. The party admitted the breach and the grant
  became a loan.
- Conduct of individual MPs: the Ghahraman convictions; the Tana and Genter findings.
- Wealth tax: the 2020 wealth tax and the 2023 Guaranteed Minimum Income were scaled back; the wealth-tax threshold rose from $2m to
  $10m for 2026.

**ACT** ([alignment](parties/act/track-record.md#alignment-did-acts-actions-match-its-stated-principles))
- Treaty referendum: described as a coalition "condition" in 2022, then dropped in 2023.
- Free expression: voted for the gang-patch ban despite its free-expression principles.
- Law-making process: champions careful law-making through the Regulatory Standards Act, yet the pay-equity changes, led by its own
  minister, passed under urgency without a select-committee stage.
- Public service: the promise to return it to its 2017 size was missed. FTEs in June 2026 (63,912) were about where they were in 2023.
- Immigration: moved from liberalising (2023) to restrictive (2026).

**NZ First** ([alignment](parties/nz-first/track-record.md#alignment-actions-vs-stated-policies-and-the-kingmaker-role))
- Regulatory Standards Act: voted it through all its stages (Nov 2025), then pledged a week later to repeal it.
- Oil and gas: part of the government that banned offshore exploration in 2018, then repealed the ban in 2025.
- Public Service Act: helped pass its diversity provisions in 2020, then moved to remove them in 2025.
- Fees-free: won its move to the final year, then agreed to scrap it.
- Historic: campaigned against National in 1996 and then went into government with it.

**Te Pāti Māori** ([actions vs kaupapa](parties/te-pati-maori/track-record.md#5-actions-vs-kaupapa))
- Foreshore and seabed: accepted the 2011 compromise that replaced the 2004 Act, which its own founder criticised.
- General seats: announced it would stand in general seats (April 2025), then stood only in Māori seats.
- Internal process: the High Court found its expulsion of Kapa-Kingi unlawful.
- Donations: disclosed 2020 donations late, a breach of electoral-finance rules. No prosecution followed.

**United Future and Mana** (historical): United Future's two signature policies, income splitting and "flexi-super", got only
procedural wins ([UF](parties/united-future/track-record.md#assessment)). Mana's Internet Party alliance raised its party vote but cost
Harawira his seat ([Mana](parties/mana/track-record.md#assessment)).

---

## 5. Performance in government, 2008–26

This section uses only outcomes already sourced in the archive. Economists disagree about how far any government can be credited or
blamed for growth, inflation or house prices. Where the archive records a dispute, it is noted.

### 5.1 2008–17: the Fifth National Government (Key, then English)

Arrangement: National ruled as a minority government with confidence-and-supply deals with ACT, United Future and the Māori Party in
all three terms ([National README](parties/national/README.md#periods-in-government-and-arrangements)).

| Area | What happened | Source |
|---|---|---|
| Fiscal | Steered through the GFC and the Canterbury earthquakes. Returned to a narrow OBEGAL surplus of $414m (0.2% of GDP) in 2014/15 | [Treasury](https://www.treasury.govt.nz/publications/year-end/financial-statements-government-new-zealand-year-ended-30-june-2015) |
| Tax | 2010 "tax switch": GST up from 12.5% to 15%, top income tax rate down from 38% to 33% | [ODT](https://www.odt.co.nz/news/politics/key-ruled-out-gst-increase-2008); [track record](parties/national/track-record.md) |
| Assets | Partly sold three power companies and part of Air NZ, raising about $4.7b against the $5–7b signalled. A 2013 referendum was 67.3% opposed (45.1% turnout) | [Wikipedia](https://en.wikipedia.org/wiki/Mixed-ownership_model); [track record](parties/national/track-record.md) |
| Christchurch | Major Crown rebuild. Several anchor projects ran years late and over budget (Parakiore opened Dec 2025 at about double its budget) | [OAG](https://oag.parliament.nz/2015/christchurch-projects/part2.htm); [ODT](https://www.odt.co.nz/star-news/star-christchurch/parakiore-set-open-after-decade-costly-delays) |
| Housing | The Auckland Housing Accord reached about 96% of its 39,000-consent target. Critics noted that affordability worsened sharply over the period | [RNZ](https://amp.rnz.co.nz/article/bd934b98-9df0-4177-ac94-da764d13135a); [Greater Auckland](https://www.greaterauckland.org.nz/2017/05/09/auckland-housing-accord-sham-shalvation/) |
| Health & families | Free GP visits for under-13s (2015); paid parental leave extended to 18 weeks; Budget 2015 hardship package of $790m, including a benefit rise for families with children | [Wikipedia](https://en.wikipedia.org/wiki/Fifth_National_Government_of_New_Zealand) |
| Welfare | Seven main benefits merged into three, with stronger work tests (2013) | [Wikipedia](https://en.wikipedia.org/wiki/Fifth_National_Government_of_New_Zealand) |
| Support partners | Māori Party: Whānau Ora, the UNDRIP endorsement, the Māori Language Act 2016. United Future: Kiwibank and RNZ not sold; a 49% cap on asset sales | [TPM record](parties/te-pati-maori/track-record.md); [UF record](parties/united-future/track-record.md) |

Promise record: 13 resolved Key/English-era promises, 54% kept and 8% broken
([National scorecard](parties/national/track-record.md#summary)).

### 5.2 2017–23: the Sixth Labour Government (Ardern, then Hipkins)

Arrangement: in 2017–20, a coalition with NZ First plus Green confidence and supply. In 2020–23, a Labour majority with a Green
cooperation agreement ([Labour README](parties/labour/README.md#government-periods-20082026)).

| Area | What happened | Source |
|---|---|---|
| Incomes | Families Package (2018); minimum wage raised from $15.75 to $20; 26 weeks' paid parental leave; 10 sick days; Matariki holiday | [Beehive](https://www.beehive.govt.nz/sites/default/files/2017-12/Families%20Package%20Factsheet.pdf); [Wikipedia](https://en.wikipedia.org/wiki/Sixth_Labour_Government_of_New_Zealand) |
| Housing | Foreign-buyer ban; Healthy Homes standards; net +10,037 public homes from Oct 2017 to June 2022 (how they were counted is disputed). **KiwiBuild's 100,000-home target was scrapped**; house prices hit records in 2021 | [Law Society](https://www.lawsociety.org.nz/news/newsroom/ban-on-most-foreign-buyers-of-existing-homes-passed/); [Spinoff](https://thespinoff.co.nz/politics/04-09-2019/cheat-sheet-megan-woods-hits-reset-on-the-beleaguered-kiwibuild-programme/); [track record](parties/labour/track-record.md) |
| Transport | Auckland light rail was promised twice; no track was laid and the project was cancelled in Jan 2024 | [track record](parties/labour/track-record.md#2c-transport-and-infrastructure) |
| Child poverty | Child Poverty Reduction Act 2018. Two of three first-period targets were met; material hardship rose again in 2022/23 | [MSD](https://msd.govt.nz/about-msd-and-our-work/child-wellbeing-and-poverty-reduction/progress-targets.html); [track record](parties/labour/track-record.md#7-did-actions-match-stated-values-alignment-and-u-turns) |
| COVID-19 | Among the lowest death rates in the developed world. The Royal Commission found the response "broadly effective but flawed". The wage subsidy paid out $13b+ in 2020; the Auditor-General found "much to commend" | [1News](https://www.1news.co.nz/2024/11/28/first-phase-of-royal-commission-of-inquiry-into-covid-19-released/); [Spinoff](https://thespinoff.co.nz/politics/10-03-2026/covid-19-inquiry-makes-final-findings-on-spending-mandates-and-lockdowns); [OAG](https://oag.parliament.nz/2021/wage-subsidy/overview.htm) |
| Inflation | Peaked at 7.3% in the year to June 2022, a 32-year high (economists differ on how much was domestic) | [1News](https://1news.co.nz/2022/07/18/inflation-rises-to-73-a-32-year-high/) |
| Health | Health NZ replaced the 20 DHBs in 2022. It ran a $722m deficit in 2023/24 | [Wikipedia](https://en.wikipedia.org/wiki/Pae_Ora_(Healthy_Futures)_Act_2022) |
| Police, regions | The "1,800 new police" target was declared met on graduates, but the net increase was about 1,000. The PGF allocated about $3b; its job claims were contested | [1News](https://www.1news.co.nz/2019/11/21/government-celebrates-hitting-target-of-1800-new-cops-but-not-all-are-convinced/); [1News](https://www.1news.co.nz/2019/05/08/jobs-created-by-provincial-growth-fund-may-not-be-quite-what-they-seem) |
| Climate | Zero Carbon Act; offshore oil and gas exploration ban; 2030 target raised to a 50% net cut | [Wikipedia](https://en.wikipedia.org/wiki/Sixth_Labour_Government_of_New_Zealand) |
| Migration | Promised a cut of 20,000–30,000 a year. Instead net migration hit a record of about 91,700 before COVID | [Newsroom](https://www.newsroom.co.nz/2017/10/19/54611/big-policy-changes-ahead-for-labour-led-government) |

Promise record in office: 61 resolved, delivery index 67% (§4). The 2020–23 majority term was no more reliable than the coalition
term: the kept rate went from 58% to 61% while Labour's own abandonments rose
([Labour trends](parties/labour/track-record.md#8-trends)). The 2023 election was "the largest defeat of a sitting government under
MMP" ([trends §4](elections/trends.md#4-the-two-party-vote-and-swing)).

### 5.3 2023–26: the Sixth National Government (National–ACT–NZ First coalition, Luxon)

Arrangement: two coalition agreements, one with ACT and one with NZ First. The deputy prime ministership rotated from Peters to Seymour
on 31 May 2025. Partners used "agree to disagree" clauses several times
([National README](parties/national/README.md#periods-in-government-and-arrangements)).

| Area | What happened | Source |
|---|---|---|
| Legislation | Repealed Fair Pay Agreements, Three Waters, the RMA replacement laws, the Clean Car Discount, smokefree generation and the oil and gas ban. Passed the Fast-track Approvals Act 2024, Local Water Done Well and the Regulatory Standards Act 2025. Many changes were made under urgency | [elections/2026.md](elections/2026.md#the-record-being-judged-the-54th-parliament-202326) |
| Tax | Income-tax relief from July 2024 averaging $3.7b a year, reaching about 83% of taxpayers. Few households received the advertised "up to $250 a fortnight" | [1News](https://www.1news.co.nz/2024/05/30/budget-2024-tax-cuts-wont-cause-borrowing-or-inflation-willis/); [ODT](https://www.odt.co.nz/news/national/fewer-50-families-get-nationals-full-tax-package-says-ctu) |
| Inflation & growth | Inflation fell from 5.6% (Sept 2023) to 2.2% (Sept 2024), then rose to 3.7% (Sept 2026), with petrol the main driver. Recession for much of 2024. Unemployment 5.6% (June 2026), the highest since 2015. Annual growth to June 2026: see §8 for conflicting figures | [track record](parties/national/track-record.md); [Stats NZ](https://www.stats.govt.nz/information-releases/consumers-price-index-september-2026-quarter/); [1News](https://www.1news.co.nz/2026/08/05/nzs-unemployment-rate-hits-11-year-high-in-june-quarter/) |
| Fiscal | The promised 2026/27 surplus was missed; Treasury now forecasts a surplus in 2028/29 on the OBEGALx measure. Budget 2024 added about $12b of borrowing. Net debt is forecast to peak at 43.9% of GDP | [1News](https://www.1news.co.nz/2025/12/16/govt-pushes-out-surplus-expectations-again/); [Newshub](https://newshub.co.nz/home/politics/2024/05/budget-2024-jenna-lynch-analysis-the-as-advertised-budget-brings-tax-cuts-for-most-but-who-s-left-behind.html); [RNZ](https://www.rnz.co.nz/news/politics_election-2026/1647005/treasury-gives-willis-pre-election-boost-as-surplus-forecast-improves) |
| Health | Short-stay ED and elective-surgery targets are improving but remain well below 95% (exact figures differ by source; see §8). Hospital beds per 1,000 people fell from 2.7 (2014) to 2.5 (2024) | [b2bnews](https://b2bnews.co.nz/news/nz-health-targets-improve-but-ed-waits-stay-stuck/); [1News](https://www.1news.co.nz/2026/09/30/new-zealands-emergency-departments-in-crisis-report-says/) |
| Crime | Gang-patch ban, three strikes, military-style academies. The violent-crime-victim and serious-youth-offending targets were met early (829 young offenders against a target of 900). The 500-extra-police deadline was missed. 11,240 people were in prison (Feb 2026), projected to reach 15,200 by 2036 | [RNZ](https://www.rnz.co.nz/news/politics/613970/pm-christopher-luxon-s-public-sector-targets-the-hits-and-misses-in-latest-update); [1News](https://www.1news.co.nz/2025/05/13/govt-concedes-itll-likely-miss-november-target-for-500-new-police); [Justice](https://www.justice.govt.nz/about/news-and-media/media-releases/justice-sector-projections-released-june-2026/) |
| Housing | Households in emergency housing were cut to 471, beating the 2030 target early (eligibility was also tightened). Median house price $755,000 (Sept 2026), down 2.3% on a year earlier | [RNZ](https://www.rnz.co.nz/news/politics/613970/pm-christopher-luxon-s-public-sector-targets-the-hits-and-misses-in-latest-update); [REINZ via Property Brokers](https://www.propertybrokers.co.nz/news/measured-national-picture-continues-alongside-strong-regional-results-reinz-stats-september-2026) |
| Child poverty | Child material hardship 14.3% in the year to June 2025, the highest since 2015. The interim target was loosened | [1News](https://www.1news.co.nz/2026/02/26/unacceptable-childrens-commissioner-says-child-poverty-progress-has-stalled); [RNZ](https://rnz.co.nz/news/political/523167/minister-defends-lowered-child-poverty-targets-as-achievable) |
| Education | Phone ban, structured literacy and an hour a day each of reading, writing and maths. Regular attendance 64.3% (target 80%). Fees-free was scrapped in Budget 2026 | [DPMC](https://www.dpmc.govt.nz/sites/default/files/2026-09/gt-factsheet-target-6-jun26.pdf); [track record](parties/national/track-record.md) |
| Public service | Headcount down 4.6% (Dec 2023 – June 2025), then up 2.0% in the year to June 2026 | [Public Service Commission](https://www.publicservice.govt.nz/data/workforce-data/public-sector-composition/workforce-size); [track record](parties/national/track-record.md) |
| Climate | Net-zero 2050 kept. The methane target was cut to 14–24%. The first two emissions budgets are reported on track | [National](https://www.national.org.nz/news/20251012-hon-todd-mcclay-government-sets-methane-targets-for-2050); [track record](parties/national/track-record.md) |
| Treaty | ACT's Treaty Principles Bill was voted down 112–11 (April 2025) after the November 2024 hīkoi | [1News](https://www.1news.co.nz/2025/04/10/treaty-principles-bill-voted-down-amid-fiery-mp-debate) |
| Regions | NZ First's $1.2b Regional Infrastructure Fund had paid out only $153m by 31 July 2026 | [NZ First README](parties/nz-first/README.md#in-government-20232026) |

Promise record so far: National 2023–26 has 28 kept, 6 partly kept, 4 broken, 5 abandoned and 10 in progress. ACT and NZ First's
2023–26 counts are in §4.

---

## 6. Trends, 2011–2026

### 6.1 Vote share and seats

<!-- GENERATED:report-votes START -->
| Party | 2008 | 2011 | 2014 | 2017 | 2020 | 2023 | Oct 2026 polls |
|---|---:|---:|---:|---:|---:|---:|---:|
| National | 44.9 (58) | 47.3 (59) | 47.0 (60) | 44.5 (56) | 25.6 (33) | 38.1 (49) | 28.7 |
| Labour | 34.0 (43) | 27.5 (34) | 25.1 (32) | 36.9 (46) | 50.0 (65) | 26.9 (34) | 27.9 |
| Green | 6.7 (9) | 11.1 (14) | 10.7 (14) | 6.3 (8) | 7.9 (10) | 11.6 (15) | 15.2 |
| ACT | 3.6 (5) | 1.1 (1) | 0.7 (1) | 0.5 (1) | 7.6 (10) | 8.6 (11) | 9.8 |
| NZ First | 4.1 (0) | 6.6 (8) | 8.7 (11) | 7.2 (9) | 2.6 (0) | 6.1 (8) | 10.2 |
| Te Pāti Māori | 2.4 (5) | 1.4 (3) | 1.3 (2) | 1.2 (0) | 1.2 (2) | 3.1 (6) | 1.4 |
| TOP (Opportunity) | – | – | – | 2.4 (0) | 1.5 (0) | 2.2 (0) | 6.2 |

Party-vote % (total seats in brackets). Source: [`data/elections/`](data/elections/); Oct 2026 = 30-day poll average (no seats).
<!-- GENERATED:report-votes END -->

The two big parties move in long arcs:

- National polled 44–47% in 2008–17, fell to 25.6% in 2020 and recovered to 38.1% in 2023.
- Labour fell to 25–27% in 2011–14, peaked at 50.0% in 2020 and then lost almost half its vote in 2023.

Source: [trends §1](elections/trends.md#1-party-vote-share-).

### 6.2 How the system is behaving: turnout, wasted votes and fragmentation

<!-- GENERATED:report-system START -->
| Election | Turnout % (of enrolled) | Parties on party-vote ballot | Parties winning seats | Effective no. of parties (votes) | Effective no. of parties (seats) | Gallagher disproportionality | "Wasted" party vote % | Overhang | Nat+Lab share % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2008 | 79.46 | 19 | 7 | 3.07 | 2.78 | 3.84 | 6.55 | 2 | 78.9 |
| 2011 | 74.21 | 13 | 8 | 3.15 | 2.98 | 2.38 | 3.37 | 1 | 74.8 |
| 2014 | 77.9 | 15 | 7 | 3.27 | 2.96 | 3.72 | 6.24 | 1 | 72.2 |
| 2017 | 79.75 | 16 | 5 | 2.91 | 2.67 | 2.73 | 4.68 | 0 | 81.3 |
| 2020 | 82.24 | 17 | 5 | 3.04 | 2.61 | 4.15 | 7.80 | 0 | 75.6 |
| 2023 | 78.2 | 17 | 6 | 4.10 | 3.78 | 2.70 | 5.58 | 3 | 65.0 |

Effective number of parties = 1 / Σ(share²) (Laakso–Taagepera). Gallagher index = √(½ Σ(vote% − seat%)²); lower is more proportional. Seat shares use final seat totals in `data/elections/<year>.json` (2023 includes the Port Waikato by-election seat). Computed by `tools/report_stats.py` from [`data/elections/`](data/elections/).
<!-- GENERATED:report-system END -->

- **Fragmentation is rising.** In 2023 National and Labour together won only 65% of the vote, the lowest since 2002, and the effective
  number of parties reached its highest level in this series (table above). October 2026 polls put the two together at about 57%
  (§1).
- **The wasted vote** peaked at 7.8% in 2020 ([trends §3](elections/trends.md#3-turnout-overhang-and-the-wasted-vote)).
  - In 2026 it hinges on TOP: about 2% if TOP clears 5%, about 7% if it does not (scenario D, §1).
  - The 2012 MMP review's recommendation to lower the threshold to 4% was never legislated (same source).
- **Turnout:**
  - It ranged from 74.2% (2011) to 82.2% (2020).
  - Enrolment now closes 13 days before polling day, and prisoners are barred from voting under the Electoral Amendment Act 2025
    ([elections/2026.md](elections/2026.md#rule-changes-since-2023)).
  - By 15 October 2026, 65.5% of 18–24-year-olds were enrolled (same source).
- **Overhang:**
  - The 2023 House had 123 seats, the most under MMP (§6.4).
  - The 2026 House starts at 120 seats: 71 electorates and 49 list seats, with one more list seat than in 2023
    ([data/elections/2026.json](data/elections/2026.json)).

### 6.3 The 54th Parliament: turnover

<!-- GENERATED:report-parliament START -->
| Party | Start (Dec 2023) | Dissolution (1 Oct 2026) |
|---|---:|---:|
| National | 49 | 48 |
| Labour | 34 | 34 |
| Green | 15 | 15 |
| ACT | 11 | 11 |
| NZ First | 8 | 8 |
| Te Pāti Māori | 6 | 4 |
| Independent | 0 | 2 |
| **Total** | 123 | 122 |

Government (National+ACT+NZ First): 68 of 123 at the start, 67 of 122 at dissolution (Papakura vacant after Judith Collins resigned on 14 May 2026). Source: [`data/parliaments/54.json`](data/parliaments/54.json).
<!-- GENERATED:report-parliament END -->

The 54th Parliament had the most turnover of the five covered here: 137 people served and there were 22 mid-term changes. They
included deaths, the first expulsion under the waka-jumping law, and two Te Pāti Māori expulsions
([trends §9](elections/trends.md#9-parliament-turnover)).

### 6.4 The Māori electorates

<!-- GENERATED:report-maori START -->
| Election | Labour | Māori Party / Te Pāti Māori | Mana | TPM party vote % |
|---|---:|---:|---:|---:|
| 2008 | 2 | 5 | 0 | 2.39 |
| 2011 | 3 | 3 | 1 | 1.43 |
| 2014 | 6 | 1 | 0 | 1.32 |
| 2017 | 7 | 0 | 0 | 1.18 |
| 2020 | 6 | 1 | 0 | 1.17 |
| 2023 | 1 | 6 | 0 | 3.08 |

Winners of the seven Māori electorates (from `data/elections/<year>.json`). At dissolution (Oct 2026) the seven were held by Te Pāti Māori 4, Labour 1, Te Tai Tokerau Party 1 and an independent 1 ([`data/parliaments/54.json`](data/parliaments/54.json); [electorates/README.md](electorates/README.md)).
<!-- GENERATED:report-maori END -->

The seven Māori seats tend to swing as a bloc between Labour and the Māori Party / Te Pāti Māori. Many Māori-roll voters split their
votes, which is why Te Pāti Māori won six seats on 3.1% of the party vote in 2023 and created two overhang seats
([trends §7](elections/trends.md#7-the-māori-electorates)). As of 3 August 2026, 54.4% of Māori voters were on the Māori roll
([Te Ao Māori News](https://www.teaonews.co.nz/2026/08/05/maori-roll-gains-momentum-as-deadline-looms-after-nationwide-enrolment-push/)).
In 2026, former Te Pāti Māori MPs are running against the party in Te Tai Tokerau (Kapa-Kingi) and Te Tai Tonga (Ferris, now an
independent) ([electorates/README.md](electorates/README.md#battleground-seats-to-watch-in-2026)).

### 6.5 Minor-party cycles

- **NZ First** rises and falls. It was out in 2008, back in 2011, kingmaker in 2017, out in 2020 and in coalition in 2023. Each time
  it has left a coalition its support has collapsed ([NZ First trends](parties/nz-first/track-record.md#trends-2011--2026)).
- **ACT** survived on Epsom alone at 0.5–1.1% (2011–17), then won 7.6–8.6% (2020–23) ([trends §5–6](elections/trends.md#6-electorate-deals-coat-tailing-epsom-and-ōhāriu)).
- **The Greens** are the most stable minor party (6–12%). They do better in opposition than in government
  ([Green trends](parties/green/track-record.md#6-trends)).
- **Small parties near the threshold:** the Conservatives' 3.97% in 2014 was the biggest near-miss. COVID-era protest parties won
  about 1–2% combined in 2020 and 2023. TOP polled above 5% for the first time in 2026, peaking at 9.5% (Roy Morgan, August)
  ([MINOR_PARTIES.md](parties/MINOR_PARTIES.md); [TOP README](parties/opportunity/README.md#2026-campaign-summary)).

### 6.6 Polling swings this term

<!-- GENERATED:report-quarters START -->
| Party | 2023 election | Highest quarter | Lowest quarter | Latest quarter (2026 Q4) | Swing election → latest quarter (pp) |
|---|---:|---|---|---:|---:|
| National | 38.1 | 38.2 (2024 Q1) | 28.4 (2026 Q4) | 28.4 | -9.7 |
| Labour | 26.9 | 33.9 (2026 Q1) | 25.0 (2023 Q4) | 28.5 | +1.6 |
| Green | 11.6 | 14.9 (2026 Q4) | 10.4 (2025 Q4) | 14.9 | +3.3 |
| ACT | 8.6 | 9.7 (2024 Q4) | 7.7 (2026 Q1) | 9.5 | +0.8 |
| NZ First | 6.1 | 12.0 (2026 Q2) | 5.6 (2024 Q2) | 10.3 | +4.3 |
| Te Pāti Māori | 3.1 | 5.1 (2024 Q4) | 1.3 (2026 Q4) | 1.3 | -1.8 |
| TOP (Opportunity) | 2.2 | 6.2 (2026 Q4) | 1.6 (2025 Q4) | 6.2 | +3.9 |

Largest party by quarterly mean: 2023 Q4: National +11.7 · 2024 Q1: National +12.3 · 2024 Q2: National +6.7 · 2024 Q3: National +9.9 · 2024 Q4: National +4.2 · 2025 Q1: National +0.7 · 2025 Q2: National +1.7 · 2025 Q3: Labour +1.1 · 2025 Q4: Labour +1.6 · 2026 Q1: Labour +2.9 · 2026 Q2: Labour +3.5 · 2026 Q3: National +0.5 · 2026 Q4: Labour +0.1.
Total polls since the 2023 election: 129. Quarterly means are simple averages of polls whose fieldwork ended in that quarter.
<!-- GENERATED:report-quarters END -->

- National led every quarter until mid-2025. Labour led from 2025 Q3 to 2026 Q2. The two have been level since 2026 Q3.
- NZ First (to about 10–12%) and, late in the campaign, TOP and the Greens gained most as National fell
  ([trends §8](elections/trends.md#8-polling-20232026)).
- Te Pāti Māori fell below 2% after its 2025 split (same source).
- Events behind these moves are listed in [data/polls-2026.json](data/polls-2026.json) (`events`). They include:
  - Luxon's two leadership votes (April and August 2026);
  - Kapa-Kingi's new party (May 2026);
  - the March 2026 fuel-price shock ([elections/2026.md](elections/2026.md)).

### 6.7 Electorate battlegrounds for 2026

Media analysts have named these seats as ones to watch. The table gives each seat's 2023 majority
([electorates/README.md](electorates/README.md#battleground-seats-to-watch-in-2026), which links each source):

| Seat | Held by (2023) | 2023 majority | Why |
|---|---|---:|---|
| [Mt Albert](electorates/mt-albert.md) | Labour | 18 | Four-way race; TOP leader Qiulae Wong is standing |
| [Nelson](electorates/nelson.md) | Labour | 26 | Second-closest result in 2023 |
| [Tāmaki Makaurau](electorates/tamaki-makaurau.md) | Te Pāti Māori | 42 | Labour's candidate resigned on 23 Oct 2026 ([NZ Herald](https://www.nzherald.co.nz/nz/politics/election-2026-live-updates-kerrin-leoni-resigns-as-labour-candidate-after-campaigning-with-mongrel-mob/R5IJCEB4TNF3LETYQ5JOSBPH7A/)) |
| [Henderson](electorates/henderson.md) | Labour (Te Atatū) | 131 | Twyford v Nicholas rematch |
| [Te Tai Tokerau](electorates/te-tai-tokerau.md) | Te Pāti Māori → Te Tai Tokerau Party | 517 | Four-way Māori seat |
| [Hutt South](electorates/hutt-south.md) | National | 1,332 | Bellwether; boundary change |
| [Mt Roskill](electorates/mt-roskill.md) | National | 1,564 | Cheung v Wood rematch |
| [Wellington Bays](electorates/wellington-bays.md) | Green (Rongotai) | 2,717 | Green v Labour |
| [Te Tai Tonga](electorates/te-tai-tonga.md) | Te Pāti Māori → independent | 2,824 | Ferris v his former party |
| [Auckland Central](electorates/auckland-central.md) | Green | 3,896 | Green co-leader's seat |
| [Tāmaki](electorates/tamaki.md) | ACT | 4,158 | Open seat (van Velden retiring) |
| [Epsom](electorates/epsom.md) | ACT | 8,142 | National's Goldsmith openly contesting it |

- **No formal electorate deals** have been announced this year
  ([electorates/README.md](electorates/README.md#battleground-seats-to-watch-in-2026)). Since ACT has polled above 5% since 2020, Epsom
  no longer decides whether ACT gets into Parliament ([trends §6](elections/trends.md#6-electorate-deals-coat-tailing-epsom-and-ōhāriu)).
- **New and renamed seats** created by the 2025 boundary review include Waitākere, Glendene, Henderson, Kenepuru, Kāpiti, Wellington
  North and Wellington Bays ([electorates/README.md](electorates/README.md#what-changed-in-the-2025-boundary-review)).

---

## 7. Who's who

Every person has a folder at `parties/<party>/people/<slug>/`, containing `README.md`, `person.json` and usually `photo.jpg`. Roles
and list ranks come from the party READMEs and policy.nz's 2026 lists.

| Party | Leader(s) | Key figures (2026 list rank) |
|---|---|---|
| National | [Christopher Luxon](parties/national/people/christopher-luxon/) – PM; Botany | [Nicola Willis](parties/national/people/nicola-willis/) (2, Finance) · [Chris Bishop](parties/national/people/chris-bishop/) (3, Housing, Infrastructure, Transport) · [Simeon Brown](parties/national/people/simeon-brown/) (4, Health; campaign chair) · [Erica Stanford](parties/national/people/erica-stanford/) (5, Education, Immigration) · [Paul Goldsmith](parties/national/people/paul-goldsmith/) (6, Justice; standing in Epsom) · [Mark Mitchell](parties/national/people/mark-mitchell/) (8, Police) |
| Labour | [Chris Hipkins](parties/labour/people/chris-hipkins/) – Leader of the Opposition; Remutaka | [Carmel Sepuloni](parties/labour/people/carmel-sepuloni/) (2, deputy) · [Barbara Edmonds](parties/labour/people/barbara-edmonds/) (3, finance) · [Willie Jackson](parties/labour/people/willie-jackson/) (4) · [Megan Woods](parties/labour/people/megan-woods/) (5) · [Ayesha Verrall](parties/labour/people/ayesha-verrall/) (6, health) · [Kieran McAnulty](parties/labour/people/kieran-mcanulty/) (10, campaign chair) |
| Green | [Marama Davidson](parties/green/people/marama-davidson/) (list) and [Chlöe Swarbrick](parties/green/people/chloe-swarbrick/) (Auckland Central) | [Teanau Tuiono](parties/green/people/teanau-tuiono/) (3) · [Tamatha Paul](parties/green/people/tamatha-paul/) (4, Wellington North) · [Julie Anne Genter](parties/green/people/julie-anne-genter/) (5, Wellington Bays) · [Ricardo Menéndez March](parties/green/people/ricardo-menendez-march/) (9) |
| ACT | [David Seymour](parties/act/people/david-seymour/) – Deputy PM since 31 May 2025; Epsom | [Nicole McKee](parties/act/people/nicole-mckee/) (2, deputy leader since June 2026) · [Andrew Hoggard](parties/act/people/andrew-hoggard/) (3) · [Karen Chhour](parties/act/people/karen-chhour/) (5) · [Todd Stephenson](parties/act/people/todd-stephenson/) (6) |
| NZ First | Winston Peters – Foreign Minister (*no person folder in the archive; see §8*) | [Shane Jones](parties/nz-first/people/shane-jones/) (deputy; Regional Development, Resources) · [Casey Costello](parties/nz-first/people/casey-costello/) (Customs, Seniors) · [Mark Patterson](parties/nz-first/people/mark-patterson/) · [Jenny Marcroft](parties/nz-first/people/jenny-marcroft/) · [Alfred Ngaro](parties/nz-first/people/alfred-ngaro/) (ex-National, ex-NewZeal) |
| Te Pāti Māori | [Debbie Ngarewa-Packer](parties/te-pati-maori/people/debbie-ngarewa-packer/) (Te Tai Hauāuru) and [Rawiri Waititi](parties/te-pati-maori/people/rawiri-waititi/) (Waiariki) | [Hana-Rawhiti Maipi-Clarke](parties/te-pati-maori/people/hana-rawhiti-maipi-clarke/) (Hauraki-Waikato) · [Oriini Kaipara](parties/te-pati-maori/people/oriini-kaipara/) (Tāmaki Makaurau, by-election 2025) |
| TOP | [Qiulae Wong](parties/opportunity/people/qiulae-wong/) – leader since Nov 2025; Mt Albert | [Daniel Eb](parties/opportunity/people/daniel-eb/) (2) · [Jessica Hammond](parties/opportunity/people/jessica-hammond/) (3) |
| Te Tai Tokerau Party | [Mariameno Kapa-Kingi](parties/te-tai-tokerau-party/people/mariameno-kapa-kingi/) – MP for Te Tai Tokerau | Independent MP [Tākuta Ferris](parties/independent/people/takuta-ferris/) (Te Tai Tonga) was also expelled from Te Pāti Māori |
| Others | [Kelvyn Alp](parties/nz-loyal/people/kelvyn-alp/) (NZ Loyal) · [Sue Grey](parties/nz-outdoors-freedom/people/sue-grey/) (Outdoors & Freedom) · [Maki Herbert](parties/legalise-cannabis/people/maki-herbert/) and [Michael Appleby](parties/legalise-cannabis/people/michael-appleby/) (ALCP) · [Rob McNeil](parties/animal-justice/people/rob-mcneil/) (Animal Justice) · [Victor Billot](parties/alliance/people/victor-billot/) (Alliance) · [Helen Houghton](parties/conservative/people/helen-houghton/) (Conservative) · [Jill Ovens](parties/womens-rights/people/jill-ovens/) (Women's Rights) · [Hannah Tamaki](parties/vision-nz/people/hannah-tamaki/) (Vision NZ) | Free Palestine leader Paul Hopkinson and co-leaders Danette Wereta (Animal Justice) and Dawn Trenberth (Women's Rights) have no folders |

Sources for ranks and roles: [National README](parties/national/README.md#current-caucus-and-key-figures),
[Labour README](parties/labour/README.md#current-caucus-54th-parliament), [Green README](parties/green/README.md#8-current-caucus-october-2026-15-mps),
[ACT README](parties/act/README.md), [NZ First README](parties/nz-first/README.md#in-government-20232026), [TOP README](parties/opportunity/README.md#2026-campaign-summary).

**MPs leaving at this election** (10): Duncan Webb, Paulo Garcia, Maureen Pugh, Celia Wade-Brown, Judith Collins (already resigned in
May 2026), Shane Reti, Brooke van Velden, Greg O'Connor, Andrew Bayly and Chris Penk. Penk lost his portfolios after an unsuccessful
move against Luxon ([elections/2026.md](elections/2026.md#who-is-standing)).

---

## 8. Data quality and limitations

**Blocked or unreachable sources, and the workarounds used:**

- **Party websites:** greens.org.nz, nzfirst.nz, maoriparty.org.nz and opportunity.org.nz block automated access (Cloudflare 403,
  including from a headless browser), and web.archive.org could not be reached ([docs/AGENT_BRIEF.md](docs/AGENT_BRIEF.md)).
  - Their web pages were recovered from **Common Crawl** captures, dated July–October 2026. These may predate later edits.
  - Press releases were taken from the party's own releases mirrored on **Scoop**, and PDFs from the parties' file hosts.
  - Each method is described in the party's policies README, for example the [Green](parties/green/policies/README.md),
    [NZ First](parties/nz-first/policies/README.md) and [TOP](parties/opportunity/policies/README.md) policy pages.
- **Pages that could not be recovered:**
  - Seven nzfirst.nz pages, one maoriparty.org.nz page and three opportunity.org.nz pages. Each has a `not-retrieved` placeholder that
    gives the URL and the reason, with no paraphrase.
  - Green: the disability policy PDF and the 23 Oct fiscal plan itself (reported via RNZ).
  - nzloyal.com ([NZ Loyal note](parties/nz-loyal/policies/documents/nzloyal-com-not-retrievable.md)).
- **Official results:** electionresults.govt.nz was blocked. Results come from Wikipedia's tables, which cite the official counts, and
  2023 electorate majorities were cross-checked against each electorate's article ([trends sources](elections/trends.md#sources);
  [electorates/README.md](electorates/README.md#about-the-data)).
- **Parliament and legislation:** parliament.nz and legislation.govt.nz could not be fetched. Bill dates come from news reports and
  Wikipedia ([NZ First policies](parties/nz-first/policies/README.md)).
- **Coalition agreements:** the 2023 coalition-agreement PDFs returned 403, so their contents come from reporting
  ([NZ First track record](parties/nz-first/track-record.md#how-to-read-this)).
- **Old manifestos:** Labour's 2017 and 2020 manifesto PDFs could not be obtained, so the wording of those promises comes from
  contemporary news and official releases ([Labour method](parties/labour/track-record.md#10-method-and-caveats)).
- **Other trackers:** the Parliament Pulse tracker's data could not be read ([National gaps](parties/national/track-record.md#gaps-and-things-this-archive-could-not-verify)).

**Second-hand sources:**

- The poll series is Wikipedia's table, with each row linked to the pollster's own release
  ([data/polls-2026.json](data/polls-2026.json)).
- Party summaries in [elections/2026.md](elections/2026.md) come from campaign coverage collated on Wikipedia.
- Policy "Why/How" summaries are policy.nz's (`summary_source` in each `policies.json`). The verbatim party texts sit beside them in
  `documents/`.
- The **official candidate count** was not retrievable. policy.nz lists 470 electorate candidacies, which should be treated as
  approximate ([elections/2026.md](elections/2026.md#who-is-standing)).

**Known disagreements and inconsistencies (unresolved):**

| Topic | Disagreement | Where |
|---|---|---|
| GDP growth to June 2026 | 1.7% year on year (1News/Stats NZ) vs "2.6%" (National's claim, repeated in the National track record). Possibly different measures (annual vs annual-average); not resolved | [issues.json](data/guide/issues.json) · [National track record](parties/national/track-record.md) · [National README](parties/national/README.md#the-2026-campaign-pitch-and-headline-promises) |
| Health targets | ED within six hours: 76.3% (Apr–Jun 2026, b2bnews) vs 74.2% ("June 2026 report", track record). Electives within four months: 72.6% vs 64.5%. Likely different reporting periods | [issues.json](data/guide/issues.json) · [National track record](parties/national/track-record.md) |
| National seat count | National README: "49 MPs"; data/parliaments/54.json and the guide: 48 at dissolution (Papakura vacant since May 2026). 49 is the count after the Port Waikato by-election | [National README](parties/national/README.md#current-caucus-and-key-figures) · [54.json](data/parliaments/54.json) |
| Vote shares in the second decimal place | e.g. NZ First 2023: 6.09% (elections JSON) vs 6.08% (NZ First README); ACT 2020: 7.59% vs 7.58%; Conservative 2023: 0.16% vs 0.15%; Animal Justice 0.17% vs 0.18% | [trends](elections/trends.md) · party READMEs · [MINOR_PARTIES.md](parties/MINOR_PARTIES.md) |
| 2023 electorate figures | data/elections/2023.json is built from Wikipedia's summary table, which uses some preliminary-count figures; electorate pages use official counts and note differences. Some policy.nz electorate descriptions describe the winner's vote total as the "margin" | [electorates/README.md](electorates/README.md#about-the-data) |
| Costings | Labour pay equity (Treasury, via National, $11b vs Labour's allowance); Labour fare cap ($65m vs $91–112m); NZ First package ($71.6b, Green estimate, rejected by NZ First); BNZ buy-back ($7.5b vs up to $24b) | §2 |
| Promise tallies | This archive vs NZ Politics Promise Tracker (National: 23 kept, 18 in progress, 1 broken) | [National summary](parties/national/track-record.md#summary) |
| Delivery-index definitions | Smaller parties' files count "broken" regardless of cause; National and Labour count it only when the party could have delivered | §4.2 |
| Archive gaps | No person folder for Winston Peters or Brooke van Velden; some `person.json` statuses say `candidate-2026` for sitting MPs (e.g. Luxon) | `parties/*/people/` |
| Te Pāti Māori "bottom line" | NZ First's leader said Te Pāti Māori called its tax policy a "bottom line"; no Te Pāti Māori statement using that phrase was found | [TPM policies](parties/te-pati-maori/policies/README.md) |

**How to verify anything in this report:**

1. Follow the link on the sentence. For archive files, follow the source links inside them. Promise entries carry `sources` arrays.
2. For policy wording, open `parties/<party>/policies/documents/<doc>.md`, which holds the verbatim published text with its source URL
   and retrieval date in the front matter.
3. For numbers, run `python3 tools/report_stats.py`, and see [docs/SCHEMA.md](docs/SCHEMA.md) for the data formats.
4. For official results, enrolment and voting places, the primary source is the Electoral Commission:
   [vote.nz](https://vote.nz) and [elections.nz](https://elections.nz).
5. Snapshot date: everything is as of 23 October 2026. Parties were still releasing policy, and new polls will follow
   ([quiz-method.md §4](guide/quiz-method.md#4-limitations)).

---

## 9. How to use this archive

| You want to… | Go to |
|---|---|
| Explore interactively: match quiz, party pages, issue comparison, your electorate's candidates, Parliament seat maps, poll trends, coalition builder, MMP seat calculator | [`site/index.html`](site/index.html). Serve the folder with any static web server (e.g. `python3 -m http.server` in `site/`); rebuild its data with `python3 tools/build_site.py` |
| Read plain-English party cards and issue explainers | [guide/parties.md](guide/parties.md) · [guide/issues.md](guide/issues.md) · quiz method: [guide/quiz-method.md](guide/quiz-method.md) |
| See every 2026 policy of a party, with full source texts | `parties/<party>/policies/README.md`, with `policies.json` and `documents/` beside it |
| Check whether a party kept its word | `parties/<party>/track-record.md` and [data/promises/](data/promises/) |
| Look up a politician | `parties/<party>/people/<slug>/README.md` (+ `person.json`, `photo.jpg`) |
| Find your electorate and its candidates | [electorates/README.md](electorates/README.md), one page per seat; find your seat on the [Electoral Commission maps](https://elections.nz/democracy-in-nz/historical-events/boundary-review-2025/electorate-maps) |
| Read the history of each election | [elections/2011.md](elections/2011.md) … [elections/2023.md](elections/2023.md), [elections/2026.md](elections/2026.md), [elections/trends.md](elections/trends.md) |
| Look up minor and historical parties | [parties/MINOR_PARTIES.md](parties/MINOR_PARTIES.md) |
| Use the raw data | `data/` (formats: [docs/SCHEMA.md](docs/SCHEMA.md)); original downloads in `raw/`; build scripts in `tools/` |

*Compiled 23 October 2026 from the archive's own files. Not affiliated with any party. Enrol and find where to vote at
[vote.nz](https://vote.nz).*
