"""Distribution validation in a standalone plugin folder."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class DistributionTests(unittest.TestCase):
    def test_manifests(self):
        a=json.loads((ROOT/'plugin.json').read_text())
        b=json.loads((ROOT/'.claude-plugin/plugin.json').read_text())
        c=json.loads((ROOT/'.codex-plugin/plugin.json').read_text())
        self.assertEqual({'seichi-junrei'},{a['name'],b['name'],c['name']})
        self.assertEqual({a['version']},{b['version'],c['version']})
        self.assertEqual('./skills/',c['skills'])
    def test_resources(self):
        for p in ['skills/seichi-junrei/SKILL.md','skills/seichi-junrei/agents/openai.yaml',
                  'commands/seichi-junrei.md','references/hosts.md','scripts/render_guide.py',
                  'scripts/make_ballot.py','assets/nile-original.webp','examples/egypt_guide.json',
                  'requirements.txt']:
            with self.subTest(path=p): self.assertTrue((ROOT/p).is_file(),p)
        skill=(ROOT/'skills/seichi-junrei/SKILL.md').read_text()
        self.assertIn('**STOP HERE.**',skill)
        self.assertIn('Codex plugin',skill)
    def test_command(self):
        cmd=(ROOT/'commands/seichi-junrei.md').read_text()
        self.assertIn('$'+'{CLAUDE_PLUGIN_ROOT}/skills/seichi-junrei/SKILL.md',cmd)
        self.assertIn('$ARGUMENTS',cmd)
    def test_media(self):
        guide=json.loads((ROOT/'examples/egypt_guide.json').read_text())
        for m in guide['media_rights']:
            path=(ROOT/m['file']).resolve()
            self.assertTrue(path.is_relative_to(ROOT))
            self.assertTrue(path.is_file(),path)

if __name__=='__main__':unittest.main()
