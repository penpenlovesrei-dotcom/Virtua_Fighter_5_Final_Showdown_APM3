---
name: reference-2i-objet-est-un-work
description: "Un objet de SF3 2nd Impact est le même WORK que le port porte en C ; son +8 est l'id qui choisit sa routine d'effet."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 879a3b00-23a6-411b-9fa5-103162735ed3
  modified: 2026-09-03T08:43:49.804Z
---

Un objet de *2nd Impact* est le **même `WORK`** que 3SX porte en C (`src/structs.h`) — la
disposition se recoupe champ par champ avec ce que les spawners écrivent :

    +0 be_flag  +1 disp_flag  +4 type  +6 work_id  +8 id
    +32 dead_f  +36 routine_no[8]  +52 old_rno[8]  +68 hit_stop  +72 cgromtype

`+8` est l'**id** et indexe la table des routines d'effet, **`0x8C179FDC`, 196 entrées**,
lue par le répartiteur `0x8C0215E0`. Le tas d'objets est `0x8C6466EC`, 2048 octets chacun.
Contrôle : chaque spawner est écrit **juste après sa routine** (id 18 → `0x8C028510` puis
`0x8C028792` ; id 66 → `0x8C03215C` puis `0x8C0323F0` ; id 87 → `0x8C0363A4` puis
`0x8C036480`).

La routine appelle une **seconde** routine choisie par le champ `+38` du bloc, via une
table (`0x8C5F9FB4` pour l'id 66, `0x8C5F9EA4` pour l'id 18) ; c'est elle qui pose le
script en appelant `0x8C0B4AD4` (`objet+456 = numéro de script`).

**Pourquoi :** j'ai conclu à tort que deux lecteurs « ne faisaient pas d'objets animés »
parce qu'ils n'écrivaient pas `+456`. Un balayage qui suit les `jsr` par leurs littéraux
rate une routine atteinte **uniquement par une table**, même en profondeur 3.

**Comment l'appliquer :** quand une chaîne s'arrête sur « cette fonction n'écrit pas X »,
vérifier d'abord qu'aucune table de pointeurs n'a été laissée de côté — **une table de
pointeurs est un appel**. Voir [[reference-tables-indexees-par-personnage]] et
[[reference-decors-doc-unique]].
