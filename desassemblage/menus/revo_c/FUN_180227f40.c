/* FUN_180227f40  --  VF5FS+0x227f40
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x180227f40.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


bool FUN_180227f40(char param_1)

{
  if (param_1 == '\0') {
    return *(uint *)(*(longlong *)(DAT_18079b7f0 + 0x70) + 0x14) <
           *(uint *)(*(longlong *)(DAT_18079b7f0 + 0x70) + 0x28);
  }
  if (param_1 == '\x01') {
    return *(uint *)(*(longlong *)(DAT_18079b7f0 + 0x58) + 0x14) <
           *(uint *)(*(longlong *)(DAT_18079b7f0 + 0x58) + 0x28);
  }
  if (param_1 == '\x02') {
    return *(uint *)(*(longlong *)(DAT_18079b7f0 + 0x60) + 0x14) <
           *(uint *)(*(longlong *)(DAT_18079b7f0 + 0x60) + 0x28);
  }
  return true;
}
