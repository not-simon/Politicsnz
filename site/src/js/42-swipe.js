/* ----- Policy swipe -----
   Real 2026 policies, party hidden (data/swipe.json is leak-filtered at build time). Decide, then see whose it was.
   Rounds of 20 cards, dealt by weighted round-robin so no party floods the deck. Tally = agreement rate per party, A–Z. */
const SWIPE_ROUND = 20;
function swipeState() { try { const s = JSON.parse(store.get('swipe') || '{}'); return s && typeof s === 'object' ? s : {} } catch { return {} } }
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
function tallyFor(st, party) { let n = 0, agree = 0; for (const d of Object.values(st.done || {})) if (d.party === party && d.v !== 'skip') { n++; if (d.v === 'agree') agree++ } return { n, agree } }
const swipeTopic = t => TOPIC_NAMES[t] || 'Other';
// The tally block (used on the swipe page and on Your results).
function swipeTallyHTML(st, noHead) {
  const done = Object.values(st.done || {}); const seen = [...new Set(done.filter(d => d.v !== 'skip').map(d => d.party))];
  const total = done.filter(d => d.v !== 'skip').length;
  const rows = chooseAZ(seen).map(p => ({ p, ...tallyFor(st, p) })).filter(r => r.n);
  const unseen = chooseAZ(chooseParties().filter(s => !seen.includes(s)));
  const hd = noHead ? '' : `<div class="shead"><div class="shead__row"><h2 class="h3">Your tally so far</h2><span class="micro muted">${total} card${total === 1 ? '' : 's'}</span></div></div>`;
  if (!total) return `${hd}<p class="small soft">Your agreement rate with each party shows up here as you go.</p>`;
  return `${hd}
    <p class="small soft">How often you agreed, out of the cards you’ve seen from each party, A–Z. Parties come up about equally often, so long manifestos don’t win by volume.</p>
    <div class="tally ctally">${rows.map((r, k) => { const rate = Math.round(r.agree / r.n * 100); return `<div class="tally__row" style="--pc:${pcolor(r.p)}"><span class="tally__who"><span class="ptag ptag--s"><span class="sw"></span>${esc(pname(r.p))}</span>${r.n < 3 ? ' <span class="badge" title="Fewer than 3 cards">few</span>' : ''}</span><div class="bar" role="img" aria-label="${esc(pname(r.p))}: agreed with ${r.agree} of ${r.n}, ${rate}%"><i style="--w:${rate}%;--i:${k}"></i></div><span class="tally__v"><b>${r.agree}</b> of ${r.n}</span></div>` }).join('')}</div>
    ${unseen.length ? `<p class="micro muted">No cards yet from: ${unseen.map(s => esc(pname(s))).join(', ')}.</p>` : ''}
    <p class="micro muted">${total < SWIPE_ROUND ? `${total} card${total === 1 ? ' is' : 's is'} a small sample. Keep going for a clearer picture.` : '“Few” marks parties you’ve seen fewer than 3 cards from: their rate can swing a lot.'}</p>` }
function swipeLiked(st) { const byId = Object.fromEntries((S.swipe || []).map(c => [c.id, c]));
  return Object.entries(st.done || {}).filter(([, d]) => d.v === 'agree').sort((a, b) => (b[1].t || 0) - (a[1].t || 0)).map(([id]) => byId[id]).filter(Boolean) }
function swipeLikedList(liked) { return `<div class="stack stack--s">${liked.map(c => `<div class="pol" style="--pc:${pcolor(c.party)}"><p class="pol__t" style="font-weight:600">${esc(c.statement)}</p><p class="pol__m micro muted"><span class="ptag ptag--s" style="--pc:${pcolor(c.party)}"><span class="sw"></span>${esc(pname(c.party))}</span> · ${esc(swipeTopic(c.topic))}${c.doc ? ` · <button class="linkbtn" type="button" data-doc="${esc(c.party)}|${esc(c.doc)}">Read the full policy</button>` : ''}</p></div>`).join('')}</div>` }
function swipeLikedHTML(st, open) { const liked = swipeLiked(st); if (!liked.length) return '';
  return `<details class="disclose"${open ? ' open' : ''}><summary>Policies you agreed with (${liked.length})</summary><div class="disclose__body">${swipeLikedList(liked)}</div></details>` }

V.swipe = async () => {
  if (!S.swipe) S.swipe = await getJSON('data/swipe.json').catch(() => []);
  await loadPeople();
  const st = swipeState(); st.done = st.done || {}; let topic = st.topic || '';
  let deck = buildDeck(S.swipe, st.done, topic); let i = 0, sess = 0, busy = false;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const topics = Object.keys(TOPIC_NAMES).filter(t => S.swipe.some(c => c.topic === t));
  $('#main').innerHTML = sectionFrame('choose', 'choose/swipe', `
    ${chooseHead('cards', 'Choose · Policy swipe', 'Agree or disagree?', 'Real 2026 policies, party hidden until you decide.')}
    <div class="chips chips--scroll" role="group" aria-label="Topic" id="sw-topics">${[['', 'All topics'], ...topics.map(t => [t, TOPIC_NAMES[t]])].map(([t, l]) => `<button class="chip" type="button" data-topic="${esc(t)}" aria-pressed="${t === topic}">${esc(l)}</button>`).join('')}</div>
    <div class="split split--7-5">
      <section class="stack stack--l" aria-label="Card">
        <div class="progress-line" id="sw-prog"></div>
        <div class="deck" id="deck"></div>
        <div class="swipe-actions" id="acts" role="group" aria-label="Your verdict on this card">
          <button class="swipe-btn swipe-btn--disagree" type="button" data-swipe="disagree" aria-label="Disagree with this policy" aria-keyshortcuts="ArrowLeft"><i>${ic('x')}</i>Disagree</button>
          <button class="swipe-btn swipe-btn--skip" type="button" data-swipe="skip" aria-label="Not sure, skip this policy" aria-keyshortcuts="ArrowUp"><i>${ic('minus')}</i>Not sure</button>
          <button class="swipe-btn swipe-btn--agree" type="button" data-swipe="agree" aria-label="Agree with this policy" aria-keyshortcuts="ArrowRight"><i>${ic('check')}</i>Agree</button>
        </div>
        <p class="micro muted" style="text-align:center">Swipe the card, use the buttons, or the arrow keys: → agree, ← disagree, ↑ not sure. Summaries are each party’s own policy, described neutrally.</p>
        <p class="sr-only" id="sw-say" role="status"></p>
      </section>
      <aside class="stack stack--l">
        <div id="sw-reveal"></div>
        <div class="rows" id="sw-rows"></div>
        ${chooseUnknownsDisclose(['The tally only covers the cards you happened to see, so a party you saw twice can swing from 0% to 100%.', 'Some parties publish far fewer policies; you may see the same few from them.', 'A specific promise can look very different from a party’s overall direction. Find your match is the more careful tool.'], ['How the swipe works', 'guide/quiz-research.md'])}
        <div class="row"><a class="btn btn--s" href="#/choose/results/swipe">All your results</a><button class="btn btn--s btn--quiet" type="button" id="sw-reset">Start over</button></div>
        ${RESULT_DISCLAIMER}
      </aside>
    </div>`);
  const stage = $('#deck'), acts = $('#acts');
  const cardHTML = c => `<article class="scard" aria-labelledby="sc-s" id="sc-top">
      <span class="scard__stamp" aria-hidden="true">AGREE</span>
      <div class="row row--between"><span class="badge">${esc(swipeTopic(c.topic))}</span><span class="scard__blind">${ic('lock', 'i--xs')} Party hidden</span></div>
      <p id="sc-s" class="scard__s">${esc(c.statement)}</p>
      ${c.how ? `<div class="scard__body"><p><b>What it would do:</b> ${esc(c.how)}</p></div>` : ''}
      ${c.why ? `<details class="disclose" style="border-top:1px solid var(--line)"><summary class="small">The reasoning given</summary><div class="disclose__body small"><p>${esc(c.why)}</p></div></details>` : ''}
      <p class="src">${ic('doc')} From a party’s 2026 policy document · summarised, meaning kept</p></article>`;
  // The tally and the liked list sit behind rows that open the sheet, so the deck stays the first screen.
  const tallySheet = () => openSheet({ title: 'Your tally so far', html: `<div class="stack">${swipeTallyHTML(st, true)}<a class="more small" href="#/choose/results/swipe">All your results ${ic('chev', 'i--xs')}</a>${RESULT_DISCLAIMER}</div>` });
  const likedSheet = () => { const liked = swipeLiked(st); openSheet({ title: `Policies you agreed with (${liked.length})`, html: `<div class="stack"><p class="small soft">Newest first. Each one’s party is shown now that you’ve decided.</p>${swipeLikedList(liked)}${RESULT_DISCLAIMER}</div>` }) };
  const drawTally = () => { const total = Object.values(st.done).filter(d => d.v !== 'skip').length; const parties = new Set(Object.values(st.done).filter(d => d.v !== 'skip').map(d => d.party)).size; const liked = swipeLiked(st).length;
    $('#sw-rows').innerHTML = chooseRowBtn('id="sw-tally"', 'poll', 'Your tally so far', total ? `${total} card${total === 1 ? '' : 's'} from ${parties} part${parties === 1 ? 'y' : 'ies'} · agreement with each, A–Z` : 'Your agreement rate with each party shows up here as you go')
      + (liked ? chooseRowBtn('id="sw-liked"', 'check', `Policies you agreed with (${liked})`, 'With the party, the topic and the full policy') : '');
    $('#sw-tally').onclick = tallySheet; const l = $('#sw-liked'); if (l) l.onclick = likedSheet };
  const drawProg = () => { const left = deck.length - i; $('#sw-prog').innerHTML = `<b>Card ${Math.min(sess + 1, SWIPE_ROUND)} of ${SWIPE_ROUND}</b><div class="bar"><i style="--w:${Math.round(sess / SWIPE_ROUND * 100)}%"></i></div><span class="micro muted">${left} left${topic ? ' on this topic' : ''}</span>` };
  const render = () => { busy = false; drawProg();
    const hadFocus = acts.contains(document.activeElement);
    const stop = html => { stage.innerHTML = html; acts.hidden = true; const t = $('#sw-tally2'); if (t) t.onclick = tallySheet; if (hadFocus) { const f = stage.querySelector('button, a'); if (f) f.focus() } };
    if (i >= deck.length) { stop(`<div class="panel panel--sunk"><h2 class="h3">You’ve seen every card${topic ? ' on this topic' : ''}.</h2><p class="soft">Pick another topic, or look at your tally.</p><div class="row"><button class="btn btn--primary" type="button" id="sw-tally2" aria-haspopup="dialog">See your tally</button><a class="btn" href="#/choose/results/swipe">All your results</a></div></div>`); return }
    if (sess >= SWIPE_ROUND) { stop(`<div class="panel panel--sunk"><h2 class="h3">That’s ${SWIPE_ROUND} cards.</h2><p class="soft">Another round gives a clearer picture.</p><div class="row"><button class="btn btn--primary" type="button" id="sw-more">Another ${SWIPE_ROUND}</button><button class="btn" type="button" id="sw-tally2" aria-haspopup="dialog">See your tally</button><a class="btn btn--quiet" href="#/choose/results/swipe">All your results</a></div></div>`); $('#sw-more').onclick = () => { sess = 0; render(); const b = acts.querySelector('[data-swipe="agree"]'); if (b) b.focus() }; return }
    acts.hidden = false;
    stage.innerHTML = (deck[i + 2] ? '<article class="scard scard--behind2" aria-hidden="true"><p>.</p></article>' : '') + (deck[i + 1] ? '<article class="scard scard--behind" aria-hidden="true"><p>.</p></article>' : '') + cardHTML(deck[i]);
    attachDrag($('#sc-top')) };
  const reveal = (c, verdict) => { const faces = typeof leaderFaces === 'function' ? leaderFaces(c.party) : []; const t = tallyFor(st, c.party);
    $('#sw-reveal').innerHTML = `<section class="reveal" style="--pc:${pcolor(c.party)}" aria-labelledby="rv">
      <div class="reveal__who">${faces[0] ? faceHTML(faces[0], c.party) : ''}<span class="stack stack--s" style="gap:2px"><span class="micro muted">Last card was from</span><span id="rv" class="reveal__name">${esc(P(c.party).name || pname(c.party))}</span></span></div>
      <p class="small"><span class="badge badge--ink">${ic(verdict === 'agree' ? 'check' : 'x', 'i--xs')} You ${verdict === 'agree' ? 'agreed' : 'disagreed'}</span></p>
      <p style="font-weight:700">${esc(c.statement)}</p>
      <p class="small soft">So far you’ve agreed with <b>${t.agree}</b> of the <b>${t.n}</b> ${esc(pname(c.party))} polic${t.n === 1 ? 'y' : 'ies'} you’ve seen.</p>
      <div class="row">${c.doc ? `<button class="btn btn--s" type="button" data-doc="${esc(c.party)}|${esc(c.doc)}">${ic('doc', 'i--xs')} Read the full policy</button>` : ''}<a class="btn btn--s btn--quiet" href="#/parties/${esc(c.party)}">About this party</a></div></section>` };
  const decide = verdict => { if (busy) return; const c = deck[i]; if (!c) return; if (acts.hidden) return; busy = true;
    st.done[c.id] = { v: verdict, party: c.party, t: Date.now() }; saveSwipe(st);
    const top = $('#sc-top'); if (top) { top.style.transition = ''; top.style.transform = verdict === 'agree' ? 'translateX(130%) rotate(16deg)' : verdict === 'disagree' ? 'translateX(-130%) rotate(-16deg)' : 'translateY(-40px) scale(.96)'; top.style.opacity = '0' }
    setTimeout(() => { i++; sess++; if (verdict !== 'skip') reveal(c, verdict); drawTally(); render();
      const next = sess < SWIPE_ROUND && deck[i]; $('#sw-say').textContent = `${verdict === 'skip' ? 'Skipped.' : `You ${verdict === 'agree' ? 'agreed' : 'disagreed'}. That was a ${P(c.party).name || pname(c.party)} policy.`} ${next ? `Next card: ${next.statement}` : 'That’s the end of this round.'}` }, reduce ? 10 : 280) };
  function attachDrag(el) { if (!el) return; let x0 = null, y0 = 0, dx = 0, id = null; const stamp = el.querySelector('.scard__stamp');
    el.addEventListener('pointerdown', e => { if (e.button > 0 || e.target.closest('summary, a, button, details[open] .disclose__body')) return; x0 = e.clientX; y0 = e.clientY; dx = 0; id = e.pointerId });
    el.addEventListener('pointermove', e => { if (x0 == null || e.pointerId !== id) return; dx = e.clientX - x0;
      if (!el.hasPointerCapture(id)) { if (Math.abs(dx) < 8 || Math.abs(dx) < Math.abs(e.clientY - y0)) return; try { el.setPointerCapture(id) } catch {} el.style.transition = 'none' }
      el.style.transform = `translateX(${dx}px) rotate(${dx / 18}deg)`; el.classList.toggle('scard--tilt', Math.abs(dx) > 60); if (stamp) stamp.textContent = dx > 0 ? 'AGREE' : 'DISAGREE' });
    const end = () => { if (x0 == null) return; x0 = null; el.classList.remove('scard--tilt');
      if (dx > 100) decide('agree'); else if (dx < -100) decide('disagree'); else { el.style.transition = ''; el.style.transform = '' } dx = 0 };
    el.addEventListener('pointerup', end); el.addEventListener('pointercancel', end) }
  acts.onclick = e => { const b = e.target.closest('[data-swipe]'); if (b) decide(b.dataset.swipe) };
  $('#sw-topics').onclick = e => { const b = e.target.closest('[data-topic]'); if (!b) return; topic = b.dataset.topic; st.topic = topic; saveSwipe(st);
    $('#sw-topics').querySelectorAll('[data-topic]').forEach(x => x.setAttribute('aria-pressed', x === b)); deck = buildDeck(S.swipe, st.done, topic); i = 0; render() };
  $('#sw-reset').onclick = () => { if (!confirm('Clear every card you’ve swiped from this device?')) return; st.done = {}; saveSwipe(st); V.swipe() };
  if (S.swipeKeys) document.removeEventListener('keydown', S.swipeKeys);
  S.swipeKeys = e => { if (S.route !== 'choose/swipe' || $('#sheet').open || /^(INPUT|TEXTAREA|SELECT)$/.test((document.activeElement || {}).tagName || '') || e.altKey || e.ctrlKey || e.metaKey) return;
    const v = { ArrowRight: 'agree', ArrowLeft: 'disagree', ArrowUp: 'skip' }[e.key]; if (v) { e.preventDefault(); decide(v) } };
  document.addEventListener('keydown', S.swipeKeys);
  drawTally(); render();
};
// Old #swipe-tally route: the tally now sits on the swipe page itself.
V['swipe-tally'] = () => V.swipe();
