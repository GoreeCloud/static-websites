# GoreeCloud Website — Glaze V1.7 Canonical Readback

**Website revision:** `17303b6c7381faaa0e89ce6175ce24048fb56a12`  
**Canonical origin:** `https://www.goreecloud.com`  
**Consumer state:** `source-adopted-unaccepted / pending-human-acceptance`  
**Evidence result:** PASS — all current canonical HTML routes matched repository source byte-for-byte.

## Exact canonical route readback

| Route | Source bytes | Canonical bytes | Result |
| --- | ---: | ---: | --- |
| `/` | 11,825 | 11,825 | PASS |
| `/platform-systems/` | 9,922 | 9,922 | PASS |
| `/suite/` | 15,527 | 15,527 | PASS |
| `/android/` | 12,272 | 12,272 | PASS |
| `/office-suite/` | 9,178 | 9,178 | PASS |
| `/firefox/` | 10,030 | 10,030 | PASS |
| `/github/` | 6,579 | 6,579 | PASS |
| `/contact/` | 10,321 | 10,321 | PASS |
| `/design/` | 9,798 | 9,798 | PASS |
| `/security/` | 9,953 | 9,953 | PASS |
| `/privacy/` | 10,154 | 10,154 | PASS |

**Total compared canonical HTML:** 115,559 bytes.

## Additional changed-artifact readback

| Artifact | Bytes | Result |
| --- | ---: | --- |
| 404 body | 2,120 | PASS — exact repository bytes |
| `/assets/systems/glaze-ui.svg` | 858 | PASS — exact repository bytes |
| `/assets/systems/mesh.svg` | 2,600 | PASS — exact repository bytes |

The canonical requests used a cache-busting query value tied to the candidate revision. The 404 comparison used the response body from an intentionally missing route. Exact byte comparison for the 404 and SVG assets was performed against the same checked-out repository revision.

## Supporting exact-revision machine evidence

- Repository validation: GitHub Actions run `37191505046` — PASS.
- Main website validation: GitHub Actions run `37191505073` — PASS.
- Pinned Glaze V1.7.0 authority validation — PASS within the main website run.
- Isolated public artifact and public-boundary validation — PASS.
- Canonical-page Chrome responsive/interaction smoke — PASS.
- Current JavaScript syntax validation — PASS.
- Glyph mobile-navigation regression gate — PASS.

## Boundary

This evidence establishes exact canonical deployment/readback for the listed HTML routes and changed artifacts plus machine validation for the exact revision. It does **not** establish owner visual acceptance, keyboard-only acceptance, assistive-technology acceptance, representative device/browser performance acceptance, or final Glaze consumer acceptance.
