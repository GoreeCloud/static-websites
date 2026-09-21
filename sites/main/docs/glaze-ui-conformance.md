# GoreeCloud Main Website — GLAZE UI V1.6 Consumer Contract

## Current contract

- Target GLAZE UI version: **V1.6 / 1.6.0 Stable**
- Canonical design-system repository: `GoreeCloud/glaze-ui`
- Stable lifecycle authority: `081527eff1c5fe5001b6b9598d60439c8fb3c5e3`
- Accepted published release source: `a7180679ea851389e0f3004515f9a25f420e716d`
- Stable runtime entrypoint: `js/glaze-v1.6.0.mjs`
- Entrypoint Git blob: `7dfc863d6c39def97c263de80b21b73efe54db1e`
- Website consumer state: **migration-candidate-unaccepted**
- Production eligibility: **not established**

GLAZE UI V1.6.0 is the current shared Stable target. Shared Stable status does not grant downstream website conformance, deployment acceptance, or production acceptance.

## Current website implementation

The retained website is sourced from `GoreeCloud/static-websites/sites/main` and published only as `www.goreecloud.com` with path-based sections.

The current rebuild uses same-origin website presentation code and records its exact V1.6 target in `glaze.lock.json`. It does not claim that metadata, visual resemblance, or shared Glaze release status proves consumer acceptance.

The current interface implements the website's required adaptive and accessibility foundations, including:

- a 48px general interaction floor for governed core controls;
- responsive phone, tablet, and desktop layouts;
- visible keyboard focus;
- reduced-motion behavior;
- reduced-transparency fallback;
- increased-contrast treatment;
- forced-colors support;
- light and dark appearance;
- bounded mobile navigation; and
- horizontal-overflow failure checks at representative compact widths.

Repository-local browser validation exercises all six canonical website pages at 1180×900, 768×900, 390×844, and 320×844. Automated validation complements rather than replaces human review.

## Current information and authority boundary

The website reflects the current nine Integral Platform Systems: GoreeCloud Manager, Privacy Shield, Wardveil Security, Everkeep, Glaze UI, GoreeCloud Mesh, GoreeCloud Identity, GoreeCloud Policy, and GoreeCloud Observability.

GoreeCloud Sync remains separately governed synchronization capability and is not a tenth Integral Platform System.

The current Suite presentation uses the reconciled 45-product registry across nine functional groups. Live GitHub remains authoritative for current repository existence, naming, visibility, descriptions, and archive state.

The website does not load PostHog or another analytics runtime in the current rebuild. The public GitHub catalog is visitor-triggered and contacts only the public GitHub API after the visitor explicitly chooses to load it.

## Consumer acceptance boundary

The authoritative Glaze consumer registry still requires fresh repository-local V1.6.0 acceptance for GoreeCloud Website. A separate registry-reconciliation pull request may correct repository identity without granting acceptance.

Before this consumer can be treated as accepted for the current Stable Glaze contract, the exact website candidate must complete all applicable repository-local evidence, including human visual review, keyboard review, accessibility/assistive-technology review, performance review, responsive review, and any other required acceptance lanes.

If the candidate revision changes, exact-revision evidence must be revalidated. Prior V1.3, V1.4, 2.0, 2.1, or other historical website evidence does not automatically transfer.

## Deployment boundary

A successful source build, GitHub Actions run, or Cloudflare branch preview is not production acceptance.

Merge authorization, exact production deployment, deployed-byte and header verification, canonical-domain behavior, rollback readiness, and final production acceptance remain separate governed transitions.

Historical Glaze website migrations remain valid only as historical evidence for their exact reviewed revisions.
