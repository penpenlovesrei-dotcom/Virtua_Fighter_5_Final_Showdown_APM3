/* FUN_1800e6580  --  VF5FS+0xe6580
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1800e6580.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


undefined8 FUN_1800e6580(void)

{
  char cVar1;
  int iVar2;
  int *piVar3;
  bool bVar4;
  
  FUN_1802cd400(DAT_1807514b0,"SYSTEM_STARTUP");
  piVar3 = (int *)FUN_180179e70();
  iVar2 = FUN_18000ba10();
  if (iVar2 == 0) {
LAB_1800e6615:
    cVar1 = FUN_18019fd10();
    if (((cVar1 == '\0') && (*piVar3 != 9)) && (*piVar3 != 1)) {
      _guard_check_icall(0x33);
    }
    FUN_1800d4df0(&DAT_18073fe60,0);
    FUN_1800d4df0(&DAT_18073ff18,1);
  }
  else {
    if (iVar2 == 1) {
      cVar1 = FUN_18019fd10();
      if (cVar1 != '\0') {
        return 1;
      }
      bVar4 = *piVar3 == 1;
    }
    else {
      if (iVar2 != 2) {
        if (iVar2 == 3) {
          cVar1 = FUN_18019fd10();
          if ((cVar1 == '\0') && (*piVar3 != 3)) {
            _guard_check_icall(0x33);
          }
          FUN_1800d4df0(&DAT_18073fe60,0);
          return 1;
        }
        goto LAB_1800e6615;
      }
      cVar1 = FUN_18019fd10();
      if (cVar1 != '\0') {
        return 1;
      }
      bVar4 = *piVar3 == 9;
    }
    if (!bVar4) {
      _guard_check_icall(0x33);
      return 1;
    }
  }
  return 1;
}
