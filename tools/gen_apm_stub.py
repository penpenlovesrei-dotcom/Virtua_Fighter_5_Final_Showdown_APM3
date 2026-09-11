#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere un apm.dll de substitution pour faire demarrer vfes.exe hors borne.

vfes.exe importe 57 fonctions d'apm.dll, la bibliotheque de la carte ALLS/APM3.
La vraie apm.dll dialogue avec amdaemon, le demon ALL.Net (reseau, comptabilite,
keychip) : sans lui, le jeu leve amdaemon::Exception et s'arrete. Ce stub remplace
apm.dll par une implementation locale qui repond « tout va bien, partie gratuite ».

Chaque fonction annonce son appel par OutputDebugStringA : tools/instrument.py les
journalise, ce qui donne la sequence d'appels reelle et sert de boucle de mise au point.

ENTREES SCRIPTEES
    Input_isOn et Input_isOnNow sont les seules sources de boutons du jeu a ce
    stade : c'est donc le stub qui tient la manette. Il ne rend plus « rien
    d'appuye » mais joue un scenario lu dans un fichier texte, apm_entrees.txt,
    place a cote de la DLL. Le fichier est relu des qu'il change : on regle une
    sequence sans jamais recompiler.

    Signature reelle, etablie sur la vraie apm.dll :
        char Input_isOn(int code)      code 0..15, un seul argument
    L'appelant passe par un tronc de vtable de vfes.exe (0x140002BE0) qui fait
    « mov ecx, edx ; jmp [Input_isOn] » : le code arrive donc en premier argument.

Le stub n'est ecrit que dans la copie de travail VF5RE\\runtime : le dump n'est pas
touche, et la vraie apm.dll y est conservee sous le nom apm.reelle.dll.

Usage :
    py -3 tools/gen_apm_stub.py            genere et compile
    py -3 tools/gen_apm_stub.py --source   ecrit seulement le source C
"""
import os
import subprocess
import sys

GCC = r'C:\msys64\mingw64\bin\gcc.exe'
MINGW = r'C:\msys64\mingw64\bin'
DST = 'runtime/media/vf5fs'
SRC = 'tools/apm_stub.c'
SCENARIO = 'tools/apm_entrees.txt'

# Les 57 fonctions importees par vfes.exe, avec ce que le stub doit rendre.
#   0   -> renvoie 0 / faux
#   1   -> renvoie 1 / vrai
#   'S' -> renvoie une chaine C statique (le nom sert de valeur)
#   'O' -> fonction a valeur d'objet : rend le pointeur cache recu en rcx
#   'E' -> entree scriptee : ecrite a la main dans ENTETE
FONCTIONS = [
    # Core_execute est le battement de la carte : c'est LA que la vraie apm.dll
    # echantillonne les entrees, une fois par trame. Ecrite a la main.
    ('Core_execute', 'E'), ('Core_isExitNeeded', 0), ('Core_exitGame', 0),

    # sequence de partie : hors test, et on laisse commencer
    ('Sequence_isTest', 'E'), ('Sequence_beginPlay', 1), ('Sequence_continuePlay', 1),
    ('Sequence_endPlay', 0), ('Sequence_getBookkeeping', 0), ('Sequence_clearBackup', 1),

    # credits : partie gratuite, jamais a zero
    ('Credit_isFreePlay', 1), ('Credit_isGameCostEnough', 1), ('Credit_isZero', 0),
    ('Credit_getCredit', 9), ('Credit_getRemain', 9), ('Credit_setCoinInHook', 0),
    ('Credit_toString', 'O'),

    # reseau ALL.Net : authentifie, developpement
    ('AllnetAuth_isGood', 1), ('AllnetAuth_getCountryCode', 'S'),
    ('AllnetAuth_getLocationName', 'S'), ('AllnetAuth_getLocationId', 0),
    ('AllnetAuth_getAbaasLinkServerName', 'S'), ('AllnetAuth_getAbaasGsServerName', 'S'),

    # identite de la carte
    ('System_getGameVersion', 'S'), ('System_getGameId', 'S'),
    ('System_getKeychipId', 'S'), ('System_getBoardId', 'S'),

    # lecteur de carte Aime : absent, rien en cours
    ('Aime_start', 0), ('Aime_cancel', 0), ('Aime_isBusy', 0), ('Aime_hasResult', 0),
    ('Aime_hasConfirm', 0), ('Aime_getConfirm', 0), ('Aime_acceptConfirm', 0),
    ('Aime_hasError', 0), ('Aime_getErrorCategory', 0), ('Aime_getAimeId', 'S'),
    ('Aime_getAccessCode', 'S'), ('Aime_isMobile', 0), ('Aime_isReaderDetected', 0),
    ('Aime_setLedError', 0), ('Aime_setLedSuccess', 0), ('Aime_isDBAlive', 1),

    # sauvegarde
    ('Backup_setupRecords', 1), ('Backup_isSetupSucceeded', 1),
    ('Backup_saveRecord', 1), ('Backup_getRecordStatus', 0),

    # entrees : le scenario tient les boutons
    ('Input_setGamepadConfig', 0), ('Input_isGamepadDetect', 0),
    ('Input_isOn', 'E'), ('Input_isOnNow', 'E'),

    ('Error_isOccurred', 0), ('Error_setDeviceLost', 0),
    ('Emoney_isOpenMainWindow', 0),

    ('ApmSystemSetting_getTimeToClosingTime', 0),
    ('ApmSystemSetting_getMatchingGroup', 0),
    ('ApmSystemSetting_getFixedTitle', 0),
    ('ApmSystemSetting_getAdvertizeSound', 1),
]

# ---------------------------------------------------------------------------
# L'IDENTITE DE LA BORNE, telle que `LinkMain::setup` l'exige.
#
# Le sous-systeme reseau (`am::abaas`, les bornes liees) n'est ni bouchonne ni
# garde par un reglage du jeu : `AbaasManager` est cree sans condition dans
# `module_start`, et `setupLink` (`0x180219BF0`) est RETENTE A CHAQUE TRAME
# tant qu'il echoue. Ses deux seules gardes sont `Sequence_isTest()` faux et
# `AllnetAuth_isGood()` vrai -- auxquelles le stub repondait deja bien.
#
# Ce qui bloquait, c'est la VALIDATION des sept parametres dans
# `ImplLink::setup` (`0x1802C9D20`), qui mesure chaque champ au caractere pres.
# Notre `"0000"` universel n'en satisfaisait qu'un, par hasard :
#
#     +0x30  gameId       taille == 4          "0000" passait
#     +0x58  countryCode  taille == 3, ALPHABETIQUE
#     +0x78  keychipId    taille == 11
#     +0x98  mainId       taille == 11
#
# Et les deux identifiants ne sont PAS des chaines : le moteur lit `+0x22` du
# pointeur rendu. Verifie dans le moteur, pas deduit :
#
#     0x180219D00  call qword ptr [rax + 0x1b0]   ; System_getKeychipId
#     0x180219D06  lea  rcx, [rax + 0x22]         ; <<<
#     0x180219D21  call qword ptr [rax + 0x1a8]   ; System_getBoardId
#     0x180219D27  lea  rcx, [rax + 0x22]         ; <<<
#
# La vraie apm.dll de SEGA rend bien une structure a deux champs
# (`0x180016440`) : 17 octets en `+0x00` (identifiant long) et 12 octets en
# `+0x22` (identifiant court, 11 caracteres + NUL). On refait cette forme.
#
# Les valeurs elles-memes sont libres : le serveur d'appariement, c'est nous.
# Detail : `analysis/reseau_allnet.md`.
#
# L'URI DU SERVEUR : le PREMIER verrou, et je l'avais d'abord laisse de cote.
#
# Mesure du 2026-09-05 (`tools/pister_link.cmd`) : `setupLink` et
# `ImplLink::setup` sont bien atteints -- le reseau est donc reellement tente --
# mais AUCUNE des quatre validations d'identite ne l'est, pas meme `gameId`,
# qui passait pourtant deja. Or un seul test precede `gameId` :
#
#     0x1802C9D97  lea  r13, [rdx + 0x10]
#     0x1802C9D9B  cmp  qword ptr [r13], 0     ; la TAILLE de serverURI
#     0x1802C9DA0  jne  0x1802C9DC8            ; non vide -> on continue
#                  sinon -> "Error: server URI is empty"
#
# Le chemin s'arrete donc la. Et `"0000"` devrait pourtant donner une taille de
# 4 : c'est que le poseur `0x18021A470` ne se contente pas de recopier. Il
# convertit en chaine large par `mbstowcs_s`, et **en cas d'echec il pose une
# chaine par defaut** (`0x18021A50B`, chaine `0x180347568`). Une valeur qui
# n'est pas une URI n'y survit pas.
#
# On donne donc une vraie URI. Le port est ferme tant que le serveur
# d'appariement n'existe pas, mais un refus de connexion sur la boucle locale
# est immediat -- pas de delai d'attente, donc pas de saccade.
# TOUTES LES CHAINES SONT EN UTF-16 -- mesure du 2026-09-05, 25812 echecs sur
# 25812. Nos valeurs arrivaient pourtant intactes au convertisseur
# (`0x18021A470`) : la sonde les a lues en clair, `b'JPN'`, `b'A69E01A8888'`,
# `b'http://127.0.0.1:8080'`. C'est la CONVERSION qui les refusait toutes.
#
# La raison est dans la CRT. `0x18021A470` appelle `0x1803131B8`, dont le corps
# `0x1803130D0` ecrit sa destination OCTET par octet :
#
#     0x1803130F4  test rdx, rdx                ; dst
#     0x180313103  mov  byte ptr [rdx], r14b    ; dst[0] = 0  <- UN SEUL OCTET
#
# La sortie est donc etroite, et l'entree large : ce n'est pas `mbstowcs_s`
# mais **`wcstombs_s`**. Le moteur attend des `const wchar_t *`. L'allocation
# le confirmait deja : `0x18021A4BF` reserve `taille` octets, pas `taille * 2`.
#
# Donne de l'ASCII, `wcstombs_s` lit `"JPN"` comme de l'UTF-16, tombe sur
# 0x504A, et echoue. D'ou les cinq champs a taille 0, `gameId` compris.
#
# La vraie `apm.dll` de SEGA parcourt bien ses chaines en `cmp word ptr
# [rax + r8*2], 0` -- un parcours de `wchar_t`.
# INTERRUPTEUR, et une erreur a ne pas refaire.
#
# Premier essai : passer TOUTES les chaines en UTF-16. Le jeu a plante au
# demarrage, avant meme la pose des points d'arret :
#
#     EXCEPTION STACK_BUFFER_OVERRUN (__fastfail)  a 0x180303B38
#     sortie du processus, code 0xC0000409
#
# Le site est explicite -- ce n'est PAS un debordement de pile :
#
#     0x180303B24  mov  ecx, 0x17
#     0x180303B29  call IsProcessorFeaturePresent(23)
#     0x180303B33  mov  ecx, 5              ; FAST_FAIL_INVALID_ARG
#     0x180303B38  int  0x29                ; __fastfail
#     0x180303B40  mov  edx, 0xC0000417     ; STATUS_INVALID_CRUNTIME_PARAMETER
#
# C'est `_invalid_parameter` de la CRT : une fonction `_s` a recu un argument
# invalide. La faute etait la generalisation : la mesure ne designait que SIX
# fonctions -- celles que la sonde a vues entrer dans le convertisseur
# `0x18021A470`. Les autres (`Aime_*`, `System_getGameVersion`,
# `AllnetAuth_getLocationName`...) sont lues ailleurs comme de l'ASCII, et les
# passer en large casse ces chemins-la.
#
# On ne convertit donc QUE les six du chemin `setupLink`, et l'interrupteur
# reste manuel tant que ce n'est pas valide a l'ecran.
UTF16 = '--utf16' in sys.argv
# Les seules vues entrer dans `0x18021A470` par `tools/pister_link.cmd` :
LARGES = {
    'AllnetAuth_getAbaasLinkServerName',
    'AllnetAuth_getAbaasGsServerName',
    'AllnetAuth_getCountryCode',
    'System_getGameId',
    'System_getKeychipId',
    'System_getBoardId',
}
# Les deux � ServerName � sont des NOMS D'HOTE NUS, pas des URL.
#
# Mesure du 2026-09-06 (`tools/pister_http.py`, point sur `CURLOPT_URL`) : le
# moteur construit lui-meme l'URL en collant trois morceaux, dont deux
# litteraux voisins de la table des chemins --
#     "http://" (0x1805BE118) + <nom> + ":80" (0x1805BE120) + <chemin>
# Avec l'ancienne valeur, libcurl recevait :
#     http://http://127.0.0.1:8080:80/api/turninfo
# et n'atteignait evidemment aucun serveur. D'ou 37 POST emis et zero recu.
#
# Le PORT est donc cable a 80 pour les DEUX bibliotheques : elles partagent le
# meme serveur, et se distinguent par leurs chemins, qui sont disjoints
# (`/api/turninfo`, `/api/match`... pour Link ; `/api/data/*`, `/api/user/*`...
# pour GS). `tools/serveur_allnet.py` ecoute donc sur 80 et choisit la cle
# d'apres le chemin.
CHAINES = {
    'AllnetAuth_getCountryCode': 'JPN',        # 3 lettres, alphabetiques
    'AllnetAuth_getAbaasLinkServerName': '127.0.0.1',
    'AllnetAuth_getAbaasGsServerName': '127.0.0.1',
}
# Les deux qui rendent une STRUCTURE : { char long[0x22]; char court[12]; }
IDENTIFIANTS = {
    'System_getKeychipId': ('A69E01A8888ABCD', 'A69E01A8888'),
    'System_getBoardId':   ('AAVE01A8888ABCD', 'AAVE01A8888'),
}
# `System_getGameVersion` (creneau 56, hote+0x1C0) n'est PAS un getter de
# chaine. Les DEUX sites d'appel du moteur le lisent de la meme facon -- un
# pointeur vers deux entiers 32 bits, `{ major, minor }` :
#
#     0x180219A14  call [rax+0x1C0]              ; -> pointeur
#     0x180219A1A  mov  rax, qword ptr [rax]     ; il lit HUIT octets
#     0x180219A1D  mov  byte ptr [rbp-9],  al    ; majorVersion = octet 0
#     0x180219A20  shr  rax, 0x20
#     0x180219A24  mov  byte ptr [rbp-8],  al    ; minorVersion = octet 4
#
#     0x1800DE298  call [rax+0x1C0]              ; l'evenement `vfes_se_title`
#     0x1800DE2A6  movzx eax, byte ptr [rax]     ; octet 0
#     0x1800DE2AF  movzx eax, byte ptr [rcx+4]   ; octet 4  (NULL tolere)
#
# Le stub rendait `const char *"0000"` : le moteur y lisait 0x30 et 0x00, soit
# la version « 48.00 ». Mesure du 2026-09-06, `analysis/pister_link.txt` :
#
#     2.7 ms  version GS : major=48 minor=0 -> "48.00"
#
# `am::abaas::GsMain::ImplGs::setTitleServerConfig` (`0x1802942A0`) accepte
# pourtant jusqu'a 99 (`cmp al, 0x63 ; jbe`), alors que le formateur qui suit
# n'a qu'un tampon de CINQ octets :
#
#     0x18029E6D7  mov  edx, 5
#     0x18029E6E0  call sprintf_s(buf, 5, "%d.%02d", major, minor)
#
# « 48.00 » demande six octets avec le NUL -> retour -2, ERANGE, et la CRT tue
# le processus par `_invalid_parameter`. Le majeur doit donc rester A UN SEUL
# CHIFFRE : c'est un defaut du binaire d'origine, pas du notre, mais il nous
# borne. L'assertion plus bas le garde.
VERSIONS = {
    'System_getGameVersion': (1, 0),
}

ENTETE = r'''/* apm.dll de substitution -- genere par tools/gen_apm_stub.py, ne pas editer a la main.
 *
 * Remplace la bibliotheque de la carte ALLS/APM3 pour faire demarrer vfes.exe sans
 * amdaemon. Chaque appel est annonce par OutputDebugStringA.
 *
 * Les deux fonctions d'entree jouent un scenario lu dans apm_entrees.txt, place a
 * cote de la DLL. Le fichier est relu des qu'il change : pas de recompilation.
 */
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_PAS   256
#define MAX_CODE   32
#define MAX_NOM    24

static int g_journal;      /* 1 par defaut ; " journal = 0 " dans le scenario
                            * coupe TOUT le journal du stub. Sous debogueur ces
                            * 900 messages par seconde font tomber le jeu de 60
                            * a 25 images par seconde. */

static void journal(const char *nom)
{
    char b[160];
    if (!g_journal) return;
    _snprintf(b, sizeof b, "[apm] %s\n", nom);
    OutputDebugStringA(b);
}

/* Une std::string MSVC vide : tampon SSO de 16 octets, taille 0, capacite 15. */
static void chaine_vide(void *p)
{
    if (!p) return;
    memset(p, 0, 32);
    ((size_t *)p)[3] = 15;
}

/* --------------------------------------------------------------------------
 * Scenario d'entrees
 *
 * Un pas = un instant (ms depuis le premier appel d'entree) et le masque des
 * codes tenus a partir de cet instant. Le dernier pas vaut jusqu'a la fin.
 * -------------------------------------------------------------------------- */

typedef struct { unsigned t_ms; unsigned masque; } Pas;
typedef struct { char nom[MAX_NOM]; int code; } Nom;

static CRITICAL_SECTION g_cs;
static int       g_cs_prete;
static char      g_chemin[MAX_PATH];
static FILETIME  g_ecrit;              /* date du fichier deja charge */
static DWORD     g_dernier_test;       /* GetTickCount du dernier controle */
static Pas       g_pas[MAX_PAS];
static int       g_npas;
static int       g_absent_signale;
static Nom       g_noms[MAX_CODE];
static int       g_nnoms;
static unsigned  g_front = 34;         /* ms pendant lesquelles isOnNow reste vrai */
/* g_journal est declare tout en haut : il commande aussi journal() */
static DWORD     g_t0;                 /* premier appel d'entree */
static int       g_demarre;
static int       g_test;              /* Sequence_isTest : le menu operateur */
static int       g_pas_courant = -1;
static unsigned  g_masque;             /* masque en vigueur */
static unsigned  g_masque_scenario;    /* la part venant du fichier */
static unsigned  g_presse[MAX_CODE];   /* instant du debut d'appui, en ms */

/* --------------------------------------------------------------------------
 * Entrees VIVANTES : clavier et manette
 *
 * Le scenario suffit pour mesurer, pas pour JOUER. Ces deux sources s'ajoutent
 * a lui (elles sont combinees par OU), de sorte qu'un scenario vide laisse la
 * main a l'humain sans rien changer d'autre.
 *
 * La manette est chargee a la demande : lier XInput a l'edition ferait echouer
 * le chargement de la DLL sur une machine qui ne l'a pas.
 * -------------------------------------------------------------------------- */

static int  g_clavier = 1;
static int  g_manette = 1;
/* IMPULSION A USAGE UNIQUE.
 *
 * " impulsion = start " dans le fichier fait presser ces codes pendant
 * g_impulsion_duree millisecondes, **a partir du moment ou la ligne est lue**.
 * C'est ce qui manquait : les pas d'un scenario sont dates depuis le premier
 * sondage d'entree, instant qu'un outil exterieur ne connait pas. Ici il suffit
 * d'ecrire le fichier pour declencher un appui, sans savoir quelle heure il est
 * pour le jeu. Le declencheur est la DATE du fichier : reecrire la meme ligne
 * relance une impulsion. */
static unsigned g_impulsion;        /* les codes a tenir */
static DWORD    g_impulsion_fin;    /* jusqu'a quand, en GetTickCount */
static unsigned g_impulsion_duree = 120;

static unsigned g_montants;    /* ~precedent & courant : vient d'etre presse */
static unsigned g_descendants; /* ~courant & precedent : vient d'etre relache */
static DWORD    g_vif_date;    /* instant du dernier echantillonnage */
static int  g_touche[MAX_CODE];        /* code d'entree -> code virtuel Windows */
static unsigned g_bouton[MAX_CODE];    /* code d'entree -> masque XInput */

/* XInput : boutons du wButtons, plus quatre bits a nous pour les gachettes
 * et le stick gauche, que l'on fabrique dans lire_manette(). */
#define XI_UP 0x0001
#define XI_DOWN 0x0002
#define XI_LEFT 0x0004
#define XI_RIGHT 0x0008
#define XI_START 0x0010
#define XI_BACK 0x0020
#define XI_LB 0x0100
#define XI_RB 0x0200
#define XI_A 0x1000
#define XI_B 0x2000
#define XI_X 0x4000
#define XI_Y 0x8000
#define XI_LT 0x0040           /* fabrique : gachette gauche */
#define XI_RT 0x0080           /* fabrique : gachette droite */

typedef struct { DWORD paquet; WORD boutons; BYTE gl, gr;
                 SHORT gx, gy, dx, dy; } XI_ETAT;
typedef DWORD (WINAPI *XI_GET)(DWORD, XI_ETAT *);
static XI_GET   g_xinput;
static int      g_xinput_tente;

typedef struct { const char *nom; int vk; } Touche;

/* Les noms acceptes a droite de " touche N = ... ". Une seule lettre ou un
 * chiffre valent pour eux-memes. */
static const Touche g_dico[] = {
    {"haut", VK_UP}, {"bas", VK_DOWN}, {"gauche", VK_LEFT}, {"droite", VK_RIGHT},
    {"up", VK_UP}, {"down", VK_DOWN}, {"left", VK_LEFT}, {"right", VK_RIGHT},
    {"entree", VK_RETURN}, {"return", VK_RETURN}, {"enter", VK_RETURN},
    {"espace", VK_SPACE}, {"space", VK_SPACE}, {"echap", VK_ESCAPE},
    {"tab", VK_TAB}, {"maj", VK_SHIFT}, {"ctrl", VK_CONTROL}, {"alt", VK_MENU},
    {"retour", VK_BACK}, {"suppr", VK_DELETE}, {"inser", VK_INSERT},
    {"f1", VK_F1}, {"f2", VK_F2}, {"f3", VK_F3}, {"f4", VK_F4},
    {"f5", VK_F5}, {"f6", VK_F6}, {"f7", VK_F7}, {"f8", VK_F8},
    {"f9", VK_F9}, {"f10", VK_F10}, {"f11", VK_F11}, {"f12", VK_F12},
    {"pave0", VK_NUMPAD0}, {"pave1", VK_NUMPAD1}, {"pave2", VK_NUMPAD2},
    {"pave3", VK_NUMPAD3}, {"pave4", VK_NUMPAD4}, {"pave5", VK_NUMPAD5},
    {"pave6", VK_NUMPAD6}, {"pave7", VK_NUMPAD7}, {"pave8", VK_NUMPAD8},
    {"pave9", VK_NUMPAD9},
    {"rien", 0}, {"aucune", 0},
    {0, 0}
};

static const Touche g_dico_pad[] = {
    {"haut", XI_UP}, {"bas", XI_DOWN}, {"gauche", XI_LEFT}, {"droite", XI_RIGHT},
    {"up", XI_UP}, {"down", XI_DOWN}, {"left", XI_LEFT}, {"right", XI_RIGHT},
    {"a", XI_A}, {"b", XI_B}, {"x", XI_X}, {"y", XI_Y},
    {"lb", XI_LB}, {"rb", XI_RB}, {"lt", XI_LT}, {"rt", XI_RT},
    {"start", XI_START}, {"back", XI_BACK}, {"select", XI_BACK},
    {"rien", 0}, {"aucun", 0},
    {0, 0}
};

static int vk_du_nom(const char *s)
{
    int i;
    char t[MAX_NOM];
    int k = 0;
    while (s[k] && s[k] != ' ' && s[k] != '\t' && k < MAX_NOM - 1) {
        t[k] = (char)tolower((unsigned char)s[k]);
        k++;
    }
    t[k] = 0;
    if (k == 1) {
        if (t[0] >= 'a' && t[0] <= 'z') return (int)(t[0] - 'a' + 'A');
        if (t[0] >= '0' && t[0] <= '9') return (int)t[0];
    }
    for (i = 0; g_dico[i].nom; i++)
        if (!strcmp(g_dico[i].nom, t)) return g_dico[i].vk;
    return -1;
}

static int pad_du_nom(const char *s)
{
    int i;
    char t[MAX_NOM];
    int k = 0;
    while (s[k] && s[k] != ' ' && s[k] != '\t' && k < MAX_NOM - 1) {
        t[k] = (char)tolower((unsigned char)s[k]);
        k++;
    }
    t[k] = 0;
    for (i = 0; g_dico_pad[i].nom; i++)
        if (!strcmp(g_dico_pad[i].nom, t)) return (int)g_dico_pad[i].vk;
    return -1;
}

/* La disposition par defaut, DEUX JOUEURS.
 *
 * Le lecteur d'entrees du moteur (0x180243ED0) ne lisait qu'un joueur : sa
 * boucle sautait toutes les lectures quand l'index de joueur n'etait pas nul,
 * si bien que le masque du joueur 2 valait toujours zero -- d'ou l'ecran de
 * reglages d'OFFLINE VERSUS grise, qui reclame en clair une seconde manette.
 * Le correctif --joueur2 de patch_moteur.py y insere `shl ebp, 4` et rend les
 * codes relatifs au joueur, si bien que le joueur 2 demande le code du joueur
 * 1 PLUS SEIZE.
 *
 * D'ou cette table : codes 0 a 14 pour le joueur 1, au CLAVIER SEUL ; codes
 * 18 a 30 pour le joueur 2, a la MANETTE SEULE. Sans cette separation la
 * manette piloterait les deux joueurs a la fois.
 *
 * Clavier AZERTY : A Z E sous les trois doigts.
 * Codes connus : 0 = TEST, 1 = SERVICE, 7 = START. */
#define P2 16                      /* le decalage du second joueur */

static void disposition_par_defaut(void)
{
    int i;
    for (i = 0; i < MAX_CODE; i++) { g_touche[i] = 0; g_bouton[i] = 0; }
    /* joueur 1 : clavier seul */
    g_touche[0] = VK_F1;                                  /* TEST    */
    g_touche[1] = VK_F2;                                  /* SERVICE */
    g_touche[2] = VK_UP;
    g_touche[3] = VK_DOWN;
    g_touche[4] = VK_LEFT;
    g_touche[5] = VK_RIGHT;
    g_touche[6] = VK_SPACE;                               /* piece   */
    g_touche[7] = VK_RETURN;                              /* START   */
    /* Les quatre boutons de face, disposes comme sur une manette PlayStation.
     * Choix de Frederic (2026-09-05) : la rangee W X C V, qui tombe sous la
     * main gauche en AZERTY -- et `X` pour la croix se retient tout seul.
     * Rappel de ce que le moteur en fait :
     *   code 8  = ANNULER dans les menus (0x1801A2B90 lit ce code, et lui seul)
     *   code 7  = VALIDER dans les menus (0x1801A2BC0)
     *   codes 9, 10, 13, 14 = les boutons de combat (codes logiques 100 a 103) */
    g_touche[8] = 'W';                                    /* carre    []  */
    g_touche[9] = 'X';                                    /* croix    X   */
    g_touche[10] = 'C';                                   /* rond     O   */
    g_touche[11] = 'V';                                   /* triangle /\  */
    g_touche[12] = 'T';                                   /* L1       */
    g_touche[13] = 'Y';                                   /* R1       */
    g_touche[14] = 'U';                                   /* R2       */
    /* code 15 : LA TOUCHE DE SORTIE. Le moteur ne le lit nulle part -- il est
     * libre entre les codes du joueur 1 (0 a 14) et ceux du joueur 2 (18 a
     * 30). Seul le relais --transition-game l'interroge, pour quitter un mode
     * et revenir au menu. N'entrant pas dans la boucle par joueur, il peut
     * avoir les deux sources sans effet de bord. */
    g_touche[15] = VK_ESCAPE; g_bouton[15] = XI_BACK;
    /* joueur 2 : manette seule */
    g_bouton[P2 + 2] = XI_UP;
    g_bouton[P2 + 3] = XI_DOWN;
    g_bouton[P2 + 4] = XI_LEFT;
    g_bouton[P2 + 5] = XI_RIGHT;
    g_bouton[P2 + 6] = XI_BACK;                           /* piece   */
    g_bouton[P2 + 7] = XI_START;                          /* START   */
    g_bouton[P2 + 8] = XI_X;
    g_bouton[P2 + 9] = XI_A;
    g_bouton[P2 + 10] = XI_B;
    g_bouton[P2 + 11] = XI_Y;
    g_bouton[P2 + 12] = XI_LB;
    g_bouton[P2 + 13] = XI_RB;
    g_bouton[P2 + 14] = XI_RT;
}

static unsigned lire_clavier(void)
{
    unsigned m = 0;
    int i;
    if (!g_clavier) return 0;
    /* Le jeu ne doit repondre que s'il a le premier plan : sinon on taperait
     * dans la fenetre du dessus tout en pilotant le jeu par-dessous. */
    {
        DWORD pid = 0;
        HWND f = GetForegroundWindow();
        if (!f) return 0;
        GetWindowThreadProcessId(f, &pid);
        if (pid != GetCurrentProcessId()) return 0;
    }
    for (i = 0; i < MAX_CODE; i++)
        if (g_touche[i] && (GetAsyncKeyState(g_touche[i]) & 0x8000))
            m |= (1u << i);
    return m;
}

static unsigned lire_manette(void)
{
    XI_ETAT e;
    unsigned m = 0;
    unsigned b;
    int i;
    if (!g_manette) return 0;
    if (!g_xinput_tente) {
        HMODULE h;
        g_xinput_tente = 1;
        h = LoadLibraryA("xinput1_4.dll");
        if (!h) h = LoadLibraryA("xinput1_3.dll");
        if (!h) h = LoadLibraryA("xinput9_1_0.dll");
        if (h) g_xinput = (XI_GET)GetProcAddress(h, "XInputGetState");
        OutputDebugStringA(g_xinput ? "[apm] manette : XInput charge\n"
                                    : "[apm] manette : XInput absent\n");
    }
    if (!g_xinput) return 0;
    memset(&e, 0, sizeof e);
    if (g_xinput(0, &e) != 0) return 0;
    b = e.boutons;
    if (e.gl > 60) b |= XI_LT;
    if (e.gr > 60) b |= XI_RT;
    /* le stick gauche vaut la croix : zone morte a un tiers de la course */
    if (e.gy > 10000) b |= XI_UP;
    if (e.gy < -10000) b |= XI_DOWN;
    if (e.gx < -10000) b |= XI_LEFT;
    if (e.gx > 10000) b |= XI_RIGHT;
    for (i = 0; i < MAX_CODE; i++)
        if (g_bouton[i] && (b & g_bouton[i]) == g_bouton[i]) m |= (1u << i);
    return m;
}

static int code_du_nom(const char *s, int n)
{
    int i;
    char t[MAX_NOM];
    if (n <= 0 || n >= MAX_NOM) return -1;
    for (i = 0; i < n; i++) t[i] = (char)tolower((unsigned char)s[i]);
    t[n] = 0;
    if (t[0] >= '0' && t[0] <= '9') return atoi(t);
    for (i = 0; i < g_nnoms; i++)
        if (!strcmp(g_noms[i].nom, t)) return g_noms[i].code;
    return -1;
}

/* Decoupe " start,coin " ou " start + coin " en codes, et rend le masque. */
static unsigned masque_de(const char *s)
{
    unsigned m = 0;
    while (*s) {
        const char *d;
        int c;
        while (*s && (*s == ' ' || *s == '\t' || *s == ',' || *s == '+')) s++;
        d = s;
        while (*s && *s != ' ' && *s != '\t' && *s != ',' && *s != '+') s++;
        if (s == d) break;
        if (s - d == 4 && !_strnicmp(d, "rien", 4)) continue;
        c = code_du_nom(d, (int)(s - d));
        if (c >= 0 && c < MAX_CODE) m |= 1u << c;
    }
    return m;
}

static void charger(void)
{
    HANDLE h;
    WIN32_FILE_ATTRIBUTE_DATA fa;
    DWORD lus = 0, taille;
    char *buf, *p;
    char msg[220];

    if (!GetFileAttributesExA(g_chemin, GetFileExInfoStandard, &fa)) {
        if (!g_absent_signale) {
            g_absent_signale = 1;
            _snprintf(msg, sizeof msg, "[apm] entrees: %s absent, aucun bouton\n",
                      g_chemin);
            OutputDebugStringA(msg);
        }
        return;
    }
    if (fa.ftLastWriteTime.dwLowDateTime == g_ecrit.dwLowDateTime &&
        fa.ftLastWriteTime.dwHighDateTime == g_ecrit.dwHighDateTime)
        return;
    g_ecrit = fa.ftLastWriteTime;

    h = CreateFileA(g_chemin, GENERIC_READ, FILE_SHARE_READ | FILE_SHARE_WRITE,
                    NULL, OPEN_EXISTING, 0, NULL);
    if (h == INVALID_HANDLE_VALUE) return;
    taille = GetFileSize(h, NULL);
    if (taille > 64 * 1024) taille = 64 * 1024;
    buf = (char *)malloc(taille + 1);
    if (!buf) { CloseHandle(h); return; }
    ReadFile(h, buf, taille, &lus, NULL);
    CloseHandle(h);
    buf[lus] = 0;

    g_npas = 0;
    g_nnoms = 0;
    g_front = 34;
    g_journal = 1;
    g_test = 0;
    g_clavier = 1;
    g_manette = 1;
    disposition_par_defaut();     /* pour qu'effacer une ligne la rende bien */
    p = buf;
    while (*p) {
        char *fin = p, *q;
        while (*fin && *fin != '\n') fin++;
        q = fin;
        if (*fin) *fin++ = 0;
        while (q > p && (q[-1] == '\r' || q[-1] == ' ' || q[-1] == '\t')) *--q = 0;
        while (*p == ' ' || *p == '\t') p++;
        if (*p && *p != '#' && *p != ';') {
            if (!_strnicmp(p, "nom", 3) && (p[3] == ' ' || p[3] == '\t')) {
                char n[MAX_NOM];
                int c, i, k = 0;
                char *r = p + 3;
                while (*r == ' ' || *r == '\t') r++;
                while (*r && *r != ' ' && *r != '\t' && *r != '=' && k < MAX_NOM - 1)
                    n[k++] = (char)tolower((unsigned char)*r++);
                n[k] = 0;
                while (*r == ' ' || *r == '\t' || *r == '=') r++;
                c = atoi(r);
                if (k && c >= 0 && c < MAX_CODE && g_nnoms < MAX_CODE) {
                    for (i = 0; i <= k; i++) g_noms[g_nnoms].nom[i] = n[i];
                    g_noms[g_nnoms].code = c;
                    g_nnoms++;
                }
            } else if (!_strnicmp(p, "front", 5)) {
                char *r = p + 5;
                while (*r == ' ' || *r == '\t' || *r == '=') r++;
                g_front = (unsigned)atoi(r);
            } else if (!_strnicmp(p, "test", 4)) {
                char *r = p + 4;
                while (*r == ' ' || *r == '	' || *r == '=') r++;
                g_test = atoi(r);
            } else if (!_strnicmp(p, "journal", 7)) {
                char *r = p + 7;
                while (*r == ' ' || *r == '\t' || *r == '=') r++;
                g_journal = atoi(r);
            } else if (!_strnicmp(p, "impulsion", 9)) {
                char *r = p + 9;
                unsigned m;
                while (*r == ' ' || *r == '	' || *r == '=') r++;
                m = masque_de(r);
                if (m) {
                    DWORD n = GetTickCount();
                    g_impulsion = m;
                    g_impulsion_fin = n + g_impulsion_duree;
                    if (!g_impulsion_fin) g_impulsion_fin = 1;
                }
            } else if (!_strnicmp(p, "duree", 5)) {
                char *r = p + 5;
                while (*r == ' ' || *r == '	' || *r == '=') r++;
                g_impulsion_duree = (unsigned)atoi(r);
            } else if (!_strnicmp(p, "clavier", 7)) {
                char *r = p + 7;
                while (*r == ' ' || *r == '\t' || *r == '=') r++;
                g_clavier = atoi(r);
            } else if (!_strnicmp(p, "manette", 7)) {
                char *r = p + 7;
                while (*r == ' ' || *r == '\t' || *r == '=') r++;
                g_manette = atoi(r);
            } else if (!_strnicmp(p, "touche", 6)
                       && (p[6] == ' ' || p[6] == '\t')) {
                char *r = p + 6;
                int c, vk;
                while (*r == ' ' || *r == '\t') r++;
                c = code_du_nom(r, (int)strcspn(r, " \t="));
                while (*r && *r != ' ' && *r != '\t' && *r != '=') r++;
                while (*r == ' ' || *r == '\t' || *r == '=') r++;
                vk = vk_du_nom(r);
                if (c >= 0 && c < MAX_CODE && vk >= 0) g_touche[c] = vk;
            } else if (!_strnicmp(p, "bouton", 6)
                       && (p[6] == ' ' || p[6] == '\t')) {
                char *r = p + 6;
                int c, b;
                while (*r == ' ' || *r == '\t') r++;
                c = code_du_nom(r, (int)strcspn(r, " \t="));
                while (*r && *r != ' ' && *r != '\t' && *r != '=') r++;
                while (*r == ' ' || *r == '\t' || *r == '=') r++;
                b = pad_du_nom(r);
                if (c >= 0 && c < MAX_CODE && b >= 0) g_bouton[c] = (unsigned)b;
            } else if (*p >= '0' && *p <= '9' && g_npas < MAX_PAS) {
                char *r = p;
                unsigned t = (unsigned)strtoul(p, &r, 10);
                g_pas[g_npas].t_ms = t;
                g_pas[g_npas].masque = masque_de(r);
                g_npas++;
            }
        }
        p = fin;
    }
    free(buf);
    g_pas_courant = -1;
    _snprintf(msg, sizeof msg, "[apm] entrees: %d pas, %d nom(s), front=%u ms\n",
              g_npas, g_nnoms, g_front);
    OutputDebugStringA(msg);
}

/* Prend UN instantane des entrees et en deduit les fronts. Appele sous g_cs.
 *
 * Copie fidele de ce que fait la vraie apm.dll en 0x180013EF0, qui n'a qu'un
 * seul appelant : Core_execute+0xFB. Cinq masques, et le calcul de fronts :
 *
 *     [0x18012B2EC] precedent      [0x18012B2F0] courant   <- Input_isOn
 *     [0x18012B2F4] change         [0x18012B2F8] montants  <- Input_isOnNow
 *     [0x18012B2FC] descendants
 *
 * C'est pour cela que le jeu peut interroger dix-sept fois par trame sans
 * jamais toucher au materiel -- mesure : 13 Input_isOn et 4 Input_isOnNow par
 * appel de Core_execute. */
static void maj(void)
{
    DWORD now;
    unsigned t, avant;
    int i, k;
    char msg[160];

    now = GetTickCount();
    /* Deux cadences, parce qu'il y a deux besoins distincts.
     *
     * 30 ms QUAND UN SCENARIO JOUE : les instants du scenario ne peuvent pas
     * etre plus fins que la relecture. Or les menus appliquent une
     * auto-repetition -- mesure : 80 ms font avancer le curseur de trois
     * lignes, 40 ms de deux, 20 ms d'une seule. A 250 ms, aucune impulsion
     * assez breve n'etait exprimable, et un appui "court" balayait toute la
     * liste pour revenir a son point de depart.
     *
     * 500 ms SINON : quand on joue, le clavier et la manette sont lus a CHAQUE
     * appel, sans passer par le fichier. Celui-ci ne sert plus qu'a changer la
     * disposition -- un geste humain, pour lequel 30 ms est trente fois trop
     * souvent. Le controle reste peu couteux (une seule interrogation de date,
     * la lecture n'a lieu que si le fichier a change), mais inutile est
     * inutile. */
    if (!g_dernier_test
        || now - g_dernier_test > (DWORD)(g_npas > 0 ? 30 : 500)) {
        g_dernier_test = now ? now : 1;
        charger();
    }
    /* L'horloge du scenario part au PREMIER APPEL D'ENTREE, pas au premier
     * battement. Core_execute est appelee des le demarrage du processus, bien
     * avant que le moteur soit charge : y demarrer l'horloge avancait tous les
     * scenarios d'une dizaine de secondes, et le START scripte tombait dans le
     * vide. C'est la regression du 03/09/2026, et c'est pour cela que
     * g_demarre est arme dans entree(). */
    t = g_demarre ? (unsigned)(now - g_t0) : 0u;

    /* 1. la part du scenario, qui ne change qu'aux instants declares */
    if (g_demarre && g_npas > 0) {
        k = -1;
        for (i = 0; i < g_npas; i++) {
            if (g_pas[i].t_ms <= t) k = i; else break;
        }
        if (k != g_pas_courant) {
            g_pas_courant = k;
            g_masque_scenario = (k < 0) ? 0u : g_pas[k].masque;
            _snprintf(msg, sizeof msg,
                      "[apm] entrees: pas %d a t=%u ms, masque=0x%08X\n",
                      k, t, g_masque_scenario);
            OutputDebugStringA(msg);
        }
    } else {
        g_masque_scenario = 0;
    }

    /* 2. les entrees vivantes. Le scenario et l'humain sont combines par OU,
     *    donc un scenario vide ne gene personne. Une seule lecture du materiel
     *    par appel -- et comme cette fonction n'est appelee que par
     *    Core_execute, cela fait une lecture par trame, comme l'originale. */
    if (g_impulsion_fin && (long)(now - g_impulsion_fin) >= 0) {
        g_impulsion = 0;
        g_impulsion_fin = 0;
    }
    avant = g_masque;
    g_masque = g_masque_scenario | g_impulsion
             | lire_clavier() | lire_manette();

    /* 3. les fronts, exactement comme la vraie bibliotheque */
    g_montants = ~avant & g_masque;
    g_descendants = ~g_masque & avant;
    g_vif_date = now ? now : 1;
    /* les instants d'appui, dont se sert la fenetre de temps d'Input_isOnNow */
    for (i = 0; i < MAX_CODE; i++)
        if (g_montants & (1u << i)) g_presse[i] = t;
    if (g_montants || g_descendants) {
        _snprintf(msg, sizeof msg,
                  "[apm] fronts: courant=0x%08X montants=0x%08X descendants=0x%08X\n",
                  g_masque, g_montants, g_descendants);
        OutputDebugStringA(msg);
    }
    (void)t;
}

/* Le battement de la carte. C'est ici, et NULLE PART AILLEURS, que les entrees
 * sont echantillonnees -- comme dans la vraie apm.dll. */
__declspec(dllexport) long long Core_execute(void)
{
    journal("Core_execute");
    if (g_cs_prete) {
        EnterCriticalSection(&g_cs);
        maj();
        LeaveCriticalSection(&g_cs);
    }
    return 0;
}

static char entree(const char *nom, int code, int front_seul)
{
    char r = 0;
    char msg[96];
    if (!g_cs_prete) return 0;
    EnterCriticalSection(&g_cs);
    if (!g_demarre) { g_t0 = GetTickCount(); g_demarre = 1; }
    /* Aucun echantillonnage ici : on lit l'instantane pris par Core_execute.
     * Deux garde-fous seulement :
     *   - le tout premier appel, si le jeu interroge avant le premier battement ;
     *   - un battement qui s'arrete (chargement, gel) : au-dela de 50 ms sans
     *     instantane, on en prend un, pour ne pas rendre le jeu insensible.
     * Hors de ces deux cas, la valeur est stable sur toute la trame -- et
     * Input_isOnNow ne vaut vrai que sur LA trame du front, comme l'original. */
    {
        DWORD now = GetTickCount();
        if (!g_vif_date || now - g_vif_date > 50) maj();
    }
    if (code >= 0 && code < MAX_CODE && (g_masque & (1u << code))) {
        if (!front_seul) r = 1;
        else {
            /* FENETRE DE TEMPS, et non bit de front.
             *
             * La vraie apm.dll fait un vrai front d'une trame (voir
             * docs/formats/apm_input.md) et j'ai essaye de la copier : le jeu
             * n'a plus jamais quitte APM3_ENTRY. Mesure : le front EST calcule
             * (montants=0x80 deux fois pour les deux START du scenario) et
             * Input_isOnNow(7) est appele 2660 fois, mais il ne rend JAMAIS
             * vrai. Le consommer a la lecture n'a rien change non plus. La
             * cause reste a etablir -- probablement une histoire de fils, le
             * jeu interrogeant les entrees ailleurs que la ou il bat.
             *
             * On garde donc la fenetre de temps, qui marche. Elle dure
             * g_front = 34 ms, soit deux trames au lieu d'une : c'est un ecart
             * connu et mesure avec l'original, pas un oubli. */
            unsigned tt = (unsigned)(GetTickCount() - g_t0);
            r = (tt - g_presse[code] < g_front) ? 1 : 0;
        }
    }

    if (g_journal) {
        _snprintf(msg, sizeof msg, "[apm] %s(%d)%s\n", nom, code, r ? " = OUI" : "");
        OutputDebugStringA(msg);
    }
    LeaveCriticalSection(&g_cs);
    return r;
}

/* Le menu operateur SEGA. Le jeu appelle Sequence_isTest environ 60 fois par
 * seconde ; rendre vrai le fait demarrer dans le menu de test, dont l'ecran de
 * test d'entrees NOMME chaque signal. Pilote par " test = 1 " dans le scenario,
 * pour ne pas avoir a recompiler. */
__declspec(dllexport) long long Sequence_isTest(void)
{
    if (g_cs_prete) {
        EnterCriticalSection(&g_cs);
        maj();
        LeaveCriticalSection(&g_cs);
    }
    return g_test;
}

__declspec(dllexport) char Input_isOn(int code)
{ return entree("Input_isOn", code, 0); }

__declspec(dllexport) char Input_isOnNow(int code)
{ return entree("Input_isOnNow", code, 1); }

BOOL WINAPI DllMain(HINSTANCE h, DWORD r, LPVOID x)
{
    (void)x;
    if (r == DLL_PROCESS_ATTACH) {
        char *s;
        InitializeCriticalSection(&g_cs);
        g_cs_prete = 1;
        g_journal = 1;
        GetModuleFileNameA(h, g_chemin, MAX_PATH);
        s = strrchr(g_chemin, '\\');
        if (s) s[1] = 0; else g_chemin[0] = 0;
        strncat(g_chemin, "apm_entrees.txt", MAX_PATH - strlen(g_chemin) - 1);
        OutputDebugStringA("[apm] stub charge\n");
    }
    return TRUE;
}

'''


def source():
    out = [ENTETE]
    for nom, val in FONCTIONS:
        if val == 'E':
            continue                                  # ecrite a la main dans ENTETE
        if val == 'S' and nom in VERSIONS:
            # Deux entiers 32 bits, JAMAIS une chaine : le moteur lit l'octet
            # +0 et l'octet +4. Le majeur reste a un chiffre, sinon le
            # `sprintf_s(buf, 5, ...)` de `0x18029E6E0` deborde et tue le jeu.
            maj, mnr = VERSIONS[nom]
            assert 0 <= maj <= 9, '%s : le majeur doit tenir en un chiffre' % nom
            assert 0 <= mnr <= 99, '%s : le mineur doit tenir en deux chiffres' % nom
            out.append(
                'static const unsigned int %s_v[2] = { %du, %du };'
                '   /* major, minor */\n'
                '__declspec(dllexport) const void *%s(void)\n'
                '{ journal("%s"); return %s_v; }\n\n'
                % (nom, maj, mnr, nom, nom, nom))
        elif val == 'S' and nom in IDENTIFIANTS:
            # Une STRUCTURE, pas une chaine : le moteur lit son champ +0x22.
            longue, courte = IDENTIFIANTS[nom]
            assert len(courte) == 11, '%s : le champ +0x22 doit faire 11' % nom
            typ, pre = (('wchar_t', 'L') if (UTF16 and nom in LARGES)
                        else ('char', ''))
            out.append(
                'static struct { char longue[0x22]; %s courte[12]; } %s_id ='
                '\n    { "%s", %s"%s" };\n'
                '__declspec(dllexport) const void *%s(void)\n'
                '{ journal("%s"); return &%s_id; }\n\n'
                % (typ, nom, longue, pre, courte, nom, nom, nom))
        elif val == 'S':
            valeur = CHAINES.get(nom, '0000')
            typ, pre = (('wchar_t', 'L') if (UTF16 and nom in LARGES)
                        else ('char', ''))
            out.append(
                '__declspec(dllexport) const %s *%s(void)\n'
                '{ journal("%s"); return %s"%s"; }\n\n'
                % (typ, nom, nom, pre, valeur))
        elif val == 'O':
            out.append(
                '__declspec(dllexport) void *%s(void *ret)\n'
                '{ journal("%s"); chaine_vide(ret); return ret; }\n\n' % (nom, nom))
        else:
            out.append(
                '__declspec(dllexport) long long %s(void *a, void *b, void *c, void *d)\n'
                '{ (void)a; (void)b; (void)c; (void)d; journal("%s"); return %d; }\n\n'
                % (nom, nom, val))
    return ''.join(out)


def main():
    os.makedirs(os.path.dirname(SRC) or '.', exist_ok=True)
    with open(SRC, 'w', encoding='ascii') as fp:
        fp.write(source())
    print('%s ecrit : %d fonctions' % (SRC, len(FONCTIONS)))
    if '--source' in sys.argv:
        return 0

    env = dict(os.environ)
    env['PATH'] = MINGW + ';' + env.get('PATH', '')     # gcc a besoin de ses propres DLL
    out = os.path.join(DST, 'apm.dll')
    reelle = os.path.join(DST, 'apm.reelle.dll')
    if os.path.exists(out) and not os.path.exists(reelle):
        os.replace(out, reelle)
        print('la vraie apm.dll est conservee sous %s' % reelle)
    r = subprocess.run([GCC, '-shared', '-O2', '-s', '-o', out, SRC,
                        '-Wl,--kill-at', '-static-libgcc'],
                       env=env, capture_output=True, text=True)
    if r.stdout:
        print(r.stdout, end='')
    if r.stderr:
        print(r.stderr, end='')
    if r.returncode:
        print('gcc a echoue (code %d)' % r.returncode)
        return 1
    print('%s compile (%d octets)' % (out, os.path.getsize(out)))

    # Le scenario d'entrees voyage avec le stub.
    dst_sc = os.path.join(DST, 'apm_entrees.txt')
    if os.path.exists(SCENARIO):
        with open(SCENARIO, 'rb') as fp:
            data = fp.read()
        with open(dst_sc, 'wb') as fp:
            fp.write(data)
        print('%s copie (%d octets)' % (dst_sc, len(data)))
    else:
        print('ATTENTION : %s absent, le stub ne pressera aucun bouton' % SCENARIO)
    return 0


if __name__ == '__main__':
    sys.exit(main())
