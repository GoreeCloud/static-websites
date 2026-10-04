# GoreeCloud Main Website — Glaze V1.7 Consumer Contract

## Current contract

- Target Glaze version: **V1.7 / 1.7.0 Stable**
- Canonical design-system repository: `GoreeCloud/glaze`
- Bounded Stable promotion revision: `1a5756daed2294155be2e9972b24f580f6222b7b`
- Stable runtime entrypoint: `js/glaze-v1.7.0.mjs`
- Entrypoint Git blob: `c669d9c6f1738b2a56cb02b2e00fa0ca229117c0`
- Stable runtime baseline: **1.6.0**
- Website consumer state: **source-adopted-unaccepted / pending-human-acceptance**
- Exact website candidate: `17303b6c7381faaa0e89ce6175ce24048fb56a12`
- Machine/deployment evidence: **complete for the exact candidate**
- Final Glaze consumer acceptance: **not established**

Glaze V1.7.0 is the current shared Stable/Anchor target. Its bounded Stable runtime intentionally inherits the accepted V1.6.0 runtime and excludes unverified V1.7 Development behavior. That compatibility choice permits a bounded source migration, but it does not transfer downstream website acceptance.

## Current website implementation

The retained website source is `GoreeCloud/static-websites/sites/main`. Every canonical page records the V1.7 target and the fail-closed `source-adopted-unaccepted` state. The exact design-system source pin is recorded in `glaze.lock.json` and verified by repository CI.

The website retains its existing accessibility and adaptation foundations, including the 48 px interaction floor, responsive layouts, visible keyboard focus, reduced-motion and reduced-transparency behavior, increased-contrast and forced-colors handling, light/dark appearance, bounded mobile navigation, and compact-width overflow checks.

## Acceptance boundary

The V1.6 consumer record remains historical exact-revision evidence only. Current V1.7 adoption starts a fresh evidence cycle in `acceptance/glaze-ui-v1.7-consumer-acceptance.json`.

For exact candidate `17303b6c7381faaa0e89ce6175ce24048fb56a12`, repository validation, website validation, rendered/responsive browser smoke, isolated-artifact checks, privacy/security validation, deployment, and deployed-byte readback are complete. Human visual, keyboard, assistive-technology, representative performance/resilience, and explicit owner acceptance remain pending.

The exact canonical readback is recorded in `acceptance/GLAZE-V1.7-CANONICAL-READBACK.md`. A source build, GitHub Actions run, canonical deployment, visual resemblance, or Glaze's own Stable lifecycle cannot independently grant final website consumer acceptance.

## Authority boundary

Glaze remains presentation authority only. Website presentation state cannot create Privacy Shield consent or privacy authorization, Wardveil security authority, runtime capability, deployment state, production state, or another product authority.

Historical V1.6 and earlier evidence remains useful provenance only for the exact bytes it reviewed.
