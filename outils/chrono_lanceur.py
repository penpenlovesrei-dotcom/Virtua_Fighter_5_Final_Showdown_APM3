# -*- coding: utf-8 -*-
r"""CHRONOMETRER LE LANCEUR, etape par etape.

Frederic parle du temps entre le DOUBLE-CLIC sur item_porte.cmd et le premier
ecran. Le profil BOOT ne mesurait que la seconde moitie -- son horloge part au
chargement de apm.dll, donc APRES tout le travail du lanceur.

Avant de lancer vfes.exe, item_porte.cmd fait cinq choses :

    1. gen_apm_stub.py        regenere et RECOMPILE apm.dll (gcc)
    2. decor_neuf.py          refait les deux bases de decors
    3. shader_empreintes.py
    4. boutons_style.py       pose le style de boutons
    5. patch_moteur.py        une cinquantaine de chantiers sur le moteur

On les relance ici une par une, exactement comme le lanceur, et on chronometre.
Rien de destructeur : ce sont les memes commandes, dans le meme ordre.

    py -3 tools/chrono_lanceur.py
"""
import os
import subprocess
import sys
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAM = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'ram')


def lire(nom, defaut):
    c = os.path.join(RAM, nom)
    try:
        with open(c) as fp:
            return fp.read().split()
    except IOError:
        return defaut


res = lire('resolution.txt', ['1280', '720'])
mode = lire('mode.txt', ['console'])[0]
btn = lire('boutons.txt', ['ps5'])[0]

ETAPES = [
    ('apm.dll (gcc)', ['tools/gen_apm_stub.py']),
    ('decors 5r+vf5 (bases)', ['tools/decor_neuf.py', '--poser-lot', '5r+vf5',
                               '--bases-seules']),
    ('empreintes de shaders', ['tools/shader_empreintes.py']),
    ('style de boutons', ['tools/boutons_style.py', '--poser', btn]),
]

PATCH = [
    'tools/patch_moteur.py', '--resolution', res[0], res[1], '--langue',
    '--logo-japonais', '--dural', '--wxga', '--dural-grille', '--mode', '0',
    '--menu-init', '--sousmenu', '--transition-game', '--sp-menu',
    '--sp-lancer', '--sp-sparring', '--joueur2', '--menu-fermer',
    '--options-raccourci', '--dojo-howto', '--dojo-cadre', '--options-v2',
    '--menu-exit', '--legende-sousmenu', '--attract-retour-titre',
    '--sans-now-loading', '--options-tips', '--sans-ecran-epilepsie',
    '--decor-perso', 'trm', '--terminal-boutons', '--customize-curseur',
    '--replays-sans-gel', '--vignettes-costume', '--selitem-grille',
    '--selitem-republier', '--selitem-ecreter', '--selpart-curseur',
    '--item-basculer', '--sans-warning', '--options-resolution',
    '--options-mode', '--menu-v2', '--menu-griser', '--versus-joueur2',
    '--sans-legende', '--options-dural', '--versus-manette',
    '--terminal-ordre', '--film-cadres', '--nom-donnees', '--du2-collision',
    '--variantes', '--variantes-texte', '--variantes-5r', '--variantes-vf5',
    '--decors-5r', '--decors-vf5', '--decors-5r-dural', '--decors-table',
    '86', '--grille-table', '--decor-ecretage', '86', '--decor-repli', '42',
    '--obj-db-libre',
]
ETAPES.append(('patch du moteur (%d chantiers)'
               % sum(1 for a in PATCH if a.startswith('--')), PATCH))


def main():
    print('resolution %s x %s, mode %s, boutons %s'
          % (res[0], res[1], mode, btn))
    print()
    total = 0.0
    for nom, cmd in ETAPES:
        t = time.time()
        r = subprocess.run([sys.executable] + cmd, cwd=RACINE,
                           capture_output=True, text=True)
        d = time.time() - t
        total += d
        etat = 'ok' if r.returncode == 0 else 'ECHEC %d' % r.returncode
        print('%7.2f s   %-34s %s' % (d, nom, etat))
        if r.returncode:
            print(r.stdout[-600:])
            print(r.stderr[-600:])
    print('-' * 58)
    print('%7.2f s   AVANT MEME QUE vfes.exe DEMARRE' % total)
    print()
    print('Le profil BOOT du journal mesure ce qui vient APRES.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
