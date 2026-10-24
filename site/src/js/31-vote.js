/* ===== Vote: Ready to vote · Key dates · Make a plan · How MMP works · Glossary · What specials could change (mockups/vote.html) =====
   Everything about *how* to vote links to vote.nz; this guide must never look official. */
const OFFICIAL_LINE = `<p class="note">${ic('info', 'i--s')}<span>Official information comes from the Electoral Commission: <a href="https://vote.nz" target="_blank" rel="noopener">vote.nz</a> or 0800 36 76 56 (free, 24 hours). Ballot Book NZ is an independent guide, not the Commission.</span></p>`;
const voteFoot = () => `<div class="stack stack--s">${OFFICIAL_LINE}<div class="micro notec">${NOT_EC}</div></div>`;
const voteHead = (eyebrow, h1, lede) => `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('vote', 'i--s')} Vote${eyebrow ? ' · ' + esc(eyebrow) : ''}</p><h1>${h1}</h1>${lede ? `<p class="lede">${lede}</p>` : ''}</header>`;
const vExt = (href, label, cls = 'btn btn--s') => `<a class="${cls}" href="${esc(href)}" target="_blank" rel="noopener">${label} ${ic('ext', 'i--xs ext')}</a>`;

const rowbtn = (attrs, icon, title, sub) => `<button class="rowlink" type="button" aria-haspopup="dialog" ${attrs}><span class="rowlink__icon">${ic(icon)}</span><span><span class="rowlink__title">${title}</span><span class="rowlink__sub" style="display:block">${sub}</span></span>${ic('chev')}</button>`;
const contactLabel = k => k.replace(/_/g, ' ').replace(/^\w/, c => c.toUpperCase());

V.vote = async sub => {
  const views = { plan: votePlan, mmp: voteMMP, glossary: voteGlossary, specials: voteSpecials, dates: voteDates };
  const fn = views[sub] || voteReady; const key = views[sub] ? 'vote/' + sub : 'vote';
  $('#main').innerHTML = sectionFrame('vote', key, `<div class="stack stack--xl" id="vote-body"></div>`);
  fn($('#vote-body'));
};

/* ----- Ready to vote: five ticks, deadline, "which of these are you?" ----- */
// Situations, matched against each how-to-vote section's who_its_for list. 'basics' is the default.
const VOTE_SIT = [
  ['basics', 'Just the basics', 'The steps everyone needs', null, ['eligible', 'enrol', 'when-where', 'first-time']],
  ['first', 'First time voting', 'What happens inside', /first-time|refresher/i, ['eligible', 'enrol']],
  ['moved', 'Moved house', 'Update by Sunday 25 Oct', /moved house/i, ['when-where']],
  ['lapsed', 'Haven’t voted in a while', 'Check your details', /refresher|moved house/i, ['eligible', 'enrol', 'when-where']],
  ['away', 'Away on the day', 'Vote anywhere in NZ', /away from home|shift workers/i, []],
  ['overseas', 'Overseas', 'Download, sign, upload', /overseas|abroad|travellers/i, []],
  ['help', 'Need help to vote', 'Phone, a helper, access', /disab|blind|deaf|illness|mobility|hand|dementia|hospital/i, []],
  ['student', 'Student', 'Home or uni electorate', /student/i, ['enrol']],
  ['newres', 'New to New Zealand', 'Are you eligible?', /new residents|visas/i, ['enrol']]];
function sitSections(secs, key) { const s = VOTE_SIT.find(x => x[0] === key) || VOTE_SIT[0]; const [, , , re, extra] = s;
  return secs.filter(sec => extra.includes(sec.id) || (re && (sec.who_its_for || []).some(w => re.test(w)))) }

function voteReady(root) {
  const H = G().howtovote || {}; const secs = H.sections || []; const list = H.checklist || []; const ph = electionPhase();
  if (!list.length && !secs.length) { root.innerHTML = `${voteHead('', 'How to vote', '')}<p class="note">${ic('info', 'i--s')}<span>The guide is being verified. Meanwhile: enrol or check your details at <a href="https://vote.nz" target="_blank" rel="noopener">vote.nz</a> or call 0800 36 76 56.</span></p>${voteFoot()}`; return }
  let st; try { st = JSON.parse(store.get('votecheck') || '{}') || {} } catch { st = {} }
  let sit = store.get('votesit'); if (!VOTE_SIT.some(s => s[0] === sit)) sit = 'basics';   // old values ('all', 'first-time voters'…) fall back to the basics
  const core = list.slice(0, 5); const extra = list.slice(5); const toE = daysTo('2026-10-25');
  const top = { enrol: `<b>Enrolment closes at midnight on Sunday 25 October.</b> There is no enrolling at voting places or on election day this year. If you’re not sure you’re enrolled, check now: it takes two minutes.`,
    advance: `<b>Voting is open.</b> You can vote at any voting place in the country until Friday 6 November, or on election day, Saturday 7 November, 9am–7pm.`,
    electionday: `<b>Today is election day.</b> Voting places are open 9am–7pm. You don’t need ID or your EasyVote card.`,
    results: `<b>Voting has closed.</b> Election-night results are preliminary; special votes are counted later.`,
    after: `<b>The 2026 election has been held.</b> Special votes are being counted; the official result is due Friday 27 November.` }[ph];
  const actions = (c, i) => { const a = [];
    if (c.url) a.push(vExt(c.url, /vote\.nz/.test(c.url) && !/map\.vote/.test(c.url) ? 'At vote.nz' : /map\.vote/.test(c.url) ? 'Find a voting place' : 'Official source', `btn btn--s${i === 1 && ph === 'enrol' ? ' btn--primary' : ''}`));
    if (i === 2) a.push(`<a class="btn btn--s btn--quiet" href="#/vote/plan">Make a plan</a>`);
    if (i === 4) a.push(`<a class="more small" href="#/vote/mmp">See the ballot paper ${ic('chev', 'i--xs')}</a>`);
    return a.length ? `<div class="check__a">${a.join('')}</div>` : '' };
  const checkLi = (c, i) => `<li class="check${st[i] ? ' is-done' : ''}">
      <label class="check__tick"><input class="sr-only" type="checkbox" data-ck="${i}"${st[i] ? ' checked' : ''}><span class="sr-only">Mark done: ${esc(c.step)}</span>${TICK_SVG()}</label>
      <span class="check__t">${esc(c.step)}${i === 1 && ph === 'enrol' ? ` <span class="deadline">${toE > 1 ? `${toE} days left` : toE === 1 ? '1 day left' : 'Closes tonight'}</span>` : ''}</span>
      <p class="check__d">${esc(c.done_when)}</p>${actions(c, i)}</li>`;
  const progress = () => { const n = core.filter((_, i) => st[i]).length; return `<b>${n} of ${core.length} done</b><div class="bar"><i style="--w:${core.length ? n / core.length * 100 : 0}%"></i></div>` };
  const secHTML = sec => `<details class="disclose"><summary>${esc(sec.title.replace(/^\d+\.\s*/, ''))}</summary><div class="disclose__body">
      <ol class="vsteps">${(sec.steps || []).map(x => `<li><p>${esc(x.text)}${x.date ? ` <span class="badge">${esc(x.date)}</span>` : ''}</p>${x.url ? `<p class="src">${ic('doc')} ${extA(x.url, esc((x.source || 'Source').split(',')[0]))}</p>` : ''}</li>`).join('')}</ol>
      ${(sec.notes || []).length ? `<ul class="small muted vnotes">${sec.notes.map(n => `<li>${esc(n)}</li>`).join('')}</ul>` : ''}</div></details>`;
  const personaHTML = () => { const shown = sitSections(secs, sit);
    return `<div class="persona" role="group" aria-label="Your situation">${VOTE_SIT.map(([k, l, s]) => `<button type="button" data-sit="${k}" aria-pressed="${k === sit}">${esc(l)}<span>${esc(k === 'moved' && ph !== 'enrol' ? 'Where you’re enrolled' : s)}</span></button>`).join('')}</div>
      <div class="stack stack--s" id="sit-out"><p class="small muted">${shown.length} part${shown.length === 1 ? '' : 's'} of the official guidance, in plain words, with a link to the source for every step.</p><div>${shown.map(secHTML).join('')}</div></div>` };
  const kd = (H.key_dates || []).filter(d => d.date >= nzToday().iso); const next = kd[0];
  const contacts = Object.entries(H.contacts || {}).filter(([k, v]) => typeof v === 'string');
  const vp = H.voting_places || {}; const anyExtra = extra.some((_, j) => st[j + 5]);
  root.innerHTML = `${voteHead('Ready to vote', `Ready to vote in ${core.length === 5 ? 'five' : core.length} ticks.`, 'Most people need about five minutes. There’s nothing to bring and no ID to show. Your ticks are saved on this device, nowhere else.')}
    <div class="callout callout--signal"><p>${top}</p></div>
    <div class="split split--7-5">
      <section class="stack" aria-labelledby="h-check">
        <h2 id="h-check" class="sr-only">Checklist</h2>
        <div class="progress-line" id="vprog" aria-live="polite">${progress()}</div>
        <ol class="checklist">${core.map(checkLi).join('')}</ol>
        ${extra.length ? `<details class="disclose"${anyExtra ? ' open' : ''}><summary>If it applies to you: ${extra.length} more tick${extra.length === 1 ? '' : 's'}</summary><div class="disclose__body"><ol class="checklist">${extra.map((c, j) => checkLi(c, j + 5)).join('')}</ol></div></details>` : ''}
      </section>
      <section class="stack" aria-labelledby="h-who">
        <div class="panel">
          <div class="stack stack--s"><h2 id="h-who" class="h3">Which of these are you?</h2><p class="small muted">Pick one to see the steps that apply to you. Each opens with a link to its official source.</p></div>
          <div id="persona">${personaHTML()}</div>
        </div>
      </section>
    </div>
    <section class="stack" aria-labelledby="h-next">
      <div class="shead"><h2 id="h-next">Next steps</h2></div>
      <div class="rows">
        ${rowbtn('data-vsheet="places"', 'map', 'Find a voting place', 'Any voting place in New Zealand. Hours vary during advance voting.')}
        ${rowlink('#/vote/dates', 'clock', 'Key dates', next ? `Next: ${shortDate(next.date)}, ${esc(next.event.replace(/\s*\(.*?\)/g, '').split(/[.;]/)[0].replace(/^[A-Z ]{6,}\b/, m => m.charAt(0) + m.slice(1).toLowerCase()))}` : 'Every date in the 2026 election, and what it means.')}
        ${ph === 'results' || ph === 'after' ? '' : rowlink('#/vote/plan', 'caladd', 'Make a plan', 'Pick a day, a time and a place. Add it to your calendar.')}
        ${contacts.length ? rowbtn('data-vsheet="help"', 'phone', 'Need a hand?', 'Free phone, text, email and post contacts at the Electoral Commission.') : ''}
        ${(H.could_not_verify || []).length ? rowbtn('data-page="guide/how-to-vote.md"', 'book', 'The full guide', 'Every step in one page, and what we couldn’t verify.') : ''}
      </div>
    </section>
    <p class="src">${ic('shield')} Checked ${esc(H.as_of || '')} against vote.nz, elections.nz and the Electoral Act 1993. Every step links to its source.</p>
    ${voteFoot()}`;
  root.querySelectorAll('[data-ck]').forEach(c => c.onchange = () => { st[c.dataset.ck] = c.checked; store.set('votecheck', JSON.stringify(st)); c.closest('.check').classList.toggle('is-done', c.checked); $('#vprog').innerHTML = progress() });
  $('#persona').addEventListener('click', e => { const b = e.target.closest('[data-sit]'); if (!b) return; sit = b.dataset.sit; store.set('votesit', sit);
    $('#persona').innerHTML = personaHTML(); const nb = $(`#persona [data-sit="${sit}"]`); if (nb) nb.focus({ preventScroll: true }) });
  root.addEventListener('click', e => { const b = e.target.closest('[data-vsheet]'); if (!b) return;
    if (b.dataset.vsheet === 'places') openSheet({ title: 'Find a voting place', depth: ['Ready to vote', 'Voting places'], at: 1, src: `From vote.nz, checked ${esc(H.as_of || '')}. Hours and places can change, so check the official finder before you go.`,
      html: `<p class="soft">The official finder shows every voting place with its days and hours, and lets you filter for wheelchair access. Hours vary during advance voting; on election day every place is open 9am–7pm. You can vote at any voting place in New Zealand.</p>
        <div class="row">${vExt(vp.official_finder || 'https://map.vote.nz', 'Open the official finder', 'btn btn--s btn--ink')}${vExt(vp.official_finder_list_view || 'https://vote.nz', 'List view', 'btn btn--s btn--quiet')}</div>${OFFICIAL_LINE}` });
    if (b.dataset.vsheet === 'help') openSheet({ title: 'Need a hand?', depth: ['Ready to vote', 'Contacts'], at: 1, src: `Electoral Commission contacts, from vote.nz, checked ${esc(H.as_of || '')}.`,
      html: `<dl class="dl vhelp">${contacts.map(([k, v]) => `<dt>${esc(contactLabel(k))}</dt><dd>${esc(v)}</dd>`).join('')}</dl>${OFFICIAL_LINE}` }) });
}

/* ----- Key dates: every date in the 2026 election and what it means (coming up first, then the ones already past) ----- */
function voteDates(root) {
  const H = G().howtovote || {}; const all = (H.key_dates || []).slice().sort((a, b) => a.date.localeCompare(b.date)); const t = nzToday().iso;
  const up = all.filter(d => d.date >= t), past = all.filter(d => d.date < t);
  const wd = iso => new Date(iso + 'T00:00:00Z').toLocaleDateString('en-NZ', { weekday: 'short', timeZone: 'UTC' });
  const li = d => `<li${d.date === '2026-11-07' ? ' class="is-eday"' : ''}><span class="num">${shortDate(d.date)}<span class="micro muted vdates__wd">${wd(d.date)}</span></span><span class="stack stack--s"><span class="small">${esc(d.event)}${d.date === t ? ' <span class="badge badge--signal">Today</span>' : ''}</span>${d.source ? `<span class="src">${ic('doc')} ${extA(d.source, esc(d.source.replace(/^https?:\/\//, '').split('/')[0]))}${d.source_date ? ` · checked ${esc(shortDate(d.source_date))}` : ''}</span>` : ''}</span></li>`;
  root.innerHTML = `${voteHead('Key dates', 'Key dates, and what each means.', 'Every date in the 2026 election, from roll changes to the official result. Dates come from the Electoral Commission; check vote.nz if anything changes.')}
    <section class="stack stack--s" aria-labelledby="h-kd-up"><div class="shead"><h2 id="h-kd-up">Coming up</h2></div>
      ${up.length ? `<ul class="vdates">${up.map(li).join('')}</ul>` : '<p class="small muted">All the key dates have passed.</p>'}</section>
    ${past.length ? `<details class="disclose"><summary>Already passed: ${past.length} date${past.length === 1 ? '' : 's'}</summary><div class="disclose__body"><ul class="vdates">${past.map(li).join('')}</ul></div></details>` : ''}
    <div class="rows">${rowlink('#/vote', 'vote', 'Ready to vote', 'Five ticks, and which steps apply to you.')}${rowlink('#/vote/specials', 'clock', 'What special votes could change', 'Between election night and the official result.')}</div>
    ${voteFoot()}`;
}

/* ----- Make a plan: when, where, with whom → .ics + message ----- */
const PLAN_SLOTS = [['morning', 'Morning', 9, 11], ['midday', 'Midday', 11, 13], ['afternoon', 'Afternoon', 13, 16], ['late', 'After 4', 16, 18]];
function planDays() { const t = nzToday(); const out = [];
  for (let d = 26; d <= 38; d++) { const dt = new Date(Date.UTC(2026, 9, d)); const iso = dt.toISOString().slice(0, 10); if (iso < t.iso) continue;
    const eday = iso === '2026-11-07'; out.push({ iso, eday, label: dt.toLocaleDateString('en-NZ', { weekday: 'short', day: 'numeric', month: 'short', timeZone: 'UTC' }) }) }
  return out }
function planText(p, days) { const d = days.find(x => x.iso === p.day); const s = PLAN_SLOTS.find(x => x[0] === p.slot); if (!d || !s) return '';
  const hr = h => (h > 12 ? h - 12 : h) + (h >= 12 ? 'pm' : 'am');
  return `My voting plan: ${d.eday ? 'election day, ' : ''}${d.label}, ${s[1].toLowerCase()} (${hr(s[2])}–${hr(s[3])})${p.where ? `, at ${p.where}` : ''}${p.withWho ? `, with ${p.withWho}` : ''}. Find a voting place and its hours: https://map.vote.nz` }
function planICS(p, days) { const d = days.find(x => x.iso === p.day); const s = PLAN_SLOTS.find(x => x[0] === p.slot); if (!d || !s) return null;
  const [y, m, dd] = d.iso.split('-').map(Number); const stamp = h => new Date(Date.UTC(y, m - 1, dd, h - 13)).toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z');   // NZDT is UTC+13 for the whole voting period
  const escI = v => String(v).replace(/[\\;,]/g, c => '\\' + c).replace(/\n/g, '\\n');
  return ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Ballot Book NZ//Voting plan//EN', 'CALSCALE:GREGORIAN', 'BEGIN:VEVENT',
    `UID:voteplan-${d.iso}-${s[0]}@ballotbook.nz`, `DTSTAMP:${new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z')}`, `DTSTART:${stamp(s[2])}`, `DTEND:${stamp(s[2] + 1)}`,
    `SUMMARY:${escI('Go and vote' + (p.withWho ? ' with ' + p.withWho : ''))}`, `LOCATION:${escI(p.where || 'Any voting place (map.vote.nz)')}`,
    `DESCRIPTION:${escI(planText(p, days) + '\nNo ID needed. Official information: vote.nz or 0800 36 76 56.')}`, 'URL:https://map.vote.nz',
    'BEGIN:VALARM', 'TRIGGER:-PT1H', 'ACTION:DISPLAY', 'DESCRIPTION:Voting today', 'END:VALARM', 'END:VEVENT', 'END:VCALENDAR'].join('\r\n') }
function votePlan(root) {
  const ph = electionPhase(); const days = planDays();
  let p; try { p = JSON.parse(store.get('voteplan') || '{}') || {} } catch { p = {} }
  if (!days.some(d => d.iso === p.day)) p.day = (days.find(d => d.eday) || days[0] || {}).iso;
  if (!PLAN_SLOTS.some(s => s[0] === p.slot)) p.slot = 'morning';
  const closed = ph === 'results' || ph === 'after' || !days.length;
  const save = () => store.set('voteplan', JSON.stringify(p));
  const draw = () => { const txt = planText(p, days);
    root.innerHTML = `${voteHead('Make a plan', 'Make a voting plan.', 'People who decide when and where they’ll vote are more likely to follow through. Your plan becomes a calendar event or a message. Nothing is sent to us; it’s saved on this device.')}
      ${closed ? `<div class="callout callout--signal"><p><b>Voting has closed for 2026.</b> There’s nothing left to plan; see <a href="#/vote/specials">what special votes could change</a>.</p></div>` : `
      <div class="split split--7-5">
        <div class="plan">
          <div class="row row--between"><b>My voting plan</b><span class="micro muted">Saved on this device</span></div>
          <div class="plan__q" style="margin-top:14px"><span id="pq-day">When</span><div class="chips chips--scroll" role="group" aria-labelledby="pq-day">${days.map(d => `<button class="chip" type="button" data-day="${d.iso}" aria-pressed="${d.iso === p.day}">${esc(d.label)}${d.eday ? ' · election day' : ''}</button>`).join('')}</div>
            <div class="chips" role="group" aria-label="Time of day">${PLAN_SLOTS.map(([k, l, a, b]) => `<button class="chip" type="button" data-slot="${k}" aria-pressed="${k === p.slot}">${l} <span class="micro muted">${a > 12 ? a - 12 : a}–${b > 12 ? b - 12 : b}${b >= 12 ? 'pm' : 'am'}</span></button>`).join('')}</div>
            <p class="micro muted">${(days.find(d => d.iso === p.day) || {}).eday ? 'Election day: every voting place is open 9am–7pm.' : 'Advance voting hours differ from place to place; check yours on map.vote.nz.'}</p></div>
          <div class="plan__q"><label for="pq-where"><span class="plan__lbl">Where</span></label><input class="input" id="pq-where" type="text" maxlength="80" autocomplete="off" placeholder="e.g. the library on the main street" value="${esc(p.where || '')}">
            <a class="more small" href="https://map.vote.nz" target="_blank" rel="noopener">Find voting places near you on map.vote.nz ${ic('ext', 'i--xs ext')}</a></div>
          <div class="plan__q"><label for="pq-who"><span class="plan__lbl">Who with</span></label><input class="input" id="pq-who" type="text" maxlength="60" autocomplete="off" placeholder="On my own, or a name" value="${esc(p.withWho || '')}"></div>
          <div class="row"><button class="btn btn--primary" type="button" id="pl-ics">${ic('caladd', 'i--s')} Add to calendar</button><a class="btn" id="pl-sms" href="sms:?&body=${encodeURIComponent(txt)}">${ic('msg', 'i--s')} Text it</a><a class="btn btn--quiet" id="pl-wa" href="https://wa.me/?text=${encodeURIComponent(txt)}" target="_blank" rel="noopener">WhatsApp</a><button class="btn btn--quiet" type="button" id="pl-copy">${ic('share', 'i--s')} Copy</button></div>
          <p class="small soft" id="pl-text" aria-live="polite">${esc(txt)}</p>
        </div>
        <div class="stack"><p class="lede">Three choices: a day, a time and a place. Going with someone helps too.</p>
          <p class="small muted">You can vote at any voting place in New Zealand. No ID needed; your EasyVote card makes it quicker if you have it.</p></div>
      </div>`}
      ${voteFoot()}`;
    if (closed) return;
    const on = root.querySelector('[data-day][aria-pressed="true"]'); if (on) { const row = on.parentElement; row.scrollLeft = Math.max(0, on.offsetLeft - row.offsetLeft - 8) }
    root.querySelectorAll('[data-day]').forEach(b => b.onclick = () => { p.day = b.dataset.day; save(); draw(); const n = root.querySelector(`[data-day="${p.day}"]`); if (n) n.focus({ preventScroll: true }) });
    root.querySelectorAll('[data-slot]').forEach(b => b.onclick = () => { p.slot = b.dataset.slot; save(); draw(); const n = root.querySelector(`[data-slot="${p.slot}"]`); if (n) n.focus({ preventScroll: true }) });
    const upd = () => { const t = planText(p, days); $('#pl-text').textContent = t; $('#pl-sms').href = 'sms:?&body=' + encodeURIComponent(t); $('#pl-wa').href = 'https://wa.me/?text=' + encodeURIComponent(t) };
    $('#pq-where').oninput = e => { p.where = e.target.value.trim(); save(); upd() };
    $('#pq-who').oninput = e => { p.withWho = e.target.value.trim(); save(); upd() };
    $('#pl-ics').onclick = () => { const ics = planICS(p, days); if (!ics) return; const url = URL.createObjectURL(new Blob([ics], { type: 'text/calendar;charset=utf-8' }));
      const a = document.createElement('a'); a.href = url; a.download = 'voting-plan.ics'; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 4000) };
    $('#pl-copy').onclick = async () => { const t = planText(p, days); let ok = false; try { await navigator.clipboard.writeText(t); ok = true } catch {}
      const b = $('#pl-copy'); b.innerHTML = `${ic('check', 'i--s')} ${ok ? 'Copied' : 'Select the text below'}`; setTimeout(() => { if (document.body.contains(b)) b.innerHTML = `${ic('share', 'i--s')} Copy` }, 2200) } };
  draw();
}

/* ----- How MMP works: a contents list, then one short section per idea; the ballot illustration stays ----- */
const MMP_TOC = [['mmp-two', 'You have two votes', 'A party vote and an electorate vote.'], ['mmp-5', 'The 5% rule', 'The threshold a party needs for list seats.'],
  ['mmp-61', '61 to govern', 'Why parties form coalitions.'], ['mmp-fill', 'How the seats are filled', 'Electorates first, then party lists.'],
  ['mmp-oh', 'Overhang', 'When Parliament has more than 120 seats.'], ['mmp-ballot', 'The ballot paper', 'What you’ll see, as an illustration.']];
function voteMMP(root) {
  const sec = (id, title, body, cls = 'stack stack--s') => `<section class="${cls} mmp-sec" aria-labelledby="${id}"><div class="shead shead--quiet"><h2 id="${id}" class="h3" tabindex="-1">${title}</h2></div>${body}</section>`;
  root.innerHTML = `${voteHead('How MMP works', 'Two ticks, one Parliament.', 'New Zealand has used MMP (mixed-member proportional representation) since 1996. Here is the whole system in a few short ideas.')}
    <nav aria-labelledby="h-mmp-toc" class="stack stack--s"><h2 id="h-mmp-toc" class="eyebrow">On this page</h2>
      <ol class="rows mmp-toc" role="list">${MMP_TOC.map(([id, t, sub], i) => `<li><a class="rowlink rowlink--plain" href="#/vote/mmp" data-jump="${id}"><span><span class="rowlink__title"><span class="num muted">${i + 1}</span> ${t}</span><span class="rowlink__sub" style="display:block">${sub}</span></span>${ic('down')}</a></li>`).join('')}</ol></nav>
    ${sec('mmp-two', 'You have two votes', twoVotesHTML(), 'stack mmp-sec')}
    <div class="cols cols--2">
      ${sec('mmp-5', 'The 5% rule', `<p class="soft">A party gets its share of the 120 seats only if it wins at least 5% of the party vote, or wins at least one electorate. Party votes for parties that do neither don’t count towards any seats.</p>`)}
      ${sec('mmp-61', '61 to govern', `<p class="soft">A government needs the support of a majority of MPs: usually 61 of 120, more if there is an overhang. One party rarely gets there alone, so parties form coalitions or support agreements.</p>`)}
      ${sec('mmp-fill', 'How the seats are filled', `<p class="soft">Every electorate winner gets a seat. Each party’s remaining seats are filled from its ranked party list, so its total matches its share of the party vote (worked out with the Sainte-Laguë formula).</p>`)}
      ${sec('mmp-oh', 'Overhang', `<p class="soft">If a party wins more electorates than its party vote entitles it to, it keeps them, and Parliament has a few more than 120 seats until the next election.</p>`)}
    </div>
    <section class="stack mmp-sec" aria-labelledby="mmp-ballot"><div class="shead shead--quiet"><div class="shead__row"><h2 id="mmp-ballot" class="h3" tabindex="-1">The ballot paper</h2><span class="micro muted">Illustration only</span></div></div>
      <div class="split split--7-5">${ballotHTML()}
        <div class="stack"><p class="soft">Party vote on the left, electorate vote on the right. Tick one circle on each side, or only one side if you prefer. Made a mistake? Ask for a new paper.</p></div>
      </div></section>
    <section class="stack stack--s" aria-labelledby="h-mmp-try"><div class="shead shead--quiet"><h2 id="h-mmp-try" class="h3">Try it yourself</h2></div>
      <div class="rows">${rowlink('#/seats/calculator', 'scale', 'Try the seat calculator', 'Turn party-vote shares into seats.')}${rowlink('#/seats/coalition', 'users', 'Coalition builder', 'Add parties up to 61.')}${rowlink('#/vote/glossary', 'book', 'Glossary', 'Every MMP term in plain English.')}</div></section>
    ${voteFoot()}`;
  root.querySelector('.mmp-toc').addEventListener('click', e => { const a = e.target.closest('[data-jump]'); if (!a) return; e.preventDefault();
    const h = document.getElementById(a.dataset.jump); if (!h) return; h.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' }); h.focus({ preventScroll: true }) });
  requestAnimationFrame(startBallot);
}

/* ----- Glossary (plain English, neutral, no party names) ----- */
const GLOSSARY = [
  ['Advance voting', 'Voting before election day, at any voting place in the country. In 2026 it runs from Monday 26 October to Friday 6 November.'],
  ['Ballot paper', 'The single sheet you vote on: parties on the left for your party vote, candidates for your electorate on the right. Parties are listed alphabetically, and candidates alphabetically by surname.'],
  ['Coalition', 'An agreement between two or more parties to govern together, usually sharing ministerial jobs and an agreed programme.'],
  ['Confidence and supply', 'A deal where a party promises to support the government on confidence votes and on budgets (supply) without fully joining it. It may still hold some ministerial roles.'],
  ['Dormant roll', 'The list of people who have been taken off the main roll, usually because mail to them was returned. People on it can still vote by casting a special vote.'],
  ['EasyVote card', 'A card the Electoral Commission sends to enrolled voters. Bringing it (on paper or your phone) makes finding you on the roll faster, but it is not required.'],
  ['Electoral Commission', 'The independent Crown entity that runs New Zealand elections. Its official information is at vote.nz and 0800 36 76 56.'],
  ['Electorate', 'A geographic area that elects one MP. In 2026 there are 71: 64 general electorates and 7 Māori electorates.'],
  ['Electorate vote', 'Your tick on the right-hand side of the ballot paper. It chooses the MP for your area; the candidate with the most votes wins.'],
  ['Enrolment', 'Being on the electoral roll, which you must be to vote. In 2026 enrolment closes at midnight on Sunday 25 October, and you can’t enrol at a voting place.'],
  ['Informal vote', 'A vote where the counters can’t tell what the voter intended. It is recorded but not counted for anyone.'],
  ['List MP', 'An MP who gets a seat from their party’s ranked list rather than by winning an electorate. List seats top each party up to its share of the party vote.'],
  ['Majority', 'More than half the seats in Parliament: usually 61 of 120. In an electorate, the majority is the number of votes between the winner and the runner-up.'],
  ['Māori roll', 'People of Māori descent can choose to be on the Māori roll or the general roll. It decides which electorate you vote in; your party vote is the same either way.'],
  ['MMP', 'Mixed-member proportional representation, New Zealand’s voting system since 1996. You get two votes, and the party vote decides how many seats each party gets.'],
  ['Official result', 'The final count, including special votes, after every vote has been checked and recounted by hand. For 2026 it is due on Friday 27 November.'],
  ['Overhang', 'When a party wins more electorates than its party vote entitles it to. It keeps those seats, so Parliament has more than 120 MPs until the next election.'],
  ['Party list', 'The ranked list of candidates each party publishes. List seats are filled from the top, skipping anyone who has already won an electorate.'],
  ['Party vote', 'Your tick on the left-hand side of the ballot paper. It decides how many of the 120 seats each party gets overall.'],
  ['Preliminary result', 'The count released on election night. It leaves out special votes and can change before the official result.'],
  ['Recount', 'A fresh count that a candidate or party can ask a District Court judge for within three working days of the official result.'],
  ['Sainte-Laguë formula', 'The arithmetic used to share the seats out in proportion to the party vote among parties that pass the threshold or win an electorate.'],
  ['Special vote', 'A normal vote plus a signed declaration, used when you aren’t on the printed roll where you vote: for example if you enrolled after Writ Day, are voting outside your electorate, are overseas or are on the unpublished roll. Special votes are counted in the official result.'],
  ['Spoilt paper', 'A ballot paper you have made a mistake on. Hand it back and ask for a new one; spoilt papers are not counted.'],
  ['Threshold', 'The 5% of the party vote a party needs, unless it wins an electorate, to get list seats in proportion to its party vote.'],
  ['Unpublished roll', 'A confidential part of the roll for people whose safety could be at risk if their name and address were public. They vote with a special vote.'],
  ['Wasted vote', 'A party vote for a party that neither reaches 5% nor wins an electorate. It doesn’t count towards any party’s seats.'],
  ['Writ Day', 'The day the election is formally called. In 2026 it was 4 October; people who enrol or update their details after it cast a special vote.']];
function voteGlossary(root) {
  const slug = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  const items = GLOSSARY.slice().sort((a, b) => a[0].localeCompare(b[0], 'en-NZ'));
  const letter = t => t.normalize('NFD').charAt(0).toUpperCase();
  const groups = []; items.forEach(it => { const L = letter(it[0]); const g = groups.find(x => x.L === L); if (g) g.items.push(it); else groups.push({ L, items: [it] }) });
  root.innerHTML = `${voteHead('Glossary', 'MMP words, in plain English.', `${items.length} terms you’ll meet in election coverage, each in a sentence or two. For anything official, check vote.nz.`)}
    <div class="stack stack--s">
      <div class="input-icon gloss__find">${ic('search', 'i--s')}<input class="input" type="search" id="gl-q" placeholder="Filter the terms" aria-label="Filter the glossary" aria-describedby="gl-count" autocomplete="off"></div>
      <nav class="gloss__az" aria-label="Jump to a letter">${groups.map(g => `<a href="#/vote/glossary" data-jump="gl-${g.L}" aria-label="Terms starting with ${g.L}">${g.L}</a>`).join('')}</nav>
      <p class="micro muted" id="gl-count" role="status">${items.length} terms, A–Z</p>
    </div>
    <div class="stack stack--l" id="gl-list">${groups.map(g => `<section class="gloss__grp" aria-labelledby="gl-${g.L}"><h2 class="gloss__l" id="gl-${g.L}" tabindex="-1">${g.L}</h2>
      <dl class="gloss">${g.items.map(([t, d]) => `<div class="gloss__row" id="g-${slug(t)}" data-t="${esc((t + ' ' + d).toLowerCase())}"><dt>${esc(t)}</dt><dd>${esc(d)}</dd></div>`).join('')}</dl></section>`).join('')}</div>
    <p class="small muted" id="gl-none" hidden>No term matches. Try a shorter word.</p>
    ${voteFoot()}`;
  $('#gl-q').oninput = e => { const q = e.target.value.trim().toLowerCase(); let n = 0;
    root.querySelectorAll('.gloss__row').forEach(r => { const on = !q || r.dataset.t.includes(q); r.hidden = !on; if (on) n++ });
    root.querySelectorAll('.gloss__grp').forEach(g => { g.hidden = !g.querySelector('.gloss__row:not([hidden])') });
    $('#gl-none').hidden = n > 0; $('#gl-count').textContent = q ? (n ? `${n} term${n === 1 ? '' : 's'} match` : 'No term matches') : `${items.length} terms, A–Z` };
  root.querySelector('.gloss__az').addEventListener('click', e => { const a = e.target.closest('[data-jump]'); if (!a) return; e.preventDefault();
    const q = $('#gl-q'); if (q.value) { q.value = ''; q.dispatchEvent(new Event('input')) }
    const h = document.getElementById(a.dataset.jump); if (h) { h.scrollIntoView({ block: 'start' }); h.focus({ preventScroll: true }) } });
}

/* ----- What special votes could change ----- */
function voteSpecials(root) {
  const H = G().howtovote || {}; const secs = H.sections || [];
  const sv = secs.find(s => s.id === 'special-votes'); const af = secs.find(s => s.id === 'after');
  const pick = (sec, re) => ((sec && sec.steps) || []).filter(x => re.test(x.text));
  const what = pick(sv, /special vote is|how special votes are counted|another electorate/i);
  const changed = pick(af, /special votes have changed|^2020:|not final|official results:/i);
  const step = x => `<li><p>${esc(x.text)}</p>${x.url ? `<p class="src">${ic('doc')} ${extA(x.url, esc((x.source || x.url.replace(/^https?:\/\//, '').split('/')[0]).split(',')[0]))}</p>` : ''}</li>`;
  const notes = [].concat((sv && sv.notes) || [], (af && af.notes) || []).filter(n => /special/i.test(n));
  const steps = (list, label) => list.length ? `<details class="disclose"><summary>${label} (${list.length})</summary><div class="disclose__body"><ol class="vsteps">${list.map(step).join('')}</ol></div></details>` : '';
  root.innerHTML = `${voteHead('Special votes', 'What special votes could change.', 'The result on election night is not the final result. Special votes are counted over the following three weeks; in 2023 they were about one vote in five, and they can move seats.')}
    <div class="split split--7-5">
      <div class="stack stack--l">
        <section class="stack stack--s" aria-labelledby="h-sv1"><div class="shead"><h2 id="h-sv1">What a special vote is</h2></div>
          <p class="soft">A special vote is an ordinary vote with a signed declaration attached. People cast one when they aren’t on the printed roll where they vote, for example because they enrolled late, voted outside their electorate or voted from overseas. Each declaration is checked before the vote is counted.</p>
          ${steps(what, 'How they are cast and counted')}</section>
        <section class="stack stack--s" aria-labelledby="h-sv2"><div class="shead"><h2 id="h-sv2">What they have changed before</h2></div>
          <p class="soft">Because special votes are counted last, the official result can differ from election night: a party can gain or lose a seat or two, close electorates can change hands, and the numbers a government needs can shift.</p>
          ${steps(changed, 'Past elections and the official result')}</section>
      </div>
      <aside class="stack sticky" aria-labelledby="h-sv-dates">
        <div class="panel"><h2 class="h3" id="h-sv-dates">Dates</h2><dl class="dl"><dt>Election night</dt><dd>Sat 7 Nov, from 7pm: preliminary results</dd><dt>Specials arrive</dt><dd>Up to 10 days after election day</dd><dt>Official result</dt><dd>Fri 27 Nov 2026</dd></dl>
          ${vExt('https://electionresults.govt.nz', 'Official results site', 'btn btn--s')}</div>
        ${notes.length ? `<div class="stack stack--s">${notes.map(n => `<p class="small muted">${esc(n)}</p>`).join('')}</div>` : ''}
        <div class="rows">${rowlink('#/vote/dates', 'clock', 'Key dates', 'Every date in the 2026 election.')}${rowlink('#/vote/glossary', 'book', 'Glossary', 'Preliminary, official, special and more.')}${rowlink('#/vote/mmp', 'scale', 'How MMP works', 'Why a few votes can move a seat.')}</div>
      </aside>
    </div>
    ${H.as_of ? `<p class="src">${ic('shield')} Checked ${esc(H.as_of)} against vote.nz and elections.nz.</p>` : ''}
    ${voteFoot()}`;
}
