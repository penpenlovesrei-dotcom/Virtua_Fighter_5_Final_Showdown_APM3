---
name: reference_debogueur_win32_pieges
description: Trois pièges silencieux du débogueur Win32 de tools/instrument.py, tous corrigés le 2026-09-02.
metadata:
  type: reference
---

Trois défauts silencieux rencontrés en écrivant `VF5RE/tools/instrument.py`. Aucun ne
produit de message : ils se manifestent par « ça ne s'arrête pas » ou « ça ne se déclenche
jamais ».

1. **La boucle ne s'arrête jamais sous un flot d'événements.** Contrôler la durée dans la
   seule branche de temporisation de `WaitForDebugEvent` ne suffit pas : quand les
   `OutputDebugString` affluent, cette branche n'est jamais prise. Un `--secondes 25`
   tournait plus de deux minutes. Contrôler la durée **à chaque tour**.
2. **L'adresse d'un point d'arrêt logiciel.** Windows met dans `ExceptionAddress`
   **l'adresse de l'INT3 lui-même**, pas `adresse+1` comme le RIP du contexte. Rapprocher sur
   `a-1` échoue, l'octet d'origine n'est jamais rendu, et le processus rejoue l'INT3 sans fin.
3. **Le DR7 périmé.** Si on désarme un registre matériel pendant le traitement d'une
   exception puis qu'on réécrit le contexte tel qu'on l'avait lu, le DR7 qu'il porte encore
   remet le registre en place. Recalculer DR0-DR3 et DR7 depuis l'état courant avant
   `SetThreadContext`.

Autres points utiles : les registres DR sont **par thread** (57 threads ici), il faut donc les
poser sur tous et sur chaque thread créé ensuite ; et un DR « en lecture » sur x86 est en
réalité *lecture ou écriture*, il attrape donc aussi les écritures.
