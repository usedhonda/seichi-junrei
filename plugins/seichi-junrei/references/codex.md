# Codex-native illustrated pilgrimage workflow

Codex only; canonical instructions: `../skills/seichi-junrei/SKILL.md`.

## Start from a selected work

Read only the relevant trip through an actually connected calendar, or use a supplied itinerary. Present 3–5 evidence-backed works and stop for selection or explicit delegation. Do not repeat a choice already made. Verify the episode/scene-to-place links before composing the guide.

## Native image-generation and preserved characters

Check actual native image-generation availability. Use ImageGen where exposed, or reuse appropriate artwork already approved in the conversation. Do not request API keys, call paid fallback image services or install local diffusion models.

When the user wants character fan art, **keep the recognizable fictional cast** in new compositions. Do not replace the protagonist, companions and scene panels with scenery, anonymous silhouettes or props. Maintain a character/scene coverage list and compare it with the actual rendered phone screens. Follow `editorial-and-art.md`; rights cautions are not a blanket prohibition on original character fan art.

Make separate assets for hero and scene panels. No copied official frames, false official affiliation or falsely documentary compositions. Label fan art and keep provenance/limitations. Actual photographs and third-party stills need their own appropriate usage basis. The label 'generated' is not proof of legal clearance for public reuse.

## Build, do not keep making mockups

Once a visual reference is approved, implement a working mobile HTML. Continue requests mean advancing implementation, not sending more static page pictures. Preserve the approved cast and imagery in the working artifact. Keep all lettering, menus, controls and responsive text in HTML/CSS.

Put image files in a trip workspace outside the plugin cache. References such as `assets/scene-01.webp` are relative to `--assets-root`:

```sh
python /path/to/plugin/scripts/render_guide.py /path/to/trip/guide.json --assets-root /path/to/trip --out /path/to/trip/guide.html
python /path/to/plugin/scripts/lint_guide.py /path/to/trip/guide.html --guide /path/to/trip/guide.json
```

The baseline renderer may be adapted for the accepted mobile design. A generated screenshot is not the HTML and never satisfies interaction tests.

## Quality gates

- No fabricated scene/place claims; sources checked and edition/episode labels accurate.
- Requested characters visible in hero and story panels, including destination chapters; no silent scenic-only fallback.
- Faithful layout, image placement and color hierarchy compared with the approved reference.
- Phone-width page switching, thumb navigation, swipe cards, detail sheets and image zoom function.
- Reduced-motion and storage-unavailable fallback work; no external image loading dependency.
- Images readable even if output grows; disclose artifact size rather than silently stripping art.
- Privacy checked, publication optional, actual generated files delivered with screenshots.
- Report structural tests, browser emulation, mock-storage tests, physical devices and live deployment separately. Never describe an unperformed test or publication as complete.
