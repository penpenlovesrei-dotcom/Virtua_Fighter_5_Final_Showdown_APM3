@echo off
rem ---------------------------------------------------------------------------
rem SFD -> USM : convertit les films Sofdec1 en Sofdec2, SANS REENCODER
rem
rem Deux facons de s'en servir :
rem
rem   . GLISSEZ un ou plusieurs .sfd sur ce fichier : chaque film est converti
rem     a cote de lui, en .usm ;
rem   . ou DOUBLE-CLIQUEZ : tous les .sfd des dumps connus sont convertis dans
rem     extracted\usm\.
rem
rem POURQUOI IL N'Y A AUCUNE PERTE
rem
rem   Un .sfd est un flux de programme MPEG : sa video est deja du MPEG-1 et
rem   son son est deja de l'ADX. Sofdec2 sait lire exactement les memes deux
rem   choses -- VIDEO_HDRINFO.mpeg_codec = 1 (Sofdec.Prime) est du MPEG-1, et
rem   AUDIO_HDRINFO.audio_codec = 2 est de l'ADX. Verifie sur vf5adv.usm du
rem   jeu : son flux video ne contient AUCUN code d'extension MPEG-2.
rem
rem   L'outil ne fait donc que REMBALLER : il demultiplexe le MPEG-PS, decoupe
rem   la video image par image et l'ADX par blocs de 50, puis ecrit les
rem   morceaux Sofdec2 autour. Les octets d'image et de son ne sont pas
rem   touches.
rem
rem   PREUVE, faite sur vf5moe.sfd : le flux video extrait du .usm produit a la
rem   MEME EMPREINTE MD5 que celui extrait du .sfd d'origine
rem   (4d9bef4b0a77b70c7cef10e5cdbed4bf, 52 209 294 octets), et le flux ADX
rem   aussi (f02d829d80f6224176f26cc35e219f9f). Pas un octet de perdu.
rem
rem   C'est la difference avec le Scaleform Video Encoder du dossier
rem   " MP4 to USM " : medianoche.exe DECODE puis REENCODE en H.264. Il donne
rem   un USM lisible, mais il repasse par la compression.
rem
rem LE MULTIPISTE AUDIO
rem
rem   Un .sfd peut porter plusieurs sons. vf5verBadv.sfd en a deux : un ADX
rem   simple (la piste principale) et un conteneur AIX, le multipiste de CRI,
rem   ou trois ADX sont entrelaces par morceaux AIXP etiquetes du numero de
rem   leur flux. L'outil deplie l'AIX et donne a chaque flux sa propre voie
rem   @SFA -- ce film sort en QUATRE voies audio, les quatre verifiees octet
rem   pour octet. --pistes N limite le nombre de voies ecrites.
rem
rem POUR VERIFIER UN FILM PRODUIT
rem     py -3 tools\usm_mux.py --verifier <film.usm>
rem     py -3 tools\usm.py info <film.usm>
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
if not "%~1"=="" goto glisses

echo Aucun fichier glisse : conversion de tous les .sfd des dumps connus.
echo.
if not exist extracted\usm mkdir extracted\usm
for %%D in (
  "extracted\sfd_x360"
  "C:\Users\frede\Desktop\VF5 FS DECOMP\APM3_FS\rom\movie"
) do (
  if exist "%%~D" (
    for %%F in ("%%~D\*.sfd") do (
      echo === %%~nxF
      py -3 tools\usm_mux.py "%%~F" "extracted\usm\%%~nF.usm"
      echo.
    )
  )
)
goto fin

:glisses
:boucle
if "%~1"=="" goto fin
echo === %~nx1
py -3 tools\usm_mux.py "%~1" "%~dpn1.usm"
echo.
shift
goto boucle

:fin
echo.
echo Termine.
pause
endlocal
