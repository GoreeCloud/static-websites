# GoreeCloud Website — Glaze V1.7 Canonical Readback Evidence

**Status:** Partial production readback verified; consumer acceptance remains pending  
**Website revision:** `531744f2a82133caca8ddde00fa782415d1a42e1`  
**Canonical origin:** `https://www.goreecloud.com`  
**Readback date:** October 3, 2026 (America/Chicago)

## Exact source and machine evidence

The current canonical `GoreeCloud/static-websites` main revision is `531744f2a82133caca8ddde00fa782415d1a42e1`.

For that exact revision:

- repository validation run `37171153953` passed;
- main website validation run `37171153974` passed;
- the isolated public artifact validated at 100 files / 322713 bytes;
- headless Chrome smoke passed all eleven canonical pages at representative desktop, tablet, modern-phone, and narrow-phone widths;
- Cloudflare Pages reported successful deployment for the exact revision.

## Canonical route readback

Readback was performed from the authorized GoreeCloud connected device by fetching the canonical HTTPS URLs directly and comparing the returned HTML text with the exact GitHub source files at revision `531744f2a82133caca8ddde00fa782415d1a42e1`.

### Security Center

- Canonical URL: `https://www.goreecloud.com/security/`
- Source path: `sites/main/security/index.html`
- Source blob: `1c3f93866eb76c9ce366ba8f2db42b15dc5ad427`
- Live/source text length: 9745 / 9745
- Exact text comparison: **passed**

### Privacy Center

- Canonical URL: `https://www.goreecloud.com/privacy/`
- Source path: `sites/main/privacy/index.html`
- Source blob: `aadf935248db716858b7882b1685d0bcdd4a6da4`
- Live/source text length: 9966 / 9966
- Exact text comparison: **passed**

Both live pages declare Glaze `1.7.0` and consumer state `source-adopted-unaccepted`.

## Remaining boundary

This evidence verifies two canonical page HTML readbacks. It does **not** prove byte equivalence for the entire deployed public tree, all static assets, headers, redirects, or every canonical route.

The following therefore remain pending:

- complete deployed-tree equivalence where required;
- owner visual review;
- keyboard review;
- assistive-technology review;
- representative performance/resilience acceptance;
- exact rollback exercise/evidence;
- final production consumer approval.

No Privacy Shield privacy authority, Wardveil security authority, runtime authority, or Glaze consumer acceptance is created by this partial readback.
