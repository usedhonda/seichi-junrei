"""Run: python -m unittest discover -s tests -v"""
import copy
import json
import sys
import tempfile
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from render_guide import validate, render
from rank_candidates import rank
from extract_calendar import parse_export
from lint_guide import lint

class SkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'examples/egypt_guide.json').read_text(encoding='utf-8'))
        cls.candidates = json.loads((ROOT / 'examples/egypt_candidates.json').read_text(encoding='utf-8'))

    def test_selection_required(self):
        for d in [ {}, {"user_confirmed":False,"delegated":False,"primary_work_id":"jojo-3"} ]:
            spec = copy.deepcopy(self.data)
            spec['selection'] = d
            with self.assertRaises(ValueError): validate(spec)

    def test_explicit_delegation_allowed(self):
        spec = copy.deepcopy(self.data)
        spec['selection']={"primary_work_id":"jojo-3","delegated":True,"user_confirmed":False,"secondary_work_ids":[]}
        validate(spec)

    def test_candidate_ranking_no_selection(self):
        options=rank(self.candidates)
        self.assertEqual(3,len(options))
        self.assertEqual('jojo-3',options[0]['id'])
        self.assertTrue(all(0<=x['score']<=100 for x in options))

    def test_pnr_field_rejected(self):
        spec=copy.deepcopy(self.data)
        spec['meta']['booking_reference']='ABC123'
        with self.assertRaises(ValueError): validate(spec)

    def test_pnr_in_prose_rejected(self):
        spec=copy.deepcopy(self.data)
        spec['stages'][0]['location_note']='PNR: ABC123 is private'
        with self.assertRaises(ValueError): validate(spec)

    def test_unverified_connection_rejected(self):
        spec=copy.deepcopy(self.data)
        spec['stages'][0]['connections'][0]['source_url']=''
        with self.assertRaises(ValueError): validate(spec)

    def test_private_calendar_projection(self):
        fixture=json.loads((ROOT/'examples/calendar_sanitization_test.json').read_text(encoding='utf-8'))
        draft=parse_export(fixture)
        encoded=json.dumps(draft,ensure_ascii=False)
        for secret in ('SECRET12','test@example.com','23C','Alice','ABC123'):
            self.assertNotIn(secret,encoded)
        self.assertEqual(2,len(draft['events']))

    def test_unlabeled_name_in_title_not_exposed(self):
        fixture = {"items": [
            {"summary": "Flight MS80 for Alice Qwerty SECRET88 CAI → ASW",
             "start": {"dateTime": "2027-03-15T10:00:00+02:00"},
             "end": {"dateTime": "2027-03-15T11:00:00+02:00"}},
            {"summary": "Hotel reserved for Bob PrivateGuest",
             "start": {"date": "2027-03-15"}, "end": {"date": "2027-03-16"}},
        ]}
        draft = parse_export(fixture)
        encoded = json.dumps(draft, ensure_ascii=False)
        for secret in ("Alice", "Qwerty", "SECRET88", "PrivateGuest", "Bob"):
            self.assertNotIn(secret, encoded)
        self.assertEqual(2, len(draft["events"]))
        flight = next(e for e in draft["events"] if e["kind"] == "flight")
        self.assertEqual("MS80", flight["flight_code"])

    def test_numeric_date_is_not_flight_number(self):
        fixture = {"items": [{"summary": "Flight 2027 book a trip",
                              "start": "2027-03-15", "end": "2027-03-16"}]}
        flight = parse_export(fixture)["events"][0]
        self.assertNotIn("flight_code", flight)

    def test_japanese_flight_titles_are_not_dropped(self):
        for title in ("羽田空港からカイロへ", "明日のフライト", "エジプト航空 MS80便", "6E123便で移動"):
            with self.subTest(title=title):
                draft = parse_export([{"summary": title, "start": "2027-03-15"}])
                self.assertEqual(1, len(draft["events"]))
                self.assertEqual("flight", draft["events"][0]["kind"])
                self.assertNotIn(title, json.dumps(draft, ensure_ascii=False))

    def test_year_alone_is_not_a_flight(self):
        draft = parse_export([{"summary": "2027 年度計画", "start": "2027-03-15"}])
        self.assertEqual([], draft["events"])

    def test_renderer_media_and_lint(self):
        html=render(self.data,ROOT)
        errs,parser=lint(html,self.data)
        self.assertFalse(errs,errs)
        self.assertGreaterEqual(len(parser.images),10)
        self.assertTrue(all(x['src'].startswith('data:image/webp;base64,') for x in parser.images))

    def test_codex_generated_image_assets_root(self):
        # Mimic ImageGen-exported art in a writable, per-trip workspace.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for media in self.data["media_rights"]:
                original = ROOT / media["file"]
                target = root / media["file"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(original, target)
            spec_path = root / "guide.json"
            output = root / "finished.html"
            spec_path.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")
            cmd = [sys.executable, str(ROOT / "scripts/render_guide.py"),
                   str(spec_path), "--assets-root", str(root), "--out", str(output)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            html = output.read_text(encoding="utf-8")
            issues, parsed = lint(html, self.data)
            self.assertFalse(issues, issues)
            self.assertGreaterEqual(len(parsed.images), 10)
            self.assertTrue(all(x["src"].startswith("data:image/webp;base64,") for x in parsed.images))

    def test_remote_media_rejected(self):
        spec=copy.deepcopy(self.data)
        spec['meta']['hero_image']='https://images.example.org/x.jpg'
        with self.assertRaises(ValueError): render(spec,ROOT)

    def test_path_escape_rejected(self):
        spec=copy.deepcopy(self.data)
        spec['meta']['hero_image']='../../etc/passwd'
        with self.assertRaises(ValueError): render(spec,ROOT)

if __name__=='__main__':unittest.main()
