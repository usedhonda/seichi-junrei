"""Two sample-specific editorial compositions using the shared control contract.

The templates are examples, not a universal style catalogue. Data stays separate
from layout; the existing runtime owns navigation, storage, dialogs and downloads.
"""


def compose(layout, data, stages, episodes, scenes, missions, primary,
            image, rail, feature, paragraphs, link, mission_group, H, types,
            tabs, panels):
    meta = data['meta']
    case = layout == 'casefile'
    def heading(en, ja):
        return f'<div class="editorial-heading"><span>{H(en)}</span><h2>{H(ja)}</h2></div>'
    def index():
        result = ''
        for i, st in enumerate(stages):
            spec = st['spec']
            result += f'<a class="place-index" href="#{st["id"]}"><span class="index-number">{i+1:02}</span><div><small>{H(spec.get("label", ""))}</small><h3>{H(st["title"])}</h3><p>{H(spec.get("hook", ""))}</p></div><span class="index-arrow">↗</span></a>'
        return result
    def story_list(ident):
        # Vertical, readable story entries replace the default horizontal poster rail.
        return rail(episodes, ident, 'episode')
    count = len(stages)
    def scene_notes(ident):
        return '<div class="scene-notes">'+''.join(
            '<button class="scene-note" data-scene="'+H(s['id'])+'"><small>'+H(s['caption'])+'</small><strong>'+H(s['name'])+'</strong><span>場面を読む →</span></button>'
            for s in scenes if s['stage']==ident)+'</div>'
    credit = '<p class="editorial-credit">'+H(meta.get('art_label', 'AI FAN ART · 非公式'))+' · '+H(meta.get('dates', ''))+'</p>'
    if case:
        cover = f'''<header class="case-cover"><div class="issue-line"><span>SINGAPORE / FIELD NOTES</span><span>FIELD GUIDE</span></div><h1><small>{H(primary["title"])}</small>街に残った、<br><em>手がかり。</em></h1><p class="cover-deck">{H(meta['subtitle'])}</p><figure class="case-portrait">{image(meta['hero_image'], 'hero-art', True)}<figcaption>01—{count:02} / 場面の記憶を、手がかりに。</figcaption></figure>{credit}<a class="editorial-start" href="#{stages[0]['id']}">調査をはじめる <span>↓</span></a></header>'''
        intro = heading('THE BRIEF', '観光名所より、場面の手がかり。')+paragraphs(meta.get('introduction', []))
        home = '<section class="view active" id="home">'+cover+'<section class="editorial-block brief">'+intro+'</section><section class="editorial-block">'+heading('THE CLUES', '今回の調査先。')+index()+'</section><section class="editorial-block story-index">'+heading('SCENE FILES', 'あの場面を、もう一度。')+story_list('home-episodes')+'</section><section class="editorial-block checklist">'+heading('YOUR FIELD NOTES', '見つけたものに、チェック。')+mission_group('all','旅全体',missions)+'</section></section>'
    else:
        cover = f'''<header class="literary-cover"><p class="edition">A JOURNEY THROUGH GERMANY & CZECHIA</p><h1>MONSTER<span>記憶の街を歩く。</span></h1><figure>{image(meta['hero_image'], 'hero-art', True)}<figcaption>TENMA / JOHAN — AN UNOFFICIAL TRAVEL ESSAY</figcaption></figure><p class="literary-deck">大学の窓。ホテルの屋根。<br>見覚えのある街が、<br>静かに物語へとつながる。</p><a class="editorial-start" href="#{stages[0]['id']}">第一章を読む <span>→</span></a>{credit}</header>'''
        home = '<section class="view active" id="home">'+cover+'<section class="editorial-block essay-intro">'+heading('PROLOGUE', 'テンマの旅の、断片を探す。')+paragraphs(meta.get('introduction',[]))+'</section><section class="editorial-block contents">'+heading('CONTENTS / THREE CITIES', '三つの街、三つの記憶。')+index()+'</section><section class="editorial-block story-index">'+heading('READING THE STORY', '旅の前の、小さな読書。')+story_list('home-episodes')+'</section><section class="editorial-block checklist">'+heading('TRAVEL MARGINALIA', '旅の余白に、記録する。')+mission_group('all','旅全体',missions)+'</section></section>'
    story = '<section class="view" id="story"><header class="editorial-page-head">'+heading('SCENE FILES' if case else 'READING NOTES', primary['title'])+'<p>'+H(meta.get('story_intro',''))+'</p></header><section class="editorial-block story-index">'+story_list('story-episodes')+'</section></section>'
    chapters = ''
    for i, st in enumerate(stages):
        spec, ident = st['spec'], st['id']
        title = f'<span class="chapter-number">{("CLUE" if case else "CHAPTER")} {i+1:02}</span><h1>{H(st["title"])}</h1><p class="local-name">{H(st["label"])}</p><p class="chapter-deck">{H(spec.get("hook", ""))}</p>'
        art = feature(spec['image'], 'AI FAN ART · 非公式の創作イラスト')
        if case:
            opening = '<header class="case-chapter">'+title+'</header>'+art
        else:
            opening = '<header class="literary-chapter">'+title+'</header><div class="chapter-plate">'+art+'</div>'
        chapter = f'<section class="view" id="{ident}">'+opening+f'<div class="chapter-tools"><button data-bookmark="{ident}" aria-pressed="false">◇ この章を保存</button><button data-action="share">仲間に渡す ↗</button></div>'
        # Site observations lead Conan's investigation; MONSTER leads with the essay.
        observation = f'<section class="editorial-block observations" id="{ident}-sights">'+heading('LOOK FOR THESE' if case else 'NOTES ON THE PLACE', '現地で探す、細部。' if case else '街に残る、物語の輪郭。')
        for j, sight in enumerate(spec['highlights']):
            item = sight if isinstance(sight,dict) else {'title':sight}
            observation += f'<article class="observation"><span>{j+1:02}</span><div><h3>{H(item["title"])}</h3><p>{H(item.get("description", ""))}</p>'+link(item.get('map_url') or spec.get('map_url'),'地図を開く','map-link')+link(item.get('source_url'),'現地情報の出典')+'</div></article>'
        observation += '</section>'
        narrative = f'<section class="editorial-block chapter-essay" id="{ident}-story">'+heading('THE SCENE' if case else 'STORY / MEMORY',spec.get('story_heading','物語の記憶。'))+paragraphs(spec.get('paragraphs',[]))+scene_notes(ident)+'</section>'
        chapter += observation+narrative if case else narrative+observation
        evidence = '<section class="editorial-block evidence">'+heading('EVIDENCE NOTES' if case else 'SOURCE NOTES','場所と場面の、確かめ方。')
        for rel in spec.get('connections',[]):
            evidence += '<div class="evidence-note"><strong>'+H(types[rel['type']])+'</strong><p>'+H(rel['description'])+'</p>'+link(rel['source_url'],'関係の根拠')+'</div>'
        evidence += '<aside class="practical"><h3>'+H(spec.get('practical_title','訪問のメモ'))+'</h3><p>'+H(spec.get('practical',''))+'</p></aside></section>'
        chapter += evidence+f'<section class="editorial-block checklist" id="{ident}-missions">'+heading('FIELD CHECK' if case else 'MARGINALIA','この街で、覚えておくこと。')+mission_group(ident,st['label'],[m for m in missions if m['stage']==ident])+'</section>'
        if i+1<len(stages):
            nxt=stages[i+1]
            chapter += f'<a class="editorial-next" href="#{nxt["id"]}"><small>{"NEXT CLUE" if case else "NEXT CHAPTER"} / {i+2:02}</small><strong>{H(nxt["title"])}</strong><span>→</span></a>'
        chapters += chapter+'</section>'
    route = '<section class="view" id="route"><header class="editorial-page-head">'+heading('THE DAY PLAN' if case else 'TRAVEL ITINERARY','手がかりをつなぐ、一日。' if case else '街から街へ、余白を残して。')+'<p>'+H(meta.get('regions',''))+'</p></header><div class="day-switch" role="tablist" aria-label="日程">'+tabs+'</div>'+panels+'<p class="info-note">'+H(meta.get('itinerary_note',''))+'</p><section class="editorial-block"><div class="menu-list"><button data-action="save">画像込みで保存 ↓</button><button data-action="share">旅仲間に渡す ↗</button><button data-open="howto">使い方</button><button data-open="sources">出典と制作記録</button><button data-action="motion" aria-pressed="true">ON</button></div></section></section>'
    return home,story,chapters,route
