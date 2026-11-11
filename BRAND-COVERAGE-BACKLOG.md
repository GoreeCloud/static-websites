# GoreeCloud brand identity coverage — website source audit

Audit date: November 11, 2026. Scope: GoreeCloud's **12 selected website product cards** and authoritative first-party source repositories. This is not a comprehensive audit of every repository or installed application.

## Provenance and website state

| Product | Source found | Status in website review | Next action |
| --- | --- | --- | --- |
| GoreeCloud UI | `brand-assets/products/gc-ui`; Flowframe v2 draft PR #22 | **New design candidate, not official** | Review the new proposed mark against GC UI and approve before central replacement |
| GoreeShield | No approved icon recovered | **Missing** | Original privacy brand identity; do not confuse with Wardveil cybersecurity |
| Wardveil | No approved icon recovered | **Missing** | Original cybersecurity brand identity; not GoreeShield |
| GoreeCloud Mesh | No approved icon recovered | **Missing** | Original cross-product integration mark, distinguish from security/privacy |
| GoreeCloud Browser | Founder-approved `brand-assets/products/browser-mobile/app-icon.svg` | **Approved shared Prism Tabs v5 icon** | Product/platform acceptance remains distinct |
| Browser Mobile | Same shared Browser family master | **Approved shared Prism Tabs v5 icon** | Android adaptive/themed package acceptance remains distinct |
| GoreeCloud Maps | No approved icon recovered | **Missing** | Original map/location icon family, with verified service release status |
| GoreeCloud Search | Recovered `brand-assets/products/search/app-icon.svg` | **Verified existing first-party icon** | Confirm new consumer surfaces; core icon already sourced |
| GoreeCloud Drive | `GoreeCloud/drive/services/web/assets/themes/goreecloud/assets/icon.svg` | **Existing first-party consumer icon; central approval pending** | Review original theme license/provenance and publish master/derivatives centrally if accepted |
| GoreeCloud Projects | Upstream Plane/GitHub/etc. icons were found, **not** an approved original GoreeCloud product mark | **Missing** | Create first-party identity; do not misrepresent upstream third-party Plane branding |
| GoreeCloud Analytics | No approved icon recovered | **Missing** | Original privacy-first analytics product mark |
| GoreeCloud Gateway | No approved icon recovered | **Missing** | Original edge/gateway infrastructure mark |

**Coverage:** 2 products use the same founder-approved Browser-family mark; 1 uses recovered first-party Search; 1 uses the existing Drive consumer mark (not yet centrally approved); 1 displays the distinct Flowframe v2 candidate (not yet approved); 7 have no eligible official source. A neutral dashed token is shown in place of inventing an official logo. It is explicitly labeled on the website as pending identity artwork.

## Scope / rights / security

Only existing first-party source SVGs are copied to the isolated nonproduction website. No visual identity is invented or promoted to official status in this integration. `PRODUCT-ICON-SOURCES.json`, `scripts/verify_product_identity_coverage.py`, and the negative regression tests establish source hashes and forbid silent promotion to official.

The existing public `GoreeCloud/drive` theme icon is custom GoreeCloud cloud artwork, **not** an OpenCloud upstream symbol; confirm its rights, central master and founder approval separately. The site does not use Plane or OpenCloud upstream logos as GoreeCloud identities. These four brand pillars remain semantically distinct: GoreeShield = privacy, Wardveil = cybersecurity, GoreeCloud Mesh = integration, GoreeCloud UI = design language.

The central brand-assets repository, not this website, must own each new approved logo/icon/artwork/favicon master. Any eventual promotion needs provenance, original design review, SVG safety, alpha/contrast, 16/32/48/192/512px rendering, light/dark backgrounds, native/platform packaging and consumer copy verification. Do not mistake a placeholder or candidate for a release-ready official mark.

Current website development references: [nonproduction static-sites PR #4](https://github.com/GoreeCloud/static-websites/pull/4), [proposed GC UI Flowframe v2 PR #22](https://github.com/GoreeCloud/brand-assets/pull/22). The permanent GoreeCloud umbrella G is separate from all product marks.
