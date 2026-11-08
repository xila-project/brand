#!/usr/bin/env python3
"""Build the SVG, PNG and ICO brand assets from the checked-in sources."""
from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib
import json

import cairosvg
from fontTools.ttLib import TTFont
from PIL import Image

from svg_utils import clean

ROOT = Path(__file__).resolve().parents[1]
SVG_NS = "http://www.w3.org/2000/svg"
CONFIG = json.loads((ROOT / "source/identity.json").read_text())
COLORS = CONFIG["colors"]
SOURCE = ET.parse(ROOT / "source/symbol.svg").getroot()
LOCKUP = ET.parse(ROOT / "source/lockup.svg").getroot()


def recolor(group, color):
    group = deepcopy(group)
    group.set("fill", color)
    for node in group.iter():
        if "fill" in node.attrib:
            node.set("fill", color)
    return ET.tostring(group, encoding="unicode")


def symbol(color):
    return recolor(SOURCE.find(f"{{{SVG_NS}}}g"), color)


def svg(width, height, body, title="Xila"):
    return clean(
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


def lockup(mark_color, text_color):
    """Recolor the reviewed outlines without reshaping the wordmark."""
    mark, lettering = LOCKUP.findall(f"{{{SVG_NS}}}g")
    width = float(LOCKUP.get("viewBox").split()[2])
    return width, recolor(mark, mark_color) + recolor(lettering, text_color)


def main():
    # Preserve the upstream font timestamps for deterministic local web exports.
    for style, source in (("normal", CONFIG["font"]), ("italic", CONFIG["italic_font"])):
        webfont = TTFont(ROOT / source, recalcTimestamp=False)
        webfont.flavor = "woff2"
        target = ROOT / "assets/typography" / f"Montserrat-{style}.woff2"
        target.parent.mkdir(parents=True, exist_ok=True)
        webfont.save(target)
    write("assets/typography/OFL.txt", (ROOT / "fonts/OFL-Montserrat.txt").read_text())
    family = CONFIG["typography"]["family"]
    faces = "\n\n".join(
        f'@font-face {{\n  font-family: "{family}";\n'
        f'  src: url("./Montserrat-{style}.woff2") format("woff2");\n'
        f'  font-style: {style};\n  font-weight: 100 900;\n  font-display: swap;\n}}'
        for style in ("normal", "italic")
    )
    write("assets/typography/montserrat.css", faces + "\n")
    for name in ("ink", "black", "white", "indigo"):
        content = svg(64, 64, symbol(COLORS[name]), f"Xila symbol — {name}")
        write(f"assets/symbol/xila-symbol-{name}.svg", content)
        for size in (16, 32, 48, 64, 128, 256, 512, 1024):
            render(content, f"exports/png/symbol-{name}-{size}.png", size, size)
    for name, mark, text in (
        ("ink", "ink", "ink"), ("black", "black", "black"),
        ("white", "white", "white"),
        ("principal", "white", "black"),
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
    # Repository previews are maintained centrally as outlined vector masters.
    for master in sorted((ROOT / "source/repository-social").glob("*.svg")):
        content = clean(master.read_text())
        write(f"assets/social/repositories/{master.name}", content)
        render(content, f"assets/social/repositories/{master.stem}.png", 1280, 640)

    files = sorted(p for folder in ("assets", "exports", "integrations/website/images")
                   for p in (ROOT / folder).rglob("*") if p.is_file())
    manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    write("manifest.json", json.dumps({"version": CONFIG["version"], "sha256": manifest}, indent=2) + "\n")
    print(f"Exported {len(files)} assets from source/symbol.svg")


if __name__ == "__main__":
    main()
