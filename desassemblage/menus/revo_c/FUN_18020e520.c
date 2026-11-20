/* FUN_18020e520  --  VF5FS+0x20e520
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x18020e520.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


void FUN_18020e520(void)

{
  longlong lVar1;
  
  lVar1 = FUN_1801d1ae0();
  if ((*(ushort *)(lVar1 + 0x22) & 2) == 0) {
    *(ushort *)(lVar1 + 0x22) = *(ushort *)(lVar1 + 0x22) | 2;
  }
  return;
}
