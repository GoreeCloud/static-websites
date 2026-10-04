# GoreeCloud Website Release Readiness Checklist

## Purpose

This repository-only checklist defines the minimum evidence required before an exact GoreeCloud Website candidate may be considered for production acceptance.

Passing CI is necessary evidence but does **not** by itself authorize merge, production publication, DNS changes, public release, Glaze consumer acceptance, or Stable status.

If the candidate SHA or public artifact bytes change, re-run every affected check and bind human evidence to the new exact revision.

## 1. Candidate freeze

- [ ] Record the exact 40-character candidate SHA.
- [ ] Confirm the candidate is the intended head of the active pull request.
- [ ] Confirm the base branch is `main`.
- [ ] Confirm no unreviewed commit is being treated as covered by older evidence.
- [ ] Confirm the public artifact is produced only by the current `PUBLIC_FILES` allowlist.
- [ ] Confirm repository-only docs, tests, historical source, and unused assets remain outside `dist/`.

## 2. Current authority checks

- [ ] Verify `www.goreecloud.com` is the one current website.
- [ ] Verify `sites/url-namespace.json` contains the current **eleven** canonical destinations.
- [ ] Verify the Integral Platform Systems page contains the authoritative nine systems and preserves the separate GoreeCloud Sync boundary.
- [ ] Verify the Suite page uses the current reconciled **45-product** registry.
- [ ] Verify Android lifecycle claims are evidence-scoped and do not promote products from repository activity alone.
- [ ] Verify Office implementation claims match the live `GoreeCloud/office` repository and distinguish implemented from planned capability.
- [ ] Verify Firefox source/release claims match the canonical `GoreeCloud/firefox-addons` repository and application-owned client repositories.
- [ ] Verify the GitHub page does not publish private repository names or a hard-coded repository total.
- [ ] Verify current official branding and artwork provenance against `GoreeCloud/branding-assets`.
- [ ] Verify Privacy Shield and Wardveil lifecycle text matches their current authoritative records without manufacturing production or Stable status.

## 3. Automated source and artifact gates

Run the current governed checks on the exact candidate:

```bash
python scripts/validate_url_namespace.py
python scripts/validate_manifest.py
python sites/main/scripts/validate_site.py
python sites/main/scripts/validate_public_surface.py
python sites/main/scripts/validate_glaze_ui.py
python sites/main/scripts/build_public_site.py
python sites/main/scripts/validate_build_artifact.py
python sites/main/scripts/browser_artifact_smoke.py
node --check sites/main/js/theme-init-v8.js
node --check sites/main/js/site-v8.js
```

Required evidence:

- [ ] The retained-site repository workflow is green on the exact SHA.
- [ ] The Main website validation workflow is green on the exact SHA.
- [ ] The exact artifact contains only allowlisted public files.
- [ ] Current **Glaze V1.7 / 1.7.0** target validation passes against the pinned authority.
- [ ] Chrome automation passes all eleven canonical pages at the governed representative viewports.
- [ ] Governed core interactive controls satisfy the 48 px floor.
- [ ] No unintended horizontal overflow is present.
- [ ] JavaScript syntax validation passes.

## 4. Candidate deployment / preview gate

When a provider preview or candidate deployment is part of the release path:

- [ ] The provider reports successful deployment for the exact candidate SHA.
- [ ] Record the immutable preview/deployment URL or provider identifier when available.
- [ ] Confirm any stable branch alias resolves to the current candidate.
- [ ] Do not treat provider deployment success alone as human visual acceptance.

If an immutable preview is not available, record that limitation explicitly and preserve exact-revision production verification as a separate required gate.

## 5. Human visual and interaction review

Review all eleven canonical destinations for the exact candidate or exact deployed public artifact:

- [ ] Desktop visual hierarchy and spacing are polished.
- [ ] Tablet layout is purpose-built and not merely compressed desktop.
- [ ] Modern-phone and narrow-phone layouts remain readable with no clipping or horizontal scrolling.
- [ ] Light appearance is coherent.
- [ ] Dark appearance is coherent.
- [ ] Reduced-motion behavior is acceptable.
- [ ] Reduced-transparency fallback is acceptable.
- [ ] Increased-contrast / forced-colors behavior remains usable where available.
- [ ] Navigation opens, closes, and reflows correctly.
- [ ] Focus indicators are visible and logical.
- [ ] Keyboard-only navigation reaches every required interactive control.
- [ ] Pointer/touch targets are practical and meet the 48 px general floor.
- [ ] No placeholder, dead, misleading, duplicated, or visibly unfinished production control remains.

## 6. Accessibility and assistive-technology review

- [ ] Landmark and heading structure is understandable.
- [ ] Link and control names make sense without surrounding visual context.
- [ ] Keyboard focus order is logical.
- [ ] Text resize/zoom does not cause loss of information or functionality.
- [ ] Screen-reader or other representative assistive-technology review is completed for navigation and representative page content.
- [ ] Any identified accessibility blocker is resolved and revalidated on the exact candidate.

Automated checks complement but do not replace this section.

## 7. Privacy and security review

- [ ] No advertising, behavioral analytics, session replay, fingerprinting, or unnecessary telemetry is active.
- [ ] Visitor-triggered GitHub discovery remains explicit and limited to public GitHub metadata.
- [ ] CSP and Permissions Policy reflect only required browser capabilities/origins.
- [ ] `.well-known/security.txt` has a valid reporting contact and current canonical references.
- [ ] No credential, secret, private host, private IP, internal topology, or non-public operational data is in the public artifact.
- [ ] Public security/privacy statements remain evidence-scoped and do not overclaim platform state.

## 8. Performance and browser review

- [ ] Representative pages meet the current website performance budgets.
- [ ] No unnecessary third-party runtime dependency has been introduced.
- [ ] Current supported modern desktop and mobile browser behavior is acceptable.
- [ ] Failure of optional JavaScript leaves core navigation/content understandable where practical.
- [ ] Representative browser/device performance and resilience evidence is recorded for the exact candidate.

## 9. Glaze V1.7 consumer acceptance

- [ ] The website targets **Glaze V1.7 / 1.7.0 Stable**.
- [ ] Exact Glaze lifecycle/source identities match `glaze.lock.json`.
- [ ] Repository-local V1.7 evidence is bound to the exact website public-artifact revision.
- [ ] Required human visual, keyboard, assistive-technology, and representative performance/resilience lanes are complete.
- [ ] `acceptance/glaze-ui-v1.7-consumer-acceptance.json` records the exact accepted revision and real reviewer/environment evidence.
- [ ] Explicit GoreeCloud project-owner acceptance is recorded.
- [ ] Do not mark the Website consumer `accepted-v1` until governed website-specific acceptance is actually complete.

## 10. Merge and production transition

Before merge, satisfy the current GoreeCloud governance requirements for authorization, risk, review, exact-head checks, and rollback. Owner standing delegation may cover ordinary governed project merges; exceptional actions still require the task-specific authority defined by governing instructions.

After governed merge:

- [ ] Verify the exact merge revision on `main`.
- [ ] Verify the production deployment corresponds to the exact reviewed public artifact.
- [ ] Verify canonical `https://www.goreecloud.com/` content, headers, redirects, 404 behavior, and all eleven canonical destinations.
- [ ] Re-run production browser/responsive checks as required.
- [ ] Confirm rollback remains available.
- [ ] Reconcile directly affected README/docs, the Glaze consumer record, project record, canonical indexes where materially affected, and Tasks Management.
- [ ] Only then record production acceptance if every applicable gate is satisfied.

## Completion rule

Do not call the website or Glaze consumer acceptance complete while a required human review, representative performance/resilience review, owner acceptance, deployment verification, documentation/index reconciliation, task obligation, or material uncertainty remains unresolved.
