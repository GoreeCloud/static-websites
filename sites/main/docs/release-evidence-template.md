# GoreeCloud Website Release Evidence Record Template

## Purpose

Use this repository-only template for one exact GoreeCloud Website release candidate.

A completed record documents evidence observed for that exact candidate. It does not itself authorize a merge, deployment, Stable classification, Glaze consumer acceptance, DNS change, or production release. Evidence from one candidate must not be silently reused for a changed candidate.

All release-evidence timestamps use Central Time (`America/Chicago`) and a 12-hour time format. This template and every generated record must remain outside the website `dist/` artifact. Historical evidence must remain distinguishable from current state.

Do not place credentials, tokens, private keys, private IP addresses, private hostnames, private topology, or other non-public operational material in a release-evidence record. Do not paste raw logs when a bounded run ID, result, checksum, Git blob ID, or protected-system reference is sufficient. Sensitive evidence belongs in the appropriate protected system.

A checksum, Git blob ID, workflow result, or deployment identifier is evidence for the specific property it validates; it is not proof of unrelated security, privacy, accessibility, or release readiness.

## 1. Candidate identity

- Review date/time:
- Exact candidate commit (40-character SHA):
- Pull request:
- Source branch:
- Intended base branch: `main`
- Reviewer / reviewer role:
- Main website validation run:
- Retained-site validation run:
- Provider deployment / preview identifier:

Candidate freeze:
- [ ] Exact candidate SHA confirmed.
- [ ] No later unreviewed commit is being treated as covered by this record.
- [ ] Pull request still targets the intended base branch.
- [ ] Candidate has not been merged or promoted unintentionally.

Evidence/notes:

## 2. Automated validation evidence

Record exact run IDs or bounded results for the applicable current gates.

- URL namespace / eleven canonical routes:
- Current public semantics:
- Glaze V1.7 source-target validation:
- Isolated artifact build and allowlist:
- Responsive Chrome smoke:
- Privacy/security/public-boundary checks:
- JavaScript syntax:
- Unit tests:
- Other applicable checks:

Result:
- [ ] All required automated gates passed on the exact candidate.
- [ ] Any failure or exception is documented below instead of being silently ignored.

Evidence/notes:

## 3. Human visual and interaction acceptance

Review all eleven canonical routes at representative desktop, tablet, modern-phone, and narrow-phone sizes in applicable appearance modes.

Record:
- Desktop result:
- Tablet result:
- Modern-phone result:
- Narrow-phone result:
- Light appearance:
- Dark appearance:
- Reduced motion / transparency:
- Increased contrast / forced colors:
- Navigation / focus:
- Visual defects found and resolved:

Result:
- [ ] Accepted for this exact candidate.
- [ ] No material visual or interaction defect remains hidden by automated validation.

Evidence/notes:

## 4. Accessibility acceptance

Record:
- Keyboard-only navigation:
- Focus order and focus visibility:
- Text resize / zoom / reflow:
- Screen reader or representative assistive technology:
- Touch-target review:
- Accessibility defects and resolutions:

Result:
- [ ] Human acceptance completed for this exact candidate.
- [ ] No formal WCAG conformance claim is being inferred solely from this record or CI.

Evidence/notes:

## 5. Progressive enhancement, resilience, privacy, and origin boundary

Record:
- Optional-JavaScript failure behavior:
- Reduced-motion / reduced-transparency fallback:
- Privacy / telemetry state:
- GitHub visitor-triggered request boundary:
- CSP / permissions / security-reporting state:
- Secret and private-data review:

Result:
- [ ] Progressive enhancement and resilience accepted.
- [ ] Privacy/origin behavior accepted.

Evidence/notes:

## 6. Publication and creative-rights boundary

Record:
- Repository publication / reachable-history review:
- Artwork / licensing / provenance review:
- Public/private disclosure boundary:

Result:
- [ ] Repository publication and creative-rights review is complete for the actions being authorized.
- [ ] No source-publication or third-party-rights claim exceeds the evidence actually reviewed.

Evidence/notes:

## 7. Isolated artifact and deployment boundary

Record:
- Public artifact revision:
- Build output:
- Provider deployment identifier:
- Canonical readback:
- Redirect / 404 behavior:
- Rollback availability:

Result:
- [ ] Isolated public artifact is verified as the production publication boundary.
- [ ] Fresh exact production verification passed.

Evidence/notes:

## 8. Glaze consumer evidence

- Required version: 1.7.0
- Stable authority: `GoreeCloud/glaze`
- Stable promotion revision:
- Website exact public-artifact revision:
- Consumer acceptance record:
- Human/performance lanes complete:
- Explicit owner acceptance:

Result:
- [ ] Current Glaze consumer acceptance is supported by exact-revision evidence.
- [ ] No acceptance is claimed solely from shared Glaze Stable status.

Evidence/notes:

## 9. Release authorization

- Merge authorization:
- Production-release authorization:
- Authorizing person/role:
- Authorization date/time:
- Authorization scope:
- Candidate SHA at authorization:
- Merge method:
- Rollback plan:

Result:
- [ ] Authorization is recorded only for the exact action and exact candidate actually approved.

Evidence/notes:

## 10. Post-release production verification

- Main merge revision:
- Production deployment revision:
- Production verifier result:
- Production verification date/time:
- Canonical route/readback result:
- Header / redirect / 404 result:
- Production browser follow-up:
- Rollback availability:

Result:
- [ ] Production verification passed without a material discrepancy.
- [ ] Production acceptance is supported rather than inferred.

Evidence/notes:

## 11. Final reconciliation

- [ ] Tasks Management updated.
- [ ] Directly affected repository documentation updated.
- [ ] Glaze consumer record reconciled where applicable.
- [ ] Canonical Drive/GitHub indexes reconciled if materially affected.
- [ ] No unresolved blocker makes completion inaccurate.

## Final candidate disposition

Select exactly one final candidate disposition only when the record leaves the working state:

- [ ] ACCEPTED
- [ ] BLOCKED
- [ ] REJECTED
- [ ] SUPERSEDED

Evidence/notes:
