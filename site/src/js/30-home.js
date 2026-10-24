/* ===== Today (home): phase hero, four tasks, two votes, the Today feed, resume (site/redesign/mockups/home.html) ===== */
// NZ calendar helpers (all "today" logic uses the NZ date so everyone sees the same thing on the same day)
function nzToday() { const t = nzNow(); const y = t.getFullYear(), m = t.getMonth() + 1, d = t.getDate(); const p = n => String(n).padStart(2, '0');
  return { y, m, d, md: `${p(m)}-${p(d)}`, iso: `${y}-${p(m)}-${p(d)}`, n: Math.round(Date.UTC(y, m - 1, d) / 864e5), num: y * 10000 + m * 100 + d } }
const NZ_MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
function nzDateLong() { return nzNow().toLocaleDateString('en-NZ', { weekday: 'long', day: 'numeric', month: 'long' }) }
const shortDate = s => { const m = String(s || '').match(/^(\d{4})-(\d{2})-(\d{2})/); return m ? `${+m[3]} ${NZ_MON[+m[2] - 1]}` : '' };
function hashStr(s) { let h = 2166136261; for (const c of String(s)) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619) } return h >>> 0 }
const extA = (href, html, cls = '') => `<a${cls ? ` class="${cls}"` : ''} href="${esc(href)}" target="_blank" rel="noopener">${html}</a>`;
const extIc = () => ic('ext', 'i--xs ext');
const lsJSON = (k, fn) => { if (typeof fn === 'function') { try { return fn() || {} } catch {} } try { return JSON.parse(store.get(k) || '{}') || {} } catch { return {} } };

// Phase hero copy (IA.md §2.2). Returns { n, eyebrow, h1, p, ctas, step }
function heroCopy(ph) {
  const t = nzToday(); const dl = daysLeft(); const toE = daysTo('2026-10-25'); const toFinal = daysTo('2026-11-27');
  const eyebrow = nzDateLong() + (dl > 0 ? ` · ${dl} day${dl === 1 ? '' : 's'} to election day` : '');
  const vnz = (l, primary = true) => `<a class="btn ${primary ? 'btn--primary' : 'btn--on-band'} btn--l" href="https://vote.nz" target="_blank" rel="noopener">${l} ${ic('ext', 'i--s ext')}</a>`;
  const mapA = (primary = true) => `<a class="btn ${primary ? 'btn--primary' : 'btn--on-band'} btn--l" href="https://map.vote.nz" target="_blank" rel="noopener">Find a voting place ${ic('ext', 'i--s ext')}</a>`;
  const inA = (href, l, primary = false) => `<a class="btn ${primary ? 'btn--primary' : 'btn--on-band'} btn--l" href="${href}">${l}</a>`;
  if (ph === 'enrol') return { n: toE > 0 ? toE : null, eyebrow, step: 0,
    h1: toE > 1 ? `days left<br>to enrol.` : toE === 1 ? `day left<br>to enrol.` : `Last day<br>to enrol.`,
    p: `Enrolment closes at midnight on Sunday 25 October. This year you can’t enrol at a voting place, so if you’ve moved or never enrolled, do it now. It takes about five minutes.`,
    ctas: vnz('Check I’m enrolled') + inA('#/vote', 'First vote? Start here') };
  if (ph === 'advance') return { n: dl > 0 ? dl : null, eyebrow: nzDateLong() + ' · voting is open', step: 1,
    h1: `${dl > 0 ? `day${dl === 1 ? '' : 's'} to go.<br>` : ''}Vote early, anywhere.`,
    p: `Advance voting is open at any voting place in the country until Friday 6 November. No ID is needed, and you can vote outside your own electorate. Hours vary, so check the official map first.`,
    ctas: mapA() + inA('#/vote/plan', 'Make a plan') };
  if (ph === 'electionday') return { n: null, eyebrow: nzDateLong() + ' · election day', step: 2,
    h1: `Today’s the day.`,
    p: `Voting places are open 9am to 7pm. You can vote at any voting place in New Zealand, and you don’t need ID or your EasyVote card.`,
    ctas: mapA() + inA('#/vote', 'What to expect inside') };
  if (ph === 'results') return { n: null, eyebrow: nzDateLong() + ' · voting has closed', step: 2,
    h1: `Results are<br>coming in.`,
    p: `These are preliminary election-night results. Special votes are counted later, so seats can still change; the official result is due on Friday 27 November.`,
    ctas: inA('#/seats/results', 'See the results', true) + inA('#/vote/specials', 'What specials could change') };
  if (t.num < 20261127) return { n: toFinal > 0 ? toFinal : null, eyebrow: nzDateLong() + ' · special votes are being counted', step: 3,
    h1: `${toFinal > 0 ? `day${toFinal === 1 ? '' : 's'} to the<br>` : ''}final result.`,
    p: `Special votes, including overseas votes, are being checked and counted. The official result is due on Friday 27 November; until then, seat counts can move.`,
    ctas: inA('#/vote/specials', 'What specials could change', true) + inA('#/seats/parliament', 'Parliament now') };
  return { n: null, eyebrow: nzDateLong(), step: 4, h1: `Forming a<br>government.`,
    p: `The official result is in. Under MMP one party rarely governs alone, so parties negotiate coalition or support agreements. There is no deadline for this.`,
    ctas: inA('#/seats/coalition', 'Coalition builder', true) + inA('#/vote/glossary', 'What the terms mean') } }

function heroHTML(ph) { const h = heroCopy(ph);
  const stops = [['Enrol', 'by Sun 25 Oct'], ['Vote early', '26 Oct – 6 Nov'], ['Election day', 'Sat 7 Nov'], ['Final result', 'Fri 27 Nov']];
  return `<section class="hero bleed" aria-labelledby="h-hero">
    <p class="eyebrow">${esc(h.eyebrow)}</p>
    <div class="hero__count">${h.n != null ? `<span class="figure countup" style="--to:${h.n}" aria-hidden="true"></span>` : ''}<h1 id="h-hero">${h.n != null ? `<span class="sr-only">${h.n} </span>` : ''}${h.h1}</h1></div>
    <p>${h.p}</p>
    <div class="hero__ctas">${h.ctas}</div>
    <ol class="track" aria-label="Election calendar">${stops.map(([b, s], i) => `<li${i === h.step ? ' aria-current="step"' : i < h.step ? ' data-done' : ''}><b>${b}</b>${s}</li>`).join('')}</ol>
  </section>` }

const TICK_SVG = (on = false) => `<svg class="tick${on ? ' is-on' : ''}" viewBox="0 0 28 28" aria-hidden="true"><circle cx="14" cy="14" r="12"/><path d="M8.5 14.5l3.6 3.6L19.5 10"/></svg>`;
function twoVotesHTML() { return `<div class="twovotes">
    <div><span class="twovotes__k">${TICK_SVG(true)} Party vote</span><span class="twovotes__big">Decides how many seats each party gets.</span><p>About 1% of the party vote is roughly 1 seat of 120. A party needs 5% of the party vote, or to win an electorate.</p></div>
    <div><span class="twovotes__k">${TICK_SVG(true)} Electorate vote</span><span class="twovotes__big">Picks your local MP.</span><p>The candidate with the most votes wins. You can give your two ticks to different parties, or use just one.</p></div>
  </div>` }

function rowlink(href, icon, title, sub) { return `<a class="rowlink" href="${href}"><span class="rowlink__icon">${ic(icon)}</span><span><span class="rowlink__title">${title}</span><span class="rowlink__sub" style="display:block">${sub}</span></span>${ic('chev')}</a>` }

/* ----- the Today feed ----- */
function potdCard() { const cards = (S.swipe || []).filter(c => c && c.statement && c.statement.length <= 220); if (!cards.length) return null;
  // equal chance for every registered party (some parties have far more cards than others), then one of its cards
  const reg = new Set((G().parties || []).map(p => p.slug)); const pool = reg.size && cards.some(c => reg.has(c.party)) ? cards.filter(c => reg.has(c.party)) : cards;
  const parties = [...new Set(pool.map(c => c.party))].sort(); const day = nzToday().iso;
  const party = parties[hashStr('potd-party:' + day) % parties.length];
  const mine = pool.filter(c => c.party === party).sort((a, b) => String(a.id).localeCompare(String(b.id)));
  return mine[hashStr('potd-card:' + day) % mine.length] }
function potdHTML() { const c = potdCard(); if (!c) return '';
  const st = lsJSON('potd'); const mine = st.date === nzToday().iso && st.id === c.id ? st.v : null;
  const label = { agree: 'You agreed', disagree: 'You disagreed', unsure: 'You weren’t sure' }[mine];
  return `<div class="feed__item" id="potd">
    <span class="feed__k">${ic('cards')} Policy of the day</span>
    <div class="potd">
      <p class="small muted">A real 2026 policy, party hidden. Everyone sees the same card today.</p>
      <p class="potd__s">${esc(c.statement)}</p>
      ${mine ? `<div class="reveal" style="--pc:${pcolor(c.party)}"><div class="reveal__who"><span class="sw"></span><span class="stack stack--s"><span class="micro muted">${esc(label)}. It’s from</span><span class="reveal__name">${esc(P(c.party).name || pname(c.party))}</span></span></div>
          ${c.why ? `<p class="small soft">${esc(c.why.length > 260 ? c.why.slice(0, 257).replace(/\s+\S*$/, '') + '…' : c.why)}</p>` : ''}
          <div class="row"><a class="more small" href="#/parties/${esc(c.party)}">About ${esc(pname(c.party))} ${ic('chev', 'i--xs')}</a>${c.doc ? `<span class="small"><button class="linkbtn" type="button" data-doc="${esc(c.party)}|${esc(c.doc)}">Read the full text</button></span>` : ''}<a class="more small" href="#/choose/swipe">Try more cards ${ic('chev', 'i--xs')}</a></div>
          <p class="micro muted">The party’s own policy, described neutrally. Your answer stays on this device.</p></div>`
      : `<div class="potd__actions" role="group" aria-label="Your view"><button class="btn btn--s" type="button" data-potd="disagree">${ic('x', 'i--xs')} Disagree</button><button class="btn btn--s btn--quiet" type="button" data-potd="unsure">Not sure</button><button class="btn btn--s btn--ink" type="button" data-potd="agree">${ic('check', 'i--xs')} Agree</button></div>`}
    </div></div>` }

function realPolls() { return (S.data.polls || []).filter(p => p && p.date && !/election result/i.test(p.pollster || '')) }
function sinceHTML() { const t = nzToday(); const out = [];
  const wk = new Date(Date.UTC(t.y, t.m - 1, t.d) - 7 * 864e5).toISOString().slice(0, 10);
  const nPolls = realPolls().filter(p => p.date >= wk && p.date <= t.iso).length;
  if (nPolls) out.push(`<a href="#/seats/polls"><b>${nPolls}</b><span>new poll${nPolls === 1 ? '' : 's'} in the last 7 days</span></a>`);
  if (S.news && S.news.items) { const y = new Date(Date.UTC(t.y, t.m - 1, t.d) - 864e5).toISOString().slice(0, 10);
    const nRel = S.news.items.filter(i => i.party !== 'government' && String(i.date).slice(0, 10) >= y).length;
    if (nRel) out.push(`<a href="#/parties/news"><b>${nRel}</b><span>party release${nRel === 1 ? '' : 's'} since yesterday</span></a>`) }
  if (!out.length) return '';
  return `<div class="feed__item"><span class="feed__k">${ic('spark')} New lately</span><div class="changes">${out.join('')}</div></div>` }

function pollWatchHTML() { const ps = realPolls(); if (!ps.length) return ''; const last = ps.map(p => p.date).sort().pop(); const latest = ps.filter(p => p.date === last);
  const who = latest.map(p => `${esc(p.pollster)}${p.sample_size ? ` (${Number(p.sample_size).toLocaleString('en-NZ')} people)` : ''}`);
  const list = who.length > 1 ? who.slice(0, -1).join(', ') + ' and ' + who[who.length - 1] : who[0];
  return `<div class="feed__item"><span class="feed__k">${ic('poll')} Poll watch</span>
    <p class="feed__t">${latest.length > 1 ? `${latest.length} polls` : 'The latest poll'} finished fieldwork on ${shortDate(last)}: ${list}.</p>
    <p class="src">${latest.map(p => p.source_url ? extA(p.source_url, esc(p.pollster)) : '').filter(Boolean).join(' · ')}</p>
    <a class="more small" href="#/seats/polls">What the polls would mean in seats ${ic('chev', 'i--xs')}</a></div>` }

function otdHTML() { const O = S.otd; if (!O || !O.days) return ''; const t = nzToday(); const list = (O.days[t.md] || []).filter(x => x && x.text && x.year && !x.upcoming);
  if (!list.length) return '';
  const person = slug => slug && (S.people || []).find(p => p.slug === slug);
  const item = x => { const pe = person(x.related && x.related.person); const pa = x.related && x.related.party && S.data.parties[x.related.party] ? x.related.party : null;
    return `<div class="otd"><span class="otd__year">${esc(x.year)}</span><div class="stack stack--s">${x.title ? `<b>${esc(x.title)}</b>` : ''}<p class="small soft">${esc(x.text)}</p>
      ${pe || pa ? `<p class="small">${pa ? `<a class="ptag ptag--s" style="--pc:${pcolor(pa)}" href="#/parties/${esc(pa)}"><span class="sw"></span>${esc(pname(pa))}</a>` : ''}${pe ? `${pa ? ' · ' : ''}<button class="linkbtn" type="button" data-person="${esc(pe.folder)}">${esc(pe.name)}</button>` : ''}</p>` : ''}
      ${x.source_url ? `<p class="src">${ic('doc')} ${extA(x.source_url, esc(x.source_name || 'Source'))}${x.approx_day ? ' · date approximate' : ''}</p>` : ''}</div></div>` };
  const more = O.nzhistory_day_url && O.nzhistory_day_url[t.md];
  return `<div class="feed__item"><span class="feed__k">${ic('history')} On this day</span>${list.map(item).join('')}
    ${more ? `<a class="more small" href="${esc(more)}" target="_blank" rel="noopener">More on this day at NZHistory ${extIc()}</a>` : ''}</div>` }

function fromPartiesHTML() { const N = S.news; if (!N || !N.items) return '';
  const all = (G().parties || []).map(p => p.slug).filter(s => N.parties[s] || (N.follow_parties || {})[s] || N.items.some(i => i.party === s));
  const slugs = all.sort((a, b) => pname(a).localeCompare(pname(b), 'en-NZ')); if (!slugs.length) return '';
  const k = slugs.length; const start = ((nzToday().n * 3) % k + k) % k; const pick = [0, 1, 2].slice(0, Math.min(3, k)).map(i => slugs[(start + i) % k]);
  const items = N.items.filter(i => i.party !== 'government').sort((a, b) => String(b.date).localeCompare(String(a.date)));
  const tag = s => `<span class="ptag ptag--s" style="--pc:${pcolor(s)}"><span class="sw"></span>${esc(pname(s))}</span>`;
  const row = s => { const it = items.find(i => i.party === s); const pm = N.parties[s] || (N.follow_parties || {})[s] || {};
    if (it) return `<a class="release" href="${esc(it.url)}" target="_blank" rel="noopener nofollow"><span class="release__t">${esc(it.title)}</span><span class="release__m">${tag(s)}<span>${shortDate(it.date)}</span><span>via ${esc(it.source || 'source')} ↗</span></span></a>`;
    return pm.newsroom_url ? `<a class="release" href="${esc(pm.newsroom_url)}" target="_blank" rel="noopener nofollow"><span class="release__t">No release in the feeds we read in the last ${N.window_days || 60} days. Their own newsroom ↗</span><span class="release__m">${tag(s)}</span></a>`
      : `<div class="release"><span class="release__t">No release in the feeds we read in the last ${N.window_days || 60} days.</span><span class="release__m">${tag(s)}</span></div>` };
  return `<div class="feed__item"><span class="feed__k">${ic('news')} From the parties</span>
    <p class="small soft">Today’s three parties in an A–Z rotation, so every party gets the same space. Their own words, not fact-checked.</p>
    <div>${pick.map(row).join('')}</div>
    <a class="more small" href="#/parties/news">All parties, three releases each ${ic('chev', 'i--xs')}</a></div>` }

function resumeHTML() { const out = [];
  const Q = G().quiz2; const q = lsJSON('quiz2', typeof q2State === 'function' ? q2State : null); const qn = Object.keys(q.answers || {}).length; const qt = ((Q && Q.statements) || []).length || 30;
  if (qn) out.push(`<a class="resume" href="#/choose/${qn >= qt ? 'results' : 'quiz'}"><span class="ring" style="--p:${Math.round(Math.min(1, qn / qt) * 100)}"><span>${qn}</span></span><span><b>Find your match</b><span class="small muted" style="display:block">${qn >= qt ? 'Finished · see your results' : `${qn} of ${qt} statements answered`}</span></span>${ic('chev')}</a>`);
  const sw = lsJSON('swipe', typeof swipeState === 'function' ? swipeState : null); const sn = Object.keys(sw.done || {}).length;
  if (sn) out.push(`<a class="resume" href="#/choose/swipe"><span class="ring" style="--p:${Math.round(Math.min(1, sn / 20) * 100)}"><span>${sn}</span></span><span><b>Policy swipe</b><span class="small muted" style="display:block">${sn} card${sn === 1 ? '' : 's'} decided${sn < 20 ? ` · 20 makes a good sample` : ''}</span></span>${ic('chev')}</a>`);
  const C = (G().compass || {}).items || []; const cs = lsJSON('compass', typeof compassState === 'function' ? compassState : null); const cn = Object.keys(cs.answers || {}).length;
  if (cn) out.push(`<a class="resume" href="#/choose/compass"><span class="ring" style="--p:${C.length ? Math.round(Math.min(1, cn / C.length) * 100) : 50}"><span>${cn}</span></span><span><b>Values compass</b><span class="small muted" style="display:block">${C.length ? `${cn} of ${C.length} questions answered` : `${cn} answered`}</span></span>${ic('chev')}</a>`);
  const me = store.get('myElectorate'); const e = me && (S.data.electorates || []).find(x => x.slug === me);
  if (e) out.push(`<a class="resume" href="#/vote/electorate/${esc(e.slug)}"><span class="rowlink__icon">${ic('pin')}</span><span><b>${esc(e.name)}</b><span class="small muted" style="display:block">Your electorate · ${(e.candidates || []).length} candidates</span></span>${ic('chev')}</a>`);
  const vc = lsJSON('votecheck'); const vn = Object.values(vc).filter(Boolean).length; const vt = Math.min(5, ((G().howtovote || {}).checklist || []).length) || 5;
  if (vn && electionPhase() !== 'results' && electionPhase() !== 'after') { const core = [0, 1, 2, 3, 4].filter(i => vc[i]).length;
    out.push(`<a class="resume" href="#/vote"><span class="ring" style="--p:${Math.round(core / vt * 100)}"><span>${core}</span></span><span><b>Ready to vote</b><span class="small muted" style="display:block">${core} of ${vt} ticks done</span></span>${ic('chev')}</a>`) }
  if (!out.length) return '';
  return `<section class="stack" aria-labelledby="h-mine"><div class="shead shead--quiet"><div class="shead__row"><h2 id="h-mine" class="h3">Pick up where you left off</h2><span class="micro muted">Saved on this device only</span></div></div>
    <div class="cols cols--3">${out.join('')}</div></section>` }

function feedHTML() { const eday = isElectionDay();
  const lockItem = `<div class="feed__item"><div class="locked">${ic('lock')}<div><b>Policy of the day, poll watch, party releases and “on this day” are hidden until 7pm.</b><p>${esc(ELECTION_DAY_BLOCK)}</p></div></div></div>`;
  const parts = eday ? [lockItem] : [potdHTML(), sinceHTML(), pollWatchHTML(), otdHTML(), fromPartiesHTML()];
  const body = parts.filter(Boolean).join('');
  return body ? `<div class="feed">${body}</div>` : '<p class="small muted">Nothing new today.</p>' }

V.home = async () => {
  const ph = electionPhase();
  // feed data loads in parallel; none of it is required for the page to work
  const loads = [];
  if (!S.swipe) loads.push(getJSON('data/swipe.json').then(d => { S.swipe = d }).catch(() => { S.swipe = [] }));
  if (S.news === undefined || S.news === null) loads.push(getJSON('data/newsroom.json').then(d => { S.news = d }).catch(() => { S.news = null }));
  if (S.otd === undefined || (S.otd && S.otd.days && !S.otd.days[nzToday().md])) loads.push(getJSON(`data/onthisday/${nzToday().md}.json`).then(d => { S.otd = d }).catch(() => { S.otd = null }));
  await Promise.all(loads);
  const upd = S.data.generated ? `Updated ${esc(shortDate(S.data.generated) || String(S.data.generated).slice(0, 10))}` : '';
  $('#main').innerHTML = `<div class="split split--7-5">
    <div class="stack stack--xl">
      <div class="stack stack--s">${heroHTML(ph)}<div class="micro notec">${NOT_EC}</div></div>
      <section class="stack" aria-labelledby="h-start">
        <div class="shead"><h2 id="h-start">What do you want to do?</h2></div>
        <div class="rows" style="border-top:0">
          ${rowlink('#/vote', 'vote', 'Can I vote, and how?', 'Five quick checks. No ID needed.')}
          ${rowlink('#/vote/electorate', 'pin', 'Who is standing where I live?', 'Your electorate, candidates and how close it was.')}
          ${rowlink('#/choose', 'choose', 'Which parties agree with me?', 'Swipe, quiz or compass. Party names hidden.')}
          ${rowlink('#/seats/polls', 'seats', 'What might happen?', 'Polls, seat ranges and every map since 2011.')}
        </div>
      </section>
      <section class="stack" aria-labelledby="h-two">
        <div class="shead shead--quiet"><div class="shead__row"><h2 id="h-two" class="h3">You have two votes</h2><a class="more small" href="#/vote/mmp">MMP in 60 seconds ${ic('chev', 'i--xs')}</a></div></div>
        ${twoVotesHTML()}
      </section>
    </div>
    <aside class="stack stack--l" aria-labelledby="h-today">
      <div class="shead__row"><h2 id="h-today">Today</h2><span class="small muted">${upd}</span></div>
      ${feedHTML()}
    </aside>
  </div>
  ${resumeHTML()}`;
  const pt = $('#potd'); if (pt) pt.addEventListener('click', e => { const b = e.target.closest('[data-potd]'); if (!b) return; const c = potdCard(); if (!c) return;
    store.set('potd', JSON.stringify({ date: nzToday().iso, id: c.id, v: b.dataset.potd }));
    pt.outerHTML = potdHTML(); const n = $('#potd'); if (n) { const f = n.querySelector('.reveal a, .reveal button'); if (f) f.focus({ preventScroll: true }) } });
};

/* ----- the animated ballot illustration (shown in Vote › How MMP works) -----
   Rules: every registered party, alphabetical; ticks glide at random and never point at a choice; only the lists scroll,
   never the page; illustration only. */
function ballotParties() { const gp = (G().parties || []).map(p => ({ slug: p.slug, name: p.name || pname(p.slug) }));
  const list = gp.length ? gp : Object.keys(S.data.parties || {}).map(s => ({ slug: s, name: P(s).name || pname(s) }));
  return list.sort((a, b) => a.name.localeCompare(b.name, 'en-NZ')) }
function ballotHTML() { const bp = ballotParties();
  return `<figure class="ballot-fig stack stack--s">
    <div class="ballot" role="img" aria-label="Example ballot paper (illustration only; the ticks move at random and do not indicate a choice)">
      <div class="ballot__col"><span class="ballot__h">Party vote</span><div class="ballot__list" id="bl-p">${bp.map(p => `<span class="ballot__opt"><span class="ballot__name"><span class="sw" style="--pc:${pcolor(p.slug)}"></span>${esc(p.name)}</span><span class="ballot__box"></span></span>`).join('')}<span class="ballot__tick" id="bt-p">${TICK_SVG(true)}</span></div></div>
      <div class="ballot__col"><span class="ballot__h">Electorate vote</span><div class="ballot__list" id="bl-e">${['Candidate A', 'Candidate B', 'Candidate C', 'Candidate D', 'Candidate E', 'Candidate F'].map(c => `<span class="ballot__opt"><span class="ballot__name">${c}</span><span class="ballot__box"></span></span>`).join('')}<span class="ballot__tick" id="bt-e">${TICK_SVG(true)}</span></div></div>
    </div>
    <figcaption class="small muted">Illustration only: the ticks move at random and don’t show a choice. All ${bp.length} registered parties appear on the real paper, in alphabetical order, and candidates are listed alphabetically by surname. You can split your two votes between different parties. What the real paper looks like: ${extA('https://vote.nz/2026-general-election/voting-in-the-election/what-to-do', 'vote.nz')}.</figcaption>
  </figure>` }
function startBallot() { if (S.ballotTimer) clearInterval(S.ballotTimer); if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const cols = [['#bl-p', '#bt-p'], ['#bl-e', '#bt-e']].map(([l, t]) => ({ list: $(l), tick: $(t), i: 0 })).filter(c => c.list && c.tick);
  if (!cols.length) return; cols[1] && (cols[1].i = 2);
  const place = c => { const rows = c.list.querySelectorAll('.ballot__opt'); if (!rows.length) return; const r = rows[c.i % rows.length];
    c.tick.style.top = (r.offsetTop + (r.offsetHeight - 22) / 2) + 'px'; c.tick.classList.add('on');
    // scroll only the list, never the page
    const top = r.offsetTop - c.list.clientHeight / 2 + r.offsetHeight / 2; c.list.scrollTo({ top: Math.max(0, top), behavior: 'smooth' }) };
  cols.forEach(place);
  S.ballotTimer = setInterval(() => { if (!document.body.contains(cols[0].list)) { clearInterval(S.ballotTimer); S.ballotTimer = null; return }
    cols.forEach(c => { const n = c.list.querySelectorAll('.ballot__opt').length; if (n < 2) return; let j; do { j = Math.floor(Math.random() * n) } while (j === c.i); c.i = j; place(c) }) }, 1700) }
