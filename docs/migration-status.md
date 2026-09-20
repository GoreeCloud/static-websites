# Static Website Retirement and Consolidation Status

**Canonical repository:** `GoreeCloud/static-websites`  
**Reviewed:** 2026-09-20  
**Current website:** `https://www.goreecloud.com`  
**Current website count:** 1

## Current public state

`www.goreecloud.com` is the only current GoreeCloud website.

Former public website hostnames and standalone public-site deployments recorded in older migration and production-acceptance evidence are no longer current website authority. They are retired or are being removed through the controlled website-retirement workflow.

The absence of a former hostname, redirect, CNAME, Pages binding, or public endpoint is expected retirement state when that surface has been retired. Do not recreate an obsolete endpoint solely because a historical verifier expects it.

## Repository/source state

This repository may still contain multiple `sites/<site-id>/` packages and a manifest that records their migration history. Those packages are retained temporarily for source preservation, evidence, recovery, dependency review, and retirement cleanup.

Their presence does **not** mean that multiple GoreeCloud websites currently exist.

For current-state interpretation:

- `sites/main` corresponds to the retained `www.goreecloud.com` website;
- other site packages are historical/retirement material unless a later authoritative decision explicitly reclassifies one;
- legacy `canonical_domain` and `deployment_state` fields in migration records are historical migration evidence when they conflict with the September 20, 2026 retirement direction; and
- web applications and service endpoints remain governed by their application/service records rather than this static-website inventory.

## Verified September 20 repository milestones

The controlling GoreeCloud task record verifies that:

- PR #106 was re-scoped to preserve `www.goreecloud.com` while removing the requirement for the retired Firefox informational hostname;
- PR #106 merged as `3ce6de95d0b16a89bf265e5a990cd6c5131e0433` after all 16 exact-head pull-request workflows passed;
- focused cleanup PR #107 merged as `ac0bf579cd5b96fb045acdf8d646a8e4d528d06d` after its applicable checks passed; and
- pre-existing multi-site migration pull requests were dispositioned as superseded where appropriate.

These milestones establish repository reconciliation progress. They do not by themselves prove that every secondary provider resource has been retired.

## Remaining retirement work

The controlled retirement workflow still requires:

1. verification of remaining public website exposure and provider resources;
2. retirement of obsolete secondary DNS/custom-domain and Pages resources;
3. reconciliation of CI/CD that still expects retired endpoints;
4. preservation of required historical/recovery evidence;
5. removal or archival of obsolete secondary-site source only after dependency review;
6. reconciliation of Drive and GitHub documentation; and
7. final authoritative verification that `www.goreecloud.com` is retained and no other website remains active unless separately authorized.

## Historical evidence

Older migration states such as `inventory-confirmed`, `validated-in-central-repo`, `production-verified`, and `legacy-source-retired` describe the migration history at the time they were recorded.

They must be preserved as historical evidence where required, but they must not override the current single-website state.

## Completion boundary

This document does not declare the secondary-site retirement program complete.

Final completion requires authoritative verification across DNS, hosting/provider resources, deployment automation, repository state, Drive/GitHub documentation, indexes, and task management.
