; taskmenuversus_update.asm  --  TaskMenuVersus_Update
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1801DDB40 - 0x1801DDCFB  (443 octets)
;
; A QUOI : Pose le MODE DE JEU = 4 (Versus) en 0x1801DDC43.
;
; D'OU VIENT LE NOM : VF5RE/analysis/mode_de_jeu.md, section 1
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
  0001801DDB40  48895C2410                 mov qword ptr [rsp + 0x10], rbx       
  0001801DDB45  48896C2418                 mov qword ptr [rsp + 0x18], rbp       
  0001801DDB4A  4889742420                 mov qword ptr [rsp + 0x20], rsi       
  0001801DDB4F  57                         push rdi                              
  0001801DDB50  4883EC50                   sub rsp, 0x50                         
  0001801DDB54  488BF9                     mov rdi, rcx                          
  0001801DDB57  4032F6                     xor sil, sil                          
  0001801DDB5A  4881C158020000             add rcx, 0x258                        
  0001801DDB61  E8AADFFDFF                 call 0x1801bbb10                         -> 0x1801BBB10 (.text)
  0001801DDB66  488D8FB0020000             lea rcx, [rdi + 0x2b0]                
  0001801DDB6D  E89EDFFDFF                 call 0x1801bbb10                         -> 0x1801BBB10 (.text)
  0001801DDB72  33C9                       xor ecx, ecx                          
  0001801DDB74  E8175DFCFF                 call 0x1801a3890                         -> 0x1801A3890 (.text)
  0001801DDB79  BA0C5A0000                 mov edx, 0x5a0c                       
  0001801DDB7E  488BCF                     mov rcx, rdi                          
  0001801DDB81  E8FA0CFEFF                 call 0x1801be880                         -> 0x1801BE880 (.text)
  0001801DDB86  BA0C5A0000                 mov edx, 0x5a0c                       
  0001801DDB8B  488BCF                     mov rcx, rdi                          
  0001801DDB8E  E86D0CFEFF                 call 0x1801be800                         -> 0x1801BE800 (.text)
  0001801DDB93  488BCF                     mov rcx, rdi                          
  0001801DDB96  E835FEFDFF                 call 0x1801bd9d0                         -> 0x1801BD9D0 (.text)
  0001801DDB9B  84C0                       test al, al                           
  0001801DDB9D  0F85A8000000               jne 0x1801ddc4b                          -> 0x1801DDC4B (.text)
  0001801DDBA3  488D8F58020000             lea rcx, [rdi + 0x258]                
  0001801DDBAA  E811FEFDFF                 call 0x1801bd9c0                         -> 0x1801BD9C0 (.text)
  0001801DDBAF  84C0                       test al, al                           
  0001801DDBB1  0F8494000000               je 0x1801ddc4b                           -> 0x1801DDC4B (.text)
  0001801DDBB7  488D8FB0020000             lea rcx, [rdi + 0x2b0]                
  0001801DDBBE  E8FDFDFDFF                 call 0x1801bd9c0                         -> 0x1801BD9C0 (.text)
  0001801DDBC3  84C0                       test al, al                           
  0001801DDBC5  0F8480000000               je 0x1801ddc4b                           -> 0x1801DDC4B (.text)
  0001801DDBCB  40387760                   cmp byte ptr [rdi + 0x60], sil        
  0001801DDBCF  7477                       je 0x1801ddc48                           -> 0x1801DDC48 (.text)
  0001801DDBD1  4C638744020000             movsxd r8, dword ptr [rdi + 0x244]    
  0001801DDBD8  4C8D152124E2FF             lea r10, [rip - 0x1ddbdf]                ; -> 0x180000000
  0001801DDBDF  4863974C020000             movsxd rdx, dword ptr [rdi + 0x24c]   
  0001801DDBE6  48638F48020000             movsxd rcx, dword ptr [rdi + 0x248]   
  0001801DDBED  48638740020000             movsxd rax, dword ptr [rdi + 0x240]   
  0001801DDBF4  470FB68C10C8215300         movzx r9d, byte ptr [r8 + r10 + 0x5321c8]
  0001801DDBFD  450FB78452B8215300         movzx r8d, word ptr [r10 + rdx*2 + 0x5321b8]
  0001801DDC06  410FB7944AB8215300         movzx edx, word ptr [r10 + rcx*2 + 0x5321b8]
  0001801DDC0F  488D4C2460                 lea rcx, [rsp + 0x60]                 
  0001801DDC14  420FB68410C0215300         movzx eax, byte ptr [rax + r10 + 0x5321c0]
  0001801DDC1D  88442420                   mov byte ptr [rsp + 0x20], al         
  0001801DDC21  E8BADFFBFF                 call 0x18019bbe0                         -> 0x18019BBE0 (.text)
  0001801DDC26  83BF5002000000             cmp dword ptr [rdi + 0x250], 0        
  0001801DDC2D  0F9FC3                     setg bl                               
  0001801DDC30  E81B320300                 call 0x180210e50                         -> 0x180210E50 (.text)
  0001801DDC35  440FB6C3                   movzx r8d, bl                         
  0001801DDC39  488D542460                 lea rdx, [rsp + 0x60]                 
  0001801DDC3E  B904000000                 mov ecx, 4                            
  0001801DDC43  E8D8E8FBFF                 call 0x18019c520                         -> 0x18019C520 (.text)
  0001801DDC48  40B601                     mov sil, 1                            
  0001801DDC4B  80BF0803000000             cmp byte ptr [rdi + 0x308], 0         
  0001801DDC52  0F8580000000               jne 0x1801ddcd8                          -> 0x1801DDCD8 (.text)
  0001801DDC58  B901000000                 mov ecx, 1                            
  0001801DDC5D  E8CE46FCFF                 call 0x1801a2330                         -> 0x1801A2330 (.text)
  0001801DDC62  85C0                       test eax, eax                         
  0001801DDC64  0F99C1                     setns cl                              
  0001801DDC67  888F09030000               mov byte ptr [rdi + 0x309], cl        
  0001801DDC6D  85C0                       test eax, eax                         
  0001801DDC6F  7905                       jns 0x1801ddc76                          -> 0x1801DDC76 (.text)
  0001801DDC71  E8EA41FCFF                 call 0x1801a1e60                         -> 0x1801A1E60 (.text)
  0001801DDC76  488BCF                     mov rcx, rdi                          
  0001801DDC79  E862DFFDFF                 call 0x1801bbbe0                         -> 0x1801BBBE0 (.text)
  0001801DDC7E  80BF0903000000             cmp byte ptr [rdi + 0x309], 0         
  0001801DDC85  7437                       je 0x1801ddcbe                           -> 0x1801DDCBE (.text)
  0001801DDC87  48634758                   movsxd rax, dword ptr [rdi + 0x58]    
  0001801DDC8B  BB03000000                 mov ebx, 3                            
  0001801DDC90  C74424307B000000           mov dword ptr [rsp + 0x30], 0x7b      
  0001801DDC98  C74424347A000000           mov dword ptr [rsp + 0x34], 0x7a      
  0001801DDCA0  C744243883000000           mov dword ptr [rsp + 0x38], 0x83      
  0001801DDCA8  C744243C84000000           mov dword ptr [rsp + 0x3c], 0x84      
  0001801DDCB0  C744244085000000           mov dword ptr [rsp + 0x40], 0x85      
  0001801DDCB8  8B548430                   mov edx, dword ptr [rsp + rax*4 + 0x30]
  0001801DDCBC  EB08                       jmp 0x1801ddcc6                          -> 0x1801DDCC6 (.text)
  0001801DDCBE  BB06000000                 mov ebx, 6                            
  0001801DDCC3  8D537B                     lea edx, [rbx + 0x7b]                 
  0001801DDCC6  488BCF                     mov rcx, rdi                          
  0001801DDCC9  E8B20BFEFF                 call 0x1801be880                         -> 0x1801BE880 (.text)
  0001801DDCCE  8BD3                       mov edx, ebx                          
  0001801DDCD0  488BCF                     mov rcx, rdi                          
  0001801DDCD3  E8280BFEFF                 call 0x1801be800                         -> 0x1801BE800 (.text)
  0001801DDCD8  B902000000                 mov ecx, 2                            
  0001801DDCDD  E8AE5BFCFF                 call 0x1801a3890                         -> 0x1801A3890 (.text)
  0001801DDCE2  488B5C2468                 mov rbx, qword ptr [rsp + 0x68]       
  0001801DDCE7  400FB6C6                   movzx eax, sil                        
  0001801DDCEB  488B742478                 mov rsi, qword ptr [rsp + 0x78]       
  0001801DDCF0  488B6C2470                 mov rbp, qword ptr [rsp + 0x70]       
  0001801DDCF5  4883C450                   add rsp, 0x50                         
  0001801DDCF9  5F                         pop rdi                               
  0001801DDCFA  C3                         ret                                   
