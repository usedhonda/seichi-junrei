#!/usr/bin/env python3
"""Make a portable offline candidate ballot. It cannot replace explicit user choice."""
import argparse
import html
import json
from pathlib import Path
from rank_candidates import rank

def esc(x):
    return html.escape(str(x), quote=True)

def make(data):
    options = rank(data)
    cards = []
    for c in options:
        urls = " ".join(f'<a target="_blank" rel="noopener" href="{esc(u)}">出典 ↗</a>'
                        for u in c.get("evidence_urls", []) if u.startswith("https://"))
        cards.append(f'''<article class="card" data-id="{esc(c['id'])}"><div class="cover"><span class="chip">{esc(c.get('medium',''))}</span><strong>{esc(c['title'])}</strong><span class="grade">関連度 {esc(c['connection_grade'])}</span></div><div class="body"><p>{esc(c.get('why',''))}</p><blockquote>{esc(c.get('scene',''))}</blockquote><div class="fine">{esc(c.get('caveat',''))}</div><div class="evidence">{urls}</div><label><input type="radio" name="primary" value="{esc(c['id'])}">主役にする</label><label><input type="checkbox" name="secondary" value="{esc(c['id'])}">寄り道として追加</label></div></article>''')
    return '''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>物語を選ぶ | Seichi Junrei</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#0d1120;color:#f7ead8;font-family:system-ui,-apple-system,'Noto Sans JP',sans-serif}main{max-width:970px;margin:auto;padding:28px 16px 120px}.top{font:800 12px system-ui;color:#eec47c;letter-spacing:.19em}h1{font-size:clamp(30px,7vw,60px);letter-spacing:-.04em;line-height:1.2}p{line-height:1.85}.sub{color:#bbbed0}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:15px}.card{background:#1b2234;border:1px solid #555a69;border-radius:18px;overflow:hidden}.cover{min-height:150px;padding:20px;background:radial-gradient(circle at 80% 10%,#4b4771,transparent 50%),linear-gradient(125deg,#34233c,#0c2139);display:flex;flex-direction:column;gap:8px}.cover strong{font-size:24px;line-height:1.2}.chip{font-size:11px;color:#f5c47d;font-weight:900}.grade{font-size:11px;color:#d3d4dc}.body{padding:16px}blockquote{padding-left:14px;border-left:3px solid #e1bb7b;line-height:1.7;margin:10px 0}.fine{font-size:12px;color:#cfbdc7}.evidence{display:flex;gap:10px;margin:14px 0}.evidence a{color:#e8d097;font-size:12px}.body label{min-height:45px;display:flex;align-items:center;gap:10px;font-size:14px;font-weight:700}input{width:21px;height:21px;accent-color:#f6c577}.bar{position:sticky;bottom:0;background:#101827eF;padding:16px;margin:24px -16px -120px;display:flex;gap:10px;align-items:center;flex-wrap:wrap;backdrop-filter:blur(10px)}button{border:0;border-radius:12px;background:#f4ce81;color:#17151d;padding:13px 20px;font-weight:900;cursor:pointer}.status{color:#c4c7d0;font-size:12px}pre{white-space:pre-wrap;word-wrap:break-word;font-size:12px;color:#dfead2}</style></head><body><main><div class="top">SEICHI JUNREI / SELECT YOUR STORY</div><h1>この旅の主役を、<br>選んでください。</h1><p class="sub">おすすめ順に並んでいますが、決めるのはあなた。主役を1つ、寄り道を最大2つ。候補の下に関連性と出典があります。</p><div class="cards">''' + "".join(cards) + '''</div><div class="bar"><button id="copy">選択内容をコピー</button><span class="status" id="status">選ぶまでは本編を作りません</span></div><pre id="result"></pre></main><script>
const $=s=>document.querySelector(s);$('#copy').onclick=async()=>{const main=document.querySelector('input[name="primary"]:checked');if(!main){$('#status').textContent='主役を1つ選んでください';return;}const extra=Array.from(document.querySelectorAll('input[name="secondary"]:checked')).map(e=>e.value).filter(x=>x!==main.value);if(extra.length>2){$('#status').textContent='寄り道は2つまで';return;}const obj={primary_work_id:main.value,secondary_work_ids:extra,user_confirmed:true,delegated:false};const s=JSON.stringify(obj);$('#result').textContent=s;try{await navigator.clipboard.writeText(s);$('#status').textContent='コピーしました。ChatGPTに貼り付けてください';}catch(e){$('#status').textContent='下の選択内容をコピーしてChatGPTに送ってください';}};
</script></body></html>'''

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("json_file", type=Path)
    p.add_argument("--out", required=True, type=Path)
    a=p.parse_args()
    x=make(json.loads(a.json_file.read_text(encoding="utf-8")))
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(x,encoding="utf-8")
    print(f"Ballot HTML: {a.out}")

if __name__ == "__main__":
    main()
