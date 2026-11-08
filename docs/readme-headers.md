# README headers

Logo design by [Martin Legand](https://www.behance.net/martinlegand).

Compact headers share the Monogram identity while naming each Xila repository and its role. The visible brand is **Xila**; `xila-project` remains the GitHub handle.

## Delivery files

Each header is a self-contained 1280 × 224 SVG with outlined lettering and a transparent background. Use black artwork for light themes and white artwork for dark themes. There is no background tile, font download, script or remote resource.

| Repository | Light theme | Dark theme |
| --- | --- | --- |
| `core` | [Light](../assets/headers/xila-core-header-light.svg) | [Dark](../assets/headers/xila-core-header-dark.svg) |
| `platforms` | [Light](../assets/headers/xila-platforms-header-light.svg) | [Dark](../assets/headers/xila-platforms-header-dark.svg) |
| `applications` | [Light](../assets/headers/xila-applications-header-light.svg) | [Dark](../assets/headers/xila-applications-header-dark.svg) |
| `package_manager` | [Light](../assets/headers/xila-package_manager-header-light.svg) | [Dark](../assets/headers/xila-package_manager-header-dark.svg) |
| `registry` | [Light](../assets/headers/xila-registry-header-light.svg) | [Dark](../assets/headers/xila-registry-header-dark.svg) |
| `workspace` | [Light](../assets/headers/xila-workspace-header-light.svg) | [Dark](../assets/headers/xila-workspace-header-dark.svg) |
| `website` | [Light](../assets/headers/xila-website-header-light.svg) | [Dark](../assets/headers/xila-website-header-dark.svg) |
| `brand` | [Light](../assets/headers/xila-brand-header-light.svg) | [Dark](../assets/headers/xila-brand-header-dark.svg) |
| `wasm_application_template` | [Light](../assets/headers/xila-wasm_application_template-header-light.svg) | [Dark](../assets/headers/xila-wasm_application_template-header-dark.svg) |
| `.github` | [Light](../assets/headers/xila-community-header-light.svg) | [Dark](../assets/headers/xila-community-header-dark.svg) |

## Edit and regenerate

`source/repository-headers.json` owns the names and role summaries. `scripts/repository_headers.py` owns the shared layout and outlines text with the bundled Montserrat font; `source/symbol.svg` supplies the unchanged monogram. Names use weight 800, descriptions 400 and the small Xila label 500. No additional Python dependencies are required.

From the brand root:

```sh
python scripts/export.py
python scripts/validate.py
git diff --check
```

The exporter writes `assets/headers/` and includes every delivery hash in `manifest.json`. Validation checks dimensions, self-contained SVGs and transparent raster corners. Review both themes on non-white/non-black surfaces and check long repository names before publishing.

## README integration

The shared writing template and adaptation guide live in [xila-project/.github](https://github.com/xila-project/.github), under `templates/`. Use one H1 containing the themed picture, with descriptive image alt text; do not repeat the title as a separate visible Markdown H1.

Consumers keep local deployment copies, normally `.github/brand/header-light.svg` and `.github/brand/header-dark.svg`. Record the exact imported brand commit in the accompanying asset README and preserve the OFL font attribution. The organization profile can keep its copies under `profile/assets/`. Brand itself references the generated headers directly.

Keep each repository's commands, examples, warnings, anchors and specialized sections. The shared navigation and neutral footer do not establish a common software license. Existing consumer builds do not need to run this generator or fetch identity assets at build time.
