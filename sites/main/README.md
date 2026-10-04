# GoreeCloud Main Website

Canonical source for GoreeCloud's one current public website.

- Canonical domain: `https://www.goreecloud.com/`
- Canonical repository: `GoreeCloud/static-websites`
- Site root: `sites/main`
- Cloudflare Pages project: `goreecloud-website`
- Current public model: one website with path-based sections
- Current design target: **Glaze V1.7 / 1.7.0 Stable**
- Consumer state: **source adopted — repository-local acceptance pending**

## Current public information architecture

The website is intentionally path-based rather than a collection of separate public websites:

- `/` — GoreeCloud overview
- `/platform-systems/` — the nine Integral Platform Systems
- `/suite/` — the reconciled 45-product GoreeCloud Suite registry
- `/android/` — Android applications and product clients grouped by current lifecycle
- `/office-suite/` — GoreeCloud Office Suite
- `/firefox/` — standalone extensions and application-owned Firefox clients
- `/github/` — current public GitHub repository discovery

Compatibility paths such as `/repositories.html`, `/privacy.html`, and `/security.html` are retained only as transition entry points and must not carry stale standalone content.

## Truth and authority

Public content must not manufacture current state.

- The authoritative Suite inventory controls Suite membership. The current reconciled registry is 45 products across nine functional groups.
- `Instructions — Integral Platform Systems` controls the current nine-system platform model.
- Live GitHub is authoritative for repository existence, names, visibility, descriptions, and archive state.
- Product implementation and lifecycle state remain controlled by each product's authoritative repository and project records.
- Glaze UI presentation must not be presented as proof of privacy, security, deployment, production readiness, or platform integration.

The website must not publish private repository names or fixed private-repository counts.

## Glaze V1.7 source adoption

This source now targets the current bounded Stable Glaze 1.7.0 contract at `GoreeCloud/glaze@1a5756daed2294155be2e9972b24f580f6222b7b` using `js/glaze-v1.7.0.mjs`. Glaze 1.7.0 intentionally inherits the accepted 1.6.0 runtime surface, but downstream website conformance is not inherited automatically. The website therefore records `source-adopted-unaccepted` until exact-revision rendered, accessibility, performance/resilience, rollback, deployment/readback, and owner acceptance evidence is completed.

The rebuild uses local, same-origin presentation code. It does not require remote Glaze runtime execution in the browser.

## Build and validation

From the repository root:

```bash
python sites/main/scripts/build_public_site.py
python sites/main/scripts/validate_build_artifact.py
python sites/main/scripts/validate_site.py
python sites/main/scripts/validate_public_surface.py
python sites/main/scripts/validate_glaze_ui.py
python sites/main/scripts/browser_artifact_smoke.py
node --check sites/main/js/theme-init-v8.js
node --check sites/main/js/site-v8.js
```

The public artifact is allowlisted and excludes repository-only documentation, tests, source history, private data, and retired website packages.

## Privacy and repository catalog

The GitHub page does not contact GitHub automatically. A visitor must explicitly choose **Load current public repositories** before the browser requests public repository metadata from `api.github.com`. The page contains a direct organization link for visitors who prefer not to make that request from the GoreeCloud site.

## Production redeploy trigger — September 21, 2026

Owner acceptance for PR #121 is complete. Accepted public-source head `02b60edf27b36e7cad31d0bbf383b147bcfed6f4` was merged to `main` as `3715e132e6a2ce6f3f4034a9dc6f0b70b2078af4`.

A production redeploy was explicitly requested after the canonical hostname continued to serve the prior website bytes. This repository-only note intentionally changes no public website source or generated public artifact; its purpose is to create a governed `main` push so the connected Cloudflare Pages project can rebuild and publish the already accepted website bytes.

Production completion still requires post-push live verification of `https://www.goreecloud.com/`, `/design/`, `/security/`, and `/privacy/`.

## Acceptance boundary

Source changes, a successful build, CI success, or a Cloudflare deployment do not by themselves establish final production acceptance. Merge, deployment, exact deployed-byte verification, rendered review, accessibility acceptance, performance acceptance, rollback readiness, and current Glaze consumer acceptance remain separately governed transitions.
