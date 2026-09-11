#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""`tex_db.bin` : le nom de chaque texture, et son identifiant global.

La troisieme et derniere des bases que `ajouter_un_decor.md` §2 nommait. C'est
la plus simple des trois -- et la seule dont la table soit TRIEE, ce qui change
la facon d'y ajouter.

LA CARTE, mesuree le 2026-09-09

    0x00000   u32 nombre de textures   25 992
    0x00004   u32 offset de la table   0x9ABF0
    0x00008   deux u32 a zero
    0x00010   POT : les noms, termines par zero          633 296 o
    0x9ABF0   TABLE   25 992 x 8   {identifiant, offset du nom}
    0xCD830   fin du fichier, a l'octet pres

    [    0] id 0x0000  F_VF5C_DUMMY
    [    1] id 0x0001  F_VF5C_AKI01_FJ_DOUGI
    [25991] id 0x7E02  F_VF5C_VAN749_KAMI_T

CE QUI LA DISTINGUE DE `obj_db.bin`

  . **la table est triee par identifiant** -- verifie sur les 25 992 entrees.
    On n'ajoute donc PAS a la fin : on INSERE a sa place. `obj_db`, lui, n'est
    trie ni par jeu ni par objet, et s'ajoute a la fin ;
  . l'espace des identifiants est TROUE : 25 992 textures pour des
    identifiants allant jusqu'a 32 258. Il reste donc de la place partout, et
    `--libres` la montre ;
  . un seul pot de chaines, pas deux.

CE QU'UN DECOR IMPORTE N'Y CHANGE PAS

Le dojo a **271 textures**, `F_VF5E_DJO00_*`, identifiants 0x19C7 et suivants.
Une archive importee puis renommee garde ses noms ET ses identifiants de
texture internes : ils sont deja dans cette base sous leurs noms d'origine.
**Un decor importe n'a donc rien a ajouter ici.** Ce n'est qu'une texture
VRAIMENT neuve qui demande une entree.

C'est aussi la reponse a une question restee ouverte le 2026-09-08 : `tex_db`
n'etait pas le risque du plan d'ajout. L'emplacement `trs`, lui, ne porte que
DEUX textures (`F_VF5S_TRS00_MU_BLUE` et une autre) -- mais il n'en avait pas
besoin de plus, puisqu'il chargeait celles du dojo.

    py -3 tools/tex_db.py --essai
    py -3 tools/tex_db.py --montrer DJO00
    py -3 tools/tex_db.py --libres
    py -3 tools/tex_db.py --ajouter F_VF5E_XXX00_IK_MUR --id 32300 --sortie <f>
"""
import io
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
DEFAUT = os.path.join(RACINE, 'extracted', 'tex_db.bin')

POT = 0x10
PAS = 8


class Base:
    def __init__(self, brut):
        n, t = struct.unpack_from('<2I', brut, 0)
        self.reste = struct.unpack_from('<2I', brut, 8)
        if not POT < t <= len(brut) or t + n * PAS != len(brut):
            raise ValueError('en-tete incoherent : %d entrees a 0x%X pour %d '
                             'octets' % (n, t, len(brut)))
        self.pot = bytearray(brut[POT:t])
        self._pot0 = POT
        self.textures = []
        for k in range(n):
            i, o = struct.unpack_from('<2I', brut, t + k * PAS)
            if not POT <= o < t:
                raise ValueError('texture %d : offset 0x%X hors du pot' % (k, o))
            self.textures.append([i, o])

    def nom(self, off):
        i = self.pot.index(b'\x00', off - self._pot0)
        return self.pot[off - self._pot0:i].decode('latin-1')

    def _ajouter(self, texte):
        off = self._pot0 + len(self.pot)
        self.pot += texte.encode('ascii') + b'\x00'
        return off

    def triee(self):
        return all(self.textures[k][0] <= self.textures[k + 1][0]
                   for k in range(len(self.textures) - 1))

    def identifiants(self):
        return {i for i, _ in self.textures}

    def ajouter(self, nom, identifiant):
        """INSERE a sa place : la table est triee, et on ne casse pas ca.

        `obj_db` s'ajoute a la fin parce que ses tables ne sont pas triees.
        Ici elles le sont sur les 25 992 entrees, et rien ne dit que le moteur
        n'y fasse pas une dichotomie. On insere.
        """
        if identifiant in self.identifiants():
            raise ValueError('l identifiant %d est deja pris (%s)'
                             % (identifiant,
                                next(self.nom(o) for i, o in self.textures
                                     if i == identifiant)))
        off = self._ajouter(nom)
        k = 0
        while k < len(self.textures) and self.textures[k][0] < identifiant:
            k += 1
        self.textures.insert(k, [identifiant, off])
        return k

    def octets(self):
        t = POT + len(self.pot)
        out = bytearray()
        out += struct.pack('<4I', len(self.textures), t, *self.reste)
        out += self.pot
        for i, o in self.textures:
            out += struct.pack('<2I', i, o)
        return bytes(out)


def charger(chemin=DEFAUT):
    return Base(io.open(chemin, 'rb').read())


def essai(chemin=DEFAUT):
    brut = io.open(chemin, 'rb').read()
    b = charger(chemin)
    rendu = b.octets()
    print('fichier : %s' % chemin)
    print('   %d octets ; %d textures ; pot %d octets'
          % (len(brut), len(b.textures), len(b.pot)))
    print('   table triee par identifiant : %s' % ('oui' if b.triee() else 'NON'))
    print('   identifiants de %d a %d, index max %d'
          % (min(b.identifiants()), max(b.identifiants()), len(b.textures) - 1))
    print('reecrit : %d octets' % len(rendu))
    if rendu == brut:
        print()
        print('ALLER-RETOUR IDENTIQUE A L OCTET PRES.')
        return 0
    k = next((i for i in range(min(len(rendu), len(brut)))
              if rendu[i] != brut[i]), min(len(rendu), len(brut)))
    print()
    print('ECART au premier octet 0x%X' % k)
    print('   attendu %s' % brut[k:k + 24].hex())
    print('   obtenu  %s' % rendu[k:k + 24].hex())
    return 1


def main():
    argv = sys.argv[1:]
    chemin = DEFAUT
    if '--fichier' in argv:
        i = argv.index('--fichier')
        chemin = argv[i + 1]
        del argv[i:i + 2]

    if '--essai' in argv or not argv:
        return essai(chemin)

    b = charger(chemin)

    if '--montrer' in argv:
        motif = argv[argv.index('--montrer') + 1].upper()
        trouve = [(i, b.nom(o)) for i, o in b.textures if motif in b.nom(o)]
        print('%d texture(s) dont le nom contient « %s »' % (len(trouve), motif))
        for i, nom in trouve[:24]:
            print('   id 0x%-6X %-6d %s' % (i, i, nom))
        if len(trouve) > 24:
            print('   … et %d autres' % (len(trouve) - 24))
        return 0

    if '--libres' in argv:
        pris = b.identifiants()
        haut = max(pris)
        trous, debut = [], None
        for i in range(0, haut + 400):
            if i not in pris and debut is None:
                debut = i
            elif i in pris and debut is not None:
                trous.append((debut, i - 1))
                debut = None
        if debut is not None:
            trous.append((debut, haut + 400))
        print('%d textures ; identifiants de %d a %d'
              % (len(b.textures), min(pris), haut))
        print('%d plage(s) libre(s) ; les plus grandes :' % len(trous))
        for a, z in sorted(trous, key=lambda p: p[0] - p[1])[:6]:
            print('   %6d .. %-6d  (%d)' % (a, z, z - a + 1))
        return 0

    if '--ajouter' in argv:
        nom = argv[argv.index('--ajouter') + 1]
        if '--id' not in argv:
            print('--ajouter demande --id <identifiant>. '
                  '`--libres` montre les plages disponibles.')
            return 1
        ident = int(argv[argv.index('--id') + 1], 0)
        try:
            k = b.ajouter(nom, ident)
        except ValueError as e:
            # Un refus est un resultat, pas un plantage : on le DIT, et on
            # renvoie vers l outil qui donne la reponse.
            print('REFUS : %s' % e)
            print('`--libres` montre les plages d identifiants disponibles.')
            return 1
        print('texture « %s » inseree au rang %d, identifiant %d (0x%X)'
              % (nom, k, ident, ident))
        print('   la table reste triee : %s' % ('oui' if b.triee() else 'NON'))
        print()
        print('RAPPEL : un decor IMPORTE n a rien a ajouter ici. Son archive')
        print('garde ses noms et ses identifiants de texture, qui sont deja')
        print('dans cette base. Seule une texture vraiment neuve en demande.')
        if '--sortie' in argv:
            s = argv[argv.index('--sortie') + 1]
            io.open(s, 'wb').write(b.octets())
            print()
            print('ecrit : %s (%d octets)' % (s, os.path.getsize(s)))
        else:
            print()
            print('(rien n a ete ecrit : ajoutez --sortie <fichier>)')
        return 0

    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
