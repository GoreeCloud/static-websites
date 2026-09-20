# GoreeCloud Website Release Evidence Record Template

## Purpose

Use this repository-only template for one exact GoreeCloud Website release candidate.

A completed record documents evidence observed for that exact candidate. It does not authorize merge, deployment, Stable classification, Glaze consumer acceptance, or production release.

If the candidate SHA changes, create or update evidence only after explicitly revalidating the affected lanes. Never silently transfer acceptance from an older revision.

## 1. Candidate identity

- Review date/time:
- Exact 40-character candidate SHA:
- Pull request:
- Source branch:
- Target branch:
- Reviewer / reviewer role:
- Main website validation run:
- Retained-site validation run:
- Cloudflare immutable branch-preview URL:
- Cloudflare branch-preview alias:

Candidate freeze:
- [ ] Exact SHA confirmed.
- [ ] PR still targets `main`.
- [ ] No later unreviewed commit is being treated as covered.
- [ ] Candidate has not been merged unintentionally.

## 2. Current-authority verification

Record the authoritative source checked for each claim.

- One current website:
- Canonical six-path route registry:
- Nine Integral Platform Systems:
- GoreeCloud Sync separate-governance boundary:
- 45-product Suite registry:
- Office current implementation state:
- Firefox extension/client current source and release state:
- GitHub live repository authority:
- Branding authority:

Result:
- [ ] Public claims are current and evidence-scoped.
- [ ] No historical snapshot is being presented as current authority.

## 3. Automated source/artifact evidence

- URL namespace:
- Historical manifest boundary:
- Public site semantics:
- Public link/sitemap surface:
- Glaze V1.6 target:
- Isolated artifact build:
- Artifact exact-byte/allowlist validation:
- Responsive Chrome smoke:
- 48px interactive-target gate:
- JavaScript syntax:
- Other applicable security/privacy/performance checks:

Result:
- [ ] All required automated gates passed on the exact candidate.
- [ ] Any exception/failure is documented rather than ignored.

## 4. Branch-preview evidence

- Provider deployment check:
- Exact candidate SHA shown by provider:
- Immutable preview URL:
- Stable branch alias:
- Preview fetch/result:
- Preview corresponds to exact PR head: Yes / No / Unverified

Result:
- [ ] Exact branch preview succeeded.
- [ ] Provider success is not being substituted for human acceptance.

## 5. Human visual acceptance

Review:
- Home
- Integral Platform Systems
- Suite
- Office Suite
- Firefox
- GitHub

Record:
- Desktop result:
- Tablet result:
- Mobile/compact result:
- Light appearance:
- Dark appearance:
- Reduced motion:
- Reduced transparency:
- Increased contrast / forced colors:
- Navigation and focus:
- Visual defects found/resolved:

Result:
- [ ] Human visual review accepted the exact candidate.

## 6. Keyboard, touch, and assistive technology

- Keyboard-only navigation:
- Focus order:
- Focus visibility:
- 48px interaction target review:
- Text resize/zoom:
- Screen reader / assistive technology:
- Touch review:
- Accessibility defects and resolutions:

Result:
- [ ] Applicable human accessibility/AT acceptance is complete.

## 7. Privacy and security

- Analytics/telemetry state:
- GitHub visitor-triggered request boundary:
- CSP:
- Permissions Policy:
- Security reporting contact:
- Secret/private-data review:
- Security/privacy claim review:

Result:
- [ ] Current public artifact preserves the approved privacy/security boundary.

## 8. Performance and browser compatibility

- Performance evidence:
- Desktop browser evidence:
- Mobile browser evidence:
- Optional-JavaScript failure behavior:
- Regressions/waivers:

Result:
- [ ] Applicable performance/browser acceptance is complete.

## 9. Glaze UI consumer evidence

- Required version: 1.6.0
- Stable lifecycle authority:
- Accepted published Glaze source:
- Website exact reference revision:
- Repository-local evidence reference:
- Human review complete:
- Current consumer-registry repository:
- Registry status:
- Registry update PR/commit if applicable:

Result:
- [ ] Current Glaze consumer acceptance is supported by exact-revision evidence.
- [ ] No acceptance is claimed solely from shared Glaze Stable status.

## 10. Merge authorization

Risk warning recorded:
Explicit user confirmation:
Authorization scope:
Candidate SHA at authorization:
Merge method:
Rollback plan:

Result:
- [ ] Merge was explicitly authorized for the exact candidate.

## 11. Production verification

Complete only after authorized merge.

- Main merge revision:
- Production deployment identifier:
- Production deployment revision:
- Canonical home verification:
- Six canonical destinations:
- Headers/CSP:
- Redirects:
- Production responsive/browser result:
- Production accessibility follow-up if required:
- Rollback availability:

Result:
- [ ] Exact production deployment verified.
- [ ] Production acceptance is supported rather than inferred.

## 12. Final reconciliation

- [ ] Pull Request operational record updated.
- [ ] Tasks Management updated.
- [ ] Directly affected repository documentation updated.
- [ ] Glaze consumer registry reconciled where applicable.
- [ ] Canonical Drive/GitHub indexes reconciled if materially affected.
- [ ] No unresolved blocker makes completion inaccurate.

Final disposition:
Accepted / Rejected / Blocked / Superseded / Unverified

Notes:
