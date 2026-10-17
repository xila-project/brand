# Xila visual identity repository

This repository owns Xila's visual identity and reusable artwork. It is not the operating-system source or the website implementation. Read `README.md`, `docs/visual-guidelines.md` and the relevant source files before changing assets.

## Selected direction

- Preserve **Continuity**: four separate rectangular modules, a square silhouette, sharp corners and the original orientation. The mark is deliberately abstract; do not introduce a literal X or redesign it unless the task requests a new direction.
- `source/symbol.svg` is the editable geometry master. Its current 64-unit viewBox contains four 18-by-38-unit rectangles with 8-unit end separations.
- `source/identity.json` owns palette, font, spacing and identity version. Prefer reading these values over duplicating them in scripts or documentation.
- Black/white are the primary identity. Ink/paper are neutral presentation colors. Indigo remains optional; do not silently promote it to the primary brand color.
- Keep documentation in English, with concise, concrete instructions and root-relative file paths in prose. Preserve the spelling **Xila**.

## Sources, generated files and history

| Location | Responsibility |
| --- | --- |
| `source/` | Editable symbol and identity configuration |
| `fonts/` | Font required for reproducible outlined wordmarks and its license |
| `scripts/` | Export, validation and explicit website synchronization |
| `assets/` | Generated SVGs, favicons, avatar and social graphics |
| `exports/` | Generated raster variants |
| `integrations/website/images/` | Generated compatibility exports for the website |
| `manifest.json` | Generated SHA-256 inventory of delivery assets |
| `legacy/` | Unmodified original assets and their provenance |
| `docs/` | Visual guidelines and consumer migration instructions |

Edit masters or tooling, regenerate, then commit the resulting exports together. Do not hand-edit individual generated files, regenerate archived originals, or edit manifest hashes to hide drift. Keep `legacy/website/` byte-identical to its recorded source and preserve its provenance. A historical correction must retain evidence of the original import.

Use vector geometry for the established mark and lettering. Do not replace it with raster-generated artwork or approximate its shapes from a screenshot. Finished lockup SVGs must contain outlined lettering, with no installed-font dependency, embedded scripts or external resources. Preserve attribution and font notices; changing the repository or font license is outside routine design work.

## Working environment

Use Python 3.10+ with Cairo available. Install the pinned Python dependencies in an isolated environment, from the repository root:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

On Debian/Ubuntu the native Cairo runtime is supplied by `libcairo2`. Keep font inputs local and exports deterministic; generation must not fetch remote design assets or add timestamps. Reuse existing tools before adding dependencies. Do not commit virtual environments, caches or temporary preview files. Generated delivery assets are intentionally committed.

## Verification

For a source or export-tooling change, run:

```sh
python scripts/export.py
python scripts/validate.py
git diff --check
```

Review the diff for unexpected generated changes. If export tooling changes, regenerate twice and compare the manifest to check determinism. Validation checks geometry, archived hashes, the delivery inventory, self-contained SVGs, PNG dimensions and separations, favicons and local documentation links.

Inspect affected artwork visually as well: light and dark backgrounds, transparent variants, horizontal wordmarks, actual 16/32px symbols and circular avatar crops as relevant. Passing the script is not proof of visual quality or compatibility with every embedded display. State which checks actually ran; distinguish unavailable hardware or browser checks.

For documentation-only changes, check referenced paths and `git diff --check`. Do not regenerate artwork or change the identity version solely for instruction-file or documentation edits.

## Consumer integration

`brand` owns editable masters. Consumers keep deployment copies so rendering and builds do not depend on runtime downloads or authenticated access to this repository, which may be private.

`python scripts/sync_website.py /path/to/website` explicitly replaces the three compatibility logo files. It does not copy the favicon or change configuration. Follow `docs/migration.md` for those steps. Preserve the existing logo URLs and record the exact imported brand commit in the consumer. Do not replace working image URLs with GitHub blob-page links.

Before changing a consumer repository, read its own `AGENTS.md`, preserve unrelated work and run its required checks. Website changes require formatting, `npm run check` and `git diff --check`. Do not merge or deploy a consumer merely because artwork has been updated here; follow the user's requested delivery scope.

## Agent entry points

`AGENTS.md` is the sole instruction source. `CLAUDE.md`, `GEMINI.md` and `.github/copilot-instructions.md` are relative symbolic links to it. Tools that support `AGENTS.md` directly, including Codex and OpenCode, need no extra copy. Preserve Git mode `120000` for the aliases; do not replace them with duplicated prose. If symlink support is disabled in a checkout, document the limitation rather than maintaining competing instruction files.
