(() => {
  const root = document.documentElement;
  const key = "goreecloud-theme";
  const saved = localStorage.getItem(key);
  if (saved === "light" || saved === "dark") root.dataset.theme = saved;
  else root.dataset.theme = matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
})();