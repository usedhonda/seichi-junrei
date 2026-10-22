# Changelog

このプロジェクトは開発初期段階のSkillです。明確なリリースタグを作成したときに、ここへ変更履歴を追記します。

## Unreleased

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
