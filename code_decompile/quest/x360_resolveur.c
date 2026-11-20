// ===================================================
// 822C7468  ->  FUN_822c7468  (entree 822c7468)
// ===================================================

void FUN_822c7468(int param_1)

{
  char cVar1;
  int iVar2;
  undefined4 uVar3;
  
  if ((*(int *)(param_1 + 0xc) == 1) || (*(int *)(param_1 + 0xc) == 3)) goto LAB_822c7518;
  iVar2 = *(int *)(param_1 + 0x14);
  cVar1 = FUN_822c73c0();
  if (cVar1 == '\0') goto LAB_822c7518;
  switch(iVar2 + -1) {
  case 0:
    uVar3 = 1;
    *(undefined4 *)(param_1 + 0x18) = 1;
    break;
  case 1:
    *(undefined4 *)(param_1 + 0x18) = 3;
    *(undefined4 *)(param_1 + 0x1c) = 1;
    goto switchD_822c74c0_default;
  case 2:
    uVar3 = 2;
    break;
  case 3:
    uVar3 = 3;
    break;
  case 4:
    uVar3 = 1;
    break;
  default:
    goto switchD_822c74c0_default;
  }
  *(undefined4 *)(param_1 + 0x1c) = uVar3;
switchD_822c74c0_default:
  *(undefined4 *)(param_1 + 0x14) = 0;
LAB_822c7518:
  *(undefined4 *)(param_1 + 0xc) = *(undefined4 *)(param_1 + 0x18);
  *(undefined4 *)(param_1 + 0x10) = *(undefined4 *)(param_1 + 0x1c);
  return;
}



