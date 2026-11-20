; tache_creer_par_nom.asm  --  Tache_CreerParNom  (la fabrique de taches)
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x180245830 - 0x180245849  (25 octets)   [AUCUNE entree .pdata : borne au premier ret/jmp]
;
; A QUOI : LA fabrique de taches par nom d'APM3 : (objet, "NOM"). 165 references dans le module, mesurees. Jumelle de FUN_1802CD400 cote REVO, qui en a 189. Pas d'entree .pdata : feuille, bornee au premier ret/jmp. C'est par elle que passent toutes les scenes du menu (ARCADE MENU, VERSUS MENU, TRAINING MENU, TERMINAL MENU, OPTION...).
;
; D'OU VIENT LE NOM : mesure du 2026-11-19 : 0x1801E46D0, corps du fn_entree de MENU_MAIN, fait `mov rcx,[0x180753818] ; lea rdx,"MAIN MENU" ; jmp ici`
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
  000180245830  4C8BC2                     mov r8, rdx                           
  000180245833  41B902000000               mov r9d, 2                            
  000180245839  488B1500BB9F00             mov rdx, qword ptr [rip + 0x9fbb00]      ; -> 0x180C41340
  000180245840  488B5210                   mov rdx, qword ptr [rdx + 0x10]       
  000180245844  E977FEFFFF                 jmp 0x1802456c0                          -> 0x1802456C0 (.text)
