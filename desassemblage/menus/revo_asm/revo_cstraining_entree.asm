; revo_cstraining_entree.asm  --  CsTraining_EntrerLeSousEtat (REVO)
;
; Cible   : vf5fs-pxd-w64-d3d12_SteamRetail.dll  (le module de R.E.V.O.)
;           7229952 octets, md5 64fea1ce4db6
; Base PE : 0x180000000
; Bornes  : 0x180212140 - 0x1802121EB  (171 octets)
;
; A QUOI : Sous-etat 45 = CS_TRAINING, gestionnaire d'ENTREE. C'est la destination des cinq entrees 5 a 9 du switch du MAIN MENU, qui menent toutes au mode 7 et ne se distinguent que par leur SORTE.
;
; D'OU VIENT LE NOM : VF5RE/TABLE_DES_SCENES_APM3_VS_REVO.md, section 5 (ligne 45) ; VF5RE/code_decompile/MENU.md section 5
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
  000180212140  48895C2408                 mov qword ptr [rsp + 8], rbx          
  000180212145  57                         push rdi                              
  000180212146  4883EC20                   sub rsp, 0x20                         
  00018021214A  BBFFFFFFFF                 mov ebx, 0xffffffff                   
  00018021214F  E86C85F9FF                 call 0x1801aa6c0                         -> 0x1801AA6C0 (.text)
  000180212154  83E806                     sub eax, 6                            
  000180212157  745A                       je 0x1802121b3                           -> 0x1802121B3 (.text)
  000180212159  83E801                     sub eax, 1                            
  00018021215C  7438                       je 0x180212196                           -> 0x180212196 (.text)
  00018021215E  83E801                     sub eax, 1                            
  000180212161  7422                       je 0x180212185                           -> 0x180212185 (.text)
  000180212163  83E801                     sub eax, 1                            
  000180212166  7411                       je 0x180212179                           -> 0x180212179 (.text)
  000180212168  83F801                     cmp eax, 1                            
  00018021216B  7518                       jne 0x180212185                          -> 0x180212185 (.text)
  00018021216D  BF04000000                 mov edi, 4                            
  000180212172  BB27000000                 mov ebx, 0x27                         
  000180212177  EB54                       jmp 0x1802121cd                          -> 0x1802121CD (.text)
  000180212179  BF03000000                 mov edi, 3                            
  00018021217E  BB27000000                 mov ebx, 0x27                         
  000180212183  EB48                       jmp 0x1802121cd                          -> 0x1802121CD (.text)
  000180212185  33FF                       xor edi, edi                          
  000180212187  E8B4AEFCFF                 call 0x1801dd040                         -> 0x1801DD040 (.text)
  00018021218C  488BC8                     mov rcx, rax                          
  00018021218F  E8FCA8FCFF                 call 0x1801dca90                         -> 0x1801DCA90 (.text)
  000180212194  EB37                       jmp 0x1802121cd                          -> 0x1802121CD (.text)
  000180212196  BF01000000                 mov edi, 1                            
  00018021219B  E80085F9FF                 call 0x1801aa6a0                         -> 0x1801AA6A0 (.text)
  0001802121A0  BB27000000                 mov ebx, 0x27                         
  0001802121A5  84C0                       test al, al                           
  0001802121A7  B90B000000                 mov ecx, 0xb                          
  0001802121AC  0F44CB                     cmove ecx, ebx                        
  0001802121AF  8BD9                       mov ebx, ecx                          
  0001802121B1  EB1A                       jmp 0x1802121cd                          -> 0x1802121CD (.text)
  0001802121B3  BF02000000                 mov edi, 2                            
  0001802121B8  E883AEFCFF                 call 0x1801dd040                         -> 0x1801DD040 (.text)
  0001802121BD  488BC8                     mov rcx, rax                          
  0001802121C0  4533C0                     xor r8d, r8d                          
  0001802121C3  BA5D000000                 mov edx, 0x5d                         
  0001802121C8  E8A3B3FCFF                 call 0x1801dd570                         -> 0x1801DD570 (.text)
  0001802121CD  E8CE9A0400                 call 0x18025bca0                         -> 0x18025BCA0 (.text)
  0001802121D2  4533C0                     xor r8d, r8d                          
  0001802121D5  8BD3                       mov edx, ebx                          
  0001802121D7  8BCF                       mov ecx, edi                          
  0001802121D9  E8B2980400                 call 0x18025ba90                         -> 0x18025BA90 (.text)
  0001802121DE  488B5C2430                 mov rbx, qword ptr [rsp + 0x30]       
  0001802121E3  B001                       mov al, 1                             
  0001802121E5  4883C420                   add rsp, 0x20                         
  0001802121E9  5F                         pop rdi                               
  0001802121EA  C3                         ret                                   
