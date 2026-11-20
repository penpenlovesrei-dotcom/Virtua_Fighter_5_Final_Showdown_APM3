; revo_menu_lecteur_etat_5fa.asm  --  Menu_LireLEtatDUneEntree (REVO)
;
; Cible   : vf5fs-pxd-w64-d3d12_SteamRetail.dll  (le module de R.E.V.O.)
;           7229952 octets, md5 64fea1ce4db6
; Base PE : 0x180000000
; Bornes  : 0x1802117D0 - 0x1802117F5  (37 octets)
;
; A QUOI : Quatrieme site de 0x5FA : `cmp byte [rax+rcx+0x5fa], 2` -- il teste l'etat 2 = pas dessinee du tout. Sans .c dans code_decompile.
;
; D'OU VIENT LE NOM : VF5RE/code_decompile/MENU.md, section 419.83 (les quatre sites de 0x5FA)
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
  0001802117D0  4883EC28                   sub rsp, 0x28                         
  0001802117D4  48634158                   movsxd rax, dword ptr [rcx + 0x58]    
  0001802117D8  80BC08FA05000002           cmp byte ptr [rax + rcx + 0x5fa], 2   
  0001802117E0  7507                       jne 0x1802117e9                          -> 0x1802117E9 (.text)
  0001802117E2  32C0                       xor al, al                            
  0001802117E4  4883C428                   add rsp, 0x28                         
  0001802117E8  C3                         ret                                   
  0001802117E9  E812E3FCFF                 call 0x1801dfb00                         -> 0x1801DFB00 (.text)
  0001802117EE  B001                       mov al, 1                             
  0001802117F0  4883C428                   add rsp, 0x28                         
  0001802117F4  C3                         ret                                   
