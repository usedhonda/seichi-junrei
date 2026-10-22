# Calendar reading, timing and privacy

## Read a bounded range

- Search visible Google Calendars with an explicit trip date span. Do not scan all calendars unbounded. For "next trip", search upcoming travel events in a bounded window (e.g. 90 days), then refine to the relevant stay. Event attendees and body text should not appear in the public guide.
- Read flight, lodging and destination events; treat calendar events as *planned* until confirmed. Do not assume flights are on time or establishments open. Respect local timezone/DST of each location. Airline schedules give local departures/arrivals; use offsets if present.
- Prefer user's expressed travel order. An overnight stay can change the day label but not the scene chronology.
- Identify flight code and IATA airports only when supported by the event; parse cautiously. Long free windows between flights and hotel events are not automatically usable: arrival transfer, immigration, check-in, sleep and transport matter. Mark ambiguous windows "要確認".
- Do not leak private work meetings from the same calendar. Extract only elements needed for travel feasibility, and show only public trip elements.

## Privacy by default

Keep privately in runtime: full original calendar events, PNRs, ticket numbers, seat assignments, confirmation codes, email addresses, phone numbers, passenger names, exact hotel room/host address, internal event descriptions, precise tracking URLs, shared calendar IDs and organizer emails.

Allowed by default in *shared* guide: public destination names, travel day, city/region, notable accessible places, approximate activity windows, public map links. Exact flight code, airport times or hotel name only if relevant to the group and expressly suitable for sharing. If the user wants a detailed travel schedule, offer both **private** and **share-safe** versions.

The static HTML must not contain source calendar JSON in comments, script tags, hidden elements or base64 payloads. "Noindex" and guess-resistant URLs cannot protect leaked secrets.

## Export helper

`scripts/extract_calendar.py` accepts Google Calendar-style `items` or `events`, summarizes flight and stay events and optional landmarks, writes *private* JSON only, and does not include freeform description text. This is a deterministic helper, not a substitute for interpreting ambiguous bookings or getting live data.
