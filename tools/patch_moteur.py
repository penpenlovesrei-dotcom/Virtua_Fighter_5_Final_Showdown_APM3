#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patcheur unique de `vfes.exe` et du moteur. Toujours a partir des originaux.

Pourquoi un seul outil : chaque correctif avait son propre `.origine`, et le
suivant ecrasait le precedent. Ici on repart **systematiquement des fichiers
d'origine** et on applique la liste complete des options demandees. L'etat est
donc toujours reconstructible et jamais empile.

Les correctifs disponibles :

  * **resolution** -- quatre immediats, deux par binaire. Corriger `vfes.exe`
    seul laisse le moteur creer ses cibles et sa vue en 1920x1080.
  * **langue** -- le getter de region `0x1802447C0` rend toujours 2 (export).
    Verifie a l'ecran : plus un caractere japonais.
  * **logo-japonais** -- ne force QUE le site du logo (`0x18006BBD1`) a
    reprendre la branche Japon, en remplacant son `call` par `xor eax, eax`.
    Le reste du jeu suit le drapeau global, donc reste en anglais.
  * **config de demarrage** -- le `vf5fs_game_config_t` que `vfes.exe` passe a
    `module_start`. YAMP en donne les champs ; nous en avons trouve les cinq
    instructions qui l'ecrivent, dans `vfes.exe+0x2D45..0x2E32`. Le moteur en
    fait un global (`0x18064D950`) et en derive quatre drapeaux, dont
    `game_mode != 0` -- l'aiguillage borne/console, consulte a 32 endroits.

Usage :
    py -3 tools/patch_moteur.py --lire
    py -3 tools/patch_moteur.py --resolution 1280 720 --langue --logo-japonais
    py -3 tools/patch_moteur.py --mode 0            demarre en mode console
    py -3 tools/patch_moteur.py --temps 99 --energie 300 --rounds 3
    py -3 tools/patch_moteur.py --rendre
"""
import os
import shutil
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
RACINE = os.path.dirname(ICI)
JEU = os.path.join(RACINE, 'runtime', 'media', 'vf5fs')
EXE, DLL = 'vfes.exe', 'vf5fs-pxd-w64-Retail_APM3.dll'

RESOLUTION = [
    (EXE, 0x140002FD3 + 3, 'largeur'),      # mov [rbp-0x50], 0x780
    (EXE, 0x140002FDA + 3, 'hauteur'),      # mov [rbp-0x4c], 0x438
    (DLL, 0x1800E74A0 + 6, 'largeur'),      # mov [rsi+0xa4], 0x780
    (DLL, 0x1800E74AA + 6, 'hauteur'),      # mov [rsi+0xa8], 0x438
]
# Region : DEUX fonctions lisent le meme octet 0x18064D956, et il faut les
# corriger TOUTES LES DEUX. N'en patcher qu'une laisse le jeu revenir au
# japonais -- erreur commise le 2026-09-03.
#   0x1802447B0  movzx eax, byte [..] ; ret                  -> rend 0 ou 1
#   0x1802447C0  movzx ... neg ; sbb ; and 2 ; ret            -> rend 0 ou 2
LANGUE = [
    (DLL, 0x1802447B0, bytes.fromhex('0FB605'), bytes.fromhex('B801000000C3')),
    (DLL, 0x1802447C0, bytes.fromhex('0FB605'), bytes.fromhex('B802000000C3')),
]
# site du logo : call RegionExport  ->  xor eax,eax ; nop nop nop
LOGO_JP = (DLL, 0x18006BBD1, b'\xE8', bytes.fromhex('31C0909090'))

# ---------------------------------------------------------------------------
# vf5fs_game_config_t -- les 8 octets passes a `module_start`
#
# YAMP (CookiePLMonster, source/V6-VF5FS.cpp) en donne les champs :
#     uint16_t energy; int8_t round; int8_t time; int8_t diff;
#     int8_t game_mode; int8_t lang;
#     bool is_triangle_start : 4;  bool is_dural_unlocked : 4;
#
# `vfes.exe` l'ecrit sur la pile en CINQ instructions, dans cet ordre. La
# structure complete des parametres commence a [rsp+0x40] et fait 0x70 octets ;
# la config est donc a [rsp+0x78].
#
#   0x140002D45  mov  dword [rsp+0x78], 0x2D0300DC   energy=220 round=3 time=45
#   0x140002D77  mov  dword [rsp+0x7C], 0x01000102   diff=2 mode=1 lang=0 fl=1
#   0x140002DE7  and  byte  [rsp+0x7F], 0xF0         efface is_triangle_start
#   0x140002E1C  mov  byte  [rsp+0x7D], 1            game_mode  (dernier mot)
#   0x140002E32  mov  byte  [rsp+0x7A], 2            round      (dernier mot)
#
# Deux champs sont ecrits DEUX FOIS : `round` et `game_mode`. C'est la
# deuxieme ecriture qui compte, et c'est elle qu'on patche.
#
# Valeur finale relevee au debogueur sur `module_start` :
#   DC 00 02 2D 02 01 00 00
# soit exactement ce que cette lecture predit, octet pour octet. CONFIRMED.
#
# Cote moteur, `module_start` recopie les 8 octets d'un bloc dans le global
# 0x18064D950, puis en derive quatre drapeaux :
#   0x180C3B700 = is_dural_unlocked        (5 references)
#   0x180C3B701 = game_mode != 0           (32 references -- L'AIGUILLAGE)
#   0x180C3B702 = game_mode == 2           (12 references -- un 3e mode existe)
#   0x180C3B703 = is_triangle_start        (5 references)
# Et 0x18064D950 + 6 est exactement l'octet de langue deja patche : la
# coincidence ferme la demonstration.
CFG_SITES = {                      # site -> (binaire, VA, octets attendus)
    'D45': (EXE, 0x140002D45, bytes.fromhex('C7442478')),
    'D77': (EXE, 0x140002D77, bytes.fromhex('C744247C')),
    'DE7': (EXE, 0x140002DE7, bytes.fromhex('80642 47F'.replace(' ', ''))),
    'E1C': (EXE, 0x140002E1C, bytes.fromhex('C644247D')),
    'E32': (EXE, 0x140002E32, bytes.fromhex('C644247A')),
}
# champ -> (site, decalage dans l'immediat, taille, borne haute, libelle)
CONFIG = {
    'energie':    ('D45', 0, 2, 65535, 'energie de depart'),
    'temps':      ('D45', 3, 1, 255, 'temps de round, en secondes'),
    'difficulte': ('D77', 0, 1, 255, 'difficulte'),
    'rounds':     ('E32', 0, 1, 255, 'rounds a gagner'),
    'mode':       ('E1C', 0, 1, 2, 'game_mode : 0 console, 1 borne, 2 ?'),
}
CFG_DRAPEAUX = ('D77', 3)          # l'octet des deux quartets
CFG_MASQUE = ('DE7', 0)            # le 0xF0 du `and`

# ---------------------------------------------------------------------------
# MENU CONSOLE : rendre a la page du menu principal les deux tics qu'elle a
# perdus.
#
# Mesure. En mode console (`--mode 0`) le moteur atteint bien l'etat MENU et
# DESSINE le cadre du menu, mais pas ses entrees. La fonction de dessin
# (`0x1801E0C80`) garde chacun de ses blocs par un predicat minuscule :
#
#     0x1801BDA10   cmp dword ptr [rcx], 3 ; sete al ; ret
#
# c'est-a-dire « cet objet AET est-il pret ? ». Point d'arret sur la garde :
# **1452 passages, en-tete = 1 et texte = 1, jamais 3.** Les deux objets sont
# crees mais n'avancent jamais.
#
# Or l'etat d'un objet AET est avance par un tic, `0x1801BBB10` :
#     1 -> 0x1801BE520(obj, 0) ; etat = 2
#     2 -> si charge : 0x1801BE520(obj, 1) ; etat = 3
# Rester a 1 ne veut donc pas dire « le chargement echoue » : cela veut dire
# que **personne ne fait tourner le tic**.
#
# La page du menu est un objet C++ construit par `0x1801DA550`, dont la vtable
# est en `0x180532AE8`. Le creneau 2 de cette vtable est la mise a jour de la
# page. Comparaison avec les CINQ pages soeurs que le meme constructeur
# assemble, en comptant les appels au tic dans chaque mise a jour :
#
#     0x1801DDB40 : 2      0x1801DD9C0 : 2      0x1801DC510 : 2
#     0x1801DD7A0 : 2      0x1801DD400 : 2
#     0x1801DC620 (MENU) : 0
#
# Cinq soeurs, deux tics chacune ; le menu, zero. C'est la coupe du build
# arcade, a l'instruction pres.
#
# Le remede : un relais de 52 octets, pose dans le rembourrage de `.text`, qui
# fait les deux tics manquants sur `objet+0x240` (l'en-tete) et `objet+0x298`
# (le texte), puis saute dans la fonction d'origine. Le creneau 2 de la vtable
# pointe sur le relais.
# ---------------------------------------------------------------------------
# MENU CONSOLE, LA VRAIE CAUSE : une attente d'initialisation qui ne finit
# jamais, parce que son predicat est un bouchon.
#
# La mise a jour de la page de menu est UNE SEULE fonction, chainee sur trois
# entrees `.pdata` : 0x1801DC620, 0x1801DCE9D et 0x1801DD146. (0x1801DCE9D
# commence par `mov [rsp+0xd8], r12` : ce n'est pas un prologue.) Ne prendre
# que la premiere entree pour la fonction entiere induit en erreur -- erreur
# commise, puis corrigee, le 2026-09-03.
#
# Son debut :
#
#   0x1801DC6C2  cmp  byte [rdi+0x29FB], 0   ; drapeau "initialisation faite"
#   0x1801DC6C9  jne  0x1801DC709            ; deja faite -> le corps du menu
#   0x1801DC6CB  lea  rcx, [rbp+0x67]
#   0x1801DC6CF  call 0x180029FB0            ; <- BOUCHON : `mov al,1 ; ret`
#   0x1801DC6D4  test al, al
#   0x1801DC6D6  jne  0x1801DCE33            ; -> `xor al,al` = retour faux
#   0x1801DC6DC  ...                         ; JAMAIS ATTEINT :
#   0x1801DC6E3  mov  byte [rdi+0x29FB], 1   ;   poser le drapeau
#   0x1801DC709  ...                         ;   puis le corps du menu
#
# `0x180029FB0` est le jumeau des bouchons deja connus `0x180007450`
# (`xor al,al ; ret`) et `0x180007430` (`ret 0`) : il rend TOUJOURS 1, donc
# "encore occupe". Le menu attend donc une initialisation qui ne finira jamais,
# ne pose jamais son drapeau, et son corps ne tourne pas une seule fois.
#
# Mesure par jalons, sur une passe de 50 s dans le menu :
#     entree de la fonction        1844 passages
#     apres le `jne` de 0x1DC6D6      0 passages
#     sortie 0x1801DCE33           1289 passages
#     bloc des tics 0x1801DCE96       0 passages
#
# Cela explique LES DEUX symptomes d'un coup : pas de tic sur les scenes AET
# (le menu s'affichait vide) et pas de lecture des entrees (la navigation etait
# morte). Le relais de `--menu-console` soignait le premier en aval ; celui-ci
# s'attaque a la cause.
#
# Le correctif : neutraliser le `jne` de 6 octets, pour que l'initialisation
# aille au bout. Le bloc qu'elle traverse alors n'appelle que des bouchons
# (`0x180007430`) et ne lit pas le tampon que `0x180029FB0` aurait rempli.
MENU_INIT = (DLL, 0x1801DC6D6, bytes.fromhex('0F8557070000'),
             bytes.fromhex('909090909090'))

# ---------------------------------------------------------------------------
# MENU CONSOLE, deuxieme verrou : l'attente du CLASSEMENT.
#
# PERIME -- NE PLUS UTILISER. Remplace par `--sousmenu` le 2026-09-05.
# Le `jne` neutralise ici est la garde PARTAGEE des cinq sous-menus : la
# retirer laissait les directions traverser chaque sous-menu jusqu'au menu
# principal. La vraie cause etait le rangement de la page RANKING en
# `0x1801DCE2C`. Voir `analysis/menu_console.md` section 17.
#
# Une fois l'initialisation levee, la mise a jour du menu sort encore
# immediatement sur 1105 trames sur 1277. Jalons :
#
#     entree de la fonction   0x1DC620   1277 passages
#     apres le premier `je`   0x1DC6BB    172 passages
#     sortie `xor al,al`      0x1DCE33   1104 passages
#
# Le partage est des la troisieme instruction utile :
#
#   0x1801DC63D  mov  rcx, [rdi + 0x650]
#   0x1801DC644  test rcx, rcx
#   0x1801DC647  je   0x1801DC6BB      ; objet nul -> la suite du menu
#   0x1801DC649  call 0x180244EA0      ; "cette scene joue-t-elle encore ?"
#   0x1801DC650  jne  0x1801DCE33      ; oui -> retour faux
#
# Et `[menu+0x650]` est pose en `0x1801DCE2C` par `0x1801B0120`, qui charge la
# scene nommee **"RANKING"** (`0x180411948`). Le menu attend donc la fin d'une
# animation de CLASSEMENT -- qui, sur une borne sans reseau, n'a rien a jouer
# et ne se termine jamais.
#
# Meme remede que pour l'initialisation : neutraliser le `jne` de 6 octets.
MENU_RANKING = (DLL, 0x1801DC650, bytes.fromhex('0F85DD070000'),
                bytes.fromhex('909090909090'))

# ---------------------------------------------------------------------------
# MENU CONSOLE, troisieme verrou : le SERVICE que la borne ne fournit pas.
#
# L'attente du classement levee, plus aucune sortie anticipee (jalon 0x1DCE33 :
# 0 passage) et les tics tournent a chaque trame. Mais le corps interactif du
# menu reste saute : le jalon 0x1DC71F ne passe jamais, et 0x1DCE96 -- le bloc
# des tics, qui est aussi la sortie « pas de service » -- passe 1244 fois.
#
#   0x1801DC702  mov  rax, [0x180C3B6F0]
#   0x1801DC709  test rax, rax
#   0x1801DC70C  je   0x1801DCE96        ; pas d objet -> on saute le corps
#   0x1801DC712  cmp  qword [rax+0x1FE10], rsi
#   0x1801DC719  je   0x1801DCE96        ; pas de rappel -> idem
#   0x1801DC71F  ...                     ; LE CORPS : etat du menu, navigation
#
# `0x180C3B6F0` est pose par `module_start` depuis **`params+0x68`**, l'un des
# trois champs qu'APM3 ajoute aux 64 octets de YAMP. Le relevé au debogueur le
# montre alloue mais NON REMPLI : son premier qword est une vtable de
# `vfes.exe`, puis `AB AB AB AB ...`, le remplissage « non initialise » du tas
# de debogage. Le champ `+0x1FE10`, un pointeur de fonction, est donc nul.
#
# Autrement dit : la borne alloue le service que le menu console attend, et ne
# le branche pas. On neutralise les deux gardes de 6 octets ; le corps se garde
# lui-meme (`mov r9, [rax+0x1FE10] ; test r9, r9 ; je ...`) a chaque endroit ou
# il s'en sert reellement.
MENU_SERVICE = [
    (DLL, 0x1801DC70C, bytes.fromhex('0F8484070000'),
     bytes.fromhex('909090909090')),
    (DLL, 0x1801DC719, bytes.fromhex('0F8477070000'),
     bytes.fromhex('909090909090')),
]

# ---------------------------------------------------------------------------
# DURAL DANS LA GRILLE DE LA BORNE : quatre bornes a 18.
#
# Tout le reste est en place, verifie couche par couche (analysis/dural.md) :
#   * les donnees de combat sont completes -- 356 roles sur 363, mieux que TAK ;
#   * le tableau de la grille, lu EN MEMOIRE sur 384 passages, compte vingt
#     cases et la dix-neuvieme porte l'indice 20, c'est-a-dire Dural ;
#   * la planche `aet_s_selcha` de la borne est **identique au bit pres** a
#     celle de la console, et les calques de Dural y sont complets (portrait,
#     nom, style, animations `dur`/`dur_end`, quatre variantes, deux joueurs).
#
# Ne restait que le code. CORRECTION du 2026-09-04 : la note qui figurait ici
# donnait « dur = 19, rnd = 20 » dans une pretendue numerotation d'affichage.
# C'est FAUX, et les tables de disposition le disent en clair (voir plus bas,
# DURAL_GRILLE) : la table de la borne place le personnage **20** a la case 19,
# et il n'y a AUCUNE case « aleatoire » dans la grille de la borne. Le numero
# rendu par `0x180173AA0(selecteur, joueur)` -- c'est-a-dire `[case + 8]` --
# va de 0 a 20 :
#
#   aki sar lau shu jef pai jak kag lio wol aoi lei van bra goh mon msk krt tak
#    0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18
#   te2 dur
#    19  20            et 0x15 (21) = « aucun personnage »
#
# Les quatre sites ci-dessous bornent a **0x12 = 18** juste avant d'indexer les
# enregistrements de case (`imul .., 0x298`) : au-dela, la case est sautee et
# son descripteur reste vide. Ils excluent donc 19 ET 20 -- donc Dural.
#
#   0x18016EB2D  cmp eax,  0x12 ; jg   dans 0x18016E390
#   0x18016EC37  cmp eax,  0x12 ; jg   dans 0x18016E390
#   0x18016EEBA  cmp r15b, 0x12 ; ja   dans 0x18016E390, avant imul .., 0x298
#   0x180172391  cmp ebx,  0x12 ; ja   dans 0x180172300, le descripteur de case
#
# Il faut donc **0x14**, pas 0x13 : porter la borne a 0x13 n'ouvrait que TE2 et
# laissait Dural dehors. C'est ce que faisait `--dural-grille` jusqu'ici, ce
# qui explique qu'elle n'ait rien change quand on l'a essayee seule.
#
# Et c'est sans danger : le tableau d'enregistrements compte exactement VINGT
# ET UN elements. `0x180141EBA` lit `[rdx + 0x35A8]`, soit 0x298 * 21, le
# premier champ APRES le tableau. L'indice 20 est donc dans les bornes.
GRILLE_BORNES = [
    (DLL, 0x18016EB2D, bytes.fromhex('83F812'), 2),
    (DLL, 0x18016EC37, bytes.fromhex('83F812'), 2),
    (DLL, 0x18016EEBA, bytes.fromhex('4180FF12'), 3),
    (DLL, 0x180172391, bytes.fromhex('83FB12'), 2),
]

# ---------------------------------------------------------------------------
# WXGA : la variante d'affichage -- et la vraie raison de l'absence de Dural.
#
# La planche `aet_s_selcha` contient DEUX scenes, lues par tools/aet.py :
#
#     VGA_MAIN    113 compositions -- Dural : ZERO calque
#     WXGA_MAIN   174 compositions -- Dural : trois calques, comme les autres
#
# La grille de la borne ne « lie pas dix-neuf calques sur vingt » : elle charge
# la scene VGA, qui n'a pas de case Dural du tout. Cela explique du meme coup
# `spr_c_mchdurvga`, seule planche absente du registre des 862 actifs -- la
# variante VGA n'ayant pas de case Dural, son sprite VGA n'existe pas.
#
# Le choix des deux scenes tient a UN octet, `[0x1806490D0 + 0x20]`, lu a
# **54 endroits** de l'interface (par exemple `0x1801703F7`, qui decale un
# identifiant de scene de 0x149 a 0x14A). Il est en `.data`, vaut 0, et
# **aucune instruction ne l'ecrit** : c'est une constante de compilation.
WXGA = (DLL, 0x1806490D0 + 0x20, bytes.fromhex('00'), bytes.fromhex('01'))

# ---------------------------------------------------------------------------
# DURAL DANS LA GRILLE : deux appels a un predicat bouchonne.
#
# La grille de selection est la composition `chara_icon_name_base` de la
# planche `aet_s_selcmn` (SEL_COMMON), et elle existe en trois tailles :
#
#     VGA_MAIN    chara_icon_name_base       19 calques
#     WXGA_MAIN   chara_icon_name_base       20 calques
#     WXGA_MAIN   chara_icon_name_base_dur   21 calques   <- avec Dural
#
# Le moteur SAIT s'en servir : `0x18016DA30` porte les quatre noms en `_dur`
# (`chara_end_dur`, `chara_icon_name_out_dur`, `chara_icon_base_in_dur`,
# `chara_icon_name_in_dur`). Mais chacun est garde par le meme predicat :
#
#     0x18016DC69  call 0x180007450     ; `xor al,al ; ret` -- BOUCHON
#     0x18016DC8D  test al, al
#     0x18016DC8F  je   ...             ; toujours pris -> la variante SANS Dural
#
# `0x180007450` est le predicat « Dural est-elle debloquee ? » -- le meme qui
# garde la scene `UNLOCK_DURAL` (voir section 2 de analysis/dural.md). Il est
# bouchonne a FAUX dans ce build, et il a 210 appelants : on ne le patche donc
# pas lui, on remplace **les deux appels concernes** par `mov al, 1`.
#
# Ces compositions `_dur` n'existent que dans la scene WXGA : `--dural-grille`
# n'a de sens qu'avec `--wxga`.
#
# TROISIEME SITE, et c'est celui qui rend la case ATTEIGNABLE. Les deux
# premiers font DESSINER Dural -- verifie a l'ecran le 2026-09-04 : « dural
# s'affiche bien mais le curseur ne peut pas aller dessus ». La raison n'est
# pas une borne, c'est une desactivation explicite :
#
#     0x18016E20B  call 0x180007450     ; predicat bouchonne -> 0
#     0x18016E210  test al, al
#     0x18016E212  jne 0x18016E221      ; si VRAI : on ne desactive rien
#     0x18016E214  mov edx, 0x14        ; 20 = DURAL
#     0x18016E21C  call 0x180173F50     ; marque sa case [+0x14] = 1
#
# `0x180173F50(grille, perso)` parcourt la liste des cases et pose `1` en
# `+0x14` de celle dont le `+8` vaut `perso`. Or le deplacement du curseur
# (`0x180173110`) cherche la case voisine avec `cmp byte [rax+0x14], 0 ; jne
# suivante` : une case marquee est SAUTEE. La case existe, elle est dessinee,
# et le curseur passe a cote. Voir analysis/dural.md section 14.
DURAL_GRILLE = [
    (DLL, 0x18016DC69, bytes.fromhex('E8E297E9FF'), bytes.fromhex('B001909090')),
    (DLL, 0x18016E109, bytes.fromhex('E84293E9FF'), bytes.fromhex('B001909090')),
    (DLL, 0x18016E20B, bytes.fromhex('E84092E9FF'), bytes.fromhex('B001909090')),
]

# ---------------------------------------------------------------------------
# LA TRANSITION VERS LE MODE GAME -- deux liens a fabriquer, pas un.
#
# Constat du bilan (analysis/menu_console.md section 8) : le repartiteur d'etats
# n'a qu'une porte publique pour demander un mode, `0x1800DA9A0`, et une pour
# demander un sous-etat, `0x1800DA9C0`. On peut donc enumerer TOUTES les
# demandes du moteur. Resultat : le mode 2 `GAME` a ses trois gestionnaires
# vivants et **zero demandeur**. Idem pour le sous-etat 19 `VS` : rien ne le
# demande, sauf la sortie de `GAMEOVER` (le « rejouer »).
#
# Il manque donc DEUX maillons, et non un :
#
#     MENU  --(absent)-->  GAME/SELECTOR  --(absent)-->  VS
#
# Les deux fonctions de demande sont des feuilles de quatre instructions :
#     0x1800DA9A0(ecx) : [0x18070C4F4] = ecx ; [0x18070C500] = 1 ; [0x18070C51C] = 0
#     0x1800DA9C0(ecx) : [0x18070C510] = ecx ; [0x18070C51C] = 1
# et tous les appelants d'origine posent le mode PUIS le sous-etat. On fait
# pareil.
#
# ---------------------------------------------------------------------------
# MAILLON 1 -- l'entree SINGLE PLAYER du menu principal demande GAME/SELECTOR.
#
# Dans le repartiteur de validation `0x1801DDF30`, la branche de l'entree 0
# occupe 27 octets, de 0x1801DDF86 a 0x1801DDFA0 :
#
#     lea rbx, [rdi+0x658] / mov rcx, rbx / call 0x1801E48E0
#     lea rdx, "ARCADE MENU" / jmp 0x1801DE06C
#
# On y tient exactement les deux demandes (20 octets) plus un saut vers
# l'epilogue (5), et il reste deux octets a remplir. Pas besoin de caverne.
#
# Le sous-etat choisi est **17 SELECTOR**, et non 18 MODE_SELECTOR : c'est le
# seul dont on ait la preuve qu'il tourne. Mesure du 2026-09-04
# (analysis/machine_console.md section 5) : en posant les globaux a la main,
# `0x1800DCA90` (entree de SELECTOR) passe une fois et `0x1800DB270` (son
# milieu) 1326 fois. Et son milieu pilote l'objet `[0x180714928]` -- le
# selecteur de combat, celui-la meme dont on vient d'ouvrir la case de Dural.
#
# L'epilogue vise, 0x1801DDFDF, restaure `rbx` depuis [rsp+0x30] ; or `rbx` y
# est sauve a 0x1801DDF7D, AVANT notre code. Le saut est donc legitime.
TRANSITION_HOOK = 0x1801DDF86
TRANSITION_FIN = 0x1801DDFA1        # premiere adresse a ne pas toucher
TRANSITION_EPILOGUE = 0x1801DDFDF
TRANSITION_TETE = bytes.fromhex(
    '488d9f58060000488bcbe84b690000488d15444c3500e9cb000000')
DEMANDER_MODE = 0x1800DA9A0
DEMANDER_SOUS_ETAT = 0x1800DA9C0
MODE_GAME = 2
SOUS_ETAT_SELECTOR = 17             # 0x11
SOUS_ETAT_VS = 19                   # 0x13

# ---------------------------------------------------------------------------
# MAILLON 2 -- la fin du selecteur mene au combat au lieu de revenir au menu.
#
# `0x1800DB270` (milieu de SELECTOR) se termine ainsi, une fois la selection
# faite et non annulee :
#
#     0x1800DB372  cmp byte [0x180C3B701], al   ; game_mode != 0 (0 = console)
#     0x1800DB378  jne 0x1800DB438              ; borne : autre chemin
#     0x1800DB385  call 0x18016D360(objet)      ; selection terminee ?
#     0x1800DB38C  je  0x1800DB438
#     0x1800DB392  xor ecx, ecx ; call 0x180186D40
#     0x1800DB399  mov ecx, 4                   ; <-- ICI
#     0x1800DB39E  call 0x1800DA9A0             ; demande le mode 4 MENU
#
# Autrement dit, en mode console, terminer la selection **revient au menu**.
# C'est coherent avec un build ou le combat n'est jamais demande : la branche
# console de ce selecteur ne sert qu'a choisir un personnage et repartir.
#
# On remplace ces dix octets par « demander le sous-etat 19 VS », en restant
# dans le mode GAME. Les tailles coincident exactement : `mov ecx, imm32` fait
# cinq octets dans les deux cas, et les deux fonctions de demande sont
# voisines, donc le `call rel32` garde sa longueur.
#
# Portee du changement : cette branche n'est atteignable qu'en mode console
# (`game_mode == 0`) ET depuis le mode GAME -- c'est-a-dire, aujourd'hui,
# uniquement par le maillon 1. Les trois autres demandeurs de SELECTOR
# (`0x1800BABEC`, `0x1801E89BA`, `0x1800DABFA`) ne passent pas par la.
TRANSITION_VS_HOOK = 0x1800DB399
TRANSITION_VS_TETE = bytes.fromhex('b904000000e8fdf5ffff')

# ---------------------------------------------------------------------------
# MAILLON 3 -- creer l'objet de session avant d'entrer dans GAME.
#
# Premiere version : le jeu PLANTE. Journal Windows, et il donne l'adresse :
#
#     vfes.exe / vf5fs-pxd-w64-Retail_APM3.dll
#     Exception code: 0xC0000005 (violation d'acces)
#     Fault offset:   0x00000000000B1D33   ->  VA 0x1800B1D33
#
# En 0x1800B1D33 il y a une feuille de trois instructions, sans entree
# `.pdata` (d'ou l'utilite de `tools/plage.py`) :
#
#     0x1800B1D30  movsxd rax, edx
#     0x1800B1D33  movzx  eax, byte [rax + rcx + 0xC]     <-- ici
#     0x1800B1D38  ret
#
# C'est un accesseur `f(objet, indice)`. Il plante parce que `rcx` est NUL. Et
# l'appelant est justement le notre :
#
#     0x1800DCA90  ENTREE DU SOUS-ETAT 17 SELECTOR
#     0x1800DCA9D  call 0x1800B23A0     ; rend l'objet de session
#     0x1800DCAAE  mov  rbx, rax        ; sans le tester
#     0x1800DCAC7  call 0x1800B1D30     ; boum
#
# `0x1800B23A0` rend le singleton `[0x1806F9C18]`. Il est cree par
# `0x1800B3620(ecx)` -- qui alloue 0x16E0 octets --, et **l'entree du mode GAME
# (`0x1800DC7D0`) ne le cree pas**. Les cinq createurs sont ailleurs :
# `0x1801E5010` (entree de CS_TERM), `0x1801E2E80`, `0x180209DB0`,
# `0x18023A3C0` et `0x18023DF10` -- tous sur les chemins borne, terminal ou
# entrainement. Sur la borne, c'est le parcours APM3 qui le fabrique avant
# d'arriver au selecteur. Par le menu console, personne.
#
# Il manquait donc un TROISIEME maillon, et ce n'est pas une transition : c'est
# une CREATION. L'idiome exact est copie de `0x18023DFC0`, sur le chemin APM3 :
#
#     call 0x1800B23A0 ; test rax,rax ; jne deja
#     xor ecx, ecx     ; call 0x1800B3620
#   deja:
#
# `ecx` vaut 0 chez cet appelant, et `0x1800B3620` refuse tout ecx > 1.
#
# Ces 46 octets ne tiennent plus dans les 27 de la branche : on les pose dans
# la caverne de fin de `.text`, dans sa SECONDE moitie pour ne pas se marcher
# dessus avec le relais de `--menu-console` (52 octets, premiere moitie).
# ---------------------------------------------------------------------------
# MAILLON 4 -- apres le combat, revenir au MENU et non a l'ecran-titre.
#
# Mesure a l'ecran : le combat va jusqu'au bout, la chaine ne se rompt pas, et
# le jeu revient a l'ECRAN-TITRE. C'est la premiere des deux sorties de secours
# du milieu du mode GAME (`0x1800DA9D0`) qui a pris :
#
#     0x1800DA9DB  bl = 0x1801B6FE0()   ; drapeaux ctx+0x68C1 ET ctx+0x68C2
#     0x1800DA9E3  al = 0x1801B6E40()   ; le retour au MENU
#     0x1800DA9E8  test bl, bl ; je ...
#     0x1800DA9EC  xor ecx, ecx ; call 0x1800DA9A0   ; mode 0 STARTUP
#     0x1800DA9F3  mov ecx, 3   ; call 0x1800DA9C0   ; sous-etat 3 CS_TITLE
#     0x1800DAA25  test al, al ; je ...
#     0x1800DAA29  mov ecx, 4   ; call 0x1800DA9A0   ; mode 4 MENU
#
# Et le retour au menu ne pouvait de toute facon pas gagner : `0x1801B6E40` se
# termine par
#
#     0x1801B6E8E  call 0x180007450   ; BOUCHON -> 0
#     0x1801B6E95  je   ...           ; toujours pris -> rend FAUX
#     0x1801B6E97  mov  al, 1         ; jamais atteint
#
# Le meme mal que la case de Dural : un dernier verrou bouchonne. On ne touche
# pas a ce predicat -- il a quatre appelants. On corrige **la branche**, la ou
# la portee est nulle : le mode 2 GAME n'a AUCUN demandeur dans tout le moteur
# en dehors de notre caverne (enumeration des 27 demandes de mode, section 8 de
# menu_console.md). `0x1800DA9D0` ne tourne donc que sur notre parcours.
#
# On remplace les 17 octets de la branche « titre » par la branche « menu »,
# copiee de `0x1800DAA29` : mode 4, sans sous-etat -- c'est l'entree du mode
# MENU qui pose le sien.
RETOUR_MENU_HOOK = 0x1800DA9EC
RETOUR_MENU_FIN = 0x1800DA9FD
RETOUR_MENU_TETE = bytes.fromhex('33c9e8adffffffb903000000e8c3ffffff')
MODE_MENU = 4

# ---------------------------------------------------------------------------
# MAILLON 6 -- eteindre le menu quand on entre en combat.
#
# Mesure a l'ecran, OFFLINE VERSUS : les deux curseurs bougent bien separement
# (le joueur 2 fonctionne), mais **ils pilotent en meme temps le menu principal
# reste en arriere-plan**, et plus rien ne valide.
#
# La sortie du mode MENU (`0x1800DCB80`) demonte bien les trois taches du menu
# (0x208, 0x268, 0x269, posees par son entree `0x1800DCBF0`) -- mais seulement
# sous condition :
#
#     0x1800DCB90  call 0x1801B7010
#     0x1800DCB95  test al, al
#     0x1800DCB97  jne  0x1800DCB9E     ; vrai : on demonte
#     0x1800DCB99  add rsp, 0x28 ; ret  ; faux : ON NE DEMONTE RIEN
#
# et `0x1801B7010` rend « l'objet `0x180752000` n'est PAS occupe ». Quand on
# entre en combat depuis la validation d'une page encore ouverte, il l'est --
# le menu n'est donc jamais demonte, ses taches continuent de tourner et de
# consommer les entrees.
#
# Noter aussi que la sortie rend alors `al = 0`, c'est-a-dire « pas fini » : le
# repartiteur la rappelle a chaque trame, et la transition reste en suspens.
#
# On rend le demontage inconditionnel. La semantique est sans ambiguite --
# quitter le mode MENU doit retirer les taches du menu -- et la portee est
# celle du parcours console, seul a emprunter ce mode ici.
MENU_FERMER = (DLL, 0x1800DCB95, bytes.fromhex('84c07505'),
               bytes.fromhex('9090eb05'))      # nop nop ; jmp 0x1800DCB9E

# ---------------------------------------------------------------------------
# EXIT GAME : la dixieme entree du menu, ecrite puis effacee par le moteur.
#
# Demande de Frederic : une ligne « EXIT GAME » en bas du menu pour revenir
# sous Windows. Elle existe DEJA -- libelle 0x183, scene de confirmation
# `EXIT_CAUTION` (0x180532C78), texte 0x3EE -- et tout son chemin est intact.
# UNE seule chose l'empeche d'apparaitre, et le moteur la fait expres :
#
#     0x1801E39D0  mov dword [rbx+0x224], 9    ; DERNIER INDICE (pas un compte)
#     0x1801E39E6  mov qword [rbx+0x642], 0    ; etats 0..7 : normal
#     0x1801E39F1  mov word  [rbx+0x64A], 0    ; etats 8 et 9 : normal AUSSI
#     0x1801E3A13  mov byte  [rbx+0x64B], 2    ; ... puis on RECACHE la 9
#
# L'etat vit dans `page + 0x642 + i` : `0` normal, `1` grise, `2` pas dessine.
# L'entree 9 est mise a 0 puis remise a 2 : c'est le SEUL octet a changer.
#
# PIEGE, paye a l'ecran le 2026-09-05. `[page+0x224]` n'est PAS le nombre
# d'entrees mais le **dernier indice** -- la boucle de dessin le prouve :
#
#     0x1801E0EFF  cmp dword [rsi+0x224], edi   ; edi = l indice
#     0x1801E0F05  jl  fin                      ; on sort quand count < i
#     ...
#     0x1801E1079  cmp edi, dword [rsi+0x224]
#     0x1801E107F  jle boucle                   ; i va de 0 a count INCLUS
#
# A 9, dix rangees etaient donc deja dessinees, la dixieme etant cachee par
# son etat. L'avoir porte a 10 ajoutait une ONZIEME rangee, qui lisait le
# tableau de libelles (dix entrees, `rbp-0x50` a `rbp-0x2C`) hors bornes :
# l'identifiant tombait a 0, soit « :Enter ». Frederic : « une ligne
# inutile "enter" est apparue juste au dessous ». Cet octet est retire.
#
# Ce que fait la validation, deja ecrit et NON bouchonne (c'est rare ici) :
#
#     0x1801DE18E  scene "EXIT_CAUTION", texte 0x3EE  ; le dialogue oui/non
#     0x1801DCEDB  call 0x1801BCE90                   ; la reponse
#     0x1801DCEE9  js sortie                          ; <0 : pas encore repondu
#     0x1801DCEF6  jne ailleurs                       ; !=0 : NON
#     0x1801DCEF8  cmp dword [rdi+0x58], 9            ; <- l entree 9, en dur
#     0x1801DCF09  call 0x1801DB8B0                   ; demontage des scenes
#     0x1801DCF0E  mov byte [rdi+0x641], 1            ; « le menu est fini »
#
# Le `cmp ..., 9` prouve a lui seul que l'entree 9 EST « EXIT GAME ».
#
# Mais le moteur n'a AUCUNE sortie de processus : sur borne, un jeu ne se
# ferme pas, c'est l'hote qui coupe. Les seuls `ExitProcess` du moteur sont
# ceux de la bibliotheque C. `vfes.exe` importe bien `Core_exitGame` et
# `Core_isExitNeeded` de `apm.dll` -- notre stub, qui les rend a 0 -- mais le
# moteur ne les atteint pas depuis le menu.
#
# On branche donc la derniere marche : la ou le moteur ecrit « le menu est
# fini » (entree 9 confirmee, demontage deja fait), on appelle `ExitProcess`,
# que la DLL importe deja (IAT 0x180346318). Douze octets contigus sont
# disponibles -- l'ecriture du drapeau (7) et le saut de sortie (5) -- donc
# AUCUNE caverne n'est consommee :
#
#     c6 87 41 06 00 00 01 e9 20 02 00 00     avant
#     33 c9 ff 15 02 94 16 00 90 90 90 90     apres
#      \____/  \_______________/  \________/
#     ecx = 0   call [ExitProcess]  remplissage
#
# `ExitProcess` ne revient pas ; si jamais elle revenait, les `nop` menent a
# `0x1801DCF1A`, une frontiere d'instruction valide. Le reste du menu est
# intact : l'entree 9 ne se valide que par son dialogue.
# ---------------------------------------------------------------------------
# L'ECRAN D'AVERTISSEMENT SUR L'EPILEPSIE (le 4e au demarrage).
#
# Demande de Frederic. C'est le sous-etat **WARNING**, cle 2 de la table
# `0x1803A05A0` -- son nom est en `0x1803A0F28`, et son texte est
# l'identifiant 0x36C de `string_array` :
#
#   « All unsaved... » non : « A very small percentage of people may experience
#   a seizure when exposed to certain visual images... »  (resolu en 0x18006C4FE)
#
# Ses trois gestionnaires :
#
#     entree  0x1800DE510   demarre la scene AET "WARNING"
#     milieu  0x1800DD7C0   `call 0x180244EA0 ; sete al` -- « fini quand elle
#                           ne joue plus »
#     sortie  0x1800DDAF0   detruit la scene
#
# Le moteur a DEJA son chemin de saut, et c'est un bouchon qui le ferme :
#
#     0x1800DE514  call 0x180007450     ; BOUCHON -> toujours faux
#     0x1800DE51B  jne  0x1800DE538     ; vrai -> on sort SANS demarrer la scene
#     0x1800DE525  ...  "WARNING" -> 0x180245830
#
# On rend ce saut inconditionnel. La scene n'est jamais demarree ; le milieu
# demande alors a `0x180244EA0` si une scene absente joue encore, obtient non,
# et rend « fini » des la premiere trame. L'etat s'enchaine tout seul.
#
# Portee : l'objet de scene `0x18070C530` n'a que QUATRE lecteurs dans tout le
# moteur, dont les trois gestionnaires de WARNING. Aucun autre ecran ne s'en
# sert. Et la sortie detruit une scene absente sans broncher -- c'est le
# `0x1802450A0` de tout le monde.
SANS_AVERTISSEMENT = (DLL, 0x1800DE51B, bytes.fromhex('751b'),
                      bytes.fromhex('eb1b'))      # jne -> jmp

# ---------------------------------------------------------------------------
# ... SAUF QUE CE N'EST PAS CET ECRAN-LA. Essai fait le 2026-09-05, dementi a
# l'ecran : « l'ecran warning est toujours present ». Le sous-etat WARNING
# existe et son saut fonctionne, mais l'avertissement sur l'epilepsie n'est
# pas dessine par lui.
#
# L'ECRAN D'EPILEPSIE, pour de vrai.
#
# Le texte est l'identifiant 0x36C, resolu en `0x18006C4FE`. Cette fonction,
# `0x18006C490`, n'est appelee par personne : son adresse est le creneau
# **+0x20** (le DESSIN) d'une vtable en `0x18034CB90`, posee en `0x18000194A`
# sur un singleton statique -- l'objet `0x180677040`.
#
# Cet objet joue toute la presentation de demarrage. Sa mise a jour (creneau
# +0x10, `0x18006B880`) est une machine a DOUZE phases sur `[obj+0x58]`, et ces
# phases font du VRAI chargement :
#
#     4  "EFFEFFCMN", "STGCMN", "NAGE_VF4", "rom/sound/se_system.csb"
#     8  "rom/sound/se_tv_cmn.csb"
#    10  "rom/sound/se_terminal.csb"
#
# Le sous-etat qui l'heberge s'appelle d'ailleurs `DATA_INITIALIZE` -- c'est
# l'ECRAN DE CHARGEMENT. Sauter ses phases, ce serait sauter le chargement.
# On ne touche donc pas a la machine : on retire seulement le DESSIN du texte.
#
# Sa garde est en tete du creneau +0x20 :
#
#     0x18006C4B6  mov  ecx, [rcx + 0x58]    ; la phase
#     0x18006C4B9  cmp  ecx, 1
#     0x18006C4BC  jbe  0x18006C803          ; <- l'epilogue
#     0x18006C4D7  cmp  ecx, 3
#     0x18006C4DA  jle  0x18006C803
#     0x18006C4FE  mov  ecx, 0x36C           ; le texte, a partir de la phase 4
#
# On saute a l'epilogue sans condition. Douze octets, et le prologue est
# conserve -- c'est indispensable : `0x18006C803` restaure `rbx`, `xmm6` et
# 0x110 octets de pile. Court-circuiter la fonction depuis son entree
# corromprait la pile.
#
# ETAT : le texte part bien -- verifie a l'ecran le 2026-09-05. Il reste alors
# un ECRAN BLANC, celui de la scene AET "DATA_INITIALIZE" demarree en
# `0x18006C9E2`. Retirer aussi ce fond a ete essaye puis ANNULE : rien ne dit
# encore ce que cet ecran doit devenir, et Frederic a arrete l'essai. L'option
# n'enleve donc QUE le texte, et elle n'est dans aucun lanceur.
SANS_EPILEPSIE = [
    (DLL, 0x18006C4B6,
     bytes.fromhex('8b4958' '83f901' '0f8641030000'),
     bytes.fromhex('e948030000') + bytes.fromhex('90') * 7),
]

# ---------------------------------------------------------------------------
# OPTIONS : le raccourci de borne detourne toutes les validations.
#
# Constat de Frederic : « je n'arrive plus a valider les sous/sous menus a part
# credits ». Mesure (tools/pister_scene.py, 2026-09-05) :
#
#     GARDE  validation=1  entree=5      <- quatre fois, TOUJOURS 5
#     L0 How to Play 0 | L1 Controls 0 | L2 Settings 0 | L3 Save Data 0
#     L5 Info 4
#
# et AUCUN demarrage de scene n'echoue (44 appels, 44 fois OK). L'aiguillage ne
# voit donc jamais que le cas 5, `OPTION INFO` -- ce que Frederic appelle
# « credits ».
#
# La cause est dans la mise a jour de la liste des options :
#
#     0x1801A7C75  cmp  dword [0x1807513B8], 0  ; type == 0 -> chemin console
#     0x1801A7C7C  jne  0x1801A7CDD             ; sinon : navigation normale
#     0x1801A7C8E  lea  ecx, [rdx+1]            ; masque 1, le BIT 0
#     0x1801A7C91  call 0x1801A2CA0             ; ce bouton est-il TENU ?
#     0x1801A7C98  js   0x1801A7CDD             ; personne -> navigation
#     0x1801A7CA8  mov  dword [rbx+0x58], 5     ; <- sinon on FORCE l'entree 5
#     0x1801A7CD4  mov  byte  [rbx+0x2F0], 1    ;    et on valide
#
# C'est un raccourci de borne : tenir un bouton ouvre la page d'informations.
# Mais le bit 0, d'apres la table des entrees (menu_console.md 10.2), c'est
# **Entree (START, code 7)** -- la touche meme avec laquelle on valide. Toute
# validation tient donc le bit 0 dans la meme trame, et part sur l'entree 5.
#
# Quels boutons agissent ici, etabli le 2026-09-05 (essai de Frederic : « seul A
# fonctionne dans le menu, T et R non », puis « A a la fonction annule »,
# « ENTREE : valider »). Le curseur partage interroge deux predicats, chacun ne
# lisant qu'UN code, et appelle deux creneaux distincts :
#
#     0x1801BBCC6  call 0x1801A2B90  (code 8 = A)       -> creneau +0x48 ANNULER
#     0x1801BBCDD  call 0x1801A2BC0  (code 7 = Entree)  -> creneau +0x50 VALIDER
#
# `T` et `R` ne sont lus par personne dans ces menus. Et la table du 10.2 de
# `menu_console.md` (bits 0 a 3 = « grille : VALIDER ») ne vaut que pour la
# GRILLE de selection, qui lit le masque arcade brut.
#
# D'ou le defaut : **Entree valide, et Entree est le bit 0**. Au moment meme ou
# elle valide, elle est TENUE -- le raccourci se declenche et detourne vers
# l'entree 5. C'est ce que la mesure montrait : `entree=5` quatre fois sur
# quatre. Sur borne le geste peut etre distinct ; au clavier il ne peut pas.
#
# On rend le saut inconditionnel : la navigation ordinaire reprend et le
# raccourci disparait. Deux octets, `75` -> `eb`.
OPTIONS_RACCOURCI = (DLL, 0x1801A7C7C, bytes.fromhex('755f'),
                     bytes.fromhex('eb5f'))          # jne -> jmp

# ---------------------------------------------------------------------------
# UNE QUATRIEME LIGNE AU DOJO : « How to Play ».
#
# Demande de Frederic : « deplace How to Play vers DOJO », puis « tu ajoutes
# une ligne, ne remplace rien ». Les trois lignes existantes restent intactes :
#
#     0  Tutorial          (0x217)  page 0x180754A70 -- vivante
#     1  Command Training  (0x218)  scene COMMAND_TRAINING MENU
#     2  Free Training     (0x219)  ferme le menu et lance l'entrainement
#
# La page du menu Dojo : vtable 0x180532968, init 0x1801E4420, dessin
# 0x1801E1E40, valider 0x1801DE440.
#
# Quatre gestes, et deux cavernes.
#
# 1. LE COMPTE. `0x1801E444B mov dword [rdi+0x224], 2` -> 3. Comme ailleurs,
#    `+0x224` est le DERNIER INDICE, pas un compte : 3 donne quatre lignes.
#
# 2. LE LIBELLE. Le dessin pose ses trois identifiants sur la pile, et la
#    boucle les parcourt par `lea r14, [rsp+0x40]` :
#
#        0x1801E1E8A  mov dword [rsp+0x40], 0x217
#        0x1801E1E92  mov dword [rsp+0x44], 0x218
#        0x1801E1E9A  mov dword [rsp+0x48], 0x219
#
#    `[rsp+0x4C]` est libre PENDANT la boucle -- il n'est reutilise qu'apres
#    (`0x1801E221E vmovss [rsp+0x4C], xmm0`). On y ecrit 0x2F1, « How to Play »,
#    depuis une caverne, faute de dix octets sur place.
#
# 3. L'AIGUILLAGE. `0x1801DE440` teste `[rbx+0x58]` : 1 -> Command Training,
#    0 -> Tutorial, le reste -> fermeture (Free Training). On detourne l'entree
#    de ce test pour intercepter le 3.
#
# 4. LE RELAIS. Pour le 3, on ouvre la page d'options par sa fabrique
#    `0x1801AB3A0(0, 0, 0)`, on lui presele l'entree 0 (`[page+0xB8] = 0`,
#    `[page+0xC0] = 1` : c'est exactement ce que la page attend, voir
#    `carte_options.md`), et on range la page dans `[menu+0x2F8]` -- le meme
#    champ que Command Training, pour que le menu Dojo se suspende comme il
#    sait deja le faire.
#
# LES CAVERNES. Celle de `.text` n'a plus que 23 octets contigus a
# `0x180345785` : elle prend le libelle (19 octets). Le relais, lui, tient dans
# les **82 octets du raccourci desactive** par `--options-raccourci`,
# `0x1801A7C89`-`0x1801A7CDB` : plus rien ne peut les atteindre depuis que
# `0x1801A7C7C` est un saut inconditionnel. D'ou la dependance : `--dojo-howto`
# EXIGE `--options-raccourci`.
DOJO_HOWTO_COMPTE = (DLL, 0x1801E4451, bytes.fromhex('02'), bytes.fromhex('03'))
DOJO_HOWTO_CAVE_A = 0x180345785
DOJO_HOWTO_CAVE_A_MAX = 0x18034579C - 0x180345785
DOJO_HOWTO_HOOK_A = 0x1801E1EA2
DOJO_HOWTO_HOOK_A_TETE = bytes.fromhex('c5f857c0' 'c5fa1144' '2430')
DOJO_HOWTO_CAVE_B = 0x1801A7C89
DOJO_HOWTO_CAVE_B_MAX = 0x1801A7CDC - 0x1801A7C89
DOJO_HOWTO_HOOK_B = 0x1801DE461
DOJO_HOWTO_HOOK_B_TETE = bytes.fromhex('8b4358' '83f801')
HOWTO_LIBELLE = 0x2F1              # « How to Play »
OPTIONS_FABRIQUE = 0x1801AB3A0
# Les huit premiers octets du corps du raccourci, pour que le REFUS serve :
# `xor edx,edx ; mov sil,1 ; lea ecx,[rdx+1]` -- si ce n'est pas ca, la
# caverne n'est pas celle qu'on croit.
RACCOURCI_CORPS = bytes.fromhex('33d240b6018d4a01')


def dojo_howto_cave_a():
    """Pose le quatrieme libelle, puis refait les deux instructions deplacees.

    On est appele : `rsp` est huit octets plus bas qu'au site, d'ou les
    decalages `+8` sur les deux emplacements de pile.
    """
    c = bytes.fromhex('c7442454') + struct.pack('<I', HOWTO_LIBELLE)
    c += bytes.fromhex('c5f857c0')                 # vxorps xmm0, xmm0, xmm0
    c += bytes.fromhex('c5fa11442438')             # vmovss [rsp+0x38], xmm0
    c += bytes.fromhex('c3')
    if len(c) > DOJO_HOWTO_CAVE_A_MAX:
        raise AssertionError('caverne A du dojo debordee : %d > %d'
                             % (len(c), DOJO_HOWTO_CAVE_A_MAX))
    return c


def dojo_howto_cave_b():
    """Intercepte l'entree 3 et ouvre « How to Play » ; sinon rend la main."""
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    a = DOJO_HOWTO_CAVE_B
    c = bytes.fromhex('8b4358')                    # mov eax, [rbx+0x58]
    c += bytes.fromhex('83f803')                   # cmp eax, 3
    c += bytes.fromhex('7408')                     # je nous  (+16)
    c += bytes.fromhex('83f801')                   # cmp eax, 1  (les flags rendus)
    c += bytes.fromhex('e9') + rel(a + len(c) + 5, 0x1801DE467)
    assert len(c) == 16
    c += bytes.fromhex('4533c0')                   # xor r8d, r8d   drapeau = 0
    c += bytes.fromhex('33d2')                     # xor edx, edx   type = 0
    c += bytes.fromhex('33c9')                     # xor ecx, ecx   mode = 0
    c += bytes.fromhex('e8') + rel(a + len(c) + 5, OPTIONS_FABRIQUE)
    c += bytes.fromhex('4885c0')                   # test rax, rax
    c += bytes.fromhex('741b')                     # je echec  (+60)
    c += bytes.fromhex('33c9')                     # xor ecx, ecx
    c += bytes.fromhex('8988b8000000')             # mov [rax+0xB8], ecx   entree 0
    c += bytes.fromhex('c680c000000001')           # mov byte [rax+0xC0], 1  valide
    c += bytes.fromhex('488983f8020000')           # mov [rbx+0x2F8], rax
    c += bytes.fromhex('e9') + rel(a + len(c) + 5, 0x1801DE4C0)
    assert len(c) == 60
    c += bytes.fromhex('e9') + rel(a + len(c) + 5, 0x1801DE4CC)
    if len(c) > DOJO_HOWTO_CAVE_B_MAX:
        raise AssertionError('caverne B du dojo debordee : %d > %d'
                             % (len(c), DOJO_HOWTO_CAVE_B_MAX))
    return c


def dojo_howto_hook_a():
    return (bytes.fromhex('e8')
            + struct.pack('<i', DOJO_HOWTO_CAVE_A - (DOJO_HOWTO_HOOK_A + 5))
            + bytes.fromhex('90') * 5)


def dojo_howto_hook_b():
    return (bytes.fromhex('e9')
            + struct.pack('<i', DOJO_HOWTO_CAVE_B - (DOJO_HOWTO_HOOK_B + 5))
            + bytes.fromhex('90'))


# ---------------------------------------------------------------------------
# RETIRER « How to Play » DES OPTIONS, une fois posee au Dojo.
#
# Demande de Frederic, apres avoir vu la quatrieme ligne du Dojo fonctionner :
# « bien sur que si il faut enlever how to play de options ».
#
# La liste passe de cinq lignes a quatre, et tout se decale d'un cran :
#
#     avant                        apres
#     0 How to Play  (0x2F1)       0 Controls   (0x2F2)
#     1 Controls     (0x2F2)       1 Settings   (0x2F3)
#     2 Settings     (0x2F3)       2 Save Data  (0x2F4)
#     3 Save Data    (0x2F4)       3 Credits    (0x2F5)
#     4 Credits      (0x2F5)
#
# Trois familles d'octets, aucune caverne :
#
# 1. LES LIBELLES, poses par le dessin `0x1801A9DC0` : on decale les quatre
#    premiers d'un cran. Les cinquieme et sixieme emplacements deviennent
#    inutiles ; on les laisse.
#
# 2. LA BORNE, dans l'init `0x1801AAFF0` : `mov eax, 4` -> 3. Comme partout,
#    `+0x224` est le DERNIER INDICE.
#
# 3. L'AIGUILLAGE, dans la mise a jour `0x1801A6F70`. Le cas 0 menait a
#    `OPTION HOWTO` : on rend son `jne` inconditionnel, ce qui le saute. Puis
#    chaque `cmp` recule d'un :
#
#        0x1801A703B  jne  -> jmp        (l'entree 0 n'est plus How to Play)
#        0x1801A707F  cmp eax, 1 -> 0    Controls
#        0x1801A70D1  cmp eax, 2 -> 1    Settings
#        0x1801A7117  cmp eax, 3 -> 2    Save Data
#        0x1801A715D  cmp eax, 5 -> 3    OPTION INFO (les credits)
#
#    Le cas 4 (`0x1801A71D8`, la fabrique `0x1801B11C0`) devient inatteignable ;
#    on n'y touche pas.
#
# Le contenu de « How to Play » n'est PAS supprime : la scene `OPTION HOWTO` et
# son sous-objet restent en place, et c'est le relais du Dojo (`--dojo-howto`)
# qui les ouvre desormais.
OPTIONS_SANS_HOWTO = [
    (DLL, 0x1801A9E06, bytes.fromhex('f1020000'), bytes.fromhex('f2020000')),
    (DLL, 0x1801A9E0E, bytes.fromhex('f2020000'), bytes.fromhex('f3020000')),
    (DLL, 0x1801A9E16, bytes.fromhex('f3020000'), bytes.fromhex('f4020000')),
    (DLL, 0x1801A9E1E, bytes.fromhex('f4020000'), bytes.fromhex('f5020000')),
    (DLL, 0x1801AB03F, bytes.fromhex('04'), bytes.fromhex('03')),
    (DLL, 0x1801A703B, bytes.fromhex('75'), bytes.fromhex('eb')),
    (DLL, 0x1801A7080, bytes.fromhex('01'), bytes.fromhex('00')),
    (DLL, 0x1801A70D2, bytes.fromhex('02'), bytes.fromhex('01')),
    (DLL, 0x1801A7118, bytes.fromhex('03'), bytes.fromhex('02')),
    (DLL, 0x1801A715E, bytes.fromhex('05'), bytes.fromhex('03')),
]

# ---------------------------------------------------------------------------
# LE CADRE DU SOUS-MENU DOJO : emprunter celui des OPTIONS.
#
# Avec sa quatrieme ligne, « How to Play » deborde du cadre. Celui-ci ne se
# redimensionne pas : `[obj+0x224]` n'est lu que par la boucle de dessin, et le
# dessin du Dojo (`0x1801E1E40`) ne contient aucune geometrie de cadre -- rien
# que la taille du texte (32.0), deux decalages (3.0, 4.0) et deux ancres.
# Le cadre vient donc de la scene AET.
#
# Idee de Frederic : « au pire tu prends la sous fenetre de OPTIONS qui a la
# bonne taille pour le coup ». La scene `OPTION MENU` est taillee pour CINQ
# lignes ; le Dojo en a quatre. On la lui donne.
#
# Deux scenes, deux ancres. Le dessin des OPTIONS demande `p_small_head_lt` et
# `p_txt_01_lt` ; celui du Dojo `head_tit_ct` et `p_txt_01_lt`. La seconde est
# commune, la premiere non : il faut donc changer AUSSI l'ancre du Dojo, sinon
# il chercherait dans `OPTION MENU` un calque qui n'y est pas.
#
# Trois `lea` redirigees, douze octets, aucune caverne :
#
#     0x1801DE048  "TRAINING MENU" -> "OPTION MENU"     l'ouverture
#     0x1801E3DD1  "TRAINING MENU" -> "OPTION MENU"     la fermeture (la tache
#                                                       choisit la scene a fermer)
#     0x1801E1EEF  "head_tit_ct"   -> "p_small_head_lt" l'ancre du titre
#
# Les deux sites de scene doivent bouger ENSEMBLE : s'ils divergent, la scene
# ouverte n'est pas celle que la tache cherche a fermer.
DOJO_CADRE = [
    (DLL, 0x1801DE04B, bytes.fromhex('b14b3500'), bytes.fromhex('b1302300')),
    (DLL, 0x1801E3DD4, bytes.fromhex('28ee3400'), bytes.fromhex('28d32200')),
    (DLL, 0x1801E1EF2, bytes.fromhex('92f42200'), bytes.fromhex('eaed2200')),
]

# ---------------------------------------------------------------------------
# SINGLE PLAYER : que les quatre modes LANCENT le combat.
#
# `--sp-menu` a rendu le sous-menu (Arcade, Score Attack, License Challenge,
# Special Sparring) mais, comme prevu, plus rien ne mene au combat : aucun site
# du moteur ne demande le mode GAME (enquete exhaustive du 2026-09-04).
#
# La chaine native s'arrete a un endroit precis. Choisir un mode ouvre sa page
# de reglages (`NORMAL MENU` pour Arcade, `[modes+0x300]`), dont la validation
# `0x1801DDE80` ne fait que refermer. Le parent, la mise a jour de la page des
# modes, s'en apercoit ici :
#
#     0x1801DBEF2  call 0x1801A5B80   ; la sous-page a-t-elle ete VALIDEE ?
#     0x1801DBEF7  test al, al
#     0x1801DBEF9  je   0x1801DBF28   ; non -> on attend
#     0x1801DBEFB  ...                ; oui -> on referme, et plus rien ne suit
#
# C'est le jumeau exact du maillon d'OFFLINE VERSUS (`0x1801DEB12`), ou l'on
# avait remplace « enregistrer les reglages » par « enregistrer PUIS lancer ».
# Ici on interpose un relais sur le predicat : il rend la meme reponse, et
# quand elle est OUI il appelle en plus la caverne de transition -- celle qui
# cree la session et demande GAME/SELECTOR.
#
# Le relais tient dans une caverne NEUVE : depuis `--options-sans-howto`, le
# cas « How to Play » du repartiteur des options est inatteignable (son `jne`
# est devenu `jmp`), ce qui libere `0x1801A703D`-`0x1801A707D`, soit 65 octets.
#
# D'ou trois dependances : `--transition-game` (la caverne), `--sp-menu` (sans
# quoi le sous-menu est court-circuite et le relais inutile) et
# `--options-sans-howto` (sans quoi le bloc est encore execute).
# MESURE du 2026-09-05 (tools/pister_sp.cmd) : la page de reglages s'ouvre bien
# (`SCENE DU MODE demarree : OUI`, sous-page rangee puis effacee 1,4 s plus
# tard), mais la fermeture passe par le PREMIER des deux tests d'identite, qui
# saute le site que j'avais choisi -- 0 passage. Et on ne peut pas se greffer
# sur la fermeture commune : **valider et annuler sont indiscernables**, les
# deux posant `[page+0x308] = 1`, et ne differant que par le son joue
# (`0x1801BC010` valider, `0x1801BB9D0` annuler).
#
# On se greffe donc DANS chaque validateur, qui ne s'execute que sur
# « valider ». C'est la forme du maillon d'OFFLINE VERSUS.
#
# LE MODE DE JEU. Frederic, a l'ecran : « Score Attack et License Challenge
# lancent le mode arcade mais pas leur vrai mode ». Le mode de jeu est le dword
# global **`0x180751010`**, premiere case d'un bloc de reglages de partie de
# seize octets. Huit references dans tout `.text`, balayage lineaire :
#
#     0x18019C090  lecture           0x18019C1F8  lecture
#     0x18019C372  = 9               0x18019C3D2  ecriture
#     0x18019C426  ecriture          0x18019C490  ecriture   <- le poseur
#     0x18019C4A8  ecriture          0x18019C522  ecriture
#
# `0x18019C490` est une feuille d'une seule instruction :
#
#     0x18019C490  mov dword [0x180751010], ecx
#     0x18019C496  ret
#
# Les valeurs : 0 Arcade, 1 Score Attack, 2 License Challenge, 3 Special
# Sparring, 4 Versus. Le binaire le dit lui-meme : `0x1800B8B9F cmp eax,3 ; ja`
# -- au-dessus de 3, on ne lit plus les reglages solo.
#
# Pourquoi tout partait en Arcade : la chaine native pose le mode dans la MISE
# A JOUR de la page, plusieurs trames apres la validation, une fois l'animation
# de sortie finie. Notre caverne lance immediatement : l'ecriture n'avait
# jamais lieu, et le global restait a 0.
#
# D'ou une caverne PAR MODE, chacune posant sa valeur avant de lancer :
#
#     sub rsp, 0x28
#     call 0x1801BC010      ; l'appel deplace -- rcx est encore la page
#     push N ; pop rcx      ; le mode
#     call 0x18019C490      ; le poser
#     call TRANSITION_CAVE  ; session + GAME/SELECTOR
#     add rsp, 0x28 ; ret
#
# Elles tiennent dans les deux blocs morts liberes par `--options-sans-howto` :
# le cas « How to Play » (`0x1801A703D`, 65 octets) et le cas « Credits » par
# la fabrique (`0x1801A71D8`, 37 octets), tous deux devenus inatteignables.
#
# PIEGE CONNU, non corrige : `0x1800A48A0`, le validateur de Score Attack, est
# cite par **trois** vtables (`0x18039A160`, `0x1805326C8`, `0x180532728`). La
# greffe s'y declenche donc pour les trois classes. Si un combat se lance
# depuis un ecran inattendu, c'est de la.
SP_MODE_POSER = 0x18019C490          # mov [0x180751010], ecx ; ret
SP_SON_VALIDER = 0x1801BC010
SP_LANCER_BLOC_A = (0x1801A703D, bytes.fromhex('8b8360150000'))   # cas How to Play
SP_LANCER_BLOC_B = (0x1801A71D8, bytes.fromhex('83f80475208b8b'))  # cas Credits
# (caverne, mode, site de greffe, octets attendus au site, nom)
# CORRECTION du 2026-09-05, apres essai : « score attack plante au debut du
# combat et ne semble pas etre le score attack ». Il y a DEUX poseurs voisins,
# et j'avais pris le mauvais :
#
#     0x18019C490  mov [0x180751010], ecx ; ret        <- le mode SEUL
#     0x18019C4A0  mov [0x180751010], ecx              <- le mode ET le bloc
#                  mov [0x180751014], 0 ... [0x18075101E], 0
#                  puis recopie les reglages depuis [rdx]
#
# Le bloc de seize octets porte le mode PUIS la sante, le temps, les rounds et
# le niveau CPU. Poser le mode seul laisse le reste tel quel : le combat
# demarre sur des reglages incoherents. Le chemin natif appelle `0x18019C4A0`
# avec une structure de reglages construite juste avant (`0x1801DD73E`, dans la
# mise a jour de la page Score Attack).
#
# En attendant de savoir fournir cette structure, on ne pose PLUS le mode : les
# trois modes relancent en Arcade, ce qui au moins ne plante pas.
SP_LANCER = [
    (0x1801A703D, None, 0x1801DDE89, bytes.fromhex('e882e1fdff'), 'Arcade'),
    (0x1801A7058, None, 0x1800A48A9, bytes.fromhex('e862771100'), 'Score Attack'),
    (0x1801A71D8, None, 0x1801DDE49, bytes.fromhex('e8c2e1fdff'), 'License Challenge'),
]


def sp_lancer_cave(a, mode):
    """Refait l'appel deplace, pose le mode de jeu, puis lance."""
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    c = bytes.fromhex('4883ec28')                       # sub rsp, 0x28
    c += bytes.fromhex('e8') + rel(a + len(c) + 5, SP_SON_VALIDER)
    if mode is not None:
        if mode == 0:
            c += bytes.fromhex('33c9')                  # xor ecx, ecx
        else:
            c += bytes.fromhex('6a') + bytes([mode]) + bytes.fromhex('59')
        c += bytes.fromhex('e8') + rel(a + len(c) + 5, SP_MODE_POSER)
    c += bytes.fromhex('e8') + rel(a + len(c) + 5, TRANSITION_CAVE)
    c += bytes.fromhex('4883c428')                      # add rsp, 0x28
    c += bytes.fromhex('c3')
    return c


def sp_lancer_hook(va, cave):
    return bytes.fromhex('e8') + struct.pack('<i', cave - (va + 5))


# ---------------------------------------------------------------------------
# `--sp-mode` -- Score Attack et License Challenge lancent LEUR mode.
#
# Ce que `--sp-lancer` fait, et pourquoi ca ne suffit pas : il se greffe dans le
# VALIDATEUR de la page (creneau [10]) et lance immediatement. Or le mode de jeu
# n'est pas pose la : la chaine native l'ecrit dans la MISE A JOUR (creneau [2]),
# plusieurs trames plus tard, une fois l'animation de sortie finie. On partait
# donc toujours en Arcade, mode 0 -- la valeur que le global a deja.
#
# La correction essayee le 2026-09-05 -- poser le mode nous-memes, par
# `0x18019C490(mode)` -- a plante a l'ecran. La cause est lisible : le mode est
# la PREMIERE CASE d'un bloc de seize octets qui porte aussi la sante, le temps,
# les rounds et le niveau CPU. Le poser seul laisse les douze autres octets a
# zero, et le combat demarre sur des reglages impossibles.
#
#     0x18019C490  mov [0x180751010], ecx ; ret        <- le mode SEUL
#     0x18019C4A0  mov [0x180751010], ecx              <- le mode ET le bloc
#                  mov [0x180751014], 0 ... puis recopie les reglages de [rdx]
#
# D'ou cette approche-ci, qui ne pose plus rien elle-meme : **laisser la page
# faire son travail, et se greffer sur son propre appel au setter**. Les quatre
# arguments sont deja calcules par le jeu, exactement comme sur console ; on
# refait l'appel deplace, puis on lance.
#
#     0x1801DD73E  call 0x18019C4A0     TaskMenuScoreAttack::update  (mode 1)
#     0x1801DC179  call 0x18019C420     ...LicenceChallenge::update  (mode 2)
#
# Les deux mises a jour ont la meme forme, verifiee au desassembleur :
#
#     call 0x1801BD9D0(page)          si VRAI  -> on saute tout
#     call 0x1801BD9C0(page+0x240)    si FAUX  -> on saute tout   (dword == 0 ?)
#     cmp  byte [page+0x60], 0        << « on lance » (et non « on annule »)
#     call 0x18019BBE0(&reglages, 0xDC, 0xDC, 0x2D, 2)   les cinq reglages
#     call <le setter>                                    <- NOTRE SITE
#
# Les vtables le confirment, creneau [2] : `TaskMenuScoreAttack` `0x1805326C8`
# -> `0x1801DD6A0`, `TaskMenuArcadeLicenceChallenge` `0x1805327E8` ->
# `0x1801DC050`.
#
# Le validateur de ces deux modes REDEVIENT donc celui d'origine : il se
# contente de poser `[page+0x60]` par `0x1801BC010`, et c'est la mise a jour qui
# lance. Arcade, lui, garde `--sp-lancer` : il marche, et mode 0 est la valeur
# par defaut. Cela libere les deux cavernes que Score Attack et License
# Challenge occupaient -- ce sont celles que l'on reprend ici, sans avoir a
# trouver de la place ailleurs.
#
# Alignement de pile : aux deux sites, `rsp` vaut 0 modulo 16 avant le `call`
# (Score Attack : `push rdi` + `sub rsp,0x30` ; License Challenge : trois `push`
# + `sub rsp,0x30`). Le `call` empile 8, `sub rsp,0x28` ramene a 0 et reserve
# les 32 octets d'espace d'accueil. `rdx` pointe sur la pile de l'appelant et
# n'est pas touche : la structure de reglages arrive intacte au setter.
#
# RISQUE ASSUME, a juger a l'ecran : si les deux gardes d'animation ne
# retombent jamais dans ce build, la mise a jour n'atteint pas le site et ces
# deux modes ne lanceront PLUS RIEN -- au lieu de lancer en Arcade. C'est pour
# cela que l'essai a son propre lanceur, `tools/essai_mode.cmd`, et que
# `tools/console.cmd` n'est pas touche.
SP_MODE_CAVE_MAX = 0x24                        # 36 o : la plus petite des deux
# (caverne, tete attendue de la caverne, setter natif, site, octets du site, nom)
SP_MODE = [
    (0x1801A7058, None, 0x18019C4A0, 0x1801DD73E,
     bytes.fromhex('e85dedfbff'), 'Score Attack'),
    (0x1801A71D8, bytes.fromhex('83f80475208b8b'), 0x18019C420, 0x1801DC179,
     bytes.fromhex('e8a202fcff'), 'License Challenge'),
]


def sp_mode_cave(a, setter):
    """Refait l'appel deplace au setter natif, puis lance. Dix-neuf octets."""
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    c = bytes.fromhex('4883ec28')                        # sub rsp, 0x28
    c += b'\xE8' + rel(a + len(c) + 5, setter)           # call le setter natif
    c += b'\xE8' + rel(a + len(c) + 5, TRANSITION_CAVE)  # call la caverne
    c += bytes.fromhex('4883c428')                       # add rsp, 0x28
    c += b'\xC3'                                         # ret
    if len(c) > SP_MODE_CAVE_MAX:
        raise AssertionError('la caverne de mode deborde : %d > %d octets'
                             % (len(c), SP_MODE_CAVE_MAX))
    return c


# ---------------------------------------------------------------------------
# `--sp-sparring` -- Special Sparring lance enfin son combat.
#
# Les trois autres entrees de SINGLE PLAYER marchent ; celle-ci ne lance RIEN.
# Ce n'est pas la meme panne que Score Attack et License Challenge, qui eux
# partaient en Arcade : ici la chaine native va jusqu'au bout et s'arrete.
#
# `analysis/mode_de_jeu.md` #9 l'avait etabli sans poser la greffe : la chaine
# existe (l'entree 3 pousse "CARD SELECTOR" -> `TaskMenuSetting`, puis
# `TaskMenuArcade::update` pousse `TaskMenuTeam`), et `TaskMenuTeam::update`
# pose bien le mode 3 -- mais **personne ne demande le mode GAME au bout**.
#
# Le site est la copie conforme de celui de License Challenge, verifie octet
# pour octet dans `.origine` le 2026-09-06 :
#
#     0x1801A4236  cmp   byte [rbx+0x60], 0        ; on valide (pas on annule)
#     0x1801A423C  movzx r8d, byte [rbx+0x4D8]
#     0x1801A4244  lea   rdx, [rbx+0x4D0]          ; le bloc de seize octets
#     0x1801A424B  xor   r9d, r9d
#     0x1801A424E  lea   ecx, [r9+3]               ; mode 3
#     0x1801A4252  call  0x18019C420               ; <-- NOTRE SITE  (e8c981ffff)
#     0x1801A4257  mov   dword [0x1807513A4], 0
#
# Meme principe qu'au `--sp-mode` : on ne pose rien nous-memes, on refait
# l'appel deplace -- le jeu a deja calcule ses quatre arguments -- puis on
# lance. Le bloc de reglages part donc entier, ce qui etait la cause du
# plantage du 2026-09-05.
#
# ALIGNEMENT. Prologue de `TaskMenuTeam::update` (`0x1801A4160`) : `push rdi`
# puis `sub rsp,0x20`. A l'entree `rsp % 16 == 8`, apres le push `== 0`, apres
# le sub `== 0`. Au site, `rsp % 16 == 0` : exactement comme aux deux sites du
# `--sp-mode`.
#
# LA PLACE, et pourquoi la greffe n'a pas la meme forme. Les quatre cavernes
# sont pleines ; mesure faite en comparant le binaire patche a `.origine` avec
# le jeu d'options de `console.cmd` :
#
#     fin de .text          164 o   ->  2 o libres
#     How to Play mort       64 o   -> 18 o libres a 0x1801A706B
#     Credits mort           36 o   -> 17 o libres
#     raccourci desactive    83 o   -> 18 o libres
#
# Le plus grand reste fait DIX-HUIT octets ; la greffe de `--sp-mode` en fait
# dix-neuf. On remplace donc le `call` de la caverne de transition par un SAUT
# TERMINAL, apres avoir remis la pile : dix-huit octets, et la transition rend
# la main directement a `0x1801A4257`.
#
#     sub rsp, 0x28          ; 32 o d'accueil + alignement
#     call <setter natif>
#     add rsp, 0x28          ; rsp pointe de nouveau l'adresse de retour
#     jmp  TRANSITION_CAVE   ; entree comme si elle etait appelee
#
# C'est licite ici, et verifie : `TRANSITION_CAVE` (`0x18034579C`) est une
# routine complete terminee par `ret`, qui n'emploie que `rax` et `rcx` -- deux
# registres volatils. `rbx` (la page) et `sil`, vivants apres `0x1801A4257`,
# lui survivent.
#
# Les deux greffes existantes ne sont PAS touchees : elles marchent, et elles
# gardent leur forme a dix-neuf octets.
SP_SPARRING_SITE = 0x1801A4252
SP_SPARRING_TETE = bytes.fromhex('e8c981ffff')
SP_SPARRING_SETTER = 0x18019C420
SP_SPARRING_CAVE = 0x1801A706B              # la queue de la caverne How to Play
SP_SPARRING_CAVE_TETE = bytes.fromhex('c74358010000004889bb68150000e9820100')
SP_SPARRING_CAVE_MAX = 0x1801A707D - 0x1801A706B          # 18 octets


def sp_sparring_cave(a, setter):
    """Refait l'appel deplace, puis SAUTE dans la transition. Dix-huit octets."""
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    c = bytes.fromhex('4883ec28')                        # sub rsp, 0x28
    c += b'\xE8' + rel(a + len(c) + 5, setter)           # call le setter natif
    c += bytes.fromhex('4883c428')                       # add rsp, 0x28
    c += b'\xE9' + rel(a + len(c) + 5, TRANSITION_CAVE)  # jmp la caverne
    if len(c) > SP_SPARRING_CAVE_MAX:
        raise AssertionError('la caverne de Special Sparring deborde : '
                             '%d > %d octets' % (len(c), SP_SPARRING_CAVE_MAX))
    return c


# ---------------------------------------------------------------------------
# `--attract-long` -- l'animation de titre longue, meme en mode console.
#
# Constat de Frederic : la sequence d'attract ne se joue plus, il ne reste
# qu'un bref ecran noir. En mode BORNE (`--mode 1`) elle est la : Akira qui
# enchaine des mouvements, le titre en 3D derriere, un mouvement de camera qui
# finit sur l'ecran-titre classique.
#
# Ce n'est PAS une video -- fausse piste suivie une demi-journee. C'est du
# temps reel, et le moteur choisit entre DEUX animations selon le mode de jeu,
# dans l'entree de `CS_TITLE` (`0x1800DDE00`) :
#
#     0x1800DE110  cmp dword [rsi+0x24], 1
#     0x1800DE114  je  0x1800DE125
#     0x1800DE116  cmp byte [0x180C3B701], bl    ; game_mode != 0 ?
#     0x1800DE11C  lea rax, "logo_vf5_short"     ; la COURTE
#     0x1800DE123  je  0x1800DE12C               ; console -> on garde la courte
#     0x1800DE125  lea rax, "logo_vf5"           ; la LONGUE
#     0x1800DE12C  mov [rbp-0x68], rax
#
# `0x180C3B701` est l'aiguillage borne/console du `vf5fs_game_config_t`, et les
# deux litteraux sont voisins en `0x1803A1560` : `logo_vf5` et
# `logo_vf5_short`. En console, le jeu prend la courte -- d'ou l'impression
# qu'il ne se passe rien.
#
# Un second test, vingt octets plus bas, saute en plus un appel :
#
#     0x1800DE15D  cmp dword [rsi+0x24], 1
#     0x1800DE161  je  0x1800DE16C
#     0x1800DE163  cmp byte [0x180C3B701], 0
#     0x1800DE16A  je  0x1800DE178               ; console -> SAUTE l'appel
#     0x1800DE172  call 0x180029CA0              ; borne -> le fait
#
# On neutralise donc les DEUX sauts, et rien d'autre : deux fois `74 xx` -> deux
# `nop`. Le mode console emprunte alors exactement le chemin de la borne pour
# cette sequence-la. Aucune caverne, aucun corps de fonction touche -- on ne
# fait que retirer un aiguillage, au site.
ATTRACT_LONG = [
    (DLL, 0x1800DE123, bytes.fromhex('7407'), bytes.fromhex('9090'),
     'le titre prend l animation LONGUE (logo_vf5) et non la courte'),
    (DLL, 0x1800DE16A, bytes.fromhex('740c'), bytes.fromhex('9090'),
     'et l appel que le mode console sautait est refait'),
]

# ---------------------------------------------------------------------------
# `--film-sfd` -- les films sont lus en `.sfd`, et non en `.usm`.
#
# Le moteur nomme ses films en `.sfd` : `rom/movie/vf5adv.sfd`
# (`0x1803A15A8`), `vf5title_bg.sfd`, `vf5end.sfd`. Mais le portage APM3_US
# **reecrit l'extension a la volee** : `0x1800E7810` (et son jumeau
# `0x1800E89C0`) cherchent `.sfd` dans le chemin et le remplacent par `.usm` --
# une substitution SSE classique, `vpcmpistri` pour la recherche puis une
# recopie de 16 octets :
#
#     0x1800E7A24  vmovdqu xmm4, [0x1803A1D64]   ; ".sfd"  -- ce qu'on cherche
#     0x1800E7A9E  vmovdqu xmm0, [0x1803A1D6C]   ; ".usm"  -- ce qu'on ecrit
#     0x1800E7AB0  vmovdqu [r8], xmm0            ; la substitution
#
# D'ou la mesure de `tools/tracer_fichiers.py` : le jeu n'ouvre QUE
# `vf5adv.usm`, jamais le `.sfd`, meme si celui-ci est depose a cote.
#
# Or ce `.usm` est encode en **codec 5**, lu dans son propre en-tete
# (`VIDEO_HDRINFO.mpeg_codec = 5`, 1920x1088, 8842 images, 60 im/s), alors que
# le seul decodeur inscrit dans `vfes.exe` porte l'**id 1** -- mesure de
# `tools/pister_decodeur.py`. D'ou, a chaque attract :
#
#     E11030202M: No available decoder is attached for the video stream.
#
# Le `.sfd` de la vraie borne (`APM3_FS/rom/movie/vf5adv.sfd`, 216 Mo) est lui
# un flux systeme **MPEG** (`00 00 01 BA` puis `00 00 01 BB`) : c'est du
# ressort du decodeur 1. Le fichier a copier est donc deja bon ; il suffit que
# le moteur le demande.
#
# On ne touche donc PAS au code : on change le litteral de REMPLACEMENT.
# `.usm` -> `.sfd`, quatre octets, et la substitution devient une identite.
# Le litteral n'a que quatre references, toutes dans ces deux fonctions : pas
# d'effet de bord ailleurs.
#
# RESULTAT DE L'ESSAI, 2026-09-06 -- NE PAS UTILISER CETTE OPTION TELLE QUELLE.
# Le jeu ouvre bien `vf5adv.sfd` (mesure `tracer_fichiers`), et le message du
# decodeur DISPARAIT. Mais il en vient un autre :
#
#     avant : E11030202M: No available decoder is attached for the video stream.
#     apres : E07020701M: Input is not CRI Movie data.
#
# CRI Mana 2.18 ne lit que le conteneur **USM**. Le `.sfd` est le format de
# **Sofdec 1** (Lindbergh, PS3, X360) : un flux systeme MPEG brut, sans
# conteneur CRI. Le codec video, lui, est le bon -- c'est du MPEG, ce que sait
# faire le decodeur `id = 1`.
#
# Ce qu'il faut donc pour caler un film dans ce build :
#
#     conteneur    USM (magie `CRID`)
#     video        mpeg_codec = 1   (Sofdec Prime / MPEG)  -- PAS 5 (le livre)
#     audio        audio_codec = 2  (ADX), 48 kHz          -- decodeur inscrit
#
# Autrement dit : REMULTIPLEXER le flux MPEG du `.sfd` dans un conteneur USM.
# Le contenu est bon, l'emballage ne l'est pas.
#
# Cette option reste utile comme MESURE (elle a permis de distinguer
# � codec inconnu � de � conteneur inconnu �), pas comme correctif.
#
# A COMBINER : sans `--attract-long`, `CS_DEMO` joue le film ; avec, l'ecran
# titre enchaine ensuite son animation `logo_vf5`. Les deux sont independants.
FILM_SFD = (DLL, 0x1803A1D6C, b'.usm\x00', b'.sfd\x00',
            'le remplacement d extension devient une identite : les films sont '
            'lus en .sfd')

# ---------------------------------------------------------------------------
# `--film-taille` -- la texture du film suit le FILM, plus l'ecran.
#
# Le moteur cree la texture de lecture a **MIN(ecran, film)**, ce qui casse des
# que le film est plus grand que la resolution de rendu. Juste apres avoir
# demande les infos du film (`call [rax+0x150]`) :
#
#     0x1800E7D93  mov   ecx, [rsi+0xA4]     ; largeur de l'ECRAN
#     0x1800E7D99  mov   eax, [rbp+0x18]     ; largeur du FILM
#     0x1800E7D9C  cmp   ecx, eax
#     0x1800E7D9E  cmovb eax, ecx            ; <- eax = MIN(ecran, film)
#     0x1800E7DA1  mov   [rsi+0x118], eax    ; largeur de la texture
#
#     0x1800E7DA7  mov   ecx, [rsi+0xA8]     ; hauteur de l'ECRAN
#     0x1800E7DAD  mov   eax, [rbp+0x1C]     ; hauteur du FILM
#     0x1800E7DB0  cmp   ecx, eax
#     0x1800E7DB2  cmovb eax, ecx            ; <- idem
#     0x1800E7DB5  mov   [rsi+0x11C], eax
#
# puis `0x180194E60` cree la texture avec `r8d` = largeur, `r9d` = hauteur.
#
# CE QUE CA PRODUISAIT. Rendu 1280x720, film 1920x1080 -> texture 1280x720, et
# le decodeur y ecrit des lignes de 1920 octets :
#
#     ACCESS_VIOLATION en ECRITURE, vfes.exe+0x111E3E  (rep movsb)
#     r8 = 0x780 = 1920 (une ligne)   rdi = la destination = l'adresse fautive
#
# Mesure de `tools/pister_tampon.py`, juste avant la faute : le televersement
# recevait `r8d = 1280, r9d = 720` -- la resolution de RENDU, pas celle du
# fichier.
#
# LE CORRECTIF. Retirer les deux `cmovb` : `eax` garde alors la dimension du
# FILM, et la texture est creee a sa taille. Six octets, deux sites, aucun
# corps de fonction touche.
#
# Le `cmp` qui precede devient inutile mais reste inoffensif (il ne fait que
# poser des drapeaux que plus personne ne lit).
# DEUX sites ecrivent `+0x118`/`+0x11C`, et le second ecrase le premier :
# l'INITIALISATION du lecteur y pose la taille d'ecran, sans aucune
# comparaison --
#
#     0x1800E87A9  mov eax, [rdi+0xA4]      ; largeur de l'ECRAN
#     0x1800E87BE  mov [rdi+0x118], eax
#     0x1800E87C4  mov eax, [rdi+0xA8]
#     0x1800E87CA  mov [rdi+0x11C], eax
#
# Retirer les seuls `cmovb` ne suffit donc pas -- essai du 2026-09-06, le
# plantage restait identique. On neutralise aussi ces deux rangements : les
# champs gardent alors ce que le chemin des infos du film y aura mis.
FILM_TAILLE = [
    (DLL, 0x1800E7D9E, bytes.fromhex('0f42c1'), bytes.fromhex('909090'),
     'la LARGEUR de la texture suit le film, non l ecran'),
    (DLL, 0x1800E7DB2, bytes.fromhex('0f42c1'), bytes.fromhex('909090'),
     'la HAUTEUR de la texture suit le film, non l ecran'),
    (DLL, 0x1800E87BE, bytes.fromhex('898718010000'), bytes.fromhex('909090909090'),
     'l init ne force plus la LARGEUR d ecran dans la taille de texture'),
    (DLL, 0x1800E87CA, bytes.fromhex('89871c010000'), bytes.fromhex('909090909090'),
     'l init ne force plus la HAUTEUR d ecran dans la taille de texture'),
]

# ---------------------------------------------------------------------------
# `--attract-retour-titre` -- couper le film ramene au TITRE, pas en mode borne.
#
# Constat de Frederic : en coupant l'attract par START, il faut QUATRE appuis
# de plus pour traverser un ecran noir, et on arrive directement sur la
# selection de personnages du mode arcade.
#
# Le tracage d'etats (`tools/tracer_etats.py --scenario ...`) le montre :
#
#     16,0 s  SYSTEM_STARTUP -> CS_DEMO
#     18,5 s  CS_DEMO -> etat APM3          <- la coupure bascule en mode BORNE
#     63,6 s  APM3_ENTRY -> CS_TITLE        (apres les appuis repetes)
#
# L'ecran noir est `APM3_ENTRY` -- celui qu'on ne peut traverser qu'a coups de
# START, deja connu du chantier.
#
# La decision est une branche unique, dans le gestionnaire de phase 2 de
# `CS_DEMO` (`0x1800DD8B0`) :
#
#     0x1800DD8FB  cmp byte [0x18070C558], 0   ; « la demo s'est terminee SEULE »
#     0x1800DD902  je  0x1800DD915             ; drapeau a 0 -> on a COUPE
#     0x1800DD904  mov ecx, 3
#     0x1800DD909  call 0x1800DA9C0            ; sous-etat 3 = CS_TITLE
#     0x1800DD915  mov ecx, 8
#     0x1800DD91A  call 0x1800DA9A0            ; MODE 8 = APM3
#
# Le drapeau `0x18070C558` n'est pose qu'en `0x1800DD551`, dans la mise a jour,
# et SEULEMENT quand la scene du film meurt d'elle-meme. Couper le film le
# laisse a zero, d'ou la bascule.
#
# C'est la semantique ARCADE : appuyer pendant l'attract veut dire « je mets une
# piece, je joue ». En mode console elle n'a pas de sens.
#
# Deux octets : le `je` neutralise, et les DEUX cas demandent le titre.
#
# A NE PAS APPLIQUER en mode borne (`--mode 1`), ou ce comportement est le bon.
ATTRACT_RETOUR_TITRE = (
    DLL, 0x1800DD902, bytes.fromhex('7411'), bytes.fromhex('9090'),
    'couper l attract ramene au TITRE et non en mode APM3')

# ---------------------------------------------------------------------------
# `--sans-now-loading` -- retirer le texte « NOW LOADING » des ecrans de
# chargement.
#
# Ce n'est PAS un identifiant de la table de libelles. L'identifiant `0x171`
# existe bien (`NOW LOADING...`), mais **aucun code ne le charge** -- balayage
# des immediats, zero site. Le texte affiche vient d'un LITTERAL du binaire,
# `0x18040A990`, voisin de `TIPS` :
#
#     0x18019BEA2  lea  r8, "NOW LOADING"       ; le texte
#     0x18019BEA9  mov  edx, 0x28
#     0x18019BEAE  lea  rcx, [rbp-0x59]         ; la mise en page
#     0x18019BEB2  call 0x18019B2E0             ; <- LE DESSIN
#
# Le litteral n'a **qu'une reference**, donc un seul site couvre tous les
# ecrans qui passent par la. On neutralise l'appel, et lui seul : cinq `nop`.
#
# On ne touche PAS au corps de `0x18019B2E0` -- c'est le dessin de texte
# generique, avec 118 appelants.
#
# A NE PAS CONFONDRE avec les douze phases de l'ecran de chargement
# (`0x18006B880`), qui chargent pour de vrai : les sauter casserait le jeu.
# Seul le texte peut partir, et c'est ce qu'on fait ici.
SANS_NOW_LOADING = (
    DLL, 0x18019BEB2, bytes.fromhex('e829f4ffff'), bytes.fromhex('9090909090'),
    'le texte « NOW LOADING » n est plus dessine')

# ---------------------------------------------------------------------------
# `--options-tips` -- une ligne « Tips » a bascule dans OPTIONS > Settings.
#
# Demande de Frederic, le 2026-09-06 : « ajoute la possibilite d'activer ou non
# les TIPS ». Les TIPS sont la scene voisine de « NOW LOADING » : le conseil
# affiche pendant les chargements, demarre par `0x18019C340`.
#
# LA PAGE. `TaskOptionSetting` (vtable `0x1804111F8`) dessine ses lignes par une
# boucle d'une regularite parfaite (`0x1801AA140`) :
#
#     0x1801AA47E  mov ebx, [rbp+r14*4-0x60]     ; identifiant du LIBELLE
#     0x1801AA485  call 0x1801EFD10              ; -> texte du libelle
#     0x1801AA49E  mov ecx, [rdi+r14*4+0x240]    ; VALEUR courante
#     0x1801AA4A6  inc ecx
#     0x1801AA4A8  add ecx, ebx                  ; id_valeur = id_libelle+1+valeur
#     0x1801AA4AA  call 0x1801EFD10              ; -> texte de la valeur
#
# Une ligne a bascule est donc un libelle suivi IMMEDIATEMENT de `Off` puis `On`
# dans la table des textes. Les quatre lignes sont `[rbp-0x60]` : 0x30C (Volume
# Music), 0x2F6 (Volume SE), 0x322 (Stage BGM), 0x32A (Autosave).
#
# POURQUOI ON REPREND « Autosave » AU LIEU D'AJOUTER UNE LIGNE. Mesure faite :
#   . le tableau des valeurs `[rdi+0x240]` ne fait que QUATRE entrees -- l'init
#     `0x1801AB190` ecrit `vmovsd [rdi+0x250]` juste apres, la cinquieme case
#     n'existe pas ;
#   . le tableau des libelles `[rbp-0x60]` bute sur `[rbp-0x50]`, deja pris ;
#   . la boucle porte sa propre borne `cmp r14, 4 / jge` (`0x1801AA40B`).
# Ajouter une cinquieme ligne demanderait donc de deplacer deux tableaux et
# d'agrandir l'objet. Or « Autosave » est INERTE sur APM3 : sa valeur vit en
# `config+0x5020` (accesseur `0x1801B8980`), et le balayage ne trouve que trois
# lecteurs -- l'init de la page, sa validation, et les routines de serialisation
# du bloc. Aucune borne n'a de carte memoire. On reprend donc la ligne, avec sa
# persistance et ses bornes 0/1 deja en place. Son defaut vaut 1
# (`0x1801B8D7E mov dword [rbx+0x5020], 1`) : les TIPS restent actifs par
# defaut, comme aujourd'hui.
#
# TROIS FAMILLES D'OCTETS.
#
# 1. LA VALEUR. L'identifiant de la ligne 3 passe de 0x32A a 0x1D5. Ce n'est
#    pas « Stage select » qu'on veut afficher : c'est que 0x1D6 = `Off` et
#    0x1D7 = `On`, donc la colonne de droite marche telle quelle.
#
# 2. LE LIBELLE. Aucun texte « Tips » n'existe dans `string_array_en.bin`, et
#    cette table vit dans le `.par` -- un lien dur vers le dump, qu'on ne
#    touche pas. On ecrit donc la chaine dans le binaire et on detourne le SEUL
#    appel du resolveur qui rend le libelle (`0x1801AA485`), en le gardant sur
#    l'indice de ligne :
#
#        cmp r14b, 3
#        jne  .natif
#        lea  rax, [rip+"Tips"]      ; le resolveur rend un const char* en rax
#        ret
#    .natif:
#        jmp  0x1801EFD10
#
#    L'appel du titre de page (`0x1801AA2E2`, id 0x2F3) et celui de la VALEUR
#    (`0x1801AA4AA`) ne sont pas touches.
#
# 3. LA GARDE. `0x18019C340` demarre la scene TIPS ; trois sites y menent
#    (`0x1800BC688`, `0x1801C5B33` en `call`, `0x180203F72` en `jmp`). On les
#    fait tous passer par une caverne qui lit le reglage :
#
#        call 0x1801B8980            ; rax = &config.autosave  (= nos TIPS)
#        cmp  dword [rax], 0
#        je   .off
#        jmp  0x18019C340            ; queue d'appel : pile inchangee
#    .off:
#        ret
#
#    Le `jmp` terminal preserve la pile du site d'appel, et le `ret` de `.off`
#    rend la main exactement comme la sortie hative de `0x18019C340`. Le site
#    en `jmp` garde donc sa semantique de queue d'appel.
#
#    On ne verifie pas que le singleton de config est non nul : le moteur ne le
#    verifie nulle part non plus (`0x1801AB190` et `0x1801A8360` le
#    dereferencent sec), et les trois appelants sont des taches de scene, pas du
#    code de demarrage.
#
# LES CAVERNES. Les quatre connues sont pleines (18 octets libres au mieux). On
# prend donc deux bourrages d'alignement `int3`, VERIFIES hors de toute entree
# de `.pdata` (13 661 fonctions balayees) et suivis d'une frontiere a 16 :
#
#     0x1802786EB  21 octets  -> le libelle          (19 octets)
#     0x18027718B  21 octets  -> la garde + « Tips » (16 + 5 octets)
#
# La chaine vit en `.text`, qui est lisible : seul l'ecriture y serait
# interdite, et on ne fait que la lire.
TIPS_ID_LIGNE = 0x1801AA1A5                 # l'immediat 0x32A de la ligne 3
TIPS_BASE = 0x1D5                           # 0x1D6 = Off, 0x1D7 = On
TIPS_APPEL_LIBELLE = 0x1801AA485
TIPS_RESOLVEUR = 0x1801EFD10
TIPS_SCENE = 0x18019C340
TIPS_ACCESSEUR = 0x1801B8980                # rend &config+0x5020
TIPS_CAVE_LIBELLE = 0x1802786EB
TIPS_CAVE_LIBELLE_MAX = 21
TIPS_CAVE_GARDE = 0x18027718B
TIPS_CAVE_GARDE_MAX = 21
TIPS_LIGNE = 3                              # « Autosave », la quatrieme
TIPS_SITES = (0x1800BC688, 0x1801C5B33, 0x180203F72)


def _rel(depuis, vers):
    return struct.pack('<i', vers - depuis)


def tips_cave_garde():
    """La garde, puis la chaine. Seize octets de code, cinq de texte."""
    a = TIPS_CAVE_GARDE
    c = b'\xE8' + _rel(a + 5, TIPS_ACCESSEUR)        # call l'accesseur natif
    c += bytes.fromhex('833800')                     # cmp dword [rax], 0
    c += bytes.fromhex('7405')                       # je .off
    c += b'\xE9' + _rel(a + len(c) + 5, TIPS_SCENE)  # jmp la scene TIPS
    c += b'\xC3'                                     # .off: ret
    texte = a + len(c)
    c += b'Tips\0'
    if len(c) > TIPS_CAVE_GARDE_MAX:
        raise AssertionError('la caverne de la garde TIPS deborde : %d > %d'
                             % (len(c), TIPS_CAVE_GARDE_MAX))
    return c, texte


def tips_cave_libelle(texte):
    """Rend « Tips » pour la ligne visee, et delegue pour toutes les autres."""
    a = TIPS_CAVE_LIBELLE
    c = bytes.fromhex('4180fe') + bytes((TIPS_LIGNE,))   # cmp r14b, 3
    c += bytes.fromhex('7508')                           # jne .natif
    c += bytes.fromhex('488d05') + _rel(a + len(c) + 7, texte)
    c += b'\xC3'                                         # ret
    c += b'\xE9' + _rel(a + len(c) + 5, TIPS_RESOLVEUR)  # .natif: jmp resolveur
    if len(c) > TIPS_CAVE_LIBELLE_MAX:
        raise AssertionError('la caverne du libelle TIPS deborde : %d > %d'
                             % (len(c), TIPS_CAVE_LIBELLE_MAX))
    return c


def options_tips():
    """Les sept points du correctif, prets pour la boucle d'application."""
    garde, texte = tips_cave_garde()
    libelle = tips_cave_libelle(texte)
    vide = b'\xCC' * TIPS_CAVE_GARDE_MAX
    points = [
        (DLL, TIPS_ID_LIGNE, struct.pack('<I', 0x32A),
         struct.pack('<I', TIPS_BASE)),
        (DLL, TIPS_CAVE_GARDE, vide[:len(garde)], garde),
        (DLL, TIPS_CAVE_LIBELLE, vide[:len(libelle)], libelle),
        (DLL, TIPS_APPEL_LIBELLE, bytes.fromhex('e886580400'),
         b'\xE8' + _rel(TIPS_APPEL_LIBELLE + 5, TIPS_CAVE_LIBELLE)),
    ]
    for site in TIPS_SITES:
        tete = b'\xE9' if site == 0x180203F72 else b'\xE8'
        points.append((DLL, site, tete + _rel(site + 5, TIPS_SCENE),
                       tete + _rel(site + 5, TIPS_CAVE_GARDE)))
    return points


MENU_EXIT = [
    (DLL, 0x1801E3A13, bytes.fromhex('c6834b060000' '02'),
     bytes.fromhex('c6834b060000' '00')),            # entree 9 : dessinee
    (DLL, 0x1801DCF0E, bytes.fromhex('c68741060000' '01' 'e920020000'),
     bytes.fromhex('33c9' 'ff15' '02941600' '90909090')),
    # Et le dialogue d'avertissement lui-meme : « All unsaved progress will be
    # lost. Are you sure? » (texte 0x3EE). Sur borne il n'y a rien a sauver ;
    # Frederic l'a demande retire. Le bloc qui l'ouvre n'appartient qu'a
    # l'entree 9 -- `0x1801DE152 cmp ecx, 9` deux instructions plus haut, et
    # l'autre branche est un bouchon (`0x1801DE15B call 0x180007450`) :
    #
    #     0x1801DE182  lea  rcx, [rdi+0x4C0]      ; preparer la scene
    #     0x1801DE189  call 0x1801BD950
    #     0x1801DE18E  ... "EXIT_CAUTION", texte 0x3EE, oui/non
    #
    # On y quitte directement. Douze octets, la meme paire qu'en 0x1801DCF0E.
    (DLL, 0x1801de182,
     bytes.fromhex('488d8fc0040000e8c2f7fdff'),
     bytes.fromhex('33c9ff158e81160090909090')),
]

# ---------------------------------------------------------------------------
# MAILLON 7 -- le DOJO. Et une CORRECTION de l'enquete precedente.
#
# Le bilan de la section 8 de menu_console.md affirmait que les modes 2 GAME et
# 6 CS_TRAINING n'avaient AUCUN demandeur. C'est vrai pour GAME ; **c'est faux
# pour CS_TRAINING**, et l'erreur venait de la methode : le balayage parcourait
# les fonctions listees dans `.pdata`. Or `0x18019C3D0` est une feuille -- pas
# de cadre de pile, sortie par saut terminal -- donc **sans entree `.pdata`**,
# donc invisible. Le meme angle mort que la feuille qui nous avait plantes
# (`0x1800B1D30`).
#
# Un balayage LINEAIRE de `.text` par motif d'octets (E8/E9 + rel32) donne le
# compte exact : 28 sites de demande de mode, 41 de sous-etat, dont **un seul**
# echappait a `.pdata` -- et c'est justement celui-ci :
#
#     0x18019C3D0  mov  [0x180751010], ecx    ; le type de partie
#     ...          remet les reglages a zero
#     0x18019C407  test r8b, r8b
#     0x18019C40A  je   0x18019C414
#     0x18019C40C  lea  ecx, [rax + 6]        ; rax = 0
#     0x18019C40F  jmp  0x1800DA9A0           ; DEMANDE LE MODE 6 CS_TRAINING
#
# La page DOJO (`0x1801DD9C0`, creneau 2 de la vtable `0x180532968`) l'appelle
# avec `r8b = 1` des que le joueur valide :
#
#     0x1801DDA45  eax = [page+0x58]          ; l'entree choisie
#     0x1801DDA4C  ecx = 6                    ; entree 0
#     0x1801DDA51  ecx = 7 ou 8               ; entrees 1 et 2
#     0x1801DDA61  call 0x18019C3D0
#
# **Le DOJO demande donc deja son mode.** Il ne lui manque qu'une chose : rien
# au monde ne demande le **sous-etat 41 CS_TRAINING** (verifie au balayage
# lineaire). Sans lui, le mode change mais le sous-etat reste MENU_MAIN, dont
# le milieu est un bouchon : il ne se passerait rien.
#
# D'ou un maillon plus court que les precedents : on accroche le site d'appel
# (les six autres appelants de `0x18019C3D0` ne sont pas concernes), on laisse
# la fonction poser son type et demander son mode, puis on cree la session si
# besoin et on demande le sous-etat 41.
DOJO_HOOK = 0x1801DDA61
DOJO_TETE = bytes.fromhex('e86ae9fbff')
DOJO_TYPE = 0x18019C3D0
SOUS_ETAT_CS_TRAINING = 41                  # 0x29
DOJO_CAVE = 0x18034575C                     # la premiere moitie de la caverne
DOJO_CAVE_MAX = 0x40

# ---------------------------------------------------------------------------
# MAILLON 8 -- une touche pour SORTIR d'un mode.
#
# Constat de Frederic : « il manque des touches pour sortir des differents
# modes de jeu ». C'est structurel, et coherent avec tout le reste : **sur une
# borne on ne sort pas d'un mode**, on joue jusqu'a la fin. Le seul « arret »
# du moteur vient de l'exterieur -- `0x1801B8C40`, qui pose le drapeau de fin
# `ctx+0x68C1`, n'a qu'UN appelant, `0x180245C51`, dans la zone des points
# d'entree du module : c'est l'hote qui le commande, pas le jeu.
#
# Or les deux milieux de mode qui nous concernent ont deja la porte, et elle a
# exactement la meme forme dans les deux :
#
#     0x1800DA9DB / 0x1801E4E66   bl = 0x1801B6FE0()   -> ecran-titre
#     0x1800DA9E3 / 0x1801E4E6E   al = 0x1801B6E40()   -> mode 4 MENU
#     ...          test al, al ; je ... ; mov ecx, 4 ; call demander_mode
#
# `0x1801B6E40` ne peut jamais rendre vrai (dernier verrou bouchonne, voir
# section 8 de vs_gameover.md), mais on ne le touche pas : il a quatre
# appelants. On remplace **les deux sites d'appel** par un test de bouton.
#
# PREMIERE VERSION, ABANDONNEE : le masque `0x200`, c'est-a-dire la piece
# (Espace). Frederic : « la touche espace est deja utilisee ». Et il n'y a
# aucun masque libre a prendre : les seize bits qu'alimente `0x180243ED0` sont
# tous cables sur une touche qui sert (voir la table de la section 10 de
# menu_console.md), et les bits 8, 10 et 11 n'ont aucune source du tout.
#
# D'ou une solution plus propre : **ne pas passer par le masque**. Le relais
# interroge directement `Input_isOn` sur un code que le moteur ne lit nulle
# part -- le **15**, libre entre les codes du joueur 1 (0 a 14) et ceux du
# joueur 2 (18 a 30). Le stub lui donne la touche `Echap` et le bouton BACK de
# la manette ; comme ce code n'entre pas dans la boucle par joueur, lui donner
# les deux sources est sans effet de bord.
#
# `Input_isOn` est le creneau `+0x158` de la vtable de l'objet `[0x180C3B6F8]`,
# exactement comme dans `0x180243ED0`. Il rend deja un booleen dans `al` : la
# branche `test al, al` qui suit n'a rien a convertir.
SORTIE_HOOKS = [
    (0x1800DA9E3, bytes.fromhex('e858c40d00')),      # milieu du mode GAME
    (0x1801E4E6E, bytes.fromhex('e8cd1ffdff')),      # milieu du mode CS_TRAINING
]
SORTIE_CODE = 15                            # libre : ni joueur 1 ni joueur 2
ENTREES_OBJET = 0x180C3B6F8                 # l'objet dont +0x158 est Input_isOn
ENTREES_CRENEAU = 0x158
SORTIE_CAVE = 0x1803457E0                   # apres la caverne versus
SORTIE_CAVE_MAX = 0x180345800 - 0x1803457E0

# ---------------------------------------------------------------------------
# LES SOUS-MENUS : le menu principal continue de lire les directions.
#
# Constat de Frederic : « quand je me deplace dans un sous menu, les directions
# agissent aussi sur le menu principal situe en arriere plan ».
#
# Le mecanisme voulu est ECRIT, et il est correct. Ouvrir un sous-menu demarre
# sa scene et range la sous-page dans `[menu + 0x650]` ; la mise a jour du menu
# principal (`0x1801DC620`) se coupe alors des sa premiere instruction :
#
#     0x1801DC63D  mov  rcx, [rdi + 0x650]
#     0x1801DC647  je   suite              ; vide -> le menu principal continue
#     0x1801DC649  call 0x180244EA0        ; <- LA GARDE
#     0x1801DC650  jne  0x1801DCE33        ; vivante -> on rend la main
#     0x1801DC656  ...  [rdi+0x650] = 0    ; morte -> on OUBLIE la sous-page
#
# MESURE (tools/pister_sousmenu.py, 2026-09-05), recit brut :
#
#     OUVRE  OFFLINE VERSUS -> reussie
#     GARDE  sous-page=0x2535ABEB288  vivante=1  (curseur deja bouge 320 x)
#     OUBLI  la sous-page est effacee de [menu+0x650]
#     OUVRE  OFFLINE VERSUS -> ECHOUEE
#     OUVRE  OFFLINE VERSUS -> ECHOUEE
#
#     curseur du menu principal deplace : 1323 fois
#
# La garde n'a donc tenu qu'UNE trame. `0x180244EA0` ne demande pas « le
# sous-menu est-il ouvert ? » mais « la scene joue-t-elle encore ? » :
#
#     0x180244EA9  call 0x180244F90        ; la scene existe-t-elle ?
#     0x180244EB2  cmp  [rbx+0x18], 0      ; je -> vrai
#     0x180244EB8  cmp  [rbx+0x1C], 0      ; je -> FAUX
#
# L'animation d'ouverture finit, la scene se tait, et le menu principal se
# reveille sous le sous-menu.
#
# Le bon predicat existe deja dans le moteur : le champ `+0x60` de la
# sous-page, son drapeau « je m'en vais ». L'ouverture le met a zero --
# `0x1801DDFA6 xor ebx, ebx` puis `0x1801DDFBD mov [rdi+0x1A08], bl`, et
# `0x1A08 = 0x19A8 + 0x60` -- et la tache du menu le relit pour choisir quelle
# scene fermer (`0x1801E3CFB cmp byte [rbx+0x1A08], sil`).
#
# On remplace donc l'appel de la garde, et LUI SEUL (un seul site), par huit
# octets de caverne :
#
#     80 79 60 00    cmp  byte [rcx + 0x60], 0    ; la sous-page s'en va-t-elle ?
#     0f 94 c0       sete al                      ; non -> elle est OUVERTE
#     c3             ret
#
# Le corps de `0x180244EA0` n'est pas touche : il a 96 autres appelants.
# C'est la regle de ce chantier -- patcher le site d'appel, jamais le corps.
#
# Quand le sous-menu se ferme, il met son `+0x60` a 1, le predicat devient
# faux, `0x1801DC656` efface la sous-page et le menu principal reprend la main.
# Le retour marche donc toujours.
#
# La caverne : on utilise le trou de 23 octets laisse entre le relais du DOJO
# (qui finit en 0x180345784) et celui de la transition (0x18034579C).
SOUSMENU_GARDE = 0x1801DC649
SOUSMENU_GARDE_TETE = bytes.fromhex('e852880600')   # call 0x180244EA0
SOUSMENU_PREDICAT = 0x180244F90                     # « la scene EXISTE-t-elle ? »

# Et il faut DEFAIRE `--menu-ranking`, qui soignait le symptome au mauvais
# endroit. Ce verrou-la venait d'une branche de la mise a jour qui ouvre la
# page RANKING et la range comme si c'etait un sous-menu :
#
#     0x1801DCE27  call 0x1801B0120        ; ouvrir la page RANKING
#     0x1801DCE2C  mov  [rdi+0x650], rax   ; <- c'est CE rangement qui figeait
#
# Sur une borne sans reseau, cette scene n'a rien a jouer et ne se termine
# jamais : le menu restait suspendu derriere elle. `--menu-ranking` retirait
# alors le `jne` de la garde -- ce qui levait bien le blocage, mais retirait du
# meme coup la suspension pour TOUS les sous-menus. C'est la cause exacte du
# defaut signale par Frederic, et elle etait de notre main.
#
# On neutralise donc les 7 octets du rangement, et la garde reste entiere.
SOUSMENU_RANKING = (DLL, 0x1801DCE2C, bytes.fromhex('48898750060000'),
                    bytes.fromhex('90909090909090'))

SESSION_LIRE = 0x1800B23A0
SESSION_CREER = 0x1800B3620
TRANSITION_CAVE = 0x18034575C + 0x40        # = MENU_CAVE + 0x40, defini plus bas
TRANSITION_CAVE_MAX = 0x30                  # 48 octets, puis vient VERSUS_CAVE

# ---------------------------------------------------------------------------
# MAILLON 5 -- OFFLINE VERSUS mene lui aussi au combat.
#
# La page VERSUS est la soeur exacte de celle du menu principal : meme classe,
# vtable `0x1805328A8` (creneau 1 = entree `0x1801E4560`, 2 = mise a jour
# `0x1801DDB40`, 3 = validation `0x1801DEA60`, 4 = dessin `0x1801E2190` -- dont
# les libelles sont bien « Round count / Time limit / Max health 1P / Max
# health 2P / Stage select »).
#
# Sa validation `0x1801DEA60` **ne lance rien** : quand `[page+0x60]` est pose,
# elle recopie ses cinq reglages (`page+0x240` a `+0x250`) dans le bloc courant
# et appelle `0x1801BA0A0` pour l'enregistrer, puis referme la page. Exactement
# la meme forme que SINGLE PLAYER : la page finit, et personne ne demarre.
#
# On accroche donc **la fin du chemin valide**, et lui seul -- le chemin
# « annule » passe par `0x1801DEB19` et ne nous concerne pas. A `0x1801DEB12`,
# `rcx` pointe deja le bloc de reglages ; le relais appelle l'enregistrement
# avec ses arguments intacts, puis la caverne du maillon 1.
#
#     0x1801DEA66  cmp byte [rcx+0x60], 0   ; valide ?
#     0x1801DEA6D  je  0x1801DEB19          ; non : annule
#     ...          recopie des cinq reglages
#     0x1801DEB12  call 0x1801BA0A0         ; <-- ICI
VERSUS_HOOK = 0x1801DEB12
VERSUS_TETE = bytes.fromhex('e889b5fdff')
VERSUS_ENREGISTRER = 0x1801BA0A0
VERSUS_CAVE = 0x18034575C + 0x70            # apres la caverne du maillon 1
VERSUS_CAVE_MAX = 164 - 0x70                # 36 octets

# ---------------------------------------------------------------------------
# LE JOUEUR 2 N'EXISTE PAS DANS CE BUILD.
#
# Mesure a l'ecran : l'ecran de reglages d'OFFLINE VERSUS s'affiche **grise**,
# rien n'est modifiable, et on ne peut pas lancer. Le message que la page
# affiche alors (identifiant de texte 0x81, resolu par tools/libelles.py) est
# sans ambiguite :
#
#     « Two controllers are needed to play this mode.
#       Press the START button on Player 2's controller. »
#
# Sa mise a jour `0x1801DDB40` demande en effet, a chaque trame :
#
#     0x1801DDC58  mov  ecx, 1
#     0x1801DDC5D  call 0x1801A2330      ; le peripherique 1 a-t-il un joueur ?
#     0x1801DDC64  setns cl
#     0x1801DDC67  mov  byte [rdi+0x309], cl
#
# et tant que `[page+0x309]` est nul, elle affiche le message 0x81 et n'accepte
# rien. **Ce n'est pas nous** : la page est intacte et fait son travail.
#
# La cause est deux etages plus bas, dans le lecteur d'entrees APM3 :
#
#     0x180243F5F  mov  ebx, r14d       ; ebx = 0
#     0x180243F62  test ebp, ebp        ; ebp = le numero de joueur
#     0x180243F64  jne  0x1802440D6     ; JOUEUR 2 : saute TOUTES les lectures
#
# Autrement dit, **le masque de boutons du joueur 2 vaut toujours zero** : la
# quinzaine d'appels a `Input_isOn` n'est faite que pour le joueur 1. Ce build
# est mono-joueur des la couche d'entree.
#
# `--versus-miroir` retire ce saut. Le joueur 2 lit alors les MEMES touches que
# le joueur 1 : l'ecran se debloque, on peut regler et lancer, et les deux
# combattants bougent ensemble. C'est un **palliatif de mesure**, pas un vrai
# deux-joueurs -- il sert a voir le parcours, pas a y jouer. Un vrai joueur 2
# demande d'etendre notre `apm.dll` a une seconde source et d'ecrire un second
# bloc de lecture : environ 0x16C octets, la caverne n'en a plus assez.
VERSUS_MIROIR = (DLL, 0x180243F64, bytes.fromhex('0f856c010000'),
                 bytes.fromhex('909090909090'))

# ---------------------------------------------------------------------------
# UN VRAI JOUEUR 2 : `--joueur2`
#
# Le miroir ci-dessus fait bouger les deux combattants ensemble. Pour un vrai
# second joueur il faut que le bloc de lecture demande, pour le joueur 2, des
# codes DIFFERENTS de ceux du joueur 1. Il y a treize sites qui posent le code
# dans `edx`, et deux d'entre eux le font **deja relativement au joueur** :
#
#     0x180243F71  lea edx, [rbp + 2]     <- rbp est l'index de joueur
#     0x180243F84  lea edx, [rbp + 5]
#     0x180243FA5  mov edx, 3             <- les onze autres sont absolus
#     ...
#
# D'ou le correctif, en deux temps.
#
# 1. Les onze `mov edx, imm32` (5 octets) deviennent `lea edx, [rbp + code]`
#    (3 octets) suivis de deux `nop`. Tous les codes sont alors relatifs.
#
# 2. Les six octets du saut retire par le miroir recoivent `shl ebp, 4`, si
#    bien que `rbp` vaut 0 pour le joueur 1 et **16** pour le joueur 2. Les
#    codes du joueur 2 sont donc ceux du joueur 1 plus seize : 18 a 30, tous
#    dans les 32 creneaux du stub.
#
# Pourquoi ce decalage ne casse pas la boucle : apres ce point `ebp` n'est plus
# relu jusqu'a `inc ebp ; cmp ebp, 2 ; jb` en 0x180244156. Pour le joueur 1,
# 0 << 4 = 0, puis 1 -- la boucle repart. Pour le joueur 2, 16 puis 17, et
# `cmp 17, 2` sort. C'est exactement le comportement voulu, sans restauration.
#
# Cote stub, `tools/gen_apm_stub.py` separe alors les deux sources : codes 0 a
# 14 au CLAVIER seul, codes 18 a 30 a la MANETTE seule. Sans cette separation
# la manette piloterait les deux joueurs.
JOUEUR2_SHL = (DLL, 0x180243F64, bytes.fromhex('0f856c010000'),
               bytes.fromhex('c1e504') + b'\x90' * 3)      # shl ebp, 4
JOUEUR2_CODES = [                       # (VA, octets attendus, code)
    (0x180243FA5, bytes.fromhex('ba03000000'), 3),
    (0x180243FC2, bytes.fromhex('ba04000000'), 4),
    (0x180243FDF, bytes.fromhex('ba0b000000'), 0x0B),
    (0x180243FFB, bytes.fromhex('ba07000000'), 7),
    (0x180244017, bytes.fromhex('ba0c000000'), 0x0C),
    (0x180244033, bytes.fromhex('ba08000000'), 8),
    (0x18024404F, bytes.fromhex('ba09000000'), 9),
    (0x18024406B, bytes.fromhex('ba0a000000'), 0x0A),
    (0x180244088, bytes.fromhex('ba0d000000'), 0x0D),
    (0x1802440A4, bytes.fromhex('ba0e000000'), 0x0E),
    (0x1802440C0, bytes.fromhex('ba06000000'), 6),
]

# ---------------------------------------------------------------------------
# LE DECOR DE L'ECRAN TERMINAL : DEUX index en dur, pas un.
#
# Constat de Frederic : « le decor du mode terminal est bugge ». Trois
# tentatives de correction n'ont RIEN change a l'ecran. La raison est simple et
# elle a mis du temps a sortir : **je changeais le mauvais octet**.
#
# L'ecran de personnalisation enregistre une tache `STAGE_TASK` (`0x1801C4D60`,
# machine a 41 etapes dont 7 seulement font quelque chose). Ses deux premieres
# etapes demandent DEUX choses differentes, chacune avec son propre `1` :
#
#     etape 0 :  0x1801C4DA6  mov  ecx, 1
#                0x1801C4DAB  call 0x18018FCF0     <- la GEOMETRIE
#     etape 1 :  0x1801C4DCB  mov  ecx, 1
#                0x1801C4DD0  call 0x1800D7130     <- l'ECLAIRAGE
#
# `0x1800D7130` ne charge PAS de decor : il compose `%s/%s.ibl` sous
# `./rom/ibl` et `%s/light_%s.txt` sous `./rom/light_param`. C'est la sonde
# d'environnement et les parametres de lumiere, rien d'autre. Le seul effet
# visible d'en changer l'index est un changement de teinte -- imperceptible
# entre deux decors de test. D'ou trois essais « sans difference ».
#
# `0x18018FCF0` est la vraie demande. C'est une FEUILLE (donc absente de
# `.pdata`, il a fallu un balayage lineaire pour la trouver) :
#
#     0x18018FCF0  cmp   ecx, 0x29           ; borne : 41 decors
#     0x18018FCF5  mov   rax, [0x1807499D8]  ; le gestionnaire de decor
#     0x18018FCFC  cmp   ecx, [rax + 0x5C]   ; deja charge ? on ne fait rien
#     0x18018FD01  mov   [rax + 0x60], ecx   ; <- LA DEMANDE
#
# Le gestionnaire est un singleton (`0x1807499D8`, vtable `0x180408210`). Son
# slot +0x10 (`0x18018EF40`) consomme la demande a chaque trame :
#
#     +0x58  phase (0 libre, 1..5 chargement en cours)
#     +0x5C  index CHARGE          +0x60  index DEMANDE (-1 = rien)
#     +0x68  descripteur = 0x180403430 + index * 0xF0
#
# La table des descripteurs se lit en clair et confirme la numerotation :
#
#     index  1 -> "STGTS2"  "EFFSTGTS2"  ...  bgm vfes_bgm_vf2_ban.adx
#     index  5 -> "STGTER"  "EFFSTGTER"  ...  bgm vfes_bgm_stg_ter.adx
#     index 26 -> "STGTRM"  "EFFSTGTRM"  ...  bgm vfes_bgm_stg_ban.adx
#
# Ce qui EST etabli, et ce qui ne l'est pas
# -----------------------------------------
# Compare avec R.E.V.O. (`vf5fs-pxd-w64-d3d12_SteamRetail.dll`), la tache est
# identique cas par cas -- meme decoupage en 41 etapes, memes 7 cas utiles,
# meme `Decor_Demander(1)` puis `Eclairage_Charger(1)`, meme BGM
# `vfes_bgm_cus.adx`. La borne ne DIFFERE donc pas du PC.
#
# Mais cela ne dit pas que `ts2` est ce qu'il faut afficher : cela dit que le
# PC afficherait la meme chose. L'essai `trm` sur la geometrie n'a jamais ete
# fait -- il commence ici.
#
# Tailles dans le `.par`, pour l'echelle :
#
#     stgts2.farc      505 420 o     <- ce qui est charge aujourd'hui
#     stgtrm.farc    1 289 391 o     <- le decor « terminal »
#     stgdjo.farc   10 516 296 o     <- un vrai decor de combat
#
# `--decor-perso <index|nom>` remplace les DEUX octets. Portee : exactement
# l'ecran de personnalisation -- `0x18018FCF0` n'a que trois appelants
# (celui-ci, `0x1800BC6AD` et `0x1802035AA`, tous deux a index variable).
DECOR_PERSO_SITES = [
    (DLL, 0x1801C4DA6 + 1, bytes.fromhex('01'), 'geometrie (0x18018FCF0)'),
    (DLL, 0x1801C4DCB + 1, bytes.fromhex('01'), 'eclairage (0x1800D7130)'),
]
DECOR_NOMS = ['tst', 'ts2', 'ts3', 'wht', 'ban', 'ter', 'nyc', 'cas', 'riv',
              'jin', 'sin', 'djo', 'umi', 'hai', 'are', 'slk', 'yuk', 'tak',
              'aur', 'bar', 'tan', 'du1', 'du2', 'du3', 'du4', 'du5', 'trm',
              'cid', 'trs', 'evo00', 'evo01', 'evo02', 'evo03', 'evo04',
              'evo05', 'evo06', 'evo07', 'evo08', 'evo09', 'gym', 'smo']

# ---------------------------------------------------------------------------
# LES CINQ DECORS DE DURAL : pourquoi on n'en voit qu'UN SEUL
#
# Etabli le 2026-09-07. Le decor d'un combat solo n'est pas choisi par le code :
# c'est le DECOR MAISON DE L'ADVERSAIRE, une donnee de `rom/game_score.txt`
# (`score.chara.<n>.stage=STGDJO`, 21 entrees, fichier en clair du `.par`). Le
# constructeur de match `0x1800B8540` le demande a `0x1800AF400(personnage)`,
# qui n'a **qu'un seul appelant** -- ce site-la :
#
#     0x1800B8AF6  mov  ecx, [rsp+rbx+0x3c]   ; le personnage ADVERSE
#     0x1800B8AFA  call 0x1800AF400           ; -> son decor maison
#     0x1800B8AFF  mov  r12d, eax
#     0x1800B8B02  cmp  eax, 0x15             ; 21 = du1, le decor de Dural
#     0x1800B8B05  jne  0x1800B8B24
#     0x1800B8B07  call 0x1800B23A0           ; l'objet de session
#     0x1800B8B0C  test rax, rax
#     0x1800B8B0F  je   0x1800B8B24
#     0x1800B8B11  mov  rcx, rax
#     0x1800B8B14  call 0x1800B23B0           ; rcx + 0x50
#     0x1800B8B19  mov  rcx, rax
#     0x1800B8B1C  call 0x1800B2330           ; <- LE CHOIX PARMI LES CINQ
#     0x1800B8B21  mov  r12d, eax
#
# Et `0x1800B2330` fait SIX OCTETS :
#
#     0x1800B2330  b8 16 00 00 00   mov eax, 0x16     ; 22 = du2
#     0x1800B2335  c3               ret
#
# Un bouchon. Il ignore son argument, il n'a qu'un appelant, et il rend une
# constante. C'est le motif dominant de ce build : la fonction qui, sur la
# borne, choisissait parmi DU1..DU5 selon la progression a ete remplacee par
# « toujours DU2 ». **Les cinq decors de Dural sont dans le jeu, entiers et
# charges par le meme chemin que les autres -- un seul est atteignable.**
#
# `--decors-dural [premier]` reecrit le bloc `0x1800B8B02`-`0x1800B8B20`
# (31 octets, EN PLACE, aucune caverne) par une TRANSLATION de cinq decors
# consecutifs vers du1..du5 :
#
#     cmp eax, lo ; jl fin ; cmp eax, lo+4 ; jg fin ; add eax, 21-lo ; fin:
#
# Deux precautions qui ne sautent pas aux yeux :
#
#  * `0x1800B8B21` (`mov r12d, eax`) est **preserve** : un autre chemin y saute
#    (`0x1800B8A2D`, la voie License Challenge). L'ecraser casserait ce mode
#    sans un seul message -- exactement la collision de caverne du 2026-09-06.
#  * la translation agit AVANT que l'index ne devienne le decor courant, donc
#    les cas particuliers indexes (8 et 9 dans `0x18018F030`, 16 et 40 dans
#    `0x18018FAC6`) ne se declenchent pas sur les decors traduits.
#
# Effet de bord voulu : le combat contre Dural rend desormais 21 (du1) au lieu
# de la constante 22 -- le bouchon n'est plus appele du tout.
DURAL_DECORS_VA = 0x1800B8B02
DURAL_DECORS_TETE = bytes.fromhex(
    '83f815751de89498ffff4885c07413488bc8e89798ffff488bc8e80f98ffff')
DURAL_DECORS_LO = 7        # cas riv jin sin djo  ->  du1 du2 du3 du4 du5

# ---------------------------------------------------------------------------
# LE DEUXIEME ET LE TROISIEME BOUCHON DE DURAL : cote ECRAN
#
# Trouves le 2026-09-07, apres que `--decors-dural` a ete valide a l'ecran.
# La substitution « du1 -> du2 » n'est pas un accident du constructeur de
# match : c'est une POLITIQUE, appliquee a TROIS endroits independants.
#
#   1. 0x1800B2330                le combat   -> traite par --decors-dural
#   2. 0x18017533D / 0x180175344  l'ecran de selection (dans 0x180175320)
#   3. 0x1801753A8                le chemin APM3 (dans 0x180175390, un cmove)
#
# Les deux derniers encadrent le meme tirage, `0x1801749F0` -- le TIREUR
# ALEATOIRE de decor. Il parcourt exactement la grille d'icones
# (`0x180400218`, pas 0x20, borne 0x2A0 = 21 cases), saute la case ALEATOIRE
# (0x29), saute ce que designe la table d'exclusion `0x180400770` -- qui vaut
# `-1`, donc n'exclut RIEN -- et saute ce qui a deja ete tire. Autrement dit :
# **du1 est bien dans le tirage, et les deux sites le remplacent apres coup.**
#
#     0x180175320 :  cmp eax, 0x15 ; jne suite ; [+0x60] = 0x16 ; [+0x5C] = 0x16
#     0x180175390 :  cmp eax, 0x15 ; mov ecx, 0x16 ; cmove eax, ecx
#
# `--decors-dural-grille` fait trois choses, toutes EN PLACE :
#
#   . `0x18017533B` : le `jne` devient un `jmp` -- UN octet. Le bloc de
#     substitution devient inatteignable et `[+0x5C] = eax` s'applique
#     toujours ;
#   . `0x1801753A8` : le `cmove` devient trois `nop` ;
#   . quatre cases de la grille passent de riv/jin/sin/djo a du2/du3/du4/du5.
#     La case `dur` (indice 20, icone `stage_icon_dur_c`) garde du1 : la
#     grille porte alors les CINQ decors de Dural, sans doublon.
#
# Les ICONES des quatre cases ne changent pas -- elles gardent
# `stage_icon_riv_c` et compagnie. C'est voulu : c'est ce qui permet de dire
# quelle case on a prise. L'apercu, lui, montre l'habillage `dur` pour les
# cinq, parce que la liste de `0x180174BF0` associe deja `dur`/`dur_stay` aux
# indices 0x15 a 0x19 -- rien a ajouter de ce cote.
# QUATRIEME site, trouve le 2026-09-07 apres l'essai de Frederic (« DU1 = DU2 »
# alors que les trois autres etaient deja leves). Il est dans `TaskSelStage::
# update` elle-meme, et c'est LUI qui decidait du decor reellement charge :
#
#     0x18017448A  mov r8d, [rbx+0x5c]     ; le decor selectionne
#     0x18017448E  cmp r8d, 0x15           ; 21 = du1
#     0x180174492  jne suite
#     0x180174494  mov r8d, 0x16           ; 22 = du2
#     0x18017449A  mov [rbx+0x5c], r8d     ; ... et on l'ECRIT
#
# Ici on ne detourne pas le saut : on change **l'immediat**, 0x16 -> 0x15. Le
# bloc s'execute alors a l'identique mais rend du1 a du1 -- aucune instruction
# morte, aucun flot modifie, un octet. C'etait la forme la plus sure, et c'est
# celle qu'il aurait fallu prendre pour les trois autres.
#
# Les quatre sites se retrouvent d'un coup avec `tools/substitutions.py 0x15
# 0x16` -- ecrit pour ca, parce que les chercher un par un en avait laisse un.
DURAL_GRILLE_UPD = (0x180174494, bytes.fromhex('41b816000000'),
                    0x180174496, bytes([0x15]))
DURAL_GRILLE_JNE = (0x18017533B, bytes.fromhex('7514'), bytes.fromhex('eb14'))
DURAL_GRILLE_CMOVE = (0x1801753A0,
                      bytes.fromhex('83f815b9160000000f44c1'),
                      0x1801753A8, bytes.fromhex('909090'))
# (adresse du champ +0x08 de la case, decor attendu, decor pose, nom de case)
DURAL_GRILLE_CASES = [
    (0x1804002B8, 8, 22, 'riv'),
    (0x180400378, 9, 23, 'jin'),
    (0x180400278, 10, 24, 'sin'),
    (0x180400338, 11, 25, 'djo'),
]

# ---------------------------------------------------------------------------
# AGRANDIR LA GRILLE : ajouter des cases au lieu d'en detourner
#
# Etabli le 2026-09-07. `--decors-dural-grille` DETOURNE quatre cases : riv,
# jin, sin et djo disparaissent de l'ecran. Ici on en AJOUTE.
#
# La place existe, et elle est contigue. Les deux tables de cases se suivent,
# et la liste d'exclusion vient juste apres :
#
#     0x180400210   grille hors ligne      21 cases x 0x20   = 0x2A0
#     0x1804004B0   grille bornes liees    22 cases x 0x20   = 0x2C0
#     0x180400770   liste d'exclusion (premiere entree -1 : n'exclut rien)
#
# soit 0x560 d'affilee = 43 cases. La table des bornes liees n'est lue que si
# `[0x180C3B6F0] + 0x1FE10` est non nul ; en console il est nul et c'est la
# branche HORS LIGNE qui tourne (`0x180174B6D : cmp ... , r8=0 ; je`). On
# etend donc la premiere table dans la seconde.
#
# Une case fait 0x20 octets :
#     +0x00 colonne   +0x04 ligne   +0x08 index du decor
#     +0x0C 0x14C     +0x10 0x14B   (le pas de cellule)
#     +0x14 0         +0x18 char*   ancre de position (un `stage_icon_xxx_c`)
#
# ET C'EST LA LE POINT : l'ancre n'est PAS obligatoire. `0x180173BD0` retient
# la derniere case ancree (`+0x60` colonne, `+0x64` ligne), calcule deux
# gradients (`xmm11` par colonne, `xmm10` par ligne) et, pour une case SANS
# ancre, extrapole : position = reference + (colonne - colonne_de_reference) x
# gradient. Une case neuve se pose donc toute seule, au pas de la grille, avec
# `+0x18 = 0`. C'est l'exact inverse de l'erreur du 2026-09-07, ou repointer
# `+0x18` sur une ancre DEJA UTILISEE empilait les cases au meme endroit.
#
# Quatre compteurs seulement -- les autres `0x15` du voisinage sont des
# identifiants de calques AET (`0x18017481B`, `0x180174FBC`, `0x180175056`,
# `0x180175129`) ou l'index du decor du1 (`0x180174E13`), pas des comptes.
GRILLE_TABLE_VA = 0x180400210
GRILLE_CASE = 0x20
GRILLE_N = 21
GRILLE_PAS_X, GRILLE_PAS_Y = 0x14C, 0x14B
# (adresse de l'immediat, taille, valeur attendue, role)
GRILLE_COMPTES = [
    (0x1801746D2 + 2, 4, GRILLE_N, 'le compte passe au constructeur 0x180173BD0'),
    (0x18017493C + 3, 1, GRILLE_N, 'la boucle qui cherche la case ALEA'),
    (0x180174BBE + 3, 1, GRILLE_N, 'la boucle index de decor -> case'),
    (0x180174AA0 + 3, 4, GRILLE_N * GRILLE_CASE,
     'la borne du tirage au sort (0x1801749F0)'),
]
# Les cases ajoutees : (colonne, ligne, index de decor). Par defaut la 4e
# ligne, avec les quatre decors de Dural qui ne sont PAS dans la grille --
# du1 y est deja, case ligne 2 colonne 6.
GRILLE_AJOUTS = [(0, 3, 22), (1, 3, 23), (2, 3, 24), (3, 3, 25)]

# ---------------------------------------------------------------------------
# LES VARIANTES D'UN DECOR, AU BOUTON SELECT (2026-09-08)
#
# Demande de Frederic : le curseur reste sur UNE case, et la barre espace fait
# defiler les variantes du decor. Les cinq decors de Dural sont les variantes
# d'un meme lieu -- du1 SNOW, du2 ECLIPSE/METEOR, du3 SUBMERSION, du4 STORM,
# du5 SPACE.
#
# TROIS MESURES RENDENT CE CORRECTIF POSSIBLE
#
# 1. La barre espace est un canal LIBRE. Le stub la met sur le code brut 6, et
#    la vraie `apm.dll` ne l'affirme jamais (« le code 6 n'a pas de bit et rend
#    toujours faux »). Deux sites du moteur l'interrogent deja -- 0x18023B269
#    et 0x18023BA48 -- donc la forme de la requete est connue. On la copie de
#    `0x1801A2BC0` (VALIDER, code 7) :
#
#        mov rcx, [0x180C3B6F8] ; mov edx, 6 ; mov rax, [rcx]
#        call [rax + 0x160]
#
# 2. `[rbx+0x5C]`, le decor sous le curseur, n'est reecrit QUE quand le curseur
#    bouge : le bloc 0x18017476B-0x180174781 est garde par `test al,al ; je
#    epilogue` en 0x180174769. Une valeur qu'on y fait tourner PERSISTE donc.
#
# 3. `0x180174BF0(this)` rafraichit l'apercu ; on le rappelle apres chaque
#    rotation.
#
# LE POINT D'ACCROCHE est `0x180174710`, la queue commune jouee a chaque trame
# (plusieurs `jmp 0x180174710` y menent). Six octets a reprendre :
# `xor edx,edx ; lea rcx,[rbx+0x70]` -- on les rejoue dans la greffe.
#
# PAS DE `sub rsp` : le code d'origine appelle `0x1801724A0` juste apres, sans
# rien ajuster. L'espace d'ombre est donc deja reserve par le prologue de la
# fonction, et l'alignement est bon.
# CE QUE LA MESURE DU 2026-09-08 A CORRIGE
#
# Premiere version : le detour ecrivait `[rbx+0x5C]` en `0x180174710`. Il
# marchait -- 300 passages, `al = 1` a chaque appui, index ecrit a 22 -- et
# pourtant seul du1 se chargeait. Un point d'arret MATERIEL en ecriture sur le
# champ a nomme les autres ecrivains :
#
#     rva 0x17477D  -> ecrit -1        (0x180174776)
#     rva 0x174784  -> ecrit la case   (0x180174781, la RECOMPUTATION depuis
#                                       le curseur)
#     rva 0x175354  -> 1372 acces      (0x180175351, la ROULETTE de la case
#                                       ALEA, alimentee par 0x1801749F0)
#
# Notre ecriture arrivait donc AVANT la recomputation, qui la defaisait dans
# la meme trame. La lecon est la meme que partout ailleurs ici : ce n'est pas
# le raisonnement qui a tranche, c'est le processeur.
#
# D'ou la forme actuelle, en deux entrees et un sous-programme :
#
#   ENTREE A, en 0x180174710 : lit la barre espace et fait tourner le NUMERO
#     DE VARIANTE, garde dans la greffe -- plus dans `[rbx+0x5C]`, qui ne nous
#     appartient pas. Puis applique.
#   ENTREE B, en 0x1801747C0 : APRES la recomputation, juste avant le
#     rafraichissement de l'apercu. Applique de nouveau -- c'est elle qui a le
#     dernier mot.
#   APPLIQUER : si `[rbx+0x5C]` est dans l'anneau, y pose `premier + numero`.
VARIANTES_HOOK_VA = 0x180174710
VARIANTES_HOOK_TETE = bytes.fromhex('33d2' '488d4b70')
VARIANTES_RETOUR_VA = 0x180174716
VARIANTES_HOOK_B_VA = 0x1801747C0
VARIANTES_HOOK_B_TETE = bytes.fromhex('488bcb' 'e828040000')
VARIANTES_RETOUR_B_VA = 0x1801747C8
VARIANTES_ENTREES_VA = 0x180C3B6F8       # -> l'objet d'entrees
VARIANTES_APERCU_VA = 0x180174BF0        # rafraichit l'apercu
VARIANTES_CODE_ESPACE = 6

# LES ANNEAUX. Un anneau = les indices de decor entre lesquels la barre espace
# fait tourner, et les noms a afficher. Le PREMIER indice est la BASE : c'est
# celui que la case de la grille porte naturellement, celui que la recomputation
# du curseur (0x180174781) remet a chaque trame, et celui avec lequel on
# rafraichit l'apercu -- la liste de 0x180174BF0 n'a que 26 entrees et EFFACE
# les trois couches quand elle ne trouve rien.
#
# Rien n'oblige les indices a se suivre : le dojo de VF5 R vit sur un
# emplacement libre (`trm`, indice 26), a l'autre bout de la table.
# Vingt anneaux : les dix-neuf decors de VF5 R (une case de grille
# chacun) plus celui de Dural. Le tableau des noms pese alors
# 20 x 8 x 32 = 5120 octets, d'ou la taille de la greffe.
VARIANTES_MAX_ANNEAUX = 20
# HUIT VARIANTES PAR ANNEAU -- SEIZE AVEC LE VF5 D'ORIGINE (2026-09-11).
# La case de Dural en demande NEUF : les cinq de Final Showdown et les quatre
# de ver.B. Le rang d'une variante vaut `anneau * MAX + position`, et le code
# de la greffe le decoupe par DECALAGE (`shr ecx, 3`) et par MASQUE
# (`and eax, ~7`) : MAX doit rester une puissance de deux, donc 16.
#
# ET ON NE LE CHANGE QUE POUR LE BUILD QUI EN A BESOIN. Le build VF5 R
# (`decors_5r.cmd`) est essaye a l'ecran avec huit : sa greffe doit rester
# identique a l'octet pres. D'ou la lecture de la ligne de commande ICI, a
# l'import -- les tailles de la greffe en derivent toutes.
VARIANTES_MAX_VARIANTES = 16 if '--variantes-vf5' in sys.argv else 8
VARIANTES_DECALAGE = VARIANTES_MAX_VARIANTES.bit_length() - 1
assert 1 << VARIANTES_DECALAGE == VARIANTES_MAX_VARIANTES
VARIANTES_ANNEAU_DURAL = (
    [21, 22, 23, 24, 25],
    ['SNOW', 'ECLIPSE', 'SUBMERSION', 'STORM', 'SPACE'])
# Le dojo d'Akira : Final Showdown en 11, la version VF5 R sur l'emplacement
# d'accueil. Le libelle est la GENERATION, ce que Frederic a demande le
# 2026-09-08.
#
# CE FUT UNE CONSTANTE, ET ELLE ETAIT FAUSSE. Elle disait `[11, 26]` -- 26,
# c'est `trm` -- alors que le clonage du descripteur visait
# `VARIANTES_TRM_INDEX = 29`, c'est-a-dire `evo00`. Le correctif posait donc le
# decor a un endroit et faisait defiler vers un autre : la barre espace aurait
# montre le decor TERMINAL. Personne ne l'a jamais vu, l'option n'ayant pas ete
# relancee depuis. C'est la raison pour laquelle l'emplacement est desormais un
# ARGUMENT dont TOUT est derive -- indice, objset, collision, anneau.
def variantes_anneau_djo(indice):
    return ([VARIANTES_DJO_INDEX, indice],
            ['VIRTUA FIGHTER 5 FS', 'VIRTUA FIGHTER 5 R'])
# LE DESSIN DU NOM DE VARIANTE
#
# L'ecran de selection ne dessine aucun texte -- le resolveur de libelles a
# 276 appelants, aucun dans 0x18017xxxx. Mais le texte ne passe PAS par le
# repartiteur : c'est une fonction ordinaire, et on la connaissait deja sans le
# savoir. `0x18019BEB2` est l'appel que `--sans-now-loading` neutralise, et il
# dessine « NOW LOADING » a x=640, y=678 sur un ecran de 1280x720.
#
#     0x18019A8C0(desc)          construit le DESCRIPTEUR, 0x50 octets
#     0x18019A9D0(style)         construit le STYLE, 0x40 octets
#     0x18019B6F0(style, 2)      pose le mode
#     0x18019B830(style, xmm1)   pose la taille (32.0, lue en 0x18034AF78)
#     desc+0x08 = -1             la couleur, blanc
#     desc+0x34/38/3C/40         x1 y1 x2 y2, en pixels d'ecran
#     desc+0x48 = style
#     0x18019B2E0(desc, 0x28, texte)    LE DESSIN
#
# Les champs `+0x24 = 7` et `+0x2C = 9` que le site d'appel reecrit sont deja
# les valeurs par defaut du constructeur : inutile de les reposer.
#
# `desc` et `style` sont des objets de PILE chez CRI ; on les met dans la
# greffe, ou ils ne genent personne -- un seul fil dessine, une fois par trame.
VARIANTES_DESC_NEUF = 0x18019A8C0
VARIANTES_STYLE_NEUF = 0x18019A9D0
VARIANTES_STYLE_MODE = 0x18019B6F0
VARIANTES_STYLE_TAILLE = 0x18019B830
VARIANTES_DESSIN = 0x18019B2E0
VARIANTES_POLICE_VA = 0x18034AF78        # 32.0

# L'EMPLACEMENT LIBRE QUI RECOIT LE DOJO DE VF5 R
#
# `trm` (indice 26, objset 43) est un decor d'essai : le prendre ne coute aucun
# decor reel et ne touche aucune borne.
#
# PREMIERE VERSION, ET ELLE ETAIT FAUSSE. Je n'avais recopie que trois champs
# (objets, collision, musique) et j'ai explique l'image ratee par l'eclairage de
# VF5 R. Frederic a tranche en relancant `decor_5r_akira.cmd` : « les couleurs
# et eclairages sont bons !!! » -- le MEME decor, les MEMES fichiers
# d'eclairage, sur l'emplacement `djo`. Les fichiers n'y etaient donc pour rien.
#
# La difference se lit en comparant les deux descripteurs champ par champ. Un
# descripteur fait 0xF0 octets et n'en dit pas trois, il en dit quinze :
#
#   +0x2C..+0x34  trois identifiants que SEULS huit decors portent (ter, jin,
#                 djo, umi, slk, aur, tan, du5). trm : -1.
#   +0xB8         2 pour ban, cas, jin, djo, are, bar, gym. trm : 0.
#   +0xC0         un pointeur chez djo. trm : 0.
#   +0xD0         lu par 0x18018F440, compare a 0 et a 4 : il AIGUILLE un rendu
#                 (0x180084F58, 0x18011F7D1). djo : 1. trm : 0.
#   +0xD4         lu par 0x18018F630, puis `cmp eax,9` et un SAUT INDIRECT sur
#                 dix cas, chacun posant une constante flottante differente
#                 dans xmm8 (0x180204863). djo : 2. trm : 0.
#   +0xE4/+0xE8   la taille de l'aire. djo : 12x12. trm : 16x16.
#
# Autrement dit `trm` n'est pas un dojo mal eclaire : c'est un decor d'ESSAI,
# et ses proprietes de rendu sont celles d'un decor d'essai.
#
# LE CORRECTIF EST DONC UN CLONAGE. On recopie le descripteur de djo EN ENTIER
# sur celui de trm, et on ne garde en propre que ce qui doit changer :
#
#   +0x10         l'objset : 43, celui de l'emplacement
#   +0x14..+0x24  les cinq objets, empaquetes (objset << 16) | rang. djo porte
#                 0x1C0072/76/75/74/73, soit objset 28, rangs 114 118 117 116
#                 115 (gnd, ring, sky, sdw, reflect) ; le decor importe garde
#                 ces rangs -- c'est ce qui rendait l'import gratuit -- mais il
#                 vit desormais dans l'objset 43.
#   +0x48         la collision : celle de VF5 R, posee sous le nom de
#                 l'emplacement. Aucune chaine `rom/STGTRM_COLI...` n'existe
#                 dans le binaire, on l'ecrit dans le mou de `.rdata` APRES
#                 celle de DU2 -- deux correctifs se disputeraient l'adresse en
#                 silence sinon.
#
# CE QU'ON NE PEUT PAS CLONER, et c'est une contrainte du FORMAT PE, pas un
# choix : dix des champs de djo sont des POINTEURS, et une adresse d'image
# n'est juste que la ou une RELOCATION la suit au rebasage. Le descripteur de
# djo en a dix-sept, celui de trm SEPT (0x00 0x08 0x48 0x50 0x58 0x60 0x68).
# Les dix autres -- les neuf variantes de musique (+0x70..+0xB0) et +0xC0 --
# resteraient a la base preferee 0x180000000 et pointeraient dans le vide.
# On les remet donc a zero. Consequence assumee : sur cet emplacement, seule la
# musique principale joue, pas les neuf reprises VF1..VF5FS.
VARIANTES_DJO_INDEX = 11
# L'EMPLACEMENT D'ACCUEIL. Il ne se choisit PAS librement : `trm` (26) est le
# decor TERMINAL, REPARE et VALIDE A L'ECRAN le 2026-09-05. Le recycler l'a
# casse le 2026-09-08 -- son descripteur avait ete ecrase par un clone de djo.
# Un emplacement « libre » qui a deja ete repare n'est plus libre.
VARIANTES_EMPLACEMENTS_INTERDITS = {
    26: 'trm : le decor TERMINAL, repare et valide a l ecran le 2026-09-05',
    11: 'djo : le dojo de Final Showdown lui-meme',
}
# L'EMPLACEMENT D'ACCUEIL SE CHOISIT, ET RIEN N'EN EST PLUS ECRIT EN DUR.
#
# Premiere version : une constante, `trm`. Elle a coute le decor TERMINAL.
# Deuxieme version : une constante, `evo00` -- et l'anneau de la barre espace
# etait reste sur 26, `trm`. Le correctif clonait a un endroit et faisait
# defiler vers un autre.
# Celle-ci : `--variantes-djo <code>`, et l'indice, l'objset, la chaine de
# collision et l'anneau en sont tous DERIVES.
#
# LE CODE DOIT FAIRE TROIS LETTRES. `importer_decor.py --vers` reecrit les noms
# internes de l'archive (`stgdjo_obj.bin` -> `stgtrs_obj.bin`) par substitution
# EN PLACE : `stgevo00_obj.bin` ne tient pas dans la place de `stgdjo_obj.bin`.
# Les emplacements a trois lettres encore libres, MESURES par
# `tools/emplacements.py` : tst ts3 wht cid trs.
VARIANTES_DJO_EMPLACEMENT = 'trs'
VARIANTES_DESC_TABLE = 0x180403430
VARIANTES_DESC_PAS = 0xF0
VARIANTES_DJO_RANGS = (114, 118, 117, 116, 115)
def variantes_tete_essai(objset):
    """Ce qu'un decor d'ESSAI porte en +0x14 : deux objets, rien d'autre.

    On ne fige plus la valeur : elle depend de l'objset de l'emplacement, et
    figer celle de `trm` avait rendu la garde inutilisable ailleurs.
    """
    return struct.pack('<5I', (objset << 16) | 0, 0xFFFFFFFF,
                       (objset << 16) | 1, 0xFFFFFFFF, 0xFFFFFFFF)
# Le mou de .rdata, apres les 24 octets que `--du2-collision` y prend deja
# (0x180641B60..0x180641B78). 0x180641B80 est le suivant aligne a 16, et le mou
# court jusqu'a 0x180641C00 : 128 octets, on en prend 24 pour un code a trois
# lettres. La borne est verifiee, elle n'est plus supposee.
VARIANTES_COLI_CHAINE_VA = 0x180641B80
VARIANTES_COLI_MOU_FIN = 0x180641C00
VARIANTES_DESC_COLI = 0x48
VARIANTES_DESC_BGM = 0x68
VARIANTES_DESC_OBJETS = 0x14
VARIANTES_DESC_OBJSET = 0x10
# Les offsets ou djo porte un pointeur mais ou un decor d'ESSAI n'a PAS de
# relocation. Recopier une adresse la serait la meme faute que les pointeurs
# absolus de la greffe : juste au repos, faux des le rebasage.
#
# Mesure du 2026-09-09 sur les six emplacements candidats (tst ts3 wht cid trs
# evo00) : les six portent EXACTEMENT les memes SEPT relocations -- 0x00 0x08
# 0x48 0x50 0x58 0x60 0x68 -- la ou djo en a dix-sept. La liste ci-dessous vaut
# donc pour n'importe lequel d'entre eux, et non pour le seul `trm`.
VARIANTES_DESC_SANS_RELOC = (0x70, 0x78, 0x80, 0x88, 0x90, 0x98,
                             0xA0, 0xA8, 0xB0, 0xC0)


def variantes_emplacement(argv):
    """Le code d'emplacement qui suit `--variantes-djo`, ou le defaut.

    Rend `(code, indice)` ; l'indice vaut -1 si le code n'est pas un decor.
    """
    i = argv.index('--variantes-djo') + 1
    code = (argv[i] if i < len(argv) and not argv[i].startswith('--')
            else VARIANTES_DJO_EMPLACEMENT)
    return code, (DECOR_NOMS.index(code) if code in DECOR_NOMS else -1)
# LE CRENEAU 4 : la phase de RENDU
#
# Mesure du 2026-09-08. Le dessin s'executait avec des parametres PARFAITS --
# chaine a une adresse reelle, blanc opaque, modes 7 et 9, coordonnees 640/460,
# style sain (police valide, metriques 48/48, echelles 32/32/0,667) -- et rien
# n'apparaissait. Parce qu'on l'emettait depuis l'`update`.
#
# `0x18019BDD0`, qui dessine « NOW LOADING », n'a AUCUN appelant : une seule
# reference, un pointeur en `.rdata`. C'est le **creneau 4** d'une vtable, donc
# une methode virtuelle appelee par le moteur a la phase de RENDU -- pas a
# l'update, qui est le creneau 2.
#
# Et le creneau 4 de `TaskSelStage` est un BOUCHON (`0x180007430`, `ret 0`) :
# cet ecran ne dessine rien en propre, tout y est de l'AET. Le creneau est donc
# libre, et il est RELOCALISE (type 10) -- y ecrire une adresse d'image est
# donc sur au rebasage, contrairement aux pointeurs de la greffe.
# OU DESSINER : DEUX ESSAIS RATES, PUIS LA MESURE QUI TIENT
#
# 1. Creneau 4 de `TaskSelStage` : le texte s'affiche, mais SOUS les couches
#    AET de l'ecran.
# 2. Creneau 6 de `TaskSelStage` : plus rien du tout. Les bouchons `ret 0` des
#    creneaux 5 et 6 ne prouvaient donc PAS qu'ils sont appeles -- j'en avais
#    deduit le contraire, a tort.
#
# Ce qui reste acquis : au creneau 4 le dessin PART, et `TaskSelector`, le
# parent, OCCUPE son propre creneau 4 (`0x18016CEE0`) -- c'est lui qui dessine
# le panneau, apres son enfant. On DETOURNE donc ce creneau-la : on appelle
# l'original, puis on dessine. Le texte passe ainsi apres le panneau.
#
# `TaskSelStage` est un MEMBRE de `TaskSelector`, en `+0x3B0` : le `this` du
# parent donne donc l'enfant sans rien chercher.
# LA MESURE QUI A TRANCHE (2026-09-08, tools/pister_ordre.py). La suite des
# appels, relevee sur 120 evenements, est parfaitement reguliere :
#
#     NOTRE DESSIN -> AetMgr 4 -> AetMgr 6 -> AetMgr 2 -> NOTRE DESSIN -> ...
#
# `AetMgr` passe donc APRES nous a chaque fois, et son DERNIER creneau est le
# 2. C'est lui qui nous recouvre. On le detourne : l'original d'abord, notre
# texte ensuite.
#
# Deux precautions, parce que `AetMgr` est GLOBAL et tourne sur tous les
# ecrans :
#   . le singleton `TaskSelector` vaut zero au repos -- on teste avant de s'en
#     servir ;
#   . `DESSINER` ne dessine que si l'etat de `TaskSelStage` vaut 2, la
#     navigation, sinon le nom s'afficherait ailleurs.
# LA PROFONDEUR EXISTE, ET ELLE SE CALCULE (desassemble le 2026-09-08)
#
# `0x180187C00` soumet la commande de dessin au contexte 2D global
# (`0x180719900`), et `0x18018CA20` l'insere. La clef y est CALCULEE :
#
#     clef = (cmd+0x1C) + 1 + ((cmd+0x18 + cmd+0x14) << 5)
#     puis  [contexte + clef*16]  -> une tete de liste et un compteur
#
# C'est un tableau de COMPARTIMENTS parcouru dans l'ordre : clef plus grande =
# dessine plus tard = AU-DESSUS.
#
# La commande du texte tire `cmd+0x1C` de `desc+0x24` (7 par defaut) et
# `cmd+0x18` de `desc+0x28` (0). Mais elle ne pose PAS `cmd+0x14` : il reste a
# -1, et `0x18018CA2B` retombe alors sur **`[contexte+0x828]`**, le CALQUE
# COURANT. C'est ce calque que l'AET a monte avant de dessiner, et c'est pour
# cela que notre texte passait dessous quel que soit le moment de l'appel.
#
# PREMIER JET, ET IL A PLANTE : monter `[contexte+0x828]` de 8. Frederic,
# 2026-09-08 : « le jeu crash juste avant de pouvoir selectionner l'icone du
# decor de Dural. » La raison est arithmetique, et elle se LIT :
#
#   0x18018A030  mov ecx, 0x838 ; call operator new    <- le contexte fait
#                                                         0x838 octets
#   0x18018A092  call 0x1802FE160 (rbx+0x10, 0x10, 0x80, ctor, dtor)
#                                                      <- 128 compartiments
#                                                         de 16 octets, en +0x10
#   +0x818, +0x820 deux champs, +0x828 le calque courant. 0x838 : c'est plein.
#
# Le « +1 » de la clef est exactement le decalage de 0x10 du tableau. L'INDICE
# REEL est donc :
#
#     indice = (desc+0x24) + (((desc+0x28) + calque) << 5)     dans 0..127
#
# soit QUATRE calques de TRENTE-DEUX rangs. Monter le calque de 8 demandait
# l'indice 8+256 = 264, deux kilo-octets au-dela du contexte : lecture d'un
# pointeur de hasard, et l'acces invalide.
#
# LE CORRECTIF est donc BORNE par construction, et il ne touche a rien de
# global : on ne modifie que NOTRE descripteur.
#
#   desc+0x28 <- plafond - calque     (le calque effectif vaut toujours 3)
#   desc+0x24 <- ordre                (31, le dernier rang du calque 3)
#
# L'indice vaut alors 31 + 3*32 = 127 : le TOUT DERNIER compartiment, parcouru
# en dernier, donc dessine par-dessus tout le reste -- et il ne peut pas sortir
# du tableau. Si le calque courant depassait deja le plafond, on ne dessine
# pas : mieux vaut pas de texte qu'un acces invalide.
#
# Les deux champs sont a nous seuls : le constructeur du descripteur
# (0x18019A8E6) pose +0x24 = 7 et +0x28 = 0, et 0x18019B1D0/D6 sont les SEULS
# lecteurs -- verifie sur toute la plage 0x18019A8C0..0x18019B2E0.
VARIANTES_CTX_VA = 0x180719900           # le contexte 2D
VARIANTES_CALQUE_OFF = 0x828             # le calque courant, dans le contexte
VARIANTES_PLAFOND = 3                    # le dernier calque du tableau
VARIANTES_ORDRE = 31                     # le dernier rang de ce calque

VARIANTES_VTABLE_SLOT_VA = 0x180400A38   # TaskSelStage, creneau 4
VARIANTES_SLOT_ORIGINAL = 0x180007430    # le bouchon `ret 0`
VARIANTES_SELECTEUR_VA = 0x180714928     # le singleton TaskSelector
VARIANTES_SELSTAGE_OFF = 0x3B0           # TaskSelStage dans TaskSelector
VARIANTES_VTABLE_SLOT_TETE = struct.pack('<Q', VARIANTES_SLOT_ORIGINAL)
# La position, en pixels d'ecran. Le rendu tombe une cinquantaine de pixels
# PLUS HAUT que la valeur donnee -- mesure a l'ecran : 460 rendait ~405 (sur la
# legende), 500 rendait ~448 (sur le bord du cadre).
#
# 460 EST LA POSITION VALIDEE PAR FREDERIC. Elle avait ete abandonnee pour 490
# uniquement pour fuir la plaque AET « Sanctuary / Single Wall 16x16 », qui
# couvre le rendu jusqu'a ~420 et sous laquelle le texte disparaissait. Cette
# contrainte n'existe plus : depuis que le dessin part au rang 127, le dernier
# compartiment du contexte 2D, il passe DEVANT la plaque. On rend donc la
# position qu'il avait choisie. Frederic, 2026-09-08 : « remonte le texte, il
# n'est plus a la position validee. »
# 2026-09-08, sur capture : « c'est bon le texte est enfin au premier plan,
# redescend le juste un peu vers le bas. » 460 posait SNOW colle sous
# « Single Wall 16x16 » ; 478 l'a descendu d'une vingtaine de pixels.
# Puis, sur la capture suivante : « remonte un peu le texte. » 470 rend la
# moitie du pas -- la fenetre utile est etroite, entre le bas de la legende et
# le bord de l'apercu (500 rendait ~448, sur le bord).
VARIANTES_XY = (640.0, 470.0)
# La taille de police. Le site d'origine lit 32.0 en 0x18034AF78 ; on garde la
# NOTRE dans la greffe, pour pouvoir la changer sans toucher au moteur.
# `0x18019B830` en tire les echelles en divisant par les metriques (48).
VARIANTES_TAILLE = 24.0
# LE LISERE. Le texte se detachait mal du decor : on le dessine NEUF fois --
# huit passes noires decalees de deux pixels tout autour, puis la blanche au
# centre. C'est le contour a la main, et il ne demande aucune option du moteur
# qu'il faudrait d'abord trouver.
VARIANTES_LISERE = 2.0
VARIANTES_PASSES = [(-1, -1), (0, -1), (1, -1),
                    (-1, 0), (1, 0),
                    (-1, 1), (0, 1), (1, 1)]
VARIANTES_NOIR = 0xFF000000
VARIANTES_BLANC = 0xFFFFFFFF
VARIANTES_PAS = 32                       # pas fixe des chaines : il permet de
                                         # les adresser SANS pointeur absolu.
                                         # 32 et non 16 depuis que le libelle
                                         # est une generation entiere
                                         # (« VIRTUA FIGHTER 5 FS », 19 o).

# Emplacements fixes dans la greffe : plus lisibles a relire qu'un calcul de
# tailles, et il y a 4096 octets.
VAR_A = 0x000                            # entree A
VAR_B = 0x0C0                            # entree B
VAR_TROUVE = 0x180                       # TROUVER : indice de decor -> rang
VAR_APPL = 0x1C0                         # le sous-programme d'application
VAR_DESS = 0x300                         # le sous-programme de dessin
VAR_SLOT = 0x500                         # le CRENEAU 4 de la vtable
# --- les donnees ---
# LA FRONTIERE CODE / DONNEES. Le code de la greffe s'arrete ici ; les six
# sous-programmes ci-dessus sont bornes dessus.
VAR_DONNEES = 0x600
VAR_RANG = 0x610                         # le rang trouve (anneau*8 + position)
VAR_APPLIQUE = 0x614                     # l'indice applique, le temps de
                                         # rafraichir l'apercu sur la BASE
VAR_PLAFOND = 0x618                      # le calque le plus haut du tableau
VAR_ORDRE = 0x61C                        # le rang dans ce calque
VAR_X = 0x620                            # la position, modifiable a la main
VAR_Y = 0x624
VAR_PASSE = 0x628                        # le compteur de passes du lisere
VAR_TAILLE = 0x62C                       # la taille de police, modifiable
VAR_DESC = 0x640                         # le descripteur de texte, 0x50
VAR_STYLE = 0x6A0                        # le style, 0x40
VAR_PASSES = 0x700                       # 9 passes de {dx, dy, couleur}
# LES TROIS TABLEAUX SE SUIVENT, ET LEURS TAILLES SONT DERIVEES. Elles etaient
# en dur (0x780 / 0x790 / 0x820) tant qu'il n'y avait que quatre anneaux ; les
# dix-neuf decors de VF5 R en demandent vingt, et un offset en dur se serait
# recouvert en silence.
VAR_COMPTES = 0x780                      # un u32 : la longueur de chaque anneau
VAR_IDX = VAR_COMPTES + VARIANTES_MAX_ANNEAUX * 4      # les indices de decor,
                                         # -1 pour une case inutilisee
VAR_TEXTES = VAR_IDX + (VARIANTES_MAX_ANNEAUX * VARIANTES_MAX_VARIANTES * 4)
# LE NUMERO COURANT PAR ANNEAU. Il etait a 0x600 avec **quatre** entrees en dur,
# et il y est reste quand les anneaux sont passes de 4 a 20 : au dix-neuvieme,
# `VAR_NUM[anneau]` lisait -- et ECRIVAIT -- dans `VAR_RANG`, puis dans le
# descripteur de texte et son style. D'ou le plantage du 2026-09-10, mesure par
# `pister_plantage.py` : `mov eax, [rdx + rcx*4]` en `.greffe+0x1E7` avec
# rcx = 0x43EB0048, un flottant lu dans `VAR_DESC`. Il est donc DERIVE, comme
# les trois autres tableaux, et pose apres eux -- la ou il y a de la place.
VAR_NUM = (VAR_TEXTES
           + VARIANTES_MAX_ANNEAUX * VARIANTES_MAX_VARIANTES * 32)
VAR_FIN = VAR_NUM + VARIANTES_MAX_ANNEAUX * 4


# ---------------------------------------------------------------------------
# WATER_RING : UN OBJET ECRIT EN DUR DANS LE CODE (2026-09-10)
#
# Frederic : « decor de Eileen : il manque l'eau ou le sable du ring ». Eileen,
# c'est `MON` dans `game_score.txt`, donc `STGSLK` -- l'indice 15, dont notre
# variant est `sk5` (53). Son modele demande quatre taches d'effet ; WATER_RING
# en est.
#
# `TaskEffectWaterRing` n'a **aucune table indexee par le decor**. Son creneau 4
# dessine un objet nomme par un LITTERAL :
#
#     0x180085620  cmp byte ptr [rcx+0x5c], 0
#     0x180085624  je  0x18008563A
#     0x180085626  xor r8d, r8d
#     0x180085629  lea rdx, [rip+0x50]
#     0x180085630  mov ecx, 0x27006E        <- (39 << 16) | 110
#     0x180085635  jmp 0x1800EC520
#
# `0x27006E` = l'objet 110 de l'objset 39, `STGSLK_WATER_RING`. Le moteur est
# donc cable sur le decor de Final Showdown : notre `sk5` est l'objset 6161, et
# rien ne s'affichait.
#
# LE REMEDE. `rcx` porte encore la tache en 0x180085630 (rien ne l'a touche
# depuis l'entree), et `setStage` a range l'indice du decor en `+0x58`. Les cinq
# octets du `mov ecx, imm32` deviennent donc un `call` vers un stub de la
# greffe, qui balaie une petite table `{indice, objet}` et rend le LITTERAL
# D'ORIGINE quand l'indice n'y est pas -- `slk` se comporte exactement comme
# avant, au registre pres.
#
#     mov eax, [rcx+0x58]          l'indice du decor
#     lea r9, [rip+table]
#   L: cmp dword [r9], -1  / je DEFAUT
#     cmp eax, [r9]        / je TROUVE
#     add r9, 8            / jmp L
#   DEFAUT: mov ecx, 0x27006E ; ret
#   TROUVE: mov ecx, [r9+4]   ; ret
#
# `eax` et `r9` sont volatils et ne portent aucun des trois arguments du saut
# terminal (`ecx`, `rdx`, `r8d`).
GREFFE_POSEE = None                      # (va, offset) une fois posee
EAU_ANNEAU_SITE = 0x180085630            # le `mov ecx, imm32`
EAU_ANNEAU_DEFAUT = 0x27006E             # (39 << 16) | 110, l'objet de slk
EAU_ANNEAU_MAX = 8                       # entrees de la table, terminateur compris

GRE_EAU = 0x1EA0                         # le stub, dans la greffe
GRE_EAU_TABLE = 0x1EE0                   # sa table {indice, objet}
if VARIANTES_MAX_VARIANTES > 8:
    # Seize variantes par anneau : la table des noms passe de 5 a 10 Ko et
    # repousse VAR_FIN au-dela de 0x1EA0. Le stub suit, derriere elle.
    GRE_EAU = (VAR_FIN + 0x3F) & ~0x3F
    GRE_EAU_TABLE = GRE_EAU + 0x40
# Les stubs des taches de generation et leurs tables : tout le reste de la
# greffe (voir GENERATION_STUBS). Le patcheur REFUSE s'ils n'y tiennent pas.
GRE_GEN = (GRE_EAU_TABLE + EAU_ANNEAU_MAX * 8 + 0x3F) & ~0x3F


# ---------------------------------------------------------------------------
# LES TACHES QUI LISENT UN DOSSIER A ADRESSE FIXE (2026-09-11)
#
# Frederic : « applique les effets VF5 a VF5 [...] decompile les effets dont
# on ne sait pas se servir ». FOG_RING, SNOW_RING et RAIN n'ont PAS de table :
# FS lit UN SEUL dossier, a une adresse fixe de `.data`, par une dizaine de
# chargements `[rip+d]` -- et seulement dans une fonction :
#
#   FOG_RING   0x1806431C8 (0x3C, du2)  lu par 0x180072130 seule, appelee par
#              le setStage 0x180072B60 (`call` en 0x180072B80)
#   SNOW_RING  0x180643450 (0x2C, yuk)  lu par 0x18007D820 seule, appelee par
#              l'init 0x18007DA60 (`call` en 0x18007DA8A)
#   RAIN       0x180643280 (0x5C, bar)  recopie dans l'etat par l'init
#              0x180079170 ; le setStage de Rain est le `ret 0` commun
#              (0x180007430, creneau 7 de la vtable 0x18034EFC0)
#
# Les trois se lisent APRES que l'indice du decor est connu : l'etat 3 de
# 0x18006F380 appelle `vtable[7](tache, indice)` juste apres avoir cree la
# tache (`0x180245830` ne fait que l'inscrire ; l'init tourne a sa premiere
# trame -- c'est pourquoi l'init de WetCloth peut lire l'indice en +0x60).
#
# Le remede : un stub recopie dans le dossier de FS celui du decor qu'on
# charge -- le NOTRE si l'indice est dans sa table, sinon L'ORIGINAL DE FS,
# relu dans `.origine` et range en fin de table -- puis rend la main a la
# fonction d'origine. Un decor de FS relit donc exactement ses octets.
#
#     lea  rax, [rip+table]      ; nos dossiers, puis celui de FS
#     mov  r9d, n
#  L: test r9d, r9d / je COPIE   ; plus rien : rax est sur celui de FS
#     cmp  edx, [rax] / je COPIE
#     add  rax, pas / dec r9d / jmp L
#  COPIE: lea r8, [rip+dossier_fs] ; mov r9,[rax+k] ; mov [r8+k],r9 ...
#     jmp  <fonction d'origine>  (ou `ret` pour le setStage de Rain)
#
# rax, r8, r9 sont volatils ; rcx et edx (les deux arguments) ne bougent pas.
GENERATION_STUBS = {
    'FOG_RING': dict(tache=18, site=0x180072B80, appel=0x180072130,
                     dossier=0x1806431C8, pas=0x3C, indice=True),
    'SNOW_RING': dict(tache=15, site=0x18007DA8A, appel=0x18007D820,
                      dossier=0x180643450, pas=0x2C, indice=True),
    'RAIN': dict(tache=8, vtable=0x18034EFF8, defaut=0x180007430,
                 dossier=0x180643280, pas=0x5C, indice=False),
}
# WET_CLOTH : pas de dossier, un SCALAIRE choisi par `indice == 19` (bar) :
#
#     0x18008599F  vmovd xmm0, [rbx+0x60]     l'indice du decor
#     0x1800859AC  mov   eax, 0x13            <- cinq octets
#     0x1800859B1  vmovd xmm1, eax ; vpcmpeqd ; vblendvps (0,001 ou 0,4)
#
# Le `mov` devient un `call` vers un stub qui rend l'INDICE LUI-MEME quand il
# est dans notre liste (la comparaison reussit : 0,4), et 0x13 sinon -- bar
# garde son 0,4, tout autre decor son 0,001. rbx porte la tache.
WET_CLOTH_SITE = 0x1800859AC

# YUKA (le sol de ban qui se casse) : pas de dossier du tout, CINQ LITTERAUX
# qui cablent le moteur sur `ban` -- et le setStage (0x180086660) ignore
# l'indice qu'on lui donne :
#
#   0x1800861CB  mov ecx, 0x18            l'objset (ses textures), init
#   0x1800861EB  lea rax, [rip+table]     0x180356620 : 0x90 dalles x 3
#   0x1800863BB  lea rax, [rip+table]       couches d'objets, init
#   0x180086675  mov edx, 0x496           l'uid du debris, dans le setStage
#   0x180085D1D  mov ecx, 0x180000        l'objet dessine (STGBAN_DUMMY)
#
# (`mov [rcx+0x58], 0x496` et `cmp [rdi+0x58], 0x496` restent : c'est un
# MARQUEUR « l'animation est chargee », pas l'animation elle-meme.)
#
# Le creneau 7 de TaskEffectYuka passe par un stub qui choisit, selon
# l'indice, NOTRE configuration ou celle de FS (relue dans `.origine`), et
# l'ecrit dans une variable de la greffe {objset, uid, objet, -, table} ; les
# cinq sites la relisent : trois `mov imm32` deviennent des `call` vers un
# `mov reg, [rip+var] ; ret`, les deux `lea` des `mov rax, [rip+var]` (meme
# longueur). Un decor de FS relit exactement ses valeurs d'origine.
YUKA_VTABLE = 0x18034EE98                # creneau 7 de 0x18034EE60
YUKA_SETSTAGE = 0x180086660
YUKA_SITE_JEU = 0x1800861CB              # b9 imm32
YUKA_SITES_TABLE = (0x1800861EB, 0x1800863BB)   # 48 8d 05 d32
YUKA_TABLE_FS = 0x180356620
YUKA_SITE_UID = 0x180086675              # ba imm32
YUKA_SITE_OBJET = 0x180085D1D            # b9 imm32

GENERATION_TACHES = (('FOG_RING', 18), ('SNOW_RING', 15), ('RAIN', 8),
                     ('WET_CLOTH', 17), ('YUKA', 6))

# ---------------------------------------------------------------------------
# LES COMPORTEMENTS CABLES SUR UN NUMERO DE DECOR OU D'UID (2026-09-11)
#
# Frederic : « decor de Jean / de Wolf : barriere du ring invisible (decor qui
# alterne no wall et wall entre les rounds) », « decor de Taka-Arashi : les
# flashs des appareils photo ne doivent se lancer qu'en fin de round (trouver
# le trigger) ». Le declencheur n'est pas une donnee : c'est un TEST EN DUR.
#
#   grillage     0x18008474A, 0x180084D7F  `decor == 16 || decor == 39`
#                (yuk, gym : le grillage qui monte et descend)
#   reflet       0x180083835  `decor == 39`, puis `mov ecx, 0xB1F009D`
#                (0x180083895, STGGYM_EFF_SAKU_REFLECT, objset de FS)
#   reflet_sin   0x18010B6CB  `decor == 10` : plan de coupe -0,8 de S_REFL
#   bar          0x180105636  `decor == 0x13` : second jeu de parametres
#   a3d_riv      TaskEffectAuth3D::setStage 0x1800706B0 : `== 8` -> +0xB1
#   a3d_flash    idem, `== 0x28` -> +0xB0 (les flashs de fin de round)
#   uid          l'init 0x180070340 et la mise a jour 0x18006FC30 testent
#                l'uid de chaque animation (0x4E8/0x4E9 IDOU/KAWA, 0x7F4
#                FLASH) -- nos uid sont renumerotes, ils ne passent jamais
#
# On ne rend un comportement a une entree que si SA generation l'a (voir
# `generation.CABLAGES`, verifie instruction par instruction) :
#
#   * aux appels de l'accesseur (`call 0x18018F580`), un stub rend l'indice
#     du decor FS du meme lieu pour NOS entrees eligibles, l'indice reel sinon
#     -- et seulement a CES sites : le chargement, la musique, les tables
#     continuent de voir le vrai indice ;
#   * le setStage d'Auth3D passe par un stub qui pose le drapeau apres
#     l'original ;
#   * l'accesseur d'uid (`0x180041440`) est enveloppe aux quatre appels
#     d'Auth3D : notre uid de STGRV5_EFF_IDOU y devient 0x4E8, etc.
#
# Ce que FS teste et qu'AUCUNE generation ne teste n'est PAS rendu (plan d'eau
# riv/jin 0x18018FBC0, particules de yuk et hai, jin du ring-out 0x1800795FB,
# drapeau gym 0x1801F4272, public/neons/voitures d'Auth3D) : ce sont des
# ajouts de FS.
GETTER_DECOR = 0x18018F580
GESTIONNAIRE_DECOR = 0x1807499D8          # le pointeur du singleton (+0x5C)
CABLAGES_APPELS = {
    'grillage': (0x18008474A, 0x180084D7F),
    'reflet_grillage': (0x180083835,),
    'reflet_sin': (0x18010B6CB,),
    'bar': (0x180105636,),
}
CABLAGE_REFLET_SITE = 0x180083895         # mov ecx, 0xB1F009D
CABLAGE_REFLET_DEFAUT = 0xB1F009D
CABLAGES_DRAPEAUX = {'a3d_riv': 0xB1, 'a3d_flash': 0xB0}
A3D_VTABLE7 = 0x18034EB28                 # creneau 7 de 0x18034EAF0
A3D_SETSTAGE = 0x1800706B0
UID_ACCESSEUR = 0x180041440
A3D_UID_SITES = (0x1800703B9, 0x18006FC93, 0x18006FED5, 0x18006FF6B)


def _balayage(c, va, reg_idx, table):
    """Ajoute `lea rcx,[rip+table]` + balayage {cle, valeur} fin -1 sur
    `reg_idx` (eax) ; saute a F (valeur dans eax) ou D. Rend les positions
    des deux sauts a corriger."""
    c += b'\x48\x8d\x0d' + struct.pack('<i', table - (va + len(c) + 7))
    etiq = len(c)
    c += b'\x83\x39\xff' + b'\x74\x00'           # cmp dword [rcx],-1 ; je D
    j_d = len(c) - 1
    c += b'\x3b\x01' + b'\x74\x00'               # cmp eax,[rcx] ; je F
    j_f = len(c) - 1
    c += b'\x48\x83\xc1\x08'                     # add rcx, 8
    c += b'\xeb' + struct.pack('<b', etiq - (len(c) + 2))
    return j_d, j_f


def stub_alias(va, table):
    """L'indice du decor (lu comme 0x18018F580), traduit par `table`."""
    c = bytearray(b'\x48\x8b\x05' + struct.pack(
        '<i', GESTIONNAIRE_DECOR - (va + 7)))    # mov rax,[rip+singleton]
    c += b'\x8b\x40\x5c'                          # mov eax,[rax+0x5c]
    c += b'\x51'                                  # push rcx
    j_d, j_f = _balayage(c, va, 'eax', table)
    c[j_f] = len(c) - (j_f + 1)
    c += b'\x8b\x41\x04'                          # F: mov eax,[rcx+4]
    c[j_d] = len(c) - (j_d + 1)
    c += b'\x59\xc3'                              # D: pop rcx ; ret
    return bytes(c)


def stub_objet_reflet(va, table):
    """`ecx` = l'objet du reflet pour le decor REEL, sinon celui de FS."""
    c = bytearray(b'\x48\x8b\x05' + struct.pack(
        '<i', GESTIONNAIRE_DECOR - (va + 7)))
    c += b'\x8b\x40\x5c'
    j_d, j_f = _balayage(c, va, 'eax', table)
    c[j_f] = len(c) - (j_f + 1)
    c += b'\x8b\x49\x04\xc3'                      # F: mov ecx,[rcx+4] ; ret
    c[j_d] = len(c) - (j_d + 1)
    c += b'\xb9' + struct.pack('<I', CABLAGE_REFLET_DEFAUT) + b'\xc3'
    return bytes(c)


def stub_a3d_setstage(va, table):
    """Appelle le setStage d'Auth3D, puis pose [tache+decal] = 1 pour chaque
    {indice, decal} de `table` qui vise l'indice recu."""
    c = bytearray(b'\x53\x56\x48\x83\xec\x28')   # push rbx/rsi ; sub rsp,28
    c += b'\x48\x89\xcb\x89\xd6'                  # mov rbx,rcx ; mov esi,edx
    c += b'\xe8' + struct.pack('<i', A3D_SETSTAGE - (va + len(c) + 5))
    c += b'\x48\x8d\x0d' + struct.pack('<i', table - (va + len(c) + 7))
    etiq = len(c)
    c += b'\x83\x39\xff' + b'\x74\x00'           # cmp [rcx],-1 ; je D
    j_d = len(c) - 1
    c += b'\x3b\x31' + b'\x75\x07'               # cmp esi,[rcx] ; jne N
    c += b'\x8b\x41\x04'                          # mov eax,[rcx+4]
    c += b'\xc6\x04\x03\x01'                      # mov byte [rbx+rax],1
    c += b'\x48\x83\xc1\x08'                      # N: add rcx,8
    c += b'\xeb' + struct.pack('<b', etiq - (len(c) + 2))
    c[j_d] = len(c) - (j_d + 1)
    c += b'\x48\x83\xc4\x28\x5e\x5b\xc3'          # D: add rsp ; pop ; ret
    return bytes(c)


def stub_uid(va, table):
    """L'uid d'une animation (0x180041440), traduit par `table`."""
    c = bytearray(b'\x48\x83\xec\x28')            # sub rsp, 0x28 (ombre)
    c += b'\xe8' + struct.pack('<i', UID_ACCESSEUR - (va + len(c) + 5))
    c += b'\x48\x83\xc4\x28'                      # add rsp, 0x28
    c += b'\x51'                                  # push rcx
    j_d, j_f = _balayage(c, va, 'eax', table)
    c[j_f] = len(c) - (j_f + 1)
    c += b'\x8b\x41\x04'                          # F: mov eax,[rcx+4]
    c[j_d] = len(c) - (j_d + 1)
    c += b'\x59\xc3'                              # D: pop rcx ; ret
    return bytes(c)


def stubs_yuka(va, va_var, va_table, n_nous, pas, defaut):
    """Le setStage de Yuka et ses trois lecteurs. `defaut` = (objset, uid,
    objet) de FS. Rend (octets, {nom: adresse du lecteur})."""
    c = bytearray()
    c += b'\x48\x8d\x05' + struct.pack('<i', va_table - (va + 7))
    c += b'\x41\xb9' + struct.pack('<I', n_nous)
    etiq = len(c)
    c += b'\x45\x85\xc9' + b'\x74\x00'                  # test r9d ; je DEFAUT
    j_def = len(c) - 1
    c += b'\x3b\x10' + b'\x74\x00'                      # cmp edx,[rax] ; je
    j_tr = len(c) - 1
    c += b'\x48\x05' + struct.pack('<I', pas)           # add rax, pas
    c += b'\x41\xff\xc9'                                # dec r9d
    c += b'\xeb' + struct.pack('<b', etiq - (len(c) + 2))
    c[j_tr] = len(c) - (j_tr + 1)
    # TROUVE : {objset, uid} en 8 octets, l'objet, et l'adresse de la table
    c += b'\x4c\x8d\x05' + struct.pack('<i', va_var - (va + len(c) + 7))
    c += b'\x4c\x8b\x48\x04' + b'\x4d\x89\x08'          # mov r9,[rax+4] ; [r8]
    c += b'\x44\x8b\x48\x0c' + b'\x45\x89\x48\x08'      # objet -> [r8+8]
    c += b'\x4c\x8d\x48\x10' + b'\x4d\x89\x48\x10'      # lea r9,[rax+0x10]
    c += b'\xeb\x00'
    j_suite = len(c) - 1
    c[j_def] = len(c) - (j_def + 1)
    # DEFAUT : les valeurs de FS
    c += b'\x4c\x8d\x05' + struct.pack('<i', va_var - (va + len(c) + 7))
    c += b'\x41\xc7\x00' + struct.pack('<I', defaut[0])
    c += b'\x41\xc7\x40\x04' + struct.pack('<I', defaut[1])
    c += b'\x41\xc7\x40\x08' + struct.pack('<I', defaut[2])
    c += b'\x4c\x8d\x0d' + struct.pack('<i', YUKA_TABLE_FS - (va + len(c) + 7))
    c += b'\x4d\x89\x48\x10'
    c[j_suite] = len(c) - (j_suite + 1)
    c += b'\xe9' + struct.pack('<i', YUKA_SETSTAGE - (va + len(c) + 5))
    lecteurs = {}
    for nom, reg, dec in (('jeu', 0x0D, 0), ('uid', 0x15, 4),
                          ('objet', 0x0D, 8)):
        lecteurs[nom] = va + len(c)
        c += b'\x8b' + bytes([reg]) + struct.pack(
            '<i', va_var + dec - (va + len(c) + 6))     # mov e?x, [rip+d]
        c += b'\xc3'
    return bytes(c), lecteurs


def stub_copie(va, va_table, n_nous, pas_entree, src, n, dest, suite):
    """Le stub de recopie (voir GENERATION_STUBS). `suite` : l'adresse de la
    fonction d'origine (saut terminal), ou None pour un `ret`."""
    if pas_entree >= 0x80 or src + n > 0x80:
        raise AssertionError('stub_copie : pas 0x%X / fin 0x%X hors disp8'
                             % (pas_entree, src + n))
    c = bytearray()
    c += b'\x48\x8d\x05' + struct.pack('<i', va_table - (va + 7))
    c += b'\x41\xb9' + struct.pack('<I', n_nous)
    etiq = len(c)
    c += b'\x45\x85\xc9' + b'\x74\x00'                  # test r9d,r9d ; je
    j1 = len(c) - 1
    c += b'\x3b\x10' + b'\x74\x00'                      # cmp edx,[rax] ; je
    j2 = len(c) - 1
    c += b'\x48\x83\xc0' + bytes([pas_entree])          # add rax, pas
    c += b'\x41\xff\xc9'                                # dec r9d
    c += b'\xeb' + struct.pack('<b', etiq - (len(c) + 2))
    copie = len(c)
    c[j1] = copie - (j1 + 1)
    c[j2] = copie - (j2 + 1)
    c += b'\x4c\x8d\x05' + struct.pack('<i', dest - (va + len(c) + 7))
    k = 0
    while k + 8 <= n:
        c += b'\x4c\x8b\x48' + bytes([src + k])         # mov r9, [rax+d8]
        c += b'\x4d\x89\x48' + bytes([k])               # mov [r8+d8], r9
        k += 8
    if k + 4 <= n:
        c += b'\x44\x8b\x48' + bytes([src + k])         # mov r9d, [rax+d8]
        c += b'\x45\x89\x48' + bytes([k])               # mov [r8+d8], r9d
        k += 4
    if k != n:
        raise AssertionError('stub_copie : %d octets, pas un multiple de 4'
                             % n)
    if suite is None:
        c += b'\xc3'
    else:
        c += b'\xe9' + struct.pack('<i', suite - (va + len(c) + 5))
    return bytes(c)


def stub_wet_cloth(va, va_table):
    """`rbx` = la tache ; rend dans eax l'indice s'il est dans la table
    (fin -1), sinon 0x13."""
    c = bytearray(b'\x8b\x43\x60')                      # mov eax,[rbx+0x60]
    c += b'\x4c\x8d\x0d' + struct.pack('<i', va_table - (va + 10))
    c += b'\x41\x83\x39\xff' + b'\x74\x0b'              # cmp [r9],-1 ; je DEF
    c += b'\x41\x3b\x01' + b'\x74\x0b'                  # cmp eax,[r9] ; je OK
    c += b'\x49\x83\xc1\x04'                            # add r9, 4
    c += b'\xeb\xef'                                    # jmp L
    c += b'\xb8\x13\x00\x00\x00'                        # DEF: mov eax, 0x13
    c += b'\xc3'                                        # OK: ret
    assert len(c) == 0x21, len(c)
    return bytes(c)


# ---------------------------------------------------------------------------
# LE SHADER DES EMPREINTES (2026-09-11) -- voir tools/shader_empreintes.py
#
# Les empreintes de SNOW_RING sont des POINTS de 6 pixels ; sous Direct3D 11
# un point fait un pixel, et le portage n'a pas donne de geometry shader a
# `snow_footprint..vp` (il l'a fait pour les cinq autres programmes de
# points). `shader_empreintes.py` pose `w64/shader_vf5_w64.farc`, qui ne
# contient que ce programme, en `GSFX`. Le moteur lit chaque shader PAR SON
# NOM dans l'archive de FS :
#
#   0x180176826  mov r8, rsi                     le nom du membre
#   0x180176829  lea rdx, [rip+0x28A5A0]         -> 0x180400DD0, le chemin
#   0x180176835  call 0x180217C60                ouvre (chemin, membre)
#
# Le `lea` (7 octets) devient `call stub ; nop2` : le stub rend le chemin de
# FS, sauf pour « snow_footprint..vp ». rax, r10, r11 sont libres (l'appel
# qui suit les ecrase) ; la pile n'est pas touchee. Pose seulement quand une
# entree recoit SNOW_RING.
SHADER_EMPREINTES_SITE = 0x180176829
SHADER_ARCHIVE_FS_VA = 0x180400DD0


def stub_shader_empreintes(va, va_nom, va_chemin):
    c = bytearray(b'\x48\x8d\x15' + struct.pack(
        '<i', SHADER_ARCHIVE_FS_VA - (va + 7)))           # lea rdx, [FS]
    c += b'\x4c\x8d\x15' + struct.pack('<i', va_nom - (va + 14))  # lea r10
    c += b'\x4d\x8b\xd8'                                # mov r11, r8
    c += b'\x41\x8a\x03'                                # L: mov al, [r11]
    c += b'\x41\x3a\x02'                                # cmp al, [r10]
    c += b'\x75\x13'                                    # jne FIN
    c += b'\x84\xc0'                                    # test al, al
    c += b'\x74\x08'                                    # je EGAL
    c += b'\x49\xff\xc2' + b'\x49\xff\xc3'              # inc r10 ; inc r11
    c += b'\xeb\xec'                                    # jmp L
    c += b'\x48\x8d\x15' + struct.pack(
        '<i', va_chemin - (va + 44))                    # EGAL: lea rdx, [VF5]
    c += b'\xc3'                                        # FIN: ret
    assert len(c) == 45, len(c)
    return bytes(c)


def eau_anneau_stub(va_stub, va_table):
    """Les octets du stub. `rcx` = la tache, on rend l'objet dans `ecx`."""
    a = va_stub
    c = bytes.fromhex('8b4158')                       # mov eax,[rcx+0x58]
    c += bytes.fromhex('4c8d0d') + struct.pack('<i', va_table - (a + 0x0A))
    c += bytes.fromhex('418339ff')                    # cmp dword [r9],-1
    c += bytes.fromhex('740b')                        # je DEFAUT
    c += bytes.fromhex('413b01')                      # cmp eax,[r9]
    c += bytes.fromhex('740c')                        # je TROUVE
    c += bytes.fromhex('4983c108')                    # add r9,8
    c += bytes.fromhex('ebef')                        # jmp L
    c += b'\xb9' + struct.pack('<I', EAU_ANNEAU_DEFAUT)   # DEFAUT
    c += b'\xc3'
    c += bytes.fromhex('418b4904')                    # TROUVE: mov ecx,[r9+4]
    c += b'\xc3'
    assert len(c) == 0x26, len(c)
    return c


def _disposition():
    """Les zones de la greffe, pour le controle de recouvrement."""
    n, v = VARIANTES_MAX_ANNEAUX, VARIANTES_MAX_VARIANTES
    return [('A', VAR_A, VAR_B - VAR_A), ('B', VAR_B, VAR_TROUVE - VAR_B),
            ('TROUVE', VAR_TROUVE, VAR_APPL - VAR_TROUVE),
            ('APPL', VAR_APPL, VAR_DESS - VAR_APPL),
            ('DESS', VAR_DESS, VAR_SLOT - VAR_DESS),
            ('SLOT', VAR_SLOT, VAR_DONNEES - VAR_SLOT),
            ('RANG', VAR_RANG, 4), ('APPLIQUE', VAR_APPLIQUE, 4),
            ('PLAFOND', VAR_PLAFOND, 4), ('ORDRE', VAR_ORDRE, 4),
            ('X', VAR_X, 4), ('Y', VAR_Y, 4), ('PASSE', VAR_PASSE, 4),
            ('TAILLE', VAR_TAILLE, 4), ('DESC', VAR_DESC, 0x50),
            ('STYLE', VAR_STYLE, 0x40), ('PASSES', VAR_PASSES, 9 * 12),
            ('COMPTES', VAR_COMPTES, n * 4), ('IDX', VAR_IDX, n * v * 4),
            ('TEXTES', VAR_TEXTES, n * v * 32), ('NUM', VAR_NUM, n * 4),
            ('EAU', GRE_EAU, GRE_EAU_TABLE - GRE_EAU),
            ('EAU_TABLE', GRE_EAU_TABLE, EAU_ANNEAU_MAX * 8),
            ('GEN', GRE_GEN, max(0, GREFFE_TAILLE - GRE_GEN))]


def verifier_disposition(taille):
    """AUCUNE zone de la greffe n'en recouvre une autre, et tout tient.

    Ce controle n'existait pas, et son absence a coute la seance du
    2026-09-10 : `VAR_NUM` gardait ses quatre entrees en dur pendant que le
    nombre d'anneaux passait a vingt. Un tableau qui deborde sur le voisin ne
    dit rien -- il ecrit, et le jeu tombe ailleurs, plus tard.
    """
    zones = sorted(_disposition(), key=lambda z: z[1])
    for (n1, d1, t1), (n2, d2, _) in zip(zones, zones[1:]):
        if d1 + t1 > d2:
            raise AssertionError(
                'greffe : %s (0x%X..0x%X) recouvre %s (0x%X)'
                % (n1, d1, d1 + t1, n2, d2))
    n, d0, t = zones[-1]
    if d0 + t > taille:
        raise AssertionError('greffe : %s finit a 0x%X, la section fait 0x%X'
                             % (n, d0 + t, taille))
    return True


def variantes_greffe(va, avec_texte=False, anneaux=None):
    """Assemble la greffe pour l'adresse `va`.

    `anneaux` est une liste de `(indices, noms)`. Un anneau = ce que la barre
    espace fait defiler sur UNE case ; son premier indice est la BASE, celui
    que la case porte naturellement.

    `avec_texte` branche le dessin du nom de variante. Il reste OPTIONNEL : le
    defilement seul (`--variantes`) est acquis et valide a l'ecran, on ne le
    perd pas si le dessin devait encore bouger.

    Historique du drapeau -- il a d'abord PLANTE : Frederic, 2026-09-08, « le
    jeu plante juste avant de pouvoir se positionner sur l'icone du decor de
    Dural » -- c'est-a-dire a la premiere trame ou `[rbx+0x5C]` entre dans
    l'anneau et ou DESSINER s'execute vraiment. La cause etait la montee du
    calque 2D, qui sortait du tableau de compartiments ; elle est retiree et
    remplacee par un rang BORNE dans notre propre descripteur.
    """
    # AVANT TOUT : que rien ne recouvre rien. Voir `verifier_disposition`.
    verifier_disposition(GREFFE_TAILLE)
    anneaux = anneaux or [VARIANTES_ANNEAU_DURAL]
    if len(anneaux) > VARIANTES_MAX_ANNEAUX:
        raise AssertionError('%d anneaux, le maximum est %d'
                             % (len(anneaux), VARIANTES_MAX_ANNEAUX))
    for idx, noms in anneaux:
        if len(idx) != len(noms):
            raise AssertionError('anneau %r : %d indices pour %d noms'
                                 % (idx, len(idx), len(noms)))
        if len(idx) > VARIANTES_MAX_VARIANTES:
            raise AssertionError('anneau %r : %d variantes, maximum %d'
                                 % (idx, len(idx), VARIANTES_MAX_VARIANTES))
    bloc = bytearray(VAR_FIN)

    def rel32(cible, apres):
        return struct.pack('<i', cible - apres)

    def poser(off, octets):
        bloc[off:off + len(octets)] = octets

    def faire(base):
        """Rend (c, ici, rip) pour assembler a `base` dans la greffe."""
        c = bytearray()

        def ici(long_instr):
            return va + base + len(c) + long_instr

        def rip(tete, cible, suffixe=b''):
            return (tete + struct.pack('<i', cible - ici(len(tete) + 4
                                                         + len(suffixe)))
                    + suffixe)
        return c, ici, rip

    # --- TROUVER : un indice de decor -> son RANG dans la table -------------
    # Le rang vaut `anneau * 8 + position`. Il sert de clef unique : il designe
    # a la fois la case de VAR_IDX et la chaine de VAR_TEXTES, et son quotient
    # par 8 designe le compteur de l'anneau. Les cases inutilisees valent -1,
    # donc un simple balayage des 32 cases suffit -- pas de longueurs a tester.
    c, ici, rip = faire(VAR_TROUVE)
    c += bytes.fromhex('31c9')                        # xor ecx, ecx
    boucle = len(c)
    c += rip(bytes.fromhex('488d15'), va + VAR_IDX)   # lea rdx, table
    c += bytes.fromhex('39048a')                      # cmp [rdx+rcx*4], eax
    c += bytes.fromhex('7400')                        # je trouve
    p_ok = len(c) - 1
    c += bytes.fromhex('ffc1')                        # inc ecx
    # `cmp ecx, imm` : au-dela de 127 l'imm8 est SIGNE et la borne
    # deviendrait negative. On passe donc a l'imm32 des que le tableau
    # depasse -- 19 anneaux de VF5 R en font 152.
    _borne = VARIANTES_MAX_ANNEAUX * VARIANTES_MAX_VARIANTES
    if _borne < 0x80:
        c += bytes([0x83, 0xF9, _borne])       # cmp ecx, imm8
    else:
        c += bytes([0x81, 0xF9]) + struct.pack('<I', _borne)
    c += bytes.fromhex('7200')                        # jb boucle
    c[len(c) - 1] = (boucle - len(c)) & 0xFF
    c += bytes.fromhex('b8ffffffff')                  # mov eax, -1
    c += bytes.fromhex('c3')                          # ret
    c[p_ok] = len(c) - (p_ok + 1)
    c += bytes.fromhex('8bc1')                        # mov eax, ecx
    c += bytes.fromhex('c3')                          # ret
    if len(c) > VAR_APPL - VAR_TROUVE:
        raise AssertionError('TROUVER deborde : %d' % len(c))
    poser(VAR_TROUVE, c)

    # --- APPLIQUER : poser sur la case la variante choisie ------------------
    c, ici, rip = faire(VAR_APPL)
    c += bytes.fromhex('8b435c')                      # mov eax, [rbx+0x5c]
    c += bytes([0xE8]) + rel32(va + VAR_TROUVE, ici(5))
    c += bytes.fromhex('85c0')                        # test eax, eax
    c += bytes.fromhex('7800')                        # js fin
    p_fin = len(c) - 1
    c += bytes.fromhex('8bc8')                        # mov ecx, eax
    c += bytes([0xC1, 0xE9, VARIANTES_DECALAGE])      # shr ecx, 3   -> l'anneau
    c += rip(bytes.fromhex('488d15'), va + VAR_NUM)   # lea rdx, numeros
    c += bytes.fromhex('8b148a')                      # mov edx, [rdx+rcx*4]
    c += bytes([0xC1, 0xE1, VARIANTES_DECALAGE])      # shl ecx, 3
    c += bytes.fromhex('03ca')                        # add ecx, edx -> le rang
    c += rip(bytes.fromhex('488d15'), va + VAR_IDX)   # lea rdx, table
    c += bytes.fromhex('8b048a')                      # mov eax, [rdx+rcx*4]
    c += bytes.fromhex('83f8ff')                      # cmp eax, -1
    c += bytes.fromhex('7403')                        # je +3
    c += bytes.fromhex('89435c')                      # mov [rbx+0x5c], eax
    c[p_fin] = len(c) - (p_fin + 1)
    c += bytes.fromhex('c3')                          # ret
    if len(c) > VAR_DESS - VAR_APPL:
        raise AssertionError('APPLIQUER deborde : %d' % len(c))
    poser(VAR_APPL, c)

    # --- ENTREE A : lire la barre espace, faire tourner le numero ----------
    c, ici, rip = faire(VAR_A)
    c += rip(bytes.fromhex('488b0d'), VARIANTES_ENTREES_VA)    # mov rcx, obj
    c += bytes([0xBA]) + struct.pack('<I', VARIANTES_CODE_ESPACE)
    c += bytes.fromhex('488b01')                      # mov rax, [rcx]
    c += bytes.fromhex('ff9060010000')                # call [rax+0x160]
    c += bytes.fromhex('84c0')                        # test al, al
    sauts = []
    c += bytes.fromhex('7400')                        # je appliquer
    sauts.append(len(c) - 1)
    c += bytes.fromhex('837b5802')                    # cmp [rbx+0x58], 2
    c += bytes.fromhex('7500')                        # jne appliquer
    sauts.append(len(c) - 1)
    # De quel anneau la case releve-t-elle ? La question n'a plus de reponse
    # constante depuis qu'il y en a plusieurs : on la POSE.
    c += bytes.fromhex('8b435c')                      # mov eax, [rbx+0x5c]
    c += bytes([0xE8]) + rel32(va + VAR_TROUVE, ici(5))
    c += bytes.fromhex('85c0')                        # test eax, eax
    c += bytes.fromhex('7800')                        # js appliquer
    sauts.append(len(c) - 1)
    c += bytes.fromhex('8bc8')                        # mov ecx, eax
    c += bytes([0xC1, 0xE9, VARIANTES_DECALAGE])      # shr ecx, 3   -> l'anneau
    c += rip(bytes.fromhex('488d15'), va + VAR_NUM)   # lea rdx, numeros
    c += bytes.fromhex('8b048a')                      # mov eax, [rdx+rcx*4]
    c += bytes.fromhex('ffc0')                        # inc eax
    c += rip(bytes.fromhex('4c8d05'), va + VAR_COMPTES)        # lea r8, comptes
    c += bytes.fromhex('413b0488')                    # cmp eax, [r8+rcx*4]
    c += bytes.fromhex('7202')                        # jb +2
    c += bytes.fromhex('33c0')                        # xor eax, eax
    c += bytes.fromhex('89048a')                      # mov [rdx+rcx*4], eax
    for p in sauts:
        c[p] = len(c) - (p + 1)
    c += bytes([0xE8]) + rel32(va + VAR_APPL, ici(5))
    c += VARIANTES_HOOK_TETE                          # les deux deplacees
    c += bytes([0xE9]) + rel32(VARIANTES_RETOUR_VA, ici(5))
    if len(c) > VAR_B - VAR_A:
        raise AssertionError('entree A deborde sur B : %d' % len(c))
    poser(VAR_A, c)

    # --- ENTREE B : le dernier mot, apres la recomputation -----------------
    c, ici, rip = faire(VAR_B)
    # Le dessin ne s'appelle PAS d'ici : l'update est le creneau 2, et dessiner
    # a ce moment ne produit rien. Il part du creneau 4, la phase de rendu.
    c += bytes([0xE8]) + rel32(va + VAR_APPL, ici(5))
    # L'APERCU SE RAFRAICHIT SUR LA BASE, PAS SUR LA VARIANTE. La liste de
    # 0x180174BF0 n'a que 26 entrees (boucle 0x180175010, `cmp rax, 0x1a`) et,
    # quand elle ne trouve pas l'indice, elle EFFACE les trois couches AET
    # (0x18017502D) : l'ecran resterait vide sur un emplacement recycle comme
    # `trm` (26). On l'appelle donc avec la base de l'anneau -- l'image reste
    # celle du decor, exactement comme les cinq Dural partagent `dur_stay` --
    # puis on rend la variante.
    c += bytes.fromhex('8b435c')                      # mov eax, [rbx+0x5c]
    c += rip(bytes.fromhex('8905'), va + VAR_APPLIQUE)
    c += bytes([0xE8]) + rel32(va + VAR_TROUVE, ici(5))
    c += bytes.fromhex('85c0')                        # test eax, eax
    c += bytes.fromhex('7800')                        # js apercu
    p_ap = len(c) - 1
    c += bytes([0x83, 0xE0, 0xFF & ~(VARIANTES_MAX_VARIANTES - 1)])
    c += rip(bytes.fromhex('488d15'), va + VAR_IDX)   # lea rdx, table
    c += bytes.fromhex('8b0482')                      # mov eax, [rdx+rax*4]
    c += bytes.fromhex('89435c')                      # mov [rbx+0x5c], eax
    c[p_ap] = len(c) - (p_ap + 1)
    c += bytes.fromhex('488bcb')                      # mov rcx, rbx
    c += bytes([0xE8]) + rel32(VARIANTES_APERCU_VA, ici(5))
    c += rip(bytes.fromhex('8b05'), va + VAR_APPLIQUE)
    c += bytes.fromhex('89435c')                      # mov [rbx+0x5c], eax
    c += bytes([0xE9]) + rel32(VARIANTES_RETOUR_B_VA, ici(5))
    if len(c) > VAR_TROUVE - VAR_B:
        raise AssertionError('entree B deborde sur TROUVER : %d' % len(c))
    poser(VAR_B, c)

    # --- DESSINER : le nom de la variante, a l'ecran -----------------------
    c, ici, rip = faire(VAR_DESS)

    c += bytes.fromhex('4883ec38')                    # sub rsp, 0x38
    # `AetMgr` est GLOBAL : sans cette garde, le nom s'afficherait sur tous
    # les ecrans ou l'objet de selection existe encore. 2 = navigation.
    c += bytes.fromhex('837b5802')                    # cmp [rbx+0x58], 2
    c += bytes.fromhex('0f8500000000')                # jne fin (near)
    p_jne = len(c) - 4
    # La case porte-t-elle une variante ? Le rang rendu par TROUVER designe
    # DIRECTEMENT la chaine : APPLIQUER a deja pose la variante choisie dans
    # `[rbx+0x5C]`, donc la position trouvee EST le numero courant.
    c += bytes.fromhex('8b435c')                      # mov eax, [rbx+0x5c]
    c += bytes([0xE8]) + rel32(va + VAR_TROUVE, ici(5))
    c += bytes.fromhex('85c0')                        # test eax, eax
    c += bytes.fromhex('0f8800000000')                # js fin (near)
    p_jae = len(c) - 4
    c += rip(bytes.fromhex('8905'), va + VAR_RANG)    # mov [rip+rang], eax
    # les deux constructions
    c += rip(bytes.fromhex('488d0d'), va + VAR_DESC)  # lea rcx, desc
    c += bytes([0xE8]) + rel32(VARIANTES_DESC_NEUF, ici(5))
    c += rip(bytes.fromhex('488d0d'), va + VAR_STYLE)
    c += bytes([0xE8]) + rel32(VARIANTES_STYLE_NEUF, ici(5))
    # mode 2, puis la taille
    c += rip(bytes.fromhex('488d0d'), va + VAR_STYLE)
    c += bytes.fromhex('ba02000000')                  # mov edx, 2
    c += bytes([0xE8]) + rel32(VARIANTES_STYLE_MODE, ici(5))
    c += rip(bytes.fromhex('c5fa100d'), va + VAR_TAILLE)       # vmovss xmm1
    c += rip(bytes.fromhex('488d0d'), va + VAR_STYLE)
    c += bytes([0xE8]) + rel32(VARIANTES_STYLE_TAILLE, ici(5))
    # LE RANG DE DESSIN. `cmd+0x14` reste a -1 -- la chaine de dessin ne le pose
    # jamais (verifie : 0x180189880 le met a -1, et 0x18019B18B..0x18019B203 ne
    # le reecrit pas) -- donc 0x18018CA3B retombe sur `[contexte+0x828]`, le
    # calque que l'AET a deja monte, et notre texte tombait dessous.
    #
    # On ne monte PAS ce calque : il est global, et le tableau ne contient que
    # 4 x 32 compartiments (voir le pave en tete). On corrige NOTRE descripteur
    # pour viser le dernier compartiment, le 127, sans jamais en sortir :
    #
    #     desc+0x28 = plafond - calque      -> calque effectif = 3
    #     desc+0x24 = ordre                 -> rang 31
    #
    c += rip(bytes.fromhex('488b05'), VARIANTES_CTX_VA)        # mov rax, ctx
    c += bytes.fromhex('4885c0')                      # test rax, rax
    c += bytes.fromhex('0f8400000000')                # jz fin (near)
    p_ctx = len(c) - 4
    c += bytes.fromhex('8b88') + struct.pack('<I', VARIANTES_CALQUE_OFF)
    c += rip(bytes.fromhex('8b05'), va + VAR_PLAFOND)          # mov eax, plafond
    c += bytes.fromhex('3bc8')                        # cmp ecx, eax
    # Si le calque courant depasse deja le plafond, aucun rang ne tient dans le
    # tableau : on renonce au texte plutot que de lire hors du contexte.
    c += bytes.fromhex('0f8f00000000')                # jg fin (near)
    p_haut = len(c) - 4
    c += bytes.fromhex('2bc1')                        # sub eax, ecx
    c += rip(bytes.fromhex('8905'), va + VAR_DESC + 0x28)      # -> desc+0x28
    c += rip(bytes.fromhex('8b05'), va + VAR_ORDRE)   # mov eax, ordre
    c += rip(bytes.fromhex('8905'), va + VAR_DESC + 0x24)      # -> desc+0x24

    # le style entre au descripteur -- une seule fois, il ne bouge plus
    c += rip(bytes.fromhex('488d05'), va + VAR_STYLE)          # lea rax
    c += rip(bytes.fromhex('488905'), va + VAR_DESC + 0x48)    # mov [rip],rax

    # LA BOUCLE DES NEUF PASSES. Huit noires decalees tout autour, puis la
    # blanche au centre : c'est le lisere, fait a la main. Chaque passe relit
    # son (dx, dy, couleur) dans la table, donc rien n'est en dur ici.
    c += rip(bytes.fromhex('c705'), va + VAR_PASSE,
             struct.pack('<I', 0))                    # mov [rip+passe], 0
    boucle = len(c)
    c += rip(bytes.fromhex('8b05'), va + VAR_PASSE)   # mov eax, [rip+passe]
    c += bytes.fromhex('486bc00c')                    # imul rax, rax, 12
    c += rip(bytes.fromhex('488d0d'), va + VAR_PASSES)         # lea rcx, table
    c += bytes.fromhex('4801c1')                      # add rcx, rax
    c += bytes.fromhex('8b4108')                      # mov eax, [rcx+8]
    c += rip(bytes.fromhex('8905'), va + VAR_DESC + 0x08)      # la couleur
    c += rip(bytes.fromhex('c5fa1005'), va + VAR_X)            # vmovss xmm0, x
    c += bytes.fromhex('c5fa5801')                    # vaddss xmm0, xmm0, [rcx]
    c += rip(bytes.fromhex('c5fa1105'), va + VAR_DESC + 0x34)
    c += rip(bytes.fromhex('c5fa1105'), va + VAR_DESC + 0x3C)
    c += rip(bytes.fromhex('c5fa1005'), va + VAR_Y)            # vmovss xmm0, y
    c += bytes.fromhex('c5fa584104')                  # vaddss xmm0,xmm0,[rcx+4]
    c += rip(bytes.fromhex('c5fa1105'), va + VAR_DESC + 0x38)
    c += rip(bytes.fromhex('c5fa1105'), va + VAR_DESC + 0x40)
    # LA CHAINE. Surtout PAS un tableau de pointeurs absolus : la DLL est
    # REBASEE a l'execution (0x7FFDB0620000 lors de la mesure du 2026-09-08) et
    # notre section n'a aucune relocation. Un pointeur ecrit a la base preferee
    # 0x180000000 ne designe alors rien -- c'est exactement ce qui faisait
    # planter le dessin, le moteur lisant `r8 = 0x180EA1900` en terre inconnue.
    # On calcule donc l'adresse a l'EXECUTION, en RIP-relatif, sur des chaines
    # a PAS FIXE.
    c += rip(bytes.fromhex('8b05'), va + VAR_RANG)             # mov eax, rang
    c += rip(bytes.fromhex('488d0d'), va + VAR_TEXTES)         # lea rcx, textes
    c += bytes.fromhex('48c1e005')                    # shl rax, 5   (pas de 32)
    c += bytes.fromhex('4c8d0401')                    # lea r8, [rcx+rax]
    c += bytes.fromhex('ba28000000')                  # mov edx, 0x28
    c += rip(bytes.fromhex('488d0d'), va + VAR_DESC)  # lea rcx, desc
    c += bytes([0xE8]) + rel32(VARIANTES_DESSIN, ici(5))
    c += rip(bytes.fromhex('8b05'), va + VAR_PASSE)   # mov eax, [rip+passe]
    c += bytes.fromhex('ffc0')                        # inc eax
    c += rip(bytes.fromhex('8905'), va + VAR_PASSE)   # mov [rip+passe], eax
    c += bytes([0x83, 0xF8, len(VARIANTES_PASSES) + 1])        # cmp eax, 9
    c += bytes.fromhex('0f82') + struct.pack('<i', boucle - (len(c) + 6))
    # RIEN A RENDRE. La version precedente montait `[contexte+0x828]` ici puis
    # le restaurait ; elle plantait. On ne touche plus a aucun etat global : le
    # rang est dans NOTRE descripteur, et il meurt avec lui.
    struct.pack_into('<i', c, p_jae, len(c) - (p_jae + 4))     # jae  -> fin
    struct.pack_into('<i', c, p_jne, len(c) - (p_jne + 4))     # jne  -> fin
    struct.pack_into('<i', c, p_ctx, len(c) - (p_ctx + 4))     # jz   -> fin
    struct.pack_into('<i', c, p_haut, len(c) - (p_haut + 4))   # jg   -> fin
    c += bytes.fromhex('4883c438')                    # add rsp, 0x38
    c += bytes.fromhex('c3')                          # ret
    if len(c) > VAR_SLOT - VAR_DESS:
        raise AssertionError('DESSINER deborde : %d' % len(c))
    poser(VAR_DESS, c)

    # --- LE CRENEAU 4 : ce que le moteur appelle a la phase de RENDU -------
    # Signature du creneau : `(this)` dans rcx, rend un entier. Le bouchon
    # d'origine (0x180007430) rend 0 ; on fait pareil.
    c = bytearray()

    def ici_s(long_instr):
        return va + VAR_SLOT + len(c) + long_instr

    # L'ORDRE EST L'INVERSE DU PREMIER JET, ET C'EST TOUT LE CORRECTIF.
    #
    # Version precedente : original PUIS dessin -> texte INVISIBLE. Ce qui
    # s'explique : le creneau 2 CONSOMME la liste, et on y ajoutait apres.
    # Le creneau 6 empile les sprites de l'AET dans un vecteur d'elements de
    # 0x18 octets (`movabs r15, 0xaaaaaaaaaaaaaa9`, la division par 24), et
    # notre texte insere des elements de 0x18 octets par `0x1801067C0` : c'est
    # la MEME liste. L'ordre y est celui de l'insertion.
    #
    # On dessine donc A L'ENTREE du creneau 2 -- apres que le 6 a tout empile,
    # avant que le 2 ne vide. Notre texte est alors le DERNIER insere, donc
    # dessine par-dessus l'AET. Et rien n'est retire de l'ecran.
    # Le creneau 4 de TaskSelStage : un bouchon `ret 0`, donc `this` est la
    # tache elle-meme, et il n'y a pas d'original a rappeler. C'est ici que le
    # texte etait DEJA visible ; ce qui manquait n'etait pas le moment, mais le
    # CALQUE, que `DESSINER` monte maintenant.
    c += bytes.fromhex('53')                          # push rbx
    c += bytes.fromhex('488bd9')                      # mov rbx, rcx (la tache)
    c += bytes.fromhex('4883ec20')                    # sub rsp, 0x20
    c += bytes([0xE8]) + rel32(va + VAR_DESS, ici_s(5))
    c += bytes.fromhex('4883c420')                    # add rsp, 0x20
    c += bytes.fromhex('5b')                          # pop rbx
    c += bytes.fromhex('33c0')                        # xor eax, eax
    c += bytes.fromhex('c3')                          # ret
    if len(c) > VAR_DONNEES - VAR_SLOT:
        raise AssertionError('le creneau deborde : %d' % len(c))
    poser(VAR_SLOT, c)

    # --- les donnees -------------------------------------------------------
    struct.pack_into('<f', bloc, VAR_X, VARIANTES_XY[0])
    struct.pack_into('<f', bloc, VAR_Y, VARIANTES_XY[1])
    struct.pack_into('<f', bloc, VAR_TAILLE, VARIANTES_TAILLE)
    struct.pack_into('<I', bloc, VAR_PLAFOND, VARIANTES_PLAFOND)
    struct.pack_into('<I', bloc, VAR_ORDRE, VARIANTES_ORDRE)
    # LES ANNEAUX. Les cases inutilisees valent -1 : TROUVER balaye les 32
    # cases et compare, sans avoir a tester la moindre longueur -- et -1 n'est
    # l'indice d'aucun decor.
    for k in range(VARIANTES_MAX_ANNEAUX * VARIANTES_MAX_VARIANTES):
        struct.pack_into('<i', bloc, VAR_IDX + k * 4, -1)
    for r, (indices, noms) in enumerate(anneaux):
        struct.pack_into('<I', bloc, VAR_COMPTES + r * 4, len(indices))
        for k, (idx, nom) in enumerate(zip(indices, noms)):
            rang = r * VARIANTES_MAX_VARIANTES + k
            struct.pack_into('<I', bloc, VAR_IDX + rang * 4, idx)
            brut = nom.encode('ascii') + b'\x00'
            if len(brut) > VARIANTES_PAS:
                raise AssertionError('%r depasse le pas de %d octets'
                                     % (nom, VARIANTES_PAS))
            o = VAR_TEXTES + rang * VARIANTES_PAS
            bloc[o:o + len(brut)] = brut
    # les neuf passes : huit noires autour, la blanche au centre EN DERNIER
    passes = [(dx * VARIANTES_LISERE, dy * VARIANTES_LISERE, VARIANTES_NOIR)
              for dx, dy in VARIANTES_PASSES]
    passes.append((0.0, 0.0, VARIANTES_BLANC))
    for k, (dx, dy, coul) in enumerate(passes):
        struct.pack_into('<ffI', bloc, VAR_PASSES + k * 12, dx, dy, coul)
    return bytes(bloc)



# ---------------------------------------------------------------------------
# DEPLACER LES DEUX TABLES INDEXEES PAR LE DECOR  (`--decors-table [N]`)
#
# LE BUT, et il n'est PAS d'ajouter un decor tout de suite. Frederic, le
# 2026-09-09 : « recycler un emplacement d'essai n'est pas un ajout, et ils ne
# sont pas assez nombreux ». Passer a plus de 41 decors demande de deplacer les
# deux tables ; ce correctif fait le deplacement SEUL, a N inchange, pour qu'on
# puisse verifier que le jeu tourne toujours a 41 decors AVANT d'en ajouter un.
#
# Ce qui rend le deplacement possible, c'est `pe_sections.py` : une section
# greffee peut desormais porter ses RELOCATIONS. Sans elles, deplacer une table
# de 515 pointeurs n'aurait servi a rien -- ils seraient tous restes a la base
# preferee.
#
# LES DEUX TABLES, mesurees le 2026-09-09
#
#   0x180403430   41 descripteurs de 0xF0 octets       0x2670 o
#                 515 pointeurs relogés, a dix-sept decalages :
#                 +0x00 +0x08 +0x48 +0x50 +0x58 +0x60 +0x68 +0x70..+0xB0 +0xC0
#                 17 decors en ont 7 (les emplacements d'essai), 12 en ont 16,
#                 12 en ont 17.
#   0x18039F7A0   41 pointeurs vers les codes a trois lettres   0x148 o
#                 41 sur 41 relogés ; la table finit la (le qword suivant n'est
#                 pas une relocation).
#
# ON NE DEVINE PAS OU SONT LES POINTEURS : on recopie une relocation partout ou
# la SOURCE en a une. C'est exact, et ca ne suppose rien sur la forme du
# descripteur -- la faute qui a coute deux seances etait justement de croire
# qu'un descripteur « disait trois champs ».
#
# LES HUIT SITES QUI CHARGENT LES TABLES, enumeres par `tools/refs_plage.py`
# (un balayage de PLAGE, pas d'adresse : le moteur entre aussi par +0x70).
# Le champ a reecrire est le disp32, dont la position ne depend pas du prefixe
# REX que capstone rate parfois en partant mal aligne.
DECORS_BASE = 0x180000000
DECORS_TABLE_VA = 0x180403430
DECORS_TABLE_PAS = 0xF0
DECORS_TABLE_N = 41
DECORS_CODES_VA = 0x18039F7A0
DECORS_CODES_PAS = 8
# (champ disp32, decalage vise dans la table)
DECORS_TABLE_SITES = (
    (0x18018EF7B, 0x00),    # 0x18018EF40, le gestionnaire : mov [rcx+0x68], r8
    (0x18018F3DF, 0x00),    # la musique
    (0x18018F409, 0x70),    # la musique, base des neuf reprises
    (0x18018F56B, 0x00),    # le nom
    (0x18018F59B, 0x00),    # 0x18018F590, nom -> index
    (0x18018F642, 0x00),    # la propriete +0xD4
)
DECORS_CODES_SITES = (
    (0x1800D6148, 0x00),
    (0x1800D713B, 0x00),    # 0x1800D7130, qui compose ibl/ et light_param/
)

# ---------------------------------------------------------------------------
# LA QUATRIEME TABLE INDEXEE PAR L'ETAGE : les objsets EN PLUS (2026-09-10)
#
# C'est elle qui bloquait le decor ajoute sur un ecran de chargement infini,
# et elle n'a ete trouvee qu'en DECOMPILANT (Ghidra) le passage de l'etat 3 a
# l'etat 4 :
#
#     void FUN_18006F620(int indice)            // 0x18006F620
#     {
#         for (p = &DAT_18034D510; *p != -1; p++)  charger_objset(*p, 1);
#         FUN_18003C200("EFFEFFCMN");
#         liste = &DAT_18034D570 + indice * 0x60;      // <<<< ICI
#         for (p = liste; *p != -1; p++)  charger_objset(*p, 1);
#         DAT_180642FE0 = indice;  DAT_180642FE8 = liste;
#     }
#
# et l'etat 4 attend que TOUTE cette liste soit chargee :
#
#     else if (etat == 4 && FUN_18006FA60() == 0) { ... etat = 5; }
#
# La table a 41 entrees de 0x60 octets. A l'indice 42 la lecture sort de la
# table et tombe sur ce qui suit dans `.rdata` : des MOITIES DE POINTEURS,
# prises pour des identifiants d'objset. Le moteur les demande, elles
# n'existent pas, et il les attend pour toujours. Aucun message.
#
# UNE ENTREE N'EST PAS UNE LISTE, C'EST DEUX (corrige le 2026-09-10, apres deux
# essais a l'ecran). Ce commentaire disait « les 41 entrees reelles sont TOUTES
# VIDES ». C'etait vrai des QUATRE PREMIERS OCTETS, et faux de l'entree :
#
#     +0x00  8 identifiants d'objset a charger EN PLUS, fin -1   (tous vides)
#     +0x20  16 indices de TACHES D'EFFET a creer, fin -1        (PAS vides)
#
# Le +0x20 est lu par `0x18006F380`, le createur des taches d'effet :
#
#     for (p = &DAT_18034D530; *p != -1; p++)   creer_tache(*p);   // toujours
#     for (i = 0; ...; i++)                                        // par decor
#         creer_tache(*(int *)(liste + 0x20 + i*4));
#
# avec `liste = &DAT_18034D570 + indice * 0x60`, pose par `FUN_18006F620`. Les
# noms sont en clair dans `0x18034E4D0` : 0=EFFECT_HIT, 1=EFFECT_AUTH3D,
# **2=EFFECT_WALL**, 3=LEAF, 5=SNOW, 7=RIPPLE, 9=THUNDER, 12=RINGOUT_SPLASH,
# 14=SPLASH, 16=FOG_ANIM, 17=WET_CLOTH, 19=BREATH, 22=ELE_BOARD…
#
# TOUJOURS creees (0x18034D530) : 0 HIT, 1 AUTH3D, 10 DOWN, 11 MOVE,
# 20 PARTICLE, 21 POISON. **EFFECT_WALL n'en est pas.** `djo` (11) demande
# `[2]`, et 32 des 41 decors demandent 2 = WALL.
#
# D'ou le defaut : une entree neuve clonee sur l'entree 0 ne demande AUCUNE
# tache. Le decor ajoute avait donc ses flammes (AUTH3D est toujours creee) et
# pas ses barrieres (WALL n'existait pas), avec une table de murs pourtant
# juste et une collision correcte -- elle, vient du descripteur +0xB8/+0xC0.
# Une entree neuve est maintenant un CLONE COMPLET de celle du modele.
#
# Le reste tient toujours :
#   . la table ne contient que des ENTIERS, aucun pointeur : son deplacement
#     ne demande aucune relocation -- contrairement aux trois autres. Le
#     correctif le verifie quand meme avant de copier ;
#   . `refs_plage.py` ne lui trouve qu'UN SEUL site.
OBJSETS_TABLE_VA = 0x18034D570
OBJSETS_TABLE_PAS = 0x60
OBJSETS_TABLE_N = 41
OBJSETS_TABLE_SITES = ((0x18006F675, 0x00),)   # lea dans 0x18006F620
OBJSETS_TABLE_TACHES = 0x20                    # +0x20 : les taches d'effet

# LES TACHES QU'ON SAIT SERVIR, ET POURQUOI LES AUTRES SONT RETIREES
#
# Mesure du 2026-09-10, apres trois essais a l'ecran. **Chaque tache d'effet a
# sa propre table indexee par le decor**, et la creer sans lui donner son
# entree la laisse SANS DONNEES -- puis sa mise a jour tourne quand meme.
#
#     TaskEffectBreath::setStage  = TROIS comparaisons explicites :
#         0x1806430C0 -> 16 (yuk)   0x1806430D4 -> 18 (aur)   0x1806430E8 -> 21 (du1)
#         aucune ne correspond -> `return`, et la tache reste vierge.
#
#     FOG_ANIM 0x180643130 -> 14 (are)      SNOW 0x180643340 -> 16 (yuk)
#     THUNDER  0x180351BB8                  SPLASH 0x180351B18
#
# `aur` demande WALL **et BREATH** ; notre indice 56 n'est dans aucune de ces
# tables. C'est ce qui faisait planter aurora apres que le mur, les objets et
# les bases ont ete corriges.
#
# DEUX FACONS D'EN SORTIR : deplacer chacune de ces tables pour y ajouter une
# entree (ce qu'on a fait pour WALL et AUTH3D), ou **ne pas demander la tache**.
# La seconde est immediate et ne peut pas planter : le decor perd l'effet, il
# ne perd rien d'autre. On garde donc :
#
#   . AUTH3D (1) et les cinq autres toujours creees (HIT, DOWN, MOVE,
#     PARTICLE, POISON) -- elles ne passent pas par cette liste ;
#   . WALL (2), dont on POSE l'entree.
#
# Les autres sont retirees de la liste du decor ajoute, et le patcheur le DIT.
# Chacune se rouvrira le jour ou on deplacera sa table.
#
# 2026-09-10, deuxieme passe : SIX taches sont desormais servies. SNOW, DOWN et
# MOVE parce que leur table a demenage ; BREATH, FOG_ANIM, SPLASH et THUNDER
# parce que leur chaine de comparaisons deroulee est devenue un balayage (voir
# CHAINES). DOWN et MOVE ne passent pas par cette liste -- elles sont toujours
# creees --, d'ou cinq numeros seulement ici.
#
# Ce qui reste ferme, et pourquoi : LEAF (3), RIPPLE (7), WATER_RING (13) et
# SNOW_RING (15) partagent `setStage 0x180076B00` ; RINGOUT_SPLASH (12),
# WET_CLOTH (17) et ELE_BOARD (22) n'ont pas de `lea rip` en tete. Leur forme
# n'est pas mesuree : on ne les demande donc pas, et le patcheur le DIT.
#
# 2026-09-11, troisieme passe (« applique les effets VF5 a VF5 ») : LEAF (3),
# RAIN (8), SNOW_RING (15), WET_CLOTH (17) et FOG_RING (18) sont servies aux
# entrees SPECIALES (VF5 R, ver.B), avec les donnees de leur generation --
# voir GENERATION_STUBS. Une entree clonee de FS ne les recoit pas : aucune
# tache n'est demandee sans son dossier pose (le tri final le garantit).
#
# Et YUKA (6) et RINGOUT_SPLASH (12), voir YUKA_SITES et RINGOUT_TABLE_VA.
EFFETS_SERVIS = (2, 3, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19)
                                               # WALL LEAF SNOW YUKA RIPPLE
                                               # RAIN THUNDER RINGOUT_SPLASH
                                               # WATER_RING SPLASH SNOW_RING
                                               # FOG_ANIM WET_CLOTH FOG_RING
                                               # BREATH
# Les noms des taches d'effet, lus dans le tableau de pointeurs 0x18034E4D0.
EFFETS_NOMS = (
    'EFFECT_HIT', 'EFFECT_AUTH3D', 'EFFECT_WALL', 'EFFECT_LEAF',
    'EFFECT_WATA', 'EFFECT_SNOW', 'EFFECT_YUKA', 'EFFECT_RIPPLE',
    'EFFECT_RAIN', 'EFFECT_THUNDER', 'EFFECT_DOWN', 'EFFECT_MOVE',
    'EFFECT_RINGOUT_SPLASH', 'EFFECT_WATER_RING', 'EFFECT_SPLASH',
    'EFFECT_SNOW_RING', 'EFFECT_FOG_ANIM', 'EFFECT_WET_CLOTH',
    'EFFECT_FOG_RING', 'EFFECT_BREATH', 'EFFECT_PARTICLE', 'EFFECT_POISON',
    'EFFECT_ELE_BOARD')

# ---------------------------------------------------------------------------
# LES EFFETS DU DECOR : DEUX TABLES DE PLUS, UNE PAR TACHE (2026-09-10)
#
# Le decor ajoute se chargeait, mais **sans ses flammes ni son mur**. Les deux
# manques ont la meme cause, et le decompilateur la nomme : a l'etat 3, le
# moteur donne l'indice du decor a chaque tache d'effet
# (`obj->vtable[7](obj, indice)`, dans `0x18006F380`), et **chaque tache a sa
# propre table indexee par le decor** :
#
#   TaskEffectAuth3D::setStage  0x1800706B0  -> table 0x18034FD20
#       22 entrees {indice, pointeur vers une liste d'uid}, terminees {-1, 0}
#       djo (11) -> [1193, 1191, 1192] : HATA, FIRE, FIRE_REFLECT
#
#   TaskEffectWall::setStage    0x1800843A0  -> table 0x180355C30
#       32 entrees de 0x40 {indice, trois pointeurs, quatre qwords a zero}
#       djo (11) -> {11, 0x180352060, 0x180352560, 0x180352568}
#
# Ce sont des LISTES D'ASSOCIATION, comme les sons d'ambiance : un indice
# inconnu ne plante pas, il ne fait RIEN. D'ou deux absences en silence.
#
# Les nombres `1191..1193` sont les **numeros d'uid d'`auth_3d_db`**
# (`uid.1191.value = A STGDJO_EFF_FIRE`). L'entree neuve doit donc porter NOS
# numeros, ceux que `decor_neuf.py` a attribues a la categorie `EFFSTG<CODE>`
# -- ils ne sont pas devinables, ils se lisent dans la base POSEE.
#
# Les deux tables sont pleines : apres le terminateur de la table Auth3D
# viennent des flottants (`0x18034FE90`). Elles demenagent donc dans `.decors`
# comme les quatre autres, et elles portent des POINTEURS, donc avec leurs
# relocations. Un seul site chacune, trouve par `refs_plage.py`.
EFFETS_A3D_VA = 0x18034FD20
EFFETS_A3D_N = 22
EFFETS_A3D_PAS = 0x10
EFFETS_A3D_SITES = ((0x1800706BC, 0x00),)      # lea dans 0x1800706B0
EFFETS_MUR_VA = 0x180355C30
EFFETS_MUR_N = 32
EFFETS_MUR_PAS = 0x40
EFFETS_MUR_SITES = ((0x1800843B0, 0x00),)      # lea dans 0x1800843A0
EFFETS_UIDS_MAX = 40                            # place reservee par decor neuf

# LES ANIMATIONS QUE 2008 A ET QUE FINAL SHOWDOWN N'A PLUS
#
# Frederic, 2026-09-10 : « il manque les personnages en 3D animes dans le
# decor ». Mesure sur `aur` : la liste d'animations d'effet du modele FS est
# `[JYOUKI, RORA]` -- de la vapeur et un rouleau. L'archive de 2008, elle,
# porte AUSSI `ARUKI`, `ARUKI_B`, `ARUKI_C` (aruki = la marche) et `KANKYAKU`
# (kankyaku = les spectateurs). Final Showdown les a coupees ; la liste du
# modele ne les demande donc pas, et le decor de 2008 restait desert.
#
# On ajoute donc a la liste toutes les animations de la categorie POSEE que le
# modele ne demandait pas -- sauf celles qu'un AUTRE mecanisme joue, sinon
# elles tourneraient deux fois ou hors de leur declencheur :
#
#   KABE_REACT, SAKU_*, BROKEN*   -> TaskEffectWall
#   DOWNKEMU                      -> TaskEffectDown
#   DASH                          -> TaskEffectMove
#
# La regle est ecrite ici pour pouvoir etre attaquee : c'est une PREMISSE, pas
# une mesure. Si une animation ajoutee se voit de travers, elle se retire de
# cette liste.
#
# 2026-09-10, deuxieme passe : la lecture des sept tables a NOMME trois
# mecanismes de plus, et la liste s'allonge d'autant.
#
#   TOIKI               -> TaskEffectBreath   (0x1806430C0, +0x0C)
#   KAMINARI, SKY_DOME  -> TaskEffectThunder  (0x180351B98, sept uid)
#
# Les laisser dans la liste auth_3d les jouerait EN BOUCLE : trois domes de
# ciel superposes sur `hi5`, un eclair permanent, un souffle qui ne s'arrete
# pas. La regle n'a pas change -- une animation appartient a UN mecanisme --
# c'est la mesure qui a rattrape la premisse.
EFFETS_AUTRES_MECANISMES = ('KABE_REACT', 'SAKU', 'BROKEN', 'DOWNKEMU',
                            'DASH', 'TOIKI', 'KAMINARI', 'SKY_DOME')

# LE REGISTRE : CE QU'ON A VU A L'ECRAN, ET RIEN D'AUTRE (2026-09-10)
#
# Cette liste etait une REGLE : « ajouter toutes les animations de 2008 que le
# modele ne demande pas, sauf celles qu'un autre mecanisme joue ». Frederic,
# le 2026-09-10 : « ne fais jamais de supposition, il y a des eclairs dans le
# decor de Goh en version R qui n'ont rien a y faire ».
#
# Il avait raison, et le defaut etait dans la regle elle-meme. La liste
# auth_3d d'un decor est la liste de ce qui tourne EN BOUCLE. Y verser une
# animation de 2008 revient a decider qu'elle est une boucle -- ce que rien ne
# dit. Sur `hi5` (Broken House, le decor de Goh), `LIHGT` et `SKY_HIKARI1` sont
# des eclairs d'UNE SECONDE, la duree exacte de `KAMINARI1` : des coups, pas
# des boucles. Ils clignotaient sans arret.
#
# On a cherche un meilleur critere -- la duree declaree dans le `.a3da`
# (`play_control.size / fps`) : ARUKI 65 s, ARUKI_B 117 s contre LIHGT 1,0 s.
# Mais `DENKI_B` fait 2,7 s et Final Showdown le joue bien en boucle : la duree
# ne PROUVE rien. Un critere plus fin resterait une supposition.
#
# Donc plus de regle du tout. Par defaut un decor ajoute joue exactement ce que
# son modele demande. Une animation de 2008 ne s'ouvre qu'apres avoir ete VUE,
# et son entree ici est le proces-verbal de cet essai. Le patcheur NOMME celles
# qu'il n'a pas jouees, pour qu'elles ne se reperdent pas.
# CE QU'UN VARIANT NE DOIT PAS AVOIR (2026-09-10)
#
# Le pendant d'ANIMATIONS_VALIDEES : un decor ajoute herite de la liste de
# taches de son modele, et parfois cet heritage est FAUX -- la generation de
# 2008 ne faisait pas la meme chose au meme endroit. Chaque entree porte le
# constat qui l'a decidee.
#
# Frederic, 2026-09-10 : « pour le decor de Goh, dans sa version FS, il y a des
# eclairs et c'est normal, n'y touche pas. Par contre dans sa version R, on voit
# des effets de l'eclair, avec des changements tres rapides de l'eclairage, et
# ca n'a rien a faire dans ce variant. »
#
# `hai` (13) garde donc son tonnerre, intact -- on ne touche a rien chez lui.
# C'est `hi5` (51) qui ne demande plus EFFECT_THUNDER : ni les quatre
# KAMINARI, ni les trois SKY_DOME. Ces derniers sont la cause mesuree du
# clignotement : dans les fichiers de 2008 ils portent 90 a 102 courbes de
# `light` et 18 a 48 de `camera_auxiliary` -- l'eclairage de scene et
# l'exposition de l'image entiere. Final Showdown, lui, les a vides sur `_M` et
# `_L` et ne les garde que sur `_H`.
#
# Si les eclairs eux-memes doivent revenir sans le clignotement, c'est une
# ligne a retirer ici, plus le retrait des courbes `light`/`camera_auxiliary`
# de NOS fichiers `STGHI5_EFF_SKY_DOME_M` et `_L` -- les notres, jamais ceux du
# jeu d'origine.
EFFETS_RETIRES = {
    'hi5': (9,),                               # EFFECT_THUNDER
}

ANIMATIONS_VALIDEES = {
    # ar5 -- Frederic, 2026-09-10 : « les personnages en 3D du decors sont
    # bien presents [...] ce decor est valide ».
    'ar5': ('EFF_ARUKI', 'EFF_ARUKI_B', 'EFF_ARUKI_C', 'EFF_KANKYAKU'),
    # jn5 -- Frederic, 2026-09-11 : « decor d'Aoi (shrine) ; il manque [...]
    # les personnages en 3D dans le decor ». L'archive de 2008 les porte, et
    # rien ne les jouait : ARUKI_A 94 s, ARUKI_B 187 s, ARUKI_C 60 s (des
    # marcheurs) et TALK 4 s (deux personnes qui parlent). Leurs objets sont
    # tous dans obj_db -- verifie. Les ANIMATIONS sont validees a l'ecran
    # le 2026-09-11 (« personnages en 3D dans le decor OK ») ; le DECOR,
    # lui, ne l'est pas : il lui manque encore le brouillard de premier
    # plan (groupe 1 de fog_jn5.txt).
    'jn5': ('EFF_ARUKI_A', 'EFF_ARUKI_B', 'EFF_ARUKI_C', 'EFF_TALK'),
}


def animations_en_plus(code, deja):
    """Les animations de 2008 que ce decor joue EN PLUS de la liste du modele.

    Rend `(a_jouer, disponibles)` : la liste `[(numero, nom), ...]` a ajouter,
    et celle des animations de 2008 qu'aucun mecanisme ne joue -- pour que le
    patcheur puisse les NOMMER sans les jouer.
    """
    import a3d_db
    chemin = os.path.join(JEU, 'vf5fs_media', 'rom', 'auth_3d',
                          'auth_3d_db.bin')
    if not os.path.exists(chemin):
        return [], []
    pose = a3d_db.charger(chemin)
    veut = ANIMATIONS_VALIDEES.get(code, ())
    a_jouer, dispo = [], []
    for k, v in sorted(pose.uids_de('EFFSTG%s' % code.upper()).items()):
        if k in deja:
            continue
        nom = v['value'].split()[-1]
        court = nom.split('_', 1)[-1] if '_' in nom else nom
        if any(x in court for x in EFFETS_AUTRES_MECANISMES):
            continue                      # un autre mecanisme la joue
        if court in veut or court.replace('EFF_', '') in veut:
            a_jouer.append((k, nom))
        else:
            dispo.append(court)
    return a_jouer, dispo

# ---------------------------------------------------------------------------
# LE MUR : CLONER SON ENTREE NE CLONE PAS LE MUR (2026-09-10, apres essai)
#
# Le decor ajoute s'est affiche AVEC SES FLAMMES et SANS SES BARRIERES. Les
# flammes etaient reparees parce que leur table porte des NUMEROS D'UID, qu'on
# a substitues. La table des murs, elle, ne porte que des POINTEURS : tout le
# mur est dans les TROIS BLOCS qu'ils designent, et ces blocs nomment leurs
# objets par `(objset << 16) | rang`.
#
# Pour `djo`, lus dans `.origine` :
#
#   +0x08 -> 0x180352060  LES MORCEAUX, 28 enregistrements de 0x2C, fin -1
#                         {objet, 10 flottants : x y z / rx ry rz / ... }
#                         4 poteaux (objset 28, rang 113 = STGDJO_EFF_POLE)
#                           aux quatre coins (+-6, +-6), tournes -45/45/135/225
#                         24 panneaux (objset 28, rang 47 = STGDJO_EFF_FENCE)
#                           a +-1, +-3, +-5 le long des quatre cotes
#                         -- c'est LITTERALEMENT la barriere du ring
#   +0x10 -> 0x180352560  LES UID, entiers termines par -1 : [1194]
#                         uid.1194.value = A STGDJO_EFF_KABE_REACT
#   +0x18 -> 0x180352568  LES PAIRES, 0x10 par entree, fin -1
#                         {intact, casse, uid, uid}
#                         {28:47 STGDJO_EFF_FENCE, 28:48 ..._FENCE_KOWARE,
#                          1194, 1194}
#   +0x20 -> [tache+0xD58], +0x28/+0x30/+0x38 -> trois arguments de plus.
#            NULS chez `djo` : on REFUSE si le modele en porte, plutot que de
#            recopier un bloc qu'on n'a pas lu.
#
# Un clone octet pour octet de l'entree renvoie donc a l'objset 28 et a l'uid
# 1194 -- l'objset du MODELE, qui n'est pas charge dans un build d'ajout, et un
# uid d'une autre categorie. `TaskEffectWall` ne trouve rien a poser : pas de
# barriere, et pas un message. C'est le meme defaut que les flammes, un cran
# plus bas.
# ---------------------------------------------------------------------------
# LE SON D'AMBIANCE : UNE SEPTIEME TABLE INDEXEE PAR LE DECOR (2026-09-10)
#
# `0x180408850`, 24 entrees de 0x10 : `{indice, pointeur vers un bloc de 0x30}`,
# terminee par `{-1, 0}`. Le bloc porte le fichier d'ambiance et les cris de
# choc contre le mur :
#
#     djo  +0x00 rom/sound/se_stage_djo.csb   +0x08 vfxse_wall_religious3
#                                             +0x20 stg_vfvse_floor_kishimi
#     aur  +0x00 rom/sound/se_stage_aur.csb   +0x08 stg_vf5r_wallbreak_stn1
#                                             +0x10 ...stn2  +0x18 ...stn3
#
# C'est une LISTE D'ASSOCIATION a valeur par defaut : `0x1801903DC` pose
# l'ambiance de `are` avant de chercher, et `0x1801903F3` parcourt. Un indice
# absent ne plante pas -- il prend `are`. C'est ce que les dix-neuf decors
# ajoutes avaient jusqu'ici.
#
# La table est suivie IMMEDIATEMENT de ses chaines (`0x1804089E0` porte
# `rom/sound/se_stage_are.csb`) : elle ne peut pas grandir sur place, elle
# demenage. Une entree neuve reprend le POINTEUR DE BLOC DU MODELE -- le decor
# ajoute est le meme lieu, il a la meme ambiance et les memes cris de mur, et
# le `.csb` du modele est deja dans le `.par`.
SON_TABLE_VA = 0x180408850
SON_TABLE_PAS = 0x10
SON_TABLE_N = 24
# Les deux sites sont l ADRESSE DU CHAMP disp32, pas celle de l instruction :
# 0x1801903D0 fait `cmp dword ptr [rip+d], 0` sur l entree 0 + 8 (le pointeur
# de bloc, teste contre zero -- c est le terminateur), puis `lea` sur la tete.
SON_TABLE_SITES = ((0x1801903D7, 0x08, 1), (0x1801903ED, 0x00))

# ---------------------------------------------------------------------------
# LES SEPT AUTRES TABLES D'EFFET (2026-09-10) -- TROIS FORMES, TROIS COUTS
#
# `0x18006F380` donne l'indice du decor a CHAQUE tache d'effet creee, par le
# creneau 7 de sa vtable (`(**(code **)(*tache + 0x38))(tache, indice)`), et
# chaque tache va chercher ses donnees a SA facon. Le decompilateur les a
# toutes rendues ; il y a exactement trois formes, et elles ne coutent pas la
# meme chose :
#
#   TABLEAU DENSE INDEXE PAR LE DECOR -- se deplace, un `lea` a repointer
#     DOWN  0x18034FF20   41 int   `t[indice]` = l'uid de STG<X>_EFF_DOWNKEMU
#     MOVE  0x180350820   41 int   `t[indice]` = l'uid de STG<X>_EFF_DASH
#     C'est une MINE, pas une liste d'association : au-dela de 41 le moteur
#     lit ce qui suit dans `.rdata` -- du TEXTE -- et le prend pour un uid.
#     Et ces deux taches-la sont dans les six TOUJOURS creees (0x18034D530) :
#     tout decor ajoute y passait, sans exception.
#
#   LISTE A PAS FIXE, FIN -1 -- se deplace, deux `lea` a repointer
#     SNOW  0x180643340   2 x 0x58, `{indice, ...parametres...}`, fin -1
#     Aucun uid dedans : de la neige, c'est un systeme de particules.
#
#   CHAINE DE COMPARAISONS DEROULEE -- le NOMBRE d'entrees est dans le CODE
#     BREATH   0x1806430C0  3 x 0x14  (16 yuk, 18 aur, 21 du1)  uid en +0x0C
#     FOG_ANIM 0x180643130  2 x 0x34  (14 are, 13 hai)          aucun uid
#     SPLASH   0x180643490  3 x 0x38  (via FUN_180080A10)
#     THUNDER  0x180351B98 / 0x180351BB8, compares aux LITTERAUX 13 et 24
#     Celles-la ne se deplacent pas toutes seules : le compilateur a deroule
#     la boucle en autant de `cmp` qu'il y a d'entrees. Les ajouter demande de
#     remplacer la selection par un balayage -- c'est un autre chantier, et
#     il est ecrit ici pour qu'il ne se reperde pas.
#
# Les uid sont ceux d'`auth_3d_db` : ils se TRADUISENT, comme partout ailleurs
# sur ce chantier (STGAUR_EFF_DOWNKEMU -> STGAR5_EFF_DOWNKEMU).
DOWN_TABLE_VA = 0x18034FF20                    # TaskEffectDown::setStage
DOWN_TABLE_SITES = ((0x1800713EF, 0x00),)      # lea rcx dans 0x1800713E0
MOVE_TABLE_VA = 0x180350820                    # TaskEffectMove::setStage
MOVE_TABLE_SITES = ((0x1800770AF, 0x00),)      # lea rcx dans 0x1800770A0
SNOW_TABLE_VA = 0x180643340                    # TaskEffectSnow::setStage
SNOW_TABLE_PAS = 0x58
SNOW_TABLE_N = 2
SNOW_TABLE_SITES = ((0x18007D20A, 0x00),       # mov eax, [rip+d]  (l'indice)
                    (0x18007D211, 0x00))       # lea rcx, [rip+d]  (la base)

# ---------------------------------------------------------------------------
# LES QUATRE CHAINES DEROULEES, ET COMMENT ON LES OUVRE (2026-09-10)
#
# BREATH, FOG_ANIM, SPLASH et THUNDER ne cherchent pas leur decor dans une
# table : le compilateur a DEROULE la boucle en autant de `cmp` qu'il y a
# d'entrees. Le nombre d'entrees vit donc dans le CODE, et deplacer la table
# ne suffirait a rien.
#
#     BREATH   0x180070E00  cmp edx,[rip]  x3  -> r15   sinon 0x180070F92
#     FOG_ANIM 0x180071B3E  cmp eax,[rip]  x2  -> rdx   sinon 0x180071B91
#     SPLASH   0x180080A30  cmp ebp,[rip]  x3  -> rsi   sinon 0x180080C6E
#     THUNDER  0x180082616  cmp edx, 13/24     -> rdi   sinon 0x180082693
#
# Ce que le compilateur a deroule, il l'a aussi PAYE en octets : la chaine
# occupe entre 26 et 63 octets, et un balayage tient dans 26. On remplace donc
# la chaine, SUR PLACE, par la boucle qu'elle etait :
#
#     lea  CUR, [rip + table]
#   L: cmp  dword ptr [CUR + decal], -1     ; le terminateur
#     je   AUCUN
#     cmp  IDX, dword ptr [CUR + decal]
#     je   TROUVE
#     add  CUR, pas
#     jmp  L
#   AUCUN: jmp <sortie d'origine>
#   TROUVE: <epilogue> puis on retombe sur la suite d'origine
#
# et la table demenage dans `.decors` avec un terminateur et des entrees en
# plus. Aucune caverne : tout tient dans la place liberee, et le patcheur
# REFUSE si le compte n'y est pas.
#
# THUNDER est le cas particulier : ses indices (13, 24) sont des LITTERAUX,
# pas un champ. Ses deux dossiers font 0x20 octets dont sept d'uid et un mot
# de bourrage en +0x1C -- c'est la qu'on ecrit l'indice, et le balayage compare
# `[rdi+0x1C]`. Le registre porte alors directement le dossier, comme avant.
CHAINES = {
    #        table VA,   pas,   n, decal, uids,             (depart, reprise, aucun)
    'BREATH': (0x1806430C0, 0x14, 3, 0x00, (0x0C,),
               (0x180070E00, 0x180070E3F, 0x180070F92),
               'rax', 'edx', b'\x4c\x8b\xf1', b'\x49\x89\xc7'),
    'FOG_ANIM': (0x180643130, 0x34, 2, 0x00, (),
                 (0x180071B3E, 0x180071B5E, 0x180071B91),
                 'rdx', 'eax', b'', b''),
    'SPLASH': (0x180643490, 0x38, 3, 0x00, (),
               (0x180080A30, 0x180080A6C, 0x180080C6E),
               'rsi', 'ebp', b'', b''),
    # RIPPLE : la chaine n'est pas dans `setStage` (un simple setter) mais
    # dans `FUN_18007AE10`, appelee depuis l'init. `mov r15d, edx` est pris
    # dans la zone : il faut le remettre en tete.
    'RIPPLE': (0x1806432E0, 0x2C, 2, 0x00, (),
               (0x18007AE1F, 0x18007AE4D, 0x18007B01D),
               'rcx', 'edx', b'\x41\x89\xd7', b''),
    'THUNDER': (0x180351B98, 0x20, 2, 0x1C,
                (0x00, 0x04, 0x08, 0x0C, 0x10, 0x14, 0x18),
                (0x180082616, 0x180082630, 0x180082693),
                'rdi', 'edx', b'', b''),
    # LEAF (2026-09-11) : deux `cmp eax, [rip]` dans l'init 0x180074EC0,
    # dossiers {indice, objet dessine en premier, objet dessine en second}
    # (ter 5, jin 9). `xor r8d, r8d` est pris dans la zone et sert plus loin
    # (`mov [rcx+0x64], r8d`) : il passe en tete. Sans dossier, l'init rend 0
    # (0x180074F0B).
    'LEAF': (0x180643248, 0x0C, 2, 0x00, (),
             (0x180074EC7, 0x180074EEA, 0x180074F0B),
             'rdx', 'eax', b'\x45\x33\xc0', b''),
}
# THUNDER compare des litteraux : ses deux dossiers portent ces indices-la.
CHAINES_INDICES = {'THUNDER': (13, 24)}
# Le nom de la tache d'effet, pour EFFETS_SERVIS et pour le journal.
CHAINES_TACHE = {'BREATH': 19, 'FOG_ANIM': 16, 'SPLASH': 14,
                 'THUNDER': 9, 'RIPPLE': 7, 'LEAF': 3}
# Les chaines dont le dossier nomme des OBJETS : un clone de FS (entree non
# speciale) les recopierait avec l'objset du modele. On ne les clone pas ; les
# entrees speciales, elles, les recoivent de leur generation, traduites.
CHAINES_OBJETS = ('LEAF',)

# ---------------------------------------------------------------------------
# RINGOUT_SPLASH (2026-09-11) : un TABLEAU borne par une adresse de fin
# litterale, 4 x 0x20 {indice, uid, uid _S, flottant, pointeur de chaine,
# decalage y, y}, lu par le setStage 0x180079A30 :
#
#     0x180079B6A  lea r8,  [rip+0x180350C10]     le debut
#     0x180079B74  lea rdx, [rip+0x180350C90]     la fin (4 x 0x20 plus loin)
#
# Il demenage dans `.decors` (avec les relocations de ses pointeurs) et les
# deux `lea` sont repointes -- la fin suit le nombre d'entrees.
#
# R et ver.B n'ont que 0x14 octets : ni le decalage y de l'animation (FS
# l'ajoute en 0x1800796B1), ni le y de l'entree que FS pousse dans la liste de
# 0x180677330 (0x180079729..0x180079786) -- leur code (R 0x84C4E30 /
# 0x84C4D20, ver.B 0x839511C) pose l'animation a la position calculee et ne
# pousse RIEN. D'ou : decalage 0,0, et un y NaN (0xFFFFFFFF) que le stub mis
# a la place du `call 0x18006F350` lit comme « ne pas pousser » -- il rend
# alors 0, ce que le moteur teste deja (`test rax, rax / je`).
RINGOUT_TABLE_VA = 0x180350C10
RINGOUT_TABLE_PAS = 0x20
RINGOUT_TABLE_N = 4
RINGOUT_SITE_DEBUT = 0x180079B6D           # disp32 du `lea r8`
RINGOUT_SITE_FIN = 0x180079B77             # disp32 du `lea rdx`
RINGOUT_SITE_POUSSEE = 0x180079729         # call 0x18006F350
RINGOUT_GESTIONNAIRE = 0x18006F350
RINGOUT_CHAINE_MAX = 0x20


def stub_ringout_poussee(va):
    """`cmp dword [rbx+rdi+0x4C], -1 ; jne 0x18006F350 ; xor eax,eax ; ret`
    -- rbx+rdi est l'element de la tache (0x1800796B1 y lit +0x48)."""
    c = bytearray(b'\x83\x7c\x3b\x4c\xff')
    c += b'\x0f\x85' + struct.pack('<i', RINGOUT_GESTIONNAIRE - (va + 11))
    c += b'\x31\xc0\xc3'
    return bytes(c)

_LEA = {'rax': b'\x48\x8d\x05', 'rcx': b'\x48\x8d\x0d',
        'rdx': b'\x48\x8d\x15',
        'rsi': b'\x48\x8d\x35', 'rdi': b'\x48\x8d\x3d'}
_MODRM = {'rax': 0, 'rcx': 1, 'rdx': 2, 'rsi': 6, 'rdi': 7}
_ADD = {'rax': b'\x48\x83\xc0', 'rcx': b'\x48\x83\xc1',
        'rdx': b'\x48\x83\xc2',
        'rsi': b'\x48\x83\xc6', 'rdi': b'\x48\x83\xc7'}
_REG32 = {'eax': 0, 'edx': 2, 'ebp': 5}


def _modrm(reg, base, decal):
    """`[base]` ou `[base+decal8]`, avec `reg` en champ /r."""
    b = _MODRM[base]
    if decal == 0:
        return bytes([0x00 | (reg << 3) | b])
    return bytes([0x40 | (reg << 3) | b, decal])


def balayage_chaine(nom, table_va, faits):
    """Les octets qui remplacent la chaine deroulee de `nom`.

    Rend `(adresse, octets)`, ou `(None, message)` si ca ne tient pas -- on
    ne tronque JAMAIS un patch de code, on refuse.
    """
    (_, pas, _, decal, _, (depart, reprise, aucun),
     cur, idx, prologue, epilogue) = CHAINES[nom]
    place = reprise - depart
    o = depart + len(prologue)
    lea_fin = o + 7
    # lea CUR, [rip + table]
    corps = prologue + _LEA[cur] + struct.pack('<i', table_va - lea_fin)
    etiq_l = lea_fin
    cmp_term = b'\x83' + _modrm(7, cur, decal) + b'\xff'
    cmp_idx = b'\x3b' + _modrm(_REG32[idx], cur, decal)
    apres_l = (etiq_l + len(cmp_term) + 2 + len(cmp_idx) + 2
               + len(_ADD[cur]) + 1 + 2)
    aucun_a = apres_l
    saut_aucun = _saut(aucun_a, aucun)
    trouve_a = aucun_a + len(saut_aucun)
    corps += cmp_term
    corps += b'\x74' + struct.pack('<b', aucun_a - (etiq_l + len(cmp_term) + 2))
    corps += cmp_idx
    corps += b'\x74' + struct.pack(
        '<b', trouve_a - (etiq_l + len(cmp_term) + 2 + len(cmp_idx) + 2))
    corps += _ADD[cur] + bytes([pas])
    corps += b'\xeb' + struct.pack('<b', etiq_l - apres_l)
    corps += saut_aucun + epilogue
    reste = place - len(corps)
    if reste < 0:
        return None, ('%s : le balayage fait %d octets et la chaine n en '
                      'occupe que %d' % (nom, len(corps), place))
    corps += b'\x90' * reste            # on retombe sur la suite d'origine
    faits.append('effets : la chaine de comparaisons DEROULEE de '
                 'TaskEffect%s (0x%X, %d octets) devient un balayage de %d '
                 'octets sur une table a terminateur -- le nombre d entrees '
                 'quitte le CODE pour les DONNEES.'
                 % (nom.title().replace('_', ''), depart, place,
                    len(corps) - reste))
    return depart, corps


def _saut(de, vers):
    """`jmp` court si possible, long sinon."""
    if -128 <= vers - (de + 2) <= 127:
        return b'\xeb' + struct.pack('<b', vers - (de + 2))
    return b'\xe9' + struct.pack('<i', vers - (de + 5))


EFFETS_MUR_PIECE_PAS = 0x2C      # un morceau de mur : {objet, 10 flottants}
EFFETS_MUR_PIECE_MAX = 256
EFFETS_MUR_PAIRE_PAS = 0x10      # {intact, casse, uid, uid}
EFFETS_MUR_PAIRE_MAX = 64


def mur_charge_modele(pe, entree):
    """Les trois blocs de charge d'une entree de la table des murs.

    `entree` est l'enregistrement de 0x40 octets, lu dans `.origine`. Rend un
    dictionnaire, ou None -- et le refus est deliberement bavard : recopier a
    l'aveugle un bloc qu'on n'a pas decode, c'est ce qui a coute la seance.
    """
    def lire(va, n):
        return pe.get_data(va - DECORS_BASE, n)

    ptrs = struct.unpack_from('<7Q', entree, 8)
    p_pieces, p_uids, p_paires = ptrs[0], ptrs[1], ptrs[2]
    p20, u28, o30, u38 = ptrs[3], ptrs[4], ptrs[5], ptrs[6]
    # SEUL LE PREMIER BLOC EST OBLIGATOIRE. `FUN_1800848C0` teste `param_3` et
    # `param_4` contre NULL : onze decors sur trente-deux n'ont que leurs
    # morceaux -- pas de liste d'uid, pas de paire intact/casse. Un mur qui ne
    # se casse pas, tout simplement.
    if not p_pieces:
        print('REFUS : l entree de mur du modele n a pas de bloc de morceaux.')
        return None
    n_pieces = 0
    while struct.unpack('<i', lire(p_pieces + n_pieces * EFFETS_MUR_PIECE_PAS,
                                   4))[0] != -1:
        n_pieces += 1
        if n_pieces > EFFETS_MUR_PIECE_MAX:
            print('REFUS : plus de %d morceaux de mur sans terminateur a '
                  '0x%X : ce n est pas le tableau attendu.'
                  % (EFFETS_MUR_PIECE_MAX, p_pieces))
            return None
    n_paires = 0
    while p_paires and struct.unpack('<i', lire(
            p_paires + n_paires * EFFETS_MUR_PAIRE_PAS, 4))[0] != -1:
        n_paires += 1
        if n_paires > EFFETS_MUR_PAIRE_MAX:
            print('REFUS : plus de %d paires intact/casse sans terminateur a '
                  '0x%X.' % (EFFETS_MUR_PAIRE_MAX, p_paires))
            return None
    uids = []
    while p_uids and struct.unpack('<i', lire(p_uids + 4 * len(uids), 4))[0] != -1:
        uids.append(struct.unpack('<i', lire(p_uids + 4 * len(uids), 4))[0])
        if len(uids) > EFFETS_UIDS_MAX - 1:
            print('REFUS : plus de %d uid de mur sans terminateur a 0x%X.'
                  % (EFFETS_UIDS_MAX - 1, p_uids))
            return None
    # LES QUATRE CHAMPS DE PLUS. Sept decors sur dix-neuf en portent, et ils
    # nomment eux aussi des objets et des uid : les recopier tels quels
    # renverrait a l'objset du modele, exactement comme les trois premiers.
    #
    #   +0x20  un SECOND tableau de morceaux, meme forme que +0x08 (0x2C),
    #          recopie dans `[tache+0xD58]`                      -- nyc
    #   +0x28  EXACTEMENT DEUX uid (`FUN_1800848C0` deroule `lVar13 = 2`) :
    #          l'animation du grillage, `EFF_SAKU_UP` / `_DOWN` -- yuk, gym
    #   +0x30  des enregistrements de 0x10 {objet, uid, ., .}, fin -1 : les
    #          objets cassables du decor                  -- umi, hai, aur, tan
    #   +0x38  un uid par enregistrement de +0x30, -1 quand il n'y en a pas
    extra = {}
    if p20:
        k = 0
        while struct.unpack('<i', lire(p20 + k * EFFETS_MUR_PIECE_PAS,
                                       4))[0] != -1:
            k += 1
            if k > EFFETS_MUR_PIECE_MAX:
                print('REFUS : le second tableau de morceaux (0x%X) n a pas '
                      'de terminateur.' % p20)
                return None
        extra['p20'] = [lire(p20, (k + 1) * EFFETS_MUR_PIECE_PAS), k]
    if u28:
        extra['u28'] = [bytearray(lire(u28, 8)), 2]
    if o30:
        k = 0
        while struct.unpack('<i', lire(o30 + k * EFFETS_MUR_PAIRE_PAS,
                                       4))[0] != -1:
            k += 1
            if k > EFFETS_MUR_PAIRE_MAX:
                print('REFUS : le tableau des objets cassables (0x%X) n a pas '
                      'de terminateur.' % o30)
                return None
        extra['o30'] = [lire(o30, (k + 1) * EFFETS_MUR_PAIRE_PAS), k]
    if u38:
        k = extra.get('o30', [None, 0])[1]
        if not k:
            print('REFUS : +0x38 (0x%X) sans +0x30 : on ne sait pas combien '
                  'd entiers lire.' % u38)
            return None
        extra['u38'] = [bytearray(lire(u38, k * 4)), k]
    return {
        'extra': extra,
        'pieces': lire(p_pieces, (n_pieces + 1) * EFFETS_MUR_PIECE_PAS),
        'n_pieces': n_pieces,
        'paires': (lire(p_paires, (n_paires + 1) * EFFETS_MUR_PAIRE_PAS)
                   if p_paires else b''),
        'n_paires': n_paires,
        'uids': uids,
        'a_uids': bool(p_uids),
        'a_paires': bool(p_paires),
    }


class Traducteur(object):
    """Rend a NOTRE decor les identifiants d'une generation (2026-09-11).

    Une donnee de generation nomme trois sortes de choses, et aucune ne se
    recopie telle quelle :

      . des ANIMATIONS par uid : la valeur dans SA base (`A STGHAI_EFF_FIRE`),
        renommee comme nos archives (`STGHAI_` -> `STGHIB_`), retrouvee dans
        la base POSEE, categorie `EFFSTG<eff>` ;
      . des TEXTURES par identifiant : telles quelles chez VF5 R (meme
        numerotation que FS), par NOM chez ver.B (`variantes_vf5`) -- et dans
        les deux cas l'identifiant doit etre dans NOS objsets ;
      . des OBJETS `(objset << 16) | rang` : l'objset de la generation devient
        le notre, le rang reste -- c'est l'archive de la generation qu'on pose.

    Chaque methode rend None quand elle ne sait pas : a l'appelant de RETIRER
    ce qui en dependait, jamais de deviner.
    """

    def __init__(self, e, g):
        import a3d_db
        import variantes_5r
        self.e, self.g = e, g
        pose = a3d_db.charger(os.path.join(JEU, 'vf5fs_media', 'rom',
                                           'auth_3d', 'auth_3d_db.bin'))
        # par le NOM de l'animation (le dernier mot de la valeur) : les
        # listes de la generation portent 'A STGDJO_EFF_FIRE' ou le nom seul
        self.u = dict((v.get('value', '').split()[-1], k) for k, v in
                      pose.uids_de('EFFSTG%s' % e['eff'].upper()).items())
        self.src, self.geo = e['src_geo'], e['geo']
        self.o_gen = g.objset_de(self.src)
        if self.o_gen is None:
            raise ValueError('%s : pas d objset STG%s' % (g.nom,
                                                          self.src.upper()))
        self.ids_geo = variantes_5r.ids_archive(self.geo) or set()
        self.o_ciel = self.ids_ciel = None
        if e.get('ciel'):
            self.o_ciel = g.objset_de(e['ciel'][2])
            self.ids_ciel = variantes_5r.ids_archive(e['ciel'][0]) or set()
        import variantes_vf5
        self.tex_nous = set(variantes_vf5.textures_objset(self.geo) or [])
        if e.get('ciel'):
            self.tex_nous |= set(variantes_vf5.textures_objset(
                e['ciel'][0]) or [])

    def uid(self, valeur):
        if valeur is None:
            return None
        nom = valeur.split()[-1]
        return self.u.get(nom.replace('STG%s_' % self.src.upper(),
                                      'STG%s_' % self.geo.upper()))

    def tex(self, t):
        if t in (0xFFFFFFFF, -1):
            return t & 0xFFFFFFFF
        if self.e['gen'] == 'verb':
            import variantes_vf5
            carte, _, _ = variantes_vf5.carte_textures()
            t = carte.get(self.g.nom_texture(t))
        return t if t in self.tex_nous else None

    def obj(self, v):
        v &= 0xFFFFFFFF
        if v == 0xFFFFFFFF:
            return v
        hi, r = v >> 16, v & 0xFFFF
        if hi == self.o_gen and r in self.ids_geo:
            return (self.e['objset'] << 16) | r
        if self.o_ciel is not None and hi == self.o_ciel and \
                r in self.ids_ciel:
            return (self.e['ciel'][1] << 16) | r
        return None

    def dossier(self, nom, b):
        """Un dossier d'effet de la generation, au format FS, traduit. Rend
        (octets, [ce qui manque])."""
        import generation
        ch = generation.CHAMPS[nom]
        b = bytearray(b)
        manque = []
        for o in ch.get('uids', ()):
            v = struct.unpack_from('<i', b, o)[0]
            if v == -1:
                continue
            n = self.uid(self.g.valeur_uid(v))
            if n is None:
                manque.append('uid %s' % self.g.valeur_uid(v).split()[-1])
                continue
            struct.pack_into('<i', b, o, n)
        for o in ch.get('tex', ()):
            v = struct.unpack_from('<I', b, o)[0]
            n = self.tex(v)
            if n is None:
                manque.append('texture %d' % v)
                continue
            struct.pack_into('<I', b, o, n)
        for o in ch.get('objets', ()):
            v = struct.unpack_from('<I', b, o)[0]
            n = self.obj(v)
            if n is None:
                manque.append('objet %d:%d' % (v >> 16, v & 0xFFFF))
                continue
            struct.pack_into('<I', b, o, n)
        # un OBJSET entier (YUKA nomme le sien) : celui de la generation
        # devient le notre
        for o in ch.get('jeux', ()):
            v = struct.unpack_from('<I', b, o)[0]
            if v != self.o_gen:
                manque.append('objset %d' % v)
                continue
            struct.pack_into('<I', b, o, self.e['objset'])
        return bytes(b), manque


def uids_correspondants(code, depuis, liste_modele, tolerant=False):
    """Nos numeros d'uid, dans l'ORDRE du modele. Rend None si l'un manque.

    La table des effets designe les animations par NUMERO d'uid dans
    `auth_3d_db` -- pas par nom. `decor_neuf.py` a recopie celles du modele
    sous la categorie `EFFSTG<CODE>` en les renommant (`STGDJO_` -> `STGD5R_`,
    l'index global des noms d'objets etant unique). On retrouve donc chaque
    numero par sa VALEUR, et on garde l'ordre du modele : c'est lui qui dit
    dans quel ordre le jeu les joue.

    On lit la base POSEE, pas une note : c'est elle qui a attribue les numeros.
    """
    import a3d_db
    chemin_pose = os.path.join(JEU, 'vf5fs_media', 'rom', 'auth_3d',
                               'auth_3d_db.bin')
    if not os.path.exists(chemin_pose):
        print('REFUS : %s n est pas pose. Passez decor_neuf.py --poser '
              'avant le patch.' % chemin_pose)
        return None
    orig = a3d_db.charger(os.path.join(RACINE, 'extracted', 'auth_3d_db.bin'))
    pose = a3d_db.charger(chemin_pose)
    u_orig = orig.uids()
    u_pose = {v.get('value'): k
              for k, v in pose.uids_de('EFFSTG%s' % code.upper()).items()}
    out = []
    for numero in liste_modele:
        valeur = u_orig.get(numero, {}).get('value')
        if valeur is None:
            print('REFUS : l uid %d du modele est introuvable dans '
                  'l auth_3d_db d origine.' % numero)
            return None
        neuve = valeur.replace('STG%s_' % depuis.upper(),
                               'STG%s_' % code.upper())
        if neuve not in u_pose:
            if tolerant:
                # LA GENERATION DE 2008 N'A PAS TOUJOURS L'ANIMATION.
                # `decor_neuf.py` ne declare que les uid dont le `.a3da` est
                # dans l'archive posee : `aur` n'a ni `EFF_SAKU_BROKEN` ni ses
                # deux `BROKEN_SHADOW`. L'appelant retire alors ce que cette
                # animation servait, plutot que de pointer sur un uid absent
                # -- que `TaskEffectWall` attendrait pour toujours.
                out.append(None)
                continue
            print('REFUS : « %s » (uid %d du modele) n a pas d equivalent '
                  '« %s » dans la categorie EFFSTG%s de la base posee. '
                  'decor_neuf.py et patch_moteur.py ne parlent pas du meme '
                  'decor.' % (valeur, numero, neuve, code.upper()))
            return None
        out.append(u_pose[neuve])
    return out
# LES BORNES. Toutes des comparaisons a un immediat, sauf la derniere qui borne
# en OCTETS (41 * 0xF0). Elles ne bougent QUE si N depasse 41 -- a N = 41 le
# correctif ne touche pas une seule de ces instructions, et c'est voulu : on
# veut pouvoir separer « le deplacement casse » de « la borne casse ».
#   (adresse du champ, taille, valeur attendue, ce que c'est)
DECORS_BORNES = (
    (0x1800D7132, 1, 0x28, 'cmp ecx, 0x28   table des codes'),
    (0x18018EF6E, 1, 0x29, 'cmp edx, 0x29   gestionnaire'),
    (0x18018F3D9, 1, 0x29, 'cmp r10d, 0x29  musique'),
    (0x18018F562, 1, 0x29, 'cmp ecx, 0x29   nom'),
    (0x18018F632, 1, 0x29, 'cmp ecx, 0x29   propriete +0xD4'),
    (0x18018FCF2, 1, 0x29, 'cmp ecx, 0x29   la demande'),
)
# LA SEPTIEME BORNE NE SE LEVE PAS, ET CE N'EST PAS UNE PRUDENCE.
#
# `analysis/ajouter_un_decor.md` la notait « 0x1801B5F7F, compteurs de parties,
# 41 entrees de 0x10 o, cmp r8d, 0x29 -- protege ». L'adresse etait celle du
# DEBUT DE FONCTION relevee dans `.pdata`, pas celle de la comparaison : les
# vraies sont 0x1801B648D et 0x1801B6507 (plus 0x1801B6483, `cmp r8d, 0x22`,
# la version deroulee par huit, soit N - 7).
#
# Mais surtout, relue le 2026-09-09, cette boucle n'indexe pas une table de
# `.rdata` : elle recopie des compteurs d'un OBJET vers un autre.
#
#   source       [r14 + 0x11FC + i*8]     deux dwords : parties, victoires
#   destination  [rdi + 0x1A2EC + i*0x10] trois dwords et un ratio flottant
#
# Et les deux tableaux sont EXACTEMENT dimensionnes a 41 : juste apres la
# boucle, le code fait `lea rsi, [rdi + 0x1A580]` -- or 0x1A2EC + 41*0x10 =
# 0x1A57C -- et `lea rbx, [r14 + 0x1348]` -- or 0x11FC + 41*8 = 0x1344. La
# 42e entree ecrirait dans le champ suivant de la structure.
#
# Lever cette borne ne donnerait donc pas des statistiques pour les decors
# ajoutes : cela corromprait l'objet. On la laisse a 41, definitivement. Les
# decors ajoutes n'auront pas de compteur de parties, et c'est tout.
#
# LA LECON POUR LA SUITE, et elle vaut plus que la borne elle-meme : toutes les
# bornes a 41 ne sont pas des bornes de TABLE. Certaines sont des TAILLES DE
# TABLEAU dans une structure. Avant d'en lever une, verifier ce qui suit le
# tableau -- ici, une seule instruction le disait.
DECORS_BORNE_COMPTEURS = (
    (0x1801B6483, 0x22, 'cmp r8d, 0x22   compteurs, boucle deroulee (N-7)'),
    (0x1801B648D, 0x29, 'cmp r8d, 0x29   compteurs, entree de la boucle'),
    (0x1801B6507, 0x29, 'cmp r8d, 0x29   compteurs, boucle simple'),
)
DECORS_BORNE_OCTETS = (0x18018F5E4, 4, 0x2670, 'cmp r9, 41*0xF0  nom -> index')
DECORS_SECTION = b'.decors\x00'
# LE MODELE DES ENTREES NEUVES, ET POURQUOI IL EN FAUT UN
#
# Une entree de descripteur laissee a ZERO n'est pas neutre : `0x18018F590`
# balaie les N descripteurs et DEREFERENCE `+0x00` pour comparer le nom --
# `mov r8, [r9+rbx]` puis `movzx ecx, [rax+r8]`. Un pointeur nul y lit a une
# adresse absurde. La borne levee sans contenu valide serait donc une mine.
#
# Toute entree au-dela de 41 est par consequent un CLONE octet pour octet du
# descripteur modele -- `djo` par defaut -- avec son propre code a trois
# lettres. Tous ses pointeurs restent valides et relogés ; rien ne la
# selectionne tant qu'un anneau ou une case ne la nomme pas.
DECORS_MODELE = 11                       # djo
DECORS_CODE_NEUF = 'x%02d'               # x00, x01, … -- trois lettres

# UN DECOR VRAIMENT AJOUTE  (`--decor-neuf <code> --objset <id> --auth3d <NOM>`)
#
# La premiere entree neuve (indice 41) cesse d'etre un clone du dojo et recoit
# ce qui la rend distincte. Tout ce qu'il lui faut est un POINTEUR, et c'est
# precisement ce qu'une section greffee ne pouvait pas porter avant le
# 2026-09-09 :
#
#   +0x00  « STGD5R »                  le nom du jeu d'animation
#   +0x08  « EFFSTGD5R »               celui des effets
#   +0x10  l'identifiant d'objset      neuf, pris dans obj_db.bin
#   +0x14..+0x24  (objset << 16) | rang   les cinq objets
#   +0x48  « rom/STGD5R_COLI.000.bin » sa collision
#
# Tout le reste vient du modele et reste JUSTE : les neuf reprises de musique,
# la table des murs (+0xC0), les proprietes de rendu, la taille de l'aire.
# C'est la difference entre ce decor-ci et celui pose sur `trs` en septembre,
# qui perdait dix champs sur dix-sept.
#
# LES NOMS SE DEDUISENT DU CODE, et leurs longueurs se correspondent -- c'est
# ce qui permet a `importer_decor.py` de renommer les archives en place :
#   djo (3) -> d5r (3)   stgdjo (6) -> stgd5r (6)   EFFSTGDJO (9) -> EFFSTGD5R
# LES CINQ OBJETS D'UN DECOR NE SONT PAS AUX MEMES RANGS D'UN DECOR A L'AUTRE.
#
# Ceci valait `(114, 118, 117, 116, 115)` -- gnd, ring, sky, sdw, reflect -- et
# c'etait juste POUR `djo`, le premier decor ajoute. Mesure du 2026-09-10 sur
# les dix-neuf modeles : **dix-huit ont d'autres rangs**, et plusieurs ont des
# emplacements VIDES (`0xFFFFFFFF`) :
#
#     djo  114 118 117 116 115        aur  413 598 414  -1  -1
#     ban  817 941 818  -1 942        gym    0 158   1  -1 151
#     cas  151 181  -1 153 152        smo    0 308   1  -1  -1
#
# Ecrire les rangs de `djo` chez `aur` demande donc les objets 114 a 118 de
# l'objset d'`aur` -- des morceaux d'effet pris au hasard -- et rate les
# vrais. C'est ce qui donnait, selon le decor, un plantage, un chargement
# infini, ou un decor tres incomplet.
#
# Les cinq champs se recopient donc du MODELE, l'objset substitue et le rang
# INCHANGE ; `0xFFFFFFFF` (« pas d'objet ») passe tel quel.
DECOR_NEUF_RANGS = (114, 118, 117, 116, 115)   # djo seul : gnd ring sky sdw reflect
DECOR_NEUF_ROLES = ('gnd', 'ring', 'sky', 'sdw', 'reflect')

# L'INDICE 41 EST RESERVE, ET IL A COUTE UN ESSAI A L'ECRAN
#
# Frederic, 2026-09-09 : « le decor charge est celui d'un decor de FS charge au
# hasard ». Le premier decor ajoute avait ete pose a l'indice 41 -- le premier
# libre apres les 41 du jeu, indices 0 a 40.
#
# Sauf que **41 = 0x29 est le code « decor ALEATOIRE »**. Sept sites le testent
# par EGALITE, et non comme une borne :
#
#   0x18013391E   un balayage de liste cherchant la valeur 41
#   0x1801744AE   0x1801744AF   0x1801748F3   0x180174930   0x180174A4C
#                 TaskSelStage : la case ALEA, dont l'icone est
#                 `stage_icon_rnd_c` et dont le champ +0x08 vaut 41
#   0x18001422D   idem, ailleurs
#
# La garde du gestionnaire le disait deja, pour qui savait lire : `cmp edx,
# 0x29 ; jae` accepte 0..40, soit les 41 decors -- et laisse 41 dehors. Lever
# cette borne a rendu 41 adressable comme descripteur, sans lui retirer son
# sens de sentinelle ailleurs. Le decor s'y chargeait donc, et le tirage au
# sort aussi.
#
# LA REGLE : un decor ajoute commence a 42. On garde 41 pour ce qu'il est.
DECORS_INDICE_ALEA = 41
DECORS_PREMIER_NEUF = DECORS_INDICE_ALEA + 1

# LE MODE DOJO CHOISIT SON DECOR EN DUR  (`--dojo-decor <indice>`)
#
# Mesure du 2026-09-09, apres un journal de sonde qui ne montrait qu'UNE
# demande, `index 39 (gym)`, et jamais notre 42 :
#
#   0x18020AE50   cmp ecx, 1        ... le mode 1
#                 test dl, dl
#   0x18020AE6E   mov eax, 0x27     39 = gym, la Training Room
#   0x18020AE73   mov ecx, 0x0B     11 = djo, le dojo d'Akira
#   0x18020AE78   cmovne eax, ecx   dl != 0 -> djo, sinon -> gym
#   0x18020AE7B   mov [0x180754A58], eax
#
# ATTENTION -- CETTE LECTURE ETAIT FAUSSE, et Frederic l a tranchee le
# 2026-09-10 : le mode DOJO A BIEN un ecran de selection de decor. Ne pas
# reecrire ici qu il n en a pas. Ce qui est vrai : ce bloc pose l un des deux
# indices en dur. Le decor ajoute n'etait pas rejete -- il n'etait pas demande.
#
# Cette option remplace l'immediat « djo » par l'indice qu'on veut. C'est le
# seul chemin qui rende un decor ajoute visible sans passer par le mode
# VERSUS -- lequel demande une seconde manette.
DOJO_DECOR_GYM = (0x18020AE6F, 39, 'mov eax, 39 -- gym, la Training Room')
DOJO_DECOR_DJO = (0x18020AE74, 11, 'mov ecx, 11 -- djo, le dojo d Akira')

# ---------------------------------------------------------------------------
# L'ECRETAGE QUI RAMENAIT TOUT A LA TRAINING ROOM (`--decor-ecretage`,
# `--decor-repli`)   -- lu le 2026-09-10
#
# LE 39 NE VENAIT PAS DU MODE DOJO. La sonde du 2026-09-09 avait mesure zero
# passage sur le `cmovne` du bloc ci-dessus (0x18020AE78) : le mode DOJO ne
# prend donc PAS cette branche, et `--dojo-decor` patchait un immediat qui ne
# s'execute pas. La chaine reelle, lue d'un bout a l'autre, est celle-ci --
# chaque maillon vient d'une enumeration COMPLETE de references, jamais d'un
# candidat choisi a la lecture :
#
#   0x18020AE60   mov [0x180754A58], r9d      l'indice du mode. Ses DEUX
#                                             appelants (enumeres) passent
#                                             r9d = -1 (0x1801E51FB) ou
#                                             r9d = [0x180C406FC] (0x18023E19D)
#   0x180209B16   cmovne ebx, [0x180754A58]   si le mode console est actif
#   0x180209B31   call 0x180203E40 (ecx=ebx)  les parametres du combat
#   0x180203F0F   mov eax, 0x27               39 = gym
#   0x180203F1E   cmp ebp, 0x28               l'indice demande
#   0x180203F2E   cmova ebp, eax              >>> AU-DESSUS DE 40 : 39 <<<
#   0x180203F34   mov [params + 0xD0], ebp
#   0x1802035A4   mov ecx, [params + 0xD0]
#   0x1802035AA   call 0x18018FCF0            TaskStage::demander
#   0x18018FD01   mov [TaskStage + 0x60], ecx la demande
#   0x18018EF8B   mov [TaskStage + 0x5C], edx la recopie, par le validateur
#   0x18018F8A3   -> le chargeur, index = [TaskStage + 0x5C]
#
# `cmova` est un ECRETAGE NON SIGNE. Un indice de -1 -- « aucun decor choisi »,
# ce que l'appelant 0x1801E51FB pose en dur -- vaut 0xFFFFFFFF : il est donc
# « au-dessus de 40 » et devient **39, gym**. C'est mot pour mot ce que la
# sonde voyait : un seul chargement, `index 39 (gym)`, quel que soit le patch.
#
# POURQUOI AUCUNE DES SIX BORNES NE L'AVAIT ATTRAPE : elles ont toutes ete
# trouvees en enumerant les LECTEURS des deux tables de decors. Celle-ci ne lit
# aucune table -- elle assainit un indice avant de le ranger dans les
# parametres du combat. Une borne n'est donc pas forcement un `jae` devant une
# table ni une sentinelle `je` : elle peut etre un `cmov` avec valeur de repli.
# Un balayage de tout `.text` pour la forme « cmp reg, 40/41 ... cmov » rend
# quinze sites ; les neuf du groupe 0x1800A2xxx sont le classificateur deja
# ecarte le 2026-09-09, et 0x180203F1E est le seul qui ecrete un indice de
# decor. La premisse de ce balayage, pour qu'on puisse l'attaquer : il ne voit
# QUE la forme `cmp`+`cmov`. Un ecretage ecrit en branchement
# (`cmp` / `jbe` / `mov`) lui echapperait.
#
#   --decor-ecretage <N>   porte la borne a N - 1, comme --decors-table porte
#                          les six autres. Sans elle, un indice de 42 est
#                          ramene a 39 avant meme d'etre demande ;
#   --decor-repli <i>      remplace le repli gym par <i>. C'est le seul geste
#                          qui rende un decor ajoute visible quand l'appelant
#                          ne demande RIEN (-1), ce qui est le cas du DOJO.
#
# Les deux se completent : l'ecretage laisse passer un indice demande, le repli
# choisit ce qu'on obtient quand personne ne demande.
ECRETAGE_BORNE = (0x180203F20, 1, 0x28, 'cmp ebp, 0x28 -- ecretage de l indice')
ECRETAGE_REPLI = (0x180203F10, 4, 39, 'mov eax, 39 -- le repli, gym')

# ---------------------------------------------------------------------------
# LES BASES SONT EMBARQUEES DANS LE BINAIRE (`--obj-db-libre`) -- 2026-09-10
#
# Pourquoi le decor ajoute ne chargeait toujours pas : le moteur ne lisait NI
# notre `obj_db.bin` pose dans `vf5fs_media/rom/objset/`, NI celui du `.par`.
# Trois mesures le disaient, et toutes les trois semblaient impossibles
# ensemble :
#
#   . masquer le nom dans l'index du `.par` -- des deux facons, dernier
#     caractere puis premier -- ne changeait rien ;
#   . `tracer_fichiers.py --tout` ne montrait AUCUNE ouverture de
#     `rom/objset/...` sur le disque : seul le `.par` etait ouvert ;
#   . ecrire nos octets DANS le `.par` (entree d'index repointee, membre non
#     comprime en fin d'archive) ne changeait rien non plus.
#
# La raison est dans le binaire : il porte une **archive FArC embarquee** en
# `0x1804137F0`, et elle contient les bases :
#
#     mot_db.bin        offset 0x00000136  comprime  83693   taille  290208
#     obj_db.bin        offset 0x00014823  comprime 262037   taille 1141248
#     tex_db.bin        offset 0x000547B8  comprime 184594   taille  841776
#     spr_db.bin        offset 0x000818CA  comprime 418011   taille 1524752
#     aet_db.bin        offset 0x000E79A5  comprime  15540   taille   45520
#     rob_mot_tbl.bin   offset 0x000EB659  comprime  10188   taille   79808
#     tst.ibl + les cinq light_param de `tst`
#
# `obj_db.bin` y fait 1 141 248 octets : l'original a l'octet pres. Le chargeur
# `0x1800F97E0` compose bien `./rom/objset/obj_db.bin`, mais le resolveur
# consulte d'abord cette archive-la, decompresse le membre dans le tas, et rend
# un pointeur qui n'est dans AUCUN module -- ce que la sonde montrait sans
# qu'on sache le lire.
#
# LA PREUVE CROISEE, et elle est nette : `auth_3d_db.bin` n'est PAS dans cette
# archive, et c'est justement la seule base dont le masquage du `.par`
# fonctionnait -- `tracer_fichiers.py` la voyait s'ouvrir sur le disque. Les
# fichiers qui ignoraient nos masquages sont exactement ceux qui sont embarques.
#
# LE CORRECTIF est le meme geste que le masquage du `.par`, mais dans le
# binaire : un octet, le `n` de `obj_db.bin` dans l'en-tete du FArC embarque.
# Le membre devient introuvable sous ce nom, et le resolveur passe a la suite --
# le `.par`, puis le disque. Le patcheur repartant toujours de `.origine`,
# retirer l'option rend l'archive embarquee intacte.
#
# On ne touche qu'a `obj_db.bin` : les quatre autres bases embarquees n'ont
# aucune raison d'etre liberees, et chacune est un risque en plus.
OBJDB_EMBARQUE = (0x18041381C, ord('n'),
                  'le « n » de obj_db.bin dans le FArC embarque en 0x1804137F0')
MASQUE_EMBARQUE = ord('_')



# ---------------------------------------------------------------------------
# LA GRILLE DE SELECTION  (`--grille-table`, avec `--decors-table`)
#
# Deux tables de cases de 0x20 octets, contigues :
#
#   0x180400210   21 cases, 3 lignes x 7 colonnes, AVEC icone   -- hors ligne
#   0x1804004B0   22 cases, 2 x 11, SANS icone                  -- bornes liees
#   0x180400770   la liste d'exclusion : DEUX qwords, -1 et 0
#   0x180400778   ... et TOUT DE SUITE les chaines d'icones
#
# UNE ERREUR DE LA DOC EST CORRIGEE ICI. `ajouter_un_decor.md` §6.2 annoncait
# « 0x560 octets d'affilee = 43 cases » en comptant sur la table des bornes
# liees comme sur de la place libre. C'est faux : juste apres elle vient la
# liste d'exclusion, puis **les chaines `stage_icon_*_c` que la grille
# elle-meme pointe**. Ecrire 43 cases la detruirait les noms d'icones. La
# mesure : 0x180400778 porte 'stage_icon_are_c', et la case 0 y pointe.
#
# On ne s'entasse donc plus : la grille DEMENAGE dans `.decors`, comme les deux
# autres tables, avec ses relocations. Ses 21 pointeurs d'icone en ont une
# chacun ; la table des bornes liees, elle, n'en a aucune (pas d'icone) et ne
# bouge pas -- ce build n'utilise pas le mode bornes liees.
#
# LA CASE, mesuree le 2026-09-09
#   +0x00 colonne   +0x04 ligne   +0x08 INDEX DU DECOR   +0x0C 332
#   +0x10 331       +0x18 pointeur vers 'stage_icon_xxx_c'
# (332 / 331 sont le pas de cellule ; la table des bornes liees a 0 partout.)
#
# LES CINQ SITES, enumeres par `refs_plage.py` -- ils visent la base ET `+0x8`,
# le champ d'index, sur lequel deux boucles balaient.
GRILLE_TABLE_VA = 0x180400210
GRILLE_TABLE_N = 21
GRILLE_TABLE_PAS = 0x20
GRILLE_TABLE_SITES = (
    (0x1801746CE, 0x00),   # le compte et la table passes au constructeur
    (0x180174928, 0x08),   # recherche de la case ALEA : balayage sur +8
    (0x180174947, 0x00),   # ... et la base pour calculer l'adresse
    (0x180174BAE, 0x08),   # index de decor -> case : balayage sur +8
    (0x180174BCE, 0x00),   # ... et la base
)
# Les quatre nombres a changer LE JOUR ou la grille grandira. Ils ne sont pas
# touches par le simple demenagement.
GRILLE_TABLE_COMPTES = (
    (0x1801746D4, 4, 21, 'mov r8d, 21 -- le compte passe a 0x180173BD0'),
    (0x18017493F, 1, 21, 'cmp rbx, 21 -- recherche de la case ALEA'),
    (0x180174BC1, 1, 21, 'cmp rax, 21 -- index de decor -> case'),
    (0x180174AA3, 4, 0x2A0, 'cmp rsi, 21*0x20 -- le tirage au sort'),
)
# Et ce qui N'EST PAS un compte, releve au passage : `0x180174C00` et
# `0x18017507B` portent 0x2C0, mais ce sont `sub rsp, 0x2C0` et `add rsp,
# 0x2C0` -- la taille de pile du constructeur d'apercus. Une valeur qui
# ressemble a 22*0x20 n'est pas pour autant un compte de cases.


# ---------------------------------------------------------------------------
# LA COLLISION DE DU2 : un defaut du build d'origine, pas du notre
#
# Releve le 2026-09-07 a partir d'une observation de Frederic : « dans ce
# decor, le personnage en ring out est sur un sol qui n'existe pas, il devrait
# chuter beaucoup plus bas. »
#
# Le descripteur de du2 (`0x1804048D0`) pointe sa collision sur
# **`rom/STGDU1_COLI.000.bin`** -- celle de du1. Ce n'est pas un partage
# volontaire :
#
#   . `STGDU2_COLI.000.bin` EXISTE dans le `.par` : 3 984 octets, contre 5 744
#     pour celle de du1. Deux tailles differentes, donc deux formes de sol ;
#   . la chaine `rom/STGDU2_COLI.000.bin` **n'existe nulle part dans le
#     binaire** -- elle n'a jamais ete emise a la compilation ;
#   . du2 se retrouve dans le meme sac que `trm`, `cid` et `trs`, les trois
#     decors d'essai, qui prennent la collision de du1 faute d'en avoir une.
#
# Le correctif ecrit la chaine manquante dans le MOU DE FIN DE `.rdata`
# (`0x180641B56`-`0x180641C00`, 170 octets a zero, compris dans
# `SizeOfRawData` donc bel et bien projete en memoire -- c'est la meme
# mecanique que la caverne de fin de `.text` deja utilisee en `0x18034575C`),
# puis repointe le champ `+0x48` du descripteur.
DU2_COLI_CHAINE_VA = 0x180641B60          # aligne a 16 dans le mou de .rdata
DU2_COLI_CHAINE = b'rom/STGDU2_COLI.000.bin\x00'
DU2_COLI_PTR_VA = 0x180404918             # descripteur de du2, champ +0x48
DU2_COLI_PTR_TETE = struct.pack('<Q', 0x180407920)   # -> rom/STGDU1_COLI...

# ---------------------------------------------------------------------------
# NE PAS TOUCHER AU CHAMP +0x18 D'UNE CASE DE GRILLE. Erreur payee le
# 2026-09-07, et elle a casse l'ecran de trois facons a la fois.
#
# J'avais lu `+0x18` comme « le nom de l'icone a dessiner » et j'ai fait
# pointer quatre cases sur `stage_icon_dur_c` pour qu'elles montrent Dural.
# Resultat rapporte par Frederic : les icones n'avaient pas change, le curseur
# sautait quatre cases, et la case restante rendait un autre decor que le sien.
#
# `+0x18` n'est pas une icone : c'est **le sprite d'ANCRAGE qui donne a la case
# sa position a l'ecran**. Le constructeur de grille `0x180173BD0` le lit ainsi
# (rsi = table + 4, donc `[rsi+0x14]` = case+0x18) :
#
#     cmp qword [rsi+0x14], 0     ; pas d'ancre -> position INTERPOLEE
#     je  0x180173DAC
#     ...
#     call 0x1800298B0(buf, [rsi+0x14])   ; resout le sprite par son NOM
#     vmovsd xmm0, [rax+0x40]             ; -> x, y REELS du sprite
#     vmovsd [r14+rdi+8], xmm0            ; la position de la case
#
# Quatre cases pointant sur le meme sprite recoivent donc **les memes x et y** :
# cinq entrees empilees au meme endroit. Le curseur n'en atteint qu'une, et la
# selection rend n'importe laquelle des cinq. Les trois symptomes tiennent a
# cette seule ligne.
#
# Et l'icone dessinee ne vient pas de la : elle est peinte par la scene AET
# `SEL_STAGE`. La changer demande de toucher aux donnees 2D du `.par`
# (`spr_db` / `aet_db` et la planche), pas a cette table.
#
# Le champ sur lequel on PEUT agir sans rien deplacer est `+0x08`, l'indice de
# decor -- c'est ce que fait `--decors-dural-grille`, et lui ne touche ni a la
# position ni au dessin.

MENU_TIC = 0x1801BBB10             # le tic d'un objet AET
MENU_MAJ = 0x1801DC620             # la mise a jour de la page de menu
MENU_VTABLE_C2 = 0x180532AF8       # creneau 2 de la vtable 0x180532AE8
MENU_CAVE = 0x18034575C            # 164 octets libres en fin de .text
MENU_OBJ_ENTETE = 0x240
MENU_OBJ_TEXTE = 0x298
MENU_OBJ_TROIS = 0x2F0
# Les trois objets que le bloc 0x1801DCE96 fait avancer. Le relais les reprend
# tous les trois, pour etre l'exact equivalent de ce bloc -- c'est ce qui
# permet d'emprunter le chemin "avec service" (--menu-service), ou ce bloc
# n'est plus atteint, sans perdre l'affichage.


def relais_menu(cave):
    """Le relais, assemble a la main. Convention Microsoft x64.

    A l'entree rsp vaut 8 modulo 16 ; `sub rsp, 0x38` le ramene a 0, si bien
    que le `call` retrouve la convention. Les 32 premiers octets sont l'espace
    d'accueil du callee, et `[rsp+0x30]` sert de rangement pour `rcx`.
    """
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    c = b''
    c += bytes.fromhex('4883EC38')                       # sub rsp, 0x38
    c += bytes.fromhex('48894C2430')                     # mov [rsp+0x30], rcx
    c += bytes.fromhex('4881C1') + struct.pack('<I', MENU_OBJ_ENTETE)
    c += b'\xE8' + rel(cave + len(c) + 5, MENU_TIC)      # call tic
    c += bytes.fromhex('488B4C2430')                     # mov rcx, [rsp+0x30]
    c += bytes.fromhex('4881C1') + struct.pack('<I', MENU_OBJ_TEXTE)
    c += b'\xE8' + rel(cave + len(c) + 5, MENU_TIC)      # call tic
    c += bytes.fromhex('488B4C2430')                     # mov rcx, [rsp+0x30]
    c += bytes.fromhex('4881C1') + struct.pack('<I', MENU_OBJ_TROIS)
    c += b'\xE8' + rel(cave + len(c) + 5, MENU_TIC)      # call tic
    c += bytes.fromhex('488B4C2430')                     # mov rcx, [rsp+0x30]
    c += bytes.fromhex('4883C438')                       # add rsp, 0x38
    c += b'\xE9' + rel(cave + len(c) + 5, MENU_MAJ)      # jmp la fonction vraie
    return c


def transition_cave():
    """Le corps du maillon 1+3, pose dans la caverne de fin de `.text`.

    Convention Microsoft x64. Au `call` qui nous amene ici, rsp vaut 0 modulo
    16 (l'hote a `push rdi` puis `sub rsp, 0x20`) ; le `call` empile 8, donc a
    l'entree rsp vaut 8. `sub rsp, 0x28` le ramene a 0 et reserve les 32 octets
    d'espace d'accueil que la convention exige de l'appelant.
    """
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    a = TRANSITION_CAVE
    c = b''
    c += bytes.fromhex('4883EC28')                            # sub rsp, 0x28
    c += b'\xE8' + rel(a + len(c) + 5, SESSION_LIRE)           # call session_lire
    c += bytes.fromhex('4885C0')                              # test rax, rax
    c += bytes.fromhex('7507')                                # jne +7 (deja la)
    c += bytes.fromhex('33C9')                                # xor ecx, ecx
    c += b'\xE8' + rel(a + len(c) + 5, SESSION_CREER)          # call session_creer
    c += b'\xB9' + struct.pack('<I', MODE_GAME)               # mov ecx, 2
    c += b'\xE8' + rel(a + len(c) + 5, DEMANDER_MODE)         # call demander_mode
    c += b'\xB9' + struct.pack('<I', SOUS_ETAT_SELECTOR)      # mov ecx, 17
    c += b'\xE8' + rel(a + len(c) + 5, DEMANDER_SOUS_ETAT)    # call demander_sous_etat
    c += bytes.fromhex('4883C428')                            # add rsp, 0x28
    c += b'\xC3'                                              # ret
    if len(c) > TRANSITION_CAVE_MAX:
        raise AssertionError('la caverne deborde : %d > %d octets'
                             % (len(c), TRANSITION_CAVE_MAX))
    return c


def transition_menu():
    """Les 27 octets du maillon 1 : appeler la caverne, puis sortir.

    L'epilogue vise restaure `rbx` depuis [rsp+0x30], ou il est sauve a
    0x1801DDF7D -- avant notre code. Le saut est donc legitime.
    """
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    a = TRANSITION_HOOK
    c = b''
    c += b'\xE8' + rel(a + len(c) + 5, TRANSITION_CAVE)      # call caverne
    c += b'\xE9' + rel(a + len(c) + 5, TRANSITION_EPILOGUE)  # jmp epilogue
    reste = (TRANSITION_FIN - TRANSITION_HOOK) - len(c)
    if reste < 0:
        raise AssertionError('le maillon 1 deborde de %d octets' % -reste)
    return c + b'\x90' * reste


def transition_versus():
    """Le relais du maillon 5, pose dans la caverne.

    Meme convention que `transition_cave` : a l'entree rsp vaut 8 modulo 16
    (l'hote a `push rbx` puis `sub rsp, 0x70`, donc 0 avant son `call`), et
    `sub rsp, 0x28` ramene a 0 en reservant l'espace d'accueil. `rcx` n'est pas
    touche : l'enregistrement recoit son argument intact.
    """
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    a = VERSUS_CAVE
    c = bytes.fromhex('4883EC28')                             # sub rsp, 0x28
    c += b'\xE8' + rel(a + len(c) + 5, VERSUS_ENREGISTRER)    # call enregistrer
    c += b'\xE8' + rel(a + len(c) + 5, TRANSITION_CAVE)       # call la caverne
    c += bytes.fromhex('4883C428')                            # add rsp, 0x28
    c += b'\xC3'                                              # ret
    if len(c) > VERSUS_CAVE_MAX:
        raise AssertionError('la caverne versus deborde : %d > %d'
                             % (len(c), VERSUS_CAVE_MAX))
    return c


def transition_dojo():
    """Le relais du maillon 7, dans la premiere moitie de la caverne.

    `0x18019C3D0` recoit ses arguments intacts (ecx = le type choisi par la
    page, edx = 0, r8b = 1) : c'est elle qui pose le type et demande le mode 6.
    Nous n'ajoutons que la session et le sous-etat.
    """
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    a = DOJO_CAVE
    c = bytes.fromhex('4883EC28')                             # sub rsp, 0x28
    c += b'\xE8' + rel(a + len(c) + 5, DOJO_TYPE)             # call type+mode 6
    c += b'\xE8' + rel(a + len(c) + 5, SESSION_LIRE)          # call session_lire
    c += bytes.fromhex('4885C0')                              # test rax, rax
    c += bytes.fromhex('7507')                                # jne +7
    c += bytes.fromhex('33C9')                                # xor ecx, ecx
    c += b'\xE8' + rel(a + len(c) + 5, SESSION_CREER)         # call session_creer
    c += b'\xB9' + struct.pack('<I', SOUS_ETAT_CS_TRAINING)   # mov ecx, 41
    c += b'\xE8' + rel(a + len(c) + 5, DEMANDER_SOUS_ETAT)    # call sous-etat
    c += bytes.fromhex('4883C428')                            # add rsp, 0x28
    c += b'\xC3'                                              # ret
    if len(c) > DOJO_CAVE_MAX:
        raise AssertionError('la caverne dojo deborde : %d > %d'
                             % (len(c), DOJO_CAVE_MAX))
    return c


def transition_sortie():
    """Le relais du maillon 8 : `Input_isOn(15)`, la touche de sortie.

    Meme idiome que `0x180243ED0` : l'objet d'entrees est en `[0x180C3B6F8]`,
    sa vtable est son premier champ, et `Input_isOn` en est le creneau `+0x158`.
    """
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    a = SORTIE_CAVE
    c = bytes.fromhex('4883EC28')                             # sub rsp, 0x28
    c += bytes.fromhex('488B0D') + rel(a + len(c) + 7, ENTREES_OBJET)
    c += bytes.fromhex('488B01')                              # mov rax, [rcx]
    c += b'\xBA' + struct.pack('<I', SORTIE_CODE)             # mov edx, 15
    c += bytes.fromhex('FF90') + struct.pack('<I', ENTREES_CRENEAU)
    c += bytes.fromhex('4883C428')                            # add rsp, 0x28
    c += b'\xC3'                                              # ret
    if len(c) > SORTIE_CAVE_MAX:
        raise AssertionError('la caverne de sortie deborde : %d > %d'
                             % (len(c), SORTIE_CAVE_MAX))
    return c


def sousmenu_hook():
    """La garde appelle « la scene existe-t-elle ? » au lieu de « joue-t-elle ? ».

    Aucune caverne : c'est un predicat du moteur, deja utilise sur le MEME
    objet deux cents octets plus loin (`0x1801DD01A`).
    """
    return (bytes.fromhex('e8')
            + struct.pack('<i', SOUSMENU_PREDICAT - (SOUSMENU_GARDE + 5)))


# ---------------------------------------------------------------------------
# `--legende-sousmenu` -- la legende du bas ne se superpose plus.
#
# Constat de Frederic : � le texte descriptif du bandeau du bas superpose les
# textes du menu principal en arriere plan et ceux du sous menu en cours �.
#
# CE N'EST PAS NOTRE FAIT. Mesure du 2026-09-06 : un build TEMOIN sans
# `--sousmenu` montre exactement la meme superposition. C'est natif a ce build.
#
# La legende n'est pas un bandeau partage : c'est un CHAMP DE CHAQUE PAGE.
# Trois poseurs de deux instructions, tous sur `this` :
#
#     0x1801BE880(page, id)      -> page+0x21C = id        ligne 1
#     0x1801BE800(page, id)      -> page+0x220 = id        ligne 2
#     0x1801BE8B0(page, chaine)  -> page+0x21C = 0x5A0C
#                                   page+0xC0  = chaine
#
# et la passe de resolution les relit :
#
#     0x1801BBD01  mov  ecx, [rbx+0x21C]
#     0x1801BBD07  cmp  ecx, 0x5A0C          ; la BORNE de la table de libelles
#     0x1801BBD0D  je   +0xC                 ; egal -> ne pas re-resoudre
#     0x1801BBD0F  call 0x1801EFD10          ; sinon resoudre
#     0x1801BBD14  mov  [rbx+0xC0], rax      ; ligne 1 -> +0xC0  (ligne 2 -> +0x198)
#
# `0x5A0C` (23052) n'est donc PAS un � vide � : c'est � la chaine est deja en
# +0xC0, ne la refais pas �. Le poser seul figerait le texte au lieu de
# l'effacer.
#
# PREMIER ESSAI, ET IL ETAIT FAUX. J'ai d'abord ecrit l'IDENTIFIANT : la table
# ne contient aucune chaine vide (verifie sur les 23052 entrees) mais vingt-cinq
# entrees valent une seule espace, dont `0x5780`. Poser `[page+0x21C] = 0x5780`
# n'a RIEN change a l'ecran.
#
# La sonde `tools/pister_legende.py` dit pourquoi, et c'est net :
#
#     caverne legende    947 passages     <- notre greffe tourne bien
#     CAVERNE atteinte : page=0x20CD3CD4F00  [+0x21C]=0x62    (1er passage)
#     CAVERNE atteinte : page=0x20CD3CD4F00  [+0x21C]=0x5780  (les suivants)
#
#     porteurs de legende vus dans la resolution :
#       objet 0x20CD3CD5858   717 passages   ligne1=0x5A0C
#       objet 0x20CD3CD5558   232 passages   ligne1=0x5A0C
#       objet 0x20CD3CD4F00    93 passages   ligne1=0x62      <- le menu principal
#
# L'objet est le BON et l'ecriture PREND. Mais la passe de resolution ne visite
# plus cette page une fois le sous-menu ouvert : 93 passages, tous d'avant.
# Le texte dessine vient donc de `+0xC0`, DEJA RESOLU -- reecrire l'identifiant
# ne peut plus rien.
#
# C'est donc le POINTEUR DE CHAINE qu'il faut vider, et lui seul. On le fait
# pointer sur les huit octets nuls de `0x180347568` (chaine vide deja employee
# par le moteur, verifiee). On ne touche PAS a `+0x21C` : il garde son `0x62`,
# et quand le sous-menu se ferme la resolution reprend, relit l'identifiant et
# repose la chaine. Rien a defaire.
#
# Le geste se greffe sur le site que `--sousmenu` occupe deja -- le seul
# endroit qui sait qu'un sous-menu est ouvert. A `0x1801DC649`, `rdi` est la
# page du menu principal (`0x1801DC638 : mov rdi, rcx`, confirme par la sonde)
# et le site n'est atteint QUE si `[rdi+0x650] != 0`. Aucune garde de plus.
#
#     lea  rax, [rip + d]        ; -> 0x180347568, la chaine vide
#     mov  [rdi+0xC0], rax       ; la ligne 1 de la legende devient vide
#     jmp  0x180244F90           ; puis le predicat de --sousmenu
#
# Le saut terminal rend la main a `0x1801DC64E` : la pile est celle qu'un appel
# direct au predicat aurait produite, et son resultat reste dans `al`.
#
# LA PLACE, et une COLLISION corrigee le 2026-09-06. La caverne etait posee
# dans les octets morts de � Credits � (0x1801A71D8). C'etait FAUX : cette
# caverne appartient deja a `--sp-lancer`, qui y loge le lancement de License
# Challenge (le site 0x1801DDE49 y saute). Les deux options sont dans
# `console.cmd`, la legende est appliquee en dernier, et elle ecrasait le
# lancement -- verifie sur la DLL patchee, ou 0x1801DDE49 et 0x1801DC649
# appelaient tous deux 0x1801A71D8, qui ne contenait plus que la legende.
# License Challenge etait donc casse depuis l'ajout de `--legende-sousmenu`.
#
# Le controle ne pouvait pas l'attraper : il compare les octets attendus a
# `.origine`, jamais au fichier en cours d'ecriture. Deux options peuvent donc
# se disputer une caverne sans qu'aucune ne proteste. Un refus croise existait
# pour `--sp-mode` ; il manquait pour `--sp-lancer`.
#
# La caverne est donc deplacee dans un BOURRAGE D'ALIGNEMENT `int3`, comme
# `--options-tips` : `0x1802758DB`, 21 octets, verifie hors de toute entree de
# `.pdata` et suivi d'une frontiere a 16. Ce faisant, la legende ne depend plus
# ni de `--options-sans-howto` ni de l'absence de `--sp-mode`.
#
# CE QU'IL NE FAUT PAS � CORRIGER �. Le TITRE se superpose lui aussi : � MAIN
# MENU � transparait sous � SINGLE PLAYER �, par la scene d'en-tete
# (`[page+0x240]`, garde `0x1801E0DA5`). Frederic a tranche le 2026-09-06 :
# **c'est l'affichage normal**. Ne pas y toucher.
LEGENDE_SITE = 0x1801DC649                  # le meme site que --sousmenu
LEGENDE_TETE = bytes.fromhex('e852880600')  # call 0x180244EA0, tel qu'en origine
LEGENDE_CHAINE_VIDE = 0x180347568           # huit octets nuls, verifies
LEGENDE_CAVE = 0x1802758DB                  # bourrage int3, hors .pdata
LEGENDE_CAVE_MAX = 21
LEGENDE_CAVE_TETE = b'\xCC' * 19            # on n'ecrit que ce qu'on occupe


def legende_cave(a):
    """Vide la ligne 1 de la legende, puis saute dans le predicat. Dix-neuf octets."""
    c = bytes.fromhex('488d05')
    c += struct.pack('<i', LEGENDE_CHAINE_VIDE - (a + 7))   # lea rax, [rip+d]
    c += bytes.fromhex('488987c0000000')                    # mov [rdi+0xC0], rax
    c += b'\xE9' + struct.pack('<i', SOUSMENU_PREDICAT - (a + len(c) + 5))
    if len(c) > LEGENDE_CAVE_MAX:
        raise AssertionError('la caverne de legende deborde : %d > %d octets'
                             % (len(c), LEGENDE_CAVE_MAX))
    return c


def transition_dojo_hook():
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    return b'\xE8' + rel(DOJO_HOOK + 5, DOJO_CAVE)


def transition_versus_hook():
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    return b'\xE8' + rel(VERSUS_HOOK + 5, VERSUS_CAVE)


def transition_retour_menu():
    """Les 17 octets du maillon 4 : demander le mode MENU au lieu du titre."""
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    a = RETOUR_MENU_HOOK
    c = b'\xB9' + struct.pack('<I', MODE_MENU)               # mov ecx, 4
    c += b'\xE8' + rel(a + len(c) + 5, DEMANDER_MODE)        # call demander_mode
    reste = (RETOUR_MENU_FIN - RETOUR_MENU_HOOK) - len(c)
    if reste < 0:
        raise AssertionError('le maillon 4 deborde de %d octets' % -reste)
    return c + b'\x90' * reste


def transition_vs():
    """Les 10 octets du maillon 2 : demander VS au lieu du mode MENU."""
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    a = TRANSITION_VS_HOOK
    c = b'\xB9' + struct.pack('<I', SOUS_ETAT_VS)            # mov ecx, 19
    c += b'\xE8' + rel(a + len(c) + 5, DEMANDER_SOUS_ETAT)   # call demander_sous_etat
    assert len(c) == len(TRANSITION_VS_TETE)
    return c


def image(chemin):
    from pe_disasm import Image
    return Image(chemin)


def offset(chemin, va):
    for s in image(chemin).secs:
        if s['va'] <= va < s['va'] + max(s.get('vsize', 0), s['rsize']):
            return s['off'] + (va - s['va'])
    return None


# ---------------------------------------------------------------------------
# UNE SECTION DE PLUS, quand les cavernes ne suffisent plus
#
# Les bourrages `int3` rendent des plages de 20 octets au mieux, et il y en a
# quatre. Un detour qui doit interroger une entree, faire tourner un index et
# rafraichir l'ecran fait 76 octets : le chainer sur cinq cavernes serait
# illisible et fragile.
#
# Or le fichier a de la place aux deux endroits qu'il faut :
#
#   . l'en-tete : la table des sections finit en 0x348 et `SizeOfHeaders` vaut
#     0x400 -- **184 octets libres**, soit quatre en-tetes de section de plus ;
#   . la fin : le fichier s'arrete exactement ou finit `.reloc`
#     (6 965 248 octets), et cette taille est deja alignee sur `FileAlignment`
#     (0x200). On peut donc ajouter des donnees sans rien deplacer.
#
# On ajoute donc une section `.greffe`, executable, apres `.reloc`. Aucun
# decalage : les offsets de tout le reste du fichier ne bougent pas, et les
# correctifs deja ecrits restent valides.
#
# Le code qu'on y met n'utilise que de l'adressage RELATIF (`jmp`, `call`,
# `mov rcx, [rip+d]`) : il survit donc a un rebasage, comme les cavernes.
GREFFE_NOM = b'.greffe\x00'
GREFFE_TAILLE = 0x3000   # le code tient dans 0x600 ; le reste est la
                         # table des anneaux (VAR_FIN)
if VARIANTES_MAX_VARIANTES > 8:
    # seize variantes par anneau (voir plus haut), et depuis le 2026-09-11 les
    # stubs des taches de generation : YUKA a elle seule porte 0x6D0 octets
    # par decor (sa table de 432 objets). GRE_GEN commence a 0x35C0.
    GREFFE_TAILLE = 0x5000
# CODE | EXECUTE | READ | WRITE : la greffe garde aussi une VARIABLE (le numero
# de variante courant). Sans le droit d'ecriture, le premier `mov` dedans
# fauterait.
GREFFE_CARAC = 0xE0000020


def ajouter_greffe(nom):
    """Ajoute (ou retrouve) la section `.greffe`. Rend (va, offset fichier)."""
    chemin = os.path.join(JEU, nom)
    with open(chemin, 'r+b') as fp:
        d = bytearray(fp.read(0x400))
        e_lfanew = struct.unpack_from('<I', d, 0x3C)[0]
        n_sec = struct.unpack_from('<H', d, e_lfanew + 6)[0]
        taille_opt = struct.unpack_from('<H', d, e_lfanew + 20)[0]
        opt = e_lfanew + 24
        align_sec = struct.unpack_from('<I', d, opt + 32)[0]
        align_fic = struct.unpack_from('<I', d, opt + 36)[0]
        table = opt + taille_opt

        for i in range(n_sec):                       # deja greffee ?
            h = table + i * 40
            if bytes(d[h:h + 8]) == GREFFE_NOM:
                return (struct.unpack_from('<I', d, h + 12)[0]
                        + struct.unpack_from('<Q', d, opt + 24)[0],
                        struct.unpack_from('<I', d, h + 20)[0])

        h_neuf = table + n_sec * 40
        if h_neuf + 40 > struct.unpack_from('<I', d, opt + 60)[0]:
            raise AssertionError('pas de place pour un en-tete de section : '
                                 'la table finit en 0x%X, SizeOfHeaders vaut '
                                 '0x%X' % (h_neuf + 40,
                                           struct.unpack_from('<I', d,
                                                              opt + 60)[0]))
        dernier = table + (n_sec - 1) * 40
        va_prec = struct.unpack_from('<I', d, dernier + 12)[0]
        vsize_prec = struct.unpack_from('<I', d, dernier + 8)[0]
        va = (va_prec + vsize_prec + align_sec - 1) & ~(align_sec - 1)

        fp.seek(0, 2)
        off = fp.tell()
        if off % align_fic:
            fp.write(b'\x00' * (align_fic - off % align_fic))
            off = fp.tell()
        fp.write(b'\x00' * GREFFE_TAILLE)

        struct.pack_into('<8s', d, h_neuf, GREFFE_NOM)
        struct.pack_into('<I', d, h_neuf + 8, GREFFE_TAILLE)     # VirtualSize
        struct.pack_into('<I', d, h_neuf + 12, va)               # VirtualAddr
        struct.pack_into('<I', d, h_neuf + 16, GREFFE_TAILLE)    # SizeOfRaw
        struct.pack_into('<I', d, h_neuf + 20, off)              # PtrToRaw
        struct.pack_into('<I', d, h_neuf + 36, GREFFE_CARAC)
        struct.pack_into('<H', d, e_lfanew + 6, n_sec + 1)
        taille_image = (va + GREFFE_TAILLE + align_sec - 1) & ~(align_sec - 1)
        struct.pack_into('<I', d, opt + 56, taille_image)        # SizeOfImage
        fp.seek(0)
        fp.write(bytes(d))
        base = struct.unpack_from('<Q', d, opt + 24)[0]
        return base + va, off


def decors_table(argv, orig, faits):
    """Deplace les deux tables dans `.decors`, avec leurs relocations.

    Rend `(code_retour, [VA a reloger])`. Le code retour non nul arrete le
    patch ; la liste est donnee a `pe_sections.reconstruire_relocations`, qui
    doit etre appelee EN DERNIER, quand toutes les sections sont posees.
    """
    import pe_sections

    # Le compte est FACULTATIF, et on ne consomme le mot suivant que s il est
    # un nombre. `verifier_lanceurs.py` rejoue la ligne de patch d un `.cmd`
    # sans toujours retirer la redirection `>nul` : consommer aveuglement le
    # mot suivant faisait echouer le controle sur un lanceur pourtant sain.
    i = argv.index('--decors-table') + 1
    n = DECORS_TABLE_N
    if i < len(argv):
        mot = argv[i]
        if mot.isdigit() or (mot.lower().startswith('0x')
                             and mot[2:].isalnum()):
            n = int(mot, 0)
    if n < DECORS_TABLE_N:
        print('REFUS : %d decors, c est MOINS que les %d du jeu. On agrandit, '
              'on ne tronque pas.' % (n, DECORS_TABLE_N))
        return 1, []

    # LE LOT DES DECORS AJOUTES. Un decor ajoute clone SON PROPRE MODELE -- le
    # decor de Final Showdown correspondant -- et non `djo` : le descripteur
    # porte la musique, la configuration de l'anneau (+0xB8/+0xC0), l'aire et
    # les proprietes de rendu, et l'entree de mur comme la liste de taches
    # d'effet sont elles aussi indexees par le decor.
    #
    # `lot` = [(indice modele, code, indice neuf, objset, nom auth_3d), ...]
    lot = []
    if '--decors-5r' in argv:
        import variantes_5r
        fautes = variantes_5r.controler()
        if fautes:
            print('REFUS : la table de variantes_5r.py a %d faute(s) :'
                  % len(fautes))
            for x in fautes:
                print('   . %s' % x)
            return 2, []
        for modele, code, indice, objset in variantes_5r.DECORS_5R:
            if modele not in DECOR_NOMS:
                print('REFUS : « %s » n est pas un decor du jeu.' % modele)
                return 2, []
            lot.append((DECOR_NOMS.index(modele), code, indice, objset,
                        'STG%s' % code.upper()))
    elif '--decor-neuf' in argv:
        code = argv[argv.index('--decor-neuf') + 1]
        if '--objset' not in argv:
            print('REFUS : --decor-neuf demande --objset <identifiant>. '
                  '`py -3 tools/obj_db.py --libres` donne les plages libres.')
            return 2, []
        lot.append((DECORS_MODELE, code, DECORS_PREMIER_NEUF,
                    int(argv[argv.index('--objset') + 1], 0),
                    argv[argv.index('--auth3d') + 1] if '--auth3d' in argv
                    else 'STG%s' % code.upper()))
    # LE VF5 D'ORIGINE (ver.B), A LA SUITE. Ses entrees ne sont pas des clones
    # purs de leur modele : leurs cinq objets, leurs reflets d'objectif et
    # leurs noms viennent de ver.B -- voir `variantes_vf5.py`. `speciaux` les
    # porte, par indice, et chaque etape du clonage le consulte.
    speciaux = {}
    # VF5 R AUSSI (2026-09-11). Frederic : « applique a VF5 R ses propres
    # listes, rien ne doit venir de FS ». Ses entrees deviennent « speciales »
    # comme celles de ver.B : ce que le decor CONTIENT est relu dans SON
    # binaire (`generation.py`).
    if '--decors-5r' in argv:
        import variantes_5r
        for e in variantes_5r.entrees():
            speciaux[e['indice']] = e
    if '--decors-vf5' in argv:
        import variantes_vf5
        fautes = variantes_vf5.controler()
        if fautes:
            print('REFUS : la table de variantes_vf5.py a %d faute(s) :'
                  % len(fautes))
            for x in fautes:
                print('   . %s' % x)
            return 2, []
        for e in variantes_vf5.entrees():
            if e['modele'] not in DECOR_NOMS:
                print('REFUS : « %s » n est pas un decor du jeu.' % e['modele'])
                return 2, []
            lot.append((DECOR_NOMS.index(e['modele']), e['code'], e['indice'],
                        e['objset'], e['a3d']))
            speciaux[e['indice']] = e
    # LES QUATRE DURAL DE VF5 R (indices 82-85), apres ver.B : voir
    # variantes_5r.DURAL_5R. Leur scene `STGD<n>5` n'existe pas -- comme celle
    # de leurs modeles, que R et FS declarent vides.
    if '--decors-5r-dural' in argv:
        import variantes_5r
        codes_dr = set(c for _, c, _, _ in variantes_5r.DURAL_5R)
        for e in variantes_5r.entrees(dural=True):
            if e['code'] not in codes_dr:
                continue
            lot.append((DECOR_NOMS.index(e['modele']), e['code'], e['indice'],
                        e['objset'], e['a3d']))
            speciaux[e['indice']] = e

    def _textes(code, nom_a3d, indice):
        """Les trois chaines du descripteur : auth_3d, effets, collision."""
        e = speciaux.get(indice)
        if e is None:
            return [nom_a3d, 'EFF%s' % nom_a3d,
                    'rom/STG%s_COLI.000.bin' % code.upper()]
        return [e['a3d'], 'EFFSTG%s' % e['eff'].upper(),
                'rom/STG%s_COLI.000.bin' % e['coli'].upper()]

    def _eff(indice, code):
        """Le code de la categorie d'effets : les quatre Dural de ver.B
        partagent `EFFSTGDRB`, comme ver.B partage `EFFSTGDUR`."""
        return speciaux[indice]['eff'] if indice in speciaux else code
    for _, code, indice, _, _ in lot:
        if len(code) != 3:
            print('REFUS : le code d un decor fait TROIS lettres (« %s » en a '
                  '%d). Les archives se renomment en place, et `djo` fait '
                  'trois.' % (code, len(code)))
            return 2, []
        if code in DECOR_NOMS:
            print('REFUS : le code « %s » est deja celui d un decor du jeu.'
                  % code)
            return 2, []
        if indice == DECORS_INDICE_ALEA:
            print('REFUS : l indice %d est RESERVE -- c est le code « decor '
                  'aleatoire », teste par egalite a sept endroits.'
                  % DECORS_INDICE_ALEA)
            return 2, []
        if indice >= n:
            print('REFUS : le lot pose un decor a l indice %d et la table n en '
                  'a que %d. Passez --decors-table %d ou plus.'
                  % (indice, n, indice + 1))
            return 2, []
    # de quel decor l'entree neuve `i` est-elle le clone ?
    modeles = dict((indice, m) for m, _, indice, _, _ in lot)

    def modele_de(i):
        return modeles.get(i, DECORS_MODELE)

    chemin = os.path.join(JEU, DLL)
    # 1. LA SOURCE, et ses relocations. On les lit dans `.origine` : c'est la
    #    seule image dont on sait qu'aucun correctif ne l'a touchee.
    import pefile
    pe = pefile.PE(orig[DLL], fast_load=True)
    pe.parse_data_directories(directories=[
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_BASERELOC']])
    relogees = set()
    for b in pe.DIRECTORY_ENTRY_BASERELOC:
        for e in b.entries:
            if e.type == 10:
                relogees.add(DECORS_BASE + e.rva)
    desc = pe.get_data(DECORS_TABLE_VA - DECORS_BASE,
                       DECORS_TABLE_N * DECORS_TABLE_PAS)
    codes = pe.get_data(DECORS_CODES_VA - DECORS_BASE,
                        DECORS_TABLE_N * DECORS_CODES_PAS)

    # 1 bis. LES DEUX TABLES D'EFFETS ET LA CHARGE DU MUR. On les lit AVANT de
    #        dimensionner la section, parce que les trois blocs du mur y sont
    #        recopies : leur taille entre dans le calcul.
    src_a3d = pe.get_data(EFFETS_A3D_VA - DECORS_BASE,
                          (EFFETS_A3D_N + 1) * EFFETS_A3D_PAS)
    src_mur = pe.get_data(EFFETS_MUR_VA - DECORS_BASE,
                          (EFFETS_MUR_N + 1) * EFFETS_MUR_PAS)

    def _rang(src, nb, pas, indice):
        """Le rang de l'entree du decor `indice`, ou None. Ce sont des LISTES
        D'ASSOCIATION : tous les decors n'y sont pas."""
        for r in range(nb):
            if struct.unpack_from('<i', src, r * pas)[0] == indice:
                return r
        return None

    # Chaque decor du lot a SON modele : on releve pour chacun son rang dans
    # les deux tables d'effets, et la charge de son mur. Un modele sans entree
    # n'est pas une faute -- neuf decors sur 41 n'ont pas de mur.
    r_a3d, r_mur, charges = {}, {}, {}
    for m in sorted(set([e[0] for e in lot] + [DECORS_MODELE])):
        r_a3d[m] = _rang(src_a3d, EFFETS_A3D_N, EFFETS_A3D_PAS, m)
        r_mur[m] = _rang(src_mur, EFFETS_MUR_N, EFFETS_MUR_PAS, m)
        if r_mur[m] is None:
            continue
        e = src_mur[r_mur[m] * EFFETS_MUR_PAS:(r_mur[m] + 1) * EFFETS_MUR_PAS]
        charges[m] = mur_charge_modele(pe, e)
        if charges[m] is None:
            print('   (c est le decor modele %d, « %s »)'
                  % (m, DECOR_NOMS[m]))
            return 2, []
    if r_mur[DECORS_MODELE] is None:
        print('REFUS : le decor modele %d n a pas d entree de mur : le clone '
              'de remplissage n aurait rien a porter.' % DECORS_MODELE)
        return 2, []
    modele_mur = src_mur[r_mur[DECORS_MODELE] * EFFETS_MUR_PAS:
                         (r_mur[DECORS_MODELE] + 1) * EFFETS_MUR_PAS]
    charge_mur = charges[DECORS_MODELE]

    # --- CE QUE LE DECOR CONTIENT VIENT DE SA GENERATION (2026-09-11) -----
    # Frederic : « rien ne doit venir de FS ». Pour chaque entree speciale
    # (VF5 R et ver.B), les objets, les murs, les taches, les animations et
    # les dossiers d'effet sont RELUS dans le binaire de sa generation
    # (`generation.py`), et ses identifiants rendus a NOTRE decor par un
    # `Traducteur` : uid par NOM, textures par NOM (ver.B) ou telles quelles
    # (R, qui numerote comme FS), objets par objset substitue.
    #
    # LE MUR est celui de la generation, converti au format de FS -- un
    # morceau fait 0x28 chez R et ver.B, 0x2C chez FS (FS a insere un ENTIER a
    # +4 : 0 sur 293 morceaux, 1 sur 15 ; on met 0). Un objet absent de
    # l'archive posee annule le mur : on ne pose pas un mur a moitie.
    trad_verb, mur_verb, charge_verb, trads = {}, {}, {}, {}
    if speciaux:
        import generation as _gen
        for i_v, e_v in sorted(speciaux.items()):
            g_v = _gen.generation(e_v['gen'])
            try:
                tr = Traducteur(e_v, g_v)
                w_v = g_v.mur(e_v['cle'])
            except (_gen.Refus, ValueError) as x:
                print('REFUS : %s' % x)
                return 2, []
            trads[i_v] = tr
            if w_v is None:
                mur_verb[i_v] = False
                continue
            objs_v = [x for x, _ in w_v['pieces']]
            objs_v += [x for x, _ in (w_v['p20'] or [])]
            objs_v += [q[0] for q in w_v['paires']]
            objs_v += [q[1] for q in w_v['paires'] if q[1] != 0xFFFFFFFF]
            mauvais_v = ['%d:%d' % (x >> 16, x & 0xFFFF) for x in objs_v
                         if tr.obj(x) is None]
            if mauvais_v:
                mur_verb[i_v] = False
                faits.append('%s : %s n aura PAS de mur -- sa table nomme %d '
                             'objet(s) absents de l archive posee (%s).'
                             % (g_v.nom, e_v['code'], len(mauvais_v),
                                ' '.join(mauvais_v[:3])))
                continue

            def _morceaux_fs(lst, _tr=tr):
                """{objet, 9 flottants} -> {objet, 0, 9 flottants}."""
                b = bytearray()
                for obj_v, flottants in lst:
                    b += struct.pack('<Ii', _tr.obj(obj_v), 0) + flottants
                b += struct.pack('<i', -1) + bytes(EFFETS_MUR_PIECE_PAS - 4)
                return bytes(b)
            charge_verb[i_v] = dict(
                pieces=_morceaux_fs(w_v['pieces']),
                p20=_morceaux_fs(w_v['p20']) if w_v['p20'] else None,
                uids=w_v['uids'], paires=w_v['paires'],
                n_pieces=len(w_v['pieces']),
                u28=w_v['u28'], o30=w_v['o30'], u38=w_v['u38'])
            mur_verb[i_v] = True

    # 2. LA SECTION. `.greffe` doit avoir ete posee AVANT si elle est demandee
    #    -- elle est documentee a 0x180EA1000 -- donc ce correctif passe apres
    #    tous les autres, a la fin de main().
    grille = '--grille-table' in argv
    neufs = n - DECORS_TABLE_N
    taille_desc = n * DECORS_TABLE_PAS
    taille_codes = n * DECORS_CODES_PAS
    off_codes = (taille_desc + 0xF) & ~0xF
    off_grille = (off_codes + taille_codes + 0xF) & ~0xF
    taille_grille = GRILLE_TABLE_N * GRILLE_TABLE_PAS if grille else 0
    off_objsets = (off_grille + taille_grille + 0xF) & ~0xF
    taille_objsets = n * OBJSETS_TABLE_PAS
    off_eff_a3d = (off_objsets + taille_objsets + 0xF) & ~0xF
    taille_eff_a3d = (EFFETS_A3D_N + neufs + 1) * EFFETS_A3D_PAS
    off_eff_mur = (off_eff_a3d + taille_eff_a3d + 0xF) & ~0xF
    taille_eff_mur = (EFFETS_MUR_N + neufs + 1) * EFFETS_MUR_PAS
    off_eff_uids = (off_eff_mur + taille_eff_mur + 0xF) & ~0xF
    taille_eff_uids = neufs * EFFETS_UIDS_MAX * 4
    # LA CHARGE DU MUR, UN JEU PAR DECOR AJOUTE QUI EN A UN. Les entrees
    # neuves de remplissage (`x00`…) gardent les pointeurs du modele : elles
    # n'ont ni objset ni uid a elles.
    off_mur = {}
    o = (off_eff_uids + taille_eff_uids + 0xF) & ~0xF
    for m, _, indice, _, _ in lot:
        if indice in charge_verb:
            # le mur de ver.B, converti : ses blocs a lui, tailles connues
            cv = charge_verb[indice]
            p = o
            o = (p + len(cv['pieces']) + 0xF) & ~0xF
            u = o
            o = (u + (len(cv['uids']) + 1) * 4 + 0xF) & ~0xF
            q = o
            o = (q + (len(cv['paires']) + 1) * EFFETS_MUR_PAIRE_PAS
                 + 0xF) & ~0xF
            sup = {}
            if cv['p20'] is not None:
                sup['p20'] = o
                o = (o + len(cv['p20']) + 0xF) & ~0xF
            # les trois champs de VF5 R : grillage anime, objets cassables
            if cv['u28'] is not None:
                sup['u28'] = o
                o = (o + 8 + 0xF) & ~0xF
            if cv['o30'] is not None:
                sup['o30'] = o
                o = (o + len(cv['o30']) * EFFETS_MUR_PAIRE_PAS + 0xF) & ~0xF
            if cv['u38'] is not None:
                sup['u38'] = o
                o = (o + len(cv['u38']) * 4 + 0xF) & ~0xF
            off_mur[indice] = (p, u, q, sup)
            continue
        if indice in speciaux:
            continue                  # ver.B sans mur : rien a reserver
        if charges.get(m) is None:
            continue
        c = charges[m]
        p = o
        o = (p + len(c['pieces']) + 0xF) & ~0xF
        u = q = 0
        if c['a_uids']:
            u = o
            o = (u + (len(c['uids']) + 1) * 4 + 0xF) & ~0xF
        if c['a_paires']:
            q = o
            o = (q + len(c['paires']) + 0xF) & ~0xF
        sup = {}
        for nom_bloc, (octets, _) in sorted(c['extra'].items()):
            sup[nom_bloc] = o
            o = (o + len(octets) + 0xF) & ~0xF
        off_mur[indice] = (p, u, q, sup)
    off_son = (o + 0xF) & ~0xF
    taille_son = (SON_TABLE_N + neufs + 1) * SON_TABLE_PAS
    off_down = (off_son + taille_son + 0xF) & ~0xF
    taille_down = n * 4
    off_move = (off_down + taille_down + 0xF) & ~0xF
    taille_move = n * 4
    off_snow = (off_move + taille_move + 0xF) & ~0xF
    taille_snow = (SNOW_TABLE_N + neufs + 1) * SNOW_TABLE_PAS
    off_ch = {}
    o_ch = (off_snow + taille_snow + 0xF) & ~0xF
    for _nom in sorted(CHAINES):
        _pas, _n = CHAINES[_nom][1], CHAINES[_nom][2]
        off_ch[_nom] = o_ch
        o_ch = (o_ch + (_n + neufs + 1) * _pas + 0xF) & ~0xF
    # RINGOUT_SPLASH : le tableau (sans terminateur : borne par sa fin), puis
    # les chaines de nos entrees
    off_ringout = o_ch
    o_ch = (o_ch + (RINGOUT_TABLE_N + neufs) * RINGOUT_TABLE_PAS + 0xF) & ~0xF
    off_ringout_ch = o_ch
    o_ch = (o_ch + neufs * RINGOUT_CHAINE_MAX + 0xF) & ~0xF
    off_chaines = o_ch
    # Chaque decor ajoute porte trois chaines : le nom auth_3d, celui des
    # effets, et le chemin de sa collision. Plus un code de quatre octets par
    # entree neuve.
    taille_chaines = neufs * 4                     # « xNN\0 »
    for _, code, indice_t, _, nom_a3d in lot:
        for t in _textes(code, nom_a3d, indice_t):
            taille_chaines += (len(t) + 8) & ~7
    besoin = (off_chaines + taille_chaines + 0xFFF) & ~0xFFF
    va, off = pe_sections.ajouter_section(chemin, DECORS_SECTION, besoin)

    # 3. LA COPIE, et les relocations qui vont avec. Une par pointeur de la
    #    source : on ne devine aucun decalage.
    contenu = bytearray(besoin)
    contenu[0:len(desc)] = desc
    contenu[off_codes:off_codes + len(codes)] = codes
    a_reloger = []
    # LES ENTREES NEUVES. Un clone complet de LEUR modele, et un code a elles.
    def _reloc_desc(m):
        return [o for o in range(0, DECORS_TABLE_PAS, 8)
                if DECORS_TABLE_VA + m * DECORS_TABLE_PAS + o in relogees]

    for k in range(neufs):
        i = DECORS_TABLE_N + k
        m = modele_de(i)
        contenu[i * DECORS_TABLE_PAS:(i + 1) * DECORS_TABLE_PAS] = \
            desc[m * DECORS_TABLE_PAS:(m + 1) * DECORS_TABLE_PAS]
        for o in _reloc_desc(m):
            a_reloger.append(va + i * DECORS_TABLE_PAS + o)
        code = (DECORS_CODE_NEUF % k).encode('ascii') + b'\x00'
        oc = off_chaines + k * 4
        contenu[oc:oc + len(code)] = code
        struct.pack_into('<Q', contenu, off_codes + i * DECORS_CODES_PAS,
                         va + oc)
        a_reloger.append(va + off_codes + i * DECORS_CODES_PAS)
    if grille:
        g = pe.get_data(GRILLE_TABLE_VA - DECORS_BASE, taille_grille)
        contenu[off_grille:off_grille + taille_grille] = g
        for k in range(0, taille_grille, 8):
            if GRILLE_TABLE_VA + k in relogees:
                a_reloger.append(va + off_grille + k)
    # LA TABLE DES OBJSETS EN PLUS -- ET DES TACHES D'EFFET. Que des entiers :
    # on REFUSE si l'origine y a la moindre relocation, plutot que de la
    # recopier sans elle. Voir le commentaire de OBJSETS_TABLE_VA : le +0x20
    # est la LISTE DES TACHES D'EFFET a creer pour ce decor, et c'est elle qui
    # fait exister `TaskEffectWall`.
    source_objsets = OBJSETS_TABLE_N * OBJSETS_TABLE_PAS
    for k in range(0, source_objsets, 8):
        if OBJSETS_TABLE_VA + k in relogees:
            print('REFUS : 0x%X porte une relocation a +0x%X. Cette table etait '
                  'reputee ne contenir que des entiers ; elle ne peut pas etre '
                  'copiee telle quelle.' % (OBJSETS_TABLE_VA, k))
            return 2, []
    codes_neufs_t = dict((indice, c) for _, c, indice, _, _ in lot)
    o = pe.get_data(OBJSETS_TABLE_VA - DECORS_BASE, source_objsets)
    contenu[off_objsets:off_objsets + source_objsets] = o
    # Les entrees neuves sont un CLONE COMPLET DE L'ENTREE DU MODELE, comme le
    # descripteur et comme l'entree de mur. Elles clonaient l'entree 0, qui ne
    # demande AUCUNE tache : le decor ajoute n'avait donc pas de
    # `TaskEffectWall`, et sa table de murs -- pourtant juste -- n'etait jamais
    # consultee. Pas de barrieres, et pas un message.
    def _taches(m):
        e = o[m * OBJSETS_TABLE_PAS:(m + 1) * OBJSETS_TABLE_PAS]
        t = list(struct.unpack_from('<16i', e, OBJSETS_TABLE_TACHES))
        if -1 not in t:
            print('REFUS : la liste de taches d effet du decor %d (0x%X + '
                  '%d*0x%X + 0x%X) n a pas de terminateur -1 : ce n est pas le '
                  'tableau attendu.'
                  % (m, OBJSETS_TABLE_VA, m, OBJSETS_TABLE_PAS,
                     OBJSETS_TABLE_TACHES))
            return None
        return t[:t.index(-1)]

    if _taches(DECORS_MODELE) is None:
        return 2, []
    dits = []
    taches_v = None                     # les taches de ver.B, lues a la demande
    for k in range(neufs):
        i = DECORS_TABLE_N + k
        m = modele_de(i)
        t = _taches(m)
        if t is None:
            return 2, []
        d = off_objsets + i * OBJSETS_TABLE_PAS
        contenu[d:d + OBJSETS_TABLE_PAS] = \
            o[m * OBJSETS_TABLE_PAS:(m + 1) * OBJSETS_TABLE_PAS]
        if i in speciaux:
            # ver.B DEMANDE SES PROPRES TACHES, pas celles du modele FS : sa
            # table (meme forme que celle-ci) est relue dans son ELF. Celle de
            # VF5 R, relue pareil, donne `hai` = WALL seul -- sans THUNDER,
            # ce que Frederic a constate a l'ecran sur hi5. Une generation a
            # SES effets. Ce qu'on ne sait pas servir (pas de dossier chez le
            # modele) tombe plus bas, comme pour VF5 R.
            import generation as _gen_t
            t = _gen_t.generation(speciaux[i]['gen']).taches(
                speciaux[i]['cle'])
        if i in modeles:
            # ON NE DEMANDE QUE CE QU'ON SAIT SERVIR. Voir EFFETS_SERVIS.
            gardees = [v for v in t if v in EFFETS_SERVIS]
            if (i in speciaux and not mur_verb.get(i)) or \
                    (i not in speciaux and r_mur.get(m) is None):
                gardees = [v for v in gardees if v != 2]
            # LES OBJSETS EN PLUS (+0x00) : le ciel des Dural de ver.B. C'est
            # le `+0x0C` du descripteur de ver.B, et FS a le meme mecanisme,
            # complet et jamais servi : `0x18006F620` demande chaque objset de
            # la liste (`FUN_1800F9C60`), la porte de l'etat 4 (`0x18006F380`,
            # etat 1) attend qu'il soit pret (`FUN_1800FB7E0`), et le
            # dechargement (`0x18006FA70`) le rend (`FUN_1800F86C0`).
            e_c = speciaux.get(i)
            if e_c is not None and e_c['ciel'] is not None:
                for j in range(8):
                    struct.pack_into('<i', contenu, d + j * 4,
                                     e_c['ciel'][1] if j == 0 else -1)
                faits.append('ver.B : l entree %d (%s) charge EN PLUS '
                             'l objset %d (stg%s, son ciel) -- liste +0x00 de '
                             '0x%X, demandee par 0x18006F620, attendue par '
                             '0x18006F380, rendue par 0x18006FA70.'
                             % (i, e_c['code'], e_c['ciel'][1],
                                e_c['ciel'][0], OBJSETS_TABLE_VA))
            # CE QUE CE VARIANT NE DOIT PAS AVOIR, sur constat a l'ecran.
            refus = EFFETS_RETIRES.get(codes_neufs_t.get(i), ())
            if refus:
                gardees = [v for v in gardees if v not in refus]
            retirees = [v for v in t if v not in gardees]
            for j in range(16):
                struct.pack_into('<i', contenu,
                                 d + OBJSETS_TABLE_TACHES + j * 4,
                                 gardees[j] if j < len(gardees) else -1)
            if refus:
                faits.append('decor neuf : l entree %d (%s) ne demande PAS %s '
                             '-- ce variant ne doit pas l avoir, constate a '
                             'l ecran. Le decor d origine, lui, la garde '
                             'intacte. Voir EFFETS_RETIRES.'
                             % (i, codes_neufs_t.get(i),
                                ' '.join(EFFETS_NOMS[v] for v in refus)))
            if retirees:
                faits.append('decor neuf : l entree %d ne demande PAS les '
                             'taches %s -- leur table indexee par le decor n a '
                             'pas d entree pour %d, et une tache creee sans '
                             'donnees plante a la mise a jour. Elle garde %s.'
                             % (i,
                                ' '.join(EFFETS_NOMS[v]
                                         if 0 <= v < len(EFFETS_NOMS) else '?'
                                         for v in retirees),
                                i,
                                ' '.join(EFFETS_NOMS[v] for v in gardees)
                                or '(aucune)'))
            t = gardees
        if i in modeles:
            dits.append('%d<-%s(%s)'
                        % (i, DECOR_NOMS[m],
                           ' '.join(EFFETS_NOMS[v] if 0 <= v < len(EFFETS_NOMS)
                                    else '?' for v in t) or 'aucune'))
    faits.append('decor neuf : les %d entrees neuves de la table 0x%X clonent '
                 'celle de LEUR modele, pas l entree 0. Son +0x%X est la LISTE '
                 'DES TACHES D EFFET a creer pour le decor -- lue par '
                 '0x18006F380, qui n instancie `TaskEffectWall` que si le '
                 'decor le demande. Un clone de l entree 0 n en demandait '
                 'aucune : la table des murs, pourtant juste, n etait jamais '
                 'consultee. %s'
                 % (neufs, OBJSETS_TABLE_VA, OBJSETS_TABLE_TACHES,
                    ' '.join(dits)))

    # --- LE SON D'AMBIANCE ---------------------------------------------------
    # Une entree neuve reprend le POINTEUR DE BLOC DU MODELE : meme lieu, meme
    # ambiance, et le `.csb` du modele est deja dans le `.par`.
    src_son = pe.get_data(SON_TABLE_VA - DECORS_BASE,
                          (SON_TABLE_N + 1) * SON_TABLE_PAS)
    n_son = SON_TABLE_N * SON_TABLE_PAS
    contenu[off_son:off_son + n_son] = src_son[:n_son]
    for kk in range(0, n_son, 8):
        if SON_TABLE_VA + kk in relogees:
            a_reloger.append(va + off_son + kk)
    blocs_son = {}
    for r in range(SON_TABLE_N):
        i_src = struct.unpack_from('<i', src_son, r * SON_TABLE_PAS)[0]
        blocs_son[i_src] = struct.unpack_from('<Q', src_son,
                                              r * SON_TABLE_PAS + 8)[0]
    son_ajoutes, son_dits = 0, []
    for m_s, code_s, indice_s, _, _ in lot:
        bloc = blocs_son.get(m_s)
        if not bloc:
            son_dits.append('%s : %s n a pas d ambiance propre'
                            % (code_s, DECOR_NOMS[m_s]))
            continue
        ds = off_son + (SON_TABLE_N + son_ajoutes) * SON_TABLE_PAS
        struct.pack_into('<i', contenu, ds, indice_s)
        struct.pack_into('<Q', contenu, ds + 8, bloc)
        a_reloger.append(va + ds + 8)
        son_ajoutes += 1
        son_dits.append('%s <- %s' % (code_s, DECOR_NOMS[m_s]))
    ds = off_son + (SON_TABLE_N + son_ajoutes) * SON_TABLE_PAS
    contenu[ds:ds + SON_TABLE_PAS] = src_son[n_son:n_son + SON_TABLE_PAS]
    if lot:
        faits.append('son d ambiance : la liste 0x%X demenage dans .decors '
                     '(+0x%X) et recoit %d entree(s) -- chacune reprend le bloc '
                     'du modele, donc son se_stage_*.csb et ses cris de choc '
                     'contre le mur. Sans elle, un decor ajoute prenait '
                     'l ambiance de `are`, la valeur par defaut de '
                     '0x1801903DC. %s'
                     % (SON_TABLE_VA, off_son, son_ajoutes,
                        ' '.join(son_dits)))

    # --- DOWN, MOVE ET SNOW --------------------------------------------------
    # DOWN et MOVE sont des TABLEAUX DENSES : ils n'ont pas de terminateur, et
    # `t[indice]` se lit sans aucune verification. Les etendre a `n` entrees
    # n'est donc pas un enrichissement, c'est une REPARATION : jusqu'ici tout
    # decor ajoute y lisait du texte de `.rdata` et le donnait a l'auth_3d
    # comme un numero d'uid. Ces deux taches sont toujours creees.
    src_down = pe.get_data(DOWN_TABLE_VA - DECORS_BASE, DECORS_TABLE_N * 4)
    src_move = pe.get_data(MOVE_TABLE_VA - DECORS_BASE, DECORS_TABLE_N * 4)
    contenu[off_down:off_down + len(src_down)] = src_down
    contenu[off_move:off_move + len(src_move)] = src_move
    # Les entrees neuves valent -1 par defaut : « ce decor n'a pas de poussiere
    # de chute ». C'est ce que le jeu ecrit lui-meme pour quinze de ses decors.
    for i in range(DECORS_TABLE_N, n):
        struct.pack_into('<i', contenu, off_down + i * 4, -1)
        struct.pack_into('<i', contenu, off_move + i * 4, -1)
    src_snow = pe.get_data(SNOW_TABLE_VA - DECORS_BASE,
                           (SNOW_TABLE_N + 1) * SNOW_TABLE_PAS)
    n_snow = SNOW_TABLE_N * SNOW_TABLE_PAS
    contenu[off_snow:off_snow + n_snow] = src_snow[:n_snow]
    snow_de = {}
    for r in range(SNOW_TABLE_N):
        snow_de[struct.unpack_from('<i', src_snow, r * SNOW_TABLE_PAS)[0]] = r
    # LES QUATRE CHAINES DEROULEES : on recopie leurs dossiers, et on note
    # quel decor porte lequel. THUNDER n'a pas de champ d'indice -- ses deux
    # indices sont des litteraux du code -- on l'ecrit dans son bourrage.
    src_ch, ch_de, ch_ajoutes = {}, {}, {}
    for nom_ch in sorted(CHAINES):
        va_ch, pas_ch, n_ch, decal_ch = CHAINES[nom_ch][:4]
        src_ch[nom_ch] = pe.get_data(va_ch - DECORS_BASE, n_ch * pas_ch)
        contenu[off_ch[nom_ch]:off_ch[nom_ch] + n_ch * pas_ch] = src_ch[nom_ch]
        ch_de[nom_ch] = {}
        for r in range(n_ch):
            if nom_ch in CHAINES_INDICES:
                i_r = CHAINES_INDICES[nom_ch][r]
                struct.pack_into('<i', contenu,
                                 off_ch[nom_ch] + r * pas_ch + decal_ch, i_r)
            else:
                i_r = struct.unpack_from('<i', src_ch[nom_ch],
                                         r * pas_ch + decal_ch)[0]
            ch_de[nom_ch][i_r] = r
        ch_ajoutes[nom_ch] = 0
    # RINGOUT_SPLASH : les quatre dossiers de FS, avec les relocations de
    # leurs pointeurs de chaine ; les notres suivent (voir RINGOUT_TABLE_VA).
    src_ro = pe.get_data(RINGOUT_TABLE_VA - DECORS_BASE,
                         RINGOUT_TABLE_N * RINGOUT_TABLE_PAS)
    contenu[off_ringout:off_ringout + len(src_ro)] = src_ro
    for k in range(0, len(src_ro), 8):
        if RINGOUT_TABLE_VA + k in relogees:
            a_reloger.append(va + off_ringout + k)
    ro_ajoutes = 0
    snow_ajoutes, dms_dits, servies, eau_table = 0, [], {}, []
    gen_tables = {}                     # GENERATION_TACHES : {nom: [(i, rec)]}
    cablages_x = {}                     # CABLAGES_APPELS & co : {nom: [(a, b)]}
    uids_fs_x = {}
    if speciaux:
        import a3d_db as _a3d_c
        for _k, _v in _a3d_c.charger(os.path.join(
                RACINE, 'extracted', 'auth_3d_db.bin')).uids().items():
            uids_fs_x.setdefault(_v.get('value', '').split()[-1], _k)
    for m_x, code_x, indice_x, objset_x, _ in lot:
        # LES DOSSIERS D'EFFET D'UNE ENTREE SPECIALE VIENNENT DE SA GENERATION
        # (2026-09-11) : neige, souffle, brume animee, eclaboussures, ondes,
        # tonnerre, anneau d'eau et poussiere de chute, relus dans son binaire
        # (`generation.py`) et traduits. On ne pose un dossier que si la
        # generation DEMANDE la tache pour ce decor ; une tache dont le dossier
        # manque (un uid, une texture, un objet absents) est retiree plus bas.
        if indice_x in speciaux:
            import generation as _gen_x
            e_x = speciaux[indice_x]
            g_x = _gen_x.generation(e_x['gen'])
            tr_x = trads[indice_x]
            cle_x = e_x['cle']
            veut_x = set(g_x.taches(cle_x))
            servies[indice_x] = set()
            dit = []
            try:
                v_down = g_x.down(cle_x)
            except _gen_x.Refus as x:
                print('REFUS : %s' % x)
                return 2, []
            if v_down is not None:
                n_down = tr_x.uid(v_down)
                if n_down is None:
                    dit.append('DOWN absent (%s)' % v_down.split()[-1])
                else:
                    struct.pack_into('<i', contenu, off_down + indice_x * 4,
                                     n_down)
                    dit.append('DOWN=%s' % v_down.split('_EFF_')[-1])
            # MOVE (`EFF_DASH`) n'existe pas chez R ni ver.B : -1, pose plus haut
            for nom_x, num_x in (('SNOW', 5),) + tuple(
                    (nch, CHAINES_TACHE[nch]) for nch in sorted(CHAINES)):
                if num_x not in veut_x:
                    continue
                try:
                    rec_x = g_x.dossiers(nom_x).get(cle_x)
                except _gen_x.Refus as x:
                    print('REFUS : %s' % x)
                    return 2, []
                if rec_x is None:
                    dit.append('%s : %s n a pas de dossier' % (nom_x, g_x.nom))
                    continue
                rec_x, manque_x = tr_x.dossier(nom_x, rec_x)
                if manque_x:
                    dit.append('%s retire (%s)' % (nom_x, ', '.join(manque_x)))
                    continue
                if nom_x == 'SNOW':
                    ds = off_snow + (SNOW_TABLE_N + snow_ajoutes) * SNOW_TABLE_PAS
                    contenu[ds:ds + SNOW_TABLE_PAS] = rec_x
                    struct.pack_into('<i', contenu, ds, indice_x)
                    snow_ajoutes += 1
                else:
                    _, pas_ch, n_ch, decal_ch = CHAINES[nom_x][:4]
                    dc = off_ch[nom_x] + (n_ch + ch_ajoutes[nom_x]) * pas_ch
                    contenu[dc:dc + pas_ch] = rec_x
                    struct.pack_into('<i', contenu, dc + decal_ch, indice_x)
                    ch_ajoutes[nom_x] += 1
                servies[indice_x].add(num_x)
                dit.append(nom_x)
            # L'ANNEAU D'EAU : l'objet que la generation dessine (le litteral
            # de SON code), rendu a notre objset.
            if 13 in veut_x:
                try:
                    o_eau, r_eau = g_x.objet_anneau_eau()
                except _gen_x.Refus as x:
                    print('REFUS : %s' % x)
                    return 2, []
                n_eau = tr_x.obj((o_eau << 16) | r_eau)
                if n_eau is None:
                    dit.append('WATER_RING : objet %d:%d absent'
                               % (o_eau, r_eau))
                else:
                    eau_table.append((indice_x, n_eau))
                    servies[indice_x].add(13)
                    dit.append('WATER_RING')
            # LES DOSSIERS A ADRESSE FIXE (FOG_RING, SNOW_RING, RAIN) ET LE
            # SCALAIRE DE WET_CLOTH : relus dans la generation, traduits, et
            # poses plus bas dans les tables des stubs (GENERATION_STUBS).
            for nom_x, num_x in GENERATION_TACHES:
                if num_x not in veut_x:
                    continue
                try:
                    rec_x = g_x.dossiers(nom_x).get(cle_x)
                except _gen_x.Refus as x:
                    print('REFUS : %s' % x)
                    return 2, []
                if rec_x is None:
                    dit.append('%s : %s n a pas de dossier' % (nom_x, g_x.nom))
                    continue
                rec_x, manque_x = tr_x.dossier(nom_x, rec_x)
                if manque_x:
                    dit.append('%s retire (%s%s)' % (
                        nom_x, ', '.join(manque_x[:4]),
                        ' ...' if len(manque_x) > 4 else ''))
                    continue
                if not _gen_x.CHAMPS[nom_x].get('sans_indice'):
                    rec_x = bytearray(rec_x)
                    struct.pack_into('<i', rec_x, 0, indice_x)
                    rec_x = bytes(rec_x)
                gen_tables.setdefault(nom_x, []).append((indice_x, rec_x))
                servies[indice_x].add(num_x)
                dit.append(nom_x if nom_x != 'WET_CLOTH' else
                           'WET_CLOTH=%.3g' % struct.unpack('<f', rec_x)[0])
            # RINGOUT_SPLASH : le dossier de la generation au format de FS,
            # uid traduits, sa CHAINE recopiee dans `.decors` (le texte de la
            # generation, pas celui de FS).
            if 12 in veut_x:
                try:
                    rec_x = g_x.dossiers('RINGOUT_SPLASH').get(cle_x)
                    texte_x = None if rec_x is None else g_x.chaine(
                        struct.unpack_from('<Q', rec_x, 0x10)[0])
                except _gen_x.Refus as x:
                    print('REFUS : %s' % x)
                    return 2, []
                if rec_x is None:
                    dit.append('RINGOUT_SPLASH : %s n a pas de dossier'
                               % g_x.nom)
                else:
                    rec_x, manque_x = tr_x.dossier('RINGOUT_SPLASH', rec_x)
                    brut_x = texte_x.encode('latin-1') + b'\x00'
                    if manque_x:
                        dit.append('RINGOUT_SPLASH retire (%s)'
                                   % ', '.join(manque_x))
                    elif len(brut_x) > RINGOUT_CHAINE_MAX:
                        print('REFUS : la chaine RINGOUT_SPLASH « %s » depasse '
                              '%d octets' % (texte_x, RINGOUT_CHAINE_MAX))
                        return 2, []
                    else:
                        oc = off_ringout_ch + ro_ajoutes * RINGOUT_CHAINE_MAX
                        contenu[oc:oc + len(brut_x)] = brut_x
                        rec_x = bytearray(rec_x)
                        struct.pack_into('<i', rec_x, 0, indice_x)
                        struct.pack_into('<Q', rec_x, 0x10, va + oc)
                        dr = off_ringout + (RINGOUT_TABLE_N + ro_ajoutes) * \
                            RINGOUT_TABLE_PAS
                        contenu[dr:dr + RINGOUT_TABLE_PAS] = rec_x
                        a_reloger.append(va + dr + 0x10)
                        ro_ajoutes += 1
                        servies[indice_x].add(12)
                        dit.append('RINGOUT_SPLASH')
            # LES COMPORTEMENTS CABLES : seulement ceux que SA generation a,
            # verifies dans son code (generation.CABLAGES, CABLAGES_APPELS).
            try:
                cab_x = g_x.cablages()
            except _gen_x.Refus as x:
                print('REFUS : %s' % x)
                return 2, []
            for nom_c, c_c in sorted(cab_x.items()):
                if cle_x in c_c['codes']:
                    if c_c['objet'] is not None:
                        n_o = tr_x.obj(c_c['objet'])
                        if n_o is None:
                            dit.append('%s retire (objet %d:%d absent)'
                                       % (nom_c, c_c['objet'] >> 16,
                                          c_c['objet'] & 0xFFFF))
                            continue
                        cablages_x.setdefault('objets_reflet', []).append(
                            (indice_x, n_o))
                    if nom_c in CABLAGES_APPELS:
                        cablages_x.setdefault(nom_c, []).append(
                            (indice_x, DECOR_NOMS.index(cle_x)))
                    if nom_c in CABLAGES_DRAPEAUX:
                        cablages_x.setdefault('drapeaux', []).append(
                            (indice_x, CABLAGES_DRAPEAUX[nom_c]))
                    dit.append('cable:%s' % nom_c)
                for nom_a in sorted(c_c['uids']):
                    n_u = tr_x.uid('A ' + nom_a)
                    if n_u is None:
                        continue              # ce decor n'a pas l'animation
                    fs_u = uids_fs_x.get(nom_a)
                    if fs_u is None:
                        print('REFUS : %s n est pas dans l auth_3d_db de FS -- '
                              'aucun test de FS ne la vise.' % nom_a)
                        return 2, []
                    cablages_x.setdefault('uids', []).append((n_u, fs_u))
                    dit.append('uid:%s=%d->0x%X' % (nom_a.split('_EFF_')[-1],
                                                   n_u, fs_u))
            dms_dits.append('%s[%s](%s)' % (code_x, g_x.nom, ' '.join(dit)))
            continue
        depuis_x = DECOR_NOMS[m_x]
        u_down = struct.unpack_from('<i', src_down, m_x * 4)[0]
        u_move = struct.unpack_from('<i', src_move, m_x * 4)[0]
        demande = [v for v in (u_down, u_move) if v != -1]
        for nom_ch in sorted(CHAINES):
            if m_x not in ch_de[nom_ch]:
                continue
            pas_ch = CHAINES[nom_ch][1]
            r = ch_de[nom_ch][m_x]
            for du in CHAINES[nom_ch][4]:
                v = struct.unpack_from('<i', src_ch[nom_ch], r * pas_ch + du)[0]
                if v != -1 and v not in demande:
                    demande.append(v)
        traduits = uids_correspondants(_eff(indice_x, code_x), depuis_x,
                                       demande, tolerant=True)
        if traduits is None:
            return 2, []
        table_x = dict(zip(demande, traduits))
        dit = []
        for nom_t, valeur, ou in (('DOWNKEMU', u_down, off_down),
                                  ('DASH', u_move, off_move)):
            if valeur == -1:
                continue
            neuf_uid = table_x.get(valeur)
            if neuf_uid is None:
                dit.append('%s absent en 2008' % nom_t)
                continue
            struct.pack_into('<i', contenu, ou + indice_x * 4, neuf_uid)
            dit.append('%s=%d' % (nom_t, neuf_uid))
        servies[indice_x] = set()
        # LA NEIGE : un clone du dossier du modele, indice mis a jour. Le
        # dossier ne porte aucun uid -- que des parametres de particules --
        # donc rien a traduire.
        if m_x in snow_de:
            ds = off_snow + (SNOW_TABLE_N + snow_ajoutes) * SNOW_TABLE_PAS
            r = snow_de[m_x]
            contenu[ds:ds + SNOW_TABLE_PAS] = \
                src_snow[r * SNOW_TABLE_PAS:(r + 1) * SNOW_TABLE_PAS]
            struct.pack_into('<i', contenu, ds, indice_x)
            snow_ajoutes += 1
            servies[indice_x].add(5)
            dit.append('SNOW')
        # LES QUATRE CHAINES : un clone du dossier du modele, indice mis a
        # jour, uid traduits. Un uid que 2008 n'a pas fait RENONCER au dossier
        # entier -- l'effet ne se joue pas a moitie.
        for nom_ch in sorted(CHAINES):
            if m_x not in ch_de[nom_ch]:
                continue
            if CHAINES_TACHE[nom_ch] in EFFETS_RETIRES.get(code_x, ()):
                continue                  # ce variant n'en veut pas
            if nom_ch in CHAINES_OBJETS:
                # des objets de l'objset du MODELE : pas de clone (la tache
                # tombe au tri final, faute de dossier)
                dit.append('%s non clone (objets)' % nom_ch)
                continue
            va_ch, pas_ch, n_ch, decal_ch, uids_ch = CHAINES[nom_ch][:5]
            r = ch_de[nom_ch][m_x]
            bloc = bytearray(src_ch[nom_ch][r * pas_ch:(r + 1) * pas_ch])
            perdu = False
            for du in uids_ch:
                v = struct.unpack_from('<i', bloc, du)[0]
                if v == -1:
                    continue
                t = table_x.get(v)
                if t is None:
                    perdu = True
                    break
                struct.pack_into('<i', bloc, du, t)
            if perdu:
                dit.append('%s absent en 2008' % nom_ch)
                continue
            struct.pack_into('<i', bloc, decal_ch, indice_x)
            dc = off_ch[nom_ch] + (n_ch + ch_ajoutes[nom_ch]) * pas_ch
            contenu[dc:dc + pas_ch] = bloc
            ch_ajoutes[nom_ch] += 1
            servies[indice_x].add(CHAINES_TACHE[nom_ch])
            dit.append(nom_ch)
        # L'ANNEAU D'EAU. Il n'a pas de table : le moteur nomme UN objet en
        # dur. On ne pose une substitution que si le modele demande vraiment
        # la tache, que son objset est bien celui du litteral, et que le rang
        # existe dans l'archive de 2008 -- trois mesures, aucune supposition.
        t_mod = [struct.unpack_from('<i', o, m_x * OBJSETS_TABLE_PAS
                                    + OBJSETS_TABLE_TACHES + j * 4)[0]
                 for j in range(16)]
        if -1 in t_mod:
            t_mod = t_mod[:t_mod.index(-1)]
        if 13 in t_mod:
            objset_m = struct.unpack_from(
                '<I', desc, m_x * DECORS_TABLE_PAS + VARIANTES_DESC_OBJSET)[0]
            rang = EAU_ANNEAU_DEFAUT & 0xFFFF
            if indice_x in speciaux:
                # ver.B : le rang de `STGSLK_WATER_RING` n'est pas 110.
                rang = trad_verb[indice_x].get(rang, -1)
            import variantes_5r as _v5r_e
            geo_x = speciaux[indice_x]['geo'] if indice_x in speciaux \
                else code_x
            if objset_m != EAU_ANNEAU_DEFAUT >> 16:
                dms_dits.append('%s(WATER_RING : le litteral 0x%X ne designe '
                                'pas l objset du modele %d)'
                                % (code_x, EAU_ANNEAU_DEFAUT, objset_m))
            elif rang not in dict(_v5r_e.objets_archive(geo_x) or []):
                dms_dits.append('%s(WATER_RING : 2008 n a pas le rang %d)'
                                % (code_x, rang))
            else:
                eau_table.append((indice_x, (objset_x << 16) | rang))
                servies[indice_x].add(13)
                dit.append('WATER_RING')
        if dit:
            dms_dits.append('%s(%s)' % (code_x, ' '.join(dit)))
    ds = off_snow + (SNOW_TABLE_N + snow_ajoutes) * SNOW_TABLE_PAS
    contenu[ds:ds + SNOW_TABLE_PAS] = src_snow[n_snow:n_snow + SNOW_TABLE_PAS]
    for nom_ch in sorted(CHAINES):
        _, pas_ch, n_ch, decal_ch = CHAINES[nom_ch][:4]
        dc = off_ch[nom_ch] + (n_ch + ch_ajoutes[nom_ch]) * pas_ch
        struct.pack_into('<i', contenu, dc + decal_ch, -1)
        dms_dits.append('%s+%d' % (nom_ch, ch_ajoutes[nom_ch]))
    # UNE TACHE DEMANDEE QUI N'A PAS RECU SON DOSSIER SE RETIRE. La liste des
    # taches a ete filtree plus haut sur EFFETS_SERVIS -- une prevision. Ici on
    # sait ce qui a ETE POSE, et c'est cela qui fait foi : une tache servie en
    # theorie mais sans dossier (un uid que 2008 n'a pas) reviendrait a ce
    # qu'on vient de corriger.
    for indice_x, posees in sorted(servies.items()):
        dt = off_objsets + indice_x * OBJSETS_TABLE_PAS + OBJSETS_TABLE_TACHES
        avant = []
        for j in range(16):
            v = struct.unpack_from('<i', contenu, dt + j * 4)[0]
            if v == -1:
                break
            avant.append(v)
        apres = [v for v in avant if v == 2 or v in posees]
        if apres == avant:
            continue
        for j in range(16):
            struct.pack_into('<i', contenu, dt + j * 4,
                             apres[j] if j < len(apres) else -1)
        faits.append('effets : l entree %d retire %s de sa liste de taches -- '
                     'elle etait servie en theorie, mais son dossier n a pas '
                     'pu etre pose (un uid que 2008 n a pas).'
                     % (indice_x,
                        ' '.join(EFFETS_NOMS[v] for v in avant
                                 if v not in apres)))
    if lot:
        faits.append('effets : les tableaux DENSES de TaskEffectDown '
                     '(0x%X) et TaskEffectMove (0x%X) passent de %d a %d '
                     'entrees dans .decors (+0x%X, +0x%X). Ils n ont NI '
                     'terminateur NI garde : au-dela de 41 le moteur y lisait '
                     'du texte de .rdata et le donnait a l auth_3d comme un '
                     'numero d uid -- et ces deux taches sont TOUJOURS creees, '
                     'donc tout decor ajoute y passait. La liste de '
                     'TaskEffectSnow (0x%X, pas 0x%X, fin -1) demenage aussi '
                     'et recoit %d entree(s). %s'
                     % (DOWN_TABLE_VA, MOVE_TABLE_VA, DECORS_TABLE_N, n,
                        off_down, off_move, SNOW_TABLE_VA, SNOW_TABLE_PAS,
                        snow_ajoutes, ' '.join(dms_dits)))

    # LE STUB DE L'ANNEAU D'EAU, dans la greffe -- c'est la seule section
    # executable qui soit a nous. Sans greffe, pas de substitution : on le DIT
    # plutot que de laisser le decor sans son eau en silence.
    if eau_table:
        if GREFFE_POSEE is None:
            print('REFUS : WATER_RING a besoin de la section .greffe, donc de '
                  '--variantes. Sans elle le stub n a nulle part ou vivre.')
            return 2, []
        if len(eau_table) + 1 > EAU_ANNEAU_MAX:
            print('REFUS : %d anneaux d eau pour %d places'
                  % (len(eau_table) + 1, EAU_ANNEAU_MAX))
            return 2, []
        g_va, g_off = GREFFE_POSEE
        va_stub, va_table = g_va + GRE_EAU, g_va + GRE_EAU_TABLE
        _poser(DLL, g_off + GRE_EAU, eau_anneau_stub(va_stub, va_table),
               va_stub)
        octets = b''
        for i_e, obj_e in eau_table:
            octets += struct.pack('<iI', i_e, obj_e)
        octets += struct.pack('<iI', -1, 0)
        _poser(DLL, g_off + GRE_EAU_TABLE, octets, va_table)
        _poser(DLL, offset(orig[DLL], EAU_ANNEAU_SITE),
               b'\xe8' + struct.pack('<i', va_stub - (EAU_ANNEAU_SITE + 5)),
               EAU_ANNEAU_SITE)
        faits.append('effets : TaskEffectWaterRing nomme son objet par un '
                     'LITTERAL (0x%X = objset %d rang %d, celui de slk) -- il '
                     'n a aucune table indexee par le decor. Les cinq octets '
                     'du `mov ecx, imm32` en 0x%X deviennent un appel au stub '
                     'de la greffe (0x%X), qui balaie {indice, objet} et rend '
                     'le litteral d origine quand l indice n y est pas : le '
                     'decor du jeu ne change pas d un poil. %d entree(s) : %s'
                     % (EAU_ANNEAU_DEFAUT, EAU_ANNEAU_DEFAUT >> 16,
                        EAU_ANNEAU_DEFAUT & 0xFFFF, EAU_ANNEAU_SITE, va_stub,
                        len(eau_table),
                        ' '.join('%d->%d:%d' % (i_e, obj_e >> 16,
                                                obj_e & 0xFFFF)
                                 for i_e, obj_e in eau_table)))

    # --- LES STUBS DES TACHES DE GENERATION (2026-09-11) --------------------
    # Voir GENERATION_STUBS : FOG_RING, SNOW_RING et RAIN recopient le dossier
    # du decor charge dans celui de FS ; WET_CLOTH rend l'indice ou 0x13.
    if gen_tables or ro_ajoutes or cablages_x:
        if GREFFE_POSEE is None:
            print('REFUS : %s ont besoin de la section .greffe, donc de '
                  '--variantes.' % ' '.join(sorted(gen_tables)))
            return 2, []
        g_va, g_off = GREFFE_POSEE
        o_g = GRE_GEN
        dits_gen = []

        def _lire_orig(va_l, n_l):
            return pe.get_data(va_l - DECORS_BASE, n_l)

        def _octets_dll(va_l, n_l):
            with open(orig[DLL], 'rb') as fp_l:
                fp_l.seek(offset(orig[DLL], va_l))
                return fp_l.read(n_l)

        def _appel(site_l, cible_l):
            _poser(DLL, offset(orig[DLL], site_l), b'\xe8' + struct.pack(
                '<i', cible_l - (site_l + 5)), site_l)

        # le `call 0x18006F350` de RINGOUT_SPLASH : voir RINGOUT_TABLE_VA
        if ro_ajoutes:
            va_stub = g_va + o_g
            avant = _octets_dll(RINGOUT_SITE_POUSSEE, 5)
            if avant[0] != 0xE8 or RINGOUT_SITE_POUSSEE + 5 + struct.unpack(
                    '<i', avant[1:])[0] != RINGOUT_GESTIONNAIRE:
                print('REFUS : 0x%X n appelle pas 0x%X (%s).'
                      % (RINGOUT_SITE_POUSSEE, RINGOUT_GESTIONNAIRE,
                         avant.hex()))
                return 2, []
            stub = stub_ringout_poussee(va_stub)
            _poser(DLL, g_off + o_g, stub, va_stub)
            _appel(RINGOUT_SITE_POUSSEE, va_stub)
            dits_gen.append('RINGOUT_SPLASH : le `call 0x%X` (0x%X) passe par '
                            '0x%X, qui rend 0 -- « ne pas pousser » -- quand '
                            'le y de l element est le NaN des generations'
                            % (RINGOUT_GESTIONNAIRE, RINGOUT_SITE_POUSSEE,
                               va_stub))
            o_g = (o_g + len(stub) + 0xF) & ~0xF

        for nom_s, _ in GENERATION_TACHES:
            ents_s = gen_tables.get(nom_s)
            if not ents_s:
                continue
            va_stub = g_va + o_g
            if nom_s == 'YUKA':
                pas_y = len(ents_s[0][1])
                jeu_fs = _octets_dll(YUKA_SITE_JEU, 5)
                uid_fs = _octets_dll(YUKA_SITE_UID, 5)
                obj_fs = _octets_dll(YUKA_SITE_OBJET, 5)
                if jeu_fs[0] != 0xB9 or uid_fs[0] != 0xBA or \
                        obj_fs[0] != 0xB9:
                    print('REFUS : les litteraux de Yuka ne sont pas ou on '
                          'les attend (%s %s %s).' % (
                              jeu_fs.hex(), uid_fs.hex(), obj_fs.hex()))
                    return 2, []
                defaut_y = tuple(struct.unpack('<I', b[1:])[0]
                                 for b in (jeu_fs, uid_fs, obj_fs))
                for s_t in YUKA_SITES_TABLE:
                    b = _octets_dll(s_t, 7)
                    if b[:3] != b'\x48\x8d\x05' or s_t + 7 + struct.unpack(
                            '<i', b[3:])[0] != YUKA_TABLE_FS:
                        print('REFUS : 0x%X ne charge pas la table 0x%X.'
                              % (s_t, YUKA_TABLE_FS))
                        return 2, []
                if struct.unpack('<Q', _lire_orig(YUKA_VTABLE, 8))[0] != \
                        YUKA_SETSTAGE or YUKA_VTABLE not in relogees:
                    print('REFUS : le creneau 0x%X ne vaut pas 0x%X.'
                          % (YUKA_VTABLE, YUKA_SETSTAGE))
                    return 2, []
                va_var = va_stub
                va_stub = va_var + 0x20
                longueur = len(stubs_yuka(va_stub, va_var, va_stub, 0, pas_y,
                                          defaut_y)[0])
                va_table = (va_stub + longueur + 0xF) & ~0xF
                stub, lecteurs = stubs_yuka(va_stub, va_var, va_table,
                                            len(ents_s), pas_y, defaut_y)
                table = b''.join(r_s for _, r_s in ents_s)
                fin = va_table + len(table)
                if fin - g_va > GREFFE_TAILLE:
                    print('REFUS : la greffe est pleine (YUKA : 0x%X > 0x%X)'
                          % (fin - g_va, GREFFE_TAILLE))
                    return 2, []
                _poser(DLL, g_off + (va_var - g_va), b'\x00' * 0x20, va_var)
                _poser(DLL, g_off + (va_stub - g_va), stub, va_stub)
                _poser(DLL, g_off + (va_table - g_va), table, va_table)
                _appel(YUKA_SITE_JEU, lecteurs['jeu'])
                _appel(YUKA_SITE_UID, lecteurs['uid'])
                _appel(YUKA_SITE_OBJET, lecteurs['objet'])
                for s_t in YUKA_SITES_TABLE:
                    _poser(DLL, offset(orig[DLL], s_t), b'\x48\x8b\x05' +
                           struct.pack('<i', va_var + 0x10 - (s_t + 7)), s_t)
                _poser(DLL, offset(orig[DLL], YUKA_VTABLE),
                       struct.pack('<Q', va_stub), YUKA_VTABLE)
                dits_gen.append('YUKA : le creneau 7 (0x%X) passe par 0x%X, '
                                'qui ecrit en 0x%X {objset, uid, objet, table} '
                                '-- de %s, sinon ceux de FS (%d, %d, 0x%X, '
                                '0x%X) ; les cinq litteraux la relisent'
                                % (YUKA_VTABLE, va_stub, va_var,
                                   ' '.join(str(i) for i, _ in ents_s),
                                   defaut_y[0], defaut_y[1], defaut_y[2],
                                   YUKA_TABLE_FS))
                o_g = (fin - g_va + 0xF) & ~0xF
                continue
            if nom_s == 'WET_CLOTH':
                # seuls les decors a 0,4 entrent dans la table : les autres
                # prennent le 0,001 de FS, puisque leur indice n'est pas 19
                fort = [i_s for i_s, r_s in ents_s
                        if struct.unpack('<I', r_s)[0] == 0x3ECCCCCD]
                if not fort:
                    dits_gen.append('WET_CLOTH : %s a 0,001, le choix de FS '
                                    'pour tout indice autre que 19 -- aucun '
                                    'stub' % ' '.join(str(i) for i, _ in
                                                       ents_s))
                    continue
                va_table = va_stub + 0x30
                stub = stub_wet_cloth(va_stub, va_table)
                table = b''.join(struct.pack('<i', i_s) for i_s in fort) + \
                    struct.pack('<i', -1)
                site_o = offset(orig[DLL], WET_CLOTH_SITE)
                with open(orig[DLL], 'rb') as fp:
                    fp.seek(site_o)
                    avant = fp.read(5)
                if avant != b'\xb8\x13\x00\x00\x00':
                    print('REFUS : 0x%X porte %s, pas `mov eax, 0x13`.'
                          % (WET_CLOTH_SITE, avant.hex()))
                    return 2, []
                fin = va_table + len(table)
                if fin - g_va > GREFFE_TAILLE:
                    print('REFUS : la greffe est pleine (WET_CLOTH)')
                    return 2, []
                _poser(DLL, g_off + (va_stub - g_va), stub, va_stub)
                _poser(DLL, g_off + (va_table - g_va), table, va_table)
                _poser(DLL, site_o, b'\xe8' + struct.pack(
                    '<i', va_stub - (WET_CLOTH_SITE + 5)), WET_CLOTH_SITE)
                dits_gen.append('WET_CLOTH : `mov eax, 0x13` (0x%X) -> stub '
                                '0x%X ; 0,4 pour %s, 0,001 pour les autres'
                                % (WET_CLOTH_SITE, va_stub,
                                   ' '.join(str(i) for i in fort)))
                o_g = (fin - g_va + 0xF) & ~0xF
                continue
            d_s = GENERATION_STUBS[nom_s]
            pas_s = d_s['pas']
            fs_orig = _lire_orig(d_s['dossier'], pas_s)
            if d_s['indice']:
                entree_pas, src = pas_s, 0
                table = b''.join(r_s for _, r_s in ents_s) + fs_orig
            else:
                entree_pas, src = 4 + pas_s, 4
                table = b''.join(struct.pack('<i', i_s) + r_s
                                 for i_s, r_s in ents_s) + \
                    struct.pack('<i', -1) + fs_orig
            # la taille du stub ne depend pas des adresses : un premier jet
            longueur = len(stub_copie(va_stub, va_stub, 0, entree_pas, src,
                                      pas_s, d_s['dossier'], d_s.get('appel')))
            va_table = (va_stub + longueur + 0xF) & ~0xF
            stub = stub_copie(va_stub, va_table, len(ents_s), entree_pas, src,
                              pas_s, d_s['dossier'], d_s.get('appel'))
            fin = va_table + len(table)
            if fin - g_va > GREFFE_TAILLE:
                print('REFUS : la greffe est pleine (%s : 0x%X > 0x%X)'
                      % (nom_s, fin - g_va, GREFFE_TAILLE))
                return 2, []
            if 'site' in d_s:
                site_o = offset(orig[DLL], d_s['site'])
                with open(orig[DLL], 'rb') as fp:
                    fp.seek(site_o)
                    avant = fp.read(5)
                if avant[0] != 0xE8 or d_s['site'] + 5 + struct.unpack(
                        '<i', avant[1:])[0] != d_s['appel']:
                    print('REFUS : 0x%X n appelle pas 0x%X (%s).'
                          % (d_s['site'], d_s['appel'], avant.hex()))
                    return 2, []
                _poser(DLL, site_o, b'\xe8' + struct.pack(
                    '<i', va_stub - (d_s['site'] + 5)), d_s['site'])
                ou = 'l appel 0x%X -> 0x%X' % (d_s['site'], d_s['appel'])
            else:
                # le creneau 7 d'une vtable : un pointeur de .rdata, qui a sa
                # relocation -- on change sa valeur, la relocation reste
                if struct.unpack('<Q', _lire_orig(d_s['vtable'], 8))[0] != \
                        d_s['defaut'] or d_s['vtable'] not in relogees:
                    print('REFUS : le creneau 0x%X ne vaut pas 0x%X, ou n a '
                          'pas de relocation.' % (d_s['vtable'],
                                                   d_s['defaut']))
                    return 2, []
                _poser(DLL, offset(orig[DLL], d_s['vtable']),
                       struct.pack('<Q', va_stub), d_s['vtable'])
                ou = 'le creneau 7 (0x%X, etait le `ret 0` 0x%X)' % (
                    d_s['vtable'], d_s['defaut'])
            _poser(DLL, g_off + (va_stub - g_va), stub, va_stub)
            _poser(DLL, g_off + (va_table - g_va), table, va_table)
            dits_gen.append('%s : %s passe par le stub 0x%X, qui recopie dans '
                            '0x%X (0x%X octets) le dossier de %s, sinon '
                            'l original de FS' % (
                                nom_s, ou, va_stub, d_s['dossier'], pas_s,
                                ' '.join(str(i) for i, _ in ents_s)))
            o_g = (fin - g_va + 0xF) & ~0xF
        # --- le shader des empreintes, avec SNOW_RING (voir plus haut) -----
        if gen_tables.get('SNOW_RING'):
            import shader_empreintes
            fautes_sh = shader_empreintes.controler()
            if fautes_sh:
                print('REFUS : SNOW_RING est servie mais %s n est pas conforme '
                      '(%s) -- lancer d abord tools\\shader_empreintes.py.'
                      % (shader_empreintes.CHEMIN_VF5, ' ; '.join(fautes_sh)))
                return 2, []
            avant = _octets_dll(SHADER_EMPREINTES_SITE, 7)
            if avant[:3] != b'\x48\x8d\x15' or SHADER_EMPREINTES_SITE + 7 + \
                    struct.unpack('<i', avant[3:])[0] != SHADER_ARCHIVE_FS_VA:
                print('REFUS : 0x%X ne charge pas 0x%X (%s).'
                      % (SHADER_EMPREINTES_SITE, SHADER_ARCHIVE_FS_VA,
                         avant.hex()))
                return 2, []
            if _lire_orig(SHADER_ARCHIVE_FS_VA, 24) != \
                    b'w64/shader_pxd_w64.farc\x00':
                print('REFUS : 0x%X n est pas le chemin de l archive de FS.'
                      % SHADER_ARCHIVE_FS_VA)
                return 2, []
            va_s = g_va + o_g
            va_nom = va_s + 48
            nom_b = shader_empreintes.MEMBRE.encode('ascii') + b'\x00'
            va_ch = (va_nom + len(nom_b) + 7) & ~7
            ch_b = shader_empreintes.CHEMIN_VF5.encode('ascii') + b'\x00'
            fin = va_ch + len(ch_b)
            if fin - g_va > GREFFE_TAILLE:
                print('REFUS : la greffe est pleine (shader des empreintes)')
                return 2, []
            _poser(DLL, g_off + (va_s - g_va),
                   stub_shader_empreintes(va_s, va_nom, va_ch), va_s)
            _poser(DLL, g_off + (va_nom - g_va), nom_b, va_nom)
            _poser(DLL, g_off + (va_ch - g_va), ch_b, va_ch)
            _poser(DLL, offset(orig[DLL], SHADER_EMPREINTES_SITE),
                   b'\xe8' + struct.pack('<i', va_s - (
                       SHADER_EMPREINTES_SITE + 5)) + b'\x66\x90',
                   SHADER_EMPREINTES_SITE)
            dits_gen.append('shader des empreintes : le `lea` 0x%X passe par '
                            '0x%X ; « %s » est lu dans %s (GSFX, geometry '
                            'shader), tout autre shader dans celle de FS'
                            % (SHADER_EMPREINTES_SITE, va_s,
                               shader_empreintes.MEMBRE,
                               shader_empreintes.CHEMIN_VF5))
            o_g = (fin - g_va + 0xF) & ~0xF
        # --- LES COMPORTEMENTS CABLES (voir CABLAGES_APPELS) ---------------
        def _poser_stub(stub_fn, entrees_c):
            """Pose stub + table {a, b} fin -1 ; rend l'adresse du stub."""
            nonlocal_o = [o_g]
            va_s = g_va + nonlocal_o[0]
            long_s = len(stub_fn(va_s, va_s))
            va_t = (va_s + long_s + 0xF) & ~0xF
            tab = b''.join(struct.pack('<iI', a_c, b_c & 0xFFFFFFFF)
                           for a_c, b_c in entrees_c) + struct.pack('<iI', -1, 0)
            fin_c = va_t + len(tab)
            if fin_c - g_va > GREFFE_TAILLE:
                return None, fin_c
            _poser(DLL, g_off + (va_s - g_va), stub_fn(va_s, va_t), va_s)
            _poser(DLL, g_off + (va_t - g_va), tab, va_t)
            return va_s, fin_c

        def _verifier_appel(site_c, cible_c):
            b_c = _octets_dll(site_c, 5)
            return b_c[0] == 0xE8 and site_c + 5 + struct.unpack(
                '<i', b_c[1:])[0] == cible_c

        for nom_c in sorted(CABLAGES_APPELS):
            ents_c = cablages_x.get(nom_c)
            if not ents_c:
                continue
            if not all(_verifier_appel(s_c, GETTER_DECOR)
                       for s_c in CABLAGES_APPELS[nom_c]):
                print('REFUS : %s -- un site n appelle plus 0x%X.'
                      % (nom_c, GETTER_DECOR))
                return 2, []
            va_s, fin_c = _poser_stub(stub_alias, ents_c)
            if va_s is None:
                print('REFUS : la greffe est pleine (%s)' % nom_c)
                return 2, []
            for s_c in CABLAGES_APPELS[nom_c]:
                _appel(s_c, va_s)
            dits_gen.append('%s : %s appellent 0x%X, qui rend %s' % (
                nom_c, ' '.join('0x%X' % s for s in CABLAGES_APPELS[nom_c]),
                va_s, ' '.join('%d->%d' % e_c for e_c in ents_c)))
            o_g = (fin_c - g_va + 0xF) & ~0xF
        if cablages_x.get('objets_reflet'):
            if _octets_dll(CABLAGE_REFLET_SITE, 5) != b'\xb9' + struct.pack(
                    '<I', CABLAGE_REFLET_DEFAUT):
                print('REFUS : 0x%X n est pas `mov ecx, 0x%X`.'
                      % (CABLAGE_REFLET_SITE, CABLAGE_REFLET_DEFAUT))
                return 2, []
            va_s, fin_c = _poser_stub(stub_objet_reflet,
                                      cablages_x['objets_reflet'])
            if va_s is None:
                print('REFUS : la greffe est pleine (reflet)')
                return 2, []
            _appel(CABLAGE_REFLET_SITE, va_s)
            dits_gen.append('reflet du grillage : `mov ecx, 0x%X` (0x%X) -> '
                            '0x%X : %s' % (
                                CABLAGE_REFLET_DEFAUT, CABLAGE_REFLET_SITE,
                                va_s, ' '.join('%d->%d:%d' % (
                                    i_c, o_c >> 16, o_c & 0xFFFF) for i_c, o_c
                                    in cablages_x['objets_reflet'])))
            o_g = (fin_c - g_va + 0xF) & ~0xF
        if cablages_x.get('drapeaux'):
            if struct.unpack('<Q', _lire_orig(A3D_VTABLE7, 8))[0] != \
                    A3D_SETSTAGE or A3D_VTABLE7 not in relogees:
                print('REFUS : le creneau 0x%X ne vaut pas 0x%X.'
                      % (A3D_VTABLE7, A3D_SETSTAGE))
                return 2, []
            va_s, fin_c = _poser_stub(stub_a3d_setstage,
                                      cablages_x['drapeaux'])
            if va_s is None:
                print('REFUS : la greffe est pleine (Auth3D)')
                return 2, []
            _poser(DLL, offset(orig[DLL], A3D_VTABLE7),
                   struct.pack('<Q', va_s), A3D_VTABLE7)
            dits_gen.append('Auth3D : le creneau 7 (0x%X) passe par 0x%X, '
                            'qui pose apres coup %s' % (
                                A3D_VTABLE7, va_s, ' '.join(
                                    '%d:+0x%X' % e_c
                                    for e_c in cablages_x['drapeaux'])))
            o_g = (fin_c - g_va + 0xF) & ~0xF
        if cablages_x.get('uids'):
            if not all(_verifier_appel(s_c, UID_ACCESSEUR)
                       for s_c in A3D_UID_SITES):
                print('REFUS : un site d Auth3D n appelle plus 0x%X.'
                      % UID_ACCESSEUR)
                return 2, []
            va_s, fin_c = _poser_stub(stub_uid, cablages_x['uids'])
            if va_s is None:
                print('REFUS : la greffe est pleine (uid)')
                return 2, []
            for s_c in A3D_UID_SITES:
                _appel(s_c, va_s)
            dits_gen.append('Auth3D : l accesseur d uid (0x%X) passe par '
                            '0x%X a %s : %s' % (
                                UID_ACCESSEUR, va_s, ' '.join(
                                    '0x%X' % s for s in A3D_UID_SITES),
                                ' '.join('%d->0x%X' % e_c
                                         for e_c in cablages_x['uids'])))
            o_g = (fin_c - g_va + 0xF) & ~0xF
        faits.append('effets de generation : %s. Greffe utilisee jusqu a '
                     '0x%X sur 0x%X.' % (' ; '.join(dits_gen), o_g,
                                         GREFFE_TAILLE))

    # --- LES DEUX TABLES D'EFFETS, ET LES UID DU DECOR NEUF -----------------
    # Sans elles, le decor se charge mais reste sans ses flammes et sans son
    # mur : chaque tache d'effet a sa propre liste d'association, et un indice
    # inconnu n'y fait RIEN. Voir le commentaire de EFFETS_A3D_VA.
    n_a3d, n_mur = EFFETS_A3D_N * EFFETS_A3D_PAS, EFFETS_MUR_N * EFFETS_MUR_PAS
    contenu[off_eff_a3d:off_eff_a3d + n_a3d] = src_a3d[:n_a3d]
    contenu[off_eff_mur:off_eff_mur + n_mur] = src_mur[:n_mur]
    for k in range(0, n_a3d, 8):
        if EFFETS_A3D_VA + k in relogees:
            a_reloger.append(va + off_eff_a3d + k)
    for k in range(0, n_mur, 8):
        if EFFETS_MUR_VA + k in relogees:
            a_reloger.append(va + off_eff_mur + k)

    # `src_a3d`, `src_mur`, `r_a3d`, `r_mur`, `charges` et `modele_mur` sont
    # lus en 1 bis : la taille de la charge du mur entre dans le calcul de la
    # section.
    def _liste_uid(ptr):
        out = []
        while len(out) < EFFETS_UIDS_MAX - 1:
            v = struct.unpack('<i', pe.get_data(
                ptr - DECORS_BASE + 4 * len(out), 4))[0]
            if v == -1:
                break
            out.append(v)
        return out

    def _reloc_mur(m):
        return [o for o in range(0, EFFETS_MUR_PAS, 8)
                if EFFETS_MUR_VA + r_mur[m] * EFFETS_MUR_PAS + o in relogees]

    # Les trois blocs du mur sont repointes plus bas : leurs relocations
    # doivent DEJA exister chez le modele, sinon l adresse qu on y ecrit ne
    # survivrait pas au rebasage -- la faute deja payee sur la greffe.
    for m in charges:
        rl = _reloc_mur(m)
        besoin_rl = set([0x08])
        if charges[m]['a_uids']:
            besoin_rl.add(0x10)
        if charges[m]['a_paires']:
            besoin_rl.add(0x18)
        for nom_bloc, champ in (('p20', 0x20), ('u28', 0x28),
                                ('o30', 0x30), ('u38', 0x38)):
            if nom_bloc in charges[m]['extra']:
                besoin_rl.add(champ)
        if not besoin_rl.issubset(rl):
            print('REFUS : l entree de mur de %s n a pas de relocation en %s '
                  '(elle en a en %s). Repointer ces champs ecrirait une '
                  'adresse morte au rebasage.'
                  % (DECOR_NOMS[m],
                     ' '.join('+0x%02X' % o for o in sorted(besoin_rl)),
                     ' '.join('+0x%02X' % o for o in rl)))
            return 2, []
    mur_reloc = _reloc_mur(DECORS_MODELE)
    codes_neufs = dict((i, c) for _, c, i, _, _ in lot)
    objsets_neufs = dict((i, s) for _, _, i, s, _ in lot)

    a3d_ajoutes = mur_ajoutes = 0
    anims_v = None                      # les animations de ver.B, a la demande
    for k in range(neufs):
        indice = DECORS_TABLE_N + k
        m = modele_de(indice)
        # LE MUR : un clone complet de l'entree du modele, indice mis a jour.
        # UN MODELE SANS MUR N'EN DONNE PAS. `riv` et `smo` n'ont pas d'entree
        # dans cette table -- c'est une LISTE D'ASSOCIATION, tous les decors
        # n'y sont pas. Leur en fabriquer une, fut-elle inerte, ferait pointer
        # le clone sur le mur de `djo` : exactement le defaut qu'on vient de
        # corriger, et le controle le voit.
        #
        # ET UN DECOR SANS MUR GARDE SES ANIMATIONS D'EFFET (2026-09-11). Ce
        # bloc sautait jusqu'a l'entree suivante : `rv5` et `so5` perdaient
        # donc AUSSI leur entree dans la table des animations d'effet, que
        # leurs modeles ont (riv et smo y sont, releve dans `.origine`). Le
        # mur et les animations sont deux tables : l'absence de l'un ne dit
        # rien de l'autre.
        if indice in speciaux:
            sans_mur = indice not in charge_verb
        else:
            sans_mur = r_mur.get(m) is None
        if sans_mur:
            faits.append('decor neuf : l entree %d n a PAS d entree de mur, '
                         'parce que %s.'
                         % (indice, '%s n en a pas pour ce lieu'
                            % trads[indice].g.nom
                            if indice in speciaux else
                            'son modele %s n en a pas' % DECOR_NOMS[m]))
        elif indice in charge_verb:
            # UNE ENTREE NEUVE, PAS UN CLONE : ses pointeurs sont poses plus
            # bas avec LEURS relocations -- aucune n'est heritee d'un modele.
            d = off_eff_mur + (EFFETS_MUR_N + mur_ajoutes) * EFFETS_MUR_PAS
            contenu[d:d + EFFETS_MUR_PAS] = bytes(EFFETS_MUR_PAS)
            struct.pack_into('<i', contenu, d, indice)
            mur_ajoutes += 1
        else:
            d = off_eff_mur + (EFFETS_MUR_N + mur_ajoutes) * EFFETS_MUR_PAS
            contenu[d:d + EFFETS_MUR_PAS] = \
                src_mur[r_mur[m] * EFFETS_MUR_PAS:(r_mur[m] + 1) * EFFETS_MUR_PAS]
            struct.pack_into('<i', contenu, d, indice)
            for o in _reloc_mur(m):
                a_reloger.append(va + d + o)
            mur_ajoutes += 1
        if indice not in modeles:
            continue                       # une entree de remplissage (xNN)

        code_neuf = codes_neufs[indice]
        objset_neuf = objsets_neufs[indice]
        depuis_neuf = DECOR_NOMS[m]
        objset_modele = struct.unpack_from(
            '<I', desc, m * DECORS_TABLE_PAS + VARIANTES_DESC_OBJSET)[0]
        eff_neuf = _eff(indice, code_neuf)

        # ver.B : LA LISTE D'ANIMATIONS EST LA SIENNE, relue dans son ELF
        # (`variantes_vf5.animations_verb`), noms rendus a NOS uid par la base
        # posee. Pas de registre ici : le binaire dit ce que ver.B jouait.
        if indice in speciaux:
            import generation as _gen_a
            e_a = speciaux[indice]
            noms_a = _gen_a.generation(e_a['gen']).animations(e_a['cle'])
            nos_uids, perdus_a = [], []
            for nom_a in noms_a:
                k_a = trads[indice].uid(nom_a)
                if k_a is None:
                    perdus_a.append(nom_a.split()[-1])
                else:
                    nos_uids.append(k_a)
            if nos_uids:
                ou = off_eff_uids + k * EFFETS_UIDS_MAX * 4
                for j, num in enumerate(nos_uids[:EFFETS_UIDS_MAX - 1]):
                    struct.pack_into('<i', contenu, ou + j * 4, num)
                struct.pack_into('<i', contenu,
                                 ou + min(len(nos_uids),
                                          EFFETS_UIDS_MAX - 1) * 4, -1)
                da = off_eff_a3d + (EFFETS_A3D_N + a3d_ajoutes) * EFFETS_A3D_PAS
                struct.pack_into('<i', contenu, da, indice)
                struct.pack_into('<Q', contenu, da + 8, va + ou)
                a_reloger.append(va + da + 8)
                a3d_ajoutes += 1
            faits.append('%s : les ANIMATIONS d effet de l entree %d (%s) '
                         'sont les siennes : %s%s.'
                         % (_gen_a.generation(e_a['gen']).nom, indice,
                            code_neuf,
                            ' '.join(x.split()[-1].split('_EFF_')[-1]
                                     for x in noms_a) or 'aucune',
                            ' ; ABSENTES de l archive : %s' % perdus_a
                            if perdus_a else ''))
        # LES ANIMATIONS D'EFFET : la liste doit porter NOS numeros d'uid.
        if indice not in speciaux and r_a3d.get(m) is not None:
            liste_modele = _liste_uid(struct.unpack_from(
                '<Q', src_a3d, r_a3d[m] * EFFETS_A3D_PAS + 8)[0])
            nos_uids = uids_correspondants(eff_neuf, depuis_neuf,
                                           liste_modele, tolerant=True)
            if nos_uids is None:
                return 2, []
            absents = [liste_modele[j] for j, v in enumerate(nos_uids)
                       if v is None]
            nos_uids = [v for v in nos_uids if v is not None]
            if absents:
                faits.append('decor neuf : %s n a pas en 2008 les animations '
                             'd effet %s -- elles sont retirees de sa liste.'
                             % (code_neuf, absents))
            if not nos_uids:
                faits.append('decor neuf : %s n a AUCUNE animation d effet en '
                             '2008 : pas d entree dans la table des effets '
                             'a3d.' % code_neuf)
                liste_modele = []
            if not nos_uids:
                pass
            # ET LES ANIMATIONS QUE 2008 A EN PLUS : les marcheurs, les
            # spectateurs. Voir `animations_en_plus`.
            en_plus, dispo_2008 = animations_en_plus(eff_neuf,
                                                     set(nos_uids))
            if dispo_2008:
                faits.append('decor neuf : %s a en 2008 %d animation(s) '
                             'qu AUCUN mecanisme du moteur ne demande, et '
                             'qu on ne joue donc PAS : %s. Les jouer serait '
                             'les mettre en boucle sans savoir si elles sont '
                             'des boucles -- c est ce qui a mis des eclairs '
                             'permanents sur hi5. Elles s ouvrent une par une, '
                             'par ANIMATIONS_VALIDEES, apres un essai a '
                             'l ecran.' % (code_neuf, len(dispo_2008),
                                           ' '.join(dispo_2008)))
            if en_plus:
                reste = EFFETS_UIDS_MAX - 1 - len(nos_uids)
                if len(en_plus) > reste:
                    en_plus = en_plus[:reste]
                nos_uids = nos_uids + [n for n, _ in en_plus]
                faits.append('decor neuf : %s joue AUSSI %d animation(s) que '
                             '2008 a et que Final Showdown n a plus : %s. '
                             'Chacune est au REGISTRE : elle a ete vue a '
                             'l ecran.'
                             % (code_neuf, len(en_plus),
                                ' '.join(nom.split('_', 1)[-1]
                                         for _, nom in en_plus)))
            ou = off_eff_uids + k * EFFETS_UIDS_MAX * 4
            for j, num in enumerate(nos_uids):
                struct.pack_into('<i', contenu, ou + j * 4, num)
            struct.pack_into('<i', contenu, ou + len(nos_uids) * 4, -1)
            da = off_eff_a3d + (EFFETS_A3D_N + a3d_ajoutes) * EFFETS_A3D_PAS
            struct.pack_into('<i', contenu, da, indice)
            struct.pack_into('<Q', contenu, da + 8, va + ou)
            a_reloger.append(va + da + 8)
            a3d_ajoutes += 1
            faits.append('decor neuf : les ANIMATIONS d effet de l entree %d '
                         '(%s) sont les uid %s ; celles de %s etaient %s.'
                         % (indice, code_neuf, nos_uids, depuis_neuf,
                            liste_modele))

        # LE MUR, POUR DE BON. L'entree ne porte que des pointeurs : tout le
        # mur est dans les trois blocs qu'ils designent, et ces blocs nomment
        # leurs objets par `(objset << 16) | rang` -- l'objset du MODELE. Un
        # clone de l'entree seule renvoie donc au mur du modele, qui n'est pas
        # charge : le decor s'affiche sans ses barrieres, en silence.
        # LE MUR DE ver.B : ses blocs convertis, ses uid retrouves PAR NOM dans
        # la base posee, et les relocations des quatre pointeurs posees ici.
        if indice in charge_verb:
            cv = charge_verb[indice]
            tr_w = trads[indice]

            def _uid_w(nom_w):
                if nom_w is None:
                    return -1
                return tr_w.uid(nom_w)
            off_p, off_u, off_q, off_sup = off_mur[indice]
            contenu[off_p:off_p + len(cv['pieces'])] = cv['pieces']
            uids_w = [_uid_w(x) for x in cv['uids']]
            perdus_w = [x for x, y in zip(cv['uids'], uids_w) if y is None]
            uids_w = [y for y in uids_w if y is not None]
            for j, num in enumerate(uids_w):
                struct.pack_into('<i', contenu, off_u + j * 4, num)
            struct.pack_into('<i', contenu, off_u + len(uids_w) * 4, -1)
            garde_w = 0
            for j, (ob1, ob2, n1, n2) in enumerate(cv['paires']):
                a1, a2 = _uid_w(n1), _uid_w(n2)
                if a1 is None or a2 is None:
                    perdus_w.append('paire %d' % j)
                    break
                struct.pack_into(
                    '<IIii', contenu, off_q + j * EFFETS_MUR_PAIRE_PAS,
                    tr_w.obj(ob1), tr_w.obj(ob2), a1, a2)
                garde_w += 1
            struct.pack_into('<i', contenu,
                             off_q + garde_w * EFFETS_MUR_PAIRE_PAS, -1)
            champs_w = [(0x08, off_p), (0x10, off_u), (0x18, off_q)]
            if cv['p20'] is not None:
                o2 = off_sup['p20']
                contenu[o2:o2 + len(cv['p20'])] = cv['p20']
                champs_w.append((0x20, o2))
            # VF5 R : +0x28 le grillage anime (DEUX uid, deroules sans
            # condition), +0x30 les objets cassables {objet, uid, 2 flottants}
            # et +0x38 un uid par objet -- le moteur en lit min(morceaux, 4).
            # Une animation manquante met le POINTEUR a zero (seule garde du
            # moteur), jamais un bloc tronque. Voir le mur des modeles FS.
            if cv['u28'] is not None:
                t28 = [tr_w.uid(x) for x in cv['u28']]
                if None in t28:
                    perdus_w.append('grillage anime')
                else:
                    o2 = off_sup['u28']
                    struct.pack_into('<2i', contenu, o2, *t28)
                    champs_w.append((0x28, o2))
            if cv['o30'] is not None:
                recs, ok30 = [], True
                for ob_c, u_c, fl_c in cv['o30']:
                    ob_n = tr_w.obj(ob_c)
                    if ob_n is None and (ob_c >> 16) != tr_w.o_gen:
                        # UN OBJET D'UN AUTRE DECOR, recopie tel quel : chez
                        # VF5 R comme chez FS, l'entree de `tan` nomme l'objet
                        # 34:545 -- celui de `hai` -- avec ses propres uid
                        # (l'enregistrement de hai recopie chez SEGA). Cet
                        # objset n'est pas charge : l'objet ne fait rien, dans
                        # la generation deja. Le clone se comporte pareil.
                        ob_n = ob_c
                        perdus_w.append('objet %d:%d d un autre decor, recopie '
                                        'tel quel' % (ob_c >> 16,
                                                      ob_c & 0xFFFF))
                    u_n = -1 if u_c is None else tr_w.uid(u_c)
                    if ob_n is None or u_n is None:
                        ok30 = False
                        break
                    recs.append(struct.pack('<Ii', ob_n, u_n) + fl_c)
                u38 = []
                for u_c in (cv['u38'] or []):
                    u_n = -1 if u_c is None else tr_w.uid(u_c)
                    if u_n is None:
                        ok30 = False
                    u38.append(-1 if u_n is None else u_n)
                if not ok30:
                    perdus_w.append('objets cassables')
                else:
                    o2 = off_sup['o30']
                    contenu[o2:o2 + 0x10 * len(recs)] = b''.join(recs)
                    champs_w.append((0x30, o2))
                    if cv['u38'] is not None:
                        o3 = off_sup['u38']
                        struct.pack_into('<%di' % len(u38), contenu, o3, *u38)
                        champs_w.append((0x38, o3))
            for champ_w, off_w in champs_w:
                struct.pack_into('<Q', contenu, d + champ_w, va + off_w)
                a_reloger.append(va + d + champ_w)
            nom_gen_w = tr_w.g.nom
            faits.append('%s : le MUR de l entree %d (%s) est le sien, '
                         'converti au format de FS : %d morceaux%s, '
                         '%d uid, %d paire(s)%s.'
                         % (nom_gen_w, indice, code_neuf, cv['n_pieces'],
                            ' + un second tableau' if cv['p20'] else '',
                            len(uids_w), garde_w,
                            ' ; perdus : %s' % perdus_w if perdus_w else ''))
            continue
        charge = charges.get(m)
        if charge is None or sans_mur:
            faits.append('decor neuf : %s n a pas d entree de mur (%s) -- ce '
                         'decor n a pas de barrieres.'
                         % (code_neuf, 'le modele %s non plus' % depuis_neuf
                            if charge is None else
                            'ver.B n a pas les objets du mur de %s'
                            % depuis_neuf))
            continue
        # TOUS LES UID DU MUR, pas seulement ceux de la liste +0x10. Les blocs
        # +0x30 et +0x38 en citent d'autres de la meme categorie (`umi` :
        # 3361 = STGUMI_EFF_SAKU_BROKEN). On les releve d'abord, puis on les
        # traduit EN UN SEUL appel -- `uids_correspondants` relit la base
        # posee a chaque fois.
        tous = list(charge['uids'])
        for j in range(charge['n_paires']):
            o = j * EFFETS_MUR_PAIRE_PAS
            tous += [struct.unpack_from('<i', charge['paires'], o + c)[0]
                     for c in (0x8, 0xC)]
        for nom_bloc, (octets, nb) in charge['extra'].items():
            if nom_bloc == 'u28':
                tous += list(struct.unpack_from('<2i', octets, 0))
            elif nom_bloc == 'o30':
                tous += [struct.unpack_from('<i', octets,
                                            j * EFFETS_MUR_PAIRE_PAS + 4)[0]
                         for j in range(nb)]
            elif nom_bloc == 'u38':
                tous += list(struct.unpack_from('<%di' % nb, octets, 0))
        tous = sorted(set(v for v in tous if v != -1))
        traduits = uids_correspondants(eff_neuf, depuis_neuf, tous,
                                       tolerant=True)
        if traduits is None:
            return 2, []
        table_uid = dict(zip(tous, traduits))
        perdus = sorted(v for v, t in table_uid.items() if t is None)
        if perdus:
            faits.append('decor neuf : %s n a pas en 2008 les animations de '
                         'mur %s ; ce qu elles servaient est retire (un uid '
                         'absent, c est TaskEffectWall qui attend pour '
                         'toujours).' % (code_neuf, perdus))
        if any(table_uid.get(v) is None for v in charge['uids']):
            faits.append('decor neuf : %s perd la reaction de mur elle-meme.'
                         % code_neuf)
        uids_mur = [table_uid[v] for v in charge['uids']
                    if table_uid.get(v) is not None]

        def _objet_neuf(v, ou, _mod=objset_modele, _neuf=objset_neuf,
                        _trad=trad_verb.get(indice)):
            """Le meme rang, dans NOTRE objset. None si le bloc surprend.

            `-1` passe tel quel : c'est « pas d'objet ». `ban` s'en sert pour
            dire qu'un panneau n'a pas de version cassee.

            ver.B : le rang se TRADUIT par le nom (`_trad`), ses rangs n'etant
            pas ceux de FS. Un mur n'est pose que si tous ses objets ont une
            traduction (voir `mur_verb`) : un rang absent ici est une faute.
            """
            if v == 0xFFFFFFFF:
                return v
            if v >> 16 != _mod:
                print('REFUS : %s designe l objet %d:%d, qui n est pas de '
                      'l objset du modele (%d). Ce bloc n est pas celui '
                      'qu on croit lire.' % (ou, v >> 16, v & 0xFFFF, _mod))
                return None
            if _trad is not None:
                if (v & 0xFFFF) not in _trad:
                    print('REFUS : %s -- le rang %d n a pas de traduction '
                          'dans ver.B' % (ou, v & 0xFFFF))
                    return None
                return (_neuf << 16) | _trad[v & 0xFFFF]
            return (_neuf << 16) | (v & 0xFFFF)

        off_p, off_u, off_q, off_sup = off_mur[indice]
        a_zero = []
        # Les objets cassables ne se posent QUE si toutes leurs animations
        # existent en 2008. Sinon les deux pointeurs partent a zero -- voir
        # plus bas pourquoi tronquer ne suffit pas.
        o30_impossible = False
        if 'o30' in charge['extra']:
            octets30, nb30 = charge['extra']['o30']
            for j in range(nb30):
                u = struct.unpack_from('<i', octets30,
                                       j * EFFETS_MUR_PAIRE_PAS + 4)[0]
                if u != -1 and table_uid.get(u) is None:
                    o30_impossible = True
        if o30_impossible:
            struct.pack_into('<Q', contenu, d + 0x30, 0)
            struct.pack_into('<Q', contenu, d + 0x38, 0)
            a_zero.append('+0x30/+0x38 (objets cassables)')
        pieces = bytearray(charge['pieces'])
        for j in range(charge['n_pieces']):
            o = j * EFFETS_MUR_PIECE_PAS
            nv = _objet_neuf(struct.unpack_from('<I', pieces, o)[0],
                             '%s : le morceau de mur %d' % (code_neuf, j))
            if nv is None:
                return 2, []
            struct.pack_into('<I', pieces, o, nv)
        contenu[off_p:off_p + len(pieces)] = pieces

        if charge['a_uids']:
            for j, num in enumerate(uids_mur):
                struct.pack_into('<i', contenu, off_u + j * 4, num)
            struct.pack_into('<i', contenu, off_u + len(uids_mur) * 4, -1)

        paires = bytearray(charge['paires'])
        garde = charge['n_paires']
        for j in range(charge['n_paires']):
            o = j * EFFETS_MUR_PAIRE_PAS
            # Une paire dont l'animation n'existe pas en 2008 ne se pose pas :
            # on TRONQUE la liste ici. Pointer sur un uid absent, c'est
            # `TaskEffectWall` qui l'attend pour toujours.
            uids_paire = [struct.unpack_from('<i', paires, o + c)[0]
                          for c in (0x8, 0xC)]
            if any(u != -1 and table_uid.get(u) is None for u in uids_paire):
                garde = j
                struct.pack_into('<i', paires, o, -1)
                break
            for c in (0x0, 0x4):                       # intact, casse
                nv = _objet_neuf(struct.unpack_from('<I', paires, o + c)[0],
                                 '%s : la paire intact/casse %d (+0x%X)'
                                 % (code_neuf, j, c))
                if nv is None:
                    return 2, []
                struct.pack_into('<I', paires, o + c, nv)
            for c in (0x8, 0xC):                       # les deux uid
                anc = struct.unpack_from('<i', paires, o + c)[0]
                if anc != -1:
                    struct.pack_into('<i', paires, o + c, table_uid[anc])
        if garde != charge['n_paires']:
            faits.append('decor neuf : %s garde %d paire(s) intact/casse sur '
                         '%d -- les suivantes demandaient une animation que '
                         '2008 n a pas.'
                         % (code_neuf, garde, charge['n_paires']))
        if charge['a_paires']:
            contenu[off_q:off_q + len(paires)] = paires

        # LES QUATRE BLOCS DE PLUS, substitues de la meme facon.
        def _uid_neuf(v, ou):
            """L'uid correspondant, ou -1 si 2008 n'a pas cette animation."""
            if v == -1:
                return -1
            t = table_uid.get(v)
            return -1 if t is None else t

        etrangers = []

        def _objet_extra(v, ou):
            """Comme `_objet_neuf`, mais TOLERANT dans les blocs de plus.

            `tan` (+0x30) designe l objet 34:545 -- celui de `hai` -- avec ses
            propres uid : l enregistrement de `hai` a ete recopie chez SEGA et
            seul l uid a change. L objset n est pas charge quand on joue `tan`,
            donc l objet ne fait rien -- dans le jeu d origine deja. On recopie
            tel quel : le clone se comporte comme son modele, et on le DIT.
            """
            if v != 0xFFFFFFFF and v >> 16 != objset_modele:
                etrangers.append('%s -> %d:%d' % (ou, v >> 16, v & 0xFFFF))
                return v
            return _objet_neuf(v, ou)

        for nom_bloc, (octets, nb) in sorted(charge['extra'].items()):
            b = bytearray(octets)
            if nom_bloc == 'p20':
                for j in range(nb):
                    o2 = j * EFFETS_MUR_PIECE_PAS
                    nv = _objet_extra(struct.unpack_from('<I', b, o2)[0],
                                      '+0x20 morceau %d' % j)
                    if nv is None:
                        return 2, []
                    struct.pack_into('<I', b, o2, nv)
            elif nom_bloc == 'u28':
                lus = [struct.unpack_from('<i', b, j * 4)[0] for j in range(2)]
                if any(v != -1 and table_uid.get(v) is None for v in lus):
                    # LE POINTEUR A ZERO, PAS UN BLOC TRONQUE : `param_5` est
                    # deroule sur DEUX entrees sans condition ; seule la garde
                    # `if (param_5 != 0)` l'arrete.
                    struct.pack_into('<Q', contenu, d + 0x28, 0)
                    a_zero.append('+0x28 (animation du grillage)')
                    continue
                for j, v in enumerate(lus):
                    struct.pack_into('<i', b, j * 4, _uid_neuf(v, '+0x28'))
            elif nom_bloc in ('o30', 'u38'):
                # LE NOMBRE D'ENREGISTREMENTS NE VIENT PAS DE CE BLOC : c'est
                # `min(nombre de morceaux, 4)`, lu dans `+0x08`. Un terminateur
                # `-1` ne l'arrete donc pas -- le moteur lit le champ +4 de
                # chaque enregistrement, terminateur compris, puis deborde.
                # Si une seule animation manque, on met les DEUX pointeurs a
                # zero : `if (param_6 != 0)` est la seule garde.
                if o30_impossible:
                    continue
                if nom_bloc == 'o30':
                    for j in range(nb):
                        o2 = j * EFFETS_MUR_PAIRE_PAS
                        u = struct.unpack_from('<i', b, o2 + 4)[0]
                        nv = _objet_extra(struct.unpack_from('<I', b, o2)[0],
                                          '+0x30 objet cassable %d' % j)
                        if nv is None:
                            return 2, []
                        struct.pack_into('<I', b, o2, nv)
                        struct.pack_into('<i', b, o2 + 4, _uid_neuf(u, '+0x30'))
                else:
                    for j in range(nb):
                        v = struct.unpack_from('<i', b, j * 4)[0]
                        struct.pack_into('<i', b, j * 4, _uid_neuf(v, '+0x38'))
            o2 = off_sup[nom_bloc]
            contenu[o2:o2 + len(b)] = b
            struct.pack_into('<Q', contenu, d + {'p20': 0x20, 'u28': 0x28,
                                                 'o30': 0x30, 'u38': 0x38}
                             [nom_bloc], va + o2)

        if a_zero:
            faits.append('decor neuf : %s met a ZERO %s -- 2008 n a pas '
                         'l animation, et le moteur ne compte pas ces blocs : '
                         'il en lit min(morceaux, 4) et deborderait.'
                         % (code_neuf, ' et '.join(a_zero)))
        struct.pack_into('<Q', contenu, d + 0x08, va + off_p)
        if charge['a_uids']:
            struct.pack_into('<Q', contenu, d + 0x10, va + off_u)
        if charge['a_paires']:
            struct.pack_into('<Q', contenu, d + 0x18, va + off_q)
        # Leurs relocations sont deja posees : l'entree est un clone du
        # modele, dont ces trois champs sont relogés (verifie plus haut).
        if etrangers:
            faits.append('decor neuf : %s garde tels quels %d objet(s) de mur '
                         'qui designent un AUTRE objset que celui du modele '
                         '(%s) -- c est deja le cas dans le jeu d origine, ou '
                         'l objset n est pas charge non plus.'
                         % (code_neuf, len(etrangers), ' '.join(etrangers)))
        faits.append('decor neuf : le MUR de l entree %d (%s) ne pointe plus '
                     'sur celui de %s : %d morceaux de 0x%X, %d uid, %d '
                     'paire(s), objset %d au lieu de %d, uid %s au lieu de %s.'
                     % (indice, code_neuf, depuis_neuf, charge['n_pieces'],
                        EFFETS_MUR_PIECE_PAS, len(uids_mur),
                        charge['n_paires'], objset_neuf, objset_modele,
                        uids_mur, charge['uids']))
    # les terminateurs, recopies des originaux
    d = off_eff_a3d + (EFFETS_A3D_N + a3d_ajoutes) * EFFETS_A3D_PAS
    contenu[d:d + EFFETS_A3D_PAS] = src_a3d[n_a3d:n_a3d + EFFETS_A3D_PAS]
    d = off_eff_mur + (EFFETS_MUR_N + mur_ajoutes) * EFFETS_MUR_PAS
    contenu[d:d + EFFETS_MUR_PAS] = src_mur[n_mur:n_mur + EFFETS_MUR_PAS]
    for k in range(0, DECORS_TABLE_N * DECORS_TABLE_PAS, 8):
        if DECORS_TABLE_VA + k in relogees:
            a_reloger.append(va + k)
    for k in range(0, DECORS_TABLE_N * DECORS_CODES_PAS, 8):
        if DECORS_CODES_VA + k in relogees:
            a_reloger.append(va + off_codes + k)
    # --- LES DECORS VRAIMENT AJOUTES ---------------------------------------
    if lot and not neufs:
        print('REFUS : un decor ajoute demande au moins une entree neuve. '
              'Passez --decors-table %d ou plus.' % (DECORS_TABLE_N + 1))
        return 2, []
    o = off_chaines + neufs * 4
    for m, code, i, objset, nom_a3d in lot:
        base = i * DECORS_TABLE_PAS
        # les chaines, apres les codes des entrees neuves
        textes = _textes(code, nom_a3d, i)
        adresses = []
        for t in textes:
            brut = t.encode('ascii') + b'\x00'
            if o + len(brut) > besoin:
                print('REFUS : plus de place dans .decors pour « %s »' % t)
                return 2, []
            contenu[o:o + len(brut)] = brut
            adresses.append(va + o)
            o += (len(brut) + 7) & ~7          # aligne : ce sont des cibles
        for champ, adr in zip((0x00, 0x08, 0x48), adresses):
            struct.pack_into('<Q', contenu, base + champ, adr)
            # la relocation est DEJA posee : l'entree est un clone du modele,
            # dont ces trois champs sont relogés. On ne la remet pas.
        struct.pack_into('<I', contenu, base + VARIANTES_DESC_OBJSET, objset)
        # LES CINQ OBJETS : ceux du MODELE, objset substitue, rang inchange.
        objset_m = struct.unpack_from(
            '<I', desc, m * DECORS_TABLE_PAS + VARIANTES_DESC_OBJSET)[0]
        # ET LE RANG DOIT EXISTER DANS L'ARCHIVE POSEE. La generation de 2008
        # n'a pas toujours les cinq : `ban`, `jin` et `are` n'ont pas leur
        # objet `reflect`, qui est une addition de Final Showdown. Un rang
        # absent, c'est un chargement qui ne finit pas ou un decor incomplet,
        # sans un message -- alors qu'un emplacement VIDE (`0xFFFFFFFF`) est
        # une valeur que le jeu porte lui-meme dans onze descripteurs.
        import variantes_5r as _v5r
        ids = _v5r.ids_archive(code if i not in speciaux
                               else speciaux[i]['geo'])
        objets, vides = [], []
        # ver.B : LES CINQ OBJETS VIENNENT DE SON PROPRE DESCRIPTEUR, relu
        # dans l'ELF, et les rangs y sont les siens. Ses champs ne sont pas
        # dans l'ordre de FS -- `variantes_vf5.VERB_ROLE` -- et il n'a pas
        # d'objet RING (le sol le porte). Le ciel des Dural est dans l'objset
        # de ciel, que la liste +0x00 fait charger.
        if i in speciaux:
            # LES CINQ OBJETS ET LES REFLETS D'OBJECTIF VIENNENT DU
            # DESCRIPTEUR DE LA GENERATION, relu dans son binaire et controle
            # par nom (`generation.Generation.descripteur`). ver.B n'a pas
            # d'objet RING (le sol le porte) ; son ciel de Dural est dans
            # l'objset de ciel, que la liste +0x00 fait charger. Les reflets
            # (+0x2C..+0x34) sont des TEXTURES : traduites, et seulement si
            # elles sont dans NOS objsets.
            import generation as _gen_d
            e_d = speciaux[i]
            g_d = _gen_d.generation(e_d['gen'])
            tr_d = trads[i]
            try:
                dv = g_d.descripteur(e_d['cle'])
            except _gen_d.Refus as x:
                print('REFUS : %s' % x)
                return 2, []
            for role in DECOR_NEUF_ROLES:
                v = dv['objets'].get(role, 0xFFFFFFFF)
                if v == 0xFFFFFFFF:
                    objets.append(v)
                    continue
                n_o = tr_d.obj(v)
                if n_o is None:
                    print('REFUS : %s -- l objet %s de %s (%d:%d) n est pas '
                          'dans l archive posee.'
                          % (code, role, g_d.nom, v >> 16, v & 0xFFFF))
                    return 2, []
                objets.append(n_o)
            flares = []
            for t in dv['flares']:
                n_t = None if t == 0xFFFFFFFF else tr_d.tex(t)
                flares.append(0xFFFFFFFF if n_t is None else n_t)
            if 0xFFFFFFFF in flares:
                flares = [0xFFFFFFFF] * 3
            struct.pack_into('<3I', contenu, base + 0x2C, *flares)
            struct.pack_into('<5I', contenu, base + VARIANTES_DESC_OBJETS,
                             *objets)
            faits.append('%s : l entree %d (%s) prend ses objets a son propre '
                         'descripteur : %s ; reflets d objectif %s.'
                         % (g_d.nom, i, code,
                            ' '.join('%s=%s' % (r, '-' if v == 0xFFFFFFFF
                                                else '%d:%d' % (v >> 16,
                                                                v & 0xFFFF))
                                     for r, v in zip(DECOR_NEUF_ROLES,
                                                     objets)),
                            'aucun' if flares[0] == 0xFFFFFFFF else
                            ' '.join(str(x) for x in flares)))
        for k_o, v in enumerate(() if i in speciaux else struct.unpack_from(
                '<5I', desc,
                m * DECORS_TABLE_PAS + VARIANTES_DESC_OBJETS)):
            if v == 0xFFFFFFFF:
                objets.append(v)                     # deja « pas d objet »
                continue
            if v >> 16 != objset_m:
                print('REFUS : le descripteur de %s demande l objet %d:%d, qui '
                      'n est pas de son objset (%d). On ne substitue pas ce '
                      'qu on n a pas compris.'
                      % (DECOR_NOMS[m], v >> 16, v & 0xFFFF, objset_m))
                return 2, []
            rang = v & 0xFFFF
            if ids is not None and rang not in ids:
                objets.append(0xFFFFFFFF)
                vides.append('%s (rang %d)'
                             % (DECOR_NEUF_ROLES[k_o], rang))
                continue
            objets.append((objset << 16) | rang)
        if i not in speciaux:
            struct.pack_into('<5I', contenu, base + VARIANTES_DESC_OBJETS,
                             *objets)
        if ids is None:
            faits.append('decor neuf : l archive de %s n a pas pu etre lue -- '
                         'les cinq rangs sont recopies SANS controle.' % code)
        if vides:
            faits.append('decor neuf : %s n a pas %s dans l archive de 2008 ; '
                         'l emplacement est mis a « pas d objet », comme le '
                         'jeu le fait lui-meme dans onze descripteurs.'
                         % (code, ' ni '.join(vides)))
        # le code a trois lettres de l'entree : on ecrase celui de sa case
        oc = off_chaines + (i - DECORS_TABLE_N) * 4
        contenu[oc:oc + 4] = code.encode('ascii') + b'\x00'
        faits.append('decor neuf : l entree %d porte le code « %s », l objset '
                     '%d, les objets %s, l animation « %s » / « EFF%s » et sa '
                     'collision « rom/STG%s_COLI.000.bin ». Le RESTE vient de '
                     '%s -- les neuf reprises de musique, la table des murs '
                     '+0xC0, les proprietes de rendu, l aire.'
                     % (i, code, objset,
                        ' '.join('-' if v == 0xFFFFFFFF else str(v & 0xFFFF)
                                 for v in objets),
                        nom_a3d, nom_a3d, code.upper(), DECOR_NOMS[m]))

    with open(chemin, 'r+b') as fp:
        fp.seek(off)
        fp.write(bytes(contenu))

    # 4. LES HUIT SITES. new_disp = cible - (champ + 4), le disp32 etant
    #    toujours le dernier champ de l'instruction.
    lots = [(DECORS_TABLE_SITES, va, 'descripteurs'),
            (DECORS_CODES_SITES, va + off_codes, 'codes'),
            (OBJSETS_TABLE_SITES, va + off_objsets, 'objsets'),
            (EFFETS_A3D_SITES, va + off_eff_a3d, 'effets a3d'),
            (EFFETS_MUR_SITES, va + off_eff_mur, 'effets mur'),
            (SON_TABLE_SITES, va + off_son, 'son d ambiance'),
            (DOWN_TABLE_SITES, va + off_down, 'effet down'),
            (MOVE_TABLE_SITES, va + off_move, 'effet move'),
            (SNOW_TABLE_SITES, va + off_snow, 'effet snow')]
    if grille:
        lots.append((GRILLE_TABLE_SITES, va + off_grille, 'grille'))
    for sites, base_neuve, quoi in lots:
        for site in sites:
            # UN SITE PEUT AVOIR DES OCTETS APRES SON disp32. On a longtemps
            # ecrit « le disp32 est toujours le dernier champ de
            # l'instruction » : faux pour `cmp dword ptr [rip+d], 0`, qui porte
            # un immediat d'un octet APRES. Le site le declare, sinon le
            # calcul est decale d'autant -- et le REFUS l'a vu tout de suite.
            champ, dec = site[0], site[1]
            apres = site[2] if len(site) > 2 else 0
            o = offset(orig[DLL], champ)
            with open(orig[DLL], 'rb') as fp:
                fp.seek(o)
                ancien = struct.unpack('<i', fp.read(4))[0]
            source = {'descripteurs': DECORS_TABLE_VA,
                      'codes': DECORS_CODES_VA,
                      'objsets': OBJSETS_TABLE_VA,
                      'effets a3d': EFFETS_A3D_VA,
                      'effets mur': EFFETS_MUR_VA,
                      'son d ambiance': SON_TABLE_VA,
                      'effet down': DOWN_TABLE_VA,
                      'effet move': MOVE_TABLE_VA,
                      'effet snow': SNOW_TABLE_VA,
                      'grille': GRILLE_TABLE_VA}[quoi] + dec
            if champ + 4 + apres + ancien != source:
                print('REFUS : 0x%X ne vise pas 0x%X (il vise 0x%X). Le site '
                      'a bouge, ou refs_plage.py doit etre repasse.'
                      % (champ, source, champ + 4 + apres + ancien))
                return 2, []
            neuf = base_neuve + dec - (champ + 4 + apres)
            if not -0x80000000 <= neuf < 0x80000000:
                print('REFUS : le deplacement de 0x%X ne tient pas sur '
                      '32 bits' % champ)
                return 2, []
            _poser(DLL, o, struct.pack('<i', neuf), champ)

    # 4 ter. RINGOUT_SPLASH : le debut ET la fin (voir RINGOUT_TABLE_VA)
    for champ, ancienne, neuve in (
            (RINGOUT_SITE_DEBUT, RINGOUT_TABLE_VA, va + off_ringout),
            (RINGOUT_SITE_FIN, RINGOUT_TABLE_VA
             + RINGOUT_TABLE_N * RINGOUT_TABLE_PAS,
             va + off_ringout + (RINGOUT_TABLE_N + ro_ajoutes)
             * RINGOUT_TABLE_PAS)):
        o = offset(orig[DLL], champ)
        with open(orig[DLL], 'rb') as fp:
            fp.seek(o)
            ancien = struct.unpack('<i', fp.read(4))[0]
        if champ + 4 + ancien != ancienne:
            print('REFUS : 0x%X ne vise pas 0x%X (il vise 0x%X).'
                  % (champ, ancienne, champ + 4 + ancien))
            return 2, []
        _poser(DLL, o, struct.pack('<i', neuve - (champ + 4)), champ)
    faits.append('effets : le tableau de TaskEffectRingoutSplash (0x%X, %d x '
                 '0x%X, borne par une adresse de FIN litterale) demenage dans '
                 '.decors (+0x%X) avec %d entree(s) de plus ; ses deux `lea` '
                 '(0x%X debut, 0x%X fin) sont repointes.'
                 % (RINGOUT_TABLE_VA, RINGOUT_TABLE_N, RINGOUT_TABLE_PAS,
                    off_ringout, ro_ajoutes, RINGOUT_SITE_DEBUT - 3,
                    RINGOUT_SITE_FIN - 3))

    # 4 bis. LES QUATRE CHAINES DEROULEES DEVIENNENT DES BALAYAGES.
    # C'est le seul endroit de ce correctif ou on reecrit du CODE : ailleurs
    # on ne touche qu'a des disp32. Voir `balayage_chaine`.
    for nom_ch in sorted(CHAINES):
        ou_ch, octets_ch = balayage_chaine(nom_ch, va + off_ch[nom_ch], faits)
        if ou_ch is None:
            print('REFUS : %s' % octets_ch)
            return 2, []
        _poser(DLL, offset(orig[DLL], ou_ch), octets_ch, ou_ch)

    # 5. LES BORNES, et seulement si on depasse 41. A N = 41 le jeu doit se
    #    comporter EXACTEMENT comme avant : c'est tout l'interet de l'etape.
    bornes = 0
    if n > DECORS_TABLE_N:
        for champ, taille, attendu, quoi in DECORS_BORNES:
            o = offset(orig[DLL], champ)
            with open(orig[DLL], 'rb') as fp:
                fp.seek(o)
                brut = fp.read(taille)
            v = int.from_bytes(brut, 'little')
            if v != attendu:
                print('REFUS : borne 0x%X = %d, attendu %d (%s)'
                      % (champ, v, attendu, quoi))
                return 2, []
            # la borne du gestionnaire est un `jae` sur N, celle de la table
            # des codes un `ja` sur N-1 : on garde l ecart d origine.
            neuf = v - DECORS_TABLE_N + n
            if taille == 1 and not 0 <= neuf < 0x80:
                print('REFUS : la borne 0x%X passerait a %d, ce qui ne tient '
                      'plus dans l immediat signe sur un octet de `cmp`. '
                      'Au-dela il faut reassembler l instruction.'
                      % (champ, neuf))
                return 2, []
            _poser(DLL, o, neuf.to_bytes(taille, 'little'), champ)
            bornes += 1
        champ, taille, attendu, quoi = DECORS_BORNE_OCTETS
        o = offset(orig[DLL], champ)
        with open(orig[DLL], 'rb') as fp:
            fp.seek(o)
            v = int.from_bytes(fp.read(taille), 'little')
        if v != attendu:
            print('REFUS : borne 0x%X = 0x%X, attendu 0x%X (%s)'
                  % (champ, v, attendu, quoi))
            return 2, []
        _poser(DLL, o, (n * DECORS_TABLE_PAS).to_bytes(taille, 'little'), champ)
        bornes += 1
        # Les compteurs de parties restent a 41 : leurs deux tableaux sont
        # dimensionnes a 41 DANS une structure, et la 42e entree ecrirait
        # dans le champ suivant. On le DIT, pour que personne ne cherche
        # pourquoi un decor ajoute n a pas de statistiques.
        faits.append('decors : les compteurs de parties (0x1801B648D, '
                     '0x1801B6507) restent bornes a 41 -- leurs tableaux font '
                     'exactement 41 entrees dans la structure (0x1A2EC + '
                     '41*0x10 = 0x1A57C, et le champ suivant commence a '
                     '0x1A580). Les decors ajoutes n auront pas de compteur.')

    if grille:
        # LES QUATRE COMPTES NE SONT PAS TOUCHES. La grille garde 21 cases :
        # le demenagement doit se prouver seul, comme celui des descripteurs.
        # Et une case VIDE serait dangereuse -- son index de decor irait a
        # 0x18018FCF0, dont la garde est `cmp ecx, 0x29 ; jge ret` : elle
        # arrete les index TROP GRANDS, pas les negatifs, et un -1 multiplie
        # par 0xF0 lit AVANT la table. On n'ajoute donc pas de case tant qu'on
        # n'a pas de decor a y mettre.
        faits.append('grille : les %d cases de selection sont deplacees dans '
                     '.decors (+0x%X), cinq sites repointes (dont deux qui '
                     'visent +0x8, le champ d index). Les %d pointeurs d icone '
                     'sont relogés. AUCUN des quatre comptes n est touche : '
                     '0x%X (mov r8d), 0x%X et 0x%X (cmp), 0x%X (cmp rsi, '
                     '21*0x20). La table des bornes liees ne bouge pas -- elle '
                     'n a aucun pointeur, et ce build n utilise pas ce mode.'
                     % (GRILLE_TABLE_N, off_grille, GRILLE_TABLE_N,
                        GRILLE_TABLE_COMPTES[0][0], GRILLE_TABLE_COMPTES[1][0],
                        GRILLE_TABLE_COMPTES[2][0], GRILLE_TABLE_COMPTES[3][0]))
    # ------------------------------------------------------------------
    # UNE RELOCATION SUR UN POINTEUR NUL FABRIQUE UN POINTEUR NON NUL
    #
    # Mesure du 2026-09-10, sur le plantage d'aurora (sonde
    # `analysis/pister_plantage.txt`) : ACCESS_VIOLATION en 0x180084BF0,
    # `mov eax, [rbp+4]` avec rbp = 0x00007FF8892E0000. Or
    #
    #     base du module - 0x180000000 = 0x7FFA092E0000 - 0x180000000
    #                                  = 0x7FF8892E0000   == rbp
    #
    # rbp EST le delta de rebasage. Le champ valait donc ZERO dans le fichier
    # et portait quand meme une relocation : le chargeur y a ajoute le delta,
    # et `if (param_6 != 0)` -- la seule garde -- a laisse passer.
    #
    # C'est le `+0x30`/`+0x38` qu'on met a zero quand 2008 n'a pas l'animation
    # des objets cassables : l'entree de mur est clonee AVEC les relocations du
    # modele, puis le champ est remis a zero -- et la relocation reste.
    #
    # La regle est generale, donc le garde-fou l'est aussi : on retire de la
    # liste toute relocation qui vise un quadruple mot NUL. Mettre un pointeur
    # a zero est notre facon de dire « ce champ n'existe pas » ; une relocation
    # le contredirait a chaque fois.
    nulles = [p for p in a_reloger
              if struct.unpack_from('<Q', contenu, p - va)[0] == 0]
    if nulles:
        a_reloger = [p for p in a_reloger
                     if struct.unpack_from('<Q', contenu, p - va)[0] != 0]
        faits.append('relocations : %d relocation(s) retiree(s) parce que le '
                     'champ vise vaut ZERO (%s). Une relocation sur un '
                     'pointeur nul lui ajoute le delta de rebasage : le champ '
                     'devient non nul, et la garde `if (ptr != 0)` du moteur '
                     'laisse passer un pointeur mort. C est ce qui plantait '
                     'aurora en 0x180084BF0.'
                     % (len(nulles),
                        ' '.join('+0x%X' % (p - va) for p in nulles[:12])
                        + (' ...' if len(nulles) > 12 else '')))
    faits.append('decors : les DEUX tables indexees par le decor sont '
                 'deplacees dans la section .decors (0x%X, %d octets) -- '
                 '%d descripteurs de 0x%X en +0, %d pointeurs de code en '
                 '+0x%X. %d pointeurs recoivent une RELOCATION, recopiee la ou '
                 '.origine en a une : rien n est devine. Huit sites repointes '
                 '(six pour les descripteurs dont un sur +0x70, deux pour les '
                 'codes). %s'
                 % (va, besoin, n, DECORS_TABLE_PAS, n, off_codes,
                    len(a_reloger),
                    ('%d bornes levees a %d decors ; les %d entrees '
                     'neuves sont des CLONES complets de %s (codes %s..%s), '
                     'pointeurs relogés compris -- une entree nulle serait une '
                     'mine, 0x18018F590 dereference +0x00 sur les N'
                     % (bornes, n, neufs, DECOR_NOMS[DECORS_MODELE],
                        DECORS_CODE_NEUF % 0, DECORS_CODE_NEUF % (neufs - 1)))
                    if bornes
                    else 'AUCUNE borne touchee : N reste a 41, le jeu doit se '
                         'comporter exactement comme avant'))
    return 0, a_reloger


# Le journal des octets deja ecrits, et pourquoi il existe.
#
# Chaque correctif verifie les octets qu'il attend -- mais il les verifie dans
# `.origine`, jamais dans le fichier en cours d'ecriture. Deux options peuvent
# donc se disputer la MEME caverne sans qu'aucune ne proteste : la seconde
# ecrase la premiere, et le site d'appel de la premiere saute desormais dans le
# code de la seconde.
#
# Ce n'est pas une hypothese. Le 2026-09-06, `--sp-lancer` (License Challenge,
# caverne 0x1801A71D8) et `--legende-sousmenu` (meme adresse) etaient tous deux
# dans `console.cmd` ; sur la DLL patchee, 0x1801DDE49 et 0x1801DC649
# appelaient la meme caverne, qui ne contenait plus que la legende. License
# Challenge etait casse, sans un seul message.
#
# D'ou ce journal : un octet appartient a un seul correctif, et la collision
# arrete le patch au lieu de produire un binaire silencieusement faux.
_JOURNAL = []


def _poser(nom, o, octets, va=None, reprise=False):
    """Ecrit, et REFUSE si un autre correctif a deja pris ces octets.

    `reprise=True` autorise le recouvrement : c'est le cas d'un correctif qui
    REPREND sciemment le site d'un autre (`--legende-sousmenu` reprend celui de
    `--sousmenu` et saute dans son predicat). Une reprise se declare ; une
    collision s'arrete.
    """
    for nom2, o2, taille2, va2 in _JOURNAL:
        if reprise:
            break
        if nom2 == nom and o2 < o + len(octets) and o < o2 + taille2:
            raise AssertionError(
                'COLLISION dans %s : deux correctifs ecrivent sur les memes '
                'octets -- 0x%X (%d o) contre 0x%X (%d o). Deplacez une des '
                'deux cavernes.'
                % (nom, va if va is not None else o, len(octets),
                   va2 if va2 is not None else o2, taille2))
    _JOURNAL.append((nom, o, len(octets), va))
    with open(os.path.join(JEU, nom), 'r+b') as fp:
        fp.seek(o)
        fp.write(octets)


def origines():
    """Garantit une copie d'origine de chaque binaire, et la rend."""
    out = {}
    for nom in (EXE, DLL):
        chemin = os.path.join(JEU, nom)
        orig = chemin + '.origine'
        if not os.path.exists(orig):
            shutil.copy2(chemin, orig)
            print('original conserve : %s.origine' % nom)
        out[nom] = orig
    return out


def _cfg_verifier(orig):
    """Controle que les cinq instructions sont bien celles qu'on croit."""
    for cle, (nom, va, tete) in CFG_SITES.items():
        o = offset(orig[nom], va)
        if o is None:
            return 'site %s : VA 0x%X hors des sections' % (cle, va)
        with open(orig[nom], 'rb') as fp:
            fp.seek(o)
            vu = fp.read(len(tete))
        if vu != tete:
            return ('site %s a 0x%X : %s au lieu de %s'
                    % (cle, va, vu.hex(), tete.hex()))
    return None


def _cfg_imm(orig, cle):
    """Offset fichier de l'immediat du site (juste apres l'opcode)."""
    nom, va, tete = CFG_SITES[cle]
    return nom, offset(orig[nom], va) + len(tete)


def cfg_lire(orig):
    """Reconstitue les 8 octets de config tels que vfes.exe les produira."""
    cfg = bytearray(8)
    nom, o = _cfg_imm(orig, 'D45')
    with open(os.path.join(JEU, nom), 'rb') as fp:
        fp.seek(o); cfg[0:4] = fp.read(4)
        nom2, o2 = _cfg_imm(orig, 'D77')
        fp.seek(o2); cfg[4:8] = fp.read(4)
        nom3, o3 = _cfg_imm(orig, 'DE7')
        fp.seek(o3); masque = fp.read(1)[0]
        cfg[7] &= masque
        nom4, o4 = _cfg_imm(orig, 'E1C')
        fp.seek(o4); cfg[5] = fp.read(1)[0]
        nom5, o5 = _cfg_imm(orig, 'E32')
        fp.seek(o5); cfg[2] = fp.read(1)[0]
    return bytes(cfg)


def cfg_afficher(cfg, titre):
    e, r, t, d, m, la, fl = (struct.unpack_from('<H', cfg, 0)[0], cfg[2],
                             cfg[3], cfg[4], cfg[5], cfg[6], cfg[7])
    modes = {0: 'console', 1: 'borne', 2: '(troisieme mode)'}
    print('%s : %s' % (titre, ' '.join('%02X' % b for b in cfg)))
    print('    energie %-6d rounds %-3d temps %-4d difficulte %d' % (e, r, t, d))
    print('    game_mode %d = %-18s langue %d' % (m, modes.get(m, '?'), la))
    print('    is_triangle_start %d   is_dural_unlocked %d'
          % (bool(fl & 0x0F), bool(fl & 0xF0)))


def lire():
    orig = origines()
    cfg_afficher(cfg_lire(orig), 'vf5fs_game_config_t en place')
    print()
    print('%-32s %-12s %-14s %s' % ('binaire', 'adresse', 'en place', 'origine'))
    for nom, va, quoi in RESOLUTION:
        chemin = os.path.join(JEU, nom)
        o = offset(orig[nom], va)
        with open(chemin, 'rb') as fp:
            fp.seek(o); a = struct.unpack('<I', fp.read(4))[0]
        with open(orig[nom], 'rb') as fp:
            fp.seek(o); b = struct.unpack('<I', fp.read(4))[0]
        print('%-32s 0x%-10X %-14s %s  (%s)' % (nom, va, a, b, quoi))
    for nom, va, tete, neuf in LANGUE + [LOGO_JP]:
        chemin = os.path.join(JEU, nom)
        o = offset(orig[nom], va)
        with open(chemin, 'rb') as fp:
            fp.seek(o); a = fp.read(len(neuf))
        etat = 'APPLIQUE' if a == neuf else ('origine' if a[:len(tete)] == tete
                                             else 'inconnu')
        print('%-32s 0x%-10X %s' % (nom, va, etat))


def main():
    argv = sys.argv[1:]
    if not argv or '--lire' in argv:
        lire()
        return 0

    orig = origines()
    if '--rendre' in argv:
        for nom in (EXE, DLL):
            shutil.copy2(orig[nom], os.path.join(JEU, nom))
        print('binaires rendus a leur etat d origine')
        return 0

    # on repart TOUJOURS de l'original : les correctifs ne s'empilent pas
    for nom in (EXE, DLL):
        shutil.copy2(orig[nom], os.path.join(JEU, nom))

    faits = []
    if '--resolution' in argv:
        i = argv.index('--resolution')
        larg, haut = int(argv[i + 1]), int(argv[i + 2])
        if not (256 <= larg <= 7680 and 144 <= haut <= 4320):
            print('resolution hors bornes : %dx%d' % (larg, haut))
            return 1
        for nom, va, quoi in RESOLUTION:
            val = larg if quoi == 'largeur' else haut
            o = offset(orig[nom], va)
            _poser(nom, o, struct.pack('<I', val), va)
        faits.append('resolution %d x %d' % (larg, haut))

    for drapeau, points, quoi in (
            ('--langue', LANGUE, 'langue : export (anglais), les DEUX getters'),
            ('--logo-japonais', [LOGO_JP], 'logo : japonais conserve'),
            ('--wxga', [WXGA],
             'affichage WXGA au lieu de VGA -- la grille a alors sa case Dural'),
            ('--dural-grille', DURAL_GRILLE,
             'grille : compositions _dur prises ET case de Dural non desactivee'),
            ('--versus-miroir', [VERSUS_MIROIR],
             'joueur 2 : lit les memes touches que le joueur 1 (palliatif)'),
            ('--menu-fermer', [MENU_FERMER],
             'le menu est demonte sans condition quand on quitte le mode MENU'),
            ('--dojo-cadre', DOJO_CADRE,
             'dojo : le sous-menu emprunte le cadre des OPTIONS, taille pour '
             'cinq lignes'),
            ('--options-sans-howto', OPTIONS_SANS_HOWTO,
             'options : « How to Play » retiree, les quatre autres lignes '
             'decalees (elle vit desormais au Dojo)'),
            ('--options-raccourci', [OPTIONS_RACCOURCI],
             'options : le raccourci « tenir START » ne detourne plus les '
             'validations vers la page d informations'),
            ('--options-tips', options_tips(),
             'options > Settings : la quatrieme ligne devient « Tips » Off/On '
             '(elle etait « Autosave », inerte sur borne) et commande le '
             'conseil des ecrans de chargement'),
            ('--sans-avertissement', [SANS_AVERTISSEMENT],
             'le sous-etat WARNING est saute (ce N EST PAS l ecran '
             'd epilepsie -- essai dementi a l ecran)'),
            ('--sans-epilepsie', SANS_EPILEPSIE,
             'l avertissement sur l epilepsie n est plus dessine sur l ecran '
             'de chargement'),
            ('--menu-exit', MENU_EXIT,
             'menu console : EXIT GAME (entree 9) est affichee, et sa '
             'confirmation ferme le jeu'),

            ('--menu-init', [MENU_INIT],
             'menu console : l attente d initialisation est levee'),
            ('--menu-ranking', [MENU_RANKING],
             'menu console : l attente du classement est levee'),
            ('--menu-service', MENU_SERVICE,
             'menu console : les deux gardes de service sont levees')):
        if drapeau not in argv:
            continue
        for nom, va, tete, neuf in points:
            o = offset(orig[nom], va)
            with open(orig[nom], 'rb') as fp:
                fp.seek(o); avant = fp.read(len(tete))
            if avant != tete:
                print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                      % (va, avant.hex(), tete.hex()))
                return 2
            _poser(nom, o, neuf, va)
        faits.append(quoi)

    # --- vf5fs_game_config_t --------------------------------------------
    demandes = [c for c in CONFIG if '--' + c in argv]
    drapeaux = [d for d in ('--dural', '--triangle') if d in argv]
    if demandes or drapeaux:
        souci = _cfg_verifier(orig)
        if souci:
            print('REFUS, config : %s' % souci)
            return 2
        for champ in demandes:
            site, dec, taille, borne, quoi = CONFIG[champ]
            val = int(argv[argv.index('--' + champ) + 1], 0)
            if not (0 <= val <= borne):
                print('%s hors bornes : %d (0 a %d)' % (champ, val, borne))
                return 1
            nom, o = _cfg_imm(orig, site)
            fmt = '<H' if taille == 2 else '<B'
            with open(os.path.join(JEU, nom), 'r+b') as fp:
                fp.seek(o + dec); fp.write(struct.pack(fmt, val))
            faits.append('%s = %d (%s)' % (champ, val, quoi))
        if drapeaux:
            # L'octet des quartets est ecrit par D77 puis rabote par le
            # `and .., 0xF0` de DE7. On ecrit la valeur voulue et on ouvre
            # le masque, pour que les deux quartets survivent tels quels.
            fl = (0x10 if '--dural' in argv else 0) | \
                 (0x01 if '--triangle' in argv else 0)
            site, dec = CFG_DRAPEAUX
            nom, o = _cfg_imm(orig, site)
            with open(os.path.join(JEU, nom), 'r+b') as fp:
                fp.seek(o + dec); fp.write(bytes([fl]))
                nom2, o2 = _cfg_imm(orig, CFG_MASQUE[0])
                fp.seek(o2 + CFG_MASQUE[1]); fp.write(b'\xFF')
            faits.append('drapeaux = 0x%02X (%s)' % (fl, ', '.join(
                d.lstrip('-') for d in drapeaux)))

    # --- menu console : rendre ses deux tics a la page de menu -----------
    if '--menu-console' in argv:
        o_cave = offset(orig[DLL], MENU_CAVE)
        o_slot = offset(orig[DLL], MENU_VTABLE_C2)
        with open(orig[DLL], 'rb') as fp:
            fp.seek(o_cave); libre = fp.read(64)
            fp.seek(o_slot); slot = struct.unpack('<Q', fp.read(8))[0]
        if any(libre):
            print('REFUS : le rembourrage de .text a 0x%X n est pas vierge'
                  % MENU_CAVE)
            return 2
        if slot != MENU_MAJ:
            print('REFUS : creneau 2 de la vtable = 0x%X, attendu 0x%X'
                  % (slot, MENU_MAJ))
            return 2
        relais = relais_menu(MENU_CAVE)
        with open(os.path.join(JEU, DLL), 'r+b') as fp:
            fp.seek(o_cave); fp.write(relais)
            fp.seek(o_slot); fp.write(struct.pack('<Q', MENU_CAVE))
        faits.append('menu console : relais de %d octets a 0x%X, creneau 2 '
                     'de la vtable repointe' % (len(relais), MENU_CAVE))

    # --- Dural dans la grille de la borne --------------------------------
    if '--dural-grille' in argv or '--dural-grille-rnd' in argv:
        # 0x14 = 20 = DURAL. La valeur 0x13 utilisee jusqu'au 2026-09-04
        # n'ouvrait que TE2 (19) et laissait Dural dehors ; voir le commentaire
        # de GRILLE_BORNES. `--dural-grille-rnd` n'a plus de raison d'etre : la
        # grille de la borne n'a pas de case aleatoire. On le garde comme alias.
        neuf = 0x14
        for nom, va, tete, dec in GRILLE_BORNES:
            o = offset(orig[nom], va)
            with open(orig[nom], 'rb') as fp:
                fp.seek(o); avant = fp.read(len(tete))
            if avant != tete:
                print('REFUS : borne inattendue a 0x%X (%s au lieu de %s)'
                      % (va, avant.hex(), tete.hex()))
                return 2
            with open(os.path.join(JEU, nom), 'r+b') as fp:
                fp.seek(o + dec); fp.write(bytes([neuf]))
        faits.append('grille de la borne : %d bornes portees de 18 a %d '
                     '(Dural comprise)' % (len(GRILLE_BORNES), neuf))

    # --- le decor de l'ecran de personnalisation ---------------------------
    if '--decor-perso' in argv:
        i = argv.index('--decor-perso') + 1
        arg = argv[i] if i < len(argv) else ''
        if arg in DECOR_NOMS:
            n = DECOR_NOMS.index(arg)
        else:
            try:
                n = int(arg, 0)
            except ValueError:
                n = -1
        if not 0 <= n < len(DECOR_NOMS):
            print('--decor-perso attend un indice 0 a %d ou un nom parmi :'
                  % (len(DECOR_NOMS) - 1))
            print('   %s' % ' '.join(DECOR_NOMS))
            return 1
        for nom, va, tete, quoi in DECOR_PERSO_SITES:
            o = offset(orig[nom], va)
            with open(orig[nom], 'rb') as fp:
                fp.seek(o); avant = fp.read(1)
            if avant != tete:
                print('REFUS : octet inattendu a 0x%X (%s), attendu %s -- %s'
                      % (va, avant.hex(), tete.hex(), quoi))
                return 2
            _poser(nom, o, bytes([n]), va)
        faits.append('decor de l ecran de personnalisation : %d (%s) au lieu '
                     'de 1 (ts2) -- les DEUX index, geometrie ET eclairage'
                     % (n, DECOR_NOMS[n]))

    # --- les cinq decors de Dural, a la place de cinq decors existants ------
    if '--decors-dural' in argv:
        i = argv.index('--decors-dural') + 1
        lo = DURAL_DECORS_LO
        if i < len(argv) and not argv[i].startswith('--'):
            arg = argv[i]
            if arg in DECOR_NOMS:
                lo = DECOR_NOMS.index(arg)
            else:
                try:
                    lo = int(arg, 0)
                except ValueError:
                    lo = -1
        if not 0 <= lo <= 16:
            print('--decors-dural attend le PREMIER des cinq decors a '
                  'remplacer : indice 0 a 16, ou son nom parmi')
            print('   %s' % ' '.join(DECOR_NOMS[:17]))
            return 1
        # LA COLLISION QUI M'A COUTE DEUX ESSAIS A L'ECRAN, le 2026-09-08.
        # `--decors-dural cas` translate les indices 7..11 vers 21..25, et
        # **djo vaut 11** : le dojo devenait du5 dans tout combat. Frederic
        # regardait donc du5 en croyant regarder son dojo, et j'ai accuse
        # l'eclairage de VF5 R. `decor_5r_akira.cmd`, qui marche, n'a jamais eu
        # cette option -- c'etait toute la difference entre les deux lanceurs.
        if ('--variantes-djo' in argv
                and lo <= VARIANTES_DJO_INDEX <= lo + 4):
            print('REFUS : --decors-dural %s translate les indices %d..%d vers '
                  'du1..du5, et le dojo (indice %d) est dedans. Le combat '
                  'chargerait du%d au lieu du dojo, et --variantes-djo n aurait '
                  'plus rien a montrer. Choisissez un autre premier decor, ou '
                  'retirez --decors-dural.'
                  % (DECOR_NOMS[lo] if lo < len(DECOR_NOMS) else lo, lo, lo + 4,
                     VARIANTES_DJO_INDEX, VARIANTES_DJO_INDEX - lo + 1))
            return 1
        o = offset(orig[DLL], DURAL_DECORS_VA)
        with open(orig[DLL], 'rb') as fp:
            fp.seek(o)
            avant = fp.read(len(DURAL_DECORS_TETE))
        if avant != DURAL_DECORS_TETE:
            print('REFUS : octets inattendus a 0x%X (%s)'
                  % (DURAL_DECORS_VA, avant.hex()))
            return 2
        code = (bytes([0x83, 0xF8, lo])            # cmp eax, lo
                + bytes([0x7C, 0x08])              # jl  fin
                + bytes([0x83, 0xF8, lo + 4])      # cmp eax, lo+4
                + bytes([0x7F, 0x03])              # jg  fin
                + bytes([0x83, 0xC0, 21 - lo])     # add eax, 21-lo
                + bytes([0xEB, 0x10])              # fin: jmp 0x1800B8B21
                + b'\x90' * 16)
        assert len(code) == len(DURAL_DECORS_TETE), len(code)
        _poser(DLL, o, code, DURAL_DECORS_VA)
        faits.append('decors de Dural : %s -> du1 du2 du3 du4 du5 '
                     '(decor maison de l adversaire ; le bouchon 0x1800B2330 '
                     'qui forcait du2 n est plus appele)'
                     % ' '.join(DECOR_NOMS[lo:lo + 5]))

    # --- les cinq decors de Dural dans la GRILLE de selection ---------------
    if '--decors-dural-grille' in argv:
        va, tete, va2, neuf = DURAL_GRILLE_UPD
        o = offset(orig[DLL], va)
        with open(orig[DLL], 'rb') as fp:
            fp.seek(o)
            avant = fp.read(len(tete))
        if avant != tete:
            print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                  % (va, avant.hex(), tete.hex()))
            return 2
        _poser(DLL, offset(orig[DLL], va2), neuf, va2)

        va, tete, neuf = DURAL_GRILLE_JNE
        o = offset(orig[DLL], va)
        with open(orig[DLL], 'rb') as fp:
            fp.seek(o)
            avant = fp.read(len(tete))
        if avant != tete:
            print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                  % (va, avant.hex(), tete.hex()))
            return 2
        _poser(DLL, o, neuf, va)

        va, tete, va2, neuf = DURAL_GRILLE_CMOVE
        o = offset(orig[DLL], va)
        with open(orig[DLL], 'rb') as fp:
            fp.seek(o)
            avant = fp.read(len(tete))
        if avant != tete:
            print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                  % (va, avant.hex(), tete.hex()))
            return 2
        _poser(DLL, offset(orig[DLL], va2), neuf, va2)

        poses = []
        for va, attendu, neufd, nom in DURAL_GRILLE_CASES:
            o = offset(orig[DLL], va)
            with open(orig[DLL], 'rb') as fp:
                fp.seek(o)
                avant = fp.read(4)
            if avant != struct.pack('<I', attendu):
                print('REFUS : case de grille inattendue a 0x%X (%s, attendu '
                      '%d = %s)'
                      % (va, avant.hex(), attendu, DECOR_NOMS[attendu]))
                return 2
            _poser(DLL, o, struct.pack('<I', neufd), va)
            poses.append('%s->%s' % (nom, DECOR_NOMS[neufd]))
        faits.append('grille des decors : les TROIS substitutions « du1 -> du2 »'
                     ' de l ecran sont levees (0x180174496 l immediat de '
                     'TaskSelStage::update, 0x18017533B le jne, 0x1801753A8 le '
                     'cmove), et quatre cases deviennent %s ; la case dur garde'
                     ' du1, donc les cinq sont dans la grille sans doublon'
                     % ' '.join(poses))

    # `--grille-ajout` a EXISTE et a ete RETIRE le 2026-09-08. Il ajoutait une
    # QUATRIEME LIGNE de cases (du2..du5). Frederic a tranche : ce n'est pas la
    # bonne idee. Une case doit rester UNE case, et le bouton SELECT doit faire
    # defiler les VARIANTES du decor sous le curseur. La mesure qui reste
    # acquise -- 43 cases de place contigue, et une case sans ancre placee par
    # extrapolation -- est consignee dans `analysis/ajouter_un_decor.md` §6.
    if '--grille-ajout' in argv:
        print('REFUS : --grille-ajout a ete retire. Ajouter une 4e ligne de '
              'cases n est pas la bonne forme : une case reste UNE case, et '
              'c est le bouton SELECT qui doit faire defiler les variantes du '
              'decor sous le curseur (--variantes).')
        return 1

    # `--decors-dural-icones` a EXISTE et a ete RETIRE le 2026-09-07 : il
    # repointait le champ +0x18 des cases, qui est l'ancrage de position et non
    # l'icone. Voir le commentaire au-dessus de DURAL_GRILLE_CASES. On refuse
    # explicitement l'option plutot que de l'ignorer en silence, parce qu'elle
    # est encore dans les vieux lanceurs.
    if '--decors-dural-icones' in argv:
        print('REFUS : --decors-dural-icones a ete retire. Le champ +0x18 '
              'd une case n est pas son icone mais son ANCRAGE de position ; '
              'le repointer empile les cases au meme endroit et rend le '
              'curseur incapable de les atteindre. L icone est peinte par la '
              'scene AET SEL_STAGE, elle n est pas dans cette table.')
        return 1

    # --- les variantes d'un decor, au bouton SELECT --------------------------
    if '--variantes' in argv:
        if '--decors-dural-grille' in argv:
            print('REFUS : --variantes et --decors-dural-grille se disputent '
                  'les memes octets, et font le contraire l un de l autre. '
                  'La grille detourne quatre cases ; les variantes en gardent '
                  'UNE et font defiler au SELECT. Choisissez.')
            return 1

        # Les trois substitutions « du1 -> du2 » de l'ecran doivent tomber,
        # sinon du2..du5 rendraient du1 -- ou l'inverse.
        for va, tete, va2, neuf in (DURAL_GRILLE_UPD, DURAL_GRILLE_CMOVE):
            o = offset(orig[DLL], va)
            with open(orig[DLL], 'rb') as fp:
                fp.seek(o)
                avant = fp.read(len(tete))
            if avant != tete:
                print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                      % (va, avant.hex(), tete.hex()))
                return 2
            _poser(DLL, offset(orig[DLL], va2), neuf, va2)
        va, tete, neuf = DURAL_GRILLE_JNE
        o = offset(orig[DLL], va)
        with open(orig[DLL], 'rb') as fp:
            fp.seek(o)
            avant = fp.read(len(tete))
        if avant != tete:
            print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                  % (va, avant.hex(), tete.hex()))
            return 2
        _poser(DLL, o, neuf, va)

        sites = ((VARIANTES_HOOK_VA, VARIANTES_HOOK_TETE, VAR_A),
                 (VARIANTES_HOOK_B_VA, VARIANTES_HOOK_B_TETE, VAR_B))
        for va, tete, _ in sites:
            o = offset(orig[DLL], va)
            with open(orig[DLL], 'rb') as fp:
                fp.seek(o)
                avant = fp.read(len(tete))
            if avant != tete:
                print('REFUS : le point d accroche 0x%X ne porte pas les '
                      'octets attendus (%s au lieu de %s)'
                      % (va, avant.hex(), tete.hex()))
                return 2
        anneaux = [VARIANTES_ANNEAU_DURAL]

        # --- le dojo d'Akira : Final Showdown ET VF5 R, sur la meme case ----
        # L'ANNEAU VERS UN DECOR NEUF. Rien a cloner ni a garder ici : le
        # descripteur a deja ete rempli par `--decor-neuf`, et l'indice
        # n'existe pas dans `.origine` -- la garde « emplacement d essai
        # intact » n'aurait aucun sens.
        if '--variantes-neuf' in argv:
            i = argv.index('--variantes-neuf') + 1
            quel = argv[i] if i < len(argv) else ''
            try:
                idx = int(quel, 0)
            except ValueError:
                print('--variantes-neuf attend l INDICE du decor neuf '
                      '(41 pour la premiere entree ajoutee).')
                return 1
            if idx < DECORS_PREMIER_NEUF:
                print('REFUS : l indice %d ne designe pas un decor ajoute.'
                      % idx)
                if idx == DECORS_INDICE_ALEA:
                    print('L indice %d est RESERVE : c est le code « decor '
                          'aleatoire », teste par EGALITE a sept endroits du '
                          'moteur (0x18013391E, 0x1801744AE, 0x1801748F3, '
                          '0x180174930, 0x180174A4C, 0x18001422D). Un decor '
                          'pose la se fait tirer au sort.'
                          % DECORS_INDICE_ALEA)
                else:
                    print('C est un decor du jeu. Les entrees ajoutees '
                          'commencent a %d.' % DECORS_PREMIER_NEUF)
                return 1
            anneaux.append(variantes_anneau_djo(idx))
            faits.append('variantes : la barre espace fait defiler le dojo '
                         'entre Final Showdown (indice %d) et le decor AJOUTE '
                         'a l indice %d. Aucun emplacement du jeu n est '
                         'recycle.' % (VARIANTES_DJO_INDEX, idx))

        # --- UN ANNEAU PAR DECOR DE VF5 R ----------------------------------
        # La barre espace fait alors passer CHAQUE case de la grille de sa
        # version Final Showdown a sa version VF5 R. C'est le meme mecanisme
        # que pour Dural : le premier indice de l'anneau est la BASE, celui que
        # la case porte naturellement et avec lequel l'apercu se rafraichit.
        if '--variantes-5r' in argv:
            import variantes_5r
            fautes = variantes_5r.controler()
            if fautes:
                print('REFUS : la table de variantes_5r.py a %d faute(s) :'
                      % len(fautes))
                for x in fautes:
                    print('   . %s' % x)
                return 1
            poses = []
            for modele, code, idx, _ in variantes_5r.DECORS_5R:
                if modele not in DECOR_NOMS:
                    print('REFUS : « %s » n est pas un decor du jeu.' % modele)
                    return 1
                base = DECOR_NOMS.index(modele)
                if len(anneaux) >= VARIANTES_MAX_ANNEAUX:
                    print('REFUS : %d anneaux, le maximum est %d. Relevez '
                          'VARIANTES_MAX_ANNEAUX (et GREFFE_TAILLE avec).'
                          % (len(anneaux) + 1, VARIANTES_MAX_ANNEAUX))
                    return 1
                anneaux.append(([base, idx], list(variantes_5r.GENERATIONS)))
                poses.append('%s %d<->%d' % (code, base, idx))
            # LES QUATRE DURAL DE VF5 R rejoignent la case de Dural, apres
            # les cinq de FS (et avant ceux de ver.B, ajoutes plus bas).
            if '--decors-5r-dural' in argv:
                if VARIANTES_MAX_VARIANTES < 16:
                    print('REFUS : --decors-5r-dural porte la case de Dural a '
                          'neuf variantes et plus : il faut --variantes-vf5 '
                          '(seize par anneau).')
                    return 1
                idx_d, noms_d = anneaux[0]
                if idx_d[0] != VARIANTES_ANNEAU_DURAL[0][0]:
                    print('REFUS : le premier anneau n est pas celui de Dural.')
                    return 1
                for (_, code_d, idx_dr, _), lib in zip(
                        variantes_5r.DURAL_5R, variantes_5r.DURAL_5R_LIBELLES):
                    idx_d = list(idx_d) + [idx_dr]
                    noms_d = list(noms_d) + [lib]
                    poses.append('%s du+%d' % (code_d, idx_dr))
                anneaux[0] = (idx_d, noms_d)
            faits.append('variantes : %d anneaux de plus -- la barre espace '
                         'fait passer chaque case de sa version Final Showdown '
                         'a sa version VF5 R (%s). Aucun emplacement du jeu '
                         'n est recycle.' % (len(poses), ' '.join(poses)))

        # --- LE VF5 D'ORIGINE, TROISIEME GENERATION DE CHAQUE CASE ----------
        # Un anneau par case existe deja si `--variantes-5r` est passe : on y
        # AJOUTE la version de 2007, a la suite (FS -> R -> VF5 -> FS). Sinon
        # on le cree. La case de Dural recoit les QUATRE variantes de ver.B
        # a la suite des cinq de Final Showdown -- d'ou les seize variantes par
        # anneau (voir VARIANTES_MAX_VARIANTES).
        if '--variantes-vf5' in argv:
            import variantes_vf5
            fautes = variantes_vf5.controler()
            if fautes:
                print('REFUS : la table de variantes_vf5.py a %d faute(s) :'
                      % len(fautes))
                for x in fautes:
                    print('   . %s' % x)
                return 1
            poses = []
            dural_code = dict((c, lib) for (c, _, _, _, _, _), lib in
                              zip(variantes_vf5.DURAL_VF5,
                                  variantes_vf5.DURAL_LIBELLES))
            for e in variantes_vf5.entrees():
                if e['code'] in dural_code:
                    idx_d, noms_d = anneaux[0]
                    if idx_d[0] != VARIANTES_ANNEAU_DURAL[0][0]:
                        print('REFUS : le premier anneau n est pas celui de '
                              'Dural.')
                        return 1
                    anneaux[0] = (list(idx_d) + [e['indice']],
                                  list(noms_d) + [dural_code[e['code']]])
                    poses.append('%s du1+%d' % (e['code'], e['indice']))
                    continue
                base = DECOR_NOMS.index(e['modele'])
                trouve = False
                for r_a, (idx_a, noms_a) in enumerate(anneaux):
                    if idx_a[0] == base:
                        anneaux[r_a] = (list(idx_a) + [e['indice']],
                                        list(noms_a)
                                        + [variantes_vf5.GENERATION])
                        trouve = True
                        break
                if not trouve:
                    if len(anneaux) >= VARIANTES_MAX_ANNEAUX:
                        print('REFUS : %d anneaux, le maximum est %d.'
                              % (len(anneaux) + 1, VARIANTES_MAX_ANNEAUX))
                        return 1
                    anneaux.append(([base, e['indice']],
                                    ['VIRTUA FIGHTER 5 FS',
                                     variantes_vf5.GENERATION]))
                poses.append('%s %d+%d' % (e['code'], base, e['indice']))
            for idx_a, _ in anneaux:
                if len(idx_a) > VARIANTES_MAX_VARIANTES:
                    print('REFUS : un anneau de %d variantes, le maximum est '
                          '%d.' % (len(idx_a), VARIANTES_MAX_VARIANTES))
                    return 1
            faits.append('variantes : la version du VF5 d origine (ver.B) '
                         's ajoute a %d case(s) (%s). La case de Dural fait '
                         'maintenant %d variantes.'
                         % (len(poses), ' '.join(poses), len(anneaux[0][0])))

        if '--variantes-djo' in argv:
            code, emp = variantes_emplacement(argv)
            if emp < 0:
                print('--variantes-djo attend un code d emplacement parmi :')
                print('   %s' % ' '.join(DECOR_NOMS))
                return 1
            if emp in VARIANTES_EMPLACEMENTS_INTERDITS:
                print('REFUS : emplacement %s (%d) interdit -- %s.'
                      % (code, emp, VARIANTES_EMPLACEMENTS_INTERDITS[emp]))
                print('Un emplacement deja repare ou deja valide n est PAS un '
                      'emplacement libre. Choisissez-en un que rien n a jamais '
                      'touche : tools/emplacements.py le MESURE.')
                return 1
            if len(code) != 3:
                print('REFUS : « %s » ne fait pas trois lettres. Cote fichiers, '
                      'importer_decor.py --vers reecrit les noms internes de '
                      'l archive par substitution EN PLACE : le code d arrivee '
                      'doit avoir exactement la longueur de « djo ». '
                      'Emplacements a trois lettres encore libres : '
                      'tst ts3 wht cid trs.' % code)
                return 1
            base = VARIANTES_DESC_TABLE + emp * VARIANTES_DESC_PAS
            djo = VARIANTES_DESC_TABLE + VARIANTES_DJO_INDEX * VARIANTES_DESC_PAS
            chaine = ('rom/STG%s_COLI.000.bin' % code.upper()).encode() + b'\x00'
            if VARIANTES_COLI_CHAINE_VA + len(chaine) > VARIANTES_COLI_MOU_FIN:
                print('REFUS : la chaine de collision fait %d octets et le mou '
                      'de .rdata s arrete a 0x%X (il commence a 0x%X).'
                      % (len(chaine), VARIANTES_COLI_MOU_FIN,
                         VARIANTES_COLI_CHAINE_VA))
                return 2
            with open(orig[DLL], 'rb') as fp:
                fp.seek(offset(orig[DLL], base))
                emp_avant = fp.read(VARIANTES_DESC_PAS)
                fp.seek(offset(orig[DLL], djo))
                clone = bytearray(fp.read(VARIANTES_DESC_PAS))
                fp.seek(offset(orig[DLL], VARIANTES_COLI_CHAINE_VA))
                mou = fp.read(len(chaine))
            avant = emp_avant[VARIANTES_DESC_OBJETS:VARIANTES_DESC_OBJETS + 20]
            coli = struct.unpack_from('<Q', emp_avant, VARIANTES_DESC_COLI)[0]
            objset = struct.unpack_from('<I', emp_avant,
                                        VARIANTES_DESC_OBJSET)[0]
            # LA GARDE QUI COMPTE : la FORME du descripteur. Un emplacement
            # d'essai intact porte deux objets de son propre objset et trois
            # -1. Un emplacement deja repare -- `trm` l'etait -- ne la passe
            # pas. C'est cette garde, et non une liste de codes, qui empeche de
            # recycler un decor repare.
            if avant != variantes_tete_essai(objset):
                print('REFUS : l emplacement %s (0x%X) ne porte pas les objets '
                      'd un decor d ESSAI intact (%s). Il a deja ete modifie -- '
                      'on ne recycle pas un emplacement repare.'
                      % (code, base, avant.hex()))
                return 2
            if mou != b'\x00' * len(chaine):
                print('REFUS : le mou de .rdata n est pas vide a 0x%X (%s). '
                      'Un autre correctif s y est deja pose -- deux ecritures '
                      'a la meme adresse se detruisent en silence.'
                      % (VARIANTES_COLI_CHAINE_VA, mou.hex()))
                return 2
            # LE CLONAGE. On part du descripteur de djo EN ENTIER : c'est lui
            # qui porte les proprietes de rendu du dojo (+0x2C..+0x34, +0xB8,
            # +0xD0, +0xD4, la taille de l'aire), et c'est leur absence -- pas
            # l'eclairage de VF5 R -- qui ratait l'image.
            struct.pack_into('<I', clone, VARIANTES_DESC_OBJSET, objset)
            struct.pack_into('<5I', clone, VARIANTES_DESC_OBJETS,
                             *[(objset << 16) | r
                               for r in VARIANTES_DJO_RANGS])
            # La collision vient du decor importe, et aucune chaine
            # `rom/STGTRM_COLI...` n'existe : on l'ecrit dans le mou de .rdata.
            _poser(DLL, offset(orig[DLL], VARIANTES_COLI_CHAINE_VA),
                   chaine, VARIANTES_COLI_CHAINE_VA)
            struct.pack_into('<Q', clone, VARIANTES_DESC_COLI,
                             VARIANTES_COLI_CHAINE_VA)
            # Les pointeurs sans relocation chez un decor d'essai : les
            # recopier serait refaire la faute des adresses absolues de la
            # greffe.
            for o in VARIANTES_DESC_SANS_RELOC:
                struct.pack_into('<Q', clone, o, 0)
            _poser(DLL, offset(orig[DLL], base), bytes(clone), base)
            anneaux.append(variantes_anneau_djo(emp))
            faits.append('variantes : le dojo d Akira defile entre Final '
                         'Showdown (indice %d) et VF5 R, AJOUTE sur l '
                         'emplacement libre %s (indice %d). Aucun decor reel n '
                         'est perdu. Le descripteur 0x%X est un CLONE de celui '
                         'de djo -- il fallait les quinze champs, pas trois : '
                         'les proprietes de rendu +0x2C..+0x34, +0xB8, +0xD0 '
                         '(aiguillage), +0xD4 (dix constantes) et l aire 12x12. '
                         'Restent en propre l objset (%d), les cinq objets '
                         '(rangs %s) et la collision importee, ecrite en 0x%X '
                         '(l emplacement pointait 0x%X). Les dix pointeurs sans '
                         'relocation sont mis a zero : seule la musique '
                         'principale joue. L apercu se rafraichit sur la BASE, '
                         'la liste de 0x%X n ayant que 26 entrees.'
                         % (VARIANTES_DJO_INDEX, code, emp, base, objset,
                            ' '.join(str(r) for r in VARIANTES_DJO_RANGS),
                            VARIANTES_COLI_CHAINE_VA, coli,
                            VARIANTES_APERCU_VA))

        greffe_va, greffe_off = ajouter_greffe(DLL)
        # `decors_table()` passe APRES et a besoin de la greffe pour y poser
        # le stub de WATER_RING. On retient donc ou elle est.
        global GREFFE_POSEE
        GREFFE_POSEE = (greffe_va, greffe_off)
        corps = variantes_greffe(greffe_va, '--variantes-texte' in argv,
                                 anneaux)
        if len(corps) > GREFFE_TAILLE:
            print('REFUS : la greffe deborde (%d > %d)'
                  % (len(corps), GREFFE_TAILLE))
            return 2
        _poser(DLL, greffe_off, corps, greffe_va)
        for va, tete, entree in sites:
            saut = (bytes([0xE9])
                    + struct.pack('<i', greffe_va + entree - (va + 5)))
            saut += b'\x90' * (len(tete) - len(saut))
            assert len(saut) == len(tete), (len(saut), len(tete))
            _poser(DLL, offset(orig[DLL], va), saut, va)

        if '--variantes-texte' in argv:
            # Le creneau 4 de TaskSelStage est un bouchon `ret 0` : cet ecran
            # ne dessine rien en propre. On y branche notre dessin, qui sera
            # donc appele a la phase de RENDU -- la seule ou il produise
            # quelque chose. Le creneau est relocalise (type 10), donc y
            # ecrire une adresse d'image suit le rebasage.
            o = offset(orig[DLL], VARIANTES_VTABLE_SLOT_VA)
            with open(orig[DLL], 'rb') as fp:
                fp.seek(o)
                avant = fp.read(8)
            if avant != VARIANTES_VTABLE_SLOT_TETE:
                print('REFUS : le creneau 4 de TaskSelStage (0x%X) ne porte '
                      'pas le bouchon attendu (%s au lieu de %s)'
                      % (VARIANTES_VTABLE_SLOT_VA, avant.hex(),
                         VARIANTES_VTABLE_SLOT_TETE.hex()))
                return 2
            _poser(DLL, o, struct.pack('<Q', greffe_va + VAR_SLOT),
                   VARIANTES_VTABLE_SLOT_VA)
            faits.append('variantes : le nom de la variante est dessine par le '
                         'CRENEAU 4 de TaskSelStage (0x%X), qui etait un '
                         'bouchon `ret 0` -- c est la phase de RENDU, la seule '
                         'ou un dessin produise quelque chose. Depuis l update '
                         '(creneau 2) l appel partait avec des parametres '
                         'parfaits et ne donnait rien.'
                         % VARIANTES_VTABLE_SLOT_VA)

        faits.append('variantes : la barre espace (code 6, canal libre) fait '
                     'defiler du1..du5 sur la case du curseur. DEUX accroches '
                     '- 0x%X lit le bouton et fait tourner le numero, 0x%X '
                     'l applique APRES la recomputation du curseur '
                     '(0x180174781), qui defaisait la premiere version. '
                     'Section greffee en 0x%X. Les trois substitutions '
                     'du1 -> du2 de l ecran sont levees.'
                     % (VARIANTES_HOOK_VA, VARIANTES_HOOK_B_VA, greffe_va))

    # --- la collision manquante de DU2 --------------------------------------
    if '--du2-collision' in argv:
        o = offset(orig[DLL], DU2_COLI_PTR_VA)
        with open(orig[DLL], 'rb') as fp:
            fp.seek(o)
            avant = fp.read(8)
        if avant != DU2_COLI_PTR_TETE:
            print('REFUS : pointeur de collision inattendu a 0x%X (%s au lieu '
                  'de %s)' % (DU2_COLI_PTR_VA, avant.hex(),
                              DU2_COLI_PTR_TETE.hex()))
            return 2
        oc = offset(orig[DLL], DU2_COLI_CHAINE_VA)
        with open(orig[DLL], 'rb') as fp:
            fp.seek(oc)
            avant = fp.read(len(DU2_COLI_CHAINE))
        if avant != b'\x00' * len(DU2_COLI_CHAINE):
            print('REFUS : le mou de .rdata n est pas vide a 0x%X (%s)'
                  % (DU2_COLI_CHAINE_VA, avant.hex()))
            return 2
        _poser(DLL, oc, DU2_COLI_CHAINE, DU2_COLI_CHAINE_VA)
        _poser(DLL, o, struct.pack('<Q', DU2_COLI_CHAINE_VA), DU2_COLI_PTR_VA)
        faits.append('du2 : sa VRAIE collision (rom/STGDU2_COLI.000.bin, 3984 o'
                     ' dans le .par) au lieu de celle de du1 (5744 o) ; la '
                     'chaine manquante est ecrite dans le mou de fin de .rdata')

    # --- un vrai joueur 2 --------------------------------------------------
    if '--joueur2' in argv:
        if '--versus-miroir' in argv:
            print('REFUS : --joueur2 et --versus-miroir touchent le meme site.')
            return 2
        points = [(JOUEUR2_SHL[1], JOUEUR2_SHL[2], JOUEUR2_SHL[3],
                   'shl ebp, 4 : le joueur 2 decale ses codes de seize')]
        for va, tete, code in JOUEUR2_CODES:
            # lea edx, [rbp + code]  puis deux nop
            points.append((va, tete,
                           bytes.fromhex('8d55') + bytes([code]) + b'\x90\x90',
                           None))
        for va, tete, neuf, quoi in points:
            o = offset(orig[DLL], va)
            with open(orig[DLL], 'rb') as fp:
                fp.seek(o); avant = fp.read(len(tete))
            if avant != tete:
                print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                      % (va, avant.hex(), tete.hex()))
                return 2
            _poser(DLL, o, neuf, va)
            if quoi:
                faits.append('joueur 2 : %s' % quoi)
        faits.append('joueur 2 : %d codes rendus relatifs au joueur '
                     '(clavier = 1P, manette = 2P)' % len(JOUEUR2_CODES))

    # --- la transition vers le mode GAME ---------------------------------
    if '--transition-game' in argv:
        corps = transition_cave()
        # la caverne est du remplissage de fin de section : des zeros, pas des
        # `int3`. On l'exige explicitement, pour que le REFUS se declenche si
        # un jour quelque chose s'y installe.
        points = [(TRANSITION_CAVE, b'\x00' * len(corps), corps,
                   'caverne : cree la session, puis demande GAME/SELECTOR'),
                  (TRANSITION_VS_HOOK, TRANSITION_VS_TETE, transition_vs(),
                   'la fin du selecteur demande VS au lieu du menu'),
                  (RETOUR_MENU_HOOK, RETOUR_MENU_TETE, transition_retour_menu(),
                   'apres le combat, retour au MENU et non a l ecran-titre'),
                  (VERSUS_CAVE, b'\x00' * len(transition_versus()),
                   transition_versus(),
                   'caverne versus : enregistre les reglages puis lance'),
                  (VERSUS_HOOK, VERSUS_TETE, transition_versus_hook(),
                   'OFFLINE VERSUS mene au combat'),
                  (DOJO_CAVE, b'\x00' * len(transition_dojo()),
                   transition_dojo(),
                   'caverne dojo : type, mode 6, session, sous-etat 41'),
                  (DOJO_HOOK, DOJO_TETE, transition_dojo_hook(),
                   'DOJO mene a l entrainement'),
                  (SORTIE_CAVE, b'\x00' * len(transition_sortie()),
                   transition_sortie(),
                   'caverne de sortie : Echap (ou BACK) quitte le mode')]
        for va, tete in SORTIE_HOOKS:
            points.append((va, tete,
                           b'\xE8' + struct.pack('<i', SORTIE_CAVE - (va + 5)),
                           'Echap quitte le mode (site 0x%X)' % va))
        if '--sp-menu' not in argv:
            # Le maillon 1 detourne les 27 octets qui ouvraient ARCADE MENU :
            # SINGLE PLAYER va droit a la grille, et les quatre modes (Arcade,
            # Score Attack, License Challenge, Special Sparring) sont
            # court-circuites. `--sp-menu` le laisse en place -- le sous-menu
            # revient, mais plus rien ne mene au combat par cette entree.
            # Voir menu_console.md section 19.
            points.insert(1, (TRANSITION_HOOK, TRANSITION_TETE,
                              transition_menu(),
                              'SINGLE PLAYER appelle la caverne'))
        if '--menu-console' in argv:
            print('REFUS : --menu-console et --transition-game se partagent la '
                  'caverne de .text. Le relais du menu est de toute facon '
                  'supplante par --menu-init.')
            return 2
        for va, tete, neuf, quoi in points:
            o = offset(orig[DLL], va)
            with open(orig[DLL], 'rb') as fp:
                fp.seek(o); avant = fp.read(len(tete))
            if avant != tete:
                print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                      % (va, avant.hex(), tete.hex()))
                return 2
            _poser(DLL, o, neuf, va)
            faits.append('transition : %s (0x%X, %d octets)'
                         % (quoi, va, len(neuf)))

    # --- SINGLE PLAYER : chaque mode lance SON combat --------------------
    if '--sp-lancer' in argv:
        manque = [d_ for d_ in ('--transition-game', '--sp-menu',
                                '--options-sans-howto') if d_ not in argv]
        if manque:
            print('REFUS : --sp-lancer exige %s.' % ' et '.join(manque))
            return 2
        points = []
        vus = set()
        # Avec `--sp-mode`, Score Attack et License Challenge ne passent plus
        # par leur validateur : c'est leur mise a jour qui lance, une fois le
        # mode pose. Leur validateur reste donc d'origine, et leurs deux
        # cavernes se liberent -- `--sp-mode` les reprend telles quelles.
        repris = {'Score Attack', 'License Challenge'} if '--sp-mode' in argv \
            else set()
        for cave, mode, hook, tete, nom in SP_LANCER:
            if nom in repris:
                continue
            corps = sp_lancer_cave(cave, mode)
            for bloc, tete_bloc in (SP_LANCER_BLOC_A, SP_LANCER_BLOC_B):
                if cave == bloc and bloc not in vus:
                    vus.add(bloc)
                    points.append((bloc, tete_bloc, corps,
                                   'caverne %s : lancement (mode non pose)' % nom))
                    break
            else:
                points.append((cave, None, corps,
                               'caverne %s : lancement (mode non pose)' % nom))
            points.append((hook, tete, sp_lancer_hook(hook, cave),
                           'le validateur de %s passe par sa caverne' % nom))
        for va, tete, neuf_, quoi in points:
            o = offset(orig[DLL], va)
            if tete is not None:
                with open(orig[DLL], 'rb') as fp:
                    fp.seek(o); avant = fp.read(len(tete))
                if avant != tete:
                    print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                          % (va, avant.hex(), tete.hex()))
                    return 2
            _poser(DLL, o, neuf_, va)
            faits.append('single player : %s (0x%X, %d octets)'
                         % (quoi, va, len(neuf_)))

    # --- Score Attack et License Challenge lancent LEUR mode --------------
    if '--sp-mode' in argv:
        if '--sp-lancer' not in argv:
            print('REFUS : --sp-mode exige --sp-lancer (il reprend ses '
                  'cavernes et sa caverne de transition).')
            return 2
        points = []
        for cave, tete_cave, setter, hook, tete, nom in SP_MODE:
            points.append((cave, tete_cave, sp_mode_cave(cave, setter),
                           'caverne %s : pose le mode par le setter natif, '
                           'puis lance' % nom))
            points.append((hook, tete, sp_lancer_hook(hook, cave),
                           'la mise a jour de %s passe par sa caverne' % nom))
        for va, tete_, neuf_, quoi in points:
            o = offset(orig[DLL], va)
            if tete_ is not None:
                with open(orig[DLL], 'rb') as fp:
                    fp.seek(o); avant = fp.read(len(tete_))
                if avant != tete_:
                    print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                          % (va, avant.hex(), tete_.hex()))
                    return 2
            _poser(DLL, o, neuf_, va)
            faits.append('mode de jeu : %s (0x%X, %d octets)'
                         % (quoi, va, len(neuf_)))

    # --- Special Sparring lance enfin son combat --------------------------
    if '--sp-sparring' in argv:
        manque = [d_ for d_ in ('--transition-game', '--sp-menu', '--sp-lancer')
                  if d_ not in argv]
        if manque:
            print('REFUS : --sp-sparring exige %s.' % ' et '.join(manque))
            return 2
        if '--options-sans-howto' not in argv:
            print('REFUS : --sp-sparring loge sa greffe dans la queue de la '
                  'caverne How to Play. Sans --options-sans-howto, ces octets '
                  'sont encore executes.')
            return 2
        points = [
            (SP_SPARRING_CAVE, SP_SPARRING_CAVE_TETE,
             sp_sparring_cave(SP_SPARRING_CAVE, SP_SPARRING_SETTER),
             'caverne Special Sparring : pose le mode 3 par le setter natif, '
             'puis saute dans la transition'),
            (SP_SPARRING_SITE, SP_SPARRING_TETE,
             sp_lancer_hook(SP_SPARRING_SITE, SP_SPARRING_CAVE),
             'la mise a jour de Special Sparring passe par sa caverne'),
        ]
        for va, tete_, neuf_, quoi in points:
            o = offset(orig[DLL], va)
            with open(orig[DLL], 'rb') as fp:
                fp.seek(o); avant = fp.read(len(tete_))
            if avant != tete_:
                print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                      % (va, avant.hex(), tete_.hex()))
                return 2
            _poser(DLL, o, neuf_, va)
            faits.append('Special Sparring : %s (0x%X, %d octets)'
                         % (quoi, va, len(neuf_)))

    # --- une quatrieme ligne au Dojo : How to Play -----------------------
    if '--dojo-howto' in argv:
        if '--options-raccourci' not in argv:
            print('REFUS : --dojo-howto pose son relais dans les 82 octets du '
                  'raccourci desactive par --options-raccourci. Sans celui-ci, '
                  'ces octets sont encore executes.')
            return 2
        ca, cb = dojo_howto_cave_a(), dojo_howto_cave_b()
        points = [
            (DOJO_HOWTO_COMPTE[1], DOJO_HOWTO_COMPTE[2], DOJO_HOWTO_COMPTE[3],
             'le menu passe de trois a quatre lignes'),
            (DOJO_HOWTO_CAVE_A, bytes(len(ca)), ca,
             'caverne : le quatrieme libelle, « How to Play »'),
            (DOJO_HOWTO_HOOK_A, DOJO_HOWTO_HOOK_A_TETE, dojo_howto_hook_a(),
             'le dessin appelle la caverne du libelle'),
            (DOJO_HOWTO_CAVE_B, RACCOURCI_CORPS, cb,
             'caverne : l entree 3 ouvre How to Play'),
            (DOJO_HOWTO_HOOK_B, DOJO_HOWTO_HOOK_B_TETE, dojo_howto_hook_b(),
             'l aiguillage passe par le relais'),
        ]
        for va, tete, neuf, quoi in points:
            o = offset(orig[DLL], va)
            with open(orig[DLL], 'rb') as fp:
                fp.seek(o); avant = fp.read(len(tete))
            if avant != tete:
                print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                      % (va, avant.hex(), tete.hex()))
                return 2
            _poser(DLL, o, neuf, va)
            faits.append('dojo : %s (0x%X, %d octets)' % (quoi, va, len(neuf)))

    # --- les sous-menus mangent les directions du menu principal ---------
    if '--sousmenu' in argv:
        if '--menu-ranking' in argv:
            print('REFUS : --sousmenu remplace --menu-ranking. Celui-ci '
                  'retirait le `jne` de la garde du menu principal, ce qui '
                  'laissait les directions traverser les sous-menus. Retirez '
                  '--menu-ranking de la ligne de commande.')
            return 2
        points = [(SOUSMENU_GARDE, SOUSMENU_GARDE_TETE, sousmenu_hook(),
                   'la garde teste l EXISTENCE de la scene, non plus son '
                   'animation'),
                  (SOUSMENU_RANKING[1], SOUSMENU_RANKING[2],
                   SOUSMENU_RANKING[3],
                   'la page RANKING n est plus rangee comme un sous-menu')]
        for va, tete, neuf, quoi in points:
            o = offset(orig[DLL], va)
            with open(orig[DLL], 'rb') as fp:
                fp.seek(o); avant = fp.read(len(tete))
            if avant != tete:
                print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                      % (va, avant.hex(), tete.hex()))
                return 2
            _poser(DLL, o, neuf, va)
            faits.append('sous-menu : %s (0x%X, %d octets)'
                         % (quoi, va, len(neuf)))

    # --- retirer le texte NOW LOADING ---------------------------------------
    if '--sans-now-loading' in argv:
        nom_, va, tete, neuf, quoi = SANS_NOW_LOADING
        o = offset(orig[nom_], va)
        with open(orig[nom_], 'rb') as fp:
            fp.seek(o); avant = fp.read(len(tete))
        if avant != tete:
            print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                  % (va, avant.hex(), tete.hex()))
            return 2
        _poser(nom_, o, neuf, va)
        faits.append('chargement : %s (0x%X, %d octets)' % (quoi, va, len(neuf)))

    # --- couper l attract ramene au titre -----------------------------------
    if '--attract-retour-titre' in argv:
        if '--mode' in argv and argv[argv.index('--mode') + 1] != '0':
            print('REFUS : --attract-retour-titre ne vaut que pour le mode '
                  'console (--mode 0). En mode borne, couper l attract DOIT '
                  'lancer une partie.')
            return 2
        nom_, va, tete, neuf, quoi = ATTRACT_RETOUR_TITRE
        o = offset(orig[nom_], va)
        with open(orig[nom_], 'rb') as fp:
            fp.seek(o); avant = fp.read(len(tete))
        if avant != tete:
            print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                  % (va, avant.hex(), tete.hex()))
            return 2
        _poser(nom_, o, neuf, va)
        faits.append('attract : %s (0x%X, %d octets)' % (quoi, va, len(neuf)))

    # --- la texture du film suit le film ------------------------------------
    if '--film-taille' in argv:
        for nom_, va, tete, neuf, quoi in FILM_TAILLE:
            o = offset(orig[nom_], va)
            with open(orig[nom_], 'rb') as fp:
                fp.seek(o); avant = fp.read(len(tete))
            if avant != tete:
                print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                      % (va, avant.hex(), tete.hex()))
                return 2
            _poser(nom_, o, neuf, va)
            faits.append('film : %s (0x%X, %d octets)' % (quoi, va, len(neuf)))

    # --- les films sont lus en .sfd -----------------------------------------
    if '--film-sfd' in argv:
        nom_, va, tete, neuf, quoi = FILM_SFD
        o = offset(orig[nom_], va)
        with open(orig[nom_], 'rb') as fp:
            fp.seek(o); avant = fp.read(len(tete))
        if avant != tete:
            print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                  % (va, avant.hex(), tete.hex()))
            return 2
        _poser(nom_, o, neuf, va)
        faits.append('film : %s (0x%X, %d octets)' % (quoi, va, len(neuf)))

    # --- l animation de titre longue, meme en console -----------------------
    if '--attract-long' in argv:
        for nom_, va, tete, neuf, quoi in ATTRACT_LONG:
            o = offset(orig[nom_], va)
            with open(orig[nom_], 'rb') as fp:
                fp.seek(o); avant = fp.read(len(tete))
            if avant != tete:
                print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                      % (va, avant.hex(), tete.hex()))
                return 2
            _poser(nom_, o, neuf, va)
            faits.append('attract : %s (0x%X, %d octets)'
                         % (quoi, va, len(neuf)))

    # --- la legende du bas ne se superpose plus -----------------------------
    # Ce bloc REPREND le site de `--sousmenu` : la caverne efface la legende,
    # puis saute dans le meme predicat. Il doit donc passer APRES lui.
    if '--legende-sousmenu' in argv:
        if '--sousmenu' not in argv:
            print('REFUS : --legende-sousmenu reprend le site de --sousmenu '
                  '(0x1801DC649) et saute dans son predicat. Sans lui, la '
                  'garde du menu principal ne serait plus celle qu\'on croit.')
            return 2
        points = [
            (LEGENDE_CAVE, LEGENDE_CAVE_TETE, legende_cave(LEGENDE_CAVE),
             'caverne : efface la legende de la page, puis le predicat'),
            (LEGENDE_SITE, LEGENDE_TETE,
             b'\xE8' + struct.pack('<i', LEGENDE_CAVE - (LEGENDE_SITE + 5)),
             'la garde du menu principal passe par sa caverne'),
        ]
        for va, tete, neuf, quoi in points:
            o = offset(orig[DLL], va)
            with open(orig[DLL], 'rb') as fp:
                fp.seek(o); avant = fp.read(len(tete))
            if avant != tete:
                print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                      % (va, avant.hex(), tete.hex()))
                return 2
            # Le SITE est repris a --sousmenu, sciemment : la caverne saute
            # dans son predicat. La caverne, elle, doit etre a nous seuls.
            _poser(DLL, o, neuf, va, reprise=(va == LEGENDE_SITE))
            faits.append('legende : %s (0x%X, %d octets)'
                         % (quoi, va, len(neuf)))

    # --- le decor du mode DOJO, pose en dur ---------------------------------
    if '--dojo-decor' in argv:
        i = argv.index('--dojo-decor') + 1
        try:
            idx = int(argv[i], 0) if i < len(argv) else -1
        except ValueError:
            idx = -1
        if idx < 0:
            print('--dojo-decor attend un indice de decor. 11 = le dojo '
                  'd origine, 39 = la Training Room ; un decor ajoute commence '
                  'a %d.' % DECORS_PREMIER_NEUF)
            return 1
        if idx == DECORS_INDICE_ALEA:
            print('REFUS : %d est le code « decor aleatoire ».'
                  % DECORS_INDICE_ALEA)
            return 1
        champ, attendu, quoi = DOJO_DECOR_DJO
        o = offset(orig[DLL], champ)
        with open(orig[DLL], 'rb') as fp:
            fp.seek(o)
            v = int.from_bytes(fp.read(4), 'little')
        if v != attendu:
            print('REFUS : 0x%X vaut %d, attendu %d (%s)'
                  % (champ, v, attendu, quoi))
            return 2
        _poser(DLL, o, idx.to_bytes(4, 'little'), champ)
        faits.append('dojo : le mode DOJO charge le decor %d au lieu de %d. Ce '
                     'mode A BIEN un ecran de selection de decor (tranche le 2026-09-10) ; '
                     'ce bloc-ci '
                     'pose l indice en dur en 0x18020AE73 (djo) ou 0x18020AE6E '
                     '(gym, la Training Room), selon un drapeau. Mesure du '
                     '2026-09-09 : la sonde ne montrait qu une demande, '
                     '« index 39 (gym) ».' % (idx, attendu))

    # --- liberer obj_db de l archive EMBARQUEE dans le binaire --------------
    if '--obj-db-libre' in argv:
        champ, attendu, quoi = OBJDB_EMBARQUE
        o = offset(orig[DLL], champ)
        with open(orig[DLL], 'rb') as fp:
            fp.seek(o)
            v = fp.read(1)[0]
        if v != attendu:
            print('REFUS : 0x%X vaut 0x%02X, attendu 0x%02X (%s)'
                  % (champ, v, attendu, quoi))
            return 2
        _poser(DLL, o, bytes([MASQUE_EMBARQUE]), champ)
        faits.append('obj_db : le nom du membre « obj_db.bin » est masque dans '
                     'l ARCHIVE FArC EMBARQUEE (0x1804137F0), un octet. Sans '
                     'cela le moteur lit toujours cette copie-la -- ni le '
                     'fichier pose, ni le .par, meme reecrit -- et un objset '
                     'ajoute reste introuvable. auth_3d_db, lui, n est pas '
                     'embarque : c est pourquoi son masquage suffisait.')

    # --- l ecretage de l indice, et son repli --------------------------------
    if '--decor-ecretage' in argv:
        i = argv.index('--decor-ecretage') + 1
        try:
            n = int(argv[i], 0) if i < len(argv) else -1
        except ValueError:
            n = -1
        if not DECORS_TABLE_N <= n < 0x80:
            print('--decor-ecretage attend un NOMBRE de decors, entre %d et '
                  '127. C est la meme valeur que --decors-table.'
                  % DECORS_TABLE_N)
            return 1
        champ, taille, attendu, quoi = ECRETAGE_BORNE
        o = offset(orig[DLL], champ)
        with open(orig[DLL], 'rb') as fp:
            fp.seek(o)
            v = int.from_bytes(fp.read(taille), 'little')
        if v != attendu:
            print('REFUS : 0x%X vaut %d, attendu %d (%s)'
                  % (champ, v, attendu, quoi))
            return 2
        neuf = v - DECORS_TABLE_N + n
        _poser(DLL, o, neuf.to_bytes(taille, 'little'), champ)
        faits.append('ecretage : l indice de decor est ecrete a %d au lieu de '
                     '%d (0x180203F1E, `cmova ebp, 39`). Sans ce correctif, '
                     'tout indice au-dessus de 40 -- un decor ajoute, mais '
                     'aussi -1, « aucun decor choisi » -- devenait 39, gym, '
                     'AVANT d etre demande. C est ce que la sonde du '
                     '2026-09-09 voyait.' % (neuf, attendu))

    if '--decor-repli' in argv:
        i = argv.index('--decor-repli') + 1
        try:
            idx = int(argv[i], 0) if i < len(argv) else -1
        except ValueError:
            idx = -1
        if idx < 0:
            print('--decor-repli attend un indice de decor : celui qu on veut '
                  'obtenir quand personne n en demande. 39 = gym, la valeur '
                  'd origine ; un decor ajoute commence a %d.'
                  % DECORS_PREMIER_NEUF)
            return 1
        if idx == DECORS_INDICE_ALEA:
            print('REFUS : %d est le code « decor aleatoire », et le repli est '
                  'lu comme un indice, pas comme un code.'
                  % DECORS_INDICE_ALEA)
            return 1
        champ, taille, attendu, quoi = ECRETAGE_REPLI
        o = offset(orig[DLL], champ)
        with open(orig[DLL], 'rb') as fp:
            fp.seek(o)
            v = int.from_bytes(fp.read(taille), 'little')
        if v != attendu:
            print('REFUS : 0x%X vaut %d, attendu %d (%s)'
                  % (champ, v, attendu, quoi))
            return 2
        _poser(DLL, o, idx.to_bytes(taille, 'little'), champ)
        faits.append('repli : quand aucun decor n est demande (-1), le combat '
                     'charge le decor %d au lieu de %d (gym). Le mode DOJO est '
                     'dans ce cas : son appelant pose r9d = -1 en dur '
                     '(0x1801E51FB), et l ecretage non signe de 0x180203F2E en '
                     'faisait gym.' % (idx, attendu))

    # --- LE DEPLACEMENT DES TABLES, EN DERNIER ------------------------------
    # Deux raisons, et elles sont toutes les deux des contraintes de format :
    #   . `.greffe` doit garder 0x180EA1000 -- ses reglages sont documentes a
    #     des adresses fixes -- donc elle est posee avant `.decors` ;
    #   . la table de relocations decrit les sections : elle se reconstruit
    #     quand elles sont toutes la.
    if '--grille-table' in argv and '--decors-table' not in argv:
        print('REFUS : --grille-table demande --decors-table. Les deux tables '
              'partagent la section .decors et la meme reconstruction des '
              'relocations, qui doit etre faite UNE fois, en dernier.')
        return 1
    if '--decors-table' in argv:
        code, a_reloger = decors_table(argv, orig, faits)
        if code:
            return code
        if a_reloger:
            import pe_sections
            rva, taille = pe_sections.reconstruire_relocations(
                os.path.join(JEU, DLL), a_reloger)
            faits.append('relocations : table entiere reecrite en RVA 0x%X '
                         '(%d octets), repertoire de donnees n 5 repointe. '
                         'Sans cela les %d pointeurs deplaces resteraient a la '
                         'base preferee.' % (rva, taille, len(a_reloger)))

    if '--logo-japonais' in argv and '--langue' not in argv:
        print('note : --logo-japonais sans --langue ne change rien de visible,')
        print('       le drapeau global etant deja sur le Japon.')

    print('applique : %s' % (', '.join(faits) if faits else 'rien'))
    if demandes or drapeaux:
        print()
        cfg_afficher(cfg_lire(orig), 'vf5fs_game_config_t desormais')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except AssertionError as souci:
        # Collision de cavernes ou caverne qui deborde : un refus, pas une
        # trace de pile. Le binaire reste celui que main() a deja ecrit, donc
        # incomplet -- le lanceur s'arrete sur le code de retour.
        print()
        print('REFUS : %s' % souci)
        sys.exit(2)
