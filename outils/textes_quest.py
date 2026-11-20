#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""LES TEXTES DU QUEST, AJOUTES A LA TABLE DE FINAL SHOWDOWN.

Frederic, 2026-09-12, entre deux voies : « 1 » -- les ajouter au
`string_array.farc` de FS, comme `bases_2d.py` a ajoute les planches. La voie
fidele : le texte devient une donnee du jeu, et le moteur le resout seul.

ON AJOUTE, ON NE REMPLACE RIEN. Les 23 052 identifiants de Final Showdown
gardent leur numero et leur contenu ; les chaines du Quest sont posees A LA
SUITE, sur les numeros libres.

LE FORMAT, mesure le 2026-09-12
-------------------------------
`rom/string_array.farc` (1 165 900 octets dans le `.par`, non comprime) est un
FArc de deux membres : `string_array_en.bin` (472 944 o) et
`string_array_jp.bin` (692 888 o). Chacun est :

    un tableau de u32 GROS-BOUTISTES : l'offset ABSOLU de la chaine, depuis le
    debut du membre ; puis les chaines UTF-8, terminees par un zero.

Le premier offset donne donc la longueur du tableau. Il y a **23 052 entrees
utiles (0 a 23 051), puis DEUX zeros** : c'est le premier zero qui borne le
chargeur (`FUN_1801EFDD0` convertit chaque entree -- echange d'octets, puis
offset absolu -> ecart relatif a sa propre case -- et s'arrete des qu'une case
vaut zero). Et 23 052 est exactement `0x5A0C`, la borne du getter
`0x1801EFD10`. Les deux se tiennent.

CE QUE CET OUTIL FAIT
---------------------
1. extrait `string_array.farc` du `.par` ;
2. ajoute les chaines du Quest a la suite des 23 052, dans LES DEUX membres
   (le meme texte anglais dans les deux : Frederic garde le jeu en anglais) ;
3. remet deux zeros a la fin, pour borner le chargeur comme avant ;
4. ecrit `vf5fs_media/rom/string_array.farc` et MASQUE le nom dans le `.par`
   (le `.par` passe avant le disque : voir `bases_2d.py`) ;
5. ecrit `tools/quest_textes_map.h`, la table {identifiant Xbox -> identifiant
   FS} que `quest_runtime.c` inclut.

Le moteur, lui, doit accepter les nouveaux numeros :
`patch_moteur.py --textes-quest` monte la borne du getter.

    py -3 tools/textes_quest.py --ajouter
    py -3 tools/textes_quest.py --controle
    py -3 tools/textes_quest.py --retirer
"""
import os
import struct
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import par_inventaire                                       # noqa: E402
import quest_textes                                         # noqa: E402

PAR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_data.par')
ROM = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media', 'rom')
CIBLE = os.path.join(ROM, 'string_array.farc')
CARTE = os.path.join(ICI, 'quest_textes_map.h')
NOM_PAR = 'string_array.farc'
MEMBRES = ('string_array_en.bin', 'string_array_jp.bin')
FS_ENTREES = 23052          # 0x5A0C : les identifiants de Final Showdown
FS_ZEROS = 2                # les deux cases nulles qui bornent le chargeur


class Refus(Exception):
    pass


# ---------------------------------------------------------------------------
# le FArc, et un membre
# ---------------------------------------------------------------------------
def farc_lire(d):
    """Rend [(nom, octets)] d'un FArc non comprime."""
    if d[:4] != b'FArc':
        raise Refus('pas un FArc : %s' % d[:4])
    entete = struct.unpack_from('>I', d, 4)[0]
    out = []
    o = 0x0C
    while o < entete + 8:
        f = d.index(b'\x00', o)
        nom = d[o:f].decode('latin-1')
        o = f + 1
        if not nom or o + 8 > len(d):
            break
        a, t = struct.unpack_from('>II', d, o)
        o += 8
        out.append((nom, d[a:a + t]))
    return out


def farc_ecrire(membres, alignement=1):
    """Rebatit un FArc non comprime. Meme disposition que l'original :
    en-tete {'FArc', taille de l'en-tete, alignement}, puis, par membre, le
    nom termine par zero, l'offset et la taille en gros-boutien."""
    entete = 0x0C
    for nom, _ in membres:
        entete += len(nom) + 1 + 8
    entete -= 8                       # la taille annoncee exclut le dernier
    debut = entete + 8
    corps = bytearray()
    places = []
    for _, oct_ in membres:
        while (debut + len(corps)) % 4:
            corps += b'\x00'
        places.append(debut + len(corps))
        corps += oct_
    d = bytearray(b'FArc')
    d += struct.pack('>II', entete, alignement)
    for (nom, oct_), a in zip(membres, places):
        d += nom.encode('latin-1') + b'\x00' + struct.pack('>II', a, len(oct_))
    while len(d) < debut:
        d += b'\x00'
    d += corps
    return bytes(d)


def table_lire(b):
    """Le membre -> la liste des chaines (bytes), zeros compris."""
    prem = struct.unpack_from('>I', b, 0)[0]
    n = prem // 4
    out = []
    for i in range(n):
        o = struct.unpack_from('>I', b, 4 * i)[0]
        if o == 0:
            out.append(None)
            continue
        out.append(b[o:b.index(b'\x00', o)])
    return out


def table_ecrire(chaines):
    """La liste -> le membre. Les chaines EGALES partagent leur place, comme
    dans l'original (deux entrees y pointent souvent le meme texte)."""
    n = len(chaines)
    debut = n * 4
    donnees = bytearray()
    ou = {}
    table = []
    for s in chaines:
        if s is None:
            table.append(0)
            continue
        if s not in ou:
            ou[s] = debut + len(donnees)
            donnees += s + b'\x00'
        table.append(ou[s])
    d = bytearray()
    for v in table:
        d += struct.pack('>I', v)
    return bytes(d + donnees)


# ---------------------------------------------------------------------------
# le `.par`
# ---------------------------------------------------------------------------
def par_masquer(action):
    r = subprocess.run([sys.executable, os.path.join(ICI, 'par_masquer.py'),
                        action, NOM_PAR], capture_output=True, text=True)
    if r.returncode:
        raise Refus('par_masquer %s : %s' % (action, (r.stdout or '') +
                                             (r.stderr or '')))
    return r.stdout


def par_masquee():
    _, fichiers = par_inventaire.lire(PAR)
    noms = set(n for n, *_ in fichiers)
    return NOM_PAR not in noms and NOM_PAR[:-1] + '_' in noms


def par_extraire():
    """Les octets de `string_array.farc`, tels que le `.par` les porte."""
    _, fichiers = par_inventaire.lire(PAR)
    for nom, taille, comp, offset, comprime in fichiers:
        if nom not in (NOM_PAR, NOM_PAR[:-1] + '_'):
            continue
        if comprime:
            raise Refus('%s est comprime dans le .par' % nom)
        with open(PAR, 'rb') as fp:
            fp.seek(offset)
            return fp.read(taille)
    raise Refus('%s introuvable dans le .par' % NOM_PAR)


# ---------------------------------------------------------------------------
def textes_du_quest(langue='en'):
    """{identifiant Xbox: chaine} -- l'inventaire de `quest_textes.py`."""
    import quest_x360 as qx
    img = qx.Image()
    tab = quest_textes.chaines(langue)
    fonctions = img.fonctions()
    debuts = [f for f, _ in fonctions]
    ens = set(debuts)
    racines = set()
    for nom, vts in img.classes().items():
        if not nom.startswith(('TaskQuest', 'TaskTournament', 'TaskItemShop',
                               'TaskEmblemEdit', 'TaskNewEmblemList',
                               'TaskNewItemList', 'TaskGameItemFight',
                               'TaskGameRank', 'TaskLiveRankingUpdate',
                               'TaskRankingUpdate', 'QuestAet')):
            continue
        for vt in vts:
            racines.update(img.methodes(vt, ens))
    app, appelants = qx.graphe(img, fonctions)
    quest = qx.propre(racines, app, appelants)
    import bisect
    out = {}
    for site, ident in quest_textes.appels(img):
        k = bisect.bisect_right(debuts, site) - 1
        if k < 0 or debuts[k] not in quest:
            continue
        if ident is None or not (0 <= ident < len(tab)):
            continue
        out[ident] = tab[ident]
    # LES CHARGEMENTS INDIRECTS. Le balayage ci-dessus ne voit que le
    # `li r3, imm` qui precede l'appel ; le menu de la maison du Quest ecrit
    # ses six identifiants dans un tableau de PILE et les relit dans sa
    # boucle. Huit libelles manquaient ainsi le 2026-09-26, dont le titre des
    # fenetres de lieu (535 « EVENT SQUARE ») et deux de ses trois lignes.
    # `quest_textes.immediats` releve tout immediat plausible du MODULE du
    # Quest : une sur-approximation assumee, qui ne deplace aucun numero.
    for ident in quest_textes.immediats(img, quest, debuts):
        if 0 <= ident < len(tab) and tab[ident]:
            out.setdefault(ident, tab[ident])
    return dict(sorted(out.items()))


def ajouter(verbeux=True):
    d = par_extraire()
    membres = farc_lire(d)
    noms = [n for n, _ in membres]
    if noms != list(MEMBRES):
        raise Refus('membres inattendus : %s' % noms)
    quest = textes_du_quest('en')
    neufs = list(quest.items())
    dits = []
    sortie = []
    for nom, oct_ in membres:
        chaines = table_lire(oct_)
        if len(chaines) != FS_ENTREES + FS_ZEROS:
            raise Refus('%s : %d entrees, %d attendues'
                        % (nom, len(chaines), FS_ENTREES + FS_ZEROS))
        if any(c is not None for c in chaines[FS_ENTREES:]):
            raise Refus('%s : les %d dernieres cases ne sont pas nulles'
                        % (nom, FS_ZEROS))
        base = chaines[:FS_ENTREES]
        base += [s.encode('utf-8') for _, s in neufs]
        base += [None] * FS_ZEROS
        sortie.append((nom, table_ecrire(base)))
        dits.append('%s : %d -> %d entrees' % (nom, FS_ENTREES, len(base)))
    os.makedirs(ROM, exist_ok=True)
    with open(CIBLE, 'wb') as fp:
        fp.write(farc_ecrire(sortie))
    if not par_masquee():
        par_masquer('--masquer')
    carte(neufs)
    if verbeux:
        for x in dits:
            print('  ' + x)
        print('  %d chaines du Quest posees aux identifiants %d a %d'
              % (len(neufs), FS_ENTREES, FS_ENTREES + len(neufs) - 1))
        print('  %s ecrit (%d octets) ; %s masque dans le .par'
              % (CIBLE, os.path.getsize(CIBLE), NOM_PAR))
        print('  %s ecrit' % CARTE)
        print('  IL FAUT ENCORE : patch_moteur.py --textes-quest '
              '(la borne du getter passe de %d a %d)'
              % (FS_ENTREES, FS_ENTREES + len(neufs)))
    return len(neufs)


def carte(neufs):
    """La table {identifiant Xbox -> identifiant FS}, pour le C."""
    lignes = ['/* Ecrit par tools/textes_quest.py -- NE PAS EDITER A LA MAIN.',
              ' *',
              ' * Les textes du Quest, ajoutes a la suite des %d de Final'
              % FS_ENTREES,
              ' * Showdown dans `rom/string_array.farc`. A gauche le numero de',
              ' * la version Xbox 360 (2007), a droite le notre.',
              ' */',
              '#define QUEST_TEXTE_BASE   %d' % FS_ENTREES,
              '#define QUEST_TEXTE_NOMBRE %d' % len(neufs),
              '',
              'static const struct { int x360, fs; } g_quest_textes[] = {']
    for k, (ident, s) in enumerate(neufs):
        court = s.replace('\n', ' ')[:44]
        court = ''.join(c if 32 <= ord(c) < 127 else '.' for c in court)
        lignes.append('    { %5d, %5d },   /* %s */' % (ident, FS_ENTREES + k,
                                                        court))
    lignes += ['};', '']
    with open(CARTE, 'w', encoding='ascii', newline='\n') as fp:
        fp.write('\n'.join(lignes))


def controle():
    fautes = []
    if not os.path.exists(CIBLE):
        fautes.append('%s absent' % CIBLE)
    else:
        membres = farc_lire(open(CIBLE, 'rb').read())
        if [n for n, _ in membres] != list(MEMBRES):
            fautes.append('membres inattendus dans %s' % CIBLE)
        else:
            for nom, oct_ in membres:
                t = table_lire(oct_)
                if len(t) <= FS_ENTREES + FS_ZEROS:
                    fautes.append('%s : %d entrees, pas d ajout'
                                  % (nom, len(t)))
                elif t[FS_ENTREES] is None:
                    fautes.append('%s : la case %d est nulle'
                                  % (nom, FS_ENTREES))
                elif any(c is not None for c in t[-FS_ZEROS:]):
                    fautes.append('%s : la table ne finit pas par %d zeros'
                                  % (nom, FS_ZEROS))
    if not par_masquee():
        fautes.append('%s non masque dans le .par' % NOM_PAR)
    if not os.path.exists(CARTE):
        fautes.append('%s absent' % CARTE)
    return fautes


def retirer():
    if os.path.exists(CIBLE):
        os.remove(CIBLE)
    if par_masquee():
        par_masquer('--rendre')
    carte([])          # la carte reste, VIDE : `quest_runtime.c` l'inclut
    print('  textes du Quest retires ; %s rendu au .par' % NOM_PAR)


def main():
    a = sys.argv[1:]
    if '--controle' in a:
        f = controle()
        if f:
            print('textes du Quest : %s' % ' ; '.join(f))
            return 1
        print('textes du Quest : CONFORMES')
        return 0
    if '--retirer' in a:
        retirer()
        return 0
    if '--ajouter' in a:
        ajouter()
        return 0
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
