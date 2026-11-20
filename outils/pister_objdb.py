#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""D'ou vient l'`obj_db.bin` que le moteur charge, et combien de jeux y trouve-t-il ?

L'ENIGME, mesuree le 2026-09-10

Le vecteur d'objsets du moteur (`[[0x18070FA90]]`, enregistrements de 0x200,
cle en tete, dichotomie en `0x1800F9450`) contient **6044** entrees -- le compte
de l'`obj_db.bin` D'ORIGINE. Le notre en a 6045, et notre objset 6150 est absent,
donc la geometrie du decor ajoute n'est jamais demandee : `stgd5r.farc` n'est
jamais ouvert et le chargement ne finit pas.

Or :

  . le nom `obj_db.bin` est MASQUE dans l'index du `.par` (essaye des deux
    facons : dernier caractere, puis premier) ;
  . `tracer_fichiers.py --tout` ne montre AUCUNE ouverture d'un chemin
    `rom/objset/...` sur le disque -- seul le `.par` est ouvert ;
  . retirer notre fichier pose ne change rien : toujours 6044.

Les trois ensemble sont impossibles, donc l'une de mes lectures est fausse.
Cette sonde va voir, au lieu de raisonner : elle pose des points d'arret dans le
chargeur `0x1800F97E0` et lit ce qui en sort.

    0x1800F97E9  mov rbx, [0x18070FA88]      le gestionnaire
    0x1800F97F0  cmp byte [rbx+0x90], 0      deja charge ? on saute
    0x1800F9803  "./rom/objset/"  puis  "obj_db.bin"  ->  [rsp+0x20]
    0x1800F9836  call 0x180217E70(rbx, chemin, 0)
    0x1800F9846  call 0x180217940(rbx)  ->  rax = les OCTETS
    0x1800F984B  mov [rbx+0x98], rax

On lit donc, au dernier point : l'adresse rendue, et les vingt premiers octets.
Le premier dword est le nombre de jeux -- **6044 = l'origine, 6045 = le notre**.
Cela tranche sans discussion d'ou viennent les octets.

    py -3 tools/pister_objdb.py
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                              # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
EXE = os.path.join(JEU, 'vfes.exe')
SCENARIO_ACTIF = os.path.join(JEU, 'apm_entrees.txt')
SCENARIO = """# ecrit par tools/pister_objdb.py -- aucune entree.
front   = 10
journal = 0
clavier = 1
manette = 1
0       rien
"""

ENTREE = 0x0F97E0          # le chargeur d'obj_db
APRES_CHEMIN = 0x0F982B    # le chemin est compose, il est en [rsp+0x20]
APRES_LECTURE = 0x0F984B   # rax = les octets
GEST_RVA = 0x70FA88


def main():
    argv = sys.argv[1:]
    secondes = 60
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])
    journal = os.path.join(RACINE, 'analysis', 'pister_objdb.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.sortie = fichier
    dbg.bp_max = 200000
    et = {'pose': False, 'base': 0}

    def sur_bp(d, bp, ctx, tid):
        b = et['base']
        if bp.nom == 'entree':
            gest = d.u64(b + GEST_RVA) or 0
            drapeau = (d.read(gest + 0x90, 1) or b'\xff')[0] if gest else 255
            d.dire('  CHARGEUR obj_db appele : gestionnaire 0x%X, '
                   '+0x90 (deja charge) = %d' % (gest, drapeau))
            return
        if bp.nom == 'chemin':
            chemin = d.cstr(ctx.Rsp + 0x20, 200)
            d.dire('  chemin compose : %r' % chemin)
            return
        if bp.nom == 'octets':
            a = ctx.Rax
            brut = d.read(a, 20) or b''
            n = struct.unpack_from('<I', brut, 0)[0] if len(brut) >= 4 else -1
            d.dire('  octets rendus a 0x%X : %s' % (a, brut.hex()))
            d.dire('  --> nombre de jeux = %d  (%s)'
                   % (n, '6045 = LE NOTRE' if n == 6045 else
                      '6044 = L ORIGINE' if n == 6044 else 'inattendu'))
            mod, off = d.module_of(a)
            d.dire('      (module de cette adresse : %s+0x%X)' % (mod, off))

    def tic(d, t):
        if et['pose']:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['base'] = b
        et['pose'] = True
        for nom, rva in (('entree', ENTREE), ('chemin', APRES_CHEMIN),
                         ('octets', APRES_LECTURE)):
            bp = instrument.PointArret(nom, b + rva, max_coups=200000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  trois points d\'arret poses a t=%.1f s' % t)

    dbg.on_bp = sur_bp
    dbg.tic = tic
    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)
    print('MESURE : d ou viennent les octets d obj_db.bin ?')
    print('  Aucune navigation. journal : %s' % journal)
    dbg.run(EXE, JEU, secondes, ())
    fichier.close()
    print('Journal ecrit : %s' % journal)
    return 0


if __name__ == '__main__':
    sys.exit(main())
