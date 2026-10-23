/* ----- global search: typed results (party, person, policy, electorate, issue, page) ----- */
const fold = s => String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
async function searchIndex() {
  if (S.searchIdx) return S.searchIdx;
  await loadPeople(); if (!S.policies) S.policies = await getJSON('data/policies.json').catch(() => ({})); await loadPages();
  const idx = [];
  for (const g of (G().parties || [])) idx.push({ kind: 'Party', title: g.name, sub: g.tagline || '', go: 'parties/' + g.slug, pc: pcolor(g.slug), key: fold(g.name + ' ' + (g.short_name || '') + ' ' + pname(g.slug)) });
  for (const p of (S.people || [])) idx.push({ kind: 'Person', title: p.name, sub: [pname(p.party), p.electorate_2026 ? p.electorate_2026 : '', STATUS[p.status] || ''].filter(Boolean).join(' · '), person: p.folder, pc: pcolor(p.party), key: fold(p.name) });
  for (const [party, list] of Object.entries(S.policies || {})) for (const x of list) idx.push({ kind: 'Policy', title: x.statement, sub: pname(party) + (x.topic_group ? ' · ' + (TOPIC_NAMES[x.topic_group] || x.topic_group) : ''), go: `parties/${party}/policies`, pc: pcolor(party), key: fold(x.statement + ' ' + (x.summary && x.summary.why || '')) });
  for (const e of (S.data.electorates || [])) idx.push({ kind: 'Electorate', title: e.name, sub: (e.type === 'maori' ? 'Māori electorate' : 'General electorate') + (e.region ? ' · ' + e.region : ''), go: 'vote/electorate/' + e.slug, key: fold(e.name + ' ' + (e.region || '')) });
  for (const i of (G().issues || [])) idx.push({ kind: 'Issue', title: i.title, sub: i.why_it_matters || '', go: 'parties/issues/' + i.slug, key: fold(i.title + ' ' + (i.why_it_matters || '')) });
  for (const k of Object.keys(S.pages || {})) if (!/\/people\//.test(k)) idx.push({ kind: 'Page', title: pageTitle(k), sub: k, go: 'about/page/' + k, key: fold(pageTitle(k) + ' ' + k) });
  return (S.searchIdx = idx) }
function searchRun(idx, q) { const terms = fold(q).split(/\s+/).filter(t => t.length > 1); if (!terms.length) return [];
  const scored = []; for (const it of idx) { let s = 0; for (const t of terms) { const i = it.key.indexOf(t); if (i < 0) { s = -1; break } s += i === 0 || it.key[i - 1] === ' ' ? 3 : 1 } if (s > 0) scored.push([s + (it.kind === 'Party' ? 2 : it.kind === 'Person' || it.kind === 'Electorate' ? 1 : 0), it]) }
  return scored.sort((a, b) => b[0] - a[0] || a[1].title.localeCompare(b[1].title)).slice(0, 60).map(x => x[1]) }
V.search = async q => {
  $('#main').innerHTML = `<div class="stack stack--l" style="max-width:820px"><header class="pagehead"><p class="eyebrow">Search</p><h1>Search the guide</h1><p class="lede">Parties, people, policies, electorates, issues and pages. Results are listed by how well they match, then A–Z.</p></header>
    <div class="input-icon">${ic('search', 'i--s')}<input class="input" id="sq" type="search" value="${esc(q || '')}" placeholder="Try a name, a place or a policy word" aria-label="Search" autocomplete="off"></div>
    <div id="sres" class="rows" aria-live="polite"></div></div>`;
  const idx = await searchIndex(); const out = $('#sres'); const inp = $('#sq');
  const draw = () => { const v = inp.value.trim(); try { history.replaceState(null, '', '#/search/' + encodeURIComponent(v)) } catch {}
    const rs = searchRun(idx, v); if (!v) { out.innerHTML = `<p class="small muted">Type to search. Press <kbd>/</kbd> anywhere to come back here.</p>`; return }
    if (!rs.length) { out.innerHTML = `<p class="empty">Nothing matched “${esc(v)}”. Try fewer or different words.</p>`; return }
    const groups = {}; rs.forEach(r => (groups[r.kind] = groups[r.kind] || []).push(r));
    out.innerHTML = Object.entries(groups).map(([k, L]) => `<div class="shead shead--quiet"><div class="shead__row"><h2 class="h4">${esc(k === 'Person' ? 'People' : k === 'Policy' ? 'Policies' : k === 'Party' ? 'Parties' : k + 's')}</h2><span class="small muted">${L.length}</span></div></div>` +
      L.map(r => `<a class="rowlink" href="${r.go ? '#/' + esc(r.go) : '#'}"${r.person ? ` data-person="${esc(r.person)}"` : ''}>${r.pc ? `<span class="sw" style="--pc:${r.pc}"></span>` : ''}<span><span class="rowlink__title">${esc(r.title)}</span>${r.sub ? `<span class="rowlink__sub">${esc(r.sub)}</span>` : ''}</span>${ic('chev', 'i--s')}</a>`).join('')).join('') };
  inp.oninput = draw; draw(); if (!q) inp.focus();
  out.onclick = e => { const a = e.target.closest('a[data-person]'); if (a) { e.preventDefault(); openPersonByFolder(a.dataset.person) } } };
