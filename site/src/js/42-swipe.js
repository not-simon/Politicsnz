/* ----- policy swipe ----- */
function swipeState() { try { return JSON.parse(store.get('swipe') || '{}') } catch { return {} } }
function saveSwipe(st) { store.set('swipe', JSON.stringify(st)) }
function buildDeck(cards, done, topic) {
  const pool = cards.filter(c => !done[c.id] && (!topic || c.topic === topic));
  const byParty = {}; pool.forEach(c => (byParty[c.party] = byParty[c.party] || []).push(c));
  Object.values(byParty).forEach(a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]] } });
  const deck = [];
  while (deck.length < pool.length) { // weighted round-robin so no party floods the deck
    const live = Object.keys(byParty).filter(p => byParty[p].length); if (!live.length) break;
    const tot = live.reduce((a, p) => a + byParty[p][0].weight, 0); let r = Math.random() * tot, pick = live[0];
    for (const p of live) { r -= byParty[p][0].weight; if (r <= 0) { pick = p; break } }
    deck.push(byParty[pick].shift()) }
  return deck;
}
V.swipe = async () => {
  if (!S.swipe) S.swipe = await getJSON('data/swipe.json').catch(() => []);
  await loadPeople();
  const st = swipeState(); st.done = st.done || {}; const topic = st.topic || '';
  const deck = buildDeck(S.swipe, st.done, topic); let i = 0; let revealed = false;
  const nDone = Object.keys(st.done).length;
  $('#main').innerHTML = `<section class="view"><div class="swipe-wrap">
    <div class="tallybar"><div><div class="kicker">Policy swipe</div><h2 style="font-size:24px">Agree or disagree?</h2></div>
      <div class="row"><select id="sw-topic" aria-label="Topic"><option value="">All topics</option>${Object.entries(TOPIC_NAMES).map(([t, n]) => `<option value="${t}" ${t === topic ? 'selected' : ''}>${n}</option>`).join('')}</select>
      <button class="btn sm" data-go="swipe-tally">Your tally${nDone ? ` (${nDone})` : ''}</button></div></div>
    <p class="small muted" style="margin-top:-6px">Real 2026 policies, one at a time, with no party named. Decide first; then see whose it is. Swipe right to agree, left to disagree.</p>
    <div class="stage" id="stage"></div>
    <div class="swipe-actions" id="acts"><button class="big no" id="sw-no">✕ Disagree</button><button class="btn sm" id="sw-skip">Skip</button><button class="big yes" id="sw-yes">✓ Agree</button></div>
    <p class="tiny muted" style="text-align:center">${deck.length} policies left in this deck. Summaries are the party's own policy described neutrally; tap "Read the full policy" after revealing.</p></div></section>`;
  const stage = $('#stage');
  const cardHTML = (c, cls) => `<article class="scard ${cls}" data-id="${esc(c.id)}"><span class="stamp yes">AGREE</span><span class="stamp no">DISAGREE</span>
    <div class="tiny muted">${esc(TOPIC_NAMES[c.topic] || 'Other')}</div><div class="stmt">${esc(c.statement)}</div>
    <div class="body">${c.how ? `<div><b>What it would do</b><div>${esc(c.how)}</div></div>` : ''}${c.why ? `<div><b>The reasoning given</b><div>${esc(c.why)}</div></div>` : ''}</div></article>`;
  const render = () => { revealed = false;
    if (i >= deck.length) { stage.innerHTML = `<div class="scard" style="position:relative;place-items:center;text-align:center"><h3>You've seen every card${topic ? ' on this topic' : ''}.</h3><p class="muted">Change the topic, or look at your tally.</p><button class="btn primary" data-go="swipe-tally">See your tally</button></div>`; $('#acts').hidden = true; return }
    $('#acts').hidden = false;
    stage.innerHTML = (deck[i + 2] ? cardHTML(deck[i + 2], 'back2') : '') + (deck[i + 1] ? cardHTML(deck[i + 1], 'back') : '') + cardHTML(deck[i], 'top');
    attachDrag(stage.querySelector('.top')) };
  const decide = (verdict) => { if (revealed) return; const c = deck[i]; if (!c) return;
    if (verdict !== 'skip') { st.done[c.id] = { v: verdict, party: c.party, t: Date.now() }; saveSwipe(st) } else { st.done[c.id] = { v: 'skip', party: c.party, t: Date.now() }; saveSwipe(st) }
    const top = stage.querySelector('.top'); if (top) { top.classList.add('fly'); top.style.transform = verdict === 'agree' ? 'translateX(130%) rotate(16deg)' : verdict === 'disagree' ? 'translateX(-130%) rotate(-16deg)' : 'translateY(-120%)'; top.style.opacity = '0' }
    setTimeout(() => verdict === 'skip' ? (i++, render()) : reveal(c, verdict), 260) };
  const reveal = (c, verdict) => { revealed = true; $('#acts').hidden = true;
    const faces = leaderFaces(c.party); const tally = tallyFor(st, c.party);
    stage.innerHTML = `<article class="scard reveal" style="position:relative;--pc:${pcolor(c.party)}"><div class="row" style="justify-content:space-between"><span class="verdict-pill" style="background:${verdict === 'agree' ? 'var(--v-kept)' : 'var(--v-broken)'}">${verdict === 'agree' ? '✓ You agreed' : '✕ You disagreed'}</span><span class="tiny muted">${esc(TOPIC_NAMES[c.topic] || 'Other')}</span></div>
      <div class="row" style="gap:12px">${faces.length ? `<span class="faces">${faces.slice(0, 2).map(f => faceHTML(f, c.party)).join('')}</span>` : `<span class="mono" style="--pc:${pcolor(c.party)}">${esc(initials(c.party))}</span>`}<div><div class="tiny muted">This is a policy of</div><h3>${esc(P(c.party).name)}</h3></div></div>
      <div class="stmt" style="font-size:19px">${esc(c.statement)}</div>
      <p class="small muted">So far you've agreed with <b>${tally.agree}</b> of the <b>${tally.n}</b> ${esc(pname(c.party))} policies you've seen.</p>
      <div class="row">${c.doc ? `<button class="btn sm" data-doc="${esc(c.party)}|${esc(c.doc)}">Read the full policy</button>` : ''}<button class="btn sm" data-go="party-${esc(c.party)}">About this party</button><button class="btn primary" id="sw-next" style="margin-left:auto">Next →</button></div></article>`;
    $('#sw-next').onclick = () => { i++; render() } };
  function attachDrag(el) { if (!el) return; let x0 = null, dx = 0;
    const yes = el.querySelector('.stamp.yes'), no = el.querySelector('.stamp.no');
    el.addEventListener('pointerdown', e => { x0 = e.clientX; el.setPointerCapture(e.pointerId); el.classList.add('dragging') });
    el.addEventListener('pointermove', e => { if (x0 == null) return; dx = e.clientX - x0; el.style.transform = `translateX(${dx}px) rotate(${dx / 18}deg)`; yes.style.opacity = Math.min(1, Math.max(0, dx / 90)); no.style.opacity = Math.min(1, Math.max(0, -dx / 90)) });
    const end = () => { if (x0 == null) return; el.classList.remove('dragging'); x0 = null;
      if (dx > 100) decide('agree'); else if (dx < -100) decide('disagree'); else { el.style.transform = ''; yes.style.opacity = 0; no.style.opacity = 0 } dx = 0 };
    el.addEventListener('pointerup', end); el.addEventListener('pointercancel', end) }
  $('#sw-yes').onclick = () => decide('agree'); $('#sw-no').onclick = () => decide('disagree'); $('#sw-skip').onclick = () => decide('skip');
  $('#sw-topic').onchange = () => { st.topic = $('#sw-topic').value; saveSwipe(st); V.swipe() };
  S.swipeKeys && document.removeEventListener('keydown', S.swipeKeys);
  S.swipeKeys = e => { if (S.route !== 'swipe' || $('#dlg').open) return; if (e.key === 'ArrowRight') decide('agree'); if (e.key === 'ArrowLeft') decide('disagree'); if (e.key === 'ArrowUp') decide('skip'); if (e.key === 'Enter' && revealed) { i++; render() } };
  document.addEventListener('keydown', S.swipeKeys);
  render();
};
function tallyFor(st, party) { let n = 0, agree = 0; for (const d of Object.values(st.done || {})) if (d.party === party && d.v !== 'skip') { n++; if (d.v === 'agree') agree++ } return { n, agree } }
V['swipe-tally'] = async () => {
  if (!S.swipe) S.swipe = await getJSON('data/swipe.json').catch(() => []);
  const st = swipeState(); const done = st.done || {}; const byId = Object.fromEntries(S.swipe.map(c => [c.id, c]));
  const parties = [...new Set(Object.values(done).map(d => d.party))];
  const rows = parties.map(p => ({ p, ...tallyFor(st, p) })).filter(r => r.n).sort((a, b) => (b.agree / b.n) - (a.agree / a.n) || b.n - a.n);
  const total = Object.values(done).filter(d => d.v !== 'skip').length, agreed = Object.values(done).filter(d => d.v === 'agree').length;
  const liked = Object.entries(done).filter(([, d]) => d.v === 'agree').map(([id]) => byId[id]).filter(Boolean);
  $('#main').innerHTML = `<section class="view"><div class="swipe-wrap" style="max-width:760px">
    <button class="btn ghost sm" data-go="swipe" style="justify-self:start">← Keep swiping</button>
    <div><div class="kicker">Your tally</div><h2>You agreed with ${agreed} of ${total} policies</h2><p class="muted">How often you agreed with each party's policies among the cards you've seen. It's a reflection of the cards you happened to get, not a full comparison; the Find your match quiz is the more careful tool.</p>${RESULT_DISCLAIMER}</div>
    ${rows.length ? `<div class="card stack">${rows.map(r => `<div class="row" style="flex-wrap:nowrap"><span style="width:130px;flex:none" class="small"><b>${esc(pname(r.p))}</b></span><div class="meter" style="flex:1;height:14px"><span style="width:${r.agree / r.n * 100}%;background:${pcolor(r.p)}"></span></div><span class="num small" style="width:140px;text-align:right;white-space:nowrap">${r.agree}/${r.n} · ${Math.round(r.agree / r.n * 100)}%${r.n < 3 ? ' <span class="tiny muted">(few)</span>' : ''}</span></div>`).join('')}</div>` : '<p class="empty">No cards swiped yet.</p>'}
    ${liked.length ? `<div class="stack"><h3>Policies you agreed with (${liked.length})</h3><div class="stack" style="gap:8px">${liked.slice().reverse().map(c => `<div class="pol"><div class="head"><span class="dot" style="background:${pcolor(c.party)};margin-top:6px"></span><div><div class="st" style="font-size:15px">${esc(c.statement)}</div><div class="tiny muted">${esc(pname(c.party))} · ${esc(TOPIC_NAMES[c.topic] || 'Other')}</div></div></div>${c.doc ? `<div class="srcs"><button class="btn sm" data-doc="${esc(c.party)}|${esc(c.doc)}">Read the full policy</button></div>` : ''}</div>`).join('')}</div></div>` : ''}
    <div class="row"><button class="btn" id="sw-reset">Start over</button></div></div></section>`;
  $('#sw-reset').onclick = () => { st.done = {}; saveSwipe(st); route('swipe') };
};
