# App source

The interactive guide is one static page assembled by `tools/build_site.py` from:

- `shell.html` — the page markup (masthead, phase ribbon, five-section tab bar, sheet, footer). `/* @CSS */` and `/* @JS */`
  are replaced at build time.
- `css/*.css` — `00-tokens.css` and `01-components.css` are the design system (from `site/redesign/`); `05-compat.css` holds
  two aliases; `10-*.css` are per-section additions. Tokens only, light and dark.
- `js/*.js` — concatenated in filename order into a single classic `<script>`: `00-core` (state, helpers, `V = {}`),
  `10-mmp-chamber` (MMP maths, hemicycle, scrubber), `20-people-helpers`, `25-phase-locate-autolink` (election phase,
  geolocation, auto-linking, saved-answer export), then one file per view group — `30` Today, `31` Vote, `32` electorate,
  `33` parties, `35` policies and issues, `36` people, `37` promises, `38` newsroom, `40` compass, `41` quiz, `42` swipe,
  `43` game, `44` Choose hub/results/compare, `50` map, `52` Parliament, `55` polls, `56` results, `60` about, `61` pages,
  `62` search — and `90-shell-router` (sheet, navigation, routes `#/section/sub/arg`, redirects for old hashes, boot).

Build: `python3 tools/build_site.py` writes `site/index.html` and `site/artifact.html` plus `site/data/`.
Every function is global across files; keep names unique. Structure and class names follow `site/redesign/PORTING.md`.
