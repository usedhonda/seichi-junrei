# Input data contracts

The renderer accepts a UTF-8 JSON guide specification. Use plain Unicode text. All `image` fields point to **local image files**; never use a third-party remote image for the final offline build.

```json
{
  "meta": {"title":"Travel title", "subtitle":"Short Japanese tagline", "dates":"2026.10.23 – 10.24", "regions":"ASWAN → ABU SIMBEL", "hero_image":"assets/...webp", "theme":"night-gold", "visibility":"companions"},
  "selection": {"primary_work_id":"work-1", "secondary_work_ids":[], "user_confirmed":true, "delegated":false},
  "works": [{"id":"work-1", "title":"Full title", "medium":"anime", "episodes":[{"number":"25", "title":"Exact episode name", "summary":"Short verified plot", "image":"assets/...webp", "source_url":"https://..."}]}],
  "stages": [{"id":"aswan", "label":"STAGE 01", "location":"ASWAN", "date":"2026.10.23", "hook":"A memorable line in your own words", "image":"assets/...webp", "location_note":"historical fact", "map_url":"https://www.google.com/maps/search/?api=1&query=Aswan", "connections":[{"type":"named_setting", "description":"What is supported", "source_url":"https://..."}], "scenes":[{"title":"Scene title", "episode":"EP.27", "description":"Moment", "image":"assets/...webp", "spoiler":false, "source_url":"https://..."}], "highlights":["Real-world things to notice"], "events":[{"time":"13:10", "label":"Depart by air (share-safe)"}], "missions":[{"id":"take-photo", "text":"Observe the light on the water"}]}],
  "sources": [{"label":"Official episode 27", "url":"https://..."}],
  "media_rights": [{"file":"assets/...webp", "status":"original_generated", "creator":"OpenAI-generated original composition", "notes":"Not a real documentary image"}]
}
```

Fields `selection.user_confirmed` and `selection.delegated` must be explicit booleans. Renderer refuses to run otherwise, or if chosen work ID isn't provided. Example fixtures demonstrate technical mechanics, not that the current real user chose any work.

`connections[].type` must be from: `named_setting`, `filming_location`, `official_inspiration`, `documented_connection`, `thematic`, `speculative`. The UI labels the strength of each connection. Prefer to omit speculation.

No `private_calendar` or `booking` object is allowed anywhere in the guide. The output HTML rejects suspicious booking/ID field names, remote image URLs and disallowed source protocols. Private data must stay in a separate runtime-only file.


## ImageGen-generated asset root

For new trips, keep generated images in a writable workspace rather than the installed Skill directory. The CLI `--assets-root` points to that workspace; image paths in the JSON remain relative (for example `assets/scene-01.png`). The renderer rejects path traversal, remote image URLs and missing rights declarations. Pillow converts supported PNG/JPEG/WebP inputs into embedded WebP data URIs.

```sh
python /path/to/plugin/scripts/render_guide.py /path/to/trip/guide.json --assets-root /path/to/trip --out /path/to/trip/guide.html
```

Do not treat the sample's already-selected test fixture as a real user's current choice. Production requires an actual user selection/delegation record. ImageGen availability is checked by Codex at runtime, not assumed from the plugin manifest.
