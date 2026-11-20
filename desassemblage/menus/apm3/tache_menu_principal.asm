; tache_menu_principal.asm  --  TacheMenuPrincipal_Init
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801E36D0 - 0x1801E3E5E  (1934 octets)
;
; A QUOI : LA fonction qui monte le menu principal de la console : elle pose [page+0x224]=9 en 0x1801E39D0 (DERNIER INDICE, donc DIX entrees 0 a 9), porte le predicat de grisement en 0x1801E39FA, et en 0x1801E38ED la sequence temoin 0x5140C -> &page+0x29E8 -> commande 74. Jumelle probable de FUN_18020F1E0 cote REVO (NON apparie a l'octet).
;
; D'OU VIENT LE NOM : VF5RE/analysis/menu_console.md, section 8.3 ; VF5RE/desassemblages/apm3_menu_0x1E38ED.asm
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
  0001801E36D0  48895C2408                 mov qword ptr [rsp + 8], rbx          
  0001801E36D5  48896C2410                 mov qword ptr [rsp + 0x10], rbp       
  0001801E36DA  4889742418                 mov qword ptr [rsp + 0x18], rsi       
  0001801E36DF  57                         push rdi                              
  0001801E36E0  4156                       push r14                              
  0001801E36E2  4157                       push r15                              
  0001801E36E4  4881EC90000000             sub rsp, 0x90                         
  0001801E36EB  488BD9                     mov rbx, rcx                          
  0001801E36EE  E81D39FDFF                 call 0x1801b7010                         -> 0x1801B7010 (.text)
  0001801E36F3  84C0                       test al, al                           
  0001801E36F5  0F8444070000               je 0x1801e3e3f                           -> 0x1801E3E3F (.text)
  0001801E36FB  488B05EE7FA500             mov rax, qword ptr [rip + 0xa57fee]      ; -> 0x180C3B6F0
  0001801E3702  4885C0                     test rax, rax                         
  0001801E3705  0F8497020000               je 0x1801e39a2                           -> 0x1801E39A2 (.text)
  0001801E370B  4883B810FE010000           cmp qword ptr [rax + 0x1fe10], 0      
  0001801E3713  0F8489020000               je 0x1801e39a2                           -> 0x1801E39A2 (.text)
  0001801E3719  4533C9                     xor r9d, r9d                          
  0001801E371C  488D150D3DE2FF             lea rdx, [rip - 0x1dc2f3]                ; -> 0x180007430
  0001801E3723  4533C0                     xor r8d, r8d                          
  0001801E3726  418D4949                   lea ecx, [r9 + 0x49]                  
  0001801E372A  E8213EEAFF                 call 0x180087550                         -> 0x180087550 (.text)
  0001801E372F  4533C9                     xor r9d, r9d                          
  0001801E3732  488D1537F3FFFF             lea rdx, [rip - 0xcc9]                   ; -> 0x1801E2A70
  0001801E3739  4533C0                     xor r8d, r8d                          
  0001801E373C  418D494A                   lea ecx, [r9 + 0x4a]                  
  0001801E3740  E80B3EEAFF                 call 0x180087550                         -> 0x180087550 (.text)
  0001801E3745  4533C9                     xor r9d, r9d                          
  0001801E3748  488D15E13CE2FF             lea rdx, [rip - 0x1dc31f]                ; -> 0x180007430
  0001801E374F  4533C0                     xor r8d, r8d                          
  0001801E3752  418D494B                   lea ecx, [r9 + 0x4b]                  
  0001801E3756  E8F53DEAFF                 call 0x180087550                         -> 0x180087550 (.text)
  0001801E375B  4533C9                     xor r9d, r9d                          
  0001801E375E  488D150BF3FFFF             lea rdx, [rip - 0xcf5]                   ; -> 0x1801E2A70
  0001801E3765  4533C0                     xor r8d, r8d                          
  0001801E3768  418D494C                   lea ecx, [r9 + 0x4c]                  
  0001801E376C  E8DF3DEAFF                 call 0x180087550                         -> 0x180087550 (.text)
  0001801E3771  E83A68E4FF                 call 0x180029fb0                         -> 0x180029FB0 (.text)
  0001801E3776  33F6                       xor esi, esi                          
  0001801E3778  84C0                       test al, al                           
  0001801E377A  7576                       jne 0x1801e37f2                          -> 0x1801E37F2 (.text)
  0001801E377C  E88F52FDFF                 call 0x1801b8a10                         -> 0x1801B8A10 (.text)
  0001801E3781  80B8954F000002             cmp byte ptr [rax + 0x4f95], 2        
  0001801E3788  7207                       jb 0x1801e3791                           -> 0x1801E3791 (.text)
  0001801E378A  4088B0954F0000             mov byte ptr [rax + 0x4f95], sil      
  0001801E3791  E86A52FDFF                 call 0x1801b8a00                         -> 0x1801B8A00 (.text)
  0001801E3796  C5FC1000                   vmovups ymm0, ymmword ptr [rax]       
  0001801E379A  C5FC11442440               vmovups ymmword ptr [rsp + 0x40], ymm0
  0001801E37A0  C5FC104820                 vmovups ymm1, ymmword ptr [rax + 0x20]
  0001801E37A5  C5FC114C2460               vmovups ymmword ptr [rsp + 0x60], ymm1
  0001801E37AB  8B4040                     mov eax, dword ptr [rax + 0x40]       
  0001801E37AE  89842480000000             mov dword ptr [rsp + 0x80], eax       
  0001801E37B5  85C0                       test eax, eax                         
  0001801E37B7  7414                       je 0x1801e37cd                           -> 0x1801E37CD (.text)
  0001801E37B9  89B42480000000             mov dword ptr [rsp + 0x80], esi       
  0001801E37C0  488D4C2440                 lea rcx, [rsp + 0x40]                 
  0001801E37C5  C5F877                     vzeroupper                            
  0001801E37C8  E8D368FDFF                 call 0x1801ba0a0                         -> 0x1801BA0A0 (.text)
  0001801E37CD  C5F877                     vzeroupper                            
  0001801E37D0  E85B52FDFF                 call 0x1801b8a30                         -> 0x1801B8A30 (.text)
  0001801E37D5  C5FB1000                   vmovsd xmm0, qword ptr [rax]          
  0001801E37D9  C5FB11442430               vmovsd qword ptr [rsp + 0x30], xmm0   
  0001801E37DF  397008                     cmp dword ptr [rax + 8], esi          
  0001801E37E2  740E                       je 0x1801e37f2                           -> 0x1801E37F2 (.text)
  0001801E37E4  488D4C2430                 lea rcx, [rsp + 0x30]                 
  0001801E37E9  89742438                   mov dword ptr [rsp + 0x38], esi       
  0001801E37ED  E8DE68FDFF                 call 0x1801ba0d0                         -> 0x1801BA0D0 (.text)
  0001801E37F2  488B0DF77EA500             mov rcx, qword ptr [rip + 0xa57ef7]      ; -> 0x180C3B6F0
  0001801E37F9  4885C9                     test rcx, rcx                         
  0001801E37FC  7430                       je 0x1801e382e                           -> 0x1801E382E (.text)
  0001801E37FE  4839B110FE0100             cmp qword ptr [rcx + 0x1fe10], rsi    
  0001801E3805  7427                       je 0x1801e382e                           -> 0x1801E382E (.text)
  0001801E3807  C744243001000000           mov dword ptr [rsp + 0x30], 1         
  0001801E380F  488B8110FE0100             mov rax, qword ptr [rcx + 0x1fe10]    
  0001801E3816  4885C0                     test rax, rax                         
  0001801E3819  7413                       je 0x1801e382e                           -> 0x1801E382E (.text)
  0001801E381B  488B8918FE0100             mov rcx, qword ptr [rcx + 0x1fe18]    
  0001801E3822  4C8D442430                 lea r8, [rsp + 0x30]                  
  0001801E3827  BAA4000000                 mov edx, 0xa4                         
  0001801E382C  FFD0                       call rax                              
  0001801E382E  E87D42FDFF                 call 0x1801b7ab0                         -> 0x1801B7AB0 (.text)
  0001801E3833  84C0                       test al, al                           
  0001801E3835  7407                       je 0x1801e383e                           -> 0x1801E383E (.text)
  0001801E3837  C6833F06000001             mov byte ptr [rbx + 0x63f], 1         
  0001801E383E  E8DD43FDFF                 call 0x1801b7c20                         -> 0x1801B7C20 (.text)
  0001801E3843  E8E87EFDFF                 call 0x1801bb730                         -> 0x1801BB730 (.text)
  0001801E3848  488BC8                     mov rcx, rax                          
  0001801E384B  E8003CE2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801E3850  84C0                       test al, al                           
  0001801E3852  7407                       je 0x1801e385b                           -> 0x1801E385B (.text)
  0001801E3854  C6833F06000001             mov byte ptr [rbx + 0x63f], 1         
  0001801E385B  E8C051FDFF                 call 0x1801b8a20                         -> 0x1801B8A20 (.text)
  0001801E3860  488BF8                     mov rdi, rax                          
  0001801E3863  F6401E01                   test byte ptr [rax + 0x1e], 1         
  0001801E3867  743D                       je 0x1801e38a6                           -> 0x1801E38A6 (.text)
  0001801E3869  488B5760                   mov rdx, qword ptr [rdi + 0x60]       
  0001801E386D  B850000000                 mov eax, 0x50                         
  0001801E3872  48395730                   cmp qword ptr [rdi + 0x30], rdx       
  0001801E3876  B920000000                 mov ecx, 0x20                         
  0001801E387B  0F46C8                     cmovbe ecx, eax                       
  0001801E387E  4803CF                     add rcx, rdi                          
  0001801E3881  E86A2DFDFF                 call 0x1801b65f0                         -> 0x1801B65F0 (.text)
  0001801E3886  B9FEFF0000                 mov ecx, 0xfffe                       
  0001801E388B  66214F1E                   and word ptr [rdi + 0x1e], cx         
  0001801E388F  C6833F06000001             mov byte ptr [rbx + 0x63f], 1         
  0001801E3896  4885C0                     test rax, rax                         
  0001801E3899  740B                       je 0x1801e38a6                           -> 0x1801E38A6 (.text)
  0001801E389B  4883F801                   cmp rax, 1                            
  0001801E389F  0F95C0                     setne al                              
  0001801E38A2  FEC0                       inc al                                
  0001801E38A4  EB02                       jmp 0x1801e38a8                          -> 0x1801E38A8 (.text)
  0001801E38A6  33C0                       xor eax, eax                          
  0001801E38A8  8883142A0000               mov byte ptr [rbx + 0x2a14], al       
  0001801E38AE  4038B33F060000             cmp byte ptr [rbx + 0x63f], sil       
  0001801E38B5  740C                       je 0x1801e38c3                           -> 0x1801E38C3 (.text)
  0001801E38B7  BAFFFFFFFF                 mov edx, 0xffffffff                   
  0001801E38BC  B101                       mov cl, 1                             
  0001801E38BE  E89D40FDFF                 call 0x1801b7960                         -> 0x1801B7960 (.text)
  0001801E38C3  4088B33F060000             mov byte ptr [rbx + 0x63f], sil       
  0001801E38CA  4038B3FB290000             cmp byte ptr [rbx + 0x29fb], sil      
  0001801E38D1  7505                       jne 0x1801e38d8                          -> 0x1801E38D8 (.text)
  0001801E38D3  E8583BE2FF                 call 0x180007430                         -> 0x180007430 (.text)
  0001801E38D8  6689B3F8290000             mov word ptr [rbx + 0x29f8], si       
  0001801E38DF  4088B3FA290000             mov byte ptr [rbx + 0x29fa], sil      
  0001801E38E6  4088B3FC290000             mov byte ptr [rbx + 0x29fc], sil      
  0001801E38ED  C783E82900000C140500       mov dword ptr [rbx + 0x29e8], 0x5140c 
  0001801E38F7  6689B3EC290000             mov word ptr [rbx + 0x29ec], si       
  0001801E38FE  4088B3EE290000             mov byte ptr [rbx + 0x29ee], sil      
  0001801E3905  4889B3F0290000             mov qword ptr [rbx + 0x29f0], rsi     
  0001801E390C  4889B350060000             mov qword ptr [rbx + 0x650], rsi      
  0001801E3913  488B05D67DA500             mov rax, qword ptr [rip + 0xa57dd6]      ; -> 0x180C3B6F0
  0001801E391A  4885C0                     test rax, rax                         
  0001801E391D  0F841C050000               je 0x1801e3e3f                           -> 0x1801E3E3F (.text)
  0001801E3923  4839B010FE0100             cmp qword ptr [rax + 0x1fe10], rsi    
  0001801E392A  0F840F050000               je 0x1801e3e3f                           -> 0x1801E3E3F (.text)
  0001801E3930  488D8B002A0000             lea rcx, [rbx + 0x2a00]               
  0001801E3937  E844F5FFFF                 call 0x1801e2e80                         -> 0x1801E2E80 (.text)
  0001801E393C  4533C0                     xor r8d, r8d                          
  0001801E393F  488D156AF23400             lea rdx, [rip + 0x34f26a]                ; -> 0x180532BB0  "rom/sound/bgm/vfes_bgm_mnu.adx"
  0001801E3946  33C9                       xor ecx, ecx                          
  0001801E3948  E85324FAFF                 call 0x180185da0                         -> 0x180185DA0 (.text)
  0001801E394D  488B0D9C7DA500             mov rcx, qword ptr [rip + 0xa57d9c]      ; -> 0x180C3B6F0
  0001801E3954  488B8110FE0100             mov rax, qword ptr [rcx + 0x1fe10]    
  0001801E395B  4885C0                     test rax, rax                         
  0001801E395E  0F84DB040000               je 0x1801e3e3f                           -> 0x1801E3E3F (.text)
  0001801E3964  488B8918FE0100             mov rcx, qword ptr [rcx + 0x1fe18]    
  0001801E396B  4C8D83E8290000             lea r8, [rbx + 0x29e8]                
  0001801E3972  BA4A000000                 mov edx, 0x4a                         
  0001801E3977  FFD0                       call rax                              
  0001801E3979  83F801                     cmp eax, 1                            
  0001801E397C  0F85BD040000               jne 0x1801e3e3f                          -> 0x1801E3E3F (.text)
  0001801E3982  4038B3FB290000             cmp byte ptr [rbx + 0x29fb], sil      
  0001801E3989  0F84B0020000               je 0x1801e3c3f                           -> 0x1801E3C3F (.text)
  0001801E398F  488B0D5A662200             mov rcx, qword ptr [rip + 0x22665a]      ; -> 0x180409FF0
  0001801E3996  E8353AFBFF                 call 0x1801973d0                         -> 0x1801973D0 (.text)
  0001801E399B  B001                       mov al, 1                             
  0001801E399D  E99F040000                 jmp 0x1801e3e41                          -> 0x1801E3E41 (.text)
  0001801E39A2  B201                       mov dl, 1                             
  0001801E39A4  488BCB                     mov rcx, rbx                          
  0001801E39A7  E8B4AEFDFF                 call 0x1801be860                         -> 0x1801BE860 (.text)
  0001801E39AC  BA0A000000                 mov edx, 0xa                          
  0001801E39B1  488BCB                     mov rcx, rbx                          
  0001801E39B4  E8B7AEFDFF                 call 0x1801be870                         -> 0x1801BE870 (.text)
  0001801E39B9  B201                       mov dl, 1                             
  0001801E39BB  488BCB                     mov rcx, rbx                          
  0001801E39BE  E81DAEFDFF                 call 0x1801be7e0                         -> 0x1801BE7E0 (.text)
  0001801E39C3  488BCB                     mov rcx, rbx                          
  0001801E39C6  E85597FDFF                 call 0x1801bd120                         -> 0x1801BD120 (.text)
  0001801E39CB  B902000000                 mov ecx, 2                            
  0001801E39D0  C7832402000009000000       mov dword ptr [rbx + 0x224], 9        
  0001801E39DA  C6832802000000             mov byte ptr [rbx + 0x228], 0         
  0001801E39E1  E8AAFEFBFF                 call 0x1801a3890                         -> 0x1801A3890 (.text)
  0001801E39E6  48C7834206000000000000     mov qword ptr [rbx + 0x642], 0        
  0001801E39F1  66C7834A0600000000         mov word ptr [rbx + 0x64a], 0         
  0001801E39FA  E8513AE2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801E39FF  84C0                       test al, al                           
  0001801E3A01  7410                       je 0x1801e3a13                           -> 0x1801E3A13 (.text)
  0001801E3A03  C6834606000001             mov byte ptr [rbx + 0x646], 1         
  0001801E3A0A  66C783430600000101         mov word ptr [rbx + 0x643], 0x101     
  0001801E3A13  C6834B06000002             mov byte ptr [rbx + 0x64b], 2         
  0001801E3A1A  488D8B40020000             lea rcx, [rbx + 0x240]                
  0001801E3A21  C6834806000002             mov byte ptr [rbx + 0x648], 2         
  0001801E3A28  33F6                       xor esi, esi                          
  0001801E3A2A  89B338060000               mov dword ptr [rbx + 0x638], esi      
  0001801E3A30  E87B96FDFF                 call 0x1801bd0b0                         -> 0x1801BD0B0 (.text)
  0001801E3A35  488D8B98020000             lea rcx, [rbx + 0x298]                
  0001801E3A3C  E86F96FDFF                 call 0x1801bd0b0                         -> 0x1801BD0B0 (.text)
  0001801E3A41  488D8BF0020000             lea rcx, [rbx + 0x2f0]                
  0001801E3A48  E86396FDFF                 call 0x1801bd0b0                         -> 0x1801BD0B0 (.text)
  0001801E3A4D  4088B33C060000             mov byte ptr [rbx + 0x63c], sil       
  0001801E3A54  6689B340060000             mov word ptr [rbx + 0x640], si        
  0001801E3A5B  4038B33F060000             cmp byte ptr [rbx + 0x63f], sil       
  0001801E3A62  740A                       je 0x1801e3a6e                           -> 0x1801E3A6E (.text)
  0001801E3A64  8D56FF                     lea edx, [rsi - 1]                    
  0001801E3A67  B101                       mov cl, 1                             
  0001801E3A69  E8F23EFDFF                 call 0x1801b7960                         -> 0x1801B7960 (.text)
  0001801E3A6E  B9FFFFFFFF                 mov ecx, 0xffffffff                   
  0001801E3A73  4088B33F060000             mov byte ptr [rbx + 0x63f], sil       
  0001801E3A7A  4889B350060000             mov qword ptr [rbx + 0x650], rsi      
  0001801E3A81  40B501                     mov bpl, 1                            
  0001801E3A84  E8C739E2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801E3A89  84C0                       test al, al                           
  0001801E3A8B  7434                       je 0x1801e3ac1                           -> 0x1801E3AC1 (.text)
  0001801E3A8D  E8AE39E2FF                 call 0x180007440                         -> 0x180007440 (.text)
  0001801E3A92  8BC8                       mov ecx, eax                          
  0001801E3A94  E8B739E2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801E3A99  84C0                       test al, al                           
  0001801E3A9B  0F84D6010000               je 0x1801e3c77                           -> 0x1801E3C77 (.text)
  0001801E3AA1  E8AA39E2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801E3AA6  84C0                       test al, al                           
  0001801E3AA8  0F8426010000               je 0x1801e3bd4                           -> 0x1801E3BD4 (.text)
  0001801E3AAE  33D2                       xor edx, edx                          
  0001801E3AB0  33C9                       xor ecx, ecx                          
  0001801E3AB2  E80988FCFF                 call 0x1801ac2c0                         -> 0x1801AC2C0 (.text)
  0001801E3AB7  48898350060000             mov qword ptr [rbx + 0x650], rax      
  0001801E3ABE  4032ED                     xor bpl, bpl                          
  0001801E3AC1  488B0D28652200             mov rcx, qword ptr [rip + 0x226528]      ; -> 0x180409FF0
  0001801E3AC8  E80339FBFF                 call 0x1801973d0                         -> 0x1801973D0 (.text)
  0001801E3ACD  BA07000000                 mov edx, 7                            
  0001801E3AD2  488D8B40020000             lea rcx, [rbx + 0x240]                
  0001801E3AD9  E802AEFDFF                 call 0x1801be8e0                         -> 0x1801BE8E0 (.text)
  0001801E3ADE  BA2B000000                 mov edx, 0x2b                         
  0001801E3AE3  488D8B40020000             lea rcx, [rbx + 0x240]                
  0001801E3AEA  E8319FFDFF                 call 0x1801bda20                         -> 0x1801BDA20 (.text)
  0001801E3AEF  BA01000000                 mov edx, 1                            
  0001801E3AF4  488D8B98020000             lea rcx, [rbx + 0x298]                
  0001801E3AFB  E8E0ADFDFF                 call 0x1801be8e0                         -> 0x1801BE8E0 (.text)
  0001801E3B00  BA2A000000                 mov edx, 0x2a                         
  0001801E3B05  488D8B98020000             lea rcx, [rbx + 0x298]                
  0001801E3B0C  E80F9FFDFF                 call 0x1801bda20                         -> 0x1801BDA20 (.text)
  0001801E3B11  BA19000000                 mov edx, 0x19                         
  0001801E3B16  488D8BF0020000             lea rcx, [rbx + 0x2f0]                
  0001801E3B1D  E8BEADFDFF                 call 0x1801be8e0                         -> 0x1801BE8E0 (.text)
  0001801E3B22  BA2C000000                 mov edx, 0x2c                         
  0001801E3B27  488D8BF0020000             lea rcx, [rbx + 0x2f0]                
  0001801E3B2E  E8ED9EFDFF                 call 0x1801bda20                         -> 0x1801BDA20 (.text)
  0001801E3B33  488D05EEBB3400             lea rax, [rip + 0x34bbee]                ; -> 0x18052F728  "neu_e"
  0001801E3B3A  41B900000100               mov r9d, 0x10000                      
  0001801E3B40  4889442428                 mov qword ptr [rsp + 0x28], rax       
  0001801E3B45  488D15446C1B00             lea rdx, [rip + 0x1b6c44]                ; -> 0x18039A790  "bg_base"
  0001801E3B4C  488D0571BF2100             lea rax, [rip + 0x21bf71]                ; -> 0x1803FFAC4  "neu_s"
  0001801E3B53  41B801000000               mov r8d, 1                            
  0001801E3B59  B9A3020000                 mov ecx, 0x2a3                        
  0001801E3B5E  4889442420                 mov qword ptr [rsp + 0x20], rax       
  0001801E3B63  E8885FE4FF                 call 0x180029af0                         -> 0x180029AF0 (.text)
  0001801E3B68  898338060000               mov dword ptr [rbx + 0x638], eax      
  0001801E3B6E  4839B350060000             cmp qword ptr [rbx + 0x650], rsi      
  0001801E3B75  0F859F020000               jne 0x1801e3e1a                          -> 0x1801E3E1A (.text)
  0001801E3B7B  488B059EFC5600             mov rax, qword ptr [rip + 0x56fc9e]      ; -> 0x180753820
  0001801E3B82  40387060                   cmp byte ptr [rax + 0x60], sil        
  0001801E3B86  0F8418010000               je 0x1801e3ca4                           -> 0x1801E3CA4 (.text)
  0001801E3B8C  E8BF38E2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801E3B91  84C0                       test al, al                           
  0001801E3B93  0F84F1000000               je 0x1801e3c8a                           -> 0x1801E3C8A (.text)
  0001801E3B99  E8B238E2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801E3B9E  84C0                       test al, al                           
  0001801E3BA0  0F85E4000000               jne 0x1801e3c8a                          -> 0x1801E3C8A (.text)
  0001801E3BA6  488B0D73FC5600             mov rcx, qword ptr [rip + 0x56fc73]      ; -> 0x180753820
  0001801E3BAD  488D151CF03400             lea rdx, [rip + 0x34f01c]                ; -> 0x180532BD0  "MULTI MENU"
  0001801E3BB4  E8771C0600                 call 0x180245830                         -> 0x180245830 (.text)
  0001801E3BB9  84C0                       test al, al                           
  0001801E3BBB  0F8459020000               je 0x1801e3e1a                           -> 0x1801E3E1A (.text)
  0001801E3BC1  488B0558FC5600             mov rax, qword ptr [rip + 0x56fc58]      ; -> 0x180753820
  0001801E3BC8  48898350060000             mov qword ptr [rbx + 0x650], rax      
  0001801E3BCF  E946020000                 jmp 0x1801e3e1a                          -> 0x1801E3E1A (.text)
  0001801E3BD4  E87738E2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801E3BD9  84C0                       test al, al                           
  0001801E3BDB  7469                       je 0x1801e3c46                           -> 0x1801E3C46 (.text)
  0001801E3BDD  E86E38E2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801E3BE2  84C0                       test al, al                           
  0001801E3BE4  7560                       jne 0x1801e3c46                          -> 0x1801E3C46 (.text)
  0001801E3BE6  488B0533FC5600             mov rax, qword ptr [rip + 0x56fc33]      ; -> 0x180753820
  0001801E3BED  B907000000                 mov ecx, 7                            
  0001801E3BF2  C7405801000000             mov dword ptr [rax + 0x58], 1         
  0001801E3BF9  488B0520FC5600             mov rax, qword ptr [rip + 0x56fc20]      ; -> 0x180753820
  0001801E3C00  C6406001                   mov byte ptr [rax + 0x60], 1          
  0001801E3C04  E8976DEFFF                 call 0x1800da9a0                         -> 0x1800DA9A0 (.text)
  0001801E3C09  488B0D08FC5600             mov rcx, qword ptr [rip + 0x56fc08]      ; -> 0x180753818
  0001801E3C10  33D2                       xor edx, edx                          
  0001801E3C12  E8490D0000                 call 0x1801e4960                         -> 0x1801E4960 (.text)
  0001801E3C17  488B05FAFB5600             mov rax, qword ptr [rip + 0x56fbfa]      ; -> 0x180753818
  0001801E3C1E  C7405802000000             mov dword ptr [rax + 0x58], 2         
  0001801E3C25  488B05F4FB5600             mov rax, qword ptr [rip + 0x56fbf4]      ; -> 0x180753820
  0001801E3C2C  C6406001                   mov byte ptr [rax + 0x60], 1          
  0001801E3C30  488BCB                     mov rcx, rbx                          
  0001801E3C33  C6834106000001             mov byte ptr [rbx + 0x641], 1         
  0001801E3C3A  E861140600                 call 0x1802450a0                         -> 0x1802450A0 (.text)
  0001801E3C3F  B001                       mov al, 1                             
  0001801E3C41  E9FB010000                 jmp 0x1801e3e41                          -> 0x1801E3E41 (.text)
  0001801E3C46  E8E537E2FF                 call 0x180007430                         -> 0x180007430 (.text)
  0001801E3C4B  488B0DC6FB5600             mov rcx, qword ptr [rip + 0x56fbc6]      ; -> 0x180753818
  0001801E3C52  33D2                       xor edx, edx                          
  0001801E3C54  E8070D0000                 call 0x1801e4960                         -> 0x1801E4960 (.text)
  0001801E3C59  488B05B8FB5600             mov rax, qword ptr [rip + 0x56fbb8]      ; -> 0x180753818
  0001801E3C60  C7405802000000             mov dword ptr [rax + 0x58], 2         
  0001801E3C67  488B05B2FB5600             mov rax, qword ptr [rip + 0x56fbb2]      ; -> 0x180753820
  0001801E3C6E  C6406001                   mov byte ptr [rax + 0x60], 1          
  0001801E3C72  E94AFEFFFF                 jmp 0x1801e3ac1                          -> 0x1801E3AC1 (.text)
  0001801E3C77  33C9                       xor ecx, ecx                          
  0001801E3C79  E8226DEFFF                 call 0x1800da9a0                         -> 0x1800DA9A0 (.text)
  0001801E3C7E  B903000000                 mov ecx, 3                            
  0001801E3C83  E8386DEFFF                 call 0x1800da9c0                         -> 0x1800DA9C0 (.text)
  0001801E3C88  EBA6                       jmp 0x1801e3c30                          -> 0x1801E3C30 (.text)
  0001801E3C8A  488B058FFB5600             mov rax, qword ptr [rip + 0x56fb8f]      ; -> 0x180753820
  0001801E3C91  897058                     mov dword ptr [rax + 0x58], esi       
  0001801E3C94  40887060                   mov byte ptr [rax + 0x60], sil        
  0001801E3C98  4088B0F4020000             mov byte ptr [rax + 0x2f4], sil       
  0001801E3C9F  E976010000                 jmp 0x1801e3e1a                          -> 0x1801E3E1A (.text)
  0001801E3CA4  488DBB58060000             lea rdi, [rbx + 0x658]                
  0001801E3CAB  4038B3B8060000             cmp byte ptr [rbx + 0x6b8], sil       
  0001801E3CB2  0F8522010000               jne 0x1801e3dda                          -> 0x1801E3DDA (.text)
  0001801E3CB8  4038B3B8090000             cmp byte ptr [rbx + 0x9b8], sil       
  0001801E3CBF  0F8515010000               jne 0x1801e3dda                          -> 0x1801E3DDA (.text)
  0001801E3CC5  4038B3980E0000             cmp byte ptr [rbx + 0xe98], sil       
  0001801E3CCC  0F8508010000               jne 0x1801e3dda                          -> 0x1801E3DDA (.text)
  0001801E3CD2  4038B358110000             cmp byte ptr [rbx + 0x1158], sil      
  0001801E3CD9  0F85FB000000               jne 0x1801e3dda                          -> 0x1801E3DDA (.text)
  0001801E3CDF  E83C19FCFF                 call 0x1801a5620                         -> 0x1801A5620 (.text)
  0001801E3CE4  83F802                     cmp eax, 2                            
  0001801E3CE7  0F84ED000000               je 0x1801e3dda                           -> 0x1801E3DDA (.text)
  0001801E3CED  E86E19FCFF                 call 0x1801a5660                         -> 0x1801A5660 (.text)
  0001801E3CF2  83F802                     cmp eax, 2                            
  0001801E3CF5  0F84DF000000               je 0x1801e3dda                           -> 0x1801E3DDA (.text)
  0001801E3CFB  4038B3081A0000             cmp byte ptr [rbx + 0x1a08], sil      
  0001801E3D02  7413                       je 0x1801e3d17                           -> 0x1801E3D17 (.text)
  0001801E3D04  488DBBA8190000             lea rdi, [rbx + 0x19a8]               
  0001801E3D0B  488D15DEEE3400             lea rdx, [rip + 0x34eede]                ; -> 0x180532BF0  "VERSUS MENU"
  0001801E3D12  E9F0000000                 jmp 0x1801e3e07                          -> 0x1801E3E07 (.text)
  0001801E3D17  488DBBF01C0000             lea rdi, [rbx + 0x1cf0]               
  0001801E3D1E  4038B3501D0000             cmp byte ptr [rbx + 0x1d50], sil      
  0001801E3D25  0F8593000000               jne 0x1801e3dbe                          -> 0x1801E3DBE (.text)
  0001801E3D2B  4038B350200000             cmp byte ptr [rbx + 0x2050], sil      
  0001801E3D32  0F8586000000               jne 0x1801e3dbe                          -> 0x1801E3DBE (.text)
  0001801E3D38  E833B40200                 call 0x18020f170                         -> 0x18020F170 (.text)
  0001801E3D3D  84C0                       test al, al                           
  0001801E3D3F  757D                       jne 0x1801e3dbe                          -> 0x1801E3DBE (.text)
  0001801E3D41  488DBB28230000             lea rdi, [rbx + 0x2328]               
  0001801E3D48  4038B388230000             cmp byte ptr [rbx + 0x2388], sil      
  0001801E3D4F  7564                       jne 0x1801e3db5                          -> 0x1801E3DB5 (.text)
  0001801E3D51  E84AC0FEFF                 call 0x1801cfda0                         -> 0x1801CFDA0 (.text)
  0001801E3D56  83F802                     cmp eax, 2                            
  0001801E3D59  745A                       je 0x1801e3db5                           -> 0x1801E3DB5 (.text)
  0001801E3D5B  E8001FFEFF                 call 0x1801c5c60                         -> 0x1801C5C60 (.text)
  0001801E3D60  84C0                       test al, al                           
  0001801E3D62  7551                       jne 0x1801e3db5                          -> 0x1801E3DB5 (.text)
  0001801E3D64  4038B388260000             cmp byte ptr [rbx + 0x2688], sil      
  0001801E3D6B  7548                       jne 0x1801e3db5                          -> 0x1801E3DB5 (.text)
  0001801E3D6D  4038B31A290000             cmp byte ptr [rbx + 0x291a], sil      
  0001801E3D74  753F                       jne 0x1801e3db5                          -> 0x1801E3DB5 (.text)
  0001801E3D76  4038B33D060000             cmp byte ptr [rbx + 0x63d], sil       
  0001801E3D7D  7418                       je 0x1801e3d97                           -> 0x1801E3D97 (.text)
  0001801E3D7F  4533C0                     xor r8d, r8d                          
  0001801E3D82  33D2                       xor edx, edx                          
  0001801E3D84  33C9                       xor ecx, ecx                          
  0001801E3D86  E895C3FCFF                 call 0x1801b0120                         -> 0x1801B0120 (.text)
  0001801E3D8B  48898350060000             mov qword ptr [rbx + 0x650], rax      
  0001801E3D92  E983000000                 jmp 0x1801e3e1a                          -> 0x1801E3E1A (.text)
  0001801E3D97  4038B33E060000             cmp byte ptr [rbx + 0x63e], sil       
  0001801E3D9E  747A                       je 0x1801e3e1a                           -> 0x1801E3E1A (.text)
  0001801E3DA0  4533C0                     xor r8d, r8d                          
  0001801E3DA3  33D2                       xor edx, edx                          
  0001801E3DA5  33C9                       xor ecx, ecx                          
  0001801E3DA7  E8F475FCFF                 call 0x1801ab3a0                         -> 0x1801AB3A0 (.text)
  0001801E3DAC  48898350060000             mov qword ptr [rbx + 0x650], rax      
  0001801E3DB3  EB65                       jmp 0x1801e3e1a                          -> 0x1801E3E1A (.text)
  0001801E3DB5  488D1554EE3400             lea rdx, [rip + 0x34ee54]                ; -> 0x180532C10  "TERMINAL MENU"
  0001801E3DBC  EB49                       jmp 0x1801e3e07                          -> 0x1801E3E07 (.text)
  0001801E3DBE  E88D36E2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801E3DC3  488BCF                     mov rcx, rdi                          
  0001801E3DC6  84C0                       test al, al                           
  0001801E3DC8  7407                       je 0x1801e3dd1                           -> 0x1801E3DD1 (.text)
  0001801E3DCA  E8710C0000                 call 0x1801e4a40                         -> 0x1801E4A40 (.text)
  0001801E3DCF  EB1A                       jmp 0x1801e3deb                          -> 0x1801E3DEB (.text)
  0001801E3DD1  488D1528EE3400             lea rdx, [rip + 0x34ee28]                ; -> 0x180532C00  "TRAINING MENU"
  0001801E3DD8  EB30                       jmp 0x1801e3e0a                          -> 0x1801E3E0A (.text)
  0001801E3DDA  E87136E2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001801E3DDF  84C0                       test al, al                           
  0001801E3DE1  741D                       je 0x1801e3e00                           -> 0x1801E3E00 (.text)
  0001801E3DE3  488BCF                     mov rcx, rdi                          
  0001801E3DE6  E8F50A0000                 call 0x1801e48e0                         -> 0x1801E48E0 (.text)
  0001801E3DEB  33D2                       xor edx, edx                          
  0001801E3DED  33C9                       xor ecx, ecx                          
  0001801E3DEF  E8CC84FCFF                 call 0x1801ac2c0                         -> 0x1801AC2C0 (.text)
  0001801E3DF4  48898350060000             mov qword ptr [rbx + 0x650], rax      
  0001801E3DFB  4032ED                     xor bpl, bpl                          
  0001801E3DFE  EB1A                       jmp 0x1801e3e1a                          -> 0x1801E3E1A (.text)
  0001801E3E00  488D15D9ED3400             lea rdx, [rip + 0x34edd9]                ; -> 0x180532BE0  "ARCADE MENU"
  0001801E3E07  488BCF                     mov rcx, rdi                          
  0001801E3E0A  E8211A0600                 call 0x180245830                         -> 0x180245830 (.text)
  0001801E3E0F  84C0                       test al, al                           
  0001801E3E11  7407                       je 0x1801e3e1a                           -> 0x1801E3E1A (.text)
  0001801E3E13  4889BB50060000             mov qword ptr [rbx + 0x650], rdi      
  0001801E3E1A  6689B33D060000             mov word ptr [rbx + 0x63d], si        
  0001801E3E21  4084ED                     test bpl, bpl                         
  0001801E3E24  0F8415FEFFFF               je 0x1801e3c3f                           -> 0x1801E3C3F (.text)
  0001801E3E2A  4533C0                     xor r8d, r8d                          
  0001801E3E2D  488D15ECED3400             lea rdx, [rip + 0x34edec]                ; -> 0x180532C20  "rom/sound/bgm/vf5b_tkv.adx"
  0001801E3E34  33C9                       xor ecx, ecx                          
  0001801E3E36  E8651FFAFF                 call 0x180185da0                         -> 0x180185DA0 (.text)
  0001801E3E3B  B001                       mov al, 1                             
  0001801E3E3D  EB02                       jmp 0x1801e3e41                          -> 0x1801E3E41 (.text)
  0001801E3E3F  32C0                       xor al, al                            
  0001801E3E41  4C8D9C2490000000           lea r11, [rsp + 0x90]                 
  0001801E3E49  498B5B20                   mov rbx, qword ptr [r11 + 0x20]       
  0001801E3E4D  498B6B28                   mov rbp, qword ptr [r11 + 0x28]       
  0001801E3E51  498B7330                   mov rsi, qword ptr [r11 + 0x30]       
  0001801E3E55  498BE3                     mov rsp, r11                          
  0001801E3E58  415F                       pop r15                               
  0001801E3E5A  415E                       pop r14                               
  0001801E3E5C  5F                         pop rdi                               
  0001801E3E5D  C3                         ret                                   
