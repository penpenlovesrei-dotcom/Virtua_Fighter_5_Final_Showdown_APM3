; mode_selector_maj.asm  --  ModeSelector_MettreAJour
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1800DAE20 - 0x1800DB0F2  (722 octets)   [5 entrees .pdata chainees]
;
; A QUOI : Sous-etat 18 = MODE_SELECTOR, gestionnaire de MISE A JOUR (390 o). Jumeau cote REVO : 0x1800E2010, deja decompile sous le nom SE20_MODE_SELECTOR_Phase1_MontageDuMatch.c.
;
; D'OU VIENT LE NOM : VF5RE/analysis/mode_selector.md ; VF5RE/TABLE_DES_SCENES_APM3_VS_REVO.md section 6 (ligne 18)
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
  0001800DAE20  4053                       push rbx                              
  0001800DAE22  56                         push rsi                              
  0001800DAE23  57                         push rdi                              
  0001800DAE24  4154                       push r12                              
  0001800DAE26  4157                       push r15                              
  0001800DAE28  4883EC30                   sub rsp, 0x30                         
  0001800DAE2C  E86F75FDFF                 call 0x1800b23a0                         -> 0x1800B23A0 (.text)
  0001800DAE31  488BC8                     mov rcx, rax                          
  0001800DAE34  4C8BF8                     mov r15, rax                          
  0001800DAE37  E87475FDFF                 call 0x1800b23b0                         -> 0x1800B23B0 (.text)
  0001800DAE3C  498BCF                     mov rcx, r15                          
  0001800DAE3F  4C8BE0                     mov r12, rax                          
  0001800DAE42  E86976FDFF                 call 0x1800b24b0                         -> 0x1800B24B0 (.text)
  0001800DAE47  8B15E7975600               mov edx, dword ptr [rip + 0x5697e7]      ; -> 0x180644634
  0001800DAE4D  32DB                       xor bl, bl                            
  0001800DAE4F  488BF0                     mov rsi, rax                          
  0001800DAE52  488BB890100000             mov rdi, qword ptr [rax + 0x1090]     
  0001800DAE59  83EA01                     sub edx, 1                            
  0001800DAE5C  7429                       je 0x1800dae87                           -> 0x1800DAE87 (.text)
  0001800DAE5E  83EA01                     sub edx, 1                            
  0001800DAE61  0F848F000000               je 0x1800daef6                           -> 0x1800DAEF6 (.text)
  0001800DAE67  83FA01                     cmp edx, 1                            
  0001800DAE6A  0F840E010000               je 0x1800daf7e                           -> 0x1800DAF7E (.text)
  0001800DAE70  E8DBC5F2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001800DAE75  84C0                       test al, al                           
  0001800DAE77  0F8566020000               jne 0x1800db0e3                          -> 0x1800DB0E3 (.text)
  0001800DAE7D  C705AD97560001000000       mov dword ptr [rip + 0x5697ad], 1        ; -> 0x180644634
  0001800DAE87  33C9                       xor ecx, ecx                          
  0001800DAE89  E8C2C5F2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001800DAE8E  84C0                       test al, al                           
  0001800DAE90  0F854D020000               jne 0x1800db0e3                          -> 0x1800DB0E3 (.text)
  0001800DAE96  B901000000                 mov ecx, 1                            
  0001800DAE9B  E8B0C5F2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001800DAEA0  84C0                       test al, al                           
  0001800DAEA2  0F853B020000               jne 0x1800db0e3                          -> 0x1800DB0E3 (.text)
  0001800DAEA8  E8A3C5F2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001800DAEAD  84C0                       test al, al                           
  0001800DAEAF  0F852E020000               jne 0x1800db0e3                          -> 0x1800DB0E3 (.text)
  0001800DAEB5  E896C5F2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001800DAEBA  84C0                       test al, al                           
  0001800DAEBC  0F8521020000               jne 0x1800db0e3                          -> 0x1800DB0E3 (.text)
  0001800DAEC2  E889C5F2FF                 call 0x180007450                         -> 0x180007450 (.text)
  0001800DAEC7  84C0                       test al, al                           
  0001800DAEC9  0F8514020000               jne 0x1800db0e3                          -> 0x1800DB0E3 (.text)
  0001800DAECF  E84CE1FDFF                 call 0x1800b9020                         -> 0x1800B9020 (.text)
  0001800DAED4  84C0                       test al, al                           
  0001800DAED6  0F8507020000               jne 0x1800db0e3                          -> 0x1800DB0E3 (.text)
  0001800DAEDC  488BCE                     mov rcx, rsi                          
  0001800DAEDF  E86CC9FDFF                 call 0x1800b7850                         -> 0x1800B7850 (.text)
  0001800DAEE4  84C0                       test al, al                           
  0001800DAEE6  0F85F7010000               jne 0x1800db0e3                          -> 0x1800DB0E3 (.text)
  0001800DAEEC  C7053E97560002000000       mov dword ptr [rip + 0x56973e], 2        ; -> 0x180644634
  0001800DAEF6  33C9                       xor ecx, ecx                          
  0001800DAEF8  E843BE0A00                 call 0x180186d40                         -> 0x180186D40 (.text)
  0001800DAEFD  4885FF                     test rdi, rdi                         
  0001800DAF00  7433                       je 0x1800daf35                           -> 0x1800DAF35 (.text)
  0001800DAF02  488BCF                     mov rcx, rdi                          
  0001800DAF05  E8B6CB0800                 call 0x180167ac0                         -> 0x180167AC0 (.text)
  0001800DAF0A  488BCF                     mov rcx, rdi                          
  0001800DAF0D  8BD8                       mov ebx, eax                          
  0001800DAF0F  E88CCB0800                 call 0x180167aa0                         -> 0x180167AA0 (.text)
  0001800DAF14  488BD0                     mov rdx, rax                          
  0001800DAF17  C7442420FFFFFFFF           mov dword ptr [rsp + 0x20], 0xffffffff
  0001800DAF1F  41B101                     mov r9b, 1                            
  0001800DAF22  448BC3                     mov r8d, ebx                          
  0001800DAF25  498BCF                     mov rcx, r15                          
  0001800DAF28  E873CCFDFF                 call 0x1800b7ba0                         -> 0x1800B7BA0 (.text)
  0001800DAF2D  84C0                       test al, al                           
  0001800DAF2F  0F85AC010000               jne 0x1800db0e1                          -> 0x1800DB0E1 (.text)
  0001800DAF35  33D2                       xor edx, edx                          
  0001800DAF37  498BCF                     mov rcx, r15                          
  0001800DAF3A  E8F16DFDFF                 call 0x1800b1d30                         -> 0x1800B1D30 (.text)
  0001800DAF3F  84C0                       test al, al                           
  0001800DAF41  7463                       je 0x1800dafa6                           -> 0x1800DAFA6 (.text)
  0001800DAF43  BA01000000                 mov edx, 1                            
  0001800DAF48  498BCF                     mov rcx, r15                          
  0001800DAF4B  E8E06DFDFF                 call 0x1800b1d30                         -> 0x1800B1D30 (.text)
  0001800DAF50  84C0                       test al, al                           
  0001800DAF52  7452                       je 0x1800dafa6                           -> 0x1800DAFA6 (.text)
  0001800DAF54  488B0DCD996300             mov rcx, qword ptr [rip + 0x6399cd]      ; -> 0x180714928
  0001800DAF5B  E810200900                 call 0x18016cf70                         -> 0x18016CF70 (.text)
  0001800DAF60  8BD0                       mov edx, eax                          
  0001800DAF62  4533C0                     xor r8d, r8d                          
  0001800DAF65  498BCF                     mov rcx, r15                          
  0001800DAF68  E8C3DDFDFF                 call 0x1800b8d30                         -> 0x1800B8D30 (.text)
  0001800DAF6D  B301                       mov bl, 1                             
  0001800DAF6F  0FB6C3                     movzx eax, bl                         
  0001800DAF72  4883C430                   add rsp, 0x30                         
  0001800DAF76  415F                       pop r15                               
  0001800DAF78  415C                       pop r12                               
  0001800DAF7A  5F                         pop rdi                               
  0001800DAF7B  5E                         pop rsi                               
  0001800DAF7C  5B                         pop rbx                               
  0001800DAF7D  C3                         ret                                   
  0001800DAF7E  E8DD1FFEFF                 call 0x1800bcf60                         -> 0x1800BCF60 (.text)
  0001800DAF83  84C0                       test al, al                           
  0001800DAF85  0F8558010000               jne 0x1800db0e3                          -> 0x1800DB0E3 (.text)
  0001800DAF8B  B911000000                 mov ecx, 0x11                         
  0001800DAF90  E82BFAFFFF                 call 0x1800da9c0                         -> 0x1800DA9C0 (.text)
  0001800DAF95  B301                       mov bl, 1                             
  0001800DAF97  0FB6C3                     movzx eax, bl                         
  0001800DAF9A  4883C430                   add rsp, 0x30                         
  0001800DAF9E  415F                       pop r15                               
  0001800DAFA0  415C                       pop r12                               
  0001800DAFA2  5F                         pop rdi                               
  0001800DAFA3  5E                         pop rsi                               
  0001800DAFA4  5B                         pop rbx                               
  0001800DAFA5  C3                         ret                                   
  0001800DAFA6  4C896C2468                 mov qword ptr [rsp + 0x68], r13       
  0001800DAFAB  E8F08F0900                 call 0x180173fa0                         -> 0x180173FA0 (.text)
  0001800DAFB0  8BD0                       mov edx, eax                          
  0001800DAFB2  498BCC                     mov rcx, r12                          
  0001800DAFB5  8BD8                       mov ebx, eax                          
  0001800DAFB7  E8F478FDFF                 call 0x1800b28b0                         -> 0x1800B28B0 (.text)
  0001800DAFBC  85DB                       test ebx, ebx                         
  0001800DAFBE  0F84C2000000               je 0x1800db086                           -> 0x1800DB086 (.text)
  0001800DAFC4  83EB01                     sub ebx, 1                            
  0001800DAFC7  0F8507010000               jne 0x1800db0d4                          -> 0x1800DB0D4 (.text)
  0001800DAFCD  48896C2460                 mov qword ptr [rsp + 0x60], rbp       
  0001800DAFD2  4C89742470                 mov qword ptr [rsp + 0x70], r14       
  0001800DAFD7  E834A5FBFF                 call 0x180095510                         -> 0x180095510 (.text)
  0001800DAFDC  498BCF                     mov rcx, r15                          
  0001800DAFDF  488BE8                     mov rbp, rax                          
  0001800DAFE2  E8E994F4FF                 call 0x1800244d0                         -> 0x1800244D0 (.text)
  0001800DAFE7  488B0D224B6300             mov rcx, qword ptr [rip + 0x634b22]      ; -> 0x18070FB10
  0001800DAFEE  8BD0                       mov edx, eax                          
  0001800DAFF0  448BE8                     mov r13d, eax                         
  0001800DAFF3  E828680200                 call 0x180101820                         -> 0x180101820 (.text)
  0001800DAFF8  4C8BF0                     mov r14, rax                          
  0001800DAFFB  E840C4F2FF                 call 0x180007440                         -> 0x180007440 (.text)
  0001800DB000  8BD8                       mov ebx, eax                          
  0001800DB002  E84969F3FF                 call 0x180011950                         -> 0x180011950 (.text)
  0001800DB007  8BF8                       mov edi, eax                          
  0001800DB009  E84269F3FF                 call 0x180011950                         -> 0x180011950 (.text)
  0001800DB00E  488BCD                     mov rcx, rbp                          
  0001800DB011  8BF0                       mov esi, eax                          
  0001800DB013  E808A9FBFF                 call 0x180095920                         -> 0x180095920 (.text)
  0001800DB018  448BCF                     mov r9d, edi                          
  0001800DB01B  89742420                   mov dword ptr [rsp + 0x20], esi       
  0001800DB01F  448BC3                     mov r8d, ebx                          
  0001800DB022  498BD6                     mov rdx, r14                          
  0001800DB025  488BCD                     mov rcx, rbp                          
  0001800DB028  E823ABFBFF                 call 0x180095b50                         -> 0x180095B50 (.text)
  0001800DB02D  8BD7                       mov edx, edi                          
  0001800DB02F  498BCC                     mov rcx, r12                          
  0001800DB032  E8397FFDFF                 call 0x1800b2f70                         -> 0x1800B2F70 (.text)
  0001800DB037  8BD6                       mov edx, esi                          
  0001800DB039  498BCC                     mov rcx, r12                          
  0001800DB03C  E87F78FDFF                 call 0x1800b28c0                         -> 0x1800B28C0 (.text)
  0001800DB041  488BCD                     mov rcx, rbp                          
  0001800DB044  E867A8FBFF                 call 0x1800958b0                         -> 0x1800958B0 (.text)
  0001800DB049  410FB79620050000           movzx edx, word ptr [r14 + 0x520]     
  0001800DB051  440FB6C8                   movzx r9d, al                         
  0001800DB055  448BC6                     mov r8d, esi                          
  0001800DB058  418BCD                     mov ecx, r13d                         
  0001800DB05B  E890DFF6FF                 call 0x180048ff0                         -> 0x180048FF0 (.text)
  0001800DB060  410FB69617010000           movzx edx, byte ptr [r14 + 0x117]     
  0001800DB068  418BCD                     mov ecx, r13d                         
  0001800DB06B  E8C0DFF6FF                 call 0x180049030                         -> 0x180049030 (.text)
  0001800DB070  41807E0100                 cmp byte ptr [r14 + 1], 0             
  0001800DB075  4C8B742470                 mov r14, qword ptr [rsp + 0x70]       
  0001800DB07A  488B6C2460                 mov rbp, qword ptr [rsp + 0x60]       
  0001800DB07F  7453                       je 0x1800db0d4                           -> 0x1800DB0D4 (.text)
  0001800DB081  418BCD                     mov ecx, r13d                         
  0001800DB084  EB49                       jmp 0x1800db0cf                          -> 0x1800DB0CF (.text)
  0001800DB086  498BCF                     mov rcx, r15                          
  0001800DB089  E84294F4FF                 call 0x1800244d0                         -> 0x1800244D0 (.text)
  0001800DB08E  488B0D7B4A6300             mov rcx, qword ptr [rip + 0x634a7b]      ; -> 0x18070FB10
  0001800DB095  8BD0                       mov edx, eax                          
  0001800DB097  8BF8                       mov edi, eax                          
  0001800DB099  E882670200                 call 0x180101820                         -> 0x180101820 (.text)
  0001800DB09E  8BCF                       mov ecx, edi                          
  0001800DB0A0  488BD8                     mov rbx, rax                          
  0001800DB0A3  E8C8B9FDFF                 call 0x1800b6a70                         -> 0x1800B6A70 (.text)
  0001800DB0A8  8BD0                       mov edx, eax                          
  0001800DB0AA  498BCC                     mov rcx, r12                          
  0001800DB0AD  E82E82FDFF                 call 0x1800b32e0                         -> 0x1800B32E0 (.text)
  0001800DB0B2  8BCF                       mov ecx, edi                          
  0001800DB0B4  E827E0F6FF                 call 0x1800490e0                         -> 0x1800490E0 (.text)
  0001800DB0B9  0FB69317010000             movzx edx, byte ptr [rbx + 0x117]     
  0001800DB0C0  8BCF                       mov ecx, edi                          
  0001800DB0C2  E869DFF6FF                 call 0x180049030                         -> 0x180049030 (.text)
  0001800DB0C7  807B0100                   cmp byte ptr [rbx + 1], 0             
  0001800DB0CB  7407                       je 0x1800db0d4                           -> 0x1800DB0D4 (.text)
  0001800DB0CD  8BCF                       mov ecx, edi                          
  0001800DB0CF  E84CE1F6FF                 call 0x180049220                         -> 0x180049220 (.text)
  0001800DB0D4  498BCF                     mov rcx, r15                          
  0001800DB0D7  E864D4FDFF                 call 0x1800b8540                         -> 0x1800B8540 (.text)
  0001800DB0DC  4C8B6C2468                 mov r13, qword ptr [rsp + 0x68]       
  0001800DB0E1  B301                       mov bl, 1                             
  0001800DB0E3  0FB6C3                     movzx eax, bl                         
  0001800DB0E6  4883C430                   add rsp, 0x30                         
  0001800DB0EA  415F                       pop r15                               
  0001800DB0EC  415C                       pop r12                               
  0001800DB0EE  5F                         pop rdi                               
  0001800DB0EF  5E                         pop rsi                               
  0001800DB0F0  5B                         pop rbx                               
  0001800DB0F1  C3                         ret                                   
