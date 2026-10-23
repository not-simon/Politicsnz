# Repository layout & data schema

Everything is plain Markdown + JSON so it reads well on GitHub and feeds the interactive site in `site/`.

```
README.md                      Start here: index + how to use
REPORT.md                      The comprehensive report (trends, reliability, promises, alignment)
elections/<year>.md            Narrative of each election 2011, 2014, 2017, 2020, 2023 + 2026.md (upcoming)
elections/trends.md            Cross-election trends
data/elections/<year>.json     Results (schema below)
data/parliaments/<n>.json      Membership of the 50th-54th Parliaments (schema below)
data/polls-2026.json           2026 opinion-poll series
data/promises/<party>.json     Promise tracker entries (schema below)
parties/<party>/README.md      Party profile
parties/<party>/track-record.md   Promises vs delivery, reliability, policy/action alignment
parties/<party>/policies/README.md            Every 2026 policy, grouped by topic, with summaries
parties/<party>/policies/policies.json        Structured list of the same
parties/<party>/policies/documents/<doc>.md   FULL VERBATIM text of each source policy document/page
parties/<party>/people/<person>/README.md     Person profile (+ photo.jpg, person.json)
raw/                           Untouched source downloads (policy.nz JSON etc.)
tools/                         Scripts that fetch/build everything
site/                          Interactive viewer (parliament maps, trends, coalition builder, policy browser)
```

## Party folder slugs
Current/2026: `national, labour, green, act, nz-first, te-pati-maori, opportunity` (TOP), `nz-loyal, nz-outdoors-freedom,
legalise-cannabis, animal-justice, alliance, conservative, womens-rights, vision-nz, free-palestine, te-tai-tokerau-party`
plus small electorate-only groups. Historical (2011-2023): `united-future, mana, internet-party, new-conservative`(if distinct
from `conservative`), `advance-nz, freedoms-nz, democracynz, newzeal, social-credit, heartland, sustainable-nz, ban-1080,
leighton-baker, ...` — use lowercase-hyphen names. The Māori Party = `te-pati-maori`; TOP = `opportunity`.

## data/elections/<year>.json
```json
{"year": 2023, "date": "2023-10-14", "parliament": 54, "turnout_pct": 78.2, "enrolled": 0, "votes_cast": 0,
 "overhang": 2, "total_seats": 123,
 "parties": [{"party": "national", "name": "National", "party_votes": 0, "party_vote_pct": 38.06,
              "electorate_seats": 43, "list_seats": 5, "total_seats": 48, "electorate_votes_pct": 0}],
 "government": {"formed": "2023-11-27", "pm": "Christopher Luxon", "parties": ["national","act","nz-first"],
                "arrangement": "coalition", "support": [], "notes": "..."},
 "electorates": [{"name": "Botany", "winner": "Christopher Luxon", "party": "national", "majority": 0, "runner_up": "..", "runner_up_party": ".."}],
 "sources": ["https://..."]}
```

## data/parliaments/<n>.json
```json
{"parliament": 54, "election_year": 2023, "start": "2023-12-05", "end": null,
 "composition_start": {"national": 48, "labour": 34},
 "composition_now_or_end": {"national": 49},
 "members": [{"name": "Christopher Luxon", "slug": "christopher-luxon", "party": "national",
              "seat": "Botany", "type": "electorate|list", "entered": "2023-10-14", "left": null,
              "left_reason": null, "party_changes": [], "notes": ""}],
 "changes": [{"date": "", "description": "by-election / resignation / defection ..."}],
 "sources": []}
```
Person `slug` = lowercase ASCII, hyphenated, macrons stripped (e.g. `chloe-swarbrick`, `hana-rawhiti-maipi-clarke`). Use the same slug policy.nz uses where it exists (folders already exist under `parties/*/people/`).

## parties/<party>/people/<slug>/person.json
```json
{"name": "", "slug": "", "party": "<current/most recent party>",
 "party_history": [{"party": "", "from": "", "to": ""}],
 "status": "current-mp | candidate-2026 | current-mp-standing-2026 | current-mp-retiring | former-mp | deceased | party-official",
 "status_detail": "free text: what they are doing now (Oct 2026)",
 "roles": ["Prime Minister (2023-)"], "parliaments": [52, 53, 54], "first_elected": 2017,
 "electorate_2026": null, "list_rank_2026": null, "born": "", "wikipedia": "",
 "photo": "photo.jpg", "photo_source": "url", "photo_credit": "", "photo_license": "",
 "sources": ["url", "..."]}
```
README.md for a person: `# Name`, photo, quick facts, then sections: Current status, Biography, Political career,
Positions & notable votes/actions, Controversies (factual, sourced), 2026 candidacy (the auto-generated block between
`<!-- GENERATED:2026-candidacy START -->` / `END -->` markers — never edit inside it, it is rebuilt by `tools/build_candidates.py`), Sources.

## parties/<party>/policies/policies.json
```json
[{"id": "POL54642", "statement": "Allow pharmacists to treat more sicknesses", "topics": ["health"],
  "summary": {"why": "...", "how": "..."}, "summary_source": "policy.nz",
  "sources": [{"title": "", "url": "", "document": "documents/<doc-slug>.md"}]}]
```
`documents/<doc-slug>.md`: front matter (`title, party, source_url, retrieved, format: html|pdf, fetch_method`) then the
complete text exactly as published (only whitespace/markup normalised). If a source could not be retrieved, the
document file says so explicitly with the reason — never paraphrase inside a "full text" section.

## data/promises/<party>.json
```json
[{"promise": "", "made": "2023 election", "category": "", "status": "kept|partially-kept|broken|in-progress|abandoned|not-yet-due",
  "detail": "what happened", "sources": ["url"]}]
```
