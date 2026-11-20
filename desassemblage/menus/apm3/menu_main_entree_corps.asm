; menu_main_entree_corps.asm  --  MenuMain_EntrerLeSousEtat_corps
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801E46D0 - 0x1801E46E3  (19 octets)   [AUCUNE entree .pdata : borne au premier ret/jmp]
;
; A QUOI : LE CORPS du gestionnaire d'entree du sous-etat 36 = MENU_MAIN : 0x1800DCCA0 ne fait que `sub rsp,0x28 ; call ici ; mov al,1 ; ret`. Aucune entree .pdata (feuille) : borne au premier ret/jmp.
;
; D'OU VIENT LE NOM : mesure du 2026-11-19 : seul appel de 0x1800DCCA0, lui-meme fn_entree de la ligne 36 de la table 0x1803A05A0 (VF5RE/TABLE_DES_SCENES_APM3_VS_REVO.md section 6)
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
  0001801E46D0  488B0D41F15600             mov rcx, qword ptr [rip + 0x56f141]      ; -> 0x180753818
  0001801E46D7  488D15C2E43400             lea rdx, [rip + 0x34e4c2]                ; -> 0x180532BA0  "MAIN MENU"
  0001801E46DE  E94D110600                 jmp 0x180245830                          -> 0x180245830 (.text)
