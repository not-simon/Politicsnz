/* ===== shell ===== */
function openDialog(title, html) { $('#dlg-title').textContent = title; $('#dlg-body').innerHTML = html; const d = $('#dlg'); if (!d.open) d.showModal(); $('#dlg-body').scrollTop = 0; d.scrollTop = 0; loadPeople().then(() => autolink($('#dlg-body'))) }
async function openPersonByFolder(folder) { await loadPeople(); const p = S.people.find(x => x.folder === folder); if (p) openPerson(p) }
$('#dlg-close').onclick = () => $('#dlg').close();
$('#dlg').addEventListener('click', e => { if (e.target === $('#dlg')) $('#dlg').close() });
document.addEventListener('click', e => {
  const pl = e.target.closest('button.lnk[data-person]'); if (pl) { openPersonByFolder(pl.dataset.person); return }
  const lc = e.target.closest('[data-locate]'); if (lc) { runLocate(lc.dataset.locate); return }
  const go = e.target.closest('[data-go]'); if (go) { if ($('#dlg').open) $('#dlg').close(); route(go.dataset.go); return }
  const d = e.target.closest('[data-doc]'); if (d) { const [p, path] = d.dataset.doc.split('|'); openDoc(p, path); return }
  const ip = e.target.closest('[data-issuepol]'); if (ip) { const [p, ids] = ip.dataset.issuepol.split('|'); showIssuePolicies(p, ids); return }
  const pg = e.target.closest('[data-page]'); if (pg) { openPage(pg.dataset.page); return }
  const a = e.target.closest('.prose a'); if (a) { const href = a.getAttribute('href') || '';
    if (!/^https?:|^mailto:/.test(href) && /\.(md|json)(#.*)?$|\/$/.test(href)) { e.preventDefault(); const base = (a.closest('[data-base]') || {}).dataset?.base || ''; const parts = base.split('/').slice(0, -1);
      href.replace(/#.*$/, '').split('/').forEach(s => { if (s === '..') parts.pop(); else if (s && s !== '.') parts.push(s) }); let k = parts.join('/'); if (!/\.md$/.test(k)) k = k.replace(/\/?$/, '/README.md'); openPage(k) } }
});
function route(r) {
  if (S.ballotTimer) { clearInterval(S.ballotTimer); S.ballotTimer = null }
  r = r || 'home'; let view = r, arg;
  for (const pre of ['party', 'issue', 'electorate', 'newsroom']) if (r.startsWith(pre + '-')) { view = pre; arg = r.slice(pre.length + 1) }
  if (['chamber', 'trends', 'coalition', 'calculator'].includes(r)) { view = 'parliament'; arg = r }
  if (!V[view]) { view = 'home'; r = 'home' }
  renderBanner();
  if (blockedToday(view) || blockedToday(r)) { document.querySelectorAll('#nav button, #bnav button').forEach(b => b.setAttribute('aria-current', 'false')); S.route = r; window.scrollTo(0, 0); $('#main').innerHTML = `<section class="view"><div class="card stack"><h2>Hidden until 7pm</h2><p>${ELECTION_DAY_BLOCK}</p><p class="small muted">Everything else — parties, policies, candidates, your electorate, how to vote — stays available.</p><div class="row"><button class="btn primary" data-go="electorate">Your electorate</button><button class="btn" data-go="parties">Parties</button></div></div></section>`; return }
  const navKey = { party: 'parties', issue: 'issues', 'swipe-tally': 'swipe', electorate: 'map', newsroom: 'more', polls: 'more', trends: 'more', policies: 'more', people: 'more', promises: 'more' }[view] || view;
  document.querySelectorAll('#nav button, #bnav button').forEach(b => b.setAttribute('aria-current', b.dataset.go === navKey ? 'page' : 'false'));
  S.route = r; try { history.replaceState(null, '', '#' + r) } catch {}
  window.scrollTo(0, 0); Promise.resolve(V[view](arg)).then(() => loadPeople().then(() => { if (S.route === r) $('#main').querySelectorAll('.read, .quote, .pol p, .lede, #ctx, .mapside').forEach(autolink) }));
}
(async () => {
  try { const t = localStorage.getItem('bb-theme'); if (t) document.documentElement.dataset.theme = t } catch {}
  $('#themebtn').onclick = () => { const r = document.documentElement; const dark = r.dataset.theme === 'dark' || (!r.dataset.theme && matchMedia('(prefers-color-scheme: dark)').matches); r.dataset.theme = dark ? 'light' : 'dark'; try { localStorage.setItem('bb-theme', r.dataset.theme) } catch {} };
  $('#nav').innerHTML = NAV.map(([k, l]) => `<button data-go="${k}">${l}</button>`).join('');
  $('#bnav').innerHTML = [['home', 'Home'], ['vote', 'Vote'], ['match', 'Match'], ['swipe', 'Swipe'], ['parties', 'Parties'], ['more', 'More']].map(([k, l]) => `<button data-go="${k}">${ic(k)}<span>${l}</span></button>`).join('');
  try { S.data = await getJSON('data/bundle.json') } catch (e) { $('#main').innerHTML = `<p class="empty">The guide's data didn't load (${esc(e.message)}).</p>`; return }
  loadPeople().then(() => { if ((location.hash || '#home') === '#home' || !location.hash) { /* refresh faces on home */ const h = location.hash.slice(1) || 'home'; if (['home', 'parties'].includes(h)) route(h) } });
  $('#foot').innerHTML = `<p><b>Ballot Book NZ</b> is an independent, non-partisan guide. It does not tell you how to vote. Built ${esc(S.data.generated)}. <button class="btn ghost sm" data-go="trust">Why trust this?</button> <button class="btn ghost sm" data-page="docs/EDITORIAL_STANDARDS.md">Standards</button> <button class="btn ghost sm" data-go="trust">Privacy &amp; contact</button> <a class="btn ghost sm" href="https://github.com/not-simon/Politicsnz/issues/new?template=correction.yml" target="_blank" rel="noopener">Report an error</a> <a class="btn ghost sm" href="https://vote.nz" target="_blank" rel="noopener">Enrol / find a voting place</a></p><p class="tiny muted">Not the Electoral Commission. For official information on enrolling, voting places and hours, go to vote.nz or call 0800 36 76 56. Party documents, photos and other third-party material belong to their owners; owners can ask for removal or correction and we act within 24 hours during the campaign.</p>`;
  window.addEventListener('hashchange', () => { const h = location.hash.slice(1); if (h && h !== S.route) route(h) });
  route((location.hash || '').slice(1) || 'home');
})();
})();
