/* FUN_180086350  --  VF5FS+0x86350
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180086350.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_180086350(undefined4 param_1,undefined1 param_2,undefined4 param_3,undefined1 param_4,
                  undefined1 param_5,undefined1 param_6)

{
  longlong lVar1;
  
  lVar1 = DAT_18073d1b8;
  *(undefined8 *)(DAT_18073d1b8 + 0x58) = 0;
  *(undefined2 *)(lVar1 + 0x68) = 0;
  *(undefined4 *)(lVar1 + 0x7c) = 0;
  *(undefined1 *)(lVar1 + 0x72) = param_5;
  *(undefined4 *)(lVar1 + 0x6c) = param_1;
  *(undefined1 *)(lVar1 + 0x70) = param_2;
  *(undefined1 *)(lVar1 + 0x73) = param_6;
  *(undefined8 *)(lVar1 + 0x60) = 300;
  *(undefined4 *)(lVar1 + 0x78) = param_3;
  *(undefined1 *)(lVar1 + 0x71) = param_4;
  *(undefined2 *)(lVar1 + 0x74) = 0;
  *(undefined1 *)(lVar1 + 0x76) = 0;
  FUN_1802cd400(lVar1,"TASK_ENDING");
  return;
}
