# Website compatibility files

These generated files replace the existing logo files without changing their public paths. Run `python scripts/sync_website.py /path/to/website` from the brand repository. See [the migration guide](../../docs/migration.md) for favicon integration and validation.

`logo_light.svg` is black on a transparent background. `logo_dark.svg` and `logo_dark.png` are white on a transparent background. These are deployment copies; edit `source/symbol.svg` and regenerate to update them.
