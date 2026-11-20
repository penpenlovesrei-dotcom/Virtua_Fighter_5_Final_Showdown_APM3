#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REMPLACER UNE TEXTURE DU JEU PAR UNE VERSION HD, depuis un simple PNG.

CE QUI REND L OPERATION POSSIBLE, et c est MESURE, pas suppose :

  1. **Les UV des sprites sont des flottants NORMALISES**, pas des pixels. Un
     enregistrement de sprite fait 0x28 octets dans le `spr_n_*.bin` --
     {indice de texture, rotation, u0, v0, u1, v1, x, y, largeur, hauteur} --
     et les quatre UV valent entre 0 et 1. Releve sur `spr_n_cmn.bin` :
     sprite 0, `uv=(0.64648,0.77734)-(0.92773,0.83984)`.
     **Donc agrandir une planche ne deplace aucun sprite** : la meme region
     normalisee porte simplement plus de texels. Rien a toucher dans
     `spr_db.bin`, rien dans la table des sprites.

  2. **Les archives 2D sont deja des fichiers LIBRES.** Les vingt noms
     `spr_n_*` et `aet_n_*` sont masques dans le `.par` (`.far_`, `.bi_`) :
     c est la copie de `rom/2d/` que le moteur charge. On ecrit donc la, et
     nulle part ailleurs.

  3. **Le jeu de textures (TXP) est en FIN de fichier.** L en-tete du jeu de
     sprites pointe la texture en `+0x04` ; dans `spr_n_cmn.bin` cela vaut
     0x3240 et le fichier s arrete apres. Faire grossir une texture ne
     deplace donc rien de ce qui la precede -- seuls les offsets INTERNES du
     TXP sont a recalculer, et cet outil les reconstruit tous.

LA SEULE CONTRAINTE : on remplace **une planche entiere**, pas un sprite. Les
UV etant normalisees, la DISPOSITION doit etre preservee -- une planche HD est
l ancienne agrandie (x2, x4), pas une planche reorganisee. Et les cotes
doivent rester multiples de 4 (le BC travaille par blocs de 4x4).

LES FORMATS. `RGBA8`, `RGB8` et `A8` s ecrivent tels quels. `DXT1` et `DXT5`
passent par `tools/bc.py`, l encodeur BC ecrit pour ce chantier. Le format
d origine est CONSERVE : une planche DXT5 reste DXT5 en HD, sans quoi le
fichier quadruplerait sans que le rendu y gagne.

LES NIVEAUX DE MIP sont REGENERES en nombre identique, par reduction de
moitie. Garder leur compte evite de toucher a ce que le moteur attend.

    py -3 tools/textures_hd.py --inventaire
    py -3 tools/textures_hd.py --sortir         les originaux en PNG
    py -3 tools/textures_hd.py --poser       les PNG de HD_TEXTURES/HD/2D
    py -3 tools/textures_hd.py --controle
    py -3 tools/textures_hd.py --retirer
"""
import io
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import bc                                                    # noqa: E402
import farc as mfarc                                          # noqa: E402
import txp                                                    # noqa: E402

DEUXD = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media',
                     'rom', '2d')
# L ARBORESCENCE, rangee le 2026-10-11 a la demande de Frederic : ce qui SORT
# du jeu et ce qui y RENTRE ne se melangent plus, et chaque famille a son
# dossier.
#
#   HD_TEXTURES/EXTRACTED/2D          les planches 2D sorties du jeu
#   HD_TEXTURES/EXTRACTED/STAGES      les textures de decor sorties
#   HD_TEXTURES/EXTRACTED/CHARACTERS  les textures de personnage sorties
#   HD_TEXTURES/HD/2D                 les versions HD a poser  <- cet outil
#   HD_TEXTURES/HD/STAGES             idem, decors             (textures_hd3d)
#   HD_TEXTURES/HD/CHARACTERS         idem, personnages        (textures_hd3d)
HD_RACINE = os.path.join(RACINE, 'HD_TEXTURES')
HD = os.path.join(HD_RACINE, 'HD', '2D')
ORIGINAUX = os.path.join(HD_RACINE, 'EXTRACTED', '2D')
NOMS_FORMAT = {0: 'A8', 1: 'RGB8', 2: 'RGBA8', 6: 'DXT1', 9: 'DXT5'}


# --------------------------------------------------------------- TXP ------
def lire_txp(d):
    """Rend (debut, [textures]), chaque texture etant la liste de ses niveaux.

    Un niveau : {'larg', 'haut', 'format', 'octets'}. On garde TOUS les
    niveaux, au contraire de `txp.py` qui ne lit que le zero : les reecrire
    demande de les connaitre.
    """
    i = d.find(b'TXP\x03')
    if i < 0:
        return None, []
    n, groupe = struct.unpack_from('<II', d, i + 4)
    offs = struct.unpack_from('<%dI' % n, d, i + 12)
    textures = []
    for o in offs:
        t = i + o
        nm, g2 = struct.unpack_from('<II', d, t + 4)
        so = struct.unpack_from('<%dI' % nm, d, t + 12)
        niveaux = []
        for j in so:
            s = t + j
            w, h, f, lvl, taille = struct.unpack_from('<5I', d, s + 4)
            niveaux.append({'larg': w, 'haut': h, 'format': f, 'niveau': lvl,
                            'octets': d[s + 0x18:s + 0x18 + taille]})
        textures.append({'groupe': g2, 'niveaux': niveaux})
    return (i, groupe), textures


def ecrire_txp(groupe, textures):
    """Reconstruit le bloc TXP entier : tous les offsets sont recalcules."""
    n = len(textures)
    tete = bytearray(b'TXP\x03' + struct.pack('<II', n, groupe))
    tete += b'\x00' * (4 * n)                     # les offsets, posés apres
    corps = bytearray()
    offsets = []
    for tex in textures:
        offsets.append(len(tete) + len(corps))
        nm = len(tex['niveaux'])
        bloc = bytearray(b'TXP\x04' + struct.pack('<II', nm, tex['groupe']))
        bloc += b'\x00' * (4 * nm)
        sous = bytearray()
        so = []
        for niv in tex['niveaux']:
            so.append(len(bloc) + len(sous))
            sous += b'TXP\x02' + struct.pack(
                '<5I', niv['larg'], niv['haut'], niv['format'],
                niv['niveau'], len(niv['octets']))
            sous += niv['octets']
        for k, v in enumerate(so):
            struct.pack_into('<I', bloc, 12 + 4 * k, v)
        corps += bloc + sous
    for k, v in enumerate(offsets):
        struct.pack_into('<I', tete, 12 + 4 * k, v)
    return bytes(tete) + bytes(corps)


def octets_du_niveau(im, format_txp):
    """L image, dans le format d origine. L ordre des lignes est celui du
    fichier -- `txp.py` retourne les planches compressees a la LECTURE, on les
    retourne donc avant d ECRIRE."""
    from PIL import Image
    # TOUTES les planches sont stockees de bas en haut : on retourne une fois,
    # ici, pour tous les formats. `txp.image` fait le chemin inverse.
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    if format_txp in (6, 9):
        return bc.encoder(im, format_txp)
    if format_txp == 2:
        return im.convert('RGBA').tobytes()
    if format_txp == 1:
        return im.convert('RGB').tobytes()
    if format_txp == 0:
        return im.convert('RGBA').split()[3].tobytes()
    if format_txp in (3, 5):
        import numpy as np
        a = np.asarray(im.convert('RGBA'), dtype=np.uint16)
        r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
        if format_txp == 3:                      # RGB5 : 565, sans alpha
            v = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
        else:                                    # RGBA4 : 4444
            v = ((al >> 4) << 12) | ((r >> 4) << 8) | ((g >> 4) << 4) | (b >> 4)
        return v.astype('<u2').tobytes()
    raise SystemExit('format %d non gere a l ecriture' % format_txp)


# ------------------------------------------------------------ sprites -----
# LA TABLE DES SPRITES, ET POURQUOI IL FAUT Y TOUCHER (2026-10-11)
#
# Constat de Frederic, a l ecran : « les images dimensionnees pour la 4K ne
# sont pas mises a l echelle en 1080p ». Elles n etaient pas mal mises a
# l echelle -- on n en voyait QU UN QUART, agrandi. Le logo SEGA ressemblait
# a un gros D bleu.
#
# LA CAUSE EST DANS LE SPRITE SET, pas dans la texture. Chaque sprite porte
# son rectangle DEUX FOIS :
#
#     +0x00  int   index de texture
#     +0x04  int   rotation
#     +0x08  float u1, v1, u2, v2      le rectangle NORMALISE  (0..1)
#     +0x18  float x, y, w, h          LE MEME, EN PIXELS
#
# et c est la seconde forme qui commande -- verifie sur `spr_n_adv` : pour
# ATTENTION_01, x=2 w=902 sur une texture de 1024 donnent exactement
# u1 = 2/1024 = 0.0020 et u2 = 904/1024 = 0.8828. En quadruplant la texture
# sans toucher aux pixels, 2 et 902 designent le quart superieur gauche.
#
# ON MULTIPLIE DONC x, y, w et h par le facteur d agrandissement, pour les
# seuls sprites qui visent la texture remplacee. Les u,v normalises, eux, ne
# bougent pas : ils etaient deja justes.
#
# L EN-TETE du sprite set, relevee sur `spr_n_adv.bin` et verifiee sur
# `spr_n_fnt32.bin` :
#     +0x04 offset du TXP   +0x08 nb textures   +0x0C nb sprites
#     +0x10 offset des sprites (pas de 0x28)
SPR_NSPR, SPR_OFS, SPR_PAS = 0x0C, 0x10, 0x28


def sprites_echelle(d, facteurs):
    """Rend `d` avec les rectangles PIXELS mis a l echelle.

    `facteurs` : {index de texture: facteur}. Les sprites qui visent une
    autre texture ne sont pas touches.
    """
    if not facteurs:
        return d
    n, = struct.unpack_from('<I', d, SPR_NSPR)
    ofs, = struct.unpack_from('<I', d, SPR_OFS)
    if ofs + SPR_PAS * n > len(d):
        print('   ! table des sprites hors bornes (%d sprites a 0x%X) -- '
              'les rectangles ne sont PAS mis a l echelle' % (n, ofs))
        return d
    b = bytearray(d)
    touches = 0
    for i in range(n):
        o = ofs + SPR_PAS * i
        tex, = struct.unpack_from('<i', b, o)
        f = facteurs.get(tex)
        if not f or f == 1:
            continue
        for j in range(4):                      # x, y, w, h
            p = o + 0x18 + 4 * j
            v, = struct.unpack_from('<f', b, p)
            struct.pack_into('<f', b, p, v * f)
        touches += 1
    if touches:
        print('   %d sprite(s) mis a l echelle' % touches)
    return bytes(b)


# ----------------------------------------------------------- archives -----
def archives():
    if not os.path.isdir(DEUXD):
        raise SystemExit('%s manque' % DEUXD)
    return sorted(n for n in os.listdir(DEUXD)
                  if n.endswith('.farc') and n.startswith('spr_'))


def contenu(nom):
    chemin = os.path.join(DEUXD, nom)
    return chemin, mfarc.Farc(chemin)


def membres(chemin):
    # `Farc.read` prend l ENTREE, pas le nom -- la lire au nom rend un
    # TypeError muet sur `entry["offset"]`.
    f = mfarc.Farc(chemin)
    return dict((e['name'], f.read(e)) for e in f.entries)


# ------------------------------------------------------------ actions -----
def inventaire(sortir=False):
    from PIL import Image
    os.makedirs(ORIGINAUX, exist_ok=True) if sortir else None
    total = 0
    for nom in archives():
        chemin = os.path.join(DEUXD, nom)
        m = membres(chemin)
        for fich, d in m.items():
            if not fich.endswith('.bin'):
                continue
            _tete, textures = lire_txp(d)
            if not textures:
                continue
            base = nom[:-5]
            print('%s  (%d texture(s))' % (nom, len(textures)))
            for k, tex in enumerate(textures):
                n0 = tex['niveaux'][0]
                f = n0['format']
                etiquette = '%s__tex%02d.png' % (base, k)
                print('   %-24s %-6s %5dx%-5d %d niveau(x)'
                      % (etiquette, NOMS_FORMAT.get(f, '?%d' % f),
                         n0['larg'], n0['haut'], len(tex['niveaux'])))
                total += 1
                if sortir:
                    # UNE TEXTURE QUI NE SE DECODE PAS NE DOIT PAS ARRETER LES
                    # CENT SOIXANTE-DIX AUTRES. Le premier jet le faisait : un
                    # `format 3 inconnu` a coupe l export a la 120e, et le
                    # journal du fond ne le disait qu a sa derniere ligne.
                    try:
                        im = txp.image({'larg': n0['larg'], 'haut': n0['haut'],
                                        'format': f, 'octets': n0['octets']})
                        im.save(os.path.join(ORIGINAUX, etiquette))
                    except Exception as ex:               # noqa: BLE001
                        print('      NON SORTIE : %s' % ex)
    print()
    print('%d texture(s) remplacables.' % total)
    if sortir:
        print('Originaux en PNG : %s' % ORIGINAUX)
    return 0


def _mips(im, format_txp, combien, anciens=None):
    """La chaine de mips, AUX MEMES DIMENSIONS DECLAREES que l originale.

    PIEGE MESURE (2026-10-11) : les deux derniers niveaux d une texture du jeu
    sont declares **2x2 et 1x1**, pour huit octets chacun -- un bloc BC complet,
    puisqu un bloc couvre 4x4 quoi qu il arrive. Ecreter la DECLARATION a 4x4,
    comme le faisait le premier jet, donne le bon nombre d octets mais la
    mauvaise taille : le moteur echantillonnerait ce niveau comme s il faisait
    quatre texels de cote. On declare donc `w >> j` (plancher 1) et on encode
    une image de `max(4, w >> j)`.
    """
    from PIL import Image
    w, h = im.size
    # UNE CHAINE COMPLETE LE RESTE. L originale de `stgnyc` descend jusqu a
    # 1x1 : c est une chaine COMPLETE, et en garder seulement le nombre de
    # niveaux apres un agrandissement l arreterait a 2x2. On regarde donc le
    # DERNIER niveau d origine, et s il valait 1x1 on va jusqu a 1x1.
    if anciens and anciens[-1]['larg'] <= 1 and anciens[-1]['haut'] <= 1:
        combien = max(w, h).bit_length()
    out = []
    for j in range(combien):
        dw, dh = max(1, w >> j), max(1, h >> j)
        ew, eh = max(4, dw), max(4, dh)
        src = im if j == 0 else im.resize((ew, eh), Image.LANCZOS)
        out.append({'larg': dw, 'haut': dh, 'format': format_txp,
                    'niveau': j, 'octets': octets_du_niveau(src, format_txp)})
    return out


def _png_demandes():
    """Les PNG poses dans HD_TEXTURES/HD/2D : {(archive, k): chemin}."""
    out = {}
    # UN PNG POSE A L ANCIEN ENDROIT NE DOIT PAS ETRE IGNORE EN SILENCE.
    # L arborescence a change le 2026-10-11 ; un fichier reste a la racine de
    # HD_TEXTURES ne serait plus vu, et l outil dirait seulement " aucun PNG ".
    perdus = [n for n in sorted(os.listdir(HD_RACINE))
              if n.lower().endswith('.png')] if os.path.isdir(HD_RACINE) else []
    for n in perdus:
        print('   A DEPLACER : %s est a la racine de HD_TEXTURES ;'
              ' les PNG 2D vont dans HD%s2D.' % (n, chr(92)))
    if not os.path.isdir(HD):
        return out
    for n in sorted(os.listdir(HD)):
        if not n.lower().endswith('.png') or '__tex' not in n:
            continue
        base, reste = n.rsplit('__tex', 1)
        try:
            k = int(reste.split('.')[0])
        except ValueError:
            print('   nom illisible, ignore : %s' % n)
            continue
        out[(base + '.farc', k)] = os.path.join(HD, n)
    return out


def poser(controle=False):
    from PIL import Image
    demandes = _png_demandes()
    if not demandes:
        print('Aucun PNG dans %s' % HD)
        print('Le nom doit etre <archive>__texNN.png, par exemple '
              'spr_n_cmn__tex04.png.')
        print('Lancez --sortir pour avoir les originaux et leurs noms.')
        return 1
    par_archive = {}
    for (arc, k), png in demandes.items():
        par_archive.setdefault(arc, []).append((k, png))

    for arc, liste in sorted(par_archive.items()):
        chemin = os.path.join(DEUXD, arc)
        if not os.path.exists(chemin):
            print('%s : archive inconnue' % arc)
            continue
        origine = chemin + '.origine'
        source = origine if os.path.exists(origine) else chemin
        m = membres(source)
        change = False
        facteurs = {}
        for fich in list(m):
            if not fich.endswith('.bin'):
                continue
            d = m[fich]
            tete, textures = lire_txp(d)
            if not textures:
                continue
            for k, png in sorted(liste):
                if k >= len(textures):
                    print('   %s : la texture %d n existe pas (%d en tout)'
                          % (arc, k, len(textures)))
                    continue
                tex = textures[k]
                f = tex['niveaux'][0]['format']
                aw, ah = tex['niveaux'][0]['larg'], tex['niveaux'][0]['haut']
                im = Image.open(png).convert('RGBA')
                w, h = im.size
                if w % 4 or h % 4:
                    print('   %s : %dx%d -- les cotes doivent etre multiples '
                          'de 4' % (os.path.basename(png), w, h))
                    continue
                facteur = '%gx' % (w / float(aw)) if aw else '?'
                print('   %-24s %s %dx%d -> %dx%d (%s)'
                      % (os.path.basename(png), NOMS_FORMAT.get(f, f),
                         aw, ah, w, h, facteur))
                if controle:
                    continue
                tex['niveaux'] = _mips(im, f, len(tex['niveaux']),
                                        tex['niveaux'])
                if aw and ah and (w != aw or h != ah):
                    facteurs[k] = w / float(aw)
                change = True
            if change and tete:
                # LES RECTANGLES DES SPRITES SUIVENT LA TEXTURE : sans cela
                # on n affiche qu un coin de l image agrandie.
                d = sprites_echelle(d, facteurs)
                d = d[:tete[0]] + ecrire_txp(tete[1], textures)
                m[fich] = d
        if change:
            if not os.path.exists(origine):
                os.rename(chemin, origine)
            # DANS LA FORME DE L'ORIGINAL, et ce n'est pas un detail de style :
            # `spr_n_fnt32.farc` reecrite en `FArc` brut la ou le jeu avait un
            # `FArC` ferme le jeu, avec le membre INCHANGE (2026-10-11).
            mfarc.comme(origine, chemin, m)
            _registre_ajouter(arc)
            print('   -> %s reecrit (%d octets)'
                  % (arc, os.path.getsize(chemin)))
            _aet_suivre(arc, facteurs)
    return 0


# ---------------------------------------------------------------------------
# LES CALQUES SUIVENT LA PLANCHE (2026-10-12)
#
# MESURE, et elle est sans appel : `spr_n_adv__tex01` et `tex03` posees en 4x,
# rien d autre touche -- le logo AM2 s affiche QUATRE FOIS TROP GRAND et son
# coin haut-gauche n a pas bouge. Deux choses s en deduisent, et `tools/aet.py`
# les explique :
#
#   . la taille du quad vient du RECTANGLE EN PIXELS DU SPRITE (celui que
#     `sprites_echelle` vient de multiplier), pas du champ `largeur/hauteur`
#     de la surface AET ;
#   . l `origine` du calque est en pixels de la surface : laissee telle quelle
#     devant une image F fois plus grande, elle ancre au 1/F de l image.
#
# Poser une planche agrandie SANS corriger ses calques ne donne donc pas un
# resultat imparfait : il donne un ecran casse. L outil le fait lui-meme.
def _aet_suivre(arc, facteurs):
    """Remet a l echelle les calques AET qui dessinent les textures posees."""
    if not facteurs:
        return
    base = arc[:-5] if arc.endswith('.farc') else arc        # spr_n_adv
    aet_nom = 'aet_' + base.split('_', 1)[1] + '.bin'        # aet_n_adv.bin
    aet_chemin = os.path.join(DEUXD, aet_nom)
    if not os.path.exists(aet_chemin):
        print('   (pas de %s : aucun calque a reprendre)' % aet_nom)
        return
    import aet_echelle
    par_facteur = {}
    for k, f in facteurs.items():
        par_facteur.setdefault(f, []).append(k)
    for f, tex in sorted(par_facteur.items()):
        r = aet_echelle.main(
            [aet_chemin, '--spr', os.path.join(DEUXD, arc),
             '--texture'] + [str(k) for k in sorted(tex)]
            + ['--facteur', '%g' % f])
        if r:
            print('   ATTENTION : les calques de %s n ont PAS ete repris '
                  '(code %d). L image sera %g fois trop grande.'
                  % (aet_nom, r, f))
            return
    _registre_ajouter(aet_nom)


# LE REGISTRE DE CE QU ON A POSE. Il faut le tenir, et c est paye : le premier
# `--retirer` rendait TOUT `.farc.origine` trouve dans `rom/2d/`, y compris
# celui de `spr_n_cmnps3` -- pose par `schema_manette_xbox.py` le 2026-10-09.
# Il a defait le repeignage d un autre chantier sans rien dire. Un outil ne
# rend que ce qu il a lui-meme pose.
REGISTRE = os.path.join(HD_RACINE, '_POSEES.txt')


def _registre_lire():
    if not os.path.exists(REGISTRE):
        return []
    with io.open(REGISTRE, encoding='ascii') as fp:
        return [l.strip() for l in fp if l.strip()]


def _registre_ajouter(nom):
    v = _registre_lire()
    if nom not in v:
        v.append(nom)
        with io.open(REGISTRE, 'w', encoding='ascii', newline=chr(10)) as fp:
            fp.write(chr(10).join(sorted(v)) + chr(10))


def retirer():
    poses = _registre_lire()
    if not poses:
        print('Le registre %s est vide : rien n a ete pose par cet outil.'
              % os.path.basename(REGISTRE))
        return 0
    n = 0
    for nom in poses:
        # Le registre porte des `.farc` ET des `.bin` : les planches et les
        # calques qu'on a repris avec elles. Les deux se rendent pareil.
        origine = os.path.join(DEUXD, nom + '.origine')
        cible = os.path.join(DEUXD, nom)
        if not os.path.exists(origine):
            print('   %s : pas d origine gardee' % nom)
            continue
        if os.path.exists(cible):
            os.remove(cible)
        os.rename(origine, cible)
        print('   rendu : %s' % nom)
        n += 1
    if os.path.exists(REGISTRE):
        os.remove(REGISTRE)
    print('%d archive(s) rendue(s).' % n)
    return 0


def main(argv):
    if '--sortir' in argv:
        return inventaire(sortir=True)
    if '--inventaire' in argv:
        return inventaire()
    if '--poser' in argv:
        return poser()
    if '--controle' in argv:
        return poser(controle=True)
    if '--retirer' in argv:
        return retirer()
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
