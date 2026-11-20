; page_replays.asm  --  TaskMenuReplay::draw  (la page REPLAYS)
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801E1430 - 0x1801E1795  (869 octets)
;
; A QUOI : Creneau [4] de la vtable TaskMenuReplay 0x1805329C8. Jumelle de FUN_18020CFB0 cote REVO. MENU.md 419.95 fait 2 l'avait DEDUITE de son en-tete 0x2A2 << Replays >> ; le RTTI le confirme.
;
; D'OU VIENT LE NOM : RTTI : vtable 0x1805329C8 creneau [4] ; MENU.md section 419.95
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
  0001801E1430  488BC4                     mov rax, rsp                          
  0001801E1433  55                         push rbp                              
  0001801E1434  56                         push rsi                              
  0001801E1435  57                         push rdi                              
  0001801E1436  4156                       push r14                              
  0001801E1438  4157                       push r15                              
  0001801E143A  488D6888                   lea rbp, [rax - 0x78]                 
  0001801E143E  4881EC50010000             sub rsp, 0x150                        
  0001801E1445  48C745E0FEFFFFFF           mov qword ptr [rbp - 0x20], 0xfffffffffffffffe
  0001801E144D  48895818                   mov qword ptr [rax + 0x18], rbx       
  0001801E1451  C5F82970C8                 vmovaps xmmword ptr [rax - 0x38], xmm6
  0001801E1456  C5F82978B8                 vmovaps xmmword ptr [rax - 0x48], xmm7
  0001801E145B  C5782940A8                 vmovaps xmmword ptr [rax - 0x58], xmm8
  0001801E1460  C578294898                 vmovaps xmmword ptr [rax - 0x68], xmm9
  0001801E1465  C578295088                 vmovaps xmmword ptr [rax - 0x78], xmm10
  0001801E146A  C578299878FFFFFF           vmovaps xmmword ptr [rax - 0x88], xmm11
  0001801E1472  488BF1                     mov rsi, rcx                          
  0001801E1475  C74424409B020000           mov dword ptr [rsp + 0x40], 0x29b     
  0001801E147D  C74424449C020000           mov dword ptr [rsp + 0x44], 0x29c     
  0001801E1485  C74424489D020000           mov dword ptr [rsp + 0x48], 0x29d     
  0001801E148D  C5F857C0                   vxorps xmm0, xmm0, xmm0               
  0001801E1491  C5FA11442430               vmovss dword ptr [rsp + 0x30], xmm0   
  0001801E1497  C5FA11442434               vmovss dword ptr [rsp + 0x34], xmm0   
  0001801E149D  C5FA11442438               vmovss dword ptr [rsp + 0x38], xmm0   
  0001801E14A3  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E14A8  E81394FBFF                 call 0x18019a8c0                         -> 0x18019A8C0 (.text)
  0001801E14AD  90                         nop                                   
  0001801E14AE  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E14B2  E81995FBFF                 call 0x18019a9d0                         -> 0x18019A9D0 (.text)
  0001801E14B7  E8E465FAFF                 call 0x180187aa0                         -> 0x180187AA0 (.text)
  0001801E14BC  448BF8                     mov r15d, eax                         
  0001801E14BF  B902000000                 mov ecx, 2                            
  0001801E14C4  E8E767FAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801E14C9  488D8E40020000             lea rcx, [rsi + 0x240]                
  0001801E14D0  E83BC5FDFF                 call 0x1801bda10                         -> 0x1801BDA10 (.text)
  0001801E14D5  33DB                       xor ebx, ebx                          
  0001801E14D7  C5FA103D999A1600           vmovss xmm7, dword ptr [rip + 0x169a99]   ; -> 0x18034AF78
  0001801E14DF  C57A1005D16B1600           vmovss xmm8, dword ptr [rip + 0x166bd1]   ; -> 0x1803480B8
  0001801E14E7  C5FA1035219F1600           vmovss xmm6, dword ptr [rip + 0x169f21]   ; -> 0x18034B410
  0001801E14EF  C57A101555581600           vmovss xmm10, dword ptr [rip + 0x165855]   ; -> 0x180346D4C
  0001801E14F7  84C0                       test al, al                           
  0001801E14F9  0F84C8000000               je 0x1801e15c7                           -> 0x1801E15C7 (.text)
  0001801E14FF  48895C2420                 mov qword ptr [rsp + 0x20], rbx       
  0001801E1504  41B101                     mov r9b, 1                            
  0001801E1507  4C8D05D2F72200             lea r8, [rip + 0x22f7d2]                 ; -> 0x180410CE0  "p_small_head_lt"
  0001801E150E  488D542430                 lea rdx, [rsp + 0x30]                 
  0001801E1513  488D8E40020000             lea rcx, [rsi + 0x240]                
  0001801E151A  E851B8FDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E151F  8D5301                     lea edx, [rbx + 1]                    
  0001801E1522  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E1526  E8C5A1FBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801E152B  8D5302                     lea edx, [rbx + 2]                    
  0001801E152E  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E1532  E839A3FBFF                 call 0x18019b870                         -> 0x18019B870 (.text)
  0001801E1537  C5F828CF                   vmovaps xmm1, xmm7                    
  0001801E153B  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E153F  E8ECA2FBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801E1544  C57A1145D4                 vmovss dword ptr [rbp - 0x2c], xmm8   
  0001801E1549  C5FA1175D8                 vmovss dword ptr [rbp - 0x28], xmm6   
  0001801E154E  488D45A0                   lea rax, [rbp - 0x60]                 
  0001801E1552  48894598                   mov qword ptr [rbp - 0x68], rax       
  0001801E1556  C744247412000000           mov dword ptr [rsp + 0x74], 0x12      
  0001801E155E  C5FA104C2430               vmovss xmm1, dword ptr [rsp + 0x30]   
  0001801E1564  C5FA114D8C                 vmovss dword ptr [rbp - 0x74], xmm1   
  0001801E1569  C5FA10442434               vmovss xmm0, dword ptr [rsp + 0x34]   
  0001801E156F  C5FA114590                 vmovss dword ptr [rbp - 0x70], xmm0   
  0001801E1574  C5FA114D84                 vmovss dword ptr [rbp - 0x7c], xmm1   
  0001801E1579  C5FA114588                 vmovss dword ptr [rbp - 0x78], xmm0   
  0001801E157E  C744247C09000000           mov dword ptr [rsp + 0x7c], 9         
  0001801E1586  C5AA594C2438               vmulss xmm1, xmm10, dword ptr [rsp + 0x38]
  0001801E158C  C5FA2CC1                   vcvttss2si eax, xmm1                  
  0001801E1590  66C78580000000FFB7         mov word ptr [rbp + 0x80], 0xb7ff     
  0001801E1599  C6858200000039             mov byte ptr [rbp + 0x82], 0x39       
  0001801E15A0  888583000000               mov byte ptr [rbp + 0x83], al         
  0001801E15A6  8B8580000000               mov eax, dword ptr [rbp + 0x80]       
  0001801E15AC  89442458                   mov dword ptr [rsp + 0x58], eax       
  0001801E15B0  B99A020000                 mov ecx, 0x29a                        
  0001801E15B5  E856E70000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E15BA  488BD0                     mov rdx, rax                          
  0001801E15BD  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E15C2  E8399DFBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E15C7  488D8E98020000             lea rcx, [rsi + 0x298]                
  0001801E15CE  E83DC4FDFF                 call 0x1801bda10                         -> 0x1801BDA10 (.text)
  0001801E15D3  84C0                       test al, al                           
  0001801E15D5  0F8476010000               je 0x1801e1751                           -> 0x1801E1751 (.text)
  0001801E15DB  48895C2420                 mov qword ptr [rsp + 0x20], rbx       
  0001801E15E0  41B101                     mov r9b, 1                            
  0001801E15E3  4C8D053E941B00             lea r8, [rip + 0x1b943e]                 ; -> 0x18039AA28  "p_txt_01_lt"
  0001801E15EA  488D542430                 lea rdx, [rsp + 0x30]                 
  0001801E15EF  488D8E98020000             lea rcx, [rsi + 0x298]                
  0001801E15F6  E875B7FDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E15FB  BA01000000                 mov edx, 1                            
  0001801E1600  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E1604  E8E7A0FBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801E1609  BA02000000                 mov edx, 2                            
  0001801E160E  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E1612  E859A2FBFF                 call 0x18019b870                         -> 0x18019B870 (.text)
  0001801E1617  C5F828CF                   vmovaps xmm1, xmm7                    
  0001801E161B  488D4DA0                   lea rcx, [rbp - 0x60]                 
  0001801E161F  E80CA2FBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801E1624  C57A1145D4                 vmovss dword ptr [rbp - 0x2c], xmm8   
  0001801E1629  C5FA1175D8                 vmovss dword ptr [rbp - 0x28], xmm6   
  0001801E162E  488D45A0                   lea rax, [rbp - 0x60]                 
  0001801E1632  48894598                   mov qword ptr [rbp - 0x68], rax       
  0001801E1636  C744247412000000           mov dword ptr [rsp + 0x74], 0x12      
  0001801E163E  C54A585DC8                 vaddss xmm11, xmm6, dword ptr [rbp - 0x38]
  0001801E1643  C5A2587C2434               vaddss xmm7, xmm11, dword ptr [rsp + 0x34]
  0001801E1649  C57A10442430               vmovss xmm8, dword ptr [rsp + 0x30]   
  0001801E164F  399E24020000               cmp dword ptr [rsi + 0x224], ebx      
  0001801E1655  0F8CF6000000               jl 0x1801e1751                           -> 0x1801E1751 (.text)
  0001801E165B  488BFB                     mov rdi, rbx                          
  0001801E165E  C57A100DD2561600           vmovss xmm9, dword ptr [rip + 0x1656d2]   ; -> 0x180346D38
  0001801E1666  66660F1F840000000000       nop word ptr [rax + rax]              
  0001801E1670  C5FA10742438               vmovss xmm6, dword ptr [rsp + 0x38]   
  0001801E1676  80BC3EF302000000           cmp byte ptr [rsi + rdi + 0x2f3], 0   
  0001801E167E  750E                       jne 0x1801e168e                          -> 0x1801E168E (.text)
  0001801E1680  4885FF                     test rdi, rdi                         
  0001801E1683  750E                       jne 0x1801e1693                          -> 0x1801E1693 (.text)
  0001801E1685  E88659FDFF                 call 0x1801b7010                         -> 0x1801B7010 (.text)
  0001801E168A  84C0                       test al, al                           
  0001801E168C  7505                       jne 0x1801e1693                          -> 0x1801E1693 (.text)
  0001801E168E  C4C14A59F1                 vmulss xmm6, xmm6, xmm9               
  0001801E1693  8B4658                     mov eax, dword ptr [rsi + 0x58]       
  0001801E1696  3BD8                       cmp ebx, eax                          
  0001801E1698  751D                       jne 0x1801e16b7                          -> 0x1801E16B7 (.text)
  0001801E169A  C5FA105DC8                 vmovss xmm3, dword ptr [rbp - 0x38]   
  0001801E169F  C5F828D7                   vmovaps xmm2, xmm7                    
  0001801E16A3  C4C17828C8                 vmovaps xmm1, xmm8                    
  0001801E16A8  488D8E98020000             lea rcx, [rsi + 0x298]                
  0001801E16AF  E8BCCDFDFF                 call 0x1801be470                         -> 0x1801BE470 (.text)
  0001801E16B4  8B4658                     mov eax, dword ptr [rsi + 0x58]       
  0001801E16B7  C57A11458C                 vmovss dword ptr [rbp - 0x74], xmm8   
  0001801E16BC  C5FA117D90                 vmovss dword ptr [rbp - 0x70], xmm7   
  0001801E16C1  C57A114584                 vmovss dword ptr [rbp - 0x7c], xmm8   
  0001801E16C6  C5FA117D88                 vmovss dword ptr [rbp - 0x78], xmm7   
  0001801E16CB  C744247C09000000           mov dword ptr [rsp + 0x7c], 9         
  0001801E16D3  C4C14A59C2                 vmulss xmm0, xmm6, xmm10              
  0001801E16D8  3BD8                       cmp ebx, eax                          
  0001801E16DA  C5FA2CC0                   vcvttss2si eax, xmm0                  
  0001801E16DE  751E                       jne 0x1801e16fe                          -> 0x1801E16FE (.text)
  0001801E16E0  66C78580000000FF5B         mov word ptr [rbp + 0x80], 0x5bff     
  0001801E16E9  C685820000005B             mov byte ptr [rbp + 0x82], 0x5b       
  0001801E16F0  888583000000               mov byte ptr [rbp + 0x83], al         
  0001801E16F6  8B8580000000               mov eax, dword ptr [rbp + 0x80]       
  0001801E16FC  EB1C                       jmp 0x1801e171a                          -> 0x1801E171A (.text)
  0001801E16FE  66C78588000000C6C8         mov word ptr [rbp + 0x88], 0xc8c6     
  0001801E1707  C6858A000000D0             mov byte ptr [rbp + 0x8a], 0xd0       
  0001801E170E  88858B000000               mov byte ptr [rbp + 0x8b], al         
  0001801E1714  8B8588000000               mov eax, dword ptr [rbp + 0x88]       
  0001801E171A  89442458                   mov dword ptr [rsp + 0x58], eax       
  0001801E171E  8B4CBC40                   mov ecx, dword ptr [rsp + rdi*4 + 0x40]
  0001801E1722  E8E9E50000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E1727  4C8BC0                     mov r8, rax                           
  0001801E172A  488D15C7651600             lea rdx, [rip + 0x1665c7]                ; -> 0x180347CF8
  0001801E1731  488D4C2450                 lea rcx, [rsp + 0x50]                 
  0001801E1736  E8C59BFBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E173B  C4C14258FB                 vaddss xmm7, xmm7, xmm11              
  0001801E1740  FFC3                       inc ebx                               
  0001801E1742  48FFC7                     inc rdi                               
  0001801E1745  3B9E24020000               cmp ebx, dword ptr [rsi + 0x224]      
  0001801E174B  0F8E1FFFFFFF               jle 0x1801e1670                          -> 0x1801E1670 (.text)
  0001801E1751  418BCF                     mov ecx, r15d                         
  0001801E1754  E85765FAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801E1759  90                         nop                                   
  0001801E175A  4C8D9C2450010000           lea r11, [rsp + 0x150]                
  0001801E1762  498B5B40                   mov rbx, qword ptr [r11 + 0x40]       
  0001801E1766  C4C1782873F0               vmovaps xmm6, xmmword ptr [r11 - 0x10]
  0001801E176C  C4C178287BE0               vmovaps xmm7, xmmword ptr [r11 - 0x20]
  0001801E1772  C441782843D0               vmovaps xmm8, xmmword ptr [r11 - 0x30]
  0001801E1778  C44178284BC0               vmovaps xmm9, xmmword ptr [r11 - 0x40]
  0001801E177E  C441782853B0               vmovaps xmm10, xmmword ptr [r11 - 0x50]
  0001801E1784  C44178285BA0               vmovaps xmm11, xmmword ptr [r11 - 0x60]
  0001801E178A  498BE3                     mov rsp, r11                          
  0001801E178D  415F                       pop r15                               
  0001801E178F  415E                       pop r14                               
  0001801E1791  5F                         pop rdi                               
  0001801E1792  5E                         pop rsi                               
  0001801E1793  5D                         pop rbp                               
  0001801E1794  C3                         ret                                   
