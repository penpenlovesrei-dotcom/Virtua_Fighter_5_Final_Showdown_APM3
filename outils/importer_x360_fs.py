#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Importe la Final Showdown CONSOLE (Xbox 360) dans Ghidra. Une seule fois.

POURQUOI (2026-10-05). Frederic : « importer la Final Showdown console dans
Ghidra ». Jusqu'ici je ne l'avais que DESASSEMBLEE -- `tools/x360_ppc.py`,
capstone sur l'image, instruction par instruction. Ghidra ne portait que la
console de **2007** (projet `vf5x360_2007`, celle du mode Quest) ; le dossier
`ghidra/vf5fs_x360` etait vide.

LA RECETTE EST CELLE DE 2007, consignee au journal (68), et on n'en invente
aucun parametre -- chacun est MESURE sur CETTE image :

  . binaire BRUT a sa base, `PowerPC:BE:64:A2ALT-32addr`. L'image sort deja
    chargee (le decompresseur rend l'image memoire, pas le fichier), donc la
    RVA vaut l'offset et un chargement plat a 0x82000000 est exact ;
  . les fonctions creees depuis `.pdata` AVANT l'analyse (`PdataX360.java`).
    `tools/x360_ppc.py sections` donne `.pdata` en 0x8217DA00, 0x1D8F0 octets
    -- soit 15 086 entrees ;
  . les routines `__savegprlr_N` / `__restgprlr_N` neutralisees par un call
    fixup (`SauvegardesX360.java`). Sans lui Ghidra en fait des fonctions qui
    ne reviennent pas, et tout ce qui suit l'appel est perdu.
    **Leurs adresses ne se recopient PAS de 2007 :** `tools/x360_savegpr.py`
    les trouve dans cette image en cherchant la plus longue suite de
    `std rN,-M(r1)` / `ld rN,-M(r1)`, et les queues confirment
    (`stw r12,-8(r1) ; blr` et `lwz r12 ; mtlr r12 ; blr`). Ici DIX-HUIT
    entrees chacune -- r14 a r31 -- contre seize en 2007.

Usage :
    py -3 tools/importer_x360_fs.py            importe et analyse
    py -3 tools/importer_x360_fs.py --refaire   efface le projet et recommence

Lanceur : tools\importer_x360_fs.cmd
Ensuite : py -3 tools/decomp.py --gen fs360 0x82235068
"""
import os
import shutil
import subprocess
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)

GHIDRA = os.path.join('C:' + os.sep, 'Users', 'frede', 'Desktop',
                      'Nouveau dossier', 'ghidra_12.1.2_PUBLIC_20260605',
                      'ghidra_12.1.2_PUBLIC', 'support', 'analyzeHeadless.bat')
PROJET = os.path.join(RACINE, 'ghidra')
NOM = 'vf5fs_x360'
IMAGE = os.path.join(RACINE, 'extracted', 'X360_FS', 'sel', 'default.img')
SCRIPTS = os.path.join(ICI, 'ghidra')

BASE = 0x82000000
LANGAGE = 'PowerPC:BE:64:A2ALT-32addr'
# mesures de tools/x360_ppc.py sections
PDATA, PDATA_TAILLE = 0x8217DA00, 0x1D8F0
# mesures de tools/x360_savegpr.py sur CETTE image (intervalles INCLUSIFS,
# c'est la convention de SauvegardesX360.java : `for a = debut; a <= fin`)
SAUVE_DEB, SAUVE_FIN = 0x826D8B90, 0x826D8BD4
REST_DEB, REST_FIN = 0x826D8BE0, 0x826D8C24


def main():
    argv = sys.argv[1:]
    if not os.path.exists(GHIDRA):
        print('analyzeHeadless introuvable : %s' % GHIDRA)
        return 1
    if not os.path.exists(IMAGE):
        print('image introuvable : %s' % IMAGE)
        return 1
    gpr = os.path.join(PROJET, NOM + '.gpr')
    rep = os.path.join(PROJET, NOM + '.rep')
    if '--refaire' in argv:
        for c in (gpr, rep):
            if os.path.exists(c):
                shutil.rmtree(c) if os.path.isdir(c) else os.remove(c)
                print('efface : %s' % os.path.relpath(c, RACINE))
    if os.path.exists(gpr):
        print('Le projet %s existe deja. --refaire pour le reconstruire.' % NOM)
        return 0
    # Un dossier `ghidra/vf5fs_x360` VIDE traine depuis une tentative
    # precedente : il n'est pas un projet (pas de .gpr) et gene l'import.
    nu = os.path.join(PROJET, NOM)
    if os.path.isdir(nu) and not os.listdir(nu):
        os.rmdir(nu)
        print('dossier vide retire : %s' % os.path.relpath(nu, RACINE))

    cmd = [GHIDRA, PROJET, NOM,
           '-import', IMAGE,
           '-loader', 'BinaryLoader',
           '-loader-baseAddr', '0x%X' % BASE,
           '-processor', LANGAGE,
           '-scriptPath', SCRIPTS,
           '-preScript', 'PdataX360.java', '0x%X' % PDATA,
           '0x%X' % PDATA_TAILLE,
           '-preScript', 'SauvegardesX360.java',
           '0x%X' % SAUVE_DEB, '0x%X' % SAUVE_FIN,
           '0x%X' % REST_DEB, '0x%X' % REST_FIN]
    print('Image   : %s (%.1f Mo)'
          % (os.path.relpath(IMAGE, RACINE), os.path.getsize(IMAGE) / 1e6))
    print('Projet  : ghidra/%s   langage %s' % (NOM, LANGAGE))
    print('.pdata  : 0x%X, 0x%X octets (%d entrees)'
          % (PDATA, PDATA_TAILLE, PDATA_TAILLE // 8))
    print('savegpr : 0x%X..0x%X   restgpr : 0x%X..0x%X'
          % (SAUVE_DEB, SAUVE_FIN, REST_DEB, REST_FIN))
    print()
    print('L analyse de 15 000 fonctions prend du temps. Sortie complete :')
    print()
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout or '') + (r.stderr or '')
    # On NE FILTRE PAS une sortie de construction : on garde ce qui informe,
    # et on dit tout le reste en cas d'echec.
    for ligne in out.splitlines():
        if any(m in ligne for m in ('PdataX360', 'SauvegardesX360', 'ERROR',
                                    'WARN ', 'Exception', 'INFO ANALYZING',
                                    'INFO REPORT', 'Import failed')):
            print('   %s' % ligne.strip())
    print()
    print('termine en %.0f s, code %d' % (time.time() - t0, r.returncode))
    if r.returncode:
        print()
        print(out[-4000:])
        return r.returncode
    print()
    print('Verifiez : py -3 tools/decomp.py --gen fs360 0x82235068')
    return 0


if __name__ == '__main__':
    sys.exit(main())
