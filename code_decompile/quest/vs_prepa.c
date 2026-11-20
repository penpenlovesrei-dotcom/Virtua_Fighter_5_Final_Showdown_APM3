// ===================================================
// 1800B3100  ->  FUN_1800b3100  (entree 1800b3100)
// ===================================================

void FUN_1800b3100(longlong param_1)

{
  longlong lVar1;
  longlong lVar2;
  
  lVar2 = (longlong)*(int *)(param_1 + 8);
  lVar1 = param_1 + 0x4e0;
  if (*(int *)(param_1 + 0x4e8) == 0) {
    FUN_1800b3340(lVar1,*(int *)(param_1 + 8));
    *(undefined1 *)(lVar2 + 0x5d + lVar1) = 0;
    FUN_1800b1be0(lVar1);
    *(undefined4 *)(param_1 + 0x30 + lVar2 * 4) = *(undefined4 *)(param_1 + 0x4fc + lVar2 * 4);
    *(undefined4 *)(param_1 + 0x38 + lVar2 * 4) = *(undefined4 *)(param_1 + 0x504 + lVar2 * 4);
  }
  else if (*(int *)(param_1 + 0x4e8) == 1) {
    FUN_1800b3340(lVar1,0);
    FUN_1800b3340(lVar1,1);
    FUN_1800b1be0(lVar1);
    *(undefined4 *)(param_1 + 0x30) = *(undefined4 *)(param_1 + 0x4fc);
    *(undefined4 *)(param_1 + 0x38) = *(undefined4 *)(param_1 + 0x504);
    *(undefined4 *)(param_1 + 0x34) = *(undefined4 *)(param_1 + 0x500);
    *(undefined4 *)(param_1 + 0x3c) = *(undefined4 *)(param_1 + 0x508);
    return;
  }
  return;
}



// ===================================================
// 1800B2450  ->  FUN_1800b2450  (entree 1800b2450)
// ===================================================

longlong FUN_1800b2450(longlong param_1,int param_2)

{
  return param_1 + 0x68 + (longlong)param_2 * 0x5a0;
}



