# How the poll-of-polls and seat forecast work

*Covers `data/forecast.json`, produced by `tools/forecast.py` from `data/polls-2026.json` (refreshed by
`tools/polls_update.py`) and `data/polls-history/*.json`. Written 23 October 2026; the numbers quoted below are from that
day's run and are superseded by whatever `data/forecast.json` currently says. Election day: Saturday 7 November 2026.*

## How to read it (plain English)

1. **Poll average** – where the public polls put each party *today*, after adjusting each pollster for its habitual lean
   and weighting recent, larger polls more. The narrow interval beside it only says how noisy the polls are.
2. **Forecast vote** – the poll average plus two extra kinds of uncertainty: how far New Zealand's final polls have missed
   the result at the last five elections, and how much support can still move before 7 November. This interval is wider,
   and it is the one that matters.
3. **Seats** – we run the real MMP rules (5% or an electorate seat; Sainte-Laguë; 120 seats plus overhang) on 40,000
   simulated election nights. "Expected seats" is the average; the 80% range is where 8 in 10 simulations land.
4. **Bloc majority** – the share of simulations in which those parties alone hold more than half of all seats
   (61 of 120, 62 of 122 or 123). It says the seats would exist, not that the parties would agree to govern.
5. **Rounding is deliberate.** Probabilities are rounded to the nearest 1% and seats to whole numbers because the inputs do
   not support anything finer. A 70% chance means the other outcome happens about 3 times in 10.

## 1. Pooling the polls

**Data.** Every public party-vote poll since the 2023 election, as tabulated on Wikipedia with fieldwork dates, sample
size and a link to the pollster's own release ([Opinion polling for the 2026 New Zealand general election][wp2026]).
`tools/polls_update.py` re-reads that article every six hours through the MediaWiki API, adds new rows, never deletes or
overwrites an existing row, tags each series (`pollster_key`) so renamed series stay together, and marks party- or
corporate-commissioned polls that are published selectively (`internal: true` – Talbot Mills, Anacta, Curia's own
releases). Pollster metadata (who commissions, who does the fieldwork, mode) is stored under `pollsters`.

**Latent trend.** Each party's support is treated as an unobserved quantity that polls measure with noise – the
"pooling the polls" framework of Jackman (2005) [[1]], used for multi-party systems by Linzer (2013) [[2]] and, for New
Zealand, by Peter Ellis's `nz-election-forecast` state-space model for 2017 and 2020 [[3]][[4]]. We use a transparent
non-Bayesian version of the same idea: at any date *t* the estimate is the weighted mean of house-adjusted polls with
fieldwork ending on or before *t*, weight

    w = 2^(−age/21 days) × √(n/1000) × (0.5 if internal)

*Half-life 21 days.* The random-walk state-space models fitted to NZ data imply latent support drifts by roughly
0.1–0.3 points a day for a major party [[3]], so a poll three weeks old carries about half the information of a new
one; with only ~4–6 public polls a month, a shorter half-life makes the average jump around on single polls and a longer
one lags real movement (compare the 2020 campaign, when National fell 5 points in six weeks). Weighting by √n is the
standard inverse-variance weight for a binomial proportion, capped by not letting one 1,700-person poll dominate.
The estimate is **one-sided** (only polls up to *t*), so the weekly trend series shows what was knowable at the time
and the backtest is honest.

**House effects.** Each pollster's house effect for each party is its mean deviation from the pooled trend over the term
(iterated five times so trend and house effects are mutually consistent), shrunk by n/(n+2) and constrained to
**sum to zero across the independent public pollsters** (1 News–Verian, RNZ–Reid Research, Taxpayers' Union–Curia,
Roy Morgan, The Post/Freshwater Strategy). Sum-to-zero is the identifying constraint Jackman used; Ellis instead
anchored house effects to past election results, which is better when pollsters are stable but is not possible for
series that did not exist in 2023 (Freshwater, Anacta). Internal polls receive a house effect but do not anchor the
average. Consequence, stated plainly in the JSON: house effects describe *relative* leans; if every pollster shares a
bias (as in 2020) the average shares it. On 23 Oct 2026 the largest estimated leans were Roy Morgan −2.1 on Labour and
+1.5 on Greens, Talbot Mills +3.0 on Labour, Freshwater and Reid Research +2 on Labour, Verian +1.2 on National.

**Undecided voters.** All NZ pollsters publish shares of decided voters (5–15% undecided excluded), so the polls already
sum to ~100 and no reallocation is done; "others" is implied. The historical calibration below measures the error that
results, so a separate undecided adjustment would double-count.

Outputs: current aggregate with 80%/95% intervals (`parties[].poll_average*`), the weekly trend from Nov 2023
(`trend_weekly`), per-pollster house effects with poll counts and the latest poll from each (`pollsters`).

## 2. Calibrating the error empirically

`tools/polls_update.py` also parses the polling articles for 2011, 2014, 2017, 2020 and 2023 into
`data/polls-history/`. For each election the final-three-weeks pooled average (√n weights, no house adjustment) is
compared with the official party vote (`data/elections/<year>.json`). Results on the 23 Oct 2026 run
(`calibration.error_table` has every row):

| Party size (final polls) | n | RMSE | mean abs error | mean bias (result − polls) |
|---|---|---|---|---|
| ≥20% | 10 | 3.1 | 2.5 | −0.5 |
| 5–20% | 10 | 1.2 | 0.9 | −0.4 |
| <5% | 21 | 0.8 | 0.5 | +0.3 |

Error grows with party size roughly like a binomial proportion, so the model SD is
`k·√(p(100−p))/10` with `k` fitted by least squares on squared errors (k ≈ 0.60: SD 3.0 at 45%, 2.7 at 30%,
1.8 at 10%, 1.3 at 5%, floor 0.6 for tiny parties). Squared error rather than variance is used so that historical bias
*widens* the interval instead of being used to shift the mean – we do not assume a direction. This is the approach
recommended by Shirani-Mehr, Rothschild, Goel and Gelman (2018), who find real-world poll error is about twice the
nominal sampling margin because of shared, non-sampling error [[5]]; the international average absolute error for
final-week polls is ~2 points and has not worsened over time (Jennings & Wlezien 2018, 351 elections) [[6]].

**Direction of past errors, from the data (not assumed):**

- *National* was overstated by the final polls in 2011 (−4.2), 2014 (−0.9) and 2020 (−5.6) and understated in 2017
  (+3.6) and 2023 (+2.5). Largest single-party errors on record; both directions.
- *Greens* were overstated in four of five elections (2011 −1.1, 2014 −2.0, 2017 −0.4, 2023 −1.5; 2020 +0.5).
- *NZ First* was understated in 2011 (+2.8), 2014 (+2.1) and 2020 (+0.1), overstated in 2017 (−0.2) and 2023 (−0.5)
  – so the "polls always understate Winston" rule held for the landline era but not for the last two elections.
- *Labour*: no net bias (mean −0.0) but a 3.7-point overstatement in 2017 and 3.4 understatement in 2020.
- *ACT* slightly overstated in four of five; *Te Pāti Māori* slightly understated in three of five (all < 0.7).

These findings match the 1News retrospective of final-poll accuracy 2002–2023 [[7]] and Ellis's house-effect
analyses of the 2011–2014 pollsters [[8]].

**Correlation.** Errors are correlated across parties: when National is overstated, Labour tends to be understated
(empirical r = −0.86 over five elections, shrunk to −0.54 because five observations cannot pin a correlation down;
pairs need four shared elections; the matrix is forced positive-definite). These correlations feed the multivariate
draws, so "National high and Labour low" scenarios appear at the right frequency rather than independently.

**Movement before election day.** A random-walk drift term, variance per day estimated from this term's own week-to-week
trend changes (half attributed to real movement, half to poll noise), multiplied by the days remaining – the same
random-walk assumption as Jackman and Ellis. Fifteen days out it adds ~0.5 points of SD for a major party.

Total forecast SD per party = √(calibrated error² + aggregate standard error² + drift²), shown in
`parties[].uncertainty`.

## 3. Monte Carlo seat simulation

40,000 draws (fixed seed, so reruns on unchanged data are byte-identical).

1. **Party votes** – a multivariate logit-normal around the poll average with the covariance above. The logit scale
   keeps small parties positive and gives them the right-skewed uncertainty seen historically (a 1.7% party is more
   likely to reach 3% than to fall to 0.4%).
2. **Epsom** – ACT's insurance seat. David Seymour won by 8,142 in 2023 against Paul Goldsmith (National), who stands
   again; no 2026 Epsom poll exists. P(ACT holds) = 0.90. Because ACT polls 9–11% this only matters if ACT falls below 5%.
3. **The seven Māori electorates** – these decide the overhang because Te Pāti Māori's party vote (~1.7%) is far below
   its likely electorate seats. For each seat the decided-voter candidate shares are 0.7 × the mean of the electorate
   polls from the last 45 days (Whakaata Māori–Curia, Mata–Horizon; n≈500–700, listed in
   `electorates.maori_seats[].polls_used`) + 0.3 × the same party's 2023 candidate share (new candidates get a zero
   prior; for the two MPs who have since left Te Pāti Māori, half of their 2023 vote is credited to their new vehicle –
   Mariameno Kapa-Kingi's Te Tai Tokerau Party, Tākuta Ferris as an independent). Each candidate is drawn with
   SD = √(sampling + 9²) points: Māori-roll polls are small and have missed badly before, and incumbency, turnout and the
   split on the left (Labour, Greens, TPM, TTT all competing) make these genuinely uncertain. The 2025 Tāmaki Makaurau
   by-election (Kaipara 6,948 v Henare 3,429, low turnout) is noted as context but the 2023 general-election shares are
   the prior. An independent winner is deducted from the 120 before allocation; a Te Tai Tokerau Party winner makes that
   party eligible for list seats on its (~0.3%) party vote, which yields none, so its seat becomes overhang.
4. **Allocation** – parties with ≥5% or ≥1 electorate seat share the list seats by Sainte-Laguë; each party takes the
   greater of its allocation and its electorate seats (overhang). Verified against 2023 (48/34/15/11/8/4, TPM 6 → 122).
   General electorates won by National, Labour or the Greens are assumed never to exceed their list entitlement, so they
   are not simulated. TOP has no realistic electorate (its 2023 Ilam bid is not repeated), so it lives or dies at 5%.
5. **Outputs** – expected seats and 80%/95% ranges per party, seat histograms, P(≥5%), P(wins an electorate),
   P(in Parliament), probability of a majority for National+ACT+NZ First, Labour+Green+TPM, those blocs with TOP, and
   "no bloc has a majority"; P(TOP holds the balance of power), P(NZ First holds it), P(overhang), total-seat
   distribution, and the single most frequent seat combination.

## 4. Track record (backtest)

The same aggregator – polls to 14 days before each election, house effects from that term, calibration from the *other*
four elections – versus the official result (`historical_track_record.elections`):

| Election | forecast 2 wks out → result (major parties) | biggest miss | inside 80% | inside 95% |
|---|---|---|---|---|
| 2011 | Nat 53.1→47.3, Lab 28.5→27.5, Grn 10.3→11.1, NZF 2.9→6.6 | NZF +3.7, Nat −5.8 (late "teapot tape" swing) | 5/8 | 5/8 |
| 2014 | Nat 48.7→47.0, Lab 25.9→25.1, Grn 12.7→10.7, NZF 5.5→8.7 | NZF +3.1 | 6/7 | 6/7 |
| 2017 | Nat 40.6→44.5, Lab 37.2→36.9, NZF 9.3→7.2, Grn 7.9→6.3 | Nat +3.8 | 6/6 | 6/6 |
| 2020 | Lab 48.8→50.0, Nat 30.4→25.6, Grn 7.5→7.9, ACT 6.7→7.6 | Nat −4.8 | 7/8 | 8/8 |
| 2023 | Nat 36.1→38.1, Lab 26.6→26.9, Grn 12.4→11.6, ACT 11.7→8.6, NZF 5.3→6.1 | ACT −3.1 | 6/7 | 7/7 |
| **All** | | | **30/36 (83%)** | **32/36 (89%)** |

Coverage of 83% for nominal 80% intervals is on target; the 95% intervals are a little narrow (89%), driven by the 2011
NZ First surge and Conservative Party entry that no two-weeks-out poll average could see. The largest party was correctly
identified every time; the 2017 and 2020 National misses show the common NZ pattern of the incumbent-side vote being
mis-measured late.

**Incumbent governments, mid-term poll to polling day** (`incumbent_*` fields): National 2011 50.7 → 47.3 (−3.4);
National 2014 46.3 → 47.0 (+0.8); National 2017 46.8 → 44.5 (−2.4); Labour 2020 48.2 → 50.0 (+1.8, COVID);
Labour 2023 36.0 → 26.9 (−9.1). For 2026, National stood at 33.3 in May 2025 (18 months out) and 28.6 in the
23 Oct 2026 average – already an unusually large fall for a first-term government.

## 5. Caveats (read these)

- **Polling error is the dominant uncertainty.** The final polls missed a major party by 4–6 points in 2011 and 2020.
  Our intervals include those misses, but a miss bigger than anything since 2011 is always possible.
- **Threshold cliffs.** TOP (~6%) and, to a lesser degree, NZ First sit near 5%. A one-point move can shift 6–10 seats
  between blocs, so bloc probabilities are far less certain than vote shares look.
- **Electorate assumptions** (Epsom, Māori seats) rest on a handful of small polls and stated judgements; they are the
  weakest input and are published in full so you can disagree with them.
- **Late swing and undecideds.** About a fifth of voters decide in the final fortnight; advance voting (from 26 Oct)
  blunts this only partly. Polls exclude 5–15% undecided.
- **Shared bias.** House effects are relative; a bias common to all pollsters is invisible until election night.
- **Selective publication.** Internal/corporate polls (Talbot Mills, Anacta, Curia) appear when someone chooses to
  release them; they are down-weighted but still present.
- **No coalition model.** Majority = seats exist, not that a government forms. Post-election bargaining (NZ First, TOP)
  is outside the model.
- **Only seven parties.** A minor party winning an electorate or crossing 5% from nowhere is not simulated.

## 6. Reproducing it

    python3 tools/polls_update.py          # refresh polls (needs network; --offline re-parses the cache)
    python3 tools/forecast.py              # writes data/forecast.json (≈3 s)
    python3 tools/forecast.py --asof 2026-09-01 --out /tmp/f.json   # what it would have said on an earlier date

`.github/workflows/polls.yml` does this every six hours and commits the result (requires GitHub Actions enabled).

## References

[1]: https://doi.org/10.1080/10361140500302472
[2]: https://doi.org/10.1080/01621459.2012.737735
[3]: https://freerangestats.info/elections/state-space
[4]: https://freerangestats.info/blog/2020/06/06/nz-2020-forecasts
[5]: https://doi.org/10.1080/01621459.2018.1448823
[6]: https://doi.org/10.1038/s41562-018-0315-6
[7]: https://www.1news.co.nz/2026/08/28/i-dont-believe-your-poll-politicians-like-to-say-but-are-they-right/
[8]: https://freerangestats.info/blog/2017/09/09/nzpolls-again
[wp2026]: https://en.wikipedia.org/wiki/Opinion_polling_for_the_2026_New_Zealand_general_election

1. Jackman, S. (2005). "Pooling the polls over an election campaign." *Australian Journal of Political Science* 40(4),
   499–517. https://doi.org/10.1080/10361140500302472
2. Linzer, D. A. (2013). "Dynamic Bayesian forecasting of presidential elections in the states." *Journal of the
   American Statistical Association* 108(501), 124–134. https://doi.org/10.1080/01621459.2012.737735
3. Ellis, P. (2017). *New Zealand general election forecasts – state space model* (Free Range Statistics) and
   "Forecasting New Zealand elections with R and Stan" (WRUG talk). https://freerangestats.info/elections/state-space ;
   code: https://github.com/ellisp/nz-election-forecast
4. Ellis, P. (2020). "Forecasts for the 2020 New Zealand elections using R and Stan."
   https://freerangestats.info/blog/2020/06/06/nz-2020-forecasts
5. Shirani-Mehr, H., Rothschild, D., Goel, S. & Gelman, A. (2018). "Disentangling bias and variance in election polls."
   *Journal of the American Statistical Association* 113(522), 607–614. https://doi.org/10.1080/01621459.2018.1448823
6. Jennings, W. & Wlezien, C. (2018). "Election polling errors across time and space." *Nature Human Behaviour* 2,
   276–283. https://doi.org/10.1038/s41562-018-0315-6
7. 1News (28 Aug 2026). "'I don't believe your poll', politicians like to say. But are they right?"
   https://www.1news.co.nz/2026/08/28/i-dont-believe-your-poll-politicians-like-to-say-but-are-they-right/
8. Ellis, P. (2017). "House effects in New Zealand voting intention polls" and "The long view on New Zealand political
   polls." https://freerangestats.info/blog/2017/09/09/nzpolls-again
9. Electoral Commission. "What is MMP?" (threshold, Sainte-Laguë, overhang).
   https://elections.nz/democracy-in-nz/what-is-new-zealands-system-of-government/what-is-mmp/
10. Wikipedia. Opinion polling for the 2011, 2014, 2017, 2020, 2023 and 2026 New Zealand general elections (poll tables
    with source links); results from `data/elections/<year>.json` (Electoral Commission official counts).
