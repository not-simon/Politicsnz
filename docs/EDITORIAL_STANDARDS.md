# Editorial standards

Ballot Book NZ is a public voter guide. Its standard is simple: **true and factual, not biased.** This page is the public
commitment behind that: the rules every voter-facing summary is written to, how they were applied before publication, and how to
tell us when we get something wrong.

These rules apply to the plain-English layer a voter reads first: the party cards (`data/guide/parties.json` → `guide/parties.md`),
the issue explainers (`data/guide/issues.json` → `guide/issues.md`), the top of `REPORT.md` and `README.md`. The deeper layers
(party profiles, policy lists, full-text documents, people profiles, promise trackers) follow the same principles and carry their
own sources; gaps found there are listed for follow-up in [`REVIEW_LOG.md`](REVIEW_LOG.md).

## 1. Describe, don't judge

- We say what a party proposes, not whether it is a good idea or whether it would work.
- We avoid words that carry a verdict: *radical, sensible, extreme, slash, generous, tough/tougher, finally, so-called, crack down,
  clean up, giants, teeth, huge, massive, reckless, common-sense, real.* Where a verdict is someone else's, we quote them and name them.
- Headlines and taglines use the same register as the body text. A party's slogan is quoted as a slogan.
- Where a party uses a label that others dispute (for example "race-based", "mass immigration", "co-governance", "one law for all",
  "citizens first", "fair play in sports", "woke", "unborn child"), we put it in quotation marks and attribute it: *what it calls…*,
  *its phrase is…*. The guide does not adopt any side's label as its own description.

## 2. Equal treatment

- Every party card has the same fields, filled to a similar depth where sources allow: tagline, nutshell, five to seven headline
  policies with policy ids or document links, the party's own pitch ("they say"), attributed criticism ("critics say"), seats,
  polling, coalition stance, whether it has published costings, a track-record line, and sources.
- "They say" is always the party's own words, quoted and dated.
- "Critics say" is always attributed to a named person or organisation, with a date and a link. Criticism of a related body (a
  church, a founder, a predecessor party) is labelled as such, not presented as criticism of the party. Where we could find no
  named criticism in 2026 campaign coverage, the card says so in the same words for every party, with the date we searched.
- Headline policies are the party's own headline commitments, checked against its campaign launch, manifesto or policy index
  (`parties/<party>/policies/README.md`), not a selection chosen to flatter or caricature it.
- Left–right labels are the party's English Wikipedia infobox label, quoted as Wikipedia's, with the retrieval date. Where Wikipedia
  gives none we say so and quote how the article describes the party.
- Polling, seat and promise figures are computed by the same scripts, with the same rules, for every party.

## 3. Facts: sourced, dated, checked

- Every number, date and quotation links to a source a reader can open. Figures carry an "as of" date or the period they measure.
- Before publication every number and date in the party cards and issue key facts was checked against its cited source (fetched on
  23 October 2026). Anything that could not be supported was corrected, re-sourced or removed; the log records each case.
- Where sources conflict, the guide says so and gives both (for example, the cost of buying back BNZ: NZ First's own $7.5b against
  "other estimates" of up to $24b whose source the NZ Herald does not name).
- Where a party's own site could not be retrieved (some block automated access), the card says so and names the secondary source
  used (for example RNZ's quotation of the NZ Loyal website).
- Secondary summaries (Wikipedia, policy.nz) are used as finding aids and labelled as such; where they are the only source for a
  characterisation, the card says "Wikipedia describes…" rather than stating it as fact.

## 4. Contested topics

For Te Tiriti o Waitangi, immigration, welfare, crime, climate and sex/gender, each party's position is described in its own terms,
and no side's framing is used as the neutral description. The issue explainers set out the disagreement ("some parties want…; others
want…") before the positions, and the "why it matters" text uses measured facts (prison numbers, migration flows, emissions shares,
hardship rates) rather than characterisations.

## 5. Currency

- Every card and explainer carries an "as of" date. Coalition stances, polling and costings carry the date of the latest statement
  or poll used.
- Polling is a simple, unweighted average of all published polls with fieldwork ending in the 30 days to the "as of" date, recomputed
  by `tools/guide_enrich.py` from `data/polls-2026.json`. Small parties that pollsters do not report separately are shown as such.
- Significant campaign developments after the snapshot (candidate resignations, new fiscal plans, rule-outs) are added as dated notes
  rather than rewritten into the body, so a reader can see what changed and when.

## 6. Plain English

- Short sentences. One idea per sentence where possible.
- Jargon is defined the first time it appears in a card or explainer (for example: OBEGAL, PREFU, "bright-line" rule, Sainte-Laguë,
  "gentailer", confidence and supply).
- Numbers are rounded to what a reader needs, with the exact figure in the source.
- Māori terms used by parties (kai, mokopuna, whānau, mana whenua, tino rangatiratanga) are kept and glossed in brackets the first
  time they appear.

## 7. What the guide is not

- It is not a recommendation. No card, explainer or report section says who to vote for.
- It is not a prediction. Seat scenarios are arithmetic on poll averages and are labelled as illustrations.
- It is not complete. Policy counts reflect how parties publish, not how much they plan to do. Promise trackers cover high-profile,
  checkable promises, not every manifesto line.

## How to report an error

1. **Open an issue** on the repository using the **Correction** template (`.github/ISSUE_TEMPLATE/correction.yml`). Say which page or
   file, what is wrong, what is right, and link to a source: the party's own document, an official release, or a reputable news
   report.
2. **Or edit and open a pull request**: data lives in JSON under `data/` and in `parties/*/policies/policies.json`; the Markdown pages
   and the site are generated from it (`python3 tools/guide_render.py`, `python3 tools/report_stats.py --write`,
   `python3 tools/build_site.py`). One topic per pull request, with the source linked.
3. **What happens next.** Factual corrections are checked against the primary source and applied; the change is recorded in
   [`REVIEW_LOG.md`](REVIEW_LOG.md) with the before/after wording. A party's description of its own policy is corrected against the
   party's own published text. Disputes about framing are resolved by attributing the disputed wording to whoever uses it, not by
   choosing a side.
4. **Timing.** During the campaign, corrections to the voter-facing summaries take priority over all other work on the archive.

*Last reviewed: 23 October 2026.*

## Right of reply, corrections and items about people

- **Reply within five working days.** Anyone named on the site who believes an item is wrong or unfair can open an issue (or use any
  contact route on the site). We check the item against the published record, correct or remove it, and publish the person's reply
  alongside the item if they want one. The target is a response within five working days (Defamation Act 1992 s 25 timeframe) and
  an immediate fix for plain factual errors.
- **Inclusion rules for criticism and "controversies".** An item about a person or party appears only if (1) it is on the public
  record in at least two reputable sources or an official record, (2) it is relevant to fitness for public office or to the party's
  conduct in office, (3) the outcome is stated (resolved, withdrawn, ongoing, finding made), and (4) the subject's own response is
  included where one was given. Items that cannot meet all four are removed. Headings are descriptive ("Disputes and criticism").
- **Name suppression.** Before any court-related item is added, check for suppression orders; nothing subject to suppression is
  published, whatever its source.
- **Privacy.** Candidates' home suburbs are never published and personal webmail addresses are not shown; only party, parliamentary
  or campaign-domain contacts and public accounts the person listed themselves.
- **Takedowns.** Owners of third-party material (party texts, photos) can ask for removal, correction or different attribution; during
  the campaign requests are actioned within 24 hours.
