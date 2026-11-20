/* FUN_180210bd0  --  VF5FS+0x210bd0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180210bd0.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_180210bd0(longlong param_1)

{
  undefined1 uVar1;
  
  *(undefined4 *)(param_1 + 0x58) = 0;
  *(undefined1 *)(param_1 + 0x60) = 0;
  *(undefined4 *)(param_1 + 0x338) = 0;
  *(undefined1 *)(param_1 + 0x340) = 0;
  uVar1 = FUN_1801ceef0();
  *(undefined1 *)(param_1 + 0x5ce) = uVar1;
  *(undefined4 *)(param_1 + 2000) = 0;
  *(undefined1 *)(param_1 + 0x7d8) = 0;
  *(undefined4 *)(param_1 + 0xa60) = 0;
  *(undefined1 *)(param_1 + 0x1223) = 0;
  *(undefined1 *)(param_1 + 0xa68) = 0;
  *(undefined4 *)(param_1 + 0x1224) = 0xffffffff;
  FUN_1801fece0();
  FUN_1801b6060();
  return;
}
