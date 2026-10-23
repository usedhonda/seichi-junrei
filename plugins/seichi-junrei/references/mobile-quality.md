# Mobile-first fan pilgrimage acceptance contract

## Scope

The target is an interactive **phone companion guide**, not a shrunken desktop poster. The approved gold/navy cinematic reference and character-rich story panels are the acceptance target. Wider screens may show a centered phone-width layout; do not dilute the phone design to make a generic desktop page.

## Visible product requirements

1. A cinematic character-led portrait hero. Faces, hats and other identifying features remain visible at 360, 390 and 430px. Headings are HTML text with sufficient contrast.
2. Distinct full-size character fan art in episode cards and inside destination chapters. Retain user-approved illustrations. Scenery and original character art alternate; all images do not collapse into a decorative header.
3. Separate navigable views or chapters for the cover, episodes, destinations and itinerary. Bottom navigation respects the phone's safe area and leaves enough end padding.
4. Horizontal scene/episode carousels use native scrolling and snap points. Visible next-card hints and operable dots/arrows supplement touch swiping.
5. Detail panels expose readable scene recaps and sources, with intentional spoiler controls. Close buttons, Escape and focus behavior are tested. Optional image zoom has a clear exit.
6. Chapter bookmarks and visit/check missions remain local to the reader. No transmission or synchronization is implied. Storage failures must not break the page.
7. Share/save actions work where supported, otherwise offer a file fallback. They must not invent a public URL or require deployment to count as finished.

## Motion

Use small, purposeful transitions: subtle parallax, card/page entrance, detail-sheet slides and checked-state feedback. Avoid flashing, autoplay audio, scroll hijacking, long blocking intros and continuous CPU-heavy effects. Respect prefers-reduced-motion and offer an explicit switch. Never make content dependent on completing an animation.

## Images and performance

Use adequate-resolution embedded WebP/PNG/JPEG. A 4–8 MB companion file is acceptable when justified by the approved artwork; this is a target range, not a hard limit. Do not meet an arbitrary small-file budget by deleting characters or reducing every chapter to an icon. Keep a count and provenance list of unique assets; repeated use can be deduplicated without removing visible art.

## Verification record

Capture the actual browser-rendered hero, at least one destination scene card, an open detail panel and the itinerary. Record viewport dimensions, image-loading checks, horizontal overflow, JavaScript errors and interaction results. Exercise navigation, swipe, zoom, spoiler, day tabs, bookmark, mission, reduced motion and file fallback. Test storage separately; simulated Storage API is not proof of persistent browser storage.

A phone-width Chromium test is not a physical iPhone/Safari test. Record unavailable checks as unavailable. A mockup produced by ImageGen is never a screenshot of the implemented site. Deliver the actual HTML and truthful test evidence.

## Character-retention regression

A revision fails when previously approved characters disappear, even if the revised scenery is attractive. Reviewers must inspect pixels, not just require a nonzero image count. Before removing or substituting a character-led asset, obtain the user's agreement or explain a specific actual constraint; do not apply a generic automatic character ban.
