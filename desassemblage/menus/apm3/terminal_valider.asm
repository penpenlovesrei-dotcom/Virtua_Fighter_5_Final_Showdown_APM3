; terminal_valider.asm  --  TaskMenuTerminal::validate
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801DE340 - 0x1801DE439  (249 octets)   [4 entrees .pdata chainees]
;
; A QUOI : Dernier creneau non bouchonne [10] de la vtable TaskMenuTerminal 0x180532A28 : la validation de la page TERMINAL. 0 reference directe (methode virtuelle). C'est l'une des onze fonctions que VF5RE/desassemblages/APM3_A_VIDER.txt signale comme videes NULLE PART.
;
; D'OU VIENT LE NOM : RTTI : vtable 0x180532A28 creneau [10] ; VF5RE/desassemblages/APM3_A_VIDER.txt
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
  0001801DE340  48895C2410                 mov qword ptr [rsp + 0x10], rbx       
  0001801DE345  56                         push rsi                              
  0001801DE346  4883EC20                   sub rsp, 0x20                         
  0001801DE34A  4883B9F802000000           cmp qword ptr [rcx + 0x2f8], 0        
  0001801DE352  8BF2                       mov esi, edx                          
  0001801DE354  488BD9                     mov rbx, rcx                          
  0001801DE357  0F85D1000000               jne 0x1801de42e                          -> 0x1801DE42E (.text)
  0001801DE35D  48897C2430                 mov qword ptr [rsp + 0x30], rdi       
  0001801DE362  8B7958                     mov edi, dword ptr [rcx + 0x58]       
  0001801DE365  85FF                       test edi, edi                         
  0001801DE367  7536                       jne 0x1801de39f                          -> 0x1801DE39F (.text)
  0001801DE369  E8A28CFDFF                 call 0x1801b7010                         -> 0x1801B7010 (.text)
  0001801DE36E  84C0                       test al, al                           
  0001801DE370  0F84B3000000               je 0x1801de429                           -> 0x1801DE429 (.text)
  0001801DE376  E835BCE4FF                 call 0x180029fb0                         -> 0x180029FB0 (.text)
  0001801DE37B  84C0                       test al, al                           
  0001801DE37D  0F84A6000000               je 0x1801de429                           -> 0x1801DE429 (.text)
  0001801DE383  8BD6                       mov edx, esi                          
  0001801DE385  488BCB                     mov rcx, rbx                          
  0001801DE388  E883DCFDFF                 call 0x1801bc010                         -> 0x1801BC010 (.text)
  0001801DE38D  8D4F05                     lea ecx, [rdi + 5]                    
  0001801DE390  E80BC6EFFF                 call 0x1800da9a0                         -> 0x1800DA9A0 (.text)
  0001801DE395  8D4F25                     lea ecx, [rdi + 0x25]                 
  0001801DE398  E823C6EFFF                 call 0x1800da9c0                         -> 0x1800DA9C0 (.text)
  0001801DE39D  EB43                       jmp 0x1801de3e2                          -> 0x1801DE3E2 (.text)
  0001801DE39F  E86CDCFDFF                 call 0x1801bc010                         -> 0x1801BC010 (.text)
  0001801DE3A4  83FF01                     cmp edi, 1                            
  0001801DE3A7  7559                       jne 0x1801de402                          -> 0x1801DE402 (.text)
  0001801DE3A9  488DBB00030000             lea rdi, [rbx + 0x300]                
  0001801DE3B0  C7835803000000000000       mov dword ptr [rbx + 0x358], 0        
  0001801DE3BA  488BCF                     mov rcx, rdi                          
  0001801DE3BD  C6836003000000             mov byte ptr [rbx + 0x360], 0         
  0001801DE3C4  488D156D4B3500             lea rdx, [rip + 0x354b6d]                ; -> 0x180532F38  "REPLAY MENU"
  0001801DE3CB  C683F205000000             mov byte ptr [rbx + 0x5f2], 0         
  0001801DE3D2  E859740600                 call 0x180245830                         -> 0x180245830 (.text)
  0001801DE3D7  84C0                       test al, al                           
  0001801DE3D9  7413                       je 0x1801de3ee                           -> 0x1801DE3EE (.text)
  0001801DE3DB  4889BBF8020000             mov qword ptr [rbx + 0x2f8], rdi      
  0001801DE3E2  488D8B98020000             lea rcx, [rbx + 0x298]                
  0001801DE3E9  E832D6FDFF                 call 0x1801bba20                         -> 0x1801BBA20 (.text)
  0001801DE3EE  488B7C2430                 mov rdi, qword ptr [rsp + 0x30]       
  0001801DE3F3  C6436000                   mov byte ptr [rbx + 0x60], 0          
  0001801DE3F7  488B5C2438                 mov rbx, qword ptr [rsp + 0x38]       
  0001801DE3FC  4883C420                   add rsp, 0x20                         
  0001801DE400  5E                         pop rsi                               
  0001801DE401  C3                         ret                                   
  0001801DE402  488BCB                     mov rcx, rbx                          
  0001801DE405  E8D6D6FDFF                 call 0x1801bbae0                         -> 0x1801BBAE0 (.text)
  0001801DE40A  488D8B40020000             lea rcx, [rbx + 0x240]                
  0001801DE411  E80AD6FDFF                 call 0x1801bba20                         -> 0x1801BBA20 (.text)
  0001801DE416  488D8B98020000             lea rcx, [rbx + 0x298]                
  0001801DE41D  E8FED5FDFF                 call 0x1801bba20                         -> 0x1801BBA20 (.text)
  0001801DE422  C683F002000001             mov byte ptr [rbx + 0x2f0], 1         
  0001801DE429  488B7C2430                 mov rdi, qword ptr [rsp + 0x30]       
  0001801DE42E  488B5C2438                 mov rbx, qword ptr [rsp + 0x38]       
  0001801DE433  4883C420                   add rsp, 0x20                         
  0001801DE437  5E                         pop rsi                               
  0001801DE438  C3                         ret                                   
