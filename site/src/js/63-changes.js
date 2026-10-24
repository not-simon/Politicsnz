/* ----- What changed this week (#/about/changes): data/changes.json, written daily by tools/changelog.py -----
   Grouped by day, newest first; this week open, older weeks behind a disclosure. Filters by kind and by party (A–Z).
   Every party's changes are shown the same way. On election day (before 7pm) poll and party-release entries are hidden,
   as the polls page and newsroom are. */
const CHG_KINDS = [['policy-added', 'New policies'], ['policy-changed', 'Policy updates'], ['policy-withdrawn', 'Withdrawn policies'],
  ['candidate-added', 'New candidates'], ['candidate-changed', 'Candidate updates'], ['poll-added', 'Polls'], ['release', 'Party releases'], ['site', 'This site']];
const CHG_LABEL = { 'policy-added': 'New policy', 'policy-changed': 'Policy updated', 'policy-withdrawn': 'Policy withdrawn', 'candidate-added': 'New candidate',
  'candidate-changed': 'Candidate update', 'poll-added': 'New poll', release: 'Press release', site: 'Site' };
const CHG_HIDDEN_TODAY = ['poll-added', 'release'];
const chgDayN = iso => { const [y, m, d] = String(iso).slice(0, 10).split('-').map(Number); return Math.round(Date.UTC(y, m - 1, d) / 864e5) };
const chgDay = iso => new Date(chgDayN(iso) * 864e5).toLocaleDateString('en-NZ', { weekday: 'long', day: 'numeric', month: 'long', timeZone: 'UTC' });
const chgShort = n => new Date(n * 864e5).toLocaleDateString('en-NZ', { day: 'numeric', month: 'short', timeZone: 'UTC' });
const chgHref = u => /^#\/[\w\-/%.]*$/.test(String(u || '')) ? u : '#/about/changes';
const chgExt = u => /^https?:\/\//.test(String(u || '')) ? u : '';

function chgRow(e) {
  const t = e.kind === 'poll-added' ? `${e.title}, fieldwork to ${shortDate(e.poll_date || e.date)}` : e.title;
  const showSum = e.summary && !['policy-added', 'release', 'site'].includes(e.kind);
  const src = e.kind === 'site' ? '' : chgExt(e.source);
  return `<div class="release"><a class="release__t" href="${esc(chgHref(e.url))}">${esc(t)}</a>
    <span class="release__m"><span class="badge">${esc(CHG_LABEL[e.kind] || e.kind)}</span>${e.party ? ptTag(e.party) : ''}${showSum ? `<span>${esc(e.summary.length > 160 ? e.summary.slice(0, 157).replace(/\s+\S*$/, '') + '…' : e.summary)}</span>` : ''}${src ? `<a href="${esc(src)}" target="_blank" rel="noopener nofollow">${ic('ext', 'i--xs')} ${esc(e.kind === 'release' && e.via ? 'via ' + e.via : ptHost(src) || 'source')}</a>` : ''}</span></div>` }

function chgDays(list) { const by = new Map(); for (const e of list) { const d = String(e.date).slice(0, 10); if (!by.has(d)) by.set(d, []); by.get(d).push(e) }
  return [...by.entries()].sort((a, b) => b[0].localeCompare(a[0])).map(([d, L]) => `<section class="stack stack--s" aria-label="${esc(chgDay(d))}"><div class="shead shead--quiet"><div class="shead__row"><h3 class="h4">${esc(chgDay(d))}</h3><span class="micro muted">${L.length} change${L.length === 1 ? '' : 's'}</span></div></div><div>${L.map(chgRow).join('')}</div></section>`).join('') }

V.changes = async arg => {
  if (!S.changes) S.changes = await getJSON('data/changes.json').catch(() => null);
  const C = S.changes;
  const head = `<header class="pagehead"><p class="eyebrow">About this guide</p><h1>What changed this week</h1>
    <p class="lede">New and changed 2026 policies and candidates on policy.nz, new polls and party press releases, newest first. Every entry links to its source. Checked daily.</p></header>`;
  if (!C || !Array.isArray(C.entries)) { $('#main').innerHTML = `<div class="stack stack--xl" style="max-width:980px">${head}<p class="muted">The change log isn’t available in this build.</p></div>`; return }
  const eday = electionPhase() === 'electionday';
  const all = C.entries.filter(e => e && e.date && e.kind && !(eday && CHG_HIDDEN_TODAY.includes(e.kind)));
  const kinds = CHG_KINDS.filter(([k]) => all.some(e => e.kind === k));
  const parties = [...new Set(all.map(e => e.party).filter(Boolean))].sort((a, b) => ptCmp(pname(a), pname(b)) || ptCmp(a, b));
  const st = S.chgFilter || (S.chgFilter = { kind: 'all', party: 'all' });
  if (arg) { if (kinds.some(([k]) => k === arg)) { st.kind = arg; st.party = 'all' } else if (parties.includes(arg)) { st.party = arg; st.kind = 'all' } }
  if (st.kind !== 'all' && !kinds.some(([k]) => k === st.kind)) st.kind = 'all';
  if (st.party !== 'all' && !parties.includes(st.party)) st.party = 'all';
  const t = nzToday();
  const draw = () => {
    const list = all.filter(e => (st.kind === 'all' || e.kind === st.kind) && (st.party === 'all' || e.party === st.party));
    const nk = k => all.filter(e => e.kind === k && (st.party === 'all' || e.party === st.party)).length;
    const weeks = new Map();
    for (const e of list) { const w = Math.max(0, Math.floor((t.n - chgDayN(e.date)) / 7)); if (!weeks.has(w)) weeks.set(w, []); weeks.get(w).push(e) }
    const thisWeek = weeks.get(0) || [];
    const older = [...weeks.entries()].filter(([w]) => w > 0).sort((a, b) => a[0] - b[0]);
    const span = w => `${chgShort(t.n - w * 7 - 6)} – ${chgShort(t.n - w * 7)}`;
    $('#chg-body').innerHTML = `
      <div class="stack stack--s">
        <div class="chips chips--scroll chg-kinds" role="group" aria-label="Kind of change">${[['all', 'Everything', all.filter(e => st.party === 'all' || e.party === st.party).length], ...kinds.map(([k, l]) => [k, l, nk(k)])].map(([k, l, n]) => `<button class="chip" type="button" data-chgk="${esc(k)}" aria-pressed="${k === st.kind}">${esc(l)} <span class="count">${n}</span></button>`).join('')}</div>
        ${parties.length ? `<div class="chips chips--scroll chg-parties" role="group" aria-label="Party (A to Z)">${[['all', 'All parties'], ...parties.map(p => [p, pname(p)])].map(([k, l]) => `<button class="chip" type="button" data-chgp="${esc(k)}" aria-pressed="${k === st.party}">${k !== 'all' ? `<span class="sw" style="--pc:${pcolor(k)}"></span>` : ''}${esc(l)}</button>`).join('')}</div>` : ''}
      </div>
      ${thisWeek.length ? chgDays(thisWeek) : `<p class="small muted">${list.length ? 'Nothing matching in the last 7 days. Earlier changes are below.' : 'Nothing matching in the last ' + esc(C.window_days || 60) + ' days.'}</p>`}
      ${older.length ? `<div>${older.map(([w, L]) => `<details class="disclose"><summary>Earlier: ${esc(span(w))} <span class="micro muted" style="margin-left:auto">${L.length} change${L.length === 1 ? '' : 's'}</span></summary><div class="disclose__body">${chgDays(L)}</div></details>`).join('')}</div>` : ''}`;
    $('#chg-body').querySelectorAll('[data-chgk]').forEach(b => b.onclick = () => { st.kind = b.dataset.chgk; draw() });
    $('#chg-body').querySelectorAll('[data-chgp]').forEach(b => b.onclick = () => { st.party = b.dataset.chgp; draw() });
    ptScrollChips($('#chg-body .chg-kinds')); ptScrollChips($('#chg-body .chg-parties')) };
  const checked = C.policy_nz_checked ? new Date(C.policy_nz_checked) : null;
  const when = checked && !isNaN(checked) ? checked.toLocaleString('en-NZ', { day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit', timeZone: 'Pacific/Auckland' }) : '';
  $('#main').innerHTML = `<div class="stack stack--xl" style="max-width:980px">${head}
    ${eday ? `<div class="note">${ic('lock')}<div><b>Election day.</b> Poll and party-release entries are hidden until voting closes at 7pm. Policy and candidate changes stay listed.</div></div>` : ''}
    <div class="split split--8-4"><div class="stack stack--l" id="chg-body"></div>
      <aside class="stack sticky"><div class="note">${ic('info')}<div><b>Same treatment for every party.</b> Changes are listed as they happen, newest first, and filtered A to Z. Nothing here is a ranking or a recommendation.</div></div>
        <p class="small">A policy taken down from policy.nz is never deleted here: it stays on the party’s policy list, marked withdrawn. Party releases are headlines only and link to the original.</p>
        <p class="micro muted">${when ? `policy.nz last checked ${esc(when)}${C.policy_nz_failures ? ` (${esc(C.policy_nz_failures)} page${C.policy_nz_failures === 1 ? '' : 's'} could not be read; the previous copy was kept)` : ''} · ` : ''}last ${esc(C.window_days || 60)} days · polls from <a href="#/seats/polls">Polls</a> · releases from <a href="#/parties/news">From the parties</a></p>
        <p class="small"><a href="feed.xml">${ic('news', 'i--xs')} RSS feed</a> <span class="micro muted">the latest 50 changes</span></p>
        <p class="micro muted">Something wrong or missing? <a href="${CORRECTION_URL}" target="_blank" rel="noopener">Ask for a correction</a></p></aside></div></div>`;
  draw();
};
