#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES TEXTURES 3D -- celles des DECORS et des personnages -- en version HD.

Le pendant de `tools/textures_hd.py`, qui ne traite que la 2D. **Le format est
le MEME** : la banque de textures d un objset est un bloc TXP, mesure sur
`stgnyc_tex.bin` -- magie `TXP\\x03` a l offset 0, 332 textures, les memes
formats 6 (DXT1) et 9 (DXT5). Tout le lecteur et tout l encodeur se
reutilisent tels quels.

TROIS DIFFERENCES, ET ELLES COMPTENT :

  1. **L archive n est PAS un fichier libre.** Les `spr_n_*` de la 2D ont leur
     nom masque dans le `.par`, donc la copie de `rom/2d/` gagne. Les objsets
     de decor, eux, ne sont QUE dans le `.par` : `rom/objset/` ne porte que
     les decors importes et `obj_db.bin`. Poser une texture demande donc les
     DEUX gestes de la recette des decors -- deposer le fichier libre dans
     `rom/objset/` **et** masquer le nom dans le `.par` (`par_masquer.py`).
     C est `--poser` qui les fait, et `--retirer` qui les defait.

  2. **Une banque porte plusieurs centaines de textures**, et chacune ses
     niveaux de mip. On ne sort donc pas tout : `--sortir <code>` prend
     `--combien N` (les N plus grandes) ou `--indices 3,17,42`.

  3. **Le fichier est gros** (38 Mo pour `stgnyc_tex.bin`, 22 Mo comprime).
     Reecrire l archive en `FArc` brut la fait grossir -- le moteur lit les
     deux, c est de la place sur le disque, pas de la memoire video.

    py -3 tools/textures_hd3d.py --decors
    py -3 tools/textures_hd3d.py --inventaire stgnyc
    py -3 tools/textures_hd3d.py --sortir stgnyc --combien 8
    py -3 tools/textures_hd3d.py --sortir stgnyc --indices 107,108
    py -3 tools/textures_hd3d.py --poser stgnyc
    py -3 tools/textures_hd3d.py --retirer stgnyc

LES DOSSIERS. `--sortir` ecrit dans `HD_TEXTURES/EXTRACTED/STAGES` ou
`.../CHARACTERS`, `--poser` lit dans `HD_TEXTURES/HD/STAGES` ou
`.../CHARACTERS`. La famille est LUE dans `analysis/table_decors.csv` : les
quarante et un decors y sont, tout le reste est un personnage.
"""
import io
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import farc as mfarc                                          # noqa: E402
import par_inventaire as mpar                                 # noqa: E402
import textures_hd as t2d                                     # noqa: E402
import txp                                                    # noqa: E402

PAR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_data.par')
OBJSET = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media',
                      'rom', 'objset')
HD_RACINE = os.path.join(RACINE, 'HD_TEXTURES')
REGISTRE = os.path.join(HD_RACINE, '_POSEES_3D.txt')
TABLE = os.path.join(RACINE, 'analysis', 'table_decors.csv')


# L ARBORESCENCE, rangee le 2026-10-11 : ce qui SORT du jeu va dans
# `EXTRACTED/`, ce qui y RENTRE dans `HD/`, et chacun par famille --
# `2D`, `STAGES`, `CHARACTERS`. La famille d un code n est pas DEVINEE : elle
# est lue dans `analysis/table_decors.csv`. Tout ce qui n y figure pas est un
# personnage.
def famille(code):
    """'STAGES' ou 'CHARACTERS', d apres la table des decors.

    La table porte le code court (`nyc`) et le nom long (`STGNYC`) ; l archive
    d objset, elle, s appelle `stgnyc.farc`. On compare donc les trois.
    """
    c = code.lower()
    for _i, court, long_ in decors():
        if c in (court.lower(), 'stg' + court.lower(), long_.lower()):
            return 'STAGES'
    return 'CHARACTERS'


def dossier_hd(code):
    """Ou l on prend les PNG HD a poser."""
    return os.path.join(HD_RACINE, 'HD', famille(code))


def dossier_originaux(code):
    """Ou l on depose les PNG sortis du jeu."""
    return os.path.join(HD_RACINE, 'EXTRACTED', famille(code))


def decors():
    """Les 41 decors : code -> nom. Lu dans la table du chantier, pas devine."""
    out = []
    if not os.path.exists(TABLE):
        return out
    with io.open(TABLE, encoding='utf-8') as fp:
        lignes = [l.strip() for l in fp if l.strip()]
    for l in lignes[1:]:
        c = l.split(';')
        if len(c) > 2:
            out.append((int(c[0]), c[1], c[2]))
    return out


def _entree_par(nom):
    """L entree du `.par`, a la CASSE PRES d abord.

    PIEGE PAYE : le `.par` porte DEUX entrees par decor -- `STGNYC.farc`
    (25 Ko, le jeu d animations auth_3d) et `stgnyc.farc` (22 Mo, l objset
    avec sa geometrie et ses textures). Une comparaison insensible a la casse
    rend la premiere des deux, et l outil annonce alors " aucun membre
    *_tex.bin " sur une archive qui n en a jamais eu.
    """
    _d, fic = mpar.lire(PAR)
    replis = None
    for n, t, c, o, f in fic:
        if n == nom:
            return n, t, c, o, f
        if replis is None and n.lower() == nom.lower():
            replis = (n, t, c, o, f)
    return replis


def archive(code):
    """Rend les octets de l archive d objset, libre si elle existe, sinon du
    `.par`. On lit TOUJOURS le fichier libre en priorite : c est lui que le
    moteur charge une fois le nom masque."""
    libre = os.path.join(OBJSET, code + '.farc')
    if os.path.exists(libre):
        return open(libre, 'rb').read(), libre
    e = _entree_par(code + '.farc')
    if not e:
        raise SystemExit('%s.farc : ni fichier libre ni entree du .par' % code)
    _n, _t, c, o, _f = e
    with open(PAR, 'rb') as fp:
        fp.seek(o)
        return fp.read(c), None


def banque(code):
    """Rend ({nom: octets}, nom du membre de textures, textures lues)."""
    brut, _src = archive(code)
    tmp = os.path.join(RACINE, 'extracted', '_hd3d_%s.farc' % code)
    with open(tmp, 'wb') as fp:
        fp.write(brut)
    f = mfarc.Farc(tmp)
    membres = dict((e['name'], f.read(e)) for e in f.entries)
    forme = (f.alignment or 1, f.compressed)
    os.remove(tmp)
    nom_tex = None
    for n in membres:
        if n.endswith('_tex.bin'):
            nom_tex = n
    if nom_tex is None:
        raise SystemExit('%s : aucun membre *_tex.bin' % code)
    tete, textures = t2d.lire_txp(membres[nom_tex])
    return membres, nom_tex, tete, textures, forme


def inventaire(code, combien=0):
    _m, nom_tex, _t, textures, _forme = banque(code)
    print('%s : %s, %d textures' % (code, nom_tex, len(textures)))
    rangs = _choisir(textures, combien) if combien else range(len(textures))
    for k in rangs:
        n0 = textures[k]['niveaux'][0]
        print('   %s__tex%03d.png  %-6s %5dx%-5d %d niveau(x)'
              % (code, k, t2d.NOMS_FORMAT.get(n0['format'], n0['format']),
                 n0['larg'], n0['haut'], len(textures[k]['niveaux'])))
    return 0


def _choisir(textures, combien):
    """Les `combien` plus GRANDES. Une texture HD se juge sur les planches qui
    couvrent de la surface, pas sur les vignettes de 8x8."""
    tailles = [(t['niveaux'][0]['larg'] * t['niveaux'][0]['haut'], k)
               for k, t in enumerate(textures)]
    tailles.sort(reverse=True)
    return sorted(k for _s, k in tailles[:combien])


def sortir(code, combien=0, indices=None):
    from PIL import Image
    _m, nom_tex, _t, textures = banque(code)
    sortie = dossier_originaux(code)
    os.makedirs(sortie, exist_ok=True)
    if indices:
        rangs = [i for i in indices if 0 <= i < len(textures)]
    else:
        rangs = _choisir(textures, combien or 8)
    n = 0
    for k in rangs:
        n0 = textures[k]['niveaux'][0]
        etiquette = '%s__tex%03d.png' % (code, k)
        try:
            im = txp.image(n0)
            im.save(os.path.join(sortie, etiquette))
        except Exception as ex:                        # noqa: BLE001
            print('   NON SORTIE %s : %s' % (etiquette, ex))
            continue
        print('   %-24s %-6s %5dx%-5d %d niveau(x)'
              % (etiquette, t2d.NOMS_FORMAT.get(n0['format'], n0['format']),
                 n0['larg'], n0['haut'], len(textures[k]['niveaux'])))
        n += 1
    print()
    print('%d texture(s) dans %s' % (n, sortie))
    return 0


def _png_demandes(code):
    out = {}
    hd = dossier_hd(code)
    if not os.path.isdir(hd):
        return out
    for n in sorted(os.listdir(hd)):
        if not n.lower().endswith('.png') or '__tex' not in n:
            continue
        base, reste = n.rsplit('__tex', 1)
        if base != code:
            continue
        try:
            out[int(reste.split('.')[0])] = os.path.join(hd, n)
        except ValueError:
            print('   nom illisible, ignore : %s' % n)
    return out


def poser(code, controle=False):
    from PIL import Image
    demandes = _png_demandes(code)
    if not demandes:
        print('Aucun PNG pour %s dans %s' % (code, dossier_hd(code)))
        print('Le nom doit etre %s__texNNN.png.' % code)
        return 1
    membres, nom_tex, tete, textures = banque(code)
    change = False
    for k, png in sorted(demandes.items()):
        if k >= len(textures):
            print('   la texture %d n existe pas (%d en tout)'
                  % (k, len(textures)))
            continue
        tex = textures[k]
        f = tex['niveaux'][0]['format']
        aw, ah = tex['niveaux'][0]['larg'], tex['niveaux'][0]['haut']
        im = Image.open(png).convert('RGBA')
        w, h = im.size
        if w % 4 or h % 4:
            print('   %s : %dx%d -- cotes multiples de 4 exiges'
                  % (os.path.basename(png), w, h))
            continue
        print('   %-24s %s %dx%d -> %dx%d'
              % (os.path.basename(png), t2d.NOMS_FORMAT.get(f, f),
                 aw, ah, w, h))
        if controle:
            continue
        tex['niveaux'] = t2d._mips(im, f, len(tex['niveaux']),
                                    tex['niveaux'])
        change = True
    if controle or not change:
        return 0

    d = membres[nom_tex]
    membres[nom_tex] = d[:tete[0]] + t2d.ecrire_txp(tete[1], textures)
    os.makedirs(OBJSET, exist_ok=True)
    cible = os.path.join(OBJSET, code + '.farc')
    # LA FORME DE LA SOURCE, pas la notre -- voir `farc.ecrire_farc`.
    mfarc.ecrire_farc(cible, membres, forme[0], forme[1])
    print('   -> %s ecrit (%d octets)' % (cible, os.path.getsize(cible)))

    # LE FICHIER LIBRE NE SUFFIT PAS : le resolveur consulte le `.par` AVANT
    # le disque pour ces archives-la. On masque donc le nom, comme la recette
    # des decors le fait depuis le 2026-09-10.
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(ICI, 'par_masquer.py'),
                        '--masquer', code + '.farc'],
                       capture_output=True, text=True)
    print((r.stdout or r.stderr).strip()[:400])
    _registre_ajouter(code)
    return 0


def _registre_lire():
    if not os.path.exists(REGISTRE):
        return []
    with io.open(REGISTRE, encoding='ascii') as fp:
        return [l.strip() for l in fp if l.strip()]


def _registre_ajouter(code):
    v = _registre_lire()
    if code not in v:
        v.append(code)
        with io.open(REGISTRE, 'w', encoding='ascii', newline=chr(10)) as fp:
            fp.write(chr(10).join(sorted(v)) + chr(10))


def retirer(code=None):
    import subprocess
    codes = [code] if code else _registre_lire()
    if not codes:
        print('Rien a retirer : le registre est vide.')
        return 0
    for c in codes:
        libre = os.path.join(OBJSET, c + '.farc')
        if os.path.exists(libre):
            os.remove(libre)
            print('   fichier libre retire : %s.farc' % c)
        r = subprocess.run([sys.executable, os.path.join(ICI, 'par_masquer.py'),
                            '--rendre', c + '.farc'],
                           capture_output=True, text=True)
        print('   ' + (r.stdout or r.stderr).strip()[:300])
    v = [x for x in _registre_lire() if x not in codes]
    if v:
        with io.open(REGISTRE, 'w', encoding='ascii', newline=chr(10)) as fp:
            fp.write(chr(10).join(v) + chr(10))
    elif os.path.exists(REGISTRE):
        os.remove(REGISTRE)
    return 0


def main(argv):
    if '--decors' in argv:
        for i, code, nom in decors():
            print('   %2d  %-6s %s' % (i, code, nom))
        return 0
    combien = 0
    if '--combien' in argv:
        combien = int(argv[argv.index('--combien') + 1])
    indices = None
    if '--indices' in argv:
        indices = [int(x) for x in
                   argv[argv.index('--indices') + 1].replace(' ', '').split(',')
                   if x]
    for mot, fonc in (('--inventaire', 'i'), ('--sortir', 's'),
                      ('--poser', 'p'), ('--controle', 'c'),
                      ('--retirer', 'r')):
        if mot in argv:
            j = argv.index(mot) + 1
            code = argv[j] if j < len(argv) and not argv[j].startswith('-') \
                else None
            if fonc == 'r':
                return retirer(code)
            if not code:
                print('il faut le code du decor, par exemple stgnyc')
                return 1
            if fonc == 'i':
                return inventaire(code, combien)
            if fonc == 's':
                return sortir(code, combien, indices)
            return poser(code, controle=(fonc == 'c'))
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
