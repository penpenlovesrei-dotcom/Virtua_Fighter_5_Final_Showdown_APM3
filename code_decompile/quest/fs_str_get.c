// ===================================================
// 1801EFD10  ->  FUN_1801efd10  (entree 1801efd10)
// ===================================================

char * FUN_1801efd10(uint param_1)

{
  int iVar1;
  char cVar2;
  int *piVar3;
  uint local_18 [2];
  char *local_10;
  
  if ((DAT_180c3b6f0 != 0) && (*(longlong *)(DAT_180c3b6f0 + 0x1fe10) != 0)) {
    if (*(code **)(DAT_180c3b6f0 + 0x1fe10) != (code *)0x0) {
      local_18[0] = param_1;
      (**(code **)(DAT_180c3b6f0 + 0x1fe10))(*(undefined8 *)(DAT_180c3b6f0 + 0x1fe18),0x74,local_18)
      ;
    }
    return local_10;
  }
  if ((DAT_180753900 == 0) || (0x5a0b < param_1)) {
    if (param_1 - 0x5a0d < 0x22) {
      return "dummy";
    }
  }
  else {
    cVar2 = FUN_180029fb0();
    if ((cVar2 == '\0') && (param_1 < 0x31)) {
      param_1 = param_1 + 0x31;
    }
    piVar3 = (int *)(DAT_180753900 + (ulonglong)param_1 * 4);
    iVar1 = *piVar3;
    if (iVar1 != 0) {
      return (char *)((longlong)piVar3 + (longlong)iVar1);
    }
  }
  return (char *)0x0;
}



