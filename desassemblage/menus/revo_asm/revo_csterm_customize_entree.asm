; revo_csterm_customize_entree.asm  --  CsTermCustomize_EntrerLeSousEtat (REVO)
;
; Cible   : vf5fs-pxd-w64-d3d12_SteamRetail.dll  (le module de R.E.V.O.)
;           7229952 octets, md5 64fea1ce4db6
; Base PE : 0x180000000
; Bornes  : 0x180211F90 - 0x180211FC8  (56 octets)
;
; A QUOI : Sous-etat 41 = CS_TERM_CUSTOMIZE, gestionnaire d'ENTREE. C'est la porte du TERMINAL, le seul sous-menu du menu principal qui atteigne un mode vivant cote APM3.
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
  000180211F90  4883EC28                   sub rsp, 0x28                         
  000180211F94  E8B7E4FDFF                 call 0x1801f0450                         -> 0x1801F0450 (.text)
  000180211F99  488BC8                     mov rcx, rax                          
  000180211F9C  E84FE3FDFF                 call 0x1801f02f0                         -> 0x1801F02F0 (.text)
  000180211FA1  488B0DE0581B00             mov rcx, qword ptr [rip + 0x1b58e0]      ; -> 0x1803C7888
  000180211FA8  BA08000000                 mov edx, 8                            
  000180211FAD  E8DE84ECFF                 call 0x1800da490                         -> 0x1800DA490 (.text)
  000180211FB2  BA08000000                 mov edx, 8                            
  000180211FB7  B951000000                 mov ecx, 0x51                         
  000180211FBC  E88FFCE6FF                 call 0x180081c50                         -> 0x180081C50 (.text)
  000180211FC1  B001                       mov al, 1                             
  000180211FC3  4883C428                   add rsp, 0x28                         
  000180211FC7  C3                         ret                                   
