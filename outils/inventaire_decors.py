#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Inventaire et comparaison des decors des quatre generations.

Compare, decor par decor, ce qui a ete extrait dans `extracted/decors/` :

    VF5_VERB      Virtua Fighter 5 ver.B   Lindbergh, snapshot 2007-05-30
    VF5R          Virtua Fighter 5 R       Lindbergh, 2008-06-16
    VF5FS_LIND    Final Showdown Rev A     Lindbergh, 2010-06-28
    APM3          Final Showdown           borne APM3, lu dans le .par

Rend `analysis/decors_lindbergh.csv` et une table lisible. La taille de
l'objset est la mesure la plus parlante : c'est elle qui a montre que cinq
decors ont MAIGRI entre R et Final Showdown.

    py -3 tools/inventaire_decors.py
"""
import csv
import hashlib
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
DEC = os.path.join(RACINE, 'extracted', 'decors')
JEUX = ['VF5_VERB', 'VF5R', 'VF5FS_LIND']
PAR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_data.par')
CSV = os.path.join(RACINE, 'analysis', 'decors_lindbergh.csv')


def taille(p):
    return os.path.getsize(p) if os.path.exists(p) else 0


def sha(p, n=1 << 20):
    if not os.path.exists(p):
        return ''
    h = hashlib.sha256()
    with open(p, 'rb') as fp:
        while True:
            b = fp.read(n)
            if not b:
                break
            h.update(b)
    return h.hexdigest()[:16]


def apm3_objsets():
    """Tailles decompressees des `stg*.farc` de la borne, lues dans l'index."""
    out = {}
    sys.path.insert(0, ICI)
    import sllz                                                # noqa: E402
    sauve = sys.argv
    tmp = os.path.join(DEC, '_apm3_index.txt')
    sys.argv = ['sllz', 'lister', PAR, 'stg']
    dep = sys.stdout
    with open(tmp, 'w', encoding='utf-8') as fp:
        sys.stdout = fp
        try:
            sllz.main()
        finally:
            sys.stdout = dep
            sys.argv = sauve
    for l in open(tmp, encoding='utf-8'):
        m = re.match(r'\s+(stg[a-z0-9]+)\.farc\s+(\d+) o', l)
        if m:
            out[m.group(1)[3:]] = int(m.group(2))
    return out


def main():
    codes = set()
    par_jeu = {}
    for j in JEUX:
        d = os.path.join(DEC, j, 'objset')
        noms = sorted(os.listdir(d)) if os.path.isdir(d) else []
        m = {}
        for n in noms:
            if n.startswith('stg') and n.endswith('.farc'):
                m[n[3:-5]] = os.path.join(d, n)
        par_jeu[j] = m
        codes |= set(m)
    apm = apm3_objsets()
    codes |= set(apm)
    codes = sorted(codes)

    lignes = []
    print('%-8s %12s %12s %12s %12s   %s'
          % ('decor', 'VF5 ver.B', 'VF5 R', 'FS Lindbergh', 'FS APM3',
             'remarque'))
    for c in codes:
        t = [taille(par_jeu[j].get(c, '')) for j in JEUX]
        ta = apm.get(c, 0)
        rem = []
        if t[0] and not t[1]:
            rem.append('DISPARU apres ver.B')
        if not t[0] and t[1]:
            rem.append('nouveau en R')
        if not t[1] and ta:
            rem.append('nouveau en FS')
        if t[2] and ta and t[2] == ta:
            rem.append('FS Lind == APM3')
        elif t[2] and ta:
            rem.append('FS Lind != APM3')
        print('%-8s %12s %12s %12s %12s   %s'
              % (c, t[0] or '-', t[1] or '-', t[2] or '-', ta or '-',
                 ', '.join(rem)))
        lignes.append([c, t[0], t[1], t[2], ta, ' | '.join(rem)])

    with open(CSV, 'w', encoding='utf-8', newline='') as fp:
        w = csv.writer(fp, delimiter=';')
        w.writerow(['decor', 'VF5_verB', 'VF5R', 'FS_Lindbergh', 'FS_APM3',
                    'remarque'])
        w.writerows(lignes)
    print()
    print('=> %s' % CSV)
    for j in JEUX:
        n = len(par_jeu[j])
        t = sum(taille(p) for p in par_jeu[j].values())
        print('   %-12s %2d objsets  %7.1f Mo' % (j, n, t / 1048576))
    print('   %-12s %2d objsets' % ('APM3', len(apm)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
