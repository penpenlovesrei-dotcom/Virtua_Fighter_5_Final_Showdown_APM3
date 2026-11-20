; apm3_pages_sousmenus_0x1E1C51.asm -- LES QUATRE PAGES FILLES DU MENU,
; lues dans le module d'APM3 d'origine et mises en regard de REVO.
; Releve du 2026-11-09 (SS 419.94).
;
; ------------------------------------------------------------------------
; POURQUOI CE FICHIER EXISTE
; ------------------------------------------------------------------------
; Le menu de REVO affichait des libelles DECALES : ligne 0 << OFFLINE
; VERSUS >> la ou il faut << SINGLE PLAYER >>, en-tete du DOJO
; << SCOREBOARDS >>, et des lignes << Select data / Difficulty / VERY EASY /
; EASY >> sous SINGLE PLAYER.
;
; LA CAUSE. Le module a ete recompile contre la liste de textes de REVO, qui
; a des entrees de plus, alors que le `string_array.farc` livre est le
; millesime FS. En vente ca ne se voit pas : le module ne lit JAMAIS
; `string_array`, il demande chaque libelle a l'hote par la commande 135.
; C'est NOTRE chemin autonome qui lit la table en direct.
;
; POURQUOI ICI ET PAS DANS `code_decompile`. Les identifiants sont des
; IMMEDIATS ecrits dans des variables de PILE. La decompilation Ghidra les
; montre, mais elle ne donne ni l'adresse exacte de l'immediat ni les octets
; qui le precedent -- or c'est exactement ce qu'il faut pour controler un
; site avant d'y ecrire. Et le cote APM3 n'est pas charge dans Ghidra du
; tout : il est LU dans le fichier. C'est donc un desassemblage, pas une
; decompilation. Les onze fonctions, elles, sont consignees dans
; `VF5RE/a_vider.txt` et videes dans `VF5RE/code_decompile`.
;
; ------------------------------------------------------------------------
; L'ORACLE, ET LA PREUVE QU'IL EST VIERGE
; ------------------------------------------------------------------------
;   SOURCES\APM3_US\runtime\media\vf5fs\vf5fs-pxd-w64-Retail_APM3.dll
;   md5 commence par 3214e19696de ; 6 965 248 octets ; AUCUNE section
;   `.decors`.
;
; Les deux autres copies du disque -- `FS APM3\banc_revo\...` et
; `VF5RE\runtime\media\vf5fs\...` -- font 7 181 824 octets et PORTENT
; `.decors` : ce sont les patchees, et elles n'ont pas servi.
;
; ------------------------------------------------------------------------
; LA METHODE, ET SON AUTO-TEST
; ------------------------------------------------------------------------
; Chaque page resout son titre par `MOV ECX,<id> ; CALL FUN_1802316E0`. Chez
; APM3 la meme page fait de meme avec l'identifiant JUSTE. On retrouve donc
; la page jumelle par son titre NON DECALE, puis on releve les
; `MOV r/m32, imm32` qui l'entourent : ce sont ses libelles.
;
; L'instrument a ete valide AVANT usage : la meme recherche, lancee sur REVO
; avec les identifiants decales, doit retrouver les quatre sites deja
; desassembles par Ghidra. Elle les retrouve tous les quatre
; (0x18020B109, 0x18020DDF1, 0x18020DAA6, 0x18020D77A). Un balayage d'octets
; n'est pas un decodage : sans cet auto-test le releve ne vaut rien.
;
; ------------------------------------------------------------------------
; REVO -- CE QU'IL ECRIT  (vf5fs-pxd-w64-d3d12_SteamRetail.dll, 7 229 952 o)
; ------------------------------------------------------------------------
;
; MENU PRINCIPAL -- FUN_18020C880
;
; +0x20CA46   B9 79 01 00 00                 MOV ECX, 0x179   ; en-tete
; +0x20C8F1   C7 45 A0 7A 01 00 00           MOV [RBP-0x60], 0x17A ; ligne 0
; +0x20C8F8   C7 45 A4 7B 01 00 00           MOV [RBP-0x5C], 0x17B ; ligne 1
; +0x20C8FF   C7 45 A8 7D 01 00 00           MOV [RBP-0x58], 0x17D ; ligne 2
; +0x20C906   C7 45 AC 7E 01 00 00           MOV [RBP-0x54], 0x17E ; ligne 3
; +0x20C90D   C7 45 B0 7F 01 00 00           MOV [RBP-0x50], 0x17F ; ligne 4
; +0x20C914   C7 45 B4 81 01 00 00           MOV [RBP-0x4C], 0x181 ; ligne 5
; +0x20C91B   C7 45 B8 82 01 00 00           MOV [RBP-0x48], 0x182 ; ligne 6
; +0x20C922   C7 45 BC 83 01 00 00           MOV [RBP-0x44], 0x183 ; ligne 7
; +0x20C929   BB 84 01 00 00                 MOV EBX, 0x184   ; ligne 8 demo
; +0x20C92E   C7 45 C4 86 01 00 00           MOV [RBP-0x3C], 0x186 ; ligne 9
; +0x20C935   E8 E6 F0 DF FF                 CALL 0x18000BA20
; +0x20C93A   B9 85 01 00 00                 MOV ECX, 0x185   ; ligne 8 complet
; +0x20C941   0F 44 D9                       CMOVZ EBX, ECX
;
;   LE COUPLE CONDITIONNEL. `FUN_18000BA20` est un bouchon `XOR AL,AL`, donc
;   ZF=1 et le CMOVZ prend TOUJOURS 0x185. L'ecran montre bien DOWNLOAD
;   CONTENT et jamais UNLOCK FULL GAME. Les DEUX branches ont ete corrigees,
;   et c'est la verification la plus forte du releve : une erreur de palier
;   aurait fait apparaitre un libelle incoherent sur l'une des deux.
;
; SINGLE PLAYER -- FUN_18020AFC0
;
; +0x20B109   B9 7A 01 00 00                 MOV ECX, 0x17A   ; en-tete
; +0x20B002   C7 44 24 40 A2 01 00 00        MOV [RSP+0x40], 0x1A2
; +0x20B00A   C7 44 24 44 A3 01 00 00        MOV [RSP+0x44], 0x1A3
; +0x20B012   C7 44 24 48 A4 01 00 00        MOV [RSP+0x48], 0x1A4
; +0x20B01A   C7 44 24 4C A5 01 00 00        MOV [RSP+0x4C], 0x1A5
;
; OFFLINE VERSUS -- FUN_18020DC80
;
; +0x20DDF1   B9 7B 01 00 00                 MOV ECX, 0x17B   ; en-tete
; +0x20DCC5   C7 45 A0 B1 01 00 00           MOV [RBP-0x60], 0x1B1
; +0x20DCCC   C7 45 A4 AD 01 00 00           MOV [RBP-0x5C], 0x1AD
; +0x20DCD3   C7 45 A8 CF 01 00 00           MOV [RBP-0x58], 0x1CF
; +0x20DCDA   C7 45 AC D4 01 00 00           MOV [RBP-0x54], 0x1D4
; +0x20DCE1   C7 45 B0 D9 01 00 00           MOV [RBP-0x50], 0x1D9
;
;   A RETENIR : ces cinq-la ne sont PAS consecutifs. Une page lit n'importe
;   ou dans la liste, donc on ne devine jamais le libelle suivant.
;
; DOJO -- FUN_18020D960
;
; +0x20DAA6   B9 7E 01 00 00                 MOV ECX, 0x17E   ; en-tete
; +0x20D9A7   C7 44 24 40 1B 02 00 00        MOV [RSP+0x40], 0x21B
; +0x20D9AF   C7 44 24 44 1C 02 00 00        MOV [RSP+0x44], 0x21C
; +0x20D9B7   C7 44 24 48 1D 02 00 00        MOV [RSP+0x48], 0x21D
;
; TERMINAL -- FUN_18020D640
;
; +0x20D77A   B9 7F 01 00 00                 MOV ECX, 0x17F   ; en-tete
; +0x20D682   C7 45 68 A1 02 00 00           MOV [RBP+0x68], 0x2A1
; +0x20D689   C7 45 6C A2 02 00 00           MOV [RBP+0x6C], 0x2A2
;
; ------------------------------------------------------------------------
; APM3 -- CE QUI EST JUSTE  (vf5fs-pxd-w64-Retail_APM3.dll, 6 965 248 o)
; ------------------------------------------------------------------------
;
; +0x1DF256   B9 77 01 00 00                 MOV ECX, 0x177  ; SINGLE PLAYER
; +0x1E2307   B9 78 01 00 00                 MOV ECX, 0x178  ; OFFLINE VERSUS
; +0x1E1F93   B9 7B 01 00 00                 MOV ECX, 0x17B  ; DOJO
; +0x1E1C51   B9 7C 01 00 00                 MOV ECX, 0x17C  ; TERMINAL
;
; +0x1E1E8A   C7 44 24 40 17 02 00 00        MOV [RSP+0x40], 0x217
;             C7 44 24 44 18 02 00 00        MOV [RSP+0x44], 0x218
;             C7 44 24 48 19 02 00 00        MOV [RSP+0x48], 0x219
;
;   Les trois lignes du DOJO d'APM3, octet pour octet dans la meme forme que
;   celles de REVO : seul l'immediat differe. C'est ce qui autorise une
;   substitution d'immediat sans toucher a l'encodage.
;
;   Les autres pages d'APM3 ont ete relevees par le meme outil, qui rend
;   leurs libelles autour de l'en-tete :
;     SINGLE PLAYER  0x19E 0x19F 0x1A0 0x1A1
;     OFFLINE VERSUS 0x1AD 0x1A9 0x1CB 0x1D0 0x1D5
;     DOJO           0x217 0x218 0x219
;     TERMINAL       0x299 0x29A
;
; ------------------------------------------------------------------------
; LA CONCLUSION : TROIS PALIERS, ET AUCUNE REGLE
; ------------------------------------------------------------------------
;
;   region                      | REVO ecrit                    | APM3        | ecart
;   ----------------------------|-------------------------------|-------------|------
;   menu principal 0x176..0x186 | 0x179 0x17A ... 0x186         | -3          | +3
;   en-tetes des quatre pages   | 0x17A 0x17B 0x17E 0x17F       | 0x177 0x178 0x17B 0x17C | +3
;   SINGLE PLAYER               | 0x1A2 0x1A3 0x1A4 0x1A5       | 0x19E..0x1A1| +4
;   OFFLINE VERSUS              | 0x1B1 0x1AD 0x1CF 0x1D4 0x1D9 | 0x1AD 0x1A9 0x1CB 0x1D0 0x1D5 | +4
;   DOJO                        | 0x21B 0x21C 0x21D             | 0x217..0x219| +4
;   TERMINAL                    | 0x2A1 0x2A2                   | 0x299 0x29A | +8
;   legendes 0x62..0x6E         | inchangees                    | identiques  | +0
;
; UN `-3` GENERAL EST FAUX, et c'est la mesure qui le dit, pas une intuition.
; Il aurait casse les trois pages a +4 et la page a +8. La raison en est
; simple : REVO a insere des entrees a PLUSIEURS endroits de sa liste, pas a
; un seul. Verifie aussi par l'autre bout au SS 419.92 : `FUN_18020D2F0`
; (0x1C1 0x1C2 0x1C3) donne << CLASS / HIGH SCORE / CLEAR >> TELLE QUELLE et
; du charabia a -3, et `FUN_18020D640` donnait a -3 deux LEGENDES DE BOUTON.
;
; ------------------------------------------------------------------------
; CE QUI EST POSE, ET CE QUI NE L'EST PAS
; ------------------------------------------------------------------------
; POSE. 12 immediats du menu principal (SS 419.90, `VF5_MENU_LIBELLES`) et 18
; des quatre pages filles (SS 419.94, `VF5_SOUSMENUS`), dans
; `FS REVO/host_revo/vf5fs_host.cpp`. Les deux fonctions verifient TOUS leurs
; sites -- lisibilite, prefixe, immediat attendu -- et refusent EN BLOC sans
; rien ecrire si un seul ne correspond pas. Ecriture en IMAGE CHARGEE
; seulement, avant `module_start` : le `.dll` du disque est intact, et ce
; releve-ci le prouve puisqu'il lit encore `A2 01`, `1B 02`, `A1 02`.
;
; VU A L'ECRAN par Frederic : le menu principal, MAIN MENU et ses dix lignes,
; avec DOWNLOAD CONTENT present et UNLOCK FULL GAME absent.
;
; NON CORRIGE, et ce n'est PAS un decalage :
;  - l'en-tete et la legende du menu PARENT ne sont pas effaces quand la page
;    fille s'ouvre ; << MAIN MENU >> transparait sous << SCOREBOARDS >> et
;    les deux legendes se superposent. C'est une destruction d'objets AET qui
;    manque, a traiter separement.
;  - trois pages soeurs lues mais laissees telles quelles, hors priorite :
;    FUN_18020CC90 (en-tete 0x17C, lignes 0x1DC 0x1DD 0x1DE),
;    FUN_18020CFB0 (la page REPLAYS : en-tete 0x2A2, lignes 0x2A3 0x2A4
;    0x2A5), FUN_1801B82D0 (l'en-tete HELP & OPTIONS, 0x183).
;  - 0x17C, l'en-tete de FUN_18020CC90, tombe ENTRE OFFLINE VERSUS (0x17B) et
;    ONLINE BATTLE (0x17D) : c'est une des entrees que REVO a inserees.
;
; ET UNE CONTRE-EPREUVE A NE PAS OUBLIER. `FUN_1801DBA00` ne grave AUCUN
; immediat de pile : elle POSTE ses identifiants (0x19D, 0x1A6, ...) a l'hote
; par le repartiteur `bloc+0x1FF08` avec la commande 0xC1 (193). Il existe
; donc DEUX facons pour une page de nommer son texte, et une correction
; d'immediats ne touche que la premiere. A relire avant de s'acharner sur une
; page qui resiste.
;
; ------------------------------------------------------------------------
; CE QUI REJOUE CE RELEVE
; ------------------------------------------------------------------------
; Les deux outils vivent dans le bac a sable de la seance et ne sont pas des
; outils du chantier ; ce fichier-ci EST le resultat. Pour le refaire :
; chercher `B9 <id juste>` dans le `.text` d'APM3, puis relever les
; `C7 /0 imm32` dans une fenetre de 0x300 octets autour -- et faire passer
; l'auto-test sur REVO AVANT de croire le resultat.
