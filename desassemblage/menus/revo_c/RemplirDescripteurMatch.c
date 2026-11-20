/* RemplirDescripteurMatch  --  VF5FS+0x1aa1d0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801aa1d0.
 * Vidée le 2026-11-11.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined2 *
RemplirDescripteurMatch
          (undefined2 *param_1,undefined2 param_2,undefined2 param_3,undefined1 param_4,
          undefined1 param_5)

{
  *(undefined1 *)((longlong)param_1 + 5) = param_5;
  *param_1 = param_2;
  param_1[1] = param_3;
  *(undefined1 *)(param_1 + 2) = param_4;
  return param_1;
}
