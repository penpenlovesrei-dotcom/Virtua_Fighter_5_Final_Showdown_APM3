; page_multi.asm  --  TaskMenuMulti::draw  (la page MULTI MENU)
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801E10E0 - 0x1801E142B  (843 octets)
;
; A QUOI : Creneau [4] de la vtable TaskMenuMulti 0x180532B48. Jumelle de FUN_18020CC90 cote REVO, dont MENU.md 419.92 ne savait pas ce qu'elle etait : son en-tete 0x17C tombe ENTRE OFFLINE VERSUS (0x17B) et ONLINE BATTLE (0x17D), et ses lignes 0x1DC 0x1DD 0x1DE se lisent Custom Match / Create Match / Custom Match -- une page EN LIGNE, ce que le RTTI confirme maintenant.
;
; D'OU VIENT LE NOM : RTTI : VF5RE/analysis/rtti_apm3.txt, vtable 0x180532B48 creneau [4] ; pour la lecture des libelles, MENU.md section 419.92
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
  0001801E10E0  488BC4                     mov rax, rsp                          
  0001801E10E3  55                         push rbp                              
  0001801E10E4  57                         push rdi                              
  0001801E10E5  4154                       push r12                              
  0001801E10E7  4156                       push r14                              
  0001801E10E9  4157                       push r15                              
  0001801E10EB  488D6888                   lea rbp, [rax - 0x78]                 
  0001801E10EF  4881EC50010000             sub rsp, 0x150                        
  0001801E10F6  48C745E0FEFFFFFF           mov qword ptr [rbp - 0x20], 0xfffffffffffffffe
  0001801E10FE  48895818                   mov qword ptr [rax + 0x18], rbx       
  0001801E1102  48897020                   mov qword ptr [rax + 0x20], rsi       
  0001801E1106  C5F82970C8                 vmovaps xmmword ptr [rax - 0x38], xmm6
  0001801E110B  C5F82978B8                 vmovaps xmmword ptr [rax - 0x48], xmm7
  0001801E1110  C5782940A8                 vmovaps xmmword ptr [rax - 0x58], xmm8
  0001801E1115  C578294898                 vmovaps xmmword ptr [rax - 0x68], xmm9
  0001801E111A  C578295088                 vmovaps xmmword ptr [rax - 0x78], xmm10
  0001801E111F  C578299878FFFFFF           vmovaps xmmword ptr [rax - 0x88], xmm11
  0001801E1127  488BF9                     mov rdi, rcx                          
  0001801E112A  C7442440D8010000           mov dword ptr [rsp + 0x40], 0x1d8     
  0001801E1132  C7442444D9010000           mov dword ptr [rsp + 0x44], 0x1d9     
  0001801E113A  C7442448DA010000           mov dword ptr [rsp + 0x48], 0x1da     
  0001801E1142  C5F857C0                   vxorps xmm0, xmm0, xmm0               
  0001801E1146  C5FA11442430               vmovss dword ptr [rsp + 0x30], xmm0   
  0001801E114C  C5FA11442434               vmovss dword ptr [rsp + 0x34], xmm0   
  0001801E1152  C5FA11442438               vmovss dword ptr [rsp + 0x38], xmm0   
  0001801E1158  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E115D  E85E97FBFF                 call 0x18019a8c0                         -> 0x18019A8C0 (.text)
  0001801E1162  90                         nop                                   
  0001801E1163  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E1167  E86498FBFF                 call 0x18019a9d0                         -> 0x18019A9D0 (.text)
  0001801E116C  E82F69FAFF                 call 0x180187aa0                         -> 0x180187AA0 (.text)
  0001801E1171  448BE0                     mov r12d, eax                         
  0001801E1174  B902000000                 mov ecx, 2                            
  0001801E1179  E8326BFAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801E117E  488D8F40020000             lea rcx, [rdi + 0x240]                
  0001801E1185  33DB                       xor ebx, ebx                          
  0001801E1187  48895C2420                 mov qword ptr [rsp + 0x20], rbx       
  0001801E118C  41B101                     mov r9b, 1                            
  0001801E118F  4C8D05F2012300             lea r8, [rip + 0x2301f2]                 ; -> 0x180411388  "head_tit_ct"
  0001801E1196  488D542430                 lea rdx, [rsp + 0x30]                 
  0001801E119B  E8D0BBFDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E11A0  C5FA1035D09D1600           vmovss xmm6, dword ptr [rip + 0x169dd0]   ; -> 0x18034AF78
  0001801E11A8  C57A100D9C5B1600           vmovss xmm9, dword ptr [rip + 0x165b9c]   ; -> 0x180346D4C
  0001801E11B0  84C0                       test al, al                           
  0001801E11B2  0F8492000000               je 0x1801e124a                           -> 0x1801E124A (.text)
  0001801E11B8  8D5302                     lea edx, [rbx + 2]                    
  0001801E11BB  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E11BF  E82CA5FBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801E11C4  C5F828CE                   vmovaps xmm1, xmm6                    
  0001801E11C8  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E11CC  E85FA6FBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801E11D1  488D45A0                   lea rax, [rbp - 0x60]                 
  0001801E11D5  48894598                   mov qword ptr [rbp - 0x68], rax       
  0001801E11D9  C744247412000000           mov dword ptr [rsp + 0x74], 0x12      
  0001801E11E1  C5FA104C2430               vmovss xmm1, dword ptr [rsp + 0x30]   
  0001801E11E7  C5FA114D8C                 vmovss dword ptr [rbp - 0x74], xmm1   
  0001801E11EC  C5FA10442434               vmovss xmm0, dword ptr [rsp + 0x34]   
  0001801E11F2  C5FA114590                 vmovss dword ptr [rbp - 0x70], xmm0   
  0001801E11F7  C5FA114D84                 vmovss dword ptr [rbp - 0x7c], xmm1   
  0001801E11FC  C5FA114588                 vmovss dword ptr [rbp - 0x78], xmm0   
  0001801E1201  C744247C09000000           mov dword ptr [rsp + 0x7c], 9         
  0001801E1209  C5B2594C2438               vmulss xmm1, xmm9, dword ptr [rsp + 0x38]
  0001801E120F  C5FA2CC1                   vcvttss2si eax, xmm1                  
  0001801E1213  66C78580000000FFB7         mov word ptr [rbp + 0x80], 0xb7ff     
  0001801E121C  C6858200000039             mov byte ptr [rbp + 0x82], 0x39       
  0001801E1223  888583000000               mov byte ptr [rbp + 0x83], al         
  0001801E1229  8B8580000000               mov eax, dword ptr [rbp + 0x80]       
  0001801E122F  89442458                   mov dword ptr [rsp + 0x58], eax       
  0001801E1233  B979010000                 mov ecx, 0x179                        
  0001801E1238  E8D3EA0000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E123D  488BD0                     mov rdx, rax                          
  0001801E1240  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E1245  E8B6A0FBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E124A  488D8F98020000             lea rcx, [rdi + 0x298]                
  0001801E1251  E8BAC7FDFF                 call 0x1801bda10                         -> 0x1801BDA10 (.text)
  0001801E1256  84C0                       test al, al                           
  0001801E1258  0F8484010000               je 0x1801e13e2                           -> 0x1801E13E2 (.text)
  0001801E125E  48895C2420                 mov qword ptr [rsp + 0x20], rbx       
  0001801E1263  41B101                     mov r9b, 1                            
  0001801E1266  4C8D05BB971B00             lea r8, [rip + 0x1b97bb]                 ; -> 0x18039AA28  "p_txt_01_lt"
  0001801E126D  488D542430                 lea rdx, [rsp + 0x30]                 
  0001801E1272  488D8F98020000             lea rcx, [rdi + 0x298]                
  0001801E1279  E8F2BAFDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E127E  BA01000000                 mov edx, 1                            
  0001801E1283  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E1287  E864A4FBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801E128C  BA02000000                 mov edx, 2                            
  0001801E1291  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E1295  E8D6A5FBFF                 call 0x18019b870                         -> 0x18019B870 (.text)
  0001801E129A  C5F828CE                   vmovaps xmm1, xmm6                    
  0001801E129E  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E12A2  E889A5FBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801E12A7  C5FA1005096E1600           vmovss xmm0, dword ptr [rip + 0x166e09]   ; -> 0x1803480B8
  0001801E12AF  C5FA1145D4                 vmovss dword ptr [rbp - 0x2c], xmm0   
  0001801E12B4  C5FA100D54A11600           vmovss xmm1, dword ptr [rip + 0x16a154]   ; -> 0x18034B410
  0001801E12BC  C5FA114DD8                 vmovss dword ptr [rbp - 0x28], xmm1   
  0001801E12C1  488D45A0                   lea rax, [rbp - 0x60]                 
  0001801E12C5  48894598                   mov qword ptr [rbp - 0x68], rax       
  0001801E12C9  C744247412000000           mov dword ptr [rsp + 0x74], 0x12      
  0001801E12D1  C5FA105DC8                 vmovss xmm3, dword ptr [rbp - 0x38]   
  0001801E12D6  C56258D9                   vaddss xmm11, xmm3, xmm1              
  0001801E12DA  C57A10442430               vmovss xmm8, dword ptr [rsp + 0x30]   
  0001801E12E0  C5FA107C2434               vmovss xmm7, dword ptr [rsp + 0x34]   
  0001801E12E6  399F24020000               cmp dword ptr [rdi + 0x224], ebx      
  0001801E12EC  0F8CF0000000               jl 0x1801e13e2                           -> 0x1801E13E2 (.text)
  0001801E12F2  488DB7F1020000             lea rsi, [rdi + 0x2f1]                
  0001801E12F9  4C8D742440                 lea r14, [rsp + 0x40]                 
  0001801E12FE  C57A1015325A1600           vmovss xmm10, dword ptr [rip + 0x165a32]   ; -> 0x180346D38
  0001801E1306  66660F1F840000000000       nop word ptr [rax + rax]              
  0001801E1310  C5FA10742438               vmovss xmm6, dword ptr [rsp + 0x38]   
  0001801E1316  803E00                     cmp byte ptr [rsi], 0                 
  0001801E1319  7405                       je 0x1801e1320                           -> 0x1801E1320 (.text)
  0001801E131B  C4C14A59F2                 vmulss xmm6, xmm6, xmm10              
  0001801E1320  8B4758                     mov eax, dword ptr [rdi + 0x58]       
  0001801E1323  3BD8                       cmp ebx, eax                          
  0001801E1325  7518                       jne 0x1801e133f                          -> 0x1801E133F (.text)
  0001801E1327  C5F828D7                   vmovaps xmm2, xmm7                    
  0001801E132B  C4C17828C8                 vmovaps xmm1, xmm8                    
  0001801E1330  488D8F98020000             lea rcx, [rdi + 0x298]                
  0001801E1337  E834D1FDFF                 call 0x1801be470                         -> 0x1801BE470 (.text)
  0001801E133C  8B4758                     mov eax, dword ptr [rdi + 0x58]       
  0001801E133F  C57A11458C                 vmovss dword ptr [rbp - 0x74], xmm8   
  0001801E1344  C5FA117D90                 vmovss dword ptr [rbp - 0x70], xmm7   
  0001801E1349  C57A114584                 vmovss dword ptr [rbp - 0x7c], xmm8   
  0001801E134E  C5FA117D88                 vmovss dword ptr [rbp - 0x78], xmm7   
  0001801E1353  C744247C09000000           mov dword ptr [rsp + 0x7c], 9         
  0001801E135B  C4C14A59C1                 vmulss xmm0, xmm6, xmm9               
  0001801E1360  3BD8                       cmp ebx, eax                          
  0001801E1362  C5FA2CC0                   vcvttss2si eax, xmm0                  
  0001801E1366  751E                       jne 0x1801e1386                          -> 0x1801E1386 (.text)
  0001801E1368  66C78580000000FF5B         mov word ptr [rbp + 0x80], 0x5bff     
  0001801E1371  C685820000005B             mov byte ptr [rbp + 0x82], 0x5b       
  0001801E1378  888583000000               mov byte ptr [rbp + 0x83], al         
  0001801E137E  8B8580000000               mov eax, dword ptr [rbp + 0x80]       
  0001801E1384  EB1C                       jmp 0x1801e13a2                          -> 0x1801E13A2 (.text)
  0001801E1386  66C78588000000C6C8         mov word ptr [rbp + 0x88], 0xc8c6     
  0001801E138F  C6858A000000D0             mov byte ptr [rbp + 0x8a], 0xd0       
  0001801E1396  88858B000000               mov byte ptr [rbp + 0x8b], al         
  0001801E139C  8B8588000000               mov eax, dword ptr [rbp + 0x88]       
  0001801E13A2  89442458                   mov dword ptr [rsp + 0x58], eax       
  0001801E13A6  418B0E                     mov ecx, dword ptr [r14]              
  0001801E13A9  E862E90000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E13AE  4C8BC0                     mov r8, rax                           
  0001801E13B1  488D1540691600             lea rdx, [rip + 0x166940]                ; -> 0x180347CF8
  0001801E13B8  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E13BD  E83E9FFBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E13C2  C4C14258FB                 vaddss xmm7, xmm7, xmm11              
  0001801E13C7  FFC3                       inc ebx                               
  0001801E13C9  48FFC6                     inc rsi                               
  0001801E13CC  4983C604                   add r14, 4                            
  0001801E13D0  3B9F24020000               cmp ebx, dword ptr [rdi + 0x224]      
  0001801E13D6  7F0A                       jg 0x1801e13e2                           -> 0x1801E13E2 (.text)
  0001801E13D8  C5FA105DC8                 vmovss xmm3, dword ptr [rbp - 0x38]   
  0001801E13DD  E92EFFFFFF                 jmp 0x1801e1310                          -> 0x1801E1310 (.text)
  0001801E13E2  418BCC                     mov ecx, r12d                         
  0001801E13E5  E8C668FAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801E13EA  90                         nop                                   
  0001801E13EB  4C8D9C2450010000           lea r11, [rsp + 0x150]                
  0001801E13F3  498B5B40                   mov rbx, qword ptr [r11 + 0x40]       
  0001801E13F7  498B7348                   mov rsi, qword ptr [r11 + 0x48]       
  0001801E13FB  C4C1782873F0               vmovaps xmm6, xmmword ptr [r11 - 0x10]
  0001801E1401  C4C178287BE0               vmovaps xmm7, xmmword ptr [r11 - 0x20]
  0001801E1407  C441782843D0               vmovaps xmm8, xmmword ptr [r11 - 0x30]
  0001801E140D  C44178284BC0               vmovaps xmm9, xmmword ptr [r11 - 0x40]
  0001801E1413  C441782853B0               vmovaps xmm10, xmmword ptr [r11 - 0x50]
  0001801E1419  C44178285BA0               vmovaps xmm11, xmmword ptr [r11 - 0x60]
  0001801E141F  498BE3                     mov rsp, r11                          
  0001801E1422  415F                       pop r15                               
  0001801E1424  415E                       pop r14                               
  0001801E1426  415C                       pop r12                               
  0001801E1428  5F                         pop rdi                               
  0001801E1429  5D                         pop rbp                               
  0001801E142A  C3                         ret                                   
