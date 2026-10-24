/* ----- Seats › Results (election night, 7 Nov from 7pm) -----
   Until a 2026 result is loaded this is a calm explainer: countdown, how counting works, what to watch, and 2023 for reference.
   On election day before 7pm it shows only the countdown and the explainer: nothing predictive. When a results object
   ({ parties: [{ party, party_vote_pct, electorate_seats, list_seats, total_seats }], counted_pct?, official?, updated?,
   source_url?, electorates? }) appears for 2026, it renders the live seat count. */
// Resolves as soon as the page is painted: the electorate map, the countdown and the refresh timer start without being awaited.
V.results = () => { resultsView(); armResultsRefresh() };
function resultsView() {
  const ph = electionPhase(), eday = ph === 'electionday', R = eday ? null : results2026();
  const body = R ? resultsLive(R) : resultsWaiting(ph);
  $('#main').innerHTML = sectionFrame('seats', 'seats/results', body);
  if (!R) { const tick = () => { const el = $('#rcount'); if (!el) return false; el.innerHTML = countdownHTML(); return true };
    tick(); const t = setInterval(() => { if (!tick()) clearInterval(t) }, 30000) }
  if (R) { bindElectionTable($('#rtable')); bindJumps($('#main'));
    if ((R.electorates || []).length) resultsMap() }
};
async function resultsMap() { try { await loadGeo(2025); const c = await mapContext(2026, 'general'); const box = $('#rmap'); if (!box || S.route !== 'seats/results') return;
      box.innerHTML = `<svg class="nzmap" viewBox="0 0 520 640" role="img" aria-label="Map of general electorates coloured by the 2026 winner" aria-describedby="rmapleg rmapalt"><text class="yr" x="20" y="96" font-size="96">2026</text>${mapPaths(c.feats, c.resFor, c.idx.bbox_mainland, 520, 640, null)}</svg>`;
      const counts = {}; c.feats.forEach(f => { const r = c.resFor(f); const p = r && r.party ? r.party : 'vacant'; counts[p] = (counts[p] || 0) + 1 }); $('#rmapleg').innerHTML = legendHTML(counts, true) } catch { } }
function countdownHTML() { const ms = ELECTION_DAY.getTime() - Date.now();
  if (ms <= 0) return `<span class="figure">7pm</span><span class="soft">Voting has closed. The first results usually arrive within the hour.</span>`;
  const d = Math.floor(ms / 864e5), h = Math.floor(ms % 864e5 / 36e5), m = Math.floor(ms % 36e5 / 6e4);
  return d >= 1 ? `<span class="figure">${d}<small class="rcount__u">${d === 1 ? 'day' : 'days'}</small> ${h}<small class="rcount__u">h</small></span><span class="soft">until voting closes at 7pm on Saturday 7 November</span>`
    : `<span class="figure">${h}<small class="rcount__u">h</small> ${m}<small class="rcount__u">m</small></span><span class="soft">until voting closes at 7pm tonight</span>` }
const COUNTING_HTML = `<section class="stack" aria-labelledby="h-count"><div class="shead"><h2 id="h-count">How the count works</h2></div>
  <ol class="rsteps">
    <li><b>7pm, election night: the preliminary count.</b> Votes cast in advance and on the day are counted at each voting place and published by the Electoral Commission through the evening. The first numbers are mostly advance votes, so early totals can shift as the night goes on.</li>
    <li><b>The next three weeks: special votes.</b> Votes from people voting outside their electorate, overseas, or not on the printed roll are checked before they are counted. They are not in the election-night numbers. In recent elections they were roughly one vote in six (closer to one in five in 2023), and they have moved a seat or two each time.</li>
    <li><b>Friday 27 November: the official result.</b> Every vote is counted again, specials included, and the final seats are declared. Only then is the Parliament settled; a recount can still be asked for in a close electorate.</li></ol>
  <p class="srcline">Official results are published by the Electoral Commission at <a href="https://www.electionresults.govt.nz" target="_blank" rel="noopener">electionresults.govt.nz</a>. Dates: <a href="https://vote.nz/2026-general-election/about/overview/key-dates" target="_blank" rel="noopener">vote.nz key dates</a>.</p></section>`;
const WATCH_HTML = `<section class="stack stack--s" aria-labelledby="h-watch"><div class="shead"><h2 id="h-watch">What to watch on the night</h2></div>
  <div>
    <details class="disclose"><summary>The 5% line</summary><div class="disclose__body"><p class="small">A party needs 5% of the party vote, or one electorate, to get list seats. A party just under the line gets none, and its votes are "wasted": everyone else's share of the seats grows. A few tenths of a point can move several seats.</p></div></details>
    <details class="disclose"><summary>Electorate lifeboats</summary><div class="disclose__body"><p class="small">If a small party's candidate wins an electorate, the party gets its full share of seats even below 5%. That is why some electorates (Epsom in past elections) draw attention, and why larger parties sometimes signal they won't campaign hard there.</p></div></details>
    <details class="disclose"><summary>Overhang</summary><div class="disclose__body"><p class="small">A party that wins more electorates than its party vote earns keeps them, and the House grows past 120. The number needed to govern then rises from 61.</p></div></details>
    <details class="disclose"><summary>61 isn't the end</summary><div class="disclose__body"><p class="small">A government needs a majority on confidence votes, which can mean days or weeks of talks after the result. The coalition builder lets you try combinations on any result.</p><a class="more small" href="#/seats/coalition">Coalition builder ${ic('chev', 'i--xs')}</a></div></details>
  </div></section>`;
function resultsWaiting(ph) {
  const eday = ph === 'electionday', live = ph === 'results' || ph === 'after';
  const head = `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('seats', 'i--s')} Seats · Results</p>
    <h1>${live ? 'Results are coming in' : eday ? 'Results from 7pm tonight' : 'Results from 7pm Saturday 7 November'}</h1>
    <p class="lede">${live ? 'The Electoral Commission is publishing the preliminary count. This page shows the seat count as soon as it is loaded here; until then the official site has it first.' : 'This page turns into the live seat count when voting closes. Until then, here is how the count works.'}</p>
    ${live ? `<div class="row"><a class="btn btn--ink" href="https://www.electionresults.govt.nz" target="_blank" rel="noopener">Official results ${ic('ext', 'i--xs')}</a></div>` : `<div class="rcount" id="rcount" aria-live="off"></div>`}</header>`;
  if (eday) return head + COUNTING_HTML + `<p class="small soft">Everything else, including parties, policies, candidates and your electorate, stays available today. <a href="https://map.vote.nz" target="_blank" rel="noopener">Find a voting place</a>.</p>`;
  return head + COUNTING_HTML + WATCH_HTML + results2023Block() }
function results2023Block() {
  const e = (S.data.elections || []).filter(x => x.year < 2026).slice(-1)[0]; if (!e) return '';
  const parl = (S.data.parliaments || []).find(p => p.election_year === e.year);
  const comp = (parl && (parl.composition_at_election || parl.composition_start)) || Object.fromEntries((e.parties || []).filter(r => r.total_seats).map(r => [r.party, r.total_seats]));
  const rows = (e.parties || []).filter(r => r.party_vote_pct != null).sort((a, b) => byShort(a.party, b.party)), max = Math.max(...rows.map(r => r.party_vote_pct));
  return `<section class="stack" aria-labelledby="h-ref"><div class="shead"><div class="shead__row"><h2 id="h-ref">For reference: the ${e.year} result</h2><span class="small muted">official count · parties A–Z</span></div></div>
    <div class="split split--5-7"><div class="stack stack--s">${chamberSVG(seatsFromComposition(comp, []), { label: `Seats after the ${e.year} election`, describedby: 'r23leg' })}<div class="legend" id="r23leg" role="group" aria-label="Seats by party, A to Z">${legendHTML(comp)}</div></div>
      <div>${rows.map((r, k) => `<div class="rrow" style="--pc:${pcolor(r.party)}">${ptagHTML(r.party, r.name || pname(r.party))}<div class="bar"><i style="--w:${(r.party_vote_pct / max * 100).toFixed(1)}%;--i:${k}"></i></div><span class="rrow__v"><b>${fmt(r.party_vote_pct, 1)}%</b><span>${comp[r.party] || 0} seats</span></span></div>`).join('')}</div></div>
    <p class="srcline">${esc(seatDate(e.date))} · turnout ${fmt(e.turnout_pct)}% · Electoral Commission official result${(e.sources || []).length ? ` · <a href="${esc(typeof e.sources[0] === 'string' ? e.sources[0] : e.sources[0].url)}" target="_blank" rel="noopener">source</a>` : ''}. Seats as declared at the official count${parl && parl.composition_at_election ? '' : ' and after'}.</p>
    <div class="row"><a class="more small" href="#/seats/parliament">Every Parliament since 2011 ${ic('chev', 'i--xs')}</a></div></section>` }
function resultsLive(R) {
  const rows = (R.parties || []).slice().sort((a, b) => byShort(a.party, b.party));
  const comp = Object.fromEntries(rows.filter(r => r.total_seats).map(r => [r.party, r.total_seats]));
  const total = Object.values(comp).reduce((a, b) => a + b, 0), maj = Math.floor(total / 2) + 1;
  const F = S.data.forecast, fBy = Object.fromEntries(((F && F.parties) || []).map(x => [x.party, x]));
  const max = Math.max(45, Math.ceil(Math.max(...rows.map(r => Math.max(r.party_vote_pct || 0, ((fBy[r.party] || {}).forecast_vote_80 || [0, 0])[1]))) / 5) * 5);
  const pc = v => (Math.max(0, Math.min(max, v)) / max * 100).toFixed(1) + '%';
  return `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('seats', 'i--s')} Seats · Results ${R.official ? '<span class="badge badge--ink">Official</span>' : '<span class="badge badge--live">Live</span>'}</p>
      <h1>2026 election: the ${R.official ? 'official' : 'preliminary'} count</h1>
      <p class="lede">${R.counted_pct != null ? `Results in from ${fmt(R.counted_pct, 0)}% of voting places${R.votes_cast ? ` (${Number(R.votes_cast).toLocaleString('en-NZ')} votes so far)` : ''}. ` : ''}${R.official ? 'Every vote counted, special votes included.' : 'Preliminary results leave out special votes (roughly one in six). The final result is due Friday 27 November.'}</p>
      <p class="srcline">${R.updated ? `Commission feed updated ${esc(String(R.updated).replace('T', ' ').slice(0, 16))} NZ time · this page refreshes every two minutes · ` : ''}Source: <a href="${esc(R.source_url || 'https://www.electionresults.govt.nz')}" target="_blank" rel="noopener">Electoral Commission</a></p></header>
    <section class="stack" aria-labelledby="h-live"><div class="shead"><div class="shead__row"><h2 id="h-live">Seats</h2><span class="small muted">${total} seats · ${maj} to govern</span></div></div>
      <div class="split split--7-5"><div class="stack stack--s">${chamberSVG(seatsFromComposition(comp, []), { label: '2026 seat count', describedby: 'rleg' })}<div class="legend" id="rleg" role="group" aria-label="Seats by party, A to Z">${legendHTML(comp)}</div></div>
        <div class="stack"><p class="small soft">No single party is shown as the winner: governments are formed by negotiation, and the count can still move.</p><a class="btn btn--s" href="#/seats/coalition">Try combinations in the coalition builder</a></div></div></section>
    <nav class="stack stack--s" aria-labelledby="h-onpage"><h2 class="h4" id="h-onpage">On this page</h2><div class="rows">
      ${jumpRow('h-pv', 'Party vote', 'Every party\'s share so far, against the forecast range and the 5% line')}
      ${(R.electorates || []).length ? jumpRow('h-rmap', 'Electorates', 'Who is ahead in each seat, on the map') : ''}
      ${jumpRow('h-el2026', 'The full table', 'Party vote, votes, electorate and list seats')}
      ${R.official ? '' : jumpRow('h-count', 'How the count works', 'Preliminary tonight, specials next, official on 27 November')}</div></nav>
    <section class="stack" aria-labelledby="h-pv"><div class="shead"><div class="shead__row"><h2 id="h-pv">Party vote</h2><span class="small muted">parties A–Z</span></div></div>
      <div>${rows.map(r => { const f = fBy[r.party]; const v = r.party_vote_pct || 0;
        return `<div class="rrow" style="--pc:${pcolor(r.party)}">${ptagHTML(r.party, r.name || pname(r.party))}<div class="rbar" style="${f ? `--lo:${pc(f.forecast_vote_80[0])};--hi:${pc(f.forecast_vote_80[1])};` : '--lo:0%;--hi:0%;'}--m:${pc(v)};--x:${pc(5)}" role="img" aria-label="${esc(pname(r.party))}: ${fmt(v)}% counted${f ? `; the forecast said ${Math.round(f.forecast_vote_80[0])} to ${Math.round(f.forecast_vote_80[1])}%` : ''}"><span class="rbar__mark"></span>${f ? '<span class="rbar__band rbar__band--ghost"></span>' : ''}<span class="rbar__mean"></span></div><span class="rrow__v"><b>${fmt(v)}%</b><span>${r.total_seats || 0} seats${r.electorate_seats ? ` · ${r.electorate_seats} elec.` : ''}</span></span></div>` }).join('')}</div>
      <div class="legend small"><span><span class="lg-mean"></span> the count says</span>${F ? '<span><span class="lg-band"></span> the forecast said (8 in 10 range, 23 Oct)</span>' : ''}<span><span class="lg-thr"></span> 5% threshold</span></div></section>
    ${(R.electorates || []).length ? `<section class="stack" aria-labelledby="h-rmap"><div class="shead"><div class="shead__row"><h2 id="h-rmap">Electorates</h2><a class="more small" href="#/seats/map/2026">Explore the map ${ic('chev', 'i--xs')}</a></div></div><div class="mapstage rmap"><div id="rmap"><p class="muted small">Loading the map…</p></div><div class="legend" id="rmapleg" role="group" aria-label="Electorates by party, A to Z"></div><p class="small soft" id="rmapalt">Every seat and who is ahead is named in <a href="#/seats/map/2026">the map's list view</a>.</p></div></section>` : `<div class="row"><a class="more" href="#/seats/map/2026">Electorate map ${ic('chev', 'i--xs')}</a></div>`}
    <section class="stack" id="rtable" aria-labelledby="h-el2026">${electionTableHTML({ year: 2026, date: R.date, parties: R.parties, official: R.official })}</section>
    ${R.official ? '' : COUNTING_HTML}` }

/* Election night: poll site/data/results.json every two minutes and re-render when the Commission feed has moved.
   The timer lives in S.resultsTimer so the router clears it on navigation. */
function armResultsRefresh() {
  if (S.resultsTimer) clearInterval(S.resultsTimer);
  const R = results2026(); if (R && R.official) return;
  if (!['results', 'after'].includes(electionPhase())) return;
  S.resultsTimer = setInterval(async () => {
    if (S.route !== 'seats/results') { clearInterval(S.resultsTimer); S.resultsTimer = null; return }
    try { const r = await getJSON('data/results.json?t=' + Date.now()); const cur = results2026();
      if (r && r.votes_cast && (!cur || r.updated !== cur.updated || r.votes_cast !== cur.votes_cast)) { S.data.upcoming = { ...(S.data.upcoming || { year: 2026 }), results: r }; V.results() } } catch {}
  }, 120000) }
