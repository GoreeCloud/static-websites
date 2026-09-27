# Project Specifications — Public Websites

> **Canonical repository:** `GoreeCloud/static-websites`  
> **Current public topology:** one retained website at `https://www.goreecloud.com`  
> **Migration source:** Google Drive record `1UzMvKduiDeB2VH4v6azFXAAWg8tT4CZPoonXRgzUi0M`  
> **Authority boundary:** this file contains current normative project requirements. Historical multi-site deployment evidence is retained in `PROJECT-RECORD.md`.

GoreeCloud — Project Record — Public Websites

Document Metadata
Document Owner: LaDamian Goree
Version: v0.15
Status: Production Verified — One current public website at https://www.goreecloud.com; owner-accepted Design, Security, and Privacy update is deployed and exact-byte verified on the canonical hostname against production-source main b19a7d21f6c90cb7901271f166c8c2d52e6218e4.
Created: August 19, 2026
Classification: Internal
Document Type: Public Website Portfolio Project Record
Current Deployment Model: One retained public website at https://www.goreecloud.com. Historical satellite-site and subdomain records below remain historical evidence only unless separately reactivated by later governance.
Canonical Static Website Repository: GoreeCloud/static-websites
Hosting Platform: Cloudflare Pages
Design Language: Glaze UI V1.6 / 1.6.0 — Current Official Stable shared design-system target. Website consumer acceptance remains exact-revision scoped.
Security Identity: Wardveil Security by GoreeCloud
Authoritative Record: Yes

## 1. Purpose

This document records the current GoreeCloud public website and preserves historical website-portfolio evidence. The present public model is one retained website at https://www.goreecloud.com with path-based destinations for the ecosystem, platform systems, products, public source, contact, design, security, and privacy.

Historical satellite-site and custom-subdomain material later in this record is retained as dated evidence only. It does not override the current one-website model.

## 2. Current Public Website Model

The current retained public website exposes ten canonical path-based destinations:

- / — GoreeCloud home and ecosystem overview.
- /platform-systems/ — Integral Platform Systems.
- /suite/ — GoreeCloud Suite.
- /office-suite/ — GoreeCloud Office Suite.
- /firefox/ — GoreeCloud Firefox work.
- /github/ — Current public GoreeCloud source discovery.
- /contact/ — Approved public contact and social channels.

## 3. Repository and Deployment Model

GoreeCloud/static-websites is the mandatory canonical source repository for the retained public website and other governed static-site source. The current production-facing public model is one retained website at https://www.goreecloud.com; historical multi-site source and deployment records below remain historical unless later reactivated by explicit governance.

September 6, 2026 source-consolidation checkpoint: all 13 currently identified standalone GoreeCloud public static website packages are now present in GoreeCloud/goreecloud-static-websites and are validated-in-central-repo. Main source migration was accepted through PR #8 at merge 553e42f59573f8cacc5e6ab8bb2223d6b7575bb3. Privacy Shield, Wardveil Security, and Everkeep were rebased after the shared-manifest change and accepted through PR #10 at merge 4bfee305550e2e43991188816f4fc80c16ccfad5. The resulting central main revision passed repository validation and the dedicated Privacy/Security/Everkeep post-merge validation. Repository discovery scanned 66 public non-archived GoreeCloud repositories and the authenticated installed-repository inventory, including the accessible private repositories, and identified no additional standalone GoreeCloud static public website package beyond the 13 current manifest entries.

This source checkpoint does not supersede existing exact-revision production acceptance or prove that Cloudflare Pages is reading from the centralized repository. All 13 current manifest entries still record deployment_state legacy-source. Cloudflare Pages repository/root/build cutover, deployment-reference reconciliation, exact production verification, legacy-copy retirement, dependency/preservation checks, and the final GoreeCloud/goreecloud-website deletion gate remain separately required.

The sites are intended to remain lightweight public properties rather than extensions of private GoreeCloud infrastructure. Public website content must not expose credentials, private network information, administrative interfaces, internal-only configuration, or sensitive operational records.

## 4. Glaze UI and Brand Consistency

The retained public website uses Glaze UI as the governing GoreeCloud design language. Current canonical public pages target Glaze UI V1.6 / 1.6.0 and retain exact-revision consumer acceptance boundaries.

GoreeCloud Privacy Shield is the official privacy identity used where privacy-specific presentation is appropriate. Wardveil Security by GoreeCloud is the official security identity used for security-related presentation, controls, explanations, and public security information.

The sites should maintain consistent typography, surface treatment, navigation behavior, responsive layouts, accessibility, reduced-motion support, icon treatment, interaction states, and GoreeCloud product identity.

## 5. Blog Site

The Blog foundation is located under sites/blog/ in the primary website repository.

Its initial structure provides an editorial homepage and content direction for:

- GoreeCloud development articles.
- Homelab lessons.
- Project and application updates.
- Architecture decisions and explanations.
- Glaze UI design work.
- Privacy and security topics.
- Open-source and self-hosting lessons.

The foundation includes hardened static-site behavior, content-security controls, reduced-motion handling, a dedicated 404 experience, a Cloudflare Pages deployment contract, and fail-closed validation.

The initial implementation was prepared in draft pull request #46. The dedicated Blog validation workflow and the existing public-website validation workflow passed on the prepared PR head during initial development.

## 6. Archive Site

The Archive foundation is located under sites/archive/ in the primary website repository.

I designed the Archive around chronology rather than ordinary editorial publishing. Its initial timeline covers major eras including:

- GoreeCloud foundation and early purpose.
- Infrastructure and architecture development.
- Application-development expansion.
- Glaze UI development.
- Privacy Shield and Wardveil Security identity development.
- Expansion of the public GoreeCloud web presence.

The Archive is a curated public historical record. It is not a public mirror of internal change logs. Internal change logs may contain implementation detail, troubleshooting history, operational data, or other information that is inappropriate for automatic public publication. Historical material must therefore be deliberately selected and adapted before appearing in the Archive.

The Archive foundation also includes hardened static-site behavior, security headers, reduced-motion handling, a dedicated 404 experience, a Cloudflare Pages deployment contract, and validation tooling.

The initial implementation was prepared in draft pull request #47. Its dedicated validation and primary public-website validation workflows were queued when the initial foundation work concluded; successful production acceptance must be recorded separately after final verification.

## 7. Security and Privacy Requirements

Public GoreeCloud sites must follow privacy-by-default and minimum-exposure principles. I will not publish private service addresses, reusable credentials, private keys, API keys, internal-only configuration, private network inventories, personal information that is not intentionally public, or sensitive infrastructure details merely to make a public site more complete.

Static-site security controls should include restrictive security headers and content-security policy appropriate to each site. External scripts, trackers, analytics, fonts, embeds, and third-party dependencies should not be introduced without deliberate review and a documented purpose.

## 8. Content Boundaries

The public portfolio serves public communication and education. It does not replace internal GoreeCloud governance, architecture, project specifications, inventories, policies, standards, or change logs.

Public content may summarize approved concepts from internal records, but the public sites are not authoritative substitutes for those internal records. Where internal information changes, the authoritative internal record remains the source for administration and engineering decisions until a controlled documentation change explicitly establishes otherwise.

## 9. Productionization Requirements

The retained public website is not considered production-accepted for a new revision solely because source exists or has merged. Before a changed revision is treated as production-accepted, I must complete the applicable deployment and acceptance work, including:

- Review and merge the applicable source changes.
- Confirm all CI and site-specific validation gates pass on the exact production revision.
- Confirm the retained Cloudflare Pages project and deployment source remain correct.
- Confirm the canonical repository, main branch, site root, build command, and output directory used for production.
- Verify the canonical https://www.goreecloud.com hostname remains bound to the intended deployment.
- Verify public DNS and HTTPS/TLS behavior for the retained hostname.
- Verify HTTPS and certificate issuance.
- Verify redirects, canonical URLs, security headers, content-security policy, 404 behavior, responsive behavior, accessibility, and reduced-motion behavior.
- Validate cross-page navigation and ensure links do not expose private GoreeCloud services.
- Perform a final content review for accuracy, privacy, security, and public suitability.
- Record the final deployment state and production revision in the appropriate GoreeCloud documentation and change log.

## 10. Current Status

The current public model is one retained website at https://www.goreecloud.com. Canonical source is GoreeCloud/static-websites. Historical satellite-site and subdomain production records below are preserved as historical exact-revision evidence and do not define the current public topology.

Current retained-site state:

https://www.goreecloud.com/ — current retained public website.
Canonical destinations: /platform-systems/, /suite/, /office-suite/, /firefox/, /github/, /contact/, /design/, /security/, and /privacy/.
PR #121 exact accepted head 02b60edf27b36e7cad31d0bbf383b147bcfed6f4 passed owner human acceptance and exact-head validation before guarded squash merge.
Accepted source merged to canonical main as 3715e132e6a2ce6f3f4034a9dc6f0b70b2078af4.
Production deployment is verified for the accepted public artifact. Production verifier PR #123 exact head 4557f388abb0dc19b5b921ca2f8d9503222a0ebb passed Verify main GoreeCloud production deployment #2 / run 35656940637, Validate static website repository #606 / run 35656940654, and Validate main GoreeCloud website #305 / run 35656940674. The verifier compared the canonical hostname byte-for-byte against production-source main b19a7d21f6c90cb7901271f166c8c2d52e6218e4 for Home, Design, Security, and Privacy and also verified required security/indexing headers, legacy Privacy/Security redirects, and exact 404 behavior.
Glaze UI remains V1.6 / 1.6.0 Stable authority; website consumer acceptance remains exact-revision scoped.
No satellite subdomain is treated as a current GoreeCloud website merely because historical records below describe prior production states.

## 11. Next Phase

The next phase is iterative improvement of the one retained public website: richer current content, first-class path-based sections, artwork and identity fidelity, navigation consistency, responsive/mobile quality, accessibility, privacy/security truthfulness, and continued removal of stale historical assumptions from current-state documentation. The September 21 Design/Security/Privacy deployment is production-verified and no longer an open deployment gate.

## Repository documentation authority

Detailed implementation state remains controlled by verified repository source, tests, CI, deployment evidence, and exact production acceptance. Historical satellite-site material does not recreate or authorize retired public websites. Any future website or restored hostname requires explicit current governance and repository evidence.
