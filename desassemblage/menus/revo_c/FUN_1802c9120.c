/* FUN_1802c9120  --  VF5FS+0x2c9120
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1802c9120.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1802c9120(void)

{
  longlong lVar1;
  
  lVar1 = FUN_1802ecd00(2,0x10);
  if (lVar1 != 0) {
    DAT_180ea7348 = FUN_1802c8b70(lVar1);
    return;
  }
  DAT_180ea7348 = 0;
  return;
}
