/* ----- more / learn ----- */
// Long-form pages: a small index (key -> [group, title]) and four chunks fetched on first use.
async function loadPages() { if (!S.pageIndex) S.pageIndex = await getJSON('data/pages/index.json').catch(() => ({})); S.pages = S.pages || {} }
async function loadPage(k) { await loadPages(); if (S.pages[k] !== undefined) return S.pages[k]; const grp = (S.pageIndex[k] || [])[0]; if (!grp) return undefined;
  S.pageChunks = S.pageChunks || {}; if (!S.pageChunks[grp]) S.pageChunks[grp] = getJSON(`data/pages/${grp}.json`).catch(() => ({}));
  Object.assign(S.pages, await S.pageChunks[grp]); return S.pages[k] }
function pageTitle(k) { const e = S.pageIndex && S.pageIndex[k]; if (e) return e[1]; const t = ((S.pages || {})[k] || '').match(/^#\s+(.+)$/m); return t ? t[1].replace(/[*_`]/g, '') : k }
async function openPage(k) { const t = await loadPage(k);
  if (blockedPage(k)) { openDialog('Hidden until 7pm', `<p>${ELECTION_DAY_BLOCK}</p>`); return }
  if (!t) { openDialog('Not written yet', `<p>${esc(k)} isn't in this version of the guide yet.</p>`); return }
  openDialog(pageTitle(k), `<div class="prose" data-base="${esc(k)}">${md(t.replace(/^#\s+.+\n/, ''))}</div>`) }
function md(t) { try { return DOMPurify.sanitize(marked.parse(String(t || ''))) } catch { return `<pre>${esc(t)}</pre>` } }

// Layer-2 page for long-form markdown (footer links, "about" routes): rendered in the page, not a sheet.
V.page = async key => { const t = await loadPage(key);
  if (blockedPage(key)) { $('#main').innerHTML = `<div class="lock">${ic('lock')}<h2 class="h3">Hidden until 7pm</h2><p>${ELECTION_DAY_BLOCK}</p></div>`; return }
  $('#main').innerHTML = `<article class="stack stack--l" style="max-width:760px"><header class="pagehead"><p class="eyebrow">${esc(key.split('/')[0] === 'docs' ? 'About this guide' : key.split('/')[0])}</p><h1>${esc(t ? pageTitle(key) : 'Not written yet')}</h1></header>
    <div class="prose" data-base="${esc(key)}">${t ? md(t.replace(/^#\s+.+\n/, '')) : `<p>${esc(key)} isn't in this version of the guide yet.</p>`}</div>
    <p class="src">Plain-text source: <a href="https://github.com/not-simon/Politicsnz/blob/main/${esc(key)}" target="_blank" rel="noopener">${esc(key)}</a></p></article>` };
