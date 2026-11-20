@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- POURQUOI LE NOM DE VARIANTE NE S'AFFICHE PAS
rem
rem Double-cliquez, PATIENTEZ le demarrage, puis allez a STAGE SELECT et
rem amenez le curseur sur la case de DURAL. C'est la que le dessin s'execute
rem pour la premiere fois -- et donc la que ca plante.
rem Le bilan s'affiche apres.
rem
rem POURQUOI LA CASE DE DURAL PRECISEMENT
rem
rem   DESSINER commence par une garde : si [rbx+0x5C] n'est pas dans l'anneau
rem   21..25, il ressort aussitot. Sur toutes les autres cases il ne fait donc
rem   RIEN. Le plantage arrive exactement quand il travaille pour la premiere
rem   fois -- ce qui colle mot pour mot a ce que vous avez vu.
rem
rem CE QUE LA SONDE VIDE, ET C'EST LA QUE SERA LA REPONSE
rem
rem   Juste avant l'appel de dessin, elle releve TOUT ce qu'il recoit :
rem     . la chaine et son adresse reelle ;
rem     . la couleur, les deux modes, les quatre coordonnees x1 y1 x2 y2 ;
rem     . le style : son mode, sa police, ses metriques et ses QUATRE ECHELLES.
rem
rem   Trois lectures possibles :
rem     . echelles a 0 ou NaN     -> le style n'est pas initialise. Le site
rem       d'origine appelle 0x180187AA0 puis 0x180187CB0(2) avant de poser le
rem       mode ; je les avais sautes ;
rem     . coordonnees aberrantes  -> le texte tombe hors de l'ecran ;
rem     . tout est bon            -> le dessin part, mais il est recouvert, ou
rem       il faut l'emettre en phase de RENDU et non dans l'update.
rem
rem CE QUE LA MESURE FAIT AUSSI
rem
rem   DESSINER enchaine cinq appels au moteur. Un jalon devant chacun, et le
rem   DERNIER jalon atteint nomme le fautif :
rem
rem     0x180EA1313  construire le DESCRIPTEUR   (0x18019A8C0)
rem     0x180EA131F  construire le STYLE         (0x18019A9D0)
rem     0x180EA132B  poser le mode 2             (0x18019B6F0)
rem     0x180EA1344  poser la taille 32.0        (0x18019B830)
rem     0x180EA13AE  LE DESSIN                   (0x18019B2E0)
rem     0x180EA13BA  apres le dessin -- atteint = il a survecu
rem
rem   Le debogueur journalise en plus l'exception, avec son adresse.
rem
rem   ATTENTION : cet outil REPATCHE la DLL avec le dessin (--variantes-texte),
rem   qui ne fait plus partie de la build normale. Pour retrouver une build
rem   jouable ensuite, relancez variantes.cmd.
rem
rem   Journal complet : analysis\pister_dessin.txt
rem ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0.."
taskkill /f /im vfes.exe >nul 2>&1
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>&1
py -3 tools\pister_dessin.py --secondes 300
echo.
pause
endlocal
