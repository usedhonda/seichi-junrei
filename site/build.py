"""Build the public sample with the same renderer installed with the skill."""
import argparse
import json
import sys
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1] / 'plugins/seichi-junrei'
sys.path.insert(0, str(PLUGIN / 'scripts'))
from render_guide import render

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    guide = json.loads((PLUGIN / 'examples/egypt_guide.json').read_text(encoding='utf-8'))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render(guide, PLUGIN), encoding='utf-8')
    print(f'Built {args.out} with the installed-skill renderer')
