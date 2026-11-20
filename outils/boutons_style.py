#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE STYLE DES PASTILLES DE BOUTONS : PS3, PS5, XBOX 360, Xbox One.

Ce que la ligne « Buttons style » d OPTIONS > Controls demande, c est ce
fichier qui le POSE. Deux gestes, et ils sont de nature differente :

  1. **LA PLANCHE** `rom/2d/spr_n_fnt32.farc` -- ses pastilles, en pixels ;
  2. **LA TABLE DE CHAINES** `rom/string_array.farc` -- quel glyphe chaque
     libelle demande.

CE QUE LE JEU PORTE DEJA, et c est la table des echappements qui le dit
(`analysis/polices_et_pictos.md`) : la planche a **DEUX** jeux de pastilles --
`U+E000`-`E003` (B, A, Y, X : **Xbox**) et `U+E015`-`E018` (○, ✕, △, □ :
**PS3**). Les libelles du jeu visent le bloc PS3 ; `tools/pictos_xbox.py` les
fait viser le bloc Xbox. **Passer de PS3 a XBOX 360 ne demande donc AUCUN
dessin** : c est un changement de table, rien d autre.

Les autres styles REPEIGNENT le bloc PS3 de la planche -- c est ce que
Frederic a fait pour la PS5 et la Xbox One. La PS4 attend la sienne.

| style | planche | table de chaines |
|---|---|---|
| `ps3` | d origine | d origine (bloc PS3) |
| `ps5` | `spr_n_fnt32__tex00_PS5.png` | d origine |
| `xone` | `spr_n_fnt32__tex00_xboxone.png` | d origine |
| `x360` | d origine | `pictos_xbox --poser` (bloc Xbox) |
| `ps4` | **absente** | refus |

POURQUOI LES ARCHIVES SONT GARDEES EN CACHE. Reencoder une planche de
2048 x 2048 en DXT5 prend quelques secondes ; ce n est pas grand-chose, mais
le lanceur le ferait a CHAQUE demarrage. On les construit donc une fois dans
`extracted/fnt32_<style>.farc` et on recopie ensuite.

ET LE JEU DOIT ETRE FERME : la planche est RESIDENTE -- mesure du 2026-10-11,
echangee en cours de partie elle ne change rien a l ecran. Le choix ne
s applique qu au lancement suivant.

    py -3 tools/boutons_style.py --etat
    py -3 tools/boutons_style.py --poser x360
"""
import io
import os
import shutil
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
DEUXD = os.path.join(JEU, 'vf5fs_media', 'rom', '2d')
PLANCHE = os.path.join(DEUXD, 'spr_n_fnt32.farc')
CACHE = os.path.join(RACINE, 'extracted')
HD2D = os.path.join(RACINE, 'HD_TEXTURES', 'HD', '2D')
ETAT = os.path.join(JEU, 'ram', 'boutons.txt')

# LA TABLE EST CELLE DU MENU, pas une copie : `options_v2.BOUTONS` porte
# (clef, nom affiche, suffixe du PNG ou None, table Xbox ?), et c est le meme
# indice qui circule du menu a `apm.dll` et jusqu ici.
import options_v2 as ov2                                    # noqa: E402
STYLES = ov2.BOUTONS


def _png(suffixe):
    return os.path.join(HD2D, 'spr_n_fnt32__tex00_%s.png' % suffixe)


def dispo(clef):
    """Un style est disponible si sa planche existe -- ou s il n en veut pas."""
    for c, _n, suf, _x in STYLES:
        if c == clef:
            return suf is None or os.path.exists(_png(suf))
    return False


ORIGINE = os.path.join(CACHE, 'fnt32_origine.farc')


def _origine():
    """La planche D ORIGINE, et on ne la devine pas.

    DEFAUT DU 2026-10-11 : le style `ps3` se construisait en recopiant « ce
    qui est en place », et ce qui etait en place etait la planche Xbox One
    qu on venait de poser. Le cache `fnt32_ps3.farc` portait donc l art de la
    Xbox One, et « revenir en PS3 » ne revenait a rien.

    L original est garde une fois pour toutes dans `extracted/`, et c est LUI
    la reference -- pour `ps3` comme pour le point de depart des repeintes.
    """
    if not os.path.exists(ORIGINE):
        depart = PLANCHE + '.origine'
        if not os.path.exists(depart):
            depart = PLANCHE
        if os.path.exists(ETAT):
            raise SystemExit(
                'REFUS : un style est deja pose et %s manque -- on ne sait '
                'plus ou est la planche d origine. Rendez-la depuis le .par '
                'avant de continuer.' % ORIGINE)
        os.makedirs(CACHE, exist_ok=True)
        shutil.copyfile(depart, ORIGINE)
    return ORIGINE


def _construire(clef, suf):
    """Fabrique l archive du style et la garde en cache.

    On passe par `textures_hd.py`, qui sait relire le TXP, reencoder au FORMAT
    D ORIGINE, refaire les niveaux de mip et REECRIRE L ARCHIVE DANS SA FORME
    (`FArC` ici -- poser un `FArc` brut a sa place ferme le jeu, mesure du
    2026-10-11).

    ON PART TOUJOURS DE L ORIGINAL : la planche en place peut deja porter un
    autre style, et repeindre par-dessus ferait perdre un niveau de qualite a
    chaque passage.
    """
    cible = os.path.join(CACHE, 'fnt32_%s.farc' % clef)
    if os.path.exists(cible):
        return cible
    orig = _origine()
    if suf is None:
        shutil.copyfile(orig, cible)
        return cible
    shutil.copyfile(orig, PLANCHE)
    if os.path.exists(PLANCHE + '.origine'):
        os.remove(PLANCHE + '.origine')
    tmp = os.path.join(HD2D, 'spr_n_fnt32__tex00.png')
    deja = os.path.exists(tmp)
    if deja:
        raise SystemExit('un spr_n_fnt32__tex00.png traine dans HD/2D ; '
                         'otez-le, il serait pris pour une version HD')
    shutil.copyfile(_png(suf), tmp)
    try:
        print('   construction de la planche %s...' % clef)
        r = subprocess.run([sys.executable,
                            os.path.join(ICI, 'textures_hd.py'), '--poser'],
                           capture_output=True, text=True)
        if r.returncode:
            raise SystemExit((r.stdout or r.stderr)[-500:])
        shutil.copyfile(PLANCHE, cible)
    finally:
        os.remove(tmp)
        subprocess.run([sys.executable,
                        os.path.join(ICI, 'textures_hd.py'), '--retirer'],
                       capture_output=True, text=True)
        shutil.copyfile(orig, PLANCHE)
    return cible


def poser(clef):
    t = [s for s in STYLES if s[0] == clef]
    if not t:
        raise SystemExit('style inconnu : %s (connus : %s)'
                         % (clef, ', '.join(s[0] for s in STYLES)))
    _c, nom, suf, xbox = t[0]
    if not dispo(clef):
        print('REFUS : %s n a pas de planche. Posez %s dans HD_TEXTURES/HD/2D.'
              % (nom, os.path.basename(_png(suf))))
        return 2
    if os.path.exists(os.path.join(JEU, 'vfes.exe')) and _tourne():
        print('REFUS : le jeu tourne. La planche est RESIDENTE -- la changer '
              'maintenant ne se verrait pas, et reecrire un fichier qu il '
              'lit est inutilement risque.')
        return 2
    arch = _construire(clef, suf)
    shutil.copyfile(arch, PLANCHE)
    print('   planche : %s (%d octets)' % (os.path.basename(arch),
                                           os.path.getsize(PLANCHE)))
    r = subprocess.run([sys.executable, os.path.join(ICI, 'pictos_xbox.py'),
                        '--poser' if xbox else '--retirer'],
                       capture_output=True, text=True)
    sortie = (r.stdout or r.stderr).strip().split(chr(10))
    print('   table de chaines : %s' % (sortie[-1] if sortie else '?'))
    os.makedirs(os.path.dirname(ETAT), exist_ok=True)
    io.open(ETAT, 'w', encoding='ascii', newline=chr(10)).write(clef + chr(10))
    print()
    print('Style pose : %s. Il sera visible au prochain lancement.' % nom)
    return 0


def _tourne():
    r = subprocess.run(['tasklist', '/fi', 'imagename eq vfes.exe'],
                       capture_output=True, text=True)
    return 'vfes.exe' in (r.stdout or '')


def etat():
    courant = ''
    if os.path.exists(ETAT):
        courant = io.open(ETAT, encoding='ascii').read().strip()
    print('style       nom              planche     en place')
    for c, nom, suf, _x in STYLES:
        print('   %-8s %-16s %-11s %s'
              % (c, nom, 'oui' if dispo(c) else 'MANQUE',
                 '<--' if c == courant else ''))
    if not courant:
        print()
        print('Aucun style pose par cet outil ; le jeu porte ce que le '
              'dernier correctif y a laisse.')
    return 0


def main(argv):
    if '--etat' in argv:
        return etat()
    if '--poser' in argv:
        i = argv.index('--poser') + 1
        if i >= len(argv):
            print('--poser attend un style : %s'
                  % ', '.join(s[0] for s in STYLES))
            return 1
        return poser(argv[i].lower())
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
