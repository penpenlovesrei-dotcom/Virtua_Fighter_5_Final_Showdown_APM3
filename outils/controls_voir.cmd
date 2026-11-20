@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- VOIR OPTIONS ^> CONTROLS, SANS RIEN TOUCHER. Double-cliquez.
rem
rem Le jeu est lance, navigue tout seul jusqu a OPTIONS ^> Controls et
rem photographie l ecran. Environ soixante-dix secondes, aucun clavier.
rem
rem CE QU IL FAUT Y VOIR, apres le correctif du 2026-10-10 : les quatre
rem pictos des quatre premieres lignes sont les boutons XBOX -- le Y, le B,
rem le A et le X colores, et non plus le triangle, le rond, la croix et le
rem carre PlayStation.
rem
rem POURQUOI CE N ETAIT PAS LA TABLE D ECHAPPEMENTS : le moteur PERMUTE les
rem deux jeux de glyphes. Mesure -- U+E000 dessine le rond, U+E015 dessine le
rem B. Les libelles portent donc desormais l autre jeu, un octet chacun.
rem
rem La capture : analysis\essai_controls_t58.png
rem Pour tout rendre : py -3 tools\pictos_xbox.py --retirer
rem ---------------------------------------------------------------------------
cd /d "%~dp0.."
py -3 tools\essai_menu.py controls
echo.
pause
