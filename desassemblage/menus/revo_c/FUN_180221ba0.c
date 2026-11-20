/* FUN_180221ba0  --  VF5FS+0x221ba0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180221ba0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


longlong FUN_180221ba0(undefined1 param_1,undefined1 param_2,undefined1 param_3)

{
  char cVar1;
  longlong lVar2;
  
  lVar2 = DAT_18079b760;
  *(undefined1 *)(DAT_18079b760 + 0x58) = param_1;
  *(undefined1 *)(lVar2 + 0x59) = param_2;
  *(undefined1 *)(lVar2 + 0x5a) = param_3;
  *(undefined1 *)(lVar2 + 0x5b) = 0;
  cVar1 = FUN_1802cd400(lVar2,"MULTI RNKCHG");
  lVar2 = 0;
  if (cVar1 != '\0') {
    lVar2 = DAT_18079b760;
  }
  return lVar2;
}
