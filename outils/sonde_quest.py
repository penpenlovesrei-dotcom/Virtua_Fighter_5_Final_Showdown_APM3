#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""LA SONDE DU MODE QUEST : le jeu mene tout seul, sans clavier.

Calquee sur `tools/sonde_decor.py`, qui fait deja exactement cela pour un
decor. Elle lance `vfes.exe`, joue un scenario d'appuis que `apm.dll` relit a
chaud (`apm_entrees.txt`, controle toutes les 250 ms), capture a heures fixes
(`tools/capture_fenetre.py`), relit `quest_journal.txt`, et rend un rapport
plus les PNG dans `analysis/sonde/`.

**Le scenario manuel est sauve avant et remis apres** : le jeu lance ensuite a
la main ne doit pas appuyer tout seul.

UN SCENARIO PAR ECRAN. Ils sont ecrits dans `tools/scenarios/quest_*.txt`
avant d'etre joues, pour qu'on puisse les relire et les corriger a la main :

""" + '' + r"""
    creation   le choix du personnage et la creation des donnees
    carte      la carte a neuf lieux, le repere qui se deplace
    lieu       une salle ouverte : fenetre, curseur, liste des rivaux
    rencontre  l ecran de rencontre et les deux repliques
    combat     le combat lui-meme, jusqu au verdict
    apres      l apres-combat : verdict, serie, argent, grade
    boutique   Customize depuis la maison : les 3382 objets et leurs prix
    tournoi    le DOME : les trois tours
    emblemes   le STATUT, puis la liste des emblemes
    reglages   Quest settings : la difficulte

    py -3 tools/sonde_quest.py --liste
    py -3 tools/sonde_quest.py carte
    py -3 tools/sonde_quest.py combat --secondes 240
    py -3 tools/sonde_quest.py --ecrire-seulement      (n'ouvre pas le jeu)

INTERDICTION EN VIGUEUR. Frederic : « je t'interdis de lancer le jeu jusqu'a
nouvel ordre ». La sonde **refuse de lancer** tant que le fichier temoin
`runtime/media/vf5fs/AUTORISATION_LANCEMENT.txt` n'existe pas ; `--ecrire-
seulement` ne lance rien et sert a preparer les scenarios. Creer ce fichier
est un geste de Frederic, pas de l'agent.
"""
import os
import shutil
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
EXE = os.path.join(JEU, 'vfes.exe')
SCENARIO_ACTIF = os.path.join(JEU, 'apm_entrees.txt')
JOURNAL_JEU = os.path.join(JEU, 'quest_journal.txt')
DOSSIER = os.path.join(RACINE, 'analysis', 'sonde')
RAPPORT = os.path.join(RACINE, 'analysis', 'sonde_quest.txt')
MODELES = os.path.join(ICI, 'scenarios')
TEMOIN = os.path.join(JEU, 'AUTORISATION_LANCEMENT.txt')

# Les codes du stub, tels que `tools/gen_apm_stub.py` les distribue.
CODES = {'haut': 2, 'bas': 3, 'gauche': 4, 'droite': 5, 'piece': 6,
         'start': 7, 'carre': 8, 'croix': 9, 'rond': 10, 'triangle': 11,
         'l1': 12, 'r1': 13, 'r2': 14, 'sortie': 15,
         'camera': 16, 'vue': 17}

# CE QUI MENE AU QUEST, ET POURQUOI CES INSTANTS-LA.
#
# `tools/sonde_decor.py` a mesure qu'un appui de 200 ms fait descendre le
# curseur de DEUX crans : la repetition automatique du menu tombe dedans.
# On garde donc 80 ms, cinq trames -- assez pour etre vu, trop peu pour
# repeter. Les trois premiers START passent le titre, l'avertissement de
# sauvegarde et l'ecran d'accueil ; ils sont espaces de quatre secondes
# parce que chacun declenche une transition.
PRELUDE = [(20.0, 'start'), (24.0, 'start'), (28.0, 'start')]
# SCOREBOARDS est l'entree **5** du menu principal (menu_console.md §8.4) :
# cinq « bas » depuis l'entree 0, puis valider.
VERS_QUEST = ([(33.0 + 0.8 * i, 'bas') for i in range(5)]
              + [(38.0, 'start')])
DEBUT = 40.0                     # l'ecran du Quest est monte a partir d'ici


def apres(t, *suite):
    """(instant, touche) a partir de `t`, un appui toutes les 0,8 s."""
    return [(t + 0.8 * i, k) for i, k in enumerate(suite)]


# Chaque scenario : (description, touches apres DEBUT, duree, instants de
# capture). Les captures sont calees APRES l'appui qu'elles doivent montrer.
SCENARIOS = {
    'creation': (
        'la creation de donnees : choix du personnage, NO-NAME, 10th kyu, '
        'et les 50 000 G qui se versent',
        apres(DEBUT + 2, 'droite', 'droite', 'start'),
        110, [42, 45, 48, 52, 58, 70, 90]),
    'carte': (
        'la carte a neuf lieux : le repere se deplace, la fiche du joueur '
        'en bas a gauche, la photo du lieu sous le curseur',
        apres(DEBUT + 10, 'droite', 'droite', 'droite', 'gauche',
              'gauche', 'droite'),
        120, [50, 52, 54, 56, 60, 70, 90]),
    'lieu': (
        'une salle ouverte : la fenetre, le curseur, la liste des rivaux '
        'et leur grade',
        apres(DEBUT + 10, 'droite', 'start', 'bas', 'bas', 'droite',
              'droite', 'gauche'),
        140, [52, 55, 58, 62, 66, 80, 100]),
    'rencontre': (
        'l ecran de rencontre : le rival, son grade, ses deux repliques',
        apres(DEBUT + 10, 'droite', 'start', 'bas', 'start'),
        150, [55, 58, 62, 68, 80, 100]),
    'combat': (
        'le combat : les bons combattants, le bon decor, la bonne force '
        'de CPU -- et l habillage (nom et costume du rival)',
        apres(DEBUT + 10, 'droite', 'start', 'bas', 'start', 'start'),
        260, [60, 75, 90, 110, 140, 180, 220, 250]),
    'apres': (
        'l apres-combat : verdict, bit battu, serie, argent, grade',
        apres(DEBUT + 10, 'droite', 'start', 'bas', 'start', 'start'),
        320, [200, 230, 250, 270, 290, 310]),
    'boutique': (
        'Customize depuis la MAISON : les 3382 objets et leurs prix',
        apres(DEBUT + 10, 'start', 'bas', 'start', 'bas', 'bas',
              'start', 'bas', 'bas'),
        170, [55, 60, 64, 70, 80, 100, 130, 160]),
    'tournoi': (
        'le DOME : un tournoi de trois tours',
        apres(DEBUT + 10, 'droite', 'droite', 'droite', 'droite', 'start',
              'start'),
        300, [60, 70, 90, 130, 180, 240, 290]),
    'emblemes': (
        'le STATUT, puis la liste des emblemes',
        apres(DEBUT + 10, 'droite', 'start', 'droite', 'droite', 'start'),
        140, [55, 60, 65, 75, 95, 130]),
    'reglages': (
        'Quest settings : la difficulte (+0,2 ou +0,4 a la force du CPU)',
        apres(DEBUT + 10, 'start', 'bas', 'bas', 'start', 'droite',
              'droite', 'carre'),
        140, [55, 60, 66, 72, 80, 110]),
}


def texte_scenario(nom, touches, duree):
    """Le fichier que `apm.dll` relit. ASCII pur : il est verifie AVANT."""
    d, _, _ = SCENARIOS[nom][0], None, None
    l = ['# ---------------------------------------------------------------',
         '# Scenario du mode Quest : %s' % nom,
         '# %s' % d,
         '#',
         '# ECRIT PAR tools/sonde_quest.py -- il remplace le scenario manuel',
         '# le temps d une sonde, et la sonde le REMET a la fin.',
         '#',
         '# Duree prevue : %d s.' % duree,
         '# ---------------------------------------------------------------',
         '']
    for k, c in sorted(CODES.items(), key=lambda kv: kv[1]):
        l.append('nom %-8s = %d' % (k, c))
    l += ['', 'front   = 20', 'journal = 0', 'clavier = 0', 'manette = 0',
          '', '0       rien']
    horaire = []
    for t, k in PRELUDE + VERS_QUEST + list(touches):
        if k not in CODES:
            raise KeyError('touche inconnue : %r' % k)
        ms = int(t * 1000)
        horaire += [(ms, '%-7d %s' % (ms, k)),
                    (ms + 80, '%-7d rien' % (ms + 80))]
    l += [x for _, x in sorted(horaire)]
    txt = '\n'.join(l) + '\n'
    txt.encode('ascii')                  # la regle : verifier AVANT d'ecrire
    return txt


def ecrire_modeles():
    """Pose les dix scenarios dans `tools/scenarios/`, lisibles a la main."""
    os.makedirs(MODELES, exist_ok=True)
    poses = []
    for nom in sorted(SCENARIOS):
        _, touches, duree, _ = SCENARIOS[nom]
        chemin = os.path.join(MODELES, 'quest_%s.txt' % nom)
        txt = texte_scenario(nom, touches, duree)
        with open(chemin, 'w', encoding='ascii', newline='\n') as fp:
            fp.write(txt)
        poses.append(chemin)
    return poses


def autorise():
    return os.path.exists(TEMOIN)


def jouer(nom, secondes=None):
    import instrument
    _, touches, duree, captures = SCENARIOS[nom]
    duree = secondes or duree
    os.makedirs(DOSSIER, exist_ok=True)
    cibles = [(os.path.join(DOSSIER, 'quest_%s_t%03d.png' % (nom, t)),
               float(t), 'Virtua Fighter')
              for t in captures if t < duree - 2]

    # le journal du jeu est remis a zero : on veut CE passage-la
    if os.path.exists(JOURNAL_JEU):
        os.replace(JOURNAL_JEU, JOURNAL_JEU + '.avant_sonde')

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = True
    fichier = open(RAPPORT, 'w', encoding='utf-8')
    dbg.sortie = fichier
    sauve = SCENARIO_ACTIF + '.avant_sonde'
    shutil.copyfile(SCENARIO_ACTIF, sauve)
    debut = time.time()
    try:
        with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
            fp.write(texte_scenario(nom, touches, duree))
        print('scenario « %s » : %d s, %d capture(s)'
              % (nom, duree, len(cibles)))
        r = dbg.run(EXE, os.path.dirname(EXE), duree, tuple(cibles))
    finally:
        shutil.copyfile(sauve, SCENARIO_ACTIF)
        os.remove(sauve)
        fichier.close()
    return r, cibles, time.time() - debut


def rapporter(nom, cibles, secondes):
    lignes = ['SONDE DU MODE QUEST -- scenario « %s »' % nom,
              SCENARIOS[nom][0], '',
              '%.0f s de jeu.' % secondes, '']
    lignes.append('CAPTURES (%d) :' % len(cibles))
    for chemin, t, _ in cibles:
        etat = ('%d octets' % os.path.getsize(chemin)
                if os.path.exists(chemin) else 'MANQUANTE')
        lignes.append('  t=%-5.0f %-44s %s'
                      % (t, os.path.relpath(chemin, RACINE), etat))
    lignes.append('')
    if os.path.exists(JOURNAL_JEU):
        with open(JOURNAL_JEU, encoding='utf-8', errors='replace') as fp:
            j = fp.read().splitlines()
        lignes.append('quest_journal.txt : %d ligne(s)' % len(j))
        lignes += ['  %s' % x for x in j[-120:]]
    else:
        lignes.append('quest_journal.txt : ABSENT -- le module Quest n a rien '
                      'journalise. Soit l ecran n a pas ete atteint, soit il '
                      'n a pas tourne.')
    lignes.append('')
    lignes.append('LES CAPTURES SONT MONTREES A FREDERIC SANS VERDICT : '
                  'c est lui qui tranche.')
    txt = '\n'.join(lignes) + '\n'
    with open(RAPPORT, 'a', encoding='utf-8') as fp:
        fp.write('\n' + txt)
    print(txt)


def main():
    a = sys.argv[1:]
    if '--liste' in a or not a:
        print('SCENARIOS DU MODE QUEST')
        print()
        for nom in sorted(SCENARIOS):
            print('  %-10s %s' % (nom, SCENARIOS[nom][0]))
        print()
        print('  py -3 tools/sonde_quest.py <nom> [--secondes N]')
        print('  py -3 tools/sonde_quest.py --ecrire-seulement')
        return 0
    if '--ecrire-seulement' in a:
        for c in ecrire_modeles():
            print('ecrit : %s' % os.path.relpath(c, RACINE))
        return 0
    nom = a[0]
    if nom not in SCENARIOS:
        print('scenario inconnu : %r' % nom)
        print('les scenarios : %s' % ' '.join(sorted(SCENARIOS)))
        return 2
    ecrire_modeles()
    if not autorise():
        print()
        print('REFUS DE LANCER LE JEU.')
        print()
        print('  « je t interdis de lancer le jeu jusqu a nouvel ordre »')
        print()
        print('  Le scenario est ECRIT et pret :')
        print('    %s' % os.path.relpath(
            os.path.join(MODELES, 'quest_%s.txt' % nom), RACINE))
        print()
        print('  Pour lever l interdiction, creez le fichier temoin :')
        print('    %s' % os.path.relpath(TEMOIN, RACINE))
        print('  (son contenu n a aucune importance ; seule son existence '
              'compte)')
        return 3
    secondes = int(a[a.index('--secondes') + 1]) if '--secondes' in a else None
    r, cibles, duree = jouer(nom, secondes)
    rapporter(nom, cibles, duree)
    return 0 if r in (0, None) else 1


if __name__ == '__main__':
    sys.exit(main())
