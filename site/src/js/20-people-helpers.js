/* ===== people helpers (shared: people list, party People tab, electorate candidates, parliament seat cards) ===== */
async function loadPeople() { if (!S.people) S.people = await getJSON('data/people.json').catch(() => []) }
const faceSrc = p => { if (!p) return null; if (p.photo) return p.photo; const q = (S.people || []).find(x => x.folder === p.folder); return q && q.photo || null };
const STATUS = { 'current-mp': 'MP', 'current-mp-standing-2026': 'MP · standing', 'current-mp-retiring': 'MP · retiring', 'candidate-2026': 'Candidate', 'former-mp': 'Former MP', 'deceased': 'Deceased', 'party-official': 'Official' };
const isMP = s => String(s || '').startsWith('current-mp');
const findPerson = (slug, name) => (S.people || []).find(p => p.slug === slug) || (S.people || []).find(p => name && p.name === name);
const CORRECTION_URL = 'https://github.com/not-simon/Politicsnz/issues/new?template=correction.yml';

/* Small shared helpers for the Parties section (prefixed pt to keep global names unique) */
// Text wrapped in .nm is skipped by autolink() (source lines and statements stay plain text).
// A–Z everywhere: base-letter comparison so Ā sorts with A, case ignored.
const ptCmp = (a, b) => String(a || '').localeCompare(String(b || ''), 'en-NZ', { sensitivity: 'base' });
// Surname = last word of the name ("Alma de Anda" files under A, "William Donald Alexander" under A).
const ptSurname = p => { const w = String((p && p.name) || '').trim().split(/\s+/); return w[w.length - 1] || '' };
const ptBySurname = (a, b) => ptCmp(ptSurname(a), ptSurname(b)) || ptCmp(a.name, b.name);
const ptLetter = p => (ptSurname(p).normalize('NFD').replace(/[^A-Za-z]/g, '')[0] || '#').toUpperCase();
const ptInitials = name => String(name || '?').trim().split(/\s+/).filter(Boolean).map(w => w[0]).filter((c, i, a) => i === 0 || i === a.length - 1).join('').toUpperCase();
const ptDate = (iso, opts = { day: 'numeric', month: 'short', year: 'numeric' }) => { if (!iso) return ''; const t = new Date(/^\d{4}-\d{2}-\d{2}$/.test(iso) ? iso + 'T12:00:00' : iso); return isNaN(t) ? String(iso) : t.toLocaleDateString('en-NZ', opts) };
const ptHost = u => { try { return new URL(u).hostname.replace(/^www\./, '') } catch { return '' } };
const ptExt = (u, label, cls = '') => `<a${cls ? ` class="${cls}"` : ''} href="${esc(u)}" target="_blank" rel="noopener">${label}</a>`;
// Source links for any guide value ({sources:[…]} / {source:…} / string list): "source 1 · source 2 …", all of them.
const ptSources = (v, word = 'source') => { const a = Array.isArray(v) ? v.map(x => typeof x === 'string' ? x : x && x.url).filter(Boolean) : srcOf(v); return a.map((u, i) => ptExt(u, esc(word + (a.length > 1 ? ' ' + (i + 1) : '')))).join(' ') };
const ptTag = (s, cls = 'ptag ptag--s') => `<span class="${cls}" style="--pc:${pcolor(s)}"><span class="sw"></span>${esc(pname(s))}</span>`;

// Same crop for everyone: a round .face with the party ring; initials (never a stand-in photo) when there is no photo.
const faceHTML = (p, party, cls = 'face') => { const img = faceSrc(p); const pc = pcolor(party || (p && p.party));
  return img ? `<img class="${cls}" style="--pc:${pc}" loading="lazy" src="${img}" alt="" width="56" height="56">` : `<span class="face--none ${cls}" style="--pc:${pc}" aria-hidden="true">${esc(ptInitials((p && p.name) || '?'))}</span>` };

// Layer 3 for a person: the sheet. Same fields, same order, for everyone.
function openPerson(p) {
  if (!p) return;
  const party = P(p.party); const pc = pcolor(p.party);
  const standing = p.electorate_2026 || p.list_rank_2026 ? `${p.electorate_2026 ? esc(p.electorate_2026) + ' electorate' : 'List only'}${p.list_rank_2026 ? ` · #${esc(p.list_rank_2026)} on the party list` : ''}` : '';
  const row = (k, v) => v ? `<dt>${k}</dt><dd>${v}</dd>` : '';
  const roles = (p.roles || []).map(r => typeof r === 'string' ? r : (r.role || r.title || JSON.stringify(r)));
  const photo = p.photo_credit ? `Photo: ${esc(p.photo_credit)}${p.photo_license ? ' · ' + (p.photo_license_url ? ptExt(p.photo_license_url, esc(p.photo_license)) : esc(p.photo_license)) : ''}${/wikimedia|commons/i.test(p.photo_credit) ? ', cropped' : ''}` : 'No photo supplied';
  const wikiAttr = p.wikipedia && p.has_profile ? `<span>Biography adapted from ${ptExt(p.wikipedia, 'Wikipedia')}, licensed ${ptExt('https://creativecommons.org/licenses/by-sa/4.0/', 'CC BY-SA 4.0')}, and the sources it cites.</span>` : '';
  // Header first (photo, party, status, standing), then the longer blocks folded; the first block present starts open.
  const blocks = [
    roles.length ? ['Roles', roles.length, `<ul class="small person-roles">${roles.map(r => `<li>${esc(r)}</li>`).join('')}</ul>`] : null,
    p.bio || p.before || p.has_profile || p.wikipedia ? ['Profile', '', `${p.bio ? `<div class="prose"><p>${esc(p.bio)}</p></div>` : ''}${p.before ? `<p class="small"><b>Before politics:</b> ${esc(p.before)}</p>` : ''}
      <div class="row">${p.has_profile ? `<a class="btn btn--s" href="#/about/page/${esc(p.folder)}/README.md">${ic('book', 'i--xs')} Read full profile</a>` : ''}${p.wikipedia ? `<a class="btn btn--s btn--quiet" href="${esc(p.wikipedia)}" target="_blank" rel="noopener">Wikipedia article ${ic('ext', 'i--xs')}</a>` : ''}</div>`] : null,
    p.why ? ["In their words: why they're standing", '', `<div class="prose"><p>${esc(p.why)}</p></div>`] : null].filter(Boolean);
  openSheet({ title: p.name, depth: ['Party', 'Person', 'Sources'], at: 1,
    src: `<a class="ptag ptag--s" style="--pc:${pc}" href="#/parties/${esc(p.party)}"><span class="sw"></span>${esc(party.name || pname(p.party))}</a><span>${esc(STATUS[p.status] || p.status || '')}</span>${p.wikipedia ? ptExt(p.wikipedia, 'Wikipedia') : ''}${ptExt('https://github.com/not-simon/Politicsnz/tree/main/' + p.folder, 'Profile source')}`,
    html: `<div class="person-sheet">${faceHTML(p, p.party, 'face face--l')}
      <dl class="dl">${row('Party', `<a href="#/parties/${esc(p.party)}">${esc(party.name || pname(p.party))}</a>`)}${row('Status', esc(STATUS[p.status] || p.status || '') + (p.status_detail ? `<span class="soft" style="display:block;font-weight:400">${esc(p.status_detail)}</span>` : ''))}
        ${row('Standing in 2026', standing)}${row('In Parliament', p.parliaments ? esc(p.parliaments.map(ordinal).join(', ')) + ' Parliament' + (p.parliaments.length > 1 ? 's' : '') : '')}</dl></div>
      <div class="person-blocks">${blocks.map(([t, n, body], i) => `<details class="disclose"${i === 0 ? ' open' : ''}><summary>${esc(t)}${n ? ` <span class="micro muted" style="margin-left:auto">${n}</span>` : ''}</summary><div class="disclose__body">${body}</div></details>`).join('')}</div>
      <p class="src"><span class="nm">${photo}</span>${wikiAttr}<a href="${CORRECTION_URL}" target="_blank" rel="noopener">${ic('flag', 'i--xs')} Correct or reply</a></p>` });
}
// Bring the pressed chip of a horizontally scrolling chip row into view (without moving the page).
function ptScrollChips(row) { if (!row) return; const c = row.querySelector('[aria-pressed="true"], [aria-current="page"]'); if (c && row.scrollWidth > row.clientWidth) row.scrollLeft = Math.max(0, c.offsetLeft - row.offsetLeft - 16) }
