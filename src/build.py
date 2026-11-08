"""Construit le site statique dans docs/ à partir de src/pages/*.html.
Chaque page commence par des lignes d'en-tête 'title:' et 'description:' puis '---'."""
import pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE_URL = "https://newsgamingshow-sudo.github.io/balko/"
LAYOUT = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{description}">
<link rel="canonical" href="{url}"><link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📄</text></svg>">
</head><body>
<header class="site"><div class="in"><a class="logo" href="./">Balko</a>
<nav><a href="facture.html">Facture</a><a href="facture.html?type=devis">Devis</a><a href="tjm.html">Calcul TJM</a><a href="pack.html">Pack Pro</a></nav></div></header>
<main>{body}</main>
<footer><div class="in"><a href="mentions-legales.html">Mentions légales</a><a href="cgv.html">CGV</a><a href="confidentialite.html">Confidentialité</a>
<p>Balko — outils gratuits pour micro-entrepreneurs et freelances. Aucune donnée n'est envoyée sur un serveur : tout reste dans votre navigateur.</p></div></footer>
</body></html>
"""
pages = []
for f in sorted((ROOT / "src/pages").glob("*.html")):
    head, body = f.read_text(encoding="utf-8").split("\n---\n", 1)
    meta = dict(l.split(":", 1) for l in head.strip().splitlines())
    name = f.name
    url = BASE_URL + ("" if name == "index.html" else name)
    (ROOT / "docs" / name).write_text(LAYOUT.format(title=meta["title"].strip(), description=meta["description"].strip(), url=url, body=body), encoding="utf-8")
    pages.append(url)
today = datetime.date.today().isoformat()
(ROOT / "docs/sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in pages) + "</urlset>\n", encoding="utf-8")
(ROOT / "docs/robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n", encoding="utf-8")
(ROOT / "docs/.nojekyll").write_text("")
print(f"{len(pages)} pages générées")
