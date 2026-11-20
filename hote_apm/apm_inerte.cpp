// ===========================================================================
//  apm_inerte.cpp : un apm.dll de remplacement, pour mesurer et pour mentir.
//
//  CE QU'EST apm.dll. La bibliotheque de la borne d'arcade SEGA. Ses noms le
//  disent en clair : `AllnetAuth_isGood`, `AllnetAuth_getLocationId`,
//  `AllnetAccounting_beginPlay`, `Credit_isFreePlay`, `Aime_isReaderDetected`,
//  `APMv3SystemReboot`, et tout l'espace de noms `amdaemon::ipc::*`. Elle
//  dialogue par IPC avec amdaemon, le demon systeme ALL.Net. Il n'y a pas
//  d'amdaemon sur cette machine, et aucun `systemconfig.json` dans l'arbre.
//
//  `vfes.exe` l'importe STATIQUEMENT et en consomme 57 des 106 fonctions.
//  Sans elle, l'executable ne demarre pas du tout.
//
//  DEUX MODES, ET LE DEFAUT EST LE TEMOIN.
//
//    APM_INERTE=0 (defaut) : on RELAIE vers la vraie apm.dll, chargee par
//        chemin complet. On ne change rien au comportement, on ne fait que
//        journaliser. C'est le temoin, et c'est lui qui repondra a la seule
//        question du premier essai : apm.dll bloque-t-elle au CHARGEMENT ou
//        seulement a l'AUTHENTIFICATION ? Sans ce mode, un << ca ne demarre
//        pas >> ne designerait personne ([[hypothese-avec-temoin]]).
//        Il valide aussi l'instrument sur des reponses connues
//        ([[proxy-dll-reproduit-la-table-entiere]]).
//
//    APM_INERTE=1 : on repond nous-memes. Chaque reponse est un MENSONGE
//        DELIBERE, inscrite dans la table `kReponses` avec sa raison, et
//        journalisee comme telle. Un bouchon fidele peut tuer -- le vrai
//        `GetStatus` rendait 7 devant notre poignee nulle, et 7 etait
//        terminal ([[bouchon-fidele-peut-tuer]]). Donc on ment sciemment, et
//        on l'ecrit.
//
//  CE QUE CETTE DLL NE FAIT PAS. Elle ne contourne aucune protection du jeu :
//  apm.dll n'en est pas une, c'est une couche materielle de borne. Elle ne
//  remplace pas la vraie, qui reste intacte dans SOURCES/lib. Elle ne part
//  dans aucun paquet (analysis/BASE_LEGALE.md).
//
//  LES TREMPLINS. Les 106 points d'entree sont en assembleur, dans
//  apm_tremplins.asm, genere par gen_table.py. On ne connait pas les
//  signatures ; un tremplin qui journalise puis `jmp` ne touche a aucune
//  convention d'appel et rend la valeur de la cible quel qu'en soit le type.
//  Voir l'en-tete de gen_table.py pour le detail du cadre de pile.
// ===========================================================================
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <stdint.h>

#include "apm_noms.inc"      // kNoms[], kNombre

// ---------------------------------------------------------------- le journal
//
// Anneau sans verrou : les tremplins tirent depuis n'importe quel fil, et un
// verrou sur le chemin chaud transformerait l'instrument en cause de panne
// ([[instrument-cause-la-faute]]). On ecrit dans un tableau fixe, un fil de
// vidange recopie vers le fichier.
struct Note {
    uint32_t idx;
    uint32_t fil;
    uint64_t a, b, c, d;
};
static const uint64_t kNotes  = 1ull << 18;      // 8 Mo
static const uint64_t kMasque = kNotes - 1;
static Note  g_notes[kNotes];
static volatile LONG64 g_nNotes = 0;

// Un compteur par fonction. Compter en grepant le journal donne un chiffre
// faux des que le journal est plafonne ([[les-journaux-du-banc-sont-plafonnes]]).
static volatile LONG g_compte[256];

static HANDLE g_log      = INVALID_HANDLE_VALUE;
static long   g_detail   = 8;        // lignes detaillees par fonction
static bool   g_inerte   = false;    // defaut : on relaie
static bool   g_relaisOk = false;    // la vraie DLL a-t-elle ete chargee ?
static HMODULE g_vraieDll = nullptr;
static void*  g_vraies[256];
static char   g_cheminVraie[MAX_PATH] = {0};

static void EcrireF(const char* fmt, ...) {
    if (g_log == INVALID_HANDLE_VALUE) return;
    char t[2048];
    va_list ap;
    va_start(ap, fmt);
    const int n = _vsnprintf_s(t, sizeof(t), _TRUNCATE, fmt, ap);
    va_end(ap);
    if (n <= 0) return;
    DWORD ecrit = 0;
    WriteFile(g_log, t, (DWORD)n, &ecrit, nullptr);
}

// ------------------------------------------------------- les reponses inertes
//
// Chaque entree est une DECISION, pas une valeur par defaut. `chaine` non
// nulle gagne sur `valeur` : on rend le pointeur. Pourquoi des chaines pour
// tout ce qui ressemble a un nom ou un identifiant : si la fonction rend en
// realite un `const char*`, rendre 0 fait dereferencer l'adresse nulle chez
// l'appelant ; si elle rend un entier, rendre un pointeur ne donne qu'un
// grand nombre. Le pointeur est donc le choix SUR dans les deux cas, et
// l'inverse ne l'est pas.
struct Reponse {
    const char* nom;
    uint64_t    valeur;
    const char* chaine;
    const char* pourquoi;
};

static const Reponse kReponses[] = {
    // --- l'authentification reseau : on affirme que tout va bien
    { "AllnetAuth_isGood",                 1, nullptr, "MENSONGE : pas d'amdaemon, on declare l'auth bonne" },
    { "AllnetAuth_isDevelop",              1, nullptr, "MENSONGE : mode developpement, pour eviter les controles de site" },
    { "AllnetAuth_getCountryCode",         0, "JPN",   "valeur de facade" },
    { "AllnetAuth_getRegionCode",          0, "1",     "valeur de facade" },
    { "AllnetAuth_getLocationId",          0, "0",     "valeur de facade" },
    { "AllnetAuth_getLocationName",        0, "BANC",  "valeur de facade" },
    { "AllnetAuth_getLocationNickname",    0, "BANC",  "valeur de facade" },
    { "AllnetAuth_getRegionName",          0, "BANC",  "valeur de facade" },
    { "AllnetAuth_getRegionNamePartCount", 0, nullptr, "zero partie" },
    { "AllnetAuth_getLocationNicknamePartCount", 0, nullptr, "zero partie" },
    { "AllnetAuth_getAbaasGsServerName",   0, "",      "chaine vide : aucun serveur" },
    { "AllnetAuth_getAbaasLinkServerName", 0, "",      "chaine vide : aucun serveur" },
    { "AllnetAccounting_beginPlay",        0, nullptr, "comptabilite muette" },
    { "AllnetAccounting_endPlay",          0, nullptr, "comptabilite muette" },

    // --- le monnayeur : partie gratuite, credit toujours suffisant
    { "Credit_isFreePlay",                 1, nullptr, "MENSONGE : partie gratuite, il n'y a pas de monnayeur" },
    { "Credit_isGameCostEnough",           1, nullptr, "MENSONGE : credit toujours suffisant" },
    { "Credit_isZero",                     0, nullptr, "MENSONGE : le credit n'est jamais a zero" },
    { "Credit_getCredit",                 99, nullptr, "MENSONGE : 99 credits" },
    { "Credit_getRemain",                 99, nullptr, "MENSONGE : 99 credits restants" },
    { "Credit_getAddableCoin",             0, nullptr, "aucune piece ajoutable" },
    { "Credit_getCoinToCredit",            1, nullptr, "une piece = un credit" },
    // FAUTE CONNUE, NON CORRIGEE, ET C'EST VOLONTAIRE DE L'ECRIRE ICI.
    // analysis/INSTRUMENTATION.md section 6 a mesure que Credit_toString rend
    // un std::string PAR VALEUR : l'appelant passe un pointeur de tampon cache
    // en RCX et attend ce meme pointeur dans RAX, le tampon construit. Rendre
    // un const char* fait lire un litteral de 9 octets comme un objet.
    // Le mode RELAIS n'est pas concerne -- le tremplin saute vers la vraie
    // fonction sans rien interpreter. Le mode INERTE, lui, est FAUX sur cette
    // entree, et le restera jusqu'a ce qu'on construise vraiment l'objet.
    { "Credit_toString",                   0, "FREE PLAY", "FAUX : rend un std::string par valeur, voir ci-dessus" },
    { "Credit_payGameCost",                1, nullptr, "le paiement reussit toujours" },

    // --- le lecteur de carte Aime : absent, et qui ne fait jamais attendre
    { "Aime_isReaderDetected",             0, nullptr, "pas de lecteur de carte" },
    { "Aime_isDBAlive",                    0, nullptr, "pas de base de cartes" },
    { "Aime_isBusy",                       0, nullptr, "jamais occupe : ne pas faire attendre la boucle" },
    { "Aime_hasError",                     0, nullptr, "jamais en erreur" },
    { "Aime_hasResult",                    0, nullptr, "jamais de resultat" },
    { "Aime_hasConfirm",                   0, nullptr, "jamais de confirmation" },
    { "Aime_isMobile",                     0, nullptr, "pas de telephone" },
    { "Aime_getErrorCategory",             0, nullptr, "aucune categorie d'erreur" },
    { "Aime_getAimeId",                    0, "",      "chaine vide : pas de carte" },
    { "Aime_getAccessCode",                0, "",      "chaine vide : pas de carte" },

    // --- l'etat de la borne
    { "Core_isExitNeeded",                 0, nullptr, "ne jamais demander la sortie" },
    { "Error_isOccurred",                  0, nullptr, "aucune erreur materielle" },
    { "Sequence_isTest",                   0, nullptr, "pas le menu de test de la borne" },
    { "Sequence_isPlaying",                0, nullptr, "pas de partie comptabilisee en cours" },
    { "Sequence_isAccountingPlaying",      0, nullptr, "idem" },
    { "Backup_isSetupSucceeded",           1, nullptr, "MENSONGE : la sauvegarde est prete" },
    { "Backup_getRecordStatus",            0, nullptr, "aucun enregistrement" },
    { "Backup_setupRecords",               1, nullptr, "la preparation reussit" },
    { "Backup_saveRecord",                 1, nullptr, "la sauvegarde reussit" },
    { "Emoney_isOpenMainWindow",           0, nullptr, "pas de fenetre de paiement" },

    // --- l'identite du systeme
    { "System_isDevelop",                  1, nullptr, "MENSONGE : machine de developpement" },
    { "System_getGameId",                  0, "SDHP",  "l'identifiant que les cles de SOURCES/key suggerent" },
    { "System_getGameVersion",             0, "1.00",  "valeur de facade" },
    { "System_getBoardId",                 0, "BANC0000",       "valeur de facade" },
    { "System_getKeychipId",               0, "A00E-00000000",  "valeur de facade" },
    { "System_getRegionCode",              1, nullptr, "valeur de facade" },
    { "System_getAppRootPath",             0, ".",     "le dossier courant : le banc tourne dedans" },

    // --- les reglages de borne
    { "ApmSystemSetting_getFixedTitle",       0, nullptr, "pas de titre impose" },
    { "ApmSystemSetting_getAdvertizeSound",   1, nullptr, "son d'attraction autorise" },
    { "ApmSystemSetting_getMatchingGroup",    0, nullptr, "aucun groupe d'appariement" },
    { "ApmSystemSetting_getTimeToClosingTime", 0x7FFFFFFF, nullptr, "jamais l'heure de fermeture" },
    { "ApmSystemSetting_getClosingTimes",     0, nullptr, "aucune fermeture programmee" },
    { "ApmSystemSetting_getEmoneySetting",    0, nullptr, "pas de paiement electronique" },
    { "ApmSystemSetting_getGamePadSetting",   0, nullptr, "reglage par defaut" },
    { "ApmSystemSetting_getUiSetting",        0, nullptr, "reglage par defaut" },

    // --- les entrees. Rien n'est presse ici : si la manette doit etre vue,
    //     le journal du mode relais le dira avant qu'on decide.
    { "Input_isGamepadDetect",             0, nullptr, "INCERTAIN : aucune manette annoncee ; a relire au premier journal" },
    { "Input_isOn",                        0, nullptr, "aucun bouton tenu" },
    { "Input_isOnNow",                     0, nullptr, "aucun appui" },
    { "Input_isOffNow",                    0, nullptr, "aucun relachement" },
    { "Input_isFlipNow",                   0, nullptr, "aucun changement" },
    { "Input_isOpenPewviewWindow",         0, nullptr, "pas de fenetre de previsualisation" },
    { "apmGamepadIsDetected",              0, nullptr, "INCERTAIN : idem Input_isGamepadDetect" },
    { "apmGamepadIsXInputDevice",          0, nullptr, "pas de peripherique XInput" },
    { "apmGamepadUpdate",                  0, nullptr, "rien a mettre a jour" },

    // --- le reseau
    { "NetworkProperty_getAddressString",  0, "0.0.0.0", "pas d'adresse" },
    { "NetworkProperty_getAddressValue",   0, nullptr, "pas d'adresse" },
};

// Resolu a l'initialisation : indice de fonction -> reponse, ou nullptr.
static const Reponse* g_rep[256];

// Le fil courant vient d'etre note par ApmNoter : la reponse inerte a besoin
// de savoir POUR QUI elle repond, et le tremplin ne peut pas le lui passer
// sans toucher aux arguments de l'appelant.
static __declspec(thread) int t_idx = -1;

// ------------------------------------------------------- l'unique repondeur
//
// Aucun argument declare, un seul retour entier : l'appelant a pose ses
// arguments dans les registres et nettoiera sa pile lui-meme. Vrai pour toute
// fonction qui rend un entier ou un pointeur -- et le journal nomme celles
// pour lesquelles ca pourrait ne pas l'etre.
extern "C" uint64_t RendInerte() {
    const int i = t_idx;
    if (i < 0 || i >= kNombre) return 0;
    const Reponse* r = g_rep[i];
    if (!r) return 0;
    return r->chaine ? (uint64_t)(uintptr_t)r->chaine : r->valeur;
}

// ----------------------------------------------------------- initialisation
//
// Paresseuse : charger une DLL depuis DllMain prend le verrou du chargeur et
// peut bloquer. On le fait au premier appel reel.
static volatile LONG g_init = 0;

static void Ouvrir() {
    char chemin[MAX_PATH * 2];
    DWORD n = GetEnvironmentVariableA("APM_JOURNAL", chemin, sizeof(chemin));
    if (n == 0 || n >= sizeof(chemin)) {
        char dossier[MAX_PATH];
        if (!GetCurrentDirectoryA(sizeof(dossier), dossier)) dossier[0] = 0;
        _snprintf_s(chemin, sizeof(chemin), _TRUNCATE,
                    "%s\\apm_journal_%lu.txt", dossier,
                    (unsigned long)GetCurrentProcessId());
    }
    g_log = CreateFileA(chemin, GENERIC_WRITE, FILE_SHARE_READ, nullptr,
                        CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);
}

static void Charger() {
    // Chemin de la vraie DLL. Jamais "apm.dll" tout court : ce nom, c'est
    // NOUS, et on se chargerait soi-meme.
    DWORD n = GetEnvironmentVariableA("APM_VRAIE", g_cheminVraie,
                                      sizeof(g_cheminVraie));
    if (n == 0 || n >= sizeof(g_cheminVraie)) {
        _snprintf_s(g_cheminVraie, sizeof(g_cheminVraie), _TRUNCATE,
                    "%s", "..\\..\\SOURCES\\lib\\apm.dll");
    }
    g_vraieDll = LoadLibraryA(g_cheminVraie);
    if (!g_vraieDll) {
        EcrireF("  ECHEC : la vraie apm.dll n'a pas pu etre chargee depuis\n"
                "          %s   (GetLastError=%lu)\n"
                "  >>> BASCULE FORCEE EN MODE INERTE. Le temoin n'a pas eu\n"
                "      lieu : ne pas lire ce run comme un relais.\n",
                g_cheminVraie, (unsigned long)GetLastError());
        g_inerte = true;
        return;
    }
    long manquants = 0;
    for (int i = 0; i < kNombre; ++i) {
        g_vraies[i] = (void*)GetProcAddress(g_vraieDll, kNoms[i]);
        if (!g_vraies[i]) { ++manquants; EcrireF("  ABSENTE de la vraie DLL : %s\n", kNoms[i]); }
    }
    g_relaisOk = (manquants == 0);
    EcrireF("  vraie apm.dll chargee a %p depuis %s   (%d/%d resolues)\n",
            (void*)g_vraieDll, g_cheminVraie, kNombre - manquants, kNombre);
}

static DWORD WINAPI FilVidange(LPVOID);
static void Vidanger();

static void Initialiser() {
    if (InterlockedCompareExchange(&g_init, 1, 0) != 0) {
        while (g_init < 2) Sleep(0);          // un autre fil s'en charge
        return;
    }
    Ouvrir();

    char v[32] = {0};
    GetEnvironmentVariableA("APM_INERTE", v, sizeof(v));
    g_inerte = (v[0] == '1');
    char d[32] = {0};
    if (GetEnvironmentVariableA("APM_DETAIL", d, sizeof(d)) > 0)
        g_detail = atol(d);

    EcrireF("apm_inerte -- apm.dll de remplacement, %d exports\n", kNombre);
    EcrireF("  mode : %s   (APM_INERTE=1 pour inerte, 0 ou absent pour relais)\n",
            g_inerte ? "INERTE -- nos reponses" : "RELAIS -- la vraie DLL, journalisee");
    EcrireF("  detail : %ld lignes par fonction, puis seulement le compteur\n",
            g_detail);

    // La table de reponses, resolue par nom. Ce qui n'y figure pas rendra
    // zero, et le bilan final le dira nom par nom : une decision non prise
    // doit se voir ([[hypothese-ecrite-comme-mesure]]).
    long decidees = 0;
    for (int i = 0; i < kNombre; ++i) {
        g_rep[i] = nullptr;
        for (size_t j = 0; j < sizeof(kReponses) / sizeof(kReponses[0]); ++j) {
            if (lstrcmpA(kNoms[i], kReponses[j].nom) == 0) {
                g_rep[i] = &kReponses[j];
                ++decidees;
                break;
            }
        }
    }
    EcrireF("  reponses inertes decidees : %ld sur %d ; les autres rendront 0\n",
            decidees, kNombre);

    if (!g_inerte) Charger();
    FlushFileBuffers(g_log);

    CreateThread(nullptr, 0, &FilVidange, nullptr, 0, nullptr);
    InterlockedExchange(&g_init, 2);
}

// ------------------------------------------------------------- les tremplins
//
// Appelee par le tramway, AVANT la cible. On note ce que le tremplin
// TRANSMET -- les quatre registres d'arguments tels qu'ils arrivent -- et pas
// une interpretation : le thunk contient souvent deja un filtre, et noter ce
// qu'on croit avoir recu masque ce qui passe vraiment
// ([[instrument-cause-la-faute]]).
extern "C" void ApmNoter(int idx, uint64_t a, uint64_t b, uint64_t c,
                         uint64_t d) {
    if (g_init != 2) Initialiser();
    if (idx < 0 || idx >= kNombre) return;
    t_idx = idx;
    const LONG n = InterlockedIncrement(&g_compte[idx]);
    const uint64_t k = (uint64_t)InterlockedIncrement64(&g_nNotes) - 1;
    if (k < kNotes && n <= g_detail) {
        Note* p = &g_notes[k & kMasque];
        p->idx = (uint32_t)idx;
        p->fil = GetCurrentThreadId();
        p->a = a; p->b = b; p->c = c; p->d = d;
    }
}

extern "C" void* ApmCible(int idx) {
    if (g_init != 2) Initialiser();
    if (idx < 0 || idx >= kNombre) return (void*)&RendInerte;
    if (!g_inerte && g_vraies[idx]) return g_vraies[idx];
    return (void*)&RendInerte;
}

// ---------------------------------------------------------------- la vidange
static volatile LONG64 g_vidangees = 0;

static void Vidanger() {
    const LONG64 fin = g_nNotes;
    LONG64 i = g_vidangees;
    if (i == 0 && fin > 0)
        EcrireF("\n=== APPELS, DANS L'ORDRE (les %ld premiers de chaque"
                " fonction) ===\n", g_detail);
    for (; i < fin && i < (LONG64)kNotes; ++i) {
        const Note* p = &g_notes[i & kMasque];
        if (p->idx >= (uint32_t)kNombre) continue;
        EcrireF("  [%s] fil=%lu  rcx=0x%llX rdx=0x%llX r8=0x%llX r9=0x%llX\n",
                kNoms[p->idx], (unsigned long)p->fil,
                (unsigned long long)p->a, (unsigned long long)p->b,
                (unsigned long long)p->c, (unsigned long long)p->d);
    }
    g_vidangees = i;
    if (g_log != INVALID_HANDLE_VALUE) FlushFileBuffers(g_log);
}

static DWORD WINAPI FilVidange(LPVOID) {
    // Une premiere vidange tot : si le processus meurt a la seconde 3, un
    // intervalle de 20 s n'aurait rien ecrit
    // ([[fenetre-de-sonde-est-un-temps]]).
    Sleep(2000);
    for (;;) { Vidanger(); Sleep(5000); }
}

static void Bilan() {
    Vidanger();
    EcrireF("\n=== BILAN : COMBIEN DE FOIS, ET CE QU'ON A REPONDU ===\n");
    EcrireF("  mode : %s%s\n",
            g_inerte ? "INERTE" : "RELAIS",
            (!g_inerte && !g_relaisOk)
                ? "  (ATTENTION : des fonctions n'ont pas ete resolues)" : "");
    long appelees = 0;
    for (int i = 0; i < kNombre; ++i) {
        const LONG n = g_compte[i];
        if (n == 0) continue;
        ++appelees;
        const Reponse* r = g_rep[i];
        if (g_inerte) {
            char rep[64];
            if (r && r->chaine) _snprintf_s(rep, sizeof(rep), _TRUNCATE, "\"%s\"", r->chaine);
            else                _snprintf_s(rep, sizeof(rep), _TRUNCATE, "%llu",
                                            (unsigned long long)(r ? r->valeur : 0));
            EcrireF("  %-42s %6ld appels   -> %-14s  %s\n", kNoms[i], n, rep,
                    r ? r->pourquoi : "AUCUNE DECISION PRISE : zero par defaut");
        } else {
            EcrireF("  %-42s %6ld appels   -> la vraie DLL\n", kNoms[i], n);
        }
    }
    EcrireF("  >>> %ld fonctions sur %d ont ete appelees ; les %d autres,"
            " jamais.\n", appelees, kNombre, kNombre - appelees);
    EcrireF("  >>> un zero ici veut dire << jamais appelee >>, pas << sans"
            " effet >> ([[absence-de-resultat-nest-pas-preuve]]).\n");
    if (g_log != INVALID_HANDLE_VALUE) FlushFileBuffers(g_log);
}

BOOL WINAPI DllMain(HINSTANCE, DWORD raison, LPVOID) {
    // Rien de lourd ici : pas de LoadLibrary, pas de fil. Le verrou du
    // chargeur est pris, et l'instrument ne doit pas pouvoir tuer son sujet.
    if (raison == DLL_PROCESS_DETACH) Bilan();
    return TRUE;
}
