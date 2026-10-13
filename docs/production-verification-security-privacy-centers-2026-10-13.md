# October 13, 2026 — Canonical Security and Privacy Center production readback

**Type:** independently observed public-site runtime evidence
**Environment:** GoreeCloud production public website
**Canonical repository:** `GoreeCloud/static-websites`
**Observed source revision:** `9ae21cf12e276ea7e553fcf2573318602886428e`
**Qualification outcome:** Source/deployed HTML byte match confirmed; **Glaze downstream human acceptance remains pending**.
**Authority effect:** None. Not production approval of Wardveil, Privacy Shield, or their runtime services.

## Method and scope

Two owner-authorized machines independently made read-only HTTPS GET requests using Python's standard-library HTTPS client with default TLS certificate verification and a bounded timeout. Both received final HTTP 200 responses. Each verifier computed SHA-256 and the Git blob SHA-1 of the returned **raw response body bytes**, and compared the Git blob identifier against the respective canonical GitHub source file at the above revision.

No public write endpoint, private authentication, secret, protected user resource, production mutation, recovery operation, redirect/cutover, or deployment action was exercised. No raw response body or client credential is retained in this record.

| Verifier | UTC capture time | Scope |
|---|---|---|
| GoreeCloud VPS | 2026-10-13T19:29:49.762309Z | Both routes |
| Independent owner-operated laptop | 2026-10-13T19:29:54.227996Z | Both routes |

## Verified observations

Both verifiers observed identical outputs:

| Route / exact source | HTTP | Response bytes | Git blob SHA-1 | Response SHA-256 |
|---|---|---:|---|---|
| `https://www.goreecloud.com/security/` → `sites/main/security/index.html` | 200 | 9,969 | `f3d6cac2b16954e0879298de0724bfe16b916715` | `678dbb1d759886f731f90e2b0e994ae20c3047d23c5d9a4881ee4847796f5c2b` |
| `https://www.goreecloud.com/privacy/` → `sites/main/privacy/index.html` | 200 | 10,166 | `40d4bcb1f8fc1e53bbbcde15f151ce1027157f96` | `4ad8dd14e311a504d10b8e18af0bab8246e81b3e6be64402febaa9e59d898105` |

Both endpoints returned `Content-Type: text/html; charset=utf-8` and remained on the expected canonical HTTPS URL. Source content continues to declare Glaze 1.7.0 and `source-adopted-unaccepted`.

The character lengths of source files returned through the GitHub text interface differ from the UTF-8 response **byte** lengths; the equal Git blob hashes establish exact byte identity.

## What this evidence proves

- At the specified observation times and two network vantage points, both public production routes were reachable over HTTPS and their bodies matched the canonical Git source bytes exactly.
- The current Glaze 1.7.0 static-site implementation was being served at those public URLs.
- This is fresh corroboration of the already completed public source/deployment/readback portion of the downstream Glaze consumer gate.

## What it does not prove

- Owner-reviewed visual, keyboard, assistive-technology, or representative-device acceptance.
- Representative performance, resilience, accessibility conformance, consent enforcement, privacy-policy correctness, or Wardveil security-protection effectiveness.
- Production deployment, authenticated runtime behavior, provider signing/key custody, quarantine, recovery, or Anchor qualification of either Wardveil or Privacy Shield.
- Any continuous uptime guarantee, CDN cache-invalidation guarantee, immutable release publication, or future source equivalence.

## Remaining gate and traceability

This is **historical, immutable-source-bound observation**. A later website release requires fresh verification.

- Wardveil's `security-center-glaze-acceptance` stays **blocked** pending owner reviews, performance/resilience acceptance, final approval, and legacy route transition.
- Privacy Shield's `privacy-center-glaze-acceptance` stays **blocked** for the same independent consumer acceptance and legacy transition requirements.
- The shared Glaze consumer registry remains `pending-human-acceptance` until its governing evidence-based transition is performed.

References: `GoreeCloud/wardveil/docs/integrations/security-center-static-site.md` and `GoreeCloud/privacy-shield/docs/integrations/privacy-center-static-site.md`.
