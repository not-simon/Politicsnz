/* ===== Vote › Your electorate: finder → found → candidates in ballot order → 2023 result → history ===== */
const elSlug = n => String(n || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/^mount-|^mount /, 'mt-').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').replace(/^mount-/, 'mt-').replace(/-electorate$/, '');
const ELEC_CONSENT = 'Your browser will ask for permission. Your location is checked against the electorate map on this device only; it is not stored or sent anywhere. You can also just choose your electorate from the list.';
// Ballot order: A–Z by surname (last word, keeping lower-case particles such as "van"), then given names
function surnameKey(name) { const w = String(name || '').trim().split(/\s+/); let i = w.length - 1; while (i > 0 && /^(van|von|de|da|di|du|le|la|te|der|den)$/.test(w[i - 1])) i--;
  return (w.slice(i).join(' ') + ' ' + w.slice(0, i).join(' ')).replace(/^(van|von|de|da|di|du|le|la|te|der|den)\s+/i, '') }
const ballotSort = (a, b) => surnameKey(a.name).localeCompare(surnameKey(b.name), 'en-NZ', { sensitivity: 'base' });
const elInitials = n => String(n || '?').replace(/[^A-Za-zĀ-ūÀ-ÿ' -]/g, '').split(/\s+/).filter(Boolean).map(w => w[0]).filter((_, i, a) => i === 0 || i === a.length - 1).join('').toUpperCase();
function elList() { return (S.data.electorates || []).slice().sort((a, b) => a.name.localeCompare(b.name, 'en-NZ')) }
function featToElectorate(f) { if (!f) return null; const E = S.data.electorates || []; const s = f.properties && (f.properties.slug || elSlug(f.properties.name));
  return E.find(x => elSlug(x.slug) === s || elSlug(x.name) === s) || null }

function candFace(c) { const img = faceSrc(c); const pc = pcolor(c.party);
  return img ? `<img class="face" style="--pc:${pc}" loading="lazy" src="${img}" alt="" width="56" height="56">` : `<span class="face face--none" style="--pc:${pc}" aria-hidden="true">${esc(elInitials(c.name))}</span>` }
function candRow(c) { const p = findPerson(c.slug, c.name) || {}; const mp = !!c.sitting_mp;
  return `<li><button class="cand" type="button" data-cand="${esc(c.slug || '')}" data-cname="${esc(c.name)}">${candFace(c)}<span><span class="cand__name">${esc(c.name)}</span>
    <span class="cand__meta"><span class="ptag ptag--s" style="--pc:${pcolor(c.party)}"><span class="sw"></span>${esc(S.data.parties[c.party] ? pname(c.party) : (c.party_name || pname(c.party)))}</span>${mp ? '<span class="badge badge--ink">Sitting MP</span>' : ''}<span>${c.list_rank_2026 ? `List #${c.list_rank_2026}` : 'Electorate only'}</span></span></span>${ic('chev')}</button></li>` }

// winners of this seat (or the seat(s) it replaced) at each election since 2011
function elHistory(e) { const names = new Set([e.name, ...(e.predecessor_seats || [])].map(elSlug)); const out = [];
  for (const el of (S.data.elections || []).filter(x => x.year >= 2011).sort((a, b) => a.year - b.year)) {
    const hits = (el.electorates || []).filter(r => names.has(elSlug(r.name)));
    const r = hits.find(h => elSlug(h.name) === elSlug(e.name)) || hits[0]; if (r) out.push({ year: el.year, r, other: hits.length > 1 }) }
  return out }

function electorateBody(e) { const r = e.result_2023 || {}; const eday = isElectionDay(); const maori = e.type === 'maori';
  const cands = (e.candidates || []).slice().sort(ballotSort);
  const loc = S.locHit || {}; const here = featToElectorate(maori ? loc.maori : loc.general); const alt = here && here.slug === e.slug ? featToElectorate(maori ? loc.general : loc.maori) : null;
  const altLine = maori ? `This is one of the seven <a href="#/vote/maori">Māori electorates</a>: you vote here if you’re on the Māori roll.${alt ? ` On the general roll, your electorate is <b>${esc(alt.name)}</b> (<a href="#/vote/electorate/${esc(alt.slug)}">see it</a>).` : ''}`
    : `On the Māori roll? ${alt ? `Your electorate is <b>${esc(alt.name)}</b>. <a href="#/vote/electorate/${esc(alt.slug)}">See its candidates</a>.` : 'Your Māori electorate depends on where you live; use your location above, or check at vote.nz.'} <a href="#/vote/maori">How the Māori electorates work</a>. <a href="https://vote.nz" target="_blank" rel="noopener">Not sure which roll you’re on?</a>`;
  // 2023 result: top two and the margin
  const rc = (r.candidates || []).slice().sort((a, b) => (b.votes || 0) - (a.votes || 0)); const top2 = rc.slice(0, 2); const maxPct = Math.max(1, ...top2.map(c => c.pct || 0));
  let rank = ''; if (!eday && r.majority && !r.for_predecessor_seat) { const all = ((S.data.elections || []).find(x => x.year === 2023) || {}).electorates || [];
    const ms = all.map(x => x.majority).filter(m => typeof m === 'number').sort((a, b) => a - b); const i = ms.indexOf(r.majority);
    if (i === 0) rank = 'the closest seat in the country in 2023'; else if (i > 0 && i < 10) rank = `the ${ordinal(i + 1)} closest of ${ms.length} seats in 2023` }
  const pred = r.for_predecessor_seat || (e.predecessor_seats || []).some(x => x !== e.name);
  const pv = Object.entries(r.party_vote_pct || {}).sort((a, b) => pname(a[0]).localeCompare(pname(b[0]), 'en-NZ'));
  const hist = elHistory(e);
  const resSum = r.winner ? `2023: ${esc(r.winner)} (${esc(pname(r.party))})${r.majority ? ` by ${Number(r.majority).toLocaleString('en-NZ')} votes` : ''}${pred ? ` in ${esc(r.seat || (e.predecessor_seats || []).join(', '))}` : ''}` : '';
  const links = [`<button class="rowlink rowlink--plain" type="button" aria-haspopup="dialog" data-page="electorates/${esc(e.slug)}.md"><span><span class="rowlink__title">Full electorate guide</span><span class="rowlink__sub" style="display:block">Everything we hold on ${esc(e.name)}, with sources.</span></span>${ic('chev')}</button>`,
    `<a class="rowlink rowlink--plain" href="#/seats/map/2023/${esc(e.slug)}"><span><span class="rowlink__title">See ${esc(e.name)} on the map</span><span class="rowlink__sub" style="display:block">Every election since 2011.</span></span>${ic('chev')}</a>`,
    e.map_pdf ? `<a class="rowlink rowlink--plain" href="${esc(e.map_pdf)}" target="_blank" rel="noopener"><span><span class="rowlink__title">Boundary map (PDF)</span><span class="rowlink__sub" style="display:block">The 2025 boundary review map, from elections.nz.</span></span>${ic('ext')}</a>` : ''].join('');
  return `<div class="found">
      <p class="eyebrow">${maori ? 'Māori electorate' : 'General electorate'}${e.region ? ' · ' + esc(e.region) : ''}</p>
      <h2>${esc(e.name)}</h2>
      ${e.boundary_status && /new|renamed|redrawn/i.test(e.boundary_status) ? `<p class="small muted">${esc(e.boundary_status)}</p>` : ''}
      ${e.sitting_mp ? `<p class="small"><b>Current MP:</b> ${esc(e.sitting_mp.name)} (${esc(pname(e.sitting_mp.party))})${e.mp_standing_again === false ? ', not standing again' : ''}.</p>` : ''}
      <p class="found__alt">${altLine}</p>
    </div>
    <div class="split split--7-5">
      <section class="stack" aria-labelledby="h-cands">
        <div class="shead__row"><h3 id="h-cands">On your ballot: ${cands.length} candidate${cands.length === 1 ? '' : 's'}</h3><span class="micro muted">Ballot order (A–Z by surname)</span></div>
        ${cands.length ? `<ul class="cands" role="list">${cands.map(candRow).join('')}</ul>` : '<p class="small muted">The candidate list for this electorate is still being checked.</p>'}
        <div class="row el-actions"><a class="btn" href="https://map.vote.nz" target="_blank" rel="noopener">${ic('pin', 'i--s')} Voting places near ${esc(e.name)} ${ic('ext', 'i--xs ext')}</a><button class="btn btn--quiet" type="button" id="el-print">${ic('print', 'i--s')} Print a one-pager</button>${cands.length > 1 ? `<button class="btn btn--quiet" type="button" id="el-compare" aria-haspopup="dialog">${ic('swap', 'i--s')} Compare candidates</button>` : ''}</div>
        <p class="micro muted">Candidates from policy.nz and party lists; the official list is on your EasyVote card and at vote.nz. You also have a party vote, for any party, wherever you live.</p>
      </section>
      <section class="stack stack--s el-more" aria-labelledby="h-elmore">
        <div class="shead shead--quiet"><h3 id="h-elmore" class="h4">More about ${esc(e.name)}</h3></div>
        ${e.contest_notes && !eday ? `<p class="small soft">${esc(e.contest_notes)}</p>` : ''}
        <div>
        ${r.winner ? `<details class="disclose" data-print><summary><span>${resSum}${rank ? `<span class="small muted el-sum">${esc(rank.charAt(0).toUpperCase() + rank.slice(1))}</span>` : ''}</span></summary><div class="disclose__body">
          ${r.majority ? `<div class="margin"><span class="figure">${Number(r.majority).toLocaleString('en-NZ')}</span><span><b>votes</b> between first and second${rank ? `<br>${rank}` : ''}</span></div>` : ''}
          ${top2.length ? `<div class="duel">${top2.map((c, i) => `<div class="duel__row" style="--pc:${pcolor(c.party)}"><span class="duel__name">${esc(c.name)} <span class="muted small" style="font-weight:500">${esc(pname(c.party))}</span></span><span class="duel__v">${fmt(c.pct, 1)}%</span><div class="bar"><i style="--w:${(c.pct || 0) / maxPct * 90}%;--i:${i}"></i></div></div>`).join('')}</div>` : `<p class="small">${esc(r.winner)} (${esc(pname(r.party))}) won.</p>`}
          ${pred ? `<p class="micro muted">Based on ${esc((e.predecessor_seats || []).join(', ') || r.seat || '')} before the 2025 boundary changes, so the 2026 contest is not directly comparable.</p>` : ''}
          <p class="src">${ic('doc')} ${r.source ? extA(r.source, 'Official count, as reported') : 'Official count, Electoral Commission'}</p>
        </div></details>` : ''}
        ${pv.length ? `<details class="disclose"><summary>Party vote in this area, 2023</summary><div class="disclose__body"><p class="micro muted">A–Z. ${esc(r.party_vote_basis || 'Official count')}.</p>${pv.map(([p, v], i) => `<div class="rrow" style="--pc:${pcolor(p)}"><span>${esc(pname(p))}</span><div class="bar"><i style="--w:${Math.min(100, v * 2)}%;--i:${i}"></i></div><span class="rrow__v">${fmt(v)}%</span></div>`).join('')}
          ${r.source ? `<p class="src">${ic('doc')} ${extA(r.source, 'Official count, as reported')}</p>` : ''}</div></details>` : ''}
        ${hist.length ? `<details class="disclose" data-print><summary>Who won here since 2011</summary><div class="disclose__body">
          <div class="history">${hist.map(h => `<div style="--pc:${pcolor(h.r.party)}"${h.year === 2023 ? ' aria-current="true"' : ''}><i></i><span>${h.year}</span><span>${esc(pname(h.r.party))}</span></div>`).join('')}</div>
          <p class="micro muted">${hist.map(h => `${h.year}: ${esc(h.r.winner)}${h.r.majority ? ` by ${Number(h.r.majority).toLocaleString('en-NZ')}` : ''}${elSlug(h.r.name) !== elSlug(e.name) ? ` (${esc(h.r.name)})` : ''}`).join(' · ')}.</p></div></details>` : ''}
        ${e.description ? `<details class="disclose"><summary>About ${esc(e.name)}</summary><div class="disclose__body"><p>${esc(e.description)}</p><p class="src">${ic('doc')} Description from policy.nz, quoted as published.</p>
          ${(e.description_fact_check || []).length ? `<div class="note note--warn">${ic('flag', 'i--s')}<div><b>Fact-check notes on this description</b><ul>${e.description_fact_check.map(f => `<li>${esc(typeof f === 'string' ? f : (f.note || f.correction || f.text || JSON.stringify(f)))}</li>`).join('')}</ul></div></div>` : ''}</div></details>` : ''}
        </div>
        <div class="rows el-links">${links}</div>
      </section>
    </div>` }

function compareCands(e) { const cands = (e.candidates || []).slice().sort(ballotSort);
  const rows = cands.map(c => { const p = findPerson(c.slug, c.name) || {};
    return `<tr><td><b>${esc(c.name)}</b></td><td><span class="sw" style="--pc:${pcolor(c.party)}"></span> ${esc(S.data.parties[c.party] ? pname(c.party) : (c.party_name || pname(c.party)))}</td><td class="n">${c.list_rank_2026 ? '#' + c.list_rank_2026 : 'Electorate only'}</td><td>${c.sitting_mp ? 'Sitting MP' : (p.parliaments || []).length ? 'Former MP' : 'No'}</td><td style="white-space:normal;min-width:12rem">${esc(p.before || '–')}</td></tr>` }).join('');
  openSheet({ title: `${e.name}: the candidates side by side`, depth: ['Electorate', 'Candidates', 'Compare'], at: 2, src: 'Ballot order (A–Z by surname). From policy.nz, party lists and the candidates’ own profiles.',
    html: `<div class="table-wrap"><table class="table"><thead><tr><th>Candidate</th><th>Party</th><th class="n">List place</th><th>Been an MP?</th><th>Before politics</th></tr></thead><tbody>${rows}</tbody></table></div>
      <p class="small muted">Tap a candidate on the page for their profile, in their own words where they’ve given them. To compare the parties’ policies, use <a href="#/choose/compare">Compare two parties</a>.</p>` }) }

function pickerSheet(cur) { const E = elList(); const grp = t => E.filter(e => (e.type || 'general') === t);
  openSheet({ title: 'Choose your electorate', depth: null, html: `<div class="input-icon">${ic('search', 'i--s')}<input class="input" type="search" id="el-sq" placeholder="Type an electorate, town or suburb" aria-label="Filter electorates" autocomplete="off"></div>
    ${['general', 'maori'].map(t => `<section class="stack stack--s" data-grp><h3 class="h4">${t === 'maori' ? 'Māori electorates' : 'General electorates'} <span class="num muted">${grp(t).length}</span></h3><div class="rows">${grp(t).map(e => `<a class="rowlink rowlink--plain" href="#/vote/electorate/${esc(e.slug)}" data-el-q="${esc((e.name + ' ' + (e.region || '')).toLowerCase())}" data-el-d="${esc((e.description || '').toLowerCase())}"${e.slug === cur ? ' aria-current="page"' : ''}><span><span class="rowlink__title">${esc(e.name)}</span><span class="rowlink__sub" style="display:block">${esc(e.region || '')}${e.region ? ' · ' : ''}${(e.candidates || []).length} candidates</span></span>${ic('chev')}</a>`).join('')}</div></section>`).join('')}` });
  const q = $('#el-sq'); if (q) q.oninput = () => { const v = q.value.trim().toLowerCase(); document.querySelectorAll('#sheet-body [data-el-q]').forEach(a => { a.hidden = !!v && !a.dataset.elQ.includes(v) && !(v.length >= 4 && a.dataset.elD.includes(v)) }) } }

function browseRows() { const E = elList();
  return ['general', 'maori'].map(t => { const L = E.filter(e => (e.type || 'general') === t);
    return `<section class="stack stack--s" aria-labelledby="h-b-${t}"><div class="shead shead--quiet"><div class="shead__row"><h3 id="h-b-${t}" class="h4">${t === 'maori' ? 'Māori electorates' : 'General electorates'}</h3><span class="micro muted">${L.length}, A–Z</span></div></div>
      <div class="rows">${L.map(e => `<a class="rowlink rowlink--plain" href="#/vote/electorate/${esc(e.slug)}"><span><span class="rowlink__title">${esc(e.name)}</span><span class="rowlink__sub" style="display:block">${esc(e.region || '')}${e.region ? ' · ' : ''}${(e.candidates || []).length} candidates</span></span>${ic('chev')}</a>`).join('')}</div></section>` }).join('') }

V.electorate = async slug => {
  await loadPeople(); const E = elList();
  const saved = store.get('myElectorate'); const sel = (slug && E.find(x => x.slug === slug)) || (!slug && saved && E.find(x => x.slug === saved)) || null;
  if (sel) store.set('myElectorate', sel.slug);
  const finder = `<div class="finder">
      <button class="btn btn--ink btn--l btn--block" type="button" id="el-loc">${ic('pin', 'i--s')} Use my location <span class="small" style="font-weight:500;opacity:.8">— stays on your device</span></button>
      <p class="micro muted">${ELEC_CONSENT}</p>
      <div id="el-loc-out" aria-live="polite"></div>
      <div class="finder__or">or</div>
      <div class="input-icon">${ic('search', 'i--s')}<input class="input" type="search" id="el-q" placeholder="Type your electorate, town or suburb" aria-label="Find your electorate by name, town or suburb" autocomplete="off" aria-controls="el-sugg"></div>
      <div class="rows el-sugg" id="el-sugg" hidden></div>
      <div class="row"><button class="chip chip--menu" type="button" id="el-all">${sel ? 'Choose a different electorate' : `All ${E.length} electorates`}</button><a class="small more" href="https://vote.nz" target="_blank" rel="noopener">Look up your address at vote.nz ${ic('ext', 'i--xs ext')}</a></div>
    </div>`;
  $('#main').innerHTML = sectionFrame('vote', 'vote/electorate', `<div class="stack stack--xl el-page">
    <div class="el-print-head"><p>Ballot Book NZ · independent guide, not the Electoral Commission · printed ${esc(nzDateLong())} · official information: vote.nz or 0800 36 76 56</p>
      ${sel ? `<figure class="el-qr"><img src="data/qr/${esc(sel.slug)}.svg" alt="QR code linking to this page" width="96" height="96"><figcaption>Scan for the latest: not-simon.github.io/Politicsnz</figcaption></figure>` : ''}</div>
    <header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('pin', 'i--s')} Vote · Your electorate</p><h1>Who’s standing where you live</h1>
      <p class="lede">Find your electorate to meet the candidates on your ballot, in ballot order, with how close it was last time.</p><div class="micro notec">${NOT_EC}</div></header>
    ${sel ? `<details class="disclose el-find"><summary>Not your electorate? Find yours</summary><div class="disclose__body"><div class="el-find__in">${finder}</div></div></details><div class="stack stack--l" id="el-body">${electorateBody(sel)}</div>`
      : `<div class="split split--5-7"><div class="stack sticky">${finder}</div><div class="stack stack--l"><div class="shead"><h2>Browse all ${E.length}</h2></div>${browseRows()}</div></div>`}
    ${OFFICIAL_LINE}
  </div>`);
  // typed picker: electorate names first, then electorates whose description mentions the place
  const q = $('#el-q'), sg = $('#el-sugg');
  q.oninput = () => { const v = q.value.trim().toLowerCase(); if (v.length < 2) { sg.hidden = true; sg.innerHTML = ''; return }
    const byName = E.filter(e => e.name.toLowerCase().includes(v) || elSlug(e.name).includes(elSlug(v)));
    const byText = byName.length && v.length < 6 ? [] : E.filter(e => !byName.includes(e) && ((e.region || '').toLowerCase().includes(v) || (v.length >= 4 && (e.description || '').toLowerCase().includes(v)))).slice(0, 6);
    const row = (e, why) => `<a class="rowlink rowlink--plain" href="#/vote/electorate/${esc(e.slug)}"><span><span class="rowlink__title">${esc(e.name)}</span><span class="rowlink__sub" style="display:block">${why}</span></span>${ic('chev')}</a>`;
    sg.innerHTML = byName.slice(0, 8).map(e => row(e, `${e.type === 'maori' ? 'Māori' : 'General'} electorate · ${(e.candidates || []).length} candidates`)).join('')
      + (byText.length ? `<p class="micro muted el-sugg__h">Mentions “${esc(q.value.trim())}”: boundaries can split a town, so check at vote.nz</p>` + byText.map(e => row(e, esc(e.region || 'Mentioned in its description'))).join('') : '')
      || `<p class="small muted el-sugg__h">No electorate matches. Try the list, or look up your address at vote.nz.</p>`;
    sg.hidden = false };
  q.onkeydown = e => { if (e.key === 'Enter') { const a = sg.querySelector('a'); if (a) { e.preventDefault(); go(a.getAttribute('href')) } } };
  $('#el-all').onclick = () => pickerSheet(sel && sel.slug);
  // location (device-side only; uses the shared locateElectorate())
  $('#el-loc').onclick = async () => { const out = $('#el-loc-out'); out.innerHTML = '<p class="small muted">Finding your electorate…</p>';
    try { const r = await locateElectorate(); if (!r.general && !r.maori) { out.innerHTML = '<p class="small">That location is outside New Zealand’s electorates. Choose from the list instead.</p>'; return }
      S.locHit = { general: r.general || null, maori: r.maori || null, accuracy: r.accuracy };
      const g = featToElectorate(r.general), m = featToElectorate(r.maori);
      const warn = r.accuracy > 2000 ? `<p class="micro muted">Location accuracy is about ${Math.round(r.accuracy / 1000)} km, so near a boundary the result may be wrong; check your address at vote.nz.</p>` : '';
      if (g) { if (warn) S.locWarn = warn; go('#/vote/electorate/' + g.slug); return }
      out.innerHTML = `<p class="small">You’re in the <b>${esc(r.general ? r.general.properties.name : '–')}</b> general electorate${r.maori ? ` and the <b>${esc(r.maori.properties.name)}</b> Māori electorate` : ''}.</p>${m ? `<a class="btn btn--s" href="#/vote/electorate/${esc(m.slug)}">${esc(m.name)}</a>` : ''}${warn}` }
    catch (err) { out.innerHTML = `<p class="small">Couldn’t get your location (${esc(err && err.message || 'permission denied')}). Pick your electorate from the list instead, or look up your address at vote.nz.</p>` } };
  if (S.locWarn && sel) { $('#el-loc-out').innerHTML = S.locWarn; const d = $('.el-find'); if (d) d.open = true; S.locWarn = null }
  if (!sel) return;
  const body = $('#el-body');
  body.addEventListener('click', ev => { const b = ev.target.closest('[data-cand]'); if (!b) return; const p = findPerson(b.dataset.cand, b.dataset.cname); if (p) openPerson(p);
    else openSheet({ title: b.dataset.cname, html: '<p class="small muted">We don’t have a profile for this candidate yet. Their party’s website, policy.nz and vote.nz list the candidates standing.</p>' }) });
  // the one-pager prints the 2023 result and the seat's history even when those blocks are closed on screen
  $('#el-print').onclick = () => { const shut = [...body.querySelectorAll('.disclose[data-print]:not([open])')]; shut.forEach(d => { d.open = true });
    const back = () => { shut.forEach(d => { d.open = false }); removeEventListener('afterprint', back) }; addEventListener('afterprint', back); window.print() };
  const cmp = $('#el-compare'); if (cmp) cmp.onclick = () => compareCands(sel);
};
