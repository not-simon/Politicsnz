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
