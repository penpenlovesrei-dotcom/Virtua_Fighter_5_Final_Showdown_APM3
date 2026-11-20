; taskmenuscoreattack_update.asm  --  TaskMenuScoreAttack_Update
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801DD6A0 - 0x1801DD799  (249 octets)
;
; A QUOI : Pose le MODE DE JEU = 1 (Score Attack) en 0x1801DD73E.
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
  0001801DD6A0  48895C2410                 mov qword ptr [rsp + 0x10], rbx       
  0001801DD6A5  4889742418                 mov qword ptr [rsp + 0x18], rsi       
  0001801DD6AA  57                         push rdi                              
  0001801DD6AB  4883EC30                   sub rsp, 0x30                         
  0001801DD6AF  488BF9                     mov rdi, rcx                          
  0001801DD6B2  32DB                       xor bl, bl                            
  0001801DD6B4  4881C140020000             add rcx, 0x240                        
  0001801DD6BB  E850E4FDFF                 call 0x1801bbb10                         -> 0x1801BBB10 (.text)
  0001801DD6C0  33C9                       xor ecx, ecx                          
  0001801DD6C2  E8C961FCFF                 call 0x1801a3890                         -> 0x1801A3890 (.text)
  0001801DD6C7  BA0C5A0000                 mov edx, 0x5a0c                       
  0001801DD6CC  488BCF                     mov rcx, rdi                          
  0001801DD6CF  E8AC11FEFF                 call 0x1801be880                         -> 0x1801BE880 (.text)
  0001801DD6D4  BA0C5A0000                 mov edx, 0x5a0c                       
  0001801DD6D9  488BCF                     mov rcx, rdi                          
  0001801DD6DC  E81F11FEFF                 call 0x1801be800                         -> 0x1801BE800 (.text)
  0001801DD6E1  488BCF                     mov rcx, rdi                          
  0001801DD6E4  E8E702FEFF                 call 0x1801bd9d0                         -> 0x1801BD9D0 (.text)
  0001801DD6E9  84C0                       test al, al                           
  0001801DD6EB  7558                       jne 0x1801dd745                          -> 0x1801DD745 (.text)
  0001801DD6ED  488D8F40020000             lea rcx, [rdi + 0x240]                
  0001801DD6F4  E8C702FEFF                 call 0x1801bd9c0                         -> 0x1801BD9C0 (.text)
  0001801DD6F9  84C0                       test al, al                           
  0001801DD6FB  7448                       je 0x1801dd745                           -> 0x1801DD745 (.text)
  0001801DD6FD  385F60                     cmp byte ptr [rdi + 0x60], bl         
  0001801DD700  7441                       je 0x1801dd743                           -> 0x1801DD743 (.text)
  0001801DD702  BADC000000                 mov edx, 0xdc                         
  0001801DD707  C644242002                 mov byte ptr [rsp + 0x20], 2          
  0001801DD70C  448BC2                     mov r8d, edx                          
  0001801DD70F  488D4C2440                 lea rcx, [rsp + 0x40]                 
  0001801DD714  41B12D                     mov r9b, 0x2d                         
  0001801DD717  E8C4E4FBFF                 call 0x18019bbe0                         -> 0x18019BBE0 (.text)
  0001801DD71C  0FB65F58                   movzx ebx, byte ptr [rdi + 0x58]      
  0001801DD720  B908000000                 mov ecx, 8                            
  0001801DD725  E8E654FCFF                 call 0x1801a2c10                         -> 0x1801A2C10 (.text)
  0001801DD72A  85C0                       test eax, eax                         
  0001801DD72C  488D542440                 lea rdx, [rsp + 0x40]                 
  0001801DD731  440FB6C3                   movzx r8d, bl                         
  0001801DD735  B901000000                 mov ecx, 1                            
  0001801DD73A  410F99C1                   setns r9b                             
  0001801DD73E  E85DEDFBFF                 call 0x18019c4a0                         -> 0x18019C4A0 (.text)
  0001801DD743  B301                       mov bl, 1                             
  0001801DD745  80BF9802000000             cmp byte ptr [rdi + 0x298], 0         
  0001801DD74C  752E                       jne 0x1801dd77c                          -> 0x1801DD77C (.text)
  0001801DD74E  488BCF                     mov rcx, rdi                          
  0001801DD751  E88AE4FDFF                 call 0x1801bbbe0                         -> 0x1801BBBE0 (.text)
  0001801DD756  488D97A0020000             lea rdx, [rdi + 0x2a0]                
  0001801DD75D  48837A1810                 cmp qword ptr [rdx + 0x18], 0x10      
  0001801DD762  7203                       jb 0x1801dd767                           -> 0x1801DD767 (.text)
  0001801DD764  488B12                     mov rdx, qword ptr [rdx]              
  0001801DD767  488BCF                     mov rcx, rdi                          
  0001801DD76A  E84111FEFF                 call 0x1801be8b0                         -> 0x1801BE8B0 (.text)
  0001801DD76F  BA03000000                 mov edx, 3                            
  0001801DD774  488BCF                     mov rcx, rdi                          
  0001801DD777  E88410FEFF                 call 0x1801be800                         -> 0x1801BE800 (.text)
  0001801DD77C  B902000000                 mov ecx, 2                            
  0001801DD781  E80A61FCFF                 call 0x1801a3890                         -> 0x1801A3890 (.text)
  0001801DD786  488B742450                 mov rsi, qword ptr [rsp + 0x50]       
  0001801DD78B  0FB6C3                     movzx eax, bl                         
  0001801DD78E  488B5C2448                 mov rbx, qword ptr [rsp + 0x48]       
  0001801DD793  4883C430                   add rsp, 0x30                         
  0001801DD797  5F                         pop rdi                               
  0001801DD798  C3                         ret                                   
