---
name: reference-sn-operator-protocole
description: "Disposition de la réponse 0x04 du SN Operator, établie sur 11 cartouches ; checksum 0000 = slot vide."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 633fc950-d752-4e5d-9a3f-2ee9fe13d331
  modified: 2026-08-22T06:30:44.488Z
---

Réponse à la commande `0x04` du SN Operator (512 octets), établie le 22/08/2026 en confrontant **11 cartouches de 512 Ko à 4 Mo** au catalogue GameDB-SNES :

```
byte[2]      0x50 si cartouche présente
byte[5]      exposant de la taille, EN OCTETS   (2^20 = 1 Mo)
byte[6:8]    0x0D21 si pile de sauvegarde
byte[13:15]  checksum 16 bits, petit-boutiste
byte[16]     le même exposant, en kilo-octets   (= byte[5] - 10)
byte[17]     caractère 0 du titre interne
byte[18]     caractère 6 du titre interne
```

Au-delà de l'octet 33, **tout est à zéro**. Le lecteur ne relaie PAS l'en-tête de la cartouche : le titre complet n'est nulle part dans les 512 octets, inutile de l'y chercher.

**`byte[2] == 0x50` ne suffit pas à conclure qu'une cartouche est là.** Slot vide, le lecteur répond quand même « présent » avec un enregistrement à zéro, donc **checksum `0000`**. Un checksum nul vaut absence. Sans ce garde-fou le retrait n'est jamais annoncé, et `0000` passe pour un vrai jeu — il avait fini enregistré comme « Rockman X2 » dans la base utilisateur.

**Le checksum est celui de l'en-tête SNES** (somme des octets de la ROM sur 16 bits, pas un hachage). Il est donc publié par [[reference-gamedb-snes]] pour chaque jeu. 111 checksums sur 3 314 désignent plusieurs jeux ; **l'empreinte de deux caractères (byte 17 + byte 18) en sépare 104**, le titre complet en séparerait 111 mais il est inaccessible.

Deux erreurs que j'ai commises et qu'il ne faut pas refaire : conclure que `byte[5]` était constant après **deux** cartouches de même taille (il fallait en insérer une d'une autre taille), et chercher le titre complet par balayage ASCII alors qu'il n'y en a pas.

Voir [[project-cartridgeshelf-settings]], [[reference-playnite-sdk-settings]].
