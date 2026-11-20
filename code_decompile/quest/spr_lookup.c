// ===================================================
// 18018C420  ->  FUN_18018c420  (entree 18018c420)
// ===================================================

int * FUN_18018c420(longlong param_1,int param_2)

{
  int *piVar1;
  longlong lVar2;
  longlong lVar3;
  int *piVar4;
  
  piVar4 = *(int **)(param_1 + 0x90);
  lVar3 = (*(longlong *)(param_1 + 0x98) - (longlong)piVar4) / 0x58;
  piVar1 = *(int **)(param_1 + 0x98);
  if (0 < lVar3) {
    do {
      lVar2 = lVar3 >> 1;
      if (piVar4[lVar2 * 0x16] < param_2) {
        piVar4 = piVar4 + lVar2 * 0x16 + 0x16;
        lVar2 = lVar3 + (-1 - lVar2);
      }
      lVar3 = lVar2;
    } while (0 < lVar2);
    piVar1 = *(int **)(param_1 + 0x98);
  }
  if ((piVar4 == piVar1) || (param_2 < *piVar4)) {
    piVar4 = *(int **)(param_1 + 0x98);
  }
  piVar1 = DAT_180719910;
  if (piVar4 != *(int **)(param_1 + 0x98)) {
    piVar1 = piVar4 + 2;
  }
  return piVar1;
}



