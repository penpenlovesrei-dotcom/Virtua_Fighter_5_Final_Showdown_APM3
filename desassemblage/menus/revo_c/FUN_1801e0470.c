/* FUN_1801e0470  --  VF5FS+0x1e0470
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801e0470.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1801e0470(int *param_1,int param_2)

{
  if (*param_1 != 0) {
    if (param_1[4] != 0) {
      FUN_180026140();
      param_1[4] = 0;
    }
    if (param_1[5] != 0) {
      FUN_180026140();
      param_1[5] = 0;
    }
    *param_1 = 0;
    param_1[0xb] = 0;
    if (*(longlong *)(param_1 + 8) != 0) {
      FUN_180279c00();
      param_1[8] = 0;
      param_1[9] = 0;
    }
    param_1[10] = 0;
    param_1[1] = param_2;
    *param_1 = 1;
    return;
  }
  param_1[1] = param_2;
  *param_1 = 1;
  return;
}
