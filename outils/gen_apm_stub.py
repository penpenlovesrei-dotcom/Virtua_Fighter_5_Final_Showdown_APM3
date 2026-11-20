#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere un apm.dll de substitution pour faire demarrer vfes.exe hors borne.

vfes.exe importe 57 fonctions d'apm.dll, la bibliotheque de la carte ALLS/APM3.
La vraie apm.dll dialogue avec amdaemon, le demon ALL.Net (reseau, comptabilite,
keychip) : sans lui, le jeu leve amdaemon::Exception et s'arrete. Ce stub remplace
apm.dll par une implementation locale qui repond "tout va bien, partie gratuite".

Chaque fonction annonce son appel par OutputDebugStringA : tools/instrument.py les
journalise, ce qui donne la sequence d'appels reelle et sert de boucle de mise au point.

ENTREES SCRIPTEES
    Input_isOn et Input_isOnNow sont les seules sources de boutons du jeu a ce
    stade : c'est donc le stub qui tient la manette. Il ne rend plus "rien
    d'appuye" mais joue un scenario lu dans un fichier texte, apm_entrees.txt,
    place a cote de la DLL. Le fichier est relu des qu'il change : on regle une
    sequence sans jamais recompiler.

    Signature reelle, etablie sur la vraie apm.dll :
        char Input_isOn(int code)      code 0..15, un seul argument
    L'appelant passe par un tronc de vtable de vfes.exe (0x140002BE0) qui fait
    "mov ecx, edx ; jmp [Input_isOn]" : le code arrive donc en premier argument.

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
    ('Input_setGamepadConfig', 0), ('Input_isGamepadDetect', 'E'),
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
# la version "48.00". Mesure du 2026-09-06, `analysis/pister_link.txt` :
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
# "48.00" demande six octets avec le NUL -> retour -2, ERANGE, et la CRT tue
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
#include <stdarg.h>


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

static unsigned g_quest_ms_declencheur;  /* "quest = <secondes>" */
static int  g_clavier = 1;
static int  g_manette = 1;
/* SUR QUEL JOUEUR LA MANETTE TOMBE (2026-10-04).
 *
 * Frederic : "la manette Xbox ne fonctionne plus du tout". Ce n'etait pas
 * une panne : depuis --joueur2, TOUS les boutons etaient assignes aux codes
 * P2+n (18 a 30), que seul le SECOND joueur lit. Or l'ecran-titre, les menus,
 * Customize et tout le solo sont du joueur 1, qui ne lit que 0 a 14 -- la
 * manette n'y pouvait donc rien, par construction, et le commentaire de
 * `disposition_par_defaut()` l'annoncait sans que personne en tire la
 * consequence.
 *
 *   1 = la manette DOUBLE le clavier sur le joueur 1 -- le defaut, c'est ce
 *       qu'on veut quand on joue seul devant le PC ;
 *   2 = la manette tient le joueur 2 et le clavier le joueur 1 -- le VERSUS
 *       a deux, qui est du travail valide et qu'on ne defait pas.
 *
 * Se regle dans apm_entrees.txt, a chaud, sans rien recompiler. */
static int  g_manette_joueur = 1;
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
/* CE QUE LE MOTEUR A OBTENU, code par code, au coup precedent. C est ce qui
 * rend la ligne " LU " fiable -- voir le commentaire de `entree`. */
static char      g_dernier_lu[32];
static unsigned g_descendants; /* ~courant & precedent : vient d'etre relache */
static DWORD    g_vif_date;    /* instant du dernier echantillonnage */
static int  g_touche[MAX_CODE];        /* code d'entree -> code virtuel Windows */
static unsigned g_bouton[MAX_CODE];    /* code d'entree -> masque XInput */
/* UN SECOND MASQUE PAR CODE, ET IL FALLAIT LE SEPARER (2026-10-04).
 *
 * `(etat & masque) == masque` est un ACCORD : deux bits dans un masque veut
 * dire "les deux tenus ensemble". On ne pouvait donc pas donner DEUX boutons
 * au meme code -- or c'est exactement ce qu'on veut pour une manette Xbox :
 * START **ou** A valident, X **ou** B annulent. D'ou un second masque,
 * combine par OU avec le premier. Se regle par " bouton2 <code> = <nom> ". */
static unsigned g_bouton_bis[MAX_CODE];
/* ET LA MEME CHOSE AU CLAVIER (2026-10-09), " touche2 <code> = <nom> ".
 * Il la fallait pour le L2 demande : le modele APM n a que SEPT entrees
 * d action (voir disposition_par_defaut), donc un huitieme bouton ne peut que
 * DOUBLER un des sept -- et doubler demande une seconde source. */
static int       g_touche_bis[MAX_CODE];
/* LE JOURNAL SUR FICHIER, et c'est ce qui manquait pour regler la manette.
 *
 * `OutputDebugStringA` ne se lit que sous debogueur, et le debogueur fait
 * tomber le jeu a 25 images par seconde : impossible de juger une manette dans
 * ces conditions. Avec " journal_fichier = 1 ", le stub ecrit lui-meme, a cote
 * de la DLL, dans apm_journal.txt :
 *
 *   PAD  0x1000 = A                       l'etat BRUT du wButtons a change
 *   MASQUE 0x00000200  codes 9            ce que le stub en a tire
 *   LU   Input_isOn(9) = OUI              ce que le MOTEUR a demande
 *
 * Trois lignes qui separent les trois pannes possibles -- la manette n'arrive
 * pas, elle arrive mais ne tombe pas sur le bon code, ou elle tombe bien et le
 * moteur ne demande pas ce code. Rien ne s'ecrit quand rien ne change. */
static int      g_journal_fichier;
/* " sauvegarde = 0|1 " : la sauvegarde locale du personnage personnalise.
 * Declaree ICI et non pres de son code, qui vit apres le lecteur du
 * fichier -- en C une variable se declare avant de servir. */
static int      g_sauvegarde = 1;
/* LA SAISIE DU NOM DE DONNEES EST-ELLE OUVERTE ? Declaree ICI et non pres de
 * son code : `lire_clavier` vit bien avant, et en C une variable se declare
 * avant de servir. Voir le bloc " LA SAISIE DU NOM DE DONNEES ". */
static int      g_nom_saisie;
static FILE    *g_trace;
static char     g_dossier[MAX_PATH];
static unsigned g_pad_vu = 0xFFFFFFFFu;   /* dernier wButtons journalise */
static unsigned g_masque_vu = 0xFFFFFFFFu;
static int      g_trace_lignes;

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
/* LE BOUTON XBOX. XInputGetState NE LE REND PAS -- le bit 0x0400 y est filtre
 * par l API publique. Il n arrive que par XInputGetStateEx, l export SANS NOM
 * d ordinal 100. MESURE du 2026-10-09 : xinput1_4.dll porte bien les ordinaux
 * 100 a 104 et 108/109 sans nom ; xinput9_1_0.dll n en a aucun. */
#define XI_GUIDE 0x0400

typedef struct { DWORD paquet; WORD boutons; BYTE gl, gr;
                 SHORT gx, gy, dx, dy; } XI_ETAT;
typedef DWORD (WINAPI *XI_GET)(DWORD, XI_ETAT *);
static XI_GET   g_xinput;
static int      g_xinput_tente;
static int      g_xinput_ex;       /* on a XInputGetStateEx : bouton XBOX lu */
/* LA MANETTE REPOND-ELLE ? Pose a chaque lecture, lu par Input_isGamepadDetect.
 * XInputGetState rend ERROR_DEVICE_NOT_CONNECTED (1167) quand la prise est
 * vide : le stub a donc TOUJOURS su la reponse, il ne la disait a personne. */
static int      g_pad_present;
static int      g_pad_present_vu = -1;   /* pour ne tracer que les changements */

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
    {"menu", XI_START}, {"affichage", XI_BACK}, {"view", XI_BACK},
    {"guide", XI_GUIDE}, {"xbox", XI_GUIDE},
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

/* Une ligne dans apm_journal.txt. Le fichier est ouvert a la premiere ligne et
 * VIDE a ce moment-la : un essai ne se lit pas par-dessus le precedent. Vide
 * apres chaque ligne, pour que le fichier soit lisible meme si le jeu est tue
 * -- c'est la lecon des journaux de sonde perdus a la fermeture. */
/* L HORLOGE DU JOURNAL. Frederic a demande pourquoi le demarrage est long
 * (2026-10-15). Ce qui est deja mesure : vf5fs_data.par fait 4,07 Go, rom/
 * fait 1,0 Go, le disque est un NVMe, et NI le stub NI le lanceur ne dorment.
 * Le temps est donc pris ailleurs -- et un journal sans heure ne peut pas le
 * dire. Chaque ligne porte maintenant les millisecondes depuis le chargement
 * de apm.dll : le trou se lira entre deux lignes. */
static unsigned g_trace_depart;   /* arme par DllMain, via trace_ms() */

static unsigned trace_ms(void)
{
    unsigned t = GetTickCount();
    if (!g_trace_depart) g_trace_depart = t ? t : 1;
    return t - g_trace_depart;
}

static void trace(const char *f, ...)
{
    va_list a;
    unsigned ms;
    if (!g_journal_fichier) return;
    if (!g_trace) {
        char c[MAX_PATH];
        _snprintf(c, sizeof c, "%sapm_journal.txt", g_dossier);
        g_trace = fopen(c, "w");
        if (!g_trace) { g_journal_fichier = 0; return; }
    }
    /* UNE BORNE, et elle est volontaire : un journal qui grossit sans fin
     * remplirait le disque sur une longue partie et ne serait plus lisible.
     * 8000 lignes couvrent tres largement un essai de manette. */
    if (g_trace_lignes >= 8000) {
        if (g_trace_lignes == 8000) {
            fputs("-- 8000 lignes : journal arrete ici --\n", g_trace);
            fflush(g_trace);
            g_trace_lignes++;
        }
        return;
    }
    g_trace_lignes++;
    ms = trace_ms();
    fprintf(g_trace, "[%3u.%03u] ", ms / 1000u, ms % 1000u);
    va_start(a, f);
    vfprintf(g_trace, f, a);
    va_end(a);
    fputc('\n', g_trace);
    fflush(g_trace);
}

/* Les noms des bits du wButtons, pour que le journal se lise sans table. */
static void nommer_pad(unsigned b, char *s, int n)
{
    static const struct { unsigned m; const char *n; } t[] = {
        {XI_UP,"haut"}, {XI_DOWN,"bas"}, {XI_LEFT,"gauche"}, {XI_RIGHT,"droite"},
        {XI_START,"START"}, {XI_BACK,"BACK"}, {XI_LB,"LB"}, {XI_RB,"RB"},
        {XI_A,"A"}, {XI_B,"B"}, {XI_X,"X"}, {XI_Y,"Y"},
        {XI_LT,"LT"}, {XI_RT,"RT"}, {XI_GUIDE,"XBOX"}, {0,0}
    };
    int i, k = 0;
    s[0] = 0;
    for (i = 0; t[i].n; i++)
        if (b & t[i].m) {
            int l = (int)strlen(t[i].n);
            if (k + l + 2 >= n) break;
            if (k) s[k++] = ' ';
            memcpy(s + k, t[i].n, l);
            k += l;
            s[k] = 0;
        }
    if (!k) { if (n > 6) memcpy(s, "rien", 5); }
}

/* LE MODE DE JEU, et il commande la disposition. Le lanceur ecrit
 * ram\mode.txt AVANT de patcher le moteur : c est la seule source qui dise
 * dans quel mode CE build a ete prepare. Lu une fois -- le mode ne peut pas
 * changer a chaud, `game_mode` est ecrit par vfes.exe (0x140002E1C) et le
 * moteur en derive ses drapeaux UNE FOIS (0x180C3B701). Absent = console. */
static int mode_arcade(void)
{
    static int vu = -1;
    char chemin[MAX_PATH];
    char mot[32];
    FILE *f;
    if (vu >= 0) return vu;
    vu = 0;
    _snprintf(chemin, sizeof chemin, "%sram\\mode.txt", g_dossier);
    f = fopen(chemin, "r");
    if (f) {
        if (fgets(mot, sizeof mot, f) && !_strnicmp(mot, "arcade", 6)) vu = 1;
        fclose(f);
    }
    return vu;
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
 * D'ou cette table : codes 0 a 14 pour le joueur 1 ; codes 18 a 30 pour le
 * joueur 2. `g_manette_joueur` decide sur LEQUEL la manette tombe -- 1 par
 * defaut, c'est-a-dire a cote du clavier. Mise sur les deux a la fois elle
 * piloterait les deux joueurs ensemble, ce qui n'a de sens nulle part : d'ou
 * un reglage et non une addition.
 *
 * Clavier AZERTY : A Z E sous les trois doigts.
 * Codes connus : 0 = TEST, 1 = SERVICE, 7 = START. */
#define P2 16                      /* le decalage du second joueur */

static void disposition_par_defaut(void)
{
    int i;
    for (i = 0; i < MAX_CODE; i++) {
        g_touche[i] = 0; g_touche_bis[i] = 0;
        g_bouton[i] = 0; g_bouton_bis[i] = 0;
    }
    /* joueur 1 : clavier seul */
    g_touche[0] = VK_F1;                                  /* TEST    */
    g_touche[1] = VK_F2;                                  /* SERVICE */
    g_touche[2] = VK_UP;
    g_touche[3] = VK_DOWN;
    g_touche[4] = VK_LEFT;
    g_touche[5] = VK_RIGHT;
    g_touche[6] = VK_SPACE;                               /* piece   */
    g_touche[7] = VK_RETURN;                              /* START   */
    /* ET `X` VALIDE AUSSI (demande de Frederic, 2026-10-11).
     *
     * C est le pendant clavier de ce que le bouton A fait deja a la manette
     * (`g_bouton_bis[7] = XI_A`) : une SECONDE touche sur le meme code, par
     * le second masque -- un masque a plusieurs touches est un ACCORD, pas
     * une alternative, donc on ne peut pas les mettre ensemble.
     *
     * `X` PORTE DEJA LE CODE 9 (le P du joueur 1), et c est sans danger :
     * presser X enverra les codes 7 ET 9, et `tools/entrees.py` a mesure sur
     * ce build que les codes 7, 8, 11 et 12 ne sortent QU EN codes logiques
     * de validation -- aucun n est un bouton de combat. En plein combat le
     * code 7 n est donc lu par personne. C est dit plutot que cache. */
    g_touche_bis[7] = 'X';                                /* VALIDER aussi */
    /* LES QUATRE BOUTONS D ACTION, ET ENFIN AUX BONS CODES (2026-10-10).
     *
     * CE QUI ETAIT FAUX, ET QUI SE VOYAIT MANETTE EN MAIN -- "les boutons
     * sont mappes n importe comment". Les noms que ce fichier donnait aux
     * codes etaient faux : le `D` appele "R1" portait en realite le G (la
     * GARDE), et `W` comme `V` ne faisaient RIEN en combat.
     *
     * LA CHAINE COMPLETE, relevee par `tools/entrees.py` sur CE build, de la
     * touche au code que l interface lit :
     *
     *     code apm   bit du masque arcade   code logique   role
     *        7            0                      7         VALIDER
     *        8            1                      8         VALIDER (annuler)
     *       12            2                      7         VALIDER
     *       11            3                      9         VALIDER
     *        9            6                    100         COMBAT  -- P
     *       10            7                    102         COMBAT  -- K
     *       13            4                    103         COMBAT  -- G
     *       14            5                    101         COMBAT  -- le 4e
     *
     * IL N Y A DONC QUE QUATRE BOUTONS D ACTION, et le jeu lui-meme n en
     * emploie que TROIS : son ecran OPTIONS > Controls affiche "P" sur la
     * croix, "K" sur le rond, "G" sur le carre et "NO USE" sur le
     * triangle. Les codes 8, 11 et 12 ne servent qu a valider.
     *
     * ET C EST LA REPONSE A "pourquoi pas le L2 et le R2". Ils existent
     * bien dans le jeu d origine -- la version console a sa couche d entrees
     * a elle. Ici, le masque arcade que `0x180243ED0` compose ne porte que
     * douze bits, et ses bits 8, 10 et 11 ne sont produits par AUCUN code
     * d entree : le modele APM3 n a pas de quoi les alimenter. L ecran
     * Controls le dit lui-meme, toutes ses lignes de gachette sont
     * "NO USE". Il n y a donc rien a quoi les brancher, et ce n est pas une
     * limite qu on s impose.
     *
     * LA DISPOSITION, calquee sur le schema "Standard" du jeu :
     *     croix / A  = P       rond / B = K       carre / X = G
     * `W` garde l annulation des menus (code 8), qui n a aucun role en
     * combat ; `V` prend le G, `Q` le quatrieme bouton. */
    g_touche[8] = 'W';                                    /* ANNULER      */
    g_touche[9] = 'X';                                    /* P            */
    g_touche[10] = 'C';                                   /* K            */
    g_touche[13] = 'V';                                   /* G -- la garde */
    g_touche[14] = 'Q';                                   /* le 4e, NO USE */
    /* code 15 : LA TOUCHE DE SORTIE. Le moteur ne le lit nulle part -- il est
     * libre entre les codes du joueur 1 (0 a 14) et ceux du joueur 2 (18 a
     * 30). Seul le relais --transition-game l'interroge, pour quitter un mode
     * et revenir au menu. N'entrant pas dans la boucle par joueur, il peut
     * avoir les deux sources sans effet de bord. */
    g_touche[15] = VK_ESCAPE; g_bouton[15] = XI_BACK;
    /* codes 16 et 17 : LES DEUX BOUTONS DE CAMERA DE L'ECRAN TERMINAL.
     * Mesure de `tools/boutons_terminal.py` (2026-09-30) : des 32 creneaux du
     * stub, seuls 16, 17 et 31 sont libres -- le moteur lit 0 a 15 (dont le
     * 15, contrairement a ce qu'affirmait patch_moteur.py : `Input_isOnNow(15)`
     * en 0x18021490F), et `--joueur2` reserve 18 a 30 au second joueur.
     * `--terminal-boutons` accroche les deux sites de 0x1801C7890 sur ces
     * codes ; sans ce correctif ils ne sont lus par personne.
     *   code 16 = B = recentrer la camera   (l'ancien masque 0x100)
     *   code 17 = N = changer de vue        (l'ancien masque 0x800)
     * Comme le code 15, ils n'entrent pas dans la boucle par joueur. */
    g_touche[16] = 'B';
    g_touche[17] = 'N';
    /* LA MANETTE, sur le joueur que `manette_joueur` designe. Avec 1 elle
     * double le clavier sur le joueur 1 ; avec 2 elle tient le joueur 2
     * pendant que le clavier garde le joueur 1. */
    {
        int d = (g_manette_joueur == 2) ? P2 : 0;
        g_bouton[d + 2] = XI_UP;
        g_bouton[d + 3] = XI_DOWN;
        g_bouton[d + 4] = XI_LEFT;
        g_bouton[d + 5] = XI_RIGHT;
        g_bouton[d + 6] = XI_BACK;                        /* piece   */
        g_bouton[d + 7] = XI_START;                       /* START   */
        /* LES QUATRE BOUTONS DE FACE SUR LES QUATRE CODES D ACTION, au
         * schema "Standard" du jeu : croix = P, rond = K, carre = G. Sur
         * une manette Xbox cela donne A, B et X ; le Y prend le quatrieme
         * code, celui que le jeu affiche "NO USE".
         * L ANNULATION DES MENUS passe par le second masque du bouton B (voir
         * plus bas) : le code 8 ne sert qu aux menus, et lui donner un bouton
         * de face a lui seul coutait un bouton de combat. */
        g_bouton[d + 9] = XI_A;                           /* P */
        g_bouton[d + 10] = XI_B;                          /* K */
        g_bouton[d + 13] = XI_X;                          /* G -- la garde */
        g_bouton[d + 14] = XI_Y;                          /* le 4e, NO USE */
        /* LB, RB, LT, RT : RIEN. Ce n est pas un choix, c est le modele
         * d entrees -- il n a que quatre boutons d action, tous pris. */
        /* LES DEUX BOUTONS QUE LES MENUS LISENT, DOUBLES (2026-10-04).
         *
         * Mesure deja consignee (analysis/carte_options.md S 6) : dans les
         * menus le moteur ne lit que le code 7 (valider, 0x1801A2BC0) et le
         * code 8 (annuler, 0x1801A2B90). A la manette, START validait et X
         * annulait -- et le bouton A, celui que tout le monde presse, ne
         * faisait rien. "a la manette les boutons ne sont pas reconnus, seul
         * le bouton start fonctionne" : c'etait exact, et par construction.
         *
         * On ne peut pas ajouter A au masque du code 7 (ce serait l'ACCORD
         * START+A) : d'ou le second masque. A vaut maintenant START, et B
         * vaut X -- la convention Xbox, et le croisement habituel avec la
         * croix PlayStation que porte le clavier. */
        g_bouton_bis[d + 7] = XI_A;                       /* VALIDER aussi */
        g_bouton[d + 8] = XI_B;                           /* ANNULER       */
        /* LA MANETTE DOIT POUVOIR VALIDER LES MENUS, MEME SUR LE JOUEUR 2.
         *
         * Frederic, 2026-10-11 : " la touche menu n est pas liee a la fonction
         * START, donc impossible de lancer le joueur 2 ". Son journal dit
         * pourtant que tout arrive --
         *     PAD    0x0010  START
         *     MASQUE 0x00800000  codes 23
         * -- 23, c est bien le START du joueur 2. Ce qui manque n est pas la
         * liaison, c est le LECTEUR : les menus ne lisent QUE le joueur 1
         * (0x1801A2BC0 pour valider, 0x1801A2B90 pour annuler).
         *
         * On donne donc a la manette, EN PLUS, les codes 7 et 8 DU JOUEUR 1.
         * Et c est sans danger, parce que c est mesure (tools/entrees.py) :
         * les codes 7, 8, 11 et 12 ne sortent QUE en codes logiques de
         * validation -- aucun n est un bouton de combat. En plein combat ils
         * ne font donc rien du tout, et le joueur 1 ne bouge pas.
         *
         * LES DIRECTIONS, ELLES, NE SONT PAS DONNEES AU JOUEUR 1 : les codes
         * 2 a 5 FONT marcher le combattant. La manette deplacerait les deux
         * a la fois. On navigue au clavier, on valide des deux. Pour tout
         * piloter a la manette, " manette_joueur = 1 " -- relu a chaud. */
        if (d) {
            g_bouton[7] = XI_START;                       /* valider      */
            /* `A` NE VALIDE PLUS COTE JOUEUR 1 -- demande de Frederic,
             * 2026-10-11. Il portait `g_bouton_bis[7] = XI_A`, c est-a-dire
             * la validation DES MENUS, que le moteur ne lit que sur le
             * joueur 1 (0x1801A2BC0). Il garde ses deux codes a lui : 25
             * (le poing) et 23 (valider, cote joueur 2). Dans les menus,
             * c est donc le seul bouton Menu qui valide. */
            g_bouton[8] = XI_B;                           /* annuler      */
            /* ET LE CODE 15 LUI EST RETIRE -- demande de Frederic,
             * 2026-10-11. C est le code "quitter le mode courant", celui que
             * `--transition-game` interroge pour revenir au menu. Il est
             * HORS de la boucle par joueur, donc il n appartient a personne,
             * et la manette l avait en plus de tout le reste : sur BACK elle
             * mettait un credit au joueur 2 (code 24) ET quittait le mode.
             * Un joueur 2 n a pas a sortir du mode. Le CLAVIER garde Echap,
             * et la manette le reprend des qu elle revient sur le joueur 1
             * (`manette_joueur = 1`), ou elle double le joueur 1 en tout. */
            g_bouton[15] = 0;
        }
        /* LE MODE ARCADE met les deux boutons d exploitation sur la manette
         * (demande de Frederic, 2026-10-09) :
         *
         *     TEST    (code 0) = bouton affichage  BACK
         *     SERVICE (code 1) = bouton XBOX       GUIDE
         *
         * BACK est alors RETIRE du code 6 et du code 15. Trois roles sur un
         * bouton S ADDITIONNERAIENT -- (etat & masque) == masque n est pas une
         * alternative : presser BACK aurait mis une piece, quitte le mode ET
         * ouvert le menu TEST d un seul coup. Le clavier garde Espace et
         * Echap : la demande ne porte que sur la manette. */
        if (mode_arcade()) {
            g_bouton[0] = XI_BACK;
            g_bouton[1] = XI_GUIDE;
            g_bouton[d + 6] = 0;
            g_bouton[15] = 0;
        }
    }
}

static unsigned lire_clavier(void)
{
    unsigned m = 0;
    int i;
    if (!g_clavier) return 0;
    /* PENDANT LA SAISIE DU NOM, AUCUNE TOUCHE NE PART DANS LE JEU. Le moteur
     * gele deja la page (0x1801C4F9C saute son traitement des entrees), mais
     * les AUTRES taches de la page lisent toujours : sans cette coupure, taper
     * un nom les piloterait. */
    if (g_nom_saisie) return 0;
    /* Le jeu ne doit repondre que s'il a le premier plan : sinon on taperait
     * dans la fenetre du dessus tout en pilotant le jeu par-dessous. */
    {
        DWORD pid = 0;
        HWND f = GetForegroundWindow();
        if (!f) return 0;
        GetWindowThreadProcessId(f, &pid);
        if (pid != GetCurrentProcessId()) return 0;
    }
    for (i = 0; i < MAX_CODE; i++) {
        if (g_touche[i] && (GetAsyncKeyState(g_touche[i]) & 0x8000))
            m |= (1u << i);
        else if (g_touche_bis[i]
                 && (GetAsyncKeyState(g_touche_bis[i]) & 0x8000))
            m |= (1u << i);
    }
    return m;
}

static unsigned lire_manette(void)
{
    XI_ETAT e;
    unsigned m = 0;
    unsigned b;
    int i;
    if (!g_manette) { g_pad_present = 0; return 0; }
    if (!g_xinput_tente) {
        HMODULE h;
        g_xinput_tente = 1;
        h = LoadLibraryA("xinput1_4.dll");
        if (!h) h = LoadLibraryA("xinput1_3.dll");
        if (!h) h = LoadLibraryA("xinput9_1_0.dll");
        /* L EXPORT SANS NOM D ORDINAL 100 D ABORD : c est XInputGetStateEx,
         * la seule facon d obtenir le bouton XBOX (bit 0x0400), que
         * XInputGetState filtre. Meme signature, donc meme pointeur. On
         * retombe sur l export nomme quand il manque -- xinput9_1_0 n a aucun
         * ordinal sans nom. */
        if (h) {
            g_xinput = (XI_GET)GetProcAddress(h, (LPCSTR)100);
            if (g_xinput) g_xinput_ex = 1;
            else g_xinput = (XI_GET)GetProcAddress(h, "XInputGetState");
        }
        OutputDebugStringA(
            !g_xinput ? "[apm] manette : XInput absent\n"
            : g_xinput_ex ? "[apm] manette : XInputGetStateEx charge "
                            "(bouton XBOX lisible)\n"
                          : "[apm] manette : XInputGetState charge "
                            "(bouton XBOX NON lisible)\n");
        trace("PAD    %s", !g_xinput ? "XInput absent"
              : g_xinput_ex ? "XInputGetStateEx (ordinal 100) : le bouton XBOX "
                              "est lisible"
                            : "XInputGetState seul : le bouton XBOX n est PAS "
                              "lisible");
    }
    if (!g_xinput) { g_pad_present = 0; return 0; }
    memset(&e, 0, sizeof e);
    if (g_xinput(0, &e) != 0) { g_pad_present = 0; return 0; }
    g_pad_present = 1;
    b = e.boutons;
    if (e.gl > 60) b |= XI_LT;
    if (e.gr > 60) b |= XI_RT;
    /* le stick gauche vaut la croix : zone morte a un tiers de la course */
    if (e.gy > 10000) b |= XI_UP;
    if (e.gy < -10000) b |= XI_DOWN;
    if (e.gx < -10000) b |= XI_LEFT;
    if (e.gx > 10000) b |= XI_RIGHT;
    if (b != g_pad_vu) {
        char n[96];
        nommer_pad(b, n, sizeof n);
        trace("PAD    0x%04X  %s", b, n);
        g_pad_vu = b;
    }
    for (i = 0; i < MAX_CODE; i++) {
        unsigned m1 = g_bouton[i], m2 = g_bouton_bis[i];
        if (m1 && (b & m1) == m1) m |= (1u << i);
        else if (m2 && (b & m2) == m2) m |= (1u << i);
    }
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
    g_journal_fichier = 0;
    g_sauvegarde = 1;
    g_test = 0;
    g_quest_ms_declencheur = 0;
    g_clavier = 1;
    g_manette = 1;
    /* `manette_joueur` DOIT etre connu AVANT la disposition, puisque c'est
     * lui qui decide sur quels codes les boutons tombent. On le cherche donc
     * en pre-passe, et l'ordre des lignes dans le fichier n'a pas d'effet. */
    g_manette_joueur = 1;
    {
        char *s = buf;
        while (*s) {
            char *l = s;
            while (*s && *s != '\n') s++;
            if (*s) s++;
            while (*l == ' ' || *l == '\t') l++;
            if (!_strnicmp(l, "manette_joueur", 14)) {
                char *r = l + 14;
                while (*r == ' ' || *r == '\t' || *r == '=') r++;
                g_manette_joueur = atoi(r);
                if (g_manette_joueur != 2) g_manette_joueur = 1;
            }
        }
    }
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
            } else if (!_strnicmp(p, "journal_fichier", 15)) {
                /* AVANT "journal", et c'est le MEME piege que
                 * manette_joueur : `_strnicmp(p, "journal", 7)` reconnait
                 * aussi "journal_fichier" et lirait `atoi("_fichier = 1")`
                 * = 0, ce qui eteindrait le journal qu'on vient de demander.
                 * Un prefixe commun se teste toujours du plus long au plus
                 * court. */
                char *r = p + 15;
                while (*r == ' ' || *r == '\t' || *r == '=') r++;
                g_journal_fichier = atoi(r);
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
            } else if (!_strnicmp(p, "quest", 5)) {
                char *r = p + 5;
                while (*r == ' ' || *r == '	' || *r == '=') r++;
                g_quest_ms_declencheur = (unsigned)(atof(r) * 1000.0);
            } else if (!_strnicmp(p, "sauvegarde", 10)) {
                char *r = p + 10;
                while (*r == ' ' || *r == '	' || *r == '=') r++;
                g_sauvegarde = atoi(r);
            } else if (!_strnicmp(p, "clavier", 7)) {
                char *r = p + 7;
                while (*r == ' ' || *r == '\t' || *r == '=') r++;
                g_clavier = atoi(r);
            } else if (!_strnicmp(p, "manette_joueur", 14)) {
                /* AVANT "manette", et c'est un piege a ne pas se poser :
                 * `_strnicmp(p, "manette", 7)` reconnait AUSSI
                 * "manette_joueur", et lirait `atoi("_joueur = 1")` = 0,
                 * ce qui eteindrait la manette au lieu de la deplacer. La
                 * valeur a deja ete prise en pre-passe ; on consomme la ligne
                 * pour qu'elle ne retombe pas sur le test suivant. */
                (void)0;
            } else if (!_strnicmp(p, "manette", 7)) {
                char *r = p + 7;
                while (*r == ' ' || *r == '\t' || *r == '=') r++;
                g_manette = atoi(r);
            } else if (!_strnicmp(p, "touche2", 7)
                       && (p[7] == ' ' || p[7] == '\t')) {
                /* AVANT "touche", prefixe commun, meme regle que bouton2. */
                char *r = p + 7;
                int c, vk;
                while (*r == ' ' || *r == '\t') r++;
                c = code_du_nom(r, (int)strcspn(r, " \t="));
                while (*r && *r != ' ' && *r != '\t' && *r != '=') r++;
                while (*r == ' ' || *r == '\t' || *r == '=') r++;
                vk = vk_du_nom(r);
                if (c >= 0 && c < MAX_CODE && vk >= 0) g_touche_bis[c] = vk;
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
            } else if (!_strnicmp(p, "bouton2", 7)
                       && (p[7] == ' ' || p[7] == '\t')) {
                /* AVANT "bouton", prefixe commun, meme regle. Le SECOND
                 * bouton d'un code : combine par OU, pas par accord. */
                char *r = p + 7;
                int c, b;
                while (*r == ' ' || *r == '\t') r++;
                c = code_du_nom(r, (int)strcspn(r, " \t="));
                while (*r && *r != ' ' && *r != '\t' && *r != '=') r++;
                while (*r == ' ' || *r == '\t' || *r == '=') r++;
                b = pad_du_nom(r);
                if (c >= 0 && c < MAX_CODE && b >= 0)
                    g_bouton_bis[c] = (unsigned)b;
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
    if (g_masque != g_masque_vu) {
        char c[160];
        int k = 0, j;
        c[0] = 0;
        for (j = 0; j < MAX_CODE; j++)
            if ((g_masque & (1u << j)) && k < (int)sizeof c - 5)
                k += _snprintf(c + k, sizeof c - k, "%s%d", k ? " " : "", j);
        trace("MASQUE 0x%08X  codes %s", g_masque, k ? c : "rien");
        g_masque_vu = g_masque;
    }
    (void)t;
}

/* --------------------------------------------------------------------------
 * LA SAUVEGARDE DU PERSONNAGE PERSONNALISE (2026-10-04, revu le 10-05)
 *
 * Frederic : "il n y a pas de personnage modifie enregistre apres relance".
 *
 * POURQUOI LE MOTEUR N EN A PAS, ET CE N EST PAS UN DEFAUT A REPARER.
 * Tout a ete lu, rien suppose :
 *
 *  . la sauvegarde LOCALE de la borne ne porte que 128 octets -- quatre
 *    enregistrements Backup_* statiques (0x38, 0x10, 0x2C, 0x0C) ;
 *  . le moteur a bien une sauvegarde SUR FICHIER (BackupRamFile, vtable
 *    0x180409478, chemin "ram/BackupRam" en 0x1804094B8) et elle est creee
 *    sans condition. Son dossier a ete cree : il reste VIDE. Des 51 fonctions
 *    du module, les quatre de son API ne sont appelees que par le CHARGEUR
 *    0x180049910 -- aucun appelant externe pour une ecriture ;
 *  . le chemin console est entier dans le binaire -- CS_AUTOLOAD, sous-etat 5,
 *    dix etapes non bouchonnees en 0x180644640 -- mais son etape 0 passe par
 *    le bouchon 0x180007450 et, surtout, ses etapes 5 a 8 testent
 *    [joueurs+0x1FE10], un couple {fonction, objet} que le binaire lit des
 *    centaines de fois et n ecrit JAMAIS. Le service n a pas ete desactive,
 *    il a ete RETIRE. Le forcer ferait defiler les neuf etapes dans leurs
 *    branches nulles, sans rien charger.
 *
 * ON TIENT DONC LA SAUVEGARDE NOUS-MEMES, et il faut DEUX blocs -- c est ce
 * que le premier jet avait rate :
 *
 *  1. L ENREGISTREMENT DE TRAVAIL, ce qu on est en train d habiller.
 *     0x1801C5AB0 : [0x18070FB10] + 0x18 + joueur*0x5A0, 1440 octets par
 *     joueur, et il n y en a que DEUX (le gestionnaire est alloue avec 0xFD8
 *     en 0x1800FF7F2). Ses 24 parties equipees sont les mots a partir de
 *     +0x262. Celui-la etait bien sauve et bien relu -- le journal le disait,
 *     et le moteur ne l effacait pas.
 *
 *  2. LA TABLE DES PERSONNAGES ENREGISTRES, ce que l ecran LISTE, et c est
 *     elle qui manquait. Le dessin du DataSelector (0x1801CFAA2) est sans
 *     ambiguite :
 *
 *         cmp dword [rbx+0x288], 0        ; le NOMBRE d entrees
 *         je  -> affiche "---"
 *         imul rcx, rax, 0x84             ; une ligne fait 0x84 octets
 *         cmp byte [rcx+rbx+0x28C], 0     ; nom vide -> "---"
 *
 *     et son remplisseur (0x1801D0B00) prend ses entrees de 0x1801C5A80 :
 *     [0x180752148] + 0x28 + index*0x80, index borne a 150
 *     (cmp rbx, 0x96 ; cmovb). Une entree compte si son PREMIER OCTET n est
 *     pas nul. L objet est alloue avec 0x68D8 octets (0x1801B4FA6), donc les
 *     150 x 0x80 = 0x4B00 tiennent largement.
 *
 *     On ne sauve QUE ce tableau, pas l objet entier : au-dela vivent des
 *     std::string et des pointeurs, et restaurer un pointeur d une execution
 *     precedente serait catastrophique. Les entrees, elles, sont des donnees
 *     plates -- le remplisseur les recopie a l aveugle par quatre vmovups.
 *
 * CE QUI REND L OPERATION INOFFENSIVE, et c est la seule raison pour laquelle
 * on se permet d ecrire dans la memoire du moteur :
 *
 *   . on ne RELIT que si la table des personnages est ENTIEREMENT vide --
 *     aucune entree occupee. On remplit ce que le moteur n a pas rempli, et
 *     on n ecrase jamais une sauvegarde vivante ;
 *   . on n ENREGISTRE jamais deux blocs tous les deux vides ;
 *   . chaque page est verifiee par VirtualQuery avant d etre touchee : les
 *     deux pointeurs sont nuls au demarrage et le restent un moment.
 *
 * Se coupe par " sauvegarde = 0 " dans apm_entrees.txt.
 * -------------------------------------------------------------------------- */
#define CUST_RVA      0x70FB10      /* pointeur -> enregistrements de travail */
#define CUST_TETE     0x18
#define CUST_PAS      0x5A0
#define CUST_JOUEURS  2
#define CUST_PARTS    0x262         /* les 24 mots des parties equipees */
#define PERSO_RVA     0x752148      /* pointeur -> table des personnages */
#define PERSO_TETE    0x28
#define PERSO_PAS     0x80
#define PERSO_MAX     150           /* cmp rbx, 0x96 ; cmovb */
/* LE MARQUEUR DE FIN DE DEMARRAGE, et c est le moteur qui l ecrit.
 *
 * MESURE du 2026-10-06. Le bloc est remis a zero par FUN_1801B8A80, appelee de
 * trois sites : 0x1801B76BC (mort, ferme par le bouchon 0x180007450),
 * 0x1801B8C61 (init du sous-systeme) et 0x1801B9DE4, VIVANT -- sa garde
 * FUN_180007440() rend 0, donc " -1 < 0 " est vrai. Ce dernier n a qu un
 * appelant, 0x1800DDDE1, premier champ de l enregistrement numero 5 de la
 * table d etats 0x1803A0628 : une ETAPE DE DEMARRAGE. Il y a donc DEUX
 * effacements, tous deux avant que le joueur puisse agir.
 *
 * Le second, et lui seul, passe par FUN_1801B69B0(1), qui ecrit
 * " byte [bloc+0x671D] = 1 " en 0x1801B6A3F. L init, elle, pose un MOT a
 * +0x671C (" mov word [rax+0x671c], 1 " en 0x1801B8C78), ce qui laisse
 * +0x671D a ZERO. Les quatre autres ecritures de +0x671D sont mortes :
 * 0x1801B7687 et 0x1801B799E sont dans les deux lanceurs fermes par le
 * bouchon, 0x1801B6A77 est la fin du SAVE qui ne tourne jamais.
 *
 * Donc +0x671D passe de 0 a 1 EXACTEMENT UNE FOIS, au dernier effacement du
 * demarrage. On ne lit et on n ecrit rien avant. Si le marqueur n arrivait
 * jamais, le journal le dirait -- un echec visible vaut mieux qu une
 * sauvegarde ecrasee en silence. */
#define PERSO_MARQUEUR 0x671D
/* "VF56" : le format porte DEUX blocs depuis le 10-05 ; l ancien fichier de
 * 2888 octets est refuse proprement par la magie et les tailles. */
#define CUST_MAGIE    0x36354656u

#define CUST_N1  ((size_t)CUST_JOUEURS * CUST_PAS)
#define CUST_N2  ((size_t)PERSO_MAX * PERSO_PAS)

static int      g_cust_attente;    /* on a dit une fois qu on attendait */
static int      g_cust_n_fichier = -2;  /* -2 pas encore lu, -1 inexploitable */
static int      g_cust_arme;       /* la remise en table a eu lieu */
static unsigned g_cust_somme;
static DWORD    g_cust_date;
static char     g_cust_fichier[MAX_PATH];

/* UN CONTROLE QUI MESURAIT L UNIFORMITE ET CROYAIT MESURER LA LISIBILITE
 * (corrige le 2026-10-07, journal 140).
 *
 * L ancienne derniere ligne etait :
 *
 *     if (p + n > mbi.BaseAddress + mbi.RegionSize) return 0;
 *
 * Or `VirtualQuery` ne rend QU UNE region -- celle, autour de `p`, ou l etat
 * et la protection sont uniformes. Exiger que toute la plage y tienne, c est
 * exiger que la plage ne soit pas fragmentee. Et une section INSCRIPTIBLE
 * l est presque toujours : le chargeur applique ses protections page par
 * page, le BSS d une `.data` ne vient pas du fichier, et toute ecriture en
 * copie-sur-ecriture coupe la region en deux.
 *
 * MESURE du 2026-10-07 (`RES/DIAG`, dans le processus vivant) : des sept
 * sections du moteur, les cinq en lecture seule etaient dites "lisibles" et
 * les DEUX inscriptibles -- `.data` et `.greffe` -- "ILLISIBLES". C est la
 * signature exacte du defaut, et c est ce qui empechait de trouver la zone
 * VF5RESOL alors que le module etait charge des le premier tour.
 *
 * On parcourt donc les regions successives jusqu a couvrir `n`. Et on rejette
 * explicitement PAGE_GUARD et PAGE_NOACCESS : l ancien test les laissait
 * passer, `PAGE_READONLY|PAGE_GUARD` valant 0x102, dont le ET avec le masque
 * de lecture est non nul -- alors qu y toucher leve une exception. */
static int page_lisible(const void *p, size_t n, int ecriture)
{
    MEMORY_BASIC_INFORMATION mbi;
    /* PAGE_EXECUTE_WRITECOPY (0x80) MANQUAIT AUX DEUX MASQUES, et c est la
     * seconde moitie du defaut du 2026-10-07. `.greffe` est greffee
     * EXECUTABLE ET INSCRIPTIBLE (0xE0000060, parce qu elle porte des
     * relais) : le chargeur donne donc EXECUTE_WRITECOPY a ses pages tant
     * qu elles n ont pas ete ecrites, et EXECUTE_READWRITE (0x40) a celles
     * qui l ont ete. Mesure dans le processus vivant, journal du 2026-10-07 :
     *     region 0  taille 0x2000  prot 0x80
     *     region 1  taille 0x1000  prot 0x40
     *     region 2  taille 0x1000  prot 0x80
     * Deux des trois etaient rejetees sur la PROTECTION, la plage entiere sur
     * la FRAGMENTATION. Il fallait les deux corrections. */
    const DWORD lire = PAGE_READONLY | PAGE_READWRITE | PAGE_WRITECOPY
                     | PAGE_EXECUTE_READ | PAGE_EXECUTE_READWRITE
                     | PAGE_EXECUTE_WRITECOPY;
    const DWORD ecr = PAGE_READWRITE | PAGE_WRITECOPY
                    | PAGE_EXECUTE_READWRITE | PAGE_EXECUTE_WRITECOPY;
    const char *d = (const char *)p;
    const char *fin;
    if (!p) return 0;
    if (n == 0) return 1;
    fin = d + n;
    while (d < fin) {
        const char *suite;
        if (!VirtualQuery(d, &mbi, sizeof mbi)) return 0;
        if (mbi.State != MEM_COMMIT) return 0;
        if (mbi.Protect & (PAGE_GUARD | PAGE_NOACCESS)) return 0;
        if (!(mbi.Protect & (ecriture ? ecr : lire))) return 0;
        suite = (const char *)mbi.BaseAddress + mbi.RegionSize;
        if (suite <= d) return 0;      /* aucun progres : on ne boucle pas */
        d = suite;
    }
    return 1;
}

static unsigned somme(const unsigned char *p, size_t n)
{
    unsigned h = 2166136261u;        /* FNV-1a, et c est bien assez */
    size_t i;
    for (i = 0; i < n; i++) { h ^= p[i]; h *= 16777619u; }
    return h;
}

/* Resout un bloc : [moteur+rva] doit etre un pointeur valide, et
 * pointeur + tete une page inscriptible de n octets. */
static unsigned char *bloc_moteur(unsigned rva, unsigned tete, size_t n)
{
    static HMODULE h;
    unsigned char **pp, *b;
    if (!h) h = GetModuleHandleA("vf5fs-pxd-w64-Retail_APM3.dll");
    if (!h) return NULL;
    pp = (unsigned char **)((char *)h + rva);
    if (!page_lisible(pp, sizeof *pp, 0)) return NULL;
    if (!*pp) return NULL;
    b = *pp + tete;
    if (!page_lisible(b, n, 1)) return NULL;
    return b;
}

/* Une entree de la table compte quand son premier octet n est pas nul -- c est
 * le test du moteur lui-meme (0x1801C5A57, 0x1801CFAB5, 0x1801D0B0B), et la
 * console l ecrit a 1 en 0x8222C408. Compte en perso_compte(), plus bas.
 *
 * LA TABLE EST-ELLE INITIALISEE PAR LE MOTEUR, ou encore du remplissage de tas ?
 *
 * MESURE du 2026-10-05 (tools\sauvegarde.cmd, point d arret materiel sur
 * [0x180752148]+0x28). A l instant ou 0x1801B5050 pose le pointeur, la sonde
 * compte CENT CINQUANTE entrees occupees : l objet sort de " new 0x68D8 " et
 * porte encore 0xBAADF00D, le motif d allocation non initialisee du tas de
 * debogage -- vu en clair dans la valeur relevee, 010000ba 03f0adba. Le
 * moteur ne met les octets d occupation a zero qu ENSUITE, en 0x1801C5CE4.
 *
 * C etait LA faute : notre coup unique de relecture etait grille sur cette
 * image-la (" la table est deja garnie "), et plus rien n etait relu de toute
 * la session. Le fichier etait bon ; personne ne le lisait.
 *
 * LE TEST NE S INVENTE PAS. L octet d occupation ne vaut jamais que 0 ou 1 :
 *   . la console l ecrit a 1 en 0x8222C408  (*(base + i*0x80 + 0x28) = 1)
 *   . la borne le teste contre 0 en 0x1801C5A57 et 0x1801CFAB5
 * Toute autre valeur -- 0xBA, 0xEE, 0xFE, 0xCD -- n est pas une entree, c est
 * du tas. Tant qu on en voit une, on ne relit rien et on n ecrit rien. */
static int perso_pret(const unsigned char *t)
{
    int i;
    for (i = 0; i < PERSO_MAX; i++)
        if (t[(size_t)i * PERSO_PAS] > 1) return 0;
    return 1;
}

static int travail_vide(const unsigned char *b)
{
    int i;
    for (i = 0; i < 24; i++) {
        unsigned short v;
        memcpy(&v, b + CUST_PARTS + i * 2, 2);
        if (v) return 0;
    }
    return 1;
}

/* Combien de personnages le FICHIER porte-t-il ? -1 s il est illisible ou d un
 * autre format. C est la garde qui empeche de l ecraser par une table vide. */
static int cust_fichier_compte(void)
{
    FILE *f;
    unsigned e[3];
    int n = 0, i;
    unsigned char ligne[PERSO_PAS];
    if (!g_cust_fichier[0]) return -1;
    f = fopen(g_cust_fichier, "rb");
    if (!f) return -1;
    if (fread(e, sizeof e, 1, f) != 1 || e[0] != CUST_MAGIE
            || e[1] != (unsigned)CUST_N1 || e[2] != (unsigned)CUST_N2) {
        fclose(f);
        return -1;
    }
    if (fseek(f, (long)sizeof e + (long)CUST_N1, SEEK_SET) != 0) {
        fclose(f);
        return -1;
    }
    for (i = 0; i < PERSO_MAX; i++) {
        if (fread(ligne, 1, PERSO_PAS, f) != PERSO_PAS) break;
        if (ligne[0]) n++;
    }
    fclose(f);
    return n;
}

/* Relit le fichier DANS les deux blocs vivants. Rend le nombre de personnages
 * remis en table, ou -1 si rien n a pu etre relu. */
static int cust_relire(unsigned char *b1, unsigned char *b2)
{
    FILE *f;
    unsigned e[3];
    int n = 0, i;
    f = fopen(g_cust_fichier, "rb");
    if (!f) return -1;
    if (fread(e, sizeof e, 1, f) != 1 || e[0] != CUST_MAGIE
            || e[1] != (unsigned)CUST_N1 || e[2] != (unsigned)CUST_N2) {
        fclose(f);
        return -1;
    }
    if (fread(b1, 1, CUST_N1, f) != CUST_N1
            || fread(b2, 1, CUST_N2, f) != CUST_N2) {
        fclose(f);
        return -1;
    }
    fclose(f);
    for (i = 0; i < PERSO_MAX; i++)
        if (b2[(size_t)i * PERSO_PAS]) n++;
    return n;
}

static int perso_compte(const unsigned char *t)
{
    int n = 0, i;
    for (i = 0; i < PERSO_MAX; i++)
        if (t[(size_t)i * PERSO_PAS]) n++;
    return n;
}

/* Le dernier effacement du demarrage a-t-il eu lieu ? Voir PERSO_MARQUEUR. */
static int boot_fini(void)
{
    const unsigned char *m = bloc_moteur(PERSO_RVA, PERSO_MARQUEUR, 1);
    return m && *m == 1;
}

static void cust_tic(void)
{
    unsigned char *b1, *b2;
    DWORD now;
    int n;
    if (!g_sauvegarde) return;
    now = GetTickCount();
    if (g_cust_date && now - g_cust_date < 500) return;   /* deux fois par s */
    g_cust_date = now ? now : 1;
    b1 = bloc_moteur(CUST_RVA, CUST_TETE, CUST_N1);
    b2 = bloc_moteur(PERSO_RVA, PERSO_TETE, CUST_N2);
    if (!b1 || !b2) return;
    if (!g_cust_fichier[0])
        _snprintf(g_cust_fichier, sizeof g_cust_fichier,
                  "%sram\\customize.bin", g_dossier);
    /* RIEN avant que le moteur n ait initialise la table. Le pointeur est pose
     * en 0x1801B5050, mais les octets d occupation ne sont mis a zero qu en
     * 0x1801C5CE4 : entre les deux, on lit du 0xBAADF00D. C est la que notre
     * coup unique se grillait. Mesure : tools\sauvegarde.cmd, 2026-10-05. */
    if (!perso_pret(b2)) {
        if (!g_cust_attente) {
            g_cust_attente = 1;
            trace("SAUVE  la table n est pas encore initialisee par le moteur "
                  "(remplissage de tas) -- on attend, rien n est lu ni ecrit");
        }
        return;
    }
    /* ET RIEN non plus avant le dernier effacement du demarrage : c est lui
     * qui avait defait notre restauration (journal " ecrit : 0 personnage(s) ").
     * Le moteur nous le dit lui-meme -- voir PERSO_MARQUEUR. */
    if (!boot_fini()) {
        if (g_cust_attente < 2) {
            g_cust_attente = 2;
            trace("SAUVE  le demarrage n a pas fini son dernier effacement "
                  "(bloc+0x671D vaut encore 0) -- on attend");
        }
        return;
    }
    /* Combien le fichier en porte : lu une fois, tenu a jour ensuite. */
    if (g_cust_n_fichier == -2) {
        g_cust_n_fichier = cust_fichier_compte();
        if (g_cust_n_fichier < 0)
            trace("SAUVE  aucun %s exploitable : premier lancement",
                  g_cust_fichier);
        else
            trace("SAUVE  %s porte %d personnage(s)",
                  g_cust_fichier, g_cust_n_fichier);
    }
    n = perso_compte(b2);

    /* LA REMISE EN TABLE, une seule fois, et au bon moment.
     *
     * On arrive ici le marqueur pose : les DEUX effacements du demarrage sont
     * passes (voir PERSO_MARQUEUR pour leur releve complet). La relecture peut
     * donc redevenir un coup unique -- c est le MOMENT qui manquait, pas le
     * nombre d essais.
     *
     * Et comme la table ne sera plus jamais videe par le moteur, un vidage
     * ulterieur est une SUPPRESSION VOULUE : elle se sauvegarde normalement,
     * sans garde speciale. Il n y a donc rien a sacrifier, contrairement a la
     * premiere redaction qui remettait en table a chaque tour et empechait de
     * supprimer son dernier personnage. */
    if (!g_cust_arme) {
        g_cust_arme = 1;
        if (n == 0 && g_cust_n_fichier > 0) {
            int r = cust_relire(b1, b2);
            if (r > 0) {
                trace("SAUVE  %d personnage(s) remis en table", r);
                OutputDebugStringA("[apm] personnalisation remise\n");
            } else {
                g_cust_n_fichier = -1;
                trace("SAUVE  %s illisible a la relecture, rien n est remis",
                      g_cust_fichier);
            }
        } else if (n) {
            trace("SAUVE  la table porte deja %d personnage(s), rien n est "
                  "relu", n);
        }
        g_cust_somme = somme(b1, CUST_N1) ^ somme(b2, CUST_N2);
        return;
    }
    {
        unsigned s = somme(b1, CUST_N1) ^ somme(b2, CUST_N2);
        if (s == g_cust_somme) return;
        g_cust_somme = s;
        if (n == 0 && travail_vide(b1)) return;           /* jamais du vide */
        {
            FILE *f = fopen(g_cust_fichier, "wb");
            if (f) {
                unsigned e[3];
                e[0] = CUST_MAGIE;
                e[1] = (unsigned)CUST_N1;
                e[2] = (unsigned)CUST_N2;
                fwrite(e, sizeof e, 1, f);
                fwrite(b1, 1, CUST_N1, f);
                fwrite(b2, 1, CUST_N2, f);
                fclose(f);
                g_cust_n_fichier = n;
                trace("SAUVE  ecrit : travail %u o + table %u o, "
                      "%d personnage(s) enregistre(s) (somme 0x%08X)",
                      (unsigned)CUST_N1, (unsigned)CUST_N2, n, s);
            }
        }
    }
}

/* --- LES REGLAGES D OPTIONS, QUI NE TENAIENT PAS (2026-10-09) -------------
 *
 * MESURE du 2026-10-09. Les reglages vivent dans la MEME structure globale que
 * la table des personnages -- [0x180752148], notre PERSO_RVA -- et le moteur
 * DESIGNE LUI-MEME ce qui est persistable, par deux fonctions :
 *
 *   0x1801B7C20  le serialiseur : recopie la structure vivante vers son
 *                instantane [base+0x68C8] ;
 *   0x1801B7AC0  le predicat " c est sale " : compare vivant et instantane,
 *                champ par champ -- et c est lui qui donne la LISTE, sans trou :
 *
 *     memcmp(0 .. 0x4FD0)        la tete plate, dont la table des personnages,
 *                                deja tenue par cust_tic()
 *     memcmp(0x4FD0 .. 0x5014)   0x44 octets de reglages
 *     qword [0x5014]             les DEUX VOLUMES
 *     dword [0x501C], [0x5020]   dont Tips en 0x5020 (accesseur 0x1801B8980)
 *     2 x 0x18 a partir de 0x5024    un bloc par joueur
 *     word [0x5074], word [0x5076]
 *
 * Les volumes sont bien la : l applicateur du mixeur les lit a cette adresse
 * meme -- " vcvtsi2ss xmm0, xmm0, dword [rax+0x5014] " en 0x1801B9013 et
 * " dword [rax+0x5018] " en 0x1801B9033, divises par une constante et coupes
 * par l octet [base+0x6724]. Le poseur 0x1801B9130 les ecrit avant d y sauter.
 *
 * POURQUOI RIEN NE TENAIT : TaskCsSystemSaveData(SAVE), 0x1801B7960, est fermee
 * par trois bouchons -- 0x180007440, 0x180007450, 0x180007430. REVO a RETIRE
 * cette garde, il ne l a pas reimplementee (analysis/correspondance_revo.md,
 * site no 2) ; mais chez nous la suite de la tache ecrit par une API de
 * peripherique de carte qui n existe pas sur cette borne. On tient donc la
 * sauvegarde nous-memes, exactement comme la personnalisation.
 *
 * CE QUI REND L OPERATION SURE, et c est la raison de chaque borne :
 *
 *   . AUCUN POINTEUR dans la plage. Les deux qwords-pointeurs du voisinage sont
 *     a +0x4F8C (lu en 0x1801E27AD) et +0x4FC4 (ecrit en 0x1801B92AE), tous
 *     deux SOUS 0x4FD0 ; celui du sous-objet de +0x5058 est a son +0x60, donc
 *     en 0x50B8, AU-DESSUS de 0x5078. C est de la donnee plate -- le moteur la
 *     recopie lui-meme a l aveugle par deux " vmovups ymm " en 0x1801B7C52.
 *   . ON SAUTE 0x5054 .. 0x5074, que le predicat du moteur ne compare pas : ce
 *     sont les premiers champs du sous-objet de +0x5058, de l etat vivant. Les
 *     inclure ferait reecrire le fichier sans cesse.
 *   . UN FICHIER A PART, ram\options.bin. customize.bin garde son format et sa
 *     garde " jamais ecrire du vide " -- laquelle interdirait justement
 *     d enregistrer un reglage tant qu aucun personnage n existe.
 *   . MEME GARDE DE DEMARRAGE que la personnalisation : rien avant que le
 *     moteur ait pose son marqueur +0x671D. Ce marqueur est ecrit en
 *     0x1801B6A3F par FUN_1801B69B0, qui enchaine en 0x1801B6A5F sur le
 *     serialiseur : quand il vaut 1, les valeurs par defaut sont posees
 *     (0x1801B8D2F, 0x1801B8D5E, 0x1801B8D73) et l instantane est pris. C est
 *     l instant exact ou notre restauration ne sera plus defaite -- la faute
 *     corrigee le 10-06 pour la personnalisation, et on ne la refait pas.
 *
 * Se coupe par " sauvegarde = 0 " dans apm_entrees.txt, comme le reste.
 * -------------------------------------------------------------------------- */
#define OPT_TETE      0x4FD0        /* debut des reglages dans la structure */
#define OPT_N         0x84          /* 0x4FD0 .. 0x5054 */
#define OPT_D2        0xA4          /* 0x5074 - 0x4FD0 */
#define OPT_N2        4             /* 0x5074 .. 0x5078 */
#define OPT_SPAN      (OPT_D2 + OPT_N2)
#define OPT_TAILLE    (OPT_N + OPT_N2)
#define OPT_INSTANT   0x68C8        /* [base+0x68C8] -> l instantane */
/* Dans l INSTANTANE les deux mots sont en 0x5054, pas en 0x5074 : le
 * serialiseur recopie " live+0x5074 -> snap+0x5054 " en 0x1801B7CE6 et
 * " live+0x5076 -> snap+0x5056 " en 0x1801B7CF4. Decalage de 0x20. */
#define OPT_SNAP_D2   0x84
#define OPT_MAGIE     0x4F354656u   /* "VF5O" */
/* Trois temoins pour le journal, et rien d autre : on enregistre le bloc
 * entier, on n a donc pas besoin d etiqueter les autres octets. */
#define OPT_V1        (0x5014 - OPT_TETE)   /* volume lu en 0x1801B9013 */
#define OPT_V2        (0x5018 - OPT_TETE)   /* volume lu en 0x1801B9033 */
#define OPT_TIPS      (0x5020 - OPT_TETE)   /* accesseur 0x1801B8980 */

static int      g_opt_arme;        /* la restauration a eu lieu */
static int      g_opt_attente;     /* on a dit une fois qu on attendait */
static unsigned g_opt_somme;
static DWORD    g_opt_date;
static char     g_opt_fichier[MAX_PATH];

/* L instantane du moteur : [[module+PERSO_RVA]+0x68C8]+OPT_TETE. Facultatif --
 * s il n est pas alloue on s en passe, le predicat dira seulement " sale ". */
static unsigned char *opt_instantane(void)
{
    static HMODULE h;
    unsigned char **pp, **qq, *b;
    if (!h) h = GetModuleHandleA("vf5fs-pxd-w64-Retail_APM3.dll");
    if (!h) return NULL;
    pp = (unsigned char **)((char *)h + PERSO_RVA);
    if (!page_lisible(pp, sizeof *pp, 0) || !*pp) return NULL;
    qq = (unsigned char **)(*pp + OPT_INSTANT);
    if (!page_lisible(qq, sizeof *qq, 0) || !*qq) return NULL;
    b = *qq + OPT_TETE;
    if (!page_lisible(b, OPT_TAILLE, 1)) return NULL;
    return b;
}

/* La somme ne porte QUE sur ce qu on enregistre. Voir la borne plus haut. */
static unsigned opt_somme(const unsigned char *b)
{
    return somme(b, OPT_N) ^ somme(b + OPT_D2, OPT_N2);
}

static int opt_relire(unsigned char *b)
{
    FILE *f;
    unsigned e[2];
    unsigned char t[OPT_TAILLE];
    unsigned char *s;
    if (!g_opt_fichier[0]) return 0;
    f = fopen(g_opt_fichier, "rb");
    if (!f) return 0;
    if (fread(e, sizeof e, 1, f) != 1 || e[0] != OPT_MAGIE
            || e[1] != (unsigned)OPT_TAILLE
            || fread(t, 1, OPT_TAILLE, f) != OPT_TAILLE) {
        fclose(f);
        return 0;
    }
    fclose(f);
    memcpy(b, t, OPT_N);
    memcpy(b + OPT_D2, t + OPT_N, OPT_N2);
    s = opt_instantane();
    if (s) {
        memcpy(s, t, OPT_N);
        memcpy(s + OPT_SNAP_D2, t + OPT_N, OPT_N2);
    }
    return 1;
}

static void opt_ecrire(const unsigned char *b)
{
    unsigned e[2];
    FILE *f = fopen(g_opt_fichier, "wb");
    if (!f) return;
    e[0] = OPT_MAGIE;
    e[1] = (unsigned)OPT_TAILLE;
    fwrite(e, sizeof e, 1, f);
    fwrite(b, 1, OPT_N, f);
    fwrite(b + OPT_D2, 1, OPT_N2, f);
    fclose(f);
}

static void opt_tic(void)
{
    unsigned char *b;
    DWORD now;
    unsigned s;
    if (!g_sauvegarde) return;
    now = GetTickCount();
    if (g_opt_date && now - g_opt_date < 500) return;     /* deux fois par s */
    g_opt_date = now ? now : 1;
    b = bloc_moteur(PERSO_RVA, OPT_TETE, OPT_SPAN);
    if (!b) return;
    if (!g_opt_fichier[0])
        _snprintf(g_opt_fichier, sizeof g_opt_fichier,
                  "%sram\\options.bin", g_dossier);
    if (!boot_fini()) {
        if (!g_opt_attente) {
            g_opt_attente = 1;
            trace("OPT    le demarrage n a pas fini son effacement "
                  "(bloc+0x671D vaut encore 0) -- on attend, rien n est "
                  "lu ni ecrit");
        }
        return;
    }
    if (!g_opt_arme) {
        g_opt_arme = 1;
        if (opt_relire(b))
            trace("OPT    reglages relus de %s : %u o remis en place "
                  "(volumes %u / %u, Tips %u)",
                  g_opt_fichier, (unsigned)OPT_TAILLE,
                  b[OPT_V1], b[OPT_V2], b[OPT_TIPS]);
        else
            trace("OPT    aucun %s exploitable : les reglages du moteur "
                  "restent en place", g_opt_fichier);
        g_opt_somme = opt_somme(b);
        return;
    }
    s = opt_somme(b);
    if (s == g_opt_somme) return;
    g_opt_somme = s;
    opt_ecrire(b);
    trace("OPT    reglages ecrits dans %s : %u o (volumes %u / %u, Tips %u, "
          "somme 0x%08X)", g_opt_fichier, (unsigned)OPT_TAILLE,
          b[OPT_V1], b[OPT_V2], b[OPT_TIPS], s);
}

/* Le mode Quest : un module ECRIT A LA MAIN, pas genere. Il ne fait
 * rien tant que le scenario ne porte pas une ligne "quest = <s>". */

/* --- LA RESOLUTION CHOISIE DANS OPTIONS > SETTINGS (2026-10-06) -----------
 *
 * `--options-resolution` pose dans la section .greffe du moteur une zone qui
 * commence par la magie " VF5RESOL ", suivie de la valeur COURANTE (+8), de la
 * valeur CONFIRMEE (+0xC, que la validation de la page y recopie) et des cinq
 * couples largeur/hauteur (+0x10).
 *
 * ON LA TROUVE EN BALAYANT LA SECTION, et pas a une adresse en dur : la
 * disposition de la greffe bouge a chaque option ajoutee -- GRE_RES vaut
 * 0x2FC0 aujourd hui et vaudra autre chose demain -- alors que la magie, elle,
 * ne bouge pas.
 *
 * POURQUOI ON SURVEILLE LA VALEUR CONFIRMEE ET NON LA COURANTE : sans cela le
 * jeu se fermerait des le premier appui sur la fleche, avant meme d avoir
 * montre le choix.
 *
 * ET POURQUOI ON QUITTE. La resolution ne peut pas changer a chaud : la chaine
 * d echange de vfes.exe et les cibles de rendu du moteur sont creees UNE FOIS
 * au demarrage, depuis quatre immediats statiques. On ecrit donc le choix dans
 * ram\resolution.txt -- du TEXTE, pour qu un .cmd le relise par " set /p " --
 * on force la sauvegarde du personnage, et on sort. Le lanceur relit et
 * rouvre. C est ce que Frederic a choisi : " ligne en jeu + relance
 * automatique ". */
#define RES_MAGIE   "VF5RESOL"
#define RES_O_VAL   0x08
#define RES_O_CONF  0x0C
#define RES_O_LISTE 0x10
#define RES_MAX     5

/* POURQUOI LA RECHERCHE N EST PAS UNIQUE, et c est la capture du 2026-10-07
 * qui l a appris -- "au redemarrage le changement de resolution n est pas
 * applique", et le journal disait pourquoi en TROISIEME LIGNE :
 *
 *     RES    pas de zone VF5RESOL dans .greffe : le moteur n a pas ete
 *            patche avec --options-resolution
 *
 * Or il l etait : la magie etait bien dans la DLL, a l offset 0x6A77C0, avec
 * ses cinq couples. Ce qui manquait n etait pas la zone mais LE MOMENT.
 * `apm.dll` est chargee bien AVANT `vf5fs-pxd-w64-Retail_APM3.dll` (le releve
 * de `analysis/resolution.txt` les montre dans cet ordre, le moteur n arrivant
 * qu apres d3d11, dxgi et D3DCompiler), donc au premier `Core_execute`
 * `GetModuleHandleA` rend NULL -- et `g_res_cherche = 1` fermait la recherche
 * pour toute la session. Valider ne pouvait donc RIEN faire : ni ecrire le
 * fichier, ni fermer le jeu. C est la meme faute que le compte lu sur un tas
 * fraichement alloue : un releve pris trop tot ne dit pas "absent", il ne
 * dit RIEN.
 *
 * Deux remedes, et il faut les deux :
 *   - on distingue "pas encore la" (on REESSAYE au battement suivant) de
 *     "la, mais sans zone" (la, et la seulement, on abandonne) ;
 *   - chaque diagnostic est trace UNE fois, pour ne pas inonder le journal.
 *
 * RES_ATTEND est donc un etat, pas un echec. */
#define RES_TROUVE  0   /* la zone est la                                   */
#define RES_ATTEND  1   /* le moteur n est pas encore charge -> on reessaye  */
#define RES_SANS    2   /* le moteur est la, mais pas de zone -> on abandonne*/

static unsigned char *g_res;
static unsigned g_res_conf;
static int g_res_fini;          /* 1 = on ne cherche plus, dans les deux sens */
static int g_res_dit;           /* le diagnostic deja trace                   */

/* LA RECHERCHE EST GENERIQUE depuis le 2026-10-07 : `--options-mode` pose une
 * SECONDE zone dans la meme section, et rien ne justifiait d en recopier le
 * balayage. `magie` fait toujours huit octets, `besoin` est la taille minimale
 * de la zone (pour ne pas la reconnaitre a cheval sur la fin de section). */
static unsigned char *greffe_chercher(const char *magie, size_t besoin,
                                      int *etat)
{
    HMODULE h;
    unsigned char *b;
    IMAGE_DOS_HEADER *dos;
    IMAGE_NT_HEADERS64 *nt;
    IMAGE_SECTION_HEADER *s;
    unsigned i;
    *etat = RES_ATTEND;
    h = GetModuleHandleA("vf5fs-pxd-w64-Retail_APM3.dll");
    if (!h) return NULL;                       /* pas encore chargee */
    b = (unsigned char *)h;
    dos = (IMAGE_DOS_HEADER *)b;
    if (!page_lisible(b, 0x40, 0) || dos->e_magic != IMAGE_DOS_SIGNATURE)
        return NULL;                           /* en cours de mappage */
    nt = (IMAGE_NT_HEADERS64 *)(b + dos->e_lfanew);
    if (!page_lisible(nt, sizeof *nt, 0) || nt->Signature != IMAGE_NT_SIGNATURE)
        return NULL;
    s = IMAGE_FIRST_SECTION(nt);
    for (i = 0; i < nt->FileHeader.NumberOfSections; i++, s++) {
        unsigned char *p;
        size_t n, k;
        if (memcmp(s->Name, ".greffe", 7) != 0) continue;
        p = b + s->VirtualAddress;
        n = s->Misc.VirtualSize;
        if (!page_lisible(p, n, 0)) return NULL;   /* pas encore mappee */
        /* la zone est alignee sur 0x40 ; un pas de huit est large et sur */
        for (k = 0; k + besoin <= n; k += 8)
            if (memcmp(p + k, magie, 8) == 0) {
                *etat = RES_TROUVE;
                return p + k;
            }
        /* la section EST la et ne porte pas la magie : c est definitif */
        *etat = RES_SANS;
        return NULL;
    }
    /* le module est charge et n a pas de .greffe du tout : definitif aussi */
    *etat = RES_SANS;
    return NULL;
}

static unsigned char *res_trouver(int *etat)
{
    return greffe_chercher(RES_MAGIE, RES_O_LISTE + 8 * RES_MAX, etat);
}

/* LE DIAGNOSTIC COMPLET, et il remplace un message qui mentait.
 *
 * Le 2026-10-07, apres la premiere correction, le journal disait "on
 * cherchera au battement suivant" -- et plus jamais rien. Deux explications
 * tenaient dans ce silence, et aucune ne se distinguait de l autre :
 *   - `Core_execute` ne bat plus une fois le moteur charge, donc `res_tic`
 *     n est jamais rappele ;
 *   - il bat, et c est `res_trouver` qui echoue toujours.
 * Un seul essai doit trancher : on trace donc l ETAT A CHAQUE ETAPE a
 * quelques tours choisis, et le compteur de tours dit a lui seul si le
 * battement tourne. */
static unsigned g_res_tours;

static void res_diag(void)
{
    HMODULE h;
    unsigned char *b;
    IMAGE_DOS_HEADER *dos;
    IMAGE_NT_HEADERS64 *nt;
    IMAGE_SECTION_HEADER *s;
    unsigned i;
    h = GetModuleHandleA("vf5fs-pxd-w64-Retail_APM3.dll");
    if (!h) {
        trace("RES/DIAG tour %u : GetModuleHandleA rend NULL -- le moteur "
              "n est pas (encore) charge sous ce nom", g_res_tours);
        return;
    }
    b = (unsigned char *)h;
    dos = (IMAGE_DOS_HEADER *)b;
    if (!page_lisible(b, 0x40, 0) || dos->e_magic != IMAGE_DOS_SIGNATURE) {
        trace("RES/DIAG tour %u : module a %p mais en-tete DOS illisible "
              "ou sans MZ", g_res_tours, (void *)b);
        return;
    }
    nt = (IMAGE_NT_HEADERS64 *)(b + dos->e_lfanew);
    if (!page_lisible(nt, sizeof *nt, 0) || nt->Signature != IMAGE_NT_SIGNATURE) {
        trace("RES/DIAG tour %u : en-tete NT illisible ou sans PE",
              g_res_tours);
        return;
    }
    s = IMAGE_FIRST_SECTION(nt);
    trace("RES/DIAG tour %u : module a %p, %u section(s)",
          g_res_tours, (void *)b, (unsigned)nt->FileHeader.NumberOfSections);
    for (i = 0; i < nt->FileHeader.NumberOfSections; i++, s++) {
        char nom[9];
        memcpy(nom, s->Name, 8);
        nom[8] = 0;
        trace("RES/DIAG     [%u] %-8s VA=%08X VS=%06X %s", i, nom,
              (unsigned)s->VirtualAddress, (unsigned)s->Misc.VirtualSize,
              page_lisible(b + s->VirtualAddress, s->Misc.VirtualSize, 0)
              ? "lisible" : "ILLISIBLE");
        /* Pour .greffe, on DETAILLE les regions : c est ce decoupage qui
         * faisait repondre "illisible" a l ancien controle, et le voir
         * ecrit est ce qui distingue une mesure d une explication. */
        if (memcmp(s->Name, ".greffe", 7) == 0) {
            MEMORY_BASIC_INFORMATION mbi;
            const char *d = (const char *)(b + s->VirtualAddress);
            const char *fin = d + s->Misc.VirtualSize;
            unsigned r = 0;
            while (d < fin && r < 8) {
                if (!VirtualQuery(d, &mbi, sizeof mbi)) break;
                trace("RES/DIAG         region %u : base=%p taille=%06X "
                      "etat=%08X prot=%08X", r, mbi.BaseAddress,
                      (unsigned)mbi.RegionSize, (unsigned)mbi.State,
                      (unsigned)mbi.Protect);
                if ((const char *)mbi.BaseAddress + mbi.RegionSize <= d) break;
                d = (const char *)mbi.BaseAddress + mbi.RegionSize;
                r++;
            }
        }
    }
}

static void res_tic_corps(void)
{
    unsigned conf, l, h;
    char chemin[MAX_PATH];
    FILE *f;
    if (!g_res) {
        int etat;
        if (g_res_fini) return;
        /* Le compteur AVANT la recherche : s il reste a 1 dans le journal,
         * c est que le battement s est arrete, et non que la zone manque. */
        g_res_tours++;
        g_res = res_trouver(&etat);
        if (!g_res) {
            /* LE DIAGNOSTIC NE PARLE QUE QUAND CA VA MAL. Le tracer avant la
             * recherche noyait le journal de douze lignes a chaque lancement
             * reussi ; ici il ne sort que si la zone manque vraiment, et a
             * trois tours espaces pour montrer si l etat evolue. */
            if (g_res_tours == 1 || g_res_tours == 600 || g_res_tours == 6000)
                res_diag();
            if (etat == RES_SANS) {
                g_res_fini = 1;
                trace("RES    pas de zone " RES_MAGIE " dans .greffe : le "
                      "moteur n a pas ete patche avec --options-resolution");
            } else if (!g_res_dit) {
                g_res_dit = 1;
                trace("RES    le moteur n est pas encore charge ; on "
                      "cherchera la zone " RES_MAGIE " au battement suivant");
            }
            return;
        }
        g_res_fini = 1;
        memcpy(&g_res_conf, g_res + RES_O_CONF, 4);
        memcpy(&l, g_res + RES_O_LISTE + 8 * (g_res_conf % RES_MAX), 4);
        memcpy(&h, g_res + RES_O_LISTE + 8 * (g_res_conf % RES_MAX) + 4, 4);
        trace("RES    zone trouvee au tour %u ; resolution en place : "
              "%u x %u (entree %u). La ligne Resolution est vivante.",
              g_res_tours, l, h, g_res_conf);
        return;
    }
    memcpy(&conf, g_res + RES_O_CONF, 4);
    if (conf == g_res_conf) return;
    if (conf >= RES_MAX) {
        trace("RES    entree %u hors de la liste, ignoree", conf);
        g_res_conf = conf;
        return;
    }
    memcpy(&l, g_res + RES_O_LISTE + 8 * conf, 4);
    memcpy(&h, g_res + RES_O_LISTE + 8 * conf + 4, 4);
    g_res_conf = conf;
    _snprintf(chemin, sizeof chemin, "%sram\\resolution.txt", g_dossier);
    f = fopen(chemin, "w");
    if (!f) {
        trace("RES    %s impossible a ecrire, le choix est perdu", chemin);
        return;
    }
    fprintf(f, "%u %u\n", l, h);
    fclose(f);
    trace("RES    choix confirme : %u x %u, ecrit dans %s. Le jeu se ferme "
          "pour que le lanceur le rouvre dans cette resolution.", l, h, chemin);
    /* La sauvegarde du personnage AVANT de sortir : cust_tic n ecrit que
     * lorsque la somme a change, et la temporisation de 500 ms pourrait
     * retenir les dernieres modifications. */
    g_cust_date = 0;
    cust_tic();
    g_opt_date = 0;
    opt_tic();
    ExitProcess(0);
}

/* DEUX FILS L APPELLENT DESORMAIS -- le battement de la carte
 * (`Core_execute`) et le fil du moteur (`Input_isOn`). Un verrou NON
 * BLOQUANT suffit : si l autre fil est deja dedans, ce tour-ci ne sert a
 * rien et on sort. On ne prend pas de section critique, parce que ce corps
 * fait des entrees-sorties et peut terminer le processus -- un fil qui
 * mourrait en la tenant bloquerait l autre pour toujours. */
static volatile LONG g_res_dans;

static void res_tic(void)
{
    if (InterlockedCompareExchange(&g_res_dans, 1, 0) != 0) return;
    res_tic_corps();
    InterlockedExchange(&g_res_dans, 0);
}

/* --- LE MODE DE JEU : CONSOLE OU ARCADE D ORIGINE (2026-10-07) ------------
 *
 * Meme forme que la resolution, et pour la meme raison : `game_mode` n est pas
 * lu par le moteur mais ECRIT PAR `vfes.exe` (0x140002E1C), qui le passe a
 * `module_start` ; le moteur en derive alors quatre drapeaux globaux UNE FOIS
 * (0x180C3B701 = l aiguillage borne/console, 32 references). Rien ne peut donc
 * changer a chaud -- c est encore plus net que pour la resolution, puisque
 * l octet est dans l AUTRE binaire. On ecrit le choix dans ram\mode.txt et on
 * sort ; le lanceur relit et repatche avec la bonne ligne.
 *
 * DEUX PORTES, parce qu une seule ne suffit pas : en mode arcade l ecran
 * OPTIONS > Settings du menu console n existe pas. L aller se prend donc dans
 * Settings (sixieme ligne), et le RETOUR dans le menu TEST de la borne
 * (`apm3TestMode::MenuTop`, septieme ligne "CONSOLE MODE"), ou les deux
 * relais du patcheur posent CONF. Les deux ecrivent dans la meme zone.
 *
 * Le fichier porte un MOT, pas un chiffre : un `.cmd` le relit tel quel, et il
 * se lit a l oeil quand on va voir pourquoi le jeu a demarre dans un mode. */
#define MOD_MAGIE   "VF5MODE"          /* 7 + le NUL = les 8 octets compares */
#define MOD_O_VAL   0x08
#define MOD_O_CONF  0x0C
#define MOD_MAX     2

static unsigned char *g_mod;
static unsigned g_mod_conf;
static int g_mod_fini;

static void mod_tic_corps(void)
{
    static const char *NOMS[MOD_MAX] = { "console", "arcade" };
    unsigned conf;
    char chemin[MAX_PATH];
    FILE *f;
    if (!g_mod) {
        int etat;
        if (g_mod_fini) return;
        g_mod = greffe_chercher(MOD_MAGIE, MOD_O_CONF + 4, &etat);
        if (!g_mod) {
            /* RES_SANS est normal ici : `--options-mode` est une option, et
             * le build courant peut tres bien ne pas la porter. On se tait,
             * au lieu d annoncer un defaut qui n en est pas un. */
            if (etat == RES_SANS) g_mod_fini = 1;
            return;
        }
        g_mod_fini = 1;
        memcpy(&g_mod_conf, g_mod + MOD_O_CONF, 4);
        trace("MODE   zone " MOD_MAGIE " trouvee ; mode en place : %s",
              g_mod_conf < MOD_MAX ? NOMS[g_mod_conf] : "?");
        return;
    }
    memcpy(&conf, g_mod + MOD_O_CONF, 4);
    if (conf == g_mod_conf) return;
    if (conf >= MOD_MAX) {
        trace("MODE   valeur %u hors de la liste, ignoree", conf);
        g_mod_conf = conf;
        return;
    }
    g_mod_conf = conf;
    _snprintf(chemin, sizeof chemin, "%sram\\mode.txt", g_dossier);
    f = fopen(chemin, "w");
    if (!f) {
        trace("MODE   %s impossible a ecrire, le choix est perdu", chemin);
        return;
    }
    fprintf(f, "%s\n", NOMS[conf]);
    fclose(f);
    trace("MODE   choix confirme : %s, ecrit dans %s. Le jeu se ferme pour "
          "que le lanceur le rouvre dans ce mode.", NOMS[conf], chemin);
    g_cust_date = 0;
    cust_tic();
    g_opt_date = 0;
    opt_tic();
    ExitProcess(0);
}

static volatile LONG g_mod_dans;

static void mod_tic(void)
{
    if (InterlockedCompareExchange(&g_mod_dans, 1, 0) != 0) return;
    mod_tic_corps();
    InterlockedExchange(&g_mod_dans, 0);
}

/* --- LE STYLE DES PASTILLES DE BOUTONS (2026-10-11) ----------------------
 *
 * Troisieme de la meme famille, et la raison est encore une mesure : LA
 * PLANCHE EST RESIDENTE. `rom/2d/spr_n_fnt32.farc` est lue au demarrage ;
 * l echanger en cours de partie ne change rien a l ecran. Le choix ne peut
 * donc s appliquer qu au lancement suivant -- comme la resolution, comme le
 * mode.
 *
 * La zone est celle de la refonte des menus (`--options-v2`), magie
 * " VF5OPTV2 " : +0x60 la valeur courante, +0x64 la CONFIRMEE. On surveille
 * la confirmee, pour la meme raison que partout ailleurs : sans cela le jeu
 * se fermerait des le premier appui sur une fleche.
 *
 * Le fichier porte un MOT -- ps3, ps4, ps5, x360, xone -- parce qu un `.cmd`
 * le relit tel quel et qu il se lit a l oeil. */
#define BTN_MAGIE   "VF5OPTV2"
#define BTN_O_VAL   0x60
#define BTN_O_CONF  0x64
#define BTN_MAX     5

static unsigned char *g_btn;
static unsigned g_btn_conf;
static int g_btn_fini;

static void btn_tic_corps(void)
{
    static const char *NOMS[BTN_MAX] = { "ps3", "ps4", "ps5", "x360", "xone" };
    unsigned conf;
    char chemin[MAX_PATH];
    FILE *f;
    if (!g_btn) {
        int etat;
        if (g_btn_fini) return;
        g_btn = greffe_chercher(BTN_MAGIE, BTN_O_CONF + 4, &etat);
        if (!g_btn) {
            /* `--options-v2` est une option : son absence n est pas un
             * defaut, et on se tait. */
            if (etat == RES_SANS) g_btn_fini = 1;
            return;
        }
        g_btn_fini = 1;
        memcpy(&g_btn_conf, g_btn + BTN_O_CONF, 4);
        trace("BTN    zone " BTN_MAGIE " trouvee ; style en place : %s",
              g_btn_conf < BTN_MAX ? NOMS[g_btn_conf] : "?");
        return;
    }
    memcpy(&conf, g_btn + BTN_O_CONF, 4);
    if (conf == g_btn_conf) return;
    if (conf >= BTN_MAX) {
        trace("BTN    valeur %u hors de la liste, ignoree", conf);
        g_btn_conf = conf;
        return;
    }
    g_btn_conf = conf;
    _snprintf(chemin, sizeof chemin, "%sram\\boutons.txt", g_dossier);
    f = fopen(chemin, "w");
    if (!f) {
        trace("BTN    %s impossible a ecrire, le choix est perdu", chemin);
        return;
    }
    fprintf(f, "%s\n", NOMS[conf]);
    fclose(f);
    trace("BTN    choix confirme : %s, ecrit dans %s. Le jeu se ferme pour "
          "que le lanceur repose la planche et le rouvre.", NOMS[conf],
          chemin);
    g_cust_date = 0;
    cust_tic();
    g_opt_date = 0;
    opt_tic();
    ExitProcess(0);
}

static volatile LONG g_btn_dans;

static void btn_tic(void)
{
    if (InterlockedCompareExchange(&g_btn_dans, 1, 0) != 0) return;
    btn_tic_corps();
    InterlockedExchange(&g_btn_dans, 0);
}


/* --- LA SAISIE DU NOM DE DONNEES, AU CLAVIER (2026-10-13) -----------------
 *
 * " Edit data name " du CUSTOMIZE MENU. Le chemin est celui de SEGA, entier ;
 * `patch_moteur.py --nom-donnees` relaie ses TROIS sites vers la greffe, et
 * c est ici qu on remplit la boite aux lettres.
 *
 * CE QUE LA LIGNE FAISAIT, mesure du 2026-10-13 : elle EFFACAIT le nom.
 * `0x18005F840` rend un pointeur sur une chaine VIDE (0x180347568, longueur
 * zero) et `0x180029FB0` rend `mov al,1` -- toujours " saisie finie ". La
 * mise a jour recopiait donc "" dans l enregistrement par
 * `strcpy_s(enregistrement+0x90, "", 0x15)`.
 *
 * LA BOITE AUX LETTRES, zone " VF5NAME " de la greffe :
 *
 *     +0x08  etat     0 repos, 1 saisie, 2 valide, 3 annule, 4 abandon
 *     +0x0C  maxi     ce que le moteur a demande -- 0x14, vingt caracteres
 *     +0x10  present  NOUS y posons 1 : sans cela le relais pose l etat 4
 *     +0x14  long     la longueur courante
 *     +0x18  tampon   0x28 octets
 *
 * LE MENU EST GELE PENDANT LA SAISIE, ET C EST LE MOTEUR QUI LE FAIT :
 * `0x1801C4F9C` saute par-dessus `0x1801C4FF5`, son traitement des entrees,
 * tant que le drapeau `[page+0x2A0]` est pose. Rien a neutraliser de ce
 * cote -- mais on coupe quand meme `lire_clavier`, parce que les AUTRES
 * taches de la page, elles, lisent toujours.
 *
 * LES CODES VIRTUELS SONT DEJA LES CARACTERES : `VK_A` a `VK_Z` valent
 * 0x41..0x5A, soit " A " a " Z ", et `VK_0` a `VK_9` valent 0x30..0x39. Sur un
 * clavier AZERTY, Windows attribue ces codes PAR CARACTERE de la disposition
 * primaire : la touche qui porte " A " rend bien VK_A. Aucune table a ecrire.
 *
 * Entree valide, Echap annule -- et annuler rend NULL au moteur, qui saute la
 * recopie en `0x1801C4FB8` : le nom reste celui qu il etait.
 *
 * Se coupe par " sauvegarde = 0 " dans apm_entrees.txt, comme le reste : sans
 * ce tour de garde, `present` reste a zero et la ligne ne fait rien.
 * -------------------------------------------------------------------------- */
#define NOM_MAGIE      "VF5NAME"     /* 7 + le NUL = les 8 octets compares */
#define NOM_O_ETAT     0x08
#define NOM_O_MAXI     0x0C
#define NOM_O_PRESENT  0x10
#define NOM_O_LONG     0x14
/* LA DESTINATION DU MOTEUR, rangee par le relais `ouvrir` : c est
 * `enregistrement + 0x68`, le champ du nom. On y relit le nom COURANT pour
 * ouvrir le champ dessus -- sinon valider sans rien taper l effacerait. */
#define NOM_O_DEST     0x18
#define NOM_O_TAMPON   0x20
#define NOM_TAMPON     0x20          /* la place reservee dans la zone */
#define NOM_O_PAGE     0x40          /* la page, rangee par le relais */
#define NOM_O_DESSIN   0x48          /* NOTRE dessin, publie ici */
#define NOM_O_CURSEUR  0x50          /* la case choisie dans la grille */
#define NOM_MAXI       20            /* ce que le moteur recopie, moins le zero */

static unsigned char *g_nom;
static int            g_nom_fini;
static int            g_nom_saisie;  /* lu par lire_clavier */
static unsigned char  g_nom_vu[256]; /* l etat precedent de chaque touche */
static unsigned       g_nom_pad;     /* l etat precedent de la manette */

/* Le caractere d un code virtuel, ou zero. Voir le commentaire plus haut :
 * les codes SONT les caracteres pour les lettres et les chiffres. */
/* MAJUSCULE OU MINUSCULE : Maj et Verr.Maj, par un OU EXCLUSIF, comme le
 * fait n importe quel clavier. Les codes virtuels des lettres valent
 * 'A'..'Z' : les rendre tels quels donnait TOUJOURS une majuscule, et c est
 * pourquoi les minuscules manquaient aussi au clavier physique. Sans rien de
 * tenu, c est minuscule -- un nom se tape comme un mot. */
static int nom_car(int vk)
{
    int maj = ((GetAsyncKeyState(VK_SHIFT) & 0x8000) ? 1 : 0)
            ^ ((GetKeyState(VK_CAPITAL) & 1) ? 1 : 0);
    if (vk >= 'A' && vk <= 'Z') return maj ? vk : vk + 32;
    if (vk >= '0' && vk <= '9') return vk;
    if (vk >= VK_NUMPAD0 && vk <= VK_NUMPAD9) return '0' + (vk - VK_NUMPAD0);
    if (vk == VK_SPACE) return ' ';
    if (vk == VK_OEM_MINUS || vk == VK_SUBTRACT) return '-';
    if (vk == VK_OEM_PERIOD || vk == VK_DECIMAL) return '.';
    return 0;
}

static void nom_poser(unsigned o, unsigned v)
{
    memcpy(g_nom + o, &v, 4);
}

static unsigned nom_lire(unsigned o)
{
    unsigned v;
    memcpy(&v, g_nom + o, 4);
    return v;
}

/* --- LE CLAVIER VIRTUEL DU NOM DE DONNEES (2026-10-13) --------------------
 *
 * La saisie marchait mais etait AVEUGLE : le journal du 2026-10-13 montre que
 * Frederic tapait ses touches de menu (X C W V B) sans savoir que la capture
 * etait ouverte. On dessine donc le champ et une grille, et on les commande
 * aux directions -- clavier OU manette, puisque le stub lit deja les deux.
 *
 * OU CA SE DESSINE. La vtable du CUSTOMIZE MENU est 0x18052FCF8 et son
 * CRENEAU 4, 0x1801C51B0, est la phase de rendu. Le relais de la greffe
 * appelle d abord ce dessin d origine, puis saute ICI : notre code tourne donc
 * sur le fil du moteur, dans la bonne phase, et par-dessus le reste.
 *
 * L IDIOME EST CELUI DE CETTE PAGE, transcrit et non invente -- lu en
 * 0x1801C51B0 :
 *
 *     0x180187AA0()            lit le calque 2D courant
 *     0x180187CB0(2)           le pose a 2      <- et on le REMET a la fin
 *     0x1801BDA10(fenetre)     la fenetre est-elle prete ?
 *     0x18019A8C0(desc)        descripteur, 0x50 octets
 *     0x18019A9D0(style)       style, 0x40 octets
 *     0x1801BCD70(fenetre, &vec3, "p_txt_01_lt", 1)   l ANCRE -> x, y
 *     0x18019B6F0(style, 1)    mode de police
 *     0x18019B870(style, 2)    sous-mode
 *     0x18019B830(style, t)    taille
 *     0x18019B300(desc, "%s", chaine)                 le dessin
 *
 * Les champs du descripteur, releves aux memes adresses que la page :
 *     +0x08 couleur   +0x24 rang   +0x2C = 9   +0x34..+0x40 la boite
 *     +0x48 le style
 * La couleur range le ROUGE EN PREMIER (R, G, B, A).
 *
 * LE DESCRIPTEUR EST RECONSTRUIT A CHAQUE LIGNE, comme le fait la page : elle
 * rappelle 0x18019A8C0 entre ses deux groupes de texte (0x1801C5368).
 * -------------------------------------------------------------------------- */
#define CLV_LIRE_CALQUE   0x187AA0
#define CLV_POSER_CALQUE  0x187CB0
#define CLV_FEN_PRETE     0x1BDA10
#define CLV_DESC_INIT     0x19A8C0
#define CLV_STYLE_INIT    0x19A9D0
#define CLV_ANCRE         0x1BCD70
#define CLV_STYLE_MODE    0x19B6F0
#define CLV_STYLE_SMODE   0x19B870
#define CLV_STYLE_TAILLE  0x19B830
#define CLV_DESSINER      0x19B300
#define CLV_FORMAT        0x347CF8          /* la chaine "%s" du moteur */
#define CLV_FEN           0x240             /* page + 0x240 : sa fenetre */
#define CLV_ANCRE_NOM     "p_txt_01_lt"
/* NOTRE FENETRE. `0x1801BDA20(fen, rang)` l ouvre sur un bloc a zero : il ne
 * fait qu y poser le rang et l etat 1 (0x1801BDA7C). Le tic la charge, l etat
 * 3 la dit prete, et `0x1801BBA20` DEUX FOIS la referme (3 -> 4, puis
 * liberation). Le RANG vient de la table 0x18052E680 : 0x13 = choice_win_08,
 * huit bandes de CONTENU -- le titre ne compte pas.
 *
 * ET SES ANCRES REGLENT LES RESOLUTIONS : on dessine sur les ancres de NOTRE
 * fenetre, pas a des pixels comptes pour 1920 x 1080. */
#define NOM_O_FENETRE     0x180
#define CLV_OUVRIR        0x1BDA20
#define CLV_FERMER        0x1BBA20
#define CLV_TIC           0x1BBB10
#define CLV_RANG          0x13
/* LE CONSTRUCTEUR, ET POURQUOI IL EST OBLIGATOIRE (mesure du 2026-10-15).
 * Le journal ne portait qu une ligne : etat 2, pas prete -- la machine
 * s arretait au chargement. 0x1801BBB10 dit que l etat 2 attend
 * 0x180029770([fen+0x10]), la fin du marqueur `sta`. Et 0x1801BE520 recopie
 * [fen+0x0C] dans la requete (+0x80) : c est la VITESSE d animation. Sur un
 * bloc a zero elle vaut 0.0, donc `sta` n avance JAMAIS.
 * 0x1801BD0B0 est ce qui la met a 1.0f -- plus la visibilite ([fen+8] = 1) et
 * la priorite ([fen+0x48] = 10). La page l appelle en 0x1801C5B82, juste
 * avant d ouvrir : `0x1801BDA20` ne pose que le rang et l etat, il ne
 * remplace pas ce reglage. C etait la piece manquante, pas le rang. */
#define CLV_CONSTRUIRE    0x1BD0B0
#define CLV_PRIORITE      0x1BE8E0
/* LA PRIORITE NE SE DEDUIT PAS -- TROIS LECTURES, TROIS REPONSES :
 *   - 0x1801BE520 donne au curseur [fen+0x48] + 1 : si le curseur est devant,
 *     plus grand = devant ;
 *   - mais les 86 sites de 0x1801BE8E0 donnent 0x01 au fond `bg_base` (rang
 *     0x54) et 0x15 au fond `bg` (rang 0x55) -- les deux bouts de l echelle
 *     pour deux fonds ;
 *   - et la capture du 2026-10-15 montre notre 0x20 DERRIERE le 0x0E de la
 *     page, ce qui contredit la premiere.
 * Donc on ne lit plus, on balaie : PAGE-HAUT et PAGE-BAS la changent pendant
 * la saisie, le journal dit la valeur, et l ecran tranche. L echelle employee
 * par le moteur va de 0x01 a 0x19. */
/* LA PRIORITE EST MESUREE (2026-10-15). Un seul appui de 0x0D vers 0x0E a
 * fait passer le cadre DEVANT : PLUS GRAND EST DEVANT. Le 0x20 d avant
 * echouait parce qu il sortait de l echelle employee par le moteur, qui va
 * de 0x01 a 0x19 sur ses 86 sites. On prend 0x10 -- une valeur que le moteur
 * emploie lui-meme douze fois, franchement au-dessus du 0x0E de la page. */
#define CLV_PRIORITE_VAL  0x10

/* LE PLACEMENT, LUI, RESTE A REGLER A L ECRAN. L espace libre sous le
 * panneau du personnage fait environ 240 unites de reference (1280 x 768) et
 * `choice_win_08` en fait 324 : descendre ne suffit pas, il faut aussi
 * pouvoir changer de cadre. Les deux sont donc reglables ET AFFICHES.
 *
 * `0x1801BE520` lit [fen+0x4C] (x) et [fen+0x50] (y) a l ouverture et les
 * passe a 0x180029D00 : c est un DECALAGE sur la position dessinee, dans le
 * repere de la planche. Le constructeur les remet a zero -- on ecrit donc
 * APRES lui et AVANT d ouvrir.
 *
 * Clavier AZERTY COMPACT : ni Debut, ni Fin, ni touches de page. F1 et F2
 * sont prises (TEST et SERVICE). Fiche : reference_clavier_frederic. */
#define CLV_BAS(v)    ((v) == VK_F6 || (v) == VK_NEXT)
#define CLV_HAUT(v)   ((v) == VK_F5 || (v) == VK_PRIOR)
#define CLV_CADRE_P(v) ((v) == VK_F7)
#define CLV_CADRE_S(v) ((v) == VK_F8)
/* VINGT, ET NON DIX : dix appuis au lieu de vingt pour traverser l ecran. */
#define CLV_DY_PAS    20.0f
#define CLV_DY_MAXI   400.0f

/* Les cadres essayables, du plus court au plus haut. Hauteurs relevees dans
 * aet_n_cmn.bin (scene BASE, 1280 x 768) par tools/cadres_fenetres.py. */
typedef struct { int rang; const char *nom; } CLV_CADRE;
static const CLV_CADRE g_clv_cadres[] = {
    { 0x06, "l" },              /* cmn_win_l_01    cadre 762 x 180 */
    { 0x09, "xl" },             /* cmn_win_xl_01   cadre 762 x 216 */
    { 0x0A, "xxl" },            /* cmn_win_xxl_01  cadre 762 x 252 */
    { 0x13, "ch8" },            /* choice_win_08   cadre 762 x 324 */
};
#define CLV_N_CADRES ((int)(sizeof g_clv_cadres / sizeof g_clv_cadres[0]))
/* SOUS LE PANNEAU, ET NON PAR-DESSUS -- ET LE PLACEMENT SE CALCULE.
 *
 * La capture du 2026-10-15 (cadre xxl, dy +280) donne deux points : le cadre
 * occupait 495..747 en repere planche, et 655..1050 pixels a l ecran. D ou
 *
 *     px = 1,567 x ref - 121
 *
 * Controle : le bas de la planche (768) tombe a 1083 px pour un ecran de
 * 1080. Trois pixels -- la droite est bonne.
 *
 * Le panneau du personnage finit vers 735 px, soit 546 en repere planche. Il
 * faut donc haut >= 546 et bas <= 768 :
 *
 *     l    haut 180 : dy de 331 a 373   MARGE 42
 *     xl   haut 216 : dy de 331 a 337   marge 6
 *     xxl  haut 252 : NE TIENT PAS      il manque 30 unites
 *
 * `xxl` ne POUVAIT pas marcher, et c est pour ca que le panneau couvrait son
 * haut. `xl` tient a six unites pres -- moins que mon erreur de lecture sur
 * une capture. On prend `l`, au milieu de sa plage.
 *
 * F5 / F6 ajustent, F7 / F8 changent de cadre, et le reglage est RANGE. */
static int   g_clv_cadre;                      /* cmn_win_l_01 */
static float g_clv_dy = 352.0f;                /* le milieu de la plage */
/* L INTERIEUR DE LA FENETRE, et non plus un pas compte entre deux ancres :
 * `p_txt_02_lt` n existe NI dans choice_win_08 NI dans term_win -- le repli a
 * 30.0f etait donc pris a tous les coups. choice_win_08 porte p_txt_01_lt en
 * (288, 235) et p_txt_02_rb en (992, 519) : 704 x 284 pour huit lignes. */
#define CLV_ANCRE_RB      "p_txt_02_rb"
#define CLV_LIGNES        8

/* LA GRILLE : VINGT COLONNES SUR QUATRE RANGEES, et chaque chiffre est
 * calcule. Ce qui bride la taille des signes, c est le nombre de LIGNES.
 *
 * Il faut 80 cases : 26 majuscules, 26 minuscules, 10 chiffres, 16 signes de
 * ponctuation et les 4 commandes. En 20 x 4 :
 *
 *     lignes = 1 (le champ) + 4 + 1 (l aide) = 6
 *     h = 140 / 6 = 23,3 unites  ->  glyphes a 0,85 h = 31 px
 *     le signe mesure 0,485 x 31 = 15,1 px (mesure de l entree 222)
 *     il en tient 1113 / 15,1 = 73 par ligne, et on en emploie 60
 *
 * soit 82 % de la largeur. Les glyphes passent de 37 a 31 px : c est le prix
 * des minuscules, et il est chiffre. Ils restent plus gros que les 27 qui
 * avaient fait dire " il faut les agrandir ".
 *
 * LE SOULIGNE DE LA PONCTUATION EST DEVENU UN EGAL : la commande
 * ESPACE se dessine deja "_", et deux cases au meme dessin font
 * choisir au hasard. */
#define CLV_COL 20
#define CLV_RAN 4
/* le champ, les rangees, l aide */
#define CLV_LIGNES_TOT (CLV_RAN + 2)
#define CLV_CASES (CLV_COL * CLV_RAN)
#define CLV_ESPACE 1
#define CLV_EFFACE 2
#define CLV_VALIDE 3
#define CLV_ANNULE 4
static const char g_clv_grille[CLV_CASES + 1] =
    "ABCDEFGHIJKLMNOPQRST"
    "UVWXYZabcdefghijklmn"
    "opqrstuvwxyz01234567"
    "89.,-=/'!?():;+&\x01\x02\x03\x04";

typedef int   (*CLV_LIRE)(void);
typedef void  (*CLV_POSER)(int);
typedef char  (*CLV_PRETE)(void *);
typedef void  (*CLV_INIT)(void *);
/* CINQ ARGUMENTS, et le cinquieme compte : 0x1801BCDD5 lit
 * `[rsp+0x90]` et le TESTE. La page le met a zero avant chaque appel
 * (`mov [rsp+0x20], rdi` avec rdi nul). Ne pas le passer laissait la
 * fonction lire de la pile sale -- plantage mesure du 2026-10-13,
 * 0xC0000005 en 0x180024660 sur un nom a -1. */
typedef void  (*CLV_ANC)(void *, float *, const char *, char, void *);
typedef void  (*CLV_MODE)(void *, int);
typedef void  (*CLV_TAILLE)(void *, float);
typedef void  (*CLV_DESS)(void *, const char *, const char *);
typedef void  (*CLV_RANGER)(void *, int);
typedef void  (*CLV_UN)(void *);

static unsigned char *g_clv_base;        /* la base du moteur */
/* LE CALQUE COURANT, pour calculer notre profondeur. La recette validee le
 * 2026-09-08 (reference_vf5_texte_2d) : l indice de la commande 2D vaut
 *     (desc+0x24) + ((desc+0x28 + calque) << 5),   borne a 0..127,
 * soit QUATRE calques de TRENTE-DEUX rangs. On vise 127 -- le dernier
 * compartiment, dessine apres tout le reste -- en corrigeant NOTRE PROPRE
 * descripteur, jamais le calque global qui est partage. */
static int g_clv_calque;
/* L INDICE DE NOTRE COMMANDE 2D, et le sens MESURE (2026-10-15) :
 *   indice 82  -> visible, devant le texte de la page, derriere le portrait
 *   indice 127 -> derriere TOUT
 * donc PLUS GRAND = PLUS TOT = DERRIERE. La fiche reference_vf5_texte_2d dit
 * l inverse ; elle a ete validee sur TaskSelStage, un autre ecran, et sa
 * recette ne vaut pas ici. Avec un calque de 2 et un +0x28 qui ne peut pas
 * etre negatif, les indices atteignables vont de 64 a 127 : on vise 64. */
/* 82 : la seule valeur MESUREE qui passe devant le panneau du menu. 64 est
 * derriere lui (capture du 2026-10-15), 127 est derriere tout. */
static int g_clv_rang = 18;     /* desc+0x24 -> indice 18 + (0+2 << 5) = 82 */
static int g_clv_sup = 0;       /* desc+0x28 */

static void *clv_f(unsigned rva)
{
    return (void *)(g_clv_base + rva);
}

static void nom_bouger(int pas)
{
    int cur;
    if (!g_nom) return;
    cur = (int)nom_lire(NOM_O_CURSEUR) + pas;
    while (cur < 0) cur += CLV_CASES;
    while (cur >= CLV_CASES) cur -= CLV_CASES;
    nom_poser(NOM_O_CURSEUR, (unsigned)cur);
}

/* Une ligne de texte, a l endroit voulu et de la couleur voulue. */
static void clv_ligne(void *style, float x, float y, unsigned couleur,
                      const char *texte)
{
    /* ALIGNES A 16 : le moteur emploie `movaps` sur ces structures, et
     * une pile mal alignee serait un plantage immediat. */
    unsigned char desc[0x50] __attribute__((aligned(16)));
    memset(desc, 0, sizeof desc);
    ((CLV_INIT)clv_f(CLV_DESC_INIT))(desc);
    memcpy(desc + 0x08, &couleur, 4);
    *(float *)(desc + 0x34) = x;
    *(float *)(desc + 0x38) = y;
    *(float *)(desc + 0x3C) = x;
    *(float *)(desc + 0x40) = y;
    *(unsigned *)(desc + 0x2C) = 9;
    /* L INDICE 127, ET NON LE 0x12 DE LA PAGE. Le panneau du personnage
     * (0x1801C5540, appele en 0x1801C54F7) emploie le meme 0x12 que le
     * texte de la page : a rang egal, l ordre n est pas garanti, et c est
     * pour ca que le portrait passait devant la grille. */
    *(unsigned *)(desc + 0x24) = (unsigned)g_clv_rang;
    *(unsigned *)(desc + 0x28) = (unsigned)g_clv_sup;
    *(void **)(desc + 0x48) = style;
    ((CLV_DESS)clv_f(CLV_DESSINER))(desc, (const char *)clv_f(CLV_FORMAT),
                                    texte);
}

/* Le libelle d une case, sur TROIS colonnes. Quatre rendaient la grille large
 * de 635 pixels sur la capture du 2026-10-13 -- elle couvrait l ecran. Les
 * commandes tiennent donc en UN signe, et une ligne d aide les nomme. */
/* UNE CASE TIENT EN TROIS SIGNES, crochets compris -- et c est ce qui permet
 * de dessiner une RANGEE ENTIERE en une seule commande. Seize cases font 48
 * signes, soit 870 des 1113 pixels de l interieur : 78 % de la largeur. */
static void clv_case(char *s, char ch, int choisi)
{
    char c = ch;
    if (ch == CLV_ESPACE) c = '_';
    else if (ch == CLV_EFFACE) c = '<';
    else if (ch == CLV_VALIDE) c = '#';
    else if (ch == CLV_ANNULE) c = '*';
    s[0] = choisi ? '[' : ' ';
    s[1] = c;
    s[2] = choisi ? ']' : ' ';
}

/* UNE LIGNE ET SON OMBRE. Frederic : " sans fond pour le detacher des autres
 * menus en arriere plan ".
 *
 * LE LISERE DE NEUF PASSES A ETE ESSAYE ET RETIRE, et c est une mesure : la
 * capture du 2026-10-13 montrait TOUTE LA PLANCHE DE POLICE deversee en bas de
 * l ecran. Neuf passes par ligne font SOIXANTE-TROIS commandes 2D par trame,
 * toutes au MEME rang -- or le tableau du contexte 2D est BORNE : 128 cases,
 * quatre calques de trente-deux rangs (analysis/texte_2d.md S 8). Deux passes
 * suffisent a detacher le texte, et c est ce qui tient dans le tableau. */
static void clv_lisere(void *style, float x, float y, unsigned couleur,
                       const char *texte)
{
    clv_ligne(style, x + 2.0f, y + 2.0f, 0x000000FFu, texte);
    clv_ligne(style, x, y, couleur, texte);
}

/* LE REGLAGE SURVIT AUX RECOMPILATIONS. Sans ca, chaque build reposait
 * Frederic au depart et il fallait tout replacer a la main. Deux nombres
 * dans ram/clavier.txt : le cadre et le decalage. */
static void clv_reglage_chemin(char *c, int n)
{
    _snprintf(c, n, "%sram\\clavier.txt", g_dossier);
    c[n - 1] = 0;
}

/* A LA MAIN, ET NON AVEC fscanf : l appel a fscanf faisait passer apm.dll
 * de 117 760 a 156 160 octets -- toute la machinerie de scanf, avec ses
 * flottants, pour lire deux entiers. */
static const char *clv_entier(const char *p, int *v)
{
    int n = 0, s = 1;
    while (*p == 0x20 || *p == 0x09 || *p == 0x0D || *p == 0x0A) p++;
    if (*p == 0x2D) { s = -1; p++; }
    if (*p < 0x30 || *p > 0x39) return (const char *)0;
    while (*p >= 0x30 && *p <= 0x39) n = n * 10 + (*p++ - 0x30);
    *v = n * s;
    return p;
}

static void clv_reglage_lire(void)
{
    char c[MAX_PATH], ligne[64];
    FILE *f;
    const char *p;
    int cadre = -1, dy = 0;
    clv_reglage_chemin(c, sizeof c);
    f = fopen(c, "r");
    if (!f) return;
    ligne[0] = 0;
    fgets(ligne, (int)sizeof ligne, f);
    p = clv_entier(ligne, &cadre);
    if (p) p = clv_entier(p, &dy);
    if (p && cadre >= 0 && cadre < CLV_N_CADRES
            && dy >= -(int)CLV_DY_MAXI && dy <= (int)CLV_DY_MAXI) {
        g_clv_cadre = cadre;
        g_clv_dy = (float)dy;
        trace("NOM    reglage relu de ram\\clavier.txt : cadre %s, y %+d",
              g_clv_cadres[cadre].nom, dy);
    }
    fclose(f);
}

static void clv_reglage_ranger(void)
{
    char c[MAX_PATH];
    FILE *f;
    clv_reglage_chemin(c, sizeof c);
    f = fopen(c, "w");
    if (!f) return;
    fprintf(f, "%d %d\n", g_clv_cadre, (int)g_clv_dy);
    fclose(f);
}

/* Deplacer le curseur dans la grille, en bouclant. */
/* Notre fenetre est-elle prete ? Sinon on la pousse d un cran. */
static int g_clv_etat_vu = -1;

static void *clv_fenetre(void)
{
    unsigned char *fen = g_nom + NOM_O_FENETRE;
    unsigned etat;
    int pret;
    memcpy(&etat, fen, 4);
    if (etat == 0) {
        /* DANS L ORDRE DE LA PAGE (0x1801C5B82 .. 0x1801C5BA4) : construire,
         * puis la priorite, puis ouvrir. Le constructeur ecrit 0x5A dans
         * [fen+4] et l ouverture l ecrase par le rang -- l inverse perdrait
         * le rang, et 0x1801BCD70 refuse justement le rang 0x5A. */
        ((CLV_UN)clv_f(CLV_CONSTRUIRE))(fen);
        ((CLV_RANGER)clv_f(CLV_PRIORITE))(fen, CLV_PRIORITE_VAL);
        /* LE DECALAGE SE POSE ENTRE LES DEUX : le constructeur vient de
         * remettre [fen+0x48..0x53] a zero, et l ouverture n y touche pas. */
        memcpy(fen + 0x50, &g_clv_dy, 4);
        ((CLV_RANGER)clv_f(CLV_OUVRIR))(fen, g_clv_cadres[g_clv_cadre].rang);
    }
    ((CLV_UN)clv_f(CLV_TIC))(fen);
    memcpy(&etat, fen, 4);
    pret = ((CLV_PRETE)clv_f(CLV_FEN_PRETE))(fen) ? 1 : 0;
    /* ON MESURE, ON NE DEVINE PAS. L etat (1 a charger, 2 en cours, 3 prete)
     * ET l objet AET : [fen+0x10] est ce que 0x180029a90 a rendu. Zero = la
     * planche du rang n est pas chargee ; non nul = elle l est, et toute
     * panne restante est ailleurs. Deux pannes, deux chiffres. */
    if ((int)etat != g_clv_etat_vu) {
        unsigned objet;
        g_clv_etat_vu = (int)etat;
        memcpy(&objet, fen + 0x10, 4);
        trace("NOM    notre fenetre : etat %u, objet AET %u, cadre %s, "
              "y %+d, %s", etat, objet, g_clv_cadres[g_clv_cadre].nom,
              (int)g_clv_dy, pret ? "PRETE" : "pas prete");
    }
    return pret ? (void *)fen : (void *)0;
}

/* La refermer : DEUX appels d affilee (3 -> 4, puis liberation). */
static void clv_refermer(void)
{
    unsigned char *fen;
    unsigned etat;
    if (!g_nom || !g_clv_base) return;
    fen = g_nom + NOM_O_FENETRE;
    memcpy(&etat, fen, 4);
    if (!etat) return;
    ((CLV_UN)clv_f(CLV_FERMER))(fen);
    ((CLV_UN)clv_f(CLV_FERMER))(fen);
}

static void nom_dessin(void *page)
{
    unsigned char style[0x40] __attribute__((aligned(16)));
    float vec[4] __attribute__((aligned(16)));
    float vec2[4] __attribute__((aligned(16)));
    float pas, h, y0;
    int notre = 0;
    void *fen;
    int calque, r, c;
    unsigned lg, cur;
    char ligne[CLV_COL * 3 + 4];
    char champ[48];
    if (!g_nom || !g_clv_base || !page) return;
    if (nom_lire(NOM_O_ETAT) != 1) return;
    fen = (unsigned char *)page + CLV_FEN;
    calque = ((CLV_LIRE)clv_f(CLV_LIRE_CALQUE))();
    ((CLV_POSER)clv_f(CLV_POSER_CALQUE))(2);
    /* GARDE : l indice doit rester dans 0..127, sinon on sort du tableau de
     * 128 cases -- c est le plantage du 2026-09-08. Notre calque vaut 2 et
     * notre +0x28 au plus 1 : (1+2) << 5 = 96, plus 31 = 127. Dans la
     * borne. */
    g_clv_calque = 2;
    {
        void *mien = clv_fenetre();
        if (mien) { fen = mien; notre = 1; }   /* nos ancres, nos proportions */
    }
    if (((CLV_PRETE)clv_f(CLV_FEN_PRETE))(fen)) {
        memset(style, 0, sizeof style);
        ((CLV_INIT)clv_f(CLV_STYLE_INIT))(style);
        /* DEUX ANCRES, et c est ce qui rend le dessin independant de la
         * resolution : la premiere donne l origine, la seconde donne le PAS
         * entre deux lignes. Tout le reste -- position des rangees, taille des
         * glyphes -- s exprime en multiples de ce pas, jamais en pixels
         * comptes pour un ecran donne. */
        memset(vec, 0, sizeof vec);
        memset(vec2, 0, sizeof vec2);
        ((CLV_ANC)clv_f(CLV_ANCRE))(fen, vec, CLV_ANCRE_NOM, 1, (void *)0);
        ((CLV_ANC)clv_f(CLV_ANCRE))(fen, vec2, CLV_ANCRE_RB, 0, (void *)0);
        /* LES DEUX COINS DE L INTERIEUR, pas un pas devine : haut-gauche et
         * bas-droite. Le moteur les rend deja mis a l echelle de l ecran, si
         * bien que la hauteur de ligne sort d une division et vaut pour
         * toutes les resolutions. */
        pas = vec2[1] - vec[1];
        if (pas < 40.0f || pas > 900.0f) pas = 30.0f * CLV_LIGNES_TOT;
        h = pas / (float)CLV_LIGNES_TOT;

        /* SUR NOTRE FENETRE on part de son ancre. SUR CELLE DE LA PAGE il
         * faut descendre sous elle et sous le panneau du personnage : six
         * pas et demi, mesures sur la capture du 2026-10-13 -- et exprimes
         * EN PAS, donc valables a toute resolution. */
        y0 = vec[1] + (notre ? 0.0f : h * 6.5f);
        ((CLV_MODE)clv_f(CLV_STYLE_MODE))(style, 1);
        ((CLV_MODE)clv_f(CLV_STYLE_SMODE))(style, 2);
        ((CLV_TAILLE)clv_f(CLV_STYLE_TAILLE))(style, h * 0.85f);
        lg = nom_lire(NOM_O_LONG);
        if (lg > NOM_MAXI) lg = NOM_MAXI;
        cur = nom_lire(NOM_O_CURSEUR);
        if (cur >= CLV_CASES) cur = 0;
        memcpy(champ, g_nom + NOM_O_TAMPON, lg);
        champ[lg] = '_';
        champ[lg + 1] = 0;
        clv_lisere(style, vec[0], y0, 0xFFFFFFFFu, champ);
        /* UNE CHAINE PAR RANGEE, ET ON COMPTE LES COMMANDES. Dessiner
         * chaque case a son abscisse donnait 48 cases x 2 passes = 96
         * commandes 2D par trame, toutes au meme indice -- or SOIXANTE-TROIS
         * avaient suffi, le 2026-10-13, a deverser toute la planche de
         * police (le contexte 2D est borne a 128 compartiments). Trois
         * rangees, le champ et l aide : DIX commandes.
         * La largeur s obtient autrement, et mieux : en CINQ lignes au lieu
         * de huit les glyphes passent de 27 a 37 pixels, le signe mesure
         * 18,1 px, et 48 signes couvrent 870 des 1113 pixels utiles. */
        for (r = 0; r < CLV_RAN; r++) {
            int k = 0;
            for (c = 0; c < CLV_COL; c++) {
                clv_case(ligne + k, g_clv_grille[r * CLV_COL + c],
                         (r * CLV_COL + c) == (int)cur);
                k += 3;
            }
            ligne[k] = 0;
            clv_lisere(style, vec[0], y0 + h * (float)(r + 1),
                       0xFFC6C8D0u, ligne);
        }
        /* L AIDE PORTE L ETAT : Frederic a demande ou le cadre etait
         * indique, et il ne l etait nulle part -- seul le journal le
         * disait. Une ligne a l ecran vaut mieux qu une ligne dans un
         * fichier qu il faut aller ouvrir. */
        {
            char aide[96];
            /* TRENTE-CINQ SIGNES AU PLUS. Mesure sur la capture du
             * 2026-10-15 : la grille fait 24 signes pour environ 600 px a
             * 1920, soit 25 px le signe ; l interieur de la fenetre fait
             * 704 unites de reference, environ 990 px -- une quarantaine
             * de signes. Les 52 d avant debordaient. */
            sprintf(aide, "_esp  <eff  #ok  *ann     F5-F8  %s y%+d",
                    g_clv_cadres[g_clv_cadre].nom, (int)g_clv_dy);
            /* UNE TAILLE A ELLE : a 43 pixels le signe, ses trente-cinq
             * signes deborderaient du cadre. */
            ((CLV_TAILLE)clv_f(CLV_STYLE_TAILLE))(style, h * 0.45f);
            clv_lisere(style, vec[0], y0 + h * ((float)CLV_RAN + 1.2f),
                       0xFF60F5BFu, aide);
        }
    }
    ((CLV_POSER)clv_f(CLV_POSER_CALQUE))(calque);
}

static void nom_tic(void)
{
    unsigned etat, lg, maxi;
    int vk, bouge = 0;
    if (!g_sauvegarde) return;
    if (!g_nom) {
        int e;
        if (g_nom_fini) return;
        g_nom = greffe_chercher(NOM_MAGIE, NOM_O_CURSEUR + 4, &e);
        if (!g_nom) {
            /* RES_SANS est normal : `--nom-donnees` est une option, et le
             * build courant peut tres bien ne pas la porter. On se tait. */
            if (e == RES_SANS) g_nom_fini = 1;
            return;
        }
        g_nom_fini = 1;
        /* LE DESSIN SE PUBLIE AVANT LA PRESENCE : le relais lit l adresse et
         * ne saute que si elle est non nulle, mais autant ne jamais lui
         * offrir la fenetre. */
        g_clv_base = (unsigned char *)GetModuleHandleA(
            "vf5fs-pxd-w64-Retail_APM3.dll");
        {
            void *p = (void *)nom_dessin;
            memcpy(g_nom + NOM_O_DESSIN, &p, sizeof p);
        }
        nom_poser(NOM_O_CURSEUR, 0);
        clv_reglage_lire();
        nom_poser(NOM_O_PRESENT, 1);
        trace("NOM    zone " NOM_MAGIE " trouvee ; saisie et clavier virtuel "
              "tenus par le stub (moteur en %p)", (void *)g_clv_base);
        return;
    }
    etat = nom_lire(NOM_O_ETAT);
    if (etat != 1) {
        if (g_nom_saisie) {
            g_nom_saisie = 0;
            g_nom_pad = 0;
            memset(g_nom_vu, 0, sizeof g_nom_vu);
            clv_refermer();
        }
        return;
    }
    /* Le jeu doit avoir le premier plan : sinon on saisirait ce qui est tape
     * dans la fenetre du dessus. Meme garde que lire_clavier. */
    {
        DWORD pid = 0;
        HWND f = GetForegroundWindow();
        if (!f) return;
        GetWindowThreadProcessId(f, &pid);
        if (pid != GetCurrentProcessId()) return;
    }
    if (!g_nom_saisie) {
        unsigned char *dest;
        g_nom_saisie = 1;
        g_nom_pad = lire_manette();     /* les boutons tenus ne comptent pas */
        memset(g_nom_vu, 0, sizeof g_nom_vu);
        maxi = nom_lire(NOM_O_MAXI);
        /* LE CHAMP S OUVRE SUR LE NOM COURANT. Sans cela, valider sans rien
         * taper recopiait une chaine vide : c est ce que le journal du
         * 2026-10-13 montrait, dix-sept fois. */
        lg = 0;
        memcpy(&dest, g_nom + NOM_O_DEST, sizeof dest);
        if (dest && page_lisible(dest, NOM_MAXI + 1, 0)) {
            while (lg < NOM_MAXI && dest[lg] >= 0x20 && dest[lg] < 0x7F) {
                g_nom[NOM_O_TAMPON + lg] = dest[lg];
                lg++;
            }
        }
        g_nom[NOM_O_TAMPON + lg] = 0;
        nom_poser(NOM_O_LONG, lg);
        trace("NOM    saisie ouverte sur \"%s\", %u caractere(s) au plus "
              "(Entree valide, Echap annule, Retour efface)",
              (char *)(g_nom + NOM_O_TAMPON), maxi);
        return;                       /* on ne lit pas la trame d ouverture */
    }
    lg = nom_lire(NOM_O_LONG);
    if (lg > NOM_MAXI) lg = NOM_MAXI;
    for (vk = 8; vk < 256; vk++) {
        int bas = (GetAsyncKeyState(vk) & 0x8000) ? 1 : 0;
        int avant = g_nom_vu[vk];
        g_nom_vu[vk] = (unsigned char)bas;
        if (!bas || avant) continue;             /* seulement les appuis */
        if (vk == VK_RETURN) {
            /* UN CHAMP VIDE N EFFACE PAS : on annule. Le relais `texte` rend
             * alors NULL et le moteur saute la recopie (0x1801C4FB8). */
            if (!lg) {
                nom_poser(NOM_O_ETAT, 3);
                trace("NOM    champ vide : annule, le nom n est pas touche");
                return;
            }
            g_nom[NOM_O_TAMPON + lg] = 0;
            nom_poser(NOM_O_LONG, lg);
            nom_poser(NOM_O_ETAT, 2);
            trace("NOM    valide : \"%s\" (%u caractere(s))",
                  (char *)(g_nom + NOM_O_TAMPON), lg);
            return;
        }
        if (vk == VK_ESCAPE) {
            nom_poser(NOM_O_ETAT, 3);
            trace("NOM    annule -- le nom n est pas touche");
            return;
        }
        if (vk == VK_BACK) {
            if (lg) lg--;
            bouge = 1;
            continue;
        }
        /* LE BALAYAGE DE LA PRIORITE. Refermer DEUX FOIS remet l etat a 0
         * (0x1801BBA20 : 3 -> 4, puis liberation) ; la trame suivante
         * rouvre avec la valeur neuve, puisque c est a l ouverture que
         * 0x1801BE520 la lit. */
        /* PLACER LA FENETRE. Refermer DEUX FOIS remet l etat a 0
         * (0x1801BBA20 : 3 -> 4, puis liberation) ; la trame suivante
         * rouvre, et c est a l ouverture que 0x1801BE520 lit le cadre et
         * le decalage. */
        if (CLV_BAS(vk) || CLV_HAUT(vk) || CLV_CADRE_P(vk)
                || CLV_CADRE_S(vk)) {
            if (CLV_BAS(vk))  g_clv_dy += CLV_DY_PAS;
            if (CLV_HAUT(vk)) g_clv_dy -= CLV_DY_PAS;
            if (g_clv_dy >  CLV_DY_MAXI) g_clv_dy =  CLV_DY_MAXI;
            if (g_clv_dy < -CLV_DY_MAXI) g_clv_dy = -CLV_DY_MAXI;
            if (CLV_CADRE_S(vk)) g_clv_cadre++;
            if (CLV_CADRE_P(vk)) g_clv_cadre--;
            if (g_clv_cadre >= CLV_N_CADRES) g_clv_cadre = 0;
            if (g_clv_cadre < 0) g_clv_cadre = CLV_N_CADRES - 1;
            clv_refermer();
            g_clv_etat_vu = -1;
            clv_reglage_ranger();
            trace("NOM    essai : cadre %s (rang 0x%02X), y %+d -- range",
                  g_clv_cadres[g_clv_cadre].nom,
                  g_clv_cadres[g_clv_cadre].rang, (int)g_clv_dy);
            continue;
        }
        if (vk == VK_UP || vk == VK_DOWN || vk == VK_LEFT
                || vk == VK_RIGHT) {
            nom_bouger(vk == VK_UP ? -CLV_COL : vk == VK_DOWN ? CLV_COL
                       : vk == VK_LEFT ? -1 : 1);
            continue;
        }
        {
            int c = nom_car(vk);
            if (c && lg < NOM_MAXI) {
                g_nom[NOM_O_TAMPON + lg] = (unsigned char)c;
                lg++;
                bouge = 1;
            }
        }
    }
    /* LA MANETTE. Les codes du stub sont ceux du jeu : 2 a 5 les directions,
     * 7 valider, 8 annuler, 9 la croix. On ne retient que les FRONTS. */
    {
        unsigned m = lire_manette();
        unsigned neuf = m & ~g_nom_pad;
        g_nom_pad = m;
        if (neuf & (1u << 2)) nom_bouger(-CLV_COL);
        if (neuf & (1u << 3)) nom_bouger(CLV_COL);
        if (neuf & (1u << 4)) nom_bouger(-1);
        if (neuf & (1u << 5)) nom_bouger(1);
        if (neuf & (1u << 8)) {                      /* annuler : effacer */
            if (lg) { lg--; bouge = 1; }
        }
        if (neuf & ((1u << 7) | (1u << 9))) {        /* valider : la case */
            unsigned cur = nom_lire(NOM_O_CURSEUR);
            char ch = (cur < CLV_CASES) ? g_clv_grille[cur] : 0;
            if (ch == CLV_VALIDE) {
                if (!lg) {
                    nom_poser(NOM_O_ETAT, 3);
                    trace("NOM    champ vide : annule");
                    return;
                }
                g_nom[NOM_O_TAMPON + lg] = 0;
                nom_poser(NOM_O_LONG, lg);
                nom_poser(NOM_O_ETAT, 2);
                trace("NOM    valide : \"%s\" (%u caractere(s))",
                      (char *)(g_nom + NOM_O_TAMPON), lg);
                return;
            }
            if (ch == CLV_ANNULE) {
                nom_poser(NOM_O_ETAT, 3);
                trace("NOM    annule -- le nom n est pas touche");
                return;
            }
            if (ch == CLV_EFFACE) {
                if (lg) { lg--; bouge = 1; }
            } else if (ch && lg < NOM_MAXI) {
                g_nom[NOM_O_TAMPON + lg] = (ch == CLV_ESPACE) ? ' '
                                                              : (unsigned char)ch;
                lg++;
                bouge = 1;
            }
        }
    }
    if (bouge) {
        g_nom[NOM_O_TAMPON + lg] = 0;
        nom_poser(NOM_O_LONG, lg);
        trace("NOM    \"%s\"", (char *)(g_nom + NOM_O_TAMPON));
    }
}

#include "quest_runtime.c"

/* Le battement de la carte. C'est ici, et NULLE PART AILLEURS, que les entrees
 * sont echantillonnees -- comme dans la vraie apm.dll. */
/* LE PROFIL DU DEMARRAGE. `Core_execute` bat a chaque trame des le
 * demarrage du processus : son compte par seconde dit si le moteur TOURNE
 * (environ 60) ou s il CHARGE (zero, ou quelques unites). Trente secondes
 * suffisent, et le journal reste lisible.
 *
 * Pourquoi il le fallait : le journal horodate montrait douze secondes de
 * silence entre 2,4 et 14,4 -- mais la ligne de 14,4 etait un APPUI de
 * Frederic, pas un evenement du jeu. Un temps de reaction inconnu etait
 * dedans. Il faut une ligne que le MOTEUR produise. */
static void boot_profil(void)
{
    static unsigned prochaine = 1000, battements, precedent;
    unsigned ms;
    battements++;
    ms = trace_ms();
    if (ms < prochaine || prochaine > 30000) return;
    trace("BOOT   %2u s : %u battements (%u sur la seconde)",
          prochaine / 1000u, battements, battements - precedent);
    precedent = battements;
    while (prochaine <= ms) prochaine += 1000;
}

__declspec(dllexport) long long Core_execute(void)
{
    journal("Core_execute");
    boot_profil();
    if (g_cs_prete) {
        EnterCriticalSection(&g_cs);
        maj();
        LeaveCriticalSection(&g_cs);
    }
    /* le mode Quest, hors section critique : il appelle le moteur */
    quest_horloge(GetTickCount() - g_t0, g_quest_ms_declencheur);
    /* la sauvegarde du personnage, hors section critique elle aussi : elle ne
     * touche qu'a la memoire du moteur et a un fichier, jamais a nos etats */
    cust_tic();
    /* les reglages d OPTIONS, meme mecanique et memes gardes que la
     * personnalisation -- un fichier a part, ram\options.bin */
    opt_tic();
    /* la saisie du nom de donnees : elle ne fait rien tant que le moteur n a
     * pas pose l etat 1 dans la zone VF5NAME */
    nom_tic();
    /* la resolution choisie dans OPTIONS > Settings : si elle a change, on
     * ecrit le choix et on sort pour que le lanceur relance */
    res_tic();
    /* le mode de jeu (console / arcade), meme mecanique et memes raisons */
    mod_tic();
    /* le style des pastilles de boutons : la planche est RESIDENTE */
    btn_tic();
    return 0;
}

static char entree(const char *nom, int code, int front_seul)
{
    char r = 0;
    char msg[96];
    quest_tic_moteur();      /* le Quest, sur le fil DU MOTEUR */
    /* LA RESOLUTION BAT ICI AUSSI, et c est la lecon du Quest reprise telle
     * quelle : `Input_isOn` est le fil DU MOTEUR, celui qui tourne tant que le
     * jeu tourne, alors que `Core_execute` est le battement de LA CARTE. Si le
     * second s arrete une fois le moteur charge, la zone ne serait jamais
     * trouvee -- et c est precisement ce que le journal du 2026-10-07 laissait
     * ouvert. On appelle donc des deux cotes ; `res_tic` est idempotent (il
     * sort tout de suite des que `g_res_fini` est pose) et le compteur de
     * tours dira lequel a opere. HORS section critique, comme le Quest : il
     * fait des entrees-sorties et peut terminer le processus. */
    res_tic();
    mod_tic();
    btn_tic();
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
    /* Sur FICHIER on ne garde que les reponses positives DU FRONT.
     *
     * "r vrai" seul donnerait soixante lignes par seconde par code tenu, et un
     * journal de cent mille lignes ne se lit pas. Ce qu'on cherche a savoir,
     * c'est si le moteur a DEMANDE ce code et l'a OBTENU : une ligne par appui
     * suffit, et `g_montants` la donne exactement -- il ne porte un bit que
     * sur la trame ou le code vient d'etre presse. */
    /* UNE LIGNE PAR FOIS OU LE MOTEUR OBTIENT CE CODE, et une seule.
     *
     * LA PREMIERE VERSION NE MARCHAIT PAS, et c est mesure le 2026-10-11 :
     * elle exigeait `g_montants & (1 << code)`, c est-a-dire que l appel du
     * moteur tombe dans l intervalle entre le `maj()` qui a vu le front et le
     * suivant. Or `maj()` tourne AUSSI depuis `Core_execute`, soixante fois
     * par seconde et sur l AUTRE fil : il efface `g_montants` avant que le
     * moteur n ait demande. Resultat, un journal de 425 lignes avec **zero**
     * ligne LU -- alors que le jeu repondait au clavier. Un releve vide qui
     * passait pour une reponse, une fois de plus.
     *
     * On garde donc le front NOTRE : la derniere valeur rendue, par code.
     * Elle ne depend d aucun fil et d aucune horloge. */
    if (code >= 0 && code < MAX_CODE) {
        if (r && !g_dernier_lu[code])
            trace("LU     %s(%d) = OUI", nom, code);
        g_dernier_lu[code] = r;
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

/* `Input_isGamepadDetect` -- LE CRENEAU 45 DE LA TABLE, +0x168.
 *
 * Il etait genere a "rend 0", comme les quarante autres bouchons, et AUCUN
 * site du moteur ne l appelait (balayage des appels sur l objet 0x180C3B6F8 :
 * zero). C est normal -- une borne APM3 n a pas de manette. Mais la question
 * est exactement celle que le menu console doit poser pour savoir si OFFLINE
 * VERSUS est jouable, et l interface existait deja.
 *
 * CE QU IL REND, ET POURQUOI C EST BIEN "LE JOUEUR 2" :
 *   . la manette repond (XInputGetState(0) != 1167), ET
 *   . `manette_joueur` vaut 2, c est-a-dire qu elle tient le JOUEUR 2.
 * Avec `manette_joueur = 1`, la manette DOUBLE le joueur 1 : il n y a alors
 * aucun second peripherique, et OFFLINE VERSUS n est pas jouable non plus.
 * Les deux conditions disent donc la meme chose -- "un second joueur
 * peut-il entrer ?" -- et c est la seule question que ce creneau sert.
 *
 * LE BRANCHEMENT A CHAUD EST GRATUIT : `maj()` appelle `lire_manette()`
 * soixante fois par seconde depuis `Core_execute`, et c est elle qui pose
 * `g_pad_present`. Rien a surveiller, rien a relancer. */
__declspec(dllexport) char Input_isGamepadDetect(void)
{
    int r;
    if (!g_cs_prete) return 0;
    EnterCriticalSection(&g_cs);
    {
        DWORD now = GetTickCount();
        if (!g_vif_date || now - g_vif_date > 50) maj();
    }
    r = (g_pad_present && g_manette_joueur == 2) ? 1 : 0;
    if (r != g_pad_present_vu) {
        trace("PAD    %s", r ? "manette presente, joueur 2 jouable"
                             : "aucune manette sur le joueur 2");
        g_pad_present_vu = r;
    }
    LeaveCriticalSection(&g_cs);
    return (char)r;
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
        trace_ms();                 /* l horloge du journal part ICI */
        InitializeCriticalSection(&g_cs);
        g_cs_prete = 1;
        g_journal = 1;
        GetModuleFileNameA(h, g_chemin, MAX_PATH);
        s = strrchr(g_chemin, '\\');
        if (s) s[1] = 0; else g_chemin[0] = 0;
        memcpy(g_dossier, g_chemin, strlen(g_chemin) + 1);
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


def _refuser_non_ascii(texte):
    """Le `.c` s ecrit en ASCII pur, et un accent y fait echouer l ecriture.

    L erreur native est un `UnicodeEncodeError` qui ne donne qu un DECALAGE
    dans la source produite -- inutilisable pour retrouver la ligne du
    GENERATEUR. Trois fois le 2026-10-07 un guillemet francais depose dans un
    commentaire C a coute un aller-retour. Un piege ecrit ne protege de rien
    tant qu un outil ne le voit pas : celui-ci NOMME la ligne et le caractere.
    """
    mauvais = [(i, c) for i, c in enumerate(texte) if ord(c) > 127]
    if not mauvais:
        return
    lignes = texte.split('\n')
    print('REFUS : le source C doit etre en ASCII pur, %d caractere(s) '
          'fautif(s).' % len(mauvais))
    vues = set()
    for i, c in mauvais[:10]:
        no = texte.count('\n', 0, i)
        if no in vues:
            continue
        vues.add(no)
        print('  ligne %d du .c : %r dans %r'
              % (no + 1, c, lignes[no].strip()[:90]))
    raise SystemExit(2)


def main():
    os.makedirs(os.path.dirname(SRC) or '.', exist_ok=True)
    src = source()
    _refuser_non_ascii(src)
    with open(SRC, 'w', encoding='ascii') as fp:
        fp.write(src)
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
    # -Wall -Wextra depuis le 2026-09-29 : la compilation ne doit rien taire.
    # (Ils n'auraient PAS attrape la collision de noms du 27/09 -- deux
    #  'static int' de meme nom sont une definition provisoire, legale --
    #  mais tout le reste passe par la.)
    r = subprocess.run([GCC, '-shared', '-O2', '-s', '-Wall', '-Wextra',
                        '-o', out, SRC,
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
