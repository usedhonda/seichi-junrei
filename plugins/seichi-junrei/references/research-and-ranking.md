# Evidence-backed candidate discovery

## Candidate ballot

Prepare 3–5 alternatives spanning relevant media; user picks **one primary** and optionally two secondary works. Do **not** generate the final HTML until selection. If no credible local connection exists, suggest the closest honest cultural theme rather than inventing a pilgrimage.

For each candidate: title, medium, why the destination matters, memorable scene/sequence, exact place(s), which kinds of place relations are substantiated, practical feasibility, a 1-line caveat, 1–3 URLs to primary/reliable sources, and estimated value. Some trips legitimately have only 1–2 evidenced candidates; explain the shortage instead of padding with invented choices.

## Connection grades (never conflate)

- **A — actual filming location / explicitly named real location:** authoritative location/official narrative evidence; name the distinction (fictional setting ≠ filming site).
- **B — creator/production confirmed inspiration:** primary creator statements or official commentary.
- **C — independently documented local connection:** recognized local record or historical tie, with provenance.
- **D — strongly thematic, but not a confirmed scene or model:** label "雰囲気・テーマ", not "聖地".
- **E — unverified fandom speculation:** normally exclude. If included as culture, clearly flag uncertainty.

Rank works by source support (max 35), trip accessibility (max 30), memorable story beats (max 20), appeal for companions (max 15). Add only grounded values; score is advisory; user preference overrides ranking. `scripts/rank_candidates.py` implements this transparently and may flag E or source-less items.

## Research after selection

- Get primary/official episode title, number and arc. Verify anime numbering vs seasonal indexing.
- Manga volumes change across tankōbon, bunko and digital color editions; ALWAYS state the edition. If page/chapter isn't reliably located, omit precision.
- Films: distinguish narrative place from film location, as some "Egypt" films shoot in other countries.
- Separate what characters did from what a tourist can see today. Don't assert a specific café was used unless verifiable.
- Verify hours, **last entry**, visitor access, closures, route times and modes via primary sources where possible. Date any time-sensitive information.
- Record source URL for every factual story beat, historical fact and location; keep short citation labels and a sources section.
- Use narrative beats, not long dialogue/scripts, anime stills or lifted manga panels. User-selected spoiler level controls whether the ending appears expanded.

## Sample distinctions

In the provided Egypt example, the JoJo anime official synopsis specifically mentions an Aswan café in episode 27 (https://jojo-animation.com/sc/contents/story/27.html). The Ministry's Abu Simbel page confirms the real Ramses II temple and two annual sunlight dates (https://egymonuments.gov.eg/en/archaeological-sites/abu-simbel/). Agatha Christie’s official site says the **1978 film Death on the Nile was shot in Egypt** (https://www.agathachristie.com/en/film-and-tv/death-on-the-nile-1978); a specific Abu Simbel location also appears in a separately documented filming-locations list (https://www.imdb.com/title/tt0077413/locations/). The 1999 film The Mummy is set in Egypt but IMDb lists significant shoots in Morocco and England (https://www.imdb.com/title/tt0120616/locations/); do not claim it was shot at Abu Simbel.
