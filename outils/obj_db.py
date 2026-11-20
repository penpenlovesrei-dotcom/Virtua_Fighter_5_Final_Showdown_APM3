#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""`obj_db.bin` : les jeux d'objets, leurs fichiers, et leurs objets.

C'est la base qui decide de la FAISABILITE d'un decor ajoute : l'identifiant
d'objset qu'un descripteur demande en `+0x10` est cherche ici, par dichotomie
dans un vecteur construit au demarrage (`0x1800F9450`, rempli par
`0x18006B7E0` qui lit `./rom/objset/` + `obj_db.bin`).

LA CARTE, mesuree le 2026-09-09 -- et il n'y a PLUS de zone inexpliquee

    0x000000   en-tete, huit u32
    0x000020   POT A : les chaines de la table des jeux
    0x042760   table des JEUX D'OBJETS   6044 x 0x24
    0x077950   POT B : les noms d'objets
    0x0F3F80   table des OBJETS          17744 x 8
    0x116A00   fin du fichier, a l'octet pres

`ajouter_un_decor.md` §5 signalait « la zone 0x77890-0x0F3F80 n'est pas
expliquee ». Elle l'est : c'est le second pot de chaines, et il commence
EXACTEMENT ou finit la table des jeux (0x77950 -- l'adresse notee etait
approchee). Le premier nom qu'on y lit est `TEST_00A`, celui de l'objet 0.

    en-tete   +0x00 nombre de jeux     +0x04 le PLUS GRAND IDENTIFIANT
              (et non une version : mesure du 2026-09-10 sur trois bases.
               APM3 et APM3_FS : 6044 jeux, champ = 6149 = leur max id a
               l'unite pres. Xbox 360 : 1667 jeux, champ = 2119 -- superieur
               au compte, comme un max d'identifiants troue. `ajouter_jeu`
               le tient donc a jour, sinon un identifiant ajoute au-dela
               serait hors du domaine annonce.)
              +0x08 offset de leur table
              +0x0C nombre d'objets    +0x10 offset de leur table
              +0x14..+0x1C  zero

    jeu       +0x00 offset du NOM        "STGDJO"
    (0x24 o)  +0x04 IDENTIFIANT          28
              +0x08 offset "stgdjo_obj.bin"
              +0x0C offset "stgdjo_tex.bin"
              +0x10 offset "stgdjo.farc"
              +0x14..+0x20  quatre u32 a zero

    objet     +0x00 IDENTIFIANT EMPAQUETE  (objset << 16) | rang
    (8 o)     +0x04 offset du nom          "STGDJO_GND"

L'empaquetage est le meme que celui du descripteur de decor : `djo` demande
`0x1C0072 0x1C0076 0x1C0075 0x1C0074 0x1C0073`, soit objset 28, rangs 114 118
117 116 115 -- GND, RING, SKY, SDW, REFLECT. L'objset 28 porte 171 objets ;
seuls ces cinq sont nommes par le descripteur, les 166 autres sont des effets.

NI L'UNE NI L'AUTRE TABLE N'EST TRIEE. On peut donc ajouter a la fin sans rien
reordonner : le moteur construit son index trie au demarrage.

COMMENT ON REECRIT LE FICHIER, ET POURQUOI C'EST SUR

Les deux pots sont gardes tels quels, en octets, et on n'y AJOUTE qu'a la fin.
Les offsets du pot A ne bougent donc jamais (il commence a 0x20 dans les deux
cas) ; ceux du pot B se decalent d'une quantite connue -- la croissance du pot A
plus les entrees de jeu ajoutees. Sans ajout, le decalage est nul et le fichier
ressort **identique a l'octet pres**. C'est `--essai`, et c'est ce qui prouve
qu'on a compris la carte.

    py -3 tools/obj_db.py --essai
    py -3 tools/obj_db.py --montrer STGDJO
    py -3 tools/obj_db.py --libres                identifiants d'objset libres
    py -3 tools/obj_db.py --ajouter STGTRS --id 6000 --depuis STGDJO \
                          --fichiers stgtrs --sortie <fichier>
"""
import io
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
DEFAUT = os.path.join(RACINE, 'extracted', 'obj_db.bin')

ENTETE = 0x20
PAS_JEU = 0x24
PAS_OBJET = 8


class Base:
    def __init__(self, brut):
        (n_jeux, self.version, t_jeux,
         n_objets, t_objets) = struct.unpack_from('<5I', brut, 0)
        fin_jeux = t_jeux + n_jeux * PAS_JEU
        if t_jeux < ENTETE or fin_jeux > t_objets > len(brut):
            raise ValueError('en-tete incoherent')
        self.pot_a = bytearray(brut[ENTETE:t_jeux])
        self.pot_b = bytearray(brut[fin_jeux:t_objets])
        self._t_jeux0 = t_jeux
        self._pot_b0 = fin_jeux
        self.jeux = []
        for k in range(n_jeux):
            e = list(struct.unpack_from('<9I', brut, t_jeux + k * PAS_JEU))
            # ZERO EST UNE VALEUR : 191 jeux sur 6044 n'ont ni fichier d'objets,
            # ni fichier de textures, ni archive -- ce sont les objsets
            # d'ITEMS (AKIITM012, …), qui vivent dans l'archive d'un autre.
            # Refuser le zero faisait echouer le chargement des le rang 70.
            for o in (0, 2, 3, 4):
                if e[o] and not ENTETE <= e[o] < t_jeux:
                    raise ValueError('jeu %d : offset 0x%X hors du pot A'
                                     % (k, e[o]))
                if o == 0 and not e[o]:
                    raise ValueError('jeu %d : un jeu sans NOM' % k)
            self.jeux.append(e)
        self.objets = []
        for k in range(n_objets):
            i, o = struct.unpack_from('<2I', brut, t_objets + k * PAS_OBJET)
            if not self._pot_b0 <= o < t_objets:
                raise ValueError('objet %d : offset 0x%X hors du pot B' % (k, o))
            self.objets.append([i, o])
        if len(brut) != t_objets + n_objets * PAS_OBJET:
            raise ValueError('le fichier ne finit pas sur la table des objets')

    # --- chaines ------------------------------------------------------------
    def _lire(self, pot, base, off):
        i = pot.index(b'\x00', off - base)
        return pot[off - base:i].decode('latin-1')

    def nom_a(self, off):
        return self._lire(self.pot_a, ENTETE, off) if off else ''

    def nom_b(self, off):
        return self._lire(self.pot_b, self._pot_b0, off)

    def _ajouter_a(self, texte):
        """Ajoute une chaine au pot A et rend son offset (dans l'ancien repere).

        Le pot A commence a 0x20 avant comme apres : ses offsets sont donc
        directement valides.
        """
        off = ENTETE + len(self.pot_a)
        self.pot_a += texte.encode('ascii') + b'\x00'
        return off

    def _ajouter_b(self, texte):
        off = self._pot_b0 + len(self.pot_b)
        self.pot_b += texte.encode('ascii') + b'\x00'
        return off

    # --- lectures -----------------------------------------------------------
    def jeu(self, nom_ou_id):
        for k, e in enumerate(self.jeux):
            if self.nom_a(e[0]) == nom_ou_id or e[1] == nom_ou_id:
                return k, e
        return None, None

    def objets_de(self, objset):
        return [(i & 0xFFFF, self.nom_b(o)) for i, o in self.objets
                if (i >> 16) == objset]

    def identifiants(self):
        return sorted(e[1] for e in self.jeux)

    # --- ecriture -----------------------------------------------------------
    def ajouter_jeu(self, nom, identifiant, base_fichiers):
        if self.jeu(nom)[1] is not None:
            raise ValueError('le jeu « %s » existe deja' % nom)
        if identifiant in {e[1] for e in self.jeux}:
            raise ValueError('l identifiant %d est deja pris' % identifiant)
        e = [self._ajouter_a(nom), identifiant,
             self._ajouter_a('%s_obj.bin' % base_fichiers),
             self._ajouter_a('%s_tex.bin' % base_fichiers),
             self._ajouter_a('%s.farc' % base_fichiers), 0, 0, 0, 0]
        self.jeux.append(e)
        # Le champ +0x04 est le plus grand identifiant, pas une version : on le
        # tient a jour, sinon l'identifiant ajoute sort du domaine annonce.
        if identifiant > self.version:
            self.version = identifiant
        return len(self.jeux) - 1

    def ajouter_objet(self, objset, rang, nom):
        self.objets.append([(objset << 16) | rang, self._ajouter_b(nom)])

    def octets(self):
        t_jeux = ENTETE + len(self.pot_a)
        pot_b = t_jeux + len(self.jeux) * PAS_JEU
        t_objets = pot_b + len(self.pot_b)
        delta_b = pot_b - self._pot_b0
        out = bytearray()
        out += struct.pack('<8I', len(self.jeux), self.version, t_jeux,
                           len(self.objets), t_objets, 0, 0, 0)
        out += self.pot_a
        for e in self.jeux:
            out += struct.pack('<9I', *e)
        out += self.pot_b
        for i, o in self.objets:
            out += struct.pack('<2I', i, o + delta_b)
        return bytes(out)


def charger(chemin=DEFAUT):
    return Base(io.open(chemin, 'rb').read())


def essai(chemin=DEFAUT):
    brut = io.open(chemin, 'rb').read()
    b = charger(chemin)
    rendu = b.octets()
    print('fichier : %s' % chemin)
    print('   %d octets ; %d jeux d objets ; %d objets'
          % (len(brut), len(b.jeux), len(b.objets)))
    print('   pot A %d octets, pot B %d octets'
          % (len(b.pot_a), len(b.pot_b)))
    print('reecrit : %d octets' % len(rendu))
    if rendu == brut:
        print()
        print('ALLER-RETOUR IDENTIQUE A L OCTET PRES.')
        print('La carte est juste, la « zone inexpliquee » etait le pot B.')
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
        quoi = argv[argv.index('--montrer') + 1]
        try:
            quoi = int(quoi, 0)
        except ValueError:
            pass
        k, e = b.jeu(quoi)
        if e is None:
            print('aucun jeu d objets « %s »' % quoi)
            return 1
        objets = b.objets_de(e[1])
        print('%s : rang %d, identifiant %d' % (b.nom_a(e[0]), k, e[1]))
        print('   %s / %s / %s'
              % (b.nom_a(e[2]), b.nom_a(e[3]), b.nom_a(e[4])))
        print('   %d objet(s), rangs %d..%d'
              % (len(objets), min(r for r, _ in objets),
                 max(r for r, _ in objets)))
        for r, nom in objets:
            marque = '  <-- nomme par le descripteur' if r in (114, 115, 116,
                                                               117, 118) else ''
            if r >= 110 or r < 4:
                print('      rang %-4d %s%s' % (r, nom, marque))
        return 0

    if '--libres' in argv:
        pris = set(b.identifiants())
        print('%d jeux d objets ; identifiants de %d a %d'
              % (len(b.jeux), min(pris), max(pris)))
        trous, debut = [], None
        for i in range(0, max(pris) + 200):
            if i not in pris and debut is None:
                debut = i
            elif i in pris and debut is not None:
                trous.append((debut, i - 1))
                debut = None
        if debut is not None:
            trous.append((debut, max(pris) + 200))
        print('%d plage(s) libre(s) ; les plus utiles :' % len(trous))
        for a, z in trous[-6:]:
            print('   %d .. %d   (%d)' % (a, z, z - a + 1))
        print()
        print('L espace est TROUE et non borne : du5, gym et smo portent 5529,')
        print('2847 et 2848, pris ailleurs. Rien dans le moteur ne le borne.')
        return 0

    if '--ajouter' in argv:
        nom = argv[argv.index('--ajouter') + 1]
        depuis = argv[argv.index('--depuis') + 1] if '--depuis' in argv else None
        if not depuis or '--id' not in argv:
            print('--ajouter demande --id <identifiant> et --depuis <modele>.')
            return 1
        ident = int(argv[argv.index('--id') + 1], 0)
        base_f = (argv[argv.index('--fichiers') + 1] if '--fichiers' in argv
                  else nom.lower())
        _, m = b.jeu(depuis)
        if m is None:
            print('jeu modele « %s » inconnu' % depuis)
            return 1
        modele = b.objets_de(m[1])
        k = b.ajouter_jeu(nom, ident, base_f)
        for r, n in modele:
            b.ajouter_objet(ident, r, n)
        print('jeu « %s » ajoute au rang %d, identifiant %d' % (nom, k, ident))
        print('   %s_obj.bin / %s_tex.bin / %s.farc'
              % (base_f, base_f, base_f))
        print('   %d objets recopies de %s, rangs %d..%d, NOMS INCHANGES'
              % (len(modele), depuis, min(r for r, _ in modele),
                 max(r for r, _ in modele)))
        print()
        print('Les noms d objets sont recopies VERBATIM : une archive importee')
        print('puis renommee garde ses noms internes -- seuls les DEUX noms de')
        print('fichier changent, et c est `importer_decor.py --vers` qui les')
        print('reecrit dans l en-tete du FArC.')
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
