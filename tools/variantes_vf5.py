# -*- coding: utf-8 -*-
r"""LA TABLE DES DECORS DU VIRTUA FIGHTER 5 D'ORIGINE (ver.B) AJOUTES.

Le pendant de `variantes_5r.py`, et pour la meme raison : `decor_neuf.py` pose
les fichiers, `patch_moteur.py` remplit le binaire, `controle_decors_vf5.py`
verifie -- les trois lisent CE fichier, et le lot ne vit qu'ici.

Source : `extracted/decors/VF5_VERB` (VF5 ver.B, build 20070530), et l'ELF du
jeu, `extracted/LIND_VF5/id/disk0/vf5`, dont on LIT la table des descripteurs.

CE QUE ver.B APPORTE

  . les dix-sept lieux de 2007, dans leur premiere version ;
  . et SURTOUT le decor de Dural d'origine : `stgdur.farc`, 35,7 Mo, que plus
    aucune version ne contient. ver.B en fait QUATRE variantes -- la meme
    geometrie (`stgdur`) sous quatre ciels (`stgdu1`..`stgdu4`, qui ne sont PAS
    des decors mais des objsets de ciel) et quatre eclairages (`dur`, `du2`,
    `du3`, `du4`). Lu dans le descripteur de ver.B : `+0x08` = `stgdur`,
    `+0x0C` = l'objset du ciel, `+0x14` = `STGDU<n>_SKY`.

CE QUI N'EST PAS COMME VF5 R, ET QUI A TOUT DECIDE (mesure du 2026-09-11)

1. LES IDENTIFIANTS DE TEXTURE. VF5 R numerote ses textures comme Final
   Showdown : sur les dix-neuf objsets poses, CHAQUE identifiant connu de la
   `tex_db` de FS y designe une texture du meme decor. ver.B, non :

       3 975 textures de decor, 3 277 dont l'identifiant designe AUTRE CHOSE
       chez FS -- `F_VF5E_DJO00_IK_DOWNKEM_000` porte le numero de
       `F_VF5E_BAR00_HR_PERA_102`, `stgdur` celui des lunettes de Wolf.

   Poser ces objsets tels quels, c'est deux textures pour un numero. On les
   RENUMEROTE : un nom que FS connait prend le numero de FS ; un nom que FS ne
   connait pas (1 381) prend un numero LIBRE, pris dans les trous de la
   `tex_db` de FS et hors de ceux que VF5 R utilise. Les identifiants d'un
   objset sont en DEUX endroits, et deux seulement -- la liste de l'en-tete
   (`+0x1C`, `+0x20`) et les huit emplacements de chaque materiau
   (`+0x14 + t*0x78 + 4`) : verifie sur quatre archives, AUCUN emplacement
   non vide ne sort de la liste. Les `.a3da` de ver.B ne nomment aucune
   texture (courbes, objets, lumieres, cameras) : rien d'autre a toucher.

2. LES RANGS DES OBJETS. Ceux de ver.B ne sont pas ceux de FS (`djo` : sol
   114 chez FS, 0 chez ver.B). Les cinq objets du descripteur viennent donc du
   descripteur de ver.B, relu dans l'ELF et controle PAR NOM :

       ver.B  +0x10 GND  +0x14 SKY  +0x18 SDW  +0x1C (vide)  +0x20 REFLECT
       FS     +0x14 GND  +0x18 RING +0x1C SKY  +0x20 SDW     +0x24 REFLECT

   ver.B n'a pas d'objet RING : le sol le porte. `-1` est une valeur que FS
   ecrit lui-meme (`tst`, `trm`...).

LE CODE A TROIS LETTRES : `<1re lettre><3e lettre>b`, b pour ver.B -- unique,
et aucun code du jeu ni du lot VF5 R ne finit par b. Les variantes de Dural :
`drb` (dur), `d2b` `d3b` `d4b` ; le ciel de `drb` a son propre objset, `d1b`.

L'INDICE ET L'OBJSET : a la suite de VF5 R (42..60), donc 61..81 ; objsets
6169..6190 dans la plage libre 6150..6349.
"""
import io
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
SOURCE = 'VF5_VERB'
SRC = os.path.join(RACINE, 'extracted', 'decors', SOURCE)
ELF = os.path.join(RACINE, 'extracted', 'LIND_VF5', 'id', 'disk0', 'vf5')
TEX_DB_VERB = os.path.join(SRC, '_db', 'tex_db.bin')
TEX_DB_FS = os.path.join(RACINE, 'extracted', 'tex_db.bin')
MEDIA = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media')

# (modele FS, source ver.B, code, indice, objset)
DECORS_VF5 = (
    ('djo', 'djo', 'dob', 61, 6169),
    ('ban', 'ban', 'bnb', 62, 6170),
    ('ter', 'ter', 'trb', 63, 6171),
    ('nyc', 'nyc', 'ncb', 64, 6172),
    ('cas', 'cas', 'csb', 65, 6173),
    ('riv', 'riv', 'rvb', 66, 6174),
    ('jin', 'jin', 'jnb', 67, 6175),
    ('sin', 'sin', 'snb', 68, 6176),
    ('umi', 'umi', 'uib', 69, 6177),
    ('hai', 'hai', 'hib', 70, 6178),
    ('are', 'are', 'aeb', 71, 6179),
    ('slk', 'slk', 'skb', 72, 6180),
    ('yuk', 'yuk', 'ykb', 73, 6181),
    ('tak', 'tak', 'tkb', 74, 6182),
    ('aur', 'aur', 'arb', 75, 6183),
    ('bar', 'bar', 'brb', 76, 6184),
    ('tan', 'tan', 'tnb', 77, 6185),
    ('du1', 'dur', 'drb', 78, 6186),        # la GEOMETRIE de Dural, 35,7 Mo
)

# LES QUATRE VARIANTES DE DURAL DE ver.B -- une geometrie, quatre ciels.
# (code, indice, source d'eclairage, source du ciel, code du ciel, objset du
#  ciel). `drb` est aussi dans DECORS_VF5 : c'est lui qui porte la geometrie.
DURAL_VF5 = (
    ('drb', 78, 'dur', 'du1', 'd1b', 6187),
    ('d2b', 79, 'du2', 'du2', 'd2b', 6188),
    ('d3b', 80, 'du3', 'du3', 'd3b', 6189),
    ('d4b', 81, 'du4', 'du4', 'd4b', 6190),
)
DURAL_MODELE = 'du1'
DURAL_GEOMETRIE = 'drb'

GENERATION = 'VIRTUA FIGHTER 5'
# Les libelles des quatre Dural : leur NOM n'est pas devine -- Frederic a
# nomme lui-meme ceux de Final Showdown. En attendant, la generation et le
# numero de ver.B.
DURAL_LIBELLES = ('VIRTUA FIGHTER 5 - 1', 'VIRTUA FIGHTER 5 - 2',
                  'VIRTUA FIGHTER 5 - 3', 'VIRTUA FIGHTER 5 - 4')

# LA TABLE DES DESCRIPTEURS DE ver.B, dans son ELF (x86-32, pas 0x70). Trouvee
# par le pointeur vers « STGDJO » (0x852F6F0) et parcourue jusqu'aux bornes :
# 28 entrees, de `tst` a `trs`.
VERB_DESC_VA = 0x852F220
VERB_DESC_PAS = 0x70
VERB_DESC_N = 28
VERB_RODATA = (0x08521BA0, 0x4D9BA0, 0x11F9D4)       # va, offset, taille

# Correspondance des champs d'objets, ver.B -> FS (voir l'en-tete)
ROLES_FS = ('gnd', 'ring', 'sky', 'sdw', 'reflect')
VERB_ROLE = {'gnd': 0x10, 'sky': 0x14, 'sdw': 0x18, 'reflect': 0x20}

MATERIAU_PAS = 0x4B0
TEXTURE_PAS = 0x78
TEXTURES_PAR_MATERIAU = 8


# ---------------------------------------------------------------------------
# LE LOT, sous une forme que les trois outils partagent
# ---------------------------------------------------------------------------
def entrees():
    """Une entree par INDICE ajoute. Chaque champ est ecrit, rien n'est deduit
    ailleurs.

        modele    le decor FS dont on clone le descripteur et les tables
        code      le code a trois lettres (les fichiers d'eclairage)
        indice    l'indice dans la table des decors
        objset    l'objset de la GEOMETRIE (partage par les quatre Dural)
        geo       le code de l'archive de geometrie (`stg<geo>.farc`)
        source    la source ver.B de la geometrie, ou None (variante Dural)
        eclairage la source ver.B des cinq fichiers d'eclairage
        verb      la cle du descripteur de ver.B a relire
        a3d       le nom auth_3d du descripteur
        eff       le code de la categorie d'effets (`EFFSTG<eff>`)
        coli      le code de la collision (`rom/STG<coli>_COLI.000.bin`)
        ciel      (code, objset, source) de l'objset de ciel, ou None
    """
    out = []
    dural = dict((e[0], e) for e in DURAL_VF5)
    for modele, source, code, indice, objset in DECORS_VF5:
        e = dict(gen='verb', modele=modele, code=code, indice=indice,
                 objset=objset, geo=code, source=source, src_geo=source,
                 eclairage=source, verb=source, cle=source,
                 a3d='STG%s' % code.upper(), eff=code, coli=code, ciel=None)
        if code in dural:
            _, _, ecl, s_ciel, c_ciel, o_ciel = dural[code]
            e['eclairage'] = ecl
            e['ciel'] = (c_ciel, o_ciel, s_ciel)
        out.append(e)
    objset_geo = dict((e[2], e[4]) for e in DECORS_VF5)[DURAL_GEOMETRIE]
    for code, indice, ecl, s_ciel, c_ciel, o_ciel in DURAL_VF5:
        if code == DURAL_GEOMETRIE:
            continue
        out.append(dict(gen='verb', modele=DURAL_MODELE, code=code,
                        indice=indice, objset=objset_geo,
                        geo=DURAL_GEOMETRIE, source=None,
                        src_geo=dict((e[2], e[1]) for e in DECORS_VF5)[
                            DURAL_GEOMETRIE],
                        eclairage=ecl, verb=ecl, cle=ecl,
                        a3d='STG%s' % code.upper(),
                        eff=DURAL_GEOMETRIE, coli=DURAL_GEOMETRIE,
                        ciel=(c_ciel, o_ciel, s_ciel)))
    return sorted(out, key=lambda e: e['indice'])


def par_code(code):
    for e in entrees():
        if e['code'] == code:
            return e
    return None


def objsets_poses():
    """Tous les objsets que le lot pose : [(code, objset, source ver.B)]."""
    out = []
    for e in entrees():
        if e['source'] is not None:
            out.append((e['geo'], e['objset'], e['source']))
        if e['ciel'] is not None:
            out.append((e['ciel'][0], e['ciel'][1], e['ciel'][2]))
    return out


def controler():
    fautes = []
    vus = {'code': set(), 'indice': set(), 'objset': set()}
    for e in entrees():
        for k in ('code', 'indice'):
            if e[k] in vus[k]:
                fautes.append('%s %r en double' % (k, e[k]))
            vus[k].add(e[k])
        if len(e['code']) != 3:
            fautes.append('« %s » ne fait pas trois caracteres' % e['code'])
        if e['indice'] < 42:
            fautes.append('l indice %d est reserve' % e['indice'])
    for code, objset, _ in objsets_poses():
        if objset in vus['objset']:
            fautes.append('objset %d en double' % objset)
        vus['objset'].add(objset)
        if len(code) != 3:
            fautes.append('« %s » ne fait pas trois caracteres' % code)
    try:
        import variantes_5r
        i5 = set(x[2] for x in variantes_5r.lot(True))
        o5 = set(x[3] for x in variantes_5r.lot(True))
        c5 = set(x[1] for x in variantes_5r.lot(True))
        for e in entrees():
            if e['indice'] in i5:
                fautes.append('indice %d deja pris par VF5 R' % e['indice'])
            if e['code'] in c5:
                fautes.append('code %s deja pris par VF5 R' % e['code'])
        for _, objset, _ in objsets_poses():
            if objset in o5:
                fautes.append('objset %d deja pris par VF5 R' % objset)
    except ImportError:
        pass
    return fautes


# ---------------------------------------------------------------------------
# LE DESCRIPTEUR DE ver.B, relu dans son ELF
# ---------------------------------------------------------------------------
def _elf():
    return open(ELF, 'rb').read()


def descripteurs_verb():
    """{code ver.B: {...}} -- `djo`, `dur`, `du2`... pour les 28 entrees.

    Rend les objets PAR ROLE (identifiants empaquetes de ver.B), le second
    objset, et les trois textures de reflet d'objectif (`+0x28..+0x30`).
    """
    d = _elf()
    ro_va, ro_off, ro_sz = VERB_RODATA

    def off(va):
        if not ro_va <= va < ro_va + ro_sz:
            raise ValueError('0x%X hors de .rodata' % va)
        return va - ro_va + ro_off

    def chaine(va):
        o = off(va)
        return d[o:d.index(b'\x00', o)].decode('ascii')

    out = {}
    for i in range(VERB_DESC_N):
        e = d[off(VERB_DESC_VA + i * VERB_DESC_PAS):
              off(VERB_DESC_VA + i * VERB_DESC_PAS) + VERB_DESC_PAS]
        nom = chaine(struct.unpack_from('<I', e, 0)[0])
        if not nom.startswith('STG'):
            raise ValueError('entree %d de ver.B : %r n est pas un nom de '
                             'decor -- la table n est pas ou on la croit'
                             % (i, nom))
        o1, o2 = struct.unpack_from('<2i', e, 0x08)
        objets = dict((r, struct.unpack_from('<I', e, v)[0])
                      for r, v in VERB_ROLE.items())
        out[nom[3:].lower()] = dict(
            rang=i, nom=nom, eff=chaine(struct.unpack_from('<I', e, 4)[0]),
            objset=o1, objset2=o2, objets=objets,
            refract=struct.unpack_from('<I', e, 0x24)[0],
            flares=struct.unpack_from('<3I', e, 0x28),
            coli=chaine(struct.unpack_from('<I', e, 0x40)[0]))
    return out


# ---------------------------------------------------------------------------
# LES TACHES D'EFFET DE ver.B, relues dans son ELF (2026-09-11)
#
# Meme forme que `0x18034D570` chez FS : 0x60 par decor, `+0x00` les objsets
# en plus, `+0x20` les taches, fins -1. Trouvee par la liste de `slk`
# (`[2, 12, 7, 13, 16]` en 0x85FFAE0), referencee par le code en 0x343514.
#
# POURQUOI ELLE ET PAS CELLE DU MODELE : la table de VF5 R, relue de la meme
# facon dans `vf5r.bin`, donne pour `hai` **WALL seul** -- pas de THUNDER.
# C'est exactement ce que Frederic a vu a l'ecran sur hi5 (« des eclairs qui
# n'ont rien a faire dans ce variant ») et qu'on a du retirer a la main. Une
# generation a SES effets. ver.B, lui, a THUNDER sur `hai`, pas de SNOW sur
# `yuk` (SNOW_RING a la place), YUKA seul sur `ban`...
#
# Les numeros de ver.B sont ceux de VF5 R (19 taches, pas de MOVE) : on les
# traduit PAR NOM, les noms etant lus dans le tableau de pointeurs de l'ELF.
# Le `+0x00` de ver.B nomme l'objset 45, `EFFCMN` -- que FS charge TOUJOURS
# (`0x18034D510` = [21 = EFFCMN]). Rien a ajouter.
VERB_TACHES_VA = 0x85FF520
VERB_TACHES_PAS = 0x60


def taches_verb():
    """{code ver.B: [taches, NUMEROTEES COMME FS]}."""
    d = _elf()
    ro_va, ro_off, ro_sz = VERB_RODATA

    def off(va):
        return va - ro_va + ro_off

    # les noms : le tableau de pointeurs vers « EFFECT_HIT »...
    nom0 = d.find(b'EFFECT_HIT\x00')
    va0 = nom0 - ro_off + ro_va
    p = d.find(struct.pack('<I', va0))
    if nom0 < 0 or p < 0:
        raise ValueError('ver.B : le tableau des noms de taches est introuvable')
    noms = []
    while True:
        v = struct.unpack_from('<I', d, p + 4 * len(noms))[0]
        if not ro_va <= v < ro_va + ro_sz:
            break
        s = d[off(v):d.index(b'\x00', off(v))]
        if not s.startswith(b'EFFECT_'):
            break
        noms.append(s.decode())
    import patch_moteur
    fs = dict((n, i) for i, n in enumerate(patch_moteur.EFFETS_NOMS))
    rangs = dict((x['rang'], k) for k, x in descripteurs_verb().items())
    out = {}
    for i in range(VERB_DESC_N):
        e = d[off(VERB_TACHES_VA + i * VERB_TACHES_PAS):
              off(VERB_TACHES_VA + i * VERB_TACHES_PAS) + VERB_TACHES_PAS]
        t = []
        for x in struct.unpack_from('<16i', e, 0x20):
            if x == -1:
                break
            if not 0 <= x < len(noms):
                raise ValueError('ver.B : tache %d hors des %d noms' % (x,
                                                                        len(noms)))
            t.append(fs[noms[x]])
        out[rangs[i]] = t
    return out


# ---------------------------------------------------------------------------
# LES MURS DE ver.B, relus dans son ELF (2026-09-11)
#
# Cloner le mur du modele FS ne marche pas pour ver.B : ses grillages
# (`EFF_SAKU`...) sont des ajouts de VF5 R, et ver.B n'en a pas un seul. Mais
# ver.B a SA table, qui dit ses propres murs -- 14 entrees de 0x14, trouvees
# par le pointeur vers les morceaux de `djo` (0x86012C0) :
#
#     +0x00 indice   +0x04 morceaux   +0x08 uid   +0x0C paires   +0x10 morceaux 2
#
# et elle a la FORME de celle de FS, a deux differences pres, mesurees :
#
#   . un morceau fait 0x28 : {objet, x y z, rx ry rz, sx sy sz}. FS en fait
#     0x2C : il a insere un ENTIER a +4 -- 0 sur 293 morceaux, 1 sur 15.
#     ver.B n'a pas ce champ : on y met 0, la valeur de tous les morceaux de
#     `djo` chez FS (dont les positions sont celles de ver.B a l'unite pres) ;
#   . FS a ajoute trois champs (+0x28 +0x30 +0x38 : grillage anime, objets
#     cassables) que ver.B n'a pas : nuls.
#
# Les objets sont des identifiants empaquetes de ver.B, les uid des numeros de
# SA `auth_3d_db` : on rend les uid par leur NOM, le patcheur les retrouve dans
# la base posee.
VERB_MURS_VA = 0x8600480
VERB_MURS_PAS = 0x14
VERB_MORCEAU_PAS = 0x28


def murs_verb():
    """{code ver.B: {'pieces': [(objet, 9 flottants bruts)], 'p20': [...],
    'uids': [nom], 'paires': [(intact, casse, nom uid, nom uid)]}}."""
    import a3d_db
    d = _elf()
    ro_va, ro_off, ro_sz = VERB_RODATA

    def off(va):
        if not ro_va <= va < ro_va + ro_sz:
            raise ValueError('ver.B : 0x%X hors de .rodata' % va)
        return va - ro_va + ro_off

    base = a3d_db.charger(os.path.join(SRC, '_db', 'auth_3d_db.bin')).uids()

    def nom_uid(u):
        v = base.get(u, {}).get('value')
        if v is None:
            raise ValueError('ver.B : uid %d absent de sa auth_3d_db' % u)
        return v

    def morceaux(p):
        out = []
        while True:
            o = off(p) + len(out) * VERB_MORCEAU_PAS
            obj = struct.unpack_from('<I', d, o)[0]
            if obj == 0xFFFFFFFF:
                return out
            out.append((obj, d[o + 4:o + VERB_MORCEAU_PAS]))
            if len(out) > 256:
                raise ValueError('ver.B : morceaux sans fin en 0x%X' % p)

    rangs = dict((x['rang'], k) for k, x in descripteurs_verb().items())
    out = {}
    for k in range(64):
        e = struct.unpack_from('<i4I', d, off(VERB_MURS_VA + k * VERB_MURS_PAS))
        if e[0] == -1:
            break
        if not 0 <= e[0] < VERB_DESC_N or not e[1]:
            raise ValueError('ver.B : entree de mur %d incoherente' % k)
        uids, paires = [], []
        if e[2]:
            while True:
                u = struct.unpack_from('<i', d, off(e[2]) + 4 * len(uids))[0]
                if u == -1:
                    break
                uids.append(nom_uid(u))
        if e[3]:
            while True:
                q = struct.unpack_from('<IIii', d, off(e[3]) + 0x10 * len(paires))
                if q[0] == 0xFFFFFFFF:
                    break
                paires.append((q[0], q[1],
                               nom_uid(q[2]) if q[2] != -1 else None,
                               nom_uid(q[3]) if q[3] != -1 else None))
        out[rangs[e[0]]] = dict(pieces=morceaux(e[1]),
                                p20=morceaux(e[4]) if e[4] else None,
                                uids=uids, paires=paires)
    return out


# ---------------------------------------------------------------------------
# LES ANIMATIONS D'EFFET DE ver.B (2026-09-11)
#
# La table de `TaskEffectAuth3D` : {indice, pointeur} de 8 octets, 18
# entrees, fin -1, en 0x86001E0 -- trouvee par la liste de `djo`
# (HATA FIRE FIRE_REFLECT, en 0x86002B8). Elle dit ce que ver.B JOUAIT sur
# chaque decor : les marcheurs d'Aoi (ARUKI_A/B/C, TALK -- ceux que Frederic
# a valides sur jn5), les spectateurs de Lau (KANKYAKU), le feu de Goh...
# C'est la reponse que `ANIMATIONS_VALIDEES` attend pour VF5 R : ici, le
# binaire la donne, il n'y a rien a deviner ni a essayer une par une.
VERB_ANIMS_VA = 0x86001E0


def animations_verb():
    """{code ver.B: [valeurs auth_3d, 'A STGDJO_EFF_FIRE'...]}."""
    import a3d_db
    d = _elf()
    ro_va, ro_off, ro_sz = VERB_RODATA

    def off(va):
        if not ro_va <= va < ro_va + ro_sz:
            raise ValueError('ver.B : 0x%X hors de .rodata' % va)
        return va - ro_va + ro_off

    base = a3d_db.charger(os.path.join(SRC, '_db', 'auth_3d_db.bin')).uids()
    rangs = dict((x['rang'], k) for k, x in descripteurs_verb().items())
    out = {}
    for k in range(64):
        i, p = struct.unpack_from('<iI', d, off(VERB_ANIMS_VA + 8 * k))
        if i == -1:
            break
        if not 0 <= i < VERB_DESC_N:
            raise ValueError('ver.B : entree d animations %d incoherente' % k)
        noms = []
        while True:
            u = struct.unpack_from('<i', d, off(p) + 4 * len(noms))[0]
            if u == -1:
                break
            v = base.get(u, {}).get('value')
            if v is None:
                raise ValueError('ver.B : uid %d absent de sa base' % u)
            noms.append(v)
        out[rangs[i]] = noms
    return out


# ---------------------------------------------------------------------------
# LES TEXTURES : renumerotation par NOM
# ---------------------------------------------------------------------------
def _tex_db(chemin):
    """{identifiant: nom}, lecture tolerante (celle de ver.B a un bourrage de
    24 octets 0x90 en fin, que `tex_db.py` refuse)."""
    d = open(chemin, 'rb').read()
    n, t = struct.unpack_from('<2I', d, 0)
    out = {}
    for k in range(n):
        i, o = struct.unpack_from('<2I', d, t + k * 8)
        out[i] = d[o:d.index(b'\x00', o)].decode('latin-1')
    return out


def _ids_textures_obj(octets):
    nb, = struct.unpack_from('<I', octets, 0x20)
    off, = struct.unpack_from('<I', octets, 0x1C)
    return list(struct.unpack_from('<%dI' % nb, octets, off))


def _obj_de_farc(chemin):
    import farc
    f = farc.Farc(chemin)
    for e in f.entries:
        if e['name'].endswith('_obj.bin'):
            return f.read(e)
    raise ValueError('%s : pas de *_obj.bin' % chemin)


def ids_textures_5r():
    """Les identifiants de texture des archives de VF5 R -- le pot neuf les
    evite. Mis en cache : dix-neuf archives ne se decompriment pas a chaque
    fois."""
    import json
    import variantes_5r
    cache = os.path.join(RACINE, 'extracted', '_tex_ids_5r.json')
    src = os.path.join(RACINE, 'extracted', 'decors', 'VF5R', 'objset')
    archives = sorted(os.path.join(src, 'stg%s.farc' % m)
                      for m, _, _, _ in variantes_5r.DECORS_5R)
    archives = [a for a in archives if os.path.exists(a)]
    empreinte = [[os.path.basename(a), os.path.getsize(a)] for a in archives]
    if os.path.exists(cache):
        try:
            c = json.load(open(cache))
            if c.get('empreinte') == empreinte:
                return set(c['ids'])
        except Exception:
            pass
    ids = set()
    for a in archives:
        ids.update(_ids_textures_obj(_obj_de_farc(a)))
    json.dump({'empreinte': empreinte, 'ids': sorted(ids)}, open(cache, 'w'))
    return ids


_CARTE = None


def carte_textures():
    """{nom de texture ver.B: identifiant neuf}, pour TOUT le lot.

    DETERMINISTE : le patcheur et le controle la recalculent et tombent sur
    les memes numeros que `decor_neuf.py` a ecrits. Rend aussi `(vb, fs)` :
    les deux `tex_db` lues.
    """
    global _CARTE
    if _CARTE is not None:
        return _CARTE
    vb = _tex_db(TEX_DB_VERB)
    fs = _tex_db(TEX_DB_FS)
    fs_nom = {}
    for i, n in fs.items():
        fs_nom.setdefault(n, i)
    noms = set()
    for code, _, source in objsets_poses():
        ch = os.path.join(SRC, 'objset', 'stg%s.farc' % source)
        for i in _ids_textures_obj(_obj_de_farc(ch)):
            if i not in vb:
                raise ValueError('%s : la texture %d n est pas dans la tex_db '
                                 'de ver.B' % (source, i))
            noms.add(vb[i])
    carte = {}
    neufs = sorted(n for n in noms if n not in fs_nom)
    for n in noms:
        if n in fs_nom:
            carte[n] = fs_nom[n]
    pris = set(fs) | ids_textures_5r()
    haut = max(fs)
    pot = (i for i in range(1, haut) if i not in pris)
    for n in neufs:
        try:
            carte[n] = next(pot)
        except StopIteration:
            raise ValueError('plus de numeros libres sous %d' % haut)
    _CARTE = (carte, vb, fs)
    return _CARTE


def renumeroter_obj(octets):
    """Rend (octets neufs, nombre de textures, nombre d'emplacements
    reecrits). REFUSE (ValueError) si un emplacement de materiau nomme une
    texture qui n'est pas dans la liste de l'objset : on ne reecrit pas ce
    qu'on n'a pas compris."""
    carte, vb, _ = carte_textures()
    b = bytearray(octets)
    nb, = struct.unpack_from('<I', b, 0x20)
    off_tex, = struct.unpack_from('<I', b, 0x1C)
    anciens = list(struct.unpack_from('<%dI' % nb, b, off_tex))
    neuf_de = {}
    for i in anciens:
        neuf_de[i] = carte[vb[i]]
    if len(set(neuf_de.values())) != len(set(anciens)):
        raise ValueError('deux textures differentes recoivent le meme numero')
    for k, i in enumerate(anciens):
        struct.pack_into('<I', b, off_tex + k * 4, neuf_de[i])
    nobj, = struct.unpack_from('<I', b, 0x04)
    off_obj, = struct.unpack_from('<I', b, 0x0C)
    emplacements = 0
    for k in range(nobj):
        po, = struct.unpack_from('<I', b, off_obj + k * 4)
        nmat, offm = struct.unpack_from('<2I', b, po + 0x20)
        if nmat > 4096 or po + offm + nmat * MATERIAU_PAS > len(b):
            raise ValueError('objet %d : %d materiaux a +0x%X, incoherent'
                             % (k, nmat, offm))
        for j in range(nmat):
            m = po + offm + j * MATERIAU_PAS
            for t in range(TEXTURES_PAR_MATERIAU):
                o = m + 0x14 + t * TEXTURE_PAS + 4
                v, = struct.unpack_from('<I', b, o)
                if v == 0xFFFFFFFF:
                    continue
                if v not in neuf_de:
                    raise ValueError('objet %d materiau %d : texture %d hors '
                                     'de la liste de l objset' % (k, j, v))
                struct.pack_into('<I', b, o, neuf_de[v])
                emplacements += 1
    return bytes(b), nb, emplacements


def ecrire_objset(source, code, dest):
    """Pose `stg<source>.farc` de ver.B sous `dest`, membres renommes
    `stg<code>_*`, textures renumerotees. Le `_tex.bin` est recopie tel quel,
    COMPRIME : on ne recomprime que l'`_obj.bin`, avec l'en-tete gzip que SEGA
    ecrit (drapeau FNAME, le nom du membre)."""
    import farc
    import gzip
    f = farc.Farc(os.path.join(SRC, 'objset', 'stg%s.farc' % source))
    if not f.compressed:
        raise ValueError('archive de ver.B non comprimee : inattendu')
    membres = []
    stats = None
    for e in f.entries:
        nom = e['name'].replace('stg%s_' % source, 'stg%s_' % code)
        if nom == e['name']:
            raise ValueError('%s : membre %r sans le prefixe stg%s_'
                             % (source, e['name'], source))
        brut = f.data[e['offset']:e['offset'] + e['csize']]
        if e['name'].endswith('_obj.bin'):
            neuf, nb, empl = renumeroter_obj(f.read(e))
            stats = (nb, empl)
            tampon = io.BytesIO()
            with gzip.GzipFile(filename=nom, mode='wb', fileobj=tampon,
                               mtime=0) as g:
                g.write(neuf)
            membres.append((nom, tampon.getvalue(), len(neuf)))
        else:
            membres.append((nom, brut, e['usize']))
    tete = sum(len(n.encode('ascii')) + 1 + 12 for n, _, _ in membres)
    debut = 12 + tete
    corps = bytearray()
    entetes = bytearray()
    pos = debut
    for nom, donnees, usize in membres:
        entetes += nom.encode('ascii') + b'\x00'
        entetes += struct.pack('>III', pos, len(donnees), usize)
        corps += donnees
        pos += len(donnees)
    sortie = bytearray(b'FArC')
    sortie += struct.pack('>II', debut - 8, 1)
    sortie += entetes
    assert len(sortie) == debut
    with open(dest, 'wb') as fp:
        fp.write(bytes(sortie) + bytes(corps))
    return stats


def textures_objset(code):
    """Les identifiants de texture de l'objset POSE `stg<code>.farc`."""
    ch = os.path.join(MEDIA, 'rom', 'objset', 'stg%s.farc' % code)
    if not os.path.exists(ch):
        return None
    return _ids_textures_obj(_obj_de_farc(ch))


if __name__ == '__main__':
    f = controler()
    print('%d entrees de ver.B' % len(entrees()))
    for e in entrees():
        print('  %-3d %-4s modele %-4s geo %-4s objset %-5d ciel %s  ecl %s'
              % (e['indice'], e['code'], e['modele'], e['geo'], e['objset'],
                 e['ciel'], e['eclairage']))
    if f:
        print('%d FAUTE(S)' % len(f))
        for x in f:
            print('   . %s' % x)
        sys.exit(1)
    dv = descripteurs_verb()
    print('%d descripteurs lus dans l ELF' % len(dv))
    carte, vb, fs = carte_textures()
    neufs = [n for n in carte if n not in set(fs.values())]
    print('%d textures renumerotees, dont %d a un numero neuf (%d..%d)'
          % (len(carte), len(neufs), min(carte[n] for n in neufs),
             max(carte[n] for n in neufs)))
