@echo off
rem ---------------------------------------------------------------------------
rem VF5 FS -- POSER DES TEXTURES HD. Double-cliquez.
rem
rem Il prend tous les .png poses dans HD_TEXTURES\HD\2D et les met dans le
rem jeu, a la place des textures d origine.
rem
rem LE NOM DU FICHIER EST SON ADRESSE :   <archive>__texNN.png
rem    par exemple   spr_n_cmn__tex04.png
rem HD_TEXTURES\EXTRACTED\2D porte les 171 textures du jeu deja sorties en
rem PNG, chacune sous le nom exact qu il faut lui redonner. On part de celle-la.
rem
rem L ARBORESCENCE :  EXTRACTED\ ce qui SORT du jeu,  HD\ ce qui y RENTRE,
rem et les trois familles  2D\  STAGES\  CHARACTERS  dans chacun.
rem
rem CE QUI EST POSSIBLE, ET C EST MESURE : les UV des sprites sont des
rem flottants NORMALISES, pas des pixels. Agrandir une planche ne deplace donc
rem aucun sprite -- la meme region porte simplement plus de texels.
rem
rem ET LES CALQUES SUIVENT, depuis le 2026-10-12. Essai a l appui : les
rem deux planches de spr_n_adv posees en 4x sans rien d autre, et le logo
rem AM2 s affichait QUATRE FOIS TROP GRAND, coin haut-gauche en place.
rem La taille du dessin vient du rectangle en PIXELS du sprite, et
rem l ancre du calque AET est elle aussi en pixels : les deux doivent
rem suivre la planche. Cet outil corrige maintenant lui-meme les calques
rem de aet_<nom>.bin -- echelle divisee, ancre multipliee -- et garde
rem le .bin d origine a cote, comme l archive.
rem
rem LA SEULE CONTRAINTE : on remplace une PLANCHE ENTIERE, pas un sprite. Une
rem planche HD est l ancienne AGRANDIE (x2, x4), pas une planche reorganisee.
rem Et les deux cotes doivent rester multiples de 4.
rem
rem Le format d origine est conserve, les niveaux de mip regeneres, et
rem l archive d origine gardee a cote en .farc.origine.
rem
rem    py -3 tools\textures_hd.py --inventaire   les 171 textures
rem    py -3 tools\textures_hd.py --controle     ce qui SERAIT fait
rem    py -3 tools\textures_hd.py --retirer      rend les archives d origine
rem
rem Tout est explique dans HD_TEXTURES\LISEZMOI.md
rem ---------------------------------------------------------------------------
cd /d "%~dp0.."
py -3 tools\textures_hd.py --poser
echo.
pause
