# Donations: payment activation and publication readiness

**Scope:** `https://www.goreecloud.com/donations/` on the one retained public website  
**Canonical source:** `GoreeCloud/static-websites/sites/main/donations/`  
**Status (October 10, 2026):** PR [#142](https://github.com/GoreeCloud/static-websites/pull/142) is a source candidate. Financial collection is **not enabled**, and production publication of the new path is **unverified**.

## Purpose and current boundary

The Donations page explains voluntary ways to support GoreeCloud. It currently provides navigation to public source and an approved contact channel. There is no authorized verified payment destination, amount selector, checkout session, donor account, receipt system, or payment database. No monetary donations can be accepted through the page.

The project must remain ad-free, ownership-preserving, vendor-replaceable, privacy-conscious, and user-first. Donations must never become a prerequisite to accessing existing public content or an excuse to introduce tracking, sponsorship or unrelated advertising. Do not describe the project as a tax-exempt nonprofit or claim charitable deductions without separate authoritative evidence.

## Payment integration gate (future work, not live)

1. **Authority and provider:** Confirm the owner-approved payment method and verified GoreeCloud-owned merchant identity. Evaluate provider data practices, fees, account custody, exportability and a viable replacement/exit path. Do not create a new merchant account, broaden credentials or bind a vendor as part of a website content change.
2. **Scope of collection:** Decide whether contributions are one-time only or optionally recurring; define refund/cancellation process and accurate public-facing payment terms before offering either. Never make an unapproved recurring charge the default.
3. **Privacy and security:** Prefer a verified hosted checkout using the provider's secure domain. Never ingest or store card data in the static website or expose merchant tokens, webhook secrets or personal banking addresses in public source. Minimize donor data, disable optional tracking where possible and document unavoidable processor disclosures.
4. **Receipt and records:** Validate confirmation and refund handling, receipts, statement descriptors, ownership, reconciliation and proportionate retention. Tax and legal representations require verified authority and must not be guessed.
5. **Fraud resistance:** Only link to the checked provider destination; make it unmistakably clear when leaving GoreeCloud. Do not direct contributors to emailed payment links, cryptocurrency addresses, user-submitted payment URLs, social DMs or unverifiable accounts.
6. **Control, reliability and accessibility:** Support functional keyboard and assistive-technology flows, accessible error states, mobile checkout, checkout cancellation, disabled/expired destinations, clear currency/fees and safe return navigation. Document outage and rollback handling.
7. **Verification:** Test a sandbox transaction where available, receipt, failure, cancellation, refund and webhook behavior where relevant; review CSP and redirects; inspect small and large viewports; verify that no client or server secret leaks; run exact-head CI and production-readback on the final governed revision.
8. **Publication:** Update public text and metadata to match verified status only after checkout and its public terms are accepted. Preserve versioned rollback and disallow accepting payments when evidence is missing.

## Current page verification

From the repository root:

```bash
python -m unittest discover -s sites/main/tests -p "test_*.py"
python scripts/validate_url_namespace.py
python sites/main/scripts/validate_site.py
python sites/main/scripts/validate_public_surface.py
python sites/main/scripts/build_public_site.py
python sites/main/scripts/validate_build_artifact.py
python sites/main/scripts/browser_artifact_smoke.py
```

The GitHub Actions website workflow is authoritative for exact-head CI status, not for owner/human Glaze acceptance or live deployment. Do not infer published status from passing tests, provider build status or a merged pull request. Check production at the canonical domain against the deployed artifact after separately authorized deployment.

## Unresolved release and checkout dependencies

- **Website release:** Review repository protection policy, accepted visual/keyboard/assistive-technology evidence, governed merge and rollback, and the production browser/readback acceptance. Retain the existing `source-adopted-unaccepted` Glaze consumer status until its independent acceptance is complete.
- **Financial checkout:** A verified owned merchant destination, policy decisions and authorization to activate it remain outstanding. The static page must continue to state that financial donations are unavailable until then.

Open work is tracked in GoreeCloud's designated task system rather than treating this source document as a competing operational task registry.
