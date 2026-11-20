#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Decompresseur LZX -- la variante Microsoft des XEX Xbox 360 et des WIM.

POURQUOI (2026-10-01). L'executable de VF5 FS sur Xbox 360
(`extracted/X360_FS/sel/default.xex`) est en compression 2, dite « normale »,
c'est-a-dire LZX. `tools/xex.py` savait deja ouvrir la compression 1
(« basique », celle de VF5 2007) et refusait celle-ci -- c'est ce refus qui
avait arrete la piste console le 2026-09-11. Ce fichier leve le refus.

Ecrit a partir de la specification, sans executer d'outil tiers : la
description du format LZX de Microsoft (document [MS-PATCH], section 2.2) et
la lecture du decodeur de Xenia pour les deux details que la specification
laisse implicites -- la fenetre n'est PAS reinitialisee entre les blocs d'un
XEX, et les trois derniers ecarts (R0, R1, R2) survivent d'un bloc a l'autre.

CE QU'IL FAUT SAVOIR DU FORMAT, et qui se trompe facilement :

  . LE FLOT DE BITS EST EN MOTS DE 16 BITS PETIT-BOUTISTES, et dans chaque
    mot les bits se lisent du POIDS FORT au poids faible. Ce melange est la
    premiere source d'erreur ; un flot lu octet par octet ne donne rien.

  . Trois sortes de blocs : 1 = verbatim, 2 = ecarts alignes, 3 = non
    compresse. Chacun porte sa taille sur 24 bits.

  . Les longueurs de code des arbres sont elles-memes compressees, par un
    PRE-ARBRE de vingt elements lus sur quatre bits. Les symboles 17, 18 et
    19 de ce pre-arbre sont des repetitions, et le 19 relit un code du
    pre-arbre pour la valeur -- oublier ce second tour decale tout l'arbre.

  . Les longueurs sont DELTA : `(precedente - valeur + 17) % 17`.

  . L'arbre principal a `256 + 8 * nombre_de_creneaux` elements, et il se lit
    EN DEUX MOITIES (les 256 litteraux d'abord), chacune avec son pre-arbre.

  . Les creneaux 0, 1 et 2 ne sont pas des ecarts mais R0, R1, R2 -- les
    trois derniers ecarts utilises.

  . Un bloc non compresse s'aligne sur 16 bits, puis donne R0, R1, R2 en
    quatre octets petit-boutistes chacun, puis les octets bruts.

  . La traduction « E8 » (les appels x86 absolus) est annoncee par un bit en
    tete de flot. Les XEX de Xbox 360 sont du PowerPC et ne s'en servent pas,
    mais on la lit quand meme pour ne pas decaler le flot.

Usage :
    py -3 tools/lzx.py --essai        verifie le decodeur sur un cas construit
"""
import struct
import sys

# Les tailles de fenetre vont de 2^15 a 2^25 ; a chacune son nombre de
# creneaux de position. La table est dans la specification ; on la garde
# telle quelle plutot que de la recalculer, pour pouvoir la relire.
CRENEAUX_PAR_FENETRE = {
    15: 30, 16: 32, 17: 34, 18: 36, 19: 38, 20: 42,
    21: 50, 22: 66, 23: 98, 24: 162, 25: 290,
}

PRETREE_N = 20
ARBRE_LONGUEUR_N = 249
ARBRE_ALIGNE_N = 8
LONGUEUR_MIN = 2

# Bits supplementaires et base de chaque creneau de position. Les trois
# premiers creneaux sont R0/R1/R2 et n'ont pas d'ecart propre.
BITS_SUP = [0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7,
            8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14,
            15, 15, 16, 16, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
            17, 17, 17, 17]
while len(BITS_SUP) < 290:
    BITS_SUP.append(17)

BASE_CRENEAU = [0]
for _i in range(1, 290):
    BASE_CRENEAU.append(BASE_CRENEAU[_i - 1] + (1 << BITS_SUP[_i - 1]))


class Refus(Exception):
    pass


class Bits:
    """Lecteur de bits sur des mots de 16 bits petit-boutistes.

    On ne charge QUE des mots entiers : c'est ce qui permet de savoir, a tout
    instant, de combien on est entre dans le mot courant (`reste % 16`) et
    donc de se realigner sans compter les bits depuis le debut.
    """

    __slots__ = ('d', 'pos', 'tampon', 'reste')

    def __init__(self, d):
        self.d = d
        self.pos = 0
        self.tampon = 0
        self.reste = 0

    def _charger(self, k):
        d, n = self.d, len(self.d)
        while self.reste < k:
            p = self.pos
            if p + 1 < n:
                m = d[p] | (d[p + 1] << 8)
            elif p < n:
                m = d[p]
            else:
                m = 0
            self.pos = p + 2
            self.tampon = (self.tampon << 16) | m
            self.reste += 16

    def lire(self, k):
        if not k:
            return 0
        if self.reste < k:
            self._charger(k)
        self.reste -= k
        v = (self.tampon >> self.reste) & ((1 << k) - 1)
        self.tampon &= (1 << self.reste) - 1
        return v

    def guetter(self, k):
        if self.reste < k:
            self._charger(k)
        return (self.tampon >> (self.reste - k)) & ((1 << k) - 1)

    def sauter(self, k):
        self.reste -= k
        self.tampon &= (1 << self.reste) - 1

    def aligner(self):
        """Jette les bits entames du mot courant."""
        r = self.reste % 16
        if r:
            self.sauter(r)

    def position_octet(self):
        """L'octet courant, le flot etant aligne sur 16 bits."""
        if self.reste % 16:
            raise Refus('position_octet sur un flot non aligne')
        return self.pos - (self.reste // 16) * 2

    def placer_octet(self, p):
        self.pos = p
        self.tampon = 0
        self.reste = 0


class Huffman:
    """Arbre canonique, decode par table : on guette `rapide` bits, et on ne
    descend bit a bit que pour les codes plus longs que cela."""

    __slots__ = ('longueurs', 'table', 'rapide', 'longs')

    def __init__(self, longueurs, rapide=10):
        self.longueurs = longueurs
        self.rapide = rapide
        self.table = [-1] * (1 << rapide)
        self.longs = {}
        code = 0
        maxlen = max(longueurs) if longueurs else 0
        for lg in range(1, maxlen + 1):
            for sym, l in enumerate(longueurs):
                if l != lg:
                    continue
                if lg <= rapide:
                    # on remplit toutes les entrees qui commencent par ce code
                    base = code << (rapide - lg)
                    for k in range(1 << (rapide - lg)):
                        self.table[base + k] = (sym << 5) | lg
                else:
                    self.longs[(lg, code)] = sym
                code += 1
            code <<= 1
        if maxlen and code > (1 << (maxlen + 1)):
            raise Refus('arbre de Huffman incoherent')

    def decoder(self, bits):
        v = self.table[bits.guetter(self.rapide)]
        if v >= 0:
            bits.sauter(v & 31)
            return v >> 5
        # Code long : on rallonge d'un bit a la fois. `guetter` relit depuis
        # le debut du code a chaque tour -- c'est plus simple que de
        # maintenir un accumulateur, et ces codes sont rares.
        lg = self.rapide
        while True:
            lg += 1
            if lg > 32:
                raise Refus('code de Huffman introuvable')
            code = bits.guetter(lg)
            s = self.longs.get((lg, code))
            if s is not None:
                bits.sauter(lg)
                return s


def _lire_pretree(bits):
    return Huffman([bits.lire(4) for _ in range(PRETREE_N)], rapide=6)


def _lire_longueurs(bits, longueurs, debut, fin):
    """Relit, en place, les longueurs de code de `debut` a `fin`.

    Les valeurs sont codees en DELTA par rapport aux longueurs precedentes :
    c'est ce qui permet a un bloc de ne reecrire qu'une partie de l'arbre.
    """
    pre = _lire_pretree(bits)
    i = debut
    while i < fin:
        s = pre.decoder(bits)
        if s == 17:                      # une serie de zeros, 4 bits + 4
            n = bits.lire(4) + 4
            for _ in range(n):
                if i >= fin:
                    break
                longueurs[i] = 0
                i += 1
        elif s == 18:                    # une longue serie de zeros, 5 + 20
            n = bits.lire(5) + 20
            for _ in range(n):
                if i >= fin:
                    break
                longueurs[i] = 0
                i += 1
        elif s == 19:                    # une repetition : 1 bit + 4, puis
            n = bits.lire(1) + 4         # UN CODE DU PRE-ARBRE pour la valeur
            s2 = pre.decoder(bits)
            v = (longueurs[i] - s2 + 17) % 17
            for _ in range(n):
                if i >= fin:
                    break
                longueurs[i] = v
                i += 1
        else:
            longueurs[i] = (longueurs[i] - s + 17) % 17
            i += 1


TRAME = 32768


def decompresser(src, taille_sortie, bits_fenetre, journal=False):
    """Rend `taille_sortie` octets decompresses de `src`.

    `bits_fenetre` est le logarithme de la taille de fenetre (15 pour 32 Ko).

    LA TRAME DE 32768 OCTETS, et c'est elle qui m'a manque trois heures.
    LZX ne produit pas un flot continu : la sortie est decoupee en TRAMES de
    32768 octets, et A LA FIN DE CHAQUE TRAME le flot de bits se recale sur
    une frontiere de seize bits. Les blocs, eux, traversent les trames : les
    deux decoupages sont independants, et c'est pour cela qu'on ne peut pas
    se contenter d'une boucle par bloc.

    Comment je l'ai su, plutot que devine : dans un XEX, chaque MORCEAU de la
    chaine de blocs est exactement une trame. En notant, a chaque multiple de
    32768 octets de sortie, ou en etait le flot, les deux premieres frontieres
    tombaient pile sur les frontieres de morceau (0x292E, 0x55C0) et les
    suivantes derivaient de plus en plus. Un decalage qui grandit a chaque
    trame ne peut venir que d'un recalage oublie une fois par trame.
    """
    if bits_fenetre not in CRENEAUX_PAR_FENETRE:
        raise Refus('fenetre 2^%d hors specification' % bits_fenetre)
    creneaux = CRENEAUX_PAR_FENETRE[bits_fenetre]
    n_principal = 256 + 8 * creneaux

    bits = Bits(src)
    out = bytearray(taille_sortie)
    pos = 0

    # LA TRADUCTION E8. Un bit, puis une taille sur 32 bits si le bit est mis.
    # Le PowerPC ne s'en sert pas, mais le bit est la et il faut le lire.
    if bits.lire(1):
        bits.lire(16)
        bits.lire(16)

    lg_principal = [0] * n_principal
    lg_longueur = [0] * ARBRE_LONGUEUR_N
    arbre_principal = arbre_longueur = arbre_aligne = None
    r0, r1, r2 = 1, 1, 1
    type_bloc = 0
    restant = 0            # octets de sortie restant dans le bloc courant
    taille_bloc = 0
    n_bloc = 0

    while pos < taille_sortie:
        fin_trame = min(pos + TRAME, taille_sortie)

        while pos < fin_trame:
            if restant == 0:
                type_bloc = bits.lire(3)
                taille_bloc = ((bits.lire(8) << 16) | (bits.lire(8) << 8)
                               | bits.lire(8))
                if journal:
                    print('  bloc #%d  type=%d  taille=%d  sortie=%d/%d'
                          % (n_bloc, type_bloc, taille_bloc, pos,
                             taille_sortie))
                n_bloc += 1
                if taille_bloc == 0:
                    raise Refus('bloc de taille nulle')
                if type_bloc == 3:
                    bits.aligner()
                    p = bits.position_octet()
                    r0, r1, r2 = struct.unpack_from('<III', src, p)
                    bits.placer_octet(p + 12)
                elif type_bloc in (1, 2):
                    if type_bloc == 2:
                        arbre_aligne = Huffman(
                            [bits.lire(3) for _ in range(ARBRE_ALIGNE_N)],
                            rapide=3)
                    _lire_longueurs(bits, lg_principal, 0, 256)
                    _lire_longueurs(bits, lg_principal, 256, n_principal)
                    arbre_principal = Huffman(lg_principal)
                    _lire_longueurs(bits, lg_longueur, 0, ARBRE_LONGUEUR_N)
                    arbre_longueur = Huffman(lg_longueur)
                else:
                    raise Refus('type de bloc %d inconnu a la sortie %d'
                                % (type_bloc, pos))
                restant = taille_bloc

            n = min(restant, fin_trame - pos)
            restant -= n
            cible = pos + n

            if type_bloc == 3:
                p = bits.position_octet()
                out[pos:cible] = src[p:p + n]
                p += n
                if restant == 0 and taille_bloc & 1:
                    p += 1              # un bloc impair porte un octet de bourre
                bits.placer_octet(p)
                pos = cible
                continue

            while pos < cible:
                s = arbre_principal.decoder(bits)
                if s < 256:
                    out[pos] = s
                    pos += 1
                    continue
                s -= 256
                en_tete = s & 7
                creneau = s >> 3
                if en_tete == 7:
                    longueur = (arbre_longueur.decoder(bits) + 7
                                + LONGUEUR_MIN)
                else:
                    longueur = en_tete + LONGUEUR_MIN

                if creneau == 0:
                    ecart = r0
                elif creneau == 1:
                    ecart, r1 = r1, r0
                    r0 = ecart
                elif creneau == 2:
                    ecart, r2 = r2, r0
                    r0 = ecart
                else:
                    sup = BITS_SUP[creneau]
                    if type_bloc == 2 and sup >= 3:
                        pied = ((bits.lire(sup - 3) << 3)
                                + arbre_aligne.decoder(bits))
                    else:
                        pied = bits.lire(sup)
                    ecart = BASE_CRENEAU[creneau] + pied - 2
                    r2, r1, r0 = r1, r0, ecart

                if ecart <= 0 or ecart > pos:
                    raise Refus('ecart %d impossible a la position %d'
                                % (ecart, pos))
                arret = min(pos + longueur, taille_sortie)
                src_i = pos - ecart
                # copie octet par octet : les recouvrements sont LEGITIMES,
                # c'est ainsi que LZX exprime les repetitions.
                while pos < arret:
                    out[pos] = out[src_i]
                    pos += 1
                    src_i += 1

        # FIN DE TRAME : le flot se recale sur seize bits.
        bits.aligner()

    return bytes(out)


def _essai():
    """Un cas construit a la main : un bloc NON COMPRESSE, qui exerce
    l'alignement, la lecture de R0/R1/R2 et la reprise du flot."""
    charge = bytes(range(64))
    flot = bytearray()
    # bit E8 = 0, type = 3 (3 bits), taille = 64 (24 bits) -> 28 bits,
    # qu'on ecrit a la main dans des mots de 16 bits, poids fort d'abord.
    val, nb = 0, 0

    def pousser(v, k):
        nonlocal val, nb
        val = (val << k) | v
        nb += k
        while nb >= 16:
            nb -= 16
            m = (val >> nb) & 0xFFFF
            flot.extend(struct.pack('<H', m))
            val &= (1 << nb) - 1

    pousser(0, 1)          # pas de traduction E8
    pousser(3, 3)          # bloc non compresse
    pousser(0, 8)
    pousser(0, 8)
    pousser(64, 8)         # taille = 64
    if nb:                 # aligner sur 16 bits
        pousser(0, 16 - nb)
    flot.extend(struct.pack('<III', 1, 1, 1))     # R0, R1, R2
    flot.extend(charge)
    rendu = decompresser(bytes(flot), 64, 15)
    if rendu != charge:
        print('ESSAI RATE : %s' % rendu[:16].hex())
        return 1
    print('essai : bloc non compresse de 64 octets, aligne et relu -- OK')
    return 0


def main():
    if '--essai' in sys.argv:
        return _essai()
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
