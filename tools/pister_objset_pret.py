#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""POURQUOI l'objset ajoute ne se declare-t-il jamais PRET ? On compare son
enregistrement a celui d'un objset qui, lui, l'est.

CE QUE LA MESURE PRECEDENTE A ETABLI (analysis/pister_import_d5r.txt)

    t=42,0 s  etat 2  OUVERT : rom/objset/stgd5r.farc   <- la geometrie EST demandee
    t=42,7 s  etat 3  les neuf autres pieces sont ouvertes
    t=43,1 s  etat 4 (derniere attente)  ... et jamais l'etat 5

Et les sept portes de l'etat 3 passent **exactement** comme dans le build qui
marche : 24 24 9 5 5 5 5 1 des deux cotes. Aucune piece ne manque, aucune porte
ne refuse. Le mur est l'etat 4, qui appelle `0x1800F8A40(objset)` :

    0x1800F8A40  ... call 0x1800F9450(id)      l'enregistrement de l'objset
                 test rax, rax        ; je -> PAS pret (introuvable)
    0x1800F8A66  cmp byte [rax+0x90],  0 ; je -> PAS pret
    0x1800F8A6F  cmp byte [rax+0x128], 0 ; je -> PAS pret
    0x1800F8A78  mov dl, 1 ; jmp 0x180217900     PRET
    (et `0x1800F8A90`, la variante voisine, teste `[rax+0x1F4]`)

L'archive est ouverte et lue, et l'objset ne se declare pas pret. Deviner lequel
des sous-systemes -- geometrie, textures, animation -- n'a pas fini serait
repartir dans les hypotheses. On compare donc.

CE QUE CETTE SONDE FAIT

Le gestionnaire garde **un enregistrement de 0x200 octets par objset**, dans un
vecteur trie par identifiant (`[[0x18070FA90]]`, dichotomie en `0x1800F9450`).
Quand `TaskStage` se fige a l'etat 4, la sonde ecrit :

  . l'enregistrement de **notre objset** (6150 par defaut), 128 dwords ;
  . celui d'un objset TEMOIN qui est pret -- par defaut `STGGYM` (2847), le
    decor de la Training Room, que le DOJO charge de toute facon ; a defaut, le
    premier enregistrement rencontre dont les trois drapeaux sont poses ;
  . le **DIFF** des deux, offset par offset ;
  . les trois drapeaux nommes, cote a cote.

Le champ qui differe nomme le sous-systeme qui n'a pas fini. C'est la meme
methode que la comparaison de builds : deux objets de meme forme, un qui marche,
un qui ne marche pas.

    Lancez, allez au DOJO, choisissez le dojo de VF5 R, LAISSEZ le chargement
    tourner (c'est pendant qu'il tourne que la mesure se prend), puis fermez.

    py -3 tools/pister_objset_pret.py
    py -3 tools/pister_objset_pret.py --objset 6150 --temoin 2847
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
SCENARIO = """# ecrit par tools/pister_objset_pret.py -- le clavier mene.
front   = 10
journal = 0
clavier = 1
manette = 1
0       rien
"""

VECTEUR_RVA = 0x70FA90         # -> l'objet qui porte {debut, fin}
PAS = 0x200
TACHE_RVA = 0x7499D8           # TaskStage : +0x58 l'etat, +0x5C le decor
# Les trois octets que `0x1800F8A40` et sa voisine testent.
DRAPEAUX = (0x90, 0x128, 0x1F4)


def vecteur(d, base):
    objet = d.u64(base + VECTEUR_RVA)
    if not objet:
        return None, 0
    tete = d.read(objet, 16)
    if not tete or len(tete) != 16:
        return None, 0
    debut, fin = struct.unpack('<QQ', tete)
    if not debut or fin <= debut:
        return None, 0
    return debut, (fin - debut) // PAS


def tout_lire(d, debut, n):
    """Le vecteur entier en UNE lecture : 6045 x 0x200 = 3 Mo.

    Le lire enregistrement par enregistrement coutait 6045 appels a
    ReadProcessMemory, et le jeu est fige pendant ce temps-la.
    """
    return d.read(debut, n * PAS) or b''


def rang_de(brut, n, cle):
    for k in range(n):
        if struct.unpack_from('<I', brut, k * PAS)[0] == cle:
            return k
    return None


def pret(enr):
    return all(enr[o] for o in DRAPEAUX)


def enregistrement(brut, k):
    e = brut[k * PAS:(k + 1) * PAS]
    return e, (list(struct.unpack('<128I', e)) if len(e) == PAS else [])


def main():
    argv = sys.argv[1:]
    objset = int(argv[argv.index('--objset') + 1], 0) if '--objset' in argv else 6150
    temoin = int(argv[argv.index('--temoin') + 1], 0) if '--temoin' in argv else 2847
    secondes = int(argv[argv.index('--secondes') + 1], 0) if '--secondes' in argv else 300

    journal = os.path.join(RACINE, 'analysis', 'pister_objset_pret.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.sortie = fichier
    et = {'base': 0, 'etat': None, 'fait': False, 'vu4': None}

    def dumper(d, debut, n, t):
        vect = tout_lire(d, debut, n)
        if len(vect) < n * PAS:
            d.dire('  le vecteur n a pas pu etre lu en entier (%d octets)'
                   % len(vect))
            return False
        rn = rang_de(vect, n, objset)
        if rn is None:
            d.dire('  notre objset %d est ABSENT du vecteur -- rien a comparer'
                   % objset)
            return False
        brut_n, mots_n = enregistrement(vect, rn)
        rt = rang_de(vect, n, temoin)
        brut_t, mots_t = (None, [])
        if rt is not None:
            brut_t, mots_t = enregistrement(vect, rt)
        if not brut_t or not pret(brut_t):
            # le temoin demande n'est pas pret : on prend le premier qui l'est
            for k in range(n):
                b, m = enregistrement(vect, k)
                if len(b) == PAS and pret(b):
                    rt, brut_t, mots_t = k, b, m
                    d.dire('  (le temoin %d n etait pas pret : on prend '
                           'l objset %d, rang %d)'
                           % (temoin, m[0], k))
                    break
        if not brut_t:
            d.dire('  aucun objset PRET dans le vecteur -- rien a comparer')
            return False
        cle_t = struct.unpack_from('<I', brut_t, 0)[0]

        d.dire('')
        d.dire('=' * 70)
        d.dire('  t=%6.1f s  COMPARAISON DES ENREGISTREMENTS (0x200 octets)' % t)
        d.dire('  notre objset %d (rang %d)   contre   temoin %d (rang %d)'
               % (objset, rn, cle_t, rt))
        d.dire('=' * 70)
        d.dire('  les trois drapeaux que 0x1800F8A40 teste :')
        for o in DRAPEAUX:
            d.dire('     +0x%03X : le notre = %d      le temoin = %d   %s'
                   % (o, brut_n[o], brut_t[o],
                      '<-- CE DRAPEAU MANQUE' if brut_t[o] and not brut_n[o]
                      else ''))
        d.dire('')
        d.dire('  les dwords qui DIFFERENT (offset, le notre, le temoin) :')
        vus = 0
        for i in range(128):
            if mots_n[i] == mots_t[i]:
                continue
            vus += 1
            if vus <= 48:
                d.dire('     +0x%03X   %08X   %08X' % (i * 4, mots_n[i],
                                                       mots_t[i]))
        d.dire('  %d dword(s) different sur 128.' % vus)
        d.dire('')
        d.dire('  notre enregistrement en entier :')
        for i in range(0, 128, 8):
            d.dire('     +0x%03X  %s' % (i * 4, ' '.join('%08X' % mots_n[j]
                                                         for j in range(i, i + 8))))
        d.dire('')
        d.dire('  celui du temoin :')
        for i in range(0, 128, 8):
            d.dire('     +0x%03X  %s' % (i * 4, ' '.join('%08X' % mots_t[j]
                                                         for j in range(i, i + 8))))
        return True

    def tic(d, t):
        b = d.base_de(MOTEUR)
        if not b:
            return
        et['base'] = b
        tache = d.u64(b + TACHE_RVA) or 0
        if not tache:
            return
        etat = d.u32(tache + 0x58)
        courant = d.u32(tache + 0x5C)
        if etat != et['etat']:
            et['etat'] = etat
            d.dire('  t=%6.1f s  etat %s, decor courant %s'
                   % (t, etat, courant))
            if etat == 4:
                et['vu4'] = t
        if et['fait'] or etat != 4:
            return
        # On laisse deux secondes a l'etat 4 : s'il passe, c'est que tout va
        # bien et il n'y a rien a comparer.
        if et['vu4'] is None or t - et['vu4'] < 2.0:
            return
        debut, n = vecteur(d, b)
        if not debut:
            return
        d.dire('  t=%6.1f s  l etat 4 dure depuis %.1f s : on compare.'
               % (t, t - et['vu4']))
        et['fait'] = dumper(d, debut, n, t)

    dbg.tic = tic
    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)
    print('MESURE : pourquoi l objset %d ne se declare-t-il pas PRET ?' % objset)
    print()
    print('  Le clavier est a VOUS. MENU -> DOJO -> le dojo de VF5 R,')
    print('  et LAISSEZ le chargement tourner : c est pendant qu il tourne')
    print('  que la comparaison se prend. Fermez le jeu ensuite.')
    print('  journal : %s' % journal)
    print()
    dbg.run(EXE, JEU, secondes, ())
    if not et['fait']:
        dbg.dire('\nAUCUNE comparaison prise : l etat 4 n a jamais dure deux '
                 'secondes. Soit le decor a fini par se charger, soit le mode '
                 'n a pas ete atteint.')
    fichier.close()
    print()
    print('Journal ecrit : %s' % journal)
    return 0


if __name__ == '__main__':
    sys.exit(main())
