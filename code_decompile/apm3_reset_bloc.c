// ===================================================
// 1801B76BC  ->  FUN_1801b7640  (entree 1801b7640)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1801b7640(undefined1 param_1,undefined1 param_2,int param_3)

{
  longlong lVar1;
  char cVar2;
  
  if ((*(char *)(DAT_180752148 + 0x68c4) != '\0') &&
     (cVar2 = FUN_180244ea0(&DAT_180752000), cVar2 == '\0')) {
    *(undefined1 *)(DAT_180752148 + 0x671d) = 0;
    if (param_3 < 0) {
      param_3 = FUN_180007440();
    }
    cVar2 = FUN_180007450(param_3);
    if ((cVar2 != '\0') && (param_3 == *(int *)(DAT_180752148 + 0x6718))) {
      FUN_1801b8a80();
      lVar1 = DAT_180752148;
      cVar2 = FUN_180244f90(&DAT_180752000);
      if (cVar2 == '\0') {
        FUN_1801b6ad0(&DAT_180752000);
        _DAT_180752058 = 7;
        _DAT_180752070 = FUN_1801b69b0;
        _DAT_180752060 = lVar1;
        _DAT_18075205c = param_3;
        DAT_180752068 = param_1;
        DAT_180752069 = param_2;
        FUN_1802456b0(&DAT_180752000,0,"TaskCsSystemSaveData(LOAD)");
      }
    }
  }
  return;
}



// ===================================================
// 1801B9DE4  ->  FUN_1801b9dd0  (entree 1801b9dd0)
// ===================================================

void FUN_1801b9dd0(void)

{
  longlong lVar1;
  int iVar2;
  
  iVar2 = FUN_180007440();
  if (-1 < iVar2) {
    FUN_1801b8a80(DAT_180752148);
    iVar2 = FUN_180007440();
    lVar1 = DAT_180752148;
    if (iVar2 == 1) {
      *(undefined4 *)(DAT_180752148 + 0x4fd0) = 1;
    }
    else if (iVar2 == 2) {
      *(undefined4 *)(DAT_180752148 + 0x4fd0) = 3;
    }
    else {
      *(undefined4 *)(DAT_180752148 + 0x4fd0) = 2;
    }
    *(undefined4 *)(lVar1 + 0x6720) = 0;
    _guard_check_icall();
    FUN_1801b69b0(1);
    FUN_1801b9d40(0);
    return;
  }
  return;
}



