/* GoreeCloud identity review only. No data collection, analytics or remote APIs. */
(() => {
  'use strict';
  const controls = document.querySelector('[data-review-workbench]');
  const grid = document.querySelector('[data-review-grid]');
  if (!controls || !grid) return;
  const filter = controls.querySelector('[data-review-filter]');
  const compare = controls.querySelector('[data-review-compare]');
  const reset = controls.querySelector('[data-review-reset]');
  const count = controls.querySelector('[data-review-count]');
  const cards = [...grid.querySelectorAll('[data-review-product][data-review-status="candidate"]')];
  const allowed = new Set(['all', 'pillars', 'applications', 'infrastructure']);
  if (!filter || !compare || !reset || !count || cards.length !== 7) return;

  const apply = () => {
    const group = allowed.has(filter.value) ? filter.value : 'all';
    if (group !== filter.value) filter.value = group;
    let visible = 0;
    for (const card of cards) {
      // Only the declared candidate group affects visibility. Status is never changed.
      card.hidden = group !== 'all' && card.dataset.reviewCategory !== group;
      if (!card.hidden) visible++;
    }
    count.textContent = group === 'all'
      ? 'Showing all 7 proposed designs.'
      : 'Showing ' + visible + ' of 7 proposed designs.';
  };
  const setCompare = enabled => {
    grid.dataset.reviewCompare = String(enabled);
    compare.setAttribute('aria-pressed', String(enabled));
    compare.textContent = enabled
      ? 'Hide side-by-side wordmarks'
      : 'Compare light and dark wordmarks';
  };
  filter.addEventListener('change', apply);
  compare.addEventListener('click', () => {
    setCompare(compare.getAttribute('aria-pressed') !== 'true');
  });
  reset.addEventListener('click', () => {
    filter.value = 'all';
    setCompare(false);
    apply();
    count.textContent = 'Review reset. Showing all 7 proposed designs.';
  });
  // Native fragment links allow direct concept review without URL query state,
  // persistent storage, clipboard permissions or external requests.
  const showHashTarget = () => {
    const hash = window.location.hash || '';
    if (!/^#identity-(goreeshield|wardveil|mesh|maps|projects|analytics|gateway)$/.test(hash)) return;
    const match = cards.find(card => '#' + card.id === hash);
    if (match && match.hidden) {
      filter.value = 'all';
      apply();
    }
  };
  window.addEventListener('hashchange', showHashTarget);
  setCompare(false);
  apply();
  showHashTarget();
})();