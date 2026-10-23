/* ===== MMP maths ===== */
function sainteLague(votes, seats) { const out = {}; Object.keys(votes).forEach(p => out[p] = 0);
  for (let i = 0; i < seats; i++) { let best = null, bq = -1; for (const p in votes) { const q = votes[p] / (2 * out[p] + 1); if (q > bq) { bq = q; best = p } } if (best == null) break; out[best]++ }
  return out }
function mmp(pct, elec, threshold = 5, house = 120) {
  const qual = {}; for (const p in pct) if (pct[p] >= threshold || (elec[p] || 0) > 0) qual[p] = pct[p];
  const indep = Object.entries(elec).filter(([p]) => !(p in pct)).reduce((a, [, v]) => a + v, 0);
  const alloc = sainteLague(qual, house - indep); const res = {}; let overhang = 0;
  for (const p in qual) { const e = elec[p] || 0; if (e > alloc[p]) { overhang += e - alloc[p]; res[p] = e } else res[p] = alloc[p] }
  for (const [p, v] of Object.entries(elec)) if (!(p in pct)) res[p] = v;
  const wasted = Object.keys(pct).filter(p => !(p in qual)).reduce((a, p) => a + pct[p], 0);
  return { seats: res, overhang, total: Object.values(res).reduce((a, b) => a + b, 0), wasted } }
function projection(nPolls = 6) {
  const polls = (S.data.polls || []).filter(p => p.date && p.parties).sort((a, b) => b.date.localeCompare(a.date)).slice(0, nPolls);
  const sum = {}; polls.forEach(p => { for (const [k, v] of Object.entries(p.parties)) if (typeof v === 'number') sum[k] = (sum[k] || 0) + v });
  const pct = {}; Object.keys(sum).forEach(k => pct[k] = sum[k] / polls.length);
  let saved = null; try { saved = JSON.parse(store.get('elecAssume') || 'null') } catch {}
  const elec = saved || { 'te-pati-maori': 4, act: 1 };
  return { ...mmp(pct, elec), pct, elec, n: polls.length, range: polls.length ? `${polls[polls.length - 1].date} to ${polls[0].date}` : 'no polls loaded' } }

/* ===== hemicycle ===== */
function hemicycle(n) {
  const rows = n > 160 ? 9 : n > 110 ? 7 : n > 60 ? 5 : 4, r0 = .36;
  const radii = Array.from({ length: rows }, (_, i) => r0 + (1 - r0) * i / (rows - 1));
  const sum = radii.reduce((a, b) => a + b, 0), raw = radii.map(r => n * r / sum), counts = raw.map(Math.floor);
  const rem = n - counts.reduce((a, b) => a + b, 0);
  raw.map((v, i) => [v - Math.floor(v), i]).sort((a, b) => b[0] - a[0]).slice(0, rem).forEach(([, i]) => counts[i]++);
  const pts = []; radii.forEach((r, i) => { const k = counts[i]; for (let j = 0; j < k; j++) { const t = k === 1 ? Math.PI / 2 : Math.PI * (1 - j / (k - 1)); pts.push({ t, r, x: Math.cos(t) * r, y: Math.sin(t) * r }) } });
  pts.sort((a, b) => b.t - a.t || a.r - b.r); return { pts, dot: (1 - r0) / (rows - 1) * .42 } }
function chamberSVG(seatList, { highlight = null, label = 'Seats', animate = false, caption = true } = {}) {
  const n = seatList.length; if (!n) return '<p class="empty">No seat data yet.</p>';
  const { pts, dot } = hemicycle(n), R = 185, cx = 200, cy = 200;
  const c = pts.map((p, i) => { const s = seatList[i]; const dim = highlight && !highlight.has(s.party) ? ' dim' : '';
    const ring = ['nz-first', 'act'].includes(s.party) ? ' ring' : ''; return `<circle class="seat${dim}${ring}${animate ? ' pop' : ''}" style="${animate ? `animation-delay:${Math.min(400, i * 2.5)}ms;transform-origin:${(cx + p.x * R).toFixed(1)}px ${(cy - p.y * R).toFixed(1)}px` : ''}" tabindex="0" data-i="${i}" cx="${(cx + p.x * R).toFixed(1)}" cy="${(cy - p.y * R).toFixed(1)}" r="${(dot * R).toFixed(2)}" fill="${pcolor(s.party)}"><title>${esc(s.name || pname(s.party))}</title></circle>` }).join('');
  const maj = Math.floor(n / 2) + 1;
  return `<svg viewBox="0 0 400 ${caption ? 240 : 204}" role="img" aria-label="${esc(label)}">${c}${caption ? `<text x="200" y="222" text-anchor="middle" style="font:800 30px var(--font-display);fill:var(--text)">${n}</text><text x="200" y="237" text-anchor="middle" style="font:600 11px var(--font-mono);fill:var(--text-2)">seats · ${maj} to govern</text>` : ''}</svg>` }
function chamberUpdate(container, seatList, opts = {}) { // animate fills in place when the seat count is unchanged
  const svg = container.querySelector('svg'); const circles = svg ? svg.querySelectorAll('circle.seat') : [];
  if (!svg || circles.length !== seatList.length) { container.innerHTML = chamberSVG(seatList, { ...opts, animate: true }); return }
  circles.forEach((c, i) => { const s = seatList[i]; c.setAttribute('fill', pcolor(s.party)); c.querySelector('title').textContent = s.name || pname(s.party); c.classList.toggle('dim', !!(opts.highlight && !opts.highlight.has(s.party))) });
}
function seatsFromComposition(comp, members) {
  const parties = Object.keys(comp).filter(p => comp[p] > 0).sort((a, b) => P(a).order - P(b).order); const list = [];
  for (const p of parties) { const ms = (members || []).filter(m => m.party === p).sort((a, b) => (a.type === 'electorate' ? 0 : 1) - (b.type === 'electorate' ? 0 : 1) || String(a.name).localeCompare(b.name));
    for (let i = 0; i < comp[p]; i++) list.push(ms[i] ? { ...ms[i], party: p } : { party: p }) }
  return list }
function parliamentSeats(parl, mode) {
  const comp = mode === 'start' ? (parl.composition_start || {}) : (parl.composition_now_or_end || parl.composition_start || {});
  const startCut = new Date(parl.start || (parl.election_year + '-12-31')); startCut.setDate(startCut.getDate() + 30);
  const endRef = parl.end ? new Date(parl.end) : null;
  const ms = (parl.members || []).filter(m => { const en = m.entered ? new Date(m.entered) : null, lf = m.left ? new Date(m.left) : null;
    return mode === 'start' ? (!en || en <= startCut) : (!lf || (endRef && lf >= endRef)) })
    .map(m => { const ch = m.party_changes || []; const party = !ch.length ? m.party : mode === 'start' ? (ch[0].from || m.party) : (ch[ch.length - 1].to || m.party); return { ...m, party } });
  return seatsFromComposition(comp, ms) }
const currentParl = () => { const ps = S.data.parliaments || []; if (ps.length) return ps[ps.length - 1];
  const e = (S.data.elections || []).filter(x => x.parties).slice(-1)[0]; if (!e) return null;
  const comp = Object.fromEntries(e.parties.filter(r => r.total_seats).map(r => [r.party, r.total_seats]));
  return { parliament: e.parliament, election_year: e.year, composition_start: comp, composition_now_or_end: comp, members: [] } };
