# GoreeCloud Website — Glaze V1.7 Canonical Readback

**Website revision:** `36bfb823abe52007ae377766c6d224407df5f071`  
**Canonical origin:** `https://www.goreecloud.com`  
**Consumer state:** `source-adopted-unaccepted`  
**Evidence result:** PASS — all current canonical HTML routes matched the repository source byte-for-byte.

## Exact route readback

| Route | Source bytes | Canonical bytes | Result |
| --- | ---: | ---: | --- |
| `/` | 11,825 | 11,825 | PASS |
| `/platform-systems/` | 9,922 | 9,922 | PASS |
| `/suite/` | 15,486 | 15,486 | PASS |
| `/android/` | 12,231 | 12,231 | PASS |
| `/office-suite/` | 9,178 | 9,178 | PASS |
| `/firefox/` | 10,030 | 10,030 | PASS |
| `/github/` | 6,538 | 6,538 | PASS |
| `/contact/` | 10,280 | 10,280 | PASS |
| `/design/` | 9,757 | 9,757 | PASS |
| `/security/` | 9,953 | 9,953 | PASS |
| `/privacy/` | 10,154 | 10,154 | PASS |

**Total compared HTML:** 115,354 bytes.

The canonical requests used a cache-busting query value tied to the candidate revision. The comparison removed only the Desktop Commander transport annotation appended after the fetched response; the HTTP-delivered HTML itself matched repository source exactly.

## Supporting exact-revision machine evidence

- Repository validation: GitHub Actions run `37175225674` — PASS.
- Main website validation: GitHub Actions run `37175225680` — PASS.
- Pinned Glaze V1.7.0 authority validation — PASS within the main website run.
- Isolated public artifact and public-boundary validation — PASS.
- Canonical-page Chrome responsive/interaction smoke — PASS.
- Current JavaScript syntax validation — PASS.

## Boundary

This evidence establishes exact canonical deployment/readback for the listed HTML routes and machine validation for the exact revision. It does **not** establish owner visual acceptance, keyboard-only acceptance, assistive-technology acceptance, representative device/browser performance acceptance, or final Glaze consumer acceptance.
