; menu_main_entree.asm  --  MenuMain_EntrerLeSousEtat
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1800DCCA0 - 0x1800DCCB0  (16 octets)
;
; A QUOI : Sous-etat 36 = MENU_MAIN, gestionnaire d'ENTREE (fn_entree du descripteur). Sa phase 1 est le bouchon 0x180007450, donc le sous-etat ne finit jamais : MENU_MAIN est l'etat de REPOS.
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
  0001800DCCA0  4883EC28                   sub rsp, 0x28                         
  0001800DCCA4  E8277A1000                 call 0x1801e46d0                         -> 0x1801E46D0 (.text)
  0001800DCCA9  B001                       mov al, 1                             
  0001800DCCAB  4883C428                   add rsp, 0x28                         
  0001800DCCAF  C3                         ret                                   
