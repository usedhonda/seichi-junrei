# Changelog

このプロジェクトは開発初期段階のSkillです。明確なリリースタグを作成したときに、ここへ変更履歴を追記します。

## 0.7.1 — 2026-10-26

- Added trip intake before production for mostly fixed, early-planning and mixed itineraries, using calendar/text together while retaining per-item booking certainty.
- Added a concise trip brief, grouped material questions and stage-appropriate readiness before full image/layout work; preserve unaffected material when constraints change.
- Documented natural-language starting requests and the distinction between an extraction helper and booking-status interpretation. Guide renderer and existing samples are unchanged.

## 0.7.0 — 2026-10-26

- Replanned JoJo and MONSTER end to end from distinct whole-guide visual storyboards, including chapter copy, artwork count, movement, camera scale, companions, transfer-day rhythm and endings.
- Added eight selected new assets: JoJo desert distance, Iggy poses and a deformed ensemble; MONSTER courtyard, rail travel, over-shoulder street, restrained margin figures and a quiet deformed epilogue. Approved covers and story artwork are preserved.
- Added ordered mixed illustration roles for transitions and escaped work-specific chapter labels, with independent-input and offline-browser coverage.
- Updated the distributable skill, production examples, public screenshots and embedded JoJo demonstration to match the complete reading journeys.

## 0.6.2 — 2026-10-26

- Replaced Conan’s repeated seated compositions with an overhead active hawker scene and a low-angle, full-body walking ensemble closing.
- Added whole-guide visual storyboarding before image generation: asset/drawing/placement counts, reading position, purpose, cast/action, treatment and camera geometry, with a worked Conan plan.

## 0.6.1 — 2026-10-26

- Added recurring transparent character stamps through Conan’s day and a stylized ensemble closing illustration. Existing scene art is retained.
- Added reusable event/closing illustration roles, stamp-sheet display panels and alpha-preserving image embedding.
- Added skill guidance for whole-guide image pacing and user-selected combinations of scene, stamp and ensemble treatments.

## 0.6.0 — 2026-10-25

- Applied the integrated reading journey to JoJo and MONSTER, preserving their distinct adventure/thriller covers and all scene illustrations.
- Added multi-day reading, transfer-only chapters, day/leg maps, secondary observations and explicit cross-day endpoints; captions and order derive from trip input.
- Removed Conan-specific copy/count assumptions, added independent-work/day-order portability checks, and retained dialog-only story art in the offline asset manifest.
- Updated the skill's production/schema guidance and local execution path for the same distributable engine.

## 0.5.0 — 2026-10-25

- Rebuilt Conan as one chronological day: orientation and overview map lead into the actual timed visits, story context, onsite observations, optional mural, rest and next-leg directions.
- Removed separate Conan story/place/itinerary screens; local maps and source notes open at their stops. Existing progress/bookmark IDs are preserved.
- Added a one-day casebook reading-flow contract and browser checks for continuous reading and inline maps. Other guides retain their current compositions; multi-day integration is not yet implemented.

## 0.4.3 — 2026-10-25

- Made maps visible from every guide's cover with a persistent labelled shortcut and an explicit Map/Itinerary navigation label.
- Put the map near the top of the route view, replacing the large decorative lead with a compact heading.

## 0.4.2 — 2026-10-25

- Replaced MONSTER's quiet travel-journal presentation with a psychological-thriller journey: cinematic cover, visual city chapters, story files and optional research notes.

- Added geographic daily/whole-trip maps to the three selected guides with sourced public coordinates, timed-stop focus and external directions.
- Bundled Leaflet controls and license; online basemaps load only in the route view with visible attribution. Offline files retain stops/order and explain the missing road basemap.
- Added map input safety and daily-stop consistency checks; browser CI checks map selection and fallback while blocking external tiles.
- Added map and timetable integration to the reusable production instructions.

## 0.4.1 — 2026-10-25

- Preserved the approved JoJo design and gave Conan and MONSTER distinct document compositions: an investigation notebook and a literary travel journal.
- Added Raffles Long Bar as Conan's third researched stop, a new character illustration, two field checks and a full-day model with transfer/waiting time.
- Separated layout from palette and strengthened skill guidance against substituting color/image swaps for work-specific art direction.

## 0.4.0 — 2026-10-25

- Selected JoJo/Egypt, Conan/Singapore and MONSTER/Germany–Czechia as the three public showcases; retained earlier example URLs.
- Added two character-led guides, seven new final illustrations, source limits, branch-specific discoveries, and a five-day Europe model with dedicated transfer days.
- Added teal casebook and ink/copper visual directions while retaining the same mobile interaction engine.
- Added representative-image preflight and bounded handling of rejection, transient failure and pending generation, preserving completed work.
- Pages builds and isolated browser acceptance include the selected three guides.

## 0.3.3 — 2026-10-25

- Added scene-level discovery research: distinguish familiar works from famous landmarks and investigate specific branches, corners and visual clues.
- Separate story evidence, physical identification and current access; preserve originating speculation and inspect images rather than trusting captions.
- Added a sourced Conan/Singapore research case with observed image-caption mismatches, an unresolved street and a related mural, explicitly distinguished from a completed guide or independent skill evaluation.
- Kept the renderer, existing sample guides and ranking API unchanged.

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
