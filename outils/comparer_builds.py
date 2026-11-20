#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Compare deux builds du moteur PXD par leurs STRUCTURES, pas leurs adresses.

Deux builds n'ont pas la meme disposition : comparer des adresses n'a aucun
sens. On compare donc ce qui est invariant --

  . la TABLE DES DECORS : on la retrouve dans chaque binaire en cherchant un
    tableau de pas 0xF0 dont le premier champ pointe sur « STGTST » ;
  . les DESCRIPTEURS eux-memes, champ par champ, decor par decor ;
  . la table des CODES d'eclairage (41 chaines de trois lettres) ;
  . la presence de chaines-temoins.

    py -3 tools/comparer_builds.py <a.dll> <b.dll>
"""
import os
import struct
import sys

import pefile

CODES = ['tst', 'ts2', 'ts3', 'wht', 'ban', 'ter', 'nyc', 'cas', 'riv', 'jin',
         'sin', 'djo', 'umi', 'hai', 'are', 'slk', 'yuk', 'tak', 'aur', 'bar',
         'tan', 'du1', 'du2', 'du3', 'du4', 'du5', 'trm', 'cid', 'trs',
         'evo00', 'evo01', 'evo02', 'evo03', 'evo04', 'evo05', 'evo06',
         'evo07', 'evo08', 'evo09', 'gym', 'smo']
PAS = 0xF0


class Image(object):
    def __init__(self, chemin):
        self.chemin = chemin
        self.pe = pefile.PE(chemin, fast_load=True)
        self.base = self.pe.OPTIONAL_HEADER.ImageBase
        self.brut = bytes(self.pe.__data__)
        self.plages = [(self.base + s.VirtualAddress,
                        self.base + s.VirtualAddress + s.Misc_VirtualSize,
                        s.PointerToRawData) for s in self.pe.sections]

    def off(self, va):
        for deb, fin, raw in self.plages:
            if deb <= va < fin:
                return raw + (va - deb)
        return None

    def lire(self, va, n):
        o = self.off(va)
        return self.brut[o:o + n] if o is not None else b''

    def chaine(self, va, maxi=120):
        o = self.off(va)
        if o is None:
            return None
        f = self.brut.find(b'\x00', o)
        if f < 0 or f - o > maxi:
            return None
        try:
            return self.brut[o:f].decode('ascii')
        except UnicodeDecodeError:
            return None

    def contient(self, texte):
        """Le motif apparait-il quelque part ? SOUS-CHAINE, pas mot entier.

        `am::abaas` prefixe des noms plus longs et `STGDUR` vit dans
        `rom/auth_3d/STGDUR.farc` : exiger un NUL juste apres faisait repondre
        « NON » sur des chaines pourtant presentes.
        """
        return self.brut.find(texte.encode()) >= 0

    def va_de_chaine(self, texte):
        """Toutes les VA ou `texte\\0` apparait."""
        cible = texte.encode() + b'\x00'
        out, i = [], self.brut.find(cible)
        while i >= 0:
            for deb, fin, raw in self.plages:
                if raw <= i < raw + (fin - deb):
                    out.append(deb + (i - raw))
                    break
            i = self.brut.find(cible, i + 1)
        return out

    def table_decors(self):
        """Rend (adresse, PAS) de la table des 41 descripteurs.

        Le pas SE DEDUIT : il vaut 0xF0 sur APM3 et **0xD8 sur le build
        Yakuza 6** -- l'enregistrement APM3 est 24 octets plus long. Le figer
        aurait fait conclure « table introuvable ».
        """
        for va_tst in self.va_de_chaine('STGTST'):
            aiguille = struct.pack('<Q', va_tst)
            i = self.brut.find(aiguille)
            while i >= 0:
                for deb, fin, raw in self.plages:
                    if raw <= i < raw + (fin - deb):
                        va = deb + (i - raw)
                        for pas in range(0x80, 0x200, 8):
                            q = self.lire(va + pas, 8)
                            if len(q) == 8 and self.chaine(
                                    struct.unpack('<Q', q)[0]) == 'STGTS2':
                                # confirme sur une troisieme entree
                                q2 = self.lire(va + 11 * pas, 8)
                                if self.chaine(
                                        struct.unpack('<Q', q2)[0]) == 'STGDJO':
                                    return va, pas
                i = self.brut.find(aiguille, i + 1)
        return None, None

    def table_eclairage(self):
        """Le tableau de 41 pointeurs sur « tst », « ts2 », ..."""
        for va_tst in self.va_de_chaine('tst'):
            aiguille = struct.pack('<Q', va_tst)
            i = self.brut.find(aiguille)
            while i >= 0:
                for deb, fin, raw in self.plages:
                    if raw <= i < raw + (fin - deb):
                        va = deb + (i - raw)
                        p = struct.unpack_from('<Q', self.lire(va + 8, 8))[0]
                        if self.chaine(p) == 'ts2':
                            return va
                i = self.brut.find(aiguille, i + 1)
        return None


TEMOINS = [
    ('am::abaas', 'le netcode de bornes liees'),
    ('APM3_ENTRY', 'l ecran noir de la borne'),
    ('vfes_bgm_cus', 'la musique de l ecran Customize'),
    ('EXIT_CAUTION', 'la confirmation de EXIT GAME'),
    ('TERMINAL MENU', 'la page TERMINAL'),
    ('NOW LOADING', 'le texte de chargement'),
    ('rom/game_score.txt', 'le decor maison de l adversaire'),
    ('obj_db.bin', 'la base des jeux d objets'),
    ('STGDUR', 'le decor perdu de Dural'),
    ('%s/envmap_correct_%s.txt', 'la correction d environnement'),
]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    a, b = Image(sys.argv[1]), Image(sys.argv[2])
    na, nb = (os.path.basename(x.chemin)[:34] for x in (a, b))

    print('=' * 78)
    print('%-38s %s' % (na, nb))
    print('=' * 78)

    ta, pa = a.table_decors()
    tb, pb = b.table_decors()
    print('\ntable des decors      0x%-30X 0x%X' % (ta or 0, tb or 0))
    print('   pas d une entree   %-32s %s'
          % ('0x%X' % pa if pa else '?', '0x%X' % pb if pb else '?'))
    if pa and pb and pa != pb:
        print('   -> %d pointeur(s) de plus du cote le plus long : le bloc BGM'
              % (abs(pa - pb) // 8))
    ea, eb = a.table_eclairage(), b.table_eclairage()
    print('table d eclairage     0x%-30X 0x%X' % (ea or 0, eb or 0))

    print('\n--- CHAINES TEMOINS ---')
    for texte, quoi in TEMOINS:
        print('   %-26s %-9s %-9s  %s'
              % (texte,
                 'oui' if a.contient(texte) else 'NON',
                 'oui' if b.contient(texte) else 'NON', quoi))

    if not (ta and tb):
        return 0
    # Les champs APRES le bloc BGM sont decales du differentiel de pas.
    decalage = pa - pb

    print('\n--- LES 41 DESCRIPTEURS, CHAMP PAR CHAMP ---')
    # (offset chez A, format, nom, decale-t-il apres le bloc BGM ?)
    champs = [(0x10, 'I', 'objset', 0), (0x14, 'I', 'obj0', 0),
              (0x18, 'I', 'obj1', 0), (0x1C, 'I', 'obj2', 0),
              (0x20, 'I', 'obj3', 0), (0x24, 'I', 'obj4', 0),
              (0x2C, 'I', 'x2C', 0), (0xB8, 'I', 'murs', 1),
              (0xD0, 'I', 'xD0', 1), (0xD4, 'I', 'xD4', 1),
              (0xE4, 'f', 'aireX', 1), (0xE8, 'f', 'aireY', 1)]
    ecarts = 0
    for i, code in enumerate(CODES):
        da = a.lire(ta + i * pa, pa)
        db = b.lire(tb + i * pb, pb)
        diff = []
        for off, fmt, nom, apres in champs:
            va = struct.unpack_from('<' + fmt, da, off)[0]
            vb = struct.unpack_from('<' + fmt, db, off - apres * decalage)[0]
            if va != vb:
                diff.append('%s %s/%s' % (nom, va, vb))
        for off, nom in ((0x00, 'code'), (0x08, 'eff'), (0x48, 'coli')):
            sa = a.chaine(struct.unpack_from('<Q', da, off)[0])
            sb = b.chaine(struct.unpack_from('<Q', db, off)[0])
            if sa != sb:
                diff.append('%s %r/%r' % (nom, sa, sb))
        if diff:
            ecarts += 1
            print('   %2d %-6s %s' % (i, code, ' | '.join(diff)))
    print('   -> %d descripteur(s) different(s) sur %d' % (ecarts, len(CODES)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
