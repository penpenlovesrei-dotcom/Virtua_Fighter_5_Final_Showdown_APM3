#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""LE CATALOGUE DES CADRES DU MOTEUR : la table des rangs, et leur geometrie.

Toute fenetre du jeu est un RANG dans la table `0x18052E680`. Un rang y vaut
trois mots de huit octets :

    +0x00  u32  la PLANCHE (le set AET : 671 a 682)
    +0x08  ptr  le nom de la composition
    +0x10  i32  le nombre de bandes de contenu, ou -1

`0x1801BE520(fen, phase)` lit ce rang depuis `[fen+4]`, en tire la planche et
le nom, et demande l'objet a `0x180029a90`. Ouvrir une fenetre, c'est donc
choisir un numero -- **le cadre, son fond et ses ancres sont deja dessines**.

La geometrie se lit ensuite dans la planche. Chaque composition porte les
memes ancres nommees :

    p_win_edg_lt / p_win_edg_rb    les deux coins du CADRE
    p_txt_01_lt  / p_txt_02_rb     les deux coins de l'INTERIEUR
    p_txt_03_rt                    le coin haut-droit, quand il existe
    winbase_N / cwbase_N           la composition qui EST le fond

C'est ce que `0x1801BCD70(fen, &vec3, nom, c, 0)` resout a l'execution, deja
mis a l'echelle de l'ecran : dessiner sur ces deux coins suffit a tenir
n'importe quelle resolution, sans compter un seul pixel.

    py -3 tools/cadres_fenetres.py                 la table entiere
    py -3 tools/cadres_fenetres.py choice_win_08   la geometrie d'un cadre
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aet import Aet                                       # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTEUR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                      'vf5fs-pxd-w64-Retail_APM3.dll.origine')
DEUXD = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media',
                     'rom', '2d')
TABLE = 0x18052E680
PAS = 24
ANCRES = ('p_win_edg_lt', 'p_win_edg_rb', 'p_txt_01_lt', 'p_txt_02_rb',
          'p_txt_03_rt')

# LES PLANCHES. Le numero de set ne se lit nulle part en clair ; on l'etablit
# par le CONTENU -- chaque rang nomme une composition, et une seule planche la
# porte. Les quatre ci-dessous sont celles que les rangs emploient.
PLANCHES = ('aet_n_cmn.bin', 'aet_n_main.bin', 'aet_n_term.bin',
            'aet_n_adv.bin', 'aet_n_match.bin', 'aet_n_info.bin',
            'aet_n_dojo.bin', 'aet_n_clg.bin', 'aet_n_buy.bin',
            'aet_n_tnt.bin', 'aet_n_que.bin', 'aet_n_qwin.bin')


class Pe(object):
    """Juste assez de PE pour lire une VA."""

    def __init__(self, chemin):
        import pefile
        pe = pefile.PE(chemin, fast_load=True)
        self.base = pe.OPTIONAL_HEADER.ImageBase
        self.secs = [(self.base + s.VirtualAddress, s.Misc_VirtualSize,
                      s.PointerToRawData) for s in pe.sections]
        with open(chemin, 'rb') as fp:
            self.d = fp.read()

    def off(self, va):
        for v, vs, o in self.secs:
            if v <= va < v + vs:
                return o + (va - v)
        return None

    def chaine(self, va):
        o = self.off(va)
        if o is None:
            return None
        return self.d[o:self.d.index(b'\0', o)].decode('latin-1')


def rangs(pe):
    """[(rang, planche, nom, bandes)], jusqu'au premier nom illisible."""
    o = pe.off(TABLE)
    out = []
    i = 0
    while True:
        if o + (i + 1) * PAS > len(pe.d):
            break
        set_id, _, nom_va = struct.unpack_from('<IIQ', pe.d, o + i * PAS)
        bandes = struct.unpack_from('<i', pe.d, o + i * PAS + 0x10)[0]
        nom = pe.chaine(nom_va) if nom_va else None
        if not nom or not nom.isprintable():
            break
        out.append((i, set_id, nom, bandes))
        i += 1
    return out


def _valeur(p):
    if p is None:
        return None
    if p['valeur'] is not None:
        return p['valeur']
    return p['cles'][0][1] if p['cles'] else None


def geometrie(nom):
    """Les ancres de la composition `nom`, dans la planche qui la porte."""
    for f in PLANCHES:
        ch = os.path.join(DEUXD, f)
        if not os.path.exists(ch):
            continue
        a = Aet(ch)
        for p in a.scenes():
            sc = a.scene(p)
            compos = a.compositions(sc)
            if not compos:
                continue
            n, q = compos[-1]
            for c in a.calques(n, q):
                if c['nom'] != nom or c['type'] != 3:
                    continue
                n2, q2 = a.u32(c['element']), a.u32(c['element'] + 4)
                d = {}
                fond = []
                for e in a.calques(n2, q2):
                    if e['type'] == 3:
                        fond.append(e['nom'])
                    if e['nom'] in ANCRES and e['nom'] not in d:
                        t = a.transforme(a.u32(e['offset'] + 0x28))
                        if t:
                            d[e['nom']] = (_valeur(t['Position.X']),
                                           _valeur(t['Position.Y']))
                return f, sc, d, fond
    return None


def main():
    pe = Pe(MOTEUR)
    voulus = sys.argv[1:]
    if not voulus:
        print('rang  set   bandes  nom')
        for i, s, nom, b in rangs(pe):
            print('0x%02X  %-5d %-6s  %s'
                  % (i, s, '-' if b < 0 else b, nom))
        print()
        print('Un nom en argument en donne la geometrie.')
        return 0
    par_nom = {}
    for i, s, nom, b in rangs(pe):
        par_nom.setdefault(nom, (i, s, b))
    for nom in voulus:
        if nom in par_nom:
            i, s, b = par_nom[nom]
            print('%s -- rang 0x%02X, set %d, %s bande(s)'
                  % (nom, i, s, '-' if b < 0 else b))
        else:
            print('%s -- absent de la table des rangs' % nom)
        g = geometrie(nom)
        if not g:
            print('   composition introuvable dans les planches')
            continue
        f, sc, d, fond = g
        print('   planche %s, scene %s, reference %d x %d'
              % (f, sc['nom'], sc['resolution'][0], sc['resolution'][1]))
        for k in ANCRES:
            v = d.get(k)
            if v and None not in v:
                print('   %-14s %7.1f , %7.1f' % (k, v[0], v[1]))
        lt, rb = d.get('p_win_edg_lt'), d.get('p_win_edg_rb')
        if lt and rb and None not in lt and None not in rb:
            print('   CADRE        %7.0f x %7.0f'
                  % (rb[0] - lt[0], rb[1] - lt[1]))
        lt, rb = d.get('p_txt_01_lt'), d.get('p_txt_02_rb')
        if lt and rb and None not in lt and None not in rb:
            print('   INTERIEUR    %7.0f x %7.0f'
                  % (rb[0] - lt[0], rb[1] - lt[1]))
        if fond:
            print('   fond         %s' % ', '.join(fond))
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
