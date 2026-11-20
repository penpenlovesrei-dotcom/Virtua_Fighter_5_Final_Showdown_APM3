---
name: reference_python_stub_windows
description: "Sur cette machine, `python` est un stub inerte du Microsoft Store ; il faut lancer `py -3`."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3331ac98-19db-49de-a075-1d62462a23f2
  modified: 2026-09-01T04:51:09.973Z
---

`C:\WINDOWS\system32\python` existe et se lance **sans rien faire** : sortie vide, pas de
code de retour. C'est le stub du Microsoft Store, pas un interpréteur.

Le vrai interpréteur est `py -3`
(`C:\Users\frede\AppData\Local\Python\pythoncore-3.14-64\python.exe`, Python 3.14.3).

Piège : un script lancé par `python mon_script.py` ne produit **aucun message d'erreur** —
on croit à un script silencieux alors que rien n'a tourné. Toujours écrire `py -3`.

`py -3 -m pip install` fonctionne normalement (pycryptodome installé de cette façon).

Rejoint [[feedback_verifier_le_build]] : une sortie vide n'est pas un succès.
