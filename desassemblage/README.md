# Le désassemblage déposé

Régénéré par `py -3 tools/deposer_disasm.py`, jamais édité à la main.
La liste des fonctions vit dans l'outil, en clair, avec pour chacune ce
qu'elle sert et où elle est racontée.

Ce dossier existe parce que les séances d'octobre n'avaient laissé que des
extraits cités dans `REPRISE.md`. Un extrait prouve ce qu'on en dit ; il ne
permet pas de relire la fonction, ni de voir ce qu'on n'avait pas remarqué.

## APM3 — la borne

- [`selitem_update.txt`](selitem_update.txt) — `0x1801C7440`, 544 octets. TaskSelItemMenu::update.
- [`selitem_consommateur.txt`](selitem_consommateur.txt) — `0x1801C7B50`, 288 octets. LE CONSOMMATEUR DE MESSAGE MORT de « select item », et la piece maitresse : en 0x1801C7B83 il fait d'un index ABSOLU le couple (position +0x9D0, defilement +0x9C8) -- ecretage au total et pas de huit compris.
- [`selitem_dessin.txt`](selitem_dessin.txt) — `0x1801C8110`, 352 octets. Le dessin de la grille.
- [`selpart_curseur.txt`](selpart_curseur.txt) — `0x1801C7D00`, 608 octets. Le curseur de « select part ».
- [`selpart_dessin.txt`](selpart_dessin.txt) — `0x1801CA040`, 976 octets. Le dessin de « select part ».
- [`resolveur_objset.txt`](resolveur_objset.txt) — `0x180217E70`, 544 octets. Le resolveur de nom d'objset, par dichotomie dans une table TRIEE de 0x35E = 862 entrees basee en 0x18054BB30.
- [`chargeur_archive.txt`](chargeur_archive.txt) — `0x180038600`, 640 octets. Le demandeur d'archive d'objets, mesure a la sonde : c'est lui qui demande `objset/akiitm` et `objset/akiitm_patch` (site d'appel 0x180038803).
- [`aet_marqueurs_customize.txt`](aet_marqueurs_customize.txt) — `0x1801CBFE0`, 256 octets. Ce qu'on avait pris pour le chargeur du modele au changement de categorie : c'est l'animation 2D de la fenetre.
- [`itmeq_update.txt`](itmeq_update.txt) — `0x1801C13B0`, 896 octets. customize::ItmEqTask -- LA TACHE QUI EQUIPE UN OBJET (vtable 0x180530D10, creneau 2, trouvee par le RTTI).
- [`itmeq_basculement.txt`](itmeq_basculement.txt) — `0x1801CE400`, 96 octets. 0x1801CE400 -- CE QUI REND L'OBJET VISIBLE, et il n'equipe rien : il BASCULE le modele affiche.
- [`taskrobsingle_update.txt`](taskrobsingle_update.txt) — `0x180151CF0`, 384 octets. TaskRobSingle::update (vtable 0x1803F8E68, creneau 2).
- [`publieur_joueur.txt`](publieur_joueur.txt) — `0x1801437E0`, 288 octets. Le publieur de la structure joueur : il recopie les champs d'un objet source dans [0x180C3B6F0] + index*0xFA88.
- [`itemmain_update.txt`](itemmain_update.txt) — `0x1801C2EC0`, 256 octets. customize::ItemMain::update -- le PILOTE de la tache d'equipement.
- [`repartiteur_curseur.txt`](repartiteur_curseur.txt) — `0x1801BBBE0`, 384 octets. Le repartiteur de curseur, celui que toutes les pages de personnalisation appellent.

## Xbox 360 — la console Final Showdown

`extracted/X360_FS/sel/default.img` — elle porte `VF5FS`, `FINAL SHOWDOWN` et
`takitm`, et l'espace de noms `customize::`, le même qu'APM3. **Ce n'est pas**
la console de 2007 : celle-là est `extracted/X360_VF5/vf5_x360.img`.
Une image ne se nomme pas par son dossier.

- [`x360_grille_deplacement.txt`](x360_grille_deplacement.txt) — `0x82230818`, 180 instructions. LE PRODUCTEUR, cote console : quatre blocs, un par direction, sur HUIT colonnes et une fenetre de 0x28 = quarante cases.
- [`x360_page_update.txt`](x360_page_update.txt) — `0x82231A50`, 170 instructions. La mise a jour de la page.
- [`x360_repartiteur.txt`](x360_repartiteur.txt) — `0x82217B30`, 120 instructions. TaskCsMenu::update cote console -- LA PIERRE DE ROSETTE : curseur V/H en +0x4C/+0x50, comptes en +0x1B4/+0x1BC, bouclages en +0x1B8/+0x1C0.
- [`x360_itmeq_update.txt`](x360_itmeq_update.txt) — `0x82229750`, 260 instructions. customize::ItmEqTask::update cote CONSOLE (vtable 0x820113C0, creneau 2), trouvee par `tools/x360_rtti.
- [`x360_taskrobsingle_update.txt`](x360_taskrobsingle_update.txt) — `0x82356840`, 110 instructions. TaskRobSingle::update cote console (vtable 0x820B20F4, creneau 2).

## Lindbergh — la borne d'avant

`extracted/LIND_FS/sel/vf5` — ELF x86 32 bits, `rom_version` 2010, `libsama.so` :
un binaire **d'arcade**. Espace de noms `terminal::`, et les libellés de
tâches en clair à côté des noms de types (`TERMINAL_ITEM_EQUIP`).
La personnalisation n'est donc pas une exclusivité console.

- [`lind_itmeq_update.txt`](lind_itmeq_update.txt) — `0x849893C`, 170 instructions. terminal::ItmEqTask::update sur la borne LINDBERGH (vtable 0x089AD9E8, creneau 3 -- GCC pose DEUX destructeurs, le numero de creneau ne se transpose pas).
