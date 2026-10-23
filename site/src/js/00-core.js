(() => {
'use strict';
const ELECTION_DAY = new Date('2026-11-07T19:00:00+13:00');
const KEY_DATES = [['2026-10-25', 'Last day to enrol', 'There is no enrolling on election day this year. Enrol or update your details at vote.nz.'],
  ['2026-10-26', 'Advance voting opens', 'Vote early at any voting place in the country.'],
  ['2026-11-07', 'Election day', 'Voting places open 9am to 7pm. Results start coming in that night.'],
  ['2026-11-27', 'Official results', 'Special votes are counted and the final seat count is confirmed (approx. 3 weeks later).']];
const NAV = [['home', 'Home'], ['vote', 'How to vote'], ['match', 'Match'], ['swipe', 'Swipe'], ['compass', 'Compass'], ['polls', 'Polls'], ['map', 'Map'], ['game', 'Game'], ['parties', 'Parties'], ['issues', 'Issues'], ['parliament', 'Parliament'], ['more', 'More']];
const ICON = {
  home: '<path d="M4 11l8-7 8 7v9a1 1 0 0 1-1 1h-4v-6H9v6H5a1 1 0 0 1-1-1z"/>',
  match: '<path d="M12 21s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.6-7 10-7 10z"/>',
  parties: '<circle cx="8" cy="9" r="3"/><circle cx="16" cy="9" r="3"/><path d="M2 20c0-3 3-5 6-5s6 2 6 5M12 20c0-3 3-5 6-5s4 1.5 4 3"/>',
  issues: '<path d="M4 5h16M4 12h16M4 19h10"/>',
  polls: '<path d="M4 19h16M6 16V9M11 16V5M16 16v-6M20 16v-3"/>',
  vote: '<path d="M4 11h16v9H4zM8 11V5h8v6M9.5 8l1.5 1.5L14 6.5"/>',
  map: '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2zM9 4v14M15 6v14"/>',
  game: '<rect x="3" y="7" width="18" height="11" rx="3"/><path d="M8 11v3M6.5 12.5h3M15 11h.01M17.5 13.5h.01"/>',
  compass: '<circle cx="12" cy="12" r="9"/><path d="m15 9-2 6-4 0 2-6z" fill="currentColor"/>',
  play: '<path d="M7 5v14l12-7z" fill="currentColor"/>', pause: '<path d="M7 5h4v14H7zM13 5h4v14h-4z" fill="currentColor"/>',
  swipe: '<rect x="6" y="4" width="12" height="16" rx="2"/><path d="M3 8v10a2 2 0 0 0 2 2M21 8v10a2 2 0 0 1-2 2M9 15l2 2 4-5"/>',
  more: '<circle cx="5" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="19" cy="12" r="1.6"/>' };
const ic = (k, w = 24) => `<svg viewBox="0 0 24 24" width="${w}" height="${w}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICON[k] || ''}</svg>`;
const S = { data: null, policies: null, people: null, thumbs: null, fulltext: {}, pages: null };
const $ = (s, el = document) => el.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const getJSON = async p => { const r = await fetch(p); if (!r.ok) throw new Error(p + ' ' + r.status); return r.json() };
const store = { get(k) { try { return localStorage.getItem(k) } catch { return null } }, set(k, v) { try { localStorage.setItem(k, v) } catch {} } };
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
