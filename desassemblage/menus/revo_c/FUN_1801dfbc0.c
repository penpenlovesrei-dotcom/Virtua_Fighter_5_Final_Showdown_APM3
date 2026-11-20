/* FUN_1801dfbc0  --  VF5FS+0x1dfbc0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801dfbc0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined8 FUN_1801dfbc0(longlong param_1)

{
  *(undefined1 *)(param_1 + 0x11c) = 1;
  *(undefined1 *)(param_1 + 0x11d) = *(undefined1 *)(param_1 + 0x200);
  *(undefined4 *)(param_1 + 0x118) = *(undefined4 *)(param_1 + 0x204);
  *(undefined8 *)(param_1 + 0xc0) = 0;
  *(undefined8 *)(param_1 + 400) = 0;
  *(undefined4 *)(param_1 + 0x1e8) = 0x13;
  *(undefined2 *)(param_1 + 0x1ec) = 0x101;
  FUN_1802cd400(param_1 + 0x68,"MENU_EXPLAIN");
  *(undefined1 *)(param_1 + 0x1ed) = *(undefined1 *)(param_1 + 0x201);
  *(undefined4 *)(param_1 + 0x1e8) = *(undefined4 *)(param_1 + 0x208);
  FUN_1802cd400(param_1 + 0x138,"MENU_CONTROL");
  *(undefined4 *)(param_1 + 0x214) = 0;
  *(undefined4 *)(param_1 + 0x21c) = 0;
  *(undefined4 *)(param_1 + 0x60) = 0;
  *(undefined2 *)(param_1 + 100) = 0;
  *(undefined1 *)(param_1 + 0x66) = 0;
  *(undefined1 *)(param_1 + 0x221) = 1;
  return 1;
}
