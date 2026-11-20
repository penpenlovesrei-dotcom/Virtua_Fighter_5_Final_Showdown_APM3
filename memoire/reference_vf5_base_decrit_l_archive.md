---
name: reference_vf5_base_decrit_l_archive
description: "auth_3d_db doit décrire l'archive POSÉE, pas la liste du modèle ; et son champ `size` est le play_control.size du .a3da."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f95243fb-8203-4006-9dcc-187781c1c519
  modified: 2026-09-10T22:18:37.814Z
---

`decor_neuf.py` ne declarait dans `auth_3d_db` que les animations **que le
modele de Final Showdown declarait**. Sur le sanctuaire d'Aoi :

    EFFSTGJIN (FS)    7 animations
    EFFSTGJN5.farc   10 fichiers  ->  5 declarees, 5 INVISIBLES

`EFF_ARUKI_A/_B/_C`, `EFF_TALK` et `EFF_IKE` etaient dans l'archive posee et
n'entraient jamais dans la base : aucun mecanisme ne pouvait les atteindre, et
`animations_en_plus()` ne les voyait meme pas. Symptome a l'ecran : « il manque
les personnages en 3D dans le decor ».

**Une base decrit ce qui est POSE, pas ce que le modele demandait.** Declarer un
uid ne le joue pas -- c'est la liste d'animations du decor (0x18034FD20) qui
decide, via [[feedback_registre_pas_regle]].

Le champ `size` d'un uid n'est pas la taille du fichier : c'est **exactement le
`play_control.size` du `.a3da`** (mesure sur les douze uid d'EFFSTGAR5 :
ARUKI 3901, ARUKI_B 7021, KANKYAKU 241, TOIKI 30). Il se LIT dans le `.a3da`.

Le meme `play_control.size / fps` donne la DUREE, utile pour distinguer un
one-shot d'une boucle -- mais elle ne prouve rien a elle seule (DENKI_B fait
2,7 s et Final Showdown le joue en boucle).

Voir [[reference_vf5_obj_db]], [[reference_vf5_taches_effet]].
