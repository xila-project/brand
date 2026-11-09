# Xila Typst templates

Reusable A4 documents and 16:9 presentations for Xila’s Monogram identity. The templates use local Montserrat fonts and outlined logo assets, and read palette and type weights from `source/identity.json`. Black/white are primary; ink/paper provide neutral presentation surfaces. There are no external Typst package dependencies or network requests during compilation.

## Preview

- [Document PDF](previews/document.pdf): cover, running headers and footers, sections, table, callouts and code.
- [Presentation PDF](previews/presentation.pdf): title, content, split columns, section, flow and closing slides, on light and dark surfaces.

These PDFs are specimens, not product specifications. Example dates and content are explicit inputs and must be replaced for actual documents.

## Build

Install Typst separately; the templates and previews were checked with **Typst 0.15.1**. From the repository root:

```sh
python3 scripts/build_typst.py
```

The script sets the font path, disables system fonts, fixes the PDF creation timestamp and rejects compiler diagnostics. It writes to `templates/typst/previews/`; use `--output /tmp/xila-typst` for temporary PDFs or `--typst /path/to/typst` to select an executable. Use the same CLI version for byte-for-byte regeneration.

To compile your own source from the repository root:

```sh
typst compile --root . --font-path fonts --ignore-system-fonts \
  --creation-timestamp 0 templates/typst/examples/document.typ /tmp/document.pdf
```

Pass the repository root with `--root`: templates load the identity and artwork from outside the example directory. Keep the repository layout intact when using these sources. To move a template into a consumer, copy its required local sources together and adapt their paths explicitly; do not add network asset URLs.

## Documents

Start from `templates/typst/examples/document.typ`:

```typ
#import "../document.typ": xila-document
#import "../theme.typ": callout

#show: xila-document.with(
  title: "Your document title",
  subtitle: "A concise explanation",
  authors: ("Your name",),
  category: "Technical note",
  date: "9 November 2026",
  version: "Draft 1",
  summary: [Explain the purpose in two or three sentences.],
)

= Your first section

Write the point first.

#callout[Decision][State the decision and why it matters.]
```

`title`, `authors` and `category` have defaults. `subtitle`, `date`, `version` and `summary` default to `none` and are omitted. `lang` defaults to `"en"`. Authors are an array of strings; retain the trailing comma for a single author. The cover counts as page 1; running numbers start visibly on page 2. Standard Typst headings, lists, tables, figures and links remain available.

## Presentations

Start from `templates/typst/examples/presentation.typ`:

```typ
#import "../presentation.typ": *

#show: xila-presentation.with(
  title: "Your presentation title",
  authors: ("Your name",),
)

#title-slide([Your presentation title], subtitle: "Your subtitle", authors: "Your name")
#slide(title: "One clear point")[Your content.]
#split-slide("A comparison", [Left column.], [Right column.])
#section-slide("02 / Design", "Your next section")
#closing-slide(contact: "Your contact details")
```

- `slide(title: none, kicker: none, dark: false, footer: "Xila", body)` creates a content slide.
- `title-slide(title, subtitle: none, authors: "Xila project", date: none)` creates a dark cover.
- `split-slide(title, left, right, kicker: none, dark: false)` creates two equal columns.
- `section-slide(number, title, subtitle: none)` creates a dark section divider.
- `closing-slide(title: "Let’s build together.", subtitle: none, contact: "xila.dev")` creates a dark closing page.

Each helper creates a fixed 320 × 180 mm page. Keep content concise and inspect the PDF: helpers do not shrink overflowing text automatically. Use content line breaks (`\ `) when deliberate line breaks are needed. Metadata in `xila-presentation` and visible cover details are separate; update both. Put detailed prose in the document template.

The `callout(title, body, dark: false)` helper is available from `theme.typ`. Pass `dark: true` when placing it on a dark slide. Code uses Typst’s bundled DejaVu Sans Mono rather than Montserrat.

## Identity, licensing and attribution

The shared identity source is `source/identity.json`; the reference rules are in `docs/visual-guidelines.md`. Templates retain a generous clear space around the supplied lockup and never redraw or re-typeset it. The template source is covered by the repository’s Apache-2.0 license.

The Monogram logo was designed by [Martin Legand](https://www.behance.net/martinlegand). Keep this deployment credit and the repository’s `NOTICE` when distributing the template bundle. Montserrat has a separate SIL Open Font License in `fonts/OFL-Montserrat.txt`; preserve it with redistributed fonts. For an offline bundle, include `templates/typst/`, `source/identity.json`, `assets/lockup/`, `assets/symbol/`, both Montserrat TTF files in `fonts/`, the font license, `LICENSE` and `NOTICE`. Keep their relative paths intact.

Preview PDFs are rebuilt with `scripts/build_typst.py` and live alongside the template examples, outside the artwork export inventory. Regenerate them after template, identity, font or logo changes; `scripts/export.py` remains responsible for SVG/PNG/ICO artwork and its manifest.
