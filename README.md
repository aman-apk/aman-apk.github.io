# amanlabs.app

Source of the Aman Labs website. A single generated page: `tools/build_site.py` reads the app list and writes `index.html`; `store/` is the download redirect for Aman Store; `media/` holds the images the GitHub READMEs embed.

The live app versions on the page are filled in at load time from `https://dl.amanlabs.app/catalog.json`, the same catalog Aman Store uses. To change copy or layout, edit the generator, not `index.html`.

Downloads, hashes and signing fingerprints live in [aman-releases](https://github.com/aman-apk/aman-releases).
