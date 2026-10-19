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
