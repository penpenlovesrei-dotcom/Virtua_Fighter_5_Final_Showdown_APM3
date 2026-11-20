# hote_apm — un relais, pas un bouchon. Et il ne sert à rien aujourd'hui.

## Le bouchon existe déjà, ailleurs, et il tourne

Avant de toucher à ce dossier : **le bouchon `apm.dll` du projet n'est pas
ici.** Il est produit par `outils/gen_apm_stub.py` (57 exports, ceux que
`vfes.exe` importe), compilé par `outils/construire_stub.cmd`, et il est en
service dans le banc :

    Virtua Fighter 5 FS\VF5RE\runtime\media\vf5fs\apm.dll

`analysis/INSTRUMENTATION.md` §6 et §7 le mesurent : le jeu démarre, affiche
l'écran-titre, et va jusqu'au combat. 12 666 appels au bouchon en 18 secondes,
22 fonctions distinctes, aucun plantage. C'est acquis depuis septembre 2026.

**Ce dossier a été écrit le 4 novembre 2026 sans avoir lu ce qui précède.**
C'est un doublon. Il est gardé pour une seule raison, celle du paragraphe
suivant.

## Ce que le relais fait que le bouchon ne fait pas

Le bouchon **répond à la place** de la borne. Le relais, lui, peut
**journaliser puis sauter vers la VRAIE `apm.dll`** :

    APM_INERTE=0  (défaut)  relais : on note l'appel, puis `jmp` vers la vraie
    APM_INERTE=1            inerte : nos réponses, comme le bouchon

Les 106 points d'entrée sont des tremplins en assembleur
(`gen_table.py` → `apm_tremplins.asm`). On ne connaît pas les signatures ; un
tremplin qui journalise puis `jmp` ne touche à aucune convention d'appel et
rend la valeur de la vraie fonction, quel que soit son type. C'est la seule
façon correcte de relayer une signature inconnue — et c'est ce qui distingue
ce dossier du bouchon, qui doit deviner chaque type de retour.

**La question qui le rendrait utile, et il n'y en a pas d'autre :** un écran
qui se comporte autrement sous le bouchon que sous la vraie DLL. Le relais
donnerait alors la séquence d'appels réelle de la borne, à comparer à celle du
bouchon. Tant que personne n'observe cet écart, ce dossier dort.

## Faute connue dans le mode inerte

`kReponses` rend `Credit_toString` en `const char*`. C'est **faux** :
`INSTRUMENTATION.md` §6 a mesuré qu'il rend un `std::string` **par valeur**
(pointeur de tampon caché en RCX, rendu dans RAX — ABI x64). Le mode relais
n'est pas concerné. Le mode inerte l'est, et la faute est signalée en
commentaire à l'endroit même de la table. Ne pas se servir du mode inerte
d'ici sans la corriger : le bouchon d'`outils/` sait déjà le faire.

## Si on s'en sert

    # par PowerShell, chemin complet (via Bash, vcvars64 se bloque)
    hote_apm\build.cmd            # régénère la table depuis la VRAIE apm.dll, compile
    python -I hote_apm\essai_instrument.py   # valide sans lancer le jeu
    outils\monter_banc.cmd        # monte FS APM3\banc (liens durs + jonction)

`banc/` est un **second** banc. Le vrai est dans `VF5RE/runtime/media/vf5fs`.
Deux bancs divergent : ne pas mesurer dans l'un en croyant lire l'autre.
