> **Status (24 Oct 2026): the port is complete.** `site/src/` is now the redesigned app and `site/index.html` is built from it. This file is kept as the record of how the port was organised.

# Porting the redesign — shared brief for the view agents

Read first: `site/redesign/IA.md` (why), `site/redesign/PORTING.md` (how: shell, routes, class names, per-view changes,
neutrality checklist, QA list), the mockup HTML for your screens in `site/redesign/mockups/`, and `docs/AGENT_BRIEF.md`
(editorial and legal rules). `docs/LEGAL_REVIEW.md` §2 lists the legal constraints the app already implements; keep them.

## Where things are

- **Source being ported (now `site/src/`):** `site/src-next/` — `shell.html` + `css/*.css` + `js/*.js`, concatenated in filename order by
  `python3 tools/build_site.py` into `site/new.html` (preview). The live site (`site/index.html`) is built from `site/src/`
  and must not be touched. Every function is global across files; keep names unique.
- **Already done (stage 1, do not edit):** `shell.html`, `css/00-tokens.css`, `css/01-components.css`, `js/00-core.js`,
  `js/25-phase-locate-autolink.js`, `js/60-trust.js`, `js/61-pages.js`, `js/90-shell-router.js`.
  - Routes: `#/section/sub/arg`, resolved in `resolve()` in `90-shell-router.js`. View functions are called with the
    arguments listed there (e.g. `V.party(slug, tab)`, `V.electorate(slug)`, `V.map(year, slug)`, `V.vote(sub)`,
    `V.newsroom(party)`, `V.match(arg)`, `V.results()`, `V.compare(arg)`, `V.choose()`). Old hashes and `data-go` values
    are translated by `normaliseRoute()`; `go(path)` navigates; `route` is an alias of `go`.
  - Navigation: `sectionFrame(sec, currentKey, html)` wraps a view in the section chrome (sub-nav chip row / rail).
    `SUBNAV` in the router lists the sub-items; add an item there only if your brief says so.
  - `openSheet({ title, depth, at, src, html, route })` is the layer-3 sheet; `openDialog(title, html)` still works.
  - `focusMode('Find your match', 'choose')` turns on the distraction-free header; `focusMode(null)` turns it off (the
    router does this on every route change, so call it after rendering each question screen).
  - Icons: `ic('name', 'i--s')` from the sprite (names in PORTING.md §1). Phase: `electionPhase()`, `renderPhase()`,
    `blockedToday(view)`, `ELECTION_DAY_BLOCK`, `RESULT_DISCLAIMER` (must appear on every result page), `NOT_EC`.
  - `S` is the shared state (`S.data` = bundle, `S.people`, `S.thumbs`, `S.pages`, `S.swipe`, `S.news`…), `store`
    wraps localStorage, `$`, `esc`, `getJSON`, `P(slug)`, `pname`, `pcolor`, `G()` (guide data), `fmt`, `T`, `srcLinks`.
- **CSS:** the design system is complete; use its classes. If you genuinely need extra rules, add them in your own file
  `css/10-<section>.css` (tokens only, no raw colours, both themes). Never edit `00-tokens.css` or `01-components.css`.
- **Data:** `site/data/*.json` (bundle, policies, people, thumbs, pages, swipe, newsroom, forecast inside bundle,
  geo/, fulltext/). Do not change `tools/build_site.py`; if you need a data shape change, say so in your report.

## Rules

1. Edit **only the files you own** (listed in your prompt). Do not touch other agents' files, the shell, the router, the
   bundler, `site/src/`, `site/index.html`, or anything under `data/`, `parties/`, `tools/`. Do not run git commands.
2. Keep every existing feature of the views you port (the old code is your spec for behaviour; the mockups and
   PORTING.md §5 are your spec for structure and look). Data shown must stay sourced and dated.
3. Neutrality (PORTING.md §7): A–Z or ballot order everywhere except the polls page; all parties shown on every result;
   no single winner; ranges not decimals; party colour only via `--pc`; never pink for a party.
4. Legal (already built, keep): `blockedToday()` views render the lock; `RESULT_DISCLAIMER` on match/compass/swipe
   results; `NOT_EC` line on Today, Vote and electorate; geolocation consent wording in the finder; no imitation ballot
   with a voting direction; no "who will you vote for" questions; headlines-only newsroom.
5. Phone first: 390×844 then 1280×900, light and dark. No horizontal scroll (`scrollWidth === innerWidth`), nothing
   under 11px, `prefers-reduced-motion` respected (the CSS does most of this).
6. Verify in a browser. A static server is on `http://localhost:8765/` serving `site/` (if it is down, start one:
   `cd site && setsid nohup python3 -m http.server 8765 >/dev/null 2>&1 &`). Rebuild with `python3 tools/build_site.py`,
   then open `http://localhost:8765/new.html#/<your route>`. Playwright: `NODE_PATH=/opt/node22/lib/node_modules node …`
   with `chromium.launch({ executablePath: '/opt/pw-browsers/chromium' })`; a ready harness is
   `/tmp/claude-0/-home-user-Politicsnz/2c7d5a5b-def6-5680-ab5e-66728dbb1a3b/scratchpad/shotnew.js` (args: `route` or
   `route@390`; prints OVERFLOW and page errors; screenshots next to it as `n-<route>-<width>.png`). Look at your
   screenshots. Zero console errors on every route you own.
7. Report back with: files changed, routes to look at, screenshots path, anything you could not do and why, and any
   data or router change you need from the coordinator.
