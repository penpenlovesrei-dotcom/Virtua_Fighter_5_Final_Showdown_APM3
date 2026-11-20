# Le répartiteur `[[0x180C3B6F0]+0x1FE10]` : l'API à commandes du moteur

Établi le 2026-09-08, en cherchant comment écrire une ligne de texte sur
l'écran de sélection des décors.

---

## 1. La forme

Beaucoup de services du moteur ne sont pas des fonctions nommées : ils passent
par **un seul point d'entrée**, avec un numéro de commande.

```
mov  rcx, [0x180C3B6F0]          ; l'objet de contexte
mov  rax, [rcx + 0x1FE10]        ; le pointeur de fonction ; nul = service absent
test rax, rax ; je  ...          ; tous les appelants testent
mov  rcx, [rcx + 0x1FE18]        ; le contexte du service
lea  r8,  [rsp + N]              ; la structure d'argument, aller ET retour
mov  edx, <commande>
call rax
```

La structure sert **dans les deux sens** : `0x1801EFD10` y met un identifiant
de libellé et relit la chaîne au même endroit.

## 2. Les commandes, relevées par balayage

56 commandes distinctes dans `.text`, trouvées en cherchant le déplacement
`0x1FE18` puis le `mov edx, imm32` qui suit :

```
0x01 x4    0x02 x1    0x05 x2    0x06 x19   0x19 x1    0x1B x1    0x1E x1
0x1F x1    0x25 x1    0x27 x2    0x2B x19   0x2C x3    0x36 x1    0x38 x1
0x3A x3    0x3B x1    0x3C x1    0x3D x1    0x3E x1    0x40 x4    0x42 x4
0x47 x1    0x49 x1    0x4A x2    0x4B x1    0x53 x1    0x5F x1    0x62 x1
0x63 x1    0x64 x2    0x6A x1    0x6B x1    0x6F x1    0x74 x1    0x77 x5
0x78 x2    0x7C x1    0x82 x1    0x83 x1    0x84 x2    0x85 x9    0x87 x2
0x88 x1    0x89 x1    0x8B x1    0x90 x1    0x92 x1    0x96 x1    0x97 x1
0x99 x2    0x9A x5    0x9C x1    0xA4 x7    0xA8 x1    0xAF x1    0xB1 x1
```

Trois sont identifiées :

| commande | structure | rôle | site |
|---|---|---|---|
| **0x74** | `{u32 identifiant}` → `{…, char* chaîne}` | **résoudre un libellé** | `0x1801EFD41` |
| **0x05** | un octet, écrit puis **relu** | une **question** (rend un booléen) | `0x180174563`, dans `TaskSelStage` |
| **0x06** | 0x30 octets : `{1, …, octets en +5, +6, +9}` | le curseur / la case | 19 sites, dont le constructeur de grille |
| **0x5F** | `{char* texte, octet}` | passe un texte au service | `0x180239D6E` |
| **0x77** | 18 octets à zéro | — | `0x18020DE3F` |

## 3. Ce que ça dit pour le libellé de l'écran de décors

**Cet écran ne dessine aucun texte.** Le résolveur `0x1801EFD10` a **276
appelants** dans le moteur et **aucun** dans `0x18017xxxx`. Les deux commandes
que `TaskSelStage` utilise — 5 et 6 — sont une question et le curseur, pas un
dessin.

Tout ce que l'écran affiche est de l'art peint, désigné par nom de composition
AET et joué par `0x180171E90(ctx, couche, index, nom, …)` :

```
stage_icon_xxx_c    les 21 ancres de cases
xxx_stay            l'apercu, une couche par decor (dont un `ari_stay` inutilise)
stage_icon_name_out / _out_e / _in / _in_e     la plaque NOM + TAILLE
stage_name_l_base / _e, stage_graph_l_base, deco_tit_stage_out
```

**Ce qui reste à trouver** : la commande qui dessine une chaîne à une position
choisie. Les candidates non ouvertes sont celles des écrans qui affichent
beaucoup de texte — `0x85` (9 sites, vers `0x18023Axxx`), `0xA4` (7 sites,
`0x1801DCxxx`), `0x2B` (19 sites). La méthode qui a marché ici marchera là :
prendre le site, lire la structure qu'il remplit, et voir si elle porte un
`char*` **et** des flottants de position.

`0x5F` est la plus proche du but (elle prend déjà un `char*`) mais son seul
appelant, `0x180239D40`, passe le libellé `0x5A0D` — **hors table**, la borne
étant `0x5A0C`. À éclaircir avant de s'en servir.

---

## 4. TROUVÉ : le dessin de texte n'est pas dans le répartiteur

La piste des commandes était la mauvaise. `0xA4` prend `{dword 6}`, `0x77`
dix-huit octets à zéro : ni l'une ni l'autre ne dessine.

Le texte se dessine par une **fonction ordinaire**, et on la connaissait déjà
sans le savoir : **`0x18019BEB2`**, l'appel que `--sans-now-loading` neutralise.

```
0x18019BE18  lea rcx,[rbp-0x59] ; call 0x18019A8C0    <- construit le DESCRIPTEUR
0x18019BE22  lea rcx,[rbp-9]    ; call 0x18019A9D0    <- construit le STYLE
0x18019BE3C  mov edx,2 ; lea rcx,[rbp-9] ; call 0x18019B6F0   <- mode du style
0x18019BE4A  vmovss xmm1,[0x18034AF78] ; call 0x18019B830     <- taille
0x18019BE5B  lea rax,[rbp-9] ; mov [rbp-0x11],rax     <- le style entre au descripteur
0x18019BE63  mov dword [rbp-0x35], 7
0x18019BE6A  vmovss xmm1,[0x18039F648]   ; 640.0
0x18019BE77  vmovss xmm0,[0x18040A9A4]   ; 678.0
             -> [rbp-0x25],[rbp-0x21] et [rbp-0x1D],[rbp-0x19]
0x18019BE8E  mov dword [rbp-0x2D], 9
0x18019BE95  mov dword [rbp-0x51], -1    ; couleur (blanc)
0x18019BEA2  lea r8,[0x18040A990]        ; "NOW LOADING"
0x18019BEA9  mov edx,0x28
0x18019BEAE  lea rcx,[rbp-0x59]
0x18019BEB2  call 0x18019B2E0            <- LE DESSIN
```

**Les trois vérifications qui ferment le dossier** :

* `0x18040A990` contient bien `"NOW LOADING"` ;
* `0x18039F648` vaut **640.0** — le milieu exact d'un écran de 1280 — et
  `0x18040A9A4` vaut **678.0**, près du bas d'un écran de 720. Ce sont des
  coordonnées, en pixels d'écran ;
* `0x18019B2E0` est un enveloppeur de type `printf` : il déverse `r8`/`r9`
  dans l'espace d'ombre puis appelle `0x18019B330(desc, 0x28, format,
  &arguments)`.

**Et c'est une API GÉNÉRALE**, pas un cas du chargement : le balayage rend des
dizaines d'appelants répartis sur tous les écrans — le menu du Dojo
(`0x1801E1EBD`, à quinze octets du site que `--dojo-howto` patche déjà), les
pages de résultats (`0x18020xxxx`), le classement (`0x18022xxxx`), le menu
opérateur (`0x18023xxxx`, `0x18024xxxx`).

## 5. Ce qu'il reste à faire pour le libellé de génération

Reproduire ce bloc dans la greffe, avec notre propre cadre de pile, en ne
changeant que **la chaîne** et **la position**. Le descripteur fait environ
0x50 octets ; le style est un petit objet séparé rangé en `+0x48` du
descripteur.

Deux inconnues à lever avant d'écrire :

1. **la taille exacte** du descripteur et du style — `0x18019A8C0` et
   `0x18019A9D0` le diront ;
2. **le moment** : il faudra appeler ce dessin à chaque trame depuis l'écran
   de sélection, donc depuis l'entrée B de la greffe (`0x1801747C0`), qui est
   déjà jouée au bon endroit.

La chaîne, elle, ne pose plus de problème : ce n'est pas un identifiant
`string_array` mais un **pointeur direct**, et la greffe a 4096 octets pour
loger `Virtua Fighter 5`, `Virtua Fighter 5R` et
`Virtua Fighter 5 Final Showdown`.
