; revo_csterm_customize_sortie.asm  --  CsTermCustomize_SortirDuSousEtat (REVO)
;
; Cible   : vf5fs-pxd-w64-d3d12_SteamRetail.dll  (le module de R.E.V.O.)
;           7229952 octets, md5 64fea1ce4db6
; Base PE : 0x180000000
; Bornes  : 0x180211E90 - 0x180211EA8  (24 octets)
;
; A QUOI : Sous-etat 41 = CS_TERM_CUSTOMIZE, gestionnaire de SORTIE.
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
  000180211E90  4883EC28                   sub rsp, 0x28                         
  000180211E94  E8B7E5FDFF                 call 0x1801f0450                         -> 0x1801F0450 (.text)
  000180211E99  488BC8                     mov rcx, rax                          
  000180211E9C  E8DFDBFDFF                 call 0x1801efa80                         -> 0x1801EFA80 (.text)
  000180211EA1  B001                       mov al, 1                             
  000180211EA3  4883C428                   add rsp, 0x28                         
  000180211EA7  C3                         ret                                   
