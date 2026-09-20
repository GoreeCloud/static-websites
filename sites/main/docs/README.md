# GoreeCloud Website Repository Documentation

## Purpose

This directory contains repository-only records that support the retained `www.goreecloud.com` website. These records are not browser-facing website content and must remain outside the generated public `dist/` artifact.

The public artifact is controlled by the explicit allowlist in `scripts/build_public_site.py`.

## Current authority

Current website facts must come from the systems that own them:

- website source and implementation: live `GoreeCloud/static-websites`;
- public route model: `sites/url-namespace.json`;
- Glaze lifecycle and shared contract: live `GoreeCloud/glaze-ui`;
- current repository metadata: live GitHub;
- current Suite membership: the authoritative reconciled Suite inventory;
- branding: `GoreeCloud/branding-assets`;
- product lifecycle/runtime claims: each owning product repository and governed project record;
- current website work and blockers: GoreeCloud Tasks Management.

Repository-only snapshots do not override those sources.

## Current records

### `glaze-ui-conformance.md`

Current website-specific GLAZE UI V1.6 consumer contract and downstream acceptance boundary.

### `stability-baseline.md`

Current website stability definition, one-site public architecture, and required pre-production gates.

### `governance-readiness.md`

Website-specific governance applicability record for the anonymous static architecture.

### `wardveil-security-and-observability.md`

Website-specific security and operational-observability boundary. Domain authority remains with Wardveil Security and GoreeCloud Observability where applicable.

### `release-readiness-checklist.md`

Reusable release procedure. Candidate-specific evidence must remain bound to the exact reviewed revision.

### `release-evidence-template.md`

Template only. It does not prove that any acceptance lane was completed.

## Historical retained records

Several files remain only as dated provenance or review snapshots. Their contents may accurately describe an earlier date but are **not current authority** unless a later governing record explicitly revalidates them.

This includes:

- `repository-portfolio.json` — dated 2026-08-31 repository snapshot;
- `public-runtime-status.json` — dated 2026-08-31 runtime/product snapshot;
- `suite-portfolio.json` — dated 2026-09-01 Suite snapshot;
- `glaze-ui-2.0-public-sites.md` and `glaze-ui-2.1-public-sites.md` — historical Glaze public-web baselines;
- `posthog-telemetry-review.md` — retired telemetry review;
- historical release-evidence records; and
- older migration/normalization documentation whose exact scope is preserved by Git history.

Do not use a dated snapshot to override current live GitHub, Drive, product, deployment, or design-system state.

## Repository inventory boundary

The current `/github/` public page deliberately avoids a hard-coded repository total and does not publish private repository names.

When a visitor explicitly chooses to load the public repository catalog, the browser requests current public metadata from GitHub. That visitor-triggered public request is part of the current website design and supersedes the older repository-local snapshot model for current public repository discovery.

## Public-information boundary

Repository validation and documentation must distinguish:

- current state from historical state;
- product membership from lifecycle maturity;
- source presence from production acceptance;
- branch preview from production deployment;
- Glaze presentation from product/platform authority; and
- historical multi-site evidence from the one current website.

Passing CI does not authorize merge or production release.
