# GoreeCloud Main Website Public Asset Inventory

## Current publication boundary

The current retained-site build publishes only assets explicitly named by `sites/main/scripts/build_public_site.py`.

Repository presence does not make an asset deployable.

Current public artwork/media files:

| Public asset | Current role | Source/provenance | Reviewed Git blob |
| --- | --- | --- | --- |
| `assets/goreecloud-logo.svg` | GoreeCloud brand mark used by the header, favicon/manifest, and shared navigation | Canonical `GoreeCloud/branding-assets` → `official/goreecloud-logo.svg`; current website copy is byte-identical | `082936062de7839148db89ea3ab4e86ff71341b0` |
| `assets/social-preview.png` | Website-specific social preview image | Retained website publication asset; not an independent GoreeCloud branding authority | `64aaf437835b31a8473292487cf57366bb58c4fa` |

## Source-only retained assets

Older platform, service, social-network, Suite, roadmap, and migration artwork may remain in the repository for history, provenance, rollback, or retirement cleanup.

Those files are **not current public assets** unless they are explicitly added to the current `PUBLIC_FILES` allowlist and pass all applicable branding, rights, privacy, security, accessibility, performance, and publication review.

The current Suite page intentionally uses neutral text presentation rather than silently publishing an older icon inventory as current.

## Branding authority

Canonical first-party GoreeCloud branding comes from `GoreeCloud/branding-assets`.

Website-local copies are publication derivatives only. A local copy must not become a competing source of truth.

Products without approved canonical artwork must remain neutral/textual rather than receiving fabricated official artwork.

## Rights and truth boundary

This inventory is not a license grant.

Third-party marks retained elsewhere in source remain subject to their owners' rights and must not be reintroduced into the public artifact without current need and review.

An asset's presence, provenance, or successful validation does not establish product implementation, lifecycle maturity, privacy/security state, or production acceptance.
