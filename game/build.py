"""Construit docs/index.html (GitHub Pages) à partir de game/empilo.html."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
body = (ROOT / "game/empilo.html").read_text(encoding="utf-8")
html = ('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">'
        '<meta property="og:title" content="Empilo"><meta property="og:description" content="Empilez des cubes le plus haut possible. Tu dépasses la tour Eiffel ?">'
        '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 100 100%27><rect x=%2715%27 y=%2755%27 width=%2770%27 height=%2730%27 rx=%276%27 fill=%27%23ff7a2f%27/><rect x=%2725%27 y=%2720%27 width=%2750%27 height=%2730%27 rx=%276%27 fill=%27%239f6bff%27/></svg>">'
        '</head><body>\n' + body + '\n</body></html>\n')
(ROOT / "docs/index.html").write_text(html, encoding="utf-8")
print("docs/index.html généré")
