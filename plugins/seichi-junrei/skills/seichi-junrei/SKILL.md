---
name: seichi-junrei
description: Turn travel plans into 3–5 evidence-backed anime, manga, film or literary pilgrimage candidates. After user selection, make an illustrated mobile companion guide with recognizable character fan art when requested. Native Codex ImageGen, offline HTML, publication optional.
---

# Seichi Junrei — 勝手に聖地巡礼

## Product promise: the characters travel with the user

This is a **story pilgrimage**, not a generic sightseeing brochure. When the user requests character fan art or approves a reference containing it, **preserve the characters and scene illustrations**. The hero, episode cards and destination chapters must visibly connect the selected work to the real trip. Do not silently replace the cast with scenery, silhouettes, props, abstract motifs or text alone. Original fan art may depict the requested fictional characters in new compositions; do not present it as an official screenshot or automatically rights-cleared material.

The user has explicitly said: **「なんのための聖地巡礼かわからないので、絵をなくさないで。」** Treat character retention as a product acceptance criterion. Refer to `references/editorial-and-art.md` and `references/mobile-quality.md`.

## Codex execution

- Target **Codex only**. Invoke `$seichi-junrei:seichi-junrei` for the plugin, or `$seichi-junrei` for a discovered direct skill. Do not invent commands.
- This file is `skills/seichi-junrei/SKILL.md`. The plugin root is two directories above it, containing `scripts/`, `assets/`, `references/`, `examples/` and `requirements.txt`. Resolve paths from the installed plugin, not from the user's current project by assumption.
- Check the session's actual calendar, search, local execution, browser and **native image-generation** capabilities. Installing this Skill grants none of them by itself.
- Native **ImageGen** creates assets, not a frozen screenshot of the final page. Existing user-approved character artwork can be reused. Do not endlessly generate more mockup pictures instead of implementing HTML.
- Test one representative image for each new guide before generating the rest. On failure, distinguish rejection, transient error and pending status; retain completed work and follow the bounded recovery procedure in `references/editorial-and-art.md`. "Fan art" is a provenance description, not a guarantee of tool acceptance.
- No extra image API: do not request an API key, call a billed image service or install a local diffusion model as a hidden fallback. If native image generation is unavailable, retain existing suitable images, report the gap and do not silently downgrade the requested art.
- Write assets, private drafts and output outside the plugin/cache. Run `scripts/render_guide.py <guide.json> --assets-root <trip-workspace> --out <guide.html>` for local image embedding. The default renderer includes the public sample’s mobile design and interactions. A timed itinerary needs a geographic map and linked stops beside the schedule; follow the map contract and online/offline limits in `references/mobile-production.md`. Read that reference before production; use this engine rather than recreating a simpler page. Reuse the controls while composing the visual design for the selected work. Read the structural-diversity criteria in `references/mobile-production.md`; changing colors and images alone is not a new design. Preserve any guide the user has excluded from redesign.

## Workflow

1. **Read the trip.** Use a connected Google Calendar if available, bounded to the relevant travel window. Read flights and lodging; preserve local timezones, distinguish confirmed reservations from suggestions, and infer no nonexistent leg. Otherwise use the user's itinerary/export. See `references/calendar-and-privacy.md`; `scripts/extract_calendar.py` produces an internal draft, not shareable calendar data.
2. **Find candidates.** Research 3–5 works with meaningful location connections. Separate a familiar work from a famous landmark: when discovery is the goal, look for the particular branch, street corner, background building or everyday place that a fan can recognize from a scene. Show the scene, physical clues, evidence strength, travel feasibility and why discovering it is rewarding. Rank using `scripts/rank_candidates.py` only as advice; its tourism/accessibility score does not establish a scene match or discovery value. Never invent locations to fill a shortlist. Read `references/research-and-ranking.md`; use the scene-level process there before promoting a place into a guide.
3. **Ask the user to choose. STOP HERE.** One main work and up to two side works; explicit delegation also counts. Do not silently choose the highest score. If the user already selected in this conversation, retain the choice instead of repeatedly asking. `scripts/make_ballot.py` is optional; ordinary chat selection is sufficient.
4. **Verify the chosen story.** Check exact adaptation, episode numbers/titles, manga edition/volume and film scenes. Keep a claim-level research ledger: story evidence, physical-location evidence and current access are separate claims. Inspect the actual images before using them as visual proof; captions, search snippets and generated art are insufficient. Preserve uncertainty from the originating report and downgrade conflicting matches. Read `references/scene-research.md` for discovery, visual comparison and a worked research case. Separate fictional setting, filming location, officially confirmed inspiration, thematic connection and speculation. Verify hours and transit constraints; last admission is not necessarily closing time. Keep source URLs and check dates. Do not imply a character visited a place just because an illustration depicts them there.
5. **Edit in travel order.** Interleave actual destination → recognizable character/scene fan art → scene recall → real-world observation. Include specific callbacks for fans and enough context for companions unfamiliar with the work. Keep spoilers expandable. Do not reduce the illustrations to a cover or a small decorative strip.
6. **Lock the design and cast.** Record approved colors, typography, image placement, characters, scene coverage and mobile proportions. Reuse the approved character illustrations where possible. Generate distinct missing art in new compositions. Label AI-generated fan art visibly on the cover and explain that it is unofficial, newly imagined art rather than documentary evidence. Inspect group portraits for cropped faces and overlapping text. Build a media manifest identifying the depicted characters, associated scene, provenance and non-official status. Never substitute the approved cast without user agreement.
7. **Implement a real mobile guide.** Use HTML/CSS for text and controls, embedded images for the artwork. Prioritize 360–430px phones, large single-column art, thumb-friendly bottom navigation, swipeable scene cards, accessible detail sheets, image zoom, chapter bookmarks and trip-day switching. Motion should support the story: restrained parallax, transitions and reveals, plus reduced-motion support. No dead controls, autoplay audio or a blocking intro. See `references/mobile-quality.md`.
8. **Verify the artifact.** Render in a real browser, inspect screenshots for character visibility and clipping, and exercise controls. Run structural/privacy checks and the reusable browser acceptance runner against the actual built HTML. Inspect its cover, destination and detail screenshots against the approved reference; test offline assets. Distinguish desktop browser emulation from physical-phone testing, and simulated storage from real persistence. A static mockup or merely valid HTML is not a finished site. Deliver the actual HTML and a screenshot taken from it.
9. **Protect the trip.** Remove PNRs, ticket numbers, seats, contact details, guest names, room numbers, private event descriptions and internal links from the companion file. Review sensitive data manually as well as with `scripts/lint_guide.py`. Keep personal itinerary snapshots out of public repository fixtures.
10. **Sharing is optional.** Offline HTML is a complete deliverable. Do not block delivery on Sites. Publish or update a live site only when explicitly requested; verify the URL before claiming deployment. Unlisted/noindex is not authentication. A public repo change, a generated file and a deployed website are three different outcomes.

## Non-negotiable gates

- **User choice:** current selection/delegation before guide generation; never inherit consent from a fixture.
- **Character-retention gate:** approved/requested cast appears prominently on the phone, with scene-specific art in the destination chapters. A scenery-only substitute fails unless explicitly requested.
- **Grounding:** no invented episode/location match; illustrative composites are not geographical evidence.
- **Design fidelity:** compare the actual 390/430px screenshots against the approved reference, including the cast and art placement.
- **Mobile behavior:** navigation, swipe, detail sheets, zoom, local-state fallback and reduced-motion work; images load; no horizontal page overflow.
- **Privacy:** no sensitive bookings in shared HTML or public samples.
- **Provenance:** fan art is labelled non-official; licensed photos and actual stills have their own provenance. Generated fan art is not automatically lawful for every publication or licensed under the code's MIT grant. Do not turn this caveat into a blanket removal of requested fictional characters.
- **Completion honesty:** generated artwork is not an implemented mobile site, and local HTML is not a published URL.

## Bundled helpers

- `scripts/extract_calendar.py`: minimal private travel draft.
- `scripts/rank_candidates.py`: advisory ranking; no selection.
- `scripts/make_ballot.py`: optional candidate-choice HTML.
- `scripts/render_guide.py`: the sample-quality mobile renderer, with `--assets-root`, explicit choice check and optional character manifest enforcement.
- `assets/mobile-guide/`: the reusable mobile design and runtime, bundled with the plugin.
- `tests/browser_check.py`: real-origin browser acceptance for a supplied trip and built artifact.
- `references/mobile-production.md`: art direction, content preparation, generation and verification.
- `examples/conan_singapore_guide.json` and `examples/monster_europe_guide.json`: selected character-led discovery samples, with source limits and differing destination/day counts.
- `examples/k_on_london_guide.json`: researched anime-film London example with a bright theme and generated fan art.
- `examples/oxford_alice_guide.json`: a different-work/destination/day-count production example.
- `scripts/lint_guide.py`: structural and heuristic checks; not a substitute for visual inspection or rights review.
- `references/guide-contract.md`: baseline input schema.
- `examples/egypt_candidates.json`, `examples/egypt_guide.json`: illustrative fixtures, not current real travel evidence.

Run from the plugin root:

```sh
python scripts/rank_candidates.py examples/egypt_candidates.json
python scripts/make_ballot.py examples/egypt_candidates.json --out /tmp/story-choices.html
python scripts/render_guide.py examples/egypt_guide.json --out /tmp/story-guide.html
python scripts/lint_guide.py /tmp/story-guide.html --guide examples/egypt_guide.json
```

For a new trip, provide actual local assets with `--assets-root`. The sample selection record is illustrative only; the live conversation must obtain the user's choice.
