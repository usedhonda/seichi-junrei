"""A non-showcase input for renderer portability, not a real travel proposal."""
import copy
import json
from pathlib import Path


def independent_input(root):
    data=json.loads((Path(root)/'examples/oxford_alice_guide.json').read_text())
    # Different work, days, named IDs, point order and collection order from the
    # three showcases. Existing cleared public-domain images are reused for QA.
    first,last=copy.deepcopy(data['stages'][0]),copy.deepcopy(data['stages'][-1])
    data['stages']=[last,first]
    data['meta'].update({'id':'qa-independent-journey','title':'OXFORD / ANOTHER READING JOURNEY','layout':'casefile','reading_flow':'journey','character_art_required':False,'cover_title_lines':['ページの外へ。','物語の道へ。'],'cover_issue':'OXFORD / QA INPUT','cover_caption':'技術検証用の架空日程','journey_start':'検証用の旅を開く','dates':'QA ONLY / 3 DAYS','public_url':'','journey_intro':{'title':'別作品の入力で組み立てる。','body':['これは配布物の独立動作を確かめる検証データです。日程・座標は実旅行の案内ではありません。'],'facts':['3日','2地点','移動日あり'],'note':'Synthetic dates and coordinates for QA only.'}})
    data['route_map']={'stops':[
        {'id':'last-point','label':last['location'],'lat':51.75,'lon':-1.26,'stage_id':last['id'],'note':'QA座標。実際の入口を指しません。'},
        {'id':'first-point','label':first['location'],'lat':51.76,'lon':-1.25,'stage_id':first['id'],'note':'QA座標。実際の入口を指しません。'}]}
    data['itinerary']=[
        {'id':'arrival','label':'FIRST DAY','title':'最初の場所へ','map_stop_ids':['first-point'],'events':[{'time':'朝','title':first['name'],'stage_id':first['id'],'map_stop_id':'first-point','description':'検証用の観察時間。'}]},
        {'id':'between','label':'TRAVEL DAY','title':'次の場所へ','kind':'transfer','map_stop_ids':['first-point','last-point'],'events':[{'time':'終日','title':'移動の検証','kind':'transfer','from_stop_id':'first-point','to_stop_id':'last-point','travelmode':'walking','description':'実際の移動時間ではありません。'}]},
        {'id':'after','label':'LAST DAY','title':'次の場面へ','map_stop_ids':['last-point'],'events':[{'time':'午後','title':last['name'],'stage_id':last['id'],'map_stop_id':'last-point','description':'検証用の観察時間。'}]}]
    data['itinerary'][1]['events'][0]['illustration']=[{'role':'sticker','image':first['image'],'caption':'QA: another work supplies its own companion art.'},{'role':'scene','image':last['image'],'caption':'QA: the planned wide transition follows the margin figure.'}]
    data['meta']['journey_labels']={'scene':'ページに残る記憶。','onsite':'街で確かめる。'}
    data['meta']['closing_illustration']={'role':'scene','image':last['image'],'caption':'QA: a separate trip closing illustration.'}
    return data
