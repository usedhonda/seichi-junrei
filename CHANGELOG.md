# Changelog

このプロジェクトは開発初期段階のSkillです。明確なリリースタグを作成したときに、ここへ変更履歴を追記します。

## 0.3.2 — 2026-10-25

- Added a researched London example for the K-On! anime film, with newly generated, labelled unofficial fan art.
- Added a bright postcard theme using the same mobile runtime, with full-ensemble artwork and readable light-theme sheets.
- Distinguished filming locations, visitor attractions, fan location records and illustrative composites; labelled route durations as estimates.
- Bundled the London guide and its artwork in the distributable skill, with browser acceptance and Pages publication.

## 0.3.1 — 2026-10-25

- Replaced the static baseline with the public sample's reusable mobile design and runtime inside the installed plugin.
- Added data-driven destinations, story IDs, days, synchronized missions, bookmarks, sheets, zoom, motion and offline save/share.
- Public Pages builds now use the same renderer as installed skills; original character art and full scene prose are bundled.
- Added Oxford/Alice as a second, sourced example with three destinations/days and different mission counts.
- Added isolated-plugin browser acceptance for both trips and instructions for inspecting the actual generated output.
- Fixed privacy lint false positives on base64 image bytes and preserved suitable WebP artwork without recompression.

## Earlier changes

- v0.3.0: Codex-only direction. Removed CC marketplace, command and plugin manifest.
- Native ImageGen-first illustration workflow, no external image API keys or local diffusion installation.
- New `--assets-root` lets Codex embed dynamically generated images from a separate trip workspace.
- Tests ensure Codex-only packaging and writable external asset root while preserving user-choice/privacy checks.


- v0.2.0: single self-contained skill shared by Claude Code and Codex, modelled after makeloop's marketplace design
- Claude Code marketplace/command, Codex marketplace/plugin manifests, portable root plugin.json and direct-skill compatibility wrapper
- Isolated plugin distribution tests, README install instructions and host-capability boundaries

- Public README with setup, limitations, example workflow, privacy and asset-rights notes
- MIT license for code and original documentation; visual assets excluded
- CONTRIBUTING, SECURITY, community guidance and issue templates
- CI installs Pillow; modernized, read-only GitHub Actions workflow
- Calendar export helper no longer preserves raw event titles that may include personal names

## Initial import (2026-10-22)

- User-selected 3–5 story candidates
- Evidence-aware scene/location linking
- Offline-first, image-embedded mobile HTML generator
- Japan/Egypt-inspired demonstration data and tests
