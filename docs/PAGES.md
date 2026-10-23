# Mobile sample on GitHub Pages

This repository uses GitHub as the source of truth. Sites and Google Drive are not deployment dependencies.

## Initial setup (once)

1. Repository Settings → Pages → Build and deployment → Source: **GitHub Actions**.
2. Upload the prepared **stardust-pages-source.zip** (about 1.2 MB) to the repository root on `main`, without renaming or unpacking it. The reviewed archive's SHA-256 is `027a03180a651e16753752fb165ef62210ecb426d3317eaea041f80447b044b1`.
3. Watch **Actions → Mobile guide · GitHub Pages**. The workflow imports the 15 reviewed files into `site/`, removes the one-time ZIP from the current tree, builds the guide, tests it and deploys. The verified URL is recorded by the deployment job and shown under Settings → Pages. Do not announce a live URL until that deployment succeeds.

If source is not uploaded yet, the workflow prints a setup message and **skips** building and publishing. A successful prepare job is NOT a live-site confirmation.

## Subsequent updates

Edit the tracked files in `site/`. A push to `main` touching that folder builds and tests the mobile site and updates the same Pages URL. There is no repeated HTML download/re-upload into Sites. For manual re-deployment use Actions → Mobile guide · GitHub Pages → Run workflow.

The source ZIP is only an initial transfer container, not the long-term source of truth. The source and all character illustrations become normal versioned Git files. Existing source is never overwritten by the bootstrap importer. A concurrent push causes a normal non-fast-forward rejection; no force push is used.

## Content preserved

- Seven character/scene fan-art assets plus two location illustrations
- Responsive single-column mobile layout, scene/episode drawers and artwork enlargement
- Correct mission counts: Aswan 3, Abu Simbel 3, overall 6, deduplicated across views
- Per-browser progress, bookmarks and reduced-motion controls
- Public HTTPS Share button shares the fixed URL; Save provides the offline self-contained HTML

Personal flight numbers, exact flight times and private calendar details are removed from the public source, not just hidden in the page. The itinerary uses generic Day 1 / Day 2. The artwork remains unofficial AI-generated fan art; no blanket publication/reuse clearance is claimed.

## Verification and access

The pipeline tests touch input, view synchronization, real HTTP-origin reload persistence, scene dialogs, day switching, loaded character art and horizontal overflow at 360 / 390 / 430 / 520px. Deployment happens only after these tests pass. These are browser emulation tests, not physical iPhone/Safari testing.

Only `_site/` is uploaded as the Pages artifact. The repository root is never published wholesale. The page includes noindex and robots.txt discourages indexing, but GitHub Pages is public: these are not authentication or access controls.

The workflow uses contents-write only for the one-time tracked source import. Deployment uses pages-write and id-token-write. No personal access token or new external service is required. Pages must be enabled once in the repository settings; this workflow does not pretend to enable unavailable administrative APIs.
