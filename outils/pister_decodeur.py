#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Un decodeur video est-il PRESENT mais non enregistre, ou absent ?

C'est la question qui decide entre les deux routes pour caler une video a la
place de l'animation de titre.

Dans CRI Mana, la selection du decodeur passe par une table (`vfes.exe`) :

    0x1400D629F  test r9, r9              ; r9 = nombre de decodeurs inscrits
    0x1400D62A2  je  -> "E11030202M:No available decoder is attached..."
    0x1400D62A4  lea rbp, [0x1404241A0]   ; la table, entrees de 0x18 octets
    0x1400D62B0  cmp dword [rax], r8d     ; on y cherche le codec demande

On lit donc DEUX choses :

  * `r9` au moment du test -- combien de decodeurs sont inscrits, et `r8d`,
    quel codec est reclame ;
  * si le chemin d'enregistrement (`0x1400D59D8`) est jamais emprunte.

    decodeurs = 0 et enregistrement jamais appele
        -> le module existe peut-etre, mais rien ne l'inscrit : VERROU, reparable.
    decodeurs = 0 et enregistrement appele
        -> il est appele et echoue : lire pourquoi.
    decodeurs > 0
        -> il y a bien des decodeurs, et c'est le codec reclame qui n'y est pas.

    py -3 tools/pister_decodeur.py --secondes 55
"""
import collections
import os
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                            # noqa: E402

HOTE = 'vfes.exe'
EXE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vfes.exe')

POINTS = [
    ('test du nombre',   0x0D629F),   # test r9, r9
    ('enregistrement A', 0x0D59D8),   # lea rdx, [table]
    ('enregistrement B', 0x0D5AB1),   # lea rdi, [table]
    ('erreur aucun',     0x0D62D5),   # le message "No available decoder"
]
TABLE = 0x1404241A0


def main():
    argv = sys.argv[1:]
    secondes = 55
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.bp_max = 400
    journal = os.path.join(RACINE, 'analysis', 'pister_decodeur.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg.sortie = fichier
    et = {'pose': False, 'compte': collections.Counter(), 't0': None,
          'base': None, 'dits': set()}

    def note(t):
        fichier.write(t + os.linesep)
        fichier.flush()

    def sur_bp(d, bp, ctx, tid):
        et['compte'][bp.nom] += 1
        if et['t0'] is None:
            et['t0'] = time.time()
        ms = (time.time() - et['t0']) * 1000.0
        n = et['compte'][bp.nom]

        if bp.nom == 'test du nombre' and n <= 8:
            r9 = ctx.R9 & 0xFFFFFFFFFFFFFFFF
            r8 = ctx.R8 & 0xFFFFFFFF
            note('%9.1f ms  decodeurs inscrits = %d   codec reclame = 0x%X'
                 % (ms, r9, r8))
            # et le contenu de la table, si elle en a
            b = et['base'] or 0
            if r9 and b:
                brut = d.read(b + (TABLE - 0x140000000), min(r9, 4) * 0x18)
                if brut:
                    for k in range(min(r9, 4)):
                        e = brut[k*0x18:(k+1)*0x18]
                        note('              entree %d : id=0x%X  %s'
                             % (k, int.from_bytes(e[0:4], 'little'),
                                e.hex()))
            return
        if bp.nom not in et['dits']:
            et['dits'].add(bp.nom)
            note('%9.1f ms  PREMIERE FOIS : %s' % (ms, bp.nom))

    def tic(d, t):
        if et['pose']:
            return
        b = d.base_de(HOTE)
        if not b:
            return
        et['pose'] = True
        et['base'] = b
        for nom_, rva in POINTS:
            bp = instrument.PointArret(nom_, b + rva, max_coups=100000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
        d.dire('  points poses dans %s, base 0x%X' % (HOTE, b))

    dbg.on_bp = sur_bp
    dbg.tic = tic

    print('MESURE : un decodeur video est-il inscrit ?')
    print('  Laissez tourner. Aucune touche.')
    print()
    dbg.run(EXE, os.path.dirname(EXE), secondes, ())
    fichier.close()

    lignes = []

    def dit(t=''):
        lignes.append(t)

    dit()
    dit('=' * 72)
    dit('COMPTES :')
    for nom_, _ in POINTS:
        dit('   %-18s %d' % (nom_, et['compte'][nom_]))
    dit()
    dit('RELEVE :')
    with open(journal, encoding='utf-8') as fp:
        for l in fp:
            if 'decodeurs inscrits' in l or 'entree ' in l or 'PREMIERE' in l:
                dit('   ' + l.rstrip())
    dit()
    dit('LECTURE :')
    dit('   inscrits = 0 et enregistrement JAMAIS appele -> VERROU, reparable.')
    dit('   inscrits = 0 et enregistrement appele        -> il echoue, lire pourquoi.')
    dit('   inscrits > 0                                 -> le codec reclame n y est pas.')
    bilan = os.path.join(RACINE, 'analysis', 'pister_decodeur_bilan.txt')
    with open(bilan, 'w', encoding='utf-8') as fp:
        fp.write(os.linesep.join(lignes) + os.linesep)
    for t in lignes:
        try:
            print(t)
        except UnicodeEncodeError:
            print(t.encode('ascii', 'replace').decode('ascii'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
