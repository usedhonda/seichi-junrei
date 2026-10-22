# seichi-junrei — Codex plugin

An offline-first story pilgrimage Skill for **Codex**. The user shows a trip itinerary; Codex researches 3–5 location-grounded anime, manga, film or book candidates; the **user chooses a work**; Codex creates an engaging, scene-led mobile HTML guide with a rights-conscious image plan.

- Plugin entrypoint: `$seichi-junrei:seichi-junrei` (or the supported `/skills` menu)
- Canonical Skill: `skills/seichi-junrei/SKILL.md`
- Codex runtime notes: `references/codex.md`
- Native ImageGen when actually available; **no new external image API**, no hidden local model installation
- Output: single self-contained HTML, **sharing/hosting optional**

## Local sample

From this plugin directory (Python 3.11+):

```sh
python -m pip install -r requirements.txt
python scripts/rank_candidates.py examples/egypt_candidates.json
python scripts/make_ballot.py examples/egypt_candidates.json --out /tmp/choices.html
python scripts/render_guide.py examples/egypt_guide.json --out /tmp/guide.html
python scripts/lint_guide.py /tmp/guide.html --guide examples/egypt_guide.json
```

For a **real trip**, use the Codex-generated local media directory:

```sh
python scripts/render_guide.py /path/to/trip/guide.json --assets-root /path/to/trip --out /path/to/trip/guide.html
```

Images referenced inside `guide.json` should have paths such as `assets/scene-01.png` and a matching `media_rights` entry.

See the [repository README](https://github.com/usedhonda/seichi-junrei#readme).
