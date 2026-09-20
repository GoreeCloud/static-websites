# GoreeCloud Website — Retention and Retirement Roadmap

**Status:** Active retirement control  
**As of:** 2026-09-20  
**Canonical repository:** `GoreeCloud/static-websites`  
**Controlling task record:** GoreeCloud Main Website Retention and Public Website Retirement — Task List

## Current direction

`www.goreecloud.com` is the only current GoreeCloud website and is permanently retained.

The former multi-site expansion model is superseded. Secondary public websites, legacy informational hostnames, redirects, standalone hosting projects, and website-specific acceptance requirements are being retired unless an explicit later GoreeCloud decision reauthorizes them.

Historical source and exact-revision acceptance evidence remain history; they are not current deployment authority.

## Active roadmap

| ID | Obligation | Priority | Current state |
| --- | --- | --- | --- |
| WR-001 | Preserve `www.goreecloud.com` as the permanent GoreeCloud website, including its source, DNS, TLS, deployment path, privacy/security controls, and production verification. | High | Ongoing |
| WR-002 | Inventory and retire remaining secondary website exposure, including obsolete DNS/custom-domain bindings, redirects, Cloudflare Pages projects, Functions/Workers, and provider resources. | High | In progress |
| WR-003 | Reconcile website CI/CD so retired endpoints are not recreated or required by superseded checks while retained-site gates remain intact. | High | In progress |
| WR-004 | Preserve required source history, migration evidence, rollback/recovery material, and exact-revision acceptance evidence before deleting obsolete secondary-site resources. | High | In progress |
| WR-005 | Reconcile Drive and GitHub documentation so current-state text identifies only `www.goreecloud.com` as a website and historical multi-site records are clearly non-current. | High | In progress |
| WR-006 | Remove or archive retired secondary-site source and repository references only after dependency and preservation review. | Medium | Pending governed cleanup |
| WR-007 | Verify final retirement against authoritative DNS, hosting/provider, repository, documentation, index, and task state before closing the retirement program. | High | Pending final verification |

## Superseded roadmap work

The earlier roadmap for operating fourteen website packages, performing per-site Cloudflare cutovers, maintaining legacy informational-host redirects, and expanding website commerce is superseded by the September 20, 2026 retirement direction.

In particular:

- former multi-site GLAZE reconciliation obligations are no longer requirements for retired websites;
- Labs, Manager informational-site, and other secondary-site deployment cutovers are not active publication goals;
- legacy informational-host redirects must not be recreated solely to satisfy old migration checks;
- PW-006 through PW-008 commerce/payment/hosting expansion work is superseded and must not be implemented for retired websites; and
- retained-site validation principles continue to apply to `www.goreecloud.com` where they are actually relevant.

Historical roadmap text remains available in Git history and existing dated evidence. It must not be rewritten as though the former plan never existed.

## Evidence boundary

Repository source, a site package, a former custom domain, an old production-verification record, or a green historical workflow does not establish that a website is current.

Current website status requires current authoritative deployment/DNS evidence and the applicable GoreeCloud governance records.

## Completion rule

Do not close the retirement program merely because a hostname returns 404, a CNAME is absent, a Pages project is deleted, or source was removed.

Completion requires verification that:

- `www.goreecloud.com` remains intentionally retained and healthy;
- no other retired GoreeCloud public website remains supported or reachable unless explicitly authorized;
- obsolete provider resources and publication automation are dispositioned;
- required history/evidence is preserved;
- directly affected Drive and GitHub documentation and indexes reflect current state; and
- the controlling GoreeCloud task record is reconciled.
