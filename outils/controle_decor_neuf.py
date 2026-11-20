# -*- coding: utf-8 -*-
r"""Controle avant vol d un decor VRAIMENT AJOUTE : les fichiers, les bases, le binaire.

La question qui compte : les cinq objets que le DESCRIPTEUR demande existent-ils
dans l'objset POSE, sous l'identifiant d'objset POSE ? Le reste peut etre juste
et le decor ne pas charger si celle-la est fausse.
"""
import io
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
MEDIA = os.path.join(RACINE, r'runtime\media\vf5fs\vf5fs_media')

import a3d_db
import farc
import obj_db as mod_objdb
import objset as mod_objset
import pefile

# Les trois valeurs se passent en argument ; les defauts sont ceux du
# dojo VF5 R, le premier decor vraiment ajoute au jeu.
_a = sys.argv[1:]
CODE = _a[_a.index('--code') + 1] if '--code' in _a else 'd5r'
INDICE = int(_a[_a.index('--indice') + 1], 0) if '--indice' in _a else 41
OBJSET = int(_a[_a.index('--objset') + 1], 0) if '--objset' in _a else 6150
BASE = 0x180000000
fautes = []

print('=' * 72)
print('CONTROLE AVANT VOL -- decor AJOUTE « %s », indice %d' % (CODE, INDICE))
print('=' * 72)

# --- 1. le descripteur, dans la DLL patchee -------------------------------
pe = pefile.PE(os.path.join(RACINE,
                            r'runtime\media\vf5fs\vf5fs-pxd-w64-Retail_APM3.dll'),
               fast_load=True)
sec = [s for s in pe.sections if s.Name.rstrip(b'\x00') == b'.decors'][0]
va = BASE + sec.VirtualAddress
d = pe.get_data(va + INDICE * 0xF0 - BASE, 0xF0)


def ch(v):
    try:
        return pe.get_data(v - BASE, 64).split(b'\x00')[0].decode('latin-1')
    except Exception:
        return '?'


objset = struct.unpack_from('<I', d, 0x10)[0]
objets = struct.unpack_from('<5I', d, 0x14)
print('\n1. LE DESCRIPTEUR')
print('   objset demande        %d' % objset)
print('   objets demandes       %s'
      % ' '.join('%d:%d' % (v >> 16, v & 0xFFFF) for v in objets))
print('   auth_3d               %r / %r'
      % (ch(struct.unpack_from('<Q', d, 0)[0]),
         ch(struct.unpack_from('<Q', d, 8)[0])))
print('   collision             %r' % ch(struct.unpack_from('<Q', d, 0x48)[0]))
if objset != OBJSET:
    fautes.append('le descripteur demande l objset %d, pas %d' % (objset, OBJSET))

# --- 2. les neuf fichiers --------------------------------------------------
# DIX pieces, et la dixieme a coute un ecran de chargement infini le
# 2026-09-10 : le chargeur d'eclairage 0x1800D7130 compose SIX chemins, dont
# `envmap_correct_<code>.txt` en 0x1800D727A. Un controle qui n'en verifiait que
# neuf laissait passer exactement la panne qu'il doit attraper.
print('\n2. LES DIX PIECES POSEES')
lot = [('objset', 'stg%s.farc' % CODE), ('', 'STG%s_COLI.000.bin' % CODE.upper()),
       ('auth_3d', 'STG%s.farc' % CODE.upper()),
       ('auth_3d', 'EFFSTG%s.farc' % CODE.upper()), ('ibl', '%s.ibl' % CODE)]
for p in ('light', 'fog', 'glow', 'wind', 'envmap_correct'):
    lot.append(('light_param', '%s_%s.txt' % (p, CODE)))
for dest, nom in lot:
    chemin = os.path.join(MEDIA, 'rom', dest, nom)
    if os.path.exists(chemin):
        print('   %-26s %10d o' % (nom, os.path.getsize(chemin)))
    else:
        print('   %-26s ABSENT' % nom)
        fautes.append('fichier absent : %s' % nom)

# --- 3. obj_db pose --------------------------------------------------------
print('\n3. LA BASE obj_db POSEE')
o = mod_objdb.charger(os.path.join(MEDIA, r'rom\objset\obj_db.bin'))
k, e = o.jeu('STG%s' % CODE.upper())
if e is None:
    fautes.append('STG%s absent de l obj_db pose' % CODE.upper())
else:
    print('   STG%s : identifiant %d, %s / %s / %s'
          % (CODE.upper(), e[1], o.nom_a(e[2]), o.nom_a(e[3]), o.nom_a(e[4])))
    if e[1] != objset:
        fautes.append('obj_db donne l identifiant %d, le descripteur demande %d'
                      % (e[1], objset))
    print('   %d objets sous cet identifiant' % len(o.objets_de(e[1])))

# --- 4. LA question : les objets demandes sont-ils dans l archive posee ? ---
print('\n4. LES OBJETS DEMANDES EXISTENT-ILS DANS L ARCHIVE POSEE ?')
ids = None
arch = os.path.join(MEDIA, r'rom\objset\stg%s.farc' % CODE)
tmp = os.path.join(RACINE, 'extracted', '_controle_%s' % CODE)
interne = 'stg%s_obj.bin' % CODE
chemin = os.path.join(tmp, interne)
if not os.path.exists(chemin) or os.path.getmtime(chemin) < os.path.getmtime(arch):
    os.makedirs(tmp, exist_ok=True)
    farc.extract_one(arch, tmp, quiet=True)
if not os.path.exists(chemin):
    fautes.append('l archive posee ne contient pas %s -- l en-tete n a pas ete '
                  'renommee' % interne)
    print('   %s INTROUVABLE dans l archive' % interne)
else:
    obj = mod_objset.Objset(chemin)
    ids = dict(zip(obj.ids(), obj.noms()))
    print('   %s : %d objets, id max %d' % (interne, obj.nombre, obj.id_max))
    for v in objets:
        hi, lo = v >> 16, v & 0xFFFF
        if lo in ids:
            print('     %5d:%-5d %s' % (hi, lo, ids[lo]))
        else:
            print('     %5d:%-5d INTROUVABLE' % (hi, lo))
            fautes.append('objet %d absent de l archive posee' % lo)

# --- 5. auth_3d_db pose ----------------------------------------------------
print('\n5. LA BASE auth_3d_db POSEE')
a = a3d_db.charger(os.path.join(MEDIA, r'rom\auth_3d\auth_3d_db.bin'))
for cat in ('STG%s' % CODE.upper(), 'EFFSTG%s' % CODE.upper()):
    u = a.uids_de(cat)
    if not u:
        fautes.append('categorie %s absente' % cat)
        print('   %-12s ABSENTE' % cat)
    else:
        print('   %-12s %d uid(s) : %s'
              % (cat, len(u), ', '.join(u[k]['value'].split()[-1]
                                        for k in sorted(u))))
print('   (aller-retour de la base posee : %s)'
      % ('exact' if a.texte().encode('ascii')
         == io.open(os.path.join(MEDIA, r'rom\auth_3d\auth_3d_db.bin'),
                    'rb').read() else 'DIFFERENT'))

# --- 6. LES DEUX TABLES D EFFETS, ET CE QU ELLES NOMMENT -------------------
# LE CONTROLE QUI MANQUAIT. Le 2026-09-10, le decor ajoute s'est affiche avec
# ses flammes et SANS SES BARRIERES, sans un message. Cause : la table des murs
# ne porte que des POINTEURS, et tout le mur est dans les trois blocs qu'ils
# designent -- 28 morceaux nommes `(objset << 16) | rang`, une liste d'uid, une
# paire intact/casse. Un clone de l'entree renvoyait donc a l'objset du MODELE,
# qui n'est pas charge dans un build d'ajout.
#
# Les deux tables sont des LISTES D'ASSOCIATION : un indice inconnu ne plante
# pas, il ne fait RIEN. Aucune de leurs fautes ne se voit autrement qu'a
# l'ecran -- d'ou ce controle, qui les lit dans le binaire PATCHE.
print('\n6. LES DEUX TABLES D EFFETS (lues dans la DLL patchee)')
uids_a_nous = set(a.uids_de('EFFSTG%s' % CODE.upper()))


def _table(site):
    """La cible du `lea` : les tables ont demenage dans .decors."""
    return site + 4 + struct.unpack('<i', pe.get_data(site - BASE, 4))[0]


def _entree(site, pas, indice):
    t = _table(site)
    r = 0
    while r < 128:
        e = pe.get_data(t + r * pas - BASE, pas)
        v = struct.unpack_from('<i', e, 0)[0]
        if v == -1:
            return None
        if v == indice:
            return t + r * pas, e
        r += 1
    return None


def _liste(va, pas, champs):
    """Les enregistrements d'un bloc, jusqu'au -1 de tete."""
    out = []
    while len(out) < 512:
        rec = pe.get_data(va + len(out) * pas - BASE, pas)
        if struct.unpack_from('<i', rec, 0)[0] == -1:
            return out
        out.append(struct.unpack_from('<%di' % champs, rec, 0))
    return out


def _objet(v, ou):
    """Un `(objset << 16) | rang` : notre objset, et un rang qui existe."""
    hi, lo = v >> 16, v & 0xFFFF
    if hi != OBJSET:
        fautes.append('%s nomme l objset %d, pas le notre (%d) -- l effet se '
                      'lierait a un objset qui n est pas charge' % (ou, hi, OBJSET))
    elif ids is not None and lo not in ids:
        fautes.append('%s nomme le rang %d, absent de l archive posee' % (ou, lo))


def _uid(v, ou):
    if v not in uids_a_nous:
        fautes.append('%s cite l uid %d, qui n est pas de la categorie '
                      'EFFSTG%s' % (ou, v, CODE.upper()))


e = _entree(0x1800706BC, 0x10, INDICE)      # TaskEffectAuth3D, 0x1800706B0
if e is None:
    print('   animations   AUCUNE ENTREE pour l indice %d' % INDICE)
    fautes.append('l indice %d n a pas d entree dans la table des animations '
                  'd effet : pas de flammes, en silence' % INDICE)
else:
    ptr = struct.unpack_from('<Q', e[1], 8)[0]
    u = [v[0] for v in _liste(ptr, 4, 1)]
    print('   animations   0x%X -> %s' % (ptr, u))
    for v in u:
        _uid(v, 'la liste d animations')

e = _entree(0x1800843B0, 0x40, INDICE)      # TaskEffectWall, 0x1800843A0
if e is None:
    print('   mur          AUCUNE ENTREE pour l indice %d' % INDICE)
    fautes.append('l indice %d n a pas d entree dans la table des murs : pas '
                  'de barrieres, en silence' % INDICE)
else:
    q = struct.unpack_from('<7Q', e[1], 8)
    if any(q[3:]):
        fautes.append('l entree de mur porte des champs +0x20..+0x38 non nuls '
                      '(%s) : ils n ont pas ete decodes'
                      % ' '.join('0x%X' % v for v in q[3:]))
    morceaux = _liste(q[0], 0x2C, 1)
    uids = [v[0] for v in _liste(q[1], 4, 1)]
    paires = _liste(q[2], 0x10, 4)
    rangs = {}
    for v in morceaux:
        rangs[v[0] & 0xFFFF] = rangs.get(v[0] & 0xFFFF, 0) + 1
    print('   mur          0x%X : %d morceaux %s'
          % (q[0], len(morceaux),
             ' '.join('rang %d x%d' % (r, c) for r, c in sorted(rangs.items()))))
    print('                0x%X : uid %s' % (q[1], uids))
    print('                0x%X : %d paire(s) %s'
          % (q[2], len(paires),
             ' '.join('%d:%d->%d:%d' % (p[0] >> 16, p[0] & 0xFFFF,
                                        p[1] >> 16, p[1] & 0xFFFF)
                      for p in paires)))
    if not morceaux:
        fautes.append('le mur de l indice %d n a aucun morceau' % INDICE)
    for i, v in enumerate(morceaux):
        _objet(v[0], 'le morceau de mur %d' % i)
    for v in uids:
        _uid(v, 'la liste d uid du mur')
    for i, p in enumerate(paires):
        _objet(p[0], 'la paire %d (intact)' % i)
        _objet(p[1], 'la paire %d (casse)' % i)
        _uid(p[2], 'la paire %d' % i)
        _uid(p[3], 'la paire %d' % i)

# --- 7. LES TACHES D EFFET DU DECOR ----------------------------------------
# LE CONTROLE QUI MANQUAIT, DEUXIEME COUCHE. Le 2026-09-10, l'entree de mur
# etait juste et les barrieres restaient invisibles : `TaskEffectWall` n'etait
# tout simplement pas CREEE pour le decor ajoute. Les taches d'effet a creer
# sont dans le +0x20 de la table 0x18034D570, celle qu'on croyait « toutes
# entrees vides » -- ce n'etait vrai que de ses quatre premiers octets.
EFFETS_NOMS = (
    'EFFECT_HIT', 'EFFECT_AUTH3D', 'EFFECT_WALL', 'EFFECT_LEAF',
    'EFFECT_WATA', 'EFFECT_SNOW', 'EFFECT_YUKA', 'EFFECT_RIPPLE',
    'EFFECT_RAIN', 'EFFECT_THUNDER', 'EFFECT_DOWN', 'EFFECT_MOVE',
    'EFFECT_RINGOUT_SPLASH', 'EFFECT_WATER_RING', 'EFFECT_SPLASH',
    'EFFECT_SNOW_RING', 'EFFECT_FOG_ANIM', 'EFFECT_WET_CLOTH',
    'EFFECT_FOG_RING', 'EFFECT_BREATH', 'EFFECT_PARTICLE', 'EFFECT_POISON',
    'EFFECT_ELE_BOARD')
MODELE = 11                                    # djo, le decor modele


def _taches(t, i):
    e = pe.get_data(t + i * 0x60 - BASE, 0x60)
    out = []
    for v in struct.unpack_from('<16i', e, 0x20):
        if v == -1:
            return out
        out.append(v)
    return out


def _dire(lst):
    return ' '.join('%d=%s' % (v, EFFETS_NOMS[v] if 0 <= v < len(EFFETS_NOMS)
                               else '?') for v in lst) or '(aucune)'


print('\n7. LES TACHES D EFFET CREEES POUR LE DECOR')
t = _table(0x18006F675)                        # lea dans 0x18006F620
print('   table                0x%X' % t)
n, m = _taches(t, INDICE), _taches(t, MODELE)
print('   indice %-3d           %s' % (INDICE, _dire(n)))
print('   modele %-3d (djo)     %s' % (MODELE, _dire(m)))
if not n:
    fautes.append('l indice %d ne demande AUCUNE tache d effet : sans '
                  'EFFECT_WALL la table des murs n est jamais consultee, et '
                  'le decor s affiche sans ses barrieres' % INDICE)
elif n != m:
    fautes.append('l indice %d demande %s la ou le modele demande %s : le '
                  'clone n est pas complet' % (INDICE, _dire(n), _dire(m)))

print('\n' + '-' * 72)
if fautes:
    print('%d FAUTE(S) :' % len(fautes))
    for f in fautes:
        print('   . %s' % f)
    sys.exit(1)
print('RIEN A REDIRE.')
print('-' * 72)
