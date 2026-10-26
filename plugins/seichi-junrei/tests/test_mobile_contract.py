"""Protected contracts for the reusable mobile generator, not rendered wording."""
import copy
import json
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from render_guide import render, validate
from lint_guide import lint
from journey_fixture import independent_input

class GuideParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.in_data = False
        self.payload = ''
        self.art_ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'): self.ids.append(attrs['id'])
        if tag=='img' and attrs.get('data-art'):self.art_ids.add(attrs['data-art'])
        if tag == 'a' and attrs.get('href', '').startswith('#'): self.links.append(attrs['href'][1:])
        if tag == 'script' and attrs.get('id') == 'guide-data': self.in_data = True
    def handle_endtag(self, tag):
        if tag == 'script': self.in_data = False
    def handle_data(self, data):
        if self.in_data: self.payload += data

class MobileContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.alice = json.loads((ROOT/'examples/oxford_alice_guide.json').read_text())
        cls.egypt = json.loads((ROOT/'examples/egypt_guide.json').read_text())

    def test_different_work_destinations_and_days_are_rendered(self):
        source = render(self.alice, ROOT)
        parser = GuideParser(); parser.feed(source)
        state = json.loads(parser.payload)
        self.assertEqual(3, len(state['stages']))
        self.assertEqual(['riverbank', 'questions', 'mad-tea'], [ep['id'] for ep in state['episodes']])
        self.assertEqual(len(parser.ids), len(set(parser.ids)), 'IDs collide')
        self.assertTrue(set(parser.links).issubset(parser.ids), 'Broken internal link')
        self.assertEqual(4, len(state['missions']))
        self.assertEqual(4, len({m['id'] for m in state['missions']}))
        self.assertNotIn('STARDUST', source)
        self.assertNotIn('aswan', source.lower())
        self.assertFalse(lint(source, self.alice)[0])

    def test_theme_and_cover_credit_do_not_inject_markup(self):
        spec = copy.deepcopy(self.alice)
        spec['meta']['theme'] = '\"><script>alert(1)</script>'
        with self.assertRaisesRegex(ValueError, 'Unknown mobile theme'):
            render(spec, ROOT)
        spec['meta']['theme'] = 'pop-postcard'
        spec['meta']['art_label'] = '<script>unsafe-credit</script>'
        source = render(spec, ROOT)
        self.assertIn('data-theme="pop-postcard"', source)
        self.assertNotIn('<script>unsafe-credit</script>', source)
        self.assertIn('&lt;script&gt;unsafe-credit&lt;/script&gt;', source)

    def test_unselected_candidate_is_not_in_the_guide(self):
        spec = copy.deepcopy(self.alice)
        candidate = copy.deepcopy(spec['works'][0])
        candidate['id'] = 'unselected'
        candidate['title'] = 'UNSELECTED-CANDIDATE'
        candidate['episodes'][0]['title'] = 'UNAPPROVED-STORY'
        spec['works'].append(candidate)
        source = render(spec, ROOT)
        self.assertNotIn('UNSELECTED-CANDIDATE', source)
        self.assertNotIn('UNAPPROVED-STORY', source)

    def test_required_cast_cannot_be_silently_dropped(self):
        spec = copy.deepcopy(self.egypt)
        spec['media_rights'][0]['characters'] = []
        with self.assertRaisesRegex(ValueError, 'character artwork'): validate(spec)

    def test_duplicate_stage_day_and_mission_ids_rejected(self):
        for kind in ('stage', 'day', 'mission'):
            with self.subTest(kind=kind):
                spec = copy.deepcopy(self.alice)
                if kind == 'stage': spec['stages'][1]['id'] = spec['stages'][0]['id']
                elif kind == 'day': spec['itinerary'][1]['id'] = spec['itinerary'][0]['id']
                else: spec['stages'][0]['missions'].append(copy.deepcopy(spec['stages'][0]['missions'][0]))
                with self.assertRaises(ValueError): render(spec, ROOT)

    def test_embedded_data_cannot_end_script_element(self):
        spec = copy.deepcopy(self.alice)
        value = '</script><script>window.injected=true</script>'
        spec['meta']['title'] = value
        spec['works'][0]['episodes'][0]['tag'] = value
        source = render(spec, ROOT)
        self.assertNotIn(value, source)
        parser = GuideParser(); parser.feed(source)
        self.assertEqual(value, json.loads(parser.payload)['title'])

    def test_unsafe_editorial_link_rejected(self):
        spec = copy.deepcopy(self.alice)
        spec['stages'][0]['highlights'][0]['map_url'] = 'javascript:alert(1)'
        with self.assertRaises(ValueError): render(spec, ROOT)

    def test_integrated_day_preserves_one_reading_flow(self):
        spec=json.loads((ROOT/'examples/conan_singapore_guide.json').read_text())
        source=render(spec,ROOT)
        parser=GuideParser();parser.feed(source)
        self.assertEqual(source.count('class="view active"'),1)
        self.assertNotIn('class="view" id="story"',source)
        self.assertNotIn('class="view" id="route"',source)
        ids=['stage-'+s['id'] for s in spec['stages']]
        self.assertEqual([parser.ids.count(i) for i in ids],[1]*len(ids))
        self.assertEqual([parser.ids.index(i) for i in ids],sorted(parser.ids.index(i) for i in ids))
        self.assertIn('data-local-map="breakfast"',source)
        self.assertIn('travelmode=walking',source)
        del spec['itinerary'][0]['events'][4]['stage_id']
        with self.assertRaisesRegex(ValueError,'exactly once'):render(spec,ROOT)

    def test_multiday_input_owns_copy_order_and_transfer_days(self):
        spec=independent_input(ROOT)
        source=render(spec,ROOT);parser=GuideParser();parser.feed(source)
        state=json.loads(parser.payload)
        expected=['stage-'+e['stage_id'] for d in spec['itinerary'] for e in d['events'] if e.get('stage_id')]
        self.assertEqual(expected,[n['id'] for n in state['navigation'][2:]])
        self.assertTrue({e['art'] for e in state['episodes']}.issubset(parser.art_ids | set(state.get('supportArt',{}))))
        self.assertLess(parser.ids.index('day-arrival'),parser.ids.index('day-between'))
        self.assertLess(parser.ids.index('day-between'),parser.ids.index('day-after'))
        self.assertIn('次の場所への経路候補を開く',source)
        for copied in ['朝食から、探偵の一杯まで。','小五郎','SINGAPORE / ONE-DAY CASEBOOK']:
            self.assertNotIn(copied,source)
        self.assertFalse(lint(source,spec)[0])
        self.assertTrue(set(parser.links).issubset(parser.ids))
        self.assertEqual(len(parser.ids),len(set(parser.ids)))

    def test_all_requested_scenes_remain_visible_assets(self):
        for name in ['egypt_guide','monster_europe_guide']:
            spec=json.loads((ROOT/'examples'/(name+'.json')).read_text())
            source=render(spec,ROOT);parser=GuideParser();parser.feed(source)
            state=json.loads(parser.payload)
            self.assertTrue({s['art'] for s in state['scenes']}.issubset(parser.art_ids))
            if name=='monster_europe_guide':self.assertIn('class="scene-spoiler"',source)

    def test_supplemental_art_uses_external_trip_fields(self):
        spec=independent_input(ROOT)
        art=spec['stages'][0]['image']
        spec['itinerary'][0]['events'][0]['illustration']={'role':'sticker','image':art,'panel':'top-right','caption':'<unsafe-note>'}
        spec['meta']['closing_illustration']={'role':'scene','image':art,'caption':'A new trip ending'}
        source=render(spec,ROOT)
        self.assertIn('sticker-viewport top-right',source)
        self.assertIn('&lt;unsafe-note&gt;',source)
        self.assertNotIn('<unsafe-note>',source)
        self.assertIn('A new trip ending',source)
        spec['itinerary'][0]['events'][0]['illustration']['role']='unexpected'
        with self.assertRaisesRegex(ValueError,'illustration role'):render(spec,ROOT)

    def test_transparent_stamp_survives_offline_embedding(self):
        import base64,io
        from PIL import Image
        from render_guide import Media
        spec=json.loads((ROOT/'examples/conan_singapore_guide.json').read_text())
        stamp=next(e['illustration']['image'] for e in spec['itinerary'][0]['events'] if e.get('illustration'))
        payload=Media(spec,ROOT).embed(stamp).split(',',1)[1]
        with Image.open(io.BytesIO(base64.b64decode(payload))) as im:
            self.assertIn('A',im.getbands())
            self.assertEqual((0,255),im.getchannel('A').getextrema())

if __name__ == '__main__': unittest.main()
