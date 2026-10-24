/* ----- Seats › Parliament (seat map), Coalition builder, Seat calculator -----
   The section sub-navigation replaces the old tabs; the old "Polls & trends" tab now lives on Seats › Polls & forecast. */
V.parliament = (sub = 'chamber') => (({ coalition: parlCoalition, calculator: parlCalculator })[sub] || parlChamber)();

// The 2026 step of the seat map: the result once loaded; before that one plausible Parliament from the forecast (never on election day).
function parl2026() {
  const R = results2026();
  if (R) { const comp = Object.fromEntries((R.parties || []).filter(r => r.total_seats).map(r => [r.party, r.total_seats]));
    return { kind: 'result', comp, R, note: `${R.official ? 'Official' : 'Preliminary'} result${R.counted_pct != null ? ` · ${fmt(R.counted_pct, 0)}% counted` : ''}` } }
  if (forecastHidden()) return null;
  const F = S.data.forecast, mlp = F && F.most_likely_parliament && F.most_likely_parliament.seats;
  if (mlp) return { kind: 'forecast', comp: mlp, note: 'One plausible result from the forecast, not a prediction' };
  const pr = projection(); return { kind: 'projection', comp: pr.seats, pr, note: 'Poll average turned into seats, not a prediction' } }

function parlChamber() {
  const parls = S.data.parliaments || [], els = S.data.elections || [];
  const steps = parls.map(p => ({ key: `p${p.parliament}`, label: String(p.election_year), parl: p }));
  const p26 = parl2026(); if (p26) steps.push({ key: 'p2026', label: '2026', p26 });
  let i = steps.findIndex(x => x.key === store.get('chamberSel')); if (i < 0) i = Math.max(0, parls.length - 1);
  let mode = 'start';
  $('#main').innerHTML = sectionFrame('seats', 'seats/parliament', `
    <header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('seats', 'i--s')} Seats · Parliament</p><h1>Every seat in every Parliament since 2011</h1>
      <p class="lede">Press play to watch the House change from one election to the next, or tap a seat to see who sat there.</p></header>
    ${scrubberHTML({ id: 'cscrub', labels: steps.map(s => s.label), i, aria: 'Parliament', play: 'Play through the Parliaments' })}
    <div class="row row--between"><div class="seg" id="cmode" role="group" aria-label="When in the term"><button type="button" data-m="start" aria-pressed="true">After the election</button><button type="button" data-m="now" aria-pressed="false">End of term</button></div>
      <div class="legend" id="clegend" role="group" aria-label="Seats by party, A to Z"></div></div>
    <div class="split split--7-5">
      <figure class="stack stack--s"><div id="hemi"></div><figcaption class="small soft" id="ctitle"></figcaption>
        <p class="small soft" id="calt" hidden>Seat counts by party are in the legend; <button class="linkbtn" type="button" id="copen" aria-controls="cresults-d">the result table</button> has the votes, electorate and list seats.</p></figure>
      <div class="stack stack--l sticky"><section class="seatsheet" id="seatinfo" aria-live="polite"></section><div class="stack" id="cctx"></div></div>
    </div>
    <details class="disclose" id="cresults-d"><summary id="cresults-s">The election result, party by party</summary><div class="disclose__body" id="cresults" data-compact="1"></div></details>`);
  const resetSeat = () => { $('#seatinfo').classList.add('seatsheet--idle'); $('#seatinfo').innerHTML = `<p class="eyebrow">Seat details</p><p class="small soft">Tap or select any seat to see who sat there. Seats are grouped by party, left to right as the parties usually sit.</p>` };
  const draw = () => { const st = steps[i]; store.set('chamberSel', st.key); let seats, ctx = '', table = '', cap = '';
    if (st.p26) { const x = st.p26; seats = seatsFromComposition(x.comp, []); $('#cmode').hidden = true;
      if (x.kind === 'result') { cap = `The 2026 ${x.R.official ? 'official' : 'preliminary'} result, party by party`; ctx = `<p class="eyebrow">55th Parliament · ${esc(x.note)}</p><p class="small">Seats from the Electoral Commission's ${x.R.official ? 'official' : 'preliminary'} count. Preliminary results leave out special votes, which can move a seat or two; the official result is due on 27 November.</p><a class="more small" href="#/seats/results">Election night results ${ic('chev', 'i--xs')}</a>`; table = electionTableHTML({ year: 2026, date: x.R.date, parties: x.R.parties, official: x.R.official }, 'az', { compact: true }) }
      else if (x.kind === 'forecast') { const F = S.data.forecast;
        ctx = `<p class="eyebrow">2026 · ${esc(x.note)}</p><p class="small">${esc(F.most_likely_parliament.note || '')}</p><p class="small soft">Every party's likely range, and how often each group reaches a majority, is on the polls page.</p><a class="more small" href="#/seats/polls">Polls &amp; forecast ${ic('chev', 'i--xs')}</a>` }
      else { const pr = x.pr; ctx = `<p class="eyebrow">2026 · ${esc(x.note)}</p><p class="small">Average of the ${pr.n} latest polls (${esc(pr.range)}), turned into seats with the Sainte-Laguë formula. Assumed electorate wins: ${esc(Object.entries(pr.elec).map(([p, n]) => pname(p) + ' ' + n).join(', ') || 'none')}.</p><a class="more small" href="#/seats/polls">Polls &amp; forecast ${ic('chev', 'i--xs')}</a>` } }
    else { $('#cmode').hidden = false; const parl = st.parl; seats = parliamentSeats(parl, mode);
      const e = els.find(x => x.year === parl.election_year); const g = e && e.government;
      ctx = `<p class="eyebrow">${ordinal(parl.parliament)} Parliament · ${esc(seatDate(parl.start))} to ${esc(parl.end ? seatDate(parl.end) : 'today')}</p>
        ${g ? `<p class="small"><b>Government:</b> ${esc(g.pm || '')}, ${esc((g.parties || []).map(pname).join(' + '))} (${esc(g.arrangement || '')})${(g.support || []).length ? ', with support from ' + esc(g.support.map(pname).join(', ')) : ''}.</p>${g.notes ? `<p class="small soft">${esc(g.notes)}</p>` : ''}` : ''}
        ${(parl.changes || []).length ? `<details class="disclose"><summary>${parl.changes.length} changes during the term</summary><div class="disclose__body"><ul class="small" role="list">${parl.changes.map(c => `<li><span class="num muted">${esc(seatDate(c.date))}</span> ${esc(c.description)}</li>`).join('')}</ul></div></details>` : ''}
        ${(parl.sources || []).length ? `<p class="srcline">Sources: ${parl.sources.slice(0, 3).map((u, k) => `<a href="${esc(typeof u === 'string' ? u : u.url)}" target="_blank" rel="noopener">${k + 1}</a>`).join(' ')}</p>` : ''}`;
      if (e) { table = electionTableHTML(e, 'az', { compact: true }); cap = `The ${e.year} election result, party by party` } }
    S.curSeats = seats; chamberUpdate($('#hemi'), seats, { label: st.p26 ? '2026 seat map' : `Seat map, ${st.label}`, interactive: true, describedby: 'ctitle clegend' });
    const maj = Math.floor(seats.length / 2) + 1;
    $('#ctitle').textContent = `${st.p26 ? '2026 · ' + st.p26.note : ordinal(st.parl.parliament) + ' Parliament · ' + st.label + ' election · ' + (mode === 'start' ? 'after the election' : 'end of term')} · ${seats.length} seats · ${maj} to govern`;
    $('#cscrub .scrubber__note').textContent = st.p26 ? (st.p26.kind === 'result' ? '55th Parliament' : 'one plausible result') : `${ordinal(st.parl.parliament)} Parliament · ${seats.length} seats`;
    const counts = {}; seats.forEach(s => counts[s.party] = (counts[s.party] || 0) + 1); $('#clegend').innerHTML = legendHTML(counts);
    $('#cctx').innerHTML = ctx; $('#cresults').innerHTML = table; $('#cresults-d').hidden = !table; $('#calt').hidden = !table; if (cap) $('#cresults-s').textContent = cap;
    resetSeat(); scrub.sync(i) };
  const scrub = bindScrubber($('#cscrub'), { labels: steps.map(s => s.label), get: () => i, set: k => { i = k; draw() }, play: 'Play through the Parliaments' });
  bindElectionTable($('#cresults')); bindSeatKeys($('#hemi'));
  $('#copen').onclick = () => { const d = $('#cresults-d'); d.open = true; $('#cresults-s').focus(); d.scrollIntoView({ block: 'nearest', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }) };
  $('#cmode').onclick = e => { const b = e.target.closest('[data-m]'); if (!b) return; mode = b.dataset.m; $('#cmode').querySelectorAll('[data-m]').forEach(x => x.setAttribute('aria-pressed', x === b)); draw() };
  const showSeat = e => { const c = e.target.closest('circle[data-i]'); if (!c) return; $('#hemi').querySelectorAll('circle.is-sel').forEach(x => x.classList.remove('is-sel')); c.classList.add('is-sel'); seatInfo(S.curSeats[+c.dataset.i]) };
  $('#hemi').addEventListener('click', showSeat); $('#hemi').addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); showSeat(e) } });
  draw();
}
async function seatInfo(s) { const box = $('#seatinfo'); if (!box || !s) return; box.classList.remove('seatsheet--idle');
  if (!s.name) { box.innerHTML = `<p class="eyebrow">Seat details</p><p>${ptagHTML(s.party)} seat</p><p class="small soft">Names are shown for Parliaments since 2011; this seat is part of a projection or result without a member list.</p>`; return }
  await loadPeople(); const person = findPerson(s.slug, s.name);
  box.innerHTML = `<p class="eyebrow">${esc(s.type === 'list' ? 'List MP' : 'Electorate MP' + (s.seat ? ' · ' + s.seat : ''))}</p>
    <div class="row row--nowrap" style="gap:var(--s-4)">${faceHTML(person || { name: s.name }, s.party)}<div class="stack stack--s"><h2 class="h3">${esc(s.name)}</h2><div>${ptagHTML(s.party)}</div></div></div>
    ${s.left ? `<p class="small soft">Left Parliament ${esc(seatDate(s.left))}${s.left_reason ? ' · ' + esc(s.left_reason) : ''}</p>` : ''}${s.notes ? `<p class="small soft">${esc(s.notes)}</p>` : ''}
    ${person ? `<div class="row"><button class="btn btn--s" type="button" id="seatprof">Profile</button></div>` : ''}`;
  const b = $('#seatprof'); if (b) b.onclick = () => openPerson(person) }
// Election results table. Parties A–Z by default (neutral order), with a switch to sort by party vote.
function electionTableHTML(el, sort = 'az', { compact = false } = {}) {
  const rows = (el.parties || []).slice().sort(sort === 'votes' ? (a, b) => (b.party_vote_pct || 0) - (a.party_vote_pct || 0) : (a, b) => byShort(a.party, b.party));
  return `<div class="shead${compact ? ' shead--quiet' : ''}"><div class="shead__row">${compact ? `<span class="small muted">${el.year} general election</span>` : `<h2 id="h-el${el.year}">${el.year} general election</h2>`}<div class="seg" role="group" aria-label="Order parties" data-year="${el.year}"><button type="button" data-sort="az" aria-pressed="${sort === 'az'}">A–Z</button><button type="button" data-sort="votes" aria-pressed="${sort === 'votes'}">Most party votes</button></div></div>
    <p class="small muted">${el.date ? esc(seatDate(el.date)) : ''}${el.turnout_pct != null ? ` · turnout <span class="num">${fmt(el.turnout_pct)}%</span>` : ''}${el.overhang ? ` · overhang ${el.overhang}` : ''}${el.wasted_party_vote_pct != null ? ` · wasted party vote <span class="num">${fmt(el.wasted_party_vote_pct)}%</span>` : ''}</p></div>
  ${twrap(`${el.year} election result`, `<table class="table"><caption class="sr-only">${el.year} general election: party vote and seats, parties ${sort === 'votes' ? 'by party vote' : 'A to Z'}</caption><thead><tr><th scope="col">Party</th><th class="n" scope="col">Party vote</th><th class="n" scope="col">Votes</th><th class="n" scope="col">Electorate</th><th class="n" scope="col">List</th><th class="n" scope="col">Seats</th></tr></thead><tbody>
  ${rows.map(r => `<tr><th scope="row">${ptagHTML(r.party, r.name || pname(r.party))}</th><td class="n">${r.party_vote_pct != null ? fmt(r.party_vote_pct, 2) + '%' : '–'}</td><td class="n">${r.party_votes ? Number(r.party_votes).toLocaleString('en-NZ') : '–'}</td><td class="n">${r.electorate_seats ?? 0}</td><td class="n">${r.list_seats ?? 0}</td><td class="n"><b>${r.total_seats ?? 0}</b></td></tr>`).join('')}
  </tbody></table>`)}
  <p class="srcline">${el.year === 2026 && !el.official ? 'Preliminary count (special votes not yet included)' : 'Official results'}, Electoral Commission${(el.sources || []).length ? ` · <a href="${esc(typeof el.sources[0] === 'string' ? el.sources[0] : el.sources[0].url)}" target="_blank" rel="noopener">source</a>` : ''}</p>
  ${el.year < 2026 ? `<div class="row"><button class="btn btn--s" type="button" data-page="elections/${el.year}.md">Read the story of the ${el.year} election</button></div>` : ''}` }
const electionTable = el => electionTableHTML(el);
function bindElectionTable(box) { box.onclick = e => { const b = e.target.closest('[data-sort]'); if (!b) return; const y = +b.closest('[data-year]').dataset.year;
  const el = y === 2026 ? (() => { const R = results2026(); return R && { year: 2026, date: R.date, parties: R.parties, official: R.official } })() : (S.data.elections || []).find(x => x.year === y); if (el) { box.innerHTML = electionTableHTML(el, b.dataset.sort, { compact: !!box.dataset.compact }); const nb = box.querySelector(`[data-sort="${b.dataset.sort}"]`); if (nb) nb.focus() } } }

/* ----- coalition builder ----- */
function parlCoalition() {
  const els = (S.data.elections || []).filter(e => e.year >= 2011 && e.year < 2026), R = results2026();
  const srcs = [...(R ? [['r2026', '2026 result']] : forecastHidden() ? [] : [['proj', '2026 poll average']]), ...els.map(e => [`e${e.year}`, `${e.year} result`]).reverse()];
  let src = srcs.some(s => s[0] === store.get('coalSrc')) ? store.get('coalSrc') : srcs[0][0];
  let bloc; try { bloc = new Set(JSON.parse(store.get('coalBloc') || 'null') || ['national', 'act', 'nz-first']) } catch { bloc = new Set(['national', 'act', 'nz-first']) }
  $('#main').innerHTML = sectionFrame('seats', 'seats/coalition', `
    <header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('seats', 'i--s')} Seats · Coalition builder</p><h1>Build a government</h1>
      <p class="lede">Pick a result, then tap parties to put them together. A government needs more than half the seats to win confidence votes.</p></header>
    <div class="stack stack--s"><span class="small muted" id="csrc-l">Seats from</span><div class="seg" id="csrc" role="group" aria-labelledby="csrc-l">${srcs.map(([v, l]) => `<button type="button" data-v="${v}" aria-pressed="${v === src}">${esc(l)}</button>`).join('')}</div></div>
    <div class="stack stack--s"><span class="small muted" id="cchips-l">Parties, A–Z (tap to add or remove)</span><div class="chips" id="cchips" role="group" aria-labelledby="cchips-l"></div>
      <div class="row" role="group" aria-label="Try a combination"><span class="small muted" aria-hidden="true">Try:</span><button class="btn btn--s btn--quiet" type="button" data-pre="labour,green,te-pati-maori">Labour + Green + Te Pāti Māori</button><button class="btn btn--s btn--quiet" type="button" data-pre="national,act,nz-first">National + ACT + NZ First</button><button class="btn btn--s btn--quiet" type="button" data-pre="">Clear</button></div></div>
    <div class="split split--5-7">
      <div class="stack" aria-live="polite" aria-atomic="true"><div class="row" style="align-items:baseline;gap:var(--s-3)"><span class="figure figure--s" id="chave">0</span><span class="soft" id="cof"></span></div>
        <p id="cverdict" class="h4"></p><div class="cbar" id="cbar" aria-hidden="true"></div><p class="small soft" id="cnote"></p></div>
      <figure class="stack stack--s"><div id="chemi"></div><figcaption class="small soft">Chosen parties' seats at full colour, from the left; the rest faded. The dashed line is the majority mark. The count and the sum beside it say the same in words.</figcaption></figure>
    </div>
    <p class="srcline">Seats: official results, Electoral Commission${R ? '; 2026 from the count as loaded here' : ''}.</p>
    <div class="stack stack--s">
      <details class="disclose"><summary>Why more than half?</summary><div class="disclose__body"><p class="small">A government has to keep the confidence of the House: win the votes that say it may govern, and pass a Budget. With 120 seats that means 61. If there are overhang seats the House is bigger and the number rises with it. Parties can also govern as a minority with "confidence and supply" support from parties outside the Cabinet.</p></div></details>
      <details class="disclose"><summary>Where these seat counts come from</summary><div class="disclose__body"><p class="small">Seat counts are the official results for past elections. The 2026 option turns the latest poll average into seats with the same formula as the seat calculator; it is an illustration, not a forecast.</p></div></details>
      <details class="disclose"><summary>Who would actually work with whom</summary><div class="disclose__body"><p class="small">Adding numbers up is the easy part. What each party has said about working with the others is on its own page, under "Who they'd work with".</p><div class="row"><a class="more small" href="#/parties">All parties, A–Z ${ic('chev', 'i--xs')}</a></div></div></details></div>`);
  const seatsFor = v => v === 'proj' ? projection().seats : v === 'r2026' ? Object.fromEntries((R.parties || []).filter(r => r.total_seats).map(r => [r.party, r.total_seats]))
    : Object.fromEntries((els.find(e => `e${e.year}` === v).parties || []).filter(r => r.total_seats).map(r => [r.party, r.total_seats]));
  const draw = () => { store.set('coalSrc', src); store.set('coalBloc', JSON.stringify([...bloc]));
    const seats = seatsFor(src), total = Object.values(seats).reduce((a, b) => a + b, 0), maj = Math.floor(total / 2) + 1, ps = Object.keys(seats).sort(byShort);
    $('#cchips').innerHTML = ps.map(p => `<button class="chip" type="button" data-p="${p}" aria-pressed="${bloc.has(p)}" style="--pc:${pcolor(p)}"><span class="sw"></span>${esc(pname(p))} <span class="count">${seats[p]}<span class="sr-only"> seats</span></span></button>`).join('');
    const inB = ps.filter(p => bloc.has(p)), have = inB.reduce((a, p) => a + seats[p], 0);
    $('#chave').textContent = have; $('#cof').textContent = `of ${total} seats · ${maj} needed`;
    $('#cverdict').innerHTML = !inB.length ? 'Tap parties to build a government.' : have >= maj ? `${ic('check', 'i--s')} A majority, with ${have - maj + 1} to spare over half` : `${maj - have} short of a majority`;
    const order = p => P(p).order; const left = inB.slice().sort((a, b) => order(a) - order(b)), rest = ps.filter(p => !bloc.has(p)).sort((a, b) => order(a) - order(b));
    $('#cbar').innerHTML = left.map(p => `<i style="--pc:${pcolor(p)};flex:${seats[p]} 0 0" title="${esc(pname(p))} ${seats[p]}"></i>`).join('') + (total - have > 0 ? `<i class="cbar__rest" style="flex:${total - have} 0 0"></i>` : '') + `<b class="cbar__maj" style="left:${maj / total * 100}%"><span>${maj}</span></b>`;
    $('#cnote').textContent = inB.length ? `${inB.map(p => `${pname(p)} ${seats[p]}`).join(' + ')} = ${have}.` : '';
    // chosen parties first, so the dashed line at the majority mark shows whether they reach it
    const list = []; [...left, ...rest].forEach(p => { for (let k = 0; k < seats[p]; k++) list.push({ party: p }) });
    chamberUpdate($('#chemi'), list, { highlight: bloc, label: 'Coalition seats' }) };
  $('#csrc').onclick = e => { const b = e.target.closest('[data-v]'); if (!b) return; src = b.dataset.v; $('#csrc').querySelectorAll('[data-v]').forEach(x => x.setAttribute('aria-pressed', x === b)); draw() };
  $('#cchips').onclick = e => { const b = e.target.closest('[data-p]'); if (!b) return; const p = b.dataset.p; bloc.has(p) ? bloc.delete(p) : bloc.add(p); draw(); const nb = $('#cchips').querySelector(`[data-p="${p}"]`); if (nb) nb.focus() };
  $('#main').querySelectorAll('[data-pre]').forEach(b => b.onclick = () => { bloc = new Set(b.dataset.pre ? b.dataset.pre.split(',') : []); draw() });
  draw() }

/* ----- seat calculator (MMP: 5% or an electorate, Sainte-Laguë, overhang) ----- */
function parlCalculator() {
  const hide = forecastHidden(), e23 = (S.data.elections || []).filter(e => e.year < 2026).slice(-1)[0];
  const fromPolls = () => { const pr = projection(); return { pct: pr.pct, elec: pr.elec, label: `the average of the ${pr.n} latest polls (${pr.range})` } };
  const fromResult = () => { const pct = {}, elec = {}; (e23.parties || []).filter(r => r.party_vote_pct >= 1 || r.electorate_seats).forEach(r => { pct[r.party] = r.party_vote_pct; if (r.electorate_seats) elec[r.party] = r.electorate_seats }); return { pct, elec, label: `the ${e23.year} election result` } };
  let start = hide ? fromResult() : fromPolls();
  let pct = {}, elec = {};
  const load = s => { start = s; pct = {}; elec = {}; Object.keys({ ...s.pct, ...s.elec }).forEach(p => { pct[p] = Math.round((s.pct[p] || 0) * 10) / 10; elec[p] = s.elec[p] || 0 }) };
  load(start);
  $('#main').innerHTML = sectionFrame('seats', 'seats/calculator', `
    <header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('seats', 'i--s')} Seats · Seat calculator</p><h1>Turn votes into seats</h1>
      <p class="lede">Move the party-vote sliders and set who wins electorates. Seats are shared out of 120 with the Sainte-Laguë method, the same rules the Electoral Commission uses.</p></header>
    <div class="row"><span class="small muted">Start from</span><div class="seg" role="group" aria-label="Start from" id="cstart">${hide ? '' : `<button type="button" data-s="polls" aria-pressed="true">Latest polls</button>`}<button type="button" data-s="result" aria-pressed="${hide}">${e23.year} result</button></div></div>
    <div class="split split--7-5">
      <div class="stack"><p class="small soft" id="cfrom"></p><div class="calc" id="calc"></div>
        <div class="row"><button class="btn btn--s" type="button" id="csave">Use these electorate wins in the 2026 projection</button></div></div>
      <div class="stack sticky"><div class="row" style="align-items:baseline;gap:var(--s-3)"><span class="figure figure--s" id="ctot">120</span><span class="soft" id="cmaj"></span></div>
        <figure class="stack stack--s"><div id="calchemi"></div><figcaption class="sr-only">The seats below, party by party, say the same in words.</figcaption></figure><div id="cbars"></div><p class="small soft" id="csum"></p>
        <p class="sr-only" id="clive" aria-live="polite" aria-atomic="true"></p></div>
    </div>
    <section class="stack stack--s" aria-labelledby="h-how"><div class="shead"><h2 id="h-how">How the seats are worked out</h2></div>
      <div>
        <details class="disclose"><summary>1 · Who qualifies: the 5% threshold</summary><div class="disclose__body"><p class="small">A party gets list seats only if it wins at least 5% of the party vote or at least one electorate. Votes for every other party are "wasted": they elect nobody, and everyone else's share of the seats grows a little.</p></div></details>
        <details class="disclose"><summary>2 · Sharing the seats: Sainte-Laguë</summary><div class="disclose__body"><p class="small">The 120 seats (less any won by independents) go one at a time to whichever qualifying party has the highest score: its votes divided by 1, then 3, 5, 7… as it wins seats. Each party's electorate wins are counted first; list seats top it up to its share.</p></div></details>
        <details class="disclose"><summary>3 · When the House grows: overhang</summary><div class="disclose__body"><p class="small">If a party wins more electorates than its party-vote share entitles it to, it keeps them all and the House grows past 120. Those extra seats are the overhang, and the majority needed rises with them.</p></div></details>
      </div>
      <a class="more small" href="#/vote/mmp">How MMP works, step by step ${ic('chev', 'i--xs')}</a></section>`);
  const rows = () => Object.keys(pct).sort(byShort);
  const drawInputs = () => { $('#cfrom').textContent = `Starting from ${start.label}. Electorate wins: change them with − and +.`;
    $('#calc').innerHTML = rows().map(p => `<div class="calc__row" style="--pc:${pcolor(p)}" data-p="${p}">
      <div class="calc__head"><label for="pv-${p}">${ptagHTML(p)}<span class="sr-only"> party vote, percent</span></label><output class="calc__v num" id="out-${p}" for="pv-${p}" aria-hidden="true">${fmt(pct[p])}%</output></div>
      <input class="range" type="range" id="pv-${p}" min="0" max="60" step="0.1" value="${pct[p]}" aria-valuetext="${fmt(pct[p])}% of the party vote" style="--fill:${pct[p] / 60 * 100}%">
      <div class="calc__elec" role="group" aria-label="Electorates won by ${esc(pname(p))}"><span class="small soft" aria-hidden="true">Electorates won</span><button class="iconbtn" type="button" data-d="-1" aria-label="One fewer electorate for ${esc(pname(p))}">−</button><output class="num" id="ev-${p}" aria-live="polite" aria-label="${esc(pname(p))} electorates">${elec[p]}</output><button class="iconbtn" type="button" data-d="1" aria-label="One more electorate for ${esc(pname(p))}">+</button></div></div>`).join('') };
  const run = () => { const e = {}; for (const p in elec) if (elec[p]) e[p] = elec[p];
    const r = mmp(pct, e); const maj = Math.floor(r.total / 2) + 1;
    $('#ctot').textContent = r.total; $('#cmaj').textContent = `seats · ${maj} for a majority${r.overhang ? ` · ${r.overhang} overhang` : ''}`;
    const max = Math.max(1, ...Object.values(r.seats));
    $('#cbars').innerHTML = rows().map((p, k) => { const s = r.seats[p] || 0, el = e[p] || 0, list = Math.max(0, s - el), out = !s && pct[p] > 0;
      return `<div class="rrow" style="--pc:${pcolor(p)}">${ptagHTML(p)}<div class="bar"><i style="--w:${s / max * 100}%;--i:${k}"></i></div><span class="rrow__v"><b>${s}</b><span>${out ? 'below 5%' : el ? `${el} elec. + ${list} list` : `${list} list`}</span></span></div>` }).join('');
    const sum = Object.values(pct).reduce((a, b) => a + b, 0);
    $('#csum').innerHTML = `Party votes entered add to <b class="num">${fmt(sum)}%</b>${Math.abs(sum - 100) > 0.5 ? ' (seats are shared in proportion to what is entered)' : ''}. Wasted vote (parties below 5% with no electorate): <b class="num">${fmt(r.wasted)}%</b>${r.overhang ? `. Overhang: <b>${r.overhang}</b>, so the House has ${r.total} seats` : ''}.`;
    chamberUpdate($('#calchemi'), seatsFromComposition(r.seats, []), { label: 'Calculated seats' });
    // one short spoken summary, after the slider stops moving
    clearTimeout(S.calcLive); const said = `${r.total} seats, ${maj} for a majority${r.overhang ? `, ${r.overhang} overhang` : ''}. ` + rows().filter(p => r.seats[p]).map(p => `${pname(p)} ${r.seats[p]}`).join(', ') + '.';
    S.calcLive = setTimeout(() => { const l = $('#clive'); if (l) l.textContent = said }, 700); return e };
  $('#calc').addEventListener('input', ev => { const t = ev.target; if (!t.matches('.range')) return; const p = t.closest('[data-p]').dataset.p; pct[p] = +t.value; t.style.setProperty('--fill', (+t.value / 60 * 100) + '%'); $('#out-' + p).textContent = fmt(+t.value) + '%'; t.setAttribute('aria-valuetext', fmt(+t.value) + '% of the party vote'); run() });
  $('#calc').addEventListener('click', ev => { const b = ev.target.closest('[data-d]'); if (!b) return; const p = b.closest('[data-p]').dataset.p; elec[p] = Math.max(0, Math.min(72, (elec[p] || 0) + +b.dataset.d)); $('#ev-' + p).textContent = elec[p]; run() });
  $('#cstart').onclick = ev => { const b = ev.target.closest('[data-s]'); if (!b) return; $('#cstart').querySelectorAll('[data-s]').forEach(x => x.setAttribute('aria-pressed', x === b)); load(b.dataset.s === 'polls' ? fromPolls() : fromResult()); drawInputs(); run() };
  $('#csave').onclick = () => { store.set('elecAssume', JSON.stringify(run())); $('#csave').textContent = 'Saved: the projection now uses these electorate wins' };
  drawInputs(); run() }
