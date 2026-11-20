#!/usr/bin/env py -3
# -*- coding: utf-8 -*-
r"""Les BASES 2D de FS (`aet_db.bin`, `spr_db.bin`) : les lire, et y AJOUTER
une planche -- celles du mode Quest de VF5 Xbox 360 (2007).

POURQUOI (2026-09-11, etape 3 du mode Quest)

Les ecrans du Quest sont des planches AET et des jeux de sprites que nos
outils lisent DEJA telles quelles (`aet.py`, `txp.py` : meme format qu'APM3,
1280 x 720, textures non tuilees). Pour que le moteur de FS puisse les
charger, il faut qu'elles existent dans ses deux bases.

OU SONT LES BASES, ET COMMENT ON LES LIBERE

Elles ne sont pas sur le disque : le binaire porte une ARCHIVE FArC
EMBARQUEE en `0x1804137F0` (mot_db, obj_db, tex_db, spr_db, aet_db,
rob_mot_tbl, et le decor `tst`). Le resolveur la consulte AVANT le `.par` et
le disque -- c'est ce qui avait fait croire, pour `obj_db`, que nos fichiers
etaient ignores. Le remede est le meme : masquer un octet du nom du membre
dans l'en-tete du FArC embarque (`patch_moteur`, `--bases-2d-libres`), et le
moteur lit alors `./rom/2d/aet_db.bin` et `./rom/2d/spr_db.bin`.

LES DEUX FORMATS, mesures le 2026-09-11

    aet_db   +0x00 nb planches  +0x04 table  +0x08 nb scenes  +0x0C table
             planche 0x14 : {id, nom, fichier, RANG, id du jeu de sprites}
             scene   0x0C : {id, nom, (rang de la planche << 16) | rang}
    spr_db   meme en-tete
             planche 0x10 : {id, nom, fichier, RANG}
             sprite  0x0C : {id, nom, info}
                      info = (rang de la planche << 16) | rang, et le
                      quartet de poids fort 1 = TEXTURE, 0 = sprite

    500 planches AET / 631 scenes ; 593 planches de sprites / 39 903 sprites.
    Identifiants les plus grands : planche AET 525, scene 682, planche de
    sprites 364, sprite 0xD78F. On numerote au-dessus.

CE QUI LIE LES DEUX, et ce qui permet de renumeroter : une video de la
planche AET nomme son sprite (`N_QUE_EFF_PTCL`) ET le designe par son
identifiant (`0x6130`). Chez FS, le sprite du meme nom s'appelle
`SPR_N_QUE_EFF_PTCL`. On ajoute donc les sprites sous ce nom, avec NOS
identifiants, et on reecrit les identifiants dans la copie de la planche.

    py -3 tools/bases_2d.py --lister
    py -3 tools/bases_2d.py --ajouter que
    py -3 tools/bases_2d.py --controle
"""
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)

import subprocess                                             # noqa: E402

import farc                                                   # noqa: E402
import pefile                                                 # noqa: E402

DLL = os.path.join(RACINE, 'runtime', 'media', 'vf5fs',
                   'vf5fs-pxd-w64-Retail_APM3.dll.origine')
MEDIA = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_media')
DEUXD = os.path.join(MEDIA, 'rom', '2d')
FARC_EMBARQUE = 0x4137F0          # rva de l'archive dans le binaire
X360 = os.path.join('C:' + os.sep, 'Users', 'frede', 'Desktop',
                    'VF5 FS DECOMP', 'X360_VF5', 'media', 'lang', 'en', 'rom',
                    '2d')

# Les planches du Quest. `scenes` : le nom de scene tel qu'il est DANS le
# fichier (lu par aet.py), auquel on donne un identifiant neuf.
PLANCHES = {
    'que': dict(aet='aet_n_que.bin', spr='spr_n_que.farc',
                nom='N_QUE', libelle='la carte et les salles du Quest'),
    'qwin': dict(aet='aet_n_qwin.bin', spr='spr_n_qwin.farc',
                 nom='N_QWIN', libelle='les fenetres du Quest'),
    'tnt': dict(aet='aet_n_tnt.bin', spr='spr_n_tnt.farc',
                nom='N_TNT', libelle='les tournois'),
    'tnto': dict(aet='aet_n_tnto.bin', spr='spr_n_tnto.farc',
                 nom='N_TNTO', libelle='les tableaux de tournoi'),
    # LES PICTOS DE GRADE. Mesure du 2026-09-30 : Final Showdown a bien un jeu
    # `SPR_S_GAMDAN` (identifiant 299), mais son contenu n a RIEN a voir --
    # ce sont les effets de l ecran de montee en grade (SPLASH, START_TXT,
    # WAK_OP...). Les pictos de rang, eux, sont dans la planche de 2007, et
    # sous forme de COMPOSITIONS, une par rang : `s_gamdan_kyu01` a `kyu09`,
    # `s_gamdan_dan01` a `dan10`, et vingt-deux titres `s_gamdan_shogo_*`
    # -- quarante et un rangs, exactement l etendue du champ `npc_tbl + 0x7C`
    # (42 valeurs, 0 a 41). On l importe donc sous un nom a nous, `S_QDAN`,
    # pour ne pas heurter celui de FS.
    'qdan': dict(aet='aet_s_gamdan.bin', spr='spr_s_gamdan.farc',
                 # le nom doit rester S_GAMDAN : les videos de la planche
                 # nomment leurs sprites `S_GAMDAN_<sprite>`, et c est par ce
                 # nom que l outil les relie. Sous S_QDAN, 212 liens cassaient.
                 # FS a deja un SPR_S_GAMDAN (299) au contenu different ; les
                 # identifiants, eux, restent uniques.
                 nom='S_GAMDAN', libelle='les pictos de grade du Quest',
                 # ECRASE DEUX FICHIERS DE FS, ET C EST MESURE le 2026-10-19.
                 # La base d ORIGINE de FS porte `AET_S_GAMDAN` = planche 242
                 # (fichier `aet_s_gamdan.bin`, rang 381, sprites 299), et le
                 # `.par` nomme encore `aet_s_gamdan.bin` (279 936 o,
                 # comprime) ET `spr_s_gamdan.farc` (178 810 o). Notre copie
                 # dans `rom/2d` fait 743 472 o -- la taille exacte de celle
                 # de 2007. Les deux ne peuvent pas etre servies : le `.par`
                 # passe AVANT le disque (c est la raison meme de
                 # `par_masquer`), et il n est masque QUE pour `aet_db.bin` et
                 # `spr_db.bin`. Donc soit nos pictos de grade ne viennent pas
                 # de la ou le dossier le dit, soit le `.par` ne gagne pas
                 # ici. NON TRANCHE -- il faut le voir a l ecran ou le sonder.
                 # TRANCHE LE 2026-10-19, ET C EST LE .par QUI GAGNE (§21.3
                 # puis §22). La chaine de mesure :
                 #   1. le moteur consulte le `.par` AVANT le disque -- mesure
                 #      au point d arret sur CreateFileW
                 #      (`analysis/import_decors.md`, cf. `par_masquer.py`) ;
                 #   2. TOUS les fichiers qu une seance passee a voulu
                 #      remplacer sur le disque ont leur nom MASQUE dans le
                 #      `.par` : `aet_n_adv.bi_`, `spr_n_adv.far_`,
                 #      `spr_n_cmnps3.far_`, `aet_db.bi_`, `spr_db.bi_` ;
                 #   3. `aet_s_gamdan.bin` et `spr_s_gamdan.farc`, eux, NE
                 #      SONT PAS masques ;
                 #   4. la planche de FS, extraite du `.par` (279 936 o), a
                 #      218 noms de calque et **AUCUN en commun** avec celle
                 #      de 2007 (236 noms) : elle nomme `end_kyu01`,
                 #      `end_dan01`, et n a aucun `shogo`.
                 # Donc la planche 242 de FS n etait PAS ecrasee -- mais
                 # `quest_grade_calque()` demande `s_gamdan_kyu09`... PAR NOM
                 # dans la scene 688, et ces noms n existent pas dans la
                 # planche servie. LE PICTO DE GRADE NE POUVAIT PAS S AFFICHER.
                 # LA CORRECTION EST SUSPENDUE (§23). Lui donner un nom pose
                 # a part -- `aet_q_dan.bin` / `spr_q_dan.farc` -- a casse le
                 # lancement du mode Quest : l etape 1 de la greffe demande
                 # justement la planche 530 et le jeu de sprites 627, et le
                 # journal s arrete la. La raison probable est dans le §22
                 # lui-meme : sous l ancien nom, 627 resolvait
                 # `spr_s_gamdan.bin`, donc le `.par` servait le jeu de
                 # sprites de FS (178 810 o) ; sous le nom neuf, le disque sert
                 # celui de 2007 (1 042 268 o), que FS n avait JAMAIS charge.
                 # On revient donc au nom d origine -- le picto de grade reste
                 # invisible, mais le mode se lance -- et `ecrase_fs` dit que
                 # l ecrasement du fichier est connu et sans effet (le `.par`
                 # gagne, §22.1).
                 #
                 # L ESSAI DU 2026-10-19 A TRANCHE, ET CE N ETAIT PAS LA
                 # TEXTURE : renommer le jeu de sprites seul cassait aussi le
                 # lancement, et la cause est que le MEMBRE de l archive
                 # gardait son nom source (voir `ajouter()`). Corrige la, le
                 # renommage complet redevient possible -- et c est lui qui
                 # rend le picto de grade affichable, sans ecraser la planche
                 # de FS.
                 aet_pose='aet_q_dan.bin', spr_pose='spr_q_dan.farc'),
    # LES DEUX PLANCHES QUI MANQUAIENT A FS (2026-10-19, §20.1). Le releve de
    # `tools/ancres_ecrans.py --2007` a trouve :
    #   . les QUATRE fenetres d'`Announce` (`p_que_info_win_01_ct`,
    #     `_36_02_ct`, `_03_ct`, `_30_04_ct`) dans `aet_n_cmn.bin` de 2007,
    #     introuvables dans les quinze planches de FS (§17.17, §19.1) ;
    #   . la BOUTIQUE entiere dans `aet_n_cstm.bin` -- composition c5 :
    #     `p_item_win_tit_ct`, `p_iteme_win_30_01_ct`,
    #     `p_iteminfo_win_248x394_lt`, `p_item_grid_01..05_lt` et les quatre
    #     `p_itemshop_arrow_*_c`. La c4, sa soeur, est l'EDITEUR de tenue
    #     (`p_itempoint_win_248x72_lt`, fleches `itemedit`).
    #
    # LE NOM INTERNE RESTE CELUI DE 2007 (`N_CMN`, `N_CSTM`), pour la meme
    # raison que `qdan` : les videos de la planche appellent leurs sprites
    # `<nom>_<sprite>`. FS a deja un `AET_N_CMN` et un `SPR_N_CMN` au contenu
    # different ; seuls les IDENTIFIANTS doivent rester uniques, et ils le
    # sont.
    #
    # MAIS LE FICHIER POSE, LUI, CHANGE DE NOM -- voir `aet_pose`.
    'qcmn': dict(aet='aet_n_cmn.bin', spr='spr_n_cmn.farc',
                 aet_pose='aet_q_cmn.bin', spr_pose='spr_q_cmn.farc',
                 nom='N_CMN',
                 libelle='les quatre fenetres d Announce (media de 2007)'),
    # LE BADGE DE GRADE : RIEN A IMPORTER POUR LES VINGT PREMIERS GRADES.
    #
    # J avais declare ici une entree `qccmn` (le `aet_c_cmn` / `spr_c_cmn` de
    # 2007). Question de Frederic : « pourquoi ne pas utiliser le grade de
    # FS ? » -- et la mesure lui donne raison. Le `aet_c_cmn` de FS, extrait
    # du `.par`, porte DEJA les calques nommes, aux tailles exactes de 2007 :
    #
    #   c_cmn_dan_kyu_1_e.pic .. c_cmn_dan_kyu_10_e.pic   74..88 x 28..30
    #   c_cmn_dan_dan_1_e.pic .. c_cmn_dan_dan_10_e.pic   72..88 x 26
    #   c_cmn_dan_base1p.pic / base2p.pic                 102 x 30, la plaque
    #
    # (le suffixe `_E` est la version anglaise ; FS porte les deux langues.)
    # Sa planche est l identifiant 1, son jeu de sprites le 0, sa scene MAIN
    # la 5 -- tout est deja dans la base d origine, rien a declarer, rien a
    # charger en plus, aucune collision de nom.
    #
    # CE QUE FS N A PAS : les VINGT-DEUX TITRES (grades 20 a 41) --
    # `DAN_KAIDEN`, `DAN_MOSA`, `DAN_KENSEI`... Ils n existent que dans le
    # media de 2007, et FS les remplace par son propre systeme de rangs en
    # ligne (`DAN_BASE_BRZ/SLV/GLD/DIA/MAS/SEI/STN/WOD`). Si l on veut un
    # jour les vingt-deux titres, c est la -- et SEULEMENT la -- qu il
    # faudra importer `aet_c_cmn` de 2007.
    'qcstm': dict(aet='aet_n_cstm.bin', spr='spr_n_cstm.farc',
                  aet_pose='aet_q_cstm.bin', spr_pose='spr_q_cstm.farc',
                  nom='N_CSTM',
                  libelle='la boutique et l editeur de tenue (media de 2007)'),
    # LA PLAQUE RONDE DE LA FICHE -- ET LA RAISON QUI MANQUAIT (2026-10-20).
    #
    # Le commentaire ci-dessus disait : « si l on veut un jour les vingt-deux
    # titres, c est la -- et SEULEMENT la -- qu il faudra importer
    # `aet_c_cmn` de 2007 ». Il y a une seconde raison, et elle se mesure :
    #
    # `FUN_8230AC50` pose TROIS objets sur la fiche du joueur -- le portrait,
    # le badge, et **`gen_base`**, l anneau de six billes que Frederic voit a
    # gauche du cadre sur la capture de 2007. Or le `aet_c_cmn` de FS, celui
    # du `.par`, declare bien la composition racine `gen_base`... avec
    # **ZERO calque**. L objet se cree (identifiant non nul au journal) et
    # rien ne se dessine : c est une coquille vide.
    #
    # Le `aet_c_cmn` de 2007, lui, la porte en entier : six
    # `c_cmn_gen_ball.pic` de 12 x 12 en cercle, qui apparaissent une par
    # une (trames 60, 120, 180, 240, 300, 360) -- d ou les SEPT variantes
    # « 0 » a « 6 » que `FUN_82309C38` plafonne a 6.
    'qccmn': dict(aet='aet_c_cmn.bin', spr='spr_c_cmn.farc',
                  aet_pose='aet_qc_cmn.bin', spr_pose='spr_qc_cmn.farc',
                  nom='C_CMN',
                  libelle='la plaque gen_base, et les 22 titres (2007)'),
}


PAR = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'vf5fs_data.par')
BASES = ('aet_db.bin', 'spr_db.bin')


class Refus(Exception):
    pass


def par_masquer(action):
    """Le `.par` passe AVANT le disque : tant que `aet_db.bin` y est nomme,
    notre copie de `rom/2d/` n'est jamais ouverte (mesure a la sonde le
    2026-09-11 : le moteur lisait les planches sur le disque, mais pas les
    bases). On masque donc les deux noms, comme pour un decor."""
    r = subprocess.run([sys.executable, os.path.join(ICI, 'par_masquer.py'),
                        action] + list(BASES), capture_output=True, text=True)
    if r.returncode:
        raise Refus('par_masquer %s : %s' % (action, (r.stdout or '') +
                                             (r.stderr or '')))
    return r.stdout


def par_masquees():
    """Les bases dont le nom est masque dans l'index du `.par`."""
    import par_inventaire
    _, fichiers = par_inventaire.lire(PAR)
    noms = set(n for n, *_ in fichiers)
    return [b for b in BASES if b not in noms and b[:-1] + '_' in noms]


# ---------------------------------------------------------------------------
# lire et ecrire les deux bases
# ---------------------------------------------------------------------------
def _cs(d, o):
    return d[o:d.index(b'\0', o)].decode('latin-1')


def lire_base(d, pas_entree, pas_second):
    n1, o1, n2, o2 = struct.unpack_from('<4I', d, 0)
    prem = [list(struct.unpack_from('<%dI' % (pas_entree // 4), d,
                                    o1 + pas_entree * k)) for k in range(n1)]
    sec = [list(struct.unpack_from('<%dI' % (pas_second // 4), d,
                                   o2 + pas_second * k)) for k in range(n2)]
    for e in prem:
        e[1], e[2] = _cs(d, e[1]), _cs(d, e[2])
    for e in sec:
        e[1] = _cs(d, e[1])
    return prem, sec


def ecrire_base(prem, sec, pas_entree, pas_second):
    """Rend les octets : en-tete, les deux tables, puis le pot de chaines."""
    o1 = 0x10
    o2 = o1 + pas_entree * len(prem)
    pot = o2 + pas_second * len(sec)
    chaines, octets = {}, bytearray()

    def poser(t):
        if t not in chaines:
            chaines[t] = pot + len(octets)
            octets.extend(t.encode('latin-1') + b'\0')
        return chaines[t]

    b = bytearray(struct.pack('<4I', len(prem), o1, len(sec), o2))
    t1 = bytearray()
    for e in prem:
        v = list(e)
        v[1], v[2] = poser(e[1]), poser(e[2])
        t1 += struct.pack('<%dI' % (pas_entree // 4), *v)
    t2 = bytearray()
    for e in sec:
        v = list(e)
        v[1] = poser(e[1])
        t2 += struct.pack('<%dI' % (pas_second // 4), *v)
    return bytes(b + t1 + t2 + octets)


def bases_origine():
    """Les deux bases telles qu'elles sont DANS le binaire d'origine."""
    pe = pefile.PE(DLL, fast_load=True)
    tmp = os.path.join(RACINE, 'extracted', 'quest', 'bases')
    os.makedirs(tmp, exist_ok=True)
    chemin = os.path.join(tmp, 'embarque.farc')
    open(chemin, 'wb').write(pe.get_data(FARC_EMBARQUE, 0x120000))
    a = farc.Farc(chemin)
    out = {}
    for e in a.entries:
        if e['name'] in ('aet_db.bin', 'spr_db.bin'):
            out[e['name']] = a.read(e)
    if len(out) != 2:
        raise Refus('les bases ne sont pas dans l archive embarquee')
    return out


# ---------------------------------------------------------------------------
# un jeu de sprites : ses noms
# ---------------------------------------------------------------------------
def noms_sprites(chemin_farc):
    """{sprites: [noms], textures: [noms]} d'un `spr_*.farc`."""
    import txp
    m = txp.defarc(chemin_farc)
    d = list(m.values())[0]
    _, _, n_tex, n_spr, _, o_ntex, o_nspr, _ = struct.unpack_from('<8I', d, 0)
    spr = [_cs(d, struct.unpack_from('<I', d, o_nspr + 4 * k)[0])
           for k in range(n_spr)]
    tex = [_cs(d, struct.unpack_from('<I', d, o_ntex + 4 * k)[0])
           for k in range(n_tex)]
    return spr, tex


def videos_aet(d):
    """Les (decalage du champ identifiant, nom, identifiant) des sources de
    video d'une planche AET -- toutes scenes confondues."""
    out = []
    o = 0
    while True:
        p = struct.unpack_from('<I', d, o)[0]
        if p == 0 or p >= len(d):
            break
        nv, pv = struct.unpack_from('<II', d, p + 0x28)
        for k in range(nv):
            nsrc, psrc = struct.unpack_from('<II', d, pv + 0x14 * k + 0x0C)
            for j in range(nsrc):
                no, ident = struct.unpack_from('<II', d, psrc + 8 * j)
                out.append((psrc + 8 * j + 4, _cs(d, no) if no else '', ident))
        o += 4
    return out


# ---------------------------------------------------------------------------
def ajouter(codes, verbeux=True):
    src = bases_origine()
    aet_p, aet_s = lire_base(src['aet_db.bin'], 0x14, 0x0C)
    spr_p, spr_s = lire_base(src['spr_db.bin'], 0x10, 0x0C)
    id_aet = max(e[0] for e in aet_p) + 1
    id_scene = max(e[0] for e in aet_s) + 1
    id_spr = max(e[0] for e in spr_p) + 1
    id_sprite = max(e[0] for e in spr_s) + 1
    # REFUS : un nom POSE qui est deja le fichier d une planche de FS.
    # `rom/2d` porte TOUTES les planches de FS depuis `--bases-2d-libres` :
    # ecrire par-dessus en casserait une, sans un mot. C est le piege du
    # 2026-10-19 -- `aet_n_cmn.bin` existe des deux cotes.
    fichiers_fs = set(e[2] for e in aet_p) | set(e[2] for e in spr_p)
    for code in codes:
        p = PLANCHES[code]
        for pose in (p.get('aet_pose', p['aet']),
                     p.get('spr_pose', p['spr']).replace('.farc', '.bin')):
            if pose in fichiers_fs and not p.get('ecrase_fs'):
                raise Refus('%s : le nom pose %s est deja le fichier d une '
                            'planche de Final Showdown. Donnez-lui un '
                            '`aet_pose` / `spr_pose` a part, ou posez '
                            '`ecrase_fs=True` si c est voulu.' % (code, pose))
    os.makedirs(DEUXD, exist_ok=True)
    dits = []
    for code in codes:
        p = PLANCHES[code]
        f_spr = os.path.join(X360, p['spr'])
        f_aet = os.path.join(X360, p['aet'])
        for f in (f_spr, f_aet):
            if not os.path.exists(f):
                raise Refus('%s introuvable' % f)
        sprites, textures = noms_sprites(f_spr)
        # --- le jeu de sprites
        rang_spr = len(spr_p)
        pose_aet = p.get('aet_pose', p['aet'])
        pose_spr = p.get('spr_pose', p['spr'])
        spr_p.append([id_spr, 'SPR_' + p['nom'],
                      pose_spr.replace('.farc', '.bin'), rang_spr])
        # le nom d'un sprite DANS le jeu est court (`EFF_PTCL`) ; la base le
        # nomme `SPR_<planche>_<sprite>`, et la video de la planche AET
        # l'appelle `<planche>_<sprite>` -- c'est ce qui les relie
        ids = {}
        for k, nom in enumerate(sprites):
            complet = '%s_%s' % (p['nom'], nom)
            ids[complet] = id_sprite
            spr_s.append([id_sprite, 'SPR_' + complet, (rang_spr << 16) | k])
            id_sprite += 1
        for k, nom in enumerate(textures):
            spr_s.append([id_sprite, 'SPRTEX_%s_%s' % (p['nom'], nom),
                          (1 << 28) | (rang_spr << 16) | k])
            id_sprite += 1
        # --- la planche AET : ses scenes, et ses identifiants renumerotes
        d = bytearray(open(f_aet, 'rb').read())
        rang_aet = len(aet_p)
        aet_p.append([id_aet, 'AET_' + p['nom'], pose_aet, rang_aet, id_spr])
        import aet as mod_aet
        a = mod_aet.Aet(f_aet)
        noms_scenes = []
        for k, s in enumerate(a.scenes()):
            # `scenes()` rend les pointeurs ; le nom est le premier champ
            nom = a.chaine(a.u32(s)) or 'MAIN'
            noms_scenes.append(nom)
            aet_s.append([id_scene, 'AET_%s_%s' % (p['nom'], nom),
                          (rang_aet << 16) | k])
            id_scene += 1
        inconnus, poses = 0, 0
        for decalage, nom, ancien in videos_aet(d):
            if nom in ids:
                struct.pack_into('<I', d, decalage, ids[nom])
                poses += 1
            else:
                inconnus += 1
        # A COTE, PUIS ON REMPLACE : la regle du depot.
        import shutil
        dest = os.path.join(DEUXD, pose_aet)
        with open(dest + '.neuf', 'wb') as fh:
            fh.write(bytes(d))
        os.replace(dest + '.neuf', dest)
        # L ARCHIVE DE SPRITES : SON MEMBRE DOIT PORTER LE NOM QUE LA BASE
        # NOMME. Mesure du 2026-10-19 : le moteur ouvre `<pose>.farc` puis y
        # cherche le membre `<pose>.bin`. Copier l archive telle quelle laisse
        # le membre sous son nom SOURCE, et le jeu de sprites ne devient
        # jamais pret -- c est ce qui a casse le lancement du mode Quest quand
        # `qdan` a recu un nom pose a part. `farc.comme()` preserve la
        # variante et l alignement du modele.
        dest = os.path.join(DEUXD, pose_spr)
        if pose_spr == p['spr']:
            shutil.copyfile(f_spr, dest + '.neuf')
        else:
            import farc as mod_farc
            voulu = pose_spr.replace('.farc', '.bin')
            a = mod_farc.Farc(f_spr)
            if len(a.entries) != 1:
                raise Refus('%s : %s porte %d membres (%s) -- on ne sait pas '
                            'lequel renommer en %s'
                            % (code, p['spr'], len(a.entries),
                               [e['name'] for e in a.entries], voulu))
            mod_farc.comme(f_spr, dest + '.neuf',
                           {voulu: a.read(a.entries[0])})
        os.replace(dest + '.neuf', dest)
        dits.append('%s : planche AET %d (%s, fichier %s), %d scene(s) %s ; '
                    'jeu de sprites %d, %d sprites + %d textures ; '
                    '%d identifiant(s) renumerotes%s'
                    % (code, id_aet, 'AET_' + p['nom'], pose_aet,
                       len(noms_scenes),
                       ' '.join(noms_scenes), id_spr, len(sprites),
                       len(textures), poses,
                       '' if not inconnus else
                       ', %d SANS sprite du meme nom' % inconnus))
        id_aet += 1
        id_spr += 1
    open(os.path.join(DEUXD, 'aet_db.bin'), 'wb').write(
        ecrire_base(aet_p, aet_s, 0x14, 0x0C))
    open(os.path.join(DEUXD, 'spr_db.bin'), 'wb').write(
        ecrire_base(spr_p, spr_s, 0x10, 0x0C))
    manquantes = [b for b in BASES if b not in par_masquees()]
    if manquantes:
        par_masquer('--masquer')
        dits.append('%s masquee(s) dans l index du .par : sans cela le moteur '
                    'lit la copie de l archive et ignore la notre'
                    % ' et '.join(manquantes))
    if verbeux:
        for t in dits:
            print('  ' + t)
        print('bases posees : %s' % DEUXD)
    return dits


def controle():
    """Relit les bases POSEES : elles contiennent tout l original, plus nos
    planches, et chaque video de nos planches vise un sprite de la base."""
    fautes = []
    absentes = [b for b in BASES if b not in par_masquees()]
    if absentes:
        fautes.append('%s non masquee(s) dans le .par' % ' '.join(absentes))
    src = bases_origine()
    o_aet_p, o_aet_s = lire_base(src['aet_db.bin'], 0x14, 0x0C)
    o_spr_p, o_spr_s = lire_base(src['spr_db.bin'], 0x10, 0x0C)
    for nom in ('aet_db.bin', 'spr_db.bin'):
        if not os.path.exists(os.path.join(DEUXD, nom)):
            return ['%s n est pas pose' % nom]
    aet_p, aet_s = lire_base(open(os.path.join(DEUXD, 'aet_db.bin'),
                                  'rb').read(), 0x14, 0x0C)
    spr_p, spr_s = lire_base(open(os.path.join(DEUXD, 'spr_db.bin'),
                                  'rb').read(), 0x10, 0x0C)
    for avant, apres, quoi in ((o_aet_p, aet_p, 'planches AET'),
                               (o_aet_s, aet_s, 'scenes'),
                               (o_spr_p, spr_p, 'planches de sprites'),
                               (o_spr_s, spr_s, 'sprites')):
        if apres[:len(avant)] != avant:
            fautes.append('%s : l original n est pas conserve' % quoi)
    par_id = {e[0]: e for e in spr_s}
    for e in aet_p[len(o_aet_p):]:
        f = os.path.join(DEUXD, e[2])
        if not os.path.exists(f):
            fautes.append('%s absent de rom/2d' % e[2])
            continue
        d = open(f, 'rb').read()
        manquants = [n for _, n, i in videos_aet(d) if i not in par_id]
        if manquants:
            fautes.append('%s : %d video(s) sans sprite (%s)'
                          % (e[1], len(manquants), manquants[:3]))
        jeu = [s for s in spr_p if s[0] == e[4]]
        if not jeu:
            fautes.append('%s : le jeu de sprites %d n existe pas'
                          % (e[1], e[4]))
        elif not os.path.exists(os.path.join(DEUXD,
                                             jeu[0][2].replace('.bin',
                                                               '.farc'))):
            fautes.append('%s absent de rom/2d' % jeu[0][2])
    return fautes


def main():
    a = sys.argv[1:]
    try:
        if '--lister' in a:
            src = bases_origine()
            aet_p, aet_s = lire_base(src['aet_db.bin'], 0x14, 0x0C)
            spr_p, spr_s = lire_base(src['spr_db.bin'], 0x10, 0x0C)
            print('aet_db : %d planches, %d scenes (id max %d / %d)'
                  % (len(aet_p), len(aet_s), max(e[0] for e in aet_p),
                     max(e[0] for e in aet_s)))
            print('spr_db : %d planches, %d sprites (id max %d / 0x%X)'
                  % (len(spr_p), len(spr_s), max(e[0] for e in spr_p),
                     max(e[0] for e in spr_s)))
            for e in aet_p[:3] + aet_p[-2:]:
                print('   AET %4d %-20s %-24s spr %d' % (e[0], e[1], e[2],
                                                         e[4]))
            return 0
        if '--controle' in a:
            f = controle()
            for x in f:
                print('FAUTE : %s' % x)
            print('bases 2D : %s' % ('CONFORMES' if not f else
                                     '%d faute(s)' % len(f)))
            return 1 if f else 0
        if '--ajouter' in a:
            codes = [x for x in a[a.index('--ajouter') + 1:]
                     if not x.startswith('--')]
            for c in codes:
                if c not in PLANCHES:
                    print('planche inconnue : %s (connues : %s)'
                          % (c, ' '.join(sorted(PLANCHES))))
                    return 1
            ajouter(codes)
            f = controle()
            for x in f:
                print('FAUTE : %s' % x)
            return 1 if f else 0
        print(__doc__)
        return 1
    except Refus as e:
        print('REFUS : %s' % e)
        return 1


if __name__ == '__main__':
    sys.exit(main())
