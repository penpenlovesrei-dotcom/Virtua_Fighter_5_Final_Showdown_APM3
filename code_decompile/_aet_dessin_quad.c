// ===================================================
// 180025440  ->  FUN_180025440  (entree 180025440)
// ===================================================

void FUN_180025440(longlong *param_1,undefined8 param_2,int *param_3,undefined8 param_4,
                  undefined4 param_5)

{
  int iVar1;
  longlong lVar2;
  int iVar3;
  longlong lVar4;
  
  iVar3 = *param_3 + -1;
  if (-1 < iVar3) {
    lVar4 = (longlong)iVar3 * 0x30;
    do {
      iVar1 = param_3[1];
      lVar2 = 0;
      if (iVar1 != 0) {
        lVar2 = (longlong)(param_3 + 1) + (longlong)iVar1;
      }
      (**(code **)(*param_1 + 0xb8))(param_1,param_2,lVar4 + lVar2,param_4,param_5);
      lVar4 = lVar4 + -0x30;
      iVar3 = iVar3 + -1;
    } while (-1 < iVar3);
  }
  return;
}



