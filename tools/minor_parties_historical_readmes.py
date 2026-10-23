#!/usr/bin/env python3
"""Write README.md profiles for historical (no longer registered) minor parties that contested 2011-2023
general elections (or registered but never stood). Content was written by hand from the Wikipedia articles saved in
raw/minor-parties/wiki/ and the primary sources they cite; vote figures come from raw/minor-parties/results.json
(official results as tabulated by Wikipedia). Usage: python3 -I tools/minor_parties_historical_readmes.py"""
import json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RES = json.load(open(os.path.join(ROOT, "raw/minor-parties/results.json")))
WP = "https://en.wikipedia.org/wiki/"
RESULTS_SRC = "Official results as tabulated in the Wikipedia 2011–2023 general election articles (citing electionresults.govt.nz), extracted by `tools/minor_parties_results.py` into `raw/minor-parties/results.json`"


def result_rows(slug, notes=None):
    notes = notes or {}
    rows = []
    for y in ["2011", "2014", "2017", "2020", "2023"]:
        for r in RES[y]["parties"]:
            if r["slug"] == slug:
                pv = f"{int(r['party_votes']):,}" if r["party_votes"] else "no list"
                pc = f"{r['party_vote_pct']:.2f}" if r["party_vote_pct"] is not None else "—"
                rows.append(f"| {y} | {r['name']} | {pv} | {pc} | {r['total_seats']} | {notes.get(y, '')} |")
    for y, n in notes.items():
        if not any(row.startswith(f"| {y} ") for row in rows):
            rows.append(f"| {y} | — | — | — | — | {n} |")
    rows.sort()
    return "| Election | Ballot name | Party votes | Party vote % | Seats | Notes |\n|---|---|---|---|---|---|\n" + "\n".join(rows)


P = {}
P["social-credit"] = dict(
    title="Social Credit (Democrats for Social Credit / New Zealand Democratic Party for Social Credit)",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request on 28 February 2023 (membership below 500 after leader Chris Leitch's death in January 2023); said it would remain active. Not contesting 2026."),
           ("Founded", "1953 as the Social Credit Political League; called the Democratic Party 1985–2018 (\"Democrats for Social Credit\" from 2005); renamed Social Credit in June 2018"),
           ("Leaders (2011–23)", "Stephnie de Ruyter (from 2002); Chris Leitch (2018–2023)"),
           ("Ideology", "Social credit monetary reform (government-created credit, opposition to bank-issued debt money)"),
           ("Seats", "None since 1987 in its own right (held 1–2 seats 1966–87; 20.7% of the vote in 1981)")],
    body="""New Zealand's third party from the 1950s to the 1980s, Social Credit was part of the Alliance from 1991 to 2002 and
briefly of the Progressive Coalition, then re-established itself as an independent party. In this archive's period it
was a fringe party: 0.08% in 2011, 0.07% in 2014, 0.03% in 2017 and 0.05% under the restored Social Credit name in 2020.
In 2021 it opposed COVID-19 vaccine mandates. After deregistration its president Gloria Bruni said it intended to
rebrand to avoid comparison with China's "social credit system". [1][2]

Historically the movement faced accusations of antisemitism stemming from founder C. H. Douglas's views; Te Ara and
Paul Spoonley describe this as ending by the 1970s–1984 under Bruce Beetham. [1]

*Data note:* Wikipedia's party article gives 1,432 party votes for 2011; the official-results table gives 1,714 (used
below). [1][3]""",
    notes={"2011": "official count; party article says 1,432", "2023": "deregistered Feb 2023 — did not stand"},
    sources=[WP + "Social_Credit_Party_(New_Zealand)",
             "Electoral Commission, \"Amendment to Party Register\" (2023) — https://elections.nz/media-and-news/2023/amendment-to-party-register/ ; The Spinoff, \"'Here for good': The long, strange twilight of Social Credit\" (27 Oct 2019) https://thespinoff.co.nz/politics/27-10-2019/here-for-good-the-long-strange-twilight-of-social-credit/",
             RESULTS_SRC])
P["libertarianz"] = dict(
    title="Libertarianz",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request on 29 January 2014 (went into recess)"),
           ("Founded", "Late 1995 by Ian Fraser"), ("Leaders", "Ian Fraser; Lindsay Perigo; Peter Cresswell; Russell Watkins; Richard McGrath (at deregistration)"),
           ("Ideology", "Libertarianism, influenced by Ayn Rand's Objectivism; slogan \"More Freedom, Less Government\""), ("Seats", "None")],
    body="""Libertarianz contested every election from 1996 (best: 0.29% in 1999). In 2006 member Bernard Darnton sued Helen
Clark over Labour's publicly funded 2005 pledge card. Its last general election was 2011 (0.07%). In January 2014 leader
Richard McGrath asked the Electoral Commission to deregister it, saying volunteer administration had become impossible,
and advised members to support ACT under its new president Jamie Whyte. [1]""",
    notes={}, sources=[WP + "Libertarianz", "Electoral Commission, \"Amendment to the Register of Political Parties\" (29 Jan 2014) — https://elections.nz/media-and-news/2014new-medianews-folder/amendment-to-the-register-of-political-parties/", RESULTS_SRC])
P["ban-1080"] = dict(
    title="Ban 1080 Party",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request on 28 February 2018"), ("Founded", "2014 by Bill Wallace; registered 8 August 2014"),
           ("Leaders", "Co-leaders Bill Wallace and Mike Downard"), ("Ideology", "Single issue: end aerial drops of sodium fluoroacetate (1080) poison; \"people not poison\" targeted pest control"), ("Seats", "None")],
    body="""The party wanted the Department of Conservation's aerial 1080 programme stopped immediately and replaced with
species-specific protection plans and targeted pest control. Its best candidate result was Pete Salter's 6.5% (fourth)
in West Coast-Tasman in 2014. Police visited party officials in 2015 during the investigation into threats to
contaminate infant formula with 1080; the threats were found to be unrelated to the party. After the 2017 result it
deregistered, and many supporters moved to the [Outdoors Party](../nz-outdoors-freedom/README.md). [1][2]

*Data note:* Wikipedia's party article says 4,368 party votes in 2014; the official-results table gives 5,113 (used
below). [1][3]""",
    notes={"2014": "official count; party article says 4,368"},
    sources=[WP + "Ban_1080_Party", "Electoral Commission, \"Amendments to the Register of Political Parties – 28 February 2018\" — https://elections.nz/media-and-news/2018/amendments-to-the-register-of-political-parties-28-february-2018/ ; Stuff, \"Ban 1080 party in push for election\" (18 Jun 2014) http://www.stuff.co.nz/national/politics/10172333/Ban-1080-party-in-push-for-election", RESULTS_SRC])
P["focus-nz"] = dict(
    title="Focus New Zealand (Focus NZ, formerly NZ Rural)",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request on 22 February 2016"), ("Founded", "2012 in Northland as \"NZ Rural\"; renamed Focus New Zealand Nov 2012; registered 29 January 2014"),
           ("Ideology", "Interests of business owners, producers and provincial communities; exchange rate; community empowerment"), ("Seats", "None")],
    body="""A Northland-based party that stood in the 2013 Far North and Whangārei local elections and the 2014 general election,
where its 639 party votes were the fewest of the 15 registered parties. [1]""",
    notes={}, sources=[WP + "Focus_NZ", "Stuff, \"New party for 'all rural people'\" (22 Aug 2012) — http://www.stuff.co.nz/auckland/local-news/northland/northern-news/7517432/New-party-for-all-rural-people", RESULTS_SRC])
P["nz-independent-coalition"] = dict(
    title="NZ Independent Coalition",
    facts=[("Status (Oct 2026)", "**Deregistered** 20 May 2016"), ("Founded", "January 2014 by Brendan Horan; registered 24 July 2014"),
           ("Leader", "Brendan Horan (MP 2011–14: elected for NZ First, expelled December 2012, then independent)"), ("Ideology", "Electorate-driven representation (MPs to poll electorates and vote accordingly); higher pensions; free tertiary education"), ("Seats", "None won (Horan sat as an independent MP until 2014)")],
    body="""Brendan Horan was expelled from NZ First in December 2012 amid accusations (which he denied) of taking money from his
dying mother's bank account. He formed the party for the 2014 election on the slogan "safe children, safe whanau, safe
society". It won 872 votes (0.04%) and Horan left Parliament. [1][2]""",
    notes={}, sources=[WP + "NZ_Independent_Coalition", "RNZ, \"Brendan Horan launches new party\" (30 Jul 2014) — http://www.radionz.co.nz/news/political/250964/brendan-horan-launches-new-party ; Electoral Commission, \"Registration of NZ Independent Coalition and Logo\" (24 Jul 2014) http://www.elections.org.nz/news-media/registration-nz-independent-coalition-and-logo", RESULTS_SRC])
P["nz-independent-coalition"]["mps"] = "None elected under its banner. Leader Brendan Horan was already a sitting MP (elected on NZ First's list in 2011; independent from December 2012) and left Parliament at the 2014 election."
P["civilian"] = dict(
    title="The Civilian Party",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request on 5 May 2015"), ("Founded", "Announced June 2013 by satirist Ben Uffindell (editor of *The Civilian* satirical website); registered 11 August 2014"),
           ("Ideology", "Satirical/joke party (e.g. \"a llama to every child living in poverty\", independence from Hamilton)"), ("Seats", "None")],
    body="""The party drew criticism in 2014 for receiving $33,635 of broadcasting funding; John Key quipped "the biggest joke's
on us, the taxpayer". Uffindell replied that other "joke parties" were getting funding too. It won 1,096 votes (0.05%)
in 2014 and stood no electorate candidates. [1][2]""",
    notes={}, sources=[WP + "The_Civilian_Party", "Stuff, \"Satirical party that promised to ban satire deregistered\" (15 May 2015) — http://www.stuff.co.nz/national/politics/68598160/satirical-party-that-promised-to-ban-satire-deregistered", RESULTS_SRC])
P["1law4all"] = dict(
    title="1Law4All Party",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request on 5 May 2015; **never contested an election**"), ("Founded", "June 2013; registered 24 July 2014"),
           ("Ideology", "Opposed Treaty of Waitangi references in law, the Waitangi Tribunal, Māori electorates and the UN Declaration on the Rights of Indigenous Peoples"), ("Seats", "None")],
    body="""Registered for the 2014 election, it failed to lodge a candidate list after four of five board members resigned
shortly before nominations closed. It had earlier removed references to Allan Titford from its website after his
conviction for rape and arson. As an unregistered group it distributed pamphlets in 2017 and 2019; the Advertising
Standards Authority ordered it to stop the 2019 material as likely to cause "serious offence". [1]""",
    notes={"2014": "registered but stood no candidates"}, sources=[WP + "1Law4All_Party", "Stuff, \"Party distances itself from Titford\" (22 Nov 2013) — http://www.stuff.co.nz/national/politics/9431455/Party-distances-itself-from-Titford", "Electoral Commission, \"Application to register 1Law4All party and logo\" (14 Jun 2014) — http://www.elections.org.nz/news-media/application-register-1law4all-party-and-logo"])
P["pirate-party"] = dict(
    title="Pirate Party of New Zealand",
    facts=[("Status (Oct 2026)", "**Inactive; never registered**"), ("Founded", "c. 2009–2010 (modelled on Sweden's Pirate Party; member of Pirate Parties International)"),
           ("Ideology", "Copyright and patent reform, internet privacy"), ("Seats", "None")],
    body="""As an unregistered party it could not contest the party vote. In 2011 it stood in the Botany by-election (32 votes)
and in Hamilton East (137 votes) and Wellington Central (277 votes) at the general election, after being conditionally
awarded $20,000 of broadcasting funding and having its logo registered. It stood no candidates in 2014 and failed to
gain registration for 2017. [1]""",
    notes={"2011": "unregistered: 2 electorate candidates (414 votes)"}, sources=[WP + "Pirate_Party_of_New_Zealand", "Stuff, \"Pirate Party pushes candidates for protest\" (25 Nov 2011) — http://www.stuff.co.nz/national/politics/6034385/Pirate-Party-pushes-candidates-for-protest"])
P["advance-nz"] = dict(
    title="Advance New Zealand (Advance NZ) — incl. the NZ Public Party",
    facts=[("Status (Oct 2026)", "**Deregistered** 19 August 2021"), ("Founded", "Announced April 2020 by independent MP Jami-Lee Ross; registered 6 August 2020"),
           ("Leaders", "Co-leaders Jami-Lee Ross and Billy Te Kahika (NZ Public Party), July–October 2020"),
           ("Ideology", "Billed by Ross as centrist and anti-corruption; campaigned largely on COVID-19 and vaccine conspiracy claims, 5G, 1080 and opposition to lockdowns"), ("Seats", "None won (Ross lost his seat)")],
    body="""Jami-Lee Ross, MP for Botany, left National in 2018 after accusing leader Simon Bridges of corruption over a
$100,000 donation; he was later himself charged by the Serious Fraud Office over the donation scheme and was acquitted
at a High Court trial that began in July 2022, while three co-defendants were convicted. In July 2020 Advance merged campaigns with Billy Te Kahika's NZ Public
Party, a party known for spreading COVID-19 "plandemic" misinformation; other component parties were the NZ People's
Party, Reset NZ and Direct Democracy NZ. [1][2]

During the campaign the Speaker referred Ross to the Privileges Committee for using doctored parliamentary footage in an
advertisement, the Advertising Standards Authority ordered removal of an ad comparing COVID-19 deaths to seasonal flu,
Facebook removed the party's page for repeated COVID-19 misinformation, and the leaders held a mass rally on 12 September
2020 in defiance of distancing rules. Advance won **0.98%** (28,429). Te Kahika claimed the election was rigged; the
Public Party split from Advance on 26 October 2020 and Te Kahika shut it down in February 2021. Te Kahika was later
convicted (and discharged on appeal) of breaching COVID-19 lockdown rules. [1][3][4]""",
    notes={}, sources=[WP + "Advance_New_Zealand", WP + "Jami-Lee_Ross", WP + "Billy_Te_Kahika",
                       "RNZ, \"Billy Te Kahika quits politics, shuts down New Zealand Public Party\" (19 Feb 2021) — https://www.rnz.co.nz/news/political/436757/billy-te-kahika-quits-politics-shuts-down-new-zealand-public-party ; Wikipedia \"New Zealand Public Party\" " + WP + "New_Zealand_Public_Party", RESULTS_SRC])
P["advance-nz"]["mps"] = "None elected. Co-leader Jami-Lee Ross was the sitting (independent, ex-National) MP for Botany when he founded Advance; he chose not to defend Botany and left Parliament in 2020."
P["heartland"] = dict(
    title="Heartland New Zealand Party (HeartlandNZ)",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request in June 2023; did not stand in 2023 or 2026"), ("Founded", "2019/2020 (sources differ); registered 6 August 2020"),
           ("Leader", "Mark Ball (former Franklin District mayor)"), ("Ideology", "Rural party opposing the Emissions Trading Scheme, the Paris Agreement, the oil-and-gas exploration ban and agricultural environmental regulation"), ("Seats", "None")],
    body="""Backed at its founding by Hamilton entrepreneur Harry Mowbray, Heartland ran a five-person list in 2020 and won 914
party votes (0.03%), the fewest of any registered party, though Ball polled 8,462 electorate votes (21%, third) in Port
Waikato. [1][2]""",
    notes={"2020": "Mark Ball 3rd in Port Waikato (8,462 votes)"}, sources=[WP + "Heartland_New_Zealand_Party", "Stuff, \"New rural Heartland party challenges climate change and water restrictions\" (17 Jul 2020) — https://www.stuff.co.nz/national/politics/300054112/new-rural-heartland-party-challenges-climate-change-and-water-restrictions", RESULTS_SRC])
P["sustainable-nz"] = dict(
    title="Sustainable New Zealand Party (Sustainable NZ)",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request on 15 December 2021"), ("Founded", "Launched November 2019 by Vernon Tava (ex-Green); registered 4 December 2019"),
           ("Leader", "Vernon Tava"), ("Ideology", "Environmentalist but willing to work with National or Labour (\"blue-green\"/\"teal\" in media; Tava preferred \"green-green\")"), ("Seats", "None")],
    body="""Former party secretary Helen Cartwright alleged in February 2020 that she had been asked to falsify membership records
to reach the 500 needed for registration; Tava said the party complied fully with the Electoral Act. Cartwright left and
founded the Integrity Party. Sustainable NZ received a $53,840 broadcasting allocation and won 1,880 votes (0.07%) in
2020. [1][2]""",
    notes={}, sources=[WP + "Sustainable_New_Zealand_Party", "RNZ, \"Sustainable New Zealand Party to prioritise water, native species, economy\" (10 Nov 2019) — https://www.rnz.co.nz/news/political/402964/sustainable-new-zealand-party-to-prioritise-water-native-species-economy ; Electoral Commission, \"Amendment to the Register of Political Parties\" (15 Dec 2021) https://elections.nz/media-and-news/2021/amendment-to-the-register-of-political-parties-3/", RESULTS_SRC])
P["newzeal"] = dict(
    title="NewZeal (formerly ONE Party)",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request on 31 March 2026, after leader Alfred Ngaro aligned the party with NZ First and became a NZ First candidate"),
           ("Founded", "ONE Party launched June 2020 (company incorporated Sept 2019 by Stephanie Harawira); renamed NewZeal July/August 2023"),
           ("Leaders", "Stephanie Harawira & Edward Shanly (2019–21); Ian Johnson, Allan Cawood & Kariana Black (2021–23); Alfred Ngaro (2023–Mar 2026)"),
           ("Ideology", "Christian/socially conservative (ONE originally proposed MPs answerable to an \"Apostolic Council\"); under Ngaro presented as a party \"for all New Zealanders\""), ("Seats", "None")],
    body="""ONE Party launched at Marsden Cross in June 2020, made a reciprocal electorate arrangement with Vision NZ and won
0.28% (8,121). In 2022 it jointly backed a New Conservative candidate in the Hamilton West by-election. Former National
minister **Alfred Ngaro** — who said he was disappointed by National's stance on conversion therapy and gender identity —
took over and renamed it NewZeal in 2023; it won 0.57% (16,126). On 22 March 2026 Ngaro announced at Winston Peters'
State of the Nation speech that he would stand for NZ First, citing "strategic realism and shared values", and the party
deregistered. [1][2]""",
    notes={"2020": "as ONE Party", "2023": "as NewZeal"}, sources=[WP + "NewZeal", "NZ Herald, \"Alfred Ngaro explains why he turned his back on National Party to launch NewZeal\" (17 Aug 2023) — https://www.nzherald.co.nz/nz/real-life-alfred-ngaro-explains-why-he-turned-his-back-on-national-party-to-launch-new-zeal/5ML6ZNUOAZD4HOF2MC36LOJP34/ ; Electoral Commission \"NewZeal no longer registered\" (31 Mar 2026) https://elections.nz/media-and-news/newzeal-no-longer-registered", RESULTS_SRC])
P["freedoms-nz"] = dict(
    title="Freedoms New Zealand (Freedoms NZ)",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request, 1 May 2025; disbanded as an umbrella"), ("Founded", "Announced 22 August 2022 by Brian Tamaki at a Parliament protest; registered 16 February 2023"),
           ("Leaders", "Brian Tamaki; co-leader Sue Grey (2023)"), ("Components", "Vision NZ, NZ Outdoors & Freedom (from May 2023), New Nation (left by Sept 2023), unregistered Yes Aotearoa and Rock the Vote NZ, plus Tamaki's Freedom & Rights Coalition"),
           ("Ideology", "Anti-COVID-mandate \"freedom movement\" umbrella; anti-establishment"), ("Seats", "None")],
    body="""Tamaki forecast 20% of the vote. National, Labour, the Greens and ACT all ruled out working with it (National after
initially telling reporters to "read between the lines"). The High Court rejected its challenge to the Electoral
Commission's decision to give the group a single broadcasting allocation. During the 2023 campaign Freedoms NZ supporters,
notably Vision candidate Karl Mokaraka, disrupted Labour, National and ACT events, including Labour's campaign launch.
It won **0.34%** (9,586). [1]""",
    notes={}, sources=[WP + "Freedoms_New_Zealand", "NZ Herald, \"Brian Tamaki announces new political party\" (23 Aug 2022) — https://www.nzherald.co.nz/nz/parliament-protest-brian-tamaki-announces-new-political-party-freedoms-nz/GYZSQDORMUKGO7MP3OMMAN2D6Q/ ; Electoral Commission, \"Freedoms New Zealand no longer registered\" (2 May 2025) https://www.elections.nz/media-and-news/2025/freedoms-new-zealand-no-longer-registered/", RESULTS_SRC])
P["democracynz"] = dict(
    title="DemocracyNZ",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request, 15 February 2024"), ("Founded", "March 2022 by former National MP Matt King after the Parliament-grounds occupation; registered 12 October 2022"),
           ("Leader", "Matt King"), ("Ideology", "Self-described centrist, democracy/equality/unity; in practice focused on opposing the COVID-19 response and climate regulation"), ("Seats", "None")],
    body="""King, Northland MP 2017–2020, joined the 2022 anti-mandate protest and left National. In June 2023 five candidates
quit over the party's culture, and many supporters moved to NZ First. DemocracyNZ ran 13 candidates in 2023 and won
**0.24%** (6,786); King came fourth in Northland (3,812 votes). [1][2]""",
    notes={"2023": "Matt King 4th in Northland"}, sources=[WP + "DemocracyNZ", "Stuff, \"'We stand for democracy': Ex-National MP Matt King launches anti-mandate party\" (18 Mar 2022) — https://www.stuff.co.nz/national/politics/128102034/we-stand-for-democracy-exnational-mp-matt-king-launches-antimandate-party ; Electoral Commission \"DemocracyNZ no longer registered\" (16 Feb 2024) https://elections.nz/media-and-news/2024/democracynz-no-longer-registered/", RESULTS_SRC])
P["leighton-baker"] = dict(
    title="Leighton Baker Party",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request, 27 May 2024"), ("Founded", "June 2023 by Leighton Baker (New Conservative leader 2017–20); registered 16 August 2023"),
           ("Ideology", "Christian social conservatism; family values"), ("Seats", "None")],
    body="""Baker, arrested during the 2022 Wellington protest, launched the party after being replaced as New Conservative
leader. It won **0.07%** (2,105) in 2023; Baker came fourth in Waimakariri (3.9%). He said: "maybe there's not that
many people that agree with us, but we still have an obligation to present a different view." After the election the
Electoral Commission admitted data-entry errors at three booths had wrongly assigned hundreds of votes to the Leighton
Baker Party and New Conservatives (corrected; seat allocation unaffected). See also [Conservative](../conservative/README.md). [1][2][3]""",
    notes={}, sources=[WP + "Leighton_Baker", WP + "2023_New_Zealand_general_election", "Electoral Commission, \"Leighton Baker Party no longer registered\" (27 May 2024) — https://elections.nz/media-and-news/2024/leighton-baker-party-no-longer-registered/", RESULTS_SRC])
P["nz-tea-party"] = dict(
    title="New Zealand TEA Party (Taxpayers and Entrepreneurs Alliance)",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request, 14 September 2022"), ("Founded", "2020 by former Auckland mayoral candidates John Hong and Susanna Kruger; registered 6 August 2020"),
           ("Leader", "John Hong"), ("Ideology", "Self-described anti-racist, socially democratic and fiscally conservative; pro-business, pro-migration, against a capital gains tax and recreational cannabis; Roger Douglas named as patron"), ("Seats", "None")],
    body="""Unconnected to the US Tea Party. Candidate John Palino campaigned for an electorate from Florida. It won 2,414 votes
(0.08%) in 2020. [1][2]""",
    notes={}, sources=[WP + "New_Zealand_TEA_Party", "The Spinoff, \"John Palino is running for parliament – from Florida\" (2 Sep 2020) — https://thespinoff.co.nz/politics/02-09-2020/john-palino-is-running-for-parliament-from-florida/", RESULTS_SRC])
P["nz-peoples-party"] = dict(
    title="New Zealand People's Party (2015–2019)",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request, 30 April 2019; component of Advance NZ in 2020"), ("Founded", "2015; registered 20 June 2017"),
           ("Leaders", "Roshan Nauhria (co-founder); Anil Sharma (2020)"), ("Ideology", "Focus on the rights of immigrants (strong Indian-community base)"), ("Seats", "None")],
    body="""Nauhria came third (4.2%) in the 2016 Mount Roskill by-election; Winston Peters called the party a "National Party
front". It won 1,890 votes (0.07%) in 2017 with six list candidates and joined Advance NZ in 2020. For the 2026
"People's Party New Zealand" electorate candidates see [peoples-party-new-zealand](../peoples-party-new-zealand/README.md)
— our sources do not establish a connection. [1]""",
    notes={"2020": "component of Advance NZ"}, sources=[WP + "New_Zealand_People%27s_Party", "NZ Herald, \"Roshan Nauhria chasing shock win in Roskill\" (1 Dec 2016) — http://www.nzherald.co.nz/nz/news/article.cfm?c_id=1&objectid=11757997", RESULTS_SRC])
P["new-nation"] = dict(
    title="New Nation Party",
    facts=[("Status (Oct 2026)", "**Deregistered** at its own request, 29 January 2025"), ("Founded", "c. 2022; registered 12 April 2023"),
           ("Leaders", "Michael Jacomb; later Guy Slocum"), ("Ideology", "Opposed vaccine mandates, Three Waters and the United Nations"), ("Seats", "None")],
    body="""A founding component of Freedoms NZ, it left in July 2023 to stand on its own and won 1,530 votes (0.05%) — the
lowest of any party in 2023. Its candidate in the 2022 Tauranga by-election, former councillor Andrew Hollis, won 260
votes. [1][2]""",
    notes={}, sources=[WP + "New_Nation_Party", "Electoral Commission, \"Registration of the New Nation Party and logo\" (12 Apr 2023) — https://elections.nz/media-and-news/2023/registration-of-the-new-nation-party-and-logo/ ; \"New Nation Party no longer registered\" (30 Jan 2025) https://elections.nz/media-and-news/2025/new-nation-party-no-longer-registered/", RESULTS_SRC])

for slug, p in P.items():
    d = os.path.join(ROOT, "parties", slug)
    os.makedirs(d, exist_ok=True)
    facts = "\n".join(f"| **{k}** | {v} |" for k, v in p["facts"])
    md = f"# {p['title']}\n\n| | |\n|---|---|\n{facts}\n\n## History\n\n{p['body']}\n\n## Election results (2011–2023)\n\n"
    md += result_rows(slug, p["notes"]) + "\n\n## MPs\n\n" + p.get("mps", "None elected for this party.") + "\n\n## Sources\n\n"
    md += "\n".join(f"{i}. {s if not s.startswith('http') else 'Wikipedia — ' + s}" for i, s in enumerate(p["sources"], 1))
    md += "\n\nLocal copies of the Wikipedia articles: `raw/minor-parties/wiki/`. Electoral Commission pages are cited as referenced by Wikipedia (elections.nz blocks automated access from this environment).\n"
    open(os.path.join(d, "README.md"), "w").write(md)
    print("wrote", slug)
