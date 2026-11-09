#import "../document.typ": xila-document
#import "../theme.typ": callout, palette

#show: xila-document.with(
  title: "A shared language for Xila.",
  subtitle: "Document template and authoring guide",
  category: "Brand / Template specimen",
  authors: ("Xila project",),
  date: "9 November 2026",
  version: "Example 1.0",
  summary: [A practical starting point for technical notes, proposals and project reports. Replace this example with your own content.],
)

= Start with the decision

Write the point of the document first. Explain who it helps, what changes and which evidence supports the recommendation. Keep headings short and use a concrete title.

This specimen demonstrates Xila’s document hierarchy: Montserrat Regular for text, SemiBold for headings and Bold for emphasis. The outlined logo remains an artwork asset; it is never recreated as text.

#callout[One identity, several formats][
  Use this template for reports and technical notes. Use the companion 16:9 template when the material will be presented on screen.
]

== Structure a useful document

- Give the reader enough context to understand the decision.
- State the constraints before describing the implementation.
- Separate verified results from planned work.
- End with the next action and the person responsible.

== Keep the evidence readable

#table(
  columns: (1fr, 2.3fr),
  table.header([*Element*], [*Purpose*]),
  [Heading], [Helps the reader find the next idea.],
  [Table], [Makes genuinely parallel information easier to compare.],
  [Callout], [Highlights one decision or constraint.],
)

#pagebreak()
= Make the template yours

== Supply document metadata

The template accepts a title, subtitle, category, authors, date, version, summary and language. Omit optional values rather than filling the page with placeholder labels.

```typ
#import "../document.typ": xila-document
#show: xila-document.with(
  title: "Your document title",
  authors: ("Your name",),
  category: "Technical note",
)
```

== Use local, reproducible assets

The palette and typography settings come from `source/identity.json`. The templates use the repository’s outlined SVG logos and local Montserrat font files. Compilation requires no remote package registry or font service.

#callout[Before sharing][
  Check page breaks, links, table wrapping and the distinction between measured results and assumptions. Update the title and author metadata as well as the visible cover.
]

== Credit the work

The Xila Monogram logo was designed by #link("https://www.behance.net/martinlegand")[Martin Legand]. Montserrat is distributed under the SIL Open Font License; preserve `fonts/OFL-Montserrat.txt` when redistributing the font files. See the repository’s `NOTICE` for artwork attribution.

This is a template specimen, not a product specification or a claim about supported hardware.
