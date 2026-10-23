/* ----- electorate ----- */
V.electorate = async slug => {
  await loadPeople(); const E = (S.data.electorates || []).slice().sort((a, b) => a.name.localeCompare(b.name));
  const sel = slug || store.get('myElectorate') || '';
  $('#main').innerHTML = `<section class="view"><div class="stack"><div class="kicker">Your local vote</div><h2>Who's standing where you live</h2>
    <p class="lede">Choose your electorate to meet the candidates. Not sure which one you're in? Look up your address at vote.nz.</p>${NOT_EC}</div>
    ${locateBlock('loc-el')}
    <div class="toolbar"><select id="esel" aria-label="Electorate"><option value="">Choose your electorate…</option>
      ${['general', 'maori'].map(t => `<optgroup label="${t === 'maori' ? 'Māori electorates' : 'General electorates'}">${E.filter(e => (e.type || 'general') === t).map(e => `<option value="${esc(e.slug)}" ${e.slug === sel ? 'selected' : ''}>${esc(e.name)}</option>`).join('')}</optgroup>`).join('')}</select></div>
    <div id="ebody"></div></section>`;
  const draw = () => { const v = $('#esel').value; store.set('myElectorate', v); const e = E.find(x => x.slug === v); const b = $('#ebody');
    if (!e) { b.innerHTML = E.length ? (isElectionDay() ? `<div class="grid">${E.map(x => `<button class="starter" style="padding:14px" data-elec="${esc(x.slug)}"><h4>${esc(x.name)}</h4></button>`).join('')}</div>` : `<div class="grid">${E.filter(x => x.marginal).slice(0, 9).map(x => `<button class="starter" data-elec="${esc(x.slug)}"><div class="kicker">Battleground</div><h3>${esc(x.name)}</h3><p class="small muted">${esc(x.contest_notes || '')}</p></button>`).join('')}</div>`) : '<p class="empty">Electorate guides are still being built.</p>'; return }
    const r = e.result_2023 || {};
    b.innerHTML = `<div class="split"><div class="stack" style="gap:16px"><div class="card stack"><h2>${esc(e.name)}</h2>${e.description ? `<p class="read">${esc(e.description)}</p><p class="tiny muted">Description from policy.nz.</p>` : ''}
        ${(e.description_fact_check || []).length ? `<details class="small"><summary style="cursor:pointer;color:var(--primary);font-weight:700">Fact-check notes on this description (${e.description_fact_check.length})</summary><ul>${e.description_fact_check.map(f => `<li>${esc(typeof f === 'string' ? f : (f.note || f.correction || f.text || JSON.stringify(f)))}</li>`).join('')}</ul></details>` : ''}
        ${e.contest_notes && !isElectionDay() ? `<p class="note">${esc(e.contest_notes)}</p>` : ''}</div>
      <div class="stack"><h3>${(e.candidates || []).length} candidates</h3><div class="people">${(e.candidates || []).map(c => { const p = findPerson(c.slug, c.name) || { name: c.name, party: c.party };
        return `<button class="person" data-person="${esc(c.slug)}">${faceHTML(p, c.party)}<span class="nm">${esc(c.name)}</span><span class="row tiny muted" style="gap:5px;justify-content:center"><span class="dot" style="background:${pcolor(c.party)}"></span>${esc(pname(c.party))}</span>${isMP(p.status) ? '<span class="status mp">Sitting MP</span>' : ''}</button>` }).join('')}</div></div></div>
      <div class="stack" style="gap:16px">${e.sitting_mp ? `<div class="card stack"><h3>Current MP</h3><p>${esc(e.sitting_mp.name)} (${esc(pname(e.sitting_mp.party))})${e.mp_standing_again === false ? ' is not standing again.' : ''}</p></div>` : ''}
        ${r.winner ? `<div class="card stack"><h3>Last time (2023)</h3><p class="small">${esc(r.winner)} (${esc(pname(r.party))}) won${r.majority ? ` by <b class="num">${Number(r.majority).toLocaleString('en-NZ')}</b> votes` : ''}${r.runner_up ? ` over ${esc(r.runner_up)} (${esc(pname(r.runner_up_party))})` : ''}.</p>
          ${r.party_vote_pct ? '<p class="tiny muted">Party vote in this area</p>' : ''}${r.party_vote_pct ? Object.entries(r.party_vote_pct).sort((a, b) => b[1] - a[1]).slice(0, 6).map(([p, v]) => `<div class="row" style="flex-wrap:nowrap"><span class="small" style="width:110px">${esc(pname(p))}</span><div class="meter" style="flex:1"><span style="width:${v}%;background:${pcolor(p)}"></span></div><span class="num tiny" style="width:44px;text-align:right">${fmt(v)}%</span></div>`).join('') : ''}
          ${r.for_predecessor_seat || (e.predecessor_seats || []).some(x => x !== e.name) ? `<p class="tiny muted">Based on ${esc((e.predecessor_seats || []).join(', ') || r.seat || '')} before the 2025 boundary changes.</p>` : ''}</div>` : ''}
        <button class="btn sm" data-page="electorates/${esc(e.slug)}.md" style="justify-self:start">Full electorate guide</button></div></div>`;
    b.querySelectorAll('[data-person]').forEach(x => x.onclick = () => { const p = findPerson(x.dataset.person); if (p) openPerson(p) }) };
  $('#esel').onchange = draw;
  $('#ebody').addEventListener('click', e => { const b = e.target.closest('[data-elec]'); if (b) { $('#esel').value = b.dataset.elec; draw() } });
  draw();
};
