#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES PICTOS DE BOUTON EN XBOX -- un octet par occurrence.

LA MESURE QUI COMMANDE CET OUTIL (2026-10-10, journal 169-170). Quatre
codepoints differents ont ete poses sur les quatre lignes d OPTIONS > Controls
et l ecran photographie (`tools/pictos_essai.cmd`) :

    U+E000  -> l ecran dessine le ROND PlayStation   (la planche y met le B)
    U+E003  -> l ecran dessine le CARRE PlayStation  (la planche y met le X)
    U+E015  -> l ecran dessine le B XBOX             (la planche y met le rond)
    U+E01A  -> l ecran dessine le P              <-- le TEMOIN, intact

LES DEUX JEUX SONT DONC PERMUTES, et seulement eux : le temoin hors de la
plage sort juste, et le START du bandeau du bas (U+E004/E005) aussi. Ce n est
ni le texte, ni la planche, ni `fontmap.bin` -- les trois disent Xbox pour
U+E000..E003, et c est verifie :

  . `spr_n_fnt32` est identique a l octet pres dans le `.par` et sur le disque ;
  . `fontmap.bin` n existe qu en UN exemplaire, sans aucun doublon de
    codepoint, et envoie U+E000..E003 sur la rangee 56 colonnes 50-53 ;
  . aucune des 23 052 chaines ne porte U+E014..E018.

Ce n est pas non plus la table d echappements (`--boutons-xbox`) : celle-ci est
un dictionnaire NOM -> glyphe, et aucun libelle ne cite un `ESC_BTN_*`.

LE CORRECTIF EST DONC DANS LE TEXTE, ET IL FAIT UN OCTET PAR OCCURRENCE. On
ecrit le codepoint de l AUTRE jeu, celui que le moteur traduit vers l art Xbox :

    U+E000 -> U+E015      EE 80 80 -> EE 80 95      rond   -> B
    U+E001 -> U+E016      EE 80 81 -> EE 80 96      croix  -> A
    U+E002 -> U+E017      EE 80 82 -> EE 80 97      triangle -> Y
    U+E003 -> U+E018      EE 80 83 -> EE 80 98      carre  -> X

Trois octets pour trois : AUCUN pointeur de la table ne bouge, et la
correspondance est celle de SEGA elle-meme (la table d echappements nomme
U+E000 `ESC_BTN_CIRCLE` et U+E015 `ESC_BTN_CIRCLE_PS3`).

ON ECRIT DANS LA TABLE VIVANTE, `vf5fs_media/rom/string_array.farc` -- le
fichier libre que `textes_quest.py` a depose et que le moteur lit a la place de
celui du `.par`. L original est garde a cote en `.pictos_origine`.

L OPERATION EST IDEMPOTENTE : on ne traduit que 0x80-0x83, jamais 0x95-0x98.

    py -3 tools/pictos_xbox.py --poser
    py -3 tools/pictos_xbox.py --controle
    py -3 tools/pictos_xbox.py --retirer
"""
import os
import shutil
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
TABLE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media',
                     'rom', 'string_array.farc')
SAUVE = TABLE + '.pictos_origine'

# (ce qu on remplace, par quoi, le nom que SEGA leur donne)
PAIRES = (
    (0xE000, 0xE015, 'CIRCLE   -> le B'),
    (0xE001, 0xE016, 'CROSS    -> le A'),
    (0xE002, 0xE017, 'TRIANGLE -> le Y'),
    (0xE003, 0xE018, 'SQUARE   -> le X'),
)


# LES NOMS DE TOUCHES, demande de Frederic du 2026-10-10 : « passe les en
# LB / RB / BACK ». Chaque libelle a son PROPRE pointeur -- verifie, aucun
# n est partage -- et le nom neuf tient dans la place de l ancien, donc on
# ecrit EN PLACE et rien ne bouge.
#
# Ce que l ecran Controls dit lui-meme de ces lignes : NO USE, toutes. Le
# modele d entrees APM3 ne porte que QUATRE boutons d action (les bits 4 a 7
# du masque arcade, codes 9, 10, 13 et 14), dont le jeu n en emploie que
# trois -- P, K et G. Les gachettes n ont rien a quoi se brancher ici ; elles
# sont nommees juste, voila tout.
NOMS_TOUCHES = {
    0x33D: 'LB button',
    0x33E: 'LT button',
    0x33F: 'LS button',
    0x340: 'RB button',
    0x341: 'RT button',
    0x342: 'RS button',
    0x346: 'BACK button',
}


def renommer(d, base, taille, poser):
    """Ecrit les noms Xbox a la place des noms PlayStation, EN PLACE.

    Refuse tout nom plus long que celui qu il remplace : la table est un
    tableau de pointeurs, et rallonger une chaine demanderait de la
    reconstruire entiere.
    """
    n = 0
    for ident, neuf in sorted(NOMS_TOUCHES.items()):
        if 4 * ident + 4 > taille:
            continue
        p = struct.unpack_from('>I', d, base + 4 * ident)[0]
        if p <= 0 or p >= taille:
            continue
        o = base + p
        fin = d.find(b'\x00', o)
        ancien = bytes(d[o:fin])
        b = neuf.encode('ascii')
        if len(b) > len(ancien):
            raise AssertionError('%r (%d) ne tient pas dans %r (%d)'
                                 % (neuf, len(b), ancien, len(ancien)))
        if ancien == b:
            continue
        n += 1
        if poser:
            d[o:fin] = b + b'\x00' * (len(ancien) - len(b))
    return n


def membres(d):
    """Les (nom, offset, taille) d un FArc non compresse."""
    if d[:4] != b'FArc':
        raise SystemExit('%s n est pas un FArc' % TABLE)
    fin_entete = struct.unpack_from('>I', d, 4)[0]
    p = 0x0C
    out = []
    while p < fin_entete:
        f = d.find(b'\x00', p)
        if f < 0:
            break
        nom = d[p:f].decode('ascii', 'replace')
        p = f + 1
        # La borne `fin_entete` vaut la fin des NOMS, pas celle des entrees :
        # le couple {offset, taille} de la DERNIERE y deborde. Payer cette
        # ligne a coute un membre entier -- `string_array_jp.bin` sortait de
        # l inventaire sans un mot.
        if p + 8 > len(d):
            break
        off, taille = struct.unpack_from('>II', d, p)
        p += 8
        if nom:
            out.append((nom, off, taille))
    return out


def parcourir(d, base, taille, traduire):
    """Applique `traduire` a CHAQUE chaine du tableau de pointeurs.

    On passe par les pointeurs, et non par un balayage d octets : les trois
    octets `EE 80 8x` existent aussi dans le tableau de pointeurs lui-meme et
    dans d autres donnees, et un balayage les toucherait sans le dire.
    Une chaine partagee par plusieurs identifiants est vue plusieurs fois --
    sans consequence, la traduction etant idempotente.
    """
    vus = set()
    compte = {a: 0 for a, _b, _n in PAIRES}
    i = 0
    while 4 * i + 4 <= taille:
        p = struct.unpack_from('>I', d, base + 4 * i)[0]
        i += 1
        if p <= 0 or p >= taille:
            continue
        if p in vus:
            continue
        vus.add(p)
        o = base + p
        fin = d.find(b'\x00', o)
        if fin < 0 or fin - o > 4096:
            continue
        for k in range(o, fin - 2):
            if d[k] == 0xEE and d[k + 1] == 0x80:
                for a, b, _nom in PAIRES:
                    if d[k + 2] == (a & 0x3F) | 0x80:
                        compte[a] += 1
                        if traduire:
                            d[k + 2] = (b & 0x3F) | 0x80
                        break
    return compte


def main(argv):
    quoi = 'controle'
    for a in argv:
        if a in ('--poser', '--retirer', '--controle'):
            quoi = a[2:]
    if not os.path.exists(TABLE):
        print('ABSENT : %s' % TABLE)
        print('La table vivante est posee par tools/textes_quest.py.')
        return 1

    if quoi == 'retirer':
        if not os.path.exists(SAUVE):
            print('Rien a rendre : %s n existe pas.' % SAUVE)
            return 1
        shutil.copyfile(SAUVE, TABLE)
        os.remove(SAUVE)
        print('Table rendue dans son etat d origine.')
        return 0

    d = bytearray(open(TABLE, 'rb').read())
    noms = membres(d)
    poser = (quoi == 'poser')
    if poser and not os.path.exists(SAUVE):
        shutil.copyfile(TABLE, SAUVE)
        print('original garde : %s' % os.path.basename(SAUVE))

    total = 0
    noms_a_faire = 0
    for nom, off, taille in noms:
        c = parcourir(d, off, taille, poser)
        s = ' '.join('U+%04X x%d' % (a, c[a]) for a, _b, _n in PAIRES)
        r = renommer(d, off, taille, poser)
        print('  %-24s %s   noms de touches : %d' % (nom, s, r))
        total += sum(c.values())
        noms_a_faire += r

    if poser:
        open(TABLE, 'wb').write(bytes(d))
        print()
        print('%d glyphe(s) passe(s) en Xbox. Un octet chacun ; aucun pointeur'
              ' n a bouge.' % total)
        print('%d nom(s) de touche reecrit(s) : L1/L2/L3/R1/R2/R3 -> '
              'LB/LT/LS/RB/RT/RS, et SELECT -> BACK.' % noms_a_faire)
        for a, b, nom in PAIRES:
            print('   U+%04X -> U+%04X   %s' % (a, b, nom))
    else:
        print()
        reste = total + noms_a_faire
        if reste:
            print('%d glyphe(s) et %d nom(s) restent a poser : la table n est'
                  ' PAS posee.' % (total, noms_a_faire))
        else:
            print('Rien a faire : glyphes et noms de touches sont deja poses.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
