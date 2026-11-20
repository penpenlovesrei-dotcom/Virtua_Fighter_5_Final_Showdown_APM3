// ===================================================
// 82322820  ->  FUN_82322820  (entree 82322820)
// ===================================================

/* WARNING: Function: __savegprlr_29 replaced with injection: x360_savegprlr */
/* WARNING: Function: __restgprlr_29 replaced with injection: x360_restgprlr */

undefined8 FUN_82322820(void)

{
  char cVar4;
  int iVar3;
  undefined8 uVar1;
  undefined8 uVar2;
  int *piVar5;
  
  if (DAT_82ad1c40 == (int *)0x0) {
    cVar4 = FUN_821ccb40(0xffffffff82ad1c48);
    if ((cVar4 != '\0') || (iVar3 = FUN_821ccb68(0xffffffff82ad1c48), iVar3 == 0)) {
      return 1;
    }
    uVar1 = FUN_821ccb88(0xffffffff82ad1c48);
    DAT_82ad1c40 = (int *)FUN_8220cf50(0xe,uVar1,0xffffffff820b1580);
    uVar1 = FUN_821ccb88(0xffffffff82ad1c48);
    uVar2 = FUN_821ccb68(0xffffffff82ad1c48);
    FUN_825ffd30(DAT_82ad1c40,uVar2,uVar1);
    FUN_821ce558(0xffffffff82ad1c48,1);
    piVar5 = DAT_82ad1c40;
    do {
      *piVar5 = (int)DAT_82ad1c40 + *piVar5;
      piVar5 = piVar5 + 1;
    } while (*piVar5 != 0);
  }
  return 0;
}



