# All eleven retained routes — isolated GC UI candidate

**Status: source-only candidate. Not published, deployed, production accepted or content-parity accepted.**

The one current website is \`https://www.goreecloud.com\`. This builder produces a **separate, noindex, first-party GC UI route candidate** for its eleven already approved paths. It never writes the production \`sites/main/dist/\` artifact, touches DNS, or revives retired public websites.

The page copy is preliminary and **does not establish parity with existing production copy, functionality, accessibility, SEO, or governance**. Its value is a coherent original GC UI interface scaffold, route preservation, exact-pinned Foundations reuse, responsive layout, semantic navigation, and negative-testable artifact integrity while migration issue #144 remains open.

Run from the repository root:

\`\`\`sh
python3 gc-ui-www-preview/validate.py
python3 gc-ui-www-preview/build_routes.py
python3 -m unittest discover -s gc-ui-www-preview -p 'test_routes.py' -v
python3 -m http.server 4173 --directory dist-gc-ui-routes-preview
\`\`\`

The generated output is \`dist-gc-ui-routes-preview/\`, which must **not** be pointed at a production Pages project. It carries \`SHA256SUMS.json\` with all acceptance booleans false. Do not create a Cloudflare Pages project or publish a new hostname for this isolated proof-of-structure.

Completion requires review of the existing eleven pages and features, original brand assets, real-browser/assistive-technology behavior, production-level headers and route semantics, and a proven rollback plan. See [retained site migration issue #144](https://github.com/GoreeCloud/static-websites/issues/144).

## Public-copy reconciliation

The isolated candidate now extracts public source article **text only** and presents it in original GC UI patterns; it does not import legacy HTML, scripts or CSS. It excludes predecessor design claims and uses original GC UI copy for /design/. Source page SHA-256 values are included in the generated artifact manifest.

Run `python3 gc-ui-www-preview/audit_source.py` after `build_routes.py` to see conservative per-route content, controls and main-link gaps. The report is diagnostic and leaves every production/content/accessibility acceptance flag false.

## Opt-in GitHub repository directory

The isolated `/github/` preview now has an explicit visitor-initiated public repository directory. It uses a fixed GitHub organization endpoint, no credentials, a five-page maximum, bounded request timeout, and safe DOM text rendering. Private or malformed records are excluded, duplicates are ignored, and provider URLs are not trusted for navigation. Filtering operates locally once public metadata is loaded. No GitHub request occurs merely because the page loads.

**Test scope:** The Chromium/Firefox isolated browser workflow now checks consent-only loading, private-result exclusion, local filtering, HTTP rate-limit retry, bounded pagination, and duplicate exclusion using synthetic GitHub responses. Browser run `39367086949` passed at implementation head `43826d561d3642f5edfd2386cfc123960dcc168f`. Actual GitHub provider integration, deployment CSP, production accessibility acceptance and cutover remain unverified.
