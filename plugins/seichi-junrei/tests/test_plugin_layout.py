"""Codex-only plugin packaging and offline asset tests."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class DistributionTests(unittest.TestCase):
    def test_codex_manifests(self):
        manifest = json.loads((ROOT / "plugin.json").read_text())
        cdx = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        self.assertEqual({"seichi-junrei"}, {manifest["name"], cdx["name"]})
        self.assertEqual({"0.3.0"}, {manifest["version"], cdx["version"]})
        self.assertEqual("./skills/", cdx["skills"])
        self.assertFalse((ROOT / ".claude-plugin").exists())
        self.assertFalse((ROOT / "commands").exists())

    def test_resources_and_imagegen_guidance(self):
        required = [
            "skills/seichi-junrei/SKILL.md", "skills/seichi-junrei/agents/openai.yaml",
            "references/codex.md", "references/editorial-and-art.md",
            "scripts/render_guide.py", "scripts/make_ballot.py",
            "assets/nile-original.webp", "examples/egypt_guide.json", "requirements.txt",
        ]
        for path in required:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file(), path)
        skill = (ROOT / "skills/seichi-junrei/SKILL.md").read_text()
        self.assertIn("**STOP HERE.**", skill)
        self.assertIn("ImageGen", skill)
        self.assertIn("--assets-root", skill)
        self.assertNotIn("Claude Code", skill)
        host = (ROOT / "references/codex.md").read_text()
        self.assertIn("native image-generation", host)
        self.assertIn("No fabricated scene", host)

    def test_media_inside_plugin(self):
        guide = json.loads((ROOT / "examples/egypt_guide.json").read_text())
        for media in guide["media_rights"]:
            p = (ROOT / media["file"]).resolve()
            self.assertTrue(p.is_relative_to(ROOT))
            self.assertTrue(p.is_file())

if __name__ == "__main__":
    unittest.main()
