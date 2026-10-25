"""Codex packaging and instruction-regression checks; not visual image recognition."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class DistributionTests(unittest.TestCase):
    def test_codex_manifests(self):
        manifest = json.loads((ROOT / "plugin.json").read_text())
        cdx = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        self.assertEqual({"seichi-junrei"}, {manifest["name"], cdx["name"]})
        self.assertEqual(manifest["version"], cdx["version"])
        self.assertEqual("./skills/", cdx["skills"])
        self.assertFalse((ROOT / ".claude-plugin").exists())
        self.assertFalse((ROOT / "commands").exists())

    def test_resources_and_imagegen_guidance(self):
        required = [
            "skills/seichi-junrei/SKILL.md", "skills/seichi-junrei/agents/openai.yaml",
            "references/codex.md", "references/editorial-and-art.md",
            "references/mobile-quality.md", "scripts/render_guide.py",
            "scripts/make_ballot.py", "assets/nile-original.webp",
            "examples/egypt_guide.json", "examples/oxford_alice_guide.json", "requirements.txt",
            "assets/mobile-guide/guide.css", "assets/mobile-guide/guide.js", "references/mobile-production.md",
        ]
        for path in required:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file(), path)
        skill = (ROOT / "skills/seichi-junrei/SKILL.md").read_text()
        # Test the required stop wording, not a particular Markdown bold boundary.
        self.assertIn("STOP HERE.", skill)
        self.assertIn("current selection/delegation before guide generation", skill)
        self.assertIn("ImageGen", skill)
        self.assertIn("--assets-root", skill)
        self.assertNotIn("Claude Code", skill)
        host = (ROOT / "references/codex.md").read_text()
        self.assertIn("native image-generation", host)
        self.assertIn("No fabricated scene", host)

    def test_character_retention_instruction(self):
        skill = (ROOT / "skills/seichi-junrei/SKILL.md").read_text()
        art = (ROOT / "references/editorial-and-art.md").read_text()
        mobile = (ROOT / "references/mobile-quality.md").read_text()
        self.assertIn("Character-retention gate", skill)
        self.assertIn("Do not replace recognizable fictional characters", art)
        self.assertIn("360, 390 and 430px", mobile)
        self.assertIn("inspect pixels", mobile)
        self.assertIn("not proof of persistent browser storage", mobile)

    def test_media_inside_plugin(self):
        guide = json.loads((ROOT / "examples/egypt_guide.json").read_text())
        for media in guide["media_rights"]:
            p = (ROOT / media["file"]).resolve()
            self.assertTrue(p.is_relative_to(ROOT))
            self.assertTrue(p.is_file())

if __name__ == "__main__":
    unittest.main()
