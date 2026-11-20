# -*- coding: utf-8 -*-
r"""LA TABLE DES DECORS DE VF5 R AJOUTES — une seule, partagee.

`decor_neuf.py` pose les fichiers, `patch_moteur.py` remplit le binaire et
`controle_decor_neuf.py` verifie : les trois doivent parler du MEME lot. La
lecon du 2026-09-09 (`--variantes-djo`, deux constantes pour une donnee) dit
qu'un emplacement ne vit qu'a UN endroit. Ici, c'est ce fichier.

CE QUE VF5 R APPORTE, ET CE QU'IL N'APPORTE PAS

VF5 R n'a **aucun decor que l'APM3 n'ait pas** — il a les memes, moins `du5`.
Ce qu'il apporte, ce sont des versions **plus riches** des memes lieux : `djo`
+8,1 Mo, `sin` +8,1, `smo` +7,3, `nyc` +6,9, `du3` +4,3 (mesure dans
`analysis/decors_vf5r.md` §3). Les ajouter, c'est donc mettre les DEUX
generations cote a cote, une par variante de la meme case de grille.

LES DIX-NEUF QUI SONT COMPLETS, ET POURQUOI PAS LES AUTRES

Le releve croise (les 41 descripteurs du binaire contre
`extracted/decors/VF5R/`) donne :

  . 19 decors COMPLETS : les dix pieces sont la ;
  . `du1`..`du4` : il manque `auth_3d/STGDU<n>.farc` -- ce n'est pas un
    manque, leurs categories sont VIDES dans la base de R (voir DURAL_5R,
    ajoutes le 2026-09-11 aux indices 82-85) ;
  . `du5` : **n'existe pas dans VF5 R**, c'est un decor de Final Showdown ;
  . `tst ts2 ts3 wht trm cid trs evo00..evo09` : emplacements d'essai, de 0 a
    1,2 Mo, sans animation. Rien a transplanter.

LE CODE A TROIS LETTRES

Il fait TROIS caracteres, obligatoirement : `importer_decor.renommer_farc`
reecrit `stg<modele>_obj.bin` -> `stg<neuf>_obj.bin` **en place** dans l'en-tete
du `FArC`. Le schema est `<1re lettre><3e lettre>5` — il est unique sur les
dix-neuf et ne heurte aucun code du jeu.

`djo` fait exception avec `d5r` : c'est le premier decor ajoute du chantier,
valide a l'ecran le 2026-09-10, et on ne renomme pas un build valide pour
l'elegance d'un schema.

L'INDICE ET L'OBJSET

L'indice 41 est le code « decor ALEATOIRE », teste par egalite a sept endroits :
les ajouts commencent a **42**. Les identifiants d'objset viennent de la plage
libre 6150..6349 (`obj_db.py --libres`), dans l'ordre.
"""

# (modele, code neuf, indice, objset)
#
# L'ordre est celui de l'indice. `djo` est en tete : c'est l'entree 42, deja
# validee, et elle ne bouge pas.
DECORS_5R = (
    ('djo', 'd5r', 42, 6150),
    ('ban', 'bn5', 43, 6151),
    ('ter', 'tr5', 44, 6152),
    ('nyc', 'nc5', 45, 6153),
    ('cas', 'cs5', 46, 6154),
    ('riv', 'rv5', 47, 6155),
    ('jin', 'jn5', 48, 6156),
    ('sin', 'sn5', 49, 6157),
    ('umi', 'ui5', 50, 6158),
    ('hai', 'hi5', 51, 6159),
    ('are', 'ae5', 52, 6160),
    ('slk', 'sk5', 53, 6161),
    ('yuk', 'yk5', 54, 6162),
    ('tak', 'tk5', 55, 6163),
    ('aur', 'ar5', 56, 6164),
    ('bar', 'br5', 57, 6165),
    ('tan', 'tn5', 58, 6166),
    ('gym', 'gm5', 59, 6167),
    ('smo', 'so5', 60, 6168),
)

# LES QUATRE DECORS DE DURAL DE VF5 R (2026-09-11)
#
# Frederic : « decors de Dural : importer son ou ses decors ». Ils etaient
# restes dehors parce que `auth_3d/STGDU<n>.farc` manque a l'archive de R. Ce
# n'est PAS un manque : la base de R declare ces quatre categories VIDES (0
# uid), exactement comme celle de FS pour STGDU1 -- R ne joue aucune scene sur
# ses decors de Dural (`STGDUR.farc`, trois `S180A0x0_DUR_STG`, n'est demande
# par AUCUN descripteur). Tout le reste y est : quatre objsets de 27 a 32 Mo,
# les effets, les collisions, l'eclairage. Voir SANS_SCENE et `controler()`.
#
# Indices 82-85, a la suite de ver.B (61-81) : ils n'existent donc que dans
# le build VF5 (`decors_vf5.cmd`, `--decors-5r-dural`), dont les anneaux ont
# seize variantes -- la case de Dural en fait treize : FS 5, R 4, ver.B 4.
DURAL_5R = (
    ('du1', 'd15', 82, 6191),
    ('du2', 'd25', 83, 6192),
    ('du3', 'd35', 84, 6193),
    ('du4', 'd45', 85, 6194),
)
DURAL_5R_LIBELLES = ('SNOW - VF5 R', 'ECLIPSE - VF5 R', 'SUBMERSION - VF5 R',
                     'STORM - VF5 R')
# Les modeles dont R n'a pas de scene (categorie STG<modele> vide dans SA
# base, pas de .farc) : on ne pose pas cette piece-la.
SANS_SCENE = ('du1', 'du2', 'du3', 'du4')

# Les noms lisibles, pour le libelle de la barre espace.
GENERATIONS = ('VIRTUA FIGHTER 5 FS', 'VIRTUA FIGHTER 5 R')

SOURCE = 'VF5R'


def ids_archive(code, media=None, racine=None):
    """Les identifiants d'objet presents dans l'archive POSEE, ou None.

    Le patcheur ET le controle en ont besoin : le descripteur d'un decor
    ajoute demande cinq objets par leur RANG, et rien ne garantit que la
    generation de 2008 les ait tous. Mesure du 2026-09-10 : `ban`, `jin` et
    `are` n'ont pas leur objet `reflect` -- le reflet est une addition de Final
    Showdown. Un rang absent, c'est un chargement qui ne finit pas ou un decor
    incomplet, sans un message.

    L'extraction est mise en cache sous `extracted/_controle_<code>` : dix-neuf
    archives de vingt megaoctets ne se depaquettent pas a chaque appel.
    """
    import os
    import sys
    ici = os.path.dirname(os.path.abspath(__file__))
    if ici not in sys.path:
        sys.path.insert(0, ici)
    racine = racine or os.path.dirname(ici)
    media = media or os.path.join(racine, 'runtime', 'media', 'vf5fs',
                                  'vf5fs_media')
    import objset as mod_objset
    chemin = _extraire_obj(code, media, racine)
    if chemin is None:
        return None
    return set(mod_objset.Objset(chemin).ids())


def objets_archive(code, media=None, racine=None):
    """Les objets de l'archive POSEE : [(identifiant, nom), ...], ou None.

    C'est ce qui doit etre declare dans `obj_db`, et non les objets du modele :
    `obj_db` decrit l'archive qu'on POSE. Mesure du 2026-09-10 sur les
    dix-neuf : entre 47 et 196 objets declares n'existent pas dans la
    generation de 2008, et jusqu'a 58 objets de 2008 n'etaient pas declares --
    or ce sont ceux que ses propres `.a3da` nomment.
    """
    import os
    import sys
    ici = os.path.dirname(os.path.abspath(__file__))
    if ici not in sys.path:
        sys.path.insert(0, ici)
    chemin = _extraire_obj(code, media, racine)
    if chemin is None:
        return None
    import objset as mod_objset
    ob = mod_objset.Objset(chemin)
    return list(zip(ob.ids(), ob.noms()))


def _extraire_obj(code, media=None, racine=None):
    import os
    import sys
    ici = os.path.dirname(os.path.abspath(__file__))
    if ici not in sys.path:
        sys.path.insert(0, ici)
    racine = racine or os.path.dirname(ici)
    media = media or os.path.join(racine, 'runtime', 'media', 'vf5fs',
                                  'vf5fs_media')
    import farc
    arch = os.path.join(media, 'rom', 'objset', 'stg%s.farc' % code)
    if not os.path.exists(arch):
        return None
    tmp = os.path.join(racine, 'extracted', '_controle_%s' % code)
    chemin = os.path.join(tmp, 'stg%s_obj.bin' % code)
    if (not os.path.exists(chemin)
            or os.path.getmtime(chemin) < os.path.getmtime(arch)):
        os.makedirs(tmp, exist_ok=True)
        try:
            farc.extract_one(arch, tmp, quiet=True)
        except Exception:
            return None
    return chemin if os.path.exists(chemin) else None


def par_code(code):
    for e in DECORS_5R + DURAL_5R:
        if e[1] == code:
            return e
    return None


def lot(dural=False):
    """Le lot : les dix-neuf, et les quatre de Dural si `dural`."""
    return DECORS_5R + (DURAL_5R if dural else ())


def sans_scene(code):
    """Vrai si le decor (code neuf OU modele) n'a pas de scene chez R."""
    e = par_code(code)
    return (e[0] if e else code) in SANS_SCENE


def entrees(dural=False):
    """Le lot sous la forme de `variantes_vf5.entrees()` -- une entree par
    indice, chaque champ ecrit. Depuis le 2026-09-11 (« applique a VF5 R ses
    propres listes, rien ne doit venir de FS »), le patcheur traite les deux
    lots de la meme facon : ce que le decor CONTIENT (objets, taches, murs,
    animations, dossiers d'effet) est relu dans le binaire de SA generation
    (`generation.py`), et seul le COMPORTEMENT (musique, anneau, rendu) vient
    du modele Final Showdown. `cle` est le code du decor dans la generation.
    """
    out = []
    for modele, code, indice, objset in lot(dural):
        out.append(dict(gen='r', modele=modele, code=code, indice=indice,
                        objset=objset, geo=code, source=modele,
                        src_geo=modele, eclairage=modele, verb=modele,
                        cle=modele, a3d='STG%s' % code.upper(), eff=code,
                        coli=code, ciel=None))
    return out


def indices(dural=False):
    return [e[2] for e in lot(dural)]


def controler():
    """Rend une liste de fautes. Un lot se verifie avant de servir -- les
    quatre de Dural compris, pour que codes, indices et objsets restent
    uniques quel que soit le build."""
    fautes = []
    codes, indices_, objsets = set(), set(), set()
    # SANS_SCENE n'est pas une supposition : la base de R doit declarer la
    # categorie VIDE, et l'archive ne doit pas avoir le .farc.
    import os
    ici = os.path.dirname(os.path.abspath(__file__))
    racine = os.path.dirname(ici)
    base_r = os.path.join(racine, 'extracted', 'decors', SOURCE, '_db',
                          'auth_3d_db.bin')
    if os.path.exists(base_r):
        import sys
        if ici not in sys.path:
            sys.path.insert(0, ici)
        import a3d_db
        a = a3d_db.charger(base_r)
        for m in SANS_SCENE:
            if a.uids_de('STG%s' % m.upper()):
                fautes.append('SANS_SCENE : la base de R declare des uid '
                              'sous STG%s' % m.upper())
            if os.path.exists(os.path.join(racine, 'extracted', 'decors',
                                           SOURCE, 'auth_3d',
                                           'STG%s.farc' % m.upper())):
                fautes.append('SANS_SCENE : STG%s.farc existe chez R'
                              % m.upper())
    for modele, code, indice, objset in lot(True):
        if len(code) != 3:
            fautes.append('« %s » ne fait pas trois caracteres' % code)
        if len(modele) != 3:
            fautes.append('le modele « %s » ne fait pas trois caracteres '
                          '(la substitution dans le FArC est EN PLACE)'
                          % modele)
        for ens, v, quoi in ((codes, code, 'code'),
                             (indices_, indice, 'indice'),
                             (objsets, objset, 'objset')):
            if v in ens:
                fautes.append('%s %r en double' % (quoi, v))
            ens.add(v)
        if indice < 42:
            fautes.append('l indice %d est reserve (41 = decor aleatoire)'
                          % indice)
    return fautes


if __name__ == '__main__':
    import sys
    f = controler()
    largeur = max(len(e[0]) for e in DECORS_5R)
    print('%d decors de VF5 R a ajouter' % len(DECORS_5R))
    print('%-*s  %-5s %-7s %s' % (largeur, 'modele', 'code', 'indice',
                                  'objset'))
    for modele, code, indice, objset in DECORS_5R:
        print('%-*s  %-5s %-7d %d' % (largeur, modele, code, indice, objset))
    print()
    if f:
        print('%d FAUTE(S) :' % len(f))
        for x in f:
            print('   . %s' % x)
        sys.exit(1)
    print('table saine ; table des decors a passer : --decors-table %d'
          % (max(e[2] for e in DECORS_5R) + 1))
