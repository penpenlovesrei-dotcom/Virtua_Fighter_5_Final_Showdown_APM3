; revo_csterm_customize_maj.asm  --  CsTermCustomize_MettreAJour (REVO)
;
; Cible   : vf5fs-pxd-w64-d3d12_SteamRetail.dll  (le module de R.E.V.O.)
;           7229952 octets, md5 64fea1ce4db6
; Base PE : 0x180000000
; Bornes  : 0x180211A80 - 0x180211B1A  (154 octets)   [3 entrees .pdata chainees]
;
; A QUOI : Sous-etat 41 = CS_TERM_CUSTOMIZE, gestionnaire de MISE A JOUR.
;
; D'OU VIENT LE NOM : VF5RE/TABLE_DES_SCENES_APM3_VS_REVO.md, section 5 (ligne 41)
;
; POURQUOI UN .ASM ET PAS UN .C : cette fonction est NOMMEE dans les notes
; et n'a aucune decompilation dans VF5RE/code_decompile (mesure du
; 2026-11-19). Lue ici par pefile + capstone dans le FICHIER du module.
; Ghidra n'a pas ete touche. Un desassemblage ne donne PAS la structure que
; donnerait une decompilation : il reste a vider proprement.
;
; CE N'EST PAS DU CODE A RECOPIER NI A COMPILER.
;
; ATTENTION AUX ADRESSES : ceci est REVO. Les deux modules ont la MEME base
; 0x180000000 et des adresses DIFFERENTES.
;
  000180211A80  4883EC28                   sub rsp, 0x28                         
  000180211A84  E8C7E9FDFF                 call 0x1801f0450                         -> 0x1801F0450 (.text)
  000180211A89  488BC8                     mov rcx, rax                          
  000180211A8C  E80FDCFDFF                 call 0x1801ef6a0                         -> 0x1801EF6A0 (.text)
  000180211A91  84C0                       test al, al                           
  000180211A93  747E                       je 0x180211b13                           -> 0x180211B13 (.text)
  000180211A95  E8A6FEECFF                 call 0x1800e1940                         -> 0x1800E1940 (.text)
  000180211A9A  833803                     cmp dword ptr [rax], 3                
  000180211A9D  755C                       jne 0x180211afb                          -> 0x180211AFB (.text)
  000180211A9F  E83C07EAFF                 call 0x1800b21e0                         -> 0x1800B21E0 (.text)
  000180211AA4  4885C0                     test rax, rax                         
  000180211AA7  742E                       je 0x180211ad7                           -> 0x180211AD7 (.text)
  000180211AA9  48895C2420                 mov qword ptr [rsp + 0x20], rbx       
  000180211AAE  E82D07EAFF                 call 0x1800b21e0                         -> 0x1800B21E0 (.text)
  000180211AB3  33D2                       xor edx, edx                          
  000180211AB5  488BC8                     mov rcx, rax                          
  000180211AB8  488BD8                     mov rbx, rax                          
  000180211ABB  E8100CEAFF                 call 0x1800b26d0                         -> 0x1800B26D0 (.text)
  000180211AC0  BA01000000                 mov edx, 1                            
  000180211AC5  488BCB                     mov rcx, rbx                          
  000180211AC8  E8030CEAFF                 call 0x1800b26d0                         -> 0x1800B26D0 (.text)
  000180211ACD  E83E06EAFF                 call 0x1800b2110                         -> 0x1800B2110 (.text)
  000180211AD2  488B5C2420                 mov rbx, qword ptr [rsp + 0x20]       
  000180211AD7  E84490F9FF                 call 0x1801aab20                         -> 0x1801AAB20 (.text)
  000180211ADC  488B0DA55D1B00             mov rcx, qword ptr [rip + 0x1b5da5]      ; -> 0x1803C7888
  000180211AE3  33D2                       xor edx, edx                          
  000180211AE5  E8A689ECFF                 call 0x1800da490                         -> 0x1800DA490 (.text)
  000180211AEA  B917000000                 mov ecx, 0x17                         
  000180211AEF  E82C00EDFF                 call 0x1800e1b20                         -> 0x1800E1B20 (.text)
  000180211AF4  32C0                       xor al, al                            
  000180211AF6  4883C428                   add rsp, 0x28                         
  000180211AFA  C3                         ret                                   
  000180211AFB  B905000000                 mov ecx, 5                            
  000180211B00  E8FBFFECFF                 call 0x1800e1b00                         -> 0x1800E1B00 (.text)
  000180211B05  488B0D7C5D1B00             mov rcx, qword ptr [rip + 0x1b5d7c]      ; -> 0x1803C7888
  000180211B0C  33D2                       xor edx, edx                          
  000180211B0E  E87D89ECFF                 call 0x1800da490                         -> 0x1800DA490 (.text)
  000180211B13  32C0                       xor al, al                            
  000180211B15  4883C428                   add rsp, 0x28                         
  000180211B19  C3                         ret                                   
