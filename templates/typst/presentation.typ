#import "theme.typ": *

#let xila-presentation(title: "Presentation title", authors: ("Xila project",), lang: "en", body) = {
  set document(title: title, author: authors)
  set text(font: family, size: 18pt, weight: body-weight, lang: lang)
  set par(leading: 0.6em, spacing: 0.9em)
  show strong: set text(weight: emphasis-weight)
  show heading: set text(weight: heading-weight)
  show raw: set text(font: "DejaVu Sans Mono", size: 14pt)
  set list(indent: 14pt, body-indent: 8pt, spacing: 12pt)
  body
}

// Each helper emits exactly one 16:9 page. Keep content concise; pages do not shrink text.
#let slide(title: none, kicker: none, dark: false, footer: "Xila", body) = {
  let foreground = if dark { palette.white } else { palette.ink }
  page(
    width: 320mm, height: 180mm,
    margin: (left: 20mm, right: 20mm, top: 16mm, bottom: 17mm),
    fill: if dark { palette.ink } else { palette.paper },
    footer: text(size: 8pt, fill: foreground)[
      #footer #h(1fr) #context counter(page).display("1")
    ],
    {
      set text(fill: foreground)
      if kicker != none { eyebrow(kicker, dark: dark); v(3mm) }
      if title != none { text(size: 30pt, weight: heading-weight, title); v(9mm) }
      body
    },
  )
}

#let title-slide(title, subtitle: none, authors: "Xila project", date: none) = slide(dark: true, footer: "xila.dev")[
  #logo(dark: true, width: 43mm)
  #v(17mm)
  #block(width: 92%)[#text(size: 39pt, weight: heading-weight, title)]
  #if subtitle != none { v(6mm); text(size: 21pt, subtitle) }
  #v(1fr)
  #text(size: 11pt)[#authors #if date != none { [ · #date] }]
]

#let section-slide(number, title, subtitle: none) = slide(dark: true)[
  #eyebrow(number, dark: true)
  #v(15mm)
  #text(size: 41pt, weight: heading-weight, title)
  #if subtitle != none { v(8mm); text(size: 21pt, subtitle) }
]

#let split-slide(title, left, right, kicker: none, dark: false) = slide(title: title, kicker: kicker, dark: dark)[
  #grid(columns: (1fr, 1fr), gutter: 14mm, left, right)
]

#let closing-slide(title: "Let’s build together.", subtitle: none, contact: "xila.dev") = slide(dark: true, footer: "Xila")[
  #logo(dark: true, width: 43mm)
  #v(20mm)
  #text(size: 39pt, weight: heading-weight, title)
  #if subtitle != none { v(7mm); text(size: 20pt, subtitle) }
  #v(1fr)
  #text(size: 16pt, contact)
]
