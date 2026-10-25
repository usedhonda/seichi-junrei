"""Geographic stop maps; routing stays with the linked map provider."""
import html
import json
import math
import re
from urllib.parse import urlencode


def prepare(data, days):
    config = data.get('route_map')
    if not config:
        return '', ''
    stops = config.get('stops', [])
    if not stops or len(stops) > 30:
        raise ValueError('Route map needs 1–30 public stops')
    ids = set()
    for stop in stops:
        ident = stop.get('id', '')
        if not re.fullmatch(r'[A-Za-z0-9_-]+', ident) or ident in ids:
            raise ValueError('Map stop IDs must be unique safe identifiers')
        ids.add(ident)
        if not isinstance(stop.get('label'), str) or not stop['label']:
            raise ValueError('Map stop needs a label')
        for key, low, high in [('lat', -85, 85), ('lon', -180, 180)]:
            v = stop.get(key)
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or not low <= v <= high:
                raise ValueError('Invalid map coordinate: '+key)
        if stop.get('stage_id') and stop['stage_id'] not in {s['id'] for s in data['stages']}:
            raise ValueError('Map stop refers to unknown stage')
    ordered_days = []
    for day in days:
        day_stops = day.get('map_stop_ids', [])
        if len(day_stops) != len(set(day_stops)) or any(s not in ids for s in day_stops):
            raise ValueError('Map day refers to duplicate or unknown stops')
        for event in day.get('events', []):
            if event.get('map_stop_id') and event['map_stop_id'] not in day_stops:
                raise ValueError('Timed stop must belong to its map day')
        ordered_days.append({'id': str(day['id']), 'label': day['label'], 'stops': day_stops,
                             'mode': day.get('map_mode', '')})
    # Map search links use coordinates; detailed entrances remain in the guide.
    clean_stops = []
    for index, stop in enumerate(stops):
        point = str(stop['lat'])+','+str(stop['lon'])
        clean_stops.append({**{k: stop[k] for k in ['id','label','lat','lon']},
                            'number': index+1, 'stage': 'stage-'+stop['stage_id'] if stop.get('stage_id') else '',
                            'note': stop.get('note',''),
                            'url': 'https://www.google.com/maps/search/?'+urlencode({'api':1,'query':point})})
    payload = {'stops': clean_stops, 'days': ordered_days}
    encoded = json.dumps(payload, ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    content = '''<section class="route-map-section" aria-labelledby="route-map-title"><div class="route-map-heading"><div><span class="kicker">PLACES & MOVEMENT</span><h2 id="route-map-title">この日の、場所と道のり。</h2></div><div class="map-view-switch" role="group" aria-label="地図の範囲"><button data-map-view="day" aria-pressed="true">この日</button><button data-map-view="all" aria-pressed="false">全体</button></div></div><p class="map-caption" data-map-caption></p><div id="journey-map" class="journey-map" role="region" aria-label="巡礼スポットの地図"></div><p class="map-status" data-map-status role="status">背景地図は通信時に表示します。保存版でも地点と訪問順は確認できます。</p><div class="map-stop-list" data-map-stops></div><p class="map-note">点線は訪問順です。道路や鉄道路線、実際の経路を表していません。地図の点は施設・街の代表位置で、入口や席の指定ではありません。</p></section>'''
    return content, '<script type="application/json" id="route-map-data">'+encoded+'</script>'


def event_link(event):
    ident = event.get('map_stop_id')
    if not ident:
        return ''
    return '<button class="timeline-map-link" data-map-stop="'+html.escape(ident, quote=True)+'">地図で場所を見る ↑</button>'
