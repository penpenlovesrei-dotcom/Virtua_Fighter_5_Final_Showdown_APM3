; =====================================================================
; LE CHARGEMENT 2D DU SELECTEUR DE PERSONNAGES  --  module de VF5 R.E.V.O.
; =====================================================================
;
; Binaire      : vf5fs-pxd-w64-d3d12_SteamRetail.dll  (module de REVO)
; Base d'image : 0x180000000  --  toutes les adresses ci-dessous sont des
;                RVA, donc VF5FS+0x..., jamais une adresse absolue.
; Outil        : VF5RE/plage_module.py  (capstone, operandes rip-relatifs
;                resolus) et une relecture directe du PE pour les tables.
; Releve du    : 2026-11-10, SS 419.136 / 419.137.
; Regenere par : py -3 <scratchpad>/faire_asm_chargeur2d.py
;                (chaque plage est RE-DEMANDEE a l'outil : rien n'est
;                 recopie a la main)
; Consigne dans: VF5RE/code_decompile/MENU.md section 419.137
;
; #####################################################################
; ## ERRATUM DU SS 419.139 -- A LIRE AVANT LE RESTE DE CE FICHIER
; #####################################################################
;
; La conclusion 2 ci-dessous -- << l'escalier de la phase 0 DECHARGE,
; c'est la demolition de l'ecran precedent >> -- est **FAUSSE**, et le
; relevé qui la refute est dans ce fichier meme, section E.
;
; CE QUI L'A REFUTEE : la POLARITE, lue sur l'epilogue au lieu d'etre
; supposee. Toutes les branches de l'escalier font `jne 0x17B208`, et
; 0x17B208 est l'EPILOGUE de la fonction :
;
;     0017AE7C  xor      bpl, bpl          ; bpl = 0, le registre zero
;       ...
;     0017B204  cmove    ebp, r13d         ; r13d = 1 : le SEUL chemin a 1
;     0017B208  movzx    eax, bpl          ; <-- l'epilogue rend bpl
;     0017B227  ret
;
; Donc `jne 0x17B208` veut dire **<< rends 0 >>**, et rendre 0 pour une
; methode de pas veut dire << pas fini, rappelle-moi a l'image suivante >>.
; Par consequent `0x196130` et `0x0262E0` rendent **non-zero tant que
; l'operation est EN COURS**, et l'escalier de la phase 0 est
; **L'ATTENTE DU CHARGEMENT**, pas une demolition.
;
; CE QUE CA CHANGE, ET C'EST LOURD :
;
;   * Le drapeau `+0xB8` mesure a 1 au SS 419.136 sur les six jeux du
;     selecteur ne veut pas dire << libere >> mais **<< chargement
;     TERMINE >>**, et `+0x20 = 2` veut dire deux elements tenus. L'art
;     du selecteur EST charge. SPR_S_WADV a `+0xB8 = 0` parce que l'art
;     du titre a depuis ete DECHARGE, ce qui est normal au selecteur.
;
;   * L'absence de lecture de fichier dans le journal n'est donc PAS une
;     anomalie : les donnees 2D viennent d'une FENETRE dans
;     vf5fs_data.par, pas d'un open() par fichier (SS 372). Le journal
;     n'avait aucune raison de montrer spr_s_selcha.farc.
;
;   * La cause de l'ecran vide est AILLEURS, et la section E la nomme :
;     la DOUBLE PORTE `[sel+0x5d]` / `[sel+0x5e]`.
;
; Ce que j'avais mal lu : `0x278BC0` libere bien quatre blocs et met
; `[req+0x70]` a zero -- mais il est appele **a la FIN** de l'operation,
; pour rendre le brouillon de la requete, et non au DEBUT pour defaire un
; chargement. Les sections B et C de ce fichier restent justes comme
; relevé d'instructions ; seuls les NOMS << dechargement >> qu'elles
; portent sont a lire comme << attente et finalisation >>.
;
; [[le-titre-d-une-fiche-porte-la-conclusion]] : ce fichier avait un
; titre juste et une conclusion inversee.
;
; ---------------------------------------------------------------------
; LE SUJET, ET LA CONCLUSION QU'IL PORTE
; ---------------------------------------------------------------------
;
; L'art du selecteur de personnages n'est JAMAIS lu : aucun des cinq
; fichiers (spr_s_selcha.farc, aet_s_selcha.bin, spr_s_selcmn.farc,
; spr_c_chara.farc, aet_c_chara.bin) n'apparait dans les 60 lectures
; d'une course, sur 428 images passees dans le sous-etat 19=SELECTOR.
; Les fichiers sont intacts dans l'archive de 3,7 Go -- c'est la LECTURE
; qui manque.
;
; Ce fichier porte trois conclusions, dans cet ordre :
;
;   1. CHARGER ET DECHARGER SONT DEUX FONCTIONS JUMELLES, rangees cote a
;      cote. Celle qui passe le NOM est le chargeur :
;
;          charger          decharger
;          sprites : 0x1960A0        0x196130  (-> 0x19BE10)
;          AET     : 0x026180        0x0262E0  (-> 0x024880)
;
;   2. L'<< ESCALIER >> DU SELECTEUR N'APPELLE QUE DES DECHARGEURS.
;      C'est la DEMOLITION de l'ecran precedent, pas un chargement.
;      `test al,al ; jne 0x17B208` veut dire << il reste quelque chose a
;      liberer, reviens a l'image suivante >>. Il a fonctionne.
;      J'ai appele cette fonction << l'escalier de chargement >> du
;      SS 419.131 au SS 419.136 : le nom etait FAUX et il m'a envoye
;      sonder le chargeur pendant six sections.
;
;   3. LE SEUL SITE QUI CHARGE L'ART EST 0x17B850, ET IL NE TOURNE
;      JAMAIS. Il est le creneau +0x08 d'une table virtuelle dont le
;      creneau +0x10 -- le pas -- est, lui, bien appele. Et dedans,
;      `bloc+0x1FF08` (NOTRE repartiteur) choisit : NUL -> il charge son
;      art ; POSE -> il delegue par la commande 4 et joue un film de
;      borne. C'est le motif +0x1FF08 pour la TROISIEME fois, apres
;      CS_TITLE et le menu.
;
; MESURE a l'appui (journal host_log_419_136_le_drapeau_est_pose_sans_
; lecture.txt, releve pose a l'image 700, sous-etat 19=SELECTOR) :
;
;     sprites [0x75E018] -> chargeur [0x75E010], recherche VF5FS+0x198810
;       0x026 cle 0x1FD "SPR_S_SELCMN"   nb[+0x20]=1  relache[+0xB8]=1
;       0x15E cle 0x21A "SPR_S_VSELCMN"  nb[+0x20]=0  relache[+0xB8]=0
;       0x161 cle 0x21D "SPR_S_WSELCMN"  nb[+0x20]=1  relache[+0xB8]=1
;       0x144 cle 0x1FC "SPR_S_SELCHA"   nb[+0x20]=2  relache[+0xB8]=1
;       0x15F cle 0x21B "SPR_S_WADV"     nb[+0x20]=0  relache[+0xB8]=0  <- TEMOIN
;     AET [0x6AF3B8] -> chargeur [0x6AF3D0], recherche VF5FS+0x1FD20
;       0x112 cle 0x1B4 "AET_S_SELCHA"   [+0xB0]=1
;       0x12E cle 0x1D3 "AET_S_WADV"     [+0xB0]=0                      <- TEMOIN
;
; Le temoin est l'art de l'ECRAN-TITRE, dont la lecture est mesuree a
; l'image 307. Son drapeau est a ZERO et ceux du selecteur a UN : c'est
; lui qui a renverse la lecture. Sans temoin, je concluais l'inverse.
;
; RIEN ICI N'EST DU CODE A COMPILER NI A RECOPIER DANS L'HOTE. Ce sont
; des lectures, gardees pour ne pas les refaire. Le PE n'est ni charge
; ni execute : on lit le fichier.
;

; ######################################################################
; ## A. LE SELECTEUR : SON AIGUILLAGE PAR PHASE, ET SA DEMOLITION
; ######################################################################
;
; 0x17AE88 est un CORPS CHAINE (drapeau 0x4 de .pdata) de la fonction
; mere 0x17AE30 : borner par .pdata rend la mere seule et rate ce corps
; ([[balayer-pdata-n-est-pas-balayer-le-code]]). La plage est donc DITE.
;
; Les quatre premieres instructions sauvegardent des registres, puis
; l'aiguillage :
;     mov ecx,[rdx + rax*4 + 0x17B228] ; add rcx,rdx ; jmp rcx
; avec rdx = VF5FS+0x0 (pose par le `lea rdx,[rip-0x17AE94]`) et rax =
; la PHASE. Les entrees de la table sont donc des RVA sur 32 bits.
;
; `cmp byte ptr [rax+0x20], bpl` et `cmp byte ptr [rdi+0x63], bpl` :
; `bpl` est l'octet bas de rbp, qui sert de registre ZERO sur ce chemin.
; Ce sont donc des comparaisons a 0.
;
; LA POLARITE, qui decide de tout : `test al,al ; jne 0x17B208` saute
; vers la SORTIE quand al est NON NUL. Donc
;     al != 0  ->  << pas fini, reviens a l'image suivante >>
;     al == 0  ->  << c'est libere, continue >>
;
; 0x17AF26 : `cmp byte [rdi+0x63], bpl` -- et c'est 0x17B850 qui POSE
; cet octet, a `(bloc+0x1FF08) != 0`. Les deux fonctions sont liees par
; ce seul octet. Avec le repartiteur retire, l'octet est nul et la
; demolition relache 0x144/0x112 elle-meme ; avec le repartiteur pose,
; elle demande a l'hote par `edx = 5` (commande 5), que nos journaux
; n'ont JAMAIS vue.
;
--- VF5FS+0x17AE88 .. +0x17AFE0  (344 octets), plage DITE
  0017AE88  mov      qword ptr [rsp + 0x58], r13             
  0017AE8D  lea      rdx, [rip - 0x17ae94]                      ; VF5FS+0x0
  0017AE94  mov      qword ptr [rsp + 0x88], rbx             
  0017AE9C  mov      r13d, 1                                 
  0017AEA2  mov      qword ptr [rsp + 0x90], rsi             
  0017AEAA  mov      ecx, dword ptr [rdx + rax*4 + 0x17b228] 
  0017AEB1  add      rcx, rdx                                
  0017AEB4  jmp      rcx                                     
  0017AEB6  mov      ecx, 0x26                               
  0017AEBB  mov      byte ptr [rdi + 0x5c], r13b             
  0017AEBF  call     0x180196130                                -> VF5FS+0x196130
  0017AEC4  test     al, al                                  
  0017AEC6  jne      0x18017b208                                -> VF5FS+0x17B208
  0017AECC  mov      ecx, 0x113                              
  0017AED1  call     0x1800262e0                                -> VF5FS+0x262E0
  0017AED6  test     al, al                                  
  0017AED8  jne      0x18017b208                                -> VF5FS+0x17B208
  0017AEDE  call     0x180179e70                                -> VF5FS+0x179E70
  0017AEE3  cmp      byte ptr [rax + 0x20], bpl              
  0017AEE7  je       0x18017af02                                -> VF5FS+0x17AF02
  0017AEE9  mov      ecx, 0x161                              
  0017AEEE  call     0x180196130                                -> VF5FS+0x196130
  0017AEF3  test     al, al                                  
  0017AEF5  jne      0x18017b208                                -> VF5FS+0x17B208
  0017AEFB  mov      ecx, 0x130                              
  0017AF00  jmp      0x18017af19                                -> VF5FS+0x17AF19
  0017AF02  mov      ecx, 0x15e                              
  0017AF07  call     0x180196130                                -> VF5FS+0x196130
  0017AF0C  test     al, al                                  
  0017AF0E  jne      0x18017b208                                -> VF5FS+0x17B208
  0017AF14  mov      ecx, 0x12d                              
  0017AF19  call     0x1800262e0                                -> VF5FS+0x262E0
  0017AF1E  test     al, al                                  
  0017AF20  jne      0x18017b208                                -> VF5FS+0x17B208
  0017AF26  cmp      byte ptr [rdi + 0x63], bpl              
  0017AF2A  je       0x18017af71                                -> VF5FS+0x17AF71
  0017AF2C  mov      rcx, qword ptr [rip + 0xb12ff5]            ; VF5FS+0xC8DF28
  0017AF33  mov      byte ptr [rsp + 0x80], bpl              
  0017AF3B  mov      rax, qword ptr [rcx + 0x1ff08]          
  0017AF42  test     rax, rax                                
  0017AF45  je       0x18017b208                                -> VF5FS+0x17B208
  0017AF4B  mov      rcx, qword ptr [rcx + 0x1ff10]          
  0017AF52  lea      r8, [rsp + 0x80]                        
  0017AF5A  mov      edx, 5                                  
  0017AF5F  call     rax                                     
  0017AF61  cmp      byte ptr [rsp + 0x80], bpl              
  0017AF69  je       0x18017b208                                -> VF5FS+0x17B208
  0017AF6F  jmp      0x18017af95                                -> VF5FS+0x17AF95
  0017AF71  mov      ecx, 0x144                              
  0017AF76  call     0x180196130                                -> VF5FS+0x196130
  0017AF7B  test     al, al                                  
  0017AF7D  jne      0x18017b208                                -> VF5FS+0x17B208
  0017AF83  mov      ecx, 0x112                              
  0017AF88  call     0x1800262e0                                -> VF5FS+0x262E0
  0017AF8D  test     al, al                                  
  0017AF8F  jne      0x18017b208                                -> VF5FS+0x17B208
  0017AF95  call     0x1801aa3b0                                -> VF5FS+0x1AA3B0
  0017AF9A  call     0x18021f0f0                                -> VF5FS+0x21F0F0
  0017AF9F  call     0x180195090                                -> VF5FS+0x195090
  0017AFA4  mov      dword ptr [rdi + 0x58], r13d            
  0017AFA8  mov      byte ptr [rdi + 0x5c], r13b             
  0017AFAC  lea      rdx, [rip + 0x2ad2ed]                      ; VF5FS+0x4282A0  "SEL_COMMON"
  0017AFB3  mov      rcx, qword ptr [rip + 0x2adea6]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017AFBA  call     0x1802cd400                                -> VF5FS+0x2CD400
  0017AFBF  mov      dword ptr [rdi + 0x58], 2               
  0017AFC6  mov      rcx, rdi                                
  0017AFC9  mov      byte ptr [rdi + 0x5c], r13b             
  0017AFCD  call     0x18017b280                                -> VF5FS+0x17B280
  0017AFD2  test     al, al                                  
  0017AFD4  je       0x18017b208                                -> VF5FS+0x17B208
  0017AFDA  mov      esi, 7                                  

; ----------------------------------------------------------------------
; LA TABLE DE SAUTS PAR PHASE, a VF5FS+0x17B228
; ----------------------------------------------------------------------
; Relue directement dans le PE (dwords = RVA). Elle dit que la
; phase 0 est L'ATTENTE DU CHARGEMENT (voir l'erratum 419.139), que la
; DEMOLITION est la phase 12, et que 0x17B850 n'y est PAS : le chargeur
; n'est pas une phase de cette fonction, c'est un autre creneau virtuel.
;
;
; CORRIGE AU SS 419.144 : **la table a VINGT entrees, pas quatorze.** Les
; dwords relus dans le PE (VF5RE/octets_module.py 0x17B228 96) donnent, puis
; du remplissage 0xCC :
;
;     phase  0  ->  VF5FS+0x17AEB6      phase 12..16 ->  VF5FS+0x17B19A
;     phase  1  ->  VF5FS+0x17AFA8      phase 17     ->  VF5FS+0x17B1A5
;     phase  2..6 ->  VF5FS+0x17AFC6    phase 18     ->  VF5FS+0x17B1D1
;     phase  7..11 ->  VF5FS+0x17B18A   phase 19     ->  VF5FS+0x17B0CD
;
; CE QUE MA PREMIERE LECTURE AVAIT FAUX, ET C'EST LOURD : j'avais attribue
; `0x17B0CD` -- le bloc qui monte `chara_start`, `loop_start`, `loop_end` et
; `bg_light_change` -- aux phases 7 a 11. **Il est a la phase 19**, que
; `0x17B077` pose, c'est-a-dire APRES la double porte et APRES que
; `[sel+0x61]` soit pose par `0x17B280`. Ces animations appartiennent donc a
; la SORTIE VERS LE MATCH, pas a l'entree dans le selecteur. J'avais compte
; quatorze entrees parce que je m'etais arrete a la derniere qui me servait
; ([[compter-avant-d-annoncer-un-nombre]]).
;

; ----------------------------------------------------------------------
; LA TABLE VIRTUELLE DU SELECTEUR, a VF5FS+0x428210
; ----------------------------------------------------------------------
; Trouvee en cherchant le QWORD 0x18017B850 dans le fichier : un seul
; pointeur, en .rdata a VF5FS+0x428268. Celui de 0x17AE30 est juste a
; cote, en +0x428270. 0x17B280 (la phase 2 / SEL_CHARA) n'a AUCUN
; pointeur : il est atteint par du code, pas par une table.
;
; L'objet a DEUX bases : +0x428210 et +0x428258 portent des valeurs de
; .data (0x5E8848 et 0x5E88D0) qui sont les localisateurs RTTI que MSVC
; range en vtable[-1]. La SECONDE table commence donc en +0x428260, et
; les creneaux qui nous occupent y sont a +0x08 et +0x10.
;
;     +0x428210 : VF5FS+0x5E8848
;     +0x428218 : VF5FS+0x17ABE0
;     +0x428220 : VF5FS+0x17E9D0
;     +0x428228 : VF5FS+0x17C1E0
;     +0x428230 : VF5FS+0x17D750
;     +0x428238 : VF5FS+0x17D820
;     +0x428240 : VF5FS+0x00AF60
;     +0x428248 : VF5FS+0x00AF60
;     +0x428250 : VF5FS+0x00AF70
;     +0x428258 : VF5FS+0x5E88D0   <-- RTTI de la 2e base ; la table commence APRES
;     +0x428260 : VF5FS+0x17ACB0   <-- 2e table +0x00
;     +0x428268 : VF5FS+0x17B850   <-- 2e table +0x08 : LE CHARGEUR 2D
;     +0x428270 : VF5FS+0x17AE30   <-- 2e table +0x10 : LE PAS (attente en phase 0)
;     +0x428278 : VF5FS+0x17B6A0   <-- 2e table +0x18
;     +0x428280 : VF5FS+0x17B7A0   <-- 2e table +0x20
;     +0x428288 : VF5FS+0x00AF60

; ######################################################################
; ## B. ATTENDRE ET FINALISER : LA CHAINE COMPLETE, DES DEUX COTES
; ##    (lue au 419.137 comme << decharger >> -- voir l'erratum)
; ######################################################################
;
; Ce que l'escalier appelle. Les deux cotes ont la meme forme : une
; recherche dans le REGISTRE (identifiant -> entree), puis une demande
; au CHARGEUR avec la CLE prise en `entree+0x18` du resultat.
;
; ATTENTION A L'OFFSET DE LA CLE. `FUN_180020520` (et son homologue
; sprite 0x199220) rend `entree + 0x08` -- `piVar3 + 2` sur un `int *`
; dans la decompilation -- et l'appelant lit `+0x18` de CE resultat. Le
; champ reellement passe est donc **entree + 0x20**, pas +0x18. C'est la
; correction du SS 419.133 : j'avais imprime +0x18 pendant une seance,
; un champ qui rend une valeur dans l'image du module pour TOUTES les
; entrees et ne distingue donc rien.
;
; ----------------------------------------------------------------------
; B.1  cote SPRITE : 0x196130, le point d'entree du dechargement
; ----------------------------------------------------------------------
--- VF5FS+0x196130 .. +0x196155  (37 octets), plage DITE
  00196130  sub      rsp, 0x28                               
  00196134  mov      edx, ecx                                
  00196136  mov      rcx, qword ptr [rip + 0x5c7edb]            ; VF5FS+0x75E018
  0019613D  call     0x180199220                                -> VF5FS+0x199220
  00196142  mov      rcx, qword ptr [rip + 0x5c7ec7]            ; VF5FS+0x75E010
  00196149  mov      edx, dword ptr [rax + 0x18]             
  0019614C  add      rsp, 0x28                               
  00196150  jmp      0x18019be10                                -> VF5FS+0x19BE10

; ----------------------------------------------------------------------
; B.2  cote SPRITE : 0x19BE10 EN ENTIER -- et c'est lui qui prouve que
;      ces fonctions DECHARGENT
; ----------------------------------------------------------------------
; Lu de bout en bout :
;
;     rax = 0x198810(chargeur, cle)          ; l'objet de CE jeu
;     cmp byte [rax+0xB8],0 ; je  0x19BE2F
;        si != 0 : xor al,al ; ret            (a) DEJA RELACHE -> << fini >>
;     rcx = rax+0x28 ; call 0x278E30
;     test al,al ; jne 0x19BE85
;        si != 0 : mov al,1 ; ret                 OCCUPE -> << pas fini >>
;     cmp dword [rbx+0x20],0 ; jne 0x19BE52
;        si == 0 : ret (al vaut 0)            (b) RIEN A RELACHER -> << fini >>
;     [rbx+0xC8] != 0 -> 0x2796A0(1, [rbx+0xC8]) ; [rbx+0xC8] = 0
;     0x278BC0(rbx+0x28, 1)                   ; LE RESET (voir section C)
;     mov byte [rbx+0xB8], 1                  ; marque RELACHE
;     mov al,1 ; ret                          ; << pas fini, reviens >>
;
; Donc `+0xB8 = 1` veut dire RELACHE, et `+0x20` est le nombre
; d'elements encore detenus. La requete du jeu est en `objet + 0x28` :
; c'est LU, pas suppose -- `lea rcx,[rax+0x28]` en 0x19BE2F avant
; 0x278E30, et `lea rcx,[rbx+0x28]` en 0x19BE75 avant 0x278BC0.
;
--- VF5FS+0x19BE10 .. +0x19BE95  (133 octets), plage DITE
  0019BE10  push     rbx                                     
  0019BE12  sub      rsp, 0x20                               
  0019BE16  call     0x180198810                                -> VF5FS+0x198810
  0019BE1B  mov      rbx, rax                                
  0019BE1E  cmp      byte ptr [rax + 0xb8], 0                
  0019BE25  je       0x18019be2f                                -> VF5FS+0x19BE2F
  0019BE27  xor      al, al                                  
  0019BE29  add      rsp, 0x20                               
  0019BE2D  pop      rbx                                     
  0019BE2E  ret                                              
  0019BE2F  lea      rcx, [rax + 0x28]                       
  0019BE33  mov      qword ptr [rsp + 0x30], rdi             
  0019BE38  call     0x180278e30                                -> VF5FS+0x278E30
  0019BE3D  test     al, al                                  
  0019BE3F  jne      0x18019be85                                -> VF5FS+0x19BE85
  0019BE41  cmp      dword ptr [rbx + 0x20], 0               
  0019BE45  jne      0x18019be52                                -> VF5FS+0x19BE52
  0019BE47  mov      rdi, qword ptr [rsp + 0x30]             
  0019BE4C  add      rsp, 0x20                               
  0019BE50  pop      rbx                                     
  0019BE51  ret                                              
  0019BE52  mov      rdx, qword ptr [rbx + 0xc8]             
  0019BE59  test     rdx, rdx                                
  0019BE5C  je       0x18019be73                                -> VF5FS+0x19BE73
  0019BE5E  mov      ecx, 1                                  
  0019BE63  call     0x1802796a0                                -> VF5FS+0x2796A0
  0019BE68  mov      qword ptr [rbx + 0xc8], 0               
  0019BE73  mov      dl, 1                                   
  0019BE75  lea      rcx, [rbx + 0x28]                       
  0019BE79  call     0x180278bc0                                -> VF5FS+0x278BC0
  0019BE7E  mov      byte ptr [rbx + 0xb8], 1                
  0019BE85  mov      rdi, qword ptr [rsp + 0x30]             
  0019BE8A  mov      al, 1                                   
  0019BE8C  add      rsp, 0x20                               
  0019BE90  pop      rbx                                     
  0019BE91  ret                                              
  0019BE92  int3                                             
  0019BE93  int3                                             
  0019BE94  int3                                             

; ----------------------------------------------------------------------
; B.3  cote SPRITE : 0x198810, la recherche << cle -> objet >>
; ----------------------------------------------------------------------
; Un parcours d'ARBRE : racine en `[chargeur]`, cle 32 bits comparee a
; `[noeud+0x10]`, saut de noeud par `movsx rdx, word [rax+0x0E]`, et la
; charge utile rendue en `noeud + 0x18`.
;
; La queue en 0x1988EC est le cas RACINE NULLE :
;     mov rdx,rbx ; test rdx,rdx ; lea rax,[rdx+0x18] ; cmove rax,rbx
; avec rbx mis a zero en 0x19882A. Donc un arbre vide fait rendre NUL,
; et l'appelant deref `[rax+0xB8]` : il FAUTERAIT. Comme la course ne
; faute pas, l'objet existe pour les dix cles relevees -- l'arbre est
; monte. C'est ce qui rend le releve de la section A exploitable.
;
--- VF5FS+0x198810 .. +0x198920  (272 octets), plage DITE
  00198810  mov      qword ptr [rsp + 8], rbx                
  00198815  mov      qword ptr [rsp + 0x10], rsi             
  0019881A  push     rdi                                     
  0019881B  sub      rsp, 0x1b0                              
  00198822  mov      rax, qword ptr [rcx]                    
  00198825  lea      r9, [rsp + 0x10]                        
  0019882A  xor      ebx, ebx                                
  0019882C  mov      qword ptr [rsp], r9                     
  00198830  mov      qword ptr [rsp + 8], 0x18               
  00198839  mov      r10d, edx                               
  0019883C  mov      r11, rcx                                
  0019883F  mov      r8d, ebx                                
  00198842  test     rax, rax                                
  00198845  je       0x1801988ec                                -> VF5FS+0x1988EC
  0019884B  movabs   rdi, 0xffff000000000000                 
  00198855  nop      word ptr [rax + rax]                    
  00198860  movsx    rdx, word ptr [rax + 0xe]               
  00198865  add      rdx, rax                                
  00198868  cmp      dword ptr [rdx + 0x10], r10d            
  0019886C  jbe      0x1801988a3                                -> VF5FS+0x1988A3
  0019886E  mov      ecx, r8d                                
  00198871  lea      rdx, [r9 + rcx*8]                       
  00198875  test     rdx, rdx                                
  00198878  je       0x180198896                                -> VF5FS+0x198896
  0019887A  mov      rcx, rax                                
  0019887D  xor      rcx, qword ptr [rdx]                    
  00198880  and      rcx, rdi                                
  00198883  xor      rcx, rax                                
  00198886  mov      qword ptr [rdx], rcx                    
  00198889  mov      word ptr [rdx + 6], bx                  
  0019888D  mov      r8d, dword ptr [rsp + 0xc]              
  00198892  mov      r9, qword ptr [rsp]                     
  00198896  inc      r8d                                     
  00198899  mov      dword ptr [rsp + 0xc], r8d              
  0019889E  mov      rax, qword ptr [rax]                    
  001988A1  jmp      0x1801988db                                -> VF5FS+0x1988DB
  001988A3  jae      0x18019890f                                -> VF5FS+0x19890F
  001988A5  mov      ecx, r8d                                
  001988A8  lea      rdx, [r9 + rcx*8]                       
  001988AC  test     rdx, rdx                                
  001988AF  je       0x1801988cf                                -> VF5FS+0x1988CF
  001988B1  mov      rcx, rax                                
  001988B4  xor      rcx, qword ptr [rdx]                    
  001988B7  and      rcx, rdi                                
  001988BA  xor      rcx, rax                                
  001988BD  mov      qword ptr [rdx], rcx                    
  001988C0  mov      word ptr [rdx + 6], 1                   
  001988C6  mov      r8d, dword ptr [rsp + 0xc]              
  001988CB  mov      r9, qword ptr [rsp]                     
  001988CF  inc      r8d                                     
  001988D2  mov      dword ptr [rsp + 0xc], r8d              
  001988D7  mov      rax, qword ptr [rax + 8]                
  001988DB  shl      rax, 0x10                               
  001988DF  sar      rax, 0x10                               
  001988E3  test     rax, rax                                
  001988E6  jne      0x180198860                                -> VF5FS+0x198860
  001988EC  mov      rdx, rbx                                
  001988EF  lea      r11, [rsp + 0x1b0]                      
  001988F7  test     rdx, rdx                                
  001988FA  mov      rsi, qword ptr [r11 + 0x18]             
  001988FE  lea      rax, [rdx + 0x18]                       
  00198902  cmove    rax, rbx                                
  00198906  mov      rbx, qword ptr [r11 + 0x10]             
  0019890A  mov      rsp, r11                                
  0019890D  pop      rdi                                     
  0019890E  ret                                              
  0019890F  mov      qword ptr [rsp + 0xd0], rdx             
  00198917  lea      r10, [rsp + 0xf0]                       

; ----------------------------------------------------------------------
; B.4  cote AET : 0x0262E0, le point d'entree du dechargement
; ----------------------------------------------------------------------
; Meme forme qu'au sprite, avec le registre AET en [0x6AF3B8] et le
; chargeur AET en [0x6AF3D0]. Deux sauts terminaux de suite.
;
--- VF5FS+0x262E0 .. +0x26305  (37 octets), plage DITE
  000262E0  sub      rsp, 0x28                               
  000262E4  mov      edx, ecx                                
  000262E6  mov      rcx, qword ptr [rip + 0x6890cb]            ; VF5FS+0x6AF3B8  .data+0x6AF3B8
  000262ED  call     0x180020520                                -> VF5FS+0x20520
  000262F2  mov      rcx, qword ptr [rip + 0x6890d7]            ; VF5FS+0x6AF3D0  .data+0x6AF3D0
  000262F9  mov      edx, dword ptr [rax + 0x18]             
  000262FC  add      rsp, 0x28                               
  00026300  jmp      0x180024880                                -> VF5FS+0x24880

; ----------------------------------------------------------------------
; B.5  cote AET : 0x024880 -- un saut par TABLE VIRTUELLE
; ----------------------------------------------------------------------
;     sub rsp,0x28
;     call 0x1FD20          ; rcx/rdx sont passes TELS QUELS (la recherche)
;     mov rcx,[rax]         ; la table virtuelle de l'objet rendu
;     mov rdx,[rcx+0x10]    ; la methode +0x10
;     mov rcx,rax           ; this = l'objet
;     jmp rdx               ; -> methode(this), UN SEUL argument
;
; Donc la cle ne sert QU'A la recherche, et la methode ne recoit que
; l'objet -- exactement comme au sprite, ou 0x19BE10 n'utilise rdx que
; pour 0x198810.
;
; CE QUI N'EST PAS LU : cette methode +0x10. Je ne l'ai jamais
; desassemblee, et je ne sais donc PAS si la disposition de l'objet AET
; est celle du sprite. C'est pourquoi le releve du SS 419.137 imprime
; la table virtuelle de l'objet et sa case +0x10 en VF5FS+0x..., pour
; la faire NOMMER par la mesure au lieu de deviner un offset.
;
--- VF5FS+0x24880 .. +0x24899  (25 octets), plage DITE
  00024880  sub      rsp, 0x28                               
  00024884  call     0x18001fd20                                -> VF5FS+0x1FD20
  00024889  mov      rcx, qword ptr [rax]                    
  0002488C  mov      rdx, qword ptr [rcx + 0x10]             
  00024890  mov      rcx, rax                                
  00024893  add      rsp, 0x28                               

; ----------------------------------------------------------------------
; B.6  la fonction VOISINE, 0x0248A0 -- NON CONFIRMEE comme etant la
;      methode +0x10 ci-dessus
; ----------------------------------------------------------------------
; Elle suit 0x024880 apres un bourrage d'int3, et elle a la MEME forme
; que 0x19BE10 : un drapeau en `+0xB0` (et non +0xB8), la requete en
; `rcx+0x20` (et non +0x28), 0x278E30 pour << est-ce occupe >>, puis un
; appel virtuel `[rax+0x20]` et `mov byte [rbx+0xB0],1`.
;
; La ressemblance est forte, mais je n'ai PAS etabli que c'est la cible
; du `jmp rdx` de 0x024880 : une forme voisine n'est pas une preuve
; d'identite. Elle est gardee ici comme CANDIDATE, a confirmer par la
; mesure (le creneau +0x10 imprime par le releve).
;
--- VF5FS+0x2488A0 .. +0x2488E3  (67 octets), plage DITE
  002488A0  or       al, 0xba                                
  002488A2  int1                                             
  002488A3  call     qword ptr [rax + 0x244c8b48]            
  002488A9  test     rcx, rcx                                
  002488AD  je       0x1802488ba                                -> VF5FS+0x2488BA
  002488AF  xor      edx, edx                                
  002488B1  mov      ecx, dword ptr [rcx + 0x14]             
  002488B4  call     0x180026200                                -> VF5FS+0x26200
  002488B9  nop                                              
  002488BA  vmovsd   xmm0, qword ptr [rsi + 0x40]            
  002488BF  mov      eax, dword ptr [rsi + 0x48]             
  002488C2  mov      dword ptr [rsp + 0x38], eax             
  002488C6  vmovsd   qword ptr [rsp + 0x30], xmm0            
  002488CC  vaddss   xmm0, xmm0, xmm6                        
  002488D0  vmovss   dword ptr [rsp + 0x30], xmm0            
  002488D6  vmovss   xmm1, dword ptr [rsp + 0x34]            

; ----------------------------------------------------------------------
; B.7  cote AET : 0x01FD20, la recherche << cle -> objet >>, et sa queue
; ----------------------------------------------------------------------
; Meme arbre qu'au sprite, a une difference : la racine est en
; `[chargeur + 0x58]` et non `[chargeur]`.
;
--- VF5FS+0x1FD20 .. +0x1FD70  (80 octets), plage DITE
  0001FD20  mov      qword ptr [rsp + 8], rbx                
  0001FD25  mov      qword ptr [rsp + 0x10], rsi             
  0001FD2A  push     rdi                                     
  0001FD2B  sub      rsp, 0x1b0                              
  0001FD32  mov      rax, qword ptr [rcx + 0x58]             
  0001FD36  lea      r11, [rcx + 0x58]                       
  0001FD3A  xor      ebx, ebx                                
  0001FD3C  mov      qword ptr [rsp + 8], 0x18               
  0001FD45  lea      r9, [rsp + 0x10]                        
  0001FD4A  mov      r10d, edx                               
  0001FD4D  mov      qword ptr [rsp], r9                     
  0001FD51  mov      r8d, ebx                                
  0001FD54  test     rax, rax                                
  0001FD57  je       0x18001fdfc                                -> VF5FS+0x1FDFC
  0001FD5D  movabs   rdi, 0xffff000000000000                 
  0001FD67  nop      word ptr [rax + rax]                    
;
; ... et la queue, le cas RACINE NULLE :
;
--- VF5FS+0x1FDFC .. +0x1FE20  (36 octets), plage DITE
  0001FDFC  mov      rdx, rbx                                
  0001FDFF  lea      r11, [rsp + 0x1b0]                      
  0001FE07  test     rdx, rdx                                
  0001FE0A  mov      rsi, qword ptr [r11 + 0x18]             
  0001FE0E  lea      rax, [rdx + 0x18]                       
  0001FE12  cmove    rax, rbx                                
  0001FE16  mov      rbx, qword ptr [r11 + 0x10]             
  0001FE1A  mov      rsp, r11                                
  0001FE1D  pop      rdi                                     
  0001FE1E  ret                                              

; ######################################################################
; ## C. LA REQUETE : SON ETAT, ET LE << LANCEMENT >> QUI EST UN RESET
; ######################################################################
;
; C'est ici que je m'etais trompe. J'ai lu 0x278BC0 comme un LANCEMENT
; de chargement, et j'en ai conclu que l'escalier chargeait. Ses deux
; etapes LIBERENT.
;
; ----------------------------------------------------------------------
; C.1  0x278E30 : << cette requete est-elle occupee ? >>
; ----------------------------------------------------------------------
;     r8d = [req+0x08]                  ; l'ETAT de la requete
;     etat 0        -> al = 0           ; INERTE, jamais armee
;     etat 5 ou 6   -> al = 0           ; FINIE  (lea edx,[r8-5] ; cmp 1 ; jbe)
;     etat 0xF      -> al = 0           ; si [req+0x88] != 0
;     sinon         -> al = 1           ; EN VOL
;
--- VF5FS+0x278E30 .. +0x278E57  (39 octets), plage DITE
  00278E30  mov      r8d, dword ptr [rcx + 8]                
  00278E34  test     r8d, r8d                                
  00278E37  je       0x180278e54                                -> VF5FS+0x278E54
  00278E39  lea      edx, [r8 - 5]                           
  00278E3D  cmp      edx, 1                                  
  00278E40  jbe      0x180278e54                                -> VF5FS+0x278E54
  00278E42  cmp      byte ptr [rcx + 0x88], 0                
  00278E49  je       0x180278e51                                -> VF5FS+0x278E51
  00278E4B  cmp      r8d, 0xf                                
  00278E4F  je       0x180278e54                                -> VF5FS+0x278E54
  00278E51  mov      al, 1                                   
  00278E53  ret                                              
  00278E54  xor      al, al                                  
  00278E56  ret                                              

; ----------------------------------------------------------------------
; C.2  0x278C00 : ou sont les donnees -- et ce que l'etat 5 veut dire
; ----------------------------------------------------------------------
;     if ([req+0x08] == 5) return [req+0x70];  else return 0;
; Donc `[req+0x08] == 5` veut dire LES DONNEES SONT LA, en `[req+0x70]`.
; Trois valeurs separent tout : 0 = jamais armee, 5 = donnees presentes,
; autre = en vol.
;
--- VF5FS+0x278C00 .. +0x278C0E  (14 octets), plage DITE
  00278C00  cmp      dword ptr [rcx + 8], 5                  
  00278C04  jne      0x180278c0b                                -> VF5FS+0x278C0B
  00278C06  mov      rax, qword ptr [rcx + 0x70]             
  00278C0A  ret                                              
  00278C0B  xor      eax, eax                                
  00278C0D  ret                                              

; ----------------------------------------------------------------------
; C.3  0x278BC0 : LE RESET -- ce que j'avais pris pour un lancement
; ----------------------------------------------------------------------
;     edi = dl ; rbx = rcx
;     call 0x277E00          ; etape 1
;     rcx = rbx ; call 0x277EB0   ; etape 2
;     if (dl != 0) call 0x277BE0
;
--- VF5FS+0x278BC0 .. +0x278BF2  (50 octets), plage DITE
  00278BC0  mov      qword ptr [rsp + 8], rbx                
  00278BC5  push     rdi                                     
  00278BC6  sub      rsp, 0x20                               
  00278BCA  movzx    edi, dl                                 
  00278BCD  mov      rbx, rcx                                
  00278BD0  call     0x180277e00                                -> VF5FS+0x277E00
  00278BD5  mov      rcx, rbx                                
  00278BD8  call     0x180277eb0                                -> VF5FS+0x277EB0
  00278BDD  test     dil, dil                                
  00278BE0  je       0x180278be7                                -> VF5FS+0x278BE7
  00278BE2  call     0x180277be0                                -> VF5FS+0x277BE0
  00278BE7  mov      rbx, qword ptr [rsp + 0x30]             
  00278BEC  add      rsp, 0x20                               
  00278BF0  pop      rdi                                     
  00278BF1  ret                                              

; ----------------------------------------------------------------------
; C.4  0x277E00 : etape 1 du reset
; ----------------------------------------------------------------------
; Elle efface `[rbx+0x64]`, et si `[rbx] == 2` elle construit un nom de
; fichier TEMPORAIRE : `lea rdx,[rip+...]` resout sur la chaine ".tmp",
; et la boucle `vpcmpistri` en est la recherche de longueur. C'est un
; nettoyage de brouillon, pas une ouverture de ressource.
;
--- VF5FS+0x277E00 .. +0x277E70  (112 octets), plage DITE
  00277E00  push     rbx                                     
  00277E02  sub      rsp, 0x20                               
  00277E06  mov      rbx, rcx                                
  00277E09  mov      ecx, dword ptr [rcx + 0x64]             
  00277E0C  test     ecx, ecx                                
  00277E0E  je       0x180277e8c                                -> VF5FS+0x277E8C
  00277E10  call     0x180279cf0                                -> VF5FS+0x279CF0
  00277E15  mov      dword ptr [rbx + 0x64], 0               
  00277E1C  cmp      dword ptr [rbx], 2                      
  00277E1F  jne      0x180277e8c                                -> VF5FS+0x277E8C
  00277E21  mov      rdx, qword ptr [rbx + 0x18]             
  00277E25  lea      rcx, [rsp + 0x30]                       
  00277E2A  call     0x18000e180                                -> VF5FS+0xE180
  00277E2F  nop                                              
  00277E30  vmovdqu  xmm1, xmmword ptr [rip + 0xfbe38]          ; VF5FS+0x373C70  .rdata+0x373C70
  00277E38  lea      rdx, [rip + 0x1b035d]                      ; VF5FS+0x42819C  ".tmp"
  00277E3F  lea      rax, [rdx - 0x10]                       
  00277E43  nop      dword ptr [rax]                         
  00277E47  nop      word ptr [rax + rax]                    
  00277E50  add      rax, 0x10                               
  00277E54  vmovdqu  xmm0, xmmword ptr [rax]                 
  00277E58  vpcmpistri xmm1, xmm0, 0x14                        
  00277E5E  jne      0x180277e50                                -> VF5FS+0x277E50
  00277E60  sub      eax, edx                                
  00277E62  lea      r8d, [rax + rcx]                        
  00277E66  lea      rcx, [rsp + 0x30]                       
  00277E6B  call     0x180010a70                                -> VF5FS+0x10A70

; ----------------------------------------------------------------------
; C.5  0x277EB0 : etape 2 du reset -- LA PREUVE QUE CA LIBERE
; ----------------------------------------------------------------------
; Quatre liberations de suite par 0x2796A0, et `[rbx+0x70] = 0` :
;     [rbx+0x70] -> 0x2796A0(ecx, ...) selon [rbx+0x28]  puis [rbx+0x70] = 0
;     [rbx+0x20] -> 0x2796A0(1, ...)
;     [rbx+0x18] -> 0x2796A0(1, ...)
;     [rbx+0x10] -> 0x2796A0(1, ...)
; `[rbx+0x70]` est exactement le champ que 0x278C00 rend quand l'etat
; vaut 5, c'est-a-dire LA DONNEE CHARGEE. Une fonction qui met ce champ
; a zero ne charge pas : elle relache.
;
--- VF5FS+0x277EB0 .. +0x277F40  (144 octets), plage DITE
  00277EB0  mov      qword ptr [rsp + 8], rbx                
  00277EB5  push     rdi                                     
  00277EB6  sub      rsp, 0x20                               
  00277EBA  cmp      dword ptr [rcx], 1                      
  00277EBD  mov      rbx, rcx                                
  00277EC0  jne      0x180277ee4                                -> VF5FS+0x277EE4
  00277EC2  mov      rcx, qword ptr [rcx + 0x70]             
  00277EC6  test     rcx, rcx                                
  00277EC9  je       0x180277ee4                                -> VF5FS+0x277EE4
  00277ECB  mov      eax, dword ptr [rbx + 0x28]             
  00277ECE  cmp      eax, 2                                  
  00277ED1  je       0x180277edf                                -> VF5FS+0x277EDF
  00277ED3  mov      rdx, rcx                                
  00277ED6  mov      ecx, eax                                
  00277ED8  call     0x1802796a0                                -> VF5FS+0x2796A0
  00277EDD  jmp      0x180277ee4                                -> VF5FS+0x277EE4
  00277EDF  call     0x180338fac                                -> VF5FS+0x338FAC
  00277EE4  mov      rdx, qword ptr [rbx + 0x20]             
  00277EE8  xor      edi, edi                                
  00277EEA  mov      qword ptr [rbx + 0x70], rdi             
  00277EEE  test     rdx, rdx                                
  00277EF1  je       0x180277efd                                -> VF5FS+0x277EFD
  00277EF3  mov      ecx, 1                                  
  00277EF8  call     0x1802796a0                                -> VF5FS+0x2796A0
  00277EFD  mov      rdx, qword ptr [rbx + 0x18]             
  00277F01  test     rdx, rdx                                
  00277F04  je       0x180277f10                                -> VF5FS+0x277F10
  00277F06  mov      ecx, 1                                  
  00277F0B  call     0x1802796a0                                -> VF5FS+0x2796A0
  00277F10  mov      rdx, qword ptr [rbx + 0x10]             
  00277F14  test     rdx, rdx                                
  00277F17  je       0x180277f23                                -> VF5FS+0x277F23
  00277F19  mov      ecx, 1                                  
  00277F1E  call     0x1802796a0                                -> VF5FS+0x2796A0
  00277F23  mov      qword ptr [rbx + 0x10], rdi             
  00277F27  mov      al, 1                                   
  00277F29  mov      qword ptr [rbx + 0x18], rdi             
  00277F2D  mov      qword ptr [rbx + 0x20], rdi             
  00277F31  mov      dword ptr [rbx + 8], 6                  
  00277F38  mov      rbx, qword ptr [rsp + 0x30]             

; ######################################################################
; ## D. CHARGER : LE JUMEAU, ET COMMENT ON LE RECONNAIT
; ######################################################################
;
; Les deux fonctions sont rangees cote a cote. Celle qui passe le NOM du
; jeu -- un TROISIEME argument en r8 -- est le chargeur :
;
;     0x1960B3  rcx = [0x75E018]        ; le REGISTRE
;     0x1960BA  call 0x199220           ; cherche l'entree
;     0x1960C3  rsi = rax + 0x10        ; <<< le NOM EMPAQUETE
;     0x1960C7  rax = [rax+0x10] ; shl 0x14 ; sar 0x14   ; decode sa longueur
;     0x1960E1  rcx = [0x75E018] ; call 0x199220         ; re-cherche
;     0x1960ED  rcx = [0x75E010]        ; le CHARGEUR
;     0x1960F4  r8  = rbx + 4           ; <<< 3e argument
;     0x1960FB  edx = [rax+0x18]        ; la CLE
;     0x1960FE  cmove r8, rsi           ; r8 = le NOM si rbx est nul
;
; `entree+0x10` est exactement le champ que notre releve du registre
; imprime comme `nom=` : c'est la paire (pointeur, longueur) empaquetee
; sur 64 bits. Le dechargeur, lui, ne passe que la cle.
;
; Et la fonction finit par un SAUT TERMINAL :
;
;     0x196111  jmp 0x18019B490
;
; donc le travail de chargement est fait par **0x19B490**, appelee avec
; rcx = le chargeur [0x75E010], edx = la cle, r8 = le nom (ou rbx+4).
; C'est l'homologue de 0x19BE10 du cote dechargement. 0x19B490 n'est PAS
; lue : c'est la prochaine a lire si le pilote du creneau +0x08 ne suffit
; pas a expliquer l'absence de lecture.
;
; La plage commence a 0x196090 et non 0x196080 : partir de 0x196080
; tombe AU MILIEU d'une instruction et produit du charabia
; (`ror byte ptr [rcx-0x75], 0xE3`), ce qui m'est deja arrive deux fois
; dans ce chantier ([[un-balayage-d-octets-n-est-pas-un-decodage]]).
;
--- VF5FS+0x196090 .. +0x196130  (160 octets), plage DITE
  00196090  mov      rcx, qword ptr [rip + 0x5c7f79]            ; VF5FS+0x75E010
  00196097  jmp      0x18019a010                                -> VF5FS+0x19A010
  0019609C  int3                                             
  0019609D  int3                                             
  0019609E  int3                                             
  0019609F  int3                                             
  001960A0  mov      qword ptr [rsp + 8], rbx                
  001960A5  mov      qword ptr [rsp + 0x10], rsi             
  001960AA  push     rdi                                     
  001960AB  sub      rsp, 0x20                               
  001960AF  mov      edi, ecx                                
  001960B1  mov      edx, ecx                                
  001960B3  mov      rcx, qword ptr [rip + 0x5c7f5e]            ; VF5FS+0x75E018
  001960BA  call     0x180199220                                -> VF5FS+0x199220
  001960BF  xor      ecx, ecx                                
  001960C1  mov      edx, edi                                
  001960C3  lea      rsi, [rax + 0x10]                       
  001960C7  mov      rax, qword ptr [rax + 0x10]             
  001960CB  shl      rax, 0x14                               
  001960CF  sar      rax, 0x14                               
  001960D3  mov      rbx, rax                                
  001960D6  shl      rbx, 4                                  
  001960DA  test     rax, rax                                
  001960DD  cmove    rbx, rcx                                
  001960E1  mov      rcx, qword ptr [rip + 0x5c7f30]            ; VF5FS+0x75E018
  001960E8  call     0x180199220                                -> VF5FS+0x199220
  001960ED  mov      rcx, qword ptr [rip + 0x5c7f1c]            ; VF5FS+0x75E010
  001960F4  lea      r8, [rbx + 4]                           
  001960F8  test     rbx, rbx                                
  001960FB  mov      edx, dword ptr [rax + 0x18]             
  001960FE  cmove    r8, rsi                                 
  00196102  mov      rbx, qword ptr [rsp + 0x30]             
  00196107  mov      rsi, qword ptr [rsp + 0x38]             
  0019610C  add      rsp, 0x20                               
  00196110  pop      rdi                                     
  00196111  jmp      0x18019b490                                -> VF5FS+0x19B490
  00196116  int3                                             
  00196117  int3                                             
  00196118  int3                                             
  00196119  int3                                             
  0019611A  int3                                             
  0019611B  int3                                             
  0019611C  int3                                             
  0019611D  int3                                             
  0019611E  int3                                             
  0019611F  int3                                             
  00196120  mov      edx, ecx                                
  00196122  mov      rcx, qword ptr [rip + 0x5c7ee7]            ; VF5FS+0x75E010
  00196129  jmp      0x18019b970                                -> VF5FS+0x19B970
  0019612E  int3                                             
  0019612F  int3                                             


; ######################################################################
; ## E. L'ESCALIER ENTIER, ET LA DOUBLE PORTE QUI DEMOLIT  (SS 419.139)
; ######################################################################
;
; Ci-dessous la fonction du PAS en ENTIER -- la mere 0x17AE30 et ses six
; corps de phase -- la ou le 419.137 n'en avait relevé que l'entree et la
; phase 0. C'est ce relevé qui donne l'epilogue, donc la polarite, donc
; l'erratum en tete de fichier.
;
; L'INDEX EST LU, PLUS SUPPOSE :
;
;     0017AE78  movsxd   rax, dword ptr [rdi + 0x58]
;     0017AEAA  mov      ecx, dword ptr [rdx + rax*4 + 0x17b228]
;     0017AEB4  jmp      rcx
;
; donc la phase est `[sel+0x58]`, et la table est bien celle de 0x17B228.
;
; LA CHAINE DES PHASES, telle que le code l'enchaine lui-meme :
;
;   0        attendre les SIX jeux 2D demandes par le creneau +0x08 :
;            0x026 + 0x113, puis 0x161+0x130 ou 0x15E+0x12D selon
;            `[FUN_180179E70() + 0x20]`, puis -- si `[sel+0x63]` est a
;            zero -- 0x144 + 0x112 ; sinon la commande 5 par `+0x1FF08`.
;            Quand les six sont la : 0x1AA3B0, 0x21F0F0, 0x195090, et
;            `[sel+0x58] = 1`.
;   1        FUN_1802CD400([0x428E60], "SEL_COMMON") ; `[sel+0x58] = 2`
;   2..6     0x17B280(sel) ; s'il rend 0, attendre. Puis la commande 7
;            par `+0x1FF08`. **PUIS LA DOUBLE PORTE.**
;   7..11    monte les animations AET PAR NOM : "chara_start"
;            (jeu 0x16A ou 0x16D), "bg_light_change" (0x14B ou 0x14C),
;            bornes "loop_start" / "loop_end", couche 0x10000, par
;            FUN_180180DF0 ; puis 0x17B4F0.
;   12..13   LA DEMOLITION : 0x17E370 sur sel, sel+0x68 et sel+0x3A0,
;            puis 0x2CCA00 sur les trois. C'est le seul chemin qui
;            rend 1.
;
; LA DOUBLE PORTE, ET CE QU'ELLE FAIT :
;
;     0017B006  cmp byte ptr [rdi + 0x5d], bpl ; je 0x17B09F
;     0017B010  cmp byte ptr [rdi + 0x5e], bpl ; je 0x17B09F
;       ...
;     0017B09F  mov dword ptr [rdi + 0x58], 0xc    <-- phase 12
;     0017B0AD  call 0x1800F0A50  ([VF5FS+0x7598C0])
;
; **L'un des deux octets a zero et le selecteur se DEMOLIT**, par la
; phase 12, sans jamais atteindre la phase 7 -- la seule qui monte les
; animations. Un ecran de selection qui ne montre rien et dont les
; boutons repondent est exactement ce que ce chemin produit.
;
; CE QUE SONT CES DEUX OCTETS. 0x17B7D0 est la fonction << REJOINDRE >> :
;
;     FUN_18017B7D0(sel, joueur) :
;       si joueur < 2 et [sel+0x5c] != 0 et [sel + 0x5d + joueur] == 0 :
;           [sel + 0x5d + joueur] = 1 ; rend 1
;       sinon rend 0
;
; donc `[sel+0x5d]` = le joueur 0 a rejoint, `[sel+0x5e]` = le joueur 1
; a rejoint, et `[sel+0x5c]` = les inscriptions sont ouvertes. L'escalier
; ferme `+0x5c` des la phase 7 (`mov byte [rdi+0x5c], bpl` en 0x17B18D).
;
; QUI LES POSE, ET SOUS QUELLE CONDITION. FUN_18017BB10 ouvre :
;
;     [sel+0x5c] = 1 (en DWORD : il remet donc +0x5d, +0x5e, +0x5f a 0)
;     [sel+0x60] = 0
;     FUN_1802CD400(sel, "SELECTOR")
;
; et le sous-etat 19 phase 0 (FUN_1800E3F90) enchaine :
;
;     FUN_18017BB10(DAT_1807598B8);                   // ouvre, 0x5d=0x5e=0
;     if (FUN_1800B1B10(ctx, 0)) FUN_18017B7D0(sel, 0);
;     if (FUN_1800B1B10(ctx, 1)) FUN_18017B7D0(sel, 1);
;
; LA PORTE EST DONC DEUX OCTETS D'UN AUTRE OBJET :
;
;     FUN_1800B1B10(ctx, port) = [ctx + 0x0C + port]
;     ctx = FUN_1800B21E0() = DAT_18073D9D8 = [VF5FS+0x73D9D8]
;
; et VF5FS+0x73D9D8 est **le meme objet d'entree** que celui dont la
; nullite casse le match ([[le-match-casse-sur-un-objet-d-entree-nul]]).
;
; L'AUTRE SITE, par image : FUN_1800E2470 rejoint TARD, sous
; `FUN_18017AE00(sel, n)` puis `FUN_1800B6E60(n)` -- c'est le
; << PRESS START pour entrer >> d'une borne, donc un joueur peut encore
; rejoindre apres l'ouverture.
;
; CE QUI RESTE A MESURER, et c'est court : `[sel+0x58]`, `[sel+0x5c]`,
; `[sel+0x5d]`, `[sel+0x5e]`, plus les deux octets
; `[[VF5FS+0x73D9D8]+0x0C]` et `+0x0D`. Six octets disent si le selecteur
; se demolit par cette porte.
;
; ----------------------------------------------------------------------
; E.1  LE PAS EN ENTIER : 0x17AE30 .. 0x17B228  (225 instructions)
; ----------------------------------------------------------------------
--- VF5FS+0x17AE30 .. +0x17B228  (1016 octets), plage DITE
  0017AE30  push     rbp                                     
  0017AE32  push     rdi                                     
  0017AE33  sub      rsp, 0x68                               
  0017AE37  mov      rdi, rcx                                
  0017AE3A  xor      edx, edx                                
  0017AE3C  mov      rcx, qword ptr [rip + 0x2ae01d]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017AE43  call     0x180181480                                -> VF5FS+0x181480
  0017AE48  cmp      byte ptr [rdi + 0x5d], 0                
  0017AE4C  je       0x18017ae62                                -> VF5FS+0x17AE62
  0017AE4E  cmp      byte ptr [rdi + 0x5e], 0                
  0017AE52  je       0x18017ae62                                -> VF5FS+0x17AE62
  0017AE54  mov      rcx, qword ptr [rip + 0x2ae005]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017AE5B  mov      dl, 1                                   
  0017AE5D  call     0x180181480                                -> VF5FS+0x181480
  0017AE62  mov      eax, dword ptr [rdi + 0x58]             
  0017AE65  xor      cl, cl                                  
  0017AE67  cmp      eax, 4                                  
  0017AE6A  je       0x18017ae71                                -> VF5FS+0x17AE71
  0017AE6C  cmp      eax, 9                                  
  0017AE6F  jne      0x18017ae73                                -> VF5FS+0x17AE73
  0017AE71  mov      cl, 1                                   
  0017AE73  call     0x1801cf1f0                                -> VF5FS+0x1CF1F0
  0017AE78  movsxd   rax, dword ptr [rdi + 0x58]             
  0017AE7C  xor      bpl, bpl                                
  0017AE7F  cmp      eax, 0x13                               
  0017AE82  ja       0x18017b21d                                -> VF5FS+0x17B21D
  0017AE88  mov      qword ptr [rsp + 0x58], r13             
  0017AE8D  lea      rdx, [rip - 0x17ae94]                      ; VF5FS+0x0
  0017AE94  mov      qword ptr [rsp + 0x88], rbx             
  0017AE9C  mov      r13d, 1                                 
  0017AEA2  mov      qword ptr [rsp + 0x90], rsi             
  0017AEAA  mov      ecx, dword ptr [rdx + rax*4 + 0x17b228] 
  0017AEB1  add      rcx, rdx                                
  0017AEB4  jmp      rcx                                     
  0017AEB6  mov      ecx, 0x26                               
  0017AEBB  mov      byte ptr [rdi + 0x5c], r13b             
  0017AEBF  call     0x180196130                                -> VF5FS+0x196130
  0017AEC4  test     al, al                                  
  0017AEC6  jne      0x18017b208                                -> VF5FS+0x17B208
  0017AECC  mov      ecx, 0x113                              
  0017AED1  call     0x1800262e0                                -> VF5FS+0x262E0
  0017AED6  test     al, al                                  
  0017AED8  jne      0x18017b208                                -> VF5FS+0x17B208
  0017AEDE  call     0x180179e70                                -> VF5FS+0x179E70
  0017AEE3  cmp      byte ptr [rax + 0x20], bpl              
  0017AEE7  je       0x18017af02                                -> VF5FS+0x17AF02
  0017AEE9  mov      ecx, 0x161                              
  0017AEEE  call     0x180196130                                -> VF5FS+0x196130
  0017AEF3  test     al, al                                  
  0017AEF5  jne      0x18017b208                                -> VF5FS+0x17B208
  0017AEFB  mov      ecx, 0x130                              
  0017AF00  jmp      0x18017af19                                -> VF5FS+0x17AF19
  0017AF02  mov      ecx, 0x15e                              
  0017AF07  call     0x180196130                                -> VF5FS+0x196130
  0017AF0C  test     al, al                                  
  0017AF0E  jne      0x18017b208                                -> VF5FS+0x17B208
  0017AF14  mov      ecx, 0x12d                              
  0017AF19  call     0x1800262e0                                -> VF5FS+0x262E0
  0017AF1E  test     al, al                                  
  0017AF20  jne      0x18017b208                                -> VF5FS+0x17B208
  0017AF26  cmp      byte ptr [rdi + 0x63], bpl              
  0017AF2A  je       0x18017af71                                -> VF5FS+0x17AF71
  0017AF2C  mov      rcx, qword ptr [rip + 0xb12ff5]            ; VF5FS+0xC8DF28
  0017AF33  mov      byte ptr [rsp + 0x80], bpl              
  0017AF3B  mov      rax, qword ptr [rcx + 0x1ff08]          
  0017AF42  test     rax, rax                                
  0017AF45  je       0x18017b208                                -> VF5FS+0x17B208
  0017AF4B  mov      rcx, qword ptr [rcx + 0x1ff10]          
  0017AF52  lea      r8, [rsp + 0x80]                        
  0017AF5A  mov      edx, 5                                  
  0017AF5F  call     rax                                     
  0017AF61  cmp      byte ptr [rsp + 0x80], bpl              
  0017AF69  je       0x18017b208                                -> VF5FS+0x17B208
  0017AF6F  jmp      0x18017af95                                -> VF5FS+0x17AF95
  0017AF71  mov      ecx, 0x144                              
  0017AF76  call     0x180196130                                -> VF5FS+0x196130
  0017AF7B  test     al, al                                  
  0017AF7D  jne      0x18017b208                                -> VF5FS+0x17B208
  0017AF83  mov      ecx, 0x112                              
  0017AF88  call     0x1800262e0                                -> VF5FS+0x262E0
  0017AF8D  test     al, al                                  
  0017AF8F  jne      0x18017b208                                -> VF5FS+0x17B208
  0017AF95  call     0x1801aa3b0                                -> VF5FS+0x1AA3B0
  0017AF9A  call     0x18021f0f0                                -> VF5FS+0x21F0F0
  0017AF9F  call     0x180195090                                -> VF5FS+0x195090
  0017AFA4  mov      dword ptr [rdi + 0x58], r13d            
  0017AFA8  mov      byte ptr [rdi + 0x5c], r13b             
  0017AFAC  lea      rdx, [rip + 0x2ad2ed]                      ; VF5FS+0x4282A0  "SEL_COMMON"
  0017AFB3  mov      rcx, qword ptr [rip + 0x2adea6]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017AFBA  call     0x1802cd400                                -> VF5FS+0x2CD400
  0017AFBF  mov      dword ptr [rdi + 0x58], 2               
  0017AFC6  mov      rcx, rdi                                
  0017AFC9  mov      byte ptr [rdi + 0x5c], r13b             
  0017AFCD  call     0x18017b280                                -> VF5FS+0x17B280
  0017AFD2  test     al, al                                  
  0017AFD4  je       0x18017b208                                -> VF5FS+0x17B208
  0017AFDA  mov      esi, 7                                  
  0017AFDF  cmp      byte ptr [rdi + 0x63], bpl              
  0017AFE3  je       0x18017b006                                -> VF5FS+0x17B006
  0017AFE5  mov      rcx, qword ptr [rip + 0xb12f3c]            ; VF5FS+0xC8DF28
  0017AFEC  mov      rax, qword ptr [rcx + 0x1ff08]          
  0017AFF3  test     rax, rax                                
  0017AFF6  je       0x18017b006                                -> VF5FS+0x17B006
  0017AFF8  mov      rcx, qword ptr [rcx + 0x1ff10]          
  0017AFFF  xor      r8d, r8d                                
  0017B002  mov      edx, esi                                
  0017B004  call     rax                                     
  0017B006  cmp      byte ptr [rdi + 0x5d], bpl              
  0017B00A  je       0x18017b09f                                -> VF5FS+0x17B09F
  0017B010  cmp      byte ptr [rdi + 0x5e], bpl              
  0017B014  je       0x18017b09f                                -> VF5FS+0x17B09F
  0017B01A  lea      rcx, [rdi + 0x3a0]                      
  0017B021  call     0x180184680                                -> VF5FS+0x184680
  0017B026  call     0x180041230                                -> VF5FS+0x41230
  0017B02B  lea      rcx, [rax + 8]                          
  0017B02F  call     0x180040b70                                -> VF5FS+0x40B70
  0017B034  test     eax, eax                                
  0017B036  setne    bl                                      
  0017B039  call     0x1801aa6c0                                -> VF5FS+0x1AA6C0
  0017B03E  cmp      eax, 4                                  
  0017B041  jne      0x18017b04b                                -> VF5FS+0x17B04B
  0017B043  call     0x1801aa6e0                                -> VF5FS+0x1AA6E0
  0017B048  movzx    ebx, al                                 
  0017B04B  test     bl, bl                                  
  0017B04D  je       0x18017b08b                                -> VF5FS+0x17B08B
  0017B04F  lea      rcx, [rdi + 0x68]                       
  0017B053  call     0x1802cca00                                -> VF5FS+0x2CCA00
  0017B058  test     al, al                                  
  0017B05A  jne      0x18017b208                                -> VF5FS+0x17B208
  0017B060  cmp      byte ptr [rdi + 0x61], bpl              
  0017B064  je       0x18017b090                                -> VF5FS+0x17B090
  0017B066  mov      rcx, qword ptr [rip + 0x2b7eb3]            ; VF5FS+0x432F20  .rdata+0x432F20
  0017B06D  call     0x1801a3f20                                -> VF5FS+0x1A3F20
  0017B072  call     0x18017ba00                                -> VF5FS+0x17BA00
  0017B077  mov      esi, 0x13                               
  0017B07C  mov      ecx, 0x708                              
  0017B081  mov      dword ptr [rdi + 0x58], esi             
  0017B084  call     0x18000af60                                -> VF5FS+0xAF60
  0017B089  jmp      0x18017b0b2                                -> VF5FS+0x17B0B2
  0017B08B  mov      esi, 0x11                               
  0017B090  mov      ecx, 0x708                              
  0017B095  mov      dword ptr [rdi + 0x58], esi             
  0017B098  call     0x18000af60                                -> VF5FS+0xAF60
  0017B09D  jmp      0x18017b0b2                                -> VF5FS+0x17B0B2
  0017B09F  mov      rcx, qword ptr [rip + 0x5de81a]            ; VF5FS+0x7598C0
  0017B0A6  mov      dword ptr [rdi + 0x58], 0xc             
  0017B0AD  call     0x1800f0a50                                -> VF5FS+0xF0A50
  0017B0B2  mov      rcx, qword ptr [rip + 0x5d99d7]            ; VF5FS+0x754A90
  0017B0B9  call     0x180106fb0                                -> VF5FS+0x106FB0
  0017B0BE  mov      ecx, 0x384                              
  0017B0C3  call     0x18000af60                                -> VF5FS+0xAF60
  0017B0C8  jmp      0x18017b208                                -> VF5FS+0x17B208
  0017B0CD  mov      qword ptr [rsp + 0x60], r12             
  0017B0D2  mov      qword ptr [rsp + 0x50], r15             
  0017B0D7  call     0x180179e70                                -> VF5FS+0x179E70
  0017B0DC  mov      rcx, qword ptr [rip + 0x2add7d]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017B0E3  lea      r12, [rip + 0x24822e]                      ; VF5FS+0x3C3318  "loop_end"
  0017B0EA  mov      qword ptr [rsp + 0x40], r12             
  0017B0EF  lea      r15, [rip + 0x248232]                      ; VF5FS+0x3C3328  "loop_start"
  0017B0F6  mov      qword ptr [rsp + 0x38], r15             
  0017B0FB  lea      r9, [rip + 0x2ad1ae]                       ; VF5FS+0x4282B0  "chara_start"
  0017B102  movzx    ebx, byte ptr [rax + 0x20]              
  0017B106  mov      r8d, 0x16a                              
  0017B10C  mov      eax, 0x16d                              
  0017B111  mov      dword ptr [rsp + 0x30], 0x10000         
  0017B119  test     bl, bl                                  
  0017B11B  mov      esi, 7                                  
  0017B120  mov      dword ptr [rsp + 0x28], esi             
  0017B124  cmovne   r8d, eax                                
  0017B128  mov      qword ptr [rsp + 0x20], 0               
  0017B131  xor      edx, edx                                
  0017B133  call     0x180180df0                                -> VF5FS+0x180DF0
  0017B138  mov      rcx, qword ptr [rip + 0x2add21]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017B13F  lea      r9, [rip + 0x2ad17a]                       ; VF5FS+0x4282C0  "bg_light_change"
  0017B146  xor      r8d, r8d                                
  0017B149  mov      qword ptr [rsp + 0x40], r12             
  0017B14E  mov      qword ptr [rsp + 0x38], r15             
  0017B153  test     bl, bl                                  
  0017B155  mov      dword ptr [rsp + 0x30], 0x10000         
  0017B15D  mov      edx, esi                                
  0017B15F  setne    r8b                                     
  0017B163  mov      dword ptr [rsp + 0x28], r13d            
  0017B168  add      r8d, 0x14b                              
  0017B16F  mov      qword ptr [rsp + 0x20], 0               
  0017B178  call     0x180180df0                                -> VF5FS+0x180DF0
  0017B17D  mov      r15, qword ptr [rsp + 0x50]             
  0017B182  mov      r12, qword ptr [rsp + 0x60]             
  0017B187  mov      dword ptr [rdi + 0x58], esi             
  0017B18A  mov      rcx, rdi                                
  0017B18D  mov      byte ptr [rdi + 0x5c], bpl              
  0017B191  call     0x18017b4f0                                -> VF5FS+0x17B4F0
  0017B196  test     al, al                                  
  0017B198  je       0x18017b208                                -> VF5FS+0x17B208
  0017B19A  mov      byte ptr [rdi + 0x5c], bpl              
  0017B19E  mov      dword ptr [rdi + 0x58], 0x11            
  0017B1A5  mov      byte ptr [rdi + 0x5c], bpl              
  0017B1A9  mov      rcx, qword ptr [rip + 0x2adcb0]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017B1B0  call     0x18017e370                                -> VF5FS+0x17E370
  0017B1B5  lea      rcx, [rdi + 0x68]                       
  0017B1B9  call     0x18017e370                                -> VF5FS+0x17E370
  0017B1BE  lea      rcx, [rdi + 0x3a0]                      
  0017B1C5  call     0x18017e370                                -> VF5FS+0x17E370
  0017B1CA  mov      dword ptr [rdi + 0x58], 0x12            
  0017B1D1  mov      byte ptr [rdi + 0x5c], bpl              
  0017B1D5  mov      rcx, qword ptr [rip + 0x2adc84]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017B1DC  call     0x1802cca00                                -> VF5FS+0x2CCA00
  0017B1E1  test     al, al                                  
  0017B1E3  jne      0x18017b208                                -> VF5FS+0x17B208
  0017B1E5  lea      rcx, [rdi + 0x68]                       
  0017B1E9  call     0x1802cca00                                -> VF5FS+0x2CCA00
  0017B1EE  test     al, al                                  
  0017B1F0  jne      0x18017b208                                -> VF5FS+0x17B208
  0017B1F2  lea      rcx, [rdi + 0x3a0]                      
  0017B1F9  call     0x1802cca00                                -> VF5FS+0x2CCA00
  0017B1FE  test     al, al                                  
  0017B200  movzx    ebp, bpl                                
  0017B204  cmove    ebp, r13d                               
  0017B208  mov      rsi, qword ptr [rsp + 0x90]             
  0017B210  mov      rbx, qword ptr [rsp + 0x88]             
  0017B218  mov      r13, qword ptr [rsp + 0x58]             
  0017B21D  movzx    eax, bpl                                
  0017B221  add      rsp, 0x68                               
  0017B225  pop      rdi                                     
  0017B226  pop      rbp                                     
  0017B227  ret                                              

; ----------------------------------------------------------------------
; E.2  0x17B7D0 : REJOINDRE  (30 instructions)
; ----------------------------------------------------------------------
--- VF5FS+0x17B7D0 .. +0x17B810  (64 octets), plage DITE
  0017B7D0  cmp      edx, 1                                  
  0017B7D3  ja       0x18017b7ed                                -> VF5FS+0x17B7ED
  0017B7D5  cmp      byte ptr [rcx + 0x5c], 0                
  0017B7D9  je       0x18017b7ed                                -> VF5FS+0x17B7ED
  0017B7DB  movsxd   rax, edx                                
  0017B7DE  cmp      byte ptr [rax + rcx + 0x5d], 0          
  0017B7E3  jne      0x18017b7ed                                -> VF5FS+0x17B7ED
  0017B7E5  mov      byte ptr [rax + rcx + 0x5d], 1          
  0017B7EA  mov      al, 1                                   
  0017B7EC  ret                                              
  0017B7ED  xor      al, al                                  
  0017B7EF  ret                                              
  0017B7F0  add      rcx, 0x68                               
  0017B7F4  jmp      0x18017e440                                -> VF5FS+0x17E440
  0017B7F9  int3                                             
  0017B7FA  int3                                             
  0017B7FB  int3                                             
  0017B7FC  int3                                             
  0017B7FD  int3                                             
  0017B7FE  int3                                             
  0017B7FF  int3                                             
  0017B800  add      rcx, 0x68                               
  0017B804  jmp      0x18017e460                                -> VF5FS+0x17E460
  0017B809  int3                                             
  0017B80A  int3                                             
  0017B80B  int3                                             
  0017B80C  int3                                             
  0017B80D  int3                                             
  0017B80E  int3                                             
  0017B80F  int3                                             

; ----------------------------------------------------------------------
; E.3  0x17BB10 : OUVRIR, et demander la tache "SELECTOR"  (16)
; ----------------------------------------------------------------------
--- VF5FS+0x17BB10 .. +0x17BB40  (48 octets), plage DITE
  0017BB10  mov      dword ptr [rcx + 0x5c], 1               
  0017BB17  lea      rdx, [rip + 0x24da62]                      ; VF5FS+0x3C9580  "SELECTOR"
  0017BB1E  mov      word ptr [rcx + 0x60], 0                
  0017BB24  jmp      0x1802cd400                                -> VF5FS+0x2CD400
  0017BB29  int3                                             
  0017BB2A  int3                                             
  0017BB2B  int3                                             
  0017BB2C  int3                                             
  0017BB2D  int3                                             
  0017BB2E  int3                                             
  0017BB2F  int3                                             
  0017BB30  mov      qword ptr [rsp + 8], rbx                
  0017BB35  push     rdi                                     
  0017BB36  sub      rsp, 0x20                               
  0017BB3A  lea      rbx, [rcx + 0x68]                       
  0017BB3E  mov      edi, edx                                

; ----------------------------------------------------------------------
; E.4  0x0B1B10 : LA PORTE, deux octets de [VF5FS+0x73D9D8]  (12)
; ----------------------------------------------------------------------
--- VF5FS+0xB1B10 .. +0xB1B30  (32 octets), plage DITE
  000B1B10  movsxd   rax, edx                                
  000B1B13  movzx    eax, byte ptr [rax + rcx + 0xc]         
  000B1B18  ret                                              
  000B1B19  int3                                             
  000B1B1A  int3                                             
  000B1B1B  int3                                             
  000B1B1C  int3                                             
  000B1B1D  int3                                             
  000B1B1E  int3                                             
  000B1B1F  int3                                             
  000B1B20  movsxd   rax, edx                                
  000B1B23  imul     rax, rax, 0x5f0                         


; ######################################################################
; ## F. LA CHAINE D'ENTREE DU JOUEUR 2, ET SEL_CHARA  (SS 419.141/142)
; ######################################################################
;
; CE QUE LA MESURE A DONNE (27 releves, sonde accrochee AU SOUS-ETAT et non
; a un numero d'image -- deux courses perdues avant ca) :
;
;     inscriptions[+0x5c]=1  joueur0[+0x5d]=1  joueur1[+0x5e]=0
;     objet d'entree [VF5FS+0x73D9D8] : port0 [+0x0C]=1  port1 [+0x0D]=0
;     PAS [sel+0x58] : 0 -> 4
;
; LA PHASE 4 N'EST PAS UN MUR. `0x17B280` (F.1) est un escalier dans
; l'escalier, et sa phase 4 est l'etat de REPOS de l'ecran de selection qui
; TOURNE : il a delegue la grille et les portraits a la sous-tache
; `SEL_CHARA` (`sel+0x68`, demandee par nom en 0x17B418) et a `SEL_CURSOR`.
; La double porte de la section E n'est donc pas encore atteinte -- elle est
; testee APRES que `0x17B280` ait rendu 1, c'est-a-dire a sa phase 6.
;
; LA CHAINE DU JOUEUR 2, LUE DE BOUT EN BOUT, du haut vers le bas :
;
;   [sel+0x5e]            pose seulement par FUN_18017B7D0(sel,1)
;     ^- appelee seulement si FUN_1800B6E60(1) != 0   (sous-etat 19 phase 1)
;   FUN_1800B6E60(p) = FUN_1800B6E70(p, 0)            (F.4) qui exige :
;       (ctx == 0 || [ctx+0x0C+p] == 0)
;       && FUN_1801A0E20(tab, p) != 0                 (F.5) = [tab + p]
;              tab = [VF5FS+0x432D70] -> VF5FS+0x6441E0
;              VALEUR D'IMAGE MESUREE : **01 01** -> les DEUX ports sont
;              declares. CETTE PORTE N'EST PAS LE MUR.
;       && FUN_18000BA20(...) == 0                    (bouchon de SEGA : vrai)
;       -> puis FUN_18019DB70(bloc, 2) != 0           = L'APPUI
;   FUN_18019DA30(p) = &DAT_18078E290 + p * 0x868     -- PAR PORT. Ghidra
;       perd l'argument parce que `ecx` porte encore le port au moment de
;       l'appel (0xB6E86 `mov ebx,ecx` le sauve, 0xB6E8B `call` suit).
;       [[la-decompilation-ghidra-perd-des-parametres]]
;   FUN_18019DB70(bloc, n) = (bloc[(n>>6)*8] >> (n & 0x3F)) & 1
;       -- une carte de 99 bits ; START est le bit 2 (ou 0x10 si
;       [VF5FS+0xC8DE1A] != 0). **C'est une SECONDE couche d'entree**, pas la
;       table des manettes de 0x795950 au pas de 0x54.
;   La carte est remplie une fois par image, pour les deux ports (F.6) :
;       FUN_18019DBF0(bloc, port) recopie l'etat precedent en bloc+0x30,
;       met a zero +0x00/+0x10/+0x20, puis demande sa source :
;       FUN_18000BA20 (bouchon, rend 0) puis **FUN_1801B2300(sortie, port)**.
;   FUN_1801B2300 (F.7) EST LA PORTE DU BAS :
;       movsxd rcx, dword ptr [rdx + rax*4 + 0x795c18]   ; DWORD, port*4
;       cmp ecx, 1 ; ja -> rend 0                        ; valide si <= 1
;       sinon recopie 0x70 octets de VF5FS+0x795A58 + liaison*0xD8
;       -> la LIAISON du port est un dword : port 0 en VF5FS+0x795C18,
;          port 1 en **VF5FS+0x795C1C**. La zone est HORS de la partie
;          initialisee du PE, donc le chargeur la met a ZERO : les deux
;          ports demarrent lies a la manette 0.
;
; CE QUE CA PREDIT, ET QUI EST TESTABLE EN UNE TOUCHE : si rien n'ecrit
; `[VF5FS+0x795C1C]`, le port 1 lit la manette 0, et un seul appui sur START
; depuis l'ecran de selection doit faire entrer le joueur 2 -- la garde du
; haut de 0x0B6E70 fait sortir le port 0 tout de suite, puisque son
; `[ctx+0x0C]` vaut deja 1. A MESURER AVANT D'ECRIRE QUOI QUE CE SOIT.
;
; SEL_CHARA (F.2), table VF5FS+0x428218, creneau +0x08 = 0x17E9D0 :
;   * il CHARGE pour de vrai : FUN_1801960A0(0x144) = SPR_S_SELCHA et
;     FUN_180026180(0x112) = AET_S_SELCHA, les deux chargeurs qui passent le
;     nom. L'art du selecteur est demande ICI, en plus de 0x17B850.
;   * `[sel_chara+0x58] = 0` : sa propre phase.
;   * DEUX bouchons `FUN_18000BA20` le detournent de son chemin de SEGA. Le
;     premier saute 0x17EA18..0x17EB0B, qui parcourait les 21 personnages,
;     interrogeait `FUN_180136960(n)` pour chacun (le filtre de deverrouillage),
;     sautait le n^o 0x13, batissait le tableau des permis et y tirait au
;     hasard. Le second saute 0x17EB19..0x17EB65.
;   * le chemin REELLEMENT pris, 0x17EB66 : ebx = FUN_1801AA370(), puis
;     [sel_chara+0x64] et [sel_chara+0x94] = FUN_1802CC250(0, ebx+0x12, 0)
;     -- les personnages des deux joueurs, au hasard ; 0x13 remplace par 0x14.
;     [sel_chara+0x68] = 0, [sel_chara+0x98] = 0, puis
;     FUN_1801E0390(sel_chara + 0x1D0).
;   * FUN_1801E0390 (F.3) initialise le widget : `[w+0x84] = 0x15` (21
;     personnages), `[w+0x8C] = 0x0101`, `[w+0x88] = 2`, le reste a zero ;
;     et si `bloc+0x1FF08` est POSE, `[w+0x90] = 1`. **Le motif +0x1FF08
;     pour la QUATRIEME fois**, apres CS_TITLE, le menu et 0x17B850.
;
; CE QUI N'EST PAS ETABLI : le lien avec le 419.135. Les dimensions nulles
; y portaient sur `[+0x214]` et `[+0x21c]` d'un objet de `FUN_1801DE510`, or
; ce widget-ci s'arrete a `+0xC4`. Ce sont deux objets differents jusqu'a
; preuve du contraire, et les souder serait une supposition.
;
; RESTE NON LU : `FUN_18017C1E0`, le PAS de SEL_CHARA (creneau +0x10), et
; `FUN_18017ED10` / `ED20` / `EE40`, les trois predicats de la phase 4.
;
; ----------------------------------------------------------------------
; F.1  0x17B280 : l'escalier DANS l'escalier, phases 2..6
; ----------------------------------------------------------------------
--- VF5FS+0x17B280 .. +0x17B4F0  (624 octets), plage DITE
  0017B280  push     rbx                                     
  0017B282  push     rsi                                     
  0017B283  push     rdi                                     
  0017B284  sub      rsp, 0x40                               
  0017B288  mov      qword ptr [rsp + 0x60], rbp             
  0017B28D  mov      rbx, rcx                                
  0017B290  mov      qword ptr [rsp + 0x68], r12             
  0017B295  xor      sil, sil                                
  0017B298  mov      qword ptr [rsp + 0x70], r13             
  0017B29D  xor      dil, dil                                
  0017B2A0  mov      qword ptr [rsp + 0x38], r14             
  0017B2A5  mov      qword ptr [rsp + 0x30], r15             
  0017B2AA  call     0x1800b21e0                                -> VF5FS+0xB21E0
  0017B2AF  mov      r14, rax                                
  0017B2B2  mov      r13d, 1                                 
  0017B2B8  cmp      byte ptr [rbx + 0x5d], sil              
  0017B2BC  je       0x18017b321                                -> VF5FS+0x17B321
  0017B2BE  xor      edx, edx                                
  0017B2C0  mov      rcx, rax                                
  0017B2C3  call     0x1800b22c0                                -> VF5FS+0xB22C0
  0017B2C8  xor      edx, edx                                
  0017B2CA  mov      rcx, r14                                
  0017B2CD  mov      r15d, eax                               
  0017B2D0  call     0x1800b22e0                                -> VF5FS+0xB22E0
  0017B2D5  xor      edx, edx                                
  0017B2D7  mov      rcx, r14                                
  0017B2DA  mov      r12d, eax                               
  0017B2DD  call     0x1800b22f0                                -> VF5FS+0xB22F0
  0017B2E2  xor      edx, edx                                
  0017B2E4  lea      rcx, [rbx + 0x68]                       
  0017B2E8  cmp      r15d, 0x15                              
  0017B2EC  je       0x18017b2ff                                -> VF5FS+0x17B2FF
  0017B2EE  mov      r9d, r12d                               
  0017B2F1  mov      dword ptr [rsp + 0x20], eax             
  0017B2F5  mov      r8d, r15d                               
  0017B2F8  call     0x18017ee50                                -> VF5FS+0x17EE50
  0017B2FD  jmp      0x18017b304                                -> VF5FS+0x17B304
  0017B2FF  call     0x18017e290                                -> VF5FS+0x17E290
  0017B304  cmp      byte ptr [rbx + 0x5f], sil              
  0017B308  je       0x18017b315                                -> VF5FS+0x17B315
  0017B30A  xor      edx, edx                                
  0017B30C  lea      rcx, [rbx + 0x68]                       
  0017B310  call     0x18017f070                                -> VF5FS+0x17F070
  0017B315  cmp      r15d, 0x15                              
  0017B319  movzx    esi, sil                                
  0017B31D  cmovne   esi, r13d                               
  0017B321  cmp      byte ptr [rbx + 0x5e], dil              
  0017B325  je       0x18017b38f                                -> VF5FS+0x17B38F
  0017B327  mov      edx, r13d                               
  0017B32A  mov      rcx, r14                                
  0017B32D  call     0x1800b22c0                                -> VF5FS+0xB22C0
  0017B332  mov      edx, r13d                               
  0017B335  mov      rcx, r14                                
  0017B338  mov      r15d, eax                               
  0017B33B  call     0x1800b22e0                                -> VF5FS+0xB22E0
  0017B340  mov      edx, r13d                               
  0017B343  mov      rcx, r14                                
  0017B346  mov      r12d, eax                               
  0017B349  call     0x1800b22f0                                -> VF5FS+0xB22F0
  0017B34E  lea      rcx, [rbx + 0x68]                       
  0017B352  mov      edx, r13d                               
  0017B355  cmp      r15d, 0x15                              
  0017B359  je       0x18017b36c                                -> VF5FS+0x17B36C
  0017B35B  mov      r9d, r12d                               
  0017B35E  mov      dword ptr [rsp + 0x20], eax             
  0017B362  mov      r8d, r15d                               
  0017B365  call     0x18017ee50                                -> VF5FS+0x17EE50
  0017B36A  jmp      0x18017b371                                -> VF5FS+0x17B371
  0017B36C  call     0x18017e290                                -> VF5FS+0x17E290
  0017B371  cmp      byte ptr [rbx + 0x60], dil              
  0017B375  je       0x18017b383                                -> VF5FS+0x17B383
  0017B377  mov      edx, r13d                               
  0017B37A  lea      rcx, [rbx + 0x68]                       
  0017B37E  call     0x18017f070                                -> VF5FS+0x17F070
  0017B383  cmp      r15d, 0x15                              
  0017B387  movzx    edi, dil                                
  0017B38B  cmovne   edi, r13d                               
  0017B38F  mov      ecx, dword ptr [rbx + 0x58]             
  0017B392  mov      r15, qword ptr [rsp + 0x30]             
  0017B397  mov      r14, qword ptr [rsp + 0x38]             
  0017B39C  mov      r13, qword ptr [rsp + 0x70]             
  0017B3A1  mov      r12, qword ptr [rsp + 0x68]             
  0017B3A6  mov      rbp, qword ptr [rsp + 0x60]             
  0017B3AB  sub      ecx, 2                                  
  0017B3AE  je       0x18017b3dd                                -> VF5FS+0x17B3DD
  0017B3B0  sub      ecx, 1                                  
  0017B3B3  je       0x18017b424                                -> VF5FS+0x17B424
  0017B3B5  sub      ecx, 1                                  
  0017B3B8  je       0x18017b438                                -> VF5FS+0x17B438
  0017B3BA  sub      ecx, 1                                  
  0017B3BD  je       0x18017b4ce                                -> VF5FS+0x17B4CE
  0017B3C3  cmp      ecx, 1                                  
  0017B3C6  je       0x18017b4d5                                -> VF5FS+0x17B4D5
  0017B3CC  mov      dword ptr [rbx + 0x58], 2               
  0017B3D3  xor      al, al                                  
  0017B3D5  add      rsp, 0x40                               
  0017B3D9  pop      rdi                                     
  0017B3DA  pop      rsi                                     
  0017B3DB  pop      rbx                                     
  0017B3DC  ret                                              
  0017B3DD  test     sil, sil                                
  0017B3E0  je       0x18017b3fc                                -> VF5FS+0x17B3FC
  0017B3E2  test     dil, dil                                
  0017B3E5  je       0x18017b3fc                                -> VF5FS+0x17B3FC
  0017B3E7  mov      byte ptr [rbx + 0x61], 1                
  0017B3EB  xor      al, al                                  
  0017B3ED  mov      dword ptr [rbx + 0x58], 5               
  0017B3F4  add      rsp, 0x40                               
  0017B3F8  pop      rdi                                     
  0017B3F9  pop      rsi                                     
  0017B3FA  pop      rbx                                     
  0017B3FB  ret                                              
  0017B3FC  mov      rcx, qword ptr [rip + 0x2b7b1d]            ; VF5FS+0x432F20  .rdata+0x432F20
  0017B403  call     0x1801a3f20                                -> VF5FS+0x1A3F20
  0017B408  call     0x18017ba00                                -> VF5FS+0x17BA00
  0017B40D  lea      rcx, [rbx + 0x68]                       
  0017B411  lea      rdx, [rip + 0x2aceb8]                      ; VF5FS+0x4282D0  "SEL_CHARA"
  0017B418  call     0x1802cd400                                -> VF5FS+0x2CD400
  0017B41D  mov      dword ptr [rbx + 0x58], 3               
  0017B424  lea      rcx, [rbx + 0x68]                       
  0017B428  call     0x18017ee40                                -> VF5FS+0x17EE40
  0017B42D  test     al, al                                  
  0017B42F  je       0x18017b3d3                                -> VF5FS+0x17B3D3
  0017B431  mov      dword ptr [rbx + 0x58], 4               
  0017B438  cmp      byte ptr [rbx + 0x62], 0                
  0017B43C  jne      0x18017b4bd                                -> VF5FS+0x17B4BD
  0017B43E  lea      rcx, [rbx + 0x68]                       
  0017B442  call     0x18017ed20                                -> VF5FS+0x17ED20
  0017B447  test     al, al                                  
  0017B449  jne      0x18017b45b                                -> VF5FS+0x17B45B
  0017B44B  lea      rcx, [rbx + 0x3a0]                      
  0017B452  call     0x1801846c0                                -> VF5FS+0x1846C0
  0017B457  test     al, al                                  
  0017B459  je       0x18017b4bd                                -> VF5FS+0x17B4BD
  0017B45B  cmp      byte ptr [rip + 0xb129b6], 0               ; VF5FS+0xC8DE18
  0017B462  jne      0x18017b4bd                                -> VF5FS+0x17B4BD
  0017B464  call     0x1801b34a0                                -> VF5FS+0x1B34A0
  0017B469  lea      rcx, [rbx + 0x68]                       
  0017B46D  mov      byte ptr [rbx + 0x62], 1                
  0017B471  call     0x1802ccb60                                -> VF5FS+0x2CCB60
  0017B476  cmp      byte ptr [rbx + 0x63], 0                
  0017B47A  je       0x18017b4a0                                -> VF5FS+0x17B4A0
  0017B47C  mov      rcx, qword ptr [rip + 0xb12aa5]            ; VF5FS+0xC8DF28
  0017B483  mov      rax, qword ptr [rcx + 0x1ff08]          
  0017B48A  test     rax, rax                                
  0017B48D  je       0x18017b4a0                                -> VF5FS+0x17B4A0
  0017B48F  mov      rcx, qword ptr [rcx + 0x1ff10]          
  0017B496  xor      r8d, r8d                                
  0017B499  mov      edx, 7                                  
  0017B49E  call     rax                                     
  0017B4A0  mov      rcx, qword ptr [rip + 0x5de419]            ; VF5FS+0x7598C0
  0017B4A7  call     0x1800f0a50                                -> VF5FS+0xF0A50
  0017B4AC  xor      al, al                                  
  0017B4AE  mov      dword ptr [rbx + 0x58], 0x11            
  0017B4B5  add      rsp, 0x40                               
  0017B4B9  pop      rdi                                     
  0017B4BA  pop      rsi                                     
  0017B4BB  pop      rbx                                     
  0017B4BC  ret                                              
  0017B4BD  lea      rcx, [rbx + 0x68]                       
  0017B4C1  call     0x18017ed10                                -> VF5FS+0x17ED10
  0017B4C6  test     al, al                                  
  0017B4C8  jne      0x18017b3d3                                -> VF5FS+0x17B3D3
  0017B4CE  mov      dword ptr [rbx + 0x58], 6               
  0017B4D5  mov      byte ptr [rbx + 0x5c], 0                
  0017B4D9  mov      al, 1                                   
  0017B4DB  add      rsp, 0x40                               
  0017B4DF  pop      rdi                                     
  0017B4E0  pop      rsi                                     
  0017B4E1  pop      rbx                                     
  0017B4E2  ret                                              
  0017B4E3  int3                                             
  0017B4E4  int3                                             
  0017B4E5  int3                                             
  0017B4E6  int3                                             
  0017B4E7  int3                                             
  0017B4E8  int3                                             
  0017B4E9  int3                                             
  0017B4EA  int3                                             
  0017B4EB  int3                                             
  0017B4EC  int3                                             
  0017B4ED  int3                                             
  0017B4EE  int3                                             
  0017B4EF  int3                                             
; ----------------------------------------------------------------------
; F.2  0x17E9D0 : le CHARGEUR de SEL_CHARA (creneau +0x08)
; ----------------------------------------------------------------------
--- VF5FS+0x17E9D0 .. +0x17EBF0  (544 octets), plage DITE
  0017E9D0  mov      qword ptr [rsp + 8], rbx                
  0017E9D5  mov      qword ptr [rsp + 0x10], rbp             
  0017E9DA  mov      qword ptr [rsp + 0x18], rsi             
  0017E9DF  mov      qword ptr [rsp + 0x20], rdi             
  0017E9E4  push     r12                                     
  0017E9E6  push     r14                                     
  0017E9E8  push     r15                                     
  0017E9EA  sub      rsp, 0x40                               
  0017E9EE  mov      r15, rcx                                
  0017E9F1  mov      ecx, 0x144                              
  0017E9F6  call     0x1801960a0                                -> VF5FS+0x1960A0
  0017E9FB  mov      ecx, 0x112                              
  0017EA00  call     0x180026180                                -> VF5FS+0x26180
  0017EA05  xor      edi, edi                                
  0017EA07  mov      dword ptr [r15 + 0x58], edi             
  0017EA0B  call     0x18000ba20                                -> VF5FS+0xBA20
  0017EA10  test     al, al                                  
  0017EA12  je       0x18017eb10                                -> VF5FS+0x17EB10
  0017EA18  mov      qword ptr [rsp + 0x20], rdi             
  0017EA1D  mov      ebp, edi                                
  0017EA1F  mov      dword ptr [rsp + 0x28], edi             
  0017EA23  mov      ebx, edi                                
  0017EA25  mov      dword ptr [rsp + 0x2c], ebx             
  0017EA29  xor      sil, sil                                
  0017EA2C  nop      dword ptr [rax]                         
  0017EA30  movzx    ecx, sil                                
  0017EA34  call     0x180136960                                -> VF5FS+0x136960
  0017EA39  test     al, al                                  
  0017EA3B  je       0x18017eac6                                -> VF5FS+0x17EAC6
  0017EA41  cmp      sil, 0x13                               
  0017EA45  je       0x18017eac6                                -> VF5FS+0x17EAC6
  0017EA47  movzx    r12d, sil                               
  0017EA4B  cmp      ebp, ebx                                
  0017EA4D  ja       0x18017eab2                                -> VF5FS+0x17EAB2
  0017EA4F  lea      ecx, [rbp + 1]                          
  0017EA52  shr      ecx, 1                                  
  0017EA54  mov      eax, 1                                  
  0017EA59  add      ecx, ebp                                
  0017EA5B  cmovne   eax, ecx                                
  0017EA5E  add      eax, 0xf                                
  0017EA61  and      eax, 0xfffffff0                         
  0017EA64  mov      ebp, eax                                
  0017EA66  mov      ecx, eax                                
  0017EA68  shl      rcx, 2                                  
  0017EA6C  call     0x180279bd0                                -> VF5FS+0x279BD0
  0017EA71  mov      r14, rax                                
  0017EA74  cmp      ebx, 1                                  
  0017EA77  jb       0x18017ea99                                -> VF5FS+0x17EA99
  0017EA79  mov      rdx, rax                                
  0017EA7C  mov      rcx, rdi                                
  0017EA7F  sub      rcx, rax                                
  0017EA82  mov      r8d, ebx                                
  0017EA85  test     rdx, rdx                                
  0017EA88  je       0x18017ea8f                                -> VF5FS+0x17EA8F
  0017EA8A  mov      eax, dword ptr [rcx + rdx]              
  0017EA8D  mov      dword ptr [rdx], eax                    
  0017EA8F  add      rdx, 4                                  
  0017EA93  sub      r8, 1                                   
  0017EA97  jne      0x18017ea85                                -> VF5FS+0x17EA85
  0017EA99  test     rdi, rdi                                
  0017EA9C  je       0x18017eaa6                                -> VF5FS+0x17EAA6
  0017EA9E  mov      rcx, rdi                                
  0017EAA1  call     0x180279c00                                -> VF5FS+0x279C00
  0017EAA6  mov      rdi, r14                                
  0017EAA9  mov      qword ptr [rsp + 0x20], r14             
  0017EAAE  mov      dword ptr [rsp + 0x28], ebp             
  0017EAB2  mov      eax, ebx                                
  0017EAB4  lea      rcx, [rdi + rax*4]                      
  0017EAB8  test     rcx, rcx                                
  0017EABB  je       0x18017eac0                                -> VF5FS+0x17EAC0
  0017EABD  mov      dword ptr [rcx], r12d                   
  0017EAC0  inc      ebx                                     
  0017EAC2  mov      dword ptr [rsp + 0x2c], ebx             
  0017EAC6  inc      sil                                     
  0017EAC9  cmp      sil, 0x15                               
  0017EACD  jb       0x18017ea30                                -> VF5FS+0x17EA30
  0017EAD3  xor      r8d, r8d                                
  0017EAD6  lea      edx, [rbx - 1]                          
  0017EAD9  xor      ecx, ecx                                
  0017EADB  call     0x1802cc250                                -> VF5FS+0x2CC250
  0017EAE0  mov      ecx, eax                                
  0017EAE2  mov      eax, dword ptr [rdi + rcx*4]            
  0017EAE5  mov      dword ptr [r15 + 0x64], eax             
  0017EAE9  xor      r8d, r8d                                
  0017EAEC  lea      edx, [rbx - 1]                          
  0017EAEF  xor      ecx, ecx                                
  0017EAF1  call     0x1802cc250                                -> VF5FS+0x2CC250
  0017EAF6  mov      ecx, eax                                
  0017EAF8  mov      eax, dword ptr [rdi + rcx*4]            
  0017EAFB  mov      dword ptr [r15 + 0x94], eax             
  0017EB02  mov      rcx, rdi                                
  0017EB05  call     0x180279c00                                -> VF5FS+0x279C00
  0017EB0A  nop                                              
  0017EB0B  jmp      0x18017ebb2                                -> VF5FS+0x17EBB2
  0017EB10  call     0x18000ba20                                -> VF5FS+0xBA20
  0017EB15  test     al, al                                  
  0017EB17  je       0x18017eb66                                -> VF5FS+0x17EB66
  0017EB19  vmovdqu  xmm0, xmmword ptr [rip + 0x2aa32f]         ; VF5FS+0x428E50  .rdata+0x428E50
  0017EB21  vmovdqu  xmmword ptr [rsp + 0x20], xmm0          
  0017EB27  mov      dword ptr [rsp + 0x30], 6               
  0017EB2F  xor      r8d, r8d                                
  0017EB32  mov      edx, 4                                  
  0017EB37  xor      ecx, ecx                                
  0017EB39  call     0x1802cc250                                -> VF5FS+0x2CC250
  0017EB3E  mov      eax, eax                                
  0017EB40  mov      ecx, dword ptr [rsp + rax*4 + 0x20]     
  0017EB44  mov      dword ptr [r15 + 0x64], ecx             
  0017EB48  xor      r8d, r8d                                
  0017EB4B  mov      edx, 4                                  
  0017EB50  xor      ecx, ecx                                
  0017EB52  call     0x1802cc250                                -> VF5FS+0x2CC250
  0017EB57  mov      eax, eax                                
  0017EB59  mov      ecx, dword ptr [rsp + rax*4 + 0x20]     
  0017EB5D  mov      dword ptr [r15 + 0x94], ecx             
  0017EB64  jmp      0x18017ebb2                                -> VF5FS+0x17EBB2
  0017EB66  call     0x1801aa370                                -> VF5FS+0x1AA370
  0017EB6B  movzx    ebx, al                                 
  0017EB6E  xor      r8d, r8d                                
  0017EB71  lea      edx, [rbx + 0x12]                       
  0017EB74  xor      ecx, ecx                                
  0017EB76  call     0x1802cc250                                -> VF5FS+0x2CC250
  0017EB7B  mov      dword ptr [r15 + 0x64], eax             
  0017EB7F  xor      r8d, r8d                                
  0017EB82  lea      edx, [rbx + 0x12]                       
  0017EB85  xor      ecx, ecx                                
  0017EB87  call     0x1802cc250                                -> VF5FS+0x2CC250
  0017EB8C  mov      dword ptr [r15 + 0x94], eax             
  0017EB93  cmp      dword ptr [r15 + 0x64], 0x13            
  0017EB98  jne      0x18017eba2                                -> VF5FS+0x17EBA2
  0017EB9A  mov      dword ptr [r15 + 0x64], 0x14            
  0017EBA2  cmp      eax, 0x13                               
  0017EBA5  jne      0x18017ebb2                                -> VF5FS+0x17EBB2
  0017EBA7  mov      dword ptr [r15 + 0x94], 0x14            
  0017EBB2  mov      byte ptr [r15 + 0x68], 0                
  0017EBB7  mov      byte ptr [r15 + 0x98], 0                
  0017EBBF  lea      rcx, [r15 + 0x1d0]                      
  0017EBC6  call     0x1801e0390                                -> VF5FS+0x1E0390
  0017EBCB  mov      al, 1                                   
  0017EBCD  mov      rbx, qword ptr [rsp + 0x60]             
  0017EBD2  mov      rbp, qword ptr [rsp + 0x68]             
  0017EBD7  mov      rsi, qword ptr [rsp + 0x70]             
  0017EBDC  mov      rdi, qword ptr [rsp + 0x78]             
  0017EBE1  add      rsp, 0x40                               
  0017EBE5  pop      r15                                     
  0017EBE7  pop      r14                                     
  0017EBE9  pop      r12                                     
  0017EBEB  ret                                              
  0017EBEC  int3                                             
  0017EBED  int3                                             
  0017EBEE  int3                                             
  0017EBEF  int3                                             
; ----------------------------------------------------------------------
; F.3  0x1E0390 : l'init du widget en sel_chara+0x1D0
; ----------------------------------------------------------------------
--- VF5FS+0x1E0390 .. +0x1E0410  (128 octets), plage DITE
  001E0390  xor      edx, edx                                
  001E0392  mov      dword ptr [rcx + 0x88], 2               
  001E039C  mov      qword ptr [rcx + 0x70], rdx             
  001E03A0  mov      qword ptr [rcx + 0x60], rdx             
  001E03A4  mov      dword ptr [rcx + 0x58], edx             
  001E03A7  mov      byte ptr [rcx + 0x68], dl               
  001E03AA  mov      dword ptr [rcx + 0x80], edx             
  001E03B0  mov      byte ptr [rcx + 0xc1], dl               
  001E03B6  mov      dword ptr [rcx + 0xc4], edx             
  001E03BC  mov      dword ptr [rcx + 0x90], edx             
  001E03C2  mov      dword ptr [rcx + 0x84], 0x15            
  001E03CC  mov      word ptr [rcx + 0x8c], 0x101            
  001E03D5  mov      rax, qword ptr [rip + 0xaadb4c]            ; VF5FS+0xC8DF28
  001E03DC  test     rax, rax                                
  001E03DF  je       0x1801e0402                                -> VF5FS+0x1E0402
  001E03E1  cmp      qword ptr [rax + 0x1ff08], rdx          
  001E03E8  je       0x1801e0402                                -> VF5FS+0x1E0402
  001E03EA  mov      dword ptr [rcx + 0x90], 1               
  001E03F4  mov      word ptr [rcx + 0x94], dx               
  001E03FB  mov      qword ptr [rcx + 0x98], rdx             
  001E0402  ret                                              
  001E0403  int3                                             
  001E0404  int3                                             
  001E0405  int3                                             
  001E0406  int3                                             
  001E0407  int3                                             
  001E0408  int3                                             
  001E0409  int3                                             
  001E040A  int3                                             
  001E040B  int3                                             
  001E040C  int3                                             
  001E040D  int3                                             
  001E040E  int3                                             
  001E040F  int3                                             
; ----------------------------------------------------------------------
; F.4  0x0B6E70 : la porte de l'APPUI d'un port
; ----------------------------------------------------------------------
--- VF5FS+0xB6E70 .. +0xB6FF8  (392 octets), plage DITE
  000B6E70  mov      qword ptr [rsp + 0x10], rbx             
  000B6E75  mov      qword ptr [rsp + 0x18], rbp             
  000B6E7A  mov      qword ptr [rsp + 0x20], rsi             
  000B6E7F  push     rdi                                     
  000B6E80  sub      rsp, 0x20                               
  000B6E84  mov      esi, edx                                
  000B6E86  mov      ebx, ecx                                
  000B6E88  xor      dil, dil                                
  000B6E8B  call     0x18019da30                                -> VF5FS+0x19DA30
  000B6E90  mov      rbp, rax                                
  000B6E93  call     0x1800b21e0                                -> VF5FS+0xB21E0
  000B6E98  test     rax, rax                                
  000B6E9B  je       0x1800b6eaf                                -> VF5FS+0xB6EAF
  000B6E9D  mov      edx, ebx                                
  000B6E9F  mov      rcx, rax                                
  000B6EA2  call     0x1800b1b10                                -> VF5FS+0xB1B10
  000B6EA7  test     al, al                                  
  000B6EA9  jne      0x1800b6fea                                -> VF5FS+0xB6FEA
  000B6EAF  mov      rcx, qword ptr [rip + 0x37beba]            ; VF5FS+0x432D70  .rdata+0x432D70
  000B6EB6  mov      edx, ebx                                
  000B6EB8  call     0x1801a0e20                                -> VF5FS+0x1A0E20
  000B6EBD  test     al, al                                  
  000B6EBF  je       0x1800b6fea                                -> VF5FS+0xB6FEA
  000B6EC5  mov      rcx, qword ptr [rip + 0x2bc914]            ; VF5FS+0x3737E0  .rdata+0x3737E0
  000B6ECC  call     0x18000ba20                                -> VF5FS+0xBA20
  000B6ED1  test     al, al                                  
  000B6ED3  jne      0x1800b6ee5                                -> VF5FS+0xB6EE5
  000B6ED5  mov      rcx, qword ptr [rip + 0x2bc904]            ; VF5FS+0x3737E0  .rdata+0x3737E0
  000B6EDC  call     0x18000ba20                                -> VF5FS+0xBA20
  000B6EE1  test     al, al                                  
  000B6EE3  je       0x1800b6f08                                -> VF5FS+0xB6F08
  000B6EE5  cmp      esi, 1                                  
  000B6EE8  jne      0x1800b6fea                                -> VF5FS+0xB6FEA
  000B6EEE  call     0x1800857a0                                -> VF5FS+0x857A0
  000B6EF3  test     rax, rax                                
  000B6EF6  je       0x1800b6f08                                -> VF5FS+0xB6F08
  000B6EF8  mov      rcx, rax                                
  000B6EFB  call     0x180085300                                -> VF5FS+0x85300
  000B6F00  test     al, al                                  
  000B6F02  je       0x1800b6fea                                -> VF5FS+0xB6FEA
  000B6F08  mov      qword ptr [rsp + 0x30], r14             
  000B6F0D  mov      r14d, 1                                 
  000B6F13  test     ebx, ebx                                
  000B6F15  jne      0x1800b6f1b                                -> VF5FS+0xB6F1B
  000B6F17  xor      ecx, ecx                                
  000B6F19  jmp      0x1800b6f27                                -> VF5FS+0xB6F27
  000B6F1B  cmp      ebx, r14d                               
  000B6F1E  jne      0x1800b6fe5                                -> VF5FS+0xB6FE5
  000B6F24  mov      ecx, r14d                               
  000B6F27  call     0x180057870                                -> VF5FS+0x57870
  000B6F2C  mov      rbx, rax                                
  000B6F2F  test     rax, rax                                
  000B6F32  je       0x1800b6fe5                                -> VF5FS+0xB6FE5
  000B6F38  mov      edx, esi                                
  000B6F3A  mov      rcx, rax                                
  000B6F3D  call     0x18000af60                                -> VF5FS+0xAF60
  000B6F42  mov      rcx, rbx                                
  000B6F45  call     0x180026620                                -> VF5FS+0x26620
  000B6F4A  test     al, al                                  
  000B6F4C  je       0x1800b6fe5                                -> VF5FS+0xB6FE5
  000B6F52  cmp      esi, r14d                               
  000B6F55  jne      0x1800b6fce                                -> VF5FS+0xB6FCE
  000B6F57  call     0x1800857a0                                -> VF5FS+0x857A0
  000B6F5C  test     rax, rax                                
  000B6F5F  je       0x1800b6fce                                -> VF5FS+0xB6FCE
  000B6F61  mov      rcx, rax                                
  000B6F64  call     0x1800857f0                                -> VF5FS+0x857F0
  000B6F69  test     eax, eax                                
  000B6F6B  jne      0x1800b6fce                                -> VF5FS+0xB6FCE
  000B6F6D  cmp      byte ptr [rip + 0xbd6ea6], dil             ; VF5FS+0xC8DE1A
  000B6F74  mov      edx, 2                                  
  000B6F79  mov      eax, 0x10                               
  000B6F7E  mov      rcx, rbp                                
  000B6F81  cmovne   edx, eax                                
  000B6F84  call     0x18019db70                                -> VF5FS+0x19DB70
  000B6F89  test     al, al                                  
  000B6F8B  je       0x1800b6fe5                                -> VF5FS+0xB6FE5
  000B6F8D  cmp      byte ptr [rip + 0xbd6e84], dil             ; VF5FS+0xC8DE18
  000B6F94  mov      rax, qword ptr [rip + 0xbd6f8d]            ; VF5FS+0xC8DF28
  000B6F9B  je       0x1800b6fad                                -> VF5FS+0xB6FAD
  000B6F9D  mov      ecx, dword ptr [rax + 0x10]             
  000B6FA0  test     cl, 2                                   
  000B6FA3  jne      0x1800b6fad                                -> VF5FS+0xB6FAD
  000B6FA5  or       ecx, 8                                  
  000B6FA8  mov      dword ptr [rax + 0x10], ecx             
  000B6FAB  jmp      0x1800b6fe5                                -> VF5FS+0xB6FE5
  000B6FAD  or       dword ptr [rax + 0x10], 4               
  000B6FB1  cmp      byte ptr [rip + 0xbd6e60], dil             ; VF5FS+0xC8DE18
  000B6FB8  je       0x1800b6fc8                                -> VF5FS+0xB6FC8
  000B6FBA  lea      rdx, [rip + 0x30cc8f]                      ; VF5FS+0x3C3C50  "sy_charin00st"
  000B6FC1  xor      ecx, ecx                                
  000B6FC3  call     0x180194800                                -> VF5FS+0x194800
  000B6FC8  movzx    edi, r14b                               
  000B6FCC  jmp      0x1800b6fe5                                -> VF5FS+0xB6FE5
  000B6FCE  mov      edx, 2                                  
  000B6FD3  mov      rcx, rbp                                
  000B6FD6  call     0x18019db70                                -> VF5FS+0x19DB70
  000B6FDB  test     al, al                                  
  000B6FDD  movzx    edi, dil                                
  000B6FE1  cmovne   edi, r14d                               
  000B6FE5  mov      r14, qword ptr [rsp + 0x30]             
  000B6FEA  mov      rbx, qword ptr [rsp + 0x38]             
  000B6FEF  movzx    eax, dil                                
  000B6FF3  mov      rbp, qword ptr [rsp + 0x40]             
; ----------------------------------------------------------------------
; F.5  0x1A0E20 : << ce port est-il declare >> = [p+n]
; ----------------------------------------------------------------------
--- VF5FS+0x1A0E20 .. +0x1A0E30  (16 octets), plage DITE
  001A0E20  cmp      edx, 2                                  
  001A0E23  jge      0x1801a0e2d                                -> VF5FS+0x1A0E2D
  001A0E25  movsxd   rax, edx                                
  001A0E28  movzx    eax, byte ptr [rax + rcx]               
  001A0E2C  ret                                              
  001A0E2D  xor      al, al                                  
  001A0E2F  ret                                              
; ----------------------------------------------------------------------
; F.6  0x19D9B0 : la boucle par image qui remplit les deux cartes
; ----------------------------------------------------------------------
--- VF5FS+0x19D9B0 .. +0x19DA30  (128 octets), plage DITE
  0019D9B0  mov      ecx, dword ptr [rsi]                    
  0019D9B2  mov      edx, edi                                
  0019D9B4  call     0x18000ba20                                -> VF5FS+0xBA20
  0019D9B9  inc      edi                                     
  0019D9BB  lea      rsi, [rsi + 0x868]                      
  0019D9C2  cmp      edi, 2                                  
  0019D9C5  jl       0x18019d9b0                                -> VF5FS+0x19D9B0
  0019D9C7  call     0x18000af60                                -> VF5FS+0xAF60
  0019D9CC  call     0x1801b19a0                                -> VF5FS+0x1B19A0
  0019D9D1  call     0x1801c8640                                -> VF5FS+0x1C8640
  0019D9D6  lea      rdi, [rip + 0x5f08b3]                      ; VF5FS+0x78E290
  0019D9DD  nop      dword ptr [rax]                         
  0019D9E0  mov      edx, ebx                                
  0019D9E2  mov      rcx, rdi                                
  0019D9E5  call     0x18019dbf0                                -> VF5FS+0x19DBF0
  0019D9EA  inc      ebx                                     
  0019D9EC  add      rdi, 0x868                              
  0019D9F3  cmp      ebx, 2                                  
  0019D9F6  jl       0x18019d9e0                                -> VF5FS+0x19D9E0
  0019D9F8  mov      rbx, qword ptr [rsp + 0x30]             
  0019D9FD  mov      rsi, qword ptr [rsp + 0x38]             
  0019DA02  add      rsp, 0x20                               
  0019DA06  pop      rdi                                     
  0019DA07  ret                                              
  0019DA08  int3                                             
  0019DA09  int3                                             
  0019DA0A  int3                                             
  0019DA0B  int3                                             
  0019DA0C  int3                                             
  0019DA0D  int3                                             
  0019DA0E  int3                                             
  0019DA0F  int3                                             
  0019DA10  sub      rsp, 0x28                               
  0019DA14  call     0x18000af60                                -> VF5FS+0xAF60
  0019DA19  add      rsp, 0x28                               
  0019DA1D  jmp      0x1801b1a60                                -> VF5FS+0x1B1A60
  0019DA22  int3                                             
  0019DA23  int3                                             
  0019DA24  int3                                             
  0019DA25  int3                                             
  0019DA26  int3                                             
  0019DA27  int3                                             
  0019DA28  int3                                             
  0019DA29  int3                                             
  0019DA2A  int3                                             
  0019DA2B  int3                                             
  0019DA2C  int3                                             
  0019DA2D  int3                                             
  0019DA2E  int3                                             
  0019DA2F  int3                                             
; ----------------------------------------------------------------------
; F.7  0x1B2300 : LA SOURCE, et la LIAISON qui la garde
; ----------------------------------------------------------------------
--- VF5FS+0x1B2300 .. +0x1B2340  (64 octets), plage DITE
  001B2300  mov      r8, rcx                                 
  001B2303  test     rcx, rcx                                
  001B2306  je       0x1801b2367                                -> VF5FS+0x1B2367
  001B2308  movsxd   rax, edx                                
  001B230B  lea      rdx, [rip - 0x1b2312]                      ; VF5FS+0x0
  001B2312  movsxd   rcx, dword ptr [rdx + rax*4 + 0x795c18] 
  001B231A  cmp      ecx, 1                                  
  001B231D  ja       0x1801b2367                                -> VF5FS+0x1B2367
  001B231F  imul     rcx, rcx, 0xd8                          
  001B2326  mov      al, 1                                   
  001B2328  vmovups  ymm0, ymmword ptr [rcx + rdx + 0x795a58]
  001B2331  vmovups  ymmword ptr [r8], ymm0                  
  001B2336  vmovups  ymm1, ymmword ptr [rcx + rdx + 0x795a78]

; ######################################################################
; ## G. LE PAS DE SEL_CHARA, ET LES TROIS PREDICATS  (SS 419.143)
; ######################################################################
;
; `FUN_18017C1E0`, creneau +0x10 de la table `VF5FS+0x428218`. `rdi` =
; l'objet SEL_CHARA, c'est-a-dire `selecteur + 0x68`.
;
; LE PREAMBULE, a chaque image :
;
;     [rdi+0x6b] <- [rdi+0x6a] ; [rdi+0x6a] = FUN_180181540(rdi+0xC8, 0)
;     [rdi+0x9b] <- [rdi+0x9a] ; [rdi+0x9a] = FUN_180181540(rdi+0xC8, 1)
;     si (l'un des deux a CHANGE) et [rdi+0x58] != 2 :  [rdi+0x58] = 0
;
; et `FUN_180181540(o, p) = [o + (p+2) * 0x40]`, donc les deux octets suivis
; sont **[sel_chara+0x148]** (joueur 1) et **[sel_chara+0x188]** (joueur 2).
; Ce sont des octets stables, pas des valeurs qui bougent d'elles-memes : la
; remise a zero de la phase n'est donc PAS une boucle infinie, c'est un
; << le joueur a bouge, on rejoue l'entree >>.
;
; Puis `esi = 0x14B + ([FUN_180179E70()+0x20] != 0 ? 1 : 0)` -- le JEU AET,
; le meme choix VGA/WXGA que partout ailleurs dans le selecteur -- et un
; switch sur `[rdi+0x58]` :
;
;     0 -> 0x17C8D5    1 -> 0x17C89C    2 -> 0x17C4CA
;     3 -> 0x17C365    4 -> 0x17C29B    autre -> 0x17CB66 (sortie)
;
; PHASE 0 (G.2), ET C'EST ELLE QUI DESSINE :
;
;     si [[VF5FS+0xC8DF28] + 0x1FF08] != 0  ->  0x17C9D7, et RIEN de ce qui
;         suit n'est monte. **Le motif +0x1FF08 pour la CINQUIEME fois**,
;         apres CS_TITLE, le menu, 0x17B850 et 0x1E0390.
;     FUN_180196130(0x144) != 0  ->  sortir   ; attend SPR_S_SELCHA
;     FUN_1800262E0(0x112) != 0  ->  sortir   ; attend AET_S_SELCHA
;     puis FUN_180180DB0([0x428E60], id, esi, NOM, arg, 0x20000) :
;         "bg_light_in"             id=0x07  arg=1
;         "deco_tit_chara_in"       id=0x0F  arg=9
;         "chara_icon_base_in"      id=0x10  arg=0xB   <-- LES ICONES
;         "chara_icon_name_in"      id=0x10  arg=0xB   <-- LEURS NOMS
;     et si FUN_1801AA370() rend non-zero, les variantes
;         "chara_icon_base_in_dur" / "chara_icon_name_in_dur" a la place.
;
; PHASE 1 : FUN_1802CCB10(rdi+0xC8) ; si 0, sortir. Puis
;     FUN_180183110(rdi+0xC8, 0, 0) et (rdi+0xC8, 1, 0) ; [rdi+0x58] = 2.
;
; PHASE 4 : FUN_180180BE0([0x428E60], 0x11) rend un flottant ; s'il atteint
;     [VF5FS+0x376030], alors FUN_1801813C0([0x428E60], 0x13) puis (.., 0x14)
;     -- **les couches 19 (1P) et 20 (2P)**, celles du portrait
;     ([[l-art-du-selecteur-n-est-jamais-lu]]).
;
; LES TROIS PREDICATS QUE LE SELECTEUR LUI POSE (G.3, G.4) :
;
;     FUN_18017EE40(x) = ([x+0x58] == 2)    ; la phase 3 du selecteur attend CA
;     FUN_18017ED10(x) = ([x+0x58] != 4)    ; la phase 4 du selecteur RESTE
;                                             tant que SEL_CHARA n'est pas a 4
;     FUN_18017ED20(x) = FUN_1802CCA00(x) ? (FUN_1801DF8E0(x+0x1D0) == 0) : 0
;
; CE QUE CA ETABLIT. La machine a etats est **coherente de bout en bout** :
; le selecteur se gare a sa phase 4 parce que SEL_CHARA n'est pas a sa
; phase 4, c'est-a-dire parce que **personne n'a choisi**. Ce n'est pas un
; blocage, et le portrait blanc n'est donc pas un defaut d'automate.
;
; LA SEULE QUESTION QUI RESTE, ET ELLE TIENT EN UN DWORD : SEL_CHARA
; atteint-il sa phase 2 ? Si oui, la phase 0 a monte les quatre animations
; et le defaut est dans leur RENDU ; si non, il est garé sur
; `FUN_180196130(0x144)` ou `FUN_1800262E0(0x112)`, c'est-a-dire sur le
; chargement -- ce que la section E dit pourtant termine. **A MESURER :
; `[sel_chara+0x58]`, avec sel_chara = [VF5FS+0x7598B8] + 0x68.**
;
; RESTE NON LU : les phases 2 (0x17C4CA) et 3 (0x17C365) du pas, et
; `FUN_1801DF8E0`, qui interroge le widget de +0x1D0.
;
; ----------------------------------------------------------------------
; G.1  0x17C1E0 : le PAS de SEL_CHARA -- preambule et switch
; ----------------------------------------------------------------------
--- VF5FS+0x17C1E0 .. +0x17C300  (288 octets), plage DITE
  0017C1E0  push     rbx                                     
  0017C1E2  push     rbp                                     
  0017C1E3  push     rsi                                     
  0017C1E4  push     rdi                                     
  0017C1E5  push     r12                                     
  0017C1E7  sub      rsp, 0x50                               
  0017C1EB  movzx    eax, byte ptr [rcx + 0x6a]              
  0017C1EF  lea      rbp, [rcx + 0xc8]                       
  0017C1F6  mov      byte ptr [rcx + 0x6b], al               
  0017C1F9  mov      rdi, rcx                                
  0017C1FC  mov      rcx, rbp                                
  0017C1FF  xor      edx, edx                                
  0017C201  xor      r12b, r12b                              
  0017C204  call     0x180181540                                -> VF5FS+0x181540
  0017C209  mov      byte ptr [rdi + 0x6a], al               
  0017C20C  mov      edx, 1                                  
  0017C211  movzx    eax, byte ptr [rdi + 0x9a]              
  0017C218  mov      rcx, rbp                                
  0017C21B  mov      byte ptr [rdi + 0x9b], al               
  0017C221  call     0x180181540                                -> VF5FS+0x181540
  0017C226  movzx    ecx, byte ptr [rdi + 0x6b]              
  0017C22A  xor      ebx, ebx                                
  0017C22C  mov      byte ptr [rdi + 0x9a], al               
  0017C232  cmp      byte ptr [rdi + 0x6a], cl               
  0017C235  jne      0x18017c23f                                -> VF5FS+0x17C23F
  0017C237  cmp      al, byte ptr [rdi + 0x9b]               
  0017C23D  je       0x18017c248                                -> VF5FS+0x17C248
  0017C23F  cmp      dword ptr [rdi + 0x58], 2               
  0017C243  je       0x18017c248                                -> VF5FS+0x17C248
  0017C245  mov      dword ptr [rdi + 0x58], ebx             
  0017C248  mov      qword ptr [rsp + 0x90], r14             
  0017C250  mov      qword ptr [rsp + 0x98], r15             
  0017C258  call     0x180179e70                                -> VF5FS+0x179E70
  0017C25D  mov      ecx, dword ptr [rdi + 0x58]             
  0017C260  mov      esi, ebx                                
  0017C262  cmp      byte ptr [rax + 0x20], bl               
  0017C265  setne    sil                                     
  0017C269  add      esi, 0x14b                              
  0017C26F  test     ecx, ecx                                
  0017C271  je       0x18017c8d5                                -> VF5FS+0x17C8D5
  0017C277  sub      ecx, 1                                  
  0017C27A  je       0x18017c89c                                -> VF5FS+0x17C89C
  0017C280  sub      ecx, 1                                  
  0017C283  je       0x18017c4ca                                -> VF5FS+0x17C4CA
  0017C289  sub      ecx, 1                                  
  0017C28C  je       0x18017c365                                -> VF5FS+0x17C365
  0017C292  cmp      ecx, 1                                  
  0017C295  jne      0x18017cb66                                -> VF5FS+0x17CB66
  0017C29B  mov      rcx, qword ptr [rip + 0x2acbbe]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C2A2  mov      edx, 0x11                               
  0017C2A7  call     0x180180be0                                -> VF5FS+0x180BE0
  0017C2AC  vcomiss  xmm0, dword ptr [rip + 0x1f9d7c]           ; VF5FS+0x376030  .rdata+0x376030
  0017C2B4  jb       0x18017c2d8                                -> VF5FS+0x17C2D8
  0017C2B6  mov      rcx, qword ptr [rip + 0x2acba3]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C2BD  mov      edx, 0x13                               
  0017C2C2  call     0x1801813c0                                -> VF5FS+0x1813C0
  0017C2C7  mov      rcx, qword ptr [rip + 0x2acb92]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C2CE  mov      edx, 0x14                               
  0017C2D3  call     0x1801813c0                                -> VF5FS+0x1813C0
  0017C2D8  xor      ecx, ecx                                
  0017C2DA  call     0x1800d10e0                                -> VF5FS+0xD10E0
  0017C2DF  test     al, al                                  
  0017C2E1  je       0x18017c2f2                                -> VF5FS+0x17C2F2
  0017C2E3  xor      ecx, ecx                                
  0017C2E5  call     0x1800d1100                                -> VF5FS+0xD1100
  0017C2EA  test     al, al                                  
  0017C2EC  je       0x18017cb66                                -> VF5FS+0x17CB66
  0017C2F2  mov      ecx, 1                                  
  0017C2F7  call     0x1800d10e0                                -> VF5FS+0xD10E0
  0017C2FC  test     al, al                                  
  0017C2FE  je       0x18017c312                                -> VF5FS+0x17C312
; ----------------------------------------------------------------------
; G.2  ses phases 1 et 0 ; la phase 0 MONTE LES ICONES
; ----------------------------------------------------------------------
--- VF5FS+0x17C89C .. +0x17C9C0  (292 octets), plage DITE
  0017C89C  mov      rcx, rbp                                
  0017C89F  call     0x1802ccb10                                -> VF5FS+0x2CCB10
  0017C8A4  test     al, al                                  
  0017C8A6  je       0x18017cb66                                -> VF5FS+0x17CB66
  0017C8AC  xor      r8d, r8d                                
  0017C8AF  xor      edx, edx                                
  0017C8B1  mov      rcx, rbp                                
  0017C8B4  call     0x180183110                                -> VF5FS+0x183110
  0017C8B9  xor      r8d, r8d                                
  0017C8BC  mov      edx, 1                                  
  0017C8C1  mov      rcx, rbp                                
  0017C8C4  call     0x180183110                                -> VF5FS+0x183110
  0017C8C9  mov      dword ptr [rdi + 0x58], 2               
  0017C8D0  jmp      0x18017cb66                                -> VF5FS+0x17CB66
  0017C8D5  mov      rax, qword ptr [rip + 0xb1164c]            ; VF5FS+0xC8DF28
  0017C8DC  cmp      qword ptr [rax + 0x1ff08], rbx          
  0017C8E3  jne      0x18017c9d7                                -> VF5FS+0x17C9D7
  0017C8E9  mov      ecx, 0x144                              
  0017C8EE  call     0x180196130                                -> VF5FS+0x196130
  0017C8F3  test     al, al                                  
  0017C8F5  jne      0x18017cb66                                -> VF5FS+0x17CB66
  0017C8FB  mov      ecx, 0x112                              
  0017C900  call     0x1800262e0                                -> VF5FS+0x262E0
  0017C905  test     al, al                                  
  0017C907  jne      0x18017cb66                                -> VF5FS+0x17CB66
  0017C90D  mov      rcx, qword ptr [rip + 0x2ac54c]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C914  lea      r9, [rip + 0x2ac1c5]                       ; VF5FS+0x428AE0  "bg_light_in"
  0017C91B  mov      dword ptr [rsp + 0x28], 0x20000         
  0017C923  mov      r8d, esi                                
  0017C926  mov      edx, 7                                  
  0017C92B  mov      dword ptr [rsp + 0x20], 1               
  0017C933  call     0x180180db0                                -> VF5FS+0x180DB0
  0017C938  mov      rcx, qword ptr [rip + 0x2ac521]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C93F  lea      r9, [rip + 0x2ac1aa]                       ; VF5FS+0x428AF0  "deco_tit_chara_in"
  0017C946  mov      r8d, esi                                
  0017C949  mov      dword ptr [rsp + 0x28], 0x20000         
  0017C951  mov      edx, 0xf                                
  0017C956  mov      dword ptr [rsp + 0x20], 9               
  0017C95E  call     0x180180db0                                -> VF5FS+0x180DB0
  0017C963  call     0x1801aa370                                -> VF5FS+0x1AA370
  0017C968  mov      rcx, qword ptr [rip + 0x2ac4f1]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C96F  mov      r8d, esi                                
  0017C972  mov      dword ptr [rsp + 0x28], 0x20000         
  0017C97A  mov      edx, 0x10                               
  0017C97F  mov      dword ptr [rsp + 0x20], 0xb             
  0017C987  test     al, al                                  
  0017C989  je       0x18017c9a0                                -> VF5FS+0x17C9A0
  0017C98B  lea      r9, [rip + 0x2ac176]                       ; VF5FS+0x428B08  "chara_icon_base_in_dur"
  0017C992  call     0x180180db0                                -> VF5FS+0x180DB0
  0017C997  lea      r9, [rip + 0x2ac182]                       ; VF5FS+0x428B20  "chara_icon_name_in_dur"
  0017C99E  jmp      0x18017c9b3                                -> VF5FS+0x17C9B3
  0017C9A0  lea      r9, [rip + 0x2ac191]                       ; VF5FS+0x428B38  "chara_icon_base_in"
  0017C9A7  call     0x180180db0                                -> VF5FS+0x180DB0
  0017C9AC  lea      r9, [rip + 0x2ac19d]                       ; VF5FS+0x428B50  "chara_icon_name_in"
  0017C9B3  mov      rcx, qword ptr [rip + 0x2ac4a6]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C9BA  mov      r8d, esi                                
; ----------------------------------------------------------------------
; G.3  0x17ED10 et 0x17ED20 : deux des trois predicats
; ----------------------------------------------------------------------
--- VF5FS+0x17ED10 .. +0x17ED50  (64 octets), plage DITE
  0017ED10  cmp      dword ptr [rcx + 0x58], 4               
  0017ED14  setne    al                                      
  0017ED17  ret                                              
  0017ED18  int3                                             
  0017ED19  int3                                             
  0017ED1A  int3                                             
  0017ED1B  int3                                             
  0017ED1C  int3                                             
  0017ED1D  int3                                             
  0017ED1E  int3                                             
  0017ED1F  int3                                             
  0017ED20  push     rbx                                     
  0017ED22  sub      rsp, 0x20                               
  0017ED26  mov      rbx, rcx                                
  0017ED29  call     0x1802cca00                                -> VF5FS+0x2CCA00
  0017ED2E  test     al, al                                  
  0017ED30  jne      0x18017ed38                                -> VF5FS+0x17ED38
  0017ED32  add      rsp, 0x20                               
  0017ED36  pop      rbx                                     
  0017ED37  ret                                              
  0017ED38  lea      rcx, [rbx + 0x1d0]                      
  0017ED3F  call     0x1801df8e0                                -> VF5FS+0x1DF8E0
  0017ED44  test     eax, eax                                
  0017ED46  sete     al                                      
  0017ED49  add      rsp, 0x20                               
  0017ED4D  pop      rbx                                     
  0017ED4E  ret                                              
  0017ED4F  int3                                             
; ----------------------------------------------------------------------
; G.4  0x17EE40 : << SEL_CHARA est-il a sa phase 2 >>
; ----------------------------------------------------------------------
--- VF5FS+0x17EE40 .. +0x17EE50  (16 octets), plage DITE
  0017EE40  cmp      dword ptr [rcx + 0x58], 2               
  0017EE44  sete     al                                      
  0017EE47  ret                                              
  0017EE48  int3                                             
  0017EE49  int3                                             
  0017EE4A  int3                                             
  0017EE4B  int3                                             
  0017EE4C  int3                                             
  0017EE4D  int3                                             
  0017EE4E  int3                                             
  0017EE4F  int3                                             

; ######################################################################
; ## H. LES PHASES 2 ET 3 DU PAS DE SEL_CHARA  (SS 419.144)
; ######################################################################
;
; PHASE 3 (H.1) est la sequence de SORTIE, et elle finit par
; `[sel_chara+0x58] = 4` -- ce que `FUN_18017ED10` attend pour laisser le
; selecteur quitter sa propre phase 4 :
;
;     FUN_180182D70(rbp) != 0  ->  attendre
;     FUN_1802CCB60(rbp)
;     par port : si FUN_1800D10E0(p) alors FUN_1800D1130(p)
;     "bg_light_change"                 id=0x07  arg=1
;     "deco_tit_chara_out_stage_in"     id=0x0F  arg=9, bornes
;                                       "cha_out_start" / "cha_out_end"
;     "chara_end"            (ou _dur)  id=0x10  arg=0xB
;     "chara_icon_name_out"  (ou _dur)  id=0x11  arg=0xF
;     FUN_180181400([0x428E60], [VF5FS+0x7598D0], 4)
;     FUN_180181400([0x428E60], [VF5FS+0x7598F8], 4)
;     [sel_chara+0x58] = 4
;
; L'id 0x11 est exactement celui dont la phase 4 interroge la progression
; (`FUN_180180BE0([0x428E60], 0x11)` compare a `[VF5FS+0x376030]`) avant de
; jouer les couches 0x13 et 0x14, celles du portrait. La chaine se tient.
;
; PHASE 2 (H.2) est la BOUCLE DE SELECTION :
;
;     si [[0x428E60]+0x139] != 0 ou [+0x13A] != 0  ->  attendre
;     FUN_180183110(rbp, 0, 0) ; FUN_180183110(rbp, 1, 0)
;     si FUN_18017F700([0x428E60], 7) : monter "bg_light" id=7 arg=1,
;                                       couche **0x10000** (et non 0x20000)
;     rsi = sel_chara + 0x1D0                       ; LE WIDGET
;     si FUN_1802CCAB0(rsi)  ->  0x17C6E2
;     si [VF5FS+0xC8DE18] != 0 et [VF5FS+0xC8DE19] == 0  ->  0x17C6E2
;     si FUN_1801DF8E0(rsi) == 0  ->  SORTIR
;     puis, par joueur : FUN_1802CCA00(sel_chara), [sel_chara+0x68] /
;         [+0x98], FUN_1801B24B0(port) -> FUN_1801B6DA0(...)
;     FUN_1800E1940() : si [rax] == 8 alors FUN_18000BA20(-1) (bouchon)
;     si [VF5FS+0xC8DE19] != 0  ->  0x17C702
;     FUN_1801B2870() -> r14d
;     si bloc+0x1FF08 est POSE : commande 0xF5 puis commande 0xF6
;
; et le widget se lit ainsi :
;
;     FUN_1801DF8E0(w) :
;       si [w+0x68] != 0 et FUN_1802CCAB0() == 0 :  rend [w+0x64]
;       sinon rend -1
;
; donc `[w+0x68]` = << un choix a ete fait >>, `[w+0x64]` = l'indice choisi,
; et les deux sont mis a zero par `FUN_1801E0390` (section F.3). ATTENTION :
; `-1` est NON nul, donc la phase 2 ne sort que si le resultat est
; EXACTEMENT 0.
;
; LE 419.135 NE PARLAIT PAS DE CE WIDGET. `FUN_1801DE510` est appelee par
; `FUN_1801FA490` et `FUN_1802079E0`, et `FUN_1801DFBC0` par
; `FUN_18020F1E0`, le batisseur du MENU PRINCIPAL. Les dimensions nulles du
; 419.135 portaient donc sur le widget de liste DU MENU. Verifie par les
; appelants, pas suppose par la famille d'adresses.
;
; RESTE NON LU : `FUN_1801B24B0` / `FUN_1801B6DA0`, le bloc `0x17C6E2`, et
; surtout **qui fait tourner le widget `sel_chara+0x1D0`** -- le candidat est
; le pas de `SEL_CURSOR`, `FUN_180181550` (table `0x4281D0`, relevee au
; 419.138).
;
; ----------------------------------------------------------------------
; H.1  0x17C365 : la phase 3, la sequence de SORTIE  (68 instructions)
; ----------------------------------------------------------------------
--- VF5FS+0x17C365 .. +0x17C4CA  (357 octets), plage DITE
  0017C365  mov      rcx, rbp                                
  0017C368  call     0x180182d70                                -> VF5FS+0x182D70
  0017C36D  test     al, al                                  
  0017C36F  jne      0x18017cb66                                -> VF5FS+0x17CB66
  0017C375  mov      rcx, rbp                                
  0017C378  call     0x1802ccb60                                -> VF5FS+0x2CCB60
  0017C37D  xor      ecx, ecx                                
  0017C37F  call     0x1800d10e0                                -> VF5FS+0xD10E0
  0017C384  test     al, al                                  
  0017C386  je       0x18017c38f                                -> VF5FS+0x17C38F
  0017C388  xor      ecx, ecx                                
  0017C38A  call     0x1800d1130                                -> VF5FS+0xD1130
  0017C38F  mov      ecx, 1                                  
  0017C394  call     0x1800d10e0                                -> VF5FS+0xD10E0
  0017C399  test     al, al                                  
  0017C39B  je       0x18017c3a7                                -> VF5FS+0x17C3A7
  0017C39D  mov      ecx, 1                                  
  0017C3A2  call     0x1800d1130                                -> VF5FS+0xD1130
  0017C3A7  mov      rcx, qword ptr [rip + 0x2acab2]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C3AE  lea      r9, [rip + 0x2abf0b]                       ; VF5FS+0x4282C0  "bg_light_change"
  0017C3B5  mov      dword ptr [rsp + 0x28], 0x20000         
  0017C3BD  mov      r8d, esi                                
  0017C3C0  mov      edx, 7                                  
  0017C3C5  mov      dword ptr [rsp + 0x20], 1               
  0017C3CD  call     0x180180db0                                -> VF5FS+0x180DB0
  0017C3D2  mov      rcx, qword ptr [rip + 0x2aca87]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C3D9  lea      rax, [rip + 0x2ac7b8]                      ; VF5FS+0x428B98  "cha_out_end"
  0017C3E0  mov      qword ptr [rsp + 0x40], rax             
  0017C3E5  lea      r9, [rip + 0x2ac7cc]                       ; VF5FS+0x428BB8  "deco_tit_chara_out_stage_in"
  0017C3EC  lea      rax, [rip + 0x2ac7b5]                      ; VF5FS+0x428BA8  "cha_out_start"
  0017C3F3  mov      r8d, esi                                
  0017C3F6  mov      qword ptr [rsp + 0x38], rax             
  0017C3FB  mov      edx, 0xf                                
  0017C400  mov      dword ptr [rsp + 0x30], 0x20000         
  0017C408  mov      dword ptr [rsp + 0x28], 9               
  0017C410  mov      qword ptr [rsp + 0x20], rbx             
  0017C415  call     0x180180df0                                -> VF5FS+0x180DF0
  0017C41A  call     0x1801aa370                                -> VF5FS+0x1AA370
  0017C41F  mov      rcx, qword ptr [rip + 0x2aca3a]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C426  mov      r8d, esi                                
  0017C429  mov      dword ptr [rsp + 0x28], 0x20000         
  0017C431  mov      edx, 0x10                               
  0017C436  mov      dword ptr [rsp + 0x20], 0xb             
  0017C43E  test     al, al                                  
  0017C440  je       0x18017c457                                -> VF5FS+0x17C457
  0017C442  lea      r9, [rip + 0x2ac78f]                       ; VF5FS+0x428BD8  "chara_end_dur"
  0017C449  call     0x180180db0                                -> VF5FS+0x180DB0
  0017C44E  lea      r9, [rip + 0x2ac793]                       ; VF5FS+0x428BE8  "chara_icon_name_out_dur"
  0017C455  jmp      0x18017c46a                                -> VF5FS+0x17C46A
  0017C457  lea      r9, [rip + 0x2ac7a2]                       ; VF5FS+0x428C00  "chara_end"
  0017C45E  call     0x180180db0                                -> VF5FS+0x180DB0
  0017C463  lea      r9, [rip + 0x2ac7a6]                       ; VF5FS+0x428C10  "chara_icon_name_out"
  0017C46A  mov      rcx, qword ptr [rip + 0x2ac9ef]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C471  mov      r8d, esi                                
  0017C474  mov      dword ptr [rsp + 0x28], 0x20000         
  0017C47C  mov      edx, 0x11                               
  0017C481  mov      dword ptr [rsp + 0x20], 0xf             
  0017C489  call     0x180180db0                                -> VF5FS+0x180DB0
  0017C48E  mov      edx, dword ptr [rip + 0x5dd43c]            ; VF5FS+0x7598D0
  0017C494  mov      r8d, 4                                  
  0017C49A  mov      rcx, qword ptr [rip + 0x2ac9bf]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C4A1  call     0x180181400                                -> VF5FS+0x181400
  0017C4A6  mov      edx, dword ptr [rip + 0x5dd44c]            ; VF5FS+0x7598F8
  0017C4AC  mov      r8d, 4                                  
  0017C4B2  mov      rcx, qword ptr [rip + 0x2ac9a7]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C4B9  call     0x180181400                                -> VF5FS+0x181400
  0017C4BE  mov      dword ptr [rdi + 0x58], 4               
  0017C4C5  jmp      0x18017cb66                                -> VF5FS+0x17CB66

; ----------------------------------------------------------------------
; H.2  0x17C4CA : la phase 2, la BOUCLE DE SELECTION  (94 instructions)
; ----------------------------------------------------------------------
--- VF5FS+0x17C4CA .. +0x17C680  (438 octets), plage DITE
  0017C4CA  mov      rax, qword ptr [rip + 0x2ac98f]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C4D1  cmp      byte ptr [rax + 0x139], bl              
  0017C4D7  jne      0x18017cb66                                -> VF5FS+0x17CB66
  0017C4DD  cmp      byte ptr [rax + 0x13a], bl              
  0017C4E3  jne      0x18017cb66                                -> VF5FS+0x17CB66
  0017C4E9  xor      r8d, r8d                                
  0017C4EC  xor      edx, edx                                
  0017C4EE  mov      rcx, rbp                                
  0017C4F1  call     0x180183110                                -> VF5FS+0x183110
  0017C4F6  xor      r8d, r8d                                
  0017C4F9  mov      edx, 1                                  
  0017C4FE  mov      rcx, rbp                                
  0017C501  call     0x180183110                                -> VF5FS+0x183110
  0017C506  mov      rcx, qword ptr [rip + 0x2ac953]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C50D  mov      edx, 7                                  
  0017C512  call     0x18017f700                                -> VF5FS+0x17F700
  0017C517  test     al, al                                  
  0017C519  je       0x18017c546                                -> VF5FS+0x17C546
  0017C51B  mov      rcx, qword ptr [rip + 0x2ac93e]            ; VF5FS+0x428E60  .rdata+0x428E60
  0017C522  lea      r9, [rip + 0x2ac64f]                       ; VF5FS+0x428B78  "bg_light"
  0017C529  mov      dword ptr [rsp + 0x28], 0x10000         
  0017C531  mov      r8d, esi                                
  0017C534  mov      edx, 7                                  
  0017C539  mov      dword ptr [rsp + 0x20], 1               
  0017C541  call     0x180180db0                                -> VF5FS+0x180DB0
  0017C546  lea      rsi, [rdi + 0x1d0]                      
  0017C54D  mov      rcx, rsi                                
  0017C550  call     0x1802ccab0                                -> VF5FS+0x2CCAB0
  0017C555  test     al, al                                  
  0017C557  jne      0x18017c6e2                                -> VF5FS+0x17C6E2
  0017C55D  cmp      byte ptr [rip + 0xb118b5], bl              ; VF5FS+0xC8DE18
  0017C563  je       0x18017c571                                -> VF5FS+0x17C571
  0017C565  cmp      byte ptr [rip + 0xb118ae], bl              ; VF5FS+0xC8DE19
  0017C56B  je       0x18017c6e2                                -> VF5FS+0x17C6E2
  0017C571  mov      rcx, rsi                                
  0017C574  call     0x1801df8e0                                -> VF5FS+0x1DF8E0
  0017C579  test     eax, eax                                
  0017C57B  je       0x18017cb66                                -> VF5FS+0x17CB66
  0017C581  mov      rcx, rdi                                
  0017C584  call     0x1802cca00                                -> VF5FS+0x2CCA00
  0017C589  test     al, al                                  
  0017C58B  je       0x18017c5ac                                -> VF5FS+0x17C5AC
  0017C58D  cmp      byte ptr [rdi + 0x68], bl               
  0017C590  jne      0x18017c702                                -> VF5FS+0x17C702
  0017C596  xor      ecx, ecx                                
  0017C598  call     0x1801b24b0                                -> VF5FS+0x1B24B0
  0017C59D  mov      ecx, eax                                
  0017C59F  call     0x1801b6da0                                -> VF5FS+0x1B6DA0
  0017C5A4  test     al, al                                  
  0017C5A6  jne      0x18017c702                                -> VF5FS+0x17C702
  0017C5AC  mov      rcx, rdi                                
  0017C5AF  call     0x1802cca00                                -> VF5FS+0x2CCA00
  0017C5B4  test     al, al                                  
  0017C5B6  je       0x18017c5dd                                -> VF5FS+0x17C5DD
  0017C5B8  cmp      byte ptr [rdi + 0x98], bl               
  0017C5BE  jne      0x18017c702                                -> VF5FS+0x17C702
  0017C5C4  mov      ecx, 1                                  
  0017C5C9  call     0x1801b24b0                                -> VF5FS+0x1B24B0
  0017C5CE  mov      ecx, eax                                
  0017C5D0  call     0x1801b6da0                                -> VF5FS+0x1B6DA0
  0017C5D5  test     al, al                                  
  0017C5D7  jne      0x18017c702                                -> VF5FS+0x17C702
  0017C5DD  call     0x1800e1940                                -> VF5FS+0xE1940
  0017C5E2  cmp      dword ptr [rax], 8                      
  0017C5E5  jne      0x18017c5f9                                -> VF5FS+0x17C5F9
  0017C5E7  mov      ecx, 0xffffffff                         
  0017C5EC  call     0x18000ba20                                -> VF5FS+0xBA20
  0017C5F1  test     al, al                                  
  0017C5F3  jne      0x18017c702                                -> VF5FS+0x17C702
  0017C5F9  cmp      byte ptr [rip + 0xb1181a], bl              ; VF5FS+0xC8DE19
  0017C5FF  jne      0x18017c702                                -> VF5FS+0x17C702
  0017C605  call     0x1801b2870                                -> VF5FS+0x1B2870
  0017C60A  mov      rcx, qword ptr [rip + 0xb11917]            ; VF5FS+0xC8DF28
  0017C611  mov      r14d, eax                               
  0017C614  cmp      qword ptr [rcx + 0x1ff08], rbx          
  0017C61B  je       0x18017c698                                -> VF5FS+0x17C698
  0017C61D  mov      dword ptr [rsp + 0x88], ebx             
  0017C624  mov      byte ptr [rsp + 0x80], bl               
  0017C62B  mov      rax, qword ptr [rcx + 0x1ff08]          
  0017C632  test     rax, rax                                
  0017C635  je       0x18017c65b                                -> VF5FS+0x17C65B
  0017C637  mov      rcx, qword ptr [rcx + 0x1ff10]          
  0017C63E  lea      r8, [rsp + 0x80]                        
  0017C646  mov      edx, 0xf5                               
  0017C64B  call     rax                                     
  0017C64D  mov      rcx, qword ptr [rip + 0xb118d4]            ; VF5FS+0xC8DF28
  0017C654  mov      ebx, dword ptr [rsp + 0x88]             
  0017C65B  mov      rax, qword ptr [rcx + 0x1ff08]          
  0017C662  test     rax, rax                                
  0017C665  je       0x18017c684                                -> VF5FS+0x17C684
  0017C667  mov      rcx, qword ptr [rcx + 0x1ff10]          
  0017C66E  lea      r8, [rsp + 0x88]                        
  0017C676  mov      edx, 0xf6                               
  0017C67B  call     rax                                     


; ######################################################################
; ## I. SEL_CURSOR, ET L'OCTET QUI L'AUTORISE  (SS 419.145)
; ######################################################################
;
; LE PAS DE SEL_CURSOR NE FAIT RIEN LUI-MEME (I.1) :
;
;     FUN_180181550(curseur) :
;         FUN_180181FE0(curseur, 1)
;         FUN_180181FE0(curseur, 0)
;         FUN_180181580(curseur)
;         xor al, al ; ret            ; IL REND TOUJOURS 0
;
; et `FUN_180181580` ne calcule qu'un etat << les deux joueurs sont sur le
; meme personnage >> en `+0x78` (1..4), depuis `[+0x88]`/`[+0xC8]` et
; `[+0xA0]`/`[+0xE0]`. Tout le mouvement est donc dans `FUN_180181FE0`.
;
; LES SIX PORTES DE `FUN_180181FE0(curseur, port)` (I.2). Avec
; `rec = curseur + (port+2)*0x40` -- et noter que `port*0x40 + 0x81` vaut
; exactement `rec + 1`, donc les deux premieres portes sont DEUX OCTETS
; VOISINS DU MEME ENREGISTREMENT :
;
;     si [rec + 0] == 0                        -> SORTIR
;     si [rec + 0x20] vaut 6 ou 7              -> sortir
;     si [rec + 0x28] == 6                     -> sortir
;     si [rec + 8] nul, ou [[rec + 8]] nul     -> sortir
;     si [rec + 1] == 0                        -> SORTIR
;     si [[0x428E60]+0x139] ou [+0x13A] != 0   -> sortir
;     si [bloc+0x1FF08] == 0 -> 0x18215A       ; notre cas : on saute les
;                                              ; commandes 8 et 0xD
;
; `[rec + 0]` est l'octet que le preambule de SEL_CHARA surveille
; (`FUN_180181540(o,p) = [o + (p+2)*0x40]`, section G). `[rec + 1]` est celui
; que `FUN_180183110` ecrit :
;
;     FUN_180183110(o, p, v) :  [o + p*0x40 + 0x81] = v        (I.3)
;
; HUIT SITES D'APPEL, RELEVES PAR `VF5RE/qui_appelle.py` (outil NEUF du
; 419.145, auto-teste sur ces memes sites). SEPT passent `xor r8d, r8d`,
; donc ZERO :
;
;     0x17C4F1, 0x17C501   phase 2 de SEL_CHARA, les deux ports, A CHAQUE IMAGE
;     0x17C8B4, 0x17C8C4   phase 1 de SEL_CHARA, les deux ports
;     0x17D3CB, 0x17D583   dans FUN_18017CC20
;     0x183597             dans la phase 2 du conteneur
;
; et UN SEUL passe une valeur non nulle :
;
;     0x18364B   movzx r8d, r13b   avec r13d = 1 (pose en 0x1833D9)
;
; DONC : la phase 2 de SEL_CHARA EFFACE cet octet a chaque image, et le seul
; code du module qui le RALLUME est la phase 2 de `FUN_180183390`.
;
; `FUN_180183390` EST LE PAS DU CONTENEUR DU CURSEUR. Sa vtable est
; `VF5FS+0x429D98`, relevee par `octets_module.py` :
;
;     +0x00 = 0x183320    +0x08 = 0x1844E0
;     +0x10 = 0x183390    +0x18 = 0x183A80
;
; la meme forme que toutes les tables de taches. `qui_appelle.py` ne lui
; trouve AUCUN appelant direct : il n'est atteint que par ce creneau. Et le
; constructeur `0x183150` pose `[obj] = 0x429D98` ET `[obj+0x70] = 0x4281D0`,
; la table de SEL_CURSOR -- donc l'objet SEL_CURSOR est le sous-objet `+0x70`
; de ce conteneur, et le conteneur est lui-meme une tache.
;
; SON AIGUILLAGE (I.4), sur `[rbx+0x58]`, avec r13d = 1 :
;
;     0 -> 0x183789    1 -> 0x18376C    2 -> 0x18355A
;     3 -> 0x1834AA    4 -> 0x183413    autre -> 0x1839AC (sortie)
;
; SA PHASE 2 EST L'ARMEMENT (I.5) :
;
;     r15 ^= 1                                  ; l'AUTRE port
;     FUN_180183110(rbx+0x70, r15, 0)           ; on efface d'abord
;     si FUN_1802CCAB0(rbx+0x178)        -> 0x183650
;     si FUN_1801DF8E0(rbx+0x178) == 0   -> SORTIR
;     si FUN_1800E1940() rend 8 et FUN_18000BA20(-1) : chemin MORT (bouchon)
;     r12 = FUN_1801B2870()
;     si r12 < 0  ->  0x183640 :  FUN_180183110(rbx+0x70, r15, 1)   <<<< ICI
;     sinon : FUN_1801E0390(rbx+0x178), tache "CANCEL_CAUTION",
;             FUN_1802316E0(0x400) -> [rbx+0x1e8], FUN_1801E1700(..,1),
;             [rbx+0x200] = r12, [rbx+0x20d] = 1   -- et RIEN n'est arme
;
; `rbx+0x178` est le MEME widget que la phase 2 de SEL_CHARA interroge
; (`sel_chara+0x1D0`, section H.2) : meme `FUN_1801DF8E0`, meme
; `FUN_1801E0390`.
;
; LE DECIDEUR `FUN_1801B2870` (I.7), ENTIER. Il boucle sur les deux ports :
;
;     edi = FUN_18000BA20()  = 0 (bouchon)    ; donc eax vaut 2 plus bas
;     ebx = -1
;     par port p = 0, 1 :
;         si [VF5FS+0x795C10 + p] == 0  ->  port suivant
;         r10 = [VF5FS+0x795AC8 + p*0xD8]  (borne a [0,1])
;         si (r10 & 2) != 0  ->  ebx = p
;     puis, si bloc+0x1FF08 est POSE :
;         commande 0xF5 avec [rsp+0x40] (octet) et [rsp+0x48] (dword), nuls
;         commande 0xF6 avec [rsp+0x48]
;         edx = [rsp+0x48] ; si edx >= 2  ->  rendre ebx
;         si [VF5FS+0x795C10 + edx] == 0  ->  rendre ebx
;         si [rsp+0x40] != 0  ->  ebx = edx
;     rendre ebx
;
; `octets_module.py` : **`VF5FS+0x795C10` et `VF5FS+0x795AC8` sont tous deux
; HORS de la partie initialisee de .data -- le chargeur les met a ZERO.**
; MAIS L'IMAGE N'EST PAS L'EXECUTION, et ma propre fiche le disait :
; `FUN_1801B26B0` pose `_DAT_180795c10 = 0x101`, donc les deux octets valent 1
; des que cette fonction tourne. LA CONCLUSION TIENT DANS LES DEUX CAS :
;   - a 0 : la boucle saute chaque port, ebx reste -1 ;
;   - a 1 : r10 = [0x795AC8 + p*0xD8] vaut 0, `test r10d, 2` est faux, donc
;     ebx reste -1 ; et la queue ne remplace ebx que si l'octet [rsp+0x40]
;     rendu par la commande 0xF6 est non nul -- notre hote n'ecrit rien.
; Donc `FUN_1801B2870()` rend -1, `js 0x183640` EST PRIS : l'armement est
; ATTEIGNABLE dans notre course. Le decideur n'est pas le mur.
;
; SA PHASE 0 EST LA PORTE (I.6) :
;
;     si [rbx+0x2e0] == 0  ->  0x1837D7 :
;         FUN_180196130(0x146) != 0  ->  sortir      ; attend un jeu SPR
;         FUN_...(0x115)                             ; et un jeu AET
;     sinon, CHEMIN HOTE :
;         [rsp+0xb0] = 0
;         si bloc+0x1FF08 est NUL  ->  0x1839AC, SORTIR sans rien faire
;         poster la COMMANDE 5 avec &[rsp+0xb0]
;         si [rsp+0xb0] est reste ZERO  ->  0x1839AC, SORTIR
;
; et sa phase 4 (0x183413) teste le MEME `[rbx+0x2e0]` pour choisir entre la
; commande 7 et `FUN_18017B830`. C'est le motif du repartiteur pour la
; SIXIEME fois dans ce seul ecran.
;
; CE QUE CA ETABLIT, ET CE QUE CA NE DIT PAS. La chaine complete de la grille
; est lue de bout en bout, et chaque maillon de l'ARMEMENT se verifie. Il
; reste UNE inconnue, et elle est etroite : **`FUN_180183390` atteint-il sa
; phase 2 ?** Sa phase 0 veut, selon `[rbx+0x2e0]`, soit deux jeux 2D de plus
; (SPR 0x146, AET 0x115 -- PAS les 0x144/0x112 de SEL_CHARA), soit un octet
; NON NUL en reponse a la commande 5, que notre hote ne gere pas (son
; aiguillage ne connait que 1, 2, 3 dans cette plage). Je ne sais pas lequel
; des deux chemins est pris : `[rbx+0x2e0]` n'est pas mesure, et le supposer
; serait inventer.
;
; ----------------------------------------------------------------------
; I.1  0x181550 : le PAS de SEL_CURSOR (table 0x4281D0, +0x10)  (93 instructions)
; ----------------------------------------------------------------------
--- VF5FS+0x181550 .. +0x1816C0  (368 octets), plage DITE
  00181550  push     rbx                                     
  00181552  sub      rsp, 0x20                               
  00181556  mov      edx, 1                                  
  0018155B  mov      rbx, rcx                                
  0018155E  call     0x180181fe0                                -> VF5FS+0x181FE0
  00181563  xor      edx, edx                                
  00181565  mov      rcx, rbx                                
  00181568  call     0x180181fe0                                -> VF5FS+0x181FE0
  0018156D  mov      rcx, rbx                                
  00181570  call     0x180181580                                -> VF5FS+0x181580
  00181575  xor      al, al                                  
  00181577  add      rsp, 0x20                               
  0018157B  pop      rbx                                     
  0018157C  ret                                              
  00181580  mov      qword ptr [rsp + 8], rbx                
  00181585  mov      qword ptr [rsp + 0x10], rsi             
  0018158A  push     rdi                                     
  0018158B  sub      rsp, 0x50                               
  0018158F  xor      edx, edx                                
  00181591  mov      rbx, rcx                                
  00181594  call     0x180181e70                                -> VF5FS+0x181E70
  00181599  mov      edx, 1                                  
  0018159E  mov      rcx, rbx                                
  001815A1  call     0x180181e70                                -> VF5FS+0x181E70
  001815A6  mov      r8d, dword ptr [rbx + 0x78]             
  001815AA  xor      edi, edi                                
  001815AC  mov      dword ptr [rbx + 0x7c], r8d             
  001815B0  mov      eax, edi                                
  001815B2  mov      rdx, qword ptr [rbx + 0x88]             
  001815B9  mov      esi, 3                                  
  001815BE  test     rdx, rdx                                
  001815C1  je       0x180181616                                -> VF5FS+0x181616
  001815C3  mov      rcx, qword ptr [rbx + 0xc8]             
  001815CA  test     rcx, rcx                                
  001815CD  je       0x180181616                                -> VF5FS+0x181616
  001815CF  cmp      rdx, rcx                                
  001815D2  jne      0x180181616                                -> VF5FS+0x181616
  001815D4  mov      edx, dword ptr [rbx + 0xa0]             
  001815DA  cmp      edx, 1                                  
  001815DD  je       0x1801815e4                                -> VF5FS+0x1815E4
  001815DF  cmp      edx, 7                                  
  001815E2  jne      0x180181616                                -> VF5FS+0x181616
  001815E4  mov      ecx, dword ptr [rbx + 0xe0]             
  001815EA  cmp      ecx, 1                                  
  001815ED  je       0x1801815f4                                -> VF5FS+0x1815F4
  001815EF  cmp      ecx, 7                                  
  001815F2  jne      0x180181616                                -> VF5FS+0x181616
  001815F4  cmp      edx, 7                                  
  001815F7  jne      0x18018160b                                -> VF5FS+0x18160B
  001815F9  cmp      ecx, 7                                  
  001815FC  mov      eax, 2                                  
  00181601  mov      edx, 4                                  
  00181606  cmove    eax, edx                                
  00181609  jmp      0x180181616                                -> VF5FS+0x181616
  0018160B  cmp      ecx, 7                                  
  0018160E  mov      eax, 1                                  
  00181613  cmove    eax, esi                                
  00181616  mov      dword ptr [rbx + 0x78], eax             
  00181619  cmp      eax, r8d                                
  0018161C  je       0x18018166e                                -> VF5FS+0x18166E
  0018161E  mov      rcx, qword ptr [rip + 0x2a783b]            ; VF5FS+0x428E60  .rdata+0x428E60
  00181625  xor      edx, edx                                
  00181627  mov      r8d, 2                                  
  0018162D  call     0x180181400                                -> VF5FS+0x181400
  00181632  mov      rcx, qword ptr [rip + 0x2a7827]            ; VF5FS+0x428E60  .rdata+0x428E60
  00181639  mov      r8d, esi                                
  0018163C  xor      edx, edx                                
  0018163E  call     0x180181400                                -> VF5FS+0x181400
  00181643  mov      rcx, qword ptr [rip + 0x2a7816]            ; VF5FS+0x428E60  .rdata+0x428E60
  0018164A  mov      edx, 1                                  
  0018164F  mov      r8d, 2                                  
  00181655  call     0x180181400                                -> VF5FS+0x181400
  0018165A  mov      rcx, qword ptr [rip + 0x2a77ff]            ; VF5FS+0x428E60  .rdata+0x428E60
  00181661  mov      r8d, esi                                
  00181664  mov      edx, 1                                  
  00181669  call     0x180181400                                -> VF5FS+0x181400
  0018166E  cmp      dword ptr [rbx + 0x78], edi             
  00181671  je       0x1801817c7                                -> VF5FS+0x1817C7
  00181677  mov      rax, qword ptr [rbx + 0x88]             
  0018167E  vxorps   xmm0, xmm0, xmm0                        
  00181682  vmovss   dword ptr [rsp + 0x40], xmm0            
  00181688  vmovss   dword ptr [rsp + 0x44], xmm0            
  0018168E  vmovss   dword ptr [rsp + 0x48], xmm0            
  00181694  test     rax, rax                                
  00181697  je       0x1801817de                                -> VF5FS+0x1817DE
  0018169D  cmp      qword ptr [rax], rdi                    
  001816A0  je       0x1801817de                                -> VF5FS+0x1817DE
  001816A6  mov      rcx, qword ptr [rip + 0x2a77b3]            ; VF5FS+0x428E60  .rdata+0x428E60
  001816AD  xor      edx, edx                                
  001816AF  mov      r8d, 2                                  
  001816B5  call     0x18017f740                                -> VF5FS+0x17F740
  001816BA  test     al, al                                  
  001816BC  jne      0x1801816ca                                -> VF5FS+0x1816CA
; ----------------------------------------------------------------------
; I.2  0x181FE0 : les SIX portes de la mise a jour par joueur  (40 instructions)
; ----------------------------------------------------------------------
--- VF5FS+0x181FE0 .. +0x18208C  (172 octets), plage DITE
  00181FE0  mov      dword ptr [rsp + 0x10], edx             
  00181FE4  push     rbp                                     
  00181FE5  push     rsi                                     
  00181FE6  push     rdi                                     
  00181FE7  push     r12                                     
  00181FE9  push     r13                                     
  00181FEB  push     r15                                     
  00181FED  lea      rbp, [rsp - 0x2f]                       
  00181FF2  sub      rsp, 0xa8                               
  00181FF9  movsxd   r15, edx                                
  00181FFC  mov      rsi, rcx                                
  00181FFF  xor      r12d, r12d                              
  00182002  mov      rcx, r15                                
  00182005  mov      r13d, r12d                              
  00182008  lea      rdi, [r15 + 2]                          
  0018200C  shl      rdi, 6                                  
  00182010  add      rdi, rsi                                
  00182013  cmp      byte ptr [rdi], r12b                    
  00182016  je       0x180182847                                -> VF5FS+0x182847
  0018201C  mov      eax, dword ptr [rdi + 0x20]             
  0018201F  cmp      eax, 6                                  
  00182022  je       0x180182847                                -> VF5FS+0x182847
  00182028  cmp      eax, 7                                  
  0018202B  je       0x180182847                                -> VF5FS+0x182847
  00182031  cmp      dword ptr [rdi + 0x28], 6               
  00182035  je       0x180182847                                -> VF5FS+0x182847
  0018203B  mov      rax, qword ptr [rdi + 8]                
  0018203F  test     rax, rax                                
  00182042  je       0x180182847                                -> VF5FS+0x182847
  00182048  cmp      qword ptr [rax], r12                    
  0018204B  je       0x180182847                                -> VF5FS+0x182847
  00182051  shl      rcx, 6                                  
  00182055  cmp      byte ptr [rcx + rsi + 0x81], r12b       
  0018205D  je       0x180182847                                -> VF5FS+0x182847
  00182063  mov      rax, qword ptr [rip + 0x2a6df6]            ; VF5FS+0x428E60  .rdata+0x428E60
  0018206A  cmp      byte ptr [rax + 0x139], r12b            
  00182071  jne      0x180182847                                -> VF5FS+0x182847
  00182077  cmp      byte ptr [rax + 0x13a], r12b            
  0018207E  jne      0x180182847                                -> VF5FS+0x182847
  00182084  mov      r9, qword ptr [rip + 0xb0be9d]             ; VF5FS+0xC8DF28
; ----------------------------------------------------------------------
; I.3  0x183110 : le poseur d'UN octet, et ses deux voisins  (23 instructions)
; ----------------------------------------------------------------------
--- VF5FS+0x183110 .. +0x183160  (80 octets), plage DITE
  00183110  movsxd   rax, edx                                
  00183113  shl      rax, 6                                  
  00183117  mov      byte ptr [rax + rcx + 0x81], r8b        
  0018311F  ret                                              
  00183120  sub      rsp, 0x28                               
  00183124  call     0x1801aa6c0                                -> VF5FS+0x1AA6C0
  00183129  test     eax, eax                                
  0018312B  je       0x180183141                                -> VF5FS+0x183141
  0018312D  sub      eax, 1                                  
  00183130  je       0x180183141                                -> VF5FS+0x183141
  00183132  sub      eax, 1                                  
  00183135  je       0x180183141                                -> VF5FS+0x183141
  00183137  cmp      eax, 1                                  
  0018313A  jne      0x180183141                                -> VF5FS+0x183141
  0018313C  add      rsp, 0x28                               
  00183140  ret                                              
  00183141  xor      eax, eax                                
  00183143  add      rsp, 0x28                               
  00183147  ret                                              
  00183150  mov      qword ptr [rsp + 0x18], rbx             
  00183155  mov      qword ptr [rsp + 0x20], rsi             
  0018315A  mov      qword ptr [rsp + 8], rcx                
  0018315F  push     rdi                                     
; ----------------------------------------------------------------------
; I.4  0x1833CC : l'aiguillage du pas du CONTENEUR (0x183390)  (28 instructions)
; ----------------------------------------------------------------------
--- VF5FS+0x1833CC .. +0x183450  (132 octets), plage DITE
  001833CC  mov      ecx, dword ptr [rbx + 0x58]             
  001833CF  xor      ebp, ebp                                
  001833D1  mov      qword ptr [rsp + 0xc0], r12             
  001833D9  mov      r13d, 1                                 
  001833DF  mov      qword ptr [rsp + 0x80], r15             
  001833E7  test     ecx, ecx                                
  001833E9  je       0x180183789                                -> VF5FS+0x183789
  001833EF  sub      ecx, r13d                               
  001833F2  je       0x18018376c                                -> VF5FS+0x18376C
  001833F8  sub      ecx, r13d                               
  001833FB  je       0x18018355a                                -> VF5FS+0x18355A
  00183401  sub      ecx, r13d                               
  00183404  je       0x1801834aa                                -> VF5FS+0x1834AA
  0018340A  cmp      ecx, r13d                               
  0018340D  jne      0x1801839ac                                -> VF5FS+0x1839AC
  00183413  cmp      byte ptr [rbx + 0x2e0], bpl             
  0018341A  je       0x180183456                                -> VF5FS+0x183456
  0018341C  mov      rcx, qword ptr [rip + 0xb0ab05]            ; VF5FS+0xC8DF28
  00183423  mov      rax, qword ptr [rcx + 0x1ff08]          
  0018342A  test     rax, rax                                
  0018342D  je       0x180183440                                -> VF5FS+0x183440
  0018342F  mov      rcx, qword ptr [rcx + 0x1ff10]          
  00183436  xor      r8d, r8d                                
  00183439  mov      edx, 7                                  
  0018343E  call     rax                                     
  00183440  movzx    r14d, r13b                              
  00183444  call     0x18017b830                                -> VF5FS+0x17B830
  00183449  mov      rcx, rax                                
; ----------------------------------------------------------------------
; I.5  0x18355A : sa phase 2 -- LE SEUL ARMEMENT du module  (66 instructions)
; ----------------------------------------------------------------------
--- VF5FS+0x18355A .. +0x183680  (294 octets), plage DITE
  0018355A  mov      rax, qword ptr [rip + 0x2a58ff]            ; VF5FS+0x428E60  .rdata+0x428E60
  00183561  cmp      byte ptr [rax + 0x139], bpl             
  00183568  jne      0x1801839ac                                -> VF5FS+0x1839AC
  0018356E  cmp      byte ptr [rax + 0x13a], bpl             
  00183575  jne      0x1801839ac                                -> VF5FS+0x1839AC
  0018357B  xor      edx, edx                                
  0018357D  lea      rcx, [rbx + 0x70]                       
  00183581  call     0x180181540                                -> VF5FS+0x181540
  00183586  movzx    r15d, al                                
  0018358A  lea      rcx, [rbx + 0x70]                       
  0018358E  xor      r15d, r13d                              
  00183591  xor      r8d, r8d                                
  00183594  mov      edx, r15d                               
  00183597  call     0x180183110                                -> VF5FS+0x183110
  0018359C  lea      rcx, [rbx + 0x178]                      
  001835A3  call     0x1802ccab0                                -> VF5FS+0x2CCAB0
  001835A8  test     al, al                                  
  001835AA  jne      0x180183650                                -> VF5FS+0x183650
  001835B0  lea      rcx, [rbx + 0x178]                      
  001835B7  call     0x1801df8e0                                -> VF5FS+0x1DF8E0
  001835BC  test     eax, eax                                
  001835BE  je       0x1801839ac                                -> VF5FS+0x1839AC
  001835C4  call     0x1800e1940                                -> VF5FS+0xE1940
  001835C9  cmp      dword ptr [rax], 8                      
  001835CC  jne      0x1801835e5                                -> VF5FS+0x1835E5
  001835CE  mov      ecx, 0xffffffff                         
  001835D3  call     0x18000ba20                                -> VF5FS+0xBA20
  001835D8  test     al, al                                  
  001835DA  je       0x1801835e5                                -> VF5FS+0x1835E5
  001835DC  cmp      byte ptr [rip + 0xb0a835], bpl             ; VF5FS+0xC8DE18
  001835E3  je       0x180183640                                -> VF5FS+0x183640
  001835E5  call     0x1801b2870                                -> VF5FS+0x1B2870
  001835EA  mov      r12d, eax                               
  001835ED  test     eax, eax                                
  001835EF  js       0x180183640                                -> VF5FS+0x183640
  001835F1  lea      rcx, [rbx + 0x178]                      
  001835F8  call     0x1801e0390                                -> VF5FS+0x1E0390
  001835FD  lea      rdx, [rip + 0x2a5584]                      ; VF5FS+0x428B88  "CANCEL_CAUTION"
  00183604  lea      rcx, [rbx + 0x178]                      
  0018360B  call     0x1802cd400                                -> VF5FS+0x2CD400
  00183610  mov      ecx, 0x400                              
  00183615  call     0x1802316e0                                -> VF5FS+0x2316E0
  0018361A  mov      edx, r13d                               
  0018361D  mov      qword ptr [rbx + 0x1e8], rax            
  00183624  lea      rcx, [rbx + 0x178]                      
  0018362B  call     0x1801e1700                                -> VF5FS+0x1E1700
  00183630  mov      dword ptr [rbx + 0x200], r12d           
  00183637  mov      byte ptr [rbx + 0x20d], r13b            
  0018363E  jmp      0x180183650                                -> VF5FS+0x183650
  00183640  movzx    r8d, r13b                               
  00183644  lea      rcx, [rbx + 0x70]                       
  00183648  mov      edx, r15d                               
  0018364B  call     0x180183110                                -> VF5FS+0x183110
  00183650  xor      edx, edx                                
  00183652  lea      rcx, [rbx + 0x70]                       
  00183656  call     0x180181540                                -> VF5FS+0x181540
  0018365B  mov      edx, r13d                               
  0018365E  lea      rcx, [rbx + 0x70]                       
  00183662  movzx    r15d, al                                
  00183666  call     0x180181540                                -> VF5FS+0x181540
  0018366B  xor      edx, edx                                
  0018366D  lea      rcx, [rbx + 0x70]                       
  00183671  movzx    esi, al                                 
  00183674  call     0x1801814f0                                -> VF5FS+0x1814F0
  00183679  mov      edx, r13d                               
  0018367C  lea      rcx, [rbx + 0x70]                       
; ----------------------------------------------------------------------
; I.6  0x183789 : sa phase 0 -- la COMMANDE 5  (19 instructions)
; ----------------------------------------------------------------------
--- VF5FS+0x183789 .. +0x1837F0  (103 octets), plage DITE
  00183789  cmp      byte ptr [rbx + 0x2e0], bpl             
  00183790  je       0x1801837d7                                -> VF5FS+0x1837D7
  00183792  mov      rcx, qword ptr [rip + 0xb0a78f]            ; VF5FS+0xC8DF28
  00183799  mov      byte ptr [rsp + 0xb0], bpl              
  001837A1  mov      rax, qword ptr [rcx + 0x1ff08]          
  001837A8  test     rax, rax                                
  001837AB  je       0x1801839ac                                -> VF5FS+0x1839AC
  001837B1  mov      rcx, qword ptr [rcx + 0x1ff10]          
  001837B8  lea      r8, [rsp + 0xb0]                        
  001837C0  mov      edx, 5                                  
  001837C5  call     rax                                     
  001837C7  cmp      byte ptr [rsp + 0xb0], bpl              
  001837CF  je       0x1801839ac                                -> VF5FS+0x1839AC
  001837D5  jmp      0x1801837fb                                -> VF5FS+0x1837FB
  001837D7  mov      ecx, 0x146                              
  001837DC  call     0x180196130                                -> VF5FS+0x196130
  001837E1  test     al, al                                  
  001837E3  jne      0x1801839ac                                -> VF5FS+0x1839AC
  001837E9  mov      ecx, 0x115                              
; ----------------------------------------------------------------------
; I.7  0x1B2870 : le decideur FUN_1801B2870, entier  (77 instructions)
; ----------------------------------------------------------------------
--- VF5FS+0x1B2870 .. +0x1B2980  (272 octets), plage DITE
  001B2870  mov      qword ptr [rsp + 0x18], rbx             
  001B2875  push     rbp                                     
  001B2876  push     rsi                                     
  001B2877  push     rdi                                     
  001B2878  sub      rsp, 0x20                               
  001B287C  call     0x18000ba20                                -> VF5FS+0xBA20
  001B2881  xor      edx, edx                                
  001B2883  movzx    edi, al                                 
  001B2886  lea      rbp, [rip + 0x5e3383]                      ; VF5FS+0x795C10
  001B288D  mov      r8d, edx                                
  001B2890  mov      ebx, 0xffffffff                         
  001B2895  lea      r11, [rip + 0x5e322c]                      ; VF5FS+0x795AC8
  001B289C  mov      r9, rbp                                 
  001B289F  lea      rsi, [rip + 0x5e30ba]                      ; VF5FS+0x795960
  001B28A6  cmp      byte ptr [r9], dl                       
  001B28A9  je       0x1801b28df                                -> VF5FS+0x1B28DF
  001B28AB  movsxd   r10, dword ptr [r11]                    
  001B28AE  mov      eax, 1                                  
  001B28B3  test     r10d, r10d                              
  001B28B6  mov      ecx, r10d                               
  001B28B9  cmovs    ecx, edx                                
  001B28BC  cmp      ecx, eax                                
  001B28BE  cmovl    eax, ecx                                
  001B28C1  cmp      r10d, eax                               
  001B28C4  jne      0x1801b28d0                                -> VF5FS+0x1B28D0
  001B28C6  imul     rcx, r10, 0x54                          
  001B28CA  mov      r10d, dword ptr [rcx + rsi]             
  001B28CE  jmp      0x1801b28d3                                -> VF5FS+0x1B28D3
  001B28D0  mov      r10d, edx                               
  001B28D3  mov      eax, edi                                
  001B28D5  xor      eax, 1                                  
  001B28D8  inc      eax                                     
  001B28DA  test     r10d, eax                               
  001B28DD  jne      0x1801b28f4                                -> VF5FS+0x1B28F4
  001B28DF  inc      r8d                                     
  001B28E2  inc      r9                                      
  001B28E5  add      r11, 0xd8                               
  001B28EC  cmp      r8d, 2                                  
  001B28F0  jb       0x1801b28a6                                -> VF5FS+0x1B28A6
  001B28F2  jmp      0x1801b28f7                                -> VF5FS+0x1B28F7
  001B28F4  mov      ebx, r8d                                
  001B28F7  mov      rcx, qword ptr [rip + 0xadb62a]            ; VF5FS+0xC8DF28
  001B28FE  cmp      qword ptr [rcx + 0x1ff08], rdx          
  001B2905  je       0x1801b2971                                -> VF5FS+0x1B2971
  001B2907  mov      dword ptr [rsp + 0x48], edx             
  001B290B  mov      byte ptr [rsp + 0x40], dl               
  001B290F  mov      rax, qword ptr [rcx + 0x1ff08]          
  001B2916  test     rax, rax                                
  001B2919  je       0x1801b2939                                -> VF5FS+0x1B2939
  001B291B  mov      rcx, qword ptr [rcx + 0x1ff10]          
  001B2922  lea      r8, [rsp + 0x40]                        
  001B2927  mov      edx, 0xf5                               
  001B292C  call     rax                                     
  001B292E  mov      edx, dword ptr [rsp + 0x48]             
  001B2932  mov      rcx, qword ptr [rip + 0xadb5ef]            ; VF5FS+0xC8DF28
  001B2939  mov      rax, qword ptr [rcx + 0x1ff08]          
  001B2940  test     rax, rax                                
  001B2943  je       0x1801b295c                                -> VF5FS+0x1B295C
  001B2945  mov      rcx, qword ptr [rcx + 0x1ff10]          
  001B294C  lea      r8, [rsp + 0x48]                        
  001B2951  mov      edx, 0xf6                               
  001B2956  call     rax                                     
  001B2958  mov      edx, dword ptr [rsp + 0x48]             
  001B295C  cmp      edx, 2                                  
  001B295F  jae      0x1801b2971                                -> VF5FS+0x1B2971
  001B2961  mov      ecx, edx                                
  001B2963  cmp      byte ptr [rcx + rbp], 0                 
  001B2967  je       0x1801b2971                                -> VF5FS+0x1B2971
  001B2969  cmp      byte ptr [rsp + 0x40], 0                
  001B296E  cmovne   ebx, edx                                
  001B2971  mov      eax, ebx                                
  001B2973  mov      rbx, qword ptr [rsp + 0x50]             
  001B2978  add      rsp, 0x20                               
  001B297C  pop      rdi                                     
  001B297D  pop      rsi                                     
  001B297E  pop      rbp                                     
  001B297F  ret                                              

; ######################################################################
; ## J. LA CAUSE : [rbx+0x2e0] EST NOTRE PROPRE REPARTITEUR  (SS 419.146)
; ######################################################################
;
; `FUN_1801844E0`, creneau +0x08 de la vtable `VF5FS+0x429D98` :
;
;     001844F2  mov   rax, [rip+0xb09a2f]     ; VF5FS+0xC8DF28, notre bloc
;     001844F9  mov   rdx, [rax + 0x1ff08]    ; LE REPARTITEUR
;     00184503  setne al                      ; al = (repartiteur pose ?)
;     00184506  mov   byte [rcx + 0x2e0], al
;     0018450F  je    0x180184638             ; nul -> l'autre chemin
;
; `qui_ecrit_champ.py 0x2e0` : seuls DEUX ecrivains de ce champ sont dans
; cette classe -- le constructeur `0x1832E7` (`sil`, mis a zero en 0x18318B)
; et celui-ci. Donc `[rbx+0x2e0]` est l'EMPREINTE DE NOTRE REPARTITEUR, prise
; une fois au creneau +0x08. Ce n'est ni une resolution, ni un mode de borne.
;
; LA CHAINE DU DEFAUT, DE BOUT EN BOUT :
;   1. nous posons bloc+0x1FF08        -> [rbx+0x2e0] = 1
;   2. phase 0 prend le chemin HOTE    -> poste la COMMANDE 5
;   3. notre hote ne gere pas la 5     -> l'octet revient NUL -> elle sort
;   4. le pas n'atteint jamais sa PHASE 2, seul endroit qui ecrive [rec+1]=1
;   5. la phase 2 de SEL_CHARA efface [rec+1] a CHAQUE IMAGE
;   6. FUN_180181FE0 sort a sa 5e porte, deux ports, chaque image.
;
; CE QUE L'ORACLE REPOND (cmd_oracle.py 5 -> 0x1415CAF55 -> 0x1416E7E20) :
;
;     rbx = args
;     si [rip+0x1693ca8] != 0 : rax=[rcx] ; rdx=rbx ; call [rax+8]  <- ECRIT
;     si [rip+0x1693c9b] != 0 : si FUN_14105E3D0()==0 : [rbx]=0     ; VETO
;     si [rip+0x1693c8c] != 0 : si FUN_14105E3D0()==0 : [rbx]=0     ; VETO
;
; LE FORMAT EST MESURE : un octet en args[0], zero = non. LA VALEUR NON :
; elle sort d'une methode virtuelle d'un singleton non resolu.
;
; ######################################################################
; ## CE QUI RESTE A LIRE  (revu au 419.139)
; ######################################################################
;
; 1. LE PILOTE du creneau +0x08 : **TROUVE ET MESURE** au SS 419.138.
;    C'est FUN_1802CD130, qui repartit sur `[tache+0x18]` : 1 appelle
;    +0x08, 2 appelle +0x10, 3 appelle +0x18. La mesure a nomme la tache
;    (<< SELECTOR >>, rang 16), son objet (le singleton [VF5FS+0x7598B8])
;    et sa table (VF5FS+0x428260), et les 20 taches etaient a la phase 2.
;    Comme `+0x18` ne passe a 2 QUE dans la branche
;    `[+0x18]==1 && vt[+0x08]() != 0`, **le creneau +0x08 a tourne** :
;    0x17B850 a bien demande les six jeux.
;
; 2. LA METHODE +0x10 de l'objet AET (section B.5), pour savoir si
;    0x2488A0 est bien elle. Toujours non lue.
;
; 3. 0x19B490, le saut terminal du chargeur sprite. Toujours non lu --
;    mais ce n'est plus la piste principale : l'erratum 419.139 dit que
;    le chargement a ABOUTI (+0xB8 = 1, +0x20 = 2).
;
; 4. 0x17B280, la phase 2 : il rend 0 tant qu'il n'est pas pret, et
;    personne ne l'a lu. C'est lui qui precede la double porte.
;
; CIBLE, REVUE : non plus << faire tourner 0x17B850 >> -- il tourne, et
; il charge -- mais **ouvrir la double porte** : faire en sorte que
; `[[VF5FS+0x73D9D8]+0x0C]` et `+0x0D` soient non nuls au moment ou le
; sous-etat 19 phase 0 ouvre le selecteur, pour que `[sel+0x5d]` et
; `[sel+0x5e]` passent a 1 et que la phase 7 -- celle qui monte
; "chara_start", "loop_start", "loop_end" et "bg_light_change" -- soit
; enfin atteinte. A MESURER AVANT D'AGIR : les six octets ci-dessus.
