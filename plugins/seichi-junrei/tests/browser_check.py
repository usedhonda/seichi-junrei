import argparse
import copy
import os
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from render_guide import render
from make_ballot import make
p=argparse.ArgumentParser()
p.add_argument('--outdir',type=Path,default=ROOT/'checks')
args=p.parse_args()
OUT=args.outdir
OUT.mkdir(parents=True,exist_ok=True)
spec=json.loads((ROOT/'examples/egypt_guide.json').read_text(encoding='utf-8'))
html_source=render(spec,ROOT)
ballot_source=make(json.loads((ROOT/'examples/egypt_candidates.json').read_text(encoding='utf-8')))

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True, **({'executable_path':os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}))
    for width,height in [(390,844),(430,932),(1280,800)]:
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.route('https://guide.test/**', lambda route: route.fulfill(content_type='text/html', body=html_source))
        page.goto('https://guide.test/trip',wait_until='load')
        page.locator('.hero img').wait_for()
        page.screenshot(path=str(OUT/f'story_pilgrimage_{width}_top.png'),full_page=False)
        page.locator('#stage-aswan').scroll_into_view_if_needed()
        page.screenshot(path=str(OUT/f'story_pilgrimage_{width}_aswan.png'),full_page=False)
        image_stats=page.locator('img').evaluate_all('(els)=>els.map(e=>({ok:e.complete&&e.naturalWidth>0,w:e.naturalWidth}))')
        overflow=page.evaluate('document.documentElement.scrollWidth - innerWidth')
        assert overflow<=1,(width,overflow)
        assert all(x['ok'] for x in image_stats), (width,image_stats)
        assert not errors, errors
        page.locator('[data-mission]').first.check()
        assert page.locator('[data-mission]').first.is_checked()
        total=page.locator('[data-mission]').count()
        assert page.locator('#mission-count').inner_text()==f'1 / {total} ミッション達成'
        page.reload()
        assert page.locator('[data-mission]').first.is_checked()
        assert page.locator('#mission-meter').get_attribute('value')=='1'
        page.locator('#episodes').scroll_into_view_if_needed()
        page.screenshot(path=str(OUT/f'story_pilgrimage_{width}_episodes.png'),full_page=False)
        print(f'guide {width}: overflow={overflow}; embedded images={len(image_stats)}; interactions=PASS')
        page.close()
    # A distinct trip on the same origin must not inherit another trip's checks.
    context=browser.new_context()
    page=context.new_page()
    other=copy.deepcopy(spec)
    other['meta']['dates']='A different trip'
    other_html=render(other,ROOT)
    page.route('https://guide.test/**',lambda route: route.fulfill(content_type='text/html',body=other_html if route.request.url.endswith('/other') else html_source))
    page.goto('https://guide.test/first')
    page.locator('[data-mission]').first.check()
    page.goto('https://guide.test/other')
    assert not page.locator('[data-mission]').first.is_checked()
    page.goto('https://guide.test/first')
    assert page.locator('[data-mission]').first.is_checked()
    context.close()
    # Real browser Storage exceptions: checklist stays interactive and reports fallback.
    context=browser.new_context()
    context.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError')}})")
    page=context.new_page()
    page.route('https://guide.test/**',lambda route: route.fulfill(content_type='text/html',body=html_source))
    page.goto('https://guide.test/blocked')
    page.locator('[data-mission]').first.check()
    assert page.locator('#mission-meter').get_attribute('value')=='1'
    assert '保存できません' in page.locator('#storage-status').inner_text()
    context.close()
    print('storage: reload, same-origin trip isolation and denied-storage fallback=PASS')
    page=browser.new_page(viewport={'width':390,'height':844})
    err=[]
    page.on('pageerror',lambda e:err.append(str(e)))
    page.goto('about:blank')
    page.set_content(ballot_source,wait_until='load')
    page.screenshot(path=str(OUT/'story_pilgrimage_ballot.png'),full_page=False)
    page.locator('input[name="primary"]').first.check()
    page.locator('input[name="secondary"]').nth(1).check()
    page.locator('#copy').click()
    result=page.locator('#result').inner_text()
    assert '"primary_work_id":"jojo-3"' in result,result
    assert '"secondary_work_ids":["death-nile-1978"]' in result,result
    assert not err,err
    print('ballot: primary and secondary selection=PASS')
    browser.close()
