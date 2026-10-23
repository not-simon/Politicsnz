/* ----- Find your match (quiz v2) -----
   Scoring follows guide/quiz-method.md exactly: a_ij = 1 − |u − p| / 4 over the statements both answered, importance
   weights (less .5, normal 1, a lot 2), k = 4 phantom neutral statements, coverage rule |S_j| ≥ max(10, ½M).
   Results live at #/choose/results (V.results); this view is the intro and the question screen (focus mode). */
const SCALE = [[-2, 'Strongly disagree'], [-1, 'Disagree'], [0, 'Neutral'], [1, 'Agree'], [2, 'Strongly agree']];
function quizState() { try { return JSON.parse(store.get('quiz') || '{}') } catch { return {} } }
function saveQuiz(q) { store.set('quiz', JSON.stringify(q)) }
const IMP = [['less', 'Less'], ['normal', 'Normal'], ['very', 'A lot']];
const QDIMS = ['E', 'S', 'T', 'V', 'O', 'D'];
const QDIM_SHORT = { E: 'Economy', S: 'Society & justice', T: 'Te Tiriti', V: 'Environment', O: 'Immigration & the world', D: 'Democracy' };
function q2State() { try { const s = JSON.parse(store.get('quiz2') || '{}'); return s && typeof s === 'object' ? s : {} } catch { return {} } }
function q2Save(st) { store.set('quiz2', JSON.stringify(st)) }
function shuffled(ids, seed) { let x = seed || 1; const r = () => (x = (x * 1664525 + 1013904223) % 4294967296) / 4294967296; const a = ids.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]] } return a }
// shift: 0 as coded; +1 moves every ±1 party cell one step toward the user's answer, −1 one step away (the method's uncertainty band).
function q2Scores(Q, st, { dropLow = false, shift = 0 } = {}) { const W = { less: .5, normal: 1, very: 2 }; const k = ((Q.scoring || {}).shrinkage || {}).k ?? 4;
  const answered = Q.statements.filter(q => typeof st.answers[q.id] === 'number'); const M = answered.length; const need = Math.max(10, Math.ceil(0.5 * M));
  const out = []; for (const [slug, meta] of Object.entries(Q.parties || {})) { let num = 0, den = 0, n = 0; const byDim = {};
    for (const q of answered) { const c = q.positions[slug]; if (!c || typeof c.position !== 'number') continue; if (dropLow && c.confidence === 'low') continue;
      const u = st.answers[q.id]; let p = c.position;
      if (shift && Math.abs(p) === 1) { const d = u !== p ? Math.sign(u - p) : -Math.sign(p); p = Math.max(-2, Math.min(2, p + shift * d)) }
      const w = W[(st.weights || {})[q.id] || 'normal']; const a = 1 - Math.abs(u - p) / 4; num += w * a; den += w; n++; (byDim[q.dimension] = byDim[q.dimension] || []).push(a) }
    if (!n) continue; out.push({ slug, name: meta.name, n, M, raw: num / den, match: (num + k * .5) / (den + k), inRanking: n >= need, dims: Object.fromEntries(Object.entries(byDim).map(([d, arr]) => [d, arr.reduce((x, y) => x + y, 0) / arr.length])) }) }
  return out.sort((a, b) => b.match - a.match) }
function dimPositions(Q, st) { const dims = {}; for (const q of Q.statements) { const d = dims[q.dimension] = dims[q.dimension] || { label: q.dimension_label, a: q.pole_a, b: q.pole_b, user: [], parties: {} };
    if (typeof st.answers[q.id] === 'number') d.user.push(q.polarity_sign * st.answers[q.id]);
    for (const [slug, c] of Object.entries(q.positions)) if (c && typeof c.position === 'number') (d.parties[slug] = d.parties[slug] || []).push(q.polarity_sign * c.position) }
  const mean = a => a.length ? a.reduce((x, y) => x + y, 0) / a.length : null;
  return Object.fromEntries(Object.entries(dims).map(([k, d]) => [k, { ...d, user: d.user.length >= 2 ? mean(d.user) : null, parties: Object.fromEntries(Object.entries(d.parties).filter(([, a]) => a.length >= 2).map(([s, a]) => [s, mean(a)])) }])) }
// Every party, with a likely range: min–max of the shrunk score, the raw score, the score without low-confidence cells,
// and the scores with ±1 cells moved one step toward / away from you. Buckets come from the shrunk score.
function q2Results(Q, st) {
  const by = a => Object.fromEntries(a.map(x => [x.slug, x]));
  const base = by(q2Scores(Q, st)), low = by(q2Scores(Q, st, { dropLow: true })), tw = by(q2Scores(Q, st, { shift: 1 })), aw = by(q2Scores(Q, st, { shift: -1 }));
  const M = Q.statements.filter(q => typeof st.answers[q.id] === 'number').length; const need = Math.max(10, Math.ceil(0.5 * M));
  return chooseParties().map(slug => { const meta = (Q.parties || {})[slug] || {}; const b = base[slug]; const limited = meta.in_default_ranking === false;
    const common = { slug, M, need, limited, coded: meta.positions_recorded, lowCells: meta.low_confidence_cells };
    if (!b) return { ...common, n: 0, thin: true, bucket: 'thin' };
    const vals = [b.match, b.raw, (low[slug] || {}).match, (tw[slug] || {}).match, (aw[slug] || {}).match].filter(v => typeof v === 'number');
    const m = Math.round(b.match * 100); const thin = !b.inRanking || limited;
    return { ...common, ...b, lo: Math.round(Math.min(...vals) * 100), hi: Math.round(Math.max(...vals) * 100), m, thin, bucket: thin ? 'thin' : m >= 70 ? 'strong' : m >= 55 ? 'moderate' : 'weak' } }) }
const BUCKET = { strong: 'Strong', moderate: 'Moderate', weak: 'Weak', thin: 'Too few positions' };
function q2Explainer(q) { if (q.explainer) return esc(q.explainer);
  const toA = q.polarity_sign >= 0; const lab = esc(q.dimension_label || QDIM_SHORT[q.dimension] || '');
  return `This statement is one of the ones on <b>${lab}</b>. Agreeing with it puts you nearer “${esc(toA ? q.pole_a : q.pole_b)}”; disagreeing puts you nearer “${esc(toA ? q.pole_b : q.pole_a)}”. There’s no right answer, and “Neutral” or “Skip” are fine if you’re unsure.` }

V.match = (arg) => {
  const Q = G().quiz2; if (!Q || !(Q.statements || []).length) { $('#main').innerHTML = sectionFrame('choose', 'choose/quiz', `${chooseHead('choose', 'Choose · Find your match', 'Find your match', '')}<p class="soft">The quiz is being rebuilt on a published method. Check back soon.</p>`); return }
  const st = q2State(); st.answers = st.answers || {}; st.weights = st.weights || {}; if (!st.seed) { st.seed = Math.floor(Math.random() * 1e9) + 1; q2Save(st) }
  const order = shuffled(Q.statements.map(q => q.id), st.seed); const byId = Object.fromEntries(Q.statements.map(q => [q.id, q])); const N = order.length; let i = Math.min(st.i || 0, N);
  const dimTotal = d => Q.statements.filter(q => q.dimension === d).length;
  const dimDone = d => Q.statements.filter(q => q.dimension === d && typeof st.answers[q.id] === 'number').length;
  const intro = () => { const n = Object.keys(st.answers).filter(id => byId[id]).length; const done = i >= N;
    $('#main').innerHTML = sectionFrame('choose', 'choose/quiz', `
      ${chooseHead('choose', 'Choose · Find your match', 'Which parties think like you?', `${N} statements on six themes, written without party names. At the end you’ll see all ${chooseParties().length} parties A to Z, how closely each one’s recorded positions match yours, and how much we know about each one’s views.`)}
      <div class="row">${done ? `<a class="btn btn--primary btn--l" href="#/choose/results">See your results ${ic('chev', 'i--s')}</a><button class="btn btn--l" type="button" id="qstart">Change my answers</button>` : `<button class="btn btn--primary btn--l" type="button" id="qstart">${n ? 'Continue' : 'Start'} ${ic('chev', 'i--s')}</button>${n ? '<a class="btn btn--l" href="#/choose/results">Results so far</a>' : ''}`}${n ? '<button class="btn btn--quiet" type="button" id="qreset">Start over</button>' : ''}</div>
      <div class="split split--7-5">
        <section class="stack">
          <div class="shead"><h2 class="h3">How it works</h2></div>
          <ol class="ideas">
            <li><div><b>Say how much you agree</b><span class="small soft">Five steps from strongly disagree to strongly agree, or skip. Mark the ones that matter a lot to you.</span></div></li>
            <li><div><b>Then see every party</b><span class="small soft">All ${chooseParties().length}, A to Z, each as a likely range with how many of your answers it could be compared on. Parties with too few recorded positions are shown but not compared.</span></div></li>
            <li><div><b>Check the evidence</b><span class="small soft">“Why” on each party shows its position on every statement you answered, with the source.</span></div></li>
          </ol>
          <p class="small soft">Positions were placed by two independent coders from manifestos, recorded votes and leaders’ statements, then reconciled (they agreed within one point on ${esc(String(((Q.agreement || {}).within1_pct) ?? 99.6))}% of positions). Statements come in a different order for everyone. Quiz ${esc(Q.version || '')}, frozen ${esc(Q.freeze_date || '')}.</p>
          <a class="more small" href="#/about/page/guide/quiz-method.md">Method and full audit table ${ic('chev', 'i--xs')}</a>
        </section>
        <aside class="stack">
          <div class="locked">${ic('lock')}<div><b>Parties’ positions appear after you answer,</b> so you decide on the substance first.</div></div>
          <div class="note">${ic('shield')}<div><b>Your answers stay on this device.</b> Nothing is sent or stored by us.</div></div>
        </aside>
      </div>`);
    $('#qstart').onclick = () => { if (i >= N) i = 0; ask() };
    const z = $('#qreset'); if (z) z.onclick = () => { st.answers = {}; st.weights = {}; st.i = 0; i = 0; q2Save(st); intro() } };
  const ask = () => { if (i >= N) { st.i = N; q2Save(st); go('choose/results'); return }
    const q = byId[order[i]]; const a = st.answers[q.id]; const w = st.weights[q.id] || 'normal'; const last = i === N - 1;
    const tabFor = v => (typeof a === 'number' ? a === v : v === SCALE[0][0]) ? 0 : -1;
    $('#main').innerHTML = `<div class="split split--7-5 quizq">
      <section class="stack stack--l" aria-labelledby="stmt">
        <div class="quizbar">
          <div class="quizbar__meta"><span><b>${i + 1}</b> of ${N}</span><a class="small" href="#/choose/results">Results so far</a></div>
          <div class="quizbar__dims" aria-hidden="true">${QDIMS.map(d => `<i style="--p:${Math.round(dimDone(d) / Math.max(1, dimTotal(d)) * 100)}%"${d === q.dimension ? ' aria-current="step"' : ''}></i>`).join('')}</div>
        </div>
        <p id="stmt" class="statement" tabindex="-1">${esc(q.text)}</p>
        <details class="disclose" style="border-top:1px solid var(--line)"><summary>What does this mean?</summary><div class="disclose__body"><p>${q2Explainer(q)}</p>
          <p class="src">${ic('doc')} Written without party names · positions checked by two coders · <a href="#/about/page/guide/quiz-method.md">method</a></p></div></details>
        <div class="likert" role="radiogroup" aria-labelledby="stmt"><div class="likert__opts">${SCALE.map(([v, l]) => `<button class="likert__opt" role="radio" type="button" data-v="${v}" aria-checked="${a === v}" tabindex="${tabFor(v)}"><span class="likert__dot">${TICK}</span>${l}</button>`).join('')}</div></div>
        <div class="field"><span class="field__label" id="implab">How much does this matter to you?</span><div class="seg seg--block" role="group" aria-labelledby="implab" id="qimp">${IMP.map(([k, l]) => `<button type="button" data-w="${k}" aria-pressed="${w === k}">${l}</button>`).join('')}</div></div>
        <div class="quiz-nav"><button class="btn btn--quiet" type="button" id="qback"${i === 0 ? ' disabled' : ''}>${ic('back', 'i--s')} Back</button><button class="btn btn--quiet" type="button" id="qskip">Skip, no opinion</button><button class="btn btn--primary btn--l" type="button" id="qnext"${typeof a === 'number' ? '' : ' disabled'}>${last ? 'See results' : 'Next'} ${ic('chev', 'i--s')}</button></div>
      </section>
      <aside class="stack stack--l sticky">
        <div class="locked">${ic('lock')}<div><b>Parties’ positions on this appear after you answer,</b> so you decide on the substance first.</div></div>
        <div class="panel panel--sunk">
          <h2 class="h3">Six themes</h2>
          <div class="terms">${QDIMS.map(d => `<div class="term"><div class="term__h"><b>${esc(QDIM_SHORT[d])}</b><span class="muted">${dimDone(d)} of ${dimTotal(d)}</span></div><div class="bar" style="height:6px"><i style="--w:${Math.round(dimDone(d) / Math.max(1, dimTotal(d)) * 100)}%;--pc:var(--signal)"></i></div></div>`).join('')}</div>
          <p class="small soft">Statements come in a different order for everyone, so no theme always comes first. Saved on this device as you go.</p>
          <a class="more small" href="#/about/page/guide/quiz-method.md">How the matching works ${ic('chev', 'i--xs')}</a>
        </div>
      </aside></div>`;
    focusMode('Find your match', 'choose');
    const opts = [...$('#main').querySelectorAll('.likert__opt')];
    const pickOpt = (b, focus) => { st.answers[q.id] = +b.dataset.v; q2Save(st); opts.forEach(x => { const on = x === b; x.setAttribute('aria-checked', on); x.tabIndex = on ? 0 : -1 }); if (focus) b.focus(); $('#qnext').disabled = false };
    opts.forEach((b, k) => { b.onclick = () => pickOpt(b);
      b.onkeydown = e => { const d = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key]; if (!d) return; e.preventDefault(); pickOpt(opts[(k + d + opts.length) % opts.length], true) } });
    $('#qimp').onclick = e => { const b = e.target.closest('[data-w]'); if (!b) return; st.weights[q.id] = b.dataset.w; q2Save(st); $('#qimp').querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x.dataset.w === b.dataset.w)) };
    const step = d => { i = Math.max(0, i + d); st.i = i; q2Save(st); ask(); window.scrollTo(0, 0); const s = $('#stmt'); if (s) s.focus({ preventScroll: true }) };
    $('#qnext').onclick = () => step(1); $('#qskip').onclick = () => { delete st.answers[q.id]; step(1) }; $('#qback').onclick = () => step(-1) };
  if (arg === 'start') { if (i >= N) i = 0; ask() } else if (Object.keys(st.answers).length && i < N) ask(); else intro();
};

/* ----- match results (rendered inside V.results) ----- */
function renderMatchResults(box, Q) {
  const st = q2State(); st.answers = st.answers || {}; st.weights = st.weights || {};
  const N = Q.statements.length; const byId = Object.fromEntries(Q.statements.map(q => [q.id, q]));
  const R = q2Results(Q, st); const M = R.length ? R[0].M : 0; const need = Math.max(10, Math.ceil(0.5 * M)); const sort = st.sort || 'az';
  const head = `<div class="shead"><div class="shead__row"><h2 id="h-match">Find your match</h2><span class="micro muted">${M} of ${N} answered · Quiz ${esc(Q.version || '')} · frozen ${esc(Q.freeze_date || '')}</span></div></div>`;
  if (!M) { box.innerHTML = `${head}<div class="panel panel--sunk"><p><b>No answers yet.</b></p><p class="small soft">${N} statements on six themes, written without party names. About 8 minutes.</p><a class="btn btn--primary btn--s" href="#/choose/quiz" style="justify-self:start">Start the quiz ${ic('chev', 'i--xs')}</a></div>`; return }
  const az = chooseAZ(R.map(r => r.slug)); const ballot = chooseBallot(R.map(r => r.slug));
  const rows = sort === 'close' ? R.slice().sort((x, y) => (x.thin - y.thin) || ((y.m ?? -1) - (x.m ?? -1)) || az.indexOf(x.slug) - az.indexOf(y.slug)) : sort === 'ballot' ? ballot.map(s => R.find(r => r.slug === s)) : az.map(s => R.find(r => r.slug === s));
  const reason = r => r.n === 0 ? 'No recorded position on the statements you answered' : r.limited ? `Not compared: positions found on only ${r.coded} of ${N} statements` : `Not compared: only ${r.n} of your ${M} answers could be matched (needs ${need})`;
  const mrow = (r, k) => `<div class="mrow${r.thin ? ' mrow--thin' : ''}" style="--pc:${pcolor(r.slug)}">
      <span class="mrow__name"><span class="sw"></span><span>${esc(pname(r.slug))}</span></span>
      <span class="row row--nowrap" style="gap:6px"><span class="bucket bucket--${r.bucket}">${BUCKET[r.bucket]}</span><button class="btn btn--s btn--quiet" type="button" data-why="${esc(r.slug)}" aria-label="Why: ${esc(pname(r.slug))}, statement by statement">Why</button></span>
      <div class="mrow__bar" style="--lo:${r.thin ? 0 : r.lo}%;--hi:${r.thin ? 0 : r.hi}%;--m:${r.thin ? 0 : r.m}%;--i:${k}" role="img" aria-label="${esc(pname(r.slug))}: ${r.thin ? 'too few positions to compare' : `${BUCKET[r.bucket].toLowerCase()} agreement, likely between ${r.lo} and ${r.hi} percent`}"><i></i><b></b></div>
      <span class="mrow__cov"><span class="coverage"><i style="--c:${Math.round(r.n / Math.max(1, M) * 100)}%"></i>Positions on ${r.n} of your ${M}</span>${r.thin ? `<span>${reason(r)}</span>` : `<span>Likely ${r.lo}–${r.hi} of 100</span>`}</span></div>`;
  const dims = dimPositions(Q, st); const dimKeys = QDIMS.filter(d => dims[d]);
  const withDims = az.filter(s => Object.values(dims).some(d => d.parties[s] != null));
  const cmp = (st.cmp || []).filter(s => withDims.includes(s)).slice(0, 2);
  const pctA = v => Math.round((2 - v) / 4 * 100);
  box.innerHTML = `${head}
    <h3 class="h2" style="margin-top:calc(-1 * var(--s-2))">How each party’s positions compare with yours</h3>
    <p class="lede">All ${R.length} parties. Each bar is a likely range, not a precise score, so parties whose ranges overlap are about as close to you as each other.</p>
    <div class="row"><span class="micro muted">Sort</span><div class="seg" role="group" aria-label="Sort parties">${[['az', 'A–Z'], ['close', 'Closest first'], ['ballot', 'Ballot order']].map(([k, l]) => `<button type="button" data-sort="${k}" aria-pressed="${sort === k}">${l}</button>`).join('')}</div>
      <button class="btn btn--s" type="button" id="qshare">${ic('share', 'i--xs')} Share all ${R.length}</button><a class="btn btn--s btn--quiet" href="#/choose/quiz/start">Change answers</a></div>
    <div class="split split--7-5">
      <section class="stack" aria-label="Every party">
        <div class="legend"><span><i class="bucket bucket--strong">Strong</i> 70+</span><span><i class="bucket bucket--moderate">Moderate</i> 55–69</span><span><i class="bucket bucket--weak">Weak</i> under 55</span><span><i class="bucket bucket--thin">Too few positions</i></span></div>
        <div>${rows.map(mrow).join('')}</div>
        <p class="micro muted">${sort === 'close' ? 'Sorted by the middle of each range; parties with too few positions go last. Small differences mean nothing.' : sort === 'ballot' ? 'Ballot order: A–Z by each party’s full registered name.' : 'A–Z by short name.'} Bars show the score with and without the pull toward 50, with low-confidence positions set aside, and with ±1 positions moved a step either way.</p>
      </section>
      <aside class="stack stack--l">
        <section class="stack" aria-labelledby="h-dims">
          <div class="shead"><h2 id="h-dims" class="h3">Where you sit on each theme</h2></div>
          <p class="small soft">Pick up to two parties to put beside you.</p>
          <div class="chips chips--scroll" role="group" aria-label="Compare with up to two parties">${withDims.map(s => `<button class="chip" type="button" data-cmp="${esc(s)}" aria-pressed="${cmp.includes(s)}" style="--pc:${pcolor(s)}"><span class="sw"></span>${esc(pname(s))}</button>`).join('')}</div>
          <div class="legend"><span><span class="dim__pt dim__pt--you" style="position:static;margin:0;display:inline-block"></span> You</span>${cmp.map(s => `<span><span class="ptag ptag--s" style="--pc:${pcolor(s)}"><span class="sw"></span>${esc(pname(s))}</span></span>`).join('')}</div>
          <div class="dims">${dimKeys.map(k => { const d = dims[k]; const pts = cmp.filter(s => d.parties[s] != null);
            const lab = [d.user != null ? `you at ${pctA(d.user)} of 100` : 'not enough of your answers', ...pts.map(s => `${pname(s)} ${pctA(d.parties[s])}`)].join('; ');
            return `<div class="dim"><div class="dim__h"><b>${esc(QDIM_SHORT[k] || d.label)}</b>${d.user == null ? '<span class="micro muted">Answer 2+ to place you</span>' : ''}</div>
              <div class="dim__axis" role="img" aria-label="${esc(QDIM_SHORT[k] || d.label)} (0 = ${esc(d.a)}, 100 = ${esc(d.b)}): ${esc(lab)}">${pts.map(s => `<span class="dim__pt" style="--x:${pctA(d.parties[s])}%;--pc:${pcolor(s)}"></span>`).join('')}${d.user != null ? `<span class="dim__pt dim__pt--you" style="--x:${pctA(d.user)}%"></span>` : ''}</div>
              <div class="dim__ends"><span>${esc(d.a)}</span><span>${esc(d.b)}</span></div></div>` }).join('')}</div>
          <p class="micro muted">The ends describe the statements, not left or right. This map is an illustration; the list uses every statement.</p>
        </section>
        ${chooseUnknowns([`${N} statements can’t cover everything a party stands for: competence, trust, local candidates and who they’d work with aren’t here.`, 'Some parties have published little; we never guess a position, so their bars are hatched rather than placed.', 'Positions are coded from documents by people. Two coders agreed closely, but a party could fairly be placed a step either way; the ranges show what that would do.', 'Your policy swipe and values compass may point elsewhere. They measure different things.'])}
      </aside>
    </div>`;
  box.querySelectorAll('[data-sort]').forEach(b => b.onclick = () => { const s2 = q2State(); s2.sort = b.dataset.sort; q2Save(s2); renderMatchResults(box, Q) });
  box.querySelectorAll('[data-cmp]').forEach(b => b.onclick = () => { const s2 = q2State(); let c = (s2.cmp || []).filter(s => withDims.includes(s)); const s = b.dataset.cmp;
    if (c.includes(s)) c = c.filter(x => x !== s); else { c.push(s); if (c.length > 2) c.shift() } s2.cmp = c; q2Save(s2); renderMatchResults(box, Q); const nb = box.querySelector(`[data-cmp="${CSS.escape(s)}"]`); if (nb) nb.focus({ preventScroll: true }) });
  $('#qshare', box).onclick = () => { const text = [`Ballot Book NZ · Find your match (quiz ${Q.version || ''})`, `My answers on ${M} of ${N} statements compared with all ${R.length} parties, A–Z:`, '',
      ...az.map(s => { const r = R.find(x => x.slug === s); return `${pname(s)}: ${r.thin ? 'too few positions to compare' : `${BUCKET[r.bucket].toLowerCase()} (likely ${r.lo}–${r.hi} of 100)`}` }), '',
      'Information, not advice: it shows how answers line up with published positions, and is not a recommendation about how to vote.', chooseShareURL('choose/quiz')].join('\n');
    chooseCopy(text, 'Share all ' + R.length) };
  box.querySelectorAll('[data-why]').forEach(b => b.onclick = () => q2Why(Q, st, b.dataset.why, R.find(r => r.slug === b.dataset.why)));
}
function q2Why(Q, st, p, r) {
  const lab = v => (SCALE.find(x => x[0] === v) || [0, '–'])[1]; const tiers = Q.evidence_tiers || {};
  const order = shuffled(Q.statements.map(q => q.id), st.seed); const byId = Object.fromEntries(Q.statements.map(q => [q.id, q]));
  const ids = order.filter(id => typeof st.answers[id] === 'number');
  const imp = { less: 'matters less', very: 'matters a lot' };
  const rows = ids.map(id => { const q = byId[id]; const c = q.positions[p]; const u = st.answers[id]; const has = c && typeof c.position === 'number';
    const ev = c && c.evidence ? String(c.evidence) : ''; const short = ev.length > 420 ? ev.slice(0, 420).replace(/\s+\S*$/, '') + '…' : ev;
    return `<article class="qwhy__row${has ? '' : ' qwhy__row--none'}"><p class="qwhy__s">${esc(q.text)}</p>
      <dl class="dl"><dt>You</dt><dd>${lab(u)}${imp[(st.weights || {})[id]] ? ` <span class="muted">· ${imp[st.weights[id]]}</span>` : ''}</dd>
        <dt>${esc(pname(p))}</dt><dd>${has ? lab(c.position) + (c.position === 0 ? ' (argued neutral)' : '') : '<span class="muted">No evidenced position, so left out</span>'}</dd>
        ${has ? `<dt>Agreement</dt><dd>${Math.round((1 - Math.abs(u - c.position) / 4) * 100)} of 100</dd>` : ''}</dl>
      ${short ? `<p class="small soft">${esc(short)}</p>${ev.length > short.length ? `<details class="disclose qwhy__ev"><summary class="small">Full evidence</summary><div class="disclose__body small"><p>${esc(ev)}</p></div></details>` : ''}` : ''}
      ${has ? chooseSrc([c.source_url, c.source_url_2], [c.tier ? `Tier ${c.tier}${tiers[c.tier] ? ': ' + esc(tiers[c.tier]) : ''}` : '', c.confidence ? esc(c.confidence) + ' confidence' : ''].filter(Boolean).join(' · ')) : ''}</article>` }).join('');
  openSheet({ title: `You and ${pname(p)}`, depth: ['Your results', 'Evidence'], at: 1,
    src: `Coded by two coders from published sources · Quiz ${esc(Q.version || '')}, frozen ${esc(Q.freeze_date || '')} · <a href="#/about/page/guide/quiz-method.md">method</a>`,
    html: `<div class="stack"><p class="small soft">Each statement you answered, your answer, ${esc(pname(p))}’s coded position and the evidence behind it.${r ? ` ${r.n} of your ${r.M} answers could be compared${r.thin ? ', which is too few for a fair comparison' : `; likely ${r.lo}–${r.hi} of 100`}.` : ''}</p>
      <div class="qwhy">${rows || '<p class="muted">Answer some statements first.</p>'}</div>${RESULT_DISCLAIMER}</div>` }) }
