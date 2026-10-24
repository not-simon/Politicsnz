/* ===== shell: sheet, navigation, router, boot =====
   Routes are '#/section/sub/arg…' (see site/redesign/PORTING.md §3). Old-style hashes ('#match', '#party-labour') and
   data-go values are translated by normaliseRoute(), so every link that ever existed still works. */

/* ----- sheet (layer 3: full texts, people, related policies, long-form pages) ----- */
function openSheet({ title = '', depth = null, at = 2, src = '', html = '', route = null } = {}) {
  $('#sheet-title').textContent = title;
  const dep = $('#sheet-depth'); dep.innerHTML = depth ? depth.map((d, i) => `<span${i === at ? ' aria-current="step"' : ''}>${esc(d)}</span>`).join('') : ''; dep.hidden = !depth;
  const sr = $('#sheet-src'); sr.innerHTML = src || ''; sr.hidden = !src;
  $('#sheet-body').innerHTML = html;
  const d = $('#sheet');
  if (!d.open) { try { history.pushState({ sheet: route || true }, '', location.href) } catch {} d.showModal() }
  $('#sheet-body').scrollTop = 0; loadPeople().then(() => autolink($('#sheet-body'))) }
// Backwards-compatible name used by the views that have not been ported yet.
const openDialog = (title, html) => openSheet({ title, html });
function closeSheet() { const d = $('#sheet'); if (!d.open) return; if (history.state && history.state.sheet) history.back(); else d.close() }
$('#sheet-close').onclick = closeSheet;
$('#sheet').addEventListener('click', e => { if (e.target === $('#sheet')) closeSheet() });
$('#sheet').addEventListener('cancel', e => { e.preventDefault(); closeSheet() });   // Esc
addEventListener('popstate', () => { const d = $('#sheet'); if (d.open && !(history.state && history.state.sheet)) d.close() });
async function openPersonByFolder(folder) { await loadPeople(); const p = S.people.find(x => x.folder === folder); if (p) openPerson(p) }

/* ----- focus mode (quiz, swipe, game in progress): one task, one screen ----- */
function focusMode(title, exitRoute = 'choose') {
  const on = !!title; document.body.classList.toggle('focus-mode', on); document.body.classList.toggle('has-tabbar', !on);
  $('#bnav').hidden = on; $('#phase').hidden = on || !PHASE_MSG()[electionPhase()];
  const inner = $('#mast-in');
  if (on) { if (!S.mastHTML) S.mastHTML = inner.innerHTML;
    inner.innerHTML = `<a class="btn btn--quiet btn--s" href="#/${exitRoute}">${ic('close', 'i--s')} Exit</a><span class="h4" style="flex:1;text-align:center">${esc(title)}</span><div class="mast__tools"><button class="iconbtn theme-toggle" type="button" id="themebtn" aria-label="Switch light or dark">${ic('moon', 'i--s')}${ic('sun', 'i--s')}</button></div>`; bindTheme() }
  else if (S.mastHTML) { inner.innerHTML = S.mastHTML; S.mastHTML = null; bindTheme(); bindSearch(); drawNav() } }
function bindTheme() { const b = $('#themebtn'); if (!b) return; b.onclick = () => { const r = document.documentElement; const dark = r.dataset.theme === 'dark' || (!r.dataset.theme && matchMedia('(prefers-color-scheme: dark)').matches); r.dataset.theme = dark ? 'light' : 'dark'; try { localStorage.setItem('bb-theme', r.dataset.theme) } catch {} } }
function bindSearch() { const b = $('#searchbtn'); if (b) b.onclick = () => go('search') }

/* ----- navigation ----- */
function drawNav(sec) {
  $('#nav').innerHTML = SECTIONS.map(([k, l]) => `<a href="#/${k}" data-sec="${k}">${l}</a>`).join('');
  $('#bnav').innerHTML = SECTIONS.map(([k, l]) => `<a href="#/${k}" data-sec="${k}">${ic(k)}<span>${l}</span></a>`).join('');
  markNav(sec || S.sec) }
function markNav(sec) { document.querySelectorAll('[data-sec]').forEach(a => { if (a.dataset.sec === sec) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current') }) }
// Section sub-navigation: a chip row on phones, a sticky rail on desktop. `items` = [[path, label, count?]]
function subnav(sec, items, current) { const label = Object.fromEntries(SECTIONS)[sec] || sec;
  return `<nav class="subnav" aria-label="${esc(label)}"><span class="subnav__label">${esc(label)}</span>${items.map(([p, l, n]) => `<a href="#/${p}"${p === current ? ' aria-current="page"' : ''}>${esc(l)}${n != null ? ` <span class="num">${esc(String(n))}</span>` : ''}</a>`).join('')}</nav>` }
const SUBNAV = {
  vote: () => [['vote', 'Ready to vote'], ['vote/electorate', 'Your electorate'], ['vote/plan', 'Make a plan'], ['vote/dates', 'Key dates'], ['vote/mmp', 'How MMP works'], ['vote/glossary', 'Glossary'], ['vote/specials', 'Special votes'], ['vote/maori', 'Māori electorates'], ['vote/lang', 'Other languages']],
  choose: () => [['choose', 'Start here'], ['choose/swipe', 'Policy swipe'], ['choose/quiz', 'Find your match'], ['choose/compass', 'Values compass'], ['choose/game', 'Whose policy? game'], ['choose/compare', 'Compare two parties'], ['choose/results', 'Your results']],
  parties: () => [['parties', 'Parties', (G().parties || []).length || null], ['parties/issues', 'Issues', (G().issues || []).length || null], ['parties/policies', 'Policies', Object.values(S.data.parties || {}).reduce((a, p) => a + (p.policy_count || 0), 0) || null], ['parties/promises', 'Promises'], ['parties/people', 'People', (S.people || []).length || null], ['parties/news', 'From the parties']],
  seats: () => [['seats/polls', 'Polls & forecast'], ['seats/map', 'Electorate map'], ['seats/parliament', 'Parliament'], ['seats/coalition', 'Coalition builder'], ['seats/calculator', 'Seat calculator'], ['seats/results', 'Results']] };
// Wrap a view's content in the section frame. Views call: sectionFrame('seats', 'seats/polls', html)
function sectionFrame(sec, current, html) { const items = (SUBNAV[sec] || (() => []))(); return `<div class="section">${items.length ? subnav(sec, items, current) : ''}<div class="section__body">${html}</div></div>` }

/* ----- routes ----- */
// Old hash / data-go value → new path. Anything already in new form passes through.
const OLD_ROUTES = { home: 'today', more: 'today', match: 'choose/quiz', swipe: 'choose/swipe', 'swipe-tally': 'choose/swipe', compass: 'choose/compass', game: 'choose/game',
  parties: 'parties', issues: 'parties/issues', policies: 'parties/policies', promises: 'parties/promises', people: 'parties/people', newsroom: 'parties/news',
  electorate: 'vote/electorate', vote: 'vote', map: 'seats/map', polls: 'seats/polls', trends: 'seats/polls', parliament: 'seats/parliament', chamber: 'seats/parliament',
  coalition: 'seats/coalition', calculator: 'seats/calculator', trust: 'about/trust', search: 'search', choose: 'choose', seats: 'seats/polls', today: 'today', results: 'seats/results' };
function normaliseRoute(r) { r = String(r || '').replace(/^#/, ''); if (r.startsWith('/')) return r.replace(/^\/+/, '').replace(/\/+$/, '') || 'today';
  if (!r) return 'today'; if (OLD_ROUTES[r]) return OLD_ROUTES[r];
  const m = r.match(/^(party|issue|electorate|newsroom)-(.+)$/); if (m) return { party: 'parties/', issue: 'parties/issues/', electorate: 'vote/electorate/', newsroom: 'parties/news/' }[m[1]] + m[2];
  return r }
// path → { sec, view, args, key }  (key is the sub-navigation item to highlight)
function resolve(path) { const seg = path.split('/'); const [a, b, ...rest] = seg; const arg = rest.join('/') || undefined;
  if (a === 'today') return { sec: 'today', view: 'home', args: [] };
  if (a === 'search') return { sec: null, view: 'search', args: [b ? decodeURIComponent(b) : ''] };
  if (a === 'about') { if (!b || b === 'trust') return { sec: null, view: 'trust', args: [] }; if (b === 'page') return { sec: null, view: 'page', args: [arg] }; if (b === 'changes') return { sec: null, view: 'changes', args: [arg] }; return { sec: null, view: 'trust', args: [] } }
  if (a === 'vote') { if (b === 'electorate') return { sec: 'vote', view: 'electorate', args: [arg], key: 'vote/electorate' };
    if (b === 'maori') return { sec: 'vote', view: 'maoriHub', args: [arg], key: 'vote/maori' };
    if (b === 'lang') return { sec: 'vote', view: 'voteLang', args: [arg], key: 'vote/lang' };
    return { sec: 'vote', view: 'vote', args: [b], key: 'vote' + (b ? '/' + b : '') } }
  if (a === 'choose') { const v = { quiz: 'match', swipe: 'swipe', compass: 'compass', game: 'game', compare: 'compare', results: 'chooseResults' }[b]; return { sec: 'choose', view: v || 'choose', args: [arg], key: 'choose' + (b ? '/' + b : '') } }
  if (a === 'parties') { if (!b) return { sec: 'parties', view: 'parties', args: [], key: 'parties' };
    if (b === 'issues') return { sec: 'parties', view: arg ? 'issue' : 'issues', args: [arg], key: 'parties/issues' };
    if (b === 'policies') return { sec: 'parties', view: 'policies', args: [arg], key: 'parties/policies' };
    if (b === 'promises') return { sec: 'parties', view: 'promises', args: [arg], key: 'parties/promises' };
    if (b === 'people') return { sec: 'parties', view: 'people', args: [arg], key: 'parties/people' };
    if (b === 'news') return { sec: 'parties', view: 'newsroom', args: [arg], key: 'parties/news' };
    return { sec: 'parties', view: 'party', args: [b, arg || 'glance'], key: 'parties' } }
  if (a === 'seats') { const sub = b || 'polls';
    if (sub === 'polls') return { sec: 'seats', view: 'polls', args: [rest[0]], key: 'seats/polls' };
    if (sub === 'map') return { sec: 'seats', view: 'map', args: [rest[0] ? +rest[0] : undefined, rest[1]], key: 'seats/map' };
    if (sub === 'parliament') return { sec: 'seats', view: 'parliament', args: ['chamber'], key: 'seats/parliament' };
    if (sub === 'coalition' || sub === 'calculator') return { sec: 'seats', view: 'parliament', args: [sub], key: 'seats/' + sub };
    if (sub === 'results') return { sec: 'seats', view: 'results', args: [], key: 'seats/results' } }
  return { sec: 'today', view: 'home', args: [] } }
// Navigate. Pushes a history entry via the hash; render() runs from the hashchange handler.
function go(r) { const path = normaliseRoute(r); if ($('#sheet').open) { const d = $('#sheet'); d.close(); if (history.state && history.state.sheet) { history.back(); setTimeout(() => { location.hash = '/' + path }, 0); return } }
  if (location.hash === '#/' + path) render(path); else location.hash = '/' + path }
const route = go;
function render(path) {
  if (S.ballotTimer) { clearInterval(S.ballotTimer); S.ballotTimer = null }
  if (S.scrubTimer) { clearInterval(S.scrubTimer); S.scrubTimer = null }
  if (S.resultsTimer) { clearInterval(S.resultsTimer); S.resultsTimer = null }
  const R = resolve(path); if (!V[R.view]) { R.view = 'home'; R.sec = 'today' }
  S.route = path; S.sec = R.sec; S.subkey = R.key; markNav(R.sec); renderPhase();
  if (document.body.classList.contains('focus-mode')) focusMode(null);
  const main = $('#main'); main.className = 'wrap page' + (R.view === 'home' ? ' page--hero' : '');
  const swap = async () => {
    if (blockedToday(R.view) || blockedToday(path.split('/').pop())) { main.innerHTML = `<div class="lock">${ic('lock')}<h2 class="h3">Hidden until 7pm</h2><p>${ELECTION_DAY_BLOCK}</p><p class="small muted">Everything else — parties, policies, candidates, your electorate, how to vote — stays available.</p><div class="row"><a class="btn btn--primary" href="https://map.vote.nz" target="_blank" rel="noopener">Find a voting place</a><a class="btn" href="#/vote/electorate">Your electorate</a></div></div>`; return }
    await V[R.view](...R.args);
    loadPeople().then(() => { if (S.route === path) main.querySelectorAll('.read, .prose, .quote, .pol p, .lede, #ctx, .mapside, .feed__t, .side, .nutshell').forEach(autolink);
      // a page never links to itself
      main.querySelectorAll('.linkbtn[data-go]').forEach(b => { if (normaliseRoute(b.dataset.go) === S.route.replace(/\/(glance|policies|record|people|history)$/, '')) b.replaceWith(document.createTextNode(b.textContent)) }) }) };
  const run = () => { window.scrollTo(0, 0); main.classList.remove('page-enter'); void main.offsetWidth; main.classList.add('page-enter'); return swap() };
  if (document.startViewTransition && !matchMedia('(prefers-reduced-motion: reduce)').matches) document.startViewTransition(run); else run();
}

/* ----- footer ----- */
function drawFooter() {
  $('#foot').innerHTML = `<div class="wrap colophon__grid">
    <div class="stack"><a class="brand" href="#/today"><svg class="brand__mark" viewBox="0 0 30 30" aria-hidden="true"><circle cx="13" cy="16" r="11"/><path d="M7.5 15.5l4.5 4.5L27 3.5"/></svg><span class="brand__word">Ballot Book</span></a>
      <p class="colophon__pledge">Independent and non-partisan. It will never tell you how to vote.</p>
      <p>Built from public sources, every figure linked. Nothing you do here leaves your device. Not the Electoral Commission: for official information on enrolling, voting places and hours, go to vote.nz or call 0800 36 76 56.</p>
      <p class="micro muted">Built ${esc(S.data.generated || '')}. Party documents, photos and other third-party material belong to their owners; owners can ask for removal or correction and we act within 24 hours during the campaign.</p></div>
    <div><h2 class="h4">Use the guide</h2><ul><li><a href="#/search">Search everything</a></li><li><a href="#/vote/glossary">Glossary of MMP terms</a></li><li><a href="#/vote/electorate">Your electorate</a></li><li><a href="#/choose/results">Your saved answers</a></li><li><a href="#/about/changes">What changed this week</a></li><li><a href="feed.xml">RSS feed</a></li></ul></div>
    <div><h2 class="h4">Trust</h2><ul><li><a href="#/about/trust">Why trust this?</a></li><li><a href="#/about/page/docs/EDITORIAL_STANDARDS.md">Editorial standards</a></li><li><a href="#/about/page/guide/quiz-research.md">How the tools work</a></li><li><a href="#/about/page/docs/REVIEW_LOG.md">Review log</a></li><li><a href="#/about/trust">Privacy &amp; contact</a></li></ul></div>
    <div><h2 class="h4">Get in touch</h2><ul><li><a href="https://github.com/not-simon/Politicsnz/issues/new?template=correction.yml" target="_blank" rel="noopener">${ic('flag', 'i--xs')} Report an error</a></li><li><a href="https://github.com/not-simon/Politicsnz" target="_blank" rel="noopener">Open data and source</a></li><li><a href="https://vote.nz" target="_blank" rel="noopener">vote.nz (official)</a></li><li>0800 36 76 56</li></ul></div>
  </div>` }

/* ----- event delegation (one listener for the whole app) ----- */
document.addEventListener('click', e => {
  const pl = e.target.closest('.linkbtn[data-person], button.lnk[data-person]'); if (pl) { openPersonByFolder(pl.dataset.person); return }
  const lc = e.target.closest('[data-locate]'); if (lc) { runLocate(lc.dataset.locate); return }
  const gob = e.target.closest('[data-go]'); if (gob) { go(gob.dataset.go); return }
  const d = e.target.closest('[data-doc]'); if (d) { const [p, path] = d.dataset.doc.split('|'); openDoc(p, path); return }
  const ip = e.target.closest('[data-issuepol]'); if (ip) { const [p, ids] = ip.dataset.issuepol.split('|'); showIssuePolicies(p, ids); return }
  const pg = e.target.closest('[data-page]'); if (pg) { openPage(pg.dataset.page); return }
  const a = e.target.closest('.prose a'); if (a) { const href = a.getAttribute('href') || '';
    if (!/^https?:|^mailto:|^#/.test(href) && /\.(md|json)(#.*)?$|\/$/.test(href)) { e.preventDefault(); const base = (a.closest('[data-base]') || {}).dataset?.base || ''; const parts = base.split('/').slice(0, -1);
      href.replace(/#.*$/, '').split('/').forEach(s => { if (s === '..') parts.pop(); else if (s && s !== '.') parts.push(s) }); let k = parts.join('/'); if (!/\.md$/.test(k)) k = k.replace(/\/?$/, '/README.md'); openPage(k) } }
  // in-app links inside the sheet: close the sheet first so the page behind changes
  const ha = e.target.closest('#sheet a[href^="#/"]'); if (ha) { e.preventDefault(); go(ha.getAttribute('href').slice(1)) }
});
document.addEventListener('keydown', e => { if (e.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName) && !$('#sheet').open) { e.preventDefault(); go('search') } });

/* ----- boot ----- */
(async () => {
  try { const t = localStorage.getItem('bb-theme'); if (t) document.documentElement.dataset.theme = t } catch {}
  document.body.classList.add('has-tabbar'); bindTheme(); bindSearch(); drawNav();
  try { S.data = await getJSON('data/bundle.json') } catch (e) { $('#main').innerHTML = `<p class="empty">The guide's data didn't load (${esc(e.message)}).</p>`; return }
  drawFooter();
  const start = normaliseRoute(location.hash);
  window.addEventListener('hashchange', () => { const p = normaliseRoute(location.hash); if (location.hash !== '#/' + p) { history.replaceState(null, '', '#/' + p); } if (p !== S.route) render(p) });
  if (location.hash !== '#/' + start) history.replaceState(null, '', '#/' + start);
  render(start);
  loadPeople().then(() => { if (['today', 'parties'].includes(S.route)) render(S.route) });
})();
})();
