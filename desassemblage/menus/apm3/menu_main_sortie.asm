; menu_main_sortie.asm  --  MenuMain_SortirDuSousEtat
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1800DCBE0 - 0x1800DCBF0  (16 octets)
;
; A QUOI : Sous-etat 36 = MENU_MAIN, gestionnaire de SORTIE (fn_sortie).
;
; D'OU VIENT LE NOM : VF5RE/TABLE_DES_SCENES_APM3_VS_REVO.md, section 6 (ligne 36)
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
  0001800DCBE0  4883EC28                   sub rsp, 0x28                         
  0001800DCBE4  E887EC0F00                 call 0x1801db870                         -> 0x1801DB870 (.text)
  0001800DCBE9  B001                       mov al, 1                             
  0001800DCBEB  4883C428                   add rsp, 0x28                         
  0001800DCBEF  C3                         ret                                   
