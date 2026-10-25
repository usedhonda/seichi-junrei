"""One-time import of the reviewed public sample; never overwrite an existing site."""
import hashlib
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

EXPECTED = '9d609a4a90871f2e7e395ce5d8c504fd740851edb1f6123ebd992f3922245513'
ASSETS = ('abu', 'anubis', 'aswan', 'boingo', 'brothers', 'hero', 'iggy', 'ndoul', 'tobacco')
ALLOWED = {'site/'+name for name in ('README.md', 'app.css', 'app.js', 'build.py', 'content.json', 'media.json')}
ALLOWED.update('site/assets/'+name+'.webp' for name in ASSETS)

def import_bundle(archive, root):
    archive, root = Path(archive), Path(root).resolve()
    if (root/'site').exists():
        raise ValueError('site/ already exists; edit the tracked source instead of importing again')
    if hashlib.sha256(archive.read_bytes()).hexdigest() != EXPECTED:
        raise ValueError('Archive does not match the reviewed public sample')
    with zipfile.ZipFile(archive) as z:
        entries = z.infolist()
        if len(entries) != len(ALLOWED) or {x.filename for x in entries} != ALLOWED:
            raise ValueError('Unexpected or duplicate archive path')
        if sum(x.file_size for x in entries) > 10_000_000:
            raise ValueError('Archive too large')
        payloads = []
        for item in entries:
            path = PurePosixPath(item.filename)
            if path.is_absolute() or '..' in path.parts or stat.S_ISLNK(item.external_attr >> 16):
                raise ValueError('Unsafe archive entry')
            content = z.read(item)
            destination = (root/item.filename).resolve()
            if not destination.is_relative_to(root):
                raise ValueError('Path outside repository')
            payloads.append((destination, content))
        for destination, content in payloads:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
    print(f'Imported {len(payloads)} reviewed public files into site/')

if __name__ == '__main__':
    import_bundle(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else '.')
