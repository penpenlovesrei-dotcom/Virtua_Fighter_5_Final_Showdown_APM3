/* FUN_1801a4030  --  VF5FS+0x1a4030
 *
 * Decompilation Ghidra, vidée par VF5RE/vider_fonctions.py.
 * Binaire : vf5fs_revo / vf5fs-pxd-w64-d3d12_SteamRetail.dll
 * Base d'image 0x180000000 ; adresse absolue 0x1801a4030.
 * Vidée le 2026-11-07.
 *
 * CE N'EST PAS DU CODE A COMPILER ni a recopier dans l'hote : c'est
 * une LECTURE du module, gardée pour ne pas la refaire.
 */


/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1801a4030(undefined8 param_1,undefined1 param_2)

{
  int iVar1;
  int *piVar2;
  
  DAT_1807958f7 = param_2;
  _guard_check_icall(1);
  if (DAT_180795788 == 1) goto LAB_1801a4170;
  if (DAT_180795788 == 2) {
LAB_1801a408c:
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
    goto LAB_1801a408c;
  }
  iVar1 = 0;
  piVar2 = &DAT_18079573c;
  do {
    if ((iVar1 != 0) && (*piVar2 != 0)) {
      FUN_180026140();
      *piVar2 = 0;
    }
    iVar1 = iVar1 + 1;
    piVar2 = piVar2 + 1;
  } while (iVar1 < 0x13);
  if (DAT_18079573c == 0) {
    FUN_1801a48c0(&DAT_1807956e0,0,4,0,0x10000,0,0);
  }
  FUN_1801a3c80(&DAT_1807956e0);
  DAT_180795788 = 1;
  _DAT_18079578c = 0x15;
  _DAT_180795790 = 0x15;
  DAT_1807957a0 = 1;
LAB_1801a4170:
  _guard_check_icall();
  return;
}
