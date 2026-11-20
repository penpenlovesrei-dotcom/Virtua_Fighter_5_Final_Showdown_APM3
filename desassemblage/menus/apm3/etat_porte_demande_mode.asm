; etat_porte_demande_mode.asm  --  Etat_DemanderUnMode
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll  (le module d'APM3)
;           6965248 octets, md5 3214e19696de  -- l'oracle VIERGE
; Base PE : 0x180000000
; Bornes  : 0x1800DA9A0 - 0x1800DA9B5  (21 octets)   [AUCUNE entree .pdata : borne au premier ret/jmp]
;
; A QUOI : La SEULE porte publique pour demander un mode (27 sites d'appel dans tout le module). Sans pdata : fonction feuille, bornee a son `ret`.
;
; D'OU VIENT LE NOM : VF5RE/analysis/menu_console.md, section 8.5
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
  0001800DA9A0  890D4E1B6300               mov dword ptr [rip + 0x631b4e], ecx      ; -> 0x18070C4F4
  0001800DA9A6  C605531B630001             mov byte ptr [rip + 0x631b53], 1         ; -> 0x18070C500
  0001800DA9AD  C605681B630000             mov byte ptr [rip + 0x631b68], 0         ; -> 0x18070C51C
  0001800DA9B4  C3                         ret                                   
