# Legal and compliance review — Ballot Book NZ (New Zealand law)

**Status:** review dated 23 October 2026, 15 days before polling day (Saturday 7 November 2026).
**Scope:** the public site at https://not-simon.github.io/Politicsnz/ and the open repository behind it.
**Owner of this file:** the compliance reviewer. Everything else in the repo is the maintainers' to change.

> **This is not legal advice.** It was prepared by a non-lawyer reviewer from the primary sources cited below
> (statute text on legislation.govt.nz as at 23 October 2026, the Electoral Commission's 2026 handbooks and
> guidance pages, and the published terms of the third-party sites used). It is a risk assessment to help the
> maintainers decide what to do; it is not a substitute for advice from a New Zealand lawyer, and the Electoral
> Commission offers free advisory opinions on whether something is an election advertisement. Where this review
> says "low risk" it means "a claim is unlikely and would probably fail", not "impossible".

---

## 1. Summary verdict

Ballot Book NZ is, in substance, a reference work: it describes what parties and candidates say and have done, applies
the same rules to all of them, and tells nobody how to vote. On the two statutes that bite hardest on election
websites, that matters:

- **Electoral Act 1993.** A non-partisan guide that does not "encourage or persuade voters to vote, or not to vote"
  for a party or candidate is not an *election advertisement* (s 3A(1)), so the promoter-statement (s 204F),
  authorisation (ss 204G–204H) and spending (s 204B) rules should not apply to the site as it stands. The parts
  that come closest to the line are the **quiz / compass / swipe results** (a tailored statement that the reader
  agrees most with party X) and the **seat forecast**. Those should be kept descriptive, all-party, and free of
  imperative language, and the Commission should be asked for a free advisory opinion this week. On **election day**,
  the law (s 197(1)(g)) and the Commission's 2026 guidance are clear enough: material placed on a website *before*
  polling day may stay up if it is only reached by people who go looking for it and the site is not promoted that
  day, but **nothing new may be published, and nothing may comment on who is likely to win**. The site's current
  00:00–19:00 blackout of quiz results, polls and forecast is the right idea but is **incomplete** (the home-page
  poll card, the "Battleground" electorate list, polling lines on party cards and the forecast prose in the
  Markdown pages are still visible) and is **undermined by the automated poll workflow**, which would publish fresh
  poll and forecast data on polling day. Both are fixable in an hour.

- **Copyright Act 1994.** The **biggest legal exposure on the site is the verbatim reproduction of 993 party
  documents in full.** New Zealand has no general "fair use"; the fair-dealing defences for criticism/review and
  news reporting (s 42) exist, but reproducing whole works as a standing archive, with the "review" being a short
  summary, is a weak fit, and research/private study (s 43) protects the *reader's* copying, not a publisher's.
  The practical risk is not a damages claim (a party suing a free, neutral voter guide mid-campaign would be a poor
  look and the loss is nil); it is a **takedown notice to GitHub**, which can disable the whole repository, and
  with it the whole site, in the final week. The pragmatic response is to (a) ask each party for permission now,
  (b) move the full texts into a separate repository/host so a notice cannot take the guide offline, (c) show
  excerpts by default with the full text one tap away, and (d) make the takedown promise visible on the site.
  Second on the list is the **~470 candidate photographs and questionnaire fields copied from policy.nz**, whose
  terms of service prohibit redistribution; that needs an email to Policy Ltd today and a plan B.

- **Defamation, privacy, harmful digital communications, trade marks, accessibility:** manageable with editorial
  rules the project has mostly adopted already. The specific fixes are listed below.

The licence of the repository also needs a correction: the MIT licence cannot cover text derived from Wikipedia
(CC BY-SA 4.0) or from NZHistory (CC BY-NC 3.0 NZ). A simple licence split is proposed.

---

## 2. Action list

Priorities: **MUST** = do before 7 November (legal exposure or a hard date); **SHOULD** = do during the campaign or
shortly after; **NOTE** = good practice / things to keep in mind.

### MUST (before 7 November)

| # | Action | Why | Where |
|---|---|---|---|
| M1 | **Freeze deployments from 23:59 Friday 6 Nov to 19:00 Saturday 7 Nov (NZDT).** Disable the `polls.yml` cron for that window (it runs every 6 hours, rebuilds `site/` and pushes new poll/forecast data), and do not merge anything that changes `site/` or `data/` until after 7pm. The only acceptable change on polling day is *removing* material. | Electoral Act s 197(1)(g) (publishing on polling day a statement likely to influence a vote; penalty up to $20,000). The website defence in s 197(2A) only covers material "placed on the web site before polling day". The Commission's 2026 Media Kit: "Election material posted on websites before election day can remain, but the material cannot be added to on election day". | `.github/workflows/polls.yml`, `pages.yml` |
| M2 | **Extend the election-day blackout** so that, from 00:00 to 19:00 on 7 Nov NZ time, the site shows no poll numbers, no seat projection, no "battleground"/"marginal" labels, no match/compass/swipe results, and no forecast prose. Today `blockedToday()` hides only the `match`, `compass`, `swipe`, `swipe-tally`, `polls`, `trends` views. Still visible: the home-page "The polls — Where things stand" card, the "Battleground" starter tiles on the electorate view, polling averages on party cards, and the poll/forecast sections of `REPORT.md`, `elections/2026.md` and `guide/parties.md` served through `pages.json`. Simplest: on election day render a reduced site (parties, policies, candidates, electorate, how to vote) and a single "hidden until 7pm" card for everything else. | The Commission's Publisher & Broadcaster Handbook 2026 (p 26) gives as examples of breaching election-day rules an item that "commented on a candidate's likelihood of winning an electorate seat" or "commented on each party's likelihood of passing the 5 percent party vote threshold". Quiz results computed on the day are *new* statements, not material "placed on the web site before polling day". | `site/index.html` (`blockedToday`, `V.home`, `V.electorate`, page rendering) |
| M3 | **No promotion of the site on polling day** by any contributor: no social posts, no "check your match before you vote" messages, no newsletter, no RSS/push. Say so in `CONTRIBUTING.md`. | s 197(2A)(c): the website defence is lost if the defendant "did, on polling day, distribute, broadcast, or exhibit ... or publish ... any material promoting or advertising the web site". The Commission: "no advertisements promoting the page or site are published on election day" and "you don't repost the material on election day". | `CONTRIBUTING.md` |
| M4 | **Ask the Electoral Commission for an advisory opinion** on (a) the match quiz / compass / policy-swipe result pages and (b) the seat forecast. Send the request today (it is free; "Request an advisory opinion" in the Publisher & Broadcaster Handbook, p 12; phone 0800 36 76 56 or the contact form on elections.nz). Attach screenshots of a result page. Until the answer arrives, apply M5. | If any element is an election advertisement it needs a promoter statement (s 204F; illegal practice), and a result that "encourages ... voters to vote for a party" would be a *party advertisement* needing the party secretary's written authorisation (s 204H), which is impractical across 17 parties. Getting the Commission's view removes the uncertainty. | — |
| M5 | **Keep the result pages descriptive.** Rank *all* parties, describe the output as agreement with stated policy positions ("your answers agreed most with…"), never as a recommendation; no "vote", "back", "support", "choose" verbs; no single-party badge, share image or copyable blurb that reads like an ad; keep the standing disclaimer on every result page (wording in §3.1.4). | Keeps the content outside s 3A(1) on the Commission's own test: content, style, apparent purpose, factual context and "effect as a whole" judged by a reasonable observer (*Electoral Commission v Watson* [2016] NZCA 512; Handbook p 7). | `site/index.html` match/compass/swipe renderers |
| M6 | **Publish a "Who we are / contact" box** on the About view and in the site footer with the project name, the name of a responsible person, and a working contact (email and the repository URL). Do not label it a "promoter statement" unless the Commission says the site needs one; the content satisfies s 204F(2)–(4) either way. Wording in §3.1.5. | s 204F(2) (name and contact details); s 204F(4) (unregistered group must name an authorised representative). A visible contact is also what the Defamation Act s 25 reply process, the Copyright takedown promise and the Privacy Act depend on. | `site/index.html` About view, footer; `README.md` |
| M7 | **Full-text party documents — reduce the blast radius now.** (a) Email every party secretary/communications lead with the short permission request in §3.2.6 and log replies in `NOTICE.md`. (b) Move `parties/*/policies/documents/` and `site/data/fulltext/*.json` into a **separate repository** (for example `Politicsnz-documents`) served from its own GitHub Pages URL, and load full texts from there. (c) Default the policy pages to an **excerpt** (the summary plus the relevant passage, ≤ ~300 words) with a "Show the party's full text" control and a prominent link to the original. (d) Put the takedown promise on the site, not just in `NOTICE.md`: wording in §3.2.7. (e) Record each party's own licence terms where they publish one (National's website states a CC BY licence according to the credit recorded in `person.json`; Beehive releases are Crown copyright and most NZ government sites license content CC BY 4.0 — verify the footer of beehive.govt.nz and record it). | Copyright Act s 29 (copying the whole or a substantial part); s 42 fair dealing is purpose-limited and "fairness" weighs amount copied; s 43 is for the reader's own research/private study (one copy, s 43(4)). GitHub's DMCA policy: "If the notice alleges that the entire contents of a repository infringe ... GitHub will ... disable the entire repository". A separated document store means a takedown costs one party's texts, not the voter guide. | `parties/*/policies/documents/`, `site/data/fulltext/`, `tools/build_site.py`, `NOTICE.md` |
| M8 | **policy.nz material (≈470 photos, 511 questionnaire blocks).** Email contact@policy.nz today: disclose the use (non-commercial voter information, with attribution and link), ask for permission or a no-fee licence, and offer to remove on request. In parallel: (a) replace policy.nz photos where a Wikimedia Commons, Parliament or party-site image with a stated licence exists; (b) stop displaying candidates' **"Residence"** and any **personal-domain email** (26 of 271 are gmail/hotmail/outlook etc.) — see P1; (c) if Policy Ltd declines, remove the photos and questionnaire text within 24 hours and link to policy.nz instead. | policy.nz Terms of service: "You may use this website for your personal, non-commercial, non-professional use only ... You may not redistribute or produce derivative works based on the contents of this website without the permission of Policy Limited." Copyright in a commissioned photograph vests in the commissioner under the Copyright Act s 21(3), so the owner is usually the party/candidate, not policy.nz, but the contractual restriction on redistribution is Policy Ltd's and they run a commercial licensing business. | `parties/*/people/*/person.json`, `tools/people_*`, `NOTICE.md` |
| M9 | **Fix the licence split.** Keep MIT for code (`tools/`, `site/` source). License the project's own text and data under **CC BY-SA 4.0** (compatible with the Wikipedia-derived biographies and election tables, which *must* stay CC BY-SA 4.0). Mark NZHistory-derived content, if any is added, CC BY-NC 3.0 NZ. Update `LICENSE` footer, `README.md`, `NOTICE.md` and the site's Licences card. Add a per-page line on person profiles: "Biography adapted from Wikipedia, "<article>", licensed CC BY-SA 4.0 (retrieved <date>)". | CC BY-SA 4.0 §3(b) (ShareAlike): adaptations must be licensed under the same or a compatible licence; MIT is not. Wikimedia Terms of Use §7: attribution by hyperlink to the article satisfies the attribution condition. | `LICENSE`, `README.md`, `NOTICE.md`, `tools/people_render*` |
| M10 | **Privacy statement + geolocation consent text** on the About view and linked from the footer and from the "find my electorate" control (wording in §3.4.4). Confirm the geolocation lookup never leaves the browser (it does today: `locateElectorate()` tests coordinates against local GeoJSON). | Privacy Act 2020 IPP 3 (make people aware of collection and purpose); the Commission and public expect it; geolocation is sensitive. | `site/index.html` |
| M11 | **Controversies and "critics say": apply the five rules** in §3.3.3 to every entry before election day, in order of audience: party cards first, then current candidates, then former MPs. Remove any entry that cannot meet them. Put the right-of-reply / correction route on every profile page. | Defamation Act 1992 ss 8–12 (truth, honest opinion), ss 16–19 and Sch 1 (qualified privilege for fair and accurate reports), s 25 (retraction or reply within 5 working days of a request). *Lange v Atkinson* [2000] 3 NZLR 385 (CA); *Durie v Gardiner* [2018] NZCA 278. | `parties/*/people/*/README.md`, `data/guide/parties.json` |

### SHOULD (during the campaign / soon after)

| # | Action | Why |
|---|---|---|
| S1 | Self-host the four Google Fonts and the two cdnjs libraries (marked, DOMPurify) or declare them in the privacy statement. | Each third-party request sends the visitor's IP address to Google/Cloudflare. The current "no tracking" claim is true for the project but the statement should be accurate about third parties. |
| S2 | Show photo credits and licences **on the person page** (caption or "Photo: <author>, <licence link>, via Wikimedia Commons; cropped"), not only in `person.json`. | CC BY / CC BY-SA 2.0–4.0 require attribution, a licence notice and an indication of changes *with* the copy. Commons guidance: credit the creator (the "author" field), not the uploader. |
| S3 | Use Stats NZ's template attribution for *adapted* content (the boundaries are simplified): "This work is based on/includes Stats NZ's data which are licensed by Stats NZ for reuse under the Creative Commons Attribution 4.0 International licence." Write "Stats NZ" in words, not the logo; keep "simplified for web display". | Stats NZ copyright page (separate templates for content reused as-is and for adapted content); CC BY 4.0 §3(a)(1)(B) (indicate modifications). |
| S4 | Add a 5-working-day **reply/correction** paragraph to `EDITORIAL_STANDARDS.md` and to each profile page: who to contact, what will be published, how fast. | Defamation Act s 25 requests must be made within 5 working days of the person becoming aware; a visible route makes an early, cheap settlement likely and is strong mitigation (s 29). |
| S5 | Decide and publish **inclusion criteria for "Controversies"** (on the public record in ≥2 reputable sources or an official record; relevant to fitness for public office; outcome stated; subject's response included). Rename the heading to something descriptive and neutral, e.g. "On the record" or "Disputes and criticism", or keep "Controversies" but apply the criteria. | Honest-opinion and qualified-privilege defences depend on accuracy and fairness of the underlying facts; a published standard is evidence of responsible communication (*Durie*). |
| S6 | Add a **name-suppression check** step before adding any court-related item to a profile. | Defamation Act s 17 (no privilege where publication is prohibited by law); Criminal Procedure Act 2011 s 211 (breach of suppression is an offence). |
| S7 | Re-point the site at the separated document store (M7) **and** add `rel="nofollow noopener"` plus the original URL beside every full text. Keep the per-document front matter (source URL, retrieval date, method). | Supports the fair-dealing "sufficient acknowledgement" requirement (s 42(1)) and the implied-licence argument for press releases. |
| S8 | For Scoop-sourced party releases, record in the front matter that the text is the **party's** release republished by Scoop; cite the party as the copyright owner and Scoop as the mirror. For the planned RSS feed (§3.8.3) show **headline + date + link only**. | Scoop's terms claim copyright "in all content as it is published on scoop.co.nz" and define "commercial users" to include organisations "whether for profit or not for profit"; the party's text is the party's, but harvesting Scoop pages at scale is what the terms target. |
| S9 | Replace the candidates' `Residence` field with the electorate/region, and drop ages for people who are not standing in 2026 unless the date of birth comes from Wikipedia/Parliament. | Privacy Act IPP 11(1)(d): disclosure from a publicly available publication is permitted only where "it would not be unfair or unreasonable". Residence-level detail of politicians has a safety dimension and adds nothing to the voter's decision. |
| S10 | Put a one-line **"not the Electoral Commission"** disclaimer under the site title on the home view and on the electorate view (wording in §3.6.3), and keep all official instructions as links to vote.nz. | Avoids any confusion with official voting information, which the Commission asks the public to verify against vote.nz/elections.nz. |
| S11 | Consider forming an **incorporated society or charitable trust** to hold the project after the election. | Today "Ballot Book NZ contributors" is an unincorporated group; defamation and copyright liability sits with the individuals who publish. Not urgent for 7 Nov. |
| S12 | Publish a short **accessibility statement** and run an automated WCAG 2.2 AA pass (axe/Lighthouse) on the quiz, map and seat views. | Not legally mandated for a private site; the NZ Government Web Accessibility Standard 1.2 (WCAG 2.2 AA) is the local benchmark; Human Rights Act s 44 (services to the public) is untested against websites in NZ. |

### NOTE (keep in mind)

| # | Note |
|---|---|
| N1 | **Opinion polls.** NZ has no general ban on publishing opinion polls, and nothing in the Electoral Act stops the site from republishing published polls during the campaign. The restrictions are on *conducting* polls: s 197(1)(d) (at any time before close of poll, a poll of persons voting before polling day) and s 197(1)(e) (any poll on polling day). So: never add a "who will you vote for?" or "have you voted / who for?" question, and never publish an aggregate of users' quiz results as a "poll"; the site's no-server design already prevents this. On polling day, previously published polls are covered by s 197(2A) if unchanged, but publishing a *new* poll or forecast before 7pm would be a plain s 197(1)(g) breach, hence M1–M2. |
| N2 | **Broadcasting Act 1989 ss 69–70** (election programmes) apply to *broadcasters*; the Act's definition of broadcasting excludes transmissions "on the demand of a particular person", and the Commission's handbook deals with election programmes only for TV/radio and broadcasters' on-demand platforms. A website is governed by the Electoral Act, not the Broadcasting Act. The BSA Election Programmes Code does not apply. The ASA codes apply only to *advertising* the site might run; the Media Council only to its members. |
| N3 | **Regulated period and spending.** The regulated period for 2026 is 7 August – 6 November. An unregistered third-party promoter may spend up to $17,000 (incl. GST) on election advertising in that period; registration is required above that; the registered cap is $424,000. Volunteer labour is excluded from "advertising expenses" (s 3E(1)(b)(iii)); hosting on GitHub Pages is free. Even on the most adverse reading of the quiz pages, the site is nowhere near a registration threshold; the live questions are only the promoter statement (M6) and authorisation (M4). |
| N4 | **Election Amendment Act 2025 changes that touch this site:** enrolment closed 25 October (13 days before election day; no election-day enrolment); advance voting fixed at 12 days (26 Oct – 6 Nov); promoter statements may now give an email, phone, PO Box or a link to a page with contact details instead of a street address (s 204F(2) as amended from 1 Jan 2026); spending limits are inflation-indexed; new offence of providing free food, drink or entertainment within 100 m of a voting place; bribery/treating/undue influence extended to enrolment. The site's key-dates text already reflects the enrolment change. |
| N5 | **Imitation ballot papers.** s 197(1)(f) prohibits, on polling day and the 3 days before, distributing anything "purporting to be in imitation of any ballot paper" with candidate/party names and any voting direction. Candidate lists per electorate are fine as information, but do not add a printable "your ballot" or tick-box mock-up, and keep the electorate pages free of any indication of who to vote for. |
| N6 | **Party logos and colours.** The site uses party colours and names but no party logos (checked: only the site's own logo). Names used descriptively are not use "in the course of trade" (Trade Marks Act 2002 s 89) and the Fair Trading Act applies only "in trade"; passing off needs a misrepresentation in trade. If logos are ever added, use them small, for identification only, unaltered, with "Party names and logos are the trade marks of their owners". On polling day, logos and slogans are specifically listed in s 197(1)(g)(iii); colours alone are not (only "ribbons, streamers, rosettes" in party colours are, and those are exempted when worn). Pre-existing coloured charts are covered by s 197(2A). |
| N7 | **"Ballot Book".** A quick search found no New Zealand product or registered mark of that name; do an IPONZ trade mark search to be sure. Avoid any styling that resembles the Electoral Commission's orange "Vote" branding. |
| N8 | **Human Rights Act 1993 s 61** (racial disharmony) can be engaged by *republishing* threatening, abusive or insulting material likely to excite hostility on racial/ethnic grounds; the s 61(2) reporting defence is drafted for newspapers/periodicals/broadcasters. If a party document plainly falls in that category, link to it rather than reproduce it. |
| N9 | **Harmful Digital Communications Act 2015.** There is no user-generated content on the site (confirmed: no comments, forms, server or analytics; GitHub Issues/PRs are hosted by GitHub). Nothing to do now. If any feature lets one person's input be shown to another (names on a leaderboard, free text in a game, an aggregated feed), set up the s 24 complaints/take-down process for an "online content host" and avoid Principle 1 (sensitive personal facts) and Principle 6 (false allegations) problems by not publishing free text at all. |
| N10 | **Children.** The site collects nothing, so there is no age-gating obligation. If a feature ever collects data (even an email for a newsletter), take extra care with under-16s (OPC guidance on children's privacy) and prefer not to. |
| N11 | **Clock-dependence of the blackout.** `electionPhase()` uses the visitor's device clock converted to Pacific/Auckland time. A visitor with a wrong clock could see hidden material; a static site cannot prevent this. Pre-rendering a reduced site for election day (M2) removes the dependence entirely. |
| N12 | **Jurisdiction.** Hosting on GitHub Pages (US) does not change the analysis: the promoter and the audience are in New Zealand, and the Commission states the rules apply to election advertisements published in New Zealand regardless of where the promoter is, and to those published overseas if the promoter is in New Zealand. |

---

## 3. Analysis by topic

### 3.1 Electoral Act 1993

#### 3.1.1 Is the guide an "election advertisement"?

Section 3A(1) defines an election advertisement as "an advertisement in any medium that may reasonably be regarded as
encouraging or persuading voters to do either or both of the following: (i) to vote, or not to vote, for a type of
candidate described or indicated by reference to views or positions that are, or are not, held or taken ...; (ii) to
vote, or not to vote, for a type of party described or indicated by reference to views or positions ..."; it includes
candidate and party advertisements. Section 3A(2) excludes, among other things, "(c) the editorial content of — (i) a
periodical: (ii) a radio or television programme: (iii) a publication on a news media Internet site" and "(e) any
publication on the Internet, or other electronic medium, of personal political views by an individual who does not
make or receive a payment in respect of the publication of those views."

The Commission's test (Publisher & Broadcaster Handbook 2026, pp 7–8; Third Party Handbook 2026, pp 18–19): whether an
advertisement encourages or persuades "depends on its content, style, apparent purpose, factual context, effect as a
whole", assessed "from the perspective of a reasonable observer, recognising the importance and value of political
speech in a democracy (*The Electoral Commission v Watson & Anor* 2016)". "Unpaid advertising can still be an election
advertisement." "Matters such as size, frequency, scale, and proximity to the election are relevant."

Applied to Ballot Book:

- **Party pages, policy lists, full texts, people profiles, electorate pages, election history, track records,
  issue explainers:** descriptive reference material applying one template to every party. A reasonable observer would
  not regard it as encouraging a vote for or against anyone. Not an election advertisement.
- **Track records ("kept / broken")** and **"critics say"**: evaluative, but balanced across parties and sourced; the
  format is a report card, not a call to action. Low risk, provided the same rubric is visibly applied to all.
- **Match quiz, political compass, policy swipe tally:** the output is a statement generated for one reader: "you agree
  most with party X". Arguments that it is *not* an election advertisement: it ranks every party; it is driven by the
  reader's own answers; it states agreement with policy positions, not a recommendation; it carries a disclaimer;
  comparable tools (TVNZ's Vote Compass, policy.nz) have run in NZ elections. Arguments the other way: it is tailored,
  it names parties, and a result card is easy to read as "this is your party". This is the element to put to the
  Commission (M4) and to keep descriptive (M5). Note that the *personal political views* exemption in s 3A(2)(e) is
  unlikely to help: the Third Party Handbook (p 19) says the exemption "doesn't apply if you're using a website ...
  to express political views on behalf of a group", and the project presents itself as a group ("contributors").
  The *editorial content* exemption in s 3A(2)(c)(iii) requires a "news media Internet site" (in practice, Media
  Council or BSA oversight); Ballot Book is not one.
- **Seat forecast / coalition builder / MMP calculator:** arithmetic on published polls. Not advocacy, but the Commission
  treats commentary on parties' chances as influence on *polling day* (see 3.1.3). Before polling day it is permitted.

**Consequences if an element were an election advertisement:** it would need a promoter statement (s 204F; wilful
breach is an illegal practice; the Commission cites fines up to $40,000 for promoters and $10,000 for publishers); a
*party advertisement* "that may reasonably be regarded as encouraging or persuading voters to vote for a party" needs
the party secretary's written authorisation (s 204H); and advertising expenses in the regulated period count against
the $17,000 unregistered cap (s 204B(1)(d)). The spending issue is theoretical here (free hosting, volunteer labour
excluded by s 3E(1)(b)(iii)). The authorisation issue is why the quiz must stay on the right side of the line: nobody
can obtain 17 party secretaries' consents for an algorithmic result.

**Advertising that links to the site.** If the project ever buys or posts promotion ("Find your match at ..."), the
Handbook (p 9) says the content of the linked site helps decide whether the promotion is an election advertisement, so
the same analysis applies to the promotion.

#### 3.1.2 Promoter statement — needed or not?

Not required unless the Commission concludes some element is an election advertisement. The content requirement is
light since 1 January 2026 (s 204F(2) as amended: "name and contact details"; s 204F(4): an unregistered body must also
name "a member of the body who is the duly authorised representative"), and the Third Party Handbook (p 27) says that on
a website with many pages the statement can go on the home page. Recommendation (M6): publish the same information as a
"Who we are / contact" box so that the requirement is met in substance whatever the characterisation, and label it a
promoter statement only if the Commission advises that one is required.

#### 3.1.3 Election day (Saturday 7 November 2026, 00:00–19:00 NZDT)

Section 197(1)(g) makes it an offence (fine up to $20,000) "at any time on polling day before the close of the poll" to
exhibit in a public place, publish, distribute or broadcast "(i) any statement advising or intended or likely to
influence any elector as to the candidate or party for whom the elector should or should not vote; (ii) any statement
... likely to influence any elector to abstain from voting; (iii) any party name, emblem, slogan, or logo; or (iv) any
ribbons, streamers, rosettes ... in party colours", with provisos for newspapers published before 6 pm the day before,
fixed signage at party headquarters, and *news* in newspapers, periodicals and broadcasts (not websites generally).

**The website defence, s 197(2A):** it is a defence to a (1)(g) charge relating to "publication on an Internet web
site" if the defendant proves that "(a) the statement or material was placed on the web site before polling day; and
(b) the defendant did not operate or permit the operation of systems that cause the statement or material on the web
site to be made available, on polling day, to persons other than persons who voluntarily access the web site; and (c)
the defendant did not, on polling day, distribute, broadcast, or exhibit in or in view of a public place, or publish ...
any material promoting or advertising the web site."

**Commission guidance for 2026** (Publisher & Broadcaster Handbook pp 26–27; Media Kit pp 22, 25; Social media page):

- "On election day, you can't publish or broadcast anything that is likely to influence voters until after voting
  closes at 7pm." "You could still be seen as encouraging or persuading voters even if your item is balanced ..., you
  do not mention the name of a party or candidate, [or] you give all candidates or parties equal coverage."
- Examples of breaches: an item that "commented on a candidate's likelihood of winning an electorate seat" or
  "commented on each party's likelihood of passing the 5 percent party vote threshold".
- "You can keep existing election material on your website or social media page, so long as ... you published the
  material before election day; the material is only available to people who voluntarily access it; you don't publish
  advertisements promoting the page or site on election day; you don't repost the material on election day."
- "Election material posted on websites before election day can remain, but the material cannot be added to on
  election day, and the website cannot be advertised on election day." Parties and third parties must "not post any
  new material on websites."
- "We recommend you disable the public message boards and comment sections of your websites and social media on
  election day." (Not applicable: there are none.)
- "The election day rules make no exemption for the expression of personal political views online."
- Permitted: noting that it is election day, when results will be available, how and where to vote; party and candidate
  *names* in news; reminders to vote.

**Application to the site's current blackout.** Hiding `match`, `compass`, `swipe`, `swipe-tally`, `polls` and `trends`
from 00:00 to 19:00 is well judged: quiz results are generated on the day (so not clearly "placed on the web site before
polling day"), and polls/forecasts are exactly the "likelihood" commentary the Commission flags. It is **not
sufficient** as implemented, because (i) the home view still renders the "Where things stand" poll-average card, (ii)
the electorate view's "Battleground" tiles label marginal seats, (iii) party cards carry polling averages, (iv) the
Markdown pages (`REPORT.md`, `elections/2026.md`, `guide/parties.md`) contain poll averages and seat scenarios, and (v)
`polls.yml` would publish *new* poll and forecast data during the day, which is both a new statement under
s 197(1)(g) and a loss of the s 197(2A)(a) defence for that material. Fix: M1 and M2.

Is the blackout **necessary** for pre-existing, unchanged content? Strictly, the s 197(2A) defence would be available
for untouched content on a frozen, unpromoted site. But the defence is a defence (the burden is on the publisher), the
Commission's guidance treats "likelihood of winning" content as influence, and the cost of hiding it for 19 hours is
nil. Keep the blackout and widen it. Everything factual (parties, policies, candidates, electorates, how to vote) can
and should stay available all day.

**Party names and colours on polling day.** s 197(1)(g)(iii) lists "any party name, emblem, slogan, or logo". The site
displays party names everywhere; this is unavoidable for a reference work and is covered by s 197(2A) for pre-existing
pages. Do not add party logos before the election (N6).

#### 3.1.4 Standing disclaimer for result pages (quiz, compass, swipe)

> *This shows how closely your answers line up with each party's published positions on the questions you answered.
> It is information, not advice: it does not take account of candidates, coalitions, trust, or the issues we did not
> ask about, and it is not a recommendation about how to vote. Every party is listed. Read the party pages and the
> original policy texts before deciding. Ballot Book NZ is independent and not affiliated with any party, candidate or
> the Electoral Commission.*

#### 3.1.5 "Who we are / contact" box (satisfies s 204F content if ever required)

> **Ballot Book NZ** is published by an unincorporated group of volunteers. Responsible person: *[full name]*.
> Contact: *[email address]* · https://github.com/not-simon/Politicsnz. We are not affiliated with any political
> party, candidate or the Electoral Commission. Official information about enrolling and voting is at vote.nz.

If the Commission advises that an element is an election advertisement, prefix the box with its recommended form:
"Promoted by Ballot Book NZ, authorised representative *[full name]*, *[email]*."

#### 3.1.6 Opinion polls generally

See N1. There is no NZ restriction on *publishing* polls at any time other than polling day's general rule. The RANZ
Political Polling Code governs pollsters, not republishers; attributing each poll to the pollster, with fieldwork dates
and sample size, is good practice and is already the site's convention.

#### 3.1.7 Electoral Amendment Act 2025

Royal assent 19 December 2025; most provisions in force 20 December 2025, advertising/promoter provisions 1 January 2026
(Ministry of Justice summary). Relevant changes are listed in N4. Note s 204B(1)(d) now refers to "the amount published
on the Electoral Commission's internet site under section 266A" ($17,000 incl. GST for 2026) and s 204F(2)–(3) were
amended to allow contact details other than a street address.

#### 3.1.8 Broadcasting Act 1989

See N2. Not applicable to a website.

### 3.2 Copyright Act 1994

#### 3.2.1 The full-text party documents (the biggest risk)

**What the law says.** Copyright in a literary work (a manifesto, policy page or press release) is infringed by copying
"the work as a whole or any substantial part of it" without licence (s 29). The relevant permitted acts are:

- **s 42(1)** — "Fair dealing with a work for the purposes of criticism or review, of that or another work ... does not
  infringe copyright in the work if such fair dealing is accompanied by a sufficient acknowledgement."
- **s 42(3)** — "Fair dealing with a work (other than a photograph) for the purposes of reporting current events by any
  means ... does not infringe copyright in the work if such fair dealing is accompanied by a sufficient acknowledgement."
- **s 43(1)** — fair dealing "for the purposes of research or private study"; s 43(3) lists the fairness factors
  (purpose; nature of the work; whether it could be obtained within a reasonable time at an ordinary commercial price;
  effect on the potential market or value; amount and substantiality of the part copied); s 43(4) limits it to one copy.

There is no general fair-use defence, no "archive" or "public interest" exception for publishers, and no exception for
political speech. Crown copyright works (Beehive releases) are protected like any other (s 26), though s 27 removes
copyright from Bills, Acts, regulations, Hansard, select committee reports and judgments, and most government websites
license their content CC BY 4.0 under NZGOAL.

**How the defences fit.** Research/private study (s 43) protects what a *reader* does, not a site that distributes
copies to the public. Criticism/review and news reporting (s 42) are real candidates: the site summarises each
document, tags it, cross-references it and holds parties to it; publishing what parties said during a campaign is
reporting current events. The weakness is the fit between purpose and quantity. Fair dealing is assessed by reference
to what the purpose *needs*; a review that reproduces the whole of 993 documents, with a short summary each, looks
like an archive with reviews attached rather than reviews that quote. Factors in the site's favour: the works are free,
published to be read as widely as possible, and have no market the copy displaces; the reproduction is attributed and
linked; the purpose is public-interest reference; several parties block automated access and change their pages, so
the public record argument is genuine. Factors against: whole-work copying; a standing archive rather than a
time-limited report; and the fact that the summary, not the full text, does the "reviewing". The press releases are the
strongest case (they are issued to be republished and Scoop republishes them verbatim as a matter of course, which
supports an **implied licence**); manifestos and policy PDFs are the weakest.

**Practical risk.** A party is unlikely to sue a free, neutral voter guide during a campaign: the optics are bad, the
damages are nil, and an injunction would take weeks. The realistic risk is a **copyright notice to GitHub**. GitHub's
DMCA Takedown Policy says that where a notice "alleges that the entire contents of a repository infringe ... GitHub will
skip ahead and disable the entire repository"; otherwise the repository owner gets roughly one business day to remove
the identified content. A notice from one party could therefore take the entire site offline in the last week, and a
counter-notice takes 10–14 business days to restore access. That is the exposure to manage.

**Options, from most to least protective:**

1. **Permission.** Email every party (template in 3.2.6). A yes converts the risk to zero for that party and should be
   recorded in `NOTICE.md` with the date. A no means remove that party's full texts and keep summaries plus links.
2. **Separate the store.** Put the full texts in their own repository and Pages site; the main site fetches them on
   demand. A notice then disables the documents, not the guide. Do this regardless of the answers to (1).
3. **Excerpt by default.** Show the summary and the relevant passage (≤ ~300 words) with the full text behind a control
   and the original linked first. This does not change the legal analysis (the full text is still reproduced) but it
   reduces the prominence and substitution effect that a fairness assessment weighs, and makes the "review" character
   visible.
4. **Visible notice-and-takedown** (3.2.7) with a 24-hour commitment, and actually honouring it.
5. **Record licences.** Where a party or the Crown publishes under CC BY (National's site is recorded as doing so;
   check beehive.govt.nz's footer), the reproduction is licensed and the attribution should say so.

Notice-and-takedown does **not** give the project a statutory safe harbour: ss 92B–92C protect an *Internet service
provider* storing material "provided by a user of the service", and here the project is the author of the upload.
GitHub has its own safe harbour; the project does not. The value of the notice is practical (parties contact you
rather than GitHub) and evidential (fairness, good faith, mitigation).

#### 3.2.2 Candidate photographs and questionnaire text from policy.nz

Copyright in a commissioned photograph belongs to the person who commissioned and paid for it (s 21(3)), so the owner
of a candidate headshot is usually the party or candidate, not policy.nz; a photographer who was not commissioned
keeps copyright. Identification use of a publicity headshot is low copyright risk and arguably impliedly licensed
(publicity photos exist to be used), but there is no express licence and `person.json` correctly records "Not stated".

The sharper issue is **policy.nz's terms of service**: "You may use this website for your personal, non-commercial,
non-professional use only ... You may not redistribute or produce derivative works based on the contents of this
website without the permission of Policy Limited. ... You can get a license to use content from this website for
commercial and professional purposes ... by emailing contact@policy.nz." Copying ~470 photos and 511 questionnaire
blocks into a public repository is redistribution. Policy Ltd runs a licensing business and has an interest in
enforcing this. Action: M8. If permission is refused, remove the policy.nz-sourced photos and questionnaire fields
within 24 hours and link to the candidate's policy.nz page instead; the candidates' own party pages and Parliament
pages are alternative photo sources (Parliament's MP photos are generally CC BY 4.0; check each).

#### 3.2.3 Wikipedia-derived text — licence split

Wikipedia text is licensed CC BY-SA 4.0 (and GFDL). Reuse requires attribution (a hyperlink to the article satisfies the
Wikimedia Terms of Use), a licence notice, and **ShareAlike**: any adaptation must be released under CC BY-SA 4.0 or a
compatible licence. The repository's MIT licence footer says MIT covers "the original analysis written for this
project (REPORT.md, guide/, track records, profiles)" — but the profiles' biographies and the election tables derive from
Wikipedia, so MIT cannot apply to them. Recommended split (M9):

- **Code** (`tools/`, `site/` source): MIT.
- **Project text and data** (REPORT, guide, profiles, track records, elections, `data/`): **CC BY-SA 4.0**. This is
  compatible with incorporating Wikipedia text and is a normal licence for open civic data. (If the maintainers would
  prefer CC BY 4.0 for their *original* material, they must then keep Wikipedia-derived passages separately marked
  CC BY-SA 4.0; a single CC BY-SA is simpler and defensible.)
- **Third-party material** (party documents, photos, Stats NZ, NZHistory, pollsters): as stated per item in `NOTICE.md`.

Add the per-page attribution line in M9. Facts (dates, votes, results) are not copyright and may be reused without
attribution; the attribution is for the prose and the compilation.

#### 3.2.4 Wikimedia Commons photographs

306 photos carry a recorded licence (CC BY-SA 4.0/3.0/2.0, CC BY 4.0/3.0 NZ/2.0). All require, alongside the copy: the
creator's name (the "author" field on the Commons file page, not the uploader), the licence name with a link, a link to
the source, and an indication of changes ("cropped, resized"). Today this lives in `person.json` and `NOTICE.md`; it
should be visible on the person page (S2). Some Commons files are flagged "VRT pending" ("uploader will deal with
VRT"): treat those as unverified and prefer another image.

#### 3.2.5 Stats NZ, Scoop, RSS, critics' quotes

- **Stats NZ** boundaries: CC BY 4.0. Because the polygons are simplified, use Stats NZ's adapted-content template:
  "This work is based on/includes Stats NZ's data which are licensed by Stats NZ for reuse under the Creative Commons
  Attribution 4.0 International licence" (the "Source: Stats NZ and licensed by Stats NZ for reuse under…" form is for
  content reused unchanged), and keep "simplified" (S3). The current attribution is substantively compliant.
- **Scoop**: terms claim copyright "in all content as it is published on scoop.co.nz", permit personal, non-commercial
  reproduction with attribution, and treat organisations "whether for profit or not for profit" using content "in any
  professional capacity" as commercial users needing a licence. The party releases are the party's copyright, so the
  copyright question is the party's (strong implied licence for press releases); the Scoop terms are a contract/ToS
  question with modest practical risk for ~a dozen mirrored releases, but they clearly target automated harvesting, so
  the planned **RSS feed** should be headlines, dates and links only (S8), with "via Scoop" attribution. A client-side
  fetch of Scoop's RSS will also hit CORS; running a proxy that re-serves Scoop content is the "harvesting" the terms
  prohibit.
- **Critics' quotes**: a sentence or two, attributed, dated and linked, is fair dealing for criticism/review or news
  reporting (s 42) and in most cases not a "substantial part". Keep quotes short and never alter them.

#### 3.2.6 Permission request to parties (email template)

> Subject: Ballot Book NZ — permission to reproduce your published policy documents
>
> Kia ora, I help run Ballot Book NZ (https://not-simon.github.io/Politicsnz/), a free, non-partisan voter guide for the
> 7 November election. For reference we reproduce, verbatim and with a link to the original, the policy pages, PDFs and
> press releases your party has published, alongside neutral summaries; every party is treated the same way. Could you
> confirm that *[party]* is happy for its published policy documents to be reproduced in this way (attributed, unaltered,
> non-commercial), or tell us if you would prefer we show excerpts and link to you instead? If you ever want anything
> removed or corrected, email *[address]* and it will be done within 24 hours. Ngā mihi, *[name]*.

#### 3.2.7 Takedown / correction notice for the site

> **Third-party material.** Party documents, photographs and other material on this site belong to their owners and
> are reproduced for public reference with attribution and a link to the original. If you own something here and want
> it removed, corrected or attributed differently, email *[address]* or open an issue; we act within 24 hours during
> the campaign. See the full attribution notice.

### 3.3 Defamation Act 1992 — "Controversies" and "critics say"

#### 3.3.1 Exposure

291 profile READMEs contain a "Controversies" heading and every party card has a "critics say" quote. Repeating a
defamatory allegation is itself publication: "X said Y is corrupt" is actionable against the repeater unless a defence
applies. The defences that matter:

- **Truth** (s 8): the imputations were true or "not materially different from the truth"; taken as a whole, "in
  substance true".
- **Honest opinion** (ss 9–12): the statement is recognisable as opinion, based on facts stated or generally known
  and proved true (s 11). For another person's opinion that the site quotes, s 10(2)(b) requires that the opinion "did
  not purport to be the opinion of the defendant" and that the defendant "had no reasonable cause to believe that the
  opinion was not the genuine opinion of the author". Hence: attribute, quote, do not adopt.
- **Qualified privilege** (ss 16–19, Schedule 1): fair and accurate reports of proceedings in Parliament, of courts,
  and (Part 2, subject to s 18's duty to publish a reasonable explanation or contradiction on request) of public
  meetings, press conferences and official statements. Lost if "predominantly motivated by ill will" or the occasion is
  misused (s 19). *Lange v Atkinson* [2000] 3 NZLR 385 (CA) recognised a privilege for statements about the actions and
  qualities of those seeking or holding elected office; *Durie v Gardiner* [2018] NZCA 278 reframed it as a general
  **public interest / responsible communication** defence: the matter must be of public interest and the communication
  responsible (verification, reliability of sources, seeking comment, tone, urgency). A published editorial standard and
  a correction process are evidence of responsible communication.
- **Innocent dissemination** (s 21) does not help an author/publisher.

#### 3.3.2 Remedies and process

Section 25: a person defamed "in a news medium" may, within 5 working days of becoming aware, request a retraction or a
reasonable reply with similar prominence; agreeing to publish one carries costs consequences but typically ends the
matter. Section 26: a court may recommend a correction; publishing it ends the proceedings with costs only. A visible,
fast correction route is therefore both an editorial virtue and a legal shield (S4).

#### 3.3.3 Five practical rules for every controversy entry and critic quote

1. **Report the dispute, not the allegation.** Say who alleged what, when, in what forum, and what happened next
   (investigation, finding, apology, resignation, dismissal of complaint, court outcome). Never state a contested
   allegation as fact.
2. **Attribute, date, link.** Named person or organisation, date, link to a primary record (Hansard, court judgment,
   official report) or to at least two reputable news reports.
3. **Include the response.** The subject's denial, explanation or apology, in their words, with a link.
4. **No adjectives, no adopted labels.** Describe; do not characterise ("misleading", "corrupt", "racist" only inside a
   quotation with attribution). The editorial standards' banned-words list applies.
5. **Right of reply on the page.** Every profile links to the correction route and says replies are published with
   similar prominence within 24 hours during the campaign.

Also: observe court name suppression (S6); keep historic items only where an outcome exists and the matter bears on
public office; prefer Hansard and court records (privileged) over social media (not).

### 3.4 Privacy Act 2020

#### 3.4.1 Does it apply?

Yes. An "agency" is any person or body of persons (public or private), and the exemption for an individual's "personal
or domestic affairs" (s 27) does not cover publishing a website. The news-entity carve-out applies only to entities
subject to the BSA, the Media Council or an equivalent regulator; Ballot Book is not one.

#### 3.4.2 Republishing politicians' personal information

- **Collection** from policy.nz, Parliament and Wikipedia rather than from the individual is permitted where "the
  information is publicly available information" (IPP 2(2)(d)), meaning information "contained in a publicly available
  publication ... generally available to members of the public free of charge or on payment of a fee" (s 7). Those
  sources qualify. IPP 3A (indirect-collection notice, in force 1 May 2026) does not require notice where the agency believes on
  reasonable grounds "that the information is publicly available information" (IPP 3A(4)(b)) or that compliance "is not
  reasonably practicable" (IPP 3A(4)(e)); record that reliance in the privacy statement.
- **Disclosure** on the site is permitted where "the source of the information is a publicly available publication and
  ..., in the circumstances of the case, it would not be unfair or unreasonable to disclose the information" (IPP
  11(1)(d)). The fairness proviso is the live test:
  - Name, party, electorate, list rank, roles, parliamentary record, conscience votes, dates of birth from Wikipedia or
    Parliament: fair; central to the purpose.
  - **Age and "Before politics"** supplied by candidates to policy.nz for publication: fair, low sensitivity.
  - **"Residence" (suburb)**: supplied for publication, but politicians face real harassment risks and the field adds
    nothing to the voter's decision; replace with electorate/region (S9).
  - **"Public email"**: 245 are party/organisational addresses (fair; that is what they are for); 26 are personal
    gmail/hotmail/outlook addresses. Candidates chose to publish them, but republication in an open repository enables
    harvesting. Remove personal-domain addresses or replace with a link to the party/candidate page (M8(b)); render the
    rest as links, not plain text.
  - Deceased persons (10) are outside the Act ("individual" excludes a deceased natural person).
- **Correction and removal requests** (IPP 7 and basic fairness): honour quickly; the correction route serves this too.

#### 3.4.3 Site behaviour

The site runs no server, sets no cookies, and uses no analytics. `localStorage` holds quiz answers, the chosen
electorate, theme and dismissed banners on the visitor's device only. Third-party requests go to Google Fonts and
cdnjs (Cloudflare); each receives the visitor's IP address and user agent. GitHub Pages logs requests under GitHub's
privacy statement. Geolocation (`locateElectorate`) runs in the browser against local GeoJSON and sends nothing
anywhere. All of this is low-risk, but it should be stated (M10, S1).

#### 3.4.4 Privacy statement and geolocation wording

**Privacy statement (About view, linked from footer):**

> **Privacy.** Ballot Book NZ has no accounts, no server of its own, no cookies and no analytics. Your quiz answers,
> your chosen electorate and your display settings are stored only in your own browser (localStorage) and are never
> sent to us; clear your browser data to remove them. If you use "find my electorate", your browser asks your
> permission and your location is compared with electorate boundaries on your device only; it is not stored or sent.
> The site is hosted on GitHub Pages and loads fonts from Google Fonts and two code libraries from cdnjs (Cloudflare);
> those services receive your IP address when pages load, under their own privacy policies. Information about
> politicians and candidates comes from public sources (Parliament, party websites, policy.nz, Wikipedia, news
> reports); if you are a candidate or MP and want something corrected or removed, email *[address]*. Questions about
> privacy: *[address]*.

**Geolocation control (shown before the permission prompt):**

> *Use my location to find my electorate.* Your browser will ask for permission. Your location is checked against the
> electorate map on this device only; it is not stored or sent anywhere. You can also just choose your electorate from
> the list.

### 3.5 Harmful Digital Communications Act 2015 and Human Rights Act 1993

See N8 and N9. No user-generated content exists (confirmed in `site/index.html`: no input is displayed to other users;
no network writes). The HDCA communication principles (s 6) are still a useful checklist for the project's own
publications about individuals: Principle 1 (sensitive personal facts: the Residence field), Principle 6 (false
allegations: the controversy rules), Principle 10 (denigration on protected grounds: do not reproduce such material).
The criminal offence (s 22) requires intent to cause harm and is not a realistic exposure for a reference site.

### 3.6 Misinformation and impersonation

#### 3.6.1 Logos, colours, names

See N6. No logos are used. Party colours are used in charts and cards; that is fine. Party names are used descriptively.

#### 3.6.2 "Ballot Book"

See N7.

#### 3.6.3 "Not the Electoral Commission" disclaimer

Home and electorate views, one line under the title:

> *Independent and non-partisan. Not the Electoral Commission: for official information on enrolling, voting places and
> hours, go to vote.nz or call 0800 36 76 56.*

### 3.7 Accessibility

No statute imposes WCAG on a private New Zealand website. The Human Rights Act 1993 s 44 (discrimination in the
provision of goods and services) could in principle reach a public-facing site but has not been applied that way in NZ.
The benchmark is the NZ Government Web Accessibility Standard 1.2 (WCAG 2.2 Level AA, mandated for public service
agencies from 17 March 2025; a Digital Accessibility Standard is proposed to replace it in 2027). Good practice for a
voter guide, especially one with maps, seat charts and a compass that must not rely on colour alone (S12).

### 3.8 Planned features

#### 3.8.1 Geolocation to find the electorate

Lawful and sensible if it stays in the browser (it does). Use the consent wording in 3.4.4; do not persist coordinates;
store only the chosen electorate slug (already the behaviour); never send coordinates to a third-party geocoder. If an
address lookup is ever wanted, link to vote.nz's official finder rather than building one.

#### 3.8.2 "On this day in politics"

`raw/onthisday/` is currently Wikipedia-sourced (CC BY-SA 4.0: attribute and share alike, consistent with M9). If
**NZHistory** (Ministry for Culture and Heritage) content is used: its text is licensed **CC BY-NC 3.0 New Zealand**
("All text is licensed under the Creative Commons Attribution-NonCommercial 3.0 New Zealand Licence. Commercial re-use
may be allowed on request. All non-text content is subject to specific conditions"; the Ministry's rights statement as
published through DigitalNZ, confirming the nzhistory.govt.nz/copyright page). Non-commercial use is fine; attribute
"Ministry for Culture and Heritage, nzhistory.govt.nz, CC BY-NC 3.0 NZ" with a link; **do not copy NZHistory images**
(link instead); keep NZHistory-derived text in a clearly marked, separately licensed data file because NC content
cannot be re-licensed MIT or CC BY-SA, and any future sponsorship or advertising on the site would breach the NC term.
Short factual date lines written from primary sources (Hansard, Electoral Commission results) avoid the issue entirely.
On election day, the widget must not surface anything resembling voting advice; a date-driven widget is also "new
material" each day, so either pre-render the 7 November entry before polling day or suppress it that day.

#### 3.8.3 Party press-release feed from Scoop RSS

Headlines, dates and links only, attributed "via Scoop", with the party named as the author (S8, 3.2.5). Do not
republish full text automatically; do not run a server-side proxy that re-serves Scoop content. **Switch the feed off
for polling day** (00:00–19:00, 7 Nov): a feed is a system that pushes new material to the page, which is exactly what
s 197(2A)(a)–(b) and the Commission's "not add to the website" guidance exclude, and party releases on the day would
themselves be s 197 material.

#### 3.8.4 Links to candidates' social accounts

Linking is lawful. Risks are accuracy (linking to a parody or an impostor account would misattribute statements and
could defame) and privacy (link only accounts the candidate has published for public contact, e.g. in their policy.nz
or party profile; never personal accounts found by searching). Use plain links, not embedded timelines or platform
scripts (which set third-party cookies and would falsify the privacy statement). Note the policy.nz terms issue in
3.2.2 applies to the account URLs copied from there; the URLs themselves are facts, which is the lowest-risk category.

#### 3.8.5 Party-guessing / pass-the-phone game

Showing a verbatim policy statement and asking "which party said this?" is a quiz, not advocacy: it reveals the party
only after a guess, treats all parties alike and recommends nothing. Keep it free of scores tied to approval ("you
agree with…"), leaderboards, names or any shared state (N9), and disable it on polling day with the other interactive
results (it generates new statements on the day and displays party names and slogans, s 197(1)(g)(iii)). Policy text
used in the game is the same reproduction already addressed in 3.2.1; one or two sentences per item is fair dealing
territory and far safer than full texts.

---

## 4. What was checked in the repository

- `README.md`, `NOTICE.md`, `LICENSE`, `CONTRIBUTING.md`, `docs/EDITORIAL_STANDARDS.md`, `docs/FEATURE_REVIEW.md`,
  `docs/AGENT_BRIEF.md`.
- `site/index.html`: `electionPhase()`, `blockedToday()` (hides `match`, `compass`, `swipe`, `swipe-tally`, `polls`,
  `trends`), `ELECTION_DAY_BLOCK` text, home-view poll card, electorate "Battleground" tiles, `locateElectorate()`
  (browser-only), `store` (localStorage), About/Sources/Licences cards; no `mailto:` contact, no privacy text, no
  logos, no user input shown to others.
- `.github/workflows/polls.yml` (cron `17 */6 * * *`; rebuilds `site/` and pushes) and `pages.yml` (deploy on push).
- `parties/*/policies/documents/` (994 files, verbatim with source URL, retrieval date and method in front matter);
  `site/data/fulltext/*.json`.
- `parties/*/people/*/person.json` (685): 571 photos, of which 415 credited "Supplied to policy.nz by the candidate/party"
  and 306 with a stated licence; `questionnaire_2026` in 511 (Public email 271, of which 26 personal-domain; Residence
  264; Age 252); `born` in 283; 291 READMEs with a "Controversies" heading; questionnaire fields are rendered in
  `site/data/pages.json`.
- `data/geo/*.json` (Stats NZ, CC BY 4.0, attribution present); `data/parties-meta.json` (colours only).

## 5. References

Statutes (legislation.govt.nz, as at 23 October 2026):
- Electoral Act 1993: s 3A (meaning of election advertisement), s 3B (regulated period), s 3E (advertising expenses),
  s 197 (interfering with or influencing voters; s 197(2A) website defence), ss 204B–204H (promoters, promoter
  statement, authorisation), s 221B (election signs). https://www.legislation.govt.nz/act/public/1993/0087/latest/whole.html
- Electoral Amendment Act 2025 (2025 No 82); Ministry of Justice summary: https://www.justice.govt.nz/about/news-and-media/news/electoral-law-changes/
- Copyright Act 1994: s 21(3) (commissioned photographs), ss 26–27 (Crown copyright; works without copyright), s 29
  (infringement; substantial part), s 41 (incidental copying), s 42 (criticism, review, news reporting), s 43 (research
  or private study), ss 92B–92D (ISP safe harbours). https://www.legislation.govt.nz/act/public/1994/0143/latest/whole.html
- Defamation Act 1992: ss 8 (truth), 9–12 (honest opinion), 16–19 (qualified privilege), 21 (innocent dissemination),
  25–26 (retraction, reply, correction), Schedule 1. https://www.legislation.govt.nz/act/public/1992/0105/latest/whole.html
- Privacy Act 2020: s 7 (definitions: publicly available publication, news activity, news entity), s 22 and Schedule
  (IPPs 1–3, 3A, 11), s 27 (personal/domestic affairs). https://www.legislation.govt.nz/act/public/2020/0031/latest/whole.html
- Harmful Digital Communications Act 2015: ss 6 (communication principles), 22 (offence), 24 (safe harbour process).
- Human Rights Act 1993: s 44 (goods and services), s 61 (racial disharmony).
- Trade Marks Act 2002 s 89; Fair Trading Act 1986 ss 2, 9; Criminal Procedure Act 2011 s 211; Broadcasting Act 1989
  ss 2, 69–70.

Electoral Commission (2026):
- Publisher and Broadcaster Handbook, 2026 General Election (pp 7–12 definition, exemptions, promoter statements,
  advisory opinions; pp 25–27 election-day rules). https://elections.nz/assets/Handbooks/Publisher-and-Broadcaster-Handbook-2026-General-Election.pdf
- Third Party Handbook, 2026 General Election v2 (pp 18–20 definition and exemptions incl. group websites; p 27
  promoter statements on websites). https://www.elections.nz/assets/Handbooks/Third-Party-Handbook-2026-General-Election-v2.pdf
- 2026 General Election Media Kit (p 22 news coverage on election day; p 25 election-day rules). https://elections.nz/assets/2026-Media-Kit-/2026-General-Election-media-kit.pdf
- About election advertising: https://elections.nz/guidance-and-rules/for-voters/about-election-advertising/
- Social media (election day): https://elections.nz/guidance-and-rules/for-voters/social-media/
- For third party promoters (regulated period 7 Aug – 6 Nov 2026; $17,000 / $424,000): https://elections.nz/guidance-and-rules/for-third-party-promoters/

Cases:
- *Electoral Commission v Watson* [2016] NZCA 512 (meaning of "election advertisement"; reasonable observer; value of
  political speech); first instance *Watson v Electoral Commission* [2015] NZHC 666.
- *Lange v Atkinson* [2000] 3 NZLR 385 (CA) (qualified privilege, political statements).
- *Durie v Gardiner* [2018] NZCA 278 (public interest / responsible communication defence).
- *Television New Zealand Ltd v Newsmonitor Services Ltd* [1994] 2 NZLR 91 (HC) (copying whole programme scripts;
  fair dealing; implied licence) — illustrates that systematic whole-work copying for redistribution is hard to fit
  within fair dealing.

Third-party terms and licences:
- policy.nz Terms of service: https://policy.nz/terms
- Scoop terms and conditions of use: https://www.scoop.co.nz/about/terms.html
- Wikimedia Foundation Terms of Use §7 (CC BY-SA 4.0 licensing of text); Commons: Reusing content outside Wikimedia:
  https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia
- Creative Commons BY-SA 4.0 legal code (ss 3(a) attribution, 3(b) ShareAlike): https://creativecommons.org/licenses/by-sa/4.0/legalcode
- Stats NZ copyright and attribution template: https://www.stats.govt.nz/about-us/copyright/
- NZHistory copyright (CC BY-NC 3.0 NZ text; images separately conditioned): https://nzhistory.govt.nz/copyright
  (rights statement as republished on DigitalNZ records).
- GitHub DMCA Takedown Policy: https://docs.github.com/en/site-policy/content-removal-policies/dmca-takedown-policy
- NZ Government Web Accessibility Standard 1.2: https://www.digital.govt.nz/standards-and-guidance/nz-government-web-standards/web-accessibility-standard-1-2/

*Review date: 23 October 2026. Re-check the Commission's election-day guidance on 5–6 November in case it is updated.*
