; page_option.asm  --  TaskOption::draw  (l'en-tete HELP & OPTIONS)
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801A8420 - 0x1801A8559  (313 octets)
;
; A QUOI : Creneau [4] de la vtable TaskOption 0x180411348. Jumelle de FUN_1801B82D0 cote REVO, dont MENU.md 419.95 dit qu'elle porte l'en-tete 0x183 << HELP & OPTIONS >>, ligne 7 du menu principal, palier +3, NON corrigee.
;
; D'OU VIENT LE NOM : RTTI : vtable 0x180411348 creneau [4] ; MENU.md section 419.95
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
  0001801A8420  488BC4                     mov rax, rsp                          
  0001801A8423  55                         push rbp                              
  0001801A8424  488D68A1                   lea rbp, [rax - 0x5f]                 
  0001801A8428  4881ECE0000000             sub rsp, 0xe0                         
  0001801A842F  48C745B7FEFFFFFF           mov qword ptr [rbp - 0x49], 0xfffffffffffffffe
  0001801A8437  48895810                   mov qword ptr [rax + 0x10], rbx       
  0001801A843B  48897818                   mov qword ptr [rax + 0x18], rdi       
  0001801A843F  488BD9                     mov rbx, rcx                          
  0001801A8442  C5F857C0                   vxorps xmm0, xmm0, xmm0               
  0001801A8446  C5FA1145A7                 vmovss dword ptr [rbp - 0x59], xmm0   
  0001801A844B  C5FA1145AB                 vmovss dword ptr [rbp - 0x55], xmm0   
  0001801A8450  C5FA1145AF                 vmovss dword ptr [rbp - 0x51], xmm0   
  0001801A8455  E846F6FDFF                 call 0x180187aa0                         -> 0x180187AA0 (.text)
  0001801A845A  8BF8                       mov edi, eax                          
  0001801A845C  B902000000                 mov ecx, 2                            
  0001801A8461  E84AF8FDFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801A8466  488D8B08150000             lea rcx, [rbx + 0x1508]               
  0001801A846D  E89E550100                 call 0x1801bda10                         -> 0x1801BDA10 (.text)
  0001801A8472  84C0                       test al, al                           
  0001801A8474  0F84C3000000               je 0x1801a853d                           -> 0x1801A853D (.text)
  0001801A847A  48C744242000000000         mov qword ptr [rsp + 0x20], 0         
  0001801A8483  41B101                     mov r9b, 1                            
  0001801A8486  4C8D05FB8E2600             lea r8, [rip + 0x268efb]                 ; -> 0x180411388  "head_tit_ct"
  0001801A848D  488D55A7                   lea rdx, [rbp - 0x59]                 
  0001801A8491  488D8B08150000             lea rcx, [rbx + 0x1508]               
  0001801A8498  E8D3480100                 call 0x1801bcd70                         -> 0x1801BCD70 (.text)
  0001801A849D  84C0                       test al, al                           
  0001801A849F  0F8498000000               je 0x1801a853d                           -> 0x1801A853D (.text)
  0001801A84A5  488D4DC7                   lea rcx, [rbp - 0x39]                 
  0001801A84A9  E81224FFFF                 call 0x18019a8c0                         -> 0x18019A8C0 (.text)
  0001801A84AE  90                         nop                                   
  0001801A84AF  BA02000000                 mov edx, 2                            
  0001801A84B4  488D4D17                   lea rcx, [rbp + 0x17]                 
  0001801A84B8  E85324FFFF                 call 0x18019a910                         -> 0x18019A910 (.text)
  0001801A84BD  C5FA100DB32A1A00           vmovss xmm1, dword ptr [rip + 0x1a2ab3]   ; -> 0x18034AF78
  0001801A84C5  488D4D17                   lea rcx, [rbp + 0x17]                 
  0001801A84C9  E86233FFFF                 call 0x18019b830                         -> 0x18019B830 (.text)
  0001801A84CE  488D4517                   lea rax, [rbp + 0x17]                 
  0001801A84D2  4889450F                   mov qword ptr [rbp + 0xf], rax        
  0001801A84D6  C745EB0A000000             mov dword ptr [rbp - 0x15], 0xa       
  0001801A84DD  C5FA104DA7                 vmovss xmm1, dword ptr [rbp - 0x59]   
  0001801A84E2  C5FA114D03                 vmovss dword ptr [rbp + 3], xmm1      
  0001801A84E7  C5FA1045AB                 vmovss xmm0, dword ptr [rbp - 0x55]   
  0001801A84EC  C5FA114507                 vmovss dword ptr [rbp + 7], xmm0      
  0001801A84F1  C5FA114DFB                 vmovss dword ptr [rbp - 5], xmm1      
  0001801A84F6  C5FA1145FF                 vmovss dword ptr [rbp - 1], xmm0      
  0001801A84FB  C745F309000000             mov dword ptr [rbp - 0xd], 9          
  0001801A8502  C5FA1045AF                 vmovss xmm0, dword ptr [rbp - 0x51]   
  0001801A8507  C5FA590D3DE81900           vmulss xmm1, xmm0, dword ptr [rip + 0x19e83d]   ; -> 0x180346D4C
  0001801A850F  C5FA2CC1                   vcvttss2si eax, xmm1                  
  0001801A8513  66C74567FFB7               mov word ptr [rbp + 0x67], 0xb7ff     
  0001801A8519  C6456939                   mov byte ptr [rbp + 0x69], 0x39       
  0001801A851D  88456A                     mov byte ptr [rbp + 0x6a], al         
  0001801A8520  8B4567                     mov eax, dword ptr [rbp + 0x67]       
  0001801A8523  8945CF                     mov dword ptr [rbp - 0x31], eax       
  0001801A8526  B980010000                 mov ecx, 0x180                        
  0001801A852B  E8E0770400                 call 0x1801efd10                         -> 0x1801EFD10 (.text)
  0001801A8530  488BD0                     mov rdx, rax                          
  0001801A8533  488D4DC7                   lea rcx, [rbp - 0x39]                 
  0001801A8537  E8C42DFFFF                 call 0x18019b300                         -> 0x18019B300 (.text)
  0001801A853C  90                         nop                                   
  0001801A853D  8BCF                       mov ecx, edi                          
  0001801A853F  E86CF7FDFF                 call 0x180187cb0                         -> 0x180187CB0 (.text)
  0001801A8544  4C8D9C24E0000000           lea r11, [rsp + 0xe0]                 
  0001801A854C  498B5B18                   mov rbx, qword ptr [r11 + 0x18]       
  0001801A8550  498B7B20                   mov rdi, qword ptr [r11 + 0x20]       
  0001801A8554  498BE3                     mov rsp, r11                          
  0001801A8557  5D                         pop rbp                               
  0001801A8558  C3                         ret                                   
