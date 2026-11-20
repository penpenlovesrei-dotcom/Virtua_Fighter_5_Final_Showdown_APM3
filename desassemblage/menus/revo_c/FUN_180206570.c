/* FUN_180206570  --  VF5FS+0x206570
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180206570.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_180206570(void)

{
  longlong lVar1;
  
  lVar1 = FUN_1802ecd50(0x3028,0x10);
  if (lVar1 != 0) {
    DAT_18079b160 = FUN_1802056a0(lVar1);
    return;
  }
  DAT_18079b160 = 0;
  return;
}
