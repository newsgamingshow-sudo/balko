# JOURNAL

## 2026-11-08
- Recherche : templates et petits outils = produits numériques parmi les plus vendus ; sites d'outils gratuits rentables
  mais lents à décoller via SEO seul (exemples : 175 calculateurs → 0 trafic à 3 mois ; site de calculateurs à ~310 $/mois après 3 ans).
- Décision : outils gratuits pour micro-entrepreneurs (forte demande « modèle facture gratuit ») + produit payant à 9 €.
- Construit : site statique (src/ → docs/ via src/build.py), générateur facture/devis (PDF via impression), calculateur TJM,
  page Pack Pro, mentions légales, CGV, confidentialité, sitemap, robots.txt.
- Construit : Pack Pro (produit/build_pack.py) — tableau de bord, livre des recettes, suivi des factures, relances. Formules vérifiées avec LibreOffice.
- Testé : toutes les pages sans erreur JS, mobile 390 px sans débordement.
- Limite : sites URSSAF inaccessibles depuis la session → taux de cotisations laissés modifiables et signalés comme indicatifs.
