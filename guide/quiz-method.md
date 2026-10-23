# "Find your match" quiz: how it works

The quiz data is in [`data/guide/quiz.json`](../data/guide/quiz.json). It is built by `tools/quiz_build.py` from the hand-checked records in `tools/quiz_data.py`. The quiz works like Vote Compass or the policy.nz matcher. You rate statements from "strongly disagree" to "strongly agree", and the quiz shows how close each party's **public record** is to your answers.

It is a conversation starter, not a voting instruction. Read the parties' own policies (see `parties/<party>/policies/`) before you decide.

## 1. How the statements were chosen

We picked 45 statements. Each one had to meet four tests:

1. **It is a real 2026 dividing line.** At least two parties take clearly different public positions on it, or a recent law or vote split Parliament. Statements that every party agrees with (for example "Pharmac should get more money") were left out.
2. **It is concrete.** Where possible it names a specific mechanism, such as a 28% capital gains tax, the Fast-track Approvals Act, the Regulatory Standards Act, an age of 65 or 2% of GDP. Vague aims like "a fairer economy" were not used.
3. **It is neutrally worded.** Each statement is a plain proposal that a reasonable person could agree or disagree with. Where possible the wording avoids party names and loaded terms. Some statements say "should" and others propose reversing a change, to limit "agree-bias".
4. **It is spread across the main issues.** The issues are tax, cost of living, work, housing, health, education, crime and justice, climate, environment, energy, Te Tiriti and co-governance, democracy, local government, immigration, superannuation, welfare, transport, agriculture, foreign policy, defence, drugs and social issues.

Every statement has a one-sentence `explainer` giving neutral background.

## 2. How party positions were recorded

Each cell is `{position, evidence, source_url, policy_id?}` or `null`.

| Score | Meaning | When we used it |
|---:|---|---|
| +2 | Strongly agree | Explicit policy commitment, a "Yes" survey answer, or voting for the measure |
| +1 | Agree | Supports the direction with a material qualification, or a weaker version |
| 0 | Mixed or neutral | The party said it would neither push for nor oppose it, or its statements conflict (e.g. voted one way and later said the opposite) |
| −1 | Disagree | Opposes the direction with qualifications, or has a stated contrary approach |
| −2 | Strongly disagree | Explicit opposition, a "No" survey answer, or voting against the measure |
| `null` | No position found | Absence of evidence. **This is not a guess, and it does not count as neutral.** |

The rules we followed:

- **We never guess.** If we could not find a public statement, vote, policy document or survey answer, the cell is `null`. Where a party has said nothing, we did not infer a position from its general philosophy (for example "lower taxes" does not count as opposing a wealth tax).
- **A survey answer of "No change" is not counted as opposition.** It only means the party has not proposed the policy, so those cells are `null`.
- **Evidence is a short quote or close paraphrase.** Each cell has a `source_url` for the party page, PDF, Hansard-based record, survey answer or news report. When the cell matches a policy.nz statement, its id (e.g. `POL54670`) is in `policy_id`, so the full policy.nz summary and citations can be shown.
- **Sources, in order of preference:**
  1. Party policy documents and releases. These are archived verbatim under `parties/*/policies/documents/`, and the policy.nz dataset is in `raw/policy.nz/parties/*.json`.
  2. Recorded parliamentary votes on the relevant bill: Treaty Principles Bill second reading (10 Apr 2025), Regulatory Standards Bill, Fast-track Approvals Act, the reinstated three-strikes law and the Crown Minerals Amendment Act 2025.
  3. Party answers to 2026 election questionnaires: Greenpeace's environmental scorecard methodology, which quotes party answers in full; NZCTU's worker scorecards; and Grey Power's superannuation questionnaire.
  4. The KPMG 2026 tax policy tracker, and reputable news (RNZ, 1News, ODT, Te Ao Māori News).
- **Where we relied on a third party's assessment rather than the party's own words, the evidence says so.** For example, "Greenpeace assessment" is used where National and ACT did not answer and Greenpeace scored them from their voting record. Older statements are dated in the evidence text, such as Te Pāti Māori's May 2023 superannuation position.
- **Votes and policies can point different ways.** For example, NZ First voted for the Regulatory Standards Act and later said it would repeal it. We record this as 0 and explain it in the evidence.

Downloaded source material used only for the quiz is in `raw/quiz/`. It includes the KPMG tracker, the Greenpeace methodology, NZCTU scorecards, Grey Power responses, Alliance PDFs and the cached pages and Wikipedia extracts we checked.

## 3. Suggested scoring method

For each statement *i* that **both** the user and the party answered:

```
agreement_i = 1 − |user_i − party_i| / 4          (1 = identical, 0 = opposite ends)
```

The user can set an importance weight *w_i* for each statement: 0.5 for "less important", 1 for "normal" (the default) and 2 for "very important". A user can also skip a statement.

```
raw_match = Σ w_i · agreement_i / Σ w_i            (over statements both answered)
```

**Correcting for coverage.** A party with only two recorded positions could score 100% by luck. To stop thin records being over-rewarded, we shrink each party's score toward the neutral 0.5 by a few "phantom" neutral statements (k = 3):

```
match = (Σ w_i · agreement_i + k · 0.5) / (Σ w_i + k)
```

**What to show the user** for each party:

- the match % (adjusted);
- **coverage**, meaning "based on N of your M answers";
- a "limited information" badge when N < 10;
- the per-statement breakdown with each party's evidence quote and source link.

Parties should be ranked by the adjusted match. The raw match can be shown on request.

A worked example: a user answers 40 statements. Party A has positions on 35 of them, with a raw match of 0.70 and an adjusted match of (35·0.70 + 1.5)/(35 + 3) = 0.68. Party B has positions on 2, with a raw match of 1.00 and an adjusted match of (2 + 1.5)/5 = 0.70. Party B would still rank close to the top, but it would carry the "based on 2 of your 40 answers" badge.

Using no shrinkage at all (k = 0) is reasonable if coverage is shown very prominently. We suggest a k between 3 and 5.

## 4. Limitations

- **Coverage is uneven.** The seven parties covered by policy.nz have far more positions recorded than the ten smaller parties. Many small parties publish only a few single-issue policies, so their match scores are much less reliable.
- **Positions are a snapshot as of 23 October 2026.** Parties are still releasing policy before the 7 November election. National, for example, had not released a detailed superannuation policy, and Labour said its full manifesto was still to come.
- **The 5-point coding involves judgement.** Choosing between +1 and +2 or between −1 and −2 is a judgement call. We applied the same rules to every party, and the evidence for every cell is shown so readers can check it.
- **Third-party scorecards have their own framing.** The Greenpeace and NZCTU questions are advocacy-group questions. We only used the party's own answer, or the voting-record evidence cited, and not the group's grade.
- **Votes are not always policy.** Voting against a bill does not always mean a party would repeal the law. Where a party has said what it would do, that statement is used ahead of the vote.
- **Conscience issues are mostly `null`.** Most parties have no party line on issues such as abortion and cannabis, so most cells for those statements are `null`.
- **Matching on policies is not the whole picture.** The quiz ignores competence, record in government, coalition options and which party is likely to deliver. The track-record files in `parties/<party>/track-record.md` cover some of this.
- **Statement selection shapes the results.** Different statements would give different matches. We aimed for a broad and balanced set, but no set is neutral.

## 5. Coverage

Coverage is regenerated by `tools/quiz_build.py`.

<!-- GENERATED:quiz-coverage START -->
Statements: **45**. Cells filled: **272** of 765.

| Party | Positions recorded | Coverage | Agree (+1/+2) | Neutral (0) | Disagree (−1/−2) | via policy.nz id |
|---|---:|---:|---:|---:|---:|---:|
| Green | 40 | 89% | 27 | 0 | 13 | 29 |
| National | 31 | 69% | 11 | 0 | 20 | 11 |
| ACT | 31 | 69% | 11 | 0 | 20 | 16 |
| Labour | 30 | 67% | 18 | 2 | 10 | 12 |
| NZ First | 27 | 60% | 14 | 2 | 11 | 9 |
| Te Pāti Māori | 23 | 51% | 15 | 0 | 8 | 9 |
| Opportunity (TOP) | 22 | 49% | 17 | 1 | 4 | 16 |
| Alliance | 22 | 49% | 17 | 0 | 5 | 0 |
| Conservative | 11 | 24% | 6 | 0 | 5 | 0 |
| Vision NZ | 8 | 18% | 7 | 0 | 1 | 0 |
| Te Tai Tokerau Party | 7 | 16% | 4 | 0 | 3 | 0 |
| Animal Justice | 6 | 13% | 6 | 0 | 0 | 0 |
| Women's Rights | 5 | 11% | 4 | 0 | 1 | 0 |
| NZ Loyal | 3 | 7% | 1 | 0 | 2 | 0 |
| NZ Outdoors & Freedom | 2 | 4% | 1 | 0 | 1 | 0 |
| Legalise Cannabis | 2 | 4% | 2 | 0 | 0 | 0 |
| Free Palestine | 2 | 4% | 1 | 0 | 1 | 0 |

| # | Issue | Statement | Parties with a position |
|---|---|---|---:|
| q01 | tax | Profits from selling investment property and commercial property should be taxed, with the family home exempt. | 5 |
| q02 | tax | People with very large fortunes (for example net wealth above several million dollars) should pay an annual wealth tax. | 7 |
| q03 | cost-of-living | GST should be taken off food such as fresh fruit and vegetables. | 3 |
| q04 | tax | The first slice of everyone's income (for example the first $10,000 or more) should be tax-free. | 5 |
| q05 | cost-of-living | The government should force the two big supermarket groups to be broken up or restructured so more chains compete. | 6 |
| q06 | work | The minimum wage should rise every year by at least the rate of inflation. | 8 |
| q07 | work | Pay and conditions should be able to be set for a whole industry at once (for example all cleaners or all supermarket workers) through compulsory bargaining between unions and employers. | 9 |
| q08 | housing | There should be a legal limit on how much a landlord can raise the rent each year. | 5 |
| q09 | housing | The government should build a lot more state and public housing itself. | 7 |
| q10 | housing | Councils should have to allow more and denser housing, such as townhouses and apartments, in our cities. | 4 |
| q11 | health | Everyone should get some free GP visits each year, paid for by the government. | 4 |
| q12 | health | The $5 charge for each prescription should be scrapped for everyone. | 2 |
| q13 | education | Free school lunches should be expanded and made more generous, even if it costs more. | 3 |
| q14 | education | Privately run but publicly funded schools (charter schools) should continue to be allowed alongside state schools. | 3 |
| q15 | education | University and polytechnic study should be fees-free. | 4 |
| q16 | crime-justice | Anyone convicted of a third serious violent or sexual offence should get a mandatory longer sentence, with little room for the judge to decide otherwise. | 8 |
| q17 | crime-justice | We should send fewer people to prison and put more into rehabilitation and community-based sentences. | 8 |
| q18 | climate | Farmers should pay for their greenhouse gas emissions, for example by bringing agriculture into the Emissions Trading Scheme. | 10 |
| q19 | climate | New Zealand should keep its legal target of net-zero emissions by 2050 and stay in the Paris climate agreement. | 9 |
| q20 | environment | Ministers should be able to approve big infrastructure, mining and development projects through a faster process that bypasses the normal environmental consent system. | 8 |
| q21 | environment | Seabed mining should be banned in New Zealand waters. | 8 |
| q22 | energy | New offshore oil and gas exploration should be banned again. | 10 |
| q23 | energy | The government should take a bigger direct role in electricity, such as setting up a new state-owned power company or splitting the big power companies into separate generators and retailers. | 6 |
| q24 | te-tiriti | Parliament should write a single legal definition of the principles of the Treaty of Waitangi, rather than leaving the courts and the Waitangi Tribunal to interpret them case by case. | 6 |
| q25 | te-tiriti | The Waitangi Tribunal should be abolished or replaced once historical claims are settled. | 5 |
| q26 | te-tiriti | The Māori electorates should be abolished, or their future put to a referendum. | 2 |
| q27 | te-tiriti | Public services such as health should be targeted by need alone, with no programmes aimed specifically at Māori or other ethnic groups. | 10 |
| q28 | democracy | A recent law that requires every new piece of legislation to be checked against a fixed list of "good regulation" principles, including protecting private property rights, should be scrapped. | 8 |
| q29 | democracy | Political donations should be capped, and only individual New Zealand voters should be allowed to donate. | 6 |
| q30 | local-government | Central government should cap how much councils can raise rates each year. | 4 |
| q31 | immigration | Overall immigration to New Zealand should be reduced. | 4 |
| q32 | immigration | New residents should have to wait longer (five years or more) before they can get most benefits. | 3 |
| q33 | superannuation | The age for receiving NZ Superannuation should stay at 65. | 8 |
| q34 | welfare | Main benefits (such as Jobseeker and Sole Parent Support) should be substantially increased. | 8 |
| q35 | welfare | People on benefits should face tougher obligations and sanctions, such as drug testing or payment cuts if they do not meet requirements. | 9 |
| q36 | transport | Transport money should go mainly to public transport, cycling and rail rather than new highways. | 7 |
| q37 | agriculture | Rules limiting farm pollution of rivers (such as limits on nitrogen fertiliser and stock numbers) should be strengthened rather than loosened. | 8 |
| q38 | agriculture | Rules on gene technology (genetic modification) should be relaxed so modified crops and organisms can be used outside the laboratory. | 8 |
| q39 | foreign-policy | New Zealand should formally recognise the State of Palestine now. | 6 |
| q40 | defence | Defence spending should rise substantially, towards 2% of GDP. | 6 |
| q41 | foreign-policy | New Zealand should increase its overseas aid budget. | 4 |
| q42 | drugs | Cannabis should be legalised or decriminalised for personal use. | 4 |
| q43 | social-issues | Children under 16 should be banned from social media. | 5 |
| q44 | social-issues | Puberty blockers and other medical gender-transition treatments should not be available to people under 18. | 6 |
| q45 | social-issues | Abortion law should be made more restrictive. | 3 |
<!-- GENERATED:quiz-coverage END -->

## 6. Reproduce or extend

```
python3 -I tools/quiz_build.py              # validates every cell and writes data/guide/quiz.json and the table above
python3 -I tools/quiz_grep_policynz.py 'regex' [--full]   # find matching policy.nz statements and their citations
python3 -I tools/quiz_minor_grep.py 'regex' [party ...]   # search archived party documents
python3 -I tools/quiz_fetch_text.py <url> [regex]         # fetch and cache a news page into raw/quiz/pages
python3 -I tools/quiz_wiki.py "<Wikipedia title>" [regex] # bill and vote records
```

To add or correct a position, edit `tools/quiz_data.py` and rebuild. The builder refuses any cell that has no evidence or no source, any `policy_id` that is unknown or belongs to a different party, and any party slug that is not in the list.
