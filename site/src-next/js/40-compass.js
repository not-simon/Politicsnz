/* ----- Values compass -----
   Scoring per guide/compass-method.md: axis = 5 × mean(keyed answers), half-width = max(1, 1.96 × 5 × sd / √n).
   Questions run in focus mode with the same .likert as the quiz; results at #/choose/compass/results. */
function compassState() { try { const s = JSON.parse(store.get('compass') || '{}'); return s && typeof s === 'object' ? s : {} } catch { return {} } }
function axisScore(items, answers, axis, minItems) { const ks = items.filter(i => i.axis === axis && typeof answers[i.id] === 'number').map(i => i.direction * answers[i.id]);
  if (ks.length < minItems) return null; const m = ks.reduce((a, b) => a + b, 0) / ks.length; const sd = Math.sqrt(ks.reduce((a, b) => a + (b - m) ** 2, 0) / Math.max(1, ks.length - 1));
  return { score: 5 * m, n: ks.length, half: Math.max(1, 1.96 * 5 * sd / Math.sqrt(ks.length)) } }
function partyCompassPoints(C, CP, source) { const out = [];
  for (const [slug, p] of Object.entries((CP.parties || {}))) {
    if (source === 'published') { const cmp = p.comparison || {}; const e = cmp.gps2019_economic, so = cmp.gps2019_social; if (e && so && e.published != null && so.published != null) out.push({ slug, x: e.published, y: so.published, pop: (cmp.gps2019_populism || {}).published }) ; continue }
    const ans = {}; for (const [id, c] of Object.entries((p.coded || {}).items || {})) if (c && typeof c.position === 'number') ans[id] = c.position;
    const mins = (C.scoring && C.scoring.min_items) || { economic: 6, social: 8, populism: 4 };
    const ex = axisScore(C.items, ans, 'economic', mins.economic), sy = axisScore(C.items, ans, 'social', mins.social), pp = axisScore(C.items, ans, 'populism', mins.populism);
    out.push({ slug, x: ex && ex.score, y: sy && sy.score, pop: pp && pp.score, n: Object.keys(ans).length }) }
  return out }
const compassMins = C => (C.scoring && C.scoring.min_items) || { economic: 6, social: 8, populism: 4 };
function compassMe(C, answers) { const items = C.items || []; const mins = compassMins(C);
  return { x: axisScore(items, answers, 'economic', mins.economic), y: axisScore(items, answers, 'social', mins.social), pop: axisScore(items, answers, 'populism', mins.populism) } }
// Square plot, −10..+10 on both axes. size 'narrow' (360, phone) or 'wide' (560, desktop); CSS shows one.
function compassPlot(me, parties, { showMe = true, size = 'both' } = {}) {
  const one = (W, fs, cls) => { const pad = 28, H = W; const sx = v => pad + (v + 10) / 20 * (W - 2 * pad), sy = v => H - pad - (v + 10) / 20 * (H - 2 * pad);
    let g = `<rect class="cplot__bg" x="${pad}" y="${pad}" width="${W - 2 * pad}" height="${H - 2 * pad}" rx="10"/><g class="grid">`;
    for (let v = -10; v <= 10; v += 5) if (v) g += `<line x1="${sx(v)}" x2="${sx(v)}" y1="${pad}" y2="${H - pad}"/><line y1="${sy(v)}" y2="${sy(v)}" x1="${pad}" x2="${W - pad}"/>`;
    g += `</g><line class="cplot__axis" x1="${sx(0)}" x2="${sx(0)}" y1="${pad}" y2="${H - pad}"/><line class="cplot__axis" y1="${sy(0)}" y2="${sy(0)}" x1="${pad}" x2="${W - pad}"/>`;
    g += `<g class="cplot__ax" style="font-size:${fs}px"><text x="${W / 2}" y="${pad - 9}" text-anchor="middle">AUTHORITARIAN · TRADITIONAL</text><text x="${W / 2}" y="${H - pad + fs + 5}" text-anchor="middle">LIBERTARIAN · PLURALIST</text><text x="${pad + 6}" y="${H / 2 - 7}">LEFT</text><text x="${W - pad - 6}" y="${H / 2 - 7}" text-anchor="end">RIGHT</text></g>`;
    if (showMe && me && me.x && me.y) { const x0 = sx(me.x.score - me.x.half), x1 = sx(me.x.score + me.x.half), y0 = sy(me.y.score + me.y.half), y1 = sy(me.y.score - me.y.half);
      g += `<rect class="cplot__you" x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}" rx="8"><title>You: economic ${fmt(me.x.score - me.x.half, 0)} to ${fmt(me.x.score + me.x.half, 0)}, social ${fmt(me.y.score - me.y.half, 0)} to ${fmt(me.y.score + me.y.half, 0)}</title></rect>` }
    const placed = []; const pts = chooseAZ(parties.filter(p => p.x != null && p.y != null).map(p => p.slug)).map(s => parties.find(p => p.slug === s));
    g += pts.map(p => { const cx = sx(p.x), cy = sy(p.y); const label = pname(p.slug); const w = label.length * fs * .56 + 4, h = fs + 2;
      const cands = [[cx + 10, cy + fs / 3, 'start'], [cx - 10, cy + fs / 3, 'end'], [cx, cy - 11, 'middle'], [cx, cy + fs + 9, 'middle'], [cx + 10, cy - fs, 'start'], [cx + 10, cy + fs + 4, 'start'], [cx - 10, cy - fs, 'end'], [cx - 10, cy + fs + 4, 'end']];
      const box = ([x, y, a]) => { const l = a === 'start' ? x : a === 'end' ? x - w : x - w / 2; return [l, y - h + 3, l + w, y + 3] };
      const hit = b => b[0] < pad || b[2] > W - pad || b[1] < pad || b[3] > H - pad || placed.some(o => b[0] < o[2] && b[2] > o[0] && b[1] < o[3] && b[3] > o[1]);
      let c = cands.find(cd => !hit(box(cd))) || cands[0]; placed.push(box(c));
      return `<g class="cplot__p" style="--pc:${pcolor(p.slug)}"><circle cx="${cx}" cy="${cy}" r="7"><title>${esc(label)}: economic ${fmt(p.x, 0)}, social ${fmt(p.y, 0)}</title></circle><text x="${c[0]}" y="${c[1]}" text-anchor="${c[2]}" style="font-size:${fs}px">${esc(label)}</text></g>` }).join('');
    if (showMe && me && me.x && me.y) { const cx = sx(me.x.score), cy = sy(me.y.score); g += `<circle class="cplot__ring" cx="${cx}" cy="${cy}" r="8"/><text class="cplot__me" x="${cx}" y="${cy - 14}" text-anchor="middle" style="font-size:${fs + 1}px">You</text>` }
    return `<svg class="chart cplot ${cls}" viewBox="0 0 ${W} ${H}" role="img" aria-label="Values compass: economic left to right across, social libertarian to authoritarian up the page${showMe && me && me.x && me.y ? `; you are the shaded box` : ''}. The same positions are listed in the table below.">${g}</svg>` };
  if (size === 'narrow') return one(360, 12, '');
  return one(360, 12, 'chart--narrow') + one(560, 13, 'chart--wide') }
const compassWord = (v, lo, hi) => v == null ? '' : Math.abs(v) < 2 ? 'near the centre' : (v < 0 ? lo : hi) + (Math.abs(v) >= 6 ? ', strongly' : '');
const compassRange = a => `${fmt(Math.max(-10, a.score - a.half), 0)} to ${fmt(Math.min(10, a.score + a.half), 0)}`.replace(/-/g, '−');
function compassSentence(me) { return `${me.x ? `Economically you lean <b>${compassWord(me.x.score, 'left', 'right')}</b> (somewhere from ${compassRange(me.x)} on a −10 to +10 scale). ` : 'Answer at least 6 economic questions to place you on the economic axis. '}${me.y ? `Socially you lean <b>${compassWord(me.y.score, 'libertarian / pluralist', 'authoritarian / traditional')}</b> (${compassRange(me.y)}). ` : 'Answer at least 8 social questions for the social axis. '}${me.pop ? `On populism: <b>${compassWord(me.pop.score, 'pluralist', 'populist')}</b> (${compassRange(me.pop)}).` : ''}` }
// Small summary for Your results.
function compassSummaryHTML(st) { const C = G().compass || {}; const CP = G().compass_parties || {}; const me = compassMe(C, st.answers || {}); const n = Object.keys(st.answers || {}).length;
  const parties = partyCompassPoints(C, CP, st.source || 'coded');
  return `<div class="split split--5-7"><div class="stack"><p class="soft">${compassSentence(me)}</p><p class="micro muted">${n} of ${(C.items || []).length} answered · parties placed ${(st.source || 'coded') === 'coded' ? 'from their 2026 policies and votes' : 'by expert surveys (2019)'}. The shaded box is you, as a range.</p></div>
    <div class="cplot-s">${compassPlot(me, parties, { size: 'narrow' })}</div></div>` }

V.compass = (arg) => {
  const C = G().compass || {}; const CP = G().compass_parties || {}; const items = C.items || [];
  if (!items.length) { $('#main').innerHTML = sectionFrame('choose', 'choose/compass', `${chooseHead('compass', 'Choose · Values compass', 'Values compass', '')}<p class="soft">The compass questions are still being prepared.</p>`); return }
  const st = compassState(); st.answers = st.answers || {}; let i = Math.min(st.i || 0, items.length); let source = st.source || 'coded';
  const save = () => store.set('compass', JSON.stringify(st));
  const intro = () => { const n = Object.keys(st.answers).length;
    $('#main').innerHTML = sectionFrame('choose', 'choose/compass', `
      ${chooseHead('compass', 'Choose · Values compass', 'Where do your values sit?', `${items.length} general questions about society, the economy and authority — nothing about New Zealand parties or this year’s policies. They come from established academic surveys and are scored on the two axes political scientists use, plus a populism measure.`)}
      <div class="row"><button class="btn btn--primary btn--l" type="button" id="cstart">${n ? (i >= items.length ? 'Change my answers' : 'Continue') : 'Start'} ${ic('chev', 'i--s')}</button>${n ? `<a class="btn btn--l" href="#/choose/compass/results">See my results</a><button class="btn btn--quiet" type="button" id="creset">Start over</button>` : ''}</div>
      <div class="split split--7-5">
        <section class="stack"><div class="shead"><h2 class="h3">What you’ll get</h2></div>
          <p class="soft">Your position as a range on two axes — economic left–right and social libertarian–authoritarian — with the ${chooseParties().length} registered parties plotted on the same axes, placed two ways: from their 2026 policy documents and votes, and from published expert surveys.</p>
          <p class="small soft">Questions come from the World Values Survey, the Comparative Study of Electoral Systems, the NZ Election Study and two published psychology scales.</p>
          <a class="more small" href="#/about/page/guide/compass-method.md">How it works and where the questions come from ${ic('chev', 'i--xs')}</a></section>
        <aside class="stack"><div class="note">${ic('shield')}<div><b>Your answers stay on this device.</b> Nothing is sent or stored by us.</div></div></aside>
      </div>`);
    $('#cstart').onclick = () => { if (i >= items.length) i = 0; ask() };
    const z = $('#creset'); if (z) z.onclick = () => { st.answers = {}; st.i = 0; i = 0; save(); intro() } };
  const ask = () => { if (i >= items.length) { st.i = items.length; save(); go('choose/compass/results'); return }
    const q = items[i]; const a = st.answers[q.id]; const labels = (q.scale && q.scale.labels) || ['Strongly disagree', 'Disagree', 'Neither', 'Agree', 'Strongly agree']; const vals = (q.scale && q.scale.values) || [-2, -1, 0, 1, 2];
    const axes = ['economic', 'social', 'populism']; const tot = ax => items.filter(x => x.axis === ax).length; const done = ax => items.filter(x => x.axis === ax && typeof st.answers[x.id] === 'number').length;
    const last = i === items.length - 1;
    $('#main').innerHTML = `<div class="split split--7-5 quizq">
      <section class="stack stack--l" aria-labelledby="stmt">
        <div class="progress-line"><b>${i + 1} of ${items.length}</b><div class="bar"><i style="--w:${Math.round(i / items.length * 100)}%"></i></div><a class="small" href="#/choose/compass/results">Results so far</a></div>
        <p id="stmt" class="statement" tabindex="-1">${esc(q.text)}</p>
        ${q.scale && q.scale.type === 'feeling5' ? '<p class="soft">How do you feel about this?</p>' : ''}
        <div class="likert" role="radiogroup" aria-labelledby="stmt"><div class="likert__opts">${vals.map((v, k) => `<button class="likert__opt" role="radio" type="button" data-v="${v}" aria-checked="${a === v}" tabindex="${(typeof a === 'number' ? a === v : k === 0) ? 0 : -1}"><span class="likert__dot">${TICK}</span>${esc(labels[k])}</button>`).join('')}</div></div>
        <div class="quiz-nav"><button class="btn btn--quiet" type="button" id="qback"${i === 0 ? ' disabled' : ''}>${ic('back', 'i--s')} Back</button><button class="btn btn--quiet" type="button" id="qskip">Skip, no opinion</button><button class="btn btn--primary btn--l" type="button" id="qnext"${typeof a === 'number' ? '' : ' disabled'}>${last ? 'See results' : 'Next'} ${ic('chev', 'i--s')}</button></div>
        <p class="src">${ic('doc')} Source: ${esc((q.source && q.source.instrument) || '')}</p>
      </section>
      <aside class="stack stack--l sticky"><div class="panel panel--sunk"><h2 class="h3">Three measures</h2>
        <div class="terms">${axes.map(ax => `<div class="term"><div class="term__h"><b>${{ economic: 'Economic', social: 'Social', populism: 'Populism' }[ax]}</b><span class="muted">${done(ax)} of ${tot(ax)}</span></div><div class="bar" style="height:6px"><i style="--w:${Math.round(done(ax) / Math.max(1, tot(ax)) * 100)}%;--pc:var(--signal)"></i></div></div>`).join('')}</div>
        <p class="small soft">You need at least ${compassMins(C).economic} economic and ${compassMins(C).social} social answers to be placed. Nothing here mentions a party.</p></div></aside></div>`;
    focusMode('Values compass', 'choose');
    const opts = [...$('#main').querySelectorAll('.likert__opt')];
    const pickOpt = (b, focus) => { st.answers[q.id] = +b.dataset.v; save(); opts.forEach(x => { const on = x === b; x.setAttribute('aria-checked', on); x.tabIndex = on ? 0 : -1 }); if (focus) b.focus(); $('#qnext').disabled = false };
    opts.forEach((b, k) => { b.onclick = () => pickOpt(b); b.onkeydown = e => { const d = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key]; if (!d) return; e.preventDefault(); pickOpt(opts[(k + d + opts.length) % opts.length], true) } });
    const step = d => { i = Math.max(0, i + d); st.i = i; save(); ask(); window.scrollTo(0, 0); const s = $('#stmt'); if (s) s.focus({ preventScroll: true }) };
    $('#qnext').onclick = () => step(1); $('#qskip').onclick = () => { delete st.answers[q.id]; step(1) }; $('#qback').onclick = () => step(-1) };
  const results = () => {
    if (isElectionDay()) { $('#main').innerHTML = sectionFrame('choose', 'choose/compass', chooseHead('compass', 'Choose · Values compass', 'Where you sit', '') + chooseLock()); return }
    const me = compassMe(C, st.answers); const parties = partyCompassPoints(C, CP, source); const answered = Object.keys(st.answers).length;
    const shown = parties.filter(p => p.x != null && p.y != null); const missing = chooseAZ(chooseParties().filter(s => !shown.some(p => p.slug === s)));
    const pops = chooseAZ(parties.filter(p => p.pop != null).map(p => p.slug)).map(s => parties.find(p => p.slug === s));
    const popRow = (name, v, pc, you) => `<div class="tally__row" style="--pc:${pc}">${you ? `<span class="small"><b>${name}</b></span>` : `<span class="ptag ptag--s"><span class="sw"></span>${name}</span>`}<div class="bar" role="img" aria-label="${name}: ${fmt(v, 0)} on −10 to +10"><i style="--w:${Math.round((v + 10) / 20 * 100)}%"></i></div><span class="tally__v">${fmt(v, 0).replace('-', '−')}</span></div>`;
    $('#main').innerHTML = sectionFrame('choose', 'choose/compass', `
      ${chooseHead('compass', `Choose · Values compass · ${answered} of ${items.length} answered`, 'Where you sit', '')}
      <p class="lede">${compassSentence(me)}</p>
      <div class="row"><span class="micro muted">Place the parties</span><div class="seg" role="group" aria-label="How parties are placed"><button type="button" data-src="coded" aria-pressed="${source === 'coded'}">From 2026 policies &amp; votes</button><button type="button" data-src="published" aria-pressed="${source === 'published'}">From expert surveys (2019)</button></div></div>
      <div class="split split--7-5">
        <section class="stack">
          <div class="cplot-wrap">${compassPlot(me, parties)}</div>
          <p class="small soft">The shaded box is you: a range, from how many questions you answered and how consistent your answers were. ${source === 'coded' ? 'Party points: each party “answered” the same questions from its manifesto, policy documents, votes and leaders’ statements, with evidence for every cell; parties with too few evidenced answers on an axis are not shown.' : 'Party points: Global Party Survey 2019 (experts rated the five parliamentary parties of 2019; smaller parties and Te Pāti Māori were not rated), rescaled to these axes.'}</p>
          ${missing.length ? `<p class="micro muted">Not placed (${source === 'coded' ? 'too few evidenced answers' : 'not rated'}): ${missing.map(s => esc(pname(s))).join(', ')}.</p>` : ''}
          <details class="disclose"><summary>Positions as a list</summary><div class="disclose__body"><div class="table-wrap"><table class="table"><thead><tr><th>Party (A–Z)</th><th class="n">Economic</th><th class="n">Social</th></tr></thead><tbody>
            ${me.x && me.y ? `<tr><td><b>You</b></td><td class="n">${compassRange(me.x)}</td><td class="n">${compassRange(me.y)}</td></tr>` : ''}
            ${chooseAZ(shown.map(p => p.slug)).map(s => { const p = shown.find(x => x.slug === s); return `<tr><td><span class="sw" style="--pc:${pcolor(s)}"></span> ${esc(pname(s))}</td><td class="n">${fmt(p.x, 0).replace('-', '−')}</td><td class="n">${fmt(p.y, 0).replace('-', '−')}</td></tr>` }).join('')}</tbody></table></div><p class="micro muted">−10 = left / libertarian, +10 = right / authoritarian.</p></div></details>
        </section>
        <aside class="stack stack--l">
          ${me.pop || pops.length ? `<section class="stack"><div class="shead"><h2 class="h3">Populism</h2></div><p class="small soft">A secondary measure: higher means more anti-establishment. Indicative only. A–Z.</p><div class="tally ctally">${me.pop ? popRow('You', me.pop.score, 'var(--signal)', true) : ''}${pops.map(p => popRow(esc(pname(p.slug)), p.pop, pcolor(p.slug))).join('')}</div></section>` : ''}
          ${chooseUnknowns(['A two-axis map flattens politics: parties and people differ on things it doesn’t measure, such as Te Tiriti, the environment, competence and who they’d work with.', 'Party positions coded from documents tend to look more polarised than expert ratings; both are shown so you can see the gap.', 'Your range shrinks as you answer more questions. With only a few answers it’s wide for a reason.', 'This is not a voting recommendation. For 2026 policies, use <a href="#/choose/quiz">Find your match</a>.'], ['Full method, item sources and licences', 'guide/compass-method.md'])}
        </aside>
      </div>
      <div class="row"><button class="btn btn--primary" type="button" id="cagain">${i >= items.length ? 'Change my answers' : 'Keep answering'}</button><a class="btn" href="#/choose/results">All your results</a><button class="btn btn--quiet" type="button" id="creset2">Start over</button></div>
      ${RESULT_DISCLAIMER}`);
    $('#main').querySelectorAll('[data-src]').forEach(b => b.onclick = () => { source = b.dataset.src; st.source = source; save(); const y = scrollY; results(); scrollTo(0, y) });
    $('#cagain').onclick = () => { i = i >= items.length ? 0 : i; ask() }; $('#creset2').onclick = () => { st.answers = {}; st.i = 0; i = 0; save(); intro() } };
  if (arg === 'results') results(); else if (arg === 'start') { if (i >= items.length) i = 0; ask() } else if (Object.keys(st.answers).length && i < items.length) ask(); else intro();
};
