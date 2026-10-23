# Contributing

Ballot Book NZ is an independent, non-partisan voter guide. The most valuable contribution is a **correction with a source**.

## Report an error
Open an issue using the "Correction" template. Say which page or file, what's wrong, what's right, and link to a source (party document, official release, reputable news report). Corrections to a party's policy are checked against the party's own published text.

## Standards
- Every factual claim needs a source link. No claim is kept on memory alone.
- Neutral language. Describe what a party proposes; don't evaluate it. The same standard applies to every party. See `docs/EDITORIAL_STANDARDS.md`.
- Full-text policy documents are reproduced exactly as published. If a source can't be retrieved, the file says so rather than paraphrasing.
- Promise verdicts (kept / partly kept / broken / abandoned / in progress) follow the definitions in each party's `track-record.md` and are applied identically across parties.

## Making changes
- Data lives in JSON under `data/` and `parties/*/policies/policies.json`; the readable Markdown and the site are generated from it.
- After editing data: `python3 tools/build_site.py` (site bundle), `python3 tools/guide_render.py` (guide pages), `python3 tools/report_stats.py --write` (report tables), `python3 -I tools/quiz_build.py` (quiz).
- Person profiles: the block between `<!-- GENERATED:2026-candidacy START/END -->` is rebuilt by `tools/build_candidates.py` — edit outside it.
- Keep `raw/` HTML caches out of git (see `.gitignore`); PDFs under 10 MB are kept as the source of record.

## Pull requests
Small, sourced, one topic per PR. Describe what changed and why, with links.
