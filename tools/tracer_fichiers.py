#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Journalise les fichiers que le moteur demande au SYSTEME.

Pourquoi : pour savoir si un decor de VF5 R est importable, la premiere question
n'est pas « le format est-il compatible » mais « le moteur regarde-t-il seulement
sur le disque ? ». Les donnees de jeu sont dans `vf5fs_data.par` (3,99 Go,
conteneur PARC) ; seuls `rom/movie` et `rom/sound` sont en fichiers libres. Si le
moteur ne tente jamais d'ouvrir `rom/objset/...` sur le disque, poser un fichier
la ne servira jamais a rien -- et aucune capture d'ecran ne le dira.

On ne devine donc pas a l'image : **on met un point d'arret sur `CreateFileW` et
`CreateFileA` de KernelBase**, et on lit le chemin demande. C'est la reponse
directe, et elle ne depend ni du decor tire au sort ni de ce qu'on croit voir.

Usage :
    py -3 tools/tracer_fichiers.py --secondes 90
    py -3 tools/tracer_fichiers.py --filtre objset,stg --secondes 120
"""
import ctypes
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')
MODULES = ('KERNELBASE.dll', 'KERNEL32.DLL')
FONCTIONS = ('CreateFileW', 'CreateFileA')

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
k32.GetModuleHandleW.restype = ctypes.c_void_p
k32.GetProcAddress.restype = ctypes.c_void_p
k32.GetProcAddress.argtypes = [ctypes.c_void_p, ctypes.c_char_p]


def deplacement(module, fonction):
    """Le decalage de la fonction dans SA dll, mesure sur notre propre
    processus : meme machine, meme version, donc meme decalage. Seule la base
    change (ASLR), et on la lit dans les evenements de chargement."""
    h = k32.GetModuleHandleW(module)
    if not h:
        h = k32.LoadLibraryW(module)
    if not h:
        return None
    p = k32.GetProcAddress(ctypes.c_void_p(h), fonction.encode())
    return (p - h) if p else None


def main():
    argv = sys.argv[1:]
    secondes = 90
    filtres = ['objset', 'stg', '.farc', '.par']
    scenario = os.path.join(RACINE, 'tools', 'scenarios', 'select_a.txt')
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    if '--filtre' in argv:
        filtres = [x.strip().lower() for x in argv[argv.index('--filtre') + 1].split(',')]
    if '--tout' in argv:
        filtres = []
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]
    journal = os.path.join(RACINE, 'analysis', 'fichiers_demandes.txt')

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 200000
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'poses': set(), 'vus': {}, 'n': 0}

    def lire_chemin(d, adresse, large):
        if not adresse:
            return None
        brut = d.read(adresse, 520)
        if not brut:
            return None
        if large:
            t = brut.decode('utf-16-le', 'ignore')
            t = t.split('\x00', 1)[0]
        else:
            t = brut.split(b'\x00', 1)[0].decode('latin-1', 'ignore')
        return t or None

    def sur_bp(d, bp, ctx, tid):
        # convention Microsoft x64 : le 1er argument est dans rcx
        chemin = lire_chemin(d, ctx.Rcx, bp.nom.endswith('W'))
        if not chemin:
            return
        bas = chemin.lower()
        if filtres and not any(f in bas for f in filtres):
            return
        et['n'] += 1
        if chemin in et['vus']:
            et['vus'][chemin] += 1
            return
        et['vus'][chemin] = 1
        d.dire('  %s' % chemin)

    def tic(d, t):
        for mod in MODULES:
            for fn in FONCTIONS:
                cle = (mod, fn)
                if cle in et['poses']:
                    continue
                base = d.base_de(mod)
                off = deplacement(mod, fn)
                if not base or off is None:
                    continue
                et['poses'].add(cle)
                bp = instrument.PointArret(fn, base + off, max_coups=200000)
                bp.silencieux = True
                d.bps.append(bp)
                d.armer_logiciel(bp)
                d.dire('  point d\'arret sur %s!%s = 0x%X' % (mod, fn, base + off))

    dbg.on_bp = sur_bp
    dbg.tic = tic

    if scenario and os.path.exists(scenario):
        with open(scenario, 'rb') as fp:
            data = fp.read()
        with open(SCENARIO_ACTIF, 'wb') as fp:
            fp.write(data)
    print('journal : %s ; filtres : %s' % (journal, filtres or 'aucun'))
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    print('\n--- %d ouverture(s) retenue(s), %d chemin(s) distinct(s) ---'
          % (et['n'], len(et['vus'])))
    for c, n in sorted(et['vus'].items(), key=lambda x: -x[1])[:60]:
        print('  %5d x  %s' % (n, c))
    return 0


if __name__ == '__main__':
    sys.exit(main())
