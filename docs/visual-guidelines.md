# Xila visual guidelines

Logo design by [Martin Legand](https://www.behance.net/martinlegand).

## Direction

Monogram is the identity adopted on 8 November 2026. Keep the four rounded diagonal arms, the separate center square and the square silhouette. Do not redraw it as the earlier four-rectangle Continuity mark.

## Construction

`source/symbol.svg` preserves the supplied four paths and rounded center rectangle. The original 617.46-unit artwork is uniformly scaled into a 64 × 64 unit viewBox. The center square starts at (249.72, 249.72), measures 118.02 units on each side and has 4.4-unit corner radii before scaling. Keep the supplied path coordinates, corner radii and transparent separations.

`source/lockup.svg` contains the same symbol group and the reviewed lettering outlines. The original complete layout is 1710.4 × 617.46 units, normalized to a height of 64 units. Exports use explicit paths, fills and transforms, with a single SVG namespace and no live text, CSS classes, Adobe metadata or external resources.

The ten original designer exports remain byte-identical in `legacy/2026-11-originals/`. `source/provenance.json` records their hashes. The original complete SVGs declared live Montserrat ExtraBold text with a conflicting weight 700 declaration. The reviewed portable outlines use the bundled variable font at 800 and preserve source positioning; they differ slightly from the original PNG lettering. Do not claim that the supplied PNGs and the outlined lockup are pixel-identical.

## Spacing and sizes

Leave at least 16 units (one quarter of the symbol width) clear around a standalone symbol. Exported bare SVGs have a tight viewBox; provide this margin in the placement. The avatar includes extra crop-safe space.

Keep the spacing and lettering positions in `source/lockup.svg`. Do not substitute a system font or re-typeset the finished lockup.

Use the standalone symbol for favicons and compact icons. 16px is the initial minimum for the unpadded symbol; inspect it at its actual device scale. The full lockup should have a symbol at least 24px high. Pixel hinting or a separate micro-size master may be needed for low-DPI embedded screens; these exports do not certify rendering on every target display.

## Typography

Montserrat is the shared proportional family.

| Role | Weight | Usage |
| --- | --- | --- |
| Text | Regular 400 | Paragraphs, UI text and documentation |
| Headings | SemiBold 600 | Titles and section headings |
| Emphasis | Bold 700 | Strong text |
| Wordmark | ExtraBold 800 | Reviewed logo outlines |

Use the local variable WOFF2 exports for normal and italic styles on the website and browser demo. Keep the supplied OFL notice with deployed fonts. The source TTF files are unmodified upstream Montserrat 9.000 files, recorded in `fonts/provenance.json`. The reviewed wordmark outlines are checked in; generation does not instantiate or reshape the lettering.

Unification concerns family and hierarchy, not identical binaries on every target. Embedded builds retain their current Montserrat Regular subsets at 10/14/18/28px, rather than adding weights to flash without a demonstrated UI need. Render and verify target-specific glyphs through the existing LVGL converter. The terminal keeps Unscii at its current sizes; code on the website keeps its existing monospace stack. Never apply Montserrat to terminal cells or code blocks merely to make every element use one font.

Use this hierarchy in documents and templates. Reusable A4 document and 16:9 presentation templates are available in `templates/typst/`; their PDF specimens demonstrate the hierarchy on light and dark surfaces. These templates do not certify small-screen rendering.

## Palette

| Name | Hex | Role |
| --- | --- | --- |
| Black | `#000000` | True monochrome, light backgrounds and print |
| White | `#FFFFFF` | True monochrome, dark backgrounds |
| Ink | `#171B25` | Neutral dark presentation surface / mark |
| Paper | `#F5F4F0` | Neutral light presentation surface |
| Indigo | `#8D9EFF` | Optional accent exploration |

Prefer black/ink on a light background and white on a dark background. The optional light indigo is strongest on dark backgrounds; avoid relying on it for tiny marks on white. Choose the variant for its background, not for the reader's operating-system setting. In heritage filenames, `logo_dark.svg` means the white logo **for a dark background**.

## Applications

- Website: use the symbol next to the site title. Avoid showing the outlined wordmark alongside another identical title.
- README or presentation cover: use the horizontal lockup.
- GitHub and community avatar: use the padded square avatar, safe for a circular crop.
- Social preview: use the included 1280 × 640 graphic. No screenshots or unsupported product claims are baked into it.
- Embedded bootsplash: start from a monochrome symbol and respect the target's pixel format and margins.

## Avoid

Do not stretch, rotate, alter the corner radii, close the gaps, add shadows/gradients to the core mark, or recolor its modules independently. Do not use a white transparent logo on a light surface. Keep other applications, screenshots and hardware photos outside the mark's clear space.

## Status

The November monogram and outlined lettering were reviewed before adoption. The 400/600/700 UI hierarchy, neutral palette and optional indigo remain unchanged. The principal supplied variant combines a white symbol with black lettering and needs a suitable mid-tone background. Future changes require a visual review and version update.
