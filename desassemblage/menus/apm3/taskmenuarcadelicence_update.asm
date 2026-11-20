; taskmenuarcadelicence_update.asm  --  TaskMenuArcadeLicenceChallenge_Update
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801DC050 - 0x1801DC266  (534 octets)
;
; A QUOI : Pose le MODE DE JEU = 2 (License Challenge) en 0x1801DC179.
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
  0001801DC050  48895C2410                 mov qword ptr [rsp + 0x10], rbx       
  0001801DC055  48896C2418                 mov qword ptr [rsp + 0x18], rbp       
  0001801DC05A  56                         push rsi                              
  0001801DC05B  57                         push rdi                              
  0001801DC05C  4156                       push r14                              
  0001801DC05E  4883EC30                   sub rsp, 0x30                         
  0001801DC062  488BD9                     mov rbx, rcx                          
  0001801DC065  4032ED                     xor bpl, bpl                          
  0001801DC068  4881C140020000             add rcx, 0x240                        
  0001801DC06F  E89CFAFDFF                 call 0x1801bbb10                         -> 0x1801BBB10 (.text)
  0001801DC074  33C9                       xor ecx, ecx                          
  0001801DC076  E81578FCFF                 call 0x1801a3890                         -> 0x1801A3890 (.text)
  0001801DC07B  BA0C5A0000                 mov edx, 0x5a0c                       
  0001801DC080  488BCB                     mov rcx, rbx                          
  0001801DC083  E8F827FEFF                 call 0x1801be880                         -> 0x1801BE880 (.text)
  0001801DC088  BA0C5A0000                 mov edx, 0x5a0c                       
  0001801DC08D  488BCB                     mov rcx, rbx                          
  0001801DC090  E86B27FEFF                 call 0x1801be800                         -> 0x1801BE800 (.text)
  0001801DC095  4032FF                     xor dil, dil                          
  0001801DC098  488DB338080000             lea rsi, [rbx + 0x838]                
  0001801DC09F  90                         nop                                   
  0001801DC0A0  400FB6CF                   movzx ecx, dil                        
  0001801DC0A4  E8478AFFFF                 call 0x1801d4af0                         -> 0x1801D4AF0 (.text)
  0001801DC0A9  84C0                       test al, al                           
  0001801DC0AB  488D7601                   lea rsi, [rsi + 1]                    
  0001801DC0AF  0F94C0                     sete al                               
  0001801DC0B2  40FEC7                     inc dil                               
  0001801DC0B5  8846FF                     mov byte ptr [rsi - 1], al            
  0001801DC0B8  4080FF32                   cmp dil, 0x32                         
  0001801DC0BC  72E2                       jb 0x1801dc0a0                           -> 0x1801DC0A0 (.text)
  0001801DC0BE  488D8BA0020000             lea rcx, [rbx + 0x2a0]                
  0001801DC0C5  E8D68D0600                 call 0x180244ea0                         -> 0x180244EA0 (.text)
  0001801DC0CA  84C0                       test al, al                           
  0001801DC0CC  740D                       je 0x1801dc0db                           -> 0x1801DC0DB (.text)
  0001801DC0CE  80BB0003000000             cmp byte ptr [rbx + 0x300], 0         
  0001801DC0D5  0F846A010000               je 0x1801dc245                           -> 0x1801DC245 (.text)
  0001801DC0DB  E830C9FDFF                 call 0x1801b8a10                         -> 0x1801B8A10 (.text)
  0001801DC0E0  488D883C4B0000             lea rcx, [rax + 0x4b3c]               
  0001801DC0E7  E81484FFFF                 call 0x1801d4500                         -> 0x1801D4500 (.text)
  0001801DC0EC  0FB7C8                     movzx ecx, ax                         
  0001801DC0EF  E88C7AFFFF                 call 0x1801d3b80                         -> 0x1801D3B80 (.text)
  0001801DC0F4  83F80B                     cmp eax, 0xb                          
  0001801DC0F7  7C2D                       jl 0x1801dc126                           -> 0x1801DC126 (.text)
  0001801DC0F9  488D8B40050000             lea rcx, [rbx + 0x540]                
  0001801DC100  E89B8D0600                 call 0x180244ea0                         -> 0x180244EA0 (.text)
  0001801DC105  84C0                       test al, al                           
  0001801DC107  741D                       je 0x1801dc126                           -> 0x1801DC126 (.text)
  0001801DC109  80BB6A08000000             cmp byte ptr [rbx + 0x86a], 0         
  0001801DC110  7414                       je 0x1801dc126                           -> 0x1801DC126 (.text)
  0001801DC112  80BBA005000000             cmp byte ptr [rbx + 0x5a0], 0         
  0001801DC119  0F8426010000               je 0x1801dc245                           -> 0x1801DC245 (.text)
  0001801DC11F  C6836A08000000             mov byte ptr [rbx + 0x86a], 0         
  0001801DC126  488BCB                     mov rcx, rbx                          
  0001801DC129  E8A218FEFF                 call 0x1801bd9d0                         -> 0x1801BD9D0 (.text)
  0001801DC12E  84C0                       test al, al                           
  0001801DC130  754F                       jne 0x1801dc181                          -> 0x1801DC181 (.text)
  0001801DC132  488D8B40020000             lea rcx, [rbx + 0x240]                
  0001801DC139  E88218FEFF                 call 0x1801bd9c0                         -> 0x1801BD9C0 (.text)
  0001801DC13E  84C0                       test al, al                           
  0001801DC140  743F                       je 0x1801dc181                           -> 0x1801DC181 (.text)
  0001801DC142  807B6000                   cmp byte ptr [rbx + 0x60], 0          
  0001801DC146  7436                       je 0x1801dc17e                           -> 0x1801DC17E (.text)
  0001801DC148  BADC000000                 mov edx, 0xdc                         
  0001801DC14D  C644242002                 mov byte ptr [rsp + 0x20], 2          
  0001801DC152  448BC2                     mov r8d, edx                          
  0001801DC155  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801DC15A  41B12D                     mov r9b, 0x2d                         
  0001801DC15D  E87EFAFBFF                 call 0x18019bbe0                         -> 0x18019BBE0 (.text)
  0001801DC162  8B4B58                     mov ecx, dword ptr [rbx + 0x58]       
  0001801DC165  E8D697FFFF                 call 0x1801d5940                         -> 0x1801D5940 (.text)
  0001801DC16A  4533C9                     xor r9d, r9d                          
  0001801DC16D  488D542450                 lea rdx, [rsp + 0x50]                 
  0001801DC172  41B002                     mov r8b, 2                            
  0001801DC175  418D4902                   lea ecx, [r9 + 2]                     
  0001801DC179  E8A202FCFF                 call 0x18019c420                         -> 0x18019C420 (.text)
  0001801DC17E  40B501                     mov bpl, 1                            
  0001801DC181  80BB9802000000             cmp byte ptr [rbx + 0x298], 0         
  0001801DC188  0F85B7000000               jne 0x1801dc245                          -> 0x1801DC245 (.text)
  0001801DC18E  488BCB                     mov rcx, rbx                          
  0001801DC191  E84AFAFDFF                 call 0x1801bbbe0                         -> 0x1801BBBE0 (.text)
  0001801DC196  E875C8FDFF                 call 0x1801b8a10                         -> 0x1801B8A10 (.text)
  0001801DC19B  488D883C4B0000             lea rcx, [rax + 0x4b3c]               
  0001801DC1A2  E85983FFFF                 call 0x1801d4500                         -> 0x1801D4500 (.text)
  0001801DC1A7  0FB7C8                     movzx ecx, ax                         
  0001801DC1AA  E8D179FFFF                 call 0x1801d3b80                         -> 0x1801D3B80 (.text)
  0001801DC1AF  83F80B                     cmp eax, 0xb                          
  0001801DC1B2  7C40                       jl 0x1801dc1f4                           -> 0x1801DC1F4 (.text)
  0001801DC1B4  80BB9802000000             cmp byte ptr [rbx + 0x298], 0         
  0001801DC1BB  7537                       jne 0x1801dc1f4                          -> 0x1801DC1F4 (.text)
  0001801DC1BD  807B6000                   cmp byte ptr [rbx + 0x60], 0          
  0001801DC1C1  7531                       jne 0x1801dc1f4                          -> 0x1801DC1F4 (.text)
  0001801DC1C3  33D2                       xor edx, edx                          
  0001801DC1C5  8D4A08                     lea ecx, [rdx + 8]                    
  0001801DC1C8  E8D36AFCFF                 call 0x1801a2ca0                         -> 0x1801A2CA0 (.text)
  0001801DC1CD  85C0                       test eax, eax                         
  0001801DC1CF  7823                       js 0x1801dc1f4                           -> 0x1801DC1F4 (.text)
  0001801DC1D1  80BB6A08000000             cmp byte ptr [rbx + 0x86a], 0         
  0001801DC1D8  751A                       jne 0x1801dc1f4                          -> 0x1801DC1F4 (.text)
  0001801DC1DA  488D8B40050000             lea rcx, [rbx + 0x540]                
  0001801DC1E1  488D15486C3500             lea rdx, [rip + 0x356c48]                ; -> 0x180532E30  "DIFFICULTY CHANGE WINDOW"
  0001801DC1E8  E843960600                 call 0x180245830                         -> 0x180245830 (.text)
  0001801DC1ED  C6836A08000001             mov byte ptr [rbx + 0x86a], 1         
  0001801DC1F4  BA7F000000                 mov edx, 0x7f                         
  0001801DC1F9  488BCB                     mov rcx, rbx                          
  0001801DC1FC  E87F26FEFF                 call 0x1801be880                         -> 0x1801BE880 (.text)
  0001801DC201  4032FF                     xor dil, dil                          
  0001801DC204  E807C8FDFF                 call 0x1801b8a10                         -> 0x1801B8A10 (.text)
  0001801DC209  488D883C4B0000             lea rcx, [rax + 0x4b3c]               
  0001801DC210  E8EB82FFFF                 call 0x1801d4500                         -> 0x1801D4500 (.text)
  0001801DC215  0FB7C8                     movzx ecx, ax                         
  0001801DC218  E86379FFFF                 call 0x1801d3b80                         -> 0x1801D3B80 (.text)
  0001801DC21D  83F80B                     cmp eax, 0xb                          
  0001801DC220  440FB6C7                   movzx r8d, dil                        
  0001801DC224  BA01000000                 mov edx, 1                            
  0001801DC229  B824000000                 mov eax, 0x24                         
  0001801DC22E  440F4DC2                   cmovge r8d, edx                       
  0001801DC232  488BCB                     mov rcx, rbx                          
  0001801DC235  4584C0                     test r8b, r8b                         
  0001801DC238  BA03000000                 mov edx, 3                            
  0001801DC23D  0F45D0                     cmovne edx, eax                       
  0001801DC240  E8BB25FEFF                 call 0x1801be800                         -> 0x1801BE800 (.text)
  0001801DC245  B902000000                 mov ecx, 2                            
  0001801DC24A  E84176FCFF                 call 0x1801a3890                         -> 0x1801A3890 (.text)
  0001801DC24F  488B5C2458                 mov rbx, qword ptr [rsp + 0x58]       
  0001801DC254  400FB6C5                   movzx eax, bpl                        
  0001801DC258  488B6C2460                 mov rbp, qword ptr [rsp + 0x60]       
  0001801DC25D  4883C430                   add rsp, 0x30                         
  0001801DC261  415E                       pop r14                               
  0001801DC263  5F                         pop rdi                               
  0001801DC264  5E                         pop rsi                               
  0001801DC265  C3                         ret                                   
