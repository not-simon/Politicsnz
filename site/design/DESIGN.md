# Ballot Book NZ — visual identity

Files in this folder: `tokens.css` (all design tokens, light + dark), `components.css` (every class in the component contract), `icons.svg` (SVG symbol sprite), and seven static mockups (`home.html`, `party.html`, `quiz.html`, `swipe.html`, `polls.html`, `map.html`, `parliament.html`). The mockups inline the sprite and link the two stylesheets relatively; open any of them directly in a browser.

## 1. Direction: "a field guide, not a feed"

Ballot Book should feel like a well-made printed voter booklet that happens to live on your phone: calm, left-aligned, generous with white space, confident type, and almost no decoration. It is not a news site (no red breaking-news energy, no dense grids of headlines), not a party site (no flooding the screen with one colour), and not a dashboard (no wall of tiles). Everything the reader sees is either text, a hairline, or data.

Four rules carry the identity:

1. **Ink on stone.** Neutral surfaces (`--bg` #F3F3EF stone, `--surface` white) with a near-black ink (`--text` #171D1C). The primary button is ink, not a brand colour, so no party's colour is ever "the brand".
2. **One highlight.** A single warm orange, `--sun` (#E8600A light / #F58A3C dark), appears in exactly four places: the one highlighted call-to-action on a screen (`.btn.sun`, the `.starter.hot` on Home), focus rings, link underlines, and the "NZ 2026" tag in the logo. Orange is the colour New Zealanders already associate with voting, and no registered party uses it. Never use it for a second button on the same screen.
3. **Party colour is an accent, never a flood.** Party colours are data and are kept exactly. They appear as a 4px stripe (`.pcard::before`, `.seatcard`, `.position::before`), a ring around a face (`.face` `--pc`), a 10px `.dot`, and as marks in charts. A tinted wash (`color-mix(... 7%)`) is the maximum area fill, used only on issue-page `.position` cards. Text is never coloured with a party colour.
4. **Hairlines over shadows.** Surfaces are separated by 1px lines (`--line`) and small radius (10–16px). The only shadow in the system is on things that genuinely float: the swipe card stack, dialogs, tooltips.

Things deliberately avoided: purple gradients, cream+serif+terracotta, Inter/Space Grotesk, emoji as icons, centred everything, every block a shadowed card.

## 2. Type

Three Google Fonts, loaded with one `<link>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Atkinson+Hyperlegible+Next:wght@400..800&family=Geist+Mono:wght@400..600&display=swap" rel="stylesheet">
```

| Role | Face | Why |
|---|---|---|
| Display (`h1`, `h2`, hero numbers, `.qtext`, `.stmt`, stat values, `.count`) | **Bricolage Grotesque** (variable, optical size 96) | Distinctive, slightly idiosyncratic grotesk with wide bold weights; reads as a civic poster rather than a startup. Tight tracking (-0.02em) at display sizes. |
| Body / UI (everything else) | **Atkinson Hyperlegible Next** | Designed by the Braille Institute for low-vision readers; unambiguous letterforms (slashed zero, distinct I/l/1) suit a guide whose job is accuracy. Weights 400–800 available for UI. |
| Figures (`.num`, table cells, axis ticks, kickers) | **Geist Mono** | Tabular by nature; used for poll percentages, seat counts, dates and the small uppercase `.kicker` labels so figures line up in columns. |

Type scale (fluid between 390px and 1200px; tokens in `tokens.css`):

| Token | Size | Use |
|---|---|---|
| `--t-tiny` | 12px | `.tiny`, badges, kickers, axis text |
| `--t-small` | 13.5px | `.small`, chips, table body, meta |
| `--t-body` | 16px | body, line-height 1.55 |
| `--t-lede` | 17 → 20px | `.lede`, max 66ch |
| `--t-h4` | 17px | `h4` (body face, 700) |
| `--t-h3` | 19 → 22px | `h3` (body face, 700) |
| `--t-h2` | 24 → 30px | `h2` (display face) |
| `--t-h1` | 32 → 48px | `h1` (display face) |
| `--t-display` | 44 → 72px | countdown, bloc-probability numbers |

Kickers (`.kicker`) are 12px mono, uppercase, +0.08em tracking, muted. They label sections instead of extra heading levels, which keeps the page quiet.

## 3. Spacing, shape, motion

- 4px base: `--s-1` 4 · `--s-2` 8 · `--s-3` 12 · `--s-4` 16 · `--s-5` 24 · `--s-6` 32 · `--s-7` 48 · `--s-8` 64. Sections are separated by `--s-7` on phones and `--s-8` on desktop.
- Side gutter: `max(16px, env(safe-area-inset-left))` (and right). Page max-width 1200px. Prose max 66ch.
- Radius: `--r-sm` 6 (table head corners, small boxes) · `--r` 10 (controls, stats) · `--r-lg` 16 (cards) · 22px (swipe cards) · pill for chips, badges, meters.
- Controls are 44px tall (`.btn`, inputs, selects); `.btn.sm` and `.chip` 34px. Bottom tab bar items 56px.
- Motion: 180ms / 320ms with `cubic-bezier(.2,.7,.2,1)`; everything collapses to 0ms under `prefers-reduced-motion`. Only transforms, opacity and background animate.

## 4. Colour system

All colours are tokens on `:root`. Light values on bare `:root`; dark via `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) }` and `:root[data-theme="dark"]`, both setting `color-scheme: dark`.

### Neutrals (light → dark)

| Token | Light | Dark | Role |
|---|---|---|---|
| `--bg` | #F3F3EF | #111514 | page (body background is explicit) |
| `--surface` | #FFFFFF | #1A1F1E | cards, header, dialogs |
| `--surface-2` | #ECECE6 | #232928 | sunken areas, meter tracks, table head, flat cards |
| `--surface-3` | #E2E3DC | #2C3331 | hover of surface-2 |
| `--text` | #171D1C | #ECEEEA | ink |
| `--text-2` | #4A5250 | #B6BDB9 | secondary |
| `--text-3` | #5F6866 | #8E9692 | muted (≥ 4.5:1 on bg, surface and surface-2 in both themes) |
| `--line` / `--line-strong` | #D9DAD3 / #B9BBB2 | #2E3533 / #434B48 | hairlines / control borders |
| `--ring` | ink 18% | paper 28% | 1px ring inside party swatches |

### Brand

| Token | Light | Dark |
|---|---|---|
| `--primary` / `--on-primary` | #171D1C / #FFFFFF | #ECEEEA / #111514 |
| `--sun` / `--on-sun` | #E8600A / #1A1200 (5.4:1) | #F58A3C / #1A1200 (7.6:1) |
| `--sun-text` (sun used as text) | #B9460A (4.8:1 on bg) | #F58A3C (7.5:1 on bg) |
| `--focus` | = sun | = sun |
| `--link` / `--link-underline` | ink / sun | paper / sun |

Links are ink with an orange underline, so they are visible without being another colour of text.

### Semantic verdicts (promise tracker)

Always shown with a label and a leading dot (`.verdict`), never colour alone. Light values pass 4.5:1 on white; dark values pass on `--surface`.

| Class / token | Light | Dark | Meaning |
|---|---|---|---|
| `.v-kept` `--v-kept` | #1B7F4C | #4CC27F | kept |
| `.v-partially-kept` | #9A6410 | #E0A94A | partly kept |
| `.v-broken` | #C2342B | #F07167 | broken |
| `.v-abandoned` | #5F6866 | #9AA19D | abandoned |
| `.v-in-progress` | #1A7A8A | #5BBFD0 | in progress |
| `.v-not-yet-due` | #B9BBB2 (hollow dot) | #434B48 | not yet due |

State washes for notes/badges: `--info-*`, `--warn-*`, `--good-*`, `--bad-*` (bg + text pairs, all ≥ 4.5:1).

### Party colours (data, unchanged)

National #00529F · Labour #D82A20 · Green #0B8A3E · ACT #F2C300 · NZ First #2B2B2B · Te Pāti Māori #B2001A · Opportunity #1FB5A3 · others per `data/parties-meta.json`. Set them inline as `--pc` on `.pcard`, `.face`, `.dot`, `.match`, `.frow`, `.seatcard`, `.position`, map paths, etc.

Legibility rules for the hard cases:
- **NZ First (#2B2B2B)** on dark surfaces and **ACT (#F2C300)** on light surfaces get a ring: `.dot` has `inset 0 0 0 1px var(--ring)`; chamber seats and compass/poll end-dots for these parties carry the `.ring` class (stroke `--text-3`); `.face` rings sit on a 2px surface gap.
- Text on a party fill: white on National, Labour, Green, Te Pāti Māori; ink on ACT (`.ink-dark`) and Opportunity. Avoid text on fills where possible; the `.bar` is the only component that does it.
- Never colour text in a party colour; identity comes from the dot or stripe beside the text.

### Charts

Tokens: `--chart-grid`, `--chart-axis`, `--chart-text`, `--range-band`, `--majority`, `--map-empty`, `--map-stroke`, `--me`, `--me-ring`.

## 5. Chart style rules

- Marks carry colour; text wears text tokens. Axis text is 11px mono in `--chart-text`.
- Gridlines are 1px solid `--chart-grid`, recessive; a single baseline axis in `--chart-axis`. No dual axes, ever.
- Bars ≤ 24px thick, 4px rounded data-end, square at the baseline. Stacked segments and adjacent bars are separated by a **2px surface gap** (`.meter`, `.bar` use `gap: 2px`), not strokes.
- Lines 2.25px, round joins. Poll dots r=3.5 at 55% opacity; trend end-dots r=5 with a 2px surface ring (`.ring`). Dimmed series use `.poll.dim` / `.seat.dim` (opacity .18–.22) rather than removal, so colour stays attached to the entity.
- Direct labels only at line ends and bar tips; a legend (`.legend .item`) is always present for two or more series.
- The 5% threshold is a dashed `--text-3` line labelled once, at the left.
- Forecast ranges: `--range-band` wash with a 3px party-coloured marker for the central estimate.
- Big numbers (`.bignum`, `.count`, `.stat b`) are Bricolage Grotesque; exactly one hero number group per view.
- Wide charts live in `.chart.wide` (min-width 640px) inside an `overflow-x:auto` container so phones scroll the chart, not the page. Tables sit in `.table` for the same reason.
- Hemicycle: r=10 seats with a 1.5px surface stroke; `120` and "61 for a majority" in the arc's mouth.

## 6. Components worth knowing

- `header.top` is sticky with `top: env(safe-area-inset-top)`; desktop `nav.nav` hides under 900px and `nav.bottombar` (6 items, SVG + label, current item gets an ink underline and orange icon) takes over.
- `.sechead` = kicker + h2 + optional right-aligned aside over a hairline; stacks on phones.
- `.starter` cards switch from horizontal (icon · text · arrow) on phones to tall tiles on desktop; `.starter.hot` is the single orange entry point.
- `.pcard` carries a 4px party stripe; in `.parties-row` the name may wrap and the poll % sits under it.
- `.party-hero` places leader `.faces` (party ring) beside the name; `.stats .stat` are four quiet tiles.
- `.ideas` is a checklist with ink boxes (CSS-only ticks); `.quote.they` uses the party colour as its rule, `.quote.critics` uses muted ink.
- `.scale button[aria-pressed]` is the 5-point agree control (pressed = ink); `.toggle` is the importance switch (on = orange).
- `.scard` stack: `.top`, `.back`, `.back2`; stamps `.stamp.yes/.no` show on drag direction (`data-dir`) or `.show`; `.scard.reveal` borders in the party colour.
- `.scrubber` = round ink play button + range input + year labels; `.map .inset` are boxed cut-outs; `.map .year` is a large display year in the corner.
- `dialog` is a bottom sheet on phones and a centred 720px panel on desktop, with a sticky `.dlg-head`; `.prose` is the Markdown reader style (17px, 1.6 line height, 66ch).
- `.ballot` is the one intentionally paper-looking element (off-white, inset box ticks in orange).

## 7. Do / don't

**Do**
- Lead each screen with a kicker, an `h1`, and a `.lede`; left-align.
- Use `.btn.sun` once per screen for the single most useful action; `.btn.primary` for the next step in a flow; `.btn` default for everything else.
- Put a `.dot` or stripe beside every party name; let text stay ink.
- Date and source every fact in `.tiny.muted` under the component.
- Wrap tables and wide charts in scroll containers; keep the page itself free of horizontal scroll.
- Use `.note` for method caveats, with an icon; `.note.warn` only for things that could mislead if missed (e.g. limited information).

**Don't**
- Don't add a second accent colour, gradients, or coloured headings.
- Don't fill large areas with party colour or write text in it.
- Don't shadow static cards; hairlines do the separating.
- Don't centre body copy or lists; centre only the hero countdown units, swipe actions and empty states.
- Don't show a verdict, status or party by colour alone.
- Don't use proportional display numbers in table columns (use `.num`) or tabular figures inside running text.
- Don't invent party colours for "Other" — use `--p-other` and fold minor parties into it in charts.

## 8. Accessibility notes

- Every text/background token pair was checked ≥ 4.5:1 in both themes (muted text ≥ 4.8:1 on `--surface-2`).
- `:focus-visible` is a 2px orange ring with 2px offset on every control; chips/tabs/scale buttons expose state through `aria-pressed` / `aria-selected`, which the CSS styles.
- Tap targets: 44px controls, 56px tab bar items, 64px swipe buttons.
- `prefers-reduced-motion` zeroes all durations; `scroll-behavior` falls back to auto.
- Figures use `font-variant-numeric: tabular-nums` via `.num`; the body face has a slashed zero and distinct I/l/1 by design.
