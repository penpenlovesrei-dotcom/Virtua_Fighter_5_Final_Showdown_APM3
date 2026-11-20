/* Le mode QUEST dans FS : le pont entre apm.dll et le moteur.
 *
 * POURQUOI ICI. Le jeu charge deja apm.dll, et le moteur l'interroge a chaque
 * image (Input_isOn). Ecrire le Quest en C dans cette bibliotheque evite de
 * tasser des milliers d'octets d'assembleur dans la greffe : le moteur est
 * appele par pointeurs, resolus sur SA base (GetModuleHandleA), ce qui
 * survit au rebasage.
 *
 * CE QU'IL FAIT DEPUIS LE 2026-09-12 : le Quest est UN ETAT DU JEU, plus une
 * surimpression. Frederic : « cree un vrai ecran quest car tu es toujours en
 * surimpression », puis « non je veux un vrai ecran ». Le patcheur
 * (`patch_moteur.py --quest-ecran`) detourne l'entree SCOREBOARDS du menu vers
 * l'etat DATA_TEST / DATA_TEST_KOTSP_SS (mode 3, sous-etat 35), entierement
 * bouchonne dans FS, et y branche trois stubs de greffe. Ce module ne fait
 * donc plus RIEN tant que la machine a etats n'est pas sur cet etat -- pas
 * d'horloge, pas de declencheur : c'est le jeu qui commande.
 *
 * LA BOITE AUX LETTRES. La greffe porte un bloc « QUESTBOX » : deux octets y
 * sont partages entre le moteur et nous.
 *   +0x0C  actif   le moteur l'ecrit  (1 = la phase « boucle » tourne)
 *   +0x0D  sortie  NOUS l'ecrivons    (1 = je quitte ; l'etat se demonte et
 *                                      le moteur revient au MENU)
 * On la trouve en balayant la section `.greffe` du moteur : son adresse n'est
 * pas la meme d'un build a l'autre.
 *
 * Les adresses (RVA sur 0x180000000), lues les 2026-09-11 et 2026-09-12 :
 *   0x029C20  charger la planche AET d'identifiant <id>
 *   0x029D40  l'etat de la planche <id> ; 0 = prete
 *   0x171E90  creer un objet AET {contexte, rang, scene, calque, prio, flags}
 *   0x1721D0  LIBERER le rang <r> du contexte (detruit l'objet et vide la case)
 *   0x3FFBD0  le contexte AET des ecrans de menu
 *   0x187AB0  dimensionner le gestionnaire de sprites d'apres la base
 *   0x187C50  charger le jeu de sprites <id>   0x187CC0  son etat ; 0 = pret
 *   0x70C4F0  la tete courante (mode)          0x70C50C  le sous-etat courant
 */

/* La table {identifiant Xbox -> identifiant Final Showdown} des textes du
 * Quest, ecrite par `tools/textes_quest.py`. Vide tant qu'on n'a rien
 * ajoute. */
#include "quest_textes_map.h"

#define QUEST_RVA_TEXTE     0x1EFD10   /* resoudre un identifiant de texte */
#define QUEST_RVA_CHARGER   0x029C20
#define QUEST_RVA_ETAT      0x029D40
#define QUEST_RVA_CREER     0x171E90
#define QUEST_RVA_CREER2    0x171F40   /* la forme longue : avec les
                                        * deux noms de marqueurs */
#define QUEST_RVA_LIBERER   0x1721D0
/* LE DESCRIPTEUR DE CALQUE, ET SON ESPACE DE RESOLUTION (2026-10-20).
 *
 * `0x180171F40` construit un descripteur de 288 octets sur sa pile, le
 * remplit et le donne a `0x180029A90`. On refait la meme chose, pour
 * pouvoir ecrire UN champ de plus : l espace de resolution, en `+0x38`.
 *
 *     0x029000   construit le descripteur (il pose +0x38 = 9, EN DUR)
 *     0x029A90   cree l objet et rend son identifiant
 *     0x029140   detruit le descripteur
 *
 * Les champs, releves dans la decompilation de `0x180171F40` :
 *
 *     +0x00 u32  la scene                +0x34 u32  la priorite
 *     +0x08 ptr  le nom du calque        +0x38 u32  L ESPACE SOURCE
 *     +0x10 ptr  le marqueur de debut    +0x40 3xf  la position
 *     +0x18 ptr  le marqueur de fin      +0x28 u32  les drapeaux
 */
#define QUEST_RVA_DESC_INIT   0x029000
#define QUEST_RVA_DESC_CREER  0x029A90
#define QUEST_RVA_DESC_FIN    0x029140
#define QUEST_DESC_TAILLE     0x140      /* 288 suffisent ; on prend large */
#define QUEST_RVA_FINI      0x171070   /* le rang <r> est-il libre ou fini ? */
#define QUEST_RVA_CONTEXTE  0x3FFBD0
#define QUEST_RVA_DB        0x66B738   /* la base AET en memoire (vecteur) */
#define QUEST_RVA_MGR       0x66B750   /* le gestionnaire des planches */
#define QUEST_RVA_DB_SPR    0x719908   /* la base des sprites */
#define QUEST_RVA_MGR_SPR   0x719900   /* leur gestionnaire */
#define QUEST_RVA_MODE      0x70C4F0
#define QUEST_RVA_SOUSETAT  0x70C50C

#define QUEST_RVA_PREPARE_SPR 0x187AB0  /* dimensionne la table du
                                         * gestionnaire de sprites d'apres la
                                         * base. SANS lui, le chargeur ne
                                         * trouve pas de case et recoit un
                                         * POINTEUR NUL : le jeu meurt, meme
                                         * avec une planche d'origine. */
#define QUEST_RVA_CHARGER_SPR 0x187C50
#define QUEST_RVA_ETAT_SPR    0x187CC0

#define QUEST_AET_QUE       526      /* AET_N_QUE     (tools/bases_2d.py) */
#define QUEST_SPR_QUE       623      /* SPR_N_QUE */
#define QUEST_SCENE_MAIN    683      /* AET_N_QUE_MAIN */
/* LES FENETRES DU QUEST. Une seconde planche, `AET_N_QWIN`, porte les
 * quarante-huit fenetres : `home_menu_win` (la maison), `hall_menu_win` (une
 * salle), `status_win`, `player_list_win`, `embsel_win`, `rule_win`, les
 * ecrans de tournoi `tnt_*`, les fleches et les curseurs de boutons.
 * Identifiants lus dans `rom/2d/aet_db.bin` : planche 527, jeu de sprites
 * 624, scene 685. */
#define QUEST_AET_QWIN      527
#define QUEST_SPR_QWIN      624
#define QUEST_SCENE_QWIN    685
/* LES PICTOS DE GRADE, planche importee le 2026-09-30.
 *
 * Final Showdown a bien un jeu de sprites nomme `SPR_S_GAMDAN` (identifiant
 * 299) -- mais son contenu n'a RIEN a voir : ce sont les effets de l'ecran de
 * montee en grade (SPLASH, START_TXT, WAK_OP...). J'avais conclu trop vite que
 * « FS a la planche ».
 *
 * Les vrais pictos sont dans la planche de 2007, et ce ne sont pas des
 * sprites isoles : ce sont des COMPOSITIONS, une par rang --
 * `s_gamdan_kyu01` a `kyu09`, `s_gamdan_dan01` a `dan10`, et vingt-deux
 * titres `s_gamdan_shogo_*`. Quarante et un rangs : exactement l'etendue du
 * champ `npc_tbl + 0x7C` (42 valeurs, 0 a 41).
 *
 * On les monte donc comme tous nos autres calques, sans avoir a ecrire le
 * dessin d'un sprite. `tools/bases_2d.py --ajouter qdan` pose la planche ;
 * sa scene MAIN a recu l'identifiant 688. */
#define QUEST_AET_QDAN      530      /* AET_S_GAMDAN (les pictos de grade) */
#define QUEST_SPR_QDAN      627      /* SPR_S_GAMDAN, le notre */
#define QUEST_SCENE_QDAN    688
/* LE BADGE DE GRADE, ET IL EST DEJA DANS FINAL SHOWDOWN (2026-10-19, §29).
 *
 * Question de Frederic -- « pourquoi ne pas utiliser le grade de FS ? » --
 * apres deux essais rates sur `aet_s_gamdan` (qui est la planche de l ECRAN
 * DE PROMOTION, texte en 188x92). La mesure lui donne raison : le
 * `aet_c_cmn` de FS, extrait du `.par`, porte deja les calques nommes, aux
 * tailles EXACTES de ceux de 2007 :
 *
 *   c_cmn_dan_base1p.pic        102 x 30   la plaque rouge (2p = bleue)
 *   c_cmn_dan_kyu_10_e.pic       88 x 30   « 10th kyu »
 *   c_cmn_dan_kyu_1_e .. _9_e    74..78 x 28
 *   c_cmn_dan_dan_1_e .. _10_e   72..88 x 26
 *
 * (`_E` = la version anglaise ; FS porte les deux langues.) Chacun a UNE
 * source, donc la greffe sait les poser telle quelle -- pas besoin de
 * dessiner un sprite par identifiant.
 *
 * Rien a declarer, rien a importer, rien a charger en plus : la planche est
 * l identifiant 1, son jeu de sprites le 0, sa scene MAIN la 5, tout dans la
 * base d ORIGINE de Final Showdown.
 *
 * CE QUE FS N A PAS : les vingt-deux TITRES (grades 20 a 41). Ils n existent
 * que dans le media de 2007. Au-dela du grade 19, on reste donc en toutes
 * lettres, comme avant. */
/* LE BADGE EST SUSPENDU (2026-10-19). Six hypotheses, six echecs, et
 * beaucoup trop de temps pour un sprite. Ce qui est MESURE est garde au
 * §33 ; il suffit de remettre 1 ici pour reprendre, tout le reste est en
 * place. Le grade reste en toutes lettres, ce qui est lisible et juste. */
#define QUEST_BADGE         1

#define QUEST_AET_CCMN      1        /* AET_C_CMN, la planche commune de FS */
#define QUEST_SPR_CCMN      0        /* SPR_C_CMN */
#define QUEST_SCENE_CCMN    5        /* AET_C_CMN_MAIN */
/* LA PLANCHE COMMUNE DE 2007, posee le 2026-10-20 (`bases_2d.py --ajouter
 * qccmn`) : planche 533, scenes 693 a 697. Elle seule porte `gen_base`
 * AVEC son contenu -- la plaque `c_cmn_gen_pla.pic` (56 x 62, visible des
 * la trame 0) et les six billes qui s allument une a une. Celle de Final
 * Showdown declare la composition et la laisse VIDE.
 *
 * Elle declare 1280 x 768, comme la commune de FS : meme espace. */
#define QUEST_SCENE_QCCMN  695        /* AET_C_CMN_MAIN, media de 2007 */
#define QUEST_AET_QCCMN    533        /* AET_C_CMN, media de 2007  */
#define QUEST_SPR_QCCMN    630        /* SPR_C_CMN, le notre       */
#define QUEST_PRIO          0x40     /* au-dessus des calques de FS */

/* L'etat du jeu ou vit le Quest (voir patch_moteur.py, QUEST_MAGIE). */
#define QUEST_MODE          3        /* DATA_TEST */
#define QUEST_SOUS          35       /* DATA_TEST_KOTSP_SS */
#define QUEST_SALLE_DOME    7        /* EVENT SQUARE, les tournois */
#define QUEST_SALLE_MAISON  8

/* La boite aux lettres */
#define QUEST_BOITE_ACTIF   0x0C
#define QUEST_BOITE_SORTIE  0x0D
#define QUEST_BOITE_RAPPEL  0x18   /* NOTRE dessin, phase de rendu */

/* Nos rangs dans le contexte AET. Le tableau est indexe SANS borne par
 * 0x180171E90 : on reste dans ceux que FS emploie lui-meme. Balayage des
 * `mov edx, imm32` devant les 44 sites d'appel de creer/liberer/fini
 * (2026-09-12) : FS se sert de 1, 7, et 15 a 23. On prend 7 a 11.
 *   7 map_base   8 map_aero   9 tit   10 zoom_<salle>   11 ic_<salle> */
#define QUEST_RANG_BASE     7
#define QUEST_RANG_ZOOM     10
#define QUEST_RANG_ICONE    11
#define QUEST_RANG_HOME     12
#define QUEST_RANG_FENETRE  13
/* LES BATIMENTS DE LA CARTE, et le cadre de la fiche du joueur.
 *
 * Frederic, 2026-09-30 : « fais les images des arcades sur le cote gauche ».
 * Ce ne sont pas des images a fabriquer : ce sont NEUF calques de la
 * composition racine de `AET_N_QUE` que nous ne jouions pas --
 * `bg_01_<lieu>`, 300 images, marqueurs `sta_s`/`sta_e` seulement. `map_base`
 * n'est que l'ILE ; sans eux la carte est nue.
 *
 * Ils demandent dix rangs de plus. Le balayage du 2026-09-12 disait que FS se
 * sert de 1, 7 et 15 a 23 -- ces derniers sont ceux de SON MENU, qui est
 * demonte pendant que notre etat tient l'ecran. On les prend donc, et si
 * quelque chose clignote, c'est ici qu'il faut revenir. */
#define QUEST_RANG_BATIMENT 14           /* 14..22 : les neuf batiments */
#define QUEST_RANG_GRADE    23           /* le libelle de grade du joueur */
/* LA PLAQUE PREND LE RANG 1, PAS LE 24 (corrige le 2026-10-19).
 * `g_quest_pose[24]` et `g_quest_phase[24]` couvrent les indices 0 a 23 : le
 * rang 24 ecrivait HORS du tableau, et rien ne se dessinait. Le balayage du
 * 2026-09-12 dit que FS se sert des rangs 1, 7 et 15 a 23 ; le 1 est le seul
 * libre sous 23, et il appartient au menu de FS, qui est demonte pendant que
 * notre etat tient l ecran -- le meme raisonnement que pour 15 a 23. */
#define QUEST_RANG_PLAQUE   1            /* la plaque sous le libelle */
#define QUEST_RANG_FICHE    2            /* le cadre de la fiche du joueur */
#define QUEST_RANG_FACE     3            /* le portrait du joueur */
#define QUEST_RANG_PLAQUE2  6            /* la plaque `gen_base` */
#define QUEST_RANGS         7

/* Les codes de boutons du stub : 4 gauche, 5 droite, 8 ANNULER (le carre,
 * touche W ; c'est le code que les menus du moteur lisent pour reculer). */
#define QUEST_BTN_HAUT      2
#define QUEST_BTN_BAS       3
#define QUEST_BTN_GAUCHE    4
#define QUEST_BTN_DROITE    5
#define QUEST_BTN_VALIDER   7
#define QUEST_BTN_RETOUR    8
#define QUEST_BTN_VOIE      12      /* T : la voie du combat */

typedef void (*quest_f_charger)(unsigned int id);
typedef char (*quest_f_etat)(unsigned int id);
typedef void *(*quest_f_creer)(void *ctx, int rang, int scene,
                               const char *calque, int prio,
                               int drapeaux);
typedef void (*quest_f_creer2)(void *ctx, int rang, int scene,
                               const char *calque, void *position,
                               int prio, int drapeaux,
                               const char *m_debut,
                               const char *m_fin);
typedef void (*quest_f_liberer)(void *ctx, int rang);
typedef void *(*quest_f_desc_init)(void *d);
/* LA TAILLE PASSE EN ENTIER, DANS RDX (2026-10-20). Le desassemblage de
 * `0x180187B10` le montre : `vunpcklps xmm1, xmm1, xmm0` empaquette les deux
 * flottants, puis `vmovq rdx, xmm1` les met dans un registre ENTIER avant
 * le `call`. Un `double` partirait dans xmm1. Corrige -- mais cela n a PAS
 * suffi : voir §37.16. */
typedef void (*quest_f_cmd_taille)(void *d, unsigned long long taille);
typedef void (*quest_f_cmd_poser)(void *d);
typedef void *(*quest_f_spr_resoudre)(void *base, unsigned id);
typedef void (*quest_f_cmd_jeu)(float x0, float y0, float x1, float y1,
                                unsigned a5, unsigned a6,
                                unsigned a7, unsigned a8);
typedef unsigned (*quest_f_desc_creer)(void *d);
typedef void (*quest_f_desc_fin)(void *d);
typedef int (*quest_f_fini)(void *ctx, int rang);
typedef const char *(*quest_f_texte)(unsigned int id);

static void quest_dessiner(void *aetmgr);   /* le rappel de RENDU, plus bas */
static const char *quest_grade_texte(int g, char *out, size_t n);
static void quest_musique(int marche);      /* la BGM du Quest, plus bas */
static int quest_grade_joueur(void);        /* -1 = pas de carriere */
/* le code du personnage du joueur, ou NULL ; `out` recoit
 * « <code>_end ». Defini plus bas, avec le roster. */
static const char *quest_face_joueur(char *out, size_t n);
static void quest_tournoi_apres(int gagne); /* le tournoi, plus bas */
static void quest_profil_ecrire(void);      /* le profil, plus bas */
static void quest_profil_horloge(unsigned ms);


static unsigned char *g_quest_base;      /* base du moteur, ou NULL */
static unsigned char *g_quest_boite;     /* la boite QUESTBOX, ou NULL */
static int g_quest_cherche;              /* 1 = deja cherchee (trouvee ou non) */
static int g_quest_etape;    /* 0 dehors, 1 chargement, 2 attente, 3 vivant */
static unsigned g_quest_ms;
static int g_quest_salle;                /* la salle choisie, 0..8 */
static int g_quest_sortant;              /* 1 = sortie demandee, on attend que
                                          * la machine change vraiment d'etat
                                          * (sinon on rechargerait la planche
                                          * a la trame suivante) */
static int g_quest_zoom;                 /* 1 = la photo de la salle couvre
                                          * la carte (`zoom_<salle>` est une
                                          * composition PLEIN ECRAN : elle ne
                                          * se pose que sur validation) */
/* La fenetre montree quand un lieu est ouvert. Les noms viennent de la
 * composition racine de `AET_N_QWIN` ; ce sont ceux que la table des 59
 * fenetres de la version Xbox (0x82085700) designe. */
static int g_quest_fenetre;              /* 0 lieu, 1 joueurs, 2 statut */
static const char *g_quest_fenetres[3] = {
    0,                  /* 0 : hall_menu_win / home_menu_win, selon le lieu */
    "player_list_win",  /* 1 : LA LISTE DES JOUEURS */
    "status_win"        /* 2 : le statut */
};
static unsigned g_quest_trames;          /* trames depuis l ouverture d un lieu */
static unsigned g_quest_avant;           /* les boutons a l'image d'avant */

/* Le journal part a DEUX endroits : OutputDebugString (que la sonde lit) et
 * `quest_journal.txt`, a cote du jeu. Le fichier existe pour une raison
 * precise : Frederic tient la manette pendant les essais, la sonde ne tourne
 * pas, et il faut quand meme pouvoir MESURER ce que fait l'ecran. */
static void quest_dire(const char *quoi, long long valeur)
{
    char b[200];
    FILE *f;
    _snprintf(b, sizeof b, "[quest] %s %lld\n", quoi, valeur);
    OutputDebugStringA(b);
    f = fopen("quest_journal.txt", "a");
    if (f) { fputs(b, f); fclose(f); }
}

static int quest_moteur(void)
{
    HMODULE h;
    if (g_quest_base) return 1;
    h = GetModuleHandleA("vf5fs-pxd-w64-Retail_APM3.dll");
    if (!h) return 0;
    g_quest_base = (unsigned char *)h;
    quest_dire("moteur trouve, base", (long long)(size_t)g_quest_base);
    quest_dire("notre fil d execution", (long long)GetCurrentThreadId());
    return 1;
}

/* Le texte du Quest d'identifiant Xbox `x360`, resolu par le moteur de FS
 * (`0x1801EFD10`) sur le numero que `textes_quest.py` lui a donne. Rend NULL
 * tant que les chaines n'ont pas ete ajoutees. */
static const char *quest_texte(int x360)
{
    quest_f_texte texte;
    int i;
    if (!g_quest_base) return 0;
    texte = (quest_f_texte)(g_quest_base + QUEST_RVA_TEXTE);
    for (i = 0; i < QUEST_TEXTE_NOMBRE; i++)
        if (g_quest_textes[i].x360 == x360)
            return texte((unsigned int)g_quest_textes[i].fs);
    return 0;
}

/* Cherche « QUESTBOX » dans la section .greffe du moteur. On ne balaye pas
 * toute l'image : la greffe est nommee, et une section nommee se trouve dans
 * la table des sections. Rend NULL si le moteur n'est pas patche -- et alors
 * ce module reste inerte, ce qui est exactement ce qu'on veut. */
static unsigned char *quest_boite(void)
{
    unsigned char *b = g_quest_base;
    unsigned long e_lfanew;
    unsigned short n_sec, taille_opt;
    unsigned char *table;
    unsigned i;
    if (g_quest_boite || g_quest_cherche) return g_quest_boite;
    g_quest_cherche = 1;
    if (!b) return 0;
    e_lfanew = *(unsigned long *)(b + 0x3C);
    n_sec = *(unsigned short *)(b + e_lfanew + 6);
    taille_opt = *(unsigned short *)(b + e_lfanew + 20);
    table = b + e_lfanew + 24 + taille_opt;
    for (i = 0; i < n_sec; i++) {
        unsigned char *h = table + i * 40;
        unsigned long va, taille;
        unsigned char *p, *fin;
        if (memcmp(h, ".greffe", 8) != 0) continue;
        taille = *(unsigned long *)(h + 8);
        va = *(unsigned long *)(h + 12);
        for (p = b + va, fin = p + taille - 16; p < fin; p += 16) {
            if (memcmp(p, "QUESTBOX", 8) == 0) {
                g_quest_boite = p;
                /* on s'inscrit pour le RENDU : la greffe appelle ce pointeur
                 * depuis le creneau 4 d'AetMgr, apres l'original */
                *(void **)(p + QUEST_BOITE_RAPPEL) = (void *)quest_dessiner;
                quest_dire("boite QUESTBOX", (long long)(size_t)p);
                return p;
            }
        }
        break;
    }
    quest_dire("pas de boite QUESTBOX : moteur sans --quest-ecran", 0);
    return 0;
}

static int quest_dans_l_etat(void)
{
    return *(int *)(g_quest_base + QUEST_RVA_MODE) == QUEST_MODE
        && *(int *)(g_quest_base + QUEST_RVA_SOUSETAT) == QUEST_SOUS;
}

/* Le journal de la machine a etats : chaque changement, une ligne. C'est ce
 * qui permet a la sonde de dire OU en est le jeu sans clavier. */
static int g_quest_mode_vu = -1, g_quest_sous_vu = -1;

static void quest_machine(void)
{
    int mode = *(int *)(g_quest_base + QUEST_RVA_MODE);
    int sous = *(int *)(g_quest_base + QUEST_RVA_SOUSETAT);
    if (mode != g_quest_mode_vu || sous != g_quest_sous_vu) {
        char b[120];
        _snprintf(b, sizeof b, "[quest] machine : mode %d, sous-etat %d\n",
                  mode, sous);
        OutputDebugStringA(b);
        g_quest_mode_vu = mode;
        g_quest_sous_vu = sous;
    }
}

/* Les neuf salles, dans l'ordre ou VF5 les enumere (table 0x82309868 de la
 * version Xbox 360) ; le calque `zoom_<salle>` en est la photographie. */
/* CE QUE MONTRE UN LIEU QUAND ON LE VALIDE. Huit salles ont leur
 * photographie ; le neuvieme lieu est LA MAISON, qui n'en a pas (NULL) --
 * elle aura sa fenetre, dans `AET_N_QWIN`. Etabli a l'ecran le 2026-09-12 :
 * les neuf reperes `ic_*` tombent chacun sur un lieu different, et le
 * neuvieme est la maison bleue, celle que `map_home_txt` legende « HOME ».
 * `zoom_dom_02` reste inemployee : le dome porte DEUX tournois et un seul
 * repere -- c'est la progression du Quest qui choisira, pas la carte. */
static const char *g_quest_zooms[9] = {
    "zoom_swn", "zoom_sws", "zoom_swr", "zoom_csd", "zoom_csb",
    "zoom_sac", "zoom_sae", "zoom_dom_01", 0
};

/* LE CURSEUR. La composition racine de la scene MAIN porte neuf calques
 * `ic_<lieu>` (0-77 images) a cote des neuf `zoom_<salle>` : ce sont les
 * reperes poses sur la carte. Leurs noms, lus dans la planche :
 *   ic_csd ic_dom ic_hom ic_csb ic_sac ic_sae ic_swn ic_swr ic_sws
 * Il y a `ic_hom` (la maison) et UN SEUL `ic_dom` pour les deux domes : la
 * correspondance avec les neuf zooms n'est donc pas de un pour un. Ce
 * tableau est celui qu'on EPROUVE a l'ecran, une icone par appui. */
static const char *g_quest_icones[9] = {
    "ic_swn", "ic_sws", "ic_swr", "ic_csd", "ic_csb",
    "ic_sac", "ic_sae", "ic_dom", "ic_hom"
};

/* CHAQUE CALQUE, TENU INDIVIDUELLEMENT.
 *
 * Frederic, 2026-09-12 : « de mon cote je vois bien les fenetres s'afficher un
 * instant ». C'etait exact, et cela disait le defaut : une composition AET a
 * une DUREE (la carte 630 images, une fenetre 600, une icone 77) et s'eteint
 * au bout. Refaire TOUT le lot quand la carte finit ne pouvait pas tenir les
 * autres -- et rejouait l'animation d'entree de la carte a chaque mouvement.
 *
 * On dresse donc la liste de ce qui DOIT etre a l'ecran maintenant, et on
 * demande au moteur, rang par rang, si l'objet est fini (`0x180171070` rend 1
 * quand le rang est vide ou l'objet arrive au bout). On ne repose que
 * celui-la. `force` sert au changement d'etat : le calque a change de nom, il
 * faut le refaire meme s'il tourne encore. */
/* LES MARQUEURS : COMMENT LE QUEST JOUE SES CALQUES (lu dans le code Xbox 360,
 * 2026-09-12, apres que Frederic m'eut repris -- « tu supposes des choses et
 * tu ne t'appuies plus sur le code de la version xbox »).
 *
 * `FUN_822E4BF0` de la version 2007 est la methode « jouer » du porte-fenetre
 * du Quest. Elle dresse quatre paires de NOMS DE MARQUEURS avec leur drapeau,
 * et joue la phase demandee :
 *
 *     phase 0   "sta_s" -> "sta_e"   0x20000   l'ouverture, UNE FOIS
 *     phase 1   "neu_s" -> "neu_e"   0x10000   le repos, EN BOUCLE
 *     phase 2   "end_s" -> "end_e"   0x20000   la fermeture, une fois
 *     phase 3   "end_s" -> "end_e"   0x20000
 *
 * Les marqueurs sont DANS la planche, et se lisent (+0x20 nb, +0x24 table,
 * huit octets par marqueur : image en flottant, puis nom) :
 *
 *   hall_menu_win, home_menu_win, status_win, player_list_win, embsel_win
 *                       sta 0-27   neu 28-88   end 89-97
 *   ic_<lieu>           sta 0-16   neu 17-76
 *   map_base            sta_s 0    neu 30-629
 *   tit                 sta 0-20                 (rien d'autre)
 *   zoom_<salle>        sta 0-24                 (rien d'autre)
 *
 * CE QUE CELA EXPLIQUE, et que je n'aurais pas trouve en tatonnant :
 *   - « les fenetres s'ouvrent mais se referment au bout d'une seconde » :
 *     je jouais 0 a 600, donc je traversais `end` (89-97, soit 1,6 s) -- la
 *     fenetre jouait sa propre FERMETURE ;
 *   - « l'icone tourne en boucle mais avec les etapes du demarrage » :
 *     je bouclais 0-77 au lieu de boucler 17-76.
 *
 * Sur Final Showdown la forme longue du createur prend ces deux noms :
 *   0x180171F40(ctx, rang, scene, calque, position, prio, drapeau,
 *               marqueur_debut, marqueur_fin)
 * FS s'en sert lui-meme avec « cha_out_start »/« cha_out_end »,
 * « stg_in_start »/« stg_in_end », « loop_start »/« loop_end ».
 */
#define QUEST_TENIR    0x10000       /* en boucle */
#define QUEST_UNE_FOIS 0x20000       /* une fois, puis tient sa derniere image */

typedef struct {
    int rang, scene, prio;
    const char *nom;
    const char *sta_s, *sta_e;       /* l'ouverture, ou 0 : pas de marqueur */
    const char *neu_s, *neu_e;       /* le repos en boucle, ou 0 */
    float *position;                 /* ou 0 : le coin haut-gauche */
    /* L ESPACE DE RESOLUTION A DIRE AU MOTEUR, ou 0 pour le deduire de la
     * scene (`quest_espace`). On le force pour les pieces de la fiche qui
     * viennent d une planche en 768 mais doivent s aligner sur des ancres
     * relevees en 720 : en disant 13, la conversion 13 -> 9 fait le calcul,
     * ET le recadrage `y -= (768 - 720)` de `FUN_18016AF60` ne se declenche
     * pas, puisqu il exige une source de 9 ou 3. */
    int espace;
} quest_calque;

/* L ESPACE DE RESOLUTION D UNE SCENE -- LA CAUSE DU DECALAGE (2026-10-20).
 *
 * Frederic : « tous les elements de l ecran, dont la carte, sont trop haut,
 * on voit une bande en bas ». La chaine, lue dans le moteur :
 *
 *   1. `FUN_180029000`, qui construit le descripteur, pose son champ
 *      `+0x38` -- l espace SOURCE -- a **9**, EN DUR. Le mode 9 de la table
 *      `0x1803FEB20` est **1280 x 768** : l espace natif de l interface de
 *      Final Showdown.
 *   2. `FUN_180027900` balaie les dix-sept modes et compare la largeur et la
 *      hauteur de la SCENE (`scene + 0x14`, `scene + 0x18`) a chacun. Pour
 *      nos planches, 1280 x 720, il trouve le **mode 13**, qu il range dans
 *      l espace CIBLE de l objet (`objet + 0x8C`).
 *   3. `FUN_180023650`, avant de dessiner, convertit la position de la
 *      source vers la cible par `FUN_18016AF60`, qui est CENTREE :
 *
 *          y' = (y - h_source/2) * h_cible/h_source + h_cible/2
 *
 * Donc nos calques, dessines pour 720, sont pris pour du 768 et retrecis :
 * un y de 720 sort a (720-384) x 0,9375 + 360 = 675, soit 1012 pixels sur
 * 1080. Le bas de la carte est MESURE a 1014. C est la bande.
 *
 * LA CORRECTION tient en un champ : l espace source doit etre celui de la
 * planche d ou vient le calque. Source egale cible, la conversion devient
 * l identite, et 720 ressort a 720 -- plein ecran.
 *
 * ATTENTION, ET C EST LA SUBTILITE : la cible, elle, est DEDUITE de la
 * scene. Un calque de `aet_c_cmn` (1280 x 768) a pour cible 9, un calque de
 * `aet_n_qwin` (1280 x 720) a pour cible 13. Les deux cibles couvrent le
 * meme ecran. Deux calques qui doivent s aligner a l ecran ne portent donc
 * PAS la meme ordonnee : le badge de grade, qui vit en 768, doit viser
 * l ancre de la fiche convertie -- 448 x 768/720. */
#define QUEST_ESPACE_768   9        /* 1280 x 768, les planches de FS   */
#define QUEST_ESPACE_720  13        /* 1280 x 720, les planches du Quest */

static int quest_espace(int scene)
{
    /* Mesure du 2026-10-20 avec `tools/arbre_aet.py` : `aet_c_cmn` (la
     * planche commune de 2007, celle du badge) declare 1280 x 768 ; toutes
     * les autres planches que la greffe emploie -- `aet_n_que`,
     * `aet_n_qwin`, `aet_q_cmn`, `aet_q_cstm` -- declarent 1280 x 720. */
    /* 695 N EST PLUS DANS CETTE LISTE (2026-10-20). La planche importee de
     * 2007 est la NOTRE : on lui a declare 1280 x 720 (resolution_scene.py),
     * le moteur lui donne donc la cible 13 comme a toutes les autres, et ses
     * calques se disent avec les memes ancres, sans conversion ni cas
     * particulier. Il ne reste que la planche commune de FS, qu on ne peut
     * pas toucher sans deranger son interface. */
    return scene == QUEST_SCENE_CCMN ? QUEST_ESPACE_768 : QUEST_ESPACE_720;
}

/* `0x180171F40` refaite, avec l espace source en plus. Les offsets du
 * descripteur viennent de sa decompilation (voir QUEST_RVA_DESC_INIT). */
static void quest_creer_espace(void *ctx, quest_calque *c, int drapeau,
                               const char *m_debut, const char *m_fin)
{
    quest_f_desc_init init =
        (quest_f_desc_init)(g_quest_base + QUEST_RVA_DESC_INIT);
    quest_f_desc_creer creer =
        (quest_f_desc_creer)(g_quest_base + QUEST_RVA_DESC_CREER);
    quest_f_desc_fin fini =
        (quest_f_desc_fin)(g_quest_base + QUEST_RVA_DESC_FIN);
    quest_f_liberer liberer =
        (quest_f_liberer)(g_quest_base + QUEST_RVA_LIBERER);
    unsigned char d[QUEST_DESC_TAILLE];
    unsigned *rangee;
    /* la meme garde que `0x180171F40` : le contexte doit etre vivant */
    if (*((char *)ctx + 0x138)) return;
    init(d);
    *(unsigned *)(d + 0x00) = (unsigned)c->scene;
    *(const char **)(d + 0x08) = c->nom;
    *(const char **)(d + 0x10) = m_debut;
    *(const char **)(d + 0x18) = m_fin;
    *(unsigned *)(d + 0x28) = (unsigned)drapeau;
    *(unsigned *)(d + 0x34) = (unsigned)c->prio;
    *(unsigned *)(d + 0x38) = (unsigned)(c->espace ? c->espace
                                                   : quest_espace(c->scene));
    if (c->position) {
        *(float *)(d + 0x40) = c->position[0];
        *(float *)(d + 0x44) = c->position[1];
        *(float *)(d + 0x48) = c->position[2];
    }
    /* l ancien objet du rang, comme le fait `0x180171F40` avant de creer */
    rangee = (unsigned *)((char *)ctx + c->rang * 4 + 0x5C);
    if (*rangee) {
        liberer(ctx, c->rang);
        *rangee = 0;
    }
    *rangee = creer(d);
    fini(d);
}

static void quest_pose(quest_calque *c, const char *m_debut, const char *m_fin,
                       int drapeau)
{
    void *ctx = *(void **)(g_quest_base + QUEST_RVA_CONTEXTE);
    if (!ctx) return;
    if (!m_debut) {
        quest_f_creer creer = (quest_f_creer)(g_quest_base + QUEST_RVA_CREER);
        creer(ctx, c->rang, c->scene, c->nom, c->prio, drapeau);
        return;
    }
    {
        quest_creer_espace(ctx, c, drapeau, m_debut, m_fin);
        /* L INSTRUMENT QUI MANQUAIT (2026-10-19).
         *
         * `0x180171F40` range l identifiant de l objet cree dans
         * `ctx + rang * 4 + 0x5C` -- c est ce que sa decompilation montre :
         *
         *     param_1 = param_1 + (longlong)param_2 * 4;
         *     ...
         *     *(undefined4 *)(param_1 + 0x5c) = FUN_180029A90(descripteur);
         *
         * NUL veut donc dire que le calque n a PAS ete cree (nom introuvable
         * dans la composition racine de la scene) ; non nul, qu il existe et
         * que le probleme est ailleurs -- la position, la priorite, les
         * marqueurs. C est exactement la distinction qu on ne savait pas
         * faire, et qui a coute quatre allers-retours.
         *
         * On ne journalise que le rang du badge, et seulement quand la
         * valeur change : sans cela le journal grossirait de soixante
         * lignes par seconde. */
        if (c->rang == QUEST_RANG_GRADE || (c->rang >= 2 && c->rang <= 6)) {
            static unsigned dit[24];
            unsigned id = *(unsigned *)((char *)ctx + c->rang * 4 + 0x5C);
            if (id != dit[c->rang]) {
                dit[c->rang] = id;
                quest_dire("-- rang", c->rang);
                quest_dire("badge : identifiant de l objet cree", (long long)id);
                quest_dire("badge : position x", (long long)(c->position ? (int)c->position[0] : -1));
                quest_dire("badge : position y", (long long)(c->position ? (int)c->position[1] : -1));
                quest_dire(c->nom, c->scene);
                quest_dire(m_debut, c->prio);
            }
        }
    }
}

/* LA POSITION D'UN CALQUE, ET POURQUOI ELLE NE PEUT PAS RESTER NULLE.
 *
 * Mesure du 2026-09-30, dans `aet_n_que.bin` : la transformation de
 * `bg_01_dom_01` porte **origine (640, 360)** et **position (640, 360)** --
 * la composition est CENTREE sur l'ecran. Creee avec une position nulle, elle
 * se dessine decalee de -640, -360 : son contenu part dans le coin haut-
 * gauche, et c'est exactement le rectangle « SEGA ARENA EVENT SQUARE » que
 * Frederic a vu coince la-haut. Les neuf batiments sont dans ce cas.
 *
 * On leur passe donc leur position. `0x180171F40` prend un POINTEUR de
 * position en cinquieme argument -- trois flottants. */
static float g_quest_centre[3] = { 640.0f, 360.0f, 0.0f };

/* LA POSITION D UN CALQUE EMPRUNTE : LA REGLE, MESUREE A L ECRAN.
 *
 * Quatre calculs faux, puis un BALAYAGE : le meme calque pose cinq fois, a
 * cinq positions, chacun montrant un grade different pour se reconnaitre.
 * Un seul s est affiche, et il portait « 1st dan » -- le marqueur 10, celui
 * du rang 3, pose a (640, 384).
 *
 * LA REGLE EST DONC LA PLUS SIMPLE DES CINQ : `position` est le point ou va
 * le calque, EXPRIME DANS L ESPACE DE SA PROPRE SCENE. Aucune ancre n est a
 * retrancher, ni une ni deux. Verification sur l abscisse, qui ne depend pas
 * de l aspect : 640 / 1280 x 1920 = 960, et le badge etait a 960 pile.
 *
 * ET C EST DEJA RELATIF A LA RESOLUTION. Le moteur met a l echelle tout
 * seul : nos coordonnees vivent dans la scene, jamais en pixels d ecran.
 * La preuve tient dans ce fichier -- `QUEST_CARTE_X` vaut 96.0f et, sur une
 * capture 1080p, « NO-NAME » est a 145 px, soit 145 x 1280/1920 = 96,7.
 *
 * LE SEUL PIEGE EST QUE LES DEUX SCENES N ONT PAS LA MEME HAUTEUR :
 *
 *     AET_N_QUE_MAIN   (la carte)   1280 x 720
 *     AET_C_CMN_MAIN   (le badge)   1280 x 768
 *
 * L ancre visee, `p_dan_c`, est relevee a (588, 447) dans la planche de la
 * CARTE, donc en espace 720. Pour la dire au badge il faut la convertir :
 * la largeur est la meme, la hauteur se multiplie par 768/720.
 *
 * On l ecrit sous forme de calcul, et non du nombre tout cuit : si la
 * planche change un jour de resolution, la constante suit. */
#define QUEST_SCENE_QUE_H    720.0f        /* AET_N_QUE_MAIN  */
#define QUEST_SCENE_CCMN_H   768.0f        /* AET_C_CMN_MAIN  */
/* LES ANCRES DE LA FICHE, RELEVEES DANS LA PLANCHE (2026-10-20).
 *
 * Elles ne se cherchent pas a l ecran : `player_info_win_1p` EST une
 * composition, et elle porte ses propres reperes. `tools/arbre_aet.py`
 * les deplie, et `analysis/quest/ancres_qwin.txt` les listait deja.
 * Le suffixe du nom donne l alignement : _lt gauche-haut, _c centre.
 *
 *   p_ring_name_lt          (275, 435)   le nom
 *   p_player_info_01_lt     (322, 472)   W / L
 *   p_player_info_02_lt     (322, 502)   Win ratio
 *   p_dan_point_c           (600, 448)   le badge de grade, CENTRE
 *   p_gold_win_172x50_lt    (805, 489)   l argent
 *   p_chara_face_c          (727, 479)   le portrait, 104 x 106
 *   p_gen_plate_c           (288, 499)   la plaque, 56 x 62
 *
 * Le (588, 447) qui etait ecrit ici venait d un releve d avant la
 * correction d `ancres_que.py` (§19.0) ; la planche dit (600, 448). */
#define QUEST_ANCRE_DAN_X    600.0f        /* p_dan_point_c, espace carte */
#define QUEST_ANCRE_DAN_Y    448.0f
#define QUEST_ANCRE_NOM_X    275.0f        /* p_ring_name_lt        */
#define QUEST_ANCRE_NOM_Y    435.0f
#define QUEST_ANCRE_L1_X     322.0f        /* p_player_info_01_lt   */
#define QUEST_ANCRE_L1_Y     472.0f
#define QUEST_ANCRE_L2_X     322.0f        /* p_player_info_02_lt   */
#define QUEST_ANCRE_L2_Y     502.0f
#define QUEST_ANCRE_OR_X     805.0f        /* p_gold_win_172x50_lt  */
#define QUEST_ANCRE_OR_Y     489.0f
#define QUEST_ANCRE_FACE_X   727.0f        /* p_chara_face_c, CENTRE */
#define QUEST_ANCRE_FACE_Y   479.0f
#define QUEST_ANCRE_PLAQ_X   288.0f        /* p_gen_plate_c, CENTRE  */
#define QUEST_ANCRE_PLAQ_Y   499.0f
/* LE PAVE DU COSTUME ET LA BOITE DE L ARGENT (2026-10-20).
 *
 * La capture de 2007 que Frederic a fournie les montre a droite de la
 * fiche, et les deux occupent LA MEME COLONNE -- celle que l ancre
 * `p_gold_win_172x50_lt` annonce : x de 805 a 805+172 = 977.
 *
 * Mesures sur la capture, ramenees en 1280 x 720 :
 *
 *     pave costume      x 807,7..971,5   y 429,2..467,6
 *       bandeau titre                    y 429,2..445,1
 *       le type porte                    y 445,1..467,6
 *     cadre de l argent x 807,7..971,5   y 504,7..543,1
 *       le texte        x 883,2..960,0   y 513,3..529,9
 *
 * L ancre de l argent donne y 489..539 : le texte n est donc pas cale en
 * haut a gauche de sa boite, il est ALIGNE A DROITE, avec une marge d une
 * dizaine de pixels. C est pourquoi notre « 50000G » sortait a gauche.
 *
 * LE FOND DE CES DEUX BOITES N EST PAS PORTE : ce ne sont pas des calques
 * AET nommes. Le code de 2007 les confie a un objet d interface global,
 * `FUN_821DF868(drapeau)`, que le mode Quest se contente d allumer
 * (`FUN_823002D8`) -- un composant que Final Showdown n a pas. On ecrit
 * donc les textes a leur place, et le cadre reste a trouver (§37.9). */
#define QUEST_BOITE_X        805.0f       /* p_gold_win_172x50_lt   */
#define QUEST_BOITE_LARGE    172.0f
#define QUEST_BOITE_MARGE     10.0f
#define QUEST_COS_TITRE_Y    429.0f       /* « Main Costume »       */
#define QUEST_COS_TYPE_Y     446.0f       /* « Type A »             */
#define QUEST_OR_Y           505.0f       /* le texte de l argent   */

/* PAS DE CONVERSION DE HAUTEUR, ET C EST MESURE (2026-10-20).
 *
 * Le §34 convertissait l ancre de 720 vers les 768 de AET_C_CMN. La passe
 * du 2026-10-20 le refute : en calibrant la capture sur deux points connus
 * du cadre (le bandeau rouge a 418, le bas du bord a 546) on obtient
 * y_ecran = 1,4141 y - 36. Le badge pose a 477,9 (= 448 x 768/720) tombe
 * alors a 639,8 -- et il est MESURE a 641. Le moteur applique donc le MEME
 * facteur a toutes les scenes, quelle que soit la hauteur qu elles
 * declarent : il n y a rien a convertir.
 *
 * Le balayage du §34 ne pouvait pas trancher : ses cinq positions etaient
 * (0,0), (640,384), (1228,831), (1868,1215) et NULLE -- trente pixels
 * d ecart ne s y voient pas. */
/* L ANCRE TELLE QUE LA PLANCHE LA DONNE (2026-10-20).
 *
 * Elle etait convertie en 768, parce que le badge vient d une planche qui
 * declare 768. La mesure a montre qu il restait alors 16 pixels trop haut,
 * quand le nom -- lui en espace 13 -- tombait exactement sur son ancre.
 *
 * C est le recadrage de `FUN_18016AF60` : il s applique des que la SOURCE
 * vaut 9 ou 3. On dit donc au badge qu il est en 13 (champ `espace`) : la
 * conversion 13 -> 9 fait seule le changement d echelle, et le recadrage ne
 * se declenche plus. L ancre se dit alors telle quelle. */
static float g_quest_badge[3] = {
    QUEST_ANCRE_DAN_X,
    QUEST_ANCRE_DAN_Y,
    0.0f
};

/* BALAYAGE (2026-10-19) : on cesse de CALCULER la position, on la MESURE.
 *
 * Quatre calculs, quatre echecs, et l objet est pourtant cree a chaque fois
 * (identifiant 20). On pose donc le MEME calque CINQ fois, a cinq rangs et
 * cinq positions, et c est l ecran qui dira laquelle est la bonne :
 *
 *   rang 2  (0, 0)           la position nulle
 *   rang 3  (640, 384)       sa propre position dans la planche
 *   rang 4  (1228, 831)      ancre + une ancre retranchee
 *   rang 5  (1868, 1215)     ancre + deux ancres retranchees
 *   rang 6  NUL              aucun pointeur de position
 *
 * Les rangs 2 a 6 ne sont pas employes par Final Showdown -- le balayage du
 * 2026-09-12 dit qu il se sert de 1, 7, et 15 a 23 -- et ils tiennent dans
 * `g_quest_pose[24]`.
 *
 * A RETIRER des que la regle est connue. */
#define QUEST_BALAYAGE 0
/* 1 = pose deux `trophy_icon` a y=100 et y=600, pour mesurer la loi
 * scene -> ecran. A remettre a 0 ensuite. */
#define QUEST_TEMOINS 0
/* 1 = un quad rouge dessine par la fonction du jeu, a la place du pave */
#define QUEST_TEMOIN_QUAD 0

/* LAQUELLE DES DEUX VARIANTES DU CADRE DE LA FICHE (2026-10-20).
 *
 * Le 2026-10-19 les deux ont ete posees EN MEME TEMPS et le cadre est
 * apparu, mais le jeu a ete tue avant les captures : on ne sait pas
 * laquelle comptait. Le journal dit que les DEUX calques existent
 * (identifiants 20/25 et 21/26) -- l instrument du rang ne tranche donc
 * pas, seul l ecran le fera, une variante a la fois.
 *
 *   2 -> le rang 2 seul : position NULLE, priorite +6 (comme la fenetre
 *        `home_menu_win`, qui elle s affiche)
 *   3 -> le rang 3 seul : position explicite (640, 360), priorite +7
 *   0 -> les deux, comme le 2026-10-19
 *
 * A RETIRER des que la variante est connue, avec le rang devenu inutile. */
#define QUEST_FICHE_VARIANTE 2
static float g_quest_bal0[3] = {    0.0f,    0.0f, 0.0f };
static float g_quest_bal1[3] = {  640.0f,  384.0f, 0.0f };
static float g_quest_bal2[3] = { 1228.0f,  831.0f, 0.0f };
static float g_quest_bal3[3] = { 1868.0f, 1215.0f, 0.0f };

/* LE PICTO DE CHAQUE GRADE.
 *
 * Le grade 0 est le 10e kyu, le plus bas, et la planche n'a pas de picto pour
 * lui : elle commence au 9e (`kyu09`) et monte jusqu'au 1er (`kyu01`), puis
 * les dix dan. Au-dela du grade 19 viennent les vingt-deux titres, dont
 * l'ordre n'est PAS etabli -- ils restent en toutes lettres. */
static const char *quest_grade_calque(int g)
{
    /* LE BADGE DE GRADE EST UNE COMPOSITION A MARQUEURS (mesure le 2026-10-19).
     *
     * Trois essais rates ont fini par donner la regle. Ce qui marchait
     * jusqu ici -- `map_base`, `map_aero`, `tit`, `p_dan_c` -- est TOUJOURS
     * dans la composition RACINE de sa scene. Les calques
     * `c_cmn_dan_kyu_10_e.pic` et `c_cmn_dan_base1p.pic`, eux, vivent dans
     * des SOUS-COMPOSITIONS (77, 79, 80 sur 103) : `0x180171E90` ne les
     * trouve pas, et rien ne se dessine -- sans une erreur.
     *
     * A LA RACINE, le badge entier porte un seul nom : `dan_icon1p_e`
     * (`2p_e` pour le joueur 2, `icongray` pour la version grise). C est une
     * composition de 2820 trames avec QUARANTE-SEPT marqueurs :
     *
     *     trame    0  « 0 »      trame  600  « 10 »
     *     trame   60  « 1 »      ...
     *     trame  120  « 2 »      trame 2700  « 45 »
     *     ...                    trame 2760  « end »
     *
     * UN MARQUEUR TOUS LES SOIXANTE TRAMES, ET SON NOM EST LE GRADE. On
     * pose donc la composition et on la joue de `<grade>` a `<grade+1>`,
     * exactement comme les photos de lieu vont de `sta_s` a `sta_e` : elle
     * s arrete alors sur la bonne image et la tient.
     *
     * Quarante-six grades (0 a 45) la ou le Quest de 2007 en compte
     * quarante-deux : l echelle de Final Showdown est plus longue. La
     * correspondance au-dela du grade 41 n est PAS mesuree. */
    static const char *const marque[47] = {
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
        "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
        "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
        "40", "41", "42", "43", "44", "45", "end"
    };
    if (g < 0 || g > 45) return 0;
    return marque[g];
}



/* LA PHOTO DE CHAQUE LIEU, dans l ordre de nos neuf reperes. La maison n en
 * a pas -- la planche n a pas de `bg_01_hom`. */
static const char *const g_quest_photos[9] = {
    "bg_01_swn", "bg_01_sws", "bg_01_swr", "bg_01_csd", "bg_01_csb",
    "bg_01_sac", "bg_01_sae", "bg_01_dom_01", 0
};

/* LA TAILLE DE LA LISTE DE CALQUES.
 *
 * Elle valait 24 EN DUR a deux endroits -- la declaration `quest_calque
 * t[24]` et la boucle de remise a zero ci-dessous -- et le badge de grade,
 * qui ajoute UN calque (la plaque sous le libelle), pouvait la faire
 * deborder : `t[]` vit sur la PILE de `quest_calques()`, et rien ne
 * verifiait `n`. On la nomme, on l elargit, et `quest_liste` refuse
 * bruyamment plutot que d ecrire a cote. */
#define QUEST_CALQUES 32

static int quest_liste(quest_calque *t)
{
    int n = 0;
    for (n = 0; n < QUEST_CALQUES; n++) {
        t[n].position = 0;
        t[n].espace = 0;
    }
    n = 0;
    t[n].rang = QUEST_RANG_BASE + 0; t[n].scene = QUEST_SCENE_MAIN;
    t[n].nom = "map_base";     t[n].prio = QUEST_PRIO + 0;
    /* la carte n'a pas de `sta_e` : son ouverture va de `sta_s` a `neu_s`,
     * puis le survol aerien tourne de `neu_s` a `neu_e` */
    t[n].sta_s = "sta_s"; t[n].sta_e = "neu_s";
    t[n].neu_s = "neu_s"; t[n].neu_e = "neu_e"; n++;
    t[n].rang = QUEST_RANG_BASE + 1; t[n].scene = QUEST_SCENE_MAIN;
    t[n].nom = "map_aero";     t[n].prio = QUEST_PRIO + 1;
    t[n].sta_s = 0; t[n].sta_e = 0; t[n].neu_s = 0; t[n].neu_e = 0; n++;
    /* `map_home_txt` est la LEGENDE « HOME » sous la maison, pas un ecran :
     * elle appartient a la carte, en permanence (vu a l'ecran le 2026-09-12,
     * ou je l'avais d'abord prise pour la page de la maison). */
    t[n].rang = QUEST_RANG_HOME;     t[n].scene = QUEST_SCENE_MAIN;
    t[n].nom = "map_home_txt"; t[n].prio = QUEST_PRIO + 2;
    t[n].sta_s = 0; t[n].sta_e = 0; t[n].neu_s = 0; t[n].neu_e = 0; n++;
    t[n].rang = QUEST_RANG_BASE + 2; t[n].scene = QUEST_SCENE_MAIN;
    t[n].nom = "tit";          t[n].prio = QUEST_PRIO + 4;
    /* LE TITRE EST UNE ANIMATION D ENTREE (2026-10-20).
     * Frederic : le titre Quest n est pas a sa place. La planche le dit :
     * son cadre, n_que_tit_waku.pic, a une position ANIMEE, sept cles de
     * -30 a 50. Pose sans marqueur, le calque tenait la premiere trame --
     * et -30 est AU-DESSUS de l ecran. Ses deux marqueurs sont sta_s
     * (trame 0) et sta_e (trame 20) : on le joue, et il tient sa derniere
     * image, exactement comme la photo du lieu. */
    t[n].sta_s = "sta_s"; t[n].sta_e = "sta_e";
    t[n].neu_s = 0; t[n].neu_e = 0; n++;
    if (!g_quest_zoom) {
        /* LA PHOTO DU LIEU SOUS LE CURSEUR, en partie, a gauche de l ecran.
         * C est ce que Frederic decrit, et c est `bg_01_<lieu>` : une photo
         * de 300 images, origine et position (640, 360). Mon erreur du
         * 2026-09-30 a ete de poser les NEUF d un coup -- trois se
         * chevauchaient dans les coins. Il n y en a qu UNE a l ecran, celle
         * du lieu choisi, et elle change avec le curseur comme l icone.
         * La maison n en a pas. */
        if (g_quest_photos[g_quest_salle]) {
            t[n].rang = QUEST_RANG_BATIMENT; t[n].scene = QUEST_SCENE_MAIN;
            t[n].nom = g_quest_photos[g_quest_salle];
            /* SOUS LA CARTE. La photo se voyait par-dessus la mer, aux bords
             * de l ecran : elle etait au-DESSUS de `map_base`. En 2007 son
             * descripteur porte une priorite de 2 quand nos calques de carte
             * sont bien plus hauts -- elle passe donc derriere tout. */
            t[n].prio = QUEST_PRIO - 1;
            /* COMME 2007, ET C EST MESURE. `FUN_82309590(questaet, lieu)`
             * monte UNE photo a la fois, l ancienne liberee d abord, avec
             * les marqueurs `sta_s` -> `sta_e` et le drapeau 0x20000 : une
             * fois, puis elle tient sa derniere image. PAS de phase neutre.
             * Son tableau est indexe a partir de 1 ; l indice 0 est NUL --
             * la maison n a pas de photo, et c est le jeu qui le dit. Le
             * dome en a deux, `dom_01` et `dom_02`, la seconde quand un
             * tournoi court (`FUN_823163A0(0xE)`). */
            t[n].sta_s = "sta_s"; t[n].sta_e = "sta_e";
            t[n].neu_s = 0; t[n].neu_e = 0;
            t[n].position = g_quest_centre; n++;
        }
        /* LE CADRE DE LA FICHE DU JOUEUR (2026-10-19).
         *
         * Constat de Frederic : « la fiche n est pas vraiment visible (aucun
         * cadre ni fond) ». Sur la capture du jeu de 2007 elle a un bandeau
         * rouge et un fond sombre.
         *
         * Trouve avec la recette du §34 : `player_info_win_1p` est une
         * composition RACINE de `aet_n_qwin` -- la planche que la greffe
         * charge deja (527, scene 685) -- de position (640, 360) et origine
         * (640, 360), dans la MEME scene 1280x720 que la carte. On lui passe
         * donc sa propre position, sans conversion.
         *
         * Le dossier notait le 2026-09-30 que `waku_1p` n etait pas le
         * cadre mais une jauge : c etait vrai, et le vrai cadre portait un
         * autre nom. */
        {
            /* DEUX VARIANTES A LA FOIS, puisque la boucle automatique rend
             * un essai gratuit. La fenetre qui MARCHE (`home_menu_win`) est
             * posee SANS position -- donc NULL, et `0x180171F40` ne copie
             * rien : le calque garde celle de la planche -- et en priorite
             * `QUEST_PRIO + 6`. La mienne avait une position explicite et la
             * priorite +2. On essaie les deux differences separement.
             *
             *   rang 2 : comme la fenetre qui marche -- position NULLE,
             *            priorite +6
             *   rang 3 : position explicite (640, 360), priorite +7
             *
             * Celle qui s affiche dira laquelle des deux variables comptait. */
#if QUEST_FICHE_VARIANTE != 3
            t[n].rang = QUEST_RANG_FICHE; t[n].scene = QUEST_SCENE_QWIN;
            t[n].nom = "player_info_win_1p"; t[n].prio = QUEST_PRIO + 6;
            t[n].sta_s = "sta_s"; t[n].sta_e = "sta_e";
            t[n].neu_s = "neu_s"; t[n].neu_e = "neu_e";
            t[n].position = 0; n++;
#endif

#if QUEST_FICHE_VARIANTE != 2
            {
                static float pos[3] = { 640.0f, 360.0f, 0.0f };
                t[n].rang = 3; t[n].scene = QUEST_SCENE_QWIN;
                t[n].nom = "player_info_win_1p"; t[n].prio = QUEST_PRIO + 7;
                t[n].sta_s = "sta_s"; t[n].sta_e = "sta_e";
                t[n].neu_s = "neu_s"; t[n].neu_e = "neu_e";
                t[n].position = pos; n++;
            }
#endif
        }
        /* DEUX TEMOINS, POUR MESURER LA LOI SCENE -> ECRAN (2026-10-20).
         *
         * Frederic : « tous les elements de l ecran, dont la carte, sont
         * trop haut, on voit une bande en bas ». Deux points du cadre,
         * distants de 128 unites, ne suffisent pas a extrapoler : on pose
         * donc le MEME calque a deux hauteurs tres ecartees, dans la scene
         * du Quest, et l ecart mesure donne la pente et l ordonnee.
         *
         * `trophy_icon` est une composition RACINE de `aet_n_qwin`, de 40 x
         * 40, d origine (20, 20) -- donc centree sur sa position.
         *
         * A RETIRER des que la loi est connue. */
#if QUEST_TEMOINS
        {
            static float haut[3] = { 640.0f, 100.0f, 0.0f };
            static float bas[3]  = { 640.0f, 600.0f, 0.0f };
            t[n].rang = 4; t[n].scene = QUEST_SCENE_QWIN;
            t[n].nom = "trophy_icon"; t[n].prio = QUEST_PRIO + 9;
            t[n].sta_s = 0; t[n].sta_e = 0;
            t[n].neu_s = 0; t[n].neu_e = 0;
            t[n].position = haut; n++;
            t[n].rang = 5; t[n].scene = QUEST_SCENE_QWIN;
            t[n].nom = "trophy_icon"; t[n].prio = QUEST_PRIO + 9;
            t[n].sta_s = 0; t[n].sta_e = 0;
            t[n].neu_s = 0; t[n].neu_e = 0;
            t[n].position = bas; n++;
        }
#endif
        /* LA PLAQUE DE LA FICHE : `gen_base`, l objet gris et rond.
         *
         * Frederic la signale comme manquante le 2026-10-20, et le code de
         * 2007 la nomme : `FUN_8230AC50` pose TROIS objets sur la fiche --
         * `chara_face`, `gen_base` et `dan_icon1p`. `FUN_82309C38` montre
         * que `gen_base` a SEPT variantes, choisies par un compte de bits
         * (les huit bits de `profil + 0x130` de 2007, plafonne a 6).
         *
         * CE QUE CE COMPTE REPRESENTE N EST PAS ETABLI : l offset 0x130 de
         * 2007 ne correspond a rien de connu dans notre profil. On pose donc
         * la variante **0**, celle d un dossier neuf, plutot que d en
         * inventer une.
         *
         * Elle vit dans `aet_c_cmn`, qui declare 1280 x 768 : son ordonnee
         * se convertit, comme celle du badge. Son ancre `p_gen_plate_c` est
         * CENTREE (56 x 62). */
        {
            static float pos[3] = {
                QUEST_ANCRE_PLAQ_X, QUEST_ANCRE_PLAQ_Y, 0.0f
            };
            t[n].rang = QUEST_RANG_PLAQUE2; t[n].scene = QUEST_SCENE_QCCMN;
            t[n].nom = "gen_base"; t[n].prio = QUEST_PRIO + 8;

            t[n].sta_s = "0"; t[n].sta_e = "0";
            t[n].neu_s = 0; t[n].neu_e = 0;
            t[n].position = pos; n++;
        }
        /* LE PORTRAIT, a `p_chara_face_c` (727, 479). Au-dessus du cadre,
         * comme le badge : le panneau de la fiche est semi-transparent et
         * tout ce qui passe dessous ressort delave. */
        {
            static char fin[16];
            static float pos[3] = { QUEST_ANCRE_FACE_X,
                                    QUEST_ANCRE_FACE_Y, 0.0f };
            const char *code = quest_face_joueur(fin, sizeof fin);
            if (code) {
                t[n].rang = QUEST_RANG_FACE; t[n].scene = QUEST_SCENE_QWIN;
                t[n].nom = "chara_face_player"; t[n].prio = QUEST_PRIO + 7;
                t[n].sta_s = code; t[n].sta_e = fin;
                t[n].neu_s = 0; t[n].neu_e = 0;
                t[n].position = pos; n++;
            }
        }
        /* LE BADGE DE GRADE, sur la fiche du joueur : DEUX calques.
         *
         * La plaque `c_cmn_dan_base1p.pic` (102 x 30, rouge) dessous, le
         * libelle (74..88 x 26..30) dessus -- c est ainsi que 2007 le
         * compose, et les deux viennent de la planche COMMUNE de Final
         * Showdown (scene 5), qui les porte deja. */
        if (QUEST_BADGE) {
            int g = quest_grade_joueur();
            const char *gr = quest_grade_calque(g);
            static const char *dit;
            if (gr != dit) {
                dit = gr;
                quest_dire(gr ? gr : "(pas de marqueur de grade)", g);
            }
            if (gr) {
#if QUEST_BALAYAGE
                {
                    static float *const pos[5] = {
                        g_quest_bal0, g_quest_bal1, g_quest_bal2,
                        g_quest_bal3, 0
                    };
                    /* CHAQUE RANG MONTRE UN GRADE DIFFERENT : le TEXTE du
                     * badge visible dira lequel des cinq est a l ecran.
                     *   rang 2 (0,0)           -> « 10th kyu »
                     *   rang 3 (640,384)       -> « 1st dan »
                     *   rang 4 (1228,831)      -> « 10th dan »
                     *   rang 5 (1868,1215)     -> « 5th kyu »
                     *   rang 6 position NULLE  -> « 6th dan » */
                    static const char *const mq[5] = {
                        "0", "10", "19", "5", "15"
                    };
                    int b;
                    for (b = 0; b < 5; b++) {
                        t[n].rang = 2 + b; t[n].scene = QUEST_SCENE_CCMN;
                        t[n].nom = "dan_icon1p_e";
                        t[n].prio = QUEST_PRIO + 5;
                        t[n].sta_s = mq[b]; t[n].sta_e = mq[b];
                        t[n].neu_s = 0; t[n].neu_e = 0;
                        t[n].position = pos[b]; n++;
                    }
                }
#endif
#if !QUEST_BALAYAGE
                /* LE BADGE PASSE SUR NOTRE PLANCHE (2026-10-20).
                 * C etait le dernier objet a vivre dans une scene de 768,
                 * donc le dernier a avoir une CIBLE a lui (9) et une loi de
                 * projection differente de tout le reste -- d ou vingt
                 * pixels d ecart impossibles a rattraper proprement.
                 * `aet_qc_cmn`, la planche de 2007 que nous avons
                 * importee, porte le meme badge sous son nom d origine
                 * `dan_icon1p`
                 * (memes tailles d image : 88 x 30 pour le 10e kyu), et
                 * nous lui avons declare 1280 x 720. Cible 13 comme les
                 * autres, ancre dite telle quelle. */
                t[n].rang = QUEST_RANG_GRADE; t[n].scene = QUEST_SCENE_QCCMN;
                /* AU-DESSUS DU CADRE, et c est mesure (2026-10-20).
                 * Frederic : « le grade est derriere, on ne le voit pas ».
                 * A +5 le badge passait sous le panneau semi-transparent de
                 * player_info_win_1p (+6) : il restait visible mais delave.
                 * Plus grand = plus devant -- la photo du lieu, a
                 * QUEST_PRIO - 1, passe bien derriere tout. */
                t[n].nom = "dan_icon1p"; t[n].prio = QUEST_PRIO + 8;
                /* LE MEME MARQUEUR DES DEUX COTES, ET C EST MESURE.
                 * Dans la composition, chaque grade occupe UN creneau de
                 * soixante trames : `dan_10_kyu` va de 0 a 60, `dan_09_kyu`
                 * de 60 a 120, `dan_01_dan` de 600 a 660. Un calque vit sur
                 * [debut, fin[ : jouer de « 0 » a « 1 » et tenir la DERNIERE
                 * image s arrete sur la trame 60, ou `dan_10_kyu` vient de
                 * finir et ou `dan_09_kyu` commence -- rien de lisible.
                 * On demande donc le meme marqueur au debut et a la fin :
                 * la composition tient la trame d ouverture du creneau, et
                 * c est la que le badge du grade est dessine. */
                t[n].sta_s = gr; t[n].sta_e = gr;
                t[n].neu_s = 0; t[n].neu_e = 0;
                t[n].position = g_quest_badge; n++;
#endif
            }
        }
        t[n].rang = QUEST_RANG_ICONE; t[n].scene = QUEST_SCENE_MAIN;
        t[n].nom = g_quest_icones[g_quest_salle];
        t[n].prio = QUEST_PRIO + 3;
        t[n].sta_s = "sta_s"; t[n].sta_e = "sta_e";
        t[n].neu_s = "neu_s"; t[n].neu_e = "neu_e"; n++;
        return n;
    }
    /* MESURE du 2026-09-12, a l'ecran : `zoom_<salle>` n'est pas une vignette,
     * c'est la photographie de la salle EN PLEIN ECRAN. Posee d'office, elle
     * masquait toute la carte. Elle n'apparait donc qu'a la validation -- et
     * la maison n'en a pas. */
    if (g_quest_zooms[g_quest_salle]) {
        t[n].rang = QUEST_RANG_ZOOM;  t[n].scene = QUEST_SCENE_MAIN;
        t[n].nom = g_quest_zooms[g_quest_salle];
        t[n].prio = QUEST_PRIO + 5;
        t[n].sta_s = 0; t[n].sta_e = 0; t[n].neu_s = 0; t[n].neu_e = 0; n++;
    }
    /* la fenetre par-dessus : `hall_menu_win` dans une salle,
     * `home_menu_win` a la maison. Elle vient de l'AUTRE planche. */
    t[n].rang = QUEST_RANG_FENETRE;   t[n].scene = QUEST_SCENE_QWIN;
    t[n].nom = g_quest_fenetres[g_quest_fenetre];
    /* TROIS MENUS DIFFERENTS, et c'est la lecture du 2026-09-27 qui l'a
     * montre (`analysis/quest_regles.md`) : je posais le meme partout.
     *   une salle d'arcade -> `store_menu_win` : TROIS BORNES et leurs
     *                         occupants, plus Tournament et Customize.
     *                         C'est la qu'on se bat.
     *   le dome (salle 7)  -> `hall_menu_win` : les trois entrees de tournoi
     *   la maison (8)      -> `home_menu_win` : ses six lignes */
    if (!t[n].nom)
        t[n].nom = !g_quest_zooms[g_quest_salle] ? "home_menu_win"
                 : (g_quest_salle == QUEST_SALLE_DOME) ? "hall_menu_win"
                 : "store_menu_win";
    t[n].prio = QUEST_PRIO + 6;
    t[n].sta_s = "sta_s"; t[n].sta_e = "sta_e";
    t[n].neu_s = "neu_s"; t[n].neu_e = "neu_e"; n++;
    if (n > QUEST_CALQUES) {
        static int dit_trop;
        if (!dit_trop) { dit_trop = 1; quest_dire("DEBORDEMENT de la liste de calques", n); }
        n = QUEST_CALQUES;
    }
    return n;
}

static void quest_rendre(int rang)
{
    quest_f_liberer liberer =
        (quest_f_liberer)(g_quest_base + QUEST_RVA_LIBERER);
    void *ctx = *(void **)(g_quest_base + QUEST_RVA_CONTEXTE);
    if (ctx) liberer(ctx, rang);
}

/* CE QUI EST POSE, RANG PAR RANG, ET DANS QUELLE PHASE.
 *
 * On garde pour chaque rang le NOM du calque et la phase ou il en est :
 *   0  rien
 *   1  `sta` joue (une fois)
 *   2  `neu` tourne (en boucle) -- ou l'ouverture tient sa derniere image,
 *      pour un calque sans marqueur `neu`
 *
 * C'est la mecanique de `FUN_822E4BF0` de la version Xbox 360, transcrite.
 * Le passage de 1 a 2 se fait quand le moteur dit l'objet fini
 * (`0x180171070` rend 1). Un rang dont le nom n'a pas change n'est jamais
 * repose : reposer EMPILE (`0x1801721D0` ne rend que la racine de la
 * composition, ses enfants continuent de se dessiner -- a reposer chaque
 * trame, la photographie d'une salle blanchissait jusqu'a la surexposition)
 * et rejoue l'ouverture. */
static const char *g_quest_pose[24];
static char g_quest_phase[24];

static void quest_assurer(void)
{
    quest_calque t[QUEST_CALQUES];
    quest_f_fini fini = (quest_f_fini)(g_quest_base + QUEST_RVA_FINI);
    void *ctx = *(void **)(g_quest_base + QUEST_RVA_CONTEXTE);
    char veut[24];
    int n, i, r;
    if (!ctx) return;
    for (i = 0; i < 24; i++) veut[i] = 0;
    n = quest_liste(t);
    for (i = 0; i < n; i++) {
        r = t[i].rang;
        veut[r] = 1;
        if (g_quest_pose[r] != t[i].nom) {          /* neuf, ou change de nom */
            g_quest_pose[r] = t[i].nom;
            g_quest_phase[r] = 1;
            quest_pose(&t[i], t[i].sta_s, t[i].sta_e, QUEST_UNE_FOIS);
            continue;
        }
        /* l'ouverture est finie et il y a un repos : on enchaine, en boucle */
        if (g_quest_phase[r] == 1 && t[i].neu_s && fini(ctx, r)) {
            g_quest_phase[r] = 2;
            quest_pose(&t[i], t[i].neu_s, t[i].neu_e, QUEST_TENIR);
        }
    }
    /* ce qui n'a plus lieu d'etre s'en va (l'icone quand on entre, la photo
     * et la fenetre quand on ressort) */
    for (r = QUEST_RANG_BASE; r < QUEST_RANG_BASE + QUEST_RANGS; r++)
        if (!veut[r] && g_quest_pose[r]) {
            g_quest_pose[r] = 0;
            g_quest_phase[r] = 0;
            quest_rendre(r);
        }
}


/* En partant, on REND les rangs : sans cela la carte survivrait a l'ecran
 * jusqu'a la fin de sa composition (630 images, ~10 s) -- c'est-a-dire par
 * dessus le menu, ce qu'on vient justement de quitter. */
static void quest_retirer_calques(void)
{
    quest_f_liberer liberer =
        (quest_f_liberer)(g_quest_base + QUEST_RVA_LIBERER);
    void *ctx = *(void **)(g_quest_base + QUEST_RVA_CONTEXTE);
    int r;
    if (!ctx) return;
    for (r = 0; r < QUEST_RANGS; r++) {
        liberer(ctx, QUEST_RANG_BASE + r);
        g_quest_pose[QUEST_RANG_BASE + r] = 0;
        g_quest_phase[QUEST_RANG_BASE + r] = 0;
    }
    /* ET LES AUTRES QU ON OCCUPE : les neuf batiments (14..22), le libelle
     * de grade (23) et la plaque (1). Sans cela ils survivraient a l ecran
     * -- et le rang 1 est au MENU de FS, qu on vient de quitter. */
    for (r = QUEST_RANG_BATIMENT; r <= QUEST_RANG_GRADE; r++) {
        liberer(ctx, r);
        g_quest_pose[r] = 0;
        g_quest_phase[r] = 0;
    }
    liberer(ctx, QUEST_RANG_FICHE);
    g_quest_pose[QUEST_RANG_FICHE] = 0;
    g_quest_phase[QUEST_RANG_FICHE] = 0;
    liberer(ctx, QUEST_RANG_PLAQUE);
    g_quest_pose[QUEST_RANG_PLAQUE] = 0;
    g_quest_phase[QUEST_RANG_PLAQUE] = 0;
}

static void quest_quitter(void)
{
    quest_musique(0);
    quest_retirer_calques();
    if (g_quest_boite) g_quest_boite[QUEST_BOITE_SORTIE] = 1;
    g_quest_etape = 0;
    g_quest_avant = 0;
    g_quest_zoom = 0;
    g_quest_sortant = 1;
    quest_profil_ecrire();
    quest_dire("sortie demandee : retour au menu", 0);
}

/* ------------------------------------------------------------------------
 * DESSINER DU TEXTE : LA RECETTE DE FINAL SHOWDOWN, TRANSCRITE
 *
 * CE QUI A CHANGE LE 2026-09-26, ET POURQUOI. La version precedente composait
 * un `app::PrintGC` a la main. Elle partait bien -- le journal montrait
 * `retour=5` pour « QUEST », c'est-a-dire le formatage reussi et
 * `0x18019AC70` atteint -- et rien ne s'affichait, sur AUCUN ecran.
 *
 * On a donc arrete de composer et on est alle lire comment FS dessine SES
 * propres libelles de fenetre. `0x1801BC580` le fait, et c'est le jumeau
 * exact du `FUN_822E39C0` de la Xbox : meme table de fenetres (91 entrees de
 * 24 octets en `0x18052E680` : {planche, _, nom du calque, _, _}), meme
 * lecture d'ANCRE par nom, meme prologue. Trois appels y figurent que nous ne
 * faisions PAS :
 *
 *   1. `0x180187AA0()` / `0x180187CB0(2)` -- lire puis POSER le calque
 *      courant du contexte 2D (`[ctx+0x828]`), et le REMETTRE a la fin. La
 *      Xbox fait le meme geste, avec la meme valeur 2
 *      (`FUN_822C29E8` / `FUN_822C29D8(2)`). Nous, nous laissions le calque
 *      ou l'AET l'avait laisse et nous compensions dans notre descripteur.
 *   2. `0x18019B870(style, 2)` -- le sous-mode du style (style+0x10). Il
 *      commande la CHASSE : a 2, `0x18019B3C0` lit la largeur propre de
 *      chaque glyphe ; a 0, tout est monospace.
 *   3. `0x18019B800(desc, {x,y,l,h}, 9)` -- poser la BOITE, au lieu d'ecrire
 *      +0x34..+0x40 a la main. Il pose aussi `desc+0x2C = 9` et surtout
 *      `desc+0x10 = 1`, ce qui allume le decoupage (0x200) dans
 *      `0x18019AC70` : la boite devient le cadre de decoupe, et les drapeaux
 *      0x800 (retour a la ligne) prennent leur sens.
 *
 * Et le mode du style est **1**, pas 2 (`0x18019B6F0(style, 1)`), la couleur
 * 0xFFD0C8C6 (alpha en octet haut), le format la chaine « %s » du moteur
 * (0x180347CF8), les drapeaux 0x800.
 *
 * CE QUI RESTE DE L'ANCIENNE RECETTE : le rang de dessin. Le contexte 2D
 * range les commandes dans 128 compartiments, d'indice
 *     (desc+0x24) + (((desc+0x28) + calque) << 5)
 * FS laisse le rang du constructeur (7) et pose le calque a 2 : compartiment
 * 71. Notre variante vise 127, le dernier. On dessine LES DEUX tant que la
 * question n'est pas tranchee a l'ecran.
 */
#define QUEST_RVA_DESC_NEUF    0x19A8C0   /* le descripteur, 0x50 octets */
#define QUEST_RVA_STYLE_NEUF   0x19A9D0   /* le style, 0x40 octets */
#define QUEST_RVA_STYLE_MODE   0x19B6F0   /* la police : 0, 1 ou 2 */
#define QUEST_RVA_STYLE_SOUS   0x19B870   /* le sous-mode : la chasse */
#define QUEST_RVA_STYLE_TAILLE 0x19B830   /* la taille en pixels */
#define QUEST_RVA_DESC_BOITE   0x19B800   /* poser {x, y, largeur, hauteur} */
/* LE DESSIN D UN SPRITE (2026-10-20).
 *
 * Le depot avait toujours CONTOURNE ce dessin, en posant une composition a
 * la place. Les paves de costume ne le permettent pas : aucun calque AET ne
 * dessine `COL_ICO_*`. La chaine, lue dans le moteur :
 *
 *     0x189880  construit le descripteur de commande
 *     0x18E7C0  y pose la TAILLE
 *     0x187AF0  depose la commande (il ajoute le contexte 2D lui-meme)
 *               -> 0x18018CA20, le point ou tout le 2D se depose
 *
 * La commande, champ par champ (§37.15) :
 *
 *     +0x00  le type ; 2 pour un quad
 *     +0x04  L IDENTIFIANT DU SPRITE ; 0xFFFFFFFF = pas de sprite
 *     +0x14  le calque ; -1 = celui du contexte
 *     +0x18  le rang,        +0x1C  le compartiment
 *     +0x20 et +0x24  la couleur, ecrite DEUX fois
 *     +0x34 et +0x38  la position
 *
 * L identifiant se lit `jeu << 16 | rang`, et c est exactement ce que la
 * base des sprites appelle `info` -- le meme format que le dossier avait
 * deja releve pour la police (`quest_diagnostic_police`). */
#define QUEST_RVA_CMD_NEUF     0x189880
#define QUEST_RVA_CMD_TAILLE   0x18E7C0
#define QUEST_RVA_CMD_POSER    0x187C00   /* celle qui RESOUT le sprite */
#define QUEST_RVA_CMD_BRUT     0x187AF0   /* celle qui depose tel quel   */
#define QUEST_RVA_SPR_RESOUDRE 0x18C610   /* identifiant -> enregistrement */
/* LA CONSTRUCTION DU JEU, appelee telle quelle (2026-10-20).
 *
 * Notre construction manuelle du descripteur fait planter. Avant de la
 * corriger a l aveugle, on appelle la fonction QUI LE CONSTRUIT :
 * `0x180187B10`. Sa signature est lue au desassembleur -- quatre flottants
 * en xmm0..xmm3 (le rectangle), puis quatre entiers par la pile :
 *
 *     a5 -> +0x20 ET +0x24      a7 -> +0x08
 *     a6 -> +0x1C              a8 -> +0x18
 *
 * Elle ne pose PAS `+0x04`, donc elle dessine un quad sans sprite. Si le
 * quad apparait, la chaine est bonne et c est notre construction qui est
 * fausse ; s il ne parait pas, c est le contexte ou le compartiment. */
#define QUEST_RVA_CMD_JEU      0x187B10
#define QUEST_CMD_TAILLE       0x140
/* LES PAVES DE COSTUME SONT DEJA DANS FINAL SHOWDOWN, en anglais -- comme
 * le badge de grade l etait (§29). `spr_db.bin` les donne :
 *
 *     SPR_C_CMN_COL_ICO_MAIN_1_E .. _4_E   0x1000F 0x10011 0x10013 0x10015
 *     SPR_C_CMN_COL_ICO_SUB_1_E  .. _2_E   0x1001B 0x1001D
 *
 * Rien a importer. Le suffixe `_E` est la version anglaise ; les versions
 * sans suffixe sont japonaises. */
#define QUEST_SPR_COS_MAIN_1   55095     /* l id de la BASE, pas info */
#define QUEST_SPR_COS_SUB_1    0x1001B
#define QUEST_RVA_DESSIN       0x19B2E0   /* variadique : (desc, drap, fmt,..) */
#define QUEST_RVA_CALQUE_LIRE  0x187AA0   /* lire  [contexte 2D + 0x828] */
#define QUEST_RVA_CALQUE_POSER 0x187CB0   /* poser [contexte 2D + 0x828] */
#define QUEST_RVA_FMT          0x347CF8   /* la chaine « %s » du moteur */
#define QUEST_RVA_POLICES      0x750FF8   /* la table des polices (diagnostic) */
#define QUEST_RVA_CTX2D        0x719900   /* le contexte 2D global */
#define QUEST_CTX_CALQUE       0x828      /* le calque courant, dedans */
#define QUEST_CALQUE_TEXTE     2          /* celui que FS monte pour son texte */
#define QUEST_DRAPEAUX         0x800      /* retour a la ligne dans la boite */
#define QUEST_COULEUR          0xFFD0C8C6u  /* le blanc casse de FS */
#define QUEST_PLAFOND          3          /* le dernier calque du tableau */
#define QUEST_ORDRE            31         /* son dernier rang */

typedef void (*quest_f_1p)(void *p);
typedef void (*quest_f_pi)(void *p, int v);
typedef void (*quest_f_pf)(void *p, float v);
typedef void (*quest_f_boite)(void *desc, const float *xylh, int mode);
typedef int (*quest_f_dessin)(void *desc, int drapeaux, const char *fmt,
                              const char *texte);
typedef int (*quest_f_calque_lire)(void);
typedef void (*quest_f_calque_poser)(int v);

/* Les deux objets sont des objets de PILE chez CRI ; on les garde ici, ou ils
 * ne genent personne : un seul fil dessine, une fois par trame. */
static int g_quest_vu_rappel, g_quest_vu_ecrire, g_quest_retour;
static int g_quest_vu_contenu;   /* le journal, une fois par fenetre */
static __attribute__((aligned(16))) char g_quest_desc[0x50];
static __attribute__((aligned(16))) char g_quest_style[0x40];

/* `rang127` : 0 = la profondeur de FS (compartiment 71), 1 = la notre (127). */
/* LE TEXTE A SON ESPACE, LUI AUSSI (2026-10-20).
 *
 * `0x18019B800(descripteur, {x, y, largeur, hauteur}, 9)` range son
 * troisieme argument dans `descripteur + 0x2C` : c est l ESPACE DE
 * RESOLUTION du texte, le meme numero de mode que pour les calques. Le 9
 * veut dire 1280 x 768, l espace natif de Final Showdown.
 *
 * CE QUE CELA COUTAIT, et la mesure le dit au pixel : `FUN_18016AF60`
 * applique, quand la source vaut 9 ou 3 et la cible 13 a 16, un recadrage
 *
 *     y -= (hauteur_source - 720)
 *
 * soit 48 unites, soit 48 x 1080/768 = 67,5 pixels. Le texte etait mesure
 * 66 pixels trop haut. C est le meme recadrage, et rien d autre.
 *
 * En posant 13, la source egale la cible : le recadrage ne s applique plus
 * (13 n est ni 9 ni 3), la conversion devient l identite, et nos ancres --
 * relevees dans des planches de 1280 x 720 -- se disent telles quelles. */
#define QUEST_TEXTE_ESPACE  QUEST_ESPACE_720

static void quest_ecrire_boite(float x, float y, float largeur, float hauteur,
                               float taille, unsigned couleur, int drapeaux,
                               int rang127, const char *texte)
{
    unsigned char *b = g_quest_base;
    float boite[4];
    int sauv;
    if (!b || !texte || !*texte) return;

    /* LE CALQUE DU CONTEXTE 2D. FS le monte a 2 pour son texte de fenetre et
     * le remet ensuite ; on fait le meme geste, restauration comprise -- il
     * est GLOBAL, le laisser deplace casserait le reste de l'image. */
    sauv = ((quest_f_calque_lire)(b + QUEST_RVA_CALQUE_LIRE))();
    ((quest_f_calque_poser)(b + QUEST_RVA_CALQUE_POSER))(QUEST_CALQUE_TEXTE);

    ((quest_f_1p)(b + QUEST_RVA_DESC_NEUF))(g_quest_desc);
    ((quest_f_1p)(b + QUEST_RVA_STYLE_NEUF))(g_quest_style);
    ((quest_f_pi)(b + QUEST_RVA_STYLE_MODE))(g_quest_style, 1);
    ((quest_f_pi)(b + QUEST_RVA_STYLE_SOUS))(g_quest_style, 2);
    ((quest_f_pf)(b + QUEST_RVA_STYLE_TAILLE))(g_quest_style, taille);
    *(void **)(g_quest_desc + 0x48) = g_quest_style;

    boite[0] = x;
    boite[1] = y;
    boite[2] = largeur;
    boite[3] = hauteur;
    ((quest_f_boite)(b + QUEST_RVA_DESC_BOITE))(g_quest_desc, boite,
                                                QUEST_TEXTE_ESPACE);
    *(unsigned *)(g_quest_desc + 0x08) = couleur;
    if (rang127) {
        /* le dernier compartiment : rang 31 du calque 3. Le calque courant
         * vaut 2 puisque nous venons de le poser. */
        *(int *)(g_quest_desc + 0x24) = QUEST_ORDRE;
        *(int *)(g_quest_desc + 0x28) = QUEST_PLAFOND - QUEST_CALQUE_TEXTE;
    }
    g_quest_retour = ((quest_f_dessin)(b + QUEST_RVA_DESSIN))(
        g_quest_desc, drapeaux,
        (const char *)(b + QUEST_RVA_FMT), texte);

    ((quest_f_calque_poser)(b + QUEST_RVA_CALQUE_POSER))(sauv);
}

/* UN SPRITE, PAR SON IDENTIFIANT (2026-10-20).
 *
 * Voir le bloc QUEST_RVA_CMD_NEUF pour la structure de la commande. On fait
 * les memes gestes que `quest_ecrire_boite` autour : le calque du contexte
 * 2D monte a 2 et redescend, et le compartiment est le notre.
 *
 * La taille passe par `0x18E7C0`, qui prend les deux flottants EMPAQUETES
 * dans un seul registre -- c est ainsi que `0x180187B10` l appelle
 * (`vunpcklps` puis `vmovq rdx, xmm1`). On le reproduit avec une union. */
static void quest_sprite(unsigned id, float x, float y, float w, float h,
                         unsigned couleur)
{
    unsigned char *b = g_quest_base;
    unsigned char d[QUEST_CMD_TAILLE];
    union { unsigned long long u; float f[2]; } taille;
    int sauv;
    if (!b) return;

    sauv = ((quest_f_calque_lire)(b + QUEST_RVA_CALQUE_LIRE))();
    ((quest_f_calque_poser)(b + QUEST_RVA_CALQUE_POSER))(QUEST_CALQUE_TEXTE);

    /* LE DESCRIPTEUR, COPIE SUR CELUI DU JEU (§37.19). `FUN_180108320`, le
     * dessin d un glyphe, est le SEUL appelant de `0x180187AF0` ; relever ce
     * qu il ecrit donne la liste complete. Nous n en posions que six. */
    ((quest_f_desc_init)(b + QUEST_RVA_CMD_NEUF))(d);
    *(unsigned *)(d + 0x00) = 0;            /* 0 = un SPRITE a resoudre   */
    *(unsigned *)(d + 0x04) = id;           /* L IDENTIFIANT DU SPRITE    */
    *(unsigned *)(d + 0x08) = 0;
    *(unsigned *)(d + 0x0C) |= 2;           /* le drapeau que le jeu pose */
    *(unsigned *)(d + 0x10) = 0;
    *(int *)(d + 0x14) = -1;                /* le calque du contexte      */
    *(int *)(d + 0x18) = 0;                 /* essai : le premier         */
    *(int *)(d + 0x1C) = 0;                 /* compartiment du calque     */
    *(unsigned *)(d + 0x20) = couleur;      /* la couleur, DEUX fois      */
    *(unsigned *)(d + 0x24) = couleur;
    *(float *)(d + 0x34) = x;               /* la position                */
    *(float *)(d + 0x38) = y;
    *(unsigned *)(d + 0x3C) = 0;
    *(float *)(d + 0x40) = 1.0f;            /* L ECHELLE -- elle manquait */
    *(float *)(d + 0x44) = 1.0f;
    *(unsigned *)(d + 0x58) = 0;
    *(unsigned *)(d + 0xAC) = 0x2D;         /* ce que le jeu y met        */
    taille.f[0] = w;
    taille.f[1] = h;
    ((quest_f_cmd_taille)(b + QUEST_RVA_CMD_TAILLE))(d, taille.u);
    ((quest_f_cmd_poser)(b + QUEST_RVA_CMD_POSER))(d);

    ((quest_f_calque_poser)(b + QUEST_RVA_CALQUE_POSER))(sauv);
}

/* La forme courte : une ligne, une boite large de 640 et haute de 64. */
static void quest_ecrire(float x, float y, float taille, const char *texte)
{
    if (!texte || !*texte) return;
    quest_ecrire_boite(x + 2.0f, y + 2.0f, 640.0f, 64.0f, taille,
                       0xFF000000u, QUEST_DRAPEAUX, 0, texte);
    quest_ecrire_boite(x, y, 640.0f, 64.0f, taille, QUEST_COULEUR,
                       QUEST_DRAPEAUX, 0, texte);
}

/* LE DIAGNOSTIC, UNE SEULE FOIS. Si les deux temoins restent invisibles, la
 * reponse est ici : `0x18018CA20` laisse TOMBER la commande, sans un mot,
 * quand le jeu de sprites de la police n'est pas enregistre dans le contexte
 * 2D. L'identifiant de sprite de la police est le premier mot du descripteur
 * de police, et son jeu en est les bits 16..27. */
static void quest_diagnostic_police(void)
{
    unsigned char *b = g_quest_base;
    unsigned char *table, *police, *ctx;
    char m[220];
    unsigned id;
    int mode;
    if (!b) return;
    ctx = *(unsigned char **)(b + QUEST_RVA_CTX2D);
    table = *(unsigned char **)(b + QUEST_RVA_POLICES);
    _snprintf(m, sizeof m, "contexte 2D %p, calque %d, table des polices %p ;",
              (void *)ctx,
              ctx ? *(int *)(ctx + QUEST_CTX_CALQUE) : -1, (void *)table);
    quest_dire(m, 0);
    if (!table) return;
    for (mode = 0; mode < 3; mode++) {
        police = *(unsigned char **)(table + 0x98 + mode * 0x18);
        if (!police) {
            _snprintf(m, sizeof m, "police mode %d : ABSENTE, jeu", mode);
            quest_dire(m, -1);
            continue;
        }
        id = *(unsigned *)police;
        _snprintf(m, sizeof m,
                  "police mode %d : descripteur %p, sprite %08X, jeu",
                  mode, (void *)police, id);
        quest_dire(m, (long long)((id >> 16) & 0xFFF));
    }
}

/* ------------------------------------------------------------------------
 * LES MILLE RIVAUX
 *
 * `tools/rivaux.py --ajouter` pose `npc_tbl.bin` dans
 * `vf5fs_media/rom/` -- Final Showdown n'en avait AUCUN, les rivaux etaient
 * partis avec le mode. On le lit ici, une fois.
 *
 * Un rival n'est pas une chaine, c'est un enregistrement de 0x90 octets :
 * son nom, sa replique en deux lignes, SON PERSONNAGE, les reglages de son
 * IA. C'est pour cela qu'on pose le fichier plutot que d'ajouter des libelles
 * a `string_array` : l'etape 4 -- se battre contre un rival -- en aura besoin
 * en entier. Disposition et mesures : `tools/rivaux.py`.
 *
 * Les entiers sont GROS-BOUTISTES : c'est un fichier de Xbox 360.
 */
#define QUEST_RIVAUX_FICHIER "vf5fs_media/rom/npc_tbl.bin"
#define QUEST_RIVAUX_NOMBRE  1000
#define QUEST_RIVAUX_PAS     0x90
#define QUEST_RIVAL_NOM      0x00
#define QUEST_RIVAL_DIT1     0x04
#define QUEST_RIVAL_DIT2     0x08
#define QUEST_RIVAL_PERSO    0x14

static unsigned char *g_quest_rivaux;     /* la table, ou NULL */
static long g_quest_rivaux_taille;
static int g_quest_rivaux_vu;             /* 1 = deja cherchee */

static unsigned quest_be32(const unsigned char *p)
{
    return ((unsigned)p[0] << 24) | ((unsigned)p[1] << 16)
         | ((unsigned)p[2] << 8) | p[3];
}

/* La table, chargee a la premiere demande. Absente = on ne dessine pas de
 * noms, et le reste de l'ecran continue : le module reste inerte sur un jeu
 * ou `rivaux.py --ajouter` n'a pas ete passe. */
static unsigned char *quest_rivaux(void)
{
    FILE *f;
    long n;
    if (g_quest_rivaux_vu) return g_quest_rivaux;
    g_quest_rivaux_vu = 1;
    f = fopen(QUEST_RIVAUX_FICHIER, "rb");
    if (!f) {
        quest_dire("table des rivaux ABSENTE (" QUEST_RIVAUX_FICHIER ")", 0);
        return 0;
    }
    fseek(f, 0, SEEK_END);
    n = ftell(f);
    fseek(f, 0, SEEK_SET);
    if (n >= (long)(QUEST_RIVAUX_NOMBRE * QUEST_RIVAUX_PAS)) {
        g_quest_rivaux = (unsigned char *)malloc((size_t)n);
        if (g_quest_rivaux && fread(g_quest_rivaux, 1, (size_t)n, f)
                == (size_t)n) {
            g_quest_rivaux_taille = n;
        } else {
            free(g_quest_rivaux);
            g_quest_rivaux = 0;
        }
    }
    fclose(f);
    if (g_quest_rivaux) {
        char m[160];
        _snprintf(m, sizeof m, "table des rivaux chargee, %ld octets ; "
                  "le premier est \"%s\" ; rivaux", n,
                  (const char *)(g_quest_rivaux
                      + quest_be32(g_quest_rivaux + QUEST_RIVAL_NOM)));
        quest_dire(m, QUEST_RIVAUX_NOMBRE);
    } else {
        quest_dire("table des rivaux ILLISIBLE, octets", (long long)n);
    }
    return g_quest_rivaux;
}

/* Le champ <offset> du rival <n>, en chaine. Rend NULL si la table n'est pas
 * la ou si l'offset sort du fichier -- il vient du fichier, on ne lui fait
 * pas confiance. */
static const char *quest_rival_texte(int n, int champ)
{
    unsigned char *t = quest_rivaux();
    unsigned o;
    if (!t || n < 0 || n >= QUEST_RIVAUX_NOMBRE) return 0;
    o = quest_be32(t + (long)n * QUEST_RIVAUX_PAS + champ);
    if (o == 0 || (long)o >= g_quest_rivaux_taille) return 0;
    return (const char *)(t + o);
}

/* LE GRADE DU RIVAL. `npc_tbl + 0x7C`, 42 crans, 0 = 10th kyu -- mesure du
 * 2026-09-29, verifiee sur une capture du jeu de 2007 : « Raeme 4th kyu » est
 * le grade 6, « Qazi 10th kyu » le grade 0. */
#define QUEST_RIVAL_GRADE 0x7C

static int quest_rival_grade(int n)
{
    unsigned char *t = quest_rivaux();
    if (!t || n < 0 || n >= QUEST_RIVAUX_NOMBRE) return -1;
    return t[(long)n * QUEST_RIVAUX_PAS + QUEST_RIVAL_GRADE];
}

static int quest_rival_perso(int n)
{
    unsigned char *t = quest_rivaux();
    if (!t || n < 0 || n >= QUEST_RIVAUX_NOMBRE) return -1;
    return t[(long)n * QUEST_RIVAUX_PAS + QUEST_RIVAL_PERSO];
}

/* ------------------------------------------------------------------------
 * LE PROFIL DU QUEST
 *
 * C'est lui qui manquait, et il commandait tout le reste : les valeurs du
 * statut, la liste par lieu, le masquage des rivaux, les emblemes.
 *
 * CE QU'EN FAIT LA VERSION DE 2007. Le profil vit en `+0xC0` de la
 * sauvegarde du joueur (`FUN_8230B5B8`), et le Quest n'y lit que deux choses
 * pour ses ecrans :
 *
 *   profil + 0x74   1000 bits : le rival a ete RENCONTRE
 *   profil + 0xF4   1000 bits : le rival a ete BATTU
 *
 * Les deux champs sont des tableaux de trente-deux u32 -- 0xF4 - 0x74 = 0x80,
 * soit exactement 1000 bits arrondis. Le test du jeu est
 * `1 << (n & 0x1F) & champ[(n >> 3) & 0x1FFFFFFC]`, et le POURCENTAGE de la
 * premiere ligne du statut se lit en clair (0x8230F3xx) :
 *
 *     compte = les rivaux A LA FOIS rencontres ET battus
 *     pourcentage = compte * 0.001 * 100        (soit compte / 10)
 *
 * Les deux constantes sont dans le binaire, `_DAT_82006C1C` = 0,001 et
 * `DAT_82003EDC` = 100 : la formule n'est pas devinee.
 *
 * NOTRE FICHIER. On ne recopie pas la sauvegarde Xbox -- elle est prise dans
 * un conteneur de profil qui n'a pas d'equivalent ici. On ecrit le NOTRE, a
 * cote du jeu, avec les memes champs et en petit-boutiste :
 *
 *   +0x000  8    « QUESTPRF »
 *   +0x008  u32  version (1)
 *   +0x00C  u32  reserve
 *   +0x010  128  RENCONTRE, 1000 bits
 *   +0x090  128  BATTU,     1000 bits
 *   +0x110  u32  la plus longue serie de victoires
 *   +0x114  u32  le nombre de combats
 *   +0x118  u32  le temps de jeu, en SECONDES
 *   +0x11C  u32  reserve
 *
 * CE QUI LE REMPLIT AUJOURD'HUI, ET CE QUI NE LE REMPLIT PAS. Le temps de jeu
 * avance : c'est reel, et c'est ce qui prouve a l'ecran que le profil vit et
 * survit au redemarrage. « Rencontre » se pose quand on OUVRE un lieu -- ce
 * point est une DECISION DE PORTAGE, pas une transcription : la version de
 * 2007 le pose au combat, et il n'y a pas encore de combat. « Battu » reste
 * donc a zero, et les quatre pourcentages avec lui, ce qui est l'etat exact
 * d'un Quest ou l'on n'a encore gagne contre personne.
 */
#define QUEST_PROFIL_FICHIER "quest_profil.bin"
#define QUEST_PROFIL_MAGIE   "QUESTPRF"
#define QUEST_PROFIL_VERSION 3
#define QUEST_PROFIL_TAILLE  0x250
#define QUEST_PO_VERSION     0x008
#define QUEST_PO_RENCONTRE   0x010
#define QUEST_PO_BATTU       0x090
#define QUEST_PO_SERIE       0x110
#define QUEST_PO_COMBATS     0x114
#define QUEST_PO_SECONDES    0x118
#define QUEST_PROFIL_BITS    128          /* 1000 bits arrondis a 32 u32 */
/* LA CARRIERE, version 2 du profil (2026-09-29).
 *
 * Le Quest de 2007 ne range pas ces champs au meme endroit : il a une FICHE
 * DE JOUEUR vivante (`0x827A99F8 + 0x10 + joueur * 0x528`) et un PROFIL DE
 * SAUVEGARDE (`sauvegarde + 0xC0`) qui la persiste. Chez nous les deux se
 * confondent dans `quest_profil.bin` -- nous n'avons pas de conteneur de
 * sauvegarde Xbox. Les valeurs, elles, sont celles du jeu :
 *
 *   nom      fiche + 0x59      argent   fiche + 0xEC   (libelle 999 « %dG »)
 *   W        fiche + 0x100     L        fiche + 0x104  (libelles 396, 397)
 *   grade    fiche + 0x423     0 = 10th kyu, 42 crans
 *
 * L'argent de depart et le plafond sont ceux de la sequence d'accueil
 * `0x8230CF50` : **50 000** verses, **999 999** au plafond. */
#define QUEST_PO_PERSO       0x11C        /* 0..18 ; -1 = pas de donnees */
#define QUEST_PO_ARGENT      0x120
#define QUEST_PO_VICTOIRES   0x124
#define QUEST_PO_DEFAITES    0x128
#define QUEST_PO_GRADE       0x12C        /* 0 = 10th kyu */
#define QUEST_PO_NOM         0x130        /* 16 octets, termine par zero */
#define QUEST_PO_CREE        0x140        /* 1 = les donnees existent */
#define QUEST_PO_NOM_TAILLE  16
#define QUEST_ARGENT_DEPART  50000
#define QUEST_ARGENT_MAX     999999
#define QUEST_NOM_DEFAUT     "NO-NAME"
/* VERSION 3 (2026-09-30) : ce que l'apres-combat et la boutique demandent.
 *
 *   +0x144 la difficulte du Quest (0, 1, 2) -- `TaskQuestOption` ; c'est elle
 *          qui ajoute +0,2 ou +0,4 a la force du CPU (§9.26)
 *   +0x148 la serie EN COURS ; `+0x110` garde la plus longue
 *   +0x150 les OBJETS possedes : 2 000 bits, comme le `bitset<2000>` que FS
 *          tient en `dossier + 0x160`
 *   +0x24C les familles d'emblemes gagnees (treize, libelles 571-584) */
#define QUEST_PO_DIFFICULTE  0x144
#define QUEST_PO_SERIE_EN_COURS 0x148
#define QUEST_PO_OBJETS      0x150        /* 250 octets, 2 000 bits */
#define QUEST_PO_EMBLEMES    0x24C
#define QUEST_OBJETS_BITS    250

static unsigned char g_quest_profil[QUEST_PROFIL_TAILLE];
static int g_quest_profil_pret;           /* 1 = charge (ou cree) */
static int g_quest_profil_sale;           /* 1 = a reecrire */
static unsigned g_quest_profil_ms;        /* millisecondes non encore comptees */

static unsigned quest_lire32(int off)
{
    const unsigned char *p = g_quest_profil + off;
    return (unsigned)p[0] | ((unsigned)p[1] << 8)
         | ((unsigned)p[2] << 16) | ((unsigned)p[3] << 24);
}

static void quest_ecrire32(int off, unsigned v)
{
    unsigned char *p = g_quest_profil + off;
    p[0] = (unsigned char)v;        p[1] = (unsigned char)(v >> 8);
    p[2] = (unsigned char)(v >> 16); p[3] = (unsigned char)(v >> 24);
}

static void quest_profil_neuf(void)
{
    memset(g_quest_profil, 0, sizeof g_quest_profil);
    memcpy(g_quest_profil, QUEST_PROFIL_MAGIE, 8);
    quest_ecrire32(QUEST_PO_VERSION, QUEST_PROFIL_VERSION);
    quest_ecrire32(QUEST_PO_PERSO, 0xFFFFFFFFu);   /* pas de donnees */
    g_quest_profil_sale = 1;
}

/* Le profil, charge a la premiere demande. Un fichier absent, trop court, ou
 * d'une autre version repart a neuf : mieux vaut un profil vide qu'un profil
 * mal lu. */
static void quest_profil_charger(void)
{
    FILE *f;
    size_t n;
    if (g_quest_profil_pret) return;
    g_quest_profil_pret = 1;
    f = fopen(QUEST_PROFIL_FICHIER, "rb");
    if (!f) {
        quest_profil_neuf();
        quest_dire("profil Quest : aucun, on en cree un neuf", 0);
        return;
    }
    n = fread(g_quest_profil, 1, sizeof g_quest_profil, f);
    fclose(f);
    /* UN PROFIL DE VERSION 1 N'EST PAS ILLISIBLE : il lui manque la carriere.
     * On garde ses mille bits, ses combats et son temps de jeu -- c'est ce
     * qu'il a de plus precieux -- et on lui ajoute les champs neufs a zero,
     * donc « pas de donnees creees ». Effacer le profil d'un joueur parce
     * qu'on a ajoute des champs serait la pire facon de faire. */
    if (memcmp(g_quest_profil, QUEST_PROFIL_MAGIE, 8) == 0
            && (quest_lire32(QUEST_PO_VERSION) == 1
                || quest_lire32(QUEST_PO_VERSION) == 2)) {
        /* ON NE JETTE JAMAIS UN PROFIL : on complete. La version 1 n'avait
         * pas de carriere, la version 2 pas d'objets ni de difficulte. */
        long garde = (quest_lire32(QUEST_PO_VERSION) == 1) ? 0x11C : 0x144;
        memset(g_quest_profil + garde, 0, QUEST_PROFIL_TAILLE - garde);
        if (garde == 0x11C) quest_ecrire32(QUEST_PO_PERSO, 0xFFFFFFFFu);
        quest_ecrire32(QUEST_PO_VERSION, QUEST_PROFIL_VERSION);
        g_quest_profil_sale = 1;
        quest_dire("profil Quest repris d'une version anterieure ; combats",
                   (long long)quest_lire32(QUEST_PO_COMBATS));
        return;
    }
    if (n != sizeof g_quest_profil
            || memcmp(g_quest_profil, QUEST_PROFIL_MAGIE, 8) != 0
            || quest_lire32(QUEST_PO_VERSION) != QUEST_PROFIL_VERSION) {
        quest_profil_neuf();
        quest_dire("profil Quest ILLISIBLE, on repart a neuf ; octets lus",
                   (long long)n);
        return;
    }
    {
        char m[180];
        _snprintf(m, sizeof m,
                  "profil Quest charge : %u combats, plus longue serie %u ;"
                  " secondes de jeu",
                  quest_lire32(QUEST_PO_COMBATS),
                  quest_lire32(QUEST_PO_SERIE));
        quest_dire(m, (long long)quest_lire32(QUEST_PO_SECONDES));
    }
}

/* Le grade du joueur, ou -1 tant qu il n a pas de donnees. */
static int quest_grade_joueur(void)
{
    quest_profil_charger();
    if (!quest_lire32(QUEST_PO_CREE)) return -1;
    return (int)quest_lire32(QUEST_PO_GRADE);
}

static void quest_profil_ecrire(void)
{
    FILE *f;
    if (!g_quest_profil_pret || !g_quest_profil_sale) return;
    f = fopen(QUEST_PROFIL_FICHIER, "wb");
    if (!f) {
        quest_dire("profil Quest : ECRITURE IMPOSSIBLE", 0);
        return;
    }
    fwrite(g_quest_profil, 1, sizeof g_quest_profil, f);
    fclose(f);
    g_quest_profil_sale = 0;
}

/* Les deux champs de bits, testes comme le jeu les teste. */
static int quest_profil_bit(int champ, int n)
{
    if (n < 0 || n >= QUEST_RIVAUX_NOMBRE) return 0;
    quest_profil_charger();
    return (g_quest_profil[champ + (n >> 3)] >> (n & 7)) & 1;
}

static void quest_profil_poser(int champ, int n)
{
    if (n < 0 || n >= QUEST_RIVAUX_NOMBRE) return;
    quest_profil_charger();
    if (!((g_quest_profil[champ + (n >> 3)] >> (n & 7)) & 1)) {
        g_quest_profil[champ + (n >> 3)] |= (unsigned char)(1 << (n & 7));
        g_quest_profil_sale = 1;
    }
}

/* Combien de rivaux sont A LA FOIS rencontres ET battus -- c'est ce que
 * compte la premiere ligne du statut chez 2007. */
static int quest_profil_compte_battus(void)
{
    int n, c = 0;
    quest_profil_charger();
    for (n = 0; n < QUEST_RIVAUX_NOMBRE; n++)
        if (quest_profil_bit(QUEST_PO_RENCONTRE, n)
                && quest_profil_bit(QUEST_PO_BATTU, n))
            c++;
    return c;
}

static int quest_profil_compte_rencontres(void)
{
    int n, c = 0;
    quest_profil_charger();
    for (n = 0; n < QUEST_RIVAUX_NOMBRE; n++)
        if (quest_profil_bit(QUEST_PO_RENCONTRE, n)) c++;
    return c;
}

/* Le temps de jeu, en secondes.
 *
 * PIEGE, ET IL A COUTE UN ESSAI. `quest_tic` ne recoit PAS un ecart : il
 * recoit l'horloge ABSOLUE du module (`GetTickCount() - g_quest_t0`). La
 * premiere version ajoutait cette valeur a chaque image -- Frederic, a
 * l'ecran : « completion time / total playing time changent en continu », et
 * le profil affichait 77 heures apres quelques minutes. On garde donc
 * l'instant precedent et on n'ajoute que la difference.
 *
 * `g_quest_horloge_avant` est remis a zero en sortant du Quest : sinon, la
 * fois suivante, tout le temps passe DEHORS entrerait d'un coup. L'ecretage
 * a une seconde couvre le reste -- un ecran de chargement ne doit pas
 * compter pour dix minutes. */
static unsigned g_quest_horloge_avant;

static void quest_profil_horloge(unsigned maintenant)
{
    unsigned ecart;
    quest_profil_charger();
    if (!g_quest_horloge_avant) {
        g_quest_horloge_avant = maintenant ? maintenant : 1;
        return;
    }
    ecart = maintenant - g_quest_horloge_avant;
    g_quest_horloge_avant = maintenant ? maintenant : 1;
    if (ecart > 1000) ecart = 1000;
    g_quest_profil_ms += ecart;
    if (g_quest_profil_ms >= 1000) {
        quest_ecrire32(QUEST_PO_SECONDES,
                       quest_lire32(QUEST_PO_SECONDES)
                       + g_quest_profil_ms / 1000);
        g_quest_profil_ms %= 1000;
        g_quest_profil_sale = 1;
    }
}

/* LE LIEU D'UN RIVAL -- et donc la liste d'un lieu
 *
 * `FUN_8230E018(vecteur, filtre, masque)` construit la liste du lieu, et elle
 * ne demande AUCUN profil : elle parcourt les mille rivaux et garde ceux dont
 * `npc_tbl[n] + 0x88` tombe dans le masque. Le champ `+0x88` est donc LE
 * LIEU, et la mesure le confirme -- huit valeurs, 130 a 138 rivaux pour les
 * sept premieres, 59 pour la huitieme, mille en tout.
 *
 * LA HUITIEME. Le sous-titre de la fenetre de 2007 se prend dans
 * {528..534, 556} : les sept lieux nommes, puis « Special » -- et non 535
 * « EVENT SQUARE », le nom que la carte donne au dome. Nos sept premieres
 * salles valent donc lieu 0 a 6, mot pour mot. Pour le dome, on prend le
 * huitieme : c'est le seul restant, ses 59 rivaux sont un groupe trie a la
 * main, et le dome est le lieu des tournois. C'est une LECTURE, pas une
 * mesure -- elle est ici pour etre contredite si le jeu dit autre chose.
 * La maison n'a pas de rivaux.
 */
#define QUEST_RIVAL_LIEU 0x88

static const signed char g_quest_lieu_de_salle[9] = {
    0, 1, 2, 3, 4, 5, 6,   /* swn sws swr csd csb sac sae */
    7,                     /* dom : le huitieme groupe, « Special » */
    -1                     /* hom : la maison n'a pas de rivaux */
};

static int quest_rival_lieu(int n)
{
    unsigned char *t = quest_rivaux();
    if (!t || n < 0 || n >= QUEST_RIVAUX_NOMBRE) return -1;
    return t[(long)n * QUEST_RIVAUX_PAS + QUEST_RIVAL_LIEU];
}

/* Le <rang>-ieme rival du lieu, ou -1. Un balayage de mille entrees par
 * ligne coute un millier de lectures d'octet : c'est gratuit a cote d'un
 * dessin de texte, et cela evite de garder un index a jour. */
static int quest_rival_du_lieu(int lieu, int rang)
{
    int n, k = 0;
    if (lieu < 0) return -1;
    for (n = 0; n < QUEST_RIVAUX_NOMBRE; n++) {
        if (quest_rival_lieu(n) != lieu) continue;
        if (k == rang) return n;
        k++;
    }
    return -1;
}

static int quest_lieu_courant(void)
{
    if (g_quest_salle < 0 || g_quest_salle > 8) return -1;
    return g_quest_lieu_de_salle[g_quest_salle];
}

/* OUVRIR UN LIEU, C'EST RENCONTRER SES RIVAUX.
 *
 * DECISION DE PORTAGE, et elle est assumee : la version de 2007 pose le bit
 * « rencontre » au COMBAT, et il n'y a pas encore de combat. Sans cela la
 * liste n'afficherait que des « ？？？？？ » et le profil ne se verrait
 * jamais. Le jour ou l'etape 4 arrive, cette fonction disparait et c'est le
 * combat qui pose le bit. */
static void quest_profil_ouvrir_lieu(int lieu)
{
    int n;
    if (lieu < 0 || !quest_rivaux()) return;
    for (n = 0; n < QUEST_RIVAUX_NOMBRE; n++)
        if (quest_rival_lieu(n) == lieu)
            quest_profil_poser(QUEST_PO_RENCONTRE, n);
}

/* Ce que 2007 montre a la place d'un nom. « ？？？？？ » : cinq points
 * d'interrogation pleine chasse (U+FF1F), la chaine `0x8208E508` en
 * Shift-JIS. L'etoile des rivaux battus est `0x820117C8`, U+2605. On les
 * ecrit en UTF-8 : le dessin de FS convertit en UTF-16 avant de composer. */
#define QUEST_INCONNU "\xEF\xBC\x9F\xEF\xBC\x9F\xEF\xBC\x9F\xEF\xBC\x9F" \
                      "\xEF\xBC\x9F"
#define QUEST_ETOILE  "\xE2\x98\x85"

/* ------------------------------------------------------------------------
 * LE CONTENU DES FENETRES, POSE SUR LES ANCRES
 *
 * Rien ici n'est place a l'oeil. Les coordonnees viennent de la planche
 * `aet_n_qwin.bin` elle-meme : ses fenetres portent des calques `p_*` et
 * `c_*` qui ne dessinent rien -- ce sont des REPERES, et le suffixe du nom
 * donne l'alignement (`_lt` gauche-haut, `_rt` droite-haut, `_ct`
 * centre-haut, `_c` centre). La version Xbox les lit par leur nom
 * (`FUN_82166778`, dont le jumeau chez FS est `0x1800298B0`) et y pose son
 * texte. La table complete est dans `analysis/quest/ancres_qwin.txt`.
 *
 *   hall_menu_win    p_hall_menu_win_01_ct        640 100
 *                    c_button_csr_c_01_lt         252 133
 *                    c_button_csr_d_01_lt         252 271
 *                    c_button_csr_d_02_lt         252 335
 *   home_menu_win    p_home_menu_win_30_02_ct     640 166
 *                    p_home_menu_win_30_03_ct     640 330
 *   player_list_win  p_plylist_win_01_ct          640  95
 *                    p_plylist_win_02_ct          640 141
 *   status_win       p_status_win_01_ct           640 135
 *                    p_status_win_hed_30_02_lt    469 194
 *                    p_status_win_dat_30_02_rt    821 194
 *
 * Les PAS et les ECARTS viennent du code de 2007, lus un par un :
 *   menu de la maison   +30 par ligne       (DAT_82011814)
 *   lignes du statut    +32 par ligne       (DAT_820035F0)
 *   colonnes du statut  -72 / +72 de l'ancre (DAT_82084CB4)
 *   lignes d'un lieu    x = 640, y = ancre + 43 / +73 / +16
 *                       (DAT_82015B9C, DAT_8208E5AC, DAT_82085A50,
 *                        DAT_82003608)
 *
 * LES NEUF LIEUX PORTENT LEUR NOM. Les identifiants 528 a 535 sont, DANS
 * L'ORDRE, « SEGA WORLD NORTH », « SEGA WORLD SOUTH », « SEGA WORLD
 * ROUTE 101 », « CLUB SEGA DOWNTOWN », « CLUB SEGA BAY AREA », « SEGA ARENA
 * COAST », « SEGA ARENA EAST », « EVENT SQUARE » -- exactement l'ordre de
 * `g_quest_zooms` / `g_quest_icones`, etabli separement a l'ecran le
 * 2026-09-12. Deux mesures independantes qui tombent juste : l'ordre des
 * lieux est le bon. Le neuvieme, la maison, n'a pas de nom de lieu : il a
 * son MENU.
 *
 * LA COULEUR DES TITRES. La Xbox pose 0xFFBFF560 -- en ARGB gros-boutiste,
 * rouge 0xBF, vert 0xF5, bleu 0x60, un vert-jaune. Final Showdown range la
 * couleur octet par octet dans le sommet (`0x18019B4A0`), rouge en premier :
 * le meme vert-jaune s'y ecrit 0xFF60F5BF.
 */
#define QUEST_COUL_TEXTE  0xFFFFFFFFu    /* le blanc du corps */
#define QUEST_COUL_TITRE  0xFF60F5BFu    /* le vert-jaune des titres */
#define QUEST_COUL_GRISE  0xFF7F7F7Fu    /* une ligne indisponible */

/* L'alignement, donne par le suffixe du nom de l'ancre. Ce sont les bits que
 * `0x18019ADB0` lit : 2 = cale a droite, 8 = centre en x, 0x20 = centre en y.
 * 0x800 (retour a la ligne dans la boite) est ajoute partout, comme le fait
 * le dessin de fenetre de FS (`0x1801BC580`). */
#define QUEST_AL_LT  0x000               /* _lt : gauche-haut */
#define QUEST_AL_RT  0x002               /* _rt : droite-haut */
#define QUEST_AL_CT  0x008               /* _ct : centre-haut */
#define QUEST_AL_C   0x028               /* _c  : centre-centre */

/* Le nom de chaque lieu, dans l'ordre de `g_quest_zooms`. -1 = la maison,
 * qui n'a pas de nom de lieu mais un menu. */
static const int g_quest_noms_lieu[9] = {
    528, 529, 530, 531, 532, 533, 534, 535, -1
};
/* Le menu de la maison : six lignes (0x219, 0x21A, 0x21C..0x21F chez la
 * Xbox). 0x21B est saute -- il ne figure pas dans le tableau de 2007. */
static const int g_quest_menu_maison[6] = { 537, 538, 540, 541, 542, 543 };

#define QUEST_COUL_OMBRE  0xFF000000u    /* le noir opaque du contour */
#define QUEST_OMBRE       2.0f           /* deux pixels, en x et en y */

static void quest_ecrire_ancre(float x, float y, float taille, int alignement,
                               unsigned couleur, const char *texte)
{
    if (!texte || !*texte) return;
    /* L'OMBRE D'ABORD. « texte illisible » (2026-09-30) : nos libelles se
     * posent sur la carte du Quest, qui est claire et bariolee. Le jeu de
     * 2007 ne connait pas ce probleme -- son texte est toujours dans une
     * fenetre opaque. Tant que nous n'en posons pas, une copie noire decalee
     * de deux pixels detache le texte de n'importe quel fond, et elle ne
     * coute qu'une commande 2D de plus. */
    quest_ecrire_boite(x + QUEST_OMBRE, y + QUEST_OMBRE, 900.0f, 64.0f,
                       taille, QUEST_COUL_OMBRE,
                       QUEST_DRAPEAUX | alignement, 0, texte);
    quest_ecrire_boite(x, y, 900.0f, 64.0f, taille, couleur,
                       QUEST_DRAPEAUX | alignement, 0, texte);
}

/* LE STATUT : SEPT LIGNES, INTITULE A GAUCHE, VALEUR A DROITE
 *
 * Transcrit de `FUN_8230E6xx` (Xbox 360). Les deux ancres donnent les deux
 * colonnes, et le code de 2007 les ECARTE de 72 pixels chacune
 * (`DAT_82084CB4`) : l'intitule part a 469-72 = 397, la valeur a 821+72 =
 * 893, alignee a droite. Le pas est de 32 (`DAT_820035F0`).
 *
 * Les quatre premieres lignes sont des POURCENTAGES : le jeu prend le
 * flottant du profil, l'arrondit au dixieme (x10, troncature, /10) et le
 * compose avec « %.1f » puis le libelle 401, qui vaut « % ».
 *
 * LES DEUX DERNIERES LIGNES BASCULENT. Le code de 2007 divise un compteur
 * d'images par 180 et en prend le bit 0 -- trois secondes par page a 60
 * images par seconde. Le diviseur n'est pas ecrit en clair dans le binaire :
 * c'est la multiplication magique `0x6C16C16D` suivie de `>> 7`, et 180 est
 * la valeur RETROUVEE en la faisant tourner. Page A : « Total number of
 * matches » et « Total playing time ». Page B : « Number of matches » et
 * « Completion time », en jaune.
 *
 * LES VALEURS SONT A ZERO, ET C'EST EXACT. Elles viennent du profil Quest du
 * joueur, qui n'existe pas encore de notre cote : un Quest neuf affiche bien
 * des zeros. On n'invente rien -- on montre l'etat initial.
 */
#define QUEST_STATUT_X_GAUCHE  397.0f    /* 469 - 72 */
#define QUEST_STATUT_X_DROITE  893.0f    /* 821 + 72 */
#define QUEST_STATUT_Y         194.0f
#define QUEST_STATUT_PAS       32.0f
#define QUEST_STATUT_TAILLE    30.0f     /* le « 30 » du nom de l'ancre */
#define QUEST_BASCULE          180       /* images par page */
#define QUEST_COUL_JAUNE       0xFF00FFFFu

static unsigned g_quest_images;          /* pour la bascule des deux pages */

/* « %s » avec le libelle du moteur en suffixe, sans jamais deborder. */
static void quest_ligne_statut(int rang, int id_intitule, const char *valeur)
{
    float y = QUEST_STATUT_Y + QUEST_STATUT_PAS * rang;
    quest_ecrire_ancre(QUEST_STATUT_X_GAUCHE, y, QUEST_STATUT_TAILLE,
                       QUEST_AL_LT, QUEST_COUL_TEXTE, quest_texte(id_intitule));
    quest_ecrire_ancre(QUEST_STATUT_X_DROITE, y, QUEST_STATUT_TAILLE,
                       QUEST_AL_RT, QUEST_COUL_TEXTE, valeur);
}

static void quest_fenetre_statut(void)
{
    char v[64];
    const char *pourcent = quest_texte(401);      /* « % »        */
    const char *victoires = quest_texte(402);     /* « %d Wins »  */
    const char *entier = quest_texte(403);        /* « %d »       */
    const char *duree = quest_texte(404);         /* « %d:%d:%d » */
    int page = (g_quest_images / QUEST_BASCULE) & 1;
    unsigned s = quest_lire32(QUEST_PO_SECONDES);
    int i;

    quest_ecrire_ancre(640.0f, 135.0f, QUEST_STATUT_TAILLE, QUEST_AL_CT,
                       QUEST_COUL_TITRE, quest_texte(544));
    /* LES QUATRE POURCENTAGES. Celui des rivaux est REEL : le jeu de 2007
     * compte ceux qui sont a la fois rencontres ET battus, et multiplie par
     * 0,001 puis par 100 (`_DAT_82006C1C`, `DAT_82003EDC`) -- soit le compte
     * divise par dix. Les trois autres demandent les objets, les emblemes et
     * la note d'ensemble, qui n'existent pas encore : ils restent a zero, ce
     * qui est l'etat exact d'un Quest neuf. */
    for (i = 0; i < 4; i++) {
        double valeur = (i == 0)
            ? quest_profil_compte_battus() * 0.001 * 100.0 : 0.0;
        _snprintf(v, sizeof v, "%.1f%s", valeur, pourcent ? pourcent : "%");
        quest_ligne_statut(i, 545 + i, v);
    }
    _snprintf(v, sizeof v, victoires ? victoires : "%d Wins",
              quest_lire32(QUEST_PO_SERIE));
    quest_ligne_statut(4, 549, v);
    /* les deux dernieres, qui basculent toutes les trois secondes */
    _snprintf(v, sizeof v, entier ? entier : "%d",
              quest_lire32(QUEST_PO_COMBATS));
    quest_ligne_statut(5, page ? 552 : 550, v);
    _snprintf(v, sizeof v, duree ? duree : "%d:%d:%d",
              s / 3600, (s / 60) % 60, s % 60);
    quest_ligne_statut(6, page ? 553 : 551, v);
}

/* LA LISTE DES JOUEURS : NEUF LIGNES, CELLES DU LIEU
 *
 * Transcrit de `FUN_82311078`. Neuf lignes par page (`min(nb, 9)`), pas de
 * 36 (`DAT_82010304`), taille 36 -- le « 36 » du nom de l'ancre
 * `p_plylist_win_name_36_03_lt` est bien la taille de police.
 *
 * Les rivaux sont ceux du LIEU : `FUN_8230E018` garde ceux dont
 * `npc_tbl[n] + 0x88` tombe dans le masque, et cela ne demande aucun profil.
 * Le profil, lui, commande l'AFFICHAGE de chacun : un rival pas encore
 * rencontre sort en « ？？？？？ », un rival battu porte une etoile jaune a
 * trente pixels a sa gauche (`DAT_82011814`).
 *
 * LE FEUILLETAGE. En 2007 c'est HAUT/BAS qui font defiler la liste et
 * GAUCHE/DROITE qui changent de lieu. Chez nous HAUT/BAS font tourner les
 * trois fenetres : quand la liste est ouverte, ce sont donc GAUCHE et DROITE
 * qui tournent les pages -- elles ne servaient a rien d'autre une fois un
 * lieu ouvert.
 */
#define QUEST_LISTE_X      389.0f        /* p_plylist_win_name_36_03_lt */
#define QUEST_LISTE_Y      216.0f
#define QUEST_LISTE_PAS    36.0f         /* DAT_82010304 */
#define QUEST_LISTE_TAILLE 36.0f
#define QUEST_LISTE_LIGNES 9
#define QUEST_ETOILE_DX    30.0f         /* DAT_82011814 */
#define QUEST_RATIO_X      1022.0f       /* p_plylist_player_ratio_rt */
#define QUEST_RATIO_Y      581.0f

static int g_quest_page;                 /* la page de la liste */
static int g_quest_curseur;              /* la ligne choisie, 0..total-1 */
static int g_quest_menu;                 /* la ligne du menu du lieu / de la maison */

/* Combien de rivaux le lieu compte. */
static int quest_lieu_compte(int lieu)
{
    int n, c = 0;
    if (lieu < 0 || !quest_rivaux()) return 0;
    for (n = 0; n < QUEST_RIVAUX_NOMBRE; n++)
        if (quest_rival_lieu(n) == lieu) c++;
    return c;
}

static void quest_fenetre_joueurs(void)
{
    char v[128];
    int i, lieu = quest_lieu_courant();
    int total = quest_lieu_compte(lieu);
    const char *pourcent = quest_texte(401);

    quest_ecrire_ancre(640.0f, 95.0f, QUEST_STATUT_TAILLE, QUEST_AL_CT,
                       QUEST_COUL_TITRE, quest_texte(558));   /* RIVAL LIST */
    quest_ecrire_ancre(640.0f, 141.0f, QUEST_STATUT_TAILLE, QUEST_AL_CT,
                       QUEST_COUL_TEXTE,
                       quest_texte(g_quest_noms_lieu[g_quest_salle]));
    for (i = 0; i < QUEST_LISTE_LIGNES; i++) {
        int n = quest_rival_du_lieu(lieu,
                                    g_quest_page * QUEST_LISTE_LIGNES + i);
        float y = QUEST_LISTE_Y + QUEST_LISTE_PAS * i;
        const char *nom;
        if (n < 0) break;
        nom = quest_profil_bit(QUEST_PO_RENCONTRE, n)
            ? quest_rival_texte(n, QUEST_RIVAL_NOM) : QUEST_INCONNU;
        if (quest_profil_bit(QUEST_PO_BATTU, n))
            quest_ecrire_ancre(QUEST_LISTE_X - QUEST_ETOILE_DX, y,
                               QUEST_LISTE_TAILLE, QUEST_AL_LT,
                               QUEST_COUL_JAUNE, QUEST_ETOILE);
        /* LE CURSEUR : la COULEUR, et rien d'autre. En 2007 c'est une
         * composition AET posee sur la ligne (`FUN_8230A1C0`). J'avais
         * ajoute un chevron a gauche ; Frederic, a l'ecran le 2026-09-27 :
         * « le curseur est visible sur rival list [...] enleve le chevron,
         * ne conserve que la couleur ». */
        quest_ecrire_ancre(QUEST_LISTE_X, y, QUEST_LISTE_TAILLE,
                           QUEST_AL_LT,
                           n == quest_rival_du_lieu(lieu, g_quest_curseur)
                               ? QUEST_COUL_TITRE : QUEST_COUL_TEXTE, nom);
        /* SON GRADE, a droite de la ligne : `npc_tbl + 0x7C`, le meme champ
         * que le menu d une salle affiche. Tant que le picto n est pas
         * dessine, il est en toutes lettres. */
        if (quest_profil_bit(QUEST_PO_RENCONTRE, n)) {
            char g[32];
            int gr = quest_rival_grade(n);
            if (gr >= 0)
                quest_ecrire_ancre(QUEST_LISTE_X + 480.0f, y,
                                   QUEST_LISTE_TAILLE, QUEST_AL_RT,
                                   n == quest_rival_du_lieu(lieu, g_quest_curseur)
                                       ? QUEST_COUL_TITRE : QUEST_COUL_TEXTE,
                                   quest_grade_texte(gr, g, sizeof g));
        }
    }
    /* LE BAS DE LA FENETRE. « Arcade completion rating » (560) est un
     * compteur d'arcade que nous n'avons pas. On met a la place la seule
     * mesure vraie dont on dispose, et c'est celle qui dit si le profil
     * vit : la page courante, et combien des rivaux de CE lieu sont
     * rencontres. Elle monte de cent trente d'un coup quand on entre dans
     * un lieu neuf, et elle est retenue d'une partie a l'autre. */
    {
        int pages = (total + QUEST_LISTE_LIGNES - 1) / QUEST_LISTE_LIGNES;
        int connus = 0, n;
        for (n = 0; n < QUEST_RIVAUX_NOMBRE; n++)
            if (quest_rival_lieu(n) == lieu
                    && quest_profil_bit(QUEST_PO_RENCONTRE, n))
                connus++;
        _snprintf(v, sizeof v, "%d / %d      %d / %d  (%.1f%s)",
                  g_quest_curseur + 1, total, connus, total,
                  total ? connus * 100.0 / total : 0.0,
                  pourcent ? pourcent : "%");
        (void)pages;
    }
    quest_ecrire_ancre(QUEST_RATIO_X, QUEST_RATIO_Y, QUEST_STATUT_TAILLE,
                       QUEST_AL_RT, QUEST_COUL_TEXTE, v);
}

/* ------------------------------------------------------------------------
 * LE COMBAT DU QUEST
 *
 * Ecrit le 2026-09-29, APRES avoir lu le combat de 2007 en entier -- Frederic
 * l'avait demande en ces termes : « je ne lance plus rien de base sur une
 * supposition ». Tout ce qui suit vient de `analysis/mode_quest.md` §9.25 a
 * §9.27, et chaque appel est un appel que le moteur se fait a lui-meme.
 *
 * CE QUI NE MARCHAIT PAS, ET POURQUOI. Demander le sous-etat 18
 * (`MODE_SELECTOR`) suffit a preparer UN combat -- mais celui de l'ARCADE :
 * `0x1800B8540` prend le personnage de l'adversaire dans l'echelle d'arcade
 * (`0x1800ACD40`, une table 3 x 8 de `game_score.txt`), et ses reglages dans
 * un bloc que personne n'avait ecrit -- le journal l'a mesure, « mode de jeu
 * 9 », c'est-a-dire de la memoire jamais initialisee. D'ou « c'est le mode
 * arcade qui se lance ».
 *
 * CE QUE FAIT LE QUEST DE 2007. Il ne choisit pas un mode : il COMPOSE le
 * combat dans une structure de 0x50 octets et la remet au moteur par
 * `FUN_821DCD98` -- dont le jumeau dans Final Showdown est
 * `0x1800B34D0(session+0x4E0, descripteur)`. Les vingt mots du descripteur
 * sont cartographies (§9.25).
 *
 * NOTRE CHEMIN, et il est celui du moteur :
 *
 *   1. le joueur 0 entre en piste            `0x1800B2FA0`
 *   2. les deux personnages dans la session  `session + 0x28 + j*4`
 *   3. mode de partie 0, tirage 0            `0x1800B28B0`, `0x1800B32E0`
 *   4. le dossier du joueur                  `0x1800490E0`, `0x180049030`,
 *                                            `0x180049220` -- la queue de
 *                                            MODE_SELECTOR, dans son ordre
 *   5. LA PREPARATION DU MOTEUR              `0x1800B8540(session)`
 *   6. NOTRE descripteur par-dessus          `0x1800B34D0`, puis les deux
 *                                            fiches `0x1800B3340`
 *   7. la force du CPU du rival              `0x18010ED40`
 *   8. en avant                              mode 2 GAME, sous-etat 19 VS
 *
 * CE QUE LE DESCRIPTEUR PORTE, ET D'OU CHAQUE VALEUR VIENT :
 *
 *   temps   45 s -> 2 700 trames   (2007 : `iStack_bb8 = 0xA8C`)
 *   sante   201 pour chacun        (2007 : `uStack_bb4 = 0xC9`)
 *   rounds  3                      (2007 : `uStack_bb0 = 3`)
 *   decor   celui du rival         (`0x1800AF400`, la politique de FS ; 2007
 *                                   tire au hasard parmi une vingtaine)
 *   drapeaux premier ET dernier    -- un combat du Quest n'a pas de serie
 *
 * LA FORCE DU CPU. `npc_tbl + 0x10` est un flottant de 0 a 1 : la force
 * propre du rival. 2007 y ajoute la difficulte et la serie de victoires, borne
 * a [0, 1], puis multiplie par 30. Final Showdown compte dans LA MEME unite --
 * sa table de `game_score.txt` va de 2 a 31 -- et la range en `[fiche +
 * 0x1CF8]` par `0x18010ED40`.
 *
 * CE QUI N'Y EST PAS ENCORE, ET IL FAUT LE DIRE : le COSTUME du rival. Ses
 * deux listes de 24 objets sont lues (`npc_tbl + 0x18` et `+0x48`) et leurs
 * numeros sont traduits (`analysis/quest/objets_2007_vers_fs.json`), mais la
 * disposition du dossier de Final Showdown n'est pas cartographiee : on sait
 * seulement ou vit le champ des objets possedes (`dossier + 0x160`, un
 * `bitset<2000>`). Le rival se bat donc dans sa tenue par defaut.
 *
 * LA VOIE PAR LE SELECTEUR reste sous la touche T. Elle est validee a l'ecran
 * depuis le 2026-09-27 ; on ne defait pas ce qui marche.
 */
#define QUEST_RVA_SESSION_LIRE  0x0B23A0
#define QUEST_RVA_SESSION_CREER 0x0B3620
#define QUEST_RVA_JOUEUR_ENTRE  0x0B2FA0
#define QUEST_RVA_MODEJEU_LIRE  0x19C090   /* rend [0x180751010] */
#define QUEST_RVA_REGLAGES      0x0B23B0   /* session + 0x50 */
#define QUEST_RVA_SOUSOBJET     0x0B24B0   /* session + 0x4E0 */
#define QUEST_RVA_POSER_PARTIE  0x0B28B0   /* [session+0x58] : mode de partie */
#define QUEST_RVA_POSER_TIRAGE  0x0B32E0   /* [session+0x5C] */
#define QUEST_RVA_PREPARER      0x0B8540   /* LA preparation du combat */
#define QUEST_RVA_DESCRIPTEUR   0x0B34D0   /* le descripteur -> sous-objet */
#define QUEST_RVA_FICHE         0x0B3340   /* le dossier -> la fiche */
#define QUEST_RVA_FORCE_CPU     0x10ED40   /* [fiche + 0x1CF8] */
#define QUEST_RVA_DECOR_PERSO   0x0AF400   /* le decor « maison » d'un perso */
#define QUEST_RVA_DOSSIERS      0x70FB10   /* le tableau des dossiers */
#define QUEST_RVA_DOSSIER_A     0x0490E0
#define QUEST_RVA_DOSSIER_B     0x049030
#define QUEST_RVA_DOSSIER_C     0x049220
#define QUEST_RVA_VOEU_MODE     0x0DA9A0
#define QUEST_RVA_VOEU_SOUS     0x0DA9C0
#define QUEST_MODE_GAME         2
#define QUEST_SOUS_VS           19       /* le COMBAT lui-meme */
#define QUEST_SOUS_PREPA        18       /* MODE_SELECTOR */
#define QUEST_SOUS_SELECTOR     17       /* le choix des combattants */
#define QUEST_MODE_MENU         4
/* LE CHAMP DU COMBATTANT, trouve le 2026-09-27.
 *
 * `FUN_1800B2F80(session, joueur, p3, p4, p5, p6)` ecrit quatre mots par
 * joueur -- +0x28, +0x30, +0x38, +0x40, chacun indexe par le numero de
 * joueur sur quatre octets. `p3` est L'INDICE DU PERSONNAGE. */
#define QUEST_SESSION_PERSO     0x28
#define QUEST_SESSION_P30       0x30
#define QUEST_SESSION_P38       0x38
#define QUEST_SESSION_P40       0x40
#define QUEST_SESSION_ENPISTE   0x0C     /* un octet par joueur */
#define QUEST_SESSION_COURANT   0x08     /* le joueur courant */
#define QUEST_PERSOS            21       /* 0..20 ; 21 = AUCUN. Dural EST 20 */
#define QUEST_PERSO_DEFAUT      0        /* Akira, si la session n'a rien */
#define QUEST_DOSSIER_PAS       0x5A0
#define QUEST_RIVAL_FORCE       0x10     /* flottant GROS-BOUTISTE */
/* les valeurs du combat, lues dans le Quest de 2007 */
#define QUEST_TEMPS_TRAMES      (45 * 60)
#define QUEST_SANTE             201
#define QUEST_ROUNDS            3
#define QUEST_FORCE_ECHELLE     30.0f

typedef void *(*quest_f_session_lire)(void);
typedef int (*quest_f_session_creer)(int joueurs);   /* rend un BOOLEEN */
typedef int (*quest_f_joueur_entre)(void *session, unsigned joueur,
                                    int p3, unsigned p4);
typedef void *(*quest_f_sousobjet)(void *session);
typedef void (*quest_f_poser)(void *objet, int v);
typedef void (*quest_f_preparer)(void *session);
typedef void (*quest_f_descripteur)(void *sousobjet, int *desc);
typedef void (*quest_f_fiche)(void *sousobjet, int joueur);
typedef void (*quest_f_force)(int joueur, unsigned short force, int perso);
typedef int (*quest_f_decor)(unsigned perso);
typedef void (*quest_f_dossier1)(int joueur);
typedef void (*quest_f_dossier2)(int joueur, unsigned char v);
typedef int (*quest_f_modejeu)(void);
typedef void (*quest_f_voeu)(int v);

/* L'ETAT DU VA-ET-VIENT.
 *
 * PIEGE PAYE D'UN ESSAI : ce drapeau s'est d'abord appele `g_quest_retour`
 * -- et `g_quest_retour` EXISTAIT DEJA, c'est le code de retour du dessin de
 * texte. Deux `static int` du meme nom dans un fichier sont une definition
 * PROVISOIRE : le C n'en fait qu'une variable, et ni `-Wall` ni `-Wextra` ne
 * disent rien. Chaque texte dessine y posait 5, et la machine de retour y
 * lisait « reviens du combat » : 2 913 fois dans un seul journal.
 *
 * 0 = on ne bouge pas
 * 1 = on vient de demander le combat, on attend que le mode QUITTE le notre
 * 2 = on est dans le combat, on attend qu'il REVIENNE au menu
 * 3 = le menu est la, on redemande le Quest */
static int g_quest_combat;               /* 0..3, voir ci-dessus */
static unsigned g_quest_combat_ms;       /* pour renoncer si rien ne part */
static int g_quest_rival;                /* le rival qu'on est alle voir */
static int g_quest_voie;                 /* 0 = direct, 1 = par le selecteur */
static int g_quest_perso_joueur = QUEST_PERSO_DEFAUT;   /* son personnage */
static int g_quest_vu_vs;                /* le combat a bien eu lieu */
/* LES TROIS ECRANS AJOUTES LE 2026-09-30 :
 *   1 la RENCONTRE -- le rival, son grade et ses deux repliques, avant le
 *     combat. Ses textes sont dans `npc_tbl + 0x04` et `+0x08`, lus depuis
 *     le 27/09 et jamais montres.
 *   2 les REGLAGES du Quest (`TaskQuestOption`) : la difficulte, qui donne
 *     +0,2 ou +0,4 a la force du CPU.
 *   3 les EMBLEMES (`TaskQuestEmblemList`) : les treize familles, libelles
 *     571 a 584. */
#define QUEST_ECRAN_AUCUN     0
#define QUEST_ECRAN_RENCONTRE 1
#define QUEST_ECRAN_REGLAGES  2
#define QUEST_ECRAN_EMBLEMES  3
static int g_quest_ecran;                /* voir ci-dessus */
static int g_quest_ecran_rival = -1;     /* le rival qu'on va affronter */
#define QUEST_EMBLEMES_FAMILLES 13
#define QUEST_ECRAN_BOUTIQUE  4
#define QUEST_ECRAN_TOURNOI   5
/* LE TOURNOI -- le sous-etat 0x55 de 2007 et ses neuf classes.
 *
 * Ce qui est porte ici est la BOUCLE, pas encore le tableau dessine : on tire
 * huit adversaires parmi les rivaux du dome, on les affronte l'un apres
 * l'autre, et une defaite arrete tout. Les libelles sont ceux du jeu --
 * 620 « Participants: %d », 621 « Rounds: %d », 624 les lots, 667-669 les
 * tours, 678-680 demi-finale, finale, troisieme place, 712 « Champion ».
 *
 * LE LOT est une regle a nous, comme le gain d'un combat : 2007 le tire de
 * ses donnees de tournoi, que je n'ai pas lues. Ici, 2 000 G par tour gagne
 * et 10 000 G au titre. C'est ecrit pour etre remplace.
 */
#define QUEST_TOURNOI_TOURS  3
#define QUEST_TOURNOI_LOT    2000
#define QUEST_TOURNOI_TITRE  10000
static int g_quest_tournoi;              /* 0 = aucun ; 1..3 = le tour */
static int g_quest_tournoi_rivaux[QUEST_TOURNOI_TOURS];
/* LA BOUTIQUE. `tools/objets_quest.py` pose `quest_objets.bin` a cote du
 * jeu : par personnage, la liste de ses objets avec leur numero DANS Final
 * Showdown, leur PRIX (la colonne « Point » du CSV du jeu, pas une invention)
 * et leur nom anglais de 2007.
 *
 *   "QOBJ" u32 version u32 nb_persos, puis un decalage par personnage ;
 *   table : u32 nombre, puis { u16 id_fs, u16 prix, u32 decalage du nom }. */
#define QUEST_OBJETS_FICHIER "quest_objets.bin"
#define QUEST_BOUTIQUE_LIGNES 10
static unsigned char *g_quest_objets;
static long g_quest_objets_taille;
static int g_quest_objets_vu;
static int g_quest_boutique_curseur;
static int g_quest_boutique_page;

/* LA FORCE PROPRE DU RIVAL : un flottant gros-boutiste en `npc_tbl + 0x10`. */
static float quest_rival_force(int n)
{
    unsigned char *t = quest_rivaux();
    union { unsigned u; float f; } c;
    if (!t || n < 0 || n >= QUEST_RIVAUX_NOMBRE) return 0.0f;
    c.u = quest_be32(t + (long)n * QUEST_RIVAUX_PAS + QUEST_RIVAL_FORCE);
    return c.f;
}

/* La force du CPU, formule de 2007 (§9.26). Les constantes sont lues dans
 * l'image de la Xbox, pas choisies. La difficulte du Quest n'existe pas encore
 * chez nous (elle vaut 0, donc pas de bonus) ; la serie est celle du profil. */
static int quest_force_cpu(int rival)
{
    float f = quest_rival_force(rival);
    unsigned serie, diff;
    quest_profil_charger();
    serie = quest_lire32(QUEST_PO_SERIE_EN_COURS);
    diff = quest_lire32(QUEST_PO_DIFFICULTE);
    /* la difficulte du Quest, exactement comme 2007 : +0,2 au cran 1,
     * +0,4 au cran 2 (`0x82022658`, `0x820035B0`) */
    if (diff == 1) f += 0.20f;
    else if (diff == 2) f += 0.40f;
    if (serie >= 20) f += 0.10f;
    else if (serie >= 10) f += 0.05f;
    else if (serie >= 2) f += 0.01f;
    if (f < 0.0f) f = 0.0f;
    if (f > 1.0f) f = 1.0f;
    return (int)(f * QUEST_FORCE_ECHELLE);
}

/* LE COMBAT, compose comme le Quest de 2007 le compose. */
static void quest_combat_direct(unsigned char *sess, int rival, int perso)
{
    unsigned char *b = g_quest_base;
    quest_f_sousobjet reglages = (quest_f_sousobjet)(b + QUEST_RVA_REGLAGES);
    quest_f_sousobjet sousobj = (quest_f_sousobjet)(b + QUEST_RVA_SOUSOBJET);
    quest_f_poser partie = (quest_f_poser)(b + QUEST_RVA_POSER_PARTIE);
    quest_f_poser tirage = (quest_f_poser)(b + QUEST_RVA_POSER_TIRAGE);
    quest_f_preparer preparer = (quest_f_preparer)(b + QUEST_RVA_PREPARER);
    quest_f_descripteur poser_desc =
        (quest_f_descripteur)(b + QUEST_RVA_DESCRIPTEUR);
    quest_f_fiche fiche = (quest_f_fiche)(b + QUEST_RVA_FICHE);
    quest_f_force force = (quest_f_force)(b + QUEST_RVA_FORCE_CPU);
    quest_f_decor decor_de = (quest_f_decor)(b + QUEST_RVA_DECOR_PERSO);
    quest_f_dossier1 dos_a = (quest_f_dossier1)(b + QUEST_RVA_DOSSIER_A);
    quest_f_dossier2 dos_b = (quest_f_dossier2)(b + QUEST_RVA_DOSSIER_B);
    quest_f_dossier1 dos_c = (quest_f_dossier1)(b + QUEST_RVA_DOSSIER_C);
    void *reg = reglages((void *)sess);
    void *so;
    int desc[20];
    int joueur = *(int *)(sess + QUEST_SESSION_COURANT);
    int autre = joueur ? 0 : 1;
    int d, f_cpu, k;
    char m[200];
    unsigned char *base_dos = *(unsigned char **)(b + QUEST_RVA_DOSSIERS);

    if (joueur < 0 || joueur > 1) { joueur = 0; autre = 1; }

    /* 3. le mode de partie et le tirage, comme la queue de MODE_SELECTOR */
    partie(reg, 0);
    tirage(reg, 0);

    /* 4. le dossier du joueur, dans l'ordre de cette meme queue */
    if (base_dos) {
        unsigned char *dossier = base_dos + 0x18
                               + (long)joueur * QUEST_DOSSIER_PAS;
        dos_a(joueur);
        dos_b(joueur, dossier[0x117]);
        if (dossier[1]) dos_c(joueur);
    }

    /* 5. LA PREPARATION DU MOTEUR : fiches, sons, annonce, tout son travail */
    preparer((void *)sess);
    so = sousobj((void *)sess);
    if (!so) {
        quest_dire("pas de sous-objet de combat : on renonce", 0);
        return;
    }

    /* 6. NOTRE DESCRIPTEUR. Les vingt mots de §9.25, dans l'ordre. */
    for (k = 0; k < 20; k++) desc[k] = 0;
    desc[0] = 0;                         /* un combattant installe par VS */
    desc[1] = 0;                         /* mode de partie */
    desc[3 + joueur] = g_quest_perso_joueur;
    desc[3 + autre] = perso;
    desc[5 + joueur] = *(int *)(sess + QUEST_SESSION_P30 + joueur * 4);
    desc[5 + autre] = *(int *)(sess + QUEST_SESSION_P30 + autre * 4);
    desc[7 + joueur] = *(int *)(sess + QUEST_SESSION_P38 + joueur * 4);
    desc[7 + autre] = *(int *)(sess + QUEST_SESSION_P38 + autre * 4);
    desc[9 + joueur] = *(int *)(sess + QUEST_SESSION_P40 + joueur * 4);
    desc[9 + autre] = *(int *)(sess + QUEST_SESSION_P40 + autre * 4);
    desc[11 + joueur] = 0;               /* lui, c'est le joueur */
    desc[11 + autre] = 1;                /* l'autre, c'est la machine */
    desc[13] = QUEST_TEMPS_TRAMES;
    desc[14] = QUEST_SANTE | (QUEST_SANTE << 16);   /* deux short : 1P, 2P */
    desc[15] = QUEST_ROUNDS;
    desc[16] = joueur;
    d = decor_de((unsigned)perso);       /* le decor « maison » du rival */
    if (d < 0) d = *(int *)((unsigned char *)so + 0x4C);   /* celui du moteur */
    desc[17] = d;
    desc[18] = *(int *)(sess + 0x50 + 0x3F4);
    desc[19] = 0x00010101;               /* premier, mode != 1, dernier */
    poser_desc(so, desc);
    fiche(so, 0);
    fiche(so, 1);

    /* 7. la force du CPU du rival */
    f_cpu = quest_force_cpu(rival);
    force(autre, (unsigned short)f_cpu, perso);

    _snprintf(m, sizeof m, "combat compose : perso %d contre %d ; decor %d ;"
              " force %d ; temps %d ; rounds %d ; joueur",
              desc[3 + joueur], desc[3 + autre], d, f_cpu,
              QUEST_TEMPS_TRAMES / 60, QUEST_ROUNDS);
    quest_dire(m, (long long)joueur);
}

static void quest_partir_au_combat(int rival)
{
    unsigned char *b = g_quest_base;
    quest_f_session_lire lire;
    quest_f_session_creer creer;
    quest_f_joueur_entre entrer;
    quest_f_voeu mode, sous;
    unsigned char *sess;
    int perso, *p;
    char m[220];
    const char *nom;
    if (!b) return;
    lire = (quest_f_session_lire)(b + QUEST_RVA_SESSION_LIRE);
    creer = (quest_f_session_creer)(b + QUEST_RVA_SESSION_CREER);
    entrer = (quest_f_joueur_entre)(b + QUEST_RVA_JOUEUR_ENTRE);
    mode = (quest_f_voeu)(b + QUEST_RVA_VOEU_MODE);
    sous = (quest_f_voeu)(b + QUEST_RVA_VOEU_SOUS);
    perso = quest_rival_perso(rival);
    nom = quest_rival_texte(rival, QUEST_RIVAL_NOM);
    /* LA SESSION. `0x1800B3620` rend un BOOLEEN, pas l'objet -- la lire comme
     * un pointeur etait l'erreur du 2026-09-27. On relit donc apres. */
    sess = (unsigned char *)lire();
    if (!sess) {
        creer(0);
        sess = (unsigned char *)lire();
    }
    if (!sess) {
        quest_dire("pas de session : le combat ne part pas", 0);
        return;
    }
    p = (int *)(sess + QUEST_SESSION_PERSO);
    /* on retient SON personnage avant l'entree en piste, qui l'efface */
    if (p[0] >= 0 && p[0] < QUEST_PERSOS - 1) g_quest_perso_joueur = p[0];
    /* LE JOUEUR 0 ENTRE EN PISTE. C'est le geste du selecteur quand un joueur
     * valide : `0x1800B2FA0(session, 0, 1, 0)`. Il pose `[session+0x0C]`,
     * remet le personnage a 0x15 et trois `-1`, et inscrit le joueur dans les
     * tables. Le joueur 1 reste DEHORS : c'est un adversaire machine. */
    if (!sess[QUEST_SESSION_ENPISTE]) {
        entrer((void *)sess, 0, 1, 0);
        quest_dire("joueur 0 en piste ; drapeau",
                   (long long)sess[QUEST_SESSION_ENPISTE]);
    }
    /* LES DEUX PERSONNAGES, POSES APRES l'entree en piste. */
    p[0] = g_quest_perso_joueur;
    if (perso >= 0 && perso < QUEST_PERSOS - 1) p[1] = perso;
    _snprintf(m, sizeof m,
              "combat %s : joueur perso %d contre \"%s\" perso %d ; rival",
              g_quest_voie == 0 ? "compose (VS direct)" : "par le selecteur",
              p[0], nom ? nom : "?", p[1]);
    quest_dire(m, (long long)rival);
    quest_musique(0);          /* le combat a la sienne */
    if (g_quest_voie == 0 && perso >= 0 && perso < QUEST_PERSOS - 1) {
        quest_combat_direct(sess, rival, perso);
        mode(QUEST_MODE_GAME);
        sous(QUEST_SOUS_VS);
    } else {
        mode(QUEST_MODE_GAME);
        sous(QUEST_SOUS_SELECTOR);
    }
    g_quest_combat = 1;
    g_quest_combat_ms = GetTickCount();
    g_quest_rival = rival;
    quest_profil_charger();
    quest_ecrire32(QUEST_PO_COMBATS, quest_lire32(QUEST_PO_COMBATS) + 1);
    g_quest_profil_sale = 1;
    quest_profil_ecrire();
}

/* ------------------------------------------------------------------------
 * APRES LE COMBAT -- le sous-etat 0x58 de 2007
 *
 * LE VERDICT SE LIT, ET IL EST MESURE : `[session + 0x4E0 + 0x1054]` porte le
 * VAINQUEUR, et l'arbitre de fin de combat de FS (`0x1800DB4B0`) le compare
 * au joueur courant `[session + 8]` -- `FUN_1800B4940` n'est qu'un accesseur
 * d'une ligne. C'est ce que ce portage cherchait depuis le debut.
 *
 * CE QUE 2007 FAIT ENSUITE, dans son rappel `FUN_82320A68` :
 *   - il pose le bit BATTU du rival        (`profil + 0xF4`, `FUN_821D1798`)
 *   - il incremente la serie de victoires  (`DAT_82AD172C`, plafond 999)
 *   - il retient la plus longue            (`profil + 0x04`)
 *   - il reecrit les statistiques du rival (`FUN_8230DB40`)
 *
 * CE QUI EST UNE REGLE A NOUS, ET IL FAUT LE DIRE : le MONTANT gagne et la
 * montee en GRADE. Le code de 2007 les calcule ailleurs que dans les 323
 * fonctions du mode -- je ne les ai pas trouves, et je ne les invente pas en
 * silence. Notre regle, ecrite ici pour etre remplacee le jour ou la vraie
 * sera lue :
 *
 *   argent  = 300 G + 100 G par cran de grade du rival
 *   grade   = un cran tous les DIX rivaux battus, borne a 41
 *
 * BALAYAGE EXHAUSTIF DU 2026-09-30, pour que personne ne recommence.
 * Les 323 fonctions ont ete balayees sur le champ ARGENT. Le porte-monnaie
 * de 2007 est `FUN_82235f28(0x827A99F8, creneau) + 0xEC`, c'est-a-dire
 * `base + creneau * 0x528 + 0x10 + 0xEC` -- une FICHE DE JOUEUR de 0x528
 * octets, PAS le bloc de sauvegarde de `FUN_8230B5B8` (ou `+0xEC` tombe au
 * milieu du champ de mille bits « rencontres », qui va de +0x74 a +0xF4 :
 * les confondre corromprait ces bits).
 *
 * Ce champ n'est ecrit qu'a TROIS endroits dans tout le lot decompile :
 *   1. remis a zero            (quest_x360.c, FUN_8230B5B8 voisin, l. 3232)
 *   2. la CREATION DE DONNEES  (+50 000 G, verses par +500 par trame, ou
 *      +10 000 si `[etat+0x150]`, un son toutes les trois trames ; plafond
 *      999 999) -- c'est ce que nous avons deja porte ;
 *   3. le PAIEMENT D'UN EVENEMENT, `FUN_82317F88`.
 *
 * Il n'y a AUCUN gain d'argent par combat ordinaire. L'argent de 2007 vient
 * des EVENEMENTS, pas des combats -- ce qui rend notre « 300 G + 100 G par
 * cran » non pas faux mais ETRANGER au modele d'origine.
 *
 * Les evenements, pour le jour ou on les portera (FUN_82318B18) :
 *   . quinze evenements, 0..14 ; 0 a 6 d'une famille, 7 a 14 de l'autre
 *     (`DAT_82656B0C`) ;
 *   . chacun porte TROIS recompenses `{type, valeur}` prises dans
 *     `FUN_82315890(evenement)` (table hors du lot decompile) ;
 *   . type 0 = un objet (`FUN_82317950`), type 1 = `FUN_823179E8`,
 *     type 2 = de l'ARGENT ;
 *   . si l'evenement a DEJA ete accompli, la valeur est DIVISEE PAR DEUX
 *     (`iVar6 >> 1`) -- sauf l'evenement 0x0D, dont elle redevient 10 000 ;
 *   . `FUN_82317F88` verse, avec le plafond 999 999.
 * Le « 10 000 G » du cahier des charges est donc CONFIRME, et il appartient
 * a l'evenement 0x0D. Le « 2 000 G » est dans la table de `FUN_82315890`,
 * qui n'est pas decompilee : on ne l'ecrit pas tant qu'on ne l'a pas lue.
 *
 * La montee en GRADE n'apparait nulle part dans les 323 fonctions non plus.
 */
#define QUEST_GAIN_BASE   300
#define QUEST_GAIN_GRADE  100
#define QUEST_BATTUS_PAR_GRADE 10
#define QUEST_SESSION_SOUSOBJ 0x4E0
#define QUEST_SOUSOBJ_VAINQUEUR 0x1054

static void quest_apres_combat(void)
{
    unsigned char *b = g_quest_base;
    quest_f_session_lire lire;
    unsigned char *sess;
    int vainqueur, joueur, gagne, grade_rival, battus, grade;
    unsigned argent, serie;
    char m[200];
    if (!b || g_quest_rival < 0) return;
    lire = (quest_f_session_lire)(b + QUEST_RVA_SESSION_LIRE);
    sess = (unsigned char *)lire();
    if (!sess) return;
    vainqueur = *(int *)(sess + QUEST_SESSION_SOUSOBJ + QUEST_SOUSOBJ_VAINQUEUR);
    joueur = *(int *)(sess + QUEST_SESSION_COURANT);
    gagne = (vainqueur == joueur);
    quest_profil_charger();
    serie = quest_lire32(QUEST_PO_SERIE_EN_COURS);
    argent = quest_lire32(QUEST_PO_ARGENT);
    grade_rival = quest_rival_grade(g_quest_rival);
    if (grade_rival < 0) grade_rival = 0;

    if (gagne) {
        /* le bit BATTU, comme 2007 le pose */
        quest_profil_poser(QUEST_PO_BATTU, g_quest_rival);
        quest_ecrire32(QUEST_PO_VICTOIRES,
                       quest_lire32(QUEST_PO_VICTOIRES) + 1);
        serie = serie + 1;
        if (serie > 999) serie = 999;
        if (serie > quest_lire32(QUEST_PO_SERIE))
            quest_ecrire32(QUEST_PO_SERIE, serie);
        argent += (unsigned)(QUEST_GAIN_BASE
                             + QUEST_GAIN_GRADE * grade_rival);
        if (argent > QUEST_ARGENT_MAX) argent = QUEST_ARGENT_MAX;
        quest_ecrire32(QUEST_PO_ARGENT, argent);
        /* le grade : un cran tous les dix battus */
        battus = quest_profil_compte_battus();
        grade = battus / QUEST_BATTUS_PAR_GRADE;
        if (grade > 41) grade = 41;
        if ((unsigned)grade > quest_lire32(QUEST_PO_GRADE))
            quest_ecrire32(QUEST_PO_GRADE, (unsigned)grade);
    } else {
        quest_ecrire32(QUEST_PO_DEFAITES,
                       quest_lire32(QUEST_PO_DEFAITES) + 1);
        serie = 0;
    }
    quest_ecrire32(QUEST_PO_SERIE_EN_COURS, serie);
    g_quest_profil_sale = 1;
    quest_profil_ecrire();
    quest_tournoi_apres(gagne);
    _snprintf(m, sizeof m,
              "apres le combat : %s (vainqueur %d, joueur %d) ;"
              " serie %u ; argent %u G ; grade %u ; rival",
              gagne ? "GAGNE" : "perdu", vainqueur, joueur, serie,
              quest_lire32(QUEST_PO_ARGENT), quest_lire32(QUEST_PO_GRADE));
    quest_dire(m, (long long)g_quest_rival);
}

/* Appelee a chaque tour, meme HORS de l'etat du Quest : c'est elle qui
 * ramene.
 *
 * UNE MANCHE, PAS UNE SERIE. Frederic, 2026-09-29 : « le combat part sans
 * l'ecran de selection, mais c'est le mode arcade qui se lance. » C'est
 * exact, et c'est lisible : le MODE DE JEU (`0x180751010`, lu par
 * `0x18019C090`) vaut 0 = ARCADE tant que personne ne le pose, et l'arbitre
 * d'arcade enchaine HUIT combats (`0x1800B1D80` : `[session+0x3F0] >= 8`).
 * Le Quest, lui, veut UNE manche contre le rival, puis son ecran.
 *
 * On ne touche pas a l'arbitre : on reprend la main. Le combat est le
 * sous-etat 19 ; des qu'il le QUITTE -- quelle que soit la raison, fin de
 * manche, GAMEOVER ou retour au selecteur -- on redemande l'etat du Quest.
 * C'est le meme geste que SCOREBOARDS, deja valide a l'ecran.
 */
static void quest_retour_de_combat(void)
{
    unsigned char *b = g_quest_base;
    int mode, sous;
    if (!b || !g_quest_combat) return;
    mode = *(int *)(b + QUEST_RVA_MODE);
    sous = *(int *)(b + QUEST_RVA_SOUSETAT);
    if (g_quest_combat == 1) {
        /* ON ATTEND LE MODE **GAME**, pas « autre chose que le menu ».
         * La premiere version comparait au MENU -- mais on part de
         * DATA_TEST (mode 3, l'ecran du Quest), donc elle concluait aussitot
         * que le combat etait parti. Le journal le disait en clair :
         * « le combat est parti, mode 3 ». */
        if (mode == QUEST_MODE_GAME) {
            quest_f_modejeu mj = (quest_f_modejeu)(b + QUEST_RVA_MODEJEU_LIRE);
            quest_f_session_lire lire =
                (quest_f_session_lire)(b + QUEST_RVA_SESSION_LIRE);
            unsigned char *s = (unsigned char *)lire();
            char m[160];
            g_quest_combat = 2;
            g_quest_vu_vs = 0;
            quest_dire("le combat est parti, sous-etat", (long long)sous);
            /* CE QUE LE MOTEUR A RETENU, une fois la preparation faite : le
             * mode de jeu (0 = Arcade, 1 = Score Attack, 2 = License, 3 =
             * Special Sparring, 4 = Versus) et les deux personnages, RELUS
             * dans la session. Si le rival n'y est plus, c'est la preparation
             * qui l'a remplace, et c'est ici qu'on le verra. */
            if (s) {
                int *q = (int *)(s + QUEST_SESSION_PERSO);
                _snprintf(m, sizeof m,
                          "mode de jeu %d ; persos relus %d contre %d ;"
                          " en piste %d/%d ; cas 1P/2P",
                          mj(), q[0], q[1],
                          s[QUEST_SESSION_ENPISTE],
                          s[QUEST_SESSION_ENPISTE + 1]);
                quest_dire(m, (long long)*(int *)(s + 0x4E8));
            }
            return;
        }
        /* rien n'est parti au bout de dix secondes : on renonce plutot que
         * de rester accroche a un etat qui ne viendra pas. */
        if (GetTickCount() - g_quest_combat_ms > 10000) {
            g_quest_combat = 0;
            quest_dire("le combat n est jamais parti : on renonce", 0);
        }
        return;
    }
    if (g_quest_combat == 2) {
        /* UNE MANCHE. On guette le sous-etat 19 (VS), puis sa SORTIE. */
        if (mode == QUEST_MODE_GAME && sous == QUEST_SOUS_VS) {
            g_quest_vu_vs = 1;
            return;
        }
        if (g_quest_vu_vs) {
            g_quest_combat = 3;
            quest_apres_combat();
            quest_dire("la manche est finie, sous-etat", (long long)sous);
            return;
        }
        /* le filet de secours d'avant : si le moteur revient au MENU de
         * lui-meme (le maillon de `--transition-game`), on reprend aussi. */
        if (mode == QUEST_MODE_MENU) g_quest_combat = 3;
        return;
    }
    {
        quest_f_voeu v_mode = (quest_f_voeu)(b + QUEST_RVA_VOEU_MODE);
        quest_f_voeu v_sous = (quest_f_voeu)(b + QUEST_RVA_VOEU_SOUS);
        g_quest_combat = 0;
        g_quest_vu_vs = 0;
        v_mode(QUEST_MODE);
        v_sous(QUEST_SOUS);
        quest_dire("retour de combat : on redemande le Quest, rival",
                   (long long)g_quest_rival);
    }
}

/* LES TROIS BORNES D'UNE SALLE
 *
 * Ancres de `store_menu_win`, lues dans la planche ; les ecarts viennent du
 * code de 2007 (`DAT_8208E6F8` = 122, `DAT_82000F0C` = 12).
 *
 * QUI EST ASSIS. En 2007 les trois occupants sont trois numeros de rival
 * ranges dans la tache (`+0x64`, `+0x68`, `+0x6C`) et renouveles par le jeu.
 * Nous n'avons pas ce renouvellement : on prend les TROIS PREMIERS rivaux du
 * lieu qui ne sont PAS ENCORE BATTUS, et les trois premiers tout court quand
 * la salle est finie. C'est une regle a nous, et elle a un merite : la salle
 * se vide a mesure qu'on la gagne. */
#define QUEST_BORNE_X    257.0f
#define QUEST_BORNE_X2   644.0f
#define QUEST_BORNE_Y    136.0f
#define QUEST_BORNE_PAS   88.0f          /* 136 -> 224 -> 312 */
#define QUEST_BORNE_DX   122.0f          /* DAT_8208E6F8 */
#define QUEST_BORNE_DY    12.0f          /* DAT_82000F0C */

static int quest_borne_occupant(int borne)
{
    int lieu = quest_lieu_courant();
    int n, k = 0, repli = -1, vus = 0;
    if (lieu < 0 || !quest_rivaux()) return -1;
    for (n = 0; n < QUEST_RIVAUX_NOMBRE; n++) {
        if (quest_rival_lieu(n) != lieu) continue;
        if (vus == borne) repli = n;
        vus++;
        if (quest_profil_bit(QUEST_PO_BATTU, n)) continue;
        if (k == borne) return n;
        k++;
    }
    return repli;
}

/* Ce que porte la fenetre ouverte. Trois fenetres tournent avec BAS :
 * 0 le lieu, 1 la liste des joueurs, 2 le statut. */
static void quest_fenetre_contenu(void)
{
    int i;
    const int *menu;

    if (g_quest_fenetre == 1) {                        /* la liste */
        quest_fenetre_joueurs();
        return;
    }
    if (g_quest_fenetre == 2) {                        /* le statut */
        quest_fenetre_statut();
        return;
    }
    /* LES TROIS MENUS, ET ILS SONT DIFFERENTS -- lecture du 2026-09-27,
     * `analysis/quest_regles.md`. Le curseur est la couleur, comme dans la
     * liste : la ligne choisie prend le vert-jaune des titres.
     *
     *   la maison         six lignes
     *   le dome           trois entrees de tournoi (`hall_menu_win`)
     *   une salle         TROIS BORNES et leurs occupants, plus Tournament
     *                     et Customize (`store_menu_win`) -- c'est LA qu'on
     *                     se bat, et c'est ce qui manquait pour que le mode
     *                     ait un sens.
     */
    if (!g_quest_zooms[g_quest_salle]) {               /* la maison */
        menu = g_quest_menu_maison;
        for (i = 0; i < 6; i++)
            quest_ecrire_ancre(640.0f,
                               (i < 4 ? 166.0f + 30.0f * i
                                      : 330.0f + 30.0f * (i - 4)),
                               30.0f, QUEST_AL_CT,
                               i == g_quest_menu ? QUEST_COUL_TITRE
                                                 : QUEST_COUL_TEXTE,
                               quest_texte(menu[i]));
        return;
    }
    quest_ecrire_ancre(640.0f, 100.0f, 30.0f, QUEST_AL_CT, QUEST_COUL_TITRE,
                       quest_texte(g_quest_noms_lieu[g_quest_salle]));
    if (g_quest_salle == QUEST_SALLE_DOME) {           /* le dome */
        quest_ecrire_ancre(640.0f, 176.0f, 30.0f, QUEST_AL_CT,
                           g_quest_menu == 0 ? QUEST_COUL_TITRE
                                             : QUEST_COUL_TEXTE,
                           quest_texte(599));   /* Official Tournaments */
        quest_ecrire_ancre(640.0f, 206.0f, 30.0f, QUEST_AL_CT,
                           QUEST_COUL_GRISE, quest_texte(600));
        quest_ecrire_ancre(640.0f, 287.0f, 30.0f, QUEST_AL_CT,
                           g_quest_menu == 1 ? QUEST_COUL_TITRE
                                             : QUEST_COUL_TEXTE,
                           quest_texte(601));   /* List of official tourn. */
        quest_ecrire_ancre(640.0f, 351.0f, 30.0f, QUEST_AL_CT,
                           g_quest_menu == 2 ? QUEST_COUL_TITRE
                                             : QUEST_COUL_TEXTE,
                           quest_texte(602));   /* Customize */
        return;
    }
    /* UNE SALLE D'ARCADE : trois bornes, et qui y est assis.
     *
     * Ancres de `store_menu_win`, mesurees dans la planche :
     *   c_button_csr_a_01_lt  257 136     c_button_csr_b_01_lt  644 136
     *   c_button_csr_a_02_lt  257 224     c_button_csr_a_04_lt  644 312
     *   c_button_csr_a_03_lt  257 312
     * Le nom de l'occupant se pose a +122 en x et +12 en y de son ancre
     * (`DAT_8208E6F8`, `DAT_82000F0C`). */
    for (i = 0; i < 3; i++) {
        int n = quest_borne_occupant(i);
        float y = QUEST_BORNE_Y + QUEST_BORNE_PAS * i;
        unsigned c = i == g_quest_menu ? QUEST_COUL_TITRE : QUEST_COUL_TEXTE;
        const char *nom;
        quest_ecrire_ancre(QUEST_BORNE_X, y, 30.0f, QUEST_AL_LT, c,
                           quest_texte(589 + i));        /* « 1 » « 2 » « 3 » */
        if (n < 0) continue;
        nom = quest_profil_bit(QUEST_PO_RENCONTRE, n)
            ? quest_rival_texte(n, QUEST_RIVAL_NOM) : QUEST_INCONNU;
        if (quest_profil_bit(QUEST_PO_BATTU, n))
            quest_ecrire_ancre(QUEST_BORNE_X + QUEST_BORNE_DX - 30.0f,
                               y + QUEST_BORNE_DY, 30.0f, QUEST_AL_LT,
                               QUEST_COUL_JAUNE, QUEST_ETOILE);
        quest_ecrire_ancre(QUEST_BORNE_X + QUEST_BORNE_DX,
                           y + QUEST_BORNE_DY, 30.0f, QUEST_AL_LT, c, nom);
        /* SON GRADE, a droite du bouton -- c'est ce que 2007 affiche
         * (« Raeme 4th kyu »), et il se lit dans `npc_tbl + 0x7C`. */
        if (quest_profil_bit(QUEST_PO_RENCONTRE, n)) {
            char g[32];
            int gr = quest_rival_grade(n);
            if (gr >= 0)
                quest_ecrire_ancre(QUEST_BORNE_X2 - 24.0f, y + QUEST_BORNE_DY,
                                   26.0f, QUEST_AL_RT, c,
                                   quest_grade_texte(gr, g, sizeof g));
        }
    }
    quest_ecrire_ancre(QUEST_BORNE_X2, QUEST_BORNE_Y, 30.0f, QUEST_AL_LT,
                       g_quest_menu == 3 ? QUEST_COUL_TITRE : QUEST_COUL_TEXTE,
                       quest_texte(592));                /* Tournament */
    quest_ecrire_ancre(QUEST_BORNE_X2, QUEST_BORNE_Y + QUEST_BORNE_DY, 30.0f,
                       QUEST_AL_LT, QUEST_COUL_GRISE, quest_texte(593));
    quest_ecrire_ancre(QUEST_BORNE_X2, QUEST_BORNE_Y + QUEST_BORNE_PAS * 2,
                       30.0f, QUEST_AL_LT,
                       g_quest_menu == 4 ? QUEST_COUL_TITRE : QUEST_COUL_TEXTE,
                       quest_texte(594));                /* Customize */
}

/* LE RAPPEL DE RENDU. Appele par la greffe depuis le creneau 4 d'AetMgr --
 * celui qui fait dessiner toutes les scenes AET -- DONC A CHAQUE IMAGE ET SUR
 * TOUS LES ECRANS : on ne dessine le Quest que si son ecran est monte.
 *
 * LES TEMOINS ONT ETE RETIRES LE 2026-09-26. « QUEST FS » et « QUEST 127 »
 * sont sortis tous les deux, sur capture : la recette transcrite de
 * `0x1801BC580` fonctionne, et la profondeur n'est pas en cause (les deux
 * compartiments, 71 et 127, se voient). Ce qui reste est le CONTENU. */
/* ------------------------------------------------------------------------
 * LA MUSIQUE DU MODE QUEST
 *
 * Le morceau n'est pas choisi : il est NOMME dans le code de 2007.
 * `sound/bgm/vf5ps3_b03map.adx` est demande par `TaskQuestMap`
 * (`0x8230CBC0`), `TaskQuestHomeMenu` (`0x8230B7D0`) et `TaskQuestTenpo`
 * (`0x82315500`) -- les trois ecrans de la carte -- et par personne d'autre.
 *
 * Final Showdown ne l'a pas : la musique est partie avec le mode.
 * `tools/musique_quest.py` la pose dans `vf5fs_media/rom/sound/bgm/`, un
 * fichier NEUF, comme la table des rivaux.
 *
 * On la joue avec la fonction du jeu lui-meme : `0x180185DA0(voie, chemin, 0)`
 * est ce que FS appelle pour `rom/sound/bgm/vf5fs_bgm_sel.adx` dans
 * `0x18016D180`, et `0x180186D40(voie)` l'arrete -- c'est deja l'appel que la
 * transition vers le combat emploie.
 */
/* LES BRUITAGES. `0x180185AB0(nom)` joue une amorce sonore par son NOM --
 * c'est ce que le moteur s'appelle a lui-meme (`0x180172730` :
 * `FUN_180185AB0("sy_cursor_move")`, `"sy_select_kettei_B"`).
 *
 * Le Quest de 2007 a ses propres noms (`map_cursor_move`, `map_select`,
 * `map_select_cancel`, `map_open`, `vfv_ps3_sel` pour le compteur d'argent),
 * et Final Showdown ne les connait pas -- aucun ne figure dans son binaire.
 * On prend donc les SIENS, qui sont de la meme famille et deja charges :
 *
 *   sy_cursor_move        le curseur           (map_cursor_move)
 *   sy_select_kettei_B    la validation        (map_select)
 *   vfes_se_cansel_01     l'annulation         (map_select_cancel)
 *   vfes_se_custom_select on entre quelque part (map_open)
 *   sy_charin00st         la piece, pour le compteur d'argent (vfv_ps3_sel)
 */
#define QUEST_RVA_SON        0x185AB0
#define QUEST_SON_CURSEUR    "sy_cursor_move"
#define QUEST_SON_VALIDER    "sy_select_kettei_B"
#define QUEST_SON_ANNULER    "vfes_se_cansel_01"
#define QUEST_SON_OUVRIR     "vfes_se_custom_select"
#define QUEST_SON_PIECE      "sy_charin00st"

typedef int (*quest_f_son)(const char *nom);

static void quest_son(const char *nom)
{
    if (g_quest_base && nom)
        ((quest_f_son)(g_quest_base + QUEST_RVA_SON))(nom);
}

#define QUEST_RVA_BGM_JOUER  0x185DA0
#define QUEST_RVA_BGM_ARRET  0x186D40
#define QUEST_BGM_CHEMIN     "rom/sound/bgm/vf5ps3_b03map.adx"

typedef void (*quest_f_bgm)(int voie, const char *chemin, int p3);
typedef void (*quest_f_bgm_arret)(int voie);

static int g_quest_bgm;                  /* 1 = elle joue */

static void quest_musique(int marche)
{
    unsigned char *b = g_quest_base;
    if (!b || marche == g_quest_bgm) return;
    g_quest_bgm = marche;
    if (marche) {
        quest_f_bgm jouer = (quest_f_bgm)(b + QUEST_RVA_BGM_JOUER);
        jouer(0, QUEST_BGM_CHEMIN, 0);
        quest_dire("musique du Quest lancee (" QUEST_BGM_CHEMIN ")", 0);
    } else {
        quest_f_bgm_arret arret = (quest_f_bgm_arret)(b + QUEST_RVA_BGM_ARRET);
        arret(0);
        quest_dire("musique du Quest arretee", 0);
    }
}

/* ------------------------------------------------------------------------
 * LA CARRIERE : CREATION DE DONNEES, ACCUEIL, ET CARTE DU JOUEUR
 *
 * Ecrit le 2026-09-29, apres que Frederic a montre en captures ce que le
 * Quest de 2007 est REELLEMENT : « ca commence par la selection d'un
 * personnage et la creation de donnees pour le personnage choisi. Il commence
 * donc avec une somme d'argent (50000G) et un grade (10th kyu), puis une
 * explication. Les combattants ont tous un nom specifique et un grade. »
 *
 * Il avait raison, et le portage n'avait rien de tout cela. Ce bloc le pose,
 * et chaque nombre vient du code de 2007 (`analysis/mode_quest.md` §9.28) :
 *
 *   l'argent de depart   **50 000**, plafond **999 999**  (`0x8230CF50`)
 *   le versement         **+500 par trame**, un son toutes les trois trames,
 *                        trente trames d'attente avant et apres
 *   le message           libelle **523**, celui de la notice
 *   le grade de depart   **0 = 10th kyu**
 *   les libelles         396 « W:%6d », 397 « L:%6d », 400 « Win ratio: »,
 *                        401 « % », 999 « %dG »
 *
 * LE WIN RATIO N'EST PAS STOCKE : `FUN_82308C90` le calcule, W / (W + L)
 * x 100, et c'est ce que nous faisons.
 *
 * LE GRADE EST UN PICTO CHEZ 2007 (`gamdan_kyu01`..`kyu10`) et Final Showdown
 * a la planche (`spr_s_gamdan`). Tant que le dessin de sprite n'est pas
 * ecrit, on rend le grade EN TEXTE. Les dix premiers crans sont verifies sur
 * la capture de Frederic -- « Raeme 4th kyu » est le grade 6, « Qazi 10th
 * kyu » le grade 0 -- donc 0 = 10th kyu et l'echelle monte. Au-dela du
 * dixieme cran, les noms de 2007 ne sont PAS etablis : on rend « dan » et le
 * numero, et on ne devine pas les rangs nommes.
 *
 * LE ROSTER : les dix-neuf personnages de `analysis/CHARACTERS.md`, qui vient
 * de la table du jeu lui-meme. Dural n'y est pas -- 2007 ne la propose pas,
 * et son numero differe selon les sources (19 ou 20) : on ne tranche pas ici.
 */
#define QUEST_PHASE_CREATION 0
#define QUEST_PHASE_ACCUEIL  1
#define QUEST_PHASE_JEU      2
#define QUEST_PERSOS_CHOIX   19
#define QUEST_CREA_COLONNES  5
#define QUEST_CREA_X         190.0f
#define QUEST_CREA_Y         240.0f
#define QUEST_CREA_PAS_X     200.0f
#define QUEST_CREA_PAS_Y     56.0f
#define QUEST_CARTE_X        96.0f
#define QUEST_CARTE_Y        498.0f
#define QUEST_CARTE_DROITE   600.0f
#define QUEST_ACCUEIL_PAS    500          /* G par trame */
#define QUEST_ACCUEIL_ATTENTE 30          /* trames */

static const char *const g_quest_noms_perso[QUEST_PERSOS_CHOIX] = {
    "AKIRA", "AOI", "BRAD", "GOH", "JACKY", "JEFFRY", "KAGE", "LAU",
    "LEI-FEI", "LION", "PAI", "SARAH", "SHUN", "VANESSA", "WOLF",
    "EL BLAZE", "EILEEN", "JEAN", "TAKA-ARASHI"
};

/* LE PORTRAIT DU JOUEUR : `chara_face_player`, A MARQUEURS NOMMES.
 *
 * Releve le 2026-10-20 avec `tools/arbre_aet.py` : la composition racine
 * `chara_face_player` de `aet_n_qwin` porte DIX-SEPT images de 104 x 106,
 * un creneau de soixante trames chacune, et ses marqueurs ne sont PAS des
 * nombres comme ceux du badge -- ce sont les CODES du jeu :
 *
 *     aki pai lau wol jef kag sar jak shu lio aoi lei van goh bra msk mon
 *
 * avec, seize trames plus loin, un `<code>_end` : c est une animation
 * d apparition. On joue donc de `<code>` a `<code>_end`, et le calque tient
 * sa derniere image.
 *
 * DIX-SEPT, PAS DIX-NEUF : la planche est celle de 2007. **JEAN et
 * TAKA-ARASHI n y ont pas de portrait** -- on rend alors NULL et rien n est
 * pose, plutot que d afficher le visage d un autre. */
static const char *const g_quest_face[QUEST_PERSOS_CHOIX] = {
    "aki",  /*  0 AKIRA    */  "aoi",  /*  1 AOI         */
    "bra",  /*  2 BRAD     */  "goh",  /*  3 GOH         */
    "jak",  /*  4 JACKY    */  "jef",  /*  5 JEFFRY      */
    "kag",  /*  6 KAGE     */  "lau",  /*  7 LAU         */
    "lei",  /*  8 LEI-FEI  */  "lio",  /*  9 LION        */
    "pai",  /* 10 PAI      */  "sar",  /* 11 SARAH       */
    "shu",  /* 12 SHUN     */  "van",  /* 13 VANESSA     */
    "wol",  /* 14 WOLF     */  "msk",  /* 15 EL BLAZE    */
    "mon",  /* 16 EILEEN   */  0,      /* 17 JEAN        */
    0                          /* 18 TAKA-ARASHI */
};

static const char *quest_face_joueur(char *out, size_t n)
{
    int p;
    quest_profil_charger();
    if (!quest_lire32(QUEST_PO_CREE)) return 0;
    p = (int)quest_lire32(QUEST_PO_PERSO);
    if (p < 0 || p >= QUEST_PERSOS_CHOIX) return 0;
    if (!g_quest_face[p]) return 0;
    _snprintf(out, n, "%s_end", g_quest_face[p]);
    out[n - 1] = 0;
    return g_quest_face[p];
}

static int g_quest_carriere = QUEST_PHASE_JEU;
static int g_quest_choix;                 /* le personnage sous le curseur */
static int g_quest_accueil;               /* 0..10, la machine de 2007 */
static unsigned g_quest_accueil_cible;    /* l'argent vise */
static int g_quest_accueil_attente;       /* les trames qui restent */
static int g_quest_accueil_tic;           /* pour le son toutes les 3 */

/* LE GRADE EN TOUTES LETTRES. Voir l'avertissement en tete de bloc : seuls
 * les dix crans « kyu » sont etablis, et ils le sont par une capture. */
static const char *quest_grade_texte(int g, char *out, size_t n)
{
    static const char *const kyu[10] = {
        "10th kyu", "9th kyu", "8th kyu", "7th kyu", "6th kyu",
        "5th kyu", "4th kyu", "3rd kyu", "2nd kyu", "1st kyu"
    };
    if (g < 0) g = 0;
    if (g < 10) {
        _snprintf(out, n, "%s", kyu[g]);
    } else {
        _snprintf(out, n, "dan %d", g - 9);
    }
    out[n - 1] = 0;
    return out;
}

/* LA CARTE DU JOUEUR, sur la carte du Quest : nom, grade, W, L, le ratio et
 * l'argent. C'est ce que `FUN_82308C90` dessine en 2007. */
static void quest_carte_joueur(void)
{
    char ligne[120], grade[32];
    const char *nom;
    unsigned w, l, argent;
    quest_profil_charger();
    if (!quest_lire32(QUEST_PO_CREE)) return;
    nom = (const char *)(g_quest_profil + QUEST_PO_NOM);
    w = quest_lire32(QUEST_PO_VICTOIRES);
    l = quest_lire32(QUEST_PO_DEFAITES);
    argent = quest_lire32(QUEST_PO_ARGENT);
    /* CHAQUE LIGNE A SON ANCRE, et l ancre vient de la planche -- plus
     * aucune coordonnee devinee ici. Voir le bloc QUEST_ANCRE_* plus haut. */
    /* TAILLE 24, PAS 30. Frederic : « le nom du personnage est trop bas ».
     * Les sept reperes de la fiche sont des carres de 24 x 24 -- le releve
     * de `tools/arbre_aet.py` le donne pour chacun -- quand les ancres des
     * autres ecrans portent leur taille dans leur nom (`_hed_30_02_lt`,
     * `_sel_30_02_rt`). La taille
     * du repere EST la taille du texte : a 30, le nom depassait du bandeau
     * rouge, qui ne fait que quarante pixels de haut (418..458). */
    quest_ecrire_ancre(QUEST_ANCRE_NOM_X, QUEST_ANCRE_NOM_Y, 24.0f,
                       QUEST_AL_LT, QUEST_COUL_TEXTE,
                       *nom ? nom : QUEST_NOM_DEFAUT);
    /* LE GRADE N EST PLUS ECRIT EN TOUTES LETTRES : `p_dan_point_c` est la
     * place d un PICTO, et le picto est pose (g_quest_badge). Le texte
     * faisait double emploi -- 2007 n en a pas. `quest_grade_texte` reste,
     * elle sert au journal. */
    (void)grade;
    /* les libelles du jeu portent leur propre largeur : « W:%6d » */
    {
        const char *fw = quest_texte(396), *fl = quest_texte(397);
        char a[48], b[48];
        _snprintf(a, sizeof a, fw ? fw : "W:%6d", w);
        _snprintf(b, sizeof b, fl ? fl : "L:%6d", l);
        _snprintf(ligne, sizeof ligne, "%s   %s", a, b);
        quest_ecrire_ancre(QUEST_ANCRE_L1_X, QUEST_ANCRE_L1_Y, 26.0f,
                           QUEST_AL_LT, QUEST_COUL_TEXTE, ligne);
    }
    {
        const char *t = quest_texte(400), *p = quest_texte(401);
        double r = (w + l) ? (100.0 * (double)w / (double)(w + l)) : 0.0;
        _snprintf(ligne, sizeof ligne, "%s %.2f%s", t ? t : "Win ratio:", r,
                  p ? p : "%");
        quest_ecrire_ancre(QUEST_ANCRE_L2_X, QUEST_ANCRE_L2_Y, 26.0f,
                           QUEST_AL_LT, QUEST_COUL_TEXTE, ligne);
    }
    {
        const char *g = quest_texte(999);
        _snprintf(ligne, sizeof ligne, g ? g : "%dG", argent);
        quest_ecrire_ancre(QUEST_BOITE_X + QUEST_BOITE_LARGE
                           - QUEST_BOITE_MARGE, QUEST_OR_Y, 30.0f,
                           QUEST_AL_RT, QUEST_COUL_JAUNE, ligne);
    }
    /* LE PAVE DU COSTUME. Les libelles de 2007 sont connus -- « Main
     * Costume » est le 596, « Sub Costume » le 597, « Type A » le 809,
     * releves dans `lang/en/string_array.bin` du media de 2007 -- mais
     * AUCUN des trois n est dans notre import de 492 textes. On les demande
     * quand meme, et on retombe sur la chaine en clair tant qu ils n y sont
     * pas : c est le meme usage que pour « W:%6d » plus haut. */
    /* LES DEUX PAVES, en IMAGE et non en texte -- Frederic : « Main
     * Costume », « Type A » n est pas du texte mais une image. Ils sont
     * dans la planche commune de Final Showdown, en anglais.
     *
     * Le rectangle est celui mesure sur la capture de 2007 : la colonne
     * x 805..977 que l ancre de l argent annonce, le pave principal de
     * 429 a 469, le second juste dessous. */
    /* SUSPENDU (2026-10-20) : l appel fait PLANTER le jeu (violation d
     * acces a la premiere trame de l ecran Quest). Voir §37.16 -- la
     * structure de la commande est juste, c est la CONSTRUCTION du
     * descripteur qui ne l est pas. Remettre 1 ici pour reprendre. */
#if 0   /* le descripteur copiait le MAUVAIS modele -- voir §37.26 */
    quest_sprite(QUEST_SPR_COS_MAIN_1, QUEST_BOITE_X, QUEST_COS_TITRE_Y,
                 QUEST_BOITE_LARGE, 40.0f, 0xFFFFFFFFu);
    quest_sprite(QUEST_SPR_COS_SUB_1, QUEST_BOITE_X, QUEST_COS_TITRE_Y + 44.0f,
                 QUEST_BOITE_LARGE, 40.0f, 0xFFFFFFFFu);
#endif
    /* LE DRAPEAU « PRET » DU SPRSET (2026-10-20).
     *
     * `0x18018CA20` n accepte la commande que si
     *
     *     sprset != 0  &&  *(char *)(sprset + 0xB8) != 0
     *
     * On refait SA recherche, a l identique, pour lire les deux. La map est
     * au tout debut du contexte ; ses noeuds portent la cle en +0x20, les
     * fils en +0x00 et +0x10, le drapeau de feuille en +0x19, et la valeur
     * commence en +0x28. Lecture seule. */
    {
        static int dit_spr;
        if (!dit_spr) {
            unsigned char *ctx =
                *(unsigned char **)(g_quest_base + QUEST_RVA_MGR_SPR);
            unsigned char *racine = ctx ? *(unsigned char **)ctx : 0;
            unsigned char *garde = racine, *n = 0, *val = 0;
            unsigned cle = 1;                 /* le jeu de SPR_C_CMN */
            int tours = 0;
            dit_spr = 1;
            if (racine) n = *(unsigned char **)(racine + 0x08);
            while (n && *(char *)(n + 0x19) == 0 && tours++ < 64) {
                if (*(unsigned *)(n + 0x20) < cle)
                    n = *(unsigned char **)(n + 0x10);
                else { garde = n; n = *(unsigned char **)n; }
            }
            if (garde && garde != racine && cle >= *(unsigned *)(garde + 0x20))
                val = garde + 0x28;
            quest_dire("SPRSET du jeu 1 : contexte", (long long)ctx);
            quest_dire("   la valeur trouvee", (long long)val);
            if (val)
                quest_dire("   son drapeau PRET en +0xB8",
                           (long long)*(unsigned char *)(val + 0xB8));
        }
    }
    /* CE QUE LA RESOLUTION REND POUR NOS PAVES (2026-10-20).
     *
     * `0x180187C00` traduit l identifiant avant de deposer :
     *     enreg = 0x18018C610(base, desc[1]) ;  desc[1] = enreg[0x28]
     * Si `enreg` est nul, la traduction echoue en silence et la commande
     * part avec un identifiant qui ne designe rien -- ce qui expliquerait
     * tout. On le journalise une fois, et on ne lit `+0x28` que s il est
     * non nul. */
    {
        static int dit_res;
        if (!dit_res) {
            quest_f_spr_resoudre resoudre =
                (quest_f_spr_resoudre)(g_quest_base + QUEST_RVA_SPR_RESOUDRE);
            void *base = *(void **)(g_quest_base + 0x719908);
            void *e;
            dit_res = 1;
            e = base ? resoudre(base, QUEST_SPR_COS_MAIN_1) : 0;
            quest_dire("resolution de 55095 : enregistrement",
                       (long long)e);
            if (e)
                quest_dire("   son identifiant interne (+0x28)",
                           (long long)*(unsigned *)((char *)e + 0x28));
        }
    }
    /* LE POINTEUR OU TOUT SE DEPOSE. `0x180187AF0` et `0x180187B10` passent
     * toutes deux `DAT_180719900` a `0x18018CA20`. Mesure du 2026-10-20 : il
     * n est PAS nul (0x26F...), le gestionnaire de sprites est donc pret.
     * Le plantage vient d ailleurs -- voir §37.17. */
    {
        static int dit;
        if (!dit) {
            dit = 1;
            quest_dire("gestionnaire de sprites 0x719900",
                       (long long)*(void **)(g_quest_base + 0x719900));
            quest_dire("base des sprites   0x719908",
                       (long long)*(void **)(g_quest_base + 0x719908));
        }
    }
    /* LE TEMOIN : un quad rouge a la place du pave principal, dessine par la
     * fonction DU JEU. A retirer des que la reponse est lue. */
#if QUEST_TEMOIN_QUAD
    {
        unsigned char *b = g_quest_base;
        int sauv = ((quest_f_calque_lire)(b + QUEST_RVA_CALQUE_LIRE))();
        ((quest_f_calque_poser)(b + QUEST_RVA_CALQUE_POSER))(QUEST_CALQUE_TEXTE);
        ((quest_f_cmd_jeu)(b + QUEST_RVA_CMD_JEU))(
            QUEST_BOITE_X, QUEST_COS_TITRE_Y,
            QUEST_BOITE_X + QUEST_BOITE_LARGE, QUEST_COS_TITRE_Y + 40.0f,
            0xFF0000FFu,                      /* a5 -> +0x20/+0x24 couleur */
            (unsigned)QUEST_ORDRE,            /* a6 -> +0x1C le RANG (0..31) */
            0u,                               /* a7 -> +0x08 */
            (unsigned)(QUEST_PLAFOND - QUEST_CALQUE_TEXTE)); /* a8 -> +0x18,
                                 * qui s AJOUTE au calque puis x0x20 : il doit
                                 * rester petit. Les deux etaient inverses, et
                                 * l index debordait le tableau du contexte. */
        ((quest_f_calque_poser)(b + QUEST_RVA_CALQUE_POSER))(sauv);
    }
#endif
    {
        const char *t = quest_texte(596);
        const char *v = quest_texte(809);
        float cx = QUEST_BOITE_X + QUEST_BOITE_LARGE * 0.5f;
        quest_ecrire_ancre(cx, QUEST_COS_TITRE_Y, 18.0f, QUEST_AL_CT,
                           QUEST_COUL_TITRE, t ? t : "Main Costume");
        quest_ecrire_ancre(cx, QUEST_COS_TYPE_Y, 24.0f, QUEST_AL_CT,
                           QUEST_COUL_TEXTE, v ? v : "Type A");
    }
}

/* L'ECRAN DE CREATION : le roster, et une notice. */
static void quest_creation_dessiner(void)
{
    const char *t;
    int i;
    t = quest_texte(1368);        /* « Select the character data to use… » */
    if (!t) t = quest_texte(1363);
    quest_ecrire_ancre(640.0f, 140.0f, 30.0f, QUEST_AL_CT, QUEST_COUL_TITRE,
                       t ? t : "SELECT A CHARACTER");
    for (i = 0; i < QUEST_PERSOS_CHOIX; i++) {
        float x = QUEST_CREA_X + (float)(i % QUEST_CREA_COLONNES)
                                 * QUEST_CREA_PAS_X;
        float y = QUEST_CREA_Y + (float)(i / QUEST_CREA_COLONNES)
                                 * QUEST_CREA_PAS_Y;
        quest_ecrire_ancre(x, y, 28.0f, QUEST_AL_LT,
                           i == g_quest_choix ? QUEST_COUL_TITRE
                                              : QUEST_COUL_TEXTE,
                           g_quest_noms_perso[i]);
    }
    t = quest_texte(1352);        /* « Create new data » */
    quest_ecrire_ancre(640.0f, 560.0f, 28.0f, QUEST_AL_CT, QUEST_COUL_JAUNE,
                       t ? t : "Create new data");
}

/* L'ACCUEIL : le message 523, puis le versement des 50 000 G. La machine est
 * celle de `0x8230CF50`, reduite a ce que nous savons tenir : le message, la
 * pause, le versement, la pause, fini. */
static void quest_accueil_dessiner(void)
{
    char ligne[64];
    const char *t;
    if (g_quest_accueil <= 1) {
        t = quest_texte(523);
        quest_ecrire_boite(200.0f, 260.0f, 880.0f, 200.0f, 26.0f,
                           QUEST_COUL_TEXTE, QUEST_DRAPEAUX, 0,
                           t ? t : "Starting Quest Mode.");
        t = quest_texte(352);          /* « OK » */
        quest_ecrire_ancre(640.0f, 470.0f, 28.0f, QUEST_AL_CT,
                           QUEST_COUL_JAUNE, t ? t : "OK");
        return;
    }
    t = quest_texte(999);
    _snprintf(ligne, sizeof ligne, t ? t : "%dG",
              quest_lire32(QUEST_PO_ARGENT));
    quest_ecrire_ancre(640.0f, 360.0f, 44.0f, QUEST_AL_CT, QUEST_COUL_JAUNE,
                       ligne);
}

static void quest_accueil_tic(void)
{
    unsigned argent;
    if (g_quest_accueil <= 1) return;          /* on attend sa validation */
    if (g_quest_accueil == 2) {                /* la pause d'avant */
        if (--g_quest_accueil_attente > 0) return;
        g_quest_accueil = 3;
        return;
    }
    if (g_quest_accueil == 3) {                /* le versement */
        /* un son toutes les trois trames -- c'est le rythme de 2007 */
        if ((++g_quest_accueil_tic % 3) == 0) quest_son(QUEST_SON_PIECE);
        argent = quest_lire32(QUEST_PO_ARGENT) + QUEST_ACCUEIL_PAS;
        if (argent >= g_quest_accueil_cible) {
            argent = g_quest_accueil_cible;
            g_quest_accueil = 4;
            g_quest_accueil_attente = QUEST_ACCUEIL_ATTENTE;
        }
        quest_ecrire32(QUEST_PO_ARGENT, argent);
        g_quest_profil_sale = 1;
        return;
    }
    if (g_quest_accueil == 4) {                /* la pause d'apres */
        if (--g_quest_accueil_attente > 0) return;
        g_quest_accueil = 5;
        g_quest_carriere = QUEST_PHASE_JEU;
        quest_profil_ecrire();
        quest_dire("accueil fini : la carriere commence avec (G)",
                   (long long)quest_lire32(QUEST_PO_ARGENT));
    }
}

/* LA CREATION DES DONNEES. Le grade de depart est 0 (10th kyu), le nom celui
 * de 2007 (« NO-NAME »), l'argent est verse par l'accueil -- pas ici, pour
 * qu'il se VOIE monter comme dans le jeu. */
static void quest_creer_donnees(int perso)
{
    char m[120];
    quest_profil_charger();
    if (perso < 0 || perso >= QUEST_PERSOS_CHOIX) perso = 0;
    quest_ecrire32(QUEST_PO_PERSO, (unsigned)perso);
    quest_ecrire32(QUEST_PO_ARGENT, 0);
    quest_ecrire32(QUEST_PO_VICTOIRES, 0);
    quest_ecrire32(QUEST_PO_DEFAITES, 0);
    quest_ecrire32(QUEST_PO_GRADE, 0);
    memset(g_quest_profil + QUEST_PO_NOM, 0, QUEST_PO_NOM_TAILLE);
    memcpy(g_quest_profil + QUEST_PO_NOM, QUEST_NOM_DEFAUT,
           sizeof QUEST_NOM_DEFAUT - 1);
    quest_ecrire32(QUEST_PO_CREE, 1);
    g_quest_profil_sale = 1;
    quest_profil_ecrire();
    g_quest_carriere = QUEST_PHASE_ACCUEIL;
    g_quest_accueil = 0;
    g_quest_accueil_cible = QUEST_ARGENT_DEPART;
    g_quest_accueil_attente = QUEST_ACCUEIL_ATTENTE;
    _snprintf(m, sizeof m, "donnees creees : %s, 10th kyu ; personnage",
              g_quest_noms_perso[perso]);
    quest_dire(m, (long long)perso);
}

/* A l'ouverture de l'ecran : pas de donnees, pas de Quest. */
static void quest_carriere_entrer(void)
{
    quest_profil_charger();
    if (quest_lire32(QUEST_PO_CREE)) {
        g_quest_carriere = QUEST_PHASE_JEU;
        return;
    }
    g_quest_carriere = QUEST_PHASE_CREATION;
    g_quest_choix = 0;
    quest_dire("aucune donnee de carriere : ecran de creation", 0);
}

/* Les touches des deux ecrans de la carriere. Rend 1 si elle a pris la main. */
static int quest_carriere_touches(unsigned montants)
{
    if (g_quest_carriere == QUEST_PHASE_CREATION) {
        if (montants & (1u << QUEST_BTN_DROITE))
            g_quest_choix = (g_quest_choix + 1) % QUEST_PERSOS_CHOIX;
        if (montants & (1u << QUEST_BTN_GAUCHE))
            g_quest_choix = (g_quest_choix + QUEST_PERSOS_CHOIX - 1)
                          % QUEST_PERSOS_CHOIX;
        if (montants & (1u << QUEST_BTN_BAS))
            g_quest_choix = (g_quest_choix + QUEST_CREA_COLONNES)
                          % QUEST_PERSOS_CHOIX;
        if (montants & (1u << QUEST_BTN_HAUT))
            g_quest_choix = (g_quest_choix + QUEST_PERSOS_CHOIX
                             - QUEST_CREA_COLONNES) % QUEST_PERSOS_CHOIX;
        if (montants & ((1u << QUEST_BTN_HAUT) | (1u << QUEST_BTN_BAS)
                        | (1u << QUEST_BTN_GAUCHE) | (1u << QUEST_BTN_DROITE)))
            quest_son(QUEST_SON_CURSEUR);
        if (montants & (1u << QUEST_BTN_VALIDER)) {
            quest_son(QUEST_SON_VALIDER);
            quest_creer_donnees(g_quest_choix);
        }
        if (montants & (1u << QUEST_BTN_RETOUR)) {
            quest_son(QUEST_SON_ANNULER);
            quest_quitter();
        }
        return 1;
    }
    if (g_quest_carriere == QUEST_PHASE_ACCUEIL) {
        if (g_quest_accueil <= 1 && (montants & (1u << QUEST_BTN_VALIDER))) {
            quest_son(QUEST_SON_VALIDER);
            g_quest_accueil = 2;
            g_quest_accueil_attente = QUEST_ACCUEIL_ATTENTE;
        }
        return 1;
    }
    return 0;
}

/* LE TOURNOI : on tire trois adversaires parmi les rivaux du dome. */
static void quest_tournoi_ouvrir(void)
{
    int lieu = QUEST_SALLE_DOME, total = quest_lieu_compte(lieu), i;
    if (total <= 0) return;
    for (i = 0; i < QUEST_TOURNOI_TOURS; i++) {
        int k = (int)((GetTickCount() >> (i * 3)) % (unsigned)total);
        g_quest_tournoi_rivaux[i] = quest_rival_du_lieu(lieu, k);
    }
    g_quest_tournoi = 1;
    g_quest_ecran = QUEST_ECRAN_TOURNOI;
    quest_dire("tournoi ouvert : trois tours ; premier adversaire",
               (long long)g_quest_tournoi_rivaux[0]);
}

static void quest_tournoi_dessiner(void)
{
    char ligne[160];
    const char *f;
    int i;
    quest_ecrire_ancre(640.0f, 140.0f, 34.0f, QUEST_AL_CT, QUEST_COUL_TITRE,
                       quest_texte(599));            /* Official Tournaments */
    f = quest_texte(620);                            /* Participants: %d */
    _snprintf(ligne, sizeof ligne, f ? f : "Participants: %d", 4);
    quest_ecrire_ancre(400.0f, 200.0f, 26.0f, QUEST_AL_LT, QUEST_COUL_TEXTE,
                       ligne);
    f = quest_texte(621);                            /* Rounds: %d */
    _snprintf(ligne, sizeof ligne, f ? f : "Rounds: %d", QUEST_TOURNOI_TOURS);
    quest_ecrire_ancre(400.0f, 236.0f, 26.0f, QUEST_AL_LT, QUEST_COUL_TEXTE,
                       ligne);
    for (i = 0; i < QUEST_TOURNOI_TOURS; i++) {
        int n = g_quest_tournoi_rivaux[i];
        const char *nom = n >= 0 ? quest_rival_texte(n, QUEST_RIVAL_NOM) : 0;
        const char *tour = quest_texte(667 + i);      /* Round 1/2/3 */
        float y = 300.0f + 40.0f * (float)i;
        unsigned c = (g_quest_tournoi == i + 1) ? QUEST_COUL_TITRE
                   : (g_quest_tournoi > i + 1) ? QUEST_COUL_JAUNE
                                               : QUEST_COUL_GRISE;
        quest_ecrire_ancre(400.0f, y, 26.0f, QUEST_AL_LT, c,
                           tour ? tour : "Round");
        quest_ecrire_ancre(880.0f, y, 26.0f, QUEST_AL_RT, c, nom ? nom : "?");
    }
    f = quest_texte(624);                    /* 1st place: %dG ... */
    _snprintf(ligne, sizeof ligne, "%d G", QUEST_TOURNOI_TITRE);
    quest_ecrire_ancre(640.0f, 470.0f, 28.0f, QUEST_AL_CT, QUEST_COUL_JAUNE,
                       ligne);
    (void)f;
    quest_ecrire_ancre(640.0f, 560.0f, 26.0f, QUEST_AL_CT, QUEST_COUL_TEXTE,
                       quest_texte(629));    /* Do you want to enter? */
    quest_ecrire_ancre(640.0f, 620.0f, 26.0f, QUEST_AL_CT, QUEST_COUL_JAUNE,
                       quest_texte(3));
}

/* Appelee apres chaque manche quand un tournoi court. */
static void quest_tournoi_apres(int gagne)
{
    unsigned argent;
    if (!g_quest_tournoi) return;
    if (!gagne) {
        quest_dire("tournoi : elimine au tour", (long long)g_quest_tournoi);
        g_quest_tournoi = 0;
        return;
    }
    argent = quest_lire32(QUEST_PO_ARGENT) + QUEST_TOURNOI_LOT;
    if (g_quest_tournoi >= QUEST_TOURNOI_TOURS) {
        argent += QUEST_TOURNOI_TITRE;
        if (argent > QUEST_ARGENT_MAX) argent = QUEST_ARGENT_MAX;
        quest_ecrire32(QUEST_PO_ARGENT, argent);
        /* un emblEme par titre, tant que les treize familles ne sont pas
         * toutes gagnees -- regle de portage, comme le lot. */
        {
            unsigned e = quest_lire32(QUEST_PO_EMBLEMES);
            int k;
            for (k = 0; k < QUEST_EMBLEMES_FAMILLES; k++)
                if (!((e >> k) & 1)) {
                    quest_ecrire32(QUEST_PO_EMBLEMES, e | (1u << k));
                    break;
                }
        }
        g_quest_profil_sale = 1;
        quest_profil_ecrire();
        quest_dire("tournoi : CHAMPION -- libelle 712 ; argent",
                   (long long)quest_lire32(QUEST_PO_ARGENT));
        g_quest_tournoi = 0;
        return;
    }
    if (argent > QUEST_ARGENT_MAX) argent = QUEST_ARGENT_MAX;
    quest_ecrire32(QUEST_PO_ARGENT, argent);
    g_quest_profil_sale = 1;
    quest_profil_ecrire();
    g_quest_tournoi++;
    g_quest_ecran = QUEST_ECRAN_RENCONTRE;
    g_quest_ecran_rival = g_quest_tournoi_rivaux[g_quest_tournoi - 1];
    quest_dire("tournoi : tour suivant ; adversaire",
               (long long)g_quest_ecran_rival);
}

/* LA TABLE DES OBJETS, chargee a la premiere demande. Absente, la boutique
 * reste vide et le reste de l'ecran continue -- comme la table des rivaux. */
static unsigned char *quest_objets(void)
{
    FILE *f;
    long n;
    if (g_quest_objets_vu) return g_quest_objets;
    g_quest_objets_vu = 1;
    f = fopen(QUEST_OBJETS_FICHIER, "rb");
    if (!f) {
        quest_dire("table des objets ABSENTE (" QUEST_OBJETS_FICHIER ")", 0);
        return 0;
    }
    fseek(f, 0, SEEK_END);
    n = ftell(f);
    fseek(f, 0, SEEK_SET);
    if (n > 16) {
        g_quest_objets = (unsigned char *)malloc((size_t)n);
        if (g_quest_objets
                && fread(g_quest_objets, 1, (size_t)n, f) == (size_t)n
                && memcmp(g_quest_objets, "QOBJ", 4) == 0) {
            g_quest_objets_taille = n;
        } else {
            free(g_quest_objets);
            g_quest_objets = 0;
        }
    }
    fclose(f);
    quest_dire("table des objets chargee, octets", (long long)n);
    return g_quest_objets;
}

static unsigned quest_o32(long o)
{
    unsigned char *d = g_quest_objets;
    if (!d || o < 0 || o + 4 > g_quest_objets_taille) return 0;
    return (unsigned)d[o] | ((unsigned)d[o + 1] << 8)
         | ((unsigned)d[o + 2] << 16) | ((unsigned)d[o + 3] << 24);
}

/* La table du personnage du joueur : son decalage, et le nombre d'objets. */
static long quest_boutique_table(int *nombre)
{
    unsigned char *d = quest_objets();
    int perso;
    long o;
    *nombre = 0;
    if (!d) return -1;
    perso = (int)quest_lire32(QUEST_PO_PERSO);
    if (perso < 0 || (unsigned)perso >= quest_o32(8)) return -1;
    o = (long)quest_o32(12 + 4 * perso);
    if (o <= 0 || o + 4 > g_quest_objets_taille) return -1;
    *nombre = (int)quest_o32(o);
    return o + 4;
}

static int quest_objet_possede(int id)
{
    if (id < 0 || id >= QUEST_OBJETS_BITS * 8) return 0;
    return (g_quest_profil[QUEST_PO_OBJETS + (id >> 3)] >> (id & 7)) & 1;
}

static void quest_objet_poser(int id)
{
    if (id < 0 || id >= QUEST_OBJETS_BITS * 8) return;
    g_quest_profil[QUEST_PO_OBJETS + (id >> 3)] |=
        (unsigned char)(1 << (id & 7));
    g_quest_profil_sale = 1;
}

/* LA BOUTIQUE : le titre, l'argent, dix lignes, le prix, et « deja achete ». */
static void quest_boutique_dessiner(void)
{
    char ligne[160];
    int nombre, i;
    long o = quest_boutique_table(&nombre);
    const char *fg = quest_texte(999);
    quest_ecrire_ancre(640.0f, 120.0f, 34.0f, QUEST_AL_CT, QUEST_COUL_TITRE,
                       quest_texte(937));                /* Item shop */
    _snprintf(ligne, sizeof ligne, fg ? fg : "%dG",
              quest_lire32(QUEST_PO_ARGENT));
    quest_ecrire_ancre(1060.0f, 120.0f, 30.0f, QUEST_AL_RT, QUEST_COUL_JAUNE,
                       ligne);
    quest_ecrire_boite(200.0f, 160.0f, 880.0f, 40.0f, 24.0f, QUEST_COUL_TEXTE,
                       QUEST_DRAPEAUX | QUEST_AL_CT, 0, quest_texte(291));
    if (o < 0 || !nombre) {
        quest_ecrire_ancre(640.0f, 300.0f, 28.0f, QUEST_AL_CT,
                           QUEST_COUL_GRISE, "---");
        return;
    }
    for (i = 0; i < QUEST_BOUTIQUE_LIGNES; i++) {
        int k = g_quest_boutique_page * QUEST_BOUTIQUE_LIGNES + i;
        long e = o + (long)k * 8;
        int id, prix, choisi;
        const char *nom;
        float y = 210.0f + 34.0f * (float)i;
        if (k >= nombre) break;
        id = (int)(quest_o32(e) & 0xFFFF);
        prix = (int)((quest_o32(e) >> 16) & 0xFFFF);
        nom = (const char *)(g_quest_objets + quest_o32(e + 4));
        choisi = (k == g_quest_boutique_curseur);
        quest_ecrire_ancre(260.0f, y, 26.0f, QUEST_AL_LT,
                           choisi ? QUEST_COUL_TITRE : QUEST_COUL_TEXTE, nom);
        if (quest_objet_possede(id)) {
            quest_ecrire_ancre(1020.0f, y, 24.0f, QUEST_AL_RT,
                               QUEST_COUL_GRISE, quest_texte(998));
        } else {
            _snprintf(ligne, sizeof ligne, fg ? fg : "%dG", prix);
            quest_ecrire_ancre(1020.0f, y, 26.0f, QUEST_AL_RT,
                               choisi ? QUEST_COUL_JAUNE : QUEST_COUL_TEXTE,
                               ligne);
        }
    }
    _snprintf(ligne, sizeof ligne, "%d / %d", g_quest_boutique_curseur + 1,
              nombre);
    quest_ecrire_ancre(640.0f, 600.0f, 24.0f, QUEST_AL_CT, QUEST_COUL_TEXTE,
                       ligne);
    quest_ecrire_ancre(640.0f, 632.0f, 26.0f, QUEST_AL_CT, QUEST_COUL_JAUNE,
                       quest_texte(3));
}

static void quest_boutique_touches(unsigned montants)
{
    int nombre;
    long o = quest_boutique_table(&nombre);
    if (o < 0 || !nombre) return;
    if (montants & (1u << QUEST_BTN_BAS)) {
        g_quest_boutique_curseur = (g_quest_boutique_curseur + 1) % nombre;
        quest_son(QUEST_SON_CURSEUR);
    }
    if (montants & (1u << QUEST_BTN_HAUT)) {
        g_quest_boutique_curseur =
            (g_quest_boutique_curseur + nombre - 1) % nombre;
        quest_son(QUEST_SON_CURSEUR);
    }
    g_quest_boutique_page = g_quest_boutique_curseur / QUEST_BOUTIQUE_LIGNES;
    if (montants & (1u << QUEST_BTN_VALIDER)) {
        long e = o + (long)g_quest_boutique_curseur * 8;
        int id = (int)(quest_o32(e) & 0xFFFF);
        int prix = (int)((quest_o32(e) >> 16) & 0xFFFF);
        unsigned argent = quest_lire32(QUEST_PO_ARGENT);
        if (quest_objet_possede(id) || argent < (unsigned)prix) {
            quest_son(QUEST_SON_ANNULER);
            return;
        }
        quest_son(QUEST_SON_PIECE);
        quest_ecrire32(QUEST_PO_ARGENT, argent - (unsigned)prix);
        quest_objet_poser(id);
        quest_profil_ecrire();
        quest_dire("objet achete ; identifiant FS", (long long)id);
    }
}

/* L'ECRAN DE RENCONTRE : le rival, son grade, et ce qu'il dit. */
static void quest_rencontre_dessiner(void)
{
    char g[32];
    const char *s;
    int n = g_quest_ecran_rival;
    if (n < 0) return;
    s = quest_rival_texte(n, QUEST_RIVAL_NOM);
    quest_ecrire_ancre(640.0f, 200.0f, 40.0f, QUEST_AL_CT, QUEST_COUL_TITRE,
                       s ? s : "?");
    quest_ecrire_ancre(640.0f, 250.0f, 28.0f, QUEST_AL_CT, QUEST_COUL_TEXTE,
                       quest_grade_texte(quest_rival_grade(n), g, sizeof g));
    s = quest_rival_texte(n, QUEST_RIVAL_DIT1);
    if (s) quest_ecrire_boite(200.0f, 330.0f, 880.0f, 80.0f, 28.0f,
                              QUEST_COUL_TEXTE, QUEST_DRAPEAUX | QUEST_AL_CT,
                              0, s);
    s = quest_rival_texte(n, QUEST_RIVAL_DIT2);
    if (s) quest_ecrire_boite(200.0f, 380.0f, 880.0f, 80.0f, 28.0f,
                              QUEST_COUL_TEXTE, QUEST_DRAPEAUX | QUEST_AL_CT,
                              0, s);
    quest_ecrire_ancre(640.0f, 520.0f, 28.0f, QUEST_AL_CT, QUEST_COUL_JAUNE,
                       quest_texte(3));          /* Back / Enter */
}

/* LES REGLAGES DU QUEST : la difficulte, trois crans. */
static void quest_reglages_dessiner(void)
{
    static const char *const crans[3] = { "NORMAL", "HARD", "VERY HARD" };
    unsigned d = quest_lire32(QUEST_PO_DIFFICULTE);
    int i;
    quest_ecrire_ancre(640.0f, 180.0f, 34.0f, QUEST_AL_CT, QUEST_COUL_TITRE,
                       quest_texte(540));        /* Quest settings */
    quest_ecrire_boite(200.0f, 240.0f, 880.0f, 80.0f, 24.0f, QUEST_COUL_TEXTE,
                       QUEST_DRAPEAUX | QUEST_AL_CT, 0, quest_texte(139));
    for (i = 0; i < 3; i++)
        quest_ecrire_ancre(640.0f, 330.0f + 44.0f * i, 30.0f, QUEST_AL_CT,
                           (unsigned)i == d ? QUEST_COUL_TITRE
                                            : QUEST_COUL_TEXTE, crans[i]);
    quest_ecrire_ancre(640.0f, 520.0f, 28.0f, QUEST_AL_CT, QUEST_COUL_JAUNE,
                       quest_texte(3));
}

/* LA LISTE DES EMBLEMES : treize familles, libelles 571 a 584. */
static void quest_emblemes_dessiner(void)
{
    unsigned bits = quest_lire32(QUEST_PO_EMBLEMES);
    int i;
    quest_ecrire_ancre(640.0f, 140.0f, 34.0f, QUEST_AL_CT, QUEST_COUL_TITRE,
                       quest_texte(569));        /* EMBLEM LIST */
    for (i = 0; i < QUEST_EMBLEMES_FAMILLES; i++) {
        float y = 200.0f + 32.0f * (float)i;
        const char *nom = quest_texte(571 + i);
        quest_ecrire_ancre(420.0f, y, 26.0f, QUEST_AL_LT,
                           (bits >> i) & 1 ? QUEST_COUL_TEXTE
                                           : QUEST_COUL_GRISE,
                           nom ? nom : "?");
        if ((bits >> i) & 1)
            quest_ecrire_ancre(880.0f, y, 26.0f, QUEST_AL_RT,
                               QUEST_COUL_JAUNE, QUEST_ETOILE);
    }
    quest_ecrire_ancre(640.0f, 630.0f, 28.0f, QUEST_AL_CT, QUEST_COUL_JAUNE,
                       quest_texte(3));
}

/* Les touches des trois ecrans. Rend 1 si l'un d'eux a la main. */
static int quest_ecran_touches(unsigned montants)
{
    if (g_quest_ecran == QUEST_ECRAN_AUCUN) return 0;
    if (montants & (1u << QUEST_BTN_RETOUR)) {
        quest_son(QUEST_SON_ANNULER);
        g_quest_ecran = QUEST_ECRAN_AUCUN;
        return 1;
    }
    if (g_quest_ecran == QUEST_ECRAN_RENCONTRE) {
        if (montants & (1u << QUEST_BTN_VALIDER)) {
            int n = g_quest_ecran_rival;
            quest_son(QUEST_SON_VALIDER);
            g_quest_ecran = QUEST_ECRAN_AUCUN;
            quest_partir_au_combat(n);
        }
        return 1;
    }
    if (g_quest_ecran == QUEST_ECRAN_REGLAGES) {
        unsigned d = quest_lire32(QUEST_PO_DIFFICULTE);
        if (montants & (1u << QUEST_BTN_BAS)) {
            d = (d + 1) % 3;
            quest_son(QUEST_SON_CURSEUR);
        }
        if (montants & (1u << QUEST_BTN_HAUT)) {
            d = (d + 2) % 3;
            quest_son(QUEST_SON_CURSEUR);
        }
        if (d != quest_lire32(QUEST_PO_DIFFICULTE)) {
            quest_ecrire32(QUEST_PO_DIFFICULTE, d);
            g_quest_profil_sale = 1;
            quest_profil_ecrire();
        }
        if (montants & (1u << QUEST_BTN_VALIDER)) {
            quest_son(QUEST_SON_VALIDER);
            g_quest_ecran = QUEST_ECRAN_AUCUN;
        }
        return 1;
    }
    if (g_quest_ecran == QUEST_ECRAN_BOUTIQUE) {
        quest_boutique_touches(montants);
        return 1;
    }
    if (g_quest_ecran == QUEST_ECRAN_TOURNOI) {
        if (montants & (1u << QUEST_BTN_VALIDER)) {
            quest_son(QUEST_SON_VALIDER);
            g_quest_ecran = QUEST_ECRAN_RENCONTRE;
            g_quest_ecran_rival = g_quest_tournoi_rivaux[0];
        }
        return 1;
    }
    if (montants & (1u << QUEST_BTN_VALIDER)) {
        quest_son(QUEST_SON_VALIDER);
        g_quest_ecran = QUEST_ECRAN_AUCUN;
    }
    return 1;
}

static void quest_dessiner(void *aetmgr)
{
    (void)aetmgr;
    if (!g_quest_base) return;
    if (!g_quest_vu_ecrire) {
        g_quest_vu_ecrire = 1;
        quest_diagnostic_police();
    }
    if (g_quest_etape != 3) return;
    if (!quest_dans_l_etat()) return;
    g_quest_images++;          /* la bascule des deux dernieres lignes du
                                * statut : 180 images par page */
    if (g_quest_vu_rappel == 0) {
        g_quest_vu_rappel = 1;
        quest_dire("rappel de RENDU : l ecran Quest est monte", 0);
    }
    /* LES TROIS ECRANS AJOUTES passent devant tout le reste. */
    if (g_quest_ecran == QUEST_ECRAN_RENCONTRE) {
        quest_rencontre_dessiner();
        return;
    }
    if (g_quest_ecran == QUEST_ECRAN_REGLAGES) {
        quest_reglages_dessiner();
        return;
    }
    if (g_quest_ecran == QUEST_ECRAN_EMBLEMES) {
        quest_emblemes_dessiner();
        return;
    }
    if (g_quest_ecran == QUEST_ECRAN_BOUTIQUE) {
        quest_boutique_dessiner();
        return;
    }
    if (g_quest_ecran == QUEST_ECRAN_TOURNOI) {
        quest_tournoi_dessiner();
        return;
    }
    /* LA CARRIERE PASSE DEVANT : sans donnees, il n'y a pas de Quest. */
    if (g_quest_carriere == QUEST_PHASE_CREATION) {
        quest_creation_dessiner();
        return;
    }
    if (g_quest_carriere == QUEST_PHASE_ACCUEIL) {
        quest_accueil_dessiner();
        return;
    }
    if (g_quest_zoom) {
        /* un lieu est ouvert : la fenetre et sa ligne de commandes */
        quest_fenetre_contenu();
        if (g_quest_vu_contenu != g_quest_fenetre + 1) {
            char m[200];
            const char *t = quest_texte(g_quest_noms_lieu[g_quest_salle]);
            g_quest_vu_contenu = g_quest_fenetre + 1;
            _snprintf(m, sizeof m,
                      "contenu pose : fenetre %d, lieu %d (%s) ; ligne",
                      g_quest_fenetre, g_quest_salle, t ? t : "(sans nom)");
            quest_dire(m, (long long)(size_t)quest_texte(3));
        }
        quest_ecrire(96.0f, 654.0f, 22.0f, quest_texte(3));   /* Back/Enter */
        return;
    }
    g_quest_vu_contenu = 0;
    quest_carte_joueur();        /* nom, grade, W/L, ratio, argent */
    quest_ecrire(96.0f, 654.0f, 22.0f, quest_texte(14));   /* Open window */
}

static void quest_tic(unsigned int ms)
{
    unsigned char *boite;
    if (!quest_moteur()) return;
    quest_machine();
    boite = quest_boite();
    if (!boite) return;
    /* LE RETOUR DE COMBAT se joue HORS de notre etat : on le teste avant la
     * garde, sinon personne ne ramenerait. */
    quest_retour_de_combat();
    if (!quest_dans_l_etat()) {
        if (g_quest_etape) {          /* on en sort sans l'avoir demande */
            quest_retirer_calques();
            quest_profil_ecrire();
            g_quest_etape = 0;
            g_quest_avant = 0;
            g_quest_zoom = 0;
        }
        g_quest_horloge_avant = 0;    /* le temps DEHORS ne compte pas */
        g_quest_sortant = 0;
        return;
    }
    /* la sortie est demandee mais l'etat n'a pas encore tourne : le moteur a
     * trois trames a faire (boucle, sortie du mode, sortie du sous-etat) */
    if (g_quest_sortant) return;

    /* LE TEMPS DE JEU. Il ne compte que dans le Quest -- nous sommes deja
     * passes par `quest_dans_l_etat`. C'est le seul compteur du profil qui
     * avance aujourd'hui, et c'est lui qui prouve a l'ecran que le profil
     * vit et survit au redemarrage. On ecrit le fichier toutes les trente
     * secondes : assez rare pour ne rien couter, assez souvent pour qu'une
     * fermeture brutale ne perde pas grand-chose. */
    quest_profil_horloge(ms);
    {
        static unsigned dernier;
        unsigned s = quest_lire32(QUEST_PO_SECONDES);
        if (s / 30 != dernier / 30) quest_profil_ecrire();
        dernier = s;
    }

    if (g_quest_etape == 0) {
        /* La base AET et son gestionnaire n'existent pas a tout moment : le
         * tout premier essai est mort dans leur dichotomie, un global a
         * zero. On attend les quatre. */
        void *db = *(void **)(g_quest_base + QUEST_RVA_DB);
        void *mgr = *(void **)(g_quest_base + QUEST_RVA_MGR);
        void *dbs = *(void **)(g_quest_base + QUEST_RVA_DB_SPR);
        void *mgrs = *(void **)(g_quest_base + QUEST_RVA_MGR_SPR);
        void (*preparer)(void);
        quest_f_charger charger, charger_spr;
        if (!db || !mgr || !dbs || !mgrs) return;
        preparer = (void (*)(void))(g_quest_base + QUEST_RVA_PREPARE_SPR);
        charger = (quest_f_charger)(g_quest_base + QUEST_RVA_CHARGER);
        charger_spr =
            (quest_f_charger)(g_quest_base + QUEST_RVA_CHARGER_SPR);
        preparer();
        charger_spr(QUEST_SPR_QUE);
        charger_spr(QUEST_SPR_QWIN);
        charger_spr(QUEST_SPR_QDAN);
        charger(QUEST_AET_QUE);
        charger(QUEST_AET_QWIN);
        charger(QUEST_AET_QDAN);
        charger_spr(QUEST_SPR_CCMN);   /* la planche commune de FS : */
        charger(QUEST_AET_CCMN);       /* le badge de grade vit dedans */
        /* ET CELLE DE 2007, qui seule porte `gen_base` avec son contenu --
         * celle de FS declare la composition et la laisse vide. */
        charger_spr(QUEST_SPR_QCCMN);
        charger(QUEST_AET_QCCMN);
        g_quest_etape = 2;
        g_quest_ms = ms;
        g_quest_avant = 0;
        g_quest_zoom = 0;
        quest_dire("ecran Quest : planche et sprites demandes", QUEST_AET_QUE);
        return;
    }

    if (g_quest_etape == 2) {
        quest_f_etat etat = (quest_f_etat)(g_quest_base + QUEST_RVA_ETAT);
        quest_f_etat etat_spr =
            (quest_f_etat)(g_quest_base + QUEST_RVA_ETAT_SPR);
        char e = etat(QUEST_AET_QUE) | etat_spr(QUEST_SPR_QUE)
               | etat(QUEST_AET_QWIN) | etat_spr(QUEST_SPR_QWIN)
               | etat(QUEST_AET_QDAN) | etat_spr(QUEST_SPR_QDAN)
               | etat(QUEST_AET_CCMN) | etat_spr(QUEST_SPR_CCMN)
               | etat(QUEST_AET_QCCMN) | etat_spr(QUEST_SPR_QCCMN);
        if (!e) {
            g_quest_etape = 3;
            quest_carriere_entrer();   /* pas de donnees ? on les cree */
            quest_musique(1);          /* vf5ps3_b03map.adx, celle de 2007 */
            quest_dire("planches PRETES apres (ms)", (long long)(ms - g_quest_ms));
            g_quest_ms = ms;
            /* PREUVE que la chaine texte est branchee : on demande au moteur
             * de FS trois libelles du Quest, par leur numero de 2007. S'ils
             * reviennent en clair, `string_array.farc` etendu est charge et la
             * borne du resolveur est levee. */
            {
                int essais[3] = {544, 558, 569};   /* STATUS, RIVAL LIST... */
                int k;
                char b[200];
                for (k = 0; k < 3; k++) {
                    const char *t = quest_texte(essais[k]);
                    _snprintf(b, sizeof b, "[quest] texte %d = \"%s\"\n",
                              essais[k], t ? t : "(rien)");
                    OutputDebugStringA(b);
                    {
                        FILE *f = fopen("quest_journal.txt", "a");
                        if (f) { fputs(b, f); fclose(f); }
                    }
                }
            }
            quest_assurer();
        } else if (ms - g_quest_ms > 15000) {
            quest_dire("planche TOUJOURS PAS prete, etat", e);
            quest_quitter();
        }
        return;
    }

    quest_accueil_tic();       /* le versement des 50 000 G, s'il court */
    /* etape 3 : l'ecran est a nous. On lit la manette (le stub la tient :
     * g_masque, un bit par code) et on calcule nos propres fronts. */
    {
        unsigned m = g_masque;
        unsigned montants = ~g_quest_avant & m;
        int change = 0;
        g_quest_avant = m;
        /* la carriere d'abord : creation et accueil prennent tout le clavier */
        if (quest_carriere_touches(montants)) return;
        if (quest_ecran_touches(montants)) return;
        /* T : LA VOIE DU COMBAT. 0 = directe, par le sous-etat 18
         * (MODE_SELECTOR : la preparation que le moteur fait lui-meme) ;
         * 1 = par le selecteur d'arcade, la voie validee a l'ecran le
         * 2026-09-27. On garde les deux : il tranche a l'ecran. */
        if (montants & (1u << QUEST_BTN_VOIE)) {
            g_quest_voie = !g_quest_voie;
            quest_dire(g_quest_voie
                       ? "voie du combat : PAR LE SELECTEUR"
                       : "voie du combat : DIRECTE (sous-etat 18)",
                       (long long)g_quest_voie);
        }
        if (montants & ((1u << QUEST_BTN_HAUT) | (1u << QUEST_BTN_BAS)
                        | (1u << QUEST_BTN_GAUCHE) | (1u << QUEST_BTN_DROITE)))
            quest_son(QUEST_SON_CURSEUR);
        if (montants & (1u << QUEST_BTN_RETOUR)) {
            quest_son(QUEST_SON_ANNULER);
            if (!g_quest_zoom) { quest_quitter(); return; }
            g_quest_zoom = 0;
            g_quest_fenetre = 0;
            change = 1;
            quest_dire("retour a la carte", 0);
        }
        /* LE MENU DE LA MAISON : quatre de ses six lignes marchent.
         *   0 Customize        -- il faut la boutique et les objets
         *   1 Status           -> la fenetre du statut
         *   2 Quest settings   -- il faut les reglages du mode
         *   3 Save             -> ecrire le profil
         *   4 Return to Character Select -> mode GAME / sous-etat SELECTOR
         *   5 End Quest Mode   -> quitter, retour au menu principal
         * Les deux qui manquent demandent des sous-systemes entiers ; les
         * quatre autres sont un geste chacun. */
        if (g_quest_zoom && !g_quest_zooms[g_quest_salle]
                && (montants & (1u << QUEST_BTN_VALIDER))) {
            if (g_quest_menu == 0) {
                g_quest_ecran = QUEST_ECRAN_BOUTIQUE;   /* Customize */
                g_quest_boutique_curseur = 0;
                g_quest_boutique_page = 0;
                quest_dire("maison : Customize -- la boutique", 0);
            } else if (g_quest_menu == 1) {
                g_quest_fenetre = 2;          /* Status */
                g_quest_page = 0;
                change = 1;
                quest_dire("maison : Status", 0);
            } else if (g_quest_menu == 2) {
                g_quest_ecran = QUEST_ECRAN_REGLAGES;   /* Quest settings */
                quest_dire("maison : Quest settings", 0);
            } else if (g_quest_menu == 3) {
                quest_profil_charger();
                g_quest_profil_sale = 1;
                quest_profil_ecrire();
                quest_dire("maison : Save -- profil ecrit, secondes",
                           (long long)quest_lire32(QUEST_PO_SECONDES));
            } else if (g_quest_menu == 4) {
                quest_f_voeu v_mode =
                    (quest_f_voeu)(g_quest_base + QUEST_RVA_VOEU_MODE);
                quest_f_voeu v_sous =
                    (quest_f_voeu)(g_quest_base + QUEST_RVA_VOEU_SOUS);
                quest_profil_ecrire();
                quest_dire("maison : Return to Character Select", 0);
                v_mode(QUEST_MODE_GAME);
                v_sous(17);                   /* SELECTOR */
                return;
            } else if (g_quest_menu == 5) {
                quest_dire("maison : End Quest Mode", 0);
                quest_quitter();
                return;
            }
        }
        /* LE DOME : ses trois entrees. La premiere ouvre le tournoi (le
         * sous-etat 0x55 de 2007), la troisieme la boutique. */
        if (g_quest_zoom && g_quest_fenetre == 0
                && g_quest_salle == QUEST_SALLE_DOME
                && (montants & (1u << QUEST_BTN_VALIDER))) {
            if (g_quest_menu == 0) {
                quest_tournoi_ouvrir();
                return;
            }
            if (g_quest_menu == 2) {
                g_quest_ecran = QUEST_ECRAN_BOUTIQUE;
                g_quest_boutique_curseur = 0;
                g_quest_boutique_page = 0;
                return;
            }
        }
        /* UNE SALLE : sa cinquieme entree est Customize. */
        if (g_quest_zoom && g_quest_fenetre == 0 && g_quest_menu == 4
                && g_quest_zooms[g_quest_salle]
                && g_quest_salle != QUEST_SALLE_DOME
                && (montants & (1u << QUEST_BTN_VALIDER))) {
            g_quest_ecran = QUEST_ECRAN_BOUTIQUE;
            g_quest_boutique_curseur = 0;
            g_quest_boutique_page = 0;
            return;
        }
        /* LE STATUT : VALIDER y ouvre la liste des emblemes (libelle 555). */
        if (g_quest_zoom && g_quest_fenetre == 2
                && (montants & (1u << QUEST_BTN_VALIDER))) {
            g_quest_ecran = QUEST_ECRAN_EMBLEMES;
            return;
        }
        /* VALIDER SUR UNE BORNE : on se bat contre celui qui y est assis.
         * C'est ainsi que le Quest se joue -- libelles 146, 147, 148 :
         * « Play against the opponent on Unit 1 / 2 / 3 ». La liste des
         * rivaux, elle, est un REGISTRE (554 « View rival list »), pas un
         * selecteur : on n'y valide plus rien. */
        if (g_quest_zoom && g_quest_fenetre == 0 && g_quest_menu < 3
                && g_quest_zooms[g_quest_salle]
                && g_quest_salle != QUEST_SALLE_DOME
                && (montants & (1u << QUEST_BTN_VALIDER))) {
            int n = quest_borne_occupant(g_quest_menu);
            if (n >= 0) {
                /* L'ECRAN DE RENCONTRE d'abord : le rival se presente, et ses
                 * deux repliques se lisent enfin. VALIDER part au combat. */
                g_quest_ecran = QUEST_ECRAN_RENCONTRE;
                g_quest_ecran_rival = n;
                quest_profil_poser(QUEST_PO_RENCONTRE, n);
                return;
            }
        }
        if (montants & (1u << QUEST_BTN_VALIDER)) quest_son(QUEST_SON_VALIDER);
        if (!g_quest_zoom && (montants & (1u << QUEST_BTN_VALIDER))) {
            /* la maison entre aussi : elle n'a pas de photographie, elle a
             * `home_menu_win` par-dessus la carte */
            g_quest_zoom = 1;
            change = 1;
            g_quest_page = 0;
            g_quest_curseur = 0;
            g_quest_menu = 0;
            quest_son(QUEST_SON_OUVRIR);
            quest_profil_ouvrir_lieu(quest_lieu_courant());
            quest_dire("lieu ouvert", (long long)g_quest_salle);
        }
        /* LES TOUCHES, UN LIEU OUVERT.
         *
         * Elles ont bouge le 2026-09-27, et pour une raison : la liste des
         * rivaux a maintenant un CURSEUR, et un curseur veut HAUT et BAS.
         * En 2007 c'est exactement ce que fait le jeu (HAUT/BAS deplacent,
         * et la page suit toute seule quand on passe le bord) ; le carrousel
         * des trois fenetres, lui, n'existe pas la-bas -- ce sont trois
         * taches distinctes. On lui donne donc GAUCHE et DROITE.
         *
         *   GAUCHE / DROITE   la fenetre : le lieu, les joueurs, le statut
         *   HAUT / BAS        le curseur dans la liste (la page suit)
         *   VALIDER           combattre le rival sous le curseur
         *   W                 revenir a la carte
         *
         * Sur la carte, rien ne change : GAUCHE/DROITE choisissent le lieu,
         * VALIDER entre, W rend la main au menu. */
        /* HAUT/BAS sur la fenetre du lieu : son menu. Trois entrees dans
         * un lieu, six a la maison. */
        if (g_quest_zoom && g_quest_fenetre == 0) {
            /* six lignes a la maison, trois au dome, CINQ dans une salle :
             * trois bornes, Tournament, Customize. */
            int lignes = !g_quest_zooms[g_quest_salle] ? 6
                       : (g_quest_salle == QUEST_SALLE_DOME) ? 3 : 5;
            if (montants & (1u << QUEST_BTN_HAUT))
                g_quest_menu = (g_quest_menu + lignes - 1) % lignes;
            if (montants & (1u << QUEST_BTN_BAS))
                g_quest_menu = (g_quest_menu + 1) % lignes;
        }
        if (g_quest_zoom && g_quest_fenetre == 1) {
            int total = quest_lieu_compte(quest_lieu_courant());
            if (total > 0) {
                if (montants & (1u << QUEST_BTN_HAUT))
                    g_quest_curseur = (g_quest_curseur + total - 1) % total;
                if (montants & (1u << QUEST_BTN_BAS))
                    g_quest_curseur = (g_quest_curseur + 1) % total;
                /* la page suit le curseur, elle ne se commande pas */
                g_quest_page = g_quest_curseur / QUEST_LISTE_LIGNES;
            }
        }
        if (g_quest_zoom && (montants & (1u << QUEST_BTN_GAUCHE))) {
            g_quest_fenetre = (g_quest_fenetre + 2) % 3;
            g_quest_page = 0;
            g_quest_curseur = 0;
            change = 1;
            quest_dire("fenetre", (long long)g_quest_fenetre);
        }
        if (g_quest_zoom && (montants & (1u << QUEST_BTN_DROITE))) {
            g_quest_fenetre = (g_quest_fenetre + 1) % 3;
            g_quest_page = 0;
            g_quest_curseur = 0;
            change = 1;
            quest_dire("fenetre", (long long)g_quest_fenetre);
        }
        if (!g_quest_zoom && (montants & (1u << QUEST_BTN_GAUCHE))) {
            g_quest_salle = (g_quest_salle + 8) % 9; change = 2;
        }
        if (!g_quest_zoom && (montants & (1u << QUEST_BTN_DROITE))) {
            g_quest_salle = (g_quest_salle + 1) % 9; change = 2;
        }
        /* SONDE : tant qu'un lieu est ouvert, on demande au moteur, de temps
         * en temps, si la photographie (rang 10) et la fenetre (rang 13)
         * vivent encore -- `0x180171070` rend 1 quand le rang est vide ou
         * l'objet est arrive au bout. Frederic, 2026-09-12 : « les fenetres
         * s'ouvrent mais se referment au bout d'une seconde environ ». */
        if (g_quest_zoom) {
            static const unsigned jalons[] = {2, 15, 30, 60, 90, 150, 300,
                                              600, 900, 0};
            quest_f_fini fini = (quest_f_fini)(g_quest_base + QUEST_RVA_FINI);
            void *ctx2 = *(void **)(g_quest_base + QUEST_RVA_CONTEXTE);
            int j;
            g_quest_trames++;
            for (j = 0; jalons[j]; j++)
                if (g_quest_trames == jalons[j] && ctx2) {
                    char b2[160];
                    _snprintf(b2, sizeof b2,
                              "trame %u : photo finie %d, fenetre finie %d ;"
                              " tour", g_quest_trames,
                              fini(ctx2, QUEST_RANG_ZOOM),
                              fini(ctx2, QUEST_RANG_FENETRE));
                    quest_dire(b2, (long long)g_quest_salle);
                }
        } else {
            g_quest_trames = 0;
        }
        /* Chaque trame : on tient les calques un par un (voir
         * `quest_assurer`). `change` force ceux qui ont change de nom. */
        if (change) {
            g_quest_ms = ms;
            /* change == 2 : c'est GAUCHE ou DROITE, pas une validation */
            if (change == 2) quest_dire("lieu choisi",
                                        (long long)g_quest_salle);
        }
        quest_assurer();
    }
}

/* MESURE DU 2026-09-11 : Core_execute tourne sur un fil (la carte), et
 * Input_isOn est appelee par le MOTEUR sur un autre (17188 contre 20792).
 * Les chargeurs du moteur ne supportent pas d'etre appeles du premier ; on
 * pilote donc le Quest depuis le second, une fois par image au plus.
 *
 * Core_execute depose l'horloge ; Input_isOn la consomme. */
static unsigned g_quest_t0;
static unsigned g_quest_horloge_ms;
static unsigned g_quest_derniere;

static void quest_horloge(unsigned ms, unsigned declencheur)
{
    (void)ms;
    (void)declencheur;    /* la ligne « quest = N » du scenario ne sert plus :
                           * c'est l'etat du jeu qui commande */
    if (!g_quest_t0) g_quest_t0 = GetTickCount();
    g_quest_horloge_ms = GetTickCount() - g_quest_t0;
}

static void quest_tic_moteur(void)
{
    unsigned ms = g_quest_horloge_ms;
    if (g_quest_derniere && ms - g_quest_derniere < 16) return;  /* 1 / image */
    g_quest_derniere = ms ? ms : 1;
    quest_tic(ms);
}
