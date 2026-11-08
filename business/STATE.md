# STATE — Balko
_Mis à jour : 2026-11-08_

## Phase en cours
Phase 3 — construction terminée, en attente de mise en ligne.

## Le business
- Site d'outils gratuits en français pour micro-entrepreneurs (générateur de facture/devis, calculateur de TJM)
  → trafic Google (SEO).
- Produit payant : « Pack Pro micro-entrepreneur » (tableurs xlsx + modèles de relance), 9 €, paiement Stripe.
- Hébergement : GitHub Pages depuis `docs/` → https://newsgamingshow-sudo.github.io/balko/

## Bloquants (action du propriétaire)
1. Activer GitHub Pages (Settings → Pages → Branch `main`, dossier `/docs`). L'API Pages est bloquée depuis la session.
2. Créer le compte Stripe (identité + RIB), puis fournir la clé secrète via le formulaire sécurisé.
3. Fournir les infos des mentions légales/CGV : nom, adresse, SIRET, e-mail de contact (marqueurs [À COMPLÉTER]).

## Prochaines actions (Claude)
- Dès que Stripe est connecté : créer produit + Payment Link par l'API, livraison du pack après paiement, activer le bouton sur pack.html.
- Ajouter des pages outils SEO longue traîne (une page = une recherche Google précise).
- Programmer une session quotidienne d'optimisation.

## Note de livraison
Le dépôt est public : le fichier payant (`produit/dist/`) n'est PAS commité. Il se régénère avec `python3 produit/build_pack.py`.
