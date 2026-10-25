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

Follow `mobile-quality.md`: actual portrait layout, strong art and legible live text, 44px controls, safe-area bottom navigation, horizontal card swipes, detail sheets, image zoom and motion controls. Preserve the approved palette and hierarchy. Prefer larger image files over visibly broken or overly compressed art; embed images for reliable offline display.

Judge the implementation from real browser screenshots at 390 and 430px, not from an image-generator mockup. Inspect faces, scene placement, tap targets and overflowing captions. State physical-device and browser-engine coverage honestly.
