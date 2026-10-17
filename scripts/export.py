#!/usr/bin/env python3
"""Build the SVG, PNG and ICO brand assets from the checked-in sources."""
from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib
import json

import cairosvg
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SVG_NS = "http://www.w3.org/2000/svg"
CONFIG = json.loads((ROOT / "source/identity.json").read_text())
COLORS = CONFIG["colors"]
SOURCE = ET.parse(ROOT / "source/symbol.svg").getroot()
SHAPES = list(SOURCE.find(f"{{{SVG_NS}}}g"))


def symbol(color):
    rects = "".join(
        '<rect ' + " ".join(f'{key}="{value}"' for key, value in shape.attrib.items()) + '/>'
        for shape in SHAPES
    )
    return f'<g fill="{color}">{rects}</g>'


def svg(width, height, body, title="Xila"):
    return (
        f'<svg xmlns="{SVG_NS}" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">'
        f'<title id="title">{title}</title>{body}</svg>\n'
    )


def write(path, content):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def render(content, path, width=None, height=None):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(bytestring=content.encode(), write_to=str(path),
                    output_width=width, output_height=height)


def wordmark():
    """Return outlined glyphs and their exact ink bounds in font units."""
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.transformPen import TransformPen
    font = TTFont(ROOT / CONFIG["font"])
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    commands = []
    cursor = 0
    bounds = []
    kern = {}
    if "kern" in font:
        for table in font["kern"].kernTables:
            kern.update(table.kernTable)
    previous = None
    for char in CONFIG["name"]:
        name = cmap[ord(char)]
        if previous:
            cursor += kern.get((previous, name), 0)
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(TransformPen(pen, (1, 0, 0, 1, cursor, 0)))
        commands.append(pen.getCommands())
        bp = BoundsPen(glyphs)
        glyphs[name].draw(bp)
        if bp.bounds:
            a, b, c, d = bp.bounds
            bounds.append((a + cursor, b, c + cursor, d))
        cursor += font["hmtx"][name][0]
        previous = name
    xmin = min(b[0] for b in bounds)
    ymin = min(b[1] for b in bounds)
    xmax = max(b[2] for b in bounds)
    ymax = max(b[3] for b in bounds)
    return " ".join(commands), (xmin, ymin, xmax, ymax)


def lockup(mark_color, text_color):
    path, (xmin, ymin, xmax, ymax) = wordmark()
    scale = CONFIG["wordmark_cap_height_units"] / (ymax - ymin)
    x = 64 + CONFIG["horizontal_gap_units"]
    y = (64 + CONFIG["wordmark_cap_height_units"]) / 2
    width = round(x + (xmax - xmin) * scale, 4)
    body = symbol(mark_color) + (
        f'<g transform="translate({x - xmin * scale} {y + ymin * scale}) '
        f'scale({scale} {-scale})" fill="{text_color}"><path d="{path}"/></g>'
    )
    return width, body


def main():
    for name in ("ink", "black", "white", "indigo"):
        content = svg(64, 64, symbol(COLORS[name]), f"Xila symbol — {name}")
        write(f"assets/symbol/xila-symbol-{name}.svg", content)
        for size in (16, 32, 48, 64, 128, 256, 512, 1024):
            render(content, f"exports/png/symbol-{name}-{size}.png", size, size)
    for name, mark, text in (
        ("ink", "ink", "ink"), ("black", "black", "black"),
        ("white", "white", "white"),
        ("indigo-on-dark", "indigo", "white"),
        ("indigo-on-light", "indigo", "ink"),
    ):
        width, body = lockup(COLORS[mark], COLORS[text])
        content = svg(width, 64, body, f"Xila horizontal logo — {name}")
        write(f"assets/lockup/xila-horizontal-{name}.svg", content)
        render(content, f"exports/png/horizontal-{name}-1024.png", 1024)

    # Explicit background keeps favicons legible in either browser theme.
    favicon = svg(80, 80, '<rect width="80" height="80" rx="12" '
                  f'fill="{COLORS["paper"]}"/><g transform="translate(8 8)">'
                  + symbol(COLORS["ink"]) + '</g>', "Xila favicon")
    write("assets/favicon/favicon.svg", favicon)
    render(favicon, "assets/favicon/favicon-48.png", 48, 48)
    Image.open(ROOT / "assets/favicon/favicon-48.png").save(
        ROOT / "assets/favicon/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    render(favicon, "assets/favicon/apple-touch-icon.png", 180, 180)
    render(favicon, "assets/favicon/android-chrome-192.png", 192, 192)
    render(favicon, "assets/favicon/android-chrome-512.png", 512, 512)

    # Circular-avatar safe margin: symbol corners remain inside the crop.
    avatar = svg(512, 512, f'<rect width="512" height="512" fill="{COLORS["ink"]}"/>'
                 '<g transform="translate(96 96) scale(5)">'
                 + symbol(COLORS["white"]) + '</g>', "Xila avatar")
    write("assets/avatar/xila-avatar.svg", avatar)
    render(avatar, "assets/avatar/xila-avatar-512.png", 512, 512)

    width, body = lockup(COLORS["white"], COLORS["white"])
    scale = 880 / width
    social = svg(1280, 640,
                 f'<rect width="1280" height="640" fill="{COLORS["ink"]}"/>'
                 f'<g transform="translate(200 {320 - 32 * scale}) scale({scale})">'
                 + body + '</g>', "Xila social preview")
    write("assets/social/xila-social.svg", social)
    render(social, "assets/social/xila-social-1280x640.png", 1280, 640)

    # Compatibility names describe the target background, as on the website.
    for target, variant in (("logo_light.svg", "black"), ("logo_dark.svg", "white")):
        write(f"integrations/website/images/{target}",
              (ROOT / f"assets/symbol/xila-symbol-{variant}.svg").read_text())
    render((ROOT / "assets/symbol/xila-symbol-white.svg").read_text(),
           "integrations/website/images/logo_dark.png", 1600, 1600)
    files = sorted(p for folder in ("assets", "exports", "integrations/website/images")
                   for p in (ROOT / folder).rglob("*") if p.is_file())
    manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    write("manifest.json", json.dumps({"version": CONFIG["version"], "sha256": manifest}, indent=2) + "\n")
    print(f"Exported {len(files)} assets from source/symbol.svg")


if __name__ == "__main__":
    main()
