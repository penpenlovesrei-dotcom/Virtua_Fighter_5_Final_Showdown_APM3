#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L'ARBRE D'UNE COMPOSITION AET : tous ses elements, et OU ils sont.

POURQUOI CET OUTIL (2026-10-20). Frederic, apres quatre passes a poser un
element a la fois et a le chercher a l'ecran : « tu as toutes les donnees
pour positionner tous les elements de l'interface, alors que tu vois bien
que rien n'est en place sur tes captures ». Il a raison, et c'etait un
defaut de METHODE :

  `aet.py` ne montre que la composition RACINE et ses calques. Or une
  fenetre comme `player_info_win_1p` EST une composition : elle contient
  son cadre, son portrait, ses pavés et ses emplacements de texte, chacun
  avec sa position, deja en place. Il n'y a rien a chercher a l'ecran --
  tout est dans la planche.

CE QU'IL REND. Pour chaque calque, en descendant :

    nom, type, creneau de trames, position PROPRE, origine, echelle,
    opacite, et pour un calque d'image la taille de la surface et le
    nom du sprite.

Et la POSITION ABSOLUE, cumulee de parent en enfant.

LA REGLE DE CUMUL, ET SON TEMOIN. Un calque de type composition dessine
son contenu dans son propre repere : le contenu est translate de
(position - origine) du calque qui le porte. On cumule donc

    absolu(enfant) = absolu(parent) - origine(parent) + position(enfant)

Le temoin qui la verifie est `dan_icon1p_e` : le §34 l'a trouve par
BALAYAGE a l'ecran, a (588, 476) dans `aet_c_cmn`. Si l'arbre rend la
meme valeur sans toucher au jeu, la regle tient.

    py -3 tools/arbre_aet.py aet_n_qwin player_info_win_1p
    py -3 tools/arbre_aet.py aet_n_qwin --racine      les compositions racine
    py -3 tools/arbre_aet.py aet_c_cmn dan_icon1p_e
    py -3 tools/arbre_aet.py aet_n_qwin player_info_win_1p --2007
    py -3 tools/arbre_aet.py <chemin complet.bin> <compo>

Sans --2007 on lit la planche POSEE (runtime/.../rom/2d) -- celle que le
jeu sert, donc celle qui compte pour nos positions.
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
from aet import Aet, TYPES, _val          # noqa: E402

POSE = os.path.join(os.path.dirname(ICI), 'runtime', 'media', 'vf5fs',
                    'vf5fs_media', 'rom', '2d')
MEDIA2007 = r'C:\Users\frede\Desktop\VF5 FS DECOMP\X360_VF5\media\rom\2d'


def cst(p):
    """La valeur d'une propriete quand elle est CONSTANTE, sinon None.

    Une propriete animee n'a pas « une » position : on rend None plutot
    que de choisir une trame en douce.
    """
    if p is None:
        return None
    return p['valeur']


def surfaces_par_offset(a, sc):
    return {s['offset']: s for s in a.surfaces(sc)}


def compo_du_calque(a, c):
    """Le couple (nombre, pointeur) de la composition que porte un calque
    de type 3. L'`element` designe l'entree de la table des compositions."""
    e = c['element']
    if not a.tient(e, 8):
        return None
    return a.u32(e), a.u32(e + 4)


def descendre(a, sc, surf, n, ptr, ax, ay, prof, vus, large):
    for c in a.calques(n, ptr):
        t = a.transforme(c['video'])
        px = py = ox = oy = None
        if t:
            px, py = cst(t['Position.X']), cst(t['Position.Y'])
            ox, oy = cst(t['Origine.X']), cst(t['Origine.Y'])
        bx = ax + (px or 0.0)
        by = ay + (py or 0.0)
        marge = '  ' * prof
        detail = ''
        if t:
            detail = ('pos (%s, %s)  orig (%s, %s)  ech (%s, %s)  op %s'
                      % (_val(t['Position.X']), _val(t['Position.Y']),
                         _val(t['Origine.X']), _val(t['Origine.Y']),
                         _val(t['Echelle.X']), _val(t['Echelle.Y']),
                         _val(t['Opacite'])))
        img = ''
        if c['type'] == 1:
            s = surf.get(c['element'])
            if s:
                noms = ', '.join(x for x, _ in s['sources']) or '(sans source)'
                img = '   [%d x %d  %s]' % (s['largeur'], s['hauteur'], noms)
        print('%s%-*s %-12s %5.0f-%-5.0f  ABS (%7.1f, %7.1f)%s'
              % (marge, max(4, large - 2 * prof), c['nom'],
                 TYPES.get(c['type'], '?%d' % c['type']),
                 c['debut'], c['fin'], bx, by, img))
        if detail:
            print('%s      %s' % (marge, detail))
        if c['type'] != 3:
            continue
        sous = compo_du_calque(a, c)
        if sous is None:
            print('%s      (composition hors bornes)' % marge)
            continue
        if sous[1] in vus:
            print('%s      (deja depliee -- recursion arretee)' % marge)
            continue
        vus.add(sous[1])
        descendre(a, sc, surf, sous[0], sous[1],
                  bx - (ox or 0.0), by - (oy or 0.0), prof + 1, vus, large)
        vus.discard(sous[1])


def main():
    av = list(sys.argv[1:])
    a2007 = '--2007' in av
    if a2007:
        av.remove('--2007')
    if not av:
        print(__doc__)
        return 1
    nom = av[0]
    chemin = nom
    if not os.path.exists(chemin):
        base = MEDIA2007 if a2007 else POSE
        chemin = os.path.join(base, nom if nom.endswith('.bin')
                              else nom + '.bin')
    if not os.path.exists(chemin):
        print('planche introuvable : %s' % chemin)
        return 2
    cible = av[1] if len(av) > 1 else '--racine'
    a = Aet(chemin)
    print('planche %s' % chemin)
    for p in a.scenes():
        if not a.tient(p, 0x38):
            continue
        sc = a.scene(p)
        compos = a.compositions(sc)
        if not compos:
            continue
        print('scene "%s"  %dx%d  %d composition(s)'
              % (sc['nom'], sc['resolution'][0], sc['resolution'][1],
                 len(compos)))
        surf = surfaces_par_offset(a, sc)
        n, ptr = compos[-1]                      # la RACINE est la derniere
        racines = a.calques(n, ptr)
        if cible == '--racine':
            for c in racines:
                t = a.transforme(c['video'])
                print('   %-36s %-12s  pos (%s, %s)  orig (%s, %s)'
                      % (c['nom'], TYPES.get(c['type'], '?'),
                         _val(t['Position.X']) if t else '?',
                         _val(t['Position.Y']) if t else '?',
                         _val(t['Origine.X']) if t else '?',
                         _val(t['Origine.Y']) if t else '?'))
            continue
        vise = [c for c in racines if c['nom'] == cible]
        if not vise:
            vise = [c for c in racines if cible.lower() in c['nom'].lower()]
        if not vise:
            print('   « %s » n est PAS un calque de la composition racine.'
                  % cible)
            print('   (le moteur, 0x180171E90, ne cherche que la -- §31)')
            continue
        for c in vise:
            t = a.transforme(c['video'])
            px = cst(t['Position.X']) if t else 0.0
            py = cst(t['Position.Y']) if t else 0.0
            ox = cst(t['Origine.X']) if t else 0.0
            oy = cst(t['Origine.Y']) if t else 0.0
            print('')
            print('   %s  %s  %.0f-%.0f  pos (%s, %s)  orig (%s, %s)'
                  % (c['nom'], TYPES.get(c['type'], '?'),
                     c['debut'], c['fin'],
                     _val(t['Position.X']) if t else '?',
                     _val(t['Position.Y']) if t else '?',
                     _val(t['Origine.X']) if t else '?',
                     _val(t['Origine.Y']) if t else '?'))
            print('   %s' % ('-' * 72))
            if c['type'] != 3:
                continue
            sous = compo_du_calque(a, c)
            if sous is None:
                print('   (composition hors bornes)')
                continue
            descendre(a, sc, surf, sous[0], sous[1],
                      (px or 0.0) - (ox or 0.0), (py or 0.0) - (oy or 0.0),
                      1, {sous[1]}, 40)
    return 0


if __name__ == '__main__':
    sys.exit(main())
