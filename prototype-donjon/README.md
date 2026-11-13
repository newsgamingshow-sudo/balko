# L'Écho des Profondeurs (prototype)

Prototype jouable d'un dungeon crawler en vue FPS : dark fantasy, rendu 3D pixelisé, horreur sonore.

## Lancer le jeu

Ouvre `echo-des-profondeurs.html` dans Chrome ou Edge (fonctionne hors ligne, Three.js est intégré au fichier).
Joue avec un casque audio.

Manette Xbox (Bluetooth) : connecte-la au PC, puis appuie sur un bouton une fois la page ouverte.

## Contenu du prototype

- Un étage généré aléatoirement (salles, couloirs, cellules), qui change à chaque mort.
- Feu de camp : repos, améliorations (vitalité, endurance, lame, fioles).
- Gobelins avec voix 3D : marmonnements, cris d'alerte, bruits de pas. On les entend à travers les murs (son étouffé).
- 3 prisonniers qui appellent à l'aide. Une fois libérés, ils rejoignent le camp et débloquent des choses (forge, potions, carte).
- Un gobelin imite les cris des prisonniers.
- Combat : coup rapide, coup lourd, esquive, endurance, fioles de soin.
- Boss : le Chef gobelin, qui garde la trappe vers l'étage suivant.
- Le Rampant (nouveau monstre tous les deux étages) : créature pâle et très rapide qui se racle la gorge, erre dans tout l'étage et t'observe depuis les angles. Aux étages 1-2 il ne fait qu'observer ; à partir de l'étage 3 il chasse.
- Mort : on perd l'or porté, on garde les améliorations.

Tout (graphismes, sons, musique) est généré par le code, sans fichier externe.
