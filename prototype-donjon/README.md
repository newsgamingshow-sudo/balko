# L'Écho des Profondeurs (prototype v9)

Prototype jouable d'un dungeon crawler en vue FPS : dark fantasy, rendu 3D pixelisé, horreur sonore.

## Lancer le jeu

Ouvre `echo-des-profondeurs.html` dans Chrome ou Edge (fonctionne hors ligne, Three.js est intégré au fichier).
Joue avec un casque audio. Manette Xbox : appuie sur un bouton une fois la page ouverte.
Si une touche ne répond pas : écran titre ou pause → « Tester la manette » / « Configurer la manette ».

## Histoire

Au premier feu de camp, un sac abandonné contient la note de « M. » : les gobelins enlèvent des gens pour
les réduire en esclavage et nourrir les choses qui naissent plus bas. À chaque étage, des survivants attendent d'être libérés.

## Les 5 étages

1. **Les Geôles** : gobelins variés (maigres, brutes casquées, lanceurs de couteaux, imitateur), boss Chef gobelin, 3 prisonniers qui rejoignent le camp.
2. **Les Couveuses** : les Aveugles chassent au son. Avancer sans bruit (LT / C) pour passer à côté.
3. **Le Nid** : seulement le Rampant, immortel, et aucune torche allumée. Il rampe au plafond, s'accroche aux angles, surgit derrière toi, casse les caisses et fuit par les trous des murs.
4. **Les Ombres** : elles brûlent face à ta torche et fuient dans les murs, mais reviennent par-derrière.
5. **La Matrice** : tous les monstres et la Couveuse, boss qui pond des rejetons. Fin de la démo, puis étages sans fin.

Chaque nouveau monstre est expliqué par une note près du feu de camp.

## Systèmes

- Caisses et tonneaux à briser : or ou objets, rangés dans le coffre du camp (inventaire).
- Objets : fiole, résine de torche, pierre à aiguiser, cœur séché, herbe amère (bonus permanents).
- Trous dans les murs : les monstres en fuite s'y cachent puis ressortent ailleurs.
- Peur : à l'approche des monstres, la torche faiblit, l'image se désature, le cœur bat.
- Améliorations au feu de camp, l'or porté est perdu à la mort, le coffre est conservé.

Tout (graphismes, sons, musique) est généré par le code, sans fichier externe.
