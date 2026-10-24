/* ----- Seats › Polls & forecast -----
   The only page in the guide that orders parties by polling (and it says so). Ranges come before middles, probabilities are
   "N in 100" with icon arrays, and the model's misses are listed. Also holds the long view (party vote since 2008). */
const isPollster = p => p.pollster && !/election result/i.test(p.pollster);
const PARTY_ABBR = { national: 'NAT', labour: 'LAB', green: 'GRN', act: 'ACT', 'nz-first': 'NZF', 'te-pati-maori': 'TPM', opportunity: 'TOP' };
const pollKey = n => ({ 'National': 'national', 'Labour': 'labour', 'Green': 'green', 'ACT': 'act', 'NZ First': 'nz-first', 'Te Pāti Māori': 'te-pati-maori', 'TOP': 'opportunity', 'Te Tai Tokerau Party': 'te-tai-tokerau-party', 'Independent': 'independent' }[n] || n);
const iconArray = n => `<div class="iconarray" aria-hidden="true">${Array.from({ length: 100 }, (_, k) => `<i${k < Math.round(n || 0) ? ' class="on"' : ''} style="--i:${k}"></i>`).join('')}</div>`;

/* The page is split into a summary and five sub-views, each with its own address (#/seats/polls/<sub>):
   summary (the headline ranges and who could govern) · trend · all (every poll) · maori · wrong (how this could be wrong,
   and the track record) · method. The router passes no argument yet, so the sub is also read from the route. */
const POLL_SUBS = [['', 'Summary'], ['trend', 'Trend'], ['all', 'Every poll'], ['maori', 'Māori seats', true], ['wrong', 'Could be wrong', true], ['method', 'Method']];
V.polls = sub => {
  sub = sub || String(S.route || '').split('/')[2] || '';
  const polls = (S.data.polls || []).filter(isPollster).sort((a, b) => b.date.localeCompare(a.date));
  const F = S.data.forecast, hasF = !!(F && (F.parties || []).length);
  if (!POLL_SUBS.some(([k, , f]) => k === sub && (!f || hasF))) sub = '';
  const pollsters = [...new Set(polls.map(p => p.pollster))];
  const pr = projection(8);
  // Poll order: by the forecast middle estimate (or the poll average without a forecast). Only on this page.
  const parties = hasF ? F.parties.slice().sort((a, b) => b.forecast_vote_mean - a.forecast_vote_mean).map(x => x.party)
    : Object.entries(pr.pct).sort((a, b) => b[1] - a[1]).filter(([, v]) => v >= 0.8).map(([p]) => p);
  const asOf = hasF ? F.as_of : (polls[0] || {}).date;
  const D = { polls, F, hasF, pollsters, pr, parties, asOf };
  const body = ({ trend: pollsTrend, all: pollsAll, maori: pollsMaori, wrong: pollsWrong, method: pollsMethod })[sub] || pollsSummary;
  $('#main').innerHTML = sectionFrame('seats', 'seats/polls', `<div class="stack stack--xl" id="polls-body">${body(D)}</div>`);
  const after = { trend: bindTrend, all: bindAllPolls, '': bindSummary }[sub]; if (after) after(D);
};
const pollsUpdated = D => `<span class="badge">Updated ${esc(seatDate(D.asOf))}${D.hasF && D.F.days_to_election != null ? `, ${esc(D.F.days_to_election)} days out` : ''}</span><span class="badge badge--outline">${ic('lock', 'i--xs')} Hidden 7 Nov until 7pm</span>`;
// The sub-views' header: a way back to the summary, the title, and a switch between the sub-views.
const pollNav = (D, cur) => `<nav aria-label="Polls and forecast pages"><div class="seg pollnav">${POLL_SUBS.filter(([, , f]) => !f || D.hasF).map(([k, l]) => `<a href="#/seats/polls${k ? '/' + k : ''}"${k === cur ? ' aria-current="page"' : ''}>${esc(l)}</a>`).join('')}</div></nav>`;
function pollsHead(D, cur, h1, lede) {
  return `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('poll', 'i--s')} Seats · Polls &amp; forecast</p><h1>${h1}</h1>${lede ? `<p class="lede">${lede}</p>` : ''}<div class="row">${pollsUpdated(D)}</div></header>
    ${pollNav(D, cur)}` }
const pollsSrc = F => `<p class="srcline">Polls: each pollster's published release, compiled via <a href="${esc((F && F.polls_source) || 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_2026_New_Zealand_general_election')}" target="_blank" rel="noopener">the public record on Wikipedia</a>${F && F.polls_retrieved ? `, retrieved ${esc(seatDate(F.polls_retrieved))}` : ''}. <a href="#/seats/polls/method">Method and sources</a></p>`;

/* ----- summary: the headline ranges, who could govern, then where to go deeper ----- */
function pollsSummary(D) { const { polls, pollsters, F, hasF } = D;
  const n = polls.length, latest = polls[0];
  const deeper = [
    ['trend', 'poll', 'Trend since 2023', `Every party in every poll with an 8-poll average, and the long view back to 2008.`],
    ['all', 'list', 'Every poll', `All ${n} polls from ${pollsters.length} pollsters in a table, each linked to its release${latest ? `; latest ${esc(latest.pollster)}, ${esc(seatDate(latest.date))}` : ''}.`],
    ...(hasF && Object.keys((F.electorates || {}).maori_seats || {}).length ? [['maori', 'map', 'Māori electorates', 'The seven Māori seats, and Epsom: the chance each party wins. Low confidence.']] : []),
    ...(hasF ? [['wrong', 'shield', 'How this could be wrong', 'What the polls can\'t know, and our track record since 2011, misses included.']] : []),
    ['method', 'book', 'Method and sources', 'How the forecast is built, and where every number comes from.']];
  return `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('poll', 'i--s')} Seats · Polls &amp; forecast</p><h1>What the polls say, and what they can't</h1>
      <p class="lede">${n} polls from ${pollsters.length} pollsters since the 2023 election, pooled into ranges. Read the range, not a single number: polls have missed by several points before.</p>
      <div class="row">${pollsUpdated(D)}<a class="more small" href="#/about/page/guide/forecast-method.md">How the forecast works ${ic('chev', 'i--xs')}</a></div></header>
    ${pollNav(D, '')}
    ${hasF ? forecastSummary(F) : pollAverageBlock(D.pr)}
    <section class="stack" aria-labelledby="h-deeper"><div class="shead"><h2 id="h-deeper">Go deeper</h2></div>
      <div class="rows">${deeper.map(([k, i, t, s]) => rowlink('#/seats/polls/' + k, i, t, s)).join('')}</div>
      ${pollsSrc(F)}</section>` }
function bindSummary(D) { const { F } = D; let mode = 'vote';
  const fbox = $('#frows'); if (!fbox) return; fbox.innerHTML = forecastRows(F, mode);
  $('#fmode').onclick = e => { const b = e.target.closest('[data-m]'); if (!b) return; mode = b.dataset.m; $('#fmode').querySelectorAll('[data-m]').forEach(x => x.setAttribute('aria-pressed', x === b)); fbox.innerHTML = forecastRows(F, mode); $('#flegend').innerHTML = forecastLegend(mode) } }

/* ----- trend: the chart with party and pollster filters, and past elections ----- */
function pollsTrend(D) { const { polls, pollsters, parties } = D;
  return pollsHead(D, 'trend', 'The trend since 2023', 'Every published poll since the last election, with each party\'s 8-poll average. Switch to "Since 2008" for the election results before that.') + `
    <section class="stack" aria-labelledby="h-trend">
      <div class="shead"><div class="shead__row"><h2 id="h-trend">Party vote in the polls</h2><div class="seg" role="group" aria-label="Time span" id="pspan"><button type="button" data-s="term" aria-pressed="true">Since 2023</button><button type="button" data-s="long" aria-pressed="false">Since 2008</button></div></div>
        <p class="micro muted">Parties in poll order, largest first: this is the only page in the guide sorted by polling.</p></div>
      <div class="stack stack--s"><span class="small muted" id="pp-parties-l">Parties shown (tap to hide or show)</span><div class="chips chips--scroll" id="pp-parties" role="group" aria-labelledby="pp-parties-l">${parties.map(p => `<button class="chip" type="button" data-p="${p}" aria-pressed="true" style="--pc:${pcolor(p)}"><span class="sw"></span>${esc(pname(p))}</button>`).join('')}</div></div>
      <div class="stack stack--s"><span class="small muted" id="pp-pollsters-l">Pollsters included</span><div class="chips chips--scroll" id="pp-pollsters" role="group" aria-labelledby="pp-pollsters-l">${pollsters.map(n => `<button class="chip" type="button" data-n="${esc(n)}" aria-pressed="true">${esc(n)} <span class="count">${polls.filter(p => p.pollster === n).length}<span class="sr-only"> polls</span></span></button>`).join('')}</div></div>
      <figure class="stack stack--s" id="pchart"></figure>
      <p class="srcline" id="ptip" aria-live="polite">Tap a dot for the pollster, date and sample.</p>
      <details class="disclose" id="ppast-d"><summary>Past elections at a glance: seats, turnout and wasted vote since 2008</summary><div class="disclose__body" id="ppast"></div></details>
      ${pollsSrc(D.F)}</section>` }
function bindTrend(D) { const { polls, pollsters, parties } = D; const onP = new Set(parties), on = new Set(pollsters); let span = 'term';
  const draw = () => { const sel = polls.filter(p => on.has(p.pollster)); $('#pchart').innerHTML = pollChart(sel, parties.filter(p => onP.has(p)), { long: span === 'long' }) };
  $('#pp-parties').onclick = e => { const b = e.target.closest('[data-p]'); if (!b) return; onP.has(b.dataset.p) ? onP.delete(b.dataset.p) : onP.add(b.dataset.p); b.setAttribute('aria-pressed', onP.has(b.dataset.p)); draw() };
  $('#pp-pollsters').onclick = e => { const b = e.target.closest('[data-n]'); if (!b) return; on.has(b.dataset.n) ? on.delete(b.dataset.n) : on.add(b.dataset.n); b.setAttribute('aria-pressed', on.has(b.dataset.n)); draw() };
  $('#pspan').onclick = e => { const b = e.target.closest('[data-s]'); if (!b) return; span = b.dataset.s; $('#pspan').querySelectorAll('[data-s]').forEach(x => x.setAttribute('aria-pressed', x === b)); draw() };
  $('#pchart').onclick = e => { const c = e.target.closest('[data-tip]'); if (c) $('#ptip').textContent = c.dataset.tip };
  $('#ppast').innerHTML = pastElectionsCharts();
  $('#ppast').onclick = e => { const c = e.target.closest('[data-tip]'); if (c) $('#ppast-tip').textContent = c.dataset.tip };
  draw() }

/* ----- every poll: latest from each pollster, the full table, house effects ----- */
function pollsAll(D) { const { polls, pollsters, parties, F, hasF } = D;
  const internal = new Set(((F && F.pollsters) || []).filter(q => q.internal).map(q => q.pollster));
  const latestBy = pollsters.map(n => polls.find(p => p.pollster === n)).sort((a, b) => b.date.localeCompare(a.date));
  const th = parties.map(p => `<th class="n" scope="col"><abbr title="${esc(pname(p))}">${esc(PARTY_ABBR[p] || pname(p))}</abbr></th>`).join('');
  return pollsHead(D, 'all', 'Every poll since 2023', `${polls.length} polls from ${pollsters.length} pollsters, each linked to the pollster's own release. Party columns are in poll order, largest first: the only page in the guide sorted this way.`) + `
    <section class="stack" aria-labelledby="h-latest">
      <div class="shead"><div class="shead__row"><h2 id="h-latest">Latest poll from each pollster</h2><span class="small muted">newest first</span></div></div>
      ${twrap('Latest poll from each pollster', `<table class="table"><caption class="sr-only">Latest poll from each pollster, party-vote percentages</caption><thead><tr><th scope="col">Pollster</th><th scope="col">Ended</th>${th}<th class="n" scope="col">Sample</th><th scope="col">Release</th></tr></thead>
        <tbody>${latestBy.map(p => `<tr><th scope="row"><b>${esc(p.pollster)}</b>${internal.has(p.pollster) ? ' <span class="badge badge--outline">Party-commissioned</span>' : ''}</th><td class="num">${esc(seatDate(p.date))}</td>${parties.map(x => `<td class="n">${p.parties[x] != null ? fmt(p.parties[x]) : '–'}</td>`).join('')}<td class="n">${p.sample_size ? Number(p.sample_size).toLocaleString('en-NZ') : '–'}</td><td>${p.source_url ? `<a href="${esc(p.source_url)}" target="_blank" rel="noopener">release<span class="sr-only"> from ${esc(p.pollster)}, ${esc(seatDate(p.date))}</span> ${ic('ext', 'i--xs')}</a>` : '<span class="muted">none linked</span>'}</td></tr>`).join('')}</tbody></table>`)}
      <p class="micro muted">Each pollster's own release, linked. Fieldwork end dates. Party-vote shares exclude undecided voters, as each pollster publishes them. A pollster that differs from the others isn't necessarily wrong.</p>
      ${hasF && (F.pollsters || []).length ? houseEffectsBlock(F) : ''}</section>
    <section class="stack" aria-labelledby="h-allpolls">
      <div class="shead"><div class="shead__row"><h2 id="h-allpolls">All ${polls.length} polls</h2><span class="small muted">newest first · pollster names link to each release</span></div></div>
      <div id="palltable"></div>
      ${pollsSrc(F)}</section>` }
function bindAllPolls(D) { const { polls, parties } = D; let lim = 40;
  const th = parties.map(p => `<th class="n" scope="col"><abbr title="${esc(pname(p))}">${esc(PARTY_ABBR[p] || pname(p))}</abbr></th>`).join('');
  const all = () => { $('#palltable').innerHTML = twrap(`All ${polls.length} polls`, `<table class="table"><caption class="sr-only">Every poll since 2023, newest first, party-vote percentages</caption><thead><tr><th scope="col">Ended</th><th scope="col">Pollster</th>${th}<th class="n" scope="col">Sample</th></tr></thead><tbody>${polls.slice(0, lim).map(p => `<tr><td class="num">${esc(seatDate(p.date))}</td><td>${p.source_url ? `<a href="${esc(p.source_url)}" target="_blank" rel="noopener">${esc(p.pollster)}</a>` : esc(p.pollster)}</td>${parties.map(x => `<td class="n">${p.parties[x] != null ? fmt(p.parties[x]) : '–'}</td>`).join('')}<td class="n">${p.sample_size ? Number(p.sample_size).toLocaleString('en-NZ') : '–'}</td></tr>`).join('')}</tbody></table>`) + `<p class="small muted" aria-live="polite">Showing ${Math.min(lim, polls.length)} of ${polls.length}.</p>${polls.length > lim ? `<div class="row"><button class="btn btn--s" type="button" id="pmore2">Show ${Math.min(40, polls.length - lim)} more</button></div>` : ''}`;
    const m = $('#pmore2'); if (m) m.onclick = () => { lim += 40; all(); const b = $('#pmore2'); if (b) b.focus() } };
  all() }

/* ----- the Māori seats and Epsom ----- */
function pollsMaori(D) { const { F } = D;
  return pollsHead(D, 'maori', 'The Māori electorates', 'The seven Māori seats elect MPs chosen by voters on the Māori roll. They matter for the size of the House: a party that wins more of them than its party vote earns adds overhang seats.') + maoriSeatsBlock(F) +
    `<section class="stack" aria-labelledby="h-mlinks"><div class="shead shead--quiet"><h2 id="h-mlinks" class="h4">More on these seats</h2></div><div class="rows">
      ${rowlink('#/seats/map/2023', 'map', 'The Māori electorates on the map', 'Who has won each seat since 2011. Switch the map to "Māori".')}
      ${V.maoriHub ? rowlink('#/vote/maori', 'vote', 'Māori electorates explained', 'The Māori roll, the option, and the candidates.') : ''}
      ${rowlink('#/seats/calculator', 'scale', 'Overhang in the seat calculator', 'Set electorate wins and see when the House grows past 120.')}</div>
      ${pollsSrc(F)}</section>` }

/* ----- how this could be wrong, and the track record ----- */
function pollsWrong(D) { const { F } = D;
  return pollsHead(D, 'wrong', 'How this could be wrong', 'A forecast built from polls inherits their blind spots. Here is what it can\'t see, and how the same method did at every election since 2011.') +
    unknownsBlock(F, 'What the forecast can\'t know') + trackRecordBlock(F) + pollsSrc(F) }

/* ----- method and sources ----- */
function pollsMethod(D) { const { F, hasF } = D;
  return pollsHead(D, 'method', 'Method and sources', 'How the polls become ranges, and where every number on these pages comes from.') + `
    <section class="stack" aria-labelledby="h-meth"><div class="shead"><h2 id="h-meth">How the forecast works</h2></div>
      ${hasF && F.simulation ? `<p class="soft" style="max-width:var(--measure)">${Number(F.simulation.draws).toLocaleString('en-NZ')} simulated elections. A poll-of-polls with recency weighting and pollster house effects; polling error calibrated on the 2011–2023 elections; seats shared by Sainte-Laguë with the 5% threshold and electorate seats. Probabilities are rounded to whole numbers on purpose.</p>`
        : `<p class="soft" style="max-width:var(--measure)">Until the full forecast is published, this page shows a plain average of the latest polls, turned into seats with the Sainte-Laguë formula.</p>`}
      <p class="soft" style="max-width:var(--measure)">Parties on these pages are in poll order, largest first. This is the only page in the guide that orders parties by polling; everywhere else is A–Z or ballot order.</p>
      ${hasF && (F.how_to_read || []).length ? `<details class="disclose"><summary>How to read the ranges</summary><div class="disclose__body"><ul class="small">${F.how_to_read.map(x => `<li>${esc(x)}</li>`).join('')}</ul>${F.undecided_note ? `<p class="small">${esc(F.undecided_note)}</p>` : ''}</div></details>` : ''}
      <div class="rows">${rowlink('#/about/page/guide/forecast-method.md', 'doc', 'The full method', 'Every step of the model, with the assumptions written down.')}${hasF ? rowlink('#/seats/polls/wrong', 'shield', 'How this could be wrong', 'The caveats, and the track record with every miss.') : ''}</div></section>
    <section class="stack" aria-labelledby="h-srcs"><div class="shead"><h2 id="h-srcs">Sources</h2></div>
      <p class="srcline">Polls: each pollster's published release, compiled via <a href="${esc((F && F.polls_source) || 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_2026_New_Zealand_general_election')}" target="_blank" rel="noopener">the public record on Wikipedia</a>${F && F.polls_retrieved ? `, retrieved ${esc(seatDate(F.polls_retrieved))}` : ''}. Each poll's own release is linked on <a href="#/seats/polls/all">Every poll</a>.${hasF ? ` Forecast generated ${esc(seatDate(F.generated))}; latest poll ${esc(seatDate(F.latest_poll_date))}.` : ''}</p>
      ${hasF && (F.sources || []).length ? `<p class="srcline">Method sources: ${F.sources.map((u, k) => `<a href="${esc(u)}" target="_blank" rel="noopener"><span class="sr-only">Method source </span>${k + 1}</a>`).join(' ')}</p>` : ''}
      <p class="srcline">Election results: official counts, Electoral Commission.</p></section>` }

/* ----- forecast blocks ----- */
function forecastSummary(F) {
  const H = F.headline || {}, blocs = (F.blocs || []).slice().sort((a, b) => a.bloc.localeCompare(b.bloc, 'en-NZ'));
  // the two groups the headline reports on (the current government and the main opposition parties); other combinations go in a table
  const same = (b, set) => (b.parties || []).length === set.length && set.every(p => b.parties.includes(p));
  let main = blocs.filter(b => same(b, ['national', 'act', 'nz-first']) || same(b, ['labour', 'green', 'te-pati-maori'])); if (!main.length) main = blocs.slice(0, 2);
  const more = blocs.filter(b => !main.includes(b));
  const none = H.p_no_bloc_majority ?? F.p_no_bloc_majority;
  const bloc = (n, title, who, extra = '') => `<div class="bloc"><div class="bloc__h"><span class="bloc__n">${Math.round(n)}<small>in 100</small></span></div><p style="font-weight:700">${title}</p>${who}${extra}${iconArray(n)}</div>`;
  const whoHTML = ps => `<div class="bloc__who">${ps.map(p => `<span style="--pc:${pcolor(p)}"><span class="sw"></span>${esc(pname(p))}</span>`).join('')}</div>`;
  const lp = H.largest_party_probability || {};
  const facts = [
    ...Object.keys(lp).sort(byShort).map(p => [`${pname(p)} is the largest party`, lp[p]]),
    ['Opportunity (TOP) clears 5%', H.p_TOP_over_5pct], ['NZ First clears 5%', H.p_NZ_First_over_5pct], ['Te Pāti Māori clears 5%', H.p_TPM_over_5pct],
    ['Opportunity (TOP) holds the balance of power', H.p_TOP_holds_balance_of_power], ['NZ First holds the balance of power', H.p_NZ_First_holds_balance_of_power],
    ['There are overhang seats (a House bigger than 120)', H.p_overhang]].filter(([, v]) => v != null);
  const others = Object.entries(F.other_seat_winners || {}).filter(([, v]) => v.p_wins_seat);
  return `<section class="stack stack--l" aria-labelledby="h-fc">
    <div class="shead"><div class="shead__row"><h2 id="h-fc">If the election were held on today's polling</h2><div class="seg" role="group" aria-label="Show" id="fmode"><button type="button" data-m="vote" aria-pressed="true">Party vote</button><button type="button" data-m="seats" aria-pressed="false">Seats</button></div></div>
      <p class="small muted">Forecast ${esc(seatDate(F.generated))} · latest poll ${esc(seatDate(F.latest_poll_date))} · ${esc(F.n_polls_this_term)} polls this term</p></div>
    <div class="split split--7-5">
      <div class="stack"><div id="frows"></div><div class="legend small" id="flegend">${forecastLegend('vote')}</div>
        ${others.length ? `<p class="small soft">Seats outside the parties above: ${others.map(([p, v]) => `${esc(pname(p))} wins an electorate in ${inHundred(v.p_wins_seat)} simulations`).join('; ')}.</p>` : ''}
        <p class="micro muted">Sorted by the forecast's middle estimate. This is the only page in the guide that orders parties by polling; everywhere else is A–Z or ballot order.</p></div>
      <div class="stack stack--l"><h3>Who could govern?</h3>
        <p class="small soft">From ${F.simulation ? Number(F.simulation.draws).toLocaleString('en-NZ') : 'tens of thousands of'} simulated elections built from the polls and how far they have missed before. Not a prediction: in 2017 and 2020 late swings moved the result.</p>
        <div class="blocs">${main.map(b => bloc(b.p_majority, `${esc(b.bloc)} win a majority`, whoHTML(b.parties), `<p class="small soft">Seats: likely ${(b.seats_80 || []).join('–')}, middle ${b.seats_expected}</p>`)).join('')}
          ${none != null ? bloc(none, 'Neither group has a majority on its own', '', H.p_TOP_holds_balance_of_power != null ? `<p class="small soft">The balance of power: Opportunity (TOP) holds it in ${inHundred(H.p_TOP_holds_balance_of_power)} simulations, NZ First in ${inHundred(H.p_NZ_First_holds_balance_of_power)}.</p>` : '') : ''}</div>
        ${more.length ? `<details class="disclose"><summary>Other combinations</summary><div class="disclose__body">${twrap('Every combination of parties', `<table class="table"><thead><tr><th scope="col">Parties</th><th class="n" scope="col">Seats, likely</th><th class="n" scope="col">Majority</th></tr></thead><tbody>${blocs.map(b => `<tr><td>${esc(b.bloc)}</td><td class="n">${(b.seats_80 || []).join('–')}</td><td class="n"><b>${inHundred(b.p_majority)}</b></td></tr>`).join('')}</tbody></table>`)}<p class="small">${esc((F.majority_threshold || {}).note || '')}</p></div></details>` : ''}
        ${facts.length ? `<details class="disclose"><summary>More from the simulations</summary><div class="disclose__body"><dl class="dl">${facts.map(([l, v]) => `<dt>${esc(l)}</dt><dd>${inHundred(v)}</dd>`).join('')}</dl></div></details>` : ''}
      </div>
    </div>
    <details class="disclose"><summary>How to read this</summary><div class="disclose__body"><ul class="small">${(F.how_to_read || []).map(x => `<li>${esc(x)}</li>`).join('')}</ul>${F.undecided_note ? `<p class="small">${esc(F.undecided_note)}</p>` : ''}</div></details>
  </section>` }
function forecastLegend(mode) { return `<span><span class="lg-band"></span> 8 in 10 chance the result lands here</span><span><span class="lg-mean"></span> middle estimate</span>${mode === 'vote' ? '<span><span class="lg-thr"></span> 5% threshold</span>' : ''}` }
function forecastRows(F, mode) {
  const ps = F.parties.slice().sort(mode === 'vote' ? (a, b) => b.forecast_vote_mean - a.forecast_vote_mean : (a, b) => (b.seats_expected || 0) - (a.seats_expected || 0));
  const get = x => mode === 'vote' ? [x.forecast_vote_80[0], x.forecast_vote_80[1], x.forecast_vote_mean] : [(x.seats_80 || [0, 0])[0], (x.seats_80 || [0, 0])[1], x.seats_expected || 0];
  const max = mode === 'vote' ? Math.max(45, Math.ceil(Math.max(...ps.map(x => get(x)[1])) / 5) * 5) : Math.max(50, Math.ceil(Math.max(...ps.map(x => get(x)[1])) / 10) * 10);
  const pc = v => (Math.max(0, Math.min(max, v)) / max * 100).toFixed(1) + '%';
  return `<p class="micro muted">Scale 0–${max}${mode === 'vote' ? '% of the party vote' : ' seats'}, the same for every party.</p>` + ps.map(x => { const [lo, hi, m] = get(x); const u = mode === 'vote' ? '%' : '';
    const loS = mode === 'vote' ? Math.max(0, Math.round(lo)) : lo, hiS = mode === 'vote' ? Math.round(hi) : hi, mS = mode === 'vote' ? fmt(m) : m;
    const sub = mode === 'vote' ? (x.p_over_5pct != null && x.p_over_5pct < 99 ? `clears 5% in ${inHundred(x.p_over_5pct)}` : '') : (x.p_in_parliament != null && x.p_in_parliament < 99 ? `in Parliament in ${inHundred(x.p_in_parliament)}` : '');
    return `<div class="rrow" style="--pc:${pcolor(x.party)}"><span class="stack stack--s" style="gap:2px">${ptagHTML(x.party)}${sub ? `<span class="micro muted">${sub}</span>` : ''}</span>
      <div class="rbar" style="--lo:${pc(lo)};--hi:${pc(hi)};--m:${pc(m)}${mode === 'vote' ? `;--x:${pc(5)}` : ''}" role="img" aria-label="${esc(pname(x.party))}: likely ${loS} to ${hiS}${u}, middle estimate ${mS}${u}">${mode === 'vote' ? '<span class="rbar__mark"></span>' : ''}<span class="rbar__band"></span><span class="rbar__mean"></span></div>
      <span class="rrow__v"><b>${loS}–${hiS}${u}</b><span>middle ${mS}${u}</span></span></div>` }).join('') }
function pollAverageBlock(pr) { const ps = Object.entries(pr.pct).sort((a, b) => b[1] - a[1]).filter(([, v]) => v >= 0.8);
  return `<section class="stack" aria-labelledby="h-pa"><div class="shead"><div class="shead__row"><h2 id="h-pa">Poll of polls</h2><span class="small muted">average of the ${pr.n} latest polls (${esc(pr.range)})</span></div></div>
    <div>${ps.map(([p, v], k) => `<div class="rrow" style="--pc:${pcolor(p)}">${ptagHTML(p)}<div class="bar"><i style="--w:${v / 50 * 100}%;--i:${k}"></i></div><span class="rrow__v"><b>${fmt(v)}%</b></span></div>`).join('')}</div>
    <p class="micro muted">Sorted by poll average: the only page in the guide sorted this way. A full forecast with ranges will appear here.</p></section>` }
function unknownsBlock(F, title = 'How this could be wrong') {
  const items = (F.caveats || []).map(c => { const m = String(c).match(/^([^:]{3,60}):\s*(.+)$/); return m ? `<li><b>${esc(m[1])}:</b> ${esc(m[2])}</li>` : `<li>${esc(c)}</li>` });
  return `<section class="unknowns" aria-labelledby="h-unk"><h2 id="h-unk" class="h3">${esc(title)}</h2><ul>${items.join('')}</ul>
    <p class="small soft">It also can't know turnout under this year's earlier enrolment deadline, or how special votes will move things after election night.</p></section>` }
function trackRecordBlock(F) {
  const TR = F.historical_track_record || {}, els = TR.elections || [];
  if (!els.length) return '<div></div>';
  const misses = els.flatMap(e => (e.parties || []).filter(p => p.inside80 === false).map(p => ({ year: e.election, ...p })));
  const [hit, tot] = String(TR.coverage80 || '').split('/');
  return `<section class="stack" aria-labelledby="h-bt"><h2 id="h-bt" class="h3">Our track record, misses included</h2>
    <p class="soft">Run two weeks before each election since ${esc(els[0].election)}, the "8 in 10" range caught <b style="color:var(--text)">${esc(hit)} of ${esc(tot)}</b> party results. It missed these:</p>
    ${twrap('Forecast misses', `<table class="table"><caption class="sr-only">Party results that fell outside the 8 in 10 range, two weeks out</caption><thead><tr><th scope="col">Year</th><th scope="col">Party</th><th class="n" scope="col">Forecast</th><th class="n" scope="col">Result</th><th class="n" scope="col">Miss, points</th></tr></thead><tbody>
    ${misses.map(m => `<tr><td class="num">${esc(m.year)}</td><td>${ptagHTML(m.party)}</td><td class="n">${fmt(m.forecast_2wk_out)}%</td><td class="n">${fmt(m.result)}%</td><td class="n"><b>${m.error_result_minus_forecast > 0 ? '+' : ''}${fmt(m.error_result_minus_forecast)}</b></td></tr>`).join('')}</tbody></table>`)}
    <details class="disclose"><summary>Every election, and the "19 in 20" range</summary><div class="disclose__body">
      ${twrap('Track record by election', `<table class="table"><thead><tr><th scope="col">Election</th><th class="n" scope="col">Polls used</th><th class="n" scope="col">Inside 8 in 10</th><th class="n" scope="col">Inside 19 in 20</th></tr></thead><tbody>${els.map(t => `<tr><td class="num">${esc(t.election)}</td><td class="n">${t.n_polls_used_120d ?? '–'}</td><td class="n">${esc(t.coverage80 || '')}</td><td class="n">${esc(t.coverage95 || '')}</td></tr>`).join('')}</tbody></table>`)}
      <p class="small">${esc(TR.note || '')} Overall: ${esc(TR.coverage80 || '')} of results fell inside the 80% range and ${esc(TR.coverage95 || '')} inside the 95% range.</p></div></details></section>` }
function houseEffectsBlock(F) { const P7 = F.parties.slice().sort((a, b) => b.forecast_vote_mean - a.forecast_vote_mean);
  return `<details class="disclose"><summary>How each pollster leans compared with the others</summary><div class="disclose__body">${twrap('How each pollster leans', `<table class="table"><thead><tr><th scope="col">Pollster</th><th class="n" scope="col">Polls</th>${P7.map(x => `<th class="n" scope="col"><abbr title="${esc(pname(x.party))}">${esc(PARTY_ABBR[x.party] || pname(x.party))}</abbr></th>`).join('')}</tr></thead><tbody>${F.pollsters.filter(q => q.n_polls_this_term).map(q => `<tr><td>${esc(q.pollster)}${q.internal ? ' <span class="badge badge--outline">Party-commissioned, half weight</span>' : ''}</td><td class="n">${q.n_polls_this_term}</td>${P7.map(x => { const v = (q.house_effects || {})[x.party]; return `<td class="n">${v == null ? '–' : (v > 0 ? '+' : '') + fmt(v)}</td>` }).join('')}</tr>`).join('')}</tbody></table>`)}<p class="small">${esc(F.house_effects_note || '')}</p></div></details>` }
function maoriSeatsBlock(F) {
  const E = F.electorates || {}, M = E.maori_seats || {}; if (!Object.keys(M).length) return '';
  const rows = Object.entries(M).sort((a, b) => a[0].localeCompare(b[0], 'en-NZ')).map(([seat, m]) => { const w = Object.entries(m.p_win || {}).map(([p, v]) => [pollKey(p), v]).sort((a, b) => b[1] - a[1]);
    const el = (S.data.electorates || []).find(x => slugify(x.name) === slugify(seat) || x.slug === slugify(seat));
    return `<tr><th scope="row">${el ? `<a href="#/vote/electorate/${esc(el.slug)}"><b>${esc(seat)}</b></a>` : `<b>${esc(seat)}</b>`}</th><td>${w[0] ? ptagHTML(w[0][0]) : '–'}</td><td class="n">${w[0] ? inHundred(w[0][1]) : '–'}</td><td>${w.slice(1).filter(([, v]) => v >= 1).map(([p, v]) => `${esc(pname(p))} ${Math.round(v)}`).join(' · ') || '–'}</td><td class="small">${(m.polls_used || []).length ? m.polls_used.map(x => `${x.source_url ? `<a href="${esc(x.source_url)}" target="_blank" rel="noopener">${esc(x.pollster || 'poll')}</a>` : esc(x.pollster || 'poll')}, ${esc(x.date || '')}${x.sample_size ? ` (sample ${Number(x.sample_size).toLocaleString('en-NZ')})` : ''}`).join('<br>') : '<span class="muted">none: 2023 result only</span>'}</td></tr>` });
  return `<section class="stack" aria-labelledby="h-maori"><div class="shead"><div class="shead__row"><h2 id="h-maori">The seven Māori seats, and Epsom</h2><span class="badge badge--outline">Low confidence</span></div>
      <p class="small soft">Chance each candidate's party wins the seat. These rest on very few small electorate polls and the 2023 result, so treat them as rough.</p></div>
    ${twrap('Māori seats and Epsom', `<table class="table"><thead><tr><th scope="col">Electorate</th><th scope="col">Most likely</th><th class="n" scope="col">Chance</th><th scope="col">Others (in 100)</th><th scope="col">Electorate polls</th></tr></thead><tbody>${rows.join('')}
      ${E.epsom ? `<tr><th scope="row"><a href="#/vote/electorate/epsom"><b>Epsom</b></a></th><td>${ptagHTML('act')}</td><td class="n">${inHundred(E.epsom.p_act_wins)}</td><td>–</td><td><span class="muted">none: stated assumption</span></td></tr>` : ''}</tbody></table>`)}
    ${E.epsom && E.epsom.assumption ? `<p class="small soft"><b>Epsom:</b> ${esc(E.epsom.assumption)}</p>` : ''}
    ${E.note ? `<p class="micro muted">${esc(E.note)}</p>` : ''}</section>` }

/* ----- trend chart: a 360-wide lines-only SVG for phones and a 900-wide one with dots; CSS shows one ----- */
function pollChart(polls, parties, { long = false } = {}) {
  const label = long ? 'Party vote at each election since 2008, then every published poll since 2023 with an 8-poll rolling average' : 'Party vote in every published poll since the 2023 election, with an 8-poll rolling average';
  return trendSVG(polls, parties, 360, 300, false, long, label) + trendSVG(polls, parties, 900, 340, true, long, label) +
    `<figcaption class="micro muted">Lines: average of each party's last 8 polls${long ? '; solid dots joined by a dashed line: election results' : ''}. Dots (on wider screens): individual polls. Same 0–${long ? 55 : 45}% scale for every party. Every poll in this chart is also in <a href="#/seats/polls/all">the table of every poll</a>.</figcaption>` }
function trendSVG(polls, parties, W, H, dots, long, label) {
  const L = W < 500 ? 30 : 34, R = W < 500 ? 36 : 44, T = 12, B = 24;
  const t0 = new Date(long ? '2008-06-01' : '2023-10-01').getTime(), t1 = new Date(long ? '2026-12-15' : '2026-11-14').getTime(), maxV = long ? 55 : 45;
  const xs = d => L + (new Date(d).getTime() - t0) / (t1 - t0) * (W - L - R), ys = v => T + (1 - v / maxV) * (H - T - B);
  const ticks = long ? [0, 10, 20, 30, 40, 50] : [0, 10, 20, 30, 40];
  let g = `<g class="grid">${ticks.map(v => `<line x1="${L}" x2="${W - R}" y1="${ys(v).toFixed(1)}" y2="${ys(v).toFixed(1)}"/>`).join('')}</g>` + ticks.map((v, k) => `<text x="${L - 6}" y="${(ys(v) + 4).toFixed(1)}" text-anchor="end">${v}${k === ticks.length - 1 ? '%' : ''}</text>`).join('');
  const years = long ? (W < 500 ? [2011, 2017, 2023] : [2008, 2011, 2014, 2017, 2020, 2023]) : [2024, 2025, 2026];
  g += years.map(y => `<text x="${xs(long ? y + '-11-01' : y + '-01-01').toFixed(1)}" y="${H - 6}" text-anchor="middle">${y}</text>`).join('');
  g += `<line class="thr" x1="${L}" x2="${W - R}" y1="${ys(5).toFixed(1)}" y2="${ys(5).toFixed(1)}"/><text class="thr-l" x="${xs(long ? '2009-06-01' : '2023-12-15').toFixed(1)}" y="${(ys(5) - 5).toFixed(1)}">5% threshold</text>`;
  g += `<line class="eday" x1="${xs('2026-11-07').toFixed(1)}" x2="${xs('2026-11-07').toFixed(1)}" y1="${T}" y2="${H - B}"/><text class="eday-l" x="${(xs('2026-11-07') - 4).toFixed(1)}" y="${T + 10}" text-anchor="end">7 Nov</text>`;
  const sorted = polls.slice().sort((a, b) => a.date.localeCompare(b.date));
  const els = (S.data.elections || []).filter(e => e.year >= (long ? 2008 : 2023) && e.year < 2026);
  const ends = [];
  for (const p of parties) { const pc = pcolor(p); const pp = sorted.filter(x => typeof x.parties[p] === 'number');
    let part = '';
    const res = els.map(e => { const r = (e.parties || []).find(x => x.party === p); return r && r.party_vote_pct != null ? [e.date || e.year + '-11-01', r.party_vote_pct, e.year] : null }).filter(Boolean);
    // every party line is drawn over a 1px --ring underlay, so black and yellow lines read on either theme
    if (long && res.length > 1) { const pts = res.map(([d, v]) => `${xs(d).toFixed(1)},${ys(v).toFixed(1)}`).join(' '); part += `<polyline class="elx elx--ring" points="${pts}"/><polyline class="elx" points="${pts}"/>` }
    part += res.map(([d, v, y]) => `<circle class="res" cx="${xs(d).toFixed(1)}" cy="${ys(v).toFixed(1)}" r="${W < 500 ? 3.5 : 4.5}" data-tip="${y} election result · ${esc(pname(p))} ${fmt(v, 2)}%"></circle>`).join('');
    if (dots) part += pp.map(x => `<circle class="dot" cx="${xs(x.date).toFixed(1)}" cy="${ys(x.parties[p]).toFixed(1)}" r="3" data-tip="${esc(x.pollster)} · ${esc(seatDate(x.date))} · ${esc(pname(p))} ${fmt(x.parties[p])}%${x.sample_size ? ' · sample ' + Number(x.sample_size).toLocaleString('en-NZ') : ''}"></circle>`).join('');
    if (pp.length > 3) { const avg = pp.map((x, i) => { const w = pp.slice(Math.max(0, i - 7), i + 1); return [x.date, w.reduce((a, y) => a + y.parties[p], 0) / w.length] });
      const xy = avg.map(([d, v]) => [xs(d), ys(v)]); let len = 0; for (let k = 1; k < xy.length; k++) len += Math.hypot(xy[k][0] - xy[k - 1][0], xy[k][1] - xy[k - 1][1]);
      const pts = xy.map(([a, b]) => `${a.toFixed(1)},${b.toFixed(1)}`).join(' ');
      part += `<polyline class="avg avg--ring" style="--len:${Math.ceil(len)}" points="${pts}"/><polyline class="avg" style="--len:${Math.ceil(len)}" points="${pts}"/>`;
      const [ld, lv] = avg[avg.length - 1]; ends.push({ x: xs(ld) + 5, y: ys(lv) + 4, v: lv, p }) }
    g += `<g style="--pc:${pc}">${part}</g>` }
  // end labels, nudged apart so they don't overlap
  ends.sort((a, b) => a.y - b.y); for (let k = 1; k < ends.length; k++) if (ends[k].y - ends[k - 1].y < 12) ends[k].y = ends[k - 1].y + 12;
  g += ends.map(e => `<text class="end" x="${e.x.toFixed(1)}" y="${e.y.toFixed(1)}">${Math.round(e.v)}</text>`).join('');
  return `<svg class="chart ${dots ? 'chart--wide' : 'chart--narrow'}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(label)}">${g}</svg>` }
// Seats after each election (stacked, 61 tick) and turnout vs wasted vote, since 2008 (from the old Parliament › trends tab)
function pastElectionsCharts() {
  const els = (S.data.elections || []).filter(e => e.year >= 2008 && e.year < 2026);
  const W = 520, bh = 24, gap = 10, H = els.length * (bh + gap), x0 = 48, sc = (W - x0 - 8) / 125;
  const seats = `<svg class="chart chart--past" viewBox="0 0 ${W} ${H}" role="img" aria-label="Seats won by each party at each election since 2008">${els.map((e, i) => { let x = x0; const y = i * (bh + gap); const tot = (e.parties || []).reduce((a, r) => a + (r.total_seats || 0), 0) || 120;
    const segs = (e.parties || []).filter(r => r.total_seats).sort((a, b) => P(a.party).order - P(b.party).order).map(r => { const w = r.total_seats * sc; const s = `<rect class="stk" x="${x.toFixed(1)}" y="${y}" width="${w.toFixed(1)}" height="${bh}" style="--pc:${pcolor(r.party)}" data-tip="${e.year}: ${esc(pname(r.party))} ${r.total_seats} seats"><title>${esc(pname(r.party))} ${r.total_seats}</title></rect>`; x += w; return s }).join('');
    const mx = x0 + (Math.floor(tot / 2) + 1) * sc; return `<text x="0" y="${y + 17}">${e.year}</text>${segs}<line class="majtick" x1="${mx.toFixed(1)}" x2="${mx.toFixed(1)}" y1="${y - 3}" y2="${y + bh + 3}"/>` }).join('')}</svg>`;
  const tw = 520, th = 210, pad = 36, xs = i => pad + 16 + i * (tw - pad - 40) / Math.max(1, els.length - 1), ys = v => th - 26 - v / 100 * (th - 44);
  const waste = els.map(e => e.wasted_party_vote_pct != null ? e.wasted_party_vote_pct : (e.parties || []).filter(r => !r.total_seats).reduce((a, r) => a + (r.party_vote_pct || 0), 0));
  const turn = `<svg class="chart chart--past" viewBox="0 0 ${tw} ${th}" role="img" aria-label="Turnout and wasted party vote at each election since 2008"><g class="grid">${[0, 25, 50, 75, 100].map(v => `<line x1="${pad}" x2="${tw - 10}" y1="${ys(v)}" y2="${ys(v)}"/>`).join('')}</g>${[0, 25, 50, 75, 100].map(v => `<text x="${pad - 6}" y="${ys(v) + 4}" text-anchor="end">${v}%</text>`).join('')}
    ${els.map((e, i) => `<rect class="waste" x="${xs(i) - 12}" y="${ys(waste[i])}" width="24" height="${Math.max(0, ys(0) - ys(waste[i]))}" rx="3" data-tip="${e.year}: wasted party vote ${fmt(waste[i])}%"></rect><text x="${xs(i)}" y="${th - 8}" text-anchor="middle">${e.year}</text>`).join('')}
    <polyline class="turn" points="${els.map((e, i) => `${xs(i)},${ys(e.turnout_pct || 0)}`).join(' ')}"/>${els.map((e, i) => `<circle class="turn-pt" cx="${xs(i)}" cy="${ys(e.turnout_pct || 0)}" r="5" data-tip="${e.year}: turnout ${fmt(e.turnout_pct)}%"></circle>`).join('')}</svg>`;
  const ps = [...new Set(els.flatMap(e => (e.parties || []).filter(r => r.total_seats).map(r => r.party)))].sort(byShort);
  const tbl = twrap('Past elections in numbers', `<table class="table"><caption class="sr-only">Turnout, wasted party vote and seats won at each election since 2008, parties A to Z</caption><thead><tr><th scope="col">Election</th><th class="n" scope="col">Turnout</th><th class="n" scope="col">Wasted vote</th>${ps.map(p => `<th class="n" scope="col"><abbr title="${esc(pname(p))}">${esc(PARTY_ABBR[p] || pname(p))}</abbr></th>`).join('')}</tr></thead><tbody>${els.map((e, i) => `<tr><th scope="row">${e.year}</th><td class="n">${e.turnout_pct != null ? fmt(e.turnout_pct) + '%' : '–'}</td><td class="n">${fmt(waste[i])}%</td>${ps.map(p => { const r = (e.parties || []).find(x => x.party === p); return `<td class="n">${r && r.total_seats ? r.total_seats : '–'}</td>` }).join('')}</tr>`).join('')}</tbody></table>`);
  return `<div class="cols cols--2"><figure class="stack stack--s"><h3 class="h4">Seats after each election</h3>${seats}<figcaption class="micro muted">One bar per election, one block per party (named on hover and in the table below). The black tick marks the seats needed to govern. Parties left to right as they usually sit.</figcaption></figure>
    <figure class="stack stack--s"><h3 class="h4">Turnout and wasted vote</h3>${turn}<figcaption class="micro muted">Line: turnout of enrolled voters. Bars: "wasted" party vote, for parties that won no seats.</figcaption></figure></div>
    <p class="srcline" id="ppast-tip" aria-live="polite">Tap a bar or point for its number. Source: official results, Electoral Commission.</p>
    <details class="disclose"><summary>The same numbers in a table</summary><div class="disclose__body">${tbl}</div></details>` }
