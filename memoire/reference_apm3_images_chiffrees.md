---
name: reference_apm3_images_chiffrees
description: "Les ISO « ALL.Net P-ras Multi » sont chiffrées de bout en bout ; les douze clés du dossier key/ n'y suffisent pas."
metadata: 
  node_type: memory
  type: reference
  originSessionId: b15ec65b-bb70-48a3-8142-3934113e3c96
  modified: 2026-09-05T21:25:41.329Z
---

Les deux images de `C:\Users\frede\Desktop\VF5 FS DECOMP` — `ALL.Net P-ras
Multi Version 2 (Japan).iso` (507 Mo) et `… (Rev A).iso` (1005 Mo, extraite le
2026-09-05) — sont **chiffrées de l'octet 0 à la fin**. Entropie 7,92 partout,
aucun `CD001`, aucun en-tête NTFS.

Ce qui est **mesuré**, pas supposé :

- Le chiffrement **redémarre tous les 2048 octets** (un secteur). Deux secteurs
  de même contenu clair donnent le même chiffré, à l'octet près.
- Les 128 blocs de 16 octets d'un tel motif sont **tous distincts** : chaînage
  de blocs (CBC à VI constant), pas ECB, pas un masque XOR — le XOR du motif
  contre les autres secteurs ne rend que du bruit.
- Les secteurs 0 et 16 sont **identiques d'une image à l'autre** ; le secteur 1
  ne l'est déjà plus.

Les douze fichiers de `key\` se lisent **16 octets de clé + 16 octets de VI**
(disposition confirmée par l'outillage SEGA public : le VI y est calculé pour
que le premier bloc rende l'en-tête NTFS connu). Les huit `*_OPT.BIN` partagent
la même clé `5c84a9e7 26eaa5dd 351f2b07 50c23697` et ne diffèrent que par le VI.
**Aucune des douze ne déchiffre ces images** — ce sont des clés de jeux
(`SDGM`/`SDHF`/`SDHP`/`SDHV`/`SDHW`), pas du disque système.

La mécanique de montage est nommée dans `APM_V1.04_internal_0\Apmv3System_Data\
Managed\Assembly-CSharp.dll`, classe `Apm.System.Util.AppMounter` :
`ApmSys_mountFscrypt(fscryptImagePath, mountFolderPath)`, `ApmSys_mountVhd`,
points de montage `C:\Mount\Apm` et `C:\Mount\Option\`, volumes
`internal_0.vhd` / `internal_1.vhd` (d'où le nom du dossier
`APM_V1.04_internal_0`), motif `SDEM_*_*_*.opt` — **`SDEM` est le code du
système APM lui-même**. Les champs voisins sont `titleKey`, `bEncrypt`,
`keychipId` : **la clé vient de la puce, pas du disque**. C'est le verrou.

L'implémentation native est dans `lib\apm.dll`, mais ses 106 exports ne
montrent ni `mount` ni `crypt` : le déchiffrement n'y est pas exporté, il
faudrait le désassembler. Voir [[reference_vf5_stub_entrees]] pour ce que cette
DLL fait déjà chez nous.

Voir aussi [[project_vf5_re]], [[reference_reprise_vf5]],
[[feedback_chercher_avant_de_retroconcevoir]].
