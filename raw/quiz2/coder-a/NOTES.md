# Coder A notes — quiz2 party coding (round 1, 23 Oct 2026)

Output: `data/guide/quiz2-coder-a.json` (30 statements × 17 parties, 292 non-null cells).
Coded blind to Coder B. Scale and rules per `guide/quiz-research.md` §3.2 and §4.1–4.2.

## Method

1. Tier 1 first: grepped `parties/<party>/policies/policies.json` (1,435 policies) and
   `policies/documents/*.md` by statement theme (tax, debt, sanctions, FPA, sentencing, move-on,
   drugs, gender/RSE, speech, youth justice, Treaty/co-governance/wards/Tribunal/te reo/
   settlements, ETS/Paris/fast-track/mining, immigration/benefit stand-down/AUKUS,
   referendums/donations/rates cap). Small-party policy lists were read in full.
2. Tier 2 votes used: Treaty Principles Bill 2nd reading (10 Apr 2025, 112–11, ACT only in favour);
   Local Government (Māori Wards) Amendment Act (30 Jul 2024, 68–55); Fast-track Approvals Act
   (3rd reading 17 Dec 2024, party lines); Reinstating Three Strikes Act (13 Dec 2024, 68–43);
   Sentencing (Reform) Amendment Act (Mar 2025, all opposition parties against); Crown Minerals
   Amendment Act (31 Jul 2025); Fair Pay Agreements repeal (14 Dec 2023); Education and Training
   Amendment Bill (No 2) free-expression provisions (Nov 2025).
3. Tier 3 questionnaires: NZCTU 12-question scorecard (party answers read from the image alt text in
   `raw/quiz/pages/union_org_nz_...html`, which lists each party's Yes/No; the PDF text loses column
   order), Greenpeace 20-question methodology (verbatim party answers in
   `raw/quiz/greenpeace/methodology.txt`), Grey Power responses (used only for colour).
4. Tier 4/5 via WebSearch/WebFetch: 1News CGT reactions (28 Oct 2025), Luxon Paris bottom line
   (1 Sep 2026), Treaty clauses review (Spinoff/Te Ao News, Apr 2026), Labour on rates cap (RNZ via
   Scoop, 26 Aug 2026), move-on orders bill (ODT/1News 2026), Defence Capability Plan (Apr 2025),
   Seymour on privatisation (Jan 2025), English-first agencies (Nov 2023), Peters on AUKUS (2024).

Tier counts: T1 239, T2 9, T3 20, T4 18, T5 6. Confidence: high 150, medium 84, low 58.

## Coverage per party (non-null of 30)

National 30, Green 30, NZ First 28, ACT 27, Te Pāti Māori 27, Labour 26, Opportunity 25,
Alliance 25, Conservative 17, NZ Outdoors & Freedom 11, Te Tai Tokerau 11, NZ Loyal 10,
Animal Justice 9, Vision NZ 8, Women's Rights 5, Legalise Cannabis 2, Free Palestine 1.

Parties under the 15-position threshold (§4.1 rule 7): NZOFP, TTP, NZ Loyal, AJP, Vision, WRP,
ALCP, Free Palestine. For these, null is genuinely the state of the record; I did not stretch.

## Hard cases (flag for round 2)

- **T4 National = 0.** Voted against the Treaty Principles Bill (Apr 2025) but is legislating a
  Parliament-led rewrite of ~18 Treaty clauses to "take into account" and rejected the Tribunal's
  call to halt (Aug 2026). Coded as documented contradiction → argued neutral, low confidence.
  A +1 (low) reading is defensible.
- **T6 National = 0.** Wants to "progress" and finish remaining settlements; never says the process
  has gone far enough. Treated as addressed-but-no-side. Could equally be null.
- **T6 generally.** Only ACT and NZ First address closure explicitly. For Greens/TPM/TOP/Alliance/TTP
  I coded negative from policies that extend or strengthen redress; Labour null (no 2026 statement found).
- **E4 (private v public).** National +1 rests on Luxon's "mature conversation"/asset-recycling line
  (2025–26, tier 4), not a 2026 policy document. ACT +2 rests on Seymour's Jan 2025 "government is
  hopeless at owning things" plus Landcorp sale advocacy; ACT's 2026 documents do not state a sales policy.
- **S2 Labour = 0.** Labour wants begging/rough sleeping removed from the Move-on Orders Bill but did
  not oppose move-on powers for disorderly behaviour; I could not confirm its first-reading vote.
- **S3 ACT = 0.** No party policy; Seymour personally voted yes in 2020 and said legalisation is "not a
  priority". Only pre-2023 material exists; used because nothing newer found (§4.1 rule 1 last sentence).
- **S3 National = −1 (low).** Only evidence is random drug testing of Jobseekers with sanctions
  (Oct 2026). Scope is narrow; reconciler may prefer null.
- **S3 Labour, NZ First = null.** No 2026 drug statements found in two searches each.
- **S4 ACT = null.** ACT has clear positions on speech but I found no 2026 ACT statement on gender/RSE
  in schools; the RSE guideline removal was a NZ First coalition demand executed by a National minister
  (coded National −1 tier 5, NZ First −2 tier 1 via the Definitions of Woman and Man Bill).
- **S5 Labour = null.** Hate-speech reform was shelved in Feb 2023; nothing since. Under-16 social
  media ban support is not a speech position.
- **V2 Labour = 0; National = −1.** Both price industry via the ETS and not farmers; Labour is
  non-committal on agriculture (Greenpeace), National explicitly rules it out. Reconciler may want
  these symmetric.
- **E7 NZ First = 0, E2 NZ First = 0.** NZ First proposes both tax cuts and very large spending/
  borrowing ($100bn Future Fund); no stated trade-off.
- **O3 NZ First = 0.** Peters' 2024 "independent foreign policy never meant non-aligned" + AUKUS Pillar 2
  exploration vs "sovereignty" rhetoric. No 2026 statement found.
- **O3 ACT = null, TOP = null.** No defence/alliance policy found for 2026.
- **D1 ACT = 0.** Campaigned for a binding Treaty Principles referendum (2023–24) but opposed Luxon's
  electoral-system referendum idea (Aug 2026) and asserts parliamentary supremacy.
- **D3 Labour = 0.** Supports rates cap "in principle" to select committee (Aug 2026) after Hipkins
  called caps counter-productive (Jul 2025); opposed Māori-ward override. Genuinely mixed.
- **D3 TPM = 0, NZ First = 0.** Both would both centrally mandate and locally devolve different things.
- **Inference cells (§4.1 rule 3, all confidence low):** NZ Loyal T1/T2/T3 ("scrap all race-based
  policies"), Conservative T3/T4 ("one law for all"; judiciary "usurp" elected mandate), NZOFP S2
  (Bill of Rights supreme), AJP T2/V3/V5, WRP V1, Vision V2, Alliance T3.
- **NZCTU for National/ACT** are the CTU's own fill-ins from voting record (parties declined); I used the
  underlying votes (FPA repeal) rather than the CTU grade, consistent with §4.1 rule 1(iii).
- **Greenpeace National/ACT scores** are likewise assessed, not answered; I cited the underlying
  votes/bills (Fast-track, Crown Minerals, Conservation Amendment Bill) where used.

## Sources that could not be reached

greens.org.nz, nzfirst.nz, maoriparty.org.nz, opportunity.org.nz and web.archive.org are blocked
(per AGENT_BRIEF); I relied on the archived verbatim copies under `parties/*/policies/documents/`
and the policy.nz-cited URLs in `policies.json`. Hansard vote tallies for the Social Security
Amendment Act 2025 and the Move-on Orders Bill first reading were not retrievable in this session;
affected cells are coded from party statements (tier 4) and marked low/medium.
