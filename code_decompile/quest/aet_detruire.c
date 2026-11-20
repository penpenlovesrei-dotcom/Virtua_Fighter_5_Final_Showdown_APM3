// ===================================================
// 1801721D0  ->  FUN_1801721d0  (entree 1801721d0)
// ===================================================

void FUN_1801721d0(longlong param_1,int param_2)

{
  if ((*(char *)(param_1 + 0x138) == '\0') &&
     (*(int *)(param_1 + 0x5c + (longlong)param_2 * 4) != 0)) {
    FUN_180029be0();
    *(undefined4 *)(param_1 + (longlong)param_2 * 4 + 0x5c) = 0;
  }
  return;
}



// ===================================================
// 180171070  ->  FUN_180171070  (entree 180171070)
// ===================================================

undefined4 FUN_180171070(longlong param_1,int param_2)

{
  char cVar1;
  undefined4 uVar2;
  
  uVar2 = 1;
  if (*(char *)(param_1 + 0x138) != '\0') {
    return 1;
  }
  if (*(int *)(param_1 + 0x5c + (longlong)param_2 * 4) != 0) {
    cVar1 = FUN_180029770();
    uVar2 = 1;
    if (cVar1 == '\0') {
      uVar2 = 0;
    }
  }
  return uVar2;
}



