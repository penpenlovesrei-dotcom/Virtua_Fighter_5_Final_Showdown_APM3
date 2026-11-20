/* Entree_RolesDuPort  --  VF5FS+0x190a50
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_apm3 / vf5fs_apm3_origine.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180190a50.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined * Entree_RolesDuPort(uint param_1)

{
  if (param_1 < 2) {
    return &g_entreeRoles + (longlong)(int)param_1 * 0x868;
  }
  return &g_entreeRoles;
}
