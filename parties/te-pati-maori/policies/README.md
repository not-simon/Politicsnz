# Te Pāti Māori — 2026 election policies

Every 2026 policy of Te Pāti Māori that this archive could find, with a short neutral summary (**Why** — the reason the party gives; **How** — what it would do) and links to the **full verbatim text** of the party's own documents in [`documents/`](documents/). Election day: 7 November 2026. Compiled 23 October 2026.

## At a glance

- **91 policies** listed: 45 from [policy.nz](https://policy.nz) (all of its 45 Te Pāti Māori statements, with its Why/How summaries) + 46 more found in the party's own releases, speeches and policy PDFs (marked *archive*; summaries written for this archive).
- **68 full-text documents** archived (47 press releases/speeches, 21 PDFs) + 1 placeholder files for cited pages that could not be retrieved.
- 91 policies have at least one retrieved party text; 0 rely only on a page that could not be retrieved.

## Method & sources

1. Started from policy.nz's Te Pāti Māori data (`raw/policy.nz/parties/te-pati-maori.json`): statement, Why/How, citations.
2. maoriparty.org.nz blocks automated access (Cloudflare 403, also with a headless browser) and web.archive.org is unreachable from this environment. The party's own web pages were therefore recovered from **Common Crawl**: its 2026 crawl indexes (CC-MAIN-2026-12 … -43) were searched for every maoriparty.org.nz URL and the latest HTTP-200 capture of each page was read from the WARC archive on data.commoncrawl.org (`tools/policies_nzf_tpm_cc_index.py`, `tools/policies_nzf_tpm_cc_fetch.py`). Each such document (`documents/site-*.md`) records the capture date and WARC record; captures are 16 Aug–14 Oct 2026, so later edits are not reflected.
3. Instead, every Te Pāti Māori press release and speech from late 2025 to 23 Oct 2026 was collected from Scoop's organisation page (https://info.scoop.co.nz/Te_Pati_Maori); Scoop republishes party releases as issued, so their text is the party's own. Policy PDFs the party attached to releases (img.scoop.co.nz) or linked from its site (Google Drive) were downloaded and text-extracted.
4. Each policy links (a) the page policy.nz cited (now mostly a Common Crawl capture) and (b) other party texts on the same policy. Where a cited page could not be recovered at all, a `documents/not-retrieved-*.md` file records the URL and the reason; it contains no paraphrase.
5. Policies found in party texts but missing from policy.nz were added with neutral summaries (`summary_source: archive`). Calls on the current government and positions (e.g. opposing a bill) are included where the party presents them as what it stands for, and are labelled as such.

### Retrieval gaps (read this)

- **1 maoriparty.org.nz pages cited by policy.nz were not retrieved** (403 / archive unreachable). Where a party release covers the same policy it is linked, but the website page may contain details the release does not.
  - ['Sports', undated (accessed 18 August 2026)](documents/not-retrieved-maoriparty-sports.md) — <https://www.maoriparty.org.nz/sports> (policies: POL55068)
- The party's web policy pages are short summaries ("What we’ll do / Why it matters") that link to full manifesto chapters on Google Drive. Chapters recovered (all text-extracted in `documents/pdf-*.md`): Tax, Te Tiriti Entrenchment, Energy Sovereignty, Kai Sovereignty, Justice, Mana Motuhake, Military Neutrality, Climate, Toi Māori, Freshwater, Housing, Mokopuna Māori, Te Reo Māori, Mana Takatāpui. **No full chapter was linked for Health, Disabilities, Education & Training, Economic development or Cost of living** (those web pages have no Drive link in their captures); for these the web-page summary and the party's “What matters to you?” tool (which says its content is from the Policy Manifesto 2026) are the fullest party texts found.
- The site's Sports and Disability pages link to older documents (a 2020 sport policy; a 2023 Mana Hauā policy). They are archived but flagged as not 2026 policy.
- maoriparty.org.nz/sports (cited by policy.nz) has no Common Crawl capture; the policy index page (captured 8 Oct 2026) includes the same Sports summary.
- No Te Pāti Māori statement of formal coalition "bottom lines" was found. Its stated strategy is a candidate vote for Te Pāti Māori and party vote for Labour or the Greens, aiming for a one-term government.

## Headline commitments & stated conditions

- **Electoral strategy:** “Candidate vote Te Pāti Māori. Party vote Green or Labour, you choose.” The party list has one candidate (General Secretary Lance Norman) beyond its seven Māori electorate candidates. — [source](documents/2026-10-04-te-pati-maori-puts-its-money-where-its-mouth-is-with-one-per.md)
- **Goal:** “Our strategy is clear. We want more Māori in Parliament, a one-term Government, and an independent Māori voice that is accountable to our people.” — [source](documents/2026-10-04-te-pati-maori-puts-its-money-where-its-mouth-is-with-one-per.md)
- **Constitutional reform:** “Te Tiriti is the constitutional foundation of Aotearoa. Its mana does not rise and fall depending on who forms the Government.” — Entrenchment policy: binding Waitangi Tribunal recommendations, a Te Tiriti Commission with compliance-order powers, a $220m Mātike Mai Fund, UNDRIP action plan within 100 days. — [source](documents/2026-09-01-te-pati-maori-launches-te-tiriti-entrenchment-policy.md)
- **Tax:** Kiwi Tax Plan: first $30,000 tax-free, top rate 48% over $300,000, wealth tax from 1.5% above $2m net wealth, company tax back to 33%. (NZ First's leader said Te Pāti Māori called its tax policy a “bottom line”; this archive could not retrieve a Te Pāti Māori statement using that phrase.) — [source](documents/pdf-a-kiwi-tax-plan.md)

**Signature policies:** [Make the first $30,000 earned tax-free](#pol54812-make-the-first-30000-earned-tax-free); [Implement a targeted wealth tax starting from 1.5 percent](#pol54939-implement-a-targeted-wealth-tax-starting-from-15-percent); [Remove GST costs from kai](#pol54938-remove-gst-costs-from-kai); [Establish an independent Te Tiriti Commission](#pol54917-establish-an-independent-te-tiriti-commission); [Make Waitangi Tribunal recommendations binding](#pol54795-make-waitangi-tribunal-recommendations-binding); [Establish a $220 million Mātike Mai Fund and set 2040 as the target for constitutional transformation](#tpm-a03-establish-a-220-million-mātike-mai-fund-and-set-2040-as-the-target-for-constitutional-transformation); [Create a Māori Education Authority with responsibility for Māori education](#pol54679-create-a-māori-education-authority-with-responsibility-for-māori-education); [Invest in Māori energy sovereignty](#pol55059-invest-in-māori-energy-sovereignty); [Abolish prisons by 2040](#pol55283-abolish-prisons-by-2040); [Create an independent Māori Justice Authority funded from half of the Corrections, Police and Courts budgets](#tpm-a13-create-an-independent-māori-justice-authority-funded-from-half-of-the-corrections-police-and-courts-budgets); [Declare NZ a "military neutral" country](#pol54684-declare-nz-a-military-neutral-country); [Ban seabed mining](#pol54680-ban-seabed-mining); [$200 million over three years and an independent Takatāpui-governed Commission](#tpm-a12-200-million-over-three-years-and-an-independent-takatāpui-governed-commission); [Te Kōhanga Reo Act, secure baseline funding and 20 new kōhanga reo](#tpm-a08-te-kōhanga-reo-act-secure-baseline-funding-and-20-new-kōhanga-reo).

## Contents

- [Arts, culture, sport & takatāpui](#arts-culture-sport--takatāpui) (6)
- [Education & te reo Māori](#education--te-reo-māori) (8)
- [Environment, climate & energy](#environment-climate--energy) (16)
- [Foreign affairs & defence](#foreign-affairs--defence) (4)
- [Health, disability & whānau](#health-disability--whānau) (12)
- [Housing](#housing) (6)
- [Justice](#justice) (5)
- [Kai, cost of living & economy](#kai-cost-of-living--economy) (11)
- [Tax](#tax) (10)
- [Te Tiriti, constitution & democracy](#te-tiriti-constitution--democracy) (13)
- [Document index](#document-index)

## Arts, culture, sport & takatāpui

### POL55068: Invest in sports, particularly for young people

**Statement:** Invest in sports, particularly for young people  
*Summary source: policy.nz* · topics: media-culture-and-recreation, community-and-inclusion, sports-and-recreation, young-people

- **Why:** This party says that sports bring belonging, discipline, confidence, and connection, warranting support from government.
- **How:** This party would invest in sport initiatives which foster belonging and opportunity, including making sure there are pathways into sports for rangatahi.
- **Note:** policy.nz cites maoriparty.org.nz/sports, which Common Crawl did not capture; the party's policy index page (captured 8 Oct 2026) carries the same 'Sports' summary, and the party's 'What matters to you?' tool lists the Whānau Pakari sport fund.
- **Sources:**
  - ['Sports', undated (accessed 18 August 2026)](https://www.maoriparty.org.nz/sports) — full text **not retrieved** ([why](documents/not-retrieved-maoriparty-sports.md)) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818042739/https://www.maoriparty.org.nz/sports)
  - [Policy (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/policy) — [full text](documents/site-policy.md)
  - [Māori Sports (Party web page (Common Crawl), 2026-03-17)](https://www.maoriparty.org.nz/maori_sports) — [full text](documents/site-maori-sports.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL55072: Support Māori art and creativity

**Statement:** Support Māori art and creativity  
*Summary source: policy.nz* · topics: media-culture-and-recreation, te-ao-maori, arts-culture-and-heritage, te-reo-maori-and-culture

- **Why:** This party says that Toi Māori should be supported by the government, as such art is not decoration. It is truth-telling, resistance, healing, identity, and legacy. It tells stories that have historically been silenced by the Crown.
- **How:** This party would protect Māori cultural rights and expressions. The party would provide additional support for Māori-led arts infrastructure, funding, and pathways as well as Toi Māori and Māori creative industries.
- **Sources:**
  - ['Toi Māori', undated (accessed 18 August 2026)](https://www.maoriparty.org.nz/toi_maori) — [full text](documents/site-toi-maori.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818013537/https://www.maoriparty.org.nz/toi_maori)
  - [Te Pāti Māori Announces Toi Māori Authority And Artist Income Programme (Press release, 2026-10-12)](https://www.scoop.co.nz/stories/PA2610/S00101/te-pati-maori-announces-toi-maori-authority-and-artist-income-programme.htm) — [full text](documents/2026-10-12-te-pati-maori-announces-toi-maori-authority-and-artist-incom.md)
  - [Toi Māori — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1Jc9cFUmV5YgkPg7tlKpojeiOSvXzJX1N/view) — [full text](documents/pdf-toi-maori.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL55086: Protect takatāpui Māori

**Statement:** Protect takatāpui Māori  
*Summary source: policy.nz* · topics: community-and-inclusion, te-ao-maori, law-justice-and-government, rainbow-community, te-reo-maori-and-culture, civil-justice

- **Why:** This party says that takatāpui Māori should not have to fear discrimination or harm, nor should they be pushed to the margins. Takatāpui Māori should have the space and freedom to be themselves.
- **How:** This party would protect Takatāpui Māori's wellbeing, safety and dignity, and ensure public services account for this.
- **Sources:**
  - ['Takatāpui ', 3 June 2026 (accessed 18 August 2026)](https://www.maoriparty.org.nz/takat_pui) — [full text](documents/site-takat-pui.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818043345/https://www.maoriparty.org.nz/takat_pui)
  - [Te Pāti Māori Launches Mana Takatāpui Policy (Press release, 2026-09-23)](https://www.scoop.co.nz/stories/PA2609/S00245/te-pati-maori-launches-mana-takatapui-policy.htm) — [full text](documents/2026-09-23-te-pati-maori-launches-mana-takatapui-policy.md)
  - [Mana Takatāpui — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1qyqzCxGrLF067Q2S5ZafwQ1F_UDOpPj0/view) — [full text](documents/pdf-mana-takatapui.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A11: Independent Toi Māori Authority and an income programme for 1,000 Māori artists

**Statement:** Independent Toi Māori Authority and an income programme for 1,000 Māori artists  
*Summary source: archive* · topics: arts-culture-and-heritage, te-ao-maori

- **Why:** The party says colonisation targeted Māori artists and knowledge-holders and decisions on Toi Māori should be in Māori hands.
- **How:** This party would create a Toi Māori Authority independent of Creative New Zealand, funded at parity with it and governed by tohunga toi, and a rotating programme paying 1,000 artists at a time for 30 hours a week over two years. The Toi Māori chapter also commits $19 million baseline funding for Te Matatini, $10 million for community, hapū and iwi kapa haka, a $10 million Toi Māori research fund, and a living wage for employed and contracted artists.
- **Sources:**
  - [Te Pāti Māori Announces Toi Māori Authority And Artist Income Programme (Press release, 2026-10-12)](https://www.scoop.co.nz/stories/PA2610/S00101/te-pati-maori-announces-toi-maori-authority-and-artist-income-programme.htm) — [full text](documents/2026-10-12-te-pati-maori-announces-toi-maori-authority-and-artist-incom.md)
  - [Toi Māori — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1Jc9cFUmV5YgkPg7tlKpojeiOSvXzJX1N/view) — [full text](documents/pdf-toi-maori.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A12: $200 million over three years and an independent Takatāpui-governed Commission

**Statement:** $200 million over three years and an independent Takatāpui-governed Commission  
*Summary source: archive* · topics: community-and-inclusion, health, housing

- **Why:** The party says decisions about takatāpui have been made without takatāpui.
- **How:** This party would commit $200 million over three years (reported as reprioritised from health, social development, housing and Māori development) and create an independent Takatāpui-governed Commission with authority over ring-fenced funding for gender-affirming kaupapa Māori healthcare, mental health and suicide prevention, safe housing, protection from violence and hate, culture and education. The chapter also commits to updating the Human Rights Act for people of diverse genders, sexualities and sex characteristics.
- **Note:** The funding breakdown by portfolio comes from news coverage (RNZ reports co-leader Rawiri Waititi gave it: $100m Health, $50m Social Development, $40m Housing, $10m Vote Māori), not from the party release archived here.
- **Sources:**
  - [Te Pāti Māori Launches Mana Takatāpui Policy (Press release, 2026-09-23)](https://www.scoop.co.nz/stories/PA2609/S00245/te-pati-maori-launches-mana-takatapui-policy.htm) — [full text](documents/2026-09-23-te-pati-maori-launches-mana-takatapui-policy.md)
  - [Mana Takatāpui — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1qyqzCxGrLF067Q2S5ZafwQ1F_UDOpPj0/view) — [full text](documents/pdf-mana-takatapui.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)
  - [NZ Herald: Te Pāti Māori announces $200m fund to create Takatāpui commission](https://www.nzherald.co.nz/nz/politics/election-2026-te-pati-maori-announces-200m-fund-to-create-takatapui-commission/6V6TE7RCBJCFVIUVRTE53VHJTQ/) — News coverage (not party text).
  - [RNZ: Te Pāti Māori promises $200 million to change 'who holds power' for decisions about takatāpui](https://www.rnz.co.nz/news/politics_election-2026/1530281/te-pati-maori-promises-200-million-to-change-who-holds-power-for-decisions-about-takatapui) — News coverage (not party text).

### TPM-A39: A $100 million Whānau Pakari sport fund and Māori teams competing as Aotearoa Māori

**Statement:** A $100 million Whānau Pakari sport fund and Māori teams competing as Aotearoa Māori  
*Summary source: archive* · topics: sports-and-recreation, young-people, te-ao-maori

- **Why:** The party says sport builds belonging, wellbeing and pathways for rangatahi.
- **How:** The party's 2026 policy tool lists 'A $100 million Whānau Pakari fund for sport' (Māori sports academies, scholarships, funding for Pā Wars) and 'Māori teams competing overseas as Aotearoa Māori'. The fuller Whānau Pakari policy document the site links to dates from 2020.
- **Sources:**
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)
  - [Māori Sports (Party web page (Common Crawl), 2026-03-17)](https://www.maoriparty.org.nz/maori_sports) — [full text](documents/site-maori-sports.md)
  - [Whānau Pakari – Sport and Wellbeing Policy (2020 document — NOT confirmed as 2026 policy) (PDF)](https://drive.google.com/file/d/1IeJ-WmT2cwdeo6noqVaSRFk55dhQGpNl/view) — [full text](documents/pdf-whanau-pakari-sport-and-wellbeing-policy.md)

## Education & te reo Māori

### POL54679: Create a Māori Education Authority with responsibility for Māori education

**Statement:** Create a Māori Education Authority with responsibility for Māori education  
*Summary source: policy.nz* · topics: te-ao-maori, education, te-reo-maori-and-culture, schools, early-childhood-education

- **Why:** This party says that every child deserves to learn in a way that celebrates their culture. Children who are connected to their identity do better in the education system. Creating education systems that focus on whānau, identity and different knowledge systems will help children to succeed
- **How:** This party would increase funding in kōhanga reo and kura kaupapa Māori, wharekura and wānanga. It would embed the use of mātauranga Māori throughout the curriculum and make te reo Māori a core curriculum subject through Year 10. It also believes in expanding school lunches, free public transport for students, free school counselling and increased student support, and strengthening the education workforce.
- **Sources:**
  - ['Te Pāti Māori Announces a Māori Education Authority ', 2 August 2026 (accessed 11 August 2026)](https://www.scoop.co.nz/stories/PA2608/S00006/te-pati-maori-announces-maori-education-authority-to-restore-maori-success-in-education.htm?_gl=1%2A1x1ylqz%2A_gcl_au%2AMTk4NTg5NzkzNi4xNzg2NDAxNDc5%2A_ga%2AMTA2ODM2Mjg3Mi4xNzg2NDAxNDc5%2A_ga_GGVMM3MB82%2AczE3ODY0MTg1OTkkbzIkZzEkdDE3ODY0MTg3MTAkajUzJGwwJGgw) — [full text](documents/2026-08-02-te-pati-maori-announces-maori-education-authority-to-restore.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260811032531/https://www.scoop.co.nz/stories/PA2608/S00006/te-pati-maori-announces-maori-education-authority-to-restore-maori-success-in-education.htm?_gl=1%2A1x1ylqz%2A_gcl_au%2AMTk4NTg5NzkzNi4xNzg2NDAxNDc5%2A_ga%2AMTA2ODM2Mjg3Mi4xNzg2NDAxNDc5%2A_ga_GGVMM3MB82%2AczE3ODY0MTg1OTkkbzIkZzEkdDE3ODY0MTg3MTAkajUzJGwwJGgw)
  - ['Education and Training', undated (accessed 18 August 2026)](https://www.maoriparty.org.nz/education_training) — [full text](documents/site-education-training.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818013419/https://www.maoriparty.org.nz/education_training)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL55065: Make the state legally accountable for protecting te reo Māori

**Statement:** Make the state legally accountable for protecting te reo Māori  
*Summary source: policy.nz* · topics: te-ao-maori, te-reo-maori-and-culture, te-tiriti-o-waitangi-and-governance

- **Why:** This party says that te reo Māori is a fundamental part of New Zealand and must be both protected and strengthened.
- **How:** This party would normalise te reo Māori in all facets of life, by investing in learning pathways and community re-vitalisation. The party would also make the state legally accountable for the language's protection.
- **Sources:**
  - ['Te reo Māori', undated (accessed 18 August 2026)](https://www.maoriparty.org.nz/te_reo_maori) — [full text](documents/site-te-reo-maori.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818042325/https://www.maoriparty.org.nz/te_reo_maori)
  - [Te Reo Māori — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1m8zZo4j-pzDqeQdFj_OcVTPjq6VgEHCh/view) — [full text](documents/pdf-te-reo-maori.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A08: Te Kōhanga Reo Act, secure baseline funding and 20 new kōhanga reo

**Statement:** Te Kōhanga Reo Act, secure baseline funding and 20 new kōhanga reo  
*Summary source: archive* · topics: early-childhood-education, te-reo-maori-and-culture

- **Why:** The party says kōhanga reo are the heartbeat of te reo Māori revitalisation and need long-term certainty.
- **How:** This party would pass a Te Kōhanga Reo Act, lock in annual baseline funding, create a $20 million-a-year capital fund, invest $50 million to clear the backlog of around 80 kōhanga needing new builds or refurbishment, and fund 20 new kōhanga reo over three years.
- **Sources:**
  - [Te Pāti Māori Backs Kōhanga Reo And Kura With Long-Term Investment (Press release, 2026-10-06)](https://www.scoop.co.nz/stories/PA2610/S00052/te-pati-maori-backs-kohanga-reo-and-kura-with-long-term-investment.htm) — [full text](documents/2026-10-06-te-pati-maori-backs-kohanga-reo-and-kura-with-long-term-inve.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A09: $1.25 billion for kura Māori property and restore Te Ahu o Te Reo Māori

**Statement:** $1.25 billion for kura Māori property and restore Te Ahu o Te Reo Māori  
*Summary source: archive* · topics: schools, te-reo-maori-and-culture

- **Why:** The party says kura need fit-for-purpose buildings and the education workforce needs te reo capability.
- **How:** This party would commit $1.25 billion over five years ($250 million a year) through a ring-fenced kura Māori property plan, and restore Te Ahu o Te Reo Māori with $30 million a year.
- **Sources:**
  - [Te Pāti Māori Backs Kōhanga Reo And Kura With Long-Term Investment (Press release, 2026-10-06)](https://www.scoop.co.nz/stories/PA2610/S00052/te-pati-maori-backs-kohanga-reo-and-kura-with-long-term-investment.htm) — [full text](documents/2026-10-06-te-pati-maori-backs-kohanga-reo-and-kura-with-long-term-inve.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A10: Expand school lunches, free public transport for students, free school counselling, te reo Māori core to Year 10

**Statement:** Expand school lunches, free public transport for students, free school counselling, te reo Māori core to Year 10  
*Summary source: archive* · topics: schools, education, public-transport-cycling-and-walking

- **Why:** The party says Māori learners thrive when whānau are central and identity is upheld.
- **How:** Alongside the Māori Education Authority, the party's education policy includes expanding school lunches, free public transport for all students, free school counselling, making te reo Māori a core curriculum subject through Year 10, more student support and a stronger education workforce.
- **Sources:**
  - [Te Pāti Māori Announces Māori Education Authority To Restore Māori Success In Education (Press release, 2026-08-02)](https://www.scoop.co.nz/stories/PA2608/S00006/te-pati-maori-announces-maori-education-authority-to-restore-maori-success-in-education.htm) — [full text](documents/2026-08-02-te-pati-maori-announces-maori-education-authority-to-restore.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A27: Write off the living-cost part of student loans and pay every student a doubled student allowance

**Statement:** Write off the living-cost part of student loans and pay every student a doubled student allowance  
*Summary source: archive* · topics: tertiary-education, education

- **Why:** The party says cost barriers block whānau from education and training.
- **How:** The party's policy tool says the living-cost component of every student loan would be written off (working towards full write-offs for people who live and work here for five years), and every student would get a student allowance at double the rate, with the parental income test scrapped and allowances restored for postgraduate, part-time and long-course students.
- **Sources:**
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A28: Teachers' pay rises that keep up with inflation

**Statement:** Teachers' pay rises that keep up with inflation  
*Summary source: archive* · topics: schools, wages-and-working-conditions

- **Why:** The party says the education workforce needs support on pay and workload.
- **How:** The party's policy tool lists pay rises for teachers that keep up with inflation, support for Māori teachers, kaiako and support staff, and action on pay inequity and workload; it also lists second-chance and adult education and kai-sovereignty scholarships and trades apprenticeships.
- **Sources:**
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A38: Make te reo Māori compulsory in education and require public agencies to work bilingually

**Statement:** Make te reo Māori compulsory in education and require public agencies to work bilingually  
*Summary source: archive* · topics: te-reo-maori-and-culture, schools, public-sector

- **Why:** The party says te reo should be part of everyday life, not something you have to ask for.
- **How:** The 2026 Te Reo Māori chapter commits to compulsory te reo Māori in the education system with age-appropriate progression, bilingual public institutions, funding whānau-, marae-, hapū- and iwi-led reo initiatives, stronger Māori media and broadcasting, and protections against rollback of te reo commitments.
- **Sources:**
  - [Te Reo Māori — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1m8zZo4j-pzDqeQdFj_OcVTPjq6VgEHCh/view) — [full text](documents/pdf-te-reo-maori.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

## Environment, climate & energy

### POL54680: Ban seabed mining

**Statement:** Ban seabed mining  
*Summary source: policy.nz* · topics: economy, environment, oil-gas-and-mining, oceans, conservation

- **Why:** This party says that the sea is a responsibility and inheritance, not a resource for extraction. Seabed mining threatens the integrity of important natural places.
- **How:** This party would ban seabed mining.
- **Sources:**
  - ['Climate', 3 June 2026 (accessed 18 August 2026)](https://www.maoriparty.org.nz/climate) — [full text](documents/site-climate.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818043455/https://www.maoriparty.org.nz/climate)
  - [Seabed Mining Banned In Aotearoa Under Reintroduced Member’s Bill (Press release, 2026-02-08)](https://www.scoop.co.nz/stories/PA2602/S00040/seabed-mining-banned-in-aotearoa-under-reintroduced-members-bill.htm) — [full text](documents/2026-02-08-seabed-mining-banned-in-aotearoa-under-reintroduced-members.md)
  - [Climate — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1FzavJoSYNEzsVWhnS9sBMI3XENAb9-Dr/view) — [full text](documents/pdf-climate.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL54681: Invest in adaptation for communities most at risk from climate change

**Statement:** Invest in adaptation for communities most at risk from climate change  
*Summary source: policy.nz* · topics: environment, te-ao-maori, climate-adaptation, land-and-resources

- **Why:** This party says that land and marae are at risk from climate change. Adapting to climate change includes protecting the right to live safely on land. Māori deserve to have sovereignty on their land, even if the changing climate is putting that land at risk.
- **How:** This party would ensure communities at risk from natural disasters, flooding and other climate impacts are prioritised with funding for adapting to climate impacts.
- **Sources:**
  - ['Climate', 3 June 2026 (accessed 18 August 2026)](https://www.maoriparty.org.nz/climate) — [full text](documents/site-climate.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818043455/https://www.maoriparty.org.nz/climate)
  - [Climate — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1FzavJoSYNEzsVWhnS9sBMI3XENAb9-Dr/view) — [full text](documents/pdf-climate.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL54682: Support sustainable and regenerative means of emissions reduction in line with Māori values

**Statement:** Support sustainable and regenerative means of emissions reduction in line with Māori values  
*Summary source: policy.nz* · topics: environment, te-ao-maori, emissions-reduction, oceans, land-and-resources

- **Why:** This party says that whenua (land) and moana (ocean) are our responsibility and future. Climate justice must work to protect these vital resources, not exploit them.
- **How:** This party would focus emissions reduction efforts on sustainable and regenerative approaches.
- **Sources:**
  - ['Climate', 3 June 2026 (accessed 18 August 2026)](https://www.maoriparty.org.nz/climate) — [full text](documents/site-climate.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818043455/https://www.maoriparty.org.nz/climate)
  - [Climate — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1FzavJoSYNEzsVWhnS9sBMI3XENAb9-Dr/view) — [full text](documents/pdf-climate.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL55058: Provide financial support to households purchasing solar infrastructure and efficient appliances

**Statement:** Provide financial support to households purchasing solar infrastructure and efficient appliances  
*Summary source: policy.nz* · topics: transport-and-infrastructure, housing, environment, energy, housing-quality, climate-adaptation

- **Why:** This party says that electricity and electricity generation is increasingly increasingly is carried out by large corporations focused on profits, not people. Returning electricity generation to the people will allow costs to come down and move Aotearoa towards energy sovereignty.
- **How:** This party would provide financial support for whānau purchasing solar-power, energy-efficient appliances and EV charging ports. This support would be long-term, low-cost, and without interest.
- **Sources:**
  - ['We Want Cheaper Power and We Want Our People To Own It ', 16 September 2026 (accessed 21 September 2026)](https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it) — [full text](documents/site-we-want-cheaper-power-and-we-want-our-people-to-own-it.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260921002528/https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it)
  - [Energy Sovereignty Policy 2026 (PDF)](https://img.scoop.co.nz/media/pdfs/2609/Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf) — [full text](documents/pdf-te-pti-mori-energy-sovereignty-policy-final.md)
  - [We Want Cheaper Power And We Want Our People To Own It (Press release, 2026-09-16)](https://www.scoop.co.nz/stories/PA2609/S00161/we-want-cheaper-power-and-we-want-our-people-to-own-it.htm) — [full text](documents/2026-09-16-we-want-cheaper-power-and-we-want-our-people-to-own-it.md)
  - [Energy Sovereignty — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/1CPy0C0flCQ71RKuSmtaD3CNsoShG7QAc/view) — [full text](documents/pdf-energy-sovereignty.md)
  - [Energy Sovereignty (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/energy_sovereignty) — [full text](documents/site-energy-sovereignty.md)

### POL55059: Invest in Māori energy sovereignty

**Statement:** Invest in Māori energy sovereignty  
*Summary source: policy.nz* · topics: transport-and-infrastructure, environment, te-ao-maori, energy, climate-adaptation, te-tiriti-o-waitangi-and-governance

- **Why:** This party says that currently energy production extracts wealth and autonomy from Māori. An energy transition must uphold tino rangatiratanga and give Māori tangible rights surrounding, and ownership of, energy
- **How:** This party would establish a $1b energy sovereignty fund. It will invest in energy resilience on marae, papakāinga, and Māori land more generally. It will also reduce household power costs and provide workforce development opportunities, with an end goal of allowing whānau, iwi, and more to own more energy assets.
- **Sources:**
  - ['We Want Cheaper Power and We Want Our People To Own It ', 16 September 2026 (accessed 21 September 2026)](https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it) — [full text](documents/site-we-want-cheaper-power-and-we-want-our-people-to-own-it.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260921002528/https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it)
  - [Energy Sovereignty Policy 2026 (PDF)](https://img.scoop.co.nz/media/pdfs/2609/Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf) — [full text](documents/pdf-te-pti-mori-energy-sovereignty-policy-final.md)
  - [We Want Cheaper Power And We Want Our People To Own It (Press release, 2026-09-16)](https://www.scoop.co.nz/stories/PA2609/S00161/we-want-cheaper-power-and-we-want-our-people-to-own-it.htm) — [full text](documents/2026-09-16-we-want-cheaper-power-and-we-want-our-people-to-own-it.md)
  - [Energy Sovereignty — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/1CPy0C0flCQ71RKuSmtaD3CNsoShG7QAc/view) — [full text](documents/pdf-energy-sovereignty.md)
  - [Energy Sovereignty (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/energy_sovereignty) — [full text](documents/site-energy-sovereignty.md)

### POL55060: Establish a national energy independence plan

**Statement:** Establish a national energy independence plan  
*Summary source: policy.nz* · topics: transport-and-infrastructure, environment, energy, emissions-reduction

- **Why:** This party says that electricity and electricity generation increasingly is carried out by large corporations focused on profits, not people. It's important to create a pathway to energy independence away from monopolies.
- **How:** This party would create an independent national energy plan. It would implement a fairness framework to regulate power prices, and also identify where the renewable energies are required for a transition to cleaner energy. It would also fund upgrades and distribution required for new renewable energies. By 2035, this party wants New Zealand to have achieved energy sovereignty.
- **Sources:**
  - ['We Want Cheaper Power and We Want Our People To Own It ', 16 September 2026 (accessed 21 September 2026)](https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it) — [full text](documents/site-we-want-cheaper-power-and-we-want-our-people-to-own-it.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260921002528/https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it)
  - [Energy Sovereignty Policy 2026 (PDF)](https://img.scoop.co.nz/media/pdfs/2609/Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf) — [full text](documents/pdf-te-pti-mori-energy-sovereignty-policy-final.md)
  - [We Want Cheaper Power And We Want Our People To Own It (Press release, 2026-09-16)](https://www.scoop.co.nz/stories/PA2609/S00161/we-want-cheaper-power-and-we-want-our-people-to-own-it.htm) — [full text](documents/2026-09-16-we-want-cheaper-power-and-we-want-our-people-to-own-it.md)
  - [We Must Act Now On Energy Sovereignty- Every Household Is Paying The Price (Press release, 2026-04-09)](https://www.scoop.co.nz/stories/PA2604/S00042/we-must-act-now-on-energy-sovereignty-every-household-is-paying-the-price.htm) — [full text](documents/2026-04-09-we-must-act-now-on-energy-sovereignty-every-household-is-pay.md)
  - [If The Government Really Wants To Lower Power Bills, This Is The Way (Press release, 2026-06-09)](https://www.scoop.co.nz/stories/PA2606/S00066/if-the-government-really-wants-to-lower-power-bills-this-is-the-way.htm) — [full text](documents/2026-06-09-if-the-government-really-wants-to-lower-power-bills-this-is.md)
  - [Energy Sovereignty — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/1CPy0C0flCQ71RKuSmtaD3CNsoShG7QAc/view) — [full text](documents/pdf-energy-sovereignty.md)
  - [Energy Sovereignty (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/energy_sovereignty) — [full text](documents/site-energy-sovereignty.md)

### POL55061: Build rural energy capability and on-farm generation

**Statement:** Build rural energy capability and on-farm generation  
*Summary source: policy.nz* · topics: transport-and-infrastructure, economy, environment, energy, regional-development, agriculture

- **Why:** This party says that electricity and electricity generation is increasingly is carried out by large corporations focused on profits, not people. Therefore, making a pathway to energy independence away from monopolies, owned and benefiting rural communities is essential.
- **How:** This party would support rural communities in generating and storing renewable energy on-farm.
- **Sources:**
  - ['We Want Cheaper Power and We Want Our People To Own It ', 16 September 2026 (accessed 21 September 2026)](https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it) — [full text](documents/site-we-want-cheaper-power-and-we-want-our-people-to-own-it.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260921002528/https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it)
  - [Energy Sovereignty Policy 2026 (PDF)](https://img.scoop.co.nz/media/pdfs/2609/Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf) — [full text](documents/pdf-te-pti-mori-energy-sovereignty-policy-final.md)
  - [Energy Sovereignty — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/1CPy0C0flCQ71RKuSmtaD3CNsoShG7QAc/view) — [full text](documents/pdf-energy-sovereignty.md)
  - [Energy Sovereignty (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/energy_sovereignty) — [full text](documents/site-energy-sovereignty.md)

### POL55062: Improve compensation for households generating power into the grid

**Statement:** Improve compensation for households generating power into the grid  
*Summary source: policy.nz* · topics: transport-and-infrastructure, environment, incomes-and-employment, energy, emissions-reduction, prices

- **Why:** This party says that while households and communities are beginning to store and produce renewable power like solar energy, they are not being properly compensated for giving the energy system a buffer.
- **How:** This party would ensure households and communities are paid fairly for energy production and storage.
- **Sources:**
  - ['We Want Cheaper Power and We Want Our People To Own It ', 16 September 2026 (accessed 21 September 2026)](https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it) — [full text](documents/site-we-want-cheaper-power-and-we-want-our-people-to-own-it.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260921002528/https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it)
  - [Energy Sovereignty Policy 2026 (PDF)](https://img.scoop.co.nz/media/pdfs/2609/Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf) — [full text](documents/pdf-te-pti-mori-energy-sovereignty-policy-final.md)
  - [We Want Cheaper Power And We Want Our People To Own It (Press release, 2026-09-16)](https://www.scoop.co.nz/stories/PA2609/S00161/we-want-cheaper-power-and-we-want-our-people-to-own-it.htm) — [full text](documents/2026-09-16-we-want-cheaper-power-and-we-want-our-people-to-own-it.md)
  - [Energy Sovereignty — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/1CPy0C0flCQ71RKuSmtaD3CNsoShG7QAc/view) — [full text](documents/pdf-energy-sovereignty.md)
  - [Energy Sovereignty (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/energy_sovereignty) — [full text](documents/site-energy-sovereignty.md)

### POL55063: Reduce dependence on fossil fuels to protect sovereignty

**Statement:** Reduce dependence on fossil fuels to protect sovereignty  
*Summary source: policy.nz* · topics: environment, transport-and-infrastructure, economy, climate-adaptation, energy, foreign-investment

- **Why:** This party says that Aotearoa is currently reliant on fossil fuels imported from overseas. This means that not only is New Zealand contributing to the climate crisis, but it also has much reduced resilience against energy shocks.
- **How:** This party would support business, farms, transport and industry to switch to home-grown renewable energy sources.
- **Sources:**
  - ['We Want Cheaper Power and We Want Our People To Own It ', 16 September 2026 (accessed 21 September 2026)](https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it) — [full text](documents/site-we-want-cheaper-power-and-we-want-our-people-to-own-it.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260921002528/https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it)
  - [Energy Sovereignty Policy 2026 (PDF)](https://img.scoop.co.nz/media/pdfs/2609/Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf) — [full text](documents/pdf-te-pti-mori-energy-sovereignty-policy-final.md)
  - [Energy Sovereignty — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/1CPy0C0flCQ71RKuSmtaD3CNsoShG7QAc/view) — [full text](documents/pdf-energy-sovereignty.md)
  - [Energy Sovereignty (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/energy_sovereignty) — [full text](documents/site-energy-sovereignty.md)

### POL55064: Protect Māori data sovereignty

**Statement:** Protect Māori data sovereignty  
*Summary source: policy.nz* · topics: te-ao-maori, economy, transport-and-infrastructure, te-reo-maori-and-culture, te-tiriti-o-waitangi-and-governance, internet-and-digital-technologies

- **Why:** This party says that electricity and electricity generation increasingly is carried out by large corporations focused on profits rather than serving the people.  A pathway to renewable energy independence away from monopolies is needed, but the technologies involved in such a transition must respect tino rangatiratanga.
- **How:** This party would protect Māori data generated through smart meters, energy systems, trading platforms, and other technologies, and ensure that such information is only used for the benefit of Māori with their authority
- **Sources:**
  - ['We Want Cheaper Power and We Want Our People To Own It ', 16 September 2026 (accessed 21 September 2026)](https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it) — [full text](documents/site-we-want-cheaper-power-and-we-want-our-people-to-own-it.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260921002528/https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it)
  - [Energy Sovereignty Policy 2026 (PDF)](https://img.scoop.co.nz/media/pdfs/2609/Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf) — [full text](documents/pdf-te-pti-mori-energy-sovereignty-policy-final.md)
  - [Energy Sovereignty — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/1CPy0C0flCQ71RKuSmtaD3CNsoShG7QAc/view) — [full text](documents/pdf-energy-sovereignty.md)
  - [Energy Sovereignty (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/energy_sovereignty) — [full text](documents/site-energy-sovereignty.md)

### POL55085: Assert tino rangatiratanga over freshwater

**Statement:** Assert tino rangatiratanga over freshwater  
*Summary source: policy.nz* · topics: te-ao-maori, environment, te-tiriti-o-waitangi-and-governance, fresh-water-and-pollution, conservation, land-and-resources

- **Why:** This party says that water is the lifeblood of all those who live in New Zealand, yet decisions about it are rarely taken in concord with mana whenua.
- **How:** This party would assert Māori authority and rights over freshwater, and stop freshwater decisions being made without the go-ahead of iwi and hapū. This will ensure water is protected and its benefits are shared.
- **Sources:**
  - ['Freshwater Policy', undated (accessed 18 August 2026)](https://www.maoriparty.org.nz/freshwater_policy) — [full text](documents/site-freshwater-policy.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818043557/https://www.maoriparty.org.nz/freshwater_policy)
  - [Freshwater — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1LPTzVr2sdxSNdfLF2DFLikHqr2zaeuBP/view) — [full text](documents/pdf-freshwater.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A07: Give the Commerce Commission and Electricity Authority stronger powers over power prices and profits

**Statement:** Give the Commerce Commission and Electricity Authority stronger powers over power prices and profits  
*Summary source: archive* · topics: energy, prices

- **Why:** The party says energy is essential infrastructure that must serve people before profit.
- **How:** This party would strengthen regulators' powers to investigate excessive pricing and profits, with structural intervention, pricing tools and enforceable remedies if regulation fails, and remove barriers to whānau and communities generating and trading energy. It sets 2035 as the target for 'Energy Sovereignty'.
- **Sources:**
  - [Energy Sovereignty Policy 2026 (PDF)](https://img.scoop.co.nz/media/pdfs/2609/Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf) — [full text](documents/pdf-te-pti-mori-energy-sovereignty-policy-final.md)
  - [We Want Cheaper Power And We Want Our People To Own It (Press release, 2026-09-16)](https://www.scoop.co.nz/stories/PA2609/S00161/we-want-cheaper-power-and-we-want-our-people-to-own-it.htm) — [full text](documents/2026-09-16-we-want-cheaper-power-and-we-want-our-people-to-own-it.md)

### TPM-A34: End new oil and gas exploration and withdraw existing permits within five years

**Statement:** End new oil and gas exploration and withdraw existing permits within five years  
*Summary source: archive* · topics: emissions-reduction, energy, oceans

- **Why:** The party says whenua and moana must be protected from extractive industries.
- **How:** The 2026 Climate chapter commits to ending new oil and gas exploration, withdrawing existing on- and offshore permits within five years and decommissioning sites within ten, with planning and support for workers through a just transition.
- **Sources:**
  - [Climate — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1FzavJoSYNEzsVWhnS9sBMI3XENAb9-Dr/view) — [full text](documents/pdf-climate.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A35: Repeal the Fast-track Approvals Act and end mining on conservation land

**Statement:** Repeal the Fast-track Approvals Act and end mining on conservation land  
*Summary source: archive* · topics: conservation, land-and-resources, urban-planning-and-resource-management

- **Why:** The party says fast-track consenting overrides mana whenua and the environment.
- **How:** The 2026 Climate chapter commits to repealing the Fast-track Approvals Act and retrospectively revoking all fast-tracked mining consents, and ending mining on conservation land including reserves and Significant Natural Areas.
- **Sources:**
  - [Climate — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1FzavJoSYNEzsVWhnS9sBMI3XENAb9-Dr/view) — [full text](documents/pdf-climate.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A36: $1 billion Pūngao Auaha Fund for solar and insulation on marae, kura, papakāinga and homes

**Statement:** $1 billion Pūngao Auaha Fund for solar and insulation on marae, kura, papakāinga and homes  
*Summary source: archive* · topics: energy, climate-adaptation, housing

- **Why:** The party says Māori communities should benefit from the energy transition.
- **How:** The 2026 Climate chapter establishes a $1 billion Pūngao Auaha Fund to retrofit marae, kura, papakāinga and housing with solar and insulation, support Māori-led community energy and move Māori-owned businesses off coal and gas. (It is separate in the Climate chapter from the $1 billion Energy Sovereignty Fund in the Energy chapter; the documents do not say whether these overlap.)
- **Sources:**
  - [Climate — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1FzavJoSYNEzsVWhnS9sBMI3XENAb9-Dr/view) — [full text](documents/pdf-climate.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A37: Guarantee safe, affordable drinking water and ban the trading of water rights

**Statement:** Guarantee safe, affordable drinking water and ban the trading of water rights  
*Summary source: archive* · topics: fresh-water-and-pollution, infrastructure-funding-and-planning

- **Why:** The party says water is a taonga, not a market asset.
- **How:** The 2026 Freshwater chapter commits to safe, affordable drinking water for all whānau, investment in water infrastructure, rejecting privatisation and trading of water rights, enforceable limits to restore waterways, and funding iwi, hapū and marae water initiatives.
- **Sources:**
  - [Freshwater — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1LPTzVr2sdxSNdfLF2DFLikHqr2zaeuBP/view) — [full text](documents/pdf-freshwater.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

## Foreign affairs & defence

### POL54683: Focus the Defence Force on protection, disaster response and the Pacific

**Statement:** Focus the Defence Force on protection, disaster response and the Pacific  
*Summary source: policy.nz* · topics: defence-and-foreign-affairs, community-and-inclusion, defence-and-veterans, pasifika

- **Why:** This party says that Aotearoa should focus its foreign policy on peace, justice and Indigenous solidarity. New Zealand's foreign policy should be independent and aligned with the Pacific, rather than powerful countries and military alliances. Having a neutral military is an expression of mana motuhake.
- **How:** This party would prioritise the Pacific, responding to disasters and providing protection as the focus of the Defence Force.
- **Sources:**
  - ['Military Neutrality', 3 June 2026 (accessed 18 August 2026)](https://www.maoriparty.org.nz/military_neutrality) — [full text](documents/site-military-neutrality.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818013137/https://www.maoriparty.org.nz/military_neutrality)
  - [Military Neutrality — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1CCbBwB6mcxNgPTDnycPkcgvVrUDY5ZmL/view) — [full text](documents/pdf-military-neutrality.md)

### POL54684: Declare NZ a "military neutral" country

**Statement:** Declare NZ a "military neutral" country  
*Summary source: policy.nz* · topics: defence-and-foreign-affairs, defence-and-veterans, international-relations

- **Why:** This party says that NZ's foreign policy should be independent, not determined by military alliances with powerful countries fighting wars NZ should not be part of. Instead, New Zealand should ensure its military alliances protect the Pacific and uphold sovereignty. Military alliances should be reviewed, those which do not fit with values of peace and justice should be removed.
- **How:** This party would declare NZ to be a "militarily neutral" nation. All military alliances would be reviewed. The government would withdraw from alliances which undermine national or indigenous sovereignty.
- **Sources:**
  - ['Military Neutrality', 3 June 2026 (accessed 18 August 2026)](https://www.maoriparty.org.nz/military_neutrality) — [full text](documents/site-military-neutrality.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818013137/https://www.maoriparty.org.nz/military_neutrality)
  - [Military Neutrality — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1CCbBwB6mcxNgPTDnycPkcgvVrUDY5ZmL/view) — [full text](documents/pdf-military-neutrality.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL54688: Review foreign policy settings and relationships to focus on the Pacific

**Statement:** Review foreign policy settings and relationships to focus on the Pacific  
*Summary source: policy.nz* · topics: defence-and-foreign-affairs, community-and-inclusion, international-relations, pasifika

- **Why:** This party says that NZ's foreign policy shouldn't be determined by powerful countries, but should remain independent. NZ should focus on peace, justice and solidarity with indigenous people in its foreign policy. Foreign policy should uphold Māori values.
- **How:** This party would ensure foreign policy and international relationships are independent, prioritising Māori values, Pacific countries and indigenous relationships.
- **Sources:**
  - ['Military Neutrality', 3 June 2026 (accessed 18 August 2026)](https://www.maoriparty.org.nz/military_neutrality) — [full text](documents/site-military-neutrality.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818013137/https://www.maoriparty.org.nz/military_neutrality)
  - [Te Pāti Māori Statement: Aotearoa Must Stand For Peace (Press release, 2026-03-01)](https://www.scoop.co.nz/stories/PA2603/S00004/te-pati-maori-statement-aotearoa-must-stand-for-peace.htm) — [full text](documents/2026-03-01-te-pati-maori-statement-aotearoa-must-stand-for-peace.md)
  - [Military Neutrality — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1CCbBwB6mcxNgPTDnycPkcgvVrUDY5ZmL/view) — [full text](documents/pdf-military-neutrality.md)

### POL54690: Hold international war criminals to account

**Statement:** Hold international war criminals to account  
*Summary source: policy.nz* · topics: defence-and-foreign-affairs, international-relations

- **Why:** This party says that NZ should have independent foreign policy, not be influenced by powerful countries and wars in other places. Upholding human rights and ensuring war criminals receive justice on the international stage is important.
- **How:** This party would prioritise international human rights and justice for war criminals.
- **Sources:**
  - ['Military Neutrality', 3 June 2026 (accessed 18 August 2026)](https://www.maoriparty.org.nz/military_neutrality) — [full text](documents/site-military-neutrality.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818013137/https://www.maoriparty.org.nz/military_neutrality)
  - [Military Neutrality — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1CCbBwB6mcxNgPTDnycPkcgvVrUDY5ZmL/view) — [full text](documents/pdf-military-neutrality.md)

## Health, disability & whānau

### POL54647: Support Māori-led disability services

**Statement:** Support Māori-led disability services  
*Summary source: policy.nz* · topics: community-and-inclusion, te-ao-maori, disability, wellbeing-and-services, pasifika

- **Why:** This party says that disabled Māori have to fight the system to get the care they need. Making support easier to access and Māori specific will make the process of receiving care from whānau or external providers less degrading, better matching the reality for disabled Māori and their families. The focus should be on dignity, care and support, not fighting a beureaucratic system.
- **How:** This party would make support easier to access and reduce the focus on bureaucratic requirements. Funding would be provided based on what families say they need, not bureaucratic forms.
- **Sources:**
  - ['Disabilities', undated (accessed 10 August 2026)](https://www.maoriparty.org.nz/disabilities) — [full text](documents/site-disabilities.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL55000: Invest in whānau-led care for Māori children

**Statement:** Invest in whānau-led care for Māori children  
*Summary source: policy.nz* · topics: te-ao-maori, health, wellbeing-and-services, te-reo-maori-and-culture, te-tiriti-o-waitangi-and-governance, health-services

- **Why:** This party says that tamariki Māori must be protected as they are the future leaders of the country. However, current policy often results in Māori children being removed from their parents and raised in Pākeha-dominated spaces, removed from their culture
- **How:** This party would stop removing Māori children from their parents, and invest instead in whānau-led care. It would also make the Crown accountable for the harm this practice has caused.
- **Sources:**
  - ['Mokopuna Māori', undated (accessed 15 September 2026)](https://www.maoriparty.org.nz/mokopuna_m_ori) — [full text](documents/site-mokopuna-m-ori.md)
  - [Mokopuna Māori — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1dIy46mwnEg7G0oG-2r8xC5b0Be2Poegs/view) — [full text](documents/pdf-mokopuna-maori.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL55001: Improve support for Māori with disabilities

**Statement:** Improve support for Māori with disabilities  
*Summary source: policy.nz* · topics: te-ao-maori, community-and-inclusion, health, te-reo-maori-and-culture, disability, wellbeing-and-services

- **Why:** This party says disabled Māori need support which upholds their mana and whānau, but that too often the system degrades them.
- **How:** This party would support Māori-led disability services, make these services easier to access, and ensure dignity is preserved when the services are accessed
- **Sources:**
  - ['Disabilities', undated (accessed 15 September 2026)](https://www.maoriparty.org.nz/disabilities) — [full text](documents/site-disabilities.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL55066: Invest in Māori-health outcomes

**Statement:** Invest in Māori-health outcomes  
*Summary source: policy.nz* · topics: health, te-ao-maori, health-services, te-reo-maori-and-culture, te-tiriti-o-waitangi-and-governance, wellbeing-and-services

- **Why:** This party says that the health system as it currently stands fails Māori as the system does not understand Māori, and is not accountable to Māori.
- **How:** This party would re-create the Māori Health Authority, and make health services accessible, accountable, and culturally safe to Māori, while shifting the health system's focus to prevention rather than crisis response.
- **Sources:**
  - ['Health ', undated (accessed 18 August 2026)](https://www.maoriparty.org.nz/health) — [full text](documents/site-health.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818042407/https://www.maoriparty.org.nz/health)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL55067: Prioritise whānau decision making in the care of vulnerable children

**Statement:** Prioritise whānau decision making in the care of vulnerable children  
*Summary source: policy.nz* · topics: community-and-inclusion, law-justice-and-government, te-ao-maori, young-people, family-justice-and-safety, te-reo-maori-and-culture

- **Why:** This party says that being removed from their families creates negative social outcomes for Māori children. It says that whānau Māori and Māori wider networks are better suited than the Crown to support children growing up in high-risk environments.
- **How:** This party would hold the Crown accountable for damage caused by the uplift of children from their families. It would restore whānau authority and invest in whānau-led care.
- **Sources:**
  - ['Mokopuna Māori', undated (accessed 10 August 2026)](https://www.maoriparty.org.nz/mokopuna_m_ori) — [full text](documents/site-mokopuna-m-ori.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260810030203/https://www.maoriparty.org.nz/mokopuna_m_ori)
  - ['Mokopuna Māori', undated (accessed 15 September 2026)](https://www.maoriparty.org.nz/mokopuna_m_ori) — [full text](documents/site-mokopuna-m-ori.md)
  - [Mokopuna Māori — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1dIy46mwnEg7G0oG-2r8xC5b0Be2Poegs/view) — [full text](documents/pdf-mokopuna-maori.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A19: Fund a Marae Resilience Package so marae can act as civil-defence hubs

**Statement:** Fund a Marae Resilience Package so marae can act as civil-defence hubs  
*Summary source: archive* · topics: climate-adaptation, community-and-inclusion, te-ao-maori

- **Why:** The party says marae act as frontline shelters in emergencies without formal support or funding.
- **How:** The party has called for formal recognition of marae as emergency response hubs, upfront funding for emergency supplies and infrastructure, generators, water storage and communications, and long-term investment. The 2026 Climate chapter commits $100m to a 'Māori National Service Defence framework' giving hapū, iwi and urban Māori organisations the same access and resources as local government after natural disasters, and a $100m Māori Taiao relief fund to rebuild marae, urupā and papakāinga.
- **Note:** First made as a call on the government (April 2026); now part of the 2026 Climate chapter.
- **Sources:**
  - [Must Fund Marae Resilience Package Ahead Of Cyclone Vaianu (Press release, 2026-04-09)](https://www.scoop.co.nz/stories/PA2604/S00046/must-fund-marae-resilience-package-ahead-of-cyclone-vaianu.htm) — [full text](documents/2026-04-09-must-fund-marae-resilience-package-ahead-of-cyclone-vaianu.md)
  - [Climate — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1FzavJoSYNEzsVWhnS9sBMI3XENAb9-Dr/view) — [full text](documents/pdf-climate.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A26: End state care of mokopuna Māori and create a Mokopuna Māori Authority funded with ~70% of Oranga Tamariki's budget

**Statement:** End state care of mokopuna Māori and create a Mokopuna Māori Authority funded with ~70% of Oranga Tamariki's budget  
*Summary source: archive* · topics: family-justice-and-safety, te-ao-maori, community-and-inclusion

- **Why:** The party says state care removes Māori children from their whakapapa and causes harm.
- **How:** The 2026 Mokopuna Māori chapter commits to ending state care for mokopuna Māori, a Mokopuna Māori Act creating an independent authority, a three-year transition away from Oranga Tamariki with 70% of its budget (about $1 billion a year) reallocated, reinstating section 7AA, ending uplifts without whānau, hapū and iwi consent, closing youth care and protection residences, and implementing all 138 recommendations of the Royal Commission into Abuse in Care (Whanaketia).
- **Sources:**
  - [Mokopuna Māori — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1dIy46mwnEg7G0oG-2r8xC5b0Be2Poegs/view) — [full text](documents/pdf-mokopuna-maori.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A29: Free GP visits and free dental care for all whānau

**Statement:** Free GP visits and free dental care for all whānau  
*Summary source: archive* · topics: health-services, health

- **Why:** The party says Māori die seven years earlier than non-Māori.
- **How:** The party's policy tool lists free primary healthcare and free dental care for all whānau, clinics on marae, mobile health units and free delivery of medication, protecting rongoā Māori and funding more medicines through Pharmac.
- **Sources:**
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)
  - [Health Policy (Party web page (Common Crawl), 2026-09-08)](https://www.maoriparty.org.nz/health) — [full text](documents/site-health.md)

### TPM-A30: $500 million a year for kaupapa Māori mental health

**Statement:** $500 million a year for kaupapa Māori mental health  
*Summary source: archive* · topics: mental-health, health

- **Why:** The party says mental health services must be culturally safe and accountable to Māori.
- **How:** The party's policy tool lists $500 million a year for kaupapa Māori mental health, free community mental health services, and treating addiction as a health issue with double the funding for prevention, harm reduction and treatment.
- **Sources:**
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A31: Start bowel screening at 45 for everyone and 35 for Māori and Pacific peoples

**Statement:** Start bowel screening at 45 for everyone and 35 for Māori and Pacific peoples  
*Summary source: archive* · topics: public-health, health-services

- **Why:** The party says screening ages should reflect earlier onset among Māori and Pacific peoples.
- **How:** The party's policy tool lists earlier bowel screening: from age 45 for everyone and from 35 for Māori and Pacific peoples.
- **Sources:**
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A32: Move a quarter of all health and ACC funding to Māori-led systems

**Statement:** Move a quarter of all health and ACC funding to Māori-led systems  
*Summary source: archive* · topics: health-funding-and-workforce, te-ao-maori

- **Why:** The party says a health system that does not understand Māori will keep failing Māori.
- **How:** The party's policy tool states 'A quarter of all health and ACC funding moved to systems led by Māori.'
- **Sources:**
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)
  - [Health Policy (Party web page (Common Crawl), 2026-09-08)](https://www.maoriparty.org.nz/health) — [full text](documents/site-health.md)

### TPM-A33: Establish a Māori-led Mana Hauā Authority for disabled whānau and recognise unpaid care as work

**Statement:** Establish a Māori-led Mana Hauā Authority for disabled whānau and recognise unpaid care as work  
*Summary source: archive* · topics: disability, te-ao-maori

- **Why:** The party says disabled Māori should not have to fight a degrading system for support.
- **How:** The party's policy tool lists a Mana Hauā Authority led by Māori, support that keeps Tangata Hauā with their whānau, recognising unpaid care as real work, and aligning disability support with income so no one is forced into poverty. (The party's 2023 Mana Hauā policy, archived for reference, set out a fuller list.)
- **Sources:**
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)
  - [Disabilities (Party web page (Common Crawl), 2026-08-16)](https://www.maoriparty.org.nz/disabilities) — [full text](documents/site-disabilities.md)
  - [Mana Hauā Policy (Party web page (Common Crawl), 2026-04-12)](https://www.maoriparty.org.nz/mana_hau_policy?fbclid=IwAR3CGHLJh56Vtl-Z6tSNbCWdMvsw-c9-oXxW3ce9dqzZ_-e8sRnDZ5Q2vRE&ref=infoexchange.nz) — [full text](documents/site-mana-hau-policy.md)
  - [Mana Hauā (Disability) Policy (2023 document — NOT confirmed as 2026 policy) (PDF)](https://drive.google.com/file/d/1V1fVe2hhe5eNDVBuJYmxu3_07igGSiyo/view) — [full text](documents/pdf-mana-haua-policy.md)

## Housing

### POL55071: Increase the supply of housing in both the public and private sector

**Statement:** Increase the supply of housing in both the public and private sector  
*Summary source: policy.nz* · topics: housing, transport-and-infrastructure, housing-affordability, social-and-public-housing, construction

- **Why:** This party says that housing is a big driver of poverty and financial hardship in NZ. Housing is too scarce for people, even on Māori/ancestral land.
- **How:** This party would disincentivise holding rental properties vacant through tax changes, change regulations to allow more building on Māori/ancestral land. It would build and support more public and affordable homes.
- **Sources:**
  - ['Housing', undated (accessed 18 August 2026)](https://www.maoriparty.org.nz/housing) — [full text](documents/site-housing.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818013324/https://www.maoriparty.org.nz/housing)
  - [Oriini Kaipara: Prime Minister’s ‘Progress’ Ignores Housing Crisis Facing Māori And Rangatahi (Press release, 2026-01-29)](https://www.scoop.co.nz/stories/PA2601/S00115/oriini-kaipara-prime-ministers-progress-ignores-housing-crisis-facing-maori-and-rangatahi.htm) — [full text](documents/2026-01-29-oriini-kaipara-prime-ministers-progress-ignores-housing-cris.md)
  - [Housing — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1T8WiwxG9nIDnDEjyVujLZKvoNWp7i0Oh/view) — [full text](documents/pdf-housing.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A16: Freeze rents (then cap rises at inflation) and repeal no-cause evictions in the first 100 days

**Statement:** Freeze rents (then cap rises at inflation) and repeal no-cause evictions in the first 100 days  
*Summary source: archive* · topics: housing, housing-affordability

- **Why:** The party says renters need security amid a housing crisis.
- **How:** The 2026 Housing chapter says the party would freeze all rents, then allow increases only by the rate of inflation each year unless the owner makes significant improvements, and repeal no-cause evictions within its first 100 days in government. Earlier releases described this as 'universal rent control'.
- **Sources:**
  - [Oriini Kaipara: Prime Minister’s ‘Progress’ Ignores Housing Crisis Facing Māori And Rangatahi (Press release, 2026-01-29)](https://www.scoop.co.nz/stories/PA2601/S00115/oriini-kaipara-prime-ministers-progress-ignores-housing-crisis-facing-maori-and-rangatahi.htm) — [full text](documents/2026-01-29-oriini-kaipara-prime-ministers-progress-ignores-housing-cris.md)
  - [Housing — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1T8WiwxG9nIDnDEjyVujLZKvoNWp7i0Oh/view) — [full text](documents/pdf-housing.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A17: Build 2,000 papakāinga homes and allocate half of new social housing to whānau Māori

**Statement:** Build 2,000 papakāinga homes and allocate half of new social housing to whānau Māori  
*Summary source: archive* · topics: housing, social-and-public-housing, te-ao-maori

- **Why:** The party says Māori make up half of the social housing waitlist and homelessness is a Te Tiriti breach.
- **How:** The party's housing policy includes building 2,000 houses on papakāinga, radically increasing public housing investment, and allocating 50% of new social housing builds to whānau Māori; its Tāmaki Makaurau MP has a member's bill to prevent youth homelessness. The 2026 Housing chapter sets the 2,000 papakāinga homes within four years and commits to stopping the discounted sale of state houses to private investors and increasing funding for Sustaining Tenancies.
- **Sources:**
  - [Oriini Kaipara: Prime Minister’s ‘Progress’ Ignores Housing Crisis Facing Māori And Rangatahi (Press release, 2026-01-29)](https://www.scoop.co.nz/stories/PA2601/S00115/oriini-kaipara-prime-ministers-progress-ignores-housing-crisis-facing-maori-and-rangatahi.htm) — [full text](documents/2026-01-29-oriini-kaipara-prime-ministers-progress-ignores-housing-cris.md)
  - [Te Pāti Māori Rejects Move-on Orders: “We Will Not Police Our Way Out Of Homelessness" (Press release, 2026-02-22)](https://www.scoop.co.nz/stories/PA2602/S00141/te-pati-maori-rejects-move-on-orders-we-will-not-police-our-way-out-of-homelessness.htm) — [full text](documents/2026-02-22-te-pati-maori-rejects-move-on-orders-we-will-not-police-our.md)
  - [Housing — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1T8WiwxG9nIDnDEjyVujLZKvoNWp7i0Oh/view) — [full text](documents/pdf-housing.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A18: Stop all sales of freehold land to offshore foreign interests

**Statement:** Stop all sales of freehold land to offshore foreign interests  
*Summary source: archive* · topics: housing, foreign-investment, land-and-resources

- **Why:** The party says land should not be sold to overseas buyers.
- **How:** The party's housing policy includes stopping all sales of freehold land to offshore foreign interests.
- **Sources:**
  - [Oriini Kaipara: Prime Minister’s ‘Progress’ Ignores Housing Crisis Facing Māori And Rangatahi (Press release, 2026-01-29)](https://www.scoop.co.nz/stories/PA2601/S00115/oriini-kaipara-prime-ministers-progress-ignores-housing-crisis-facing-maori-and-rangatahi.htm) — [full text](documents/2026-01-29-oriini-kaipara-prime-ministers-progress-ignores-housing-cris.md)
  - [Housing — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1T8WiwxG9nIDnDEjyVujLZKvoNWp7i0Oh/view) — [full text](documents/pdf-housing.md)
  - [Mana Motuhake — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/12XBSiuPt6KrpmxoHovpWOhfrB5ngTYkY/view) — [full text](documents/pdf-mana-motuhake.md)

### TPM-A24: Repeal interest deductibility for landlords and use the money for social housing and papakāinga

**Statement:** Repeal interest deductibility for landlords and use the money for social housing and papakāinga  
*Summary source: archive* · topics: housing, government-revenue-and-finance

- **Why:** The party says restoring interest deductibility gave landlords a $3 billion tax break and pushes home ownership out of reach.
- **How:** The 2026 Housing chapter says the party would repeal interest deductibility and redistribute the $3 billion to help fund its social housing and papakāinga policies.
- **Sources:**
  - [Housing — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1T8WiwxG9nIDnDEjyVujLZKvoNWp7i0Oh/view) — [full text](documents/pdf-housing.md)

### TPM-A25: Create 'Rangatahi Ora' and a legal duty on government to end youth homelessness

**Statement:** Create 'Rangatahi Ora' and a legal duty on government to end youth homelessness  
*Summary source: archive* · topics: housing, young-people, social-and-public-housing

- **Why:** The party says half of homeless people are under 25 and agencies have no duty to prevent it.
- **How:** The 2026 Housing chapter would set up a new agency, Rangatahi Ora, with functions, duties and powers to prevent youth homelessness, and a legal 'duty to assist' requiring agencies to end or stabilise a young person's homelessness (building on Oriini Kaipara's member's bill).
- **Sources:**
  - [Housing — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1T8WiwxG9nIDnDEjyVujLZKvoNWp7i0Oh/view) — [full text](documents/pdf-housing.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)
  - [Te Pāti Māori Rejects Move-on Orders: “We Will Not Police Our Way Out Of Homelessness" (Press release, 2026-02-22)](https://www.scoop.co.nz/stories/PA2602/S00141/te-pati-maori-rejects-move-on-orders-we-will-not-police-our-way-out-of-homelessness.htm) — [full text](documents/2026-02-22-te-pati-maori-rejects-move-on-orders-we-will-not-police-our.md)

## Justice

### POL55070: Move towards restorative justice

**Statement:** Move towards restorative justice  
*Summary source: policy.nz* · topics: law-justice-and-government, te-ao-maori, civil-justice, family-justice-and-safety, criminal-justice, te-reo-maori-and-culture

- **Why:** This party says that the current justice system disproportionately criminalises and punishes Māori. Therefore, recreating the justice system so it is equitable for all is vital.
- **How:** This party would create a Māori-led justice authority, prevent laws from punishing poverty and survival, and move away from mass imprisonment.
- **Note:** policy.nz cites the party's 'Justice' web page (blocked); the Justice chapter of the party's 2026 manifesto (Google Drive PDF) was retrieved.
- **Sources:**
  - ['Justice', undated (accessed 18 August 2026)](https://www.maoriparty.org.nz/justice) — [full text](documents/site-justice.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818042919/https://www.maoriparty.org.nz/justice)
  - [Justice — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx/view) — [full text](documents/pdf-justice-1phb4pna7fe9ipj5sxhrrcrmgywm-mhax.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL55283: Abolish prisons by 2040

**Statement:** Abolish prisons by 2040  
*Summary source: policy.nz* · topics: law-justice-and-government, te-ao-maori, criminal-justice, te-reo-maori-and-culture

- **Why:** This party says that young Māori are regularly criminalised early in their lives, and even once they get out, often end up re-offending. This can be seen as how Māori men make up half the male prison population, while Māori women have one of the highest incarceration rates in the world. This shows that the prison system is failing Māori, and major reform is needed.
- **How:** This party would abolish prisons by 2040, and replace them with restorative, community-based, tikanga-grounded alternatives. This will reduce harm while addressing the underlying causes of offending, and prevent crime rather than punishing offenders.
- **Sources:**
  - ['Justice' (PDF), undated (accessed 14 October 2026)](https://drive.google.com/file/d/1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx/view) — [full text](documents/pdf-justice-1phb4pna7fe9ipj5sxhrrcrmgywm-mhax.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20261013210716/https://drive.google.com/file/d/1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx/view)
  - [“If You’re Not Trying To Abolish Prisons In Aotearoa, What Are You Doing In Parliament?” - Rawiri Waititi (Press release, 2026-01-28)](https://www.scoop.co.nz/stories/PA2601/S00112/if-youre-not-trying-to-abolish-prisons-in-aotearoa-what-are-you-doing-in-parliament-rawiri-waititi.htm) — [full text](documents/2026-01-28-if-youre-not-trying-to-abolish-prisons-in-aotearoa-what-are.md)

### TPM-A13: Create an independent Māori Justice Authority funded from half of the Corrections, Police and Courts budgets

**Statement:** Create an independent Māori Justice Authority funded from half of the Corrections, Police and Courts budgets  
*Summary source: archive* · topics: criminal-justice, te-ao-maori

- **Why:** The party says the justice system was imposed on Māori, breaches Te Tiriti and over-incarcerates Māori.
- **How:** This party would establish a tikanga-led Independent Māori Justice Authority with real decision-making power, funded by reallocating 50% of Vote Corrections, 50% of Vote Police and 50% of Vote Courts, and invest in kaupapa Māori legal aid and community law services.
- **Sources:**
  - [Justice — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx/view) — [full text](documents/pdf-justice-1phb4pna7fe9ipj5sxhrrcrmgywm-mhax.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A14: Repeal three strikes, gang and bail laws; raise the age of criminal responsibility to 16

**Statement:** Repeal three strikes, gang and bail laws; raise the age of criminal responsibility to 16  
*Summary source: archive* · topics: criminal-justice, young-people

- **Why:** The party says these laws discriminate against Māori and criminalise rangatahi early.
- **How:** This party would repeal three-strikes legislation, gangs legislation, the Sentencing (Reform) Amendment Act and the Bail Amendment Act, raise the age of criminal responsibility from 10 to 16, extend the Clean Slate Act to custodial sentences, require police body cameras, replace the IPCA with a Māori-grounded oversight body and reinstate funding for cultural (s27) reports.
- **Sources:**
  - [Justice — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx/view) — [full text](documents/pdf-justice-1phb4pna7fe9ipj5sxhrrcrmgywm-mhax.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A15: Decriminalise drug use and close military-style bootcamps and youth justice residences

**Statement:** Decriminalise drug use and close military-style bootcamps and youth justice residences  
*Summary source: archive* · topics: criminal-justice, health, young-people

- **Why:** The party says drug use is a health issue and youth residences harm rangatahi.
- **How:** This party would overhaul the Misuse of Drugs Act to treat drug use as a health issue and wipe convictions for use and possession, close military-style bootcamps immediately and youth justice residences by 2030, end solitary confinement as punishment, and (under 'electoral justice') restore voting rights for all people in Corrections facilities and lower the voting age to 16.
- **Sources:**
  - [Justice — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx/view) — [full text](documents/pdf-justice-1phb4pna7fe9ipj5sxhrrcrmgywm-mhax.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

## Kai, cost of living & economy

### POL54649: Protect Māori food systems

**Statement:** Protect Māori food systems  
*Summary source: policy.nz* · topics: economy, te-ao-maori, agriculture, land-and-resources, wellbeing-and-services, te-tiriti-o-waitangi-and-governance

- **Why:** This party says that many families are going hungry, even though Aotearoa grows enough food to feed everyone. Scarcity is a product of system failure, rather than lack of food. Protecting Māori food sources and agriculture will ensure food is healthy and affordable.
- **How:** This party would reject genetic engineering, look after seed sovereignty, protect the WAI262 Waitangi Tribunal claim over flora and fauna. Increasing access to land for food production and investing in regenerative agriculture and community food systems would get affordable food to people who need it.
- **Note:** policy.nz cites the party's June 2026 'Kai Sovereignty' web page (blocked); the September 2026 Kai Sovereignty Policy PDF is the party's later full policy.
- **Sources:**
  - ['Kai Sovereignty', 6 June 2026 (accessed 10 August 2026)](https://www.maoriparty.org.nz/kai_sovereignt) — [full text](documents/site-kai-sovereignt.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260810030114/https://www.maoriparty.org.nz/kai_sovereignt)
  - [Kai Sovereignty Policy 2026 (PDF)](https://img.scoop.co.nz/media/pdfs/2609/KAI_SOVEREIGNTY_POLICY_2026.pdf) — [full text](documents/pdf-kai-sovereignty-policy-2026.md)
  - [Te Pāti Māori Launches Kai Sovereignty Policy (Press release, 2026-09-21)](https://www.scoop.co.nz/stories/PA2609/S00211/te-pati-maori-launches-kai-sovereignty-policy.htm) — [full text](documents/2026-09-21-te-pati-maori-launches-kai-sovereignty-policy.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL54650: Support Māori-owned supermarkets and kai sellers

**Statement:** Support Māori-owned supermarkets and kai sellers  
*Summary source: policy.nz* · topics: te-ao-maori, incomes-and-employment, economy, wellbeing-and-services, prices, te-tiriti-o-waitangi-and-governance

- **Why:** This party says that too many families are going hungry, even though NZ grows enough food to feed everyone. Scarcity is a product of system failure, rather than lack of food. Ending corporate control of food chains will make it easier for people to access food when they need it.
- **How:** This party would support local kai sellers and Māori-owned supermarkets over large corporate supermarket chains.
- **Sources:**
  - ['Kai Sovereignty', 6 June 2026 (accessed 10 August 2026)](https://www.maoriparty.org.nz/kai_sovereignt) — [full text](documents/site-kai-sovereignt.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260810030114/https://www.maoriparty.org.nz/kai_sovereignt)
  - [Kai Sovereignty Policy 2026 (PDF)](https://img.scoop.co.nz/media/pdfs/2609/KAI_SOVEREIGNTY_POLICY_2026.pdf) — [full text](documents/pdf-kai-sovereignty-policy-2026.md)
  - [Te Pāti Māori Launches Kai Sovereignty Policy (Press release, 2026-09-21)](https://www.scoop.co.nz/stories/PA2609/S00211/te-pati-maori-launches-kai-sovereignty-policy.htm) — [full text](documents/2026-09-21-te-pati-maori-launches-kai-sovereignty-policy.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL55087: Reduce the cost of living

**Statement:** Reduce the cost of living  
*Summary source: policy.nz* · topics: incomes-and-employment, transport-and-infrastructure, housing, jobs-and-employment, prices, public-transport-cycling-and-walking

- **Why:** This party says that no one should have to choose between food, rent, power, transport or other necessities. The economy should work for the people.
- **How:** This party would lift incomes, strengthen welfare, and support cost of living relief efforts, such as reducing transport costs.
- **Sources:**
  - ['Cost of Living', 3 June 2026 (accessed 18 August 2026)](https://www.maoriparty.org.nz/cost_of_living) — [full text](documents/site-cost-of-living.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818043207/https://www.maoriparty.org.nz/cost_of_living)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### POL55088: Support the Māori economy

**Statement:** Support the Māori economy  
*Summary source: policy.nz* · topics: economy, incomes-and-employment, te-ao-maori, economic-development-and-industry, jobs-and-employment, te-reo-maori-and-culture

- **Why:** This party says that most of Aotearoa's wealth has been extracted from its indigenous people. For Māori to flourish on their own terms, building the Māori economy is vital.
- **How:** This party would create funds to support Māori enterprises, for the long-term growth of Māori wealth.
- **Sources:**
  - ['Economic development ', undated (accessed 18 August 2026)](https://www.maoriparty.org.nz/economic_development) — [full text](documents/site-economic-development.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818043029/https://www.maoriparty.org.nz/economic_development)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A06: $100 million Community Kai Fund and $100 million for regenerative Māori agriculture (Mātai Ahuwhenua)

**Statement:** $100 million Community Kai Fund and $100 million for regenerative Māori agriculture (Mātai Ahuwhenua)  
*Summary source: archive* · topics: agriculture, community-and-inclusion, te-ao-maori

- **Why:** The party says whānau should be able to grow their own kai rather than depend on food parcels and the supermarket duopoly.
- **How:** This party would set up a $100 million Community Kai Fund for home gardens, marae māra kai and community food farms, invest an extra $100 million in Mātai Ahuwhenua for regenerative and diversified Māori land-based production, and protect Māori seed, mātauranga and Indigenous plant whakapapa including through WAI 262 protections. The Climate chapter separately commits $300 million to Mātai Ahuwhenua and a five-year phase-out of synthetic fertilisers; the party's policy tool states '$400 million to help Māori farmers move to regenerative farming'.
- **Sources:**
  - [Kai Sovereignty Policy 2026 (PDF)](https://img.scoop.co.nz/media/pdfs/2609/KAI_SOVEREIGNTY_POLICY_2026.pdf) — [full text](documents/pdf-kai-sovereignty-policy-2026.md)
  - [Te Pāti Māori Launches Kai Sovereignty Policy (Press release, 2026-09-21)](https://www.scoop.co.nz/stories/PA2609/S00211/te-pati-maori-launches-kai-sovereignty-policy.htm) — [full text](documents/2026-09-21-te-pati-maori-launches-kai-sovereignty-policy.md)
  - [Climate — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1FzavJoSYNEzsVWhnS9sBMI3XENAb9-Dr/view) — [full text](documents/pdf-climate.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A20: Freeze MPs' pay rises and suspend fuel excise tax (cost-of-living calls)

**Statement:** Freeze MPs' pay rises and suspend fuel excise tax (cost-of-living calls)  
*Summary source: archive* · topics: prices, parliament-and-democracy

- **Why:** The party says politicians should not get pay rises while whānau struggle, and fuel excise adds about $35 to a 50-litre fill.
- **How:** The party has called for an immediate freeze on pay rises for MPs, Ministers and the Prime Minister (with a deeper cut for Ministers and the PM), and for the immediate suspension of fuel excise tax.
- **Note:** Made as calls on the current government in March/April 2026.
- **Sources:**
  - [Te Pāti Māori Calls For Freeze On MP Pay Rises (Press release, 2026-04-02)](https://www.scoop.co.nz/stories/PA2604/S00015/te-pati-maori-calls-for-freeze-on-mp-pay-rises.htm) — [full text](documents/2026-04-02-te-pati-maori-calls-for-freeze-on-mp-pay-rises.md)
  - [Te Pāti Māori Calls For Urgent Suspension Of Fuel Excise Tax To Relieve Pressure On Whānau (Press release, 2026-03-18)](https://www.scoop.co.nz/stories/PA2603/S00110/te-pati-maori-calls-for-urgent-suspension-of-fuel-excise-tax-to-relieve-pressure-on-whanau.htm) — [full text](documents/2026-03-18-te-pati-maori-calls-for-urgent-suspension-of-fuel-excise-tax.md)

### TPM-A21: Lift the minimum wage to the living wage ($28.95 an hour) and end youth rates

**Statement:** Lift the minimum wage to the living wage ($28.95 an hour) and end youth rates  
*Summary source: archive* · topics: wages-and-working-conditions, incomes-and-employment

- **Why:** The party says no one should be paid less than what it costs to live.
- **How:** The party's policy tool (from its 2026 manifesto) says the minimum wage would go 'straight up to the living wage', $28.95 an hour, and that youth and starting-out rates would end.
- **Sources:**
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A22: Double baseline benefits, remove sanctions and work-test obligations, cancel benefit debt

**Statement:** Double baseline benefits, remove sanctions and work-test obligations, cancel benefit debt  
*Summary source: archive* · topics: benefits, tax-and-income-support

- **Why:** The party says welfare should not punish whānau for being poor.
- **How:** The party's policy tool lists doubling baseline benefits, removing sanctions and work-test obligations, cancelling benefit debt owed to the Crown, hardship grants that do not need to be repaid, and Special Needs Grants that cover cultural costs such as tangihanga and unveilings.
- **Sources:**
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)
  - [Cost of living (Party web page (Common Crawl), 2026-09-08)](https://www.maoriparty.org.nz/cost_of_living) — [full text](documents/site-cost-of-living.md)

### TPM-A23: Free public transport for tamariki, students and Community Services Card holders, then for everyone within five years

**Statement:** Free public transport for tamariki, students and Community Services Card holders, then for everyone within five years  
*Summary source: archive* · topics: public-transport-cycling-and-walking, prices

- **Why:** The party says transport costs are a major part of the cost of living.
- **How:** The party's policy tool says public transport would be free immediately for tamariki, students (including tertiary) and Community Services Card holders, half price for everyone else, and free for everyone within five years.
- **Sources:**
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)
  - [Cost of living (Party web page (Common Crawl), 2026-09-08)](https://www.maoriparty.org.nz/cost_of_living) — [full text](documents/site-cost-of-living.md)

### TPM-A44: A quarter of government contracts for Māori businesses and a $4.5 billion Oranga Whenua Oranga Tangata Fund

**Statement:** A quarter of government contracts for Māori businesses and a $4.5 billion Oranga Whenua Oranga Tangata Fund  
*Summary source: archive* · topics: economic-development-and-industry, business-support, te-ao-maori

- **Why:** The party says Māori prosperity needs Māori-led institutions and funds.
- **How:** The party's policy tool says a quarter of all government spending on contracts would go to businesses fully owned and governed by Māori, plus a $4.5 billion Oranga Whenua Oranga Tangata Fund for Māori land, marae and business.
- **Sources:**
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)
  - [Economic development (Party web page (Common Crawl), 2026-09-08)](https://www.maoriparty.org.nz/economic_development) — [full text](documents/site-economic-development.md)

### TPM-A46: Protect the right to sell homegrown and homekill kai locally

**Statement:** Protect the right to sell homegrown and homekill kai locally  
*Summary source: archive* · topics: agriculture, prices

- **Why:** The party says communities should be able to feed each other.
- **How:** The party's policy tool lists 'The right to sell homegrown and homekill kai locally', including roadside kai, 'without interference or tax', and more land set aside for rural and urban food farms.
- **Sources:**
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)
  - [Kai Sovereignty (Party web page (Common Crawl), 2026-08-16)](https://www.maoriparty.org.nz/kai_sovereignt) — [full text](documents/site-kai-sovereignt.md)

## Tax

### POL54812: Make the first $30,000 earned tax-free

**Statement:** Make the first $30,000 earned tax-free  
*Summary source: policy.nz* · topics: incomes-and-employment, economy, tax-and-income-support, government-revenue-and-finance, wages-and-working-conditions

- **Why:** This party says that argues that Aotearoa's tax system is highly unequal, given that wages are taxed more than income from wealth. Lower-earning people have less disposable income; this party seeks to reduce how much this group is taxed.
- **How:** This party would establish six bands of income tax. The first $30,000 earned would be tax-free, while income between $30,001 and $60,000 would have a tax rate of 15%. Those earning between $60,001 and $90,001 would have a tax rate of 33%; $ 90,001- $ 180,000 would be 39%; between $180,000 and $300,000, 42%; and above $300,000, the tax rate would be 48%.
- **Sources:**
  - ['A Kiwi Tax Plan' (PDF), 26 August 2026 (accessed 31 August 2026)](https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf) — [full text](documents/pdf-a-kiwi-tax-plan.md)
  - [Pūtea Back In Your Pocket: TPM Unveils A Kiwi Tax Plan For Everyone (Press release, 2026-08-26)](https://www.scoop.co.nz/stories/PA2608/S00238/putea-back-in-your-pocket-tpm-unveils-a-kiwi-tax-plan-for-everyone.htm) — [full text](documents/2026-08-26-putea-back-in-your-pocket-tpm-unveils-a-kiwi-tax-plan-for-ev.md)
  - [Tax — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/11dbbk3BTNigHUb4xANPnTKxb2TC9dAgg/view) — [full text](documents/pdf-tax.md)
  - [Tax Policy (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/tax) — [full text](documents/site-tax.md)

### POL54938: Remove GST costs from kai

**Statement:** Remove GST costs from kai  
*Summary source: policy.nz* · topics: incomes-and-employment, tax-and-income-support, prices

- **Why:** This party says that food is too expensive for lower income people.
- **How:** This party would create an 'Income Tax Kai Credit' equivalent to eight weeks of free food each year. Only people earning less than $60,000 (64 per cent of the population) would be eligible for this kai credit.
- **Sources:**
  - ['A Kiwi Tax Plan' (PDF), 26 August 2026 (accessed 31 August 2026)](https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf) — [full text](documents/pdf-a-kiwi-tax-plan.md)
  - [Pūtea Back In Your Pocket: TPM Unveils A Kiwi Tax Plan For Everyone (Press release, 2026-08-26)](https://www.scoop.co.nz/stories/PA2608/S00238/putea-back-in-your-pocket-tpm-unveils-a-kiwi-tax-plan-for-everyone.htm) — [full text](documents/2026-08-26-putea-back-in-your-pocket-tpm-unveils-a-kiwi-tax-plan-for-ev.md)
  - [Kai Sovereignty Policy 2026 (PDF)](https://img.scoop.co.nz/media/pdfs/2609/KAI_SOVEREIGNTY_POLICY_2026.pdf) — [full text](documents/pdf-kai-sovereignty-policy-2026.md)
  - [Tax — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/11dbbk3BTNigHUb4xANPnTKxb2TC9dAgg/view) — [full text](documents/pdf-tax.md)
  - [Tax Policy (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/tax) — [full text](documents/site-tax.md)

### POL54939: Implement a targeted wealth tax starting from 1.5 percent

**Statement:** Implement a targeted wealth tax starting from 1.5 percent  
*Summary source: policy.nz* · topics: incomes-and-employment, economy, tax-and-income-support, government-revenue-and-finance

- **Why:** This party says that wealth inequality is currently extremely high. Tax reform is required to address wealth inequality, build social cohesion, and fund public services.
- **How:** This party would tax the wealth of those whose net wealth is higher than $2 million. For those whose net wealth is between $2 million and $5 million, 1.5 percent of the wealth will be taxed. Between $5 million and $10 million, this number will rise to 2 percent, and above $10 million, it will be 2.5 percent.
- **Sources:**
  - ['A Kiwi Tax Plan' (PDF), 26 August 2026 (accessed 31 August 2026)](https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf) — [full text](documents/pdf-a-kiwi-tax-plan.md)
  - [Pūtea Back In Your Pocket: TPM Unveils A Kiwi Tax Plan For Everyone (Press release, 2026-08-26)](https://www.scoop.co.nz/stories/PA2608/S00238/putea-back-in-your-pocket-tpm-unveils-a-kiwi-tax-plan-for-everyone.htm) — [full text](documents/2026-08-26-putea-back-in-your-pocket-tpm-unveils-a-kiwi-tax-plan-for-ev.md)
  - [Tax — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/11dbbk3BTNigHUb4xANPnTKxb2TC9dAgg/view) — [full text](documents/pdf-tax.md)
  - [Tax Policy (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/tax) — [full text](documents/site-tax.md)

### POL54940: Ensure tax fairness by raising corporate tax rate

**Statement:** Ensure tax fairness by raising corporate tax rate  
*Summary source: policy.nz* · topics: incomes-and-employment, economy, tax-and-income-support, business-support, government-revenue-and-finance

- **Why:** This party says that Aotearoa's current tax regime is unequal and punishes the lowest earners while rewarding wealth accumulation and property speculation. One aspect is that companies are taxed too little and are incentivised to avoid paying tax they do pay.
- **How:** This party would increase the corporate tax rate from 28 percent to 33 percent. Additionally, the party would invest $1b in eliminating tax avoidance practices.
- **Sources:**
  - ['A Kiwi Tax Plan' (PDF), 26 August 2026 (accessed 31 August 2026)](https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf) — [full text](documents/pdf-a-kiwi-tax-plan.md)
  - [Tax — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/11dbbk3BTNigHUb4xANPnTKxb2TC9dAgg/view) — [full text](documents/pdf-tax.md)
  - [Tax Policy (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/tax) — [full text](documents/site-tax.md)

### POL54941: Introduce a 5 percent tax on profit transferred overseas

**Statement:** Introduce a 5 percent tax on profit transferred overseas  
*Summary source: policy.nz* · topics: incomes-and-employment, economy, tax-and-income-support, business-support, foreign-investment, government-revenue-and-finance

- **Why:** This party says that companies should not be able to transfer money extracted from NZ offshore without paying taxes.
- **How:** This party would introduce a tax of 5 percent on the value of profits sent overseas from NZ.
- **Sources:**
  - ['A Kiwi Tax Plan' (PDF), 26 August 2026 (accessed 31 August 2026)](https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf) — [full text](documents/pdf-a-kiwi-tax-plan.md)
  - [Tax — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/11dbbk3BTNigHUb4xANPnTKxb2TC9dAgg/view) — [full text](documents/pdf-tax.md)
  - [Tax Policy (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/tax) — [full text](documents/site-tax.md)

### POL54942: Support productive use of land with a land banking tax

**Statement:** Support productive use of land with a land banking tax  
*Summary source: policy.nz* · topics: housing, economy, incomes-and-employment, housing-affordability, government-revenue-and-finance, tax-and-income-support

- **Why:** This party says that too often land is used unproductively, resulting in land banking. For example, there are 111,700 empty houses in New Zealand.
- **How:** This party would introduce a land banking tax of 33 percent on land which is not being used. It would also introduce a 2 percent vacant house tax to encourage homes to be filled faster.
- **Sources:**
  - ['A Kiwi Tax Plan' (PDF), 26 August 2026 (accessed 31 August 2026)](https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf) — [full text](documents/pdf-a-kiwi-tax-plan.md)
  - [Tax — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/11dbbk3BTNigHUb4xANPnTKxb2TC9dAgg/view) — [full text](documents/pdf-tax.md)
  - [Tax Policy (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/tax) — [full text](documents/site-tax.md)

### POL54943: Implement a 5 percent stamp duty on residential sales

**Statement:** Implement a 5 percent stamp duty on residential sales  
*Summary source: policy.nz* · topics: housing, incomes-and-employment, economy, housing-affordability, tax-and-income-support, government-revenue-and-finance

- **Why:** This party says Aotearoa's current tax regime is unequal and currently punishes the lowest earners while rewarding wealth accumulation and property speculation. To create lower taxes for the lowest earners, revenue is needed.
- **How:** This party would create a tax of 5 percent of a home's value, paid by the people buying the home.  First-home buyers buying a property worth less than $1 million would be exempt.
- **Sources:**
  - ['A Kiwi Tax Plan' (PDF), 26 August 2026 (accessed 31 August 2026)](https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf) — [full text](documents/pdf-a-kiwi-tax-plan.md)
  - [Tax — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/11dbbk3BTNigHUb4xANPnTKxb2TC9dAgg/view) — [full text](documents/pdf-tax.md)
  - [Tax Policy (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/tax) — [full text](documents/site-tax.md)

### POL54968: Align tax and environmental policy

**Statement:** Align tax and environmental policy  
*Summary source: policy.nz* · topics: incomes-and-employment, environment, economy, tax-and-income-support, climate-adaptation, government-revenue-and-finance

- **Why:** This party says that Aotearoa's current tax regime is unequal and currently punishes the lowest earners while rewarding wealth accumulation, property speculation and environmental extraction.
- **How:** This party would ensure that tax policy and environmental policy are aligned so that tax policy also protects Te Taiao. In addition, the party would ensure future environmental taxes do not disproportionately target low-income households.
- **Sources:**
  - ['A Kiwi Tax Plan' (PDF), 26 August 2026 (accessed 31 August 2026)](https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf) — [full text](documents/pdf-a-kiwi-tax-plan.md)
  - [Tax — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/11dbbk3BTNigHUb4xANPnTKxb2TC9dAgg/view) — [full text](documents/pdf-tax.md)
  - [Tax Policy (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/tax) — [full text](documents/site-tax.md)

### TPM-A01: Introduce a 2% Vacant House Tax

**Statement:** Introduce a 2% Vacant House Tax  
*Summary source: archive* · topics: housing, government-revenue-and-finance

- **Why:** The party says 111,700 homes across Aotearoa are empty while whānau need housing.
- **How:** This party would implement a Vacant House Tax of 2% as part of its Kiwi Tax Plan.
- **Sources:**
  - [A Kiwi Tax Plan — Te Pāti Māori Policy Manifesto 2026: Tax (PDF)](https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf) — [full text](documents/pdf-a-kiwi-tax-plan.md)
  - [Pūtea Back In Your Pocket: TPM Unveils A Kiwi Tax Plan For Everyone (Press release, 2026-08-26)](https://www.scoop.co.nz/stories/PA2608/S00238/putea-back-in-your-pocket-tpm-unveils-a-kiwi-tax-plan-for-everyone.htm) — [full text](documents/2026-08-26-putea-back-in-your-pocket-tpm-unveils-a-kiwi-tax-plan-for-ev.md)
  - [Tax — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/11dbbk3BTNigHUb4xANPnTKxb2TC9dAgg/view) — [full text](documents/pdf-tax.md)
  - [Housing — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1T8WiwxG9nIDnDEjyVujLZKvoNWp7i0Oh/view) — [full text](documents/pdf-housing.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A02: Invest $1 billion in Inland Revenue, the SFO, the FMA and the Financial Intelligence Unit to fight tax evasion

**Statement:** Invest $1 billion in Inland Revenue, the SFO, the FMA and the Financial Intelligence Unit to fight tax evasion  
*Summary source: archive* · topics: government-revenue-and-finance, criminal-justice

- **Why:** The party says aggressive tax avoidance must be eliminated so everyone pays their fair share.
- **How:** This party would increase investment by $1 billion across IRD, the Serious Fraud Office, the Financial Markets Authority and the NZ Financial Intelligence Unit.
- **Sources:**
  - [A Kiwi Tax Plan — Te Pāti Māori Policy Manifesto 2026: Tax (PDF)](https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf) — [full text](documents/pdf-a-kiwi-tax-plan.md)
  - [Tax — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/11dbbk3BTNigHUb4xANPnTKxb2TC9dAgg/view) — [full text](documents/pdf-tax.md)

## Te Tiriti, constitution & democracy

### POL54795: Make Waitangi Tribunal recommendations binding

**Statement:** Make Waitangi Tribunal recommendations binding  
*Summary source: policy.nz* · topics: te-ao-maori, law-justice-and-government, te-reo-maori-and-culture, civil-justice, te-tiriti-o-waitangi-and-governance

- **Why:** This party says that currently the government currently can ignore recommendations given by the Waitangi Tribunal. The party says this results in there being no accountability when Te Tiriti is breached.
- **How:** This party would will make Waitangi Tribunal recommendations binding by law.
- **Sources:**
  - ['Te Pāti Māori will make the Waitangi Tribunal Recommendation Binding ', 6 August 2026 (accessed 11 August 2026)](https://www.scoop.co.nz/stories/PA2608/S00044/te-pati-maori-will-make-the-waitangi-tribunal-recommendations-binding.htm?_gl=1%2A161whb7%2A_gcl_au%2AMTk4NTg5NzkzNi4xNzg2NDAxNDc5%2A_ga%2AMTA2ODM2Mjg3Mi4xNzg2NDAxNDc5%2A_ga_GGVMM3MB82%2AczE3ODY0MTg1OTkkbzIkZzAkdDE3ODY0MTg2MDIkajU3JGwwJGgw) — [full text](documents/2026-08-06-te-pati-maori-will-make-the-waitangi-tribunal-recommendation.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260811032410/https://www.scoop.co.nz/stories/PA2608/S00044/te-pati-maori-will-make-the-waitangi-tribunal-recommendations-binding.htm?_gl=1%2A161whb7%2A_gcl_au%2AMTk4NTg5NzkzNi4xNzg2NDAxNDc5%2A_ga%2AMTA2ODM2Mjg3Mi4xNzg2NDAxNDc5%2A_ga_GGVMM3MB82%2AczE3ODY0MTg1OTkkbzIkZzAkdDE3ODY0MTg2MDIkajU3JGwwJGgw)
  - [Te Tiriti Entrenchment Policy 2026 (PDF)](https://img.scoop.co.nz/media/pdfs/2609/TIRITI_ENTRENCHMENT_POLICY.pdf) — [full text](documents/pdf-tiriti-entrenchment-policy.md)
  - [Te Tiriti Entrenchment — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/1esXEFN0eAOtJFcdIYwYOzaVkyFtEx5vE/view) — [full text](documents/pdf-te-tiriti-entrenchment.md)
  - [Te Tiriti Entrenchment (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/te_tiriti_entrenchment) — [full text](documents/site-te-tiriti-entrenchment.md)

### POL54802: Establish an independent commissioner for Te Tiriti o Waitangi

**Statement:** Establish an independent commissioner for Te Tiriti o Waitangi  
*Summary source: policy.nz* · topics: te-ao-maori, law-justice-and-government, te-tiriti-o-waitangi-and-governance, parliament-and-democracy

- **Why:** This party says that that Te Tiriti has regularly been breached by different governments, meaning regulatory powers are needed to prevent future breaches.
- **How:** This party would establish an independent commissioner, who would act as a watchdog for potential breaches of Te Tiriti o Waitangi. It would also advise parliament to ensure Te Tiriti is central in all law-making.
- **Note:** This commitment dates from February 2025; the September 2026 Entrenchment Policy proposes an independent Te Tiriti Commission (see POL54917).
- **Sources:**
  - ['Te Pāti Māori Vow To Protect Te Tiriti With Establishment Of Independent Commissioner For Te Tiriti O Waitangi', 4 February 2025 (accessed 31 August 2026)](https://www.scoop.co.nz/stories/PA2502/S00022/te-pati-maori-vow-to-protect-te-tiriti-with-establishment-of-independent-commissioner-for-te-tiriti-o-waitangi.htm) — [full text](documents/2025-02-04-te-pati-maori-vow-to-protect-te-tiriti-with-establishment-of.md)

### POL54917: Establish an independent Te Tiriti Commission

**Statement:** Establish an independent Te Tiriti Commission  
*Summary source: policy.nz* · topics: te-ao-maori, te-tiriti-o-waitangi-and-governance, te-reo-maori-and-culture

- **Why:** This party says that says that te Triti is the constitutional foundation of Aotearoa, but how te Tiriti is treated depends on the government of the day. Therefore, a crown watchdog regarding the implementation of te Tiriti is required.
- **How:** This party would will create a Te Tiriti commission. The commission would investigate Crown activities which may breach Te Tiriti, report to Parliament on breaches, stop decisions or actions which breach Te Tiriti and require remedial action from the Crown when such breaches occur. The commission would use a Te Tiriti compliance order to prevent the government from continuing the activity. Such orders could only be overturned by the High Court.
- **Sources:**
  - ['Te Tiriti Entrenchment Policy', undated (accessed 09 September 2026)](https://img.scoop.co.nz/media/pdfs/2609/TIRITI_ENTRENCHMENT_POLICY.pdf) — [full text](documents/pdf-tiriti-entrenchment-policy.md)
  - [Te Pāti Māori Launches Te Tiriti Entrenchment Policy (Press release, 2026-09-01)](https://www.scoop.co.nz/stories/PA2609/S00008/te-pati-maori-launches-te-tiriti-entrenchment-policy.htm) — [full text](documents/2026-09-01-te-pati-maori-launches-te-tiriti-entrenchment-policy.md)
  - [TPM To Entrench Te Tiriti: Government’s Tiriti Purge Is Constitutional Vandalism (Press release, 2026-05-15)](https://www.scoop.co.nz/stories/PA2605/S00134/tpm-to-entrench-te-tiriti-governments-tiriti-purge-is-constitutional-vandalism.htm) — [full text](documents/2026-05-15-tpm-to-entrench-te-tiriti-governments-tiriti-purge-is-consti.md)
  - [Te Tiriti Entrenchment — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/1esXEFN0eAOtJFcdIYwYOzaVkyFtEx5vE/view) — [full text](documents/pdf-te-tiriti-entrenchment.md)
  - [Te Tiriti Entrenchment (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/te_tiriti_entrenchment) — [full text](documents/site-te-tiriti-entrenchment.md)

### POL54919: Implement the United Nations Declaration on the Rights of Indigenous Peoples

**Statement:** Implement the United Nations Declaration on the Rights of Indigenous Peoples  
*Summary source: policy.nz* · topics: te-ao-maori, defence-and-foreign-affairs, te-reo-maori-and-culture, international-relations, te-tiriti-o-waitangi-and-governance

- **Why:** This party says that Aotearoa has endorsed the United Nations Declaration on the Rights of Indigenous Peoples but has not done anything domestically to implement it.
- **How:** This party would fund and develop a national action plan to implement the declaration.
- **Sources:**
  - ['Te Tiriti Entrenchment Policy', undated (accessed 09 September 2026)](https://img.scoop.co.nz/media/pdfs/2609/TIRITI_ENTRENCHMENT_POLICY.pdf) — [full text](documents/pdf-tiriti-entrenchment-policy.md)
  - [Te Pāti Māori Launches Te Tiriti Entrenchment Policy (Press release, 2026-09-01)](https://www.scoop.co.nz/stories/PA2609/S00008/te-pati-maori-launches-te-tiriti-entrenchment-policy.htm) — [full text](documents/2026-09-01-te-pati-maori-launches-te-tiriti-entrenchment-policy.md)
  - [Te Tiriti Entrenchment — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/1esXEFN0eAOtJFcdIYwYOzaVkyFtEx5vE/view) — [full text](documents/pdf-te-tiriti-entrenchment.md)
  - [Te Tiriti Entrenchment (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/te_tiriti_entrenchment) — [full text](documents/site-te-tiriti-entrenchment.md)

### POL54921: Convene a Māori constitutional convention as laid out in Matike Mai

**Statement:** Convene a Māori constitutional convention as laid out in Matike Mai  
*Summary source: policy.nz* · topics: te-ao-maori, law-justice-and-government, te-reo-maori-and-culture, te-tiriti-o-waitangi-and-governance, parliament-and-democracy

- **Why:** This party says that Māori constitutional sovereignty comes from He Whakaputanga o te Rangatiratanga o Nu Tireni (the 1835 declaration of independence). However, with no written constitution, Māori authority is not constitutionally enshrined as it should be. The Mātike Mai project, which was founded in 2010 to strengthen the independence of iwi and hapū, is underfunded to resource such a transition.
- **How:** This party would convene a Māori constitutional convention which will start dialogue with tangata Tiriti and both local and central government regarding New Zealand's constitutional future. It would set 2040 as a target date for constitutional change in New Zealand, and estimates that this policy would cost $220m. This would follow the recommendations of the Matike Mai report.
- **Note:** A 2023 Te Pāti Māori 'Mana Motuhake Policy' PDF is archived for reference (documents/pdf-mana-motuhake-1y9gti2vgayijygamaq5e-wvclylcoytl.md); it predates 2026 and is not cited as 2026 policy.
- **Sources:**
  - ['Te Tiriti Entrenchment Policy', undated (accessed 09 September 2026)](https://img.scoop.co.nz/media/pdfs/2609/TIRITI_ENTRENCHMENT_POLICY.pdf) — [full text](documents/pdf-tiriti-entrenchment-policy.md)
  - ['Mana Motuhake', undated (accessed 18 August 2026)](https://www.maoriparty.org.nz/mana_motuhake) — [full text](documents/site-mana-motuhake.md) · [archived copy cited by policy.nz](https://web.archive.org/web/20260818042500/https://www.maoriparty.org.nz/mana_motuhake)
  - [Te Pāti Māori Launches Te Tiriti Entrenchment Policy (Press release, 2026-09-01)](https://www.scoop.co.nz/stories/PA2609/S00008/te-pati-maori-launches-te-tiriti-entrenchment-policy.htm) — [full text](documents/2026-09-01-te-pati-maori-launches-te-tiriti-entrenchment-policy.md)
  - [Mana Motuhake — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/12XBSiuPt6KrpmxoHovpWOhfrB5ngTYkY/view) — [full text](documents/pdf-mana-motuhake.md)

### TPM-A03: Establish a $220 million Mātike Mai Fund and set 2040 as the target for constitutional transformation

**Statement:** Establish a $220 million Mātike Mai Fund and set 2040 as the target for constitutional transformation  
*Summary source: archive* · topics: te-tiriti-o-waitangi-and-governance, parliament-and-democracy

- **Why:** The party says Māori-led constitutional work (Mātike Mai Aotearoa) has been done but lacks resources and enforceable accountability.
- **How:** This party would fund a $220 million Mātike Mai Fund over four years to independently resource iwi, hapū and Māori to lead constitutional transformation, with 2040 as the target. It says it will not itself determine the constitutional destination.
- **Sources:**
  - [Te Tiriti Entrenchment Policy 2026 (PDF)](https://img.scoop.co.nz/media/pdfs/2609/TIRITI_ENTRENCHMENT_POLICY.pdf) — [full text](documents/pdf-tiriti-entrenchment-policy.md)
  - [Te Pāti Māori Launches Te Tiriti Entrenchment Policy (Press release, 2026-09-01)](https://www.scoop.co.nz/stories/PA2609/S00008/te-pati-maori-launches-te-tiriti-entrenchment-policy.htm) — [full text](documents/2026-09-01-te-pati-maori-launches-te-tiriti-entrenchment-policy.md)
  - [Te Tiriti Entrenchment — Te Pāti Māori Policy Manifesto 2026 (Drive edition) (PDF)](https://drive.google.com/file/d/1esXEFN0eAOtJFcdIYwYOzaVkyFtEx5vE/view) — [full text](documents/pdf-te-tiriti-entrenchment.md)

### TPM-A04: Require a Te Tiriti Impact Statement for every Bill

**Statement:** Require a Te Tiriti Impact Statement for every Bill  
*Summary source: archive* · topics: te-tiriti-o-waitangi-and-governance, parliament-and-democracy

- **Why:** The party says governments can ignore the Waitangi Tribunal and weaken Te Tiriti protections.
- **How:** This party would require every Bill before Parliament to include a Te Tiriti Impact Statement.
- **Sources:**
  - [Te Pati Maori Will Make The Waitangi Tribunal Recommendations Binding (Press release, 2026-08-06)](https://www.scoop.co.nz/stories/PA2608/S00044/te-pati-maori-will-make-the-waitangi-tribunal-recommendations-binding.htm) — [full text](documents/2026-08-06-te-pati-maori-will-make-the-waitangi-tribunal-recommendation.md)
  - [Mana Motuhake — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/12XBSiuPt6KrpmxoHovpWOhfrB5ngTYkY/view) — [full text](documents/pdf-mana-motuhake.md)

### TPM-A05: Entrench the Māori electorates and require Māori wards in every council

**Statement:** Entrench the Māori electorates and require Māori wards in every council  
*Summary source: archive* · topics: parliament-and-democracy, te-ao-maori

- **Why:** The party says the Māori seats are guaranteed under Te Tiriti and should not be removable by referendum (responding to NZ First's referendum proposal).
- **How:** The party says that when it forms the next government it will 'entrench the Māori seats in the constitution beyond the reach of referendums'. The 2026 Mana Motuhake chapter and the party's policy tool also commit to requiring Māori wards and mana whenua representation in all councils.
- **Sources:**
  - [Māori Seats Are Constitutional, Not Conditional (Press release, 2026-02-13)](https://www.scoop.co.nz/stories/PA2602/S00082/maori-seats-are-constitutional-not-conditional.htm) — [full text](documents/2026-02-13-maori-seats-are-constitutional-not-conditional.md)
  - [Mana Motuhake — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/12XBSiuPt6KrpmxoHovpWOhfrB5ngTYkY/view) — [full text](documents/pdf-mana-motuhake.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)

### TPM-A40: Land back: return the foreshore and seabed, conservation land and Crown and council land to mana whenua

**Statement:** Land back: return the foreshore and seabed, conservation land and Crown and council land to mana whenua  
*Summary source: archive* · topics: land-and-resources, te-tiriti-o-waitangi-and-governance

- **Why:** The party says mana motuhake requires the return of land and authority.
- **How:** The 2026 Mana Motuhake chapter commits to returning the foreshore and seabed, all conservation land and all central and local government land to mana whenua, a first right of refusal for mana whenua on all private land sales, ending perpetual leases, and ending foreign freehold land sales (leasehold only).
- **Sources:**
  - [Mana Motuhake — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/12XBSiuPt6KrpmxoHovpWOhfrB5ngTYkY/view) — [full text](documents/pdf-mana-motuhake.md)
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)
  - [Mana Motuhake (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/mana_motuhake) — [full text](documents/site-mana-motuhake.md)

### TPM-A41: Establish a Māori Parliament

**Statement:** Establish a Māori Parliament  
*Summary source: archive* · topics: parliament-and-democracy, te-ao-maori

- **Why:** The party says Māori political authority must be restored.
- **How:** The 2026 Mana Motuhake chapter (Stage 3) commits to establishing a Māori Parliament holding authority over Māori programmes, funding streams and governance structures accountable to Māori.
- **Sources:**
  - [Mana Motuhake — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/12XBSiuPt6KrpmxoHovpWOhfrB5ngTYkY/view) — [full text](documents/pdf-mana-motuhake.md)

### TPM-A42: Remove the British monarch as head of state and make Aotearoa the official name

**Statement:** Remove the British monarch as head of state and make Aotearoa the official name  
*Summary source: archive* · topics: parliament-and-democracy, te-reo-maori-and-culture

- **Why:** The party frames these as part of Te Tiriti-based constitutional transformation.
- **How:** The 2026 Mana Motuhake chapter (Stage 3) lists removing the British Royal Family as Head of State and recognising Aotearoa as the country's official name.
- **Sources:**
  - [Mana Motuhake — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/12XBSiuPt6KrpmxoHovpWOhfrB5ngTYkY/view) — [full text](documents/pdf-mana-motuhake.md)

### TPM-A43: Reform Treaty settlements: end 'full and final' and 'large natural groupings' policies, add relativity clauses

**Statement:** Reform Treaty settlements: end 'full and final' and 'large natural groupings' policies, add relativity clauses  
*Summary source: archive* · topics: te-tiriti-o-waitangi-and-governance

- **Why:** The party says the settlement framework must be durable, just and recognise hapū-level authority.
- **How:** The 2026 Mana Motuhake chapter commits to abolishing 'full and final' and 'large natural groupings' settlement policies and inserting retrospective relativity clauses into all Te Tiriti settlements.
- **Sources:**
  - [Mana Motuhake — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/12XBSiuPt6KrpmxoHovpWOhfrB5ngTYkY/view) — [full text](documents/pdf-mana-motuhake.md)

### TPM-A45: Lower the voting age to 16 and allow switching between Māori and general rolls at any time

**Statement:** Lower the voting age to 16 and allow switching between Māori and general rolls at any time  
*Summary source: archive* · topics: parliament-and-democracy

- **Why:** The party says electoral law should not exclude Māori and young people.
- **How:** The party's policy tool and Justice chapter list lowering the voting age to 16, enrolment at any time, switching between the Māori and general rolls at any time, and restoring voting rights to people in prison.
- **Sources:**
  - [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026) (Party web page (Common Crawl), 2026-10-08)](https://www.maoriparty.org.nz/what-matters-to-you) — [full text](documents/site-what-matters-to-you-manifesto-tool.md)
  - [Justice — Te Pāti Māori Policy Manifesto 2026 (PDF)](https://drive.google.com/file/d/1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx/view) — [full text](documents/pdf-justice-1phb4pna7fe9ipj5sxhrrcrmgywm-mhax.md)

## Document index

| Date | Type | Document | Original |
|---|---|---|---|
| — | PDF | [A Kiwi Tax Plan — Te Pāti Māori Policy Manifesto 2026: Tax](documents/pdf-a-kiwi-tax-plan.md) | [link](https://img.scoop.co.nz/media/pdfs/2608/A_Kiwi_Tax_Plan.pdf) |
| — | PDF | [Te Tiriti Entrenchment Policy 2026](documents/pdf-tiriti-entrenchment-policy.md) | [link](https://img.scoop.co.nz/media/pdfs/2609/TIRITI_ENTRENCHMENT_POLICY.pdf) |
| — | PDF | [Energy Sovereignty Policy 2026](documents/pdf-te-pti-mori-energy-sovereignty-policy-final.md) | [link](https://img.scoop.co.nz/media/pdfs/2609/Te_Pti_Mori_Energy_Sovereignty_Policy_FINAL.pdf) |
| — | PDF | [Kai Sovereignty Policy 2026](documents/pdf-kai-sovereignty-policy-2026.md) | [link](https://img.scoop.co.nz/media/pdfs/2609/KAI_SOVEREIGNTY_POLICY_2026.pdf) |
| — | PDF | [Justice — Te Pāti Māori Policy Manifesto 2026](documents/pdf-justice-1phb4pna7fe9ipj5sxhrrcrmgywm-mhax.md) | [link](https://drive.google.com/file/d/1PhB4PNA7fE9Ipj5SXhRRCrmgywM-MhAx/view) |
| — | PDF | [Mana Motuhake Policy (2023 document — NOT confirmed as 2026 policy)](documents/pdf-mana-motuhake-1y9gti2vgayijygamaq5e-wvclylcoytl.md) | [link](https://drive.google.com/file/d/1Y9GTi2VGAYIJygAmaQ5e-WVCLYlCOYTL/view) |
| — | PDF | [Tax — Te Pāti Māori Policy Manifesto 2026 (Drive edition)](documents/pdf-tax.md) | [link](https://drive.google.com/file/d/11dbbk3BTNigHUb4xANPnTKxb2TC9dAgg/view) |
| — | PDF | [Te Tiriti Entrenchment — Te Pāti Māori Policy Manifesto 2026 (Drive edition)](documents/pdf-te-tiriti-entrenchment.md) | [link](https://drive.google.com/file/d/1esXEFN0eAOtJFcdIYwYOzaVkyFtEx5vE/view) |
| — | PDF | [Energy Sovereignty — Te Pāti Māori Policy Manifesto 2026 (Drive edition)](documents/pdf-energy-sovereignty.md) | [link](https://drive.google.com/file/d/1CPy0C0flCQ71RKuSmtaD3CNsoShG7QAc/view) |
| — | PDF | [Mana Motuhake — Te Pāti Māori Policy Manifesto 2026](documents/pdf-mana-motuhake.md) | [link](https://drive.google.com/file/d/12XBSiuPt6KrpmxoHovpWOhfrB5ngTYkY/view) |
| — | PDF | [Military Neutrality — Te Pāti Māori Policy Manifesto 2026](documents/pdf-military-neutrality.md) | [link](https://drive.google.com/file/d/1CCbBwB6mcxNgPTDnycPkcgvVrUDY5ZmL/view) |
| — | PDF | [Climate — Te Pāti Māori Policy Manifesto 2026](documents/pdf-climate.md) | [link](https://drive.google.com/file/d/1FzavJoSYNEzsVWhnS9sBMI3XENAb9-Dr/view) |
| — | PDF | [Toi Māori — Te Pāti Māori Policy Manifesto 2026](documents/pdf-toi-maori.md) | [link](https://drive.google.com/file/d/1Jc9cFUmV5YgkPg7tlKpojeiOSvXzJX1N/view) |
| — | PDF | [Freshwater — Te Pāti Māori Policy Manifesto 2026](documents/pdf-freshwater.md) | [link](https://drive.google.com/file/d/1LPTzVr2sdxSNdfLF2DFLikHqr2zaeuBP/view) |
| — | PDF | [Housing — Te Pāti Māori Policy Manifesto 2026](documents/pdf-housing.md) | [link](https://drive.google.com/file/d/1T8WiwxG9nIDnDEjyVujLZKvoNWp7i0Oh/view) |
| — | PDF | [Mokopuna Māori — Te Pāti Māori Policy Manifesto 2026](documents/pdf-mokopuna-maori.md) | [link](https://drive.google.com/file/d/1dIy46mwnEg7G0oG-2r8xC5b0Be2Poegs/view) |
| — | PDF | [Te Reo Māori — Te Pāti Māori Policy Manifesto 2026](documents/pdf-te-reo-maori.md) | [link](https://drive.google.com/file/d/1m8zZo4j-pzDqeQdFj_OcVTPjq6VgEHCh/view) |
| — | PDF | [Mana Takatāpui — Te Pāti Māori Policy Manifesto 2026](documents/pdf-mana-takatapui.md) | [link](https://drive.google.com/file/d/1qyqzCxGrLF067Q2S5ZafwQ1F_UDOpPj0/view) |
| — | PDF | [Whānau Pakari – Sport and Wellbeing Policy (2020 document — NOT confirmed as 2026 policy)](documents/pdf-whanau-pakari-sport-and-wellbeing-policy.md) | [link](https://drive.google.com/file/d/1IeJ-WmT2cwdeo6noqVaSRFk55dhQGpNl/view) |
| — | PDF | [Mana Hauā (Disability) Policy (2023 document — NOT confirmed as 2026 policy)](documents/pdf-mana-haua-policy.md) | [link](https://drive.google.com/file/d/1V1fVe2hhe5eNDVBuJYmxu3_07igGSiyo/view) |
| — | PDF | [Mokopuna Māori Policy (2023 document — superseded)](documents/pdf-mokopuna-maori-policy.md) | [link](https://drive.google.com/file/d/1N9MFecQz4zJngdvZhP6HtqC6IjiP5bIz/view) |
| 2025-02-04 | Press release | [Te Pāti Māori Vow To Protect Te Tiriti With Establishment Of Independent Commissioner For Te Tiriti O Waitangi](documents/2025-02-04-te-pati-maori-vow-to-protect-te-tiriti-with-establishment-of.md) | [link](https://www.scoop.co.nz/stories/PA2502/S00022/te-pati-maori-vow-to-protect-te-tiriti-with-esta.htm) |
| 2026-01-28 | Press release | [“If You’re Not Trying To Abolish Prisons In Aotearoa, What Are You Doing In Parliament?” - Rawiri Waititi](documents/2026-01-28-if-youre-not-trying-to-abolish-prisons-in-aotearoa-what-are.md) | [link](https://www.scoop.co.nz/stories/PA2601/S00112/if-youre-not-trying-to-abolish-prisons-in-aotearoa-what-are-you-doing-in-parliament-rawiri-waititi.htm) |
| 2026-01-29 | Press release | [Oriini Kaipara: Prime Minister’s ‘Progress’ Ignores Housing Crisis Facing Māori And Rangatahi](documents/2026-01-29-oriini-kaipara-prime-ministers-progress-ignores-housing-cris.md) | [link](https://www.scoop.co.nz/stories/PA2601/S00115/oriini-kaipara-prime-ministers-progress-ignores-housing-crisis-facing-maori-and-rangatahi.htm) |
| 2026-02-08 | Press release | [Seabed Mining Banned In Aotearoa Under Reintroduced Member’s Bill](documents/2026-02-08-seabed-mining-banned-in-aotearoa-under-reintroduced-members.md) | [link](https://www.scoop.co.nz/stories/PA2602/S00040/seabed-mining-banned-in-aotearoa-under-reintroduced-members-bill.htm) |
| 2026-02-13 | Press release | [Māori Seats Are Constitutional, Not Conditional](documents/2026-02-13-maori-seats-are-constitutional-not-conditional.md) | [link](https://www.scoop.co.nz/stories/PA2602/S00082/maori-seats-are-constitutional-not-conditional.htm) |
| 2026-02-22 | Press release | [Te Pāti Māori Rejects Move-on Orders: “We Will Not Police Our Way Out Of Homelessness"](documents/2026-02-22-te-pati-maori-rejects-move-on-orders-we-will-not-police-our.md) | [link](https://www.scoop.co.nz/stories/PA2602/S00141/te-pati-maori-rejects-move-on-orders-we-will-not-police-our-way-out-of-homelessness.htm) |
| 2026-03-01 | Press release | [Te Pāti Māori Statement: Aotearoa Must Stand For Peace](documents/2026-03-01-te-pati-maori-statement-aotearoa-must-stand-for-peace.md) | [link](https://www.scoop.co.nz/stories/PA2603/S00004/te-pati-maori-statement-aotearoa-must-stand-for-peace.htm) |
| 2026-03-17 | Party web page (Common Crawl) | [Māori Sports](documents/site-maori-sports.md) | [link](https://www.maoriparty.org.nz/maori_sports) |
| 2026-03-18 | Press release | [Te Pāti Māori Calls For Urgent Suspension Of Fuel Excise Tax To Relieve Pressure On Whānau](documents/2026-03-18-te-pati-maori-calls-for-urgent-suspension-of-fuel-excise-tax.md) | [link](https://www.scoop.co.nz/stories/PA2603/S00110/te-pati-maori-calls-for-urgent-suspension-of-fuel-excise-tax-to-relieve-pressure-on-whanau.htm) |
| 2026-04-02 | Press release | [Te Pāti Māori Calls For Freeze On MP Pay Rises](documents/2026-04-02-te-pati-maori-calls-for-freeze-on-mp-pay-rises.md) | [link](https://www.scoop.co.nz/stories/PA2604/S00015/te-pati-maori-calls-for-freeze-on-mp-pay-rises.htm) |
| 2026-04-09 | Press release | [We Must Act Now On Energy Sovereignty- Every Household Is Paying The Price](documents/2026-04-09-we-must-act-now-on-energy-sovereignty-every-household-is-pay.md) | [link](https://www.scoop.co.nz/stories/PA2604/S00042/we-must-act-now-on-energy-sovereignty-every-household-is-paying-the-price.htm) |
| 2026-04-09 | Press release | [Must Fund Marae Resilience Package Ahead Of Cyclone Vaianu](documents/2026-04-09-must-fund-marae-resilience-package-ahead-of-cyclone-vaianu.md) | [link](https://www.scoop.co.nz/stories/PA2604/S00046/must-fund-marae-resilience-package-ahead-of-cyclone-vaianu.htm) |
| 2026-04-12 | Party web page (Common Crawl) | [Mana Hauā Policy](documents/site-mana-hau-policy.md) | [link](https://www.maoriparty.org.nz/mana_hau_policy?fbclid=IwAR3CGHLJh56Vtl-Z6tSNbCWdMvsw-c9-oXxW3ce9dqzZ_-e8sRnDZ5Q2vRE&ref=infoexchange.nz) |
| 2026-05-15 | Press release | [TPM To Entrench Te Tiriti: Government’s Tiriti Purge Is Constitutional Vandalism](documents/2026-05-15-tpm-to-entrench-te-tiriti-governments-tiriti-purge-is-consti.md) | [link](https://www.scoop.co.nz/stories/PA2605/S00134/tpm-to-entrench-te-tiriti-governments-tiriti-purge-is-constitutional-vandalism.htm) |
| 2026-06-09 | Press release | [If The Government Really Wants To Lower Power Bills, This Is The Way](documents/2026-06-09-if-the-government-really-wants-to-lower-power-bills-this-is.md) | [link](https://www.scoop.co.nz/stories/PA2606/S00066/if-the-government-really-wants-to-lower-power-bills-this-is-the-way.htm) |
| 2026-08-02 | Press release | [Te Pāti Māori Announces Māori Education Authority To Restore Māori Success In Education](documents/2026-08-02-te-pati-maori-announces-maori-education-authority-to-restore.md) | [link](https://www.scoop.co.nz/stories/PA2608/S00006/te-pati-maori-announces-maori-education-authority-to-restore-maori-success-in-education.htm) |
| 2026-08-06 | Press release | [Te Pati Maori Will Make The Waitangi Tribunal Recommendations Binding](documents/2026-08-06-te-pati-maori-will-make-the-waitangi-tribunal-recommendation.md) | [link](https://www.scoop.co.nz/stories/PA2608/S00044/te-pati-maori-will-make-the-waitangi-tribunal-recommendations-binding.htm) |
| 2026-08-16 | Party web page (Common Crawl) | [Kai Sovereignty](documents/site-kai-sovereignt.md) | [link](https://www.maoriparty.org.nz/kai_sovereignt) |
| 2026-08-16 | Party web page (Common Crawl) | [Disabilities](documents/site-disabilities.md) | [link](https://www.maoriparty.org.nz/disabilities) |
| 2026-08-16 | Party web page (Common Crawl) | [Justice - Te Pāti Māori New (Not live)](documents/site-justice.md) | [link](https://www.maoriparty.org.nz/justice) |
| 2026-08-26 | Press release | [Pūtea Back In Your Pocket: TPM Unveils A Kiwi Tax Plan For Everyone](documents/2026-08-26-putea-back-in-your-pocket-tpm-unveils-a-kiwi-tax-plan-for-ev.md) | [link](https://www.scoop.co.nz/stories/PA2608/S00238/putea-back-in-your-pocket-tpm-unveils-a-kiwi-tax-plan-for-everyone.htm) |
| 2026-09-01 | Press release | [Te Pāti Māori Launches Te Tiriti Entrenchment Policy](documents/2026-09-01-te-pati-maori-launches-te-tiriti-entrenchment-policy.md) | [link](https://www.scoop.co.nz/stories/PA2609/S00008/te-pati-maori-launches-te-tiriti-entrenchment-policy.htm) |
| 2026-09-08 | Party web page (Common Crawl) | [Health Policy](documents/site-health.md) | [link](https://www.maoriparty.org.nz/health) |
| 2026-09-08 | Party web page (Common Crawl) | [Economic development](documents/site-economic-development.md) | [link](https://www.maoriparty.org.nz/economic_development) |
| 2026-09-08 | Party web page (Common Crawl) | [Cost of living](documents/site-cost-of-living.md) | [link](https://www.maoriparty.org.nz/cost_of_living) |
| 2026-09-08 | Party web page (Common Crawl) | [Military neutrality](documents/site-military-neutrality.md) | [link](https://www.maoriparty.org.nz/military_neutrality) |
| 2026-09-16 | Press release | [We Want Cheaper Power And We Want Our People To Own It](documents/2026-09-16-we-want-cheaper-power-and-we-want-our-people-to-own-it.md) | [link](https://www.scoop.co.nz/stories/PA2609/S00161/we-want-cheaper-power-and-we-want-our-people-to-own-it.htm) |
| 2026-09-21 | Press release | [Te Pāti Māori Launches Kai Sovereignty Policy](documents/2026-09-21-te-pati-maori-launches-kai-sovereignty-policy.md) | [link](https://www.scoop.co.nz/stories/PA2609/S00211/te-pati-maori-launches-kai-sovereignty-policy.htm) |
| 2026-09-23 | Press release | [Te Pāti Māori Launches Mana Takatāpui Policy](documents/2026-09-23-te-pati-maori-launches-mana-takatapui-policy.md) | [link](https://www.scoop.co.nz/stories/PA2609/S00245/te-pati-maori-launches-mana-takatapui-policy.htm) |
| 2026-10-04 | Press release | [Te Pāti Māori Puts Its Money Where Its Mouth Is With One-Person Party List](documents/2026-10-04-te-pati-maori-puts-its-money-where-its-mouth-is-with-one-per.md) | [link](https://www.scoop.co.nz/stories/PA2610/S00026/te-pati-maori-puts-its-money-where-its-mouth-is-with-one-person-party-list.htm) |
| 2026-10-06 | Press release | [Te Pāti Māori Backs Kōhanga Reo And Kura With Long-Term Investment](documents/2026-10-06-te-pati-maori-backs-kohanga-reo-and-kura-with-long-term-inve.md) | [link](https://www.scoop.co.nz/stories/PA2610/S00052/te-pati-maori-backs-kohanga-reo-and-kura-with-long-term-investment.htm) |
| 2026-10-08 | Party web page (Common Crawl) | [Policy](documents/site-policy.md) | [link](https://www.maoriparty.org.nz/policy) |
| 2026-10-08 | Party web page (Common Crawl) | [Energy Sovereignty](documents/site-energy-sovereignty.md) | [link](https://www.maoriparty.org.nz/energy_sovereignty) |
| 2026-10-08 | Party web page (Common Crawl) | [Te Tiriti Entrenchment](documents/site-te-tiriti-entrenchment.md) | [link](https://www.maoriparty.org.nz/te_tiriti_entrenchment) |
| 2026-10-08 | Party web page (Common Crawl) | [Tax Policy](documents/site-tax.md) | [link](https://www.maoriparty.org.nz/tax) |
| 2026-10-08 | Party web page (Common Crawl) | [Takatāpui](documents/site-takat-pui.md) | [link](https://www.maoriparty.org.nz/takat_pui) |
| 2026-10-08 | Party web page (Common Crawl) | [Mokopuna Māori](documents/site-mokopuna-m-ori.md) | [link](https://www.maoriparty.org.nz/mokopuna_m_ori) |
| 2026-10-08 | Party web page (Common Crawl) | [Housing](documents/site-housing.md) | [link](https://www.maoriparty.org.nz/housing) |
| 2026-10-08 | Party web page (Common Crawl) | [Education & Training](documents/site-education-training.md) | [link](https://www.maoriparty.org.nz/education_training) |
| 2026-10-08 | Party web page (Common Crawl) | [Toi Māori](documents/site-toi-maori.md) | [link](https://www.maoriparty.org.nz/toi_maori) |
| 2026-10-08 | Party web page (Common Crawl) | [Te Reo Māori](documents/site-te-reo-maori.md) | [link](https://www.maoriparty.org.nz/te_reo_maori) |
| 2026-10-08 | Party web page (Common Crawl) | [Mana Motuhake](documents/site-mana-motuhake.md) | [link](https://www.maoriparty.org.nz/mana_motuhake) |
| 2026-10-08 | Party web page (Common Crawl) | [Freshwater Policy](documents/site-freshwater-policy.md) | [link](https://www.maoriparty.org.nz/freshwater_policy) |
| 2026-10-08 | Party web page (Common Crawl) | [Climate](documents/site-climate.md) | [link](https://www.maoriparty.org.nz/climate) |
| 2026-10-08 | Party web page (Common Crawl) | [We Want Cheaper Power And We Want Our People To Own It.](documents/site-we-want-cheaper-power-and-we-want-our-people-to-own-it.md) | [link](https://www.maoriparty.org.nz/we_want_cheaper_power_and_we_want_our_people_to_own_it) |
| 2026-10-08 | Party web page (Common Crawl) | [“What matters to you?” policy tool (content from the Te Pāti Māori Policy Manifesto 2026)](documents/site-what-matters-to-you-manifesto-tool.md) | [link](https://www.maoriparty.org.nz/what-matters-to-you) |
| 2026-10-12 | Press release | [Te Pāti Māori Announces Toi Māori Authority And Artist Income Programme](documents/2026-10-12-te-pati-maori-announces-toi-maori-authority-and-artist-incom.md) | [link](https://www.scoop.co.nz/stories/PA2610/S00101/te-pati-maori-announces-toi-maori-authority-and-artist-income-programme.htm) |
| — | Not retrieved | ['Sports', undated (accessed 18 August 2026)](documents/not-retrieved-maoriparty-sports.md) | [link](https://www.maoriparty.org.nz/sports) |
