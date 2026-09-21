# GoreeCloud Main Website

Canonical source for GoreeCloud's one current public website.

- Canonical domain: `https://www.goreecloud.com/`
- Canonical repository: `GoreeCloud/static-websites`
- Site root: `sites/main`
- Cloudflare Pages project: `goreecloud-website`
- Current public model: one website with path-based sections
- Current design target: **GLAZE UI V1.6 / 1.6.0 Stable**
- Consumer state: **migration candidate — repository-local acceptance pending**

## Current public information architecture

The website is intentionally path-based rather than a collection of separate public websites:

- `/` — GoreeCloud overview
- `/platform-systems/` — the nine Integral Platform Systems
- `/suite/` — the reconciled 45-product GoreeCloud Suite registry
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

## Glaze UI V1.6 migration

This rebuild targets the current Official Stable Glaze UI 1.6.0 contract. Stable lifecycle authority is pinned at `081527eff1c5fe5001b6b9598d60439c8fb3c5e3`; the separately recorded accepted published release source is `a7180679ea851389e0f3004515f9a25f420e716d`. The shared Glaze UI release is consumer-eligible, but downstream website conformance is not inherited automatically. The website therefore records its state as `migration-candidate-unaccepted` until exact-revision repository-local rendered, accessibility, performance, and other required acceptance evidence is completed.

The rebuild uses local, same-origin presentation code. It does not require remote Glaze UI runtime execution in the browser.

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

Source changes, a successful build, CI success, or a Cloudflare deployment do not by themselves establish final production acceptance. Merge, deployment, exact deployed-byte verification, rendered review, accessibility acceptance, performance acceptance, rollback readiness, and current Glaze UI consumer acceptance remain separately governed transitions.
