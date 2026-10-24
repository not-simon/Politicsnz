// What Parliament's record says the MP's party is at the end of the term (party_changes applied); falls back to the electorate data.
function mpPartyLabel(mp) { if (!mp) return ''; const parl = (S.data.parliaments || []).slice(-1)[0]; const m = parl && (parl.members || []).find(x => x.name === mp.name);
  const party = m ? ((m.party_changes || []).length ? m.party_changes[m.party_changes.length - 1].to || m.party : m.party) : mp.party;
  const pn = p => esc(S.data.parties[p] ? pname(p) : p);
  if (party === 'independent' && mp.party && mp.party !== 'independent') return `independent in Parliament's records; leads the ${pn(mp.party)}`;
  return pn(party) }
/* ===== Vote › Māori electorates (#/vote/maori) and Other languages (#/vote/lang, #/vote/lang/mi|sm|to) =====
   Te reo Māori terms come from data/guide/i18n.json (each with its source); the Samoan and Tongan pages from
   data/guide/howtovote-sm.json / -to.json, where every line says whether it is the Electoral Commission's own wording
   ('ec') or our machine-assisted translation ('mt'). Te reo first, then English. Every non-English run carries a lang attribute. */
const LANG_FILES = { i18n: 'data/guide/i18n.json', sm: 'data/guide/howtovote-sm.json', to: 'data/guide/howtovote-to.json' };
async function langData(k) { S.langData = S.langData || {};
  if (!(k in S.langData)) S.langData[k] = await getJSON(LANG_FILES[k]).catch(() => null);
  return S.langData[k] }
// te reo term for an English key in a group of i18n.json (null when flagged)
function miTerm(I, group, key) { const g = ((I && I.groups) || []).find(x => x.id === group); const t = g && g.terms.find(x => x.key === key); return t && t.mi || null }
const inLang = (code, txt) => `<span lang="${code}">${esc(txt)}</span>`;
const biText = (code, xx, en) => xx ? `${inLang(code, xx)} · ${esc(en)}` : esc(en);
const LANG_OFFICIAL_NOTE = `<p class="note">${ic('phone', 'i--s')}<span>Official information comes from the Electoral Commission: <a href="https://vote.nz" target="_blank" rel="noopener">vote.nz</a> or 0800 36 76 56 (free, 24 hours). Ask for an interpreter in your language on the same number. Ballot Book NZ is an independent guide, not the Commission.</span></p>`;
const langFoot = () => `<div class="stack stack--s">${LANG_OFFICIAL_NOTE}<div class="micro notec">${NOT_EC}</div></div>`;
const srcRow = links => { const L = (links || []).filter(x => x && x[0] && x[1]); return L.length ? `<p class="src src--line">${ic('doc')}<span>${L.map(([u, l]) => extA(u, esc(l))).join(' · ')}</span></p>` : '' };
const MH = {   // vote.nz / elections.nz pages behind each claim on the Māori electorates page (checked 24 Oct 2026)
  roll: 'https://vote.nz/enrolling/get-ready-to-enrol/maori-roll-or-general-roll',
  choice: 'https://vote.nz/maori-enrolment/about-the-option/about/what-does-your-choice-mean-for-you',
  option: 'https://vote.nz/maori-enrolment/about-the-option/about/what-is-the-maori-electoral-option',
  changed: 'https://vote.nz/maori-enrolment/resources/resources/whats-changed',
  history: 'https://vote.nz/maori-enrolment/resources/resources/history-of-the-maori-electoral-option',
  stats: 'https://vote.nz/maori-enrolment/resources/resources/statistics',
  keydates: 'https://vote.nz/2026-general-election/about/overview/key-dates',
  check: 'https://vote.nz/maori-enrolment/enrol-check-or-change-rolls/enrol-check-change/how-to-make-your-choice',
  glossary: 'https://vote.nz/2026-general-election/resources/glossary',
  count: 'https://elections.nz/democracy-in-nz/what-are-electorates/working-out-how-many-electorates-there-should-be',
  review: 'https://elections.nz/democracy-in-nz/historical-events/boundary-review-2025',
  whattodo: 'https://vote.nz/2026-general-election/voting-in-the-election/what-to-do',
  whare: 'https://vote.nz/2026-general-election/voting-in-the-election/find-a-voting-place/whare-poti-maori',
  tereo: 'https://vote.nz/2026-general-election/resources/information-in-te-reo-maori' };

/* ----- Māori electorates hub -----
   Te reo headings are the Electoral Commission's own (vote.nz te reo pages and the bilingual 'Get ready' leaflet); see data/guide/i18n.json. */
function maoriSeatHTML(e, r) {
  const cands = (e.candidates || []).slice().sort(ballotSort); const mp = e.sitting_mp;
  const pn = p => esc(S.data.parties[p] ? pname(p) : p);
  // every field is guarded: a missing winner, party, majority or runner-up drops that part, and the source line only appears when there is a result and a source
  const tag = p => p ? ` <span class="ptag ptag--s" style="--pc:${pcolor(p)}"><span class="sw"></span>${pn(p)}</span>` : '';
  const maj = r && typeof r.majority === 'number' && r.majority > 0 ? ` by ${Number(r.majority).toLocaleString('en-NZ')} votes` : '';
  const res = r && r.winner ? `<p class="small"><b>2023:</b> ${esc(r.winner)}${tag(r.party)} won${maj}${r.runner_up ? ` over ${esc(r.runner_up)}${tag(r.runner_up_party)}` : ''}.</p>` : '<p class="small muted">2023 result not available.</p>';
  const srcU = r && r.winner ? ((e.result_2023 && e.result_2023.source) || String(r.majority_source || '').match(/https?:\/\/\S+/)?.[0] || '') : '';
  const resSrc = srcU ? `<p class="src src--line">${ic('doc')}<span>2023 result: official count, as reported by ${extA(srcU, esc(srcU.replace(/^https?:\/\/(www\.)?/, '').split('/')[0]))}</span></p>` : '';
  const now = mp ? `<p class="small soft"><b>MP now:</b> ${esc(mp.name)} (${mpPartyLabel(mp)})${e.mp_standing_again === false ? ', not standing again' : ''}.${e.sitting_mp_note ? ` ${esc(e.sitting_mp_note)}` : ''}</p>` : '';
  return `<section class="stack stack--s mh-seat" aria-labelledby="mh-${esc(e.slug)}">
      <div class="shead shead--quiet"><div class="shead__row"><h3 id="mh-${esc(e.slug)}" class="h4">${inLang('mi', e.name)}</h3><span class="micro muted">${esc(String(e.region || '').replace(/\s*\(Māori electorate\)\s*/i, ''))}</span></div></div>
      ${res}${resSrc}${now}
      <div class="shead__row"><span class="small"><b>On the ballot: ${cands.length}</b></span><span class="micro muted">A–Z by surname</span></div>
      ${cands.length ? `<ul class="cands" role="list">${cands.map(candRow).join('')}</ul>` : '<p class="small muted">The candidate list is still being checked.</p>'}
      <div class="row"><a class="btn btn--s" href="#/vote/electorate/${esc(e.slug)}">${ic('pin', 'i--s')} ${esc(e.name)} electorate page</a><a class="btn btn--s btn--quiet" href="#/seats/map/2023/${esc(e.slug)}">${ic('map', 'i--s')} On the map</a></div>
    </section>` }

function maoriSeatRow(e, r) { const mp = e.sitting_mp; const pn = p => esc(S.data.parties[p] ? pname(p) : p);
  const by = r && typeof r.majority === 'number' && r.majority > 0 ? ` by ${Number(r.majority).toLocaleString('en-NZ')}` : '';
  const who = (n, p) => n ? `${esc(n)}${p ? ` (${pn(p)})` : ''}` : '';
  const same = mp && mp.name && r && r.winner && elSlug(mp.name) === elSlug(r.winner) && mp.party === r.party;
  const line = same ? `MP: ${who(mp.name, mp.party)}, won 2023${by}` : [mp && mp.name ? `MP: ${who(mp.name, mp.party)}` : '', r && r.winner ? `2023: ${who(r.winner, r.party)}${by}` : ''].filter(Boolean).join(' · ');
  return `<button class="rowlink rowlink--plain" type="button" data-seat="${esc(e.slug)}" aria-haspopup="dialog"><span><span class="rowlink__title"><span lang="mi">${esc(e.name)}</span> <span class="micro muted">${esc(String(e.region || '').replace(/\s*\(Māori electorate\)\s*/i, ''))}</span></span><span class="rowlink__sub" style="display:block">${line}</span></span>${ic('chev')}</button>` }

V.maoriHub = async arg => {
  $('#main').innerHTML = sectionFrame('vote', 'vote/maori', `<div class="stack stack--xl" id="mh-body"><p class="small muted">Loading…</p></div>`);
  await loadPeople(); const I = await langData('i18n'); const t = k => miTerm(I, 'labels', k);
  const E = (S.data.electorates || []).filter(e => e.type === 'maori').sort((a, b) => a.name.localeCompare(b.name, 'en-NZ'));
  const el23 = ((S.data.elections || []).find(x => x.year === 2023) || {}).electorates || [];
  const r23 = e => el23.find(r => elSlug(r.name) === elSlug(e.name)) || null;
  const term = (k, en) => { const m = t(k); return m ? `${esc(en)} (<i lang="mi">${esc(m)}</i>)` : esc(en) };
  const dis = (mi, en, body, src, open) => `<details class="disclose"${open ? ' open' : ''}><summary><span>${biText('mi', mi, en)}</span></summary><div class="disclose__body stack stack--s">${body}${srcRow(src)}</div></details>`;
  $('#mh-body').innerHTML = `
    <header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('vote', 'i--s')} Vote · Māori electorates</p>
      <h1>${inLang('mi', miTerm(I, 'vote_pages', 'vote/maori') || 'Ngā rohe pōti Māori')} · Māori electorates</h1>
      <p class="lede">Seven of the 71 electorates are Māori electorates. If you’re on the Māori roll, your electorate vote is for a candidate in one of them. Everyone’s party vote is the same, whichever roll they’re on.</p></header>
    <div class="callout callout--signal"><p><b>Your roll is fixed for this election.</b> The last day to change between the Māori roll and the general roll was midnight, 6 August 2026. Not sure which roll you’re on? <a href="${MH.check}" target="_blank" rel="noopener">Check at vote.nz</a> or call 0800 36 76 56.</p></div>
    <section class="stack" aria-labelledby="mh-how">
      <div class="shead"><h2 id="mh-how">${biText('mi', 'Te rārangi Māori', 'How the Māori roll works')}</h2></div>
      <div class="stack stack--s"><h3 class="h4">${biText('mi', 'Te rārangi Māori, te rārangi whānui', 'The Māori roll and the general roll')}</h3>
          <p>There are two electoral rolls. On the ${term('maori_roll', 'Māori roll')} you vote for a candidate in a Māori electorate; on the ${term('general_roll', 'general roll')} you vote for a candidate in a general electorate. Your roll decides which electorate candidates you can choose from.</p>
           <p>You vote for the same list of parties whichever roll you’re on. The Electoral Commission says of the choice: “There is no right or wrong.”</p>
          ${srcRow([[MH.roll, 'vote.nz: Māori roll or general roll?'], [MH.choice, 'vote.nz: What does your choice mean for you?']])}</div>
      <div>
        ${dis('Ko te rēhita hei kaipōti mēnā he Māori koe', 'Enrolling if you are Māori: who can be on the Māori roll',
          `<p>If you are of New Zealand Māori descent, you can choose to enrol on the Māori roll or the general roll. You make the choice when you first enrol.</p>
           <p>This has been the rule since the Electoral Amendment Act 1975, which defined a Māori as a person of New Zealand Māori descent. Everyone else enrols on the general roll.</p>`,
          [[MH.glossary, 'vote.nz glossary: Māori roll'], [MH.history, 'vote.nz: History of the Māori Electoral Option']])}
        ${dis('Te Kōwhiringa Pōti Māori', 'The Māori Electoral Option',
          `<p>The Māori Electoral Option is the choice between the two rolls. Since 31 March 2023, Māori who are enrolled can change roll at any time, except in the 3 months before a general election, in the 3 months before the three-yearly local elections, and before a by-election if the change would move them into that electorate. Before then, people could only change during an Option period every 5 or 6 years.</p>
           <p>For the 2026 election the last day to change was <b>midnight, 6 August 2026</b>, so the roll you are on now is the roll you vote on. Between 31 March and 6 August 2026, 9,400 people moved from the general roll to the Māori roll and 7,633 moved the other way; 7,723 new enrolments went on the Māori roll and 3,549 on the general roll (Electoral Commission figures).</p>`,
          [[MH.option, 'vote.nz: What is the Māori Electoral Option?'], [MH.changed, 'vote.nz: Changes to the Option'], [MH.keydates, 'vote.nz: Key dates'], [MH.stats, 'vote.nz: Statistics']])}
        ${dis('Te whakatau i te maha o ngā rohe pōti Māori me ngā rohe pōti whānui', 'How the number of Māori electorates is set',
          `<p>After each census, the Government Statistician works out how many Māori and general electorates there should be, using the census and the number of Māori on the Māori roll and on the general roll. The formula and dates are set out in the Electoral Act 1993. ${term('representation_commission', 'The Representation Commission')} then draws the boundaries.</p>
           <p>For 2026 the calculation was made in 2024 from the 2023 Census and the rolls at 1 April 2024. The number of Māori electorates stayed at 7, with a population quota of 74,367 people each (South Island general electorates: 70,037; North Island: 69,875). The new boundaries were released on 8 August 2025.</p>`,
          [[MH.count, 'elections.nz: Working out how many electorates there should be'], [MH.review, 'elections.nz: Boundary Review 2025'], [MH.changed, 'vote.nz: Changes to the Option']])}
        ${dis('Me pēwhea te pōti', 'How to vote',
          `<p>Everyone gets the same two votes: a ${term('party_vote', 'party vote')} for a party, and an ${term('electorate_vote', 'electorate vote')} for a candidate. On the Māori roll, your electorate vote is for a candidate standing in your Māori electorate.</p>
           <p>You can vote at any voting place. More than 220 are <i lang="mi">Whare Pōti Māori</i>, places recommended by communities for their significance to local Māori, including many marae, kura and wānanga. 67 of them are <i lang="mi">reo rua</i> (bilingual), where you can vote in te reo Māori, English or both. Whare Pōti Māori are open to every voter, on either roll.</p>
           <div class="row">${vExt('https://map.vote.nz/voting-places/whare', 'Find Whare Pōti Māori')}${vExt('https://map.vote.nz/voting-places/maori', 'Reo rua voting places', 'btn btn--s btn--quiet')}<a class="btn btn--s btn--quiet" href="#/vote/lang/mi">Voting steps in te reo Māori</a></div>`,
          [[MH.whattodo, 'vote.nz: What to do'], [MH.whare, 'vote.nz: Whare Pōti Māori'], [MH.tereo, 'vote.nz: Information in te reo Māori']])}
      </div>
    </section>
    <section class="stack" aria-labelledby="mh-seats">
      <div class="shead"><div class="shead__row"><h2 id="mh-seats">${inLang('mi', 'Ngā rohe pōti Māori e 7')} · The 7 Māori electorates</h2><span class="micro muted">A–Z</span></div></div>
      <p class="small soft">Tap one for its candidates (A–Z by surname), the 2023 result and links. Boundaries changed in 2025.</p>
      <div class="rows" id="mh-list">${E.map(e => maoriSeatRow(e, r23(e))).join('')}</div>
      <p class="src src--line">${ic('doc')}<span>Candidates: policy.nz and party lists (official list: EasyVote card, vote.nz).${E.some(e => (r23(e) || {}).winner) ? ` 2023 results: the ${extA('https://electionresults.govt.nz', 'official count')}, as reported.` : ''} Checked 24 Oct 2026.</span></p>
      <div class="row"><a class="btn btn--s btn--quiet" href="#/vote/electorate">${ic('pin', 'i--s')} Find your electorate</a><a class="btn btn--s btn--quiet" href="#/seats/map">${ic('map', 'i--s')} Electorate map</a><a class="btn btn--s btn--quiet" href="#/vote/mmp">${ic('scale', 'i--s')} How MMP works</a></div>
    </section>
    ${voteFoot()}`;
  const openSeat = slug => { const e = E.find(x => x.slug === slug); if (!e) return;
    openSheet({ title: e.name, depth: ['Vote', 'Māori electorates', e.name], at: 2, src: `Candidates from policy.nz and party lists; the official list is on your EasyVote card and at vote.nz.${(r23(e) || {}).winner ? ' 2023: Electoral Commission official count, as reported.' : ''}`, html: maoriSeatHTML(e, r23(e)) });
    const box = $('#sheet-body .mh-seat'); if (box) box.addEventListener('click', ev => { const b = ev.target.closest('[data-cand]'); if (!b) return; const p = findPerson(b.dataset.cand, b.dataset.cname); if (p) openPerson(p);
      else openSheet({ title: b.dataset.cname, html: '<p class="small muted">We don’t have a profile for this candidate yet. Their party’s website, policy.nz and vote.nz list the candidates standing.</p>' }) }) };
  $('#mh-list').addEventListener('click', ev => { const b = ev.target.closest('[data-seat]'); if (b) openSeat(b.dataset.seat) });
  if (arg && E.some(x => x.slug === arg)) openSeat(arg);   // #/vote/maori/<slug> opens that electorate
};

/* ----- Other languages ----- */
const EC_LANGS = 'Arabic, Burmese, Chinese (Simplified and Traditional), Cook Islands Māori, Farsi, Fijian, French, Gujarati, Hindi, Japanese, Khmer, Kiribati, Korean, Malay, Niuean, Punjabi, Rotuman, Russian, Samoan, Somali, Spanish, Tagalog, Tamil, Thai, Tokelauan, Tongan, Tuvaluan and Vietnamese';
const EC_LANG_PAGE = 'https://vote.nz/2026-general-election/resources/information-in-multiple-languages';
V.voteLang = async code => {
  const fn = { mi: langMaori, sm: langPacific, to: langPacific }[code];
  $('#main').innerHTML = sectionFrame('vote', 'vote/lang', `<div class="stack stack--xl" id="lang-body"><p class="small muted">Loading…</p></div>`);
  const root = $('#lang-body');
  if (fn) await fn(root, code); else await langIndex(root);
};
const langHead = (crumb, h1, lede) => `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('vote', 'i--s')} Vote · <a href="#/vote/lang">Other languages</a>${crumb ? ' · ' + crumb : ''}</p><h1>${h1}</h1>${lede ? `<p class="lede">${lede}</p>` : ''}</header>`;

async function langIndex(root) {
  const I = await langData('i18n'); const sub = miTerm(I, 'vote_pages', 'vote/lang');
  root.innerHTML = `<header class="pagehead"><p class="eyebrow eyebrow--signal">${ic('vote', 'i--s')} Vote · Other languages</p>
      <h1>${sub ? `${inLang('mi', sub)} · ` : ''}How to vote in your language</h1>
      <p class="lede">The voting steps in te reo Māori, gagana Sāmoa and lea faka-Tonga, each beside the English, with links to the Electoral Commission’s own translated guides.</p></header>
    <div class="rows">
      ${rowlink('#/vote/lang/mi', 'book', `${inLang('mi', 'Te reo Māori')}`, `${inLang('mi', 'Te pōti ki te Pōtitanga Whānui 2026')} · in the Electoral Commission’s own te reo`)}
      ${rowlink('#/vote/lang/sm', 'book', `${inLang('sm', 'Gagana Sāmoa')} <span class="muted">· Samoan</span>`, `${inLang('sm', 'Faapefea ona palota')} · How to vote`)}
      ${rowlink('#/vote/lang/to', 'book', `${inLang('to', 'Lea faka-Tonga')} <span class="muted">· Tongan</span>`, `${inLang('to', 'Ko e founga fili')} · How to vote`)}
    </div>
    <section class="stack stack--s" aria-labelledby="h-otherl"><div class="shead shead--quiet"><h2 id="h-otherl" class="h3">Other languages</h2></div>
      <p class="soft">The Electoral Commission publishes its voting guides in ${EC_LANGS}, as well as te reo Māori, New Zealand Sign Language, Easy Read, large print, audio and braille.</p>
      <p class="soft">To talk to the Commission in another language, call <b>0800 36 76 56</b> (free) and say which language you’d like: they will connect you with an interpreter.</p>
      <div class="row">${vExt(EC_LANG_PAGE, 'Guides in your language', 'btn btn--s btn--ink')}${vExt('https://vote.nz/2026-general-election/resources/information-in-accessible-formats', 'Accessible formats', 'btn btn--s btn--quiet')}</div>
      ${srcRow([[EC_LANG_PAGE, 'vote.nz: Information in multiple languages']])}</section>
    ${langFoot()}`;
}

async function langMaori(root) {
  const I = await langData('i18n'); const P = I && I.page_mi;
  if (!P) { root.innerHTML = `${langHead('Te reo Māori', 'Te reo Māori', '')}<p class="note">${ic('info', 'i--s')}<span>This page didn’t load. The Electoral Commission’s te reo Māori material is at ${extA(MH.tereo, 'vote.nz')}.</span></p>${langFoot()}`; return }
  const srcs = I.sources || {};
  const step = (s, i) => `<li class="lp-step"><h2 class="h4" id="lm-${i}">${biText('mi', s.h.mi, s.h.en)}</h2>
      ${s.mi.map((m, j) => `<p lang="mi" class="lp__xx">${esc(m)}</p><p class="lp__en small soft">${esc(s.en[j] || '')}</p>`).join('')}
      <div class="row">${vExt(s.url, /map\.vote/.test(s.url) ? 'Find a voting place' : 'vote.nz', 'btn btn--s btn--quiet')}${(s.more || []).map(m => vExt(m.url, `<span lang="mi">${esc(m.label)}</span>`, 'btn btn--s btn--quiet')).join('')}</div></li>`;
  const STATUS = { official: 'Electoral Commission term', adapted: 'From Commission wording', dictionary: 'Te Aka Māori Dictionary', flagged: 'Not found: English kept' };
  const terms = (I.groups || []).map(g => `<h3 class="h4">${esc(g.title)}</h3><dl class="gloss lp-terms">${g.terms.map(t => `<div class="gloss__row"><dt>${t.mi ? inLang('mi', t.mi) : '<span class="muted">(English kept)</span>'}</dt><dd><span>${esc(t.en)}</span> <span class="badge${t.status === 'flagged' ? ' badge--outline' : ''}">${esc(STATUS[t.status] || t.status)}</span><span class="micro muted lp-ev">${esc(t.evidence || t.note || '')} ${(t.sources || []).map(k => srcs[k] ? extA(srcs[k].url, 'source', 'micro muted') : '').join(' ')}</span></dd></div>`).join('')}</dl>`).join('');
  root.innerHTML = `${langHead(inLang('mi', 'Te reo Māori'), `${inLang('mi', P.title.mi)} <span class="lp-h1-en">${esc(P.title.en)}</span>`, '')}
    <p class="note">${ic('info', 'i--s')}<span>Every te reo Māori sentence on this page is quoted from the Electoral Commission’s te reo pages and leaflets, beside the Commission’s own English. Not checked by a fluent speaker; the official vote.nz pages are authoritative. ${extA(MH.tereo, 'The Commission’s te reo guides')}.</span></p>
    <ol class="lp-steps" aria-label="Voting steps">${P.steps.map(step).join('')}</ol>
    <section class="stack stack--s" aria-labelledby="lm-more"><div class="shead shead--quiet"><h2 id="lm-more" class="h3">${biText('mi', P.more.mi, P.more.en)}</h2></div>
      <ul class="lp-list">${P.more.items.map(x => `<li><a href="${esc(x.url)}"${/^https/.test(x.url) ? ' target="_blank" rel="noopener"' : ''}>${inLang('mi', x.mi)}</a> · ${esc(x.en)}</li>`).join('')}</ul>
      <div class="row"><a class="btn btn--s btn--quiet" href="#/vote/maori">${ic('pin', 'i--s')} <span lang="mi">Ngā rohe pōti Māori</span> · Māori electorates</a></div></section>
    <details class="disclose"><summary>The te reo Māori terms this guide uses, and where each comes from</summary><div class="disclose__body stack stack--s">
      <p class="small soft">Checked ${esc(I.as_of === '2026-10-24' ? '24 October 2026' : I.as_of || '')}. Where we found no established term we kept the English rather than make one up. Corrections from fluent speakers are welcome.</p>${terms}
      ${(I.not_reached || []).length ? `<p class="micro muted">Could not be reached to check: ${I.not_reached.map(esc).join(' ')}</p>` : ''}</div></details>
    ${langFoot()}`;
}

async function langPacific(root, code) {
  const D = await langData(code); const names = { sm: ['Gagana Sāmoa', 'Samoan'], to: ['Lea faka-Tonga', 'Tongan'] }[code];
  if (!D) { root.innerHTML = `${langHead(names[1], names[1], '')}<p class="note">${ic('info', 'i--s')}<span>This page didn’t load. The Electoral Commission’s ${names[1]} guides are at ${extA(EC_LANG_PAGE, 'vote.nz')}.</span></p>${langFoot()}`; return }
  const X = t => `<span lang="${code}">${esc(t)}</span>`;
  const BL = D.basis_labels || {}; const bl = b => (BL[b] || {}).en || (b === 'ec' ? 'Electoral Commission wording' : 'Our translation');
  const pair = x => `<p lang="${code}" class="lp__xx">${esc(x.xx)}</p><p class="lp__en small soft">${esc(x.en)}</p>`;
  const meta = x => `<p class="micro muted lp-meta"><span class="lp-basis lp-basis--${esc(x.basis)}">${esc(bl(x.basis))}</span>${x.url ? ` · ${/^tel:/.test(x.url) ? `<a href="${esc(x.url)}">Call</a>` : extA(x.url, 'Official page')}` : ''}</p>`;
  const item = x => `<li class="lp-item">${pair(x)}${meta(x)}</li>`;
  const today = nzToday().iso;
  const sec = (s, open) => `<details class="disclose"${open ? ' open' : ''}><summary><span>${X(s.h.xx)} <span class="lp-sum-en">· ${esc(s.h.en)}</span></span></summary><div class="disclose__body">
      <${s.steps ? 'ol' : 'ul'} class="lp-list lp-list--items${s.steps ? ' lp-list--num' : ''}">${s.items.map(item).join('')}</${s.steps ? 'ol' : 'ul'}></div></details>`;
  const off = D.official || [];
  root.innerHTML = `${langHead(X(names[0]), `${X(D.title.xx)} <span class="lp-h1-en">${esc(D.title.en)}</span>`, `${X(D.lede.xx)}<br><span class="small">${esc(D.lede.en)}</span>`)}
    <div class="note note--warn" role="note">${ic('flag', 'i--s')}<div class="stack stack--s"><p lang="${code}"><b>${esc(D.disclaimer.xx)}</b></p><p><b>${esc(D.disclaimer.en)}</b></p></div></div>
    <section class="panel" aria-labelledby="lp-off">
      <h2 id="lp-off" class="h3">The Electoral Commission’s own ${esc(names[1])} guides</h2>
      <p class="small soft">These are the official translations. Where they differ from this page, follow them.</p>
      <div class="rows">${off.map(r => `<a class="rowlink rowlink--plain" href="${esc(r.url)}" target="_blank" rel="noopener"><span><span class="rowlink__title">${r.title ? X(r.title) : esc(r.title_en)}</span><span class="rowlink__sub" style="display:block">${r.title ? esc(r.title_en) : 'In ' + esc(names[1])} · ${esc(r.size || 'PDF')}</span></span>${ic('ext')}</a>`).join('')}</div>
      <p class="small" lang="${code}">${esc(D.interpreter.xx)}</p><p class="small soft">${esc(D.interpreter.en)}</p>
      <div class="row">${vExt(EC_LANG_PAGE, 'All languages at vote.nz', 'btn btn--s btn--ink')}<a class="btn btn--s btn--quiet" href="tel:0800367656">${ic('phone', 'i--s')} 0800 36 76 56</a></div>
    </section>
    <p class="small muted">Each line below is in ${esc(names[1])} with the English under it, and says whether it is the <b>${esc(bl('ec'))}</b> (quoted from the Commission’s ${esc(names[1])} guide) or <b>${esc(bl('mt'))}</b> (machine-assisted, not yet checked).</p>
    <section class="stack stack--s" aria-labelledby="lp-chk"><div class="shead"><h2 id="lp-chk">Checklist</h2></div>
      <ol class="lp-list lp-list--items lp-list--num">${(D.checklist || []).map(item).join('')}</ol></section>
    <section class="stack stack--s" aria-labelledby="lp-more"><div class="shead"><h2 id="lp-more">The details</h2></div>
      <div>${(D.sections || []).map((s, i) => sec(s, s.id === 'how')).join('')}</div></section>
    <section class="stack stack--s" aria-labelledby="lp-kd"><div class="shead shead--quiet"><h2 id="lp-kd" class="h3">Key dates</h2></div>
      <ul class="vdates lp-dates">${(D.key_dates || []).map(k => `<li${k.date === '2026-11-07' ? ' class="is-eday"' : ''}><span class="num">${shortDate(k.date)}${k.date < today ? '<span class="micro muted lp-past">passed</span>' : ''}</span><span>${pair(k)}${meta(k)}</span></li>`).join('')}</ul></section>
    <section class="stack stack--s" aria-labelledby="lp-help"><div class="shead shead--quiet"><h2 id="lp-help" class="h3">${X(D.contacts.h.xx)} · ${esc(D.contacts.h.en)}</h2></div>
      <ul class="lp-list lp-list--items">${D.contacts.items.map(item).join('')}</ul></section>
    <p class="src">${ic('shield')} Checked ${esc(D.as_of === '2026-10-24' ? '24 October 2026' : D.as_of || '')} against the Electoral Commission’s ${esc(names[1])} and English guides. <button class="linkbtn" type="button" data-page="guide/how-to-vote-${code}.md">Readable copy and translation notes</button></p>
    ${langFoot()}`;
}
