; menu_repartiteur_validation.asm  --  Menu_RepartiteurDeValidation
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801DDF30 - 0x1801DE1E3  (691 octets)   [15 entrees .pdata chainees]
;
; A QUOI : Le repartiteur de validation du menu principal : premiere chose qu'il fait, il refuse toute entree dont l'etat page+0x642+i n'est pas 0 (0x1801DDF4C..0x1801DDF65) -- une entree grisee ou masquee ne fait RIEN. Une seule fonction, 15 entrees .pdata chainees jusqu'a 0x1801DE1E3 (la note en annonce dix : compte corrige ici, mesure).
;
; D'OU VIENT LE NOM : VF5RE/analysis/menu_console.md, section 8.2
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
  0001801DDF30  4057                       push rdi                              
  0001801DDF32  4883EC20                   sub rsp, 0x20                         
  0001801DDF36  4883B95006000000           cmp qword ptr [rcx + 0x650], 0        
  0001801DDF3E  488BF9                     mov rdi, rcx                          
  0001801DDF41  0F859D000000               jne 0x1801ddfe4                          -> 0x1801DDFE4 (.text)
  0001801DDF47  E8C4E0FDFF                 call 0x1801bc010                         -> 0x1801BC010 (.text)
  0001801DDF4C  48634F58                   movsxd rcx, dword ptr [rdi + 0x58]    
  0001801DDF50  C6476000                   mov byte ptr [rdi + 0x60], 0          
  0001801DDF54  80BC394206000000           cmp byte ptr [rcx + rdi + 0x642], 0   
  0001801DDF5C  741F                       je 0x1801ddf7d                           -> 0x1801DDF7D (.text)
  0001801DDF5E  E8ED94E2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801DDF63  84C0                       test al, al                           
  0001801DDF65  747D                       je 0x1801ddfe4                           -> 0x1801DDFE4 (.text)
  0001801DDF67  33D2                       xor edx, edx                          
  0001801DDF69  33C9                       xor ecx, ecx                          
  0001801DDF6B  E850E3FCFF                 call 0x1801ac2c0                         -> 0x1801AC2C0 (.text)
  0001801DDF70  48898750060000             mov qword ptr [rdi + 0x650], rax      
  0001801DDF77  4883C420                   add rsp, 0x20                         
  0001801DDF7B  5F                         pop rdi                               
  0001801DDF7C  C3                         ret                                   
  0001801DDF7D  48895C2430                 mov qword ptr [rsp + 0x30], rbx       
  0001801DDF82  85C9                       test ecx, ecx                         
  0001801DDF84  751B                       jne 0x1801ddfa1                          -> 0x1801DDFA1 (.text)
  0001801DDF86  488D9F58060000             lea rbx, [rdi + 0x658]                
  0001801DDF8D  488BCB                     mov rcx, rbx                          
  0001801DDF90  E84B690000                 call 0x1801e48e0                         -> 0x1801E48E0 (.text)
  0001801DDF95  488D15444C3500             lea rdx, [rip + 0x354c44]                ; -> 0x180532BE0  "ARCADE MENU"
  0001801DDF9C  E9CB000000                 jmp 0x1801de06c                          -> 0x1801DE06C (.text)
  0001801DDFA1  83F901                     cmp ecx, 1                            
  0001801DDFA4  7544                       jne 0x1801ddfea                          -> 0x1801DDFEA (.text)
  0001801DDFA6  33DB                       xor ebx, ebx                          
  0001801DDFA8  4889742438                 mov qword ptr [rsp + 0x38], rsi       
  0001801DDFAD  488DB7A8190000             lea rsi, [rdi + 0x19a8]               
  0001801DDFB4  899F001A0000               mov dword ptr [rdi + 0x1a00], ebx     
  0001801DDFBA  488BCE                     mov rcx, rsi                          
  0001801DDFBD  889F081A0000               mov byte ptr [rdi + 0x1a08], bl       
  0001801DDFC3  488D15264C3500             lea rdx, [rip + 0x354c26]                ; -> 0x180532BF0  "VERSUS MENU"
  0001801DDFCA  E861780600                 call 0x180245830                         -> 0x180245830 (.text)
  0001801DDFCF  84C0                       test al, al                           
  0001801DDFD1  7407                       je 0x1801ddfda                           -> 0x1801DDFDA (.text)
  0001801DDFD3  4889B750060000             mov qword ptr [rdi + 0x650], rsi      
  0001801DDFDA  488B742438                 mov rsi, qword ptr [rsp + 0x38]       
  0001801DDFDF  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001801DDFE4  4883C420                   add rsp, 0x20                         
  0001801DDFE8  5F                         pop rdi                               
  0001801DDFE9  C3                         ret                                   
  0001801DDFEA  83F902                     cmp ecx, 2                            
  0001801DDFED  7545                       jne 0x1801de034                          -> 0x1801DE034 (.text)
  0001801DDFEF  488B052A585700             mov rax, qword ptr [rip + 0x57582a]      ; -> 0x180753820
  0001801DDFF6  488D15D34B3500             lea rdx, [rip + 0x354bd3]                ; -> 0x180532BD0  "MULTI MENU"
  0001801DDFFD  33DB                       xor ebx, ebx                          
  0001801DDFFF  895858                     mov dword ptr [rax + 0x58], ebx       
  0001801DE002  885860                     mov byte ptr [rax + 0x60], bl         
  0001801DE005  8898F4020000               mov byte ptr [rax + 0x2f4], bl        
  0001801DE00B  488B0D0E585700             mov rcx, qword ptr [rip + 0x57580e]      ; -> 0x180753820
  0001801DE012  E819780600                 call 0x180245830                         -> 0x180245830 (.text)
  0001801DE017  84C0                       test al, al                           
  0001801DE019  74C4                       je 0x1801ddfdf                           -> 0x1801DDFDF (.text)
  0001801DE01B  488B05FE575700             mov rax, qword ptr [rip + 0x5757fe]      ; -> 0x180753820
  0001801DE022  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001801DE027  48898750060000             mov qword ptr [rdi + 0x650], rax      
  0001801DE02E  4883C420                   add rsp, 0x20                         
  0001801DE032  5F                         pop rdi                               
  0001801DE033  C3                         ret                                   
  0001801DE034  83F903                     cmp ecx, 3                            
  0001801DE037  7518                       jne 0x1801de051                          -> 0x1801DE051 (.text)
  0001801DE039  488D9FF01C0000             lea rbx, [rdi + 0x1cf0]               
  0001801DE040  488BCB                     mov rcx, rbx                          
  0001801DE043  E8F8690000                 call 0x1801e4a40                         -> 0x1801E4A40 (.text)
  0001801DE048  488D15B14B3500             lea rdx, [rip + 0x354bb1]                ; -> 0x180532C00  "TRAINING MENU"
  0001801DE04F  EB1B                       jmp 0x1801de06c                          -> 0x1801DE06C (.text)
  0001801DE051  83F904                     cmp ecx, 4                            
  0001801DE054  7538                       jne 0x1801de08e                          -> 0x1801DE08E (.text)
  0001801DE056  488D9F28230000             lea rbx, [rdi + 0x2328]               
  0001801DE05D  488BCB                     mov rcx, rbx                          
  0001801DE060  E8AB690000                 call 0x1801e4a10                         -> 0x1801E4A10 (.text)
  0001801DE065  488D15A44B3500             lea rdx, [rip + 0x354ba4]                ; -> 0x180532C10  "TERMINAL MENU"
  0001801DE06C  488BCB                     mov rcx, rbx                          
  0001801DE06F  E8BC770600                 call 0x180245830                         -> 0x180245830 (.text)
  0001801DE074  84C0                       test al, al                           
  0001801DE076  0F8463FFFFFF               je 0x1801ddfdf                           -> 0x1801DDFDF (.text)
  0001801DE07C  48899F50060000             mov qword ptr [rdi + 0x650], rbx      
  0001801DE083  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001801DE088  4883C420                   add rsp, 0x20                         
  0001801DE08C  5F                         pop rdi                               
  0001801DE08D  C3                         ret                                   
  0001801DE08E  83F905                     cmp ecx, 5                            
  0001801DE091  751E                       jne 0x1801de0b1                          -> 0x1801DE0B1 (.text)
  0001801DE093  41B001                     mov r8b, 1                            
  0001801DE096  33D2                       xor edx, edx                          
  0001801DE098  33C9                       xor ecx, ecx                          
  0001801DE09A  E88120FDFF                 call 0x1801b0120                         -> 0x1801B0120 (.text)
  0001801DE09F  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001801DE0A4  48898750060000             mov qword ptr [rdi + 0x650], rax      
  0001801DE0AB  4883C420                   add rsp, 0x20                         
  0001801DE0AF  5F                         pop rdi                               
  0001801DE0B0  C3                         ret                                   
  0001801DE0B1  83F906                     cmp ecx, 6                            
  0001801DE0B4  750F                       jne 0x1801de0c5                          -> 0x1801DE0C5 (.text)
  0001801DE0B6  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001801DE0BB  4883C420                   add rsp, 0x20                         
  0001801DE0BF  5F                         pop rdi                               
  0001801DE0C0  E96B93E2FF                 jmp 0x180007430                          -> 0x180007430 (.text)
  0001801DE0C5  83F907                     cmp ecx, 7                            
  0001801DE0C8  751E                       jne 0x1801de0e8                          -> 0x1801DE0E8 (.text)
  0001801DE0CA  41B001                     mov r8b, 1                            
  0001801DE0CD  33D2                       xor edx, edx                          
  0001801DE0CF  33C9                       xor ecx, ecx                          
  0001801DE0D1  E8CAD2FCFF                 call 0x1801ab3a0                         -> 0x1801AB3A0 (.text)
  0001801DE0D6  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001801DE0DB  48898750060000             mov qword ptr [rdi + 0x650], rax      
  0001801DE0E2  4883C420                   add rsp, 0x20                         
  0001801DE0E6  5F                         pop rdi                               
  0001801DE0E7  C3                         ret                                   
  0001801DE0E8  83F908                     cmp ecx, 8                            
  0001801DE0EB  7565                       jne 0x1801de152                          -> 0x1801DE152 (.text)
  0001801DE0ED  E85E93E2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801DE0F2  84C0                       test al, al                           
  0001801DE0F4  7417                       je 0x1801de10d                           -> 0x1801DE10D (.text)
  0001801DE0F6  E83593E2FF                 call 0x180007430                         -> 0x180007430 (.text)
  0001801DE0FB  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001801DE100  C6874006000001             mov byte ptr [rdi + 0x640], 1         
  0001801DE107  4883C420                   add rsp, 0x20                         
  0001801DE10B  5F                         pop rdi                               
  0001801DE10C  C3                         ret                                   
  0001801DE10D  488D9F28290000             lea rbx, [rdi + 0x2928]               
  0001801DE114  488BCB                     mov rcx, rbx                          
  0001801DE117  488D15A2493500             lea rdx, [rip + 0x3549a2]                ; -> 0x180532AC0  "DLC STORE"
  0001801DE11E  E80D770600                 call 0x180245830                         -> 0x180245830 (.text)
  0001801DE123  84C0                       test al, al                           
  0001801DE125  7417                       je 0x1801de13e                           -> 0x1801DE13E (.text)
  0001801DE127  E80493E2FF                 call 0x180007430                         -> 0x180007430 (.text)
  0001801DE12C  48899F50060000             mov qword ptr [rdi + 0x650], rbx      
  0001801DE133  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001801DE138  4883C420                   add rsp, 0x20                         
  0001801DE13C  5F                         pop rdi                               
  0001801DE13D  C3                         ret                                   
  0001801DE13E  33DB                       xor ebx, ebx                          
  0001801DE140  48899F50060000             mov qword ptr [rdi + 0x650], rbx      
  0001801DE147  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001801DE14C  4883C420                   add rsp, 0x20                         
  0001801DE150  5F                         pop rdi                               
  0001801DE151  C3                         ret                                   
  0001801DE152  83F909                     cmp ecx, 9                            
  0001801DE155  0F8584FEFFFF               jne 0x1801ddfdf                          -> 0x1801DDFDF (.text)
  0001801DE15B  E8F092E2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801DE160  84C0                       test al, al                           
  0001801DE162  741E                       je 0x1801de182                           -> 0x1801DE182 (.text)
  0001801DE164  BA01000000                 mov edx, 1                            
  0001801DE169  33C9                       xor ecx, ecx                          
  0001801DE16B  E850E1FCFF                 call 0x1801ac2c0                         -> 0x1801AC2C0 (.text)
  0001801DE170  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001801DE175  48898750060000             mov qword ptr [rdi + 0x650], rax      
  0001801DE17C  4883C420                   add rsp, 0x20                         
  0001801DE180  5F                         pop rdi                               
  0001801DE181  C3                         ret                                   
  0001801DE182  488D8FC0040000             lea rcx, [rdi + 0x4c0]                
  0001801DE189  E8C2F7FDFF                 call 0x1801bd950                         -> 0x1801BD950 (.text)
  0001801DE18E  488D15E34A3500             lea rdx, [rip + 0x354ae3]                ; -> 0x180532C78  "EXIT_CAUTION"
  0001801DE195  488D8FC0040000             lea rcx, [rdi + 0x4c0]                
  0001801DE19C  E88F760600                 call 0x180245830                         -> 0x180245830 (.text)
  0001801DE1A1  B9EE030000                 mov ecx, 0x3ee                        
  0001801DE1A6  E8651B0100                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801DE1AB  BA01000000                 mov edx, 1                            
  0001801DE1B0  48898730050000             mov qword ptr [rdi + 0x530], rax      
  0001801DE1B7  488D8FC0040000             lea rcx, [rdi + 0x4c0]                
  0001801DE1BE  E85D07FEFF                 call 0x1801be920                         -> 0x1801BE920 (.text)
  0001801DE1C3  33DB                       xor ebx, ebx                          
  0001801DE1C5  C6873C06000001             mov byte ptr [rdi + 0x63c], 1         
  0001801DE1CC  899F48050000               mov dword ptr [rdi + 0x548], ebx      
  0001801DE1D2  889F4D050000               mov byte ptr [rdi + 0x54d], bl        
  0001801DE1D8  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001801DE1DD  4883C420                   add rsp, 0x20                         
  0001801DE1E1  5F                         pop rdi                               
  0001801DE1E2  C3                         ret                                   
