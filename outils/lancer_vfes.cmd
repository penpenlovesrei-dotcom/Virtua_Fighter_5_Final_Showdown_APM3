@echo off
rem ---------------------------------------------------------------------------
rem Lance Virtua Fighter 5 Final Showdown (vfes.exe, build APM3 du dump APM3_US).
rem
rem Fonctionne grace au apm.dll de substitution : sans lui le jeu leve
rem amdaemon::Exception et s'arrete. Voir analysis/INSTRUMENTATION.md section 6.
rem
rem La copie de travail est dans VF5RE\runtime : le dump reste en lecture seule
rem (vf5fs_data.par est un lien dur, vf5fs_media une jonction).
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0..\runtime\media\vf5fs"

if not exist vfes.exe (
  echo ERREUR : vfes.exe introuvable dans %CD%
  echo La copie de travail n'existe pas. Voir analysis/INSTRUMENTATION.md section 1.
  pause
  exit /b 1
)
if not exist apm.dll (
  echo ERREUR : apm.dll manquant. Lancez d'abord construire_stub.cmd
  pause
  exit /b 1
)

echo Dossier  : %CD%
echo apm.dll  : stub de substitution (la vraie est sous apm.reelle.dll)
echo.
echo Lancement... la fenetre s'appelle "Virtua Fighter 5 FS (PXD/64bit)".
echo Fermez-la pour arreter le jeu.
echo.
rem Chemins systeme complets : sinon timeout et findstr peuvent etre captes par
rem les outils Unix d'un Git Bash present dans le PATH.
start "" vfes.exe
"%SystemRoot%\System32\timeout.exe" /t 6 /nobreak >nul 2>&1
"%SystemRoot%\System32\tasklist.exe" /fi "imagename eq vfes.exe" /nh | "%SystemRoot%\System32\findstr.exe" /i vfes >nul
if errorlevel 1 (
  echo Le jeu s'est arrete. Relancez avec lancer_vfes_debug.cmd pour voir pourquoi.
) else (
  echo Le jeu tourne.
)
echo.
pause
endlocal
