/* ----- Whose policy? pass-the-phone game ----- */
const GAME_PARTIES = ['national', 'labour', 'green', 'act', 'nz-first', 'te-pati-maori', 'opportunity'];

V.game = async () => {
  if (!S.swipe) S.swipe = await getJSON('data/swipe.json').catch(() => []);
  await loadPeople();
  let g; try { g = JSON.parse(store.get('game') || 'null') } catch { g = null }
  const setup = () => { $('#main').innerHTML = `<section class="view"><div class="quiz" style="max-width:640px"><div class="stack"><div class="kicker">Pass-the-phone game · 2–6 players</div><h2>Whose policy?</h2>
      <p class="lede">A real 2026 policy comes up with no party named. Guess whose it is, then pass the phone. The policies come from the seven parties polling highest, dealt evenly, so nobody can win by picking one party every time.</p></div>
      <div class="card stack"><label class="small"><b>Players</b></label><div id="names" class="stack" style="gap:6px"></div><div class="row"><button class="btn sm" id="addp">Add a player</button><label class="row small" style="gap:6px">Rounds each <select id="rounds"><option>3</option><option selected>5</option><option>8</option></select></label></div>
        <button class="btn sun" id="startg" style="justify-self:start">Start</button></div>
      <p class="tiny muted">Just a game: it tests knowledge of what the parties are proposing, not what you think of them.</p></div></section>`;
    const names = $('#names'); const addRow = v => { const i = names.children.length; if (i >= 6) return; const d = document.createElement('div'); d.innerHTML = `<input type="search" value="${esc(v || 'Player ' + (i + 1))}" aria-label="Player ${i + 1} name" style="width:100%">`; names.appendChild(d) };
    addRow('Player 1'); addRow('Player 2'); $('#addp').onclick = () => addRow();
    $('#startg').onclick = () => { const players = [...names.querySelectorAll('input')].map(x => x.value.trim() || 'Player').slice(0, 6); const rounds = +$('#rounds').value;
      const pool = buildDeck(S.swipe.filter(c => GAME_PARTIES.includes(c.party) && c.statement.length < 140), {}, '').slice(0, players.length * rounds);
      g = { players, rounds, deck: pool.map(c => c.id), turn: 0, scores: players.map(() => 0), phase: 'handoff' }; store.set('game', JSON.stringify(g)); play() } };
  const card = id => S.swipe.find(c => c.id === id);
  const play = () => { const total = g.players.length * g.rounds; if (g.turn >= total || g.turn >= g.deck.length) return finish();
    const pi = g.turn % g.players.length; const c = card(g.deck[g.turn]); const round = Math.floor(g.turn / g.players.length) + 1;
    const scoreHTML = `<div class="score">${g.players.map((n, i) => `<span class="${i === pi ? 'turn' : ''}">${esc(n)} <b class="num">${g.scores[i]}</b></span>`).join('')}</div>`;
    if (g.phase === 'handoff') { $('#main').innerHTML = `<section class="view"><div class="quiz" style="max-width:640px">${scoreHTML}<div class="card handoff"><div class="kicker">Round ${round} of ${g.rounds}</div><div class="big">${esc(g.players[pi])}</div><p class="muted">Your turn. Take the phone, then tap when you're ready.</p><button class="btn sun" id="ready">I'm ready</button></div><button class="btn ghost sm" id="quitg">End game</button></div></section>`;
      $('#ready').onclick = () => { g.phase = 'guess'; store.set('game', JSON.stringify(g)); play() }; $('#quitg').onclick = finish; return }
    $('#main').innerHTML = `<section class="view"><div class="quiz gameboard" style="max-width:640px">${scoreHTML}<div class="card stack"><div class="kicker">${esc(g.players[pi])} · whose policy is this?</div><div class="qtext">${esc(c.statement)}</div>${c.how ? `<p class="small muted">${esc(c.how.slice(0, 260))}${c.how.length > 260 ? '…' : ''}</p>` : ''}</div>
      <div class="pchoices" id="choices">${GAME_PARTIES.map(p => `<button data-p="${p}"><span class="dot" style="background:${pcolor(p)}"></span>${esc(pname(p))}</button>`).join('')}</div><div id="verdict"></div></div></section>`;
    $('#choices').onclick = e => { const b = e.target.closest('[data-p]'); if (!b || $('#choices').dataset.done) return; $('#choices').dataset.done = '1'; const right = b.dataset.p === c.party; if (right) g.scores[pi]++;
      $('#choices').querySelectorAll('button').forEach(x => { if (x.dataset.p === c.party) x.classList.add('right'); else if (x === b) x.classList.add('wrong') });
      $('#verdict').innerHTML = `<div class="card stack"><div class="row"><span class="verdict-pill" style="background:${right ? 'var(--v-kept)' : 'var(--v-broken)'}">${right ? '✓ Correct' : '✕ Not quite'}</span><span>It's a <b>${esc(P(c.party).name)}</b> policy.</span></div><div class="row">${c.doc ? `<button class="btn sm" data-doc="${esc(c.party)}|${esc(c.doc)}">Read the full policy</button>` : ''}<button class="btn primary" id="nextturn" style="margin-left:auto">${g.turn + 1 >= Math.min(g.deck.length, g.players.length * g.rounds) ? 'See results' : 'Pass the phone →'}</button></div></div>`;
      $('#nextturn').onclick = () => { g.turn++; g.phase = 'handoff'; store.set('game', JSON.stringify(g)); play() } } };
  const finish = () => { const order = g.players.map((n, i) => [n, g.scores[i]]).sort((a, b) => b[1] - a[1]); const played = Math.min(g.turn, g.deck.length);
    $('#main').innerHTML = `<section class="view"><div class="quiz" style="max-width:640px"><div class="stack"><div class="kicker">Final scores · ${played} policies</div><h2>${esc(order[0][0])} ${order.length > 1 && order[0][1] === order[1][1] ? 'ties for the win' : 'wins'}</h2></div>
      <div class="card stack">${order.map(([n, sc], i) => `<div class="row" style="flex-wrap:nowrap"><span style="width:28px" class="num muted">${i + 1}</span><span style="flex:1"><b>${esc(n)}</b></span><div class="meter" style="flex:2"><span style="width:${g.rounds ? sc / g.rounds * 100 : 0}%;background:var(--sun)"></span></div><span class="num" style="width:60px;text-align:right">${sc} / ${g.rounds}</span></div>`).join('')}</div>
      <p class="small muted">Want to know more about the policies you saw? They're all in <button class="btn ghost sm" data-go="policies">the policy browser</button>, with the parties' full documents.</p>
      <div class="row"><button class="btn sun" id="again">Play again</button><button class="btn" data-go="swipe">Try Policy swipe</button></div></div></section>`;
    $('#again').onclick = () => { store.set('game', 'null'); g = null; setup() } };
  if (g && g.deck && g.turn < g.players.length * g.rounds) play(); else setup();
};
