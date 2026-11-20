; mode_selector_sortie.asm  --  ModeSelector_SortirDuSousEtat
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1800DBB50 - 0x1800DBB65  (21 octets)
;
; A QUOI : Sous-etat 18 = MODE_SELECTOR, gestionnaire de SORTIE (21 o).
;
; D'OU VIENT LE NOM : VF5RE/TABLE_DES_SCENES_APM3_VS_REVO.md, section 6 (ligne 18)
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
  0001800DBB50  4883EC28                   sub rsp, 0x28                         
  0001800DBB54  E877E5FDFF                 call 0x1800ba0d0                         -> 0x1800BA0D0 (.text)
  0001800DBB59  E8D2B8F2FF                 call 0x180007430                         -> 0x180007430 (.text)
  0001800DBB5E  B001                       mov al, 1                             
  0001800DBB60  4883C428                   add rsp, 0x28                         
  0001800DBB64  C3                         ret                                   
