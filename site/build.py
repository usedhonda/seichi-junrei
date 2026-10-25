"""Build the recovered public booklet as one offline-capable HTML file."""
import argparse
import base64
import json
from pathlib import Path


def build(out):
    root = Path(__file__).resolve().parent
    content = json.loads((root / 'content.json').read_text())
    source = content['template']
    source = source.replace('@@CSS@@', (root / 'app.css').read_text())
    source = source.replace('@@DATA@@', json.dumps(content['guide'], ensure_ascii=False).replace('</', '<\\/'))
    source = source.replace('@@JS@@', (root / 'app.js').read_text())
    for key, asset in json.loads((root / 'media.json').read_text()).items():
        data = base64.b64encode((root / asset['path']).read_bytes()).decode('ascii')
        source = source.replace('@@ART_' + key + '@@', 'data:' + asset['mime'] + ';base64,' + data)
    target = Path(out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source, encoding='utf-8')
    print(f'Built {target} ({target.stat().st_size} bytes)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    build(parser.parse_args().out)
