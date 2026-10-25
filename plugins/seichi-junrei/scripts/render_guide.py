#!/usr/bin/env python3
"""Render a user-selected pilgrimage guide into one offline, self-contained HTML file.

Requires selection consent in JSON. Images are local and embedded; no network requests. Pillow is required.
"""
import argparse
import base64
import html
import io
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    from PIL import Image
except ImportError:
    Image = None

H = lambda val: html.escape(str(val if val is not None else ""), quote=True)
SENSITIVE_KEYS = re.compile(
    r"(?i)(?:pnr|booking.?ref|reservation.?ref|confirmation.?code|ticket.?num|passport|seat.?num|"
    r"passenger|traveler.?name|first.?name|last.?name|email|phone|room.?num|"
    r"private.?calendar|calendar.?id|event.?description|record.?locator|internal.?notes|raw.?event|api.?token)"
)
SENSITIVE_TEXT = [
    ("email", re.compile(r"[\w.%+\-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("possible PNR", re.compile(r"(?i)\b(?:PNR|booking reference|reservation number|予約番号|確認番号)\s*[:：#]?\s*[A-Z0-9-]{4,}\b")),
]
TYPES = {
    "named_setting": "作中に登場する地名", "filming_location": "実際のロケ地",
    "official_inspiration": "公式に確認されたモデル", "documented_connection": "資料で確認できる関係",
    "thematic": "作品のテーマに通じる場所", "speculative": "ファンの推測・未確認"
}
SAFE_MEDIA = {"original_generated", "user_owned", "licensed", "public_domain"}


def url(v):
    if not v:
        return ""
    p = urlparse(v)
    if p.scheme != "https" or not p.netloc or p.username or p.password:
        raise ValueError("Only absolute https URLs allowed: " + repr(v))
    return H(v)


def validate(data):
    choice = data.get("selection", {})
    if not ((choice.get("user_confirmed") is True) or (choice.get("delegated") is True)):
        raise ValueError("User-selection gate: user_confirmed=true OR delegated=true required before rendering")
    chosen = choice.get("primary_work_id")
    ids = [x.get("id") for x in data.get("works", [])]
    if chosen not in ids or not chosen:
        raise ValueError("Primary work ID must match a work in 'works'")
    extras = choice.get("secondary_work_ids", [])
    if len(extras) > 2 or any(x not in ids or x == chosen for x in extras):
        raise ValueError("Secondary work list is invalid")
    if not data.get("stages"):
        raise ValueError("At least one stage required")
    if not data.get("sources"):
        raise ValueError("Guide must have verifiable source URLs")
    def walk(value, path="$"):
        if isinstance(value, dict):
            for k, v in value.items():
                if SENSITIVE_KEYS.search(k):
                    raise ValueError(f"Private field not allowed at {path}.{k}")
                walk(v, path+"."+str(k))
        elif isinstance(value, list):
            for i, v in enumerate(value):
                walk(v, path+f"[{i}]")
        elif isinstance(value, str):
            if (not path.endswith(".url") and not path.endswith(".source_url") and not path.endswith(".map_url") and not path.endswith(".notes")):
                for label, pat in SENSITIVE_TEXT:
                    if pat.search(value):
                        raise ValueError(f"Possible sensitive {label} in {path}")
    walk(data)
    stage_ids = [st.get('id', '') for st in data['stages']]
    if len(set(stage_ids)) != len(stage_ids) or any(not re.fullmatch(r'[A-Za-z0-9_-]+', ident) for ident in stage_ids):
        raise ValueError('Stage IDs must be unique safe identifiers')
    if data.get('meta', {}).get('character_art_required'):
        rights = {item['file']: item for item in data.get('media_rights', [])}
        required = [data['meta'].get('hero_image')]
        required += [ep.get('image') for work in data['works'] if work['id'] in {chosen, *extras} for ep in work.get('episodes', [])]
        required += [scene.get('image') for st in data['stages'] for scene in st.get('scenes', [])]
        if any(not rights.get(path, {}).get('characters') for path in required):
            raise ValueError('Requested character artwork needs depicted characters in hero, story cards and scene assets')
    for work in data['works']:
        if work['id'] not in {chosen, *extras}:
            continue
        for ep in work.get('episodes', []):
            if not ep.get('source_url'):
                raise ValueError('Story beat lacks source URL')
    for st in data["stages"]:
        if not st.get("scenes"):
            raise ValueError(f"Stage {st.get('id')}: include a scene beat and an image between place content")
        if not st.get("highlights"):
            raise ValueError(f"Stage {st.get('id')}: include real-world observations")
        for relation in st.get("connections", []):
            if relation.get("type") not in TYPES:
                raise ValueError("Unknown connection classification")
            if not relation.get("source_url"):
                raise ValueError("Scene-to-place claim lacks source URL")
            url(relation["source_url"])
        for scene in st.get("scenes", []):
            if not scene.get("source_url"):
                raise ValueError("Story scene lacks source URL")
            url(scene["source_url"])
    def check_urls(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key.endswith('_url') and item:
                    url(item)
                check_urls(item)
        elif isinstance(value, list):
            for item in value:
                check_urls(item)
    check_urls(data)
    day_ids = [str(day['id']) for day in data.get('itinerary', [])]
    if len(day_ids) != len(set(day_ids)):
        raise ValueError('Day IDs must be unique')
    for st in data['stages']:
        if any(not re.fullmatch(r'[A-Za-z0-9_-]+', m.get('id', '')) for m in st.get('missions', [])):
            raise ValueError('Mission IDs must be safe identifiers')
    for src in data["sources"]:
        url(src["url"])


class Media:
    def __init__(self, data, root):
        self.root = root.resolve()
        self.cached = {}
        self.rights = {item["file"]: item for item in data.get("media_rights", [])}
    def embed(self, name):
        if not name:
            return ""
        if re.match(r"https?://", name, flags=re.I) or name.startswith("data:"):
            raise ValueError("Media must be a local asset: " + name)
        if name not in self.rights:
            raise ValueError("Missing rights entry for image: " + name)
        info = self.rights[name]
        if info.get("status") not in SAFE_MEDIA:
            raise ValueError("Image rights status must be explicitly approved")
        if info["status"] == "licensed" and not info.get("license_url"):
            raise ValueError("Licensed media must include a license URL")
        if name in self.cached:
            return self.cached[name]
        p = (self.root / name).resolve()
        if not p.is_relative_to(self.root):
            raise ValueError("Image path escapes skill directory")
        if not p.is_file() or p.stat().st_size > 15_000_000:
            raise ValueError("Missing/oversize image: " + str(p))
        if Image is None:
            raise RuntimeError("Pillow required to embed and optimize images")
        with Image.open(p) as raw:
            im = raw.convert("RGB")
            im.thumbnail((1600, 1400))
            buf = io.BytesIO()
            im.save(buf, "WEBP", quality=80, method=5)
            raw_bytes = p.read_bytes() if raw.format == "WEBP" and raw.width <= 1600 and raw.height <= 1600 else buf.getvalue()
        s = "data:image/webp;base64," + base64.b64encode(raw_bytes).decode("ascii")
        self.cached[name] = s
        return s


def render(data, root):
    """Render any selected story/trip with the same mobile system as the public sample."""
    validate(data)
    import hashlib
    meta = data['meta']
    media = Media(data, Path(root))
    runtime_root = Path(__file__).resolve().parents[1] / 'assets/mobile-guide'
    theme = meta.get('theme', 'night-gold')
    if theme not in ('night-gold', 'pop-postcard', 'casebook', 'ink-copper'):
        raise ValueError('Unknown mobile theme: '+str(theme))
    css = (runtime_root / 'guide.css').read_text(encoding='utf-8')
    layout = meta.get('layout', 'immersive')
    if layout not in ('immersive', 'casefile', 'literary'):
        raise ValueError('Unknown mobile layout: '+str(layout))
    layout_attr = '' if layout == 'immersive' else f' data-layout="{layout}"'
    if layout != 'immersive':
        css += (runtime_root / 'editorial.css').read_text(encoding='utf-8')
    js = (runtime_root / 'guide.js').read_text(encoding='utf-8')
    if layout != 'immersive':
        # The editorial lists are vertical; keep their help accurate while the
        # original immersive guide and runtime remain byte-for-byte unchanged.
        js = js.replace('<h3>横にめくる</h3>', '<h3>縦に読み進める</h3>').replace(
            '話数カードと場面カードは横スワイプ。タップで詳しい読み物が下から開きます。',
            '物語と場面は縦に並んでいます。見出しや挿絵をタップすると、詳しい読み物が開きます。')
    stages, episodes, scenes, missions = [], [], [], []
    assets, provenance = {}, []
    serial = 0

    def asset(path):
        nonlocal serial
        if not path:
            raise ValueError('Every cover, story card and scene needs a local illustration')
        if path not in assets:
            serial += 1
            info = media.rights.get(path, {})
            assets[path] = {'id': 'art-'+str(serial), 'src': media.embed(path),
                            'alt': info.get('alt') or info.get('notes') or '作品と旅をつなぐ創作イラスト'}
            provenance.append({'label': assets[path]['alt'], 'creator': info.get('creator', ''), 'notes': info.get('notes', '')})
        return assets[path]

    def image(path, cls='', eager=False):
        a = asset(path)
        return f'<img class="{H(cls)}" src="{a["src"]}" alt="{H(a["alt"])}" data-art="{a["id"]}" loading="{"eager" if eager else "lazy"}" decoding="async">'

    def link(href, label, cls='source'):
        return f'<a class="{cls}" href="{url(href)}" target="_blank" rel="noopener noreferrer">{H(label)} ↗</a>' if href else ''

    def paragraphs(items):
        return ''.join('<p>'+H(x)+'</p>' for x in items)

    selected_ids = {data['selection']['primary_work_id'], *data['selection'].get('secondary_work_ids', [])}
    works = [work for work in data['works'] if work['id'] in selected_ids]
    for wi, work in enumerate(works):
        for ei, ep in enumerate(work.get('episodes', [])):
            ident = str(ep.get('id') or f'{work["id"]}-{ei+1}')
            a = asset(ep.get('image'))
            episodes.append({'id': ident, 'number': str(ep.get('number', ei+1)), 'art': a['id'],
                             'name': ep.get('name', ep['title']), 'title': ep['title'], 'place': ep.get('place', work['title']),
                             'tag': ep.get('tag', work['title']), 'body': ep.get('body') or [ep.get('summary', '')],
                             'spoiler': ep.get('spoiler', ''), 'note': ep.get('note', ''), 'source': ep.get('source_url', '')})
    if not episodes:
        raise ValueError('At least one illustrated story beat is required (film scenes may use named, nonnumeric IDs)')
    if len({ep['id'] for ep in episodes}) != len(episodes):
        raise ValueError('Story IDs must be unique across works')
    for st in data['stages']:
        ident = 'stage-'+st['id']
        stages.append({'id': ident, 'label': st.get('name', st['location']), 'title': st['location'], 'spec': st})
        for i, scene in enumerate(st['scenes']):
            a = asset(scene.get('image'))
            ep_id = str(scene.get('episode_id', ''))
            if ep_id and ep_id not in {ep['id'] for ep in episodes}:
                raise ValueError('Unknown scene episode_id: '+ep_id)
            scenes.append({'id': f'{ident}-scene-{i+1}', 'stage': ident, 'art': a['id'], 'episode': ep_id,
                           'name': scene['title'], 'caption': scene.get('episode', ''), 'text': scene['description'],
                           'spoiler': scene.get('spoiler', False), 'source': scene['source_url']})
        for m in st.get('missions', []):
            missions.append({'id': ident+':'+m['id'], 'stage': ident, 'text': m['text'], 'detail': m.get('detail', '')})
    if len({m['id'] for m in missions}) != len(missions):
        raise ValueError('Mission IDs must be unique within each stage')

    def mission_group(scope, label, subset):
        rows = ''
        for m in subset:
            control = 'mission-'+scope+'-'+m['id'].replace(':', '-')
            rows += f'<label class="mission" for="{H(control)}"><span class="mission-control"><input type="checkbox" id="{H(control)}" data-mission="{H(m["id"])}"><span class="check-ring" aria-hidden="true">✓</span></span><span class="mtext"><b>{H(m["text"])}</b><small>{H(m["detail"])}</small></span></label>'
        return f'<div class="mission-group" data-mission-scope="{H(scope)}" data-mission-label="{H(label)}" role="group" aria-label="{H(label)}のチェックリスト">{rows}<div class="mission-progress"><span data-mission-count aria-live="polite">0 / {len(subset)} 完了</span><span class="mission-track" data-mission-meter role="progressbar" aria-label="{H(label)}の達成状況" aria-valuemin="0" aria-valuemax="{len(subset)}" aria-valuenow="0"><i data-mission-progress></i></span></div><p class="mission-note" data-mission-storage>タップでチェックできます。</p></div>'

    def rail(items, ident, kind):
        cards = []
        for item in items:
            a = next(a for a in assets.values() if a['id'] == item['art'])
            img = f'<img src="{a["src"]}" alt="{H(a["alt"])}" data-art="{a["id"]}" loading="lazy" decoding="async">'
            if kind == 'episode':
                cards.append(f'<button class="episode-card" data-episode="{H(item["id"])}" aria-label="{H(item["name"])}">{img}<span class="ep-num">{H(item["number"])}</span><span class="ep-copy"><small>{H(item["place"])}</small>{H(item["name"])} →</span></button>')
            else:
                excerpt = 'タップして、ネタバレを含む場面を開く。' if item['spoiler'] else item['text']
                cards.append(f'<button class="scene-card" data-scene="{H(item["id"])}" aria-label="{H(item["name"])}を読む">{img}<div class="scene-copy"><span class="pill">{H(item["caption"])} · STORY ART</span><h3>{H(item["name"])}</h3><p>{H(excerpt)}</p><span class="open-hint">場面を振り返る →</span></div></button>')
        return f'<div class="edge"><div class="rail" id="{ident}" aria-label="物語のカード。横にスワイプできます">{"".join(cards)}</div></div><div class="rail-footer"><span>← スワイプで物語をめくる</span><div class="dots" data-rail="{ident}"></div></div>'

    def feature(path, caption):
        a = asset(path)
        return f'<figure class="feature-art">{image(path)}<figcaption class="art-label"><span>{H(caption)}</span><button data-full="{a["id"]}" aria-label="挿絵を大きく表示">拡大 ＋</button></figcaption></figure>'

    primary = next(w for w in data['works'] if w['id'] == data['selection']['primary_work_id'])
    title_lines = meta.get('title_lines') or [meta['title']]
    title = ''.join('<span'+(' class="title-small"' if i in meta.get('title_small_lines', []) else '')+'>'+H(line)+'</span>' for i, line in enumerate(title_lines))
    cover_line = H(meta.get('cover_line', 'あの物語を、旅の隣に。')).replace(chr(10), '<br>')
    kicker = H(meta.get('kicker', primary['title']))
    hero = f'<div class="hero">{image(meta["hero_image"], "hero-art", True)}<span class="star"></span><span class="star two"></span><p class="vertical">{cover_line}</p><div class="hero-bottom"><div class="kicker">{kicker}</div><h1>{title}</h1><p class="hero-subtitle">{H(meta.get("subtitle", ""))}</p><div class="journey-tag">{H(meta.get("regions", ""))}</div><div class="hero-cta"><a href="#{stages[0]["id"]}" class="btn primary">旅をひらく →</a><a href="#story" class="btn secondary">物語を振り返る →</a></div><div class="art-credit">{H(meta.get("art_label", "UNOFFICIAL STORY PILGRIMAGE"))} · {H(meta.get("dates", ""))}</div></div></div>'
    destinations = ''
    for st in stages:
        spec = st['spec']
        destinations += f'<a class="destination" href="#{st["id"]}">{image(spec["image"], "place-img")}<span class="stage-tag">{H(spec.get("label", "DESTINATION"))}</span><div class="destination-copy"><h3>{H(st["title"])}</h3><div class="destination-jp">{H(st["label"])}</div><p>{H(spec.get("hook", ""))}</p><span class="arrow">→</span></div></a>'
    home = '<section class="view active" id="home" aria-label="表紙と旅の入り口">'+hero+'<section class="section reveal"><div class="section-heading"><div><div class="kicker">REWIND THE ADVENTURE</div><h2>STORY GUIDE<small>旅の前に、あの場面を。</small></h2></div></div>'+rail(episodes, 'home-episodes', 'episode')+'</section><section class="section paper reveal"><div class="kicker">THE STORY MEETS THE PLACE</div><h2>物語と、現地が出会う。</h2>'+paragraphs(meta.get('introduction') or [meta.get('subtitle', '')])+'</section><section class="section reveal"><div class="kicker">YOUR DESTINATIONS</div>'+destinations+'</section><section class="section paper reveal"><div class="kicker">YOUR MEMORY PASSPORT</div><h2>旅の思い出を、ひとつずつ。</h2>'+mission_group('all', '旅全体', missions)+'</section><section class="outro"><div class="eyebrow">THE JOURNEY CONTINUES</div><h2>物語の景色が、<br>自分の記憶になる。</h2><p>'+H(meta.get('closing', '画面から顔を上げて、目の前の景色も楽しもう。'))+'</p></section></section>'
    story = '<section class="view" id="story" aria-label="物語"><div class="page-lead"><div class="kicker">STORY PILGRIMAGE</div><h1>THE STORY.<small>'+H(primary['title'])+'</small></h1><p>'+H(meta.get('story_intro', '知らない仲間にも伝えたい、旅につながる物語。'))+'</p></div><section class="section">'+rail(episodes, 'story-episodes', 'episode')+''.join(feature(ep.get('image'), ep['title']) for w in works for ep in w.get('episodes', []))+'</section></section>'
    chapters = ''
    for si, st in enumerate(stages):
        spec, ident = st['spec'], st['id']
        chapter = f'<section class="view" id="{ident}" aria-label="{H(st["label"])}編"><header class="subhero place-head">{image(spec["image"], eager=True)}<span class="pill">{H(spec.get("label", f"STAGE {si+1:02}"))}</span><h1>{H(st["title"])}<small>{H(st["label"])}</small></h1><p class="subtitle">{H(spec.get("hook", ""))}</p></header><div class="chapter-tools"><button data-bookmark="{ident}" aria-pressed="false">◇ この章を保存</button><button data-action="share">仲間に渡す ↗</button></div><nav class="subnav" aria-label="章内案内"><a href="#{ident}-story">物語</a><a href="#{ident}-sights">見どころ</a><a href="#{ident}-missions">ミッション</a><a href="#route">旅程</a></nav>'
        chapter += f'<section class="section" id="{ident}-story"><div class="section-heading"><div><div class="kicker">THE STORY IN THIS PLACE</div><h2>{H(spec.get("story_heading", "あの場面を、思い出す。"))}</h2></div></div>'+rail([s for s in scenes if s['stage'] == ident], ident+'-scenes', 'scene')+'</section>'
        chapter += '<section class="story-copy reveal">'+paragraphs(spec.get('paragraphs') or [spec.get('location_note', '')])+'</section>'
        for scene in spec['scenes']:
            chapter += feature(scene['image'], scene['title'])
            text = '<h2>'+H(scene['title'])+'</h2><p>'+H(scene['description'])+'</p>'+link(scene['source_url'], '物語の出典')
            if scene.get('spoiler'):
                text = '<details><summary>結末まで振り返る（ネタバレ）</summary>'+text+'</details>'
            chapter += '<section class="story-copy reveal">'+text+'</section>'
        chapter += f'<section class="section paper reveal" id="{ident}-sights"><div class="kicker">LOOK UP FROM THE SCREEN</div><h2>物語の隣にある、<br>本当の景色。</h2>'
        for i, sight in enumerate(spec['highlights']):
            item = sight if isinstance(sight, dict) else {'title': sight}
            chapter += f'<article class="sight"><span class="n">{i+1:02}</span><div><h3>{H(item["title"])}</h3><p>{H(item.get("description", ""))}</p>'+link(item.get('map_url') or spec.get('map_url'), '地図で見る', 'map-link')+link(item.get('source_url'), '現地情報の出典')+'</div></article>'
        for relation in spec.get('connections', []):
            chapter += '<div class="callout"><strong>'+H(TYPES[relation['type']])+'</strong><p>'+H(relation['description'])+'</p>'+link(relation['source_url'], '関係の根拠')+'</div>'
        chapter += '<div class="practical"><h3>'+H(spec.get('practical_title', 'ひとつ詰め込むより、一度立ち止まる。'))+'</h3><p>'+H(spec.get('practical', '移動・休息と現地の入場条件を優先。時間に合わない寄り道は省きましょう。'))+'</p></div></section>'
        chapter += f'<section class="section paper reveal" id="{ident}-missions"><div class="kicker">YOUR MEMORY PASSPORT</div><h2>{H(st["label"])}で、やってみる。</h2>'+mission_group(ident, st['label'], [m for m in missions if m['stage'] == ident])+'</section>'
        if si+1 < len(stages):
            nxt = stages[si+1]
            chapter += f'<a class="next-destination" href="#{nxt["id"]}">{image(nxt["spec"]["image"])}<div><div class="kicker">THE NEXT CHAPTER</div><strong>{H(nxt["title"])}</strong></div><span>→</span></a>'
        chapters += chapter+'</section>'
    days = data.get('itinerary') or [{'id': str(i+1), 'label': st['spec'].get('date') or 'DAY '+str(i+1), 'events': st['spec'].get('events', [])} for i, st in enumerate(stages)]
    tabs, panels = '', ''
    for i, day in enumerate(days):
        did = str(day['id'])
        if not re.fullmatch(r'[A-Za-z0-9_-]+', did):
            raise ValueError('Day IDs must contain only letters, digits, underscores or hyphens')
        tabs += f'<button role="tab" id="day-tab-{did}" aria-controls="day-{did}" aria-selected="{str(i==0).lower()}" data-day="{did}">{H(day["label"])}</button>'
        rows = ''.join('<article><div class="time">'+H(e.get('time', ''))+'</div><div><h3>'+H(e.get('title') or e.get('label', ''))+'</h3><p>'+H(e.get('description', ''))+'</p></div></article>' for e in day.get('events', []))
        panels += f'<div class="timeline" role="tabpanel" aria-labelledby="day-tab-{did}" id="day-{did}" data-day-panel="{did}"{(" hidden" if i else "")}>{rows}</div>'
    route = '<section class="view" id="route" aria-label="旅程と旅の準備"><div class="page-lead"><div class="kicker">YOUR REAL-WORLD ADVENTURE</div><h1>OUR JOURNEY.<small>物語は、旅の順番で。</small></h1><p>'+H(meta.get('regions', ''))+'</p></div><div class="day-switch" role="tablist" aria-label="日程">'+tabs+'</div>'+panels+'<p class="info-note">'+H(meta.get('itinerary_note', '時刻・営業時間・移動手段は、旅行前に最新の公式情報をご確認ください。'))+'</p><section class="section"><div class="menu-list"><button data-action="save">画像込みのしおりを保存 ↓</button><button data-action="share">旅仲間へ渡す ↗</button><button data-open="howto">使い方 →</button><button data-open="sources">出典と制作記録 →</button><button data-action="motion" aria-pressed="true">ON</button></div></section></section>'
    if layout != 'immersive':
        from editorial_layouts import compose
        home, story, chapters, route = compose(layout, data, stages, episodes, scenes, missions, primary, image, rail, feature, paragraphs, link, mission_group, H, TYPES, tabs, panels)
    navigation = [{'id': 'home', 'label': 'TOP'}, {'id': 'story', 'label': '物語'}]+[{'id': s['id'], 'label': s['label']} for s in stages]+[{'id': 'route', 'label': '旅程'}]
    public_url = meta.get('public_url', '')
    if public_url:
        url(public_url)
    guide_id = meta.get('id') or hashlib.sha256((meta['title']+meta.get('dates', '')).encode()).hexdigest()[:16]
    if not re.fullmatch(r'[A-Za-z0-9_-]+', guide_id):
        raise ValueError('meta.id must contain only letters, digits, underscores or hyphens')
    state = {'guideId': guide_id, 'title': meta['title'], 'navigation': navigation, 'stages': [{k: v for k, v in s.items() if k != 'spec'} for s in stages],
             'episodes': episodes, 'scenes': scenes, 'missions': missions, 'publicUrl': public_url,
             'sources': [{'title': s.get('label', s.get('title', '出典')), 'url': s['url']} for s in data['sources']],
             'artNote': meta.get('art_note', '挿絵は非公式の創作イラストです。公式の場面画像や記録写真ではありません。画像ごとの制作記録は以下に掲載しています。'),
             'checkedNote': meta.get('checked_note', '料金・営業時間・交通は変更されることがあります。最新の公式案内を優先してください。'),
             'provenance': provenance, 'characterArtCount': sum(bool(x.get('characters')) for x in data.get('media_rights', []))}
    encoded = json.dumps(state, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    icons = ['⌂', '▤'] + ['♧'] * len(stages) + ['↝']
    nav = ''.join(f'<a href="#{n["id"]}"{(" aria-current=page" if n["id"]=="home" else "")}><span class="nav-symbol" aria-hidden="true">{icons[i]}</span><span>{H(n["label"])}</span></a>' for i, n in enumerate(navigation))
    hero_position = meta.get('hero_position', '50% 50%')
    if not re.fullmatch(r'\d{1,3}% \d{1,3}%', hero_position):
        raise ValueError('hero_position must be two percentages')
    return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="robots" content="noindex,nofollow,noarchive"><meta name="referrer" content="no-referrer"><meta name="theme-color" content="#07131e"><meta name="description" content="{H(meta.get('subtitle',''))}"><title>{H(meta['title'])}</title><style>{css}</style></head><body data-theme="{theme}"{layout_attr} style="--hero-position:{hero_position}"><div class="app"><div class="progress" aria-hidden="true"></div><header class="topbar"><a class="wordmark" href="#home"><span>{H(meta.get('wordmark', 'STORY'))}<small>{H(meta.get('regions', 'FIELDGUIDE'))}</small></span></a><button class="circle" data-open="menu" aria-label="メニューを開く">☰</button></header><noscript><p class="no-script">本文と絵は読めます。画面切替・チェック・保存にはJavaScriptが動くブラウザをご利用ください。</p></noscript><main>{home}{story}{chapters}{route}</main><nav class="bottom-nav" aria-label="メインナビゲーション">{nav}</nav></div><dialog class="dialog" id="sheet" aria-labelledby="sheet-title"><div class="dialog-head" data-drag><span class="drag-handle"></span><span class="dialog-title" id="sheet-title"></span><button class="close" data-close="sheet" aria-label="閉じる">×</button></div><div id="sheet-content"></div></dialog><dialog class="full-art" id="artbox" aria-label="挿絵の拡大表示"><button data-close="artbox" aria-label="拡大画像を閉じる">閉じる ×</button><img id="full-art-img" alt=""><p id="full-art-caption"></p></dialog><div class="toast" role="status" aria-live="polite"></div><script type="application/json" id="guide-data">{encoded}</script><script>{js}</script></body></html>'''


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('guide_json', type=Path)
    p.add_argument('--assets-root', type=Path)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    root = args.assets_root.resolve() if args.assets_root else Path(__file__).resolve().parents[1]
    result = render(json.loads(args.guide_json.read_text(encoding='utf-8')), root)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(result, encoding='utf-8')
    print(f'Rendered {len(result.encode("utf-8")):,} bytes -> {args.out}')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, RuntimeError) as error:
        sys.exit('ERROR: '+str(error))
