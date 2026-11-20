; ranking_ouvrir.asm  --  Ranking_OuvrirLaPage
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801B0120 - 0x1801B014E  (46 octets)
;
; A QUOI : Destination de l'entree 5 SCOREBOARDS du menu principal : ouvre la scene RANKING. Jumeau probable de FUN_1801C0100 cote REVO.
;
; D'OU VIENT LE NOM : VF5RE/analysis/menu_console.md, section 8.3 (ligne 5)
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
  0001801B0120  4883EC28                   sub rsp, 0x28                         
  0001801B0124  488D151D182600             lea rdx, [rip + 0x26181d]                ; -> 0x180411948  "RANKING"
  0001801B012B  488D0DBE125A00             lea rcx, [rip + 0x5a12be]                ; -> 0x1807513F0
  0001801B0132  E8F9560900                 call 0x180245830                         -> 0x180245830 (.text)
  0001801B0137  84C0                       test al, al                           
  0001801B0139  740C                       je 0x1801b0147                           -> 0x1801B0147 (.text)
  0001801B013B  488D05AE125A00             lea rax, [rip + 0x5a12ae]                ; -> 0x1807513F0
  0001801B0142  4883C428                   add rsp, 0x28                         
  0001801B0146  C3                         ret                                   
  0001801B0147  33C0                       xor eax, eax                          
  0001801B0149  4883C428                   add rsp, 0x28                         
  0001801B014D  C3                         ret                                   
