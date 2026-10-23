# Rebuilding the "Find your match" quiz on the research: literature review and design framework

*Research note for the 2026 voter guide. Written 23 October 2026. Companion to [`quiz-method.md`](quiz-method.md) (which documents the current 45-statement quiz). Raw downloads and an index of every source are in [`raw/quiz-research/`](../raw/quiz-research/SOURCES.md).*

This note reviews the academic literature on Voting Advice Applications (VAAs) — tools like Vote Compass, Kieskompas, StemWijzer, smartvote, Wahl-O-Mat and euandi — and turns it into a concrete design for a rebuilt quiz: which dimensions to cover, how to write statements, how to place parties, how to compute and display a match, and how to check the result. Where the evidence is thin or contested we say so. Paywalled papers are cited from their abstracts or from open-access summaries; the status of each source is listed in `raw/quiz-research/SOURCES.md`.

**Headline design decisions**

1. **Thirty statements, six dimensions**, each statement a single principle with its cost stated ("X, even if Y"), no numbers, no party or programme names, direction balanced, 5-point agree scale plus "no opinion", optional importance weight.
2. **Dimensions for NZ 2026:** state vs market (economic left–right), social order vs personal freedom (GAL–TAN), Te Tiriti and biculturalism (a distinct NZ axis), environment vs development, openness (immigration and foreign ties), and democracy/power (people vs representatives, money in politics, local autonomy).
3. **Party coding by iterative, evidence-first judgement:** manifesto/policy text first, then recorded votes, then formal questionnaire answers, then dated leader statements; at least two independent coders, anonymous first round, reconciliation of disagreements, a recorded confidence level and source for every cell; "no position" kept separate from "neutral"; no inference from general ideology.
4. **Matching by weighted city-block proximity in the full statement space**, with a coverage rule and shrinkage for parties with few recorded positions; results shown as a ranked list with "based on N of your M answers", per-dimension agreement, and a sensitivity range. A low-dimensional map is a secondary, clearly labelled view, never the ranking.
5. **Framed as information, not advice**, with every party position traceable to its source.

---

## 1. What the evidence says works (and doesn't)

### 1.1 Statement selection is the most consequential design choice

Walgrave, Nuytemans and Pepermans (2009) took the 50 statements drafted for the 2007 Belgian *Doe de Stemtest*, the answers of a random sample of 1,000 Belgians, and simulated 500,000 different 36-statement versions of the tool. The share of users "advised" to vote for a given party swung enormously between configurations: for example one party ranged from 5 per cent to 32 per cent of advice, another from 0.3 to 23 per cent, and the radical right from 4 to 26 per cent. Weighting statements by importance did not fix this; it widened the spread. Their conclusion is that any batch of statements has a built-in partisan tendency, and that this is true even when (as here) the statements were chosen by political scientists, balanced across issues, worded to avoid left or right bias and agreed by the parties. They also note that in the 2006 Dutch election the two leading tools, StemWijzer and Kieskompas, sent 13 vs 21 per cent of users to the CDA and 28 vs 12 per cent to the SP, using different statements and methods. ([PDF](https://medialibrary.uantwerpen.be/oldcontent/container2608/files/Walgrave%20et%20al%202009%20-%20voting%20aid%20applications.pdf))

Lefevere and Walgrave (2014) disaggregated the effect. Statement selection follows the logic of the proximity model: the more statements load on an underlying dimension (in Belgium especially the cultural left–right dimension), the more clearly voters with a position on that dimension are matched to parties with a similar position — but *parties with extreme positions on that dimension gain and centre parties lose*. Counter-intuitively, parties were *disadvantaged* when their own "owned" issues featured heavily, because statements are chosen to discriminate between parties, and discriminating statements on a niche party's core issue tend to capture its unpopular stance (their example: a CO2 tax statement and the Greens). Much of the between-selection variance remained unexplained and, in their view, essentially random. Their two practical recommendations: **pretest the statement set on a representative sample before launch so the builder at least knows which parties a given set favours**, and **include more statements rather than fewer** (more is "never a bad thing" for measurement; the constraint is user fatigue). Across 27 VAAs they found a range of 18 to 75 statements, with most using 30–40. ([PDF](https://pure.uva.nl/ws/files/2257058/149249_A_Perfect_Match_AcceptedVersion.pdf); [record](https://dare.uva.nl/id/c55af723-1679-47c7-8949-61e8828bf5b2))

Vote Compass's own procedure is consistent with this: a content analysis of party platforms and media discourse produces up to 100 candidate questions, these are piloted on a demographically representative online sample of about 1,000 voting-eligible adults, and the final ~30 are chosen for their ability to differentiate parties and voters, their comprehensibility (no "highly technical" items, nothing needing a long explanation, nothing with high non-response in the pilot) and breadth of coverage. Consensus or "valence" issues on which all parties agree are excluded even if salient. ([Vote Compass Methodology 2026.1, §2.1](https://files.voxpoplabs.com/votecompass/methodology.pdf)) The German Wahl-O-Mat and euandi do the same filtering after collecting party positions: euandi Germany 2021 started with 41 statements and dropped six that did not sufficiently polarise the 15 parties ([euandi 2021 About](https://euandi2019.eui.eu/survey/en/deutschland2021/about)); Wahl-O-Mat Hessen 2023 drafted 80 theses, obtained party answers, then selected 38 for topical importance and contested party answers ([bpb FAQ](https://www.bpb.de/themen/wahl-o-mat/hessen-2023/523171/haeufig-gestellte-fragen-zum-wahl-o-mat/)).

**Implication for us.** A statement must divide the parties *and* cover the dimension space evenly; the number of statements per dimension is itself a weighting decision that favours parties at the poles of over-represented dimensions. We cannot run a 1,000-person pilot, but we can (a) use published NZ opinion distributions (NZES 2023 items; Vote Compass 2026 aggregates) as a stand-in to check that statements are not all lopsided, and (b) run Walgrave-style simulations with synthetic respondents to see which parties a given statement set structurally favours (see §7).

### 1.2 Wording: concrete but not technical; one idea per statement; no negations

Van Camp, Lefevere and Walgrave (2014) coded the statements of 26 VAAs in nine countries against VAA builders' own criteria and survey methodology. Builders' guidelines converge on: spread across issues, more statements on salient issues, discriminating between parties, prospective (about future policy). Methodologically they want statements that are *concrete* ("All nuclear power plants should be closed by 2015" is more informative than "Environmental pollution should be tackled"), *single-barrelled* and *unbiased*. The average VAA had 33 statements. Concreteness averaged 2.51 on a 1–3 scale (good), but about one in six statements overall — and up to a third in one tool — were double-barrelled, and the problem had not improved over time. Their key warning: **the push for concreteness itself produces double-barrelled and quantitative statements**, because builders cram the mechanism, the number and the rationale into one sentence; and conditional ("if … then") statements let parties dodge an unpopular position by "playing on the conditionality". ([PDF](https://pure.uva.nl/ws/files/1756596/149241_02_van_Camp_Lefevere_Walgrave.pdf))

Kamoen and Holleman (2017) combined 60 cognitive interviews with the answers of 357,858 users of 34 Dutch municipal VAAs. Users hit a comprehension problem on roughly one statement in five; the culprits were jargon and technical terms (tax names), geographic references, and vague quantifiers such as "more" in statements about taxes, which made users realise they did not know the status quo. Users rarely sought clarification; they guessed and answered anyway. *Semantic* problems (not knowing what a word means) pushed people to "no opinion"; *pragmatic* problems (not knowing the current situation) pushed them to the neutral midpoint — so the two non-substantive answers are not interchangeable. ([SRM 11(2)](https://ojs.ub.uni-konstanz.de/srm/article/view/6728); [Tilburg record](https://research.tilburguniversity.edu/en/publications/i-dont-get-it-response-difficulties-in-answering-political-attitu-2/)) A 2025 follow-up found that adding clickable definitions and information tabs (and a chatbot) significantly reduced non-substantive answers and raised perceived usefulness and knowledge, on desktop and mobile. ([Liebrecht, Kamoen & Van Lieshout 2025](https://research.tilburguniversity.edu/en/publications/from-buttons-to-bots-exploring-the-impact-of-enhanced-features-in/))

Holleman et al. (2016) randomised the polarity of 16 of 30 statements in the 2014 Utrecht Kieskompas (N = 31,112). "Allow vs ban" (implicit negation) wordings shifted mean answers by d = 0.13 overall but d = 0.39 among the least politically sophisticated; explicit "not" wordings d = 0.05 overall, 0.20 for the least sophisticated. Negative wordings produced more favourable evaluations of the object, consistent with negativity bias. Effects varied a lot by item. ([PLoS ONE](https://pmc.ncbi.nlm.nih.gov/articles/PMC5056712/)) Van de Pol (2016) randomised left- vs right-coded *issue headers* above Kieskompas statements: five of 17 statements moved significantly, in the expected direction, with small effects (largest: one user in twelve shifting one category). ([thesis ch. 4](https://pure.uva.nl/ws/files/6823207/04.pdf))

General survey methodology adds: agree/disagree items are prone to acquiescence (a tendency to agree regardless of content) and measurably lower in quality than item-specific response options (Saris, Revilla, Krosnick & Shaeffer 2010, [SRM 4(1)](https://ojs.ub.uni-konstanz.de/srm/article/view/2682); Krosnick & Presser 2010, [Handbook of Survey Research ch. 9](https://web.stanford.edu/dept/communication/faculty/krosnick/docs/2010/2010%20Handbook%20of%20Survey%20Research.pdf)). VAAs nevertheless use agree/disagree almost universally because the same scale must be applied to parties; the standard mitigation is to balance the direction of statements so that acquiescence does not systematically favour one pole. Greaves and Vowles make the same point about the NZES populism items: "it is best practice to include a balanced number of negatively and positively worded items, to avoid agreement bias". ([*A Populist Exception?* ch. 3](https://press-files.anu.edu.au/downloads/press/n6964/pdf/ch03.pdf))

### 1.3 Principles vs policies: where the literature lands

VAAs are overwhelmingly built on *concrete policy proposals*, not abstract values. Wagner and Ruusuvirta (2012), reviewing 13 VAAs in seven countries, describe them as treating party choice as proximity-based issue congruence with only traces of directional or salience logic, and find their party positions have strong convergent validity with expert surveys on left–right and economic positions but weaker on immigration and environment. ([LSE record](https://eprints.lse.ac.uk/46760)) smartvote Australia explicitly says its 35 questions are "primarily focused on specific policy issues, only a few questions relate to more general ideological positions", in order to shift attention to issues and away from personalities and party labels, and it supplies a short factual text beside each question. ([smartvote AU methodology](https://australia2019.smartvote.org/assets/pdf/Positional_matching_methodology.pdf)) Kieskompas, euandi and Vote Compass all code parties from manifesto text onto the same statements users answer, which only works if a party document can plausibly be said to agree or disagree with the statement.

Abstract value instruments do not transfer well to party matching. Lönnqvist and Ilmarinen (2024), with 20,464 ESS respondents across 20 countries, found Schwartz values (mainly universalism) share about 8 per cent of variance with the GAL–TAN position of the party voted for and about 4 per cent with its economic left–right position, and 1 per cent with voting populist. ([Helda PDF](https://helda.helsinki.fi/server/api/core/bitstreams/a8da7b3f-55bd-43be-8c96-dda27c5694ec/content)) Kivikangas et al.'s (2021) meta-analysis of Moral Foundations (89 samples) found the liberal–conservative differences real but "less clear cut than previously thought" and limited by measurement validity and US-heavy samples; it measured self-placement, not vote choice. ([Tampere record](https://researchportal.tuni.fi/en/publications/moral-foundations-and-political-orientation-systematic-review-and/)) Inglehart's four-item post-materialism index has long-running validity disputes and predicts individual party choice poorly outside a few countries ([Inglehart & Abramson 1999](https://ideas.repec.org/a/cup/apsrev/v93y1999i03p665-677_21.html); [Estonian/Eastern European study](https://dspace.ut.ee/handle/10062/27600)). None of these frameworks gives a defensible way to place *parties*: a manifesto does not state a party's score on "sanctity" or "self-direction". Gemenis (2013) raises the matching issue from the other side: how statements are phrased, what response scale is used, how reliably statements can be coded for parties and how validly items scale into dimensions are all open methodological problems for VAAs. ([Acta Politica 48(3) abstract](https://cise.luiss.it/?p=13771))

But fully concrete statements have their own costs, documented above: numbers and programme names require background knowledge (Kamoen & Holleman), concreteness breeds double-barrelled items (Van Camp et al.), named instruments act as party cues, and a very specific instrument can become obsolete within a campaign.

**Where this lands.** The defensible middle ground, and roughly where Kieskompas and Vote Compass sit, is the *concrete-but-general policy direction*: a sentence that names what the state should do or stop doing and makes the trade-off explicit, without a number, an Act name or a party slogan. "Farmers and industry should pay for the greenhouse gases they emit, even if that raises food and fuel prices" can be answered by a voter without knowing what the ETS is, and can be coded from a manifesto that says whether agriculture should pay for emissions. The trade-off clause ("even if Y") does two jobs: it makes the value choice visible, so the quiz measures a priority rather than a wish, and it stops the item being a consensus "valence" statement that every party agrees with. The risk, flagged by Van Camp et al., is that a conditional clause can read as a second proposition; the protocol in §3 limits the cost clause to the generally acknowledged cost of the *same* proposal and bans "and" constructions. A 2025 German Politics paper (Dieing & Siefken, "Read Between the Lines") reportedly finds parties claim "neutral" more often on VAA statements that present trade-offs; we could not retrieve the text, so treat this as a flag to check in party coding (the Vote Compass practice of denying parties the midpoint in self-placement is the standard counter-measure). ([record](https://www.mzes.uni-mannheim.de/en/publications/details/read-between-the-lines-how-linguistics-can-unearth-parties-true-voting-advice-application-positions))

### 1.4 Number of statements and response scale

Most VAAs use 30–40 statements (Van Camp et al.: average 33; Lefevere & Walgrave: range 18–75). Vote Compass uses about 30 (NZ 2026: 30 propositions; [1News](https://www.1news.co.nz/2026/10/04/vote-compass-2026-compare-your-views-with-party-policies/)); euandi 30–35; Wahl-O-Mat 38 (raised from 30 as the number of parties grew); smartvote 32–37 for its party tools (75 for Swiss candidates). More statements improve discrimination, which matters more the more parties there are, but cost completion. Thirty is the practical floor for six dimensions with five statements each.

The 5-point agree/disagree scale with a separate "no opinion" is the modal design (Kieskompas, euandi, Vote Compass, EUvox). Rosema and Louwerse (2016), converting 101-point slider answers from a 2014 Dutch VAA into shorter scales, found scale length can change the resulting advice except for users with an extreme response style, and recommend presenting a **ranked preference list rather than a single best match**. ([Policy & Internet 8(4)](https://www.tomlouwerse.nl/publications/2016-rosema-louwerse-pi/)) Baka, Figgou and Triga (2012) asked 71 Greek VAA users to justify midpoint answers and found the midpoint carries multiple meanings ([IJEG 5(3/4)](https://ktisis.cut.ac.cy/handle/20.500.14279/3447)); Kamoen and Holleman's finding that pragmatic confusion produces "neutral" is the same point. Keep both options, exclude "no opinion" from the match (as euandi does: it "is not treated as a neutral stance but rather is excluded from the calculation"; [euandi FAQ](https://euandi.eu/fr/faq.html)), and treat "neutral" as a real answer at the midpoint.

### 1.5 The algorithm matters as much as the statements

Louwerse and Rosema (2014) re-ran the actual answers of 2010 StemWijzer users (30 statements; 90 per cent answered all) through eight matching methods. The three *high-dimensional* methods — StemWijzer's agreement count, city-block (Manhattan) distance and Euclidean distance — gave the same best match for more than 80 per cent of users (city-block vs Euclidean 94.7 per cent; agreement vs city-block 85.2 per cent) and nearly identical aggregate party shares. But *low-dimensional* models (one-, two-, three- and a seven-dimensional smartvote-style spider) gave radically different results: the one-dimensional model agreed with city-block for only 7.7 per cent of users, the two-dimensional for 24.6 per cent; overall "up to 90 per cent of users would have received a different voting recommendation" under another method. The reason is structural: voters cluster near the centre of any summary dimension while parties sit at the poles, so whichever party happens to be nearest the centre of that map wins — in the 1D model two small orthodox Protestant parties took 80 per cent of best matches; in the 2D model the Labour Party's share fell from 19 to 3 per cent and the Christian Union's rose from 3 to 28 per cent. Ties were common under the agreement method (20 per cent of users), less so under city-block (12 per cent) and Euclidean (9 per cent). ([Acta Politica 49(3)](https://www.tomlouwerse.nl/publications/2014-louwerse-rosema-actapolitica/); [PDF](https://link.springer.com/content/pdf/10.1057%2Fap.2013.30.pdf))

Mendez (2012) tested four matching algorithms on experimental data and concluded they "raise a number of concerns for the future design of VAA systems" ([IJEG 5(3/4)](https://www.inderscience.com/offer.php?id=51316)); Mendez (2017) modelled proximity vs directional logic on EUvox data and found that how dimensionality is modelled changes which model fits better ([JEPOP 27(1)](https://data.gesis.org/gesiskg/resource/bibsonomy-mendez2017modeling)). The 2014 EUvox used a "hybrid" metric averaging city-block distance with a directional (scalar-product-style) distance, so that agreeing on the *side* of an issue counts for more than agreeing on exact intensity ([arXiv 2505.13329, Appendix](https://arxiv.org/pdf/2505.13329), which also tabulates that L1, L2, "L1 bonus" and hybrid metrics on the same smartvote data produce party recommendation shares that differ by tens of percentage points). Germann and Mendez (2016) and Otjes and Louwerse (2014) show that the two-dimensional maps most VAAs draw are defined a priori, often fail tests of unidimensionality and reliability, and do not fit all party systems ("one size fits all" fails) ([Germann & Mendez, Q&Q](https://link.springer.com/doi/10.1007/s11135-015-0186-0); [Otjes & Louwerse, Electoral Studies 36](https://www.tomlouwerse.nl/publications/2014-otjes-louwerse-es/)). Reiljan, Kutiyski and Krouwel (2020) found euandi and EUvox placed the same 200+ parties similarly on cultural and EU dimensions but less consistently on economic left–right, partly because of "problematic issue-statements" that tap more than one construct. ([Party Politics 26(5)](https://research.vu.nl/ws/files/72590928/https_journals.sagepub.com_doi_10.1177_1354068818812209.pdf))

Vote Compass handles this by showing *both* a factor-analytic map (built from pilot data with Bayesian ordinal item-response scoring) and a Manhattan-distance bar chart, and tells users the two "will occasionally" disagree because they measure different things and "there is no perfect measure of political distance". ([Methodology §3.3, §4–5](https://files.voxpoplabs.com/votecompass/methodology.pdf))

**Implication.** Use a high-dimensional proximity metric for the match (the three candidates agree with each other ~85–95 per cent of the time, so the choice among them is second-order); never derive the ranking from a 2D map; show a map only as a labelled secondary view; present a ranked list with the gaps visible rather than one "winner".

### 1.6 Importance weighting

Users can weight questions in smartvote (0.5 / 1 / 2, Euclidean), Vote Compass (adjustable), Wahl-O-Mat (double weight) and euandi (0.5/1/2). The evidence that weights matter much is mixed: Walgrave et al. (2009) found weighting widened the spread of advice; Jäckle and König (2019), comparing user-supplied weights in the Austrian wahlkabine.at with external manifesto-salience weights, found "the use of the internal weights cannot make much of a difference in the present form" while external weights did change the party space ([ÖZP](https://oezp.at/OEZP/article/download/2407/2245/4678)); and the adversarial-robustness study shows users do not know what the numerical weights are and that weights are a manipulation vector. Weights are cheap for users and respect the salience critique (Wagner & Ruusuvirta), so keep them, but as an optional second pass with transparent values, and show the unweighted result too.

### 1.7 Do VAAs change behaviour? (why framing matters)

Munzert and Ramirez-Ruiz's meta-analysis of 22 studies (2006–2019) finds effects on turnout and vote choice whose size and significance vary by design and context ([Garzia et al. 2026 editorial](https://www.cogitatiopress.com/politicsandgovernance/article/download/12331/5014)). Garzia, Trechsel and De Angelis (2017) find VAA users more likely to vote across 12 national election studies and in an Italian field experiment ([Political Communication 34(3)](https://cadmus.eui.eu/handle/1814/69603?show=full)). Germann, Mendez and Gemenis (2023), in field experiments in five countries, find users update party preferences in line with the advice, more so among the less interested and undecided ([Political Communication 40(5)](https://researchportal.bath.ac.uk/en/publications/do-voting-advice-applications-affect-party-preferences-evidence-f/)). Wall, Krouwel and Vitiello (2014) found Kieskompas 2010 users were more likely to vote for a recommended party when they were already seriously considering it ([Party Politics 20(3)](https://cronfa.swan.ac.uk/Record/cronfa13630)); Kleinnijenhuis et al. (2019) show that after filtering out common causes, genuine effects remain mainly for doubting voters ([Party Politics 25(3)](https://research.vu.nl/ws/files/118604966/Genuine_effects_of_vote_advice_applications_on_party_choice.pdf)). Walgrave et al. (2008) found "tiny" effects of the 2004 Belgian *Do the Vote Test* even though politicians and journalists believed the impact was large. ([PDF](https://medialibrary.uantwerpen.be/oldcontent/container2608/files/Walgrave%20Aelst%20Nuytemans%20-%20Do%20the%20vote%20test.pdf)) Effects are real but modest and concentrated among the undecided — which is exactly our audience, so the tool's framing and the visibility of its uncertainty matter.

---

## 2. Recommended dimensions for New Zealand 2026

The Chapel Hill Expert Survey (CHES) structures European party competition along an **economic left–right** dimension (privatisation, taxes, regulation, spending, welfare) and a **GAL–TAN** dimension (green/alternative/libertarian vs traditional/authoritarian/nationalist: personal freedoms such as abortion and same-sex marriage vs order, tradition and stability), with separate items for redistribution, environment ("even at the cost of economic growth"), immigration policy, multiculturalism vs assimilation, civil liberties vs law and order, ethnic minority rights, nationalism vs cosmopolitanism, decentralisation, "people vs elected representatives", and the salience of anti-elite rhetoric. ([CHES 2019 codebook](https://github.com/chesdata/chesdata.github.io/releases/download/ches-europe/2019_CHES_codebook.pdf); Hooghe, Marks & Wilson 2002, [CPS 35](https://www.cambridge.org/core/books/abs/european-integration-and-political-conflict/does-leftright-structure-party-positions-on-european-integration/70226D5A0F1D3EDFF0AFE20FCE92CFC7); Marks et al. 2006, [CPS](https://hooghe.web.unc.edu/wp-content/uploads/sites/11492/2017/02/partycompetition_cps2006.pdf)). Hooghe and Marks (2018) argue immigration, integration and trade now form a "transnational cleavage" with greens and the radical right at its poles ([JEPP 25(1)](https://ces.fas.harvard.edu/uploads/files/events/Hooghe_Marks_2017_-Cleavage-Theory-Meets-Europes-Crises_final-format.pdf)).

New Zealand evidence supports a two-plus-one structure. Jack Vowles summarises NZES research as identifying "two ideological dimensions behind party choice": the balance between state and market, and liberal vs conservative values (individual freedom vs social cohesion and traditional norms) (quoted in [this secondary source](https://memia.substack.com/p/the-axis-of-kindness), citing the NZES). Vowles (2020) shows with NZES 2017 data that authoritarian attitudes lean right and populist attitudes lean left in NZ; the Green vote is strongly associated with liberal social attitudes, the National vote with authoritarianism, and NZ First voters uniquely combine populism and authoritarianism ([*A Populist Exception?* ch. 4](https://press-files.anu.edu.au/downloads/press/n6964/pdf/ch04.pdf)). Sibley and Wilson (2007) found that whether people frame equality as group-based or as meritocracy predicted Labour/Green vs National/NZ First support in 2005 independently of other measures including support for biculturalism — the "Closing the Gaps"/Orewa cleavage ([NZJP 36(2)](https://www.psychology.org.nz/journal-archive/NZJP36-2_SibleyWilson72.pdf)). The NZES has for decades fielded validated items on each of these: income redistribution (C6a), stiffer sentences (C6d), environment vs development on a 7-point trade-off (C7), co-governance in four settings (C9), Treaty settlements (C11), removing Treaty references from law (C12d), Māori say in government (C12i), the Māori electorates (G3), immigration numbers (A15), and populist/authoritarian items (A8e strong leader, A8f people not politicians, A9 referendums, G12). ([NZES 2023 questionnaire](https://www.nzes.net/files/2024/03/2023-NZESFinal-d23f98922870a844.pdf))

The 2026 campaign confirms where the divisions are. Vote Compass 2026 (114,206 respondents, 4–7 October) found the most polarised of its 30 propositions were abolishing the Māori electoral roll (36.8 per cent agree, 43.8 disagree, with large "strongly" blocs on both sides), police powers to move on rough sleepers, and fully funded GP visits, with the Treaty's role in law (39.4 per cent want a smaller role, 30.7 greater) and free tertiary education also divisive; near-consensus items (English tests for work visas 79 per cent, citizenship test 75 per cent, limits on rent increases 69.7 per cent) illustrate statements that would not discriminate parties. ([1News, 15 Oct 2026](https://www.1news.co.nz/2026/10/15/the-three-issues-most-dividing-new-zealand-revealed/)) The Ipsos Issues Monitor (September 2026, n = 1,003) ranks cost of living (63 per cent), healthcare (44), the economy (34), unemployment (21), housing, petrol prices (17), climate change (13) and taxation (8) as the most important issues. ([Ipsos](https://www.ipsos.com/en-nz/34th-ipsos-nz-issues-monitor-sept-2026)) Salience tells us where to put *more* statements; the Lefevere–Walgrave finding tells us not to let one dimension swamp the others.

**Recommended dimensions and statement counts (30 total):**

| Code | Dimension | Poles (A ↔ B) | Statements | Basis |
|---|---|---|---|---|
| E | State and market | active, redistributive state ↔ lower taxes, markets, individual responsibility | 7 | CHES lrecon/redistribution; NZES C6a, C6c, C12a/b/c/h; Ipsos top issues |
| S | Social order and personal freedom (GAL–TAN) | personal freedom, social liberalism ↔ order, tradition, tougher justice | 6 | CHES galtan, civlib_laworder, sociallifestyle; NZES C6d, C6f, G12c; Vowles authoritarianism scale |
| T | Te Tiriti and biculturalism | partnership, Māori-specific arrangements ↔ one law and uniform treatment | 6 | NZES C9, C11, C12d, C12i, G3; Sibley & Wilson; Vote Compass 2026 most divisive items; Treaty Principles Bill (defeated 112–11, [1News 10 Apr 2025](https://www.1news.co.nz/2025/04/10/treaty-principles-bill-voted-down-amid-fiery-mp-debate)) |
| V | Environment and development | protect environment, pay for emissions ↔ growth, extraction, faster approvals | 5 | CHES environment; NZES C7, C12g, C8 |
| O | Openness | fewer migrants, assimilation, traditional alliances ↔ open, pluralist, independent | 3 | CHES immigrate_policy, multiculturalism, nationalism; NZES A15; Hooghe & Marks transnational cleavage |
| D | Democracy and power | direct democracy, limits on money, local autonomy ↔ representative decision-making, central control | 3 | CHES people_vs_elite, regions; NZES A8f, A9c, F4 |

Why not a stand-alone populism dimension: CHES measures anti-elite rhetoric as *salience*, not position; populist attitudes in NZ cut across left and right (Vowles 2020); and party positions on "the elite" cannot be coded from manifestos without judgement calls. The D dimension instead uses concrete institutional questions (referendums, donations, local vs central control) that parties do take positions on. Immigration gets its own small block rather than being folded into GAL–TAN because CHES treats it separately, Wagner and Ruusuvirta found VAA validity weakest there, and in NZ it is weakly correlated with the main economic axis (Vowles 2020 ties it to populism rather than authoritarianism).

Statement counts intentionally over-weight E and under-weight O and D. Salience (Ipsos) justifies seven economic items; O and D have fewer live partisan divisions in 2026 and over-representing them would reward parties with extreme positions on them (Lefevere & Walgrave).

---

## 3. Statement protocol and a draft set of 30

### 3.1 Rules for every statement

1. **One principle, one cost.** The sentence states a policy *direction* and, where the proposal has a widely acknowledged cost, adds it with "even if" so the item measures a priority. The cost must be the generally cited cost of *that* proposal, not a second proposal. No "and". (Van Camp et al. 2014 on double-barrelling; §1.3.)
2. **No numbers, dates, dollar figures, Act or programme names, or agency jargon** (Kamoen & Holleman 2017). If the proposal cannot be stated without one, it is too technical for the quiz (Vote Compass §2.1).
3. **No party, leader, slogan or coalition cues**, and no issue-category headers shown while answering (van de Pol 2016). Statements are presented in random order (see §6).
4. **Affirmative wording, no negations.** Write the "reverse" direction as a positive proposal ("Parliament should decide what the Treaty means") rather than "The courts should not …" (Holleman et al. 2016).
5. **Balanced direction within each dimension**: roughly half the items are worded so that "agree" lands at pole A, half at pole B (acquiescence control; Greaves & Vowles 2020; Krosnick & Presser 2010).
6. **Discriminating**: at least two of the seven parliamentary parties must be codeable at opposite signs from published material. Consensus items are dropped (Vote Compass; euandi; Wahl-O-Mat).
7. **Prospective**: about what should happen, not a verdict on the past (Van Camp et al.).
8. **Answerable without background knowledge**: an optional one-line neutral explainer is available (collapsed) but never required to understand the sentence; it never names parties or positions.
9. **Response format**: Strongly agree / Agree / Neutral / Disagree / Strongly disagree, plus a visually separate "No opinion / skip". After all 30, an optional importance pass: "Less important (×0.5) / Normal (×1) / Very important (×2)" with the multipliers shown.
10. **Where an NZES item exists, adapt it** so results can be sanity-checked against published NZ distributions.

### 3.2 Draft statements (for review)

Polarity: `+A` means agreeing places the respondent at pole A of the dimension (left/liberal/bicultural/green/open/direct-democracy), `+B` the opposite. "Source" gives the validated item or scheme it adapts.

**E — State and market** (A: active, redistributive state; B: smaller state, markets)

| # | Statement | Pol. | Source / notes |
|---|---|---|---|
| E1 | The government should take active steps to reduce the gap between high and low incomes, even if that means higher taxes for some people. | +A | NZES C6a; CHES redistribution |
| E2 | Lower taxes do more good for New Zealand than more government spending, even if it means fewer public services. | +B | NZES C12b; CHES lrecon |
| E3 | Gains people make from rising property and asset values should be taxed in the same way as income from work. | +A | NZES C12h (reversed); principle behind CGT/wealth-tax debates, no rate or threshold |
| E4 | Services like electricity, housing and transport are delivered better by private businesses competing than by government ownership. | +B | NZES C6c (privatisation) |
| E5 | People receiving benefits should face firm obligations and penalties for not meeting them, even if some households end up with less. | +B | CHES lrecon/welfare; sanctions debate |
| E6 | Workers' pay and conditions are best protected by unions bargaining for whole industries, even if that raises costs for employers. | +A | NZES C12a; Fair Pay Agreements principle |
| E7 | Keeping government debt low should take priority over spending more on health and education right now. | +B | NZES 2023 debt-vs-services scale (section C) |

**S — Social order and personal freedom** (A: personal freedom, liberal; B: order, tradition)

| # | Statement | Pol. | Source / notes |
|---|---|---|---|
| S1 | People who commit serious crimes should be given longer prison sentences, even if it means more people in prison for longer at public expense. | +B | NZES C6d; CHES civlib_laworder |
| S2 | Police should have more power to stop, search and move people on in public places, even if that limits some civil liberties. | +B | Vote Compass 2026 divisive item (move-on powers); CHES civlib_laworder |
| S3 | Adults should be free to make their own choices about things like drug use, even if others consider those choices harmful or wrong. | +A | CHES sociallifestyle; drug law debates |
| S4 | Schools and public institutions should reflect changing social attitudes about gender, sexuality and family, even if some parents and communities object. | +A | CHES galtan; relationships and sexuality education, gender debates |
| S5 | People should be free to say what they think in public and online, even if others find it offensive or harmful. | +A | CHES civil liberties; hate-speech and online-harm debates |
| S6 | Young people who offend should face tougher consequences rather than mainly being supported through welfare and youth services. | +B | NZES G12c analogue; youth-justice debates |

**T — Te Tiriti and biculturalism** (A: partnership and Māori-specific arrangements; B: uniform treatment, parliamentary definition)

| # | Statement | Pol. | Source / notes |
|---|---|---|---|
| T1 | Te Tiriti o Waitangi should continue to shape our laws and how public services are run, even if that means some decisions are made differently for Māori. | +A | NZES C12d (reversed) |
| T2 | Government should treat everyone the same regardless of ancestry, so there should be no seats, wards or services set aside specifically for Māori. | +B | NZES G3; Vote Compass 2026 most divisive item; Māori wards |
| T3 | Māori should share decision-making with the Crown over natural resources such as land and water, even if that makes some decisions slower. | +A | NZES C9a/C9c (co-governance) |
| T4 | Parliament, rather than the courts or the Waitangi Tribunal, should decide what the Treaty means in law. | +B | Treaty Principles Bill principle, no bill name |
| T5 | Te reo Māori and tikanga should have a bigger place in public life, such as in schools, government agencies and official names, even if some New Zealanders do not want this. | +A | CHES ethnic_minorities / multiculturalism |
| T6 | The Treaty settlement process has gone far enough and should be brought to a close. | +B | NZES C11 |

**V — Environment and development** (A: protect environment; B: growth and extraction)

| # | Statement | Pol. | Source / notes |
|---|---|---|---|
| V1 | We should do more to protect the environment, even if that means less economic growth. | +A | NZES C7 (converted to agree scale); CHES environment |
| V2 | Farmers and industry should pay for the greenhouse gases they emit, even if that raises food and fuel prices. | +A | NZES C12g; agricultural emissions pricing |
| V3 | Big infrastructure, mining and energy projects should be able to go ahead faster, even if environmental checks are reduced. | +B | fast-track approvals principle, no Act name |
| V4 | New Zealand should keep its international climate commitments even if other countries do less and it costs New Zealand economically. | +A | Paris/net-zero debate |
| V5 | Extracting more minerals, oil and gas from New Zealand's land and waters is a good way to pay for public services. | +B | oil and gas exploration, seabed mining, conservation land |

**O — Openness** (A: open, pluralist, independent; B: fewer migrants, assimilation, traditional alliances)

| # | Statement | Pol. | Source / notes |
|---|---|---|---|
| O1 | New Zealand should let in fewer immigrants, even if some businesses cannot find the workers they need. | +B | NZES A15; CHES immigrate_policy |
| O2 | New migrants should wait several years before they can receive benefits and other public support. | +B | residence/benefit stand-down debates |
| O3 | New Zealand should keep an independent foreign policy rather than tying itself more closely to traditional military allies, even if that means less protection. | +A | CHES nationalism/cosmopolitanism; AUKUS and defence debates |

**D — Democracy and power** (A: direct democracy, limits on money, local autonomy; B: representative decision-making, central control)

| # | Statement | Pol. | Source / notes |
|---|---|---|---|
| D1 | Major national decisions should be put to the public in binding referendums rather than decided by Parliament, even if that slows things down. | +A | NZES A8f, A9c; CHES people_vs_elite |
| D2 | Only individual voters on the electoral roll should be allowed to donate to political parties, even if parties then have less money to campaign. | +A | NZES F4b (Independent Electoral Review proposal) |
| D3 | Local councils should be free to make their own decisions, even if rates and rules then differ from place to place, rather than central government overriding them. | +A | CHES regions; rates caps, Māori wards referendums |

Direction check: of 30 items, 16 are worded towards pole A and 14 towards pole B (A/B by dimension: E 3/4, S 3/3, T 3/3, V 3/2, O 1/2, D 3/0). D is skewed and should be reviewed — rewording D1 or D3 so that "agree" lands at pole B (e.g. "Parliament, not referendums, should make major national decisions …") would bring the set to 15/15. Every item should be checked by at least one reviewer who did not draft it against rules 1–8, and the set should be run through the simulation in §7 before launch.

Items deliberately *not* included and why: GST off food, prescription charges, free school lunches, school phone bans (near-consensus or single-party items that do not discriminate); abortion and euthanasia (conscience issues with no party line, mostly uncodeable, see `quiz-method.md` §4); Pharmac funding (valence); social media age limits (Vote Compass shows broad agreement; low discrimination).

---

## 4. Party coding protocol

The three established methods for placing parties on VAA statements are expert judgement from text, party self-placement, and iterative combinations of the two. Kieskompas's method combines "text-based expert judgement, party-manifesto coding … and a self-placement by political parties" and calibrates them against each other (Krouwel & Elfrinkhof 2014, [Q&Q 48(3)](https://ideas.repec.org/a/spr/qualqt/v48y2014i3p1455-1472.html); Krouwel, Vitiello & Wall 2012, [IJEG](https://inderscience.com/offers.php?id=51308)). EU Profiler/euandi adopted the Kieskompas loop at scale: parties self-place with supporting material; country teams code independently from a *hierarchy of sources with the current manifesto at the top*; discrepancies are compared and the party is asked for more evidence; the team leader and coder make the final call ([euandi 2021 About](https://euandi2019.eui.eu/survey/en/deutschland2021/about); [euandi FAQ](https://euandi.eu/en/faq.html)). Gemenis (2015) and the EUvox project replaced one-shot expert judgement with an anonymous, iterative **Delphi** panel, on the argument that anonymity and controlled feedback filter out biased or uninformed estimates and reduce the random error visible in conventional expert surveys ([Q&Q 49(6)](https://research.utwente.nl/en/publications/an-iterative-expert-survey-approach-for-estimating-parties-policy/); Gemenis & Van Ham 2014 in Garzia & Marschall). Party self-placement alone is the weakest method: Wagner and Ruusuvirta note VAAs "can be manipulated strategically by parties", and Van Camp et al. note double-barrelled or conditional statements let parties avoid unpopular positions.

The EUvox 2014 protocol is the most fully documented and is the template below (Gemenis, Mendez & Wheatley 2019, [RDJ](https://radar.brookes.ac.uk/radar/file/33d40a1f-ae93-4d32-97d9-7dbd91e56ebc/1/%5B24523666%20-%20Research%20Data%20Journal%20for%20the%20Humanities%20and%20Social%20Sciences%5D%20Helping%20Citizens%20to%20Locate%20Political%20Parties%20in%20the%20Policy%20Space_%20a%20Dataset%20for%20the%202014%20elections%20to.pdf)): five coders per party over at least two rounds; a 5-point scale plus "no opinion"; "Completely agree/disagree" only when the party "strongly emphasized the issue and did not place any restrictions"; "Neither" is an *argued* position used in three defined cases (issue addressed only vaguely; both sides emphasised and sides deliberately not taken; party visibly divided); "No opinion" only when the position "was not mentioned in, and could not be inferred from, any relevant sources"; each judgement accompanied by a written justification, a specific source (URL or page), and a confidence rating; after round one a moderator flags any party–statement pair where Van der Eijk's agreement coefficient A is below 0.7 (commonly a coder reversing the scale) and coders see each other's justifications before round two. Vote Compass runs the same logic with a published source hierarchy — (1) election platforms, (2) official policy documents, (3) candidate statements and party press releases, (4) ministers' or spokespeople's statements including Hansard and media, (5) other elected representatives, (6) constitution and member resolutions — explicit rules for strong/somewhat/neutral, independent coding then comparison for inter-coder reliability, party self-placement on a scale *without a midpoint* (parties may argue for neutrality in a comment), a written reconciliation report citing the public statement behind each disputed cell, an academic advisory board for unresolved disputes, and all positions with URLs shown to users. ([Methodology §2.3](https://files.voxpoplabs.com/votecompass/methodology.pdf))

### 4.1 Protocol for this project

1. **Evidence hierarchy (apply in order; record which tier was used).**
   1. The party's current manifesto, policy document or policy page for the 2026 election (archived verbatim under `parties/*/policies/documents/`; the policy.nz dataset in `raw/policy.nz/` is a secondary index that links to originals and is itself an editorial summary — policy.nz says its summaries "reflect the editors' assessment, which may differ from the parties'", [policy.nz/about](https://policy.nz/about)).
   2. Recorded party votes in the 54th Parliament on legislation that directly enacts or repeals the statement's proposal (e.g. Treaty Principles Bill second reading, 112–11 on 10 April 2025). A vote on a bill is evidence about *that bill*; use it for the statement only where the bill's purpose matches the statement's principle, and note when a party has since said it would not repeal.
   3. The party's own written answers to third-party questionnaires (Greenpeace's 20 questions to seven parties, [Greenpeace 2026 scorecards](https://www.greenpeace.org/aotearoa/action-hub/election-2026-environment-scorecards/); NZCTU; Grey Power), using only the party's answer, never the organisation's grade.
   4. Dated statements by the leader or portfolio spokesperson (Hansard, press releases, interviews); the more recent and the more senior, the better.
   5. Coalition agreement commitments and government actions attributable to a specific party's negotiated demand, flagged as such (a government action is not automatically every coalition partner's preference).
   Older statements (pre-2023) count only when nothing newer exists, and the date is recorded.
2. **Scale.** +2 / +1 / 0 / −1 / −2 / `null`, with the EUvox/Vote Compass definitions: ±2 = clear, emphasised, unconditional; ±1 = supports the direction with qualifications, a weaker version, or only part of the proposal; 0 = argued neutrality (three cases above) or a documented contradiction between vote and stated policy; `null` = no position found. `null` is excluded from the match and is never displayed as neutral.
3. **No inference from general ideology.** "Lower taxes" does not imply opposition to a specific tax; "we support the Treaty" does not imply a position on co-governance of water. The one permitted inference: a ±1 may be assigned from an *explicit general statement of principle whose scope plainly includes the statement* (e.g. "we oppose any new taxes on capital" → −1 on E3), with confidence recorded as "low" and the inference stated in the evidence text.
4. **At least two independent coders per party–statement cell**, coding anonymously in round one with a written justification, a source URL (and page/paragraph for PDFs), the evidence tier, and a confidence level (high / medium / low). Round two: coders see each other's justifications (not identities) for every cell where they differ by more than one point, differ in sign, or one has `null` and the other a position; they revise or hold. Remaining disagreements go to a third reviewer who must choose one of the proposed values or `null` with a written reason. Agreement statistics (per cent exact agreement, per cent within one point) are published in the method page.
5. **Party self-placement.** Invite every included party to answer the 30 statements on the 4-point scale (no midpoint) with supporting documents. Where self-placement and coding differ, apply the Vote Compass rule: the party's placement is adopted only if it supplies public material that "conclusively accord[s]" with it; otherwise the coded value stands and the disagreement is disclosed in the cell's evidence text. Record which parties responded.
6. **Freeze and changelog.** Positions are frozen at a stated date; later changes are logged with date and reason, and the user-facing page shows the freeze date.
7. **Inclusion.** All registered parties contesting the party vote are coded; parties with fewer than 15 of 30 positions are shown with a "limited information" badge and excluded from the default ranking (see §5).

### 4.2 What counts as "no position"

- The party has no document, vote, questionnaire answer or dated statement on the proposal or its direct opposite → `null`.
- A survey answer of "no change" or "no policy" → `null` (not opposition).
- The party addresses the topic but only vaguely, or emphasises both sides without choosing, or is visibly split → `0`, with the reason in the evidence text (this is an *argued* neutral, per EUvox).
- The party voted one way and later announced the opposite intention → `0` and explain; if the later statement is the more recent and specific, prefer it with ±1 and note the vote.

---

## 5. Matching algorithm

### 5.1 Core match (high-dimensional weighted city-block)

Let `u_i ∈ {−2,…,+2}` be the user's answer to statement *i*, `p_ij ∈ {−2,…,+2}` party *j*'s coded position, and `w_i ∈ {0.5, 1, 2}` the user's importance weight (default 1). Define the set `S_j` of statements the user answered (not skipped, not "no opinion") *and* for which `p_ij ≠ null`. Per-statement agreement:

```
a_ij = 1 − |u_i − p_ij| / 4            ∈ [0, 1]
```

Raw match:

```
raw_j = Σ_{i∈S_j} w_i · a_ij / Σ_{i∈S_j} w_i
```

This is the Manhattan/city-block proximity used by Vote Compass for its bar chart ([Methodology §5.1](https://files.voxpoplabs.com/votecompass/methodology.pdf)), by euandi (L1), and by Louwerse and Rosema's "city block" variant; it agrees with Euclidean and simple-agreement rankings for the large majority of users (§1.5) and has fewer ties than the agreement count. We prefer city-block over Euclidean because it is explainable ("you were two steps apart on this statement") and because Euclidean squares large disagreements, which rewards parties that take moderate positions on everything. We do not adopt the EUvox hybrid/directional metric: it is a reasonable alternative, but its matrix cannot be explained in one sentence and the evidence that voters reason directionally is context-dependent (Mendez 2017).

### 5.2 Coverage and shrinkage

A party with positions on only a handful of statements can score 100 per cent by luck. Keep the current rule from `quiz-method.md` with a Bayesian reading: shrink each party's match towards the uninformative value 0.5 by *k* phantom neutral statements:

```
match_j = (Σ_{i∈S_j} w_i · a_ij + k · 0.5) / (Σ_{i∈S_j} w_i + k),      k = 4
```

and also apply a hard coverage rule: a party enters the default ranking only if `|S_j| ≥ max(10, 0.5 · M)` where *M* is the number of statements the user answered. Parties below that threshold are listed separately with the badge "based on only N of your M answers" and their (shrunk) score. Sensitivity to *k* is small for parties with full coverage (for a party with 30 positions and raw 0.70, k = 4 gives 0.676) and large by design for parties with few.

### 5.3 Per-dimension agreement and the secondary map

For each dimension *d*, report agreement restricted to its statements, `A_jd = Σ_{i∈d∩S_j} w_i a_ij / Σ_{i∈d∩S_j} w_i`, shown as "You and Party X agree on 4 of 6 Te Tiriti statements; the two you differ on are …". This is the Vote Compass "topics" idea (composite scores from a few questions) and is the most useful output for a conversation starter.

For the map, compute user and party coordinates on each dimension as the polarity-signed mean of answers, `x_d = mean_i( s_i · u_i ) / 2 ∈ [−1, +1]`, where `s_i = +1` for pole-A items and −1 for pole-B items, and plot E against S (with T, V, O, D selectable as alternative axes). Label it "a simplified summary; the ranking above uses all 30 statements, not this map" — because Louwerse and Rosema show the nearest party on a 2D map is frequently not the nearest in the full space, and Germann and Mendez show a priori axes often fail unidimensionality tests. Do not derive any ranking from the map. If the quiz accumulates anonymous answer data, test each dimension's internal consistency (Cronbach's alpha, Mokken scaling) and drop or move items that do not load, as dynamic scale validation recommends.

### 5.4 Uncertainty

Show a **range** for each party's match rather than a single point: recompute `match_j` (a) with every low-confidence cell set to `null`, (b) with every ±1 cell moved one step toward and away from the user, and report the min–max as a thin band. Show the number of low-confidence cells per party. Ties within two percentage points are displayed as ties.

### 5.5 What to show, and what to avoid

Show: a ranked list with the gaps visible; "based on N of your M answers" on every party; per-dimension agreement with links to the evidence for each statement; the unweighted result alongside the weighted one; the freeze date; a one-line description of the method with a link to this page; the party's own words and URL for every cell (Vote Compass does this under "You vs Party"; it is what makes the tool auditable). Avoid: a single "your party is X" headline; percentages to a decimal place (false precision — Louwerse and Rosema's point that the method alone moves results by tens of points); the word "advice" or "recommendation" (Vote Compass: "results are not intended and should not be interpreted as voting advice"; policy.nz: "the vote is the voter's own choice"); treating `null` as 0; hiding small parties entirely (show them with the badge instead); and a map without the disclaimer.

---

## 6. Known biases and mitigations

| Bias | Evidence | Mitigation in this design |
|---|---|---|
| **Acquiescence** (agreeing regardless of content) | Saris et al. 2010; Krosnick & Presser 2010; Greaves & Vowles 2020 | Half of each dimension's items worded toward each pole; dimension scores use polarity-signed means so a yes-sayer lands near the centre rather than at a pole. |
| **Polarity / negation effects** | Holleman et al. 2016 (d = 0.13–0.39 for low-sophistication users) | No "not", "ban", "forbid" where an affirmative alternative exists; both poles written as positive proposals. |
| **Framing by issue label** | van de Pol 2016 | No topic headers during answering; dimension labels appear only in results. |
| **Order effects** | Randomisation recommended as the standard fix; matching is permutation-invariant ([arXiv 2505.13329 §6](https://arxiv.org/pdf/2505.13329)) | Randomise statement order per session (block-randomise so consecutive items are from different dimensions). |
| **Party-cue and brand effects** | Candidate cues move users' answers (Ioannidis & Triga 2026, [P&G](https://www.cogitatiopress.com/politicsandgovernance/article/download/11272/4896)); VAA advice itself moves preferences (Germann et al. 2023) | No party, leader, bill or programme names in statements; party positions revealed only after all answers are in. |
| **Comprehension / satisficing** | Kamoen & Holleman 2017 (1 in 5 items); Liebrecht et al. 2025 | Plain-language test of every item; optional collapsed one-line explainer (factual, no party content) available *before* answering; distinct "Neutral" and "No opinion" buttons. No direct experiment on showing explainers before vs after answering was found; the indirect evidence (comprehension problems produce non-substantive answers; definitions reduce them; smartvote and Vote Compass both place factual context with the question) favours making context available on demand before answering, while keeping anything about parties for after. |
| **Social desirability** | Minimal for anonymous online self-completion; not specifically studied for VAAs | No accounts, no stored answers by default; wording that does not moralise either pole. |
| **Statement-selection skew** | Walgrave et al. 2009; Lefevere & Walgrave 2014 | Balanced counts per dimension; discrimination test; pre-launch simulation (§7); publish which parties the set structurally favours. |
| **Centre-party penalty / extreme-party bonus** | Lefevere & Walgrave 2014 | Limit items per dimension; report per-dimension agreement so a centrist user sees partial agreement with several parties rather than one winner. |
| **Issue-owner penalty** | Lefevere & Walgrave 2014 | Where a niche party's core issue is included, prefer the principle statement over its most unpopular instrument; disclose the effect in limitations. |
| **Strategic self-placement by parties** | Wagner & Ruusuvirta 2012; Van Camp et al. 2014 | Evidence-first coding; self-placement without midpoint; adoption only with conclusive public evidence; disagreements disclosed. |
| **False neutrality on trade-off items** | Dieing & Siefken 2025 (abstract only) | Code neutrality only in the three argued cases; "no change" is `null`, not 0. |
| **Coder bias** | EUvox protocol; Gemenis 2015 | Anonymous first round, written justifications, agreement coefficient, reconciliation, published reliability. |
| **Metric choice** | Louwerse & Rosema 2014; Rosema & Louwerse 2016 | Full-space city-block for ranking; ranked list not single match; map labelled secondary; sensitivity band. |

---

## 7. Limitations and validation checklist

### 7.1 Limitations to state on the public page

- **No representative pilot.** Vote Compass pilots up to 100 items on ~1,000 people; we cannot. Our statement set has not been tested on a sample of New Zealanders. We use NZES 2023 item wording and Vote Compass 2026 published aggregates as partial checks only.
- **Coders are not a panel of independent country experts.** Positions are coded from documents by the project's researchers (and automated assistants) following the protocol in §4; every cell carries its evidence and confidence so readers can check it. Inter-coder agreement is published.
- **Coverage is uneven**, especially for parties outside Parliament; shrinkage and badges mitigate but do not remove this.
- **Positions are a snapshot**; parties release and change policy during the campaign.
- **The proximity model ignores** competence, trust, leadership, record in government, coalition likelihood and the salience parties themselves attach to issues (Wagner & Ruusuvirta 2012). The `track-record.md` files cover some of this.
- **Any statement set favours some parties.** The simulation below estimates which; the estimate is itself model-dependent.
- **Dimensions are imposed a priori** and have not been validated on user data (Germann & Mendez 2016).
- **Effects are real but small and concentrated among the undecided**; the tool is a conversation starter, not a decision.

### 7.2 Validation checklist (run before launch; record results in `quiz-method.md`)

**Statements**
- [ ] Each item passes rules 1–8 (§3.1), checked by a reviewer who did not draft it.
- [ ] Reading-age check (target: plain English, no sentence over ~30 words).
- [ ] Direction balance per dimension within ±1 item; overall as close to 15/15 as possible (draft is 16/14; D block needs one reversal).
- [ ] Discrimination: for each item, at least two parliamentary parties coded with opposite signs; any item on which five or more of the seven are identical is reconsidered.
- [ ] No item contains a number, date, Act or programme name, party or leader name.
- [ ] Items adapted from NZES/CHES are cross-referenced in the data file.

**Party coding**
- [ ] Every non-null cell has evidence text, source URL, tier, date and confidence.
- [ ] ≥2 independent coders; reconciliation complete; per cent exact and within-one agreement computed and published.
- [ ] No cell is inferred from general ideology beyond the single permitted ±1 rule, and such cells are flagged low confidence.
- [ ] Parties invited to self-place; responses and disagreements logged.
- [ ] Freeze date set; changelog started.

**Algorithm and simulation**
- [ ] Unit tests: identical answers → 100; opposite extremes → 0; skipped and "no opinion" excluded; `null` excluded; weights applied; k shrinkage correct.
- [ ] Walgrave-style simulation: generate synthetic respondents (e.g. 10,000 draws from independent per-item distributions approximating NZES/Vote Compass marginals, plus a correlated-dimensions variant) and record the share of best matches per party and how it changes when each statement is dropped or when any 25 of the 30 are used. Publish the party-share table and name the parties the set favours.
- [ ] Metric robustness: recompute best match under city-block, Euclidean and agreement count; report the share of synthetic users whose top party changes (expect ≤ 15 per cent per Louwerse & Rosema; investigate if higher).
- [ ] Map check: for synthetic users, share whose nearest party on the 2D map differs from the full-space top match (publish; expect it to be large, which is why the map is secondary).
- [ ] Dimension coherence: once real anonymous answers exist (if collected), compute alpha/Mokken H per dimension; flag items with negative or near-zero loadings.

**Display**
- [ ] Ranked list, coverage badge, per-dimension agreement, sensitivity band, unweighted vs weighted, freeze date, method link, evidence links all present.
- [ ] No "advice/recommendation" wording; no decimals; ties shown as ties.
- [ ] Randomised order confirmed; no topic headers while answering.
- [ ] Accessibility: keyboard-operable, scale labels readable by screen readers, mobile layout.

---

## Sources

Downloaded full texts are indexed in [`raw/quiz-research/SOURCES.md`](../raw/quiz-research/SOURCES.md). Key references with URLs:

- Garzia, D. & Marschall, S. (2012) "Voting Advice Applications under review: the state of research", *IJEG* 5(3/4). https://cadmus.eui.eu/handle/1814/25277
- Garzia, D. & Marschall, S. (eds) (2014) *Matching Voters with Parties and Candidates*, ECPR Press. https://cadmus.eui.eu/handle/1814/34156
- Garzia, D., Marschall, S., Tromborg, M. W. & Albertsen, A. (2026) editorial, *Politics and Governance* 14. https://doi.org/10.17645/pag.12331
- Garzia, D., Trechsel, A. H. & De Angelis, A. (2017) "Voting Advice Applications and Electoral Participation", *Political Communication* 34(3). https://doi.org/10.1080/10584609.2016.1267053
- Germann, M., Mendez, F. & Gemenis, K. (2023) "Do VAAs Affect Party Preferences?", *Political Communication* 40(5). https://doi.org/10.1080/10584609.2023.2181896
- Germann, M. & Mendez, F. (2016) "Dynamic scale validation reloaded", *Quality & Quantity*. https://doi.org/10.1007/s11135-015-0186-0
- Gemenis, K. (2013) "Estimating parties' policy positions through VAAs", *Acta Politica* 48(3). https://doi.org/10.1057/ap.2012.36 (abstract: https://cise.luiss.it/?p=13771)
- Gemenis, K. (2015) "An iterative expert survey approach for estimating parties' policy positions", *Quality & Quantity* 49(6). https://doi.org/10.1007/s11135-014-0109-5
- Gemenis, K., Mendez, F. & Wheatley, J. (2019) EUvox 2014 dataset paper, *RDJ*. https://doi.org/10.1163/24523666-00401002
- Holleman, B. et al. (2016) "Positive vs. Negative: The Impact of Question Polarity in VAAs", *PLoS ONE*. https://pmc.ncbi.nlm.nih.gov/articles/PMC5056712/
- Hooghe, L., Marks, G. & Wilson, C. (2002), *CPS* 35; Marks et al. (2006), *CPS*; Hooghe & Marks (2018), *JEPP* 25(1). https://hooghe.web.unc.edu/wp-content/uploads/sites/11492/2017/02/partycompetition_cps2006.pdf
- Jäckle, S. & König, P. D. (2019) "Mapping the Austrian political spectrum with the help of VAAs", *ÖZP*. https://oezp.at/OEZP/article/download/2407/2245/4678
- Kamoen, N. & Holleman, B. (2017) "I don't get it", *Survey Research Methods* 11(2). https://ojs.ub.uni-konstanz.de/srm/article/view/6728
- Kivikangas, J. M. et al. (2021) "Moral foundations and political orientation: systematic review and meta-analysis", *Psychological Bulletin* 147. https://researchportal.tuni.fi/en/publications/moral-foundations-and-political-orientation-systematic-review-and/
- Kleinnijenhuis, J. et al. (2019) "Genuine effects of vote advice applications on party choice", *Party Politics* 25(3). https://doi.org/10.1177/1354068817713121
- König, P. D. & Jäckle, S. (2018) "VAAs and the Estimation of Party Positions – A Reliable Tool?", *SPSR*. https://ssoar.info/ssoar/handle/document/71549
- Krouwel, A. & Elfrinkhof, A. (2014) "Combining strengths of methods of party positioning", *Quality & Quantity* 48(3). https://doi.org/10.1007/s11135-013-9846-0
- Krouwel, A., Vitiello, T. & Wall, M. (2012) "The practicalities of issuing vote advice", *IJEG* 5(3/4). https://doi.org/10.1504/IJEG.2012.051308
- Lefevere, J. & Walgrave, S. (2014) "A perfect match?", *Electoral Studies* 36. https://doi.org/10.1016/j.electstud.2014.04.002
- Liebrecht, C., Kamoen, N. & Van Lieshout, R. (2025) "From buttons to bots", ECPR. https://research.tilburguniversity.edu/en/publications/from-buttons-to-bots-exploring-the-impact-of-enhanced-features-in/
- Lönnqvist, J.-E. & Ilmarinen, V. (2024) "Basic personal values and vote choice in 20 European countries". https://helda.helsinki.fi/server/api/core/bitstreams/a8da7b3f-55bd-43be-8c96-dda27c5694ec/content
- Louwerse, T. & Rosema, M. (2014) "The design effects of voting advice applications", *Acta Politica* 49(3). https://doi.org/10.1057/ap.2013.30
- Mendez, F. (2012) "Matching voters with political parties and candidates: an empirical test of four algorithms", *IJEG* 5(3/4). https://doi.org/10.1504/IJEG.2012.051316
- Mendez, F. (2017) "Modeling proximity and directional decisional logic", *JEPOP* 27(1). https://doi.org/10.1080/17457289.2016.1269113
- Otjes, S. & Louwerse, T. (2014) "Spatial models in voting advice applications", *Electoral Studies* 36. https://www.tomlouwerse.nl/publications/2014-otjes-louwerse-es/
- Reiljan, A., Kutiyski, Y. & Krouwel, A. (2020) "Mapping parties in a multidimensional European political space", *Party Politics* 26(5). https://doi.org/10.1177/1354068818812209
- Rosema, M. & Louwerse, T. (2016) "Response Scales in VAAs", *Policy & Internet* 8(4). https://doi.org/10.1002/poi3.139
- Saris, W., Revilla, M., Krosnick, J. & Shaeffer, E. (2010) *Survey Research Methods* 4(1). https://ojs.ub.uni-konstanz.de/srm/article/view/2682
- Sibley, C. & Wilson, M. (2007) "Political Attitudes and the Ideology of Equality", *NZJP* 36(2). https://www.psychology.org.nz/journal-archive/NZJP36-2_SibleyWilson72.pdf
- Van Camp, K., Lefevere, J. & Walgrave, S. (2014) in Garzia & Marschall (eds). https://pure.uva.nl/ws/files/1756596/149241_02_van_Camp_Lefevere_Walgrave.pdf
- van de Pol, J. (2016) *Voting Wiser*, PhD thesis, ch. 4. https://pure.uva.nl/ws/files/6823207/04.pdf
- Vowles, J. (2020) ch. 4 and Greaves, L. & Vowles, J. (2020) ch. 3 in *A Populist Exception?*, ANU Press. https://press-files.anu.edu.au/downloads/press/n6964/pdf/ch04.pdf ; https://press-files.anu.edu.au/downloads/press/n6964/pdf/ch03.pdf
- Vox Pop Labs (2026) *Vote Compass Methodology 2026.1*. https://files.voxpoplabs.com/votecompass/methodology.pdf
- Wagner, M. & Ruusuvirta, O. (2012) "Matching voters to parties", *Acta Politica* 47(4). https://eprints.lse.ac.uk/46760
- Walgrave, S., Nuytemans, M. & Pepermans, K. (2009) "Voting Aid Applications and the Effect of Statement Selection", *WEP* 32(6). https://doi.org/10.1080/01402380903230637
- Walgrave, S., Van Aelst, P. & Nuytemans, M. (2008) "'Do the vote test'", *Acta Politica* 43. https://medialibrary.uantwerpen.be/oldcontent/container2608/files/Walgrave%20Aelst%20Nuytemans%20-%20Do%20the%20vote%20test.pdf
- Wall, M., Krouwel, A. & Vitiello, T. (2014) "Do voters follow the recommendations of voter advice application websites?", *Party Politics* 20(3). https://doi.org/10.1177/1354068811436054
- Chapel Hill Expert Survey 2019 codebook. https://github.com/chesdata/chesdata.github.io/releases/download/ches-europe/2019_CHES_codebook.pdf
- NZES 2023 questionnaire. https://www.nzes.net/files/2024/03/2023-NZESFinal-d23f98922870a844.pdf
- 1News, Vote Compass 2026 (4 Oct and 15 Oct 2026). https://www.1news.co.nz/2026/10/04/vote-compass-2026-compare-your-views-with-party-policies/ ; https://www.1news.co.nz/2026/10/15/the-three-issues-most-dividing-new-zealand-revealed/
- Ipsos NZ Issues Monitor, September 2026. https://www.ipsos.com/en-nz/34th-ipsos-nz-issues-monitor-sept-2026
- policy.nz About. https://policy.nz/about
- euandi 2021 Germany About; euandi FAQ. https://euandi2019.eui.eu/survey/en/deutschland2021/about ; https://euandi.eu/en/faq.html
- smartvote Australia 2019 / ACT 2020 methodology. https://australia2019.smartvote.org/assets/pdf/Positional_matching_methodology.pdf
- Wahl-O-Mat FAQ (bpb). https://www.bpb.de/themen/wahl-o-mat/hessen-2023/523171/haeufig-gestellte-fragen-zum-wahl-o-mat/
- "Recommender Systems for Democracy: Toward Adversarial Robustness in VAAs" (2025), arXiv 2505.13329. https://arxiv.org/pdf/2505.13329
