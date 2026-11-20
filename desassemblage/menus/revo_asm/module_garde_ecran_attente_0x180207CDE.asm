; module_garde_ecran_attente_0x180207CDE.asm
;
; Binaire : vf5fs-pxd-w64-d3d12_SteamRetail.dll (le module de R.E.V.O.)
; Base d'image 0x180000000 ; .text commence a 0x180001000.
; Lu le 2026-11-09, SS 419.76 a 419.79. Desassemblage, PAS une decompilation.
;
; CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est une
; LECTURE du module, gardee pour ne pas la refaire.
;
; SUJET : le garde complet de l'ALLUMAGE de l'ecran d'attente du menu, dans
; `FUN_1802079E0` (la mise a jour de la tache [MAIN MENU]).
;
; POURQUOI CE FICHIER EXISTE. Deux lectures se sont contredites pendant trois
; sections : la note du SS 316 dans l'hote donnait le garde comme
; `(212 == 1 || menu+0x28F9 == 0)`, et le SS 419.76 le donnait comme
; `commande 81 == 1`. Or `FUN_1801A4030` n'a qu'UN site d'appel dans cette
; fonction, donc les deux decrivaient le meme allumage. La reponse est qu'il
; y a TROIS conjonctions, separees par 0x4A8 octets de code et par 270 lignes
; de decompilation Ghidra -- Ghidra ne range pas ses blocs par adresse, donc
; les numeros de ligne ne disent rien de l'imbrication.
;
;     (212 == 1 || menu+0x28F9 == 0)  &&  repartiteur != NULL  &&  81 == 1


; =====================================================================
; GARDE 1 -- le OU de la note du SS 316.  RBX = l'objet du menu.
; =====================================================================
180207cde  E88D380C00   CALL     0x1802cb570      ; = commande 212 (0xD4)
180207ce3  41BD01000000 MOV      R13D, 0x1
180207ce9  84C0         TEST     AL, AL
180207ceb  7511         JNZ      0x180207cfe      ; 212 rend 1 -> ENTRE
180207ced  4C8DB3E8280000 LEA    R14, [RBX + 0x28e8]
180207cf4  41387611     CMP      byte ptr [R14 + 0x11], SIL   ; = RBX+0x28F9
180207cf8  0F858D040000 JNZ      0x18020818b      ; +0x28F9 != 0 -> SAUTE
180207cfe  ...                                   ; LE CORPS commence ici

; Le champ de la note est bien la, mais calcule PAR UN REGISTRE DE BASE :
; R14 = RBX+0x28E8, puis [R14+0x11]. Une recherche de references sur le champ
; `+0x28F9` ne l'aurait jamais trouve.
;
; La cible du saut, 0x18020818B, est l'instruction qui SUIT immediatement
; l'allumage : le corps enjambe va donc exactement de 0x180207CFE a
; 0x180208186, et il SE TERMINE sur l'allumage.


; =====================================================================
; LE CORPS -- tout le travail de chaque image du menu
; (extrait : ce qui prouve qu'on ne peut pas le sauter)
; =====================================================================
180207d37  E8C49DFCFF   CALL     0x1801d1b00
180207d5b  E800D7FCFF   CALL     0x1801d5460
180207d6d  E89ED6FCFF   CALL     0x1801d5410
180207d74  E8C72CFAFF   CALL     0x1801aaa40      ; ECX = 0
180207d80  E8BB2CFAFF   CALL     0x1801aaa40      ; ECX = 1
180207d8e  E8AD2CFAFF   CALL     0x1801aaa40      ; ECX = 2
180207d9c  E89F2CFAFF   CALL     0x1801aaa40      ; ECX = 3
180207daa  E8912CFAFF   CALL     0x1801aaa40      ; ECX = 4
180207db3  B906000000   MOV      ECX, 0x6         ; ... et 6
...
18020806d  E8FE340C00   CALL     0x1802cb570      ; 212, RESULTAT RANGE :
180208072  88842486000000 MOV    byte ptr [RSP + 0x86], AL   ; <<< pas un garde
180208079  4038B309290000 CMP    byte ptr [RBX + 0x2909], SIL  ; +0x2909, PAS 28F9
180208080  7518         JNZ      0x18020809a
180208082  488B0D97AE2200 MOV    RCX, qword ptr [0x180432f20]
180208089  E862BEF9FF   CALL     0x1801a3ef0
1802080a2  E8D9360C00   CALL     0x1802cb780      ; cmd 136 selecteur 10
1802080ae  E80D140100   CALL     0x1802194c0
1802080c1  E80A7A0200   CALL     0x18022fad0
1802080d0  E84BE9FFFF   CALL     0x180206a20
1802080e3  E8A89BFCFF   CALL     0x1801d1c90

; Fermer le garde 1 en posant `+0x28F9` sauterait TOUT cela : destructeur.


; =====================================================================
; GARDES 2 et 3 -- le repartiteur, puis la commande 81
; =====================================================================
1802080e8  488B0D395EA800 MOV    RCX, qword ptr [0x180c8df28]   ; le bloc
1802080ef  488B8108FF0100 MOV    RAX, qword ptr [RCX + 0x1ff08] ; le repartiteur
1802080f6  4885C0       TEST     RAX, RAX
1802080f9  0F84B6080000 JZ       0x1802089b5      ; pas de repartiteur -> chemin B
1802080ff  4C8D442470   LEA      R8, [RSP + 0x70]
180208104  BA51000000   MOV      EDX, 0x51        ; COMMANDE 81
180208109  488B8910FF0100 MOV    RCX, qword ptr [RCX + 0x1ff10]
180208110  FFD0         CALL     RAX
180208112  413BC5       CMP      EAX, R13D        ; R13D = 1
180208115  0F859A080000 JNZ      0x1802089b5      ; != 1 -> CHEMIN B

; UN SEUL TEST, donc pas de `||` ici. Et un balayage des immediats de tout le
; module ne trouve qu'UN SEUL `MOV EDX,0x51` : celui-ci. L'INITIALISATION de
; MAIN MENU, `FUN_18020F1E0`, ne lit donc PAS la commande 81 -- le piege du
; SS 321 (ou repondre 2 a la commande 80 faisait echouer l'init et
; `FUN_1802079E0` ne tournait plus jamais) n'existe pas ici.


; =====================================================================
; CHEMIN A (81 == 1) -- le switch des modes, puis L'ALLUMAGE
; =====================================================================
18020811b  0FB683C4280000 MOVZX  EAX, byte ptr [RBX + 0x28c4]
180208122  83F80E       CMP      EAX, 0xe
180208125  7756         JA       0x18020817d      ; > 14 -> default (mode 0)
180208127  488D3DD27EDFFF LEA    RDI, [0x180000000]
18020812e  8B8C87588E2000 MOV    ECX, dword ptr [RDI + RAX*0x4 + 0x208e58]
180208135  4803CF       ADD      RCX, RDI
180208138  FFE1         JMP      RCX              ; table de sauts a 0x180208E58
180208157  B203         MOV      DL, 0x3          ; les modes du switch
18020815b  B204         MOV      DL, 0x4
18020815f  B209         MOV      DL, 0x9
180208163  B202         MOV      DL, 0x2
...
18020817f  488B0D...    MOV      RCX, qword ptr [0x180432f20]
180208186  E8A51E...    CALL     0x1801a4030      ; <<<< ALLUME L'ECRAN D'ATTENTE
18020818b  498BCE       MOV      RCX, R14         ; <<<< cible du JNZ du garde 1
18020818e  E8...        CALL     0x18020a2b0
18020819b  E8...        CALL     0x1800ba920
1802081a8  488DBBC4280000 LEA    RDI, [RBX + 0x28c4]
1802081bb  83F810       CMP      EAX, 0x10
1802081be  0F87...      JA       0x180208950      ; les 17 ETATS du menu

; Notre `+0x28C4` vaut 17 : il tombe dans le `default` du switch, donc mode 0.


; =====================================================================
; CHEMIN B (81 != 1) -- le menu pilote par le module. AUCUN ALLUMEUR.
; =====================================================================
1802089b5  4038B3CF280000 CMP    byte ptr [RBX + 0x28cf], SIL
1802089bc  741F         JZ       0x1802089dd
1802089be  488B8C24A8000000 MOV  RCX, qword ptr [RSP + 0xa8]
1802089c6  8B4928       MOV      ECX, dword ptr [RCX + 0x28]
1802089c9  E8E2E50500   CALL     0x180266fb0
1802089ce  488BCB       MOV      RCX, RBX
1802089d1  E84A8A0000   CALL     0x180211420      ; L'ENTREE DU MENU
1802089d6  4088B3CF280000 MOV    byte ptr [RBX + 0x28cf], SIL
1802089dd  E88E2B0C00   CALL     0x1802cb570      ; 212 -> faux chez nous
1802089e2  84C0         TEST     AL, AL
1802089e4  0F85B4000000 JNZ      0x180208a9e      ; non pris
1802089ea  413936       CMP      dword ptr [R14], ESI
1802089f1  E84AB8F8FF   CALL     0x180194240
180208a06  488D15DB1B3500 LEA    RDX, [0x18055a5e8]
180208a0f  E88CC0F8FF   CALL     0x180194aa0
180208a14  E8572B0C00   CALL     0x1802cb570
180208a33  E8785F0000   CALL     0x18020e9b0
180208a38  E85366FCFF   CALL     0x1801cf090
180208a40  E8FB64FCFF   CALL     0x1801cef40
180208a4c  E8AF90EDFF   CALL     0x1800e1b00      ; ECX = 0
180208a56  E8C590EDFF   CALL     0x1800e1b20      ; ECX = 5  (= mode MENU ?)
180208a61  E83AC7F8FF   CALL     0x1801951a0
180208a68  E863C7F8FF   CALL     0x1801951d0      ; ECX = 0
180208a70  E85BC7F8FF   CALL     0x1801951d0      ; ECX = 1
180208a9e  E8CD2A0C00   CALL     0x1802cb570
180208ac5  488D93B0270000 LEA    RDX, [RBX + 0x27b0]
180208ace  E85D52FEFF   CALL     0x1801edd30
180208ae0  C60700       MOV      byte ptr [RDI], 0x0   ; RDI = RBX+0x27d3
180208b00  E8AB4FFEFF   CALL     0x1801edab0
180208b4d  E83E5BFEFF   CALL     0x1801ee690
180208b81  (fin commune)

; Quatre appels a 0x1802CB570 et AUCUN allumeur. Le travail porte sur
; +0x27B0..+0x27D5 et +0x28DE : les champs du TaskDataSelector. Au passage
; +0x27D3 est mis a 0 -- le champ meme que notre reponse a la commande 136
; definit depuis le SS 419.74.


; =====================================================================
; L'EXTINCTION -- en amont de tout cela, donc hors d'atteinte du garde 3
; =====================================================================
; 0x180207B7D, gardee par `menu+0x28DD` (une seule fois) :
;     if (menu+0x28DD == 0) {
;         if (FUN_18021BC00(&x)) goto fin;
;         menu+0x28DD = 1;
;         FUN_180218530(lVar11, menu+0x27B0);
;         FUN_1801A3F20(&DAT_1807956D0);     // ETEINT
;     }
; 0x180207B7D < 0x180208104 : rien de ce qui precede l'appel de la 81 ne
; depend de notre reponse. L'extinction tire donc identiquement.


; =====================================================================
; LA TABLE DES MODES -- d'ou vient l'AUTRE allumage, celui du chargement
; =====================================================================
; Formule, lue dans l'hote (vf5fs_host.cpp ligne 20510), pas recopiee :
;     idx = index du mode courant dans la table 0x3C8240 (14 x 0x68 octets)
;     fn  = [0x3C8248 + idx*0x68 + phase*8]
; Pour idx = 2 : 0x3C8248 + 0xD0 = 0x3C8318, soit la PHASE 0.
;
; 0x3C8310  05 00 00 00  00 00 00 00   ; numero du mode = 5 = MENU
; 0x3C8318  40 41 0e 80 01 00 00 00   ; phase 0 -> FUN_1800E4140
; 0x3C8320  80 40 0e 80 01 00 00 00   ; phase 1 -> FUN_1800E4080
; 0x3C8328  c0 40 0e 80 01 00 00 00   ; phase 2 -> FUN_1800E40C0
;
; Les records 0 et 1 portent les modes 0 et 1 : la table est donc cherchee
; PAR NUMERO, pas indexee.
;
; `FUN_1800E4140` (mode 5 phase 0) allume l'ecran -- c'est l'ecran de
; CHARGEMENT du menu. Il arme trois chargements (0x268, 0x269, 0x208),
; verrouille `+0x18 = 1`, et rend 1 (donc passe a la phase 1) quand les trois
; sont finis. Il s'eteint TOUT SEUL. A ne pas confondre avec le rallumage.
;
; `FUN_1800E4080` (phase 1) : `return uVar1 & 0xffffffffffffff00` -- l'octet
; bas est MASQUE, donc cette phase ne rend JAMAIS << fini >>. Ce n'est pas un
; bouchon : le menu est un mode ou l'on reste. Elle poste la commande 186
; (0xBA) uniquement si `FUN_1802CB570()` est vrai, donc jamais chez nous.


; =====================================================================
; LES DEUX IDEMPOTENTS JUMEAUX (decompilation, pour memoire)
; =====================================================================
;   FUN_1801A4180  sort tot si l'etat == 1 ; batit si besoin ; ecrit 1
;   FUN_1801A3F20  sort tot si l'etat == 0 ;                   ecrit 0
;   FUN_1801A4030  comme 4180, plus un mode dans DAT_1807958F7
; L'etat est le DWORD `DAT_180795788` (= VF5FS+0x795788).
;
; Consequence : un allumeur qui tournerait a chaque image ne laisse AUCUNE
; trace mesurable quand l'ecran est deja allume. Aucune sonde sur cet etat ne
; pouvait repondre a la question -- seule la lecture pouvait.
;
; FUN_1801A4030 n'a que TROIS sites d'appel :
;     1801e6fb9, 1801e6fdd  (dans FUN_1801E6DD0)
;     180208186             (ici, chemin A)
; et sur les 28 sites de FUN_1801A4180, AUCUN n'est dans FUN_1802079E0.
