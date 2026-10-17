# Editable identity sources

`symbol.svg` is the canonical four-rectangle master for the selected Continuity direction. Open it in an SVG editor, preserving the 64-unit viewBox and module orientation.

`identity.json` defines export colors, spacing, the bundled font and the identity version. The horizontal wordmark is generated as vector paths from this font, so published SVGs do not depend on the reader’s installed fonts.

After a change, run `python scripts/export.py` and `python scripts/validate.py` from the repository root. Review the SVGs in light and dark contexts before committing updated exports.
