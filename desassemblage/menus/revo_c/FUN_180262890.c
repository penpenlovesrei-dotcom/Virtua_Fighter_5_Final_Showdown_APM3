/* FUN_180262890  --  VF5FS+0x262890
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180262890.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined1 FUN_180262890(undefined4 param_1)

{
  longlong lVar1;
  char cVar2;
  
  lVar1 = DAT_1807a7150;
  cVar2 = FUN_180261060();
  if (cVar2 == '\0') {
    return 0;
  }
  *(undefined4 *)(lVar1 + 0x58) = param_1;
  return 1;
}
