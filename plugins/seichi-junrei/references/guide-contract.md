# Input data contracts

The renderer accepts a UTF-8 JSON guide specification and produces the same interactive mobile system used by the public sample. Use plain Unicode text. All `image` fields point to **local image files**; never use a third-party remote image for the final offline build.

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


## Sample-quality editorial fields

- `meta.id`: stable safe identifier for a trip's local progress. Use a distinct ID for another trip.
- `meta.title_lines`: title lines for a portrait cover; `wordmark`, `cover_line`, `hero_position` (`"40% 50%"`) control the composition. Optional `introduction` is a list of paragraphs.
- `meta.character_art_required`: true when character-led art was requested. Cover, episode and scene images then require nonempty `media_rights[].characters`; rendered pixels still need inspection.
- `meta.public_url`: optional verified public HTTPS URL. Leave absent for a local companion guide. No sample URL is built into the runtime.
- `meta.theme`: `night-gold` (default), `pop-postcard`, `casebook`, or `ink-copper`. Unknown values are rejected. `meta.art_label` is an optional escaped cover credit, for example `AI FAN ART · 非公式`.
- `meta.art_note`, `checked_note`, `itinerary_note`, `closing`: accurate reader-facing notes. Dummy itinerary data must be labelled as illustrative.
- `works[].episodes[].id`: unique story-beat ID across works, including named IDs for films/books. `number` is a display label; navigation does not assume numeric or consecutive episodes. Add `name`, `place`, `tag`, `body` (paragraph list), `spoiler` (optional text) and `note` for rich reading. Every story card needs its own relevant `image` and `source_url`.
- `stages[].name`: localized navigation label; `location` is the large chapter title. `paragraphs` supplies scene/place prose. Keep `connections` as explicit classifications with sources.
- `stages[].scenes[].episode_id`: optional reference to a story ID. Omit when no corresponding beat exists; the UI will not show a dead link. `spoiler=true` hides the description in normal cards and body until opened. Images are required.
- `stages[].highlights`: strings or `{title, description, map_url, source_url}` objects. Use objects for practical, sourced observations. `practical` and `practical_title` supply travel advice grounded in the actual schedule.
- `stages[].missions`: `{id, text, detail}`. IDs must be unique within a stage; the engine namespaces them across destinations and deduplicates home/chapter views.
- `itinerary`: optional list of `{id, label, events:[{time, title, description}]}`. Any number of days is supported. When absent, stage `date` and `events` produce one tab per stage. These are display data, not automatically computed routing or current opening-hours evidence.
- `media_rights`: local file, status, creator, descriptive `alt`, notes, optional characters and source/license URL. Existing suitable WebP files are preserved without another lossy compression pass. The default theme is navy/gold; it does not impose a franchise on another trip.

The renderer never consults `site/` or a sibling repository. Plugin installation includes its templates, runtime and illustrative fixtures. Runtime code is fixed; text from the JSON is escaped, not executed.
