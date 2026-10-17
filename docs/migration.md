# Migrate the website artwork

## Inventory at the source revision

Source repository: `xila-project/website`.
Source commit: `490575c467bb108e2e1407e6cae0f91015cc6955`.

| Original path | Meaning | Archive |
| --- | --- | --- |
| `src/public/images/logo_light.svg` | Black symbol for light backgrounds | `legacy/website/logo_light.svg` |
| `src/public/images/logo_dark.svg` | White symbol for dark backgrounds | `legacy/website/logo_dark.svg` |
| `src/public/images/logo_dark.png` | White raster symbol | `legacy/website/logo_dark.png` |

The three originals are preserved byte for byte. `legacy/provenance.json` records source paths, Git blob IDs and SHA-256 hashes. The full Git history remains in website; this archive is a provenance-preserving copy, not a history rewrite.

At the inspected revision, `.vitepress/config.mts` references the two SVGs in `themeConfig.logo`. It also uses the white `logo_dark.svg` as its favicon, which can disappear against a light browser surface. The organization profile also references `https://www.xila.dev/images/logo_dark.svg` in its README. Keep these public URLs available during migration.

## Ownership model

`brand/source/` owns the design. `website/src/public/images/` contains deployment copies only. Keeping consumer copies avoids cross-origin fetching, CDN availability dependencies and a separate download step during every documentation build.

Do not remove website's files before replacing its references and checking external consumers. Do not replace image URLs with links to GitHub HTML blob pages.

## Rollout

1. Populate the `Xila-Project/brand` repository (created as private). Review the generated assets and tag a version, initially `v1.0.0`.
2. From a local brand checkout, run `python scripts/sync_website.py /path/to/website`. The script copies the three compatibility exports with the existing filenames.
3. Copy `assets/favicon/favicon.svg` to website's `src/public/images/favicon.svg`, then change only the favicon `head` entry to `/images/favicon.svg`. Keep `themeConfig.logo` pointing to `/images/logo_light.svg` and `/images/logo_dark.svg`.
4. Add `src/public/images/README.md` documenting the brand repository, **the actual release tag or commit imported**, and the sync command. Keep design editing in brand.
5. Format changed text files, run `npm run check` and `git diff --check` in website. Inspect light/dark navigation and the favicon, then submit a migration PR.
6. After deployment, verify the existing logo URLs still load. Update the GitHub organization avatar to `assets/avatar/xila-avatar-512.png`. Use the black horizontal logo, or a theme-aware picture element, in light-background README contexts.

The repository was created as private. Website deployment remains a separate step: merging the migration PR publishes the imported deployment copies through the existing website pipeline. Keep the actual brand import commit in the website asset README; do not make the website build depend on authenticated access to this repository.

## Future updates

Change the master, regenerate, validate, review and release in brand. Import only the selected assets into consumers and record that version. Preserve old releases; avoid moving `main` references for reproducible builds. Automating this process can be a later, separate change.
