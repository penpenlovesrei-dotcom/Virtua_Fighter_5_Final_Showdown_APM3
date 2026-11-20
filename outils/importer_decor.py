#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
"""Transplante un decor d'une AUTRE generation dans APM3, jeu complet.

Pourquoi « jeu complet » : l'essai du 2026-09-03 avait pose le seul
`stgdjo.farc` de VF5 R a cote des fichiers Final Showdown, et le jeu bouclait
sur l'ecran de chargement. Les objets d'un decor sont designes par IDENTIFIANT ;
melanger deux generations, c'est demander des objets qui n'existent pas.

Ce qui a ete VERIFIE depuis, et qui change tout (2026-09-07) :

* les cinq objets principaux de `djo` portent les MEMES identifiants dans les
  deux generations -- `gnd` 114, `reflect` 115, `sdw` 116, `sky` 117,
  `ring` 118. Les 52 objets que Final Showdown a en plus sont des effets, ids
  0 a 113. **Le descripteur du moteur n'a donc RIEN a changer** : ses champs
  `+0x14`..`+0x34` valent deja 114 118 117 116 115 ;
* VF5 R a bien son `auth_3d/STGDJO.farc` (37 811 o). La note contraire de
  `import_decors.md` §7 etait fausse ;
* l'identifiant d'objset (28) et les noms internes de l'archive
  (`stgdjo_obj.bin`, `stgdjo_tex.bin`) sont identiques : `obj_db.bin`,
  `tex_db.bin` et `auth_3d_db.bin` n'ont pas a etre reconstruits.

Il ne reste donc qu'une operation de FICHIERS : masquer les huit noms dans
l'index du `.par` et poser les huit fichiers de VF5 R dans l'arborescence
libre `vf5fs_media/`.

    py -3 tools/importer_decor.py --etat djo
    py -3 tools/importer_decor.py --poser djo --source VF5R
    py -3 tools/importer_decor.py --retirer djo

`--source` : un sous-dossier de `extracted/decors/` (VF5R, VF5_VERB,
VF5FS_LIND). `--sans-eclairage` garde l'eclairage de Final Showdown.

AJOUTER PLUTOT QUE REMPLACER : `--vers <code>`

    py -3 tools/importer_decor.py --poser djo --source VF5R --vers evo00
    py -3 tools/importer_decor.py --retirer evo00

Le decor lu chez `djo` est pose sous le code d'un emplacement d'ESSAI encore
inutilise. Final Showdown garde alors son propre `djo` : les deux generations
coexistent, et la barre espace passe de l'une a l'autre.

LA REGLE DU CHANTIER, posee par Frederic le 2026-09-09 :

    on AJOUTE des decors, on n'en REMPLACE aucun --
    sauf, eventuellement, les decors d'essai.

Et « d'essai » ne se suppose pas : `trm` en avait l'air, c'etait le decor
TERMINAL, repare et valide le 2026-09-05, utilise par TREIZE de nos lanceurs.
Le prendre l'a casse. `tools/emplacements.py` MESURE la liste sur quatre
preuves (forme du descripteur, grille de selection, liste d'apercus, nos
propres lanceurs) et `--vers` la consulte : un emplacement pris est REFUSE,
`--forcer` passe outre en le disant.

    py -3 tools/emplacements.py            la liste, avec les raisons
    py -3 tools/emplacements.py --libres   juste les codes disponibles

LE GARDE-FOU SE MORDAIT LA QUEUE : `--pour <lanceur.cmd>`

Des qu'un lanceur NOMME l'emplacement qu'il pose, `emplacements.py` le declare
pris -- preuve 4, « utilise par ... » -- et `--vers` le refuse, y compris a ce
lanceur-la. Un lanceur ne pouvait donc pas poser son propre decor deux fois de
suite.

`--pour decor_5r_akira_ajout.cmd` leve la reservation A CONDITION que ce soit
la seule raison, et que les seuls lanceurs qui citent le code soient celui-la
et ses compagnons (`*_retirer.cmd`). Une raison de MOTEUR -- vrai decor, case
de la grille, apercu en dur -- ne se leve pas : seul `--forcer` passe outre.

Ce que `--vers` fait EN PLUS d'une copie renommee : l'archive `.farc` nomme ses
deux entrees internes (`stgdjo_obj.bin`, `stgdjo_tex.bin`) et `obj_db.bin` les
cherche sous le nom de l'emplacement (id 51 -> `stgevo00_obj.bin`). Les deux noms
sont donc reecrits DANS L'EN-TETE de l'archive -- un `FArC` porte sa taille
d'en-tete en gros-boutien en `+0x04`, et on ne touche a RIEN au-dela : la meme
chaine apparait plus loin dans les donnees, et l'ecraser corromprait le flux.
Les codes font trois lettres des deux cotes : substitution en place, aucune
taille ne bouge.

Le reste de la mise en place est dans le moteur, pas ici : l'emplacement doit
apprendre les identifiants d'objets du decor importe et sa collision.
`patch_moteur.py --variantes-djo` s'en charge.

L'ECLAIRAGE VIENT D'UNE AUTRE SOURCE QUE LA GEOMETRIE : `--eclairage <source>`

    py -3 tools/importer_decor.py --poser djo --source VF5R --vers trm \
        --eclairage VF5FS_LIND

Mesure du 2026-09-08, apres une capture de Frederic : « l'eclairage de la
version 5R n'est pas bon ». Il l'etait pourtant, au sens ou il etait bien lu --
c'est la CAUSE, pas le symptome. Les fichiers de VF5 R sont ecrits pour le
rendu de 2008 et l'image sort surexposee dans celui de 2010 :

    glow_djo.txt            Final Showdown        VF5 R
      exposure                 2.00                 2.80
      flare                    0.30 0.00 1.00       1.00 1.00 0.50
      intensity                1.00 1.00 1.00       0.90 0.90 0.90
    light_djo.txt
      specular (lumiere 0)     1.00                 2.00

`--eclairage` prend les cinq pieces d'eclairage (`.ibl` et les quatre
`light_param`) chez une AUTRE generation que la geometrie. Avec
`--eclairage VF5FS_LIND`, le decor garde ses modeles et ses textures de 2008 et
recoit les reglages que Final Showdown a tailles pour son propre rendu.

Ne pas confondre avec `--sans-eclairage`, qui ne pose RIEN : sur un emplacement
recycle, cela laisserait l'eclairage du decor d'essai, pas celui du dojo.
"""
import os
import shutil
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
SOURCES = os.path.join(RACINE, 'extracted', 'decors')
MEDIA = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media')
PAR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_data.par')


def pieces(code, avec_eclairage=True):
    """Rend [(sous-dossier source, nom, sous-dossier destination), ...].

    La destination est relative a `vf5fs_media/rom/`. L'ordre suit les etats du
    chargeur : geometrie, collision, animation, effets, puis eclairage.
    """
    c, C = code.lower(), code.upper()
    lot = [
        ('objset', 'stg%s.farc' % c, 'objset'),
        ('coli', 'STG%s_COLI.000.bin' % C, ''),
        ('auth_3d', 'STG%s.farc' % C, 'auth_3d'),
        ('auth_3d', 'EFFSTG%s.farc' % C, 'auth_3d'),
    ]
    if avec_eclairage:
        lot.append(('ibl', '%s.ibl' % c, 'ibl'))
        for p in ('light', 'fog', 'glow', 'wind'):
            lot.append(('light_param', '%s_%s.txt' % (p, c), 'light_param'))
    return lot


def renommer_farc(chemin, avant, apres):
    """Reecrit `avant` -> `apres` DANS L'EN-TETE d'une archive FArC/FArc.

    L'en-tete porte sa propre longueur en `+0x04`, en GROS-BOUTIEN. On s'y
    arrete : la meme chaine reapparait dans le flux de donnees (a 0x4C dans le
    `stgdjo.farc` de VF5 R) et l'y ecraser corromprait l'archive.
    """
    with open(chemin, 'r+b') as fp:
        tete = fp.read(8)
        if tete[:4] not in (b'FArC', b'FArc', b'FARC'):
            print('  (%s n\'est pas une archive FArC, noms non touches)'
                  % os.path.basename(chemin))
            return 0
        fin = int.from_bytes(tete[4:8], 'big')
        if not 8 < fin < 0x10000:
            print('  REFUS : taille d\'en-tete invraisemblable (%d)' % fin)
            return -1
        fp.seek(0)
        entete = bytearray(fp.read(fin))
        n = entete.count(avant)
        if not n:
            print('  REFUS : %r absent de l\'en-tete' % avant.decode())
            return -1
        entete[:] = entete.replace(avant, apres)
        fp.seek(0)
        fp.write(entete)
    return n


def par(action, noms):
    cmd = [sys.executable, os.path.join(ICI, 'par_masquer.py'), action] + noms
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout.rstrip())
    if r.returncode:
        print(r.stderr.rstrip())
    return r.returncode


def etat(code, avec_eclairage=True):
    print('--- fichiers libres deposes ---')
    for _, nom, dest in pieces(code, avec_eclairage):
        p = os.path.join(MEDIA, 'rom', dest, nom)
        print('  %-28s %s' % (nom, ('%d o' % os.path.getsize(p))
                              if os.path.exists(p) else 'absent'))
    print('--- index du .par ---')
    return par('--lister', [n for _, n, _ in pieces(code, avec_eclairage)])


def raisons_de_prise(vers):
    """Les raisons etiquetees d'`emplacements.py --pourquoi`, ou None.

    None = l'outil n'a pas repondu ; [] = l'emplacement est libre.
    """
    r = subprocess.run(
        [sys.executable, os.path.join(ICI, 'emplacements.py'), '--pourquoi',
         vers], capture_output=True, text=True)
    if r.returncode:
        return None
    return [l.strip() for l in r.stdout.splitlines() if l.strip()]


def reservation_a_nous(raisons, pour):
    """`pour` est-il le SEUL lanceur a citer cet emplacement ?

    Vrai seulement si toutes les raisons sont des citations par un lanceur, et
    si chacun de ces lanceurs est `pour` lui-meme ou l'un de ses compagnons
    (`<souche>_retirer.cmd`, `<souche>_*.cmd`).
    """
    if not pour or not raisons:
        return False
    souche = os.path.basename(pour)
    if souche.lower().endswith('.cmd'):
        souche = souche[:-4]
    for r in raisons:
        if not r.startswith('lanceur '):
            return False               # une raison de MOTEUR : elle ne se leve pas
        nom = r.split(None, 1)[1]
        if not nom.lower().startswith(souche.lower()):
            return False
    return True


def emplacement_libre(vers, forcer=False, pour=None):
    """`vers` est-il un emplacement d'essai que rien n'utilise deja ?

    La regle du chantier : on AJOUTE des decors, on n'en REMPLACE aucun --
    sauf, eventuellement, les decors d'essai. Encore faut-il savoir lesquels le
    sont vraiment, et `trm` a coute cher pour l'avoir suppose : c'est le decor
    TERMINAL, repare et valide le 2026-09-05, et treize de nos lanceurs
    l'utilisent.

    `emplacements.py` le MESURE (forme du descripteur, grille, apercus, nos
    propres lanceurs). Ce garde-fou vise MA faute, pas l'utilisateur :
    `--forcer` passe outre, en le disant.
    """
    sys.path.insert(0, ICI)
    try:
        import emplacements
    except ImportError:
        return True                      # pas d'outil, pas de garde-fou
    libres = subprocess.run(
        [sys.executable, os.path.join(ICI, 'emplacements.py'), '--libres'],
        capture_output=True, text=True)
    if libres.returncode:
        return True
    dispo = libres.stdout.split()
    if vers.lower() in dispo:
        return True
    # SA PROPRE RESERVATION. Un lanceur qui nomme l'emplacement qu'il pose le
    # rend « pris » aux yeux de la preuve 4 -- y compris pour lui-meme.
    raisons = raisons_de_prise(vers)
    if reservation_a_nous(raisons, pour):
        print('L emplacement « %s » n est reserve que par %s : on passe.'
              % (vers, ', '.join(r.split(None, 1)[1] for r in raisons)))
        return True
    print('REFUS : l emplacement « %s » n est pas libre.' % vers)
    print()
    subprocess.run([sys.executable, os.path.join(ICI, 'emplacements.py')])
    print()
    print('On AJOUTE des decors, on n en REMPLACE aucun -- sauf les decors')
    print('d essai encore inutilises. Reprenez un code de la liste LIBRES.')
    if not forcer:
        print('(--forcer passe outre, en connaissance de cause.)')
    return bool(forcer)


def poser(code, source, avec_eclairage=True, vers=None, eclairage=None,
          forcer=False, pour=None):
    src = os.path.join(SOURCES, source)
    if not os.path.isdir(src):
        print('source introuvable : %s' % src)
        return 1
    if vers and not emplacement_libre(vers, forcer, pour):
        return 4
    # L'eclairage peut venir d'une AUTRE generation que la geometrie : les
    # reglages de 2008 sortent surexposes dans le rendu de 2010.
    src_ecl = src
    if eclairage:
        src_ecl = os.path.join(SOURCES, eclairage)
        if not os.path.isdir(src_ecl):
            print('source d eclairage introuvable : %s' % src_ecl)
            return 1
    lot = pieces(code, avec_eclairage)
    base = len(pieces(code, False))          # ou commence l'eclairage

    def depuis(k):
        return src if k < base else src_ecl

    manquants = [n for k, (d, n, _) in enumerate(lot)
                 if not os.path.exists(os.path.join(depuis(k), d, n))]
    if manquants:
        print('REFUS : %s ne fournit pas le jeu complet, il manque :' % source)
        for n in manquants:
            print('   %s' % n)
        print('\nUn decor s\'importe avec sa generation ENTIERE : melanger deux')
        print('generations est exactement ce qui a fait boucler l\'essai du')
        print('2026-09-03 sur l\'ecran de chargement.')
        return 2
    # Sans `--vers`, la destination porte les memes noms que la source : on
    # REMPLACE le decor. Avec, on l'AJOUTE sur un emplacement libre.
    cibles = pieces(vers or code, avec_eclairage)
    for k, ((d, nom, dest), (_, nom2, _)) in enumerate(zip(lot, cibles)):
        rep = os.path.join(MEDIA, 'rom', dest)
        os.makedirs(rep, exist_ok=True)
        shutil.copy2(os.path.join(depuis(k), d, nom), os.path.join(rep, nom2))
        marque = '' if depuis(k) is src else '   [%s]' % eclairage
        if nom == nom2:
            print('pose  %-28s -> rom/%s%s' % (nom, dest, marque))
        else:
            print('pose  %-28s -> rom/%s/%s%s' % (nom, dest, nom2, marque))
    if vers:
        # obj_db.bin cherche les deux entrees internes sous le nom de
        # l'emplacement, pas sous celui de la source.
        farc = os.path.join(MEDIA, 'rom', 'objset', 'stg%s.farc' % vers.lower())
        n = renommer_farc(farc, code.lower().encode('ascii'),
                          vers.lower().encode('ascii'))
        if n < 0:
            return 3
        print('en-tete de stg%s.farc : %d nom(s) reecrit(s) en stg%s_*'
              % (vers.lower(), n, vers.lower()))
    print()
    return par('--masquer', [n for _, n, _ in cibles])


def retirer(code, avec_eclairage=True):
    lot = pieces(code, avec_eclairage)
    r = par('--rendre', [n for _, n, _ in lot])
    print()
    for _, nom, dest in lot:
        p = os.path.join(MEDIA, 'rom', dest, nom)
        if os.path.exists(p):
            os.remove(p)
            print('retire %s' % nom)
    return r


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1
    source = 'VF5R'
    if '--source' in argv:
        i = argv.index('--source')
        source = argv[i + 1]
        del argv[i:i + 2]
    vers = None
    if '--vers' in argv:
        i = argv.index('--vers')
        vers = argv[i + 1]
        del argv[i:i + 2]
    forcer = '--forcer' in argv
    argv = [a for a in argv if a != '--forcer']
    pour = None
    if '--pour' in argv:
        i = argv.index('--pour')
        pour = argv[i + 1]
        del argv[i:i + 2]
    eclairage = None
    if '--eclairage' in argv:
        i = argv.index('--eclairage')
        eclairage = argv[i + 1]
        del argv[i:i + 2]
    ecl = '--sans-eclairage' not in argv
    argv = [a for a in argv if a != '--sans-eclairage']
    if not os.path.exists(PAR):
        print('archive introuvable : %s' % PAR)
        return 1
    for action, fonction in (('--etat', etat), ('--poser', poser),
                             ('--retirer', retirer)):
        if action in argv:
            i = argv.index(action)
            if i + 1 >= len(argv):
                print('%s attend un code de decor (djo, dur, sin, ...)' % action)
                return 1
            code = argv[i + 1]
            if fonction is poser:
                return poser(code, source, ecl, vers, eclairage, forcer, pour)
            return fonction(code, ecl)
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
