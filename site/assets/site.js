/* Progressive enhancements only. No analytics, cookies or external requests. */
(() => {
  'use strict';
  const root = document.documentElement;
  const toggle = document.querySelector('[data-theme-toggle]');
  const themeStorageKey = 'goreecloud-website-theme';
  const prefersLight = window.matchMedia?.('(prefers-color-scheme: light)')?.matches === true;
  let chosenTheme = prefersLight ? 'light' : 'dark';
  try {
    const saved = window.localStorage.getItem(themeStorageKey);
    if (saved === 'light' || saved === 'dark') chosenTheme = saved;
  } catch (_) { /* Storage may be disabled; theme remains usable. */ }
  const setTheme = theme => {
    root.dataset.theme = theme;
    const browserTheme = document.querySelector('meta[name="theme-color"]');
    browserTheme?.setAttribute('content', theme === 'dark' ? '#0b1020' : '#eef0fa');
    if (toggle) {
      toggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`);
      toggle.setAttribute('title', `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`);
      toggle.setAttribute('aria-pressed', String(theme === 'light'));
    }
  };
  setTheme(chosenTheme);
  toggle?.addEventListener('click', () => {
    chosenTheme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    setTheme(chosenTheme);
    try { window.localStorage.setItem(themeStorageKey, chosenTheme); } catch (_) { /* Optional persistence. */ }
  });
  const search = document.querySelector('[data-search]');
  const filters = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('[data-product-card]')];
  const count = document.querySelector('[data-results-count]');
  const empty = document.querySelector('[data-empty]');
  let selectedCategory = 'all';
  const updateCatalog = () => {
    const q = (search?.value || '').trim().toLocaleLowerCase();
    let visible = 0;
    cards.forEach(card => {
      const text = (card.textContent || '').toLocaleLowerCase();
      const matches = (!q || text.includes(q)) && (selectedCategory === 'all' || card.dataset.category === selectedCategory);
      card.hidden = !matches;
      if (matches) visible++;
    });
    if (count) count.textContent = `${visible} ${visible === 1 ? 'project' : 'projects'} shown`;
    if (empty) empty.hidden = visible > 0;
  };
  search?.addEventListener('input', updateCatalog);
  filters.forEach(filter => filter.addEventListener('click', () => {
    selectedCategory = filter.dataset.filter || 'all';
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === filter)));
    updateCatalog();
  }));
  updateCatalog();

  // The full GitHub repository index is a dated local snapshot. Filtering
  // uses only this document; it never queries GitHub from the browser.
  const repoSearch = document.querySelector('[data-repo-search]');
  const repoItems = [...document.querySelectorAll('[data-repo-item]')];
  const repoCount = document.querySelector('[data-repo-count]');
  const repoEmpty = document.querySelector('[data-repo-empty]');
  const updateRepos = () => {
    const query = (repoSearch?.value || '').trim().toLocaleLowerCase();
    let visible = 0;
    repoItems.forEach(item => {
      const found = !query || (item.textContent || '').toLocaleLowerCase().includes(query);
      item.hidden = !found;
      if (found) visible++;
    });
    if (repoCount) repoCount.textContent = `${visible} ${visible === 1 ? 'repository' : 'repositories'} shown`;
    if (repoEmpty) repoEmpty.hidden = visible !== 0;
  };
  repoSearch?.addEventListener('input', updateRepos);
  updateRepos();

  // A dated historical Suite name registry preserves old public editorial
  // structure; browser interactions are entirely local and do not imply launch.
  const suiteSearch = document.querySelector('[data-suite-search]');
  const suiteFilter = document.querySelector('[data-suite-filter]');
  const suiteGroups = [...document.querySelectorAll('[data-suite-group]')];
  const suiteCount = document.querySelector('[data-suite-count]');
  const suiteEmpty = document.querySelector('[data-suite-empty]');
  const updateSuite = () => {
    const query = (suiteSearch?.value || '').trim().toLocaleLowerCase();
    const activeGroup = suiteFilter?.value || 'all';
    let total = 0;
    let visibleGroups = 0;
    suiteGroups.forEach(group => {
      let groupVisible = 0;
      const groupMatches = activeGroup === 'all' || group.dataset.suiteGroupId === activeGroup;
      group.querySelectorAll('[data-suite-item]').forEach(item => {
        const found = groupMatches && (!query || (item.textContent || '').toLocaleLowerCase().includes(query));
        item.hidden = !found;
        if (found) groupVisible++;
      });
      group.hidden = groupVisible === 0;
      if (groupVisible) visibleGroups++;
      total += groupVisible;
    });
    if (suiteCount) suiteCount.textContent = `${total} ${total === 1 ? 'name' : 'names'} shown across ${visibleGroups} ${visibleGroups === 1 ? 'group' : 'groups'}`;
    if (suiteEmpty) suiteEmpty.hidden = total !== 0;
  };
  suiteSearch?.addEventListener('input', updateSuite);
  suiteFilter?.addEventListener('change', updateSuite);
  updateSuite();
})();
