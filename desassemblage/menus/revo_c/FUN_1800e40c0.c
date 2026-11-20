/* FUN_1800e40c0  --  VF5FS+0xe40c0
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800e40c0.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined1 FUN_1800e40c0(void)

{
  char cVar1;
  longlong lVar2;
  
  FUN_1801a4180(&DAT_1807956d0);
  cVar1 = FUN_1801cf0c0();
  if (cVar1 == '\0') {
    return 0;
  }
  FUN_180026150(0x208);
  FUN_180025920(0x208);
  FUN_180195da0(0x269);
  FUN_180195da0(0x268);
  lVar2 = FUN_1800e1940();
  if ((*(int *)(lVar2 + 4) != 6) || (*(int *)(lVar2 + 0x20) != 0x2a)) {
    FUN_1801951d0(0);
  }
  return 1;
}
