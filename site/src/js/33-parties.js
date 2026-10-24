/* ===== Parties: list (A–Z or ballot order) and the party page (Overview · Policies · Record · People · History) ===== */
// Every party in the guide: the 2026 party-vote list plus any other group whose policies are on file.
// mode 'az' = A–Z by short name (default everywhere); 'ballot' = alphabetical by registered name, as on the ballot paper.
// Never sorted by polling (only Seats › Polls does that, and says so).
function partyOrder(mode = 'az') {
  const gp = (G().parties || []).map(p => p.slug);
  const known = Object.keys(S.data.parties).filter(s => gp.includes(s) || P(s).policy_count > 0);
  const key = mode === 'ballot' ? s => (guideParty(s) || {}).name || P(s).name || pname(s) : s => pname(s);
  return [...new Set([...gp, ...known])].filter(s => S.data.parties[s] || guideParty(s)).sort((a, b) => ptCmp(key(a), key(b)) || ptCmp(a, b));
}
const onBallot = s => (G().parties || []).some(p => p.slug === s);
function leaderFaces(s) { const g = guideParty(s); const ls = (g && g.leaders) || []; return ls.map(l => findPerson(l.slug, l.name)).filter(Boolean) }
function partySeats(s) { const g = guideParty(s); if (g && g.current_seats && g.current_seats.seats != null) return g.current_seats.seats; return (currentParl() && (currentParl().composition_now_or_end || {})[s]) || 0 }
// Glance row used on the parties list (and by any other view that wants a party row). No polling.
function partyCard(s) {
  const g = guideParty(s) || {}; const pp = P(s); const seats = partySeats(s);
  const meta = [seats ? `${seats} MP${seats === 1 ? '' : 's'}` : 'No MPs', pp.policy_count ? `${pp.policy_count} ${pp.policy_count === 1 ? 'policy' : 'policies'}` : ''].filter(Boolean).join(' · ');
  return `<a class="rowlink rowlink--plain party-row" href="#/parties/${esc(s)}" style="--pc:${pcolor(s)}"><span class="stack stack--s"><span class="rowlink__title"><span class="ptag"><span class="sw"></span>${esc(g.name && S.partySort === 'ballot' ? g.name : pname(s))}</span></span>
    ${g.tagline || pp.intro ? `<span class="rowlink__sub">${esc(g.tagline || String(pp.intro).replace(/\[([^\]]+)\]\([^)]*\)/g, '$1').replace(/[*_`]/g, '').slice(0, 180))}</span>` : ''}<span class="micro muted">${meta}</span></span>${ic('chev')}</a>`;
}

V.parties = async () => {
  await loadPeople();
  S.partySort = store.get('partySort') === 'ballot' ? 'ballot' : 'az';
  const draw = () => {
    const order = partyOrder(S.partySort); const ballot = order.filter(onBallot), others = order.filter(s => !onBallot(s));
    $('#main').innerHTML = sectionFrame('parties', 'parties', `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('parties', 'i--s')} Parties · All parties</p><h1>The parties</h1>
      <p class="lede">Every party on the 2026 party-vote ballot. Pick one for a plain summary, then go as deep as you like: every policy in the party's own words, their people and their record.</p></header>
      <section class="stack"><div class="row row--between"><div class="seg" role="group" aria-label="Order">${[['az', 'A to Z'], ['ballot', 'Ballot order']].map(([k, l]) => `<button type="button" data-sort="${k}" aria-pressed="${S.partySort === k}">${l}</button>`).join('')}</div>
        <span class="micro muted">${S.partySort === 'ballot' ? 'Alphabetical by registered name, the order the parties appear on the ballot paper.' : 'Alphabetical by short name.'} ${ballot.length} parties.</span></div>
        <div class="rows">${ballot.map(partyCard).join('')}</div></section>
      ${others.length ? `<section class="stack"><div class="shead shead--quiet"><h2 class="h3">Also in this guide</h2></div><p class="small soft">Groups that are not on the 2026 party-vote list but whose candidates or policies are on file.</p><div class="rows">${others.map(partyCard).join('')}</div></section>` : ''}
      <p class="small muted">Former parties from 2011 to 2023 are in <a href="#/about/page/parties/MINOR_PARTIES.md">the minor parties overview</a>.</p>`);
    $('#main').querySelectorAll('[data-sort]').forEach(b => b.onclick = () => { S.partySort = b.dataset.sort; store.set('partySort', S.partySort); draw() });
  };
  draw();
};

const PARTY_TABS = [['glance', 'Overview', ''], ['policies', 'Policies', '/policies'], ['record', 'Record', '/record'], ['people', 'People', '/people'], ['history', 'History', '/history']];
// Overview sections that open in the sheet; each also has its own URL (#/parties/<slug>/two-sides …), which opens the Overview with that sheet on top.
const PARTY_SHEETS = ['big-ideas', 'two-sides', 'work-with', 'costed', 'results', 'sources'];
V.party = async (s, tab = 'glance') => {
  await loadPeople(); if (!S.policies) S.policies = await getJSON('data/policies.json').catch(() => ({}));
  const sheet = PARTY_SHEETS.includes(tab) ? tab : null;
  if (!PARTY_TABS.some(([k]) => k === tab)) tab = 'glance';
  const g = guideParty(s) || {}; const pp = P(s); const pc = pcolor(s);
  if (!S.data.parties[s] && !guideParty(s)) { $('#main').innerHTML = sectionFrame('parties', 'parties', `<div class="stack"><h1>Party not found</h1><p>There is no party called “${esc(s)}” in this guide.</p><a class="more" href="#/parties">All parties ${ic('chev', 'i--xs')}</a></div>`); return }
  const faces = leaderFaces(s); const pols = S.policies[s] || []; const prom = (S.data.promises || {})[s] || [];
  const people = S.people.filter(p => p.party === s);
  const counts = { policies: pols.length, record: prom.length, people: people.length };
  const pos = g.position || {}; const label = T(pos);
  const leaders = (g.leaders || []).map(l => { const r = String(l.role || '').replace(/^Leader(,\s*)?/i, '').trim(); return esc(l.name) + (r ? ', ' + esc(r) : '') });
  const nBallot = (G().parties || []).length;
  const head = `<div class="stack stack--l party-page"><nav class="small" aria-label="Breadcrumb"><a href="#/parties">All ${nBallot} parties</a> <span class="muted">/ ${esc(pname(s))}</span></nav>
    <header class="phead" style="--pc:${pc}">
      <div class="phead__id"><span class="phead__faces">${faces.length ? faces.slice(0, 2).map(f => faceHTML(f, s, 'face face--l')).join('') : `<span class="face--none face face--l" style="--pc:${pc}" aria-hidden="true">${esc(initials(s))}</span>`}</span>
        <div class="stack stack--s"><p class="eyebrow">${label ? (/^no /i.test(label) ? 'No position label' : esc(label)) + ` <span class="phead__src">(${pos.source ? ptExt(pos.source, "Wikipedia's label") : "Wikipedia's label"})</span>` : ''}${g.founded ? ` · Founded ${esc(g.founded)}` : ''}</p>
          <h1>${esc(g.name || pp.name)}</h1>${leaders.length ? `<p class="small soft">${(g.leaders || []).length > 1 && g.leaders.every(l => /^co-?leader/i.test(l.role || '')) ? 'Led by co-leaders ' + g.leaders.map(l => esc(l.name) + (String(l.role).replace(/^co-?leader,?\s*/i, '') ? ` (${esc(String(l.role).replace(/^co-?leader,?\s*/i, ''))})` : '')).join(' and ') : 'Led by ' + leaders.join(' and ')}</p>` : ''}</div></div>
      ${g.tagline ? `<p class="phead__tag">${esc(g.tagline)}</p>` : ''}${pos.description ? `<p class="small soft">${esc(pos.description)}</p>` : ''}
      <div class="row"><a class="btn btn--s" href="#/choose/compare/${esc(s)}">${ic('swap', 'i--xs')} Compare with another party</a>${g.website ? `<a class="btn btn--s btn--quiet" href="${esc(g.website)}" target="_blank" rel="noopener">Party website ${ic('ext', 'i--xs')}</a>` : ''}</div>
    </header>
    <nav class="ptabs" aria-label="${esc(g.name || pp.name)}">${PARTY_TABS.map(([k, l, sub]) => `<a href="#/parties/${esc(s)}${sub}"${k === tab ? ' aria-current="page"' : ''}>${l}${counts[k] != null ? ` <span class="num">${counts[k]}</span>` : ''}</a>`).join('')}</nav>
    <div id="pbody" class="party-body"></div></div>`;
  $('#main').innerHTML = sectionFrame('parties', 'parties', head);
  const body = $('#pbody');
  if (tab === 'glance') { body.innerHTML = partyOverview(s, pols, prom); bindIdeas(body, s);
    body.querySelectorAll('[data-ov]').forEach(b => b.onclick = () => openPartySheet(s, b.dataset.ov));
    if (sheet) openPartySheet(s, sheet) }
  if (tab === 'policies') policyBrowser(body, [s]);
  if (tab === 'record') promiseList(body, s);
  if (tab === 'people') peopleGrid(body, { party: s });
  if (tab === 'history') { const k = `parties/${s}/README.md`; await loadPage(k);
    body.innerHTML = `<div class="party-layout party-layout--history"><div class="party-layout__main stack"><div class="shead"><h2>History and profile</h2></div>
      ${S.pages[k] ? `<div class="prose" data-base="${esc(k)}">${md(S.pages[k].replace(/^#\s+.+\n/, ''))}</div><p class="src">Plain-text source: ${ptExt('https://github.com/not-simon/Politicsnz/blob/main/' + k, esc(k))}</p>` : '<p class="muted">The full profile for this party has not been written yet.</p>'}</div>
      <aside class="stack stack--l party-layout__side">${partyResultsMini(s, true)}</aside></div>` }
};

// Overview, first screen: glance box, "In a nutshell", the top three big ideas. Then one list of rows to everything else
// (each opens a sheet, or goes to the Record tab), then the party's full documents. Same rows, same order, for every party.
function partyFacts(s) {
  const g = guideParty(s) || {}; const pols = (S.policies || {})[s] || [];
  const cost = g.costings && typeof g.costings === 'object' ? g.costings : (g.costings ? { summary: T(g.costings) } : null);
  const cs = g.coalition_stance_2026; const csObj = cs && typeof cs === 'object' ? cs : { summary: T(cs) };
  const ideas = (g.big_ideas || []).length ? g.big_ideas.map((b, i) => { const ids = (b && b.policy_ids) || []; const ps = pols.filter(x => ids.includes(x.id)); const docs = ideaDocs(ps);
      return `<li><div><span class="idea__t">${esc(b.text || b)}</span><span class="pol__m">${ps.length ? `${ps.length} ${ps.length === 1 ? 'policy' : 'policies'}` : ''}${docs.length ? `${ps.length ? ' · ' : ''}<button class="linkbtn" type="button" data-idea="${i}">Read the full text</button>` : ''}${!docs.length && b.source ? `${ps.length ? ' · ' : ''}${ptExt(b.source, 'source')}` : ''}</span></div></li>` })
    : pols.filter(isKey).slice(0, 7).map(x => `<li><div><span class="idea__t">${esc(x.statement)}</span><span class="pol__m">${esc(TOPIC_NAMES[topicOf(x)] || 'Other')}${ideaDocs([x]).length ? ` · <button class="linkbtn" type="button" data-doc="${esc(s)}|${esc(ideaDocs([x])[0])}">Read the full text</button>` : ''}</span></div></li>`);
  return { g, pols, cost, costYes: !!(cost && cost.published === true), csObj, ideas, ideasLabel: (g.big_ideas || []).length ? 'big ideas' : 'headline policies' };
}
const ptAZ = L => (L || []).slice().sort((a, b) => ptCmp(pname(a), pname(b)));
function partyOverview(s, pols, prom) {
  const { g, cost, costYes, csObj, ideas, ideasLabel } = partyFacts(s); const pp = P(s);
  const cur = g.current_seats || {}; const seats = partySeats(s);
  const topics = new Set(pols.map(topicOf)).size; const nm = esc(pname(s));
  const sec = (id, title, inner, extra = '', quiet = false) => `<section class="stack" aria-labelledby="h-${id}"><div class="shead${quiet ? ' shead--quiet' : ''}"><div class="shead__row"><h2 id="h-${id}"${quiet ? ' class="h3"' : ''}>${title}</h2>${extra}</div></div>${inner}</section>`;
  const sc = scoreOf(prom); const hasSides = T(g.they_say) || T(g.critics_say);
  const open = ptAZ(csObj.open_to), out = ptAZ(csObj.rules_out);
  const workSub = open.length || out.length ? [open.length ? 'Open to ' + open.map(x => esc(pname(x))).join(', ') : '', out.length ? 'rules out ' + out.map(x => esc(pname(x))).join(', ') : ''].filter(Boolean).join(' · ') : T(csObj) ? 'Their stated position on post-election partners' : 'No public statement found';
  const ovRow = (key, icon, title, sub) => `<button class="rowlink ov-row" type="button" data-ov="${key}" aria-haspopup="dialog"><span class="rowlink__icon">${ic(icon)}</span><span><span class="rowlink__title">${esc(title)}</span><span class="rowlink__sub" style="display:block">${sub}</span></span>${ic('chev')}</button>`;
  const nSrc = (g.sources || []).length; const checked = ptDate((cur.as_of || (S.data.generated || '').slice(0, 10)));
  return `<div class="party-layout">
    <dl class="glance">
      <div><dt>MPs now</dt><dd>${seats}<small>of ${esc(cur.of || (currentParl() || {}).total_now_or_end || 123)} seats${cur.as_of ? ' · ' + ptDate(cur.as_of, { day: 'numeric', month: 'short' }) : ''}</small></dd></div>
      <div><dt>2026 policies</dt><dd>${pols.length}<small>${pols.length ? `${topics} topic${topics === 1 ? '' : 's'}` : 'none on file yet'}</small></dd></div>
      <div><dt>Promises checked</dt><dd>${prom.length || '–'}<small>${prom.length ? 'with sources' : 'not tracked yet'}</small></dd></div>
      <div><dt>Numbers costed?</dt><dd>${cost ? (costYes ? 'Yes' : 'No') : '–'}<small>${cost ? (costYes ? 'party-published' : 'no full plan found') : 'not checked'}</small></dd></div>
    </dl>
    <div class="stack stack--xl party-layout__main">
      ${sec('nut', 'In a nutshell', g.in_a_nutshell ? `<div class="prose"><p>${esc(g.in_a_nutshell)}</p></div>` : pp.intro ? `<div class="prose">${md(pp.intro)}</div>` : '<p class="muted">A plain summary has not been written yet.</p>')}
      ${sec('big', (g.big_ideas || []).length ? 'Big ideas for 2026' : 'Headline policies', ideas.length ? `<ol class="ideas">${ideas.slice(0, 3).join('')}</ol>` : '<p class="muted">No headline policies on file yet.</p>', pols.length ? `<a class="more small" href="#/parties/${esc(s)}/policies">All ${pols.length} policies ${ic('chev', 'i--xs')}</a>` : '')}
      ${sec('more', `More about ${nm}`, `<div class="rows">
        ${ovRow('big-ideas', 'list', `All ${ideasLabel}`, ideas.length ? `${ideas.length}, each linked to the policies and documents behind it` : 'None on file yet')}
        ${ovRow('two-sides', 'scale', 'Two sides', hasSides ? 'What they say, and what critics say, with sources' : 'Not summarised yet')}
        ${ovRow('work-with', 'users', "Who they'd work with", workSub)}
        <a class="rowlink" href="#/parties/${esc(s)}/record"><span class="rowlink__icon">${ic('history')}</span><span><span class="rowlink__title">Keeping their word</span><span class="rowlink__sub" style="display:block">${prom.length ? `${sc.n} promises checked${sc.score != null ? `, ${sc.score}% kept` : ''} · verdicts by term, with sources` : 'The promise check is still being researched'}</span></span>${ic('chev')}</a>
        ${ovRow('costed', 'doc', 'Are the numbers costed?', cost ? (costYes ? 'Yes, party-published' : 'No full costing published') : 'Not checked yet')}
        ${ovRow('results', 'poll', 'Election results', 'Party vote and seats at each election since 2008')}
        ${ovRow('sources', 'info', 'Sources', `${nSrc ? `${nSrc} source${nSrc === 1 ? '' : 's'} for this summary · ` : ''}checked ${checked}`)}</div>`)}
      ${sec('deep', 'Full documents', `<div class="rows" style="border-top:0">
        ${pp.has_readme ? deepRow('book', 'Full party profile and history', `${g.founded ? 'Founded ' + esc(g.founded) + ' · ' : ''}leaders · every result`, `#/about/page/parties/${s}/README.md`) : ''}
        ${pp.has_track_record ? deepRow('history', 'Full track record, with sources', prom.length ? `${prom.length} promises checked` : 'The written record', `#/about/page/parties/${s}/track-record.md`) : ''}
        ${deepRow('doc', 'Policy index', `${pols.length} policies${pols.length ? ` across ${topics} topic${topics === 1 ? '' : 's'}` : ''}, with the documents they come from`, `#/about/page/parties/${s}/policies/README.md`)}
        ${deepRow('news', 'From the party', 'Latest press releases and where to follow them', `#/parties/news/${s}`)}
        ${g.website ? deepRow('ext', 'Party website', esc(ptHost(g.website)), g.website, true) : ''}</div>`, '', true)}
    </div>
    <aside class="stack stack--l party-layout__side"><p class="src">${ic('clock')} Summary checked ${checked} · <a href="${CORRECTION_URL}" target="_blank" rel="noopener">report an error</a></p></aside>
  </div>`;
}
// Layer 3 for the Overview rows. Same content as the old long Overview, one section per sheet.
function openPartySheet(s, key) {
  const { g, cost, costYes, csObj, ideas, ideasLabel } = partyFacts(s); const name = pname(s); const tag = ptTag(s);
  const back = `<p class="small"><a class="more" href="#/parties/${esc(s)}">${esc(name)} overview ${ic('chev', 'i--xs')}</a></p>`;
  const chips = (L, no) => ptAZ(L).map(x => `<a class="pchip${no ? ' pchip--no' : ''}" href="#/parties/${esc(x)}" style="--pc:${pcolor(x)}"><span class="sw"></span>${esc(pname(x))}${no ? '<span class="sr-only"> (ruled out)</span>' : ''}</a>`).join('');
  const side = (v, cls, k) => T(v) ? `<div class="side${cls}"><span class="eyebrow">${k}</span><blockquote>${esc(T(v))}</blockquote><p class="src"><span class="nm">${[v.attribution || v.who, v.date ? ptDate(v.date) : ''].filter(Boolean).map(esc).join(' · ')}</span>${srcOf(v).length ? ' · ' + ptSources(v) : ''}</p></div>` : '';
  const cur = g.current_seats || {};
  const S_ = {
    'big-ideas': () => [(g.big_ideas || []).length ? `Big ideas for 2026` : 'Headline policies', ideas.length ? `<ol class="ideas">${ideas.join('')}</ol>${((S.policies || {})[s] || []).length ? `<a class="more small" href="#/parties/${esc(s)}/policies">All ${S.policies[s].length} policies ${ic('chev', 'i--xs')}</a>` : ''}` : `<p class="muted">No ${ideasLabel} on file yet.</p>`],
    'two-sides': () => ['Two sides', T(g.they_say) || T(g.critics_say) ? `<div class="sides">${side(g.they_say, '', 'What they say')}${side(g.critics_say, ' side--critics', 'What critics say')}</div>` : '<p class="muted">Not summarised yet.</p>'],
    'work-with': () => ["Who they'd work with", `${(csObj.open_to || []).length || (csObj.rules_out || []).length || csObj.conditions ? `<div class="works">${(csObj.open_to || []).length ? `<div class="works__row"><span>Open to</span><div class="row">${chips(csObj.open_to)}</div></div>` : ''}${(csObj.rules_out || []).length ? `<div class="works__row"><span>Ruled out</span><div class="row">${chips(csObj.rules_out, true)}</div></div>` : ''}${csObj.conditions ? `<div class="works__row"><span>Conditions</span><p style="padding-top:6px">${esc(T(csObj.conditions))}</p></div>` : ''}</div>` : ''}
        ${T(csObj) ? `<p class="small soft">${esc(T(csObj))}</p>` : '<p class="muted">No public statement on post-election partners found.</p>'}${csObj.note ? `<p class="small soft">${esc(csObj.note)}</p>` : ''}
        <p class="src">${csObj.as_of ? 'As of ' + ptDate(csObj.as_of) : ''}${srcOf(csObj).length ? (csObj.as_of ? ' · ' : '') + ptSources(csObj) : ''}</p>`],
    costed: () => ['Are the numbers costed?', cost ? `<p><span class="badge ${costYes ? 'badge--ink' : 'badge--outline'}">${costYes ? 'Yes, party-published' : 'No full costing published'}</span></p>${T(cost) ? `<p class="soft">${esc(T(cost))}</p>` : ''}<p class="src">${cost.date ? ptDate(cost.date) : 'Date not recorded'}${srcOf(cost).length ? ' · ' + ptSources(cost) : ''}</p>` : '<p class="muted">Not checked yet.</p>'],
    results: () => ['Election results', partyResultsMini(s, false, false)],
    sources: () => ['Sources for this summary', `${(g.sources || []).length ? `<ul class="small src-list">${g.sources.map(u => { const url = typeof u === 'string' ? u : u.url; return `<li>${ptExt(url, esc(typeof u === 'string' ? ptSrcLabel(u) : (u.title || u.url)))}</li>` }).join('')}</ul>` : '<p class="muted">No sources listed for this summary yet.</p>'}
      <p class="src">${ic('clock')} Summary checked ${ptDate((cur.as_of || (S.data.generated || '').slice(0, 10)))} · <a href="${CORRECTION_URL}" target="_blank" rel="noopener">report an error</a></p>`] };
  if (!S_[key]) return; const [title, html] = S_[key]();
  openSheet({ title, depth: ['Party', 'Summary', 'Sources'], at: key === 'sources' ? 2 : 1, src: tag, html: html + back });
  if (key === 'big-ideas') bindIdeas($('#sheet-body'), s);
}
const ptSrcLabel = u => { try { const x = new URL(u); return (x.hostname.replace(/^www\./, '') + decodeURIComponent(x.pathname).replace(/\/$/, '')).slice(0, 72) } catch { return String(u).slice(0, 72) } };
const deepRow = (icon, title, sub, href, ext = false) => `<a class="rowlink" href="${esc(href)}"${ext ? ' target="_blank" rel="noopener"' : ''}><span class="rowlink__icon">${ic(icon)}</span><span><span class="rowlink__title">${esc(title)}</span><span class="rowlink__sub" style="display:block">${sub}</span></span>${ic('chev')}</a>`;
// Documents behind a set of policies, de-duplicated, in policy order.
function ideaDocs(ps) { const seen = new Set(); const out = []; for (const x of ps) for (const d of (x.sources || [])) if (d.document && !seen.has(d.document)) { seen.add(d.document); out.push(d.document) } return out }
function bindIdeas(el, s) {
  el.querySelectorAll('[data-idea]').forEach(b => b.onclick = () => { const idea = (guideParty(s) || {}).big_ideas[+b.dataset.idea]; const ps = (S.policies[s] || []).filter(x => (idea.policy_ids || []).includes(x.id));
    const docs = ideaDocs(ps); if (docs.length) openDoc(s, docs[0], { related: docs, context: idea.text || '' }) });
}

/* ----- Keeping their word (party Overview and Record tab) ----- */
function recordSummary(s, { inRecord = false } = {}) {
  const all = (S.data.promises || {})[s] || []; const g = guideParty(s) || {};
  const head = `<div class="shead"><div class="shead__row"><h2 id="h-rec">Keeping their word</h2>${all.length ? `<span class="micro muted">${all.length} promises tracked</span>` : ''}</div></div>`;
  if (!all.length) return `<section class="stack" aria-labelledby="h-rec">${head}<p class="muted">The promise check for this party is still being researched.</p>${P(s).has_track_record ? `<a class="more small" href="#/about/page/parties/${esc(s)}/track-record.md">Read the written track record ${ic('chev', 'i--xs')}</a>` : ''}</section>`;
  const terms = TERMS.map(([k, l]) => [k, l, all.filter(x => periodOf(x) === k)]).filter(([, , L]) => L.length);
  const sc = scoreOf(all);
  return `<section class="stack" aria-labelledby="h-rec">${head}
    ${T(g.track_record_line) ? `<p class="soft">${esc(T(g.track_record_line))}</p>` : ''}
    <p class="small"><b>All time:</b> ${sc.n} promises checked${sc.score != null ? `, <b>${sc.score}%</b> kept` : ''}.</p>
    <div class="terms">${terms.map(([k, l, L]) => { const t = scoreOf(L); return `<div class="term"><div class="term__h"><span><b>${esc(l)}</b> · ${t.n} checked</span><span class="muted">${t.score != null ? `${t.score}% kept` : 'Not yet due'}</span></div>${verdictMeter(L, l)}</div>` }).join('')}</div>
    <div class="legend">${VERDICTS.filter(v => all.some(x => x.status === v)).map(v => `${verdictChip(v)}<b>${all.filter(x => x.status === v).length}</b>`).map(x => `<span>${x}</span>`).join('')}</div>
    ${RUBRIC_HTML('How each promise was judged')}
    <div class="row">${inRecord ? '' : `<a class="more small" href="#/parties/${esc(s)}/record">See every promise, with sources ${ic('chev', 'i--xs')}</a>`}${P(s).has_track_record ? `<a class="more small" href="#/about/page/parties/${esc(s)}/track-record.md">Full track record ${ic('chev', 'i--xs')}</a>` : ''}</div></section>`;
}
// Party vote at each election since 2008, as .rrow bars (party colour only via --pc).
function partyResultsMini(s, big = false, head = true) {
  const h = head ? `<h2 id="h-res" class="h4">Party vote at each election</h2>` : '';
  const els = S.data.elections.filter(e => e.year >= 2008); const rows = els.map(e => { const r = (e.parties || []).find(x => x.party === s); return [e.year, r] });
  if (!rows.some(([, r]) => r)) return `<section class="stack stack--s">${h}<p class="small muted">Has not stood for the party vote at an election since 2008.</p></section>`;
  const max = Math.max(10, ...rows.map(([, r]) => r ? r.party_vote_pct : 0));
  return `<section class="stack stack--s"${head ? ' aria-labelledby="h-res"' : ''}>${h}<div>${rows.map(([y, r], i) => `<div class="rrow rrow--yr" style="--pc:${pcolor(s)}"><span class="num">${y}</span><div class="bar"><i style="--w:${r ? (r.party_vote_pct / max * 100).toFixed(1) : 0}%;--i:${i}"></i></div><span class="rrow__v">${r ? `<b>${fmt(r.party_vote_pct)}%</b><span>${r.total_seats || 0} seat${r.total_seats === 1 ? '' : 's'}</span>` : '<span>did not stand</span>'}</span></div>`).join('')}</div>
    <p class="src">Electoral Commission results, via Wikipedia: ${els.map(e => { const u = String((e.sources || [])[0] || '').split(' ')[0]; return u ? ptExt(u, String(e.year)) : '' }).join(' ')}${big ? ' · bars scaled to the party’s best result' : ''}</p></section>`;
}
