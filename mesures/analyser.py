#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Reconstruit la base Ghidra du moteur APM3, puis MESURE la couverture.

Pourquoi ce script existe. La base Ghidra du depot d'origine ne contenait
AUCUNE annotation humaine : pas un seul symbole `USER_DEFINED` sur les
13 859 fonctions du moteur. La transporter n'aurait donc rien apporte --
elle est entierement reproductible, et l'analyse complete prend environ
deux minutes. Ce script la refait, et affiche les memes chiffres que
`ETAT_DECOMPILATION.md` pour que tu puisses verifier qu'ils sont justes.

    py -3 mesures/analyser.py                 le moteur (la DLL)
    py -3 mesures/analyser.py --exe           l'executable vfes.exe
    py -3 mesures/analyser.py --mesure-seule  sans reanalyser
    py -3 mesures/analyser.py --decompile 0x180171F40 [...]

OU TROUVE-T-IL GHIDRA. Dans cet ordre : la variable d'environnement
GHIDRA_HOME, puis `ghidra*/support/analyzeHeadless.bat` sous le Bureau,
les disques C: et D:, et `%LOCALAPPDATA%`. S'il echoue, pose
GHIDRA_HOME a la main :

    set GHIDRA_HOME=C:\ghidra_11.0_PUBLIC
"""
import glob
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
BINAIRES = os.path.join(RACINE, 'binaires')
PROJET = os.path.join(ICI, 'projet')

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll.origine'
EXE = 'vfes.exe.origine'


def trouver_ghidra():
    """Le chemin de analyzeHeadless.bat, ou None."""
    h = os.environ.get('GHIDRA_HOME')
    if h:
        p = os.path.join(h, 'support', 'analyzeHeadless.bat')
        if os.path.exists(p):
            return p
    motifs = []
    for base in (os.path.expanduser(r'~\Desktop'), 'C:\\', 'D:\\',
                 os.environ.get('LOCALAPPDATA', ''),
                 os.path.expanduser('~')):
        if not base:
            continue
        motifs += [os.path.join(base, 'ghidra*', 'support',
                                'analyzeHeadless.bat'),
                   os.path.join(base, '*', 'ghidra*', 'support',
                                'analyzeHeadless.bat'),
                   os.path.join(base, '*', 'ghidra*', 'ghidra*', 'support',
                                'analyzeHeadless.bat')]
    for m in motifs:
        trouves = sorted(glob.glob(m))
        if trouves:
            return trouves[-1]
    return None


def lancer(gh, nom_projet, args):
    cmd = [gh, PROJET, nom_projet] + args
    r = subprocess.run(cmd, capture_output=True, text=True)
    sortie = (r.stdout or '') + (r.stderr or '')
    cles = ('MESURE', 'FONCTIONS', 'FN_PAR', 'SYMBOLES', 'AUTRES', 'COUV',
            'CATEGORIES', '###')
    for ligne in sortie.splitlines():
        if '> ' in ligne and any(k in ligne for k in cles):
            t = ligne.split('> ', 1)[1].strip()
            if t.endswith('(GhidraScript)'):
                t = t[:-len('(GhidraScript)')].rstrip()
            print('   ' + t)
        elif 'ERROR' in ligne and 'REPORT' in ligne:
            print('   ' + ligne.strip())
    return r.returncode, sortie


def main():
    av = sys.argv[1:]
    cible = EXE if '--exe' in av else MOTEUR
    nom = 'vfes' if '--exe' in av else 'moteur_apm3'
    binaire = os.path.join(BINAIRES, cible)

    gh = trouver_ghidra()
    if not gh:
        print(__doc__)
        print('analyzeHeadless.bat INTROUVABLE. Pose GHIDRA_HOME.')
        return 1
    print('Ghidra  : %s' % gh)
    if not os.path.exists(binaire):
        print('binaire absent : %s' % binaire)
        return 2
    print('binaire : %s' % binaire)
    os.makedirs(PROJET, exist_ok=True)

    deja = os.path.exists(os.path.join(PROJET, nom + '.gpr'))
    if not deja and '--mesure-seule' not in av:
        print('')
        print('Import et analyse (environ deux minutes pour le moteur)...')
        c, s = lancer(gh, nom, ['-import', binaire, '-scriptPath', ICI])
        if c:
            print(s[-2000:])
            return c
        print('   analyse terminee.')
    elif deja:
        print('projet deja construit : %s' % PROJET)
    else:
        print('')
        print('Il n y a pas encore de projet pour "%s", et tu as demande' % nom)
        print('--mesure-seule : il n y a donc rien a mesurer. Relance sans.')
        return 3

    if '--decompile' in av:
        i = av.index('--decompile')
        adr = [a[2:] if a.lower().startswith('0x') else a
               for a in av[i + 1:] if not a.startswith('--')]
        sortie = os.path.join(ICI, 'decomp.c')
        print('')
        print('Decompilation de %d adresse(s) -> %s' % (len(adr), sortie))
        lancer(gh, nom, ['-noanalysis', '-readOnly', '-process', '*',
                         '-scriptPath', ICI, '-postScript', 'DecompVF5.java',
                         sortie] + adr)
        if os.path.exists(sortie):
            print(open(sortie, encoding='utf-8', errors='replace').read())
        return 0

    print('')
    print('MESURE DE COUVERTURE')
    lancer(gh, nom, ['-noanalysis', '-readOnly', '-process', '*',
                     '-scriptPath', ICI, '-postScript', 'CompterVF5.java'])
    print('')
    print('CLASSEMENT DES NOMS DE FONCTIONS')
    lancer(gh, nom, ['-noanalysis', '-readOnly', '-process', '*',
                     '-scriptPath', ICI, '-postScript', 'ClasserNoms.java'])

    print('')
    print('COUVERTURE : les fonctions que ce dossier touche vraiment')
    adr = os.path.join(ICI, 'adresses_%s.txt' % nom)
    subprocess.run([sys.executable, '-I',
                    os.path.join(ICI, 'extraire_adresses.py'), adr]
                   + (['--exe'] if '--exe' in av else []),
                   check=False)
    if os.path.exists(adr):
        lancer(gh, nom, ['-noanalysis', '-readOnly', '-process', '*',
                         '-scriptPath', ICI, '-postScript', 'CouvVF5.java',
                         adr])
        print('   COUV_TOUT = citees n importe ou ; COUV_DOCS = dans un .md')
    print('')
    print('Compare ces chiffres a ETAT_DECOMPILATION.md.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
