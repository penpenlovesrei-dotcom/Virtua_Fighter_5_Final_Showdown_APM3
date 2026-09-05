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
# MESURE du 2026-09-05 (tools/pister_sp.cmd), qui a corrige DEUX hypotheses :
#
#     8515.2 ms  MODE CHOISI : 0 (Arcade)
#     8515.4 ms  SCENE DU MODE demarree : OUI
#     8534.0 ms  sous-page = 0x1E75C0E57E8      <- la page de reglages s'ouvre
#     9909.2 ms  sous-page = 0x0                <- effacee 1,4 s plus tard
#
# Tout fonctionne donc ; seul le point de greffe etait faux. La fermeture passe
# par `0x1801A5B70`, le PREMIER des deux tests -- qui ne sont d'ailleurs pas des
# predicats de fin mais des tests d'IDENTITE (`rcx == [0x1807513A8]` ?). Mon
# premier relais, pose sur le second, n'a jamais tourne (0 passage).
#
# Et on ne peut pas se greffer sur la fermeture commune : **valider et annuler
# sont indiscernables**. Les deux gestionnaires de `NORMAL MENU` posent
# `[page+0x308] = 1` et ne different que par leur premiere instruction, le son
# joue -- `0x1801BC010` pour valider, `0x1801BB9D0` pour annuler.
#
# On se greffe donc DANS le validateur, qui ne s'execute que sur « valider ».
# C'est la forme exacte du maillon d'OFFLINE VERSUS (`0x1801DEB12`) : on
# remplace son premier appel par une caverne qui le refait, puis lance.
#
#     0x1801DDE80  NORMAL MENU, creneau +0x50 : VALIDER
#     0x1801DDE89  call 0x1801BC010     <- remplace
#
# La caverne se pose dans le bloc mort du cas « How to Play », libere par
# `--options-sans-howto` : 65 octets, dix-neuf utilises.
SP_LANCER_CAVE = 0x1801A703D
SP_LANCER_CAVE_MAX = 0x1801A707E - 0x1801A703D
# Les QUATRE modes ont chacun leur page de reglages, et leurs validateurs sont
# identiques dans la forme -- tous commencent par le meme `call 0x1801BC010`.
# Une seule caverne suffit donc, avec une greffe de cinq octets par mode :
#
#     0x1801DDE89  NORMAL MENU            (Arcade)             -- VALIDE a l'ecran
#     0x1800A48A9  SCOREATTACK MENU       (Score Attack)
#     0x1801DDE49  LICENCECHALLENGE MENU  (License Challenge)
#
# Special Sparring (mode 3) n'a pas de page a lui : il passe par la fabrique
# `0x1801A5E90`. Il n'est pas traite ici.
SP_LANCER_HOOKS = [
    (0x1801DDE89, bytes.fromhex('e882e1fdff')),
    (0x1800A48A9, bytes.fromhex('e862771100')),
    (0x1801DDE49, bytes.fromhex('e8c2e1fdff')),
]
SP_LANCER_BLOC = bytes.fromhex('8b8360150000')      # la tete du bloc mort
SP_SON_VALIDER = 0x1801BC010


def sp_lancer_cave():
    """Refait l'appel deplace, puis cree la session et demande le combat."""
    def rel(depuis, vers):
        return struct.pack('<i', vers - depuis)
    a = SP_LANCER_CAVE
    c = bytes.fromhex('4883ec28')                       # sub rsp, 0x28
    c += bytes.fromhex('e8') + rel(a + len(c) + 5, SP_SON_VALIDER)
    c += bytes.fromhex('e8') + rel(a + len(c) + 5, TRANSITION_CAVE)
    c += bytes.fromhex('4883c428')                      # add rsp, 0x28
    c += bytes.fromhex('c3')
    if len(c) > SP_LANCER_CAVE_MAX:
        raise AssertionError('caverne sp-lancer debordee : %d > %d'
                             % (len(c), SP_LANCER_CAVE_MAX))
    return c


def sp_lancer_hook(va):
    return (bytes.fromhex('e8')
            + struct.pack('<i', SP_LANCER_CAVE - (va + 5)))


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
            with open(os.path.join(JEU, nom), 'r+b') as fp:
                fp.seek(o); fp.write(struct.pack('<I', val))
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
            with open(os.path.join(JEU, nom), 'r+b') as fp:
                fp.seek(o); fp.write(neuf)
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
            with open(os.path.join(JEU, nom), 'r+b') as fp:
                fp.seek(o); fp.write(bytes([n]))
        faits.append('decor de l ecran de personnalisation : %d (%s) au lieu '
                     'de 1 (ts2) -- les DEUX index, geometrie ET eclairage'
                     % (n, DECOR_NOMS[n]))

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
            with open(os.path.join(JEU, DLL), 'r+b') as fp:
                fp.seek(o); fp.write(neuf)
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
            with open(os.path.join(JEU, DLL), 'r+b') as fp:
                fp.seek(o); fp.write(neuf)
            faits.append('transition : %s (0x%X, %d octets)'
                         % (quoi, va, len(neuf)))

    # --- SINGLE PLAYER : les quatre modes lancent le combat --------------
    if '--sp-lancer' in argv:
        manque = [d_ for d_ in ('--transition-game', '--sp-menu',
                                '--options-sans-howto') if d_ not in argv]
        if manque:
            print('REFUS : --sp-lancer exige %s.' % ' et '.join(manque))
            return 2
        corps = sp_lancer_cave()
        NOMS = {0x1801DDE89: 'Arcade', 0x1800A48A9: 'Score Attack',
                0x1801DDE49: 'License Challenge'}
        points = [(SP_LANCER_CAVE, SP_LANCER_BLOC, corps,
                   'caverne : valider des reglages lance le combat')]
        for va_, tete_ in SP_LANCER_HOOKS:
            points.append((va_, tete_, sp_lancer_hook(va_),
                           'le validateur de %s passe par la caverne'
                           % NOMS[va_]))
        for va, tete, neuf, quoi in points:
            o = offset(orig[DLL], va)
            with open(orig[DLL], 'rb') as fp:
                fp.seek(o); avant = fp.read(len(tete))
            if avant != tete:
                print('REFUS : octets inattendus a 0x%X (%s au lieu de %s)'
                      % (va, avant.hex(), tete.hex()))
                return 2
            with open(os.path.join(JEU, DLL), 'r+b') as fp:
                fp.seek(o); fp.write(neuf)
            faits.append('single player : %s (0x%X, %d octets)'
                         % (quoi, va, len(neuf)))

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
            with open(os.path.join(JEU, DLL), 'r+b') as fp:
                fp.seek(o); fp.write(neuf)
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
            with open(os.path.join(JEU, DLL), 'r+b') as fp:
                fp.seek(o); fp.write(neuf)
            faits.append('sous-menu : %s (0x%X, %d octets)'
                         % (quoi, va, len(neuf)))

    if '--logo-japonais' in argv and '--langue' not in argv:
        print('note : --logo-japonais sans --langue ne change rien de visible,')
        print('       le drapeau global etant deja sur le Japon.')

    print('applique : %s' % (', '.join(faits) if faits else 'rien'))
    if demandes or drapeaux:
        print()
        cfg_afficher(cfg_lire(orig), 'vf5fs_game_config_t desormais')
    return 0


if __name__ == '__main__':
    sys.exit(main())
