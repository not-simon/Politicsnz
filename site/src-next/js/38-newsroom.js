/* ----- From the parties: press releases (headline, date, link only) + follow directory ----- */
const ACCT_LABEL = { website: 'Website', facebook: 'Facebook', instagram: 'Instagram', x: 'X', tiktok: 'TikTok', youtube: 'YouTube', linkedin: 'LinkedIn' };
const ACCT_ORDER = ['website', 'facebook', 'instagram', 'x', 'tiktok', 'youtube', 'linkedin'];
function acctLinks(a, extra = []) { const out = Object.entries(a || {}).filter(([, u]) => u).sort((x, y) => ACCT_ORDER.indexOf(x[0]) - ACCT_ORDER.indexOf(y[0])).map(([k, u]) => `<a href="${esc(u)}" target="_blank" rel="noopener nofollow">${ACCT_LABEL[k] || esc(k)}</a>`);
  for (const e of extra || []) out.push(`<a href="${esc(e.url || e)}" target="_blank" rel="noopener nofollow">${esc(e.label || e.kind || 'Other')}</a>`); return out.join('') }
// Only office addresses: Parliament or the party's own domain. Anything else (a personal mailbox) is never shown.
function officeEmail(email, party, N) { const m = String(email || '').toLowerCase().match(/@([a-z0-9.-]+)$/); if (!m) return '';
  const fp = (N.follow_parties || {})[party] || {}; const hosts = [ptHost((fp.accounts || {}).website), ptHost(fp.newsroom_url), ptHost((guideParty(party) || {}).website), 'parliament.govt.nz'].filter(Boolean).map(h => h.toLowerCase());
  return hosts.some(h => m[1] === h || m[1].endsWith('.' + h)) ? email : '' }
const newsDate = d => { const t = new Date(d); return isNaN(t) ? '' : t.toLocaleDateString('en-NZ', { day: 'numeric', month: 'short' }) };
function releaseRow(i, withParty = false) {
  return `<a class="release" href="${esc(i.url)}" target="_blank" rel="noopener nofollow"><span class="release__t">${esc(i.title)}</span><span class="release__m">${withParty && i.party !== 'government' ? ptTag(i.party) : ''}${i.party === 'government' ? '<span class="badge badge--outline">Ministerial</span>' : ''}<span>${newsDate(i.date)}</span><span>${ic('ext', 'i--xs')} via ${esc(i.source || ptHost(i.url))}</span></span></a>` }

V.newsroom = async party => {
  if (!S.news) S.news = await getJSON('data/newsroom.json').catch(() => null);
  const N = S.news;
  if (!N || !N.items) { $('#main').innerHTML = sectionFrame('parties', 'parties/news', '<p class="muted">The press-release feed isn’t available in this build.</p>'); return }
  N.parties = N.parties || {}; N.follow_parties = N.follow_parties || {};
  const parties = partyOrder().filter(p => N.parties[p] || N.follow_parties[p]);    // A–Z by short name
  const sel = party && (N.parties[party] || N.follow_parties[party]) ? party : 'all';
  const mode = sel === 'all' && store.get('newsMode') === 'newest' ? 'newest' : 'three';
  const byDate = (a, b) => String(b.date).localeCompare(String(a.date));
  const items = N.items.filter(i => i.party !== 'government').sort(byDate);
  const gov = N.items.filter(i => i.party === 'government').sort(byDate);
  const win = N.window_days || 60;
  const quietLine = p => { const pm = N.parties[p] || N.follow_parties[p] || {}; return `<p class="small muted">No release in the last ${esc(win)} days in the feeds we read.${pm.newsroom_url ? ` <a href="${esc(pm.newsroom_url)}" target="_blank" rel="noopener nofollow">Their own newsroom ${ic('ext', 'i--xs')}</a>` : ''}</p>` };
  const group = (p, L, all = false) => `<section class="pgroup" style="--pc:${pcolor(p)}"><div class="pgroup__h"><h3>${esc(pname(p))}</h3>${all ? '' : `<a class="more micro" href="#/parties/news/${esc(p)}">All ${ic('chev', 'i--xs')}</a>`}</div>${L.length ? L.map(i => releaseRow(i)).join('') : quietLine(p)}</section>`;
  let feed;
  if (sel !== 'all') feed = group(sel, items.filter(i => i.party === sel), true);
  else if (mode === 'newest') feed = `<div>${items.map(i => releaseRow(i, true)).join('')}</div>`;
  else { // equal slots first: the latest three from every party, A to Z; then everything else newest first
    const seen = new Set(); const top = parties.map(p => { const L = items.filter(x => x.party === p).slice(0, 3); L.forEach(i => seen.add(i.url)); return [p, L] });
    const rest = items.filter(i => !seen.has(i.url));
    feed = `<div class="cols cols--2 news-cols">${top.map(([p, L]) => group(p, L)).join('')}</div>
      ${rest.length ? `<details class="disclose"><summary>Everything else, newest first <span class="micro muted" style="margin-left:auto">${rest.length} more</span></summary><div class="disclose__body">${rest.map(i => releaseRow(i, true)).join('')}</div></details>` : ''}` }
  const ministerial = sel === 'all' && gov.length ? `<section class="pgroup pgroup--gov" style="--pc:var(--text-3)"><div class="pgroup__h"><h3>Ministers’ releases</h3><span class="badge badge--outline">Ministerial</span></div>
      <p class="small soft">Official government announcements from the Beehive, not party releases. Shown separately so no party gets extra space for being in government.</p>
      ${gov.slice(0, 5).map(i => releaseRow(i)).join('')}${gov.length > 5 ? `<details class="disclose"><summary>${Math.min(gov.length, 30) - 5} more ministerial releases</summary><div class="disclose__body">${gov.slice(5, 30).map(i => releaseRow(i)).join('')}</div></details>` : ''}</section>` : '';
  // Follow directory: every party A–Z; in a single-party view, also each candidate's own public accounts.
  const followRow = p => { const fp = N.follow_parties[p]; return `<div class="follow__row"><a class="ptag" href="#/parties/news/${esc(p)}" style="--pc:${pcolor(p)}"><span class="sw"></span>${esc(pname(p))}</a><div class="follow__links">${fp ? acctLinks(fp.accounts) : ''}${fp && fp.newsroom_url ? `<a href="${esc(fp.newsroom_url)}" target="_blank" rel="noopener nofollow">Newsroom</a>` : ''}${!fp || (!fp.newsroom_url && !Object.values(fp.accounts || {}).some(Boolean)) ? '<span class="muted">No account links recorded</span>' : ''}</div></div>` };
  const fsel = sel !== 'all' ? N.follow_parties[sel] : null;
  const people = sel !== 'all' ? (N.follow_people || []).filter(p => p.party === sel).sort(ptBySurname) : [];
  const follow = `<section class="stack" aria-labelledby="h-follow"><div class="shead"><div class="shead__row"><h2 id="h-follow">${sel === 'all' ? 'Follow the parties' : 'Follow ' + esc(pname(sel))}</h2><span class="micro muted">Official accounts only · no follower counts</span></div></div>
      <div class="follow">${(sel === 'all' ? parties : [sel]).map(followRow).join('')}</div>
      ${fsel && Object.values(fsel.verified || {}).some(v => v === false) ? '<p class="micro muted">Some account links could not be checked against the party’s own website (it blocks automated access) and come from Wikidata.</p>' : ''}
      ${sel === 'all' ? '<p class="small muted">Candidates’ and MPs’ own accounts are listed on each party’s page here: pick a party above.</p>' : people.length ? `<details class="disclose"><summary>Candidates and MPs <span class="micro muted" style="margin-left:auto">${people.length}, A to Z</span></summary><div class="disclose__body"><p class="micro muted">Public accounts they listed themselves. Office email addresses only.</p><div class="follow">${people.map(p => { const em = officeEmail(p.email, p.party, N); const links = acctLinks(p.accounts, p.other) + (em ? `<a href="mailto:${esc(em)}">Email</a>` : '');
          return `<div class="follow__row"><span><button class="linkbtn" type="button" data-person="${esc(p.folder)}">${esc(p.name)}</button>${p.electorate_2026 ? `<span class="micro muted" style="display:block">${esc(p.electorate_2026)}</span>` : ''}</span><div class="follow__links">${links || '<span class="muted">No public accounts listed</span>'}</div></div>` }).join('')}</div></div></details>` : ''}
    </section>`;
  const updated = N.updated ? new Date(N.updated) : null;
  $('#main').innerHTML = sectionFrame('parties', 'parties/news', `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('news', 'i--s')} Parties · From the parties</p><h1>${sel === 'all' ? 'From the parties' : 'From ' + esc(pname(sel))}</h1>
      <p class="lede">${sel === 'all' ? `The latest press releases from every party, three each, A to Z.` : `The latest press releases from ${esc(P(sel).name || pname(sel))}.`} The parties’ own words: headlines link to the original. For what the parties have actually done, see <a href="#/parties/promises">Promises</a>.</p>
      ${sel === 'all' ? `<div class="row"><div class="seg" role="group" aria-label="Layout">${[['three', 'Three per party'], ['newest', 'Newest first']].map(([k, l]) => `<button type="button" data-mode="${k}" aria-pressed="${mode === k}">${l}</button>`).join('')}</div></div>` : ''}</header>
    <div class="chips chips--scroll news-chips" role="group" aria-label="Party">${[['all', 'All parties'], ...parties.map(p => [p, pname(p)])].map(([k, l]) => `<button class="chip" type="button" data-go="parties/news${k === 'all' ? '' : '/' + esc(k)}" aria-pressed="${k === sel}">${k !== 'all' ? `<span class="sw" style="--pc:${pcolor(k)}"></span>` : ''}${esc(l)}</button>`).join('')}</div>
    <div class="split split--8-4"><div class="stack stack--xl">${feed}${ministerial}${follow}</div>
      <aside class="stack sticky"><div class="note">${ic('info')}<div><b>In their own words.</b> These are the parties’ releases as they published them. We show the headline, date and link only, and nothing here is edited or fact-checked by Ballot Book.</div></div>
        <p class="src">Updated ${updated && !isNaN(updated) ? esc(updated.toLocaleString('en-NZ', { day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit', timeZone: 'Pacific/Auckland' })) : esc(String(N.updated || '').slice(0, 16))} · last ${esc(win)} days · party releases as published on Scoop and the Beehive; links go to the original pages · equal space for every party first</p>
        <p class="micro muted">Account links are as the parties and candidates published them (party websites, candidates’ policy.nz entries, Wikidata where a site blocks access) and are not endorsements. Personal email addresses are not shown. <a href="${CORRECTION_URL}" target="_blank" rel="noopener">Ask for a correction</a></p></aside></div>`);
  ptScrollChips($('#main .news-chips'));
  $('#main').querySelectorAll('[data-mode]').forEach(b => b.onclick = () => { store.set('newsMode', b.dataset.mode); V.newsroom(party) });
};
