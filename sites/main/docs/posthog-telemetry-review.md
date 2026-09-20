# GoreeCloud Public Website — Retired PostHog Telemetry Review

**Status:** Historical / retired from the current website rebuild  
**Current website source:** `GoreeCloud/static-websites/sites/main`

## Current state

The current GoreeCloud website rebuild does **not** load PostHog or another analytics runtime.

The current public artifact allowlist excludes the former telemetry runtime, and the active Content Security Policy does not permit PostHog script or connection origins.

The website does not require analytics, behavioral tracking, session replay, advertising, fingerprinting, or a telemetry identity in order to function.

The `/github/` catalog is not analytics. It makes a visitor-triggered request to the public GitHub API only after the visitor explicitly chooses **Load current public repositories**.

## Historical boundary

Earlier revisions evaluated a narrowly scoped, consent-gated PostHog integration. That review is retained in Git history as historical evidence for the revisions to which it applied.

Those earlier provider settings, event contracts, CSP permissions, consent controls, project identifiers, retention settings, and production-verification steps are not current website behavior and must not be represented as active.

## Reintroduction rule

If client telemetry is proposed again, it requires a fresh, explicitly authorized privacy review before source activation. The new review must define purpose, minimum data, consent behavior, retention, network origins, security/privacy controls, user controls, applicable Privacy Shield requirements, current CSP changes, and exact production acceptance evidence.

Historical approval does not automatically authorize a future telemetry implementation.
