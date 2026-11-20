; menumain_creneau3.asm  --  TaskMenuMain creneau [3]  (ROLE INCONNU)
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801DE7B0 - 0x1801DE939  (393 octets)
;
; A QUOI : Creneau [3] de la vtable TaskMenuMain 0x180532AE8, 393 o. Le sens de ce creneau n'est PAS etabli : mode_de_jeu.md section 5 l'ecrit << [3] = ? >>. Son jumeau de REVO est 0x18020A5B0 (617 o), qui n'a pas de .c non plus. Depose pour qu'on puisse le lire.
;
; D'OU VIENT LE NOM : RTTI : vtable 0x180532AE8 creneau [3] ; VF5RE/analysis/mode_de_jeu.md section 5 (qui dit ne pas savoir)
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
  0001801DE7B0  4053                       push rbx                              
  0001801DE7B2  4883EC20                   sub rsp, 0x20                         
  0001801DE7B6  488BD9                     mov rbx, rcx                          
  0001801DE7B9  488B0D30CFA500             mov rcx, qword ptr [rip + 0xa5cf30]      ; -> 0x180C3B6F0
  0001801DE7C0  4885C9                     test rcx, rcx                         
  0001801DE7C3  0F84D0000000               je 0x1801de899                           -> 0x1801DE899 (.text)
  0001801DE7C9  4883B910FE010000           cmp qword ptr [rcx + 0x1fe10], 0      
  0001801DE7D1  0F84C2000000               je 0x1801de899                           -> 0x1801DE899 (.text)
  0001801DE7D7  488B8110FE0100             mov rax, qword ptr [rcx + 0x1fe10]    
  0001801DE7DE  4885C0                     test rax, rax                         
  0001801DE7E1  0F84AA000000               je 0x1801de891                           -> 0x1801DE891 (.text)
  0001801DE7E7  488B8918FE0100             mov rcx, qword ptr [rcx + 0x1fe18]    
  0001801DE7EE  4533C0                     xor r8d, r8d                          
  0001801DE7F1  418D504C                   lea edx, [r8 + 0x4c]                  
  0001801DE7F5  FFD0                       call rax                              
  0001801DE7F7  83F801                     cmp eax, 1                            
  0001801DE7FA  0F8591000000               jne 0x1801de891                          -> 0x1801DE891 (.text)
  0001801DE800  80BB092A000000             cmp byte ptr [rbx + 0x2a09], 0        
  0001801DE807  750C                       jne 0x1801de815                          -> 0x1801DE815 (.text)
  0001801DE809  488D8B002A0000             lea rcx, [rbx + 0x2a00]               
  0001801DE810  E84BFDFFFF                 call 0x1801de560                         -> 0x1801DE560 (.text)
  0001801DE815  488B0DD4B72200             mov rcx, qword ptr [rip + 0x22b7d4]      ; -> 0x180409FF0
  0001801DE81C  E82F8BFBFF                 call 0x180197350                         -> 0x180197350 (.text)
  0001801DE821  84C0                       test al, al                           
  0001801DE823  756C                       jne 0x1801de891                          -> 0x1801DE891 (.text)
  0001801DE825  488B0DC4B72200             mov rcx, qword ptr [rip + 0x22b7c4]      ; -> 0x180409FF0
  0001801DE82C  E89F8BFBFF                 call 0x1801973d0                         -> 0x1801973D0 (.text)
  0001801DE831  488B0DB8B72200             mov rcx, qword ptr [rip + 0x22b7b8]      ; -> 0x180409FF0
  0001801DE838  E8B38BFBFF                 call 0x1801973f0                         -> 0x1801973F0 (.text)
  0001801DE83D  4533C0                     xor r8d, r8d                          
  0001801DE840  488D15E98BE2FF             lea rdx, [rip - 0x1d7417]                ; -> 0x180007430
  0001801DE847  418D4849                   lea ecx, [r8 + 0x49]                  
  0001801DE84B  E8D08BEAFF                 call 0x180087420                         -> 0x180087420 (.text)
  0001801DE850  4533C0                     xor r8d, r8d                          
  0001801DE853  488D1516420000             lea rdx, [rip + 0x4216]                  ; -> 0x1801E2A70
  0001801DE85A  418D484A                   lea ecx, [r8 + 0x4a]                  
  0001801DE85E  E8BD8BEAFF                 call 0x180087420                         -> 0x180087420 (.text)
  0001801DE863  4533C0                     xor r8d, r8d                          
  0001801DE866  488D15C38BE2FF             lea rdx, [rip - 0x1d743d]                ; -> 0x180007430
  0001801DE86D  418D484B                   lea ecx, [r8 + 0x4b]                  
  0001801DE871  E8AA8BEAFF                 call 0x180087420                         -> 0x180087420 (.text)
  0001801DE876  4533C0                     xor r8d, r8d                          
  0001801DE879  488D15F0410000             lea rdx, [rip + 0x41f0]                  ; -> 0x1801E2A70
  0001801DE880  418D484C                   lea ecx, [r8 + 0x4c]                  
  0001801DE884  E8978BEAFF                 call 0x180087420                         -> 0x180087420 (.text)
  0001801DE889  B001                       mov al, 1                             
  0001801DE88B  4883C420                   add rsp, 0x20                         
  0001801DE88F  5B                         pop rbx                               
  0001801DE890  C3                         ret                                   
  0001801DE891  32C0                       xor al, al                            
  0001801DE893  4883C420                   add rsp, 0x20                         
  0001801DE897  5B                         pop rbx                               
  0001801DE898  C3                         ret                                   
  0001801DE899  488BCB                     mov rcx, rbx                          
  0001801DE89C  E80FD8FDFF                 call 0x1801bc0b0                         -> 0x1801BC0B0 (.text)
  0001801DE8A1  488D8B40020000             lea rcx, [rbx + 0x240]                
  0001801DE8A8  E8B3D7FDFF                 call 0x1801bc060                         -> 0x1801BC060 (.text)
  0001801DE8AD  488D8B98020000             lea rcx, [rbx + 0x298]                
  0001801DE8B4  E8A7D7FDFF                 call 0x1801bc060                         -> 0x1801BC060 (.text)
  0001801DE8B9  488D8BF0020000             lea rcx, [rbx + 0x2f0]                
  0001801DE8C0  E89BD7FDFF                 call 0x1801bc060                         -> 0x1801BC060 (.text)
  0001801DE8C5  488D8B48030000             lea rcx, [rbx + 0x348]                
  0001801DE8CC  E8CF670600                 call 0x1802450a0                         -> 0x1802450A0 (.text)
  0001801DE8D1  488D8BC0040000             lea rcx, [rbx + 0x4c0]                
  0001801DE8D8  E8C3670600                 call 0x1802450a0                         -> 0x1802450A0 (.text)
  0001801DE8DD  8B8B38060000               mov ecx, dword ptr [rbx + 0x638]      
  0001801DE8E3  85C9                       test ecx, ecx                         
  0001801DE8E5  740F                       je 0x1801de8f6                           -> 0x1801DE8F6 (.text)
  0001801DE8E7  E8F4B2E4FF                 call 0x180029be0                         -> 0x180029BE0 (.text)
  0001801DE8EC  C7833806000000000000       mov dword ptr [rbx + 0x638], 0        
  0001801DE8F6  4883BB5006000000           cmp qword ptr [rbx + 0x650], 0        
  0001801DE8FE  742A                       je 0x1801de92a                           -> 0x1801DE92A (.text)
  0001801DE900  8B4358                     mov eax, dword ptr [rbx + 0x58]       
  0001801DE903  83F805                     cmp eax, 5                            
  0001801DE906  7516                       jne 0x1801de91e                          -> 0x1801DE91E (.text)
  0001801DE908  C6833D06000001             mov byte ptr [rbx + 0x63d], 1         
  0001801DE90F  B001                       mov al, 1                             
  0001801DE911  C6833F06000000             mov byte ptr [rbx + 0x63f], 0         
  0001801DE918  4883C420                   add rsp, 0x20                         
  0001801DE91C  5B                         pop rbx                               
  0001801DE91D  C3                         ret                                   
  0001801DE91E  83F807                     cmp eax, 7                            
  0001801DE921  7507                       jne 0x1801de92a                          -> 0x1801DE92A (.text)
  0001801DE923  C6833E06000001             mov byte ptr [rbx + 0x63e], 1         
  0001801DE92A  C6833F06000000             mov byte ptr [rbx + 0x63f], 0         
  0001801DE931  B001                       mov al, 1                             
  0001801DE933  4883C420                   add rsp, 0x20                         
  0001801DE937  5B                         pop rbx                               
  0001801DE938  C3                         ret                                   
