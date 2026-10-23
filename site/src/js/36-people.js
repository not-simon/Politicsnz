/* ----- people: everyone A to Z by surname, same fields and same photo crop for everyone ----- */
const PEOPLE_FILTERS = [['', 'Everyone'], ['current-mp-standing-2026', 'MP · standing'], ['current-mp-retiring', 'MP · retiring'], ['candidate-2026', 'Candidate'], ['former-mp', 'Former MP']];
// #/parties/people            everyone
// #/parties/people/<party>    preset party filter
// #/parties/people/<slug>     open that person's sheet on top of the list
V.people = async arg => { await loadPeople();
  const isParty = arg && S.people.some(p => p.party === arg); const person = arg && !isParty ? S.people.find(p => p.slug === arg) : null;
  $('#main').innerHTML = sectionFrame('parties', 'parties/people', `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('users', 'i--s')} Parties · People</p><h1>${S.people.length.toLocaleString('en-NZ')} people</h1>
    <p class="lede">Every MP since 2011 and every 2026 candidate. Same-size photos, same fields for everyone, A to Z by surname.</p></header><div id="pg"></div>`);
  peopleGrid($('#pg'), { preset: isParty ? arg : '' });
  if (person) openPerson(person) };

// `party` fixes the party (party People tab, no party picker); `preset` only preselects it.
function peopleGrid(el, { party = '', preset = '' } = {}) {
  const f = { q: '', st: '', party: party || preset, elect: '' }; let limit = 120;
  const base = () => S.people.filter(p => (!f.party || p.party === f.party) && (!f.elect || p.electorate_2026 === f.elect) && (!f.q || [p.name, p.electorate_2026, STATUS[p.status], p.status_detail, ...(p.roles || []).map(r => typeof r === 'string' ? r : r.role || r.title)].join(' ').toLowerCase().includes(f.q)));
  const matchSt = p => !f.st || p.status === f.st;
  el.innerHTML = `<div class="stack stack--l"><div class="toolbar">
      <div class="input-icon">${ic('search', 'i--s')}<input class="input" type="search" id="pq" placeholder="Name, electorate or role" aria-label="Search people"></div>
      <div class="chips chips--scroll" id="pfilt" role="group" aria-label="Filter people"></div></div>
    <nav class="alpha" id="palpha" aria-label="Jump to letter"></nav>
    <div id="plist2"></div>
    <div class="note">${ic('info')}<div>Photos come from candidates and parties (via policy.nz), Parliament or Wikimedia Commons, and are cropped the same way for everyone. Where none was supplied we show initials, never a stand-in photo. Home addresses and personal emails are never shown. <a href="#/about/page/docs/EDITORIAL_STANDARDS.md">How profiles are written and corrected</a></div></div></div>`;
  const draw = () => {
    const B = base(); const list = B.filter(matchSt).sort(ptBySurname);
    $('#pfilt', el).innerHTML = PEOPLE_FILTERS.map(([k, l]) => `<button class="chip" type="button" data-st="${k}" aria-pressed="${f.st === k}">${esc(l)} <span class="count">${(k ? B.filter(p => p.status === k) : B).length}</span></button>`).join('')
      + (party ? '' : `<button class="chip chip--menu" type="button" data-menu="party" aria-pressed="${!!f.party}" aria-haspopup="dialog">${f.party ? `<span class="sw" style="--pc:${pcolor(f.party)}"></span>${esc(pname(f.party))}` : 'Any party'}</button>`)
      + `<button class="chip chip--menu" type="button" data-menu="elect" aria-pressed="${!!f.elect}" aria-haspopup="dialog">${f.elect ? esc(f.elect) : 'Any electorate'}</button>`;
    const shown = list.slice(0, limit); const letters = new Set(list.map(ptLetter)); let last = '';
    $('#palpha', el).innerHTML = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map(c => letters.has(c) ? `<a href="#/parties/people" data-letter="${c}">${c}</a>` : `<span aria-hidden="true">${c}</span>`).join('');
    $('#plist2', el).innerHTML = list.length ? `<div class="people">${shown.map(p => { const L = ptLetter(p); const h = L !== last ? `<h2 class="letter" id="pl-${L}">${L}</h2>` : ''; last = L;
        const where = [p.electorate_2026 ? esc(p.electorate_2026) : (p.list_rank_2026 ? 'List only' : ''), p.list_rank_2026 ? `list #${esc(p.list_rank_2026)}` : ''].filter(Boolean).join(' · ');
        return `${h}<a class="person" href="#/parties/people/${esc(p.slug)}" data-i="${S.people.indexOf(p)}">${faceHTML(p, p.party)}<span><span class="person__name">${esc(p.name)}</span><span class="person__meta">${ptTag(p.party)}<span class="badge${isMP(p.status) ? ' badge--ink' : ''}">${esc(STATUS[p.status] || p.status || '')}</span>${where ? `<span>${where}</span>` : ''}</span></span></a>` }).join('')}</div>
      <div class="row" style="margin-top:var(--s-5)">${list.length > limit ? `<button class="btn" type="button" id="pmore">Show the next ${Math.min(120, list.length - limit)}</button>` : ''}<span class="small muted">${Math.min(limit, list.length)} of ${list.length} shown, A to Z by surname</span></div>`
      : '<p class="muted">Nobody matches. Try a different spelling or clear a filter.</p>';
    const m = $('#pmore', el); if (m) m.onclick = () => { limit += 120; draw() } };
  // Party / electorate picker: a chip that opens a sheet of options (no <select>).
  const menu = kind => { const B = S.people.filter(p => (kind === 'party' || !f.party || p.party === f.party) && (kind === 'elect' ? !!p.electorate_2026 : true) && (kind === 'party' ? (!f.elect || p.electorate_2026 === f.elect) : true));
    const counts = {}; B.forEach(p => { const k = kind === 'party' ? p.party : p.electorate_2026; counts[k] = (counts[k] || 0) + 1 });
    const keys = Object.keys(counts).sort((a, b) => kind === 'party' ? ptCmp(pname(a), pname(b)) : ptCmp(a, b)); const cur = kind === 'party' ? f.party : f.elect;
    openSheet({ title: kind === 'party' ? 'Choose a party' : 'Choose an electorate', html: `<div class="rows">${[['', kind === 'party' ? 'Any party' : 'Any electorate', B.length], ...keys.map(k => [k, kind === 'party' ? pname(k) : k, counts[k]])].map(([k, l, n]) => `<button class="rowlink rowlink--plain pick-row" type="button" data-pick="${esc(k)}"${k === cur ? ' aria-current="true"' : ''}><span class="row row--nowrap" style="gap:10px">${kind === 'party' && k ? `<span class="sw" style="--pc:${pcolor(k)}"></span>` : ''}<span class="rowlink__title" style="font-size:16px">${esc(l)}</span></span><span class="small muted">${n}${k === cur ? ' ' + ic('check', 'i--xs') : ''}</span></button>`).join('')}</div>` });
    $('#sheet-body').querySelectorAll('[data-pick]').forEach(b => b.onclick = () => { if (kind === 'party') f.party = b.dataset.pick; else f.elect = b.dataset.pick; limit = 120; closeSheet(); draw() }) };
  $('#pq', el).oninput = e => { f.q = e.target.value.trim().toLowerCase(); limit = 120; draw() };
  el.addEventListener('click', e => {
    const st = e.target.closest('[data-st]'); if (st) { f.st = st.dataset.st; limit = 120; draw(); return }
    const mn = e.target.closest('[data-menu]'); if (mn) { menu(mn.dataset.menu); return }
    const lt = e.target.closest('[data-letter]'); if (lt) { e.preventDefault(); limit = Infinity; draw(); const h = $('#pl-' + lt.dataset.letter, el); if (h) h.scrollIntoView({ block: 'start', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }); return }
    const b = e.target.closest('a.person[data-i]'); if (b && !e.metaKey && !e.ctrlKey && !e.shiftKey) { e.preventDefault(); openPerson(S.people[+b.dataset.i]) } });
  draw() }
