#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les bouchons du build borne, et ce qu'ils valent chez R.E.V.O.

Le build APM3 a remplace des fonctions entieres par des retours constants. Trois
etaient deja connues, et chacune a coute une demi-journee avant d'etre vue :

    0x180007430   ret 0                  creneau de vtable neutralise
    0x180007450   xor al, al ; ret       le garde de UNLOCK_DURAL
    0x180029FB0   mov al, 1 ; ret        l'attente d'initialisation du menu

Elles se reconnaissent a l'oeil une fois qu'on les regarde, mais pas quand on
suit un chemin d'execution : un predicat qui rend toujours la meme chose ne se
distingue pas d'un predicat qui a decide. D'ou cet outil : **les enumerer
toutes, d'un coup**, et compter qui les appelle.

Puis la deuxieme moitie, qui est le vrai apport : **les memes fonctions existent
pour de vrai dans R.E.V.O.**, le portage PC du meme moteur (release 6.000). Une
fonction bouchonnee chez nous et pleine chez eux, c'est une coupe identifiee, et
son corps dit ce que le code appelant attendait.

Usage :
    py -3 tools/bouchons.py                       liste les bouchons d'APM3
    py -3 tools/bouchons.py --appelants           avec le nombre d'appelants
    py -3 tools/bouchons.py --zone 0x180150000 0x180190000
    py -3 tools/bouchons.py --revo                l'inventaire de R.E.V.O. aussi
"""
import collections
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import pe_disasm as P                                       # noqa: E402

APM3 = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                    'vf5fs-pxd-w64-Retail_APM3.dll')
REVO = (r'C:\Program Files (x86)\Steam\steamapps\common\VFREVO'
        r'\runtime\media\vf5fs\vf5fs-pxd-w64-d3d12_SteamRetail.dll')

# Un bouchon = une fonction dont le corps entier tient en un retour constant.
# On accepte les formes rencontrees dans ce moteur, pas davantage : mieux vaut
# rater un cas exotique que compter comme bouchon une fonction qui decide.
FORMES = {
    'c30000': None,                       # (place tenue, voir plus bas)
}


def corps(img, deb, fin):
    o = img.va2off(deb)
    if o is None:
        return None
    return img.data[o:o + (fin - deb)]


def est_bouchon(img, deb, fin):
    """Rend la valeur constante rendue, ou None si la fonction decide."""
    if fin - deb > 16:
        return None
    ins = list(img.md.disasm(corps(img, deb, fin) or b'', deb))
    if not ins:
        return None
    # On tolere les int3 de rembourrage a la fin.
    utiles = [x for x in ins if x.mnemonic != 'int3']
    if not utiles or utiles[-1].mnemonic != 'ret':
        return None
    val = 'rien'
    for x in utiles[:-1]:
        if x.mnemonic == 'xor' and len(set(x.op_str.split(', '))) == 1:
            val = 0
        elif x.mnemonic == 'mov' and x.op_str.startswith(('al, ', 'eax, ',
                                                          'rax, ')):
            try:
                val = int(x.op_str.split(', ')[1], 0)
            except ValueError:
                return None
        else:
            return None
    return val


def cibles_appelees(img, fs):
    """Toutes les cibles de `call` directs, avec le nombre d'appels et les
    fonctions appelantes.

    Passer par les cibles d'appel plutot que par `.pdata` n'est pas un detail :
    **un bouchon est une fonction feuille sans prologue, donc SANS entree
    `.pdata`**. Les trois bouchons deja connus (`0x180007430`, `0x180007450`,
    `0x180029FB0`) n'apparaissent dans aucune entree de deroulement. Les
    chercher la etait l'erreur ; ici on part de ce qui les appelle, ce qui ne
    peut pas les manquer.
    """
    cnt = collections.Counter()
    sites = collections.defaultdict(list)
    for deb, fin in fs:
        b = corps(img, deb, fin)
        if not b:
            continue
        for x in img.md.disasm(b, deb):
            if x.mnemonic != 'call' or not x.op_str.startswith('0x'):
                continue
            c = int(x.op_str, 16)
            cnt[c] += 1
            if len(sites[c]) < 12:
                sites[c].append((x.address, deb))
    return cnt, sites


def bouchon_a(img, va):
    """Classe la fonction qui commence a `va` : constante rendue, ou None.

    On desassemble au plus 6 instructions depuis `va` ; le premier `ret`
    termine. Une fonction qui fait autre chose qu'affecter une constante et
    rendre n'est pas un bouchon.
    """
    o = img.va2off(va)
    if o is None:
        return None
    val = 'rien'
    n = 0
    for x in img.md.disasm(img.data[o:o + 24], va):
        n += 1
        if n > 6:
            return None
        if x.mnemonic == 'ret':
            return val
        if x.mnemonic == 'xor' and len(set(x.op_str.split(', '))) == 1:
            val = 0
        elif x.mnemonic == 'mov' and x.op_str.split(', ')[0] in (
                'al', 'eax', 'rax'):
            try:
                val = int(x.op_str.split(', ')[1], 0)
            except ValueError:
                return None
        else:
            return None
    return None


def inventaire(chemin, zone=None):
    img = P.Image(chemin)
    fs = P.runtime_functions(img)
    cnt, sites = cibles_appelees(img, fs)
    out = []
    for va, n in cnt.items():
        if zone and not (zone[0] <= va < zone[1]):
            continue
        v = bouchon_a(img, va)
        if v is not None:
            out.append((va, n, v))
    return img, fs, out, cnt, sites


def main():
    argv = sys.argv[1:]
    zone = None
    if '--zone' in argv:
        i = argv.index('--zone')
        zone = (int(argv[i + 1], 0), int(argv[i + 2], 0))

    img, fs, bouchons, cnt, sites = inventaire(APM3, zone)
    total = sum(n for _, n, _ in bouchons)
    print('APM3 : %d fonctions, %d cible(s) d appel, %d bouchon(s) '
          'appele(s) %d fois%s'
          % (len(fs), len(cnt), len(bouchons), total,
             (' dans 0x%X-0x%X' % zone) if zone else ''))

    connus = {0x180007430: 'creneau de vtable neutralise',
              0x180007450: 'garde de UNLOCK_DURAL',
              0x180029FB0: 'attente d initialisation du menu'}
    print()
    print('  %-14s %9s %8s   %s' % ('adresse', 'appelants', 'rend', 'note'))
    for va, n, val in sorted(bouchons, key=lambda t: -t[1]):
        print('  0x%-12X %9d %8s   %s' % (va, n, val, connus.get(va, '')))

    if '--sites' in argv:
        print()
        print('--- ou sont-ils appeles ---')
        for va, n, val in sorted(bouchons, key=lambda t: -t[1])[:12]:
            lieux = ', '.join('0x%X' % s[1] for s in sites[va][:8])
            print('  0x%-12X rend %-6s depuis %s' % (va, val, lieux))
    return 0


if __name__ == '__main__':
    sys.exit(main())
