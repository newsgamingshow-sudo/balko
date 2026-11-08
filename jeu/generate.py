"""Génère les énigmes quotidiennes de Passemot.

Principe (domaine public, « doublets » de Lewis Carroll, 1877) : passer d'un mot de départ
à un mot d'arrivée en changeant une seule lettre à chaque coup, chaque étape devant être un mot français.

Sorties (dans docs/) :
  - passemot-data.js : dictionnaire de validation + énigmes datées (une par jour).
Dépendances : pip install wordfreq ; jeu/mots-fr.json (paquet npm an-array-of-french-words, MIT).
"""
import json, re, random, unicodedata, collections, pathlib, datetime
from wordfreq import top_n_list, zipf_frequency

ROOT = pathlib.Path(__file__).resolve().parent.parent
L = 4
DAYS = 365
EPOCH = datetime.date(2026, 11, 9)  # énigme n°1
MIN_PAR, MAX_PAR = 4, 6
BLACKLIST = set("""CONS CONNE PUTE PUTES BITE BITES CHIE CHIES PINE PINES ZOBS FION TEUB NAZI PEDE PEDES
GODE GODES NIKE NIER CRIS VIOL VIOLS TUER TUEE TUES MORT MORTS MEUF NEGRE CULS SEXE SEXY SODO CUIT
SUCE SUCER BAISE NIQUE MERDE BRANLE DROGUE OBSEDE ZIZI RENE LISE LUIS ROSA MALI LIMA GAZA INDE JURA MARC
JEAN SUEZ CANA SANA CASA GAYS HOMO JUIF IMAM ANUS CACA PIPI""".split())
# Mots outils : valides en coup intermédiaire, mais jamais choisis comme départ / arrivée
OUTILS = set("""POUR DANS PLUS AVEC MAIS VOUS ELLE SONT TOUT NOUS FAIT ETRE BIEN MEME PEUT LEUR TRES SUIS
TOUS SANS RIEN DIRE FOIS FAUT DONC SOUS DONT DEJA QUOI SOIT CHEZ SERA CELA DOIT PUIS CEUX VERS SAIS
FAIS VEUT VEUX PEUX VAIS LORS TANT AUSSI ETES AVEZ AVAIT AIES AURA IRAI IRAS IRONT VONT ONT AIENT
ELLES SOIS SERAI ETAIS ETAIT ETES MOIS""".split())

def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').upper().replace('Œ', 'OE')

raw = json.loads((ROOT / 'jeu/mots-fr.json').read_text(encoding='utf-8'))
VALID = sorted({norm(w) for w in raw if len(norm(w)) == L and re.fullmatch(r'[A-Z]+', norm(w))} - BLACKLIST)
vset = set(VALID)
freq = collections.defaultdict(float)
for w in top_n_list('fr', 80000):
    n = norm(w)
    if n in vset:
        freq[n] = max(freq[n], zipf_frequency(w, 'fr'))
# Mots courants pour les solutions affichées : exclut les mots plus fréquents en anglais (CASH, CAKE…)
COMMON = {w for w in VALID if freq[w] >= 3.0 and zipf_frequency(w.lower(), 'en') < freq[w]}
# Départs / arrivées : liste choisie à la main (noms et adjectifs simples, agréables à jouer)
CHOISIS = set("""ABRI ACTE AIDE AIGU AILE AMER AMIE ANGE ANSE ARME AUBE AUTO AVAL AVEU AVIS AZUR BAIE BAIN BANC
BASE BEAU BEBE BETE BISE BLEU BLOC BOIS BORD BOUC BOUE BOUT BOXE BRAS BREF BRIN BRUN BRUT CAFE CAMP CERF CHAR
CHAT CHEF CHER CHIC CHOC CHOU CIEL CINE CINQ CIRE CITE CLAN CLEF CLOS CLOU COCO COIN COTE COUP COUR CRAN CUIR
CUVE DAME DEFI DEMI DENT DEUX DIEU DODO DOSE DOUX DRAP DUEL DUNE ECHO EGAL ELAN EPEE ETAT EURO EXIL FAIM FAUX
FETE FEUX FIER FILM FILS FIXE FLOT FLOU FOIE FOIN FOND FORT FOUS GALA GANT GARE GOUT GRAS GRIS GROS GRUE HAIE
HAUT HIER HOTE HUIT IDEE IRIS IVRE JEUX JOIE JOLI JOUR JUDO JUGE JUIN JUPE KILO LAIT LAMA LAME LARD LENT LIEN
LIEU LION LIRE LOIN LOIR LOTO LOUP LUNE LUXE MAIN MARE MARI MERE MIDI MIEL MINI MODE MONT MOTO MUET NAGE NAIF
NAIN NERF NEUF NOEL NOIR NOIX NORD NUIT OEIL OEUF ONDE ONZE ORGE OURS PAIX PAPA PARC PARI PATE PAVE PAYS PEAU
PERE PEUR PIED PILE PION PIRE PLAN PLAT PNEU POIL POIS POLE POLI PONT PORC PORT POSE POTE PRET PRIX PROF PUCE
QUAI RAGE RAME RANG RAVI REEL REIN REVE RHUM RIME RIRE RIVE ROBE ROND ROUE ROUX RUSE SAGE SAIN SANG SAUT SCIE
SEAU SEIN SEPT SEUL SIRE SOIE SOIF SOIN SOIR SOJA TARD TAUX TAXE TAXI TELE TETE THON TIGE TOIT TOUR TOUX TRAM
TRIO TROU TRUC TYPE URNE VASE VEAU VELO VENT VERT VICE VIDE VITE VOEU VOIE VOIX VRAC VRAI YEUX ZELE ZONE""".split())
ENDPOINTS = sorted(w for w in COMMON if w in CHOISIS)

def neighbours(words):
    buckets = collections.defaultdict(list)
    for w in words:
        for i in range(L):
            buckets[w[:i] + '_' + w[i+1:]].append(w)
    nb = collections.defaultdict(set)
    for b in buckets.values():
        for a in b:
            nb[a].update(x for x in b if x != a)
    return nb

NB_ALL, NB_COMMON = neighbours(VALID), neighbours(COMMON)

def bfs(nb, src):
    dist, prev, q = {src: 0}, {}, collections.deque([src])
    while q:
        u = q.popleft()
        for v in nb[u]:
            if v not in dist:
                dist[v] = dist[u] + 1; prev[v] = u; q.append(v)
    return dist, prev

rng = random.Random(20261109)
candidates = []
for s in ENDPOINTS:
    da, _ = bfs(NB_ALL, s)
    dc, prev = bfs(NB_COMMON, s)
    for t in ENDPOINTS:
        if t <= s: continue
        if t in dc and MIN_PAR <= dc[t] <= MAX_PAR and da.get(t) == dc[t]:
            # aucune lettre en commun à la même place : énigme plus intéressante
            if sum(a == b for a, b in zip(s, t)) > 1: continue
            path = [t]
            while path[-1] != s: path.append(prev[path[-1]])
            candidates.append((s, t, dc[t], path[::-1]))
rng.shuffle(candidates)
used, puzzles = collections.Counter(), []
# Courbe de difficulté hebdomadaire : lundi facile → dimanche difficile
week_par = [4, 4, 5, 4, 5, 5, 6]
by_par = collections.defaultdict(list)
for c in candidates: by_par[c[2]].append(c)
for d in range(DAYS):
    want = week_par[(EPOCH + datetime.timedelta(days=d)).weekday()]
    pool = by_par[want]
    i = min(range(len(pool)), key=lambda i: (max(used[pool[i][0]], used[pool[i][1]]), i))
    s, t, par, path = pool.pop(i)
    used[s] += 1; used[t] += 1
    if rng.random() < 0.5: s, t, path = t, s, path[::-1]
    puzzles.append({'n': d + 1, 'date': (EPOCH + datetime.timedelta(days=d)).isoformat(), 's': s, 't': t, 'par': par, 'sol': path})

out = ROOT / 'docs/passemot-data.js'
out.write_text('window.PASSEMOT=' + json.dumps({'L': L, 'epoch': EPOCH.isoformat(), 'mots': ' '.join(VALID), 'puzzles': puzzles}, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
print(f"{len(VALID)} mots valides, {len(COMMON)} courants, {len(ENDPOINTS)} départs possibles, {len(candidates)} énigmes candidates, {len(puzzles)} générées → {out}")
for p in puzzles[:21]: print(p['date'], p['s'], '→', p['t'], 'par', p['par'], ' '.join(p['sol']))
