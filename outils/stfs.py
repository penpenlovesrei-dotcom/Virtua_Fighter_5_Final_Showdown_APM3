#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lecteur de conteneurs STFS (Xbox 360 : LIVE / CON / PIRS).

Ecrit a partir de la specification -- pas d'outil tiers execute. Sources :
la page STFS de Free60, et le gabarit `Xbox360Container.bt` du depot
emoose/xbox-reversing (qui fournit un verificateur, `stfschk`, mais pas
d'extracteur).

Pourquoi on en a besoin : le menu console de VF5 vit dans une famille de
fichiers `aet_n_*` / `spr_n_*` **absente du dump APM3** et presente dans le
paquet Xbox 360. Le moteur APM3 les connait encore (`spr_n_` apparait 11 fois
dans son binaire), donc seules les donnees manquent.

Disposition, telle qu'on l'utilise ici :

    0x0000  magic : "LIVE", "CON ", "PIRS"
    0x0340  taille d'en-tete (u32 gros-boutiste)
    0x0379  descripteur de volume :
              +0x00  longueur du descripteur (0x24)
              +0x01  separation de blocs
              +0x02  nombre de blocs de la table de fichiers (u16 petit-bout.)
              +0x04  bloc de depart de la table de fichiers (u24 petit-bout.)
    0xC000  premier bloc de donnees, blocs de 0x1000 octets

Une entree de table fait 0x40 octets :

    0x00  nom, 0x28 octets                 0x28  drapeaux + longueur du nom
    0x29  blocs alloues (u24 petit-bout.)  0x2F  bloc de depart (u24)
    0x32  parent (u16)                     0x34  taille (u32 gros-boutiste)

**Le piege du format** : des tables de hachage sont intercalees dans le fichier
tous les 0xAA blocs, et une de plus tous les 0xAA*0xAA. Elles occupent de la
place reelle mais **ne comptent pas** dans la numerotation logique. Sans en
tenir compte, on lit des octets de hachage au milieu des donnees.

Usage :
    py -3 tools/stfs.py lister <paquet>
    py -3 tools/stfs.py lister <paquet> --motif aet_n_
    py -3 tools/stfs.py extraire <paquet> <dossier> --motif aet_n_,spr_n_
"""
import os
import re
import struct
import sys

TAILLE_BLOC = 0x1000
DEBUT = 0xC000


def u24(d, o):
    return d[o] | (d[o + 1] << 8) | (d[o + 2] << 16)


class Stfs:
    def __init__(self, chemin):
        self.fp = open(chemin, 'rb')
        self.chemin = chemin
        tete = self._lire(0, 0x400)
        self.magic = tete[:4]
        if self.magic not in (b'LIVE', b'CON ', b'PIRS'):
            raise ValueError('pas un conteneur STFS : %r' % self.magic)
        self.taille_entete = struct.unpack_from('>I', tete, 0x340)[0]
        vd = 0x379
        self.desc_len = tete[vd]
        self.separation = tete[vd + 1]
        self.tf_blocs = struct.unpack_from('<H', tete, vd + 2)[0]
        self.tf_debut = u24(tete, vd + 4)
        # Le decalage des tables depend de la taille d'en-tete. Regle usuelle :
        # 0 quand l'en-tete tient dans la forme courte, 1 sinon.
        self.shift = 0 if ((self.taille_entete + 0xFFF) & 0xF000) >> 0xC == 0xB else 1
        if self.separation & 1:
            self.shift = 1

    def _lire(self, off, n):
        self.fp.seek(off)
        return self.fp.read(n)

    def bloc_reel(self, bloc):
        """Numero logique -> numero reel, en sautant les tables de hachage."""
        n = bloc
        if bloc >= 0xAA:
            n += ((bloc // 0xAA) + 1) << self.shift
        if bloc >= 0x70E4:
            n += ((bloc // 0x70E4) + 1) << self.shift
        return n

    def octets_bloc(self, bloc):
        return self._lire(DEBUT + self.bloc_reel(bloc) * TAILLE_BLOC, TAILLE_BLOC)

    def table(self):
        """Les entrees de la table de fichiers."""
        brut = b''.join(self.octets_bloc(self.tf_debut + i)
                        for i in range(self.tf_blocs))
        out = []
        for i in range(0, len(brut), 0x40):
            e = brut[i:i + 0x40]
            if len(e) < 0x40 or e[0] == 0:
                continue
            drap = e[0x28]
            n = drap & 0x3F
            nom = e[:n].decode('latin-1', 'replace')
            if not nom or not re.match(r'^[\x20-\x7e]+$', nom):
                continue
            out.append({
                'nom': nom,
                'dossier': bool(drap & 0x80),
                'consecutif': bool(drap & 0x40),
                'blocs': u24(e, 0x29),
                'debut': u24(e, 0x2F),
                'parent': struct.unpack_from('<h', e, 0x32)[0],
                'taille': struct.unpack_from('>I', e, 0x34)[0],
                'index': len(out),
            })
        return out

    def contenu(self, e):
        """Le contenu d'un fichier, en suivant ses blocs."""
        reste = e['taille']
        bloc = e['debut']
        morceaux = []
        for _ in range(e['blocs']):
            if reste <= 0:
                break
            d = self.octets_bloc(bloc)
            morceaux.append(d[:min(TAILLE_BLOC, reste)])
            reste -= TAILLE_BLOC
            bloc += 1          # blocs consecutifs
        return b''.join(morceaux)


def main():
    argv = sys.argv[1:]
    if len(argv) < 2:
        print(__doc__)
        return 1
    action, paquet = argv[0], argv[1]
    motifs = []
    if '--motif' in argv:
        motifs = [x.strip().lower() for x in argv[argv.index('--motif') + 1].split(',')]

    s = Stfs(paquet)
    print('%s   en-tete 0x%X   table de fichiers : bloc %d, %d bloc(s)   shift %d'
          % (s.magic.decode(), s.taille_entete, s.tf_debut, s.tf_blocs, s.shift))
    ent = s.table()
    print('%d entree(s) dans la table' % len(ent))
    if motifs:
        ent = [e for e in ent if any(m in e['nom'].lower() for m in motifs)]
        print('%d apres filtrage sur %s' % (len(ent), motifs))

    if action == 'lister':
        for e in ent[:200]:
            print('  %-34s %9d o   bloc %6d  x%-4d %s'
                  % (e['nom'], e['taille'], e['debut'], e['blocs'],
                     'dossier' if e['dossier'] else
                     ('consecutif' if e['consecutif'] else 'chaine')))
        return 0

    if action == 'extraire':
        dest = argv[2]
        os.makedirs(dest, exist_ok=True)
        n = 0
        for e in ent:
            if e['dossier']:
                continue
            d = s.contenu(e)
            p = os.path.join(dest, e['nom'])
            with open(p, 'wb') as fp:
                fp.write(d)
            etat = 'ok' if len(d) == e['taille'] else 'TAILLE %d != %d' % (len(d), e['taille'])
            print('  %-34s %9d o   %s' % (e['nom'], len(d), etat))
            n += 1
        print('%d fichier(s) ecrit(s) dans %s' % (n, dest))
        return 0

    print('action inconnue : %s' % action)
    return 1


if __name__ == '__main__':
    sys.exit(main())
