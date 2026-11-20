#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""LANCER LE JEU SOI-MEME, le piloter par un scenario, et lire le journal.

Frederic, le 2026-10-15 : « pourquoi je dois faire ca autant de fois ? ».
Parce que je me servais de lui comme banc d essai. Le depot sait pourtant
piloter le jeu tout seul : `apm.dll` rejoue un scenario d entrees lu dans
`apm_entrees.txt`, et c est ce que font deja `pister_etat.py` et ses freres.

Cet outil fait le tour complet, sans debogueur donc a pleine vitesse :

    1. il met le scenario a la place de `apm_entrees.txt` (l original est
       remis a la fin, quoi qu il arrive) ;
    2. il efface le journal, pour ne lire que CE tour ;
    3. il lance `vfes.exe`, le laisse tourner le temps demande, le ferme ;
    4. il imprime les lignes du journal qui portent le prefixe demande.

    py -3 tools/essai_scenario.py <scenario> [--secondes 70] [--grep FILM]

Il refuse de partir si `vfes.exe` tourne deja : deux instances se disputent
le meme `apm_entrees.txt` et le meme journal.
"""
import io
import os
import shutil
import subprocess
import sys
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VF5 = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
EXE = os.path.join(VF5, 'vfes.exe')
ENTREES = os.path.join(VF5, 'apm_entrees.txt')
JOURNAL = os.path.join(VF5, 'apm_journal.txt')


def tourne_deja():
    r = subprocess.run(['tasklist', '/nh'], capture_output=True, text=True)
    return 'vfes.exe' in r.stdout


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    scenario = argv[0]
    if not os.path.isabs(scenario):
        scenario = os.path.join(RACINE, scenario)
    if not os.path.exists(scenario):
        print('scenario introuvable : %s' % scenario)
        return 2
    secondes = 70
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    motif = argv[argv.index('--grep') + 1] if '--grep' in argv else None

    if tourne_deja():
        print('vfes.exe TOURNE deja : fermez-le (deux instances se disputent '
              'le journal).')
        return 1

    garde = ENTREES + '.avant_essai'
    shutil.copy2(ENTREES, garde)
    try:
        # LA CONFIGURATION DU DEPOT EST GARDEE, et le scenario n AJOUTE que
        # ses pas. La remplacer entierement perdait journal_fichier,
        # sauvegarde, manette_joueur... -- et sans journal_fichier, aucun
        # journal : premiere lecon de ce banc d essai.
        with io.open(garde, encoding='latin-1') as fp:
            config = [l for l in fp.read().splitlines()
                      if not l[:1].isdigit()]
        with io.open(scenario, encoding='latin-1') as fp:
            pas = fp.read().splitlines()
        with io.open(ENTREES, 'w', encoding='latin-1', newline='\n') as fp:
            fp.write('\n'.join(config + ['', '# --- le scenario ---'] + pas))
            fp.write('\n')
        if os.path.exists(JOURNAL):
            os.remove(JOURNAL)
        print('scenario : %s' % os.path.basename(scenario))
        print('lancement de vfes.exe pour %d s...' % secondes)
        p = subprocess.Popen([EXE], cwd=VF5)
        t = time.time()
        # LES CAPTURES : --vue 30,45 prend une image a ces secondes-la. Le
        # journal dit quels boutons sont partis, la capture dit ce que le jeu
        # en a fait -- et c est la seule facon de savoir OU est le curseur.
        vues = []
        if '--vue' in argv:
            vues = sorted(int(x) for x in argv[argv.index('--vue') + 1].split(','))
        prises = []
        while time.time() - t < secondes:
            while vues and time.time() - t >= vues[0]:
                n = os.path.join(RACINE, 'analysis', '_essai_%02ds.png' % vues[0])
                subprocess.run([sys.executable,
                                os.path.join(RACINE, 'tools', 'capture_fenetre.py'),
                                n, '--titre', 'Virtua'], capture_output=True)
                prises.append(n)
                vues.pop(0)
            if p.poll() is not None:
                print('   le jeu s est ferme seul au bout de %.0f s'
                      % (time.time() - t))
                break
            time.sleep(1.0)
        if p.poll() is None:
            p.terminate()
            try:
                p.wait(timeout=10)
            except subprocess.TimeoutExpired:
                p.kill()
        # le jeu peut laisser un fils ; on s assure que la place est libre
        subprocess.run(['taskkill', '/f', '/im', 'vfes.exe'],
                       capture_output=True)
    finally:
        shutil.copy2(garde, ENTREES)
        os.remove(garde)

    print()
    for n in prises:
        print('capture : %s (%s)'
              % (n, 'ecrite' if os.path.exists(n) else 'MANQUEE'))
    print()
    if not os.path.exists(JOURNAL):
        print('aucun journal : le stub n a pas ecrit (journal_fichier = 0 ?)')
        return 1
    with open(JOURNAL, encoding='latin-1') as fp:
        lignes = fp.read().splitlines()
    print('journal : %d lignes' % len(lignes))
    if motif:
        gardees = [l for l in lignes if motif in l]
        print('   %d avec " %s " :' % (len(gardees), motif))
        for l in gardees:
            print('   %s' % l)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
