#import "theme.typ": *

// A4 report/technical note with a quiet monochrome cover and running furniture.
#let xila-document(
  title: "Document title",
  subtitle: none,
  authors: ("Xila project",),
  date: none,
  version: none,
  category: "Technical document",
  summary: none,
  lang: "en",
  body,
) = {
  set document(title: title, author: authors)
  set text(font: family, size: 10pt, weight: body-weight, fill: palette.ink, lang: lang)
  set par(justify: false, leading: 0.65em, spacing: 0.9em)
  set page(paper: "a4", margin: (x: 24mm, top: 24mm, bottom: 23mm))
  show strong: set text(weight: emphasis-weight)
  show heading: set text(weight: heading-weight)
  show heading.where(level: 1): set text(size: 20pt)
  show heading.where(level: 2): set text(size: 13pt)
  show raw: set text(font: "DejaVu Sans Mono", size: 9pt)
  show raw.where(block: true): block.with(fill: palette.paper, inset: 12pt, width: 100%)
  set heading(numbering: "1.1")
  set list(indent: 12pt, body-indent: 6pt, spacing: 5pt)
  set table(inset: 8pt, stroke: 0.4pt + palette.ink)
  set page(header: none, footer: none)
  pad(top: 6mm, bottom: 6mm)[
    #logo(width: 40mm)
    #v(35mm)
    #eyebrow(category)
    #v(7mm)
    #text(size: 35pt, weight: heading-weight, fill: palette.black, title)
    #if subtitle != none { v(7mm); text(size: 16pt, subtitle) }
    #v(12mm)
    #line(length: 100%, stroke: 1pt + palette.black)
    #v(8mm)
    #if summary != none { block(width: 92%, text(size: 12pt, summary)) }
    #v(1fr)
    #text(weight: heading-weight, authors.join(" · "))
    #v(3mm)
    #text(size: 9pt, (date, version).filter(value => value != none).join("  /  "))
    #v(10mm)
    #text(size: 8pt)[Xila · #link("https://www.xila.dev")[xila.dev]]
  ]
  pagebreak()
  set page(
    header: [
      #text(size: 8pt, weight: heading-weight)[Xila]
      #h(1fr)
      #text(size: 8pt, title)
      #v(4pt)
      #line(length: 100%, stroke: 0.4pt + palette.ink)
    ],
    footer: [
      #text(size: 8pt, category)
      #h(1fr)
      #text(size: 8pt, context counter(page).display("1"))
    ],
  )
  body
}
