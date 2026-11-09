// Read the same identity configuration as the asset exporters.
#let identity = json("../../source/identity.json")
#let palette = identity.colors.pairs().fold((:), (colors, pair) => {
  colors.insert(pair.at(0), rgb(pair.at(1)))
  colors
})
#let family = identity.typography.family
#let body-weight = identity.typography.body_weight
#let heading-weight = identity.typography.heading_weight
#let emphasis-weight = identity.typography.emphasis_weight

#let logo(dark: false, width: 34mm) = image(
  if dark { "../../assets/lockup/xila-horizontal-white.svg" }
  else { "../../assets/lockup/xila-horizontal-black.svg" },
  width: width,
  alt: "Xila",
)

#let symbol(dark: false, size: 7mm) = image(
  if dark { "../../assets/symbol/xila-symbol-white.svg" }
  else { "../../assets/symbol/xila-symbol-black.svg" },
  width: size,
  height: size,
  alt: "Xila Monogram",
)

#let eyebrow(body, dark: false) = text(
  size: 9pt, weight: heading-weight,
  fill: if dark { palette.paper } else { palette.ink },
  tracking: 1.1pt,
  upper(body),
)

#let callout(title, body, dark: false) = block(
  width: 100%, inset: 14pt,
  fill: if dark { palette.black } else { palette.paper },
  stroke: (left: 2pt + if dark { palette.white } else { palette.black }),
  [#text(weight: heading-weight, title) #v(5pt) #body],
)
