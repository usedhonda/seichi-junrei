"""Exercise a non-showcase journey from a runtime without examples or sample art."""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from journey_fixture import independent_input

ROOT=Path(__file__).resolve().parents[1]

def check(out,executable=None):
    out=out.resolve();out.mkdir(parents=True,exist_ok=True)
    data=independent_input(ROOT)
    (out/'independent-trip.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    with tempfile.TemporaryDirectory(prefix='journey-portability-') as temp:
        base=Path(temp);runtime=base/'runtime';trip=base/'trip';trip.mkdir()
        shutil.copytree(ROOT/'scripts',runtime/'scripts',ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT/'assets/mobile-guide',runtime/'assets/mobile-guide')
        (runtime/'tests').mkdir();shutil.copy2(ROOT/'tests/browser_check.py',runtime/'tests/browser_check.py')
        for media in data['media_rights']:
            target=trip/media['file'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/media['file'],target)
        spec=trip/'independent-trip.json';spec.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
        html=out/'independent-trip.html'
        subprocess.run([sys.executable,str(runtime/'scripts/render_guide.py'),str(spec),'--assets-root',str(trip),'--out',str(html)],cwd=trip,check=True)
        subprocess.run([sys.executable,str(runtime/'scripts/lint_guide.py'),str(html),'--guide',str(spec)],cwd=trip,check=True)
        args=[sys.executable,str(runtime/'tests/browser_check.py'),'--guide',str(spec),'--assets-root',str(trip),'--html',str(html),'--width','390','--outdir',str(out/'checks')]
        if executable:args+=['--executable',executable]
        subprocess.run(args,cwd=trip,check=True)
    print('PASS: independent input, external artwork, no examples or sample art in runtime')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--outdir',type=Path,default=Path.cwd()/'checks/portability')
    parser.add_argument('--executable')
    args=parser.parse_args();check(args.outdir,args.executable)
