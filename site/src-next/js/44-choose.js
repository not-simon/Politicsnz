/* ===== Choose: hub, your results, compare two parties (+ helpers shared by the four tools) =====
   IA.md §2.4: four lenses, not four versions of one quiz. Party names hidden until answered; never a single winner;
   every result page carries RESULT_DISCLAIMER and a "How this could be wrong" block; answers stay in localStorage
   (keys quiz2, swipe, compass, game). */

/* ----- helpers ----- */
// The 17 registered parties the guide covers. Every result lists all of them.
function chooseParties() { const g = (G().parties || []).map(p => p.slug); return g.length ? g : Object.keys((G().quiz2 || {}).parties || {}) }
function chooseAZ(slugs) { return slugs.slice().sort((a, b) => pname(a).localeCompare(pname(b), 'en', { sensitivity: 'base' })) }
// Ballot order: A–Z by each party's full registered name.
function chooseBallot(slugs) { const full = s => (guideParty(s) || {}).name || P(s).name || pname(s); return slugs.slice().sort((a, b) => full(a).localeCompare(full(b), 'en', { sensitivity: 'base' })) }
const TICK = '<svg class="tick" viewBox="0 0 28 28" aria-hidden="true"><circle cx="14" cy="14" r="12"/><path d="M8.5 14.5l3.6 3.6L19.5 10"/></svg>';
const chooseHead = (icon, eyebrow, h1, lede, extra = '') => `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic(icon, 'i--s')} ${eyebrow}</p><h1>${h1}</h1>${lede ? `<p class="lede">${lede}</p>` : ''}${extra}</header>`;
const chooseSrc = (urls, pre = '') => { const a = [].concat(urls || []).filter(Boolean); return (a.length || pre) ? `<p class="src">${ic('doc')}${pre ? ` <span>${pre}</span>` : ''}${a.slice(0, 4).map((u, i) => ` <a href="${esc(u)}" target="_blank" rel="noopener">source${a.length > 1 ? ' ' + (i + 1) : ''}</a>`).join('')}</p>` : '' };
const chooseUnknowns = (items, link = ['Method, sources and the position table', 'guide/quiz-method.md']) => `<div class="unknowns"><h2 class="h3">How this could be wrong</h2><ul>${items.map(x => `<li>${x}</li>`).join('')}</ul>${link ? `<a class="more small" href="#/about/page/${link[1]}">${link[0]} ${ic('chev', 'i--xs')}</a>` : ''}</div>`;
const chooseLock = () => `<div class="lock">${ic('lock')}<h2 class="h3">Hidden until 7pm</h2><p>${ELECTION_DAY_BLOCK}</p><p class="small muted">Everything else — parties, policies, candidates, your electorate, how to vote — stays available.</p><div class="row"><a class="btn btn--primary" href="https://map.vote.nz" target="_blank" rel="noopener">Find a voting place</a><a class="btn" href="#/vote/electorate">Your electorate</a></div></div>`;
function chooseToast(msg) { const t = document.createElement('div'); t.className = 'toast'; t.setAttribute('role', 'status'); t.textContent = msg; document.body.appendChild(t); setTimeout(() => t.remove(), 2600) }
async function chooseCopy(text, title = 'Copy this text') {
  try { await navigator.clipboard.writeText(text); chooseToast('Copied. Paste it anywhere.'); return true }
  catch { openSheet({ title, html: `<p class="small soft">Your browser didn't let us copy automatically. Select the text below and copy it.</p><textarea class="input choose-ta" rows="14" readonly>${esc(text)}</textarea>` }); const ta = $('#sheet-body textarea'); if (ta) { ta.focus(); ta.select() } return false } }
const chooseShareURL = r => location.href.split('#')[0] + '#/' + r;

/* ----- hub ----- */
V.choose = () => {
  const Q = G().quiz2 || {}; const N = (Q.statements || []).length; const q = q2State(); const qn = Object.keys(q.answers || {}).filter(id => (Q.statements || []).some(s => s.id === id)).length;
  const qi = Math.min(q.i || 0, N); const qDone = N && qi >= N;
  const sw = swipeState(); const swn = Object.values(sw.done || {}).filter(d => d.v !== 'skip').length;
  const C = G().compass || {}; const ci = (C.items || []).length; const cs = compassState(); const cn = Object.keys(cs.answers || {}).length;
  const quizMeta = !qn && !qi ? 'Your answers stay on this device' : qDone ? `${qn} of ${N} answered` : `You're ${qi} of ${N} through`;
  const quizBtn = !qn && !qi ? 'Start the quiz' : qDone ? 'See your results' : 'Continue the quiz';
  const day = isElectionDay();
  $('#main').innerHTML = sectionFrame('choose', 'choose', `
    ${chooseHead('choose', 'Choose', 'Who agrees with you?', 'Four ways in, each looking through a different lens. None of them tells you how to vote, and they won’t always agree with each other. That’s normal, and the page below says why.')}
    ${day ? `<div class="note note--warn">${ic('lock')}<div><b>Closed until 7pm today.</b> It’s election day, so the tools and your results are hidden until voting closes. Compare two parties stays open.</div></div>` : ''}
    <div class="tools">
      <a class="tool tool--lead" href="#/choose/${qDone ? 'results' : 'quiz'}">
        <span class="tool__k"><span class="badge badge--signal">The full check</span><span class="badge badge--outline">About 8 minutes</span></span>
        <svg class="tool__art" viewBox="0 0 120 96" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
          <path d="M10 22h100M10 48h100M10 74h100" opacity=".35"/>
          <g fill="var(--surface)"><circle cx="12" cy="22" r="6"/><circle cx="36" cy="22" r="6"/><circle cx="60" cy="22" r="6"/><circle cx="108" cy="22" r="6"/><circle cx="12" cy="48" r="6"/><circle cx="60" cy="48" r="6"/><circle cx="84" cy="48" r="6"/><circle cx="108" cy="48" r="6"/><circle cx="36" cy="74" r="6"/><circle cx="60" cy="74" r="6"/><circle cx="84" cy="74" r="6"/><circle cx="108" cy="74" r="6"/></g>
          <circle class="art-accent" cx="84" cy="22" r="8"/><circle class="art-accent" cx="36" cy="48" r="8"/><circle class="art-accent" cx="12" cy="74" r="8"/></svg>
        <h2 class="tool__t h3">Find your match</h2><p class="tool__p">${N || 30} statements on six themes, written without party names. See all ${chooseParties().length} parties, and how much we know about each one’s views.</p>
        <span class="tool__meta">${qn ? ic('check', 'i--xs') : ''} ${quizMeta}</span>
        <span class="tool__go"><span class="btn btn--primary">${quizBtn} ${ic('chev', 'i--s')}</span></span>
      </a>
      <a class="tool" href="#/choose/swipe">
        <span class="tool__k"><span class="badge">Quick taste</span><span class="micro muted">3 minutes</span></span>
        <h2 class="tool__t h3">Policy swipe</h2><p class="tool__p">Real 2026 policies with the party hidden. Decide first, then see whose it was.</p>
        <svg class="tool__art" viewBox="0 0 96 96" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round">
          <rect x="22" y="14" width="44" height="64" rx="7" transform="rotate(-14 44 46)" opacity=".3"/><rect x="26" y="14" width="44" height="64" rx="7" transform="rotate(-5 48 46)" opacity=".55"/>
          <rect x="30" y="14" width="44" height="64" rx="7" transform="rotate(7 52 46)" fill="var(--surface)"/>
          <path class="art-accent" d="M42 46l7 7 14-16" fill="none" stroke-width="5" stroke-linecap="round" transform="rotate(7 52 46)"/></svg>
        <span class="tool__meta">${swn ? `${ic('check', 'i--xs')} ${swn} card${swn === 1 ? '' : 's'} so far` : '20 cards, spread evenly across parties'}</span>
      </a>
      <a class="tool" href="#/choose/compass">
        <span class="tool__k"><span class="badge">Your values</span><span class="micro muted">6 minutes</span></span>
        <h2 class="tool__t h3">Values compass</h2><p class="tool__p">General questions from academic surveys. Nothing about NZ parties or this year’s policies.</p>
        <svg class="tool__art" viewBox="0 0 96 96" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="8" y="8" width="80" height="80" rx="8" opacity=".35"/><path d="M48 8v80M8 48h80" opacity=".6"/>
          <circle cx="28" cy="62" r="4"/><circle cx="66" cy="30" r="4"/><circle cx="72" cy="58" r="4"/><circle cx="34" cy="34" r="4"/><circle cx="54" cy="70" r="4"/>
          <ellipse class="art-accent" cx="58" cy="44" rx="14" ry="10" style="fill-opacity:.22"/><circle class="art-accent" cx="58" cy="44" r="5"/></svg>
        <span class="tool__meta">${cn ? `${ic('check', 'i--xs')} ${cn} of ${ci} answered` : 'Shows you as a range, not a single dot'}</span>
      </a>
      <a class="tool" href="#/choose/game">
        <span class="tool__k"><span class="badge">With friends</span><span class="micro muted">2–6 players</span></span>
        <h2 class="tool__t h3">Whose policy?</h2><p class="tool__p">Pass the phone and guess which party a real policy belongs to.</p>
        <svg class="tool__art" viewBox="0 0 96 96" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="36" y="22" width="24" height="44" rx="5" fill="var(--surface)"/><path d="M45 60h6"/>
          <circle cx="14" cy="36" r="7"/><circle cx="82" cy="36" r="7"/><circle class="art-accent" cx="48" cy="84" r="7"/>
          <path d="M22 46c4 10 10 16 18 20M74 46c-4 10-10 16-18 20" stroke-dasharray="3 5"/></svg>
        <span class="tool__meta">Scores what you know, not what you think</span>
      </a>
      <a class="tool" href="#/choose/compare">
        <span class="tool__k"><span class="badge">Side by side</span></span>
        <h2 class="tool__t h3">Compare two parties</h2><p class="tool__p">Big ideas, positions on ${(G().issues || []).length || 17} issues and who they’d work with, in two columns.</p>
        <span class="tool__art" style="width:auto;height:auto;display:grid;place-items:center">${ic('swap', 'i--l')}</span>
      </a>
    </div>
    <div class="rows">
      <a class="rowlink" href="#/choose/results"><span class="rowlink__icon">${ic('list')}</span><div><div class="rowlink__title">Your results</div><div class="rowlink__sub">${qn || swn || cn ? [qn ? `Match: ${qn} of ${N} answered` : '', swn ? `Swipe: ${swn} cards` : '', cn ? `Compass: ${cn} of ${ci}` : ''].filter(Boolean).join(' · ') : 'Everything you’ve answered, in one place, with why the tools differ'}</div></div>${ic('chev')}</a>
    </div>
    <div class="split split--7-5">
      <section class="stack" aria-labelledby="h-why">
        <div class="shead"><h2 id="h-why">Why they give different answers</h2></div>
        <p class="soft">Each tool asks about something different, so a party can be close to you on one and further away on another. Look at where they agree.</p>
        <div class="table-wrap"><table class="lens">
          <thead><tr><th>Tool</th><th>Asks about</th><th>Compares you with</th></tr></thead>
          <tbody>
            <tr><td>Policy swipe</td><td>Specific 2026 promises</td><td>The parties that made them</td></tr>
            <tr><td>Find your match</td><td>Broad statements on six themes</td><td>Each party’s recorded position, with sources</td></tr>
            <tr><td>Values compass</td><td>General values, no politics</td><td>Where experts and our coders place parties</td></tr>
            <tr><td>Whose policy?</td><td>Who said what</td><td>Nobody. It scores knowledge only</td></tr>
          </tbody></table></div>
        <a class="more" href="#/about/page/guide/quiz-research.md">How each tool works, and how it could be wrong ${ic('chev', 'i--xs')}</a>
      </section>
      <aside class="stack">
        <div class="note">${ic('lock')}<div><b>Closed on election day.</b> On Saturday 7 November these tools and your results are hidden until voting closes at 7pm, because the law limits anything that could influence votes on the day.</div></div>
        <div class="note">${ic('shield')}<div><b>Your answers stay on this device.</b> Nothing is sent or stored by us. On <a href="#/choose/results">Your results</a> you can copy a code that restores your answers on another device.</div></div>
      </aside>
    </div>`);
};

/* ----- your results: every tool in one place ----- */
// The router maps both #/choose/results and #/seats/results to the view name 'results', and Seats › Results
// (56-results.js) also defines V.results. Once every file has run, V.results dispatches on the route.
V.chooseResults = async () => {
  const head = chooseHead('choose', 'Choose · Your results', 'Your results, in one place', 'Every tool you’ve used, side by side. They measure different things, so they won’t always agree; the note further down says why.');
  if (isElectionDay()) { $('#main').innerHTML = sectionFrame('choose', 'choose/results', head + chooseLock()); return }
  if (!S.swipe) S.swipe = await getJSON('data/swipe.json').catch(() => []);
  const Q = G().quiz2 || {}; const N = (Q.statements || []).length;
  const sw = swipeState(); const swn = Object.values(sw.done || {}).filter(d => d.v !== 'skip').length;
  const C = G().compass || {}; const cs = compassState(); const cn = Object.keys(cs.answers || {}).length;
  const empty = (t, p, href, btn) => `<div class="panel panel--sunk"><p><b>${t}</b></p><p class="small soft">${p}</p><a class="btn btn--s" href="${href}" style="justify-self:start">${btn} ${ic('chev', 'i--xs')}</a></div>`;
  $('#main').innerHTML = sectionFrame('choose', 'choose/results', `${head}
    <section class="stack stack--l" aria-labelledby="h-match" id="res-match"></section>
    <section class="stack stack--l" aria-labelledby="h-swipe">
      <div class="shead"><div class="shead__row"><h2 id="h-swipe">Policy swipe</h2><a class="more small" href="#/choose/swipe">${swn ? 'Keep swiping' : 'Start swiping'} ${ic('chev', 'i--xs')}</a></div></div>
      ${swn ? `<div class="split split--7-5"><div class="stack" id="res-tally">${swipeTallyHTML(sw)}</div><div class="stack">${swipeLikedHTML(sw)}${chooseUnknowns(['The tally only covers the cards you happened to see, so a party you saw twice can swing from 0% to 100%.', 'A specific promise can look very different from a party’s overall direction.', 'Skipped cards are left out.'], null)}</div></div>`
        : empty('No cards swiped yet.', 'Real 2026 policies, one at a time, with the party hidden until you decide.', '#/choose/swipe', 'Try Policy swipe')}
    </section>
    <section class="stack stack--l" aria-labelledby="h-compass">
      <div class="shead"><div class="shead__row"><h2 id="h-compass">Values compass</h2><a class="more small" href="#/choose/compass${cn ? '/results' : ''}">${cn ? 'Full compass results' : 'Start the compass'} ${ic('chev', 'i--xs')}</a></div></div>
      ${cn ? compassSummaryHTML(cs) : empty('Not started.', 'General questions about values from academic surveys, with nothing about this year’s parties or policies.', '#/choose/compass', 'Try the Values compass')}
    </section>
    <section class="stack" aria-labelledby="h-differ">
      <div class="callout callout--signal"><h2 id="h-differ" class="h3">Why they differ</h2>
        <p class="soft">The quiz compares you with each party’s recorded position on broad statements; the swipe counts how often you liked specific promises from the cards you happened to get; the compass places your general values next to where experts and our coders put the parties. A party can be close on one and far on another. Where they agree is the more solid signal; where they don’t, read that party’s page.</p>
        <a class="more small" href="#/choose">Compare the four lenses ${ic('chev', 'i--xs')}</a></div>
    </section>
    <section class="stack" aria-labelledby="h-saved">
      <div class="shead shead--quiet"><h2 id="h-saved" class="h3">Your saved answers</h2></div>
      <p class="small soft">Your answers are kept in this browser only. Copy the code to restore them on another device or browser; nothing is sent to us.</p>
      <div class="row"><button class="btn btn--s" type="button" id="exp">${ic('share', 'i--xs')} Copy my answers code</button><span class="small muted" id="expmsg" role="status"></span></div>
      <div class="field"><label class="field__label" for="impcode">Restore from a code</label><textarea class="input choose-ta" id="impcode" rows="3" placeholder="Paste a code here"></textarea></div>
      <div class="row"><button class="btn btn--s" type="button" id="imp">Restore</button></div>
      <div class="row" style="margin-top:var(--s-3)"><span class="micro muted">Clear:</span><button class="btn btn--s btn--quiet" type="button" data-reset="quiz2">Match answers</button><button class="btn btn--s btn--quiet" type="button" data-reset="swipe">Swipe cards</button><button class="btn btn--s btn--quiet" type="button" data-reset="compass">Compass answers</button><button class="btn btn--s btn--quiet" type="button" data-reset="game">Game in progress</button></div>
    </section>
    ${RESULT_DISCLAIMER}`);
  const box = $('#res-match');
  if (N) renderMatchResults(box, Q); else box.innerHTML = `<div class="shead"><h2 id="h-match">Find your match</h2></div><p class="soft">The quiz is being rebuilt on a published method. Check back soon.</p>`;
  $('#exp').onclick = async () => { const code = exportSaved(); try { await navigator.clipboard.writeText(code); $('#expmsg').textContent = 'Copied. Paste it into this box on your other device.' } catch { $('#impcode').value = code; $('#impcode').select(); $('#expmsg').textContent = 'Select the code in the box and copy it.' } };
  $('#imp').onclick = () => { try { importSaved($('#impcode').value); chooseToast('Restored. Your saved answers are back.'); V.chooseResults() } catch { $('#expmsg').textContent = 'That code didn’t work. Check it was copied in full.' } };
  $('#main').querySelectorAll('[data-reset]').forEach(b => b.onclick = () => { const k = b.dataset.reset; const label = b.textContent.trim().toLowerCase();
    if (!confirm(`Clear your ${label} from this device? This can't be undone.`)) return;
    if (k === 'quiz2') { const st = q2State(); store.set('quiz2', JSON.stringify({ seed: st.seed })) } else if (k === 'swipe') { const st = swipeState(); store.set('swipe', JSON.stringify({ topic: st.topic || '' })) } else if (k === 'compass') { const st = compassState(); store.set('compass', JSON.stringify({ source: st.source })) } else store.set(k, 'null');
    chooseToast('Cleared.'); V.chooseResults() });
};
queueMicrotask(() => { const other = V.results; if (other && other !== V.chooseResults && !other.isChooseDispatch) V.seatsResults = other;
  const dispatch = (...a) => String(S.route || '').startsWith('seats') && V.seatsResults ? V.seatsResults(...a) : V.chooseResults(...a); dispatch.isChooseDispatch = true; V.results = dispatch });

/* ----- compare two parties ----- */
V.compare = (arg) => {
  const all = chooseAZ(chooseParties()); let pick = String(arg || '').split('-vs-').filter(s => all.includes(s)).slice(0, 2);
  const draw = () => {
    const [a, b] = chooseAZ(pick); const two = pick.length === 2;
    const chips = all.map(s => `<button class="chip" type="button" data-pick="${esc(s)}" aria-pressed="${pick.includes(s)}" style="--pc:${pcolor(s)}"><span class="sw"></span>${esc(pname(s))}</button>`).join('');
    $('#main').innerHTML = sectionFrame('choose', 'choose/compare', `
      ${chooseHead('swap', 'Choose · Compare two parties', 'Compare two parties', `Pick any two of the ${all.length}. Each gets the same fields in the same order, from the party’s own material and reporting, with sources.`)}
      <section class="stack" aria-labelledby="h-pick"><h2 id="h-pick" class="h4">${two ? 'Comparing' : pick.length ? 'Pick one more party' : 'Pick two parties'}</h2>
        <div class="chips" role="group" aria-labelledby="h-pick">${chips}</div>
        <p class="micro muted">Listed A–Z. ${two ? 'Pick another party to swap it for the one you chose first.' : ''}</p></section>
      ${two ? compareBody(a, b) : `<div class="panel panel--sunk"><p class="soft">You’ll see their summaries, big ideas, who they’d work with, whether their promises are costed, what they and their critics say, and where they stand on each issue — both parties side by side.</p></div>`}`);
    $('#main').querySelectorAll('[data-pick]').forEach(btn => btn.onclick = () => { const s = btn.dataset.pick;
      if (pick.includes(s)) pick = pick.filter(x => x !== s); else { pick.push(s); if (pick.length > 2) pick.shift() }
      const path = 'choose/compare' + (pick.length === 2 ? '/' + chooseAZ(pick).join('-vs-') : pick.length === 1 ? '/' + pick[0] : '');
      S.route = path; try { history.replaceState(history.state, '', '#/' + path) } catch {}
      const y = scrollY; draw(); scrollTo(0, y) });
  };
  draw();
};
function compareBody(a, b) {
  const ga = guideParty(a) || {}, gb = guideParty(b) || {};
  const cell = (s, html) => `<div class="cmp__cell" style="--pc:${pcolor(s)}"><span class="ptag ptag--s"><span class="sw"></span>${esc(pname(s))}</span>${html}</div>`;
  const pair = (title, fa, fb, id) => `<section class="stack" aria-labelledby="cmp-${id}"><div class="shead"><h2 id="cmp-${id}" class="h3">${title}</h2></div><div class="cmp__pair">${cell(a, fa(ga, a))}${cell(b, fb ? fb(gb, b) : fa(gb, b))}</div></section>`;
  const none = '<p class="small muted">Not recorded.</p>';
  const nutshell = g => g.in_a_nutshell ? `<p>${esc(g.in_a_nutshell)}</p>${chooseSrc(g.sources)}` : none;
  const ideas = (g, s) => (g.big_ideas || []).length ? `<ol class="ideas">${g.big_ideas.map(x => `<li><div><span style="font-weight:600">${esc(T(x))}</span>${(x.policy_ids || []).length ? `<span class="micro muted">${x.policy_ids.length} polic${x.policy_ids.length === 1 ? 'y' : 'ies'}</span>` : ''}</div></li>`).join('')}</ol><a class="more small" href="#/parties/${esc(s)}/policies">All ${esc(pname(s))} policies ${ic('chev', 'i--xs')}</a>` : none;
  const pchips = (arr, no) => (arr || []).length ? `<div class="row">${arr.map(x => `<span class="pchip${no ? ' pchip--no' : ''}" style="--pc:${pcolor(x)}"><span class="sw"></span>${esc(pname(x))}</span>`).join('')}</div>` : '<span class="small muted">None stated</span>';
  const works = g => { const c = g.coalition_stance_2026; if (!c) return none;
    return `<p>${esc(c.summary || '')}</p><div class="works"><div class="works__row"><span>Open to</span>${pchips(c.open_to)}</div><div class="works__row"><span>Ruled out</span>${pchips(c.rules_out, true)}</div></div>${chooseSrc(c.sources, c.as_of ? 'As of ' + esc(c.as_of) : '')}` };
  const costed = g => { const c = g.costings; if (!c) return none; const word = c.published === true ? 'Costings published' : c.published === false ? 'No costings published' : 'Partly costed';
    return `<p><span class="badge${c.published === true ? ' badge--ink' : ' badge--outline'}">${word}</span></p>${c.summary ? `<p class="small soft">${esc(c.summary)}</p>` : ''}${chooseSrc(c.sources, c.date ? esc(c.date) : '')}` };
  const said = (v, critics) => v && T(v) ? `<div class="side${critics ? ' side--critics' : ''}"><span class="eyebrow">${critics ? 'What critics say' : 'What they say'}</span><blockquote>${esc(T(v))}</blockquote>${chooseSrc(srcOf(v), [v.attribution, v.date].filter(Boolean).map(esc).join(' · '))}</div>` : '';
  const sides = g => said(g.they_say) + said(g.critics_say, true) || none;
  const iss = (G().issues || []).slice().sort((x, y) => String(x.title).localeCompare(String(y.title)));
  const both = iss.filter(i => (i.positions || {})[a] && (i.positions || {})[b]);
  const one = iss.filter(i => !both.includes(i) && ((i.positions || {})[a] || (i.positions || {})[b]));
  const pos = (i, s) => { const p = i.positions[s]; return `<p class="small">${esc(T(p))}</p>${chooseSrc(srcOf(p))}` };
  return `<div class="cmp stack stack--xl">
    <div class="cmp__pair cmp__heads" aria-hidden="true">${[a, b].map(s => `<div class="cmp__cell" style="--pc:${pcolor(s)}"><span class="h4">${esc(pname(s))}</span><span class="micro muted">${esc((guideParty(s) || {}).name || P(s).name || '')}</span></div>`).join('')}</div>
    ${pair('In a nutshell', nutshell, null, 'nut')}
    ${pair('Big ideas', ideas, null, 'ideas')}
    ${pair('Who they’d work with', works, null, 'works')}
    ${pair('Costed?', costed, null, 'cost')}
    ${pair('Two sides', sides, null, 'sides')}
    <section class="stack" aria-labelledby="cmp-iss"><div class="shead"><div class="shead__row"><h2 id="cmp-iss" class="h3">Where they stand on the issues</h2><span class="micro muted">${both.length} issue${both.length === 1 ? '' : 's'} where both have a position · A–Z</span></div></div>
      ${both.length ? both.map(i => `<div class="stack stack--s"><div class="shead shead--quiet"><div class="shead__row"><h3 class="h4">${esc(i.title)}</h3><a class="more small" href="#/parties/issues/${esc(i.slug)}">All parties ${ic('chev', 'i--xs')}</a></div></div><div class="cmp__pair">${cell(a, pos(i, a))}${cell(b, pos(i, b))}</div></div>`).join('') : '<p class="small muted">No issue where both parties have a recorded position.</p>'}
      ${one.length ? `<p class="small soft">Only one of the two has a recorded position on: ${one.map(i => `<a href="#/parties/issues/${esc(i.slug)}">${esc(i.title)}</a>`).join(', ')}.</p>` : ''}
    </section>
    <div class="row"><a class="btn btn--s" href="#/parties/${esc(a)}">${esc(pname(a))} party page</a><a class="btn btn--s" href="#/parties/${esc(b)}">${esc(pname(b))} party page</a></div>
  </div>`;
}
