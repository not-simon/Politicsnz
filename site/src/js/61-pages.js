/* ----- more / learn ----- */
async function loadPages() { if (!S.pages) S.pages = await getJSON('data/pages.json').catch(() => ({})) }
V.more = async () => { await loadPages(); const keys = Object.keys(S.pages);
  const group = (title, f) => { const ks = keys.filter(f); return ks.length ? `<div class="stack"><h3>${title}</h3><div class="grid">${ks.map(k => `<button class="starter" style="padding:14px" data-page="${esc(k)}"><h4>${esc(pageTitle(k))}</h4><span class="tiny muted">${esc(k)}</span></button>`).join('')}</div></div>` : '' };
  $('#main').innerHTML = `<section class="view"><div class="stack"><div class="kicker">Go deeper</div><h2>Everything else</h2></div>
    <div class="starters"><button class="starter" data-go="game"><h3>Whose policy? (game)</h3><p class="small muted">Pass-the-phone party-guessing game for 2–6 players.</p><span class="go">Play →</span></button>
      <button class="starter" data-go="trust"><h3>Why trust this?</h3><p class="small muted">Who made it, how it's funded, the rules it follows, how to report an error.</p><span class="go">Open →</span></button>
      <button class="starter" data-go="compass"><h3>Political compass</h3><p class="small muted">Your values on standard axes, with the parties plotted.</p><span class="go">Open →</span></button>
      <button class="starter" data-go="map"><h3>Electorate map</h3><p class="small muted">Every seat since 2011, coloured by winner, with a time slider.</p><span class="go">Open →</span></button>
      <button class="starter" data-go="parliament"><h3>Parliament</h3><p class="small muted">Seat maps, poll trends, coalition builder and seat calculator.</p><span class="go">Open →</span></button>
      <button class="starter" data-go="electorate"><h3>Your electorate</h3><p class="small muted">Candidates where you live, with photos and the 2023 result.</p><span class="go">Open →</span></button>
      <button class="starter" data-go="issues"><h3>The big issues</h3><p class="small muted">Where every party stands, issue by issue.</p><span class="go">Open →</span></button>
      <button class="starter" data-go="policies"><h3>Every policy</h3><p class="small muted">Search and compare all parties' 2026 policies, with full original texts.</p><span class="go">Open →</span></button>
      <button class="starter" data-go="people"><h3>People</h3><p class="small muted">Profiles and photos of MPs since 2011 and all 2026 candidates.</p><span class="go">Open →</span></button>
      <button class="starter" data-go="promises"><h3>Promise tracker</h3><p class="small muted">How each party has kept, broken or dropped its promises.</p><span class="go">Open →</span></button>
      <button class="starter" data-go="newsroom"><h3>Newsroom &amp; follow</h3><p class="small muted">The latest releases from every party, in their own words, and where to follow each party and candidate.</p><span class="go">Open →</span></button></div>
    ${group('Start here', k => ['REPORT.md', 'README.md'].includes(k) || k.startsWith('guide/') || k.endsWith('MINOR_PARTIES.md'))}
    ${group('Elections 2011–2026', k => k.startsWith('elections/') && !k.endsWith('README.md'))}
    ${group('Party profiles', k => /^parties\/[^/]+\/README\.md$/.test(k))}
    ${group('Track records', k => k.endsWith('track-record.md'))}
    <div class="card stack"><h3>Your saved answers</h3><p class="small">Quiz, swipe and compass answers are saved on this device only. To move them to another device, copy this code and paste it there.</p><div class="row"><button class="btn sm" id="exp">Copy my code</button><input type="search" id="impcode" placeholder="Paste a code" aria-label="Import code" style="flex:1 1 200px"><button class="btn sm" id="imp">Import</button><span class="tiny muted" id="expmsg"></span></div></div>
    <div class="card stack"><h3>About this guide</h3><p class="small">Ballot Book is an independent, non-partisan research archive. It isn't affiliated with any party. Summaries are written to be neutral and every fact links to a source: party websites and policy documents, the Electoral Commission, Parliament, Wikipedia, policy.nz and news reports. Party policy texts are reproduced as published, for reference. If you spot an error, the files are plain text in the GitHub repository.</p></div></section>`;
  $('#exp').onclick = async () => { const code = exportSaved(); try { await navigator.clipboard.writeText(code); $('#expmsg').textContent = 'Copied' } catch { $('#impcode').value = code; $('#impcode').select(); $('#expmsg').textContent = 'Select and copy the code' } };
  $('#imp').onclick = () => { try { importSaved($('#impcode').value); $('#expmsg').textContent = 'Imported. Your saved answers are restored.' } catch { $('#expmsg').textContent = 'That code didn’t work.' } } };
function pageTitle(k) { const t = (S.pages[k] || '').match(/^#\s+(.+)$/m); return t ? t[1].replace(/[*_`]/g, '') : k }
async function openPage(k) { await loadPages(); const t = S.pages[k];
  if (blockedPage(k)) { openDialog('Hidden until 7pm', `<p>${ELECTION_DAY_BLOCK}</p>`); return }
  if (!t) { openDialog('Not written yet', `<p>${esc(k)} isn't in this version of the guide yet.</p>`); return }
  openDialog(pageTitle(k), `<div class="prose" data-base="${esc(k)}">${md(t.replace(/^#\s+.+\n/, ''))}</div>`) }
function md(t) { try { return DOMPurify.sanitize(marked.parse(String(t || ''))) } catch { return `<pre>${esc(t)}</pre>` } }

// Layer-2 page for long-form markdown (footer links, "about" routes): rendered in the page, not a sheet.
V.page = async key => { await loadPages(); const t = S.pages[key];
  if (blockedPage(key)) { $('#main').innerHTML = `<div class="lock">${ic('lock')}<h2 class="h3">Hidden until 7pm</h2><p>${ELECTION_DAY_BLOCK}</p></div>`; return }
  $('#main').innerHTML = `<article class="stack stack--l" style="max-width:760px"><header class="pagehead"><p class="eyebrow">${esc(key.split('/')[0] === 'docs' ? 'About this guide' : key.split('/')[0])}</p><h1>${esc(t ? pageTitle(key) : 'Not written yet')}</h1></header>
    <div class="prose" data-base="${esc(key)}">${t ? md(t.replace(/^#\s+.+\n/, '')) : `<p>${esc(key)} isn't in this version of the guide yet.</p>`}</div>
    <p class="src">Plain-text source: <a href="https://github.com/not-simon/Politicsnz/blob/main/${esc(key)}" target="_blank" rel="noopener">${esc(key)}</a></p></article>` };
