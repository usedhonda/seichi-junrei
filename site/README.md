# Public skill samples

`build.py` renders the canonical `plugins/seichi-junrei/examples/egypt_guide.json`
with the same renderer, CSS and runtime shipped inside the plugin.
The workflow also renders `oxford_alice_guide.json` to `/alice/`.

Edit the canonical example JSON and its local assets to change the public guide.
`site/content.json`, `media.json`, `app.css`, `app.js` and `assets/` retain the
recovered original source as provenance; they are not the active production engine.
The old one-time ZIP/importer remains available only for archive recovery.

Build: `python site/build.py --out _site/index.html`
