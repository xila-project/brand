#!/usr/bin/env python3
"""Compile local Typst specimens without fetching packages, fonts or artwork."""

import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--typst", default="typst", help="Typst executable (tested with 0.15.1)")
    parser.add_argument(
        "--output", type=Path, default=ROOT / "templates/typst/previews",
        help="PDF output directory (default: templates/typst/previews)",
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for name in ("document", "presentation"):
        command = [
            args.typst, "compile", "--root", str(ROOT),
            "--font-path", str(ROOT / "fonts"), "--ignore-system-fonts",
            "--creation-timestamp", "0",
            str(ROOT / f"templates/typst/examples/{name}.typ"),
            str(args.output / f"{name}.pdf"),
        ]
        result = subprocess.run(command, text=True, capture_output=True)
        if result.returncode:
            raise SystemExit(
                f"Typst failed for {name} (exit {result.returncode}):\n"
                f"{result.stderr or result.stdout}"
            )
        if result.stderr:
            raise SystemExit(f"Typst emitted diagnostics for {name}:\n{result.stderr}")
        print(f"Built {args.output / f'{name}.pdf'}")


if __name__ == "__main__":
    main()
