# seichi-junrei plugin

One shared Agent Skill for Claude Code and Codex.

- Claude Code: /seichi-junrei:seichi-junrei from its available command/skill picker.
- Codex: $seichi-junrei:seichi-junrei or the installed /skills picker.
- Canonical Skill: skills/seichi-junrei/SKILL.md. All scripts, references, assets, examples and Python requirements are included in this plugin root.

Present 3–5 evidence-backed anime/manga/film candidates, stop for the user's choice, then produce a beautiful offline-friendly mobile HTML. Publishing is never required by default. External Calendar or image APIs depend on host connections.

Sample commands (from plugin root):

    python -m pip install -r requirements.txt
    python scripts/rank_candidates.py examples/egypt_candidates.json
    python scripts/render_guide.py examples/egypt_guide.json --out /tmp/guide.html
    python scripts/lint_guide.py /tmp/guide.html --guide examples/egypt_guide.json

See references/hosts.md and the repository README.
