#!/usr/bin/env python3
"""Validate geometry, provenance, delivery hashes, SVG portability and sizes."""
from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib
import json
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
NS = "{http://www.w3.org/2000/svg}"


def main():
    source = ET.parse(ROOT / "source/symbol.svg").getroot()
    rects = source.findall(f"{NS}g/{NS}rect")
    boxes = {tuple(int(rect.get(k)) for k in ("x", "y", "width", "height")) for rect in rects}
    assert len(boxes) == 4
    assert {(64 - y - h, x, h, w) for x, y, w, h in boxes} == boxes
    assert all(min(w, h) == 18 and max(w, h) == 38 for x, y, w, h in boxes)
    assert all(0 <= x < x + w <= 64 and 0 <= y < y + h <= 64 for x, y, w, h in boxes)

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

    for path in (ROOT / "assets").rglob("*.svg"):
        doc = ET.parse(path).getroot()
        assert doc.get("viewBox"), path
        assert doc.find(f"{NS}title") is not None, path
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
            assert groups == 4, (path, groups)

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
            assert (path.parent / target.split("#",1)[0]).exists(), (path, target)
    print(f"PASS: geometry, 3 legacy hashes, {len(actual)} delivery files, SVG portability, raster separations, icons and document links")


if __name__ == "__main__":
    main()
