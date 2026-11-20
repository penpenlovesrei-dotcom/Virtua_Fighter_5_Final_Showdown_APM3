; menu_dessin_page.asm  --  Menu_DessinerUnePage
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801E0C80 - 0x1801E10DA  (1114 octets)
;
; A QUOI : Le dessin d'une page de menu : boucle de 0 au DERNIER INDICE inclus (0x1801E1079 `cmp edi,[rsi+0x224]` / `jle`), lit l'etat de chaque entree dans page+0x642+i (0 normal, 1 grisee, 2 pas dessinee), resout chaque libelle par 0x1801EFD10, et choisit en 0x1801E0D3D entre UNLOCK FULL GAME et DOWNLOAD CONTENT par un `cmove`. Jumelle probable de FUN_18020C880 cote REVO.
;
; D'OU VIENT LE NOM : VF5RE/analysis/menu_console.md, sections 8.2 et 8.3 ; VF5RE/code_decompile/MENU.md section 419.83
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
  0001801E0C80  488BC4                     mov rax, rsp                          
  0001801E0C83  55                         push rbp                              
  0001801E0C84  56                         push rsi                              
  0001801E0C85  57                         push rdi                              
  0001801E0C86  4154                       push r12                              
  0001801E0C88  4155                       push r13                              
  0001801E0C8A  4156                       push r14                              
  0001801E0C8C  4157                       push r15                              
  0001801E0C8E  488DA818FFFFFF             lea rbp, [rax - 0xe8]                 
  0001801E0C95  4881ECB0010000             sub rsp, 0x1b0                        
  0001801E0C9C  48C74520FEFFFFFF           mov qword ptr [rbp + 0x20], 0xfffffffffffffffe
  0001801E0CA4  48895808                   mov qword ptr [rax + 8], rbx          
  0001801E0CA8  C5F82970B8                 vmovaps xmmword ptr [rax - 0x48], xmm6
  0001801E0CAD  C5F82978A8                 vmovaps xmmword ptr [rax - 0x58], xmm7
  0001801E0CB2  C578294098                 vmovaps xmmword ptr [rax - 0x68], xmm8
  0001801E0CB7  C578294888                 vmovaps xmmword ptr [rax - 0x78], xmm9
  0001801E0CBC  C578299078FFFFFF           vmovaps xmmword ptr [rax - 0x88], xmm10
  0001801E0CC4  C578299868FFFFFF           vmovaps xmmword ptr [rax - 0x98], xmm11
  0001801E0CCC  C57829A058FFFFFF           vmovaps xmmword ptr [rax - 0xa8], xmm12
  0001801E0CD4  C57829A848FFFFFF           vmovaps xmmword ptr [rax - 0xb8], xmm13
  0001801E0CDC  488BF1                     mov rsi, rcx                          
  0001801E0CDF  488B050AAAA500             mov rax, qword ptr [rip + 0xa5aa0a]      ; -> 0x180C3B6F0
  0001801E0CE6  4885C0                     test rax, rax                         
  0001801E0CE9  740E                       je 0x1801e0cf9                           -> 0x1801E0CF9 (.text)
  0001801E0CEB  4883B810FE010000           cmp qword ptr [rax + 0x1fe10], 0      
  0001801E0CF3  0F8596030000               jne 0x1801e108f                          -> 0x1801E108F (.text)
  0001801E0CF9  C745B077010000             mov dword ptr [rbp - 0x50], 0x177     
  0001801E0D00  C745B478010000             mov dword ptr [rbp - 0x4c], 0x178     
  0001801E0D07  C745B87A010000             mov dword ptr [rbp - 0x48], 0x17a     
  0001801E0D0E  C745BC7B010000             mov dword ptr [rbp - 0x44], 0x17b     
  0001801E0D15  C745C07C010000             mov dword ptr [rbp - 0x40], 0x17c     
  0001801E0D1C  C745C47E010000             mov dword ptr [rbp - 0x3c], 0x17e     
  0001801E0D23  C745C87F010000             mov dword ptr [rbp - 0x38], 0x17f     
  0001801E0D2A  C745CC80010000             mov dword ptr [rbp - 0x34], 0x180     
  0001801E0D31  BB81010000                 mov ebx, 0x181                        
  0001801E0D36  C745D483010000             mov dword ptr [rbp - 0x2c], 0x183     
  0001801E0D3D  E80E67E2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801E0D42  B982010000                 mov ecx, 0x182                        
  0001801E0D47  84C0                       test al, al                           
  0001801E0D49  0F44D9                     cmove ebx, ecx                        
  0001801E0D4C  895DD0                     mov dword ptr [rbp - 0x30], ebx       
  0001801E0D4F  C5F857C0                   vxorps xmm0, xmm0, xmm0               
  0001801E0D53  C5FA11442438               vmovss dword ptr [rsp + 0x38], xmm0   
  0001801E0D59  C5FA1144243C               vmovss dword ptr [rsp + 0x3c], xmm0   
  0001801E0D5F  C5FA11442440               vmovss dword ptr [rsp + 0x40], xmm0   
  0001801E0D65  C5FA11442450               vmovss dword ptr [rsp + 0x50], xmm0   
  0001801E0D6B  C5FA11442454               vmovss dword ptr [rsp + 0x54], xmm0   
  0001801E0D71  C5FA11442458               vmovss dword ptr [rsp + 0x58], xmm0   
  0001801E0D77  488D4C2460                 lea rcx, [rsp + 0x60]                 
  0001801E0D7C  E83F9BFBFF                 call 0x18019a8c0                         -> 0x18019A8C0 (.text)
  0001801E0D81  90                         nop                                   
  0001801E0D82  488D4DE0                   lea rcx, [rbp - 0x20]                 
  0001801E0D86  E8459CFBFF                 call 0x18019a9d0                         -> 0x18019A9D0 (.text)
  0001801E0D8B  E8106DFAFF                 call 0x180187aa0                         -> 0x180187AA0 (.text)
  0001801E0D90  89442448                   mov dword ptr [rsp + 0x48], eax       
  0001801E0D94  B902000000                 mov ecx, 2                            
  0001801E0D99  E8126FFAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801E0D9E  488D8E40020000             lea rcx, [rsi + 0x240]                
  0001801E0DA5  E866CCFDFF                 call 0x1801bda10                         -> 0x1801BDA10 (.text)
  0001801E0DAA  33FF                       xor edi, edi                          
  0001801E0DAC  C57A100D985F1600           vmovss xmm9, dword ptr [rip + 0x165f98]   ; -> 0x180346D4C
  0001801E0DB4  84C0                       test al, al                           
  0001801E0DB6  0F84A3000000               je 0x1801e0e5f                           -> 0x1801E0E5F (.text)
  0001801E0DBC  48897C2420                 mov qword ptr [rsp + 0x20], rdi       
  0001801E0DC1  41B101                     mov r9b, 1                            
  0001801E0DC4  4C8D05751E3500             lea r8, [rip + 0x351e75]                 ; -> 0x180532C40  "p_main_head_lt"
  0001801E0DCB  488D542438                 lea rdx, [rsp + 0x38]                 
  0001801E0DD0  488D8E40020000             lea rcx, [rsi + 0x240]                
  0001801E0DD7  E894BFFDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E0DDC  8D5702                     lea edx, [rdi + 2]                    
  0001801E0DDF  488D4DE0                   lea rcx, [rbp - 0x20]                 
  0001801E0DE3  E808A9FBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801E0DE8  488D45E0                   lea rax, [rbp - 0x20]                 
  0001801E0DEC  488945A8                   mov qword ptr [rbp - 0x58], rax       
  0001801E0DF0  C7458408000000             mov dword ptr [rbp - 0x7c], 8         
  0001801E0DF7  C5FA104C2438               vmovss xmm1, dword ptr [rsp + 0x38]   
  0001801E0DFD  C5FA114D9C                 vmovss dword ptr [rbp - 0x64], xmm1   
  0001801E0E02  C5FA1044243C               vmovss xmm0, dword ptr [rsp + 0x3c]   
  0001801E0E08  C5FA1145A0                 vmovss dword ptr [rbp - 0x60], xmm0   
  0001801E0E0D  C5FA114D94                 vmovss dword ptr [rbp - 0x6c], xmm1   
  0001801E0E12  C5FA114598                 vmovss dword ptr [rbp - 0x68], xmm0   
  0001801E0E17  C7458C09000000             mov dword ptr [rbp - 0x74], 9         
  0001801E0E1E  C5B2594C2440               vmulss xmm1, xmm9, dword ptr [rsp + 0x40]
  0001801E0E24  C5FA2CC1                   vcvttss2si eax, xmm1                  
  0001801E0E28  66C785F8000000FFB7         mov word ptr [rbp + 0xf8], 0xb7ff     
  0001801E0E31  C685FA00000039             mov byte ptr [rbp + 0xfa], 0x39       
  0001801E0E38  8885FB000000               mov byte ptr [rbp + 0xfb], al         
  0001801E0E3E  8B85F8000000               mov eax, dword ptr [rbp + 0xf8]       
  0001801E0E44  89442468                   mov dword ptr [rsp + 0x68], eax       
  0001801E0E48  B976010000                 mov ecx, 0x176                        
  0001801E0E4D  E8BEEE0000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E0E52  488BD0                     mov rdx, rax                          
  0001801E0E55  488D4C2460                 lea rcx, [rsp + 0x60]                 
  0001801E0E5A  E8A1A4FBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E0E5F  488D8E98020000             lea rcx, [rsi + 0x298]                
  0001801E0E66  E8A5CBFDFF                 call 0x1801bda10                         -> 0x1801BDA10 (.text)
  0001801E0E6B  84C0                       test al, al                           
  0001801E0E6D  0F8412020000               je 0x1801e1085                           -> 0x1801E1085 (.text)
  0001801E0E73  48897C2420                 mov qword ptr [rsp + 0x20], rdi       
  0001801E0E78  41B101                     mov r9b, 1                            
  0001801E0E7B  4C8D05CE1D3500             lea r8, [rip + 0x351dce]                 ; -> 0x180532C50  "p_menutxt_PS3_lt"
  0001801E0E82  488D542438                 lea rdx, [rsp + 0x38]                 
  0001801E0E87  488D8E98020000             lea rcx, [rsi + 0x298]                
  0001801E0E8E  E8DDBEFDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E0E93  48897C2420                 mov qword ptr [rsp + 0x20], rdi       
  0001801E0E98  4533C9                     xor r9d, r9d                          
  0001801E0E9B  4C8D05C61D3500             lea r8, [rip + 0x351dc6]                 ; -> 0x180532C68  "p_menutxt_02_rb"
  0001801E0EA2  488D542450                 lea rdx, [rsp + 0x50]                 
  0001801E0EA7  488D8E98020000             lea rcx, [rsi + 0x298]                
  0001801E0EAE  E8BDBEFDFF                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801E0EB3  BA02000000                 mov edx, 2                            
  0001801E0EB8  488D4DE0                   lea rcx, [rbp - 0x20]                 
  0001801E0EBC  E82FA8FBFF                 call 0x18019b6f0                         -> 0x18019B6F0 (.text)
  0001801E0EC1  C5FA100DAFA01600           vmovss xmm1, dword ptr [rip + 0x16a0af]   ; -> 0x18034AF78
  0001801E0EC9  488D4DE0                   lea rcx, [rbp - 0x20]                 
  0001801E0ECD  E85EA9FBFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801E0ED2  C5FA100D96A01600           vmovss xmm1, dword ptr [rip + 0x16a096]   ; -> 0x18034AF70
  0001801E0EDA  C5FA114D18                 vmovss dword ptr [rbp + 0x18], xmm1   
  0001801E0EDF  488D45E0                   lea rax, [rbp - 0x20]                 
  0001801E0EE3  488945A8                   mov qword ptr [rbp - 0x58], rax       
  0001801E0EE7  C745840C000000             mov dword ptr [rbp - 0x7c], 0xc       
  0001801E0EEE  C572586D08                 vaddss xmm13, xmm1, dword ptr [rbp + 8]
  0001801E0EF3  C57A10442438               vmovss xmm8, dword ptr [rsp + 0x38]   
  0001801E0EF9  C5FA1074243C               vmovss xmm6, dword ptr [rsp + 0x3c]   
  0001801E0EFF  39BE24020000               cmp dword ptr [rsi + 0x224], edi      
  0001801E0F05  0F8C7A010000               jl 0x1801e1085                           -> 0x1801E1085 (.text)
  0001801E0F0B  4C8DB642060000             lea r14, [rsi + 0x642]                
  0001801E0F12  4C8D7DB0                   lea r15, [rbp - 0x50]                 
  0001801E0F16  C57A10151A5E1600           vmovss xmm10, dword ptr [rip + 0x165e1a]   ; -> 0x180346D38
  0001801E0F1E  C57A1025826D1600           vmovss xmm12, dword ptr [rip + 0x166d82]   ; -> 0x180347CA8
  0001801E0F26  C57A101D1A5E1600           vmovss xmm11, dword ptr [rip + 0x165e1a]   ; -> 0x180346D48
  0001801E0F2E  6690                       nop                                   
  0001801E0F30  41803E02                   cmp byte ptr [r14], 2                 
  0001801E0F34  0F8436010000               je 0x1801e1070                           -> 0x1801E1070 (.text)
  0001801E0F3A  418B0F                     mov ecx, dword ptr [r15]              
  0001801E0F3D  E8CEED0000                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801E0F42  4C8BE0                     mov r12, rax                          
  0001801E0F45  41803E01                   cmp byte ptr [r14], 1                 
  0001801E0F49  750D                       jne 0x1801e0f58                          -> 0x1801E0F58 (.text)
  0001801E0F4B  C5FA10442440               vmovss xmm0, dword ptr [rsp + 0x40]   
  0001801E0F51  C4C17A59FA                 vmulss xmm7, xmm0, xmm10              
  0001801E0F56  EB06                       jmp 0x1801e0f5e                          -> 0x1801E0F5E (.text)
  0001801E0F58  C5FA107C2440               vmovss xmm7, dword ptr [rsp + 0x40]   
  0001801E0F5E  8B4658                     mov eax, dword ptr [rsi + 0x58]       
  0001801E0F61  3BF8                       cmp edi, eax                          
  0001801E0F63  751D                       jne 0x1801e0f82                          -> 0x1801E0F82 (.text)
  0001801E0F65  C4C13A5CCC                 vsubss xmm1, xmm8, xmm12              
  0001801E0F6A  C5FA105D08                 vmovss xmm3, dword ptr [rbp + 8]      
  0001801E0F6F  C5F828D6                   vmovaps xmm2, xmm6                    
  0001801E0F73  488D8E98020000             lea rcx, [rsi + 0x298]                
  0001801E0F7A  E8F1D4FDFF                 call 0x1801be470                         -> 0x1801BE470 (.text)
  0001801E0F7F  8B4658                     mov eax, dword ptr [rsi + 0x58]       
  0001801E0F82  C4C13A5CC3                 vsubss xmm0, xmm8, xmm11              
  0001801E0F87  C5FA11459C                 vmovss dword ptr [rbp - 0x64], xmm0   
  0001801E0F8C  C5FA1175A0                 vmovss dword ptr [rbp - 0x60], xmm6   
  0001801E0F91  C5FA114594                 vmovss dword ptr [rbp - 0x6c], xmm0   
  0001801E0F96  C5FA117598                 vmovss dword ptr [rbp - 0x68], xmm6   
  0001801E0F9B  C7458C09000000             mov dword ptr [rbp - 0x74], 9         
  0001801E0FA2  C4C14259C1                 vmulss xmm0, xmm7, xmm9               
  0001801E0FA7  C5FA2CD8                   vcvttss2si ebx, xmm0                  
  0001801E0FAB  3BF8                       cmp edi, eax                          
  0001801E0FAD  751E                       jne 0x1801e0fcd                          -> 0x1801E0FCD (.text)
  0001801E0FAF  66C785F80000005A00         mov word ptr [rbp + 0xf8], 0x5a       
  0001801E0FB8  C685FA00000000             mov byte ptr [rbp + 0xfa], 0          
  0001801E0FBF  889DFB000000               mov byte ptr [rbp + 0xfb], bl         
  0001801E0FC5  8B85F8000000               mov eax, dword ptr [rbp + 0xf8]       
  0001801E0FCB  EB1C                       jmp 0x1801e0fe9                          -> 0x1801E0FE9 (.text)
  0001801E0FCD  66C785000100006E71         mov word ptr [rbp + 0x100], 0x716e    
  0001801E0FD6  C6850201000075             mov byte ptr [rbp + 0x102], 0x75      
  0001801E0FDD  889D03010000               mov byte ptr [rbp + 0x103], bl        
  0001801E0FE3  8B8500010000               mov eax, dword ptr [rbp + 0x100]      
  0001801E0FE9  89442468                   mov dword ptr [rsp + 0x68], eax       
  0001801E0FED  4D8BC4                     mov r8, r12                           
  0001801E0FF0  488D15016D1600             lea rdx, [rip + 0x166d01]                ; -> 0x180347CF8
  0001801E0FF7  488D4C2460                 lea rcx, [rsp + 0x60]                 
  0001801E0FFC  E8FFA2FBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E1001  C57A11459C                 vmovss dword ptr [rbp - 0x64], xmm8   
  0001801E1006  C5FA1175A0                 vmovss dword ptr [rbp - 0x60], xmm6   
  0001801E100B  C57A114594                 vmovss dword ptr [rbp - 0x6c], xmm8   
  0001801E1010  C5FA117598                 vmovss dword ptr [rbp - 0x68], xmm6   
  0001801E1015  C7458C09000000             mov dword ptr [rbp - 0x74], 9         
  0001801E101C  3B7E58                     cmp edi, dword ptr [rsi + 0x58]       
  0001801E101F  751E                       jne 0x1801e103f                          -> 0x1801E103F (.text)
  0001801E1021  66C78508010000FF5B         mov word ptr [rbp + 0x108], 0x5bff    
  0001801E102A  C6850A0100005B             mov byte ptr [rbp + 0x10a], 0x5b      
  0001801E1031  889D0B010000               mov byte ptr [rbp + 0x10b], bl        
  0001801E1037  8B8508010000               mov eax, dword ptr [rbp + 0x108]      
  0001801E103D  EB14                       jmp 0x1801e1053                          -> 0x1801E1053 (.text)
  0001801E103F  66C7442430C6C8             mov word ptr [rsp + 0x30], 0xc8c6     
  0001801E1046  C6442432D0                 mov byte ptr [rsp + 0x32], 0xd0       
  0001801E104B  885C2433                   mov byte ptr [rsp + 0x33], bl         
  0001801E104F  8B442430                   mov eax, dword ptr [rsp + 0x30]       
  0001801E1053  89442468                   mov dword ptr [rsp + 0x68], eax       
  0001801E1057  4D8BC4                     mov r8, r12                           
  0001801E105A  488D15976C1600             lea rdx, [rip + 0x166c97]                ; -> 0x180347CF8
  0001801E1061  488D4C2460                 lea rcx, [rsp + 0x60]                 
  0001801E1066  E895A2FBFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801E106B  C4C14A58F5                 vaddss xmm6, xmm6, xmm13              
  0001801E1070  FFC7                       inc edi                               
  0001801E1072  4983C704                   add r15, 4                            
  0001801E1076  49FFC6                     inc r14                               
  0001801E1079  3BBE24020000               cmp edi, dword ptr [rsi + 0x224]      
  0001801E107F  0F8EABFEFFFF               jle 0x1801e0f30                          -> 0x1801E0F30 (.text)
  0001801E1085  8B4C2448                   mov ecx, dword ptr [rsp + 0x48]       
  0001801E1089  E8226CFAFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801E108E  90                         nop                                   
  0001801E108F  4C8D9C24B0010000           lea r11, [rsp + 0x1b0]                
  0001801E1097  498B5B40                   mov rbx, qword ptr [r11 + 0x40]       
  0001801E109B  C4C1782873F0               vmovaps xmm6, xmmword ptr [r11 - 0x10]
  0001801E10A1  C4C178287BE0               vmovaps xmm7, xmmword ptr [r11 - 0x20]
  0001801E10A7  C441782843D0               vmovaps xmm8, xmmword ptr [r11 - 0x30]
  0001801E10AD  C44178284BC0               vmovaps xmm9, xmmword ptr [r11 - 0x40]
  0001801E10B3  C441782853B0               vmovaps xmm10, xmmword ptr [r11 - 0x50]
  0001801E10B9  C44178285BA0               vmovaps xmm11, xmmword ptr [r11 - 0x60]
  0001801E10BF  C44178286390               vmovaps xmm12, xmmword ptr [r11 - 0x70]
  0001801E10C5  C44178286B80               vmovaps xmm13, xmmword ptr [r11 - 0x80]
  0001801E10CB  498BE3                     mov rsp, r11                          
  0001801E10CE  415F                       pop r15                               
  0001801E10D0  415E                       pop r14                               
  0001801E10D2  415D                       pop r13                               
  0001801E10D4  415C                       pop r12                               
  0001801E10D6  5F                         pop rdi                               
  0001801E10D7  5E                         pop rsi                               
  0001801E10D8  5D                         pop rbp                               
  0001801E10D9  C3                         ret                                   
