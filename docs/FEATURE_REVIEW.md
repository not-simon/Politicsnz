# Ballot Book NZ — Independent Feature Review

**Reviewer stance:** independent product review, written blind. I was given the feature list only and did not open the site or its code, so nothing here is a claim about how a feature is actually implemented; it is a view on what a product with this feature set is likely to be missing, where it could go wrong, and what to do about it with 15 days to election day (7 Nov 2026) and two days to the enrolment deadline (25 Oct).

**Comparators used:** Vote Compass (Vox Pop Labs; 1News 2026 edition, 30 propositions), Kieskompas, smartvote (CH), Wahl-O-Mat (DE), policy.nz (Policy Ltd, NZ 2017/2020/2023 GE and 2025 local), The Spinoff and RNZ election hubs, ABC Australia (Antony Green calculators, Vote Compass), BBC election results, FiveThirtyEight/The Economist forecast pages, Democracy Club (WhoCanIVoteFor / WhereDoIVote, UK), TheyWorkForYou / OpenAustralia, and the NZ Electoral Commission's own vote.nz / elections.nz services.

---

## 0. Headline verdict

The feature list is unusually deep for a volunteer-grade civic site. Fourteen areas, 1,435 policies with full source text, 685 people profiles, a Sainte-Laguë calculator, a calibrated forecast and a promise tracker is more than policy.nz, The Spinoff and RNZ offered in 2023 *combined*. Depth is not the problem.

The problem is that the list reads as a reference work built by and for people who already know how MMP works and already intend to vote. Almost nothing in it is about the two questions ordinary voters actually ask in the last fortnight — **"Am I enrolled and where do I go?"** and **"What happened?"** on election night — and almost nothing addresses the people the Electoral Commission's own Access 2026 plan says are hardest to serve (disabled voters, te reo speakers, Pacific communities, overseas voters, first-timers). The 2026 election also has a rule change that makes the first question more urgent than in any election since 1993: **same-day and advance-period enrolment have been abolished** (Electoral Amendment Act 2025). Anyone not enrolled by midnight Sunday 25 October cannot vote. If Ballot Book NZ has a countdown on its home page but not a red-banner "two days left to enrol" with a link to vote.nz, it is failing the one test that matters this week.

Second, the product has *four* overlapping "tell me who I agree with" tools (quiz, swipe, compass, issues-by-party) and no "help me use them well" layer: no glossary, no "why trust this", no methodology hub a non-academic can read, no sharing, no print, no offline. Every one of the four tools carries known VAA biases; running four of them multiplies the exposure.

Third, the results side (forecast, most-likely Parliament, bloc probabilities) is the most sophisticated public NZ forecast I know of, which is exactly why its framing needs the most care. The Economist and FiveThirtyEight learned the hard way that a probability presented without a frequency framing, a "what we don't know" box and a visible track record gets read as a prediction and blamed as one.

---

## 1. What's missing

Grouped by voter moment. Items marked **[gap vs comparator]** are things at least one comparable product does.

### 1.1 The next two days: enrolment

| Gap | Why it matters | Who does it |
|---|---|---|
| **Enrolment deadline banner, site-wide, with vote.nz link** | 25 Oct is the hard cutoff for the first time ever. The Commission forecast ~700k special votes last cycle; many of those people now simply cannot vote. The "key dates" list on the home page is not enough; a date in a list does not read as "you will be locked out". | vote.nz (every page), Democracy Club (banner on WhoCanIVoteFor), Spinoff hub |
| **"Am I enrolled? Check now"** deep link to vote.nz/enrol with the ID options (NZ driver licence, passport, RealMe) spelled out | Removes one search step at the moment of highest intent. | vote.nz |
| **"Enrolled but moved?"** update-details prompt | Renters and young voters are the most likely to be enrolled at an old address and end up casting a special vote or in the wrong electorate for the candidate they researched on your site. | vote.nz |

### 1.2 Two weeks out: how, where and when to vote

| Gap | Why it matters | Who does it |
|---|---|---|
| **Voting-place lookup** (or at minimum a prominent deep link to vote.nz's finder, with hours) **[gap vs comparator]** | Democracy Club's WhereDoIVote processed >10M postcode lookups in 2026 and scored 88% satisfaction, higher than the candidate site. "Where do I go" is the single most searched election question. You have a boundary map; it should answer "nearest voting place" or hand off to the official finder in one tap. | vote.nz, Democracy Club, Spinoff (links out) |
| **How to vote, by situation** — first-timer, voting outside your electorate, overseas (open since 21 Oct; download-papers route; 64 overseas sites; return deadlines vary), disabled (telephone dictation, Easy Read, NZSL, large print, Braille, accessible booths), unpublished roll, in hospital/rest home/prison-remand, student away from home | vote.nz has all of this but spread over dozens of pages and PDFs. A one-screen "which of these are you?" chooser is a genuine value-add and nobody in NZ media does it well. | vote.nz (content), BBC "how to vote" explainers |
| **Special votes explainer** (what they are, why ~15–20% of votes are special, why election-night results shift, "since 1999 specials have favoured the left" with evidence) | Directly inoculates against the "the count was rigged" narrative that circulates every official-results day. | Newsroom/NZ Herald explainers, elections.nz |
| **EasyVote card explainer** and "you can still vote without it" | Common anxiety; low effort. | vote.nz |
| **Printable one-page electorate guide** (candidates, parties, where/when to vote, the ballot layout) **[gap vs comparator]** | People take notes into the booth. Policy.nz's 2023 "print your choices" and Democracy Club's "print this page" are heavily used by older voters and by community groups running enrolment drives. | policy.nz, Democracy Club |
| **Candidate comparison *within* an electorate** (side-by-side questionnaire answers, party, incumbent, 2023 margin) | You have candidate questionnaire answers; the natural view is a grid for the seat, not 5–9 separate profile pages. | policy.nz 2023 (candidate Q&A grid), smartvote (candidate smartspider) |
| **The two-vote decision aid**: "My party vote goes to X; in my seat, does my electorate vote matter?" with the coat-tail / threshold logic explained for that seat | MMP's strategic layer (e.g., Epsom, Tāmaki Makaurau, 5% vs electorate seat) is where ordinary voters are most confused and most manipulated. Your calculator already knows the maths; surface it per seat. | None does this well; it would be a differentiator |

### 1.3 Election night and after

| Gap | Why it matters | Who does it |
|---|---|---|
| **Election-night results view** **[gap vs comparator]** | You have the seat map, the Sainte-Laguë calculator, the time scrubber and a forecast. Without a live results view fed from electionresults.govt.nz, all of that goes dark at 7pm on 7 Nov, which is the one moment traffic will peak. Preliminary results land progressively (Commission targets 50% by 10pm, 95% by 11:30pm). Even a 5-minute polled static JSON into the existing seat map, plus "forecast said / result says", is a huge win. | ABC, BBC, RNZ, 1News, Spinoff all run live results; The Economist/538 publish forecast-vs-result |
| **Special-vote-adjusted projection on the night** | Preliminary results exclude specials; a simple historical specials-swing adjustment ("if specials move as they did in 2017–2023, the Parliament looks like…") is the single most useful thing a forecast site can add on the night. | Nobody in NZ does this publicly; Newsroom/Herald explain it in prose |
| **Post-election coalition tracker** | Official results are 27 Nov; negotiations will run to December. Your coalition builder plus a "what each party has said about who it will work with" page becomes the coalition tracker, with a timeline of statements. | Spinoff/RNZ live blogs; Wikipedia |
| **"What the result means for your electorate / your quiz result"** | Close the loop: a user who ran the quiz in October should get "parties you matched with won N seats" in November. | None; differentiator |

### 1.4 Trust, transparency and safety

| Gap | Why it matters | Who does it |
|---|---|---|
| **"Why trust this?" page** (who we are, how funded, no party affiliation, how data is coded, how errors are fixed, how to complain) | You have editorial standards, a review log and a correction process in the long-form section. That is the right content in the wrong place; it needs a one-screen summary linked from every tool's results page. | Vote Compass "About", Kieskompas "Methodology", Wahl-O-Mat "Wie entsteht der Wahl-O-Mat", Democracy Club "About" |
| **Methodology hub in plain English** for the quiz, swipe, compass, forecast and promise verdicts, each with a "how could this be wrong" section | Every VAA that has survived scrutiny publishes this. The ETH Zurich 2025 adversarial-robustness paper on smartvote shows matching-method choice alone shifts a party's recommendation frequency by up to 105%. You are switching from one algorithm to another mid-campaign; say so and show the differences. | smartvote, Kieskompas, Vote Compass |
| **Misinformation / "check the claim" hub** | The Commission launched a "Think before you share" campaign in July 2026 after false ID-requirement and wrong-election-date claims; deepfake videos of NZ politicians at Waitangi have already circulated. You have fact-check notes on candidates; collect them, add the voting-process myths, and link the Commission's official statements. | AAP FactCheck, RNZ, BBC Verify, AEC disinformation register |
| **Glossary** (overhang, threshold, Sainte-Laguë, list MP, waka-jumping, special vote, writ day, coat-tailing, EasyVote, confidence and supply, caretaker convention) | You use every one of these terms. Hover definitions plus one page. | ABC, BBC, elections.nz |
| **Feedback loop on every page** ("Report an error", "Is something missing?") | The review log suggests you fix things; make the intake obvious and show "last reviewed" per page. | Democracy Club, Wikipedia |

### 1.5 Reach: accessibility, language, platform

| Gap | Why it matters | Who does it |
|---|---|---|
| **WCAG 2.2 AA audit and statement** | Disabled voters are reported (1News, 5 Oct 2026) still hunting for accessible booths and criticising parties for PDF-only policies. A site with 993 scraped PDFs is in the same trap unless the extracted text is the primary view, headings are real headings, images have alt text, colour is never the only encoding (your map, seat map and compass all risk this) and the quiz is keyboard- and screen-reader-operable. | vote.nz (Access 2026), BBC, ABC, gov.uk |
| **Dark mode and reduced-motion** | Cheap; the scrubber/play animations should respect `prefers-reduced-motion`. | Most news sites |
| **Te reo Māori** at minimum for navigation, the Māori-electorate pages, the "MMP in one minute" explainer and the how-to-vote page; **Easy Read / plain-language version** of the core explainers; **Samoan, Tongan, simplified Chinese, Hindi** for the enrolment/how-to-vote screens | The Commission's own 2026 "change" flyer is published in English and te reo Māori (plus a third language version); Pacific advocates say the enrolment rule change hits their communities hardest. Full translation of 1,435 policies is impossible; translating the 5 pages that get people to the booth is not. | vote.nz (Easy Read, NZSL, large print, Braille, audio), Democracy Club (Welsh) |
| **Reading-age check** on summaries ("plain-English summary" should mean Flesch-Kincaid ~grade 8; many "plain English" political summaries test at grade 12+) | Audience is "ordinary voters wanting simple information first". Measure it. | gov.uk content standards |
| **Offline / PWA** | Voting places and rural electorates have poor signal; a service worker caching the how-to-vote pages, the user's electorate page and their quiz result is a genuine use case, not a vanity feature. | Few news sites do this; it is a differentiator |
| **Performance budget** | GitHub Pages static is a good start, but 17 parties × policy JSON plus a map with 71 boundaries × 6 elections plus 685 photos can easily blow mobile budgets. Target <1.5s LCP on a mid-range Android over 4G for the home, electorate and quiz pages. | Everyone measures this |

### 1.6 Sharing, discovery, data

| Gap | Why it matters | Who does it |
|---|---|---|
| **Share/export quiz, swipe and compass results** (image card, copy link with encoded answers, PDF) **[gap vs comparator]** | Vote Compass's 700k NZ users in 2023 came largely from shared result cards. Results that cannot be shared do not spread. Design the share card so it shows the *distribution* not just "You match ACT 78%" (see §2). | Vote Compass, Wahl-O-Mat, smartvote, Kieskompas |
| **Bookmarks / shortlist** (local-only, no accounts) | "Save these 6 policies / 3 candidates to compare later" is the natural follow-on from swipe and search. | policy.nz 2023 "Your picks" |
| **Search across everything** | 14 sections, 1,435 policies, 685 people, 71 electorates, 17 issues, 129 polls. If search is per-section, a voter typing "Māori wards" or "Chris Bishop" must guess the section first. One search box with typed results. | TheyWorkForYou, BBC |
| **SEO and deep links** | Every policy, person, electorate, poll and verdict needs its own stable URL, `<title>`, meta description and Open Graph card. Journalists will link to a single promise verdict; voters will Google a candidate's name. Static sites on GitHub Pages can do this well but only if someone has done it. | TheyWorkForYou, Wikipedia |
| **Embeddable widgets for media** (poll trend, seat calculator, electorate card, countdown) | Newswire's "Election Sidekick" already runs as an embed in NZ; community papers and student media would embed yours for free. One `<iframe>` endpoint per widget with a credit line. | ABC, Datawrapper-style embeds, Newswire NZ |
| **RSS / Atom feeds and "what changed since last week"** | A changelog page ("12 new policies, 3 verdicts changed, 4 polls added") turns a reference site into something people revisit, and gives journalists a reason to check in. Feeds for polls, promise verdicts and corrections. | TheyWorkForYou alerts, Democracy Club newsletter, GitHub releases |
| **API / open-data docs** | You have an open JSON repository with a licence. What's missing from the list is a *documented* API: schema docs per file, stable paths, version/changelog, example queries, a "last updated" field, and a status page. Without docs, nobody reuses it. | Democracy Club (CSV + API), TheyWorkForYou API, AEC/ECQ media feeds |
| **Notifications** (opt-in email or web push, no accounts) for "polls updated", "your electorate candidate list changed", "results are in" | Lower priority given no-tracking stance; RSS and a calendar (.ics) file for the key dates covers 80% of this. | Democracy Club email reminders |

### 1.7 Onboarding and time-to-answer

The home page lists seven things (countdown, Parliament today, entry points, MMP explainer, key dates, poll snapshot, plus the ballot). A first-time visitor on a phone needs one question: **"What do you want to do?"** → *Check I can vote / Find my electorate / Help me choose / See what's likely to happen / Look something up.* Measure time-to-answer for the five most common tasks (I'd guess: am I enrolled; who is standing where I live; where do I vote; which party matches me; who is winning). Every comparator that has done usability testing (Democracy Club publishes satisfaction scores; 1News ran first-timers and retirees through Vote Compass on camera) has found that the explainer content people love in the newsroom is skipped by the people it's for.

---

## 2. Features that could mislead or bias voters, and guards

The site has four preference-matching tools, a forecast and several "who's winning" visualisations. Each has a documented failure mode in the VAA and forecasting literature. None of these are reasons not to ship; all are reasons to add guard rails.

### 2.1 Find-your-match quiz (45 statements → 30 principle + trade-off)

**Risks**
- *Statement selection is the algorithm.* Kieskompas's and Wahl-O-Mat's own reviewers say the choice of statements, not the matching maths, determines most of the result. Six dimensions × 5 items means a party with a distinctive position on a seventh dimension (e.g., Te Tiriti, firearms, euthanasia) is invisible. Publish the dimension coverage and the statements that were *rejected* and why.
- *City-block vs Euclidean vs agreement-count.* The ETH 2025 paper (Berdoz et al., "Recommender Systems for Democracy") shows that switching matching method alone shifts a party's recommendation share by up to 105%. You are changing algorithm mid-campaign. Users who got result A on 20 Oct and result B on 30 Oct will, reasonably, conclude the tool is broken or fiddled. Guard: version the quiz visibly ("Quiz v2, released DD Oct, replaces v1; here's what changed and why"), keep v1 results readable via their share link, and publish a comparison of how both versions score the same answer set.
- *Percent-match false precision.* "You match National 74%, ACT 71%" reads as a ranking with meaning; a 3-point gap on 30 items with a 5-point scale is noise. Guard: show a confidence band or bucket (strong/moderate/weak), show the full distribution for all 17 parties, and never show a single "winner". Vote Compass deliberately refuses to rank; Wahl-O-Mat shows all parties as bars with the user's agreement count.
- *Party-blind wording leaks.* "Party-blind" statements still encode party frames in vocabulary ("tax relief" vs "tax cuts"; "co-governance" vs "partnership"). Two independent coders is good; add a third check — have the statements rated for valence by a panel that doesn't know the parties' positions, and alternate the direction of agreement (half the statements should be ones where "agree" is the left/progressive answer and half the right/conservative answer) to kill acquiescence bias.
- *Importance weighting* magnifies the most salient (i.e., most campaigned-on) issues, which systematically favours the parties running the loudest campaigns. Guard: default weights to equal; show the result both ways.
- *Coverage badges* are good. Add the inverse: "We could not find a position for Party X on 6 of 30 statements; their score is computed on 24." Missing positions must not be treated as "neutral" (the smartvote default) because that pulls unknown parties to the centre and inflates matches for small, vague parties.
- *Order effects.* Randomise statement order per session and party order in results (alphabetical or randomised, never by match or by poll size). Show "sorted by: match | A–Z | ballot order".

### 2.2 Policy swipe

**Risks**
- *The tally is a popularity contest weighted by document length.* A party with 200 policies gets 200 chances to be agreed with; a party with 12 gets 12. If the tally shows raw counts, the Greens/Labour/National (long manifestos) will dominate every user's result regardless of views. Guard: normalise to a rate (agreed ÷ shown) per party, and sample policies evenly across parties and topics, not proportionally to volume.
- *Agreeable-policy bias.* Most policies are written to be agreeable ("more nurses", "safer communities"). A swipe tool rewards vagueness. Guard: pair each policy with its cost/trade-off where known ("funded by…", "costed: no"), and include the "what critics say" line after the reveal.
- *Reveal-after-decide* is the right design but the reveal moment is where users update their priors about the *party*, not the policy. Show the policy's source and date, and "N other parties have a similar policy" so the user doesn't attribute a consensus position to one party.
- *Gamification.* Swipe is fun; fun erodes the sense that this is consequential. Cap a session (e.g., 20 cards), then show the summary with a "this is a sample of 1,435 policies" line and a link to the topic view.

### 2.3 Political compass

**Risks**
- *The classic Political Compass is pseudo-scientific and widely criticised;* you have avoided it by using openly licensed academic scales, which is the right call, but the output — a dot on two axes — carries the same false authority. Guard: show the user as a *cloud* (bootstrapped from their answers) not a dot; label axes neutrally and symmetrically; never colour quadrants.
- *Party placement from "published expert data and our own coding".* Expert surveys (CHES, GPS, V-Party) lag by years and don't cover NZ minor parties well; your own coding is defensible only if the coding sheet and inter-coder reliability are published. Show both placements for each party, and the disagreement between them, rather than an average.
- *Populism as a third axis* is academically fashionable and politically loaded in NZ (it will land on NZ First and Te Pāti Māori). Either drop it from the user-facing chart or present it with the scale items visible so users can see what "populism" means operationally.
- *Compass + quiz + swipe disagreement.* A user will inevitably get three different "closest parties" from three tools. That is honest, but only if you explain it up front ("these tools measure different things; here's how"). Otherwise it reads as incompetence.

### 2.4 Forecast and "most likely Parliament"

**Risks**
- *Point estimates read as predictions.* "Most likely Parliament" is a mode of a 40,000-run simulation; it may have a probability of 4%. Guard: show the probability of the modal outcome next to it, and show the top five outcomes with their probabilities. The Economist's 2020 model page and FiveThirtyEight's "80 in 100 is not 100 in 100" line are the templates; both still got blamed. Lead with the *range*, not the mode.
- *Bloc-majority probabilities* are the most shared number and the most abused. "72% chance of a right bloc majority" becomes "it's over" on social media. Guard: frequency framing ("in 72 of 100 elections like this one…"), a visible "things this model cannot know" box (turnout under the new enrolment rules, specials, undecideds, polling-industry correlated error, late swings like 2017 and 2020), and the backtest *with its misses* shown as prominently as its hits.
- *Correlated polling error.* If 9 pollsters all miss the same way (as in 2020, when every pollster overstated National), recency-weighted pooling does not help. Say explicitly what the model assumes about correlated error and show the 2020 backtest.
- *Māori seat odds* based on thin polling (a handful of Māori-electorate polls, often with small samples) will be the least reliable and the most consequential numbers on the site, because of the overhang. Mark them as low-confidence; consider showing them only as ranges.
- *Bandwagon / strategic effects.* VAA and forecast research is split on whether forecasts suppress turnout; the 2016 and 2020 US debates are enough to justify caution. Guard: do not show forecast numbers on the quiz/swipe/compass result pages; keep the forecast behind one deliberate tap; and on election day itself, replace the forecast with "voting is open until 7pm, here's how" (the Commission's rules on election-day publishing also bear on this, see below).
- *Election-day law.* It is an offence in NZ to publish material on election day that is intended or likely to influence voters, and the Electoral Commission has previously advised media on what may stay online. Have a compliance view ready: a static "polling day" mode that hides the quiz/swipe/compass results and forecast until 7pm, and check the current Commission guidance for 2026. This is a Must-have.

### 2.5 Polls, pollster house effects, trend

- *House effects presented as "bias"* will be read as "that pollster is crooked". Label as "difference from the pooled average", explain that it may be the pollster who is right, and show the uncertainty.
- *Trend line start date and y-axis* are the classic manipulation surface. Fixed y-axis from 0 for party vote, fixed start date, and the same chart for every party.
- *Poll snapshot on the home page* is the first thing many voters will see. If it's a single pollster's latest, it is a coin flip; show the pooled estimate with a range, and make the pollster list one tap away.

### 2.6 Parties, promises, people

- *"What they say / what critics say"* — ensure the critics are balanced across the spectrum and that "critics" for every party includes at least one non-partisan expert (e.g., Treasury, the Climate Change Commission, Infrastructure Commission), not only opposing parties. Publish the count of critic quotes per party.
- *Promise verdicts* are editorial judgements; "broken" is a strong word. Show the rubric, the evidence and the date; let parties respond (a right-of-reply field, even if empty); and show the kept/broken ratio per party *with the denominator* and a note that governing parties are the only ones that can break promises. Opposition parties will otherwise show up as spotless.
- *"Costed: yes/no"* needs a definition ("independently costed by…" vs "party-published figures"); a self-costed manifesto is not costed in the sense a voter assumes.
- *Controversies on people pages* are a defamation surface and a bias surface. Publish the inclusion criteria (reported by ≥2 credible outlets, on the public record, relevant to office), date everything, and make the right-of-reply/correction route visible on the profile itself.
- *Ordering everywhere.* Party lists on the ballot illustration should be in official ballot order (alphabetical by party name on the actual paper) with a note; candidate lists should follow the ballot; party lists elsewhere alphabetical or randomised, never by poll standing except on the polls page.
- *Photos.* Use neutral, same-size, same-crop images; a flattering photo for one candidate and a scowl for another is bias nobody intends.

### 2.7 Structural

- *Four matching tools, one data team.* Every one depends on the same coding of party positions. A coding error propagates into four results pages. Publish the position table (party × statement, with source links) as a page in its own right so the public can audit it. Kieskompas does this; it is the single most trust-building page a VAA can publish.
- *Independence and funding* must be on the "why trust this" page, including who built it, with what tooling, and what the scheduled jobs scrape. A site that uses AI-assisted summarisation (likely, at this scale) should say so, say how it is checked, and say what the known failure modes are; the 2025 German studies found LLM-coded party positions skew left by a large margin.

---

## 3. Prioritised backlog

Effort: **S** = hours to a day, **M** = 2–4 days, **L** = a week or more. "Problem" is the voter problem solved.

### Must-have before 7 Nov (in order)

| # | Item | Effort | Problem solved |
|---|---|---|---|
| M1 | **Enrolment-deadline banner** on every page until midnight 25 Oct → then "voting is open; enrolment closed" with special-vote explainer | S | Voters locked out by the 2025 rule change |
| M2 | **How-to-vote chooser**: first-time / away from home / overseas / disabled / unpublished roll / student, each a one-screen answer with vote.nz deep links, hours, EasyVote note, "what to bring" (nothing) | M | "How do I actually do this?" — the top vote.nz query |
| M3 | **Voting-place handoff**: electorate page and home page get a "Find your nearest voting place" button to the official finder; if feasible, ingest the Commission's voting-place list into your map | S (link) / M (ingest) | "Where do I go?" |
| M4 | **Election-day compliance mode**: a flag that hides quiz/swipe/compass results, forecast numbers and poll snapshot from 00:00 to 19:00 on 7 Nov and shows how-to-vote instead; verify against Commission 2026 guidance | S | Legal exposure; avoids influencing voters on the day |
| M5 | **Election-night results view**: poll electionresults.govt.nz every 5 min into a static JSON; colour the existing electorate and seat maps; show party vote %, seats, "majority = 61", forecast-vs-result, and a specials caveat; add historical specials adjustment if time allows | L | The single largest traffic moment; your maps otherwise go dark |
| M6 | **"Why trust this" + plain-English methodology hub**, linked from every tool result and from the forecast, with a "how this could be wrong" section on each | M | Trust; defends against the inevitable "biased tool" accusation |
| M7 | **Quiz result de-biasing**: show all 17 parties, buckets not decimals, randomised statement order, party order toggle, coverage disclosure, version note explaining v1→v2 | M | False precision, order effects, mid-campaign algorithm change |
| M8 | **Swipe tally normalisation**: rate not count; even sampling across parties; session cap; trade-off/cost line on reveal | S–M | Long manifestos winning by volume |
| M9 | **Forecast framing**: probability on the "most likely Parliament", top-5 outcomes, frequency language, uncertainty box, backtest misses shown, Māori-seat odds as ranges | S–M | Probabilities read as predictions |
| M10 | **Accessibility pass on the five critical paths** (home, electorate, how-to-vote, quiz, results): keyboard, focus, alt text, contrast, non-colour encoding on maps, reduced-motion; publish an accessibility statement | M | Disabled voters (and the Commission's Access 2026 commitments) |
| M11 | **Share cards** for quiz/swipe/compass showing the distribution across parties, with a permalink encoding answers | M | Reach; honest sharing |
| M12 | **Glossary** with hover definitions for the ~20 MMP terms the site uses | S | Comprehension; first-time voters |
| M13 | **Site-wide search** (client-side index over parties, people, policies, electorates, issues, glossary) | M | Time-to-answer; 14 sections is too many to browse |
| M14 | **Printable electorate one-pager** | S–M | Notes into the booth; community enrolment drives; older voters |
| M15 | **Party-position audit table** (party × quiz statement × source) as a public page | S (data exists) | Auditability; the Kieskompas standard |

### Should-have (before official results 27 Nov if not before 7 Nov)

| # | Item | Effort | Problem solved |
|---|---|---|---|
| S1 | Candidate comparison grid per electorate (questionnaire answers side by side) | M | Choosing an electorate vote |
| S2 | Per-seat "does my electorate vote matter?" strategic explainer using the calculator | M | MMP strategic confusion; coat-tail seats |
| S3 | Post-election coalition tracker (statements timeline + coalition builder pre-loaded with the result) | M | "What happens now?" from 8 Nov to Christmas |
| S4 | Te reo Māori for nav, Māori-electorate pages, MMP explainer, how-to-vote; Easy Read version of how-to-vote; Samoan and Tongan how-to-vote | M–L | Reach to the groups the enrolment change hits hardest |
| S5 | Misinformation hub: voting-process myths (ID requirement, wrong date, "specials are rigged"), candidate fact-checks collected, Commission statements linked | M | Trust in the result |
| S6 | "What changed this week" changelog + RSS/Atom for polls, verdicts, corrections; .ics calendar of key dates | S–M | Return visits; journalist use |
| S7 | Open-data documentation: schema per file, stable paths, version field, examples, licence summary, status page | M | Reuse by media and researchers |
| S8 | Embeddable widgets (poll trend, seat calculator, electorate card, countdown) | M | Community and student media reach |
| S9 | Promise tracker fairness: rubric page, denominator shown, right-of-reply field, "only governments can break promises" note | S | Opposition parties looking spotless |
| S10 | Dark mode, reduced-motion, performance budget enforced in CI (Lighthouse) | S–M | Mobile users on poor connections |
| S11 | Reading-age check on all plain-English summaries; rewrite those above grade 9 | M–L | "Simple first" audience |
| S12 | Shortlist/bookmarks (localStorage) for policies, candidates and parties | M | Comparison across sessions |

### Nice-to-have

| # | Item | Effort | Problem solved |
|---|---|---|---|
| N1 | PWA/offline for how-to-vote, your electorate and your saved results | M | Rural signal; voting-place queue |
| N2 | Quiz result → election result follow-up ("parties you matched won N seats") | S after M5 | Closing the civic loop |
| N3 | Compass as cloud not dot; dual party placements (expert vs own coding) shown with disagreement | M | False authority of a dot |
| N4 | Time-to-answer instrumentation without tracking (self-reported "did you find it?" widget, aggregated client-side and submitted anonymously) | S | Product learning while keeping the no-tracking promise |
| N5 | Opt-in web push for "results are in" and "your electorate list changed" | M | Engagement; low priority given RSS |
| N6 | Further languages (Hindi, simplified Chinese, Korean, Tagalog) for how-to-vote | M | Reach |
| N7 | Journalist pack: CSV export of any table, citation format, "embed this chart" | S | Media reuse |
| N8 | Historical quiz: "which party would you have matched in 2017?" | L | Fun; low value |

---

## 4. Ten quick wins (each ≤ 1 day)

1. **Red enrolment banner, today.** "Enrolment closes midnight Sunday 25 October. You cannot enrol after that. Check at vote.nz." On every page. Replace Monday with "Voting is open 26 Oct–7 Nov. Not sure you're enrolled? You may be able to cast a special vote — here's how."
2. **"Find your voting place" button** on the home page and every electorate page, deep-linked to the official finder, with hours (9am–7pm election day).
3. **Glossary with hover tooltips** for overhang, threshold, Sainte-Laguë, list MP, special vote, writ day, coat-tailing, EasyVote, unpublished roll, confidence and supply.
4. **Show the probability next to "most likely Parliament"**, and show the top five outcomes. One line of code, enormous framing difference.
5. **Normalise the swipe tally** to agreed ÷ shown per party and sample cards evenly across parties.
6. **Randomise quiz statement order and alphabetise party results** by default with a sort toggle; show all 17 parties.
7. **Add "How this could be wrong" boxes** to the quiz results, forecast and promise pages (three paragraphs each).
8. **Publish the party-position audit table** (party × statement × source) you already have in your data as a page.
9. **.ics file and RSS feed** for key dates and corrections; link the existing review log and correction process from the footer as "Report an error".
10. **Election-day mode flag** in the build so compliance on 7 Nov is a one-line change, not a 6am scramble.

---

## 5. Closing note

Ballot Book NZ already has more *content* than the voter needs. What it lacks is the thin layer that turns content into help at the three moments that matter: *can I vote* (this weekend), *how do I vote* (the fortnight), and *what happened* (the night and the three weeks after). Those three moments are also where every comparable product, from vote.nz to Democracy Club to the BBC, concentrates its effort, and where a static site can be genuinely excellent because the answers change slowly. Build the thin layer; then make the four matching tools honest about their uncertainty; then make the forecast humble. The depth will still be there for the journalists and students in December.

*Sources consulted (public web, October 2026): vote.nz and elections.nz 2026 pages (key dates, enrol-by-25-October, what to expect at the voting place, what happens after the election, Access 2026 Accessibility Action Plan, accessible-formats pages, E78 change flyer, 2026 media kit); 1News Vote Compass 2026 coverage and "How the new enrolment rules could affect the election result" (16 Oct 2026); 1News "Disabled voters still hunting for accessible booths" (5 Oct 2026); Waatea News on the Commission's "Think before you share" campaign (30 Jul 2026); PMN and Newstalk ZB on the end of same-day enrolment; Victoria University / 1News on AI in the 2026 campaign; Berdoz et al., "Recommender Systems for Democracy: Toward Adversarial Robustness in Voting Advice Applications" (arXiv 2505.13329, 2025); Benesch et al. on smartvote (J. Politics 2023); Democracy Club 2026 post-election newsletter (WhereDoIVote 88% / WhoCanIVoteFor 77% satisfaction, >10M lookups); Wahl-O-Mat 2025 reporting (38 statements, ~26M uses); ABC Antony Green calculator documentation; policy.nz about page; Newsroom and Newstalk ZB special-votes explainers; AEC and NSWEC media-feed documentation (as models for results ingestion).*

---

# Round 2

Written 23 October 2026, still blind to the implementation. Two parts: (1) further ideas beyond the Round 1 backlog, organised by the audiences that comparable products and the Electoral Commission's own data say are hardest to reach, plus what makes a site worth opening every day; (2) a verdict on each of the owner's seven proposals with the simplest good implementation on a static GitHub Pages site (no server, no accounts, no tracking), bias flags, and an S/M/L ranking.

Two constraints shape everything below. First, **static means static**: anything "live" is a scheduled GitHub Action writing JSON into the repo, and anything "personal" lives in the visitor's `localStorage` or in the URL. Second, **the no-tracking promise is a feature**; it rules out third-party embeds (social posts, YouTube, most comment widgets) because they all load trackers.

## R2.1 More ideas: audiences

### People who rarely vote

Turnout in 2023 fell to 78.2% of enrolled voters (Electoral Commission), and the people who don't vote are not short of information; they are short of a *reason* and a *plan*. The behavioural evidence (Nickerson & Rogers 2010 and the GOTV literature since) is that asking people to state *when, where and how* they will vote raises turnout more than any amount of persuasion.

- **Voting plan builder** (S): three taps — "I'll vote on [date] at [voting place or 'near work/home'] with [alone / a friend]" — producing an `.ics` event, a pre-filled SMS/WhatsApp message (`sms:` / `https://wa.me/?text=`), and a printable card. No server needed. This is the single highest-leverage turnout feature a static site can offer and nobody in NZ does it.
- **"It takes five minutes" myth-busting strip** (S): you don't need ID; you can vote at any voting place in the country; you don't need your EasyVote card; it's free; employers must allow time off on election day (Electoral Act s162 — check current wording); you can take notes in; you don't have to vote for both.
- **"What actually changes for me"** persona entry points (M): renter, mortgage-holder, student, parent, superannuitant, small-business owner, farmer, new migrant, disabled person. Each pulls the tagged policies of *every* party into one scroll. Personas are how low-interest voters think; issues are how journalists think. Bias guard: tagging must be done for all 17 parties against the same rubric, and the persona page must show "N parties have no stated policy here" rather than hide them.
- **"I don't follow politics" page** (S): a 300-word honest answer to "does my vote matter under MMP?" (yes, the party vote is national; one vote in 2.9 million moves a seat roughly every 25,000 votes), with no jargon, and a single next step.

### Young and first-time voters

18–24 turnout among the enrolled was 74.2% in 2023, better than the 25–44 bracket; the leak is at *enrolment*, which is why the 25 October cutoff is the story for this group.

- **"Your first vote" walkthrough** (S–M): the full journey as a swipeable set of illustrated cards (enrolment → EasyVote → walk in → two ticks → fold → box), reusing your illustrative ballot. Export each card as a 1080×1920 image so it can be posted to an Instagram/TikTok story *as an image* (no third-party embed, no tracker). 1News filmed first-timers using Vote Compass; the finding was that the mechanics, not the policies, were the confusing part.
- **Student mode** (S): enrolled at home or at uni? Vote anywhere; if your electorate is elsewhere you'll cast a special vote; what the Māori/general roll question means; link to your home electorate page.
- **"What Parliament did to under-25s this term"** (M): a plain list from your promise and record data — student allowances/loans, minimum wage, youth payment, rental rules, public transport — with each party's 2026 position. This is a *record* page, not an opinion page; keep it to votes and legislation.
- **Distribution, not features**: offer the quiz, swipe and how-to-vote pages as embeds to student associations, Student Volunteer Army, Rock Enrol-style campaigns and school civics teachers (NZ Curriculum social studies has a civics strand). An embed with a credit line costs nothing and is how Democracy Club gets most of its reach.

### Māori audiences

Māori-descent turnout fell to 70.3% in 2023; young Māori turnout *rose* (70.3%, from 54.9% in 2014). The seven Māori electorates also carry the overhang risk that makes the whole seat count uncertain.

- **Māori electorates hub** (M): one page for the seven seats — candidates, 2023 results, the roll explanation (roll-switching has closed; explain what that means for 2026), why these seats can create an overhang, and the Māori-seat odds from your forecast *with their low-confidence label*. Te Pāti Māori, Labour, Greens, National, NZ First and ACT candidates shown identically.
- **Te reo Māori as a first-class toggle** for the five critical paths (home, how-to-vote, your electorate, MMP explainer, glossary), not a machine translation. Macrons and place names already correct everywhere (Ōtaki, Whangārei, Tāmaki Makaurau). Ask a Māori media partner (Whakaata Māori, Waatea, Te Ao Māori News) to review the translations and to embed the Māori electorates widget.
- **Te Tiriti issue page** (exists) should be the model for *every* issue page: sourced key facts, every party's position in their own words, "what critics say" from across the spectrum including iwi leaders and the Waitangi Tribunal, dated.

### Pasifika audiences

Pacific advocates (PMN, Waatea) say the end of same-day enrolment hits Pacific communities hardest: young, mobile, renting, often enrolled at an old address.

- **Samoan and Tongan how-to-vote and "have you moved?" pages** (S–M for translation; content exists): these two languages cover most of the gap; add Cook Islands Māori, Fijian and Niuean if a community partner can review.
- **Church and community printable** (S): A4, one side, big type: enrol by 25 Oct, vote 26 Oct–7 Nov, vote anywhere, bring nothing, phone 0800 36 76 56 — in English plus one Pacific language per sheet. Pacific churches and sports clubs *are* the distribution network; give them something to photocopy.
- **Family voting plan** (S): the voting plan builder above with a "we're going together" variant.

### Older voters

Over-65s vote at the highest rate and are the least served by swipe-and-tap interfaces.

- **Text-size control and a persistent "Print this page" button** (S) on every page; large-print PDF of the how-to-vote and electorate pages.
- **"You don't need the internet"** page (S): rest-home and hospital voting (the Commission takes voting to residential facilities), postal options, the 0800 number, EasyVote by post, taking a support person in, telephone dictation for blind voters (confirm 2026 availability with the Commission).
- **List alternatives for every swipe or scrubber interaction** so no information is reachable only by gesture.

### Rural voters

- **Low-data mode** (S–M): a toggle (or automatic on `navigator.connection.saveData`) that drops photos and map tiles. 685 photos and boundary polygons are expensive on rural 4G.
- **Offline (PWA)** for how-to-vote, your electorate page and your saved results (already N1; promote it for rural users).
- **Voting-place hours vary in small towns**; many advance voting places are open only certain days. Your voting-place handoff should warn "check hours; small-town advance places may not be open every day".
- **Rural issue page** (M): water regulation, agricultural emissions, roading, rural health, with every party's position.

### People with low literacy

Roughly 40% of NZ adults read below the level needed for everyday tasks (OECD PIAAC). "Plain English" that tests at grade 12 is not plain.

- **"Listen" button** (S): browser `SpeechSynthesis` reads the summary aloud — client-side, free, no third party, works offline. Add to every party summary, issue explainer and how-to-vote step.
- **Easy Read versions** (M) of the how-to-vote and MMP pages in the Commission's Easy Read style (one idea per sentence, picture beside each paragraph). The Commission publishes an Easy Read guide; match its conventions so the two feel like one system.
- **Reading-level gate in CI** (S): fail the build if any "plain-English summary" exceeds grade 9 on Flesch–Kincaid; the owner then rewrites.
- **Icons for the 17 issues and the 17 parties' *topics*** (not logos) so pages scan without reading.

## R2.2 More ideas: worth opening every day

A reference site is visited once; a *daily* site has something new above the fold each morning and a reason to come back at a known time. Keep this respectful — no streaks, no badges for engagement, no notifications you did not ask for.

1. **"Today" panel on the home page** (M, mostly assembly): days to enrol / days to vote; what changed in the last 24 hours (new polls, new policies, changed verdicts, new candidates, corrections); today's campaign events (debates — the final leaders' debate is 5 Nov 7pm on TVNZ 1; policy launches); a policy-of-the-day card; on-this-day (see R2.3.2). All of it generated by the existing scheduled jobs writing one `today.json`.
2. **Policy of the day** (S): one real policy, party hidden, agree/disagree, reveal. One card, not twenty. Rotates by date-seeded random so every visitor sees the same card and can talk about it. Even sampling across parties over the fortnight (15 days, 17 parties — publish the rotation).
3. **Poll watch** (S): "A new [pollster] poll is out: here's what Parliament would look like if it were the result, and here's what the pooled trend says" — auto-generated from existing data each time a poll lands. Journalists will link it.
4. **Promise counter** (S): "2026 promises catalogued: N (+k today)"; "Verdicts updated: m". Neutral, factual, visible.
5. **Weekly changelog + RSS** (S6 in Round 1) with a Friday "this week in the campaign" auto-digest.
6. **Electorate watchlist** (S): star up to five electorates (localStorage); the home page and the election-night view show them first. Turns the 71-seat map into *your* map.
7. **Election-night watch-party mode** (M): a big-screen layout (laptop on a TV, or phone cast) that auto-refreshes, cycles your watchlist, shows the national tally, "majority = 61", and a plain-language ticker ("Preliminary results exclude ~15–20% of votes: special votes. Official results 27 Nov."). Optional non-partisan bingo card for groups ("first seat called", "a party within 0.5% of 5%", "an overhang appears", "a list MP returns via a seat") — fun without cheering for anyone.
8. **Special-votes countdown (8–27 Nov)** (S): what specials have done in every election since 1999, what the thresholds are this time ("Party X needs +0.3% from specials to reach 5%"), and the three most likely Parliaments after specials. This is the period when misinformation about the count peaks; be the calm explainer.
9. **Post-election "what happens now" timeline** (S): return of the writ, official results, coalition talks, confidence-and-supply, swearing-in, Speaker election, Governor-General's commission — each dated as it happens. Reuses the glossary.
10. **"Did it come true?" follow-ups** (S after results): forecast vs result scorecard, quiz-match vs seats, polls vs result by pollster. Publishing your own misses is the best trust-builder you have.

## R2.3 Verdicts on the owner's proposals

Ranked by value-for-effort for the final two weeks and election night. Effort: S = hours–1 day, M = 2–4 days, L = 1 week+.

| Rank | Proposal | Verdict | Effort |
|---|---|---|---|
| 1 | Shareable result cards | **Do it** (Round 1 M11) | S–M |
| 2 | Export/import saved quiz results | **Do it**; it is the same mechanism as the share link | S |
| 3 | Geolocation → electorate → candidates | **Do it**, with a suburb-search fallback and a boundary-confidence warning; **link out** for nearest voting place | M |
| 4 | Party press-release feed from Scoop RSS | **Do it**, with per-party equal-slot layout; **do not** build a live social feed | M |
| 5 | Auto-linking party and politician names | **Do it at build time** with a stoplist; first mention per section only | S–M |
| 6 | Politicians' social-media "follow" directory | **Do a directory of outbound links**; no embeds | S |
| 7 | Pass-the-phone party-guessing game | **Do a single-device hot-seat version** with a seed-in-URL "same deck" challenge; proximity pairing confirmed impossible without a server | M |
| 8 | "On this day in NZ politics" widget | **Nice-to-have**; fold into the "Today" panel; curate, don't scrape | S–M |

### R2.3.1 Pass-the-phone party-guessing game (2+ players)

**Confirmation:** automatic proximity pairing is not achievable on a static GitHub Pages site. Web Bluetooth and WebRTC both need a signalling/discovery step that requires either a server or a manual exchange; Web Bluetooth also has no iOS Safari support; the Web NFC API is Android-Chrome only; Nearby/AirDrop are not exposed to the web. A WebRTC "copy this blob to the other phone" handshake is technically serverless but is a worse experience than simply passing the phone. Rule it out and don't apologise for it.

**Formats that work without a server, best first:**

1. **Hot-seat on one phone.** Enter player names (local only), 10 rounds, the phone is passed after each answer. Round types to mix: *Whose policy?* (real policy text, pick the party from 4 options), *Which year?* (an election result or seat map, pick the year), *Higher or lower?* (did Party X get more or fewer party votes in 2020 than 2023?), *Which seat?* (an electorate description, pick it on the map), *Who's the MP?* (photo → name, from your 685 profiles, current MPs only). Avoid quote-guessing: quotes out of context are the mislead-vector, policies from the party's own document are not.
2. **Shared screen, phones as controllers — not possible without a server.** The closest static equivalent is *shared screen, verbal answers*: cast the phone/laptop to a TV, the host reads, players shout, the host taps the winner's name to score. Design the game screen for a TV (big type, high contrast, 16:9) and this works for a flat.
3. **"Same deck" challenge across devices.** Put the random seed and quiz version in the URL hash (`#deck=20261031-ab12`). Share the link or show a QR code; a friend on their own phone gets the identical 10 questions and compares scores. Asynchronous, serverless, and it is how Wordle spread.

**Scoring:** 1 point per correct answer, +1 streak bonus from the third consecutive correct answer, a tie-break round from a different category; final scoreboard as a shareable image (same renderer as result cards). Do not score "agreement" — only knowledge. Keep a session to ~3 minutes.

**Keeping it non-partisan and fun:** sample questions evenly across all 17 parties and across years, and publish the sampling rule; party options shown in random order; never use controversies, scandals or "gaffes" as question material; every reveal shows the source and the party's own wording; no question whose wrong answers imply ridicule of a party; no leaderboard beyond the room. Offer "learn more" on the reveal (link to the policy, seat or person). Because it teaches *who stands for what*, it is a civic feature, not a toy; say so on the intro screen.

**Election-day caveat:** anything that reveals party positions is "likely to influence" and should be hidden under the election-day compliance flag (Round 1 M4).

**Bias flags:** small-party overexposure (even sampling means ACT and NZ First appear as often as National — that is fine and arguably good, but say so); photo quality differences between MPs; policy text that is cut so short it changes meaning (use a minimum of one full sentence). **Effort: M.**

### R2.3.2 "On this day in NZ politics" widget

**Verdict:** pleasant, low-value in the final fortnight, but a cheap daily hook if folded into the "Today" panel. **Do not scrape nzhistory.govt.nz** (no API/RSS; Crown copyright on the text) or rely on Wikipedia's "On this day" (no NZ political focus). **Curate**: build a 365-entry JSON from data you already hold — election dates since 1853, by-elections, coalition agreement dates, Royal Assent dates of landmark Acts (MMP referendum 1993, Electoral Act 1993 commencement, Māori electorates 1867, women's suffrage 19 Sept 1893, voting age to 18 in 1974), party foundation dates, leaders' first days. Aim for ≥1 entry per day for the 15 days to the election and backfill the rest later. Each entry: one sentence, one source link, one "related page" link into your site.

**Bias flag:** selection is editorial. Keep entries to *process and institutional* events (elections, laws, foundings, leadership changes), avoid anniversaries of scandals or "gaffes", and keep a rough balance across parties over any 30-day window. Show the source. **Effort: S for the fortnight, M for the full year.**

### R2.3.3 Geolocation → your electorate → candidates, and nearest voting place

**Verdict:** the electorate half is a strong feature and fully achievable client-side; the voting-place half should be a *handoff*, not a rebuild.

**Simplest good implementation:**

1. **Boundaries:** Stats NZ publishes "General Electorates 2025" (the 64 seats used for 2026) and the Māori electorates as ArcGIS feature services and on Datafinder (attribution: Representation Commission / Stats NZ). Export once, simplify with mapshaper or TopoJSON to ~1 MB total (the coastline is the expensive part; you can simplify aggressively because you only need point-in-polygon at street scale), and serve as a static TopoJSON. You probably already have this for the map.
2. **Point-in-polygon:** `navigator.geolocation.getCurrentPosition` → a 30-line ray-casting test against the simplified polygons (or Turf's `booleanPointInPolygon`). Run it for *both* the general and Māori layers, and ask "Are you on the Māori roll or the general roll?" before showing the result, or show both ("Your general electorate is X; if you're on the Māori roll it's Y").
3. **Fallback without GPS or on desktop:** a typeahead over ~3,500 suburbs/localities with centroids (LINZ Gazetteer / Stats NZ SA2 centroids, open data), then the same point-in-polygon. Do not attempt address geocoding client-side (the LINZ address dataset is ~2.3 million rows); for addresses, link to vote.nz's lookup.
4. **Confidence:** compute the distance from the point to the nearest electorate boundary. If under ~1 km, show "You're close to a boundary — the 2025 boundary review moved lines here; confirm at vote.nz" and name both electorates. Boundary-change suburbs (Epsom/Mt Albert, the new/renamed seats) are exactly where people will be wrong.
5. **Privacy:** the computation runs on the device; nothing leaves it. Say so in the button label ("Use my location — stays on your phone").
6. **Nearest voting place:** I found no open CSV of 2026 voting places from the Commission; the official finder on vote.nz is the authoritative source and includes hours, which change daily during advance voting. Deep-link to it (with the electorate pre-selected if the URL scheme allows) rather than scraping a list that will go stale. If a usable open dataset appears, the client-side nearest-point calculation is trivial (haversine over ~2,500 points).

**Bias/mislead flags:** wrong electorate near boundaries (mitigated above); wrong roll; implying a voter *must* vote at a particular place (they can vote anywhere). **Effort: M** (S if boundaries are already in the map bundle).

### R2.3.4 Auto-linking party and politician names

**Verdict:** yes, at *build time* (never at runtime; never on user-entered text), with discipline.

**Implementation:** compile an alias table from your people and party index (full name, surname-with-title, known nicknames; party names, abbreviations like "TPM", "NZF"). Walk text nodes in rendered HTML (not inside `<a>`, `<h1-3>`, `<code>`, blockquotes of original documents, or alt text), longest-match first, **first occurrence per section only**, link to the profile/party page, add `title` with the person's current role. Maintain a **stoplist** for ambiguous tokens: "Green/green", "Labour/labour", "First", "ACT/act", "Brown", "Little", "Peters" vs "Peter", "National" the adjective. Test on a corpus of 200 paragraphs and publish the false-positive rate. Mark auto-links visually the same as hand links; don't underline every third word.

**Bias flags:** link density is attention; a page about Labour's housing policy will link "National" every time it criticises them, which is fine, but do not auto-link *inside the parties' own policy documents* (their text should remain their text). Make sure every current MP and candidate resolves — a missing alias for a minor-party candidate is an unfair omission. **Effort: S–M** (the stoplist is the work).

### R2.3.5 Exporting/importing saved quiz results

**Verdict:** do it; it is also your share mechanism and your protection against the v1→v2 algorithm change.

**Implementation:** encode `{version, answers[30] (0–4), weights[30] (0–2), timestamp}` as a compact base64url string in the URL hash (≈70 characters). "Copy my results link" *is* export; opening the link on another device *is* import (the result is recomputed client-side from the answers, so the matching stays auditable and the link never contains a "party"). Also offer "Download as JSON" and "Paste a link or JSON" for the people who want files, and a QR code for phone-to-laptop. Store the last result in `localStorage`; never store anything else. Keep a `version` field so a v1 link opened after v2 ships says "This result was computed with quiz v1 (45 statements). Here's your v1 result; retake v2 here."

**Bias flags:** none beyond the share-card framing. **Effort: S.**

### R2.3.6 Social-media "follow" directory + Scoop RSS press-release feed

**Verdict:** split in two. The **directory** is a yes. A **live social feed is a no** on this stack and under this privacy promise. The **press-release feed** is a yes and is the better product anyway.

*Why not a live social feed:* X has ended free read access; it is pay-per-read ($0.005/post read, no free tier for new apps as of 2026). Instagram's Graph API exposes only accounts you own or hashtag search after app review and business verification. TikTok's Research API is academic-only with a weeks-to-months approval. Facebook Page Public Content Access needs app review. Embedding individual posts via each platform's embed script is allowed but loads third-party trackers, which breaks the site's no-tracking promise, and embeds vanish when posts are deleted. Platform-provided RSS does not exist on any of them.

*Directory (S):* for every party and every MP/candidate, outbound links to official accounts (verified against the party website and parliament.nz), plus parliament.nz profile, party page, public email. Same fields for everyone, alphabetical, no follower counts (follower counts are a popularity cue). Add "Report a wrong link".

*Press-release feed (M):* a GitHub Action every 30–60 minutes fetches Scoop's Parliament section RSS (the feed that carries party and ministerial releases; verify the exact URL on scoop.co.nz) plus each party's own news-page RSS where one exists, normalises to `{party, title, date, url, 200-char excerpt}`, de-duplicates, and commits `releases.json`. Show headline, party, date and a link out; keep excerpts short (copyright and fairness). **Default view: the latest 3 per party, equal slots**, with a "chronological, all parties" tab second. Label clearly: "Party press releases — the party's own words, not fact-checked." Mark releases that make a checkable claim with a link to the matching promise or issue page where you have one.

**Bias flags:** volume (National and Labour will issue 5× the releases of smaller parties; the equal-slot default fixes it); ministerial releases are government, not party, and should be tagged as such; Scoop's inclusion criteria are not yours — some fringe parties may appear more often than their vote share; the "follow" directory must not include unofficial fan or attack accounts. **Effort: S + M.**

### R2.3.7 Shareable result cards

**Verdict:** yes (Round 1 M11); the design decisions are the whole point.

**Implementation on static:** render the card client-side on a `<canvas>` (or an inline SVG → canvas), `canvas.toBlob()` → `navigator.share({files:[...]})` on mobile (Web Share Level 2 is supported in Safari and Chrome Android), fallback to a download link. Open Graph images cannot be generated per result without a server; use one well-designed generic OG image for the quiz page and encourage sharing the PNG itself. Card content: the full 17-party bar distribution (not one party), bucketed strength (strong/moderate/weak), quiz version and date, "This is not a recommendation — see how it works at [URL]", and the result link (the hash-encoded one from R2.3.5). Optional "what I care about most" line from the importance weights. Offer the same renderer for swipe, compass, electorate watchlist, game scoreboard and election-night snapshots.

**Bias flags:** single-winner cards ("I'm 78% ACT!") are the bandwagon mechanism Vote Compass deliberately avoids; show the distribution. Party colours and logos on cards create visual dominance for parties with strong brands; use uniform bars with the party name. Never include the forecast on a card during voting. **Effort: S–M.**

## R2.4 Round 2 top-ten, in order

1. Voting plan builder (.ics + SMS + print) — S
2. Result cards with full distribution + hash-encoded share/export link (one build) — S–M
3. Geolocation → electorate with boundary-confidence warning; vote.nz handoff for voting places — M
4. "Today" panel: changes in 24h, events, policy of the day, poll watch — M
5. Press-release feed (Scoop + party RSS, equal slots) + social-link directory — M + S
6. "Listen" button and text-size control site-wide — S
7. Māori electorates hub and te reo toggle for the five critical paths — M
8. Samoan/Tongan how-to-vote + church/community printable — S–M
9. Election-night watch-party mode + electorate watchlist — M
10. Hot-seat party-guessing game with "same deck" link — M

Everything above sits inside the Round 1 constraints: hide persuasive tools under the election-day flag, show distributions not winners, publish sampling rules, and keep the only data you hold about a visitor inside their own browser.
