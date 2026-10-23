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
