; tache_detruire_par_objet.asm  --  Tache_DetruireParObjet
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1802450A0 - 0x180245125  (133 octets)   [3 entrees .pdata chainees]
;
; A QUOI : Le pendant : 0x1801DB870, corps du fn_sortie de MENU_MAIN, fait `mov rcx,[0x180753818] ; jmp ici`. C'est ce qui retire la tache du menu quand le sous-etat se termine.
;
; D'OU VIENT LE NOM : mesure du 2026-11-19, par le corps du fn_sortie de la ligne 36 de la table 0x1803A05A0
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
  0001802450A0  4057                       push rdi                              
  0001802450A2  4883EC20                   sub rsp, 0x20                         
  0001802450A6  488BF9                     mov rdi, rcx                          
  0001802450A9  E8E2FEFFFF                 call 0x180244f90                         -> 0x180244F90 (.text)
  0001802450AE  84C0                       test al, al                           
  0001802450B0  746B                       je 0x18024511d                           -> 0x18024511D (.text)
  0001802450B2  BA02000000                 mov edx, 2                            
  0001802450B7  488BCF                     mov rcx, rdi                          
  0001802450BA  E861FFFFFF                 call 0x180245020                         -> 0x180245020 (.text)
  0001802450BF  84C0                       test al, al                           
  0001802450C1  745A                       je 0x18024511d                           -> 0x18024511D (.text)
  0001802450C3  48895C2430                 mov qword ptr [rsp + 0x30], rbx       
  0001802450C8  4889742438                 mov qword ptr [rsp + 0x38], rsi       
  0001802450CD  488B356CC29F00             mov rsi, qword ptr [rip + 0x9fc26c]      ; -> 0x180C41340
  0001802450D4  488B06                     mov rax, qword ptr [rsi]              
  0001802450D7  488B18                     mov rbx, qword ptr [rax]              
  0001802450DA  483BD8                     cmp rbx, rax                          
  0001802450DD  741D                       je 0x1802450fc                           -> 0x1802450FC (.text)
  0001802450DF  90                         nop                                   
  0001802450E0  488B4B10                   mov rcx, qword ptr [rbx + 0x10]       
  0001802450E4  48397910                   cmp qword ptr [rcx + 0x10], rdi       
  0001802450E8  750A                       jne 0x1802450f4                          -> 0x1802450F4 (.text)
  0001802450EA  BA02000000                 mov edx, 2                            
  0001802450EF  E89C080000                 call 0x180245990                         -> 0x180245990 (.text)
  0001802450F4  488B1B                     mov rbx, qword ptr [rbx]              
  0001802450F7  483B1E                     cmp rbx, qword ptr [rsi]              
  0001802450FA  75E4                       jne 0x1802450e0                          -> 0x1802450E0 (.text)
  0001802450FC  488BCF                     mov rcx, rdi                          
  0001802450FF  C7472002000000             mov dword ptr [rdi + 0x20], 2         
  000180245106  E895090000                 call 0x180245aa0                         -> 0x180245AA0 (.text)
  00018024510B  488B742438                 mov rsi, qword ptr [rsp + 0x38]       
  000180245110  B001                       mov al, 1                             
  000180245112  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  000180245117  4883C420                   add rsp, 0x20                         
  00018024511B  5F                         pop rdi                               
  00018024511C  C3                         ret                                   
  00018024511D  32C0                       xor al, al                            
  00018024511F  4883C420                   add rsp, 0x20                         
  000180245123  5F                         pop rdi                               
  000180245124  C3                         ret                                   
