/* ----- policy browser (shared) ----- */
const TOPIC_NAMES = { economy: 'Economy & tax', health: 'Health', education: 'Education', housing: 'Housing', environment: 'Environment & climate', 'law-justice-and-government': 'Law, justice & government',
  'community-and-inclusion': 'Community & inclusion', 'te-ao-maori': 'Te ao Māori', migration: 'Immigration', 'transport-and-infrastructure': 'Transport & infrastructure',
  'incomes-and-employment': 'Incomes & jobs', 'defence-and-foreign-affairs': 'Defence & foreign affairs', 'media-culture-and-recreation': 'Media, culture & recreation' };
const isKey = x => !!(x.key_policy || (x.topics || []).some(t => String(t).startsWith('key-policies')));
const topicOf = pol => (pol.topics || []).find(x => TOPIC_NAMES[x]) || 'other';
function docButtons(p, pol) {
  const seen = new Set(); const docs = (pol.sources || []).filter(x => x.document && !seen.has(x.document) && seen.add(x.document));
  const links = (pol.sources || []).filter(x => !x.document && x.url).slice(0, 2);
  if (!docs.length && !links.length) return '';
  const lab = x => String(x.title || x.document.split('/').pop().replace(/\.md$/, '').replace(/-/g, ' ')).replace(/^['"]|['"]$/g, '');
  return `<div class="srcs">${docs.length === 1 ? `<button class="btn sm primary" data-doc="${esc(p)}|${esc(docs[0].document)}">Read the full policy</button>` : docs.length ? `<span class="tiny muted" style="align-self:center">Full text:</span>${docs.slice(0, 6).map(x => `<button class="btn sm" data-doc="${esc(p)}|${esc(x.document)}" title="${esc(lab(x))}">${esc(lab(x).slice(0, 38))}${lab(x).length > 38 ? '…' : ''}</button>`).join('')}` : ''}${links.map(x => `<a class="btn sm ghost" href="${esc(x.url)}" target="_blank" rel="noopener">Original source</a>`).join('')}</div>`;
}
function policyCard(p, pol, showParty = true) {
  const sm = pol.summary || {};
  return `<article class="pol"><div class="head">${showParty ? `<span class="dot" style="background:${pcolor(p)};margin-top:6px"></span>` : ''}<div style="min-width:0"><div class="st">${esc(pol.statement)}</div>
    <div class="tiny muted">${showParty ? esc(pname(p)) + ' · ' : ''}${esc(TOPIC_NAMES[topicOf(pol)] || 'Other')}${isKey(pol) ? ' · <b style="color:var(--primary)">headline policy</b>' : ''}</div></div></div>
    ${sm.why || sm.how || sm.text ? `<details><summary>Why and how</summary>${sm.why ? `<p><b>Why:</b> ${esc(sm.why)}</p>` : ''}${sm.how ? `<p><b>How:</b> ${esc(sm.how)}</p>` : ''}${sm.text ? `<p>${esc(sm.text)}</p>` : ''}${sm.cost || pol.costing ? `<p><b>Cost:</b> ${esc(sm.cost || (typeof pol.costing === 'string' ? pol.costing : JSON.stringify(pol.costing)))}</p>` : ''}</details>` : ''}
    ${docButtons(p, pol)}</article>`;
}
async function policyBrowser(el, only = null) {
  if (!S.policies) S.policies = await getJSON('data/policies.json').catch(() => ({}));
  const parties = (only || Object.keys(S.policies)).filter(p => (S.policies[p] || []).length).sort((a, b) => S.policies[b].length - S.policies[a].length);
  if (!parties.length) { el.innerHTML = '<p class="empty">Policies for this party are still being collected.</p>'; return }
  el.innerHTML = `<div class="stack" style="gap:14px"><div class="toolbar"><input type="search" id="q" placeholder="Search, e.g. GST, rent, KiwiSaver, gangs" aria-label="Search policies">
    <select id="topic" aria-label="Topic"><option value="">All topics</option>${Object.entries(TOPIC_NAMES).map(([t, n]) => `<option value="${t}">${n}</option>`).join('')}<option value="other">Other</option></select></div>
    ${only && only.length === 1 ? '' : `<div class="chips" id="pchips">${parties.map(p => `<button class="chip" data-p="${p}" aria-pressed="true"><span class="dot" style="background:${pcolor(p)}"></span>${esc(pname(p))} <span class="num muted">${S.policies[p].length}</span></button>`).join('')}</div>`}
    <div id="plist"></div></div>`;
  const on = new Set(parties); let limit = 40; const single = only && only.length === 1;
  const draw = () => { const q = $('#q', el).value.trim().toLowerCase(), t = $('#topic', el).value;
    const match = pol => (!t || topicOf(pol) === t) && (!q || (pol.statement + ' ' + JSON.stringify(pol.summary || {})).toLowerCase().includes(q));
    if (t && !single) { $('#plist', el).innerHTML = `<div class="cols">${parties.filter(p => on.has(p)).map(p => { const ps = S.policies[p].filter(match);
        return `<div><h3 class="row" style="gap:8px"><span class="dot" style="background:${pcolor(p)}"></span>${esc(pname(p))} <span class="num muted small">${ps.length}</span></h3>${ps.length ? ps.map(x => policyCard(p, x, false)).join('') : '<p class="empty small">Nothing published on this topic.</p>'}</div>` }).join('')}</div>`; return }
    const all = []; parties.filter(p => on.has(p)).forEach(p => S.policies[p].filter(match).forEach(x => all.push([p, x])));
    if (single && !q && !t) { // group by topic
      const by = {}; all.forEach(([p, x]) => (by[topicOf(x)] = by[topicOf(x)] || []).push([p, x]));
      $('#plist', el).innerHTML = Object.entries(by).sort((a, b) => b[1].length - a[1].length).map(([tp, xs]) => `<details class="card flat" ${xs.length < 8 ? '' : ''}><summary style="cursor:pointer"><h3 style="display:inline">${esc(TOPIC_NAMES[tp] || 'Other')}</h3> <span class="muted num small">${xs.length}</span></summary><div class="stack" style="margin-top:12px">${xs.map(([p, x]) => policyCard(p, x, false)).join('')}</div></details>`).join('');
      return }
    $('#plist', el).innerHTML = `<p class="small muted">${all.length} matching policies</p><div class="stack" style="gap:10px">${all.slice(0, limit).map(([p, x]) => policyCard(p, x, !single)).join('')}</div>${all.length > limit ? `<div class="row" style="justify-content:center;margin-top:12px"><button class="btn primary" id="more">Show more</button></div>` : ''}`;
    const m = $('#more', el); if (m) m.onclick = () => { limit += 40; draw() } };
  $('#q', el).oninput = () => { limit = 40; draw() }; $('#topic', el).onchange = draw;
  const pc = $('#pchips', el); if (pc) pc.onclick = e => { const b = e.target.closest('[data-p]'); if (!b) return; on.has(b.dataset.p) ? on.delete(b.dataset.p) : on.add(b.dataset.p); pc.querySelectorAll('[data-p]').forEach(x => x.setAttribute('aria-pressed', on.has(x.dataset.p))); draw() };
  draw();
}
V.policies = async () => {
  $('#main').innerHTML = `<section class="view"><div class="stack"><div class="kicker">Election 2026</div><h2>Every policy, side by side</h2><p class="lede">Search all parties' published policies. Pick a topic to compare parties in columns. Each policy links to the party's full original text.</p></div><div id="pb"></div></section>`;
  policyBrowser($('#pb'));
};
async function openDoc(party, path) {
  openDialog('Loading…', '<p class="empty">Fetching the full text…</p>');
  if (!S.fulltext[party]) S.fulltext[party] = await getJSON(`data/fulltext/${party}.json`).catch(() => ({}));
  const d = S.fulltext[party][path];
  if (!d) { openDialog('Not found', `<p>This document isn't in the bundle yet (${esc(path)}).</p>`); return }
  openDialog(d.title, `<p class="small muted">${esc(P(party).name)} · ${d.source_url ? `<a href="${esc(d.source_url)}" target="_blank" rel="noopener">original source</a>` : ''} ${d.retrieved ? '· retrieved ' + esc(d.retrieved) : ''}</p><div class="prose">${md(d.text)}</div>`) }

/* ----- issues ----- */
V.issues = () => {
  const iss = G().issues || [];
  $('#main').innerHTML = `<section class="view"><div class="stack"><div class="kicker">What's at stake</div><h2>The big issues</h2><p class="lede">Pick an issue to see the key facts and where every party stands, in plain English.</p></div>
    ${iss.length ? `<div class="grid">${iss.map(i => `<button class="starter" data-go="issue-${esc(i.slug)}"><h3>${esc(i.title)}</h3><p class="small muted">${esc((i.why_it_matters || '').slice(0, 150))}${(i.why_it_matters || '').length > 150 ? '…' : ''}</p>
      <div class="row" style="gap:4px">${Object.keys(i.positions || {}).sort((a, b) => P(a).order - P(b).order).map(p => `<span class="dot" title="${esc(pname(p))}" style="background:${pcolor(p)}"></span>`).join('')}</div><span class="go">Compare ${Object.keys(i.positions || {}).length} parties →</span></button>`).join('')}</div>`
    : `<p class="empty">Issue guides are being written. Meanwhile, compare by topic in <button class="btn ghost sm" data-go="policies">the policy browser</button>.</p>`}</section>`;
};
V.issue = slug => {
  const i = (G().issues || []).find(x => x.slug === slug); if (!i) return V.issues();
  const order = Object.keys(i.positions || {}).sort((a, b) => (projection().pct[b] || 0) - (projection().pct[a] || 0));
  $('#main').innerHTML = `<section class="view"><button class="btn ghost sm" data-go="issues" style="justify-self:start">← All issues</button>
    <div class="stack"><div class="kicker">Issue</div><h1 style="font-size:clamp(30px,5vw,46px)">${esc(i.title)}</h1><p class="lede">${esc(i.why_it_matters || '')}</p></div>
    ${(i.key_facts || []).length ? `<div class="grid">${i.key_facts.map(f => `<div class="card flat stack" style="gap:6px"><p>${esc(typeof f === 'string' ? f : f.fact || f.text)}</p><div class="tiny muted">${f.date ? esc(f.date) + ' · ' : ''}${srcLinks(f)}</div></div>`).join('')}</div>` : ''}
    <div class="stack"><h2>Where the parties stand</h2><div class="grid wide">${order.map(p => { const x = i.positions[p];
      return `<div class="card stack" style="--pc:${pcolor(p)};border-top:6px solid ${pcolor(p)}"><div class="row"><h3>${esc(pname(p))}</h3></div><p>${esc(T(x))}</p>${srcLinks(x)}
      ${(x.policy_ids || []).length ? `<button class="btn sm" data-issuepol="${esc(p)}|${esc(x.policy_ids.join(','))}" style="justify-self:start">${x.policy_ids.length} related ${x.policy_ids.length === 1 ? 'policy' : 'policies'}</button>` : ''}</div>` }).join('')}</div></div>
    ${(i.sources || []).length ? `<details class="tiny muted"><summary>Sources</summary><ul>${i.sources.map(u => `<li><a href="${esc(typeof u === 'string' ? u : u.url)}" target="_blank" rel="noopener">${esc(typeof u === 'string' ? u : (u.title || u.url))}</a></li>`).join('')}</ul></details>` : ''}</section>`;
};
async function showIssuePolicies(p, ids) {
  if (!S.policies) S.policies = await getJSON('data/policies.json').catch(() => ({}));
  const set = new Set(ids.split(',')); const ps = (S.policies[p] || []).filter(x => set.has(x.id));
  openDialog(`${pname(p)}: related policies`, ps.length ? `<div class="stack">${ps.map(x => policyCard(p, x, false)).join('')}</div>` : '<p class="empty">These policies are still being added.</p>') }
