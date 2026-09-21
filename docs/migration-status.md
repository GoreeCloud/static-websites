# Static Website Retirement and Consolidation Status

**Canonical repository:** `GoreeCloud/static-websites`  
**Reviewed:** 2026-09-21  
**Current website:** `https://www.goreecloud.com`  
**Current website count:** 1

## Current public state

`www.goreecloud.com` is the only current GoreeCloud website.

Former public website hostnames and standalone public-site deployments recorded in older migration and production-acceptance evidence are no longer current website authority. They are retired under the completed controlled website-retirement workflow.

The absence of a former hostname, redirect, CNAME, Pages binding, or public endpoint is expected retirement state when that surface has been retired. Do not recreate an obsolete endpoint solely because a historical verifier expects it.

## Repository/source state

This repository may still contain multiple `sites/<site-id>/` packages and a manifest that records their migration history. Those packages are retained temporarily for source preservation, evidence, recovery, dependency review, and retirement cleanup.

Their presence does **not** mean that multiple GoreeCloud websites currently exist.

For current-state interpretation:

- `sites/main` corresponds to the retained `www.goreecloud.com` website;
- other site packages are historical/retirement material unless a later authoritative decision explicitly reclassifies one;
- legacy `canonical_domain` and `deployment_state` fields in migration records are historical migration evidence when they conflict with the September 20, 2026 retirement direction; and
- web applications and service endpoints remain governed by their application/service records rather than this static-website inventory.

## Verified retirement milestones

The completed GoreeCloud retirement workflow verified that:

- PR #106 was re-scoped to preserve `www.goreecloud.com` while removing the requirement for the retired Firefox informational hostname;
- PR #106 merged as `3ce6de95d0b16a89bf265e5a990cd6c5131e0433` after all 16 exact-head pull-request workflows passed;
- focused cleanup PR #107 merged as `ac0bf579cd5b96fb045acdf8d646a8e4d528d06d` after its applicable checks passed;
- retained one-site rebuild PR #109 merged as `4e03d06f7e6681b5a3517da5d7cbfc11cabc5834`;
- workflow-retirement PR #115 merged as `2d703a6f1c4be793db3e8504bb329b3f4a48cd56` after exact-head and post-merge retained-site validation passed; and
- pre-existing multi-site migration pull requests were dispositioned as superseded where appropriate.

Repository evidence is combined with authoritative Porkbun DNS verification and authenticated Cloudflare inventory: the 14 retired secondary hostnames are absent, Cloudflare retains only `goreecloud-website`, and `www.goreecloud.com` remains the only current website.

## Remaining retirement work

None. Secondary public website retirement was verified complete on September 21, 2026.

Preserved historical secondary-site source may remain in this repository. Any later removal or archival of that evidence is separate maintenance and is not a retirement-completion blocker.

## Historical evidence

Older migration states such as `inventory-confirmed`, `validated-in-central-repo`, `production-verified`, and `legacy-source-retired` describe the migration history at the time they were recorded.

They must be preserved as historical evidence where required, but they must not override the current single-website state.

## Completion boundary

The secondary-site retirement program is complete as of September 21, 2026.

Completion was verified across authoritative DNS, Cloudflare provider inventory, deployment automation, repository state, Drive/GitHub documentation, indexes, and task management. `www.goreecloud.com` remains the permanent retained website; no secondary public website is currently authorized or published.
