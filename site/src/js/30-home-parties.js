V.home = async () => {
  const d = daysLeft(); const parl = currentParl();
  const gps = (G().parties || []); const proj = projection();
  $('#main').innerHTML = `<section class="view">
    <div class="hero"><div class="stack" style="gap:16px">
      <span class="count">${d > 0 ? `<b>${d}</b> days until election day, Saturday 7 November` : d === 0 ? '<b>Today</b> is election day' : 'The 2026 election was held on 7 November'}</span>
      <h1>Your two votes. <em>Your call.</em></h1>
      <p class="lede">A friendly, independent guide to New Zealand's 2026 election. Start simple with plain-English summaries, then dig into every policy, every candidate and how each party has kept its promises.</p>
      <div class="cta"><button class="btn sun" data-go="match">Find your match</button><button class="btn" data-go="parties">Meet the parties</button></div>${NOT_EC}</div>
      <div class="card chamber" style="padding:16px 16px 8px">${parl ? chamberSVG(parliamentSeats(parl, 'now'), { label: 'Parliament today', animate: true }) : ''}
        <p class="tiny muted" style="text-align:center;margin-top:4px">Parliament as it stands today. <button class="btn ghost sm" data-go="parliament">Explore every Parliament since 2011</button></p></div></div>

    <div class="card" style="display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:center;border-left:6px solid var(--sun)"><span class="ic" style="width:48px;height:48px;border-radius:14px;display:grid;place-items:center;background:color-mix(in srgb, var(--sun) 30%, transparent)">${ic('vote')}</span><div><h3>First time voting, or haven't voted in a while?</h3><p class="small muted" style="margin:0">A plain, step-by-step guide: check you're enrolled, find a voting place, know what to bring and what the two ticks mean.</p></div><button class="btn sun" data-go="vote">How to vote</button></div>
    <div class="starters">
      <button class="starter" data-go="match"><span class="ic sun">${ic('match')}</span><h3>Find your match</h3><p class="muted small">Thirty statements about how New Zealand should work, no party named. See how closely each party's published positions match yours, with the evidence.</p><span class="go">Start the quiz →</span></button>
      <button class="starter" data-go="swipe"><span class="ic">${ic('swipe')}</span><h3>Policy swipe</h3><p class="muted small">Agree or disagree with real 2026 policies, one at a time, with no party names. Find out whose it was after you decide.</p><span class="go">Start swiping →</span></button>
      <button class="starter" data-go="compass"><span class="ic">${ic('compass')}</span><h3>Political compass</h3><p class="muted small">General value questions from academic surveys; see where you sit, and where the parties sit, on standard axes.</p><span class="go">Take the test →</span></button>
      <button class="starter" data-go="game"><span class="ic">${ic('game')}</span><h3>Whose policy? (game)</h3><p class="muted small">Pass the phone. Each player guesses which party a real policy belongs to. Two to six players.</p><span class="go">Play →</span></button>
      <button class="starter" data-go="map"><span class="ic">${ic('map')}</span><h3>Electorate map</h3><p class="muted small">Every seat since 2011, coloured by who won. Scrub through the years and tap a seat.</p><span class="go">Open the map →</span></button>
      <button class="starter" data-go="issues"><span class="ic">${ic('issues')}</span><h3>Compare on the issues</h3><p class="muted small">Cost of living, housing, health and more, with every party's position side by side.</p><span class="go">See the issues →</span></button>
      <button class="starter" data-go="electorate"><span class="ic">${ic('parties')}</span><h3>Meet your local candidates</h3><p class="muted small">Pick your electorate to see who's standing, with photos, in their own words.</p><span class="go">Find your electorate →</span></button></div>

    ${locateBlock('loc-home')}
    <div class="stack" style="gap:16px"><div class="row" style="justify-content:space-between"><div><div class="kicker">On the ballot</div><h2>The parties</h2></div><button class="btn sm" data-go="parties">All ${Object.keys(S.data.parties).filter(s => (guideParty(s) || P(s).policy_count)).length || ''} parties</button></div>
      <div class="grid">${partyOrder().slice(0, 6).map(partyCard).join('')}</div></div>

    <div class="card stack" style="gap:18px"><div><div class="kicker">MMP in one minute</div><h2>How your two votes work</h2></div>
      <div class="split"><div class="steps">
        <div><h4>Party vote</h4><p class="small muted">This decides how many seats each party gets. A party with 30% of the party vote gets about 30% of the 120 seats.</p></div>
        <div><h4>Electorate vote</h4><p class="small muted">This picks your local MP. Whoever gets the most votes in your area wins the seat.</p></div>
        <div><h4>The 5% rule</h4><p class="small muted">A party needs 5% of the party vote, or to win an electorate, to get its share of seats.</p></div>
        <div><h4>61 to govern</h4><p class="small muted">A government needs a majority of seats, usually 61 of 120. That's why parties form coalitions.</p></div></div>
        <div class="stack"><div class="ballot" aria-label="Example ballot paper (illustration; ticks move and do not indicate a choice)"><div><span class="bh">Party vote</span><div class="list" id="bl-p">${ballotParties().map(p => `<span class="opt"><span class="row" style="gap:6px;flex-wrap:nowrap"><span class="dot" style="background:${pcolor(p.slug)}"></span>${esc(p.name)}</span><span class="box"></span></span>`).join('')}<span class="tick" id="bt-p"></span></div></div>
          <div><span class="bh">Electorate vote</span><div class="list" id="bl-e">${['Candidate A', 'Candidate B', 'Candidate C', 'Candidate D', 'Candidate E'].map(c => `<span class="opt">${c}<span class="box"></span></span>`).join('')}<span class="tick" id="bt-e"></span></div></div></div>
          <p class="tiny muted">Illustration only: the ticks move and don't show a choice. All ${ballotParties().length} registered parties appear on the real paper, in alphabetical order. You can split your two votes between different parties. <button class="btn ghost sm" data-go="calculator">Try the seat calculator</button></p></div></div></div>

    <div class="stack"><div><div class="kicker">Key dates</div><h2>When to vote</h2></div>
      <div class="dates">${KEY_DATES.map(([dt, t, s]) => { const D = new Date(dt + 'T23:59:00+13:00'); const [, mo, dd] = dt.split('-'); return `<div class="date card flat ${D < Date.now() ? 'past' : ''}"><div class="cal"><span>${['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'][+mo - 1]}</span><b>${+dd}</b></div><div><h4>${t}</h4><p class="small muted">${s}</p></div></div>` }).join('')}</div>
      <p class="note">Check you're enrolled and find your voting place at <b>vote.nz</b> or call 0800 36 76 56. Enrolment closes on Sunday 25 October. You need to be 18+, a citizen or permanent resident, and have lived in New Zealand for a year at some point.</p></div>

    ${proj.n && !isElectionDay() ? `<div class="card stack"><div class="row" style="justify-content:space-between"><div><div class="kicker">The polls</div><h2>Where things stand</h2></div><button class="btn sm" data-go="polls">Polls & forecast</button></div>
      <p class="small muted">Average of the ${proj.n} latest polls (${esc(proj.range)}). Polls have margins of error of about ±3 points.</p>
      ${Object.entries(proj.pct).sort((a, b) => b[1] - a[1]).filter(([, v]) => v >= 0.8).map(([p, v]) => `<div class="row" style="flex-wrap:nowrap"><span style="width:120px;flex:none" class="small"><b>${esc(pname(p))}</b></span><div class="meter" style="flex:1"><span style="width:${v / 50 * 100}%;background:${pcolor(p)}"></span></div><span class="num small" style="width:48px;text-align:right">${fmt(v)}%</span></div>`).join('')}</div>` : ''}
  </section>`;
  requestAnimationFrame(startBallot);
};

function ballotParties() { const gp = (G().parties || []).map(p => ({ slug: p.slug, name: p.name || pname(p.slug) })); const list = gp.length ? gp : MAIN7.map(p => ({ slug: p, name: P(p).name }));
  return list.sort((a, b) => a.name.localeCompare(b.name, 'en-NZ')) }
function startBallot() { if (S.ballotTimer) clearInterval(S.ballotTimer); if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const cols = [['#bl-p', '#bt-p'], ['#bl-e', '#bt-e']].map(([l, t]) => ({ list: $(l), tick: $(t), i: 0 })).filter(c => c.list && c.tick);
  if (!cols.length) return; cols[1] && (cols[1].i = 2);
  const place = c => { const rows = c.list.querySelectorAll('.opt'); if (!rows.length) return; const r = rows[c.i % rows.length];
    c.tick.style.top = (r.offsetTop + (r.offsetHeight - 20) / 2) + 'px'; c.tick.classList.add('on');
    // scroll only the list, never the page
    const top = r.offsetTop - c.list.clientHeight / 2 + r.offsetHeight / 2; c.list.scrollTo({ top: Math.max(0, top), behavior: 'smooth' }) };
  cols.forEach(place);
  S.ballotTimer = setInterval(() => { cols.forEach(c => { const n = c.list.querySelectorAll('.opt').length; if (n < 2) return; let j; do { j = Math.floor(Math.random() * n) } while (j === c.i); c.i = j; place(c) }) }, 1700) }
function partyOrder() {
  const gp = (G().parties || []).map(p => p.slug);
  const known = Object.keys(S.data.parties).filter(s => gp.includes(s) || P(s).policy_count > 0);
  const poll = isElectionDay() ? {} : projection().pct;
  return [...new Set([...gp, ...known])].filter(s => S.data.parties[s] || guideParty(s)).sort((a, b) => (poll[b] || 0) - (poll[a] || 0) || (P(a).policy_count ? 0 : 1) - (P(b).policy_count ? 0 : 1) || pname(a).localeCompare(pname(b)));
}
function leaderFaces(s) { const g = guideParty(s); const ls = (g && g.leaders) || []; return ls.map(l => findPerson(l.slug, l.name)).filter(Boolean) }
function partyCard(s) {
  const g = guideParty(s) || {}; const pp = P(s); const poll = projection().pct[s]; const faces = leaderFaces(s);
  const seats = (currentParl() && (currentParl().composition_now_or_end || {})[s]) || 0;
  return `<button class="pcard" style="--pc:${pcolor(s)}" data-go="party-${s}">
    <div class="who">${faces.length ? `<span class="faces">${faces.slice(0, 2).map(f => faceHTML(f, s)).join('')}</span>` : `<span class="mono">${esc(initials(s))}</span>`}
      <div style="min-width:0"><h3>${esc(g.name || pp.name)}</h3><div class="tiny muted">${esc((g.leaders || []).map(l => l.name).join(' & ') || '')}</div></div></div>
    <p class="small">${esc(g.tagline || pp.intro || '').slice(0, 220)}</p>
    <div class="row">${seats ? `<span class="badge in">${seats} MPs</span>` : '<span class="badge">Not in Parliament</span>'}${poll && !isElectionDay() ? `<span class="badge">Polling ${fmt(poll)}%</span>` : ''}${pp.policy_count ? `<span class="badge">${pp.policy_count} policies</span>` : ''}</div></button>`;
}

V.parties = async () => {
  await loadPeople();
  const order = partyOrder();
  $('#main').innerHTML = `<section class="view"><div class="stack"><div class="kicker">Election 2026</div><h2>Meet the parties</h2>
    <p class="lede">Every party on the 2026 party-vote ballot. Tap a party for a plain summary, then go as deep as you like: every policy, their people and their record.</p></div>
    <div class="grid">${order.map(partyCard).join('')}</div>
    <p class="small muted">${isElectionDay() ? 'Sorted alphabetically today.' : 'Sorted by current polling.'} Former parties from 2011 to 2023 are in <button class="btn ghost sm" data-page="parties/MINOR_PARTIES.md">the minor parties overview</button>.</p></section>`;
};

V.party = async (s, tab = 'glance') => {
  await loadPeople(); if (!S.policies) S.policies = await getJSON('data/policies.json').catch(() => ({}));
  const g = guideParty(s) || {}; const pp = P(s); const poll = projection().pct[s];
  const seats = (currentParl() && (currentParl().composition_now_or_end || {})[s]) || 0;
  const faces = leaderFaces(s); const pols = S.policies[s] || []; const prom = (S.data.promises || {})[s] || [];
  const people = S.people.filter(p => p.party === s);
  const tabs = [['glance', 'At a glance'], ['policies', `Policies (${pols.length})`], ['record', 'Track record'], ['people', `People (${people.length})`], ['history', 'History']];
  $('#main').innerHTML = `<section class="view">
    <button class="btn ghost sm" data-go="parties" style="justify-self:start">← All parties</button>
    <div class="party-hero" style="--pc:${pcolor(s)}"><div class="row" style="gap:16px;flex-wrap:nowrap">${faces.length ? `<span class="faces">${faces.slice(0, 2).map(f => faceHTML(f, s, 'face" style="width:72px;height:72px;--pc:' + pcolor(s))).join('')}</span>` : `<span class="mono" style="width:72px;height:72px;font-size:24px">${esc(initials(s))}</span>`}
      <div style="min-width:0"><div class="kicker" style="color:var(--text)">${esc(T(g.position))}</div><h1 style="font-size:clamp(30px,5vw,46px)">${esc(g.name || pp.name)}</h1><div class="muted">${esc((g.leaders || []).map(l => l.name).join(' & '))}${g.founded ? ' · founded ' + esc(g.founded) : ''}</div></div></div>
      ${g.tagline ? `<p class="lede" style="color:var(--text)">${esc(g.tagline)}</p>` : ''}
      <div class="stats"><div class="stat"><b>${seats}</b><span>MPs now</span></div>${poll && !isElectionDay() ? `<div class="stat"><b>${fmt(poll)}%</b><span>poll average</span></div>` : ''}<div class="stat"><b>${pols.length}</b><span>2026 policies</span></div>${prom.length ? `<div class="stat"><b>${prom.length}</b><span>promises checked</span></div>` : ''}</div></div>
    <div class="tabs" role="tablist" id="ptabs">${tabs.map(([k, l]) => `<button role="tab" data-t="${k}" aria-selected="${k === tab}">${l}</button>`).join('')}</div>
    <div id="pbody"></div></section>`;
  const body = $('#pbody');
  const show = t => { $('#ptabs').querySelectorAll('button').forEach(b => b.setAttribute('aria-selected', b.dataset.t === t));
    if (t === 'glance') body.innerHTML = `<div class="split" style="--pc:${pcolor(s)}"><div class="stack" style="gap:18px">
        ${g.in_a_nutshell ? `<div class="card stack"><h3>In a nutshell</h3><p class="read">${esc(g.in_a_nutshell)}</p></div>` : pp.intro ? `<div class="card stack"><h3>About</h3><p class="read">${esc(pp.intro)}</p></div>` : ''}
        ${!(g.big_ideas || []).length && pols.some(isKey) ? `<div class="card stack"><h3>Headline policies</h3><ul class="ideas">${pols.filter(isKey).slice(0, 7).map(x => `<li><span>${esc(x.statement)}</span></li>`).join('')}</ul><button class="btn sm" data-t2="policies" style="justify-self:start">See all ${pols.length} policies</button></div>` : ''}
        ${(g.big_ideas || []).length ? `<div class="card stack"><h3>Big ideas for 2026</h3><ul class="ideas">${g.big_ideas.map(b => `<li><span>${esc(b.text || b)}</span></li>`).join('')}</ul><button class="btn sm" data-t2="policies" style="justify-self:start">See all ${pols.length} policies</button></div>` : ''}
        ${T(g.they_say) || T(g.critics_say) ? `<div class="card stack"><h3>Two sides</h3>${T(g.they_say) ? `<div class="quote"><div class="tiny muted">What they say</div>${esc(T(g.they_say))}${srcLinks(g.they_say)}</div>` : ''}${T(g.critics_say) ? `<div class="quote" style="--pc:var(--line)"><div class="tiny muted">What critics say${g.critics_say.who ? ' · ' + esc(g.critics_say.who) : ''}</div>${esc(T(g.critics_say))}${srcLinks(g.critics_say)}</div>` : ''}</div>` : ''}</div>
      <div class="stack" style="gap:18px">
        ${T(g.coalition_stance_2026) ? `<div class="card stack"><h3>Who they'd work with</h3><p class="small">${esc(T(g.coalition_stance_2026))}${srcLinks(g.coalition_stance_2026)}</p></div>` : ''}
        ${recordSummary(s)}
        ${T(g.costings) ? `<div class="card stack"><h3>Are the numbers costed?</h3><p class="small">${esc(T(g.costings))}${srcLinks(g.costings)}</p></div>` : ''}
        ${partyResultsMini(s)}
        <div class="card stack"><h3>Go deeper</h3><div class="row">${pp.has_readme ? `<button class="btn sm" data-page="parties/${s}/README.md">Full party profile</button>` : ''}${pp.has_track_record ? `<button class="btn sm" data-page="parties/${s}/track-record.md">Full track record</button>` : ''}<button class="btn sm" data-page="parties/${s}/policies/README.md">Policy index</button><button class="btn sm" data-go="newsroom-${s}">Newsroom &amp; follow</button>${g.website ? `<a class="btn sm" href="${esc(g.website)}" target="_blank" rel="noopener">Party website</a>` : ''}</div></div>
        ${(g.sources || []).length ? `<details class="tiny muted"><summary>Sources for this summary</summary><ul>${g.sources.map(u => `<li><a href="${esc(typeof u === 'string' ? u : u.url)}" target="_blank" rel="noopener">${esc(typeof u === 'string' ? u : (u.title || u.url))}</a></li>`).join('')}</ul></details>` : ''}</div></div>`;
    if (t === 'policies') policyBrowser(body, [s]);
    if (t === 'record') promiseList(body, s);
    if (t === 'people') peopleGrid(body, { party: s });
    if (t === 'history') { body.innerHTML = `<div class="stack" style="gap:18px">${partyResultsMini(s, true)}<div class="card prose" id="phist"><p class="empty">Loading…</p></div></div>`; loadPages().then(() => { const k = `parties/${s}/README.md`; $('#phist').innerHTML = S.pages[k] ? md(S.pages[k]) : '<p class="empty">Profile not written yet.</p>'; $('#phist').dataset.base = k }) }
    body.querySelectorAll('[data-t2]').forEach(b => b.onclick = () => show(b.dataset.t2)); };
  $('#ptabs').onclick = e => { const b = e.target.closest('[data-t]'); if (b) show(b.dataset.t) };
  show(tab);
};
function recordSummary(s) {
  const all = (S.data.promises || {})[s] || []; if (!all.length) return '';
  const g = guideParty(s) || {}; const cur = S.promPeriod || 'all';
  const terms = TERMS.map(([k, l]) => [k, l, all.filter(x => periodOf(x) === k)]).filter(([, , L]) => L.length);
  const sc = scoreOf(all);
  return `<div class="card stack"><h3>Keeping their word</h3>${T(g.track_record_line) ? `<p class="small">${esc(T(g.track_record_line))}</p>` : ''}
    <div class="row" style="justify-content:space-between"><span class="small"><b>All time:</b> ${sc.n} promises checked${sc.score != null ? `, <b>${sc.score}%</b> kept` : ''}</span></div>${verdictMeter(all)}
    <div class="row tiny">${VERDICTS.filter(v => all.some(x => x.status === v)).map(v => `<span class="row" style="gap:4px"><span class="verdict v-${v}">${all.filter(x => x.status === v).length}</span>${v.replace(/-/g, ' ')}</span>`).join('')}</div>
    <h4 style="margin-top:6px">By term</h4><div class="stack" style="gap:8px">${terms.map(([k, l, L]) => { const t = scoreOf(L); return `<div><div class="row tiny" style="justify-content:space-between"><span><b>${l}</b> · ${t.n} checked</span><span>${t.score != null ? `<b>${t.score}%</b> kept` : 'not yet due'}</span></div>${verdictMeter(L, 9)}</div>` }).join('')}</div>
    <details class="small"><summary style="cursor:pointer;color:var(--accent);font-weight:700">How promises were judged</summary><ul style="margin:6px 0 0 18px"><li><b>Kept</b>: delivered as promised, in substance and timing.</li><li><b>Partly kept</b>: delivered in part, late, or in a narrower form.</li><li><b>Broken</b>: not delivered while the party had the power to deliver it.</li><li><b>Abandoned</b>: dropped by the party itself (often in coalition talks); the entry says who dropped it and why.</li><li><b>In progress</b> / <b>not yet due</b>: still being implemented, or promised for after the election.</li></ul><p style="margin-top:6px">Each promise lists what was said (with a link to where it was said), what happened (with sources), and the verdict. The same definitions are applied to every party; parties in opposition have fewer promises that can be judged, which is noted.</p></details>
    <div class="row"><button class="btn sm" data-t2="record">See every promise, with sources</button>${P(s).has_track_record ? `<button class="btn sm ghost" data-page="parties/${s}/track-record.md">Full track record</button>` : ''}</div></div>`;
}
function partyResultsMini(s, big = false) {
  const els = S.data.elections.filter(e => e.year >= 2008); const rows = els.map(e => { const r = (e.parties || []).find(x => x.party === s); return [e.year, r] });
  if (!rows.some(([, r]) => r)) return '';
  const max = Math.max(10, ...rows.map(([, r]) => r ? r.party_vote_pct : 0));
  return `<div class="card stack"><h3>Election results</h3><div class="stack" style="gap:6px">${rows.map(([y, r]) => `<div class="row" style="flex-wrap:nowrap"><span class="num small" style="width:44px">${y}</span><div class="meter" style="flex:1;height:12px"><span style="width:${r ? r.party_vote_pct / max * 100 : 0}%;background:${pcolor(s)}"></span></div><span class="num small" style="width:${big ? 150 : 132}px;text-align:right;white-space:nowrap">${r ? fmt(r.party_vote_pct) + '% · ' + (r.total_seats || 0) + ' seats' : 'did not stand'}</span></div>`).join('')}</div></div>`;
}
