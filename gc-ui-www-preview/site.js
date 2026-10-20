/* GC UI retained-web preview: local-only theme mode, no analytics/remote I/O. */
(() => {
  'use strict';
  const root = document.documentElement;
  const key = 'goreecloud-gc-ui-www-design-preview-mode';
  const available = new Set(['system', 'light', 'dark']);
  const media = typeof matchMedia === 'function' ? matchMedia('(prefers-color-scheme: dark)') : null;
  const buttons = [...document.querySelectorAll('[data-mode]')];
  let choice = 'system';
  try { choice = localStorage.getItem(key) || 'system'; } catch (_) { choice = 'system'; }
  if (!available.has(choice)) choice = 'system';
  function render() {
    const mode = choice === 'system' ? (media?.matches ? 'dark' : 'light') : choice;
    root.setAttribute('data-gc-mode', mode);
    for (const button of buttons) {
      button.setAttribute('aria-pressed', String(button.dataset.mode === choice));
    }
  }
  for (const button of buttons) {
    button.addEventListener('click', () => {
      if (!available.has(button.dataset.mode)) return;
      choice = button.dataset.mode;
      try { localStorage.setItem(key, choice); } catch (_) { /* private storage */ }
      render();
    });
  }
  try { media?.addEventListener('change', () => { if (choice === 'system') render(); }); }
  catch (_) { /* old browser without change subscriptions */ }
  // Suite filtering only: this is local DOM text search, never remote retrieval.
  const suiteFilter = document.querySelector('[data-suite-filter]');
  const firefoxFilter = document.querySelector('[data-firefox-filter]');
  const currentFilter = suiteFilter || firefoxFilter;
  if (currentFilter) {
    const products = [...document.querySelectorAll('#source-content .candidate-content-card')];
    const status = document.getElementById(suiteFilter ? 'suite-filter-status' : 'firefox-filter-status');
    const update = () => {
      const query = currentFilter.value.trim().toLocaleLowerCase();
      let shown = 0;
      for (const product of products) {
        const matches = product.textContent.toLocaleLowerCase().includes(query);
        product.hidden = !matches;
        if (matches) shown++;
      }
      if (status) status.textContent = shown + ' of ' + products.length + (suiteFilter ? ' products shown' : ' Firefox tools shown');
    };
    currentFilter.addEventListener('input', update);
    update();
  }
  render();
})();
