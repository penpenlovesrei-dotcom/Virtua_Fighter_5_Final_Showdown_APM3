"""Where the item archives of each game live, and how to read them.

VF5 (2007)  : plain files  <game>/media/objset_x36/<code>itm.farc
FS base     : XBLA package  media/rom/objset/<code>itm.farc
FS DLC      : DLC package   media/rom/objset/<code>itm_patch.farc

OU VIVENT LES DONNEES -- et pourquoi il y a une LISTE de candidats.

Ces scripts ont ete ecrits le 2026-09-13 dans `Desktop\\SEPTEMBRE\\VF5 CUSTOM
DLC`, ou ils resolvaient tout par rapport a leur propre dossier. Replies dans
VF5RE le 2026-09-27, les donnees elles n'ont pas bouge : quatorze gigaoctets
de paquets Xbox 360 et d'extractions n'ont rien a faire dans un depot, qui
plus est public.

Mesure du 2026-09-27 : DEUX de ces trois sources existaient DEJA en double sur
le Bureau, a l'octet pres --

    le media de VF5 (2007), 1 285 fichiers, 3,59 Go
        `VF5 FS DECOMP\\X360_VF5\\media`
        `SEPTEMBRE\\VF5 CUSTOM DLC\\Virtua Fight3r 5 AnDreXplay\\...\\media`
    le paquet XBLA de Final Showdown + sa TU1, 2,05 Go
        `VF5RE\\extracted\\X360_FS\\Virtua Fighter 5 Final Showdown + TU1`
        `SEPTEMBRE\\VF5 CUSTOM DLC\\Virtua Fighter 5 Final Showdown + TU1`

Chaque source est donc cherchee dans PLUSIEURS emplacements, et on prend le
premier qui existe. Effacer l'une des deux copies ne casse alors rien -- et
c'etait le but : Frederic a demande la liste des doublons pour faire du
menage. Seul le paquet DLC (2 Go) n'existe qu'a un seul endroit.

`VF5_DLC_RACINE` reste prioritaire si on veut tout forcer ailleurs.
"""
import os
import re

from stfs import Stfs

BUREAU = os.path.join('C:' + os.sep, 'Users', 'frede', 'Desktop')

# LES RACINES POSSIBLES, dans l'ordre. Frederic a recopie le paquet DLC dans
# `VF5 FS DECOMP\X360_VF5_DLC` le 2026-09-27 (copie verifiee au SHA-256 sur
# les 2 075 852 800 octets) pour pouvoir effacer `SEPTEMBRE\VF5 CUSTOM DLC`.
# On cherche donc dans les deux, et `VF5_DLC_RACINE` passe devant.
RACINES = [os.path.join(BUREAU, 'SEPTEMBRE', 'VF5 CUSTOM DLC'),
           os.path.join(BUREAU, 'VF5 FS DECOMP', 'X360_VF5_DLC')]
if os.environ.get('VF5_DLC_RACINE'):
    RACINES.insert(0, os.environ['VF5_DLC_RACINE'])
# ROOT sert aux dossiers d'EXTRACTION : le premier qui existe, sinon le
# dernier -- jamais un dossier disparu, sinon une extraction ressusciterait
# l'arborescence effacee.
ROOT = next((r for r in RACINES if os.path.isdir(r)), RACINES[-1])


def _premier(quoi, candidats, dossier=False):
    """Le premier candidat qui existe, ou un refus qui DIT ou l'on a cherche."""
    for c in candidats:
        if (os.path.isdir(c) if dossier else os.path.exists(c)):
            return c
    raise SystemExit(
        '%s : introuvable. Cherche dans :%s%s%sPosez VF5_DLC_RACINE si les '
        'donnees sont ailleurs.'
        % (quoi, os.linesep,
           os.linesep.join('    ' + c for c in candidats), os.linesep))


# 1. le media de VF5 (2007) -- fichiers en clair
VF5_MEDIA = _premier('Le media de VF5 (2007)',
    [os.path.join(r, 'Virtua Fight3r 5 AnDreXplay', 'Virtua Fighter 5',
                  'media') for r in RACINES]
    + [os.path.join(BUREAU, 'VF5 FS DECOMP', 'X360_VF5', 'media')],
    dossier=True)

# 2. le paquet XBLA de Final Showdown (jeu de base)
_FS_SOUS = os.path.join('584111FE', '000D0000',
                        '7D2DF36BD11FB8394C3D652339E6FE1DA1337B1058')
FS_PKG = _premier('Le paquet XBLA de Final Showdown',
    [os.path.join(r, 'Virtua Fighter 5 Final Showdown + TU1', _FS_SOUS)
     for r in RACINES]
    + [os.path.join(BUREAU, 'VF5RE', 'extracted', 'X360_FS',
                    'Virtua Fighter 5 Final Showdown + TU1', _FS_SOUS)])
FS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(FS_PKG)))

# 3. le paquet DLC -- il n'existe qu'a UN seul endroit
DLC_PKG = _premier('Le paquet DLC de Final Showdown',
    [os.path.join(r, '408E3ECB28995A39BDE17B9A51EFE5A273B5825158')
     for r in RACINES])

# Les extractions brutes restent la ou `extract_raw.py` les a ecrites ; elles
# se refabriquent, c'est pour cela qu'elles ne sont pas cherchees ailleurs.
GAMES = {
    "vf5": dict(label="VF5 (2007)",
                extract_dir=os.path.join(ROOT, "Virtua Fight3r 5 AnDreXplay",
                                         "EXTRACTION")),
    # Toujours sous ROOT, JAMAIS a cote du paquet : si le paquet retenu est
    # celui de `VF5RE\extracted`, une extraction de 1,1 Go tomberait dans le
    # depot -- qui est public.
    "fs": dict(label="FS (jeu de base)",
               extract_dir=os.path.join(
                   ROOT, "Virtua Fighter 5 Final Showdown + TU1",
                   "EXTRACTION")),
    "dlc": dict(label="FS (DLC)", extract_dir=os.path.join(ROOT, "EXTRACTION")),
}

ARCHIVE_RE = re.compile(r"(\w{3})itm(?:_patch)?\.farc|itmcmn\.farc")


def archives(game):
    """Yield (code, archive name, loader) for every item archive of a game.

    code is the 3-letter character code, or "cmn" for the shared itmcmn archive.
    loader() returns the archive bytes.
    """
    if game == "vf5":
        folder = os.path.join(VF5_MEDIA, "objset_x36")
        for name in sorted(os.listdir(folder)):
            m = ARCHIVE_RE.fullmatch(name)
            if m:
                path = os.path.join(folder, name)
                yield (m.group(1) or "cmn"), name, (lambda p=path: open(p, "rb").read())
        return
    pkg = {"fs": FS_PKG, "dlc": DLC_PKG}[game]
    s = Stfs(pkg)
    for e in s.file_table():
        if e["is_dir"] or not e["path"].startswith("media/rom/objset/"):
            continue
        m = ARCHIVE_RE.fullmatch(e["name"])
        if m:
            yield (m.group(1) or "cmn"), e["name"], (lambda e=e: b"".join(s.iter_file(e)))
