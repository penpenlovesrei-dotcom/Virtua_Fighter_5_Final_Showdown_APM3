; page_scoreattack.asm  --  TaskMenuScoreAttack::draw  (le panneau de resultats)
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801E17A0 - 0x1801E1B10  (880 octets)
;
; A QUOI : Creneau [4] de la vtable TaskMenuScoreAttack 0x1805326C8. Jumelle de FUN_18020D2F0 cote REVO, dont les lignes 0x1C1 0x1C2 0x1C3 se lisent CLASS / HIGH SCORE / CLEAR TELLES QUELLES -- palier +0. C'est cette page qui prouve qu'un decalage -3 global serait FAUX.
;
; D'OU VIENT LE NOM : RTTI : vtable 0x1805326C8 creneau [4] ; MENU.md section 419.92
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
  0001801E17A0  488BC4                     mov rax, rsp                          
  0001801E17A3  55                         push rbp                              
  0001801E17A4  57                         push rdi                              
  0001801E17A5  4154                       push r12                              
  0001801E17A7  4156                       push r14                              
  0001801E17A9  4157                       push r15                              
  0001801E17AB  488D6888                   lea rbp, [rax - 0x78]                 
  0001801E17AF  4881EC50010000             sub rsp, 0x150                        
  0001801E17B6  48C745E0FEFFFFFF           mov qword ptr [rbp - 0x20], 0xfffffffffffffffe
  0001801E17BE  48895818                   mov qword ptr [rax + 0x18], rbx       
  0001801E17C2  48897020                   mov qword ptr [rax + 0x20], rsi       
  0001801E17C6  C5F82970C8                 vmovaps xmmword ptr [rax - 0x38], xmm6
  0001801E17CB  C5F82978B8                 vmovaps xmmword ptr [rax - 0x48], xmm7
  0001801E17D0  C5782940A8                 vmovaps xmmword ptr [rax - 0x58], xmm8
  0001801E17D5  C578294898                 vmovaps xmmword ptr [rax - 0x68], xmm9
  0001801E17DA  C578295088                 vmovaps xmmword ptr [rax - 0x78], xmm10
  0001801E17DF  C578299878FFFFFF           vmovaps xmmword ptr [rax - 0x88], xmm11
  0001801E17E7  488BF9                     mov rdi, rcx                          
  0001801E17EA  C7442440BD010000           mov dword ptr [rsp + 0x40], 0x1bd     
  0001801E17F2  C7442444BE010000           mov dword ptr [rsp + 0x44], 0x1be     
  0001801E17FA  C7442448BF010000           mov dword ptr [rsp + 0x48], 0x1bf     
  0001801E1802  C5F857C0                   vxorps xmm0, xmm0, xmm0               
  0001801E1806  C5FA11442430               vmovss dword ptr [rsp + 0x30], xmm0   
  0001801E180C  C5FA11442434               vmovss dword ptr [rsp + 0x34], xmm0   
  0001801E1812  C5FA11442438               vmovss dword ptr [rsp + 0x38], xmm0   
  0001801E1818  488D4D90                   lea rcx, [rbp - 0x70]                 
  0001801E181C  E89F90FBFF                 call 0x18019a8c0                         -> 0x18019A8C0 (.text)
  0001801E1821  90                         nop                                   
  0001801E1822  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E1827  E8A491FBFF                 call 0x18019a9d0                         -> 0x18019A9D0 (.text)
  0001801E182C  E86F62FAFF                 call 0x180187aa0                         -> 0x180187AA0 (.text)
  0001801E1831  448BE0                     mov r12d, eax                         
  0001801E1834  B902000000                 mov ecx, 2                            
  0001801E1839  E87264FAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801E183E  488D8F40020000             lea rcx, [rdi + 0x240]                
  0001801E1845  E8C6C1FDFF                 call 0x1801bda10                         -> 0x1801BDA10 (.text)
  0001801E184A  84C0                       test al, al                           
  0001801E184C  0F8468020000               je 0x1801e1aba                           -> 0x1801E1ABA (.text)
  0001801E1852  33DB                       xor ebx, ebx                          
  0001801E1854  48895C2420                 mov qword ptr [rsp + 0x20], rbx       
  0001801E1859  41B101                     mov r9b, 1                            
  0001801E185C  4C8D057DF42200             lea r8, [rip + 0x22f47d]                 ; -> 0x180410CE0  "p_small_head_lt"
  0001801E1863  488D542430                 lea rdx, [rsp + 0x30]                 
  0001801E1868  488D8F40020000             lea rcx, [rdi + 0x240]                
  0001801E186F  E8FCB4FDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E1874  8D5301                     lea edx, [rbx + 1]                    
  0001801E1877  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E187C  E86F9EFBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801E1881  8D5302                     lea edx, [rbx + 2]                    
  0001801E1884  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E1889  E8E29FFBFF                 call 0x18019b870                         -> 0x18019B870 (.text)
  0001801E188E  C5FA100DE2961600           vmovss xmm1, dword ptr [rip + 0x1696e2]   ; -> 0x18034AF78
  0001801E1896  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E189B  E8909FFBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801E18A0  C5FA103510681600           vmovss xmm6, dword ptr [rip + 0x166810]   ; -> 0x1803480B8
  0001801E18A8  C5FA117584                 vmovss dword ptr [rbp - 0x7c], xmm6   
  0001801E18AD  C57A10055B9B1600           vmovss xmm8, dword ptr [rip + 0x169b5b]   ; -> 0x18034B410
  0001801E18B5  C57A114588                 vmovss dword ptr [rbp - 0x78], xmm8   
  0001801E18BA  488D442450                 lea rax, [rsp + 0x50]                 
  0001801E18BF  488945D8                   mov qword ptr [rbp - 0x28], rax       
  0001801E18C3  C745B412000000             mov dword ptr [rbp - 0x4c], 0x12      
  0001801E18CA  C5FA104C2430               vmovss xmm1, dword ptr [rsp + 0x30]   
  0001801E18D0  C5FA114DCC                 vmovss dword ptr [rbp - 0x34], xmm1   
  0001801E18D5  C5FA10442434               vmovss xmm0, dword ptr [rsp + 0x34]   
  0001801E18DB  C5FA1145D0                 vmovss dword ptr [rbp - 0x30], xmm0   
  0001801E18E0  C5FA114DC4                 vmovss dword ptr [rbp - 0x3c], xmm1   
  0001801E18E5  C5FA1145C8                 vmovss dword ptr [rbp - 0x38], xmm0   
  0001801E18EA  C745BC09000000             mov dword ptr [rbp - 0x44], 9         
  0001801E18F1  C57A100D53541600           vmovss xmm9, dword ptr [rip + 0x165453]   ; -> 0x180346D4C
  0001801E18F9  C5B2594C2438               vmulss xmm1, xmm9, dword ptr [rsp + 0x38]
  0001801E18FF  C5FA2CC1                   vcvttss2si eax, xmm1                  
  0001801E1903  66C78580000000FFB7         mov word ptr [rbp + 0x80], 0xb7ff     
  0001801E190C  C6858200000039             mov byte ptr [rbp + 0x82], 0x39       
  0001801E1913  888583000000               mov byte ptr [rbp + 0x83], al         
  0001801E1919  8B8580000000               mov eax, dword ptr [rbp + 0x80]       
  0001801E191F  894598                     mov dword ptr [rbp - 0x68], eax       
  0001801E1922  B99F010000                 mov ecx, 0x19f                        
  0001801E1927  E8E4E30000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E192C  488BD0                     mov rdx, rax                          
  0001801E192F  488D4D90                   lea rcx, [rbp - 0x70]                 
  0001801E1933  E8C899FBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E1938  48895C2420                 mov qword ptr [rsp + 0x20], rbx       
  0001801E193D  4533C9                     xor r9d, r9d                          
  0001801E1940  4C8D05E1901B00             lea r8, [rip + 0x1b90e1]                 ; -> 0x18039AA28  "p_txt_01_lt"
  0001801E1947  488D542430                 lea rdx, [rsp + 0x30]                 
  0001801E194C  488D8F40020000             lea rcx, [rdi + 0x240]                
  0001801E1953  E818B4FDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E1958  8D5301                     lea edx, [rbx + 1]                    
  0001801E195B  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E1960  E88B9DFBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801E1965  8D5302                     lea edx, [rbx + 2]                    
  0001801E1968  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E196D  E8FE9EFBFF                 call 0x18019b870                         -> 0x18019B870 (.text)
  0001801E1972  C5FA100DFE951600           vmovss xmm1, dword ptr [rip + 0x1695fe]   ; -> 0x18034AF78
  0001801E197A  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E197F  E8AC9EFBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801E1984  C5FA117584                 vmovss dword ptr [rbp - 0x7c], xmm6   
  0001801E1989  C57A114588                 vmovss dword ptr [rbp - 0x78], xmm8   
  0001801E198E  488D442450                 lea rax, [rsp + 0x50]                 
  0001801E1993  488945D8                   mov qword ptr [rbp - 0x28], rax       
  0001801E1997  C745B412000000             mov dword ptr [rbp - 0x4c], 0x12      
  0001801E199E  C5FA105C2478               vmovss xmm3, dword ptr [rsp + 0x78]   
  0001801E19A4  C4416258D8                 vaddss xmm11, xmm3, xmm8              
  0001801E19A9  C57A10442430               vmovss xmm8, dword ptr [rsp + 0x30]   
  0001801E19AF  C5FA107C2434               vmovss xmm7, dword ptr [rsp + 0x34]   
  0001801E19B5  399F24020000               cmp dword ptr [rdi + 0x224], ebx      
  0001801E19BB  0F8CE4000000               jl 0x1801e1aa5                           -> 0x1801E1AA5 (.text)
  0001801E19C1  488DB799020000             lea rsi, [rdi + 0x299]                
  0001801E19C8  4C8D742440                 lea r14, [rsp + 0x40]                 
  0001801E19CD  C57A101563531600           vmovss xmm10, dword ptr [rip + 0x165363]   ; -> 0x180346D38
  0001801E19D5  C5FA10742438               vmovss xmm6, dword ptr [rsp + 0x38]   
  0001801E19DB  803E00                     cmp byte ptr [rsi], 0                 
  0001801E19DE  7405                       je 0x1801e19e5                           -> 0x1801E19E5 (.text)
  0001801E19E0  C4C14A59F2                 vmulss xmm6, xmm6, xmm10              
  0001801E19E5  8B4758                     mov eax, dword ptr [rdi + 0x58]       
  0001801E19E8  3BD8                       cmp ebx, eax                          
  0001801E19EA  7518                       jne 0x1801e1a04                          -> 0x1801E1A04 (.text)
  0001801E19EC  C5F828D7                   vmovaps xmm2, xmm7                    
  0001801E19F0  C4C17828C8                 vmovaps xmm1, xmm8                    
  0001801E19F5  488D8F40020000             lea rcx, [rdi + 0x240]                
  0001801E19FC  E86FCAFDFF                 call 0x1801be470                         -> 0x1801BE470 (.text)
  0001801E1A01  8B4758                     mov eax, dword ptr [rdi + 0x58]       
  0001801E1A04  C57A1145CC                 vmovss dword ptr [rbp - 0x34], xmm8   
  0001801E1A09  C5FA117DD0                 vmovss dword ptr [rbp - 0x30], xmm7   
  0001801E1A0E  C57A1145C4                 vmovss dword ptr [rbp - 0x3c], xmm8   
  0001801E1A13  C5FA117DC8                 vmovss dword ptr [rbp - 0x38], xmm7   
  0001801E1A18  C745BC09000000             mov dword ptr [rbp - 0x44], 9         
  0001801E1A1F  C4C14A59C1                 vmulss xmm0, xmm6, xmm9               
  0001801E1A24  3BD8                       cmp ebx, eax                          
  0001801E1A26  C5FA2CC0                   vcvttss2si eax, xmm0                  
  0001801E1A2A  751E                       jne 0x1801e1a4a                          -> 0x1801E1A4A (.text)
  0001801E1A2C  66C78580000000FF5B         mov word ptr [rbp + 0x80], 0x5bff     
  0001801E1A35  C685820000005B             mov byte ptr [rbp + 0x82], 0x5b       
  0001801E1A3C  888583000000               mov byte ptr [rbp + 0x83], al         
  0001801E1A42  8B8580000000               mov eax, dword ptr [rbp + 0x80]       
  0001801E1A48  EB1C                       jmp 0x1801e1a66                          -> 0x1801E1A66 (.text)
  0001801E1A4A  66C78588000000C6C8         mov word ptr [rbp + 0x88], 0xc8c6     
  0001801E1A53  C6858A000000D0             mov byte ptr [rbp + 0x8a], 0xd0       
  0001801E1A5A  88858B000000               mov byte ptr [rbp + 0x8b], al         
  0001801E1A60  8B8588000000               mov eax, dword ptr [rbp + 0x88]       
  0001801E1A66  894598                     mov dword ptr [rbp - 0x68], eax       
  0001801E1A69  418B0E                     mov ecx, dword ptr [r14]              
  0001801E1A6C  E89FE20000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E1A71  4C8BC0                     mov r8, rax                           
  0001801E1A74  488D157D621600             lea rdx, [rip + 0x16627d]                ; -> 0x180347CF8
  0001801E1A7B  488D4D90                   lea rcx, [rbp - 0x70]                 
  0001801E1A7F  E87C98FBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E1A84  C4C14258FB                 vaddss xmm7, xmm7, xmm11              
  0001801E1A89  FFC3                       inc ebx                               
  0001801E1A8B  48FFC6                     inc rsi                               
  0001801E1A8E  4983C604                   add r14, 4                            
  0001801E1A92  3B9F24020000               cmp ebx, dword ptr [rdi + 0x224]      
  0001801E1A98  7F0B                       jg 0x1801e1aa5                           -> 0x1801E1AA5 (.text)
  0001801E1A9A  C5FA105C2478               vmovss xmm3, dword ptr [rsp + 0x78]   
  0001801E1AA0  E930FFFFFF                 jmp 0x1801e19d5                          -> 0x1801E19D5 (.text)
  0001801E1AA5  4C8D442450                 lea r8, [rsp + 0x50]                  
  0001801E1AAA  488D5590                   lea rdx, [rbp - 0x70]                 
  0001801E1AAE  488BCF                     mov rcx, rdi                          
  0001801E1AB1  E8DA0B0000                 call 0x1801e2690                         -> 0x1801E2690 (.text)
  0001801E1AB6  B201                       mov dl, 1                             
  0001801E1AB8  EB02                       jmp 0x1801e1abc                          -> 0x1801E1ABC (.text)
  0001801E1ABA  33D2                       xor edx, edx                          
  0001801E1ABC  8B8F9C020000               mov ecx, dword ptr [rdi + 0x29c]      
  0001801E1AC2  E8B981E4FF                 call 0x180029c80                         -> 0x180029C80 (.text)
  0001801E1AC7  418BCC                     mov ecx, r12d                         
  0001801E1ACA  E8E161FAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801E1ACF  90                         nop                                   
  0001801E1AD0  4C8D9C2450010000           lea r11, [rsp + 0x150]                
  0001801E1AD8  498B5B40                   mov rbx, qword ptr [r11 + 0x40]       
  0001801E1ADC  498B7348                   mov rsi, qword ptr [r11 + 0x48]       
  0001801E1AE0  C4C1782873F0               vmovaps xmm6, xmmword ptr [r11 - 0x10]
  0001801E1AE6  C4C178287BE0               vmovaps xmm7, xmmword ptr [r11 - 0x20]
  0001801E1AEC  C441782843D0               vmovaps xmm8, xmmword ptr [r11 - 0x30]
  0001801E1AF2  C44178284BC0               vmovaps xmm9, xmmword ptr [r11 - 0x40]
  0001801E1AF8  C441782853B0               vmovaps xmm10, xmmword ptr [r11 - 0x50]
  0001801E1AFE  C44178285BA0               vmovaps xmm11, xmmword ptr [r11 - 0x60]
  0001801E1B04  498BE3                     mov rsp, r11                          
  0001801E1B07  415F                       pop r15                               
  0001801E1B09  415E                       pop r14                               
  0001801E1B0B  415C                       pop r12                               
  0001801E1B0D  5F                         pop rdi                               
  0001801E1B0E  5D                         pop rbp                               
  0001801E1B0F  C3                         ret                                   
