(() => {
'use strict';
const ELECTION_DAY = new Date('2026-11-07T19:00:00+13:00');
const KEY_DATES = [['2026-10-25', 'Last day to enrol', 'There is no enrolling on election day this year. Enrol or update your details at vote.nz.'],
  ['2026-10-26', 'Advance voting opens', 'Vote early at any voting place in the country.'],
  ['2026-11-07', 'Election day', 'Voting places open 9am to 7pm. Results start coming in that night.'],
  ['2026-11-27', 'Official results', 'Special votes are counted and the final seat count is confirmed (approx. 3 weeks later).']];
// Five sections, named for the voter's question (see site/redesign/IA.md). Same five on phone and desktop.
const SECTIONS = [['today', 'Today'], ['vote', 'Vote'], ['choose', 'Choose'], ['parties', 'Parties'], ['seats', 'Seats']];
// Icons come from the inline sprite in shell.html (ids i-<name>). Sizes: default 24, .i--s 18, .i--xs 14, .i--l 32.
const ic = (k, cls = '') => `<svg class="i i-${k}${cls ? ' ' + cls : ''}" aria-hidden="true"><use href="#i-${k}"/></svg>`;
const S = { data: null, policies: null, people: null, thumbs: null, fulltext: {}, pages: null };
const $ = (s, el = document) => el.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const _json = {};  // one request per URL (views re-render; cache-busted URLs with ?t= bypass the cache)
const getJSON = p => { if (_json[p] && !p.includes('?t=')) return _json[p]; const q = fetch(p).then(r => { if (!r.ok) throw new Error(p + ' ' + r.status); return r.json() }); q.catch(() => { delete _json[p] }); if (!p.includes('?t=')) _json[p] = q; return q };
const store = { get(k) { try { return localStorage.getItem(k) } catch { return null } }, set(k, v) { try { localStorage.setItem(k, v) } catch {} } };
// Election history, Parliament membership and promises are fetched on first use (see render() in 90-shell-router.js).
async function needData(...keys) { await Promise.all(keys.filter(k => !S.data[k]).map(async k => { S.data[k] = await getJSON('data/' + k + '.json').catch(() => []) })) }
const P = s => (S.data.parties[s] || { slug: s, name: s, short: s, color: '#A7ADB5', order: 90 });
const pname = s => P(s).short || s;
const pcolor = s => P(s).color || '#A7ADB5';
const fmt = (n, d = 1) => (n == null || isNaN(n)) ? '–' : Number(n).toFixed(d);
const G = () => (S.data.guide || {});
const T = v => v == null ? '' : typeof v === 'string' ? v : (v.text || v.summary || v.label || v.quote || '');
const srcOf = v => { if (!v || typeof v !== 'object') return []; const a = [].concat(v.sources || [], v.source || [], v.source_url || []); return a.map(x => typeof x === 'string' ? x : x.url).filter(Boolean) };
const srcLinks = v => { const a = srcOf(v); return a.length ? ` <span class="tiny">${a.slice(0, 3).map((u, i) => `<a href="${esc(u)}" target="_blank" rel="noopener">source${a.length > 1 ? ' ' + (i + 1) : ''}</a>`).join(' ')}</span>` : '' };
const guideParty = s => ((G().parties || []).find(p => p.slug === s) || null);
const initials = s => (pname(s) || '?').replace(/[^A-Za-zĀ-ū ]/g, '').split(' ').filter(Boolean).slice(0, 2).map(w => w[0]).join('').toUpperCase();
function ordinal(n) { const s = ['th', 'st', 'nd', 'rd'], v = n % 100; return n + (s[(v - 20) % 10] || s[v] || s[0]) }
const daysLeft = () => { const t = nzNow(); const today = Date.UTC(t.getFullYear(), t.getMonth(), t.getDate()); return Math.round((Date.UTC(2026, 10, 7) - today) / 864e5) };


/* ===== views ===== */
const V = {};
