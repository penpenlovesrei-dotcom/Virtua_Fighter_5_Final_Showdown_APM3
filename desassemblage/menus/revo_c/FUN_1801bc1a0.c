/* FUN_1801bc1a0  --  VF5FS+0x1bc1a0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801bc1a0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


longlong FUN_1801bc1a0(undefined4 param_1,undefined4 param_2)

{
  longlong lVar1;
  char cVar2;
  
  lVar1 = DAT_180795c58;
  *(undefined4 *)(DAT_180795c58 + 0x284) = param_1;
  *(undefined4 *)(lVar1 + 0x288) = param_2;
  cVar2 = FUN_1802cd400(lVar1,"PROMOTION");
  if (cVar2 != '\0') {
    FUN_1801cf1f0(0);
    FUN_1801960a0(0x26d);
    FUN_180026180(0x20d);
    return DAT_180795c58;
  }
  return 0;
}
