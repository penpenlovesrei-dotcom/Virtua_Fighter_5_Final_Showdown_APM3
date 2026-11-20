@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- LA MESURE DES ENTREES. Double-cliquez. Rien n est patche.
rem
rem Elle balaie le .origine (jamais la DLL patchee) et imprime :
rem   1. TOUS les codes que le moteur demande au stub apm.dll, par
rem      Input_isOn (+0x158) et Input_isOnNow (+0x160) -- donc quels codes
rem      des 32 creneaux sont REELLEMENT libres ;
rem   2. QUI lit quel bit du masque arcade : 121 sites, 36 fonctions, et
rem      nommement les porteurs des bits 8, 10, 11 et 20 a 23, ceux que
rem      0x180243ED0 ne remplit pas ;
rem   3. toute autre reference a l etat d entrees 0x180751040 ;
rem   4. les endroits de 0x180243ED0 ou un detour de cinq octets n avalerait
rem      ni une cible de saut ni une frontiere d instruction.
rem
rem CE QU ELLE A ETABLI LE 2026-09-30, et qui corrige le dossier :
rem   . VALIDER = Input_isOnNow(7) = ENTREE, ANNULER = Input_isOnNow(8) = W.
rem     Ni l un ni l autre ne passe par le masque arcade.
rem   . Les bits 8 et 11 de l ecran de personnalisation sont sa CAMERA.
rem   . Le code 15 n est PAS libre (0x18021490F). Les libres : 16, 17, 31.
rem
rem Le detail ecrit : analysis\customize_0x299.md section 3.
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
py -3 tools\boutons_terminal.py %*
echo.
pause
endlocal
