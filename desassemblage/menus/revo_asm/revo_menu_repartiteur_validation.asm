; revo_menu_repartiteur_validation.asm  --  Menu_RepartiteurDeValidation (REVO)
;
; Cible   : vf5fs-pxd-w64-d3d12_SteamRetail.dll  (le module de R.E.V.O.)
;           7229952 octets, md5 64fea1ce4db6
; Base PE : 0x180000000
; Bornes  : 0x180209CB0 - 0x180209F5D  (685 octets)   [15 entrees .pdata chainees]
;
; A QUOI : LE repartiteur de validation du menu principal cote REVO -- cite 13 fois dans MENU.md et JAMAIS decompile. Il lit l'etat de l'entree en 0x180209CD4 (`cmp byte [rcx+rdi+0x5fa], 0`), le meme champ que le 0x642 d'APM3. Jumeau de 0x1801DDF30 cote APM3.
;
; D'OU VIENT LE NOM : VF5RE/code_decompile/MENU.md, section 419.83 (les quatre sites de 0x5FA) -- la fonction y est nommee, pas videe
;
; POURQUOI UN .ASM ET PAS UN .C : cette fonction est NOMMEE dans les notes
; et n'a aucune decompilation dans VF5RE/code_decompile (mesure du
; 2026-11-19). Lue ici par pefile + capstone dans le FICHIER du module.
; Ghidra n'a pas ete touche. Un desassemblage ne donne PAS la structure que
; donnerait une decompilation : il reste a vider proprement.
;
; CE N'EST PAS DU CODE A RECOPIER NI A COMPILER.
;
; ATTENTION AUX ADRESSES : ceci est REVO. Les deux modules ont la MEME base
; 0x180000000 et des adresses DIFFERENTES.
;
  000180209CB0  4057                       push rdi                              
  000180209CB2  4883EC20                   sub rsp, 0x20                         
  000180209CB6  4883B90806000000           cmp qword ptr [rcx + 0x608], 0        
  000180209CBE  488BF9                     mov rdi, rcx                          
  000180209CC1  0F8597000000               jne 0x180209d5e                          -> 0x180209D5E (.text)
  000180209CC7  E8444DFDFF                 call 0x1801dea10                         -> 0x1801DEA10 (.text)
  000180209CCC  48634F58                   movsxd rcx, dword ptr [rdi + 0x58]    
  000180209CD0  C6476000                   mov byte ptr [rdi + 0x60], 0          
  000180209CD4  80BC39FA05000000           cmp byte ptr [rcx + rdi + 0x5fa], 0   
  000180209CDC  741F                       je 0x180209cfd                           -> 0x180209CFD (.text)
  000180209CDE  E83D1DE0FF                 call 0x18000ba20                         -> 0x18000BA20 (.text)
  000180209CE3  84C0                       test al, al                           
  000180209CE5  7477                       je 0x180209d5e                           -> 0x180209D5E (.text)
  000180209CE7  33D2                       xor edx, edx                          
  000180209CE9  33C9                       xor ecx, ecx                          
  000180209CEB  E8B024FBFF                 call 0x1801bc1a0                         -> 0x1801BC1A0 (.text)
  000180209CF0  48898708060000             mov qword ptr [rdi + 0x608], rax      
  000180209CF7  4883C420                   add rsp, 0x20                         
  000180209CFB  5F                         pop rdi                               
  000180209CFC  C3                         ret                                   
  000180209CFD  48895C2430                 mov qword ptr [rsp + 0x30], rbx       
  000180209D02  85C9                       test ecx, ecx                         
  000180209D04  751B                       jne 0x180209d21                          -> 0x180209D21 (.text)
  000180209D06  488D9F10060000             lea rbx, [rdi + 0x610]                
  000180209D0D  488BCB                     mov rcx, rbx                          
  000180209D10  E8BB6E0000                 call 0x180210bd0                         -> 0x180210BD0 (.text)
  000180209D15  488D15FC083500             lea rdx, [rip + 0x3508fc]                ; -> 0x18055A618  "ARCADE MENU"
  000180209D1C  E9C5000000                 jmp 0x180209de6                          -> 0x180209DE6 (.text)
  000180209D21  83F901                     cmp ecx, 1                            
  000180209D24  753E                       jne 0x180209d64                          -> 0x180209D64 (.text)
  000180209D26  33DB                       xor ebx, ebx                          
  000180209D28  4889742438                 mov qword ptr [rsp + 0x38], rsi       
  000180209D2D  488DB778180000             lea rsi, [rdi + 0x1878]               
  000180209D34  488BCE                     mov rcx, rsi                          
  000180209D37  895E58                     mov dword ptr [rsi + 0x58], ebx       
  000180209D3A  488D15E7083500             lea rdx, [rip + 0x3508e7]                ; -> 0x18055A628  "VERSUS MENU"
  000180209D41  885E60                     mov byte ptr [rsi + 0x60], bl         
  000180209D44  E8B7360C00                 call 0x1802cd400                         -> 0x1802CD400 (.text)
  000180209D49  84C0                       test al, al                           
  000180209D4B  7407                       je 0x180209d54                           -> 0x180209D54 (.text)
  000180209D4D  4889B708060000             mov qword ptr [rdi + 0x608], rsi      
  000180209D54  488B742438                 mov rsi, qword ptr [rsp + 0x38]       
  000180209D59  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  000180209D5E  4883C420                   add rsp, 0x20                         
  000180209D62  5F                         pop rdi                               
  000180209D63  C3                         ret                                   
  000180209D64  83F902                     cmp ecx, 2                            
  000180209D67  7545                       jne 0x180209dae                          -> 0x180209DAE (.text)
  000180209D69  488B05F8135900             mov rax, qword ptr [rip + 0x5913f8]      ; -> 0x18079B168
  000180209D70  488D1591083500             lea rdx, [rip + 0x350891]                ; -> 0x18055A608  "MULTI MENU"
  000180209D77  33DB                       xor ebx, ebx                          
  000180209D79  895858                     mov dword ptr [rax + 0x58], ebx       
  000180209D7C  885860                     mov byte ptr [rax + 0x60], bl         
  000180209D7F  8898D4020000               mov byte ptr [rax + 0x2d4], bl        
  000180209D85  488B0DDC135900             mov rcx, qword ptr [rip + 0x5913dc]      ; -> 0x18079B168
  000180209D8C  E86F360C00                 call 0x1802cd400                         -> 0x1802CD400 (.text)
  000180209D91  84C0                       test al, al                           
  000180209D93  74C4                       je 0x180209d59                           -> 0x180209D59 (.text)
  000180209D95  488B05CC135900             mov rax, qword ptr [rip + 0x5913cc]      ; -> 0x18079B168
  000180209D9C  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  000180209DA1  48898708060000             mov qword ptr [rdi + 0x608], rax      
  000180209DA8  4883C420                   add rsp, 0x20                         
  000180209DAC  5F                         pop rdi                               
  000180209DAD  C3                         ret                                   
  000180209DAE  83F903                     cmp ecx, 3                            
  000180209DB1  7518                       jne 0x180209dcb                          -> 0x180209DCB (.text)
  000180209DB3  488D9FA01B0000             lea rbx, [rdi + 0x1ba0]               
  000180209DBA  488BCB                     mov rcx, rbx                          
  000180209DBD  E85E6F0000                 call 0x180210d20                         -> 0x180210D20 (.text)
  000180209DC2  488D156F083500             lea rdx, [rip + 0x35086f]                ; -> 0x18055A638  "TRAINING MENU"
  000180209DC9  EB1B                       jmp 0x180209de6                          -> 0x180209DE6 (.text)
  000180209DCB  83F904                     cmp ecx, 4                            
  000180209DCE  7538                       jne 0x180209e08                          -> 0x180209E08 (.text)
  000180209DD0  488D9F98210000             lea rbx, [rdi + 0x2198]               
  000180209DD7  488BCB                     mov rcx, rbx                          
  000180209DDA  E8116F0000                 call 0x180210cf0                         -> 0x180210CF0 (.text)
  000180209DDF  488D1562083500             lea rdx, [rip + 0x350862]                ; -> 0x18055A648  "TERMINAL MENU"
  000180209DE6  488BCB                     mov rcx, rbx                          
  000180209DE9  E812360C00                 call 0x1802cd400                         -> 0x1802CD400 (.text)
  000180209DEE  84C0                       test al, al                           
  000180209DF0  0F8463FFFFFF               je 0x180209d59                           -> 0x180209D59 (.text)
  000180209DF6  48899F08060000             mov qword ptr [rdi + 0x608], rbx      
  000180209DFD  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  000180209E02  4883C420                   add rsp, 0x20                         
  000180209E06  5F                         pop rdi                               
  000180209E07  C3                         ret                                   
  000180209E08  83F905                     cmp ecx, 5                            
  000180209E0B  751E                       jne 0x180209e2b                          -> 0x180209E2B (.text)
  000180209E0D  41B001                     mov r8b, 1                            
  000180209E10  33D2                       xor edx, edx                          
  000180209E12  33C9                       xor ecx, ecx                          
  000180209E14  E8E762FBFF                 call 0x1801c0100                         -> 0x1801C0100 (.text)
  000180209E19  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  000180209E1E  48898708060000             mov qword ptr [rdi + 0x608], rax      
  000180209E25  4883C420                   add rsp, 0x20                         
  000180209E29  5F                         pop rdi                               
  000180209E2A  C3                         ret                                   
  000180209E2B  83F906                     cmp ecx, 6                            
  000180209E2E  750F                       jne 0x180209e3f                          -> 0x180209E3F (.text)
  000180209E30  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  000180209E35  4883C420                   add rsp, 0x20                         
  000180209E39  5F                         pop rdi                               
  000180209E3A  E92111E0FF                 jmp 0x18000af60                          -> 0x18000AF60 (.text)
  000180209E3F  83F907                     cmp ecx, 7                            
  000180209E42  751E                       jne 0x180209e62                          -> 0x180209E62 (.text)
  000180209E44  41B001                     mov r8b, 1                            
  000180209E47  33D2                       xor edx, edx                          
  000180209E49  33C9                       xor ecx, ecx                          
  000180209E4B  E85015FBFF                 call 0x1801bb3a0                         -> 0x1801BB3A0 (.text)
  000180209E50  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  000180209E55  48898708060000             mov qword ptr [rdi + 0x608], rax      
  000180209E5C  4883C420                   add rsp, 0x20                         
  000180209E60  5F                         pop rdi                               
  000180209E61  C3                         ret                                   
  000180209E62  83F908                     cmp ecx, 8                            
  000180209E65  7565                       jne 0x180209ecc                          -> 0x180209ECC (.text)
  000180209E67  E8B41BE0FF                 call 0x18000ba20                         -> 0x18000BA20 (.text)
  000180209E6C  84C0                       test al, al                           
  000180209E6E  7417                       je 0x180209e87                           -> 0x180209E87 (.text)
  000180209E70  E8EB10E0FF                 call 0x18000af60                         -> 0x18000AF60 (.text)
  000180209E75  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  000180209E7A  C687F805000001             mov byte ptr [rdi + 0x5f8], 1         
  000180209E81  4883C420                   add rsp, 0x20                         
  000180209E85  5F                         pop rdi                               
  000180209E86  C3                         ret                                   
  000180209E87  488D9F58270000             lea rbx, [rdi + 0x2758]               
  000180209E8E  488BCB                     mov rcx, rbx                          
  000180209E91  488D1550063500             lea rdx, [rip + 0x350650]                ; -> 0x18055A4E8  "DLC STORE"
  000180209E98  E863350C00                 call 0x1802cd400                         -> 0x1802CD400 (.text)
  000180209E9D  84C0                       test al, al                           
  000180209E9F  7417                       je 0x180209eb8                           -> 0x180209EB8 (.text)
  000180209EA1  E8BA10E0FF                 call 0x18000af60                         -> 0x18000AF60 (.text)
  000180209EA6  48899F08060000             mov qword ptr [rdi + 0x608], rbx      
  000180209EAD  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  000180209EB2  4883C420                   add rsp, 0x20                         
  000180209EB6  5F                         pop rdi                               
  000180209EB7  C3                         ret                                   
  000180209EB8  33DB                       xor ebx, ebx                          
  000180209EBA  48899F08060000             mov qword ptr [rdi + 0x608], rbx      
  000180209EC1  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  000180209EC6  4883C420                   add rsp, 0x20                         
  000180209ECA  5F                         pop rdi                               
  000180209ECB  C3                         ret                                   
  000180209ECC  83F909                     cmp ecx, 9                            
  000180209ECF  0F8584FEFFFF               jne 0x180209d59                          -> 0x180209D59 (.text)
  000180209ED5  E8461BE0FF                 call 0x18000ba20                         -> 0x18000BA20 (.text)
  000180209EDA  84C0                       test al, al                           
  000180209EDC  741E                       je 0x180209efc                           -> 0x180209EFC (.text)
  000180209EDE  BA01000000                 mov edx, 1                            
  000180209EE3  33C9                       xor ecx, ecx                          
  000180209EE5  E8B622FBFF                 call 0x1801bc1a0                         -> 0x1801BC1A0 (.text)
  000180209EEA  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  000180209EEF  48898708060000             mov qword ptr [rdi + 0x608], rax      
  000180209EF6  4883C420                   add rsp, 0x20                         
  000180209EFA  5F                         pop rdi                               
  000180209EFB  C3                         ret                                   
  000180209EFC  488D8F88040000             lea rcx, [rdi + 0x488]                
  000180209F03  E88864FDFF                 call 0x1801e0390                         -> 0x1801E0390 (.text)
  000180209F08  488D15A1073500             lea rdx, [rip + 0x3507a1]                ; -> 0x18055A6B0  "EXIT_CAUTION"
  000180209F0F  488D8F88040000             lea rcx, [rdi + 0x488]                
  000180209F16  E8E5340C00                 call 0x1802cd400                         -> 0x1802CD400 (.text)
  000180209F1B  B9FE030000                 mov ecx, 0x3fe                        
  000180209F20  E8BB770200                 call 0x1802316e0                         -> 0x1802316E0 (.text)
  000180209F25  BA01000000                 mov edx, 1                            
  000180209F2A  488987F8040000             mov qword ptr [rdi + 0x4f8], rax      
  000180209F31  488D8F88040000             lea rcx, [rdi + 0x488]                
  000180209F38  E8C377FDFF                 call 0x1801e1700                         -> 0x1801E1700 (.text)
  000180209F3D  33DB                       xor ebx, ebx                          
  000180209F3F  C687F405000001             mov byte ptr [rdi + 0x5f4], 1         
  000180209F46  899F10050000               mov dword ptr [rdi + 0x510], ebx      
  000180209F4C  889F15050000               mov byte ptr [rdi + 0x515], bl        
  000180209F52  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  000180209F57  4883C420                   add rsp, 0x20                         
  000180209F5B  5F                         pop rdi                               
  000180209F5C  C3                         ret                                   
