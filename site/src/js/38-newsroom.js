/* ----- party newsroom + follow directory (headline, date, link only) ----- */
const ACCT_LABEL = { website: 'Website', facebook: 'Facebook', instagram: 'Instagram', x: 'X', tiktok: 'TikTok', youtube: 'YouTube', linkedin: 'LinkedIn' };
function acctLinks(a, extra = []) { const out = Object.entries(a || {}).filter(([, u]) => u).map(([k, u]) => `<a class="btn sm ghost" href="${esc(u)}" target="_blank" rel="noopener nofollow">${ACCT_LABEL[k] || k}</a>`);
  for (const e of extra || []) out.push(`<a class="btn sm ghost" href="${esc(e.url || e)}" target="_blank" rel="noopener nofollow">${esc(e.label || e.kind || 'Other')}</a>`); return out.join('') }
V.newsroom = async party => {
  if (!S.news) S.news = await getJSON('data/newsroom.json').catch(() => null);
  const N = S.news; if (!N || !N.items) { $('#main').innerHTML = '<section class="view"><p class="empty">The newsroom feed isn’t available in this build.</p></section>'; return }
  const parties = partyOrder().filter(p => N.parties[p] || N.follow_parties[p]);
  const sel = party && (N.parties[party] || N.follow_parties[party]) ? party : (S.newsSel || 'all'); S.newsSel = sel;
  const fmtD = d => { const t = new Date(d); return isNaN(t) ? '' : t.toLocaleDateString('en-NZ', { day: 'numeric', month: 'short' }) };
  const items = N.items.filter(i => i.party !== 'government').sort((a, b) => String(b.date).localeCompare(String(a.date)));
  const gov = N.items.filter(i => i.party === 'government').sort((a, b) => String(b.date).localeCompare(String(a.date)));
  const row = i => `<a class="pol" style="text-decoration:none;color:inherit" href="${esc(i.url)}" target="_blank" rel="noopener nofollow"><div class="head"><span class="dot" style="background:${pcolor(i.party)};margin-top:6px"></span><div><div class="st" style="font-size:15px">${esc(i.title)}</div><div class="tiny muted">${esc(i.party === 'government' ? 'Minister’s release' : pname(i.party))} · ${fmtD(i.date)} · via ${esc(i.source || '')} ↗</div></div></div></a>`;
  let feed;
  if (sel === 'all') { // equal slots per party first (latest 3 each), then everything newest-first
    const top = [], seen = new Set();
    for (const p of parties) for (const i of items.filter(x => x.party === p).slice(0, 3)) { top.push(i); seen.add(i.url) }
    top.sort((a, b) => String(b.date).localeCompare(String(a.date)));
    const rest = items.filter(i => !seen.has(i.url));
    const quiet = parties.filter(p => !items.some(i => i.party === p) && N.parties[p]);
    feed = `<div class="stack" style="gap:8px">${top.map(row).join('')}</div>
      ${quiet.length ? `<p class="small muted">No release in the last ${N.window_days || 60} days from: ${quiet.map(p => N.parties[p].newsroom_url ? `<a href="${esc(N.parties[p].newsroom_url)}" target="_blank" rel="noopener nofollow">${esc(pname(p))}</a>` : esc(pname(p))).join(', ')} (links go to their own newsrooms).</p>` : ''}
      ${rest.length ? `<details class="card flat"><summary style="cursor:pointer"><b>Everything else, newest first</b> <span class="small muted">· ${rest.length} more</span></summary><div class="stack" style="gap:8px;margin-top:12px">${rest.map(row).join('')}</div></details>` : ''}`;
  } else { const mine = items.filter(i => i.party === sel); const pm = N.parties[sel] || {};
    feed = mine.length ? `<div class="stack" style="gap:8px">${mine.map(row).join('')}</div>` : `<p class="empty">No release from ${esc(pname(sel))} in the last ${N.window_days || 60} days in the feeds we read.${pm.newsroom_url ? ` <a href="${esc(pm.newsroom_url)}" target="_blank" rel="noopener nofollow">Their own newsroom ↗</a>` : ''}</p>` }
  const fp = sel !== 'all' ? N.follow_parties[sel] : null;
  const people = sel !== 'all' ? (N.follow_people || []).filter(p => p.party === sel) : [];
  $('#main').innerHTML = `<section class="view"><div class="stack"><div class="kicker">In their own words</div><h2>Party newsroom</h2>
    <p class="lede">The latest releases from each party, as the parties wrote them. Headlines link to the original. Nothing here is fact-checked by us; for what the parties have actually done, see the <button class="btn ghost sm" data-go="promises">promise tracker</button>.</p>
    <p class="tiny muted">Updated ${esc(String(N.updated || '').slice(0, 16).replace('T', ' '))}. Sources: party releases as published by the parties on Scoop and the Beehive; links go to the original pages. Equal space for every party first, then everything newest-first.</p></div>
    <div class="toolbar"><div class="chips">${[['all', 'All parties'], ...parties.map(p => [p, pname(p)])].map(([k, l]) => `<button class="chip" data-news="${esc(k)}" aria-pressed="${k === sel}" ${k !== 'all' ? `style="--pc:${pcolor(k)}"` : ''}>${esc(l)}</button>`).join('')}</div></div>
    ${feed}
    ${sel !== 'all' ? `<div class="card stack"><h3>Follow ${esc(pname(sel))}</h3>${fp ? `<div class="row">${acctLinks(fp.accounts)}${fp.newsroom_url ? `<a class="btn sm" href="${esc(fp.newsroom_url)}" target="_blank" rel="noopener nofollow">Newsroom</a>` : ''}</div>${Object.values(fp.verified || {}).some(v => v === false) ? '<p class="tiny muted">Some account links could not be checked against the party’s own website (it blocks automated access) and come from Wikidata.</p>' : ''}` : '<p class="small muted">No account links recorded.</p>'}
      ${people.length ? `<details><summary style="cursor:pointer"><b>Candidates and MPs (${people.length})</b> <span class="small muted">· public accounts they listed themselves</span></summary><div class="stack" style="gap:6px;margin-top:12px">${people.sort((a, b) => a.name.localeCompare(b.name)).map(p => { const links = acctLinks(p.accounts, p.other) + (p.email ? `<a class="btn sm ghost" href="mailto:${esc(p.email)}">Email</a>` : ''); return `<div class="row" style="justify-content:space-between;gap:8px"><span class="small"><button class="lnk" data-person="${esc(p.folder)}">${esc(p.name)}</button>${p.electorate_2026 ? ` <span class="tiny muted">· ${esc(p.electorate_2026)}</span>` : ''}</span><span class="row" style="gap:4px">${links || '<span class="tiny muted">no public accounts listed</span>'}</span></div>` }).join('')}</div></details>` : ''}</div>` : ''}
    ${gov.length && (sel === 'all') ? `<details class="card flat"><summary style="cursor:pointer"><b>Ministers’ releases (Beehive)</b> <span class="small muted">· ${gov.length}, official government announcements, not party releases</span></summary><div class="stack" style="gap:8px;margin-top:12px">${gov.slice(0, 30).map(row).join('')}</div></details>` : ''}
    <p class="tiny muted">Account links are as the parties and candidates published them (party websites, candidates’ policy.nz entries, Wikidata where a site blocks access) and are not endorsements. Personal email addresses are not shown. Ask for a correction via the repository.</p></section>`;
  $('#main').querySelectorAll('[data-news]').forEach(b => b.onclick = () => { S.newsSel = b.dataset.news; route(b.dataset.news === 'all' ? 'newsroom' : 'newsroom-' + b.dataset.news) });
};
