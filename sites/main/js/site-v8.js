(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector("[data-theme-toggle]");
  const nav = document.querySelector("[data-nav]");
  const navButton = document.querySelector("[data-nav-toggle]");
  const search = document.querySelector("[data-filter-input]");

  if (themeButton) {
    const syncThemeLabel = () => {
      themeButton.setAttribute(
        "aria-label",
        root.dataset.theme === "light" ? "Switch to dark theme" : "Switch to light theme"
      );
    };
    syncThemeLabel();
    themeButton.addEventListener("click", () => {
      const next = root.dataset.theme === "light" ? "dark" : "light";
      root.dataset.theme = next;
      localStorage.setItem("goreecloud-theme", next);
      syncThemeLabel();
    });
  }

  if (nav && navButton) {
    const setNavOpen = (open) => {
      nav.dataset.open = open ? "true" : "false";
      navButton.setAttribute("aria-expanded", open ? "true" : "false");
    };

    navButton.addEventListener("click", () => {
      setNavOpen(nav.dataset.open !== "true");
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && nav.dataset.open === "true") {
        setNavOpen(false);
        navButton.focus();
      }
    });

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        if (matchMedia("(max-width: 900px)").matches) setNavOpen(false);
      });
    });
  }

  if (search) {
    search.addEventListener("input", () => {
      const query = search.value.trim().toLowerCase();
      document.querySelectorAll("[data-filter-item]").forEach((item) => {
        item.hidden = query !== "" && !item.textContent.toLowerCase().includes(query);
      });
    });
  }

  const load = document.querySelector("[data-load-github]");
  const list = document.querySelector("[data-github-list]");
  const status = document.querySelector("[data-github-status]");
  if (load && list && status) {
    load.addEventListener("click", async () => {
      load.disabled = true;
      status.textContent = "Loading current public repositories from GitHub…";
      try {
        const repositories = [];
        for (let page = 1; page <= 3; page += 1) {
          const response = await fetch("https://api.github.com/orgs/GoreeCloud/repos?type=public&sort=full_name&direction=asc&per_page=100&page=" + page, {
            headers: { "Accept": "application/vnd.github+json" }
          });
          if (!response.ok) throw new Error("GitHub returned HTTP " + response.status);
          const batch = await response.json();
          repositories.push(...batch);
          if (batch.length < 100) break;
        }
        list.replaceChildren(...repositories.map((repo) => {
          const article = document.createElement("article");
          article.className = "repo-card";
          article.dataset.filterItem = "";
          const title = document.createElement("h3");
          const link = document.createElement("a");
          link.href = repo.html_url;
          link.textContent = repo.name;
          link.rel = "noopener noreferrer";
          title.append(link);
          const description = document.createElement("p");
          description.textContent = repo.description || "No public GitHub description is currently set.";
          const meta = document.createElement("div");
          meta.className = "repo-meta";
          meta.textContent = [repo.archived ? "Archived" : "Active", repo.language, repo.default_branch ? "default: " + repo.default_branch : null].filter(Boolean).join(" • ");
          article.append(title, description, meta);
          return article;
        }));
        status.textContent = "Loaded " + repositories.length + " public repositories directly from GitHub.";
        const filter = document.querySelector("[data-github-filter]");
        if (filter) filter.hidden = false;
      } catch (error) {
        status.textContent = "GitHub could not be reached. Use the organization link below for the live repository list.";
        load.disabled = false;
      }
    });
  }
})();