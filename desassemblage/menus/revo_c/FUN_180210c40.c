/* FUN_180210c40  --  VF5FS+0x210c40
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180210c40.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_180210c40(longlong param_1,char param_2)

{
  *(undefined4 *)(param_1 + 0x58) = 0;
  *(undefined1 *)(param_1 + 0x60) = 0;
  *(undefined2 *)(param_1 + 0x5f5) = 0;
  if (param_2 != '\0') {
    *(undefined1 *)(param_1 + 0x5f7) = 0;
  }
  FUN_180210bd0(param_1 + 0x610);
  *(undefined4 *)(param_1 + 0x18d0) = 0;
  *(undefined1 *)(param_1 + 0x18d8) = 0;
  *(undefined4 *)(param_1 + 0x1bf8) = 0;
  *(undefined1 *)(param_1 + 0x1c00) = 0;
  *(undefined4 *)(param_1 + 0x1ed8) = 0;
  *(undefined4 *)(param_1 + 0x20b0) = 0;
  *(undefined1 *)(param_1 + 0x1ee0) = 0;
  FUN_180260890();
  FUN_1802608b0(0);
  *(undefined4 *)(param_1 + 0x21f0) = 0;
  *(undefined1 *)(param_1 + 0x21f8) = 0;
  *(undefined4 *)(param_1 + 0x24d0) = 0;
  *(undefined1 *)(param_1 + 0x24d8) = 0;
  *(undefined1 *)(param_1 + 0x274a) = 0;
  FUN_1801fc520();
  FUN_1801f0570();
  return;
}
