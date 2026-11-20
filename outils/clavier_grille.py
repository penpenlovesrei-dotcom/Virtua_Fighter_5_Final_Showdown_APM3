# -*- coding: utf-8 -*-
r"""La grille du C PRODUIT : compte des cases, couverture, doublons.

PIEGE PAYE DEUX FOIS LE 2026-10-15 : la grille CONTIENT un point-virgule (la
ponctuation `():;+&`). Chercher la fin de la declaration sur le premier `;`
coupait donc le dernier litteral en deux, et ce controle annoncait 60 cases
sur 80 alors que le C en portait bien 80. Un controle qui ment est pire que
pas de controle.

On delimite donc sur la GUILLEMET-point-virgule, et on rend la guillemet
fermante au dernier litteral -- sinon la recherche des litterals la laisse
tomber, et on retombe sur le meme mensonge.
"""
import re

C = r'C:\Users\frede\Desktop\VF5RE\tools\apm_stub.c'
s = open(C, encoding='latin-1').read()

col = int(re.search(r'#define CLV_COL (\d+)', s).group(1))
ran = int(re.search(r'#define CLV_RAN (\d+)', s).group(1))

m = re.search(r'g_clv_grille\[CLV_CASES \+ 1\] =(.*?)";', s, re.S)
corps = m.group(1) + '"'          # la guillemet fermante, rendue
morceaux = re.findall(r'"((?:[^"\\]|\\.)*)"', corps)
cases = ''
for p in morceaux:
    cases += re.sub(r'\\x([0-9a-fA-F]{2})',
                    lambda g: chr(int(g.group(1), 16)), p)

attendu = col * ran
print('CLV_COL x CLV_RAN = %d x %d = %d cases attendues' % (col, ran, attendu))
print('cases ecrites     : %d   %s'
      % (len(cases), 'OK' if len(cases) == attendu else '<-- ECART'))
print()
print('majuscules : %2d / 26' % sum(1 for c in cases if 'A' <= c <= 'Z'))
print('minuscules : %2d / 26' % sum(1 for c in cases if 'a' <= c <= 'z'))
print('chiffres   : %2d / 10' % sum(1 for c in cases if '0' <= c <= '9'))
print('commandes  : %2d / 4 ' % sum(1 for c in cases if ord(c) < 5))
print('ponctuation: %2d' % sum(1 for c in cases
                               if ord(c) > 4 and not c.isalnum()))
doublons = sorted({c for c in cases if cases.count(c) > 1})
print()
print('doublons   : %s' % (
    ', '.join('%r' % c for c in doublons) if doublons else 'aucun'))
manquants = [c for c in
             'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
             if c not in cases]
print('manquants  : %s' % (''.join(manquants) if manquants else 'aucun'))
print()
print('la grille, rangee par rangee :')
for r in range(ran):
    ligne = cases[r * col:(r + 1) * col]
    lisible = ''.join({1: '_', 2: '<', 3: '#', 4: '*'}.get(ord(c), c)
                      for c in ligne)
    print('   %s' % ' '.join(lisible))
print()
print('%d signes par rangee (3 par case) -- il en tient 73' % (col * 3))
print('commandes 2D par trame : %d  (63 avaient suffi a tout casser)'
      % ((1 + ran + 1) * 2))
