"""Chronological pilgrimage composition driven by trip data, across travel days.

Covers retain their art direction; events join places, scenes and geographic
stops without separate story/place/timetable views or copied itinerary content.
"""
from urllib.parse import urlencode
from route_maps import ordered_stops


def compose(data, stages, episodes, scenes, missions, image, feature,
            paragraphs, link, mission_group, H, types, map_html, days, hero=''):
    meta=data['meta'];layout=meta.get('layout','immersive')
    def illustration(spec):
        if not spec:return ''
        role=spec.get('role','scene')
        if role not in ('scene','sticker'):raise ValueError('Unknown journey illustration role')
        if role=='scene':return feature(spec['image'],spec.get('caption','非公式の創作挿絵'))
        art=image(spec['image'],'travel-mascot')
        if spec.get('panel'):
            if spec['panel'] not in ('top-left','top-right','bottom-left','bottom-right'):raise ValueError('Unknown sticker panel')
            art='<span class="sticker-viewport '+spec['panel']+'">'+art+'</span>'
        return '<figure class="journey-sticker">'+art+'<figcaption>'+H(spec.get('caption',''))+'</figcaption></figure>'
    by_stage={s['spec']['id']:s for s in stages}
    visits=[e['stage_id'] for d in days for e in d['events'] if e.get('stage_id')]
    if len(visits)!=len(set(visits)) or set(visits)!=set(by_stage):
        raise ValueError('Every integrated place must be introduced exactly once across the trip')
    points={s['id']:s for s in ordered_stops(data,days)}
    highlights={h['id']:h for s in data['stages'] for h in s['highlights'] if isinstance(h,dict) and h.get('id')}
    primary=next(w for w in data['works'] if w['id']==data['selection']['primary_work_id'])
    def directions(a,b,mode=''):
        q={'api':1,'origin':str(a['lat'])+','+str(a['lon']),'destination':str(b['lat'])+','+str(b['lon'])}
        if mode in ['walking','transit','driving']:q['travelmode']=mode
        return 'https://www.google.com/maps/dir/?'+urlencode(q)
    def local_map(selected,label='この場所の地図・入口を見る'):
        chosen=selected if isinstance(selected,list) else [selected]
        ids=' '.join(p['id'] for p in chosen)
        notes=''.join('<p>'+H(p.get('note',''))+'</p>' for p in chosen)
        if len(chosen)>1:notes+='<p>点線は訪問・移動の順序です。実際の道路・鉄道路線ではありません。</p>'
        return '<details class="local-map-details"><summary>'+H(label)+'</summary><div class="local-stop-map" data-local-map="'+H(chosen[0]['id'])+'" data-local-stops="'+H(ids)+'" role="region" aria-label="'+H(label)+'"></div>'+notes+link('https://www.google.com/maps/search/?'+urlencode({'api':1,'query':str(chosen[0]['lat'])+','+str(chosen[0]['lon'])}),'地図アプリで開く')+'</details>'
    credit=H(meta.get('art_label','非公式の創作挿絵'))+' / '+H(meta.get('dates',''))
    if layout=='casefile':
        lines=meta.get('cover_title_lines') or meta.get('title_lines') or [meta['title']]
        headline='<br>'.join(('<em>'+H(t)+'</em>') if i==len(lines)-1 else H(t) for i,t in enumerate(lines))
        cover=f'''<header class="case-cover"><div class="issue-line"><span>{H(meta.get('cover_issue',meta.get('kicker','FIELD NOTES')))}</span><span>{len(episodes):02} SCENES</span></div><h1><small>{H(primary['title'])}</small>{headline}</h1><p class="cover-deck">{H(meta.get('subtitle',''))}</p><figure class="case-portrait">{image(meta['hero_image'],'hero-art',True)}<figcaption>{H(meta.get('cover_caption','物語と、旅の順番で。'))}</figcaption></figure><p class="editorial-credit">{credit}</p><a class="editorial-start" href="#trip-start">{H(meta.get('journey_start','旅をはじめる'))} <span>↓</span></a></header>'''
    elif layout=='pursuit':
        slogan=H(meta.get('cover_line',meta.get('subtitle',''))).replace('\n','<br>')
        description=H(meta.get('cover_description',meta.get('subtitle',''))).replace('\n','<br>')
        cover=f'''<header class="pursuit-cover"><div class="pursuit-poster">{image(meta['hero_image'],'hero-art',True)}<div class="pursuit-brand"><p>{H(meta.get('cover_credit',meta.get('kicker','STORY PILGRIMAGE')))}</p><h1>{H(meta.get('cover_title',meta['title']))}</h1><span>{H(meta.get('cover_tagline','FOLLOW THE STORY'))}</span></div><div class="pursuit-hero-copy"><div class="trail-counter"><b>{len(stages):02}</b><span>PLACES.<br>ONE JOURNEY.</span></div><h2>{slogan}</h2><p>{description}</p></div></div><div class="pursuit-cover-tail"><a href="#trip-start" class="pursuit-start"><span>{H(meta.get('journey_start','旅をはじめる'))}</span><b>↗</b></a><p class="pursuit-coordinates">{H(meta.get('regions',''))}</p><p class="editorial-credit">{credit}</p></div></header>'''
    else:
        cover=hero
    brief=meta.get('journey_intro',{})
    intro='<section class="journey-orientation" id="trip-start"><span class="kicker">'+H(brief.get('kicker',meta.get('kicker','YOUR JOURNEY')))+'</span><h2>'+H(brief.get('title',meta['title']))+'</h2>'+paragraphs(brief.get('body') or meta.get('introduction') or [meta.get('subtitle','')])
    intro+='<div class="journey-facts">'+''.join('<span>'+H(x)+'</span>' for x in brief.get('facts',[meta.get('dates',''),meta.get('regions','')]) if x)+'</div><p class="journey-model-note">'+H(brief.get('note',meta.get('itinerary_note','')))+'</p>'
    intro+='<details class="journey-watchlist" id="trip-reading"><summary>この旅につながる物語を振り返る</summary><p>'+H(meta.get('story_intro',''))+'</p>'+''.join('<button data-episode="'+H(e['id'])+'">'+H(e['number'])+' / '+H(e['name'])+' ↗</button>' for e in episodes)+'</details></section>'
    day_index=''
    if len(days)>1:
        day_index='<nav class="journey-day-index" aria-label="日ごとの目次">'+''.join('<a href="#day-'+H(d['id'])+'"><small>'+H(d['label'])+'</small><span>'+H(d.get('title',d['label']))+'</span></a>' for d in days)+'</nav>'
    overview='<section id="route" class="journey-overview">'+map_html+day_index+'</section>'
    body='';previous=None;episode_index={e['id']:e for e in episodes}
    for day in days:
        transfer_day=day.get('kind')=='transfer'
        body+='<section class="journey-day'+(' transfer-day' if transfer_day else '')+'" id="day-'+H(day['id'])+'" aria-label="'+H(day.get('title',day['label']))+'">'
        if len(days)>1:
            day_title=day.get('title',day['label'])
            parts=day_title.split(' → ') if transfer_day else [day_title]
            title_html='<span class="day-city">'+H(parts[0])+'</span>'
            for part in parts[1:]:title_html+='<span class="day-route-arrow" aria-hidden="true">↓</span><span class="day-city">'+H(part)+'</span>'
            body+='<header class="journey-day-heading"><span>'+H(day['label'])+(' / ON THE MOVE' if transfer_day else ' / ON LOCATION')+'</span><h2 aria-label="'+H(day_title)+'">'+title_html+'</h2><p>'+H(day.get('description',''))+'</p></header>'
            day_points=[points[k] for k in day.get('map_stop_ids',[])]
            if len(day_points)>1:body+='<div class="journey-day-geography">'+local_map(day_points,'この日の場所と移動を地図で見る')+'</div>'
        for i,event in enumerate(day['events']):
            point=points.get(event.get('map_stop_id'))
            time='<span class="journey-time">'+H(event.get('time',''))+'</span>'
            if event.get('stage_id'):
                st=by_stage[event['stage_id']];spec=st['spec']
                if not point or point.get('stage_id')!=spec['id']:raise ValueError('Integrated visit needs a matching geographic stop')
                number=list(points).index(point['id'])+1
                title=spec['name'] if layout=='casefile' else spec['location']
                subtitle=spec['location'] if layout=='casefile' else spec['name']
                body+=f'<article class="journey-visit" id="{st["id"]}" aria-labelledby="title-{st["id"]}"><header class="journey-visit-head" id="stop-{H(point["id"])}"><div class="visit-stamp">{time}<span>STOP {number:02}</span></div><h2 id="title-{st["id"]}">{H(title)}</h2><p class="visit-place">{H(subtitle)}</p><p class="visit-hook">{H(spec.get("hook",""))}</p></header>'
                body+=feature(spec['image'],'非公式の創作挿絵 · 現地の記録写真ではありません')+'<div class="journey-visit-body">'
                stage_scenes=[s for s in scenes if s['stage']==st['id']]
                for si,(scene,scene_spec) in enumerate(zip(stage_scenes,spec['scenes'])):
                    if scene_spec['image']!=spec['image']:body+=feature(scene_spec['image'],scene['name'])
                    ep=episode_index.get(scene['episode'])
                    copy=(ep.get('body') or [scene['text']])[0] if ep and si==0 else scene['text']
                    reading='<p>'+H(copy)+'</p><div class="scene-actions">'
                    if ep:reading+='<button data-episode="'+H(scene['episode'])+'">物語を振り返る ↗</button>'
                    reading+='<button data-scene="'+H(scene['id'])+'">挿絵と場面を読む ↗</button></div>'
                    if scene.get('spoiler'):reading='<details class="scene-spoiler"><summary>物語の終盤を振り返る（ネタバレ）</summary>'+reading+'</details>'
                    body+='<div class="scene-memory"><span class="kicker">あの場面を、ここで。</span><h3>'+H(scene['name'])+'</h3>'+reading+'</div>'
                body+='<section class="onsite-clues"><h3>現地で探す、手がかり。</h3>'
                for h in spec['highlights']:
                    item=h if isinstance(h,dict) else {'title':h}
                    if item.get('kind')=='related':continue
                    body+='<div class="onsite-clue"><h4>'+H(item['title'])+'</h4><p>'+H(item.get('description',''))+'</p>'+link(item.get('source_url'),'現地情報の出典')+'</div>'
                body+='</section>'+local_map(point)+'<div class="visit-practical"><span>この場所で過ごす時間</span><p>'+H(event.get('description',''))+'</p><p>'+H(spec.get('practical',''))+'</p></div>'
                body+='<details class="visit-research"><summary>場所と作品の照合メモ</summary>'+paragraphs(spec.get('paragraphs',[]))
                for rel in spec.get('connections',[]):body+='<strong>'+H(types[rel['type']])+'</strong><p>'+H(rel['description'])+'</p>'+link(rel['source_url'],'関係の根拠')
                body+='</details><details class="visit-checklist"><summary>ここで見つけたものを記録</summary>'+mission_group(st['id'],st['label'],[m for m in missions if m['stage']==st['id']])+'</details><div class="chapter-tools"><button data-bookmark="'+st['id']+'" aria-pressed="false">◇ この場所を保存</button><button data-action="share">仲間に渡す ↗</button></div></div></article>'
            elif event.get('related_highlight_id'):
                h=highlights.get(event['related_highlight_id'])
                if not h or not point:raise ValueError('Optional visit needs an existing highlight and geographic stop')
                body+='<aside class="journey-detour" id="stop-'+H(point['id'])+'"><div class="visit-stamp">'+time+'<span>任意の寄り道</span></div><h3>'+H(h['title'])+'</h3><p>'+H(h.get('description',''))+'</p><p>'+H(event.get('description',''))+'</p>'+local_map(point)+link(h.get('source_url'),'関連スポットの案内')+'</aside>'
            elif event.get('kind')=='transfer':
                start=points.get(event.get('from_stop_id')) or previous
                nxt=points.get(event.get('to_stop_id')) or next((points.get(e.get('map_stop_id')) for e in day['events'][i+1:] if e.get('map_stop_id')),None)
                if not start or not nxt:raise ValueError('Transfer needs geographic origin and destination')
                body+='<aside class="journey-transfer"><div class="transfer-line"></div>'+time+'<h3>'+H(event.get('title',event.get('label','')))+'</h3><p>'+H(event.get('description',''))+'</p>'+link(directions(start,nxt,event.get('travelmode','')),'次の場所への経路候補を開く','directions-link')+link(event.get('transport_url'),'運行・乗継を確認','transport-link')+'</aside>'
            elif event.get('kind')=='observation' and point:
                body+='<aside class="journey-observation" id="stop-'+H(point['id'])+'">'+time+'<h3>'+H(event.get('title',event.get('label','')))+'</h3><p>'+H(event.get('description',''))+'</p>'+local_map(point)+'</aside>'
            else:
                body+='<aside class="journey-pause">'+time+'<div><h3>'+H(event.get('title',event.get('label','')))+'</h3><p>'+H(event.get('description',''))+'</p></div></aside>'
            body+=illustration(event.get('illustration'))
            if point:previous=point
        body+='</section>'
    footer='<section class="journey-finish"><span class="kicker">YOUR JOURNEY / YOUR MEMORIES</span><h2>'+H(meta.get('journey_closing_heading','物語の景色が、\n自分の記憶になる。')).replace('\n','<br>')+'</h2><p>'+H(meta.get('closing',''))+'</p><details open><summary>旅の記録を見る</summary>'+mission_group('all','旅全体',missions)+'</details><div class="menu-list"><button data-action="save">画像込みでこの旅を保存 ↓</button><button data-action="share">旅仲間に渡す ↗</button><button data-open="sources">出典・挿絵の制作記録</button><button data-open="howto">使い方</button><button data-action="motion" aria-pressed="true">ON</button></div></section>'
    home='<section class="view active" id="home">'+cover+intro+overview+body+illustration(meta.get('closing_illustration'))+footer+'</section>'
    navigation=[{'id':'home','label':'表紙'},{'id':'route','label':'見取り図'}]+[{'id':by_stage[i]['id'],'label':by_stage[i]['label']} for i in visits]
    return home,navigation
