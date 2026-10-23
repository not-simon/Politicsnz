# Porting the redesign into `site/src/app.html`

This is the engineer's guide for moving the single-file app onto the new structure and stylesheet. Read `IA.md` first for the why. Everything here refers to real functions in `site/src/app.html` as of 23 Oct 2026.

**Files in `site/redesign/`**

| File | Use |
|---|---|
| `tokens.css` | Every colour, type, space, radius and motion token, light + dark. Paste first. |
| `components.css` | Every class named below. Paste second. Replaces the whole current `<style>` block. |
| `mockups/*.html` | Reference markup for each screen. `mockups/mock.js` is mockup-only behaviour (theme toggle, scrubber play, likert, swipe drag) and shows the intended interaction. |
| `IA.md` | Sections, navigation, depth model, journeys. |
| `critique/` | Screenshots of the current site used in `IA.md`. |

---

## 1. Setup

1. Replace the fonts `<link>` in `<head>`:
   ```html
   <link rel="preconnect" href="https://fonts.googleapis.com">
   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
   <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Public+Sans:ital,wght@0,400..800;1,400..700&display=swap">
   ```
2. Delete the whole current `<style>` block (including the alias block that maps `--text` → `--ink` etc.) and paste `tokens.css` then `components.css` into one `<style>`. Nothing in the new CSS depends on the old names.
3. Keep the theme mechanism exactly as it is: `localStorage['bb-theme']` sets `document.documentElement.dataset.theme`. The new toggle button needs both icons (see the shell); CSS shows the right one.
4. Add the icon sprite once, right after `<body>` (copy the `<svg width="0" height="0" …>` block from any mockup). Then replace the `ICON`/`ic()` helpers with:
   ```js
   const ic = (k, cls = '') => `<svg class="i i-${k} ${cls}" aria-hidden="true"><use href="#i-${k}"/></svg>`;
   ```
   Icon names: `today vote choose parties seats search moon sun chev down back close ext pin play pause check x minus half clock info share print caladd msg lock doc spark poll history news swap map help flag shield filter list phone cards compass scale game users book download`. Sizes: default 24, `.i--s` 18, `.i--xs` 14, `.i--l` 32.

---

## 2. The shell

Replace everything from `<header class="top">` to the `<dialog id="dlg">` with this. `#nav`, `#bnav`, `#phase` and `#foot` are filled by JS as now.

```html
<a class="skip" href="#main">Skip to content</a>
<header class="mast">
  <div class="wrap mast__in">
    <a class="brand" href="#/today" aria-label="Ballot Book NZ, home">
      <svg class="brand__mark" viewBox="0 0 30 30" aria-hidden="true"><circle cx="13" cy="16" r="11"/><path d="M7.5 15.5l4.5 4.5L27 3.5"/></svg>
      <span class="brand__word">Ballot Book</span><span class="brand__tag">NZ 2026</span>
    </a>
    <nav class="nav" id="nav" aria-label="Sections"></nav>            <!-- desktop only (CSS) -->
    <div class="mast__tools">
      <button class="search-trigger" type="button" id="searchbtn" aria-label="Search">
        <svg class="i i--s"><use href="#i-search"/></svg><span>Search parties, people, policies</span><kbd>/</kbd>
      </button>
      <button class="iconbtn theme-toggle" type="button" id="themebtn" aria-label="Switch light or dark">
        <svg class="i i--s i-moon"><use href="#i-moon"/></svg><svg class="i i--s i-sun"><use href="#i-sun"/></svg>
      </button>
    </div>
  </div>
  <div class="phase" id="phase" data-phase="enrol" role="status"></div>
</header>
<main id="main" class="wrap page"></main>
<footer class="colophon" id="foot"></footer>
<nav class="tabbar" id="bnav" aria-label="Sections"></nav>          <!-- phone only (CSS) -->
<dialog class="sheet" id="sheet" aria-labelledby="sheet-title">
  <div class="sheet__head">
    <div class="stack stack--s"><span class="depth" id="sheet-depth"></span><h2 class="h3" id="sheet-title"></h2><p class="src" id="sheet-src"></p></div>
    <button class="iconbtn" type="button" id="sheet-close" aria-label="Close" autofocus><svg class="i i--s"><use href="#i-close"/></svg></button>
  </div>
  <div class="sheet__body" id="sheet-body"></div>
</dialog>
```

`<body>` gets `class="has-tabbar"` (adds bottom padding on phones). In **focus mode** (quiz, swipe, game in progress) remove `has-tabbar`, hide `#bnav`, and render the header as:
```html
<div class="wrap mast__in"><a class="btn btn--quiet btn--s" href="#/choose"><svg class="i i--s"><use href="#i-close"/></svg> Exit</a>
  <span class="h4">Find your match</span><div class="mast__tools"><!-- theme toggle only --></div></div>
```
(see `mockups/quiz.html`).

**Nav arrays** (replace `NAV` and the `#bnav` list):
```js
const SECTIONS = [['today','Today'],['vote','Vote'],['choose','Choose'],['parties','Parties'],['seats','Seats']];
$('#nav').innerHTML  = SECTIONS.map(([k,l]) => `<a href="#/${k}" data-sec="${k}">${l}</a>`).join('');
$('#bnav').innerHTML = SECTIONS.map(([k,l]) => `<a href="#/${k}" data-sec="${k}">${ic(k)}<span>${l}</span></a>`).join('');
// on every route: document.querySelectorAll('[data-sec]').forEach(a => a.toggleAttribute('aria-current', a.dataset.sec === sec)) — set the value "page"
```

**Sub-navigation.** Each section view starts with `.section` → `.subnav` + `.section__body`. The same `<nav class="subnav">` is a chip row on phones and a sticky left rail on desktop:
```html
<div class="section">
  <nav class="subnav" aria-label="Seats"><span class="subnav__label">Seats</span>
    <a href="#/seats/polls" aria-current="page">Polls &amp; forecast</a><a href="#/seats/map">Electorate map</a>…
  </nav>
  <div class="section__body"> … view content … </div>
</div>
```
Counts go in `<span class="num">1,435</span>` inside the link. The Today page doesn't use `.section`; it uses `<main class="wrap page page--hero">` so the phase hero sits flush under the ribbon on phones.

**Phase ribbon** (replaces `renderBanner()`; keep `electionPhase()` and `nzNow()`):
```js
const PHASE_MSG = {
  enrol:  ['Enrolment closes in ' + daysTo('2026-10-25T23:59+13:00') + ' days.', 'Midnight Sunday 25 October. No enrolling at voting places this year.', 'Check at vote.nz', 'https://vote.nz'],
  advance:['Voting is open.', 'Vote early at any voting place until 6 November.', 'Find a voting place', 'https://map.vote.nz'],
  electionday:['Election day: voting closes at 7pm.', 'Results, polls and the forecast are hidden until then.', 'Find a voting place', 'https://map.vote.nz'],
  results:['Results are coming in.', 'Preliminary count. Special votes are counted later.', 'Live results', '#/seats/results'],
  after:  ['Special votes are being counted.', 'Final result Friday 27 November.', 'What could change', '#/vote/specials'] };
$('#phase').dataset.phase = ph;
$('#phase').innerHTML = `<div class="wrap phase__in"><span class="phase__dot" aria-hidden="true"></span><span><b>${m[0]}</b> <span class="phase__more">${m[1]}</span></span><a href="${m[3]}">${m[2]}</a></div>`;
```
Not dismissible in the `enrol` and `electionday` phases.

**Footer** (`#foot`): copy the `.colophon__grid` from any mockup. It carries the trust links (Why trust this, Editorial standards, How the tools work, Review log, Report an error, Open data, vote.nz, 0800 36 76 56). The current footer's inline buttons go away.

**Sheet** (replaces `openDialog()` and `#dlg`):
```js
function openSheet({ title, depth = ['Summary','Detail','Full text'], at = 2, src = '', html, route }) {
  $('#sheet-title').textContent = title;
  $('#sheet-depth').innerHTML = depth.map((d,i) => `<span${i===at?' aria-current="step"':''}>${d}</span>`).join('');
  $('#sheet-src').innerHTML = src; $('#sheet-body').innerHTML = html;
  if (route) history.pushState({ sheet: route }, '', '#' + route);   // back closes it
  const d = $('#sheet'); if (!d.open) d.showModal(); $('#sheet-body').scrollTop = 0;
}
$('#sheet-close').onclick = () => history.state?.sheet ? history.back() : $('#sheet').close();
addEventListener('popstate', () => { if ($('#sheet').open && !history.state?.sheet) $('#sheet').close() });
```
`openDoc()`, `openPerson()`, `showIssuePolicies()` and `openPage()` call `openSheet()` instead of `openDialog()`. Full text gets the `.note` "The party's own words, shown as published. Not edited or fact-checked." above a `.prose` body (see `mockups/party-reader.html`).

**Page transitions.** Wrap the body of `route()` that writes `#main` in
```js
const swap = () => { /* existing render */ };
document.startViewTransition && !matchMedia('(prefers-reduced-motion: reduce)').matches ? document.startViewTransition(swap) : swap();
```
and add `page-enter` to `#main`'s class list after each render (remove/re-add to replay). CSS does the rest.

---

## 3. Routes

New hash routes are `#/section/sub/arg`. Keep a redirect table so every old link still works:

| Old | New | View function |
|---|---|---|
| `#home` | `#/today` | `V.home` (rewritten) |
| `#match` | `#/choose/quiz` (results `#/choose/results`) | `V.match` |
| `#swipe`, `#swipe-tally` | `#/choose/swipe` (tally is on the same page) | `V.swipe` |
| `#compass` | `#/choose/compass` | `V.compass` |
| `#game` | `#/choose/game` | `V.game` |
| — | `#/choose` (hub), `#/choose/compare` | new `V.choose`, `V.compare` |
| `#parties` | `#/parties` | `V.parties` |
| `#party-{slug}` | `#/parties/{slug}` (`/policies`, `/record`, `/people`, `/history`) | `V.party(slug, tab)` |
| `#issues`, `#issue-{slug}` | `#/parties/issues`, `#/parties/issues/{slug}` | `V.issues`, `V.issue` |
| `#policies` | `#/parties/policies` | `V.policies` |
| `#promises` | `#/parties/promises` | `V.promises` |
| `#people` | `#/parties/people` | `V.people` |
| — | `#/parties/news` | new `V.news` |
| `#electorate`, `#electorate-{slug}` | `#/vote/electorate`, `#/vote/electorate/{slug}` | `V.electorate` |
| — | `#/vote` | new `V.vote` (checklist, chooser, plan) |
| `#map` | `#/seats/map` (`/{year}/{slug}`) | `V.map` |
| `#polls`, `#trends` | `#/seats/polls` | `V.polls` |
| `#parliament`, `#chamber` | `#/seats/parliament` | `V.parliament('chamber')` |
| `#coalition`, `#calculator` | `#/seats/coalition`, `#/seats/calculator` | `V.parliament(sub)` |
| `#trust` | `#/about/trust` (linked from footer) | `V.trust` |
| `#more` | `#/today` | **delete `V.more`** |

`blockedToday(view)` keeps its logic but checks the new keys (`choose/*` results, `seats/polls`, `today` policy of the day) and renders the `.lock` block:
```html
<div class="lock"><svg class="i"><use href="#i-lock"/></svg><h2 class="h3">Hidden until 7pm</h2>
<p>Today is election day. By law, material that could influence how people vote can't be published until voting closes at 7pm.</p>
<a class="btn btn--primary" href="https://map.vote.nz">Find a voting place</a></div>
```

---

## 4. Component patterns

Class names are the contract. Party colour is always passed as `style="--pc:#hex"` on the element (never as a raw `background:`), so the ring tokens and dark-mode handling apply.

**Type and structure**
```html
<header class="pagehead"><p class="eyebrow eyebrow--signal"><svg class="i i--s"><use href="#i-seats"/></svg> Seats · Polls</p>
  <h1>What the polls say</h1><p class="lede">…</p></header>
<div class="shead"><div class="shead__row"><h2>Section title</h2><a class="more small" href="…">All 126 policies <svg class="i i--xs"><use href="#i-chev"/></svg></a></div></div>
```
`.shead` = heavy ink rule + title (use `.shead--quiet` for a hairline). `.eyebrow` replaces `.kicker`. `.lede`, `.small`, `.micro`, `.muted`, `.soft`, `.num` replace `.lede`, `.small`, `.tiny`, `.muted`. `.figure` (+ `.figure--s`) is the condensed results-board numeral. `.prose` replaces `.read` and `.prose`.

**Layout**: `.stack` (`--s`/`--l`/`--xl`), `.row` (`--between`, `--nowrap`), `.cols--2/3/4`, `.split--7-5 / 8-4 / 6-6 / 5-7`, `.sticky` (desktop only), `.bleed` (escape gutters on phone). `.view`, `.grid`, `.card` go away: content sits on the page between rules; only use `.panel` (`--sunk`, `--band`) where a surface genuinely groups something.

**Buttons**: `.btn` (outlined ink), `.btn--primary` (pink, one per screen), `.btn--ink`, `.btn--quiet`, `.btn--on-band`, sizes `.btn--s` / `.btn--l`, `.btn--block`. Old → new: `.btn.sun` → `.btn--primary`; `.btn.primary` → `.btn--ink`; `.btn.ghost` → `.btn--quiet`; `.btn.sm` → `.btn--s`; `button.lnk` → `.linkbtn`. Text links to "more" use `.more`.

**Controls**: `.seg` (segmented, `aria-pressed`), `.seg--block`; `.chip` (filter, `aria-pressed`, `.chip--menu` opens a sheet with options instead of a `<select>`), `.chips`, `.chips--scroll`; `.input`, `.input-icon`; `.range` (style `--fill:%`); `.switch`. **No `<select>` elements**: topic, party and pollster pickers become chip rows or a chip that opens a sheet.

**Scrubber** (map, parliament, any time series):
```html
<div class="scrubber">
  <button class="scrubber__play" aria-label="Play through the years"><svg class="i i-play"><use href="#i-play"/></svg><svg class="i i-pause"><use href="#i-pause"/></svg></button>
  <div class="scrubber__main">
    <div class="scrubber__head"><div class="scrubber__year" aria-live="polite"><span>2023</span></div><span class="scrubber__note">2020 boundaries · 65 seats</span></div>
    <div class="scrubber__track"><input class="range" type="range" min="0" max="5" value="4" style="--fill:80%" aria-label="Election year">
      <div class="scrubber__stops"><span aria-current="false">2011</span>…<span aria-current="true">2023</span>…</div></div>
  </div>
</div>
```
Set `data-playing` on `.scrubber` while playing. Re-render the year as a new `<span>` each step (it animates in). Step every 1200ms. Map/seat fills transition on their own.

**Lists**: `.rows` > `.rowlink` (icon, title, sub, chevron) for navigation lists; `.dl`; `.resume` + `.ring` (`--p`) for progress.

**Data atoms**: `.sw` swatch (`--pc`), `.ptag` party tag (swatch + name), `.badge` (`--ink`, `--signal`, `--outline`, `--live`), `.stat`/`.stats`, `.bar > i` (`--w`, `--pc`, `--i` for stagger), `.rbar` with `.rbar__band` / `.rbar__mean` / `.rbar__mark` (`--lo --hi --m --x` in %), `.rrow` (name · bar · value), `.verdict.v-kept|v-partly|v-progress|v-broken|v-abandoned|v-notdue` (always with its icon), `.vmeter > i.v-*` (`--n`), `.legend`, `.iconarray > i.on` (100 cells), `.src` (source line).

**Today**: `.hero` (+ `.hero__count`, `.hero__ctas`, `.track > li[aria-current=step]`), `.twovotes`, `.feed > .feed__item` (`.feed__k`, `.feed__t`), `.potd`, `.otd` (`.otd__year`), `.changes`, `.release`.

**Vote**: `.tick` (SVG: `<svg class="tick" viewBox="0 0 28 28"><circle cx="14" cy="14" r="12"/><path d="M8.5 14.5l3.6 3.6L19.5 10"/></svg>`; parent `.is-done` or `.tick.is-on` draws it), `.checklist > .check` (`.check__t`, `.check__d`, `.check__a`), `.deadline`, `.progress-line`, `.persona` (buttons, `aria-pressed`), `.finder` (+ `.finder__or`), `.found` (+ `.found__alt`), `.cands > li > .cand`, `.face` (`--pc`; `.face--none` with initials when no photo; `.face--l`), `.duel` / `.duel__row`, `.margin`, `.plan` (+ `.plan__q`).

**Choose**: `.tools` > `.tool` (`.tool--lead` for the one dark tile) with `.tool__k`, `.tool__t`, `.tool__art` (inline SVG; accent shapes get `class="art-accent"`), `.tool__p`, `.tool__meta`, `.tool__go`; `.lens` table.

**Quiz**: `.quizbar` (`.quizbar__meta`, `.quizbar__dims > i` with `--p` per theme, `aria-current="step"` on the current theme), `.statement`, `.likert` (`role="radiogroup"`) > `.likert__opts` > `button.likert__opt[role=radio][aria-checked]` > `.likert__dot` > `.tick`; `.quiz-nav`; `.locked`. Results: `.mrow` (`--pc`; `.mrow--thin` for under-10 coverage) with `.mrow__name`, `.bucket--strong|moderate|weak|thin`, `.mrow__bar` (`--lo --hi --m`) > `i` + `b`, `.mrow__cov` > `.coverage` (`--c`); `.dims > .dim` (`.dim__axis` > `.dim__pt` with `--x` and `--pc`, `.dim__pt--you`); `.unknowns`.

**Swipe**: `.deck` > `.scard--behind2`, `.scard--behind`, `.scard` (`.scard__stamp`, `.scard__blind`, `.scard__s`, `.scard__body`); `.swipe-actions` > `.swipe-btn--disagree|skip|agree` (`<i>` holds the icon); `.reveal` (`--pc`) > `.reveal__who` > `.reveal__name`; `.tally > .tally__row`.

**Party**: `.phead` (`--pc`; `.phead__id`, `.phead__tag`), `.ptabs` (`aria-current="true"`), `.party-layout` with `.glance` (a `<dl>`), `.party-layout__main`, `.party-layout__side`; `.ideas` (auto-numbered), `.sides` > `.side` / `.side--critics`, `.works` > `.works__row`, `.pchip` / `.pchip--no`, `.terms > .term`, `.pol` (`.pol__t`, `.pol__m`).

**Map / Parliament**: `.mapstage` > `svg.nzmap` (paths get `fill` inline from data, `.is-sel` for the selected seat, `<text class="yr">` watermark), `.insets > .inset`, `.seatsheet` (`--float` sticks above the tab bar on phones; `.seatsheet__top`, `.seatsheet__grab`), `.history > div` (`--pc`, `aria-current`). Hemicycle: `svg.hemi` with `<circle style="--pc:…;--i:n">` per seat (seat fills and pop-in stagger come from CSS) and a `.maj` line at 61.

**Polls**: `.rrow`/`.rbar` for ranges, `.blocs > .bloc` (`.bloc__n`, `.bloc__who`, `.iconarray`), `svg.chart` (`.grid`, `.dot`, `.avg` with `--len` for the draw-in, `.end`, `.thr` + `.thr-l`, `.eday`); render a `.chart--narrow` (360-wide viewBox, lines only) and a `.chart--wide` (900-wide, with dots) and let CSS pick; `.table-wrap > .table`; `.unknowns`.

**People / news**: `.toolbar`, `.alpha`, `.people` > `h2.letter` + `a.person` (`.person__name`, `.person__meta`); `.pgroup` (`--pc`) > `.pgroup__h` + `.release` (`.release__t`, `.release__m`); `.follow > .follow__row` (`.follow__links`).

**Feedback**: `.note` (`--warn`), `.callout` (`--signal`), `.disclose` (`<details>`: summary + `.disclose__body`), `.depth`, `.lock`, `.toast`, `.countup` (`style="--to:15"`, CSS counts up).

---

## 5. What changes in each current view

| View | Changes |
|---|---|
| `V.home` | Rewrite to `mockups/home.html`: `.hero` with phase copy (see the table in IA.md §2.2), four `.rowlink` tasks, `.twovotes` (replaces the animated `.ballot` and `startBallot()`; keep the ballot illustration as a sheet behind "See the ballot paper" in Vote), Today `.feed`, `.resume` from `localStorage` keys `quiz2`, `swipe`, `myElectorate`. **Remove** the hemicycle hero, seven `.starter` cards, the party grid and the poll snapshot (poll watch links to Seats with no numbers). |
| `V.parties` | `partyOrder()` must stop sorting by poll. Default A–Z by short name, with a `.seg` for "Ballot order". Party rows use `.rowlink` with `.ptag`, tagline and MPs; no shadowed `.pcard`. |
| `V.party` | Header → `.phead`; stats → `.glance` (`<dl>`), placed first on phones by `.party-layout`; `.tabs` → `.ptabs`; "At a glance" sections become `.shead` sections in this order: In a nutshell, Big ideas (`.ideas`, each with "Read the full text" → `openSheet`), Two sides (`.sides`), Who they'd work with (`.works` with `.pchip` for `open_to` and `.pchip--no` for `rules_out`), Keeping their word, Costed?, Go deeper (`.rows`). `recordSummary()` → `.terms` of `.vmeter` + `.verdict` legend + the rubric in a `.disclose`. `partyResultsMini()` → `.rrow` bars in `.party-layout__side`. |
| `policyBrowser()` | `<select id="topic">` → `.chips--scroll` of topics (`aria-pressed`); party chips stay `.chip` but with `.sw`; rows → `.pol`; `<details>` → `.disclose`; `docButtons()` → one `.linkbtn` "Read the full text" that calls `openSheet`. |
| `V.issues` / `V.issue` | `V.issue` sorts `positions` **A–Z** (not by `projection().pct`). Positions render as a `.cols--2` of blocks with a 4px `--pc` top rule (like `.pgroup`), key facts as `.feed__item`-style rows with `.src`. |
| `V.match` | Intro → the Choose hub tile copy. Question → `mockups/quiz.html` in focus mode: `.quizbar` (six theme segments), `.statement`, `.disclose` "What does this mean?" (the statement's `explainer`), `.likert` replacing `.scale` buttons, importance as `.seg--block`, `.quiz-nav`. Results → `mockups/quiz-results.html`: **default sort A–Z** (the current code sorts by `match`), `.seg` to switch to closest-first or ballot order; every party shown; `.mrow` with buckets (strong ≥ 70, moderate 55–69, weak < 55, thin when `n < need`), range from `scLow` vs `match`, `.coverage`; `.dims` theme map comparing the user with up to two chosen parties; `.unknowns`. |
| `V.swipe` | Topic `<select>` → `.chips--scroll`; card → `.scard` in a `.deck` with two `.scard--behind*`; buttons → `.swipe-actions`; keep `attachDrag()` but set `.scard--tilt` and the stamp text past 60px. After each decision render `.reveal` (`--pc` of the revealed party) beside the deck on desktop / below it on phone. `V['swipe-tally']` folds into the same page as `.tally` (rate, not count; A–Z). |
| `V.compass` | Same focus-mode frame and `.likert` as the quiz. Results: plot "you" as the uncertainty box already computed (`me.x.half`, `me.y.half`) drawn with `--signal` at low opacity and a ring, not a dot; party placements toggle with `.seg` (the existing coded / published switch). Axis labels in `.chart text` style. |
| `V.game` | Focus mode; `.pchoices` buttons restyled as `.persona` buttons (`aria-pressed`, right/wrong via `.v-kept`/`.v-broken` outline); hand-off screen uses `.figure` for the player name. |
| `V.electorate` + `locateBlock()` | Move under Vote. `locateBlock()` → `.finder` (ink "Use my location — stays on your phone" + suburb `.input`). Result → `.found` (+ `.found__alt` for the Māori electorate) then `.cands` **in ballot order (A–Z by surname)**, `.duel` for the 2023 top two with `.margin`, actions row: Voting places (map.vote.nz), Print one-pager, Compare candidates. Remove the "Battleground" starter grid from the empty state; show the finder and "Browse all 71" as `.rows`. |
| `V.map` | Header → `.pagehead`; type chips → `.seg`; scrubber → `.scrubber` pattern; SVG → `.nzmap` (keep `projector`/`featPath`); side panel → `.seatsheet` (`--float` on phones, sticky panel on desktop) with `.history`; legend → `.legend` with `.sw--sq`; add a "List view" button that shows every seat and winner as text (colour must never be the only cue). |
| `V.parliament` | `.tabs` → the Seats `.subnav` (Parliament, Coalition builder, Seat calculator become sub-routes). `chamberSVG()` emits `svg.hemi` circles with `style="--pc:…;--i:${index}"` so fills and pop-in are CSS; the "After the election / End of term" switch → `.seg`. Calculator inputs → `.range` sliders with live seat output in `.figure--s`. |
| `V.polls` + `forecastSummary()` | Order: `.pagehead` → "If the election were held on today's polling" (`.rrow`/`.rbar` ranges, party vote/seats `.seg`) beside "Who could govern?" (`.blocs` with `.iconarray`, frequency wording "N in 100", bloc swatches neutral) → trend (`pollChart()` emits both `.chart--narrow` and `.chart--wide`; party/pollster chips) → `.unknowns` beside the track record table (misses listed from `historical_track_record`) → latest-by-pollster `.table` → Māori seats with a "Low confidence" badge. **Drop** the stat tiles and the "Most likely Parliament" headline. |
| `V.people` / `peopleGrid()` | `.toolbar` with `.input-icon` search and `.chips--scroll` filters (status chips with counts; party and electorate as `.chip--menu`); `.alpha` rail; list → `.people` with `h2.letter` per initial and `a.person` rows. **Sort A–Z by surname** for every filter (the current default groups by party). `openPerson()` → `openSheet()`. |
| `V.promises` / `promiseList()` | `.seg` for the period switch (`periodBar()`), `.vmeter` per party (A–Z), `.verdict` chips with icons on every promise, the rubric in a `.disclose` at the top. |
| `V.trust`, `openPage()` | Long-form pages render in `.prose` inside a normal page (`#/about/…`), with the footer links pointing to them. |
| `V.more` | Delete. |
| new `V.vote` | `mockups/vote.html`: `.checklist` driven by `data/guide/howtovote.json` → `checklist` (ticks saved to `localStorage['vote-ticks']`), `.persona` driven by `sections[].who_its_for`, plan builder producing an `.ics` blob and an `sms:`/WhatsApp link. |
| new `V.choose` | `mockups/choose.html`. |
| new `V.news` | `mockups/newsroom.html`; three per party, A–Z, `.seg` for "Newest first"; ministerial releases get `.badge` "Ministerial". |
| `autolink()` | Keep; it now creates `.linkbtn`. Add `.statement, .scard__s, .potd__s, .release__t, .ptag` to its skip list. |

---

## 6. Motion

All durations come from tokens and collapse to 1ms under `prefers-reduced-motion` (the scrubber still steps, just without the roll).

| Moment | How |
|---|---|
| Route change | View Transitions (`main { view-transition-name: main }`), fallback `.page-enter` on `#main` |
| Year change (map, parliament) | New `<span>` in `.scrubber__year` (`yearIn`); path/seat `fill` transitions `--dur-4` |
| Seats appear | `.hemi circle` `seatIn` with `--i × --stagger` |
| Bars and ranges | `grow` on `.bar > i`, `.rbar__band`, `.mrow__bar > i`, `.vmeter > i` (stagger with `--i`) |
| Ticks | `.tick path` dash-offset when `.is-done`/`aria-checked` |
| Reveal | `.reveal__who::before` wipes in the party colour; `.reveal__name` rises |
| Swipe | Spring (`--ease-spring`) on `.scard`; JS translates/rotates the front card |
| Numbers | `.countup` (`@property --n`) |
| Phase "you are here" | `pulse` on `.track li[aria-current=step]` and `.phase__dot` |

---

## 7. Neutrality checklist (check every ported view)

- Party lists A–Z by short name, or ballot order, with a visible note. **Only** `#/seats/polls` sorts by polling, and says so.
- Candidates in ballot order (A–Z by surname). People A–Z by surname for every filter.
- No party colour outside `--pc` marks. The brand pink is never used for a party, a bloc or a chart series other than "you".
- Quiz/swipe/compass results: all parties shown, no single winner, ranges not decimals, coverage visible, never beside the forecast.
- Probabilities as "N in 100" with an icon array; ranges before middles; misses shown.
- Every summary has a `.src` line and a dated "checked" note; every result has "How this could be wrong".
- Same fields, same photo crop (`.face`), same order of sections on every party and person page.

---

## 8. Suggested order

1. **Shell and tokens** (half a day): fonts, styles, sprite, header/phase/tabbar/footer, `SECTIONS`, router with the redirect table, `openSheet()`. Old views will render with the new base styles; check nothing breaks at 390px.
2. **Today and Vote** (the enrolment deadline is 25 Oct): `V.home`, `V.vote`, `V.electorate` + finder. Ship.
3. **Election-day lock and phase ribbon** for all phases; test by faking `nzNow()`.
4. **Choose**: hub, quiz (question + results, A–Z default), swipe (+ tally), then compass and game into focus mode.
5. **Seats**: polls/forecast, map scrubber, parliament/coalition/calculator. Then the Results view for 7 Nov (it reuses `.hemi`, `.rrow`, `.rbar` and the map).
6. **Parties**: party page, policies, issues, people, promises, news.
7. Delete `V.more`, the old dialog and dead CSS; run the QA list.

## 9. QA before each ship

- 390×844 and 1280×900, light and dark (system and toggle), no horizontal scroll (`document.documentElement.scrollWidth === innerWidth`).
- Reduced motion on: nothing animates, the scrubber still steps.
- Keyboard: tab order follows the page, `/` focuses search, Esc closes the sheet, the likert is a radiogroup, every chip/seg has `aria-pressed`.
- Contrast: tokens are checked (text ≥ 4.5:1, controls ≥ 3:1 in both themes); party colours never carry text.
- Colour is never the only cue: maps have a list view, verdicts have icons and words, buckets have words.
