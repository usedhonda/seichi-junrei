# Claude Code / Codex host compatibility

The single canonical workflow is at skills/seichi-junrei/SKILL.md. All script, image and reference resources are packaged inside this plugin; no file may rely on the repository outside the plugin.

## Claude Code
- Repository marketplace: .claude-plugin/marketplace.json, pointing at ./plugins/seichi-junrei.
- The plugin includes .claude-plugin/plugin.json, a skill and a thin commands/seichi-junrei.md wrapper.
- Install in Claude Code chat: /plugin marketplace add usedhonda/seichi-junrei, then /plugin install seichi-junrei@seichi-junrei.
- Invoke /seichi-junrei:seichi-junrei where shown in the slash picker; actual discovered commands/aliases take precedence.
- For local development, a supported Claude Code CLI can use claude --plugin-dir ./plugins/seichi-junrei.

## Codex
- Repository marketplace: .agents/plugins/marketplace.json, with source.path ./plugins/seichi-junrei.
- Portable root plugin.json and .codex-plugin/plugin.json compatibility overlay are both present.
- Where supported, install in the terminal: codex plugin marketplace add usedhonda/seichi-junrei; codex plugin add seichi-junrei@seichi-junrei.
- Invoke $seichi-junrei:seichi-junrei or select the skill from /skills / app UI. Do not invent Codex /seichi-junrei.
- Direct clone to ~/.agents/skills/seichi-junrei may use the root SKILL.md wrapper and $seichi-junrei. Avoid duplicate installations.

## Safety and capability boundary
- Installation alone does not grant Google Calendar, web search, image generation, local execution or hosting. Check the real host's available tools and permissions.
- Python needs Pillow installed from the plugin's requirements.txt for embedded images.
- Put generated guides and private calendar drafts in an authorized workspace, not a plugin cache.
- User-selected (or expressly delegated) primary story required before rendering. Publishing is optional. Noindex/unlisted is not access control.
- Tests of package structure do not verify that an external desktop/CLI host has discovered or loaded the plugin.
