# Repository social previews

Logo design by [Martin Legand](https://www.behance.net/martinlegand).

The ten Xila repository previews share the Monogram 2.0.0 identity: black background, white outlined lettering, the repository name, its role and its GitHub address. All artwork and export tooling are maintained here in brand; consumer repositories do not need image copies.

## Choose an image

| Repository | Role | Delivery |
| --- | --- | --- |
| `core` | Kernel subsystems and reusable libraries. | [PNG](../assets/social/repositories/xila-core-social-1280x640.png) · [SVG](../assets/social/repositories/xila-core-social-1280x640.svg) |
| `platforms` | Platform drivers and runtime assembly. | [PNG](../assets/social/repositories/xila-platforms-social-1280x640.png) · [SVG](../assets/social/repositories/xila-platforms-social-1280x640.svg) |
| `applications` | Native applications and WebAssembly guests. | [PNG](../assets/social/repositories/xila-applications-social-1280x640.png) · [SVG](../assets/social/repositories/xila-applications-social-1280x640.svg) |
| `package_manager` | Build, sign and verify application packages. | [PNG](../assets/social/repositories/xila-package_manager-social-1280x640.png) · [SVG](../assets/social/repositories/xila-package_manager-social-1280x640.svg) |
| `registry` | Signed package metadata and publisher keys. | [PNG](../assets/social/repositories/xila-registry-social-1280x640.png) · [SVG](../assets/social/repositories/xila-registry-social-1280x640.svg) |
| `workspace` | Shared tooling and cross-repository integration. | [PNG](../assets/social/repositories/xila-workspace-social-1280x640.png) · [SVG](../assets/social/repositories/xila-workspace-social-1280x640.svg) |
| `website` | Documentation, tutorials and architecture guides. | [PNG](../assets/social/repositories/xila-website-social-1280x640.png) · [SVG](../assets/social/repositories/xila-website-social-1280x640.svg) |
| `brand` | The visual identity of Xila. | [PNG](../assets/social/repositories/xila-brand-social-1280x640.png) · [SVG](../assets/social/repositories/xila-brand-social-1280x640.svg) |
| `wasm_application_template` | A Rust starter for your first Xila application. | [PNG](../assets/social/repositories/xila-wasm_application_template-social-1280x640.png) · [SVG](../assets/social/repositories/xila-wasm_application_template-social-1280x640.svg) |
| `.github` | Discover Xila and contribute to the project. | [PNG](../assets/social/repositories/xila-community-social-1280x640.png) · [SVG](../assets/social/repositories/xila-community-social-1280x640.svg) |

Use the PNG for upload. Each image is opaque, 1280 × 640 pixels and below 1 MB. The `.github` community repository uses the `community` filename and display title.

## Edit and regenerate

The editable SVG masters live in `source/repository-social/`. Lettering is outlined from the bundled Montserrat family: ExtraBold 800 for titles and Regular 400 / Medium 500 for supporting text. The small horizontal logo and large monogram preserve the reviewed identity geometry. Keep the font attribution in `fonts/OFL-Montserrat.txt`.

Edit the master vectors, then run the existing commands from the brand root:

```sh
uv run --locked python scripts/export.py
uv run --locked python scripts/validate.py
git diff --check
```

The exporter recreates SVG and PNG delivery files in `assets/social/repositories/` and includes their hashes in `manifest.json`. It does not fetch fonts or artwork and adds no timestamps. Commit the edited masters and regenerated exports together. The general-purpose `assets/social/xila-social-1280x640.png` remains available independently.

## Apply on GitHub

Committing these files does not configure repository social previews. For each repository, open **Settings → General → Social preview → Edit → Upload an image** and select its corresponding PNG. See [GitHub's social preview instructions](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview).

Keep source artwork and delivery files in brand. No remote image downloads are required by consumer builds, and changing an image here does not silently modify GitHub settings.
