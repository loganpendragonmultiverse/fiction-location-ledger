# Fiction Location Ledger

[![CI](https://github.com/loganpendragonmultiverse/fiction-location-ledger/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/fiction-location-ledger/actions/workflows/ci.yml)

Collect named fictional locations, first appearances, descriptions, and scene usage. The command runs locally, uses explicit UTF-8 JSON input, and produces deterministic JSON or Markdown reports without modifying the supplied source material.

## Three-minute start

```bash
python -m pip install .
location-ledger examples/sample.json
location-ledger examples/sample.json --format json --output report.json
```

The example documents the complete v1 input shape. Markdown is intended for immediate review; JSON preserves structured evidence for scripts and later comparison. An existing output file is never overwritten.

## Privacy and platforms

All story data stays local.

Python 3.10 or newer is supported on Windows, macOS, and Linux. The package has no runtime dependencies, telemetry, account, or hosted service.

## Interpretation boundary

Locations and descriptions must be supplied explicitly. The ledger does not perform named-entity recognition or infer whether aliases identify the same place.

## Development

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
python -m build
```

The project is feature-complete for its documented v1 scope. Maintenance focuses on correctness, security, compatibility, and well-supported input improvements.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Explicit aliases (1.1)

Add an optional `aliases` list to the existing input, for example
`[{"alias": "Old Gate", "canonical": "城門"}]`. Labels match after trimming and
Unicode case folding. Canonical IDs are the normalized terminal labels; a terminal
must appear in the supplied scenes. Chains are allowed, while cycles, repeated
alias keys (including case variants), and missing targets reject the entire input.
An alias label may also appear in scenes: the explicit mapping authorizes that merge.
There is no fuzzy matching. Different places must have different labels.

With `aliases` present, each location includes its canonical `id` and original
`observations` (scene ID plus an untouched `location` object), while first appearance,
scene usage and descriptions aggregate in input order. Without it the legacy report
shape is preserved. No source observations are rewritten. Markdown uses a fence
longer than embedded backtick runs to keep supplied labels inside the evidence block.
