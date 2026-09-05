#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Renommer un libelle du jeu, dans la table de textes du `.par`.

Les entrees de menu ne sont pas des chaines du binaire : ce sont des
identifiants resolus dans `string_array.farc`, un FArc NON compresse de
l'archive `vf5fs_data.par`. On peut donc reecrire un texte **sur place**, sans
reconstruire l'archive -- a condition que le nouveau tienne dans l'ancien, la
chaine etant terminee par zero.

    py -3 tools/renommer_libelle.py 0x180 "OPTIONS"
    py -3 tools/renommer_libelle.py 0x180            (montre le texte actuel)
    py -3 tools/renommer_libelle.py --rendre 0x180   (remet l'original)

PIEGE, et il est grave : `vf5fs_data.par` a longtemps ete un **lien dur** vers
le dump en lecture seule ; ecrire dedans aurait ecrit dans le dump. L'outil
REFUSE d'ecrire tant que le fichier a plus d'un lien. Ne pas contourner : faire
une vraie copie d'abord.

Les originaux sont gardes dans `analysis/libelles_renommes.json`, ce qui rend
`--rendre` possible meme apres coup.
"""
import io
import json
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import sllz                                                  # noqa: E402

PAR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_data.par')
CACHE = os.path.join(RACINE, 'extracted', 'string_array_en.bin')
JOURNAL = os.path.join(RACINE, 'analysis', 'libelles_renommes.json')
FARC_EN = 0x44                     # ou commence string_array_en.bin dans le FArc


def emplacement():
    """Rend (offset du .bin anglais dans le .par, sa taille)."""
    p = sllz.Par(PAR)
    for k, nom, drapeaux, taille, comp, offset in p.entrees():
        if nom == 'string_array.farc':
            if comp and comp != taille:
                raise SystemExit('REFUS : string_array.farc est compresse '
                                 '(%d -> %d). L\'ecriture sur place ne vaut '
                                 'que pour du non compresse.' % (taille, comp))
            return offset + FARC_EN, taille - FARC_EN
    raise SystemExit('REFUS : string_array.farc absent de l\'index du .par.')


def lire_table():
    base, n = emplacement()
    with open(PAR, 'rb') as fp:
        fp.seek(base)
        return base, fp.read(n)


def texte(en, i):
    if i < 0 or 4 * i + 4 > len(en):
        return None, None
    p = struct.unpack_from('>I', en, 4 * i)[0]        # GROS-BOUTISTE
    if p <= 0 or p >= len(en):
        return None, None
    fin = en.find(b'\0', p)
    return p, en[p:fin].decode('utf-8', 'replace')


def journal_lire():
    if os.path.exists(JOURNAL):
        with io.open(JOURNAL, encoding='utf-8') as fp:
            return json.load(fp)
    return {}


def journal_ecrire(j):
    os.makedirs(os.path.dirname(JOURNAL), exist_ok=True)
    with io.open(JOURNAL, 'w', encoding='utf-8') as fp:
        json.dump(j, fp, ensure_ascii=False, indent=2, sort_keys=True)


def ecrire(ident, neuf):
    st = os.stat(PAR)
    if st.st_nlink > 1:
        raise SystemExit(
            'REFUS : vf5fs_data.par a %d liens durs -- il pointe encore sur le '
            'dump en lecture seule. Ecrire ici ecrirait DANS LE DUMP. Faites '
            'une vraie copie d\'abord.' % st.st_nlink)
    base, en = lire_table()
    ou, ancien = texte(en, ident)
    if ou is None:
        raise SystemExit('REFUS : l\'identifiant 0x%X n\'a pas de texte.' % ident)
    octets_neuf = neuf.encode('utf-8')
    octets_anc = ancien.encode('utf-8')
    if len(octets_neuf) > len(octets_anc):
        raise SystemExit(
            'REFUS : « %s » fait %d octets, l\'ancien « %s » n\'en fait que %d. '
            'L\'ecriture sur place ne peut que raccourcir.'
            % (neuf, len(octets_neuf), ancien, len(octets_anc)))
    j = journal_lire()
    cle = '0x%X' % ident
    if cle not in j:
        j[cle] = ancien
    with open(PAR, 'r+b') as fp:
        fp.seek(base + ou)
        fp.write(octets_neuf + b'\0' * (len(octets_anc) - len(octets_neuf) + 1))
    journal_ecrire(j)
    if os.path.exists(CACHE):
        os.remove(CACHE)          # que `libelles.py` relise la table modifiee
    print('0x%X : « %s »  ->  « %s »' % (ident, ancien, neuf))
    print('   ecrit a l\'offset 0x%X du .par' % (base + ou))


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    if argv[0] == '--rendre':
        j = journal_lire()
        cle = '0x%X' % int(argv[1], 0)
        if cle not in j:
            raise SystemExit('REFUS : aucun original garde pour %s.' % cle)
        ecrire(int(argv[1], 0), j[cle])
        return 0
    ident = int(argv[0], 0)
    if len(argv) == 1:
        base, en = lire_table()
        ou, t = texte(en, ident)
        print('0x%X : « %s »   (offset 0x%X dans le .par)'
              % (ident, t, base + ou if ou else 0))
        return 0
    ecrire(ident, argv[1])
    return 0


if __name__ == '__main__':
    sys.exit(main())
