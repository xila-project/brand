"""Create compact outlined README headers from local identity inputs."""
from html import escape
import json

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont


def headers(root, config, symbol, svg):
    """Yield transparent light/dark SVG headers from local inputs."""
    font = TTFont(root / config["font"], recalcTimestamp=False)
    units = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    glyph_sets = {weight: font.getGlyphSet(location={"wght": weight})
                  for weight in (400, 500, 800)}

    def text(value, x, baseline, size, weight, color):
        glyphs = glyph_sets[weight]
        commands = []
        cursor = 0
        for character in value:
            name = cmap[ord(character)]
            pen = SVGPathPen(glyphs)
            glyphs[name].draw(TransformPen(pen, (1, 0, 0, 1, cursor, 0)))
            commands.append(pen.getCommands())
            cursor += glyphs[name].width
        scale = min(size / units, 1008 / cursor)
        assert scale * units >= size * 0.75, f"Header text is too long: {value}"
        return (f'<g fill="{color}" transform="translate({x} {baseline}) '
                f'scale({scale} {-scale})"><path d="{" ".join(commands)}"/></g>')

    entries = json.loads((root / "source/repository-headers.json").read_text())
    for entry in entries:
        for theme in ("light", "dark"):
            foreground = config["colors"]["black" if theme == "light" else "white"]
            body = (
                '<g transform="translate(56 60) scale(1.625)">'
                + symbol(foreground) + '</g>'
                + text(config["name"], 212, 58, 16, 500, foreground)
                + text(entry["title"], 210, 115, 52, 800, foreground)
                + text(entry["description"], 213, 158, 24, 400, foreground)
            )
            title = escape(f"Xila {entry['title']} — {entry['description']}")
            yield f"xila-{entry['slug']}-header-{theme}.svg", svg(1280, 224, body, title)
    font.close()
