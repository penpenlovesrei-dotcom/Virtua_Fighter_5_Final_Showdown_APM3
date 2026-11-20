---
name: reference_apm3_interface
description: "APM3 — le système ALL.Net P-ras Multi : seul amdaemon.exe sort sur le réseau, game.bat est destructeur, et le doc qui fait foi est analysis/interface_apm3.md."
metadata:
  node_type: memory
  type: reference
  originSessionId: 3f8eb787-b241-465e-a563-2b3ce8d7c55e
  modified: 2026-09-09T17:25:47.862Z
---

Dossier `…\VF5 FS DECOMP\APM_V1.04_internal_0` (241 Mo) : le **système
d'exploitation d'arcade** qui entoure le jeu, pas un jeu. Document qui fait
foi : **`analysis/interface_apm3.md`**.

**LE RÉSEAU : UN SEUL BINAIRE SORT.** `amdaemon.exe` porte les sept domaines
ALL.Net (`aime.naominet.jp`, `naominet.jp`, `at.sys-all.net`,
`amlog.sys-all.net`…) et `connect` / `WinHttpOpen` / `getaddrinfo` / `send`.
`Apmv3System.exe` et `emoneyUI.exe` (Unity 2017.3) n'ont **aucune API
réseau** — ils parlent au démon en local. Et **`firewall.cfg` du système ne
contient qu'une ligne : `x:\amdaemon.exe`**. Lancer les deux applications sans
le démon est donc hors ligne par construction : mesuré, 0 connexion, elles
s'arrêtent seules en 8 et 17 s (code 0) sur leur propre écran d'erreur.
`tools/apm_hors_ligne.cmd` le refait, en bac à sable.

**`game.bat` NE DOIT JAMAIS ÊTRE LANCÉ** : il efface `Y:\`, écrit dans
`HKLM\System\SEGA\…` et **flashe** les micrologiciels de la carte USB IO, de la
carte LED (COM2, 115200) et de la dalle tactile.

**`lib/apm.dll` est le vrai `apm.dll`** que `vfes.exe` importe — identique à
notre `apm.reelle.dll` (sha256 `a91ca49bbe728413b873`), comme `apmgamepad.dll`
(`92fe8f90b508d1a90e74`). Voir [[reference_vf5_stub_entrees]].

**Le contenu, mesuré** : 109 textures Unity (96 extraites, 13 en BC7 non
décodé) ; 78 PNG dont **13 distincts** — les logos e-money nanaco / 楽天Edy /
iD / 交通系 / WAON / PASELI / SAPICA ; 114 `.wav` dont **19 distincts**, des
jingles de paiement de 0,22 à 3,59 s, **aucune musique**, aucun `AudioClip` ;
**aucune vidéo** (le lecteur AVPro et la machinerie `Advertize` sont là, les
films viennent du réseau) ; **233 messages d'erreur** en trois langues dans
`am_resources/*.dll`, avec numéro et domaine. **Ni fond d'écran, ni jaquette.**

**Les badges grisés et barrés** vus en surimpression sur l'écran-titre de VF5
viennent de là : cadre (`EmoneyIconAvailableFrame` / `NotAvailableFrame`) +
icône + barre (`EmoneyIconNotAvailableBar`), et trois paires de coin 74 × 48 —
emoney, pad, volume. Le jeu, lui, n'a aucun asset d'icône.

**How to apply:** outils `tools/apm_icones.py` (assets Unity : Texture2D,
`streamData`, décodage RGBA32 / RGB24 / BC1 / BC3), `tools/apm_sons.py`,
`tools/apm_lancer.py`. Deux fautes payées ici : chercher un nom **supposé**
(`btn_volume_disable` s'écrit `brn_`, faute de frappe de SEGA — trois
recherches manquées), et figer des **valeurs** au lieu de tester une **forme**.
Voir [[feedback_cartographier_la_zone]] et [[feedback_premisse_qui_borne]].
