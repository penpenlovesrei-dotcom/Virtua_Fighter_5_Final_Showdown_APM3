; page_offline_versus.asm  --  TaskMenuVersus::draw  (la page OFFLINE VERSUS)
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801E2190 - 0x1801E2683  (1267 octets)
;
; A QUOI : La page fille OFFLINE VERSUS. En-tete 0x178 grave en 0x1801E2307. Libelles 0x1AD 0x1A9 0x1CB 0x1D0 0x1D5 = Round count / Time limit / Max health bar:1P / Max health bar:2P / Stage select -- NON consecutifs. Jumelle de FUN_18020DC80 cote REVO (+4).
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
  0001801E2190  488BC4                     mov rax, rsp                          
  0001801E2193  55                         push rbp                              
  0001801E2194  53                         push rbx                              
  0001801E2195  56                         push rsi                              
  0001801E2196  57                         push rdi                              
  0001801E2197  4154                       push r12                              
  0001801E2199  4155                       push r13                              
  0001801E219B  4156                       push r14                              
  0001801E219D  4157                       push r15                              
  0001801E219F  488DA838FFFFFF             lea rbp, [rax - 0xc8]                 
  0001801E21A6  4881EC88010000             sub rsp, 0x188                        
  0001801E21AD  48C74510FEFFFFFF           mov qword ptr [rbp + 0x10], 0xfffffffffffffffe
  0001801E21B5  C5F82970A8                 vmovaps xmmword ptr [rax - 0x58], xmm6
  0001801E21BA  C5F8297898                 vmovaps xmmword ptr [rax - 0x68], xmm7
  0001801E21BF  C578294088                 vmovaps xmmword ptr [rax - 0x78], xmm8
  0001801E21C4  C578298878FFFFFF           vmovaps xmmword ptr [rax - 0x88], xmm9
  0001801E21CC  C578299068FFFFFF           vmovaps xmmword ptr [rax - 0x98], xmm10
  0001801E21D4  C578299858FFFFFF           vmovaps xmmword ptr [rax - 0xa8], xmm11
  0001801E21DC  488BF9                     mov rdi, rcx                          
  0001801E21DF  C745B0AD010000             mov dword ptr [rbp - 0x50], 0x1ad     
  0001801E21E6  C745B4A9010000             mov dword ptr [rbp - 0x4c], 0x1a9     
  0001801E21ED  C745B8CB010000             mov dword ptr [rbp - 0x48], 0x1cb     
  0001801E21F4  C745BCD0010000             mov dword ptr [rbp - 0x44], 0x1d0     
  0001801E21FB  C745C0D5010000             mov dword ptr [rbp - 0x40], 0x1d5     
  0001801E2202  C5F857C0                   vxorps xmm0, xmm0, xmm0               
  0001801E2206  C5FA11442430               vmovss dword ptr [rsp + 0x30], xmm0   
  0001801E220C  C5FA11442434               vmovss dword ptr [rsp + 0x34], xmm0   
  0001801E2212  C5FA11442438               vmovss dword ptr [rsp + 0x38], xmm0   
  0001801E2218  C5FA11442448               vmovss dword ptr [rsp + 0x48], xmm0   
  0001801E221E  C5FA1144244C               vmovss dword ptr [rsp + 0x4c], xmm0   
  0001801E2224  C5FA11442450               vmovss dword ptr [rsp + 0x50], xmm0   
  0001801E222A  488D4C2460                 lea rcx, [rsp + 0x60]                 
  0001801E222F  E88C86FBFF                 call 0x18019a8c0                         -> 0x18019A8C0 (.text)
  0001801E2234  90                         nop                                   
  0001801E2235  488D4DD0                   lea rcx, [rbp - 0x30]                 
  0001801E2239  E89287FBFF                 call 0x18019a9d0                         -> 0x18019A9D0 (.text)
  0001801E223E  E85D58FAFF                 call 0x180187aa0                         -> 0x180187AA0 (.text)
  0001801E2243  89442440                   mov dword ptr [rsp + 0x40], eax       
  0001801E2247  B902000000                 mov ecx, 2                            
  0001801E224C  E85F5AFAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801E2251  488D8F58020000             lea rcx, [rdi + 0x258]                
  0001801E2258  4533E4                     xor r12d, r12d                        
  0001801E225B  4C89642420                 mov qword ptr [rsp + 0x20], r12       
  0001801E2260  41B101                     mov r9b, 1                            
  0001801E2263  4C8D051EF12200             lea r8, [rip + 0x22f11e]                 ; -> 0x180411388  "head_tit_ct"
  0001801E226A  488D542430                 lea rdx, [rsp + 0x30]                 
  0001801E226F  E8FCAAFDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E2274  C5FA1035FC8C1600           vmovss xmm6, dword ptr [rip + 0x168cfc]   ; -> 0x18034AF78
  0001801E227C  C57A1005C84A1600           vmovss xmm8, dword ptr [rip + 0x164ac8]   ; -> 0x180346D4C
  0001801E2284  84C0                       test al, al                           
  0001801E2286  0F8492000000               je 0x1801e231e                           -> 0x1801E231E (.text)
  0001801E228C  418D542402                 lea edx, [r12 + 2]                    
  0001801E2291  488D4DD0                   lea rcx, [rbp - 0x30]                 
  0001801E2295  E85694FBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801E229A  C5F828CE                   vmovaps xmm1, xmm6                    
  0001801E229E  488D4DD0                   lea rcx, [rbp - 0x30]                 
  0001801E22A2  E88995FBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801E22A7  488D45D0                   lea rax, [rbp - 0x30]                 
  0001801E22AB  488945A8                   mov qword ptr [rbp - 0x58], rax       
  0001801E22AF  C7458412000000             mov dword ptr [rbp - 0x7c], 0x12      
  0001801E22B6  C5FA104C2430               vmovss xmm1, dword ptr [rsp + 0x30]   
  0001801E22BC  C5FA114D9C                 vmovss dword ptr [rbp - 0x64], xmm1   
  0001801E22C1  C5FA10442434               vmovss xmm0, dword ptr [rsp + 0x34]   
  0001801E22C7  C5FA1145A0                 vmovss dword ptr [rbp - 0x60], xmm0   
  0001801E22CC  C5FA114D94                 vmovss dword ptr [rbp - 0x6c], xmm1   
  0001801E22D1  C5FA114598                 vmovss dword ptr [rbp - 0x68], xmm0   
  0001801E22D6  C7458C09000000             mov dword ptr [rbp - 0x74], 9         
  0001801E22DD  C5BA594C2438               vmulss xmm1, xmm8, dword ptr [rsp + 0x38]
  0001801E22E3  C5FA2CC1                   vcvttss2si eax, xmm1                  
  0001801E22E7  66C785D0000000FFB7         mov word ptr [rbp + 0xd0], 0xb7ff     
  0001801E22F0  C685D200000039             mov byte ptr [rbp + 0xd2], 0x39       
  0001801E22F7  8885D3000000               mov byte ptr [rbp + 0xd3], al         
  0001801E22FD  8B85D0000000               mov eax, dword ptr [rbp + 0xd0]       
  0001801E2303  89442468                   mov dword ptr [rsp + 0x68], eax       
  0001801E2307  B978010000                 mov ecx, 0x178                        
  0001801E230C  E8FFD90000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E2311  488BD0                     mov rdx, rax                          
  0001801E2314  488D4C2460                 lea rcx, [rsp + 0x60]                 
  0001801E2319  E8E28FFBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E231E  488D8FB0020000             lea rcx, [rdi + 0x2b0]                
  0001801E2325  E8E6B6FDFF                 call 0x1801bda10                         -> 0x1801BDA10 (.text)
  0001801E232A  84C0                       test al, al                           
  0001801E232C  0F840B030000               je 0x1801e263d                           -> 0x1801E263D (.text)
  0001801E2332  4C89642420                 mov qword ptr [rsp + 0x20], r12       
  0001801E2337  41B101                     mov r9b, 1                            
  0001801E233A  4C8D05E7861B00             lea r8, [rip + 0x1b86e7]                 ; -> 0x18039AA28  "p_txt_01_lt"
  0001801E2341  488D542430                 lea rdx, [rsp + 0x30]                 
  0001801E2346  488D8FB0020000             lea rcx, [rdi + 0x2b0]                
  0001801E234D  E81EAAFDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E2352  4C89642420                 mov qword ptr [rsp + 0x20], r12       
  0001801E2357  4533C9                     xor r9d, r9d                          
  0001801E235A  4C8D058FE92200             lea r8, [rip + 0x22e98f]                 ; -> 0x180410CF0  "p_txt_03_rt"
  0001801E2361  488D542448                 lea rdx, [rsp + 0x48]                 
  0001801E2366  488D8FB0020000             lea rcx, [rdi + 0x2b0]                
  0001801E236D  E8FEA9FDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E2372  BA01000000                 mov edx, 1                            
  0001801E2377  488D4DD0                   lea rcx, [rbp - 0x30]                 
  0001801E237B  E87093FBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801E2380  BA02000000                 mov edx, 2                            
  0001801E2385  488D4DD0                   lea rcx, [rbp - 0x30]                 
  0001801E2389  E8E294FBFF                 call 0x18019b870                         -> 0x18019B870 (.text)
  0001801E238E  C5F828CE                   vmovaps xmm1, xmm6                    
  0001801E2392  488D4DD0                   lea rcx, [rbp - 0x30]                 
  0001801E2396  E89594FBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801E239B  C5FA1005155D1600           vmovss xmm0, dword ptr [rip + 0x165d15]   ; -> 0x1803480B8
  0001801E23A3  C5FA114504                 vmovss dword ptr [rbp + 4], xmm0      
  0001801E23A8  C5FA100D60901600           vmovss xmm1, dword ptr [rip + 0x169060]   ; -> 0x18034B410
  0001801E23B0  C5FA114D08                 vmovss dword ptr [rbp + 8], xmm1      
  0001801E23B5  488D45D0                   lea rax, [rbp - 0x30]                 
  0001801E23B9  488945A8                   mov qword ptr [rbp - 0x58], rax       
  0001801E23BD  C7458412000000             mov dword ptr [rbp - 0x7c], 0x12      
  0001801E23C4  C57A10542434               vmovss xmm10, dword ptr [rsp + 0x34]  
  0001801E23CA  C5FA1055F8                 vmovss xmm2, dword ptr [rbp - 8]      
  0001801E23CF  C56A58D9                   vaddss xmm11, xmm2, xmm1              
  0001801E23D3  C5FA107C2430               vmovss xmm7, dword ptr [rsp + 0x30]   
  0001801E23D9  458BF4                     mov r14d, r12d                        
  0001801E23DC  4439A724020000             cmp dword ptr [rdi + 0x224], r12d     
  0001801E23E3  0F8C48020000               jl 0x1801e2631                           -> 0x1801E2631 (.text)
  0001801E23E9  4D8BFC                     mov r15, r12                          
  0001801E23EC  C4C17828F2                 vmovaps xmm6, xmm10                   
  0001801E23F1  C57A100D3F491600           vmovss xmm9, dword ptr [rip + 0x16493f]   ; -> 0x180346D38
  0001801E23F9  0F1F8000000000             nop dword ptr [rax]                   
  0001801E2400  443B7758                   cmp r14d, dword ptr [rdi + 0x58]      
  0001801E2404  752F                       jne 0x1801e2435                          -> 0x1801E2435 (.text)
  0001801E2406  80BF0903000000             cmp byte ptr [rdi + 0x309], 0         
  0001801E240D  7426                       je 0x1801e2435                           -> 0x1801E2435 (.text)
  0001801E240F  C5F828DA                   vmovaps xmm3, xmm2                    
  0001801E2413  C5F828D6                   vmovaps xmm2, xmm6                    
  0001801E2417  C5F828CF                   vmovaps xmm1, xmm7                    
  0001801E241B  488D8FB0020000             lea rcx, [rdi + 0x2b0]                
  0001801E2422  E849C0FDFF                 call 0x1801be470                         -> 0x1801BE470 (.text)
  0001801E2427  C5FA1055F8                 vmovss xmm2, dword ptr [rbp - 8]      
  0001801E242C  C4C16A59C1                 vmulss xmm0, xmm2, xmm9               
  0001801E2431  C57A58D6                   vaddss xmm10, xmm0, xmm6              
  0001801E2435  4983FF05                   cmp r15, 5                            
  0001801E2439  0F8D61010000               jge 0x1801e25a0                          -> 0x1801E25A0 (.text)
  0001801E243F  4180BC3F0A03000000         cmp byte ptr [r15 + rdi + 0x30a], 0   
  0001801E2448  7511                       jne 0x1801e245b                          -> 0x1801E245B (.text)
  0001801E244A  80BF0903000000             cmp byte ptr [rdi + 0x309], 0         
  0001801E2451  7408                       je 0x1801e245b                           -> 0x1801E245B (.text)
  0001801E2453  C5FA10442438               vmovss xmm0, dword ptr [rsp + 0x38]   
  0001801E2459  EB06                       jmp 0x1801e2461                          -> 0x1801E2461 (.text)
  0001801E245B  C5B259442438               vmulss xmm0, xmm9, dword ptr [rsp + 0x38]
  0001801E2461  C5FA117D9C                 vmovss dword ptr [rbp - 0x64], xmm7   
  0001801E2466  C5FA1175A0                 vmovss dword ptr [rbp - 0x60], xmm6   
  0001801E246B  C5FA117D94                 vmovss dword ptr [rbp - 0x6c], xmm7   
  0001801E2470  C5FA117598                 vmovss dword ptr [rbp - 0x68], xmm6   
  0001801E2475  C7458C09000000             mov dword ptr [rbp - 0x74], 9         
  0001801E247C  443B7758                   cmp r14d, dword ptr [rdi + 0x58]      
  0001801E2480  7531                       jne 0x1801e24b3                          -> 0x1801E24B3 (.text)
  0001801E2482  80BF0903000000             cmp byte ptr [rdi + 0x309], 0         
  0001801E2489  7428                       je 0x1801e24b3                           -> 0x1801E24B3 (.text)
  0001801E248B  66C785D0000000FF5B         mov word ptr [rbp + 0xd0], 0x5bff     
  0001801E2494  C685D20000005B             mov byte ptr [rbp + 0xd2], 0x5b       
  0001801E249B  C4C17A59C0                 vmulss xmm0, xmm0, xmm8               
  0001801E24A0  C5FA2CF0                   vcvttss2si esi, xmm0                  
  0001801E24A4  4088B5D3000000             mov byte ptr [rbp + 0xd3], sil        
  0001801E24AB  8B85D0000000               mov eax, dword ptr [rbp + 0xd0]       
  0001801E24B1  EB26                       jmp 0x1801e24d9                          -> 0x1801E24D9 (.text)
  0001801E24B3  66C785D8000000C6C8         mov word ptr [rbp + 0xd8], 0xc8c6     
  0001801E24BC  C685DA000000D0             mov byte ptr [rbp + 0xda], 0xd0       
  0001801E24C3  C4C17A59C0                 vmulss xmm0, xmm0, xmm8               
  0001801E24C8  C5FA2CF0                   vcvttss2si esi, xmm0                  
  0001801E24CC  4088B5DB000000             mov byte ptr [rbp + 0xdb], sil        
  0001801E24D3  8B85D8000000               mov eax, dword ptr [rbp + 0xd8]       
  0001801E24D9  89442468                   mov dword ptr [rsp + 0x68], eax       
  0001801E24DD  428B5CBDB0                 mov ebx, dword ptr [rbp + r15*4 - 0x50]
  0001801E24E2  8BCB                       mov ecx, ebx                          
  0001801E24E4  E827D80000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E24E9  4C8BC0                     mov r8, rax                           
  0001801E24EC  488D1505581600             lea rdx, [rip + 0x165805]                ; -> 0x180347CF8
  0001801E24F3  488D4C2460                 lea rcx, [rsp + 0x60]                 
  0001801E24F8  E8038EFBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E24FD  428B8CBF40020000           mov ecx, dword ptr [rdi + r15*4 + 0x240]
  0001801E2505  FFC1                       inc ecx                               
  0001801E2507  03CB                       add ecx, ebx                          
  0001801E2509  E802D80000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E250E  4C8BC8                     mov r9, rax                           
  0001801E2511  443B7758                   cmp r14d, dword ptr [rdi + 0x58]      
  0001801E2515  4C0F44E0                   cmove r12, rax                        
  0001801E2519  C5FA10442448               vmovss xmm0, dword ptr [rsp + 0x48]   
  0001801E251F  C5FA11459C                 vmovss dword ptr [rbp - 0x64], xmm0   
  0001801E2524  C5FA1175A0                 vmovss dword ptr [rbp - 0x60], xmm6   
  0001801E2529  C5FA114594                 vmovss dword ptr [rbp - 0x6c], xmm0   
  0001801E252E  C5FA117598                 vmovss dword ptr [rbp - 0x68], xmm6   
  0001801E2533  C7458C09000000             mov dword ptr [rbp - 0x74], 9         
  0001801E253A  7528                       jne 0x1801e2564                          -> 0x1801E2564 (.text)
  0001801E253C  80BF0903000000             cmp byte ptr [rdi + 0x309], 0         
  0001801E2543  741F                       je 0x1801e2564                           -> 0x1801E2564 (.text)
  0001801E2545  66C785E0000000FF5B         mov word ptr [rbp + 0xe0], 0x5bff     
  0001801E254E  C685E20000005B             mov byte ptr [rbp + 0xe2], 0x5b       
  0001801E2555  4088B5E3000000             mov byte ptr [rbp + 0xe3], sil        
  0001801E255C  8B85E0000000               mov eax, dword ptr [rbp + 0xe0]       
  0001801E2562  EB1D                       jmp 0x1801e2581                          -> 0x1801E2581 (.text)
  0001801E2564  66C785E8000000C6C8         mov word ptr [rbp + 0xe8], 0xc8c6     
  0001801E256D  C685EA000000D0             mov byte ptr [rbp + 0xea], 0xd0       
  0001801E2574  4088B5EB000000             mov byte ptr [rbp + 0xeb], sil        
  0001801E257B  8B85E8000000               mov eax, dword ptr [rbp + 0xe8]       
  0001801E2581  89442468                   mov dword ptr [rsp + 0x68], eax       
  0001801E2585  4C8D056C571600             lea r8, [rip + 0x16576c]                 ; -> 0x180347CF8
  0001801E258C  BA02000000                 mov edx, 2                            
  0001801E2591  488D4C2460                 lea rcx, [rsp + 0x60]                 
  0001801E2596  E8458DFBFF                 call 0x18019b2e0                         -> 0x18019B2E0 (.text)
  0001801E259B  C5FA1055F8                 vmovss xmm2, dword ptr [rbp - 8]      
  0001801E25A0  C4C14A58F3                 vaddss xmm6, xmm6, xmm11              
  0001801E25A5  41FFC6                     inc r14d                              
  0001801E25A8  49FFC7                     inc r15                               
  0001801E25AB  443BB724020000             cmp r14d, dword ptr [rdi + 0x224]     
  0001801E25B2  0F8E48FEFFFF               jle 0x1801e2400                          -> 0x1801E2400 (.text)
  0001801E25B8  4D85E4                     test r12, r12                         
  0001801E25BB  7474                       je 0x1801e2631                           -> 0x1801E2631 (.text)
  0001801E25BD  80BF0903000000             cmp byte ptr [rdi + 0x309], 0         
  0001801E25C4  746B                       je 0x1801e2631                           -> 0x1801E2631 (.text)
  0001801E25C6  49C7C1FFFFFFFF             mov r9, 0xffffffffffffffff            
  0001801E25CD  0F1F00                     nop dword ptr [rax]                   
  0001801E25D0  49FFC1                     inc r9                                
  0001801E25D3  43803C0C00                 cmp byte ptr [r12 + r9], 0            
  0001801E25D8  75F6                       jne 0x1801e25d0                          -> 0x1801E25D0 (.text)
  0001801E25DA  C5FA1005F6561600           vmovss xmm0, dword ptr [rip + 0x1656f6]   ; -> 0x180347CD8
  0001801E25E2  C5FA11442420               vmovss dword ptr [rsp + 0x20], xmm0   
  0001801E25E8  4D8BC4                     mov r8, r12                           
  0001801E25EB  488D95D0000000             lea rdx, [rbp + 0xd0]                 
  0001801E25F2  488D4C2460                 lea rcx, [rsp + 0x60]                 
  0001801E25F7  E8B492FBFF                 call 0x18019b8b0                         -> 0x18019B8B0 (.text)
  0001801E25FC  488D8F10030000             lea rcx, [rdi + 0x310]                
  0001801E2603  C5FA1085D0000000           vmovss xmm0, dword ptr [rbp + 0xd0]   
  0001801E260B  C5FA11442428               vmovss dword ptr [rsp + 0x28], xmm0   
  0001801E2611  C744242012000000           mov dword ptr [rsp + 0x20], 0x12      
  0001801E2619  41B904000000               mov r9d, 4                            
  0001801E261F  C4C17828D2                 vmovaps xmm2, xmm10                   
  0001801E2624  C5FA104C2448               vmovss xmm1, dword ptr [rsp + 0x48]   
  0001801E262A  E841BAFDFF                 call 0x1801be070                         -> 0x1801BE070 (.text)
  0001801E262F  EB0C                       jmp 0x1801e263d                          -> 0x1801E263D (.text)
  0001801E2631  488D8F10030000             lea rcx, [rdi + 0x310]                
  0001801E2638  E873BEFDFF                 call 0x1801be4b0                         -> 0x1801BE4B0 (.text)
  0001801E263D  8B4C2440                   mov ecx, dword ptr [rsp + 0x40]       
  0001801E2641  E86A56FAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801E2646  90                         nop                                   
  0001801E2647  4C8D9C2488010000           lea r11, [rsp + 0x188]                
  0001801E264F  C4C1782873E8               vmovaps xmm6, xmmword ptr [r11 - 0x18]
  0001801E2655  C4C178287BD8               vmovaps xmm7, xmmword ptr [r11 - 0x28]
  0001801E265B  C441782843C8               vmovaps xmm8, xmmword ptr [r11 - 0x38]
  0001801E2661  C44178284BB8               vmovaps xmm9, xmmword ptr [r11 - 0x48]
  0001801E2667  C441782853A8               vmovaps xmm10, xmmword ptr [r11 - 0x58]
  0001801E266D  C44178285B98               vmovaps xmm11, xmmword ptr [r11 - 0x68]
  0001801E2673  498BE3                     mov rsp, r11                          
  0001801E2676  415F                       pop r15                               
  0001801E2678  415E                       pop r14                               
  0001801E267A  415D                       pop r13                               
  0001801E267C  415C                       pop r12                               
  0001801E267E  5F                         pop rdi                               
  0001801E267F  5E                         pop rsi                               
  0001801E2680  5B                         pop rbx                               
  0001801E2681  5D                         pop rbp                               
  0001801E2682  C3                         ret                                   
