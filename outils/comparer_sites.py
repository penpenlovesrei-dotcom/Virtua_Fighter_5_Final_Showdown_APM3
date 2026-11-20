#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NOS SITES DE CORRECTIF, CHERCHES DANS UN AUTRE BUILD.

POURQUOI (2026-10-11). Frederic : « cette version est-elle facilement patchable
avec tout ce qui a ete fait pour la version APM3 ? » La question ne se repond
pas par une opinion : `patch_moteur.py` porte des dizaines de sites, chacun
sous la forme (adresse, octets ATTENDUS), et le patcheur REFUSE deja quand les
octets ne sont pas ceux-la. Il suffit donc de poser la meme question a l autre
binaire.

CE QUE L OUTIL FAIT, et rien de plus :

  1. il recolte dans `patch_moteur` tous les couples (adresse, octets attendus)
     -- les listes de correctifs y ont toutes la meme forme ;
  2. il verifie d abord que chaque couple est VRAI dans notre `.origine` (un
     couple qui ne l est pas serait un defaut de la recolte, pas du build
     d en face) ;
  3. il regarde ce que l autre binaire porte A LA MEME ADRESSE ;
  4. et, pour les couples absents, il cherche la SEQUENCE ailleurs dans le
     `.text` de l autre build -- un site deplace n est pas un site perdu.

    py -3 tools/comparer_sites.py <autre.dll>
    py -3 tools/comparer_sites.py <autre.dll> --detail
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

BASE = 0x180000000
MINI = 6          # en deca, une sequence se retrouve partout par hasard


def recolter(mod):
    """Tous les couples (adresse, octets attendus) du patcheur.

    Les correctifs y sont ecrits de trois facons, toutes reconnaissables :
        (nom, va, tete, neuf)      les listes de points
        (va, tete, neuf)           idem, sans le nom de fichier
        (va, tete)                 les sites a relais
    On ne retient que ce qui a la FORME : un entier dans la plage de l image
    suivi d octets. Aucune liste n est citee par son nom -- ajouter un
    correctif ne demande donc pas de toucher a cet outil.
    """
    vus = {}

    def essayer(t):
        for i, x in enumerate(t):
            if (isinstance(x, int) and not isinstance(x, bool)
                    and BASE < x < BASE + 0x1000000
                    and i + 1 < len(t) and isinstance(t[i + 1], bytes)
                    and t[i + 1]):
                vus.setdefault(x, t[i + 1])
                return

    def parcourir(v, profondeur=0):
        if profondeur > 3:
            return
        if isinstance(v, tuple):
            essayer(v)
        if isinstance(v, (list, tuple)):
            for x in v:
                if isinstance(x, (list, tuple)):
                    parcourir(x, profondeur + 1)

    for nom in dir(mod):
        if nom.startswith('_'):
            continue
        parcourir(getattr(mod, nom))
    return vus


def lire(chemin):
    import pefile
    p = pefile.PE(chemin, fast_load=True)
    t = [s for s in p.sections if s.Name.rstrip(b'\x00') == b'.text'][0]
    return p, BASE + t.VirtualAddress, p.get_data(t.VirtualAddress,
                                                 t.Misc_VirtualSize)


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    autre = argv[0]
    detail = '--detail' in argv
    if not os.path.exists(autre):
        print('introuvable : %s' % autre)
        return 1
    import patch_moteur as pm

    sites = recolter(pm)
    nous = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                        pm.DLL + '.origine')
    pa, _da, _ta = lire(nous)
    pb, deb_b, text_b = lire(autre)

    def octets(p, va, n):
        try:
            return p.get_data(va - BASE, n)
        except Exception:                                   # noqa: BLE001
            return None

    # 1. LE CONTROLE DE LA RECOLTE. Un couple faux chez nous ne dirait rien
    #    de l autre build -- il dirait que l outil a mal lu.
    bons, faux = {}, []
    for va, tete in sites.items():
        if octets(pa, va, len(tete)) == tete:
            bons[va] = tete
        else:
            faux.append(va)
    print('%d couple(s) (adresse, octets) recoltes dans patch_moteur.py'
          % len(sites))
    print('   %d verifies dans notre .origine, %d ecartes (recolte '
          'incertaine)' % (len(bons), len(faux)))
    print()

    # 2. LA MEME ADRESSE DANS L AUTRE BUILD.
    pareil, autres, hors = [], [], []
    for va, tete in sorted(bons.items()):
        d = octets(pb, va, len(tete))
        if d is None:
            hors.append(va)
        elif d == tete:
            pareil.append(va)
        else:
            autres.append((va, tete, d))
    print('A LA MEME ADRESSE dans %s :' % os.path.basename(autre))
    print('   %4d site(s) portent les MEMES octets' % len(pareil))
    print('   %4d site(s) portent autre chose' % len(autres))
    print('   %4d site(s) sont hors de l image' % len(hors))
    print()

    # 3. LA SEQUENCE AILLEURS. Un site deplace n est pas un site perdu : si
    #    la suite d octets est unique dans le `.text` d en face, le correctif
    #    se reporte a l adresse trouvee.
    deplaces = unique = ambigus = absents = 0
    lignes = []
    for va, tete, _d in autres:
        if len(tete) < MINI:
            ambigus += 1
            lignes.append((va, 'trop court pour etre cherche (%d o)'
                           % len(tete)))
            continue
        n, i, p0 = 0, text_b.find(tete), -1
        while i >= 0 and n < 3:
            n += 1
            p0 = i if n == 1 else p0
            i = text_b.find(tete, i + 1)
        if n == 0:
            absents += 1
            lignes.append((va, 'ABSENT du .text'))
        elif n == 1:
            unique += 1
            deplaces += 1
            lignes.append((va, 'retrouve UNE fois en 0x%X (ecart %+d)'
                           % (deb_b + p0, deb_b + p0 - va)))
        else:
            ambigus += 1
            lignes.append((va, 'retrouve %d fois ou plus' % n))
    print('LES SITES QUI NE SONT PLUS A LA MEME ADRESSE (%d) :' % len(autres))
    print('   %4d retrouves UNE seule fois ailleurs (reportables)' % unique)
    print('   %4d retrouves plusieurs fois, ou trop courts (a la main)'
          % ambigus)
    print('   %4d absents du .text' % absents)
    if detail:
        print()
        for va, quoi in lignes:
            print('   0x%X  %s' % (va, quoi))
    print()
    total = len(bons)
    print('VERDICT : %d / %d sites (%.1f %%) s appliqueraient TELS QUELS.'
          % (len(pareil), total, 100.0 * len(pareil) / max(1, total)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
