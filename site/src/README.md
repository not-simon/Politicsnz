# App source

The interactive guide is one static page assembled by `tools/build_site.py`:

- `shell.html` — the page markup. `/* @CSS */` and `/* @JS */` are replaced at build time.
- `css/*.css` — stylesheets, concatenated in filename order.
- `js/*.js` — the app, concatenated in filename order into a single classic `<script>` (no modules, no bundler).
  Files are numbered so shared helpers come first: `00-core` (state, helpers, `V = {}`), `10` MMP maths and hemicycle,
  `20` people helpers, `25` election phase / locate / autolink / save-export, `30`–`61` one file per view (30 home, 31 vote, 32 electorate, 33 parties, 35 policies+issues, 36 people, 37 promises, 38 newsroom, 40 compass, 41 quiz, 42 swipe, 43 game, 50 map, 52 parliament, 55 polls, 60 trust, 61 pages) or view group,
  `90-shell-router` (dialog, event delegation, `route()`, boot).

Build: `python3 tools/build_site.py` writes `site/index.html` (standalone) and `site/artifact.html` (fragment) plus `site/data/`.
Every function is global across files, so a view file may call helpers from any other file; keep names unique.
