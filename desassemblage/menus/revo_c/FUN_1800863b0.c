/* FUN_1800863b0  --  VF5FS+0x863b0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800863b0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_1800863b0(void)

{
  longlong lVar1;
  
  lVar1 = DAT_18073d1c0;
  *(undefined8 *)(DAT_18073d1c0 + 0x58) = 0;
  *(undefined8 *)(lVar1 + 0x60) = 300;
  *(undefined4 *)(lVar1 + 0x7c) = 0;
  *(undefined2 *)(lVar1 + 0x68) = 1;
  *(undefined4 *)(lVar1 + 0x6c) = 0xffffffff;
  FUN_1802cd400(lVar1,"TASK_VS_FINISH_ENDING");
  return;
}
