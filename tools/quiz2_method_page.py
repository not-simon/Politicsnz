#!/usr/bin/env python3
"""Write guide/quiz-method.md (v2) and raw/quiz2/RECONCILIATION.md from data/guide/quiz2.json."""
import json, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
Q = json.load(open(ROOT / "data/guide/quiz2.json"))
S = Q["statements"]
P = Q["parties"]
AG = Q["agreement"]
LOG = Q["reconciliation_log"]
PARL = ["national", "labour", "green", "act", "nz-first", "te-pati-maori"]
ORDER = list(P)

def fmt(v):
    return "—" if v is None else f"{v:+d}" if v else "0"

def esc(t):
    return t.replace("|", "\\|").replace("\n", " ")

# ------------------------------------------------------------------ worked example
def match(user, weights, party_pos, k=4):
    num = den = 0.0
    n = 0
    for sid, u in user.items():
        p = party_pos.get(sid)
        if u is None or p is None:
            continue
        w = weights.get(sid, 1.0)
        a = 1 - abs(u - p) / 4
        num += w * a; den += w; n += 1
    raw = num / den if den else None
    shrunk = (num + k * 0.5) / (den + k)
    return n, raw, shrunk, num, den

USER = {"E1": 2, "E2": -1, "E3": 1, "S1": -1, "S2": -2, "T1": 2, "T3": 1, "V1": 2, "V2": 1, "O1": -1, "D1": 0, "D3": 1}
WEIGHTS = {"E1": 2.0, "T1": 2.0, "S1": 0.5}
def party_positions(slug):
    return {s["id"]: (s["positions"][slug]["position"] if s["positions"][slug] else None) for s in S}

ex_rows = []
for slug in ["green", "labour", "national", "animal-justice"]:
    pp = party_positions(slug)
    n, raw, shrunk, num, den = match(USER, WEIGHTS, pp)
    ex_rows.append((slug, n, raw, shrunk, num, den))

ex_detail = []
pp = party_positions("labour")
for sid, u in USER.items():
    p = pp[sid]
    w = WEIGHTS.get(sid, 1.0)
    if p is None:
        ex_detail.append(f"| {sid} | {fmt(u)} | — | {w:g} | excluded (no position) |")
    else:
        a = 1 - abs(u - p) / 4
        ex_detail.append(f"| {sid} | {fmt(u)} | {fmt(p)} | {w:g} | 1 − {abs(u-p)}/4 = {a:.2f} → {w*a:.2f} |")

# ------------------------------------------------------------------ discrimination table
disc_rows = []
flagged = []
for s in S:
    vals = [s["positions"][p]["position"] if s["positions"][p] else None for p in PARL]
    pos = sum(1 for v in vals if v is not None and v > 0)
    neg = sum(1 for v in vals if v is not None and v < 0)
    counted = collections.Counter(v for v in vals if v is not None)
    mx = counted.most_common(1)[0][1] if counted else 0
    ok = "yes" if pos and neg else "**no**"
    if not (pos and neg): flagged.append(s["id"])
    if mx >= 5: flagged.append(s["id"] + " (≥5 identical)")
    disc_rows.append(f"| {s['id']} | {s['polarity']} | " + " | ".join(fmt(v) for v in vals) + f" | {ok} | {mx} |")

# ------------------------------------------------------------------ coverage table
cov_rows = []
for slug in ORDER:
    v = P[slug]
    tiers = v["tier_counts"]
    tier_s = ", ".join(f"T{k}: {n}" for k, n in tiers.items())
    badge = "default ranking" if v["in_default_ranking"] else "**limited information**"
    cov_rows.append(f"| {v['name']} | {v['positions_recorded']} | {v['low_confidence_cells']} | {v['argued_neutral_cells']} | {tier_s} | {badge} |")

# ------------------------------------------------------------------ polarity table
pol_rows = []
for s in S:
    pol_rows.append(f"| {s['id']} | {esc(s['text'])} | {s['polarity']} | {s['dimension_label']} |")

# ------------------------------------------------------------------ audit table
audit = []
for s in S:
    audit.append(f"\n#### {s['id']} — {esc(s['text'])}\n")
    audit.append("| Party | Pos. | Tier | Conf. | Coders | Evidence | Source |")
    audit.append("|---|---:|---:|---|---|---|---|")
    for slug in ORDER:
        c = s["positions"][slug]
        if c is None:
            continue
        ev = c["evidence"]
        rec = ""
        if " Reconciler: " in ev:
            ev, rec = ev.split(" Reconciler: ", 1)
            rec = f" **Reconciler:** {rec}"
        coders = "A = B" if c["coders_agreed"] else f"A {fmt(c['reconciled_from']['A'])} / B {fmt(c['reconciled_from']['B'])}"
        src = f"[link]({c['source_url']})"
        if c.get("source_url_2"):
            src += f" · [2]({c['source_url_2']})"
        audit.append(f"| {P[slug]['name']} | {fmt(c['position'])} | {c['tier']} | {c['confidence']} | {coders} | {esc(ev)}{esc(rec)} | {src} |")
    nulls = [P[slug]["name"] for slug in ORDER if s["positions"][slug] is None]
    audit.append(f"\nNo position found (excluded from the match): {', '.join(nulls) if nulls else 'none'}.")

# ------------------------------------------------------------------ decision log tables
def log_table(rows):
    out = ["| Statement | Party | A | B | Adopted | Reason |", "|---|---|---:|---:|---:|---|"]
    for r in rows:
        out.append(f"| {r['statement']} | {P[r['party']]['name']} | {fmt(r['A'])} | {fmt(r['B'])} | {fmt(r['adopted'])} | {esc(r['reason'])} |")
    return "\n".join(out)

both = [r for r in LOG if r["A"] is not None and r["B"] is not None and r["A"] != r["B"]]
single = [r for r in LOG if (r["A"] is None) != (r["B"] is None)]
same = [r for r in LOG if r["A"] is not None and r["A"] == r["B"]]

n_total = sum(v["positions_recorded"] for v in P.values())
n_low = sum(v["low_confidence_cells"] for v in P.values())
n_zero = sum(v["argued_neutral_cells"] for v in P.values())
tier_tot = collections.Counter()
for v in P.values():
    for k, n in v["tier_counts"].items(): tier_tot[k] += n
coders_agree_cells = sum(1 for s in S for p in ORDER if s["positions"][p] and s["positions"][p]["coders_agreed"])

# ================================================================== METHOD PAGE
ex_lines = []
for slug, n, raw, shrunk, num, den in ex_rows:
    cov = "in default ranking" if n >= max(10, 0.5 * len(USER)) else f"badge: based on only {n} of your {len(USER)} answers"
    ex_lines.append(f"| {P[slug]['name']} | {n} of {len(USER)} | {num:.2f} / {den:g} = {raw:.3f} → {round(raw*100)}% | ({num:.2f} + 2) / ({den:g} + 4) = {shrunk:.3f} → {round(shrunk*100)}% | {cov} |")

method = f"""# "Find your match" quiz (v2): what it measures and how

Data: [`data/guide/quiz2.json`](../data/guide/quiz2.json) (version `{Q['version']}`, positions frozen {Q['freeze_date']}). Built by `tools/quiz2_reconcile.py` from two independent codings, [`quiz2-coder-a.json`](../data/guide/quiz2-coder-a.json) and [`quiz2-coder-b.json`](../data/guide/quiz2-coder-b.json); the reconciliation log is [`raw/quiz2/RECONCILIATION.md`](../raw/quiz2/RECONCILIATION.md). The design rationale and literature review are in [`quiz-research.md`](quiz-research.md). This page replaces the v1 method page (45 concrete-instrument statements, single coder); v1 data remains in `data/guide/quiz.json` for comparison.

The quiz shows how close each party's **public record** is to your answers on 30 statements. It is a conversation starter, not voting advice: it ignores competence, trust, leadership, coalition arithmetic and how much weight parties themselves put on each issue.

## 1. What the quiz measures

Six dimensions, chosen from the Chapel Hill Expert Survey structure and New Zealand Election Study findings (research §2). Statement counts deliberately over-weight the economy (the most salient issue block in 2026 polling) and under-weight openness and democracy, where there are fewer live partisan divisions.

| Code | Dimension | Pole A | Pole B | Statements |
|---|---|---|---|---:|
""" + "\n".join(f"| {k} | {v['label']} | {v['pole_a']} | {v['pole_b']} | {sum(1 for s in S if s['dimension']==k)} |" for k, v in Q["dimensions"].items()) + f"""

## 2. Statement design and sources

Every statement follows ten rules (research §3.1): one principle and, where a widely acknowledged cost exists, one "even if" cost; no numbers, dates, dollar figures, Act, programme, party or leader names; affirmative wording; balanced direction within each dimension; at least two parliamentary parties codeable at opposite signs; prospective; answerable without background knowledge; a five-point scale plus a separate "no opinion / skip"; an optional importance pass (×0.5 / ×1 / ×2); and, where a validated NZES or CHES item exists, adapted from it. A regex check at build time asserts that no statement text contains a party, leader, Act or scheme name; it passes for all 30.

Polarity records which pole agreement moves toward: `+A` means agreeing places you at pole A, `+B` at pole B. Sixteen items are worded toward A and fourteen toward B (E 3/4, S 3/3, T 3/3, V 3/2, O 1/2, D 3/0); the D block is skewed and is flagged for rewording in a future version.

| # | Statement | Polarity | Dimension |
|---|---|---|---|
""" + "\n".join(pol_rows) + f"""

**Discrimination check.** For each statement the six parliamentary parties' coded positions, whether at least two sit at opposite signs, and the largest number sharing one value (five or more triggers review).

| # | Pol. | National | Labour | Green | ACT | NZ First | Te Pāti Māori | Opposite signs? | Max identical |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
""" + "\n".join(disc_rows) + f"""

Flagged: {', '.join(flagged) if flagged else 'none'}. O2 (migrant benefit waits) and D2 (voter-only donations) have explicit positions on one side only among parliamentary parties; the other side is `null` (no position found), not disagreement. They still inform the match for the parties that have positions and are retained with this flag; the next revision should either find published counter-positions or replace them.

## 3. How party positions were coded

Each cell is `{{position, evidence, source_url, tier, confidence, coders_agreed, reconciled_from}}` or `null`.

| Value | Meaning | Rule (EUvox / Vote Compass definitions) |
|---:|---|---|
| +2 / −2 | Strongly agree / disagree | Clear, emphasised, unconditional position |
| +1 / −1 | Agree / disagree | Supports the direction with qualifications, a weaker version, or only part of the proposal; **or** the one permitted inference: an explicit general principle whose scope plainly covers the statement (always confidence `low`, inference stated in the evidence) |
| 0 | Argued neutral | Only three cases: the issue is addressed but only vaguely; both sides are emphasised and a side is deliberately not taken; the party is visibly split. Also a documented contradiction between a vote and a later statement. A 0 counts as a position in the match. |
| `null` | No position found | No document, vote, questionnaire answer or dated statement on the proposal or its opposite; a "no change / no policy" answer; or evidence that is only an inference from general ideology. **Excluded from the match and never displayed as neutral.** |

**Evidence hierarchy** (tier recorded on every cell): (1) the party's 2026 manifesto, policy document or policy page, archived verbatim under `parties/*/policies/documents/`; (2) recorded party votes in the 54th Parliament on legislation that directly enacts or repeals the proposal; (3) the party's own written answers to third-party questionnaires (Greenpeace, NZCTU, Grey Power, KPMG tracker), never the organisation's grade; (4) dated statements by the leader or portfolio spokesperson; (5) coalition-agreement commitments and government actions attributable to the party, flagged as such. Statements older than 2023 count only when nothing newer exists, with the date recorded. Policy.nz summaries were used only to locate originals.

Tier use in the final matrix: {', '.join(f'tier {k}: {n}' for k, n in sorted(tier_tot.items()))} ({n_total} cells). Confidence: {n_low} cells are `low` (shown in the uncertainty band, §5.4); {n_zero} cells are argued neutrals.

### 3.1 Two blind coders, then reconciliation

Two coders (automated research assistants working from the same archive and protocol, blind to each other) each coded all 30 × 17 = 510 cells with a written justification, URL, tier and confidence. Their notes are in `raw/quiz2/coder-a/NOTES.md` and `raw/quiz2/coder-b/NOTES.md`. A third reviewer then reconciled every cell under fixed rules:

- both coded identically → adopted; evidence merged, lower tier kept, confidence = higher of the two when the sources differ (independent corroboration), otherwise the lower;
- both coded, one point apart → both evidence texts and sources examined (sources re-fetched where the decision turned on them); the better-evidenced value adopted; if equally evidenced, the lower tier; if still tied, the value nearer 0;
- one `null`, one coded → the coded cell's evidence verified against the source and adopted only if it meets the §3 rules; otherwise `null`;
- any cell resting on inference from general ideology → `null`; inference from an explicit principle → capped at ±1 `low`;
- every argued 0 checked against the three cases.

**Agreement statistics.** Of {AG['cells_both_coded']} cells both coders assigned a value: **{AG['exact_pct']}% identical, {AG['within1_pct']}% within one point, {AG['opposite_sign']} opposite in sign** (differences: {AG['difference_distribution']['0']} × 0, {AG['difference_distribution']['1']} × 1, {AG['difference_distribution']['2']} × 2). The one two-point gap was ACT on D3 (council autonomy). {AG['single_coder_cells']} cells were coded by one coder only; {AG['adopted_from_single_coder']} were verified and adopted, {AG['single_coder_downgraded_to_null']} were set to `null`. Of the {AG['disagreements_resolved']} disagreements, {AG['both_coded_downgraded_to_null']} ended as `null` (ACT on S3), {AG['inference_cells_reduced_to_pm1']} were ±2 inferences capped at ±1, and the rest were resolved to one coder's value or to an argued neutral. Final matrix: {n_total} positions, of which {coders_agree_cells} were coded identically by both coders. The full cell-by-cell log is in §9 and in `RECONCILIATION.md`.

For comparison, EUvox reported Van der Eijk agreement coefficients and re-coded cells below 0.7; with two coders we report the simpler exact and within-one percentages, which are the statistics Vote Compass publishes for its inter-coder check.

### 3.2 The hardest calls

- **National, T2 (no seats, wards or services set aside for Māori).** A +1, B 0. National legislated binding polls on Māori wards (a recorded vote), disestablished the Māori Health Authority and issued the "need not race" circular, but has no policy to abolish the Māori seats. Adopted **+1**: the actions are concrete and in one direction; not proposing to abolish the seats is a restriction on the position, not an opposing emphasis, and the claim that Luxon formally ruled out NZ First's seats referendum could not be verified and is not relied on.
- **National, T4 (Parliament rather than the courts or Tribunal should decide what the Treaty means).** Both coders 0. National voted the Treaty Principles Bill down (112–11) yet is legislating a Parliament-led rewrite of Treaty clauses in about eighteen statutes and rejected the Tribunal's call to halt. A documented contradiction between the vote and current action: **0**, with the contradiction stated in the cell.
- **ACT, D3 (councils free to decide, rather than central override).** A −2, B 0: the only two-point gap. ACT's programme constrains councils at every turn (rates cap, binding ward polls, removing votes from unelected appointees by statute, mandated compensation rules, opposition to councils' bed tax); B's devolving item, a tourism dividend, is a funding transfer, not autonomy. Adopted **−2**.
- **Labour, O2 (migrants should wait several years for benefits).** A null, B 0. Labour's immigration page (fetched) says nothing about benefit access; its two-to-four-year change concerns permanent residence, and the claimed opposition to a five-year benefit wait could not be sourced. **Null.** The same standard removed Green O2 (an inference from "remove barriers for migrants").
- **ACT, S4 (schools and public institutions should reflect changing attitudes on gender, sexuality and family).** A null, B −2. Verified: ACT's children's spokesperson welcomed the suspension of puberty-blocker prescriptions as putting "child safety" first (20 Nov 2025). That is an explicit position on a public institution and gender, but it is a health decision, not schools, and the removal of the sexuality-education guidelines was a NZ First coalition demand. Adopted **−1**, tier 4, medium.

Also notable: ACT on S3 (drug freedom) went from 0 / −1 to `null` because neither a 2020 personal referendum vote nor support for beneficiary drug-testing meets the rule; NZ First on E1, E2 and E7 is 0 three times because it proposes both tax cuts and very large spending without stating a trade-off; Te Pāti Māori E3 is +1 rather than +2 because its Kiwi Tax Plan taxes asset holdings and contains no capital gains tax; the Green T6 is −2 because the manifesto proposes removing "full and final" clauses, the direct opposite of closure; NZ Loyal's nine positions rest on a ten-point list quoted by RNZ (12 Oct 2026; the party's site was unreachable), re-fetched and confirmed verbatim, with every inference from "scrap all race-based policies" capped at ±1 low.

**Party self-placement.** Parties were not invited to self-place for this version (research §4.1 rule 5); none has been. The cells are therefore coding-only. This is stated in the data file and should be remedied before any further release.

## 4. Coverage

Parties with fewer than 15 of 30 positions carry a "limited information" badge and are excluded from the default ranking (they are still shown, with their score, below it). `null` is genuinely the state of the public record for most small-party cells; coders were instructed not to stretch.

| Party | Positions (of 30) | Low-confidence | Argued neutral | Evidence tiers | Display |
|---|---:|---:|---:|---|---|
""" + "\n".join(cov_rows) + f"""

## 5. The matching algorithm

Notation: `u_i` your answer to statement *i* (−2…+2), `p_ij` party *j*'s position, `w_i` your importance weight (0.5, 1 or 2; default 1). `S_j` is the set of statements you answered (not skipped, not "no opinion") for which `p_ij` is not `null`. `M` is the number of statements you answered.

### 5.1 Core match (weighted city-block)

```
a_ij  = 1 − |u_i − p_ij| / 4                        per-statement agreement, 0…1
raw_j = Σ_{{i∈S_j}} w_i · a_ij  /  Σ_{{i∈S_j}} w_i          weighted mean agreement
```

City-block (Manhattan) proximity is what Vote Compass, euandi and Louwerse & Rosema's "city block" variant use. It is explainable ("you were two steps apart on this statement") and, unlike Euclidean distance, does not square large disagreements, which would reward parties that take moderate positions on everything.

### 5.2 Shrinkage and coverage

A party with positions on a handful of statements can score 100% by luck. Each match is shrunk toward the uninformative value 0.5 by `k = 4` phantom neutral statements:

```
match_j = ( Σ_{{i∈S_j}} w_i · a_ij  +  k · 0.5 )  /  ( Σ_{{i∈S_j}} w_i  +  k )
```

A party enters the default ranking only if `|S_j| ≥ max(10, 0.5 · M)`. Below that it is listed separately with the badge "based on only N of your M answers" and its shrunk score. For a party with 30 positions and raw 0.70, shrinkage gives 0.676; for a party with 3 positions and raw 1.00 it gives 0.714.

### 5.3 Per-dimension agreement and the map

For each dimension *d*: `A_jd = Σ_{{i∈d∩S_j}} w_i a_ij / Σ_{{i∈d∩S_j}} w_i`, shown as "you and Party X agree on 4 of 6 Te Tiriti statements; the two you differ on are …", with the evidence for each.

The two-axis map plots `x_d = mean_i(s_i · v_i) / 2 ∈ [−1, +1]` for you and each party, where `s_i` is the polarity sign (+1 for `+A` items, −1 for `+B` items; stored as `polarity_sign`) and `v_i` the answer or position, so that agreeing with a `+B` statement moves toward pole B. The signed mean also neutralises acquiescence: someone who agrees with everything lands near the centre. The map is labelled "a simplified summary; the ranking above uses all 30 statements, not this map", and no ranking is derived from it.

### 5.4 Uncertainty band

Each party's match is recomputed (a) with every `low`-confidence cell set to `null` and (b) with every ±1 cell moved one step toward and away from your answer; the min–max is drawn as a thin band and the number of low-confidence cells is shown. Ties within two percentage points are displayed as ties.

### 5.5 Worked example

A respondent answers {len(USER)} statements (`{', '.join(f"{k} {fmt(v)}" for k, v in USER.items())}`), marks E1 and T1 "very important" (×2) and S1 "less important" (×0.5), and skips the other 18. For Labour:

| Statement | You | Labour | w | a = 1 − \\|u − p\\|/4 → w·a |
|---|---:|---:|---:|---|
""" + "\n".join(ex_detail) + f"""

Summing the included rows and applying shrinkage:

| Party | Statements used | raw_j | match_j (k = 4) | Coverage rule (threshold max(10, 6) = 10) |
|---|---|---|---|---|
""" + "\n".join(ex_lines) + f"""

Scores are rounded to whole percentages for display. Animal Justice's score is shown below the default ranking with its badge because fewer than 10 of the answered statements have a coded position.

## 6. Display rules

- A ranked list with the gaps between parties visible; no single "your party is X" headline.
- Whole percentages only; ties within two points shown as ties; the uncertainty band on every bar.
- "Based on N of your M answers" on every party; parties under the coverage threshold listed separately with the badge; parties with fewer than 15 coded positions badged "limited information".
- Per-dimension agreement for every party, with the party's own words and source URL for every statement (the "You vs Party" view).
- The unweighted result beside the weighted one.
- The freeze date ({Q['freeze_date']}) and a link to this page.
- Statements in randomised order, block-randomised so consecutive items come from different dimensions; no topic headers while answering; party positions revealed only after all answers are in; the optional one-line explainer never mentions parties.
- No "advice" or "recommendation" wording; `null` is never shown as neutral or as 0.

## 7. Limitations

- **No representative pilot.** The statements have not been tested on a sample of New Zealanders; NZES item wording and Vote Compass 2026 aggregates were used as partial checks only.
- **Coders are not a panel of independent country experts.** Positions were coded from documents by the project's researchers and automated assistants under the protocol above; every cell carries its evidence, tier and confidence so readers can check it, and the agreement statistics are published.
- **No party self-placement yet.** Parties have not been invited to check their cells.
- **Coverage is uneven.** Nine of seventeen parties have fewer than 15 positions; shrinkage and badges mitigate but do not remove this. Even among parliamentary parties, O2 and D2 have positions on one side only.
- **Snapshot.** Positions are frozen at {Q['freeze_date']}; parties release and change policy during the campaign. Later changes should be logged with date and reason.
- **Coalition actions.** {tier_tot.get('5', 0)} cells rest on government actions attributable to a coalition party (tier 5), flagged in the evidence; a government action is not automatically every partner's preference.
- **Older evidence.** A few cells (e.g. National S3, Te Pāti Māori S5, Legalise Cannabis T1) rest on pre-2023 statements because nothing newer exists; the date is recorded in the cell.
- **The proximity model ignores** competence, trust, leadership, record in government, coalition likelihood and the salience parties attach to issues.
- **Any statement set favours some parties.** The Walgrave-style simulation in the research checklist (§7.2) has not yet been run on this matrix; until it is, the structural bias of the set is unknown.
- **Dimensions are imposed a priori** and have not been validated on user data.
- **Effects of such tools are real but small** and concentrated among undecided voters; this is a conversation starter.

## 8. Validation checklist status

| Check | Status |
|---|---|
| Rules 1–8 for every item, reviewed by someone who did not draft it | Reviewed by the reconciler against §3.1; E5 and T5 contain "not" inside a subordinate clause, not as a negated proposal |
| No numbers, dates, Act, programme, party or leader names | Passes (regex assertion at build) |
| Direction balance | 16/14 overall; D block 3/0 flagged for rewording |
| Discrimination (two parliamentary parties at opposite signs) | 28 of 30 pass; O2 and D2 flagged (§2) |
| Every non-null cell has evidence, URL, tier, confidence | Passes ({n_total} cells) |
| ≥2 independent coders, reconciliation complete, agreement published | Done (§3.1) |
| No inference beyond the single permitted ±1 low rule | Enforced in reconciliation; {AG['inference_cells_reduced_to_pm1']} cells capped, {AG['downgraded_to_null']} nulled |
| Parties invited to self-place | Not done |
| Freeze date and changelog | Frozen {Q['freeze_date']}; changelog to start on first change |
| Algorithm unit tests, Walgrave simulation, metric-robustness and map checks | Specified in `scoring`; not yet run |

## 9. Full audit table: every party × statement × source

Positions in the party's own words (close paraphrase or quotation), with tier, confidence, whether the two coders agreed (and their values where they did not), the reconciler's reason where one was needed, and the source. Parties with no position found are listed under each statement.
""" + "\n".join(audit) + """

## 10. Reproduce or extend

`python3 -I tools/quiz2_reconcile.py` rebuilds `data/guide/quiz2.json` from the two coder files and the decision table in the script; `python3 -I tools/quiz2_method_page.py` regenerates this page and `raw/quiz2/RECONCILIATION.md`. To change a cell, add or edit its decision in `quiz2_reconcile.py` with a written reason; do not edit the coder files, which are the record of round one.
"""

(ROOT / "guide/quiz-method.md").write_text(method)

# ================================================================== RECONCILIATION.md
recon = f"""# quiz2 reconciliation report (round two, third reviewer)

Date: {Q['generated']}. Inputs: `data/guide/quiz2-coder-a.json`, `data/guide/quiz2-coder-b.json`, `raw/quiz2/coder-a/NOTES.md`, `raw/quiz2/coder-b/NOTES.md`. Output: `data/guide/quiz2.json` (version `{Q['version']}`), `guide/quiz-method.md`. Script: `tools/quiz2_reconcile.py` (the decision table in the script is the authoritative record; this file is generated from its output by `tools/quiz2_method_page.py`).

## 1. Agreement

| Statistic | Value |
|---|---:|
| Cells both coders assigned a value | {AG['cells_both_coded']} |
| Identical | {AG['difference_distribution']['0']} ({AG['exact_pct']}%) |
| Within one point | {AG['within1_pct']}% |
| Two points apart | {AG['difference_distribution']['2']} (ACT D3) |
| Opposite sign | {AG['opposite_sign']} |
| Cells coded by one coder only | {AG['single_coder_cells']} |
| … adopted after verification | {AG['adopted_from_single_coder']} |
| … set to null | {AG['single_coder_downgraded_to_null']} |
| Disagreements resolved | {AG['disagreements_resolved']} (of which {AG['both_coded_downgraded_to_null']} to null) |
| ±2 inferences capped at ±1 low | {AG['inference_cells_reduced_to_pm1']} |
| Final non-null cells | {n_total} ({coders_agree_cells} coded identically by both) |

Per-party coverage after reconciliation (coder A's and B's round-one counts are in their NOTES.md files): """ + "; ".join(f"{P[s]['name']} {P[s]['positions_recorded']}" for s in ORDER) + f""".

## 2. Rules applied

1. Identical codings adopted; evidence merged; tier = lower; confidence = higher of the two where the sources differ, else the lower.
2. One-point disagreements: both evidence texts and sources examined; the better-evidenced value adopted; if equal, the lower tier; if still equal, the value nearer 0.
3. Single-coder cells: evidence verified against the source (local verbatim archive or re-fetch) and adopted only if it meets research §4 (explicit position, or an explicit general principle plainly covering the statement → ±1 low); otherwise null.
4. Inference from general ideology → null. Inference from an explicit principle → capped at ±1 low.
5. Argued 0 must fit one of the three EUvox cases or a documented vote/statement contradiction; "no policy" and adjacent-topic material are null, not 0.

Sources re-checked for this round: the RNZ small-parties explainer (NZ Loyal list, verbatim); Animal Justice people and environment policies (donations, fossil-fuel exploration); Conservative principles, policy index and bureaucracy pages; Alliance "What we stand for"; Outdoors & Freedom agriculture policy; Vision NZ policies; Te Pāti Māori Kiwi Tax Plan (no capital gains tax); labour.org.nz/immigration (no benefit stand-down content); Peters' State of the Nation 2026 (no drug content); Reuters 5–6 Aug 2026 on Luxon's electoral-system referendum and the Labour/ACT responses; Te Ao News 12 Feb 2026 on the Māori-seats referendum; ACT's puberty-blocker release (20 Nov 2025), minerals policy and "God defend New Zealand" defence article. Unreachable: greens.org.nz, nzfirst.nz, maoriparty.org.nz, opportunity.org.nz (Cloudflare), web.archive.org; the verbatim archive under `parties/*/policies/documents/` was used instead.

## 3. Disagreements between the coders ({len(both)})

""" + log_table(both) + f"""

## 4. Cells coded by one coder only ({len(single)})

""" + log_table(single) + f"""

## 5. Identical codings adjusted ({len(same)})

""" + log_table(same) + """

## 6. Observations for round three / the next freeze

- O2 and D2 have positions on one side only among parliamentary parties (the others are null). Find published counter-positions or replace the items.
- Parties have not been invited to self-place. Do this before the next release and log responses.
- The D block is 3/0 toward pole A; reword D1 or D3 so that "agree" lands at pole B.
- Hansard division lists were not retrievable for the Social Security Amendment Act 2025 and the Move-on Orders Bill; the affected cells cite party statements (tier 4) and should be upgraded to tier 2 when the record is obtained.
- Several cells rest on pre-2023 statements with the date recorded (National S3, Te Pāti Māori S5, Legalise Cannabis T1); replace when newer material appears.
"""
(ROOT / "raw/quiz2/RECONCILIATION.md").write_text(recon)
print("method page", len(method), "bytes; reconciliation", len(recon), "bytes")
print("flagged:", flagged)
for r in ex_rows: print(r)
