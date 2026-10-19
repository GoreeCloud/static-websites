# GC UI migration — retained public website and retired secondary-site boundaries

**Recorded:** October 19, 2026. **Canonical repository:** `GoreeCloud/static-websites`. **Status:** Migration requirements identified; **no public GC UI cutover accepted**.

## Normative scope

1. The current [one-website governance](../README.md) and [verified September 21 retirement record](migration-status.md) make `https://www.goreecloud.com/` the **only current GoreeCloud public website**. Its source is `sites/main/`; `sites/url-namespace.json` lists the authorized current paths. Retired `sites/mesh/**` is historical migration/rollback material, not a live deployment mandate.
2. The owner-designated active design authority is **GoreeCloud UI (GC UI)** in [GoreeCloud/gc-ui](https://github.com/GoreeCloud/gc-ui), **Integral Platform System #5 of nine**, replacing Glaze and Glaze UI permanently. No new Glaze/Glaze UI imports, brand claims, or runtime dependencies are authorized.
3. The [Foundations 1.0.1 release](https://github.com/GoreeCloud/gc-ui/releases/tag/foundations-v1.0.1) is **scoped stable** (semantic tokens, color/theme utilities); it is not proof that the entire GC UI development workspace, native catalog, or this website is accepted as stable.

## Exact source-based public website findings

These records were read from `GoreeCloud/static-websites` main before the documentation-only reconciliation:

| Source | Git source blob | Verified legacy condition |
| --- | --- | --- |
| `sites/main/index.html` | `b94ef4acd48ce518943f249596cc3eab0d89b786` | Glaze V1.7 metadata and historical source-adopted status remain in the active homepage |
| `sites/main/design/index.html` | `ef0959914b8270530718a18aa24277512059b51c` | Public design page calls retired Glaze V1.7 the *current official stable* visual authority |
| `sites/main/platform-systems/index.html` | `66897425c4d968ca7918e9911dfc9751f67ad508` | Nine-system platform overview still contains predecessor design references |
| `sites/main/glaze.lock.json` | `4bccee2f55654bb2d0bab9b0ff819a2f56c49f9f` | Historical Glaze 1.7 pinned dependency / source-adopted-unaccepted state |
| `sites/main/scripts/validate_glaze_ui.py` | `ddec9cbb35f08b9a26cefc51806f4aa7ca083cea` | Old source conformance validator expects Glaze 1.7 |
| `.github/workflows/validate-main-site.yml` | `664a0892e465fb0975c4c4bc42c8c96c01b87596` | Current website CI still checks out retired `GoreeCloud/glaze` |
| `sites/main/scripts/build_public_site.py` | `d620c2e210881e4de461dc90004222901c40e9ec` | Public output allowlist includes historical design icon and retained pages |

A source label `source-adopted-unaccepted` in prior acceptance evidence **does not prove GC UI conformance**. Old design source and acceptance history must be retained as evidence while active imports and public authority claims are replaced through separately verified work.

## Mandatory public-site migration sequence

1. **Pin current public truth.** Establish exact current `www` source revision, live artifact, Cloudflare Pages account/project `goreecloud-website`, DNS and page response/asset hashes, runtime behavior, headers, cache policy, real 404, and tested rollback. Never infer deployment from source or acceptance JSON alone.
2. **Inventory all dependency and design surfaces.** Audit 11 route entrypoints from `sites/url-namespace.json`, referenced CSS/JS, SVG/brand/icons, hidden imports, markup classes, theme persistence, accessibility and mobile behavior, and historical Glaze assets. Separate legacy source and nonactive historical records from actual active build/runtime dependencies. Do not adopt predecessor code by mechanical renaming.
3. **Build independent GC UI candidate without affecting `www`.** Use first-party verified branding, supported and exact-pinned GC UI Foundations release where applicable, original semantic interfaces, and a self-contained build. The product's typography, colors, interactions, contrast, motion, touch/keyboard and 404 behavior require independent testing; the scoped Foundations archive does not certify them.
4. **Preserve the one-website URL namespace.** No new secondary hostname or Pages project. Preserve existing canonical paths, SEO redirects and privacy content. Replace retired Glaze authority in `/design/` and IPS #5 in `/platform-systems/` without introducing a tenth IPS or transferring security/privacy authority.
5. **Validate the exact candidate revision.** Deterministic source/build/asset hashes, browser+assistive-tech screenreader/keyboard checks, 200–400% reflow, forced-colors, reduced motion, light/dark/system, selected and composited contrast, semantic landmarks and accessible naming, constrained network/origin policies, CSP/HSTS/404 via actual HTTPS staging, privacy and security review.
6. **Gate deployment and rollback.** Maintain a separately staged candidate with owner-accepted exact artifact/SHA, Cloudflare Pages configuration, DNS and recovery evidence. Only replace the current `www` build/CI after independent acceptance; preserve prior deployment for rollback. Never revive historical Mesh or other satellite deployments as a workaround.
7. **Reconcile governed records after verified cutover.** Update the current Platform Contract and independently accepted GC UI consumer ledger. Reconcile authoritative Google Drive `Instructions.md`, `Instructions — Integral Platform Systems.md` and the system-wide platform contract **in place** using verified exact Markdown bytes and file identity. Keep completion/retirement flags false pending evidence.

## Parallel Mesh development track — explicitly not publication

An isolated first-party GC UI Mesh preview lives in `GoreeCloud/mesh/gc-ui-site/` and has offline/source, Chromium/Firefox, contrast/reflow and localhost HTTP tests. It uses the reviewed GC UI Foundations 1.0.1 source stylesheet. This **does not mean** `mesh.goreecloud.com` should resolve or that a secondary public Mesh site should be deployed. The [Mesh preview tracker](https://github.com/GoreeCloud/mesh/issues/54) is not a public DNS deployment authorization. Restore retired sites only on a later explicit owner decision that supersedes the single-website retirement authority.

## Tracking and acceptance status

Current-public-site migration: [static-websites issue #144](https://github.com/GoreeCloud/static-websites/issues/144). Platform-wide migration: [gc-ui issue #13](https://github.com/GoreeCloud/gc-ui/issues/13).

**Truth flags:** `currentWebsiteCount=1`; `activeWebsite=www.goreecloud.com`; `gcUiConsumerMigrationAccepted=false`; `liveSiteCutoverVerified=false`; `retiredSecondarySiteReactivated=false`; `canonicalGovernanceMarkdownUpdated=false`.
