; page_terminal.asm  --  TaskMenuTerminal::draw  (la page TERMINAL)
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801E1B10 - 0x1801E1E3C  (812 octets)
;
; A QUOI : La page fille TERMINAL. En-tete 0x17C grave en 0x1801E1C51. Libelles 0x299 0x29A = Customize / Replays. Jumelle de FUN_18020D640 cote REVO, qui porte 0x2A1 0x2A2 (+8 : le palier le plus eleve des trois mesures).
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
  0001801E1B10  488BC4                     mov rax, rsp                          
  0001801E1B13  55                         push rbp                              
  0001801E1B14  56                         push rsi                              
  0001801E1B15  57                         push rdi                              
  0001801E1B16  4156                       push r14                              
  0001801E1B18  4157                       push r15                              
  0001801E1B1A  488D6898                   lea rbp, [rax - 0x68]                 
  0001801E1B1E  4881EC40010000             sub rsp, 0x140                        
  0001801E1B25  48C745D0FEFFFFFF           mov qword ptr [rbp - 0x30], 0xfffffffffffffffe
  0001801E1B2D  48895820                   mov qword ptr [rax + 0x20], rbx       
  0001801E1B31  C5F82970C8                 vmovaps xmmword ptr [rax - 0x38], xmm6
  0001801E1B36  C5F82978B8                 vmovaps xmmword ptr [rax - 0x48], xmm7
  0001801E1B3B  C5782940A8                 vmovaps xmmword ptr [rax - 0x58], xmm8
  0001801E1B40  C578294898                 vmovaps xmmword ptr [rax - 0x68], xmm9
  0001801E1B45  C578295088                 vmovaps xmmword ptr [rax - 0x78], xmm10
  0001801E1B4A  C578299878FFFFFF           vmovaps xmmword ptr [rax - 0x88], xmm11
  0001801E1B52  488BF1                     mov rsi, rcx                          
  0001801E1B55  C7858000000099020000       mov dword ptr [rbp + 0x80], 0x299     
  0001801E1B5F  C785840000009A020000       mov dword ptr [rbp + 0x84], 0x29a     
  0001801E1B69  C5F857C0                   vxorps xmm0, xmm0, xmm0               
  0001801E1B6D  C5FA11442430               vmovss dword ptr [rsp + 0x30], xmm0   
  0001801E1B73  C5FA11442434               vmovss dword ptr [rsp + 0x34], xmm0   
  0001801E1B79  C5FA11442438               vmovss dword ptr [rsp + 0x38], xmm0   
  0001801E1B7F  488D4C2440                 lea rcx, [rsp + 0x40]                 
  0001801E1B84  E8378DFBFF                 call 0x18019a8c0                         -> 0x18019A8C0 (.text)
  0001801E1B89  90                         nop                                   
  0001801E1B8A  488D4D90                   lea rcx, [rbp - 0x70]                 
  0001801E1B8E  E83D8EFBFF                 call 0x18019a9d0                         -> 0x18019A9D0 (.text)
  0001801E1B93  E8085FFAFF                 call 0x180187aa0                         -> 0x180187AA0 (.text)
  0001801E1B98  448BF8                     mov r15d, eax                         
  0001801E1B9B  B902000000                 mov ecx, 2                            
  0001801E1BA0  E80B61FAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801E1BA5  488D8E40020000             lea rcx, [rsi + 0x240]                
  0001801E1BAC  33DB                       xor ebx, ebx                          
  0001801E1BAE  48895C2420                 mov qword ptr [rsp + 0x20], rbx       
  0001801E1BB3  41B101                     mov r9b, 1                            
  0001801E1BB6  4C8D05CBF72200             lea r8, [rip + 0x22f7cb]                 ; -> 0x180411388  "head_tit_ct"
  0001801E1BBD  488D542430                 lea rdx, [rsp + 0x30]                 
  0001801E1BC2  E8A9B1FDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E1BC7  C5FA1035A9931600           vmovss xmm6, dword ptr [rip + 0x1693a9]   ; -> 0x18034AF78
  0001801E1BCF  C57A101575511600           vmovss xmm10, dword ptr [rip + 0x165175]   ; -> 0x180346D4C
  0001801E1BD7  84C0                       test al, al                           
  0001801E1BD9  0F8489000000               je 0x1801e1c68                           -> 0x1801E1C68 (.text)
  0001801E1BDF  8D5302                     lea edx, [rbx + 2]                    
  0001801E1BE2  488D4D90                   lea rcx, [rbp - 0x70]                 
  0001801E1BE6  E8059BFBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801E1BEB  C5F828CE                   vmovaps xmm1, xmm6                    
  0001801E1BEF  488D4D90                   lea rcx, [rbp - 0x70]                 
  0001801E1BF3  E8389CFBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801E1BF8  488D4590                   lea rax, [rbp - 0x70]                 
  0001801E1BFC  48894588                   mov qword ptr [rbp - 0x78], rax       
  0001801E1C00  C744246412000000           mov dword ptr [rsp + 0x64], 0x12      
  0001801E1C08  C5FA104C2430               vmovss xmm1, dword ptr [rsp + 0x30]   
  0001801E1C0E  C5FA114C247C               vmovss dword ptr [rsp + 0x7c], xmm1   
  0001801E1C14  C5FA10442434               vmovss xmm0, dword ptr [rsp + 0x34]   
  0001801E1C1A  C5FA114580                 vmovss dword ptr [rbp - 0x80], xmm0   
  0001801E1C1F  C5FA114C2474               vmovss dword ptr [rsp + 0x74], xmm1   
  0001801E1C25  C5FA11442478               vmovss dword ptr [rsp + 0x78], xmm0   
  0001801E1C2B  C744246C09000000           mov dword ptr [rsp + 0x6c], 9         
  0001801E1C33  C5AA594C2438               vmulss xmm1, xmm10, dword ptr [rsp + 0x38]
  0001801E1C39  C5FA2CC1                   vcvttss2si eax, xmm1                  
  0001801E1C3D  66C74570FFB7               mov word ptr [rbp + 0x70], 0xb7ff     
  0001801E1C43  C6457239                   mov byte ptr [rbp + 0x72], 0x39       
  0001801E1C47  884573                     mov byte ptr [rbp + 0x73], al         
  0001801E1C4A  8B4570                     mov eax, dword ptr [rbp + 0x70]       
  0001801E1C4D  89442448                   mov dword ptr [rsp + 0x48], eax       
  0001801E1C51  B97C010000                 mov ecx, 0x17c                        
  0001801E1C56  E8B5E00000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E1C5B  488BD0                     mov rdx, rax                          
  0001801E1C5E  488D4C2440                 lea rcx, [rsp + 0x40]                 
  0001801E1C63  E89896FBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E1C68  488D8E98020000             lea rcx, [rsi + 0x298]                
  0001801E1C6F  E89CBDFDFF                 call 0x1801bda10                         -> 0x1801BDA10 (.text)
  0001801E1C74  84C0                       test al, al                           
  0001801E1C76  0F847C010000               je 0x1801e1df8                           -> 0x1801E1DF8 (.text)
  0001801E1C7C  48895C2420                 mov qword ptr [rsp + 0x20], rbx       
  0001801E1C81  41B101                     mov r9b, 1                            
  0001801E1C84  4C8D059D8D1B00             lea r8, [rip + 0x1b8d9d]                 ; -> 0x18039AA28  "p_txt_01_lt"
  0001801E1C8B  488D542430                 lea rdx, [rsp + 0x30]                 
  0001801E1C90  488D8E98020000             lea rcx, [rsi + 0x298]                
  0001801E1C97  E8D4B0FDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E1C9C  BA01000000                 mov edx, 1                            
  0001801E1CA1  488D4D90                   lea rcx, [rbp - 0x70]                 
  0001801E1CA5  E8469AFBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801E1CAA  BA02000000                 mov edx, 2                            
  0001801E1CAF  488D4D90                   lea rcx, [rbp - 0x70]                 
  0001801E1CB3  E8B89BFBFF                 call 0x18019b870                         -> 0x18019B870 (.text)
  0001801E1CB8  C5F828CE                   vmovaps xmm1, xmm6                    
  0001801E1CBC  488D4D90                   lea rcx, [rbp - 0x70]                 
  0001801E1CC0  E86B9BFBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801E1CC5  C5FA1005EB631600           vmovss xmm0, dword ptr [rip + 0x1663eb]   ; -> 0x1803480B8
  0001801E1CCD  C5FA1145C4                 vmovss dword ptr [rbp - 0x3c], xmm0   
  0001801E1CD2  C5FA100D36971600           vmovss xmm1, dword ptr [rip + 0x169736]   ; -> 0x18034B410
  0001801E1CDA  C5FA114DC8                 vmovss dword ptr [rbp - 0x38], xmm1   
  0001801E1CDF  488D4590                   lea rax, [rbp - 0x70]                 
  0001801E1CE3  48894588                   mov qword ptr [rbp - 0x78], rax       
  0001801E1CE7  C744246412000000           mov dword ptr [rsp + 0x64], 0x12      
  0001801E1CEF  C572585DB8                 vaddss xmm11, xmm1, dword ptr [rbp - 0x48]
  0001801E1CF4  C57A10442430               vmovss xmm8, dword ptr [rsp + 0x30]   
  0001801E1CFA  C5FA107C2434               vmovss xmm7, dword ptr [rsp + 0x34]   
  0001801E1D00  399E24020000               cmp dword ptr [rsi + 0x224], ebx      
  0001801E1D06  0F8CEC000000               jl 0x1801e1df8                           -> 0x1801E1DF8 (.text)
  0001801E1D0C  488BFB                     mov rdi, rbx                          
  0001801E1D0F  C57A100D21501600           vmovss xmm9, dword ptr [rip + 0x165021]   ; -> 0x180346D38
  0001801E1D17  660F1F840000000000         nop word ptr [rax + rax]              
  0001801E1D20  C5FA10742438               vmovss xmm6, dword ptr [rsp + 0x38]   
  0001801E1D26  80BC3EF102000000           cmp byte ptr [rsi + rdi + 0x2f1], 0   
  0001801E1D2E  7517                       jne 0x1801e1d47                          -> 0x1801E1D47 (.text)
  0001801E1D30  4885FF                     test rdi, rdi                         
  0001801E1D33  7517                       jne 0x1801e1d4c                          -> 0x1801E1D4C (.text)
  0001801E1D35  E87682E4FF                 call 0x180029fb0                         -> 0x180029FB0 (.text)
  0001801E1D3A  84C0                       test al, al                           
  0001801E1D3C  7409                       je 0x1801e1d47                           -> 0x1801E1D47 (.text)
  0001801E1D3E  E8CD52FDFF                 call 0x1801b7010                         -> 0x1801B7010 (.text)
  0001801E1D43  84C0                       test al, al                           
  0001801E1D45  7505                       jne 0x1801e1d4c                          -> 0x1801E1D4C (.text)
  0001801E1D47  C4C14A59F1                 vmulss xmm6, xmm6, xmm9               
  0001801E1D4C  8B4658                     mov eax, dword ptr [rsi + 0x58]       
  0001801E1D4F  3BD8                       cmp ebx, eax                          
  0001801E1D51  751D                       jne 0x1801e1d70                          -> 0x1801E1D70 (.text)
  0001801E1D53  C5FA105DB8                 vmovss xmm3, dword ptr [rbp - 0x48]   
  0001801E1D58  C5F828D7                   vmovaps xmm2, xmm7                    
  0001801E1D5C  C4C17828C8                 vmovaps xmm1, xmm8                    
  0001801E1D61  488D8E98020000             lea rcx, [rsi + 0x298]                
  0001801E1D68  E803C7FDFF                 call 0x1801be470                         -> 0x1801BE470 (.text)
  0001801E1D6D  8B4658                     mov eax, dword ptr [rsi + 0x58]       
  0001801E1D70  C57A1144247C               vmovss dword ptr [rsp + 0x7c], xmm8   
  0001801E1D76  C5FA117D80                 vmovss dword ptr [rbp - 0x80], xmm7   
  0001801E1D7B  C57A11442474               vmovss dword ptr [rsp + 0x74], xmm8   
  0001801E1D81  C5FA117C2478               vmovss dword ptr [rsp + 0x78], xmm7   
  0001801E1D87  C744246C09000000           mov dword ptr [rsp + 0x6c], 9         
  0001801E1D8F  C4C14A59C2                 vmulss xmm0, xmm6, xmm10              
  0001801E1D94  3BD8                       cmp ebx, eax                          
  0001801E1D96  C5FA2CC0                   vcvttss2si eax, xmm0                  
  0001801E1D9A  7512                       jne 0x1801e1dae                          -> 0x1801E1DAE (.text)
  0001801E1D9C  66C74570FF5B               mov word ptr [rbp + 0x70], 0x5bff     
  0001801E1DA2  C645725B                   mov byte ptr [rbp + 0x72], 0x5b       
  0001801E1DA6  884573                     mov byte ptr [rbp + 0x73], al         
  0001801E1DA9  8B4570                     mov eax, dword ptr [rbp + 0x70]       
  0001801E1DAC  EB10                       jmp 0x1801e1dbe                          -> 0x1801E1DBE (.text)
  0001801E1DAE  66C74578C6C8               mov word ptr [rbp + 0x78], 0xc8c6     
  0001801E1DB4  C6457AD0                   mov byte ptr [rbp + 0x7a], 0xd0       
  0001801E1DB8  88457B                     mov byte ptr [rbp + 0x7b], al         
  0001801E1DBB  8B4578                     mov eax, dword ptr [rbp + 0x78]       
  0001801E1DBE  89442448                   mov dword ptr [rsp + 0x48], eax       
  0001801E1DC2  8B8CBD80000000             mov ecx, dword ptr [rbp + rdi*4 + 0x80]
  0001801E1DC9  E842DF0000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E1DCE  4C8BC0                     mov r8, rax                           
  0001801E1DD1  488D15205F1600             lea rdx, [rip + 0x165f20]                ; -> 0x180347CF8
  0001801E1DD8  488D4C2440                 lea rcx, [rsp + 0x40]                 
  0001801E1DDD  E81E95FBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E1DE2  C4C14258FB                 vaddss xmm7, xmm7, xmm11              
  0001801E1DE7  FFC3                       inc ebx                               
  0001801E1DE9  48FFC7                     inc rdi                               
  0001801E1DEC  3B9E24020000               cmp ebx, dword ptr [rsi + 0x224]      
  0001801E1DF2  0F8E28FFFFFF               jle 0x1801e1d20                          -> 0x1801E1D20 (.text)
  0001801E1DF8  418BCF                     mov ecx, r15d                         
  0001801E1DFB  E8B05EFAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801E1E00  90                         nop                                   
  0001801E1E01  4C8D9C2440010000           lea r11, [rsp + 0x140]                
  0001801E1E09  498B5B48                   mov rbx, qword ptr [r11 + 0x48]       
  0001801E1E0D  C4C1782873F0               vmovaps xmm6, xmmword ptr [r11 - 0x10]
  0001801E1E13  C4C178287BE0               vmovaps xmm7, xmmword ptr [r11 - 0x20]
  0001801E1E19  C441782843D0               vmovaps xmm8, xmmword ptr [r11 - 0x30]
  0001801E1E1F  C44178284BC0               vmovaps xmm9, xmmword ptr [r11 - 0x40]
  0001801E1E25  C441782853B0               vmovaps xmm10, xmmword ptr [r11 - 0x50]
  0001801E1E2B  C44178285BA0               vmovaps xmm11, xmmword ptr [r11 - 0x60]
  0001801E1E31  498BE3                     mov rsp, r11                          
  0001801E1E34  415F                       pop r15                               
  0001801E1E36  415E                       pop r14                               
  0001801E1E38  5F                         pop rdi                               
  0001801E1E39  5E                         pop rsi                               
  0001801E1E3A  5D                         pop rbp                               
  0001801E1E3B  C3                         ret                                   
