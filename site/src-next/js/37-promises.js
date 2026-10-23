/* ----- promises: what each party said it would do, checked against what happened (verdict + sources on every one) ----- */
const VERDICTS = ['kept', 'partially-kept', 'in-progress', 'broken', 'abandoned', 'not-yet-due'];
const VMETA = { kept: ['kept', 'check', 'Kept'], 'partially-kept': ['partly', 'half', 'Partly kept'], 'in-progress': ['progress', 'play', 'In progress'], broken: ['broken', 'x', 'Broken'], abandoned: ['abandoned', 'minus', 'Abandoned'], 'not-yet-due': ['notdue', 'clock', 'Not yet due'] };
const vMeta = v => VMETA[v] || ['notdue', 'help', String(v || 'Unknown').replace(/-/g, ' ')];
// Verdict chip: icon + word + colour, never colour alone.
const verdictChip = v => { const [c, i, l] = vMeta(v); return `<span class="verdict v-${c}">${ic(i)}${esc(l)}</span>` };
const TERMS = [['2008-17', '2008–17'], ['2017-23', '2017–23'], ['2023-26', '2023–26'], ['2026', '2026 campaign']];
const PERIODS = [['all', 'All time'], ['since2017', 'Since 2017'], ['current', '2023–26 term'], ['2026', '2026 promises'], ['byterm', 'By term']];
function periodOf(x) { const m = String((x.made || '') + ' ' + (x.term || '')).match(/\b(20[0-2]\d)\b/); if (!m) return 'other'; const y = +m[1];
  return y <= 2016 ? '2008-17' : y <= 2022 ? '2017-23' : y <= 2025 ? '2023-26' : '2026' }
function inPeriod(x, per) { const t = periodOf(x); return per === 'all' || per === 'byterm' ? true : per === 'since2017' ? (t === '2017-23' || t === '2023-26') : per === 'current' ? t === '2023-26' : per === '2026' ? t === '2026' : true }
function periodBar(id) { const cur = S.promPeriod || 'all'; return `<div class="seg" id="${id}" role="group" aria-label="Period" style="justify-self:start">${PERIODS.map(([k, l]) => `<button type="button" data-per="${k}" aria-pressed="${cur === k}">${l}</button>`).join('')}</div>` }
function scoreOf(L) { const c = v => L.filter(x => x.status === v).length; const resolved = L.filter(x => ['kept', 'partially-kept', 'broken', 'abandoned'].includes(x.status)).length;
  return { n: L.length, kept: c('kept'), partly: c('partially-kept'), broken: c('broken'), abandoned: c('abandoned'), progress: c('in-progress'), due: c('not-yet-due'), resolved, score: resolved ? Math.round((c('kept') + .5 * c('partially-kept')) / resolved * 100) : null } }
// Stacked verdict meter (.vmeter > i.v-* with --n). `label` names it for screen readers.
function verdictMeter(L, label = '') { const parts = VERDICTS.map(v => [v, L.filter(x => x.status === v).length]).filter(([, n]) => n);
  const aria = (label ? label + ': ' : '') + (parts.map(([v, n]) => `${n} ${vMeta(v)[2].toLowerCase()}`).join(', ') || 'none');
  return `<div class="vmeter" role="img" aria-label="${esc(aria)}">${parts.map(([v, n], i) => `<i class="v-${vMeta(v)[0]}" style="--n:${n};--i:${i}"></i>`).join('')}</div>` }
// The verdict rules: the same definitions for every party.
const RUBRIC_HTML = (title = 'How verdicts are decided', open = false) => `<details class="disclose"${open ? ' open' : ''}><summary>${esc(title)}</summary><div class="disclose__body small">
  <ul class="rubric"><li>${verdictChip('kept')} delivered as promised, in substance and timing.</li><li>${verdictChip('partially-kept')} delivered in part, late, or in a narrower form.</li><li>${verdictChip('broken')} not delivered while the party had the power to deliver it.</li><li>${verdictChip('abandoned')} dropped by the party itself (often in coalition talks); the entry says who dropped it and why.</li><li>${verdictChip('in-progress')} still being implemented.</li><li>${verdictChip('not-yet-due')} promised for after the election.</li></ul>
  <p>Each promise lists what was said (with a link to where it was said), what happened (with sources), and the verdict. The same definitions are applied to every party. Parties in opposition have fewer promises that can be judged, which is noted. "% kept" counts a partly kept promise as half and leaves out promises still in progress or not yet due.</p></div></details>`;
function byTermTable(parties, pr) { return `<div class="table-wrap"><table class="table"><thead><tr><th>Party</th>${TERMS.map(([, l]) => `<th>${l}</th>`).join('')}</tr></thead><tbody>${parties.map(p => `<tr><td>${ptTag(p, 'ptag')}</td>${TERMS.map(([k, l]) => { const L = (pr[p] || []).filter(x => periodOf(x) === k); if (!L.length) return '<td class="muted">–</td>'; const sc = scoreOf(L); return `<td class="term-cell">${verdictMeter(L, pname(p) + ', ' + l)}<div class="micro muted" style="margin-top:4px">${sc.n} checked${sc.score != null ? ` · <b>${sc.score}%</b> kept` : ' · not yet due'}</div></td>` }).join('')}</tr>`).join('')}</tbody></table></div>
  <p class="micro muted">Terms are when the promise was made: 2008–17 covers the National-led years, 2017–23 the Labour-led years, 2023–26 the current term.</p>` }
const MAIN7 = ['national', 'labour', 'green', 'act', 'nz-first', 'te-pati-maori', 'opportunity'];

V.promises = arg => { const pr = S.data.promises || {};
  const parties = Object.keys(pr).filter(p => (pr[p] || []).length).sort((a, b) => ptCmp(pname(a), pname(b)));
  S.promPeriod = store.get('promPeriod') || S.promPeriod || 'all';
  const first = parties.includes(arg) ? arg : parties[0];
  $('#main').innerHTML = sectionFrame('parties', 'parties/promises', `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('history', 'i--s')} Parties · Promises</p><h1>Promises against delivery</h1>
      <p class="lede">Promises from past campaigns and coalition deals, each checked against what happened, with sources. Choose a period: the whole record, the last two governments, or just the current term.</p></header>
    ${RUBRIC_HTML('How verdicts are decided')}
    <section class="stack"><div class="shead"><div class="shead__row"><h2>By party</h2><span class="micro muted">A to Z</span></div></div>
      ${periodBar('prper')}<div id="prtable" class="stack"></div></section>
    <section class="stack" id="prsec"><div class="shead"><div class="shead__row"><h2>Every promise</h2><span class="micro muted">pick a party</span></div></div><div id="pl"></div></section>`);
  const drawTable = () => { const per = S.promPeriod || 'all'; const t = $('#prtable');
    if (per === 'byterm') { t.innerHTML = byTermTable(parties, pr); return }
    const rows = parties.map(p => ({ p, L: (pr[p] || []).filter(x => inPeriod(x, per)) })).filter(r => r.L.length);
    t.innerHTML = `<div class="terms">${rows.map(({ p, L }) => { const sc = scoreOf(L); return `<div class="term"><div class="term__h"><span><a class="ptag" href="#/parties/${esc(p)}/record" style="--pc:${pcolor(p)}"><span class="sw"></span>${esc(pname(p))}</a> · ${sc.n} checked</span><span class="muted">${sc.score == null ? 'Not yet due' : sc.score + '% kept'}</span></div>${verdictMeter(L, pname(p))}</div>` }).join('')}</div>
      <div class="legend">${VERDICTS.map(v => `<span>${verdictChip(v)}</span>`).join('')}</div>
      <details class="disclose"><summary>The numbers in a table</summary><div class="disclose__body"><div class="table-wrap"><table class="table"><thead><tr><th>Party</th><th class="n">Checked</th><th class="n">Kept</th><th class="n">Partly</th><th class="n">Broken / dropped</th><th class="n">In progress / not due</th><th class="n">% kept</th></tr></thead><tbody>
      ${rows.map(({ p, L }) => { const sc = scoreOf(L); return `<tr><td>${ptTag(p, 'ptag')}</td><td class="n">${sc.n}</td><td class="n">${sc.kept}</td><td class="n">${sc.partly}</td><td class="n">${sc.broken + sc.abandoned}</td><td class="n">${sc.progress + sc.due}</td><td class="n"><b>${sc.score == null ? '–' : sc.score + '%'}</b></td></tr>` }).join('')}</tbody></table></div></div></details>
      <p class="micro muted">Parties were assessed on different numbers of promises and from different positions (government, support partner, opposition); read each party's track record for the context.</p>` };
  $('#prper').onclick = e => { const b = e.target.closest('[data-per]'); if (!b) return; S.promPeriod = b.dataset.per; store.set('promPeriod', S.promPeriod); $('#prper').querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x.dataset.per === S.promPeriod)); drawTable(); if (parties.length) promiseList($('#pl'), S.promParty || first, parties) };
  drawTable(); if (parties.length) promiseList($('#pl'), first, parties) };

// Every promise for one party: verdict chip, what was said, what happened, all sources.
// `parties` given → party chips to switch (Promises page); otherwise the period switch is shown here (party Record tab).
function promiseList(el, party, parties = null) { const pr = S.data.promises || {}; S.promParty = parties ? party : S.promParty;
  if (!S.promPeriod) S.promPeriod = store.get('promPeriod') || 'all';
  if (!(pr[party] || []).length) { el.innerHTML = `${recordSummary(party, { inRecord: true })}`; return }
  const all = pr[party]; let vf = '', q = '';
  el.innerHTML = `<div class="stack stack--l">${parties ? `<div class="chips chips--scroll" role="group" aria-label="Party">${parties.map(p => `<button class="chip" type="button" data-prp="${esc(p)}" aria-pressed="${p === party}"><span class="sw" style="--pc:${pcolor(p)}"></span>${esc(pname(p))} <span class="count">${pr[p].length}</span></button>`).join('')}</div>` : ''}
    ${recordSummary(party, { inRecord: true })}
    <div class="toolbar">${parties ? '' : periodBar('prper2')}<div class="input-icon">${ic('search', 'i--s')}<input class="input" type="search" id="prq" placeholder="Search these promises" aria-label="Search promises"></div>
      <div class="chips chips--scroll" id="prv" role="group" aria-label="Verdict"></div></div>
    <div id="prlist"></div></div>`;
  const draw = () => { const per = S.promPeriod || 'all';
    const inP = all.filter(x => inPeriod(x, per)); const qq = q.toLowerCase();
    $('#prv', el).innerHTML = [['', 'All verdicts', inP.length], ...VERDICTS.filter(v => all.some(x => x.status === v)).map(v => [v, vMeta(v)[2], inP.filter(x => x.status === v).length])].map(([k, l, n]) => `<button class="chip" type="button" data-v="${k}" aria-pressed="${vf === k}">${k ? `<span class="v-${vMeta(k)[0]} vdot">${ic(vMeta(k)[1], 'i--xs')}</span>` : ''}${esc(l)} <span class="count">${n}</span></button>`).join('');
    const L = inP.filter(x => (!vf || x.status === vf) && (!qq || JSON.stringify(x).toLowerCase().includes(qq)));
    $('#prlist', el).innerHTML = `<p class="small muted">${L.length} promise${L.length === 1 ? '' : 's'}${per !== 'all' && per !== 'byterm' ? ' in this period' : ''}</p>
      <div class="promises">${L.map(x => `<article class="pol promise"><div class="row">${verdictChip(x.status)}<span class="micro muted">${esc(x.made || '')}${x.category ? ' · ' + esc(x.category) : ''}</span></div>
        <p class="pol__t st">${esc(x.promise)}</p>${x.detail ? `<p class="small soft">${esc(x.detail)}</p>` : ''}
        <p class="src">${(x.sources || []).length ? 'Sources: ' + ptSources(x.sources) : 'No source recorded'}${x.term ? ' · ' + esc(x.term) : ''}</p></article>`).join('') || '<p class="muted">No promises match.</p>'}</div>` };
  ptScrollChips(el.querySelector('[data-prp]') && el.querySelector('[data-prp]').parentElement);
  el.querySelectorAll('[data-prp]').forEach(b => b.onclick = () => promiseList(el, b.dataset.prp, parties));
  $('#prv', el).onclick = e => { const b = e.target.closest('[data-v]'); if (!b) return; vf = b.dataset.v; draw() };
  $('#prq', el).oninput = e => { q = e.target.value.trim(); draw() };
  const pb = $('#prper2', el); if (pb) pb.onclick = e => { const b = e.target.closest('[data-per]'); if (!b) return; S.promPeriod = b.dataset.per; store.set('promPeriod', S.promPeriod); pb.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x.dataset.per === S.promPeriod)); draw() };
  draw() }
