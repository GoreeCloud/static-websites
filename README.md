# GoreeCloud static website — preview snapshot recovery

This is a **review-only recovery branch** of the current GoreeCloud website **preview**.
It is **not** the former `GoreeCloud/static-websites` repository history, and it is
**not the source of the currently deployed production website**.

## Identity and provenance

Cloudflare Pages' saved source configuration references an earlier GitHub
repository object with ID `1358646162`, which is no longer accessible. The
present `GoreeCloud/static-websites` repository is a separate, newly created
GitHub object with ID `1453961169`; it initially had only a README.

The `site/` directory in this review branch contains the **exact 20 static
files** from the independently verified, direct-upload Cloudflare Pages
preview of November 11, 2026. This is a recovery of compiled public preview
assets, **not** a reconstruction of the old source history or the complete
standalone Python generator. The complete generator, tests and local evidence
remain in the private GoreeCloud Website Google Drive project archive.

Preview branch: `preview-gcui-rebuild-20261111`.
Immutable Pages deployment ID: `a875c44e-87e2-49c8-a5b0-bae38d5be89d`.
Immutable review URL: https://a875c44e.goreecloud-website.pages.dev/

## Scope and verification

All 14 preview content routes (including 11 formerly published sitemap paths),
the custom 404, preview-only robots policy, static JS/CSS and the temporary
`/social/` 302 are preserved. `SITE-MANIFEST.sha256` pins the original 20
files byte-for-byte. `scripts/verify_preview_snapshot.py` enforces manifest
integrity and preview-only safety. No runtime dependencies are required.

```sh
python3 scripts/verify_preview_snapshot.py
```

The GitHub Actions workflow runs only source tests and **never deploys,
changes DNS, runs Cloudflare CLI, or uses GitHub/Cloudflare credentials**.
The branch and pull request are explicitly held for source-history,
accessibility, editorial, branding, SEO, licensing and release review.
No production `main` branch changes are requested or authorized by this
snapshot. Do not connect this new GitHub ID to Cloudflare without a separate
source-mapping review.

## License and marks

The original static code and accompanying software in this recovery branch
are offered under [MIT](LICENSE). This does not grant rights to the
GoreeCloud name or marks, third-party linked content, or historical code
that is not present in this repository.
