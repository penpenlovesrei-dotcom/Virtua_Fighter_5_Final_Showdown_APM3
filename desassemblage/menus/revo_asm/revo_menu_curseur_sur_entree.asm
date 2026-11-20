; revo_menu_curseur_sur_entree.asm  --  Menu_PoserLeCurseurSurLEntree (REVO)
;
; Cible   : vf5fs-pxd-w64-d3d12_SteamRetail.dll  (le module de R.E.V.O.)
;           7229952 octets, md5 64fea1ce4db6
; Base PE : 0x180000000
; Bornes  : 0x1801E1080 - 0x1801E10BF  (63 octets)
;
; A QUOI : Appelee par le dessin des lignes (FUN_18020C880) quand l'indice de boucle egale [menu+0x58], l'entree choisie : c'est ce qui place le curseur. Sans .c dans code_decompile.
;
; D'OU VIENT LE NOM : VF5RE/code_decompile/MENU.md, section 419.83 (extrait du chemin autonome de FUN_18020C880)
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
  0001801E1080  4053                       push rbx                              
  0001801E1082  4883EC30                   sub rsp, 0x30                         
  0001801E1086  833903                     cmp dword ptr [rcx], 3                
  0001801E1089  488BD9                     mov rbx, rcx                          
  0001801E108C  752B                       jne 0x1801e10b9                          -> 0x1801E10B9 (.text)
  0001801E108E  8B4914                     mov ecx, dword ptr [rcx + 0x14]       
  0001801E1091  85C9                       test ecx, ecx                         
  0001801E1093  7424                       je 0x1801e10b9                           -> 0x1801E10B9 (.text)
  0001801E1095  C5F857C0                   vxorps xmm0, xmm0, xmm0               
  0001801E1099  488D542420                 lea rdx, [rsp + 0x20]                 
  0001801E109E  C5FA11442428               vmovss dword ptr [rsp + 0x28], xmm0   
  0001801E10A4  C5FA114C2420               vmovss dword ptr [rsp + 0x20], xmm1   
  0001801E10AA  C5FA11542424               vmovss dword ptr [rsp + 0x24], xmm2   
  0001801E10B0  E8CB51E4FF                 call 0x180026280                         -> 0x180026280 (.text)
  0001801E10B5  C6431801                   mov byte ptr [rbx + 0x18], 1          
  0001801E10B9  4883C430                   add rsp, 0x30                         
  0001801E10BD  5B                         pop rbx                               
  0001801E10BE  C3                         ret                                   
