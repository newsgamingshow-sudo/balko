"""Construit les versions autonomes d'Arènes de Valdor (aucune ressource externe) :
- docs/valdor/  : version web (GitHub Pages), langue selon le navigateur
- dist/valdor-crazygames.zip : version CrazyGames, anglais par défaut (?lang=fr pour le français)"""
import pathlib, re, base64, shutil, zipfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
V = ROOT / "valdor/vendor"
src = (ROOT / "valdor/index.html").read_text(encoding="utf-8")
def font(fam, w, f):
    b = base64.b64encode((V / f).read_bytes()).decode()
    return f"@font-face{{font-family:'{fam}';font-weight:{w};font-display:swap;src:url(data:font/woff2;base64,{b}) format('woff2')}}"
fonts = "<style>" + "".join([font("Pixelify Sans",400,"pixelify-sans-latin-400-normal.woff2"),font("Pixelify Sans",700,"pixelify-sans-latin-700-normal.woff2"),
                             font("Alegreya Sans",400,"alegreya-sans-latin-400-normal.woff2"),font("Alegreya Sans",700,"alegreya-sans-latin-700-normal.woff2")]) + "</style>\n"
src = re.sub(r'<link rel="preconnect"[^>]*>\n?', '', src)
src = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n?', fonts, src)
src = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\n?', '', src)
src = src.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>', '<script src="three.min.js"></script>')
assert "https://" not in re.sub(r"http://www\.w3\.org[^\"']*", "", src), "ressource externe restante"
def page(body, lang):
    return ('<!doctype html>\n<html lang="'+lang+'"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<meta name="description" content="Valdor Arenas — auto-battler fantasy en pixel art : votre chevalier combat seul, gagne du butin et affronte des boss.">'
            '</head><body>\n' + body + '\n</body></html>\n')
web = ROOT / "docs/valdor"; web.mkdir(parents=True, exist_ok=True)
(web / "index.html").write_text(page(src, "fr"), encoding="utf-8"); shutil.copy(V / "three.min.js", web / "three.min.js")
cg = src.replace("(new URLSearchParams(location.search).get('lang')||navigator.language||'en')", "(new URLSearchParams(location.search).get('lang')||'en')")
assert cg != src
out = ROOT / "dist/valdor-crazygames"; shutil.rmtree(out, ignore_errors=True); out.mkdir(parents=True)
(out / "index.html").write_text(page(cg, "en"), encoding="utf-8")
for f in ["three.min.js", "three.LICENSE", "OFL-pixelify-sans.txt", "OFL-alegreya-sans.txt"]:
    if (V / f).exists(): shutil.copy(V / f, out / f)
z = ROOT / "dist/valdor-crazygames.zip"
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for p in sorted(out.iterdir()): zf.write(p, p.name)
print("docs/valdor/ et", z.name, round(z.stat().st_size/1024), "Ko")
