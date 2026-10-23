# Coder B — round-one notes (quiz2, 30 statements × 17 parties)

Date: 2026-10-23. Output: `data/guide/quiz2-coder-b.json`. Coded blind to coder A.

## Method actually followed

1. Read every `parties/<party>/policies/policies.json` statement (1,435 entries) and grep-searched
   `documents/*.md` per statement with keyword sets (scripts in this folder: `ps.py`, `dg.py`, `kw.txt`).
2. Used the questionnaire material already in `raw/quiz/`: Greenpeace 2026 scorecard methodology
   (party answers quoted verbatim), NZCTU scorecards (party answers; National/ACT were filled by NZCTU
   from public record, so for them I cited votes/policy instead), Grey Power responses, KPMG tax tracker.
3. Votes: Treaty Principles Bill 2nd reading (10 Apr 2025, 112–11, ACT only in favour), Māori wards
   referendum law (30 Jul 2024), Fast-track Approvals Act (17 Dec 2024), Gangs Act (19 Sep 2024, 68–55),
   Three Strikes (13 Dec 2024, 68–43), Crown Minerals Amendment Act 2025, Social Security Amendment Act
   2025, military-style academies bill (passed under urgency 2026), move-on orders bill (18 Sep 2026),
   English Language Bill (3rd reading Jul 2026). Wikipedia/1News/ODT used as the citable record where
   Hansard division lists were not retrieved — reconciler may want to swap in parliament.nz URLs.
4. `null` wherever no document, vote, questionnaire answer or dated statement was found. Inference from an
   explicit general principle → ±1 with confidence `low` and the inference stated in the evidence text.

Coverage (non-null cells of 30): National 27, Labour 27, Green 29, ACT 29, NZ First 28, Te Pāti Māori 28,
Opportunity 27, Alliance 26, Conservative 22, Te Tai Tokerau 12, Animal Justice 10, Outdoors & Freedom 9,
Vision NZ 9, NZ Loyal 7, Women's Rights 7, Legalise Cannabis 3, Free Palestine 1.
Scale use: +2 ×86, −2 ×81, +1 ×64, −1 ×49, 0 ×21, null ×209.

## Hard cases (flagged for round two)

- **National T2 (seats/wards/services) = 0.** National restored binding Māori-ward polls and ended the
  Māori Health Authority, but Luxon has repeatedly refused a referendum on the Māori seats. Coded argued
  neutral (both sides emphasised). A coder reading "services" as the operative clause would give +1.
- **National T4 = 0.** Voted the Treaty Principles Bill down, saying court/Tribunal-developed principles should
  stand, yet committed to a Parliament-led review of Treaty clauses. Treated as a documented contradiction.
- **National E1 = −1 low, S3 = −1 (2022 statement), S5 = +1 low (coalition acts).** All inference-heavy;
  National's 2026 material is silent on income inequality, drug law and speech. Older/coalition evidence used
  only because nothing newer exists.
- **National O1 = 0.** "Attracting the skills we need" is neither fewer nor more migrants.
- **Labour E5 = −1 low.** I could not retrieve the division record for the Social Security Amendment Act 2025;
  coded from Labour's public opposition to expanded sanctions. Verify.
- **Labour S2 = 0.** Voted against the Gangs Act but will not repeal the patch ban; sought amendments to
  (not rejection of) the move-on orders bill.
- **Labour O2 = 0.** Extends the residence wait to four years but opposes National's 5-year benefit wait and
  proposes no change to the 2-year stand-down.
- **Labour D3 = +1 low.** Only evidence is the vote against the Māori-wards override; no rates-cap statement found.
- **Labour V2 = 0, D2 = 0.** Greenpeace answers are evasive ("review the ETS", "transparent and fair rules").
- **Green E3 = +2.** Greens propose a wealth tax and capital-acquisitions tax rather than a CGT; standing policy
  explicitly lists capital gains taxes. Someone reading the statement as CGT-specific might give +1.
- **Green D1 = 0.** Citizens' assemblies and casino referendums at local level, but opposed Treaty/Māori-seat
  referendums. Could be argued null.
- **ACT S3 = −1 low, O3 = −1 low, D1 = +1 low, D3 = 0.** Thin 2026 material on drugs, alliances, referendums;
  local government policy both devolves (tourism dividend) and overrides (Māori-ward polls, compensation rules).
- **NZ First E1 = 0, E7 = 0, D3 = 0.** Peters simultaneously attacks wealth taxes and neoliberalism, debt and
  proposes a $100b fund; backs local fluoride referendums but central overrides of councils.
- **NZ First T4 = +1.** Voted against the TPB yet its programme (Treaty clauses review, replacing the
  Tribunal, stripping Treaty principles from environmental law) is Parliament-defined limits.
- **Te Pāti Māori V4 = +1 low, S5 = −1 low, D1 = −1 low, D3 = 0.** No explicit Paris/hate-speech/referendum text in
  2026 material; coded from adjacent explicit principles. TPM would require Māori wards in every council
  (central mandate) — hence D3 neutral.
- **Opportunity E4 = 0, D1 = 0, O1 = 0.** Deliberately mixed positions (competition + public stakes; citizens'
  assemblies not referendums; "stable" immigration).
- **Small parties.** NZ Loyal's site was unretrievable; everything rests on the ten-point list RNZ quoted
  (12 Oct 2026) — T2 +2 and S4 −2 are direct, T1/D3/E2 are low-confidence inferences. Vision NZ T3 −1 and
  Conservative T3/T5/E3 are inferences from "one law for all"/"race-based" principles. Women's Rights S1 +1
  (higher penalties only for violence against women) and S5 +1 (opposes new hate-crime laws) are partial fits.
  Alliance O2 −1 and T2 −1 are inferences from universal-entitlement and Tiriti-in-the-state principles.
  Free Palestine has exactly one codeable statement (O3). Legalise Cannabis three.
- **Statements hardest to code overall:** D1 (binding referendums — only NZ First and Outdoors & Freedom are
  explicit; most parties address referendums only in relation to Māori seats/Treaty), O2 (migrant benefit
  waits — explicit only for National, ACT, NZ First), S5 (speech — most parties speak about online harm or
  hate speech, not offensive speech in general), T6 (settlements "far enough" — parties say "complete" or
  "expand", rarely "close"), E7 (debt vs services — parties state fiscal rules and spending promises together).

## Sources not used / caveats

- policy.nz summaries were used only to locate original documents; evidence quotes come from party text.
- NZCTU's National/ACT entries are NZCTU's own assessments, not party answers — not cited as tier 3.
- Greenpeace scores for National/ACT are Greenpeace's; only quoted party answers were used as tier 3.
- Google Drive URLs for Te Pāti Māori manifesto PDFs are the party's own published links (via maoriparty.org.nz).
