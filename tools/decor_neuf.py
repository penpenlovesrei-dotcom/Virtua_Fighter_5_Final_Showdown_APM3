#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Pose (ou retire) tout ce qu'un decor VRAIMENT AJOUTE demande cote fichiers.

Le binaire, lui, est deja fait : `patch_moteur.py --decors-table <N>
--decor-neuf <code> --objset <id>` remplit l'entree neuve. Ici on s'occupe des
QUATRE choses qui restent, et qui sont toutes des fichiers.

    1. `obj_db.bin`      une entree de jeu d'objets + ses objets
    2. `auth_3d_db.bin`  deux categories, `STGxxx` et `EFFSTGxxx`
    3. les deux bases dans le `.par`, et **pas de la meme facon** :
       `auth_3d_db.bin` est pose en fichier libre et son nom MASQUE dans
       l'index ; `obj_db.bin`, lui, est ECRIT DANS l'archive, parce que son
       chargeur y lit quand meme (voir plus bas)
    4. les DIX pieces du decor, sous le code neuf -- et la, **aucun nom a
       masquer** : `stgd5r.farc`, `d5r.ibl`, `STGD5R_COLI.000.bin` n'existent
       dans le `.par` d'aucune facon. C'est le cas facile que
       `ajouter_un_decor.md` §3.1 decrivait, et c'est la premiere fois qu'on y
       est vraiment.

LA DIXIEME PIECE NE VIENT PAS DE LA GENERATION SOURCE (2026-09-10)

Neuf pieces suffisaient... a l'ecran de chargement, qui ne finissait jamais. Le
chargeur d'eclairage `0x1800D7130` compose **SIX** chemins, pas cinq :

    ./rom/ibl/<code>.ibl                          0x1800D71C1
    ./rom/light_param/light_<code>.txt            0x1800D71EA
    ./rom/light_param/fog_<code>.txt              0x1800D720E
    ./rom/light_param/glow_<code>.txt             0x1800D7232
    ./rom/light_param/wind_<code>.txt             0x1800D7256
    ./rom/light_param/envmap_correct_<code>.txt   0x1800D727A   <-- oublie

`envmap_correct_*` **n'existe pas dans le dump VF5R** (2008) : c'est un fichier
de Final Showdown. Les 41 decors du jeu en ont un, donc il n'est pas optionnel.
On le prend dans le `.par` sous le code du MODELE : ce sont neuf nombres
(`1\n1\n1\n0\n0\n0\n0.15\n-0.75\n0.4\n` pour `djo`), aucun nom de decor dedans,
la recopie est donc exacte.

POURQUOI UN DECOR QUI REMPLACE NE MONTRAIT PAS LE DEFAUT : en remplacement, le
code reste `djo`, et seuls les neuf noms poses sont masques dans le `.par` --
l'`envmap_correct_djo.txt` de l'archive continuait de repondre. C'est
l'AJOUT qui expose le trou, parce que plus rien ne repond pour `d5r`.

LE SON D'AMBIANCE NE BLOQUE PAS, ET CE N'EST PAS UNE SUPPOSITION

`rom/sound/se_stage_<code>.csb` n'est ni compose ni dans le descripteur (verifie
: le descripteur de `djo` porte ses deux noms d'auth_3d, sa collision et ses DIX
`.adx` de musique, rien d'autre). Il vient d'une LISTE D'ASSOCIATION en
`0x180408850` : 24 entrees `{indice, pointeur}`, parcourues lineairement par
`0x1801903F3`, terminees par un pointeur nul. **Un indice absent n'echoue pas**
-- `rdx` garde la valeur par defaut posee en `0x1801903DC`, le jeu de sons de
`are`. Le decor ajoute a donc l'ambiance de `are`, et rien ne bloque.

Pour lui donner celle de `djo` il faudrait ajouter `{42, 0x1804084C0}` a cette
liste -- mais elle est suivie IMMEDIATEMENT de ses chaines (`0x1804089E0` porte
`rom/sound/se_stage_are.csb`), donc il faudrait la deplacer, comme les trois
autres tables. Ce n'est pas fait, et ce n'est pas urgent.

LES LONGUEURS DOIVENT SE CORRESPONDRE, et ce n'est pas une coquetterie :
`importer_decor.renommer_farc` substitue les noms **en place** dans l'en-tete
du `FArC`. `djo` (3) -> `d5r` (3), `stgdjo` (6) -> `stgd5r` (6), `EFFSTGDJO`
(9) -> `EFFSTGD5R` (9). Un code a quatre lettres ne passerait pas.

LES NOMS D'OBJETS CHANGENT, ET C'EST L'INVERSE DE CE QU'ON CROYAIT (2026-09-10)

On a longtemps ecrit ici que les noms d'objets se recopiaient VERBATIM. C'est
vrai DANS L'ARCHIVE -- elle est celle du modele, elle porte ses noms. C'est faux
dans `obj_db` : le moteur tient un **index GLOBAL des noms d'objets, trie, lu
par dichotomie** (`FUN_1800F8B50`). Y declarer deux fois `STGDJO_EFF_FIRE_BMZ`
fait rendre le PREMIER -- celui de l'objset 28, qui n'est pas charge -- et
l'animation des flammes se lie a un objet absent, sans un message.

`renommer()` substitue donc `STGDJO_` -> `STGD5R_` (meme longueur, en place)
dans les objets d'`obj_db`, dans les uid d'`auth_3d_db`, et dans les `.a3da`
eux-memes, qui nomment leurs objets. Les **textures** ne sont pas touchees :
elles s'appellent `F_VF5E_DJO00_…`, sans `STGDJO_`, et `tex_db` les declare
globalement sous ces noms-la.

    py -3 tools/decor_neuf.py --etat d5r
    py -3 tools/decor_neuf.py --poser d5r --depuis djo --source VF5R --objset 6150
    py -3 tools/decor_neuf.py --retirer d5r
"""
import io
import os
import re
import shutil
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import a3d_db                                                  # noqa: E402
import importer_decor                                          # noqa: E402
import obj_db                                                  # noqa: E402

SOURCES = os.path.join(RACINE, 'extracted', 'decors')
EXTRAITS = os.path.join(RACINE, 'extracted')
MEDIA = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media')
PAR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_data.par')

# Les deux bases : nom dans le `.par` (plat), et chemin que le moteur compose.
BASES = (('obj_db.bin', os.path.join('rom', 'objset')),
         ('auth_3d_db.bin', os.path.join('rom', 'auth_3d')))

# ET ELLES NE SE POSENT PAS DE LA MEME FACON (mesure du 2026-09-10).
#
# `auth_3d_db.bin` : masquer son nom dans le `.par` SUFFIT. Le moteur ne le
# trouve plus dans l'archive et l'ouvre sur le disque -- `tracer_fichiers.py`
# le voit passer, deux fois.
#
# `obj_db.bin` : le masquage NE SERT A RIEN. Son chargeur (`0x1800F97E0`)
# compose bien `./rom/objset/obj_db.bin` et recoit les octets de l'ARCHIVE,
# masque ou pas -- essaye en changeant le dernier caractere du nom, puis le
# premier, et en retirant le fichier pose : le vecteur d'objsets du moteur
# gardait ses 6044 entrees d'origine et notre objset 6150 restait introuvable,
# donc `stgd5r.farc` n'etait jamais demande et le chargement ne finissait
# jamais. Il faut donc ecrire nos octets DANS le `.par` (`par_ecrire.py`).
#
# La difference n'est pas dans le masquage : c'est l'ordre de resolution de
# chaque chargeur. Voir `REPRISE.md` (42).
BASE_DANS_LE_PAR = 'obj_db.bin'


def pieces(code):
    """Les neuf morceaux qui viennent de la generation SOURCE.

    Les decors de Dural de VF5 R n'ont pas de scene (`STG<code>.farc`) : leur
    categorie est VIDE dans la base de R (`variantes_5r.SANS_SCENE`, verifie
    par `variantes_5r.controler`). On ne la pose donc pas."""
    import variantes_5r
    c, C = code.lower(), code.upper()
    lot = [('objset', 'stg%s.farc' % c, 'objset'),
           ('coli', 'STG%s_COLI.000.bin' % C, '')]
    if not variantes_5r.sans_scene(c):
        lot.append(('auth_3d', 'STG%s.farc' % C, 'auth_3d'))
    lot += [('auth_3d', 'EFFSTG%s.farc' % C, 'auth_3d'),
            ('ibl', '%s.ibl' % c, 'ibl')]
    for p in ('light', 'fog', 'glow', 'wind'):
        lot.append(('light_param', '%s_%s.txt' % (p, c), 'light_param'))
    return lot


def pieces_du_par(code):
    """Ce que la generation source n'a pas, et que le `.par` du jeu fournit.

    Une seule pour l'instant : `envmap_correct_<code>.txt`, le sixieme fichier
    d'eclairage. Voir l'en-tete du module -- son absence bloque l'ecran de
    chargement pour toujours, et seul un AJOUT l'expose.
    """
    return [('light_param', 'envmap_correct_%s.txt' % code.lower(),
             'light_param')]


def toutes_les_pieces(code):
    return pieces(code) + pieces_du_par(code)


def extraire_du_par(nom):
    """Rend les octets d'un fichier du `.par`, ou None. Refuse le comprime.

    Les fichiers d'eclairage en texte ne sont pas comprimes (verifie : les 41
    `envmap_correct_*` sortent en clair). Un fichier comprime demanderait le
    decompresseur SLLZ, et il n'y a pas de raison d'y toucher ici : on refuse
    plutot que de rendre des octets faux.
    """
    import par_inventaire
    _, fichiers = par_inventaire.lire(PAR)
    for n, taille, comp, offset, comprime in fichiers:
        if n != nom:
            continue
        if comprime:
            print('REFUS : %s est comprime (SLLZ) dans le .par' % nom)
            return None
        with open(PAR, 'rb') as fp:
            fp.seek(offset)
            return fp.read(taille)
    return None


def renommer(texte, depuis, code):
    """`STGDJO_` -> `STGD5R_`, et la meme chose en minuscules.

    POURQUOI RENOMMER LES OBJETS, ALORS QU'ON A LONGTEMPS ECRIT LE CONTRAIRE
    (mesure du 2026-09-10)

    Les flammes du dojo importe ne s'allumaient pas. Leur animation dit :

        object.0.uid_name = STGDJO_EFF_FIRE_BMZ        un objet, par NOM

    et le moteur resout ce nom avec `FUN_1800F8B50` : un **index GLOBAL des
    noms d'objets**, {nom, valeur} de 16 octets, `[gestionnaire+0xC8..+0xD0]`,
    **trie par nom**, parcouru par DICHOTOMIE. Cet index est bati depuis
    `obj_db`. En declarant notre objset avec les 171 noms du modele, on y
    mettait deux fois les memes : la dichotomie rend le PREMIER, celui de
    l'objset 28 (`STGDJO`), qui n'est pas charge dans un build d'ajout. L'effet
    se liait a un objet d'un objset absent -- rien a l'ecran, aucun message.

    La geometrie, elle, marchait : le descripteur ne demande pas ses objets par
    nom mais par identifiant empaquete (`6150:114`..`118`).

    CE QU'ON NE RENOMME PAS, et c'est aussi important : les **textures**
    (`F_VF5E_DJO00_IK_FIRE_000`). Elles sont declarees globalement dans
    `tex_db` sous ces noms-la, et notre archive les porte telles quelles. Le
    motif est `STGDJO_`, pas `DJO` : `F_VF5E_DJO00_…` n'est donc pas touche.
    """
    return (texte.replace('STG%s_' % depuis.upper(), 'STG%s_' % code.upper())
            .replace('stg%s_' % depuis.lower(), 'stg%s_' % code.lower()))


def renommer_octets(octets, depuis, code):
    return (octets.replace(('STG%s_' % depuis.upper()).encode('ascii'),
                           ('STG%s_' % code.upper()).encode('ascii'))
            .replace(('stg%s_' % depuis.lower()).encode('ascii'),
                     ('stg%s_' % code.lower()).encode('ascii')))


def renommer_archive_a3d(chemin, depuis, code):
    """Refabrique une archive d'animations avec les noms du decor neuf.

    Les membres sont refaits en `FArc` BRUT : le moteur lit les deux variantes,
    et recomprimer demanderait de retrouver le gzip exact de SEGA pour ne gagner
    que de la place. `STGDJO` et `STGD5R` font six lettres, donc la
    substitution est EN PLACE dans le texte des `.a3da`.
    """
    import farc
    f = farc.Farc(chemin)
    membres = {}
    for e in f.entries:
        membres[renommer(e['name'], depuis, code)] = renommer_octets(
            f.read(e), depuis, code)
    n = farc.ecrire_farc(chemin, membres)
    return n, list(membres)


def par(action, noms):
    r = subprocess.run([sys.executable, os.path.join(ICI, 'par_masquer.py'),
                        action] + noms, capture_output=True, text=True)
    print(r.stdout.rstrip())
    if r.returncode:
        print(r.stderr.rstrip())
    return r.returncode


def controler_longueurs(code, depuis):
    for a, b, quoi in ((depuis, code, 'le code'),
                       ('stg' + depuis, 'stg' + code, 'le nom d objset'),
                       ('EFFSTG' + depuis.upper(), 'EFFSTG' + code.upper(),
                        'le nom d auth_3d des effets')):
        if len(a) != len(b):
            print('REFUS : %s change de longueur (%s -> %s). Les noms internes '
                  'des archives se substituent EN PLACE : c est impossible.'
                  % (quoi, a, b))
            return False
    return True


def poser_fichiers(code, depuis, src, source):
    """Les DIX pieces d'un decor, sous son code neuf. 0, ou un code d'erreur.

    Separe de `poser_lot` parce que les FICHIERS se posent un decor a la fois,
    alors que les BASES (`obj_db`, `auth_3d_db`) se chargent une fois, se
    remplissent pour tout le lot et s'ecrivent une fois. Poser dix-neuf decors
    en appelant dix-neuf fois l'ancien `poser` aurait reparti de
    `extracted/obj_db.bin` a chaque tour : chaque decor aurait efface les
    dix-huit autres, en silence.
    """
    # --- 1. les fichiers du decor -----------------------------------------
    # On lit les pieces du MODELE et on les ecrit sous le code neuf.
    lot_src = pieces(depuis)
    lot_dst = pieces(code)
    manquants = [n for d, n, _ in lot_src
                 if not os.path.exists(os.path.join(src, d, n))]
    if manquants:
        print('REFUS : %s ne fournit pas le jeu complet, il manque :' % source)
        for n in manquants:
            print('   %s' % n)
        return 2
    print('--- les neuf pieces de la source, sous le code « %s » ---'
          % code)
    for (d, nom, _), (_, nom2, dest) in zip(lot_src, lot_dst):
        rep = os.path.join(MEDIA, 'rom', dest)
        os.makedirs(rep, exist_ok=True)
        shutil.copy2(os.path.join(src, d, nom), os.path.join(rep, nom2))
        print('   %-26s -> rom/%s/%s' % (nom, dest, nom2))
    farc = os.path.join(MEDIA, 'rom', 'objset', 'stg%s.farc' % code.lower())
    n = importer_decor.renommer_farc(farc, depuis.lower().encode('ascii'),
                                     code.lower().encode('ascii'))
    if n < 0:
        return 3
    print('   en-tete de stg%s.farc : %d nom(s) reecrit(s)' % (code.lower(), n))

    # --- LES ANIMATIONS NOMMENT LEURS OBJETS : elles changent de nom aussi ---
    for nom_arch in ('STG%s.farc' % code.upper(),
                     'EFFSTG%s.farc' % code.upper()):
        chemin_arch = os.path.join(MEDIA, 'rom', 'auth_3d', nom_arch)
        if not os.path.exists(chemin_arch):
            continue
        k, membres = renommer_archive_a3d(chemin_arch, depuis, code)
        print('   %-22s %d animation(s) refaites en FArc brut : %s'
              % (nom_arch, k, ', '.join(membres)))

    # --- 1 bis. la dixieme piece, celle que VF5R n'a pas -------------------
    print()
    print('--- la dixieme piece, prise dans le .par sous le code du modele ---')
    for (_, nom_modele, dest), (_, nom_neuf, _) in zip(pieces_du_par(depuis),
                                                       pieces_du_par(code)):
        octets = extraire_du_par(nom_modele)
        if octets is None:
            print('REFUS : %s est introuvable dans le .par. Sans ce fichier, '
                  'l ecran de chargement ne finit JAMAIS (chargeur '
                  'd eclairage 0x1800D727A).' % nom_modele)
            return 2
        rep = os.path.join(MEDIA, 'rom', dest)
        os.makedirs(rep, exist_ok=True)
        io.open(os.path.join(rep, nom_neuf), 'wb').write(octets)
        print('   %-26s -> rom/%s/%s  (%d o, du .par)'
              % (nom_modele, dest, nom_neuf, len(octets)))
    print('   AUCUN nom a masquer : ces dix-la n existent pas dans le .par.')
    return 0


def pieces_vf5(e):
    """Ce que le lot du VF5 d'origine pose pour une entree : [(sous-dossier
    source, nom pose, sous-dossier rom)].

    Une entree a geometrie pose les dix pieces habituelles. Une variante de
    Dural sans geometrie (`d2b`..`d4b`) ne pose que son ECLAIRAGE -- `ibl` et
    les cinq `light_param` -- et partage la geometrie, la collision et les
    effets de `drb`, comme ver.B partage `stgdur`. Et chaque variante de
    Dural pose en plus son objset de CIEL.
    """
    code = e['code']
    if e['source'] is not None:
        lot = toutes_les_pieces(code)
    else:
        lot = pieces(code)[4:] + pieces_du_par(code)
    if e['ciel'] is not None:
        ciel = ('objset', 'stg%s.farc' % e['ciel'][0], 'objset')
        if ciel not in lot:
            lot.append(ciel)
    return lot


def poser_fichiers_vf5(e):
    """Pose une entree du lot du VF5 d'origine. 0, ou un code d'erreur.

    DEUX differences avec `poser_fichiers`, et elles sont mesurees :

      . l'objset n'est pas COPIE mais REECRIT : ses identifiants de texture
        sont ceux de ver.B, que Final Showdown attribue a d'autres textures
        (3 277 sur 3 975). `variantes_vf5.ecrire_objset` les renumerote et
        ne recomprime que le `_obj.bin` ;
      . la source n'a pas le nom du modele : `drb` prend sa geometrie a `dur`
        et son modele a `du1`.
    """
    import variantes_vf5
    src = variantes_vf5.SRC
    code = e['code']
    rom = os.path.join(MEDIA, 'rom')
    if e['source'] is not None:
        s = e['source']
        dest = os.path.join(rom, 'objset', 'stg%s.farc' % code)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            nb, empl = variantes_vf5.ecrire_objset(s, code, dest)
        except ValueError as x:
            print('REFUS : stg%s.farc -- %s' % (s, x))
            return 3
        print('   stg%s.farc -> rom/objset/stg%s.farc  (%d textures '
              'renumerotees, %d emplacements de materiau)' % (s, code, nb, empl))
        for d, nom_s, nom_c, sous in (
                ('coli', 'STG%s_COLI.000.bin' % s.upper(),
                 'STG%s_COLI.000.bin' % code.upper(), ''),
                ('auth_3d', 'STG%s.farc' % s.upper(),
                 'STG%s.farc' % code.upper(), 'auth_3d'),
                ('auth_3d', 'EFFSTG%s.farc' % s.upper(),
                 'EFFSTG%s.farc' % code.upper(), 'auth_3d')):
            p = os.path.join(src, d, nom_s)
            if not os.path.exists(p):
                print('REFUS : ver.B n a pas %s' % nom_s)
                return 2
            os.makedirs(os.path.join(rom, sous), exist_ok=True)
            shutil.copy2(p, os.path.join(rom, sous, nom_c))
            print('   %-26s -> rom/%s/%s' % (nom_s, sous, nom_c))
        for nom_arch in ('STG%s.farc' % code.upper(),
                         'EFFSTG%s.farc' % code.upper()):
            k, membres = renommer_archive_a3d(
                os.path.join(rom, 'auth_3d', nom_arch), s, code)
            print('   %-22s %d animation(s) refaites en FArc brut : %s'
                  % (nom_arch, k, ', '.join(membres)))
    # L'ECLAIRAGE : les cinq fichiers de la SOURCE D'ECLAIRAGE, sous le code
    for (d, nom_s, _), (_, nom_c, sous) in zip(pieces(e['eclairage'])[4:],
                                               pieces(code)[4:]):
        p = os.path.join(src, d, nom_s)
        if not os.path.exists(p):
            print('REFUS : ver.B n a pas %s' % nom_s)
            return 2
        os.makedirs(os.path.join(rom, sous), exist_ok=True)
        shutil.copy2(p, os.path.join(rom, sous, nom_c))
        print('   %-26s -> rom/%s/%s' % (nom_s, sous, nom_c))
    # LA DIXIEME PIECE, prise dans le .par sous le code du MODELE
    for (_, nom_modele, dest), (_, nom_neuf, _) in zip(
            pieces_du_par(e['modele']), pieces_du_par(code)):
        octets = extraire_du_par(nom_modele)
        if octets is None:
            print('REFUS : %s est introuvable dans le .par.' % nom_modele)
            return 2
        os.makedirs(os.path.join(rom, dest), exist_ok=True)
        io.open(os.path.join(rom, dest, nom_neuf), 'wb').write(octets)
        print('   %-26s -> rom/%s/%s  (%d o, du .par)'
              % (nom_modele, dest, nom_neuf, len(octets)))
    # LE CIEL DE DURAL : un objset a lui, que le descripteur nomme et que la
    # liste des objsets EN PLUS (+0x00 de 0x18034D570) fait charger.
    if e['ciel'] is not None:
        c_ciel, _, s_ciel = e['ciel']
        dest = os.path.join(rom, 'objset', 'stg%s.farc' % c_ciel)
        try:
            nb, empl = variantes_vf5.ecrire_objset(s_ciel, c_ciel, dest)
        except ValueError as x:
            print('REFUS : stg%s.farc -- %s' % (s_ciel, x))
            return 3
        print('   stg%s.farc -> rom/objset/stg%s.farc  (le CIEL ; %d '
              'texture(s) renumerotee(s))' % (s_ciel, c_ciel, nb))
    return 0


def poser_lot_vf5(lot5r, bases_seules=False):
    """Pose le lot du VF5 d'origine, puis les bases des DEUX lots."""
    import variantes_vf5
    fautes = variantes_vf5.controler()
    if fautes:
        print('REFUS : la table de variantes_vf5.py a %d faute(s) :'
              % len(fautes))
        for x in fautes:
            print('   . %s' % x)
        return 1
    ents = variantes_vf5.entrees()
    if not bases_seules:
        for i, e in enumerate(ents):
            print()
            print('=' * 72)
            print('[%d/%d] ver.B %s  ->  %s  (indice %d)'
                  % (i + 1, len(ents), e['source'] or e['eclairage'],
                     e['code'], e['indice']))
            print('=' * 72)
            r = poser_fichiers_vf5(e)
            if r:
                return r
    return poser_bases(lot5r, ents)


def retirer_lot_vf5(ents, codes_5r=()):
    """Retire les pieces du VF5 d'origine. Les bases partent avec -- le
    lanceur suivant les refait, c'est ce qu'il fait toujours."""
    print('--- les pieces des %d entrees de ver.B ---' % len(ents))
    for e in ents:
        n = 0
        for _, nom, dest in pieces_vf5(e):
            p = os.path.join(MEDIA, 'rom', dest, nom)
            if os.path.exists(p):
                os.remove(p)
                n += 1
        print('   %-5s %d piece(s) retiree(s)' % (e['code'], n))
    if codes_5r:
        retirer_lot(list(codes_5r))
        return 0
    return retirer_lot([])


def etat_lot_vf5(ents):
    print('--- les pieces des %d entrees de ver.B ---' % len(ents))
    for e in ents:
        n = [os.path.exists(os.path.join(MEDIA, 'rom', dest, nom))
             for _, nom, dest in pieces_vf5(e)]
        print('   %-5s %2d / %d piece(s)%s'
              % (e['code'], sum(n), len(n), '' if all(n) else '   INCOMPLET'))
    return etat_lot([])


def poser_lot(lot, source, bases_seules=False, sans_bases=False):
    """Pose un LOT de decors. `lot` = [(modele, code, objset), ...].

    Les fichiers se posent un par un ; les deux bases sont chargees une fois,
    remplies pour tout le lot, et ecrites une fois.

    `bases_seules` refait UNIQUEMENT les deux bases, les fichiers etant deja
    poses : elles se deduisent des archives posees, donc les refaire ne coute
    que quelques secondes la ou recopier 382 Mo en coute plusieurs minutes.
    """
    src = os.path.join(SOURCES, source)
    if not os.path.isdir(src):
        print('source introuvable : %s' % src)
        return 1
    vus = set()
    for depuis, code, objset in lot:
        if len(code) != 3:
            print('REFUS : un code de decor fait TROIS lettres '
                  '(« %s » en a %d).' % (code, len(code)))
            return 1
        if code in vus:
            print('REFUS : le code « %s » revient deux fois dans le lot.'
                  % code)
            return 1
        vus.add(code)
        if not controler_longueurs(code, depuis):
            return 1

    # --- 1. les fichiers, un decor a la fois -------------------------------
    for i, (depuis, code, _) in enumerate([] if bases_seules else lot):
        print()
        print('=' * 72)
        print('[%d/%d] %s  ->  %s' % (i + 1, len(lot), depuis, code))
        print('=' * 72)
        r = poser_fichiers(code, depuis, src, source)
        if r:
            return r

    if sans_bases:
        return 0
    return poser_bases(lot)


def poser_bases(lot, lot_vf5=()):
    """Les deux bases, UNE fois, pour TOUT ce qui est pose.

    `lot` est celui de VF5 R, `[(modele, code, objset)]` ; `lot_vf5` celui du
    VF5 d'origine, les entrees de `variantes_vf5.entrees()`. Les deux lots
    partagent les memes bases : les poser l'un apres l'autre ferait que le
    second efface le premier, en silence -- c'est la lecon du 2026-09-10.
    """
    # --- 2. obj_db.bin, UNE FOIS pour tout le lot --------------------------
    print()
    print('--- obj_db.bin ---')
    o = obj_db.charger(os.path.join(EXTRAITS, 'obj_db.bin'))
    import variantes_5r
    for depuis, code, objset in lot:
        nom_jeu = 'STG%s' % code.upper()
        _, m = o.jeu('STG%s' % depuis.upper())
        if m is None:
            print('REFUS : le jeu d objets modele STG%s est introuvable'
                  % depuis.upper())
            return 2
        # LES OBJETS SONT CEUX DE L'ARCHIVE POSEE, PAS CEUX DU MODELE.
        #
        # `obj_db` decrit l'archive qu'on POSE. On y recopiait la declaration
        # du modele Final Showdown alors qu'on pose la geometrie de 2008 :
        # mesure du 2026-09-10 sur les dix-neuf, entre 47 et 196 objets
        # declares n'existaient pas dans l'archive, et jusqu'a 58 objets de
        # 2008 n'etaient PAS declares -- or ce sont ceux que ses propres
        # `.a3da` nomment. Un nom introuvable dans l'index global, c'est un
        # effet qui ne se lie a rien, en silence ; un rang declare mais absent,
        # c'est un chargement qui ne finit pas.
        objets = variantes_5r.objets_archive(code)
        if objets is None:
            print('REFUS : l archive posee de %s est illisible -- on ne peut '
                  'pas declarer ce qu on n a pas lu.' % code)
            return 2
        modele = o.objets_de(m[1])
        try:
            k = o.ajouter_jeu(nom_jeu, objset, 'stg%s' % code.lower())
        except ValueError as e:
            print('REFUS : %s' % e)
            return 2
        for r, nom in objets:
            o.ajouter_objet(objset, r, renommer(nom.upper(), depuis, code))
        print('   %-8s rang %-5d identifiant %-5d %3d objets lus dans '
              'l ARCHIVE POSEE (le modele STG%s en declarait %d), RENOMMES en '
              'STG%s_*'
              % (nom_jeu, k, objset, len(objets), depuis.upper(), len(modele),
                 code.upper()))
    # LE VF5 D'ORIGINE. Ses objets s'appellent comme sa SOURCE (`stgdjo_gnd`,
    # en minuscules chez ver.B) : on les renomme depuis la source, pas depuis
    # le modele -- pour `drb`, la source est `dur` et le modele `du1`. Les
    # quatre objsets de CIEL de Dural (`d1b`..`d4b`) n'ont pas de modele : ce
    # sont de simples jeux d'objets, que le descripteur nomme par identifiant.
    if lot_vf5:
        import variantes_vf5
        for code, objset, source in variantes_vf5.objsets_poses():
            objets = variantes_5r.objets_archive(code)
            if objets is None:
                print('REFUS : l archive posee de %s est illisible -- on ne '
                      'peut pas declarer ce qu on n a pas lu.' % code)
                return 2
            try:
                k = o.ajouter_jeu('STG%s' % code.upper(), objset,
                                  'stg%s' % code.lower())
            except ValueError as e:
                print('REFUS : %s' % e)
                return 2
            for r, nom in objets:
                o.ajouter_objet(objset, r, renommer(nom.upper(), source, code))
            print('   %-8s rang %-5d identifiant %-5d %3d objets lus dans '
                  'l ARCHIVE POSEE de ver.B (%s), RENOMMES en STG%s_*'
                  % ('STG%s' % code.upper(), k, objset, len(objets), source,
                     code.upper()))
    print('   (l index des noms d objets est GLOBAL et trie : un doublon '
          'rendrait l objset du modele)')
    dest = os.path.join(MEDIA, 'rom', 'objset', 'obj_db.bin')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    io.open(dest, 'wb').write(o.octets())
    print('   -> rom/objset/obj_db.bin (%d octets)' % os.path.getsize(dest))

    # --- 3. auth_3d_db.bin, UNE FOIS aussi ---------------------------------
    print()
    print('--- auth_3d_db.bin ---')
    a = a3d_db.charger(os.path.join(EXTRAITS, 'auth_3d_db.bin'))
    import farc as mod_farc
    # Les categories se clonent sur le MODELE FS (ses valeurs `STG<modele>_*`
    # deviennent `STG<code>_*`) et se filtrent sur l'archive POSEE -- deja
    # renommee depuis la source. Les variantes de Dural sans geometrie
    # (`d2b`..`d4b`) n'ont pas de categorie : leur descripteur nomme celles de
    # `drb`, exactement comme ver.B nomme `EFFSTGDUR` pour ses quatre.
    lot_a3d = [(depuis, code) for depuis, code, _ in lot]
    lot_a3d += [(e['modele'], e['code']) for e in lot_vf5
                if e['source'] is not None]
    for depuis, code in lot_a3d:
        for prefixe in ('STG', 'EFFSTG'):
            modele_cat = '%s%s' % (prefixe, depuis.upper())
            neuve = '%s%s' % (prefixe, code.upper())
            uids = a.uids_de(modele_cat)
            if not uids:
                print('   (%s n a pas de categorie -- rien a ajouter)'
                      % modele_cat)
                continue
            # ON NE DECLARE QUE CE QUE L'ARCHIVE POSEE CONTIENT.
            #
            # Un uid declare sans son `.a3da` est une promesse que le moteur
            # attend : `TaskEffectWall` (creneau 1) boucle sur
            # `FUN_180044640` jusqu'a ce que ses animations soient pretes.
            # La generation de 2008 n'a pas les memes que Final Showdown --
            # `aur` n'a ni `EFF_SAKU_BROKEN` ni les deux `BROKEN_SHADOW`.
            arch = os.path.join(MEDIA, 'rom', 'auth_3d', '%s.farc' % neuve)
            membres = set()
            if os.path.exists(arch):
                try:
                    membres = set(e['name']
                                  for e in mod_farc.Farc(arch).entries)
                except Exception:
                    membres = set()
            try:
                rang = a.ajouter_categorie(neuve)
            except ValueError as e:
                print('REFUS : %s' % e)
                return 2
            poses, sautes, declares = 0, [], set()
            prefixe_val = 'A'
            for kk in sorted(uids):
                valeur = renommer(uids[kk]['value'], depuis, code)
                nom = valeur.split()[-1]
                prefixe_val = valeur.rsplit(' ', 1)[0] or 'A'
                if membres and nom + '.a3da' not in membres:
                    sautes.append(nom)
                    continue
                a.ajouter_uid(neuve, valeur, uids[kk].get('size', '0'))
                declares.add(nom + '.a3da')
                poses += 1
            # ET CE QUE 2008 A EN PLUS (2026-09-11)
            #
            # La liste du MODELE n'est pas l'inventaire de l'archive. Sur le
            # sanctuaire d'Aoi, `EFFSTGJIN` (Final Showdown) declare sept
            # animations et l'archive de 2008 en porte dix : `EFF_ARUKI_A`,
            # `_B`, `_C`, `EFF_TALK` et `EFF_IKE` n'entraient donc JAMAIS dans
            # la base, et rien ne pouvait les jouer -- c'est ce que Frederic
            # voyait : « il manque les personnages en 3D dans le decor ».
            #
            # Une base doit decrire ce qui est POSE. Declarer un uid ne le joue
            # pas : c'est la liste d'animations du decor (table 0x18034FD20)
            # qui decide, et elle passe par ANIMATIONS_VALIDEES.
            #
            # `size` n'est pas la taille du fichier : c'est exactement le
            # `play_control.size` du `.a3da` -- mesure sur les douze uid
            # d'`EFFSTGAR5` (ARUKI 3901, ARUKI_B 7021, TOIKI 30, KANKYAKU 241).
            # On le LIT, on ne le devine pas.
            en_plus = []
            if membres:
                arc = mod_farc.Farc(arch)
                tailles = dict((e['name'], e) for e in arc.entries)
                for m in sorted(membres - declares):
                    if not m.endswith('.a3da'):
                        continue
                    nom = m[:-5]
                    try:
                        texte = arc.read(tailles[m]).decode('latin-1', 'replace')
                    except Exception:
                        continue
                    trouve = re.search(r'play_control\.size=([0-9.]+)', texte)
                    if trouve is None:
                        continue          # pas de duree lisible : on n ose pas
                    taille = str(int(float(trouve.group(1))))
                    a.ajouter_uid(neuve, '%s %s' % (prefixe_val, nom), taille)
                    en_plus.append(nom.split('_', 1)[-1])
                    poses += 1
            print('   %-12s rang %-5d %2d uid(s) sur %d de %s%s%s'
                  % (neuve, rang, poses, len(uids), modele_cat,
                     '' if not sautes else
                     '   (sans .a3da en 2008 : %s)' % ' '.join(sautes),
                     '' if not en_plus else
                     '   (+%d que 2008 a en plus : %s)'
                     % (len(en_plus), ' '.join(en_plus))))
    dest = os.path.join(MEDIA, 'rom', 'auth_3d', 'auth_3d_db.bin')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    io.open(dest, 'wb').write(a.texte().encode('ascii'))
    print('   -> rom/auth_3d/auth_3d_db.bin (%d octets)' % os.path.getsize(dest))

    # --- 4. les deux bases dans le .par, chacune a sa facon ----------------
    print()
    print('--- le .par : une base MASQUEE, une base ECRITE DEDANS ---')
    r = par('--masquer', [n for n, _ in BASES if n != BASE_DANS_LE_PAR])
    if r:
        return r
    import par_ecrire
    chemin = os.path.join(MEDIA, dict(BASES)[BASE_DANS_LE_PAR],
                          BASE_DANS_LE_PAR)
    return par_ecrire.remplacer(BASE_DANS_LE_PAR, chemin)


def poser(code, depuis, source, objset):
    return poser_lot([(depuis, code, objset)], source)


def retirer_lot(codes):
    print('--- les dix pieces de chacun des %d decors ---' % len(codes))
    for code in codes:
        n = 0
        for _, nom, dest in toutes_les_pieces(code):
            p = os.path.join(MEDIA, 'rom', dest, nom)
            if os.path.exists(p):
                os.remove(p)
                n += 1
        print('   %-5s %d piece(s) retiree(s)' % (code, n))
    print()
    print('--- les deux bases ---')
    for nom, sous in BASES:
        p = os.path.join(MEDIA, sous, nom)
        if os.path.exists(p):
            os.remove(p)
            print('   retire %s' % nom)
    print()
    import par_ecrire
    r = par_ecrire.rendre(BASE_DANS_LE_PAR)
    if r == 2:
        print('   (rien a rendre pour %s dans le .par)' % BASE_DANS_LE_PAR)
    elif r:
        return r
    return par('--rendre', [n for n, _ in BASES if n != BASE_DANS_LE_PAR])


def retirer(code):
    return retirer_lot([code])


def etat_lot(codes):
    print('--- les dix pieces de chacun des %d decors ---' % len(codes))
    for code in codes:
        n = [os.path.exists(os.path.join(MEDIA, 'rom', dest, nom))
             for _, nom, dest in toutes_les_pieces(code)]
        print('   %-5s %2d / %d piece(s)%s'
              % (code, sum(n), len(n), '' if all(n) else '   INCOMPLET'))
    print('--- les deux bases ---')
    for nom, sous in BASES:
        p = os.path.join(MEDIA, sous, nom)
        print('   %-26s %s' % (nom, ('%d o' % os.path.getsize(p))
                               if os.path.exists(p) else 'absent'))
    print('--- le .par ---')
    import par_ecrire
    par_ecrire.etat(BASE_DANS_LE_PAR)
    return par('--lister', [n for n, _ in BASES if n != BASE_DANS_LE_PAR])


def etat(code):
    return etat_lot([code])


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    depuis = argv[argv.index('--depuis') + 1] if '--depuis' in argv else 'djo'
    source = argv[argv.index('--source') + 1] if '--source' in argv else 'VF5R'
    objset = int(argv[argv.index('--objset') + 1], 0) if '--objset' in argv else 0

    # LE VF5 D'ORIGINE -- `--poser-lot vf5` ou `5r+vf5`. Les BASES decrivent
    # tout ce qui est pose : `5r+vf5` les refait pour les deux lots, `vf5`
    # seul n'y met que ver.B. Le lot est dans `variantes_vf5.py`.
    for action in ('--poser-lot', '--retirer-lot', '--etat-lot'):
        if action not in argv:
            continue
        i = argv.index(action) + 1
        quoi = argv[i].lower() if i < len(argv) else '5r'
        if 'vf5' not in quoi.split('+'):
            break
        import variantes_5r
        import variantes_vf5
        # le monde VF5 (5r+vf5) porte aussi les quatre Dural de VF5 R, aux
        # indices 82-85 (voir variantes_5r.DURAL_5R)
        lot5r = ([(m, c, o) for m, c, _, o in variantes_5r.lot(dural=True)]
                 if '5r' in quoi.split('+') else [])
        if action == '--poser-lot':
            # Les fichiers de VF5 R ne se reposent que s'il en manque : ce
            # sont 400 Mo, et ils ne changent pas.
            manque_5r = [c for _, c, _ in lot5r if not os.path.exists(
                os.path.join(MEDIA, 'rom', 'objset', 'stg%s.farc' % c))]
            if manque_5r and '--bases-seules' not in argv:
                r = poser_lot([x for x in lot5r if x[1] in manque_5r],
                              variantes_5r.SOURCE, sans_bases=True)
                if r:
                    return r
            return poser_lot_vf5(lot5r, bases_seules='--bases-seules' in argv)
        codes = []
        for e in variantes_vf5.entrees():
            codes.append(e)
        if action == '--retirer-lot':
            return retirer_lot_vf5(codes, [c for _, c, _ in lot5r])
        return etat_lot_vf5(codes)

    # LE LOT : la table est dans `variantes_5r.py`, et nulle part ailleurs.
    for action, f in (('--poser-lot', poser_lot),
                      ('--retirer-lot', retirer_lot),
                      ('--etat-lot', etat_lot)):
        if action not in argv:
            continue
        import variantes_5r
        fautes = variantes_5r.controler()
        if fautes:
            print('REFUS : la table de variantes_5r.py a %d faute(s) :'
                  % len(fautes))
            for x in fautes:
                print('   . %s' % x)
            return 1
        lot = variantes_5r.DECORS_5R
        if f is poser_lot:
            return poser_lot([(m, c, o) for m, c, _, o in lot],
                             variantes_5r.SOURCE,
                             bases_seules='--bases-seules' in argv)
        return f([c for _, c, _, _ in lot])
    for action, f in (('--etat', etat), ('--retirer', retirer),
                      ('--poser', poser)):
        if action in argv:
            i = argv.index(action) + 1
            if i >= len(argv):
                print('%s attend un code de decor a trois lettres' % action)
                return 1
            code = argv[i]
            if f is poser:
                if not objset:
                    print('--poser demande --objset <identifiant>. '
                          '`py -3 tools/obj_db.py --libres` donne les plages.')
                    return 1
                return poser(code, depuis, source, objset)
            return f(code)
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
