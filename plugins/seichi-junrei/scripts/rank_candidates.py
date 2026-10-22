#!/usr/bin/env python3
"""Deterministic evidence-aware ordering. Never selects a candidate for the user."""
import argparse
import json
import sys
from pathlib import Path

WEIGHTS = {"evidence": 35, "access": 30, "story": 20, "companion": 15}
GRADES = {"A", "B", "C", "D", "E"}


def rank(data):
    works = data.get("candidates", [])
    if not (2 <= len(works) <= 5):
        raise ValueError("Expected 3–5 candidates, or explain why only two credible candidates exist")
    out = []
    ids = set()
    for item in works:
        ident = item.get("id")
        if not ident or ident in ids:
            raise ValueError("Candidate IDs must be nonempty and unique")
        ids.add(ident)
        grade = item.get("connection_grade", "E")
        if grade not in GRADES:
            raise ValueError("Invalid connection grade: " + str(grade))
        scores = item.get("score_components", {})
        score = 0
        for k, bound in WEIGHTS.items():
            number = scores.get(k, 0)
            if not isinstance(number, (int, float)) or not 0 <= number <= bound:
                raise ValueError(f"{ident}: {k} must be within 0–{bound}")
            score += number
        warnings = []
        if grade == "E":
            warnings.append("未検証の関係: 通常は候補から除く")
        if not item.get("evidence_urls"):
            warnings.append("根拠URLなし: 候補として提示前に要調査")
        if grade in ("A", "B") and scores.get("evidence", 0) < 20:
            warnings.append("高確度ラベルに対して根拠の質が不足")
        if item.get("itinerary_feasible") is False:
            warnings.append("予定内で現地訪問が難しい")
        out.append({**item, "score": round(score, 1), "warnings": warnings})
    return sorted(out, key=lambda x: x["score"], reverse=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("json_file", type=Path)
    p.add_argument("--out", type=Path)
    args = p.parse_args()
    ranked = rank(json.loads(args.json_file.read_text(encoding="utf-8")))
    result = {"recommended_order_only": True, "selection_required": True, "candidates": ranked}
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(encoded, encoding="utf-8")
    else:
        print(encoded)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError) as e:
        sys.exit(str(e))
