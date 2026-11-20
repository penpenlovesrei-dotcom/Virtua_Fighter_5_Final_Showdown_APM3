/* FUN_1801a3f20  --  VF5FS+0x1a3f20
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801a3f20.
 * Vidée le 2026-11-08.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1801a3f20(void)

{
  int *piVar1;
  longlong lVar2;
  
  _guard_check_icall(0);
  if (DAT_180795788 == 0) goto LAB_1801a4023;
  if (DAT_180795788 == 2) {
LAB_1801a3f72:
    if (DAT_1807958f4 == '\0') {
      if (DAT_1807958f2 == '\0') {
        if (DAT_1807958f3 == '\0') {
          if (DAT_1807958f5 != '\0') {
            _guard_check_icall();
          }
        }
        else {
          _guard_check_icall();
        }
      }
      else {
        _guard_check_icall();
      }
    }
    else {
      _guard_check_icall();
    }
    if (DAT_1807958f6 != '\0') {
      _guard_check_icall();
    }
  }
  else if ((((DAT_180795788 == 3) || (DAT_180795788 == 4)) || (DAT_180795788 == 5)) ||
          (DAT_180795788 == 6)) {
    FUN_1800d0670(0);
    FUN_1800d0670(1);
    goto LAB_1801a3f72;
  }
  piVar1 = &DAT_18079573c;
  lVar2 = 0x13;
  do {
    if (*piVar1 != 0) {
      FUN_180026140();
      *piVar1 = 0;
    }
    piVar1 = piVar1 + 1;
    lVar2 = lVar2 + -1;
  } while (lVar2 != 0);
  FUN_1801a3c80(&DAT_1807956e0);
  DAT_180795788 = 0;
  _DAT_18079578c = 0x15;
  _DAT_180795790 = 0x15;
  DAT_1807957a0 = 1;
LAB_1801a4023:
  _guard_check_icall();
  return;
}
