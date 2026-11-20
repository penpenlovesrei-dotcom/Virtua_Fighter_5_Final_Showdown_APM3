@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LE FILET. Double-cliquez avant et apres avoir touche au patcheur.
rem
rem Trois etages :
rem   1. verifier_lanceurs.py --sans-patch : fins de ligne, caracteres de
rem      controle, fichiers cites par les 83 lanceurs ;
rem   2. controle_quest.py --tout : compile, patche avec la ligne exacte de
rem      quest.cmd, puis mesure dans le binaire produit ;
rem   3. l EMPREINTE : la DLL produite est comparee au dernier etat de
rem      reference, PLAGE PAR PLAGE, et chaque plage dit quel correctif la
rem      revendique. Une plage qui DISPARAIT est un defaut : c est un
rem      correctif qui ne s applique plus.
rem
rem Pourquoi cet etage 3 : la seance du 2026-09-06 a ete perdue parce que la
rem legende du bas et License Challenge logeaient leur caverne a la MEME
rem adresse, et que la legende ecrasait le lancement. Une empreinte globale
rem aurait dit " ca a change " ; celle-ci dit OU.
rem
rem Pour prendre l etat actuel comme reference :
rem   py -3 tools\regression.py --poser --valide --note "ce que Frederic a vu"
rem Le drapeau --valide ne se met que quand il a dit qu il l a VU marcher.
rem
rem Rapport : analysis\regression.txt   Reference : analysis\empreinte_quest.json
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
echo.
echo   ===================================================================
echo    VF5 -- regression
echo   ===================================================================
echo.
py -3 tools\regression.py %*
set RC=%ERRORLEVEL%
echo.
if "%RC%"=="0" (
  echo   RIEN N EST DEFAIT.
) else (
  echo   DEFAUT ^(code %RC%^). Lisez analysis\regression.txt
)
echo.
pause
endlocal
exit /b %RC%
