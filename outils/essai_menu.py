#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UN ECRAN DE MENU, MESURE SEUL : on lance, on navigue, on photographie.

POURQUOI CET OUTIL (2026-10-08). Frederic a signale trois fois de suite un
ecran noir sur SINGLE PLAYER, et trois correctifs de suite ont porte a cote --
parce que chacun reposait sur une deduction. L'outil qui manquait tient en
trois pieces :

  1. UN SCENARIO BATI SUR `tools/apm_entrees.txt`. Le premier essai avait ecrit
     un scenario a lui, sans les reglages vivants du stub (manette, journal,
     sauvegarde, dispositions) : le jeu se fermait a 16 s, et le « 0 violation
     d'acces » mesure alors ne voulait RIEN DIRE. Un controle qui ment coute
     plus cher que pas de controle du tout.
  2. LA CAPTURE A INSTANTS FIXES (`tools/capture_fenetre.py`).
  3. UN VERDICT AUTOMATIQUE : le pourcentage de pixels non noirs. « Ecran
     noir » devient une mesure.

LES CODES D'ENTREE utiles ici, mesures :
    7 = START / valider      3 = BAS dans les menus
Le 3 a ete etabli le 2026-10-08 en pressant 2, 3, 4, 5 et en relevant la
position de la ligne rouge du curseur ; il manquait au dossier.

    py -3 tools/essai_menu.py sp            SINGLE PLAYER (entree 0)
    py -3 tools/essai_menu.py dojo          DOJO (entree 4)
    py -3 tools/essai_menu.py cran 6        l'entree 6, quelle qu'elle soit
    py -3 tools/essai_menu.py controls      HELP & OPTIONS (8) puis Controls (0)

Un chemin peut compter PLUSIEURS ecrans : `CHEMINS` porte alors la liste des
crans, un par validation. C'est ce qu'il fallait pour atteindre
OPTIONS > Controls, qui est a deux validations du menu principal.

Les captures vont dans `analysis/essai_<nom>_tNN.png`.
"""
import io
import os
import shutil
import subprocess
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
OUT = os.path.join(RACINE, 'analysis')
CAP = os.path.join(ICI, 'capture_fenetre.py')
REF = os.path.join(ICI, 'apm_entrees.txt')

CODE_VALIDER = 7
CODE_BAS = 3

# Le menu reorganise (--menu-v2) : 0 SINGLE PLAYER, 1 OFFLINE VERSUS,
# 2 ONLINE VERSUS, 3 QUEST MODE, 4 DOJO, 5 VF.TERMINAL, 6 SCOREBOARDS,
# 7 VF.TV, 8 HELP & OPTIONS, 9 EXIT GAME. OPTIONS n a plus que deux lignes --
# Controls (0) et Settings (1).
CHEMINS = {'sp': [0], 'versus': [1], 'dojo': [4], 'customize': [5],
           'vftv': [7], 'options': [8], 'controls': [8, 0],
           'settings': [8, 1],
           # LA PAGE DURAL : OPTIONS (8), Settings (1), puis la SEPTIEME
           # ligne -- six crans vers le bas -- et on valide. La capture
           # d avant la validation montre Settings avec le curseur sur
           # « Dural », celles d apres la page des trois bascules.
           'dural': [8, 1, 6],
           # LE MOVIE THEATER : VF.TV (7), sa ligne 0, puis la ligne visee.
           # `film0` est le TEMOIN -- la ligne 0 est la seule dont Frederic
           # dit qu elle lance une video, et c est la seule qui passe par le
           # relais d ENTREE (0x1801DE369) et non par celui de VALIDATION
           # (0x1801DE39F). Les deux essais cote a cote disent lequel des deux
           # relais ne part pas.
           'film0': [7, 0, 0],
           'film11': [7, 0, 11]}


def scenario(crans):
    """Deux START pour franchir le titre, puis, par ecran : N fois BAS et
    VALIDER.

    `crans` est une LISTE : un nombre de crans par validation. Un seul entier
    reste accepte -- c est l ancienne forme, a un seul ecran.
    """
    if isinstance(crans, int):
        crans = [crans]
    seq = ['0       rien',
           '18000   start', '18400   rien',
           '24000   start', '24400   rien']
    t = 30000
    for etage in crans:
        for _ in range(etage):
            seq += ['%d   %d' % (t, CODE_BAS), '%d   rien' % (t + 300)]
            t += 1500
        t += 1000
        seq += ['%d   start' % t, '%d   rien' % (t + 400)]
        # l ecran suivant doit avoir le temps de s ouvrir avant qu on y bouge
        t += 2500
    return '\n'.join(seq) + '\n', (t - 2500 + 2000) / 1000.0


# LES PAS LIBRES. `CHEMINS` ne sait dire que « N fois BAS puis VALIDER », et
# cela ne suffit plus : OFFLINE VERSUS n accepte la validation que lorsque le
# JOUEUR 2 est entre en jeu. Mesure du 2026-10-11 : son creneau [10]
# (0x1801DE510) commence par `cmp byte [rcx+0x309], 0`, et l unique ecriture
# qui peut y poser 1 est 0x1801DDC67 -- `setns cl` sur le retour de
# 0x1801A2330(1), c est-a-dire `[0x180751280 + 1*0x100] >= 0` : l etat du
# JOUEUR 2. Tant qu il n est pas la, Entree ne fait rien, et ce n est pas une
# panne : c est une borne a deux credits.
#
#     py -3 tools/essai_menu.py pas b v j v
#
# b bas   h haut   g gauche   d droite   v valider   a annuler
# j le START du JOUEUR 2 (code 7 + 16 : --joueur2 decale ses codes de seize)
# p la piece   . une pause d une seconde de plus
# EN MAJUSCULES, LE JOUEUR 2 : H haut  B bas  G gauche  D droite
#                              P sa piece     A son annuler
# LES PAS DU JOUEUR 2, EN MAJUSCULES (2026-10-11). Il en fallait pour
# mesurer le versus : « sur l ecran de selection des personnages, P2 n est
# pas present » ne se verifie qu en FAISANT BOUGER le joueur 2. Ses codes
# sont ceux du joueur 1 decales de seize (--joueur2).
PAS = {'b': 3, 'h': 2, 'g': 4, 'd': 5, 'v': 7, 'a': 8, 'j': 7 + 16,
       'p': 6, '.': None,
       'H': 2 + 16, 'B': 3 + 16, 'G': 4 + 16, 'D': 5 + 16,
       'P': 6 + 16, 'A': 8 + 16}


def scenario_pas(mots):
    """Une suite libre de codes, un toutes les 1,5 s a partir de 30 s."""
    seq = ['0       rien',
           '18000   start', '18400   rien',
           '24000   start', '24400   rien']
    t = 30000
    for m in mots:
        if m not in PAS:
            raise SystemExit('pas inconnu : %r (connus : %s)'
                             % (m, ' '.join(sorted(PAS))))
        c = PAS[m]
        if c is None:
            t += 1000
            continue
        seq += ['%d   %d' % (t, c), '%d   rien' % (t + 400)]
        t += 1500
    return '\n'.join(seq) + '\n', (t + 2000) / 1000.0


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    nom = argv[0]
    if nom == 'pas':
        seq, t_valide = scenario_pas(argv[1:])
        return lancer('pas', seq, t_valide)
    if nom == 'cran':
        crans = [int(a) for a in argv[1:] if a.isdigit()]
    elif nom in CHEMINS:
        crans = CHEMINS[nom]
    else:
        print('nom inconnu : %s (connus : %s, ou « cran N [N...] »)'
              % (nom, ', '.join(sorted(CHEMINS))))
        return 1

    seq, t_valide = scenario(crans)
    return lancer(nom, seq, t_valide)


def lancer(nom, seq, t_valide):
    ref = io.open(REF, encoding='latin-1').read()
    if '0       rien\n' not in ref:
        print('REFUS : %s n a pas sa ligne « 0       rien »' % REF)
        return 2
    vivant = os.path.join(JEU, 'apm_entrees.txt')
    io.open(vivant, 'w', encoding='latin-1', newline='\n').write(
        ref.replace('0       rien\n', seq, 1))

    def rendre_le_clavier():
        """Le scenario ne doit PAS survivre a l'essai.

        `item_porte.cmd` ne recopie pas `apm_entrees.txt` : le scenario laisse
        en place ferait appuyer sur START tout seul au lancement suivant, et le
        jeu naviguerait sans qu'on y touche. On le rend donc toujours, meme si
        l'essai s'interrompt.
        """
        # EN OCTETS, pas en texte : le fichier de reference est en CRLF, et le
        # relire en mode texte puis le reecrire le passerait en LF.
        shutil.copyfile(REF, vivant)
        print('  scenario retire : le clavier est rendu.')

    subprocess.run(['taskkill', '/f', '/im', 'vfes.exe'], capture_output=True)
    time.sleep(1)
    p = subprocess.Popen([os.path.join(JEU, 'vfes.exe')], cwd=JEU)
    print('vfes.exe lance ; validation prevue a %.0f s' % t_valide)

    images = []
    try:
        t0 = time.time()
        for t in (t_valide - 2, t_valide + 4, t_valide + 10, t_valide + 16):
            while time.time() - t0 < t:
                time.sleep(0.2)
            if p.poll() is not None:
                print('%2.0fs  LE JEU S EST FERME (code %s)' % (t, p.returncode))
                break
            c = os.path.join(OUT, 'essai_%s_t%02d.png' % (nom, t))
            subprocess.run([sys.executable, CAP, c], capture_output=True)
            images.append((t, c))
        time.sleep(1)
    finally:
        if p.poll() is None:
            p.terminate()
        rendre_le_clavier()

    try:
        from PIL import Image
    except ImportError:
        for t, c in images:
            print('  %2.0fs  %s' % (t, c))
        return 0
    for t, c in images:
        if not os.path.exists(c):
            print('  %2.0fs  pas de capture' % t)
            continue
        px = list(Image.open(c).convert('L').getdata())
        clairs = sum(1 for v in px if v > 24) * 100.0 / len(px)
        print('  %2.0fs  %5.1f %% de pixels non noirs   %s   %s'
              % (t, clairs, 'ECRAN NOIR' if clairs < 1.0 else 'image   ',
                 os.path.basename(c)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
