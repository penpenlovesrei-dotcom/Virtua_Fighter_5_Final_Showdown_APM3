; page_single_player.asm  --  TaskMenuArcade::draw  (la page SINGLE PLAYER)
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801DF100 - 0x1801DF446  (838 octets)
;
; A QUOI : La page fille SINGLE PLAYER. En-tete 0x177 grave en 0x1801DF256 (`B9 77 01 00 00`). Ses quatre libelles : 0x19E 0x19F 0x1A0 0x1A1 = Arcade / Score Attack / License Challenge / Special Sparring. Jumelle de FUN_18020AFC0 cote REVO, qui porte 0x1A2..0x1A5 (+4).
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
  0001801DF100  488BC4                     mov rax, rsp                          
  0001801DF103  55                         push rbp                              
  0001801DF104  56                         push rsi                              
  0001801DF105  57                         push rdi                              
  0001801DF106  4156                       push r14                              
  0001801DF108  4157                       push r15                              
  0001801DF10A  488D6888                   lea rbp, [rax - 0x78]                 
  0001801DF10E  4881EC50010000             sub rsp, 0x150                        
  0001801DF115  48C745E0FEFFFFFF           mov qword ptr [rbp - 0x20], 0xfffffffffffffffe
  0001801DF11D  48895818                   mov qword ptr [rax + 0x18], rbx       
  0001801DF121  C5F82970C8                 vmovaps xmmword ptr [rax - 0x38], xmm6
  0001801DF126  C5F82978B8                 vmovaps xmmword ptr [rax - 0x48], xmm7
  0001801DF12B  C5782940A8                 vmovaps xmmword ptr [rax - 0x58], xmm8
  0001801DF130  C578294898                 vmovaps xmmword ptr [rax - 0x68], xmm9
  0001801DF135  C578295088                 vmovaps xmmword ptr [rax - 0x78], xmm10
  0001801DF13A  C578299878FFFFFF           vmovaps xmmword ptr [rax - 0x88], xmm11
  0001801DF142  488BF1                     mov rsi, rcx                          
  0001801DF145  C74424409E010000           mov dword ptr [rsp + 0x40], 0x19e     
  0001801DF14D  C74424449F010000           mov dword ptr [rsp + 0x44], 0x19f     
  0001801DF155  C7442448A0010000           mov dword ptr [rsp + 0x48], 0x1a0     
  0001801DF15D  C744244CA1010000           mov dword ptr [rsp + 0x4c], 0x1a1     
  0001801DF165  C5F857C0                   vxorps xmm0, xmm0, xmm0               
  0001801DF169  C5FA11442430               vmovss dword ptr [rsp + 0x30], xmm0   
  0001801DF16F  C5FA11442434               vmovss dword ptr [rsp + 0x34], xmm0   
  0001801DF175  C5FA11442438               vmovss dword ptr [rsp + 0x38], xmm0   
  0001801DF17B  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801DF180  E83BB7FBFF                 call 0x18019a8c0                         -> 0x18019A8C0 (.text)
  0001801DF185  90                         nop                                   
  0001801DF186  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801DF18A  E841B8FBFF                 call 0x18019a9d0                         -> 0x18019A9D0 (.text)
  0001801DF18F  E80C89FAFF                 call 0x180187aa0                         -> 0x180187AA0 (.text)
  0001801DF194  448BF8                     mov r15d, eax                         
  0001801DF197  B902000000                 mov ecx, 2                            
  0001801DF19C  E80F8BFAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801DF1A1  488D8E40020000             lea rcx, [rsi + 0x240]                
  0001801DF1A8  33DB                       xor ebx, ebx                          
  0001801DF1AA  48895C2420                 mov qword ptr [rsp + 0x20], rbx       
  0001801DF1AF  41B101                     mov r9b, 1                            
  0001801DF1B2  4C8D05CF212300             lea r8, [rip + 0x2321cf]                 ; -> 0x180411388  "head_tit_ct"
  0001801DF1B9  488D542430                 lea rdx, [rsp + 0x30]                 
  0001801DF1BE  E8ADDBFDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801DF1C3  C5FA1035ADBD1600           vmovss xmm6, dword ptr [rip + 0x16bdad]   ; -> 0x18034AF78
  0001801DF1CB  C57A1015797B1600           vmovss xmm10, dword ptr [rip + 0x167b79]   ; -> 0x180346D4C
  0001801DF1D3  84C0                       test al, al                           
  0001801DF1D5  0F8492000000               je 0x1801df26d                           -> 0x1801DF26D (.text)
  0001801DF1DB  8D5302                     lea edx, [rbx + 2]                    
  0001801DF1DE  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801DF1E2  E809C5FBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801DF1E7  C5F828CE                   vmovaps xmm1, xmm6                    
  0001801DF1EB  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801DF1EF  E83CC6FBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801DF1F4  488D45A0                   lea rax, [rbp - 0x60]                 
  0001801DF1F8  48894598                   mov qword ptr [rbp - 0x68], rax       
  0001801DF1FC  C744247412000000           mov dword ptr [rsp + 0x74], 0x12      
  0001801DF204  C5FA104C2430               vmovss xmm1, dword ptr [rsp + 0x30]   
  0001801DF20A  C5FA114D8C                 vmovss dword ptr [rbp - 0x74], xmm1   
  0001801DF20F  C5FA10442434               vmovss xmm0, dword ptr [rsp + 0x34]   
  0001801DF215  C5FA114590                 vmovss dword ptr [rbp - 0x70], xmm0   
  0001801DF21A  C5FA114D84                 vmovss dword ptr [rbp - 0x7c], xmm1   
  0001801DF21F  C5FA114588                 vmovss dword ptr [rbp - 0x78], xmm0   
  0001801DF224  C744247C09000000           mov dword ptr [rsp + 0x7c], 9         
  0001801DF22C  C5AA594C2438               vmulss xmm1, xmm10, dword ptr [rsp + 0x38]
  0001801DF232  C5FA2CC1                   vcvttss2si eax, xmm1                  
  0001801DF236  66C78580000000FFB7         mov word ptr [rbp + 0x80], 0xb7ff     
  0001801DF23F  C6858200000039             mov byte ptr [rbp + 0x82], 0x39       
  0001801DF246  888583000000               mov byte ptr [rbp + 0x83], al         
  0001801DF24C  8B8580000000               mov eax, dword ptr [rbp + 0x80]       
  0001801DF252  89442458                   mov dword ptr [rsp + 0x58], eax       
  0001801DF256  B977010000                 mov ecx, 0x177                        
  0001801DF25B  E8B00A0100                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801DF260  488BD0                     mov rdx, rax                          
  0001801DF263  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801DF268  E893C0FBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801DF26D  488D8E98020000             lea rcx, [rsi + 0x298]                
  0001801DF274  E897E7FDFF                 call 0x1801bda10                         -> 0x1801BDA10 (.text)
  0001801DF279  84C0                       test al, al                           
  0001801DF27B  0F8481010000               je 0x1801df402                           -> 0x1801DF402 (.text)
  0001801DF281  48895C2420                 mov qword ptr [rsp + 0x20], rbx       
  0001801DF286  41B101                     mov r9b, 1                            
  0001801DF289  4C8D0598B71B00             lea r8, [rip + 0x1bb798]                 ; -> 0x18039AA28  "p_txt_01_lt"
  0001801DF290  488D542430                 lea rdx, [rsp + 0x30]                 
  0001801DF295  488D8E98020000             lea rcx, [rsi + 0x298]                
  0001801DF29C  E8CFDAFDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801DF2A1  BA01000000                 mov edx, 1                            
  0001801DF2A6  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801DF2AA  E841C4FBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801DF2AF  BA02000000                 mov edx, 2                            
  0001801DF2B4  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801DF2B8  E8B3C5FBFF                 call 0x18019b870                         -> 0x18019B870 (.text)
  0001801DF2BD  C5F828CE                   vmovaps xmm1, xmm6                    
  0001801DF2C1  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801DF2C5  E866C5FBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801DF2CA  C5FA1005E68D1600           vmovss xmm0, dword ptr [rip + 0x168de6]   ; -> 0x1803480B8
  0001801DF2D2  C5FA1145D4                 vmovss dword ptr [rbp - 0x2c], xmm0   
  0001801DF2D7  C5FA100D31C11600           vmovss xmm1, dword ptr [rip + 0x16c131]   ; -> 0x18034B410
  0001801DF2DF  C5FA114DD8                 vmovss dword ptr [rbp - 0x28], xmm1   
  0001801DF2E4  488D45A0                   lea rax, [rbp - 0x60]                 
  0001801DF2E8  48894598                   mov qword ptr [rbp - 0x68], rax       
  0001801DF2EC  C744247412000000           mov dword ptr [rsp + 0x74], 0x12      
  0001801DF2F4  C572585DC8                 vaddss xmm11, xmm1, dword ptr [rbp - 0x38]
  0001801DF2F9  C57A10442430               vmovss xmm8, dword ptr [rsp + 0x30]   
  0001801DF2FF  C5FA107C2434               vmovss xmm7, dword ptr [rsp + 0x34]   
  0001801DF305  399E24020000               cmp dword ptr [rsi + 0x224], ebx      
  0001801DF30B  0F8CF1000000               jl 0x1801df402                           -> 0x1801DF402 (.text)
  0001801DF311  488BFB                     mov rdi, rbx                          
  0001801DF314  C57A100D1C7A1600           vmovss xmm9, dword ptr [rip + 0x167a1c]   ; -> 0x180346D38
  0001801DF31C  0F1F4000                   nop dword ptr [rax]                   
  0001801DF320  C5FA10742438               vmovss xmm6, dword ptr [rsp + 0x38]   
  0001801DF326  80BC3EF102000000           cmp byte ptr [rsi + rdi + 0x2f1], 0   
  0001801DF32E  750F                       jne 0x1801df33f                          -> 0x1801DF33F (.text)
  0001801DF330  4883FF03                   cmp rdi, 3                            
  0001801DF334  750E                       jne 0x1801df344                          -> 0x1801DF344 (.text)
  0001801DF336  E875ACE4FF                 call 0x180029fb0                         -> 0x180029FB0 (.text)
  0001801DF33B  84C0                       test al, al                           
  0001801DF33D  7505                       jne 0x1801df344                          -> 0x1801DF344 (.text)
  0001801DF33F  C4C14A59F1                 vmulss xmm6, xmm6, xmm9               
  0001801DF344  8B4658                     mov eax, dword ptr [rsi + 0x58]       
  0001801DF347  3BD8                       cmp ebx, eax                          
  0001801DF349  751D                       jne 0x1801df368                          -> 0x1801DF368 (.text)
  0001801DF34B  C5FA105DC8                 vmovss xmm3, dword ptr [rbp - 0x38]   
  0001801DF350  C5F828D7                   vmovaps xmm2, xmm7                    
  0001801DF354  C4C17828C8                 vmovaps xmm1, xmm8                    
  0001801DF359  488D8E98020000             lea rcx, [rsi + 0x298]                
  0001801DF360  E80BF1FDFF                 call 0x1801be470                         -> 0x1801BE470 (.text)
  0001801DF365  8B4658                     mov eax, dword ptr [rsi + 0x58]       
  0001801DF368  C57A11458C                 vmovss dword ptr [rbp - 0x74], xmm8   
  0001801DF36D  C5FA117D90                 vmovss dword ptr [rbp - 0x70], xmm7   
  0001801DF372  C57A114584                 vmovss dword ptr [rbp - 0x7c], xmm8   
  0001801DF377  C5FA117D88                 vmovss dword ptr [rbp - 0x78], xmm7   
  0001801DF37C  C744247C09000000           mov dword ptr [rsp + 0x7c], 9         
  0001801DF384  C4C14A59C2                 vmulss xmm0, xmm6, xmm10              
  0001801DF389  3BD8                       cmp ebx, eax                          
  0001801DF38B  C5FA2CC0                   vcvttss2si eax, xmm0                  
  0001801DF38F  751E                       jne 0x1801df3af                          -> 0x1801DF3AF (.text)
  0001801DF391  66C78580000000FF5B         mov word ptr [rbp + 0x80], 0x5bff     
  0001801DF39A  C685820000005B             mov byte ptr [rbp + 0x82], 0x5b       
  0001801DF3A1  888583000000               mov byte ptr [rbp + 0x83], al         
  0001801DF3A7  8B8580000000               mov eax, dword ptr [rbp + 0x80]       
  0001801DF3AD  EB1C                       jmp 0x1801df3cb                          -> 0x1801DF3CB (.text)
  0001801DF3AF  66C78588000000C6C8         mov word ptr [rbp + 0x88], 0xc8c6     
  0001801DF3B8  C6858A000000D0             mov byte ptr [rbp + 0x8a], 0xd0       
  0001801DF3BF  88858B000000               mov byte ptr [rbp + 0x8b], al         
  0001801DF3C5  8B8588000000               mov eax, dword ptr [rbp + 0x88]       
  0001801DF3CB  89442458                   mov dword ptr [rsp + 0x58], eax       
  0001801DF3CF  8B4CBC40                   mov ecx, dword ptr [rsp + rdi*4 + 0x40]
  0001801DF3D3  E838090100                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801DF3D8  4C8BC0                     mov r8, rax                           
  0001801DF3DB  488D1516891600             lea rdx, [rip + 0x168916]                ; -> 0x180347CF8
  0001801DF3E2  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801DF3E7  E814BFFBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801DF3EC  C4C14258FB                 vaddss xmm7, xmm7, xmm11              
  0001801DF3F1  FFC3                       inc ebx                               
  0001801DF3F3  48FFC7                     inc rdi                               
  0001801DF3F6  3B9E24020000               cmp ebx, dword ptr [rsi + 0x224]      
  0001801DF3FC  0F8E1EFFFFFF               jle 0x1801df320                          -> 0x1801DF320 (.text)
  0001801DF402  418BCF                     mov ecx, r15d                         
  0001801DF405  E8A688FAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801DF40A  90                         nop                                   
  0001801DF40B  4C8D9C2450010000           lea r11, [rsp + 0x150]                
  0001801DF413  498B5B40                   mov rbx, qword ptr [r11 + 0x40]       
  0001801DF417  C4C1782873F0               vmovaps xmm6, xmmword ptr [r11 - 0x10]
  0001801DF41D  C4C178287BE0               vmovaps xmm7, xmmword ptr [r11 - 0x20]
  0001801DF423  C441782843D0               vmovaps xmm8, xmmword ptr [r11 - 0x30]
  0001801DF429  C44178284BC0               vmovaps xmm9, xmmword ptr [r11 - 0x40]
  0001801DF42F  C441782853B0               vmovaps xmm10, xmmword ptr [r11 - 0x50]
  0001801DF435  C44178285BA0               vmovaps xmm11, xmmword ptr [r11 - 0x60]
  0001801DF43B  498BE3                     mov rsp, r11                          
  0001801DF43E  415F                       pop r15                               
  0001801DF440  415E                       pop r14                               
  0001801DF442  5F                         pop rdi                               
  0001801DF443  5E                         pop rsi                               
  0001801DF444  5D                         pop rbp                               
  0001801DF445  C3                         ret                                   
