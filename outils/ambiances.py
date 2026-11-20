#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Classe TOUS les decors par leur ambiance lumineuse, toutes generations.

Les `light_param/*.txt` sont en texte clair et identiques entre le Final
Showdown Lindbergh et l'APM3 (les 206 fichiers, verifie dans
`analysis/import_decors.md` §5). On peut donc caracteriser l'ambiance de
chaque decor sans lancer le jeu.

Le critere est la couleur de brouillard `color` (la premiere, celle du fond)
et la troisieme `diffuse` du fichier `light_` (la lumiere d'appoint). Un decor
sombre a un brouillard proche du noir ; un decor de nuit y ajoute une
dominante BLEUE, un decor de couchant une dominante ROUGE.

    py -3 tools/ambiances.py
    py -3 tools/ambiances.py --seuil 0.35      ne montre que les sombres
"""
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
DEC = os.path.join(RACINE, 'extracted', 'decors')
JEUX = [('VF5 ver.B', 'VF5_VERB'), ('VF5 R', 'VF5R'),
        ('FS / APM3', 'VF5FS_LIND')]


def trio(txt, clef):
    m = re.search(clef + r' ([\d.eE+\-]+) ([\d.eE+\-]+) ([\d.eE+\-]+)', txt)
    return tuple(float(x) for x in m.groups()) if m else None


def teinte(c):
    r, v, b = c
    if max(c) < 0.02:
        return 'noir'
    if b > r * 1.3 and b > v * 1.1:
        return 'BLEUE'
    if r > b * 1.3 and r > v * 1.1:
        return 'rouge'
    return 'neutre'


def main():
    seuil = 1.01
    if '--seuil' in sys.argv:
        seuil = float(sys.argv[sys.argv.index('--seuil') + 1])
    lignes = []
    for nomjeu, dossier in JEUX:
        lp = os.path.join(DEC, dossier, 'light_param')
        if not os.path.isdir(lp):
            continue
        for f in sorted(os.listdir(lp)):
            if not f.startswith('fog_'):
                continue
            code = f[4:-4]
            fog = trio(open(os.path.join(lp, f), encoding='utf-8',
                            errors='replace').read(), 'color')
            if fog is None:
                continue
            lf = os.path.join(lp, 'light_%s.txt' % code)
            dif = None
            if os.path.exists(lf):
                t = open(lf, encoding='utf-8', errors='replace').read()
                d = re.findall(r'diffuse ([\d.eE+\-]+) ([\d.eE+\-]+) '
                               r'([\d.eE+\-]+)', t)
                if len(d) > 2:
                    dif = tuple(float(x) for x in d[2])
            clair = max(fog)
            if clair > seuil:
                continue
            lignes.append((clair, nomjeu, code, fog, dif))
    lignes.sort()
    print('%-11s %-7s %-26s %-8s %s'
          % ('jeu', 'decor', 'brouillard (fond)', 'teinte', 'diffuse 3'))
    for clair, nomjeu, code, fog, dif in lignes:
        print('%-11s %-7s %-26s %-8s %s'
              % (nomjeu, code,
                 '%.3f %.3f %.3f' % fog, teinte(fog),
                 ('%.3f %.3f %.3f' % dif) if dif else '-'))
    print('== %d decor(s)' % len(lignes))
    return 0


if __name__ == '__main__':
    sys.exit(main())
