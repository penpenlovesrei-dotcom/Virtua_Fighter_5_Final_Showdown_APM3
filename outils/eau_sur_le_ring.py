#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""L EAU PAR-DESSUS LE RING : releve le grand plan `eff_water` de `skb` pour
qu il couvre le disque du ring au lieu de passer dessous.

POURQUOI, et c est mesure

Chaque objet d un objset porte sa sphere englobante (centre, rayon) dans les
six premiers flottants de son en-tete. Pour `skb` :

    stgslk_water_ring   centre ( 0.000,  0.100,  0.000)   rayon   7.425
    stgslk_eff_water    centre (-22.500, 0.000,  5.000)   rayon 169.004

Le disque du ring est donc **dix centimetres au-dessus** du plan d eau : il le
cache, et c est tout. Rien d autre ne separe les deux.

Et le disque ne peut pas, lui, devenir de l eau : `TaskEffectWaterRing` est
INERTE dans le moteur APM3. Elle ecrit `[gestionnaire+0x330] = 1` et personne
ne lit ce champ -- verifie par un point d arret MATERIEL (DR0, 4 octets,
lecture ou ecriture) pose pendant 115 s de combat : UN SEUL acces, l ecriture
de la tache elle-meme.

Ce qui porte l animation de l eau, c est `eff_water` : son `.a3da` fait defiler
120 textures (`F_VF5S_SLK00_HR_BMP_000` a `_119`, identifiants 9085..9204) que
le moteur retrouve en reconstruisant le nom, `sprintf("%.*s%03d", n-3, nom,
image)`. Le monter au-dessus du disque, c est mettre l eau ANIMEE sur le ring.

CE QUE L OUTIL FAIT

Il ajoute une translation constante en Y a l objet, dans son `.a3da` :

    object.0.trans.y.type=0        ->   object.0.trans.y.type=1
                                        object.0.trans.y.value=<hauteur>

Il repart toujours de la sauvegarde, controle que la reconstruction de
l archive rend l original a l octet pres quand rien n a change, et RELIT
l archive produite.

    py -3 tools/eau_sur_le_ring.py --controle
    py -3 tools/eau_sur_le_ring.py --hauteur 0.2
    py -3 tools/eau_sur_le_ring.py --rendre
"""
import argparse
import os
import struct
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)

ARCHIVE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media',
                       'rom', 'auth_3d', 'EFFSTGSKB.farc')
SAUVE = ARCHIVE + '.avant_hauteur'
MEMBRE = 'STGSKB_EFF_WATER.a3da'
CLE = 'object.0.trans.y'


def lire_farc(chemin):
    """(alignement, [(nom, octets)]) d un FArc non comprime."""
    d = open(chemin, 'rb').read()
    if d[:4] != b'FArc':
        raise ValueError('%s : magie %r, FArc attendu' % (chemin, d[:4]))
    tete, alignement = struct.unpack_from('>2I', d, 4)
    fin = 8 + tete
    o, out = 12, []
    while o < fin:
        e = d.index(b'\0', o)
        nom = d[o:e].decode('ascii')
        o = e + 1
        off, taille = struct.unpack_from('>2I', d, o)
        o += 8
        if not nom:
            break
        out.append((nom, d[off:off + taille]))
    return alignement, out


def ecrire_farc(alignement, membres, dest):
    """Reconstruit un FArc non comprime : en-tete gros-boutiste, membres
    alignes, bourrage final jusqu a l alignement."""
    def cale(x):
        return (x + alignement - 1) // alignement * alignement

    # L en-tete lui-meme est CALE sur l alignement, et c est la taille CALEE
    # qui est ecrite en +0x04 : sans ca le tour complet perd onze octets.
    tete = sum(len(n.encode('ascii')) + 1 + 8 for n, _ in membres)
    debut = cale(12 + tete)

    pos = cale(debut)
    entetes, places = bytearray(), []
    for nom, brut in membres:
        places.append(pos)
        entetes += nom.encode('ascii') + b'\x00'
        entetes += struct.pack('>2I', pos, len(brut))
        pos = cale(pos + len(brut))
    sortie = bytearray(b'FArc') + struct.pack('>2I', debut - 8, alignement)
    sortie += entetes
    sortie += bytes(debut - len(sortie))
    if len(sortie) != debut:
        raise AssertionError('en-tete : %d au lieu de %d' % (len(sortie),
                                                             debut))
    corps = bytearray()
    for (nom, brut), p in zip(membres, places):
        corps += bytes(p - debut - len(corps))
        corps += brut
    corps += bytes(cale(debut + len(corps)) - debut - len(corps))
    with open(dest, 'wb') as fp:
        fp.write(bytes(sortie) + bytes(corps))


def jeu_tourne():
    s = subprocess.run(['tasklist'], capture_output=True, text=True).stdout
    return 'vfes.exe' in s


def lignes_trans(texte):
    return [l for l in texte.splitlines() if '.trans.' in l]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hauteur', type=float, default=0.2)
    ap.add_argument('--controle', action='store_true')
    ap.add_argument('--rendre', action='store_true')
    a = ap.parse_args()

    if a.rendre:
        if not os.path.exists(SAUVE):
            print('pas de sauvegarde : rien a rendre')
            return 1
        if jeu_tourne():
            print('REFUS : vfes.exe tourne')
            return 1
        if os.path.exists(ARCHIVE):
            os.remove(ARCHIVE)
        os.replace(SAUVE, ARCHIVE)
        print('archive d origine remise')
        return 0

    depart = SAUVE if os.path.exists(SAUVE) else ARCHIVE
    print('depart : %s' % os.path.basename(depart))
    origine = open(depart, 'rb').read()
    alignement, membres = lire_farc(depart)
    print('%d membre(s), alignement %d' % (len(membres), alignement))

    # LE TOUR COMPLET, avant toute modification
    tmp = ARCHIVE + '.essai'
    ecrire_farc(alignement, membres, tmp)
    tour = open(tmp, 'rb').read()
    os.remove(tmp)
    print('ALLER-RETOUR IDENTIQUE : %s' % (tour == origine))
    if tour != origine:
        print('REFUS : la reconstruction ne rend pas l archive d origine '
              '(%d octets contre %d)' % (len(tour), len(origine)))
        return 1

    noms = [n for n, _ in membres]
    if MEMBRE not in noms:
        print('REFUS : %s absent de l archive' % MEMBRE)
        return 1
    k = noms.index(MEMBRE)
    texte = membres[k][1].decode('latin-1')
    print('%s, avant :' % MEMBRE)
    for l in lignes_trans(texte):
        print('   %s' % l)
    vieux = '%s.type=0' % CLE
    if vieux not in texte:
        print('REFUS : %r introuvable (deja modifie ?)' % vieux)
        return 1
    fin = '\r\n' if '\r\n' in texte else '\n'
    neuf = ('%s.type=1%s%s.value=%g' % (CLE, fin, CLE, a.hauteur))
    texte2 = texte.replace(vieux, neuf, 1)

    if a.controle:
        print('apres (simulation) :')
        for l in lignes_trans(texte2):
            print('   %s' % l)
        print('CONTROLE SEUL : rien ecrit.')
        return 0
    if jeu_tourne():
        print('REFUS : vfes.exe tourne')
        return 1

    membres[k] = (MEMBRE, texte2.encode('latin-1'))
    cote = ARCHIVE + '.neuf'
    ecrire_farc(alignement, membres, cote)
    if not os.path.exists(SAUVE):
        os.replace(ARCHIVE, SAUVE)
        print('sauvegarde : %s' % os.path.basename(SAUVE))
    elif os.path.exists(ARCHIVE):
        os.remove(ARCHIVE)
    os.replace(cote, ARCHIVE)
    print('pose : %s (%d octets)' % (os.path.basename(ARCHIVE),
                                     os.path.getsize(ARCHIVE)))

    print()
    print('--- relu dans l archive PRODUITE ---')
    _, produits = lire_farc(ARCHIVE)
    d = dict(produits)
    if MEMBRE not in d:
        print('REFUS : %s absent de l archive produite' % MEMBRE)
        return 1
    t = d[MEMBRE].decode('latin-1')
    for l in lignes_trans(t):
        print('   %s' % l)
    if ('%s.value=%g' % (CLE, a.hauteur)) not in t:
        print('REFUS : la translation n est pas dans l archive produite')
        return 1
    print('   translation de %g m en Y, posee et relue.' % a.hauteur)
    return 0


if __name__ == '__main__':
    sys.exit(main())
