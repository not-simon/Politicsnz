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
// Seat map. svg.hemi with one <circle style="--pc;--i"> per seat: fills and the pop-in stagger come from CSS.
// opts: highlight (Set of parties to keep at full strength), label, caption (count + "N to govern"), majLine,
// interactive (seats are buttons with one tab stop; arrow keys move between them, see bindSeatKeys), describedby (ids of the
// text alternative: the legend counts and the caption)
function chamberSVG(seatList, { highlight = null, label = 'Seats', caption = true, majLine = true, interactive = false, describedby = '' } = {}) {
  const n = seatList.length; if (!n) return '<p class="muted small">No seat data yet.</p>';
  const { pts, dot } = hemicycle(n), R = 185, cx = 200, cy = 200, maj = Math.floor(n / 2) + 1;
  const c = pts.map((p, i) => { const s = seatList[i]; const dim = highlight && !highlight.has(s.party);
    return `<circle${dim ? ' class="is-dim"' : ''} style="--pc:${pcolor(s.party)};--i:${i}"${interactive ? ` role="button" tabindex="${i ? -1 : 0}" aria-label="${esc(seatLabel(s, i, n))}"` : ''} data-i="${i}" cx="${(cx + p.x * R).toFixed(1)}" cy="${(cy - p.y * R).toFixed(1)}" r="${(dot * R).toFixed(2)}"><title>${esc(seatTitle(s))}</title></circle>` }).join('');
  let line = '';
  if (majLine && n > maj) { const t = (pts[maj - 1].t + pts[maj].t) / 2, r0 = Math.min(...pts.map(p => p.r)) - dot * 1.4, r1 = 1 + dot * 1.4;
    const x0 = cx + Math.cos(t) * r0 * R, y0 = cy - Math.sin(t) * r0 * R, x1 = cx + Math.cos(t) * r1 * R, y1 = cy - Math.sin(t) * r1 * R;
    line = `<line class="maj" x1="${x0.toFixed(1)}" y1="${y0.toFixed(1)}" x2="${x1.toFixed(1)}" y2="${y1.toFixed(1)}" aria-hidden="true"/><text class="hemi__maj" x="${x1.toFixed(1)}" y="${(y1 - 4).toFixed(1)}" text-anchor="middle" aria-hidden="true">${maj}</text>` }
  const name = `${label}: ${n} seats, ${maj} needed to govern${interactive ? '. Seats are buttons: use the arrow keys to move between them and Enter to see who sat there' : ''}`;
  return `<svg class="hemi" viewBox="0 -14 400 ${caption ? 258 : 218}" role="${interactive ? 'group' : 'img'}" aria-label="${esc(name)}"${describedby ? ` aria-describedby="${describedby}"` : ''}>${line}${c}${caption ? `<text class="hemi__n" x="200" y="214" text-anchor="middle" aria-hidden="true">${n}</text><text class="hemi__l" x="200" y="236" text-anchor="middle" aria-hidden="true">seats · ${maj} to govern</text>` : ''}</svg>` }
const seatTitle = s => s.name ? `${s.name} · ${pname(s.party)}` : `${pname(s.party)} seat`;
const seatLabel = (s, i, n) => `Seat ${i + 1} of ${n}: ${seatTitle(s)}`;
// Roving focus across an interactive hemicycle: one tab stop, arrows/Home/End move along the seats (left to right).
function bindSeatKeys(container) { container.addEventListener('keydown', e => { const c = e.target.closest && e.target.closest('circle[data-i]'); if (!c) return;
  const all = [...container.querySelectorAll('circle[data-i]')], i = +c.dataset.i;
  const k = { ArrowRight: i + 1, ArrowDown: i + 1, ArrowLeft: i - 1, ArrowUp: i - 1, Home: 0, End: all.length - 1, PageDown: i + 10, PageUp: i - 10 }[e.key]; if (k == null) return;
  e.preventDefault(); const t = all[Math.max(0, Math.min(all.length - 1, k))]; all.forEach(x => x.setAttribute('tabindex', x === t ? '0' : '-1')); t.focus() }) }
// Change seats in place (fills cross-fade through CSS) when the count is unchanged; otherwise redraw (seats pop in).
function chamberUpdate(container, seatList, opts = {}) {
  const svg = container.querySelector('svg.hemi'); const circles = svg ? svg.querySelectorAll('circle') : [];
  if (!svg || circles.length !== seatList.length) { container.innerHTML = chamberSVG(seatList, opts); return }
  circles.forEach((c, i) => { const s = seatList[i]; c.style.setProperty('--pc', pcolor(s.party)); c.querySelector('title').textContent = seatTitle(s); if (c.hasAttribute('role')) c.setAttribute('aria-label', seatLabel(s, i, seatList.length)); c.classList.toggle('is-dim', !!(opts.highlight && !opts.highlight.has(s.party))) });
  if (opts.label) { const n = seatList.length; svg.setAttribute('aria-label', `${opts.label}: ${n} seats, ${Math.floor(n / 2) + 1} needed to govern${opts.interactive ? '. Seats are buttons: use the arrow keys to move between them and Enter to see who sat there' : ''}`) }
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

/* ===== shared Seats helpers ===== */
const byShort = (a, b) => pname(a).localeCompare(pname(b), 'en-NZ', { sensitivity: 'base' });   // A–Z by short name
const seatDate = iso => { if (!iso) return ''; const d = new Date(String(iso).slice(0, 10) + 'T12:00:00'); return isNaN(d) ? String(iso) : d.toLocaleDateString('en-NZ', { day: 'numeric', month: 'short', year: 'numeric' }) };
const inHundred = v => v == null ? '–' : v >= 99.5 ? 'over 99 in 100' : v < 0.5 ? 'under 1 in 100' : `${Math.round(v)} in 100`;
// Nothing predictive (polls, forecast, poll-based projections) on election day before 7pm.
const forecastHidden = () => electionPhase() === 'electionday';
// The 2026 result once it is loaded: an elections entry for 2026 with `results` (or party rows), or upcoming.results.
function results2026() {
  const cands = [...(S.data.elections || []).filter(e => e.year === 2026), S.data.upcoming].filter(Boolean);
  for (const e of cands) {
    const r = Array.isArray(e.results) ? { parties: e.results } : e.results;
    if (r && (r.parties || []).length) return { year: 2026, date: e.date, parliament: e.parliament || 55, ...r };
    if (e.year === 2026 && (e.parties || []).some(p => p && p.party_vote_pct != null)) return { year: 2026, ...e } }
  return null }
const legendHTML = (counts, sq = false) => Object.entries(counts).sort((a, b) => a[0] === 'vacant' ? 1 : b[0] === 'vacant' ? -1 : byShort(a[0], b[0]))
  .map(([p, n]) => `<span style="--pc:${p === 'vacant' ? 'var(--seat-empty)' : pcolor(p)}"><span class="sw${sq ? ' sw--sq' : ''}"></span>${p === 'vacant' ? 'No result' : esc(pname(p))} <b>${n}</b></span>`).join('');
const ptagHTML = (p, label) => `<span class="ptag ptag--s" style="--pc:${pcolor(p)}"><span class="sw"></span>${esc(label || pname(p))}</span>`;

/* ----- scrubber (map, parliament): play + rolling year + range + stops. Steps every 1200ms; timer lives in S.scrubTimer
   so the router clears it on navigation. Keyboard: the range takes arrow keys; reduced motion: CSS drops the roll, steps stay. */
function scrubberHTML({ id, labels, i, aria = 'Election year', play = 'Play through the years', note = '' }) {
  const fill = labels.length > 1 ? i / (labels.length - 1) * 100 : 0;
  // The year is announced while playing (aria-live switches to polite then); when the reader moves the slider, its
  // aria-valuetext says the year instead, so it isn't spoken twice.
  return `<div class="scrubber" id="${id}" role="group" aria-label="${esc(aria)}"><button class="scrubber__play" type="button" aria-label="${esc(play)}">${ic('play')}${ic('pause')}</button>
    <div class="scrubber__main"><div class="scrubber__head"><div class="scrubber__year" aria-live="off" aria-atomic="true"><span>${esc(labels[i])}</span></div><span class="scrubber__note">${note}</span></div>
      <div class="scrubber__track"><input class="range" type="range" id="${id}-range" min="0" max="${labels.length - 1}" step="1" value="${i}" aria-label="${esc(aria)}: ${esc(labels[0])} to ${esc(labels[labels.length - 1])}" aria-valuetext="${esc(labels[i])}" style="--fill:${fill}%">
        <div class="scrubber__stops" aria-hidden="true">${labels.map((l, k) => `<span data-k="${k}" aria-current="${k === i}">${esc(l)}</span>`).join('')}</div></div></div></div>` }
function bindScrubber(el, { labels, get, set, play = 'Play through the years' }) {
  const range = el.querySelector('.range'), btn = el.querySelector('.scrubber__play'), yr = el.querySelector('.scrubber__year'), stops = [...el.querySelectorAll('.scrubber__stops span')];
  const sync = i => { range.value = i; range.style.setProperty('--fill', (labels.length > 1 ? i / (labels.length - 1) * 100 : 0) + '%'); range.setAttribute('aria-valuetext', labels[i]);
    stops.forEach((s, k) => s.setAttribute('aria-current', String(k === i))); if (yr.textContent !== labels[i]) yr.innerHTML = `<span>${esc(labels[i])}</span>` };
  const stop = () => { if (S.scrubTimer) { clearInterval(S.scrubTimer); S.scrubTimer = null } el.removeAttribute('data-playing'); btn.setAttribute('aria-label', play); yr.setAttribute('aria-live', 'off') };
  const to = i => { sync(i); set(i) };
  range.addEventListener('input', () => { stop(); to(+range.value) });
  el.querySelector('.scrubber__stops').addEventListener('click', e => { const s = e.target.closest('[data-k]'); if (s) { stop(); to(+s.dataset.k) } });
  btn.addEventListener('click', () => { if (el.hasAttribute('data-playing')) { stop(); return }
    if (S.scrubTimer) clearInterval(S.scrubTimer);
    el.setAttribute('data-playing', ''); btn.setAttribute('aria-label', 'Pause the playback'); yr.setAttribute('aria-live', 'polite'); to(0);
    S.scrubTimer = setInterval(() => { if (!el.isConnected) { stop(); return } const i = get(); if (i >= labels.length - 1) { stop(); return } to(i + 1); if (i + 1 >= labels.length - 1) stop() }, 1200) });
  return { sync, stop } }

/* ----- shared bits for the Seats pages ----- */
// A table that scrolls sideways on phones: a named, focusable region so keyboard users can scroll it too.
const twrap = (label, table) => `<div class="table-wrap" tabindex="0" role="region" aria-label="${esc(label)}">${table}</div>`;
// "On this page" rows that jump to a heading (hash links would change the route, so these are buttons).
const jumpRow = (target, title, sub) => `<button class="rowlink rowlink--plain rowlink--btn" type="button" data-jump="${esc(target)}"><span><span class="rowlink__title">${title}</span>${sub ? `<span class="rowlink__sub" style="display:block">${sub}</span>` : ''}</span>${ic('down')}</button>`;
function bindJumps(root) { root.addEventListener('click', e => { const b = e.target.closest('[data-jump]'); if (!b) return; const t = document.getElementById(b.dataset.jump); if (!t) return;
  if (t.tagName === 'DETAILS') t.open = true;
  const h = t.matches('h1,h2,h3,summary') ? t : (t.querySelector('h2,h3,summary') || t); if (!h.hasAttribute('tabindex') && !/^(SUMMARY|BUTTON|A)$/.test(h.tagName)) h.setAttribute('tabindex', '-1');
  h.scrollIntoView({ block: 'start', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }); h.focus({ preventScroll: true }) }) }
