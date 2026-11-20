@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- CONTROLE DU MODE QUEST, SANS LANCER LE JEU. Double-cliquez.
rem
rem Il fait, dans cet ordre :
rem   1. compile apm.dll ;
rem   2. pose ce qui manque -- planches 2D, 492 libelles, npc_tbl.bin,
rem      la musique, la table des objets de la boutique ;
rem   3. patche le moteur avec la ligne EXACTE de tools\quest.cmd ;
rem   4. MESURE dans le binaire produit que chaque chose y est : les octets
rem      attendus a chaque site patche, la boite aux lettres QUESTBOX, la
rem      disposition de la greffe sans recouvrement, les libelles, la table
rem      des mille rivaux (taille, gros-boutisme, un enregistrement temoin),
rem      la boutique (en-tete QOBJ, nombre d objets, prix non nuls), la
rem      musique, les planches que qwin tnt tnto qdan, le profil.
rem
rem Il S ARRETE AU PREMIER DEFAUT et rend un code non nul.
rem Le rapport complet est ecrit dans analysis\controle_quest.txt.
rem
rem CE QU IL NE DIT PAS : que cela s affiche. Voir tools\sonde_quest.cmd.
rem
rem Il refuse de travailler si vfes.exe tourne.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- controle du mode QUEST
echo   ===================================================================
echo.
py -3 tools\controle_quest.py --tout
set RC=%ERRORLEVEL%
echo.
if "%RC%"=="0" (
  echo   AUCUN DEFAUT. Le rapport : analysis\controle_quest.txt
) else (
  echo   DEFAUT ^(code %RC%^). Le rapport : analysis\controle_quest.txt
)
echo.
pause
endlocal
exit /b %RC%
