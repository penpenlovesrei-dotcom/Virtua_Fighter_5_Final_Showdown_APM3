// ===================================================
// 1801B7A2F  ->  FUN_1801b7960  (entree 1801b7960)
// ===================================================

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1801b7960(char param_1,int param_2)

{
  longlong lVar1;
  char cVar2;
  undefined8 uVar3;
  
  if ((*(char *)(DAT_180752148 + 0x68c4) != '\0') &&
     (cVar2 = FUN_180244ea0(&DAT_180752000), cVar2 == '\0')) {
    *(undefined1 *)(DAT_180752148 + 0x671d) = 0;
    if (param_2 < 0) {
      param_2 = FUN_180007440();
    }
    cVar2 = FUN_180007450(param_2);
    if (((cVar2 != '\0') && (param_2 == *(int *)(DAT_180752148 + 0x6718))) &&
       ((param_1 == '\0' || (*(int *)(DAT_180752148 + 0x5020) != 0)))) {
      FUN_1801b7c20();
      uVar3 = FUN_1801bb730();
      _guard_check_icall(uVar3);
      lVar1 = DAT_180752148;
      cVar2 = FUN_180244f90(&DAT_180752000);
      if (cVar2 == '\0') {
        FUN_1801b6ad0(&DAT_180752000);
        _DAT_180752058 = 0;
        _DAT_180752070 = &LAB_1801b6a70;
        _DAT_180752060 = lVar1;
        _DAT_18075205c = param_2;
        DAT_180752069 = param_1;
        FUN_1802456b0(&DAT_180752000,0,"TaskCsSystemSaveData(SAVE)");
        if ((*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0) &&
           (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0)) {
          (**(code **)(DAT_180c3b6f0 + 0x1fe10))(*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0x89,0);
        }
      }
    }
  }
  return;
}



