# Xila visual guidelines

## Direction

Continuity is the selected direction. Keep the abstract four-module construction, the square silhouette and the sharp corners. The symbol does not have to depict a letter. Associate it with the name Xila on introductory materials.

## Construction

The master uses a 64 × 64 unit viewBox. Each rectangle is 18 units thick and 38 units long. The four rectangles are rotations of one another around (32,32):

| Module | x | y | Width | Height |
| --- | ---: | ---: | ---: | ---: |
| Left/top | 0 | 0 | 18 | 38 |
| Bottom/left | 0 | 46 | 38 | 18 |
| Top/right | 26 | 0 | 38 | 18 |
| Right/bottom | 46 | 26 | 18 | 38 |

Separations between neighboring ends are 8 units. The original used thickness 20, length 40 and separation 4 on the same normalized square. Maintain the orientation and the rectangular proportions.

## Spacing and sizes

Leave at least 16 units (one quarter of the symbol width) clear around a standalone symbol. Exported bare SVGs have a tight viewBox; provide this margin in the placement. The avatar includes extra crop-safe space.

The horizontal lockup uses a 20-unit gap and a 56-unit visible wordmark height against the 64-unit symbol. The lettering is outlined from the bundled DejaVu Sans Bold font. Do not substitute a system font in a finished lockup.

Use the standalone symbol for favicons and compact icons. 16px is the initial minimum for the unpadded symbol; inspect it at its actual device scale. The full lockup should have a symbol at least 24px high. Pixel hinting or a separate micro-size master may be needed for low-DPI embedded screens; these exports do not certify rendering on every target display.

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

Do not stretch, rotate, round the modules, close their gaps, add shadows/gradients to the core mark, or recolor its modules independently. Do not use a white transparent logo on a light surface. Keep other applications, screenshots and hardware photos outside the mark's clear space.

## Status

The symbol direction was selected in conversation. The layout rules, font lockup and optional palette are the initial working specification packaged with it. Future changes should receive a visual review and a version update. Similarity research was preliminary; it does not establish exclusivity.
