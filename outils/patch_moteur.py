#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE PATCHEUR DU MOTEUR -- reconstruit apres la perte du source (2026-10-12).

CE QUI S EST PASSE. Le source de ce fichier -- 14 997 lignes -- a ete VIDE par
erreur le 2026-10-12 : une ouverture en ecriture avec un `newline` invalide.
Python TRONQUE le fichier avant de valider ce parametre, et leve ensuite.

CE QUI A ETE SAUVE, et c est beaucoup :

  . `tools/socle_20261008.pyc` -- le BYTECODE du 2026-10-08, intact, et il
    se charge. Il porte tout le travail jusqu a cette date, au bit pres :
    les tables d octets, les adresses, les generateurs de zone. On s en sert
    tel quel, comme d une bibliotheque.
  . `sauvegarde_urgence/patch_moteur_20261004.py` -- 8 716 lignes AVEC leurs
    commentaires, pour la reconstruction du source propre.
  . `sauvegarde_urgence/constantes_recuperees.py` -- 229 constantes extraites
    du bytecode, exactes.
  . `sauvegarde_urgence/*.PATCHEE_20261012.dll` -- la DLL complete, celle qui
    porte tout le travail jusqu au 12.
  . et surtout `REPRISE.md` et `analysis/` : le RAISONNEMENT, intact. C est
    pour cela qu on y ecrit tout.

CE QUE FAIT CE FICHIER, EN ATTENDANT LA RECONSTRUCTION COMPLETE. Il est un
PILOTE : il charge le socle du 8 octobre pour tout ce qui vient d avant, et
porte EN SOURCE CLAIR les chantiers des 9 au 12 octobre, que le socle ne
connait pas :

    --options-dural     journal (180)
    --options-v2        journal (182) a (184)
    --menu-griser       journal (185)
    --versus-joueur2    journal (186) et (187)
    --quest-degriser    journal (236)

LE CONTROLE EST BINAIRE, pas une opinion : repatcher le `.origine` et
comparer octet pour octet avec `sauvegarde_urgence/...PATCHEE_20261012.dll`.
Identiques = la reconstruction est exacte.

LA REGLE QUI MANQUAIT, et qui vaut pour tous les outils de ce depot :
**on n ecrit jamais un fichier du depot directement**. On ecrit a cote, puis
on remplace. Et `newline` ne prend que '', '\\n', '\\r' ou '\\r\\n'.
"""
import importlib.util
import os
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
SOCLE = os.path.join(ICI, 'socle_20261008.pyc')

if not os.path.exists(SOCLE):
    sys.exit('REFUS : %s manque. C est le socle du 2026-10-08, sans lui ce '
             'pilote ne peut rien faire.' % SOCLE)

_spec = importlib.util.spec_from_file_location('_socle08', SOCLE)
_s = importlib.util.module_from_spec(_spec)
sys.modules['_socle08'] = _s
_spec.loader.exec_module(_s)

# Le vocabulaire du socle, accessible ici sans prefixe : les lanceurs et les
# autres outils citent ces noms.
for _n, _v in vars(_s).items():
    if not _n.startswith('__') and _n not in ('main',):
        globals().setdefault(_n, _v)

sys.path.insert(0, ICI)
import options_v2 as ov2                                      # noqa: E402


# ---------------------------------------------------------------------------
# LA PLACE DES CHANTIERS DU 9 AU 12 DANS LA GREFFE
#
# Le socle pose la section `.greffe` a la taille qu il connait (0x4D40). On la
# fait grandir AVANT de l appeler -- `GREFFE_TAILLE` est une globale de son
# module, et `verifier_disposition` comme `ajouter_greffe` la relisent -- puis
# on loge nos zones dans l espace ajoute, a partir de l ancienne fin.
# ET LA BASE N EST PLUS UNE CONSTANTE -- correction du 2026-10-13, et le
# jeu ne se lancait plus du tout. `GREFFE_TAILLE` vaut 0x4D40 au
# CHARGEMENT du socle, mais ce n est que sa valeur PAR DEFAUT : le socle
# dimensionne SA greffe selon les options qu on lui donne, et avec le lot
# complet des decors (--variantes-5r --variantes-vf5 --decors-5r
# --decors-vf5) la section produite fait 0x7DC0. Poser nos zones a 0x4D40
# revenait alors a les ecrire EN PLEIN MILIEU DE SES TABLES.
#
# CE QUE CA DONNAIT A L ECRAN : rien. Le jeu mourait au demarrage, et le
# debogueur a nomme le site -- `call 0x180EA7EB0` depuis 0x180176829 (le
# dessin du nom de variante, pose par --variantes-texte) tombait sur une
# zone de ZEROS, executee jusqu a l acces interdit. Mesure, pas devinee.
#
# ON MESURE DONC. Le socle tourne une premiere fois avec SA taille par
# defaut ; on relit la taille de la section qu il a produite -- c est son
# besoin REEL pour ces options-la ; on la lui redonne augmentee de nos
# zones, et il recommence depuis le `.origine`. Nos zones se posent alors
# APRES les siennes, quelles qu elles soient.
#
# ET ON VERIFIE AVANT D ECRIRE : notre bloc doit etre entierement a zero
# dans la DLL que le socle vient de rendre. Un seul octet non nul et on
# refuse -- c est exactement le controle qui manquait aujourd hui.
CPL_SOCLE_DEFAUT = _s.GREFFE_TAILLE              # 0x4D40 au 2026-10-08
_OFF_VS, CPL_VS_TAILLE = 0x000, 0x040
_OFF_DUR, CPL_DUR_TAILLE = 0x040, 0x300
_OFF_V2, CPL_V2_TAILLE = 0x340, 0xA00
_OFF_MAN, CPL_MAN_TAILLE = 0xD40, 0x080
# La zone TRM porte LE DRAPEAU du menu garde, les DEUX TABLES du
# sequenceur recopiees (18 dwords + 71 octets), ses trois relais d etat
# et les deux relais du mode MENU.
_OFF_TRM, CPL_TRM_TAILLE = 0xDC0, 0xB00
_OFF_FLM, CPL_FLM_TAILLE = 0x18C0, 0x300
# La zone NOM porte la boite aux lettres partagee avec apm.dll (magie
# « VF5NAME », 0x40 octets) puis ses trois relais, un par creneau de 0x40.
_OFF_NOM, CPL_NOM_TAILLE = 0x1BC0, 0x300
_OFF_TVF, CPL_TVF_TAILLE = 0x1EC0, 0x500
CPL_COMPLEMENT = 0x23C0                           # la longueur de NOTRE bloc
CPL_GREFFE_TOTALE = 0x10000                      # la place qu on impose
# Les adresses effectives, posees par `_placer_zones()` avant usage.
CPL_BASE = CPL_SOCLE_DEFAUT
CPL_VS = CPL_BASE + _OFF_VS
CPL_DUR = CPL_BASE + _OFF_DUR
CPL_V2 = CPL_BASE + _OFF_V2
CPL_MAN = CPL_BASE + _OFF_MAN
CPL_TRM = CPL_BASE + _OFF_TRM
CPL_FLM = CPL_BASE + _OFF_FLM
CPL_NOM = CPL_BASE + _OFF_NOM
CPL_TVF = CPL_BASE + _OFF_TVF
CPL_FIN = CPL_BASE + CPL_COMPLEMENT


def _placer_zones(base):
    """Pose nos zones a partir de `base`, le besoin reel du socle."""
    global CPL_BASE, CPL_VS, CPL_DUR, CPL_V2, CPL_MAN, CPL_TRM
    global CPL_FLM, CPL_NOM, CPL_TVF, CPL_FIN
    CPL_BASE = base
    CPL_VS = base + _OFF_VS
    CPL_DUR = base + _OFF_DUR
    CPL_V2 = base + _OFF_V2
    CPL_MAN = base + _OFF_MAN
    CPL_TRM = base + _OFF_TRM
    CPL_FLM = base + _OFF_FLM
    CPL_NOM = base + _OFF_NOM
    CPL_TVF = base + _OFF_TVF
    CPL_FIN = base + CPL_COMPLEMENT


def _taille_greffe(chemin):
    """La taille VIRTUELLE de la section `.greffe` de la DLL produite."""
    import pefile
    pe = pefile.PE(chemin, fast_load=True)
    for sec in pe.sections:
        if sec.Name.rstrip(b'\0') == b'.greffe':
            t = sec.Misc_VirtualSize
            pe.close()
            return t
    pe.close()
    return None

# Les options que le socle ignore et que ce pilote traite lui-meme.
NOUVELLES = ('--options-dural', '--options-v2', '--menu-griser',
             '--versus-joueur2', '--terminal-ordre', '--film-cadres',
             '--versus-manette', '--sans-ecran-epilepsie', '--nom-donnees',
             '--films-theatre', '--eau-refraction', '--quest-degriser')


def _greffe_posee(chemin):
    """Retrouve la section `.greffe` dans la DLL que le socle vient d ecrire.

    Le socle garde `GREFFE_POSEE` dans une variable LOCALE de son `main` : on
    ne peut pas la lui demander. On la relit donc dans le binaire, ce qui est
    de toute facon plus sur -- c est l etat reel, pas une intention.
    """
    import pefile
    pe = pefile.PE(chemin, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    for s in pe.sections:
        if s.Name.rstrip(b'\0') == b'.greffe':
            va, off = base + s.VirtualAddress, s.PointerToRawData
            pe.close()
            return va, off
    pe.close()
    return None


# ---------------------------------------------------------------------------
# `--menu-griser` -- LES ENTREES QUI NE MENENT NULLE PART (journal 185)
#
# L ETAT D UNE ENTREE EST UN OCTET, `page + 0x642 + i`, et ses trois valeurs
# sont MESUREES : 0 normal, 1 GRISE (le dessin multiplie l alpha par 0,5 en
# 0x1801E0F51), 2 pas dessine (0x1801E0F30).
#
# ET GRISER SUFFIT A RENDRE L ENTREE INERTE, c est le validateur qui le dit :
# 0x1801DDF54 envoie tout etat non nul dans une branche gardee par le bouchon
# 0x180007450.
#
# RIEN N EST GREFFE : l init porte DEJA les deux instructions qu il faut,
# mortes derriere un predicat bouchonne (c etait le grisage d origine) --
#     0x1801E3A01  je   0x1801E3A13        <- on l efface
#     0x1801E3A03  mov byte [rbx+0x646], 1 <- on change le DEPLACEMENT
#     0x1801E3A0A  mov word [rbx+0x643], 0x101
#
# ET LE CURSEUR LES SAUTE : la boucle de saut est deja dans 0x1801BBBE0 (quand
# le creneau [0x38] refuse une ligne, le moteur avance encore dans le meme
# sens). Le creneau du menu principal (0x1801E4CD0) ne refusait que l etat 2 ;
# deux octets lui font refuser tout etat non nul.
#
# L ordre est celui de --menu-v2 : 0 SINGLE PLAYER, 1 OFFLINE VERSUS,
# 2 ONLINE VERSUS, 3 QUEST MODE, 4 DOJO, 5 VF.TERMINAL, 6 SCOREBOARDS,
# 7 VF.TV, 8 HELP & OPTIONS, 9 EXIT.
MENU_GRISER = [
    (0x1801E3A01, bytes.fromhex('7410'), bytes.fromhex('9090')),
    (0x1801E3A03, bytes.fromhex('c68346060000' '01'),
     bytes.fromhex('c68348060000' '01')),            # 6 SCOREBOARDS
    (0x1801E3A0A, bytes.fromhex('66c78343060000' '0101'),
     bytes.fromhex('66c78344060000' '0101')),        # 2 ONLINE, 3 QUEST
    (0x1801E4CD8, bytes.fromhex('80bc084206000002' '7507'),
     bytes.fromhex('80bc084206000000' '7407')),      # le curseur saute
]
# `--menu-v2` nopait l octet de l entree 6 pour la DESSINER ; avec
# --menu-griser c est 0x1801E3A03 qui lui pose son etat, APRES ce site.

# ---------------------------------------------------------------------------
# `--quest-degriser` -- QUEST MODE REDEVIENT NORMALE, ET C EST UN OCTET
#
# --menu-griser pose les etats en UNE instruction, un `mov word` dont
# l immediat porte DEUX octets consecutifs :
#
#   0x1801E3A0A  mov word [rbx+0x644], 0x0101    <- +0x644 = entree 2
#                                                  +0x645 = entree 3
#
# Un `mov word` ecrit son immediat en petit-boutien : l octet BAS va en
# +0x644 (ONLINE VERSUS), l octet HAUT en +0x645 (QUEST MODE). Mettre
# l immediat a 0x0001 laisse donc ONLINE VERSUS grise (1) et rend QUEST MODE
# normale (0) -- un seul octet du binaire change.
#
# ET CELA DEVRAIT SUFFIRE A LA RENDRE SELECTIONNABLE, les deux gardes etant
# satisfaites des que l etat vaut 0 :
#   . le validateur 0x1801DDF54 (`cmp byte [rcx+rdi+0x642], 0` / `je`) prend
#     la branche utile ;
#   . le creneau de curseur 0x1801E4CD8, tel que --menu-griser le laisse
#     (`cmp ...,0` / `je`), ne refuse plus la ligne.
# A VERIFIER A L ECRAN, pas a deduire.
#
# CETTE TABLE REMPLACE LA TROISIEME LIGNE DE MENU_GRISER : les deux options
# ecrivent le meme site, et c est `_menu_griser(argv)` qui tranche.
QUEST_DEGRISER = (0x1801E3A0A, bytes.fromhex('66c78343060000' '0101'),
                  bytes.fromhex('66c78344060000' '0100'))


def _menu_griser(argv):
    """La table de --menu-griser, avec ou sans le degrisage de QUEST MODE."""
    if '--quest-degriser' not in argv:
        return MENU_GRISER
    site = QUEST_DEGRISER[0]
    return [QUEST_DEGRISER if p[0] == site else p for p in MENU_GRISER]


# ---------------------------------------------------------------------------
# POURQUOI IL N Y A PAS D OPTION POUR RELIER LA LIGNE QUEST MODE
#
# MESURE DU 2026-10-19, dans la DLL que `tools/quest.cmd` produit :
#
#   0x1801DE0B1  cmp ecx, 3
#   0x1801DE0B4  jne 0x1801DE0C5
#   0x1801DE0B6  mov rbx, [rsp+0x30]
#   0x1801DE0BB  add rsp, 0x20
#   0x1801DE0BF  pop rdi
#   0x1801DE0C0  jmp 0x180EA2FA0        <- la greffe de --quest-ecran
#
# `--quest-ecran` (du socle) REMPLACE DEJA la queue d appel de la branche
# morte de la ligne 3 -- cinq octets pour cinq, l epilogue a tourne, rien a
# ranger au retour. La ligne QUEST MODE ouvre donc le mode Quest sans rien
# ajouter, et son etat vaut 0 d office : le balayage de TOUTES les ecritures
# immediates dans le tableau d etats du `.origine` (page + 0x642 + i) rend
# +0x643, +0x644, +0x646, +0x648, +0x64A et +0x64B -- JAMAIS +0x645, qui est
# l entree 3.
#
# DEUX OPTIONS DE CE PILOTE ONT ETE RETIREES pour cela : `--quest-dojo`
# (elle faisait sauter la ligne 3 dans le corps de la ligne 4, donc vers le
# DOJO -- qui est deja la ligne 4 du menu) et `--quest-ligne3` (elle sautait
# dans la branche SCOREBOARDS, qui garde son `call 0x1801B0120`, la page des
# classements). Les deux ecrivaient 0x1801DE0B6..0x1801DE0C4 et EFFACAIENT
# donc la queue d appel de --quest-ecran. `_poser_points` ne pouvait pas le
# voir : il verifie les octets du `.origine`, pas ceux de la DLL en cours.
#
# LA LECON D OUTILLAGE : un controle contre le `.origine` ne protege que du
# mauvais site, pas du site DEJA PRIS par une autre option.

# ---------------------------------------------------------------------------
# `--versus-joueur2` -- LE JOUEUR 2 ENTRE SANS CREDIT (journal 186 et 187)
#
# PREMIER MAILLON, le menu VERSUS. Sa garde est l etat du joueur 2
# ([0x180751280 + 1*0x100]), et le menu appelle DEJA « fais entrer le joueur
# 2 » (0x1801A1E60) a chaque trame -- mais cette fonction commence par le
# bouchon 0x180007440 (`xor eax,eax`), qui rend sa branche utile
# inatteignable. On rend LA VALEUR, pas le predicat : le bouchon a 123
# appelants, on n y touche pas.
VERSUS_JOUEUR2 = [
    (0x1801A1E66, bytes.fromhex('e8d555e6ff'),
     bytes.fromhex('b8ffffffff')),                   # mov eax, -1
]
# SECOND MAILLON, le selecteur. `0x1800DB354` admet chaque joueur par deux
# tests avant de l inscrire (0x18016CF00) ; le second (0x1800B6D80) est sa
# GARDE DE CREDIT. Essayee a `mov al,1` : le curseur 2P apparait et se
# deplace. On ne la force pas sans condition -- ce bloc sert aussi SINGLE
# PLAYER -- d ou le relais ci-dessous.
VS2_SITE = (0x1800DB402, bytes.fromhex('e879b9fdff'))
VS2_ETAT = 0x1801A2330        # ecx = joueur -> eax = son etat
VS2_GARDE = 0x1800B6D80       # la garde d origine (ecx = joueur)


def vs2_relais(va):
    """ecx = le joueur. Rend al = 1 s il est deja en jeu, sinon la garde.

    L alignement est tenu : a l entree `rsp % 16 == 8`, le `push` le met a 0
    et le `sub 0x20` l y laisse. Le repli est une QUEUE D APPEL -- `rsp` y est
    revenu a son etat d entree et `ecx` n a pas bouge.
    """
    def rel(fin, cible):
        return struct.pack('<i', cible - (va + fin))

    c = bytearray()
    c += bytes.fromhex('51')                        # push rcx
    c += bytes.fromhex('4883ec20')                  # sub rsp, 0x20
    c += bytes.fromhex('e8') + rel(len(c) + 5, VS2_ETAT)
    c += bytes.fromhex('4883c420')                  # add rsp, 0x20
    c += bytes.fromhex('59')                        # pop rcx
    c += bytes.fromhex('85c0')                      # test eax, eax
    c += bytes.fromhex('7803')                      # js .garde
    c += bytes.fromhex('b001')                      # mov al, 1
    c += bytes.fromhex('c3')                        # ret
    assert len(c) == 0x16, len(c)                   # .garde tombe ici
    c += bytes.fromhex('e9') + rel(len(c) + 5, VS2_GARDE)
    if len(c) > CPL_VS_TAILLE:
        raise AssertionError('relais VS2 : %d octets' % len(c))
    return bytes(c)


# ---------------------------------------------------------------------------
# `--options-dural` -- DURAL SELECTIONNABLE OU NON, SELON LE MODE (journal 180)
#
# La case de Dural n est pas absente de la grille : elle est DESACTIVEE par un
# predicat bouchonne. `--dural-grille` y mettait `mov al,1`, inconditionnel.
# Un `call` fait cinq octets et `mov al,1 ; nop ; nop ; nop` aussi : les MEMES
# cinq octets portent desormais un `call` vers notre predicat.
#
# LES TROIS SITES Y PASSENT, pas seulement celui de la desactivation -- sans
# les deux du DESSIN, la case serait dessinee sans etre atteignable, et c est
# exactement le defaut constate a l ecran le 2026-09-04 :
#
#     0x18016DC69  les compositions `_dur` du dessin
#     0x18016E109  idem
#     0x18016E20B  la desactivation de la case
#
# D OU VIENT LE COMBAT : surtout pas du mode de jeu (0x180751010), qu Arcade
# ne pose JAMAIS sur notre chemin -- `analysis/mode_de_jeu.md` le dit, et le
# releve du 2026-09-05 montre le bloc a mode=9. On lit l ENTREE DE MENU
# VALIDEE, au repartiteur du menu principal : UN site, huit octets, et les
# trois premieres entrees portent le meme numero avant et apres --menu-v2
# (0 SINGLE PLAYER, 1 OFFLINE VERSUS, 2 ONLINE VERSUS).
DUR_SITES = (0x18016DC69, 0x18016E109, 0x18016E20B)
DUR_BOUCHON = 0x180007450
DUR_MOUCHARD = (0x1801DDF4C, bytes.fromhex('48634f58' 'c6476000'))
DUR_VAL, DUR_CONF, DUR_ORIG, DUR_FACE = 0x008, 0x014, 0x020, 0x024
DUR_TXT, DUR_TXT_PAS, DUR_CODE = 0x040, 0x10, 0x0C0
DUR_TEXTES = {0: 'Dural', 4: 'No', 5: 'Yes'}


def dural_zone(va, valeurs=(1, 1, 1)):
    """La zone de Dural : ses donnees, son predicat, son mouchard.

    VERSION RECONSTRUITE (2026-10-12), reduite a ce dont `--options-v2` a
    besoin : les trois bascules, leurs textes, et les deux relais. Les six
    relais de PAGE que portait l original vivaient dans `optres_zone`, et la
    refonte des menus les remplace tous -- elle tient la page de Dural comme
    sa cinquieme FACE.
    """
    def rip(fin, cible):
        return struct.pack('<i', cible - (va + fin))

    z = bytearray(DUR_CODE)
    for i, v in enumerate(valeurs):
        struct.pack_into('<I', z, DUR_VAL + 4 * i, 1 if v else 0)
        struct.pack_into('<I', z, DUR_CONF + 4 * i, 1 if v else 0)
    for i, t in DUR_TEXTES.items():
        b = t.encode('ascii') + b'\x00'
        if len(b) > DUR_TXT_PAS:
            raise AssertionError('texte trop long : %r' % t)
        z[DUR_TXT + DUR_TXT_PAS * i:DUR_TXT + DUR_TXT_PAS * i + len(b)] = b

    # --- P : LE PREDICAT de la case de Dural ------------------------------
    # Rend al = 1 si Dural est autorisee dans le mode d ou vient ce combat.
    # Il remplace `call 0x180007450` (`xor al,al ; ret`) a trois sites : on ne
    # touche donc QUE al, et on rend rcx intact.
    p = len(z)
    c = bytearray()
    c += bytes.fromhex('51')                            # push rcx
    c += bytes.fromhex('8b0d') + rip(p + len(c) + 6, va + DUR_ORIG)
    c += bytes.fromhex('83f902')                        # cmp ecx, 2
    c += bytes.fromhex('7602')                          # jbe .ok
    c += bytes.fromhex('31c9')                          # xor ecx, ecx
    c += bytes.fromhex('488d05') + rip(p + len(c) + 7, va + DUR_VAL)
    c += bytes.fromhex('8b0488')                        # mov eax,[rax+rcx*4]
    c += bytes.fromhex('85c0')                          # test eax, eax
    c += bytes.fromhex('0f95c0')                        # setne al
    c += bytes.fromhex('59')                            # pop rcx
    c += bytes.fromhex('c3')                            # ret
    z += c

    # --- M : LE MOUCHARD du repartiteur du menu ---------------------------
    # Les deux instructions d origine, puis `ecx` -- l entree validee -- dans
    # la greffe. Le repartiteur passe ici pour TOUTE entree validee, OPTIONS
    # comprise ; ce n est pas genant, puisqu on ne peut pas lancer un combat
    # depuis OPTIONS : la prochaine entree validee reecrira la valeur.
    m = len(z)
    c = bytearray()
    c += DUR_MOUCHARD[1]
    c += bytes.fromhex('890d') + rip(m + len(c) + 6, va + DUR_ORIG)
    c += bytes.fromhex('e9') + rip(
        m + len(c) + 5, DUR_MOUCHARD[0] + len(DUR_MOUCHARD[1]))
    z += c

    if len(z) > CPL_DUR_TAILLE:
        raise AssertionError('zone DUR : %d octets' % len(z))
    return bytes(z), va + p, va + m


# ---------------------------------------------------------------------------
# `--terminal-ordre` -- VF.TERMINAL A SON PROPRE SOUS-MENU
#
# CE QUE FREDERIC A VU, et qui tranche : « terminal est toujours completement
# casse, il lance les videos de movie theater ». C est la preuve que l objet
# [page du menu + 0x2328] N EST PLUS un sous-menu TERMINAL dans cette build :
# `--menu-v2` en a fait LA PAGE DE VF.TV. Tout ce qu on y branche retombe sur
# VF.TV -- son dessin, ses planches, et son entree 0 qui lance une video.
#
# Frederic avait choisi DEDOUBLER L OBJET des le depart. J ai cru pouvoir
# l eviter ; trois essais pour revenir a son choix.
#
# L INSTANCE EST A NOUS, dans la greffe, et VF.TV N EST PLUS TOUCHE DU TOUT.
# Si Movie Theater reste casse apres ca, il l etait avant nous.
#
# COMMENT ON CONSTRUIT UNE INSTANCE : le constructeur de `TaskMenuTerminal`
# est INLINE dans celui de la page (0x1801DA550), il n y a rien a appeler.
# Mais la sequence est triviale, et elle se lit entiere en 0x1801DA7CB :
#
#     lea rbx, [rdi+0x2328]
#     mov rcx, rbx ; call 0x1801BB750        ; le constructeur de base
#     lea rax, -> 0x180532A28 ; mov [rbx], rax     ; sa vtable
#     ... une trentaine de champs mis a zero avec rsi = 0
#     add rbx, 0x300
#     mov rcx, rbx ; call 0x1801BB750        ; le REPLAY MENU embarque
#     lea rax, -> 0x1805329C8 ; mov [rbx], rax     ; sa vtable
#     ... les memes champs a zero
#
# Aucun saut, aucun appel autre que le constructeur de base. On la refait
# telle quelle, UNE SEULE FOIS (drapeau dans la greffe) : notre zone est deja
# a zero, donc les mises a zero sont acquises, et les entrees suivantes ne
# refont que `0x1801E4A10` -- qui, lui, N ECRIT PAS LA VTABLE, d ou cette
# construction unique.
#
# LA TAILLE EST MESUREE, PAS SUPPOSEE : la page range ses sous-menus a
# 0x2328 puis 0x2928, donc l objet fait 0x600 octets, sous-objet compris
# (0x300 + 0x2EC = 0x5EC, et le champ le plus haut du parent est 0x5F2).
#
# LES QUATRE SITES, tous verifies la ou ils vivent :
#
#   A. 0x1801DE056  l entree 5 du menu principal -- DLL PATCHEE (le socle y a
#      mis `jmp <greffe>` + dix-sept `nop`). On y construit NOTRE instance et
#      on lui pose aussitot sa sous-page, le CARD SELECTOR.
#   B. 0x1801E1B10  le creneau 4 de `TaskMenuTerminal` (vtable 0x180532A28) --
#      DLL PATCHEE. Si `this` est NOTRE instance, on ne dessine rien : le
#      panneau porterait les planches de VF.TV (0x299, 0x29A, titre 0x17C).
#      SURTOUT PAS 0x1801E0C80, qui est le creneau 4 de `TaskMenuMain`, le
#      dessin du MENU PRINCIPAL -- verifie par le RTTI.
#   C. 0x1801DE369  l entree 0 du validateur -- DLL PATCHEE (le socle y saute
#      sur sa page generique des cette adresse ; 0x1801DE38D, que visaient mes
#      trois premieres versions, n y est plus qu un `nop` jamais atteint).
#      Pour NOTRE instance, elle rouvre le CARD SELECTOR ; pour celle de
#      VF.TV, elle repasse au socle, inchangee.
#   D. 0x1801DD898  dans la mise a jour, la ou le moteur referme la sous-page
#      annulee (`mov qword [rbx+0x2F8], 0`) -- site INTACT, verifie sur le
#      `.origine`. Pour NOTRE instance on y ajoute `[rbx+0x2F0] = 1`, le
#      drapeau « ce sous-menu est fini » que 0x1801DE422 pose lui-meme sur
#      l annulation : on revient donc au menu principal au lieu de rester sur
#      un sous-menu invisible.
#
# CE QUI SUIT EXISTAIT DEJA, et c est la sequence de la console : la mise a
# jour (0x1801DD8A8) inscrit « CUSTOMIZE MENU » des que la sous-page rend 2
# (0x1801C5C80), et le validateur de ce menu (0x1801C5119) demande lui-meme le
# mode 5 et le sous-etat 0x25 -- le chargement, puis le decor. Sur Xbox 360
# c est la ligne 3 du meme validateur (0x822B407C : `bl 0x821FF618` puis
# `stw r3, 0x23c(r31)`, 0x23C etant le 0x2F8 de la borne).
TRM_SITE = 0x1801DE056         # DLL PATCHEE : jmp <greffe> + 17 nop
TRM_SITE_LONG = 0x16
TRM_FERMER = (0x1801DD898,     # site INTACT, verifie sur le .origine
              bytes.fromhex('48c783f802000000000000' 'e9f4000000'))
TRM_FERMER_SUITE = 0x1801DD99C

TRM_BASE_CTOR = 0x1801BB750    # le constructeur de base
TRM_VT = 0x180532A28           # la vtable d origine, qu on COPIE
TRM_VT_FILS = 0x1805329C8      # vtable du REPLAY MENU embarque, a +0x300
TRM_FILS = 0x300
TRM_CTOR = 0x1801E4A10         # « entrer dans ce menu » (n ecrit PAS la vtable)
TRM_NOM = 0x180532C10          # « TERMINAL MENU »
TRM_INSCRIRE = 0x1801DE06C     # mov rcx,rbx ; call 0x180245830 ; [rdi+0x650]
TRM_OUVRIR = 0x1801D0720       # inscrit « CARD SELECTOR » ; rend l objet
TRM_TICK = 0x1801BC010         # la trame du menu
TRM_SOUS_PAGE = 0x2F8
TRM_ETATS = 0x2F0              # 0x2F0, 0x2F1, 0x2F4 : les etats de la sous-page

# ET ON COUPE TOUT LIEN AVEC VF.TV : NOTRE PROPRE VTABLE (2026-10-13)
#
# Frederic : « Puisque les Vtables de VF.TV et de VF.TERMINAL sont
# differentes, retire de VF.TERMINAL tout lien avec VF.TV ». C est la
# bonne facon de le dire : tant que notre instance porte la vtable
# 0x180532A28, elle appelle les MEMES fonctions que la page de VF.TV, et
# chacune de ces fonctions est detournee par le socle. Trancher dans ces
# detours -- ce que faisaient les relais B et C -- c est garder le lien.
#
# ON COPIE DONC LA VTABLE dans la greffe, avec son pointeur RTTI (le qword
# qui precede), et on n y change que DEUX creneaux :
#
#     creneau  4  le dessin   -> `xor al,al ; ret` : notre sous-menu ne
#                                dessine rien, ses planches sont celles de
#                                VF.TV (0x299, 0x29A, titre 0x17C)
#     creneau 10  le validateur -> le notre : ligne 0 ouvre le selecteur
#                                de carte, toute autre action referme le
#                                sous-menu
#
# Les dix-sept autres creneaux gardent leur adresse d origine. 0x1801E1B10
# et 0x1801DE369 sont RENDUS AU SOCLE, intacts : VF.TV retrouve exactement
# le code qu il avait.
#
# La zone TRM : le relais d entree, notre validateur, notre dessin, notre
# vtable, le relais de fermeture, le drapeau, puis l instance.
_TRM_A, _TRM_VAL, _TRM_DESS = 0x000, 0x100, 0x180
_TRM_D, _TRM_VT = 0x190, 0x200
_TRM_DRAP, _TRM_SAUVE, _TRM_DEJA = 0x2A0, 0x2A8, 0x2B0
_TRM_CUST, _TRM_ROUV = 0x300, 0x360
_TRM_SEQ, _TRM_SORT, _TRM_OBJ = 0x3A0, 0x400, 0x500
TRM_VT_CRENEAUX = 19           # releves dans 0x180532A28, le 20e n en est plus
TRM_VT_DESSIN, TRM_VT_VALID = 4, 10
TRM_FIN_PAGE = 0x1801BBAE0     # ce que fait 0x1801DE405 a la fermeture
TRM_FERMER_FEN = 0x1801BBA20
TRM_FEN = (0x240, 0x298)
TRM_PRET = 0x60                # [objet+0x60] = 0 en fin de validateur


def _rip(va, fin, cible):
    return struct.pack('<i', cible - (va + fin))


def trm_relais(va, obj, drap, vt, dessin, valid):
    """Construit NOTRE instance une fois, puis lui pose le selecteur de carte.

    LA VTABLE SE COPIE A L EXECUTION, ET CE N EST PAS UN CHOIX. La section
    `.greffe` n a AUCUNE RELOCATION : toute adresse ABSOLUE qu on y ecrit
    garde la valeur du fichier, et le chargeur ne la corrige jamais. Or la DLL
    n est pas chargee a sa base preferee -- mesure le 2026-10-13 dans le
    minidump : base 0x7FFE471B0000. Une vtable copiee au moment du patch
    envoie donc le moteur sur 0x1801E4300, qui n est plus rien.

    LE MINIDUMP LE DISAIT MOT POUR MOT : ACCESS_VIOLATION code 0xC0000005,
    parametre 0 = 8 (EXECUTION), adresse 0x1801E4300 -- le creneau 1 de la
    vtable, a sa base preferee. C est la regle de la greffe, deja ecrite dans
    le dossier, et je l avais oubliee.

    On copie donc les vingt qwords -- le pointeur RTTI et les dix-neuf
    creneaux -- depuis la VRAIE vtable, atteinte en RIP-relatif, puis on
    remplace deux creneaux par des `lea` RIP-relatifs eux aussi. Plus une
    seule adresse absolue dans la greffe.
    """
    c = bytearray()
    c += bytes.fromhex('488d1d') + _rip(va, len(c) + 7, obj)   # lea rbx, obj
    c += bytes.fromhex('833d') + _rip(va, len(c) + 7, drap) + b'\x00'
    saut = len(c)
    c += bytes.fromhex('7500')                                 # jne .deja
    c += bytes.fromhex('c705') + _rip(va, len(c) + 10, drap)
    c += struct.pack('<I', 1)                                  # drapeau = 1
    # --- la vtable : vingt qwords, de la vraie vers la notre ---------------
    c += bytes.fromhex('4c8d05') + _rip(va, len(c) + 7, TRM_VT - 8)
    c += bytes.fromhex('4c8d0d') + _rip(va, len(c) + 7, vt)
    c += bytes.fromhex('31c0')                                 # xor eax, eax
    boucle = len(c)
    c += bytes.fromhex('4d8b14c0')                 # mov r10, [r8 + rax*8]
    c += bytes.fromhex('4d8914c1')                 # mov [r9 + rax*8], r10
    c += bytes.fromhex('ffc0')                     # inc eax
    c += bytes.fromhex('83f8') + bytes((TRM_VT_CRENEAUX + 1,))
    c += bytes.fromhex('72') + bytes(((boucle - (len(c) + 2)) & 0xFF,))
    c += bytes.fromhex('4c8d15') + _rip(va, len(c) + 7, dessin)
    c += bytes.fromhex('4d8951') + bytes((8 + 8 * TRM_VT_DESSIN,))
    c += bytes.fromhex('4c8d15') + _rip(va, len(c) + 7, valid)
    c += bytes.fromhex('4d8951') + bytes((8 + 8 * TRM_VT_VALID,))
    # --- l objet : constructeur de base, notre vtable, puis le fils --------
    c += bytes.fromhex('488bcb')                               # mov rcx, rbx
    c += bytes.fromhex('e8') + _rip(va, len(c) + 5, TRM_BASE_CTOR)
    c += bytes.fromhex('488d05') + _rip(va, len(c) + 7, vt + 8)
    c += bytes.fromhex('488903')                               # mov [rbx], rax
    c += bytes.fromhex('488d8b') + struct.pack('<I', TRM_FILS)
    c += bytes.fromhex('e8') + _rip(va, len(c) + 5, TRM_BASE_CTOR)
    c += bytes.fromhex('488d05') + _rip(va, len(c) + 7, TRM_VT_FILS)
    c += bytes.fromhex('488983') + struct.pack('<I', TRM_FILS)
    c[saut + 1] = len(c) - (saut + 2)                          # .deja
    assert 0 < c[saut + 1] < 128
    c += bytes.fromhex('488bcb')                               # mov rcx, rbx
    c += bytes.fromhex('e8') + _rip(va, len(c) + 5, TRM_CTOR)
    c += bytes.fromhex('48c783') + struct.pack('<I', TRM_ETATS)
    c += struct.pack('<I', 0)
    c += bytes.fromhex('33c9')                                 # xor ecx, ecx
    c += bytes.fromhex('e8') + _rip(va, len(c) + 5, TRM_OUVRIR)
    c += bytes.fromhex('4885c0')                               # test rax, rax
    c += bytes.fromhex('7407')                                 # je .sans
    c += bytes.fromhex('488983') + struct.pack('<I', TRM_SOUS_PAGE)
    c += bytes.fromhex('488d15') + _rip(va, len(c) + 7, TRM_NOM)
    c += bytes.fromhex('e9') + _rip(va, len(c) + 5, TRM_INSCRIRE)
    assert len(c) <= _TRM_VAL - _TRM_A, len(c)
    return bytes(c)


def trm_dessin(va):
    """Le creneau 4 de NOTRE vtable : ne rien dessiner."""
    return bytes.fromhex('32c0' 'c3')                   # xor al, al ; ret


def trm_validateur(va):
    """Le creneau 10 de NOTRE vtable. rcx = this, edx = l action.

    La pile : a l entree `rsp % 16 == 8`. Deux `push` la remettent a 8, et
    `sub rsp,0x28` la ramene a 0 en reservant les 0x20 d accueil -- c est ce
    qu il faut avant un appel.
    """
    c = bytearray()
    c += bytes.fromhex('53')                            # push rbx
    c += bytes.fromhex('56')                            # push rsi
    c += bytes.fromhex('4883ec28')                      # sub rsp, 0x28
    c += bytes.fromhex('488bd9')                        # mov rbx, rcx
    c += bytes.fromhex('8bf2')                          # mov esi, edx
    c += bytes.fromhex('4883bb') + struct.pack('<I', TRM_SOUS_PAGE) + b'\x00'
    je_fin = len(c)
    # SI UNE SOUS-PAGE EST DEJA OUVERTE, ON NE FAIT RIEN : c est elle qui a
    # la main, et c est la mise a jour (0x1801DD8A8) qui la suit. `jne`,
    # PAS `je` -- l inverse laissait la ligne 0 sans effet tant que le
    # selecteur n etait pas deja ouvert, et le rouvrait quand il l etait.
    c += bytes.fromhex('0f85') + bytes(4)            # jne .fin
    c += bytes.fromhex('837b58') + b'\x00'               # cmp dword [rbx+0x58], 0
    jne_fermer = len(c)
    c += bytes.fromhex('0f85') + b'\0\0\0\0'            # jne .fermer
    # ligne 0 : le selecteur de carte devient la sous-page
    c += bytes.fromhex('8bd6')                          # mov edx, esi
    c += bytes.fromhex('488bcb')                        # mov rcx, rbx
    c += bytes.fromhex('e8') + _rip(va, len(c) + 5, TRM_TICK)
    c += bytes.fromhex('33c9')                          # xor ecx, ecx
    c += bytes.fromhex('e8') + _rip(va, len(c) + 5, TRM_OUVRIR)
    c += bytes.fromhex('4885c0')                        # test rax, rax
    c += bytes.fromhex('7407')                          # je .fin (court)
    c += bytes.fromhex('488983') + struct.pack('<I', TRM_SOUS_PAGE)
    jmp_fin = len(c)
    c += bytes.fromhex('e9') + b'\0\0\0\0'
    # .fermer : exactement ce que fait 0x1801DE402 pour les autres lignes
    o_fermer = len(c)
    c += bytes.fromhex('488bcb')                        # mov rcx, rbx
    c += bytes.fromhex('e8') + _rip(va, len(c) + 5, TRM_FIN_PAGE)
    for d in TRM_FEN:
        c += bytes.fromhex('488d8b') + struct.pack('<I', d)
        c += bytes.fromhex('e8') + _rip(va, len(c) + 5, TRM_FERMER_FEN)
    c += bytes.fromhex('c683') + struct.pack('<I', TRM_ETATS) + b'\x01'
    o_fin = len(c)
    c += bytes.fromhex('c643') + bytes((TRM_PRET,)) + b'\x00'   # [rbx+0x60] = 0
    c += bytes.fromhex('4883c428')                      # add rsp, 0x28
    c += bytes.fromhex('5e')                            # pop rsi
    c += bytes.fromhex('5b')                            # pop rbx
    c += bytes.fromhex('c3')                            # ret
    struct.pack_into('<i', c, je_fin + 2, o_fin - (je_fin + 6))
    struct.pack_into('<i', c, jne_fermer + 2, o_fermer - (jne_fermer + 6))
    struct.pack_into('<i', c, jmp_fin + 1, o_fin - (jmp_fin + 5))
    assert len(c) <= _TRM_DESS - _TRM_VAL, len(c)
    return bytes(c)


# LE PANNEAU DU SELECTEUR REVENAIT APRES LE CHARGEMENT (2026-10-13 soir)
#
# CONSTAT DE FREDERIC, capture a l appui : le decor du TERMINAL se charge, et
# le « Character Select » se redessine PAR-DESSUS l ecran 3D.
#
# POURQUOI : c est NOUS qui avons inscrit la tache « CARD SELECTOR » depuis le
# menu (0x1801D0720). Le moteur ne la ferme que sur une ANNULATION, en
# 0x1801DD87B. Quand le `CUSTOMIZE MENU` prend sa place comme sous-page --
# 0x1801DD8CE : `call 0x1801C5C80 ; mov [rbx+0x2F8], rax` -- l ancienne
# sous-page est simplement OUBLIEE, pas fermee. Elle reste donc inscrite, et
# elle se dessine encore une fois le mode change.
#
# Sur la borne ce cas n existait pas : le selecteur y est ouvert par l etat 0
# du sequenceur du mode 5, qui le ferme lui-meme. C est notre raccourci qui
# cree la fuite, c est donc a nous de la fermer -- et POUR NOTRE INSTANCE
# SEULEMENT, par 0x1802450A0, la meme fonction que 0x1801DD87B emploie.
TRM_CUST_SITE = (0x1801DD8CE,
                 bytes.fromhex('e8ad83feff' '488983f8020000'))
TRM_CUST_SUITE = 0x1801DD8DA
TRM_CUST_MENU = 0x1801C5C80    # inscrire « CUSTOMIZE MENU » ; rend l objet
TRM_CUST_CLORE = 0x1802450A0   # fermer une tache


def trm_cust_relais(va, obj, sauve, deja):
    """Le CUSTOMIZE MENU prend la place du selecteur, et le selecteur FERME."""
    c = bytearray()
    c += bytes.fromhex('4c8d15') + _rip(va, len(c) + 7, obj)   # lea r10, obj
    c += bytes.fromhex('4c39d3')                               # cmp rbx, r10
    simple = len(c)
    c += bytes.fromhex('7500')                                 # jne .simple
    c += bytes.fromhex('4c8b9b') + struct.pack('<I', TRM_SOUS_PAGE)
    c += bytes.fromhex('4c891d') + _rip(va, len(c) + 7, sauve)
    # LA DONNEE EST CHOISIE : le sequenceur du mode 5 ne la redemandera pas.
    c += bytes.fromhex('c705') + _rip(va, len(c) + 10, deja)
    c += struct.pack('<I', 1)
    c += bytes.fromhex('e8') + _rip(va, len(c) + 5, TRM_CUST_MENU)
    c += bytes.fromhex('488983') + struct.pack('<I', TRM_SOUS_PAGE)
    c += bytes.fromhex('488b0d') + _rip(va, len(c) + 7, sauve)
    c += bytes.fromhex('4885c9')                               # test rcx, rcx
    c += bytes.fromhex('7405')                                 # je .retour
    c += bytes.fromhex('e8') + _rip(va, len(c) + 5, TRM_CUST_CLORE)
    c += bytes.fromhex('e9') + _rip(va, len(c) + 5, TRM_CUST_SUITE)
    c[simple + 1] = len(c) - (simple + 2)                      # .simple
    assert 0 < c[simple + 1] < 128
    c += bytes.fromhex('e8') + _rip(va, len(c) + 5, TRM_CUST_MENU)
    c += bytes.fromhex('488983') + struct.pack('<I', TRM_SOUS_PAGE)
    c += bytes.fromhex('e9') + _rip(va, len(c) + 5, TRM_CUST_SUITE)
    assert len(c) <= _TRM_ROUV - _TRM_CUST, len(c)
    return bytes(c)


# ET LE MOTEUR LE ROUVRAIT (2026-10-13, apres la correction precedente)
#
# CONSTAT DE FREDERIC : « le cadre a bien disparu sur le 1er sous menu, mais il
# y a toujours cet ecran en trop » -- le selecteur se redessine PAR-DESSUS le
# decor, APRES le chargement. La fermeture posee sur 0x1801DD8CE etait pourtant
# bonne : le selecteur EST ferme quand le CUSTOMIZE MENU prend sa place. Mais
# la mise a jour continue, et quatre instructions plus loin elle le ROUVRE :
#
#     0x1801DD8DA  rcx = [rbx+0x2F8] ; call 0x180244F90   ; encore vivante ?
#     0x1801DD8E1  test al,al ; jne 0x1801DD99C           ; oui -> rien
#     0x1801DD8EE  rcx = [rbx+0x2F8] ; call 0x1801C5C70   ; le CUSTOMIZE MENU ?
#     0x1801DD8F5  test al,al ; je 0x1801DD914
#     0x1801DD8FE  mov ecx, 1 ; call 0x1801D0720          ; ON LE ROUVRE
#     0x1801DD908  mov [rbx+0x2F8], rax
#
# C est le comportement de la borne, et il a un sens LA-BAS : le CUSTOMIZE MENU
# qui meurt sans avoir valide renvoie au choix de carte. Chez nous il meurt
# APRES avoir demande le mode 5 (0x1801C5119), et notre instance -- STATIQUE,
# dans la greffe -- survit au changement de mode et execute cette ligne dans le
# decor.
#
# POUR NOTRE INSTANCE, ON NE ROUVRE RIEN : on remet la sous-page a zero et on
# pose `[objet+0x2F0] = 1`, le drapeau « ce sous-menu est fini » que
# 0x1801DE422 pose lui-meme. La mise a jour s arrete alors des sa premiere
# ligne (0x1801DD82B teste ce champ) et plus rien de nous ne vit dans le decor.
# On ne ferme PAS la tache depuis sa propre mise a jour : deux drapeaux
# suffisent, et ils ne risquent rien.
TRM_ROUV_SITE = (0x1801DD8FE,
                 bytes.fromhex('b901000000' 'e8182effff' '488983f8020000'))
TRM_ROUV_SUITE = 0x1801DD99C
TRM_ROUV_UN = 1                # `mov ecx, 1` : la reouverture


def trm_rouvrir_relais(va, obj):
    """Notre instance ne rouvre pas le selecteur : elle se retire."""
    c = bytearray()
    c += bytes.fromhex('4c8d15') + _rip(va, len(c) + 7, obj)   # lea r10, obj
    c += bytes.fromhex('4c39d3')                               # cmp rbx, r10
    normal = len(c)
    c += bytes.fromhex('7500')                                 # jne .normal
    c += bytes.fromhex('48c783') + struct.pack('<I', TRM_SOUS_PAGE)
    c += struct.pack('<I', 0)                                  # [2F8] = 0
    c += bytes.fromhex('c683') + struct.pack('<I', TRM_ETATS) + b'\x01'
    c += bytes.fromhex('e9') + _rip(va, len(c) + 5, TRM_ROUV_SUITE)
    c[normal + 1] = len(c) - (normal + 2)                      # .normal
    assert 0 < c[normal + 1] < 128
    c += bytes.fromhex('b9') + struct.pack('<I', TRM_ROUV_UN)
    c += bytes.fromhex('e8') + _rip(va, len(c) + 5, TRM_OUVRIR)
    c += bytes.fromhex('488983') + struct.pack('<I', TRM_SOUS_PAGE)
    c += bytes.fromhex('e9') + _rip(va, len(c) + 5, TRM_ROUV_SUITE)
    assert len(c) <= _TRM_SEQ - _TRM_ROUV, len(c)
    return bytes(c)


# L ECRAN DE CHOIX REVENAIT APRES LE CHARGEMENT -- ET C ETAIT LE SEQUENCEUR
#
# CONSTAT DE FREDERIC : « il y a toujours cet ecran en trop », sur le decor,
# APRES le chargement -- et sa capture suivante le montre dans un AUTRE etat,
# parce qu il avait valide une fois. C est donc un ecran VIVANT, pas un
# panneau oublie : c est celui du SEQUENCEUR DU MODE 5.
#
# LA TABLE DE SAUTS LE DIT (0x1801C3D60, etat en [objet+0x7C], table d octets
# 0x1801C4268 et table de dwords 0x1801C422C, decodees) :
#
#     etat  0 -> 0x1801C3D9D   ... xor ecx,ecx ; call 0x1801D0720  <- OUVRE
#                              mov [rbx+0x7C], 0xA
#     etat 10 -> 0x1801C3EAC   tient l ecran ; a la validation :
#                 0x1801C3ECD  call 0x1801CFD60 ; [rbx+0x80] = eax  <- l index
#                              movzx eax,[rbx+0xC2] ; [rbx+0x84] = al
#                              call 0x1801D0170 ; sete al
#                              mov [rbx+0x7C], 0x14   <- etat 20
#                              and [rbx+0xC0],0xFB ; [rbx+0x85]=al ; or ...
#     etat 20 -> 0x1801C3F1D   mov ecx,[rcx+0x80] ; call 0x1801CD1B0
#
# C EST LE COMPORTEMENT DE LA BORNE, et il est juste LA-BAS : on y entre dans
# le mode 5 sans avoir rien choisi. Sur console -- et par notre chemin -- la
# donnee est DEJA choisie dans le menu, et le `CUSTOMIZE MENU` a meme deja
# appele 0x1801CD1B0 (0x1801C5119) avant de demander le mode.
#
# ON NE SAUTE PAS A L ETAT 20 : il lui faut `[rbx+0x80]`, `[rbx+0x84]`,
# `[rbx+0x85]` et `[rbx+0xC0]`, que l etat 10 pose. On saute donc a LA QUEUE
# DE L ETAT 10 (0x1801C3ECD), celle qui les pose -- et `0x1801CFD60` relit
# l index sur le SELECTEUR GLOBAL, qui porte deja notre choix. Rien n est
# invente : c est le code du jeu, pris une etape plus loin.
#
# LE DRAPEAU est pose par le relais du CUSTOMIZE MENU, c est-a-dire au moment
# EXACT ou la donnee a ete choisie par notre chemin, et il est efface a son
# premier usage.
TRM_SEQ_SITE = (0x1801C3D9D, bytes.fromhex('488b0d4c79a700'))
TRM_SEQ_SUITE = 0x1801C3DA4        # la 2e instruction de l etat 0
TRM_SEQ_GLOBAL = 0x180C3B6F0       # ce que la 1re instruction chargeait
TRM_SEQ_VALIDE = 0x1801C3ECD       # la queue de l etat 10


def trm_seq_relais(va, deja):
    """Si la donnee vient du menu, on saute l ecran de choix du sequenceur."""
    c = bytearray()
    c += bytes.fromhex('833d') + _rip(va, len(c) + 7, deja) + b'\x00'
    normal = len(c)
    c += bytes.fromhex('7400')                                 # je .normal
    # LE DRAPEAU PASSE A 2, IL NE S EFFACE PAS : la sortie du mode en a
    # besoin, elle aussi (voir `trm_sortie_relais`). Il ne retombe a zero
    # qu une fois le MENU redemande.
    c += bytes.fromhex('c705') + _rip(va, len(c) + 10, deja)
    c += struct.pack('<I', 2)                                  # drapeau = 2
    c += bytes.fromhex('e9') + _rip(va, len(c) + 5, TRM_SEQ_VALIDE)
    c[normal + 1] = len(c) - (normal + 2)                      # .normal
    assert 0 < c[normal + 1] < 128
    c += bytes.fromhex('488b0d') + _rip(va, len(c) + 7, TRM_SEQ_GLOBAL)
    c += bytes.fromhex('e9') + _rip(va, len(c) + 5, TRM_SEQ_SUITE)
    assert len(c) <= _TRM_SORT - _TRM_SEQ, len(c)
    return bytes(c)


# LA SORTIE RENVOIE LE SEQUENCEUR A SON ETAT 0 -- MESURE, PAS DEDUIT
#
# TROIS CORRECTIFS A TROIS ENDROITS N Y AVAIENT RIEN CHANGE. On a donc pose
# `tools/sonde_mode.cmd` : deux points d arret, sur « je demande ce mode »
# (0x1800DA9A0) et « je demande ce sous-etat » (0x1800DA9C0), et Frederic a
# joue le scenario. Le journal tient en six lignes :
#
#     DA9C0  ecx = 3                      au demarrage
#     DA9A0  ecx = 4   +  DA9C0  ecx = 0x37     entree dans le MENU
#     DA9A0  ecx = 5   +  DA9C0  ecx = 0x25     VF.TERMINAL -> customize
#     ... et PLUS RIEN
#
# A LA SORTIE, AUCUNE DEMANDE N EST FAITE. Le sequenceur ne rend donc jamais
# 1 : ni 0x1801C2F92, ni l etat 31, ni l etat 70 ne sont sur ce chemin. La
# sortie fait ceci, a la fin de l etat 60 :
#
#     0x1801C41A5  xor eax, eax
#     0x1801C41A7  mov dword [rbx+0x7C], eax     <- L ETAT REPASSE A 0
#     0x1801C41AA  mov byte [rbx+0xBD], 0
#
# Elle BOUCLE sur l etat 0. Sur borne c est voulu : on rouvre le selecteur
# pour choisir une autre carte. Et c est pour cela que notre relais de l etat
# 0, dont le drapeau etait encore pose, renvoyait sur l ecran « Select Part » :
# C ETAIT NOUS QUI BOUCLIONS.
#
# ON PREND DONC LA SORTIE LA, et on la fait ressembler a ce que la sonde a vu
# le jeu faire pour entrer dans le menu : `mode 4` PUIS `sous-etat 0x37`, dans
# cet ordre -- important, car 0x1800DA9A0 remet a zero le drapeau de sous-etat
# (0x18070C51C) que 0x1800DA9C0 repose ensuite. Le sous-etat du MENU est bien
# 0x37 : mesure, la ou j avais ecrit 0x24 de memoire.
TRM_BCL_SITE = (0x1801C41A5, bytes.fromhex('33c0' '89437c'))
TRM_BCL_SUITE = 0x1801C41AA
TRM_BCL_MODE = 0x1800DA9A0
TRM_BCL_SOUS = 0x1800DA9C0
TRM_BCL_MENU = 4
TRM_BCL_MENU_SOUS = 0x37
TRM_BCL_FIN = 0x46                 # l etat de sortie du sequenceur
TRM_ETAT = 0x7C


def trm_boucle_relais(va, deja):
    """Par notre chemin, la sortie quitte le mode au lieu de boucler."""
    c = bytearray()
    c += bytes.fromhex('833d') + _rip(va, len(c) + 7, deja) + b'\x00'
    normal = len(c)
    c += bytes.fromhex('7400')                                 # je .normal
    c += bytes.fromhex('c705') + _rip(va, len(c) + 10, deja)
    c += struct.pack('<I', 0)                                  # drapeau = 0
    c += bytes.fromhex('b9') + struct.pack('<I', TRM_BCL_MENU)
    c += bytes.fromhex('e8') + _rip(va, len(c) + 5, TRM_BCL_MODE)
    c += bytes.fromhex('b9') + struct.pack('<I', TRM_BCL_MENU_SOUS)
    c += bytes.fromhex('e8') + _rip(va, len(c) + 5, TRM_BCL_SOUS)
    c += bytes.fromhex('c743') + bytes((TRM_ETAT,))
    c += struct.pack('<I', TRM_BCL_FIN)
    c += bytes.fromhex('e9') + _rip(va, len(c) + 5, TRM_BCL_SUITE)
    c[normal + 1] = len(c) - (normal + 2)                      # .normal
    assert 0 < c[normal + 1] < 128
    c += bytes.fromhex('31c0')                                 # xor eax, eax
    c += bytes.fromhex('89437c')                               # [rbx+0x7C] = eax
    c += bytes.fromhex('e9') + _rip(va, len(c) + 5, TRM_BCL_SUITE)
    assert len(c) <= _TRM_OBJ - _TRM_SORT, len(c)
    return bytes(c)


def trm_fermer_relais(va, obj):
    """La sous-page annulee referme AUSSI notre sous-menu.

    Site 0x1801DD898, dans la mise a jour : le moteur y remet la sous-page a
    zero apres l avoir fermee (0x1802450A0). Pour NOTRE instance on y ajoute
    `[objet+0x2F0] = 1`, le drapeau « ce sous-menu est fini » que 0x1801DE422
    pose lui-meme sur l annulation -- sans quoi on resterait sur un sous-menu
    qui ne dessine rien.
    """
    c = bytearray()
    c += bytes.fromhex('48c783') + struct.pack('<I', TRM_SOUS_PAGE)
    c += struct.pack('<I', 0)                                  # [2F8] = 0
    c += bytes.fromhex('4c8d15') + _rip(va, len(c) + 7, obj)   # lea r10, obj
    c += bytes.fromhex('4c39d3')                               # cmp rbx, r10
    c += bytes.fromhex('7507')                                 # jne .fin
    c += bytes.fromhex('c683') + struct.pack('<I', TRM_ETATS) + b'\x01'
    c += bytes.fromhex('e9') + _rip(va, len(c) + 5, TRM_FERMER_SUITE)
    assert len(c) <= _TRM_VT - _TRM_D, len(c)
    return bytes(c)


# ---------------------------------------------------------------------------
# `--film-cadres` -- LE FILM EN PLEIN ECRAN, CADRES COMPRIS (journal 158)
#
# CONSTAT DE FREDERIC (2026-10-13) : « le cadre du sous menu reste au premier
# plan pendant la lecture des videos. C est un probleme que nous avons deja
# rencontre et que tu avais regle avant les modifications d hier. »
#
# IL AVAIT RAISON, ET LE DIFF LE PROUVE. Dans la DLL du 2026-10-12
# (sauvegarde_urgence/), le relais pose sur `0x1801DD7A0` COMMENCE par un
# appel que la DLL d aujourd hui n a plus :
#
#     0x180EA52A3  push rcx ; sub rsp,0x20
#     0x180EA52A8  call 0x180EA5156        <- LE RELAIS DISPARU
#     0x180EA52AD  add rsp,0x20 ; pop rcx
#     ... la suite, identique octet pour octet a la notre
#
# Le reste est le meme. Ce chantier-la vivait dans le patcheur COMPILE du 12
# et n est PAS dans `socle_20261008.pyc` : vingt options du socle essayees une
# a une, aucune ne le repose. Il a ete perdu au changement de socle. On le
# reecrit donc en clair, a partir du relais relu dans la DLL du 12.
#
# CE QU IL FAIT, et pourquoi quatre fenetres (journal 158). Les cadres -- le
# bandeau de titre et la boite a lignes -- sont des objets AET que le moteur
# redessine de lui-meme : les cacher demande de FERMER l objet, pas de sauter
# un dessin. Il y en a QUATRE : deux a la page du sous-menu (`+0x240`,
# `+0x298`) et deux au MENU PRINCIPAL, qui vit derriere et garde les siennes
# ouvertes. Le menu principal est a `objet - 0x2328` (la page range son
# sous-menu a cet offset), d ou `-0x20E8` et `-0x2090`.
#
#     +0x00  etat  0 eteint | 1 a charger | 2 en cours | 3 PRET | 4 a fermer
#     +0x04  le RANG de la composition
#     0x1801BDA20(fen, rang)  libere, puis pose `rang` et etat = 1
#     0x1801BBA20(fen)        etat 3 -> 4 ; sinon libere et etat = 0
#
# DEUX APPELS D AFFILEE A 0x1801BBA20 donnent une fermeture nette : le premier
# passe 3 -> 4, le second tombe dans l autre branche et libere.
#
# LE RANG EST RELEVE, PAS INVENTE : on lit `+0x04` avant de fermer et on le
# rend a la reouverture. Le jeu lui-meme repose la fenetre de choix avec un
# rang qui depend du cas ; une constante aurait rendu un Movie Theater a deux
# lignes.
#
# ET ROUVRIR NE SUFFIT PAS : la mise a jour de la page de MENU (0x1801DC620)
# ne contient AUCUN appel au tic AET 0x1801BBB10, la ou ses cinq soeurs en ont
# deux chacune -- c est la coupe du build arcade. Hors film, tant qu une
# fenetre du menu principal n est pas a l etat 3, le relais lui donne son tic.
# C est auto-limite : des que l etat vaut 3, plus rien n est appele.
#
# LE DRAPEAU « UN FILM JOUE » N EST PAS CODE EN DUR : c est celui que le socle
# fait lire aux deux gardes de dessin (MENU2_FILM_CACHER). On le RELIT dans la
# DLL patchee, a la garde posee sur 0x1801E0C80 -- le dessin de `TaskMenuMain`,
# que nous ne touchons jamais -- dont la premiere instruction est
# `cmp dword [rip+d32], 0`. Il bouge avec la greffe du socle ; le lire evite de
# le perdre a la prochaine option ajoutee.
FLM_SITE = 0x1801DD7A0         # DLL PATCHEE : jmp <greffe du socle>
FLM_GARDE = 0x1801E0C80        # DLL PATCHEE : jmp <garde> ; la garde porte le
FLM_PAGE = 0x2328              # drapeau. L ecart page <-> sous-menu.
FLM_FEN = (0x240, 0x298, 0x240 - FLM_PAGE, 0x298 - FLM_PAGE)
FLM_POSER = 0x1801BDA20        # (fenetre, rang)
FLM_FERMER = 0x1801BBA20       # (fenetre)
FLM_TIC = 0x1801BBB10          # (fenetre)
_FLM_RELAIS, _FLM_CORPS, _FLM_DON = 0x000, 0x040, 0x280


def flm_relais(va, corps, socle):
    """Le detour de 0x1801DD7A0 : notre passe, puis celle du socle."""
    c = bytearray()
    c += bytes.fromhex('51')                            # push rcx
    c += bytes.fromhex('4883ec20')                      # sub rsp, 0x20
    c += bytes.fromhex('e8') + _rip(va, len(c) + 5, corps)
    c += bytes.fromhex('4883c420')                      # add rsp, 0x20
    c += bytes.fromhex('59')                            # pop rcx
    c += bytes.fromhex('e9') + _rip(va, len(c) + 5, socle)
    assert len(c) <= _FLM_CORPS - _FLM_RELAIS, len(c)
    return bytes(c)


def flm_corps(va, don, film, instance):
    """Ferme les quatre cadres pendant le film, les rouvre apres.

    `don` : 0x00 le drapeau « fermees », 0x04..0x10 les quatre rangs releves.
    `film` : le drapeau du socle, relu dans la DLL. `instance` : l objet de
    VF.TERMINAL, qui ne vit PAS dans la page -- `rbx - 0x2328` y serait du
    vide, donc on passe notre tour.
    """
    def g(i):
        return don + 4 * i

    def lea_rcx(delta):
        return bytes.fromhex('488d8b') + struct.pack('<i', delta)

    c = bytearray()
    c += bytes.fromhex('53')                            # push rbx
    c += bytes.fromhex('4883ec20')                      # sub rsp, 0x20
    c += bytes.fromhex('488bd9')                        # mov rbx, rcx
    c += bytes.fromhex('4c8d15') + _rip(va, len(c) + 7, instance)
    c += bytes.fromhex('4c39d3')                        # cmp rbx, r10
    jne_pas_nous = len(c)
    c += bytes.fromhex('0f85') + bytes(4)               # jne .pas_nous
    # NOTRE INSTANCE : ON GARDE SES DEUX FENETRES FERMEES. Son dessin est deja
    # muet (creneau 4 de notre vtable), mais le CADRE lui-meme est un objet AET
    # que le moteur dessine de son cote -- c est la lecon du journal 158, et
    # Frederic l a revue a l ecran : « il y a un cadre en trop qui entoure le
    # cadre rouge avec akira inscrit ». 0x1801BBA20 converge : etat 3 -> 4,
    # puis libere et 0 ; l appeler a chaque trame est sans effet une fois a 0.
    for _d in FLM_FEN[:2]:
        c += bytes.fromhex('488d8b') + struct.pack('<i', _d)
        c += bytes.fromhex('e8') + _rip(va, len(c) + 5, FLM_FERMER)
    jmp_fin0 = len(c)
    c += bytes.fromhex('e9') + bytes(4)
    o_pas_nous = len(c)
    c += bytes.fromhex('833d') + _rip(va, len(c) + 7, film) + b'\0'
    jne_film = len(c)
    c += bytes.fromhex('0f85') + b'\0\0\0\0'            # jne .film
    c += bytes.fromhex('833d') + _rip(va, len(c) + 7, g(0)) + b'\0'
    jne_rouvrir = len(c)
    c += bytes.fromhex('0f85') + b'\0\0\0\0'            # jne .rouvrir
    # ni film ni fermees : le tic des deux fenetres du MENU PRINCIPAL
    for d in FLM_FEN[2:]:
        c += lea_rcx(d)
        c += bytes.fromhex('833903')                    # cmp dword [rcx], 3
        c += bytes.fromhex('7405')                      # je +5
        c += bytes.fromhex('e8') + _rip(va, len(c) + 5, FLM_TIC)
    jmp_fin1 = len(c)
    c += bytes.fromhex('e9') + b'\0\0\0\0'
    # .rouvrir : on rend a chaque fenetre le rang qu on lui a pris
    o_rouvrir = len(c)
    for i, d in enumerate(FLM_FEN):
        c += lea_rcx(d)
        c += bytes.fromhex('8b15') + _rip(va, len(c) + 6, g(1 + i))
        c += bytes.fromhex('e8') + _rip(va, len(c) + 5, FLM_POSER)
    c += bytes.fromhex('c705') + _rip(va, len(c) + 10, g(0))
    c += struct.pack('<I', 0)
    jmp_fin2 = len(c)
    c += bytes.fromhex('e9') + b'\0\0\0\0'
    # .film : relever les rangs, puis fermer net -- deux appels d affilee
    o_film = len(c)
    c += bytes.fromhex('833d') + _rip(va, len(c) + 7, g(0)) + b'\0'
    jne_fin = len(c)
    c += bytes.fromhex('0f85') + b'\0\0\0\0'            # jne .fin
    for i, d in enumerate(FLM_FEN):
        c += bytes.fromhex('8b83') + struct.pack('<i', d + 4)
        c += bytes.fromhex('8905') + _rip(va, len(c) + 6, g(1 + i))
    for d in FLM_FEN:
        for _ in range(2):
            c += lea_rcx(d)
            c += bytes.fromhex('e8') + _rip(va, len(c) + 5, FLM_FERMER)
    c += bytes.fromhex('c705') + _rip(va, len(c) + 10, g(0))
    c += struct.pack('<I', 1)
    # .fin
    o_fin = len(c)
    c += bytes.fromhex('4883c420')                      # add rsp, 0x20
    c += bytes.fromhex('5b')                            # pop rbx
    c += bytes.fromhex('c3')                            # ret
    for pos, cible, taille in ((jne_pas_nous, o_pas_nous, 6),
                               (jmp_fin0, o_fin, 5),
                               (jne_film, o_film, 6),
                               (jne_rouvrir, o_rouvrir, 6),
                               (jne_fin, o_fin, 6),
                               (jmp_fin1, o_fin, 5), (jmp_fin2, o_fin, 5)):
        struct.pack_into('<i', c, pos + taille - 4, cible - (pos + taille))
    assert len(c) <= _FLM_DON - _FLM_CORPS, len(c)
    return bytes(c)


# ---------------------------------------------------------------------------
# `--versus-manette` -- OFFLINE VERSUS SUIT LA MANETTE, A CHAQUE TRAME
#
# `--menu-griser` grise TROIS entrees une fois pour toutes, a l init. Celle-ci
# en grise une QUATRIEME -- OFFLINE VERSUS -- mais seulement quand le second
# joueur n a pas de quoi jouer, et elle la rend des qu il en a.
#
# TROIS DES QUATRE PIECES EXISTAIENT DEJA, et elles sont mesurees :
#   . l etat d une entree est l octet `page + 0x642 + i`, et 1 = GRISE (le
#     dessin multiplie l alpha par 0,5 en 0x1801E0F51) ;
#   . le validateur 0x1801DDF54 envoie TOUT etat non nul dans une branche
#     bouchonnee : griser suffit a rendre l entree inerte ;
#   . le curseur saute les etats non nuls depuis 0x1801E4CD8 (--menu-griser).
# LA QUATRIEME MANQUAIT : l octet n etait ecrit qu A L INIT (0x1801E39E6 le met
# a zero, 0x1801E3A03 et 0x1801E3A0A posent les trois grisages). Il faut donc
# le reposer A CHAQUE TRAME, et c est tout ce que fait ce correctif.
#
# OU : LA MISE A JOUR DE LA PAGE, ET ELLE N APPARTIENT QU A ELLE. La vtable du
# menu principal est 0x180532AE8 -- creneau [1] init 0x1801E36D0, [2] mise a
# jour 0x1801DC620, [4] dessin 0x1801E0C80, [7] le creneau du curseur
# 0x1801E4CD0, [10] le validateur 0x1801DDF30. Balayage du binaire :
# `0x1801DC620` n a qu UN SEUL pointeur (0x180532AF8) et ZERO appel direct --
# cette fonction ne sert a aucune autre page.
#
# LE SITE : `0x1801DC638  mov rdi, rcx ; xor esi, esi`, cinq octets, soit
# exactement la taille d un `call`. Le prologue y est fini, `rcx` porte encore
# la page, et `rsp % 16 == 0` (entree a 8, cinq `push` et un `sub 0xA0`) : un
# `call` y place la pile dans l etat que l ABI demande. Le relais refait les
# deux instructions qu il recouvre.
#
# COMMENT ON DEMANDE LA MANETTE : `Input_isGamepadDetect`, LE CRENEAU 45.
# Ce n est pas un detour -- c est l interface de la borne, et le moteur sait
# deja s en servir. L objet d entrees est `[0x180C3B6F8]` et ses creneaux sont
# des relais vers apm.dll ; `analysis/apm_creneaux.json` les nomme, et les
# deux voisins le PROUVENT : +0x158 = creneau 43 = Input_isOn (14 sites), et
# +0x160 = creneau 44 = Input_isOnNow (26 sites, dont 0x1801A2BC0 qui lit la
# validation sur son FRONT -- la semantique colle). Donc +0x168 = creneau 45 =
# `Input_isGamepadDetect`, et le balayage dit qu AUCUN site du moteur ne
# l appelle : une borne APM3 n a pas de manette. Le stub y repondait 0 comme
# les quarante autres bouchons ; il y repond desormais pour de bon.
#
# ON NE LIT PAS UN CODE D ENTREE. `Input_isOnNow` ne vaut vrai que pendant la
# fenetre de 34 ms qui suit le front : un drapeau de PRESENCE n y survivrait
# pas. `Input_isGamepadDetect` ne depend d aucune horloge.
#
# ET LE CURSEUR NE RESTE PAS DESSUS. Le saut de 0x1801BBBE0 ne joue qu au
# DEPLACEMENT : si la ligne grise pendant qu on est pose dessus, le curseur y
# resterait, inerte. Le relais le ramene alors sur SINGLE PLAYER (entree 0),
# la seule qui ne grise jamais.
# LE SITE EST DESORMAIS UN `jmp` ET NON UN `call`, parce que le relais
# doit pouvoir decider que la page NE FAIT RIEN de la trame : il saute
# alors a 0x1801DCE33, la queue « rien a signaler » que le moteur emprunte
# lui-meme deux instructions plus loin (0x1801DC650). Consequence sur la
# pile : entre par `jmp`, le relais n a pas d adresse de retour empilee,
# donc `rsp % 16 == 0` des son entree et l accueil d un appel se reserve
# par `sub rsp, 0x20` -- et non 0x28 comme lorsqu il etait appele.
MAN_SITE = (0x1801DC638, bytes.fromhex('488bf9' '33f6'))
MAN_SUITE = 0x1801DC63D        # la page continue normalement
MAN_RIEN = 0x1801DCE33         # `xor al,al` : la page passe son tour
MAN_OBJET = 0x180C3B6F8        # l objet d entrees (un pointeur, pas la table)
MAN_CRENEAU = 0x168            # Input_isGamepadDetect
MAN_ETAT = 0x643               # page + 0x642 + 1 : OFFLINE VERSUS
MAN_CURSEUR = 0x58             # la ligne courante de la page


def man_relais(va, va_drapeau=None):
    """Rend l octet d etat d OFFLINE VERSUS egal a « pas de manette ».

    `rcx` porte la page a l entree ; on la met d abord dans `rdi` -- c est
    l instruction que le site portait, et `rdi` est NON VOLATIL sur Windows
    x64, donc elle survit a l appel. `esi` est remis a zero comme le faisait
    la seconde instruction recouverte, et il sert ensuite de zero.
    """
    def rip(fin, cible):
        return struct.pack('<i', cible - (va + fin))

    c = bytearray()
    c += bytes.fromhex('488bf9')                        # mov rdi, rcx
    c += bytes.fromhex('4883ec20')                      # sub rsp, 0x20
    c += bytes.fromhex('488b0d') + rip(len(c) + 7, MAN_OBJET)
    c += bytes.fromhex('488b01')                        # mov rax, [rcx]
    c += bytes.fromhex('ff90') + struct.pack('<I', MAN_CRENEAU)
    c += bytes.fromhex('4883c420')                      # add rsp, 0x20
    # ON REND `rcx`, ET CE N EST PAS UN DETAIL : l instruction qui SUIT le site
    # est `mov rcx, [rcx+0x650]`. Le premier essai ne la rendait pas, et le jeu
    # mourait d un acces interdit des le menu -- le moteur dereferencait notre
    # objet d entrees comme si c etait sa page. Mesure, pas chance : code de
    # sortie 0xC0000005 a 34 s, et la meme DLL sans ce relais tournait.
    c += bytes.fromhex('488bcf')                        # mov rcx, rdi
    c += bytes.fromhex('33f6')                          # xor esi, esi
    c += bytes.fromhex('84c0')                          # test al, al
    c += bytes.fromhex('7512')                          # jne .presente
    c += bytes.fromhex('c687') + struct.pack('<I', MAN_ETAT) + b'\x01'
    c += bytes.fromhex('837f') + bytes([MAN_CURSEUR]) + b'\x01'
    c += bytes.fromhex('7503')                          # jne .fin
    c += bytes.fromhex('8977') + bytes([MAN_CURSEUR])   # [rdi+0x58] = esi
    c += bytes.fromhex('eb07')                          # .fin: -> .suite
    c += bytes.fromhex('c687') + struct.pack('<I', MAN_ETAT) + b'\x00'
    # .suite -- ET C EST ICI QUE LA PAGE PEUT ETRE GELEE. Quand le menu est
    # garde derriere les ecrans de personnalisation (drapeau pose par la
    # sortie du mode MENU), il doit RESTER DESSINE mais ne plus rien lire :
    # sans cela ses trois taches consommeraient les memes touches que le
    # `Character Select`, et c est le defaut mesure en septembre sur
    # OFFLINE VERSUS. Le DESSIN n est pas touche -- c est un autre creneau.
    if va_drapeau is not None:
        c += bytes.fromhex('803d') + rip(len(c) + 7, va_drapeau) + b'\x00'
        c += bytes.fromhex('7505')                      # jne .geler
    c += bytes.fromhex('e9') + rip(len(c) + 5, MAN_SUITE)
    if va_drapeau is not None:
        c += bytes.fromhex('e9') + rip(len(c) + 5, MAN_RIEN)
    if len(c) > CPL_MAN_TAILLE:
        raise AssertionError('relais MAN : %d octets pour 0x%X'
                             % (len(c), CPL_MAN_TAILLE))
    return bytes(c)


# ---------------------------------------------------------------------------
# `--nom-donnees` -- « EDIT DATA NAME » FINIT LE CHEMIN DE SEGA
#
# MESURE du 2026-10-13. La ligne n est PAS inerte : elle EFFACE le nom.
# Le chemin est entier, et il tient deja les vingt caracteres :
#
#   0x1801C5096  mov byte [rbx+0x2A0], 1   la validation pose le drapeau
#   0x1801C50D8  call 0x180007430          l ouverture du clavier, bouchonnee
#
# puis, dans la mise a jour du CUSTOMIZE MENU :
#
#   0x1801C4F95  cmp byte [rdi+0x2A0], 0   drapeau pose ?
#   0x1801C4F9E  call 0x180029FB0          « finie ? »  -> mov al,1 : TOUJOURS
#   0x1801C4FB0  call 0x18005F840          le texte -> une chaine VIDE
#   0x1801C4FBD  movsxd rbx, [rdi+0x29C]   l index de l enregistrement
#   0x1801C4FC4  call 0x1801B8A10          la base de la table
#   0x1801C4FD6  mov r8d, 0x15             21 octets = 20 caracteres + le zero
#   0x1801C4FE2  call 0x1800133D0          strcpy_s(enregistrement+0x90, ...)
#   0x1801C4FEC  mov byte [rdi+0x2A0], 0   drapeau rendu
#
# Le pointeur rendu par 0x18005F840 vise 0x180347568, longueur ZERO : valider
# la ligne recopie donc `""` par-dessus le nom.
#
# ON NE TOUCHE PAS LES FONCTIONS, ON PATCHE LES SITES -- elles sont partagees :
# 0x180029FB0 a 73 appelants, 0x180007430 en a 601. (`feedback_garde_partagee`.)
#
# LE RESTE EXISTE : le champ est a +0x68 d un enregistrement de 0x80, soit 24
# octets de place ; le remplisseur du selecteur (0x1801D0B00) recopie
# l enregistrement ENTIER par quatre `vmovups ymm` et son dessin passe le
# pointeur `selecteur + 0x2F8 + ligne*0x84` -- exactement +0x68 -- a un
# formateur, SANS ecretage. Un nom de vingt caracteres s affiche donc tel quel.
# Et la table est celle qu `apm.dll` sauve deja dans `ram/customize.bin`
# (PERSO_RVA 0x752148, tete 0x28, pas 0x80) : le nom persiste sans rien de plus.
#
# LE MENU EST GELE PENDANT LA SAISIE, ET C EST LE MOTEUR QUI LE FAIT : quand le
# drapeau est pose, 0x1801C4F9C saute par-dessus 0x1801C4FF5, le traitement
# normal des entrees. Aucune touche ne part donc dans le menu pendant qu on
# tape, et il n y a rien a neutraliser.
#
# LA SORTIE DE SECOURS EST DANS LE RELAIS, pas dans le stub : si `apm.dll` n a
# pas annonce sa presence, `ouvrir` pose l etat 4 -- « abandon » -- que `fini`
# declare termine et dont `texte` rend NULL. Le moteur saute alors la recopie
# (0x1801C4FBB) et rend le drapeau : exactement le comportement d aujourd hui,
# MOINS l effacement. Sans cela, une borne sans stub gelerait son menu.
NOM_MAGIE = b'VF5NAME\x00'
NOM_O_ETAT = 0x08        # 0 repos, 1 saisie, 2 valide, 3 annule, 4 abandon
NOM_O_MAXI = 0x0C        # ce que le moteur a demande (0x14)
NOM_O_PRESENT = 0x10     # apm.dll y pose 1 des qu il a trouve la zone
NOM_O_LONG = 0x14        # la longueur courante, tenue par le stub
# LA DESTINATION DU MOTEUR, rangee par le relais : `r8` porte `[rbx+0x90]` au
# site 0x1801C50D8, c est-a-dire l enregistrement+0x68. Le stub y relit le nom
# COURANT pour ouvrir le champ dessus, au lieu d un champ vide.
NOM_O_DEST = 0x18        # un pointeur
NOM_O_TAMPON = 0x20      # 0x20 octets
# LE CLAVIER VIRTUEL (2026-10-13). La saisie etait AVEUGLE -- le journal montre
# Frederic tapant ses touches de menu sans le savoir. On dessine donc le champ
# et une grille, depuis le CRENEAU 4 de la vtable du CUSTOMIZE MENU
# (0x18052FCF8 + 0x20 = 0x1801C51B0), qui est la phase de rendu de cette page.
# Le relais appelle le dessin d origine PUIS saute chez apm.dll, dont le stub
# a depose l adresse : tout le dessin vit donc en C, la ou il se relit, et il
# tourne quand meme sur le fil du moteur et dans la bonne phase.
NOM_O_PAGE = 0x40        # la page, rangee par le relais de dessin
NOM_O_DESSIN = 0x48      # l adresse de notre dessin, posee par apm.dll
NOM_O_CURSEUR = 0x50     # la case choisie dans la grille, tenue par le stub
NOM_O_OUVRIR = 0x60
NOM_O_FINI = 0xC0
NOM_O_TEXTE = 0xE0
NOM_O_DESSIN_RELAIS = 0x120
# NOTRE PROPRE FENETRE AET, 0x58 octets. `0x1801BDA20` ne demande AUCUN
# constructeur : sur un bloc a zero il se contente de poser `[fen+4] = rang` et
# `[fen] = 1` (0x1801BDA7C). Le reste est la machine a etats du tic
# (0x1801BBB10) -- etat 1 a charger, 3 pret, 4 a fermer. Ses ANCRES reglent du
# meme coup les resolutions : on dessine sur `p_txt_0N_lt` de NOTRE fenetre, et
# non a des pixels comptes pour 1920 x 1080.
NOM_O_FENETRE = 0x180
NOM_VT = 0x18052FCF8     # la vtable du CUSTOMIZE MENU
NOM_VT_DESSIN = NOM_VT + 4 * 8
NOM_DESSIN_ORIG = 0x1801C51B0
# (site, octets attendus, offset du relais dans la zone)
NOM_SITES = ((0x1801C50D8, bytes.fromhex('e85323e4ff'), NOM_O_OUVRIR),
             (0x1801C4F9E, bytes.fromhex('e80d50e6ff'), NOM_O_FINI),
             (0x1801C4FB0, bytes.fromhex('e88ba8e9ff'), NOM_O_TEXTE))


def nom_ouvrir(va, zone):
    """Arme la capture. `edx` porte la longueur maximale voulue (0x14)."""
    def rip(fin, cible):
        return struct.pack('<i', cible - (va + fin))

    c = bytearray()
    c += bytes.fromhex('833d') + rip(len(c) + 7, zone + NOM_O_PRESENT) + b'\x00'
    saut_non = len(c)
    c += bytes.fromhex('7400')                          # je .non (comble plus bas)
    c += bytes.fromhex('c705') + rip(len(c) + 10, zone + NOM_O_ETAT)
    c += struct.pack('<I', 1)
    c += bytes.fromhex('8915') + rip(len(c) + 6, zone + NOM_O_MAXI)
    c += bytes.fromhex('c705') + rip(len(c) + 10, zone + NOM_O_LONG)
    c += struct.pack('<I', 0)
    c += bytes.fromhex('4c8905') + rip(len(c) + 7, zone + NOM_O_DEST)
    c += bytes.fromhex('4831c0')                        # xor rax, rax
    c += bytes.fromhex('488905') + rip(len(c) + 7, zone + NOM_O_TAMPON)
    saut_fin = len(c)
    c += bytes.fromhex('eb00')                          # jmp .fin
    c[saut_non + 1] = len(c) - (saut_non + 2)           # .non est ici
    c += bytes.fromhex('c705') + rip(len(c) + 10, zone + NOM_O_ETAT)
    c += struct.pack('<I', 4)                           # abandon
    c[saut_fin + 1] = len(c) - (saut_fin + 2)           # .fin est ici
    c += bytes.fromhex('31c0')                          # xor eax, eax
    c += bytes.fromhex('c3')                            # ret
    if len(c) > NOM_O_FINI - NOM_O_OUVRIR:
        raise AssertionError('relais NOM/ouvrir : %d octets pour 0x%X'
                             % (len(c), NOM_O_FINI - NOM_O_OUVRIR))
    return bytes(c)


def nom_fini(va, zone):
    """Rend VRAI des que l etat est 2 (valide), 3 (annule) ou 4 (abandon)."""
    def rip(fin, cible):
        return struct.pack('<i', cible - (va + fin))

    c = bytearray()
    c += bytes.fromhex('8b05') + rip(len(c) + 6, zone + NOM_O_ETAT)
    c += bytes.fromhex('83f802')                        # cmp eax, 2
    c += bytes.fromhex('0f93c0')                        # setae al
    c += bytes.fromhex('c3')
    if len(c) > NOM_O_TEXTE - NOM_O_FINI:
        raise AssertionError('relais NOM/fini : %d octets pour 0x%X'
                             % (len(c), NOM_O_TEXTE - NOM_O_FINI))
    return bytes(c)


def nom_relais_dessin(va, zone):
    # Le dessin d origine, puis le notre -- par-dessus, et seulement en
    # saisie. `rcx` porte la page : on la range pour le stub, on appelle
    # le dessin de la page (son retour est RENDU tel quel, il ne nous
    # appartient pas), puis on saute chez apm.dll si la saisie est
    # ouverte et qu il a depose son adresse.
    def rip(fin, cible):
        return struct.pack('<i', cible - (va + fin))

    c = bytearray()
    c += bytes.fromhex('48890d') + rip(len(c) + 7, zone + NOM_O_PAGE)
    c += bytes.fromhex('53')                            # push rbx
    c += bytes.fromhex('56')                            # push rsi
    c += bytes.fromhex('4883ec28')                      # sub rsp, 0x28
    c += bytes.fromhex('4889cb')                        # mov rbx, rcx
    c += bytes.fromhex('e8') + rip(len(c) + 5, NOM_DESSIN_ORIG)
    c += bytes.fromhex('89c6')                          # mov esi, eax
    c += bytes.fromhex('833d') + rip(len(c) + 7, zone + NOM_O_ETAT) + b'\x01'
    saut1 = len(c)
    c += bytes.fromhex('7500')                          # jne .fin
    c += bytes.fromhex('488b05') + rip(len(c) + 7, zone + NOM_O_DESSIN)
    c += bytes.fromhex('4885c0')                        # test rax, rax
    saut2 = len(c)
    c += bytes.fromhex('7400')                          # je .fin
    c += bytes.fromhex('4889d9')                        # mov rcx, rbx
    c += bytes.fromhex('ffd0')                          # call rax
    c[saut1 + 1] = len(c) - (saut1 + 2)
    c[saut2 + 1] = len(c) - (saut2 + 2)
    c += bytes.fromhex('89f0')                          # mov eax, esi
    c += bytes.fromhex('4883c428')                      # add rsp, 0x28
    c += bytes.fromhex('5e')                            # pop rsi
    c += bytes.fromhex('5b')                            # pop rbx
    c += bytes.fromhex('c3')
    if len(c) > CPL_NOM_TAILLE - NOM_O_DESSIN_RELAIS:
        raise AssertionError('relais NOM/dessin : %d octets pour 0x%X'
                             % (len(c), CPL_NOM_TAILLE - NOM_O_DESSIN_RELAIS))
    return bytes(c)


def nom_texte(va, zone):
    """Rend le tampon si la saisie est VALIDEE, NULL sinon -- et desarme.

    NULL n est pas un echec : le moteur teste `rax` en 0x1801C4FB8 et saute la
    recopie. Annuler laisse donc le nom tel qu il etait.
    """
    def rip(fin, cible):
        return struct.pack('<i', cible - (va + fin))

    c = bytearray()
    c += bytes.fromhex('31c0')                          # xor eax, eax
    c += bytes.fromhex('833d') + rip(len(c) + 7, zone + NOM_O_ETAT) + b'\x02'
    saut = len(c)
    c += bytes.fromhex('7500')                          # jne .fin
    c += bytes.fromhex('488d05') + rip(len(c) + 7, zone + NOM_O_TAMPON)
    c[saut + 1] = len(c) - (saut + 2)
    c += bytes.fromhex('c705') + rip(len(c) + 10, zone + NOM_O_ETAT)
    c += struct.pack('<I', 0)
    c += bytes.fromhex('c3')
    if len(c) > CPL_NOM_TAILLE - NOM_O_TEXTE:
        raise AssertionError('relais NOM/texte : %d octets pour 0x%X'
                             % (len(c), CPL_NOM_TAILLE - NOM_O_TEXTE))
    return bytes(c)


# ---------------------------------------------------------------------------
# `--sans-ecran-epilepsie` -- L ECRAN D AVERTISSEMENT NE SE JOUE PLUS
#
# RETROUVE LE 2026-10-12, sur constat de Frederic : « l ecran sur l epilepsie
# est de nouveau visible ». Il avait raison, et ce n etait pas une impression :
# l option vivait dans le source detruit, le pilote ne la portait pas, et
# `item_porte.cmd` la demandait dans le vide -- un nom inconnu est ignore en
# silence. Elle a ete RELEVEE DANS LA DLL DE REFERENCE du 12, puis comprise.
#
# CE N EST PAS LE MEME ECRAN QUE `--sans-epilepsie`, et la distinction a deja
# coute un essai en septembre. `--sans-epilepsie` (socle) retire le TEXTE
# dessine par le creneau +0x20 de 0x18034CB90 pendant DATA_INITIALIZE. Ici il
# s agit de la PRESENTATION DE DEMARRAGE, qui est une animation AET.
#
# LA MESURE. `0x18006BBE0` prepare trois chaines pour la presentation : le nom
# de la scene, le marqueur de DEBUT et le marqueur de FIN.
#
#     0x18006BC1D  lea rax, [rip+0x2E1120]   -> 0x18034CD44  "SEGA_e"
#     0x18006BC24  lea rcx, [rip+0x2E1125]   -> 0x18034CD50  "INFO_end"
#     0x18006BC2B  cmp byte [0x180C3B701], 0 ; cmove rax, rcx
#
# `0x180C3B701` est L AIGUILLAGE BORNE/CONSOLE (32 references, journal du
# 2026-10-07) : a zero on est en CONSOLE, et la fin est « INFO_end ».
#
# ET LES MARQUEURS SE LISENT DANS LA PLANCHE. `aet_n_adv.bin`, scene MAIN,
# composition racine, calque `logo_jpn` -- douze marqueurs, en clair :
#
#     ATTENTION_01_s@0    ATTENTION_01_e@319   ATTENTION_02_s@320
#     ATTENTION_02_e@639  SEGA_s@640           SEGA_e@779
#     AM2_s@780           AM2_e@919            CRI_s@920
#     CRI_e@1059          INFO_st@1060         INFO_end@1380
#
# (et `logo_usu` les memes, decales : CRI_e@679, INFO_st@680, INFO_end@1000.)
#
# L ECRAN D EPILEPSIE EST DONC LE SEGMENT `INFO_st` -> `INFO_end` : 320 trames
# a 60 images par seconde, soit 5,3 s -- exactement la duree relevee a l ecran
# (captures t09 a t13 de `tools/essai_adv.py`). Finir sur **CRI_e** arrete la
# presentation juste apres le logo CRIWARE, avant `INFO`.
#
# ON NE RETIRE DONC AUCUN CODE : on change le marqueur de fin. La chaine
# « CRI_e » n existe pas dans le binaire -- on l ecrit dans le bourrage qui
# suit « INFO_end » (0x18034CD58 a 0x18034CD5F, huit octets a zero dans le
# `.origine`), et on fait pointer le `lea` dessus. C est OCTET POUR OCTET ce
# que porte la DLL de reference du 12.
EPILEPSIE = [
    (0x18034CD59, bytes(6), b'CRI_e\x00'),
    (0x18006BC27, bytes.fromhex('25112e00'), bytes.fromhex('2e112e00')),
]


# =========================================================================
# `--films-theatre` : LE MOVIE THEATER JOUE LE FILM CHOISI (2026-10-15)
#
# MESURE. Le socle dessine bien la liste -- son relais 0x180EA631C calcule
# `0x2A0 + rdi`, ou `rdi` est l indice de la ligne, et sa chaine de libelles
# en nomme quatorze. Mais SON LANCEUR NE REGARDE PAS L INDICE : il porte
# `lea rdx, "rom/movie/vf5adv.sfd"` en dur et ses DEUX appelants ne lui
# passent rien. Quelle que soit la ligne, c est `vf5adv` qui part.
#
# Et le compte ne tombe pas juste non plus : le socle ecrit TREIZE lignes
# (`mov dword [rbx+0x224], 0xD`) pour quatorze libelles -- la derniere est
# injoignable.
#
# L INDICE EST AU MEME ENDROIT AUX DEUX SITES, et c est ce qui rend le
# chantier simple : `0x1801DE354` fait `mov rbx, rcx` et `0x1801DE362`
# `mov edi, [rcx+0x58]`. Donc `rbx` porte l objet du menu et `[rbx+0x58]` la
# ligne, aussi bien en 0x180EA644C qu en 0x180EA646B.
#
# ON NE NOTE AUCUNE ADRESSE DU SOCLE : elles bougent avec sa disposition. Tout
# se retrouve par SIGNATURE dans la `.greffe` produite -- le `lea` vers la
# chaine du film, les deux `call` qui l entourent, le compte de lignes, et les
# maillons de la chaine de libelles (`81 F9 <id> 75 08 48 8D 05 <rel> C3`).
#
# LA GREFFE N A AUCUNE RELOCATION : on ne range donc jamais une adresse
# absolue. Le relais CALCULE l adresse de la chaine en RIP-relatif et la pose
# dans un creneau que le lanceur relit par `mov rdx, [rip+creneau]` -- sept
# octets, exactement ceux du `lea` qu il remplace.
#
# LA TABLE SE DEDUIT DES NOMS DE FICHIERS, sauf `vf5moe` que Frederic a
# nomme : « Virtua Fighters 5 Girls ». Les cinq libelles du socle sans fichier
# (El Blaze and Wolf demo, Eileen demo, Promotional movie A/B/C) tombent :
# leurs films ne sont pas sur le disque.
# =========================================================================

# (nom de fichier sans chemin ni extension, libelle affiche)
TVF_FILMS = (
    ('vf5verAadv',  'Opening movie VF5 version A'),
    ('vf5verAend',  'Ending movie VF5 version A'),
    ('vf5verBadv',  'Opening movie VF5 version B'),
    ('vf5verCadv',  'Opening movie VF5 version C'),
    ('vf5adv',      'Opening movie VF5 Final Showdown'),
    ('vf5FSend',    'Ending movie VF5 Final Showdown'),
    ('vf5Radv',     'Opening movie VF5 R'),
    ('vf5Rend',     'Ending movie VF5 R'),
    ('vf5REVOend',  'Ending movie Virtua Fighter eSports'),
    ('vf5end',      'Ending movie VF5'),
    ('vf5moe',      'Virtua Fighters 5 Girls'),
)
TVF_PAS_NOM = 0x20          # la place d un " rom/movie/xxx.sfd "
TVF_PAS_LIB = 0x28          # la place d un libelle
TVF_O_CRENEAU = 0x000       # le pointeur que le lanceur relit
TVF_O_RELAIS = 0x020        # notre relais
TVF_O_NOMS = 0x0E0          # la table des chemins
TVF_O_LIBS = TVF_O_NOMS + TVF_PAS_NOM * len(TVF_FILMS)
TVF_O_RESTER = 0x460        # le relais " rester sur la page "
TVF_FIN = TVF_O_LIBS + TVF_PAS_LIB * len(TVF_FILMS)
# L ASSERTION QUI MANQUAIT, ET CE QU ELLE A COUTE (2026-10-15). TVF_FIN valait
# 0x420 pour une zone de 0x400 : trente-deux octets de trop. Or NOTRE BLOC
# FINIT EXACTEMENT A LA FIN DE LA SECTION `.greffe` -- le debordement est donc
# alle ecrire " 5 Girls " sur les premiers octets de `.decors` (0x180EB1000),
# la table des descripteurs de decors, cherchee PAR NOM, enregistrements de
# 0xF0 octets. Premier nom ecrase, la recherche ne trouve plus rien et sort du
# tableau : faute en 0x18018F5C3, sept secondes apres le lancement -- et
# 0x180EB1000 apparaissait deux fois sur la pile.
#
# C est le piege 3 du briefing mot pour mot : CHAQUE ASSERTION DE TAILLE DOIT
# VISER LA BORNE IMMEDIATEMENT SUIVANTE. J avais verifie la taille du relais,
# pas celle des donnees -- et la borne d apres n etait pas une autre zone a
# nous, c etait une AUTRE SECTION.
if TVF_FIN > CPL_TVF_TAILLE:
    raise AssertionError(
        'zone TVF : 0x%X octets de donnees pour 0x%X -- le debordement irait '
        'dans la section qui suit la greffe' % (TVF_FIN, CPL_TVF_TAILLE))
TVF_CHAINE_ADV = 0x1803A1598        # "rom/movie/vf5adv.sfd", dans le .rdata
# LE BRANCHEMENT QUI FAIT SORTIR DE VF.TV. `cmp edi,1 ; jne 0x1801DE402` :
# cinq octets, intacts dans le `.origine`. On y pose un saut vers un relais
# qui ajoute la condition " sommes-nous dans le Movie Theater ".
TVF_SORTIE = 0x1801DE3A4
TVF_SORTIE_TETE = bytes.fromhex('83ff017559')
TVF_RESTER = 0x1801DE3EE            # la fin de la ligne 0 : on reste
TVF_QUITTER = 0x1801DE402           # la fin des autres : on ferme et on sort
TVF_REPLAY = 0x1801DE3A9            # la ligne 1 hors theatre : Replay Menu
# LES DEUX FONCTIONS DU MOTEUR QU ON APPELLE. Ce sont celles dont le socle se
# sert lui-meme dans sa branche " bouton presse " (0x180EA6504..0x180EA650D) :
# on ne fait rien de neuf, on le fait au bon moment.
TVF_OCCUPE = 0x1800E8800            # TaskMovie est-elle encore occupee ?
TVF_LIBERER = 0x1800E89A0           # la retirer de la liste des taches
TVF_ID0 = 0x2A0                     # le premier identifiant de libelle


def tvf_donnees(va_zone):
    """Les chemins et les libelles, a plat, prets a ecrire."""
    b = bytearray(TVF_FIN - TVF_O_NOMS)
    for i, (fic, lib) in enumerate(TVF_FILMS):
        chemin = ('rom/movie/%s.sfd' % fic).encode('ascii')
        if len(chemin) >= TVF_PAS_NOM:
            raise AssertionError('chemin trop long : %r' % chemin)
        o = TVF_PAS_NOM * i
        b[o:o + len(chemin)] = chemin
        texte = lib.encode('ascii')
        if len(texte) >= TVF_PAS_LIB:
            raise AssertionError('libelle trop long : %r' % texte)
        o = (TVF_O_LIBS - TVF_O_NOMS) + TVF_PAS_LIB * i
        b[o:o + len(texte)] = texte
    return bytes(b)


def tvf_relais(va, va_zone, va_lanceur):
    """Pose dans le creneau l adresse du film de la ligne choisie.

    `rbx` porte l objet du menu aux DEUX sites d appel ; `[rbx+0x58]` est la
    ligne -- mesure a l execution, pas deduite. On borne, on multiplie par le
    pas, on ajoute la base de la table -- tout en RIP-relatif, la greffe
    n ayant aucune relocation -- et on SAUTE au lanceur du socle, dont le
    `ret` rendra la main a l appelant d origine. La pile est rendue intacte
    avant le saut : sinon ce `ret` reviendrait sur nos pousses.
    """
    def rip(fin, cible):
        return struct.pack('<i', cible - (va + fin))

    c = bytearray()
    c += bytes.fromhex('50')                            # push rax
    c += bytes.fromhex('51')                            # push rcx
    c += bytes.fromhex('48634358')                      # movsxd rax,[rbx+0x58]
    c += bytes.fromhex('4883f8') + bytes([len(TVF_FILMS)])   # cmp rax, n
    c += bytes.fromhex('7202')                          # jb +2
    c += bytes.fromhex('31c0')                          # xor eax, eax
    c += bytes.fromhex('486bc0') + bytes([TVF_PAS_NOM])  # imul rax, rax, pas
    c += bytes.fromhex('488d0d') + rip(len(c) + 7, va_zone + TVF_O_NOMS)
    c += bytes.fromhex('4801c8')                        # add rax, rcx
    c += bytes.fromhex('488905') + rip(len(c) + 7, va_zone + TVF_O_CRENEAU)
    c += bytes.fromhex('59')                            # pop rcx
    c += bytes.fromhex('58')                            # pop rax
    c += bytes.fromhex('e9') + rip(len(c) + 5, va_lanceur)
    if len(c) > TVF_O_NOMS - TVF_O_RELAIS:
        raise AssertionError('relais TVF : %d octets pour 0x%X'
                             % (len(c), TVF_O_NOMS - TVF_O_RELAIS))
    return bytes(c)


def tvf_rester(va, va_drapeau):
    """Si l on est dans le Movie Theater, rester sur la page.

    Sinon, refaire EXACTEMENT ce que faisait l original : `cmp edi,1`, et
    sortir si ce n est pas la ligne 1. Hors theatre, VF.TV ne change pas.
    """
    def rip(fin, cible):
        return struct.pack('<i', cible - (va + fin))

    c = bytearray()
    c += bytes.fromhex('833d') + rip(len(c) + 7, va_drapeau) + b'\x00'
    saut = len(c)
    c += bytes.fromhex('7400')                          # je .normal
    c += bytes.fromhex('e9') + rip(len(c) + 5, TVF_RESTER)
    c[saut + 1] = len(c) - (saut + 2)
    c += bytes.fromhex('83ff01')                        # cmp edi, 1
    c += bytes.fromhex('0f85') + rip(len(c) + 6, TVF_QUITTER)
    c += bytes.fromhex('e9') + rip(len(c) + 5, TVF_REPLAY)
    if len(c) > CPL_TVF_TAILLE - TVF_O_RESTER:
        raise AssertionError('relais TVF/rester : %d octets pour 0x%X'
                             % (len(c), CPL_TVF_TAILLE - TVF_O_RESTER))
    return bytes(c)


def tvf_reperer(chemin):
    """Retrouve, PAR SIGNATURE, les morceaux du socle a reprendre.

    Rend un dictionnaire, ou leve une AssertionError qui NOMME ce qui manque.
    Jamais d adresse notee : le socle les deplace a chaque changement.
    """
    import pefile
    pe = pefile.PE(chemin, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    sec = None
    for s in pe.sections:
        if s.Name.rstrip(b'\0') == b'.greffe':
            sec = s
    pe.close()
    if sec is None:
        raise AssertionError('pas de section .greffe')
    va = base + sec.VirtualAddress
    off = sec.PointerToRawData
    n = min(sec.Misc_VirtualSize, sec.SizeOfRawData)
    with open(chemin, 'rb') as fp:
        fp.seek(off)
        g = fp.read(n)

    # 1. le `lea rdx, "rom/movie/vf5adv.sfd"` du lanceur
    leas = []
    for i in range(n - 7):
        if g[i:i + 3] != b'\x48\x8d\x15':
            continue
        if va + i + 7 + struct.unpack_from('<i', g, i + 3)[0] == TVF_CHAINE_ADV:
            leas.append(va + i)
    if len(leas) != 1:
        raise AssertionError('lea vers la chaine du film : %d trouve(s), 1 '
                             'attendu' % len(leas))
    va_lea = leas[0]

    # 2. l entree du lanceur : le `push rbx ; push rdi ; sub rsp, 0x68` qui
    #    precede le lea de moins de 0x100 octets.
    tete = g.rfind(b'\x53\x57\x48\x83\xec\x68', 0, va_lea - va)
    if tete < 0 or (va_lea - va) - tete > 0x100:
        raise AssertionError('entree du lanceur introuvable avant le lea')
    va_lanceur = va + tete

    # 3. ses appelants, dans la greffe
    appels = []
    for i in range(n - 5):
        if g[i] != 0xE8:
            continue
        if va + i + 5 + struct.unpack_from('<i', g, i + 1)[0] == va_lanceur:
            appels.append(va + i)
    if len(appels) != 2:
        raise AssertionError('appels du lanceur : %d trouve(s), 2 attendus'
                             % len(appels))

    # 4. le compte de lignes du Movie Theater
    motif = bytes.fromhex('c78324020000') + struct.pack('<I', 0xD)
    comptes = []
    d = g.find(motif)
    while d >= 0:
        comptes.append(va + d)
        d = g.find(motif, d + 1)
    if len(comptes) != 1:
        raise AssertionError('compte de lignes : %d trouve(s), 1 attendu'
                             % len(comptes))

    # 5. les maillons de la chaine de libelles : 81 F9 <id> 75 08 48 8D 05 ..
    maillons = {}
    for i in range(n - 16):
        if g[i:i + 2] != b'\x81\xf9' or g[i + 6:i + 8] != b'\x75\x08':
            continue
        if g[i + 8:i + 11] != b'\x48\x8d\x05' or g[i + 15] != 0xC3:
            continue
        maillons[struct.unpack_from('<I', g, i + 2)[0]] = va + i
    manquants = [TVF_ID0 + k for k in range(len(TVF_FILMS))
                 if TVF_ID0 + k not in maillons]
    if manquants:
        raise AssertionError('maillons de libelle absents : %s'
                             % ', '.join('0x%X' % m for m in manquants))

    # 6. la SECONDE constante 13 : `mov ecx,eax ; mov eax,0xD ; sub eax,ecx
    #    ; cmp eax,7`. On vise le `mov eax, 0xD`, dont l immediat est en +2.
    motif13 = bytes.fromhex('89c1b80d00000029c883f807')
    treizes = []
    e = g.find(motif13)
    while e >= 0:
        treizes.append(va + e + 3)   # 89 c1 | b8 | 0d 00 00 00 : l immediat est en +3
        e = g.find(motif13, e + 1)
    if len(treizes) != 1:
        raise AssertionError('seconde constante 13 : %d trouvee(s), 1 attendue'
                             % len(treizes))

    # 7. LE DRAPEAU " on est dans le Movie Theater ". Il appartient au socle
    #    et bouge : on le retrouve par la signature de son lecteur, le relais
    #    qui calcule l identifiant du libelle --
    #    `cmp dword [rip+x],0 ; je +7 ; lea ecx,[rdi+0x2A0] ; ret`.
    drapeaux = []
    for i in range(n - 13):
        if g[i:i + 2] != b'\x83\x3d' or g[i + 6] != 0x00:
            continue
        if g[i + 7:i + 9] != b'\x74\x07':
            continue
        if g[i + 9:i + 15] != b'\x8d\x8f\xa0\x02\x00\x00':
            continue
        drapeaux.append(va + i + 7 + struct.unpack_from('<i', g, i + 2)[0])
    if len(drapeaux) != 1:
        raise AssertionError('drapeau du Movie Theater : %d trouve(s), 1 '
                             'attendu' % len(drapeaux))

    return dict(drapeau=drapeaux[0], lea=va_lea, lanceur=va_lanceur,
                appels=appels,
                compte=comptes[0], treize=treizes[0], maillons=maillons,
                va_greffe=va, off_greffe=off)


# ---------------------------------------------------------------------------
# `--eau-refraction` -- RENDRE SON ANIMATION A LA SURFACE D EAU D EILEEN
#
# L animation de la surface est un DEPLACEMENT DE SOMMETS, et le seul
# programme qui la fait est `water_ring.000.vp` :
#
#     TEX displace, a_tex0, texture[14], 2D
#
# identique dans les quatre builds. Celui de `water01` ne deforme rien.
#
# L unite 14 n est liee qu en `0x18010B2E9` (passe 7), et seulement si la
# passe 3, la refraction, est permise. Elle est allumee a l activation du
# decor, `0x18018FA92` :
#
#     rbx = [[tacheDecor+0x68] + 0xC8]
#     si rbx == 0 -> on saute tout
#     0x18010CA20(3, 1) ; 0x18010CA60([rbx]) ; 0x18010C9F1(1)
#
# MESURE : `+0xC8` est NUL pour les 41 decors de Final Showdown, alors que son
# jumeau `+0xC0`, le bloc de reflet, est renseigne pour douze d entre eux --
# `STGSLK` pointe sur `0x1804033E0` = {0, 1, 1}. Chez Lindbergh ver.B le bloc
# de refraction de `slk` valait {1, 0, 0} : la cible 1, 512 x 256. Et la table
# `0x1803A50E0` d APM3 donne, pour la refraction, la ligne [1, 1, 1] : la
# cible 1 quel que soit le premier mot. Le bloc de reflet convient donc tel
# quel, et il n y a aucune memoire a allouer.
#
# Deuxieme piece : `TaskEffectWaterRing::init` ETEINT la refraction juste
# apres --
#
#     0x18008564C  xor ecx, ecx
#     0x18008564E  call 0x18010C9F0        ; SetRefractEnable(0)
#
# sept octets, remplaces par des `nop`.
#
# Troisieme : la table des descripteurs est DEPLACEE dans la greffe par le
# socle. On relit donc son adresse dans la DLL PRODUITE, au `lea` de
# `0x18018EF78`, jamais une adresse notee.
EAU_INIT = [
    # 1. TaskEffectWaterRing::init eteint la refraction juste apres que
    #    le chargeur l a permise : sept nop.
    (0x18008564C, bytes.fromhex('33c9e89d730800'), b'\x90' * 7),
    # 2. Le bloc de refraction du decor, charge en RIP-RELATIF.
    #    L instruction d origine, mov rbx a partir de rax plus 0xC8, fait
    #    sept octets ; un lea rbx RIP-relatif aussi. Ecrire le pointeur
    #    DANS la table demanderait une relocation -- le socle reecrit la
    #    table entiere et la notre n y serait pas : le jeu plante alors a
    #    0x18018FAB8 en lisant une adresse non rebasee (essai du
    #    2026-10-15, ACCESS_VIOLATION mesuree).
    #    On vise 0x1804033E0, le bloc 0, 1, 1 du reflet de slk : la ligne
    #    refraction de 0x1803A50E0 vaut 1, 1, 1, donc la cible 1
    #    (512 x 256) quel que soit le premier mot du bloc.
    #    C est GLOBAL : le site sert a l activation de n importe quel
    #    decor. Le garde-fou du budget VRAM (20,0 Mo) reste en place.
    (0x18018FA92, bytes.fromhex('488b98c8000000'),
     bytes.fromhex('488d1d') + struct.pack('<i', 2570567)),
]
EAU_DECOR = 72                    # `skb`, la variante VF5 du decor d Eileen
EAU_BLOC = 0x1804033E0            # le bloc {0, 1, 1} du reflet de `slk`
EAU_DESC_LEA = 0x18018EF78        # `lea rax, [rip+x]` -> table des descripteurs
EAU_DESC_PAS = 0xF0
EAU_DESC_C8 = 0xC8


def _eau_refraction(chemin):
    """Pointe `descripteur[72] + 0xC8` sur un bloc de refraction.

    Rend (vrai, message) ou (faux, raison). On relit la table dans la DLL
    PRODUITE : le socle l a deplacee dans la greffe.
    """
    import pefile
    pe = pefile.PE(chemin, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    rel, = struct.unpack('<i', pe.get_data(EAU_DESC_LEA + 3 - base, 4))
    table = EAU_DESC_LEA + 7 + rel
    cible = table + EAU_DECOR * EAU_DESC_PAS + EAU_DESC_C8
    try:
        avant, = struct.unpack('<Q', pe.get_data(cible - base, 8))
        off = pe.get_offset_from_rva(cible - base)
    except Exception as e:
        pe.close()
        return False, 'descripteur %d illisible a 0x%X (%s)' % (
            EAU_DECOR, cible, e)
    pe.close()
    if avant == EAU_BLOC:
        return True, 'deja pose'
    if avant != 0:
        return False, ('0x%X porte deja 0x%X au lieu de 0 -- on ne l ecrase '
                       'pas' % (cible, avant))
    with open(chemin, 'r+b') as fp:
        fp.seek(off)
        fp.write(struct.pack('<Q', EAU_BLOC))
    return True, ('table en 0x%X, descripteur %d, +0xC8 = 0x%X'
                  % (table, EAU_DECOR, EAU_BLOC))


def _poser_points(chemin, origine, points):
    """Pose une liste (va, octets attendus, octets neufs), en verifiant."""
    for va, tete, neuf in points:
        o = _s.offset(origine, va)
        with open(origine, 'rb') as fp:
            fp.seek(o)
            vu = fp.read(len(tete))
        if vu != tete:
            print('REFUS : 0x%X porte %s au lieu de %s.'
                  % (va, vu.hex(), tete.hex()))
            return False
        with open(chemin, 'r+b') as fp:
            fp.seek(o)
            fp.write(neuf)
    return True


def main(argv):
    """Le socle d abord, nos chantiers ensuite."""
    chemin = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', _s.DLL)
    origine = chemin + '.origine'
    demandes = [a for a in argv if a in NOUVELLES]
    # LE SOCLE LIT `sys.argv` LUI-MEME : on le lui prepare, sans les options
    # qu il ne connait pas, puis on le rend tel qu on l a trouve.
    pour_socle = [a for a in argv if a not in NOUVELLES]
    # LES CAVERNES DE `--sp-lancer` VIVENT DANS LE CAS « How to Play » du
    # repartiteur des options, et il faut qu il soit MORT. Le socle ne connait
    # qu une facon de le tuer, `--options-sans-howto` ; `--options-v2` en est
    # une autre -- sous la refonte, les cas 0, 1, 3, 4 et 5 sont tous
    # inatteignables. L original relachait la garde ; ici on la satisfait, et
    # la refonte repose ensuite CHACUN des octets concernes (la borne du menu,
    # son `cmove`, son cadre et ses quatre libelles).
    if ('--options-v2' in demandes
            and ('--sp-lancer' in argv or '--sp-sparring' in argv)
            and '--options-sans-howto' not in pour_socle):
        pour_socle.append('--options-sans-howto')
    def _socle(taille):
        """Un tour de socle, a la taille de greffe demandee."""
        _s.GREFFE_TAILLE = taille
        garde = sys.argv
        sys.argv = [garde[0]] + pour_socle
        try:
            return _s.main()
        finally:
            sys.argv = garde

    # LA TAILLE DE LA GREFFE N EST PLUS DEVINEE. Le socle agrandit SA section
    # tout seul selon les options -- 0x4D40 sans les decors, 0x6E40 avec le lot
    # complet -- et REFUSE quand une de ses zones n y tient plus (« la greffe
    # est pleine (YUKA : 0x6EB0 > 0x6E40) »). On ne peut donc ni lui imposer
    # une taille fixe, ni lire son besoin apres coup. On lui en donne une
    # LARGE, et on pose notre bloc A LA FIN -- la ou ses zones, qui se rangent
    # depuis le debut, n arriveront pas. Si un jour elles y arrivent, le
    # controle « bloc vierge » refuse, bruyamment.
    taille = CPL_GREFFE_TOTALE
    for _ in range(4):
        r = _socle(taille)
        if r == 0:
            break
        taille *= 2
    if r:
        return r
    if not demandes:
        return 0
    vu = _taille_greffe(chemin)
    if vu is None:
        print('REFUS : le socle n a pose aucune section .greffe.')
        return 2
    _placer_zones(vu - CPL_COMPLEMENT)

    if '--menu-griser' in demandes and '--menu-v2' not in argv:
        print('REFUS : --menu-griser designe les entrees PAR LEUR RANG, et '
              'ces rangs sont ceux de --menu-v2.')
        return 2

    g = _greffe_posee(chemin)
    if g is None and ('--versus-joueur2' in demandes
                      or '--options-v2' in demandes
                      or '--terminal-ordre' in demandes
                      or '--versus-manette' in demandes
                      or '--options-dural' in demandes):
        print('REFUS : pas de section .greffe dans la DLL patchee -- le socle '
              'ne l a pas posee, et nos zones n ont nulle part ou aller.')
        return 2

    # NOTRE BLOC DOIT ETRE VIERGE. C est le controle qui manquait le
    # 2026-10-13 : sans lui, nos zones ont ecrase les tables du socle et le
    # jeu ne demarrait plus, sans un mot du patcheur.
    if g is not None:
        _, off_g0 = g
        with open(chemin, 'rb') as fp:
            fp.seek(off_g0 + CPL_BASE)
            bloc = fp.read(CPL_COMPLEMENT)
        if len(bloc) != CPL_COMPLEMENT or any(bloc):
            print('REFUS : la place de nos zones (greffe + 0x%X, 0x%X '
                  'octets) n est pas vierge -- %d octets lus, %d non nuls. '
                  'Le socle y a ecrit quelque chose, et nous l ecraserions.'
                  % (CPL_BASE, CPL_COMPLEMENT, len(bloc),
                     sum(1 for b in bloc if b)))
            return 2

    faits = []
    if '--quest-degriser' in demandes and '--menu-griser' not in demandes:
        print('REFUS : --quest-degriser change l immediat que --menu-griser '
              'pose en 0x1801E3A0A. Sans --menu-griser il n y a rien a '
              'degriser.')
        return 2

    if '--menu-griser' in demandes:
        if not _poser_points(chemin, origine, _menu_griser(demandes)):
            return 2
        if '--quest-degriser' in demandes:
            faits.append('menu principal : ONLINE VERSUS et SCOREBOARDS sont '
                         'GRISEES et le curseur les saute, mais QUEST MODE '
                         'NON -- l immediat de 0x1801E3A0A est passe de '
                         '0x0101 a 0x0001, donc [page+0x645] reste a 0')
        else:
            faits.append('menu principal : ONLINE VERSUS, QUEST MODE et '
                         'SCOREBOARDS sont GRISEES, et le curseur les saute')

    if '--versus-joueur2' in demandes:
        if not _poser_points(chemin, origine, VERSUS_JOUEUR2):
            return 2
        va_g, off_g = g
        va_vs = va_g + CPL_VS
        site, tete = VS2_SITE
        if not _poser_points(chemin, origine, [(
                site, tete,
                bytes.fromhex('e8') + struct.pack('<i', va_vs - (site + 5)))]):
            return 2
        with open(chemin, 'r+b') as fp:
            fp.seek(off_g + CPL_VS)
            fp.write(vs2_relais(va_vs))
        faits.append('OFFLINE VERSUS : le joueur 2 entre sans credit, menu ET '
                     'ecran de selection (relais 0x%X)' % va_vs)

    if '--nom-donnees' in demandes:
        if g is None:
            print('REFUS : --nom-donnees a besoin de la section .greffe.')
            return 2
        va_g, off_g = g
        va_n = va_g + CPL_NOM
        points = []
        for site, tete, dec in NOM_SITES:
            points.append((site, tete, bytes.fromhex('e8')
                           + struct.pack('<i', va_n + dec - (site + 5))))
        if not _poser_points(chemin, origine, points):
            return 2
        with open(chemin, 'r+b') as fp:
            fp.seek(off_g + CPL_NOM)
            fp.write(NOM_MAGIE)
            fp.seek(off_g + CPL_NOM + NOM_O_OUVRIR)
            fp.write(nom_ouvrir(va_n + NOM_O_OUVRIR, va_n))
            fp.seek(off_g + CPL_NOM + NOM_O_FINI)
            fp.write(nom_fini(va_n + NOM_O_FINI, va_n))
            fp.seek(off_g + CPL_NOM + NOM_O_TEXTE)
            fp.write(nom_texte(va_n + NOM_O_TEXTE, va_n))
            fp.seek(off_g + CPL_NOM + NOM_O_DESSIN_RELAIS)
            fp.write(nom_relais_dessin(va_n + NOM_O_DESSIN_RELAIS, va_n))
        # LE CRENEAU 4 DE LA VTABLE. Elle est en `.rdata`, donc RELOGEE : y
        # ecrire une adresse de fichier est correct, le chargeur lui applique
        # le meme delta qu aux autres creneaux.
        if not _poser_points(chemin, origine, [(
                NOM_VT_DESSIN, struct.pack('<Q', NOM_DESSIN_ORIG),
                struct.pack('<Q', va_n + NOM_O_DESSIN_RELAIS))]):
            return 2
        faits.append('CUSTOMIZE MENU : « Edit data name » ouvre une saisie de '
                     'VINGT caracteres au clavier, tenue par apm.dll dans la '
                     'zone VF5NAME (0x%X). Les trois sites de la ligne sont '
                     'relayes -- jamais les fonctions, qui sont partagees '
                     '(0x180029FB0 : 73 appelants, 0x180007430 : 601). Sans '
                     'stub, la ligne ne fait plus RIEN au lieu d effacer le '
                     'nom.' % va_n)

    if '--sans-ecran-epilepsie' in demandes:
        if not _poser_points(chemin, origine, EPILEPSIE):
            return 2
        faits.append('demarrage : la presentation s arrete sur le marqueur '
                     'CRI_e au lieu de INFO_end -- l ecran d avertissement sur '
                     'l epilepsie (segment INFO_st..INFO_end de aet_n_adv, 320 '
                     'trames) ne se joue plus. Le mode BORNE n est pas touche : '
                     'il finissait deja sur SEGA_e.')

    if '--eau-refraction' in demandes:
        if not _poser_points(chemin, origine, EAU_INIT):
            return 2
        faits.append('eau : le bloc de refraction du decor est charge en '
                     'RIP-RELATIF (0x18018FA92, lea au lieu du mov), et '
                     'TaskEffectWaterRing::init ne l eteint plus (0x18008564C, '
                     'sept nop). La passe 3 est alors permise, l unite 14 est '
                     'liee en 0x18010B2E9, et le programme de sommets de '
                     'water_ring deplace les sommets -- son `mad` ajoute la '
                     'valeur echantillonnee a la position, le long de la '
                     'normale (verifie au desassembleur du DXBC d APM3).')

    if '--versus-manette' in demandes:
        if '--menu-v2' not in argv or '--menu-griser' not in argv:
            print('REFUS : --versus-manette designe OFFLINE VERSUS PAR SON '
                  'RANG (entree 1, ordre de --menu-v2) et compte sur le saut '
                  'de curseur que --menu-griser pose en 0x1801E4CD8.')
            return 2
        va_g, off_g = g
        va_man = va_g + CPL_MAN
        # Plus de drapeau : --terminal-ordre ne quitte plus le mode MENU,
        # donc la page n a jamais a etre gelee derriere un autre ecran.
        va_drapeau = None
        site, tete = MAN_SITE
        if not _poser_points(chemin, origine, [(
                site, tete,
                bytes.fromhex('e9')
                + struct.pack('<i', va_man - (site + 5)))]):
            return 2
        with open(chemin, 'r+b') as fp:
            fp.seek(off_g + CPL_MAN)
            fp.write(man_relais(va_man, va_drapeau))
        faits.append('menu principal : OFFLINE VERSUS EST GRISE TANT QU AUCUNE '
                     'MANETTE NE TIENT LE JOUEUR 2, et rendu des qu il y en a '
                     'une -- a chaud, sans relance. Le relais 0x%X est pose sur '
                     'la mise a jour de la page (0x1801DC620, qui n a ni autre '
                     'pointeur ni appelant) et interroge le creneau 45 de '
                     'l objet d entrees, `Input_isGamepadDetect` : '
                     'l interface existait, personne ne l appelait, et le stub '
                     'y repondait 0 comme un bouchon. Si la ligne grise pendant '
                     'qu on est dessus, le curseur revient sur SINGLE PLAYER.'
                     % va_man)

    if '--terminal-ordre' in demandes:
        va_g, off_g = g
        va_a = va_g + CPL_TRM + _TRM_A
        va_val = va_g + CPL_TRM + _TRM_VAL
        va_dess = va_g + CPL_TRM + _TRM_DESS
        va_vt = va_g + CPL_TRM + _TRM_VT
        va_d = va_g + CPL_TRM + _TRM_D
        va_drap = va_g + CPL_TRM + _TRM_DRAP
        va_obj = va_g + CPL_TRM + _TRM_OBJ

        # LA VTABLE D ORIGINE, RELUE DANS LE `.origine` : le pointeur RTTI qui
        # la precede, puis ses dix-neuf creneaux.
        with open(chemin, 'rb') as fp:
            fp.seek(_s.offset(origine, TRM_VT - 8))
            vt0 = fp.read(8 * (TRM_VT_CRENEAUX + 1))
        # On ne la COPIE pas ici -- la greffe n a pas de relocations, et
        # c est le relais qui la copiera a l execution. On controle
        # seulement qu elle est bien ce qu on croit.
        for k in range(TRM_VT_CRENEAUX):
            cible = struct.unpack_from('<Q', vt0, 8 + 8 * k)[0]
            if not 0x180000000 <= cible < 0x181000000:
                print('REFUS : le creneau %d de la vtable 0x%X vaut 0x%X -- ce '
                      'n est pas une fonction du moteur.' % (k, TRM_VT, cible))
                return 2

        with open(chemin, 'r+b') as fp:
            fp.seek(off_g + CPL_TRM + _TRM_A)
            fp.write(trm_relais(va_a, va_obj, va_drap, va_vt,
                                va_dess, va_val))
            fp.seek(off_g + CPL_TRM + _TRM_VAL)
            fp.write(trm_validateur(va_val))
            fp.seek(off_g + CPL_TRM + _TRM_DESS)
            fp.write(trm_dessin(va_dess))
            fp.seek(off_g + CPL_TRM + _TRM_D)
            fp.write(trm_fermer_relais(va_d, va_obj))

        # LE CUSTOMIZE MENU : site intact, verifie sur le `.origine`.
        va_cust = va_g + CPL_TRM + _TRM_CUST
        va_sauve = va_g + CPL_TRM + _TRM_SAUVE
        va_deja = va_g + CPL_TRM + _TRM_DEJA
        va_seq = va_g + CPL_TRM + _TRM_SEQ
        va_sort = va_g + CPL_TRM + _TRM_SORT
        with open(chemin, 'r+b') as fp:
            fp.seek(off_g + CPL_TRM + _TRM_CUST)
            fp.write(trm_cust_relais(va_cust, va_obj, va_sauve, va_deja))
        site_c, tete_c = TRM_CUST_SITE
        if not _poser_points(chemin, origine, [(
                site_c, tete_c,
                bytes.fromhex('e9')
                + struct.pack('<i', va_cust - (site_c + 5))
                + bytes.fromhex('90') * (len(tete_c) - 5))]):
            return 2

        # LE SEQUENCEUR DU MODE 5 : site intact.
        with open(chemin, 'r+b') as fp:
            fp.seek(off_g + CPL_TRM + _TRM_SEQ)
            fp.write(trm_seq_relais(va_seq, va_deja))
        site_q, tete_q = TRM_SEQ_SITE
        if not _poser_points(chemin, origine, [(
                site_q, tete_q,
                bytes.fromhex('e9')
                + struct.pack('<i', va_seq - (site_q + 5))
                + bytes.fromhex('90') * (len(tete_q) - 5))]):
            return 2

        # LA SORTIE DU MODE : site intact.
        with open(chemin, 'r+b') as fp:
            fp.seek(off_g + CPL_TRM + _TRM_SORT)
            fp.write(trm_boucle_relais(va_sort, va_deja))
        site_x, tete_x = TRM_BCL_SITE
        if not _poser_points(chemin, origine, [(
                site_x, tete_x,
                bytes.fromhex('e9')
                + struct.pack('<i', va_sort - (site_x + 5))
                + bytes.fromhex('90') * (len(tete_x) - 5))]):
            return 2

        # LA REOUVERTURE DU SELECTEUR : site intact lui aussi.
        va_rouv = va_g + CPL_TRM + _TRM_ROUV
        with open(chemin, 'r+b') as fp:
            fp.seek(off_g + CPL_TRM + _TRM_ROUV)
            fp.write(trm_rouvrir_relais(va_rouv, va_obj))
        site_r, tete_r = TRM_ROUV_SITE
        if not _poser_points(chemin, origine, [(
                site_r, tete_r,
                bytes.fromhex('e9')
                + struct.pack('<i', va_rouv - (site_r + 5))
                + bytes.fromhex('90') * (len(tete_r) - 5))]):
            return 2

        # LE SITE DE FERMETURE se verifie sur le `.origine` : intact.
        site_f, tete_f = TRM_FERMER
        if not _poser_points(chemin, origine, [(
                site_f, tete_f,
                bytes.fromhex('e9')
                + struct.pack('<i', va_d - (site_f + 5))
                + bytes.fromhex('90') * (len(tete_f) - 5))]):
            return 2
        # L ENTREE DU MENU se verifie sur la DLL PATCHEE : c est le saut du
        # socle qu on remplace, et on controle que c est bien lui.
        o_t = _s.offset(origine, TRM_SITE)
        with open(chemin, 'r+b') as fp:
            fp.seek(o_t)
            vu = fp.read(TRM_SITE_LONG)
            if vu[0] != 0xE9 or any(b != 0x90 for b in vu[5:]):
                print('REFUS : 0x%X porte %s, pas le saut vers la greffe que '
                      '--menu-v2 y pose. --terminal-ordre suppose --menu-v2.'
                      % (TRM_SITE, vu.hex()))
                return 2
            fp.seek(o_t)
            fp.write(bytes.fromhex('e9')
                     + struct.pack('<i', va_a - (TRM_SITE + 5))
                     + bytes.fromhex('90') * (TRM_SITE_LONG - 5))
        faits.append('VF.TERMINAL A SON PROPRE SOUS-MENU ET SA PROPRE VTABLE : '
                     'PLUS AUCUN LIEN AVEC VF.TV. L objet [page+0x2328] n est '
                     'plus un sous-menu TERMINAL dans cette build -- --menu-v2 '
                     'en a fait LA PAGE DE VF.TV -- et c est pour cela que '
                     'VF.TERMINAL lancait les videos de Movie Theater. Notre '
                     'instance vit dans la greffe (0x%X, 0x600 octets : la page '
                     'range ses sous-menus a 0x2328 puis 0x2928) et se construit '
                     'UNE SEULE FOIS, comme le fait le constructeur de la page '
                     'en 0x1801DA7CB -- `call 0x1801BB750` puis la vtable, et la '
                     'meme chose a +0x300 pour le REPLAY MENU. Sa VTABLE est une '
                     'COPIE (0x%X) ou deux creneaux seulement changent : le 4, '
                     'le dessin, rendu muet parce que les planches du panneau '
                     'sont celles de VF.TV (0x299, 0x29A, titre 0x17C) ; et le '
                     '10, le validateur, qui ouvre le CARD SELECTOR sur la ligne '
                     '0 et referme le sous-menu sur toute autre action. '
                     '0x1801E1B10 et 0x1801DE369 sont RENDUS AU SOCLE, intacts. '
                     'Il ne reste que DEUX sites : l entree 5 du menu '
                     '(0x1801DE056, verifiee sur la DLL patchee) et la fermeture '
                     'de la sous-page (0x1801DD898, verifiee sur le .origine), '
                     'ou l on pose [objet+0x2F0] = 1 pour revenir au menu '
                     'principal. LA SUITE EXISTAIT DEJA : 0x1801DD8A8 inscrit '
                     '« CUSTOMIZE MENU » des que la sous-page rend 2, et '
                     '0x1801C5119 demande le mode 5 et le sous-etat 0x25.'
                     % (va_obj, va_vt + 8))

    if '--film-cadres' in demandes:
        va_g, off_g = g
        with open(chemin, 'rb') as fp:
            fp.seek(_s.offset(origine, FLM_SITE))
            vu_s = fp.read(5)
            fp.seek(_s.offset(origine, FLM_GARDE))
            vu_g = fp.read(5)
        if vu_s[0] != 0xE9 or vu_g[0] != 0xE9:
            print('REFUS : 0x%X porte %s et 0x%X porte %s -- --film-cadres '
                  'suppose les deux detours de --menu-v2.'
                  % (FLM_SITE, vu_s.hex(), FLM_GARDE, vu_g.hex()))
            return 2
        socle = FLM_SITE + 5 + struct.unpack('<i', vu_s[1:5])[0]
        garde = FLM_GARDE + 5 + struct.unpack('<i', vu_g[1:5])[0]
        # La garde du socle commence par `cmp dword [rip+d32], 0` : le drapeau.
        # Elle vit dans la GREFFE : `_s.offset()` ne sait pas l y trouver, la
        # table des sections du `.origine` ne la connait pas. On passe par la
        # section rendue par `_greffe_posee()`.
        with open(chemin, 'rb') as fp:
            fp.seek(off_g + (garde - va_g))
            tete = fp.read(7)
        if tete[0:2] != bytes.fromhex('833d') or tete[6] != 0x00:
            print('REFUS : la garde 0x%X commence par %s, pas par le '
                  '`cmp dword [rip], 0` qui porte le drapeau du film.'
                  % (garde, tete.hex()))
            return 2
        film = garde + 7 + struct.unpack('<i', tete[2:6])[0]
        va_r = va_g + CPL_FLM + _FLM_RELAIS
        va_c = va_g + CPL_FLM + _FLM_CORPS
        va_d = va_g + CPL_FLM + _FLM_DON
        va_i = va_g + CPL_TRM + _TRM_OBJ
        with open(chemin, 'r+b') as fp:
            fp.seek(off_g + CPL_FLM + _FLM_RELAIS)
            fp.write(flm_relais(va_r, va_c, socle))
            fp.seek(off_g + CPL_FLM + _FLM_CORPS)
            fp.write(flm_corps(va_c, va_d, film, va_i))
            fp.seek(_s.offset(origine, FLM_SITE))
            fp.write(bytes.fromhex('e9')
                     + struct.pack('<i', va_r - (FLM_SITE + 5)))
        faits.append('LE FILM DU MOVIE THEATER EST DE NOUVEAU PLEIN ECRAN, '
                     'CADRES COMPRIS. Ce chantier du 2026-10-08 (journal 158) '
                     'vivait dans le patcheur compile du 12 et avait disparu au '
                     'passage au socle du 8 -- le diff des deux DLL le montre : '
                     'le relais du 12 sur 0x1801DD7A0 commence par un '
                     '`call <plein ecran>` que la notre n avait plus. Les '
                     'cadres sont des objets AET que le moteur redessine seul : '
                     'il faut les FERMER (0x1801BBA20, deux appels d affilee : '
                     'etat 3 -> 4 puis liberation), et il y en a QUATRE -- deux '
                     'a la page du sous-menu (+0x240, +0x298) et deux au MENU '
                     'PRINCIPAL qui vit derriere (-0x20E8, -0x2090, soit la '
                     'page moins 0x2328). Le RANG de chaque fenetre est RELEVE '
                     'avant la fermeture et rendu a la reouverture : une '
                     'constante aurait rendu un Movie Theater a deux lignes. Et '
                     'hors film, le relais donne leur tic aux deux fenetres du '
                     'menu principal tant qu elles ne sont pas a l etat 3 -- la '
                     'mise a jour de cette page (0x1801DC620) n a aucun appel a '
                     '0x1801BBB10, c est la coupe du build arcade. Le drapeau '
                     '« un film joue » (0x%X) n est pas code en dur : il est '
                     'RELU dans la garde que le socle pose sur 0x1801E0C80.'
                     % film)

    if '--options-dural' in demandes:
        if '--dural-grille' not in argv or '--wxga' not in argv:
            print('REFUS : --options-dural a besoin de --dural-grille et '
                  '--wxga. Le reglage ne commande QUE le predicat de la case.')
            return 2
        va_g, off_g = g
        va_dur = va_g + CPL_DUR
        zone_d, va_p, va_m = dural_zone(va_dur)
        with open(chemin, 'r+b') as fp:
            fp.seek(off_g + CPL_DUR)
            fp.write(zone_d)
        pts = []
        for site in DUR_SITES:
            o = _s.offset(origine, site)
            with open(origine, 'rb') as fp:
                fp.seek(o)
                tete = fp.read(5)
            if (tete[0] != 0xE8 or site + 5
                    + struct.unpack('<i', tete[1:5])[0] != DUR_BOUCHON):
                print('REFUS : 0x%X ne porte pas le `call 0x%X` attendu (%s).'
                      % (site, DUR_BOUCHON, tete.hex()))
                return 2
            pts.append((site, tete, bytes.fromhex('e8')
                        + struct.pack('<i', va_p - (site + 5))))
        pts.append((DUR_MOUCHARD[0], DUR_MOUCHARD[1],
                    bytes.fromhex('e9')
                    + struct.pack('<i', va_m - (DUR_MOUCHARD[0] + 5))
                    + bytes.fromhex('90')
                    * (len(DUR_MOUCHARD[1]) - 5)))
        if not _poser_points(chemin, origine, pts):
            return 2
        faits.append('DURAL : la case suit les trois bascules, par le '
                     'predicat 0x%X aux TROIS sites, et le mouchard 0x%X qui '
                     'note l entree de menu validee' % (va_p, va_m))

    if '--menu-v2' in argv and g is not None:
        # « VF.TERMINAL », ET NON « CUSTOMIZE » -- demande de Frederic du
        # 2026-10-10, donc POSTERIEURE au socle, qui porte encore l ancien
        # mot. Le texte vit dans la zone MNU de la greffe, au pas de 0x20 ;
        # onze caracteres tiennent dans cette place, rien a deplacer. Le
        # marqueur (0x17C) ne bouge pas : il rend toujours « VF.TV » dans le
        # sous-menu, chaque relais ne vivant que sur son dessin.
        va_g, off_g = g
        for i, (_id, t) in enumerate(MENU2_TEXTES):
            if t != 'CUSTOMIZE':
                continue
            neuf = b'VF.TERMINAL\x00'
            if len(neuf) > MENU2_TXT_PAS:
                break
            with open(chemin, 'r+b') as fp:
                fp.seek(off_g + GRE_MNU + MENU2_TXT + MENU2_TXT_PAS * i)
                fp.write(neuf)
            faits.append('menu principal : la cinquieme ligne est '
                         '« VF.TERMINAL »')
            break

    if '--options-v2' in demandes and '--options-sans-howto' in pour_socle:
        # ON REND AU REPARTITEUR CE QUE `--options-sans-howto` LUI A PRIS.
        #
        # On ne l a demande au socle que pour satisfaire la garde de
        # `--sp-lancer` ; ses DIX sites ont ete releves en comparant deux
        # DLL, et la refonte n en repose qu UN (la borne du menu, 0x1801AB03F).
        # Les neuf autres gêneraient :
        #   . 0x1801A703B rend le `jne` du repartiteur inconditionnel ;
        #   . 0x1801A7080/70D2/7118/715E PERMUTENT ses cas -- or la refonte
        #     force `eax = 2`, le cas OPTION SETTING, et compte dessus ;
        #   . 0x1801A9E06/0E/16/1E changent les identifiants des libelles --
        #     or 0x2F1 a 0x2F4 sont precisement les MARQUEURS que le relais
        #     des quatre titres reconnait.
        rendre = [(0x1801A703B, 1), (0x1801A7080, 1), (0x1801A70D2, 1),
                  (0x1801A7118, 1), (0x1801A715E, 1), (0x1801A9E06, 1),
                  (0x1801A9E0E, 1), (0x1801A9E16, 1), (0x1801A9E1E, 1)]
        with open(origine, 'rb') as fo, open(chemin, 'r+b') as fc:
            for va, n in rendre:
                o = _s.offset(origine, va)
                fo.seek(o)
                fc.seek(o)
                fc.write(fo.read(n))

    if '--options-v2' in demandes:
        # LA REFONTE DES MENUS D OPTIONS (journal 182 a 184). Tout le
        # generateur est dans `tools/options_v2.py`, qui n a pas ete touche :
        # ici on ne fait que lui donner les ECARTS vers les zones voisines et
        # poser ce qu il rend.
        manque = [o for o in ('--options-resolution', '--options-mode',
                              '--options-dural') if o not in argv]
        if manque:
            print('REFUS : --options-v2 a besoin de %s.' % ', '.join(manque))
            return 2
        if '--options-sans-howto' in argv:
            print('REFUS : --options-v2 et --options-sans-howto se disputent '
                  'les memes octets.')
            return 2
        va_g, off_g = g
        va_v2 = va_g + CPL_V2

        def _ec(cible):
            return cible - CPL_V2

        ecarts = {'res': _ec(GRE_RES + RES_VAL),
                  'mod': _ec(GRE_MOD + MOD_VAL),
                  'btn': ov2.V2_BTN}
        textes = {'res': _ec(GRE_RES + RES_TXT + RES_TXT_PAS),
                  'mod': _ec(GRE_MOD + MOD_TXT + RES_TXT_PAS),
                  'btn': ov2.V2_BTN_TXT}
        confs = {'res': _ec(GRE_RES + RES_CONF),
                 'mod': _ec(GRE_MOD + MOD_CONF),
                 'btn': ov2.V2_BTN_CONF}
        for i in range(3):
            ecarts['dur%d' % i] = _ec(CPL_DUR + DUR_VAL + 4 * i)
            textes['dur%d' % i] = _ec(CPL_DUR + DUR_TXT + 4 * DUR_TXT_PAS)
        style = 0
        f_btn = os.path.join(RACINE, 'runtime', 'media', 'vf5fs', 'ram',
                             'boutons.txt')
        if os.path.exists(f_btn):
            with open(f_btn) as fp:
                clef = fp.read().strip().lower()
            if clef in ov2.BTN_CLEFS:
                style = ov2.BTN_CLEFS.index(clef)
        zone_v, pos_v = ov2.zone(va_v2, ecarts, textes,
                                 _ec(GRE_RES + RES_MAXI), confs, style,
                                 ov2.dispo(RACINE))
        if len(zone_v) > CPL_V2_TAILLE:
            print('REFUS : la zone V2 deborde (%d octets).' % len(zone_v))
            return 2
        pts = []
        for (va_s, tete), clef in (
                (ov2.PARENT_LBL_APPEL, 'parent'), (ov2.TITRE_APPEL, 'titre'),
                (ov2.LIBELLE_APPEL, 'libelle'), (ov2.VALEUR_APPEL, 'valeur'),
                (ov2.CADRE_APPEL, 'cadre')):
            pts.append((va_s, tete, bytes.fromhex('e8') + struct.pack(
                '<i', (va_v2 + pos_v[clef]) - (va_s + 5))))
        for (va_s, tete), clef in (
                (ov2.PARENT_AIGUILLAGE, 'aiguillage'),
                (ov2.PAGE_RETOUR, 'retour'), (ov2.VERT_SITE, 'vert'),
                (ov2.HORIZ_SITE, 'horiz'), (ov2.VALIDER_SITE, 'valider'),
                (ov2.FLAGS_SITE, 'init')):
            d_ = bytes.fromhex('e9') + struct.pack(
                '<i', (va_v2 + pos_v[clef]) - (va_s + 5))
            pts.append((va_s, tete, d_ + b'\x90' * (len(tete) - len(d_))))
        for creneau, clef in ((ov2.CRENEAU9, 'annuler'),
                              (ov2.CTL_CRENEAU9, 'annuler_ctl')):
            pts.append((creneau, struct.pack('<Q', 0x180007430),
                        struct.pack('<Q', va_v2 + pos_v[clef])))
        pts.append((ov2.PARENT_BORNE, b'\x04', b'\x03'))
        pts.append((ov2.PARENT_CMOVE, bytes.fromhex('0f44c1'),
                    bytes.fromhex('909090')))
        pts.append((ov2.PARENT_CADRE2, b'\x10', b'\x0f'))
        va_s, tete_g, neuf_g = ov2.PARENT_GRIS_L3
        pts.append((va_s, tete_g, neuf_g))
        for va_s, vieux in ov2.PARENT_GRIS:
            pts.append((va_s, bytes([vieux]), bytes([len(ov2.PARENT) - 1])))
        with open(chemin, 'r+b') as fp:
            fp.seek(off_g + CPL_V2)
            fp.write(zone_v)
        if not _poser_points(chemin, origine, pts):
            return 2
        faits.append('OPTIONS REFONDU EN QUATRE SOUS-MENUS : %s (zone 0x%X). '
                     'Les quatre lignes ouvrent la MEME page, chacune sur sa '
                     'face ; la page de Dural en est la cinquieme.'
                     % (' / '.join(ov2.PARENT), va_v2))

    if '--films-theatre' in demandes:
        # TOUT SE RETROUVE PAR SIGNATURE : le socle deplace ses relais a
        # chaque changement de ses options, et une adresse notee ici serait
        # fausse au prochain tour.
        try:
            r = tvf_reperer(chemin)
        except AssertionError as e:
            print('REFUS : --films-theatre ne reconnait plus le socle (%s).'
                  % e)
            return 2
        # LA GREFFE SE REPREND DE `tvf_reperer`, qui l a deja lue : une seule
        # lecture, une seule verite. Et l offset d une adresse de greffe se
        # CALCULE -- `_s.offset` rouvrirait le fichier, qu on tient deja
        # ouvert en ecriture.
        va_gr, off_gr = r['va_greffe'], r['off_greffe']

        def _o(va_s):
            return off_gr + (va_s - va_gr)

        va_z = va_gr + CPL_TVF
        off_z = _o(va_z)

        # ET UNE GARDE A L ECRITURE, en plus de celle des constantes : on
        # refuse d ecrire un seul octet au-dela de la section. La zone finit
        # EXACTEMENT au bout de la greffe, donc tout debordement tombe dans
        # la section suivante -- c est ce qui a ecrase .decors le 2026-10-15.
        if CPL_TVF + TVF_FIN > CPL_FIN:
            print('REFUS : la zone TVF deborderait de la greffe '
                  '(0x%X > 0x%X).' % (CPL_TVF + TVF_FIN, CPL_FIN))
            return 2

        # 1. NOTRE BLOC : le relais, les chemins, les libelles.
        with open(chemin, 'r+b') as fp:
            fp.seek(off_z + TVF_O_RELAIS)
            fp.write(tvf_relais(va_z + TVF_O_RELAIS, va_z, r['lanceur']))
            fp.seek(off_z + TVF_O_NOMS)
            fp.write(tvf_donnees(va_z))
            # ET LE RELAIS " RESTER SUR LA PAGE ". Sans lui, le site de
            # sortie saute dans du vide : le controle de l entree (233) l a
            # attrape parce qu on relit TOUJOURS la DLL produite.
            fp.seek(off_z + TVF_O_RESTER)
            fp.write(tvf_rester(va_z + TVF_O_RESTER, r['drapeau']))

        # 2. LE LANCEUR RELIT LE CRENEAU au lieu de sa chaine en dur.
        #    `mov rdx, [rip+creneau]` fait SEPT octets, comme le `lea` qu il
        #    remplace : rien ne bouge autour.
        pts_g = [(r['lea'], bytes.fromhex('488d15'),
                  bytes.fromhex('488b15')
                  + struct.pack('<i', (va_z + TVF_O_CRENEAU)
                                - (r['lea'] + 7)))]

        # 3. LES DEUX APPELS passent par notre relais.
        for va_a in r['appels']:
            pts_g.append((va_a, bytes.fromhex('e8'),
                          bytes.fromhex('e8')
                          + struct.pack('<i', (va_z + TVF_O_RELAIS)
                                        - (va_a + 5))))

        # 3bis. LE BRANCHEMENT DE SORTIE. Ce site est dans le code d origine,
        #       donc il se verifie sur le `.origine` -- pas comme ceux de la
        #       greffe.
        if not _poser_points(chemin, origine, [(
                TVF_SORTIE, TVF_SORTIE_TETE,
                bytes.fromhex('e9') + struct.pack(
                    '<i', (va_z + TVF_O_RESTER) - (TVF_SORTIE + 5)))]):
            return 2

        # 4. LE COMPTE DE LIGNES suit la table. Le socle en ecrivait TREIZE
        #    pour quatorze libelles ; on en ecrit autant qu on a de films.
        pts_g.append((r['compte'], bytes.fromhex('c78324020000'),
                      bytes.fromhex('c78324020000')
                      + struct.pack('<I', len(TVF_FILMS))))
        # 4bis. ET IL Y EN A UNE SECONDE. Le socle calcule aussi le nombre de
        #       lignes A DESSINER par " treize moins le defilement, au plus
        #       sept " : `mov ecx,eax ; mov eax,0xD ; sub eax,ecx ; cmp eax,7`.
        #       Avec douze films elle laissait defiler une ligne de trop.
        #        rend DEJA l adresse de l immediat (il ajoute le
        #       +2 lui-meme) : le rajouter ici visait trois octets trop loin,
        #       le controle de tete refusait, et le refus emportait les
        #       libelles qui suivaient dans la liste.
        pts_g.append((r['treize'], bytes.fromhex('0d000000'),
                      struct.pack('<I', len(TVF_FILMS))))

        # 5. LES LIBELLES : chaque maillon pointe vers NOTRE texte. Le
        #    deplacement du `lea rax` est en +0x0B, et sa cible se compte
        #    depuis +0x0F.
        for k in range(len(TVF_FILMS)):
            m = r['maillons'][TVF_ID0 + k]
            cible = va_z + TVF_O_LIBS + TVF_PAS_LIB * k
            pts_g.append((m + 0x0B, b'', struct.pack('<i', cible - (m + 0x0F))))

        # LA GREFFE NE SE VERIFIE PAS SUR LE `.origine` -- elle n y est pas.
        # On relit donc la DLL PRODUITE avant d ecrire, et on refuse si la
        # tete n est pas celle qu on attend.
        with open(chemin, 'r+b') as fp:
            for va_s, tete, neuf in pts_g:
                o = _o(va_s)
                if tete:
                    fp.seek(o)
                    vu = fp.read(len(tete))
                    if vu != tete:
                        print('REFUS : 0x%X porte %s au lieu de %s.'
                              % (va_s, vu.hex(), tete.hex()))
                        return 2
                fp.seek(o)
                fp.write(neuf)

        faits.append('MOVIE THEATER : chaque ligne joue SON film. Le lanceur '
                     'du socle (0x%X) portait " rom/movie/vf5adv.sfd " en dur '
                     'et ses deux appelants (0x%s) ne lui passaient rien : '
                     'toutes les lignes lancaient le meme film. Ils passent '
                     'maintenant par un relais (0x%X) qui lit la ligne dans '
                     '[rbx+0x58] -- elle y est aux DEUX sites -- et depose '
                     'dans un creneau l adresse du chemin, que le lanceur '
                     'relit. %d films, autant de libelles, et le compte de '
                     'lignes suit (le socle en annoncait treize pour quatorze '
                     'libelles). Aucune adresse du socle n est notee : tout '
                     'est retrouve par signature.'
                     % (r['lanceur'], ', 0x'.join('%X' % a for a in r['appels']),
                        va_z + TVF_O_RELAIS, len(TVF_FILMS)))

    for f in faits:
        print('applique : %s' % f)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
