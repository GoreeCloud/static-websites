/* GC UI isolated GitHub catalog: visitor-triggered, public-only, zero credentials. */
(() => {
  'use strict';
  const button = document.querySelector('[data-gc-load-repos]');
  const results = document.getElementById('github-live-results');
  const status = document.getElementById('github-live-status');
  const filter = document.querySelector('[data-gc-repo-filter]');
  const filterLabel = document.querySelector('label[for="github-repo-filter"]');
  if (!button || !results || !status || !filter || !filterLabel) return;
  const endpoint = 'https://api.github.com/users/GoreeCloud/repos';
  const MAX_PAGES = 5;
  const PAGE_SIZE = 100;
  const TIMEOUT_MS = 9000;
  let active = false;
  let all = [];
  let loaded = false;

  function announce(message) { status.textContent = message; }
  function element(tag, text, className) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    node.textContent = text;
    return node;
  }
  function normalize(item) {
    if (!item || typeof item !== 'object' || item.private !== false ||
        typeof item.name !== 'string' || !/^[a-zA-Z0-9._-]{1,100}$/.test(item.name) ||
        item.full_name !== 'GoreeCloud/' + item.name ||
        !item.owner || item.owner.login !== 'GoreeCloud') return null;
    return {
      name: item.name,
      url: 'https://github.com/GoreeCloud/' + encodeURIComponent(item.name),
      description: typeof item.description === 'string' ? item.description.slice(0, 350) : '',
      language: typeof item.language === 'string' ? item.language.slice(0, 40) : 'Unspecified',
      branch: typeof item.default_branch === 'string' ? item.default_branch.slice(0, 60) : 'Unknown',
      archived: item.archived === true
    };
  }
  function render() {
    const query = filter.value.trim().toLocaleLowerCase();
    const selected = all.filter(item =>
      [item.name, item.description, item.language].some(value => value.toLocaleLowerCase().includes(query)));
    const fragment = document.createDocumentFragment();
    for (const item of selected) {
      const card = document.createElement('article');
      card.className = 'panel candidate-content-card github-repo-card';
      const heading = document.createElement('h3');
      const link = document.createElement('a');
      link.href = item.url;
      link.rel = 'noopener noreferrer';
      link.textContent = item.name;
      heading.append(link);
      card.append(heading);
      card.append(element('p', item.description || 'No public description provided.'));
      card.append(element('p', 'Language: ' + item.language + ' · Branch: ' + item.branch +
        (item.archived ? ' · Archived' : '')));
      fragment.append(card);
    }
    results.replaceChildren(fragment);
    const count = selected.length + ' of ' + all.length + ' public repositories shown';
    announce(count + (selected.length === 0 ? '. No matching public repositories.' : '.'));
  }
  async function getPage(page) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);
    const url = endpoint + '?type=owner&sort=full_name&direction=asc&per_page=' +
      PAGE_SIZE + '&page=' + page;
    try {
      const response = await fetch(url, {method: 'GET', mode: 'cors', credentials: 'omit',
        redirect: 'error', cache: 'no-store', signal: controller.signal,
        headers: {Accept: 'application/vnd.github+json'}});
      if (!response.ok) throw new Error(response.status === 403 || response.status === 429 ?
        'GitHub has limited public requests. Please retry later.' :
        'GitHub request failed (HTTP ' + response.status + ').');
      const data = await response.json();
      if (!Array.isArray(data) || data.length > PAGE_SIZE)
        throw new Error('GitHub returned an unexpected public catalog response.');
      return data;
    } finally {
      clearTimeout(timeout);
    }
  }
  button.addEventListener('click', async () => {
    if (active || loaded) return;
    active = true;
    button.disabled = true;
    results.setAttribute('aria-busy', 'true');
    announce('Loading public repositories from GitHub on your request…');
    const seen = new Set();
    const collection = [];
    try {
      let completed = false;
      for (let page = 1; page <= MAX_PAGES; page++) {
        const data = await getPage(page);
        for (const item of data) {
          const normalized = normalize(item);
          if (!normalized || seen.has(normalized.name.toLocaleLowerCase())) continue;
          seen.add(normalized.name.toLocaleLowerCase());
          collection.push(normalized);
        }
        if (data.length < PAGE_SIZE) {
          completed = true;
          break;
        }
      }
      if (!completed) throw new Error('Public catalog exceeds the safe page limit. Use GitHub directly.');
      all = collection.sort((a, b) => a.name.toLocaleLowerCase().localeCompare(b.name.toLocaleLowerCase()));
      loaded = true;
      filter.hidden = false;
      filterLabel.hidden = false;
      button.textContent = 'Public repositories loaded';
      render();
    } catch (error) {
      announce(error instanceof Error ? error.message : 'Public catalog is temporarily unavailable.');
      button.disabled = false; // explicit user-triggered retry; never automatic
    } finally {
      active = false;
      results.removeAttribute('aria-busy');
    }
  });
  filter.addEventListener('input', () => { if (loaded) render(); });
})();