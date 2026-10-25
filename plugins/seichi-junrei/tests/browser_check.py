"""Behavioral acceptance for any guide made by the installed renderer.

Serves a real HTTP origin; tests persisted state separately from blocked storage.
Run this file from an isolated copy of the plugin to prove packaging is complete.
"""
import argparse
import functools
import http.server
import json
import os
import shutil
import sys
import tempfile
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_guide import render


def check(specs, out, executable=None, html_file=None, assets_root=None, widths=(360, 390, 430, 520)):
    out.mkdir(parents=True, exist_ok=True)
    records = []
    with tempfile.TemporaryDirectory() as directory:
        pages = Path(directory)
        for spec in specs:
            data = json.loads(spec.read_text(encoding='utf-8'))
            source = html_file.read_text(encoding='utf-8') if html_file and spec == specs[0] else render(data, assets_root or ROOT)
            (pages / (spec.stem+'.html')).write_text(source, encoding='utf-8')
        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *args): pass
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=directory))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            with sync_playwright() as pw:
                options = {'headless': True}
                if executable: options['executable_path'] = executable
                browser = pw.chromium.launch(**options)
                for spec in specs:
                    url = f'http://127.0.0.1:{server.server_port}/{spec.stem}.html'
                    for width in widths:
                        context = browser.new_context(viewport={'width': width, 'height': 900}, has_touch=True, reduced_motion='reduce', accept_downloads=True)
                        # Background tiles are a live service; CI checks maps without fetching them.
                        context.route('https://tile.openstreetmap.org/**', lambda route: route.abort())
                        page = context.new_page()
                        errors = []
                        page.on('pageerror', lambda e: errors.append(str(e)))
                        page.goto(url, wait_until='load')
                        page.wait_for_function('window.__pilgrimage && document.documentElement.classList.contains("checklists-ready")')
                        payload = page.locator('#guide-data').text_content()
                        data = json.loads(payload)
                        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
                        assert len(data['stages']) == len(json.loads(spec.read_text())['stages'])
                        mission = data['missions'][0]
                        stage = data['stages'][0]
                        total = len(data['missions'])
                        local_total = sum(m['stage'] == stage['id'] for m in data['missions'])
                        home_input = page.locator('#home [data-mission]').first
                        home_input.locator('..').locator('..').tap()
                        assert page.locator('#home [data-mission-count]').inner_text() == f'旅全体 1 / {total} 完了'
                        page.locator(f'.bottom-nav a[href="#{stage["id"]}"]').tap()
                        assert page.locator(f'#{stage["id"]} [data-mission-count]').inner_text() == f'{stage["label"]} 1 / {local_total} 完了'
                        assert page.locator(f'#{stage["id"]} [data-mission]').first.is_checked()
                        page.locator(f'[data-bookmark="{stage["id"]}"]').tap()
                        page.locator('.bottom-nav a[href="#home"]').tap()
                        page.reload(wait_until='load')
                        page.wait_for_function('window.__pilgrimage')
                        assert page.locator('#home [data-mission-count]').inner_text() == f'旅全体 1 / {total} 完了'
                        assert page.locator(f'[data-bookmark="{stage["id"]}"]').get_attribute('aria-pressed') == 'true'
                        # Nonnumeric story IDs and endpoints must navigate by array position.
                        page.locator('#home [data-episode]').first.tap()
                        assert page.locator('#sheet').is_visible()
                        assert not page.locator('#sheet [data-ep-step="-1"]').is_enabled()
                        if len(data['episodes']) > 1:
                            page.locator('#sheet [data-ep-step="1"]').tap()
                            assert data['episodes'][1]['title'] in page.locator('#sheet-content').inner_text()
                        page.locator('#sheet [data-full]').tap()
                        assert page.locator('#artbox').is_visible()
                        page.keyboard.press('Escape')
                        assert not page.locator('#artbox').is_visible()
                        page.keyboard.press('Escape')
                        assert not page.locator('#sheet').is_visible()
                        for ep in data['episodes']:
                            if ep.get('spoiler'):
                                page.locator(f'#home [data-episode="{ep["id"]}"]').tap()
                                page.locator('#sheet details summary').tap()
                                assert page.locator('#sheet details').get_attribute('open') is not None
                                page.keyboard.press('Escape')
                                break
                        # A short rail can fit entirely at a wider viewport.
                        overflow = page.eval_on_selector('#home-episodes', 'e=>e.scrollWidth > e.clientWidth+1')
                        if len(data['episodes']) > 1 and overflow:
                            page.locator('[data-rail="home-episodes"] button').last.tap()
                            page.wait_for_function('document.querySelector("#home-episodes").scrollLeft > 0')
                        for destination in data['stages']:
                            page.locator(f'.bottom-nav a[href="#{destination["id"]}"]').tap()
                            page.wait_for_function('(id) => document.querySelector("#"+id+".active") && scrollY===0', arg=destination['id'])
                            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
                            page.locator(f'#{destination["id"]} [data-scene]').first.tap()
                            assert page.locator('#sheet .dialog-image').get_attribute('src').startswith('data:image/')
                            page.keyboard.press('Escape')
                        page.locator('.bottom-nav a[href="#route"]').tap()
                        if page.locator('#journey-map').count():
                            page.wait_for_function('document.querySelector("#journey-map").dataset.mapReady==="true"')
                            page.locator('[data-map-view="all"]').tap()
                            map_data = json.loads(page.locator('#route-map-data').text_content())
                            assert page.locator('.route-pin').count() == len(map_data['stops'])
                            page.locator('[data-map-view="day"]').tap()
                        tabs = page.locator('[data-day]')
                        tabs.last.tap()
                        last = tabs.last.get_attribute('data-day')
                        assert page.locator(f'[data-day-panel="{last}"]').is_visible()
                        tabs.last.press('Home')
                        first = tabs.first.get_attribute('data-day')
                        assert page.locator(f'[data-day-panel="{first}"]').is_visible()
                        if page.locator('#journey-map').count():
                            page.wait_for_function('(id)=>document.querySelector("[data-map-caption]").textContent.startsWith("DAY "+id)', arg=first)
                            page.locator('.map-stop [data-map-stop]').first.tap()
                            assert page.locator('.leaflet-popup').is_visible()
                            assert 'https://www.google.com/maps/' in page.locator('.map-popup a').last.get_attribute('href')
                        page.locator('[data-action="motion"]').tap()
                        assert page.locator('body').get_attribute('data-motion') == 'off'
                        with page.expect_download() as saved:
                            page.locator('[data-action="save"]').tap()
                        download = saved.value
                        saved_path = out / (spec.stem+'-offline.html')
                        download.save_as(saved_path)
                        # Saved file keeps a pristine home view, embedded artwork and working runtime.
                        offline = context.new_page()
                        offline.goto(saved_path.resolve().as_uri())
                        offline.wait_for_function('window.__pilgrimage')
                        assert offline.locator('#home').is_visible()
                        offline.close()
                        page.locator('.bottom-nav a[href="#home"]').tap()
                        page.eval_on_selector_all('img[data-art]', 'els=>els.forEach(e=>e.loading="eager")')
                        page.wait_for_function('[...document.querySelectorAll("img[data-art]")].every(e=>e.complete&&e.naturalWidth>0)')
                        if width == 390:
                            page.goto(url, wait_until='load')
                            page.wait_for_function('window.__pilgrimage && scrollY===0')
                            page.screenshot(path=str(out / (spec.stem+'-cover.png')))
                            page.locator(f'.bottom-nav a[href="#{stage["id"]}"]').tap()
                            page.wait_for_function('(id)=>document.querySelector("#"+id+".active")&&scrollY===0', arg=stage['id'])
                            page.screenshot(path=str(out / (spec.stem+'-destination.png')))
                            page.locator(f'#{stage["id"]} [data-scene]').first.tap()
                            page.screenshot(path=str(out / (spec.stem+'-detail.png')))
                        assert not errors, errors
                        records.append({'guide': spec.name, 'width': width, 'missions': total, 'destinations': len(data['stages']), 'result': 'PASS'})
                        context.close()
                    # Read/write denial must leave fully usable controls and an honest notice.
                    context = browser.new_context(viewport={'width': 390, 'height': 900}, has_touch=True)
                    context.add_init_script('Object.defineProperty(window,"localStorage",{get(){throw new DOMException("Blocked","SecurityError")}})')
                    page = context.new_page()
                    page.goto(url)
                    page.wait_for_function('window.__pilgrimage')
                    page.locator('#home [data-mission]').first.check()
                    assert '1 /' in page.locator('#home [data-mission-count]').inner_text()
                    assert '再読み込み後の保存ができません' in page.locator('#home [data-mission-storage]').inner_text()
                    context.close()
                # Guides on the same origin must not inherit each other's progress.
                if len(specs) > 1:
                    context = browser.new_context()
                    page = context.new_page()
                    page.goto(f'http://127.0.0.1:{server.server_port}/{specs[0].stem}.html')
                    page.locator('#home [data-mission]').first.check()
                    page.goto(f'http://127.0.0.1:{server.server_port}/{specs[1].stem}.html')
                    page.wait_for_function('window.__pilgrimage')
                    assert not page.locator('#home [data-mission]').first.is_checked()
                    context.close()
                browser.close()
        finally:
            server.shutdown()
    (out / 'acceptance.json').write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--guide', type=Path, action='append')
    parser.add_argument('--assets-root', type=Path, help='Local assets for a supplied trip')
    parser.add_argument('--html', type=Path, help='Test this built artifact for the first guide')
    parser.add_argument('--outdir', type=Path, default=ROOT / 'checks')
    parser.add_argument('--executable', default=os.environ.get('CHROMIUM_EXECUTABLE'))
    parser.add_argument('--width', type=int, action='append', help='Focused viewport rerun; default tests 360/390/430/520px')
    args = parser.parse_args()
    check(args.guide or [ROOT/'examples/egypt_guide.json', ROOT/'examples/conan_singapore_guide.json', ROOT/'examples/monster_europe_guide.json'], args.outdir, args.executable, args.html, args.assets_root, args.width or (360, 390, 430, 520))
