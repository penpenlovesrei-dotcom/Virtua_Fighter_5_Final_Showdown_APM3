// ===================================================
// 180171D20  ->  FUN_180171d20  (entree 180171d20)
// ===================================================

undefined8 FUN_180171d20(longlong param_1,int param_2)

{
  int iVar1;
  undefined8 uVar2;
  
  if ((*(char *)(param_1 + 0x138) == '\0') &&
     (iVar1 = *(int *)(param_1 + 0x5c + (longlong)param_2 * 4), iVar1 != 0)) {
    uVar2 = FUN_180024430(DAT_18066b750,iVar1);
    return uVar2;
  }
  return 0;
}



// ===================================================
// 180172210  ->  FUN_180172210  (entree 180172210)
// ===================================================

void FUN_180172210(longlong param_1,int param_2,int param_3)

{
  if ((*(char *)(param_1 + 0x138) == '\0') &&
     (param_1 = param_1 + ((longlong)param_2 * 0xb + (longlong)param_3) * 4,
     *(int *)(param_1 + 0xc0) != 0)) {
    FUN_180029be0();
    *(undefined4 *)(param_1 + 0xc0) = 0;
  }
  return;
}



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



