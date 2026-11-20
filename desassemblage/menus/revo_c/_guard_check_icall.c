/* _guard_check_icall  --  VF5FS+0xaf60
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18000af60.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void _guard_check_icall(void)

{
  return;
}


/* ----------------------------------------------------------------------
 * CE NOM EST CELUI QUE GHIDRA A POSE, ET IL EST TROMPEUR. Lu le 2026-11-17.
 *
 * 0x18000AF60 = `C2 00 00` = `RET 0x0`. Ghidra l'appelle
 * `_guard_check_icall` parce que la table de configuration CFG y pointe,
 * mais ce n'est pas seulement le talon CFG : c'est LE POINT DE REPLIEMENT
 * `/OPT:ICF` DE TOUTES LES FONCTIONS VIDES DU BINAIRE.
 *
 * `xrefs 0x18000af60` rend PLUS DE MILLE references : du code de
 * sous-systemes sans rapport, et des centaines de creneaux de vtable dans
 * les zones de donnees 0x1803xxxxx / 0x1805xxxxx.
 *
 * DONC un `CALL 0x18000AF60` n'est une verification CFG que s'il est suivi
 * d'un `CALL RAX` et precede d'un pointeur 64 bits en RCX. Quand RCX porte
 * un entier 32 bits et que rien ne suit, c'est un APPEL A UNE FONCTION A
 * CORPS VIDE. Les sites ainsi mesures :
 *
 *   0x19C23C / 259 / 295 / 2D1 / 2F7   le decor      (SS 419.201)
 *   0x145F77 / 0x145F8D               l'objet en main (SS 419.201)
 *   0x18871A / 0x188734               LE TISSU DU COMBATTANT (2026-11-17)
 *
 * Voir Rendu_TirerUneEntreeDeTissu.c.
 * ---------------------------------------------------------------------- */
