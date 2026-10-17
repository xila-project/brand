#!/usr/bin/env python3
"""Explicitly copy the three compatibility exports to a website checkout."""
from pathlib import Path
import argparse
import shutil

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("website", type=Path)
    args = parser.parse_args()
    target = args.website.resolve()
    if not (target / ".vitepress/config.mts").is_file():
        parser.error("Expected the website repository with .vitepress/config.mts")
    destination = target / "src/public/images"
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("logo_light.svg", "logo_dark.svg", "logo_dark.png"):
        shutil.copyfile(ROOT / "integrations/website/images" / name, destination / name)
        print(f"Updated {destination / name}")


if __name__ == "__main__":
    main()
