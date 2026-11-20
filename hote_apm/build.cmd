@echo off
rem ===========================================================================
rem  build.cmd : compile notre apm.dll de remplacement.
rem
rem  A LANCER PAR POWERSHELL, PAR CHEMIN COMPLET. Via Bash, l'appel a
rem  vcvars64 se bloque -- regle du banc, quatre fois verifiee.
rem
rem  Trois etapes, et on verifie le code de retour de CHACUNE : une etape
rem  ignoree a deja aveugle huit mesures sur dix.
rem    1. gen_table.py relit la VRAIE apm.dll et regenere la table d'exports,
rem       les tremplins et les noms. On ne recopie jamais une table a la main.
rem    2. ml64 assemble les 106 tremplins.
rem    3. cl compile le journal et lie le tout avec le .def genere.
rem
rem  La sortie s'appelle apm.dll parce que vfes.exe l'importe sous ce nom.
rem  Elle est deposee dans .\sortie\, PAS dans SOURCES/lib : la vraie DLL
rem  reste intacte, c'est la matiere premiere.
rem ===========================================================================
setlocal

set "ICI=%~dp0"
set "VCVARS=C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"
set "VRAIE=%ICI%..\..\SOURCES\lib\apm.dll"
set "SORTIE=%ICI%sortie"

if not exist "%VCVARS%" ( echo ECHEC : vcvars64.bat introuvable : "%VCVARS%" & exit /b 1 )
if not exist "%VRAIE%"  ( echo ECHEC : la vraie apm.dll est introuvable : "%VRAIE%" & exit /b 1 )

cd /d "%ICI%"
if not exist "%SORTIE%" mkdir "%SORTIE%"

echo [1/3] Relecture de la vraie table d'exports...
python -I "%ICI%gen_table.py" "%VRAIE%"
if errorlevel 1 ( echo ECHEC : gen_table.py & exit /b 1 )
if not exist "%ICI%apm_inerte.def"     ( echo ECHEC : .def non genere & exit /b 1 )
if not exist "%ICI%apm_tremplins.asm"  ( echo ECHEC : .asm non genere & exit /b 1 )
if not exist "%ICI%apm_noms.inc"       ( echo ECHEC : .inc non genere & exit /b 1 )

call "%VCVARS%" >nul
if errorlevel 1 ( echo ECHEC : vcvars64 & exit /b 1 )

echo [2/3] Assemblage des tremplins...
ml64 /nologo /c /Fo"%SORTIE%\apm_tremplins.obj" "%ICI%apm_tremplins.asm"
if errorlevel 1 ( echo ECHEC : ml64 & exit /b 1 )

echo [3/3] Compilation et liaison...
cl /nologo /std:c++20 /EHsc /O2 /W3 /LD ^
   /Fo"%SORTIE%\\" /Fd"%SORTIE%\\" ^
   /Fe:"%SORTIE%\apm.dll" ^
   "%ICI%apm_inerte.cpp" "%SORTIE%\apm_tremplins.obj" ^
   /link /DEF:"%ICI%apm_inerte.def" /SUBSYSTEM:WINDOWS
if errorlevel 1 ( echo ECHEC DE LIAISON & exit /b 1 )

if not exist "%SORTIE%\apm.dll" ( echo ECHEC : apm.dll absente apres liaison & exit /b 1 )

echo.
echo === produit ===
dir /b "%SORTIE%\apm.dll"
for %%F in ("%SORTIE%\apm.dll") do echo     %%~zF octets
echo.
echo Controle : la table produite doit compter 106 exports.
echo Verification par monter_banc.cmd, qui relit les deux tables et les compare.
endlocal
