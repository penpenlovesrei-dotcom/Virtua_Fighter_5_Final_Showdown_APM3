/* FUN_1801fc240  --  VF5FS+0x1fc240
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801fc240.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


longlong FUN_1801fc240(int param_1,undefined8 param_2,undefined4 param_3,undefined4 param_4,
                      char param_5)

{
  longlong lVar1;
  longlong lVar2;
  
  lVar2 = (longlong)param_1 * 0x5698;
  lVar1 = DAT_18079a688 + lVar2;
  *(undefined4 *)(lVar1 + 0x230) = 2;
  *(undefined4 *)(lVar1 + 0x234) = param_4;
  if (param_5 == '\0') {
    *(undefined4 *)(lVar1 + 0x74c) = 3;
  }
  FUN_1801fc600(lVar1,param_2,8,param_3);
  FUN_1802cd400(DAT_18079a688 + lVar2,"DATA SELECTOR");
  return DAT_18079a688 + lVar2;
}
