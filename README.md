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


## November 11 — more compact layout and verified first-party product marks

This follow-up branch is **still review-only**, layered on top of the prior
catalog sharing branch. The founder likes the current visual language but
identified excess size and missing official product icons.

Spacing changes reduce oversized hero/section padding, pillar row rhythm,
CTA proportions, editorial card and footer space, and the Flowframe artwork
panel without changing route copy or token semantics. A read-only paired
Chromium measurement at 1440px compared unchanged base to revised source
and reported page-height reductions of 508px (home), 438px (ecosystem),
168px (products), 264px (principles), 204px (contact), and 275px (design).
These initial measurements precede the small follow-on search-spacing
refinement. Comparison tests covered 12 desktop/mobile route cases and
reported zero browser errors, broken images, external requests or overflow.

Existing source assets now used on the Products page:
**Browser** and **Browser Mobile** share one approved Prism Tabs v5 master;
**Search** uses its recovered canonical first-party favicon;
**Drive** uses first-party GoreeCloud-specific theme artwork that still
requires central brand approval; and **GC UI** displays the *unapproved*
Flowframe v2 visual proposal from a separate design review. Seven other
products keep explicitly identified neutral pending slots, not fake official
icons. The source and approval states are documented in
[BRAND-COVERAGE-BACKLOG.md](BRAND-COVERAGE-BACKLOG.md)
and [PRODUCT-ICON-SOURCES.json](PRODUCT-ICON-SOURCES.json),
and backed by SHA-256 and negative tests. New central master work is
tracked in [brand-assets issue #24](https://github.com/GoreeCloud/brand-assets/issues/24).

**No generator images were produced in chat.** All new site icons are
byte-identical to verified existing first-party SVGs. The founder's permanent
GoreeCloud umbrella PNG remains unchanged; production deployment, DNS, Cloudflare
Git integration and indexing are untouched. The preview is publicly reachable
by URL but noindex, and full human visual/AT/release acceptance remains open.


## November 11 — isolated Foundation v1 identity review gallery

The new **/identity-review/** route presents seven *unapproved* GoreeCloud
product identity candidates from [brand-assets draft PR #25](https://github.com/GoreeCloud/brand-assets/pull/25)
in a compact, accessible review interface. The review presents app icons
at 16px/32px actual resolution, transparent standalone symbols, adaptive
light/dark wordmarks, and conceptual artwork. The visual identities remain
proposals; the current Products page continues to mark them **missing**
until a canonical owner-approved logo is published and actually consumed.
The fixed reference commit is
`c48ebf7e9a098184e879445e6fe4aec9171fa7c3`.

All 49 web assets are exact byte-identical copies of the source branch,
with immutable SHA-256 records in `IDENTITY-REVIEW-SOURCES.json`.
The `scripts/verify_identity_review_gallery.py` gate checks candidate
status, local-only/parseable SVG and PNG content, seven distinct 16px marks,
all source hashes, navigation and visual-review disclaimers.
Seven mutation tests confirm it rejects a falsely official candidate,
asset tampering, commit drift, missing disclaimers and manifest anomalies.
These gates run in GitHub Actions. Rebuilding requires an authorized
source checkout and explicit `GOREECLOUD_BRAND_ASSETS_DIR`, not a download
at deploy time; the review site is wholly static.

**This is a preview-only route.** It is intentionally disallowed from
search indexing but is public by direct URL. It does not replace official
icons in the site catalog, production domain, favicon, native packages,
or identity master library. It does not assert that the depicted services
are live. Manual true-size, forced-colors, human screen-reader and founder
art-direction acceptance are still required.


## November 12 — candidate review workbench (additive draft)

The existing **/identity-review/** review-only route now offers three native,
keyboard-usable controls: a role/category filter, a **side-by-side comparison
of light and dark wordmarks** that does not require changing the whole
website theme, and an explicit reset. Per-product fragment permalinks enable
direct review without transmitting or storing query state. The displayed
filter count is announced in an accessible status region. Ordinary review
does not write cookies, local storage, analytics, clipboard or network
requests. All seven graphics remain *candidate-only* in both data and labels.

The workbench is applied by `scripts/upgrade_identity_workbench.py` after
the gallery-source build, without editing any of the 49 pinned candidate
asset files. `scripts/verify_identity_workbench.py` and six mutation tests
guard against unknown group assignments, candidate-to-official promotion,
broken anchors, loss of live status, or a network-capable review script.
The full static-site manifest now contains 84 files. A real Chromium run
confirmed 8/8 combinations (light/dark × 320/390/834/1440): filter,
comparison, reset, and fragment restore; no reported script errors,
broken images or horizontal overflow.

This is a *publicly accessible by URL*, noindex, isolated Pages draft
workflow; it is neither a brand approval portal with authenticated votes
nor a production deployment. Founder review, contrast/forced-colors/AT
assessment, accepted canonical master promotion and consuming-app rollout
remain separate gated work.


## November 12 — Signalform v2 proposed identity comparison

The founder requested a more distinctive coordinated family after the
original visual review. A **new, opt-in** `/identity-review-v2/` route
compares the retained Foundation v1 icon and redesigned Signalform v2 icon
for each of seven products at actual 16px/32px sizes and readable larger
tiles. Below the comparison are the v2 wordmarks in both light and dark
backgrounds, and optionally expanded original conceptual artwork.

The route uses exactly 49 V2 files copied byte-for-byte from the
authoritative [brand-assets Signalform v2 draft PR #27](https://github.com/GoreeCloud/brand-assets/pull/27)
source revision `0807d8719b13858394ba62637629c85d314bdf7a`.
The source/manifest pins are in `SIGNALFORM-V2-SOURCES.json`.
`scripts/verify_signalform_v2_review.py` and eight local mutation tests
assert identity status stays **pending**, v1 stays visible, all source files
match SHA-256, and the official Products catalog cannot adopt unapproved
V2 artwork silently. All 134 static site files are independently pinned.
The review is statically served, noindex, accessible by direct URL, and
has no analytics, third-party assets, embedded scripts or submission forms.

This comparison preview is neither a brand-approval action nor a live
production deployment. The founder's permanent GoreeCloud G, all
approved app marks and original v1 concepts remain unchanged.
