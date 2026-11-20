// ===================================================
// 822C73C0  ->  FUN_822c73c0  (entree 822c73c0)
// ===================================================

undefined8 FUN_822c73c0(int param_1,undefined4 param_2)

{
  bool bVar1;
  undefined8 uVar2;
  int iVar3;
  
  if (*(char *)(DAT_829c649c + 0x10) != '\0') {
    return 0;
  }
  uVar2 = 1;
  switch(param_2) {
  case 1:
    return 1;
  case 2:
    if (*(int *)(param_1 + 0x10) != 0) {
      return uVar2;
    }
    return 0;
  case 3:
    iVar3 = *(int *)(param_1 + 0x10);
    bVar1 = iVar3 == 1;
    break;
  case 4:
    if (*(int *)(param_1 + 0x10) == 1) {
      return uVar2;
    }
    bVar1 = *(int *)(param_1 + 0x10) == 2;
    goto LAB_822c745c;
  case 5:
    iVar3 = *(int *)(param_1 + 0x10);
    bVar1 = iVar3 == 2;
    break;
  default:
    goto switchD_822c7400_caseD_1;
  }
  if (bVar1) {
    return uVar2;
  }
  bVar1 = iVar3 == 3;
LAB_822c745c:
  if (bVar1) {
    return uVar2;
  }
switchD_822c7400_caseD_1:
  return 0;
}



