#!/usr/bin/env python3
"""Render a user-selected pilgrimage guide into one offline, self-contained HTML file.

Requires selection consent in JSON. No network requests, remote media or runtime dependencies.
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
            raw_bytes = buf.getvalue()
        s = "data:image/webp;base64," + base64.b64encode(raw_bytes).decode("ascii")
        self.cached[name] = s
        return s


def make_nav(stages):
    return '<a href="#intro">TOP</a><a href="#episodes">EPISODES</a>' + ''.join(
        f'<a href="#stage-{H(st["id"])}">{H(st["location"])}</a>' for st in stages
    ) + '<a href="#sources">SOURCES</a>'


def episode_html(works, media):
    items = []
    for w in works:
        for ep in w.get("episodes", []):
            img = media.embed(ep.get("image"))
            art = f'<img src="{img}" alt="{H(ep.get("title", ""))}を連想させるオリジナル挿絵" loading="lazy">' if img else '<div class="ep-art"></div>'
            src = f'<a href="{url(ep["source_url"])}" target="_blank" rel="noopener">出典 ↗</a>' if ep.get("source_url") else ""
            items.append(f'<article class="episode">{art}<div class="episode-copy"><b>EP. {H(ep.get("number", "—"))}</b><strong>{H(ep["title"])}</strong><p>{H(ep.get("summary", ""))}</p>{src}</div></article>')
    return ''.join(items)


def stage_html(st, media, i):
    sid = "stage-" + H(st["id"])
    cover = media.embed(st.get("image"))
    covers = f'<img src="{cover}" alt="{H(st["location"])}を題材とする創作ビジュアル" loading="lazy">' if cover else '<div class="place-gradient"></div>'
    conn = ''.join(f'<div class="relation"><span>{H(TYPES[c["type"]])}</span><p>{H(c.get("description", ""))}</p><a href="{url(c["source_url"])}" target="_blank" rel="noopener">根拠を見る ↗</a></div>' for c in st.get("connections", []))
    sights = ''.join(f'<li>{H(x)}</li>' for x in st.get("highlights", []))
    times = ''.join(f'<div class="time-row"><b>{H(t.get("time", ""))}</b><span>{H(t.get("label", ""))}</span></div>' for t in st.get("events", []))
    scenes = []
    for j, scene in enumerate(st.get("scenes", [])):
        art = media.embed(scene.get("image"))
        pic = f'<img src="{art}" alt="{H(scene["title"])}の雰囲気を表現したオリジナル場面イラスト" loading="lazy">' if art else '<div class="scene-placeholder"></div>'
        body = f'<div class="scene-copy"><span class="small-label">{H(scene.get("episode", "SCENE"))} / STORY SCENE</span><h4>{H(scene["title"])}</h4><p>{H(scene.get("description", ""))}</p><a href="{url(scene["source_url"])}" target="_blank" rel="noopener">あらすじ・出典 ↗</a></div>'
        if scene.get("spoiler"):
            body = f'<details class="spoiler"><summary>ネタバレを開く — {H(scene["title"])}</summary>{body}</details>'
        scenes.append(f'<div class="scene"><div class="scene-visual">{pic}<span class="picture-note">ORIGINAL / INSPIRED ART</span></div>{body}</div>')
    missions = ''.join(f'<label class="mission"><input type="checkbox" data-mission="{H(st["id"])}:{H(m["id"])}"><span>{H(m["text"])}</span></label>' for m in st.get("missions", []))
    mapbtn = f'<a class="mapbtn" target="_blank" rel="noopener" href="{url(st["map_url"])}">現地マップを開く ↗</a>' if st.get("map_url") else ''
    return f'''<section class="stage" id="{sid}"><div class="stage-banner"><span>{H(st.get("label", f"STAGE {i+1:02}"))} · {H(st.get("date", ""))}</span><h2>{H(st["location"])}</h2><p>{H(st.get("hook", ""))}</p></div><div class="stage-top">{covers}<div class="stage-intro"><span class="small-label">FIELD NOTES / WHAT YOU WILL SEE</span><h3>目の前の景色が、<br>物語につながる。</h3><p>{H(st.get("location_note", ""))}</p>{mapbtn}</div></div><div class="stage-body"><div class="stops"><h3 class="subhead">現地の見どころ</h3><ol>{sights}</ol><div class="conn">{conn}</div></div><div class="scenes"><h3 class="subhead">この場面を、思い出す</h3>{''.join(scenes)}</div></div><div class="utility"><div><h3>旅程メモ</h3>{times or '<p>移動・見学時間は現地確認。</p>'}</div><div><h3>現地ミッション</h3>{missions or '<p>景色と物語を楽しもう。</p>'}</div></div></section>'''


def render(data, root):
    validate(data)
    media = Media(data, root)
    meta = data["meta"]
    hero = media.embed(meta.get("hero_image"))
    img = f'<img class="hero-picture" src="{hero}" alt="旅先を象徴するオリジナルイラスト">' if hero else '<div class="hero-picture"></div>'
    primary = next(w for w in data["works"] if w["id"] == data["selection"]["primary_work_id"])
    nav = make_nav(data["stages"])
    eps = episode_html(data["works"], media)
    stages = '\n'.join(stage_html(st, media, i) for i, st in enumerate(data["stages"]))
    srcs = ''.join(f'<li><a href="{url(x["url"])}" rel="noopener" target="_blank">{H(x["label"])} ↗</a></li>' for x in data["sources"])
    asset_notes = ', '.join(dict.fromkeys(x.get("status", "") for x in data.get("media_rights", [])))
    out = '''<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="robots" content="noindex,nofollow,noarchive"><meta name="theme-color" content="#0a1323"><title>@@TITLE@@</title><style>
:root{--navy:#081524;--deep:#09101b;--ink:#132239;--gold:#eed19a;--cream:#faf0df;--parchment:#f1e3c9;--pink:#dc7fac;--line:#94836f;--side:clamp(18px,4vw,44px)}*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:75px}body{margin:0;color:var(--cream);background:#050b15;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN","Noto Sans JP",system-ui,sans-serif;line-height:1.85}img{display:block;max-width:100%}a{color:inherit}main{max-width:1200px;margin:auto;box-shadow:0 12px 90px #01050b;}p{line-height:1.85}a:focus-visible,input:focus-visible,summary:focus-visible{outline:3px solid #ffd474;outline-offset:3px}.hero{height:min(80svh,780px);min-height:510px;position:relative;overflow:hidden;background:#081528}.hero-picture{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 53%}.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#03101fe6 0%,#071624ba 43%,#09152624 82%),linear-gradient(0deg,#060e1be8 0%,transparent 50%)}.hero-inner{position:relative;z-index:1;height:100%;display:flex;flex-direction:column;justify-content:space-between;padding:27px var(--side) 40px}.hero-top{display:flex;justify-content:space-between;align-items:center;gap:15px;font-size:11px;letter-spacing:.16em;font-weight:900;color:#f7d79a}.hero-top .edition{font-size:10px;color:#fff;text-align:right}.eyebrow{letter-spacing:.19em;color:#f3d39b;font-weight:900;font-size:11px}.hero-head h1{font-family:Georgia,"Times New Roman",serif;color:#fee5a9;font-size:clamp(55px,10vw,135px);letter-spacing:-.075em;line-height:.83;text-shadow:0 7px 27px #0007;margin:15px 0 25px;max-width:950px}.hero-head .subtitle{font-size:clamp(15px,2.5vw,25px);font-weight:900;line-height:1.6;max-width:680px}.hero-head .dates{font-family:Georgia,serif;letter-spacing:.16em;font-weight:900;color:#efc792;margin-top:22px;font-size:12px}.nav{display:flex;gap:2px;align-items:center;overflow-x:auto;position:sticky;top:0;z-index:10;background:#0a1627f5;border-top:1px solid #987950;border-bottom:2px solid #b78e59;padding:8px max(12px,var(--side));scrollbar-width:none;backdrop-filter:blur(12px)}.nav::-webkit-scrollbar,.episode-strip::-webkit-scrollbar{display:none}.nav a{white-space:nowrap;text-decoration:none;text-align:center;flex:none;padding:9px 14px;color:#f7e3bc;font-size:11px;letter-spacing:.06em;font-weight:850;border:1px solid transparent;border-radius:3px}.nav a:hover,.nav a:focus-visible{border-color:#eac480;background:#2a2a32}.intro{background:radial-gradient(circle at 75% 0%,#182c42,#0b1726 60%);padding:55px var(--side) 60px;display:grid;gap:22px;grid-template-columns:minmax(0,1fr) minmax(270px,.75fr)}.intro h2{font-size:clamp(29px,4.5vw,58px);line-height:1.22;margin:13px 0 18px;letter-spacing:-.05em}.intro p{font-size:15px;max-width:600px;color:#e2dee1}.intro-side{border-left:2px solid #bb945d;padding:20px 0 16px 22px;align-self:center}.intro-side strong{display:block;font-size:22px;color:#f9dea1}.intro-side p{font-size:13px}.episodes{background:#ebe0c5;color:#161e2c;padding:28px var(--side) 42px}.section-heading{font-family:Georgia,serif;font-size:clamp(29px,4.3vw,52px);line-height:1.1;margin:5px 0 19px;font-weight:900}.section-heading span{color:#a72957}.episode-strip{display:flex;gap:9px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:10px}.episode{scroll-snap-align:start;flex:0 0 clamp(176px,20vw,237px);background:#121b2b;color:#fff;overflow:hidden;position:relative;min-height:300px;border:1px solid #a9a297}.episode>img,.ep-art{width:100%;height:156px;object-fit:cover}.episode-copy{padding:14px 13px 18px}.episode-copy b{display:block;font:900 18px Georgia,serif;color:#edcf94}.episode-copy strong{font-size:13px;display:block;line-height:1.55;margin-top:3px}.episode-copy p{font-size:11px;line-height:1.6;color:#d5d5d9;margin:8px 0}.episode-copy a{font-size:10px;color:#f7d79a}.stage{background:var(--parchment);color:var(--ink);border-top:9px solid #061527;padding-bottom:32px}.stage-banner{background:linear-gradient(110deg,#091829,#202335 80%);padding:20px var(--side);color:#fff}.stage-banner span{font-size:12px;font-weight:900;letter-spacing:.15em;color:#e8bc73}.stage-banner h2{font-family:Georgia,'Times New Roman',serif;font-size:clamp(45px,7vw,86px);line-height:1;margin:10px 0;color:#f0cc83;letter-spacing:-.055em}.stage-banner p{font-size:13px;color:#fff;margin:4px 0;font-weight:750}.stage-top{display:grid;grid-template-columns:1.16fr 1fr;min-height:280px}.stage-top>img,.place-gradient{width:100%;height:390px;object-fit:cover}.stage-intro{padding:37px var(--side);display:flex;flex-direction:column;justify-content:center;background:#f4e8d1}.small-label{font-size:10px;font-weight:900;letter-spacing:.17em;color:#9b4b61}.stage-intro h3{font-size:clamp(22px,3vw,38px);line-height:1.25;letter-spacing:-.04em;margin:14px 0}.stage-intro p{font-size:14px}.mapbtn{display:inline-block;align-self:start;background:#0c2537;color:#f6d8a1;padding:10px 16px;border-radius:4px;margin-top:12px;font-size:12px;text-decoration:none;font-weight:900;min-height:44px}.stage-body{display:grid;grid-template-columns:.84fr 1.16fr;gap:0}.stops{padding:30px var(--side);background:#f0e3c8}.scenes{padding:30px var(--side) 10px;background:#e7d7b9}.subhead{font-size:20px;margin:0 0 19px;font-weight:950}.stops ol{padding-left:26px}.stops li{padding:10px 0;font-weight:750;line-height:1.6}.relation{border-left:3px solid #be6c8e;background:#fff8eb;padding:13px 16px;margin:11px 0}.relation span{font-size:11px;font-weight:900;color:#90325e}.relation p{font-size:13px;margin:4px 0}.relation a{font-size:11px;color:#63345b}.scene{margin:0 0 22px;border:1px solid #baab90;background:#fff8e9;overflow:hidden}.scene-visual{position:relative;background:#151b2d}.scene-visual img,.scene-placeholder{width:100%;height:235px;object-fit:cover}.picture-note{font-size:10px;position:absolute;right:8px;bottom:7px;background:#091527cd;padding:4px 7px;color:#fff}.scene-copy{padding:18px}.scene-copy h4{font-size:22px;margin:7px 0;line-height:1.4}.scene-copy p{font-size:13px}.scene-copy a{font-size:11px;color:#93506b}.spoiler{padding:14px 15px}.spoiler summary{cursor:pointer;font-size:13px;font-weight:900}.spoiler .scene-copy{padding:10px 0 0}.utility{display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:1px solid #b6a78d}.utility>div{padding:23px var(--side)}.utility>div+div{background:#f7eddc}.utility h3{font-size:18px;margin:5px 0 15px}.time-row{display:flex;gap:15px;align-items:baseline;padding:9px 0;border-bottom:1px solid #cabda7;font-size:13px}.time-row b{font-family:Georgia,serif;min-width:60px}.mission{display:flex;align-items:flex-start;gap:10px;font-size:13px;padding:10px 0;cursor:pointer;min-height:44px}.mission input{accent-color:#ab476f;width:20px;height:20px;margin-top:4px}.mission input:checked+span{text-decoration:line-through;color:#857e73}.sources{background:#0c1625;padding:40px var(--side) 55px;color:#dfd9d4}.sources h2{color:#f0ce92;font-size:22px}.sources li{margin:7px 0;font-size:13px;word-wrap:break-word}.sources a{color:#e2c595}.note{font-size:11px;color:#b7bcc2;max-width:800px}.footer{border-top:1px solid #92764f;text-align:center;padding:22px;background:#070e18;font-size:10px;letter-spacing:.12em;color:#d4b986}@media(max-width:680px){.hero{height:78svh;min-height:500px;max-height:740px}.hero-picture{object-position:66% 50%}.hero:after{background:linear-gradient(90deg,#061226bd,#06172a50 70%),linear-gradient(0deg,#061125e8 2%,transparent 71%)}.hero-inner{padding:19px 22px 44px}.hero-top{font-size:9px}.hero-head h1{font-size:clamp(48px,12.8vw,83px);line-height:.87;letter-spacing:-.07em}.hero-head .subtitle{font-size:16px}.intro{display:block;padding:34px 22px}.intro-side{margin-top:28px}.episodes{padding:29px 15px}.episode{flex-basis:64vw;max-width:256px}.stage-top,.stage-body,.utility{display:block}.stage-top>img,.place-gradient{height:260px}.stage-intro,.stops,.scenes,.utility>div{padding:24px 21px}.stage-banner{padding:17px 21px}.stage-banner h2{font-size:clamp(41px,11vw,70px)}.scene-visual img,.scene-placeholder{height:230px}.nav{padding:5px 9px}.nav a{padding:10px 11px}.sources{padding:29px 21px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
</style></head><body><main><header class="hero" id="intro">@@HERO@@<div class="hero-inner"><div class="hero-top"><span>STORY PILGRIMAGE / FIELD EDITION</span><span class="edition">@@REGION@@<br>@@DATES@@</span></div><div class="hero-head"><div class="eyebrow">YOUR JOURNEY IS A STORY</div><h1>@@TITLE_TEXT@@</h1><div class="subtitle">@@SUBTITLE@@</div><div class="dates">@@DATES@@</div></div></div></header><nav class="nav" aria-label="ページ内案内">@@NAV@@</nav><section class="intro"><div><div class="eyebrow">THE STORY / HOW TO READ THIS JOURNEY</div><h2>いつもの観光を、<br>物語の中へ。</h2><p>この旅の主役は「@@PRIMARY@@」。舞台、名場面、伝説と実景を、実際に歩く順番でひもときます。作品を知らなくても楽しめるように、エピソードと歴史を一緒に紹介します。</p></div><div class="intro-side"><strong>現地 × 物語 × 記憶</strong><p>創作イラストは物語の雰囲気を描いたものです。実際の景観を示す写真や、作品の公式場面画像ではありません。</p></div></section><section class="episodes" id="episodes"><div class="eyebrow" style="color:#a52952">SCENE & EPISODE GUIDE</div><h2 class="section-heading">物語を<span>思い出す。</span></h2><div class="episode-strip">@@EPISODES@@</div></section>@@STAGES@@<section class="sources" id="sources"><h2>出典と制作ノート</h2><p class="note">各作品と実在の場所との関係は、掲載した根拠の範囲に限定しています。現地の営業時間や入場方法は変わることがあります。旅程は仲間向けの抜粋で、予約番号・座席・連絡先などを含みません。</p><ul>@@SOURCES@@</ul><p class="note">メディア権利メモ：@@MEDIA_NOTES@@。このガイドは公式作品とは無関係のファン向け非公式ガイドです。公開・転載の権利を保証するものではありません。</p></section><footer class="footer">STORY PILGRIMAGE · MADE FOR YOUR JOURNEY</footer></main><script>
(function(){const checks=[...document.querySelectorAll('[data-mission]')];for(const box of checks){const key='sp-check:'+box.dataset.mission;try{box.checked=localStorage.getItem(key)==='1'}catch(e){}box.addEventListener('change',()=>{try{localStorage.setItem(key,box.checked?'1':'0')}catch(e){}})}})();
</script></body></html>'''
    replacements = {"@@TITLE@@": H(meta["title"]), "@@HERO@@": img, "@@TITLE_TEXT@@": H(meta["title"]), "@@SUBTITLE@@": H(meta.get("subtitle", "")), "@@REGION@@": H(meta.get("regions", "")), "@@DATES@@": H(meta.get("dates", "")), "@@PRIMARY@@": H(primary["title"]), "@@NAV@@": nav, "@@EPISODES@@": eps, "@@STAGES@@": stages, "@@SOURCES@@": srcs, "@@MEDIA_NOTES@@": H(asset_notes)}
    for a, b in replacements.items():
        out = out.replace(a, b)
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("guide_json", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    data = json.loads(a.guide_json.read_text(encoding="utf-8"))
    result = render(data, root)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(result, encoding="utf-8")
    print(f"Rendered {len(result.encode('utf-8')):,} bytes -> {a.out}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, RuntimeError) as e:
        sys.exit("ERROR: " + str(e))
