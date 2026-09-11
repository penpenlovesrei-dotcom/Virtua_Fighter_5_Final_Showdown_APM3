#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""QUI ecrit l'indice de decor que le combat charge -- `TaskStage+0x5C`.

POURQUOI CETTE MESURE, ET POURQUOI CELLE-LA

Le chargeur general (`0x18018F8A3`) lit son indice dans `[rsi+0x5C]`, ou `rsi`
est la tache de decor -- `[0x1807499D8]`. Tout le reste n'est que la question
« qui a mis quoi dans ce champ ».

Le 2026-09-09, deux sondes ont donne le meme resultat : **un seul chargement,
`index 39 (gym)`**. Et la troisieme a montre que les trois sites que je
soupconnais -- le choix en dur du mode 1 (`0x18020AE78`), la demande du combat
(`0x1800BC6AD`), le decor maison (`0x1800B8AFF`) -- **ne s'executent JAMAIS**.

Chercher le prochain candidat par la lecture serait refaire la meme erreur une
quatrieme fois. On pose donc un point d'arret MATERIEL en ecriture sur le champ
et on laisse le processeur nommer l'ecrivain -- exactement ce qui avait tranche
l'affaire du1 le 2026-09-08.

CE QU'IL FAUT LIRE DANS LE JOURNAL

  . chaque ligne « ecriture depuis 0x... (rva 0x...) -> <indice> » nomme une
    instruction. La RVA est ce qui compte : elle se cherche dans le binaire ;
  . la DERNIERE avant le chargement est celle qui decide ;
  . les temps permettent de separer ce qui se passe au demarrage (l'attract)
    de ce qui se passe quand vous entrez dans le mode.

Un point d'arret LOGICIEL sur le chargeur est pose en plus, pour qu'on voie
l'ordre : ecritures, puis chargement.

    py -3 tools/pister_5c_stage.py
    py -3 tools/pister_5c_stage.py --secondes 300
"""
import os
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import instrument                                              # noqa: E402

MOTEUR = 'vf5fs-pxd-w64-Retail_APM3.dll'
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
EXE = os.path.join(JEU, 'vfes.exe')
SCENARIO_ACTIF = os.path.join(JEU, 'apm_entrees.txt')
SCENARIO = """# ecrit par tools/pister_5c_stage.py -- le clavier mene.
front   = 10
journal = 0
clavier = 1
manette = 1
0       rien
"""

TACHE_RVA = 0x7499D8           # le singleton TaskStage
CHAMP = 0x5C
CHARGEUR_RVA = 0x0D7130
NOMS = ['tst', 'ts2', 'ts3', 'wht', 'ban', 'ter', 'nyc', 'cas', 'riv', 'jin',
        'sin', 'djo', 'umi', 'hai', 'are', 'slk', 'yuk', 'tak', 'aur', 'bar',
        'tan', 'du1', 'du2', 'du3', 'du4', 'du5', 'trm', 'cid', 'trs', 'evo00',
        'evo01', 'evo02', 'evo03', 'evo04', 'evo05', 'evo06', 'evo07', 'evo08',
        'evo09', 'gym', 'smo', 'ALEA(41)', 'ajoute-42', 'ajoute-43']


def nom(i):
    if i is None:
        return '?'
    if i == 0xFFFFFFFF:
        return '-1'
    return NOMS[i] if 0 <= i < len(NOMS) else str(i)


def main():
    argv = sys.argv[1:]
    secondes = 300
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    journal = os.path.join(RACINE, 'analysis', 'pister_5c_stage.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.sortie = fichier
    dbg.bp_max = 200
    # On veut TOUTES les ecritures, pas les quarante premieres.
    dbg.dr_max = 60
    dbg.dr_auto_desarmer = False
    t0 = time.monotonic()
    et = {'arme': None, 'base': 0, 'adresse': 0, 'pose': False, 'n': 0}

    def sur_dr(d, m, ctx, tid):
        """Le DR se declenche APRES l'ecriture : rip pointe la suivante."""
        et['n'] += 1
        v = d.u32(et['adresse'])
        rva = ctx.Rip - et['base'] if et['base'] else 0
        if et['n'] <= 60:
            d.dire('  t=%6.1f s  ecriture depuis 0x%X (rva 0x%X) -> %s'
                   % (time.monotonic() - t0, ctx.Rip, rva, nom(v)))

    def sur_bp(d, bp, ctx, tid):
        if bp.nom != 'Chargeur':
            return
        index = ctx.Rcx & 0xFFFFFFFF
        retour = d.u64(ctx.Rsp) or 0
        b = d.base_de(MOTEUR) or 0
        d.dire('  t=%6.1f s  CHARGEMENT : index %d (%s)  <- retour rva 0x%X'
               % (time.monotonic() - t0, index, nom(index), retour - b))

    def tic(d, t):
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['base'] = b
        if not et['pose']:
            et['pose'] = True
            bp = instrument.PointArret('Chargeur', b + CHARGEUR_RVA,
                                       max_coups=5000)
            bp.silencieux = True
            d.bps.append(bp)
            d.armer_logiciel(bp)
            d.dire('  point d\'arret sur le chargeur pose a t=%.0f s' % t)
        if et['arme'] is not None:
            return
        tache = d.u64(b + TACHE_RVA)
        if not tache:
            return                      # la tache n'existe pas encore
        et['adresse'] = tache + CHAMP
        et['arme'] = d.armer_materiel(et['adresse'], 4, 'w',
                                      nom='TaskStage+0x5C')
        if et['arme'] is None:
            et['arme'] = False
            return
        d.dire('  DR arme sur 0x%X (t=%.1f s) -- valeur actuelle %s'
               % (et['adresse'], t, nom(d.u32(et['adresse']))))

    dbg.on_dr = sur_dr
    dbg.on_bp = sur_bp
    dbg.tic = tic
    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)

    print('MESURE : qui ecrit l indice de decor que le combat charge.')
    print()
    print('  Le clavier est a VOUS. Allez jusqu au decor comme d habitude,')
    print('  puis fermez le jeu.')
    print('  journal : %s' % journal)
    print()
    dbg.run(EXE, JEU, secondes, ())
    fichier.close()
    print()
    print('Journal ecrit : %s' % journal)
    return 0


if __name__ == '__main__':
    sys.exit(main())
