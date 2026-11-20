; selector_sortie.asm  --  Selector_SortirDuSousEtat
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1800DBB70 - 0x1800DBB87  (23 octets)
;
; A QUOI : Sous-etat 17 = SELECTOR, gestionnaire de SORTIE. Il est PARTAGE avec APM3_SELECTOR (sous-etat 49), qui pointe la meme adresse.
;
; D'OU VIENT LE NOM : VF5RE/TABLE_DES_SCENES_APM3_VS_REVO.md, section 6 (lignes 17 et 49)
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
  0001800DBB70  4883EC28                   sub rsp, 0x28                         
  0001800DBB74  488B0DAD8D6300             mov rcx, qword ptr [rip + 0x638dad]      ; -> 0x180714928
  0001800DBB7B  E870D2FEFF                 call 0x1800c8df0                         -> 0x1800C8DF0 (.text)
  0001800DBB80  B001                       mov al, 1                             
  0001800DBB82  4883C428                   add rsp, 0x28                         
  0001800DBB86  C3                         ret                                   
