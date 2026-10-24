/* ----- promises: what each party said it would do, checked against what happened (verdict + sources on every one) ----- */
const VERDICTS = ['kept', 'partially-kept', 'in-progress', 'broken', 'abandoned', 'not-yet-due', 'early-action'];
const VMETA = { kept: ['kept', 'check', 'Kept'], 'partially-kept': ['partly', 'half', 'Partly kept'], 'in-progress': ['progress', 'play', 'In progress'], broken: ['broken', 'x', 'Broken'], abandoned: ['abandoned', 'minus', 'Abandoned'], 'not-yet-due': ['notdue', 'clock', 'Not yet due'], 'early-action': ['early', 'flag', 'Early action, recorded'] };
const vMeta = v => VMETA[v] || ['notdue', 'help', String(v || 'Unknown').replace(/-/g, ' ')];
// Verdict chip: icon + word + colour, never colour alone.
const verdictChip = v => { const [c, i, l] = vMeta(v); return `<span class="verdict v-${c}">${ic(i)}${esc(l)}</span>` };
// Every promise is filed under one period: the term it was made for (its `term` field when recorded, otherwise the first year
// in `made`). 'other' = long-standing positions with no year. The party summary, the term meters, the tables and the lists all
// use these same periods, so their numbers always add up.
const TERMS = [['2008-17', '2008–17'], ['2017-23', '2017–23'], ['2023-26', '2023–26'], ['other', 'Undated, long-standing'], ['2026', '2026 campaign']];
// "By term" is no longer a period: the by-term table opens in a sheet from the Promises page (and each party's Record tab shows its own terms).
const PERIODS = [['all', 'All time'], ['since2017', 'Since 2017'], ['current', '2023–26 term'], ['2026', '2026 promises']];
const promPer = () => { const v = S.promPeriod || store.get('promPeriod') || 'all'; return PERIODS.some(([k]) => k === v) ? v : 'all' };
function periodOf(x) { const yr = v => { const m = String(v || '').match(/\b(20[0-2]\d)\b/); return m ? +m[1] : null }; const y = yr(x.term) || yr(x.made); if (!y) return 'other';
  return y <= 2016 ? '2008-17' : y <= 2022 ? '2017-23' : y <= 2025 ? '2023-26' : '2026' }
// Promises made for the 2026 election cannot be judged yet. They are never scored; one that already carries a verdict
// (something happened before the election) is shown as "Early action, recorded".
const isPastPromise = x => periodOf(x) !== '2026';
const pStatus = x => !isPastPromise(x) && x.status !== 'not-yet-due' ? 'early-action' : x.status;
function inPeriod(x, per) { const t = periodOf(x); return per === 'all' || per === 'byterm' ? true : per === 'since2017' ? (t === '2017-23' || t === '2023-26') : per === 'current' ? t === '2023-26' : per === '2026' ? t === '2026' : true }
function periodBar(id) { const cur = promPer(); return `<div class="seg" id="${id}" role="group" aria-label="Period" style="justify-self:start">${PERIODS.map(([k, l]) => `<button type="button" data-per="${k}" aria-pressed="${cur === k}">${l}</button>`).join('')}</div>` }
// n = every promise in L; past = those made before the 2026 campaign; % kept = (kept + half of partly kept) / past promises
// with a final verdict (kept, partly kept, broken, abandoned). In progress, not yet due and 2026 promises are never in the %.
function scoreOf(L) { const c = v => L.filter(x => pStatus(x) === v).length; const resolved = L.filter(x => isPastPromise(x) && ['kept', 'partially-kept', 'broken', 'abandoned'].includes(pStatus(x))).length;
  return { n: L.length, past: L.filter(isPastPromise).length, kept: c('kept'), partly: c('partially-kept'), broken: c('broken'), abandoned: c('abandoned'), progress: c('in-progress'), due: c('not-yet-due'), early: c('early-action'), resolved, score: resolved ? Math.round((c('kept') + .5 * c('partially-kept')) / resolved * 100) : null } }
// "36 kept, 10 partly kept, 7 broken …" for one set of promises (only the verdicts present).
const verdictCounts = L => VERDICTS.map(v => [v, L.filter(x => pStatus(x) === v).length]).filter(([, n]) => n).map(([v, n]) => `${n} ${vMeta(v)[2].toLowerCase()}`).join(', ');
// Stacked verdict meter (.vmeter > i.v-* with --n). `label` names it for screen readers.
function verdictMeter(L, label = '') { const parts = VERDICTS.map(v => [v, L.filter(x => pStatus(x) === v).length]).filter(([, n]) => n);
  const aria = (label ? label + ': ' : '') + (parts.map(([v, n]) => `${n} ${vMeta(v)[2].toLowerCase()}`).join(', ') || 'none');
  return `<div class="vmeter" role="img" aria-label="${esc(aria)}">${parts.map(([v, n], i) => `<i class="v-${vMeta(v)[0]}" style="--n:${n};--i:${i}"></i>`).join('')}</div>` }
// The verdict rules: the same definitions for every party.
const RUBRIC_HTML = (title = 'How verdicts are decided', open = false) => `<details class="disclose"${open ? ' open' : ''}><summary>${esc(title)}</summary><div class="disclose__body small">
  <ul class="rubric"><li>${verdictChip('kept')} delivered as promised, in substance and timing.</li><li>${verdictChip('partially-kept')} delivered in part, late, or in a narrower form.</li><li>${verdictChip('broken')} not delivered while the party had the power to deliver it.</li><li>${verdictChip('abandoned')} dropped by the party itself (often in coalition talks); the entry says who dropped it and why.</li><li>${verdictChip('in-progress')} still being implemented.</li><li>${verdictChip('not-yet-due')} promised for after the election.</li><li>${verdictChip('early-action')} a 2026 campaign promise where something has already happened. Recorded, never scored.</li></ul>
  <p>Each promise lists what was said (with a link to where it was said), what happened (with sources), and the verdict. The same definitions are applied to every party. Parties in opposition have fewer promises that can be judged, which is noted.</p>
  <p><b>Which promises are counted.</b> Each promise is filed under the term it was made for: 2008–17, 2017–23, 2023–26, undated long-standing positions, or the 2026 campaign. "Past promises" are all of them except the 2026 campaign; the party summary, the term meters, the tables and the list all count the same promises. Past promises that are still in progress or not yet due are counted as checked but left out of "% kept". "% kept" counts a partly kept promise as half, out of the past promises with a final verdict (kept, partly kept, broken, abandoned).</p>
  <p><b>2026 campaign promises are not judged.</b> They show as "Not yet due" for every party, with counts only and no percentage.</p></div></details>`;
function byTermTable(parties, pr) { return `<div class="table-wrap" tabindex="0" role="region" aria-label="Promises by term, scrollable table"><table class="table"><caption>Promises checked and share kept, by party and by the term the promise was made in</caption><thead><tr><th scope="col">Party</th>${TERMS.map(([, l]) => `<th scope="col">${l}</th>`).join('')}</tr></thead><tbody>${parties.map(p => `<tr><th scope="row">${ptTag(p, 'ptag')}</th>${TERMS.map(([k, l]) => { const L = (pr[p] || []).filter(x => periodOf(x) === k); if (!L.length) return '<td class="muted">–</td>'; const sc = scoreOf(L); return `<td class="term-cell">${verdictMeter(L, pname(p) + ', ' + l)}<div class="micro muted" style="margin-top:4px">${sc.n} ${k === '2026' ? 'recorded' : 'checked'}${sc.score != null ? ` · <b>${sc.score}%</b> kept` : k === '2026' ? ' · not yet due' : ' · no final verdicts yet'}</div></td>` }).join('')}</tr>`).join('')}</tbody></table></div>
  <p class="micro muted">Terms are the term the promise was made for: 2008–17 covers the National-led years, 2017–23 the Labour-led years, 2023–26 the term that has just ended. "Undated" are long-standing positions with no year. 2026 campaign promises are not judged.</p>` }
const MAIN7 = ['national', 'labour', 'green', 'act', 'nz-first', 'te-pati-maori', 'opportunity'];

// Numbers table for one period (sheet from the Promises page).
function promNumbersTable(rows, perLabel) { return `<div class="table-wrap" tabindex="0" role="region" aria-label="Promise numbers, scrollable table"><table class="table"><caption>Promise verdicts by party, ${esc(perLabel.toLowerCase())}</caption><thead><tr><th scope="col">Party</th><th scope="col" class="n">Checked</th><th scope="col" class="n">Kept</th><th scope="col" class="n">Partly</th><th scope="col" class="n">Broken / dropped</th><th scope="col" class="n">In progress / not due / early action</th><th scope="col" class="n">% kept</th></tr></thead><tbody>
  ${rows.map(({ p, L }) => { const sc = scoreOf(L); return `<tr><th scope="row">${ptTag(p, 'ptag')}</th><td class="n">${sc.n}</td><td class="n">${sc.kept}</td><td class="n">${sc.partly}</td><td class="n">${sc.broken + sc.abandoned}</td><td class="n">${sc.progress + sc.due + sc.early}</td><td class="n"><b>${sc.score == null ? '–' : sc.score + '%'}</b></td></tr>` }).join('')}</tbody></table></div>
  <p class="micro muted">"% kept" counts a partly kept promise as half, out of past promises with a final verdict. Promises still in progress, not yet due, or made for the 2026 campaign are counted but never in the percentage.</p>` }

V.promises = arg => { const pr = S.data.promises || {};
  const parties = Object.keys(pr).filter(p => (pr[p] || []).length).sort((a, b) => ptCmp(pname(a), pname(b)));
  S.promPeriod = promPer();
  const first = parties.includes(arg) ? arg : parties[0];
  const sheetRow = (k, icon, t, sub) => `<button class="rowlink ov-row" type="button" data-prsheet="${k}" aria-haspopup="dialog"><span class="rowlink__icon">${ic(icon)}</span><span><span class="rowlink__title">${t}</span><span class="rowlink__sub" style="display:block">${sub}</span></span>${ic('chev')}</button>`;
  $('#main').innerHTML = sectionFrame('parties', 'parties/promises', `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('history', 'i--s')} Parties · Promises</p><h1>Promises against delivery</h1>
      <p class="lede">Promises from past campaigns and coalition deals, each checked against what happened, with sources. Choose a period: the whole record, the last two governments, or the 2023–26 term. Promises made for the 2026 election are listed but not judged.</p></header>
    ${RUBRIC_HTML('How verdicts are decided')}
    <section class="stack" aria-labelledby="h-prby"><div class="shead"><div class="shead__row"><h2 id="h-prby">By party</h2><span class="micro muted">A to Z</span></div></div>
      ${periodBar('prper')}<div id="prtable" class="stack"></div>
      <div class="rows">${sheetRow('byterm', 'history', 'By term, every party', 'The term each promise was made for: 2008–17, 2017–23, 2023–26, undated, and the 2026 campaign')}${sheetRow('numbers', 'list', 'The numbers in a table', 'Checked, kept, partly, broken or dropped, in progress, for the period above')}</div></section>
    <section class="stack" id="prsec" aria-labelledby="h-prall"><div class="shead"><div class="shead__row"><h2 id="h-prall">Every promise</h2><span class="micro muted">pick a party</span></div></div><div id="pl"></div></section>`);
  const rowsFor = per => parties.map(p => ({ p, L: (pr[p] || []).filter(x => inPeriod(x, per)) })).filter(r => r.L.length);
  const drawTable = () => { const per = promPer(); const t = $('#prtable');
    t.innerHTML = `<div class="terms">${rowsFor(per).map(({ p, L }) => { const sc = scoreOf(L); return `<div class="term"><div class="term__h"><span><a class="ptag" href="#/parties/${esc(p)}/record" style="--pc:${pcolor(p)}"><span class="sw"></span>${esc(pname(p))}</a> · ${sc.n} ${per === '2026' ? 'recorded' : 'checked'}</span><span class="muted">${per === '2026' ? 'Not yet due' : sc.score == null ? 'No final verdicts yet' : sc.score + '% kept'}</span></div>${verdictMeter(L, pname(p))}</div>` }).join('')}</div>
      <div class="legend">${VERDICTS.filter(v => v !== 'early-action' || rowsFor(per).some(r => r.L.some(x => pStatus(x) === v))).map(v => `<span>${verdictChip(v)}</span>`).join('')}</div>
      <p class="micro muted">Parties were assessed on different numbers of promises and from different positions (government, support partner, opposition); read each party's track record for the context.</p>` };
  $('#main').querySelectorAll('[data-prsheet]').forEach(b => b.onclick = () => { const per = promPer(); const perL = (PERIODS.find(([k]) => k === per) || [, 'All time'])[1];
    if (b.dataset.prsheet === 'byterm') openSheet({ title: 'Promises by term', depth: ['Promises', 'By term', 'Sources'], at: 1, html: byTermTable(parties, pr) + RUBRIC_HTML('How verdicts are decided') });
    else openSheet({ title: 'The numbers: ' + perL, depth: ['Promises', 'Numbers', 'Sources'], at: 1, html: promNumbersTable(rowsFor(per), perL) + '<p class="micro muted">Change the period on the Promises page to see another table. Every promise and its sources are listed under "Every promise".</p>' }) });
  $('#prper').onclick = e => { const b = e.target.closest('[data-per]'); if (!b) return; S.promPeriod = b.dataset.per; store.set('promPeriod', S.promPeriod); $('#prper').querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x.dataset.per === S.promPeriod)); drawTable(); if (parties.length) promiseList($('#pl'), S.promParty || first, parties) };
  drawTable(); if (parties.length) promiseList($('#pl'), first, parties) };

// Every promise for one party: verdict chip, what was said, what happened, all sources.
// `parties` given → party chips to switch (Promises page); otherwise the period switch is shown here (party Record tab).
function promiseList(el, party, parties = null) { const pr = S.data.promises || {}; S.promParty = parties ? party : S.promParty;
  S.promPeriod = promPer();
  if (!(pr[party] || []).length) { el.innerHTML = `${recordSummary(party, { inRecord: true })}`; return }
  const all = pr[party]; let vf = '', q = '', limit = 20;
  el.innerHTML = `<div class="stack stack--l">${parties ? `<div class="chips chips--scroll" role="group" aria-label="Party">${parties.map(p => `<button class="chip" type="button" data-prp="${esc(p)}" aria-pressed="${p === party}"><span class="sw" style="--pc:${pcolor(p)}"></span>${esc(pname(p))} <span class="count">${pr[p].length}</span></button>`).join('')}</div>` : ''}
    ${recordSummary(party, { inRecord: true })}
    <div class="toolbar">${parties ? '' : periodBar('prper2')}<div class="input-icon">${ic('search', 'i--s')}<input class="input" type="search" id="prq" placeholder="Search these promises" aria-label="Search promises"></div>
      <div class="chips chips--scroll" id="prv" role="group" aria-label="Verdict"></div></div>
    <div id="prlist"></div></div>`;
  const draw = () => { const per = promPer();
    const inP = all.filter(x => inPeriod(x, per)); const qq = q.toLowerCase();
    $('#prv', el).innerHTML = [['', 'All verdicts', inP.length], ...VERDICTS.filter(v => all.some(x => pStatus(x) === v)).map(v => [v, vMeta(v)[2], inP.filter(x => pStatus(x) === v).length])].map(([k, l, n]) => `<button class="chip" type="button" data-v="${k}" aria-pressed="${vf === k}">${k ? `<span class="v-${vMeta(k)[0]} vdot">${ic(vMeta(k)[1], 'i--xs')}</span>` : ''}${esc(l)} <span class="count">${n}</span></button>`).join('');
    const L = inP.filter(x => (!vf || pStatus(x) === vf) && (!qq || JSON.stringify(x).toLowerCase().includes(qq)));
    const card = x => `<article class="pol promise"><div class="row">${verdictChip(pStatus(x))}<span class="micro muted">${esc(x.made || '')}${x.category ? ' · ' + esc(x.category) : ''}</span></div>
        <p class="pol__t st">${esc(x.promise)}</p>${x.detail ? `<p class="small soft">${esc(x.detail)}</p>` : ''}
        <p class="src">${(x.sources || []).length ? 'Sources: ' + ptSources(x.sources) : 'No source recorded'}${x.term ? ' · ' + esc(x.term) : ''}${pStatus(x) === 'early-action' ? ' · a 2026 campaign promise: recorded, not scored' : ''}</p></article>`;
    const head = `<p class="small muted">${L.length} promise${L.length === 1 ? '' : 's'}${per !== 'all' ? ' in this period' : ''}${!vf && !qq && L.length ? ', grouped by verdict: open a group' : ''}</p>`;
    if (!L.length) { $('#prlist', el).innerHTML = head + '<p class="muted">No promises match.</p>'; return }
    if (!vf && !qq) { // unfiltered: one fold per verdict, in the rubric's order
      $('#prlist', el).innerHTML = head + `<div class="promise-groups">${VERDICTS.map(v => [v, L.filter(x => pStatus(x) === v)]).filter(([, G]) => G.length).map(([v, G]) => `<details class="disclose"><summary><span class="row row--nowrap" style="gap:10px">${verdictChip(v)}</span><span class="micro muted" style="margin-left:auto">${G.length}</span></summary><div class="disclose__body"><div class="promises">${G.map(card).join('')}</div></div></details>`).join('')}</div>`; return }
    $('#prlist', el).innerHTML = head + `<div class="promises">${L.slice(0, limit).map(card).join('')}</div>${L.length > limit ? `<div class="row"><button class="btn" type="button" id="prmore">Show the next ${Math.min(20, L.length - limit)}</button><span class="small muted">${limit} of ${L.length} shown</span></div>` : ''}`;
    const m = $('#prmore', el); if (m) m.onclick = () => { limit += 20; draw() } };
  ptScrollChips(el.querySelector('[data-prp]') && el.querySelector('[data-prp]').parentElement);
  el.querySelectorAll('[data-prp]').forEach(b => b.onclick = () => promiseList(el, b.dataset.prp, parties));
  $('#prv', el).onclick = e => { const b = e.target.closest('[data-v]'); if (!b) return; vf = b.dataset.v; limit = 20; draw() };
  $('#prq', el).oninput = e => { q = e.target.value.trim(); limit = 20; draw() };
  const pb = $('#prper2', el); if (pb) pb.onclick = e => { const b = e.target.closest('[data-per]'); if (!b) return; S.promPeriod = b.dataset.per; store.set('promPeriod', S.promPeriod); pb.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x.dataset.per === S.promPeriod)); draw() };
  draw() }
