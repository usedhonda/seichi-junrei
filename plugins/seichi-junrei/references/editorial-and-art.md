# Narrative, character art and reference fidelity

## The actual purpose

Fans should recognize **their characters and remembered scenes** in the places they visit. A first-time companion should understand why the moment matters. A generic location image plus a franchise name does not deliver this experience.

When the user asks for character fan art or approves a character-rich reference, keep it. Do not replace recognizable fictional characters with anonymous silhouettes, a book, water, scenery or a purely typographic treatment without agreement. Fan art can be newly composed artwork featuring the requested fictional characters. It need not be an official screenshot or copied manga panel.

## Character-retention contract

Before revising a guide, list the approved/requested characters, existing image files and where they must appear. Retain working art across revisions. For the JoJo example, the approved cast/scene palette includes Jotaro, Iggy, N'Doul, Oingo and Boingo, the disguised-Jotaro cigarette gag, and Polnareff/Anubis-related battle imagery.

At minimum, when this is the requested treatment:

- Hero: a recognizably character-led composition, readable on a narrow portrait screen; do not crop the protagonist off the edge.
- Episode gallery: character/scene imagery for the corresponding episodes, not one generic background reused for every card.
- Destination chapters: large scene-specific fan-art panels interleaved with landscape imagery and actual sightseeing information.
- Optional enlargement: the user can inspect the illustration without removing the prose from the page.

A phone screenshot that loses the cast fails even if the images exist somewhere in the HTML. Asset counts alone do not prove visual fidelity.

## Editing scenes with places

Use verified episode/adaptation labels and travel order. Keep fictional events, real history, thematic associations and creative visual composites distinct. A character shown before Abu Simbel in fan art is not evidence of an in-story battle there.

For the Egypt example: episodes 25–26 concern Iggy and N'Doul in the desert; episode 27 is the Aswan Oingo/Boingo story; episodes 28–29 lead into the Anubis battles around Kom Ombo. Do not relabel these to match an attractive mockup. An illustrated travel guide is not permission to invent episode summaries. Cite the official episode pages and monument sources; label uncertain details or omit them.

Give non-fans context; give fans specific emotional beats. Place story illustrations **throughout** the destination text, not only in the introduction. Use spoiler reveals for twists. Write new commentary, not long copied dialogue or lyrics.

## Art production

Use native Codex ImageGen when actually available. Reuse suitable approved art before generating more. Generate separate missing assets with intentional subjects, aspect ratios, focal points and visual continuity. Text, navigation and layout are real HTML/CSS, never baked into a full-page generated image.

Start each new guide with one representative illustration, inspect it for cast, style and framing, then create the remaining assets. Preserve the originals and production notes in the trip workspace. An illustration can be recognizably non-photorealistic fan art without copying a frame; that label or style does not guarantee the image tool will accept it. Agree whether the intended treatment concerns fictional characters, actor likenesses or supplied reference art rather than treating them as interchangeable.

When generation fails, distinguish explicit rejection from a temporary service error or a still-pending request. Retain completed images, the research and editable guide data, and record the failed asset and the tool's stated reason without inventing an explanation. Check an existing operation's status before duplicating an uncertain request. A confirmed transient failure may receive one bounded retry; an explicit rejection must not trigger a loop of cosmetic rewording or a different service chosen to evade it. If the stated reason permits a materially compliant creative change, explain that change; an unknown reason is not proof that adding "fan art" will solve it. Offer a different user-selected work or suitable supplied/licensed art when needed. A partial guide remains partial; do not silently remove the cast or publish it as finished.

No separate image API keys, billed fallback service or local model installation. If generation is unavailable, preserve existing art and disclose the limitation; do not silently replace the promised experience with SVG decorations or photos alone.

Use clear provenance records: creator/method, supplied or generated origin, depicted characters/scene, source for actual documentary images, license terms where applicable, and non-official status. A generation/provenance field is not a legal clearance certificate. Retain the distinction between 'generated fan art' and 'licensed photograph'.

## Rights and labels

Do not represent newly generated fan art as official anime frames, manga scans, authorized merchandise or documentary photography. Do not scrape and republish original frames or panels merely because fan art was requested. Suitable supplied/permission-cleared images can be used within their conditions.

Fan art and private companion sharing do not guarantee every distribution is permitted. Record limitations and review before optional public distribution. The code's MIT license does not automatically cover franchise imagery. These caveats **do not require deleting the requested fictional characters from original fan art**.

## Mobile presentation

### Whole-guide visual storyboard (before generation)

During the overall structure pass, write an art plan in the trip workspace alongside the reading outline. Count unique asset files, distinct poses/illustrations and actual page placements separately: a four-pose sheet is one file, four drawings and potentially four placements. For each placement record the reading position, purpose/emotional beat, subjects and action, visual treatment, camera height/distance and foreground arrangement, aspect ratio/phone crop, and whether it reuses approved art or needs generation. Also note what remains text or map only. Plan the ending with the same care as the opening.

Choose when to use deformed art based on the reading experience: a small consistent companion may lighten an operational note, while an occasional whole-cast stylized scene can create a playful break or closing release. Main scene illustrations still carry place/story context. Decide that balance before commissioning the set, and retain the chosen style anchors across all poses. Neither a fixed image count nor a universal percentage of chibi art fits every work.

Read through the planned page sequence as a storyboard: where the reader slows, looks closely, moves, rests and finishes. Compare consecutive shots and the whole set for repeated framing and missing visual beats. Translate each planned shot into an explicit generation prompt; inspect completed art against the plan and actual phone crops. Revise the plan coherently if a scene fails, rather than adding unrelated pictures late. The worked `examples/conan_singapore_art_plan.md` shows counts, treatments and placement choices; it is an example, not the default blueprint for every trip.

### Selectable illustration roles and reading rhythm

Plan composition independently of rendering style. Before generating a set, note each image's action, camera height, distance, subject scale and foreground/background arrangement. An anime scene, watercolor scene and paper collage can still repeat the same seated waist-up figures behind a table. Changing the medium, cast or expressions alone does not vary the composition.

Use story-appropriate differences: an establishing view with small figures, an oblique overhead view of movement, an over-the-shoulder observation, an expressive close-up or a low-angle full-body scene. Specify the intended action and camera geometry in each prompt. These are options, not a mandatory rotation; a meal may need a seated scene, while a closing memory need not become another meal. Inspect all main images together in reading order, then the actual phone crops. If several share the same silhouette and tabletop/counter arrangement, recompose the redundant scenes rather than merely recoloring them. Preserve recognizable cast and distinguish newly imagined action from a verified scene match.

For each generation prompt, include a concrete action and camera instruction (for example, "oblique overhead wide view; both characters walking through a stall aisle, full bodies visible"). Include relevant exclusions when correcting repetition (for example, "no seated figures behind a foreground table"). Do not rely on vague words such as "dynamic", "different" or "cinematic" to change the shot. A deliberate quiet moment is useful; accidental repetition across the guide is not. Judge variety across the set rather than forcing every image into an exaggerated action pose.

Use a small set of intentional roles rather than a single treatment for every image:

- Scene art: a large composition for a story/place beat; retain the approved cast and scene context.
- Recurring stamp: a consistent, deliberately simplified character with transparent background, bold outline and expressive gestures, appearing beside occasional notes, breaks or transitions. Keep the same proportions, face and palette across poses. This can repeat as a travel companion; do not repeat a full scene solely as filler.
- Stylized ensemble: an occasional whole scene in which all characters share the chosen chibi, comic or cut-paper treatment. It can provide a change of pace or closing memory without changing every image to that style.

For a requested comparison, keep subject/action constant so the user can judge style. Confirm whether they want scene illustrations or small messaging-style stamps: merely shortening anime proportions while retaining a detailed backdrop does not produce a stamp. Once the user accepts a direction, continue into the actual guide; candidate generation alone is not the promised revision.

Plan placements from start to finish before generating: opening, visits, afternoon/transfers, final stop and closing. Inspect the last third of the actual phone page as carefully as the cover. Long stretches of prose after an image-rich opening need an editorial decision; a tiny stamp does not replace a missing requested scene illustration. Vary placement naturally, avoid stamping every chapter identically, and keep faces away from live labels and controls. Do not make cheerful comic reactions mandatory for a serious thriller.

The journey renderer supports `events[].illustration` and `meta.closing_illustration` as `{role: "sticker" | "scene", image: "local/file.png", caption: "..."}`. Register each asset in `media_rights`; use truthful character/provenance metadata and captions that identify imagined scenes. Stickers retain alpha transparency and sit alongside live text; scene art uses the existing large image and zoom control. These fields add visual rhythm to the itinerary without inventing factual stops or separate navigation screens.

For a comprehensive revision, revisit the entire text/map/image sequence before selecting replacements. A new render of the old input or stamps appended to an unchanged composition does not by itself implement a new editorial plan. Keep the work's approved strengths while checking the opening, every visit/transfer, late-page rhythm and ending together. The JoJo storyboard (`examples/egypt_art_plan.md`) uses an expressive animal companion and a playful ensemble ending; the MONSTER storyboard (`examples/monster_europe_art_plan.md`) uses quiet margin figures and a restrained epilogue. They illustrate different tonal decisions, not a single chibi recipe. Update chapter copy and labels to match that voice, and keep geographical controls in the travel flow.

Follow `mobile-quality.md`: actual portrait layout, strong art and legible live text, 44px controls, safe-area bottom navigation, horizontal card swipes, detail sheets, image zoom and motion controls. Preserve the approved palette and hierarchy. Prefer larger image files over visibly broken or overly compressed art; embed images for reliable offline display.

Judge the implementation from real browser screenshots at 390 and 430px, not from an image-generator mockup. Inspect faces, scene placement, tap targets and overflowing captions. State physical-device and browser-engine coverage honestly.
