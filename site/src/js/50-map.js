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
  if (year === 2026) { const R = results2026(); if (R && (R.electorates || []).length) { for (const r of R.electorates) out[slugify(r.name || r.slug)] = { ...r, live: true }; return out }
    for (const e of S.data.electorates || []) out[slugify(e.slug)] = { party: e.sitting_mp ? e.sitting_mp.party : null, winner: e.sitting_mp ? e.sitting_mp.name : 'Vacant', pending: true, e }; return out }
  const el = S.data.elections.find(x => x.year === year); for (const r of (el && el.electorates) || []) out[slugify(r.name)] = r; return out }
// The map's land and seat polygons for one bbox, as <path>s with a data-driven fill. Chatham Islands (+360 longitudes) are skipped by featPath.
function mapPaths(feats, resFor, bbox, W, H, sel) { const proj = projector(bbox, W, H);
  const one = f => { const d = featPath(f, proj, bbox); if (!d) return ''; const r = resFor(f);
    return `<path${sel === f.properties.slug ? ' class="is-sel"' : ''} data-slug="${esc(f.properties.slug)}" d="${d}" style="fill:${r && r.party ? pcolor(r.party) : 'var(--seat-empty)'}"><title>${esc(mapTitle(f, r))}</title></path>` };
  // the selected seat is drawn last so its outline sits on top
  return feats.filter(f => f.properties.slug !== sel).map(one).join('') + feats.filter(f => f.properties.slug === sel).map(one).join('') }
const mapTitle = (f, r) => f.properties.name + (r ? ' · ' + (r.winner || '') + (r.party ? ' (' + pname(r.party) + ')' : '') : ' · no result on record');
async function mapContext(year, type) { const idx = S.geo.index; const setId = idx.election_to_boundary_set[year]; await loadGeo(setId);
  const feats = (S.geo[`${type}-${setId}`] || {}).features || []; const res = electorateResults(year); const aliases = ((idx.boundary_sets[setId] || {}).aliases) || {};
  const resFor = f => res[f.properties.slug] || res[aliases[f.properties.slug]] || res[slugify(f.properties.name)] || Object.values(res).find(r => r.e && slugify(r.e.name) === f.properties.slug) || null;
  return { idx, setId, feats, res, resFor } }

V.map = async (startYear, startSlug) => {
  $('#main').innerHTML = sectionFrame('seats', 'seats/map', `<p class="muted">Loading the map…</p>`);
  const route = S.route; await loadPeople(); await loadGeo(2020);
  if (S.route !== route) return;   // the reader moved on while the boundaries loaded: don't draw over the new page
  const idx = S.geo.index;
  let year = MAP_YEARS.includes(+startYear) ? +startYear : (MAP_YEARS.includes(+store.get('mapYear')) ? +store.get('mapYear') : 2023);
  const layerArg = ['maori', 'general'].includes(startSlug) ? startSlug : null; if (layerArg) startSlug = undefined;
  let type = layerArg || (store.get('mapType') === 'maori' ? 'maori' : 'general'), sel = startSlug ? slugify(decodeURIComponent(startSlug)) : null, selName = '', listOn = false, built = '';
  if (sel) { const set = (idx.boundary_sets[idx.election_to_boundary_set[year]] || {}).layers || {};
    if (set.maori && set.maori.names[sel]) type = 'maori'; else if (set.general && set.general.names[sel]) type = 'general';
    selName = (set[type] && set[type].names[sel]) || '' }
  $('#main').innerHTML = sectionFrame('seats', 'seats/map', `
    <header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('seats', 'i--s')} Seats · Electorate map</p><h1>Every electorate since 2011</h1>
      <p class="lede">Each seat is coloured by the party whose candidate won it. Press play to watch the map change, or tap a seat for its story.</p></header>
    ${scrubberHTML({ id: 'mscrub', labels: MAP_YEARS.map(String), i: MAP_YEARS.indexOf(year) })}
    <div class="row row--between"><div class="seg" role="group" aria-label="Electorate type"><button type="button" data-t="general" aria-pressed="${type === 'general'}">General</button><button type="button" data-t="maori" aria-pressed="${type === 'maori'}">Māori</button></div>
      <button class="btn btn--s btn--quiet" type="button" id="mlist" aria-expanded="false" aria-controls="mlistbox">${ic('list', 'i--xs')} <span>List view</span></button></div>
    <div class="split split--7-5 mapsplit">
      <div class="mapstage" id="mstage"><div id="mmain"></div><div class="insets" id="minsets"></div>
        <div class="legend" id="mlegend" role="group" aria-label="Seats won by each party, A to Z"></div>
        <p class="small soft" id="malt">Colour is never the only cue: <button class="linkbtn" type="button" id="mlist2" aria-controls="mlistbox">the list view</button> names every seat, its winner and their party.</p></div>
      <section class="seatsheet sticky" id="mside" aria-live="polite" aria-labelledby="h-seat"></section>
    </div>
    <section class="stack" id="mlistbox" hidden aria-labelledby="h-mlist"></section>
    <p class="srcline">Boundaries: Stats NZ / Representation Commission (CC BY 4.0). Results: official counts, Electoral Commission.</p>
    <details class="disclose"><summary>About the boundaries and the results</summary><div class="disclose__body"><p class="small">Boundaries: Stats NZ / Representation Commission (CC BY 4.0), simplified; polygons extend offshore to the territorial-sea limit as published, and the Chatham Islands are left off the drawing. Each election is drawn on the boundaries it was fought on (2011 on the 2007 set, 2014 and 2017 on 2014, 2020 and 2023 on 2020, 2026 on 2025). Results: official counts via the archive's election data. For 2026, until results come in, seats are coloured by the party of the sitting MP: that is not a result or a prediction.</p></div></details>`);
  const scrub = bindScrubber($('#mscrub'), { labels: MAP_YEARS.map(String), get: () => MAP_YEARS.indexOf(year), set: i => { year = MAP_YEARS[i]; draw() } });
  const url = () => { const p = 'seats/map/' + year + (sel ? '/' + sel : ''); try { history.replaceState(history.state, '', '#/' + p) } catch {} S.route = p };
  let ctx = null;
  const draw = async () => { store.set('mapYear', year); store.set('mapType', type);
    const want = year; const c = await mapContext(year, type); if (want !== year) return; ctx = c;
    const { idx, setId, feats, resFor } = c; const key = type + '-' + setId;
    const pending = year === 2026 && !results2026();
    if (built !== key) { built = key;
      $('#mmain').innerHTML = `<svg class="nzmap" viewBox="0 0 520 640" role="img" aria-label="" aria-describedby="mlegend malt"><text class="yr" x="20" y="96" font-size="96">${year}</text>${mapPaths(feats, resFor, idx.bbox_mainland, 520, 640, sel)}</svg>`;
      $('#minsets').innerHTML = type === 'general' ? ['auckland', 'wellington', 'christchurch'].map(k => { const ins = idx.insets[k]; return `<div class="inset"><span>${esc(ins.label)}</span><svg class="nzmap" viewBox="0 0 200 200" role="img" aria-label="${esc(ins.label)} electorates, enlarged" aria-describedby="malt">${mapPaths(feats, resFor, ins.bbox, 200, 200, sel)}</svg></div>` }).join('') : '';
      $('#minsets').hidden = type !== 'general' }
    else { const bySlug = Object.fromEntries(feats.map(f => [f.properties.slug, f]));
      $('#mstage').querySelectorAll('path[data-slug]').forEach(p => { const f = bySlug[p.dataset.slug]; if (!f) return; const r = resFor(f); p.style.fill = r && r.party ? pcolor(r.party) : 'var(--seat-empty)'; p.querySelector('title').textContent = mapTitle(f, r) }) }
    $('#mmain .yr').textContent = year;
    $('#mmain svg').setAttribute('aria-label', `Map of ${type === 'maori' ? 'Māori' : 'general'} electorates coloured by the ${pending ? 'party of the sitting MP, 2026' : year + ' winner'}`);
    $('#mscrub .scrubber__note').textContent = `${setId} boundaries · ${feats.length} seats${pending ? ' · sitting MPs, not a result' : year === 2026 ? ' · 2026 result' : ''}`;
    const counts = {}; feats.forEach(f => { const r = resFor(f); const p = r && r.party ? r.party : 'vacant'; counts[p] = (counts[p] || 0) + 1 });
    $('#mlegend').innerHTML = legendHTML(counts, true);
    markSel(); side(); if (listOn) list(); scrub.sync(MAP_YEARS.indexOf(year)); url() };
  const markSel = () => $('#mstage').querySelectorAll('path[data-slug]').forEach(p => { const on = p.dataset.slug === sel; p.classList.toggle('is-sel', on); if (on) p.parentNode.appendChild(p) });
  const side = () => { const box = $('#mside');
    box.classList.toggle('seatsheet--idle', !sel);
    if (!sel) { box.classList.remove('seatsheet--float'); box.innerHTML = `<p class="eyebrow">${type === 'maori' ? 'Māori electorates' : 'General electorates'} · ${year}</p><h2 class="h3" id="h-seat">Tap a seat</h2><p class="small soft">Tap any electorate for who won it and how it has voted since 2011, or open the list view to read every seat and winner.</p>`; return }
    const f = ctx.feats.find(x => x.properties.slug === sel); const name = f ? f.properties.name : (selName || sel); selName = name;
    const r = f ? ctx.resFor(f) : null; const e26 = (S.data.electorates || []).find(x => slugify(x.slug) === sel || slugify(x.name) === sel);
    const hist = MAP_YEARS.filter(y => y !== 2026).map(y => { const rr = electorateResults(y); return [y, rr[sel] || rr[slugify(name)] || null] });
    let html = `<span class="seatsheet__grab" aria-hidden="true"></span><div class="seatsheet__top"><p class="eyebrow">${type === 'maori' ? 'Māori electorate' : 'General electorate'}${e26 && e26.region ? ' · ' + esc(e26.region) : ''}</p><button class="iconbtn iconbtn--quiet" type="button" id="mclose" aria-label="Close the seat details">${ic('close', 'i--s')}</button></div><h2 id="h-seat">${esc(name)}</h2>`;
    if (!f) html += `<p class="small soft">There was no ${esc(name)} electorate in ${year}: the boundaries changed.</p>`;
    else if (r && r.pending) { const e = r.e;
      html += `<p>${r.party ? `<b>Sitting MP:</b> ${esc(r.winner)} (${esc(pname(r.party))})` : '<b>Vacant</b>'}${e.mp_standing_again === false ? ' · not standing again' : ''}. The 2026 result comes in from 7pm on 7 November.</p>
        ${e.contest_notes ? `<p class="small soft">${esc(e.contest_notes)}</p>` : ''}
        ${(e.candidates || []).length ? `<div class="mapfaces" aria-label="Candidates, in ballot order">${(e.candidates || []).slice().sort((a, b) => String(a.name).split(' ').pop().localeCompare(String(b.name).split(' ').pop(), 'en-NZ')).slice(0, 12).map(c => { const p = findPerson(c.slug, c.name) || { name: c.name, party: c.party }; return `<span title="${esc(c.name)} (${esc(pname(c.party))})">${faceHTML(p, c.party, 'face mapface')}</span>` }).join('')}</div>` : ''}` }
    else if (r) html += `<p><b>${year}:</b> ${esc(r.winner)} (${esc(pname(r.party))}) ${/hold|retain/i.test(r.result || '') ? 'held the seat' : 'won the seat'}${r.majority ? ` by <b class="num">${Number(r.majority).toLocaleString('en-NZ')} votes</b>` : ''}${r.runner_up ? ` over ${esc(r.runner_up)} (${esc(pname(r.runner_up_party))})` : ''}.${r.result ? ` <span class="badge">${esc(r.result)}</span>` : ''}</p>`;
    else html += `<p class="small soft">No result on record for this boundary set.</p>`;
    html += `<div class="history" aria-label="Winning party at each election">${hist.map(([y, h]) => `<div style="--pc:${h && h.party ? pcolor(h.party) : 'var(--seat-empty)'}"${y === year ? ' aria-current="true"' : ''}><i></i>${y}<span>${h ? esc(pname(h.party)) : 'no seat'}</span></div>`).join('')}</div>`;
    if (e26) html += `<div class="row"><a class="btn btn--s btn--ink" href="#/vote/electorate/${esc(e26.slug)}">2026: ${(e26.candidates || []).length} candidates ${ic('chev', 'i--xs')}</a></div>`;
    box.innerHTML = html; box.classList.add('seatsheet--float');
    $('#mclose').onclick = () => { const was = sel; sel = null; markSel(); side(); if (listOn) list(); url();
      // focus goes back to the seat's row in the list view, or to the list button
      const back = (listOn && $('#mlistbox').querySelector(`[data-sel="${CSS.escape(was)}"]`)) || $('#mlist'); if (back) back.focus() } };
  const list = () => { const rows = ctx.feats.map(f => [f, ctx.resFor(f)]).sort((a, b) => a[0].properties.name.localeCompare(b[0].properties.name, 'en-NZ'));
    const pending = year === 2026 && !results2026();
    $('#mlistbox').innerHTML = `<div class="shead"><div class="shead__row"><h2 id="h-mlist">Every ${type === 'maori' ? 'Māori' : 'general'} seat, ${year}</h2><span class="small muted">${rows.length} seats · A–Z${pending ? ' · sitting MPs, not a result' : ''}</span></div></div>
      ${twrap(`Every ${type === 'maori' ? 'Māori' : 'general'} seat, ${year}`, `<table class="table"><thead><tr><th scope="col">Electorate</th><th scope="col">${pending ? 'Sitting MP' : 'Winner'}</th><th scope="col">Party</th><th class="n" scope="col">Majority</th></tr></thead><tbody>
      ${rows.map(([f, r]) => `<tr${f.properties.slug === sel ? ' aria-current="true"' : ''}><td><button class="linkbtn" type="button" data-sel="${esc(f.properties.slug)}">${esc(f.properties.name)}</button></td><td>${r ? esc(r.winner || '') : '<span class="muted">no result</span>'}</td><td>${r && r.party ? ptagHTML(r.party) : '–'}</td><td class="n">${r && r.majority ? Number(r.majority).toLocaleString('en-NZ') : '–'}</td></tr>`).join('')}
      </tbody></table>`)}` };
  $('#mstage').addEventListener('click', e => { const p = e.target.closest('path[data-slug]'); if (!p) return; sel = p.dataset.slug; markSel(); side(); if (listOn) list(); url() });
  $('#mlistbox').addEventListener('click', e => { const b = e.target.closest('[data-sel]'); if (!b) return; sel = b.dataset.sel; markSel(); side(); list(); url(); $('#mside').scrollIntoView({ block: 'nearest', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    const h = $('#h-seat'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }) } });
  const toggleList = (on = !listOn) => { listOn = on; $('#mlist').setAttribute('aria-expanded', listOn); $('#mlist2').setAttribute('aria-expanded', listOn); $('#mlist span').textContent = listOn ? 'Hide list' : 'List view'; $('#mlistbox').hidden = !listOn;
    if (listOn) { list(); $('#mlistbox').scrollIntoView({ block: 'start', behavior: 'auto' }); const h = $('#h-mlist'); h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }) } };
  $('#mlist').onclick = () => toggleList(); $('#mlist2').onclick = () => toggleList(true);
  $('#main').querySelector('.seg[aria-label="Electorate type"]').onclick = e => { const b = e.target.closest('[data-t]'); if (!b || b.dataset.t === type) return; type = b.dataset.t; sel = null;
    b.parentElement.querySelectorAll('[data-t]').forEach(x => x.setAttribute('aria-pressed', x === b)); draw() };
  await draw();
};
