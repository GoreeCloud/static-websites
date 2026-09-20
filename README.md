# GoreeCloud Static Website Source

This repository is the retained source authority for the GoreeCloud public website and for controlled preservation/retirement of former static-site source.

## Current website state

As of September 20, 2026:

- **`www.goreecloud.com` is the only current GoreeCloud website.**
- Former secondary public website hostnames and standalone website deployments are retired or in governed retirement.
- A historical source package, directory, former hostname, redirect, validation workflow, or deployment record does **not** make that surface a current website.
- Retired website endpoints must not be recreated solely to satisfy superseded validation, migration, or acceptance checks.
- Web applications, private administration interfaces, APIs, and service endpoints are not reclassified as websites merely because they use HTTP or a `goreecloud.com` hostname.

The governing retirement workflow is tracked in GoreeCloud Tasks Management under **GoreeCloud Main Website Retention and Public Website Retirement**.

## Repository role

`GoreeCloud/static-websites` remains active because `www.goreecloud.com` is permanent and retained.

Its current responsibilities are:

1. maintain the reviewed source needed for `www.goreecloud.com`;
2. preserve required source history, migration evidence, and recovery material for former public websites while retirement is still being reconciled;
3. support controlled removal or archival of retired secondary-site source, workflows, deployment references, and compatibility material after dependencies and preservation requirements are verified; and
4. prevent historical multi-site source from being mistaken for current public deployment authority.

This repository is **not** authority to publish additional GoreeCloud websites. A new or restored website requires a later explicit GoreeCloud decision plus applicable DNS, hosting, security, privacy, design, deployment, and production-verification evidence.

## Source layout

```text
sites/
  url-namespace.json
  manifest.json
  main/
  <historical-or-retirement packages>
docs/
  migration-status.md
```

`sites/main/` is the source package associated with the retained `www.goreecloud.com` website. `sites/url-namespace.json` is the current route registry for that one website and its path-based sections. `sites/manifest.json` is retained migration/retirement evidence and is not a current website inventory.

Other `sites/<site-id>/` packages may remain temporarily for history, recovery, migration, or retirement cleanup. Their presence in the repository or in `sites/manifest.json` is not a current-site inventory and must not be interpreted as proof that the corresponding hostname, Cloudflare Pages project, redirect, or public deployment still exists.

Generated deployment artifacts such as `dist/` are not authoritative source and should be regenerated from reviewed source unless a retained-site contract explicitly requires otherwise.

## Retirement boundary

Before deleting historical website source or supporting material, verify that required provenance, rollback/recovery evidence, repository history, documentation, and any remaining dependencies have been preserved or dispositioned.

Conversely, do not keep obsolete secondary-site publication requirements active merely because historical source remains in this repository. Current deployment truth must come from verified DNS/hosting/provider state and the governing GoreeCloud records.

## Safety boundary

Do not move authenticated application code, backend services, private administrative interfaces, databases, secrets, or non-static runtime code into this repository merely because a product once had a public informational site.

Only the retained public website source and controlled historical/retirement material belong here.
