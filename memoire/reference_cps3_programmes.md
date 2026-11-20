---
name: reference-cps3-programmes
description: "Lire les programmes d'arcade CPS3 : 2nd Impact n'est pas chiffre, les cles sont dans mame.exe, et les deux tableaux maitres de personnages."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1b6a7297-36d0-4db2-9df6-56a319b1221c
  modified: 2026-09-01T16:45:16.561Z
---

**Le programme de 2nd Impact n'est PAS chiffre.** L'entrelacement brut des quatre
`sfiii2-simm1.*` donne deja le vecteur `0x06000EA0`. Seul 3rd Strike l'est
(cles `0xA55432B4 / 0x0C129981`, algorithme dans `src/arcade/cps3_decrypt.c`).

**Les cles CPS3 se lisent dans `mame.exe`** : les amorces des jeux sont a la file vers
`0xBEB730`, chacune `mov edx, cle1 ; mov r8d, cle2`. Chercher les octets d'une cle connue
et lire les voisines. Celle de `sfiii2` y est `0 / 0`.

**Tableaux maitres de personnages** (lignes de `0x6C` = 24 pointeurs de section +
`CharInitData2`) : 3rd Strike `0x18B1B4`, 23 lignes ; 2nd Impact `0x1529C4`, 17 lignes.
Les dix-sept premieres sont le meme roster dans le meme ordre. Akuma = ligne 15,
Shin Akuma = ligne 16 dans les deux. **La numerotation des sprites est commune aux deux
jeux** (temoins : Ryu 630/639 `cg` communs, Ken 588/597).

**Why :** ca ouvre la comparaison directe entre les deux jeux sans passer par les disques
Dreamcast, et sans savestate.

**How to apply :** outils dans `Downloads\3sx-outils\shin-akuma\` (`shin.py`,
`comparer.py`). **Le piege** : Shin Akuma est le dernier personnage de son bloc dans les
deux jeux, et ce qui suit son `cbca` est un jeu d'animations autonome — la methode des
frontieres l'avale et le lecteur de scripts invente des centaines de sprites. Voir
[[project-shin-akuma]] et [[reference-coherence-nest-pas-role]].
