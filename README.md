# Ballot Book NZ — an independent guide to New Zealand politics, 2011–2026

A sourced, non-partisan research archive for voters in the **7 November 2026 general election**: every party, every 2026 policy (summary **and** full original text), every candidate and MP since 2011, how each party has kept its promises, and how Parliament has been made up at every election since 2011.

**Live site: https://not-simon.github.io/Politicsnz/**

It comes with an interactive, phone-friendly guide in [`site/`](site/) — find-your-match quiz, party pages, issue comparisons, your electorate's candidates, a tap-a-seat map of every Parliament, poll trends, a coalition builder and an MMP seat calculator.

> Not affiliated with any party. Every fact is meant to link to its source, and the same rules apply to every party ([editorial standards](docs/EDITORIAL_STANDARDS.md)). If you find an error, open a [Correction issue](https://github.com/not-simon/Politicsnz/issues/new/choose) or see [how to report an error](docs/EDITORIAL_STANDARDS.md#how-to-report-an-error). Party policy texts are reproduced as published, for reference. Enrol and find your voting place at **vote.nz**.

## Start here

| If you want… | Go to |
|---|---|
| The big picture: who's offering what, who keeps promises, trends | [`REPORT.md`](REPORT.md) |
| Plain-English party summaries | [`guide/parties.md`](guide/parties.md) |
| Where every party stands on the big issues | [`guide/issues.md`](guide/issues.md) |
| Your electorate and its candidates | [`electorates/`](electorates/README.md) |
| Every 2026 policy of one party, with full texts | `parties/<party>/policies/README.md` (e.g. [National](parties/national/policies/README.md), [Labour](parties/labour/policies/README.md), [Green](parties/green/policies/README.md), [ACT](parties/act/policies/README.md), [NZ First](parties/nz-first/policies/README.md), [Te Pāti Māori](parties/te-pati-maori/policies/README.md), [TOP](parties/opportunity/policies/README.md)) |
| Has a party kept its word? | `parties/<party>/track-record.md` and [`data/promises/`](data/promises/) |
| A politician's profile | `parties/<party>/people/<name>/README.md` (each has `photo.jpg` and `person.json`) |
| Each election 2011–2023 and what's ahead in 2026 | [`elections/`](elections/) and [`elections/trends.md`](elections/trends.md) |
| Minor parties, past and present | [`parties/MINOR_PARTIES.md`](parties/MINOR_PARTIES.md) |
| How the quiz works | [`guide/quiz-method.md`](guide/quiz-method.md) |

## What's in it

- **1,435 policies** from 20 parties and groups standing in 2026, backed by **993 full-text documents** (party web pages, policy PDFs, press releases) in `parties/<party>/policies/documents/`. Each policy has a summary (Why / How), its topic and links to the verbatim source.

  | Party | Policies | | Party | Policies |
  |---|---:|---|---|---:|
  | Green | 564 | | Animal Justice | 38 |
  | National | 159 | | Vision NZ | 35 |
  | Labour | 126 | | Alliance | 27 |
  | ACT | 110 | | Te Tai Tokerau Party | 22 |
  | Te Pāti Māori | 91 | | Conservative | 19 |
  | NZ First | 79 | | Outdoors & Freedom | 18 |
  | TOP (Opportunity) | 77 | | Women's Rights, Legalise Cannabis, NZ Loyal, Free Palestine + electorate-only groups | 70 |

  The Greens' count is high because their whole manifesto and 40 standing policy papers are itemised.
- **People:** profile folders for MPs who served 2011–2026 and every 2026 candidate (≈550 people, most with photos), with current status (MP, retiring, candidate, former MP and what they do now).
- **Track records:** promise-by-promise checks for National, Labour, Green, ACT, NZ First and Te Pāti Māori (plus United Future and Mana), with verdicts *kept / partly kept / broken / abandoned / in progress* and sources.
- **Elections:** full results 2008–2023 (every party, every electorate, official counts), membership of the 50th–54th Parliaments including every mid-term change, and 129 opinion polls since 2023.
- **2026 guide layer:** plain-English cards for all 17 registered parties, 17 issue explainers with key facts, a 45-question match quiz with sourced party positions, and guides to all 71 electorates.

## Folder layout

```
REPORT.md                 the comprehensive report
guide/                    plain-English party cards, issues, quiz method
elections/                one story per election + trends
electorates/              one page per 2026 electorate
parties/<party>/
  README.md               profile: history, leaders, results, 2026 pitch, coalition stance
  track-record.md         promises vs delivery
  policies/               README (every policy) · policies.json · documents/ (full texts)
  people/<person>/        README.md · person.json · photo.jpg
data/                     machine-readable JSON (elections, parliaments, polls, promises, guide, electorates)
raw/                      source downloads (policy.nz data, policy PDFs)
site/                     the interactive guide (open site/index.html via any static web server)
tools/                    the scripts that fetched and built everything
docs/SCHEMA.md            data formats
```

## Viewing the interactive guide

- **Locally:** `cd site && python3 -m http.server` then open http://localhost:8000.
- **GitHub Pages:** the workflow in `.github/workflows/pages.yml` publishes `site/` automatically. Turn it on under *Settings → Pages → Source: GitHub Actions*. (Pages on a private repository needs a paid GitHub plan; on a public repository it's free.)
- **Rebuild after editing data:** `python3 tools/build_site.py`.

## Editorial standards and corrections

- The rules the guide is written to (neutral wording, equal treatment of every party, sourced and dated facts, attributed
  criticism, plain English) are in [`docs/EDITORIAL_STANDARDS.md`](docs/EDITORIAL_STANDARDS.md).
- Every change made in the pre-publication fact-check and neutrality review, with before/after wording and the reason, is in
  [`docs/REVIEW_LOG.md`](docs/REVIEW_LOG.md). It also lists issues found outside the reviewed files that still need follow-up.
- To report an error: open an issue with the **Correction** template (say which page, what is wrong, what is right, and link a
  source), or email the maintainer. Corrections are checked against the party's own published text or the official source.

## Sources and method

Sources include party websites and policy documents, policy.nz (structured 2026 policy and candidate data), the Electoral Commission, Parliament, the Beehive, Wikipedia (for election tables and biographies, with the primary sources it cites), and news media (RNZ, Stuff, NZ Herald, The Spinoff, interest.co.nz, 1News). Some party sites (Green, NZ First, Te Pāti Māori, TOP, NZ Loyal) block automated access; their texts came from Common Crawl archive captures, the parties' own releases on Scoop, and party PDFs — each document records how and when it was captured. Gaps and source disagreements are listed in each README rather than papered over. Retrieved 23 October 2026; policies may change before election day.
