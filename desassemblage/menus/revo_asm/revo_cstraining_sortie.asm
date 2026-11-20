; revo_cstraining_sortie.asm  --  CsTraining_SortirDuSousEtat (REVO)
;
; Cible   : vf5fs-pxd-w64-d3d12_SteamRetail.dll  (le module de R.E.V.O.)
;           7229952 octets, md5 64fea1ce4db6
; Base PE : 0x180000000
; Bornes  : 0x1802120D0 - 0x1802120E5  (21 octets)
;
; A QUOI : Sous-etat 45 = CS_TRAINING, gestionnaire de SORTIE.
;
; D'OU VIENT LE NOM : VF5RE/TABLE_DES_SCENES_APM3_VS_REVO.md, section 5 (ligne 45)
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
  0001802120D0  4883EC28                   sub rsp, 0x28                         
  0001802120D4  E8C7920400                 call 0x18025b3a0                         -> 0x18025B3A0 (.text)
  0001802120D9  E8E215FAFF                 call 0x1801b36c0                         -> 0x1801B36C0 (.text)
  0001802120DE  B001                       mov al, 1                             
  0001802120E0  4883C428                   add rsp, 0x28                         
  0001802120E4  C3                         ret                                   
