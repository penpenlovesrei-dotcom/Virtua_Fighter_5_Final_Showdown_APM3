#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les `.cmd` du depot : ASCII pur, CRLF, non vides, en-tete explicatif.

Le piege est paye : un « « » dans un en-tete a VIDE `tools/quest.cmd` (0
octet). Ce controle passe sur tous les lanceurs, ou sur ceux qu'on lui
nomme, et rend un code non nul au premier defaut.

    py -3 tools/verifier_cmd.py                 tous les tools/*.cmd
    py -3 tools/verifier_cmd.py tools/x.cmd     ceux-la
"""
import glob
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)


def verifier(chemin):
    """Rend la liste des defauts de ce fichier."""
    defauts = []
    with open(chemin, 'rb') as fp:
        d = fp.read()
    if not d:
        return ['VIDE (0 octet)']
    for i, o in enumerate(d):
        if o > 0x7E or (o < 0x20 and o not in (0x09, 0x0A, 0x0D)):
            ligne = d[:i].count(b'\n') + 1
            defauts.append('octet non ASCII 0x%02X, ligne %d' % (o, ligne))
            break
    lignes = d.split(b'\n')
    sans_cr = [i + 1 for i, l in enumerate(lignes[:-1])
               if not l.endswith(b'\r')]
    if sans_cr:
        defauts.append('%d ligne(s) sans CRLF (la premiere : %d)'
                       % (len(sans_cr), sans_cr[0]))
    if not d.lstrip().lower().startswith(b'@echo off'):
        defauts.append('ne commence pas par `@echo off`')
    if b'rem ' not in d[:400].lower():
        defauts.append('pas d en-tete `rem` dans les 400 premiers octets')
    return defauts


def main():
    cibles = sys.argv[1:]
    if not cibles:
        cibles = sorted(glob.glob(os.path.join(ICI, '*.cmd')))
        cibles += sorted(glob.glob(os.path.join(RACINE, '*.cmd')))
    mauvais = 0
    for c in cibles:
        d = verifier(c)
        nom = os.path.relpath(c, RACINE)
        if d:
            mauvais += 1
            print('DEFAUT  %-34s %s' % (nom, ' ; '.join(d)))
    print()
    print('%d lanceur(s) controle(s), %d en defaut.' % (len(cibles), mauvais))
    return 1 if mauvais else 0


if __name__ == '__main__':
    sys.exit(main())
