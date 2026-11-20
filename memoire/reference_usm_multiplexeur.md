---
name: reference_usm_multiplexeur
description: "SFD → USM est un REMBALLAGE, pas une conversion : les deux portent du MPEG-1 + ADX, donc zéro perte (MD5 identiques)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-07T22:33:09.251Z
---

Écrit le 2026-09-08 : `tools/usm_mux.py`, lanceur `tools/sfd_vers_usm.cmd`
(glisser-déposer ou double-clic). Lecteurs séparés : `tools/sfd.py`,
`tools/usm.py`.

**Le fait qui décide de tout** : `VIDEO_HDRINFO.mpeg_codec = 1`
(Sofdec.Prime) est du **MPEG-1** — vérifié sur `vf5adv.usm`, qui ne contient
aucun code d'extension MPEG-2 (`00 00 01 B5`) — et `AUDIO_HDRINFO.audio_codec
= 2` est de l'**ADX**. Un `.sfd` porte déjà exactement ces deux flux. Il n'y a
donc rien à convertir : on démultiplexe le MPEG-PS et on remballe.

**Preuve** : le flux vidéo et le flux ADX ressortis du `.usm` produit ont le
même MD5 que ceux du `.sfd` d'origine (`vf5moe` : 52 209 294 o,
`4d9bef4b…` ; `vf5verBadv` : 206 916 206 o). Pas un octet perdu. C'est la
différence avec `medianoche.exe` du dossier « MP4 to USM », qui décode et
réencode en H.264.

Trois mesures faites sur les films du jeu, plutôt que supposées :

* **une image par morceau `@SFV`** (7304 morceaux pour `total_frames = 7304`) ;
* un morceau `@SFA` = **50 blocs ADX = 1600 échantillons** ; le premier ne
  porte que l'en-tête ADX ;
* `VIDEO_SEEKINFO.ofs_byte` = offset **absolu dans le fichier**, une ligne par
  début de GOP.

**Le multipiste est géré.** Un `.sfd` peut porter un conteneur **AIX** — le
multipiste de CRI : des morceaux `AIXP` entrelacés, chacun étiqueté du numéro
de son flux (`+0x08`), avec sa longueur utile en `+0x0A` et le nombre de flux
en `+0x40` de l'en-tête `AIXF`. Recoller flux par flux les charges utiles rend
des ADX complets, qui deviennent autant de **voies `@SFA`** — le mécanisme
multipiste de Sofdec2. `vf5verBadv` sort en **quatre voies**, les quatre
identiques à la source, et les trois flux AIX ont bien des empreintes
différentes. `--pistes N` limite le nombre de voies.

Réserve restante : le champ `date` de CRI avance à **moitié** du temps réel
côté vidéo (juste côté audio) — on reproduit sa convention, `--dates justes`
fait l'autre.

**How to apply:** le dump `X360_VF5` a cinq films absents d'APM3, dont
`vf5verBadv` et `vf5verCadv` **au format exact d'APM3** (1280×720, 60/s). Ils
se déposent librement : `rom/movie` est lu sur le disque, pas dans le `.par`
(voir [[project_vf5_import_5r]]). Rien n'a encore été joué dans le jeu.
Document : `analysis/films_usm.md`.
