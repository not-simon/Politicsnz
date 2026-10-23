/* ----- Whose policy? pass-the-phone game -----
   A real 2026 policy with no party named; guess whose it is, then pass the phone. Scores knowledge, never agreement.
   2–6 players. Play screens run in focus mode. The router locks this view on election day. */
const GAME_PARTIES = ['national', 'labour', 'green', 'act', 'nz-first', 'te-pati-maori', 'opportunity'];

V.game = async () => {
  if (!S.swipe) S.swipe = await getJSON('data/swipe.json').catch(() => []);
  await loadPeople();
  let g; try { g = JSON.parse(store.get('game') || 'null') } catch { g = null }
  const save = () => store.set('game', JSON.stringify(g));
  const choices = chooseAZ(GAME_PARTIES);
  const setup = () => { let rounds = 5;
    $('#main').innerHTML = sectionFrame('choose', 'choose/game', `
      ${chooseHead('game', 'Choose · Whose policy? · 2–6 players', 'Whose policy?', 'A real 2026 policy comes up with no party named. Guess whose it is, then pass the phone. The policies come from the seven parties polling highest, dealt evenly, so nobody can win by picking one party every time.')}
      <div class="split split--7-5">
        <section class="stack stack--l">
          <div class="field"><span class="field__label" id="pl-lab">Players</span><div class="stack stack--s" id="names" role="group" aria-labelledby="pl-lab"></div>
            <div class="row"><button class="btn btn--s" type="button" id="addp">Add a player</button><button class="btn btn--s btn--quiet" type="button" id="delp">Remove the last one</button></div></div>
          <div class="field"><span class="field__label" id="rd-lab">Policies each</span><div class="seg" role="group" aria-labelledby="rd-lab" id="rounds">${[3, 5, 8].map(n => `<button type="button" data-r="${n}" aria-pressed="${n === rounds}">${n}</button>`).join('')}</div></div>
          <button class="btn btn--primary btn--l" type="button" id="startg" style="justify-self:start">Start the game ${ic('chev', 'i--s')}</button>
        </section>
        <aside class="stack"><div class="note">${ic('info')}<div><b>Just a game.</b> It scores what you know about what the parties are proposing, never what you think of them. Nothing is saved except the game in progress, on this device.</div></div></aside>
      </div>`);
    const names = $('#names'); const addRow = v => { const n = names.children.length; if (n >= 6) return; const d = document.createElement('div'); d.innerHTML = `<input class="input" type="text" maxlength="24" autocomplete="off" value="${esc(v || 'Player ' + (n + 1))}" aria-label="Player ${n + 1} name">`; names.appendChild(d); sync() };
    const sync = () => { const n = names.children.length; $('#addp').disabled = n >= 6; $('#delp').disabled = n <= 2 };
    addRow('Player 1'); addRow('Player 2');
    $('#addp').onclick = () => addRow(); $('#delp').onclick = () => { if (names.children.length > 2) names.lastElementChild.remove(); sync() };
    $('#rounds').onclick = e => { const b = e.target.closest('[data-r]'); if (!b) return; rounds = +b.dataset.r; $('#rounds').querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x === b)) };
    $('#startg').onclick = () => { const players = [...names.querySelectorAll('input')].map(x => x.value.trim() || 'Player').slice(0, 6);
      const pool = buildDeck(S.swipe.filter(c => GAME_PARTIES.includes(c.party) && c.statement.length < 140), {}, '').slice(0, players.length * rounds);
      g = { players, rounds, deck: pool.map(c => c.id), turn: 0, scores: players.map(() => 0), phase: 'handoff' }; save(); play() } };
  const card = id => S.swipe.find(c => c.id === id);
  const board = pi => `<div class="game-score" aria-label="Scores">${g.players.map((n, k) => `<span${k === pi ? ' aria-current="true"' : ''}>${esc(n)} <b class="num">${g.scores[k]}</b></span>`).join('')}</div>`;
  const play = () => { const total = Math.min(g.deck.length, g.players.length * g.rounds); if (g.turn >= total) return finish();
    const pi = g.turn % g.players.length; const c = card(g.deck[g.turn]); if (!c) { g.turn++; save(); return play() } const round = Math.floor(g.turn / g.players.length) + 1;
    if (g.phase === 'handoff') {
      $('#main').innerHTML = `<div class="stack stack--l game">${board(pi)}
        <section class="game-hand stack" aria-labelledby="gp"><p class="eyebrow">Round ${round} of ${g.rounds} · pass the phone to</p><p class="figure" id="gp">${esc(g.players[pi])}</p>
          <p class="soft">Your turn. Take the phone, then tap when you’re ready.</p>
          <div class="row"><button class="btn btn--primary btn--l" type="button" id="ready">I’m ready</button><button class="btn btn--quiet" type="button" id="quitg">End game</button></div></section></div>`;
      focusMode('Whose policy?', 'choose');
      $('#ready').onclick = () => { g.phase = 'guess'; save(); play() }; $('#quitg').onclick = finish; $('#ready').focus(); return }
    $('#main').innerHTML = `<div class="stack stack--l game">${board(pi)}
      <section class="stack" aria-labelledby="gq"><p class="eyebrow">${esc(g.players[pi])} · whose policy is this?</p><p class="statement" id="gq">${esc(c.statement)}</p>${c.how ? `<p class="soft">${esc(c.how.length > 260 ? c.how.slice(0, 260).replace(/\s+\S*$/, '') + '…' : c.how)}</p>` : ''}</section>
      <div class="persona game-choices" id="choices" role="group" aria-labelledby="gq">${choices.map(p => `<button type="button" data-p="${p}" aria-pressed="false" style="--pc:${pcolor(p)}"><i class="sw" aria-hidden="true"></i>${esc(pname(p))}</button>`).join('')}</div>
      <div id="verdict" aria-live="polite"></div></div>`;
    focusMode('Whose policy?', 'choose');
    $('#choices').onclick = e => { const b = e.target.closest('[data-p]'); if (!b || $('#choices').dataset.done) return; $('#choices').dataset.done = '1'; const right = b.dataset.p === c.party; if (right) g.scores[pi]++;
      $('#choices').querySelectorAll('button').forEach(x => { x.disabled = x !== b && x.dataset.p !== c.party; if (x === b) x.setAttribute('aria-pressed', 'true'); if (x.dataset.p === c.party) x.classList.add('v-kept'); else if (x === b) x.classList.add('v-broken') });
      const lastTurn = g.turn + 1 >= Math.min(g.deck.length, g.players.length * g.rounds);
      $('#verdict').innerHTML = `<div class="panel stack"><div class="row"><span class="verdict ${right ? 'v-kept' : 'v-broken'}">${ic(right ? 'check' : 'x')} ${right ? 'Correct' : 'Not quite'}</span><span>It’s a <b>${esc(P(c.party).name || pname(c.party))}</b> policy.</span></div>
        <div class="row">${c.doc ? `<button class="btn btn--s" type="button" data-doc="${esc(c.party)}|${esc(c.doc)}">${ic('doc', 'i--xs')} Read the full policy</button>` : ''}<button class="btn btn--primary" type="button" id="nextturn" style="margin-left:auto">${lastTurn ? 'See the scores' : 'Pass the phone'} ${ic('chev', 'i--s')}</button></div></div>`;
      g.phase = 'answered'; save();
      $('#nextturn').onclick = () => { g.turn++; g.phase = 'handoff'; save(); window.scrollTo(0, 0); play() }; $('#nextturn').focus({ preventScroll: true }) }; };
  const finish = () => { focusMode(null); const order = g.players.map((n, k) => [n, g.scores[k]]).sort((a, b) => b[1] - a[1]); const played = Math.min(g.turn, g.deck.length);
    const tie = order.length > 1 && order[0][1] === order[1][1]; const seen = g.deck.slice(0, played).map(card).filter(Boolean);
    $('#main').innerHTML = sectionFrame('choose', 'choose/game', `
      ${chooseHead('game', `Choose · Whose policy? · ${played} polic${played === 1 ? 'y' : 'ies'}`, tie ? 'It’s a tie' : `${esc(order[0][0])} wins`, 'Right guesses out of the policies each player got. It’s a knowledge game: it says nothing about who agrees with whom.')}
      <div class="split split--7-5">
        <section class="stack"><div class="shead"><h2 class="h3">Final scores</h2></div>
          <div class="tally ctally">${order.map(([n, sc], k) => `<div class="tally__row" style="--pc:var(--text-2)"><span class="small"><b>${esc(n)}</b></span><div class="bar" role="img" aria-label="${esc(n)}: ${sc} right out of ${g.rounds}"><i style="--w:${g.rounds ? Math.round(sc / g.rounds * 100) : 0}%;--i:${k}"></i></div><span class="tally__v"><b>${sc}</b> of ${g.rounds}</span></div>`).join('')}</div>
          <div class="row"><button class="btn btn--primary" type="button" id="again">Play again</button><a class="btn" href="#/choose/swipe">Try Policy swipe</a></div></section>
        <aside class="stack">${seen.length ? `<details class="disclose"><summary>The policies in this game (${seen.length})</summary><div class="disclose__body"><div class="stack stack--s">${seen.map(c => `<div class="pol"><p class="pol__t" style="font-weight:600">${esc(c.statement)}</p><p class="pol__m micro muted"><span class="ptag ptag--s" style="--pc:${pcolor(c.party)}"><span class="sw"></span>${esc(pname(c.party))}</span>${c.doc ? ` · <button class="linkbtn" type="button" data-doc="${esc(c.party)}|${esc(c.doc)}">Read the full policy</button>` : ''}</p></div>`).join('')}</div></div></details>` : ''}
          <p class="small soft">Every policy is in <a href="#/parties/policies">the policy browser</a>, with the parties’ full documents.</p></aside>
      </div>`);
    $('#again').onclick = () => { store.set('game', 'null'); g = null; setup() } };
  if (g && g.deck && g.players && g.turn < Math.min(g.deck.length, g.players.length * g.rounds)) { if (g.phase === 'answered') { g.turn++; g.phase = 'handoff'; save() } play() } else setup();
};
