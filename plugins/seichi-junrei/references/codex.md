# Codex-native illustrated pilgrimage workflow

`seichi-junrei` is now **Codex only**. The canonical behavioral rules live in `../skills/seichi-junrei/SKILL.md`.

## Before proposing any art

1. Obtain the trip information from a connected calendar **if available** or from a minimal itinerary supplied by the user. Never imply that merely installing the plugin grants calendar permissions.
2. Discover 3–5 **evidence-backed** candidate works, show the user, and **stop** until they choose a main work (or explicitly delegate). The image workflow starts **only after selection**.
3. Verify key source facts and assemble an ordered sequence of real destinations, episode beats and attractive transitions.

## Native ImageGen, not an API integration

Check whether the Codex host session exposes a **native image-generation capability**. If it does:

- Use it to make **distinct visual assets**: one cinematic hero, multiple scene-driven original artworks, and one or more location-transition images. Construct images individually with appropriate orientation, cropping and visual continuity.
- Keep original anime frames, recognizable character designs, logos and distinctive compositions out of the generated artwork without permission. A reference image sets **page design** expectations, not permission to copy protected art. Use motifs, moods, environments, new compositions, architecture and non-identical silhouettes.
- For non-fans, make the scenes understandable via prose. For fans, evoke specific story beats. Pair each scene image with a verified episode/volume or film-sequence description.
- Store the exported images in a writable **trip workspace**, e.g. `/path/to/trip/assets/scene-01.png`. In the guide specification, refer to `assets/scene-01.png` and add the related `media_rights` record with `status: "original_generated"`, the creator/method and a note on non-official status. Add photographer, source and license information for licensed real-world photos.
- Do not render the entire page as an image. Use HTML/CSS for typography, menus, responsive layout, text selection, checks and directions.

If native ImageGen is not available, **do not** substitute a billed API call, add Gemini keys, install ComfyUI/MFLUX or claim that SVG sketches are equivalent. Surface the limitation. User-approved photo-only output may proceed but must be described as a limited alternative.

## Render from a trip workspace

The plugin install can be read-only. Run the renderer with a separate local workspace:

```sh
python /path/to/installed-plugin/scripts/render_guide.py /path/to/trip/guide.json --assets-root /path/to/trip --out /path/to/trip/guide.html
python /path/to/installed-plugin/scripts/lint_guide.py /path/to/trip/guide.html --guide /path/to/trip/guide.json
```

Relative image paths are checked to remain **inside** `--assets-root`; the renderer embeds and compresses images with Pillow. The default root is the plugin directory for bundled examples.

## Quality gates

- No fabricated scene/place claims; sources verified.
- Approved/mockup reference **faithfully** implemented, including art placement; actual mobile screenshot at 390 and 430px.
- Each important story beat has appropriate visual treatment; original scene images **interleaved** with documentary photos and prose. No generic montage as a substitute for the whole guide.
- Images actually load; no horizontal overflow or dead controls; guide works offline.
- No sensitive calendar details included; publishing is optional and requires separate explicit approval.
