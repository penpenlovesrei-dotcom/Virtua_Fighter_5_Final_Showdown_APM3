; selector_maj.asm  --  Selector_MettreAJour
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1800DB270 - 0x1800DB4A3  (563 octets)   [3 entrees .pdata chainees]
;
; A QUOI : Sous-etat 17 = SELECTOR, gestionnaire de MISE A JOUR. Le jumeau de REVO, 0x1800E2470, est l'ancre qui a servi a identifier la table des scenes elle-meme.
;
; D'OU VIENT LE NOM : VF5RE/TABLE_DES_SCENES_APM3_VS_REVO.md, sections 1 et 6
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
  0001800DB270  4156                       push r14                              
  0001800DB272  4883EC30                   sub rsp, 0x30                         
  0001800DB276  E82571FDFF                 call 0x1800b23a0                         -> 0x1800B23A0 (.text)
  0001800DB27B  488B0DDE422C00             mov rcx, qword ptr [rip + 0x2c42de]      ; -> 0x18039F560
  0001800DB282  BA03000000                 mov edx, 3                            
  0001800DB287  4C8BF0                     mov r14, rax                          
  0001800DB28A  E8518FFFFF                 call 0x1800d41e0                         -> 0x1800D41E0 (.text)
  0001800DB28F  833D9212630001             cmp dword ptr [rip + 0x631292], 1        ; -> 0x18070C528
  0001800DB296  0F84C2000000               je 0x1800db35e                           -> 0x1800DB35E (.text)
  0001800DB29C  488B0D85966300             mov rcx, qword ptr [rip + 0x639685]      ; -> 0x180714928
  0001800DB2A3  E8F89B1600                 call 0x180244ea0                         -> 0x180244EA0 (.text)
  0001800DB2A8  84C0                       test al, al                           
  0001800DB2AA  0F84A4000000               je 0x1800db354                           -> 0x1800DB354 (.text)
  0001800DB2B0  488B0D71966300             mov rcx, qword ptr [rip + 0x639671]      ; -> 0x180714928
  0001800DB2B7  E874200900                 call 0x18016d330                         -> 0x18016D330 (.text)
  0001800DB2BC  84C0                       test al, al                           
  0001800DB2BE  0F84E8000000               je 0x1800db3ac                           -> 0x1800DB3AC (.text)
  0001800DB2C4  48895C2440                 mov qword ptr [rsp + 0x40], rbx       
  0001800DB2C9  48896C2448                 mov qword ptr [rsp + 0x48], rbp       
  0001800DB2CE  33ED                       xor ebp, ebp                          
  0001800DB2D0  4889742450                 mov qword ptr [rsp + 0x50], rsi       
  0001800DB2D5  48897C2458                 mov qword ptr [rsp + 0x58], rdi       
  0001800DB2DA  660F1F440000               nop word ptr [rax + rax]              
  0001800DB2E0  488B0D41966300             mov rcx, qword ptr [rip + 0x639641]      ; -> 0x180714928
  0001800DB2E7  8BD5                       mov edx, ebp                          
  0001800DB2E9  E8621C0900                 call 0x18016cf50                         -> 0x18016CF50 (.text)
  0001800DB2EE  488B0D33966300             mov rcx, qword ptr [rip + 0x639633]      ; -> 0x180714928
  0001800DB2F5  8BD5                       mov edx, ebp                          
  0001800DB2F7  8BF0                       mov esi, eax                          
  0001800DB2F9  E8321C0900                 call 0x18016cf30                         -> 0x18016CF30 (.text)
  0001800DB2FE  488B0D23966300             mov rcx, qword ptr [rip + 0x639623]      ; -> 0x180714928
  0001800DB305  448BC0                     mov r8d, eax                          
  0001800DB308  8BD5                       mov edx, ebp                          
  0001800DB30A  8BF8                       mov edi, eax                          
  0001800DB30C  E80F1C0900                 call 0x18016cf20                         -> 0x18016CF20 (.text)
  0001800DB311  488B0D10966300             mov rcx, qword ptr [rip + 0x639610]      ; -> 0x180714928
  0001800DB318  8BD5                       mov edx, ebp                          
  0001800DB31A  8BD8                       mov ebx, eax                          
  0001800DB31C  E81F1C0900                 call 0x18016cf40                         -> 0x18016CF40 (.text)
  0001800DB321  89442428                   mov dword ptr [rsp + 0x28], eax       
  0001800DB325  448BCB                     mov r9d, ebx                          
  0001800DB328  448BC6                     mov r8d, esi                          
  0001800DB32B  897C2420                   mov dword ptr [rsp + 0x20], edi       
  0001800DB32F  8BD5                       mov edx, ebp                          
  0001800DB331  498BCE                     mov rcx, r14                          
  0001800DB334  E8477CFDFF                 call 0x1800b2f80                         -> 0x1800B2F80 (.text)
  0001800DB339  FFC5                       inc ebp                               
  0001800DB33B  83FD02                     cmp ebp, 2                            
  0001800DB33E  7CA0                       jl 0x1800db2e0                           -> 0x1800DB2E0 (.text)
  0001800DB340  488B7C2458                 mov rdi, qword ptr [rsp + 0x58]       
  0001800DB345  488B742450                 mov rsi, qword ptr [rsp + 0x50]       
  0001800DB34A  488B6C2448                 mov rbp, qword ptr [rsp + 0x48]       
  0001800DB34F  488B5C2440                 mov rbx, qword ptr [rsp + 0x40]       
  0001800DB354  C705CA11630001000000       mov dword ptr [rip + 0x6311ca], 1        ; -> 0x18070C528
  0001800DB35E  488B0DC3956300             mov rcx, qword ptr [rip + 0x6395c3]      ; -> 0x180714928
  0001800DB365  E8369B1600                 call 0x180244ea0                         -> 0x180244EA0 (.text)
  0001800DB36A  84C0                       test al, al                           
  0001800DB36C  0F85BD000000               jne 0x1800db42f                          -> 0x1800DB42F (.text)
  0001800DB372  38058903B600               cmp byte ptr [rip + 0xb60389], al        ; -> 0x180C3B701
  0001800DB378  0F85BA000000               jne 0x1800db438                          -> 0x1800DB438 (.text)
  0001800DB37E  488B0DA3956300             mov rcx, qword ptr [rip + 0x6395a3]      ; -> 0x180714928
  0001800DB385  E8D61F0900                 call 0x18016d360                         -> 0x18016D360 (.text)
  0001800DB38A  84C0                       test al, al                           
  0001800DB38C  0F84A6000000               je 0x1800db438                           -> 0x1800DB438 (.text)
  0001800DB392  33C9                       xor ecx, ecx                          
  0001800DB394  E8A7B90A00                 call 0x180186d40                         -> 0x180186D40 (.text)
  0001800DB399  B904000000                 mov ecx, 4                            
  0001800DB39E  E8FDF5FFFF                 call 0x1800da9a0                         -> 0x1800DA9A0 (.text)
  0001800DB3A3  B001                       mov al, 1                             
  0001800DB3A5  4883C430                   add rsp, 0x30                         
  0001800DB3A9  415E                       pop r14                               
  0001800DB3AB  C3                         ret                                   
  0001800DB3AC  488B0D75956300             mov rcx, qword ptr [rip + 0x639575]      ; -> 0x180714928
  0001800DB3B3  33D2                       xor edx, edx                          
  0001800DB3B5  E886110900                 call 0x18016c540                         -> 0x18016C540 (.text)
  0001800DB3BA  84C0                       test al, al                           
  0001800DB3BC  742A                       je 0x1800db3e8                           -> 0x1800DB3E8 (.text)
  0001800DB3BE  33C9                       xor ecx, ecx                          
  0001800DB3C0  E8BBB9FDFF                 call 0x1800b6d80                         -> 0x1800B6D80 (.text)
  0001800DB3C5  84C0                       test al, al                           
  0001800DB3C7  741F                       je 0x1800db3e8                           -> 0x1800DB3E8 (.text)
  0001800DB3C9  4533C9                     xor r9d, r9d                          
  0001800DB3CC  33D2                       xor edx, edx                          
  0001800DB3CE  498BCE                     mov rcx, r14                          
  0001800DB3D1  458D4101                   lea r8d, [r9 + 1]                     
  0001800DB3D5  E8C67BFDFF                 call 0x1800b2fa0                         -> 0x1800B2FA0 (.text)
  0001800DB3DA  488B0D47956300             mov rcx, qword ptr [rip + 0x639547]      ; -> 0x180714928
  0001800DB3E1  33D2                       xor edx, edx                          
  0001800DB3E3  E8181B0900                 call 0x18016cf00                         -> 0x18016CF00 (.text)
  0001800DB3E8  488B0D39956300             mov rcx, qword ptr [rip + 0x639539]      ; -> 0x180714928
  0001800DB3EF  BA01000000                 mov edx, 1                            
  0001800DB3F4  E847110900                 call 0x18016c540                         -> 0x18016C540 (.text)
  0001800DB3F9  84C0                       test al, al                           
  0001800DB3FB  7432                       je 0x1800db42f                           -> 0x1800DB42F (.text)
  0001800DB3FD  B901000000                 mov ecx, 1                            
  0001800DB402  E879B9FDFF                 call 0x1800b6d80                         -> 0x1800B6D80 (.text)
  0001800DB407  84C0                       test al, al                           
  0001800DB409  7424                       je 0x1800db42f                           -> 0x1800DB42F (.text)
  0001800DB40B  BA01000000                 mov edx, 1                            
  0001800DB410  4533C9                     xor r9d, r9d                          
  0001800DB413  448BC2                     mov r8d, edx                          
  0001800DB416  498BCE                     mov rcx, r14                          
  0001800DB419  E8827BFDFF                 call 0x1800b2fa0                         -> 0x1800B2FA0 (.text)
  0001800DB41E  488B0D03956300             mov rcx, qword ptr [rip + 0x639503]      ; -> 0x180714928
  0001800DB425  BA01000000                 mov edx, 1                            
  0001800DB42A  E8D11A0900                 call 0x18016cf00                         -> 0x18016CF00 (.text)
  0001800DB42F  32C0                       xor al, al                            
  0001800DB431  4883C430                   add rsp, 0x30                         
  0001800DB435  415E                       pop r14                               
  0001800DB437  C3                         ret                                   
  0001800DB438  E813C0F2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001800DB43D  84C0                       test al, al                           
  0001800DB43F  75EE                       jne 0x1800db42f                          -> 0x1800DB42F (.text)
  0001800DB441  E80AC0F2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001800DB446  84C0                       test al, al                           
  0001800DB448  75E5                       jne 0x1800db42f                          -> 0x1800DB42F (.text)
  0001800DB44A  488B0DBF466300             mov rcx, qword ptr [rip + 0x6346bf]      ; -> 0x18070FB10
  0001800DB451  384119                     cmp byte ptr [rcx + 0x19], al         
  0001800DB454  741E                       je 0x1800db474                           -> 0x1800DB474 (.text)
  0001800DB456  33D2                       xor edx, edx                          
  0001800DB458  E8C3630200                 call 0x180101820                         -> 0x180101820 (.text)
  0001800DB45D  41B8B0040000               mov r8d, 0x4b0                        
  0001800DB463  488BD0                     mov rdx, rax                          
  0001800DB466  33C9                       xor ecx, ecx                          
  0001800DB468  E8C3BFF2FF                 call 0x180007430                         -> 0x180007430 (.text)
  0001800DB46D  488B0D9C466300             mov rcx, qword ptr [rip + 0x63469c]      ; -> 0x18070FB10
  0001800DB474  80B9B905000000             cmp byte ptr [rcx + 0x5b9], 0         
  0001800DB47B  741D                       je 0x1800db49a                           -> 0x1800DB49A (.text)
  0001800DB47D  BA01000000                 mov edx, 1                            
  0001800DB482  E899630200                 call 0x180101820                         -> 0x180101820 (.text)
  0001800DB487  41B8B0040000               mov r8d, 0x4b0                        
  0001800DB48D  488BD0                     mov rdx, rax                          
  0001800DB490  B901000000                 mov ecx, 1                            
  0001800DB495  E896BFF2FF                 call 0x180007430                         -> 0x180007430 (.text)
  0001800DB49A  B001                       mov al, 1                             
  0001800DB49C  4883C430                   add rsp, 0x30                         
  0001800DB4A0  415E                       pop r14                               
  0001800DB4A2  C3                         ret                                   
