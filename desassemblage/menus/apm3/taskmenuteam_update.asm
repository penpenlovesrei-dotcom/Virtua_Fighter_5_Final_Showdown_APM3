; taskmenuteam_update.asm  --  TaskMenuTeam_Update
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801A4160 - 0x1801A42C2  (354 octets)
;
; A QUOI : Pose le MODE DE JEU = 3 (Special Sparring) en 0x1801A4252.
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
  0001801A4160  48895C2408                 mov qword ptr [rsp + 8], rbx          
  0001801A4165  48896C2410                 mov qword ptr [rsp + 0x10], rbp       
  0001801A416A  4889742418                 mov qword ptr [rsp + 0x18], rsi       
  0001801A416F  57                         push rdi                              
  0001801A4170  4883EC20                   sub rsp, 0x20                         
  0001801A4174  488BD9                     mov rbx, rcx                          
  0001801A4177  4032F6                     xor sil, sil                          
  0001801A417A  4881C140020000             add rcx, 0x240                        
  0001801A4181  E88A790100                 call 0x1801bbb10                         -> 0x1801BBB10 (.text)
  0001801A4186  488D8B98020000             lea rcx, [rbx + 0x298]                
  0001801A418D  E87E790100                 call 0x1801bbb10                         -> 0x1801BBB10 (.text)
  0001801A4192  33C9                       xor ecx, ecx                          
  0001801A4194  E8F7F6FFFF                 call 0x1801a3890                         -> 0x1801A3890 (.text)
  0001801A4199  BA0C5A0000                 mov edx, 0x5a0c                       
  0001801A419E  488BCB                     mov rcx, rbx                          
  0001801A41A1  E8DAA60100                 call 0x1801be880                         -> 0x1801BE880 (.text)
  0001801A41A6  BA0C5A0000                 mov edx, 0x5a0c                       
  0001801A41AB  488BCB                     mov rcx, rbx                          
  0001801A41AE  E84DA60100                 call 0x1801be800                         -> 0x1801BE800 (.text)
  0001801A41B3  4038B3C0040000             cmp byte ptr [rbx + 0x4c0], sil       
  0001801A41BA  744E                       je 0x1801a420a                           -> 0x1801A420A (.text)
  0001801A41BC  488D8BE8030000             lea rcx, [rbx + 0x3e8]                
  0001801A41C3  E848980100                 call 0x1801bda10                         -> 0x1801BDA10 (.text)
  0001801A41C8  84C0                       test al, al                           
  0001801A41CA  740D                       je 0x1801a41d9                           -> 0x1801A41D9 (.text)
  0001801A41CC  BA15000000                 mov edx, 0x15                         
  0001801A41D1  488BCB                     mov rcx, rbx                          
  0001801A41D4  E827A60100                 call 0x1801be800                         -> 0x1801BE800 (.text)
  0001801A41D9  488D8B20030000             lea rcx, [rbx + 0x320]                
  0001801A41E0  E8AB8C0100                 call 0x1801bce90                         -> 0x1801BCE90 (.text)
  0001801A41E5  85C0                       test eax, eax                         
  0001801A41E7  0F88B2000000               js 0x1801a429f                           -> 0x1801A429F (.text)
  0001801A41ED  BA2D000000                 mov edx, 0x2d                         
  0001801A41F2  C683C004000000             mov byte ptr [rbx + 0x4c0], 0         
  0001801A41F9  488D8B98020000             lea rcx, [rbx + 0x298]                
  0001801A4200  E81B980100                 call 0x1801bda20                         -> 0x1801BDA20 (.text)
  0001801A4205  E995000000                 jmp 0x1801a429f                          -> 0x1801A429F (.text)
  0001801A420A  488BCB                     mov rcx, rbx                          
  0001801A420D  E8BE970100                 call 0x1801bd9d0                         -> 0x1801BD9D0 (.text)
  0001801A4212  84C0                       test al, al                           
  0001801A4214  754E                       jne 0x1801a4264                          -> 0x1801A4264 (.text)
  0001801A4216  488D8B40020000             lea rcx, [rbx + 0x240]                
  0001801A421D  E89E970100                 call 0x1801bd9c0                         -> 0x1801BD9C0 (.text)
  0001801A4222  84C0                       test al, al                           
  0001801A4224  743E                       je 0x1801a4264                           -> 0x1801A4264 (.text)
  0001801A4226  488D8B98020000             lea rcx, [rbx + 0x298]                
  0001801A422D  E88E970100                 call 0x1801bd9c0                         -> 0x1801BD9C0 (.text)
  0001801A4232  84C0                       test al, al                           
  0001801A4234  742E                       je 0x1801a4264                           -> 0x1801A4264 (.text)
  0001801A4236  807B6000                   cmp byte ptr [rbx + 0x60], 0          
  0001801A423A  7425                       je 0x1801a4261                           -> 0x1801A4261 (.text)
  0001801A423C  440FB683D8040000           movzx r8d, byte ptr [rbx + 0x4d8]     
  0001801A4244  488D93D0040000             lea rdx, [rbx + 0x4d0]                
  0001801A424B  4533C9                     xor r9d, r9d                          
  0001801A424E  418D4903                   lea ecx, [r9 + 3]                     
  0001801A4252  E8C981FFFF                 call 0x18019c420                         -> 0x18019C420 (.text)
  0001801A4257  C70543D15A0000000000       mov dword ptr [rip + 0x5ad143], 0        ; -> 0x1807513A4
  0001801A4261  40B601                     mov sil, 1                            
  0001801A4264  80BBF002000000             cmp byte ptr [rbx + 0x2f0], 0         
  0001801A426B  7532                       jne 0x1801a429f                          -> 0x1801A429F (.text)
  0001801A426D  488D8B98020000             lea rcx, [rbx + 0x298]                
  0001801A4274  E897970100                 call 0x1801bda10                         -> 0x1801BDA10 (.text)
  0001801A4279  84C0                       test al, al                           
  0001801A427B  7422                       je 0x1801a429f                           -> 0x1801A429F (.text)
  0001801A427D  488BCB                     mov rcx, rbx                          
  0001801A4280  E85B790100                 call 0x1801bbbe0                         -> 0x1801BBBE0 (.text)
  0001801A4285  BA80000000                 mov edx, 0x80                         
  0001801A428A  488BCB                     mov rcx, rbx                          
  0001801A428D  E8EEA50100                 call 0x1801be880                         -> 0x1801BE880 (.text)
  0001801A4292  BA03000000                 mov edx, 3                            
  0001801A4297  488BCB                     mov rcx, rbx                          
  0001801A429A  E861A50100                 call 0x1801be800                         -> 0x1801BE800 (.text)
  0001801A429F  B902000000                 mov ecx, 2                            
  0001801A42A4  E8E7F5FFFF                 call 0x1801a3890                         -> 0x1801A3890 (.text)
  0001801A42A9  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001801A42AE  400FB6C6                   movzx eax, sil                        
  0001801A42B2  488B742440                 mov rsi, qword ptr [rsp + 0x40]       
  0001801A42B7  488B6C2438                 mov rbp, qword ptr [rsp + 0x38]       
  0001801A42BC  4883C420                   add rsp, 0x20                         
  0001801A42C0  5F                         pop rdi                               
  0001801A42C1  C3                         ret                                   
