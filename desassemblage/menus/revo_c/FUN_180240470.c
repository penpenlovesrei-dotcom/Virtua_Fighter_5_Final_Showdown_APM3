/* FUN_180240470  --  VF5FS+0x240470
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180240470.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


longlong FUN_180240470(byte param_1)

{
  uint7 uVar1;
  
  uVar1 = (uint7)((ulonglong)DAT_18079bf58 >> 8);
  if (((uint)param_1 != *(uint *)(DAT_18079bf58 + 0x4e0)) && (param_1 < 0x16)) {
    *(uint *)(DAT_18079bf58 + 0x4e0) = (uint)param_1;
    return CONCAT71(uVar1,1);
  }
  return (ulonglong)uVar1 << 8;
}
