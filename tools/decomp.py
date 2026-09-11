#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Decompile des fonctions du moteur, par adresse, avec Ghidra en headless.

Ghidra EST installe sur cette machine (je l'avais cru absent le 2026-09-10 pour
avoir regarde dans `Program Files` : il est ailleurs). Le projet d'analyse est
`ghidra/vf5fs_apm3`, deja construit -- l'analyse complete de la DLL prend
107 secondes, et elle n'est a refaire que si le binaire change.

    py -3 tools/decomp.py 0x1800F9C60
    py -3 tools/decomp.py 0x1800F9C60 0x18006F620 --sortie analysis/objsets.c

Chaque adresse est cherchee DANS sa fonction, pas a son debut : on cite
d'ordinaire une instruction. Sans `--sortie`, le C est ecrit dans
`analysis/decomp.c` ET affiche.

CE QUE CA CHANGE, ET C'EST FREDERIC QUI L'A DEMANDE : quatre tours de sondes
n'avaient pas trouve pourquoi le decor ajoute restait sur son ecran de
chargement. Le C de deux fonctions l'a donne en vingt minutes -- une table
indexee par l'etage, `0x18034D570`, lue au-dela de ses 41 entrees. Les sondes
restent utiles pour ce qui ne se lit pas (quelle branche s'execute, quelle
valeur vit dans un champ), pas pour comprendre un algorithme.
"""
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)

GHIDRA = os.path.join('C:' + os.sep, 'Users', 'frede', 'Desktop',
                      'Nouveau dossier', 'ghidra_12.1.2_PUBLIC_20260605',
                      'ghidra_12.1.2_PUBLIC', 'support', 'analyzeHeadless.bat')
PROJET = os.path.join(RACINE, 'ghidra')
NOM = 'vf5fs_apm3'
PROGRAMME = 'vf5fs_apm3_origine.dll'      # la copie de `.origine`, importee
SCRIPTS = os.path.join(ICI, 'ghidra')


def main():
    argv = sys.argv[1:]
    sortie = os.path.join(RACINE, 'analysis', 'decomp.c')
    if '--sortie' in argv:
        i = argv.index('--sortie')
        sortie = argv[i + 1]
        del argv[i:i + 2]
    adresses = [a for a in argv if not a.startswith('--')]
    if not adresses:
        print(__doc__)
        return 1
    if not os.path.exists(GHIDRA):
        print('analyzeHeadless introuvable : %s' % GHIDRA)
        return 1
    # Ghidra veut des adresses sans « 0x ».
    adresses = [a[2:] if a.lower().startswith('0x') else a for a in adresses]
    cmd = [GHIDRA, PROJET, NOM, '-process', PROGRAMME, '-noanalysis',
           '-scriptPath', SCRIPTS, '-postScript', 'DecompVF5.java',
           os.path.abspath(sortie)] + adresses
    r = subprocess.run(cmd, capture_output=True, text=True)
    for ligne in (r.stdout or '').splitlines():
        if 'DecompVF5' in ligne or 'ERROR' in ligne:
            print(ligne.strip())
    if r.returncode:
        print(r.stderr[-2000:] if r.stderr else '(pas de sortie d erreur)')
        return r.returncode
    if os.path.exists(sortie):
        print()
        print(open(sortie, encoding='utf-8', errors='replace').read())
    return 0


if __name__ == '__main__':
    sys.exit(main())
