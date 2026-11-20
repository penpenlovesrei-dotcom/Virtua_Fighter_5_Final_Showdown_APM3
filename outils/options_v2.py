#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA REFONTE DES MENUS D OPTIONS -- quatre sous-menus, une seule page.

Demande de Frederic, 2026-10-11 :

    OPTIONS / Controls / Settings        (l ecran de remappage des boutons)
    OPTIONS / Controls / Buttons style   (PS3, PS4, PS5, X360, Xbox One)
    OPTIONS / Display  / Tips
    OPTIONS / Display  / Resolution
    OPTIONS / Sound    / Volume: BGM
    OPTIONS / Sound    / Volume: Sound Effects
    OPTIONS / Sound    / BGM Type
    OPTIONS / Game     / DURAL
    OPTIONS / Game     / Game Mode

CE QUI REND L OPERATION POSSIBLE SANS CREER UNE SEULE TACHE, et c est mesure :
la page `TaskOptionSetting` est deja une LISTE DE LIGNES A VALEURS, et le
chantier de Dural (journal 180) lui a ajoute un DRAPEAU DE PAGE -- a 1, les
lignes portent autre chose. Il suffit de generaliser ce drapeau : au lieu de
deux etats, une FACE parmi cinq. Les quatre sous-menus de Frederic sont quatre
faces de la meme page, et la page de Dural une cinquieme.

LES CINQ MESURES QUI PORTENT TOUT :

1. **L entree choisie du menu OPTIONS se lit en un seul endroit.**
       0x1801A7029  mov eax, [rbx+0xB8]      ; l entree validee
       0x1801A702F  test eax, eax
       ... puis la chaine de `cmp eax, N` du repartiteur
   On s y greffe : on note l entree comme FACE et on force `eax = 2`, le cas
   « OPTION SETTING ». Les quatre lignes ouvrent alors la MEME page, chacune
   sur sa face. Six octets.

2. **Le titre de la page est un immediat**, et un seul :
       0x1801AA2E2  mov ecx, 0x2F3           ; " Settings "
       0x1801AA2E7  call 0x1801EFD10
   On detourne l APPEL : chaque face rend son titre.

3. **Les quatre libelles natifs sont des immediats de pile**, poses par le
   dessin, et leur identifiant sert aussi a la VALEUR :
       0x1801AA18D  [rbp-0x60] = 0x30C       Volume: Music
       0x1801AA194  [rbp-0x5C] = 0x2F6       Volume: Sound Effects
       0x1801AA19B  [rbp-0x58] = 0x322       Stage BGM Type
       0x1801AA1A2  [rbp-0x54] = 0x32A       Autosave (-> Tips)
   et le dessin calcule `id_valeur = id_libelle + 1 + valeur` (0x1801AA49E).
   Nos relais n ont donc PAS besoin de la table de pile : ils reconstruisent
   l identifiant eux-memes. C est ce qui permet a une face de montrer la
   ligne native 3 (Tips) en PREMIERE position sans rien deplacer.

4. **L ecran de remappage s ouvre tout seul.** `0x1801AB3A0(ecx, edx, r8b)`
   ouvre `OPTION CONTROL` quand `edx == 2` et `ecx != 0` -- c est la fabrique
   partagee, huit appelants. La ligne « Settings » de la face Controls
   l appelle avec les memes arguments que la branche du menu parent
   (`ecx = [0x1807513B8]`, `edx = 2`, `r8b = 1`).

5. **Le cadre et le nombre de lignes tiennent au meme registre** (journal 135)
   et se reposent a chaud : `0x1801BDA20(page+0x2B8, n+0xC)`. Verifie a
   l ecran le 2026-10-11 : la fenetre passe bien de huit lignes a quatre quand
   la page de Dural s ouvre.

CE QUI N EST PAS DANS CE FICHIER : les valeurs elles-memes. `Resolution` vit
dans la zone de `--options-resolution`, `Game Mode` dans celle de
`--options-mode`, les trois bascules de Dural dans celle de `--options-dural`.
On ne les deplace pas -- `apm.dll` surveille deux d entre elles par leur
magie. La table des logiques porte un ECART SIGNE vers chacune, et viser une
zone voisine depuis celle-ci reste du RIP-relatif.
"""

# --- LES TYPES DE REGLAGE -------------------------------------------------
NATIF = 0        # une ligne d origine : valeur en [page+0x240+n*4]
GREFFE = 1       # une valeur a nous, dans la greffe
PORTE = 2        # pas une valeur : valider ouvre autre chose

# --- LES STYLES DE BOUTONS ------------------------------------------------
# (nom affiche, disponible ?) -- et la DISPONIBILITE n est pas une opinion :
# elle dit si la planche existe.
#
# CE QUI EST DEJA DANS LE JEU, et c est la table des echappements qui le dit
# (`analysis/polices_et_pictos.md`) : la planche `spr_n_fnt32` porte DEUX jeux
# de pastilles, `U+E000`-`E003` (le B, A, Y, X **Xbox**) et `U+E015`-`E018`
# (le ○, ✕, △, □ **PS3**). Choisir entre ces deux-la ne demande AUCUN dessin :
# il suffit de dire aux libelles lequel viser, ce que `tools/pictos_xbox.py`
# fait deja dans la table de chaines.
#
# LES AUTRES repeignent le bloc PS3 de la planche -- c est ce que Frederic a
# fait pour la PS5 et la Xbox One. La PS4 attend sa planche.
# (clef, nom affiche, suffixe du PNG ou None, faut-il la table Xbox ?)
# C est LA table : `tools/boutons_style.py` l importe, et `apm.dll` emploie
# les memes clefs. L indice de la ligne est ce par quoi les trois se parlent.
BOUTONS = (
    ('ps3',  'PlayStation 3', None,      False),   # la planche d origine
    ('ps4',  'PlayStation 4', 'PS4',     False),
    ('ps5',  'PlayStation 5', 'PS5',     False),
    ('x360', 'XBOX 360',      None,      True),    # le bloc Xbox NATIF
    ('xone', 'XBOX One',      'xboxone', False),
)
BTN_CLEFS = tuple(b[0] for b in BOUTONS)


def planche(racine, suffixe):
    """Le chemin de la planche repeinte d un style."""
    return os.path.join(racine, 'HD_TEXTURES', 'HD', '2D',
                        'spr_n_fnt32__tex00_%s.png' % suffixe)


def dispo(racine):
    """UN BIT PAR STYLE DISPONIBLE, et ce n est pas une opinion : on regarde
    si la planche est la.

    Elle etait ECRITE EN DUR jusqu au 2026-10-11, et le jour ou Frederic a
    pose `spr_n_fnt32__tex00_PS4.png` le menu a continue de sauter la PS4.
    Un fait qui vit sur le disque se lit sur le disque.
    """
    m = 0
    for i, (_c, _n, suf, _x) in enumerate(BOUTONS):
        if suf is None or os.path.exists(planche(racine, suf)):
            m |= 1 << i
    return m

# --- LES REGLAGES, par identifiant LOGIQUE --------------------------------
# (nom affiche, type, parametre, maxi)
#   NATIF   : parametre = la ligne d origine (0 a 3)
#   GREFFE  : parametre = la clef de la variable (resolue par le patcheur)
#   PORTE   : parametre = ce que la validation fait
LOG = [
    ('Volume: BGM',           NATIF,  0,              20),
    ('Volume: Sound Effects', NATIF,  1,              20),
    ('BGM Type',              NATIF,  2,              6),
    ('Tips',                  NATIF,  3,              1),
    ('Resolution',            GREFFE, 'res',          4),
    ('Game Mode',             GREFFE, 'mod',          1),
    ('DURAL',                 PORTE,  'face:4',       0),
    ('Settings',              PORTE,  'remap',        0),
    ('Dural: Single Player',  GREFFE, 'dur0',         1),
    ('Dural: Offline VS',     GREFFE, 'dur1',         1),
    ('Dural: Online VS',      GREFFE, 'dur2',         1),
    ('Buttons style',         GREFFE, 'btn',          len(BOUTONS) - 1),
]
(L_BGM, L_SE, L_TYPE, L_TIPS, L_RES, L_MODE, L_DURAL, L_REMAP,
 L_DUR0, L_DUR1, L_DUR2, L_BTN) = range(len(LOG))

# LES IDENTIFIANTS NATIFS, releves dans le dessin (0x1801AA18D et suivants).
# L identifiant de la VALEUR vaut `id + 1 + valeur` : c est le calcul du jeu
# lui-meme (0x1801AA4A6), et nos relais le refont.
ID_NATIF = {0: 0x30C, 1: 0x2F6, 2: 0x322, 3: 0x32A}

# --- LES FACES ------------------------------------------------------------
# (titre, [logiques]) ; l ordre est celui des lignes du menu OPTIONS.
FACES = [
    ('Controls', [L_REMAP, L_BTN]),
    ('Display',  [L_TIPS, L_RES]),
    ('Sound',    [L_BGM, L_SE, L_TYPE]),
    ('Game',     [L_DURAL, L_MODE]),
    ('Dural',    [L_DUR0, L_DUR1, L_DUR2]),
]
FACE_DURAL = 4
FACE_MAX_LIGNES = 8

# Les quatre lignes du menu OPTIONS lui-meme : les quatre premieres faces.
PARENT = [f[0] for f in FACES[:4]]

# --- LES SITES ------------------------------------------------------------
# Le repartiteur du menu OPTIONS : la lecture de l entree choisie.
PARENT_AIGUILLAGE = (0x1801A7029, bytes.fromhex('8b83b8000000'))
# Le titre de la page de reglages.
TITRE_APPEL = (0x1801AA2E7, bytes.fromhex('e8245a0400'))
# Le nombre de lignes du menu OPTIONS et son cadre (init 0x1801AAFF0).
# Le menu OPTIONS lui-meme : son nombre de lignes et son cadre, dans l init
# 0x1801AAFF0. Adresses relevees par options_sans_howto, qui les manipule
# deja -- d ou le refus de poser les deux ensemble.
PARENT_BORNE = 0x1801AB03F        # l immediat de `mov eax, 4`
PARENT_CMOVE = 0x1801AB043        # `cmove eax, ecx`, a effacer
# LE CADRE DU MENU OPTIONS ne compte PAS le titre -- mesure a l ecran le
# 2026-10-09 : `choice_win_0N` donne N bandes de CONTENU, et ce menu
# porte son titre AU-DESSUS. Quatre lignes demandent donc `choice_win_04` (0x0F),
# qui est deja l immediat du premier chemin ; seul le second est a corriger.
PARENT_CADRE1 = 0x1801AB0ED       # 0x0F -- deja bon pour quatre lignes
PARENT_CADRE2 = 0x1801AB16B       # 0x10 -> 0x0F
# L INIT GRISE LES LIGNES PAR UN TABLEAU D OCTETS, un par ligne, rempli de
# comparaisons en cascade sur le dernier indice :
#     +0x2F2 = (n <= 0)   +0x2F3 = (n < 2)   +0x2F4 = (n < 3)
#     +0x2F5 = (n < 4)    +0x2F6 = (n < 5)
# A QUATRE LIGNES la derniere ressortait GRISEE -- constate a l ecran. Le
# tableau commence donc a +0x2F2 pour la ligne 0, et c est +0x2F5 qui porte
# la ligne 3 : sa condition doit passer de `n < 4` a `n < 3`. Un octet.
PARENT_GRIS = ((0x1801AB098, 4), (0x1801AB0A8, 5))   # les deux derniers crans
# LA QUATRIEME LIGNE EST REGRISEE A CHAQUE TRAME, et ce n est PAS l init :
# la mise a jour la recalcule depuis un PREDICAT BOUCHONNE --
#     0x1801A7C1F  mov  ecx, [rbx+0x2FC]
#     0x1801A7C25  call 0x1801A2330      ; l etat de ce joueur
#     0x1801A7C2C  call 0x180007450      ; LE BOUCHON : rend toujours 0
#     0x1801A7C33  je   0x1801A7C3E      ; faux -> al = 1 -> GRISEE
# C etait la garde de « Save Data », dont la page ne faisait rien sur cette
# borne. Zeroter les six octets de l init ne servait donc a rien : ils sont
# reecrits a la trame suivante. On corrige la SORTIE, deux octets, plutot que
# de forcer un predicat partage dont on ne tient pas l autre test (`bpl`).
PARENT_GRIS_L3 = (0x1801A7C3E, bytes.fromhex('b001'), bytes.fromhex('30c0'))
# LA PORTE VERS L ECRAN DE REMAPPAGE ne passe PAS par la fabrique autonome
# `0x1801AB3A0` : essayee le 2026-10-11, elle ne montre rien -- elle demarre
# sa scene par `0x180245830` et retombe en silence tant que la notre tourne.
# On passe donc par le chemin du MENU PARENT, qui est eprouve : on lui pose
# l entree 1 (« Controls ») et son drapeau de validation, on ferme notre page,
# et SON repartiteur ouvre l ecran. Le pointeur de la page OPTIONS est le
# global que la fabrique elle-meme lit.
PAGE_OPTIONS = 0x1807513C0        # un POINTEUR vers la page du menu OPTIONS
PAGE_ENTREE = 0xB8                # l entree choisie
PAGE_VALIDE = 0xC0                # « elle est validee »
# ET IL FAUT ATTENDRE LE RETOUR DE LA PAGE, pas la trame suivante.
#
# LE PREMIER SITE ESSAYE (0x1801A701D, le test de validation) N OUVRAIT RIEN
# -- essai du 2026-10-11 -- et la MACHINE A ETATS du menu OPTIONS dit pourquoi
# (0x1801A6F96, `mov ecx,[rbx+0x58]`) :
#
#   etat 0  -> 0x1801A700C : il SONDE la liste [rbx+0x60] et ressort tant
#              qu elle VIT. [rbx+0xC0] n est donc lu qu une fois, a l instant
#              ou l utilisateur vient de choisir une ligne.
#   etat 1  -> 0x1801A6FDE : une page fille tourne ; quand elle meurt,
#              0x1801A7000 pose l ETAT 2.
#   etat 2  -> 0x1801A6FAB : il REFABRIQUE la liste et repasse a l etat 0.
#
# Notre mot etait donc pose a 1 et plus jamais relu : la liste renaissait
# VIVANTE, et 0x1801A701D restait hors d atteinte jusqu au choix suivant.
# « Poser la demande a chaque trame » decrivait un site qui ne repasse pas.
#
# ON SE GREFFE DONC SUR LE RETOUR DE LA PAGE FILLE, 0x1801A7000 : la liste y
# est encore morte, et il suffit d y poser l entree 1, son drapeau de
# validation et l ETAT 0 -- au lieu de 2 -- pour que la trame suivante tombe
# dans le repartiteur par le chemin d origine, sans que la liste ait eu le
# temps de renaitre. Le mot compte trois etats :
#     0 rien   1 demande, la page se ferme   2 posee, l aiguillage la passe
PAGE_RETOUR = (0x1801A7000, bytes.fromhex('c7435802000000'))
PAGE_SUITE = 0x1801A7007          # le `jmp` vers la sortie de la fonction
PAGE_ETAT = 0x58                  # l etat du menu OPTIONS
# La fabrique des pages d options, pour la porte « Settings ».
FABRIQUE = 0x1801AB3A0
FABRIQUE_TYPE = 0x1807513B8       # le global que la branche du parent lit
# Le resolveur de textes.
RESOLVEUR = 0x1801EFD10
# Le poseur de cadre, et les trois sites de ligne de la page de reglages.
CADRE_POSER = 0x1801BDA20
CADRE_APPEL = (0x1801AB2F7, bytes.fromhex('e824270100'))
VERT_SITE = (0x1801AB9BF, bytes.fromhex('8b848140020000'))
HORIZ_SITE = (0x1801AA707, bytes.fromhex('4289848140020000'))
VALIDER_SITE = (0x1801A80E0, bytes.fromhex('48895c2408'))
LIBELLE_APPEL = (0x1801AA485, bytes.fromhex('e886580400'))
VALEUR_APPEL = (0x1801AA4AA, bytes.fromhex('e861580400'))
PARENT_LBL_APPEL = (0x1801AA0BA, bytes.fromhex('e8515c0400'))
CRENEAU9 = 0x180411240
# ET L ECRAN DE REMAPPAGE PORTE LE MEME MANQUE. Sa table (TaskOptionControl,
# 0x180411188) a elle aussi le bouchon partage `ret 0` au creneau [9] : une
# fois la porte ouverte, A et BACK n en sortaient pas -- constate a l ecran le
# 2026-10-11, l ecran restait en place quatre captures de suite. START en
# sort, parce que le creneau [10] (0x1801A7ED0) ferme la page.
#
# On lui donne donc une sortie, et PAS le creneau [10] tel quel : celui-ci
# commence par `cmp [rcx+0x58], 9` et, sur cette ligne-la, part dans
# 0x1801AB6D0 -- l essai d affectation. Notre relais reprend son prologue et
# entre APRES le test, en 0x1801A7EF4, donc il ferme toujours.
CTL_CRENEAU9 = 0x1804111D0
CTL_PROLOGUE = bytes.fromhex('48895c24085748 83ec208bfa488bd9'.replace(' ', ''))
CTL_FERMER = 0x1801A7EF4
FLAGS_SITE = (0x1801AB27E, bytes.fromhex('c7871103000000000000'))

# --- LA DISPOSITION DE LA ZONE -------------------------------------------
# Aucune adresse absolue : la greffe n a pas de relocation.
V2_MAGIE = b'VF5OPTV2'
V2_FACE = 0x008          # la face courante
V2_DEMANDE = 0x00C       # la face que le menu parent vient de demander
V2_REMAP = 0x00E         # le mot qui laisse passer l entree 1 d origine
V2_TITRES = 0x010        # par face, 0x10 octets
V2_BTN = 0x060           # le style de boutons : valeur courante
V2_BTN_CONF = 0x064      # ... et valeur CONFIRMEE, celle que apm.dll surveille
V2_BTN_DISPO = 0x068     # un bit par style disponible
V2_EDX = 0x06C           # le `edx` d origine de la validation, mis de cote
V2_NOMS = 0x090          # par logique, 0x20 octets
V2_LOGS = 0x230          # par logique, 0x10 octets (voir plus bas)
V2_TBL = 0x300           # par face, 0x10 octets : n, cadre, puis 8 logiques
# LES CINQ NOMS DE STYLES, AU PAS DE 0x10 -- celui que le relais `valeur`
# emploie pour TOUS les textes de valeur (`shl rcx, 4`). Ils etaient ECRITS
# au pas de 0x20 et LUS au pas de 0x10 : un nom sur deux tombait au milieu du
# precedent, sur ses zeros. Frederic, 2026-10-11 : « xbox 360 et xbox one
# n apparaissent pas mais il y a deux champs vides ». « PlayStation 3 », le
# plus long, fait treize caracteres : 0x10 suffit.
V2_BTN_TXT = 0x350       # les cinq noms de styles, pas de 0x10
V2_VIDE = 0x3F8          # la chaine vide, pour les lignes sans valeur
V2_CODE = 0x400

V2_TITRE_PAS = 0x10
V2_NOM_PAS = 0x20
V2_LOG_PAS = 0x10
V2_FACE_PAS = 0x10

# La table des logiques, 0x10 octets par entree :
#   +0x0  type (0 natif, 1 greffe, 2 porte)
#   +0x1  ligne native, ou le parametre de la porte
#   +0x2  maxi horizontal
#   +0x4  DEUX SENS, et ils ne se rencontrent jamais : l identifiant natif du
#         libelle pour une ligne NATIVE, l ecart signe vers la valeur
#         CONFIRMEE pour une ligne GREFFEE (0 si elle n en a pas). Un type ne
#         lit jamais le champ de l autre, et l entree tient en 0x10 octets.
#   +0x8  ecart signe vers la variable (greffe), depuis la base de la zone
#   +0xC  ecart signe vers le premier texte de valeur (greffe)
#   +0x3  un bit par valeur DISPONIBLE (0 = toutes le sont)
LOGT_TYPE, LOGT_PARAM, LOGT_MAXI, LOGT_DISPO = 0x0, 0x1, 0x2, 0x3
LOGT_CONF = 0x4          # le MEME octet que LOGT_ID, pour l autre type
LOGT_ID, LOGT_VAR, LOGT_TXT = 0x4, 0x8, 0xC


# ---------------------------------------------------------------------------
import os
import struct                                                 # noqa: E402


class Bloc(object):
    """Un morceau de code, avec des ETIQUETTES.

    Les sauts courts sont ecrits a zero puis remplis quand tout est la. La
    premiere version calculait ces distances a la main : six sur quatorze
    etaient fausses, et un `jne` qui tombe un octet trop loin ne se voit pas
    -- il entre au MILIEU de l instruction suivante.
    """

    def __init__(self, va, base):
        self.va = va          # l adresse de la zone
        self.base = base      # l offset de ce bloc dans la zone
        self.c = bytearray()
        self.etiq = {}
        self.trous = []

    def __len__(self):
        return len(self.c)

    def o(self, hexa):
        """Des octets bruts."""
        self.c += bytes.fromhex(hexa)
        return self

    def b(self, octets):
        self.c += octets
        return self

    def rip(self, hexa, cible, apres=0):
        """Une instruction a deplacement RIP, vers un offset de la zone.

        `apres` est le nombre d octets qui SUIVENT le deplacement dans
        l instruction (un immediat, par exemple).
        """
        d = bytes.fromhex(hexa)
        fin = self.base + len(self.c) + len(d) + 4 + apres
        self.c += d + struct.pack('<i', cible - fin)
        return self

    def abs_(self, hexa, cible):
        """Une instruction a deplacement RIP vers une adresse du MOTEUR."""
        d = bytes.fromhex(hexa)
        fin = self.va + self.base + len(self.c) + len(d) + 4
        self.c += d + struct.pack('<i', cible - fin)
        return self

    def court(self, op, nom):
        """Un saut court vers une etiquette, rempli en deuxieme passe."""
        self.trous.append((len(self.c) + 1, nom))
        self.c += bytes.fromhex(op) + b'\x00'
        return self

    def ici(self, nom):
        self.etiq[nom] = len(self.c)
        return self

    def fini(self):
        for pos, nom in self.trous:
            if nom not in self.etiq:
                raise AssertionError('etiquette inconnue : %s' % nom)
            d = self.etiq[nom] - (pos + 1)
            if not -128 <= d < 128:
                raise AssertionError('saut court hors de portee : %s' % nom)
            self.c[pos] = d & 0xFF
        return bytes(self.c)


def zone(va, ecarts, textes_valeur, maxi_ecart, confs=None, style=0,
         btn_dispo=None):
    """La zone V2 : les tables, puis les relais.

    `va` est l adresse de la zone ; `ecarts` donne par clef de variable
    (`res`, `mod`, `dur0`...) l ECART SIGNE entre la base de cette zone et la
    variable -- les zones de la greffe sont a des offsets FIXES l une de
    l autre, donc viser la voisine reste du RIP-relatif ; `textes_valeur`
    l ecart vers le premier texte de valeur (pas de 0x10) ; `maxi_ecart`
    celui de la table des maximums, qui vit dans la zone de la resolution.
    """
    z = bytearray(V2_CODE)
    z[0:8] = V2_MAGIE
    z[V2_VIDE] = 0

    for i, (titre, _l) in enumerate(FACES):
        bb = titre.encode('ascii') + b'\x00'
        z[V2_TITRES + V2_TITRE_PAS * i:
          V2_TITRES + V2_TITRE_PAS * i + len(bb)] = bb
    for i, (nom, _t, _p, _m) in enumerate(LOG):
        bb = nom.encode('ascii') + b'\x00'
        if len(bb) > V2_NOM_PAS:
            raise AssertionError('nom trop long : %r' % nom)
        z[V2_NOMS + V2_NOM_PAS * i:V2_NOMS + V2_NOM_PAS * i + len(bb)] = bb
    masque = (1 << len(BOUTONS)) - 1 if btn_dispo is None else btn_dispo
    struct.pack_into('<I', z, V2_BTN_DISPO, masque)
    # LE STYLE EN PLACE, pas zero : la zone s ouvre sur ce que la planche
    # porte vraiment, sans quoi `apm.dll` verrait un changement des le
    # premier battement et fermerait le jeu.
    struct.pack_into('<I', z, V2_BTN, style)
    struct.pack_into('<I', z, V2_BTN_CONF, style)
    for i, (_c, nom, _s, _x) in enumerate(BOUTONS):
        bb = nom.encode('ascii') + b'\x00'
        if len(bb) > 0x10:
            raise AssertionError('nom de style trop long : %r' % nom)
        z[V2_BTN_TXT + 0x10 * i:V2_BTN_TXT + 0x10 * i + len(bb)] = bb
    for i, (_n, typ, par, maxi) in enumerate(LOG):
        o = V2_LOGS + V2_LOG_PAS * i
        z[o + LOGT_TYPE] = typ
        z[o + LOGT_MAXI] = maxi
        if typ == NATIF:
            z[o + LOGT_PARAM] = par
            struct.pack_into('<I', z, o + LOGT_ID, ID_NATIF[par])
        elif typ == GREFFE:
            struct.pack_into('<i', z, o + LOGT_CONF,
                             (confs or {}).get(par, 0))
            struct.pack_into('<i', z, o + LOGT_VAR, ecarts[par])
            struct.pack_into('<i', z, o + LOGT_TXT, textes_valeur[par])
            if par == 'btn':
                z[o + LOGT_DISPO] = masque
        else:
            z[o + LOGT_PARAM] = (int(par.split(':')[1])
                                 if par.startswith('face:') else 0xFF)
    for i, (_t, lignes) in enumerate(FACES):
        o = V2_TBL + V2_FACE_PAS * i
        if len(lignes) > FACE_MAX_LIGNES:
            raise AssertionError('face %d : trop de lignes' % i)
        z[o] = len(lignes)
        z[o + 1] = len(lignes) + 0xC            # le cadre, choice_win_0N
        for k, lg in enumerate(lignes):
            z[o + 2 + k] = lg

    pos = {}

    def neuf(nom):
        pos[nom] = len(z)
        return Bloc(va, pos[nom])

    def ajouter(nom, bl):
        z.extend(bl.fini())
        return pos[nom]

    def appel(bl, nom):
        """`call` vers un relais deja ecrit."""
        fin = bl.base + len(bl) + 5
        bl.b(bytes.fromhex('e8') + struct.pack('<i', pos[nom] - fin))
        return bl

    # --- _log : eax = ligne -> eax = logique. N ecrase que rax. -----------
    bl = neuf('log')
    bl.o('51').o('52')                                 # push rcx, rdx
    bl.rip('8b0d', V2_FACE)                            # mov ecx,[rip+FACE]
    bl.o('c1e104')                                     # shl ecx, 4
    bl.rip('488d15', V2_TBL)                           # lea rdx,[rip+TBL]
    bl.o('4801ca')                                     # add rdx, rcx
    bl.o('4898')                                       # cdqe
    bl.o('0fb6440202')                                 # movzx eax,[rdx+rax+2]
    bl.o('5a').o('59').o('c3')
    ajouter('log', bl)

    # --- _desc : eax = logique -> rdx = &LOG[logique] --------------------
    bl = neuf('desc')
    bl.o('4898').o('48c1e004')                         # cdqe ; shl rax, 4
    bl.rip('488d15', V2_LOGS)
    bl.o('4801c2').o('c3')                             # add rdx, rax ; ret
    ajouter('desc', bl)

    # --- titre : le titre de la face -------------------------------------
    bl = neuf('titre')
    bl.rip('8b05', V2_FACE)
    bl.o('48c1e004')
    bl.rip('488d0d', V2_TITRES)
    bl.o('4801c8').o('c3')
    ajouter('titre', bl)

    # --- parent : les quatre libelles du menu OPTIONS --------------------
    # Les identifiants d origine (0x2F1 a 0x2F4) servent de MARQUEURS, et ce
    # relais ne vit que sur le dessin du menu OPTIONS : 0x2F2 reste
    # « Controls » partout ailleurs. Les quatre noms SONT les titres des
    # quatre premieres faces -- une seule table pour les deux.
    bl = neuf('parent')
    bl.b(bytes.fromhex('8d81') + struct.pack('<i', -0x2F1))
    bl.o('83f803')
    bl.court('77', 'natif')
    bl.o('48c1e004')
    bl.rip('488d0d', V2_TITRES)
    bl.o('4801c8').o('c3')
    bl.ici('natif')
    bl.abs_('e9', RESOLVEUR)
    ajouter('parent', bl)

    # --- aiguillage : le menu parent note la face et ouvre la page -------
    bl = neuf('aiguillage')
    bl.b(PARENT_AIGUILLAGE[1])                         # mov eax,[rbx+0xB8]
    # UNE DEMANDE DE REMAPPAGE PASSE TELLE QUELLE : la porte « Settings » a
    # pose l entree 1 et ce mot ; on le consomme et on laisse la branche
    # d origine ouvrir l ecran.
    bl.rip('66833d', V2_REMAP, apres=1).o('02')        # cmp word [REMAP], 2
    bl.court('75', 'suite')
    bl.rip('66c705', V2_REMAP, apres=2).o('0000')      # mot = 0
    bl.court('eb', 'natif')
    bl.ici('suite')
    bl.o('83f803')
    bl.court('77', 'natif')
    bl.rip('8905', V2_DEMANDE)
    bl.o('b802000000')                                 # mov eax, 2
    bl.ici('natif')
    bl.abs_('e9', PARENT_AIGUILLAGE[0] + len(PARENT_AIGUILLAGE[1]))
    ajouter('aiguillage', bl)

    # --- retour : la page fille vient de mourir --------------------------
    # `rbx` porte le menu OPTIONS a ce site, et `eax` y est MORT (la sortie
    # le recharge depuis `sil`, 0x1801A7205). L etat pose est 0 et non 2 :
    # c est ce qui empeche la liste de renaitre avant que le repartiteur ait
    # lu notre entree.
    bl = neuf('retour')
    bl.rip('66833d', V2_REMAP, apres=1).o('01')        # cmp word [REMAP], 1
    bl.court('75', 'natif')
    bl.rip('66c705', V2_REMAP, apres=2).o('0200')      # le mot : POSEE
    bl.b(bytes.fromhex('c783') + struct.pack('<I', PAGE_ENTREE)
         + struct.pack('<I', 1))                       # [rbx+0xB8] = 1
    bl.b(bytes.fromhex('c683') + struct.pack('<I', PAGE_VALIDE) + b'\x01')
    bl.b(bytes.fromhex('c743') + bytes([PAGE_ETAT])
         + struct.pack('<I', 0))                       # [rbx+0x58] = 0
    bl.abs_('e9', PAGE_SUITE)
    bl.ici('natif')
    bl.b(PAGE_RETOUR[1])                               # mov [rbx+0x58], 2
    bl.abs_('e9', PAGE_SUITE)
    ajouter('retour', bl)

    # --- cadre : le cadre de la face ------------------------------------
    # L init appelle `0x1801BDA20(page+0x2B8, ebp)` APRES notre poseur : si
    # l on posait le cadre dans le poseur, cet appel l ecraserait avec
    # l immediat statique. On detourne donc l appel lui-meme.
    bl = neuf('cadre')
    bl.rip('8b05', V2_FACE)
    bl.o('48c1e004')
    bl.rip('488d15', V2_TBL)
    bl.o('0fb6540201')                                 # movzx edx,[rdx+rax+1]
    bl.abs_('e9', CADRE_POSER)
    ajouter('cadre', bl)

    # --- valeur_de : rcx = page, eax = ligne -> eax = la valeur ----------
    bl = neuf('valeur_de')
    bl.o('52').o('4150')                               # push rdx, r8
    appel(bl, 'log')
    appel(bl, 'desc')
    bl.o('0fb602').o('83f800')                         # type == NATIF ?
    bl.court('75', 'greffe')
    bl.o('440fb64201')                                 # movzx r8d,[rdx+1]
    bl.o('428b848140020000')                           # eax=[rcx+r8*4+0x240]
    bl.court('eb', 'fin')
    bl.ici('greffe').o('83f801')
    bl.court('75', 'zero')
    bl.o('4c634208')                                   # mov r8d,[rdx+8]
    bl.rip('488d05', 0)                                # lea rax,[base]
    bl.o('4c01c0').o('8b00')                           # add rax,r8 ; eax=[rax]
    bl.court('eb', 'fin')
    bl.ici('zero').o('31c0')
    bl.ici('fin').o('4158').o('5a').o('c3')            # pop r8, rdx ; ret
    ajouter('valeur_de', bl)

    # --- poseur : rcx = page, edx = face --------------------------------
    # Un seul cadre de pile de 0x38 : trente-deux octets d accueil pour les
    # appels, et rsp aligne. Aucune pile empilee a la main -- la premiere
    # version poussait TROIS registres sous l espace d accueil qu elle venait
    # de reserver, ce qui desalignait rsp et ecrasait cet espace.
    bl = neuf('poseur')
    bl.o('4883ec38')                                   # sub rsp, 0x38
    bl.rip('8915', V2_FACE)                            # [FACE] = edx
    bl.o('8bc2').o('48c1e004')                         # rax = face * 0x10
    bl.rip('4c8d05', V2_TBL)
    bl.o('4901c0')                                     # r8 = &TBL[face]
    bl.o('410fb600').o('ffc8')                         # eax = n - 1
    bl.o('898124020000')                               # [rcx+0x224] = eax
    bl.o('c7415800000000')                             # [rcx+0x58] = 0
    bl.o('c6813002000000')                             # [rcx+0x230] = 0
    bl.o('4531c9')                                     # xor r9d, r9d
    bl.ici('boucle')
    bl.o('430fb6440802')                               # movzx eax,[r8+r9+2]
    bl.o('48c1e004')
    bl.rip('4c8d15', V2_LOGS)
    bl.o('410fb6440202')                               # movzx eax,[r10+rax+2]
    bl.rip('4c8d1d', maxi_ecart)
    bl.o('4389048b')                                   # [r11+r9*4] = eax
    bl.o('41ffc1').o('4183f908')                       # inc r9d ; cmp 8
    bl.court('72', 'boucle')
    bl.o('31c0')                                       # la ligne 0
    appel(bl, 'valeur_de')
    bl.o('89415c')                                     # [rcx+0x5c] = eax
    bl.rip('4c8d1d', maxi_ecart)
    bl.o('418b03').o('89812c020000')                   # [rcx+0x22c] = MAXI[0]
    bl.o('410fb65001')                                 # movzx edx,[r8+1]
    bl.o('4881c1b8020000')                             # rcx += 0x2b8
    bl.abs_('e8', CADRE_POSER)
    bl.o('4883c438').o('c3')
    ajouter('poseur', bl)

    # --- libelle : le nom du reglage de la ligne -------------------------
    bl = neuf('libelle')
    bl.o('4489f0')                                     # mov eax, r14d
    appel(bl, 'log')
    bl.o('4898').o('48c1e005')                         # rax = logique * 0x20
    bl.rip('488d0d', V2_NOMS)
    bl.o('4801c8').o('c3')
    ajouter('libelle', bl)

    # --- valeur : le texte de la valeur ---------------------------------
    # `rdi` porte la page a ce site : 0x1801AA49E lit [rdi+r14*4+0x240].
    # POUR UNE LIGNE NATIVE on refait le calcul du jeu lui-meme --
    # `id_valeur = id_libelle + 1 + valeur` (0x1801AA4A6) -- et on saute au
    # resolveur. C est ce qui permet a une face de montrer la ligne native 3
    # en PREMIERE position sans rien deplacer.
    bl = neuf('valeur')
    bl.o('4489f0')
    appel(bl, 'log')
    appel(bl, 'desc')
    bl.o('0fb602').o('83f800')
    bl.court('75', 'greffe')
    bl.o('440fb64201')                                 # movzx r8d,[rdx+1]
    bl.o('8b4a04').o('ffc1')                           # ecx = id + 1
    bl.o('428b848740020000')                           # eax=[rdi+r8*4+0x240]
    bl.o('01c1')                                       # ecx += eax
    bl.abs_('e9', RESOLVEUR)
    bl.ici('greffe').o('83f801')
    bl.court('75', 'vide')
    bl.o('4c634208')
    bl.rip('488d05', 0)
    bl.o('4c01c0').o('8b08')                           # ecx = la valeur
    bl.o('440fb64202').o('4139c8')                     # cmp maxi, ecx
    bl.court('73', 'ok')
    bl.o('31c9')                                       # hors bornes -> 0
    bl.ici('ok').o('48c1e104')                         # shl rcx, 4
    bl.o('4c63420c')
    bl.rip('488d05', 0)
    bl.o('4c01c0').o('4801c8').o('c3')
    bl.ici('vide')
    bl.rip('488d05', V2_VIDE)
    bl.o('c3')
    ajouter('valeur', bl)

    # --- vert : la valeur LUE par le gestionnaire vertical ---------------
    bl = neuf('vert')
    appel(bl, 'valeur_de')
    bl.abs_('e9', VERT_SITE[0] + len(VERT_SITE[1]))
    ajouter('vert', bl)

    # --- horiz : la valeur ECRITE par le gestionnaire horizontal ---------
    # Le site est un `mov`, pas un `call` : RIEN ne doit bouger. On empile
    # tout ce qu on touche.
    bl = neuf('horiz')
    bl.o('50').o('51').o('52').o('4150').o('4151')
    bl.o('4489c0')                                     # eax = r8d (la ligne)
    appel(bl, 'log')
    appel(bl, 'desc')
    bl.o('0fb602')
    bl.o('448b4c2420')                                 # r9d = la valeur
    bl.o('83f800')
    bl.court('75', 'greffe')
    bl.o('440fb64201')
    bl.o('46898c8140020000')                           # [rcx+r8*4+0x240]=r9d
    bl.court('eb', 'fin')
    # UNE VALEUR INDISPONIBLE EST SAUTEE, et c est la seule facon de rendre
    # « PlayStation 4 » non selectionnable : cette page sait griser une
    # LIGNE (+0x311+n), pas une VALEUR. On repart donc dans LE MEME SENS
    # jusqu a la premiere valeur dont le bit est dans DISPO.
    #
    # LE SENS SE DEDUIT, le site ne le donne pas : le moteur a deja calcule
    # `nouvelle = ancienne +/- 1` avec bouclage, donc l ecart vaut 1 (ou
    # 1 - N au passage du haut) en avant, -1 (ou N - 1) en arriere.
    #
    # INVARIANT : DISPO porte au moins un bit SOUS le nombre de valeurs,
    # sinon la recherche tournerait sans fin. `BTN_DISPO` en porte quatre
    # sur cinq, et les autres reglages laissent DISPO a zero -- le chemin
    # court, qui ecrit sans rien chercher.
    bl.ici('greffe').o('83f801')
    bl.court('75', 'fin')
    bl.o('4c634208')                                   # movsxd r8,[rdx+8]
    bl.o('0fb64203')                                   # movzx eax,[rdx+3]
    bl.o('85c0')
    bl.court('74', 'simple')
    bl.o('0fb64a02').o('ffc1')                         # ecx = maxi + 1 = N
    bl.rip('488d15', 0)                                # lea rdx,[base]
    bl.o('4c01c2')                                     # rdx = &valeur
    bl.o('52').o('50')                                 # push &valeur, DISPO
    bl.o('448b02')                                     # r8d = l ancienne
    bl.o('4489ca').o('4429c2')                         # edx = neuve - ancienne
    bl.o('83fa01')
    bl.court('74', 'avant')
    bl.o('01ca').o('83fa01')                           # + N, et on recompare
    bl.court('74', 'avant')
    bl.o('41b8ffffffff')                               # r8d = -1
    bl.court('eb', 'boucle')
    bl.ici('avant').o('41b801000000')                  # r8d = +1
    bl.ici('boucle')
    bl.o('89c2')                                       # edx = DISPO
    bl.o('51').o('4489c9').o('d3ea').o('59')           # edx >>= candidat
    bl.o('f6c201')                                     # test dl, 1
    bl.court('75', 'trouve')
    bl.o('4501c1')                                     # candidat += sens
    bl.o('4585c9')
    bl.court('79', 'pas_bas')
    bl.o('448d49ff')                                   # candidat = N - 1
    bl.ici('pas_bas')
    bl.o('4139c9')
    bl.court('72', 'boucle')
    bl.o('4531c9')                                     # candidat = 0
    bl.court('eb', 'boucle')
    bl.ici('trouve')
    bl.o('58').o('5a')                                 # pop DISPO, &valeur
    bl.o('44890a')                                     # [rdx] = candidat
    bl.court('eb', 'fin')
    bl.ici('simple')
    bl.rip('488d05', 0)
    bl.o('4c01c0').o('448908')                         # [rax] = r9d
    bl.ici('fin')
    bl.o('4159').o('4158').o('5a').o('59').o('58')
    bl.abs_('e9', HORIZ_SITE[0] + len(HORIZ_SITE[1]))
    ajouter('horiz', bl)

    # --- confirmer : VAL -> CONF pour TOUTES les lignes greffees ---------
    # `apm.dll` ne surveille pas la valeur courante mais la CONFIRMEE : sans
    # cela le jeu se fermerait des le premier appui sur une fleche, avant
    # meme d avoir montre le choix. C est ce que faisait le relais R5 de
    # `--options-resolution` ; en v2 c est NOUS qui tenons ce site, et la
    # copie avait ete oubliee -- Resolution, Game Mode et les bascules de
    # Dural s affichaient, se changeaient, et la validation ne declenchait
    # rien.
    #
    # ON CONFIRME TOUT, pas seulement la ligne courante : sur la page de
    # Dural on change une bascule, on descend, on en change une autre, et on
    # valide sur la derniere. Le relais d origine le faisait deja ainsi.
    bl = neuf('confirmer')
    bl.o('50').o('51').o('52').o('56').o('57').o('4150')   # 6 push
    bl.rip('488d35', 0)                                # rsi = base de la zone
    bl.o('31c9')                                       # xor ecx, ecx
    bl.ici('boucle')
    bl.o('4889c8')                                     # mov rax, rcx
    bl.o('48c1e004')                                   # shl rax, 4
    bl.b(bytes.fromhex('488d96') + struct.pack('<I', V2_LOGS))
    bl.o('4801d0')                                     # rax = &LOG[i]
    bl.o('803801')                                     # cmp byte [rax], GREFFE
    bl.court('75', 'suivant')
    bl.b(bytes.fromhex('486350') + bytes([LOGT_CONF]))  # movsxd rdx,[rax+4]
    bl.o('4885d2')                                     # test rdx, rdx
    bl.court('74', 'suivant')
    bl.b(bytes.fromhex('486378') + bytes([LOGT_VAR]))   # movsxd rdi,[rax+8]
    bl.o('8b043e')                                     # eax = [rsi+rdi]
    bl.o('890416')                                     # [rsi+rdx] = eax
    bl.ici('suivant')
    bl.o('ffc1')                                       # inc ecx
    bl.b(bytes.fromhex('83f9') + bytes([len(LOG)]))
    bl.court('72', 'boucle')
    bl.o('4158').o('5f').o('5e').o('5a').o('59').o('58')
    bl.o('c3')
    ajouter('confirmer', bl)

    # --- valider : les portes, ou la fermeture d origine -----------------
    # `edx` EST VIVANT A CE SITE -- 0x1801A80EA en fait `mov edi, edx` -- et
    # `desc` l ecrase. On le met de cote dans la zone (ce code ne tourne que
    # sur le fil du menu) plutot que de l empiler : une pile de plus
    # DESALIGNERAIT `rsp` pour l appel du poseur, qui appelle lui-meme.
    bl = neuf('valider')
    bl.rip('8915', V2_EDX)                             # [EDX] = edx
    bl.o('8b4158')                                     # eax = [rcx+0x58]
    appel(bl, 'log')
    appel(bl, 'desc')
    bl.o('0fb602').o('83f802')                         # type == PORTE ?
    bl.court('75', 'natif')
    bl.o('0fb65201')                                   # movzx edx,[rdx+1]
    bl.o('80fa ff'.replace(' ', ''))                   # cmp dl, 0xFF
    bl.court('74', 'remap')
    bl.o('4883ec28')
    appel(bl, 'poseur')
    bl.o('4883c428').o('c3')
    bl.ici('remap')
    bl.rip('66c705', V2_REMAP, apres=2).o('0100')      # le mot : DEMANDE
    bl.court('eb', 'natif')                            # et on ferme, comme Entree
    bl.ici('natif')
    appel(bl, 'confirmer')
    bl.rip('8b15', V2_EDX)                             # edx = [EDX]
    bl.b(VALIDER_SITE[1])
    bl.abs_('e9', VALIDER_SITE[0] + len(VALIDER_SITE[1]))
    ajouter('valider', bl)

    # --- annuler_ctl : la sortie de l ecran de remappage -----------------
    bl = neuf('annuler_ctl')
    bl.b(CTL_PROLOGUE)
    bl.abs_('e9', CTL_FERMER)
    ajouter('annuler_ctl', bl)

    # --- annuler : le creneau [9], qui etait le bouchon `ret 0` ----------
    bl = neuf('annuler')
    bl.rip('8b05', V2_FACE)
    bl.b(bytes.fromhex('83f8') + bytes([FACE_DURAL]))
    bl.court('75', 'fermer')
    bl.o('ba03000000')                                 # la face Game
    bl.o('4883ec28')
    appel(bl, 'poseur')
    bl.o('4883c428').o('31c0').o('c3')
    bl.ici('fermer')
    bl.b(VALIDER_SITE[1])
    bl.abs_('e9', VALIDER_SITE[0] + len(VALIDER_SITE[1]))
    ajouter('annuler', bl)

    # --- init : l init de la page applique la face demandee -------------
    # Le site est `mov dword [rdi+0x311], 0` (0x1801AB27E), DANS l init :
    # c est le seul endroit qui voie toutes les ouvertures, par ou qu elles
    # passent. `rdi` y porte la page. `rsp` y est aligne sur seize (prologue
    # `push rdi ; sub rsp,0x40`), et l init a deja reserve plus que les
    # trente-deux octets d accueil : on appelle donc directement, et les deux
    # `push` gardent l alignement.
    bl = neuf('init')
    bl.b(FLAGS_SITE[1])                                # l instruction d origine
    bl.o('51').o('52')                                 # push rcx, rdx
    bl.o('488bcf')                                     # mov rcx, rdi
    bl.rip('8b15', V2_DEMANDE)                         # mov edx, [DEMANDE]
    appel(bl, 'poseur')
    bl.o('5a').o('59')                                 # pop rdx, rcx
    bl.abs_('e9', FLAGS_SITE[0] + len(FLAGS_SITE[1]))
    ajouter('init', bl)

    return bytes(z), pos
