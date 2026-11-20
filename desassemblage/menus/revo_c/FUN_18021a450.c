/* FUN_18021a450  --  VF5FS+0x21a450
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18021a450.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18021a450(longlong param_1,undefined8 *param_2)

{
  _DAT_18079b6b8 = *param_2;
  _DAT_18079b6c0 = *(undefined4 *)(param_2 + 1);
  DAT_18079b6c4 = *(undefined1 *)((longlong)param_2 + 0xc);
  DAT_18079b6c5 = *(undefined1 *)(param_1 + 8);
  DAT_18079b6c6 = *(undefined1 *)(param_1 + 9);
  DAT_18079b6c7 = *(undefined1 *)(param_1 + 10);
  DAT_18079b6c8 = *(undefined1 *)(param_1 + 0x16);
  DAT_18079b6c9 = *(char *)(param_1 + 0xb) == '\0';
  FUN_180219ed0(param_2);
  return;
}
