; etat_repartiteur_3_phases.asm  --  Etat_RepartiteurDesPhases
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1800DA550 - 0x1800DA7D4  (644 octets)   [6 entrees .pdata chainees]
;
; A QUOI : LE repartiteur de la machine a etats : il lit la tete courante en 0x18070C4F0 et appelle, selon la phase, l'un des trois gestionnaires du descripteur -- table des modes 0x1803A0190 (10 entrees de 0x68), table des sous-etats 0x1803A05A0 (55 entrees de 0x20).
;
; D'OU VIENT LE NOM : VF5RE/analysis/machine_console.md, section 1
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
  0001800DA550  4056                       push rsi                              
  0001800DA552  4883EC20                   sub rsp, 0x20                         
  0001800DA556  488B0D23C72600             mov rcx, qword ptr [rip + 0x26c723]      ; -> 0x180346C80
  0001800DA55D  E8DECEF2FF                 call 0x180007440                         -> 0x180007440 (.text)
  0001800DA562  85C0                       test eax, eax                         
  0001800DA564  7407                       je 0x1800da56d                           -> 0x1800DA56D (.text)
  0001800DA566  8BC8                       mov ecx, eax                          
  0001800DA568  E8C3CEF2FF                 call 0x180007430                         -> 0x180007430 (.text)
  0001800DA56D  803D8C1F630000             cmp byte ptr [rip + 0x631f8c], 0         ; -> 0x18070C500
  0001800DA574  BE02000000                 mov esi, 2                            
  0001800DA579  7439                       je 0x1800da5b4                           -> 0x1800DA5B4 (.text)
  0001800DA57B  803D7F1F630000             cmp byte ptr [rip + 0x631f7f], 0         ; -> 0x18070C501
  0001800DA582  746D                       je 0x1800da5f1                           -> 0x1800DA5F1 (.text)
  0001800DA584  803D921F630000             cmp byte ptr [rip + 0x631f92], 0         ; -> 0x18070C51D
  0001800DA58B  7464                       je 0x1800da5f1                           -> 0x1800DA5F1 (.text)
  0001800DA58D  E88EA91600                 call 0x180244f20                         -> 0x180244F20 (.text)
  0001800DA592  84C0                       test al, al                           
  0001800DA594  0F852E020000               jne 0x1800da7c8                          -> 0x1800DA7C8 (.text)
  0001800DA59A  38057C1F6300               cmp byte ptr [rip + 0x631f7c], al        ; -> 0x18070C51C
  0001800DA5A0  BA37000000                 mov edx, 0x37                         
  0001800DA5A5  8B0D491F6300               mov ecx, dword ptr [rip + 0x631f49]      ; -> 0x18070C4F4
  0001800DA5AB  0F45155E1F6300             cmovne edx, dword ptr [rip + 0x631f5e]   ; -> 0x18070C510
  0001800DA5B2  EB2A                       jmp 0x1800da5de                          -> 0x1800DA5DE (.text)
  0001800DA5B4  803D611F630000             cmp byte ptr [rip + 0x631f61], 0         ; -> 0x18070C51C
  0001800DA5BB  7455                       je 0x1800da612                           -> 0x1800DA612 (.text)
  0001800DA5BD  803D591F630000             cmp byte ptr [rip + 0x631f59], 0         ; -> 0x18070C51D
  0001800DA5C4  744C                       je 0x1800da612                           -> 0x1800DA612 (.text)
  0001800DA5C6  E855A91600                 call 0x180244f20                         -> 0x180244F20 (.text)
  0001800DA5CB  84C0                       test al, al                           
  0001800DA5CD  0F85F5010000               jne 0x1800da7c8                          -> 0x1800DA7C8 (.text)
  0001800DA5D3  8B15371F6300               mov edx, dword ptr [rip + 0x631f37]      ; -> 0x18070C510
  0001800DA5D9  B90A000000                 mov ecx, 0xa                          
  0001800DA5DE  E81D020000                 call 0x1800da800                         -> 0x1800DA800 (.text)
  0001800DA5E3  C605331F630000             mov byte ptr [rip + 0x631f33], 0         ; -> 0x18070C51D
  0001800DA5EA  C605101F630000             mov byte ptr [rip + 0x631f10], 0         ; -> 0x18070C501
  0001800DA5F1  803D081F630000             cmp byte ptr [rip + 0x631f08], 0         ; -> 0x18070C500
  0001800DA5F8  8B0DFE1E6300               mov ecx, dword ptr [rip + 0x631efe]      ; -> 0x18070C4FC
  0001800DA5FE  7418                       je 0x1800da618                           -> 0x1800DA618 (.text)
  0001800DA600  803D161F630000             cmp byte ptr [rip + 0x631f16], 0         ; -> 0x18070C51D
  0001800DA607  0F45CE                     cmovne ecx, esi                       
  0001800DA60A  890DEC1E6300               mov dword ptr [rip + 0x631eec], ecx      ; -> 0x18070C4FC
  0001800DA610  EB06                       jmp 0x1800da618                          -> 0x1800DA618 (.text)
  0001800DA612  8B0DE41E6300               mov ecx, dword ptr [rip + 0x631ee4]      ; -> 0x18070C4FC
  0001800DA618  448B05D11E6300             mov r8d, dword ptr [rip + 0x631ed1]      ; -> 0x18070C4F0
  0001800DA61F  4C8D0D6A5B2C00             lea r9, [rip + 0x2c5b6a]                 ; -> 0x1803A0190
  0001800DA626  48895C2430                 mov qword ptr [rsp + 0x30], rbx       
  0001800DA62B  33DB                       xor ebx, ebx                          
  0001800DA62D  8BD3                       mov edx, ebx                          
  0001800DA62F  8BC3                       mov eax, ebx                          
  0001800DA631  46390408                   cmp dword ptr [rax + r9], r8d         
  0001800DA635  7420                       je 0x1800da657                           -> 0x1800DA657 (.text)
  0001800DA637  48FFC2                     inc rdx                               
  0001800DA63A  4883C068                   add rax, 0x68                         
  0001800DA63E  483D10040000               cmp rax, 0x410                        
  0001800DA644  72EB                       jb 0x1800da631                           -> 0x1800DA631 (.text)
  0001800DA646  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001800DA64B  FF05B31E6300               inc dword ptr [rip + 0x631eb3]           ; -> 0x18070C504
  0001800DA651  4883C420                   add rsp, 0x20                         
  0001800DA655  5E                         pop rsi                               
  0001800DA656  C3                         ret                                   
  0001800DA657  4C6BC268                   imul r8, rdx, 0x68                    
  0001800DA65B  4D03C1                     add r8, r9                            
  0001800DA65E  0F845F010000               je 0x1800da7c3                           -> 0x1800DA7C3 (.text)
  0001800DA664  83F901                     cmp ecx, 1                            
  0001800DA667  4863C1                     movsxd rax, ecx                       
  0001800DA66A  0F95C2                     setne dl                              
  0001800DA66D  4D8B4CC008                 mov r9, qword ptr [r8 + rax*8 + 8]    
  0001800DA672  4D85C9                     test r9, r9                           
  0001800DA675  740C                       je 0x1800da683                           -> 0x1800DA683 (.text)
  0001800DA677  41FFD1                     call r9                               
  0001800DA67A  8B0D7C1E6300               mov ecx, dword ptr [rip + 0x631e7c]      ; -> 0x18070C4FC
  0001800DA680  0FB6D0                     movzx edx, al                         
  0001800DA683  84D2                       test dl, dl                           
  0001800DA685  7441                       je 0x1800da6c8                           -> 0x1800DA6C8 (.text)
  0001800DA687  8BD1                       mov edx, ecx                          
  0001800DA689  85C9                       test ecx, ecx                         
  0001800DA68B  742F                       je 0x1800da6bc                           -> 0x1800DA6BC (.text)
  0001800DA68D  83EA01                     sub edx, 1                            
  0001800DA690  7422                       je 0x1800da6b4                           -> 0x1800DA6B4 (.text)
  0001800DA692  83FA01                     cmp edx, 1                            
  0001800DA695  7531                       jne 0x1800da6c8                          -> 0x1800DA6C8 (.text)
  0001800DA697  381D631E6300               cmp byte ptr [rip + 0x631e63], bl        ; -> 0x18070C500
  0001800DA69D  750C                       jne 0x1800da6ab                          -> 0x1800DA6AB (.text)
  0001800DA69F  88155B1E6300               mov byte ptr [rip + 0x631e5b], dl        ; -> 0x18070C500
  0001800DA6A5  8815711E6300               mov byte ptr [rip + 0x631e71], dl        ; -> 0x18070C51C
  0001800DA6AB  C6054F1E630001             mov byte ptr [rip + 0x631e4f], 1         ; -> 0x18070C501
  0001800DA6B2  EB1C                       jmp 0x1800da6d0                          -> 0x1800DA6D0 (.text)
  0001800DA6B4  8935421E6300               mov dword ptr [rip + 0x631e42], esi      ; -> 0x18070C4FC
  0001800DA6BA  EB14                       jmp 0x1800da6d0                          -> 0x1800DA6D0 (.text)
  0001800DA6BC  C705361E630001000000       mov dword ptr [rip + 0x631e36], 1        ; -> 0x18070C4FC
  0001800DA6C6  EB08                       jmp 0x1800da6d0                          -> 0x1800DA6D0 (.text)
  0001800DA6C8  85C9                       test ecx, ecx                         
  0001800DA6CA  0F84F3000000               je 0x1800da7c3                           -> 0x1800DA7C3 (.text)
  0001800DA6D0  381D471E6300               cmp byte ptr [rip + 0x631e47], bl        ; -> 0x18070C51D
  0001800DA6D6  0F85E7000000               jne 0x1800da7c3                          -> 0x1800DA7C3 (.text)
  0001800DA6DC  381D1E1E6300               cmp byte ptr [rip + 0x631e1e], bl        ; -> 0x18070C500
  0001800DA6E2  48897C2438                 mov qword ptr [rsp + 0x38], rdi       
  0001800DA6E7  7510                       jne 0x1800da6f9                          -> 0x1800DA6F9 (.text)
  0001800DA6E9  381D2D1E6300               cmp byte ptr [rip + 0x631e2d], bl        ; -> 0x18070C51C
  0001800DA6EF  7508                       jne 0x1800da6f9                          -> 0x1800DA6F9 (.text)
  0001800DA6F1  8B0D211E6300               mov ecx, dword ptr [rip + 0x631e21]      ; -> 0x18070C518
  0001800DA6F7  EB08                       jmp 0x1800da701                          -> 0x1800DA701 (.text)
  0001800DA6F9  8BCE                       mov ecx, esi                          
  0001800DA6FB  890D171E6300               mov dword ptr [rip + 0x631e17], ecx      ; -> 0x18070C518
  0001800DA701  8B15051E6300               mov edx, dword ptr [rip + 0x631e05]      ; -> 0x18070C50C
  0001800DA707  4C8D05925E2C00             lea r8, [rip + 0x2c5e92]                 ; -> 0x1803A05A0
  0001800DA70E  498BC0                     mov rax, r8                           
  0001800DA711  4032FF                     xor dil, dil                          
  0001800DA714  3910                       cmp dword ptr [rax], edx              
  0001800DA716  740F                       je 0x1800da727                           -> 0x1800DA727 (.text)
  0001800DA718  48FFC3                     inc rbx                               
  0001800DA71B  4883C020                   add rax, 0x20                         
  0001800DA71F  4883FB37                   cmp rbx, 0x37                         
  0001800DA723  72EF                       jb 0x1800da714                           -> 0x1800DA714 (.text)
  0001800DA725  EB52                       jmp 0x1800da779                          -> 0x1800DA779 (.text)
  0001800DA727  48C1E305                   shl rbx, 5                            
  0001800DA72B  4903D8                     add rbx, r8                           
  0001800DA72E  7449                       je 0x1800da779                           -> 0x1800DA779 (.text)
  0001800DA730  83F903                     cmp ecx, 3                            
  0001800DA733  7419                       je 0x1800da74e                           -> 0x1800DA74E (.text)
  0001800DA735  4863C1                     movsxd rax, ecx                       
  0001800DA738  488B54C308                 mov rdx, qword ptr [rbx + rax*8 + 8]  
  0001800DA73D  4885D2                     test rdx, rdx                         
  0001800DA740  740C                       je 0x1800da74e                           -> 0x1800DA74E (.text)
  0001800DA742  FFD2                       call rdx                              
  0001800DA744  84C0                       test al, al                           
  0001800DA746  7431                       je 0x1800da779                           -> 0x1800DA779 (.text)
  0001800DA748  8B0DCA1D6300               mov ecx, dword ptr [rip + 0x631dca]      ; -> 0x18070C518
  0001800DA74E  85C9                       test ecx, ecx                         
  0001800DA750  741D                       je 0x1800da76f                           -> 0x1800DA76F (.text)
  0001800DA752  83E901                     sub ecx, 1                            
  0001800DA755  740A                       je 0x1800da761                           -> 0x1800DA761 (.text)
  0001800DA757  83F901                     cmp ecx, 1                            
  0001800DA75A  750B                       jne 0x1800da767                          -> 0x1800DA767 (.text)
  0001800DA75C  0FB6F9                     movzx edi, cl                         
  0001800DA75F  EB18                       jmp 0x1800da779                          -> 0x1800DA779 (.text)
  0001800DA761  8935B11D6300               mov dword ptr [rip + 0x631db1], esi      ; -> 0x18070C518
  0001800DA767  FF05B31D6300               inc dword ptr [rip + 0x631db3]           ; -> 0x18070C520
  0001800DA76D  EB4F                       jmp 0x1800da7be                          -> 0x1800DA7BE (.text)
  0001800DA76F  C7059F1D630001000000       mov dword ptr [rip + 0x631d9f], 1        ; -> 0x18070C518
  0001800DA779  FF05A11D6300               inc dword ptr [rip + 0x631da1]           ; -> 0x18070C520
  0001800DA77F  4084FF                     test dil, dil                         
  0001800DA782  743A                       je 0x1800da7be                           -> 0x1800DA7BE (.text)
  0001800DA784  803D751D630000             cmp byte ptr [rip + 0x631d75], 0         ; -> 0x18070C500
  0001800DA78B  752A                       jne 0x1800da7b7                          -> 0x1800DA7B7 (.text)
  0001800DA78D  803D881D630000             cmp byte ptr [rip + 0x631d88], 0         ; -> 0x18070C51C
  0001800DA794  7521                       jne 0x1800da7b7                          -> 0x1800DA7B7 (.text)
  0001800DA796  833D731D630037             cmp dword ptr [rip + 0x631d73], 0x37     ; -> 0x18070C510
  0001800DA79D  C605781D630001             mov byte ptr [rip + 0x631d78], 1         ; -> 0x18070C51C
  0001800DA7A4  7511                       jne 0x1800da7b7                          -> 0x1800DA7B7 (.text)
  0001800DA7A6  C605531D630001             mov byte ptr [rip + 0x631d53], 1         ; -> 0x18070C500
  0001800DA7AD  C705591D630037000000       mov dword ptr [rip + 0x631d59], 0x37     ; -> 0x18070C510
  0001800DA7B7  C6055F1D630001             mov byte ptr [rip + 0x631d5f], 1         ; -> 0x18070C51D
  0001800DA7BE  488B7C2438                 mov rdi, qword ptr [rsp + 0x38]       
  0001800DA7C3  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001800DA7C8  FF05361D6300               inc dword ptr [rip + 0x631d36]           ; -> 0x18070C504
  0001800DA7CE  4883C420                   add rsp, 0x20                         
  0001800DA7D2  5E                         pop rsi                               
  0001800DA7D3  C3                         ret                                   
