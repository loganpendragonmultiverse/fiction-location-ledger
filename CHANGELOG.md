# Changelog

## 1.1.1 - 2026-10-19

- Validate scene and location shapes and reject duplicate scene IDs with actionable input errors.
- Create reports exclusively, preserving existing files and dangling symlink targets; handle closed output pipes cleanly.

## 1.1.0 - 2026-10-15

- Resolve explicit location alias chains to canonical IDs with original scene observations.
- Reject ambiguous alias keys, dangling targets and cycles; preserve legacy reports.
- Keep embedded Markdown fences inside report evidence blocks.

## 1.0.0 - 2026-07-26

- Released the first complete Fiction Location Ledger command-line workflow.
- Added deterministic JSON and Markdown reporting, representative examples, and cross-platform tests.
