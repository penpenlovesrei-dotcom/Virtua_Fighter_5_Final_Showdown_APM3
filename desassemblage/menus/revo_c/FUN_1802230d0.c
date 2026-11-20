/* FUN_1802230d0  --  VF5FS+0x2230d0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1802230d0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1802230d0(void)

{
  longlong lVar1;
  
  lVar1 = DAT_18079b7d8;
  *(undefined8 *)(DAT_18079b7d8 + 0x58) = 0;
  *(undefined8 *)(lVar1 + 0x60) = 300;
  *(undefined4 *)(lVar1 + 0x6c) = 0;
  *(undefined2 *)(lVar1 + 0x69) = 0;
  *(undefined1 *)(lVar1 + 0x6b) = 0;
  FUN_1802cd400(lVar1,"TASK_CREDIT");
  return;
}
