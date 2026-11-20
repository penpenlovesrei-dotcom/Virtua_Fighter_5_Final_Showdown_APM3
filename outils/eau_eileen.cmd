@echo off
rem ---------------------------------------------------------------------------
rem L'EAU D'EILEEN, variante VF5 (skb, indice 72).
rem
rem Ce qui a ete MESURE le 2026-10-15 :
rem
rem  . le disque du ring EST l'objet `stgslk_water_ring` (essai : tout l'objset
rem    peint en magenta sauf lui, textures coupees -> le disque devient raye) ;
rem  . ses deux textures de ver.B sont DEJA de l'eau : 12674 bleu-gris sombre
rem    (le fond) et 12675 blanc bleute (le haut-fond). Celles de VF5 R, 9205 et
rem    9206, sont la meme eau sombre MAIS un haut-fond BEIGE : les porter rend
rem    le ring plus sableux, pas moins. On garde donc celles de ver.B ;
rem  . le grand plan `stgslk_eff_water` de ver.B n'a que DEUX emplacements de
rem    texture ; celui de FS comme celui de R en ont trois, le troisieme etant
rem    le cube d'environnement `MIZU` (l'eau). On porte celui de R ;
rem  . et c'est l'ECLAIRAGE qui faisait lire le tout comme du sable :
rem        couleur du brouillard   skb 1,30 1,20 1,00   sk5 0,10 0,30 0,70
rem        densite                     0,60                 0,30
rem        ambiante                    0,70                 0,30
rem    On pose les six fichiers d'eclairage de sk5.
rem
rem Tout est reversible : l'archive et les six fichiers sont sauves en
rem `*.avant_eau`.
rem
rem    eau_eileen.cmd              poser
rem    eau_eileen.cmd --controle   tout verifier sans rien ecrire
rem    eau_eileen.cmd --rendre     tout remettre comme avant
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
py -3 tools\eau_eileen.py %*
echo.
pause
