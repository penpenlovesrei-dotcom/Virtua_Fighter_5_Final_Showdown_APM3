---
name: reference_msys2_ca_bundle_vide
description: "MSYS2 de cette machine — bundle CA mingw64 vide, et piège du partial upgrade."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 212b918c-b482-48f4-98ba-8a572ee9396f
  modified: 2026-08-04T17:08:48.362Z
---

Deux anomalies de l'install MSYS2 (`C:\msys64`) rencontrées le 2026-08-04, susceptibles de
revenir sur n'importe quel projet compilé avec :

**1. `/mingw64/etc/ssl/certs/ca-bundle.crt` est un fichier de 0 octet.** Tout HTTPS depuis
git/curl mingw64 échoue en `error adding trust anchors from file`. `/mingw64/bin/update-ca-trust`
génère bien l'extrait mais ne le recopie jamais à cet emplacement (contrairement au script MSYS
qui, lui, fait le `cp`). Correctif appliqué :

    cp /mingw64/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem /mingw64/etc/ssl/certs/ca-bundle.crt

Peut se re-vider après une mise à jour de `mingw-w64-x86_64-ca-certificates`.

**2. Ne jamais faire `pacman -Sy` suivi d'un `-S`.** L'install dormait depuis longtemps ;
installer des paquets récents par-dessus a produit des `.exe` qui plantent en `0xC0000139`
(ENTRYPOINT_NOT_FOUND), `gcc-libs` restant en 15.2 alors que clang attendait 16.1.
Toujours `pacman -Syuu` complet d'abord — et le cœur (msys2-runtime, bash, pacman) se met à jour
dans une transaction séparée, donc il faut relancer `-Suu` derrière pour le reste.

**3. Lancer bash avec `MSYSTEM=MINGW64`**, sinon `/mingw64/bin` n'est pas dans le PATH et les
exécutables situés ailleurs (ex. `/mingw64/libexec/git-core/git-remote-https.exe`) ne trouvent
pas leurs DLL — le message parle d'un DLL manquant alors que le DLL existe.

Utilisé pour [[project_3sx_bgm_remix]].
