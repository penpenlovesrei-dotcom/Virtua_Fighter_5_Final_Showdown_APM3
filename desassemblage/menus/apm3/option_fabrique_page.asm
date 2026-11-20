; option_fabrique_page.asm  --  Option_OuvrirLaPage
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801AB3A0 - 0x1801AB427  (135 octets)
;
; A QUOI : 0x1801AB3A0(mode,type,drapeau) ouvre l'une ou l'autre de DEUX pages : type==2 et mode!=0 -> page 0x1807513C8 scene "OPTION CONTROL", sinon page 0x1807513C0 scene "OPTION". HUIT appelants, dont le menu console en 0x1801DE0D1 : l'ecran d'options est partage avec la pause et le terminal. Jumeau de FUN_1801BB3A0 cote REVO.
;
; D'OU VIENT LE NOM : VF5RE/analysis/carte_options.md, section 1
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
  0001801AB3A0  4883EC28                   sub rsp, 0x28                         
  0001801AB3A4  8BC1                       mov eax, ecx                          
  0001801AB3A6  83FA02                     cmp edx, 2                            
  0001801AB3A9  7533                       jne 0x1801ab3de                          -> 0x1801AB3DE (.text)
  0001801AB3AB  85C9                       test ecx, ecx                         
  0001801AB3AD  742F                       je 0x1801ab3de                           -> 0x1801AB3DE (.text)
  0001801AB3AF  488B0D12605A00             mov rcx, qword ptr [rip + 0x5a6012]      ; -> 0x1807513C8
  0001801AB3B6  8991C8030000               mov dword ptr [rcx + 0x3c8], edx      
  0001801AB3BC  488D151D5E2600             lea rdx, [rip + 0x265e1d]                ; -> 0x1804111E0  "OPTION CONTROL"
  0001801AB3C3  8981C4030000               mov dword ptr [rcx + 0x3c4], eax      
  0001801AB3C9  E862A40900                 call 0x180245830                         -> 0x180245830 (.text)
  0001801AB3CE  84C0                       test al, al                           
  0001801AB3D0  744E                       je 0x1801ab420                           -> 0x1801AB420 (.text)
  0001801AB3D2  488B05EF5F5A00             mov rax, qword ptr [rip + 0x5a5fef]      ; -> 0x1807513C8
  0001801AB3D9  4883C428                   add rsp, 0x28                         
  0001801AB3DD  C3                         ret                                   
  0001801AB3DE  488B0DDB5F5A00             mov rcx, qword ptr [rip + 0x5a5fdb]      ; -> 0x1807513C0
  0001801AB3E5  898160150000               mov dword ptr [rcx + 0x1560], eax     
  0001801AB3EB  8915C75F5A00               mov dword ptr [rip + 0x5a5fc7], edx      ; -> 0x1807513B8
  0001801AB3F1  4584C0                     test r8b, r8b                         
  0001801AB3F4  740E                       je 0x1801ab404                           -> 0x1801AB404 (.text)
  0001801AB3F6  33C0                       xor eax, eax                          
  0001801AB3F8  8981B8000000               mov dword ptr [rcx + 0xb8], eax       
  0001801AB3FE  898158030000               mov dword ptr [rcx + 0x358], eax      
  0001801AB404  488D15755F2600             lea rdx, [rip + 0x265f75]                ; -> 0x180411380  "OPTION"
  0001801AB40B  E820A40900                 call 0x180245830                         -> 0x180245830 (.text)
  0001801AB410  84C0                       test al, al                           
  0001801AB412  740C                       je 0x1801ab420                           -> 0x1801AB420 (.text)
  0001801AB414  488B05A55F5A00             mov rax, qword ptr [rip + 0x5a5fa5]      ; -> 0x1807513C0
  0001801AB41B  4883C428                   add rsp, 0x28                         
  0001801AB41F  C3                         ret                                   
  0001801AB420  33C0                       xor eax, eax                          
  0001801AB422  4883C428                   add rsp, 0x28                         
  0001801AB426  C3                         ret                                   
