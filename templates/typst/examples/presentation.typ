#import "../presentation.typ": *
#import "../theme.typ": callout

#show: xila-presentation.with(
  title: "A shared language for Xila",
  authors: ("Xila project",),
)

#title-slide(
  [A shared language\ for Xila.],
  subtitle: "Presentation template and authoring guide",
  date: "9 November 2026",
)

#slide(title: "One idea per slide.", kicker: "01 / Narrative")[
  Lead with the point. Give the audience a clear reason to care before adding the implementation details.

  - Use short, concrete headings.
  - Keep the supporting material easy to scan.
  - Let diagrams and examples do useful work.
]

#split-slide(
  "Built from the same identity.",
  [
    *Typography*

    Montserrat Regular 400 for body text. SemiBold 600 for headings. Bold 700 for emphasis.
  ],
  [
    *Artwork*

    Use the supplied Monogram lockup. Preserve its geometry, proportions and clear space.
  ],
  kicker: "02 / Visual system",
)

#section-slide("03 / Application", "Make room\nfor the content.", subtitle: "A quiet frame for a clear explanation.")

#slide(title: "Explain the flow.", kicker: "03 / Application")[
  #grid(
    columns: (1fr, auto, 1fr, auto, 1fr),
    gutter: 5mm,
    [*Context*\ What the reader needs to know.],
    [→],
    [*Decision*\ What you propose and why.],
    [→],
    [*Evidence*\ What you checked and learned.],
  )
  #v(11mm)
  #callout[Keep the claim precise][Use actual results for product claims. This diagram describes a presentation structure.]
]

#slide(title: "Ready to adapt.", dark: true, kicker: "04 / Delivery")[
  - Replace the specimen with your own content.
  - Keep each slide inside its fixed 16:9 frame.
  - Check contrast, line breaks and attribution.
  - Export a PDF and review it at presentation size.
]

#closing-slide(
  title: "Your next idea\nstarts here.",
  subtitle: "Xila templates · Monogram identity 2.0.0",
  contact: [xila.dev · Logo design: Martin Legand],
)
