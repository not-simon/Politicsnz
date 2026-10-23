/* ===== people helpers ===== */
async function loadPeople() { if (!S.people) S.people = await getJSON('data/people.json').catch(() => []); if (!S.thumbs) S.thumbs = await getJSON('data/thumbs.json').catch(() => ({})) }
const STATUS = { 'current-mp': 'MP', 'current-mp-standing-2026': 'MP · standing', 'current-mp-retiring': 'MP · retiring', 'candidate-2026': 'Candidate', 'former-mp': 'Former MP', 'deceased': 'Deceased', 'party-official': 'Official' };
const isMP = s => String(s || '').startsWith('current-mp');
const findPerson = (slug, name) => (S.people || []).find(p => p.slug === slug) || (S.people || []).find(p => name && p.name === name);
const faceHTML = (p, party, cls = 'face') => { const img = p && S.thumbs && S.thumbs[p.folder]; return img ? `<img class="${cls}" style="--pc:${pcolor(party || p.party)}" loading="lazy" src="${img}" alt="">` : `<span class="${cls}" style="--pc:${pcolor(party || (p && p.party))};display:grid;place-items:center;font:800 20px var(--font-display);color:var(--text-2)">${esc(((p && p.name) || '?')[0])}</span>` };
function openPerson(p) {
  openDialog(p.name, `<div class="row" style="align-items:flex-start;gap:20px">${faceHTML(p, p.party, 'face" style="width:128px;height:128px;--pc:' + pcolor(p.party))}
    <div class="stack" style="flex:1;min-width:220px;gap:6px"><div class="row" style="gap:8px"><span class="dot" style="background:${pcolor(p.party)}"></span><b>${esc(P(p.party).name || pname(p.party))}</b><span class="status ${isMP(p.status) ? 'mp' : ''}">${esc(STATUS[p.status] || p.status || '')}</span></div>
    ${p.status_detail ? `<div>${esc(p.status_detail)}</div>` : ''}
    ${p.electorate_2026 || p.list_rank_2026 ? `<div class="small"><b>Standing in 2026:</b> ${p.electorate_2026 ? esc(p.electorate_2026) + ' electorate' : 'list only'}${p.list_rank_2026 ? ` · #${p.list_rank_2026} on the party list` : ''}</div>` : ''}
    ${p.parliaments ? `<div class="small"><b>In Parliament:</b> ${esc(p.parliaments.map(ordinal).join(', '))}</div>` : ''}
    ${p.before ? `<div class="small"><b>Before politics:</b> ${esc(p.before)}</div>` : ''}
    ${p.wikipedia ? `<div class="small"><a href="${esc(p.wikipedia)}" target="_blank" rel="noopener">Wikipedia article</a></div>` : ''}</div></div>
    ${(p.roles || []).length ? `<h4 style="margin-top:20px">Roles</h4><ul class="small">${p.roles.map(r => `<li>${esc(typeof r === 'string' ? r : (r.role || r.title || JSON.stringify(r)))}</li>`).join('')}</ul>` : ''}
    ${p.bio ? `<h4 style="margin-top:16px">Profile</h4><p class="read">${esc(p.bio)}</p>` : ''}
    ${p.why ? `<h4 style="margin-top:16px">In their words: why they're standing</h4><p class="read">${esc(p.why)}</p>` : ''}
    ${p.has_profile ? `<p style="margin-top:16px"><button class="btn sm" data-page="${esc(p.folder)}/README.md">Read full profile</button></p>` : ''}
    <p class="tiny muted" style="margin-top:16px">${p.photo_credit ? 'Photo: ' + esc(p.photo_credit) + (p.photo_license ? ' · ' + (p.photo_license_url ? `<a href="${esc(p.photo_license_url)}" target="_blank" rel="noopener">${esc(p.photo_license)}</a>` : esc(p.photo_license)) : '') + (/wikimedia|commons/i.test(p.photo_credit) ? ', cropped' : '') : ''}${p.wikipedia && p.has_profile ? `${p.photo_credit ? ' · ' : ''}Biography adapted from <a href="${esc(p.wikipedia)}" target="_blank" rel="noopener">Wikipedia</a>, licensed <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">CC BY-SA 4.0</a>, and the sources it cites.` : ''} · <a href="https://github.com/not-simon/Politicsnz/issues/new?template=correction.yml" target="_blank" rel="noopener">Correct or reply</a></p>`) }
