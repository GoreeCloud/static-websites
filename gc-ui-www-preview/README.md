# GoreeCloud UI /design/ — isolated retained-site preview

**Status:** **Not deployed. Not accepted.** One original /design/ page candidate only, October 19, 2026.

The only public GoreeCloud website is `www.goreecloud.com`, governed by [the one-site policy](../README.md). The active `sites/main/` website still contains historical Glaze design dependencies and is **not** replaced by this candidate. Do not create or restore standalone public secondary sites.

This original candidate uses [GC UI Foundations 1.0.1](https://github.com/GoreeCloud/gc-ui/releases/tag/foundations-v1.0.1), a narrow Apache-2.0 release with generated semantic token stylesheet. `gc-ui-foundations.css` is exact Git blob `c0e32a40f0bba280c9a4e9e01f31e1114d60f26c` from reviewed release source commit `7e0b61ee70af2edb87aa736cca483425f0aacaf4`; the validator computes original Git blob identity. This is source verification, not an independent re-download and unpack of the GitHub tarball.

### Local source and artifact validation

```sh
python3 gc-ui-www-preview/validate.py
python3 -m unittest discover -s gc-ui-www-preview -p test_preview.py -v
node --check gc-ui-www-preview/site.js
python3 gc-ui-www-preview/build.py
python3 gc-ui-www-preview/validate.py --dist
```

The preview produces **`dist-gc-ui-www-preview/`** at repository root and cannot replace or write `sites/main/dist/`; all artifact gate flags remain false. CI checks exact commit identity, preserved live source and URL namespace, local source integrity, no retired design imports, keyboard/appearance semantics, and fail-closed negative cases. The build has no remote fetches.

**Remaining:** rendered Chromium/Firefox verification, forced-color/reflow and assistive-tech acceptance, owner-approved brand, complete original 11-route migration, real security header/HSTS/404 validation under hosting, one-site rollout and rollback. The prior production `/design/` title still refers to the predecessor; this preview does not change it.

Full real-public-site migration is tracked in [issue #144](https://github.com/GoreeCloud/static-websites/issues/144); ecosystem acceptance is tracked in [gc-ui issue #13](https://github.com/GoreeCloud/gc-ui/issues/13). GoreeCloud UI is **IPS 5 of nine**, not a tenth.
