; menu_main_sortie_corps.asm  --  MenuMain_SortirDuSousEtat_corps
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801DB870 - 0x1801DB87C  (12 octets)   [AUCUNE entree .pdata : borne au premier ret/jmp]
;
; A QUOI : LE CORPS du gestionnaire de sortie du sous-etat 36 = MENU_MAIN : 0x1800DCBE0 ne fait que `sub rsp,0x28 ; call ici ; mov al,1 ; ret`.
;
; D'OU VIENT LE NOM : mesure du 2026-11-19 : seul appel de 0x1800DCBE0, lui-meme fn_sortie de la ligne 36 de la table 0x1803A05A0
;
; Desassemblage par pefile + capstone, depose le 2026-11-19. Le PE n'est NI
; charge NI execute : on lit le fichier. Les bornes viennent de .pdata, pas
; d'un comptage a l'oeil.
;
; CE N'EST PAS DU CODE A RECOPIER NI A COMPILER : c'est une LECTURE du
; module d'APM3, gardee pour ne pas la refaire.
;
; ATTENTION AUX ADRESSES. Les deux modules ont la MEME base 0x180000000 et
; des adresses DIFFERENTES. Tout ce qui est ici est APM3. Les adresses de
; REVO (vf5fs-pxd-w64-d3d12_SteamRetail.dll) ne s'y substituent jamais.
;
  0001801DB870  488B0DA17F5700             mov rcx, qword ptr [rip + 0x577fa1]      ; -> 0x180753818
  0001801DB877  E924980600                 jmp 0x1802450a0                          -> 0x1802450A0 (.text)
