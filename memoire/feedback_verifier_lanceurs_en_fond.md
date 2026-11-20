---
name: feedback_verifier_lanceurs_en_fond
description: Ne jamais lancer verifier_lanceurs.py en tâche de fond — il réécrit la DLL et la laisse dans l'état du dernier lanceur rejoué.
metadata:
  type: feedback
---

`tools/verifier_lanceurs.py` REJOUE chaque ligne de patch de chaque lanceur. Il
ne verifie pas un texte : il **reconstruit le binaire**, autant de fois qu'il y
a de lanceurs, et il laisse la DLL dans l'etat du DERNIER rejoue.

**Why:** deja paye deux fois. Le 2026-09-10 il tenait la DLL et le lanceur de
Frederic a rendu « Le patch a ECHOUE ». Le 2026-09-11 je l'ai lance en fond
juste apres avoir bati : quand j'ai relance le controle, la section `.decors`
avait disparu — la DLL etait celle d'un autre lanceur.

**How to apply:** ne l'appeler que quand aucun build n'est en cours d'usage, en
premier plan, et REBATIR juste apres. Jamais en tache de fond, jamais pendant
que Frederic teste. Verifier la forme d'un `.cmd` (CRLF, octets de controle) se
fait en le lisant, sans le rejouer.

Voir [[feedback_lanceurs_cmd]], [[reference_vf5_etat_fichiers_herite]].
