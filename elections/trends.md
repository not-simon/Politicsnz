# Trends across New Zealand elections, 2008–2023 (and polling to 2026)

> Data: [`data/elections/`](../data/elections/) (one JSON per election), [`data/parliaments/`](../data/parliaments/) (50th–54th
> Parliaments), [`data/polls-2026.json`](../data/polls-2026.json). Narratives: [2011](2011.md) · [2014](2014.md) · [2017](2017.md) ·
> [2020](2020.md) · [2023](2023.md) · [2026 (upcoming)](2026.md). Tables between `GENERATED` markers are rebuilt from the JSON by
> `tools/elections_md.py`; run `tools/elections_validate.py` to check seat arithmetic and slugs. 2008 is included as a baseline.

## 1. Party vote share (%)

<!-- GENERATED:vote-share START -->
| Party | 2008 | 2011 | 2014 | 2017 | 2020 | 2023 |
|---|---:|---:|---:|---:|---:|---:|
| National | 44.93 | 47.31 | 47.04 | 44.45 | 25.58 | 38.08 |
| Labour | 33.99 | 27.48 | 25.13 | 36.89 | 50.01 | 26.92 |
| Green | 6.72 | 11.06 | 10.70 | 6.27 | 7.86 | 11.61 |
| ACT | 3.65 | 1.07 | 0.69 | 0.50 | 7.59 | 8.64 |
| NZ First | 4.07 | 6.59 | 8.66 | 7.20 | 2.60 | 6.09 |
| Te Pāti Māori / Māori Party | 2.39 | 1.43 | 1.32 | 1.18 | 1.17 | 3.08 |
| TOP | – | – | – | 2.44 | 1.51 | 2.22 |
| Conservative / New Conservative | – | 2.65 | 3.97 | 0.24 | 1.48 | 0.16 |
| United Future | 0.87 | 0.60 | 0.22 | 0.07 | – | – |
| Mana | – | 1.08 | – | 0.14 | – | – |
| Internet MANA | – | – | 1.42 | – | – | – |
| Legalise Cannabis | 0.41 | 0.52 | 0.46 | 0.31 | 0.46 | 0.46 |
| NZ Loyal | – | – | – | – | – | 1.21 |
<!-- GENERATED:vote-share END -->

**Reading it.** The two big parties alternate in long arcs: National held 44–47% for three elections (2008–2017), collapsed to
25.6% in 2020 and recovered to 38.1% in 2023; Labour fell to 25–27% in 2011–14, surged under Ardern (36.9% → 50.0%) and then lost
half its vote in 2023 (26.9%). The Greens are the most stable minor party (6–12%). ACT went from near-extinction (0.5–1.1%, kept alive
only by Epsom) to 7.6–8.6% after 2020. NZ First is the "comeback" party – out in 2008, back in 2011, kingmaker in 2017, out in 2020,
in government again in 2023.

## 2. Seats (total, electorate + list)

<!-- GENERATED:seats START -->
| Party | 2008 | 2011 | 2014 | 2017 | 2020 | 2023 |
|---|---:|---:|---:|---:|---:|---:|
| National | 58 (41+17) | 59 (42+17) | 60 (41+19) | 56 (41+15) | 33 (23+10) | 49 (44+5) |
| Labour | 43 (21+22) | 34 (22+12) | 32 (27+5) | 46 (29+17) | 65 (46+19) | 34 (17+17) |
| Green | 9 (0+9) | 14 (0+14) | 14 (0+14) | 8 (0+8) | 10 (1+9) | 15 (3+12) |
| ACT | 5 (1+4) | 1 (1+0) | 1 (1+0) | 1 (1+0) | 10 (1+9) | 11 (2+9) |
| NZ First | 0 | 8 (0+8) | 11 (0+11) | 9 (0+9) | 0 | 8 (0+8) |
| Te Pāti Māori / Māori Party | 5 (5+0) | 3 (3+0) | 2 (1+1) | 0 | 2 (1+1) | 6 (6+0) |
| TOP | – | – | – | 0 | 0 | 0 |
| Conservative / New Conservative | – | 0 | 0 | 0 | 0 | 0 |
| United Future | 1 (1+0) | 1 (1+0) | 1 (1+0) | 0 | – | – |
| Mana | – | 1 (1+0) | – | 0 | – | – |
| **Total** | 122 | 121 | 121 | 120 | 120 | 123 |

Format: total (electorate + list). 2023 includes the Port Waikato by-election seat.
<!-- GENERATED:seats END -->

## 3. Turnout, overhang and the "wasted" vote

<!-- GENERATED:turnout START -->
| Year | Enrolled | Votes cast | Turnout % | Overhang | Parties winning seats | Parties on ballot (party vote) | 'Wasted' party vote % |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2008 | 2,990,759 | 2,376,480 | 79.46 | 2 | 7 | 19 | 6.55 |
| 2011 | 3,070,847 | 2,278,989 | 74.21 | 1 | 8 | 13 | 3.37 |
| 2014 | 3,140,417 | 2,446,297 | 77.9 | 1 | 7 | 15 | 6.24 |
| 2017 | 3,298,009 | 2,630,173 | 79.75 | 0 | 5 | 16 | 4.68 |
| 2020 | 3,549,580 | 2,919,073 | 82.24 | 0 | 5 | 17 | 7.8 |
| 2023 | 3,688,292 | 2,884,111 | 78.2 | 3 | 6 | 17 | 5.58 |
<!-- GENERATED:turnout END -->

- **Turnout** (votes cast ÷ enrolled) ranged from 74.21% (2011, the lowest since 1887) to 82.24% (2020). Turnout of the *eligible*
  population is lower because not everyone enrols; youth enrolment fell to 53% by mid-2026 before a late push (65.5% of 18–24s by
  15 Oct 2026, per the Electoral Commission as reported on Wikipedia).
- **The 5% threshold and the wasted vote.** "Wasted" here = party votes for parties that won no seats, as a share of valid party
  votes. It peaked at **7.8% in 2020** (NZ First 2.6%, TOP 1.5%, New Conservative 1.5%, Advance NZ 1.0%) and was 6.2–6.6% in 2008
  and 2014 (NZ First 4.07% in 2008; the Conservatives 3.97% in 2014). Wasted votes are redistributed in effect to parties that did
  qualify – one reason Labour's 50.0% in 2020 produced 54% of the seats. The Electoral Commission's 2012 MMP review recommended
  lowering the threshold to 4%; it was never legislated.
- **Overhang.** Overhang seats arise when a party wins more electorates than its party-vote entitlement: the Māori Party in 2008
  (+2) and 2011 (+1), United Future in 2014 (+1), and Te Pāti Māori in 2023 (+2) plus the Port Waikato by-election (+1), giving a
  **123-seat House** – the largest under MMP. 2017 and 2020 had none.

## 4. The two-party vote and swing

<!-- GENERATED:two-party START -->
| Election | National % | Labour % | Nat–Lab gap (pp) | Two-party combined % | Largest party | Govt formed by |
|---|---:|---:|---:|---:|---|---|
| 2008 | 44.93 | 33.99 | +10.94 | 78.92 | National | National |
| 2011 | 47.31 | 27.48 | +19.83 | 74.79 | National | National |
| 2014 | 47.04 | 25.13 | +21.91 | 72.17 | National | National |
| 2017 | 44.45 | 36.89 | +7.56 | 81.34 | National | Labour, NZ First |
| 2020 | 25.58 | 50.01 | -24.43 | 75.59 | Labour | Labour |
| 2023 | 38.08 | 26.92 | +11.16 | 65.00 | National | National, ACT, NZ First |
<!-- GENERATED:two-party END -->

- The combined National+Labour vote was highest in 2017 (81.3%) and lowest in 2023 (65.0%, the lowest since 2002), when minor
  parties (Greens, ACT, NZ First, TPM) won 29.4%.
- **Swing.** 2017→2020 was a ~19 pp National→Labour swing on the party vote; 2020→2023 a 12.5 pp swing back to National and a 23 pp fall
  for Labour – the largest defeat of a sitting government under MMP. The 2017 election is the only one here where the largest party
  (National) did not form the government.
- **Rise-and-fall cycle.** Each major party has followed a "three-term" pattern: Fifth National Government 2008–17 (three terms);
  Sixth Labour Government 2017–23 (two terms, ending in a landslide defeat after a landslide win). Polling through 2025–26 suggests the
  2023 coalition faces a close contest after one term (see §8).

## 5. Minor parties: who survived

| Party | Fate 2008–2023 |
|---|---|
| Greens | In Parliament every election; first electorate since 1999 in 2020 (Auckland Central), three electorates in 2023 |
| ACT | Survived 2011–2017 on Epsom alone (0.5–1.1%); 10–11 seats since 2020; in coalition 2023 |
| NZ First | Out 2008 (4.07%), in 2011–2017 (kingmaker 2017), out 2020 (2.6%), in coalition 2023 (6.09%) |
| Māori Party / Te Pāti Māori | Support partner to National 2008–17; wiped out 2017; back 2020 via Waiariki; six Māori seats 2023; split 2025–26 |
| United Future | One seat (Ōhāriu) 2008–14 via Peter Dunne; 0.07% and gone in 2017 |
| Progressive | Jim Anderton's Wigram until 2011 |
| Mana / Internet MANA | Te Tai Tokerau 2011–14 (Hone Harawira); lost it in 2014 despite the Internet Party's money |
| Conservative / New Conservative | 2.65% (2011), 3.97% (2014) – the biggest near-miss – then 0.2–1.5%; now "Conservative Party NZ" |
| TOP (Opportunity) | 2.44% (2017), 1.51% (2020), 2.22% (2023); polling 5–8% in late 2026 |
| COVID-era parties | Advance NZ 0.98% (2020); NZ Loyal 1.21%, Freedoms NZ 0.34%, DemocracyNZ 0.24% (2023) |

## 6. Electorate deals ("coat-tailing"): Epsom and Ōhāriu

Under MMP a party that wins **one electorate** gets its full party-vote share of seats even below 5%. National repeatedly signalled to
its Epsom (and Ōhāriu) voters to back ACT's (and United Future's) candidate – the 2011 "tea tape" meeting is the best-known example.

<!-- GENERATED:deals START -->
| Year | Epsom winner (majority) | Ōhāriu/Ohariu winner (majority) | Party vote of the winner's party | Seats the deal delivered |
|---|---|---|---|---|
| 2008 | Rodney Hide (ACT, 12,882) | Peter Dunne (United Future, 1,006) | ACT 3.65%; United Future 0.87% | ACT 5, UF 1 |
| 2011 | John Banks (ACT, 2,261) | Peter Dunne (United Future, 1,392) | ACT 1.07%; United Future 0.6% | ACT 1, UF 1 |
| 2014 | David Seymour (ACT, 4,250) | Peter Dunne (United Future, 710) | ACT 0.69%; United Future 0.22% | ACT 1, UF 1 |
| 2017 | David Seymour (ACT, 5,519) | Greg O'Connor (Labour, 1,051) | ACT 0.5%; United Future 0.07% | ACT 1, UF 0 |
| 2020 | David Seymour (ACT, 9,224) | Greg O'Connor (Labour, 11,961) | ACT 7.59% | ACT 10 |
| 2023 | David Seymour (ACT, 8,142) | Greg O'Connor (Labour, 1,260) | ACT 8.64% | ACT 11 |
<!-- GENERATED:deals END -->

- In 2008 Epsom brought in **four extra ACT list MPs** (3.65% → 5 seats) – the clearest coat-tail effect in this period.
- 2011–2017 ACT's party vote was so low that Epsom delivered only the electorate MP; United Future's Ōhāriu seat in 2014 was an overhang.
- 2014's attempted coat-tail for Internet MANA failed when Labour's Kelvin Davis beat Hone Harawira in Te Tai Tokerau (with public
  endorsements from John Key and Winston Peters).
- From 2020 ACT no longer needed Epsom; in 2023 National formally contested it, and Seymour still won by 8,142.
- The 2012 MMP review recommended abolishing the one-electorate threshold; Parliament did not act.

## 7. The Māori electorates

<!-- GENERATED:maori START -->
| Electorate | 2008 | 2011 | 2014 | 2017 | 2020 | 2023 |
|---|---|---|---|---|---|---|
| Hauraki-Waikato | Labour – Nanaia Mahuta (888) | Labour – Nanaia Mahuta (5,935) | Labour – Nanaia Mahuta (7,695) | Labour – Nanaia Mahuta (9,223) | Labour – Nanaia Mahuta (9,660) | Te Pāti Māori – Hana-Rawhiti Maipi-Clarke (2,911) |
| Ikaroa-Rāwhiti | Labour – Parekura Horomia (1,645) | Labour – Parekura Horomia (6,541) | Labour – Meka Whaitiri (4,673) | Labour – Meka Whaitiri (4,210) | Labour – Meka Whaitiri (6,045) | Labour – Cushla Tangaere-Manuel (2,874) |
| Te Tai Hauāuru | Te Pāti Māori – Tariana Turia (7,817) | Te Pāti Māori – Tariana Turia (3,221) | Labour – Adrian Rurawhe (1,554) | Labour – Adrian Rurawhe (1,039) | Labour – Adrian Rurawhe (1,053) | Te Pāti Māori – Debbie Ngarewa-Packer (9,162) |
| Te Tai Tokerau | Te Pāti Māori – Hone Harawira (6,308) | Mana – Hone Harawira (1,165) | Labour – Kelvin Davis (743) | Labour – Kelvin Davis (4,807) | Labour – Kelvin Davis (8,164) | Te Pāti Māori – Mariameno Kapa-Kingi (517) |
| Te Tai Tonga | Te Pāti Māori – Rahui Katene (1,049) | Labour – Rino Tirikatene (1,475) | Labour – Rino Tirikatene (3,554) | Labour – Rino Tirikatene (4,676) | Labour – Rino Tirikatene (6,855) | Te Pāti Māori – Tākuta Ferris (2,824) |
| Tāmaki Makaurau | Te Pāti Māori – Pita Sharples (7,540) | Te Pāti Māori – Pita Sharples (936) | Labour – Peeni Henare (1,462) | Labour – Peeni Henare (3,809) | Labour – Peeni Henare (927) | Te Pāti Māori – Takutai Tarsh Kemp (42) |
| Waiariki | Te Pāti Māori – Te Ururoa Flavell (6,812) | Te Pāti Māori – Te Ururoa Flavell (1,883) | Te Pāti Māori – Te Ururoa Flavell (3,889) | Labour – Tāmati Coffey (1,719) | Te Pāti Māori – Rawiri Waititi (836) | Te Pāti Māori – Rawiri Waititi (15,891) |
| **Tally** | Te Pāti Māori 5, Labour 2 | Labour 3, Te Pāti Māori 3, Mana 1 | Labour 6, Te Pāti Māori 1 | Labour 7 | Labour 6, Te Pāti Māori 1 | Te Pāti Māori 6, Labour 1 |
<!-- GENERATED:maori END -->

The seven Māori seats swing as a bloc between Labour and the Māori Party/Te Pāti Māori: Māori Party 5 (2008) → Labour 6 (2014) →
Labour 7 (2017) → Te Pāti Māori 6 (2023). Many Māori-roll voters split their votes (electorate TPM, party vote Labour/Green), which is
why TPM's 3.08% party vote in 2023 sat alongside six electorates – and two overhang seats. More than half of ethnic-Māori voters
(302,096) were on the Māori roll in July 2026. National stood in Māori seats in 2023 for the first time since 2002.

## 8. Polling, 2023–2026

<!-- GENERATED:polls START -->
| Quarter | Polls | National | Labour | Green | ACT | NZ First | Te Pāti Māori | TOP | Nat+ACT+NZF | Lab+Grn+TPM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023 Q4 | 4 | 36.8 | 25.0 | 13.2 | 9.1 | 7.0 | 4.0 | 3.5 | 52.9 | 42.1 |
| 2024 Q1 | 9 | 38.2 | 25.9 | 12.5 | 9.5 | 6.2 | 3.6 | 2.5 | 53.9 | 42.0 |
| 2024 Q2 | 10 | 35.8 | 29.1 | 13.1 | 8.5 | 5.6 | 3.9 | 1.8 | 49.9 | 46.1 |
| 2024 Q3 | 7 | 36.8 | 26.9 | 12.2 | 9.1 | 6.8 | 4.3 | 2.4 | 52.7 | 43.4 |
| 2024 Q4 | 11 | 33.8 | 29.6 | 11.3 | 9.7 | 6.4 | 5.1 | 1.9 | 49.8 | 45.9 |
| 2025 Q1 | 10 | 32.1 | 31.5 | 11.6 | 9.3 | 6.5 | 4.9 | 1.9 | 47.9 | 48.0 |
| 2025 Q2 | 10 | 32.9 | 31.2 | 10.9 | 9.3 | 7.7 | 4.0 | 2.0 | 49.8 | 46.1 |
| 2025 Q3 | 11 | 32.0 | 33.1 | 11.1 | 8.4 | 8.6 | 3.9 | 1.9 | 49.0 | 48.1 |
| 2025 Q4 | 12 | 31.7 | 33.3 | 10.4 | 8.1 | 9.5 | 2.8 | 1.6 | 49.4 | 46.5 |
| 2026 Q1 | 12 | 31.1 | 34.0 | 10.5 | 7.7 | 10.2 | 2.8 | 2.2 | 49.0 | 47.2 |
| 2026 Q2 | 12 | 29.3 | 32.8 | 10.8 | 8.0 | 12.0 | 2.5 | 3.9 | 49.2 | 46.1 |
| 2026 Q3 | 14 | 29.7 | 29.2 | 12.2 | 8.6 | 10.2 | 2.2 | 6.1 | 48.5 | 43.5 |
| 2026 Q4 | 7 | 28.4 | 28.5 | 14.9 | 9.5 | 10.3 | 1.3 | 6.2 | 48.2 | 44.7 |

Simple unweighted mean of all published polls whose fieldwork ended in the quarter (from `data/polls-2026.json`); not a forecast.
<!-- GENERATED:polls END -->

- **Honeymoon then slide.** National polled ~37–41% into early 2024, then drifted to ~29–31% by 2026; Labour climbed from ~26% to
  ~33–34% in 2025–early 2026 and led most polls, before falling back to ~28–29% by October 2026.
- **Blocs.** The governing bloc (National+ACT+NZ First) averaged 48–54% throughout because NZ First rose from ~6% to 10–12% as National
  fell. The Labour+Green+TPM bloc peaked at ~48% in 2025.
- **Late-campaign movers.** The Greens rose to ~15% and TOP to 5–8% in September–October 2026 (potentially clearing 5%); Te Pāti Māori
  fell below 2% after its 2025 split.
- Polls differ by pollster: the series combines Roy Morgan (online/phone monthly), Taxpayers' Union–Curia, 1 News–Verian,
  RNZ–Reid Research, The Post/Freshwater, Talbot Mills (Labour's pollster) and others – see each row's `source_url`.

## 9. Parliament turnover

| Parliament | Members who served | Start → end seats | Mid-term changes | By-elections |
|---|---:|---|---:|---|
| 50th (2011–14) | 129 | 121 → 120 | 12 | Ikaroa-Rāwhiti 2013, Christchurch East 2013 |
| 51st (2014–17) | 127 | 121 → 119 | 10 | Northland 2015 (NZ First gain), Mount Roskill 2016, Mount Albert 2017 |
| 52nd (2017–20) | 125 | 120 → 119 | 7 | Northcote 2018 |
| 53rd (2020–23) | 126 | 120 → 119 | 10 | Tauranga 2022, Hamilton West 2022 (National gain) |
| 54th (2023–26) | 137 | 123 → 122 | 22 | Port Waikato 2023 (delayed electorate vote), Tāmaki Makaurau 2025 |

The 54th Parliament had the most turnover in this period – deaths (Efeso Collins, Takutai Tarsh Kemp), the first expulsion under the
waka-jumping law (Darleen Tana), two Te Pāti Māori expulsions, and seven Labour list MPs replaced.

## Sources

- Wikipedia election and results articles for 2008, 2011, 2014, 2017 (and "Results of the 2017…"), 2020 (and "Results of the 2020…"),
  2023 and 2026; Wikipedia articles on the 50th–54th Parliaments; each electorate's Wikipedia article (official-count vote tables
  citing electionresults.govt.nz); "Opinion polling for the 2026 New Zealand general election". All retrieved 23 Oct 2026; raw copies
  in `raw/elections/`.
- Electoral Commission official results (archive.electionresults.govt.nz / electionresults.govt.nz) are the primary source cited by
  those articles; they were blocked by Cloudflare from the research environment and so were not fetched directly.
