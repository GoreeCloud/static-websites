# GoreeCloud homepage

Source for the new single-page public website at https://www.goreecloud.com/.

- `index.html` is the sole public content page.
- `404.html` provides an honest not-found response for removed URLs.
- `assets/` contains the locally served stylesheet and verified first-party GoreeCloud umbrella identity artwork.
- `_headers` defines production security headers.
- `robots.txt` and `sitemap.xml` list the one public content URL.

The homepage describes ecosystem intentions and distinct pillars; it does not claim that unreleased services are deployed. The official logo and connected-world artwork originate from `GoreeCloud/brand-assets`. GoreeCloud UI design language supplies the Canvas / Surface / Lens material principles.

## Hosting

Cloudflare Pages project: `goreecloud-website`; custom domain `www.goreecloud.com`. The original Git-connected repository ID differs from this repository's ID; deployment through direct-upload Wrangler is independent until source integration is intentionally reconciled. Do not infer that pushing this repository alone deploys the site.

This repository does not contain the former public website, any copy of the former pages, or site backups.

## Verification

Run the eight dependency-free source checks before release:

```sh
python3 -m unittest discover -s tests -v
```

The protected source-quality workflow checks the same contracts on GitHub. Published production assets must be independently verified against a specific source commit; GitHub `push` is not currently a verified Cloudflare production deploy trigger.

## Optional local self-hosting

The site is also packaged as a small OCI container with an inspected, digest-pinned upstream NGINX unprivileged base image. **Docker Compose is the preferred self-hosting entry point**:

```sh
docker compose up --build -d
curl -I http://127.0.0.1:18080/
docker compose down
```

`compose.yaml` binds only to `127.0.0.1:18080`, runs UID 101, drops all Linux capabilities, enables a read-only filesystem, and provides a temporary `/tmp` filesystem. A separate HTTPS-terminating reverse proxy is required before any public exposure. Do not forward the container port directly to the internet, and do not use this example to change the existing Cloudflare DNS or production service.

The same `Dockerfile` builds as a Podman OCI image (`podman build -t goreecloud-homepage:local .`). A rootless Podman runtime smoke test verified the local homepage, assets, legacy-route 404s and CSP. `podman compose` requires a separate Compose provider and was not available on the test laptop. No production self-hosted deployment is implied. No old website assets or backups are included.
