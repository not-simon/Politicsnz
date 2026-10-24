# Round 2: make every page digestible, and make it accessible

Shared brief for the section agents. Read `docs/PORT_PLAN.md` (where things are, the rules, how to test) and
`site/redesign/IA.md` §2.5 (the depth model) first. `site/src/` is now the live source; `python3 tools/build_site.py` builds
`site/index.html`; test at `http://localhost:8765/index.html#/<route>` (start the server as PORT_PLAN.md says if it is down).

## The owner's instruction

> "Reducing the amount of stuff on each page would be good. Not losing content, but splitting things up and reorganising
> into better organised pages that make it more digestible."

So, for every page you own:

1. **One job per screen.** A page should answer one question. If a page currently stacks five sections, make the first
   screen the summary and give each further section its own route (a sub-route under the section, shown in the subnav
   chip row / rail, or a clear `.rows` list of "go deeper" links), or a `.disclose` where the content is short.
2. **Nothing is lost.** Every fact, link, source line, control and tool that exists today must still be reachable within
   two taps from where it was. Move, don't delete. If you remove something, say so in your report.
3. **Phone first.** Aim for no more than about three phone screens before the reader meets a clear choice of where to go
   next. Long lists and feeds are fine when the list *is* the page (people, policies, releases, results tables).
4. **Routes for everything you split.** New sub-routes go through `resolve()` in `90-shell-router.js` ONLY if the
   coordinator adds them; instead use the pattern already in your section: `V.<view>(sub)` with the sub as the first
   argument (e.g. `#/vote/plan`), or a query-like argument your view already receives. If you genuinely need a new
   top-level sub-route added to the router or `SUBNAV`, write it in your report and build the view so it works once the
   route exists (the router falls back to the section's main view for unknown subs, so nothing breaks meanwhile).
5. **Same structure everywhere.** Use `.pagehead`, `.shead`, `.rows`/`.rowlink`, `.disclose`, `sectionFrame()`, the
   sheet for layer 3. Keep the neutrality rules (A–Z, all parties, ranges not decimals, `--pc` only).

## Accessibility (do this after the reorganisation, on every route you own)

- Run axe-core on each route at 390 and 1280, light and dark. The library is at
  `/home/user/Politicsnz/tools/node/node_modules/axe-core/axe.min.js`; inject it with Playwright
  (`await page.addScriptTag({ path })`, then `await page.evaluate(() => axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag22aa'] }))`)
  and fix every violation in your files. Common ones: missing accessible names on icon buttons, chips without
  `aria-pressed`, segmented controls without a group label, images with no `alt`, form controls without labels,
  `role="tab"` without `tablist`/`tabpanel`, contrast on muted text (use the tokens; don't invent colours).
- Keyboard: every control reachable and operable with Tab/Enter/Space/arrows; focus visible; the sheet traps focus
  (it's a `<dialog>`, so it does) and returns focus on close.
- Colour is never the only cue (words or icons next to every coloured mark). Charts and maps have a text alternative.
- Motion respects `prefers-reduced-motion` (the tokens do most of it; check your own transitions).
- Headings in order (one `h1` per page, then `h2`, `h3`); landmarks intact (`main`, `nav`, `header`, `footer` are in the shell).
- Report the before/after axe violation counts per route.

## Report

Files changed; every route you own and what each page now contains; what moved where; axe counts before and after;
anything you need from the coordinator (new routes, SUBNAV items, data). Do not run git. Do not touch files you don't own.
