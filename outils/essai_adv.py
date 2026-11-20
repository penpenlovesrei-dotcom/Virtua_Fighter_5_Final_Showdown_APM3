#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES ECRANS DE DEMARRAGE, PHOTOGRAPHIES SECONDE PAR SECONDE.

Pourquoi cet outil (2026-10-12). La question des planches 4K se tranche sur
`aet_n_adv` -- les logos ATTENTION, SEGA, AM2, CRI, RATING, qui defilent dans
les vingt premieres secondes et qu'aucun scenario d'entrees n'atteint. Il faut
donc photographier CES secondes-la, et pouvoir comparer deux lancements image
par image.

ON NE POSE AUCUN SCENARIO : `apm_entrees.txt` est laisse tel quel, et personne
n'appuie sur START -- sans quoi les logos seraient sautes, ce qui est
precisement leur raison d'etre ici.

    py -3 tools/essai_adv.py <etiquette> [premiere] [derniere]

Les captures vont dans `analysis/adv_<etiquette>_tNN.png`.
"""
import os
import subprocess
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
OUT = os.path.join(RACINE, 'analysis')
CAP = os.path.join(ICI, 'capture_fenetre.py')


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    etiquette = a[0]
    deb = int(a[1]) if len(a) > 1 else 2
    fin = int(a[2]) if len(a) > 2 else 20

    subprocess.run(['taskkill', '/f', '/im', 'vfes.exe'], capture_output=True)
    time.sleep(1)
    p = subprocess.Popen([os.path.join(JEU, 'vfes.exe')], cwd=JEU)
    print('vfes.exe lance ; captures de %d a %d s' % (deb, fin))
    images = []
    t0 = time.time()
    try:
        for t in range(deb, fin + 1):
            while time.time() - t0 < t:
                time.sleep(0.1)
            if p.poll() is not None:
                print('%2ds  LE JEU S EST FERME (code %s)' % (t, p.returncode))
                break
            c = os.path.join(OUT, 'adv_%s_t%02d.png' % (etiquette, t))
            subprocess.run([sys.executable, CAP, c], capture_output=True)
            images.append((t, c))
    finally:
        if p.poll() is None:
            p.terminate()

    try:
        from PIL import Image
    except ImportError:
        for t, c in images:
            print('  %2ds  %s' % (t, c))
        return 0
    for t, c in images:
        if not os.path.exists(c):
            print('  %2ds  pas de capture' % t)
            continue
        im = Image.open(c).convert('L')
        px = list(im.getdata())
        clairs = sum(1 for v in px if v > 24) * 100.0 / len(px)
        print('  %2ds  %5.1f %% de pixels non noirs   %s'
              % (t, clairs, os.path.basename(c)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
