# Brume du décor d'Aoi — désassemblages de la Lindbergh VF5 R

Déposé le 2026-11-19. Analyse : `../../analysis/brume_decor_aoi.md`.

Binaires lus (aucun exécuté) :

| ce qui est lu | où |
|---|---|
| ELF Lindbergh VF5 R, x86-32, 9 879 376 o | `VF5RE/extracted/LIND_R/id/disk0/vf5` |
| `/shader.farc` de VF5 R, 3 487 785 o, **sorti pour cette analyse** de l'image ext2 `vf5r_rom.bin` (`tools/ext2.py sortir`) | 4 067 programmes ARB |
| `/rom/shader.farc` de Final Showdown Lindbergh | `VF5RE/extracted/LIND_FS/tree/disk1/rom/shader.farc`, 2 724 programmes ARB |
| `w64/shader_pxd_w64.farc` du build Windows | 3 950 blobs DXBC — **c'est la seule archive que la DLL nomme** |
| `vf5fs-pxd-w64-Retail_APM3.dll.origine` | tables de présence, déclaration des `env` |

## Les fichiers

| fichier | contenu |
|---|---|
| `vf5r_appliquer_groupe_0811715E.txt` | la fonction qui applique **un groupe** de `fog_*.txt` ; groupe 0 → brouillard GL + `env[4]`, groupe **1 → `env[14]` sommet + `env[11]` fragment**, groupe 2 → `env[19]` |
| `vf5r_accesseurs_groupe_081170D0.txt` | les six accesseurs de l'enregistrement de 0x24 octets (type, densité, début, fin, index de brouillard, couleur) |
| `vf5r_appelant_pass_decor_08142229.txt` | la passe de décor, qui appelle `0x0811715E(0)`, `(1)`, `(2)` à chaque trame |
| `vf5r_defaut_groupe_081174A8.txt` | la remise à zéro d'un groupe — donne la disposition des champs en clair |
| `arb_modes_brouillard_vf5r_vs_fs.txt` | les quatre modes de brouillard côté ARB, VF5 R contre Final Showdown |
| `apm3_dxbc_stage_blinn_vp_modes_0a3.txt` | les quatre modes, côté DXBC du build Windows — **le mode 2 y pose `mov o1.w, l(0)`** |
| `apm3_dxbc_stage_blinn_fp_modes_1et2.txt` | les deux fragments : un seul dword d'écart (`cb[0][4]` → `cb[0][11]`) |
| `apm3_dxbc_blinn_per_vert_vp_modes_1et2.txt` | le témoin **intact** du même build : `max o2.x, r0.w, r1.x` |
| `apm3_dxbc_stage_blinn_signatures.txt` | signatures ISGN/OSGN, identiques entre les deux modes |
| `apm3_presence_nuanceurs.txt` | les 50 sous-nuanceurs de la DLL, et pour chacun les permutations réellement chargées |
| `apm3_declarer_env_1800F2470.txt` | la fonction APM3 qui déclare et marque les registres `env` depuis le masque `[rdi+0x1C]` |
| `donnees_groupe1_densite.txt` | quels décors ont un groupe 1 actif, des trois côtés |

## Les outils (jetables, posés ici pour pouvoir refaire la mesure)

    py -3 outil_lind_r.py appels 0x08053A98        qui appelle (ELF VF5 R)
    py -3 outil_lind_r.py func   0x0811715E --max 420
    py -3 outil_sm5.py   <blob .vp/.fp>            desassemble le DXBC
    py -3 outil_dxbc_sig.py <blob>                 ISGN / OSGN
    py -3 outil_presence_nuanceurs.py <dll>        les tables de presence

`outil_sm5.py` est un désassembleur SM4/5 minimal : il ne couvre que les opcodes
rencontrés ici, et l'opérande `IMMEDIATE32` est rendu de façon approximative
quand il n'a qu'une composante (il s'affiche `(0)`). Les conclusions de la note
ont toutes été recoupées sur les **dwords bruts**.
