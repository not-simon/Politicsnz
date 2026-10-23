/* ----- people ----- */
V.people = async () => { await loadPeople();
  $('#main').innerHTML = `<section class="view"><div class="stack"><div class="kicker">${S.people.length} people</div><h2>MPs, former MPs and 2026 candidates</h2><p class="lede">Everyone who has sat in Parliament since 2011, and everyone standing in 2026. Tap a person for their profile and what they're doing now.</p></div><div id="pg"></div></section>`;
  peopleGrid($('#pg')) };
function peopleGrid(el, { party = '' } = {}) {
  const parties = [...new Set(S.people.map(p => p.party))].sort((a, b) => P(a).order - P(b).order);
  el.innerHTML = `<div class="stack" style="gap:14px"><div class="toolbar"><input type="search" id="pq" placeholder="Search name or electorate" aria-label="Search people">
    ${party ? '' : `<select id="pp" aria-label="Party"><option value="">All parties</option>${parties.map(p => `<option value="${p}">${esc(pname(p))}</option>`).join('')}</select>`}
    <select id="ps" aria-label="Status"><option value="">Everyone</option><option value="mp">Current MPs</option><option value="candidate-2026">New candidates</option><option value="former-mp">Former MPs</option></select></div><div id="plist2"></div></div>`;
  let limit = 120;
  const draw = () => { const q = $('#pq', el).value.trim().toLowerCase(), pa = party || ($('#pp', el) || {}).value, st = $('#ps', el).value;
    const list = S.people.filter(p => (!pa || p.party === pa) && (!st || (st === 'mp' ? isMP(p.status) : p.status === st)) && (!q || (p.name + ' ' + (p.electorate_2026 || '')).toLowerCase().includes(q)))
      .sort((a, b) => (isMP(b.status) - isMP(a.status)) || (P(a.party).order - P(b.party).order) || ((a.list_rank_2026 || 999) - (b.list_rank_2026 || 999)) || a.name.localeCompare(b.name));
    $('#plist2', el).innerHTML = `<p class="small muted">${list.length} people</p><div class="people">${list.slice(0, limit).map(p => `<button class="person" data-i="${S.people.indexOf(p)}">${faceHTML(p, p.party)}<span class="nm">${esc(p.name)}</span>
      <span class="row tiny muted" style="gap:5px;justify-content:center"><span class="dot" style="background:${pcolor(p.party)}"></span>${esc(pname(p.party))}</span><span class="status ${isMP(p.status) ? 'mp' : ''}">${esc(STATUS[p.status] || p.status || '')}</span>${p.list_rank_2026 ? `<span class="tiny muted">List #${p.list_rank_2026}</span>` : ''}</button>`).join('')}</div>
      ${list.length > limit ? `<div class="row" style="justify-content:center;margin-top:12px"><button class="btn primary" id="pmore">Show more</button></div>` : ''}`;
    const m = $('#pmore', el); if (m) m.onclick = () => { limit += 120; draw() } };
  el.querySelectorAll('input,select').forEach(x => x.addEventListener('input', () => { limit = 120; draw() }));
  el.addEventListener('click', e => { const b = e.target.closest('[data-i]'); if (b) openPerson(S.people[+b.dataset.i]) });
  draw() }
