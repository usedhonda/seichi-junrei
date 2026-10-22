# Narrative, art direction and reference matching

## Editorial design

A fan wants evocative story recall. A first-time viewer wants history, atmosphere and why a scene matters. Structure: cinematic hero + premise → short episode/scene gallery → days in **actual travel order** → alternate layer (myth / filming story / history) → checkable missions, sources and share-safe itinerary.

Use real, precise scenes, but without dumping a plot summary. Thread narrative into destination cards: "episode X / what happened / what you see / why it resonates". Use optional spoiler panels for twists. Each stop should contain at least one story beat and one real-world observation. Make a distinction between an official location and an imaginative thematic comparison.

## Visual system and design lock

- Produce a single first-pass visual mockup if needed; if user provides a specific visual, use it as an acceptance reference rather than a loose aesthetic reference. Record palette, typographic hierarchy, shape treatment, image placement, layout order and proportions.
- Compare actual mobile screenshot at 390px to reference; inspect the fold, character/landmark cropping, legibility and scene-art insertion. Compare desktop/tablet too. Fix until materially matched; do not declare equivalence based on successful HTML compilation.
- Mobile-first *real* page: responsive grid, persistent accessible navigation, large tap targets (44px), scannable cards, readable 15–17px body, high text contrast, text selectable, progressive disclosure, no horizontal overflow.
- Story scene illustrations should be **interleaved** with real locations; not relegated to an episode strip while destination sections are text-only.
- No dead controls. Interactive cards need real state and no external network dependency. On offline single-file outputs, local browser storage may behave differently by origin—provide graceful fallback.

## Codex ImageGen art workflow

The default production mode is **Codex-native image generation** if the current session exposes such a tool. No separately billed Google/Gemini/OpenAI API key or locally installed diffusion model is part of this Skill. Create meaningful **separate** cover and story-panel images and weave them through the travel story, rather than using one reused background.

The agent must first verify the user's main work selection, research episodes/scenes and establish the location sequence. Then write an asset storyboard (subject, aspect ratio, usage location, scene source, safety/rights notes). Generate art, compare against the approved design reference, and export actual image files into a writable trip workspace. Build a visual-asset manifest; all image references in guide JSON are relative to the chosen `--assets-root`. If native ImageGen is not exposed, report the gap; **do not silently replace the illustrated result with SVG drawings or external API requests**.

Typography, navigation, card interactions, spoiler controls and layout are HTML/CSS. AI illustration is **supporting media**, not the final website itself.

## Images and permissions

1. Use user-owned, appropriately licensed real-world photographs or permission-cleared images. Keep a rights manifest with source, author, license URL, reuse constraints, attribution when needed.
2. Original images may depict *ideas* (desert, obelisk, sword silhouette, a book of prophecies) without tracing or replicating recognizably protected anime frame composition, outfits, character likeness, title treatment or franchise marks. The style of a franchise itself is not a blanket authorization. Local/private companion sharing may still raise copyright issues.
3. A generated image is not automatically non-infringing. Don't say "parody" or "fan art" automatically removes infringement risk. If the user supplies properly licensed stills, handle under that permission only.
4. Distinguish "創作イラスト" from photographic documentation. Do not mislead about geographical composites or where scenes occurred.
5. Embed image bytes as data URIs for the offline HTML, compress/resample as needed, and alt-text every meaningful photo. Never link to an unlicensed media asset solely for convenience.

## Publishing

HTML is the finished default. An HTML file sent directly to companions is fine; link-based deployment is **optional**. For any Site-publication, run privacy and rights audits, receive an explicit go-ahead, and verify the live link. A public URL with noindex is not access control.
