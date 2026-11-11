# GoreeCloud static website — preview snapshot recovery

The immutable recovery baseline remains on branch `recovery/immutable-pages-preview-20261111`. The current `feat/gcui-official-identity-layout-20261111` branch is a **separate branded design iteration**, not byte-identical to the earlier deployed preview and not yet approved for production.

This was originally a **review-only recovery branch** of the current GoreeCloud website **preview**.
It is **not** the former `GoreeCloud/static-websites` repository history, and it is
**not the source of the currently deployed production website**.

## Identity and provenance

Cloudflare Pages' saved source configuration references an earlier GitHub
repository object with ID `1358646162`, which is no longer accessible. The
present `GoreeCloud/static-websites` repository is a separate, newly created
GitHub object with ID `1453961169`; it initially had only a README.

The `site/` directory in this review branch contains a preview-derived set of **26 static files**. The original 20-file immutable source snapshot remains on the recovery branch; this feature branch modifies page presentation and adds six verified official GC UI image derivatives. The earlier source was deployed to Cloudflare Pages; this iteration must be staged and independently tested before claiming hosted acceptance of November 11, 2026. This is a recovery of compiled public preview
assets, **not** a reconstruction of the old source history or the complete
standalone Python generator. The complete generator, tests and local evidence
remain in the private GoreeCloud Website Google Drive project archive.

Preview branch: `preview-gcui-rebuild-20261111`.
Immutable Pages deployment ID: `a875c44e-87e2-49c8-a5b0-bae38d5be89d`.
Immutable review URL: https://a875c44e.goreecloud-website.pages.dev/

## Scope and verification

All 14 preview content routes (including 11 formerly published sitemap paths),
the custom 404, preview-only robots policy, static JS/CSS and the temporary
`/social/` 302 are preserved. `SITE-MANIFEST.sha256` pins the current 26-file iteration byte-for-byte. The provenance and original deployed snapshot are retained on the base branch. `scripts/verify_preview_snapshot.py` enforces manifest
integrity and preview-only safety. No runtime dependencies are required.

```sh
python3 scripts/verify_preview_snapshot.py
```

The GitHub Actions workflow runs only source tests and **never deploys,
changes DNS, runs Cloudflare CLI, or uses GitHub/Cloudflare credentials**.
The branch and pull request are explicitly held for source-history,
accessibility, editorial, branding, SEO, licensing and release review.
No production `main` branch changes are requested or authorized by this
snapshot. Do not connect this new GitHub ID to Cloudflare without a separate
source-mapping review.

## License and marks

The original static code and accompanying software in this recovery branch
are offered under [MIT](LICENSE). This does not grant rights to the
GoreeCloud name or marks, third-party linked content, or historical code
that is not present in this repository.


## November 11 — GC UI branding and readability iteration

The website's `/design/` page now consumes exactly pinned official
GoreeCloud UI app icon, favicon, light/dark wordmarks and the approved
Aperture Weave interface constellation artwork from
[brand-assets](https://github.com/GoreeCloud/brand-assets/tree/main/products/gc-ui)
revision `29be2e70201bd12adfcdcb3c25106abf9408c6d1`.
The website's global GoreeCloud identity remains separate: the GC UI
app favicon is deliberately route-specific, not applied to the whole
umbrella website. Hero copy, card legibility and section rhythm were
refined without replacing privacy/cybersecurity/integration boundaries.

The new SVG and ICO assets are stored locally to avoid runtime requests,
their SHA-256 is pinned and enforced by the local validator. The original
source asset license and brand-mark rights remain governed by the
GoreeCloud repository and per-product terms. Exact original files are
not AI recolored or regenerated. Consumer browser tests and typography
zoom checks are independent release gates.


## November 11 — permanent GoreeCloud G + experimental new GC UI design

This **separate site review branch** displays the exact uploaded GoreeCloud
permanent master PNG in global navigation, footer and homepage illustration,
and loads its brand-assets source-mapped SVG/ICO favicons on all 15 HTML files.
The uploaded PNG remains source-of-truth, not the SVG trace.

For the **GoreeCloud UI** product presentation only, the site shows a
clearly labeled **Flowframe v2 candidate** from
`GoreeCloud/brand-assets` [draft PR #22](https://github.com/GoreeCloud/brand-assets/pull/22).
The previous founder-approved Aperture Weave master remains published and
unchanged; this experimental website iteration does not select the candidate.

This branch is based on the existing **review-only website PR #2**, not on the
historical Cloudflare Git repository or the production source. All 29 site
assets and brand identities are SHA-256 pinned; the standalone validator
enforces noindex/CSP and flags any generic umbrella mark. This iteration must
pass hosted Pages and real-browser checks separately before visual acceptance.
No production deployment, DNS change, indexing launch or historical source
reconciliation is implied.


## November 11 — private-by-default catalog-sharing capabilities (draft)

This feature branch adds **share filtered link** and **reset filters** actions
for Products, the dated GitHub directory, and the historical Suite index.
The share control explicitly creates a same-origin, bounded (120-character)
URL query; ordinary typing is not stored, transmitted or placed in the
address bar. The browser's clipboard API is optional; a selectable link
is rendered on the page as a fallback. Escape resets search and selection.
The link is intentionally noindex because this remains a public but
nonproduction Pages preview.

The offline source audit checks all 15 HTML pages, local link targets and
fragments, external-tab rel protection, first-party-only assets, noindex
metadata and CSP-sensitive inline scripts. It is supplemented by nine
negative/positive Python unit tests and five dependency-free Node tests
for URL restoration, search bounding, safe fallback, keyboard reset and
back/forward restoration. GitHub Actions runs those gates, behavior tests, and checks
both first-party scripts; **no CI deployment credentials or Cloudflare
mutation are added**. Actual local Chromium exercised nine filtered-link
restoration, reset, share fallback and responsive scenarios successfully.
Human AT, actual touch, translation, editorial parity and production
approval remain separate gates.
