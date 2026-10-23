# App source

The interactive guide is one static page assembled by `tools/build_site.py`:

- `shell.html` — the page markup. `/* @CSS */` and `/* @JS */` are replaced at build time.
- `css/*.css` — stylesheets, concatenated in filename order.
- `js/*.js` — the app, concatenated in filename order into a single classic `<script>` (no modules, no bundler).
  Files are numbered so shared helpers come first: `00-core` (state, helpers, `V = {}`), `10` MMP maths and hemicycle,
  `20` people helpers, `25` election phase / locate / autolink / save-export, `30`–`61` one file per view or view group,
  `90-shell-router` (dialog, event delegation, `route()`, boot).

Build: `python3 tools/build_site.py` writes `site/index.html` (standalone) and `site/artifact.html` (fragment) plus `site/data/`.
Every function is global across files, so a view file may call helpers from any other file; keep names unique.
