# GoreeCloud Website Release Readiness Checklist

## Purpose

This repository-only checklist defines the minimum evidence required before an exact GoreeCloud Website candidate may be considered for production acceptance.

Passing CI is necessary evidence but does **not** authorize merge, Cloudflare production deployment, DNS changes, public release, Glaze consumer acceptance, or Stable status.

If the candidate SHA changes, re-run every affected check and bind human evidence to the new exact revision.

## 1. Candidate freeze

- [ ] Record the exact 40-character candidate SHA.
- [ ] Confirm the candidate is the intended head of the active pull request.
- [ ] Confirm the base branch is `main`.
- [ ] Confirm no unreviewed commit is being treated as covered by older evidence.
- [ ] Confirm the public artifact is produced only by the current `PUBLIC_FILES` allowlist.
- [ ] Confirm repository-only docs, tests, historical source, and unused assets remain outside `dist/`.

## 2. Current authority checks

- [ ] Verify `www.goreecloud.com` is the one current website.
- [ ] Verify `sites/url-namespace.json` contains the current six canonical destinations.
- [ ] Verify the Integral Platform Systems page contains the authoritative nine systems and preserves the separate GoreeCloud Sync boundary.
- [ ] Verify the Suite page uses the current reconciled 45-product registry.
- [ ] Verify Office implementation claims match the live Office repository and distinguish implemented from planned capability.
- [ ] Verify Firefox source/release claims match canonical repositories and release-state records.
- [ ] Verify the GitHub page does not publish private repository names or a hard-coded repository total.
- [ ] Verify current official branding against `GoreeCloud/branding-assets`.

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
- [ ] Current V1.6 target validation passes.
- [ ] Chrome acceptance passes all six canonical pages at representative desktop, tablet, and compact/mobile viewports.
- [ ] Governed core interactive controls satisfy the 48px floor.
- [ ] No unintended horizontal overflow is present.
- [ ] JavaScript syntax validation passes.

## 4. Branch-preview gate

Before merge:

- [ ] Cloudflare Pages reports a successful branch-preview deployment for the exact candidate SHA.
- [ ] Record the exact immutable preview URL.
- [ ] Record the stable branch-preview alias.
- [ ] Confirm the preview corresponds to the current PR head.
- [ ] Do not treat provider deployment success alone as human visual acceptance.

## 5. Human visual and interaction review

Review all six canonical destinations on the exact branch preview.

- [ ] Desktop visual hierarchy and spacing are polished.
- [ ] Tablet layout is purpose-built and not merely compressed desktop.
- [ ] Phone/compact layout remains readable with no clipping or horizontal scrolling.
- [ ] Light appearance is coherent.
- [ ] Dark appearance is coherent.
- [ ] Reduced-motion behavior is acceptable.
- [ ] Reduced-transparency fallback is acceptable.
- [ ] Increased-contrast / forced-colors behavior remains usable where available.
- [ ] Navigation opens, closes, and reflows correctly.
- [ ] Focus indicators are visible and logical.
- [ ] Keyboard-only navigation reaches every required interactive control.
- [ ] Pointer/touch targets are practical and meet the 48px general floor.
- [ ] No placeholder, dead, misleading, duplicated, or visibly unfinished production control remains.

## 6. Accessibility and assistive-technology review

- [ ] Landmark and heading structure is understandable.
- [ ] Link and control names make sense without surrounding visual context.
- [ ] Keyboard focus order is logical.
- [ ] Text resize/zoom does not cause loss of information or functionality.
- [ ] Screen-reader/assistive-technology review is completed for representative pages and primary navigation.
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

## 9. Glaze UI consumer acceptance

- [ ] The website targets GLAZE UI V1.6 / 1.6.0 Stable.
- [ ] Exact Glaze lifecycle/source identities match `glaze.lock.json`.
- [ ] Repository-local V1.6 evidence is bound to the exact website candidate.
- [ ] Required human visual/accessibility/performance lanes are complete.
- [ ] The authoritative Glaze consumer registry is reconciled to the canonical website repository.
- [ ] Do not mark the Website consumer `accepted-v1` until governed product-specific acceptance is actually complete.

## 10. Merge and production transition

Before merge, provide the required risk warning and obtain explicit confirmation.

After authorized merge:

- [ ] Verify the exact merge revision on `main`.
- [ ] Verify the Cloudflare production deployment corresponds to that exact reviewed revision.
- [ ] Verify canonical `https://www.goreecloud.com/` content, headers, redirects, and all six destinations.
- [ ] Re-run production browser/responsive checks as required.
- [ ] Confirm rollback remains available.
- [ ] Reconcile directly affected README/docs, Glaze consumer registry, Pull Request record, repository indexes where applicable, and Tasks Management.
- [ ] Only then record production acceptance if every applicable gate is satisfied.

## Completion rule

Do not call the website rebuild complete while a required human review, Glaze consumer acceptance, merge/deployment verification, documentation/index reconciliation, task obligation, or material uncertainty remains unresolved.
