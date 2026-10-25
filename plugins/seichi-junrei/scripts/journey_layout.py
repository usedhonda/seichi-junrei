"""Integrated one-day casebook: itinerary events join place and story content.

The chronology is the document structure. No separate story/place/timetable views.
"""
from urllib.parse import urlencode


def compose(data, stages, episodes, scenes, missions, image, feature,
            paragraphs, link, mission_group, H, types, map_html, days):
    if len(days) != 1:
        raise ValueError('The integrated casebook currently supports one complete day')
    day = days[0]
    by_stage = {s['spec']['id']: s for s in stages}
    visits = [e['stage_id'] for e in day['events'] if e.get('stage_id')]
    if len(visits) != len(set(visits)) or set(visits) != set(by_stage):
        raise ValueError('Every integrated place must be introduced exactly once in the day')
    points = {s['id']: s for s in data['route_map']['stops']}
    highlights = {h['id']: h for s in data['stages'] for h in s['highlights'] if isinstance(h,dict) and h.get('id')}
    primary = next(w for w in data['works'] if w['id'] == data['selection']['primary_work_id'])
    def directions(a, b, mode=''):
        q={'api':1,'origin':str(a['lat'])+','+str(a['lon']),'destination':str(b['lat'])+','+str(b['lon'])}
        if mode in ['walking','transit','driving']:q['travelmode']=mode
        return 'https://www.google.com/maps/dir/?'+urlencode(q)
    def local_map(point):
        # This stays inside the current stop; no jump back to the overview.
        return '<details class="local-map-details"><summary>この場所の地図・入口を見る</summary><div class="local-stop-map" data-local-map="'+H(point['id'])+'" role="region" aria-label="'+H(point['label'])+'の地図"></div><p>'+H(point.get('note',''))+'</p>'+link('https://www.google.com/maps/search/?'+urlencode({'api':1,'query':str(point['lat'])+','+str(point['lon'])}),'地図アプリで開く')+'</details>'
    cover = f'''<header class="case-cover"><div class="issue-line"><span>SINGAPORE / ONE-DAY CASEBOOK</span><span>03 SCENES</span></div><h1><small>{H(primary['title'])}</small>街に残った、<br><em>手がかり。</em></h1><p class="cover-deck">{H(data['meta']['subtitle'])}</p><figure class="case-portrait">{image(data['meta']['hero_image'],'hero-art',True)}<figcaption>一日の旅に、三つの場面を。</figcaption></figure><p class="editorial-credit">AI FAN ART · 非公式 / 1日モデル</p><a class="editorial-start" href="#day-1">今日の旅をはじめる <span>↓</span></a></header>'''
    intro = '<section class="journey-orientation" id="day-1"><span class="kicker">ONE DAY / SINGAPORE</span><h2>朝食から、探偵の一杯まで。</h2><p>『紺青の拳』の何気ない場面を、街の中で探す一日。朝食の支店から二人のランチへ。午後はラッフルズへ足を延ばします。</p><div class="journey-facts"><span>09:00—16:30</span><span>3つの舞台候補＋任意の壁画</span><span>徒歩・MRT等</span></div><p class="journey-model-note">個人予約を含まないモデルです。時刻・移動時間は編集上の概算。各場所の案内と当日の交通を確認してください。</p></section>'
    # The overview is part of the day, followed immediately by its stops.
    overview = '<section id="route" class="journey-overview">'+map_html+'</section>'
    body = ''
    previous = None
    episode_index = {e['id']:e for e in episodes}
    for i,event in enumerate(day['events']):
        point = points.get(event.get('map_stop_id'))
        time = '<span class="journey-time">'+H(event.get('time',''))+'</span>'
        if event.get('stage_id'):
            st = by_stage[event['stage_id']];spec=st['spec']
            if not point or point.get('stage_id') != spec['id']:
                raise ValueError('Integrated visit needs a matching geographic stop')
            scene = next(s for s in scenes if s['stage']==st['id'])
            ep = episode_index.get(scene['episode'])
            number = list(points).index(point['id'])+1
            body += f'<article class="journey-visit" id="{st["id"]}" aria-labelledby="title-{st["id"]}"><header class="journey-visit-head" id="stop-{H(point["id"])}"><div class="visit-stamp">{time}<span>STOP {number:02}</span></div><h2 id="title-{st["id"]}">{H(spec["name"])}</h2><p class="visit-place">{H(spec["location"])}</p><p class="visit-hook">{H(spec.get("hook",""))}</p></header>'
            body += feature(spec['image'],'非公式ファンアート · 現地の記録写真ではありません')
            body += '<div class="journey-visit-body"><div class="scene-memory"><span class="kicker">あの場面を、ここで。</span><h3>'+H(scene['name'])+'</h3><p>'+H(ep.get('body',[scene['text']])[0] if ep else scene['text'])+'</p><div class="scene-actions"><button data-episode="'+H(scene['episode'])+'">物語を振り返る ↗</button><button data-scene="'+H(scene['id'])+'">挿絵と場面を読む ↗</button></div></div>'
            body += '<section class="onsite-clues"><h3>現地で探す、手がかり。</h3>'
            for h in spec['highlights']:
                item = h if isinstance(h,dict) else {'title':h}
                if item.get('kind')=='related':continue
                body += '<div class="onsite-clue"><h4>'+H(item['title'])+'</h4><p>'+H(item.get('description',''))+'</p>'+link(item.get('source_url'),'現地情報の出典')+'</div>'
            body += '</section>'+local_map(point)
            body += '<div class="visit-practical"><span>この場所で過ごす時間</span><p>'+H(event.get('description',''))+'</p><p>'+H(spec.get('practical',''))+'</p></div>'
            body += '<details class="visit-research"><summary>場所と作品の照合メモ</summary>'+paragraphs(spec.get('paragraphs',[]))
            for rel in spec.get('connections',[]):
                body += '<strong>'+H(types[rel['type']])+'</strong><p>'+H(rel['description'])+'</p>'+link(rel['source_url'],'関係の根拠')
            body += '</details><details class="visit-checklist"><summary>ここで見つけたものを記録</summary>'+mission_group(st['id'],st['label'],[m for m in missions if m['stage']==st['id']])+'</details>'
            body += '<div class="chapter-tools"><button data-bookmark="'+st['id']+'" aria-pressed="false">◇ この場所を保存</button><button data-action="share">仲間に渡す ↗</button></div></div></article>'
        elif event.get('related_highlight_id'):
            h=highlights.get(event['related_highlight_id'])
            if not h or not point:raise ValueError('Optional visit needs an existing highlight and geographic stop')
            body += '<aside class="journey-detour" id="stop-'+H(point['id'])+'"><div class="visit-stamp">'+time+'<span>任意の寄り道</span></div><h3>'+H(h['title'])+'</h3><p>'+H(h.get('description',''))+'</p><p>'+H(event.get('description',''))+'</p>'+local_map(point)+link(h.get('source_url'),'壁画の案内')+'</aside>'
        elif event.get('kind')=='transfer':
            nxt=next((points.get(e.get('map_stop_id')) for e in day['events'][i+1:] if e.get('map_stop_id')),None)
            body += '<aside class="journey-transfer"><div class="transfer-line"></div>'+time+'<h3>'+H(event.get('title',''))+'</h3><p>'+H(event.get('description',''))+'</p>'
            if previous and nxt:body += link(directions(previous,nxt,event.get('travelmode','')),'次の場所への経路を開く','directions-link')
            body += '</aside>'
        else:
            body += '<aside class="journey-pause">'+time+'<div><h3>'+H(event.get('title',''))+'</h3><p>'+H(event.get('description',''))+'</p></div></aside>'
        if point:previous=point
    footer = '<section class="journey-finish"><span class="kicker">THE END OF TODAY\'S CASE</span><h2>今日の街が、<br>物語の記憶になる。</h2><p>'+H(data['meta'].get('closing',''))+'</p><details open><summary>一日の記録を見る</summary>'+mission_group('all','旅全体',missions)+'</details><div class="menu-list"><button data-action="save">画像込みでこの旅を保存 ↓</button><button data-action="share">旅仲間に渡す ↗</button><button data-open="sources">出典・挿絵の制作記録</button><button data-open="howto">使い方</button><button data-action="motion" aria-pressed="true">ON</button></div></section>'
    home = '<section class="view active" id="home">'+cover+intro+overview+'<section class="journey-day" aria-label="一日の旅の流れ">'+body+'</section>'+footer+'</section>'
    navigation=[{'id':'home','label':'表紙'},{'id':'route','label':'見取り図'}]+[{'id':s['id'],'label':s['label']} for s in stages]
    return home,navigation
