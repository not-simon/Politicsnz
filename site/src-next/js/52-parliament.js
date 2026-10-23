/* ----- parliament explorer: chamber / trends / coalitions / calculator ----- */
V.parliament = (sub = 'chamber') => {
  $('#main').innerHTML = `<section class="view"><div class="stack"><div class="kicker">The House of Representatives</div><h2>Explore Parliament</h2></div>
    <div class="tabs" id="ptab">${[['chamber', 'Seat map'], ['trends', 'Polls & trends'], ['coalition', 'Coalition builder'], ['calculator', 'Seat calculator']].map(([k, l]) => `<button data-s="${k}" aria-selected="${k === sub}">${l}</button>`).join('')}</div><div id="pv"></div></section>`;
  const go = s => { $('#ptab').querySelectorAll('button').forEach(b => b.setAttribute('aria-selected', b.dataset.s === s)); SUB[s]($('#pv')) };
  $('#ptab').onclick = e => { const b = e.target.closest('[data-s]'); if (b) go(b.dataset.s) };
  go(sub);
};
const SUB = {};
SUB.chamber = el => {
  const parls = S.data.parliaments, els = S.data.elections;
  const steps = parls.map(p => ({ key: `p${p.parliament}`, label: String(p.election_year), parl: p })); steps.push({ key: 'proj', label: '2026', proj: true });
  let i = Math.max(0, steps.findIndex(x => x.key === (store.get('chamberSel') || `p${parls[parls.length - 1].parliament}`))); let mode = 'start'; let playing = null;
  el.innerHTML = `<div class="stack" style="gap:16px"><p class="lede">Every seat in every Parliament since 2011. Drag the slider or press play to watch the House change; tap a seat to see who held it.</p>
    <div class="card scrubber"><button class="playbtn" id="cplay" aria-label="Play through the Parliaments">${ic('play', 22)}</button><div><input type="range" id="cyear" min="0" max="${steps.length - 1}" step="1" value="${i}" aria-label="Parliament"><div class="years">${steps.map((x, k) => `<span data-k="${k}" title="${x.proj ? 'Projection from the polls' : x.label + ' election'}">${x.label}${x.proj ? '*' : ''}</span>`).join('')}</div></div></div>
    <div class="row" style="justify-content:space-between"><span class="seg" id="modewrap"><button id="m-start" aria-pressed="true">After the election</button><button id="m-now" aria-pressed="false">End of term / today</button></span><div class="legend" id="legend"></div></div>
    <div class="split"><div class="card chamber"><div id="hemi"></div><div id="ctitle" class="row" style="justify-content:space-between;margin-top:6px"></div></div>
      <div class="card stack"><div id="seatinfo" class="seatcard muted small">Tap any seat to see who sat there.</div><hr class="soft"><div id="ctx" class="stack"></div></div></div>
    <div class="card scroll anim" id="results"></div></div>`;
  const draw = () => { const st = steps[i]; store.set('chamberSel', st.key); let seats, ctx = '', res = '';
    if (st.proj) { const pr = projection(); seats = seatsFromComposition(pr.seats, []); $('#modewrap').hidden = true;
      ctx = `<h4>2026: projection from the polls</h4><p class="small">Average of the ${pr.n} latest polls (${esc(pr.range)}), turned into seats with the Sainte-Laguë formula. Assumed electorate wins: ${esc(Object.entries(pr.elec).map(([p, n]) => pname(p) + ' ' + n).join(', ') || 'none')}. An illustration, not a forecast — see <button class="btn ghost sm" data-go="polls">Polls & forecast</button>.</p>`;
      res = `<h3>Poll average</h3><table><thead><tr><th>Party</th><th class="n">Poll %</th><th class="n">Seats</th></tr></thead><tbody>${Object.entries(pr.pct).sort((a, b) => b[1] - a[1]).map(([p, x]) => `<tr><td><span class="row" style="gap:6px"><span class="dot" style="background:${pcolor(p)}"></span>${esc(pname(p))}</span></td><td class="n">${fmt(x)}</td><td class="n">${pr.seats[p] || 0}</td></tr>`).join('')}</tbody></table>`;
    } else { $('#modewrap').hidden = false; const parl = st.parl; seats = parliamentSeats(parl, mode);
      const e = els.find(x => x.year === parl.election_year); const g = e && e.government;
      ctx = `<div class="kicker">${ordinal(parl.parliament)} Parliament · ${esc(parl.start || '')} to ${esc(parl.end || 'today')}</div>
        ${g ? `<p class="small"><b>Government:</b> ${esc(g.pm || '')}, ${esc((g.parties || []).map(pname).join(' + '))} (${esc(g.arrangement || '')})${(g.support || []).length ? ', with support from ' + esc(g.support.map(pname).join(', ')) : ''}.</p>${g.notes ? `<p class="small muted">${esc(g.notes)}</p>` : ''}` : ''}
        ${(parl.changes || []).length ? `<details><summary class="small" style="cursor:pointer;color:var(--primary);font-weight:700">${parl.changes.length} changes during the term</summary><ul class="small">${parl.changes.map(c => `<li><span class="num">${esc(c.date)}</span> ${esc(c.description)}</li>`).join('')}</ul></details>` : ''}`;
      if (e) res = electionTable(e) }
    S.curSeats = seats; chamberUpdate($('#hemi'), seats, { label: 'Seat map' });
    $('#ctitle').innerHTML = `<b style="font:800 20px var(--font-display)">${esc(st.label)}${st.proj ? ' · poll projection' : ' election'}</b><span class="tiny muted">${seats.length} seats · ${Math.floor(seats.length / 2) + 1} to govern</span>`;
    const counts = {}; seats.forEach(s => counts[s.party] = (counts[s.party] || 0) + 1);
    $('#legend').innerHTML = Object.entries(counts).sort((a, b) => P(a[0]).order - P(b[0]).order).map(([p, n]) => `<span class="item"><span class="dot" style="background:${pcolor(p)}"></span>${esc(pname(p))} <b class="num">${n}</b></span>`).join('');
    $('#ctx').innerHTML = ctx; const r = $('#results'); r.innerHTML = res || '<p class="empty">No results table for this view.</p>'; r.classList.remove('anim'); void r.offsetWidth; r.classList.add('anim');
    $('#cyear').value = i; el.querySelectorAll('.years span').forEach(x => x.classList.toggle('on', +x.dataset.k === i)) };
  $('#cyear').oninput = () => { i = +$('#cyear').value; draw() };
  el.querySelector('.years').onclick = e => { const sp = e.target.closest('[data-k]'); if (sp) { i = +sp.dataset.k; draw() } };
  $('#cplay').onclick = () => { if (playing) { clearInterval(playing); playing = null; $('#cplay').innerHTML = ic('play', 22); return }
    $('#cplay').innerHTML = ic('pause', 22); i = 0; draw(); playing = setInterval(() => { if (i >= steps.length - 1) { clearInterval(playing); playing = null; $('#cplay').innerHTML = ic('play', 22); return } i++; draw() }, 1600) };
  $('#m-start').onclick = () => { mode = 'start'; $('#m-start').setAttribute('aria-pressed', 'true'); $('#m-now').setAttribute('aria-pressed', 'false'); draw() };
  $('#m-now').onclick = () => { mode = 'now'; $('#m-now').setAttribute('aria-pressed', 'true'); $('#m-start').setAttribute('aria-pressed', 'false'); draw() };
  const showSeat = e => { const c = e.target.closest('.seat'); if (c) seatInfo(S.curSeats[+c.dataset.i]) };
  $('#hemi').addEventListener('click', showSeat); $('#hemi').addEventListener('keydown', e => { if (e.key === 'Enter') showSeat(e) });
  draw();
};
async function seatInfo(s) { const box = $('#seatinfo'); box.className = 'seatcard';
  if (!s.name) { box.innerHTML = `<span class="dot" style="background:${pcolor(s.party)}"></span> ${esc(pname(s.party))} seat`; return }
  await loadPeople(); const person = findPerson(s.slug, s.name);
  box.innerHTML = `${faceHTML(person || { name: s.name }, s.party)}<div><div style="font-weight:700">${esc(s.name)}</div><div class="small muted">${esc(pname(s.party))} · ${esc(s.type === 'list' ? 'List MP' : (s.seat || ''))}${s.left ? ' · left ' + esc(s.left) : ''}</div>
    ${s.notes ? `<div class="tiny muted">${esc(s.notes)}</div>` : ''}${person ? `<button class="btn sm" style="margin-top:6px" id="seatprof">Profile</button>` : ''}</div>`;
  const b = $('#seatprof'); if (b) b.onclick = () => openPerson(person) }
function electionTable(el) {
  const rows = (el.parties || []).slice().sort((a, b) => (b.party_vote_pct || 0) - (a.party_vote_pct || 0));
  return `<div class="row" style="justify-content:space-between"><h3>${el.year} general election</h3><span class="small muted">${esc(el.date || '')} · turnout <span class="num">${fmt(el.turnout_pct)}%</span>${el.overhang ? ` · overhang ${el.overhang}` : ''}</span></div>
  <table><thead><tr><th>Party</th><th class="n">Party vote</th><th class="n">Votes</th><th class="n">Electorate</th><th class="n">List</th><th class="n">Seats</th></tr></thead><tbody>
  ${rows.map(r => `<tr><td><span class="row" style="gap:6px;flex-wrap:nowrap"><span class="dot" style="background:${pcolor(r.party)}"></span>${esc(r.name || pname(r.party))}</span></td><td class="n">${fmt(r.party_vote_pct, 2)}%</td><td class="n">${r.party_votes ? Number(r.party_votes).toLocaleString('en-NZ') : '–'}</td><td class="n">${r.electorate_seats ?? 0}</td><td class="n">${r.list_seats ?? 0}</td><td class="n"><b>${r.total_seats ?? 0}</b></td></tr>`).join('')}
  </tbody></table><p class="small" style="margin-top:10px"><button class="btn sm" data-page="elections/${el.year}.md">Read the story of the ${el.year} election</button></p>` }
SUB.trends = el => {
  const els = S.data.elections.filter(e => e.year >= 2008);
  const main = ['national', 'labour', 'green', 'act', 'nz-first', 'te-pati-maori', 'opportunity', 'conservative', 'united-future', 'mana', 'internet-mana'];
  el.innerHTML = `<div class="stack" style="gap:16px"><p class="lede">Party vote at each election since 2008, then every published poll since the 2023 election. Tap a point for its number.</p>
    <div class="card chart stack"><div class="chips" id="tchips"></div><div id="tchart"></div><div class="tip" id="ttip">Tap a point.</div></div>
    <div class="split"><div class="card chart stack"><h3>Seats after each election</h3><div id="seatbars"></div></div>
      <div class="card chart stack"><h3>Turnout and wasted vote</h3><p class="small muted">"Wasted" vote is the party vote for parties that won no seats.</p><div id="turn"></div></div></div></div>`;
  const present = main.filter(p => els.some(e => (e.parties || []).some(r => r.party === p && r.party_vote_pct >= 1)) || (S.data.polls || []).some(x => x.parties && x.parties[p] >= 1));
  const on = new Set(present.slice(0, 6));
  const draw = () => { $('#tchips').innerHTML = present.map(p => `<button class="chip" data-p="${p}" aria-pressed="${on.has(p)}"><span class="dot" style="background:${pcolor(p)}"></span>${esc(pname(p))}</button>`).join(''); $('#tchart').innerHTML = lineChart(els, S.data.polls || [], [...on], $('#tchart').clientWidth || 760) };
  $('#tchips').onclick = e => { const b = e.target.closest('[data-p]'); if (!b) return; on.has(b.dataset.p) ? on.delete(b.dataset.p) : on.add(b.dataset.p); draw() };
  el.addEventListener('click', e => { const c = e.target.closest('[data-tip]'); if (c) $('#ttip').textContent = c.dataset.tip });
  draw();
  const W = 520, bh = 26, gap = 10, H = els.length * (bh + gap) + 20;
  $('#seatbars').innerHTML = `<svg viewBox="0 0 ${W} ${H}">${els.map((e, i) => { let x = 46; const tot = (e.parties || []).reduce((a, r) => a + (r.total_seats || 0), 0) || 120; const sc = (W - 56) / 125;
    const segs = (e.parties || []).filter(r => r.total_seats).sort((a, b) => P(a.party).order - P(b.party).order).map(r => { const w = r.total_seats * sc; const s = `<rect x="${x.toFixed(1)}" y="${i * (bh + gap)}" width="${w.toFixed(1)}" height="${bh}" fill="${pcolor(r.party)}" data-tip="${e.year}: ${esc(pname(r.party))} ${r.total_seats} seats"></rect>`; x += w; return s }).join('');
    const mx = 46 + (Math.floor(tot / 2) + 1) * sc; return `<text x="0" y="${i * (bh + gap) + 17}">${e.year}</text>${segs}<line x1="${mx}" x2="${mx}" y1="${i * (bh + gap) - 3}" y2="${i * (bh + gap) + bh + 3}" stroke="var(--text)" stroke-width="2"/>` }).join('')}<text x="46" y="${H - 2}">black tick = seats needed to govern</text></svg>`;
  const tw = 520, th = 200, pad = 34, xs = i => pad + 12 + i * (tw - pad - 34) / Math.max(1, els.length - 1), ys = v => th - 24 - v / 100 * (th - 40);
  const waste = els.map(e => (e.parties || []).filter(r => !r.total_seats).reduce((a, r) => a + (r.party_vote_pct || 0), 0));
  $('#turn').innerHTML = `<svg viewBox="0 0 ${tw} ${th}">${[0, 25, 50, 75, 100].map(v => `<line class="grid-l" x1="${pad}" x2="${tw - 10}" y1="${ys(v)}" y2="${ys(v)}"/><text x="0" y="${ys(v) + 4}">${v}%</text>`).join('')}
    ${els.map((e, i) => `<rect x="${xs(i) - 12}" y="${ys(waste[i])}" width="24" height="${Math.max(0, ys(0) - ys(waste[i]))}" rx="4" fill="var(--v-partially-kept)" data-tip="${e.year}: wasted vote ${fmt(waste[i])}%"></rect><text x="${xs(i)}" y="${th - 6}" text-anchor="middle">${e.year}</text>`).join('')}
    <polyline fill="none" stroke="var(--primary)" stroke-width="3" stroke-linejoin="round" points="${els.map((e, i) => `${xs(i)},${ys(e.turnout_pct || 0)}`).join(' ')}"/>
    ${els.map((e, i) => `<circle cx="${xs(i)}" cy="${ys(e.turnout_pct || 0)}" r="5" fill="var(--primary)" stroke="var(--surface)" stroke-width="2" data-tip="${e.year}: turnout ${fmt(e.turnout_pct)}%"></circle>`).join('')}</svg>`;
};
function lineChart(els, polls, parties, cw = 760) {
  const W = Math.max(440, Math.min(760, Math.round(cw * 1.25))), H = 330, L = 36, R = 34, T = 10, B = 26, t0 = new Date('2008-06-01').getTime(), t1 = new Date('2026-12-01').getTime();
  const xs = d => L + (new Date(d).getTime() - t0) / (t1 - t0) * (W - L - R), ys = v => T + (1 - v / 55) * (H - T - B);
  let g = [0, 10, 20, 30, 40, 50].map(v => `<line class="grid-l" x1="${L}" x2="${W - R}" y1="${ys(v)}" y2="${ys(v)}"/><text x="4" y="${ys(v) + 4}">${v}%</text>`).join('');
  g += els.map(e => `<text x="${xs(e.date || e.year + '-11-01')}" y="${H - 6}" text-anchor="middle">${e.year}</text>`).join('') + `<text x="${xs('2026-11-07')}" y="${H - 6}" text-anchor="middle" style="fill:var(--primary);font-weight:700">2026</text>`;
  g += `<line x1="${xs('2026-11-07')}" x2="${xs('2026-11-07')}" y1="${T}" y2="${H - B}" stroke="var(--primary)" stroke-dasharray="3 3"/><line x1="${L}" x2="${W - R}" y1="${ys(5)}" y2="${ys(5)}" stroke="var(--text-2)" stroke-dasharray="2 4"/><text x="${L + 4}" y="${ys(5) - 4}">5% threshold</text>`;
  const sorted = polls.filter(p => p.date && p.parties).sort((a, b) => a.date.localeCompare(b.date));
  for (const p of parties) { const c = pcolor(p);
    const pts = els.map(e => { const r = (e.parties || []).find(x => x.party === p); return r ? [e.date || e.year + '-11-01', r.party_vote_pct, e.year] : null }).filter(Boolean);
    if (pts.length > 1) g += `<polyline fill="none" stroke="${c}" stroke-width="3" stroke-linejoin="round" points="${pts.map(([d, v]) => `${xs(d).toFixed(1)},${ys(v).toFixed(1)}`).join(' ')}"/>`;
    g += pts.map(([d, v, y]) => `<circle cx="${xs(d).toFixed(1)}" cy="${ys(v).toFixed(1)}" r="5" fill="${c}" stroke="var(--surface)" stroke-width="2" data-tip="${y} election · ${esc(pname(p))} ${fmt(v, 2)}%"></circle>`).join('');
    const pp = sorted.filter(x => typeof x.parties[p] === 'number');
    g += pp.map(x => `<circle cx="${xs(x.date).toFixed(1)}" cy="${ys(x.parties[p]).toFixed(1)}" r="2.2" fill="${c}" opacity=".4" data-tip="${esc(x.date)} ${esc(x.pollster || '')} · ${esc(pname(p))} ${fmt(x.parties[p])}%"></circle>`).join('');
    if (pp.length > 4) { const avg = pp.map((x, i) => { const w = pp.slice(Math.max(0, i - 7), i + 1); return [x.date, w.reduce((a, y) => a + y.parties[p], 0) / w.length] });
      g += `<polyline fill="none" stroke="${c}" stroke-width="2.4" points="${avg.map(([d, v]) => `${xs(d).toFixed(1)},${ys(v).toFixed(1)}`).join(' ')}"/>`;
      const [ld, lv] = avg[avg.length - 1]; g += `<text x="${(xs(ld) + 6).toFixed(1)}" y="${(ys(lv) + 4).toFixed(1)}" style="fill:${c};font-weight:700">${fmt(lv)}</text>` } }
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Party vote share over time">${g}</svg>` }
SUB.coalition = el => {
  const els = S.data.elections; const srcs = [['proj', '2026 poll projection'], ...els.filter(e => e.year >= 2011).map(e => [`e${e.year}`, `${e.year} election result`]).reverse()];
  el.innerHTML = `<div class="stack" style="gap:16px"><p class="lede">Pick a result, then tap parties to build a government. It needs more than half the seats to survive confidence votes.</p>
    <div class="row"><select id="csrc" aria-label="Result">${srcs.map(([v, l]) => `<option value="${v}">${l}</option>`).join('')}</select>
    <button class="btn sm" id="pre-right">National + ACT + NZ First</button><button class="btn sm" id="pre-left">Labour + Green + Te Pāti Māori</button><button class="btn sm" id="pre-clear">Clear</button></div>
    <div class="card stack"><div class="chips" id="cchips"></div><div class="bar" id="cbar"></div><div id="cverdict" style="font:800 22px var(--font-display)"></div><div class="chamber" id="chemi"></div></div></div>`;
  let bloc = new Set(['national', 'act', 'nz-first']);
  const seatsFor = v => v === 'proj' ? projection().seats : Object.fromEntries((els.find(e => `e${e.year}` === v).parties || []).filter(r => r.total_seats).map(r => [r.party, r.total_seats]));
  const draw = () => { const seats = seatsFor($('#csrc').value), total = Object.values(seats).reduce((a, b) => a + b, 0), maj = Math.floor(total / 2) + 1, ps = Object.keys(seats).sort((a, b) => P(a).order - P(b).order);
    $('#cchips').innerHTML = ps.map(p => `<button class="chip" data-p="${p}" aria-pressed="${bloc.has(p)}"><span class="dot" style="background:${pcolor(p)}"></span>${esc(pname(p))} <span class="num">${seats[p]}</span></button>`).join('');
    const have = ps.filter(p => bloc.has(p)).reduce((a, p) => a + seats[p], 0);
    $('#cbar').innerHTML = ps.filter(p => bloc.has(p)).map(p => `<span style="width:${seats[p] / total * 100}%;background:${pcolor(p)}"></span>`).join('') + `<span class="line" style="left:${maj / total * 100}%"></span>`;
    $('#cverdict').innerHTML = have >= maj ? `<span style="color:var(--v-kept)">${have} seats: a majority of ${total}</span>` : `${have} of ${total} seats, ${maj - have} short of ${maj}`;
    $('#chemi').innerHTML = chamberSVG(seatsFromComposition(seats, []), { highlight: bloc, label: 'Coalition seats' }) };
  $('#cchips').onclick = e => { const b = e.target.closest('[data-p]'); if (!b) return; bloc.has(b.dataset.p) ? bloc.delete(b.dataset.p) : bloc.add(b.dataset.p); draw() };
  $('#csrc').onchange = draw; $('#pre-right').onclick = () => { bloc = new Set(['national', 'act', 'nz-first']); draw() };
  $('#pre-left').onclick = () => { bloc = new Set(['labour', 'green', 'te-pati-maori']); draw() }; $('#pre-clear').onclick = () => { bloc = new Set(); draw() };
  draw() };
SUB.calculator = el => {
  const pr = projection(); const rows = Object.keys({ ...pr.pct, ...pr.elec }).sort((a, b) => (pr.pct[b] || 0) - (pr.pct[a] || 0));
  el.innerHTML = `<div class="stack" style="gap:16px"><p class="lede">Type party-vote percentages and electorate wins. Seats are shared out of 120 using the Sainte-Laguë method (divisors 1, 3, 5, 7…). Parties need 5% or an electorate seat. Extra electorate wins become overhang seats. Starts from the latest poll average.</p>
    <div class="split"><div class="card scroll"><table><thead><tr><th>Party</th><th class="n">Party vote %</th><th class="n">Electorates</th><th class="n">Seats</th></tr></thead><tbody id="ctb">
    ${rows.map(p => `<tr data-p="${p}"><td><span class="row" style="gap:6px;flex-wrap:nowrap"><span class="dot" style="background:${pcolor(p)}"></span>${esc(pname(p))}</span></td><td class="n"><input type="number" style="width:84px" id="pv-${p}" step="0.1" min="0" max="100" value="${fmt(pr.pct[p] || 0)}"></td><td class="n"><input type="number" style="width:70px" id="ev-${p}" step="1" min="0" max="72" value="${pr.elec[p] || 0}"></td><td class="n"><b data-out="${p}">0</b></td></tr>`).join('')}
    </tbody></table><p class="small muted" id="csum" style="margin-top:10px"></p><button class="btn sm" id="cs-save">Use these electorate wins in the projection</button></div>
    <div class="card chamber"><div id="calchemi"></div><div class="legend" id="calcleg"></div></div></div></div>`;
  const run = () => { const pct = {}, elec = {}; $('#ctb').querySelectorAll('tr').forEach(tr => { const p = tr.dataset.p; pct[p] = parseFloat($('#pv-' + p).value) || 0; const e = parseInt($('#ev-' + p).value) || 0; if (e) elec[p] = e });
    const r = mmp(pct, elec); $('#ctb').querySelectorAll('[data-out]').forEach(b => b.textContent = r.seats[b.dataset.out] || 0);
    $('#csum').textContent = `House: ${r.total} seats (overhang ${r.overhang}). Majority needs ${Math.floor(r.total / 2) + 1}. Votes entered add to ${fmt(Object.values(pct).reduce((a, b) => a + b, 0))}%. Wasted vote: ${fmt(r.wasted)}%.`;
    $('#calchemi').innerHTML = chamberSVG(seatsFromComposition(r.seats, []), { label: 'Calculated seats' });
    $('#calcleg').innerHTML = Object.entries(r.seats).filter(([, n]) => n).sort((a, b) => P(a[0]).order - P(b[0]).order).map(([p, n]) => `<span class="item"><span class="dot" style="background:${pcolor(p)}"></span>${esc(pname(p))} <b class="num">${n}</b></span>`).join(''); return elec };
  $('#ctb').addEventListener('input', run); $('#cs-save').onclick = () => { store.set('elecAssume', JSON.stringify(run())); $('#cs-save').textContent = 'Saved' }; run() };
