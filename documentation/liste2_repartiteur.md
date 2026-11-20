# La liste 2 a un répartiteur — le second verrou est ouvert

Session du 2026-09-02, dans la foulée de `analysis/fenetres_temporelles.md`. Le second verrou
dur du chantier `mothead` tombe, et il faut d'abord dire ce qui était faux.

---

## 1. La conclusion retirée

`docs/formats/mothead.md` §3.12 affirmait, avec la confiance `SUPPORTED` :

> Le DLL ne cherche que sept des 44 codes de la liste 2 : 3, 4, 6, 11, 18, 26 et 34. Les 37
> autres — 93 141 entrées sur 119 173, soit 78 % de la liste 2 — ne sont jamais consultés par
> leur code nulle part dans le binaire.

C'est **faux**. Les 55 codes que le format peut porter ont tous un gestionnaire, dans les deux
builds. La section a été réécrite ; l'ancienne conclusion y est explicitement retirée.

Le raisonnement d'origine reposait sur une prémisse, énoncée telle quelle :
« toute lecture de la liste 2 passe nécessairement par le champ `+0x18` de l'enregistrement,
lui-même obtenu par `MothGetRecord` ». Cette prémisse est fausse, et c'est elle qui a fait
tourner cinq voies de recherche à vide.

---

## 2. Ce que la reprise a trouvé

Le fil est venu d'une fonction de trois instructions, dans le build APM3 :

```
0x180152DE0   mov rax, [rcx + 0x4A0]      ; le pointeur de liste 2 de l'enregistrement
              mov [rcx + 0x498], rax      ; ... recopie dans le champ d'a cote
              ret
```

Elle est appelée par `MothTickMotion` (`0x18015A350`) **immédiatement après** avoir rangé le
pointeur de liste 2 dans `état+0x4A0`. C'est une **remise à zéro de curseur** : `état+0x498`
est la position de lecture, remise à la base à chaque installation d'enregistrement.

La recherche précédente avait examiné les lecteurs de `état+0x518` (l'équivalent R.E.V.O. de
`0x4A0`) et conclu, à juste titre, que personne ne relit ce pointeur. **Le lecteur est le
champ d'à côté**, `état+0x510` côté R.E.V.O.

Le curseur mène droit au répartiteur.

---

## 3. `MothRunList2`

| | APM3 | R.E.V.O. |
|---|---|---|
| répartiteur | `0x180152CE0` | `0x18015D3A0` |
| table des gestionnaires | `0x180648840` | `0x180641350` |
| remise du curseur | `0x180152DE0` | `0x18015D490` |
| curseur / base dans l'état | `+0x498` / `+0x4A0` | `+0x510` / `+0x518` |

```
MothRunList2(rcx = etat, rdx = ROB, xmm2 = trame courante)

  rdx = [etat+0x498]                     ; le curseur
  ebx = (int)xmm2                        ; la trame courante, tronquee
  si rdx nul ou (s32)[rdx] < 0 : rien a faire
boucle:
  si [rdx+4] > ebx : sortir              ; entree pas encore echue -> on s'arrete la
  rax = (s32)[rdx]                       ; le CODE
  si rax >= 0x37 : passer                ; 55 codes
  r10 = table[rax].gestionnaire          ; INDICE, jamais comparaison
  si r10 :
      si table[rax].drapeau & 1 et ebx > 0 et ebx - [rdx+4] > 1 : passer
      charge = [rdx+8] ? &[rdx+8] + [rdx+8] : NULL
      r10(&ctx + table[rax].delta, charge, rdx)
passer:
  rdx += 12 ; [etat+0x498] = rdx         ; le curseur avance, et reste avance
  si (s32)[rdx] >= 0 : recommencer
```

Le contexte passé aux gestionnaires est monté sur la pile, six qwords :

```
ctx = [ ROB, ROB+0x440, [ROB+0x20]+0x30C0, ROB, ROB+0x440, ROB+0x8A0 ]
                                                            ^ l'etat de mouvement
```

Même forme que pour la liste 1 : `gestionnaire(rcx = &ctx, rdx = charge, r8 = entrée)`.

### Pourquoi les cinq voies avaient échoué

| Voie épuisée en §3.11 | Pourquoi elle ne pouvait pas aboutir |
|---|---|
| `MothFindPayload` avec le code en immédiat | il ne sert effectivement qu'à la liste 1 ; le répartiteur ne l'appelle pas |
| l'idiome `cmp r32, K` / `test r32, r32` | **le code n'est jamais comparé**, il indexe une table |
| les lecteurs du pointeur `état+0x518` | le parcours lit le **curseur** `état+0x510`, pas la base |
| un parcours avec table de saut | la répartition se fait par `call r10`, pas par un saut indirect |
| les fonctions du module `mothead` | le répartiteur n'y est pas : il est en `0x18015D3A0`, hors de la plage `0x180163460`–`0x1801647C0` |

**La liste 2 est une frise chronologique**, consommée une fois dans l'ordre des trames, le
curseur n'y revenant jamais en arrière. Ce n'est pas un dictionnaire qu'on interroge par code.
Le drapeau `+0x18` bit 0 — porté par les codes **0, 1, 8, 25 et 31**, identiquement dans les
deux builds — signifie *n'agit qu'à la trame exacte* : passé d'une trame, l'entrée est sautée
sans rattrapage. Cela n'a de sens que pour une frise.

---

## 4. Les 55 gestionnaires

Sur APM3 la table est **nulle dans le fichier** et remplie à l'exécution par l'initialiseur
`0x180003D30` (110 écritures) ; sur R.E.V.O. elle est complète dans le fichier. Les deux ont
**55 entrées sur 55 pourvues**, et le même profil de drapeaux. Relevé :
`analysis/mothead_liste2_gestionnaires.csv`.

Contrôle sur les données, 104 fichiers, quatre jeux : **le code de liste 2 le plus grand
rencontré est 54** — exactement la borne du répartiteur.

### Code 0 = un effet sonore daté. CONFIRMED

`0x180154D60` teste la charge, puis appelle `0x1801879C0`, qui borne à `0x19A = 410` et rend
`table_0x180401730[charge]` : **410 noms de sons**, `fd_gard00`, `fd_punch_00`,
`fd_kick_01st`, `fd_jump_00`, `fd_LANDING_GROUND_LAU`, `fd_vfxse_hone01`, `fd_vf2_jacky_pk`…
Le nom part dans `0x180185C20(catégorie = 2, nom)`.

Données : **16 089 charges, 71 valeurs distinctes, toutes entre 1 et 391** — aucune hors table.

### Code 9 = un commutateur de bits daté. CONFIRMED

`0x180154A20` borne la charge `u16` à 17 et saute dans un commutateur de **18 cas** qui pose
ou efface un bit du masque `état+0x4A8` (`ROB+0xD48`) :

| charge | effet |
|---|---|
| 0 | masque = 1 |
| 1 | efface le bit 0 |
| 4 | masque = 0 |
| 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17 | pose `0x2`, `0x4`, `0x8`, `0x10`, `0x20`, `0x40`, `0x80`, `0x100`, `0x200`, `0x400`, `0x800`, `0x1000`, `0x2000`, `0x8000`, `0x10000` |

Données : **28 224 charges, exactement 18 valeurs distinctes, 0 à 17** — la borne du
commutateur, et pas une de plus. C'était le code le plus employé du format.

---

## 5. La confirmation à l'exécution

`tools/pister_liste2.py` mène le jeu au combat et pose des points d'arrêt sur le répartiteur
et sur les gestionnaires demandés (`tools/pister_liste2.cmd`). Relevé brut :
`analysis/pistage_liste2.txt`.

```
BP MothRunList2
    etat=0x1C37EB98DE0  ROB=0x1C37EB98540  ecart=0x8A0
BP gestionnaire liste2 code 0
    entree : code=0 trame=114 ; charge = 0d000000 80000000     -> son 13 = fd_down0244
BP gestionnaire liste2 code 9
    entree : code=9 trame=0   ; charge = 00000000              -> masque = 1
    entree : code=9 trame=0   ; charge = 03000000 01000000     -> pose 0x4
```

Les deux codes déclarés hors d'atteinte s'exécutent, avec leurs charges, dans un combat qui
tourne. L'écart `état − ROB` vaut `0x8A0`, ce qui reconfirme à l'exécution la disposition
établie dans `analysis/fenetres_temporelles.md`.

---

## 5 bis. Une trouvaille de côté : le tampon d'entrée du combattant

Les codes 20 à 24 et 51 ne franchissent jamais leur garde, même en tenant les treize boutons à
la fois. Plutôt que d'en rester là, on a relevé **les valeurs des quatre champs de garde à
l'entrée du gestionnaire** (`oracle_liste2_vivant.py --champs`). Elles se lisent seules :

| champ | valeurs observées | lecture |
|---|---|---|
| `ROB+0x508` | `0`, `1`, `0x15`, `0x40001`, `0x2080003` | **masque d'entrée courant** — il suit nos appuis |
| `ROB+0x510` | `0`, `1`, `0x40001`, `0x80003` | **masque d'entrée tamponné** |
| `ROB+0x90C` | `15.0`, `16.0`, `17.0`, `19.0` (des flottants) | **trames restantes du tampon** |
| `ROB+0x91C` | `0` ou `1` | **le tampon est-il actif** |

Le gestionnaire choisit le masque tamponné plutôt que le courant quand le tampon est actif et
qu'il lui reste des trames, puis croise le résultat avec le masque de la charge. C'est un
**tampon d'entrée** classique dans un jeu de combat : une commande arrivée un peu trop tôt
reste valable quelques trames.

L'absence d'écriture s'explique donc **par la garde**, et non par une lecture fausse : les
codes 20, 24 et 51 passent à `SUPPORTED` sur cette base. Confiance : **SUPPORTED**.

---

## 6. Ce que cela change

- **Aucune entrée de liste 2 n'est inerte.** Les 119 173 entrées du corpus passent toutes par
  un gestionnaire. Pour le modding, la conséquence s'inverse : tous les codes ont un effet.
- **Le travail restant est ordinaire** : lire 40 gestionnaires courts, tous rassemblés entre
  `0x180152DF0` et `0x180155440` dans le build APM3. Leur adresse est déjà dans
  `analysis/mothead_liste2_gestionnaires.csv`, et `tools/pister_liste2.py --codes N` permet de
  voir n'importe lequel s'exécuter avec sa charge.
- **Une leçon de méthode, deux fois payée dans la même journée.** Les deux verrous durs du
  chantier tenaient à une adresse de base fausse — l'état dans le ROB pour les fenêtres, le
  champ voisin pour la liste 2. Dans les deux cas la recherche avait été menée
  exhaustivement, et dans les deux cas l'exhaustivité portait sur le mauvais objet. Une
  énumération complète ne vaut que ce que vaut la prémisse qui la borne, et une prémisse
  s'écrit noir sur blanc pour pouvoir être attaquée : c'est parce que §3.12 énonçait la
  sienne — « toute lecture passe par `MothGetRecord` » — qu'elle a pu être réfutée.
