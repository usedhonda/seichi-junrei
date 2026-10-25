"""Exercise the actual Pages artifact using the installed-skill acceptance test."""
import runpy
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
html = Path(sys.argv[1]).resolve()
plugin = root / 'plugins/seichi-junrei'
sys.argv = [str(plugin/'tests/browser_check.py'), '--guide', str(plugin/'examples/egypt_guide.json'), '--html', str(html), '--outdir', str(root/'checks/pages')]
runpy.run_path(str(plugin/'tests/browser_check.py'), run_name='__main__')
