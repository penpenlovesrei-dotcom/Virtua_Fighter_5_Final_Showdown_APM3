#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lit -- et modifie -- la configuration passee a `module_start`.

YAMP (CookiePLMonster) montre que le moteur PXD n'est pas pilote par ses etats
mais par un **appel de module** :

    using module_func_t = int(*)(size_t args, const void* argp);
    module_start(args, &config);

et que `config` est un `vf5fs_game_config_t` portant **le mode de jeu, la langue,
la difficulte, l'energie, les rounds et le temps**. YAMP y passe son propre
`m_arcadeMode`.

Notre moteur exporte exactement `module_start` et `module_stop`, et rien
d'autre. C'est donc `vfes.exe` qui decide du mode -- et forcer des sous-etats
apres coup, comme on l'a fait toute la journee, arrive trop tard : le mode a
deja choisi ce qu'il charge. C'est l'explication la plus simple du menu console
qui s'affiche vide.

Convention Microsoft x64 : `rcx` = args, `rdx` = pointeur de configuration.

Usage :
    py -3 tools/config_module.py                    lit et affiche la config
    py -3 tools/config_module.py --octet 4 1        met la config[4] a 1
    py -3 tools/config_module.py --mot 8 3          met le u32 a l'octet 8 a 3
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                          # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')
SCENARIO_ACTIF = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'apm_entrees.txt')
TAILLE = 0x80          # on regarde large, la structure exacte est inconnue


def depl_export(chemin, nom):
    import pefile
    pe = pefile.PE(chemin, fast_load=True)
    pe.parse_data_directories([pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT']])
    for e in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if e.name and e.name.decode() == nom:
            return e.address
    return None


def main():
    argv = sys.argv[1:]
    secondes = 45
    ecritures = []
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    i = 0
    while i < len(argv):
        if argv[i] == '--octet':
            ecritures.append(('B', int(argv[i + 1], 0), int(argv[i + 2], 0)))
            i += 2
        elif argv[i] == '--mot':
            ecritures.append(('I', int(argv[i + 1], 0), int(argv[i + 2], 0)))
            i += 2
        i += 1
    scenario = os.path.join(RACINE, 'tools', 'scenarios', 'jouer.txt')
    if '--scenario' in argv:
        scenario = argv[argv.index('--scenario') + 1]

    rva = depl_export(os.path.join(RACINE, 'runtime', 'media', 'vf5fs', MOTEUR),
                      'module_start')
    if rva is None:
        print('module_start introuvable')
        return 1
    print('module_start : RVA 0x%X' % rva)

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 20
    journal = os.path.join(RACINE, 'analysis', 'config_module.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'vu': 0}

    def sur_bp(d, bp, ctx, tid):
        et['vu'] += 1
        args, argp = ctx.Rcx, ctx.Rdx
        d.dire('  module_start(args=0x%X, argp=0x%X)' % (args, argp))
        if not argp:
            return
        av = d.read(argp, TAILLE)
        if not av:
            d.dire('  configuration illisible')
            return
        for k in range(0, TAILLE, 16):
            mots = struct.unpack_from('<4I', av, k)
            d.dire('    +0x%02X : %s   |  %s' % (k,
                   ' '.join('%08X' % m for m in mots),
                   ' '.join('%02X' % b for b in av[k:k + 16])))
        # Les pointeurs de la structure menent aux contextes et a la config
        # de jeu. On regarde ou ils pointent et ce qu'ils contiennent.
        d.dire('  --- ce que designent les pointeurs ---')
        import struct as _s
        for k in range(0, TAILLE, 8):
            v = _s.unpack_from('<Q', av, k)[0]
            if not (0x10000 < v < 0x7FFFFFFFFFFF):
                continue
            nom_mod, dep = d.module_of(v)
            cible = d.read(v, 32)
            if not cible:
                continue
            txt = ''
            brut = cible.split(bytes([0]), 1)[0]
            if 2 <= len(brut) <= 24 and all(32 <= c < 127 for c in brut):
                txt = '  "%s"' % brut.decode('latin-1')
            d.dire('    +0x%02X -> 0x%X (%s+0x%X)%s' % (k, v, nom_mod, dep, txt))
            d.dire('           %s' % ' '.join('%02X' % b for b in cible[:24]))
        for typ, off, val in ecritures:
            fmt = '<B' if typ == 'B' else '<I'
            avant = struct.unpack_from(fmt, av, off)[0]
            d.write(argp + off, struct.pack(fmt, val))
            d.dire('  >>> config+0x%X : %d -> %d' % (off, avant, val))

    def tic(d, t):
        if et['pose']:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['pose'] = True
        bp = instrument.PointArret('module_start', b + rva, max_coups=8)
        bp.silencieux = True
        d.bps.append(bp)
        d.armer_logiciel(bp)
        d.dire('  point d\'arret sur module_start = 0x%X, a t=%.1f s' % (b + rva, t))

    dbg.on_bp = sur_bp
    dbg.tic = tic
    if scenario and os.path.exists(scenario):
        with open(scenario, 'rb') as fp:
            data = fp.read()
        with open(SCENARIO_ACTIF, 'wb') as fp:
            fp.write(data)
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()
    with open(journal, encoding='utf-8') as fp:
        for l in fp:
            if l.startswith('  '):
                sys.stdout.write(l)
    return 0


if __name__ == '__main__':
    sys.exit(main())
