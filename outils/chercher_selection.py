#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cherche le GLOBAL qui porte le personnage choisi a l'ecran de selection.

Pourquoi pas un point d'arret en ecriture sur `ROB+0x10` : essaye, zero acces en
245 secondes. L'indice y est ecrit UNE fois, a la construction du ROB -- donc
avant que l'adresse du ROB existe, donc avant qu'on puisse l'armer. Le champ est
un aboutissement, pas une source.

La source est en amont, dans une donnee statique : entre `APM3_SELECTOR` et
`APM3_GAME_VS`, le choix doit bien etre range quelque part. On le trouve comme on
trouverait une vie infinie : par BALAYAGE de la memoire, deux fois, avec deux
choix differents.

  passe A : scenario qui valide le curseur ou il est          -> personnages (a1, a2)
  passe B : scenario qui deplace le curseur avant de valider  -> (b1, b2)

Les adresses qui portaient a1 en A et b1 en B sont les candidats. On ne retient
que les regions d'IMAGE : leurs adresses sont stables d'une execution a l'autre
(module + deplacement), contrairement au tas.

Usage :
    py -3 tools/chercher_selection.py --scenario tools/scenarios/select_a.txt \
        --sortie analysis/selection_a.txt
"""
import ctypes
import os
import struct
import sys
from ctypes import wintypes

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
MOTH_APPLY_RECORD = 0x158B40
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')
PERSOS = ['AKI', 'SAR', 'LAU', 'SHU', 'JEF', 'PAI', 'JAK', 'KAG', 'LIO', 'WOL',
          'AOI', 'LEI', 'VAN', 'BRA', 'GOH', 'MON', 'MSK', 'KRT', 'TAK', '?19', 'DUR']

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
MEM_COMMIT, MEM_IMAGE, MEM_PRIVATE = 0x1000, 0x1000000, 0x20000
LISIBLE = (0x02, 0x04, 0x08, 0x20, 0x40, 0x80)   # PAGE_READ*/EXEC*


class MBI(ctypes.Structure):
    _fields_ = [('BaseAddress', ctypes.c_void_p), ('AllocationBase', ctypes.c_void_p),
                ('AllocationProtect', wintypes.DWORD), ('__a', wintypes.DWORD),
                ('RegionSize', ctypes.c_size_t), ('State', wintypes.DWORD),
                ('Protect', wintypes.DWORD), ('Type', wintypes.DWORD),
                ('__b', wintypes.DWORD)]


k32.VirtualQueryEx.argtypes = [wintypes.HANDLE, ctypes.c_void_p,
                               ctypes.POINTER(MBI), ctypes.c_size_t]
k32.VirtualQueryEx.restype = ctypes.c_size_t


def regions(hproc, types):
    """PIEGE : sans argtypes, ctypes tronque l'adresse a 32 bits et le balayage
    ne rend RIEN, sans erreur -- c'est le « 0.0 Mo lus » du premier essai."""
    a, out = 0, []
    mbi = MBI()
    while a < 0x00007FFFFFFF0000:
        if not k32.VirtualQueryEx(hproc, ctypes.c_void_p(a), ctypes.byref(mbi),
                                  ctypes.sizeof(mbi)):
            break
        base = mbi.BaseAddress or 0
        taille = mbi.RegionSize or 0x1000
        if (mbi.State == MEM_COMMIT and mbi.Type in types
                and (mbi.Protect & 0xFF) in LISIBLE and not (mbi.Protect & 0x100)):
            out.append((base, taille))
        a = base + taille
    return out


def balayer(dbg, valeurs, types):
    """Rend ({valeur: [adresses]}, octets lus) pour les dwords alignes."""
    trouve = {v: [] for v in valeurs}
    vus = 0
    for base, taille in regions(dbg.hproc, types):
        if taille > (64 << 20):
            continue
        blob = dbg.read(base, taille)
        if not blob:
            continue
        vus += len(blob)
        for v in valeurs:
            cible = struct.pack('<I', v)
            i = blob.find(cible)
            while i >= 0:
                if i % 4 == 0:
                    trouve[v].append(base + i)
                i = blob.find(cible, i + 1)
    return trouve, vus


def main():
    argv = sys.argv[1:]
    scenario = os.path.join(RACINE, 'tools', 'scenarios', 'combat_long.txt')
    sortie = os.path.join(RACINE, 'analysis', 'selection.txt')
    secondes, pose_a, balayer_a = 120, 55.0, 70.0
    portee = 'image'
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]
    if '--sortie' in argv:
        sortie = argv[argv.index('--sortie') + 1]
    if '--portee' in argv:
        portee = argv[argv.index('--portee') + 1]
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    if '--a' in argv:
        pose_a = float(argv[argv.index('--a') + 1])
    if '--balayer' in argv:
        balayer_a = float(argv[argv.index('--balayer') + 1])
    types = (MEM_IMAGE,) if portee == 'image' else (MEM_IMAGE, MEM_PRIVATE)

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 12
    et = {'pose': False, 'robs': [], 'persos': [], 'fait': False}

    def nom(c):
        return PERSOS[c] if c is not None and 0 <= c < len(PERSOS) else '?'

    def sur_bp(d, bp, ctx, tid):
        rob = ctx.Rdx
        if rob and rob not in et['robs']:
            c = d.u32(rob + 0x10)
            et['robs'].append(rob)
            et['persos'].append(c)
            d.dire('  ROB %d = 0x%X   personnage %s (%s)'
                   % (len(et['robs']), rob, c, nom(c)))
        if len(et['robs']) >= 2:
            d.desarmer_logiciel(bp)

    def tic(d, t):
        if et['fait']:
            return
        if not et['pose']:
            if t < pose_a:
                return
            b = d.base_de(MOTEUR)
            if not b:
                return
            et['pose'] = True
            bp = instrument.PointArret('MothApplyRecord', b + MOTH_APPLY_RECORD,
                                       max_coups=12)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
            return
        if t < balayer_a or len(et['persos']) < 2:
            return
        et['fait'] = True
        # on saute la valeur 0 : elle est partout, et AKI=0 rendrait le
        # balayage inexploitable (des millions d'adresses).
        vals = sorted(set(x for x in et['persos'] if x))
        d.dire('  balayage (%s) pour les valeurs %s...' % (portee, vals))
        trouve, vus = balayer(d, vals, types)
        d.dire('  %.1f Mo lus' % (vus / 1048576.0))
        with open(sortie, 'w', encoding='utf-8') as fp:
            fp.write('# personnages : %s\n'
                     % ' '.join('%s=%s' % (c, nom(c)) for c in et['persos']))
            for v in vals:
                for a in trouve[v]:
                    mod = d.module_of(a)
                    if mod:
                        base = d.base_de(mod)
                        fp.write('%s+0x%X %d\n' % (mod, a - base, v))
                    else:
                        fp.write('0x%X %d\n' % (a, v))
                d.dire('  valeur %2d : %d adresse(s)' % (v, len(trouve[v])))
        d.dire('  ecrit dans %s' % sortie)

    dbg.on_bp = sur_bp
    dbg.tic = tic

    with open(scenario, 'rb') as fp:
        data = fp.read()
    with open(SCENARIO_ACTIF, 'wb') as fp:
        fp.write(data)
    print('scenario : %s ; balayage a t=%.0f s ; sortie %s'
          % (scenario, balayer_a, sortie))
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    return 0


if __name__ == '__main__':
    sys.exit(main())
