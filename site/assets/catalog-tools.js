/* GoreeCloud catalog tools: shareable local filters, without analytics or requests. */
(() => {
  'use strict';
  const panel = document.querySelector('[data-catalog-actions]');
  if (!panel) return;

  const kind = panel.dataset.catalogActions;
  if (!['products', 'github', 'suite'].includes(kind)) return;
  const input = document.querySelector({
    products: '[data-search]',
    github: '[data-repo-search]',
    suite: '[data-suite-search]'
  }[kind]);
  const share = panel.querySelector('[data-catalog-share]');
  const reset = panel.querySelector('[data-catalog-reset]');
  const status = panel.querySelector('[data-catalog-status]');
  const link = panel.querySelector('[data-catalog-link]');
  const filters = [...document.querySelectorAll('[data-filter]')];
  const group = document.querySelector('[data-suite-filter]');

  if (!input || !share || !reset || !status || !link) return;
  const maxLength = 120;
  const emit = (element, eventName) =>
    element?.dispatchEvent(new Event(eventName, { bubbles: true }));
  const categoryAllowed = value =>
    filters.some(button => button.dataset.filter === value);
  const groupAllowed = value =>
    [...(group?.options || [])].some(option => option.value === value);
  const getCategory = () =>
    filters.find(button => button.getAttribute('aria-pressed') === 'true')?.dataset.filter || 'all';

  const clearLink = () => {
    link.hidden = true;
    link.textContent = '';
  };
  const applyUrl = () => {
    const query = new URLSearchParams(window.location.search);
    const text = (query.get('q') || '').slice(0, maxLength);
    input.value = text;
    emit(input, 'input');
    if (kind === 'products') {
      const value = query.get('category') || 'all';
      filters.find(button => button.dataset.filter ===
        (categoryAllowed(value) ? value : 'all'))?.click();
    }
    if (kind === 'suite' && group) {
      const value = query.get('group') || 'all';
      group.value = groupAllowed(value) ? value : 'all';
      emit(group, 'change');
    }
    clearLink();
    status.textContent = '';
  };
  const buildLink = () => {
    // Explicit share action only: no search state is uploaded, stored, or
    // written to the address bar during ordinary typing.
    const url = new URL(window.location.pathname, window.location.origin);
    const q = input.value.trim().slice(0, maxLength);
    if (q) url.searchParams.set('q', q);
    if (kind === 'products') {
      const category = getCategory();
      if (categoryAllowed(category) && category !== 'all')
        url.searchParams.set('category', category);
    }
    if (kind === 'suite') {
      const selected = group?.value || 'all';
      if (groupAllowed(selected) && selected !== 'all')
        url.searchParams.set('group', selected);
    }
    return url;
  };
  const resetCatalog = () => {
    input.value = '';
    emit(input, 'input');
    if (kind === 'products')
      filters.find(button => button.dataset.filter === 'all')?.click();
    if (kind === 'suite' && group) {
      group.value = 'all';
      emit(group, 'change');
    }
    // Explicit reset removes catalog-specific URL query state on this page.
    history.replaceState(history.state, '', window.location.pathname);
    clearLink();
    status.textContent = 'Filters cleared. Showing the full directory.';
  };

  input.maxLength = maxLength;
  applyUrl();
  share.addEventListener('click', async () => {
    const url = buildLink();
    // Show a selectable link even if clipboard permission is unavailable.
    link.textContent = url.href;
    link.hidden = false;
    history.replaceState(history.state, '', url.pathname + url.search);
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(url.href);
      status.textContent = 'Link copied. You can share this filtered view.';
    } catch (_) {
      status.textContent = 'Link ready below. Copy it to share this filtered view.';
    }
  });
  reset.addEventListener('click', resetCatalog);
  input.addEventListener('keydown', event => {
    if (event.key === 'Escape' && (input.value || kind !== 'github')) {
      event.preventDefault();
      resetCatalog();
    }
  });
  window.addEventListener('popstate', applyUrl);
})();
