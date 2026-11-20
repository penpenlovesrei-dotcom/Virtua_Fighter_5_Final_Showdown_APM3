/* FUN_1802cca00  --  VF5FS+0x2cca00
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1802cca00.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined1 FUN_1802cca00(longlong param_1)

{
  longlong *plVar1;
  
  plVar1 = (longlong *)*DAT_180ea7608;
  while( true ) {
    if (plVar1 == (longlong *)0x0) {
      return 0;
    }
    if (*plVar1 == param_1) break;
    plVar1 = (longlong *)plVar1[2];
  }
  if ((*(int *)(param_1 + 0x18) != 0) && (*(int *)(param_1 + 0x1c) == 0)) {
    return 0;
  }
  return 1;
}
