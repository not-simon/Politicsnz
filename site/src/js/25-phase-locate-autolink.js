/* ----- election phase (NZ time) ----- */
function nzNow() { return new Date(new Date().toLocaleString('en-US', { timeZone: 'Pacific/Auckland' })) }
function electionPhase() { const t = nzNow(); const d = t.getFullYear() * 10000 + (t.getMonth() + 1) * 100 + t.getDate();
  if (d < 20261026) return 'enrol'; if (d < 20261107) return 'advance'; if (d === 20261107) return t.getHours() < 19 ? 'electionday' : 'results'; return 'after' }
const ELECTION_DAY_BLOCK = 'Today is election day. By law, material that could influence how people vote can’t be published until voting closes at 7pm, so the match quiz, swipe, compass, game, polls, forecast and party newsroom are hidden until then. Voting places are open 9am–7pm.';
function renderBanner() { const ph = electionPhase(); let el = $('#banner'); if (!el) { el = document.createElement('div'); el.id = 'banner'; el.className = 'banner'; document.querySelector('header.top').after(el) }
  const key = 'banner-' + ph; if (store.get(key) === 'x') { el.hidden = true; return }
  const msg = { enrol: 'Enrolment closes <b>midnight Sunday 25 October</b>. There is no enrolling on election day this year. <a href="https://vote.nz" target="_blank" rel="noopener">Check or update your enrolment at vote.nz</a>.',
    advance: 'Voting is open. Vote early at any voting place until 6 November, or on election day Saturday 7 November (9am–7pm). <a href="https://vote.nz" target="_blank" rel="noopener">Find a voting place</a>.',
    electionday: 'Election day: voting places are open 9am–7pm. Polls, forecasts, quiz results and the game are hidden until 7pm.',
    results: 'Voting has closed. Preliminary results are being counted; official results on 27 November.', after: '' }[ph];
  if (!msg) { el.hidden = true; return } el.hidden = false; el.innerHTML = `<div class="wrap"><span>${msg}</span><button aria-label="Dismiss" id="banner-x">×</button></div>`; $('#banner-x').onclick = () => { store.set(key, 'x'); el.hidden = true } }
function blockedToday(view) { return electionPhase() === 'electionday' && ['match', 'compass', 'swipe', 'swipe-tally', 'polls', 'trends', 'game', 'newsroom'].includes(view) }
const BLOCKED_PAGES = /^(REPORT\.md|elections\/2026\.md|elections\/trends\.md|guide\/parties\.md|guide\/forecast-method\.md|guide\/quiz-method\.md|guide\/quiz-research\.md|guide\/compass-method\.md)$/;
function blockedPage(k) { return electionPhase() === 'electionday' && BLOCKED_PAGES.test(k) }
const isElectionDay = () => electionPhase() === 'electionday';
const RESULT_DISCLAIMER = `<p class="small muted" style="border-top:1px solid var(--line);padding-top:10px">This shows how closely your answers line up with each party's published positions on the questions you answered. It is information, not advice: it does not take account of candidates, coalitions, trust, or the issues we did not ask about, and it is not a recommendation about how to vote. Every party is listed. Read the party pages and the original policy texts before deciding. Ballot Book NZ is independent and not affiliated with any party, candidate or the Electoral Commission.</p>`;
const NOT_EC = `<p class="tiny muted">Independent and non-partisan. Not the Electoral Commission: for official information on enrolling, voting places and hours, go to <a href="https://vote.nz" target="_blank" rel="noopener">vote.nz</a> or call 0800 36 76 56.</p>`;

/* ----- find my electorate from location (device-side only) ----- */
function pointInRing(pt, ring) { let inside = false; const [x, y] = pt; for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) { const [xi, yi] = ring[i], [xj, yj] = ring[j]; if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) inside = !inside } return inside }
function featureContains(f, lon, lat) { const polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates; for (const poly of polys) { if (pointInRing([lon, lat], poly[0])) { for (let k = 1; k < poly.length; k++) if (pointInRing([lon, lat], poly[k])) return false; return true } } return false }
async function locateElectorate() { if (!navigator.geolocation) throw new Error('Your browser does not offer location.');
  const pos = await new Promise((ok, no) => navigator.geolocation.getCurrentPosition(ok, no, { enableHighAccuracy: false, timeout: 12000, maximumAge: 300000 }));
  let { longitude: lon, latitude: lat } = pos.coords; if (lon < 0) lon += 360;
  await loadGeo(2025); const hit = t => (S.geo[`${t}-2025`].features || []).find(f => featureContains(f, lon, lat));
  return { general: hit('general'), maori: hit('maori'), accuracy: pos.coords.accuracy } }
function locateBlock(id) { return `<div class="card locate" id="${id}"><div class="row" style="justify-content:space-between"><div><h3>Where do you live?</h3><p class="small muted">Use your location to find your electorate and the people standing there. Your browser will ask for permission. Your location is checked against the electorate map on this device only; it is not stored or sent anywhere. You can also just choose your electorate from the list.</p></div><button class="btn primary sm" data-locate="${id}">Use my location</button></div><div class="found" id="${id}-out"></div></div>` }
async function runLocate(id) { const out = $('#' + id + '-out'); out.innerHTML = '<span class="muted small">Finding your electorate…</span>';
  try { const r = await locateElectorate(); if (!r.general && !r.maori) { out.innerHTML = '<span class="small">That location is outside New Zealand’s electorates.</span>'; return }
    const E = S.data.electorates || []; const link = f => { const e = E.find(x => slugify(x.slug) === f.properties.slug || slugify(x.name) === f.properties.slug); return e ? `<button class="btn sm" data-go="electorate-${esc(e.slug)}">${esc(f.properties.name)} · ${(e.candidates || []).length} candidates</button>` : `<b>${esc(f.properties.name)}</b>` };
    out.innerHTML = `<p class="small">You're in the <b>${r.general ? esc(r.general.properties.name) : '–'}</b> general electorate${r.maori ? ` and the <b>${esc(r.maori.properties.name)}</b> Māori electorate` : ''}. Which one you vote in depends on which roll you're on.</p><div class="row">${r.general ? link(r.general) : ''}${r.maori ? link(r.maori) : ''}</div>${r.accuracy > 2000 ? `<p class="tiny muted">Location accuracy is about ${Math.round(r.accuracy / 1000)} km, so near a boundary the result may be wrong; check at vote.nz.</p>` : ''}` }
  catch (e) { out.innerHTML = `<span class="small">Couldn't get your location (${esc(e.message || 'permission denied')}). Pick your electorate from the list instead, or look up your address at vote.nz.</span>` } }

/* ----- auto-link party and politician names in text ----- */
function buildLinker() { if (S.linker !== undefined) return S.linker; const names = [];
  for (const [slug, p] of Object.entries(S.data.parties)) { for (const n of [p.name, p.short]) if (n && n.length > 3 && !/^(Independent|Other)$/i.test(n)) names.push([n, 'party-' + slug]) }
  for (const p of (S.people || [])) if (p.name && p.name.trim().split(/\s+/).length >= 2) names.push([p.name, 'person:' + p.folder]);
  names.sort((a, b) => b[0].length - a[0].length); const map = Object.fromEntries(names);
  const re = new RegExp('(?<![\\w-])(' + names.map(([n]) => n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')(?![\\w-])', 'g');
  S.linker = names.length ? { re, map } : null; return S.linker }
function autolink(root) { const L = buildLinker(); if (!L || !root) return; const skip = 'A, BUTTON, H1, H2, H3, H4, .nm, .st, .who, .pcard, .person, .seatcard, .match, .scard, .legend, .tabs, select, input, code, pre';
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: n => (n.nodeValue.trim().length > 3 && !n.parentElement.closest(skip)) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT });
  const nodes = []; while (walker.nextNode()) nodes.push(walker.currentNode);
  for (const n of nodes) { L.re.lastIndex = 0; if (!L.re.test(n.nodeValue)) continue; const frag = document.createDocumentFragment(); let last = 0; L.re.lastIndex = 0; let m;
    while ((m = L.re.exec(n.nodeValue))) { frag.appendChild(document.createTextNode(n.nodeValue.slice(last, m.index))); const b = document.createElement('button'); b.className = 'lnk'; b.type = 'button'; b.textContent = m[0];
      const t = L.map[m[0]]; if (t.startsWith('person:')) b.dataset.person = t.slice(7); else b.dataset.go = t; frag.appendChild(b); last = m.index + m[0].length }
    frag.appendChild(document.createTextNode(n.nodeValue.slice(last))); n.parentNode.replaceChild(frag, n) } }

/* ----- export / import saved results ----- */
const SAVE_KEYS = ['quiz', 'quiz2', 'compass', 'swipe', 'myElectorate', 'bb-theme'];
function exportSaved() { const o = {}; for (const k of SAVE_KEYS) { const v = store.get(k); if (v) o[k] = v } return btoa(unescape(encodeURIComponent(JSON.stringify(o)))) }
function importSaved(code) { const o = JSON.parse(decodeURIComponent(escape(atob(code.trim())))); for (const [k, v] of Object.entries(o)) if (SAVE_KEYS.includes(k)) store.set(k, v) }
