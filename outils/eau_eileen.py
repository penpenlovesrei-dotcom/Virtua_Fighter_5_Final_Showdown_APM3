#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""L EAU D EILEEN : porte sur la variante VF5 (`skb`) les materiaux d eau de
VF5 R, et les textures qui leur manquent.

CE QUI A ETE MESURE (2026-10-15), et qui decide de tout

A l ecran, de pres : la surface du ring de `skb` a DEJA la geometrie de l eau
-- les vagues sont la, et elles s animent -- mais elle est rendue BLANC
LAITEUX. Chez `sk5` (la meme aire, version R) la meme surface est sombre et
transparente. Ce n est donc ni l objet, ni l animation, ni la chaine
nom -> identifiant (verifiee : `STGSKB_EFF_WATER` -> objset 6180 index 127,
present) : c est le MATERIAU.

Trois objets portent l eau, et les trois generations ne les accordent pas :

    objet                shader     ce qui separe ver.B de VF5 R
    stgslk_eff_water     WATER01    drapeaux 0x0101 au lieu de 0x8529, et il
                                    manque l emplacement 5 -- le cube
                                    d environnement `MIZU`, l eau elle-meme
    stgslk_water_ring    WATRING    18 octets : deux textures (9205, 9206) et
                                    les couleurs
    stgslk_reflect       BLINN      2 octets

Un bloc de materiau est de la DONNEE PURE : entre FS et VF5 R, le meme
materiau ne differe que par des identifiants de texture et des couleurs,
jamais par un deplacement. Il se transpose donc tel quel.

Pourquoi VF5 R et non Final Showdown : la teinte de `stgslk_eff_water` vaut
0,80 / 0,70 / 0,50 chez FS (du sable), 1,00 / 0,85 / 0,65 chez ver.B (plus
sable encore) et 0,10 / 0,10 / 0,10 chez R. Seule celle de R est de l eau --
et `sk5` le montre a l ecran.

CE QUI DECIDE VRAIMENT : L ECLAIRAGE

Mesure a l ecran, par elimination. On peint tous les materiaux de l objset en
magenta sauf `stgslk_water_ring`, dont on COUPE les textures : tout devient
magenta et le disque du ring devient raye. Le disque du ring EST donc
`stgslk_water_ring` -- un premier essai, qui ne coloriait que la diffuse de
BLINN en +0x3D8, n avait rien change : le shader WATRING ne la lit pas.

Mais avec le materiau ET les textures de R, le ring reste du sable. Ce qui
reste alors se lit dans `rom/light_param/` :

    fichier            skb (ver.B)            sk5 (VF5 R)
    couleur du fog     1,30 1,20 1,00         0,10 0,30 0,70
    2e couleur         0,36 0,30 0,20         0,10 0,15 0,20
    densite            0,60                   0,30
    ambiante           0,70                   0,30

Sous une lumiere chaude, la meme surface lit comme du sable. Avec les six
fichiers d eclairage de `sk5` (les cinq `light_param` et le `.ibl`), le ring
de `skb` devient de l eau sombre qui ondule -- verifie a l ecran.

L ondulation, elle, etait deja la : `STGSKB_EFF_WATER.a3da` porte la meme
courbe `WATER` que celle de `sk5` (120 images, memes cles), et le creux sous
les pas se voyait sur les captures d avant.

CE QUE L OUTIL FAIT

  1. repart TOUJOURS de la sauvegarde si elle existe : deux passages donnent
     le meme resultat, et `--rendre` remet l archive d origine ;
  2. prend dans l objset de R les blocs de materiau (0x4B0 octets chacun) et
     les textures qui manquent a `skb` ;
  3. ajoute les textures a la planche et leurs identifiants a la liste de
     l objset -- la liste est la derniere chose du fichier et des zeros la
     suivent : rien n est decale ;
  4. ecrit a cote, puis remplace ;
  5. RELIT L ARCHIVE PRODUITE et imprime ce qu elle porte. Jamais le script,
     toujours le resultat.

    py -3 tools/eau_eileen.py --controle     ne rien ecrire, tout verifier
    py -3 tools/eau_eileen.py                poser
    py -3 tools/eau_eileen.py --rendre       remettre l archive d origine
"""
import argparse
import gzip
import io
import os
import struct
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
sys.path.insert(0, ICI)

import objset as O                                             # noqa: E402
import objet_materiaux as M                                    # noqa: E402

SOURCE = os.path.join(RACINE, 'extracted', 'slk_VF5R', 'stgslk_obj.bin')
SOURCE_TEX = os.path.join(RACINE, 'extracted', 'slk_VF5R', 'stgslk_tex.bin')
POSE = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media',
                    'rom', 'objset', 'stgskb.farc')
SAUVE = POSE + '.avant_eau'

PORTS = ('stgslk_eff_water', 'stgslk_reflect')

# LE DISQUE DU RING SUR LE SHADER DE L EAU. Mesure : le shader WATRING est
# ampute (13 instructions, un cube d IRRADIANCE par la normale, aucune alpha,
# aucun reflet) ; WATER01 a le cube par le VECTEUR DE REFLET, le reflet en
# espace ecran et le Fresnel. Et la permutation que le materiau 0x8529
# choisit -- rang 130, water01.0011101001.fp -- est l une des QUATRE que ce
# build charge (table de presence du sous-shader, lue en 0x180175D2B).
# Mesure a l execution : la passe 2 (reflet) EST allumee pour notre decor
# ([donneesDecor+0xC0] non nul, le site 0x18018FA70 est atteint).
# On recopie donc le materiau de eff_water sur water_ring.
# Forme : {objet cible: objet modele, pris dans l objset POSE}
# NE PAS recopier le materiau de l eau sur l anneau : WATER01 apporte le cube
# et le reflet, mais son programme de SOMMETS ne deforme rien. Le seul
# programme qui deplace le maillage est water_ring.000.vp :
#     TEX displace, a_tex0, texture[14], 2D
# Les deux s excluent, et c est la deformation qui a ete choisie.
COPIES = {}
MATERIAU_PAS = 0x4B0

# AUCUN REMPLACEMENT DE TEXTURE -- et c est une mesure, pas un renoncement.
# L emplacement 0 de l eau nomme `F_VF5S_SLK00_MU_RINGOUTMIZU` (9261), une
# image de SABLE BEIGE NUAGEUX dans les TROIS generations (ver.B = consoles,
# R, FS). Ce n est pas l eau : c est le FOND vu a travers l eau. La remplacer
# par la turbidite de l anneau (12674) ne ressemble a rien d existant.
# Forme : {(objet, emplacement): identifiant voulu}
REMPLACEMENTS = {}

# PAS DE MELANGE ALPHA NON PLUS. Les trois generations portent
# `+0x3D4 = 0x10000A80` sur `eff_water` comme sur `water_ring`. Allumer le
# bit 0 et eteindre le bit 28 donne bien de la transparence a l ecran, mais
# ne correspond a AUCUNE version du jeu -- et sur `water_ring`, qui fait le
# plancher du ring chez ver.B (aucun objet `stgslk_ring` de ce cote), cela
# ouvre un trou : il n y a rien dessous.
#
# Pour memoire, le mecanisme, lu dans le moteur :
#     bit 0 (ou 1), bit 2 en veto   allume le melange   0x1800F3105
#     bits 5..8 / 9..12             facteurs source / destination
#     bit 28                        court-circuite tout au repartiteur
#                                   0x1800EB71B : `bt ecx,0x1c` / `jb`
#                                   envoie dans la file OPAQUE
#
# Ce qui reste : la NORMALE du ring. L emplacement 2 de `water_ring` porte
# 0x000418C3 chez ver.B et 0x000418D3 chez FS comme chez VF5 R -- un seul bit,
# 0x10, le champ qui lie l emplacement a son unite de texture (le moteur teste
# le type en 0x1800F1A86). Le shader `water_ring` lit la normale en
# `texture[2]`. L emplacement 2 commence a 0x14 + 2*0x78 = 0x104.
# Forme : {(objet, deplacement): (masque OU, masque ET)}
DRAPEAUX = {('stgslk_water_ring', 0x104): (0x00000010, 0xFFFFFFFF)}

# L ECLAIRAGE, et c est LUI qui decide de l eau (mesure du 2026-10-15, voir
# plus bas). Les fichiers sont dans l arbre libre, en clair.
ROM = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media', 'rom')
LUMIERES = [(os.path.join(ROM, 'light_param', '%s_skb.txt' % f),
             os.path.join(ROM, 'light_param', '%s_sk5.txt' % f))
            for f in ('light', 'fog', 'glow', 'wind', 'envmap_correct')]
LUMIERES.append((os.path.join(ROM, 'ibl', 'skb.ibl'),
                 os.path.join(ROM, 'ibl', 'sk5.ibl')))


# ---------------------------------------------------------------- le TXP
def lire_txp(d):
    """(debut, groupe, [textures]) -- tous les niveaux, et la magie du bloc.

    Un bloc de cube porte la magie TXP 05 et non 04 : on la garde telle
    quelle, sinon la planche relue n a plus de cube.

    Les offsets, de bloc comme de niveau, sont ALIGNES SUR QUATRE OCTETS :
    sans cela le tour complet rend 60 octets de moins sur la planche de
    `skb`, et tous les offsets apres la 217e texture sont faux.
    """
    i = d.find(b'TXP\x03')
    if i < 0:
        raise ValueError('pas de bloc TXP')
    n, groupe = struct.unpack_from('<II', d, i + 4)
    offs = list(struct.unpack_from('<%dI' % n, d, i + 12))
    textures = []
    for o in offs:
        t = i + o
        magie = d[t:t + 4]
        nm, g2 = struct.unpack_from('<II', d, t + 4)
        so = struct.unpack_from('<%dI' % nm, d, t + 12)
        niveaux = []
        for j in so:
            s = t + j
            w, h, f, lvl, taille = struct.unpack_from('<5I', d, s + 4)
            niveaux.append(dict(larg=w, haut=h, format=f, niveau=lvl,
                                octets=d[s + 0x18:s + 0x18 + taille]))
        textures.append(dict(groupe=g2, niveaux=niveaux, magie=magie))
    return i, groupe, textures


def ecrire_txp(groupe, textures):
    """Le bloc TXP entier, chaque offset aligne sur quatre octets."""
    def cale(b):
        if len(b) % 4:
            b += bytes(4 - len(b) % 4)
        return b

    n = len(textures)
    tete = bytearray(b'TXP\x03' + struct.pack('<II', n, groupe))
    tete += bytes(4 * n)
    corps = bytearray()
    offsets = []
    for tex in textures:
        corps = bytearray(cale(bytes(corps)))
        offsets.append(len(tete) + len(corps))
        nm = len(tex['niveaux'])
        bloc = bytearray(tex['magie'] + struct.pack('<II', nm, tex['groupe']))
        bloc += bytes(4 * nm)
        sous = bytearray()
        so = []
        for niv in tex['niveaux']:
            sous = bytearray(cale(bytes(sous)))
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


# ---------------------------------------------------------------- le FArC
def defarc(chemin):
    """[(nom, octets)] dans l ordre de l archive, comprimee ou non."""
    d = open(chemin, 'rb').read()
    if d[:4] not in (b'FArC', b'FArc'):
        raise ValueError('%s : pas un FArC' % chemin)
    comprime = d[:4] == b'FArC'
    fin = 8 + struct.unpack_from('>I', d, 4)[0]
    o, out = 12, []
    while o < fin:
        e = d.index(b'\0', o)
        nom = d[o:e].decode('ascii')
        o = e + 1
        if comprime:
            off, csize, usize = struct.unpack_from('>III', d, o)
            o += 12
            out.append((nom, gzip.decompress(d[off:off + csize])))
        else:
            off, usize = struct.unpack_from('>II', d, o)
            o += 8
            out.append((nom, d[off:off + usize]))
    return out


def refarc(membres, dest):
    """Ecrit un FArC comme SEGA : chaque membre gzip, en-tete gros-boutiste,
    drapeau FNAME portant le nom du membre."""
    paquets = []
    for nom, brut in membres:
        tampon = io.BytesIO()
        with gzip.GzipFile(filename=nom, mode='wb', fileobj=tampon, mtime=0) \
                as g:
            g.write(brut)
        paquets.append((nom, tampon.getvalue(), len(brut)))
    tete = sum(len(n.encode('ascii')) + 1 + 12 for n, _, _ in paquets)
    debut = 12 + tete
    entetes, corps, pos = bytearray(), bytearray(), debut
    for nom, donnees, usize in paquets:
        entetes += nom.encode('ascii') + b'\x00'
        entetes += struct.pack('>III', pos, len(donnees), usize)
        corps += donnees
        pos += len(donnees)
    sortie = bytearray(b'FArC') + struct.pack('>II', debut - 8, 1) + entetes
    if len(sortie) != debut:
        raise AssertionError('en-tete FArC : %d au lieu de %d'
                             % (len(sortie), debut))
    with open(dest, 'wb') as fp:
        fp.write(bytes(sortie) + bytes(corps))


# ---------------------------------------------------------------- l objset
def objset_de(octets, ou):
    open(ou, 'wb').write(octets)
    return O.Objset(ou)


def textures_du_materiau(m):
    out = []
    for t in range(M.TEXTURES_PAR_MATERIAU):
        dr, ident = struct.unpack_from('<2I', m, 0x14 + t * M.TEXTURE_PAS)
        if ident != 0xFFFFFFFF:
            out.append((t, dr, ident))
    return out


def jeu_tourne():
    s = subprocess.run(['tasklist'], capture_output=True, text=True).stdout
    return 'vfes.exe' in s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--controle', action='store_true')
    ap.add_argument('--eclairage-r', action='store_true')
    ap.add_argument('--rendre', action='store_true')
    a = ap.parse_args()

    if a.rendre:
        if jeu_tourne():
            print('REFUS : vfes.exe tourne')
            return 1
        rendu = 0
        for cible, _ in LUMIERES:
            vieux = cible + '.avant_eau'
            if os.path.exists(vieux):
                if os.path.exists(cible):
                    os.remove(cible)
                os.replace(vieux, cible)
                rendu += 1
        if rendu:
            print('%d fichier(s) d eclairage remis' % rendu)
        if not os.path.exists(SAUVE):
            print('pas de sauvegarde de l archive : rien de plus a rendre')
            return 0 if rendu else 1
        if os.path.exists(POSE):
            os.remove(POSE)
        os.replace(SAUVE, POSE)
        print('archive d origine remise')
        return 0

    travail = os.path.join(os.path.dirname(POSE), '_skb.lu')

    # ---- la source : VF5 R
    rob = O.Objset(SOURCE)
    r_noms = rob.noms()
    r_ids = list(struct.unpack_from('<%dI' % rob.nb_tex, rob.brut,
                                    rob.off_tex))
    _, _, r_textures = lire_txp(open(SOURCE_TEX, 'rb').read())
    if len(r_textures) != rob.nb_tex:
        print('REFUS : R, %d textures dans la planche, %d dans la liste'
              % (len(r_textures), rob.nb_tex))
        return 1
    modeles = {}
    for nom in PORTS:
        if nom not in r_noms:
            print('REFUS : %s absent de l objset de R' % nom)
            return 1
        modeles[nom] = M.materiaux(rob, r_noms.index(nom))[0][1]

    # ---- l archive : on repart TOUJOURS de la sauvegarde
    depart = SAUVE if os.path.exists(SAUVE) else POSE
    print('depart : %s' % os.path.basename(depart))
    membres = defarc(depart)
    noms_m = [n for n, _ in membres]
    paquet = dict(membres)
    obj = paquet['stgskb_obj.bin']
    tex = paquet['stgskb_tex.bin']
    kob = objset_de(obj, travail)
    k_noms = kob.noms()
    off_tex, nb_tex = kob.off_tex, kob.nb_tex
    fin_tex = kob.fin_tex
    fin_liste = off_tex + 4 * nb_tex
    ids = list(struct.unpack_from('<%dI' % nb_tex, obj, off_tex))
    debut, groupe, textures = lire_txp(tex)
    tour = tex[:debut] + ecrire_txp(groupe, textures)
    print('archive %s ; objset %d textures, liste 0x%X..0x%X, fin_tex 0x%X'
          % (' '.join(noms_m), nb_tex, off_tex, fin_liste, fin_tex))
    print('planche %d textures ; ALLER-RETOUR IDENTIQUE : %s'
          % (len(textures), tour == tex))
    if tour != tex:
        print('REFUS : le tour complet de la planche ne rend pas le fichier')
        os.remove(travail)
        return 1
    if len(textures) != nb_tex:
        print('REFUS : %d textures dans la planche, %d dans la liste'
              % (len(textures), nb_tex))
        os.remove(travail)
        return 1

    # ---- ce qu il faut ajouter
    manquantes = []
    voulues = dict(modeles)
    for (n0, empl), ident in REMPLACEMENTS.items():
        b = bytearray(voulues[n0])
        struct.pack_into('<I', b, 0x14 + empl * M.TEXTURE_PAS + 4, ident)
        voulues[n0] = bytes(b)
    for nom in PORTS:
        for t, dr, ident in textures_du_materiau(voulues[nom]):
            if ident not in ids and ident not in manquantes:
                if ident not in r_ids:
                    print('REFUS : la texture %d n est pas dans l objset de R'
                          % ident)
                    os.remove(travail)
                    return 1
                manquantes.append(ident)
    print('textures a ajouter : %s'
          % (' '.join(str(x) for x in manquantes) or '(aucune)'))
    besoin = fin_liste + 4 * len(manquantes)
    if besoin > fin_tex:
        print('REFUS : pas de place pour %d identifiants (0x%X > 0x%X)'
              % (len(manquantes), besoin, fin_tex))
        os.remove(travail)
        return 1
    if any(obj[fin_liste:besoin]):
        print('REFUS : la place apres la liste n est pas a zero')
        os.remove(travail)
        return 1
    cibles = {}
    touches = (list(PORTS) + [n for n, _ in REMPLACEMENTS]
               + [n for n, _ in DRAPEAUX] + list(COPIES) + list(COPIES.values()))
    vus_nom = []
    for n in touches:
        if n not in vus_nom:
            vus_nom.append(n)
    for nom in vus_nom:
        if nom not in k_noms:
            print('REFUS : %s absent de l objset de skb' % nom)
            os.remove(travail)
            return 1
        dep, ancien = M.materiaux(kob, k_noms.index(nom))[0]
        if len(ancien) != MATERIAU_PAS:
            print('REFUS : bloc de materiau de taille inattendue')
            os.remove(travail)
            return 1
        if nom in modeles:
            ecart = sum(1 for i in range(MATERIAU_PAS)
                        if ancien[i] != modeles[nom][i])
            print('   %-20s a 0x%06X  %3d octets a changer  (shader %r)'
                  % (nom, dep, ecart, M.shader(ancien)))
        else:
            print('   %-20s a 0x%06X  (shader %r, retouche seule)'
                  % (nom, dep, M.shader(ancien)))
        cibles[nom] = dep
    os.remove(travail)

    if not a.eclairage_r:
        rendus = 0
        for cible, _ in LUMIERES:
            vieux = cible + '.avant_eau'
            if os.path.exists(vieux):
                if os.path.exists(cible):
                    os.remove(cible)
                os.replace(vieux, cible)
                rendus += 1
        print('eclairage : celui du decor (ver.B). %d fichier(s) rendu(s).'
              % rendus)
        print('            --eclairage-r pour poser celui de sk5 a la place.')
        LUMIERES[:] = []
    print('eclairage :')
    for cible, source in LUMIERES:
        if not os.path.exists(source):
            print('REFUS : %s absent' % source)
            return 1
        pareil = (open(cible, 'rb').read() == open(source, 'rb').read()
                  if os.path.exists(cible) else False)
        print('   %-26s <- %-26s %s'
              % (os.path.basename(cible), os.path.basename(source),
                 'deja identique' if pareil else ''))

    if a.controle:
        print('CONTROLE SEUL : rien ecrit.')
        return 0
    if jeu_tourne():
        print('REFUS : vfes.exe tourne')
        return 1

    # ---- les modifications
    neuf_obj = bytearray(obj)
    for cible, modele in COPIES.items():
        dc, dm = cibles[cible], cibles[modele]
        neuf_obj[dc:dc + MATERIAU_PAS] = modeles[modele]
        print('   %s <- le materiau de %s (0x%06X <- 0x%06X)'
              % (cible, modele, dc, dm))
    for nom in PORTS:
        d = cibles[nom]
        neuf_obj[d:d + MATERIAU_PAS] = modeles[nom]
    for (nom, empl), ident in REMPLACEMENTS.items():
        d = cibles[nom]
        o = d + 0x14 + empl * M.TEXTURE_PAS + 4
        avant, = struct.unpack_from('<I', neuf_obj, o)
        struct.pack_into('<I', neuf_obj, o, ident)
        print('   %s emplacement %d : texture %d -> %d'
              % (nom, empl, avant, ident))
    for (nom, dep), (ou, et) in DRAPEAUX.items():
        d = cibles[nom]
        avant, = struct.unpack_from('<I', neuf_obj, d + dep)
        apres = (avant | ou) & et
        struct.pack_into('<I', neuf_obj, d + dep, apres)
        print('   %s +0x%03X : %08X -> %08X' % (nom, dep, avant, apres))
    for k, ident in enumerate(manquantes):
        struct.pack_into('<I', neuf_obj, fin_liste + 4 * k, ident)
        src = r_textures[r_ids.index(ident)]
        textures.append(dict(groupe=src['groupe'], niveaux=src['niveaux'],
                             magie=src['magie']))
    struct.pack_into('<I', neuf_obj, 0x20, nb_tex + len(manquantes))
    neuf_tex = tex[:debut] + ecrire_txp(groupe, textures)

    neufs = []
    for nom, brut in membres:
        if nom.endswith('_obj.bin'):
            neufs.append((nom, bytes(neuf_obj)))
        elif nom.endswith('_tex.bin'):
            neufs.append((nom, neuf_tex))
        else:
            neufs.append((nom, brut))
    cote = POSE + '.neuf'
    refarc(neufs, cote)
    if not os.path.exists(SAUVE):
        os.replace(POSE, SAUVE)
        print('sauvegarde : %s' % os.path.basename(SAUVE))
    elif os.path.exists(POSE):
        os.remove(POSE)
    os.replace(cote, POSE)
    print('pose : %s (%d octets)'
          % (os.path.basename(POSE), os.path.getsize(POSE)))

    for cible, source in LUMIERES:
        vieux = cible + '.avant_eau'
        if not os.path.exists(vieux) and os.path.exists(cible):
            os.replace(cible, vieux)
        tmp = cible + '.neuf'
        with open(tmp, 'wb') as fp:
            fp.write(open(source, 'rb').read())
        if os.path.exists(cible):
            os.remove(cible)
        os.replace(tmp, cible)
    print('eclairage pose : %d fichier(s)' % len(LUMIERES))

    # ---- RELIRE LE RESULTAT
    print()
    print('--- relu dans l archive PRODUITE ---')
    produits = dict(defarc(POSE))
    o2 = produits['stgskb_obj.bin']
    k2 = objset_de(o2, travail)
    ids2 = list(struct.unpack_from('<%dI' % k2.nb_tex, o2, k2.off_tex))
    _, _, t2 = lire_txp(produits['stgskb_tex.bin'])
    n2 = k2.noms()
    print('   textures listees %d   dans la planche %d' % (k2.nb_tex, len(t2)))
    faute = 0
    for ident in manquantes:
        ok = ident in ids2
        print('   texture %d ajoutee : %s' % (ident, ok))
        faute += 0 if ok else 1
    attendus = {}
    for cible, modele in COPIES.items():
        attendus[cible] = modeles[modele]
    for nom in PORTS:
        b = bytearray(modeles[nom])
        for (n0, empl), ident in REMPLACEMENTS.items():
            if n0 == nom:
                struct.pack_into('<I', b, 0x14 + empl * M.TEXTURE_PAS + 4,
                                 ident)
        for (n0, dep), (ou, et) in DRAPEAUX.items():
            if n0 == nom:
                v, = struct.unpack_from('<I', b, dep)
                struct.pack_into('<I', b, dep, (v | ou) & et)
        attendus[nom] = bytes(b)
    for nom in list(PORTS) + list(COPIES):
        _, m2 = M.materiaux(k2, n2.index(nom))[0]
        pareil = (m2 == attendus[nom])
        print('   %-20s shader %-9r drapeaux %08X  %d emplacements  '
              'conforme : %s'
              % (nom, M.shader(m2), struct.unpack_from('<I', m2, 4)[0], m2[0],
                 pareil))
        for t, dr, ident in textures_du_materiau(m2):
            marque = '' if ident in ids2 else '   ABSENTE !'
            if ident not in ids2:
                faute += 1
            print('        emplacement %d  drapeaux %08X  texture %d%s'
                  % (t, dr, ident, marque))
        faute += 0 if pareil else 1
    os.remove(travail)
    for cible, source in LUMIERES:
        ok = open(cible, 'rb').read() == open(source, 'rb').read()
        print('   %-26s identique a celui de sk5 : %s'
              % (os.path.basename(cible), ok))
        faute += 0 if ok else 1
    if faute:
        print('REFUS : %d defaut(s) dans ce qui est pose' % faute)
        return 1
    print('   tout concorde avec VF5 R.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
