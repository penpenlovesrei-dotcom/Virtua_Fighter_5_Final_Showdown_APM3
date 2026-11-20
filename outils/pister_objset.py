#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Le moteur CONNAIT-IL notre objset ? On lit sa table, dans le processus vivant.

POURQUOI CETTE MESURE

Journal du 2026-09-10 (`analysis/pister_import_d5r.txt`) : le decor ajoute passe
l'etat 3 et **reste bloque a l'etat 4**, et surtout `stgd5r.farc` **n'est JAMAIS
ouvert** -- alors que les neuf autres pieces le sont, et qu'en remplacement
`stgdjo.farc` s'ouvrait des l'etat 2. La geometrie n'est donc pas refusee : elle
n'est pas demandee.

L'etat 4 appelle `0x1800F8A40(objset_id)`, qui appelle `0x1800F9450(id)` -- et
`0x1800F9450` est un **lower_bound** :

    0x1800F9481  mov rax, [0x18070FA90]     le vecteur
    0x1800F9488  mov r9,  [rax + 8]         fin
    0x1800F948C  mov r8,  [rax]             debut
    0x1800F9498  sar rcx, 9                 (fin - debut) / 0x200  -> le nombre
    0x1800F94AE  cmp dword ptr [rax + r8], edi   la CLE est le dword de tete

Donc : un vecteur d'enregistrements de **0x200 octets**, cle en `+0x00`,
**recherche dichotomique**. Une dichotomie ne trouve que dans une table TRIEE --
et la table `jeux` d'`obj_db.bin` n'est PAS triee par identifiant dans le
fichier (mesure : les identifiants ne sont pas monotones). Le moteur trie donc
quelque part, ou bien il ne trouve pas.

Cette sonde ne demande aucune navigation : le vecteur est bati au demarrage. On
lance le jeu, on attend, on lit le vecteur, et on dit :

  . combien d'entrees, et si les cles sont TRIEES ;
  . si notre identifiant y est, et a quel rang ;
  . ses voisins immediats ;
  . ce qu'une dichotomie y trouverait pour notre cle -- exactement le calcul de
    `0x1800F9450`, refait ici, parce que « la cle est presente » et « la
    dichotomie la trouve » sont deux choses differentes.

    py -3 tools/pister_objset.py
    py -3 tools/pister_objset.py --objset 6150 --secondes 40
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
SCENARIO = """# ecrit par tools/pister_objset.py -- aucune entree, on ne navigue pas.
front   = 10
journal = 0
clavier = 1
manette = 1
0       rien
"""

VECTEUR_RVA = 0x70FA90         # 0x18070FA90 : {debut, fin} du vecteur
PAS = 0x200                    # taille d'un enregistrement (sar rcx, 9)


def dichotomie(lire_cle, n, cible):
    """Le lower_bound de `0x1800F9450`, refait a l'identique."""
    lo, reste = 0, n
    while reste > 0:
        demi = reste >> 1
        milieu = lo + demi
        if lire_cle(milieu) < cible:
            lo = milieu + 1
            reste = reste - demi - 1
        else:
            reste = demi
    return lo


def main():
    argv = sys.argv[1:]
    objset = 6150
    if '--objset' in argv:
        objset = int(argv[argv.index('--objset') + 1], 0)
    secondes = 40
    if '--secondes' in argv:
        secondes = int(argv[argv.index('--secondes') + 1])

    journal = os.path.join(RACINE, 'analysis', 'pister_objset.txt')
    fichier = open(journal, 'w', encoding='utf-8')
    dbg = instrument.Debugger()
    dbg.quiet = True
    dbg.muet = '--son' not in argv
    dbg.sortie = fichier
    et = {'fait': False}

    def tic(d, t):
        if et['fait'] or t < secondes - 8:
            return
        b = d.base_de(MOTEUR)
        if not b:
            return
        # `0x18070FA90` tient un POINTEUR vers l'objet ; c'est cet objet qui
        # porte {debut, fin}. Les lire directement a 0x18070FA90 rendait un
        # vecteur de 94098 entrees et des cles absurdes -- une deuxieme
        # indirection oubliee ne se signale pas, elle rend des octets.
        objet = d.u64(b + VECTEUR_RVA)
        if not objet:
            return
        tete = d.read(objet, 16)
        if not tete or len(tete) != 16:
            return
        debut, fin = struct.unpack('<QQ', tete)
        if not debut or fin <= debut:
            d.dire('  le vecteur est vide (debut 0x%X, fin 0x%X)' % (debut, fin))
            return
        et['fait'] = True
        n = (fin - debut) // PAS
        d.dire('  vecteur d objsets : 0x%X..0x%X, %d entrees de 0x%X octets'
               % (debut, fin, n, PAS))
        cles = []
        for k in range(n):
            v = d.u32(debut + k * PAS)
            cles.append(-1 if v is None else v)
        tries = all(cles[i] <= cles[i + 1] for i in range(len(cles) - 1))
        d.dire('  cles TRIEES : %s   (min %d, max %d)'
               % (tries, min(cles), max(cles)))
        if not tries:
            fautes = [i for i in range(len(cles) - 1) if cles[i] > cles[i + 1]]
            d.dire('  %d rupture(s) d ordre, la premiere au rang %d : %d > %d'
                   % (len(fautes), fautes[0], cles[fautes[0]],
                      cles[fautes[0] + 1]))
        if objset in cles:
            r = cles.index(objset)
            d.dire('  notre objset %d est PRESENT au rang %d' % (objset, r))
            d.dire('  voisins : %s' % cles[max(0, r - 3):r + 4])
        else:
            d.dire('  notre objset %d est ABSENT du vecteur' % objset)
            proches = sorted(cles)[-6:]
            d.dire('  les six plus grandes cles : %s' % proches)
        # QU'EST-CE QUE CE VECTEUR, au fait ? 6044 entrees de 0x200 octets et
        # une cle en tete ne suffisent pas a l'affirmer. On lit les chaines
        # d'un enregistrement connu : si on y trouve « STGDJO », c'est bien la
        # liste des jeux d'objets d'`obj_db.bin`.
        for cle_temoin in (28, cles[0]):
            if cle_temoin not in cles:
                continue
            r0 = cles.index(cle_temoin)
            brut = d.read(debut + r0 * PAS, PAS) or b''
            mots, courant = [], b''
            for o in brut:
                if 32 <= o < 127:
                    courant += bytes([o])
                else:
                    if len(courant) >= 4:
                        mots.append(courant.decode('ascii'))
                    courant = b''
            d.dire('  enregistrement de la cle %d (rang %d) : %s'
                   % (cle_temoin, r0, ' | '.join(mots[:8]) or '(aucune chaine)'))
        gest = d.u64(b + VECTEUR_RVA - 8)
        if gest:
            d.dire('  gestionnaire 0x%X : +0x90 (deja charge) = %s, +0x98 = 0x%X'
                   % (gest, (d.read(gest + 0x90, 1) or b'?')[:1].hex(),
                      d.u64(gest + 0x98) or 0))
        r = dichotomie(lambda i: cles[i], n, objset)
        trouve = r < n and cles[r] == objset
        d.dire('  la DICHOTOMIE du moteur tombe au rang %d (cle %s) -> %s'
               % (r, cles[r] if r < n else 'hors table',
                  'TROUVE' if trouve else 'RATE'))
        d.dire('  (present dans la table et trouvable par dichotomie sont deux '
               'choses differentes : c est le second qui compte)')

    dbg.tic = tic
    with open(SCENARIO_ACTIF, 'w', encoding='ascii', newline='\n') as fp:
        fp.write(SCENARIO)
    print('MESURE : le moteur connait-il l objset %d ?' % objset)
    print('  Aucune navigation : laissez le jeu tourner %d s, il se ferme seul.'
          % secondes)
    print('  journal : %s' % journal)
    dbg.run(EXE, JEU, secondes, ())
    if not et['fait']:
        dbg.dire('\nLe vecteur n a pas pu etre lu. Il est peut-etre bati plus '
                 'tard : relancer avec --secondes 90.')
    fichier.close()
    print()
    print('Journal ecrit : %s' % journal)
    return 0


if __name__ == '__main__':
    sys.exit(main())
