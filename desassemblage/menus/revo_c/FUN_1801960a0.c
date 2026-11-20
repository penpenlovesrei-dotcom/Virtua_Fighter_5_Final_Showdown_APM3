/* FUN_1801960a0  --  VF5FS+0x1960a0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801960a0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1801960a0(undefined4 param_1)

{
  longlong lVar1;
  longlong lVar2;
  longlong lVar3;
  longlong lVar4;
  
  lVar1 = FUN_180199220(DAT_18075e018,param_1);
  lVar2 = (*(longlong *)(lVar1 + 0x10) << 0x14) >> 0x14;
  lVar4 = lVar2 << 4;
  if (lVar2 == 0) {
    lVar4 = 0;
  }
  lVar3 = FUN_180199220(DAT_18075e018,param_1);
  lVar2 = lVar4 + 4;
  if (lVar4 == 0) {
    lVar2 = lVar1 + 0x10;
  }
  FUN_18019b490(DAT_18075e010,*(undefined4 *)(lVar3 + 0x18),lVar2);
  return;
}
