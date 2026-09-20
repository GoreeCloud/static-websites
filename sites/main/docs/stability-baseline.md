# GoreeCloud Website Stability Baseline

## Current source state

`www.goreecloud.com` is the one current GoreeCloud website.

The active rebuild is being reviewed in `GoreeCloud/static-websites` through pull request #109. The candidate is not production-accepted merely because source validation, branch preview deployment, or responsive browser checks pass.

The repository `VERSION` file remains release metadata. It does not establish current design-system authority, deployment identity, Stable status, or production acceptance by itself.

## Current design-system baseline

The required design-system target is **GLAZE UI V1.6 / 1.6.0 Stable**.

- Canonical repository: `GoreeCloud/glaze-ui`
- Stable lifecycle authority: `081527eff1c5fe5001b6b9598d60439c8fb3c5e3`
- Accepted published release source: `a7180679ea851389e0f3004515f9a25f420e716d`
- Stable runtime entrypoint: `js/glaze-v1.6.0.mjs`
- Website consumer state: `migration-candidate-unaccepted`

The Glaze consumer registry requires fresh repository-local V1.6.0 acceptance. Shared design-system Stable status does not make the website production-eligible.

## Current public-information baseline

The retained website uses six canonical destinations:

1. `/`
2. `/platform-systems/`
3. `/suite/`
4. `/office-suite/`
5. `/firefox/`
6. `/github/`

Current public architecture uses the authoritative nine Integral Platform Systems. GoreeCloud Sync remains separately governed and is not a tenth Integral Platform System.

The Suite section uses the reconciled 45-product registry across nine functional groups.

The GitHub section does not publish private repository names or a fixed repository count. Current public repository metadata is loaded from GitHub only after explicit visitor action.

## Current interface baseline

The website must preserve, at minimum:

- 48px general interactive targets for governed core controls;
- phone, tablet, and desktop responsiveness;
- no unintended horizontal scrolling;
- keyboard-operable navigation and actions;
- visible focus treatment;
- reduced-motion and reduced-transparency behavior;
- increased-contrast and forced-colors behavior;
- current official GoreeCloud branding;
- no placeholder or dead production controls; and
- graceful failure/fallback behavior.

The current website logo bytes match the approved `official/goreecloud-logo.svg` asset in the canonical `GoreeCloud/branding-assets` repository.

## Stability definition

A website revision is not Stable or production-accepted until the exact candidate satisfies all applicable source, artifact, human review, accessibility, privacy, security, performance, branch-preview, merge, deployment, rollback, and post-deployment verification requirements.

Required transition sequence includes:

1. exact source and public-artifact validation;
2. current Glaze target validation;
3. representative responsive/browser validation;
4. successful exact branch preview;
5. human visual and keyboard review;
6. appropriate accessibility and assistive-technology review;
7. explicit authorization for merge;
8. merge to the protected production branch;
9. exact production deployment;
10. canonical-domain deployed-byte/header/browser verification; and
11. final documentation, Glaze consumer registry, and task reconciliation.

A passing branch preview alone is not a Stable release. A merge alone is not a Stable release.

## Historical boundary

Earlier Glaze 2.x, V1.3, and V1.4 public-web baselines, multi-site inventories, repository totals, and former standalone website-domain records are historical evidence only. They must not be interpreted as the current website, current design-system target, or current production topology.
