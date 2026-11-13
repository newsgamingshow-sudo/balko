"""Construit la version CrazyGames d'Empilo : dist/empilo-crazygames.zip
- anglais par défaut (français seulement si on force ?lang=fr)
- aucune ressource externe : three.js inclus, police système (pas de Google Fonts)"""
import pathlib, re, zipfile, shutil
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "game/empilo.html").read_text(encoding="utf-8")
src = re.sub(r'<link rel="preconnect"[^>]*>\n?', '', src)
src = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n?', '', src)
src = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\n?', '', src)
src = src.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>', '<script src="three.min.js"></script>')
old = "(new URLSearchParams(location.search).get('lang')||navigator.language||'en')"
assert old in src
src = src.replace(old, "(new URLSearchParams(location.search).get('lang')||'en')")
src = src.replace('<title>Empilo</title>', '<title>Empilo</title>').replace(
    'content="Empilez des cubes de couleur le plus haut possible. Touchez pour poser, visez le parfait, dépassez la tour Eiffel."',
    'content="Stack colorful blocks as high as you can. Tap to drop, aim for perfect, pass the Eiffel Tower."')
assert 'https://' not in re.sub(r'http://www.w3.org[^"\']*', '', src), "ressource externe restante"
html = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">'
        '</head><body>\n' + src + '\n</body></html>\n')
out = ROOT / "dist/empilo-crazygames"; shutil.rmtree(out, ignore_errors=True); out.mkdir(parents=True)
(out / "index.html").write_text(html, encoding="utf-8")
shutil.copy(ROOT / "game/vendor/three.min.js", out / "three.min.js")
shutil.copy(ROOT / "game/vendor/three.LICENSE", out / "three.LICENSE.txt")
z = ROOT / "dist/empilo-crazygames.zip"
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as f:
    for p in sorted(out.iterdir()): f.write(p, p.name)
print(z, round(z.stat().st_size / 1024), "Ko")
