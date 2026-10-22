---
name: seichi-junrei
description: Turn Google Calendar travel plans (flights, hotels, destinations) into an evidence-checked choice of 3–5 anime, manga, film or literary pilgrimage themes. After the user chooses, research scene-to-place connections and create a visually rich, offline-friendly mobile travel guide. Sharing/publication is optional. Use for travel planning, 聖地巡礼, anime or movie locations, trip companions' interactive itineraries, and travel storytelling.
---

# Seichi Junrei — 勝手に聖地巡礼ツアー

**Goal:** Make a travel companion feel as though they have stepped into a story. A travel-booking calendar is only a starting signal. The core product is a beautiful, factual, enjoyable mobile guide for the actual trip—not a public website.

## Core contract: candidate selection is mandatory

1. Read the user's requested trip or the nearest relevant upcoming travel window from **Google Calendar**, if connected. Limit retrieval to the trip; read flight and lodging entries, deduplicate timezones, infer no reservation or transport leg that is not evidenced. If access is unavailable, request an itinerary or calendar export once; don't fake connector access. Read `references/calendar-and-privacy.md`; for exported events, run `scripts/extract_calendar.py`.
2. Find **3–5 well-researched candidates** from anime, manga, film and, when appropriate, literature. This is discovery, not a single automated recommendation. Candidates need grounded scene/setting/filming evidence and feasible visits. Reject imaginary pilgrimage pins. Read `references/research-and-ranking.md`. Structured inputs can be ranked by `scripts/rank_candidates.py`.
3. Present a concise **candidate ballot** including title, type, why it fits, a memorable scene, actual connection grade, itinerary fit and any caveat; supply one short question asking the user which work(s) they choose. **STOP HERE.** Do not select silently or generate the full guide. The user can select 1 main + up to 2 secondary works; an explicit "you decide" is a valid delegation. If a work has weak location evidence, clearly flag it before selection. Where UI controls exist, use a single multi-select with a designated main work; ordinary chat selections also work. Use `scripts/make_ballot.py` if a portable HTML ballot is useful. Do not interpret the top score as consent.
4. Only after the choice, research selected works deeply using primary sources: exact episode numbers/titles, volume edition and chapter where verified, scenes, filming locations, map addresses, current opening hours, and the actual trip's time windows. Track all significant claims with URLs and access dates. Separate **confirmed fictional setting**, **real filming location**, **creator-confirmed inspiration**, **strong resemblance**, **thematic connection** and **unverified fan speculation**. Scenes from an adaptation do not automatically establish a filming location. Refer to `references/research-and-ranking.md`.
5. Write a compelling narrative aligned to **travel order**, not necessarily episode order. Give non-fans sufficient context; give fans memorable beats with optional spoiler expansions. Keep both real history and episode recall enjoyable. Cite exact sources; do not misrepresent "fan interpretation" as production fact. See `references/editorial-and-art.md`.
6. Design before implementation: create one clear visual direction or user-supplied reference. **Design lock:** treat an approved visual mockup as a concrete acceptance target; do not re-interpret its layout just as vague mood. Use images between text sections: destination photo → key story beat illustration → real architecture → story aftermath. Default to properly licensed photography and truly original inspired imagery (not copyrighted frame/character/logo reproduction). Require rights provenance for every asset. See `references/editorial-and-art.md`.
7. Produce a **self-contained mobile HTML** with embedded image bytes and interactive episode/story cards, route, date itinerary and map links. Use the deterministic `scripts/render_guide.py` with the data contract in `references/guide-contract.md`, adapting the template when warranted. Never substitute a static generated screenshot for a working site. Use `scripts/lint_guide.py` and a real browser at 390px, 430px and desktop if available; inspect screenshots and fix clipping or unreadable text. Default output is an HTML artifact, not a live URL.
8. Remove private fields before handing the file to companions: booking reference/PNR, seat, contact, hotel room, personal names, event descriptions, internal notes and private calendar links. Do not export raw calendar JSON. Separate private input and public guide. Verify no accidental leakage with `scripts/lint_guide.py` and review `references/calendar-and-privacy.md`.
9. **Sharing is optional.** A single HTML file viewed offline or handed via AirDrop is a complete outcome. For user-requested link sharing, offer available Sites/hosting tools with restricted or unlisted settings where supported; never claim a Site was published or updated without a verified URL. Before a public/unlisted launch, get explicit confirmation after privacy/rights check. Unlisted/noindex is not authentication. If the direct publishing integration isn't available, deliver the working file and precise handoff rather than pretending that deployment occurred.

## Non-negotiable quality gates

- **User choice gate:** 3–5 candidates offered; a user selection/delegation recorded; no default silently chosen.
- **Grounding gate:** Claims and media relations categorized; primary support for distinctive scene-to-place claims; episode/movie edition checked independently. When uncertain, mark uncertain or cut.
- **Trip gate:** Real schedule, travel direction, transit feasibility and venue hours verified; no fabricated openings or travel durations. Separate closing time from last entry.
- **Editorial gate:** Fan scenes woven throughout, not just an intro; understandable to first-timers; exciting progression; clear spoilers.
- **Visual gate:** A mobile **website**, not a magazine screenshot: usable hierarchy, tap targets, no horizontal overflow, loaded images, tested interactions, visual match to reference.
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

## Run locally, with skill root as cwd

```bash
python scripts/rank_candidates.py examples/egypt_candidates.json
python scripts/make_ballot.py examples/egypt_candidates.json --out /tmp/story-choices.html
python scripts/render_guide.py examples/egypt_guide.json --out /tmp/story-guide.html
python scripts/lint_guide.py /tmp/story-guide.html --guide examples/egypt_guide.json
```

The sample guide contains an **explicit illustrative user-choice record** for testing. Never carry it over to a new trip. The live conversation must always stop for the current user's choice.
