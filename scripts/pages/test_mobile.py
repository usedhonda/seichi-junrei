"""Browser regression gate for the public character-art mobile sample."""
import functools
import http.server
import json
import re
import shutil
import sys
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

page_file = Path(sys.argv[1]).resolve()
source = page_file.read_text(encoding='utf-8')
in_memory = '--in-memory' in sys.argv
visible_source = re.sub(r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+', '', source)
for pattern in (r'(?i)\b(?:PNR|booking reference|予約番号)\s*[:：#=]\s*[A-Z0-9-]{5,}',
                r'[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', r'\bMS\s*\d{2,4}\b'):
    assert not re.search(pattern, visible_source), 'Possible private itinerary found'
assert 'noindex,nofollow,noarchive' in source
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(page_file.parent)))
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}/{page_file.name}'
reports = []
try:
    with sync_playwright() as pw:
        options = {'headless': True}
        if shutil.which('chromium'): options['executable_path'] = shutil.which('chromium')
        browser = pw.chromium.launch(**options)
        for width in (360, 390, 430, 520):
            context = browser.new_context(viewport={'width': width, 'height': 900}, has_touch=True, reduced_motion='reduce')
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            if in_memory: page.set_content(source, wait_until='load')
            else: page.goto(url, wait_until='load')
            page.wait_for_function('window.__stardust && document.documentElement.classList.contains("checklists-ready")')
            assert page.evaluate('window.__stardust.characterArtCount') == 7
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
            page.locator('#home label[for="mission-all-cafe"]').tap()
            assert page.locator('#home [data-mission-count]').inner_text() == '旅全体 1 / 6 完了'
            page.locator('.bottom-nav a[href="#aswan"]').tap()
            assert page.locator('#aswan [data-mission-count]').inner_text() == 'アスワン 1 / 3 完了'
            page.locator('#aswan label[for="mission-aswan-iggy"] .mtext').tap()
            page.locator('#aswan label[for="mission-aswan-sail"]').tap(position={'x': 14, 'y': 22})
            assert page.locator('#aswan [data-mission-count]').inner_text() == 'アスワン 3 / 3 完了'
            page.locator('.bottom-nav a[href="#abu"]').tap()
            assert page.locator('#abu [data-mission-count]').inner_text() == 'アブ・シンベル 0 / 3 完了'
            for ident in ('statues', 'book', 'small'):
                page.locator(f'#abu label[for="mission-abu-{ident}"]').tap()
            page.locator('.bottom-nav a[href="#home"]').tap()
            assert page.locator('#home [data-mission-count]').inner_text() == '旅全体 6 / 6 完了'
            if not in_memory:
                page.reload(wait_until='load')
                page.wait_for_function('window.__stardust')
            assert page.locator('#home [data-mission-count]').inner_text() == '旅全体 6 / 6 完了'
            page.locator('#home label[for="mission-all-cafe"]').tap()
            assert page.locator('#home [data-mission-count]').inner_text() == '旅全体 5 / 6 完了'
            page.locator('#home [data-episode="27"]').tap()
            assert page.locator('#sheet').is_visible()
            assert page.locator('#sheet .dialog-image').get_attribute('src').startswith('data:image/')
            page.locator('#sheet [data-close="sheet"]').tap()
            page.locator('.bottom-nav a[href="#route"]').tap()
            page.locator('[data-day="2"]').tap()
            assert page.locator('#day-2').is_visible() and not page.locator('#day-1').is_visible()
            page.locator('.bottom-nav a[href="#home"]').tap()
            page.eval_on_selector_all('img[data-art]', 'els => els.forEach(e => e.loading="eager")')
            page.wait_for_function('[...document.querySelectorAll("img[data-art]")].every(e => e.complete && e.naturalWidth>0)')
            assert not errors, errors
            reports.append({'width': width, 'touch_and_counts': 'PASS', 'reload_persistence': 'NOT TESTED' if in_memory else 'PASS', 'drawers_and_days': 'PASS', 'character_art': 7})
            context.close()
        browser.close()
finally:
    server.shutdown()
print(json.dumps({'checks': reports, 'physical_iphone_tested': False}, ensure_ascii=False, indent=2))
