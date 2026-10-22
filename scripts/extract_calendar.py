#!/usr/bin/env python3
"""Parse exported Google Calendar events into a minimal *private* travel draft.

Does not publish, show source descriptions, or decide user work selection.
"""
import argparse
import json
import re
import sys
from pathlib import Path

FLIGHT = re.compile(r"\b(?:flight|flight to|フライト|航空便|航空券|飛行機|空港|[A-Z0-9]{2}\s?\d{2,4})\b", re.I)
STAY = re.compile(r"hotel|resort|check[ -]?in|check[ -]?out|宿泊|滞在|ホテル|旅館", re.I)
IATA = re.compile(r"\b[A-Z]{3}\b")
# Never preserve original event titles in the exported summary. Event titles can
# contain unlabeled names, locations or booking identifiers that regexes miss.
FLIGHT_CODE = re.compile(r"(?<![A-Z0-9])([A-Z0-9]{2})[ -]?(\d{2,4})(?!\d)", re.I)
ROUTE = re.compile(r"\b([A-Z]{3})\s*(?:→|->|to)\s*([A-Z]{3})\b", re.I)


def moment(v):
    if isinstance(v, str):
        return v
    return (v or {}).get("dateTime") or (v or {}).get("date") or ""


def parse_export(obj):
    src = obj if isinstance(obj, list) else obj.get("items", obj.get("events", []))
    data = []
    for e in src:
        if e.get("status") == "cancelled":
            continue
        title = e.get("summary") or e.get("title") or ""
        if not title:
            continue
        # Search only event title, not description: descriptions may contain secrets.
        kind = "flight" if FLIGHT.search(title) else ("stay" if STAY.search(title) else None)
        if not kind:
            continue
        # Private helper output is intentionally minimal. The guide renderer does not accept raw events.
        rec = {"kind": kind,
               "start": moment(e.get("start")), "end": moment(e.get("end")),
               "needs_verification": True}
        if kind == "flight":
            found = FLIGHT_CODE.search(title)
            if found:
                rec["flight_code"] = (found.group(1) + found.group(2)).upper()
            route = ROUTE.search(title)
            if route:
                rec["route_codes_unverified"] = [route.group(1).upper(), route.group(2).upper()]
        data.append(rec)
    data.sort(key=lambda x: x["start"])
    return {"private_planning_only": True, "events": data,
            "notes": ["Titles/times are tentative until verified against actual reservations.",
                      "No free-form title, name, email, phone, seat, PNR or event description is exported.",
                      "Never attach this private draft to the shared guide."]}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("calendar_json", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    if a.out.resolve() == a.calendar_json.resolve():
        raise ValueError("Input and output paths must differ")
    result = parse_export(json.loads(a.calendar_json.read_text(encoding="utf-8")))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Private planning draft: {len(result['events'])} events -> {a.out}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError) as e:
        sys.exit(str(e))
