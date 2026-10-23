/* ----- electorate map ----- */
const MAP_YEARS = [2011, 2014, 2017, 2020, 2023, 2026];
const slugify = n => String(n || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/^mount-|^mount /, 'mt-').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').replace(/^mount-/, 'mt-').replace(/-electorate$/, '');
async function loadGeo(setId) { S.geo = S.geo || {}; if (!S.geo.index) S.geo.index = await getJSON('data/geo/index.json');
  for (const t of ['general', 'maori']) { const k = `${t}-${setId}`; if (!S.geo[k]) S.geo[k] = await getJSON(`data/geo/${k}.json`).catch(() => ({ features: [] })) } return S.geo }
function projector(bbox, W, H) { const [x0, y0, x1, y1] = bbox; const midLat = (y0 + y1) / 2, kx = Math.cos(midLat * Math.PI / 180);
  const sw = (x1 - x0) * kx, sh = (y1 - y0), sc = Math.min(W / sw, H / sh); const ox = (W - sw * sc) / 2, oy = (H - sh * sc) / 2;
  return ([lon, lat]) => [ox + (lon - x0) * kx * sc, oy + (y1 - lat) * sc] }
function featPath(f, proj, bbox) { const polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates; let d = '';
  for (const poly of polys) { const ring = poly[0]; if (!ring || !ring.length) continue; if (ring[0][0] > 180 || ring[0][0] < bbox[0] - 1 || ring[0][0] > bbox[2] + 1 || ring[0][1] < bbox[1] - 1 || ring[0][1] > bbox[3] + 1) continue;
    d += ring.map((c, i) => { const [x, y] = proj(c); return (i ? 'L' : 'M') + x.toFixed(1) + ' ' + y.toFixed(1) }).join('') + 'Z' } return d }
function electorateResults(year) { // slug -> {party, winner, majority, runner_up, ...}
  const out = {};
  if (year === 2026) { for (const e of S.data.electorates || []) out[slugify(e.slug)] = { party: e.sitting_mp ? e.sitting_mp.party : null, winner: e.sitting_mp ? e.sitting_mp.name : 'Vacant', pending: true, e } ; return out }
  const el = S.data.elections.find(x => x.year === year); for (const r of (el && el.electorates) || []) out[slugify(r.name)] = r; return out }
V.map = async (startYear) => {
  $('#main').innerHTML = `<section class="view"><p class="empty">Loading the map…</p></section>`;
  await loadPeople();
  let year = +startYear || +(store.get('mapYear') || 2023); let type = store.get('mapType') || 'general'; let sel = null; let playing = null;
  const idx = (await loadGeo(S.geo && S.geo.index ? S.geo.index.election_to_boundary_set[2023] : 2020)).index;
  $('#main').innerHTML = `<section class="view"><div class="stack"><div class="kicker">Every seat since 2011</div><h2>The electorate map</h2>
    <p class="lede">Each electorate coloured by the party that won it. Drag the slider or press play to move through the elections, switch to the Māori electorates, and tap any seat for its story.</p></div>
    <div class="row" style="justify-content:space-between"><div class="chips"><button class="chip" id="mt-g" aria-pressed="${type === 'general'}">General electorates</button><button class="chip" id="mt-m" aria-pressed="${type === 'maori'}">Māori electorates</button></div><div class="legend" id="mlegend"></div></div>
    <div class="card scrubber"><button class="playbtn" id="mplay" aria-label="Play through the years">${ic('play', 22)}</button><div><input type="range" id="myear" min="0" max="${MAP_YEARS.length - 1}" step="1" value="${MAP_YEARS.indexOf(year)}" aria-label="Election year"><div class="years">${MAP_YEARS.map(y => `<span data-y="${y}">${y}</span>`).join('')}</div></div></div>
    <div class="split" style="grid-template-columns:minmax(0,1.1fr) minmax(0,1fr)"><div class="stack"><div class="card map" style="padding:8px" id="mmain"></div><div class="insets map" id="minsets"></div></div>
      <div class="card mapside" id="mside"><p class="muted">Tap an electorate.</p></div></div>
    <p class="tiny muted">Boundaries: Stats NZ / Representation Commission (CC BY 4.0), simplified; polygons extend offshore to the territorial-sea limit as published. Results: official counts via the archive's election data.</p></section>`;
  const draw = async () => { store.set('mapYear', year); store.set('mapType', type);
    const setId = idx.election_to_boundary_set[year]; await loadGeo(setId); const feats = S.geo[`${type}-${setId}`].features; const res = electorateResults(year);
    const aliases = ((idx.boundary_sets[setId] || {}).aliases) || {};
    const resFor = f => res[f.properties.slug] || res[aliases[f.properties.slug]] || res[slugify(f.properties.name)] || Object.values(res).find(r => r.e && slugify(r.e.name) === f.properties.slug) || null;
    const colour = f => { const r = resFor(f); return r && r.party ? pcolor(r.party) : 'var(--surface-2)' };
    const render = (bbox, W, H) => { const proj = projector(bbox, W, H); return feats.map(f => `<path class="el ${sel === f.properties.slug ? 'sel' : ''}" data-slug="${esc(f.properties.slug)}" d="${featPath(f, proj, bbox)}" fill="${colour(f)}"><title>${esc(f.properties.name)}${(r => r ? ' · ' + esc(r.winner || '') + (r.party ? ' (' + esc(pname(r.party)) + ')' : '') : '')(resFor(f))}</title></path>`).join('') };
    $('#mmain').innerHTML = `<svg viewBox="0 0 520 640" role="img" aria-label="Map of electorates, ${year}">${render(idx.bbox_mainland, 520, 640)}<text x="12" y="28" style="font:800 28px var(--font-display);fill:var(--text)">${year}${year === 2026 ? ' · current MPs' : ''}</text></svg>`;
    $('#minsets').innerHTML = type === 'general' ? ['auckland', 'wellington', 'christchurch'].map(k => { const ins = idx.insets[k]; return `<div class="inset"><span class="lab">${esc(ins.label)}</span><svg viewBox="0 0 200 200">${render(ins.bbox, 200, 200)}</svg></div>` }).join('') : '';
    const counts = {}; feats.forEach(f => { const r = resFor(f); const p = r && r.party ? r.party : 'vacant'; counts[p] = (counts[p] || 0) + 1 });
    $('#mlegend').innerHTML = Object.entries(counts).sort((a, b) => b[1] - a[1]).map(([p, n]) => `<span class="item"><span class="dot" style="background:${p === 'vacant' ? 'var(--surface-2)' : pcolor(p)}"></span>${p === 'vacant' ? 'Vacant' : esc(pname(p))} <b class="num">${n}</b></span>`).join('');
    $('#myear').value = MAP_YEARS.indexOf(year); document.querySelectorAll('.years span').forEach(x => x.classList.toggle('on', +x.dataset.y === year));
    $('#mt-g').setAttribute('aria-pressed', type === 'general'); $('#mt-m').setAttribute('aria-pressed', type === 'maori');
    if (sel) side(feats.find(f => f.properties.slug === sel), resFor) };
  const side = (f, resFor) => { if (!f) return; const r = resFor(f); const name = f.properties.name;
    const hist = MAP_YEARS.filter(y => y !== 2026).map(y => { const rr = electorateResults(y); const h = rr[f.properties.slug] || rr[slugify(name)]; return [y, h] });
    let html = `<div class="kicker">${type === 'maori' ? 'Māori electorate' : 'General electorate'}</div><h3>${esc(name)}</h3>`;
    if (r && r.pending) { const e = r.e; html += `<p>${r.party ? `<b>Current MP:</b> ${esc(r.winner)} (${esc(pname(r.party))})` : '<b>Vacant</b>'}${e.mp_standing_again === false ? ' · not standing again' : ''}</p>
        ${e.contest_notes ? `<p class="small muted">${esc(e.contest_notes)}</p>` : ''}<div class="tiny muted">${(e.candidates || []).length} candidates in 2026</div><div class="row" style="gap:6px">${(e.candidates || []).slice(0, 12).map(c => { const p = findPerson(c.slug, c.name) || { name: c.name, party: c.party }; return `<span title="${esc(c.name)} (${esc(pname(c.party))})">${faceHTML(p, c.party, 'face" style="width:40px;height:40px;--pc:' + pcolor(c.party))}</span>` }).join('')}</div>
        <button class="btn sm" data-go="electorate-${esc(e.slug)}" style="justify-self:start">Candidates & 2026 guide</button>` }
    else if (r) html += `<p><b>${year} winner:</b> ${esc(r.winner)} (${esc(pname(r.party))})${r.majority ? ` by <span class="num">${Number(r.majority).toLocaleString('en-NZ')}</span>` : ''}${r.runner_up ? ` over ${esc(r.runner_up)} (${esc(pname(r.runner_up_party))})` : ''}${r.result ? ` · <span class="badge">${esc(r.result)}</span>` : ''}</p>`;
    else html += `<p class="muted">No result on record for this boundary set.</p>`;
    html += `<h4>History</h4><div class="hist">${hist.map(([y, h]) => `<div><span class="num muted">${y}</span><span class="dot" style="background:${h && h.party ? pcolor(h.party) : 'var(--surface-2)'}"></span><span>${h ? esc(h.winner) + ' <span class="muted">· ' + esc(pname(h.party)) + '</span>' : '<span class="muted">seat did not exist</span>'}</span></div>`).join('')}</div>`;
    $('#mside').innerHTML = html };
  $('#main').addEventListener('click', e => { const p = e.target.closest('path.el'); if (!p) return; sel = p.dataset.slug; document.querySelectorAll('path.el').forEach(x => x.classList.toggle('sel', x.dataset.slug === sel)); draw() });
  $('#myear').oninput = () => { year = MAP_YEARS[+$('#myear').value]; draw() };
  $('#mt-g').onclick = () => { type = 'general'; sel = null; draw() }; $('#mt-m').onclick = () => { type = 'maori'; sel = null; draw() };
  $('#mplay').onclick = () => { if (playing) { clearInterval(playing); playing = null; $('#mplay').innerHTML = ic('play', 22); return }
    $('#mplay').innerHTML = ic('pause', 22); year = MAP_YEARS[0]; draw(); playing = setInterval(() => { const i = MAP_YEARS.indexOf(year); if (i >= MAP_YEARS.length - 1) { clearInterval(playing); playing = null; $('#mplay').innerHTML = ic('play', 22); return } year = MAP_YEARS[i + 1]; draw() }, 1400) };
  draw();
};
