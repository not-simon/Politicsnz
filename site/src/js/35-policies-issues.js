/* ----- policy browser (shared: Parties › Policies and each party's Policies tab) ----- */
const TOPIC_NAMES = { economy: 'Economy & tax', health: 'Health', education: 'Education', housing: 'Housing', environment: 'Environment & climate', 'law-justice-and-government': 'Law, justice & government',
  'community-and-inclusion': 'Community & inclusion', 'te-ao-maori': 'Te ao Māori', migration: 'Immigration', 'transport-and-infrastructure': 'Transport & infrastructure',
  'incomes-and-employment': 'Incomes & jobs', 'defence-and-foreign-affairs': 'Defence & foreign affairs', 'media-culture-and-recreation': 'Media, culture & recreation' };
const isKey = x => !!(x.key_policy || (x.topics || []).some(t => String(t).startsWith('key-policies')));
const topicOf = pol => (pol.topics || []).find(x => TOPIC_NAMES[x]) || 'other';
const DOC_DEPTH = ['Summary', 'Policy', 'Full text'];
// Source line for one policy: one "Read the full text" control (the party's own document, in the reader sheet) plus the original links.
function docButtons(p, pol) {
  const docs = ideaDocs([pol]); const links = (pol.sources || []).filter(x => x.url);
  const seen = new Set(); const uniq = links.filter(x => !seen.has(x.url) && seen.add(x.url));
  if (!docs.length && !uniq.length) return '<p class="src">No source recorded</p>';
  return `<p class="src">${docs.length ? `<button class="linkbtn" type="button" data-doc="${esc(p)}|${esc(docs[0])}">Read the full text</button>${docs.length > 1 ? `<span>${docs.length} documents</span>` : ''}` : ''}
    ${uniq.map(x => { const t = String(x.title || '').replace(/^['"‘]|['"’]$/g, '').replace(/['"’],.*$/, ''); return ptExt(x.url, esc(t ? (t.length > 48 ? t.slice(0, 46) + '…' : t) : ptHost(x.url) || 'original source') + ' ' + ic('ext', 'i--xs')) }).join('')}${pol.summary_source ? `<span>Summary: ${esc(String(pol.summary_source).replace(/^archive\b/, 'Ballot Book'))}</span>` : ''}</p>`;
}
// Freshness: withdrawn (no longer on policy.nz since capture) stays listed, greyed, at the end of its group; new ones get a badge.
const polGone = pol => !!pol.withdrawn && !(pol.reinstated && String(pol.reinstated) >= String(pol.withdrawn));
const polOrder = L => L.filter(x => !polGone(x)).concat(L.filter(polGone));
function polBadges(pol) { return `${polGone(pol) ? `<span class="badge badge--outline">Withdrawn ${esc(ptDate(pol.withdrawn))}</span>` : ''}${pol.reinstated && !polGone(pol) ? `<span class="badge badge--outline">Back ${esc(ptDate(pol.reinstated))}</span>` : ''}${pol.added ? `<span class="badge badge--outline">New ${esc(ptDate(pol.added))}</span>` : ''}` }
function policyCard(p, pol, showParty = true) {
  const sm = pol.summary || {};
  return `<article class="pol${polGone(pol) ? ' pol--gone' : ''}" style="--pc:${pcolor(p)}"><p class="pol__t st">${esc(pol.statement)}</p>
    <p class="pol__m">${showParty ? ptTag(p) : ''}<span>${esc(TOPIC_NAMES[topicOf(pol)] || 'Other')}</span>${isKey(pol) ? '<span class="badge badge--outline">Headline policy</span>' : ''}${polBadges(pol)}</p>
    ${sm.why || sm.how || sm.text || pol.costing ? `<details class="disclose disclose--pol"><summary>Why and how</summary><div class="disclose__body small">${sm.why ? `<p><b>Why:</b> ${esc(sm.why)}</p>` : ''}${sm.how ? `<p><b>How:</b> ${esc(sm.how)}</p>` : ''}${sm.text ? `<p>${esc(sm.text)}</p>` : ''}${sm.cost || pol.costing ? `<p><b>Cost:</b> ${esc(sm.cost || (typeof pol.costing === 'string' ? pol.costing : JSON.stringify(pol.costing)))}</p>` : ''}</div></details>` : ''}
    ${docButtons(p, pol)}</article>`;
}
async function policyBrowser(el, only = null, { topic = '' } = {}) {
  if (!S.policies) S.policies = await getJSON('data/policies.json').catch(() => ({}));
  const parties = (only || Object.keys(S.policies)).filter(p => (S.policies[p] || []).length).sort((a, b) => ptCmp(pname(a), pname(b)));
  if (!parties.length) { el.innerHTML = '<p class="muted">Policies for this party are still being collected.</p>'; return }
  const single = !!(only && only.length === 1);
  let t = TOPIC_NAMES[topic] || topic === 'other' ? topic : '', q = '', limit = 40; const on = new Set(parties);
  el.innerHTML = `<div class="stack stack--l"><div class="toolbar">
      <div class="input-icon"><label class="sr-only" for="q">Search policies</label>${ic('search', 'i--s')}<input class="input" type="search" id="q" placeholder="Search, e.g. GST, rent, KiwiSaver, gangs"></div>
      <div class="chips chips--scroll" id="tchips" role="group" aria-label="Topic"></div>
      ${single ? '' : `<details class="disclose"><summary>Parties <span class="micro muted" id="pcount" style="margin-left:auto">all ${parties.length} shown</span></summary><div class="disclose__body"><div class="chips" id="pchips" role="group" aria-label="Parties">${parties.map(p => `<button class="chip" type="button" data-p="${p}" aria-pressed="true"><span class="sw" style="--pc:${pcolor(p)}"></span>${esc(pname(p))} <span class="count">${S.policies[p].length}</span></button>`).join('')}<button class="linkbtn small" type="button" id="pall">All parties</button></div></div></details>`}</div>
    <div id="plist" class="stack stack--l"></div></div>`;
  const matchQ = pol => !q || (pol.statement + ' ' + JSON.stringify(pol.summary || {})).toLowerCase().includes(q);
  const drawTopics = () => { const n = k => parties.filter(p => on.has(p)).reduce((a, p) => a + S.policies[p].filter(x => matchQ(x) && (!k || topicOf(x) === k)).length, 0);
    $('#tchips', el).innerHTML = [['', 'All topics'], ...Object.entries(TOPIC_NAMES), ['other', 'Other']].map(([k, l]) => [k, l, n(k)]).filter(([k, , c]) => !k || c || k === t).map(([k, l, c]) => `<button class="chip" type="button" data-t="${k}" aria-pressed="${t === k}">${esc(l)} <span class="count">${c}</span></button>`).join('') };
  const draw = () => { drawTopics(); const tc = $('#tchips', el), cur = tc.querySelector('[aria-pressed="true"]'); if (cur && t) tc.scrollLeft = Math.max(0, cur.offsetLeft - tc.offsetLeft - 16);
    const match = pol => (!t || topicOf(pol) === t) && matchQ(pol); const box = $('#plist', el);
    if (t && !single) { const ps = parties.filter(p => on.has(p));   // a topic picked: parties side by side, A–Z
      box.innerHTML = `<div class="shead"><div class="shead__row"><h2 class="h3">${esc(TOPIC_NAMES[t] || 'Other')}, party by party</h2><span class="micro muted">${ps.length} parties, A to Z</span></div></div><p class="small muted">Each column shows the first three of that party's published policies on this topic; open "All" for the rest.</p>
        <div class="cols ${ps.length > 2 ? 'cols--3' : 'cols--2'} pcols">${ps.map(p => { const L = polOrder(S.policies[p].filter(match));
        return `<section class="pgroup" style="--pc:${pcolor(p)}"><div class="pgroup__h"><h3>${esc(pname(p))}</h3><a class="more micro" href="#/parties/${esc(p)}/policies" aria-label="All ${S.policies[p].length} ${esc(pname(p))} policies">All ${S.policies[p].length} policies</a></div>${L.length ? L.slice(0, 3).map(x => policyCard(p, x, false)).join('') + (L.length > 3 ? `<details class="disclose disclose--more"><summary>All ${L.length} on this topic <span class="micro muted" style="margin-left:auto">${L.length - 3} more</span></summary><div class="disclose__body">${L.slice(3).map(x => policyCard(p, x, false)).join('')}</div></details>` : '') : '<p class="small muted">Nothing published on this topic.</p>'}</section>` }).join('')}</div>`; return }
    const all = []; parties.filter(p => on.has(p)).forEach(p => polOrder(S.policies[p].filter(match)).forEach(x => all.push([p, x])));
    if (single && !q && !t) { // one party, no filter: grouped by topic
      const by = {}; all.forEach(([p, x]) => (by[topicOf(x)] = by[topicOf(x)] || []).push([p, x])); Object.keys(by).forEach(k => { by[k] = by[k].filter(([, x]) => !polGone(x)).concat(by[k].filter(([, x]) => polGone(x))) });
      box.innerHTML = `<p class="small muted">${all.length} policies in ${Object.keys(by).length} topics. Open a topic, or pick one above.</p><div>${Object.entries(by).sort((a, b) => b[1].length - a[1].length || ptCmp(TOPIC_NAMES[a[0]] || 'Other', TOPIC_NAMES[b[0]] || 'Other')).map(([tp, xs]) => `<details class="disclose"><summary>${esc(TOPIC_NAMES[tp] || 'Other')} <span class="micro muted" style="margin-left:auto">${xs.length}</span></summary><div class="disclose__body">${xs.map(([p, x]) => policyCard(p, x, false)).join('')}</div></details>`).join('')}</div>`;
      return }
    box.innerHTML = `<p class="small muted">${all.length} matching ${all.length === 1 ? 'policy' : 'policies'}${single ? '' : ', grouped by party A to Z'}</p><div>${all.slice(0, limit).map(([p, x]) => policyCard(p, x, !single)).join('')}</div>${all.length > limit ? `<div class="row"><button class="btn" type="button" id="more">Show the next ${Math.min(40, all.length - limit)}</button><span class="small muted">${limit} of ${all.length} shown</span></div>` : ''}`;
    const m = $('#more', el); if (m) m.onclick = () => { limit += 40; draw() } };
  $('#q', el).oninput = e => { q = e.target.value.trim().toLowerCase(); limit = 40; draw() };
  $('#tchips', el).onclick = e => { const b = e.target.closest('[data-t]'); if (!b) return; t = b.dataset.t; limit = 40; draw() };
  const pc = $('#pchips', el); if (pc) pc.onclick = e => { if (e.target.closest('#pall')) parties.forEach(p => on.add(p)); else { const b = e.target.closest('[data-p]'); if (!b) return; on.has(b.dataset.p) ? on.delete(b.dataset.p) : on.add(b.dataset.p) }
    pc.querySelectorAll('[data-p]').forEach(x => x.setAttribute('aria-pressed', on.has(x.dataset.p))); $('#pcount', el).textContent = on.size === parties.length ? `all ${parties.length} shown` : `${on.size} of ${parties.length} shown`; limit = 40; draw() };
  draw();
}
V.policies = async arg => {
  if (!S.policies) S.policies = await getJSON('data/policies.json').catch(() => ({}));
  const n = Object.values(S.policies).reduce((a, L) => a + L.length, 0);
  $('#main').innerHTML = sectionFrame('parties', 'parties/policies', `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('doc', 'i--s')} Parties · Policies</p><h1>Every policy, side by side</h1>
    <p class="lede">Search ${n.toLocaleString('en-NZ')} published policies from every party. Pick a topic to compare parties in columns. Each policy links to the party's full original text.</p></header><div id="pb"></div>`);
  policyBrowser($('#pb'), null, { topic: arg || '' });
};
// Layer 3: the party's own document in the reader sheet.
async function openDoc(party, path, { related = null, context = '' } = {}) {
  if (!S.policies) S.policies = await getJSON('data/policies.json').catch(() => ({}));
  if (!related) { const pol = (S.policies[party] || []).find(x => (x.sources || []).some(d => d.document === path));   // the policy this document backs
    if (pol) { related = ideaDocs([pol]); if (!context) context = 'Policy: ' + pol.statement } }
  openSheet({ title: 'Loading…', depth: DOC_DEPTH, at: 2, html: '<p class="muted">Fetching the full text…</p>' });
  if (!S.fulltext[party]) S.fulltext[party] = await getJSON(`data/fulltext/${party}.json`).catch(() => ({}));
  const d = S.fulltext[party][path];
  if (!d) { openSheet({ title: 'Not found', depth: DOC_DEPTH, at: 2, src: ptTag(party), html: `<p>This document isn't in the bundle yet (${esc(path)}).</p>` }); return }
  const others = (related || []).filter(x => x !== path && S.fulltext[party][x]);
  openSheet({ title: d.title || path, depth: DOC_DEPTH, at: 2,
    src: `${ptTag(party)}${d.source_url ? ptExt(d.source_url, esc(ptHost(d.source_url) || 'original source')) : '<span>No original link recorded</span>'}${d.retrieved ? `<span>retrieved ${esc(ptDate(d.retrieved))}</span>` : ''}`,
    html: `${context ? `<p class="small soft">${esc(context)}</p>` : ''}<div class="note">${ic('info')}<div>The party's own words, shown as published. Not edited or fact-checked.</div></div>
      <div class="prose" data-base="parties/${esc(party)}/policies/${esc(path)}">${md(d.text)}</div>
      <div class="row">${d.source_url ? `<a class="btn btn--s" href="${esc(d.source_url)}" target="_blank" rel="noopener">Original page ${ic('ext', 'i--xs')}</a>` : ''}<a class="btn btn--s btn--quiet" href="${CORRECTION_URL}" target="_blank" rel="noopener">${ic('flag', 'i--xs')} Report a problem</a></div>
      ${others.length ? `<section class="stack stack--s"><h3 class="h4">Other documents behind this</h3><div class="rows">${others.map(x => `<button class="rowlink rowlink--plain doc-row" type="button" data-doc="${esc(party)}|${esc(x)}"><span class="rowlink__title" style="font-size:15px">${esc(S.fulltext[party][x].title || x)}</span>${ic('chev')}</button>`).join('')}</div></section>` : ''}` });
}

/* ----- issues ----- */
V.issues = () => {
  const iss = (G().issues || []).slice().sort((a, b) => ptCmp(a.title, b.title));
  $('#main').innerHTML = sectionFrame('parties', 'parties/issues', `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('scale', 'i--s')} Parties · Issues</p><h1>The big issues</h1>
    <p class="lede">Pick an issue to see the key facts and where every party stands, in plain English, with sources.</p></header>
    ${iss.length ? `<div class="rows">${iss.map(i => `<a class="rowlink rowlink--plain" href="#/parties/issues/${esc(i.slug)}"><span><span class="rowlink__title">${esc(i.title)}</span><span class="rowlink__sub" style="display:block">${esc((i.why_it_matters || '').slice(0, 160))}${(i.why_it_matters || '').length > 160 ? '…' : ''}</span><span class="micro muted" style="display:block;margin-top:4px">${(i.key_facts || []).length} key facts · ${Object.keys(i.positions || {}).length} parties' positions</span></span>${ic('chev')}</a>`).join('')}</div>`
    : `<p class="muted">Issue guides are being written. Meanwhile, compare by topic in <a href="#/parties/policies">the policy browser</a>.</p>`}`);
};
// First sentence of a position; the rest folds away under "More" (nothing is cut).
function ptSplitSentence(t) { const m = String(t || '').match(/^(.+?[.!?])(\s+)(?=[A-Z0-9“"‘'(])/); return m && m[1].length >= 40 ? [m[1], String(t).slice(m[0].length)] : [String(t || ''), ''] }
V.issue = slug => {
  const i = (G().issues || []).find(x => x.slug === slug); if (!i) return V.issues();
  const order = Object.keys(i.positions || {}).sort((a, b) => ptCmp(pname(a), pname(b)));   // A–Z, never by polling
  const facts = i.key_facts || []; const fact = f => `<div class="feed__item"><p>${esc(typeof f === 'string' ? f : f.fact || f.text)}</p><p class="src">${f.date ? `<span>${esc(ptDate(f.date))}</span>` : ''}${ptSources(f)}</p></div>`;
  $('#main').innerHTML = sectionFrame('parties', 'parties/issues', `<nav class="small" aria-label="Breadcrumb"><a href="#/parties/issues">All ${(G().issues || []).length} issues</a> <span class="muted">/ ${esc(i.title)}</span></nav>
    <header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('scale', 'i--s')} Parties · Issue</p><h1>${esc(i.title)}</h1>${i.why_it_matters ? `<p class="lede">${esc(i.why_it_matters)}</p>` : ''}</header>
    ${facts.length ? `<section class="stack" aria-labelledby="h-facts"><div class="shead"><div class="shead__row"><h2 id="h-facts">Key facts</h2><span class="micro muted">${facts.length}, with sources</span></div></div><div class="feed">${facts.slice(0, 5).map(fact).join('')}</div>
      ${facts.length > 5 ? `<details class="disclose"><summary>${facts.length - 5} more key fact${facts.length - 5 === 1 ? '' : 's'}</summary><div class="disclose__body"><div class="feed">${facts.slice(5).map(fact).join('')}</div></div></details>` : ''}</section>` : ''}
    <section class="stack" aria-labelledby="h-pos"><div class="shead"><div class="shead__row"><h2 id="h-pos">Where the parties stand</h2><span class="micro muted">${order.length} parties, A to Z</span></div></div>
      <div class="cols cols--2 positions">${order.map(p => { const x = i.positions[p]; const ids = (x && x.policy_ids) || []; const [lead, rest] = ptSplitSentence(T(x));
        return `<section class="pgroup" style="--pc:${pcolor(p)}" aria-label="${esc(pname(p))}"><div class="pgroup__h"><h3><a href="#/parties/${esc(p)}">${esc(pname(p))}</a></h3></div><p>${esc(lead)}</p>
          ${rest ? `<details class="disclose disclose--pol"><summary>More<span class="sr-only"> from ${esc(pname(p))}</span></summary><div class="disclose__body"><p>${esc(rest)}</p></div></details>` : ''}
          <p class="src">${srcOf(x).length ? ptSources(x) : ids.length ? '<span>From the party’s published policies</span>' : '<span>No source recorded</span>'}</p>
          ${ids.length ? `<button class="linkbtn small" type="button" data-issuepol="${esc(p)}|${esc(ids.join(','))}" aria-haspopup="dialog" style="justify-self:start">${ids.length} related ${ids.length === 1 ? 'policy' : 'policies'}<span class="sr-only"> from ${esc(pname(p))}</span></button>` : ''}</section>` }).join('')}</div></section>
    ${(i.sources || []).length ? `<details class="disclose"><summary>All sources for this issue <span class="micro muted">${i.sources.length}</span></summary><div class="disclose__body"><ul class="small src-list">${i.sources.map(u => `<li>${ptExt(typeof u === 'string' ? u : u.url, esc(typeof u === 'string' ? ptSrcLabel(u) : (u.title || u.url)))}</li>`).join('')}</ul></div></details>` : ''}`);
};
// Layer 3 from an issue: the policies behind one party's position.
async function showIssuePolicies(p, ids) {
  if (!S.policies) S.policies = await getJSON('data/policies.json').catch(() => ({}));
  const set = new Set(ids.split(',')); const ps = (S.policies[p] || []).filter(x => set.has(x.id));
  openSheet({ title: `${pname(p)}: related policies`, depth: DOC_DEPTH, at: 1, src: ptTag(p),
    html: ps.length ? `<div>${polOrder(ps).map(x => policyCard(p, x, false)).join('')}</div>` : '<p class="muted">These policies are still being added.</p>' }) }
