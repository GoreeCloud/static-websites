# GoreeCloud Main Website — Glaze V1.7 Consumer Contract

## Current contract

- Target Glaze version: **V1.7 / 1.7.0 Stable**
- Canonical design-system repository: `GoreeCloud/glaze`
- Bounded Stable promotion revision: `1a5756daed2294155be2e9972b24f580f6222b7b`
- Stable runtime entrypoint: `js/glaze-v1.7.0.mjs`
- Entrypoint Git blob: `c669d9c6f1738b2a56cb02b2e00fa0ca229117c0`
- Stable runtime baseline: **1.6.0**
- Website consumer state: **source-adopted-unaccepted**
- Production eligibility: **not established**

Glaze V1.7.0 is the current shared Stable/Anchor target. Its bounded Stable runtime intentionally inherits the accepted V1.6.0 runtime and excludes unverified V1.7 Development behavior. That compatibility choice permits a bounded source migration, but it does not transfer downstream website acceptance.

## Current website implementation

The retained website source is `GoreeCloud/static-websites/sites/main`. Every canonical page records the V1.7 target and the fail-closed `source-adopted-unaccepted` state. The exact design-system source pin is recorded in `glaze.lock.json` and verified by repository CI.

The website retains its existing accessibility and adaptation foundations, including the 48 px interaction floor, responsive layouts, visible keyboard focus, reduced-motion and reduced-transparency behavior, increased-contrast and forced-colors handling, light/dark appearance, bounded mobile navigation, and compact-width overflow checks.

## Acceptance boundary

The V1.6 consumer record remains historical exact-revision evidence only. Current V1.7 adoption starts a fresh evidence cycle in `acceptance/glaze-ui-v1.7-consumer-acceptance.json`.

Before V1.7 consumer acceptance may be claimed, one exact website revision must complete all applicable machine, rendered/responsive, privacy/security, accessibility, keyboard, assistive-technology, representative performance/resilience, rollback, deployment, deployed-byte/readback, and owner-acceptance obligations.

A source build, GitHub Actions run, Cloudflare preview, visual resemblance, or Glaze's own Stable lifecycle cannot independently grant website production acceptance.

## Authority boundary

Glaze remains presentation authority only. Website presentation state cannot create Privacy Shield consent or privacy authorization, Wardveil security authority, runtime capability, deployment state, production state, or another product authority.

Historical V1.6 and earlier evidence remains useful provenance only for the exact bytes it reviewed.
