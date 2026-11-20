/* FUN_1800e4140  --  VF5FS+0xe4140
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800e4140.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined1 FUN_1800e4140(void)

{
  char cVar1;
  longlong lVar2;
  
  lVar2 = FUN_1800e1940();
  if ((*(int *)(lVar2 + 0x18) == 0) || (*(int *)(lVar2 + 0x18) != 1)) {
    _guard_check_icall(0xffffffff);
    if ((*(int *)(lVar2 + 8) != 6) || (*(int *)(lVar2 + 0x24) != 0x2a)) {
      FUN_1801951d0(0);
      FUN_1801951d0(1);
      FUN_1801951d0(2);
    }
    FUN_1801a4180(&DAT_1807956d0);
    FUN_1801960a0(0x268);
    FUN_1801960a0(0x269);
    FUN_180026180(0x208);
    *(undefined4 *)(lVar2 + 0x18) = 1;
  }
  else {
    cVar1 = FUN_180196130(0x268);
    if (cVar1 == '\0') {
      cVar1 = FUN_180196130(0x269);
      if (cVar1 == '\0') {
        cVar1 = FUN_1800262e0(0x208);
        if (cVar1 == '\0') {
          FUN_1801cf1f0(1);
          FUN_18022fc90();
          return 1;
        }
      }
    }
  }
  return 0;
}
