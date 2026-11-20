; texte_resolveur_libelle.asm  --  Texte_ResoudreUnLibelle
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801EFD10 - 0x1801EFDCA  (186 octets)
;
; A QUOI : Resout un identifiant de texte dans la table chargee en 0x180753900 (borne 0x5A0C = 23052 entrees), qui est string_array.farc du .par. Jumeau de FUN_1802316E0 cote REVO.
;
; D'OU VIENT LE NOM : VF5RE/analysis/menu_console.md, section 8.1
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
  0001801EFD10  4053                       push rbx                              
  0001801EFD12  4883EC30                   sub rsp, 0x30                         
  0001801EFD16  8BD9                       mov ebx, ecx                          
  0001801EFD18  488B0DD1B9A400             mov rcx, qword ptr [rip + 0xa4b9d1]      ; -> 0x180C3B6F0
  0001801EFD1F  4885C9                     test rcx, rcx                         
  0001801EFD22  7438                       je 0x1801efd5c                           -> 0x1801EFD5C (.text)
  0001801EFD24  4883B910FE010000           cmp qword ptr [rcx + 0x1fe10], 0      
  0001801EFD2C  742E                       je 0x1801efd5c                           -> 0x1801EFD5C (.text)
  0001801EFD2E  895C2420                   mov dword ptr [rsp + 0x20], ebx       
  0001801EFD32  488B8110FE0100             mov rax, qword ptr [rcx + 0x1fe10]    
  0001801EFD39  4885C0                     test rax, rax                         
  0001801EFD3C  7413                       je 0x1801efd51                           -> 0x1801EFD51 (.text)
  0001801EFD3E  488B8918FE0100             mov rcx, qword ptr [rcx + 0x1fe18]    
  0001801EFD45  4C8D442420                 lea r8, [rsp + 0x20]                  
  0001801EFD4A  BA74000000                 mov edx, 0x74                         
  0001801EFD4F  FFD0                       call rax                              
  0001801EFD51  488B442428                 mov rax, qword ptr [rsp + 0x28]       
  0001801EFD56  4883C430                   add rsp, 0x30                         
  0001801EFD5A  5B                         pop rbx                               
  0001801EFD5B  C3                         ret                                   
  0001801EFD5C  48833D9C3B560000           cmp qword ptr [rip + 0x563b9c], 0        ; -> 0x180753900
  0001801EFD64  7444                       je 0x1801efdaa                           -> 0x1801EFDAA (.text)
  0001801EFD66  81FB0C5A0000               cmp ebx, 0x5a0c                       
  0001801EFD6C  733C                       jae 0x1801efdaa                          -> 0x1801EFDAA (.text)
  0001801EFD6E  E83DA2E3FF                 call 0x180029fb0                         -> 0x180029FB0 (.text)
  0001801EFD73  84C0                       test al, al                           
  0001801EFD75  7526                       jne 0x1801efd9d                          -> 0x1801EFD9D (.text)
  0001801EFD77  83FB31                     cmp ebx, 0x31                         
  0001801EFD7A  7321                       jae 0x1801efd9d                          -> 0x1801EFD9D (.text)
  0001801EFD7C  488B057D3B5600             mov rax, qword ptr [rip + 0x563b7d]      ; -> 0x180753900
  0001801EFD83  8D4B31                     lea ecx, [rbx + 0x31]                 
  0001801EFD86  488D1488                   lea rdx, [rax + rcx*4]                
  0001801EFD8A  48630A                     movsxd rcx, dword ptr [rdx]           
  0001801EFD8D  33C0                       xor eax, eax                          
  0001801EFD8F  85C9                       test ecx, ecx                         
  0001801EFD91  7431                       je 0x1801efdc4                           -> 0x1801EFDC4 (.text)
  0001801EFD93  488D040A                   lea rax, [rdx + rcx]                  
  0001801EFD97  4883C430                   add rsp, 0x30                         
  0001801EFD9B  5B                         pop rbx                               
  0001801EFD9C  C3                         ret                                   
  0001801EFD9D  488B055C3B5600             mov rax, qword ptr [rip + 0x563b5c]      ; -> 0x180753900
  0001801EFDA4  488D1498                   lea rdx, [rax + rbx*4]                
  0001801EFDA8  EBE0                       jmp 0x1801efd8a                          -> 0x1801EFD8A (.text)
  0001801EFDAA  8D83F3A5FFFF               lea eax, [rbx - 0x5a0d]               
  0001801EFDB0  83F821                     cmp eax, 0x21                         
  0001801EFDB3  770D                       ja 0x1801efdc2                           -> 0x1801EFDC2 (.text)
  0001801EFDB5  488D05C4483400             lea rax, [rip + 0x3448c4]                ; -> 0x180534680  "dummy"
  0001801EFDBC  4883C430                   add rsp, 0x30                         
  0001801EFDC0  5B                         pop rbx                               
  0001801EFDC1  C3                         ret                                   
  0001801EFDC2  33C0                       xor eax, eax                          
  0001801EFDC4  4883C430                   add rsp, 0x30                         
  0001801EFDC8  5B                         pop rbx                               
  0001801EFDC9  C3                         ret                                   
