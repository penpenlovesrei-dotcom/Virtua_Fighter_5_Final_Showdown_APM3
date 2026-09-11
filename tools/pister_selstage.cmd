@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- QUEL CODE PORTE CHAQUE BOUTON SUR L'ECRAN STAGE SELECT
rem
rem Double-cliquez, et PATIENTEZ : le demarrage est long. Le clavier reste a
rem vous -- allez jusqu'a OFFLINE VERSUS puis STAGE SELECT.
rem
rem LA, pressez UN bouton a la fois, en laissant une seconde entre deux :
rem
rem     fleches = directions      Entree = VALIDER       W = ANNULER
rem     X C V   = croix rond triangle   ESPACE = SELECT  T Y U = L1 R1 R2
rem
rem POURQUOI CETTE MESURE
rem
rem   TaskSelStage::update (0x18017425E) n'interroge pas la manette : il lit un
rem   tableau d'etats range dans l'objet, par deux fonctions triviales --
rem
rem     0x1801724A0(base, code) -> octet [(code + 2) * 0x40 + base]
rem     0x180172450(base, code) -> vrai si [rec+0x28] == 6 ou [rec+0x20] == 6
rem
rem   La validation interroge les codes 0 et 1. Les autres ne sont pas connus,
rem   et il en faut UN : celui de SELECT, pour faire defiler les variantes du
rem   decor sous le curseur.
rem
rem   L'outil releve les seize enregistrements (codes -2 a 13) pendant que vous
rem   jouez, et dit lequel bouge a chaque appui. Le code qui ne bouge QUE
rem   quand vous pressez ESPACE est celui de SELECT.
rem
rem   Journal complet : analysis\pister_selstage.txt
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\pister_selstage.py --secondes 300
echo.
pause
endlocal
