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

/* Typed electorate search. Folds macrons both ways (Otaki = Ōtaki) and common alternative spellings (Mt/Mount, Pt/Port,
   St/Saint, Wanganui/Whanganui), then matches electorate names, the seats they replaced in 2025, and regions. It never
   guesses from description text, so a suburb that isn't an electorate name gets an honest "no electorate called …". */
const EL_ALIAS = { mt: 'mount', pt: 'port', st: 'saint', wanganui: 'whanganui', chch: 'christchurch', palmy: 'palmerston north', welly: 'wellington', akl: 'auckland' };
const elFold = v => String(v || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[’'`]/g, '').replace(/[^a-z0-9]+/g, ' ').trim()
  .split(' ').filter(Boolean).map(w => EL_ALIAS[w] || w).join(' ');
const elRegions = e => String(e.region || '').replace(/\(.*?\)/g, '').split('/').map(x => x.trim()).filter(Boolean);
// score: 4 exact, 3 starts with, 2 a word starts with, 1 contains (3+ letters); 0 no match
function elScore(hay, q) { const h = elFold(hay); if (!h || !q) return 0; if (h === q) return 4; if (h.startsWith(q)) return 3;
  if ((' ' + h).includes(' ' + q)) return 2; return q.length >= 3 && h.includes(q) ? 1 : 0 }
function elSearch(raw, E = elList()) { const q = elFold(raw); if (q.length < 2) return null;
  const by = (fn) => E.map(e => ({ e, s: fn(e) })).filter(x => x.s > 0).sort((a, b) => b.s - a.s || a.e.name.localeCompare(b.e.name, 'en-NZ')).map(x => x.e);
  const byName = by(e => elScore(e.name, q));
  const formerOf = e => (e.predecessor_seats || []).filter(n => elFold(n) !== elFold(e.name));
  const byFormer = by(e => byName.includes(e) ? 0 : Math.max(0, ...formerOf(e).map(n => elScore(n, q))));
  const formerHit = e => formerOf(e).find(n => elScore(n, q) > 0);
  const byRegion = by(e => byName.includes(e) || byFormer.includes(e) ? 0 : Math.max(0, ...elRegions(e).map(r => elScore(r, q))));
  const regionHit = e => elRegions(e).find(r => elScore(r, q) > 0);
  return { q, byName, byFormer, formerHit, byRegion, regionHit } }
function elSuggHTML(raw) { const R = elSearch(raw); if (!R) return '';
  const typ = e => `${e.type === 'maori' ? 'Māori' : 'General'} electorate`; const nc = e => `${(e.candidates || []).length} candidates`;
  const row = (e, why) => `<a class="rowlink rowlink--plain" href="#/vote/electorate/${esc(e.slug)}"><span><span class="rowlink__title">${esc(e.name)}</span><span class="rowlink__sub" style="display:block">${why}</span></span>${ic('chev')}</a>`;
  let h = R.byName.slice(0, 8).map(e => row(e, `${typ(e)} · ${nc(e)}`)).join('');
  if (R.byFormer.length) h += `<p class="micro muted el-sugg__h">${R.byName.length ? 'Former electorates' : `${esc(R.formerHit(R.byFormer[0]))} is no longer an electorate`}: since the 2025 boundary changes, the area is in</p>` + R.byFormer.map(e => row(e, `Includes part of the former ${esc(R.formerHit(e))} electorate · ${nc(e)}`)).join('');
  if (R.byRegion.length) { const rg = R.regionHit(R.byRegion[0]);
    h += `<p class="micro muted el-sugg__h">${R.byRegion.length} electorate${R.byRegion.length === 1 ? '' : 's'} in ${esc(rg)}, A–Z. Boundaries can split a town, so check your address at vote.nz.</p>` + R.byRegion.slice().sort((a, b) => a.name.localeCompare(b.name, 'en-NZ')).map(e => row(e, `${typ(e)} · ${esc(String(e.region || '').replace(/\s*\(Māori electorate\)\s*/i, ''))}`)).join('') }
  if (R.byFormer.length || R.byRegion.length) h += `<p class="micro muted el-sugg__h">Boundaries changed in 2025. If you’re not sure, <a href="https://vote.nz" target="_blank" rel="noopener">look up your address at vote.nz</a>.</p>`;
  return h || `<p class="small el-sugg__h el-sugg__none">No electorate called “${esc(String(raw).trim())}”. Try your town or region, or <button class="linkbtn" type="button" data-el-useloc>use your location</button>. You can also <a href="https://vote.nz" target="_blank" rel="noopener">look up your address at vote.nz</a>.</p>` }

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

// party name for a candidate, linked to its party page whenever the guide has one (every party, not just some)
function candPartyTag(c, cls = 'ptag ptag--s ptag--wrap') { const has = !!(S.data.parties[c.party] || (typeof guideParty === 'function' && guideParty(c.party)));
  const name = esc(has ? (P(c.party).name || pname(c.party)) : (c.party_name || pname(c.party)));
  return has && c.party !== 'independent' ? `<a class="${cls}" style="--pc:${pcolor(c.party)}" href="#/parties/${esc(c.party)}"><span class="sw"></span>${name}</a>`
    : `<span class="${cls}" style="--pc:${pcolor(c.party)}"><span class="sw"></span>${name}</span>` }
const firstSentence = t => { const m = String(t || '').trim().match(/^[\s\S]*?(?<!\b(?:Dr|Mr|Mrs|Ms|St|Mt|Prof|Hon|No))[.!?](?=\s+[A-ZĀĒĪŌŪ"“‘(]|$)/); const s = (m ? m[0] : String(t || '').trim()); return s.length > 220 ? s.slice(0, 217).replace(/\s+\S*$/, '') + '…' : s };
function compareCands(e) { const cands = (e.candidates || []).slice().sort(ballotSort);
  const card = c => { const p = findPerson(c.slug, c.name);
    const rank = c.list_rank_2026 || (p && p.list_rank_2026);
    const status = [c.sitting_mp ? 'Sitting MP' : p && (p.parliaments || []).length ? 'Former MP' : '', rank ? 'Electorate and party list' : 'Electorate only'].filter(Boolean).join(' · ');
    const why = p && p.why ? firstSentence(p.why) : '';
    return `<li class="ccard">${candFace(c)}<div class="ccard__body">
      <h3 class="ccard__name">${esc(c.name)}</h3>
      <dl class="ccard__dl">
        <dt>Party</dt><dd>${candPartyTag(c)}</dd>
        <dt>List place</dt><dd>${rank ? `#${esc(rank)}` : '<span class="muted">Not on the list</span>'}</dd>
        <dt>Standing as</dt><dd>${esc(status)}</dd>
        <dt>Before politics</dt><dd>${p && p.before ? esc(p.before) : '<span class="muted">Not given</span>'}</dd>
        <dt>In their words</dt><dd>${why ? `“${esc(why)}”` : '<span class="muted">No statement given to us</span>'}</dd>
      </dl>
      ${p ? `<button class="linkbtn small" type="button" data-cmp-person="${esc(p.folder)}">Full profile: ${esc(c.name)}</button>` : '<span class="micro muted">No profile yet. Their party’s website, policy.nz and vote.nz list the candidates.</span>'}
    </div></li>` };
  openSheet({ title: `${e.name}: the candidates side by side`, depth: ['Electorate', 'Candidates', 'Compare'], at: 2, src: 'Ballot order (A–Z by surname). From policy.nz, party lists and the candidates’ own profiles; “in their words” is the first sentence of their own statement.',
    html: `<p class="small muted">${cands.length} candidates, in ballot order. The same five things for each.</p><ul class="ccards" role="list">${cands.map(card).join('')}</ul>
      <p class="small muted">To compare the parties’ policies, use <a href="#/choose/compare">Compare two parties</a>.</p>` });
  const box = $('#sheet-body .ccards'); if (box) box.addEventListener('click', ev => { const b = ev.target.closest('[data-cmp-person]'); if (!b) return; const p = (S.people || []).find(x => x.folder === b.dataset.cmpPerson); if (p) openPerson(p) }) }

function pickerSheet(cur) { const E = elList(); const grp = t => E.filter(e => (e.type || 'general') === t);
  openSheet({ title: 'Choose your electorate', depth: null, html: `<div class="input-icon">${ic('search', 'i--s')}<input class="input" type="search" id="el-sq" placeholder="Type an electorate, town or region" aria-label="Filter electorates" autocomplete="off"></div><p class="small" id="el-sq-none" role="status" hidden></p>
    ${['general', 'maori'].map(t => `<section class="stack stack--s" data-grp><h3 class="h4">${t === 'maori' ? 'Māori electorates' : 'General electorates'} <span class="num muted">${grp(t).length}</span></h3><div class="rows">${grp(t).map(e => `<a class="rowlink rowlink--plain" href="#/vote/electorate/${esc(e.slug)}" data-el-q="${esc([e.name, ...(e.predecessor_seats || []), ...elRegions(e)].map(elFold).join('|'))}"${e.slug === cur ? ' aria-current="page"' : ''}><span><span class="rowlink__title">${esc(e.name)}</span><span class="rowlink__sub" style="display:block">${esc(e.region || '')}${e.region ? ' · ' : ''}${(e.candidates || []).length} candidates</span></span>${ic('chev')}</a>`).join('')}</div></section>`).join('')}` });
  const q = $('#el-sq'); if (q) q.oninput = () => { const v = elFold(q.value); let n = 0;
    document.querySelectorAll('#sheet-body [data-el-q]').forEach(a => { const on = v.length < 2 || a.dataset.elQ.split('|').some(h => elScore(h, v) > 0); a.hidden = !on; if (on) n++ });
    document.querySelectorAll('#sheet-body [data-grp]').forEach(g => { g.hidden = !g.querySelector('[data-el-q]:not([hidden])') });
    const none = $('#el-sq-none'); if (none) { none.hidden = n > 0; none.textContent = n ? '' : `No electorate called “${q.value.trim()}”. Try your town or region, or use your location on the electorate page.` } } }

function browseRows() { const E = elList();
  return ['general', 'maori'].map(t => { const L = E.filter(e => (e.type || 'general') === t);
    return `<section class="stack stack--s" aria-labelledby="h-b-${t}"><div class="shead shead--quiet"><div class="shead__row"><h3 id="h-b-${t}" class="h4">${t === 'maori' ? 'Māori electorates' : 'General electorates'}</h3><span class="micro muted">${L.length}, A–Z</span></div></div>
      <div class="rows">${L.map(e => `<a class="rowlink rowlink--plain" href="#/vote/electorate/${esc(e.slug)}"><span><span class="rowlink__title">${esc(e.name)}</span><span class="rowlink__sub" style="display:block">${esc(e.region || '')}${e.region ? ' · ' : ''}${(e.candidates || []).length} candidates</span></span>${ic('chev')}</a>`).join('')}</div></section>` }).join('') }

V.electorate = async slug => {
  await loadPeople(); const E = elList();
  const saved = store.get('myElectorate'); const sel = (slug && E.find(x => x.slug === slug)) || (!slug && saved && E.find(x => x.slug === saved)) || null;
  if (sel) store.set('myElectorate', sel.slug);
  const finder = `<div class="finder" role="search" aria-label="Find your electorate">
      <div class="input-icon el-qwrap">${ic('search', 'i--s')}<input class="input" type="search" id="el-q" placeholder="Type your electorate, town or region" aria-label="Find your electorate by name, town or region" autocomplete="off" aria-controls="el-sugg"></div>
      <div class="rows el-sugg" id="el-sugg" aria-live="polite" hidden></div>
      <div class="finder__or">or</div>
      <button class="btn btn--ink btn--l btn--block" type="button" id="el-loc">${ic('pin', 'i--s')} Use my location <span class="small" style="font-weight:500;opacity:.8">— stays on your device</span></button>
      <p class="micro muted">${ELEC_CONSENT}</p>
      <div id="el-loc-out" aria-live="polite"></div>
      <div class="row"><button class="chip chip--menu" type="button" id="el-all">${sel ? 'Choose a different electorate' : `All ${E.length} electorates`}</button><a class="small more" href="https://vote.nz" target="_blank" rel="noopener">Look up your address at vote.nz ${ic('ext', 'i--xs ext')}</a></div>
    </div>`;
  $('#main').innerHTML = sectionFrame('vote', 'vote/electorate', `<div class="stack stack--xl el-page">
    <div class="el-print-head"><p>Ballot Book NZ · independent guide, not the Electoral Commission · printed ${esc(nzDateLong())} · official information: vote.nz or 0800 36 76 56</p>
      ${sel ? `<figure class="el-qr"><img src="data/qr/${esc(sel.slug)}.svg" alt="QR code linking to this page" width="96" height="96"><figcaption>Scan for the latest: not-simon.github.io/Politicsnz</figcaption></figure>` : ''}</div>
    <header class="pagehead el-head"><p class="eyebrow eyebrow--signal">${ic('pin', 'i--s')} Vote · Your electorate</p><h1>Who’s standing where you live</h1></header>
    ${sel ? `<div class="stack stack--s"><details class="disclose el-find"><summary>Not your electorate? Find yours</summary><div class="disclose__body"><div class="el-find__in">${finder}</div></div></details><div class="micro notec">${NOT_EC}</div></div><div class="stack stack--l" id="el-body">${electorateBody(sel)}</div>`
      : `<div class="split split--5-7 el-top"><div class="stack sticky">${finder}<p class="small soft el-lede">Find your electorate to meet the candidates on your ballot, in ballot order, with how close it was last time.</p><div class="micro notec">${NOT_EC}</div></div><div class="stack stack--l"><div class="shead"><h2>Browse all ${E.length}</h2></div>${browseRows()}</div></div>`}
    ${OFFICIAL_LINE}
  </div>`);
  // typed picker: electorate names, then the seats they replaced in 2025, then regions (never description text)
  const q = $('#el-q'), sg = $('#el-sugg');
  q.oninput = () => { const h = elSuggHTML(q.value); sg.innerHTML = h; sg.hidden = !h; if (h) keepSearchInView() };
  // on a phone the keyboard covers the lower half of the screen: bring the field (and the results under it) to the top
  const keepSearchInView = () => { if (innerWidth >= 720) return; const r = q.getBoundingClientRect(); const mh = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--mast-h')) || 56;
    if (r.top < mh + 8 || r.top > innerHeight * 0.3) scrollTo({ top: scrollY + r.top - mh - 12, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }) };
  q.onfocus = () => setTimeout(keepSearchInView, 60);
  q.onkeydown = e => { if (e.key === 'Enter') { const a = sg.querySelector('a.rowlink'); if (a) { e.preventDefault(); go(a.getAttribute('href')) } } };
  sg.addEventListener('click', e => { if (e.target.closest('[data-el-useloc]')) $('#el-loc').click() });
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
