#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Sortir en PNG les APERCUS et les VIGNETTES de l'ecran de selection de
decor des trois generations : Final Showdown (APM3), VF5 R et VF5 ver.B.

POURQUOI. Le chantier ajoute les decors de VF5 R et de VF5 ver.B comme des
decors A PART ENTIERE (`variantes_5r.py`, `variantes_vf5.py`), atteints par
l'anneau de la barre espace. Mais l'ecran ne montre qu'un seul aperçu par
case : « les cinq decors de Dural partagent la meme planche AET (dur /
dur_stay), et c'est de l'art peint » (`tools/variantes.cmd`). Pour que
l'aperçu suive la generation choisie, il faut d'abord AVOIR les images des
deux autres generations. Cet outil les sort.

LA CHAINE, mesuree et non supposee (voir `analysis/apercus_decors_par_version.md`)

    rom/2d/spr_s_selstg.farc   FArC, une entree
      -> spr_s_selstg.bin      jeu de sprites PXD
         en-tete  +0x04 offset du TXP   +0x08 nb textures  +0x0C nb sprites
                  +0x10 table des sprites (0x28 par sprite)
                  +0x14 noms de textures  +0x18 noms de sprites
         sprite   +0x00 index de texture  +0x08 u0,v0,u1,v1
                  +0x18 x, y, largeur, hauteur EN PIXELS
      -> bloc TXP, lu par `tools/txp.py`, deja ecrit

LES NOMS, et ils CHANGENT d'une generation a l'autre

    FS / APM3   REND_STAGE_<PERSO>    1024x500   grand aperçu
                ICON_STAGE_<PERSO>     140x52    vignette
    VF5 R       REND_STAGE_<PERSO>    1024x500
                ICON_STAGE_<PERSO>     140x54
    VF5 ver.B   GRAPH_L_<DECOR>01     1024x768   grand aperçu, PIECE GAUCHE
                GRAPH_L_<DECOR>02      256x768   grand aperçu, PIECE DROITE
                GRAPH_S_<DECOR>        114x110   vignette (carree, pas un
                                                 rectangle : la disposition de
                                                 2007 n'est pas celle de FS)

FS et R nomment par PERSONNAGE, ver.B par DECOR. La correspondance n'est pas
devinee : elle est lue dans les MARQUEURS du calque `stage_graph_l_base` de la
composition racine de `aet_s_selstg.bin`, dont les noms sont exactement les
codes a trois lettres de la table des 41 decors, et dans l'ordre des calques
de la composition qu'il pointe.

    py -3 outils/apercus_decors.py
    py -3 outils/apercus_decors.py --sortie "C:\...\VF5RE\APERCUS_DECORS"
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
ATELIER = os.path.join(os.path.dirname(RACINE), 'VF5RE')
SORTIE = os.path.join(ATELIER, 'APERCUS_DECORS')

import txp                                                     # noqa: E402

# Le code a trois lettres du decor -> le code du personnage sous lequel FS et
# VF5 R rangent son aperçu. MESURE : marqueur de `stage_graph_l_base` ->
# instant -> calque de la composition pointee -> sprite du calque.
DECOR_VERS_PERSO = {
    'ban': 'lau', 'ter': 'kag', 'nyc': 'jak', 'cas': 'lio', 'riv': 'shu',
    'jin': 'aoi', 'sin': 'lei', 'djo': 'aki', 'umi': 'jef', 'hai': 'goh',
    'are': 'msk', 'slk': 'mon', 'yuk': 'wol', 'tak': 'van', 'aur': 'sar',
    'bar': 'bra', 'tan': 'pai', 'dur': 'dur', 'gym': 'krt', 'smo': 'tak',
    'rnd': 'rnd',
}

# Les trois jeux de sprites. `racine` vaut None quand le fichier est deja
# depaquete a cote de la note.
GENERATIONS = (
    ('VF5FS', 'apm3'),
    ('VF5R', 'vf5r'),
    ('VF5', 'verb'),
)


# ------------------------------------------------------------ jeu de sprites
def chaine(d, o):
    return d[o:d.index(b'\0', o)].decode('latin-1')


def jeu_de_sprites(d):
    """{textures: [...], sprites: [{nom, tex, x, y, w, h}]}"""
    _, _ofs_txp, ntex, nspr, ofs_spr, a14, a18, _a1c = \
        struct.unpack_from('<8I', d, 0)
    noms_tex = [chaine(d, o) for o in
                struct.unpack_from('<%dI' % ntex, d, a14)]
    noms_spr = [chaine(d, o) for o in
                struct.unpack_from('<%dI' % nspr, d, a18)]
    sprites = []
    for i in range(nspr):
        o = ofs_spr + i * 0x28
        tex = struct.unpack_from('<i', d, o)[0]
        x, y, w, h = struct.unpack_from('<4f', d, o + 0x18)
        sprites.append(dict(nom=noms_spr[i], tex=tex, x=int(x), y=int(y),
                            w=int(w), h=int(h)))
    return dict(noms_tex=noms_tex, sprites=sprites, textures=txp.textures(d))


def planches(jeu):
    """Les planches decodees, a la demande : {index: Image}."""
    cache = {}

    def prendre(i):
        if i not in cache:
            cache[i] = txp.image(jeu['textures'][i])
        return cache[i]
    return prendre


def decouper(jeu, prendre, nom):
    s = [x for x in jeu['sprites'] if x['nom'] == nom]
    if not s:
        return None
    s = s[0]
    im = prendre(s['tex'])
    return im.crop((s['x'], s['y'], s['x'] + s['w'], s['y'] + s['h']))


# ------------------------------------------------------------------- sortie
def lire_source(chemin):
    """Le `spr_s_selstg.bin`, qu'on parte du `.farc` ou du `.bin` deja sorti."""
    if chemin.endswith('.farc'):
        contenu = txp.defarc(chemin)
        return list(contenu.values())[0]
    return open(chemin, 'rb').read()


def sortir(chemin_bin, generation, dossier):
    """Rend (apercus, vignettes, manques) pour une generation."""
    from PIL import Image
    d = lire_source(chemin_bin)
    jeu = jeu_de_sprites(d)
    prendre = planches(jeu)
    os.makedirs(dossier, exist_ok=True)
    apercus, vignettes, manques = {}, {}, []
    for code, perso in sorted(DECOR_VERS_PERSO.items()):
        if generation == 'VF5':
            g = code.upper()
            a1 = decouper(jeu, prendre, 'GRAPH_L_%s01' % g)
            a2 = decouper(jeu, prendre, 'GRAPH_L_%s02' % g)
            if a1 is not None and a2 is not None:
                im = Image.new('RGBA', (a1.width + a2.width,
                                        max(a1.height, a2.height)))
                im.paste(a1, (0, 0))
                im.paste(a2, (a1.width, 0))
                ap = im
            else:
                ap = a1 or a2
            vg = decouper(jeu, prendre, 'GRAPH_S_%s' % g)
        else:
            p = perso.upper()
            ap = decouper(jeu, prendre, 'REND_STAGE_%s' % p)
            vg = decouper(jeu, prendre, 'ICON_STAGE_%s' % p)
        if ap is not None:
            f = os.path.join(dossier, 'apercu_%s.png' % code)
            ap.save(f)
            apercus[code] = (ap.width, ap.height)
        else:
            manques.append('apercu_%s' % code)
        if vg is not None:
            f = os.path.join(dossier, 'vignette_%s.png' % code)
            vg.save(f)
            vignettes[code] = (vg.width, vg.height)
        else:
            manques.append('vignette_%s' % code)
    return apercus, vignettes, manques


def main():
    a = sys.argv[1:]
    base = SORTIE
    if '--sortie' in a:
        base = a[a.index('--sortie') + 1]
    src = os.path.join(base, '_SOURCE')
    sources = {
        'VF5FS': os.path.join(src, 'APM3_spr_s_selstg.farc'),
        'VF5R': os.path.join(src, 'VF5R_spr_s_selstg.farc'),
        'VF5': os.path.join(src, 'VF5_spr_s_selstg.farc'),
    }
    for gen, _ in GENERATIONS:
        chemin = sources[gen]
        if not os.path.exists(chemin):
            print('%-6s ABSENT : %s' % (gen, chemin))
            continue
        ap, vg, mq = sortir(chemin, gen, os.path.join(base, gen))
        tailles_a = sorted(set(ap.values()))
        tailles_v = sorted(set(vg.values()))
        print('%-6s %2d apercus %s, %2d vignettes %s'
              % (gen, len(ap), tailles_a, len(vg), tailles_v))
        if mq:
            print('       manquent : %s' % ', '.join(mq))
    return 0


if __name__ == '__main__':
    sys.exit(main())
