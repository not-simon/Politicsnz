/* Mockup behaviour only: theme toggle, segmented controls, chips, likert, scrubber play, swipe, sheet.
   The production app implements these inside its views; see PORTING.md. */
(() => {
  const root = document.documentElement;
  const store = { get(k) { try { return localStorage.getItem(k) } catch { return null } }, set(k, v) { try { localStorage.setItem(k, v) } catch {} } };
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.addEventListener('click', e => {
    const t = e.target.closest('[data-theme-toggle]');
    if (t) { const dark = root.dataset.theme === 'dark' || (!root.dataset.theme && matchMedia('(prefers-color-scheme: dark)').matches); root.dataset.theme = dark ? 'light' : 'dark'; store.set('bb-theme', root.dataset.theme); return }
    const sb = e.target.closest('.seg > button, .persona > button');
    if (sb) { sb.parentElement.querySelectorAll(':scope > button').forEach(b => b.setAttribute('aria-pressed', String(b === sb))); return }
    const ch = e.target.closest('.chip[aria-pressed]');
    if (ch) { ch.setAttribute('aria-pressed', String(ch.getAttribute('aria-pressed') !== 'true')); return }
    const lk = e.target.closest('.likert__opt');
    if (lk) { lk.parentElement.querySelectorAll('.likert__opt').forEach(b => b.setAttribute('aria-checked', String(b === lk))); return }
    const so = e.target.closest('[data-sheet-open]');
    if (so) { const d = document.getElementById(so.dataset.sheetOpen); if (d && d.showModal) d.showModal(); return }
    const sc = e.target.closest('[data-sheet-close]');
    if (sc) { sc.closest('dialog').close(); return }
    const sw = e.target.closest('[data-swipe]');
    if (sw) { const card = document.querySelector('.deck .scard:not(.scard--behind):not(.scard--behind2)'); if (!card) return;
      const dir = sw.dataset.swipe === 'agree' ? 1 : sw.dataset.swipe === 'disagree' ? -1 : 0;
      card.style.transition = 'transform var(--dur-3) var(--ease-out), opacity var(--dur-3)';
      card.style.transform = dir ? `translateX(${dir * 120}%) rotate(${dir * 14}deg)` : 'translateY(-30px) scale(.96)'; card.style.opacity = '0';
      setTimeout(() => { card.style.transition = 'none'; card.style.transform = ''; card.style.opacity = ''; requestAnimationFrame(() => card.style.transition = '') }, reduce ? 10 : 420);
      return }
  });

  /* Scrubbers: range input + play button stepping through years */
  document.querySelectorAll('.scrubber').forEach(s => {
    const range = s.querySelector('.range'), yearEl = s.querySelector('.scrubber__year'), stops = [...s.querySelectorAll('.scrubber__stops span')], play = s.querySelector('.scrubber__play');
    const years = stops.map(x => x.textContent.trim());
    const set = i => { range.value = i; range.style.setProperty('--fill', (i / (years.length - 1) * 100) + '%');
      stops.forEach((x, j) => x.setAttribute('aria-current', String(j === +i)));
      yearEl.innerHTML = `<span>${years[i]}</span>`;
      document.querySelectorAll('.nzmap path[data-fill-2023]').forEach(p => { const f = p.dataset['fill' + years[i]] || p.getAttribute('data-fill-' + years[i]); if (f !== undefined) p.style.fill = f || 'var(--seat-empty)' });
      const lbl = document.querySelector('[data-year-label]'); if (lbl) lbl.textContent = years[i] };
    range.addEventListener('input', () => set(+range.value));
    set(+range.value);
    let timer = null;
    play.addEventListener('click', () => {
      if (timer) { clearInterval(timer); timer = null; s.removeAttribute('data-playing'); play.setAttribute('aria-label', 'Play through the years'); return }
      s.setAttribute('data-playing', ''); play.setAttribute('aria-label', 'Pause');
      let i = +range.value >= years.length - 1 ? 0 : +range.value; set(i);
      timer = setInterval(() => { i++; if (i >= years.length) { clearInterval(timer); timer = null; s.removeAttribute('data-playing'); return } set(i) }, reduce ? 1600 : 1200);
    });
  });

  /* Drag-to-swipe on the front card (pointer events) */
  const deck = document.querySelector('.deck');
  if (deck) { let x0 = null, card = null;
    deck.addEventListener('pointerdown', e => { card = e.target.closest('.scard'); if (!card || card.classList.contains('scard--behind')) return; x0 = e.clientX; card.setPointerCapture(e.pointerId); card.style.transition = 'none' });
    deck.addEventListener('pointermove', e => { if (x0 == null) return; const dx = e.clientX - x0; card.style.transform = `translateX(${dx}px) rotate(${dx / 18}deg)`; card.classList.toggle('scard--tilt', Math.abs(dx) > 60); const st = card.querySelector('.scard__stamp'); if (st) st.textContent = dx > 0 ? 'AGREE' : 'DISAGREE' });
    deck.addEventListener('pointerup', () => { if (!card) return; card.style.transition = ''; card.style.transform = ''; card.classList.remove('scard--tilt'); x0 = null; card = null });
  }
})();
