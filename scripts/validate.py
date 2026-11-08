#!/usr/bin/env python3
"""Validate geometry, provenance, delivery hashes, SVG portability and sizes."""
from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib
import io
import json
import re
from urllib.parse import urlsplit
import cairosvg
from PIL import Image
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
NS = "{http://www.w3.org/2000/svg}"


def main():
    source = ET.parse(ROOT / "source/symbol.svg").getroot()
    assert source.get("viewBox") == "0 0 64 64"
    assert len(source.findall(f".//{NS}rect")) == 1, "Missing center square"
    assert len(source.findall(f".//{NS}path")) == 4, "Expected four monogram arms"
    original = ET.parse(ROOT / "legacy/2026-11-originals/Logo Alix - monogramme Noir.svg").getroot()
    def geometry(document):
        return [(node.tag, node.attrib) for node in document.iter()
                if node.tag in (f"{NS}rect", f"{NS}path")]
    assert geometry(source) == geometry(original), "Supplied monogram paths were altered"
    assert source.find(f"{NS}g").get("transform") == f"scale({64 / 617.46})"
    lockup = ET.parse(ROOT / "source/lockup.svg").getroot()
    assert ET.tostring(lockup.find(f"{NS}g")) == ET.tostring(source.find(f"{NS}g")), "Lockup symbol differs from master"
    imported = json.loads((ROOT / "source/provenance.json").read_text())
    for entry in imported["originals"]:
        assert hashlib.sha256((ROOT / entry["path"]).read_bytes()).hexdigest() == entry["sha256"], entry["path"]

    for entry in json.loads((ROOT / "legacy/provenance.json").read_text()):
        raw = (ROOT / entry["archive_path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == entry["sha256"]
        assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == entry["git_blob_sha"]

    manifest = json.loads((ROOT / "manifest.json").read_text())
    assert manifest["version"] == json.loads((ROOT / "source/identity.json").read_text())["version"]
    for path, sha in manifest["sha256"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, path
    actual = {str(p.relative_to(ROOT)) for folder in ("assets", "exports", "integrations/website/images")
              for p in (ROOT / folder).rglob("*") if p.is_file()}
    assert actual == set(manifest["sha256"]), "Manifest omits or invents assets"

    config = json.loads((ROOT / "source/identity.json").read_text())
    assert config["font_weight"] == 800
    assert config["typography"]["family"] == "Montserrat"
    provenance = json.loads((ROOT / "fonts/provenance.json").read_text())
    for name, info in provenance["files"].items():
        assert hashlib.sha256((ROOT / "fonts" / name).read_bytes()).hexdigest() == info["sha256"]
    for style in ("normal", "italic"):
        font = TTFont(ROOT / f"assets/typography/Montserrat-{style}.woff2")
        assert "Montserrat" in font["name"].getDebugName(1)
        weight = next(axis for axis in font["fvar"].axes if axis.axisTag == "wght")
        assert weight.minValue <= 400 and weight.maxValue >= 700
        assert (font["post"].italicAngle != 0) == (style == "italic")
    assert (ROOT / "assets/typography/OFL.txt").read_bytes() == (ROOT / "fonts/OFL-Montserrat.txt").read_bytes()
    css = (ROOT / "assets/typography/montserrat.css").read_text()
    assert "https://" not in css
    for target in re.findall(r'url\("([^"]+)"\)', css):
        assert (ROOT / "assets/typography" / target).is_file()

    vectors = [p for folder in ("source", "assets", "integrations")
               for p in (ROOT / folder).rglob("*.svg")]
    for path in vectors:
        doc = ET.parse(path).getroot()
        assert doc.get("viewBox"), path
        assert doc.find(f"{NS}title") is not None, path
        assert path.read_text().count('xmlns=') == 1, path
        assert all(node.tag in {f"{NS}{tag}" for tag in ("svg", "title", "desc", "g", "path", "rect")} for node in doc.iter()), path
        assert not any(k in ("class", "style", "data-name") or k.startswith("on") for node in doc.iter() for k in node.attrib), path
        assert not doc.findall(f".//{NS}text"), f"Unoutlined text in {path}"
        assert not doc.findall(f".//{NS}script"), path
        assert not any(k.endswith("href") for node in doc.iter() for k in node.attrib), path

    for path in (ROOT / "exports/png").glob("symbol-*.png"):
        size = int(path.stem.rsplit("-", 1)[1])
        with Image.open(path) as image:
            assert image.size == (size, size), path
            alpha = image.convert("RGBA").getchannel("A")
            assert alpha.getextrema() == (0, 255), path
            # Open separations must survive the 16px raster, not merge modules.
            mask = image.convert("RGBA").getchannel("A")
            seen = set()
            groups = 0
            for y in range(size):
                for x in range(size):
                    if (x, y) in seen or mask.getpixel((x, y)) < 128:
                        continue
                    groups += 1
                    todo = [(x, y)]
                    seen.add((x, y))
                    while todo:
                        a, b = todo.pop()
                        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                            c, d = a + dx, b + dy
                            if 0 <= c < size and 0 <= d < size and (c,d) not in seen and mask.getpixel((c,d)) >= 128:
                                seen.add((c,d))
                                todo.append((c,d))
            assert groups == 5, (path, groups)

    social_masters = list((ROOT / "source/repository-social").glob("*.svg"))
    assert social_masters, "No repository social preview masters"
    for master in social_masters:
        delivery = ROOT / "assets/social/repositories" / master.with_suffix(".png").name
        assert delivery.is_file(), delivery
        assert delivery.stat().st_size < 1_000_000, delivery
        with Image.open(delivery) as image:
            assert image.size == (1280, 640), delivery
            assert image.convert("RGBA").getchannel("A").getextrema() == (255, 255), delivery

    headers = json.loads((ROOT / "source/repository-headers.json").read_text())
    assert len({entry["repository"] for entry in headers}) == len(headers)
    for entry in headers:
        for theme in ("light", "dark"):
            path = ROOT / f"assets/headers/xila-{entry['slug']}-header-{theme}.svg"
            assert path.is_file(), path
            document = ET.parse(path).getroot()
            assert document.get("viewBox") == "0 0 1280 224", path
            raster = Image.open(io.BytesIO(cairosvg.svg2png(
                url=str(path), output_width=320, output_height=56))).convert("RGBA")
            alpha = raster.getchannel("A")
            assert alpha.getextrema() == (0, 255), f"Header must be transparent: {path}"
            assert all(alpha.getpixel(point) == 0 for point in
                       ((0, 0), (319, 0), (0, 55), (319, 55))), path
            title = document.find(f"{NS}title").text
            assert entry["title"] in title and entry["description"] in title, path

    with Image.open(ROOT / "assets/social/xila-social-1280x640.png") as image:
        assert image.size == (1280, 640)
    with Image.open(ROOT / "assets/avatar/xila-avatar-512.png") as image:
        assert image.size == (512, 512)
    with Image.open(ROOT / "assets/favicon/favicon.ico") as image:
        assert image.ico.sizes() == {(16,16),(32,32),(48,48)}
    for name in ("logo_light.svg", "logo_dark.svg", "logo_dark.png"):
        assert (ROOT / "integrations/website/images" / name).is_file()

    for path in ROOT.rglob("*.md"):
        for target in re.findall(r"\]\(([^\s)]+)\)", path.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            assert (path.parent / urlsplit(target).path).exists(), (path, target)
    print(f"PASS: five-part geometry, original and legacy hashes, {len(actual)} delivery files, SVG portability, raster separations, icons and document links")


if __name__ == "__main__":
    main()
