# The parties: a plain-English guide (2026 election)

*Election day: **Saturday 7 November 2026** (advance voting from 26 October). Information as at **2026-10-23**. Built from [`data/guide/parties.json`](../data/guide/parties.json) by `tools/guide_render.py`; see also the [issues guide](issues.md).*

17 parties are registered with the Electoral Commission for the 2026 election and can contest the party vote (RNZ, 12 Oct 2026; Electoral Commission register). All 17 appear on policy.nz's 2026 party-vote list. Every party below gets the same template: what it is about, its headline 2026 policies, its own pitch, the main criticism (attributed to a named source), and the facts. "They say" and "critics say" are other people's words, not ours. Each card links to the full policy list, profile and track record for anyone who wants to go deeper.

**How to read this:**
- **Position** is the left–right label in the party's English Wikipedia infobox (retrieved 23 Oct 2026); where there is none we say so. 
- **Polling** is a simple average of all published polls in the 30 days to 23 October 2026 (data: [`data/polls-2026.json`](../data/polls-2026.json)). Small parties are not polled separately. A party needs **5% of the party vote or one electorate seat** to get list seats.
- **Policy ids** (like `POL54642`) point to the full entries in `parties/<party>/policies/` (policy.nz ids or ids assigned in this archive).
- Parties are listed by current seats in Parliament, then by polling, then alphabetically.

## At a glance

| Party | Leader(s) | Wikipedia position | Seats now | Polling (avg) | Says it could work with | Has ruled out |
|---|---|---|---|---|---|---|
| [National](#national) | Christopher Luxon | centre-right | 48 | 28.7% | ACT, NZ First | Labour, Opportunity (TOP) |
| [Labour](#labour) | Chris Hipkins | centre-left | 34 | 27.9% | Greens, Opportunity (TOP), Te Pāti Māori | NZ First, ACT, National |
| [Greens](#green) | Marama Davidson, Chlöe Swarbrick | centre-left to left-wing | 15 | 15.2% | Labour | – |
| [ACT](#act) | David Seymour | right-wing | 11 | 9.8% | National, NZ First, Opportunity (TOP) | Labour |
| [NZ First](#nz-first) | Winston Peters | – | 8 | 10.2% | National, ACT | Labour, Opportunity (TOP) |
| [Te Pāti Māori](#te-pati-maori) | Debbie Ngarewa-Packer, Rawiri Waititi | left-wing | 4 | 1.4% | Labour, Greens | National, ACT, NZ First |
| [Te Tai Tokerau Party](#te-tai-tokerau-party) | Mariameno Kapa-Kingi | – | 1 | – | National | – |
| [Opportunity (TOP)](#opportunity) | Qiulae Wong | centre | 0 | 6.2% | National, Labour | – |
| [Alliance](#alliance) | Victor Billot | left-wing | 0 | <0.5% (policy.nz) | – | – |
| [Animal Justice](#animal-justice) | Rob McNeil, Danette Wereta | – | 0 | <0.5% (policy.nz) | – | – |
| [Conservatives](#conservative) | Helen Houghton | right-wing | 0 | <0.5% (policy.nz) | – | – |
| [Free Palestine](#free-palestine) | Paul Hopkinson | – | 0 | <0.5% (policy.nz) | – | – |
| [Legalise Cannabis (ALCP)](#legalise-cannabis) | Maki Herbert, Michael Appleby | – | 0 | <0.5% (policy.nz) | – | – |
| [NZ Loyal](#nz-loyal) | Kelvyn Alp | far-right | 0 | <0.5% (policy.nz) | – | – |
| [Outdoors & Freedom ('freedom')](#nz-outdoors-freedom) | Sue Grey | – | 0 | <0.5% (policy.nz) | – | – |
| [Vision NZ](#vision-nz) | Hannah Tamaki | far-right | 0 | <0.5% (policy.nz) | – | – |
| [Women's Rights](#womens-rights) | Jill Ovens, Dawn Trenberth | – | 0 | <0.5% (policy.nz) | – | – |

*Coalition columns summarise public statements up to the date shown on each card; "–" means we found no statement. See each card for wording and sources.*

---

<a id="national"></a>
## National — New Zealand National Party

> The largest party in Parliament, leading the current government, promising no new taxes and a return to surplus.

**In a nutshell:** National leads the government now, with ACT and NZ First. It wants to keep taxes where they are, cut government debt and get the books back in surplus. It is promising compulsory KiwiSaver, longer paid parental leave and changes to sentencing and consent law.

**Big ideas for 2026:**

- No new taxes next term, and the government's books back in surplus by 2028/29 `POL54733` `POL54725` `POL54726`
- Make KiwiSaver compulsory for workers and sign babies up at birth `POL54734`
- Split Foodstuffs (New World, Pak'nSave, Four Square) into two separate companies to boost supermarket competition `POL55014`
- Extend paid parental leave from 26 to 30 weeks `POL54715`
- An extra $604 million for medicines (Pharmac) and free bowel screening from age 50, paid for partly by cutting foreign aid outside the Pacific `POL55205` `POL55208` `POL55209` `NAT-ARC-32`
- Replace NCEA, make students finish Year 11, and limit screen time for young children at school `POL55174` `POL55259` `POL55050`
- Sentencing and consent law: no 'good character' sentence discounts for sexual offending, an active 'yes' required for consent, and a penalty for refusing to give information when a child has been killed `POL54926` `POL54925` `POL55322`

**They say:** National's slogan is "Fixing the Basics, Building the Future"; its fiscal plan says a re-elected National government will "not impose new taxes" and will "return to surplus in 2028/29 and stay there". — *National Party (fiscal plan, 12 Oct 2026; slogan as reported by policy.nz)* ([assets.national.org.nz](https://assets.national.org.nz/web/prod/National's%20Fiscal%20Plan.pdf), [policy.nz](https://policy.nz/2026/party-vote/parties/national-party))

**Critics say:** Labour says "National promised to grow the economy and get the Government's finances in order. It has done neither - unemployment is higher, growth is weaker, debt has continued to rise, and frontline services have been cut." — *Labour Party (fiscal plan, Oct 2026)* ([labour.org.nz](https://www.labour.org.nz/fiscal-plan))

| | |
|---|---|
| **Leader(s)** | Christopher Luxon (Leader, Prime Minister) |
| **Founded** | 1936 |
| **Position (Wikipedia)** | centre-right ([en.wikipedia.org](https://en.wikipedia.org/wiki/New_Zealand_National_Party)) |
| **Seats now** | 48 of 123 — National won 49 seats in 2023 (48 at the general election plus the Port Waikato by-election). Papakura has been vacant since Judith Collins resigned on 14 May 2026 (no by-election is required within six months of a general election), so at dissolution National held 48 of the 122 sitting members in a 123-seat House (data/parliaments/54.json). |
| **Polling** | 28.7% (average of 9 polls, 2026-09-23–2026-10-23; range 25.9–32.0%) |
| **Coalition stance** | Wants to continue the current government with ACT and NZ First. Luxon ruled out a 'grand coalition' with Labour (May 2026) and formally ruled out any deal with Opportunity, including confidence and supply, from 27 July 2026, citing its plans to raise taxes; he repeated this through October. *(as at 2026-10-22)* [rnz.co.nz](https://www.rnz.co.nz/news/politics/809555/national-rules-out-working-with-opportunity-party), [bloomberg.com](https://www.bloomberg.com/news/articles/2026-05-11/new-zealand-pm-luxon-rules-out-grand-coalition-with-labour), [1news.co.nz](https://www.1news.co.nz/2026/10/22/analysis-the-real-roadblock-to-opportunity-isnt-luxon-its-peters/), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1932454/four-headed-beast-act-leader-david-seymour-hints-at-potential-for-coalition-with-opportunity) |
| **Costed fiscal plan?** | Yes. Its fiscal plan (12 Oct 2026) keeps new spending to $2.4b a year, leaves $7.5b of operating money unallocated over four years, and part-funds promises by cutting foreign aid. It includes $1.2m for an election policy costings unit. [assets.national.org.nz](https://assets.national.org.nz/web/prod/National's%20Fiscal%20Plan.pdf), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1865939/fiscal-holes-unfunded-promises-economist-not-sure-any-of-it-matters) |
| **Track record** | Led the government since November 2023 (with ACT and NZ First) and from 2008 to 2017. Of 71 past promises checked in this archive's tracker: 35 kept, 11 partly kept, 5 broken, 10 abandoned, 10 still in progress. (11 2026 promises are tracked but not yet due.) |
| **Website** | [national.org.nz](https://www.national.org.nz) |
| **Go deeper** | [profile](../parties/national/README.md) · [all 2026 policies](../parties/national/policies/README.md) · [track record](../parties/national/track-record.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/national-party) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/New_Zealand_National_Party), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [policy.nz](https://policy.nz/2026/party-vote/parties/national-party), [assets.national.org.nz](https://assets.national.org.nz/web/prod/National's%20Fiscal%20Plan.pdf), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="labour"></a>
## Labour — New Zealand Labour Party

> The main opposition party, campaigning on cheaper doctors' visits paid for by a capital gains tax on property.

**In a nutshell:** Labour is the biggest opposition party and last governed from 2017 to 2023. It wants three free GP visits a year, paid for by a new tax on profits from selling property (not the family home). It also promises to restore pay equity and to give the Commerce Commission new powers over large companies' prices.

**Big ideas for 2026:**

- Up to three free GP visits a year, paid for by a 28% capital gains tax on property sales (family homes and farms excluded) `POL54669` `POL54670`
- Free prescriptions, free cervical screening for ages 25-69 and free referred maternity scans `POL54665` `POL54689` `POL54686`
- Restore the old pay-equity law and give 65,000 care and support workers a $4 an hour pay rise `POL55167` `POL55214`
- Make price gouging illegal and require Woolworths and Foodstuffs to run their wholesale and retail businesses separately `POL55043` `POL55092`
- Cap public transport fares at $20 a week in the three biggest cities ($10 elsewhere) and freeze fuel tax for three years `POL54685` `POL54768`
- A 'NZ Future Fund' to invest in New Zealand businesses and infrastructure `POL54687`
- Wipe 10% off eligible graduates' student loans and build at least 6,000 more social homes `POL55158` `POL55151`

**They say:** Labour's slogan is "Better Starts Now". It says "every promise Labour has made is fully paid for" and that it "will balance the books without shrinking the economy". — *Labour Party (fiscal plan page, Oct 2026)* ([labour.org.nz](https://www.labour.org.nz/fiscal-plan), [1news.co.nz](https://www.1news.co.nz/2026/08/24/labour-reveals-its-2026-election-campaign-slogan/))

**Critics say:** National's Nicola Willis called Labour's fiscal plan fraudulent, saying Treasury estimates restoring the old pay-equity scheme would cost $11 billion, leaving Labour about $8.5 billion short; Labour says it has enough unallocated money and won't name a figure during negotiations. — *Nicola Willis, National finance spokesperson (via RNZ)* ([rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1733687/labour-s-fiscal-plan-national-s-claims-and-how-labour-is-defending-it))

| | |
|---|---|
| **Leader(s)** | Chris Hipkins (Leader, Leader of the Opposition) |
| **Founded** | 1916 |
| **Position (Wikipedia)** | centre-left ([en.wikipedia.org](https://en.wikipedia.org/wiki/New_Zealand_Labour_Party)) |
| **Seats now** | 34 of 123 |
| **Polling** | 27.9% (average of 9 polls, 2026-09-23–2026-10-23; range 23.5–30.8%) |
| **Coalition stance** | Will keep working with the Greens and says its 'door is open' to Opportunity. It has ruled out NZ First (formally, 10 Aug 2026) and ACT. It says it could work with Te Pāti Māori but senior roles for them are 'unlikely', and Hipkins ruled out giving the Greens or Te Pāti Māori the police or corrections portfolios (14 Oct 2026). Its campaign chair says his preference is a government with just the Greens and Opportunity. *(as at 2026-10-16)* [nzherald.co.nz](https://www.nzherald.co.nz/nz/politics/its-clearly-not-going-to-happen-chris-hipkins-definitively-rules-out-nz-first/YGB36A3QYFF5RDBP6N7HGYV32Q/), [nzherald.co.nz](https://www.nzherald.co.nz/nz/politics/labours-door-open-to-opportunity-senior-roles-for-te-pati-maori-unlikely-as-chris-hipkins-clarifies-vague-remarks/UBE55KHGCFGDHGYSRLQ3PUQN7Q/), [1news.co.nz](https://www.1news.co.nz/2026/06/28/labour-wont-work-with-act-but-nz-first-highly-unlikely-mcanulty/), [nzherald.co.nz](https://www.nzherald.co.nz/nz/politics/election-2026-labours-chris-hipkins-rules-out-greens-te-pati-maori-from-major-ministerial-roles-in-herald-debate/3GBPYMI6TJBKHLVNOSPGY6WTKA/), [interest.co.nz](https://www.interest.co.nz/public-policy/140701/were-verge-being-able-form-coalition-just-greens-and-opportunity-labour-eyes), [bloomberg.com](https://www.bloomberg.com/news/articles/2026-05-11/new-zealand-pm-luxon-rules-out-grand-coalition-with-labour) |
| **Costed fiscal plan?** | Yes. Its fiscal plan (Oct 2026), reviewed by accounting firm Hall Chadwick, keeps the $2.4b operating allowance, forecasts a surplus in 2028/29 and aims for net debt below 20% of GDP. National disputes how pay equity, fuel tax and the Future Fund are accounted for. [labour.org.nz](https://www.labour.org.nz/fiscal-plan), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1733687/labour-s-fiscal-plan-national-s-claims-and-how-labour-is-defending-it) |
| **Track record** | Led governments from 1999 to 2008 and 2017 to 2023; in opposition since 2023. Of 71 past promises checked in this archive's tracker: 36 kept, 10 partly kept, 7 broken, 18 abandoned. (21 2026 promises are tracked but not yet due.) |
| **Website** | [labour.org.nz](https://www.labour.org.nz) |
| **Go deeper** | [profile](../parties/labour/README.md) · [all 2026 policies](../parties/labour/policies/README.md) · [track record](../parties/labour/track-record.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/labour-party) |

*Note: Campaign development, 23 Oct 2026: Labour's Tāmaki Makaurau candidate Kerrin Leoni resigned as a candidate after Te Ao Māori News published footage of her campaigning at a gathering attended by Mongrel Mob members. Hipkins said the footage was "inconsistent with the standards I expect of Labour candidates". Her name stays on the ballot because nominations had closed (1News, 23 Oct 2026). Candidate-level events for other parties are recorded in electorates/ and people profiles, not on these cards.*

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/New_Zealand_Labour_Party), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [policy.nz](https://policy.nz/2026/party-vote/parties/labour-party), [labour.org.nz](https://www.labour.org.nz/fiscal-plan), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties), [1news.co.nz](https://www.1news.co.nz/2026/10/23/labours-leoni-resigns-after-gang-campaigning-video-emerges/)</sub>

---

<a id="green"></a>
## Greens — Green Party of Aotearoa New Zealand

> An environmental and social-justice party proposing new taxes on the very wealthy to fund public services.

**In a nutshell:** The Greens want strong action on climate change and nature, and more help for people on low incomes. They would tax people with more than $10 million in wealth and cut income tax for most workers. They also want a government-owned supermarket and limits on rent rises.

**Big ideas for 2026:**

- A 2.5% yearly tax on wealth above $10 million and a tax on large inheritances and gifts, so most workers can get an income tax cut (first $10,000 tax-free) `POL55135` `POL54729` `POL54735` `POL54737`
- Cap rent rises at 2% a year and build many more public homes `POL55082` `POL55081`
- 'KiwiMart': require Foodstuffs and Woolworths to sell at least 120 stores to a new government-owned supermarket chain `POL55032`
- Free public transport for children, students, apprentices and Community Services Card holders, and $2 fares for everyone else `POL55195` `POL55029`
- A new publicly owned company, 'Kiwipower', to build renewable energy `POL54766`
- An extra $3 billion a year for health, and restore pay equity for care workers `POL55118` `POL55181`
- Keep and expand free school lunches and make early childhood education free `POL54722` `POL55093`

**They say:** The Greens' slogan is "For All of Us". Co-leader Chlöe Swarbrick says the government's current budget path is "made possible only through underinvestment in core public services". — *Green Party; Chlöe Swarbrick (fiscal plan launch, 23 Oct 2026)* ([newstalkzb.co.nz](https://www.newstalkzb.co.nz/news/politics/election-2026-green-party-s-plan-to-transform-nz-s-finances-with-more-tax-spending-debt/), [policy.nz](https://policy.nz/2026/party-vote/parties/green-party))

**Critics say:** National's campaign chair Simeon Brown says the Greens' plan contains "nine new taxes"; the Greens' own fiscal plan shows net core Crown debt about $26.6 billion higher than Treasury's forecast by 2030/31. — *Simeon Brown, National (via B2B News); Green fiscal plan figures* ([b2bnews.co.nz](https://b2bnews.co.nz/news/greens-fiscal-plan-adds-26-point-6bn-in-debt-by-2030-31/))

| | |
|---|---|
| **Leader(s)** | Marama Davidson (Co-leader), Chlöe Swarbrick (Co-leader) |
| **Founded** | 1990 |
| **Position (Wikipedia)** | centre-left to left-wing ([en.wikipedia.org](https://en.wikipedia.org/wiki/Green_Party_of_Aotearoa_New_Zealand)) |
| **Seats now** | 15 of 123 |
| **Polling** | 15.2% (average of 9 polls, 2026-09-23–2026-10-23; range 13.3–16.0%) |
| **Coalition stance** | Campaigning to change the government with Labour: the two parties held a joint stand-up at Waitangi in February 2026 to show they would work together. Co-leader Marama Davidson said the Greens had stayed in contact with Te Pāti Māori through its internal troubles. We found no formal Green statement this campaign ruling other parties in or out. *(as at 2026-10-23)* [rnz.co.nz](https://www.rnz.co.nz/news/alert-top/585809/watch-live-labour-and-greens-speak-from-waitangi-treaty-grounds), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election) |
| **Costed fiscal plan?** | Yes. Its fiscal plan (23 Oct 2026), with direct fiscal effects reviewed by Infometrics, raises about $28.75b over four years from new taxes, lifts yearly new spending to $4.5-4.7b, delays surplus to 2029/30, and has net core Crown debt reaching $256.4b (44% of GDP) by 2030/31. [newstalkzb.co.nz](https://www.newstalkzb.co.nz/news/politics/election-2026-green-party-s-plan-to-transform-nz-s-finances-with-more-tax-spending-debt/), [b2bnews.co.nz](https://b2bnews.co.nz/news/greens-fiscal-plan-adds-26-point-6bn-in-debt-by-2030-31/) |
| **Track record** | Never a full coalition partner; supported Labour-led governments in 2017-2020 (confidence and supply, with ministers outside Cabinet) and 2020-2023 (cooperation agreement). Of 22 past promises checked in this archive's tracker: 11 kept, 4 partly kept, 6 broken, 1 abandoned. (10 2026 promises are tracked but not yet due.) |
| **Website** | [greens.org.nz](https://www.greens.org.nz) |
| **Go deeper** | [profile](../parties/green/README.md) · [all 2026 policies](../parties/green/policies/README.md) · [track record](../parties/green/track-record.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/green-party) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/Green_Party_of_Aotearoa_New_Zealand), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [policy.nz](https://policy.nz/2026/party-vote/parties/green-party), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="act"></a>
## ACT — ACT New Zealand

> A free-market party in the current government that wants a smaller state and lower government spending.

**In a nutshell:** ACT is part of the current government with National and NZ First. It wants the government to spend less, have fewer ministries and deliver public services by need rather than ethnicity (its phrase is 'one law for all'). It would slowly raise the pension age to 67 and scrap the net-zero climate law.

**Big ideas for 2026:**

- A smaller government: merge 43 departments into 19 and abolish ministries for particular groups (such as women, Pacific peoples and ethnic communities) `POL54863` `POL55270`
- Raise the pension (NZ Super) age gradually to 67 by 2035 `POL55275`
- Repeal the Zero Carbon Act and the net-zero target, and abolish the Climate Change Commission `POL55046` `ACT-A04`
- Freeze the minimum wage for three years and bring in a lower training wage `POL54990` `POL54993`
- Three strikes for burglary and deporting serious offenders who aren't citizens `POL54644` `POL54880`
- Let pharmacists treat more illnesses and lift Pharmac's share of the health budget `POL54642` `POL54645`
- Remove ethnicity-based criteria from public services and close the Waitangi Tribunal once historical claims are settled `POL54839` `POL54960`

**They say:** ACT says "New Zealand needs a smaller, more efficient government if we are going to balance the books, lift wages, restore trust in democracy, and unlock New Zealand's potential." — *ACT New Zealand ('A Smaller, More Affordable Government')* ([act.org.nz](https://www.act.org.nz/affordable-government))

**Critics say:** The Greens called ACT's fiscal plan "welfare for the wealthiest" and Labour accused ACT of "punching down", after it proposed raising the pension age and spending $653 million less on disability benefits. — *Green Party and Labour Party (via RNZ)* ([rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1835030/election-2026-as-it-happened-11-oct-greens-label-act-fiscal-plan-welfare-for-the-wealthiest-opportunity-seeks-answers-over-assumptions))

| | |
|---|---|
| **Leader(s)** | David Seymour (Leader, Deputy Prime Minister) |
| **Founded** | 1994 |
| **Position (Wikipedia)** | right-wing ([en.wikipedia.org](https://en.wikipedia.org/wiki/ACT_New_Zealand)) |
| **Seats now** | 11 of 123 |
| **Polling** | 9.8% (average of 9 polls, 2026-09-23–2026-10-23; range 9.0–11.0%) |
| **Coalition stance** | Wants to keep the current government and 'lock Labour out'. Seymour said a four-party deal including Opportunity, if it crossed 5%, 'would be a good outcome' to keep the Greens and Te Pāti Māori out of power (16 Oct 2026). Labour has ruled ACT out. *(as at 2026-10-16)* [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1932454/four-headed-beast-act-leader-david-seymour-hints-at-potential-for-coalition-with-opportunity), [1news.co.nz](https://www.1news.co.nz/2026/10/22/analysis-the-real-roadblock-to-opportunity-isnt-luxon-its-peters/), [1news.co.nz](https://www.1news.co.nz/2026/06/28/labour-wont-work-with-act-but-nz-first-highly-unlikely-mcanulty/) |
| **Costed fiscal plan?** | Yes. Its fiscal plan (11 Oct 2026) promises lower debt and spending, including raising the pension age by three months a year and $653m less on disability benefits. RNZ noted two items (about $100m a year, and tax relief of $264m-$303m a year) were not explained. [assets.nationbuilder.com](https://assets.nationbuilder.com/actnz/pages/38747/attachments/original/1791599898/ACT_2026_Fiscal_Plan.pdf?1791599898), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1835030/election-2026-as-it-happened-11-oct-greens-label-act-fiscal-plan-welfare-for-the-wealthiest-opportunity-seeks-answers-over-assumptions) |
| **Track record** | In coalition government with National and NZ First since 2023; supported National-led governments 2008-2017. Of 33 past promises checked in this archive's tracker: 18 kept, 4 partly kept, 5 broken, 6 abandoned. (5 2026 promises are tracked but not yet due.) |
| **Website** | [act.org.nz](https://www.act.org.nz) |
| **Go deeper** | [profile](../parties/act/README.md) · [all 2026 policies](../parties/act/policies/README.md) · [track record](../parties/act/track-record.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/act-party) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/ACT_New_Zealand), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [policy.nz](https://policy.nz/2026/party-vote/parties/act-party), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="nz-first"></a>
## NZ First — New Zealand First

> A party led by Winston Peters, in the current government, campaigning on 'citizens first' rules for voting and benefits and on breaking up big power and grocery companies.

**In a nutshell:** NZ First is part of the current government and has been in government with both Labour and National in the past. It wants some benefits, like the pension and voting, kept for citizens only. It also wants to break up the big power companies and buy back the BNZ bank.

**Big ideas for 2026:**

- Split the big power companies' generation and retail businesses `POL54656`
- Split Foodstuffs into two cooperatives and give the Commerce Commission more power `POL54658` `POL54659`
- Buy back the Bank of New Zealand (BNZ) into public ownership `POL54663`
- Only citizens could vote and get NZ Super; citizens first for social housing `POL54759` `POL54961` `POL54962`
- A $5,000-a-year 'Kiwi Kids Grant' for a child's first three years, and $70 a week more Working for Families tax credit `POL54746` `POL55257`
- Cut company tax to 20% for small and medium businesses `POL55155`
- A binding referendum on the Māori seats and replacing the Waitangi Tribunal with a completion commission `POL54757` `POL55157`

**They say:** Winston Peters says "what is needed more than anything else is serious skill, and serious experience in the next government" and that "It is vital that the left does not win." — *Winston Peters (speech, Masterton, 2 Aug 2026)* ([scoop.co.nz](https://www.scoop.co.nz/stories/PA2608/S00010/winston-peters-speech-new-zealand-in-its-eleventh-hour.htm))

**Critics say:** The NZ Herald reports NZ First is the largest party in Parliament not publishing a fiscal plan; a Green Party analysis put its policies at about $71.6 billion over four years, which NZ First rejects without giving its own figures. Labour's Chris Hipkins accused the party of "overt racism" when ruling it out. — *NZ Herald (22 Oct 2026); Green Party analysis; Chris Hipkins, Labour (10 Aug 2026)* ([nzherald.co.nz](https://www.nzherald.co.nz/nz/politics/nz-firsts-policies-could-cost-72b-and-that-doesnt-include-buying-back-the-bnz/premium/SMEMEEW25JE7DC4IQPTINQGFYA/), [nzherald.co.nz](https://www.nzherald.co.nz/nz/politics/its-clearly-not-going-to-happen-chris-hipkins-definitively-rules-out-nz-first/YGB36A3QYFF5RDBP6N7HGYV32Q/))

| | |
|---|---|
| **Leader(s)** | Winston Peters (Leader, Foreign Minister) |
| **Founded** | 1993 |
| **Position (Wikipedia)** | no position label in Wikipedia infobox. Wikipedia's opening sentence calls it a "right-wing populist" party; the infobox lists right-wing populism, nationalism and social conservatism as its ideology. ([en.wikipedia.org](https://en.wikipedia.org/wiki/New_Zealand_First)) |
| **Seats now** | 8 of 123 |
| **Polling** | 10.2% (average of 9 polls, 2026-09-23–2026-10-23; range 8.0–12.0%) |
| **Coalition stance** | Has repeatedly ruled out Labour and is campaigning to continue the current National-led government. After the NZ Herald 'power brokers' debate (21 Oct 2026) Peters said 'No, I can't' when asked if he could sit at a Cabinet table with Opportunity's Qiulae Wong. Labour has also ruled NZ First out (10 Aug 2026). *(as at 2026-10-22)* [1news.co.nz](https://www.1news.co.nz/2026/10/22/analysis-the-real-roadblock-to-opportunity-isnt-luxon-its-peters/), [1news.co.nz](https://www.1news.co.nz/2026/06/28/labour-wont-work-with-act-but-nz-first-highly-unlikely-mcanulty/), [nzherald.co.nz](https://www.nzherald.co.nz/nz/politics/its-clearly-not-going-to-happen-chris-hipkins-definitively-rules-out-nz-first/YGB36A3QYFF5RDBP6N7HGYV32Q/) |
| **Costed fiscal plan?** | No full fiscal plan. The NZ Herald (22 Oct 2026) says NZ First is the largest party in Parliament not publishing one. It has costed some items itself, e.g. about $1b a year for the small-business tax cut and $7.5b to buy back the BNZ (the Herald reports other estimates as high as $24b, without naming their source). [nzherald.co.nz](https://www.nzherald.co.nz/nz/politics/nz-firsts-policies-could-cost-72b-and-that-doesnt-include-buying-back-the-bnz/premium/SMEMEEW25JE7DC4IQPTINQGFYA/) |
| **Track record** | In government four times: with National (1996-98, 2023-26) and with Labour (confidence and supply 2005-08, coalition 2017-20). Of 43 past promises checked in this archive's tracker: 21 kept, 3 partly kept, 7 broken, 9 abandoned, 3 still in progress. (7 2026 promises are tracked but not yet due.) |
| **Website** | [nzfirst.nz](https://www.nzfirst.nz) |
| **Go deeper** | [profile](../parties/nz-first/README.md) · [all 2026 policies](../parties/nz-first/policies/README.md) · [track record](../parties/nz-first/track-record.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/nz-first) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/New_Zealand_First), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [policy.nz](https://policy.nz/2026/party-vote/parties/nz-first), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="te-pati-maori"></a>
## Te Pāti Māori

> A Māori rights party asking Māori-roll voters for their electorate vote, focused on Te Tiriti and Māori self-determination.

**In a nutshell:** Te Pāti Māori wants Māori to have more say over their own lives and resources, based on Te Tiriti o Waitangi. Its plan is to win the Māori electorate seats and to get people to give their party vote to Labour or the Greens. It would make the first $30,000 of income tax-free and add a wealth tax.

**Big ideas for 2026:**

- 'Kiwi Tax Plan': first $30,000 of income tax-free, a wealth tax, and a higher company tax rate `POL54812` `POL54939` `POL54940`
- Take GST off food (kai) `POL54938`
- An independent Te Tiriti Commission and binding Waitangi Tribunal recommendations `POL54917` `POL54795`
- Work towards a new constitution based on Matike Mai, and put the UN Declaration on the Rights of Indigenous Peoples into practice `POL54921` `POL54919`
- Abolish prisons by 2040, replacing them with community-led solutions `POL55283` `POL55070`
- A $1 billion fund for Māori and community ownership of renewable energy `POL55059`
- A Māori Education Authority to run Māori education `POL54679`

**They say:** Co-leader Debbie Ngarewa-Packer: "There's one plan, two votes" and "The only way we're going to get this government out, get more Māori in Parliament, and continue to be the loudest, unapologetic, independent Māori voice is to focus on giving our votes to Te Pāti Māori candidates." — *Debbie Ngarewa-Packer (campaign launch, 16 Aug 2026, via RNZ)* ([rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1011909/te-pati-maori-reveals-election-strategy-as-campaign-launches-in-gisborne))

**Critics say:** Labour's campaign chair Kieran McAnulty said Te Pāti Māori needs to "prove themselves to the country that they are worthy of being part of a government", after a year in which the party split and expelled two MPs. — *Kieran McAnulty, Labour (via interest.co.nz)* ([interest.co.nz](https://www.interest.co.nz/public-policy/140701/were-verge-being-able-form-coalition-just-greens-and-opportunity-labour-eyes), [thespinoff.co.nz](https://thespinoff.co.nz/politics/12-05-2026/the-further-unravelling-of-te-pati-maori))

| | |
|---|---|
| **Leader(s)** | Debbie Ngarewa-Packer (Co-leader), Rawiri Waititi (Co-leader) |
| **Founded** | 2004 |
| **Position (Wikipedia)** | left-wing ([en.wikipedia.org](https://en.wikipedia.org/wiki/Te_P%C4%81ti_M%C4%81ori)) |
| **Seats now** | 4 of 123 — Won 6 electorates in 2023; MPs Mariameno Kapa-Kingi and Tākuta Ferris were expelled in Nov 2025 (Kapa-Kingi now leads the Te Tai Tokerau Party; Ferris sits as an independent). |
| **Polling** | 1.4% (average of 9 polls, 2026-09-23–2026-10-23; range 0.4–2.0%) |
| **Coalition stance** | Wants to remove the current government and asks supporters to give their party vote to the 'left bloc' (Labour or the Greens). Responding to Labour saying senior roles were 'unlikely', co-leader Debbie Ngarewa-Packer said "Te Pāti Māori will have that conversation on 8th November." *(as at 2026-08-16)* [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1011909/te-pati-maori-reveals-election-strategy-as-campaign-launches-in-gisborne), [nzherald.co.nz](https://www.nzherald.co.nz/nz/politics/election-2026-te-pati-maori-responds-to-labours-chris-hipkins-saying-senior-govt-roles-unlikely-in-future-coalition/CKO2UJPLVNFBHFD6P324NS2CE4/), [theguardian.com](https://www.theguardian.com/world/2022/may/31/nz-maori-party-rules-out-right-wing-coalition-after-next-election) |
| **Costed fiscal plan?** | No full fiscal plan found. It published a 'Kiwi Tax Plan' (26 Aug 2026) setting out new taxes and rebates, but we found no published overall costing of its spending promises. [img.scoop.co.nz](https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf) |
| **Track record** | Supported National-led governments under confidence-and-supply deals from 2008 to 2017 (as the Māori Party); in opposition since 2020. Of 15 past promises checked in this archive's tracker: 8 kept, 3 partly kept, 3 broken, 1 abandoned. (6 2026 promises are tracked but not yet due.) |
| **Website** | [maoriparty.org.nz](https://www.maoriparty.org.nz) |
| **Go deeper** | [profile](../parties/te-pati-maori/README.md) · [all 2026 policies](../parties/te-pati-maori/policies/README.md) · [track record](../parties/te-pati-maori/track-record.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/te-pati-maori) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/Te_P%C4%81ti_M%C4%81ori), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [policy.nz](https://policy.nz/2026/party-vote/parties/te-pati-maori), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="te-tai-tokerau-party"></a>
## Te Tai Tokerau Party

> A new Northland-based Māori party formed by sitting MP Mariameno Kapa-Kingi after her split from Te Pāti Māori.

**In a nutshell:** This party was started in May 2026 by Mariameno Kapa-Kingi, the MP for Te Tai Tokerau, after Te Pāti Māori expelled her in November 2025 (the High Court later found that unlawful) and she then left the party. It puts children (mokopuna) and whānau wellbeing at the centre of its policies. It is standing two candidates.

**Big ideas for 2026:**

- A 'Mokopuna Act' requiring government to assess and report how its decisions affect children, with an independent Commissioner for Mokopuna `TTP-01`
- Wipe about $2 billion of debt that low-income whānau owe to MSD and IRD, and simplify the benefit system `TTP-03`
- A Crown-iwi fund so local mana whenua get at least a 25% stake in big regional infrastructure projects `TTP-02`
- Move money from prisons into hapū-run rehabilitation 'healing sanctuaries' `TTP-04`
- An independent, iwi-governed Māori health authority `TTP-05`

**They say:** "Mō ngā tamariki, mō ngā mokopuna te take. For our tamariki and mokopuna - that is the cause." — *Party website, as quoted by RNZ* ([rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election))

**Critics say:** We found no prominent named criticism of the new party itself in campaign coverage (searched 23 Oct 2026). Te Pāti Māori expelled Kapa-Kingi in November 2025 over what The Spinoff reports as "accusations of financial misconduct"; she challenged this and the High Court found the suspension and expulsion unlawful (March 2026). — *The Spinoff (12 May 2026); Otago Daily Times (11 May 2026)* ([thespinoff.co.nz](https://thespinoff.co.nz/politics/12-05-2026/the-further-unravelling-of-te-pati-maori), [odt.co.nz](https://www.odt.co.nz/news/national/te-pati-maori-splits-as-kapa-kingi-forms-new-party-d3ovh5eh))

| | |
|---|---|
| **Leader(s)** | Mariameno Kapa-Kingi (Leader, MP for Te Tai Tokerau) |
| **Founded** | 2026 |
| **Position (Wikipedia)** | no position label in Wikipedia infobox. Wikipedia lists its ideology as tino rangatiratanga (Māori self-determination). ([en.wikipedia.org](https://en.wikipedia.org/wiki/Te_Tai_Tokerau_Party)) |
| **Seats now** | 1 of 123 — Mariameno Kapa-Kingi, elected for Te Pāti Māori in Te Tai Tokerau in 2023 (policy.nz lists 1 current MP). |
| **Polling** | not polled separately |
| **Coalition stance** | Would not rule any party out, saying she would let the people of Te Tai Tokerau guide her. Kapa-Kingi said she would take a call from Prime Minister Luxon if he needed her support: "Imagine having Te Tai Tokerau at that table" (May 2026). Media seat projections count the party in the opposition bloc. *(as at 2026-05-12)* [1news.co.nz](https://www.1news.co.nz/2026/05/12/kapa-kingi-talks-plan-for-new-party-after-te-pati-maori-split/), [en.wikipedia.org](https://en.wikipedia.org/wiki/Te_Tai_Tokerau_Party), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1932454/four-headed-beast-act-leader-david-seymour-hints-at-potential-for-coalition-with-opportunity) |
| **Costed fiscal plan?** | No costed plan found. |
| **Track record** | New party (founded 11 May 2026, registered 5 August 2026); its leader has been an MP since 2023. This archive has no promise tracker for it. |
| **Website** | [tetaitokerauparty.org.nz](https://tetaitokerauparty.org.nz) |
| **Go deeper** | [profile](../parties/te-tai-tokerau-party/README.md) · [all 2026 policies](../parties/te-tai-tokerau-party/policies/README.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/te-tai-tokerau-party) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/Te_Tai_Tokerau_Party), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [tetaitokerauparty.org.nz](https://tetaitokerauparty.org.nz/our-policies/), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="opportunity"></a>
## Opportunity (TOP) — Opportunity Party

> A centrist party, polling close to the 5% threshold, proposing a land tax to fund a regular 'Citizen's Income' payment.

**In a nutshell:** Opportunity has never been in Parliament, but polls suggest it could get in and decide who governs. Its big idea is a weekly 'Citizen's Income' for most adults, paid for by a tax on land. It also wants to cap political donations, register lobbyists and phase out inshore bottom trawling.

**Big ideas for 2026:**

- A 'Citizen's Income' of up to $370 a week for most adults, funded by a land value tax `POL54816` `POL54777`
- Political reform: cap donations at $30,000 per donor, a lobbying register and an independent body to investigate political corruption `POL54809` `POL54778` `POL54808`
- A 10-year plan for the health system, lifting health funding to 9% of GDP `POL54823` `POL54871`
- Phase out inshore bottom trawling by 2030 and protect 30% of the ocean `POL54776` `POL54825`
- Give the Commerce Commission stronger powers, including forcing the break-up of businesses it finds anti-competitive `POL54824`
- Bring farming into the emissions trading scheme and build a $5b climate-resilience fund `POL54810` `POL55175`
- Make public transport free `POL54786`

**They say:** Leader Qiulae Wong says Opportunity would be an MMP kingmaker that is an "accelerator for progress - instead of a handbrake on change". — *Qiulae Wong (State of the Nation speech, Feb 2026, via Scoop)* ([scoop.co.nz](https://www.scoop.co.nz/stories/PO2602/S00118/we-are-the-next-generation-of-leaders-says-qiulae-wong.htm))

**Critics say:** National's Christopher Luxon said Opportunity's universal income "wants to make every New Zealander a beneficiary" and its land tax "is going to be massive"; commentator Grant Duncan argues its claimed $4b-a-year surplus is largely offset by new borrowing costs. — *Christopher Luxon (via RNZ, 27 Jul 2026); Grant Duncan (Substack)* ([rnz.co.nz](https://www.rnz.co.nz/news/politics/809555/national-rules-out-working-with-opportunity-party), [grantduncanphd.substack.com](https://grantduncanphd.substack.com/p/opportunity-what-does-top-really))

| | |
|---|---|
| **Leader(s)** | Qiulae Wong (Leader) |
| **Founded** | 2016 |
| **Position (Wikipedia)** | centre ([en.wikipedia.org](https://en.wikipedia.org/wiki/Opportunity_Party_(New_Zealand))) |
| **Seats now** | 0 of 123 |
| **Polling** | 6.2% (average of 9 polls, 2026-09-23–2026-10-23; range 4.8–8.0%) |
| **Coalition stance** | Says it will talk to either side and will 'pick up the phone' to National if it is the largest party, but "we are not here to prop up the current coalition government" and would not support a Treaty Principles bill (21 Oct 2026). In August 2026 Wong said Opportunity would not accept Winston Peters as Foreign Minister, while not ruling out other roles for NZ First. On 30 September it set five bottom lines (Commerce Commission powers, lobbying and donations reform, a 10-year health plan, phasing out bottom trawling, and climate commitments). *(as at 2026-10-21)* [1news.co.nz](https://www.1news.co.nz/2026/10/21/opportunity-would-have-walked-away-from-current-coalition/), [1news.co.nz](https://www.1news.co.nz/2026/08/13/opportunity-party-leader-on-poll-surge-working-with-winston-peters/), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1932454/four-headed-beast-act-leader-david-seymour-hints-at-potential-for-coalition-with-opportunity), [1news.co.nz](https://www.1news.co.nz/2026/10/22/analysis-the-real-roadblock-to-opportunity-isnt-luxon-its-peters/), [rnz.co.nz](https://www.rnz.co.nz/news/politics/809555/national-rules-out-working-with-opportunity-party) |
| **Costed fiscal plan?** | No full fiscal plan found. Its 'Tax Reset' policy says that, on 2024 numbers, the land value tax pays for the Citizen's Income with about $4b a year left over; independent commentators dispute parts of this. [cdn.opportunity.org.nz](https://cdn.opportunity.org.nz/documents/policy/Opportunity%20Policy%20-%20Tax%20Reset.pdf), [grantduncanphd.substack.com](https://grantduncanphd.substack.com/p/opportunity-what-does-top-really) |
| **Track record** | Has never had an MP, so has no record in Parliament; its best result was 2.4% in 2017. |
| **Website** | [opportunity.org.nz](https://www.opportunity.org.nz) |
| **Go deeper** | [profile](../parties/opportunity/README.md) · [all 2026 policies](../parties/opportunity/policies/README.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/opportunity-party) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/Opportunity_Party_(New_Zealand)), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [policy.nz](https://policy.nz/2026/party-vote/parties/opportunity-party), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="alliance"></a>
## Alliance — Alliance Party of Aotearoa New Zealand

> A democratic socialist party, back on the ballot, wanting public ownership of key services and a wealth tax.

**In a nutshell:** The Alliance was in government with Labour from 1999 to 2002, then faded away, and has now come back. It wants the government to own power, rail and other key services again. It would make the first $20,000 of income tax-free, paid for by a wealth tax.

**Big ideas for 2026:**

- First $20,000 of income tax-free, paid for by a 2.5% wealth tax above $2 million, a capital gains tax and a financial transactions levy `ALL-01` `ALL-02` `ALL-03` `ALL-04`
- 'Reverse privatisation': bring electricity, telecommunications networks, rail and key ports back into public ownership `ALL-09` `ALL-26`
- Free GP, dental, optical and hearing care through a public Community Health Service `ALL-13`
- Full employment, a 35-hour week with no loss of pay, and five weeks' annual leave `ALL-05`
- A big public house-building programme to clear the social housing waitlist, with social rents capped at 25% of income `ALL-22`
- Keep NZ Super universal at 65 and end the asset test for rest-home care `ALL-23`

**They say:** "We are a democratic socialist party building a fairer Aotearoa New Zealand." — *Party website, as quoted by RNZ* ([rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election))

**Critics say:** We found no prominent named criticism of the party in 2026 campaign coverage (searched 23 Oct 2026). — *Archive note*

| | |
|---|---|
| **Leader(s)** | Victor Billot (Leader) |
| **Founded** | 1991 |
| **Position (Wikipedia)** | left-wing ([en.wikipedia.org](https://en.wikipedia.org/wiki/Alliance_(New_Zealand_political_party))) |
| **Seats now** | 0 of 123 |
| **Polling** | not polled separately (policy.nz: <0.5%) |
| **Coalition stance** | No public statement on post-election partners found. *(as at 2026-10-23)* |
| **Costed fiscal plan?** | Partly. It published 'Tax Policy Costings: The Numbers' (Sept 2026) for its tax package, which it says produces a net revenue surplus; we found no costing of its full programme. [allianceparty.nz](https://allianceparty.nz/alliance-tax-plan-first-20000-income-tax-free/) |
| **Track record** | In coalition with Labour from 1999 to 2002; out of Parliament since 2002, deregistered in 2015 and re-registered on 5 August 2026. |
| **Website** | [allianceparty.nz](https://allianceparty.nz) |
| **Go deeper** | [profile](../parties/alliance/README.md) · [all 2026 policies](../parties/alliance/policies/README.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/alliance-party) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/Alliance_(New_Zealand_political_party)), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [allianceparty.nz](https://allianceparty.nz/what-we-stand-for/), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="animal-justice"></a>
## Animal Justice — Animal Justice Party Aotearoa New Zealand

> A small party focused on animal welfare and a gradual shift away from animal farming.

**In a nutshell:** The Animal Justice Party wants animals to be treated with respect and protected by law. It wants to end factory farming, with help for farmers to switch to plant-based food or other land uses. It also wants no-kill dog pounds and an independent Commissioner for Animals.

**Big ideas for 2026:**

- End factory farming and ban the most harmful farming and fishing practices, with funded help for farmers to change ([animaljustice.org.nz](https://animaljustice.org.nz/election-2026/election-manifesto/))
- Make rehoming and 'no-kill' the national default for dog pounds ([animaljustice.org.nz](https://animaljustice.org.nz/election-2026/election-manifesto/))
- An independent Commissioner for Animals with real powers ([animaljustice.org.nz](https://animaljustice.org.nz/election-2026/election-manifesto/))
- Give animals legal standing so they are not treated simply as property ([animaljustice.org.nz](https://animaljustice.org.nz/election-2026/election-manifesto/))
- More plant-based food in schools and hospitals, and fairer access to vet care ([animaljustice.org.nz](https://animaljustice.org.nz/election-2026/election-manifesto/))
- Get money out of politics and protect whistleblowers ([animaljustice.org.nz](https://animaljustice.org.nz/election-2026/election-manifesto/))

**They say:** "We're here because the animals don't have a vote, and someone needs to speak up for them honestly and without apology." — *Co-leaders Danette Wereta and Rob McNeil (2026 manifesto)* ([animaljustice.org.nz](https://animaljustice.org.nz/election-2026/election-manifesto/))

**Critics say:** We found no prominent named criticism of the party in 2026 campaign coverage (searched 23 Oct 2026). — *Archive note*

| | |
|---|---|
| **Leader(s)** | Rob McNeil (Co-leader), Danette Wereta (Co-leader) |
| **Founded** | 2023 |
| **Position (Wikipedia)** | no position label in Wikipedia infobox. Wikipedia says it "advocates non-violence towards animals, sustainability, and a move away from animal-based agriculture". ([en.wikipedia.org](https://en.wikipedia.org/wiki/Animal_Justice_Party_Aotearoa_New_Zealand)) |
| **Seats now** | 0 of 123 |
| **Polling** | not polled separately (policy.nz: <0.5%) |
| **Coalition stance** | No public statement on post-election partners found. *(as at 2026-10-23)* |
| **Costed fiscal plan?** | No costed plan found. |
| **Track record** | Has never had an MP; won 0.17% of the party vote in 2023. |
| **Website** | [animaljustice.org.nz](https://animaljustice.org.nz) |
| **Go deeper** | [profile](../parties/animal-justice/README.md) · [all 2026 policies](../parties/animal-justice/policies/README.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/animal-justice-party) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/Animal_Justice_Party_Aotearoa_New_Zealand), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [animaljustice.org.nz](https://animaljustice.org.nz/election-2026/election-manifesto/), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="conservative"></a>
## Conservatives — Conservative Party NZ

> A socially conservative party campaigning on lower taxes, 'one law for all', and legal personhood for unborn children from the third trimester.

**In a nutshell:** The Conservatives (called New Conservatives in 2023) want smaller government and lower taxes. They oppose policies that treat people differently by race or identity, and want New Zealand to leave the Paris climate agreement. They also want the law to recognise an unborn child as a person from the last trimester of pregnancy.

**Big ideas for 2026:**

- Lower income and company taxes, a 12.5% GST rate, and no tax on NZ Super `CON-01` `CON-02`
- 'One people under one law': no policies based on race, ancestry, sex or identity `CON-19`
- Leave the Paris Agreement and scrap climate-based taxes on fossil fuels `CON-09`
- Legal personhood for an unborn child from the last trimester, with more support for women in crisis pregnancies `CON-17`
- Shift visas towards skilled professionals and entrepreneurs using a stable points system `CON-05`
- A Royal Commission of Inquiry into police performance `CON-06`

**They say:** "We are working to bring a conservative voice to Parliament, to turn back the 'woke' agenda and prevailing culture of death." — *Party website, as quoted by RNZ* ([rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election))

**Critics say:** Wikipedia summarises 2019-20 coverage (Stuff and others) in which some opponents and observers described the party's policies, under its New Conservative name, as far-right; the party says it has since moved to a 'more centrist' position. We found no prominent named criticism of the party in 2026 campaign coverage (searched 23 Oct 2026). — *Wikipedia (retrieved 23 Oct 2026), summarising 2019-20 commentary* ([en.wikipedia.org](https://en.wikipedia.org/wiki/Conservative_Party_NZ))

| | |
|---|---|
| **Leader(s)** | Helen Houghton (Leader) |
| **Founded** | 2011 |
| **Position (Wikipedia)** | right-wing ([en.wikipedia.org](https://en.wikipedia.org/wiki/Conservative_Party_NZ)) |
| **Seats now** | 0 of 123 |
| **Polling** | not polled separately (policy.nz: <0.5%) |
| **Coalition stance** | No public statement on post-election partners found. *(as at 2026-10-23)* |
| **Costed fiscal plan?** | No costed plan found. |
| **Track record** | Has never had an MP; its best result was 3.97% in 2014 and it won 0.15% (as New Conservatives) in 2023. |
| **Website** | [conservatives.nz](https://www.conservatives.nz) |
| **Go deeper** | [profile](../parties/conservative/README.md) · [all 2026 policies](../parties/conservative/policies/README.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/conservative-party-nz) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/Conservative_Party_NZ), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [conservatives.org.nz](https://conservatives.org.nz/policies/), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="free-palestine"></a>
## Free Palestine — Free Palestine (Palestine Free from the River to the Sea Party)

> A new single-issue party focused on Palestine and an independent foreign policy.

**In a nutshell:** Free Palestine was set up in 2026 and is contesting its first election. It wants one democratic, secular state in all of historic Palestine with equal rights for everyone. It also wants New Zealand to leave military and security alliances with the United States.

**Big ideas for 2026:**

- A single, secular, democratic state in all of Palestine with equal citizenship `FPP-02`
- The right of return for all Palestinian refugees `FPP-01`
- Press the government to back prosecutions for war crimes and uphold UN resolutions `FPP-03`
- An independent foreign policy, withdrawing from military and security alliances with the US `FPP-05`

**They say:** "A political party committed to justice, international law and a democratic national state with equal rights for all citizens." — *Party website* ([palfree.nz](https://palfree.nz/), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election))

**Critics say:** The Electoral Commission received 207 submissions opposing the party's registration, some calling its name and logo offensive; it allowed the registration but refused the proposed logo, which contained a Palestinian flag. — *Electoral Commission process, reported by RNZ* ([rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election))

| | |
|---|---|
| **Leader(s)** | Paul Hopkinson (Leader) |
| **Founded** | 2026 |
| **Position (Wikipedia)** | no position label in Wikipedia infobox. Wikipedia lists its ideology as anti-Zionism and single-issue politics. ([en.wikipedia.org](https://en.wikipedia.org/wiki/Free_Palestine_Party_(New_Zealand))) |
| **Seats now** | 0 of 123 |
| **Polling** | not polled separately (policy.nz: <0.5%) |
| **Coalition stance** | No public statement on post-election partners found. *(as at 2026-10-23)* |
| **Costed fiscal plan?** | No costed plan found. |
| **Track record** | New party (registered 5 August 2026); first election. |
| **Website** | [palfree.nz](https://palfree.nz) |
| **Go deeper** | [profile](../parties/free-palestine/README.md) · [all 2026 policies](../parties/free-palestine/policies/README.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/free-palestine) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/Free_Palestine_Party_(New_Zealand)), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [palfree.nz](https://palfree.nz/), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="legalise-cannabis"></a>
## Legalise Cannabis (ALCP) — Aotearoa Legalise Cannabis Party

> A single-issue party that wants cannabis legalised and regulated for medical, recreational and industrial use.

**In a nutshell:** The Cannabis Party has stood at every election since 1996 but has never won a seat. It wants adults to be able to grow and use cannabis without being prosecuted. It would also clear past cannabis convictions and grow a hemp industry.

**Big ideas for 2026:**

- Stop prosecuting adults for possessing, growing and using cannabis `ALCP-01`
- Regulated R18 cannabis sales, like alcohol and tobacco but with no advertising `ALCP-02`
- Wipe all past cannabis convictions `ALCP-05`
- Allow medicinal cannabis and full-scale hemp farming `ALCP-03` `ALCP-04`
- Overhaul the Misuse of Drugs Act ([rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election))

**They say:** "ALCP exists to legalise, regulate, and normalise cannabis for medicinal, recreational, and industrial use, while reducing harm caused by prohibition." — *Party website, as quoted by RNZ* ([rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election))

**Critics say:** We found no prominent named criticism of the party in 2026 campaign coverage (searched 23 Oct 2026). For context, 50.7% of voters voted against legalising recreational cannabis in the 2020 referendum and 48.4% for. — *Archive note; Electoral Commission referendum result* ([en.wikipedia.org](https://en.wikipedia.org/wiki/2020_New_Zealand_cannabis_referendum))

| | |
|---|---|
| **Leader(s)** | Maki Herbert (Co-leader), Michael Appleby (Co-leader) |
| **Founded** | 1996 |
| **Position (Wikipedia)** | no position label in Wikipedia infobox. Wikipedia describes it as "dedicated to the legalisation of cannabis for medical, recreational and industrial use". ([en.wikipedia.org](https://en.wikipedia.org/wiki/Aotearoa_Legalise_Cannabis_Party)) |
| **Seats now** | 0 of 123 |
| **Polling** | not polled separately (policy.nz: <0.5%) |
| **Coalition stance** | No public statement on post-election partners found. *(as at 2026-10-23)* |
| **Costed fiscal plan?** | No costed plan found. |
| **Track record** | Has never had an MP; won 0.45% of the party vote in 2023. |
| **Website** | [alcp.org.nz](https://www.alcp.org.nz) |
| **Go deeper** | [profile](../parties/legalise-cannabis/README.md) · [all 2026 policies](../parties/legalise-cannabis/policies/README.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/aotearoa-legalise-cannabis-party) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/Aotearoa_Legalise_Cannabis_Party), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [alcp.org.nz](https://www.alcp.org.nz/policy), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="nz-loyal"></a>
## NZ Loyal — New Zealand Loyal

> A small party that wants New Zealand out of the UN, WHO and WEF and opposes climate agreements.

**In a nutshell:** NZ Loyal was started in 2023 by Liz Gunn and is now led by Kelvyn Alp. It wants New Zealand to leave international bodies like the UN and WHO and drop climate agreements. It got 1.2% of the party vote in 2023.

**Big ideas for 2026:**

- End New Zealand's participation in the UN, the World Economic Forum and the World Health Organization `NZL-01`
- End climate agreements and pursue energy independence, including oil and gas `NZL-02` `NZL-03`
- Scrap the current tax system `NZL-05`
- Scrap what it calls 'race-based policies', and write a New Zealand constitution `NZL-06` `NZL-07`
- Decentralise government and 'return power to the people' `NZL-10`

**They say:** "We reject government overreach. We take our country back from foreign interests. We restore our freedoms. No compromise. No apologies." — *NZ Loyal website, as quoted by RNZ* ([rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election))

**Critics say:** RNZ reports that leader Kelvyn Alp was charged with sharing the livestream of the 2019 Christchurch mosque attacks, and is a founder of the Counterspin platform, which RNZ describes as far-right. We found no named criticism of the party's 2026 policies themselves. — *RNZ (12 Oct 2026)* ([rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election))

| | |
|---|---|
| **Leader(s)** | Kelvyn Alp (Leader) |
| **Founded** | 2023 |
| **Position (Wikipedia)** | far-right ([en.wikipedia.org](https://en.wikipedia.org/wiki/New_Zealand_Loyal)) |
| **Seats now** | 0 of 123 |
| **Polling** | not polled separately (policy.nz: <0.5%) |
| **Coalition stance** | No public statement on post-election partners found. *(as at 2026-10-23)* |
| **Costed fiscal plan?** | No costed plan found. |
| **Track record** | Has never had an MP; won 1.21% of the party vote in 2023. It was deregistered in July 2024 and re-registered on 5 August 2026. |
| **Website** | [nzloyal.com](https://nzloyal.com) |
| **Go deeper** | [profile](../parties/nz-loyal/README.md) · [all 2026 policies](../parties/nz-loyal/policies/README.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/new-zealand-loyal) |

*Note: The party website could not be retrieved for this archive (see parties/nz-loyal/policies/documents/nzloyal-com-not-retrievable.md); policies are taken from RNZ's quotation of it.*

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/New_Zealand_Loyal), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election), [policy.nz](https://policy.nz/2026/party-vote/parties/new-zealand-loyal), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="nz-outdoors-freedom"></a>
## Outdoors & Freedom ('freedom') — NZ Outdoors & Freedom Party

> A small party, now calling itself 'freedom', focused on individual rights, direct democracy and outdoor access.

**In a nutshell:** This party began as the NZ Outdoors Party and grew after opposing COVID-19 vaccine mandates. It wants the Bill of Rights to become supreme law so governments can't override it. It also opposes 1080 poison and wants better public access to the outdoors.

**Big ideas for 2026:**

- Make the NZ Bill of Rights 'supreme law' that no future government can override `OFP-01`
- Direct democracy: let citizens decide laws through binding votes `OFP-02`
- Replace the Department of Conservation with a new 'Department of Outdoors' promoting access, recreation and food gathering `OFP-18`
- Natural ecosystems free from poisons such as 1080 `OFP-18`
- Speed up house building by freeing land and revising resource-management rules `OFP-07`

**They say:** "People hold the power. You choose the laws. Join the global movement striving for Direct Democracy." — *Party website, as quoted by RNZ* ([rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election))

**Critics say:** After anti-vaccination activists linked to the party (as Wikipedia's election article describes them) confronted Labour MP Ayesha Verrall at a Wellington candidates' meeting on 8 September 2026, Labour leader Chris Hipkins said some people had strong 'anti-science' views that did not represent the 'vast bulk' of New Zealanders. We found no named criticism of the party's policies themselves. — *Chris Hipkins, Labour (RNZ, 9 Sep 2026)* ([rnz.co.nz](https://www.rnz.co.nz/news/politics/1310827/labour-s-chris-hipkins-says-his-party-won-t-be-intimidated-by-anti-science), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election))

| | |
|---|---|
| **Leader(s)** | Sue Grey (Leader) |
| **Founded** | 2015 |
| **Position (Wikipedia)** | no position label in Wikipedia infobox. Wikipedia says its "policies combine environmentalism with anti-government conspiracy theories"; its listed ideology includes anti-1080, environmentalism and anti-vaccination. ([en.wikipedia.org](https://en.wikipedia.org/wiki/NZ_Outdoors_%26_Freedom_Party)) |
| **Seats now** | 0 of 123 |
| **Polling** | not polled separately (policy.nz: <0.5%) |
| **Coalition stance** | No public statement on post-election partners found. *(as at 2026-10-23)* |
| **Costed fiscal plan?** | No costed plan found. |
| **Track record** | Has never had an MP; in 2023 it stood under the Freedoms NZ umbrella, which won 0.34%. |
| **Website** | [freedom.kiwi](https://freedom.kiwi) |
| **Go deeper** | [profile](../parties/nz-outdoors-freedom/README.md) · [all 2026 policies](../parties/nz-outdoors-freedom/policies/README.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/nz-outdoors--freedom-party) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/NZ_Outdoors_%26_Freedom_Party), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [freedom.kiwi](https://freedom.kiwi/policies), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="vision-nz"></a>
## Vision NZ — Vision New Zealand

> A Christian conservative party linked to Destiny Church, campaigning on 'family values', a pause on immigration and leaving the Paris Agreement.

**In a nutshell:** Vision NZ is led by Hannah Tamaki of Destiny Church. It says strong families should come first and the government should do less. It wants to pause what it calls 'mass immigration', leave the Paris climate agreement and make the first $25,000 of income tax-free.

**Big ideas for 2026:**

- A Ministry for Families and a Parental Rights Bill `VIS-01` `VIS-30`
- Make the first $25,000 of income tax-free, and stop taxing superannuation `VIS-10` `VIS-11`
- Pause what it calls 'mass immigration' and lengthen the wait for citizenship to 10 years `VIS-24` `VIS-26`
- Leave the Paris Accord and suspend commitment to UN regulations `VIS-25`
- Define sex in law as male and female and ban gender-transition treatment for minors `VIS-29` `VIS-30`
- Abolish MMP party lists so only electorate winners sit in Parliament, cut the number of MPs, and add term limits `VIS-34` `VIS-35`

**They say:** "We believe that the family is the ultimate cornerstone of society and the primary incubator for our nation's morals, which is why we will dismantle state dependency, strip away government overreach and restore parental authority to its rightful place." — *Party website, as quoted by RNZ* ([rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election))

**Critics say:** The criticism we found is aimed at Destiny Church, which Vision NZ's leader Hannah Tamaki co-leads, rather than at the party: Prime Minister Christopher Luxon said a February 2025 Destiny Church protest that disrupted a children's event at an Auckland library and the Auckland Rainbow Parade went "too far", and Auckland Mayor Wayne Brown said there was "absolutely no place for thuggery". We found no prominent named criticism of the party in 2026 campaign coverage (searched 23 Oct 2026). — *Christopher Luxon; Wayne Brown (1News, 16 Feb 2025)* ([1news.co.nz](https://www.1news.co.nz/2025/02/16/destiny-church-protesters-at-pride-events-went-too-far-pm))

| | |
|---|---|
| **Leader(s)** | Hannah Tamaki (Leader) |
| **Founded** | 2019 |
| **Position (Wikipedia)** | far-right ([en.wikipedia.org](https://en.wikipedia.org/wiki/Vision_NZ)) |
| **Seats now** | 0 of 123 |
| **Polling** | not polled separately (policy.nz: <0.5%) |
| **Coalition stance** | No public statement on post-election partners found. *(as at 2026-10-23)* |
| **Costed fiscal plan?** | No costed plan found. |
| **Track record** | Has never had an MP; in 2023 it stood under the Freedoms NZ umbrella, which won 0.34%. |
| **Website** | [vision.org.nz](https://www.vision.org.nz) |
| **Go deeper** | [profile](../parties/vision-nz/README.md) · [all 2026 policies](../parties/vision-nz/policies/README.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/vision-nz) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/Vision_NZ), [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [vision.org.nz](https://www.vision.org.nz/visionpolicies), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

<a id="womens-rights"></a>
## Women's Rights — Women's Rights Party

> A small party focused on women's sex-based rights, such as single-sex spaces and sport.

**In a nutshell:** The Women's Rights Party was started in 2023 by two former Labour members. It says rights for women should be based on biological sex. It wants single-sex spaces for women and girls and stricter limits on medical gender treatment for young people.

**Big ideas for 2026:**

- Protect single-sex spaces for women and girls `WRP-09`
- Extend the ban on puberty blockers to cross-sex hormones for under-18s, and limit gender surgery to over-25s `WRP-01`
- Women's sport and other single-sex categories decided by biological sex (it calls this 'fair play in sports') `WRP-09`
- Laws and health services that define 'woman' as an adult human female and keep words such as 'mother' and 'breastfeeding' `WRP-17`
- 'Equitable reward and recognition' (its words) for women's paid and unpaid work, including paid parental leave of 12 months `WRP-12`

**They say:** "We are women and men who believe in democracy, equality and biological reality." — *Party website, as quoted by RNZ* ([rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election))

**Critics say:** Wikipedia's article on co-leader Jill Ovens (retrieved 23 Oct 2026) describes her as an "anti-transgender activist" and the party as "anti-transgender"; the party disputes Wikipedia's characterisation of it and in October 2023 urged supporters to stop donating to Wikipedia. We found no prominent named criticism of the party in 2026 campaign coverage (searched 23 Oct 2026). — *Wikipedia (retrieved 23 Oct 2026); Women's Rights Party statement (30 Oct 2023)* ([en.wikipedia.org](https://en.wikipedia.org/wiki/Jill_Ovens), [womensrightsparty.nz](https://womensrightsparty.nz/?p=2720))

| | |
|---|---|
| **Leader(s)** | Jill Ovens (Co-leader), Dawn Trenberth (Co-leader) |
| **Founded** | 2023 |
| **Position (Wikipedia)** | no Wikipedia article or position label. Wikipedia's 2026 election article lists its ideology as gender-critical feminism. ([en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election)) |
| **Seats now** | 0 of 123 |
| **Polling** | not polled separately (policy.nz: <0.5%) |
| **Coalition stance** | No public statement on post-election partners found. *(as at 2026-10-23)* |
| **Costed fiscal plan?** | No costed plan found. |
| **Track record** | Has never had an MP; won 0.08% of the party vote in 2023. |
| **Website** | [womensrightsparty.nz](https://womensrightsparty.nz) |
| **Go deeper** | [profile](../parties/womens-rights/README.md) · [all 2026 policies](../parties/womens-rights/policies/README.md) · [policy.nz](https://policy.nz/2026/party-vote/parties/womens-rights-party) |

<sub>Sources: [en.wikipedia.org](https://en.wikipedia.org/wiki/2026_New_Zealand_general_election), [womensrightsparty.nz](https://womensrightsparty.nz/our-priorities/), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election), [policy.nz](https://policy.nz/2026/party-vote/parties/womens-rights-party), [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties)</sub>

---

*Party count sources: [elections.nz](https://elections.nz/democracy-in-nz/political-parties-in-new-zealand/register-of-political-parties), [rnz.co.nz](https://www.rnz.co.nz/news/politics_election-2026/1856067/explainer-what-you-need-to-know-about-the-smaller-political-parties-in-this-year-s-election), [siasat.com](https://www.siasat.com/530-candidates-to-contest-new-zealands-2026-general-election-3555840/), [policy.nz](https://policy.nz/2026/party-vote).*
