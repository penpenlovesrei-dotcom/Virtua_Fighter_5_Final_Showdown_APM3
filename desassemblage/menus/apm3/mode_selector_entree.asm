; mode_selector_entree.asm  --  ModeSelector_EntrerLeSousEtat
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1800DCA70 - 0x1800DCA8C  (28 octets)
;
; A QUOI : Sous-etat 18 = MODE_SELECTOR, gestionnaire d'ENTREE. MODE_SELECTOR n'est PAS un ecran : c'est un sas de trois gestionnaires, sans page, sans liste, sans libelle, sans curseur et sans lecture d'entrees, qui ecrit un seul champ de session.
;
; D'OU VIENT LE NOM : VF5RE/analysis/mode_selector.md, section 1
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
  0001800DCA70  4883EC28                   sub rsp, 0x28                         
  0001800DCA74  33C9                       xor ecx, ecx                          
  0001800DCA76  C705B47B560001000000       mov dword ptr [rip + 0x567bb4], 1        ; -> 0x180644634
  0001800DCA80  E8DBA50D00                 call 0x1801b7060                         -> 0x1801B7060 (.text)
  0001800DCA85  B001                       mov al, 1                             
  0001800DCA87  4883C428                   add rsp, 0x28                         
  0001800DCA8B  C3                         ret                                   
