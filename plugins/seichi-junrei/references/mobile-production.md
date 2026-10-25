# Produce a guide at the public sample's quality

The default `scripts/render_guide.py` uses the same mobile CSS and interaction runtime as the published STARDUST sample. Those resources are inside `assets/mobile-guide/` and travel with the installed plugin. Do not reconstruct its interaction code for every trip or fall back to the former static brochure.

## Turn research into a production brief

Keep the confirmed work/adaptation, intended readers, trip order, requested cast and approved design reference in the trip workspace. For each destination, connect a verified scene to something the traveler can actually notice. Write enough context for a first-time companion and specific emotional callbacks for fans. Expand beyond a one-line plot summary: `episodes[].body`, `stages[].paragraphs`, and rich `highlights` supply the reading experience.

Plan the images before generation: character-led portrait cover; distinct scene illustrations for story beats; scene art repeated prominently inside the corresponding destination; real-world imagery with honest provenance. Generate missing assets separately through available native ImageGen, preserving the cast and visual continuity. A scene image's fictional backdrop does not prove a real location. Use approved supplied or appropriately cleared original book art when that is the requested treatment. Do not ship the demonstration's cast as another work's characters.

Keep a per-image record in `media_rights`: `file`, `status`, `creator`, `alt`, `notes`, optional `source_url` / `license_url`, and `characters` (depicted character names). If the requested design includes characters, set `meta.character_art_required=true`; the renderer then refuses missing cast records for the cover, story cards or destination scenes. This validates the declared manifest, not the actual pixels: inspect the rendered art too.

## Build from real data

Copy `examples/egypt_guide.json` or `examples/oxford_alice_guide.json` to a writable trip workspace as a structural starting point. Replace their content, images, sources, consent record and identity. Never inherit sample user selection as real approval.

Use the schema in `guide-contract.md`. The examples demonstrate two different works, two/three destinations, two/three days, different mission totals and numeric/named story IDs. All navigation, dialogs, day tabs and progress counts are generated from the input. Give `meta.id` a distinct, stable ID so revisions keep progress and unrelated trips do not share it.

Run from the installed plugin root (absolute paths also work):

```sh
python scripts/render_guide.py /trip/guide.json --assets-root /trip --out /trip/guide.html
python scripts/lint_guide.py /trip/guide.html --guide /trip/guide.json
```

Use `meta.title_lines`, `wordmark`, `cover_line`, `hero_position` and the prose fields to art-direct the result. Choose `meta.theme` from `night-gold`, `pop-postcard` (bright cream/aqua/raspberry), `casebook` (teal/amber detective field notes), or `ink-copper` (quiet ink/copper). The latter three preserve portrait covers and landscape chapter art without side cropping. Theme changes share the tested interaction runtime; compare actual screenshots for each trip. Do not promise that arbitrary new imagery will always look good without this work.

## Verify the actual output

With Playwright available, the reusable acceptance runner tests a supplied JSON and the already-built HTML, using the installed plugin's resources and the real asset root:

```sh
python tests/browser_check.py --guide /trip/guide.json --assets-root /trip --html /trip/guide.html --outdir /trip/checks
```

It serves a real browser origin, tests 360/390/430/520px, checks local/global mission synchronization and persistence, bookmarks, scene and story dialogs, next/previous stories, zoom, Escape, day switching, native rail scrolling, save/offline reopening, reduced motion and blocked storage. If no guide is supplied it tests the selected JoJo/Egypt, Conan/Singapore and MONSTER/Europe showcase guides. Earlier Alice and K-On production examples remain available explicitly. Browser coverage is Chromium emulation; do not claim physical iPhone or Safari acceptance.

Inspect its cover, destination and detail screenshots. Compare with the approved reference for character visibility, art size, typography, density, readability and cropping; tests cannot judge those. When a visual check fails, correct that specific issue and verify the affected view. Also inspect the itinerary and relevant captions in the browser.

Deliver the editable guide data, assets and standalone HTML. Keep private booking data separate. A public demo may replace precise personal details with clearly labelled dummy/model data. Only set `meta.public_url` after actual publication is authorized; offline sharing falls back to a real HTML download. Public deployment is optional and separate from completing a guide.

## Lessons from the London productions

- Identify AI fan art on the cover with `meta.art_label`, and explain its provenance in `art_note` and the media records. It is neither official footage nor photographic evidence.
- Keep every requested face visible in the actual phone crop. For an ensemble portrait and landscape chapter art, `pop-postcard` preserves the whole image; inspect text overlapping faces too.
- Film locations and visitor attractions can differ: actual filming platforms and a present-day photo trolley need separate descriptions. Fan anime-location records must not become official production confirmation.
- For films, editorial story-beat numbers are not episode numbers or verified timestamps. Explain what the numbering means.
- Budget walking, transfers, meals, rest and queues. Mark unmeasured durations as editorial estimates, and link the current transport operator; do not present a model route as a booked itinerary.
