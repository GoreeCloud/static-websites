/* GoreeCloud appearance: fresh visitors always start in light mode.
   A manually chosen appearance is stored locally only; no telemetry or remote APIs. */
(() => {
  "use strict";

  const root = document.documentElement;
  const toggle = document.querySelector("[data-theme-toggle]");
  const text = toggle?.querySelector("[data-theme-label]");
  const symbol = toggle?.querySelector("[data-theme-symbol]");
  const themeColor = document.querySelector('meta[name="theme-color"]');
  const preferenceKey = "goreecloud.website.appearance";

  let initial = "light";
  try {
    const saved = window.localStorage.getItem(preferenceKey);
    if (saved === "light" || saved === "dark") initial = saved;
  } catch {
    // Restricted storage must never prevent the homepage from working.
  }

  function applyTheme(mode, persist = false) {
    const dark = mode === "dark";
    root.setAttribute("data-gc-theme", dark ? "dark" : "light");
    if (themeColor) themeColor.setAttribute("content", dark ? "#0d121d" : "#f6f7fb");

    if (toggle) {
      toggle.setAttribute("aria-pressed", String(dark));
      toggle.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
      if (text) text.textContent = dark ? "Light mode" : "Dark mode";
      if (symbol) symbol.textContent = dark ? "☀" : "☾";
    }

    if (persist) {
      try {
        window.localStorage.setItem(preferenceKey, dark ? "dark" : "light");
      } catch {
        // Browsers may refuse storage; the current page still switches.
      }
    }
  }

  applyTheme(initial);
  if (!toggle) return;
  toggle.hidden = false;
  toggle.addEventListener("click", () => {
    applyTheme(root.getAttribute("data-gc-theme") === "dark" ? "light" : "dark", true);
  });
})();
