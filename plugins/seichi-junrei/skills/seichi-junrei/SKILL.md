---
name: seichi-junrei
description: Turn Google Calendar travel plans (flights, hotels, destinations) into an evidence-checked choice of 3–5 anime, manga, film or literary pilgrimage themes. After the user chooses, research scene-to-place connections and create a visually rich, offline-friendly mobile travel guide. Sharing/publication is optional. Use for travel planning, 聖地巡礼, anime or movie locations, trip companions' interactive itineraries, and travel storytelling.
---

# Seichi Junrei — 勝手に聖地巡礼ツアー

## Codex execution and native image generation

This Skill targets **Codex only**. Invoke it as `$seichi-junrei:seichi-junrei` when the plugin is installed, or `$seichi-junrei` if a direct Agent Skill is registered. Follow the actual discovered host UI; do not invent commands.

- Resolve the **plugin root** two levels above this file (from `skills/seichi-junrei/SKILL.md` to `plugin.json`, `scripts/`, `assets/`, `references/`, `examples/`). Use full paths or run scripts with that root as cwd; never assume the user's project is this root.
- This Skill does not bundle Google Calendar or ImageGen privileges. **Check which tools exist in the current Codex execution session.** If Calendar is unavailable, ask for an itinerary or supplied export; never claim an unseen reservation.
- After user selection, use Codex's **native image-generation tool** (e.g., ImageGen when exposed) for genuinely original, scene-specific cover and interleaved illustrations. Generate meaningful separate images, not one full-page screenshot or repeated generic artwork. Keep lettering and layout in HTML/CSS. Follow `references/codex.md` and `references/editorial-and-art.md`.
- **No extra image API:** do not request a Gemini/OpenAI API key, invoke billed third-party image services or install/run local models such as ComfyUI/MFLUX as a workaround. If native image generation is missing or fails, report the missing capability and ask whether to proceed with licensed photographs only or to complete the visual step in a compatible Codex session. A photo-only guide must be explicitly marked as a compromise, not the promised full illustrated result.
- Native-generated images are saved under a **trip workspace** (e.g., `guide-workspace/assets/`), not the read-only plugin install. Run the renderer with `--assets-root <trip-workspace>` and the guide JSON's relative `assets/...` paths. The renderer checks each path stays within that root. The sample data still uses the bundled assets when the option is omitted.
- Keep private travel drafts, generated images and final HTML in an authorized workspace outside the plugin cache. No public deployment or sharing without a separate request.

**Goal:** Make a travel companion feel as though they have stepped into a story. A travel-booking calendar is only a starting signal. The core product is a beautiful, factual, enjoyable mobile guide for the actual trip—not a public website.

## Core contract: candidate selection is mandatory

1. Read the user's requested trip or the nearest relevant upcoming travel window from **Google Calendar**, if connected. Limit retrieval to the trip; read flight and lodging entries, deduplicate timezones, infer no reservation or transport leg that is not evidenced. If access is unavailable, request an itinerary or calendar export once; don't fake connector access. Read `references/calendar-and-privacy.md`; for exported events, run `scripts/extract_calendar.py`.
2. Find **3–5 well-researched candidates** from anime, manga, film and, when appropriate, literature. This is discovery, not a single automated recommendation. Candidates need grounded scene/setting/filming evidence and feasible visits. Reject imaginary pilgrimage pins. Read `references/research-and-ranking.md`. Structured inputs can be ranked by `scripts/rank_candidates.py`.
3. Present a concise **candidate ballot** including title, type, why it fits, a memorable scene, actual connection grade, itinerary fit and any caveat; supply one short question asking the user which work(s) they choose. **STOP HERE.** Do not select silently or generate the full guide. The user can select 1 main + up to 2 secondary works; an explicit "you decide" is a valid delegation. If a work has weak location evidence, clearly flag it before selection. Where UI controls exist, use a single multi-select with a designated main work; ordinary chat selections also work. Use `scripts/make_ballot.py` if a portable HTML ballot is useful. Do not interpret the top score as consent.
4. Only after the choice, research selected works deeply using primary sources: exact episode numbers/titles, volume edition and chapter where verified, scenes, filming locations, map addresses, current opening hours, and the actual trip's time windows. Track all significant claims with URLs and access dates. Separate **confirmed fictional setting**, **real filming location**, **creator-confirmed inspiration**, **strong resemblance**, **thematic connection** and **unverified fan speculation**. Scenes from an adaptation do not automatically establish a filming location. Refer to `references/research-and-ranking.md`.
5. Write a compelling narrative aligned to **travel order**, not necessarily episode order. Give non-fans sufficient context; give fans memorable beats with optional spoiler expansions. Keep both real history and episode recall enjoyable. Cite exact sources; do not misrepresent "fan interpretation" as production fact. See `references/editorial-and-art.md`.
6. Design before implementation: use a clear visual direction or the user's supplied reference. **Design lock:** treat an approved mockup as an acceptance target, not vague inspiration. When native ImageGen is available, create **distinct original visuals** for the hero, pivotal episode beats and key location transitions. Alternate licensed real-world imagery with scene-specific story illustrations across the article; do not replace all scenes with a single mood picture or repeat a generic image. Compose actual text, menus and responsive layout in HTML/CSS, never as frozen text in an image. Record the generation method, creator and rights limits for each asset. See `references/editorial-and-art.md`.
7. Produce a **self-contained mobile HTML** with embedded image bytes and interactive episode/story cards, route, date itinerary and map links. Use `scripts/render_guide.py <guide.json> --assets-root <trip-workspace> --out <guide.html>` with the contract in `references/guide-contract.md`, adapting the template where warranted. The example defaults to bundled assets; new trips use an external workspace image root. Never substitute a static generated screenshot for a working site. Use `scripts/lint_guide.py` and a real browser at 390px, 430px and desktop if available; inspect screenshots and fix clipping or unreadable text. Default output is an HTML artifact, not a live URL.
8. Remove private fields before handing the file to companions: booking reference/PNR, seat, contact, hotel room, personal names, event descriptions, internal notes and private calendar links. Do not export raw calendar JSON. Separate private input and public guide. Verify no accidental leakage with `scripts/lint_guide.py` and review `references/calendar-and-privacy.md`.
9. **Sharing is optional.** A single HTML file viewed offline or handed via AirDrop is a complete outcome. For user-requested link sharing, offer available Sites/hosting tools with restricted or unlisted settings where supported; never claim a Site was published or updated without a verified URL. Before a public/unlisted launch, get explicit confirmation after privacy/rights check. Unlisted/noindex is not authentication. If the direct publishing integration isn't available, deliver the working file and precise handoff rather than pretending that deployment occurred.

## Non-negotiable quality gates

- **User choice gate:** 3–5 candidates offered; a user selection/delegation recorded; no default silently chosen.
- **Grounding gate:** Claims and media relations categorized; primary support for distinctive scene-to-place claims; episode/movie edition checked independently. When uncertain, mark uncertain or cut.
- **Trip gate:** Real schedule, travel direction, transit feasibility and venue hours verified; no fabricated openings or travel durations. Separate closing time from last entry.
- **Editorial gate:** Fan scenes woven throughout, not just an intro; understandable to first-timers; exciting progression; clear spoilers.
- **Visual gate:** A mobile **website**, not a magazine screenshot: usable hierarchy, tap targets, no horizontal overflow, loaded images, tested interactions, visual match to reference. For illustrated guides, distinct native-generated scene art must appear throughout, not only on the cover. Missing ImageGen is a reported limitation, **never an automatic silent SVG fallback**.
- **Privacy gate:** No sensitive booking details inside HTML. Verify before link sharing.
- **Rights gate:** Private group sharing is not a blanket copyright exemption. A generated fan image may be derivative even when not copied pixel-for-pixel. Do not call it categorically lawful. Prefer motifs, newly composed characters and locations, licensed materials, and any applicable official guidelines. Document sources/permissions.

## Scripts and data

- `scripts/extract_calendar.py` — parse a bounded Google Calendar JSON export into a private trip summary (no raw descriptions).
- `scripts/rank_candidates.py` — score evidenced alternatives. **Ranking is advisory; never auto-select.**
- `scripts/make_ballot.py` — generate an optional offline selection HTML that copies a chosen work ID; the chat's selection remains the official gate.
- `scripts/render_guide.py` — generate a self-contained, image-embedded mobile HTML **only when** `selection.user_confirmed` or `selection.delegated` is explicitly true.
- `scripts/lint_guide.py` — verify HTML structure, images, privacy strings, required scenes and absence of remote images.
- `examples/egypt_candidates.json`, `examples/egypt_guide.json` — illustrative test fixtures and sources; not reusable evidence for other trips.
- `assets/nile-original.webp` — originally generated illustrative art; imagery is *interpretative*, not an accurate geographic composite or an anime screenshot.

## Run the bundled demo, with plugin root as cwd

```bash
python scripts/rank_candidates.py examples/egypt_candidates.json
python scripts/make_ballot.py examples/egypt_candidates.json --out /tmp/story-choices.html
python scripts/render_guide.py examples/egypt_guide.json --out /tmp/story-guide.html
python scripts/lint_guide.py /tmp/story-guide.html --guide examples/egypt_guide.json
```

For a real itinerary, save ImageGen output into an authorized trip workspace, set relative paths and `media_rights` in the guide JSON, then call `--assets-root /absolute/path/to/trip-workspace`. No API keys are needed. A native ImageGen tool must be available for automatic new original images.

The sample guide contains an **explicit illustrative user-choice record** for testing. Never carry it over to a new trip. The live conversation must always stop for the current user's choice.
