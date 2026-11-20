; page_dojo.asm  --  TaskMenuTraining::draw  (la page DOJO)
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801E1E40 - 0x1801E218B  (843 octets)
;
; A QUOI : La page fille DOJO. En-tete 0x17B grave en 0x1801E1F93. Libelles 0x217 0x218 0x219 graves en 0x1801E1E8A et suivants, octet pour octet dans la meme forme que ceux de REVO (seul l'immediat differe) = Tutorial / Command Training / Free Training. Jumelle de FUN_18020D960 cote REVO (+4).
;
; D'OU VIENT LE NOM : VF5RE/desassemblages/apm3_pages_sousmenus_0x1E1C51.asm ; VF5RE/code_decompile/MENU.md section 419.94
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
  0001801E1E40  488BC4                     mov rax, rsp                          
  0001801E1E43  55                         push rbp                              
  0001801E1E44  57                         push rdi                              
  0001801E1E45  4154                       push r12                              
  0001801E1E47  4156                       push r14                              
  0001801E1E49  4157                       push r15                              
  0001801E1E4B  488D6888                   lea rbp, [rax - 0x78]                 
  0001801E1E4F  4881EC50010000             sub rsp, 0x150                        
  0001801E1E56  48C745E0FEFFFFFF           mov qword ptr [rbp - 0x20], 0xfffffffffffffffe
  0001801E1E5E  48895818                   mov qword ptr [rax + 0x18], rbx       
  0001801E1E62  48897020                   mov qword ptr [rax + 0x20], rsi       
  0001801E1E66  C5F82970C8                 vmovaps xmmword ptr [rax - 0x38], xmm6
  0001801E1E6B  C5F82978B8                 vmovaps xmmword ptr [rax - 0x48], xmm7
  0001801E1E70  C5782940A8                 vmovaps xmmword ptr [rax - 0x58], xmm8
  0001801E1E75  C578294898                 vmovaps xmmword ptr [rax - 0x68], xmm9
  0001801E1E7A  C578295088                 vmovaps xmmword ptr [rax - 0x78], xmm10
  0001801E1E7F  C578299878FFFFFF           vmovaps xmmword ptr [rax - 0x88], xmm11
  0001801E1E87  488BF9                     mov rdi, rcx                          
  0001801E1E8A  C744244017020000           mov dword ptr [rsp + 0x40], 0x217     
  0001801E1E92  C744244418020000           mov dword ptr [rsp + 0x44], 0x218     
  0001801E1E9A  C744244819020000           mov dword ptr [rsp + 0x48], 0x219     
  0001801E1EA2  C5F857C0                   vxorps xmm0, xmm0, xmm0               
  0001801E1EA6  C5FA11442430               vmovss dword ptr [rsp + 0x30], xmm0   
  0001801E1EAC  C5FA11442434               vmovss dword ptr [rsp + 0x34], xmm0   
  0001801E1EB2  C5FA11442438               vmovss dword ptr [rsp + 0x38], xmm0   
  0001801E1EB8  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E1EBD  E8FE89FBFF                 call 0x18019a8c0                         -> 0x18019A8C0 (.text)
  0001801E1EC2  90                         nop                                   
  0001801E1EC3  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E1EC7  E8048BFBFF                 call 0x18019a9d0                         -> 0x18019A9D0 (.text)
  0001801E1ECC  E8CF5BFAFF                 call 0x180187aa0                         -> 0x180187AA0 (.text)
  0001801E1ED1  448BE0                     mov r12d, eax                         
  0001801E1ED4  B902000000                 mov ecx, 2                            
  0001801E1ED9  E8D25DFAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801E1EDE  488D8F40020000             lea rcx, [rdi + 0x240]                
  0001801E1EE5  33DB                       xor ebx, ebx                          
  0001801E1EE7  48895C2420                 mov qword ptr [rsp + 0x20], rbx       
  0001801E1EEC  41B101                     mov r9b, 1                            
  0001801E1EEF  4C8D0592F42200             lea r8, [rip + 0x22f492]                 ; -> 0x180411388  "head_tit_ct"
  0001801E1EF6  488D542430                 lea rdx, [rsp + 0x30]                 
  0001801E1EFB  E870AEFDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E1F00  C5FA103570901600           vmovss xmm6, dword ptr [rip + 0x169070]   ; -> 0x18034AF78
  0001801E1F08  C57A100D3C4E1600           vmovss xmm9, dword ptr [rip + 0x164e3c]   ; -> 0x180346D4C
  0001801E1F10  84C0                       test al, al                           
  0001801E1F12  0F8492000000               je 0x1801e1faa                           -> 0x1801E1FAA (.text)
  0001801E1F18  8D5302                     lea edx, [rbx + 2]                    
  0001801E1F1B  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E1F1F  E8CC97FBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801E1F24  C5F828CE                   vmovaps xmm1, xmm6                    
  0001801E1F28  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E1F2C  E8FF98FBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801E1F31  488D45A0                   lea rax, [rbp - 0x60]                 
  0001801E1F35  48894598                   mov qword ptr [rbp - 0x68], rax       
  0001801E1F39  C744247412000000           mov dword ptr [rsp + 0x74], 0x12      
  0001801E1F41  C5FA104C2430               vmovss xmm1, dword ptr [rsp + 0x30]   
  0001801E1F47  C5FA114D8C                 vmovss dword ptr [rbp - 0x74], xmm1   
  0001801E1F4C  C5FA10442434               vmovss xmm0, dword ptr [rsp + 0x34]   
  0001801E1F52  C5FA114590                 vmovss dword ptr [rbp - 0x70], xmm0   
  0001801E1F57  C5FA114D84                 vmovss dword ptr [rbp - 0x7c], xmm1   
  0001801E1F5C  C5FA114588                 vmovss dword ptr [rbp - 0x78], xmm0   
  0001801E1F61  C744247C09000000           mov dword ptr [rsp + 0x7c], 9         
  0001801E1F69  C5B2594C2438               vmulss xmm1, xmm9, dword ptr [rsp + 0x38]
  0001801E1F6F  C5FA2CC1                   vcvttss2si eax, xmm1                  
  0001801E1F73  66C78580000000FFB7         mov word ptr [rbp + 0x80], 0xb7ff     
  0001801E1F7C  C6858200000039             mov byte ptr [rbp + 0x82], 0x39       
  0001801E1F83  888583000000               mov byte ptr [rbp + 0x83], al         
  0001801E1F89  8B8580000000               mov eax, dword ptr [rbp + 0x80]       
  0001801E1F8F  89442458                   mov dword ptr [rsp + 0x58], eax       
  0001801E1F93  B97B010000                 mov ecx, 0x17b                        
  0001801E1F98  E873DD0000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E1F9D  488BD0                     mov rdx, rax                          
  0001801E1FA0  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E1FA5  E85693FBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E1FAA  488D8F98020000             lea rcx, [rdi + 0x298]                
  0001801E1FB1  E85ABAFDFF                 call 0x1801bda10                         -> 0x1801BDA10 (.text)
  0001801E1FB6  84C0                       test al, al                           
  0001801E1FB8  0F8484010000               je 0x1801e2142                           -> 0x1801E2142 (.text)
  0001801E1FBE  48895C2420                 mov qword ptr [rsp + 0x20], rbx       
  0001801E1FC3  41B101                     mov r9b, 1                            
  0001801E1FC6  4C8D055B8A1B00             lea r8, [rip + 0x1b8a5b]                 ; -> 0x18039AA28  "p_txt_01_lt"
  0001801E1FCD  488D542430                 lea rdx, [rsp + 0x30]                 
  0001801E1FD2  488D8F98020000             lea rcx, [rdi + 0x298]                
  0001801E1FD9  E892ADFDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E1FDE  BA01000000                 mov edx, 1                            
  0001801E1FE3  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E1FE7  E80497FBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801E1FEC  BA02000000                 mov edx, 2                            
  0001801E1FF1  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E1FF5  E87698FBFF                 call 0x18019b870                         -> 0x18019B870 (.text)
  0001801E1FFA  C5F828CE                   vmovaps xmm1, xmm6                    
  0001801E1FFE  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E2002  E82998FBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801E2007  C5FA1005A9601600           vmovss xmm0, dword ptr [rip + 0x1660a9]   ; -> 0x1803480B8
  0001801E200F  C5FA1145D4                 vmovss dword ptr [rbp - 0x2c], xmm0   
  0001801E2014  C5FA100DF4931600           vmovss xmm1, dword ptr [rip + 0x1693f4]   ; -> 0x18034B410
  0001801E201C  C5FA114DD8                 vmovss dword ptr [rbp - 0x28], xmm1   
  0001801E2021  488D45A0                   lea rax, [rbp - 0x60]                 
  0001801E2025  48894598                   mov qword ptr [rbp - 0x68], rax       
  0001801E2029  C744247412000000           mov dword ptr [rsp + 0x74], 0x12      
  0001801E2031  C5FA105DC8                 vmovss xmm3, dword ptr [rbp - 0x38]   
  0001801E2036  C56258D9                   vaddss xmm11, xmm3, xmm1              
  0001801E203A  C57A10442430               vmovss xmm8, dword ptr [rsp + 0x30]   
  0001801E2040  C5FA107C2434               vmovss xmm7, dword ptr [rsp + 0x34]   
  0001801E2046  399F24020000               cmp dword ptr [rdi + 0x224], ebx      
  0001801E204C  0F8CF0000000               jl 0x1801e2142                           -> 0x1801E2142 (.text)
  0001801E2052  488DB7F1020000             lea rsi, [rdi + 0x2f1]                
  0001801E2059  4C8D742440                 lea r14, [rsp + 0x40]                 
  0001801E205E  C57A1015D24C1600           vmovss xmm10, dword ptr [rip + 0x164cd2]   ; -> 0x180346D38
  0001801E2066  66660F1F840000000000       nop word ptr [rax + rax]              
  0001801E2070  C5FA10742438               vmovss xmm6, dword ptr [rsp + 0x38]   
  0001801E2076  803E00                     cmp byte ptr [rsi], 0                 
  0001801E2079  7405                       je 0x1801e2080                           -> 0x1801E2080 (.text)
  0001801E207B  C4C14A59F2                 vmulss xmm6, xmm6, xmm10              
  0001801E2080  8B4758                     mov eax, dword ptr [rdi + 0x58]       
  0001801E2083  3BD8                       cmp ebx, eax                          
  0001801E2085  7518                       jne 0x1801e209f                          -> 0x1801E209F (.text)
  0001801E2087  C5F828D7                   vmovaps xmm2, xmm7                    
  0001801E208B  C4C17828C8                 vmovaps xmm1, xmm8                    
  0001801E2090  488D8F98020000             lea rcx, [rdi + 0x298]                
  0001801E2097  E8D4C3FDFF                 call 0x1801be470                         -> 0x1801BE470 (.text)
  0001801E209C  8B4758                     mov eax, dword ptr [rdi + 0x58]       
  0001801E209F  C57A11458C                 vmovss dword ptr [rbp - 0x74], xmm8   
  0001801E20A4  C5FA117D90                 vmovss dword ptr [rbp - 0x70], xmm7   
  0001801E20A9  C57A114584                 vmovss dword ptr [rbp - 0x7c], xmm8   
  0001801E20AE  C5FA117D88                 vmovss dword ptr [rbp - 0x78], xmm7   
  0001801E20B3  C744247C09000000           mov dword ptr [rsp + 0x7c], 9         
  0001801E20BB  C4C14A59C1                 vmulss xmm0, xmm6, xmm9               
  0001801E20C0  3BD8                       cmp ebx, eax                          
  0001801E20C2  C5FA2CC0                   vcvttss2si eax, xmm0                  
  0001801E20C6  751E                       jne 0x1801e20e6                          -> 0x1801E20E6 (.text)
  0001801E20C8  66C78580000000FF5B         mov word ptr [rbp + 0x80], 0x5bff     
  0001801E20D1  C685820000005B             mov byte ptr [rbp + 0x82], 0x5b       
  0001801E20D8  888583000000               mov byte ptr [rbp + 0x83], al         
  0001801E20DE  8B8580000000               mov eax, dword ptr [rbp + 0x80]       
  0001801E20E4  EB1C                       jmp 0x1801e2102                          -> 0x1801E2102 (.text)
  0001801E20E6  66C78588000000C6C8         mov word ptr [rbp + 0x88], 0xc8c6     
  0001801E20EF  C6858A000000D0             mov byte ptr [rbp + 0x8a], 0xd0       
  0001801E20F6  88858B000000               mov byte ptr [rbp + 0x8b], al         
  0001801E20FC  8B8588000000               mov eax, dword ptr [rbp + 0x88]       
  0001801E2102  89442458                   mov dword ptr [rsp + 0x58], eax       
  0001801E2106  418B0E                     mov ecx, dword ptr [r14]              
  0001801E2109  E802DC0000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E210E  4C8BC0                     mov r8, rax                           
  0001801E2111  488D15E05B1600             lea rdx, [rip + 0x165be0]                ; -> 0x180347CF8
  0001801E2118  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E211D  E8DE91FBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E2122  C4C14258FB                 vaddss xmm7, xmm7, xmm11              
  0001801E2127  FFC3                       inc ebx                               
  0001801E2129  48FFC6                     inc rsi                               
  0001801E212C  4983C604                   add r14, 4                            
  0001801E2130  3B9F24020000               cmp ebx, dword ptr [rdi + 0x224]      
  0001801E2136  7F0A                       jg 0x1801e2142                           -> 0x1801E2142 (.text)
  0001801E2138  C5FA105DC8                 vmovss xmm3, dword ptr [rbp - 0x38]   
  0001801E213D  E92EFFFFFF                 jmp 0x1801e2070                          -> 0x1801E2070 (.text)
  0001801E2142  418BCC                     mov ecx, r12d                         
  0001801E2145  E8665BFAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801E214A  90                         nop                                   
  0001801E214B  4C8D9C2450010000           lea r11, [rsp + 0x150]                
  0001801E2153  498B5B40                   mov rbx, qword ptr [r11 + 0x40]       
  0001801E2157  498B7348                   mov rsi, qword ptr [r11 + 0x48]       
  0001801E215B  C4C1782873F0               vmovaps xmm6, xmmword ptr [r11 - 0x10]
  0001801E2161  C4C178287BE0               vmovaps xmm7, xmmword ptr [r11 - 0x20]
  0001801E2167  C441782843D0               vmovaps xmm8, xmmword ptr [r11 - 0x30]
  0001801E216D  C44178284BC0               vmovaps xmm9, xmmword ptr [r11 - 0x40]
  0001801E2173  C441782853B0               vmovaps xmm10, xmmword ptr [r11 - 0x50]
  0001801E2179  C44178285BA0               vmovaps xmm11, xmmword ptr [r11 - 0x60]
  0001801E217F  498BE3                     mov rsp, r11                          
  0001801E2182  415F                       pop r15                               
  0001801E2184  415E                       pop r14                               
  0001801E2186  415C                       pop r12                               
  0001801E2188  5F                         pop rdi                               
  0001801E2189  5D                         pop rbp                               
  0001801E218A  C3                         ret                                   
