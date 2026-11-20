---
name: reference_vf5_reseau
description: "VF5 APM3 — le netcode de bornes liées est INTACT dans le binaire, et c'est du STUN/TURN standard (am::abaas, pas « AVLink ») ; le rollback de REVO, lui, est absent."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7b8919f9-a3c9-4e11-a256-ad9c22b4c7e9
  modified: 2026-09-05T16:18:01.323Z
---

Pour ajouter du jeu en ligne à VF5 APM3, **il n'y a rien à écrire ni à
transplanter : le netcode de bornes liées est déjà dans le binaire.**

**Le nom n'est pas `AVLink*`** — corrigé le 2026-09-05. Le `AV` était la lettre
de classe du mangling MSVC (`.?AV`), pas un préfixe de nom. Le vrai espace de
noms est **`am::abaas`** (ALL.Net) : `am::abaas::LinkMainStateStartup`,
`Setup`, `Standby`, `Unavailable`, `MatchingAllocate`, `MatchingChannelBind`,
`MatchingConnectivityCheck`, `MatchingMatch`, `MatchingQualityCheck`,
`MatchingWaitReady`, `Playing`, `PlayEnd`, `CleanupMatch`, plus
`LinkReceiveThread`, `LinkSend`, `link::HttpData`, `link::Request`,
`link::Task`.

**Et c'est du STUN/TURN STANDARD**, ce qui est la vraie bonne nouvelle :
`ULinkPacketBindingRequestStun` / `BindingResponseStun` (RFC 5389),
`ULinkPacketAllcoateTurn` (sic), `RefreshTurn`, `ChannelBind` et leurs réponses
(RFC 5766), attributs `AttrHMAC` (MESSAGE-INTEGRITY), `AttrErrorCode`,
`AttrChannelNumber`, `AttrResponseLifeTime` ; processeurs `VStunChecker`,
`VConnectivityChecker`, `VConnectivityResponder`, `VLineQualityChecker`. SEGA
n'a pas écrit un protocole maison : la borne perce le NAT avec STUN et relaie
par TURN. **Un serveur TURN libre (coturn) existe déjà** — même leçon que SLLZ,
voir [[feedback_chercher_avant_de_retroconcevoir]].

`ULinkPacketAppData` porte les données de jeu ; savoir s'il transporte des
**entrées** ou un **état** décide de la latence tolérable, donc de tout.

Le transport est câblé : le moteur importe **quatorze fonctions de `ws2_32`**
(`socket`, `connect`, `sendto`, `recvfrom`, `WSAIoctl`…). `vfes.exe` n'en
importe aucune — le réseau est dans le moteur, pas dans l'hôte.

**Trois lignées, trois netcodes** : R.E.V.O. a du rollback + EOS (absent d'APM3 :
zéro `Rollback`, zéro `EOS_`, zéro `SteamAPI`) ; PS3/360 a du retard via
PSN/Live (mode 7 `ONLINE` bouchonné aux trois gestionnaires) ; la borne a les
bornes liées, pair à pair, et c'est celui-là qui a survécu.

**Le déterminisme est prouvé par le jeu lui-même** : il sait rejouer un combat
(`AVTaskGameVsReplay`, `AVTaskRobShortReplay_Rec`, scènes `REPLAY_VS`,
`ROB_SHORT_REPLAY_REC`, `TERM_REPLAY_BUF`). Un rejeu suppose une simulation
déterministe pilotée par des entrées enregistrées — prérequis de tout netcode.

**How to apply:** ne pas transplanter le rollback de R.E.V.O. — les deux DLL
sont des frères aux dispositions différentes (sous-page active en `+0x608`
contre `+0x650`), le code compilé ne se relocalise pas, et ce serait recopier du
code de SEGA. Ne pas écrire un lockstep de zéro non plus. Réveiller ce qui est
là : trouver où la machine s'arrête, monter un STUN/TURN à nous, et répondre
depuis notre `apm.dll` — c'est le rôle qu'elle tient déjà pour les entrées et
les pièces. C'est aussi ce que fait YAMPnet : tunneliser le protocole natif
plutôt que le réécrire.

La table RTTI se régénère par `py -3 tools/rtti.py --out analysis/rtti_apm3.txt`
(534 vtables) — voir [[reference_rtti_msvc_du_moteur]]. Détail :
`analysis/reseau.md` et `analysis/reseau_*.md`. Voir
[[project_vf5_mode_console]], [[reference_vf5_pxd_pierre_de_rosette]].
