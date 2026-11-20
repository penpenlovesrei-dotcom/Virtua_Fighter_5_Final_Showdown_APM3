; revo_cstraining_maj.asm  --  CsTraining_MettreAJour (REVO)
;
; Cible   : vf5fs-pxd-w64-d3d12_SteamRetail.dll  (le module de R.E.V.O.)
;           7229952 octets, md5 64fea1ce4db6
; Base PE : 0x180000000
; Bornes  : 0x180212070 - 0x180212083  (19 octets)
;
; A QUOI : Sous-etat 45 = CS_TRAINING, gestionnaire de MISE A JOUR.
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
  000180212070  4883EC28                   sub rsp, 0x28                         
  000180212074  E887920400                 call 0x18025b300                         -> 0x18025B300 (.text)
  000180212079  84C0                       test al, al                           
  00018021207B  0F94C0                     sete al                               
  00018021207E  4883C428                   add rsp, 0x28                         
  000180212082  C3                         ret                                   
