import argparse
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
html_source=render(json.loads((ROOT/'examples/egypt_guide.json').read_text(encoding='utf-8')),ROOT)
ballot_source=make(json.loads((ROOT/'examples/egypt_candidates.json').read_text(encoding='utf-8')))

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width,height in [(390,844),(430,932),(1280,800)]:
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto('about:blank')
        page.set_content(html_source,wait_until='load')
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
        # about:blank has no stable storage origin; storage persistence requires a served URL in real usage
        page.locator('#episodes').scroll_into_view_if_needed()
        page.screenshot(path=str(OUT/f'story_pilgrimage_{width}_episodes.png'),full_page=False)
        print(f'guide {width}: overflow={overflow}; embedded images={len(image_stats)}; interactions=PASS')
        page.close()
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
