# GoreeCloud Website Stability Baseline

## Current source state

`www.goreecloud.com` is the one current GoreeCloud public website.

- Canonical source repository: `GoreeCloud/static-websites`
- Canonical site root: `sites/main`
- Website source version: **5.25.1**
- Exact deployed public-artifact revision: `17303b6c7381faaa0e89ce6175ce24048fb56a12`
- Current Glaze consumer state: **source-adopted-unaccepted / pending-human-acceptance**

Repository `main` may advance through repository-only evidence or documentation commits without changing public HTML bytes. Production and consumer-acceptance claims remain bound to the exact public artifact and evidence record, not merely to the newest repository commit.

## Current design-system baseline

The required shared design target is **Glaze V1.7 / 1.7.0 Stable**.

- Canonical repository: `GoreeCloud/glaze`
- Bounded Stable promotion revision: `1a5756daed2294155be2e9972b24f580f6222b7b`
- Stable runtime entrypoint: `js/glaze-v1.7.0.mjs`
- Entrypoint Git blob: `c669d9c6f1738b2a56cb02b2e00fa0ca229117c0`
- Immediate rollback/runtime baseline: **1.6.0**
- Consumer evidence: `acceptance/glaze-ui-v1.7-consumer-acceptance.json`

Glaze 1.7.0 intentionally inherits the accepted 1.6.0 runtime surface, but downstream website acceptance is not inherited automatically. Final Glaze consumer acceptance remains open until the required human and representative-performance lanes pass for the exact deployed public artifact and the GoreeCloud project owner explicitly accepts that revision.

## Current public-information baseline

The canonical route registry contains **eleven** destinations:

1. `/`
2. `/platform-systems/`
3. `/suite/`
4. `/android/`
5. `/office-suite/`
6. `/firefox/`
7. `/github/`
8. `/contact/`
9. `/design/`
10. `/security/`
11. `/privacy/`

Current public architecture uses the authoritative nine Integral Platform Systems. GoreeCloud Sync remains separately governed and is not a tenth Integral Platform System.

The Suite section uses the reconciled **45-product** registry across nine functional groups.

The GitHub section does not publish private repository names or a fixed repository count. Current public repository metadata is loaded from GitHub only after explicit visitor action.

## Current interface baseline

The website must preserve, at minimum:

- 48 px general interactive targets for governed core controls;
- phone, tablet, desktop, and narrow-phone responsiveness;
- no unintended horizontal scrolling or clipped controls;
- keyboard-operable navigation and actions with visible focus;
- accessible glyph mobile navigation with correct Open/Close state;
- reduced-motion and reduced-transparency behavior;
- increased-contrast and forced-colors behavior;
- current official GoreeCloud branding and artwork provenance;
- no placeholder or dead production controls; and
- graceful local failure/fallback behavior.

## Current exact-revision machine and deployment evidence

For public artifact revision `17303b6c7381faaa0e89ce6175ce24048fb56a12`:

- repository validation run `37191505046` passed;
- Main website validation run `37191505073` passed;
- pinned Glaze V1.7 source-target validation passed;
- isolated public-artifact and public-boundary validation passed;
- canonical-page Chrome responsive/interaction smoke passed;
- canonical production readback matched repository HTML byte-for-byte across all eleven routes, totaling **115,559 HTML bytes**; and
- the changed 404 body plus the Glaze and Mesh SVG assets also matched exact source bytes.

These results establish machine and deployment evidence, not final human acceptance.

## Remaining acceptance boundary

The following lanes remain open for the exact deployed artifact:

- human visual review across representative desktop, tablet, modern-phone, and narrow-phone viewports;
- keyboard-only review;
- assistive-technology review;
- representative browser/device performance and resilience review; and
- explicit GoreeCloud project-owner acceptance.

The canonical active task record is maintained in GoreeCloud Tasks Management as **Public Website — Glaze V1.7 Human Acceptance Task List.docx**.

## Stability definition

A changed public website revision is not final-accepted merely because source exists, CI is green, a merge completed, or a deployment provider reports success.

The required transition sequence includes, as applicable:

1. exact source and public-artifact validation;
2. current Glaze target validation;
3. representative responsive/browser validation;
4. candidate deployment/preview evidence when configured;
5. human visual and keyboard review;
6. appropriate accessibility and assistive-technology review;
7. representative performance/resilience evidence;
8. governed merge to the production branch;
9. exact production deployment/readback;
10. canonical-domain byte/header/browser verification;
11. rollback/recovery readiness; and
12. final documentation, Glaze consumer record, canonical-index, and Tasks Management reconciliation.

If a source-changing correction creates a new public artifact revision, acceptance must be rebound and every affected lane revalidated. Historical acceptance must not be grandfathered to changed public bytes.

## Historical boundary

Earlier Glaze UI/Glaze 2.x, V1.3, V1.4, and V1.6 public-web baselines; multi-site inventories; former satellite domains; and dated repository-count snapshots remain historical evidence only. They do not override the current one-site topology, Glaze V1.7 target, or exact current consumer-acceptance boundary.
