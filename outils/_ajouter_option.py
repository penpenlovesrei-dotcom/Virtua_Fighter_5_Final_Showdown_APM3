#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ajoute une option a la ligne de patch d'un lanceur, SANS toucher au reste.

Les `.cmd` du depot sont en CRLF et contiennent des octets non ASCII herites
(des guillemets francais dans les en-tetes). Les reecrire entierement, c'est
risquer de les vider -- ce qui est deja arrive a `tools/quest.cmd`. On
travaille donc en OCTETS, sur la seule sous-chaine visee.

    py -3 tools/_ajouter_option.py <lanceur.cmd> <--option> [apres]
"""
import os
import sys


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    chemin, option = sys.argv[1], sys.argv[2]
    apres = sys.argv[3] if len(sys.argv) > 3 else None
    with open(chemin, 'rb') as fp:
        d = fp.read()
    opt = option.encode('ascii')
    if opt in d:
        print('%s : %s y est deja.' % (os.path.basename(chemin), option))
        return 0
    if apres is None:
        sys.exit('il faut dire APRES quelle sous-chaine inserer')
    anc = apres.encode('ascii')
    if d.count(anc) != 1:
        sys.exit('%r apparait %d fois dans %s : ambigu'
                 % (apres, d.count(anc), chemin))
    i = d.index(anc) + len(anc)
    neuf = d[:i] + b' ' + opt + d[i:]
    with open(chemin, 'wb') as fp:
        fp.write(neuf)
    print('%s : %s ajoute apres %r (%d -> %d octets)'
          % (os.path.basename(chemin), option, apres, len(d), len(neuf)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
