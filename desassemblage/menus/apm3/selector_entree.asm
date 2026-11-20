; selector_entree.asm  --  Selector_EntrerLeSousEtat
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1800DCA90 - 0x1800DCB31  (161 octets)
;
; A QUOI : Sous-etat 17 = SELECTOR (choix des combattants), gestionnaire d'ENTREE. Cote REVO le meme sous-etat porte le numero 19 et ses trois gestionnaires sont 0x1800E3F90 / 0x1800E2470 / 0x1800E2F60.
;
; D'OU VIENT LE NOM : VF5RE/TABLE_DES_SCENES_APM3_VS_REVO.md, section 6 (ligne 17)
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
  0001800DCA90  4053                       push rbx                              
  0001800DCA92  4883EC20                   sub rsp, 0x20                         
  0001800DCA96  33C9                       xor ecx, ecx                          
  0001800DCA98  E8C3A50D00                 call 0x1801b7060                         -> 0x1801B7060 (.text)
  0001800DCA9D  E8FE58FDFF                 call 0x1800b23a0                         -> 0x1800B23A0 (.text)
  0001800DCAA2  488B0DB72A2C00             mov rcx, qword ptr [rip + 0x2c2ab7]      ; -> 0x18039F560
  0001800DCAA9  BA03000000                 mov edx, 3                            
  0001800DCAAE  488BD8                     mov rbx, rax                          
  0001800DCAB1  E82A77FFFF                 call 0x1800d41e0                         -> 0x1800D41E0 (.text)
  0001800DCAB6  488B0D6B7E6300             mov rcx, qword ptr [rip + 0x637e6b]      ; -> 0x180714928
  0001800DCABD  E80E080900                 call 0x18016d2d0                         -> 0x18016D2D0 (.text)
  0001800DCAC2  33D2                       xor edx, edx                          
  0001800DCAC4  488BCB                     mov rcx, rbx                          
  0001800DCAC7  E86452FDFF                 call 0x1800b1d30                         -> 0x1800B1D30 (.text)
  0001800DCACC  84C0                       test al, al                           
  0001800DCACE  740E                       je 0x1800dcade                           -> 0x1800DCADE (.text)
  0001800DCAD0  488B0D517E6300             mov rcx, qword ptr [rip + 0x637e51]      ; -> 0x180714928
  0001800DCAD7  33D2                       xor edx, edx                          
  0001800DCAD9  E822040900                 call 0x18016cf00                         -> 0x18016CF00 (.text)
  0001800DCADE  BA01000000                 mov edx, 1                            
  0001800DCAE3  488BCB                     mov rcx, rbx                          
  0001800DCAE6  E84552FDFF                 call 0x1800b1d30                         -> 0x1800B1D30 (.text)
  0001800DCAEB  84C0                       test al, al                           
  0001800DCAED  7411                       je 0x1800dcb00                           -> 0x1800DCB00 (.text)
  0001800DCAEF  488B0D327E6300             mov rcx, qword ptr [rip + 0x637e32]      ; -> 0x180714928
  0001800DCAF6  BA01000000                 mov edx, 1                            
  0001800DCAFB  E800040900                 call 0x18016cf00                         -> 0x18016CF00 (.text)
  0001800DCB00  488BCB                     mov rcx, rbx                          
  0001800DCB03  E8A859FDFF                 call 0x1800b24b0                         -> 0x1800B24B0 (.text)
  0001800DCB08  488BC8                     mov rcx, rax                          
  0001800DCB0B  E870B0FDFF                 call 0x1800b7b80                         -> 0x1800B7B80 (.text)
  0001800DCB10  B984030000                 mov ecx, 0x384                        
  0001800DCB15  E816A9F2FF                 call 0x180007430                         -> 0x180007430 (.text)
  0001800DCB1A  E811A9F2FF                 call 0x180007430                         -> 0x180007430 (.text)
  0001800DCB1F  B001                       mov al, 1                             
  0001800DCB21  C705FDF9620000000000       mov dword ptr [rip + 0x62f9fd], 0        ; -> 0x18070C528
  0001800DCB2B  4883C420                   add rsp, 0x20                         
  0001800DCB2F  5B                         pop rbx                               
  0001800DCB30  C3                         ret                                   
