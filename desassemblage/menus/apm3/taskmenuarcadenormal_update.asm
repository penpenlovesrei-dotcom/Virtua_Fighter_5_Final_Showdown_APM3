; taskmenuarcadenormal_update.asm  --  TaskMenuArcadeNormal_Update
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801DC270 - 0x1801DC50A  (666 octets)
;
; A QUOI : Pose le MODE DE JEU = 0 (Arcade) dans le dword global 0x180751010, premiere case d'un bloc de reglages de partie de 16 octets, en 0x1801DC3A6. Nom venu du RTTI, pas d'une deduction.
;
; D'OU VIENT LE NOM : VF5RE/analysis/mode_de_jeu.md, section 1
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
  0001801DC270  48895C2410                 mov qword ptr [rsp + 0x10], rbx       
  0001801DC275  48896C2418                 mov qword ptr [rsp + 0x18], rbp       
  0001801DC27A  4889742420                 mov qword ptr [rsp + 0x20], rsi       
  0001801DC27F  57                         push rdi                              
  0001801DC280  4883EC50                   sub rsp, 0x50                         
  0001801DC284  488BF1                     mov rsi, rcx                          
  0001801DC287  4032ED                     xor bpl, bpl                          
  0001801DC28A  4881C158020000             add rcx, 0x258                        
  0001801DC291  E87AF8FDFF                 call 0x1801bbb10                         -> 0x1801BBB10 (.text)
  0001801DC296  488D9EB0020000             lea rbx, [rsi + 0x2b0]                
  0001801DC29D  488BCB                     mov rcx, rbx                          
  0001801DC2A0  E86BF8FDFF                 call 0x1801bbb10                         -> 0x1801BBB10 (.text)
  0001801DC2A5  33C9                       xor ecx, ecx                          
  0001801DC2A7  E8E475FCFF                 call 0x1801a3890                         -> 0x1801A3890 (.text)
  0001801DC2AC  BA0C5A0000                 mov edx, 0x5a0c                       
  0001801DC2B1  488BCE                     mov rcx, rsi                          
  0001801DC2B4  E8C725FEFF                 call 0x1801be880                         -> 0x1801BE880 (.text)
  0001801DC2B9  BA0C5A0000                 mov edx, 0x5a0c                       
  0001801DC2BE  488BCE                     mov rcx, rsi                          
  0001801DC2C1  E83A25FEFF                 call 0x1801be800                         -> 0x1801BE800 (.text)
  0001801DC2C6  488BCE                     mov rcx, rsi                          
  0001801DC2C9  E80217FEFF                 call 0x1801bd9d0                         -> 0x1801BD9D0 (.text)
  0001801DC2CE  84C0                       test al, al                           
  0001801DC2D0  0F85D8000000               jne 0x1801dc3ae                          -> 0x1801DC3AE (.text)
  0001801DC2D6  488D8E58020000             lea rcx, [rsi + 0x258]                
  0001801DC2DD  E8DE16FEFF                 call 0x1801bd9c0                         -> 0x1801BD9C0 (.text)
  0001801DC2E2  84C0                       test al, al                           
  0001801DC2E4  0F84C4000000               je 0x1801dc3ae                           -> 0x1801DC3AE (.text)
  0001801DC2EA  488BCB                     mov rcx, rbx                          
  0001801DC2ED  E8CE16FEFF                 call 0x1801bd9c0                         -> 0x1801BD9C0 (.text)
  0001801DC2F2  84C0                       test al, al                           
  0001801DC2F4  0F84B4000000               je 0x1801dc3ae                           -> 0x1801DC3AE (.text)
  0001801DC2FA  488D8E10030000             lea rcx, [rsi + 0x310]                
  0001801DC301  E88A8C0600                 call 0x180244f90                         -> 0x180244F90 (.text)
  0001801DC306  84C0                       test al, al                           
  0001801DC308  0F85A0000000               jne 0x1801dc3ae                          -> 0x1801DC3AE (.text)
  0001801DC30E  384660                     cmp byte ptr [rsi + 0x60], al         
  0001801DC311  0F8494000000               je 0x1801dc3ab                           -> 0x1801DC3AB (.text)
  0001801DC317  4C638648020000             movsxd r8, dword ptr [rsi + 0x248]    
  0001801DC31E  4C8D15DB3CE2FF             lea r10, [rip - 0x1dc325]                ; -> 0x180000000
  0001801DC325  48639650020000             movsxd rdx, dword ptr [rsi + 0x250]   
  0001801DC32C  48638E4C020000             movsxd rcx, dword ptr [rsi + 0x24c]   
  0001801DC333  48638644020000             movsxd rax, dword ptr [rsi + 0x244]   
  0001801DC33A  470FB68C10C8215300         movzx r9d, byte ptr [r8 + r10 + 0x5321c8]
  0001801DC343  450FB78452B8215300         movzx r8d, word ptr [r10 + rdx*2 + 0x5321b8]
  0001801DC34C  410FB7944AB8215300         movzx edx, word ptr [r10 + rcx*2 + 0x5321b8]
  0001801DC355  488D4C2460                 lea rcx, [rsp + 0x60]                 
  0001801DC35A  420FB68410C0215300         movzx eax, byte ptr [rax + r10 + 0x5321c0]
  0001801DC363  88442420                   mov byte ptr [rsp + 0x20], al         
  0001801DC367  E874F8FBFF                 call 0x18019bbe0                         -> 0x18019BBE0 (.text)
  0001801DC36C  0FB69E40020000             movzx ebx, byte ptr [rsi + 0x240]     
  0001801DC373  B908000000                 mov ecx, 8                            
  0001801DC378  E89368FCFF                 call 0x1801a2c10                         -> 0x1801A2C10 (.text)
  0001801DC37D  85C0                       test eax, eax                         
  0001801DC37F  410F99C1                   setns r9b                             
  0001801DC383  85C0                       test eax, eax                         
  0001801DC385  7814                       js 0x1801dc39b                           -> 0x1801DC39B (.text)
  0001801DC387  0FB74C2460                 movzx ecx, word ptr [rsp + 0x60]      
  0001801DC38C  0FB7442462                 movzx eax, word ptr [rsp + 0x62]      
  0001801DC391  6689442460                 mov word ptr [rsp + 0x60], ax         
  0001801DC396  66894C2462                 mov word ptr [rsp + 0x62], cx         
  0001801DC39B  440FB6C3                   movzx r8d, bl                         
  0001801DC39F  488D542460                 lea rdx, [rsp + 0x60]                 
  0001801DC3A4  33C9                       xor ecx, ecx                          
  0001801DC3A6  E87500FCFF                 call 0x18019c420                         -> 0x18019C420 (.text)
  0001801DC3AB  40B501                     mov bpl, 1                            
  0001801DC3AE  80BE0803000000             cmp byte ptr [rsi + 0x308], 0         
  0001801DC3B5  0F852C010000               jne 0x1801dc4e7                          -> 0x1801DC4E7 (.text)
  0001801DC3BB  488D8E10030000             lea rcx, [rsi + 0x310]                
  0001801DC3C2  E8C98B0600                 call 0x180244f90                         -> 0x180244F90 (.text)
  0001801DC3C7  84C0                       test al, al                           
  0001801DC3C9  0F8518010000               jne 0x1801dc4e7                          -> 0x1801DC4E7 (.text)
  0001801DC3CF  488BCE                     mov rcx, rsi                          
  0001801DC3D2  E809F8FDFF                 call 0x1801bbbe0                         -> 0x1801BBBE0 (.text)
  0001801DC3D7  488DBEC0040000             lea rdi, [rsi + 0x4c0]                
  0001801DC3DE  C744243079000000           mov dword ptr [rsp + 0x30], 0x79      
  0001801DC3E6  48837F1810                 cmp qword ptr [rdi + 0x18], 0x10      
  0001801DC3EB  488BC7                     mov rax, rdi                          
  0001801DC3EE  C74424347B000000           mov dword ptr [rsp + 0x34], 0x7b      
  0001801DC3F6  C74424387A000000           mov dword ptr [rsp + 0x38], 0x7a      
  0001801DC3FE  C744243C7C000000           mov dword ptr [rsp + 0x3c], 0x7c      
  0001801DC406  C74424407D000000           mov dword ptr [rsp + 0x40], 0x7d      
  0001801DC40E  48C7471000000000           mov qword ptr [rdi + 0x10], 0         
  0001801DC416  7203                       jb 0x1801dc41b                           -> 0x1801DC41B (.text)
  0001801DC418  488B07                     mov rax, qword ptr [rdi]              
  0001801DC41B  C60000                     mov byte ptr [rax], 0                 
  0001801DC41E  48634658                   movsxd rax, dword ptr [rsi + 0x58]    
  0001801DC422  8B4C8430                   mov ecx, dword ptr [rsp + rax*4 + 0x30]
  0001801DC426  E8E5380100                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801DC42B  488BD0                     mov rdx, rax                          
  0001801DC42E  488BCF                     mov rcx, rdi                          
  0001801DC431  E8AA60E7FF                 call 0x1800524e0                         -> 0x1800524E0 (.text)
  0001801DC436  488B5718                   mov rdx, qword ptr [rdi + 0x18]       
  0001801DC43A  488B4F10                   mov rcx, qword ptr [rdi + 0x10]       
  0001801DC43E  488BC2                     mov rax, rdx                          
  0001801DC441  482BC1                     sub rax, rcx                          
  0001801DC444  4883F801                   cmp rax, 1                            
  0001801DC448  7233                       jb 0x1801dc47d                           -> 0x1801DC47D (.text)
  0001801DC44A  488D4101                   lea rax, [rcx + 1]                    
  0001801DC44E  48894710                   mov qword ptr [rdi + 0x10], rax       
  0001801DC452  488BC7                     mov rax, rdi                          
  0001801DC455  4883FA10                   cmp rdx, 0x10                         
  0001801DC459  7203                       jb 0x1801dc45e                           -> 0x1801DC45E (.text)
  0001801DC45B  488B07                     mov rax, qword ptr [rdi]              
  0001801DC45E  488D1C08                   lea rbx, [rax + rcx]                  
  0001801DC462  41B801000000               mov r8d, 1                            
  0001801DC468  488BCB                     mov rcx, rbx                          
  0001801DC46B  488D15AEB21600             lea rdx, [rip + 0x16b2ae]                ; -> 0x180347720
  0001801DC472  E8993B1200                 call 0x180300010                         -> 0x180300010 (.text)
  0001801DC477  C6430100                   mov byte ptr [rbx + 1], 0             
  0001801DC47B  EB1F                       jmp 0x1801dc49c                          -> 0x1801DC49C (.text)
  0001801DC47D  4533C0                     xor r8d, r8d                          
  0001801DC480  48C744242001000000         mov qword ptr [rsp + 0x20], 1         
  0001801DC489  4C8D0D90B21600             lea r9, [rip + 0x16b290]                 ; -> 0x180347720
  0001801DC490  488BCF                     mov rcx, rdi                          
  0001801DC493  418D5001                   lea edx, [r8 + 1]                     
  0001801DC497  E854FBE2FF                 call 0x18000bff0                         -> 0x18000BFF0 (.text)
  0001801DC49C  B978000000                 mov ecx, 0x78                         
  0001801DC4A1  E86A380100                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801DC4A6  49C7C0FFFFFFFF             mov r8, 0xffffffffffffffff            
  0001801DC4AD  0F1F00                     nop dword ptr [rax]                   
  0001801DC4B0  49FFC0                     inc r8                                
  0001801DC4B3  42803C0000                 cmp byte ptr [rax + r8], 0            
  0001801DC4B8  75F6                       jne 0x1801dc4b0                          -> 0x1801DC4B0 (.text)
  0001801DC4BA  488BD0                     mov rdx, rax                          
  0001801DC4BD  488BCF                     mov rcx, rdi                          
  0001801DC4C0  E81B40E3FF                 call 0x1800104e0                         -> 0x1800104E0 (.text)
  0001801DC4C5  48837F1810                 cmp qword ptr [rdi + 0x18], 0x10      
  0001801DC4CA  7203                       jb 0x1801dc4cf                           -> 0x1801DC4CF (.text)
  0001801DC4CC  488B3F                     mov rdi, qword ptr [rdi]              
  0001801DC4CF  488BD7                     mov rdx, rdi                          
  0001801DC4D2  488BCE                     mov rcx, rsi                          
  0001801DC4D5  E8D623FEFF                 call 0x1801be8b0                         -> 0x1801BE8B0 (.text)
  0001801DC4DA  BA03000000                 mov edx, 3                            
  0001801DC4DF  488BCE                     mov rcx, rsi                          
  0001801DC4E2  E81923FEFF                 call 0x1801be800                         -> 0x1801BE800 (.text)
  0001801DC4E7  B902000000                 mov ecx, 2                            
  0001801DC4EC  E89F73FCFF                 call 0x1801a3890                         -> 0x1801A3890 (.text)
  0001801DC4F1  488B5C2468                 mov rbx, qword ptr [rsp + 0x68]       
  0001801DC4F6  400FB6C5                   movzx eax, bpl                        
  0001801DC4FA  488B6C2470                 mov rbp, qword ptr [rsp + 0x70]       
  0001801DC4FF  488B742478                 mov rsi, qword ptr [rsp + 0x78]       
  0001801DC504  4883C450                   add rsp, 0x50                         
  0001801DC508  5F                         pop rdi                               
  0001801DC509  C3                         ret                                   
